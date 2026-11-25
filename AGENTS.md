# AGENTS.md

## Agent Turn Guidelines

Each agent turn should:
1. **Investigate available skills** - Before starting work, check what skills are available via `npx skills find` and `npx skills use` commands to determine the best tools for the task at hand.
2. **Select appropriate skills** - Choose skills that will help with the Task Objective, or find new ones if needed.
3. **Document findings** - Capture information about the projects being worked on, including architecture, instances, and relevant code reviews.
4. **Keep TrueMotive instance info in architecture/** - We keep all info related to TrueMotive instances in our architecture/ root directory.

## Task Objective

Visit local projects to collect information for architecture/instances/mahoney-mac architecture documentation.

### Projects to investigate:
1. truemotive-desktop (in ~/Claude/Projects/)
2. mediamesh (in ~/Claude/TrueMotive/)
3. occc-ui (in ~/Claude/TrueMotive/)

### Expected directory structure:

```
architecture/
- instances/
  - mahoney-mac/
    - code/
      - truemotive-desktop/
      - mediamesh/
      - occc-ui/
- HANDOFF_INVESTIGATE_CODE.md
```

### HANDOFF_INVESTIGATE_CODE.md

Information for future agents to extrapolate and capture more data beyond this task. 
Include the task of creating the initial README.md at root with TODO placeholders 
wherever the user asks for them.

## Agent usage metrics

When you dispatch subagents, record every run's usage from its completion notice (`subagent_tokens`, `tool_uses`, `duration_ms`) in the plan's ledger: one row each for task, role, tokens, tool calls and seconds. Fix rounds and re-reviews get their own rows.
- **When a task completes**, post its rows as a comment on its Linear issue. Linear has no token field, so a comment is the record.
- **In the PR description**, add an "Agent usage" table with a row per task, a total, and the number of fix rounds.
- Label the figures approximate: a resumed agent re-reads its context, so rows overlap and must not be summed as a bill. Agents cannot see the main session's own usage; take that from the session cost view.