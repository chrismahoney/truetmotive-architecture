# Punch list

An instance is **done** when every required row is ✅ on its host. Work one instance at a time: **turbo-1 (prod) first, then mahoney-mac (dev), then helpy (test)**.

Legend: 🟡 passes, with a named follow-up · ✅ passed (date + evidence in the log below) · ❌ checked and failing · ⬜ not checked yet · ➖ not applicable · ⛔ blocked (see notes). The **Clean room** column is the mahoney-mac throwaway stack (`mmaudit`), which proves a design before it touches a real host.

Last updated: 2026-11-24 (mahoney-mac F1/F2 closed; turbo-1 SSH key not loaded, helpy still offline). Update a cell only with evidence: put the command output summary and date in [LOG.md](LOG.md).

## Where we are

| Instance | Environment | Done | Failing | Not checked | Blockers |
|---|---|---|---|---|---|
| turbo-1 | prod | 25 | 2 | 13 | E3–E7 need the web client path refactor; hosts to move to tag `v2.8.2-beta` |
| mahoney-mac | dev | 28 | 0 | 11 | E3–E7 need the web client path refactor; host to move to tag `v2.8.2-beta`; TMPC MCP only reachable on this Mac (TRU-7, TRU-30) |
| helpy | test | 0 | 0 | 40 | host offline, SSH timeout |

## A. Source and pins

| # | Check | Proof | Clean room | turbo-1 | mahoney-mac | helpy |
|---|---|---|:-:|:-:|:-:|:-:|
| A1 | mediamesh is on the fixed `main` (listener and Postgres fixes merged) | `git log -1`, PR merged | ❌ branch only | ✅ `main` @ `1d531f9` | ✅ `main` @ `1d531f9` | ⬜ |
| A2 | No uncommitted edits to tracked files | `git status --porcelain` is empty | ➖ | ✅ mediamesh clean (edits stashed); TMD built from clean worktree | ✅ edits stashed | ⬜ |
| A3 | TMD built from the target tag `v2.8.2` | `/api/health` `version`; `git describe --tags` | ⛔ tag missing (ran v2.8.0) | 🟡 v2.8.2 running (release commit `ea67e119`); tag `v2.8.2-beta` exists; host not yet moved to it | 🟡 v2.8.2 running (release commit `ea67e119`); tag `v2.8.2-beta` exists; host not yet moved to it | ⬜ |
| A4 | `.env` complete: `TMD_TOKEN`, `TMD_PROXY_SECRET` (32+ chars), `POSTGRES_PASSWORD`, edge settings | `scripts/check-env` (to write) or manual review | ⬜ | ✅ 2026-11-24 | ✅ | ⬜ |
| A5 | Database and config backed up before any change | file exists and non-empty | ➖ | ✅ 2026-11-24 | ✅ volume tarballs | ⬜ |

## B. Postgres

| # | Check | Proof | Clean room | turbo-1 | mahoney-mac | helpy |
|---|---|---|:-:|:-:|:-:|:-:|
| B1 | Postgres healthy | `docker compose ps postgres` healthy | ✅ | ✅ | ✅ | ⬜ |
| B2 | Nothing is bind-mounted into the Postgres data directory | `docker inspect` mounts | ✅ | ✅ | ✅ | ⬜ |
| B3 | TMD's role password equals `.env` | TMD logs show no `password authentication failed` | ✅ | ✅ after `ALTER USER` | ✅ | ⬜ |
| B4 | A backup restores into a scratch Postgres | restore drill, row counts match | ⬜ | ⬜ | ⬜ | ⬜ |
| B5 | Postgres published on `127.0.0.1` only | `docker port` | ⬜ | ✅ `127.0.0.1:54329` | ✅ `127.0.0.1:54329` | ⬜ |

## C. TMD

