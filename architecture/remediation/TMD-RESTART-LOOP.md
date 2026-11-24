# TMD restart loop: audit and remediation plan

Audited 2026-11-23/24. Verified on mahoney-mac (clean room) and observed live on turbo. helpy was unreachable (SSH timeout), so nothing here is verified for helpy.

## Verified result

mediamesh `origin/main` (`78c9a5e`) + TMD `v2.8.0` (`d6d700b2`) + the two compose changes in
[tmd-restart-loop-fix.patch](tmd-restart-loop-fix.patch) bring up the full stack on a fresh install on mahoney-mac:
TMD `{"ok":true,"version":"2.8.0"}`, 0 restarts, Postgres, engine, ristd, preview, mediamtx, occc-ui, web, spacecom, decisions healthy.
LiveKit was left out of the clean room (see finding 6). No Caddy, no NPM.

Clean-room location: `~/Claude/TrueMotive/audit/` (worktrees `mediamesh`, `truemotive-desktop`; compose project `mmaudit`; throwaway config in `audit/state/`). Your real checkouts, stashes and volumes were not touched.

## Root causes

| # | Finding | Evidence | Fix |
|---|---------|----------|-----|
| 1 | **Fresh Postgres cannot initialise.** `dc4d529` bind-mounts a single file over `/var/lib/postgresql/data/pg_hba.conf`, so `initdb` sees a non-empty data dir. Postgres crash-loops, TMD never starts (`dependency postgres failed to start`). | Reproduced on the Mac: `initdb: error: directory "/var/lib/postgresql/data" exists but is not empty`. | Remove the mount and `data/postgres/pg_hba.conf`. |
| 2 | **The pg_hba file is also unsafe.** It trusts `127.0.0.1`, `::1` and a hard-coded `172.24.0.0/16` with no password and has no rule for any other subnet. Docker subnets are not pinned, so on other hosts TMD would get "no pg_hba.conf entry". | `data/postgres/pg_hba.conf` on `origin/main`. | Same fix: the image default (scram-sha-256 over the network) applies. Do not reintroduce `trust`. |
| 3 | **TMD main listener collides with the token listener.** `origin/main` has `TMD_HOST=0.0.0.0` and `TMD_PORT=4715` next to `TMD_TOKEN_LISTEN=0.0.0.0:4715`. v2.8.0 exits 1 with no log output. Session mode needs a loopback main listener. | Reproduced: exit 1 and 0 log lines. With `127.0.0.1:4712` it applies migrations 001-010 and serves. | `TMD_HOST: 127.0.0.1`, `TMD_PORT: "4712"` (already correct on `helpy-close-occc-ui-port`, never reached `main`). |
| 4 | **Turbo is crash-looping on a broken container, on top of 1-3.** The container's first start failed at 22:43 with `Bind for 0.0.0.0:4712: port is already allocated`. Since then every restart dies with `getaddrinfo EAI_AGAIN postgres` (43+ restarts), although a new container on `mediamesh_net` resolves `postgres` in 6 ms. Likely a half-built network attachment (not proven). | `journalctl -u docker`, `docker events`, DNS tests on turbo. | Recreate the container (`up -d --force-recreate truemotive`) after fixing the compose file. |
| 5 | Turbo's working tree carries about 3,200 lines of uncommitted edits ([turbo-local-changes.txt](turbo-local-changes.txt)). They delete the Caddy service and Caddyfile, drop `TMD_PROXY_SECRET` and `TMD_ENGINE_URL`, set `TMD_PORT: ${TMD_PORT}`, and change the published port from `127.0.0.1:4715` to `127.0.0.1:4712`. Turbo's front door is `tailscale serve https://turbo-1.mastodon-adder.ts.net:8444 -> http://127.0.0.1:4715`, so that port change leaves the front door pointing at nothing. | `tailscale serve status` and `docker compose` diff on turbo. | Discard the local edits (after backup) and pull the fixed `main`. |
| 6 | Smaller issues. `livekit` pins `container_name: livekit`, so two compose projects cannot coexist. `api/` is bind-mounted, so a fresh checkout needs `scripts/install-api-deps.sh` before the engine starts (it modifies `api/package-lock.json`). The `Peer authentication failed` Postgres log lines come from the `pg_isready` healthcheck and are harmless. | Clean-room run. | Document, do not fix now. |
| 7 | Mahoney-mac's own volume: the old Postgres logged `password authentication failed for user "truemotive"` at 22:22, which means the volume's role password differs from `POSTGRES_PASSWORD` in `.env` (the env var only applies at first init). | Postgres log on mahoney-mac. | Align with `ALTER USER` (see below), never with `trust`. |

