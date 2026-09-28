# caveman (JuliusBrussee/caveman)

Respuestas comprimidas para ahorrar tokens, refactors seguros, reviews

Traer con `library/fetch-source.sh caveman`. Rutas relativas a `/tmp/skill-sources/caveman`.

| Nombre | Para que | Archivo |
|---|---|---|
| cavecrew | When to delegate to `cavecrew-investigator` (locate code), `cavecrew-builder` (1-2 file edit) or `cavecrew-reviewer` (diff review) instead of working inline... | `skills/cavecrew/SKILL.md` |
| caveman-commit | Write a Conventional Commits message compressed to intent only. Use for "write a commit", "commit message", /commit or /caveman-commit. | `skills/caveman-commit/SKILL.md` |
| caveman-compress | Compress a memory file such as CLAUDE.md or a todo list into caveman format to save input tokens, keeping a readable backup. Trigger: /caveman-compress. | `skills/caveman-compress/SKILL.md` |
| caveman-discover | Find and label every LLM workflow in the repository so Caveman Cloud groups spend by workflow instead of one bucket. Use for "discover workflows" or... | `skills/caveman-discover/SKILL.md` |
| caveman-evidence-review | Read-only review of Caveman Cloud evidence: cost, Cave Score, workflows, traces, latency, errors, routing, savings. Use when asked what Caveman found or... | `skills/caveman-evidence-review/SKILL.md` |
| caveman-explore | Read-only repository explorer for cold-start orientation, broad cross-file localization, or when a direct search failed. Skip it when the exact file or... | `skills/caveman-explore/SKILL.md` |
| caveman-help | Quick-reference card for caveman modes, skills and commands. Trigger: /caveman-help or "caveman help". | `skills/caveman-help/SKILL.md` |
| caveman-learn | Act on a Caveman learn report - review the ranked token sinks, apply cost-lowering fixes with per-edit consent, and report what those fixes returned. Use... | `skills/caveman-learn/SKILL.md` |
| caveman-manage | Inspect Caveman Cloud's experiment lifecycle and block unsafe execution. Use when asked to start, approve, cancel, promote or roll back a Caveman experiment. | `skills/caveman-manage/SKILL.md` |
| caveman-optimize | Turn a Caveman optimization observation into an operator-chosen candidate with a paired baseline evaluation. Use when asked to inspect or evaluate a Caveman... | `skills/caveman-optimize/SKILL.md` |
| caveman-review | Compressed code review - one line per finding with location, problem and fix. Use for /caveman-review, "review this PR", or "review the diff". | `skills/caveman-review/SKILL.md` |
| caveman-setup | Wire a repository through the Caveman Cloud gateway so every LLM request is measured, with no behavior change. Use for "set up caveman" or adding LLM spend... | `skills/caveman-setup/SKILL.md` |
| caveman-stats | Show recorded output and cache-read token usage and mode attribution for the current Claude Code session, or locate the host's native usage report. Trigger:... | `skills/caveman-stats/SKILL.md` |
| caveman | Ultra-compressed communication mode that cuts output tokens while keeping technical accuracy. Levels: lite, full, ultra and the wenyan variants. Use for... | `skills/caveman/SKILL.md` |
| investigate-first | Diagnose ambiguous failures before editing. Use for unknown causes, intermittent behavior, performance regressions, or investigations needing... | `skills/investigate-first/SKILL.md` |
| lean-build | Build feature work with high overbuilding risk. Use for new behavior, product slices, or integrations where repository reuse, strict scope, and an explicit... | `skills/lean-build/SKILL.md` |
| migration | Implement reversible compatibility-safe transitions. Use for schema, data, API, protocol, configuration, or dependency migrations requiring rollback and... | `skills/migration/SKILL.md` |
| safe-refactor | Restructure code while preserving behavior. Use for extraction, consolidation, ownership moves, or cleanup where verification must bracket structural edits. | `skills/safe-refactor/SKILL.md` |
| surgical-patch | Fix bugs and small behavior changes at the narrowest responsible layer. Use when regression proof, preserved surrounding behavior, and task-relevant tests... | `skills/surgical-patch/SKILL.md` |
| verify-and-stop | Prove existing work meets acceptance conditions without expanding scope. Use for validation-only tasks, completion checks, focused gate runs, and last-mile... | `skills/verify-and-stop/SKILL.md` |
| cavecrew-builder | Surgical 1-2 file edit. Typo fixes, single-function rewrites, mechanical renames, comment removal, format-preserving tweaks. Hard refuses 3+ file scope.... | `agents/cavecrew-builder.md` |
| cavecrew-investigator | Read-only code locator. Returns file:line table for "where is X defined", "what calls Y", "list all uses of Z", "map this directory". Output is... | `agents/cavecrew-investigator.md` |
| cavecrew-reviewer | Diff/branch/file reviewer. One line per finding, severity-tagged, no praise, no scope creep. Output format `path:line: <emoji> <severity>: <problem>.... | `agents/cavecrew-reviewer.md` |
