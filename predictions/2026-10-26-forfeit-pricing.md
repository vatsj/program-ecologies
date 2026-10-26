# Predictions: charging forfeits like failed reads, exact simulators, and the security fallback, 2026-10-26

Spec `specs/2026-10-26-forfeit-pricing.md` (reviewed by gemini-4-argon, then gpt-6.1-sol in amended mode, folded; the RS's
addendum on A_m reviewed the same way and merged from main at 21402ed before any code). Hand derivations:
`notes/forfeit-pricing.md` section 1 (committed before any code, `bd09f62`). Written and committed before any code of this
run exists and before any counted cell: **no cell has run** (the only machine use so far was reading the static tables of the
merged catalogues: which programs forfeit and which reads time out, below). Everything here is an eps = 0 seed-lottery
statistic at finite (N, I, horizon) on fixed catalogues, grammars, caps and world K, never pi and never a large-population or
island-size claim. Every counted run uses fresh run indices (RPS and inspection runs 300-339, PD reps 300-339). Scoring:
held / partial / failed / not scored (untested if a cell was cut), each with the number, in `runs/forfeit-pricing.md` and `.json`.

## The RS's messages, first

On RESULTS "Confirming failure pricing as the default compute charge" (2026-10-26):

> "I think a forfeit should be charged, esp if our simulations do so implicitly. That way, opponents have the option to
> simulate an opponent EXACTLY, potentially at cost to themselves. I further propose that those 2 costs be equal, since
> they seem like the same failure."

The addendum (2026-10-26):

> "The RPS double-charge reads like a bug. The old rule is that a forfeit spits out the minmax action - thoughts on that as
> an alternative? For RPS that's the coin, which makes me worry about state-sponsoring that solution."

Static facts read from the merged tables before writing this file (no run): in the RPS catalogue only the prover `PB`
forfeits (against every capped simulator and against itself); `PRR` has three capped reads time out against `PB`; every
capped simulator times out against every other simulator and against `PB`, and `SIM20*` against the hash programs. The
inspection catalogue has no forfeits at all, so without X the inspection tables of A, A_f and A_m are identical and the
three cells differ only by dynamics seed (this gives a noise floor, used below).

## The spec's predictions and the registered counter-predictions (verbatim)

## Predictions (the RE's; falsifiers in brackets)

1. *The leak closes.* Under A_f, RPS by mixing is met at 0.3 and 1 [not met at 0.3, or failed at 1].
2. *The lower end is unchanged.* At 0.03 and 0.1, A_f equals the concurrent A within an equivalence margin of 0.05 in
   each score (paired, run-clustered intervals) (forfeits are already 0 there): RPS by mixing
   met, inspection and the PD met [any of them not met at 0.1].
3. *High prices.* At 10, RPS by mixing is met or undetermined, not failed by non-play [forfeits above 0.05 by upper
   bound at 10].
4. *Exact simulation is rarely worth it in RPS.* Against a private-tape mixer an exact simulation predicts nothing (the
   simulated invocation draws its own tape), and against another reader it risks a forfeit, so `SIMX` is modal on fewer
   than 0.05 of RPS islands at every level under A_f [≥ 0.05 at any level].
5. *Exact simulation helps the inspector a little.* `SIMX_I` reads a compliant constant inspectee cheaply and exactly,
   so with X the inspection efficient share is within 0.10 of the A_f cell without X at every level, and `SIMX_I` is
   modal on at least 0.1 of inspector slots at 0.1 [outside 0.10, or below 0.1]. *Counter-prediction (gemini-4-argon),
   registered:* the capped simulator already reads a compliant constant within its cap at no charge, so `SIMX_I` has no
   advantage, is worse against deep inspectees, and is modal on fewer than 0.1 of inspector slots. gpt-6.1-sol agrees
   on the mechanism but expects its modal share to be prior- and drift-dependent.
6. *The PD is unaffected.* A_f at 0.1 and 1 keeps the PD met (cost-inclusive), and its count is within 6 of 40 of the
   confirmation run's A at the same level (a margin above sampling noise at these rates) [not met, or outside 6].
   *Counter-prediction (gpt-6.1-sol), registered:* a 3-run margin would be falsified by noise alone.

