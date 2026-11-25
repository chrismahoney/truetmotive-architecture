# mahoney-mac — dev

MacBook running Docker Desktop. Tailnet name `mahoney-mac.mastodon-adder.ts.net`, tailnet IP `100.126.119.105`. Checkouts: `~/Claude/TrueMotive/mediamesh` (the stack), `~/Claude/Projects/truemotive-desktop`, `~/Claude/TrueMotive/occc-ui`, and TMD release worktrees under `~/Claude/TrueMotive/worktrees/`.

Acceptance: every required row in the [punch list](../../punch-list/MATRIX.md), column mahoney-mac. Second in order, after turbo-1.

## State at 2026-11-24 (night)

Re-check any row with `verify.sh` (last row of the table); this page goes stale.

| Item | State |
|---|---|
| TMD | v2.9.1 built from tag `v2.9.1-beta` (`05fd62f8`, the latest release) in `~/Claude/TrueMotive/worktrees/tmd-v2.9.1-beta`. `.env` `TRUEMOTIVE_DESKTOP_PATH` and `TRUEMOTIVE_GIT_SHA` point there and the image revision label matches (`verify.sh` M1, M2). 2.9.x includes builder-v3 and the `/builder/` route (PRs #192, #194), which return 200 through the front door. 2.9.1 adds the "This backend" fix (PR #197, TRU-36): the backend's own host always tests and uses `TMD_ENGINE_URL`, whatever address its profile holds. Rollback: image `mediamesh-truemotive:rollback-v2.9.0-20261124` and the worktrees `tmd-v2.9.0-beta` (`7cda41b0`), `tmd-v2.8.2-beta` and `tmd-v2.8.2`; a rollback has not been drilled (TRU-15). The release PR #198 (version bump) is open; the tag points at its commit, so merge it with a merge commit |
| mediamesh | `main` @ `6f12d4d` (PRs #83 to #87 merged), no tracked changes. Earlier local edits are in `git stash` (2 entries, see the [log](../../punch-list/LOG.md)) |
| Front door | `tailscale serve` `:443` → `127.0.0.1:8880`; NPM 2.16.0, admin on `127.0.0.1:8881`. Routes, from `edge/proxy-host.json` (4 locations): `/` → `truemotive:4716` with identity, `/mcp` → `engine:8888`, `/hls/` → `engine:8888`, `/whep/` → `mediamtx:8889` (prefix stripped) |
| Proven | `/`, `/tv/`, tailnet identity and the spoof tests, valid certificate, a real MCP handshake on `/mcp`, `/hls/`, and `/whep/` including video playing in a browser over https. Database restore into a scratch Postgres, and a blank NPM provisioned from the committed file |
| Not yet | `/mediamesh/`, `/spacecom/`, `/decisions/` (TRU-5 phases 2 to 4); the rollback drill G2 (TRU-15, shelved); F3 for the UDP media ports (RIST, SRT, the livekit range): TCP and livekit TURN are proven from turbo-1, the rest needs a real sender or browser |
| Exposure | UI and control ports are loopback only. What is published beyond loopback is exactly the documented media ports. Portainer (a separate project, not part of the stack) also publishes `8000` and `9443`. mediamtx's WHEP listener is `:8889`, and `MTX_WEBRTC_ADDITIONAL_HOSTS` is set to the tailnet IP and name so a browser can receive video |
| Restart policy | every long-running service is `unless-stopped`; the two one-shot perms jobs are `no`. The old `RestartCount 20` on the RIST receivers is gone since the stack was rebuilt for 2.9.0; `rist-receiver-dante` now shows 1, cause not investigated (its log shows it bound and receiving), and `sanity.sh` K2 warns on it |
| Disk | about 42 GB free on the volume holding the stack (`sanity.sh` K5, 2026-11-24 late). `sanity.sh` K5 fails below 30 GB (`DISK_MIN_FREE_GB`). Docker's VM disk holds about 28 GB of real disk; today's image builds are part of that |
| Dev tooling on the same Mac | `tailscale serve` `:9999` → `4712` (host TMD dev app), `:9998` → `9899` (Builder v3 dev server), `:8457` → `10858`. Not part of the instance |
| Docker caveat | host networking does not reach the real host; publish ports instead. NPM resolves each `proxy_pass` name once, at config load, so reload NPM after recreating a routed container |
| Verify | `cd ~/Claude/TrueMotive/mediamesh && ~/Claude/TrueMotive/truemotive-skillz/skills/truemotive-instance-sanity/scripts/verify.sh --host mahoney-mac.mastodon-adder.ts.net` (add `--media` and `--drills` for the end-to-end and scratch checks) |

## Per-project notes (older, shallow)

These were written before the 2026-11-24 audit and are partly inaccurate; correct them as each is revisited.

- [code/mediamesh/](code/mediamesh/)
- [code/truemotive-desktop/](code/truemotive-desktop/)
- [code/occc-ui/](code/occc-ui/)

## Clean-room housekeeping

Tear down when no longer needed: `docker compose -p mmaudit down -v` and remove the worktrees under `~/Claude/TrueMotive/audit/`. The `mmaudit` stack is stopped but its 5 volumes and image are still on disk. Not done yet; ask first.
