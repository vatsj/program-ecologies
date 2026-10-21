# Predictions: coalition-proof auctions, 2026-10-21

Spec `specs/2026-10-21-coalition-proof-auctions.md` (reviewed by gemini-4-argon, then gpt-6.1-sol in amended mode, both
folded). Notes `notes/coalition-proof-auctions.md`. Written and committed before any code and any counted cell. Part B
statistics are eps = 0 seed-lottery statistics at finite (N, I, horizon), never pi; islands not fixed by the horizon
are censored. Scoring: held / failed / partial, with the number, in `runs/auctions.md`.

Scoring conventions fixed here (engineer, before any run): "instances" in Part A are the enumerated instances of the
stated family (AM: all 1,000; AM+: a fixed-seed subsample of 3,000 of 10,000, unless the full run is cheap, in which
case all, and the count is stated); fractions are over instances with the stated precondition. Part B percentages are
fractions of (run, island) pairs pooled over 40 runs x 64 islands, with the run-level spread also reported. "Pair
islands" = islands whose end state is classified `pair` (an enforced or unenforced joint deviation played on the
island); "policed" = `POL` fixed in role P; labels may overlap. Prediction 8's "never tested" is evaluated over
policed, fixed islands only. Prediction 11's "driven out" is evaluated over islands whose founding set contained both
POL in P and at least one PAIR or PAIRU in each item role.

## Predictions (the RE's; falsifiers in brackets)

1. *Substitutes control:* VCG is in the core on 100% of substitutes instances and truth is notion-robust under VCG in
   every mode and tie [any break].
2. *VCG, AM, R1, T-strict:* truth fails exactly where v_P > min(v_A, v_B). Both item bidders bidding at least v_P
   zeroes both VCG prices, whether they lose at truth (losers' collusion) or win (winners' joint overbid; corrected
   after the second review, which found the first draft's prediction missed winners). With P passive this was checked
   by the RE at 0/1,000 mismatches; with P's T-strict response the prediction is the same [a mismatch on more than 1%].
3. *Surcharge, AM, R1, T-strict:* the losers' collusion never profits, and truth fails by singleton shading on every
   instance with a positive surcharge, up to grid granularity [losers' breaks > 0, or singleton breaks on fewer than
   80% of positive-surcharge instances (lowered from 95% after review: one-tick surcharges may admit no profitable tick)].
4. *Spite (T-weak, R1):* deters at least 80% of the T-strict breaks under both VCG and the surcharge in AM
   [below 50%].
5. *Coalitional responses (R2):* the complement's own ring makes leader values exceed the joint marginal
   contributions, and the first-price notion core is empty on most AM instances [nonempty on more than 50%].
6. *Bernheim–Whinston through the notion (first-price, R1, T-weak):* where nonempty, the notion's payoff vectors lie
   within one tick of the bidder-optimal core frontier on at least 90% of instances [below 70%]. Low confidence: the
   one-round truncation may admit more.
7. *Ecology, collusion instance, VCG, no audit, prior U:* islands playing the losers' overbid (enforced `PAIR`) are at
   least 30%, and policed islands at least 20% [pair below 10%, or police below 5%].
8. *Police are a shadow:* on policed islands without migration, the police was never tested on most of them
   (more than 50%), and removing `POL` from the prior raises pair islands by at least 1.5× [a smaller rise].
9. *Surcharge rule:* pair islands under 2% in the collusion instance (the overbid does not profit, so `PAIR` plays
   truthfully); in the threshold instance, islands playing a winners' deviation (`PAIR`, `PAIRU` or `SH` in A or B) at
   least 40% [collusion ≥ 5%, or winners' deviations below 20%].
10. *The audit:* with the reading audit, enforced pairs and police are 0 by construction, and in the collusion
    instance VCG revenue with the audit is at least that without it [lower with the audit]. Narrowed after review: the
    threshold instance is reported without a prediction.
11. *Demography (prior M):* pair islands rise by at least 1.5× against prior U, and wherever `POL` founded with a
    deviating pair, the pair is driven out in at least 70% of islands [below 50%: the policing seen under U would then
    be demographic].
12. *Tremble (commit before the tremble):* at a 5% failure rate `POL`'s expected payoff against an enforced pair is
    below `T`'s in the VCG collusion instance (committed spite is safe only under certainty) [`POL` ≥ `T`].

## Scoring conventions added by the engineer (before any code or counted cell)

These fix readings the spec leaves open; each is repeated in `notes/auctions-run.md` §3.

- **Response graph.** T-strict uses the best-reply graph with strict-improvement moves only (an indifferent responder
  stays put), picks the pure Nash equilibrium of the closure closest to the complement's truthful reports in L1
  (ties by the lexicographically smallest report vector). T-weak ("spite counts") uses the closure of the graph in
  which a responder may move to *any* best reply, including a payoff-equal one, and takes the equilibrium worst for S.
  The literal reading (strict graph for both ties; spite reachable only through strict improvements) is reported as an
  extra row, "T-weak-literal", and is not the scored one for predictions 3 and 4. Under R2 the response set is the
  set of maximizers of the complement's total payoff for both ties.
- **Deviations** d_S exclude the truthful report of S (a coalition that reports truthfully has not deviated); the
  leader value v(S) (Bernheim–Whinston check) maximizes over all d_S including it.
- **Prediction 2 and 3 "instances".** Over all 1,000 AM instances; "mismatch" = an instance where
  (truth fails) differs from (v_P > min(v_A, v_B)) under VCG, R1, T-strict. Prediction 3's "positive surcharge" is
  evaluated at the truthful reports.
- **Prediction 4.** The share of instances (and of (instance, coalition) breaks) broken under T-strict that are not
  broken under T-weak, per rule, in AM, R1.
- **Prediction 5.** "First-price notion core" = the set of reporting profiles with an efficient (true-value)
  allocation giving every proper S at least v(S) under R2 (T-weak and T-strict reported; the verdict uses the larger
  nonempty fraction, which favours the prediction's falsifier).
- **Prediction 6.** "Within one tick" = L-infinity distance on the integer grid between the bidder-payoff vector and the
  nearest Pareto-maximal integer point of the true-value core; an instance counts if **every** payoff vector of its
  notion set is within one tick (the "some vector" version is reported alongside); verdict under T-weak, R1,
  first-price, AM (1,000 instances); instances with an empty set are excluded from the denominator.
- **Part B percentages** are pooled over (run, island) of absorbed-or-censored islands; censored islands are counted in
  the denominators and reported separately. `pair` = the probability that the two item bids equal the pair's joint
  deviation report (enforced or unenforced) is at least 0.5 in the island's end state; `items deviate` = the
  probability that either item bid differs from truth is at least 0.5; `policed` = `POL` is the only program of role P.
  Prediction 7's "enforced PAIR" is scored on the `pair` label; the enforced-only share is reported alongside.
  Prediction 8: "never tested" = after `POL` became the only P program, no generation (sampled each generation)
  had a `PAIR` in both item roles or `PAIRU` in both; the founding-state exposure is reported separately.
  Prediction 11: "driven out" = the island is not a `pair` island at the end; the stricter "joint deviation
  probability = 0" is reported alongside, over islands whose founders included `POL` and a `PAIR` or `PAIRU` in each
  item role.
- **Prior M:** the item priors equal U (1/4 each); `POL` mass is set to f(`PAIR`)² = 1/16 and the remaining 15/16 is
  split equally between `T` and `SH` in role P.
- **Prediction 12** is computed on the tremble tensor (commit before the trembling member's failure) at 5%, VCG,
  collusion instance, against an enforced pair, with `T` for comparison.
