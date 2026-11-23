# Investigation Report: truemotive-desktop Architecture

**Investigation Date:** 2026-11-23
**Investigator:** Cline AI Coding Agent
**Scope:** Architecture code review of truemotive-desktop project

---

---

## 1. Brief

This investigation visited local projects to collect information for architecture/instances/mahoney-mac architecture documentation. The truemotive-desktop project was investigated as the first component of the TrueMotive architecture triad, alongside mediamesh and occc-ui. The investigation focused on architecture-level understanding constrained to configuration files, data stores, and inter-project relationships rather than application source code review.

---

## 2. What We Looked At

### Projects Investigated:

1. **truemotive-desktop** - Location: `/Users/chris/.config/truemotive-desktop/`
   - Configuration files: desktop.json, profiles/this-backend.json, service.env, audit.log
   - Data store: media-graph/sqlite (media-graph.sqlite)
   - Analyses referenced: activity-density-analysis, built-in-docs, grafana-access-keys, media-library-analysis, rist-preview-node-analysis, ristgo-analysis

2. **mediamesh** - Referenced in truemotive-desktop config and grafana settings
   - Code directory: architecture/instances/mahoney-mac/code/mediamesh/

3. **occc-ui** - Monitored service in architecture dashboard
   - Code directory: architecture/instances/mahoney-mac/code/occc-ui/

### Files Examined:
- `architecture/instances/mahoney-mac/code/truemotive-desktop/README.md` - Investigation task documentation
- `/Users/chris/.config/truemotive-desktop/desktop.json` - Tailnet configuration
- `/Users/chris/.config/truemotive-desktop/profiles/this-backend.json` - Local Mac Tailnet profile
- `/Users/chris/.config/truemotive-desktop/audit.log` - 329+ log entries of real-time operations
- `/Users/chris/.config/truemotive-desktop/media-graph/media-graph.sqlite` - Media graph database (4.9 MB)
- `/Users/chris/.config/truemotive-desktop/service.env` - Environment configuration
- `HANDOFF_INVESTIGATE_CODE.md` - Cross-project handoff documentation

## 3. What We Found

### 3.1 Project Context
- truemotive-desktop is the **first component** of the TrueMotive architecture triad
- Documented within `architecture/instances/mahoney-mac/code/truemotive-desktop/`
- Part of the TrueMotive architecture alongside mediamesh and occc-ui
- Investigation focused on architecture-level understanding, not source code review

### 3.2 Configuration Architecture

#### `desktop.json`
```json
{
  "tailnet": {
    "enabled": true,
    "port": 8444
  }
}
```
- **Architecture relevance:** Tailnet networking enabled on port 8444 for inter-process communication
- Part of the TrueMotive decentralized infrastructure

#### `profiles/this-backend.json`
```json
{
  "name": "Local Mac Tailnet",
  "dockerHost": "ssh://mahoney-mac.mastodon-adder.ts.net",
  "mediameshPath": "~/Claude/TrueMotive/mediamesh",
  "engineUrl": "https://mahoney-mac.mastodon-adder.ts.net:8443",
  "tailnetHost": "mahoney-mac.mastodon-adder.ts.net",
  "composeFiles": ["docker-compose.yml"],
  "allowConfigWrites": false
}
```
- **Architecture relevance:**
  - Points to local Mac tailnet infrastructure (`mahoney-mac.mastodon-adder.ts.net`)
  - References mediamesh path for media mesh integration
  - Engine URL for backend service communication
  - Docker host for containerized services
  - `allowConfigWrites: false` indicates read-only configuration in production

### 3.3 Data Architecture

#### `media-graph.sqlite`
- SQLite database (4.9 MB with -shm and -wal files)
- **Architecture relevance:** Media graph database for truemotive-desktop
- Central data store for media data management
- Confirmed in HANDOFF_INVESTIGATE_CODE.md as the media data management layer

#### `audit.log` (329+ entries)
Key architecture-relevant operations:
- **Room management:** room.join, room.tile, room.guest_join operations
- **Media import:** media.import.start/failed (blocked URLs, size limits)
- **Receiver operations:** receiver.create, receiver.key, receiver.update
- **Mediamesh integration:** mediamesh.assistant, mediamesh.obs.scene, mediamesh.user.update, mediamesh.token.create, mediamesh.obs.save
- **Preview operations:** preview.start/stop (live standard, HTTP 404 errors, port conflicts)
- **Cleanup operations:** cleanup.data.hls, cleanup.data.tmp, cleanup.data.logs, cleanup.docker.dangling-images
- **Channel management:** channel.duplicate, cleanup.channels.never-run

### 3.4 Inter-Project Architecture

#### truemotive-desktop ↔ mediamesh
- mediamesh path referenced in `profiles/this-backend.json` (`~/Claude/TrueMotive/mediamesh`)
- Mediamesh assistant operations in audit.log (settings, obs.scene, user updates, token creation)
- Mediamesh appears connected to grafana-based monitoring interface
- Cross-references: grafana-access-keys screenshots (02-settings-mediamesh.png, 03-settings-access-library.png)

#### truemotive-desktop ↔ occc-ui
- occc-ui noted as "stopped" among 13 services monitored
- Observed in CPU/MEM meters dashboard (13 services total)
- Referenced in activity-density-analysis AUDIT.md

#### truemotive-desktop ↔ grafana
- grafana-access-keys analysis for monitoring and UI
- Settings screenshots referenced

### 3.5 Skills Investigation
- TODO: Document skills used via `npx skills find` and `npx skills use`
- Architecture investigation scope noted but not yet completed

### 4. Open Questions

1. [ ] Investigate code structure within architecture documentation scope
2. [ ] Document code review findings constrained to architecture relevance
3. [ ] Add skills investigation results relevant to the TrueMotive triad
4. [ ] Create detailed architecture diagrams showing project interactions
5. [ ] Document API interfaces and data flow between projects
6. [ ] Investigate actual source code repositories for each project

### 5. How This Was Done

- **Mode:** Deep (files and code could be read)
- **Tools Used:**
  - `read_files` - Reading configuration and log files
  - `run_commands` - Listing directory structures
  - `craft-anything__core_report_write` - Report generation
- **Constraints:** Architecture relevance only - focused on configuration, data flow, and inter-project relationships rather than application source code review

### 6. Architecture Diagram Summary

The TrueMotive architecture triad consists of:

```
truemotive-desktop  ──────▶ mediamesh
      │                   │
      │                   ▼
      │            media-graph.sqlite (SQLite)
      │                   │
      ▼                   ▼
   tailnet:8444       grafana monitoring
      │
      ▼
   occc-ui (monitored service, stopped)
```

**Data Flow:**
1. truemotive-desktop configures tailnet networking (port 8444)
2. Mediamesh integration via referenced paths and assistant operations
3. Media data stored in media-graph.sqlite
4. Monitoring via Grafana access keys and activity density analysis
5. occc-ui observed in CPU/MEM meters dashboard

**Configuration Flow:**
- `profiles/this-backend.json` → dockerHost, engineUrl, tailnetHost
- `desktop.json` → tailnet enabled/port
- audit.log → real-time operation logging
- service.env → environment variables
```
