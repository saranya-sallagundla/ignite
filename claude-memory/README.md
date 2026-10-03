# Claude memory — synced copy

This folder is a human-readable, synced **copy** of the ignite-related memory files Claude Code
keeps for this project. The files Claude actually reads at the start of every session live at
`C:\Users\devuser\.claude\projects\C--CloudOps\memory\` — that fixed location is what the harness
auto-loads into context, so it's the source of truth, not this folder.

This copy exists purely for easy access/browsing/backup inside this repo, committed and pushed
like any other file, without having to dig into the `AppData`-based path. Claude keeps it in
sync: whenever a memory file changes, the matching copy here is updated in the same turn.

- [MEMORY.md](MEMORY.md) — index copy
- [project_ignite_learning_mission.md](project_ignite_learning_mission.md)
- [feedback_ignite_teaching_style.md](feedback_ignite_teaching_style.md)
- [feedback_repo_audit_approach.md](feedback_repo_audit_approach.md)
