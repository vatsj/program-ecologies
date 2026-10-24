# Predictions: the inspection game's enforcer and its shadow, 2026-10-24

Spec `specs/2026-10-24-inspection-shadow.md` (reviewed by gemini-4-argon, then gpt-6.1-sol in amended mode; both folded).
Hand derivations: `notes/inspection-shadow.md` §1 (committed before any code). Written and committed before any code of
this run exists and before any counted cell. Chain numbers are ε→0 chain quantities (π over pairs of monomorphic role
classes, whole state space), lottery numbers are ε = 0 seed-lottery statistics at finite (N, I, horizon) (with the
declared rain where a remedy has one), never π. Scoring is held / partial / failed / not scored, each with the number, in
`runs/inspection-shadow.md` and `.json`.

## The RS's statement

"worth the confirmation" (the RS, 2026-10-24): the RE's reading of the finished two-role run (the efficient island is
held by a responsive inspector and the whole-space chain loses it to the enforcer's unconditional shadow, as in the PD)
is to be confirmed or refuted, with its remedies.

## Definitions fixed here (engineer, before any code), so no threshold can move afterwards

* **E** (payoff-efficient): a class pair with both mean game payoffs ≥ −0.05 (gross of the compute price, as in
  `isl_efficient` of the previous run). **R ⊂ E:** those E states whose inspector class deters the constant cheater,
  P(inspect | K) > 1/4. **E\*:** E states with forfeit mass < 0.05 for both roles and inspection and cheating
  probabilities both < 0.05 (the forfeit-artefact-free version). Forfeit mass and action frequencies are reported beside
  every E number.
* **Rates** are per mutation event: q(s → t) = (μ_role(mutant class)/2) · ρ_N(Δ), ρ_N the Moran fixation probability
  under fitness exp(0.3 Δ) with ρ_N(0) = 1/N. **Fates:** neutral (|Δ| ≤ 10⁻⁹ in net payoff), strict (Δ > 10⁻⁹),
  deleterious. **Conditional exit hazard** from a set X: h_X = Σ_{s∈X} π_s Σ_{t∉X} q(s,t) / π(X). **Stationary flux** is
  Σ π_s q(s,t) over the same moves. Both are reported, separately, with the per-mutant fixation probabilities and the
  prior-weighted transition rates.
* **Exit categories** (for the decomposition of h_R and h_E): by mutant role and class and fate: (A) neutral drift of an
  inspector class that does not deter K (`N` and twins: P(inspect | K) ≤ 1/4); (B) other neutral moves; (C) strict
  invasion by the constant cheater `K`; (D) strict invasion by another non-reading inspectee (light cheaters, `X`,
  mixers); (E) strict invasion by a reading inspectee (the possible fakers through mutual-reading forfeits); (F) strict
  invasion by an inspector; (G) deleterious. "The largest exit" is the largest category by h at that N.
* **Slopes** are least-squares slopes of log h (or log odds) on log N over the stated N values (three points for
  10³–10⁵). Odds = π(E)/(1 − π(E)).
* **Scoring of a clause that must hold over a range of N:** held if no falsifier fires at any N in the range; partial
  if it fires at exactly one N of a range of three; failed if it fires at two or more, or on the slope.
* **Effect-size predictions** (4, 5, 6): *held* at or above the threshold, *partial* for a positive effect below it,
  *failed* at or below zero; the point estimate decides, run-clustered 95% intervals (4,000 bootstrap resamples of runs)
  are reported beside it. Effects are paired contrasts (same runs, founders and dynamics seeds).
* **Lottery statistic:** efficient islands = share of islands with both mean game payoffs ≥ −0.05 at the verdict
  generation, averaged over islands then over runs; at the horizon 20N (2,000 / 8,000 / 16,000), with the
  generation-2,000 snapshot beside it. Cells use the paired founders of the two-role run (common random numbers by size
  and quantile).
* **Cuts** follow the spec's cut order and are disclosed.

## The RE's predictions (verbatim from the spec, with falsifiers)

1. *Mechanism* [restated after second review]. In the chain at N ≥ 10³ at c = 0, the largest conditional exit from R
   is neutral drift of `N` (or another never-inspecting class), with hazard slope in N between −1.2 and −0.8, and the
   largest exit from E is strict invasion of `K` into (`N`, `C`)-type states [the largest exit from R is a strict
   invasion, the drift hazard's slope is outside the range, or the largest exit from E is not a cheater's invasion].
   *Scoring:* N in {10³, 10⁴, 10⁵}, category (A) against the rest for R; for E, the largest category is an inspectee
   strict invasion (C, D or E) from an E state whose inspector does not deter K; the slope is that of the category-(A)
   hazard from R over 10³–10⁵. Range rule above.
