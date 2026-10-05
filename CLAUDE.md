# CLAUDE.md — working instructions for this repo

Research project: evolutionary game theory over source-observing programs ("program ecologies"). Working title only, no paper or draft planned (RS, 2026-10-04): *Program ecologies: stochastic stability in open-source games.* Collaborator: Jacob (RS). You (Claude Code) now own the whole loop: read results, reason about theory, write predictions, run, and edit docs.

## Long-term goal (RS, 2026-10-02)
Get Turing-complete program classes with source access to cooperate. The DSL arms, including the modal arm's free sound oracle, are approximations. Judge each result by what it says about realizable source-reading programs.

## Files
- `NOTATION.md` — running glossary of symbols, statistics and program names. Add an entry whenever a symbol is introduced.
- `DEFERRED.md` — decisions punted to a later Fable, each with its current *operating hypothesis*. Operating hypotheses are acted on but not defended; they move without ceremony. Add an entry whenever a decision is deferred.
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
8. **Experiment workflow** (RS, 2026-10-04; replaces the astra-then-fable gauntlet). Three steps:
   1. **Spec.** The RE (Fable) drafts a subagent spec in `specs/YYYY-MM-DD-<slug>.md`: the object, the design, the required outputs, and the RE's own numbered predictions with falsifiers. The RS is invited to add his own predictions now and then; the RE should prompt him for them when a result is genuinely uncertain.
   2. **Review by sol.** `python3 tools/review.py specs/<file> --context CLAUDE.md --model gpt-6.1-sol` (needs OPENAI_API_KEY in `.env`, gitignored; background mode with polling). Fold the material points into the spec, marked [after review], and commit the spec before launch.
   3. **Run by an Opus subagent** (Agent tool, model `opus`, own worktree). It computes the static numbers, writes `predictions/` from the spec (committed before the run), runs within 3 workers, writes `runs/`, and hands back drafts for RESULTS/REJECTED/THEORY. The RE merges, writes the shared docs, and surfaces to the RS only what matters for the program.

   **Autonomy** (RS, 2026-10-04): be maximalist with experiments; they cost the RS only tokens. Run them autonomously under this workflow, in parallel within the 10-core budget, and report only the ones that matter, spending roughly as many tokens on a result as were spent discussing the experiment.

   Keep-awake must be on while subagents run (`mcp__ccd_host__request_keep_awake`, session_idle). A closed lid still stalls them; stalled agents stay paused until the RS says go.

## Current state (2026-09-23, after the island model)
- `ROLE` is first-class (modeling commitment: public correlating signal).
- B fails well-mixed in dilemmas and fixed-role bargaining; mechanism = **unconditional shadow** (conditional program on-path identical to a constant; constant drifts in at μ/N with a large class-size advantage; then gets exploited).
- Lattice (ε→0 object, `src/lattice_rates.py`): ρ_enter(`THEM(^C)`) = 0.11, N-independent; M_exit grows ~N^0.5–0.8; cooperative share 8% (32²) → 14% (64²). Not efficient in lim_N at any rate visible. FairBot sea long-lived but unreachable by nucleation; the FairBot-pruning hypothesis is falsified. Finite εN = 1 at 128² converges to a `THEM(^C)` sea (approach rate, not π).
- lim_N chain (2026-09-28, `src/limN.py`): cooperation peaks at N ≈ 300–3,000 (0.013–0.014) and falls like N^(−1/2). The shadow's exit is μ(C)/N and vanishes; **the faker's exit is N-independent and binds in the limit.** Working conjecture (THEORY §9.2): Σ is efficient iff some efficient-supporting program enters neutrally (no grounding cost) and is unfakeable. Candidate: a modal (provability) arm.
- Priced arm (2026-10-01, `build_priced`, `src/priced_limN.py`, `src/graph_rates.py`):
  - *Atom pricing:* kills well-mixed cooperation through an entry barrier plus the price ladder (ALLC strictly invades FairBot).
  - *Torus:* entry becomes N-independent, but the ladder stays.
  - *Lazy pricing (free against constants and copies):* escapes the ladder; at n = 8 it locks in an ALLC-punishing prover family through cost incumbency.
  - *Cliques:* absorbing.
- Modal follow-ups (2026-10-01):
  - *Matched control:* same grammar and prior; simulation reaches 0.009 at N = 3·10⁴, provability 0.70. Provability alone carries the effect.
  - *Ratchet:* PrudentBot/FairBot plateaus near 0.04; P(C,C) is 0.87 at N = 3·10⁵.
  - *Finite εN:* the modal arm is at 0.99 on one well-mixed island (a defector fringe prunes the shadow); the weak arm is at 0.06.
