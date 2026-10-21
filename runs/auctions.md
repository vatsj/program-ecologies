# Coalition-proof auctions: prediction verdicts (2026-10-21)

Predictions: `predictions/2026-10-21-coalition-proof-auctions.md` (spec numbers verbatim, then the scoring conventions
committed before any code). Numbers: `runs/auctions/summary.json`, `runs/auctions/table_*.csv`, `runs/auctions/cells/`,
`notes/auctions-run.md`. Scored: **held 7** (2, 3, 7, 8, 9, 10, 12), **failed 4** (1, 4, 5, 6), **partial 1** (11).
Part A is exhaustive (AM) or a fixed-seed 3,000-instance subsample (the three 4-bidder families); Part B is the eps = 0
seed lottery at N = 100, 64 islands, 40 runs (2,560 islands per cell), every island fixed (no censoring).

| # | prediction (short) | result | verdict |
|---|---|---|---|
| 1 | substitutes: VCG in the core on 100%, truth robust in every mode and tie | VCG in the core 3,000/3,000, but truth robust on **0** instances in all five variants: every instance has a profitable winner-plus-runner-up ring ({1,2}, {3,4} and supersets break on 100%) | **failed** |
| 2 | VCG, AM, R1, T-strict: truth fails exactly where v_P > min(v_A, v_B) | 0/1,000 mismatches | **held** |
| 3 | surcharge, AM, R1, T-strict: losers' collusion never profits; singleton shading on at least 80% of positive-surcharge instances | pair {A, B} breaks on 0/1,000; singleton breaks on 835/835 = 100% of positive-surcharge instances | **held** |
| 4 | spite (T-weak, R1) deters at least 80% of T-strict breaks under both rules (falsifier below 50%) | instance level 0% (VCG), 0% (surcharge); event level 0% (VCG, spec grid), 45.5% (surcharge); wide-responder sensitivity 40.6% and 45.5% | **failed** (as scored; substance in the note below) |
| 5 | R2: first-price notion core empty on most AM instances (falsifier: nonempty on more than 50%) | nonempty on 1,000/1,000 under both R2 ties; leader values exceed the joint marginal contribution on 0 of 6,000 pairs | **failed** |
| 6 | Bernheim–Whinston through the notion: payoff vectors within one tick of the bidder-optimal frontier on at least 90% (falsifier below 70%) | all vectors within one tick on 20.8% of instances (some vector 22.8%); 88% of sets contain a zero-revenue profile; 0.6% of vectors are in the true-value core | **failed** |
| 7 | ecology, collusion, VCG, no audit, U: enforced-pair islands at least 30% and policed at least 20% | pair 0.3027 (run sd 0.053; marginal), policed 0.334 | **held** (pair is 0.3 within sampling error: se 0.008) |
| 8 | police are a shadow: never tested on more than 50% of policed islands; removing `POL` raises pair islands at least 1.5× | never tested 94.5% (856 policed islands); no-police pair 1.000 against 0.303 = 3.3× | **held** |
| 9 | surcharge: collusion pair under 2%; threshold winners' deviations at least 40% (falsifier: collusion pair ≥ 5% or winners' deviations below 20%) | collusion pair 0.000; threshold items deviate 0.787 (behaviour), 0.977 (SH, PAIR or PAIRU fixed in A or B) | **held** |
| 10 | audit: enforced pairs and police 0 by construction; collusion VCG revenue with the audit at least that without | pair 0, police 0; revenue 10.0 against 7.69 (efficiency 1.00 against 0.70); threshold reported only: 7.39 against 7.68 | **held** |
| 11 | prior M: pair islands at least 1.5× U, and wherever `POL` founded with a deviating pair the pair is driven out in at least 70% (falsifier: below 50% means the policing under U is demographic) | pair 0.930 against 0.303 = 3.07× (held); driven out **7.0%** of 2,557 founded islands (failed; U: 69.7%) | **partial**: the second conjunct's falsifier is met |
| 12 | tremble (5%): `POL`'s expected payoff against an enforced pair is below `T`'s in VCG collusion | `POL` −0.45, `T` 0.025, `SH` 0.025 (no tremble: all 0) | **held** |

## Notes on the failures and the partial

* **1 (failed).** The core says nothing about rings: the notion lets a loser lower its report at no cost, which lowers a
  winner's price. In the substitutes family (where VCG is in the core, so the surcharge is zero) every instance is broken by
  the winner-and-runner-up coalition. The note's section 4 (rings are the wall) is confirmed in the strongest form: the wall is not
  only the grand ring, it is every pair containing a winner and a loser whose report enters the winner's price.
* **4 (failed as scored).** Two things, both in `notes/auctions-run.md` 1.3. (a) Truth is broken by a *mixed* coalition on
  every instance under both rules in the families that matter, which no spite response can deter (the loser loses nothing), so the instance-level
  deterred share is 0 whatever the tie rule. (b) Among *same-side* coalitions (singletons, pure loser groups, pure winner
  groups) spite does what the note said under the surcharge on the spec grid (robust ignoring mixed: 1.000 in all four
  families), and under VCG when responders can bid above the deviators' cap (1.000); on the spec's common grid cap the VCG pair overbids to the cap
  and spite fails (AM: 0.615 of instances still broken). The literal reading of the spec's graph (strict improvements
  only) gives T-weak = T-strict identically, so spite never counts; "spite counts" needs lateral best-reply moves.
* **5 (failed).** In first-price the complement's joint maximizers and best replies give the same leader values, and they never exceed the
  joint marginal contribution, so the R2 set is as nonempty as the R1 set (100%).
* **6 (failed).** The set contains the bidders' ring outcome (zero revenue): with only proper bidder coalitions and no
  seller player nothing bounds the bidders' total, so the one-round notion on scalar bids is a different object from
  Bernheim–Whinston's coalition-proof set, as the second review warned. Mean revenue in the set 0.34 against 2.64 under
  VCG at truth.
* **11 (partial).** Pair islands rise 3.07× when `POL`'s founding mass is matched to a pair's (6.25%), but the pair is then driven out on 7% of
  islands founded with both, against 70% under U: deterrence is demographic. Driven-out share by `POL`'s founder share
  in U: 0.56 (20–30%), 0.71 (30–40%), 0.87 (≥ 40%); in M 0.06 (< 10%), 0.15 (10–20%); the breakeven is `POL` at a quarter of P.
