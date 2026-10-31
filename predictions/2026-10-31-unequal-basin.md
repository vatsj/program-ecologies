# Predictions: where the unequal basin of the length-prior arms comes from (2026-10-31)

Committed before any code of this experiment runs and before any counted cell. Spec `specs/2026-10-31-unequal-basin.md`
(queue 70; reviewed by gemini-4-argon, then gpt-6.1-sol in `--mode amended`, both folded; the folded spec is the
authority); notes `notes/unequal-basin.md` §1 (hand analysis: what the arms are, units, the key triples, the
class count and the stop rule), written before this file.

## The RS's message

> RS (2026-10-31), on the RE's list of next experiments ("1. Where the unequal basin comes from …"): "1 sgtm btw"

The target (DEFERRED 15): in majority-division games every island lands in the stable set V\* (the three fair pairs),
each member equally likely across independent worlds. RESULTS "Islands to infinity before time" found the DSL arms L
(weak evaluator) and M (modalPA) bistable on the symmetric chain; "Arm T under islands to infinity before time" showed
the nine constants alone reach V\* = 1 from every tested start. The question here: which programs of the length-prior
arms carry the unequal basin, and how.

## Frozen design choices (made before any run; the spec silent or open)

- Object, cells, starts, tilt scan, convergence criterion, charge, validations V1–V6 as in the spec. The cells are
  L × {P_fail 0, 0.1} and M × {0} at A = 0, then L × 0 and M × 0 at A = 150 (first to cut).
- **Scoring object.** The predictions are scored on the object that is actually computed. Notes §1.5 registers, before
  any run, that the behavioural lumping is expected to be vacuous (C per slot = support size ≈ 1,300) so the dense
  exact ODE has ≈ 2 × 10⁹ states and the spec's stop rule is expected to fire. If it fires, the object computed is the
  reflecting m-conditional truncation of notes §1.5 (an island holds at most m conditional programs; a blocked event
  is a null event; its rate is the reported leak), m = 1 and m = 2, validated by V3 against the full-dynamics Monte
  Carlo on the same empirical law. Every verdict is labelled with m. A verdict whose m = 1 and m = 2 values straddle
  its threshold is **partial**, and if V3 fails the verdict is **unscored**.
- **Empirical-start object** (spec, after the second review): the I → ∞ dynamics started from the post-anneal law of the
  3-pool union (49,152 islands) and restricted to its S₃-union supports plus the nine constants. All conclusions are
  restricted to that start; the seed-law mass of programs absent from the union is reported.
- Verdict classes: **held** iff the stated inequality holds in every cell it names (L and M, and for both m if m
  truncation is in force); **failed** iff the falsifier holds in any such cell; **partial** otherwise (labelled);
  **unscored** if unresolved (criterion (a) of the spec, plus the rare-class certificate for U-dominated endpoints) or
  unavailable. An endpoint is "U-dominated" iff U ≥ 0.5 at convergence ("U ≥ 0.9" where a prediction says so).
- u\* is the first U-dominated crossing within the scanned range u ∈ {0.3, …, 0.9} (bisected to ±0.02); u\* = "none" if
  no scanned u ≤ 0.9 ends U-dominated. A "shift" in u\* between "none" and a number is a shift of at least 0.9 − the
  number; two "none" are no shift.
- The families of the spec are scored as stated; because A2s and A2x are empty at n ≤ 6 (notes §1.1), prediction 4's second
  clause is registered as **vacuous before any run** (it will be reported as unscorable, not held). The informative
  syntactic splits of A1 used for attribution are defined in the engineer's predictions below, before the data.

## The RE's predictions (from the spec, falsifiers in brackets)

