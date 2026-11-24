---
status: accepted
---

# The engine's MCP endpoint is reached through the front door at `/mcp`; the tailnet is the credential

Tracks [TRU-7](https://linear.app/truemotive/issue/TRU-7) (the decision) and [TRU-30](https://linear.app/truemotive/issue/TRU-30) (every instance has it). Decided 2026-11-24. Applied on mahoney-mac; turbo-1 and helpy pending.

## Context

The TMPC MCP server is the engine's own `POST /mcp` (mediamesh `api/src/routes/mcp.js`, stateless Streamable HTTP). Operators and agents on other tailnet machines use it to list, start and stop channels, drive OBS, ingest media and edit channel graphs.

Until 2026-11-24 clients reached it directly at `http://<host>.mastodon-adder.ts.net:8888/mcp`. Closing the engine port to loopback (TRU-8, PR #84) removed that path. For a while it worked only on the host itself.

**The endpoint has no authentication of its own.** `docker-compose.yml` defaults `DISABLE_AUTH=true`, and `requireAuth` then lets every request through as a built-in admin. The full tool set includes `start_channel`, `stop_channel`, `delete_channel`, `save_channel_graph`, `ingest_media` and the OBS stream and record controls.

## Decision

Route `/mcp` through the one front door, like every other path ([ADR 0003](0003-path-based-routing-behind-one-tailnet-name.md)):

```
client --HTTPS--> tailscale serve :443 --HTTP--> NPM 127.0.0.1:8880 --location /mcp--> engine:8888/mcp
```

1. **One extra NPM location**, `/mcp`, forwarding to `engine:8888` with the path unchanged (the engine already serves `/mcp`, so there is no prefix to strip).
2. **Access is "a registered tailnet device".** Anything on the tailnet that tailscale lets reach this host's HTTPS name may call `/mcp`. There is no per-user allowlist at the edge: the platform's security boundary is the tailnet (and its ACLs), and `/mcp` is inside it like every other path. Tighten who may reach a host with tailnet ACLs, not with application rules.
3. **The identity headers and the proxy secret are not forwarded** to the engine (`strip-identity.conf`), the same rule as every non-TMD location. The engine never learns who called.
4. **The engine joins the `edge` Docker network** (`docker-compose.edge.yml`) so NPM can reach it. Its host port stays `127.0.0.1:8888`.
5. **Streaming settings:** `proxy_buffering off` and `proxy_read_timeout 300s`. NPM already sets `proxy_http_version 1.1` for the whole server; the engine excludes `/mcp` from compression.
6. **Clients use the HTTPS name with the path:** `https://<host>.mastodon-adder.ts.net/mcp`. No token in the client config.

## Alternatives considered

| Option | Why not |
|---|---|
| Reopen `8888` on the tailnet name | The exposure F exists to close: all of the engine's control API on a raw port. |
| `tailscale serve --set-path /mcp ...` (no NPM) | Splits routing between two systems and contradicts ADR 0003. Same access outcome. |
| An allowlist of Tailscale logins at the edge | Drafted, then dropped: the platform already treats the tailnet as the boundary, and a per-route list would be the only place that did not. Revisit if shared-in peers need to be kept off `/mcp` but on the rest. |
| `DISABLE_AUTH=false` with `SERVICE_TOKENS` | Changes the whole engine API (the web UI and every consumer would need logins or tokens), not just `/mcp`. Worth doing later as defence in depth. |
| Proxy `/mcp` through TMD (identity and role check, audit trail) | The right long-term home. Needs a TMD change and release first, and SSE passthrough. The client URL would not change, so moving later costs nothing. |

## Consequences

- One path on every instance, checked the same way everywhere (below).
- turbo-1's engine port can be closed (TRU-16) as soon as this route exists there.
- Every caller is the same built-in admin to the engine, and `/mcp` can start, stop and delete channels. There is no per-person audit trail until the TMD option lands. A shared-in tailnet peer that can reach the host can use it; ACLs are the control.
- Anything that can reach `127.0.0.1:8880` on the host skips tailscale entirely, as it can for every other path ([ADR 0004](0004-identity-is-trusted-only-with-the-proxy-secret.md)).

## Checks (punch list, section F)

| Check | Proof |
|---|---|
| `/mcp` answers through the front door | from a tailnet device: POST `initialize` to `https://<host>.mastodon-adder.ts.net/mcp` with `accept: application/json, text/event-stream` → `serverInfo.name` = `mediamesh` |
| Other paths unaffected | `/` and `/tv/` still 200; `/api/session` still resolves the caller |
| Engine port still loopback | `docker port <engine> 8888` → `127.0.0.1:8888`; connecting on the tailnet IP:8888 is refused |
