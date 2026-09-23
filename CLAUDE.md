# CLAUDE.md — working instructions for this repo

Research project: evolutionary game theory over source-observing programs ("program ecologies"). Paper title: *Program ecologies: stochastic stability in open-source games.* Collaborator: Jacob. You (Claude Code) now own the whole loop: read results, reason about theory, write predictions, run, and edit docs.

## Files
- `THEORY.md` — the operating hypothesis. Change only with a stated reason tied to a result.
- `IMPLEMENTATION.md` — DSL, evaluator, chain, runtime rules.
- `RESULTS.md` — append-only record of runs. Never rewrite a past verdict; add addenda.
- `REJECTED.md` — ledger of dropped proposals with reasons. **Check it before proposing anything**; if a proposal re-opens an entry, say so explicitly and state what new evidence justifies it.
- `predictions/` — dated verdict files.

## Discipline (non-negotiable)
1. **Predictions before runs.** Every experiment gets a `predictions/YYYY-MM-DD-*.md` with verdicts and an explicit falsifier, committed *before* the run. Report failures as failures.
2. **Scope each change.** One commit per task; a code fix must not silently edit a THEORY claim. Doc edits cite the RESULTS section that motivates them.
3. **Efficiency and distribution are evaluations, never selectors.**
4. **Always report support + transition structure alongside π weights.** Genuine limit cycles → indeterminate; bistable switching is not a cycle.
5. **Separate the ε→0 object from finite-εN dynamics.** Claims about π / conjecture B use ε-free quantities (per-mutant entry/exit rates). ABM runs at finite εN are about approach rates and must say so. A window shorter than mixing time is not π.
6. **Dilemma statistic is P(C,C)**, not mean-payoff share.
7. Update `REJECTED.md` whenever something is dropped, including your own wrong predictions.

## Current state (2026-09-23)
- `ROLE` is first-class (modeling commitment: public correlating signal).
- B fails well-mixed in dilemmas and fixed-role bargaining; mechanism = **unconditional shadow** (conditional program on-path identical to a constant; constant drifts in at μ/N with ~500× class-size advantage; then gets exploited). A second-order free-rider problem with zero punishment cost and neutral drift instead of active displacement.
- Lattice: entry fixed by pair nucleation (ρ≈¼ vs 1/N); exit via ALLC-subsidized D fronts; `THEM(^C)` regime plateaus at P(C,C)≈0.6. One 128² seed reached a FairBot `or(X,THEM(ME))` sea at 0.96.
- **Hypothesis under test:** FairBot's grounding noise makes lone D neutral, so roaming D prune ALLC and keep enforcement exercised. Pending runs: per-mutant rates (`src/lattice_rates.py`), 128² mixing check (3·10⁵ window). If FairBot is reachable and M_exit ≫ `THEM(^C)`'s, B′ may hold on the lattice in lim_N.

## Queue after that
1. Island model (conjectures A and B′; Chicken-without-ROLE falsifier; predicted spoiler = subsidized fronts, not fakers).
2. Optional diagnostic: prior uniform over behaviours.
3. Paper draft.
