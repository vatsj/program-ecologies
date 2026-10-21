# Spec: coalition-proof auctions: the RS's notion on package auctions, and rings versus police among open-source bidders, 2026-10-21

Status: draft by the RE; reviewed by gemini-4-argon, then by gpt-6.1-sol (`--mode amended`), both folded [after review]; to be reviewed sequentially (done); to be run
by a Sonnet subagent. Run under the RS's 24-hour autonomy window (2026-10-21), on the RS's request ("take a swing at my
idea for coalition-proof auction theory": VCG is not coalition-proof; our equilibria encode social choice; do they
suggest a refinement of VCG, ideally a side-payment rule, that buys coalitional robustness?). Theory, literature and
worked examples: `notes/coalition-proof-auctions.md` (read it first; §n below refers to it). DEFERRED 14 and 15.
REJECTED.md checked: the first entry ("Response-function equilibrium") is the RS's notion's ancestor and was re-opened
as a static menu in DEFERRED 15; nothing new re-opened here (this is a static diagnostic plus an ecology, not a
proposal to adopt the notion as the object).

## Why

The note derives the surcharge rule (VCG plus the minimal surcharges that pay no group of bidders more than its joint
marginal contribution, the VCG-nearest minimum-revenue core point) from the RS's notion with the seller as a player,
and argues three things that need numbers. (a) On the *reporting* game the notion's verdict turns on the tie rule
(whether an indifferent loser's spiteful overbid counts as a credible response) and on who responds (singletons or the
complement as one coalition). (b) The Bernheim–Whinston route (coalition-proof equilibria of the first-price package
auction give the bidder-optimal core) should reappear through the RS's notion with singleton responders. (c) In an
open-source auction, ring enforcement and collusion policing are the same program shape, and which holds an island is
a selection question. Rings are expected to win where no police are seeded, since a ring is cooperation among bidders
against the seller.

## Part A: the notion on small package auctions (static, exhaustive)

**Families** (two items A, B; single-minded bidders; integer true values on 1..G, G = 10; every instance enumerated
unless stated):
- *AM*: bidder 1 on AB, bidder 2 on A, bidder 3 on B (1,000 instances).
- *AM+*: AM plus bidder 4 on A (10,000; may subsample 3,000 with a fixed seed, say so).
- *Substitutes*: bidders 1, 2 on A and bidders 3, 4 on B (no package bidder; VCG is always in the core: a control).
- *Two packages*: bidders 1, 2 on AB, bidders 3 on A and 4 on B.

**Reports**: one bid per bidder on its own package, on 0..2G (overbids allowed). Winner determination maximizes
reported welfare; ties go to the allocation with more winners, then to the lowest bidder indices (state the rule).

**Rules**: VCG; the surcharge rule (minimum-revenue core w.r.t. reports, VCG-nearest in Euclidean distance, computed by
LP then QP over all blocking coalitions; check it against the closed form in the AM family); first-price (winners pay
their bids).

**The notion (one-round truncation).** A proper coalition S of bidders deviates to a joint report d_S. The complement
responds, in one of two modes: *R1 singletons* [after review: defined as an equilibrium set], where the response set is
the pure Nash equilibria of the complement's subgame (d_S held fixed) in the closure of the finite best-reply graph from
the complement's truthful reports (asynchronous single-player moves to a best reply, strict improvements only; computed
to closure, not by path sampling); instances with no equilibrium in the closure are recorded as unresolved and reported
separately [after second review]; *R2
coalition*, where the response set is the complement's joint reports maximizing its total payoff. Over the response
set, the tie rule is either *T-weak* (the response worst for S's total; spite counts) or *T-strict* (the response
closest to truthful in L1; spite does not count). S profits if its total payoff after the response exceeds its
truthful total by more than 1e-9 (TU within S). The truthful profile is *notion-robust* under (rule, mode, tie) if no
proper coalition profits. The grand bidder coalition is reported separately, its best joint report optimized explicitly
(the ring of §4); the seller's revenue at truth is an upper bound on its gain, attained only when the efficient
allocation survives zero payments [after second review].

**First-price** [after review]: truthful bidding gives winners zero, so truth is trivially not robust; first-price
enters Part A only through the Bernheim–Whinston check below, never the truth-robustness table.

**Outputs (A).** Per family × rule (VCG, surcharge) × mode × tie: the fraction of instances where truth is notion-robust; the breaking
coalitions classified as losers only, winners only, mixed, or singleton; the share of breaks deterred only under
T-weak (spite-dependent deterrence) and the spiter's margin (how far below winning the spiteful bid sits); P(VCG in
the core) and the mean surcharge per family; revenue at truth per rule. **The Bernheim–Whinston check:** for
first-price under R1, compute leader values v(S) (S commits, R1 response, both ties) and the set of reporting
profiles whose induced allocation is efficient for true values and gives every proper S at least v(S); compare their
bidder-payoff vectors with the true-value core and its bidder-optimal frontier (distance in grid ticks). This is a **comparison** between the RS's one-round notion on
scalar single-minded bids and Bernheim–Whinston's coalition-proof equilibria of menu auctions, which are different
solution concepts; it is not a replication [after second review]; report seller revenue and bidder welfare separately for those profiles against VCG at truth
[after review].

