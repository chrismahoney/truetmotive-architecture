# Section 1: truemotive-desktop Investigation

## 1.1 Project Overview

The truemotive-desktop project is the first component of the TrueMotive architecture, documented within the architecture worktree. This project was investigated as part of the architecture documentation task, with findings cross-referenced against the other two projects (mediamesh and occc-ui).

### Project Context

- **Documented within**: `architecture/instances/mahoney-mac/code/truemotive-desktop/`
- **Part of the TrueMotive architecture triad** (alongside mediamesh and occc-ui)
- **Investigation focused on architecture-level understanding**, not source code review
- **Key analysis types captured in HANDOFF_INVESTIGATE_CODE.md**

### Project Location

- **Code directory**: `~/Claude/Projects/truemotive-desktop/`
- **Architecture documentation**: `/Users/chris/.cline/worktrees/3d9e7/TrueMotiveArchitecture/architecture/instances/mahoney-mac/code/truemotive-desktop/`

### Package Configuration

- **Name**: `@tmd/desktop`
- **Version**: `2.7.1`
- **Private**: true
- **Description**: "Tauri 2 shell: a native window around the web UI, with the backend as a managed sidecar."
- **Scripts** (note: Tauri build workflow no longer active):
  - `sidecar`: `pnpm --filter @tmd/web build && node ../../scripts/build-sidecar.mjs`
  - `dev`: `node ../../scripts/check-node.mjs && pnpm sidecar && tauri dev`
  - `build`: `node ../../scripts/check-node.mjs`
  - `build:signed`: `node ../../scripts/check-node.mjs && pnpm sidecar && tauri build --config src-tauri/tauri.updater.conf.json`
  - `test`: `command -v cargo >/dev/null && cargo test --manifest-path core/Cargo.toml || echo 'cargo not found: skipping desktop core tests'`
  - `typecheck`: `echo 'no TypeScript in @tmd/desktop'`
  - `tauri`: `tauri`
  - **Note**: Tauri framework configuration persists (`@tauri-apps/cli: ^2.0.0` in devDependencies, Cargo.toml, lib.rs) but the Tauri-based build workflow is no longer active; the application has been restructured without the Tauri runtimetest

## 1.2 Code Structure

### Project Layout (`~/Claude/Projects/truemotive-desktop/`)

```
truemotive-desktop/
├── apps/                                    # Application directories
│   ├── builder-v3/                          # Builder application v3
│   │   ├── dist/
│   │   ├── dist-build/
│   │   └── node_modules/
│   └── desktop/                             # Main desktop application
│       ├── core/                            # Formerly Tauri core directory (restructured)
│       ├── node_modules/                    
│       ├── package.json                     # Desktop package config
│       ├── scripts/                         # Build scripts (Tauri build no longer active)
│       └── src/                             # Source directory (web UI focus)
│           └── sidecar/                     # Sidecar functionality (adjusted role)
├── config/                                  # Configuration directory
│   └── appearance/                          # Appearance configuration
│       ├── default.json                     # Default appearance settings
│       └── themes/                          # Theme definitions
├── docker/                                  # Docker configurations
├── docs/                                    # Documentation
├── event-packs/                             # Event pack collections
├── packages/                                # Shared packages
├── plans/                                   # Project plans
├── profiles/                                # Profile configurations
│   └── example.json                         # Example profile
├── reports/                                 # Investigation reports
│   └── claude/                              # Claude-generated reports
│       ├── media-library-analysis/          # Media library analysis
│       ├── media-library-wip/               # Work-in-progress media library
│       ├── rist-preview-node-analysis/      # RIST preview node analysis
│       └── ristgo-analysis/                 # RIST go analysis
├── scripts/                                 # Project scripts
├── services/                                # Service configurations
└── website/                                 # Web interface
├── package.json                             # Root package configuration
```

## 1.3 Configuration Files

### Found Configuration Files

- **`config/appearance/default.json`**: Default appearance settings (42 bytes, Oct 12 17:42)
- **`config/appearance/themes/`**: Theme directory containing multiple theme definitions
- **`profiles/example.json`**: Example profile configuration (276 bytes, Oct 12 16:54)

### Configuration Files Not Found

The following configuration files referenced in the task investigation were **not found** in the truemotive-desktop project:

- **`desktop.json`**: Not found in project search
- **`audit.log`**: Not found in project search
- **`media-graph/sqlite`**: Not found in project search
- **`profiles/this-backend.json`**: Not found in project search (profiles directory only contains `example.json`)

