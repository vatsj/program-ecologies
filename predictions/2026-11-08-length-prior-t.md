# Predictions: from arm T to a length prior (queue 75), 2026-11-08

Spec: `specs/2026-11-08-length-prior-t.md` (reviewed by gemini-4-argon and gpt-6.1-sol, folded). Committed before any
counted cell of step 2 and before step 1's final enumerations and Monte Carlo. Verdicts are written into
`runs/length-prior-t.md` and `runs/lt-prior.md` against the rules below.

## Pilot runs made before this file (disclosure)

Dynamics (step 2): validations V1 and V2 only. V1 reran the stored queue-74 cell (arm T, Lambda = 100, mN = 1) through the
new T+ code at the stored law, runs 0-39 at N = 100 (all identical to the stored rows; 40 of 40) and N = 200 (still running when this
file was committed; 21 of 21 done so far identical; final record in `runs/length_prior_t/v1_n*.json`); V2 is the table check. Timing: one cell of the new law `2a:d=0.03:b=0`, N = 200, I = 64,
run 0 (27 s; V\* share 1.0 at 120N, fair pair F1); no other new-law cell was run, no threshold quantity looked at.

Static (step 1), all before this file and none of them a final number:
- a first exhaustive enumeration of machine R0 to size 4 (before the taint rule was repaired; the mass table of sizes 1-4 was read:
  at size 1 the mass splits 0.117 junk (forfeit) to 0.049 constants (the nine codes), later sizes are almost all junk, and no
  partner-dependent program of size <= 4 exists in R0);
- one run of the targeted search for machine R1 (`lt_prior_search.py`, grammar of depth-one decision trees over a read). I
  read its class table: in R1 the shortest fair single-partner reader is the 6-node `(if (eq readn 4) 1 4)` (exact member Snon)
  with prior mass 3.8e-12 per spelling, the Trojan bully `(if (eq readn 3) 2 4)` has the same size and mass, and the summed
  reader masses of the grammar are of order 10^-11 against a constant mass of order 0.05-0.1. This pilot makes RE 5 and the
  R1 half of RE 6 unlikely to survive; they stay registered as written and are scored on the final numbers;
- a timing run of the R0 / R1 enumeration to size 4, and the R0 enumeration to size 5.

Unit tests (the Elias-gamma check range and a convergence tolerance of the size-mass sum were test artefacts) were run before.

## The spec's predictions, verbatim

- **RE 1 (the threshold is a copy count in N).** At I = 64, beta = 0, delta\* falls with N by a factor >= 1.5 per doubling
  (N = 100 -> 200 -> 400). Falsifier: a factor < 1.2 per doubling at both steps.
- **RE 2 (and in I).** At beta = 0, delta\*(N, 256) <= delta\*(N, 64) / 2 at N = 100 and 200. Falsifier: ratio > 0.8 at both.
- **RE 3 (bullies raise the threshold).** At N = 200, I = 64, delta\*(beta = 1) >= 3 * delta\*(beta = 0). Falsifier: < 1.5x.
- **RE 4 (R0 is far below).** Under R0, rho_R <= 10^-8 (readers are >= 14 nodes longer than constants at about 1/18 per
  node), and beta >= 0.3 (bullies are the same size as fair readers). Falsifier: rho_R > 10^-6 or beta < 0.1.
- **RE 5 (R1 brackets it).** Under R1, rho_R >= 10^-3. Falsifier: < 10^-4.
- **RE 6 (join).** Under R0 no tested (N, I) reaches delta\*; under R1 some tested cell does at beta = the measured R1 bully
  ratio. Falsifier: the reverse in either machine.
- **gemini-4-argon's counter (recorded, scored):** beta < 0.05 under both R0 and R1 (a bully needs an extra comparison and
  two distinct branches, 3-5 more nodes than a fair reader).
- **gpt-6.1-sol's counters (recorded, scored):** RE 1-2's thresholds do not collapse onto one copy count across N and I
  (scored: the matched-count cells' V\* spread exceeds 0.2 at c = 64 or 640), and the improvement with I is weaker than RE 2
  asserts (ratio > 0.5); RE 4's 10^-8 bound stays unsupported (scored: only a lower bound on rho_R is obtained, above
  10^-8 or not certified below it).
