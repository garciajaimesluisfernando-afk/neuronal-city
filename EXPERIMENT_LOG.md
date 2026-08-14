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

### 2026-08-13 — Phase 1: Ciudad class (multiple agents, shared days)
- **AI used:** Claude
- **Prompt(s):** Requested a way to make several agents live together through shared days, building on the existing Agente class.
- **Result:** Implemented `Ciudad` class that holds a list of agents and advances them together day by day, printing a daily report. Tested with 4 agents (3 different professions + 1 starting in poverty).
- **Iterations:** 1
- **Notes:** Interesting emergent behavior: an agent starting with low hunger and zero money gets stuck in a "poverty trap" — it always prioritizes eating (which it can't afford) and never gets to work, so it never earns money. Nobody programmed this specifically; it emerged from the priority rules. Worth deciding later whether to fix this (e.g. letting agents work anyway with a penalty) or keep it as a realistic feature of the simulation.


### 2026-08-13 — Phase 2: First web visualization
- **AI used:** Claude
- **Prompt(s):** Requested a simple web page that reads historial.json and shows agents as colored circles on a canvas, with day navigation and hover info.
- **Result:** Built `web/index.html` — a self-contained HTML/CSS/JS page with a canvas showing one circle per agent (colored by profession), day navigation buttons, and hover tooltips showing full agent state. Needed a local server (`python -m http.server`) to test it, since browsers block reading local files directly for security.
- **Iterations:** 2 — first attempt showed a blank page because the file hadn't actually been saved to disk before testing; fixed by saving and restarting the server.
- **Notes:** Real vibecoding lesson: the code being correct isn't enough if you forget to save the file. Good reminder to always double-check the browser's "view source" when something looks blank — it tells you what the server is actually sending, not what you think you wrote.


### 2026-08-13 — Phase 2: agent movement + stat bars
- **AI used:** Claude
- **Prompt(s):** Requested random agent movement between days and visual bars (yellow=hunger, blue=energy, green=money) above each agent.
- **Result:** Agents now appear at a random position on the canvas each day, with three small bars showing their hunger, energy, and money at a glance. Money has no real limit, so a visual cap (300) was used just for the bar's fill percentage — the real number is still shown in the hover tooltip.
- **Iterations:** 1
- **Notes:** Small but important design choice: separating the "real" unlimited value (money) from its "visual representation" (a capped bar) — a common pattern when visualizing unbounded data.