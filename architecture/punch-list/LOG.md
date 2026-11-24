# Punch-list evidence log

Newest first. One entry per cell you change in [MATRIX.md](MATRIX.md): row, instance, result, the command, and a short output excerpt. No secrets.

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
