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

## Current state (2026-09-23, after the island model)
- `ROLE` is first-class (modeling commitment: public correlating signal).
- B fails well-mixed in dilemmas and fixed-role bargaining; mechanism = **unconditional shadow** (conditional program on-path identical to a constant; constant drifts in at μ/N with a large class-size advantage; then gets exploited).
- Lattice (ε→0 object, `src/lattice_rates.py`): ρ_enter(`THEM(^C)`) = 0.11, N-independent; M_exit grows ~N^0.5–0.8; cooperative share 8% (32²) → 14% (64²). Not efficient in lim_N at any rate visible. FairBot sea long-lived but unreachable by nucleation; the FairBot-pruning hypothesis is falsified. Finite εN = 1 at 128² converges to a `THEM(^C)` sea (approach rate, not π).
- Islands at ε = 0 (`src/islands.py`): non-ergodic absorption lottery. B′ falsified in PD (all-`THEM(^C)` in 17.5% of runs) and narrowly in Chicken with `ROLE`. **Without mutation the spoiler is the faker, not the shadow or the subsidized front.** A holds as a set, fails for placement. The migration game (ρ − ρᵀ) is not the ε-free object.

## Queue after that
1. Optional: ergodic island model (mutation at ε ≪ m), where π exists: which exit dominates when fakers and shadows are both re-injected (THEORY §9.5 (i)).
2. Optional diagnostic: prior uniform over behaviours.
3. Paper draft.