### The RS's addendum (verbatim from the spec)

## Addendum (the RS, 2026-10-26): what a forfeit yields

The RS: "The RPS double-charge reads like a bug. The old rule is that a forfeit spits out the minmax action - thoughts
on that as an alternative? For RPS that's the coin, which makes me worry about state-sponsoring that solution." Under
A_f a forfeiter in RPS pays P_fail and also loses the play (−1 against any action, its pure security level), and its
opponent gains +1, which rewards making opponents run out of fuel. Arm **A_m**: a forfeit is replaced by the
forfeiter's security (maximin) strategy and charged P_fail once. In RPS that is the uniform mixture drawn by the
referee; in inspection and the PD the security strategies are pure (inspector: inspect; inspectee: comply; PD:
defect), so A_m's game outcome is a pure action there. [Addendum review 2] The notes publish the unilateral and mutual
forfeit payoff tables of each game under A, A_f and A_m entry by entry; where A_m's pure security action differs from
the stored forfeit outcome, inspection and the PD are separate treatments, not equivalence checks. Safeguards against
sponsoring the coin: a fallback play is never counted as the programme's own mixing in any statistic (individual
mixing, by-mixing and the coin share are computed on non-fallback plays, with the fallback share reported beside
them), and A_m is read against the stored finding that a free uniform default raised measured mixing from 0.25 to 0.87
with exploitability unchanged (RESULTS "Rock–paper–scissors and mixed actions").

Cells: A_m in RPS at 0.03, 0.1, 0.3, 1 and 10, with and without X, on the same fresh founders as A_f; inspection at 0.1
and 1 without X (a check that A_m equals A_f there up to the opponent's forfeit payoff). [Addendum review] Mutual
forfeit: under A_f and A the game's own mutual-forfeit payoff applies (RPS (0, 0); the stored tables elsewhere), stated
in the notes' hand table before P_fail; under A_m both forfeiters are replaced by their security strategies. [Addendum review 2] Exploitability is reported for the actual
policy, fallback actions included, and separately conditioned on completed plays; a conditional quantity with no
completed plays is undefined, never assigned a value. X-sham's population
mass and modal share are reported beside the exact simulators'. A concurrent A cell at 0.03 is added so that
prediction 2 is paired at both levels; prediction 2's PD clause is dropped (no concurrent PD A cells; prediction 6
covers the PD against the confirmation run, unpaired). Generation 2,000 is the primary endpoint; any extension to
4,000 covers every member of the matched comparison and is secondary. Intervals are run-clustered 95% bootstrap;
equivalence is two one-sided tests at the stated margin; "above 0.05 by upper bound" means not demonstrated below,
not demonstrated above. The notes report each simulator class's advantage on completed plays against its loss on
failed ones, and tests cover fallback independence, mutual fallback, nested timeouts and reservation exhaustion.

9. *The fallback is not selected.* Under A_m, the share of RPS plays that are fallbacks is below 0.05 at every level
   from 0.1 up, because a programme that forfeits into the mixture pays P_fail more than one that plays the coin itself
   [≥ 0.05 at any level from 0.1 up]. *Counter-prediction (gpt-6.1-sol), registered:* readers can profit on completed
   plays while occasionally falling back, so persistent fallback is possible at 0.1, especially with X.
10. *A_m and A_f agree on the band.* *Counter-prediction (gpt-6.1-sol), registered:* A_m removes the +1 reward for
   causing an opponent's forfeit, which changes selection, so classifications differ where reader-induced failures are
   common. A_m's classification equals A_f's at every level, matched by arm (A_m against A_f
   without X, A_m + X against A_f + X), and its by-mixing exploitability
   (non-fallback plays) is within 0.05 of A_f's [a classification differs, or exploitability differs by more].
11. *Exact simulation is cheaper under A_m.* `SIMX`'s population mass is at least twice its A_f mass at 0.1, because its
   worst case is the security value less P_fail rather than −1 less P_fail [less than twice]. *Counter-prediction
   (gemini-4-argon), registered:* both masses sit near the founder floor, so the ratio is founder noise.
## Scoring rules (fixed here)

