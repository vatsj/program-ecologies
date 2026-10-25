# Review of `specs/2026-10-25-pricing-rules.md` by gemini-4-argon

**1. Errors, contradictions or unsound mechanisms**

* **F+A charge definition vs. partial-cap timeouts:** "a timed-out read is charged $c \cdot K$ *in place of* its own steps" vs. "Tests cover partial-cap and nested timeouts." If the capped simulator primitive allows a caller to pass a sub-budget $b < K$ (a partial cap), charging the root cap $c \cdot K$ on timeout makes a cheap probe ($b = 100$) pay the entire root cap ($K \ge 10^4$) if its target loops, turning bounded probing into a catastrophic penalty. Conversely, if the simulator primitive always uses a fixed cap $K_{sim}$, then "partial-cap" is undefined. **Fix:** Specify whether the simulator primitive takes a budget argument $b$, and whether F+A charges $c \cdot K$ (root cap) or $c \cdot b$ (the call's cap) on timeout.
* **B-own state vs. cache keys:** "keyed like B's cache (the reader's quote and the read program's quote, both with their carried certificates)... The memo is part of the program's state". If the memo is part of the program's state, and the quote includes the program's state (as carried certificates do), updating the memo changes the quote, invalidating all keys. **Fix:** Explicitly state that the memo is runtime metadata excluded from the program's quote/source representation (unlike certificates).
* **B and B-own in the cut list:** The Addendum says to run B-own "at the same price levels and cells as B, paired with it," but fails to update the Required Outputs (which still say "the three rules' charges" instead of five) or the Budget cut order. **Fix:** Update the test spec to all five rules (F, A, F+A, B, B-own) and keep B and B-own paired in the cut order.

**2. Design flaws or confounds**

* **Statistical power vs. strict interval scoring:** Scoring requires the 95% confidence interval to lie *strictly above* the threshold ("met if the interval lies above the threshold... *undetermined* otherwise"). In the PD, the target is $0.70$, the baseline is $0.75\text{--}0.95$, and $n = 20$ runs. At $n = 20$, even $18/20$ ($0.90$) has a 95% binomial lower bound around $0.68\text{--}0.70$, meaning true $0.85$ performance will almost certainly be scored *undetermined*, guaranteeing no rule finds a joint band by a sample-size artifact. **Fix:** Either increase PD runs to 40, or score "met" by the point estimate $\ge$ threshold (reporting the 95% CI alongside to flag borderline cases).
* **Endogenous certificate production and B/B-own:** In the PD under S-nonself production, a program's carried certificate list changes when it produces a new certificate. Because B and B-own key on `(reader_quote, target_quote)` *including carried certificates*, any certificate acquisition by either party invalidates the cache for all pairs involving that party. If production happens mid-scramble, cache misses will be much higher than a static pair analysis suggests. **Fix:** Log cache invalidations due to certificate updates separately from first-encounter misses so you can tell whether B/B-own actually amortize during the scramble.

**3. Predictions you think are wrong**

* **Prediction 6 (B-own within 0.1 of B in PD at $c = 10^{-3}$):** Likely wrong if founders start with cold memos. In B, the *first* copy of FairBot on an island to check a partner subsidizes all its sibling copies on that island immediately. In B-own, *every* distinct founder copy (and every immigrant) must pay the $20\text{--}40$ verification cost out of pocket against every partner type before its lineage inherits the memo. At $c = 10^{-3}$ (cost $\approx 30$ vs. stake $2$), that initial per-founder toll can kill establishment in the scramble before inheritance kicks in. **My prediction:** B-own falls well below B (by $> 0.1$) at $c = 10^{-3}$ unless founders start with pre-warmed memos.

**4. Missing controls or cheap additions**

* **Log B-own memo size:** Since offspring inherit the parent's memo and migrants carry it across islands, memos will accumulate keys over the whole run. Log mean/max memo size per program to verify it doesn't blow up memory in PD runs.

**5. Alternative explanations**

* Nothing material.
