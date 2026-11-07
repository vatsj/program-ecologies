# REJECTED entries (draft for the RE), queue 74 (RESULTS "Majority division in the current object")

One entry per failed prediction; numbers are finite-schedule (I = 64, g ≤ 120N, N ≤ 400) and from `runs/majority-current-object.md`.

- **The RS's recorded prediction, for arm T ("majority division does not land in V\* under the current operating hypotheses").** Failed for T,
  held for M and L. T lands (V\* ≥ 0.95, lower bound ≥ 0.90) in every mN = 1 cell with Λ ∈ {0, 10, 100} at N = 100, 200 and 400 (1.000, 1.000, 0.999
  [0.998, 1.000] at Λ = 100) and at 0.91–1.00 at mN = 0.1, with no unequal consensus run. It does not hold for the DSL arms (M 0.80 / 0.48 / 0.45,
  L 0.85 / 0.58 at N = 100 / 200 / 400 and Λ = 100). The target is met in the current object only with the library prior (readers at 10% of seed
  mass, no bully family, A_f charge), not under the length prior; T0 (its constants only) falls with N like M (0.83 → 0.26 at N = 100 → 400).
  New evidence relative to the recorded prediction: finite N and I with the annealed tail rather than "no claim about the limit".
- **RE 6 (no arm reaches V\* ≥ 0.6 without migration at Λ ≤ 100).** Failed for arm T: T's V\* at mN = 0 is 0.71 at N = 200 and 0.86 at N = 400 (the tail
  adds at most 0.05). M (≤ 0.53) and L (≤ 0.40) hold. The wasteful and disagreement islands that I expected to persist in isolation shrink with N
  (T's wasteful share 0.15 / 0.045 / 0.006 at N = 100 / 200 / 400) because the islands settle on pairs at larger N, not because of the tail.
- **RE 5 (the tail lowers the wasteful share without migration by ≥ 0.10 in both arms), partial.** The reductions are 0.056 [0.045, 0.067] (M) and
  0.052 [0.041, 0.062] (T) at N = 100: the tail does clean waste (the falsifier, < 0.05, is not met) but by about half the predicted amount, and the
  effect vanishes with N (0.00 at N = 400 in M). The mechanism "a slot raising its demand, which arrivals supply" operates, but arrivals per
  individual fall like 1/N at fixed Λ.
- **RE 4 (M, mN = 1: the prior's tail does not raise V\* by more than +0.05), partial.** The points are +0.10, −0.15, +0.09 (N = 100, 200, 400)
  with intervals including 0 and ±0.25 wide, so neither the stated bound nor the falsifier is decided; the prediction as written is not supported
  by the data at N = 100 and 400 and not refuted.
- **RE 8 (D1, the clean tail, raises M's V\* at N = 100, mN = 1 by ≥ 0.15), partial.** +0.075 [−0.025, 0.175]. RE 8b at N = 200 holds (+0.275 [0.10, 0.45]).
- **gemini-4-argon's counter (RE 8 fails at N = 100 and also at N = 200).** Failed at N = 200 (gain 0.275). Its timing mechanism (most arrivals late)
  was refuted analytically before the run (3% of delivered arrivals come after 15N; 0.032 measured).
- **gpt-6.1-sol (i) (RE 8b fails: the gain falls with N and is < 0.05 at N = 200).** Failed: the gain rises from +0.075 to +0.275.
- **E6 (the engineer's: the tail raises M's V\* at N = 100, mN = 1 by > 0.10 with an interval excluding 0).** Failed: +0.100 [−0.051, 0.275]. The
  tail-free cell is already at queue 64's 0.70 and the tail cell at 0.80 with run-to-run spread (28 and 32 of 40 runs all-fair).
- **A reading to drop: "the clean tail is the remedy for M".** D1 (clean tail) gains +0.075 / +0.275; D3 (clean founders, full tail) +0.175 / +0.50; D2
  +0.20 / +0.475 (N = 100 / 200). The lever is the founding composition; the tail composition adds nothing once the founders are clean
  (D2 − D3 = −0.025). Diagnostics only; the clean tail stays out of the object (RS 2026-11-02).
- **A reading to drop: "D4 (matched-mass random removal) controls for removing mass".** At 0.217 per slot the matched mass is two of the nine constants (0.1084
  each), so D4 removes two random constants, a ½ constant in 4 of the 9 slot draws (V\* falls to 0.22 at N = 200 against 0.475). It controls for
  renormalization and for losing two constants, not for "mass".
