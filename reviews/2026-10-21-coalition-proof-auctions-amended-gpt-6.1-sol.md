# Review of `specs/2026-10-21-coalition-proof-auctions.md` by gpt-6.1-sol

## 1. Errors, contradictions, unsound mechanisms

- **Tremble cannot produce the stated loss.** “P’s best replies to the items’ resolved bids” conflicts with “spite can then make P win at a loss.” With realized bids observed, P can bid zero and obtain nonnegative payoff; a loss-making bid is not a best reply. **Fix:** distinguish an observed-tremble arm from a commitment-before-tremble arm. Only the latter tests risky spite.

- **Grand-coalition gain is misstated.** “Its gain equals the seller’s revenue at truth, under every rule” fails for integer-grid first-price. In the collusion instance, preserving P’s efficient win requires a positive bid: all-zero bids allocate to both item bidders. **Fix:** optimize the grand coalition explicitly; revenue is an upper bound, attained only with efficient allocation and zero payments.

- **Audit definition contradicts information access.** “Programs whose bids read another bidder’s program” supposedly includes `POL`, but P is “conditioned on the items’ resolved bids,” not their sources. **Fix:** define an audit of inter-bidder information access, or implement source-reading POL and distinguish it from observable-bid response.

- **R1 is not exhaustive.** “All best-reply paths up to 50 rounds” can miss reachable equilibria. **Fix:** compute reachable states to closure in the finite best-reply graph; specify asynchronous updates, whether indifferent moves count, and unresolved/no-equilibrium treatment.

## 2. Design flaws and confounds

- **The menu does not establish ring enforcement.** `PAIR` recognizes a class label, but there is no general unilateral bid mutant that exploits an accepted partner. Joint TU optimization also need not benefit each separately selected role. **Fix:** include every constant bid as an invasion diagnostic; report both members’ gains and implement transfers if TU is intended dynamically.

- **The matched prior does not match founding events.** “P(`PAIR` in A)·P(`PAIR` in B) equals P(`POL` in P)” matches one sampled triple, not presence or abundance among 100 founders per role. **Fix:** match actual founder-count distributions or coalition-establishment probabilities. Specify the remaining prior masses.

- **The Bernheim–Whinston check changes the object.** Single-minded scalar bids, reachable complement Nash responses, and one-round leader-value inequalities are not automatically the menu-auction coalition-proof theorem. **Fix:** verify theorem assumptions and label this a comparison between distinct solution concepts, not a replication.

- **One population size cannot characterize a large-population limit.** **Fix:** add a small N sweep, report unresolved islands, and separate absorption probabilities from 2,000-generation censoring.

## 3. Predictions likely wrong

- **Prediction 2 misses existing winners’ overbids.** Take AM values `(10,6,6)`. Both item bidders already win, paying 4 each. Joint reports `(10,10)` make both VCG payments zero. P’s truthful bid remains a best reply and is selected by T-strict. **Prediction:** substantial breaks also occur when item bidders win truthfully.

- **Prediction 12 is impossible under the specified adaptive POL.** Its realized best-reply payoff weakly exceeds truthful P’s payoff at every realized item-bid pair. **Prediction:** `POL ≥ T` under observed trembles.

## 4. Missing controls or cheap additions

Add all constant-bid invasion tests, actual POL-removal cells required by prediction 8, no-reading matched-bid controls, and overlap-aware behavioural labels: “policed” and “pair played” need not be mutually exclusive.

## 5. Alternative explanations not ruled out

Named-class coordination, neutral drift among behaviourally identical programs, founder abundance, sequential information advantage, and finite-time censoring can explain the ecology without genuine coalition enforcement or a general source-reading advantage.
