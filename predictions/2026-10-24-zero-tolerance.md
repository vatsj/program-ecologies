# Predictions: zero-tolerance, suspicious and sampling inspectors, 2026-10-24

Spec `specs/2026-10-24-zero-tolerance.md` (reviewed by gemini-4-argon, then gpt-6.1-sol in amended mode; both folded).
Hand derivations: `notes/zero-tolerance.md` §1 (committed before any code). Written and committed before any code of
this run exists and before any counted cell. Chain numbers are ε→0 chain quantities (π over pairs of monomorphic role
classes, whole state space), lottery numbers are ε = 0 seed-lottery statistics at finite (N, I, horizon), never π.
Scoring is held / partial / failed / not scored, each with the number, in `runs/zero-tolerance.md` and `.json`.

## The RS's statement

"I'd like u to manage that thread autonomously" (the RS, 2026-10-24): the inspection thread (the enforcer and its
shadow, and the inspector programs that might close its gap) is delegated to the RE. This spec is the RE's next step on
that thread; the RS registered no prediction of his own on it.

## Definitions fixed here (engineer, before any code), so no threshold can move afterwards

* **E, R, R\*, E\*, rates, fates, categories (A)–(G), slopes:** exactly as in `predictions/2026-10-24-inspection-shadow.md`
  (E = both mean game payoffs ≥ −0.05, gross of the price; R = E with an inspector class that deters the constant cheater,
  P(inspect | K) > 1/4, computed per arm so that R includes the arm's added inspector; hazards are flux over π of the set,
  per mutation event). **Light-cheater exit = category (D)** (strict invasion by a non-reading inspectee other than K) and
  **bounded-read exit = category (E)** (strict invasion by a reading inspectee, clean plus forfeit-driven); the shadow is
  (A); "others" is the rest. The **resident-specific** hazards are the one-state rates out of (added inspector, `C`),
  (`cr`, `C`) and (`N`, `C`) (`reference_exits`).
* **π(E) contrasts use the newly computed control** (the same total added mass m = 0.0013517 given to the class of
  `cr(THEM(ME))`), at each (N, c); the stored 0.0466 (N = 10⁵, c = 0) is context only. An arm "gains" = its π(E) minus the
  control's, same N and c. **Fixed reference weights** for aggregate hazards: the control's stationary distribution on R;
  **own weights**: the arm's.
* **Clauses over a range of N:** a clause that must hold at N = 10⁴ and 10⁵ is *held* if it holds at both, *partial* if at
  exactly one, *failed* if at neither.
* **Effect-size predictions:** *held* at or above the threshold, *failed* at or below the registered falsifier, *partial*
  between; the point estimate decides; run-clustered 95% intervals (4,000 bootstrap resamples of runs) are reported
  beside lottery numbers (the chain has no sampling error).