- **RE 7 (junk).** Under R0, junk (forfeits and default code 8) carries more than half of the prior's mass. Falsifier:
  < 0.25.

## Scoring rules fixed here (the spec leaves them open)

- "V\* share" is the mean over the 64 (or 256) islands of the indicator that the island's modal outcome at 120N is a fair
  pair (`vshare_ts[120]`), averaged over the 20 runs of a cell, with the bootstrap-over-runs interval; delta\* uses the
  mean. "Tested (N, I)" is the grid of series 2b (N in {200, 400}, I = 64) for the join of RE 6 and of the junk/join
  verdicts, extended by I = 256 only where series 2b was run there; rho_R and beta are those of the exact-member classes
  (family-level classes are reported beside them).
- Step-1 class masses are reported **conditional on a finite tree** (the semimeasure's mass of finite trees is q = 0.4748 in
  R0, 2/3 in R1; raw masses are reported beside them). rho_R = (single + two-partner fair reader mass) / (constant mass,
  the nine codes), beta = bully mass / (fair reader mass). Where only the targeted search reaches a class, the figure is a
  lower bound and the verdict that depends on a bound in the wrong direction is "not certified".
- RE 4's "rho_R <= 10^-8" is scored on the central statement (an **estimate** at or below the bound); a one-sided lower
  bound above 10^-8 falsifies it, a lower bound below 10^-8 leaves it "not certified" (sol's counter then scores). "beta >= 0.3
  and falsifier beta < 0.1" are scored on the lower-bound ratio from spellings of the same size.
- A delta\* bracket is "reached" when the smallest grid point has mean V\* >= 0.9; "beyond the grid" when no tested delta
  reaches it (reported as > 0.2); "below the grid" when the smallest grid delta (1e-4) already reaches it.
- Ratios RE 1-3 are computed from interpolated delta\* where V\* is monotone across the bracket; otherwise from the bracket
  edges, and when two edges are both brackets, the verdict is "not decided" if the interval of the ratio straddles the
  claim.

## The engineer's predictions (mine; with falsifiers)

- **E1 (shortest R0 reader).** The shortest exact-member reader in R0 has 12 nodes
  (`(if (eq (capk K (run K' n p) me) 4) 1 4)`); the shortest of the family-level fair readers (the reader whose read is the
  uncapped `app`) 11. Falsifier: an exact member found at <= 11 nodes by any search of step 1.
- **E2 (the junk share).** Conditional on a finite tree, junk (forfeit class plus failed-read class) carries more than 0.9 of
  the prior in R0 and more than 0.8 in R1. Falsifier: below 0.8 in R0 or below 0.7 in R1.
- **E3 (threshold level).** delta\*(N = 200, I = 64, beta = 0) lies in [3e-3, 3e-2] (bracket within those). Falsifier: bracket
  outside [1e-3, 1e-1].
- **E4 (a reader-free world is T0).** At delta = 1e-4 (about 1.3 founder copies per world at N = 200, I = 64) the V\* share
  is within 0.15 of the T0 value of queue 74 (0.73 at N = 200, 0.26 at N = 400). Falsifier: farther at either N.
- **E5 (copy counts collapse at the high count).** Over the five (N, I) of the matched-count cells at c = 640 the V\* means
  have spread <= 0.2 and all exceed 0.8. Falsifier: spread > 0.2 or any mean <= 0.8. (This is the opposite of sol's counter at
  c = 640; the c = 64 side is left to sol's counter, scored separately.)
- **E6 (bullies are monotone).** At N = 200, I = 64: delta\*(beta = 0) <= delta\*(beta = 1) <= delta\*(beta = 3), each
  strictly larger at beta = 3 than at 0, when beta = 3 reaches V\* >= 0.9 anywhere on the grid. Falsifier: any decrease
  beyond one grid step.
- **E7 (the join).** For both machines delta_LP is below the smallest grid delta (1e-4), so the join reports no tested (N, I)
  and an extrapolation by the fitted c\* law, labelled as such. Falsifier: either machine's delta_LP >= 1e-4.
- **E8 (a bully is as cheap as a reader).** In both machines the lower-bound beta from spellings of equal size is between 0.3
  and 3 (a bully is a reader with a different pair of codes; sol and argon's size arguments are about the Trojan *and*
  an extra comparison, which the library bully does not need). Falsifier: below 0.1 or above 10.
