# Punch-list evidence log

Newest first. One entry per cell you change in [MATRIX.md](MATRIX.md): row, instance, result, the command, and a short output excerpt. No secrets.

## 2026-11-24 (night) — TMD v2.9.1-beta cut and rolled out to both hosts

Chris merged PR #197 (the fix) and told me to cut 2.9.1 and roll it out. The fix was not live on either host until this entry: a bogus address sent with `id: this-backend` still failed on both (old code).

**Release.** `fix/this-backend-engine-url` merged as `cd22ff79` (PR #197, TRU-36). Release branch `release-v2.9.1` from that commit: `05fd62f8` "Release v2.9.1", the same 9 files as the 2.9.0 release (root, server, web, shared and desktop `package.json`, `Cargo.toml`, `Cargo.lock`, `openapi.yaml`, and the dated changelog entry); the diff is only the 2.9.0 → 2.9.1 version lines. PR #198 is open and **not merged**. Plain git tag `v2.9.1-beta` on `05fd62f8` (previous tags are lightweight too) and a GitHub pre-release with the changelog text. The tag points at the release-branch commit, which reaches `main` when #198 is merged with a merge commit, as with 2.9.0.

**mahoney-mac.** Clean worktree `~/Claude/TrueMotive/worktrees/tmd-v2.9.1-beta` at the exact tag (SHA checked first). Backups in `audit/backups/`: `truemotive-pg-before-v2.9.1-20261125T044858Z.sql` (51,502 bytes) and the `.env`. Rollback image `mediamesh-truemotive:rollback-v2.9.0-20261124` (`3138bd236031`). Built (`f6c44689569c`), then only TMD was recreated: healthy, 0 restarts, `/api/health` 2.9.1, revision `05fd62f8`; `/`, `/tv/`, `/builder/` 200; NPM reloaded (TRU-35).

**turbo-1.** Same recipe from `~/src/tmd-v2.9.1-beta`; backup `~/pre-v2.9.1-2026-11-24/` (`pg-dumpall.sql` 66,705 bytes, `env.before-v2.9.1`), rollback image `rollback-v2.9.0-20261124`, image built (`4fd34e00ba3f`) before TMD was recreated, then only TMD: healthy, 0 restarts, 2.9.1, revision `05fd62f8`. The engine and the other services were not touched, so there was no stream gap.

**The fix, proven live on both hosts.** `POST /api/hosts/test` with `{"id":"this-backend","engineUrl":"https://nowhere.invalid"}` → `{"ok":true,"status":200,...}` (the backend tested its own engine); with `{"id":"lab",...}` and the same address → `ok:false` (other hosts still test what they are given).

**turbo-1 profile restored.** "This backend" `engineUrl` is back to `https://turbo-1.mastodon-adder.ts.net` (one `PUT /api/profiles/this-backend`; `mediameshPath` stays `/mediamesh`, `allowConfigWrites` still false). The test as the UI sends it (id plus that saved address) → `ok:true`, and `/hls/stream-unavailable/index.m3u8` through the front door → 200, so the side effect noted in the previous entry (an internal HLS link) is gone on turbo-1. The mac's profile (`:8443`, named "Local Mac Tailnet") was not touched; its test now passes, but its links still use the stale Caddy port (TRU-37).

**Checks.** mahoney-mac `verify.sh`: 19 pass, 0 warn, 0 fail, 1 skip (X3, UDP media ports). turbo-1 `sanity.sh`: 26 pass, 2 warn, 0 fail (K2 on the two RIST receivers, `RestartCount=1`); turbo-1 `verify.sh` on the host: 18 pass, 1 warn (Z1 looks for a backup under the Mac's path), 0 fail, 1 skip. M1 reports 2.9.1 built from `v2.9.1-beta` on both.

**Not done.** #198 is not merged. `git fetch --tags` in the Mac's main TMD checkout exits 1 on a stale local tag `v1.3.0` ("would clobber existing tag"); it is unrelated and I did not force it. The `engineForJob` change and the Hosts page marker have no automated test (stated in #197).

## 2026-11-24 (late) — turbo-1: "This backend" host entry fixed (Hosts > Test connection)

**Symptom.** Test connection for "This backend" failed on turbo-1. **Cause.** The saved profile had `engineUrl: https://turbo-1.mastodon-adder.ts.net` (the front door). The test is made by the TMD server, from inside its container: `POST /api/hosts/test` fetches `<engineUrl>/channels/list`. On turbo-1 the container cannot reach its own tailnet name ("Couldn't connect to that address", 3 ms); the Mac only worked by accident of Docker Desktop's routing. A browser `GET /api/hosts/test` is a 404 on both hosts by design: the route is `POST` only.

**Change** (one `PUT /api/profiles/this-backend` through the app's own API; the profile before is kept in the session scratchpad only):

| Field | Before | After |
|---|---|---|
| `engineUrl` | `https://turbo-1.mastodon-adder.ts.net` | `http://engine:8888` (the backend's own `TMD_ENGINE_URL`; the Hosts page marks the entry as the backend's target when they match, and the server then uses its default engine client) |
| `mediameshPath` | `~/src/mediamesh` (a host path the container cannot resolve) | `/mediamesh` (what `/api/status` reports as the backend's target) |
| `dockerHost`, `tailnetHost`, `composeFiles`, `allowConfigWrites`, `name` | unchanged | unchanged (`unix:///var/run/docker.sock` kept as asked; the container really uses `tcp://docker-proxy:2375`, and no code connects through this field) |

**Verified.** `GET /api/profiles` shows the new values; `POST /api/hosts/test` with that `engineUrl` → `{"ok":true,"status":200,"ms":2}`; `/api/status` `target.engineUrl` equals the profile's. TMD 0 restarts. The other profile (`mahoney-mac`) was not touched.

**Known side effect.** The Hosts page builds the HLS link as `<engineUrl>/hls/<channel>/index.m3u8`, so that link now shows the internal `http://engine:8888/...` address, which a browser cannot open. The front-door address (`https://turbo-1.../hls/...`) works. TMD has one field for two jobs (server-side engine address and browser links); a separate public address needs a TMD change. Its other service links still use the retired Caddy port map (`:8445` and friends).

**Same problem elsewhere, not changed.** `mahoney-mac`'s "This backend" is named "Local Mac Tailnet", `engineUrl` `https://mahoney-mac...:8443` (a Caddy port that no longer exists), so its test fails too; and turbo-1's `mahoney-mac` entry has the same `:8443`. Turbo-1's environment has `TMD_CONFIG_WRITES=on`, so config edits are enabled there whatever any profile says.

## 2026-11-24 (late) — turbo-1 brought to parity with mahoney-mac

Authorised by Chris ("go for turbo-1 and see if we can get parity with the mac"). All commands ran over SSH with `~/.ssh/id_rsa_ish`; nothing was run with a prompt, and each step was checked before the next.

1. **Backup (A5).** `~/pre-parity-2026-11-24/` on turbo-1 (mode 600 where secret): `pg-dumpall.sql` (60,787 bytes), `decisions-pg-dumpall.sql` (7,171), `env.before-parity`, container inspects for truemotive, engine, mediamtx, web, occc-ui, spacecom and edge, `state-configs.tgz`, `serve-status.txt`, `build-truemotive.log`. The running TMD image was tagged `mediamesh-truemotive:rollback-v2.8.2-20261124` (`be047528db7f`).
2. **mediamesh (A1).** `git merge --ff-only origin/main`: `1d531f9` → `6f12d4d`; 5 files (`docker-compose.yml`, `docker-compose.edge.yml`, `edge/proxy-host.json`, `mediamtx/mediamtx.yml`, `.env.example`). No source change, so only TMD needed an image build.
3. **TMD (A3).** New worktree `~/src/tmd-v2.9.0-beta` at exactly `v2.9.0-beta` (`7cda41b0`, checked before creating it). `.env`: `TRUEMOTIVE_DESKTOP_PATH` and `TRUEMOTIVE_GIT_SHA` updated; `MTX_WEBRTC_ADDITIONAL_HOSTS=100.124.160.30,turbo-1.mastodon-adder.ts.net` added. `docker compose build truemotive` → exit 0 (image `c70363ba0402`). Turbo's `.env` is not valid shell (line 66), so it must not be sourced; compose and `edge.sh` read it fine.
4. **Recreate TMD.** `up -d --no-build --no-deps truemotive`: healthy, 0 restarts, `/api/health` → `2.9.0`, revision label `7cda41b0`, `127.0.0.1:4715` only. Migrations were already 001–010, so no schema change. `/`, `/tv/`, `/builder/` → 200.
5. **Recreate web, occc-ui, spacecom, engine, mediamtx** (03:08:33 → all healthy by 03:08:56 UTC). All five `unless-stopped`; `8080`, `5173`, `8787`, `8888` and `9997` now on `127.0.0.1`. `stream-unavailable` is the fallback channel the API starts on every boot; it was streaming at the next check. The stream gap was not measured.
6. **Edge.** `scripts/edge.sh provision` → "updated proxy host turbo-1.mastodon-adder.ts.net"; `nginx -t` ok; `nginx -s reload`; `truemotive`, `engine` and `mediamtx` resolve inside NPM (TRU-35).

**Evidence.**
* `sanity.sh` (from the Mac): 26 pass, 2 warn, 0 fail. F1, F2 and K4 now pass; A1 `6f12d4d`; C2 `2.9.0`; D6 no extra serve entries; disk 97 GB free. Warns: K2 `rist-receiver` and `rist-receiver-dante` `RestartCount=1` (not recreated; cause not investigated).
* `verify.sh` on the host (scripts copied to `/tmp/tm-verify`, run, deleted): 18 pass, 1 warn, 0 fail, 1 skip. M1 to M4 pass, M5 3 orgs and 3 users, R1 to R8 pass (`/mcp` handshake, `/hls/` playlist, WHEP OPTIONS 204, spoof tests), N1 live NPM equals `edge/proxy-host.json` (4 locations), X1 13 published entries all on the documented list, X2 TCP media ports open. Z1 warns only because the script looks for a backup under the Mac's `audit/backups` path. With `--media`: W1 to W4 pass (ready path, WHEP 201, `https://` Location, session deleted); W5 browser playback is manual and was not done; 22 pass, 1 warn, 0 fail, 2 skip. No test path was left in mediamtx (`/v3/paths/list` empty).
* C5 from the TMD container (`node -e fetch`): `occc-ui` 200, `docker-proxy` 200, `engine` 200.
* F3 probe from the Mac (read-only, TCP connects and STUN binding requests): 1935, 8889, 7880, 7881 open; `8080`, `5173`, `8787`, `8888`, `9997` closed; `3479/udp` replied; `8189/udp` no reply (inconclusive, same as on the Mac). RIST, SRT and the livekit UDP range unproven.

**Not done, and why.** The direct-consumer inventory the F gate calls for was not run on turbo-1; anything on a peer that used `turbo-1:8080/5173/8787/8888/9997` is now broken. `~/src/truemotive-desktop` (12 uncommitted files) and the `NPM_ADMIN_PASSWORD` line in `.env` were left alone. B4, D12 (drill), G2, G3 and E3–E5 are open.

## 2026-11-24 (late) — mahoney-mac re-verified on TMD 2.9.0; turbo-1 re-checked read-only

**mahoney-mac, A3 re-pinned.** The stack was rebuilt from tag `v2.9.0-beta` (`7cda41b0`, the latest release, pre-release published 2026-11-25 02:03 UTC) after the entry below; I did not do that rebuild and found it by inspection. `/api/health` → `2.9.0`; image revision label `7cda41b0`; `.env` `TRUEMOTIVE_DESKTOP_PATH` → `worktrees/tmd-v2.9.0-beta`. Range `v2.8.2-beta..v2.9.0-beta` is 36 commits and includes builder-v3 (#192) and `/builder/` (#194); `GET /builder/` through the front door → 200.

**Re-verification (read-only).** `sanity.sh`: 23 pass, 2 warn, 0 fail. Warns: K2 `rist-receiver-dante` `RestartCount=1` (started 02:54:01 UTC, healthy since); D6 the three documented dev `tailscale serve` entries (`:8457`, `:9998`, `:9999`). `verify.sh`: 19 pass, 0 fail, 1 skip (X3, UDP media ports; see F3). M3: migrations 001–010 applied, no gaps (also re-read from `schema_migrations`: ids `001_orgs_users_events_audit` … `010_media_library`, 2026-11-21). R6: `/mcp` completes an MCP `initialize` over the front door. N1: live NPM matches `edge/proxy-host.json`.

**F3 stays 🟡.** From turbo-1 (a second tailnet device), a read-only probe of the mac's tailnet name: TCP `1935`, `8889`, `7880`, `7881` open; `3479/udp` (livekit TURN) replied to a STUN binding request; `8189/udp` (mediamtx WebRTC ICE) gave no reply. That last one is inconclusive, not a failure: mediamtx logs `[WebRTC] … :8189 (UDP/ICE)` and `[SRT] … :8890 (UDP/SRT)`, and pion answers STUN only with a valid ICE username. RIST (9000, 9100, 9220–9222, 9300–9399, 9800–9811), SRT `8890` and the livekit media range `50100–50200` need a real sender or a browser. The probe script was copied to `/tmp` on turbo-1, run, and deleted.

**Linear (read, now connected):** TRU-9 (pin to `v2.8.2-beta`) is superseded by this pin; TRU-6 has PR #194 merged but its plan still lists the guarded save, embed protocol and Graph tab swap; TRU-29 and TRU-30 are mac-done and wait on turbo-1.

**Still open on mahoney-mac:** E3, E4, E5 (TRU-5 phases 4, 3, 2), G2 (TRU-15, shelved), and the UDP part of F3. A running channel, `stream-unavailable` (HLS fresh), is running now and was not running this morning; I did not start or touch it.

**turbo-1 (read-only, key `~/.ssh/id_rsa_ish`, not the default agent):** `sanity.sh` 22 pass, 3 warn, 3 fail. Fails: F1 and F2, ports `8080`, `5173`, `8787`, `8888`, `9997` on `0.0.0.0` and answering from the mac. Warns: K4 no restart policy on `web`, `occc-ui`, `engine`, `spacecom`, `mediamtx`; K2 `rist-receiver` and `rist-receiver-dante` `RestartCount=1`. TMD 2.8.2 (`ea67e119`); source checkout `~/src/truemotive-desktop` at `v2.8.0-beta-4-g2520cf2e` with 12 uncommitted files; mediamesh `main` @ `1d531f9`; `/` disk 89% (101 GB free); one running channel, `stream-unavailable`. Nothing was changed.

## 2026-11-24 (night) — mahoney-mac: A3, B4, C3, D12, E6, E7, G1 closed; F3 partly; G2 shelved

PRs #86 and #87 are merged (`c07050c1`, `6f12d4dd`); the checkout is on `main` @ `6f12d4d` with no tracked changes.

**A3 ✅ (TMD moved to the tag).** `git diff --quiet ea67e119 v2.8.2-beta` → trees identical, so the move changed provenance, not behaviour. Backups first in `~/Claude/TrueMotive/audit/backups/` (`truemotive-pg-before-a3-20261124T181823.sql` 51,502 bytes, `env.mac-before-a3-…`). Worktree `worktrees/tmd-v2.8.2-beta` (detached at `d62c01dc`); `.env` `TRUEMOTIVE_DESKTOP_PATH` and `TRUEMOTIVE_GIT_SHA` updated (the old SHA was `cad9c259`, the v2.6.4 merge, so the image revision label had been wrong). `docker compose build truemotive`, `up -d --no-deps truemotive`: healthy, `/api/health` → `2.8.2`, image revision label `d62c01dc…` equals the worktree HEAD, `RestartCount 0`, only `127.0.0.1:4715` published, `GET /` 200 and `/api/session` `via: tailnet` through the tailnet name, 0 error lines. Postgres was not recreated.

**B4 ✅ (restore drill).** `pg_dumpall` of the live database (51,502 bytes) restored into a throwaway `postgres:16-alpine` (no published ports): no restore errors, row counts identical in all 21 tables (`audit_log=25`, `users=3`, `memberships=3`, `orgs=1`, `identity_links=3`, `schema_migrations=10`). Scratch container and dump removed. Now `verify.sh --drills` Y1.

**C3 ✅.** `select * from schema_migrations` → `001_orgs_users_events_audit` … `010_media_library`, applied 2026-11-21, no gaps. `verify.sh` M3.

**D12 ✅.** The committed export is `edge/proxy-host.json` (declarative). A blank NPM 2.16.0 (fresh volumes, loopback `:18081` only) provisioned by the real `scripts/edge.sh`: "created the NPM admin", "created proxy host", a second run "updated proxy host"; `nginx -t` successful; the live proxy host equals it field for field (only NPM's own defaults differ). Scratch removed. Now `verify.sh --drills` Y2 and `verify.sh` N1 for ongoing drift (N1 was shown to catch a doctored config: `DIFFERS: location /whep/ forward_port: live=8889 committed=9999`).

**E6 ✅ and E7 ✅ (TRU-5 phase 1, mediamesh #86/#87).** Routes `/hls/` → `engine:8888` (path unchanged) and `/whep/` → `mediamtx:8889` (prefix stripped, `Location` rewritten to `https://<host>/whep/…`), both with `strip-identity.conf`; mediamtx joined the `edge` network first, then `scripts/edge.sh provision` ("updated proxy host", `nginx -t` OK). Proven first in a scratch stack, 14 of 14 checks (real mediamtx image and config, blank NPM from the branch's file, a stub that records headers): path unchanged, forged `Tailscale-User-Login`/`X-TMD-Proxy-Secret` never reach the upstream, `/` and `/mcp` still work, WHEP offer 201, DELETE at the returned path 200/204. Live through the tailnet name: `/hls/<channel>/index.m3u8` 200 playlist; `OPTIONS /whep/x/whep` 204. **In a real browser over https** (`https://mahoney-mac.mastodon-adder.ts.net/whep/<path>/`, a 150 s test stream into mediamtx): `OPTIONS` 204, offer `POST` 201, ICE `PATCH` 204, video 640x360, `paused false`, `currentTime` 6.88 → 8.88 ([screenshot](../../screens/whep-e2e-front-door-2026-11-24.png)).

**Found while doing E7 (fixed):** `mediamtx.yml` had `webrtcAddress: :8189` (the UDP media port), so the WHEP HTTP listener sat on TCP 8189 and nothing listened on the published `8889` (`curl -X OPTIONS 127.0.0.1:8889` → connection refused). Now `:8889`. mediamtx also advertised only container IPs (`172.18.0.14`, `172.22.0.5`), unreachable from a browser, so no video would flow; `MTX_WEBRTC_ADDITIONAL_HOSTS` (documented in `.env.example`, set per host) now feeds `MTX_WEBRTCADDITIONALHOSTS` and `/v3/config/global/get` shows the tailnet IP and name. No new port opened (`8889/tcp` and `8189/udp` were already published).

**Found (not fixed): NPM pins upstream IPs.** The live config has static `proxy_pass http://truemotive:4716;` per location. nginx resolves those names once at config load, so recreating a routed container with a new IP leaves its route on the old one until NPM reloads. It held through today's TMD and mediamtx recreates because the IPs were reused; a 502 right after `provision` was the old upstream port before the reload finished, and cleared in seconds.

**G1 ✅.** [instances/mahoney-mac/README.md](../instances/mahoney-mac/README.md) rewritten against the live instance (it still said `main` @ `1d531f9`, loopback fix unmerged, MCP broken).

**F3 🟡.** Published beyond loopback (`docker ps`, project `mediamesh`) equals the documented media-port list exactly; TCP 1935, 8889, 7880, 7881 accept connections on `100.126.119.105` (`nc -z`). Portainer (separate project) also publishes 8000 and 9443. UDP reachability from a second tailnet device is untested (turbo-1 SSH key not loaded).

**G2 ⬜ shelved (TRU-15).** `v2.8.0-beta` (`d7038dda`) built into a throwaway image; with the pre-A3 backup restored into a scratch Postgres (21 tables, 10 migrations) it started healthy under default auth, 0 restarts, no database errors. Not proven: reading the restored data (the admin routes need `TMD_AUTH=session`). With `TMD_AUTH=session` the container exited at startup and the cleanup removed its logs, so the cause is unknown.

**New tooling.** `truemotive-skillz` `verify.sh` (commit `b9209bd`): functional verification, read-only by default, `--media` and `--drills` opt-in. Full run on this instance: everything passes except K5 at the time (disk). K5 is now an absolute floor, 30 GB available (`1391d26`): 34 GB available now. Free space fell from about 50 GB to 34 GB during today's image builds.

## 2026-11-24 (late night) — mahoney-mac: `/mcp` through the front door (ADR 0007)

**mahoney-mac, `/mcp` ✅** (mediamesh branch `feat/edge-mcp-route`, PR #86, merged later the same night as `c07050c1`)
- Decision: any registered tailnet device may use `/mcp`; no edge allowlist ([ADR 0007](../adr/0007-route-the-mcp-endpoint-through-the-front-door.md)).
- `docker-compose.edge.yml`: `engine` also on the `edge` network; `edge/proxy-host.json`: location `/mcp` → `engine:8888`. `docker compose … up -d --no-build --no-deps engine` (healthy), `scripts/edge.sh provision` → "updated proxy host", `nginx -t` OK.
- From this Mac over its tailnet name: `POST https://mahoney-mac.mastodon-adder.ts.net/mcp` `initialize` → `mediamesh 2.0.0`; `tools/list` → 64 tools. `/` 200, `/tv/` 200, `/api/session` still resolves the caller.
- `docker port mediamesh-engine-1 8888` → `127.0.0.1:8888`; `http://100.126.119.105:8888/mcp` → connection refused.
- Client `~/.claude.json` now `https://mahoney-mac.mastodon-adder.ts.net/mcp` (was loopback, interim). Not yet tested from a different tailnet device: turbo-1 SSH key not loaded.

## 2026-11-24 (late night) — mahoney-mac: PRs #84 and #85 merged, MCP restored

**mahoney-mac, A1 ✅, F1 ✅, F2 ✅, K4 ✅** (no new MATRIX cell; F1/F2 were already ✅ from the branch, now from `main`)
- mediamesh PR #84 (loopback ports) merged as `d0a1050`; PR #85 (restart policy for `web`, `occc-ui`, `engine`, `mediamtx`, `spacecom`) merged as `11d9d70`. Checkout moved from `fix/loopback-ui-and-control-ports` to `main` @ `11d9d70`.
- `docker compose -f docker-compose.yml -f docker-compose.edge.yml up -d --no-build --no-deps web occc-ui spacecom engine mediamtx`: all five healthy within 15 s.
- `docker inspect` over every running container: `restart=unless-stopped` on all 19 stack containers, `always` on Portainer (outside the stack). `rist-receiver` and `rist-receiver-dante` still show `RestartCount 20` from the earlier boot-order loop (recreate to reset).
- Ports: web `127.0.0.1:8080`, occc-ui `127.0.0.1:5173`, spacecom `127.0.0.1:8787`, engine `127.0.0.1:8888`. `/api/health` → 2.8.2; engine `/publish/manifest` 200; `https://mahoney-mac.mastodon-adder.ts.net/tv/` 200.

**TMPC MCP, interim fix.** `~/.claude.json` entry `truemotive-master-control-program` now `http://127.0.0.1:8888/mcp` (was the tailnet name on :8888, refused after F). POST `initialize` → `mediamesh 2.0.0`; `/mcp` reconnected in Claude Code; `get_publish_manifest` returned `channels: []` (nothing running). Works on this Mac only. The route for other peers is TRU-7; the per-instance requirement is TRU-30. turbo-1's F gate (TRU-16) must not close its ports before that route exists.

## 2026-11-24 (late) — turbo-1: TMD crash loop found and fixed

Tool: `truemotive-instance-sanity` over ssh (`chris@turbo-1.mastodon-adder.ts.net`, key `~/.ssh/id_rsa_ish`, checkout `/home/chris/src/mediamesh`). Host: Ubuntu 24.04.5, Docker 29.9.2.

**Found (prod was out of service):** `mediamesh-truemotive-1` `Restarting (2)`, `RestartCount=57`, `127.0.0.1:4715` not published, front door hung (`GET /` timed out, 0 bytes). Log: `Syntax error: end of file unexpected (expecting "}")` on every start. The container (created 22:22Z) carried a start command split on spaces into separate arguments (`["sh","-c","[ -n \"$TMD_TOKEN\" ] || { echo TMD_TOKEN","is","not",...]`), so `sh -c` got a broken fragment. The image's own default command is correct (same image id `be047528db7f` as `mediamesh-truemotive:latest`), and the rendered compose has no `command:` for `truemotive`. **What created the container with that command is not known**; it was not the repo's compose. Checkout was clean on `main` @ `1d531f9`.

**Fix (approved by Chris):** `docker compose up -d --no-build --no-deps --force-recreate truemotive` from the checkout. Only TMD recreated; Postgres and the other services untouched.
- `/api/health` → `{"ok":true,"version":"2.8.2","profile":null}` within ~10 s; `RestartCount=0`; command now the image default; `docker port` → `127.0.0.1:4715`.
- From this Mac: `GET /` 200, `GET /tv/` 200.
- Re-run of the check: 22 pass, 3 warn, 3 fail. Remaining findings are the known ones below.

**Still open on turbo-1** (unchanged by this fix):
- `F1`/`F2`: web 8080, occc-ui 5173, spacecom 8787, engine 8888, mediamtx 9997 published on `0.0.0.0` and `[::]`. New: the reachability probe from the tailnet confirms all five answer (TRU-16).
- `K4`: occc-ui, web, engine, spacecom, mediamtx have no restart policy (TRU-29).
- `K2`: rist-receiver and rist-receiver-dante `RestartCount=1`.
- `C1` needs the 10-minute recheck of 0 restarts (TMD recreated about 23:20Z).

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
