# Review of `specs/2026-10-21-hooks-followups-weak.md` by gpt-6.1-sol

### 1. Errors or unsound mechanisms

- **The amended PD promise cannot bootstrap the mechanism being tested.** Original contracts accept “(D, D) → (C, C) between two default defectors”; the amendment requires “the partner provably cooperates with me” and says this is “evaluated before the new fill is written.” Two current defectors fail that predicate, so the joint promise cannot activate. **Fix:** specify whether eligibility uses pre-write or jointly amended programs. If pre-write, describe this as a different contract technology, not merely removal of parochial keys. If post-write, specify a sound proof/evaluation rule; do not select a cooperative fixed point by fiat.

- **Response evaluation is not response implementation.** The amendment computes “its best wage in {0, ¼, ½} (a single wage fill the boss could hold),” but never says the boss adopts or executes that fill. Hypothetical worker gains can therefore authorize contracts whose realized encounters remain strikes. **Fix:** explicitly distinguish a valuation-only oracle from an implemented response mechanism; log predicted versus actual wages. For boss–worker contracts, define whose payoff must improve and whether the boss can overwrite its own contracted wage.

- **The acceptance baseline remains undefined.** “Both workers are at least as well off under that response” does not specify comparison against actual current play or the boss’s best response without the candidate. **Fix:** define both counterfactuals, holding other fills and conflict resolution fixed. These are different rules.

### 2. Design flaws or confounds

- Replacing lineage keys with effective-behaviour predicates changes scope, verification, activation timing and possibly endogenous self-reference—not just parochialism. History predicates may also change when the history fill itself changes behaviour. **Fix:** freeze explicit snapshot semantics and add a matched pre-write-eligibility lineage control. Record proposal, eligibility, acceptance and activation rates.

- The main union cell changes union availability and union valuation together. The amended boss–worker-only (C) control does not substitute for an exactly matched union-(M) cell. **Fix:** retain identical union proposals, priorities and supersession rules under M and C; name all cells explicitly.

- Fixed-size, finite-horizon lottery outcomes cannot establish large-population efficiency or permanent survival. **Fix:** restrict conclusions to these lotteries; cheaply add one larger size and longer-horizon continuation of unresolved runs. Report support and transitions, as required by CLAUDE.md.

### 3. Predictions likely wrong

- **Predictions 1–3:** recovery to universal-open ≥0.65–0.7 is unsupported after amendment 1. Pre-write eligibility blocks cooperation-creating DD contracts and may merely subsidize existing cooperators. I predict substantially fewer eligible/active contracts, not necessarily restored universality; the original static-class counter-prediction is now obsolete.

- **Prediction 4’s rationale:** “a joint strike demand is never a myopic Pareto improvement” is too strong. Conditional programs or existing fills may change the wage during encounter reevaluation. I predict rejection against constant nonconceding bosses, but potentially acceptance against responsive bosses. Enumerate hand cases before retaining “never.”

- **Prediction 5:** rare executed strikes do not follow from valuation-only best responses. I predict a response gap unless wage adaptation is actually implemented.

### 4. Missing controls or cheap additions

- Exhaustively tabulate candidate demands against every boss wage, including ties; rerun ties against paying the demand.
- Report proof failures, predicate changes, overwritten fills, adoption denominators and realized payoff changes.
- Score amended predictions separately from superseded ones.

### 5. Alternative explanations

Recovery could reflect suppression of contract formation rather than openness. Fair wages could reflect favourable tie-breaking, free counterfactual optimization or forced wage adaptation rather than evolutionary selection or credible threats.
