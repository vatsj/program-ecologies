# Review of `specs/2026-10-21-core-rediscovery.md` by gpt-6.1-sol

## 1. Design flaws/confounds → fixes

- **Prediction 1 is false for the specified strategy space.** In the threshold instance, bids `(P,A,B)=(24,12,13)` form a pure Nash equilibrium: revenue is 25, allocation efficient, and neither winner benefits from shading into a random tie. P cannot profitably win and is indifferent among losing bids. This exceeds minimum-core revenue by five ticks. Bernheim–Whinston’s coalition-proof/menu-auction result does not establish the claimed ordinary-Nash statement. **Fix:** retain unrestricted bids as one arm, add a no-overbidding arm, and distinguish ordinary Nash, coalition-proof equilibrium, and minimum-revenue-core outcomes.

- **`PRU` is neither fully specified nor necessarily prudent.** Default `c>v` can win at a loss. For an item bidder, the profitable winning threshold depends on its teammate’s bid: A must beat `b_P−b_B`, not simply the opposing allocation’s total. Simultaneous iteration can cycle; taking iteration 20 manufactures a cutoff-dependent game rather than executing mutually source-reading programs. **Fix:** specify role-specific functions, cap defaults at value, handle zero-bid/tie cases explicitly, and define a terminating evaluator. Treat cycling profiles separately; test cutoff and update-order sensitivity.

- **Revenue proximity does not establish core membership.** Wrong allocations, negative bidder utility, or asymmetric payments violating coalition bounds can pass the revenue test. **Fix:** evaluate the full realized seller-and-bidder payoff vector against every true-value core inequality; separately report efficiency, individual rationality, minimum revenue, and distance to Vickrey-nearest.

- **Censoring and the asymptotic object are mismatched.** Persistent rain generally prevents absorption; genotype fixation need not imply behavioral stability with reactive programs. One population size cannot support large-population conclusions. **Fix:** report fixed-horizon outcomes for all islands without dropping censored cases, plus absorption statistics for mutation-free arms. Add a small N sweep and distinguish finite-time results from stationary or limiting claims.

## 2. Predictions likely wrong

- **3: ≥90% efficiency in every arm is too strong.** Separate item bidders face a coordination/threshold problem; package dominance can persist even when joint item value is higher. I predict appreciable inefficient package wins in some constant-only cells, especially asymmetric ones.

- **4: “Two threats erode faster” is not identified.** The collusion instance also changes winning coalition size, value ratios, and coordination requirements. Two neutral threats need not decay faster in aggregate. I predict no robust ordering without matched controls.

- **5–6: restoration percentages lack a mechanism-based basis.** Finite annealed injection need not leave a durable threat; prudent programs can be replaced neutrally by their constant shadows. I predict transient restoration followed by renewed vulnerability, not guaranteed endpoint recovery.

- **8: migration’s sign is unsupported.** Bidder-payoff-weighted migration can favor low seller revenue. I predict dependence on the exact migration weighting and role, not merely `PRU` presence.

## 3. Missing controls / cheap additions

- Inject a known profitable outbidder into representative eroded states; measure establishment and downstream revenue.
- Match `PRU` against constant defaults and a non-source-reading response oracle to separate response capability from source access.
- Report founder coverage, support and transition structure, encounter-level threat distributions, and uncertainty clustered by run.
- Enumerate grid points near Vickrey-nearest before interpreting its observed frequency.

## 4. Alternative explanations not ruled out

Overbidding threats, random-tie discontinuities, founder availability, negative-fitness handling, transient coordination failure, and migration favoring bidder surplus could explain outcomes attributed to rediscovering—or losing—the core.

## 5. Beyond this experiment

Nothing material.