## Part B: rings versus police among open-source bidders (seed lottery, fixed roles)

**Roles and values.** The AM roles: P (package bidder on AB), A, B (item bidders), one population per role per island.
Two value instances: *collusion* (P 20, A 5, B 5; P should win; the losers' collusion of §2 is available) and
*threshold* (P 20, A 15, B 15; A and B should win; the surcharge's free-riding is available). Bids on the integer grid
0..40.

**Programs** [after review: rewritten; the first draft's bids were undefined in places and its ring could not be
exploited]. Each conditional program reads only what is stated; resolution order is fixed: **item programs first**
(conditioned on the partner item program's source class), **then P** (reading the item programs' sources and
committing its bid to their *intended* bids). Trembles, where used, are realized after all commitments, so a response
committed to a pair's intended deviation can misfire [after second review]. The item pair is the deviating coalition
and P is the RS's responding complement. All deviations are computed per rule and per
instance, exhaustively on the grid:
- A and B roles: `T` (truthful); `SH` (unilateral: the singleton's best reply to truthful others under the rule in
  force: truthful under VCG, a shade under the surcharge and first-price); `PAIR` (enforced: iff the other item
  program is `PAIR`, play this item's half of the pair's best joint report against a truthful P, maximizing the pair's
  total **subject to each member gaining individually** (no transfers in the dynamics), with ties to the smaller total
  bid [after second review]; otherwise truthful; in the collusion instance under VCG this is the
  losers' overbid, in the threshold instance under the surcharge the winners' joint shade); `PAIRU` (unenforced: plays
  its half of that joint report unconditionally).
- P role: `T` (truthful); `POL` (police: reads the item programs and commits to the best reply to their intended bids
  that is worst for the items' total, i.e. the T-weak spite response; against truthful items it is truthful); `SH` (P's best reply to
  truthful items under the rule).
Under first-price, `T` is a sucker for every role (zero surplus when winning); first-price is a comparison arm, not a
test of truthfulness. The payoff tensor over role-program triples is computed and committed before the dynamics.
**Prior**: uniform over named programs per role (U); a sucker-heavy prior with half the mass on `T` (S); and a
**matched-mass prior** (M) [after review] in which the expected initial encounter rate of an enforced pair,
f(`PAIR` in A)·f(`PAIR` in B) over founder frequencies, equals f(`POL` in P), with the remaining mass uniform over the
other programs of each role (state the masses), separating demography (a pair needs two slots, the police one) from
deterrence. Also **no-police cells** (`POL` removed, mass spread uniformly), required by prediction 8.
**Seller rules**: VCG; surcharge; first-price; each with and without the **reading audit** (programs whose bids read
another bidder's program are replaced by their non-reading default: `PAIR` and `POL` become `T`, while `SH` and
`PAIRU` are unchanged), the source-reading seller of §6.
**Dynamics**: the repo's fixed-role island seed lottery at ε = 0 (reuse the fixed-role chicken or SOG island kernel,
import only), N = 100 per role per island, 64 islands, w = 0.3, random role triples per encounter, 2,000 generations, with
islands not fixed by then reported as censored (not as outcomes); a small N sweep N ∈ {50, 100, 200} in the primary
cell (VCG, collusion instance, prior U) [after second review];
migration off (primary) and the stored mN rule (secondary); 40 runs per cell, paired founders across seller rules.

**Outputs (B).** Island end states classified behaviourally: pair (an enforced or unenforced joint deviation played on
the island), policed (`POL` fixed in P), truthful, shaded, or mixed, plus the program classes; revenue and efficiency per island (evaluations,
never selectors); time to fixation; for policed islands, whether the police was ever tested (a deviating pair present
while `POL` held P); the payoff tensor itself (static), with every pure Nash equilibrium of the three-role game;
**the tremble control** [after review]: `POL`'s payoff when one `PAIR` member fails to play its half with probability
0.05 after P has committed (spite can then make P win at a loss); **constant-bid invasion diagnostics** [after second
review]: for each resident triple and each role, every constant bid on the grid as a mutant, reporting which residents
a constant invades and each pair member's individual gain. Labels may overlap (an island can be both policed and
pair-playing).

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

## Required outputs

`src/auctions.py` (rules, winner determination, the notion) and `src/auction_islands.py` (+ `_run.py`, `_report.py`);
`tests/test_auctions.py` (AM closed forms; the payoff tensor's resolution order; the Ausubel–Milgrom numbers of §2; the 2XL leader values of §8, v = (10, 6)
→ 6.9 and 5.0 on a 0.1 grid; the surcharge equals zero exactly when VCG is in the core); `notes/auctions-run.md` (§1 the
static tables, §2 the ecology, §3 deviations from this spec); `predictions/2026-10-21-coalition-proof-auctions.md`,
committed before any counted cell; `runs/auctions/` (summary JSON, small CSVs; no `.npz` or large arrays). Hand back
draft paragraphs for RESULTS, REJECTED, THEORY and NOTATION; do not edit the shared docs.

**Scale guard.** ≤ 1 worker (three sibling runs are live, one using 3 workers in a detached batch); check `ps`
first; one job per process. **Waiting:** watch short commands; for long batches wait on one background command that
exits at completion, or end the turn with outputs on disk; never poll periodically.
