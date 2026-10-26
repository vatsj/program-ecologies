# Predictions: confirming failure pricing as the default compute charge, 2026-10-25

Spec `specs/2026-10-25-failure-pricing-confirmation.md` (reviewed by gemini-4-argon, then gpt-6.1-sol in amended mode; both
folded). Hand derivations: `notes/failure-pricing-confirm.md` §1 (committed before any code, `f437753`). Written and
committed before any code of this run exists and before any counted cell. Everything here is an ε = 0 seed-lottery
statistic at finite (N, I, horizon) on fixed catalogues, grammars, caps and world K, never π and never a large-population or
island-size claim. Every counted run uses fresh run indices (PD reps 200-239; RPS and inspection runs 100-139). Scoring:
held / partial / failed / not scored, each with the number, in `runs/failure-pricing-confirm.md` and `.json`.

## The RS's message (2026-10-25), first

On the report "What compute should cost" (failure pricing at P_fail = 0.1 was the only cell meeting all three targets, on
pooled PD runs):

> "Next steps sg, happy to make this our working hypothesis / default compute charge."

DEFERRED 16 records the adoption as a working hypothesis with a circle-back after this run. This run is the circle-back's
evidence: it classifies the default as **confirmed, refuted or unresolved** on fresh runs.

## The spec's predictions and the registered counter-predictions (verbatim)

## Predictions (the RE's; falsifiers in brackets)

1. *The default holds.* On fresh runs A at 0.1 meets the RPS and inspection targets at (100, 64), and the cost-inclusive
   PD is met or undetermined with a point estimate ≥ 0.75 (40 runs cannot separate 0.85 from the 0.70 line reliably;
   that outcome classifies the default as unresolved, not confirmed) [any game failed; or the PD undetermined with a
   point estimate below 0.75]. *Counter-prediction (gpt-6.1-sol), registered:* inspection at (100, 64) is
   undetermined, its interval straddling 0.60.
2. *Inspection at larger geometry.* At (400, 16) A at 0.1 is met or undetermined with a point estimate ≥ 0.60, and
   within 0.10 of the zero price [failed, or more than 0.10 below the zero price].
3. *Band width.* RPS fails at 0.03 (simulators survive, as at 0.01) and is met by mixing at 0.3; inspection and the PD
   are met or undetermined at every level from 0.03 to 0.3 [RPS met by mixing at 0.03, or failed at 0.3; or inspection
   or the PD failed at any level from 0.03 to 0.3].
   *Counter-prediction (gemini-4-argon), registered:* 0.3 is already costly enough for guarded reads during the
   scramble that by-mixing is borderline or fails at 0.3.
4. *Mixing, not non-play, at 0.1.* At P_fail = 0.1 the RPS by-mixing score is met and `PRR` is the modal programme on at
   least 0.8 of islands; at 1 and 10 the by-mixing score fails [by-mixing fails at 0.1, or is met at 1 or at 10].
5. *Cost-inclusive PD.* A keeps its PD verdicts with the charge included (the cost-inclusive count within 2 runs of the
   cost-blind count at every A level), and its end-state charge per play is below 0.01 of the range in every run;
   stored F at 10⁻² fails it [A's count drops by more than 2 at any level; or any A run's end-state charge ≥ 0.01 of
   the range; or F 10⁻² passes]. *Counter-prediction (gpt-6.1-sol), registered:* terminal charges may be tiny while
   the scramble's charges change which network establishes.

## Scoring rules (fixed here)

**Component statuses** (`notes/failure-pricing-confirm.md` §1.2): each score is met / failed / undetermined by the
run-clustered bootstrap interval (means) or Wilson (PD counts) against the registered threshold. A game's status is the worst
of its components in the order failed < undetermined < met.
* RPS: net target (e_prog <= 0.10, registered) and by mixing (e_gross <= 0.10 and forfeits <= 0.05, both by upper bound).
* Inspection: net-of-charges efficient fraction >= 0.60 (the gross fraction is reported beside it).
* PD: score (C) = persistent universal-open (last 500 generations) with end-state charge per play <= 0.3 (0.1 of the range 3),
  against the 0.70 line; (B) persistent without the charge and (A) end-snapshot are reported beside it.

**Classification of the default** (A at P_fail = 0.1, geometry (100, 64), fresh runs): *confirmed* iff all three games are
met; *refuted* iff any game is failed; *unresolved* otherwise. The geometry (400, 16) (RPS and inspection) is classified
apart with the same rules on those two games and stated as a qualifier in the headline (a failed there is a limit on the
claim). Conclusions never leave the tested geometries.

**Scoring each numbered prediction.**
* **1** held iff RPS (both components) and inspection (net) are met at A 0.1 and the PD (C) status is met or undetermined with
  a point estimate >= 0.75 (>= 30 of 40); partial iff no game is failed and the PD point estimate is >= 0.75 but RPS or
  inspection is undetermined; failed iff any game is failed or the PD is undetermined with point < 0.75. The registered
  counter-prediction (gpt-6.1-sol, inspection undetermined at (100, 64), its interval straddling 0.60) is held iff the
  inspection status at A 0.1 is undetermined.