**Statuses and classification** as in the confirmation run (`notes/failure-pricing-confirm.md` 1.2-1.3): RPS net (e_prog <= 0.10)
and by mixing (e_gross upper bound <= 0.10 and forfeit share upper bound <= 0.05); inspection net-of-charges efficient fraction
>= 0.60; PD cost-inclusive count against the 0.70 line by Wilson. A game's status is the worst of its components. The
classification of A_f at a level is *confirmed* iff all three games are met, *refuted* iff any is failed, *unresolved* otherwise.
The PD is run at A_f 0.1 and 1 only; at 0.03, 0.3 and 10 the PD status is carried from the confirmation run's A at the same level
(identical rule: the PD has no forfeits, see below) and the classification says so. Intervals are run-clustered 95% percentile
bootstrap (4,000 resamples, seed 20261025); paired quantities pair run indices (same founders). Equivalence of paired
means at margin d: the 90% bootstrap interval of the paired difference lies inside (-d, d) (two one-sided tests at 5%);
"equivalent" otherwise "unresolved", and "different" when the 95% interval lies outside (-d, d). Under A_m the by-mixing
score uses the arm's own e_gross (actual policy, fallbacks included) and the fallback share; the completed-play exploitability
e_comp is reported beside it and is NaN on islands without completed plays (never zero).

**Scoring each numbered prediction.**
* **1** held iff by mixing is *met* at A_f 0.3 and at A_f 1 (no-X cells); partial iff met at 0.3 and undetermined at 1; failed
  otherwise (not met at 0.3, or failed at 1).
* **2** (RPS and inspection only; the PD clause was dropped): at 0.03 and at 0.1, each of RPS e_gross, RPS forfeit share, RPS
  e_prog and inspection net efficient fraction is equivalent to the concurrent A cell within 0.05 (TOST), RPS by mixing is met under
  A_f at both levels and inspection net is met at 0.1. Held iff all; partial iff no difference is "different" and statuses are
  met or undetermined; failed otherwise.
* **3** held iff the forfeit-share upper bound at A_f 10 is <= 0.05 and by mixing is not failed; partial iff the point estimate is
  <= 0.05 but the upper bound exceeds it and by mixing is not failed; failed otherwise.
* **4** (X arm, A_f): held iff the pooled share of islands whose modal programme is `SIMX` is below 0.05 at every one of the five
  levels; failed if any is >= 0.05 (point estimate). The Wilson interval is reported beside it.
* **5** (inspection, A_f + X against A_f without X): held iff (a) the net-efficient fraction with X is within 0.10 of the no-X cell at
  every level (point estimates, paired) and (b) the share of islands whose modal inspector programme is `SIMX_I` is >= 0.1 at 0.1;
  partial iff one of (a), (b); failed otherwise. The counter-prediction of gemini-4-argon is held iff (b) fails (modal share < 0.1
  at 0.1) *and* the paired payoff table shows `SIMX_I` not better than `SI100n` against any opponent class by more than 0.05 net;
  gpt-6.1-sol's claim (prior- and drift-dependent modal share) is scored as "supported" iff the modal share of `SIMX_I` at 0.1
  differs by more than 0.03 between the A_f + X cell and the X-sham cell's counterpart share, else "not supported".
* **6** held iff A_f at 0.1 and at 1 have PD (C) status met and a count within 6 of 40 of the confirmation run's A at the same
  level (37/40 at 0.1, 36/40 at 1); failed otherwise. The gpt-6.1-sol counter-prediction (a 3-run margin would be falsified by
  noise alone) is held iff the count differs by more than 3 at one of the two levels. The recorder of the maximum encounter steps must
  show zero forfeits (steps <= 10^6) in every run, which makes A_f identical to A on the PD dynamics (reported).
* **9** held iff the fallback share (forfeit rate) under A_m has point estimate below 0.05 at every level 0.1, 0.3, 1, 10 in both
  arms (no-X and X); partial iff all no-X cells but not all X cells (or vice versa); failed otherwise. gpt-6.1-sol's counter is held
  iff the share is >= 0.05 at 0.1 in some arm.
