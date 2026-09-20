# Ultimatum game verdicts — written 2026-09-19, before the first run

Settings: k = 3 levels L = 0.2 < M = 0.5 < H = 0.8; proposer plays the offer,
responder the threshold, accept iff offer ≥ threshold, payoffs (1−x, x),
rejection (0, 0).  Weak arm, n = 5, N = 100, w = 0.1 (the calibrated w has
no single value under the exponential map; 0.1 is the fallback), fitness
exp(w·payoff), Moran-fixation chain.

## (a) ROLE arm (one population, roles drawn)

Every constant A_i is strictly stable: a lower-threshold/lower-offer mutant
has its offers rejected by incumbents, a higher one rejects the incumbents'
offers.  **Verdict:** π spread across all-L, all-M, all-H with no
concentration, on-path rejection rate 0.
**Falsifier:** any concentration > 0.6 on one level.

## (b) fixed-mutual (two populations, both weak)

**Verdict:** concentration on (M, M) — the Nash bargaining solution from the
disagreement point (0, 0) — with on-path rejection 0.  Proposer share 0.5.
**Falsifier:** mode not (M, M).

## (c) fixed-one-sided (blind responders, sighted proposers)

**Verdict:** responders concentrate on threshold H, proposers accommodate at
offer H; responder share 0.8, rejection 0.
**Falsifier:** responder share < 0.7.

## Symmetry break (run after (a)–(c))

Responder outside option: rejection gives (0, 0.3).  Arm (b) only.
**Predicted:** the mode shifts toward H per generalised Nash bargaining
(maximise (1−x)(x−0.3): x = 0.65, nearest level H).  Report whether it
moves and which way.
