# Predictions: the pair-worth easy case along N (queue 73), 2026-11-03

Spec: `specs/2026-11-03-pair-worth-n.md` (reviewed by gemini-4-argon, then gpt-6.1-sol; folded). Written by the engineer from the spec before any counted cell; the predictions below are the spec's, verbatim, with the static numbers (computed first, `runs/pair_worth_n/static.json`), the manifest, the engineer's operationalizations of the reviewer predictions that the spec leaves without a number, and the engineer's own predictions. Reading guide: "core" is core proper (the 19 core grand splits) as the end class of an island's modal outcome; "paired" means shared founders and tail; a prediction whose cell is cut is **unscored**, not failed.

## Status before any counted cell

- Validation: **V6 passes** (F and F-minus against the play stated before evaluation, exhaustive over the F + constants catalogue, 4,741,632 triples per arm, 0 mismatches; independent explicit-equation chain on 9,811 triples, 0 mismatches; a mutated F is caught, so the test has power); V7 (common random numbers) and V8 (inoculation founders, F and F4 share laws) pass. V1 and V2 (stored-row reproduction) were running when this file was written; the launch of counted cells waits for them (results in `runs/pair_worth_n/validation_V*.json`).
- **Disclosure of what the engineer saw before writing this file:** one smoke run of C+F (N = 100, run 0, both mN) and C+B*_4 (N = 100, run 0, mN = 1) to test the pipeline, not scored (outputs not kept); in it every island had a compatible efficient grand support at founding (constants supply one), and C+F ended with every island in the core held by grand constants. The assays of cell F were run once as a smoke test before this file existed (exact values: matching grand constant neutral at exactly 1/N, pair offers and B*(sigma') entrants N p <= 0.035, as the equations imply); that run is **discarded and rerun** after this file is committed with fresh Monte-Carlo seeds. The static supply numbers below were computed before any run.

## Static supply numbers (spec Design 1; exact evaluation over the whole catalogue, G1/3, delta = 0.05)

P(...) = probability that one founder triple (one draw per slot from the arm's seed law) plays that outcome. Counts = N^3 P: the expected number of individual triples on one island at founding. "Named3" = all three programs are named (bid, F or grand constant). T = the spec's same-split count 28 n_sigma^3 (B*, G; 19 splits for B).

| arm | catalogue / slot | P(grand, any sum) | P(grand efficient) | P(core proper) | N^3 P(efficient) at N = 100 / 200 / 400 / 800 | named3 triples that play grand (any sum), N = 100 / 200 / 400 / 800 | T (closed form) 100 / 200 / 400 / 800 |
|---|---|---|---|---|---|---|---|
| C | 21 | 7.7766e-03 | 2.5922e-03 | 1.7590e-03 | 2.59e+03 / 2.07e+04 / 1.66e+05 / 1.33e+06 | 0 / 0 / 0 / 0 | - / - / - / - |
| C+B* | 609 | 9.3238e-03 | 3.3208e-03 | 2.2534e-03 | 3.32e+03 / 2.66e+04 / 2.13e+05 / 1.7e+06 | 0.219 / 1.75 / 14 / 112 | 0.159 / 1.28 / 10.2 / 81.6 |
| C+B | 420 | 9.3299e-03 | 3.3267e-03 | 2.3573e-03 | 3.33e+03 / 2.66e+04 / 2.13e+05 / 1.7e+06 | 0.428 / 3.43 / 27.4 / 219 | 0.346 / 2.77 / 22.2 / 177 |
| C+G | 49 | 1.3987e-02 | 4.4277e-03 | 3.0113e-03 | 4.43e+03 / 3.54e+04 / 2.83e+05 / 2.27e+06 | 73.2 / 585 / 4.68e+03 / 3.75e+04 | 0.159 / 1.28 / 10.2 / 81.6 |
| C+F | 168 | 1.4331e-02 | 4.6018e-03 | 3.1229e-03 | 4.6e+03 / 3.68e+04 / 2.95e+05 / 2.36e+06 | 73.2 / 585 / 4.68e+03 / 3.75e+04 | - / - / - / - |
| C+F4 | 126 | 1.5010e-02 | 4.7359e-03 | 3.2817e-03 | 4.74e+03 / 3.79e+04 / 3.03e+05 / 2.42e+06 | 95.3 / 762 / 6.1e+03 / 4.88e+04 | - / - / - / - |
| C+F- | 168 | 1.4339e-02 | 4.6049e-03 | 3.1250e-03 | 4.6e+03 / 3.68e+04 / 2.95e+05 / 2.36e+06 | 73.7 / 589 / 4.71e+03 / 3.77e+04 | - / - / - / - |

Three independent F shares from the (7 - s)/28 marginal are feasible (sum <= 6) with probability 0.5855 and efficient (sum = 6) with probability 0.1269; all feasible F triples play the grand coalition (V6). The F named supply (all-named feasible triples) is therefore about 460 times B*'s same-split supply at equal dose (73 against 0.16 at N = 100): F and G supply the same count, as they must (same feasibility), and constants alone already supply 2,600 efficient triples at N = 100 (every arm): **the grand coalition is never scarce, the question is which triples are selected.**

T for C+B* (28 n_sigma^3, n_sigma = delta N / 28) by dose and N:

| delta | N = 100 | 200 | 400 | 800 |
|---|---|---|---|---|
| 0.0125 | 0.00249 | 0.0199 | 0.159 | 1.28 |
| 0.025 | 0.0199 | 0.159 | 1.28 | 10.2 |
| 0.05 | 0.159 | 1.28 | 10.2 | 81.6 |
| 0.15 | 4.3 | 34.4 | 276 | 2.2e+03 |
| 0.5 | 159 | 1.28e+03 | 1.02e+04 | 8.16e+04 |

The matched-supply cells of the spec: (N, delta) = (100, 0.05), (200, 0.025), (400, 0.0125) all have T = 0.159; (200, 0.05) and (400, 0.025) have 1.28; the probability that an island has a bid triple on one common split (Poisson approximation, 28 splits) is 0.116 / 0.537 / 0.982 / 1.000 at N = 100 / 200 / 400 / 800 (delta = 0.05). Fixed-count inoculation: B*_1 has one same-split triple per island (T = 1), B*_4 has 64, at every N.

## Manifest and run-index convention

As the spec's manifest: C and C+B* at N = 200 and 400, delta = 0.05, mN = 1 are scored on runs 20-59 (stored runs 0-19 are exploratory, reported separately, pooled only with disclosure); C+G on runs 20-59; N = 100 cells on runs 0-59 (C, C+B*, C+B stored at 60; C+G stored 0-19 plus new 20-59; C+F new 0-59); N = 800 on 10 runs. **Engineer's deviation, fixed here before any counted cell:** every other new 20-run cell at N >= 200 (C+B, C+F, C+F4, C+F-, the dose cells, mN = 0 cells, C+B*_k, and cell E) uses runs **20-39** where the spec's manifest says 0-19, so that each scored contrast (for instance C+F against C+G at N = 200 and 400, the dose cells against C+B* at delta = 0.05) has its comparator on common runs; the number of runs per cell is the spec's. At N = 100 the new 20-run cells (C+B*_k, C+F-) use runs 0-19, paired with the stored rows. Lambda = 10 only at N >= 400 (Lambda in {0, 10} at N = 100, 200); every prediction is scored at Lambda = 10. Pairing for "paired differences": same run index, same N, same mN, same Lambda.

## Predictions, with falsifiers

Scored at mN = 1, Λ = 10 unless stated; "core" is core proper at the end of the run, paired differences on shared
founders with run-level bootstrap intervals; a bound counts as met only if the point estimate meets it and the stated
sample is complete. [after second review] **Manifest:** C and C+B\* at N = 200, 400, δ = 0.05 are scored on runs 20–59
(runs 0–19 are the stored exploratory rows); C+G at N = 200, 400 on runs 20–59 for pairing with them; every other
cell is new and scored on all its runs (0–19, or 0–59 at N = 100); a prediction whose cell is cut is unscored, not
failed.

**The RS's conjecture, re-scored at larger N.** G⅓: core ≥ 0.95 of islands at mN = 1 in some arm at N = 400, and at
mN = 0 every core point has island frequency ≥ 1/76 (run-clustered simultaneous 95% intervals) in C+B\*. *The RS is
invited to state his own prediction for N = 400 (does any arm reach 0.95; does the coverage clause hold).*

**RE.**

1. **Supply, not N or dose, is the lever for bids.** N = 400: C+B\* at δ = 0.05 (T ≈ 10) has core ≥ 0.7 and ≥ 0.3 above C;
   C+B\* at δ = 0.0125 (T ≈ 0.16, the N = 100 supply) has core within 0.15 of C. N = 200, δ = 0.025 (T ≈ 0.16): within
   0.15 of C. *Falsifier:* any bound violated (a violation of the δ = 0.0125 clause is the H_N reading).
2. **Dose is non-monotone at large N.** N = 400: C+B\* at δ = 0.5 (n_σ ≈ 7; mixed-σ bidders pair at the exclusion split)
   is at least 0.15 below δ = 0.05, and its pair (kind) share is at least 0.15 above δ = 0.05's. *Falsifier:* either
   gap < 0.15.
3. **Constants coordinate better than bids at every N.** C+G ≥ C+B\* − 0.05 at N = 200 and 400 (paired), and C+G core ≥ 0.8 at
   N = 400. *Falsifier:* C+B\* exceeds C+G by more than 0.05 at either N (a reading premium), or C+G < 0.8 at N = 400.
4. **A flexible bid is a constant with a fallback.** C+F is within 0.15 of C+G at N = 100, 200 and 400 (reading plus
   feasibility adds and costs nothing in the easy case), and C+F − C+B\* ≥ 0.3 at N = 100. *Falsifier:* |C+F − C+G| > 0.15
   at any N (a reading premium or penalty), or C+F − C+B\* < 0.3 at N = 100 (equality was not the bind).
5. **Local supply is enough without migration at N = 400.** mN = 0, N = 400: core ≥ 0.5 in C+B\* and in C+G, and the
   null share ≤ 0.2 (queue 72 at N = 100: core 0.02, null 0.78–0.86). *Falsifier:* core < 0.5 in either.
6. **The RS's conjecture still fails at N = 400, on the core clause.** No arm reaches core ≥ 0.95 at mN = 1 (the best
   arm ≤ 0.9; dominated pairs and non-core bid splits remain). *Falsifier:* an arm with core ≥ 0.95 and the lower
   bootstrap bound ≥ 0.9.
7. **Entry is the bind, exit is neutral drift** [restated after second review: scored on the ε-free assays, cell F].
   On a homogeneous B\*³ or grand-constant core island, an introduced matching grand constant fixes at 1/N within 2
   standard errors at N = 100, 200, 400 (neutral), and an introduced pair offer fixes at < 0.5/N (selected against).
   Raw transition rates in the runs are reported, not scored. *Falsifier:* either assay outside its bound at any N.
8. **Fixed count isolates N** [after second review]. C+B\*ₖ (k = 4) core at N = 400 exceeds k = 4 at N = 100 by less
   than 0.15 (a fixed number of same-split copies helps equally at every N, so the gain at fixed δ is supply).
   *Falsifier:* the N = 400 cell exceeds the N = 100 cell by ≥ 0.15 (H_N).

**Reviewer counter-predictions, recorded and scored.** gemini-4-argon: (i) at mN = 1 the lever is metapopulation supply
I·T, not T: C+B\* at N = 400, δ = 0.0125 reaches core ≥ 0.50 and exceeds C by > 0.15 (against RE 1; the mN = 0 cell at
the same dose separates the two: under argon, mN = 0 stays low while mN = 1 is high); (ii) C+F with matched marginals
has an efficient-dominated share > 0.15 (F stabilizes the 9 non-core splits), scored against C+F₄. gpt-6.1-sol:
(iii) raw per-generation exit rates will not follow 1/N (scored by the reported rates against the assays); (iv) C+F
differs from C+G mainly through a pair excess in infeasible encounters, not a reading premium (scored by C+F's pair
share against C+G's and C+F⁻'s); (v) metapopulation rescue depends on lineage survival and assembly, not total
compatible-triple count (scored by establishment conditional on the founding-support statistics).

## Engineer's operationalizations (fixed before the counted cells; the spec leaves these without a number)

**RE 7 scoring rule.** Cell F, 2,000 replicates per case and N in {100, 200, 400}, and the exact two-type value. Neutral cells: the introduced matching grand constant on B*^3 (3 slots x 3 N = 9 cells) must have a Monte-Carlo count within 2 standard errors of 2,000/N (binomial standard deviation under p = 1/N); the pair-offer and B*(sigma') entrants (2 + 1 per slot, both islands) must have N p < 0.5 by both the Monte-Carlo estimate and the exact value. On G^3 the "matching grand constant" is the resident program itself (identity: p = 1/N exactly) and I add the reading entrant B*(equal split); these 18 cells are reported, and an isolated |z| in (2, 3) among them is noted without failing (18 neutral cells, one at 5% is expected; the exact value is 1/N). Any |z| > 3, or a B*^3 cell outside 2 SE, or a selected entrant with N p >= 0.5, fails the prediction.

**RS conjecture clause list.** "Some arm at N = 400" = every N = 400, mN = 1, Lambda = 10 cell: C, C+B*, C+B, C+G, C+F at delta = 0.05; C+B* at delta = 0.0125, 0.15, 0.5; C+B*_1, C+B*_4. Coverage clause at mN = 0, N = 400, C+B*, Lambda = 10, 20 runs: held iff no core point has a run-clustered simultaneous (Bonferroni over 19) 95% upper bound below 1/76. RE 6 uses the same list of arms; "the lower bootstrap bound >= 0.9" is the 2.5% bound of the run-level mean.

**gemini-4-argon (i)** (N = 400, C+B*, delta = 0.0125, Lambda = 10, runs 20-39): held iff core(mN = 1) >= 0.50, core(mN = 1) - C > 0.15 (paired), and core(mN = 0) <= core(mN = 1) - 0.30 ("mN = 0 stays low while mN = 1 is high"). **(ii)** C+F (delta = 0.05, mN = 1) end share of the efficient-dominated class > 0.15 at N = 200 (C+F4 reported beside it; also N = 100 and 400); held iff C+F at N = 200 exceeds 0.15.

**gpt-6.1-sol (iii)** raw core-exit hazard per island-generation in the tail (mN = 1, Lambda = 10; the transition statistics exist only for the new cells, so the arms are C+G and C+B* on runs 20-59 at N = 200 and 400, and C+G, C+F on N = 100 runs 20-59; pooled exits over pooled in-core exposure, per arm): held iff the log-log slope of hazard against N (N = 100, 200, 400 where available for the arm; C+B* has no new N = 100 cell, so its slope is over N = 200, 400) has a 95% run-level bootstrap interval that excludes -1. **(iv)** C+F against C+G (N = 100 and 200, Lambda = 10, mN = 1): held iff pair-kind share(C+F) - pair-kind share(C+G) >= 0.05, |core(C+F) - core(C+G)| <= 0.15, and pair-kind share(C+F) - pair-kind share(C+F-) >= 0.05 (N = 100 and 200). **(v)** At mN = 0, N = 200 and 400, C+B* delta = 0.05, islands with a named-only efficient founding support: held iff the minimum abundance of that support predicts establishment (first generation a grand state is held 25 generations) at least as well as the count of compatible triples (ROC area, pooled islands with support); and, at mN = 1, N = 400, delta = 0.0125, establishment of islands without a local named support is at least half of that with one (migration rescues lineages rather than counts).

## Engineer's own predictions

**E1. The founding supply is as counted.** The share of islands with a named-only efficient founding support (all three programs bids on one split) in C+B* at delta = 0.05 is within 0.05 of 0.116 / 0.537 / 0.982 at N = 100 / 200 / 400 (pooled over the runs of each cell; binomial standard error 0.01). *Falsifier:* any difference > 0.05. (A check of the supply bookkeeping the hypotheses use, not a test of them.)

**E2. The pair fallback does not change the core share.** |core(C+F) - core(C+F-)| < 0.10 at N = 100 and N = 200, mN = 1, Lambda = 10 (paired, 20 runs; C+F on the same runs). *Falsifier:* either difference >= 0.10.

**E3. Constants carry the easy case once supply exists.** C+G core >= 0.5 at N = 200 (Lambda = 10, mN = 1, paired runs 20-59); this is a weaker version of RE 3 and fails only if the grand constants do not coordinate at N = 200. *Falsifier:* C+G core < 0.5 at N = 200.

## RS's prediction

none supplied before launch (the file `predictions/RS-prediction-queue73.txt` did not exist in the main checkout when the counted cells were launched; this line was edited after launch, at the coordinator's instruction, and carries no prediction)

