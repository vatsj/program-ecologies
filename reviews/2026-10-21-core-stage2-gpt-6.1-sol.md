# Review of `specs/2026-10-21-core-stage2.md` by gpt-6.1-sol

### 1. Design flaws/confounds and fixes
- **Rounding already breaks the proposed statics.** In skew, `TX(14)` against two `F(0.5)` programs produces bids `(8,8)`: revenue 16, two ticks above the minimum core revenue 14. For threshold, rounding 10.5 can instead produce `(10,10)` and a revenue tie, or `(11,11)` and two-tick overpayment. **Fix:** specify exact rounding, exhaustively enumerate statics before dynamics, and revise prediction 1. Coordinated rounding would require an explicit additional convention.
- **“Sucker-depleted rain” is undefined and causally confounded.** Whose threat and which share determine eligibility when P and follower populations are polymorphic? Removing low constants also directly raises item bids, potentially manufacturing core outcomes independently of prudence. **Fix:** define the distribution precisely; retain a common founding state; pair replacement counts and timing; measure TX’s selection advantage against matched constant-P programs, not just core frequency.
- **Island-mean core membership can conceal non-core encounters.** Rain and migration specifically create polymorphism. **Fix:** make encounter-level core probability and efficiency primary alongside mean-vector core membership. Report their discrepancy.
- **N = 100 cannot establish large-population behavior.** Treat this as a mechanism experiment, not limit evidence. Add a small N panel with explicit scaling of mutation, migration, and observation horizon.

### 2. Predictions I think are wrong
- **Prediction 1 fails deterministically**, as above.
- **Prediction 3 does not follow from follower-class fixation.** Two followers need not have complementary δ values; clipping and rounding can also leave their total below the threat. I predict appreciable TX wins on some follower-only islands. Condition the shadow prediction on the actual δ pair and resulting bids, not merely class fixation.
- **Prediction 7’s 10% bound lacks a selection argument.** Untested above-value threats incur no cost and can survive neutrally; their share depends on the unspecified unrestricted cap and prior. I predict depletion among repeatedly loss-making threats, but potentially substantial survival among deterrent bluffs.
- **Prediction 4’s numerical improvement is unsupported.** Rain supplies upward threats but also low threats that followers immediately accommodate. I predict the direction depends on relative invasion rates, not sucker supply alone.

### 3. Missing controls or cheap additions
- Add a **matched `TX(t)` versus constant `c=t` comparison**. Followers respond identically to them, isolating the payoff benefit of exploitation from certified deterrence.
- Split rain into **P-only and item-only** arrivals, preserving per-role arrival rates where applicable.
- Record threat-frequency trajectories, payoff differences, fixation times, and mutation/migration-driven replacements. A final threat distribution cannot distinguish scramble selection from subsequent drift.
- Predefine split scoring at revenue 15 in skew versus the reference edge at 14. The listed 9.5 midpoint is unreachable as an integer encounter payment; report distances as well as exact matches.
- Reverse-order tests should use independent fresh evaluation, not cached outputs.

### 4. Alternative explanations not ruled out
- Core recovery could reflect followers’ hard-coded `t+1` payment rule rather than evolutionary discovery of core constraints.
- Apparent threat “freezing” could be neutral fixation, survivor conditioning, or a finite observation window.
- Modal splits could reflect δ-grid multiplicities, clipping, and rounding rather than bargaining focal points.
- Order independence establishes an acyclic dependency architecture, not general mutual-source-reading semantics.

### 5. Ideas beyond this experiment
nothing material
