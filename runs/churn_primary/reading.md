
## Scored verdicts (rules of `predictions/2026-10-25-churn-primary.md`)

| prediction | verdict | numbers |
|---|---|---|
| gate (B6w = stored `M-base`) | **passed** | 40/40 runs identical at each mN (coverage, consensus, class counts, inefficiency) |
| P1, arm E (modal and weak, n = 10) | **held** | ratio to B6w 1.21 / 0.93 / 1.17 (modal) and 1.03 / 0.93 / 0.49 (weak) at mN = 0.01 / 0.1 / 1; coverage at mN = 1 is 0.00 |
| P1 control, E-min (n ≤ 6 plus explicit readers) | **fails the "no churn" rule** | ratios 2.8-16.9 (modal), 3.6-13.3 (weak); coverage at mN = 1 is 0.00 in every dose, so partial, not failed |
| P2, T-lo and T-main (c = 0) | **partial** | ratio 9.7 / 5.9 / 4.0 (lo) and 11.0 / 5.9 / 4.6 (main) at mN = 0.01 / 0.1 / 1 (intervals at mN = 1: [2.2, 10.1], [2.4, 11.6]); hazard 3-6× baseline; coverage at mN = 1 is 0.00 |
| P2 counter-prediction, gemini-4-argon (two-partner weight ≥ 0.05 makes T churn) | **failed as stated** | R(T-hi) 7.0 / 4.3 against R(T-lo) 5.9 / 4.0 at mN = 0.1 / 1: not twice; churn is already there at two-partner weight 0.003 (carried by the single-partner switchers) |
| P2 counter-prediction, gpt-6.1-sol (redirection common, island flips rare) | **held in the DSL cells, not in T** | encounter redirection at injection reaches 0.21 (modal) and 0.47 (weak) at a 50% immigrant fraction with switching 0.02 and 0.00; in T redirection peaks at 0.13 |
| P3 (excluded slot's fair offer; pooled single immigrants into slot 1, readers resident) | **held** | 0 of 6,800 (DSL modal), 0 of 6,800 (DSL weak), 0 of 10,800 (T) switches; over all slots 0.1% (T 0.07%); sham 0 of 300 in every configuration |
| P4 (coverage founders'; high at mN = 0 and 0.01, falls with mN) | **held** | coverage 1.00 / 1.00 / 0.55 / 0.00 (E modal), 1.00 / 1.00 / 0.45 / 0.00 (E weak), 1.00 / 1.00 / 0.50 / 0.00 (T-main); gpt-6.1-sol counter (no monotonicity): not seen |
| c₀ sensitivity (T-main, T-hi) | descriptive | flips 10.6 / 5.6 / 3.2× (main) at mN = 0.01 / 0.1 / 1: price lowers the flip rate slightly, does not remove it |
| E1 (arm E within 0.7-1.5×, coverage ≤ 0.05) | partial | E modal inside the band at all three mN; E weak at mN = 1 is 0.49 (interval [0.2, 1.4]) |
| E2 (E-min lo 0.7-1.5×, main 1-3×, hi 1.5-5×) | **failed** | 3.2-7.8, 3.7-9.6, 2.8-16.9 |
| E3 (T lo 1-2×, main 1-3×, hi 2-6×; c₀ does not raise flips) | **failed** (c₀ clause held) | 4.0-9.7, 4.6-11.0, 4.3-21.0 |
| E4 (probe: constants < 5%; readers 5-15% at 1%; sham < 1%; naming-preserving < 3%) | partial | constants 0.1%; readers 0.0-0.8% (far below 5-15%); sham 0%; naming-preserving 0% |
| E5 (no arm shows a 20-60× excess; largest expected 2-6×) | **failed** | T-hi at mN = 0.01 is 21× (interval [15, 31]); at mN = 0.1 / 1 it is 7.0 / 4.3 |
| E6 (gate) | held | |
| E7 (is there ≥ 10× in T-hi, E-min hi or the reader probe?) | answered | yes at mN = 0.01 in T-main, T-hi, E-min hi (11-21×), through reader-dominated islands (route share 0.83-0.92) |
| E8 (balanced start: readers within 0.5-3× of constants; coverage at mN = 0.1 at most 0.2 above) | partial | flip ratios 0.96-2.2 (held); coverage at mN = 0.1: E-min weak switch 0.70 against 0.35, T two 0.65 against 0.25, E-min modal 0.00 against 0.35 (mixed in sign) |
| ablation expectation (post hoc, addendum 2) | held | S alone 4.2× and D alone 3.6× at mN = 0.1 (S carries 86% and D 69% of the main dose's excess); Z alone 1.3-1.4× |

## Reading

- **Arm E at n = 10 does not churn**, in either evaluator: the churn-capable classes are about 0.1% of a slot and the two-partner
  reader does not exist in the grammar. This is the stored contract-free result reproduced.
- **Churn does appear in the primary object once flexible readers carry about 9% of the seed, in both the DSL (E-min) and the
  Turing-complete arm (T)**, and it is reader-mediated (83-92% of the flips occur on islands whose dominant class in some slot is
  a reader, 1-9% in the baseline and 9-27% in arm E). Hazard of member-to-member change per fair-pair island-generation is 3-6× the
  baseline's at the library priors (T-main 6.5×, 3.4×, 3.4× at mN = 0.01, 0.1, 1); the flip counts per run are 4-11× (21× at T-hi).
  This is smaller than the veto's 20-59× (134 / 1,167 / 4,375 flips per run) and the excess shrinks with migration.
- **Coverage does not appear.** At mN = 1 every cell is in consensus or a single pair (coverage 0.00 in every lottery cell), and at
  mN = 0.1 coverage is at or below the baseline's 0.62 (0.35-0.70). Where the veto held all three pairs present, the primary
  object's churn rotates islands among pairs but does not keep the three pairs alive against consolidation.
- **The route is neutral re-pairing, not encounter redirection**: single and fractional immigrants almost never switch an island
  (0.1% pooled; 13.8% / 10.8% / 27.8% only at a 90% immigrant fraction in the homogeneous cells, with no 0.5 threshold below 1);
  the ablations put the excess on readers that have somewhere to go (switchers S and two-partner D), none on null-fallback
  readers Z; flips are persistent (median dwell 650-890 generations after a flip, 21% return to the previous pair within 300
  generations, the same in the baseline). Readers whose fallback names the third slot are payoff-neutral bridges between fair
  pairs, which is how the stored chicken result found conditional straights.
- *Caveats:* finite N and I, ε = 0, 10,000 generations, 40 runs (20 in the balanced start); T and E-min priors are library priors
  chosen by me with 9% flexible mass; no tape, no certificates or proofs in T; hazards are per fair-pair island-generation;
  intervals at mN = 1 are wide (consolidation within a few thousand generations); the 8-run dwell-time diagnostic is scratch
  (`mN = 0.1`, B6w, E-min main modal, T-main) and is not in the cell files.
