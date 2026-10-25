# Predictions: islands to infinity before time, rare migration, annealed mutation (2026-10-25)

Committed before any code of this experiment runs and before any counted cell. Spec `specs/2026-10-25-many-islands.md`
(reviewed by gemini-4-argon, then gpt-6.1-sol in `--mode amended`, both folded); notes `notes/many-islands.md` §1 (hand
analysis: the one-migrant event is a constant-fitness two-type Moran process, so the island-state chain is exactly
Markov on program triples with a closed-form kernel; the S₃ symmetry of the fair block; worked examples), written
before this file.

## The RS's messages (2026-10-25), verbatim from the spec

> "I dislike the idea of transient islands because I want a crisp, well-defined notion of limiting behavior. Another
> proposal to save it: send migration to zero alongside mutation (though probably at a slower rate, since migrants are
> from a more benign distribution than mutants)."

> "I thought we still needed rare mutation to re-introduce predators to eat a shadow of unconditional cooperators /
> exploitable PD programs. 2 approaches to save coverage of the stable set: 1) disconnected components 2) send num
> islands to infinity first. I think they're related and (2) feels like the sharper choice deriving a stronger
> statement, so I'd run both but shoot for (2) and tell me if and where it fails? Anything needing several migrants is
> EVENTUALLY lost. This is why we decayed mutants - simultaneous mutations are kinda cursed."

The statement to be tested or refuted: *with mutation annealed to zero, migration rare (the mN → 0 jump chain), and
the number of islands → ∞ before time, three-player majority division ends with every island efficient and all three
fair pairs present.*

## Frozen design choices (made before any run; spec silent)

- Annealing: Poisson(A) arrivals per island, intensity (1/t₀)(1 + (t − t₁)/t₀)^(−2) on t ≥ t₁, **t₁ = 200, t₀ = 500
  generations**; an arrival picks a slot uniformly, draws a program from that slot's seed law and replaces a uniform
  resident. Founding is multinomial(N, seed law) per slot as in the stored lottery; relaxation after the last arrival
  to monomorphism (cap 20,000 generations; capped islands are counted, disclosed and excluded from the triple chain).
- Arms: **L** (weak evaluator, length prior, stored seed law), **M** (modalPA evaluator, same law), **R** (E-min *main*
  catalogue, modalPA evaluator; flexible readers ≈ 9% of the seed, `churn_primary.get_cat('Emin-main-m')`); **Rw**
  (the same catalogue under the weak evaluator) is an extra, not a registered arm. A ∈ {0, 50, 150}.
- Pools: 5 independent pools of 16,384 settled islands per (arm, A) cell (cut order in the spec if time binds). The
  4,096-island pools are the first quarter of each pool; the 65,536-island pool is pools 0–3 concatenated.
