# 🏙️ NEURONAL-CITY

> An autonomous city simulation where AI agents live, work, and evolve — built 100% with AI (vibecoding experiment).

## What is this?

NEURONAL-CITY is a simulation of an autonomous city populated by agents with their own needs (hunger, energy, money), jobs, relationships, and behaviors. Over time, the city evolves on its own as agents act based on their state.

## The experiment

This project is a deliberate **100% AI-assisted development experiment ("vibecoding")**. The rule is simple: **no code is written manually by a human.**

- 🧑‍💼 **Human (Project Director):** defines what to build, tests functionality, gives feedback, and makes product decisions — but does not write or debug code.
- 🤖 **Claude (Anthropic):** AI collaborator on the project.
- 🤖 **ChatGPT (OpenAI):** AI collaborator on the project.

Every prompt used, every bug encountered, every iteration, and every interesting decision made along the way is logged in [`EXPERIMENT_LOG.md`](./EXPERIMENT_LOG.md).

## Status

🚧 In active development — currently building the MVP simulation engine.

## Project structure

simulation/ → Python simulation engine (agents, world, economy)
web/ → Web-based visualization (HTML/JS/Canvas)


## Tech stack

- **Python** — simulation engine
- **JSON snapshots** — the engine exports the city's state over time
- **HTML/JS/Canvas** — static web visualization that reads and animates the snapshots (deployable via GitHub Pages, no backend needed)


## Roadmap

- [x] Phase 0 — Repo setup & documentation
- [x] Phase 1 — MVP: simulation engine (agents with needs, city loop, JSON export)
- [x] Phase 2 — First web visualization (canvas, movement, stat bars, autoplay)
- [ ] Phase 3.0 — City-wide metrics (survival, economy, wellbeing stats over time)
- [ ] Phase 3.1 — Deeper economy (salaries, prices, savings, inequality)
- [ ] Phase 3.2 — Random events (inflation, crises, festivals — consequence-driven)
- [ ] Phase 3.3 — Social relationships between agents
- [ ] Phase 4 — Agent personalities & emergent behavior
- [ ] Phase 5 — Portfolio polish

## A real debate between two AIs

An interesting moment happened during planning: ChatGPT and Claude proposed **different** orders for Phase 3. ChatGPT argued for Relationships → Economy → Events, prioritizing narrative richness first. Claude argued for Economy → Events → Relationships, prioritizing lower implementation risk and building on systems that already existed.

The human project director reviewed both arguments and made the call:

> ChatGPT initially proposed Relations → Economy → Events. Claude argued for Economy → Events → Relations based on implementation complexity and dependency on existing systems. After reviewing both approaches, the human project director selected Claude's sequence.

Full reasoning from both AIs is logged in [`EXPERIMENT_LOG.md`](./EXPERIMENT_LOG.md).