1. **The basin exists.** In the exact ODE at A = 0, P_fail 0, both L and M end U-dominated (U ≥ 0.9 at convergence)
   from the 0.6 unequal tilt. [either arm ends with V\* ≥ 0.9 from that start.] (Confidence about 0.65; the alternative is that
   the stored bistability was the Monte Carlo's support collapse.)
2. **Natural starts.** L ends with V\* ≥ 0.99 from its natural start; M ends U-dominated (U ≥ 0.5) from its natural start, as
   in the stored chain. [L below 0.99, or M with V\* ≥ 0.5.] (Confidence 0.8 for L, 0.5 for M.)
3. **Conditionals carry it.** Removing all conditional programs (constants only) removes the basin in both arms (u\* =
   none). [the constants-only cell has u\* ≤ 0.9.] (Confidence 0.85; V1 checks one constants-only start, not the
   correlated laws that replacement and tilting produce.)
4. **Which family.** Removing A1 alone removes the basin (u\* = none) in both arms, while removing A2s and A2x (together
   or alone) leaves u\* within 0.1 of the full arm. [A1 removal leaves u\* ≤ 0.9, or removing A2s or A2x moves u\* by more
   than 0.1.] (Confidence 0.4: I do not know whether one atom suffices.)
5. **Mechanism: the excluded slot.** The decisive classes (largest Δu\* in the attribution) sit in the excluded slot of the
   dominant unequal triples, and they block the constants' rescue move by not offering ½ to a switching low demander
   (they condition on what the pair plays). [the top-ranked class sits in a pair slot, or the blocked rescue is blocked by
   retaliation from the high demander.] (Confidence 0.5.)
   *Counter-prediction (gemini-4-argon), registered:* the obstruction sits in the pair slots, a conditional low demander
   that accepts 1/3 against a 2/3 demander and does not switch to the excluded slot unless the excluded slot already
   offers it ½, or a high demander that punishes defection; an excluded slot offering ½ invades neutrally, so it cannot
   be the block.
6. **Stability.** The unequal endpoint is linearly stable on its support, with a strictly negative leading eigenvalue on
   class-changing directions (≤ −10⁻⁵ per event), unlike the neutral single-pair endpoint of constants. [a leading
   eigenvalue ≥ −10⁻⁶ (neutral or unstable) on those directions.] (Confidence 0.6.)
   *Counter-prediction (gpt-6.1-sol), registered:* at least one arm has a near-zero mode at the unequal endpoint, or its
   stability on the support does not extend to the transverse directions; at ε = 0 the faces with missing donors are
   invariant, so neutral directions and non-hyperbolic attraction are plausible.
7. **The charge.** In L, A_f at P_fail 0.1 moves u\* by less than 0.05 against P_fail 0. [|Δu\*| ≥ 0.05.] (Confidence
   0.7; divergent programs are a small part of the founding law, but a divergence-prone carrier would change this.)

Note (gpt-6.1-sol, on prediction 3): V1 validates one constants-only start, not every correlated law that replacement and
tilting produce; "constants-only probably still reaches fairness" is its prediction, consistent with 3, and no more
confident than the 0.85 stated. Scored as 3 is, with the replacement-and-tilt cell (not only V1) as the evidence.

The RS was not asked to add predictions (the spec invites them; the RE decides).

## The engineer's predictions (from notes §1; not the RE's; scored as stated)

Definitions used below, fixed now. A *yielder* in slot s: a canonical conditional `if(THEM_j = a, x, z)` whose atom's
action a names slot s (the owner) at demand ⅔ and whose true branch x names j at ⅓ (16 per slot: 2 readable partners ×
8 false branches z ≠ x). A *fair reader*: atom action a names s at ½ and true branch x names j at ½ (z any other
action). A *bully conditional*: true or false branch names a partner at ⅔. A *conditional program is in role* high /
low / excluded of a triple by the role of its slot in that triple's outcome.

E1. **Lumping is vacuous.** The number of behaviour classes per slot equals the number of programs in the (S₃-union ∪
    constants) support, to within 1%, in L and in M; the S₃-union of the 3-pool post-anneal supports holds at least
    1,250 of the 1,296 conditionals per slot. [classes < 0.99 × support, or union < 1,200 conditionals.]
E2. **The dense exact object does not fit.** Classes per slot > 1,000, so C³ > 10⁹ and the spec's stop rule fires.
    [C ≤ 300.]
E3. **The truncation is converged by m = 2.** The m = 1 and m = 2 reflecting truncations agree on the natural-start
    endpoint's V\* to within 0.02 and on the U-dominated / V\*-dominated classification of every tilted start. [V\*
    differing by 0.05 or more, or a different classification of any start.] The blocked-event (leak) rate at m = 2 is
    below 0.05 of the event rate over the whole trajectory of the natural start. [≥ 0.05.]