Caddy and NPM: you said both are gone. Confirmed on turbo (no proxy containers). `main` still carries a `caddy` service behind a profile, `caddy/Caddyfile`, and `docker-compose.helpy.yml`, which requires an external `truemotive` network that only NPM created. That overlay will fail on any host without that network. Decision needed: delete the Caddy service and the helpy overlay, or keep them parked.

## Remediation plan (apply in this order)

Do each host separately and stop if a check fails. Every step before "Apply" is read-only or a backup.

### A. Land the fix (once)
1. Create a branch from `origin/main` in mediamesh, apply `tmd-restart-loop-fix.patch`, open a PR. Do not push to `main` directly.
2. Same PR or follow-up: remove the Caddy service and Caddyfile, and decide on `docker-compose.helpy.yml`.
3. Add a one-line startup message to TMD when the main listener and token listener share a port (finding 3 fails silently today).

### B. mahoney-mac (real instance)
1. Back up: `docker run --rm -v mediamesh_truemotive_postgres_data:/v -v $PWD:/b busybox tar czf /b/pg-backup.tgz -C /v .`
2. Switch the checkout to the fixed branch. Your uncommitted edits (`mediamtx/mediamtx.yml`, `package-lock.json`, `web/package.json`) stay in the working tree or a stash; do not discard them.
3. `docker compose up -d` (no `caddy` profile). Check `/api/health` on `127.0.0.1:4715` returns v2.8.0.
4. If TMD logs `password authentication failed`: `docker compose exec postgres psql -U truemotive -c "ALTER USER truemotive PASSWORD '<value of POSTGRES_PASSWORD>'"`.

### C. turbo
1. Backup the DB: `docker exec mediamesh-postgres-1 pg_dumpall -U truemotive > ~/pg-backup-$(date +%F).sql`.
2. Preserve the local edits: `git diff > ~/turbo-local-changes.patch && git stash push -u -m "pre-remediation"`.
3. Pull the fixed `main`, run `scripts/install-api-deps.sh` if `api/package.json` changed.
4. `docker compose up -d --force-recreate truemotive` then the rest.
5. Verify: `curl http://127.0.0.1:4715/api/health` and the tailnet URL `https://turbo-1.mastodon-adder.ts.net:8444`. Check `docker inspect -f '{{.RestartCount}}'` stays 0.
6. Postgres on turbo has an existing volume, so removing the `pg_hba` mount reverts to the image default (password required). If TMD cannot log in, use the `ALTER USER` step from B.4.

### D. helpy (not audited, unreachable)
1. Get SSH working first (`ssh chris@helpy` timed out).
2. Check whether NPM and the external `truemotive` network still exist. If not, the helpy overlay is dead and must not be in `COMPOSE_FILE`.
3. Then apply the turbo procedure.

## Out of scope until the above is verified
Consolidating truemotive-desktop into mediamesh (import with history) and archiving the old repo come after turbo and helpy run the same verified setup.

## Decisions (2026-11-24)

- Caddy is deleted; Nginx Proxy Manager is the proxy ([ADR 0005](../adr/0005-nginx-proxy-manager-as-an-in-repo-edge-overlay.md)). The helpy overlay is replaced by an `edge` overlay.
- The front door is a single `tailscale serve` per host that hands HTTP and identity headers to NPM ([ADR 0002](../adr/0002-terminate-tls-at-the-front-door-only.md), [0004](../adr/0004-identity-is-trusted-only-with-the-proxy-secret.md)).
- Turbo and helpy pin TMD **v2.8.2** ([ADR 0006](../adr/0006-pin-released-tmd-tags-never-branches.md)). That tag does not exist yet.
- Acceptance and order of work: [punch-list/MATRIX.md](../punch-list/MATRIX.md). This page remains the audit record.