| # | Check | Proof | Clean room | turbo-1 | mahoney-mac | helpy |
|---|---|---|:-:|:-:|:-:|:-:|
| C1 | Container Up with 0 restarts for 10 minutes | `docker inspect -f '{{.RestartCount}}'` | ✅ | ✅ 0 restarts (recheck at +10 min) | ✅ 0 restarts (recheck at +10 min) | ⬜ |
| C2 | `/api/health` is ok on `127.0.0.1:4715` with the pinned version | `curl -s 127.0.0.1:4715/api/health` | ✅ (v2.8.0) | ✅ v2.8.0 | ✅ v2.8.2 | ⬜ |
| C3 | Migrations applied | TMD log | ✅ 001–010 | ⬜ | ⬜ | ⬜ |
| C4 | Listeners correct: main `127.0.0.1:4712`, token `4715`, proxy `4716` **not published** | `docker port`, `TMD_HOST/PORT` | ⬜ | ✅ only `127.0.0.1:4715` | ✅ only `127.0.0.1:4715` | ⬜ |
| C5 | TMD reaches occc-ui, docker-proxy, engine | exec a request from the container (no `wget` in the image; use `node -e fetch`) | ✅ | ⬜ | ✅ 200 / 200 / 200 | ⬜ |

## D. Edge: front door, proxy, identity

| # | Check | Proof | Clean room | turbo-1 | mahoney-mac | helpy |
|---|---|---|:-:|:-:|:-:|:-:|
| D1 | Caddy removed from the repo and the host (no container, no profile) | `docker ps`, `grep caddy docker-compose*.yml` | ⬜ | ✅ | ✅ stale container removed | ⬜ |
| D2 | NPM runs from `docker-compose.edge.yml` | `docker compose ps` | ✅ | ✅ NPM 2.16.0 | ✅ NPM 2.16.0 | ⬜ |
| D3 | NPM http port published on `127.0.0.1` only | `ss -ltn`, `docker port` | ✅ | ✅ `127.0.0.1:8880` | ✅ `127.0.0.1:8880` | ⬜ |
| D4 | NPM admin UI (:81) loopback only; reachable by SSH tunnel | `ss -ltn` | ✅ | ✅ `127.0.0.1:8881` | ✅ `127.0.0.1:8881` | ⬜ |
| D5 | Exactly one `tailscale serve`: `:443` → `127.0.0.1:EDGE_PORT` | `tailscale serve status` | ➖ | ✅ `:443` → `127.0.0.1:8880` | ✅ `:443` → `127.0.0.1:8880` | ⬜ |
| D6 | Old serve entries removed | `tailscale serve status` | ➖ | ✅ `:8444` off | ✅ `:8444`, `:8456` off | ⬜ |
| D7 | Valid tailnet certificate seen from another tailnet device | `curl -v https://<host>.mastodon-adder.ts.net/` from a peer | ➖ | ✅ Let's Encrypt, expires 2027-02-04 | ✅ Let's Encrypt, expires 2027-01-09 | ⬜ |
| D8 | Visiting `/` signs you in as your tailnet user, no password prompt | browser + TMD `whoami` | ➖ | ✅ `/api/session` = tailnet user | ✅ | ⬜ |
| D9 | Spoof test: forged `Tailscale-User-Login` straight to `4716` or NPM is **rejected** | `curl -H` from the host and from another container | ✅ | ✅ | ✅ | ⬜ |
| D10 | Proxy secret reaches NPM and is **not** in git, the NPM export or any log | `git grep`, review export | ✅ | ✅ | ✅ | ⬜ |
| D11 | NPM has no certificate or SSL setting on any proxy host | NPM UI / export | ✅ | ✅ `certificate_id` 0 | ✅ | ⬜ |
| D12 | NPM configuration export committed and restores a blank NPM | export, wipe volume, import | ⬜ | ⬜ | ⬜ | ⬜ |

## E. Paths: each one valid cert, right container

Every row is proven from a tailnet peer through `https://<host>.mastodon-adder.ts.net<path>`.