E4. **Founding.** Post-anneal conditional mass per slot in [0.015, 0.04]; post-anneal V\* within 0.02 of the stored 0.280
    (L) and 0.277 (M) at A = 0 (and 0.339 / 0.332 at A = 150); L at P_fail 0.1 within 0.01 of L at 0; the mass of triples
    with a diverging slot below 10⁻³. [any outside.]
E5. **The stored bistability is mostly the finite pool.** For L at A = 0, P_fail 0: u\* = none (the 0.6 unequal tilt and
    every scanned u ≤ 0.9 end with V\* ≥ 0.5), i.e. the RE's prediction 1 fails for L. [L with a U-dominated endpoint at
    u = 0.6.] Confidence 0.5. For M I register no separate directional prediction (0.5).
E6. **Where a basin exists, a U-dominated endpoint is metastable, not an attractor.** At least one rare class (mass <
    10⁻³) has a positive relative growth rate at the horizon, or the residual falls below 10⁻⁹ only after 10⁶ events, in
    every cell with a U-dominated endpoint. [a U-dominated endpoint certified as an attractor at the stated tolerance
    in every cell having one.]
E7. **The carrier is the yielders, through the inflow.** If a basin exists (a finite u\*), then among the top 5 classes of
    the attribution (per slot role, by Δu\*) at least one is a yielder, and the top-ranked class is a pair-slot class
    (high or low), not an excluded-slot class. [no yielder in the top 5, or the top-ranked class sits in the excluded
    role.] (Closer to gemini-4-argon's counter to prediction 5 than to the RE's, for the reason in notes §1.4; argon puts
    the obstruction in the rescue, I put it in the inflow V\* → U.)
E8. **The excluded slot is not a first-order blocker.** Removing every excluded-role conditional class jointly (all
    top-20 classes that sit in the excluded role of the dominant unequal triples) shifts u\* by less than removing the
    top-20 pair-role classes. [the reverse.]
E9. **Tilt inflation.** The conditional share of the U class at t = 0 is at least 1.5 × the natural start's conditional
    share per slot, so the 0.6 tilt inflates conditionals' donor share. [ratio < 1.2.]
E10. **Charge.** In L the P_fail 0.1 ODE changes u\* by less than 0.05 and the natural endpoint's V\* by less than 0.01;
     the crossed cell (founded at 0, migrating at 0.1) is within the same bounds. [either bound exceeded.]
E11. **M versus L.** M and L natural-start V\* at the first checkpoint (10 events) differ by less than 0.02; they separate
     later only through triples with a reading edge (mutual edges between conditionals), so if M's natural start ends
     U-dominated while L's does not, at least one of the M attribution's top 5 classes is a fair reader or another class
     whose atom reads a partner's action that names the owner. [M's separation without any reading-edge class in its top 5,
     or M ≠ L at 10 events by 0.02 or more.]
E12. **Spectrum of the fair endpoint.** At a V\*-dominated endpoint the invariant-subspace Jacobian has all
     class-changing eigenvalues within 10⁻⁶ of zero on the support (neutral faces), as in arm T; the transverse
     (symmetry-breaking) spectrum has a positive real part, as in arm T's knife-edge. [an eigenvalue ≤ −10⁻⁵ on the
     invariant subspace, or a non-positive transverse spectrum.]
E13. **Restoration is dose-dependent where a knockout works.** If the smallest knockout set removes the basin, restoring
     it at 0.25, 0.5 and 1 × its mass brings u\* back monotonically (u\* "none" → number decreasing in the dose) and
     1 × reproduces the unablated u\* within 0.05. [non-monotone, or 1 × differs by 0.1 or more.] Matched-mass random
     knockouts shift u\* by less than half of the carrier knockout's shift. [random shift ≥ half.]

## Scoring and reporting rules

- Every prediction gets one of held / failed / partial / unscored with the numbers behind it, in the run report and the
  RESULTS draft. No registered prediction is edited after the first counted cell; additions after the data are labelled
  as such and are not scored.
- Support and transition structure are reported alongside every share (CLAUDE.md discipline 4): class counts per slot,
  the top donor classes of each endpoint, the U ↔ V\* flux decomposition, the rescue-move table.
- Failures are reported as failures; REJECTED entries are drafted for every failed prediction.