* **10** held iff the RPS by-mixing status under A_m equals A_f's at each of the five levels in each matched arm (no-X against no-X, X
  against X), the inspection net status under A_m equals A_f's at 0.1 and 1 (no X), and A_m's completed-play exploitability (e_comp)
  is within 0.05 of A_f's at every level and arm (point estimates; cells where e_comp is NaN do not count); partial iff the
  statuses all agree and one e_comp comparison exceeds 0.05, or one status differs while undetermined/met; failed otherwise.
  gpt-6.1-sol's counter is held iff some status differs.
* **11** held iff SIMX's mean end-state population mass (generation 2,000, pooled over islands and runs) in the A_m + X cell at 0.1 is >= 2 x its
  mass in the A_f + X cell at 0.1; failed otherwise. gemini-4-argon's counter is held iff the run-clustered 95% interval of the ratio of
  the paired means contains 1 (both masses near the founder floor); undefined if both masses are 0.

## The engineer's predictions (written before any counted cell; informed by the stored sample and the static tables only)

* **E1 (the PB leak is the leak).** Under A_f (no X) `PB` is modal on at most 0.05 of RPS islands at 1 and at 10 (concurrent A at 1
  and 10: at least 0.4, as in the confirmation run: 0.57, 0.71). [PB >= 0.05 under A_f at 1 or 10; or PB < 0.4 under concurrent A at 1]
* **E2 (the free coin carries the high end).** Under A_f at 1 and 10 `U` is modal on at least 0.6 of RPS islands and `PRR` on fewer
  than 0.15 (the prover's 3P charge on `PRR` kills the guarded reader once `PB` is present, and a coin pays nothing). [U < 0.6 or PRR >= 0.15 at 1 or 10]
* **E3 (the concurrent A reproduces the confirmation).** Concurrent A (no X, fresh runs 300-339) has by mixing met or undetermined at
  0.03 and 0.1, undetermined at 0.3 and failed at 1 and at 10. [any status different by more than one step]
* **E4 (A_f = A below the leak).** At 0.03 and 0.1 the forfeit share is 0.000 under both rules (pooled run means < 0.002). [>= 0.002]
* **E5 (scarcity of the exact simulator).** `SIMX`'s end-state mass in RPS is below 0.002 at every level and arm, and `SIMX` is present
  (at least one individual at generation 2,000) on fewer than 0.10 of islands at every level from 0.1 up. [either exceeded]
* **E6 (inspection with X is not moved).** In inspection at 0.1 and 1 the X cells' net efficient fraction is within 0.10 of no X under A_f and A, and the
  end-state mass of `SIMX_I` is below that of its capped counterpart `SI100n` in the same cell. [either fails]
* **E7 (the sham is neutral).** X-sham at 0.1 and 1 is within 0.05 (point estimates, paired) of the A_f cell without X in RPS e_gross, RPS forfeit share and
  inspection net efficient fraction. [any beyond 0.05]
* **E8 (the noise floor).** Inspection without X has identical tables under A, A_f and A_m; the paired differences in the net efficient fraction among the
  three cells at 0.1 and 1 have point estimates within 0.06, so that 0.05 is about a sampling-noise margin at 40 runs. [> 0.06]
* **E9 (A_m close to A_f in RPS without X).** Without X the forfeits come only from `PB` (against simulators and itself): the A_m and A_f cells'
  e_comp differ by at most 0.02 at every level and the fallback shares by at most 0.02. [either exceeded]
* **E10 (the PD).** A_f at 0.1 and 1 has the confirmation run's pattern (count 34-40) with zero forfeits in every run. [count < 34, or any forfeit]
* **E11 (the classification).** A_f is confirmed at 0.03, 0.1, 0.3 and 1, and confirmed or unresolved at 10 (the net target at 10 was
  undetermined under A: 0.094 [0.057, 0.138]). [refuted at any of 0.03-1, or confirmed label differs at 0.1]
* **E12 (no hidden sponsorship).** Under A_m the coin's mass (the share of programmes whose completed plays are uniform: `U`, plus
  `PRR`, `CRR` guards counted separately) at 1 and 10 is within 0.10 of its A_f value; the fallback share does not exceed the A_f
  forfeit share by more than 0.02. [either exceeded]
