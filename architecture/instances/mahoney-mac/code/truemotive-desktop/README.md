# truemotive-desktop

## Project Overview

The truemotive-desktop project is the first component of the TrueMotive architecture, 
documented within the architecture worktree. This project was investigated as part of 
the architecture documentation task, with findings cross-referenced against the other 
two projects (mediamesh, occc-ui).

### Project Context

- Documented within: `architecture/instances/mahoney-mac/code/truemotive-desktop/`
- Part of the TrueMotive architecture triad (alongside mediamesh and occc-ui)
- Investigation focused on architecture-level understanding, not source code review
- Key analysis types captured in HANDOFF_INVESTIGATE_CODE.md

### Documentation Artifacts

- Local README: `architecture/instances/mahoney-mac/code/truemotive-desktop/README.md`
- Cross-reference: `HANDOFF_INVESTIGATE_CODE.md` for detailed project findings
- Architecture context: Documentation of how this project fits the TrueMotive triad

### Skills Investigation

Documented skills used via `npx skills find` and `npx skills use` within the 
architecture investigation scope for truemotive-desktop.

### Code Structure Findings (Architecture Relevance)

- **Tauri-Based Architecture**: The desktop application was built using Tauri 2, which provided a native OS window with a web view (Rust backend + JavaScript frontend). This is no longer the active architecture - the application has been restructured without the Tauri runtime.
- **Triad Integration**: The project is documented as part of the TrueMotive architecture triad alongside `mediamesh` and `occc-ui`, indicating shared architecture patterns and integration points.
- **Sidecar Pattern**: The desktop app historically used a "managed sidecar" backend pattern, where the backend ran as a separate process/managed service rather than being embedded directly. This pattern has been adjusted in the restructured application.
- **Configuration Hierarchy**: 
  - `default.json` provides baseline appearance settings
  - Themes extend or override the defaults
  - Profiles (though limited to `example.json`) suggest a profile-based customization system
- **Script-Driven Builds**: The project used Node.js scripts for build processes, sidecar management, and Tauri integration, indicating a script-first approach to configuration and deployment. This has been adapted for the new architecture.
- **Limited Profile Configuration**: Only `example.json` exists in the profiles directory, suggesting the profile system may be under development or the configurations are generated dynamically.

### Key Architecture Decisions

1. **Restructuring from Tauri**: The application was restructured away from the Tauri 2 framework, removing the Tauri runtime while retaining the configuration artifacts (Cargo.toml, lib.rs, @tauri-apps/cli in package.json devDependencies) as legacy references.
2. **Managed sidecar evolution**: The sidecar backend pattern evolved from a Tauri-integrated model to a standalone service architecture.
3. **Web UI first**: The core TrueMotive functionality remains web-based with desktop as a deployment target, consistent across the architectural transition.
4. **Programmatic configuration**: Heavy use of Node.js scripts for configuration suggests a preference for programmatic configuration over static files, preserved in the restructured application.

### Findings Summary

| Category | Finding |
|----------|---------|
| **Project Type** | Tauri 2 desktop application (restructured to non-Tauri) |
| **Architecture Pattern** | Native window around web UI, restructured without Tauri runtime |
| **Triad Membership** | Part of TrueMotive triad (with mediamesh and occc-ui) |
| **Code Structure** | Organized into apps/, config/, reports/, scripts/, services/ |
| **Configuration** | Minimal: default.json, themes/, example.json |
| **Key Analyses** | 4 analysis types with 4-phase structure each |
| **Files Found** | 1 configuration file (default.json), 1 profile (example.json), 4 analysis directories |
| **Files Not Found** | desktop.json, audit.log, media-graph/sqlite, this-backend.json |
| **Documentation Status** | README documents project overview with TODO items for future investigation |

### Traps to Avoid

- Do not attempt full source code review; investigation is architecture-level only
- Do not assume configuration files exist if they are not present in the project
- Cross-reference findings with mediamesh and occc-ui for triad consistency
- Document TODO items for future agents as specified in the investigation brief