- One event: recipient island uniform, donor island uniform among the other islands of the recipient's component, slot
  uniform; the migrant (donor's program in that slot) fixes with the exact Moran probability (notes §1.2), else the
  island is unchanged. Validation (before any counted cell): the formula against simulated relaxation of the stored
  island kernel, draw for draw at the level of the kernel and statistically at the level of fixation frequencies.
- **Clock** = events per island. Spec checkpoints 1, 3, 10, 30, 100, 300, 1,000; **extension (not in the spec)**:
  3,000, 10,000, 30,000, 100,000 on pools (no extension is allowed to change the scoring of the spec's checkpoints).
- Classes (`migration_window.CATMAP`): F fair pair (three of them, F0 = {0,1}, F1 = {0,2}, F2 = {1,2}), U unequal
  pair (by pair and direction), G grand coalition (2,2,2), W wasteful (pair, grand-wasteful), D disagreement.
  **Efficient** = total payoff 1 (F, U, G); the registered statistic of predictions 3–5 is the **V\* share** (fair
  pairs), as in the spec, reported beside the efficient share and the mean total payoff.

## Statistics and scoring rules (fixed now)

- **V\* share** at a checkpoint = fraction of *settled* islands (triples) playing a fair pair. **Coverage** = every
  fair pair has share > 10⁻³. Intervals: across the 5 pools (t, 4 degrees of freedom) for pool means; Wilson for
  proportions of runs.
- **x₁₀₀₀** = value at the spec's last checkpoint (1,000 events per island) on the 16,384-island pools. **x_∞** =
  value at 100,000 events per island if its change over the last decade of the clock (10,000 → 100,000) is below 0.02
  in absolute value in every pool-mean, else "not converged" (the trajectory is reported and prediction scoring
  falls back to x₁₀₀₀, said so). A pool's terminal state is never identified with lim_t lim_I.
- Predictions 3, 4, 5 are **held** iff the stated inequality holds for both x₁₀₀₀ and x_∞ (or x_∞ not converged and it
  holds for x₁₀₀₀ with the trend not crossing the threshold), **failed** iff the falsifier holds for either, **partial**
  otherwise (labelled).
- Prediction 1: the net flow D_ab = [rate F_a → F_b − rate F_b → F_a] per event, over the three ordered pairs of fair
  pairs, computed exactly from K on the post-anneal pool (rates are probabilities per event of the class transition,
  expectation over recipient, donor and slot). Held iff for every (a, b) the five-pool 95% interval of D_ab contains
  0 in the L and M arms (and in R), at every A. The S₃-symmetrized D is zero by construction (a test) and is not the
  statistic.
- Prediction 6: first-loss time = events per island until the first checkpoint-free time at which some fair pair has
  zero islands, in (2a) runs (10 per I), measured on the event clock (checked every I/4 events), right-censored at
  100,000 events per island (extension) and, for the spec statement, at 1,000. Scaling = the slope of
  log(Kaplan–Meier median) on log I over the I with a defined median, with a bootstrap 95% interval. Held iff the
  slope's interval reaches 1 (≥ 0.8 allowed to count as "at least linear") and coverage at I = 4,096 at 1,000 events
  per island is ≥ 0.9 of runs (Wilson lower bound reported). If the median is undefined for I ≥ 64 (censored), the
  scaling is *unobservable* and scored **partial (censored)**.
- Prediction 7: |V\* share(C) − V\* share(1 component)| at 1,000 events per island, I = 1,024, per C ∈ {4, 16, 64},
  paired-by-construction islands (the same 1,024 islands, differently connected), mean over 10 runs; coverage across
  components = fraction of runs with all three fair pairs present among all 1,024 islands.

## Predictions (the RE's, verbatim from the spec, falsifiers in brackets)

1. *Fair pairs are neutral among themselves on average.* The symmetry-averaged antisymmetric part of the fair-to-fair
   block of K is zero within its interval for L and modalPA, by the slot symmetry of the grammar (this constrains the
   averaged kernel only; composition-conditioned transitions may be asymmetric) [a net flow outside the interval in
   either arm]. For readers the same, unless the catalogue breaks reflection symmetry (the notes check this first).
2. *Coverage holds in the I → ∞ limit.* In (2b) all three fair pairs keep positive shares in every arm [some pair's
   share → 0 in (2b) in any arm].
3. *Efficiency fails without readers.* Single migrants from fair islands rarely convert unequal, wasteful or
   disagreement islands (a mismatched migrant dies in about 10 generations), so in (2b) under L at A = 0 the V\* share
   stays below 0.6 (founding share about 0.28) [V\* share ≥ 0.9].
4. *Annealing helps efficiency but does not finish it.* Under L, A = 150 raises the post-anneal V\* share by at least
   0.1 over A = 0, and the (2b) limit stays below 0.9 [no rise, or ≥ 0.9].
5. *Readers carry conversion.* With readers at A = 150 the (2b) limit has V\* share ≥ 0.9 with coverage [below 0.9].
   This is the RE's least certain prediction. *Counter-prediction (gemini-4-argon), registered:* a single reader
   migrant into a dominated island is mismatched against the resident coalition and dies, the churn result needed
   overlapping migrants (mN ≥ 0.1), and V\* stays below 0.75 in (2b) even with readers.
6. *Finite I loses coverage slowly.* In (2a) the time to the first loss of a fair pair grows at least linearly in I
   [sublinear growth]; at I = 4,096 coverage is held in at least 0.9 of runs at the final time [below 0.9].
7. *Components and (2) agree on efficiency.* (1) gives the same V\* share as (2) within 0.05 at every C, and coverage
   across components ≥ 0.9 from C = 16 [disagreement beyond 0.05, or lower coverage]. *Counter-prediction (gpt-6.1-sol),
   registered:* smaller components lose rare conversion-carrying programs sooner, so efficiency depends on component
   size wherever readers or bridges are scarce.

Scoring of the two counter-predictions: gemini's is **held** iff V\* < 0.75 for R at A = 150 (x₁₀₀₀ and x_∞), **failed**
iff ≥ 0.75; sol's is **held** iff at some C ∈ {4, 16, 64} the L or M arm's V\* share differs from the one-component value
by more than 0.05 (95% interval excluding 0.05), **failed** otherwise.

## My own predictions, written after the notes' hand analysis (E1, E2, …)

Probabilities are my honest odds that the statement holds as scored.

- **E1 (the exactness).** The closed-form one-migrant kernel agrees with simulated relaxation of the stored island
  kernel: over at least 1,000 simulated events per arm the conversion frequency is within the binomial interval of the
  formula (cell by cell on the sampled (recipient, donor, slot) triples), and `kern` reproduces draw for draw on
  one-island runs [a disagreement, i.e. the Moran structure of §1.2 is wrong]. Odds 0.9.
- **E2 (V\* between founding and one half).** L, A = 0: the V\* share at x₁₀₀₀ is in [0.30, 0.50] and unequal pairs
  carry at least 0.40; wasteful plus disagreement carry at most 0.03 (they drain by the ratchet; F and U exchange only
  through the excluded slot at rates ~10⁻⁴ per event) [V\* outside the band, or W + D above 0.05]. Odds 0.6.
- **E3 (U is nearly absorbing).** The hazard of leaving U per event (exact K, post-anneal pool, L, A = 0) is at least 20×
  smaller than the hazard of leaving W, and the class-level chain is not Markov: the coefficient of variation of the
  per-recipient exit probability across recipients of the same class is ≥ 1 for U and for F (the excluded slot's content
  decides it) [CV < 0.5 for both, or the U/W hazard ratio below 5]. Odds 0.7.
- **E4 (annealing lowers V\* in L; against prediction 4).** Arrivals during relaxation give islands the chance to find
  local improvements; the ratchet favours the greedy step (larger fixation probability) and fills excluded slots with
  meek programs, so the post-anneal V\* share at A = 150 is *below* A = 0 by at least 0.05 [no fall of 0.05]. Odds 0.5.
  (This is the opposite sign of prediction 4; both are registered; at most one holds.)
- **E5 (readers raise V\* but not to 0.9).** R vs M at A = 150, x₁₀₀₀: V\* higher by at least 0.1 and below 0.9
  [difference < 0.1, or V\* ≥ 0.9]. Odds 0.4. Mechanism if it holds: a reader in a victim slot responds to an excluded
  migrant's offer, which makes that migrant strictly fitter (Δ = +3, P_fix 0.14), a single-migrant conversion that
  constants cannot make.
- **E6 (grand coalitions and unequal pairs persist to the extended clock).** At 100,000 events per island the pools
  still hold at least 0.3 of islands on U or G in L, A = 0 (F → U and U → F are both slow and U is not drained) [below 0.3]. Odds 0.7.
- **E7 (the extended clock matters for the symmetric state).** In (2a) at I = 256, the first-loss time on the extended
  clock is *not* ≥ linear in I between I = 16 and I = 256 (a positive feedback in the F→F flows makes the symmetric
  state unstable; the slope of log median on log I is below 0.8), while the spec checkpoint (1,000 events per island)
  sees no loss at all (censored) [slope ≥ 0.8, or a loss at 1,000]. Odds 0.4 for the pair of clauses jointly; I hold
  low confidence in the sign of the instability.
- **E8 (finite-I agreement).** The (2a) V\* share is within 0.05 of the pool value from I = 256 upward at 1,000 events
  per island, run mean over 10 runs [first I within 0.05 above 1,024]. Odds 0.8.
- **E9 (two migrants).** In the two-migrant probe from U islands, the simultaneous (overlap) conversion probability to F
  is within a factor of 5 of the sequential one (second migrant after full relaxation), i.e. overlap alone does not
  open a new route at these sizes; the efficiency failure is not "several migrants are eventually lost" but missing
  excluded-slot content [overlap more than 5× sequential]. Odds 0.5.
- **E10 (cryptic drift).** In U islands the mean hazard of conversion to F per event, after a neutral substitution of the
  excluded slot's program, is within [0.7, 1.4]× the hazard before (paired), in L at A = 0; with readers it is above 1.4 [outside the band for L]. Odds 0.5.
- **E11 (cost).** Founding plus relaxation of one L, A = 0 island costs ≤ 0.3 s on one core; one annealed A = 150 island
  ≤ 3 s; a 16,384-island A = 150 pool therefore ≤ 14 h. If the last is false the cut order applies and the cut is
  disclosed. Odds 0.5.

## Cut order (spec), disclosed in the report if used

I = 4,096 in (2a), modalPA beyond (2b), A = 50, components C = 4; additionally (mine, if the pool build binds) fewer
pools per annealed cell (down to 1 pool of 16,384 for A = 150), disclosed with the intervals that lose meaning.
