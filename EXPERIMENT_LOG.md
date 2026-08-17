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


### 2026-08-14 — Phase 1 fix: poverty trap
- **AI used:** Claude
- **Prompt(s):** Requested a fix for an emergent bug found earlier — an agent with low hunger and no money would get stuck forever, always trying to eat and never earning money to afford it.
- **Result:** `comer()` now returns True/False depending on whether the agent could actually eat. `vivir_un_dia()` uses this: if eating fails, the agent works instead as a fallback, so it can earn money and eat the next day.
- **Iterations:** 1
- **Notes:** Fixing an emergent bug like this required understanding *why* it happened first — a good example of debugging behavior that comes from rules interacting, not from a broken line of code.

### 2026-08-14 — Phase 2: autoplay button
- **AI used:** Claude
- **Prompt(s):** Requested a "play" button that automatically advances days, like a simple animation.
- **Result:** Added a "▶ Reproducir" / "⏸ Pausar" toggle button. When active, it advances one day per second automatically and stops on its own when it reaches the last day in the history.
- **Iterations:** 1
- **Notes:** Small UX addition, but makes the demo much more shareable — no need to manually click through days anymore.


### 2026-08-14 — Phase 3 planning: a debate between two AIs
- **AI used:** Claude + ChatGPT
- **Prompt(s):** Asked Claude to review the project status and propose what Phase 3 should include (relationships, economic depth, random events, or anything else it considered important) — without implementing anything yet, proposal only. The same context was then shared with ChatGPT for its independent perspective.
- **Result:** Both AIs agreed that a metrics system (population, average hunger/energy, wealth distribution, etc.) should come before any of the bigger Phase 3 features, since it gives an objective way to measure whether later changes actually help or hurt the city.

  Where they disagreed was on the order of the rest: 
  - **ChatGPT's proposal:** Relationships → Economy → Events. Reasoning: relationships turn isolated agents into a "society" early, which is narratively richer.
  - **Claude's proposal:** Economy → Events → Relationships. Reasoning: economy is a direct extension of systems that already exist (Agente/Ciudad already handle money and work), Events are technically simple (temporary changes to global variables) with high narrative payoff, and Relationships are the most complex to implement (bidirectional state, new visualization needs) — better attempted with more experience under the belt.

  **Decision:** The human project director reviewed both arguments and chose Claude's sequence: Metrics → Economy → Events → Relationships → Personalities.
- **Iterations:** N/A (planning discussion, not code)
- **Notes:** This is a good example of what "director + two AI collaborators" actually looks like in practice — not just picking whichever AI answers first, but comparing reasoning and making an informed call. Worth highlighting in future LinkedIn updates about the project.


### 2026-08-14 — Phase 3.0: city-wide metrics
- **AI used:** Claude
- **Prompt(s):** Requested a metrics system for the city (survival, economy, wellbeing stats), agreed on by both Claude and ChatGPT as the first priority for Phase 3. Then requested a panel in the web page to display these metrics per day.
- **Result:** Added `calcular_metricas()` to `Ciudad`, computing population, agents with critical hunger, agents with no money, total/average/min/max money, and average hunger/energy. These are now included in every daily snapshot in `historial.json`. Added a metrics panel below the canvas in the web page, showing all 8 numbers, updating as the day changes.
- **Iterations:** 2 — the metrics panel showed empty at first because part of the JavaScript (the `dibujarMetricas` function) hadn't actually been saved into the file, even though it looked pasted. Diagnosed using the browser console (`typeof dibujarMetricas` returned `undefined`) and a text search in the editor.
- **Notes:** Real lesson: "I pasted it" doesn't always mean it landed — verifying with the browser console (or a simple search in the file) is more reliable than assuming. Next improvement planned: move the metrics panel next to the canvas instead of below it, for better layout.


### 2026-08-15 — Bug fix: layout shifting on long tooltip text
- **AI used:** Claude
- **Prompt(s):** Reported a visual bug: hovering over certain agents (Luis, Carlos) made the metrics panel disappear or jump position — but only on some days, and the bug seemingly "fixed itself" when DevTools (F12) was open.
- **Result:** Diagnosed as a CSS layout bug: the left column (canvas + tooltip) had no fixed width, so longer tooltip text (from agents with longer "última acción" strings) stretched the column and pushed the metrics panel around. Fixed by giving the column a fixed width (matching the canvas) and allowing the tooltip text to wrap instead of stretching the layout.
- **Iterations:** 1, but required back-and-forth observation to pin down the pattern (which days, why DevTools "fixed" it) before finding the real cause.
- **Notes:** Good example of content-dependent layout bugs — the code technically "worked," but only revealed the bug with specific data. The clue that mattered most: noticing it changed when the window width changed (DevTools open vs closed).


### 2026-08-17 — Phase 3.1: deeper economy (rent, shared food price, wealth gap)
- **AI used:** Claude
- **Prompt(s):** Requested making the food price controlled by Ciudad (not a fixed constant per agent) as groundwork for future events, plus a periodic rent charge and a wealth-gap metric.
- **Result:** `Ciudad` now owns `precio_comida`, passed to each agent's `vivir_un_dia()`. Added `pagar_renta()` to `Agente`, charged automatically by `Ciudad` every 7 days. Added `brecha_economica` (richest minus poorest agent) to the metrics.
- **Iterations:** 1 for the design, but the bug below took a full separate debugging session to resolve.
- **Notes:** Money inequality is already visible after 14 days (gap grew from ~180 to ~255 between the richest and poorest agent) — a nice early signal that the simulation is starting to show emergent economic patterns, not just individual survival.

### 2026-08-17 — Bug fix: unsaved file caused a duplicated line
- **AI used:** Claude
- **Prompt(s):** Reported that hunger was dropping by 30/day instead of 15/day, even after the code looked correct.
- **Result:** After ruling out `__pycache__`, duplicate files, and checking the code multiple times, the real cause was much simpler: the file had unsaved changes in the editor (a duplicated line from an earlier paste) — the terminal was reading the old saved version from disk, which still had the duplication, regardless of what the editor displayed.
- **Iterations:** Several rounds of investigation (checking pycache, searching for duplicate files, verifying via `cat` directly from disk) before finding the actual cause.
- **Notes:** Real lesson: "the editor shows it correctly" is not proof that the file is saved. The unsaved-changes dot (●) on the tab was the actual signal, and checking it early would have saved a lot of back-and-forth. Worth remembering for future sessions.