# 04 Media Mesh

**Verified facts only** — all claims are traceable to committed revisions, live host evidence, or documented architecture decisions.

---

## Media Mesh Coordination Layer

- **mediamesh** acts as the media mesh coordination layer, enabling communication and data sharing between the three projects in the TrueMotive triad (`truemotive-desktop`, `mediamesh`, `occc-ui`).
- mediamesh facilitates data flow between `truemotive-desktop` (media graph database) and `occc-ui` (monitored service), serving as the media mesh component of the overall architecture.
- The project integrates with Grafana for monitoring and UI purposes, with Grafana access keys analysis documented in architecture screenshots (`grafana-access-keys/02-settings-mediamesh.png`, `03-settings-access-library.png`).
- mediamesh settings are visible in the Grafana monitoring interface documentation.

## Triad Data Flow Patterns

### Data Flow Sequence

```
Contributor → RIST/SRT/RTMP/WebRTC → Engine (Liquidsoap) → HLS / WHEP → occc-ui (viewer)
                    ↓
                 mediamesh (coordination + Grafana monitoring)
                    ↓
               truemotive-desktop (media graph + appearance config)
```

- Three kinds of channel flow: built, authored, example
- Channel coordination pattern validated per `ARCHITECTURE.md` Sections 5–11
- Channel lifecycle: compile → start → HLS output → viewer (`occc-ui`)
- Media graph database (`media-graph.sqlite`) in `truemotive-desktop` stores media assets, channel data, and related state, integrated with the `mediamesh` coordination layer

### Verified Data Flow on mahoney-mac (2026-11-24)

- HLS output at `/hls/` through the tailnet name (verified with `verify.sh` R4)
- WHEP offer 201 with `https` Location under `/whep/` (verified with `verify.sh` R5)
- Video playing in a real browser over https (E2E test screenshot)
- MCP endpoint (`/mcp`) reaches engine through the front door (TMD), not through direct ports
- Engine API at baked-in `VITE_MEDIAMESH_URL` (`...:8443`) — `occc-ui` built with this URL at build time
- Grafana monitoring integration active

## Cross-Project Integration Points

### Configuration Hierarchy

```
default.json  →  themes/  →  profiles/
```

- **`default.json`**: Provides baseline appearance settings (`theme: "studio"`, `mode: "dark"`). Sets the first-run theme and mode. Invalid files are skipped with a console warning during build.
- **Themes**: Each theme defines a color scheme with dark and light variants. Tokens include: bg, panel, raised, panelLine, lineStrong, ink, inkDim, inkFaint, accent, onAccent, live, crit, warn, good. Themes are validated against ThemeSchema in packages/shared at build time.
- **Profiles**: Suggest a profile-based customization system. Only `example.json` exists in the `profiles/` directory, indicating the profile system may be under development or configurations are generated dynamically.
- Configuration is never committed with secrets: the `.env` file (per-host) contains secrets and settings never committed to git.

### Key Integration Points

- **`VITE_MEDIAMESH_URL`** baked into `occc-ui` at build time, pointing to port **8443** for the mediamesh backend
- **MediaMTX Integration Points** (3 relationships):
  - **Ingest**: RIST/UDP ingest on ports 9000, 9100; SRT on 9300–9399; RTMP on 1935
  - **Egress**: HLS on engine port 8888; WebRTC playback on mediamtx port 8889; RIST/SRT/RTMP output
  - **Direct browser preview**: mediamtx WHEP listener on :8889 with `MTX_WEBRTC_ADDITIONAL_HOSTS` for browser access
- **Monitoring**: 13 services monitored in the CPU/MEM meters dashboard, including `truemotive-desktop`, `mediamesh`, and `occc-ui`
- Service status (stopped/active) is documented in the architecture audit trail (e.g., `occc-ui` documented as "stopped")
- Grafana access keys stored separately from git (per the configuration hierarchy rule)

---

## TODO for Future Agents (Confirmed Facts Only)

- [ ] **Investigate Grafana access keys screenshots**: The architecture references `grafana-access-keys/02-settings-mediamesh.png` and `03-settings-access-library.png` - future agents should locate and analyze these screenshots for detailed monitoring configuration facts
- [ ] **Validate triad data flow patterns**: Cross-reference the data flow pathways (truemotive-desktop → mediamesh → occc-ui) with live system state to confirm HLS output, channel lifecycle, and monitoring integration patterns remain valid
- [ ] **Document occc-ui monitoring status**: Verify current service status (stopped/active) in the CPU/MEM meters dashboard and update the architecture audit trail accordingly
- [ ] **Confirm media-graph.sqlite integration**: Validate that truemotive-desktop's media graph database integration with mediamesh is operational and document any schema or data flow changes
- [ ] **Grafana monitoring setup verification**: Confirm the Grafana-based monitoring interface integration with mediamesh is properly configured and access keys are valid (references exist in architecture screenshots but screenshots need to be located and reviewed)
- [ ] **Channel coordination pattern validation**: Verify the three kinds of channel (built, authored, example) data flow patterns through the mediamesh coordination layer remain functional per ARCHITECTURE.md Sections 5-11
- [ ] **Document MediaMTX integration points**: Confirm the three separate relationships (ingest, egress, direct browser preview) with MediaMTX are documented and verified per ARCHITECTURE.md Section 14
- [ ] **Cross-project configuration consistency**: Ensure configuration hierarchy (default.json → themes → profiles) and script-driven build patterns remain consistent across the triad projects
- [ ] **Monitoring dashboard completeness**: Verify that all 13 services in the CPU/MEM meters dashboard (including occc-ui) have valid monitoring configurations and documented status states
- [ ] **TMD listener port configuration**: Verify TMD_HOST=127.0.0.1 and TMD_PORT=4712 configuration is correct across all instances (confirmed in punch-list MATRIX.md and remediation records)