- Island-level selection (2026-09-30, `src/multilevel.py`, `src/multilevel_scaling.py`): payoff-weighted emigration rescues the PD only at strong between-island selection (w_g ≈ 10 at N = 100 gives P(C,C) 0.75). The threshold rises with island size (w_g* 4.2 / 4.8 / 9.0 at N = 50 / 100 / 200), so this is a finite-size rescue. Suppressing fakers brings the shadow back as the main exit.
- ε = 0 lottery concentrates on mutual defection as the island count grows (all 20 runs at 1,024 islands). Mutation stays in the object.
- Operating hypothesis (RS, 2026-10-04; DEFERRED.md 1): two objects. The ε = 0 seeding lottery (P(efficient) → 1 along a path in (N, I)) is primary for the Turing-complete goal; lim_N under rare mutation is kept as the stress test for unfakeability. Corollary 1 is a theorem about re-injection and does not bind at ε = 0.
- Decisions (RS, 2026-09-30): policy regret over response regret, defined per subpopulation with a horizon; spatial structure over the mutation prior, keeping μ = length prior fixed and taking limits of a fixed graph family (hypercubes proposed, fixed-degree tori as control); runtime price re-opened with its form left open.
- Modal arm (2026-09-30, `src/modal.py`, `src/modal_limN.py`): cooperation rises with no peak, to P(C,C) 0.73 at N = 3·10⁴ (w = 0.3), with the cooperative/D ratio ∝ N^0.44. The support is a family of provers (FairBot, `BOX1(THEM(ME))`, …); exits are neutral drift into ALLC, ∝ 1/N. Caveats: efficiency is built in by a free sound oracle, so the content is the exponent; the weak-vs-modal comparison is confounded by X and `ROLE`.
- Islands at ε = 0 (`src/islands.py`): non-ergodic absorption lottery. B′ falsified in PD (all-`THEM(^C)` in 17.5% of runs) and narrowly in Chicken with `ROLE`. **Without mutation the spoiler is the faker, not the shadow or the subsidized front.** A holds as a set, fails for placement. The migration game (ρ − ρᵀ) is not the ε-free object.

- Round of 2026-10-01/02 (RESULTS sections "Certificates-only arm", "Price scaling paths", "Certificate pricing", "Rival networks", "Ergodic islands", "Universality against drift-closure"; chain polish bug fixed in a49a007, which affected only c = 1e-3 priced cells):
  - **Certificates:** what the conjecture needs is *outcome symmetry*.
    - A C-seeded (coinductive) certificate FairBot is a mirror, with no faker and neutral entry. Löb is the way to get symmetry without a selection rule.
    - D-seeded and stratified certificates reproduce the faker limit; tags give parochial cliques.
    - Readers of truth are fakeable through probes; provers are not.
  - **Price scaling** (c_N = c0·N^-α): cooperation goes to 1 iff α > 1/2. The chain follows the two-edge reduction, and the free arm's β is 0.49–0.50.
  - **Certificate pricing:** the free set (PA decides the opponent's action) amounts to monotonicity in box atoms. It gives one network at the free arm's rate. Copy subsidies are what produce lock-in.
  - **Lazy pricing on graphs:** incumbency is a well-mixed effect. On the torus, prior mass picks the network. At finite ε, an ALLC-punisher wins borders by eating the shadow.
  - **Ergodic islands:** the faker's fixation is a constant-selection invariant (Maruyama), so islands act only on entry and the shadow. The weak arm stays at or below 0.13 on islands, while modal odds grow ∝ M.
  - **Drift-closure** (proved in the pure PD game):
    - universality and drift-closure are exclusive;
    - β = 1/2 is derived;
    - beating 1/N with free constants requires incumbency;
    - a fringe closes families only onto the parochial P* at n ≥ 8.

- Round of 2026-10-04/05 (spec → gpt-6.1-sol → Opus workflow; RESULTS sections "Three-player majority divide-the-dollar", "Almost all seeds?", "Conjecture 4: the sibling theorem", "The closed club", "Bounded provers", "Proof-carrying contracts v1", "Almost all seeds: cutoff sensitivity in n", "the tail in n", "Spoiler-conditioned establishment", "The scramble lemma and Claim A", "compatibility among co-seeded establishers", "The union game", "Prover-carrier seed at b = 0"):
  - **Sibling theorem (Conjecture 4 proved):** no class in the unbounded modal language is drift-closed; the obstruction is extensionality, not GL. **Lemma 0:** soundness buys unfakeability, Löb buys self-cooperation.
  - **Seed lottery (primary object, DEFERRED 1):** "almost all seeds" holds for the modal arm at n = 6–12 in every regime; establishment is rigorously positive uniformly in n (μ_est ≥ 0.0207); the lottery runs on D-entering self-cooperators, not unfakeability; co-seeded fakers die in the scramble by demography; compatibility resolves on islands (two self-cooperators cannot hold a stable mixture); the clean claim is on the fakerless pair (FairBot, `BOX1(THEM(ME))`); the open risks are between islands (rival networks) and the I ≫ N migration rule.
  - **Closure:** the club is a clique by declaration; a stabilization-cost budget is harmless and closes nothing (leaks run through cheaper neighbours); proof-carrying contracts need Löb, equal the free box among carriers, restore legibility where a gate binds, and spread from prover seeds above ~1–3% (with an asymmetric-read caveat).
  - **Distribution (k = 3, fixed roles):** stochastic stability selects rotating, mostly unfair pairs; source reading adds nothing (the exit is a partner's own strict defection); the union game puts π at zero wage, the quorum is FairBot's strike handshake, the prior decides the fair share, and a strike pact's wage check is fakeable (the polarity dilemma).

## Queue after that
1. Symmetric gate control for carrier seeds (is carrying an advantage without the sucker fringe?).
2. Rival networks across islands along I ≫ N: does migration merge, separate, or let one win? The mN scaling rule.
3. The demographic lemma (survival ≤ k₀/(1 + b_min·τ)) and the P(A ∧ F) bound without the 1/P(A) loss.
4. Incentive-compatible enforcement (sol's follow-up to the union game); the worker grammar/prior (DEFERRED 10).
5. An explicit proof system with measured proof length, in place of the stabilization proxy.
6. Divide-the-dollar partitions across islands with `ROLE` (RS, 2026-10-02; paused worktree agent-aefc4dd3cf297898f holds partial game files).

No paper draft (RS, 2026-10-04).