### Configuration Summary

The project has a minimal configuration setup with:
- `default.json` for appearance defaults
- `themes/` directory for theme management
- `example.json` as the only profile configuration

The absence of `desktop.json`, `audit.log`, `media-graph/sqlite`, and `profiles/this-backend.json` suggests these files either:
1. Are generated during build/time of investigation
2. Exist in a different branch or version
3. Are expected to be created as part of the investigation handoff process

## 1.4 Key Analyses

### Analysis Directories Found

The following analysis directories exist in `~/Claude/Projects/truemotive-desktop/reports/claude/`:

1. **`media-library-analysis/`**: Analysis of the media library
   - Subdirectories: `00-planning`, `01-current-state`, `02-design`, `03-recommendation`, `site`
   - Contains: `README.md` and `site/` directory

2. **`media-library-wip/`**: Work-in-progress media library analysis
   - Subdirectories: `00-planning`, `01-current-state`, `02-design`, `03-recommendation`

3. **`rist-preview-node-analysis/`**: RIST preview node analysis
   - Subdirectories: `00-planning`, `01-current-state`, `02-design`, `03-recommendation`
   - Contains: `README.md`

4. **`ristgo-analysis/`**: RIST go analysis
   - Subdirectories: `00-planning`, `01-current-state`, `02-design`, `03-recommendation`
   - Contains: `README.md`

### Analysis Summary

Each analysis directory follows a standardized structure with four phases:
- `00-planning`: Initial planning and scope definition
- `01-current-state`: Assessment of the current state
- `02-design`: Design recommendations and implementations
- `03-recommendation`: Final recommendations

The analysis types cover:
- Media library structure and analysis
- RIST (RTP-based Secure Internet Streaming) preview node configuration
- RIST go implementation analysis

## 1.5 Code Review Findings (Architecture Relevance)

### Investigation Scope

The code review was constrained to **architecture relevance only**, focusing on:
- Project structure and organization
- Configuration management
- Integration patterns with the TrueMotive triad (mediamesh, occc-ui)
- Architecture-level decisions and patterns

### Code Structure Findings

1. **Tauri-Based Architecture**: The desktop application was built using Tauri 2, which provided a native OS window with a web view (Rust backend + JavaScript frontend). This is no longer the active architecture - the application has been restructured without the Tauri runtime.

2. **Triad Integration**: The project is documented as part of the TrueMotive architecture triad alongside `mediamesh` and `occc-ui`, indicating shared architecture patterns and integration points.

3. **Sidecar Pattern**: The desktop app historically used a "managed sidecar" backend pattern, where the backend ran as a separate process/managed service rather than being embedded directly. This pattern has been adjusted in the restructured application.

4. **Configuration Hierarchy**: 
   - `default.json` provides baseline appearance settings
   - Themes extend or override the defaults
   - Profiles (though limited to `example.json`) suggest a profile-based customization system

5. **Script-Driven Builds**: The project used Node.js scripts for build processes, sidecar management, and Tauri integration, indicating a script-first approach to configuration and deployment. This has been adapted for the new architecture.

6. **Limited Profile Configuration**: Only `example.json` exists in the profiles directory, suggesting the profile system may be under development or the configurations are generated dynamically.

### Architecture Constraints and Observations

- **Architecture-focused documentation**: The investigation explicitly states it's "focused on architecture-level understanding, not source code review"
- **Cross-referencing**: Findings are cross-referenced against the other two projects (mediamesh, occc-ui) to ensure consistency across the TrueMotive triad
- **TODO items**: The README documents several TODO items for future investigation, including skills investigation and code structure documentation

### Key Architecture Decisions

1. **Restructuring from Tauri**: The application was restructured away from the Tauri 2 framework, removing the Tauri runtime while retaining the configuration artifacts (Cargo.toml, lib.rs, @tauri-apps/cli in package.json devDependencies) as legacy references.

2. **Managed sidecar evolution**: The sidecar backend pattern evolved from a Tauri-integrated model to a standalone service architecture.

3. **Web UI first**: The core TrueMotive functionality remains web-based with desktop as a deployment target, consistent across the architectural transition.

4. **Programmatic configuration**: Heavy use of Node.js scripts for configuration suggests a preference for programmatic configuration over static files, preserved in the restructured application.

## 1.6 Findings Summary

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
