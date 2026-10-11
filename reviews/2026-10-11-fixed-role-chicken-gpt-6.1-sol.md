# Review of `specs/2026-10-11-fixed-role-chicken.md` by gpt-6.1-sol

### 1. Design flaws/confounds and fixes

- **Strict action equilibria are not strict program equilibria.** Many readers can match a constant’s on-path action and invade neutrally, then change the opponent’s incentives. Thus “strict Nash ⇒ π on two conventions” does not follow. **Fix:** derive invasion/drift closure in program space, retaining distinct sources and neutral twins. Use the audited closure-seeded, log-domain solver; verify candidate traps without threshold pruning.

- **The lottery and migration law are underspecified.** Specify founder counts, sampling with/without replacement, class prior masses, role-wise independence, migration topology, role preservation, migrant replacement, and whether emigrants are payoff-weighted. Define generations and the fitness map—especially with negative hawk–dove payoffs. Otherwise demographic and selection effects cannot be separated.

- **Outcome classes can hide distinct ecological mechanisms.** A polymorphic population may implement a perfect one-sided convention; conversely, two monomorphic readers may crash. Classify by role-conditioned action probabilities and payoffs, separately from genotype diversity. Predefine convention tolerances and establishment/persistence criteria. Cross-island loss must preserve roles and specify its efficiency benchmark.

- **The large-population claim is unsupported by the lottery panel.** N = 100 and horizon 2,000 test one finite-size snapshot. Add a small N panel and doubled horizons; report censored resolution times. Explicitly separate the rare-mutation limit from mutation-free absorption.

### 2. Predictions likely wrong

- **Prediction 3’s bistability inference and \(1/N\) exit law are unjustified.** Neutral entry at \(1/N\) need not produce a successful convention switch: the next edge can be selected against or lead to a polymorphic trap. Predict neutral neighborhoods around conventions, with exit scaling determined by the complete escape path—not necessarily \(1/N\).

- **Prediction 2 overstates what “bridges” imply.** Swerve-against-straight/straight-against-swerve behavior against constants does not establish compatibility with other readers. Identical deterministic readers without a public asymmetric signal cannot anti-coordinate in self-play. Predict possible migration-induced polymorphism, crashes, or persistent patchworks; require the full bridge–resident and bridge–bridge tables before predicting merger.

- **Prediction 5’s quantitative slowdown lacks a mechanism.** Increasing C changes basin geometry and selection during mixed encounters, not merely crash-state exit rates. Neutral paths could remain unchanged. Predict lower crash exposure, but no universal twofold slowdown or invariant convention frequency.

- **Prediction 1’s patchwork threshold is weak evidence.** With 64 independent islands and roughly balanced convention probabilities, seeing both conventions is almost automatic. Report per-island establishment probabilities; distinguish the RS’s qualitative claim from the stronger ≥0.9 forecast. Align success thresholds and falsifiers, or label the gaps inconclusive.

### 3. Missing controls / cheap additions

- Constants-only two-population control: does ordinary anti-coordination already explain the norms?
- Matched grammar/prior control for weak versus modal arms, plus paired seeds.
- Forced opposite-convention islands, with candidate bridges included versus removed at matched founder mass.
- Role-swapped runs to detect implementation asymmetry.
- Report mutual-dove separately: in both hawk–dove tables it is Pareto-efficient and has the same total payoff as either pure convention. Convention frequency is not an efficiency statistic.

### 4. Alternative explanations not ruled out

Demographic founder imbalance rather than learned commitment; prior mass rather than provability; migration-driven demographic takeover rather than reader mediation; transient synchronization mistaken for absorption; cutoff-specific availability of accommodating programs.

### 5. Broader research ideas

nothing material
