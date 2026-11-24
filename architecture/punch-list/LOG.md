# Punch-list evidence log

Newest first. One entry per cell you change in [MATRIX.md](MATRIX.md): row, instance, result, the command, and a short output excerpt. No secrets.

## 2026-11-24 (late) — sanity run and recovery on mahoney-mac

Tool: `truemotive-instance-sanity` (`scripts/sanity.sh --host mahoney-mac.mastodon-adder.ts.net`, from the mediamesh checkout on `fix/loopback-ui-and-control-ports` @ `9a6e262`). Read-only; the recovery steps below are the only changes, and each was approved.

**First run: Docker Desktop was stopped.** `H2` FAIL (no daemon, no `~/.docker/run/docker.sock`), `E1` FAIL (front door 502). Everything not needing Docker matched earlier evidence: `A4` pass, `D5` `:443` → `127.0.0.1:8880`, `D7` cert 45 days left (to 2027-01-09), `D6` extra serve entries `:8457`, `:9998`, `:9999`, `K5` disk 94%.

**After starting Docker Desktop, the stack came back partly.**
- `web`, `occc-ui`, `engine`, `mediamtx`, `spacecom` stayed `Exited (255)`: no `restart:` in `docker-compose.yml`, policy `no`. Tracked as TRU-29 (turbo-1 would do the same after a reboot).
- `C2`/`C4` FAIL: `127.0.0.1:4715` refused. Compose config bound it, but `docker inspect` live ports were empty (Docker Desktop lost the forward on restart). The first version of `C4` passed this; it now requires the port to be present.
- Fix: `docker restart mediamesh-truemotive-1` → `/api/health` `{"ok":true,"version":"2.8.2"}`, `docker port` shows `127.0.0.1:4715`. Then `docker compose up -d --no-build --no-deps` for `web occc-ui engine mediamtx`.
- `spacecom` could not bind `127.0.0.1:8787`: a Cline hub dashboard (PID 10929) held it. Stopped it with Chris's approval, then started `spacecom`. Not restarted since; if it returns, use a port other than 8787.
- `rist-receiver` and `rist-receiver-dante` crash-looped (`Name does not resolve: engine`) until the engine was up, then settled (known boot-order behaviour); `RestartCount` stays 20 until recreated.

**Final run: 20 pass, 5 warn, 0 fail, 0 skip.** Warns: `A1` branch not `main` (TRU-8), `K5` disk 94%, `K2` x2 receiver restart counts, `D6` the three dev serve entries. No MATRIX cell changed: C2, C4, F1, F2, D5 and D7 were already ✅ for mahoney-mac and still hold.

**F1/F2 reachability, new evidence.** The script now also connects to 8080, 5173, 8787, 8888 and 9997 on the tailnet name from this machine: nothing answers (confirms the loopback binding, not just the compose config).

**Skill fixes made during this run** (in `truemotive-skillz`, not yet committed): a crashed or empty run no longer exits 0; checks skipped for lack of Docker are reported `SKIP`; `F1` reachability probe; `C4` requires the published port. Self-test `scripts/test-shims.sh`: 39 of 39 pass.

## 2026-11-24 (night) — loopback ports on mahoney-mac