* **Lottery statistic:** efficient islands (share of islands with both mean game payoffs ≥ −0.05) at the horizon 20N,
  averaged over islands then runs; paired contrasts by run (the founders of an arm coincide with the control's except in
  the slots replaced by the arm's program, about 9 of 6,400 at (100, 64); dynamics seeds are shared). Unresolved
  islands (not in a single resident pair for the last N generations) are reported. All lottery numbers are finite-horizon.
* **Cuts** follow the spec's cut order (400-island cell, N = 10⁵ at c = 0.01, `sr_4`) and are disclosed.

## The RE's predictions (verbatim from the spec, with falsifiers)

1. *Zero tolerance closes the light-cheater exit, and only that.* In the ZT arm at c = 0, the light-cheater exit hazard
   from R falls by at least 10× against the control at N = 10⁴ and 10⁵, and π(E) at N = 10⁵ lies between the control
   (0.047) and the light-cheaters-removed reference (0.239): at least 0.1 [below 0.07]. *Counter-prediction
   (gemini-4-argon), registered:* the bounded-read exit absorbs the flow and π(E) stays below 0.10.
   *Scoring:* held iff the category-(D) hazard from R in the ZT arm is at least 10× below the control's at both N = 10⁴
   and 10⁵ **and** gain + control ≥ 0.1, i.e. π(E)_ZT(10⁵) ≥ 0.1; failed iff π(E)_ZT(10⁵) < 0.07; partial otherwise. The
   counter-prediction is held iff π(E)_ZT(10⁵) < 0.10 **and** category (E) is the largest exit from R in the ZT arm at
   N = 10⁵.
2. *The suspicious default closes the other exit.* ZT+SUS reaches at least 0.5 at N = 10⁵ (both-removed reference 0.811)
   [below 0.3]; SUS alone lies near the reading-exploiters-removed reference (within 0.1 of 0.036) [above 0.2].
   *Counter-prediction (gpt-6.1-sol), registered:* targeted exit rates fall more reliably than stationary inefficiency;
   the flow moves to shadows and other routes, so 0.5 is overconfident.
   *Scoring:* π at N = 10⁵, c = 0. Held iff π(E)_ZT+SUS ≥ 0.5 **and** π(E)_SUS ≤ 0.136; failed iff π(E)_ZT+SUS < 0.3 **or**
   π(E)_SUS > 0.2; partial otherwise. The counter-prediction is held iff the category-(E) hazard from R falls by at least
   10× against the control at both N = 10⁴ and 10⁵ in both the SUS and the ZT+SUS arms **and** π(E)_ZT+SUS(10⁵) < 0.5.
3. *Sampling.* `sr_16` raises π(E) at N = 10⁵ above the control by at least 0.1; `sr_1` does not [`sr_16` gains under
   0.05]. *Counter-prediction (gpt-6.1-sol), registered:* sampling leaves a low-q escape channel (q below about 0.018 at
   k = 16), so its benefit depends on the grammar's q grid.
   *Scoring:* c = 0. Held iff gain(`sr_16`) ≥ 0.1 and gain(`sr_1`) < 0.1; failed iff gain(`sr_16`) < 0.05; partial
   otherwise (including `sr_16` ≥ 0.1 with `sr_1` also ≥ 0.1). The counter-prediction is scored held iff gain(`sr_16`)
   < 0.1 while the category-(D) hazard of the `sr_16` arm is zero (the grammar has no mixer below q*₁₆ = 0.0178, notes
   §1.1, so the stated channel is empty on this grid; a benefit limited by another channel is then recorded as such).
4. *Price.* At c = 0.01, `sr_16` pays 16 levels per read on path and loses to `zt` (one level) [`sr_16` at least matches
   `zt`]. *Scoring:* π(E) at c = 0.01, N = 10⁴ and 10⁵: held iff π(E)_ZT − π(E)_SR16 ≥ 0.02 at both N; partial if it is
   positive but below 0.02 at one or both N, or ≥ 0.02 at one only; failed iff π(E)_SR16 ≥ π(E)_ZT at both N. The
   resident-level fact (net payoff −0.16 against −0.01 against `C`, notes §1.4) is reported beside it. If N = 10⁵ at
   c = 0.01 is cut, the clause is scored at N = 10⁴ alone (held iff the difference ≥ 0.02).
5. *Lottery.* Efficient islands change by less than 0.1 in every arm at (100, 64), since the lottery was not limited by
   light cheaters [any arm moves by more than 0.15]. *Scoring:* the paired difference arm minus control of efficient
   islands at the horizon 2,000, for every arm (ZT, SUS, ZT+SUS, SR1, SR4, SR16, the unconditional comparator), at c = 0
   and at c = 0.01 (the prices are scored together): held iff every |difference| < 0.1; failed iff any |difference| > 0.15;
   partial otherwise.

## The engineer's added expectations (from notes §1; not part of the RE's list; non-binding but scored)

* **E1 (the suspicious variants remove the bounded-read channel at D = 12).** The nine stored reading strict invaders
  are all deleterious or neutral against `cr_s` and `zt_s` (notes §1.3), so in the SUS and ZT+SUS arms at c = 0 the
  category-(E) hazard from R falls by at least 10× against the control at N = 10⁴ and 10⁵. [Falsifier: it falls by less
  than 10× at either N in either arm.]
* **E2 (phase).** The closure of E1 is a coincidence of D = 12 (the exploit repeats with period 4 in the depth cap; notes
  §1.3): in the D = 11 control the SUS gain over its own D = 11 control at N = 10⁵ is at least 0.2 smaller than the D = 12
  gain. [Falsifier: the D = 11 gain is within 0.1 of the D = 12 gain.] This is an extra cell, outside the spec; it is
  reported, scored and does not enter the verdicts on 1–5.
* **E3 (zero tolerance parks the light cheater).** In the ZT arm the occupancy of the light-cheater detour at N = 10⁵ is
  at least 3× lower than the control's [falsifier: lower by less than 3×].
* **E4 (commitment is not the mechanism).** The unconditional-inspector comparator gains less than 0.05 on π(E) at
  N = 10⁵, c = 0 [falsifier: it gains 0.05 or more]; it is dominated (notes §1.2) and cannot hold R.
* **E5 (`sr_1` is the stored `RI`).** The `sr_1` arm (mass added to the class of `if(THEM(ME)=C,N,I)`) differs from the
  control by less than 0.03 in π(E) at N = 10³–10⁵, c = 0 [falsifier: 0.03 or more at any N]; its inspector row is
  that of the stored class (notes §1.5).
* **E6 (`sr_16` is not immune).** The `sr_16` arm's category-(E) hazard from R at N = 10⁵ is not zero (the exploiter
  `cr(coin(N, coin(X, THEM(ME))))` earns +0.79 against it) [falsifier: zero to 10⁻¹²].

## Controls and descriptive quantities (no verdict)

The recomputed control; the validation arm (added mass 0: it reproduces the stored chain; tolerance below); the
unconditional comparator; resident-specific fixation and exit rates for every arm; aggregate hazards under fixed
reference weights and under each arm's own; behavioural-class membership and aggregated mutation mass of every added
program; realized read costs and timeout (forfeit) frequencies; entry and exit scaling in N and the support (the number
of pair states carrying 0.99 of π), transitions and circulation (CLAUDE.md rule 4); lottery trajectories at common t and
t/N, unresolved islands and late transitions; the optional D = 11 and D = 13 phase cells.

**Validation tolerance (fixed here).** With added mass 0 and the stored class tables, the arm must reproduce the stored
chain to a relative 10⁻⁶ in π(E) at N = 10³ and 10⁴ and 10⁻⁴ at 10⁵ (the stored run was float32), and the lottery runs
0–2 at (100, 64) must reproduce the stored cell bit for bit at generation 2,000. A failure stops the run before any counted cell.
