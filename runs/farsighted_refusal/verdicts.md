## Verdicts (written by hand after the cells; scoring notes as fixed in the predictions file)

**Deviations, disclosed before the cells they affect** (notes §1.9): the certification search was changed (core
decomposition, probing, fail-first branching, split on the member-exit bits with a node cap of 10⁵ per subtree); the
list of fixed points is certified complete at δ ∈ {0.5, 0.8, 0.9} and **not** at 0.95 (2 of 16 subtrees capped) or 0.99
(12 of 16 capped), where it is the union of the uncapped subtrees, the exhaustive S₃- and Z₃-invariant enumerations and
1,500 restarts, every member verified exactly. Forced starts ran at mN = 0 only. The N panel ran at both mN.
M-gKR-unequal uses the δ = 0.99 fixed point whose absorbing set is both rotating unequal triads (not a held-player
pair: none exists in the list). U-g1-x ran because its freezing set differs from g1's (at (0, 0, 0)).

| # | prediction | outcome |
|---|---|---|
| RE 1 | U-g1 freezes islands at their first pair outcome; occupancy within 0.05 of 0.281 + converted disagreement (reference 0.292); far below gV | **failed in its occupancy clause** (0.188 [0.174, 0.203]: 2,114 installations, median generation 8, all out of disagreement-modal scramble islands, 0.16 of them into V\*, so the scramble's 0.28 is replaced by the uniform feasible draw's 1/6); freezing and "far below gV" held; falsifier (≥ 0.6) not fired |
| RE 2 | a V\*-absorbing KR fixed point at δ ≥ 0.9; others absorb on held-player unequal pairs | **first clause held** (certified at 0.9, found and verified at 0.95 and 0.99; it exists already at 0.8); **second failed in kind**: no fixed point absorbs on a held-player pair (certified absent at δ ≤ 0.9, not found at 0.95 / 0.99); the unequal-absorbing fixed points (0.95, 0.99) absorb on a *rotating triad* (4,2,0) → (0,4,2) → (2,0,4); falsifier not fired |
| RE 3 | the default at δ = 0.9 is not the V\* one; U-gKR(0.9) between D1 and gV | **first clause held** (default = the walk on fair and unequal pairs, 84 of 90 accepted, V\* mass 1/3); **second failed**: U-gKR(0.9) = D1 (0.333 vs 0.338 at mN = 0; 0.082 vs 0.091 at mN = 1) |
| RE 4 | where the static fixed point absorbs on V\*, the universal guard recovers the set (≥ 0.9 at mN = 0; modal ≥ 0.9 at mN = 1) | **held** (δ = 0.99: 1.000 at mN = 0; modal 1.000 at mN = 1, classifier 0.63 at 2,000 and 0.93 at 10,000) |
| RE 5 | gKR neutral at mN = 0, rises in ≥ 0.8 of runs at mN = 1 | **held** (0.000 [−0.009, 0.010]; rises 37/40 by 2,000, 40/40 by 10,000, 0.50 → 0.77 → 0.89) |
| RE 6 | C3: both refusers rise, neither wins outright by 2,000; g0 lost | **held as scored** (g0 below ⅓ in 38/40; a refuser above 0.9 in 1/40) but only gKR rises: gKR 0.55, gV 0.32 (−0.011) at 2,000; 0.72 vs 0.24 at 10,000 |
| RE 7 (revised) | C3-read: gKR-read rises against gKR | **falsifier fired**: the reader ends below gKR in 24/40 runs (0.43 vs 0.50); it rises against g0 (+0.095) |
| Gemini (counter, M-read) | the two drift neutrally | **held** (−0.002 [−0.047, 0.045], 20 rise / 20 fall) |
| RE 8 | a gKR-read decision costs ≤ 10⁵ evaluator steps | **failed** (2.4–2.6·10⁵ on every composition); falsifier (> 10⁶) not fired; deriving the table as code costs 0.7·10⁶ (δ = 0.9) to 1.8·10⁷ (0.95) |
| S1 | g1 freezes all but (0, 0, 0); g1-x freezes all | held |
| S2 | U-g1 at mN = 0 below baseline, 0.15–0.29 | held (0.188) |
| S3 | U-g1 at mN = 1 in 0.55–0.80 | **falsifier fired** (0.395 at 2,000; 0.425 at 10,000, bimodal: consensus on one member or one unequal pair) |
| S4 | U-g1-x = baseline in distribution | held (0.280) |
| S5 | V\*-absorbing at 0.9–0.99, none at 0.5 and 0.8 | **failed** (exists at 0.8; the buyer values the exit at 2.94 < 3) |
| S6 | δ = 0.5: unique, myopic | held |
| S7 | the default at δ = 0.99 absorbs exactly on V\* | held |
| S8 | ≥ 2 orbits at 0.9, 0.95, 0.99 | held (3 certified; ≥ 2; ≥ 3) |
| S9 | no ties, default margin ≥ 10⁻⁴ at 0.99 | held at the defaults (0.051); a non-default orbit at 0.9 has a tie |
| S10 | U-gKR(0.99) ≈ R2 | held on its thresholds; the cells differ in kind at mN = 1 (gKR: consensus on one member 0.85, coverage 0; R2: three members, coverage 1.00) |
| S11 | U-gKR-read = U-gKR draw for draw | held (40/40 at both mN) |
| S12 | M-gKR mirrors R1-public | held |
| S13 | M-g1: g1 rises in ≤ 0.6 of runs, gain below gKR's | **first clause failed** (32/40), second held (+0.146 vs +0.273); falsifier not fired |
| S14 | C3: g0 below ⅓ in ≥ 0.8; gV ≈ gKR | **falsifier fired** (gKR ahead by 0.23 at 2,000, in 31/40 runs) |
| S15 | C3-read: reader below gKR in more than half the runs | held (24/40) |
| S16 | rare invasion rises in ≥ 0.7 of runs | **failed narrowly** (27/40; 0.049 → 0.093); falsifier (< 0.5) not fired |
| S17 | forced starts: persistence 1.0, recovery ≥ 0.95 | held (1.000 / 1.000) |
| S18 | N panel ≥ 0.95 at mN = 0 | held (0.998, 1.000) |
| S19 | solve 0.5–3·10⁵; reader ≤ 3·10⁵; derivation ≥ 10⁶ | two clauses held; **derivation clause failed at δ = 0.9** (6.7·10⁵); falsifier not fired |
