# Review of `specs/2026-10-10-identity-and-tags.md` by gpt-6.1-sol

## 1. Design flaws/confounds and fixes

- **Connected components are not pooled cooperation families.** Mutual cooperation is non-transitive: a bridge joins two incompatible clubs into one component. Your definition therefore merges precisely the rivals whose separation you want to measure, making “universal,” “patchwork,” and largest-family counts misleading. **Fix:** retain the compatibility graph; distinguish pairwise-compatible sets, bridge-mediated connectivity, and actual occupied supports. Define universal cooperation directly by cross-island \(P(C,C)\), alongside open-carrier occupancy.

- **Identity makes spelling lumping suspect.** Two extensionally identical identity bots cooperate with their own spelling but defect against each other. Tags likewise distinguish otherwise equivalent sources. **Fix:** establish lumpability against every source-sensitive opponent, including within-class interactions. Preserve exact identities where necessary; a class payoff table cannot substitute for identity frequencies. Apply this to both the lottery and chain.

- **The proposed AND bridge does not bridge the stated rivals.** A tagged AND carrier requires its opponent to carry the tag; the untagged open CB does not. The tagged OR carrier can bridge, but cooperates with tagged defectors. **Fix:** hand-check reciprocal plays among CB, both carriers, marked/unmarked tag clubs, and marked D before declaring any bridge non-exploitable.

- **The tilts do not isolate pooling.** Increasing one spelling’s mass also changes its local copy concentration, establishment probability, and the remaining composition. **Fix:** compare equal total mass allocated to one identity versus multiple mutually incompatible identities versus compatible carriers, with matched costs and paired placements. Record per-island founder counts, not just global totals.

- **Horizon 2,000 cannot establish permanence or large-population universality.** Bridge survival and resolution times may scale with \(N,I\); only two sizes are tested. **Fix:** classify unresolved runs as censored, estimate separation/resolution hazards, and extend separated runs. Label the scaling panel finite-size evidence.

## 2. Predictions likely wrong

- **Prediction 3’s rationale is reversed.** T1 concentrates a whole family’s mass into one mutually compatible identity, eliminating its supposed inability to pool *within that intervention*. In a mutation-free lottery, mutant incompatibility is irrelevant. I predict substantially stronger clique performance under T1; the 0.7 carrier threshold is unsupported.

- **Prediction 4:** the AND bridge fails the untagged-CB test; the OR bridge admits tagged exploitation. I predict compatibility and persistence will depend on which bridge actually exists, rather than tags generically guaranteeing resolution.

- **Prediction 2:** largest global seeded count need not predict establishment or victory. Spatial placement, founder thresholds, and exploitation matter. I predict effective established mass will outperform raw counts as a predictor.

- **Prediction 6:** more islands improve bridge availability but also sample more incompatible establishers and require more resolutions. I predict no unconditional monotonicity at a fixed horizon.

## 3. Missing controls/cheap additions

- Run identity-only, tags-only, and named-CB-only ablations; pair random seeds.
- Report cross-island \(P(C,C)\), establishment-conditioned founder counts, and bridge extinction times.
- Specify normalized spelling weights, marker multiplicity/cost, and marked-source certificate behavior.
- Do not remove the OR bridge or second tag based on catalogue size without treating the reduced grammar as a separate experiment.
- Predefine threshold decisions: prediction and falsifier ranges currently leave unclassified gaps.

## 4. Alternative explanations not ruled out

Apparent pooling could instead reflect favorable establishment payoffs, demographic concentration, checker privileges, or grammar-induced prior mass. Apparent bridge-less permanence could be slow migration-mediated replacement rather than impossibility.

## 5. Broader research-program ideas

nothing material