2. *Scaling* [finite-range claim only, after second review]. The odds slope of P(E) over N = 10³–10⁵ is below 0.5
   [above 0.5]. No asymptotic claim is registered: odds growing at any positive slope still go to 1, and the limit is
   set by how the return times scale. *Counter-prediction (gpt-6.1-sol), registered:* P(E) rises with N if escapes
   scale as 1/N and return times stay bounded. *Counter-prediction (gemini-4-argon), registered:* a 1/N shadow exit with
   O(1) return makes P(efficient) grow with N; if the slope is low it will be because returns bypass the efficient
   state into committed or mixing states. *Scoring:* held iff slope < 0.5; failed iff slope ≥ 0.5 (no partial). The
   counter-predictions are scored held iff P(E) rises at every consecutive pair of N in {10³, 10⁴, 10⁵} (gemini's
   additionally records, if the slope is low, the share of excursion time spent in committed and mixing states).
3. *Lottery path.* Efficient islands fall with N along the lottery path: below 0.5 at (800, 8) at c = 0 [at or above
   0.65]. *Counter-prediction (gemini-4-argon), registered:* larger N lengthens the founding scramble, so founding
   cheaters purge `N` more thoroughly and later neutral fixation of `N` is slower; efficient islands stay at or above
   0.5, or rise. *Scoring:* the statistic at the horizon 16,000; held iff < 0.5 (and below the (100, 64) value at its
   horizon); partial in [0.5, 0.65); failed at or above 0.65. The counter-prediction is held iff ≥ 0.5.
4. *Cheater fringe.* K rain raises efficient islands against the matched C rain by at least 0.1 at (400, 16) [no
   increase, or a decrease]. *Scoring:* paired difference of efficient-island shares at the horizon 8,000, c = 0.
5. *Prudent inspectees.* ×10 reading-inspectee mass raises chain P(efficient) at N = 10⁴ by at least 0.1 against the
   matched C control [no increase]. *Scoring:* difference of π(E), boosted (§1.4, the eight classes, ×10, Δ = 9 m(S))
   minus the C control (same Δ), whole-space chain, c = 0.
6. *Price.* At c = 0.01 the reading inspectee pays to read while `C` complies free, so prudent inspectees help less at
   c = 0.01 than at c = 0 [they help as much or more]. *Scoring:* the effect of Prediction 5 at c = 0.01 against the
   effect at c = 0; held iff the c = 0 effect is positive and the c = 0.01 effect is smaller; failed iff the c = 0.01
   effect is at least the c = 0 effect; not scored if the c = 0 effect is not positive.

## The engineer's added expectations (from the one-state calculations of notes §1.2; not part of the RE's list)

* **E1 (crossover).** The strict exit from R by light cheaters and exploit readers is N-independent (7.4·10⁻⁵ per event
  at the state (CRI, C)), the neutral drift of `N` is ∝ 1/N (0.1546/N), so the largest category of h_R changes from (A)
  to a strict category between N = 10³ and N = 10⁴. [Falsifier: category (A) is largest at N = 10⁴ and 10⁵, or (A) is
  not largest at 10³.] If E1 holds, Prediction 1 fails by its own range rule.
* **E2 (sign of the scaling).** The odds slope of π(E) over 10³–10⁵ at c = 0 is negative. [Falsifier: slope ≥ 0.]
* **E3 (where the mass sits).** At N = 10⁴ and 10⁵ more π sits on non-E states whose inspectee cheats with probability in
  (0, 1/4] against an inspector that does not inspect it (the tolerated light cheater) than on states whose inspector
  is a non-deterring class facing a cheater of probability > 1/2 (the shadow excursion). [Falsifier: the shadow
  excursion holds more.]
* **E4 (price).** At c = 0.01 the hazard of leaving R by `N` is selection, so the slope of the category-(A)-plus-
  strict-inspector hazard over 10³–10⁵ is above −0.3. [Falsifier: slope ≤ −0.3.]
* **E5 (prudent inspectees, chain).** The effect of Prediction 5 at c = 0 lies in [0, 0.1): the shield addresses the
  shadow route only. [Falsifier: effect ≥ 0.1 or < 0.]

## Controls and descriptive quantities (no verdict)

Blind arm at each lottery size; `exact_er` at (100, 64) and in the chain at N = 10⁴; direct starts at (`cr`, `C`) and
(`N`, `C`), N = 100 and 400, K at mutation rate 0 and with one K arrival at generation 100; migration mN ∈ {0, 1, 10}
at (100, 64); the crossed cell (400, 64); first-passage quantities (the branching of the first entry into E from
(`N`, `K`), mean first-passage times to E and R, occupation of committed, mixing and cheater-majority states on the
way back); support, transitions and circulation (CLAUDE.md rule 4); trajectories at common t and t/N.
