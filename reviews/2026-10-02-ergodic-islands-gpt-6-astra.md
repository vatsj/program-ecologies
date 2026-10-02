# Review of `/Users/jstav/code/program-ecologies/.claude/worktrees/agent-a9c1c89dea343e9cb/predictions/2026-10-02-ergodic-islands.md` by gpt-6-astra

## 1. Design flaws/confounds and fixes

- **The patched chain is not a validated fixed-migration chain.** Most rates remain at their \(m\to0\) values, including potentially important reverse invasions and faker-drain routes. Stationary mass can be sensitive to these even when the three measured games agree. **Fix:** measure both orientations of the dominant stationary-flow edges, including C into fakers and D into C; propagate rate uncertainty through the stationary calculation. Label remaining patches exploratory.

- **The conclusions exceed the limits tested.** A takes \(m\to0\) before population growth; B tests finitely many fixed-\(mN\) cells; C uses finite mutation and finite observation windows. Agreement cannot establish “any split, any m, any graph” or inefficiency along every family. **Fix:** state separate, regime-specific conclusions. Likewise, cooperation above 0.2 or 0.3 falsifies a numerical prediction, not asymptotic inefficiency.

- **Adaptive stopping and censoring compromise the proposed intervals.** Ordinary Wilson intervals are not guaranteed to retain nominal coverage under success-count/time stopping. Excluding unresolved trials can bias fixation estimates. **Fix:** use fixed trial counts or sequentially valid intervals; bound fixation by treating unresolved trials first as failures, then as successes. Carry these bounds into patched-chain results.

- **The “static corollary” is not a full-chain bound.** \(\pi_R/\pi_D\approx\mathrm{entry}/(f+\mathrm{shadow})\) requires a validated reduction; indirect entrances and returns can invalidate the claimed inequality. **Fix:** derive the bound from full stationary-flow balance or present it only as a reduced-model prediction.

## 2. Predictions likely wrong

- **“Nothing structural sets the faker exit” is too strong.** Early branching survival is not global fixation. Local saturation, replacement competition, establishment on other islands, and spatial correlations intervene. Migration also changes reproductive opportunities, not merely offspring locations. **Prediction:** approximate branching constants at large N and rare migration, but finite-N and graph-dependent corrections—not exact structural invariance.

- **The \(mN=10\) well-mixed prediction is insufficiently justified.** Here \(m=0.1\); this alone does not imply mixing faster than selection, especially across graph families with different mixing times. **Prediction:** entry decreases toward well-mixed behavior, but neither the proposed numerical band nor the patched stationary mass is assured.

- **Lower mutation need not monotonically increase the faker:shadow island-exit ratio.** Neutral shadows also migrate, and faker supply itself depends on mutation and resident composition. Dominant-class switches need not represent successful invasions. **Prediction:** the direction is contingent; distinguish mutation-seeded from migration-seeded transitions before interpreting it.

## 3. Missing controls/cheap additions

- Add a small-\(m\) convergence ladder at one modest \((I,N)\), validating MC against \(\Phi_2\) for entry, faker, and a reverse edge.
- For selected C cells, start from all-R/all-FairBot as well as all-D. Half-window agreement from one initialization does not diagnose mixing.
- Test graph **equivalence** using uncertainty on rate ratios; overlapping intervals are not evidence of equivalence. Correct for the many cellwise verdicts.
- Monomorphic reduction is justified at finite connected \(I,N\), positive migration, and mutation tending to zero by eventual absorption—not by the limited coexistence checks. State this directly.

## 4. Alternative explanations not ruled out

- Modal superiority may reflect grammar/prior differences and the free oracle, not unfakeability alone.
- Finite-mutation cooperation may reflect persistent polymorphism and shadow pruning rather than monomorphic entry/exit rates.
- Apparent plateaus may reflect metastability or unresolved slow fixation.

## 5. Beyond this experiment

nothing material