* **2** at (400, 16): inspection net-efficient fraction at A 0.1 with status met, or undetermined with point >= 0.60, and
  the point estimate no more than 0.10 below the fresh zero price at the same geometry: held; partial if only one of the two
  clauses holds; failed otherwise (the unscored clause is stated).
* **3** three sub-claims. (3a) RPS game status at A 0.03: failed = held, undetermined = partial, met (by mixing) = failed.
  (3b) RPS by-mixing at A 0.3: met = held, undetermined = partial, failed = failed. (3c) inspection and PD (C) not failed at
  0.03, 0.1 and 0.3. P3 is held iff all three are held; partial if none is failed but one is partial; failed otherwise. The
  registered counter-prediction (gemini-4-argon, by mixing at 0.3 borderline or failing) is held iff (3b) is not *met*.
* **4** held iff by mixing is met at 0.1, PRR is the modal programme on >= 0.8 of islands (pooled point estimate), by mixing
  is failed at 1 and failed at 10; partial if exactly one of the four clauses fails and none by more than a boundary status
  (undetermined); failed otherwise.
* **5** three sub-claims. (5a) the cost-inclusive (C) count is within 2 runs of the cost-blind (B, persistent) count at every
  A level (0.03, 0.1, 0.3, 1, 10). (5b) every one of the 200 priced PD runs has an end-state charge per play below 0.03
  (0.01 of the range). (5c) the stored F at 10^-2 fails (C) (the stored rows are scored retrospectively). Held iff all
  three; partial iff (5a) and (5c) hold and (5b) fails in at most 2 runs or vice versa; failed otherwise. The registered
  counter-prediction (gpt-6.1-sol, terminal charges tiny while the scramble's charges change which network establishes)
  is held iff (5b) holds and the paired PD price-minus-zero difference in the persistent universal-open proportion has an
  interval excluding 0 at some level of 0.03 to 10 (a scramble effect on which network establishes, not on the end-state
  charge).

## The engineer's predictions (written before the fresh runs; informed by the exploratory stored sample, not by any fresh run)

* **E1 (net against gross).** At A 0.1, (100, 64), the net-of-charges efficient fraction is within 0.05 of the gross fraction
  (the stored inspector charge was 0.003, but the inspector's mean payoff sat near the -0.05 line). [gap > 0.05]
* **E2 (the scramble is where the price acts).** In the PD the scramble charge per play (generations <= 200) at A 0.1 is
  below 0.03 raw, and the ratio of the scramble charge at A 10 to that at A 0.1 is below 100 (selection removes the programs that time out,
  so the charge does not scale with the price). [scramble charge at 0.1 >= 0.03; or the ratio >= 100]
* **E3 (persistence is not the binding clause).** In every PD cell the persistent count (B) is within 2 runs of the
  end-snapshot count (A). [more than 2 at any level]
* **E4 (the PD is price-blind from 0.03 to 0.3).** Paired persistent-UO differences (price minus zero, same rep) have
  intervals containing 0 and magnitudes <= 0.15 at 0.03, 0.1 and 0.3. [any excluded or larger]
* **E5 (the 0.03 edge).** At A 0.03 the PRR modal share on RPS islands is between 0.55 and 0.85 (stored: 0.52 at 0.01, 0.91 at
  0.1). [outside]
* **E6 (stakes-normalized point).** At A_s (RPS 0.2, inspection 0.5) the by-mixing score is met and the inspection net
  fraction is >= 0.60 and between the fresh values at 0.3 and 1 (+-0.05). The PD A_s cell is A 0.3 (no separate run). [either
  clause fails]
* **E7 (large geometry).** At (400, 16): RPS by mixing is met at A 0.1 and the fresh zero price fails the by-mixing score
  (stored zero price e_prog 0.679). [either clause fails]
* **E8 (nested failed reads are rare).** At A 0.1 the non-topmost (nested inside a timed-out call) share of counted timed-out
  calls is at most 0.10 in RPS and in inspection. [> 0.10 in either]
* **E9 (the classification).** The headline is **unresolved**, because the PD cost-inclusive count is the pivot: 34 of 40 is
  the smallest count that meets the 0.70 line and a true rate near 0.85-0.875 reaches it with probability 0.6-0.77.
  Probabilities: unresolved 0.50, confirmed 0.35, refuted 0.15. [a different label; the PD (C) count at A 0.1 outside
  31-37]
* **E10 (the edges, as stored).** PD (C) is not failed at A 1 and A 10 (point estimates >= 0.70; stored 0.825, 0.800 pooled), and
  inspection net is met at A 1 and at A 10. [PD failed or inspection not met at either]