| # | Path | Expected container | Clean room | turbo-1 | mahoney-mac | helpy |
|---|---|---|:-:|:-:|:-:|:-:|
| E1 | `/` | `truemotive:4716` | ➖ | ✅ 200 | ✅ 200 | ⬜ |
| E2 | `/tv/` | occc-ui, via TMD | ➖ | ✅ 200, assets 200 after occc-ui update | ✅ 200 | ⬜ |
| E3 | `/mediamesh/` | `web` | ➖ | ⬜ | ⬜ | ⬜ |
| E4 | `/spacecom/` (websocket upgrade works) | `spacecom` | ➖ | ⬜ | ⬜ | ⬜ |
| E5 | `/decisions/` | `decisions` | ➖ | ⬜ | ⬜ | ⬜ |
| E6 | `/hls/` | `engine` | ➖ | ⬜ | ⬜ | ⬜ |
| E7 | `/whep/` | `mediamtx` | ➖ | ⬜ | ⬜ | ⬜ |

*E3–E7 are blocked, not just unchecked: the MediaMesh web client builds `host:port` URLs and has no path-prefix support. See [the finding](../system/01-edge-and-identity.md#path-map).*

## F. Exposure

| # | Check | Proof | Clean room | turbo-1 | mahoney-mac | helpy |
|---|---|---|:-:|:-:|:-:|:-:|
| F1 | No UI or control port on `0.0.0.0` (web 8080, occc-ui 5173, spacecom 8787, engine 8888, …) | `docker ps` ports vs the [media table](../system/04-media-plane.md#ports-that-stay-public-udptcp) | ⬜ | ❌ 8080, 5173, 8787, 8888, 9997 | ✅ 2026-11-24, branch only (see note) | ⬜ |
| F2 | mediamtx control API (`9997`) is loopback only | `docker port` | ⬜ | ❌ | ✅ `127.0.0.1:9997` | ⬜ |
| F3 | Media ports reachable from outside (RIST, SRT, RTMP, WebRTC) | `nc -u`, `ffprobe` per protocol | ⬜ | ⬜ | ⬜ | ⬜ |

*F is required but does not block the first pass on turbo-1 ([agreed sequencing](../adr/0006-pin-released-tmd-tags-never-branches.md)).*

**Gate before closing F on turbo-1: inventory the direct consumers first.** Closing the ports on mahoney-mac cut off one the repo did not know about: the TMPC MCP server in `~/.claude.json` is `http://mahoney-mac.mastodon-adder.ts.net:8888/mcp`, a direct tailnet hit on the engine. Anything else on a peer that uses `host:8080`, `:5173`, `:8787`, `:8888` or `:9997` breaks the same way. The engine's `/mcp` was also reachable by every tailnet device with no identity check, which is the exposure F exists to close; the proper route is through the front door (TMD, with identity), not a reopened port. Mahoney-mac's change is on branch `fix/loopback-ui-and-control-ports` (`9a6e262`), not yet pushed or merged.

## G. Docs and recovery

| # | Check | Proof | Clean room | turbo-1 | mahoney-mac | helpy |
|---|---|---|:-:|:-:|:-:|:-:|
| G1 | The instance page in [instances/](../instances/) matches reality | review | ➖ | ⬜ | ⬜ | ⬜ |
| G2 | Rollback tested: previous TMD tag restored with the database backup | drill | ⬜ | ⬜ | ⬜ | ⬜ |
| G3 | Stale networks reviewed with the owner | [adjacent services](../system/07-adjacent-services.md) | ➖ | ⬜ | ➖ | ⬜ |

## Order of work on turbo-1

```mermaid
flowchart LR
  A["Backup (A5)"] --> B["Stash local edits (A2)"] --> C["Fixed main (A1)"] --> D["Recreate TMD (C1-C5)"]
  D --> E["Edge overlay (D1-D4, D10-D12)"] --> F["Front door (D5-D7)"] --> G["Identity (D8-D9)"] --> H["Paths (E1-E7)"] --> I["Exposure (F)"]
  D -. "after tag v2.8.2 exists" .-> T["Pin (A3)"]
```

Each arrow is a stop: show you the evidence, then continue only on your go.
