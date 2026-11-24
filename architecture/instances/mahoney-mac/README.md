# mahoney-mac — dev

MacBook running Docker Desktop. Tailnet name `mahoney-mac.mastodon-adder.ts.net`, tailnet IP `100.126.119.105`. Checkouts: `~/Claude/TrueMotive/mediamesh`, `~/Claude/Projects/truemotive-desktop`, `~/Claude/TrueMotive/occc-ui`.

Acceptance: every required row in the [punch list](../../punch-list/MATRIX.md), column mahoney-mac. Second in order, after turbo-1.

## State at 2026-11-24 (after the fix)

| Item | State |
|---|---|
| TMD | v2.8.2 (release commit `ea67e119`, worktree `~/Claude/TrueMotive/worktrees/tmd-v2.8.2`), healthy |
| mediamesh | `main` @ `1d531f9` in the real checkout. Your earlier edits are in `git stash` (see [log](../../punch-list/LOG.md)) |
| Front door | `tailscale serve` `:443` → `127.0.0.1:8880`; NPM 2.16.0 loopback only |
| Proven | `/`, `/tv/`, tailnet identity, valid certificate ([log](../../punch-list/LOG.md)) |
| Exposure (2026-11-24) | UI and control ports (`8080`, `5173`, `8787`, `8888`, `9997`) are loopback only; running stack was recreated from branch `fix/loopback-ui-and-control-ports` (`9a6e262`, not yet merged to `main`). Side effect: the TMPC MCP server URL in `~/.claude.json` pointed at `:8888` over the tailnet and no longer connects |
| Dev tooling on the same Mac | `tailscale serve` `:9999` → `4712` (host TMD dev app), `:9998` → `9899` (Builder v3 dev server), `:8457` → `10858`. Not part of the instance |
| Docker caveat | host networking does not reach the real host; publish ports instead |

## Per-project notes (older, shallow)

These were written before the 2026-11-24 audit and are partly inaccurate; correct them as each is revisited.

- [code/mediamesh/](code/mediamesh/)
- [code/truemotive-desktop/](code/truemotive-desktop/)
- [code/occc-ui/](code/occc-ui/)

## Clean-room housekeeping

Tear down when no longer needed: `docker compose -p mmaudit down -v` and remove the worktrees under `~/Claude/TrueMotive/audit/`. Not done yet; ask first.
