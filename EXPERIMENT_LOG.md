📓 Experiment Log — NEURONAL-CITY

This log tracks every AI-assisted development session for this project: what was asked, which AI did it, what happened, and what was learned. This is the raw material behind the "100% AI-assisted" claim.

---

## How to log an entry

Each entry should include:
- **Date**
- **AI used** (Claude / ChatGPT)
- **Phase / Feature** being worked on
- **Prompt(s) used** (summarized or verbatim)
- **What happened** (result, errors, surprises)
- **Iterations** (how many tries it took to get a working result)
- **Decisions made** (design choices, trade-offs, why)

---

## Entries

## Entries

### 2026-08-13 — Phase 0: Repo setup
- **AI used:** Claude
- **Prompt(s):** Requested repo structure and guidance to initialize the Git repository connected to GitHub.
- **Result:** Repo created with README.md, EXPERIMENT_LOG.md, .gitignore, and simulation/, web/ folders. Ran into a snag: the local folder wasn't actually a clone of the GitHub repo, so `git status` failed with "not a git repository." Fixed by running `git init`, adding the remote, and pushing directly.
- **Iterations:** 1 (plus 1 troubleshooting round for the Git connection issue)
- **Notes:** Good early lesson — "the folder looks right in VS Code" doesn't mean it's actually a Git repo. Worth keeping in the log as a real vibecoding hiccup, not just a code bug.

### 2026-08-13 — Phase 1: Agente class (MVP core)
- **AI used:** Claude
- **Prompt(s):** Defined design for Agente class (hunger/energy 0-100, unlimited money, profession affecting income) after ChatGPT suggested refining the initial needs design.
- **Result:** Implemented `Agente` class with `comer()`, `descansar()`, `trabajar()`, and `vivir_un_dia()` methods. Tested with 3 scenarios: fresh agent, two agents with different professions over 10 days, and an edge case (agent with no money and low hunger). All behaved as expected — agents autonomously choose to eat, rest, or work based on their own state.
- **Iterations:** 1 (worked correctly on first implementation)
- **Notes:** Interesting emergent behavior even at this simple stage: agents naturally cycle between working, resting, and eating without being told to — purely from priority rules based on their internal state.