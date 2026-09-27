# ansitable — Agent Instructions

Part of the RVC ecosystem. **Read [rvc-ecosystem/AGENTS.md](https://github.com/petercorke/rvc-ecosystem/blob/main/AGENTS.md) first** — it defines shared conventions: repo ownership, math invariants, dependency boundaries, git/PR workflow, code standards, tech-debt tracking. This file only adds what's specific to this repo.

| | |
|---|---|
| PyPI package | `ansitable` |
| Nickname | ansitable |
| Owner | Peter Corke (`petercorke`) |
| Default branch | `main` (migrated from `master` 2026-09-27) |
| Contribution model | **Lightweight, solo-maintained — lighter than the ecosystem default** |

## Notes specific to this repo

- Solo-maintained workflow: one branch per issue/fix, merged **locally** with `--no-ff`, not
  pushed or tagged until explicitly told to release. Multiple merged-but-unpushed branches can
  sit on local `main` at once, released together as a batch. Full PR ceremony isn't required
  here — Peter is the sole regular committer, so routine work lands via direct push/local
  merge rather than a PR against himself. CI (`.github/workflows/master.yml`) does trigger on
  both `push` and `pull_request` to `main`, so a PR that does get opened (e.g. dependabot, an
  external contributor) is still tested.
- Still has a `tech-debt.md` file at repo root — legacy practice, not a deliberate permanent
  exception. Migrating to GitHub Issues (the ecosystem standard) is on the list, not urgent.
- Codacy badge is live on this repo.
- Standalone utility package — no internal ecosystem dependencies; used by RTB, MVTB, and
  bdsim.
