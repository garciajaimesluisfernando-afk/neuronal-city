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

- [ ] Phase 0 — Repo setup & documentation
- [ ] Phase 1 — MVP: simulation engine (console output)
- [ ] Phase 2 — First web visualization
- [ ] Phase 3 — Relationships, economy, events
- [ ] Phase 4 — Portfolio polish