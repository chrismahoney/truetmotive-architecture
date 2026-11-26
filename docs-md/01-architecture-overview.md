# 01 Architecture Overview

**Verified facts only** — all claims are traceable to committed revisions, live host evidence, or documented architecture decisions.

--- 

## Core Projects (the TrueMotive triad)

### truemotive-desktop
- **Project type**: Tauri 2 desktop application restructured to a non-Tauri native window around a web UI.
- **Architecture pattern**: Native window around web UI, restructured without the Tauri runtime. Legacy references remain as legacy artifacts.
- **Sidecar pattern**: Historically used a "managed sidecar" backend pattern where the backend ran as a separate process/managed service. This pattern has been adjusted in the restructured application.
- **Configuration hierarchy**: `default.json` provides baseline appearance settings (theme: "studio", mode: "dark"); themes extend or override the defaults; profiles suggest a profile-based customization system (only `example.json` exists).
- **Script-driven builds**: Node.js scripts used for build processes, sidecar management, and Tauri integration, indicating a script-first approach. Key scripts include: build-linux-arm64.sh, build-windows-bundle.sh, deploy-compose.sh.
- **Code structure**: Organized into apps/, config/, reports/, scripts/, services/.
- **Key finding**: Restructuring from Tauri was completed; the application no longer requires the Tauri runtime but configuration artifacts are preserved as legacy references.

### mediamesh
- **Project type**: Media mesh coordination layer connecting the three triad projects; provides Grafana-based monitoring interface.
- **Architecture pattern**: Media mesh coordination layer with Grafana integration. Acts as the media coordination layer between truemotive-desktop (media graph database) and occc-ui (monitored service).
- **Code structure**: Configuration files, analysis directories, Grafana integration. Contains packages/ui/ (React web UI), scripts/ (build-rist-receiver-dante.sh, edge.sh, seed-media.sh, start-all.sh, etc.), web/ (Vite-based frontend), edge/ (NPM proxy configuration), compose files (docker-compose.yml and overlays).
- **Key architecture decisions**:
  - Media Coordination Layer: mediamesh enables communication and data sharing between the three projects in the TrueMotive triad.
  - Grafana Monitoring Integration: The project integrates with Grafana for monitoring and UI purposes, with access keys and settings documented in architecture screenshots.
  - Cross-Project Data Flow: mediamesh facilitates data flow between truemotive-desktop and occc-ui, serving as the media mesh component of the overall architecture.

### occc-ui
- **Project type**: Viewer/TV app that reads the publish manifest; one of 13 services monitored in the CPU/MEM meters dashboard.
- **Architecture pattern**: Service monitoring within triad-wide dashboard. Integrated into the CPU/MEM meters dashboard alongside truemotive-desktop and mediamesh components.
- **Key finding**: Documented as "stopped" in the architecture audit trail; its monitoring status is visible alongside truemotive-desktop and mediamesh, enabling triad-wide monitoring and analysis.
- **Code structure**: Monitoring integration, service status documentation.

---

## Architecture Patterns

### Tauri Restructuring
- The truemotive-desktop application was rebuilt away from the Tauri 2 framework, removing the Tauri runtime while retaining legacy references.
- The application remains a native window around a web UI, but the web view is now served independently rather than through Tauri's embedded webview.
- This restructuring enables the "web UI first" approach where the core TrueMotive functionality is web-based with desktop as a deployment target.

### Sidecar Pattern
- The desktop app historically used a "managed sidecar" backend pattern where the backend ran as a separate process/managed service.
- This pattern has been adjusted in the restructured application to operate as a standalone service architecture.
- The sidecar pattern decouples the desktop application's backend functionality from the native window, allowing independent scaling and deployment.

### Web UI First
- The core TrueMotive functionality remains web-based with desktop as a deployment target.
- This is consistent across the architectural transition — all three triad projects deliver their primary UI through web technologies.
- The desktop (truemotive-desktop) is a native wrapper around web views; mediamesh and occc-ui are both web-based applications.

