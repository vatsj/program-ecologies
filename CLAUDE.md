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
8. **External review before runs** (RS, 2026-09-30). Send each experiment brief (the predictions draft) to two reviewers before running, in this order:
   1. **astra**, a fast first check: `gpt-6-astra` through `python3 tools/review.py <brief> --context CLAUDE.md`, which needs OPENAI_API_KEY in `.env` (gitignored) and runs in background mode with polling;
   2. **fable**, the thorough pass: a Claude subagent via the Agent tool with model `fable`. It may read the repo and should see astra's review, so it doesn't repeat it.

   Save both reviews under `reviews/`. Fold material points into the design before committing the predictions. Surface to Jacob only what matters for the program as a whole.

## Current state (2026-09-23, after the island model)
- `ROLE` is first-class (modeling commitment: public correlating signal).
- B fails well-mixed in dilemmas and fixed-role bargaining; mechanism = **unconditional shadow** (conditional program on-path identical to a constant; constant drifts in at μ/N with a large class-size advantage; then gets exploited).
- Lattice (ε→0 object, `src/lattice_rates.py`): ρ_enter(`THEM(^C)`) = 0.11, N-independent; M_exit grows ~N^0.5–0.8; cooperative share 8% (32²) → 14% (64²). Not efficient in lim_N at any rate visible. FairBot sea long-lived but unreachable by nucleation; the FairBot-pruning hypothesis is falsified. Finite εN = 1 at 128² converges to a `THEM(^C)` sea (approach rate, not π).
- lim_N chain (2026-09-28, `src/limN.py`): cooperation peaks at N ≈ 300–3,000 (0.013–0.014) and falls like N^(−1/2). The shadow's exit is μ(C)/N and vanishes; **the faker's exit is N-independent and binds in the limit.** Working conjecture (THEORY §9.2): Σ is efficient iff some efficient-supporting program enters neutrally (no grounding cost) and is unfakeable. Candidate: a modal (provability) arm.
- Island-level selection (2026-09-30, `src/multilevel.py`, `src/multilevel_scaling.py`): payoff-weighted emigration rescues the PD only at strong between-island selection (w_g ≈ 10 at N = 100 gives P(C,C) 0.75). The threshold rises with island size (w_g* 4.2 / 4.8 / 9.0 at N = 50 / 100 / 200), so this is a finite-size rescue. Suppressing fakers brings the shadow back as the main exit.
- ε = 0 lottery concentrates on mutual defection as the island count grows (all 20 runs at 1,024 islands). Mutation stays in the object.
- Decisions (RS, 2026-09-30): policy regret over response regret, defined per subpopulation with a horizon; spatial structure over the mutation prior, keeping μ = length prior fixed and taking limits of a fixed graph family (hypercubes proposed, fixed-degree tori as control); runtime price re-opened with its form left open.
- Modal arm (2026-09-30, `src/modal.py`, `src/modal_limN.py`): cooperation rises with no peak, to P(C,C) 0.73 at N = 3·10⁴ (w = 0.3), with the cooperative/D ratio ∝ N^0.44. The support is a family of provers (FairBot, `BOX1(THEM(ME))`, …); exits are neutral drift into ALLC, ∝ 1/N. Caveats: efficiency is built in by a free sound oracle, so the content is the exponent; the weak-vs-modal comparison is confounded by X and `ROLE`.
- Islands at ε = 0 (`src/islands.py`): non-ergodic absorption lottery. B′ falsified in PD (all-`THEM(^C)` in 17.5% of runs) and narrowly in Chicken with `ROLE`. **Without mutation the spoiler is the faker, not the shadow or the subsidized front.** A holds as a set, fails for placement. The migration game (ρ − ρᵀ) is not the ε-free object.

## Queue after that
1. Modal (Löbian) arm: provability-guarded self-reference; test whether it meets both conditions of the characterization (re-opens REJECTED 'Black-magic fixed points' — justify via unique fixed points).
2. Optional: ergodic island model (mutation at ε ≪ m), where π exists: which exit dominates when fakers and shadows are both re-injected (THEORY §9.5 (i)).
3. Optional diagnostic: prior uniform over behaviours.
4. Paper draft.
