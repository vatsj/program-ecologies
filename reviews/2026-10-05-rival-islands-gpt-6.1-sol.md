# Review of `specs/2026-10-05-rival-islands.md` by gpt-6.1-sol

### 1. Design flaws/confounds and fixes

- **“Frozen separated” may mean metastable, not absorbing.** With ongoing migration and nonzero migrant fixation probabilities, certified separation need not freeze. Single-migrant deleteriousness does not establish stability under repeated arrivals. **Fix:** distinguish absorbing certificates, metastable separation, and horizon censoring; report transition hazards and survival curves. Specify migration topology, replacement rule, time units, and whether migration continues after certification.
- **The proposed scaling variable uses the wrong nucleation clock.** First-island \(T_{\rm nuc}\) is an extreme statistic that decreases with \(I\); it need not describe the period during which other islands remain vulnerable. Also, one successful immigrant can correlate islands without replacing an appreciable fraction of residents. **Fix:** record per-island establishment times, local-versus-immigrant ancestry, and migrant arrivals before local establishment. Test both arrival exposure and replacement fraction rather than assuming \(mN T/N\) controls independence.
- **The scaling design confounds \(N\) with \(I\).** Comparing only \((100,64)\) and \((400,16)\) cannot identify an \(N\)-scaling rule. Neither sequence establishes an \(I/N\to\infty\) result. **Fix:** complete the \(N\times I\) factorial and add at least one larger-\(I/N\) point.
- **Pre-seeding and stopping are underspecified.** State whether each pair gets a separate cell, whether forced islands replace iid islands, and how “held,” “first established,” and “efficient fraction” are defined. Preserve unresolved runs in denominators; do not analyze only successful freezes.

### 2. Predictions likely wrong

- **Prediction 1’s argument is insufficient.** A fixation probability below \(10^{-4}\) can still matter over \(10^5\) generations and many migration attempts; clustered immigration may behave differently from isolated mutants. I predict separation lifetimes depend strongly on migration flux and horizon, not merely whether \(mN\le10\).
- **Prediction 2 conflates prior mass with establishment success.** Effective establishment involves seed abundance, survival through the scramble, and access to still-unestablished islands. Early spread can amplify timing rather than prior mass. I predict majority shares track measured establishment-and-colonization rates better than raw family mass.
- **Prediction 3’s migration independence is doubtful.** Immigration can suppress rare local nucleation or rescue absent networks. Under genuinely independent trials with fixed positive establishment probabilities for two rivals, observing both approaches probability one as \(I\) grows—not enduring rarity.
- **Prediction 5 needs a restricted theorem.** Majority wins for two homogeneous, symmetric coordination types; family mixtures and additional types can change the threshold. Even in the symmetric case, near-ties can resolve slowly. I predict majority dominance in clean two-type merges, without a universal \(10^3\)-generation bound.

### 3. Missing controls or cheap additions

- Add \(m=0\), one-network pre-seeding, and exactly two homogeneous networks without iid background.
- Measure establishment rates using the actual iid background, not only all-D invasion.
- Record the full compatibility/payoff matrix and network transition counts.
- Natural separation needs multiple \(I\) values to test its claimed growth. With 100 runs, a 1–5% event yields only 1–5 observations; use binomial intervals and predeclared additional replication.
- Align falsifiers with numerical predictions: observing 0.75 separation already contradicts “at least 0.9,” despite passing the stated 0.5 cutoff.

### 4. Alternative explanations not ruled out

Finite-horizon persistence; migration-driven founder effects; neutral drift among compatible variants; invasion through intermediate programs; and ascertainment bias from selecting the heaviest rival pairs. Hypothetical uniform-mixing efficiency is a counterfactual, not realized island efficiency.

### 5. Beyond this experiment

The key asymptotic object needs three limits: population size, island count, and observation time. Characterize network-loss hazards along the proposed path; growing separation lifetime and eventual universality can coexist under different limit orders.