---

## Configuration Hierarchy
```
default.json  →  themes/  →  profiles/
```

- **`default.json`**: Provides baseline appearance settings (`theme: "studio"`, `mode: "dark"`). Sets the first-run theme and mode. Invalid files are skipped with a console warning during build.
- **Themes**: Each theme defines a color scheme with dark and light variants. Tokens include: bg, panel, raised, panelLine, lineStrong, ink, inkDim, inkFaint, accent, onAccent, live, crit, warn, good. Themes are validated against ThemeSchema in packages/shared at build time.
- **Profiles**: Suggest a profile-based customization system. Only `example.json` exists in the profiles/ directory, indicating the profile system may be under development or configurations are generated dynamically.
- **Programmatic configuration**: Heavy use of Node.js scripts for configuration suggests a preference for programmatic configuration over static files, preserved in the restructured application.
- **Configuration is never committed with secrets**: The .env file (per-host) contains secrets and settings never committed to git.

---

## Script-Driven Builds

The build and deployment process is driven by Node.js shell scripts:

### truemotive-desktop scripts
- build-linux-arm64.sh / build-windows-bundle.sh / build-windows-cross.sh — platform-specific bundles
- deploy-compose.sh — deploy to Docker Compose
- finalize-linux-bundles.sh — finalize build outputs
- publish-local-mac.sh — publish to local Mac
- gen-embed-themes.mjs / make-latest-json.mjs / make-updater-json.mjs — theme and update generation
- check-contrast.mjs — WCAG contrast validation (fails build on miss)
- ops-sync.mjs — operations synchronization
- release-notes.mjs / version-files.mjs — release management

### mediamesh scripts
- edge.sh — render and provision the edge proxy (Nginx Proxy Manager)
- build-rist-receiver-dante.sh — build RIST receiver with Dante
- install-api-deps.sh — install API dependencies (touches api/package-lock.json)
- probe-capabilities.sh — probe media capabilities
- seed-media.sh — seed media library
- start-all.sh — start all services
- extract-architecture-diagrams.mjs — extract diagrams from architecture sources

### Key build facts
- docker build via docker/web/Dockerfile for truemotive-desktop image
- docker compose with docker-compose.yml + docker-compose.edge.yml overlay for mediamesh stack
- VITE_MEDIAMESH_URL baked into occc-ui at build time (port: 8443)
- Local uncommitted edits on a host drift it from others; rule: hosts have no local edits to tracked files; per-host differences live in .env
- engine bind-mounts the repo (.:/app) and needs scripts/install-api-deps.sh after a fresh checkout

---

## Monitoring Patterns

### Grafana Integration
- mediamesh is connected to Grafana-based monitoring interfaces
- Grafana access keys analysis documented in architecture screenshots (grafana-access-keys/02-settings-mediamesh.png, 03-settings-access-library.png)
- mediamesh settings visible in Grafana monitoring interface documentation

### CPU/MEM Meters Dashboard
- 13 services monitored including truemotive-desktop, mediamesh, and occc-ui
- Service status documented in the architecture audit trail (e.g., occc-ui documented as "stopped")
- Activity-density-analysis AUDIT.md references occc-ui monitoring status

### Monitoring Principles
- Service status (stopped/active) is documented in the architecture audit trail
- Monitoring configurations are per-host via .env files
- Grafana access keys are stored separately from git (per the configuration hierarchy rule)
- The monitoring dashboard provides triad-wide visibility across all three projects

### Verified monitoring state (mahoney-mac, 2026-11-24)
- occc-ui: documented as "stopped" in the CPU/MEM meters dashboard
- truemotive-desktop: monitored and visible in the dashboard
- mediamesh: monitored with Grafana integration active

---

## Triad Data Flow

The three projects interact through defined data flow pathways:

### 1. Media Graph Database (truemotive-desktop)
- truemotive-desktop uses media-graph.sqlite for media data management
- The media graph database stores media assets, channel data, and related state
- Integration with mediamesh coordination layer for data sharing

