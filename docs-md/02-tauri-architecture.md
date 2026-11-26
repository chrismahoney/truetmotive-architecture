# 02 Tauri Architecture

**Verified facts only** — all claims are traceable to committed revisions, live host evidence, or documented architecture decisions.

---
## Tauri Restructuring

- The `truemotive-desktop` application was rebuilt away from the Tauri 2 framework, removing the Tauri runtime while retaining legacy references as artifacts.
- The application remains a native window around a web UI, but the web view is now served independently rather than through Tauri's embedded webview.
- This restructuring enables the **"web UI first"** approach where the core TrueMotive functionality is web-based with desktop as a deployment target.
- Configuration artifacts from the Tauri era are preserved as legacy references; the application no longer requires the Tauri runtime to operate.
- Key scripts involved in the restructuring and build process: `build-linux-arm64.sh`, `build-windows-bundle.sh`, `build-windows-cross.sh`, `deploy-compose.sh`, `finalize-linux-bundles.sh`, `publish-local-mac.sh`.

---
## Sidecar Pattern

- The desktop app historically used a **"managed sidecar"** backend pattern where the backend ran as a separate process/managed service.
- This pattern has been adjusted in the restructured application to operate as a **standalone service architecture**.
- The sidecar pattern decouples the desktop application's backend functionality from the native window, allowing independent scaling and deployment.
- The sidecar pattern is part of the broader configuration hierarchy that includes `default.json`, themes, and profiles.
- Programmatic configuration via Node.js scripts is heavily used, suggesting a preference for programmatic configuration over static files, preserved in the restructured application.

---
## Web UI First

- The core TrueMotive functionality remains **web-based with desktop as a deployment target**.
- This is consistent across the architectural transition — all three triad projects deliver their primary UI through web technologies.
- The desktop (`truemotive-desktop`) is a native wrapper around web views; `mediamesh` and `occc-ui` are both web-based applications.
- The web UI first approach enables independent iteration on the user interface without affecting the native desktop container requirements.
- Key web-facing components: Vite-based frontend in `mediamesh`, React-based UI, and the baked-in `VITE_MEDIAMESH_URL` at build time (port: 8443).

---
## Cross-Project Integration

- The three projects (`truemotive-desktop`, `mediamesh`, `occc-ui`) interact through defined data flow pathways as part of the TrueMotive triad.
- **mediamesh** acts as the media mesh coordination layer, enabling communication and data sharing between `truemotive-desktop` and `occc-ui`.
- `VITE_MEDIAMESH_URL` is baked into `occc-ui` at build time, pointing to port 8443 for the mediamesh backend.
- **Data flow sequence**: Contributor → RIST/SRT/RTMP/WebRTC → Engine (Liquidsoap) → HLS / WHEP → `occc-ui` (viewer), with `mediamesh` facilitating coordination + Grafana monitoring, and `truemotive-desktop` serving as the media graph + appearance config.
- Channel lifecycle: compile → start → HLS output → viewer (`occc-ui`).
- Media graph database (`media-graph.sqlite`) in `truemotive-desktop` stores media assets, channel data, and related state, integrated with the `mediamesh` coordination layer.
- Monitoring integration: `mediamesh` connects to Grafana-based monitoring interfaces with documented access keys.
- 13 services are monitored in the CPU/MEM meters dashboard, including `truemotive-desktop`, `mediamesh`, and `occc-ui`.
- Instance mapping on mahoney-mac:
  - `truemotive-desktop`: `~/Claude/Projects/truemotive-desktop`
  - `mediamesh`: `~/Claude/TrueMotive/mediamesh`
  - `occc-ui`: `~/Claude/TrueMotive/occc-ui` (path to be confirmed)

---
## Configuration Hierarchy

```text
default.json  →  themes/  →  profiles/
```

- **`default.json`**: Provides baseline appearance settings (`theme: "studio"`, `mode: "dark"`). Sets the first-run theme and mode. Invalid files are skipped with a console warning during build.
- **Themes**: Each theme defines a color scheme with dark and light variants. Tokens include: bg, panel, raised, panelLine, lineStrong, ink, inkDim, inkFaint, accent, onAccent, live, crit, warn, good. Themes are validated against ThemeSchema in packages/shared at build time.
- **Profiles**: Suggest a profile-based customization system. Only `example.json` exists in the profiles/ directory, indicating the profile system may be under development or configurations are generated dynamically.
- **Configuration is never committed with secrets**: The `.env` file (per-host) contains secrets and settings never committed to git.