**mahoney-mac, F1 ✅ F2 ✅** (loopback bindings; branch `fix/loopback-ui-and-control-ports` @ `9a6e262`, not pushed)
- No channels were running (`list_channels`: all `running:false`), so recreating the engine interrupted nothing.
- `docker-compose.yml`: `8080`, `5173`, `8787`, `8888` and mediamtx `9997` now `127.0.0.1:` prefixed. `docker compose -f docker-compose.yml -f docker-compose.edge.yml up -d --no-build --no-deps web occc-ui spacecom engine mediamtx`.
- `docker ps`: web `127.0.0.1:8080`, occc-ui `127.0.0.1:5173`, spacecom `127.0.0.1:8787`, engine `127.0.0.1:8888`, mediamtx `127.0.0.1:9997`. Everything else on `0.0.0.0` is in the [public-media table](../system/04-media-plane.md#ports-that-stay-public-udptcp) (engine udp 9000/9100/9220–9222, mediamtx 1935/8189/8889/8890, ristd, rist receivers, livekit). Portainer `8000`/`9443` is outside this stack ([adjacent services](../system/07-adjacent-services.md)).
- From the Mac's own tailnet address (`100.126.119.105`) ports 8080, 5173, 8787, 8888, 9997 → connection refused; on `127.0.0.1` → 200/200/200/404/404 (404 is the API root, `/publish/manifest` → 200). `https://mahoney-mac.mastodon-adder.ts.net/` and `/tv/` still 200. TMD `/api/health` → `2.8.2`; all stack containers healthy, 0 restarts.
- **Side effect, not a regression of the stack:** the TMPC MCP server is configured as `http://mahoney-mac.mastodon-adder.ts.net:8888/mcp` (`~/.claude.json`), so it now fails with `ECONNREFUSED`. Needs a decision: point it at `http://127.0.0.1:8888/mcp` (works on this Mac only) or route `/mcp` through the front door with identity.

**mahoney-mac, C5 ✅**: from `mediamesh-truemotive-1` (`node -e fetch`, the image has no `wget`): `http://occc-ui:80/` 200, `http://docker-proxy:2375/_ping` 200, `http://engine:8888/publish/manifest` 200. C3 left ⬜: this container's log carries no migration lines to cite.

**turbo-1**: not touched. `ssh chris@turbo-1` → `Permission denied (publickey,password,keyboard-interactive)`; `ssh-add -l` shows no identities (the key used yesterday is not loaded). Tailscale lists it online.

**helpy**: still offline (tailnet: last seen 11 h ago); `ssh chris@helpy` → `Operation timed out`. Planning only, see [helpy](../instances/helpy/README.md#plan).

## 2026-11-24 (evening) — handoff state

- truemotive-desktop: PR #191 (Release v2.8.2) merged, tag `v2.8.2-beta` pushed on `d62c01dc` (plain git tag; there is no Jenkins build, only a Jenkinsfile). PR #192 (Builder Graph v3 package, `apps/builder-v3`) merged at `917e0f77`. `main` is now 2.8.2 plus builder-v3.
- Both hosts still run 2.8.2 from release commit `ea67e119`; they have not been moved to `d62c01dc` / the tag or rebuilt with builder-v3 (nothing serves it yet).
- New channel on the mac instance: `example-test-signal` (folder Examples): `video.testsrc` + 440 Hz `sine` muxed, HLS at `/hls/example-test-signal/index.m3u8`. Saved, compiles, **not started**. Not on turbo.
- Finding: the channel page's existing Graph tab embeds the MediaMesh `web` Builder from the host profile's web origin (`graphAvailability`), which cannot work behind the single front door. Serving builder-v3 from TMD at `/builder/` fixes that.
- Next (agreed): (A) serve builder-v3 at `/builder/` from TMD (Dockerfile builds `@tmd/builder-v3`, server serves its `dist/index.html`, ChannelPage Graph tab embeds `/builder/?channel=<id>`); remove the old `graph3` tab; remove the out-of-date non-built sample channels (`sample`, `mix-1`..`mix-5`) in mediamesh; web-client path refactor for E3–E7; close UI/control ports (F); bring up helpy. Worktree for A: `~/Claude/TrueMotive/worktrees/tmd-builder-embed` (clean, at `origin/main`).


**mahoney-mac (dev), front door live**
- Real checkout moved from `helpy-close-occc-ui-port` to `main` @ `1d531f9`. Uncommitted edits stashed ("pre-edge 2026-11-24"): `mediamtx/mediamtx.yml` had been replaced by an all-commented reference file (it would have removed `api: yes` and the healthcheck endpoint), plus `package-lock.json` and `web/package.json`. The branch keeps its 2 helpy-overlay commits.
- Volumes backed up first (`audit/backups/*.tgz`); the Postgres volume already had the image-default `pg_hba.conf` and the `.env` password matched, so no `ALTER USER` was needed. Decisions DB, ristd data intact.
- TMD v2.8.2 from `~/Claude/TrueMotive/worktrees/tmd-v2.8.2` (commit `ea67e119`). `/api/health` → `2.8.2`. 115 built channels present.
- NPM, `tailscale serve --https=443 http://127.0.0.1:8880`; `:8444` and `:8456` removed. From this Mac as a peer: Let's Encrypt cert for `mahoney-mac.mastodon-adder.ts.net` (to 2027-01-09), `/api/session` = my login, a forged login ignored, `/tv/` and its assets 200. The `rist-receiver*` containers restarted 4 times at start (they come up before the engine; known).
- Left in place on the Mac (dev tooling, not part of the instance): `tailscale serve` `:8457` → `10858`, `:9998` → `9899` (Builder v3 dev server), `:9999` → `4712` (host TMD dev app), and the stale clean-room stack volumes under project `mmaudit` (stopped).

**turbo-1, later the same day**
- `/tv/` assets 404: turbo's `occc-ui` checkout was 4 commits behind `main` (before the embedded `/tv/` build). Updated to `5c75460` (a stashed `package-lock.json` change saved) and rebuilt: assets 200.
- mediamesh PR #83 merged (`1d531f9`); turbo back on `main`. TMD 2.8.2 built from release commit `ea67e119` (truemotive-desktop PR #191, tag `v2.8.2-beta` to be created by the Jenkins release job); `/api/health` 2.8.2, identity and `/tv/` still fine.


**turbo-1, front door live** (mediamesh branch `fix/tmd-listeners-postgres-and-npm-edge` @ `f555385`, PR #83; TMD v2.8.0 `d6d700b2` from a clean worktree `~/src/tmd-v2.8.0`)
- Local mediamesh edits stashed (`git stash list`: "pre-remediation 2026-11-24"); untracked files also saved in `untracked-files.tgz`. TMD's own checkout `~/src/truemotive-desktop` is untouched (still has its local edits).
- Postgres recreated without the file mount. **Finding:** the volume's own `pg_hba.conf` was a custom file (local `peer`, loopback `trust`, no network rule), so TMD got `password authentication failed`. Restored the image default (backup: `volume-pg_hba.conf.before`), then `ALTER USER truemotive` to the `.env` password. B2 ✅ B3 ✅.
- TMD: `{"ok":true,"version":"2.8.0","profile":null}`, restarts 0, only `127.0.0.1:4715` published. C1 C2 C4 ✅. Existing users, orgs and sessions intact.
- NPM 2.16.0 (`docker-compose.edge.yml`, `scripts/edge.sh render|provision`): published `127.0.0.1:8880` (proxy) and `127.0.0.1:8881` (admin). D2 D3 D4 ✅. The proxy secret appears in no git file, NPM config, database or log (D10 ✅).
- `tailscale serve --https=443 http://127.0.0.1:8880` added; `:8444` removed. D5 D6 ✅.
- From the mac as a tailnet peer: valid Let's Encrypt cert for `turbo-1.mastodon-adder.ts.net` (to 2027-02-04), TLS verify OK (D7 ✅); `/api/session` → `via: tailnet`, user = my login, platformAdmin (D8 ✅); a forged `Tailscale-User-Login: boryalic@gmail.com` and forged `X-TMD-Proxy-Secret` sent from the peer were ignored, still resolved to my login (tailscale serve overwrites it); a forged login sent straight to `:4716` → 401 (D9 ✅). `/` 200 and `/tv/` 200 (E1 E2 ✅).


**turbo-1, A5 ✅ backups taken** (read-only on the stack; new files only, in `~/pre-remediation-2026-11-24/` on turbo)
- `pg-dumpall.sql` (57,701 bytes: role `truemotive`, database `truemotive`), `decisions-pg-dumpall.sql` (7,171 bytes), both mode 600.
- `tracked-local-changes.patch` (3,163 lines, mediamesh) and `tmd-tracked-local-changes.patch` (truemotive-desktop, incl. `docker/web/Dockerfile`), `git-status.txt`, `tmd-git-status.txt`, `mediamesh-HEAD.txt` (`78c9a5e`), `tmd-version.txt`, `env.backup` (600), container inspect, last TMD log, `serve-status.txt`.
- Finding: `pg_dumpall` over the socket fails (`Peer authentication failed`); it works over `127.0.0.1` because the unsafe `pg_hba.conf` trusts it. After the fix a password will be required.
- Finding: turbo's untracked files include earlier NPM attempts (`nginx/config.json`, `docs/artifacts/NPM_MIGRATION_RESULT.md`, `plans/MIGRATE_TM_DESKTOP_TO_MEDIAMESH_STACK.md`). To be read before building the edge overlay.

**Clean room (mahoney-mac, project `mmaudit`)**: B1, B2, B3, C1, C2, C3, C5 ✅
- mediamesh `origin/main` `78c9a5e` + [fix patch](../remediation/tmd-restart-loop-fix.patch), TMD `d6d700b2` (v2.8.0).
- `/api/health` → `{"ok":true,"version":"2.8.0","profile":null}`; restarts 0; migrations 001–010 applied.

**turbo-1 (read-only)**
- B1 ✅ `mediamesh-postgres-1 Up (healthy)`; B5 ✅ `127.0.0.1:54329->5432`.
- C1 ❌ `mediamesh-truemotive-1 Restarting (1)`, 44+ restarts, `getaddrinfo EAI_AGAIN postgres`.
- D1 ✅ no Caddy or NPM container running.
- D5/D6 ❌ `tailscale serve`: `https://turbo-1.mastodon-adder.ts.net:8444 → http://127.0.0.1:4715`.
- A2 ❌ ~3,200 lines of local edits ([snapshot](../remediation/turbo-local-changes.txt)).
- A3 ❌ `truemotive-desktop` at `v2.8.0-beta-4-g2520cf2e`.
- F1/F2 ❌ published on `0.0.0.0`: 8080, 5173, 8787, 8888, 9997 and others.

**helpy**: unreachable. `ssh chris@helpy` timed out; tailnet shows offline, last seen 7 h earlier.

**TMD tag**: `git tag` and `gh release list` show no `v2.8.1` or `v2.8.2`. `2.8.1` is an unreleased bump (`aa56351f`) on `feat/current-links`.