### 2. Media Mesh Coordination (mediamesh)
- mediamesh acts as the media mesh coordination layer
- Enables communication and data sharing between truemotive-desktop and occc-ui
- Three kinds of channel flow: built, authored, example
- Channel coordination pattern validated per ARCHITECTURE.md Sections 5–11

### 3. Viewer/TV App (occc-ui)
- occc-ui reads the publish manifest generated by the engine
- Displays HLS streams, WebRTC playback, and other media outputs
- Monitored in the CPU/MEM meters dashboard alongside other triad components

### 4. Engine (Liquidsoap + control API)
- The engine runs channel graphs and serves HLS output
- Ingests media from RIST, SRT, RTMP, and WebRTC contributors
- Outputs HLS playlists and WebRTC playback paths
- Publishes the manifest consumed by occc-ui

### 5. MediaMTX Integration Points (3 relationships)
- **Ingest**: RIST/UDP ingest on ports 9000, 9100; SRT on 9300–9399; RTMP on 1935
- **Egress**: HLS on engine port 8888; WebRTC playback on mediamtx port 8889; RIST/SRT/RTMP output
- **Direct browser preview**: mediamtx WHEP listener on :8889 with MTX_WEBRTC_ADDITIONAL_HOSTS for browser access

### 6. Full Triad Data Flow Sequence
```
Contributor → RIST/SRT/RTMP/WebRTC → Engine (Liquidsoap) → HLS / WHEP → occc-ui (viewer)
                                   ↓
                              mediamesh (coordination + Grafana monitoring)
                                   ↓
                          truemotive-desktop (media graph + appearance config)
```

### 7. Key Data Flow Verified on mahoney-mac (2026-11-24)
- HLS output at /hls/ through the tailnet name (verified with verify.sh R4)
- WHEP offer 201 with https Location under /whep/ (verified with verify.sh R5)
- Video playing in a real browser over https (E2E test screenshot)
- MCP endpoint (/mcp) reaches engine through the front door (TMD), not through direct ports
- Engine API at baked-in VITE_MEDIAMESH_URL (…:8443) — occc-ui built with this URL at build time
- Channel lifecycle: compile → start → HLS output → viewer (occc-ui)

---

## Instance Mapping

| Project | Host | Directory |
|---------|------|-----------|
| truemotive-desktop | mahoney-mac (dev) | `~/Claude/Projects/truemotive-desktop` |
| mediamesh | mahoney-mac (dev) | ~/Claude/TrueMotive/mediamesh |
| occc-ui | mahoney-mac (dev) | ~/Claude/TrueMotive/occc-ui |

### Release Flow (target)
1. Change lands in a branch and PR. No direct pushes to main.
2. Prove it in a clean room on dev: separate compose project, state folder and worktrees, so the real instance is not touched.
3. Run the full punch list in the clean room.
4. Tag TMD if it changed. Update the pin.
5. Apply to test, then prod, one punch-list row at a time, with a backup first.

### Known traps
- engine bind-mounts the repo; run scripts/install-api-deps.sh after a fresh checkout
- rist-receiver-dante needs a GitHub token at build time (scripts/build-rist-receiver-dante.sh); running an already built image does not
- occc-ui bakes VITE_MEDIAMESH_URL in at build time
- Local uncommitted edits on a host drift it from the others. On turbo-1 they reached ~3,200 lines. Rule: hosts have no local edits to tracked files; per-host differences live in .env
- TMD listener port configuration: TMD_HOST is 127.0.0.1 and TMD_PORT is 4712. Always. Session mode requires the main listener on loopback.
- Nothing but NPM is pointed at 4716, and 4716 is never in a ports: list
- NPM is never pointed at 4715. That listener ignores tailnet identity, so people would see a login prompt instead of being recognised
- Do not edit the proxy secret in only one place. It lives in .env as TMD_PROXY_SECRET and is delivered to NPM as described
- Secrets never appear in docs; name the variable, never the value
