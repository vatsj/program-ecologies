# Review of `specs/2026-10-05-spoiler-conditioned.md` by gpt-6.1-sol

### 1. Design flaws/confounds and fixes

- **Forced seeds often test the wrong interaction.** FairBot plus a faker of `BOX(THEM(^C))` need not be a target–faker pair. Insert each faker beside its actual target; include FairBot only where exploitation of FairBot is verified. Define insertion as replacement at fixed N, specify how existing copies are handled, and pair treatment/control backgrounds.

- **Natural conditioning is not a causal spoiler estimate.** Faker presence correlates with target identity/count, other establishers, and background composition. Cells (ii) and (iii) also overlap when both faker types occur. Use four disjoint categories: none, non-establisher only, establisher only, both. Report target-specific/count-stratified estimates; reserve causal claims for randomized insertions.

- **The combined-bound formula is incomplete or mislabeled.** For unconditional natural-seed establishment, it generally needs a factor P(A), separate treatment of mixed/establisher-faker cells, and any establishment without A. A weighted decomposition fitted and checked on the same data is an identity, not mechanistic validation. Define the estimand and test predictions on held-out seeds.

- **The proposed conclusion exceeds the experiment.** Three cutoffs and two finite populations cannot establish a uniform-in-n discount or an “almost all seeds” limit. State the required path in (n,N,I), island aggregation rule, and independence assumptions; report finite-cell evidence only.

- **Define success and censoring.** Target survival, cooperative fixation, and Pareto efficiency are distinct. Report certified recurrent support, transition structure, and P(C,C), not just the winning class. Unresolved outcomes at 10⁵ must remain censored/indeterminate rather than losses.

### 2. Predictions likely wrong

- **“Tiny rare-target advantage” does not imply negligible harm.** The relevant quantity is accumulated relative selection versus drift. Target and faker advantages may both scale with target frequency; a faker need not be strictly disadvantaged against D—it may tie. I predict heterogeneous effects by payoff profile and target abundance, with no basis for a universal d ≥ 0.7.

- **Flatness in n is unsupported.** Increasing n changes target–faker composition and background interactions, not just exposure. I predict the pooled discount can move even if every matched pair’s effect is unchanged.

- **Prediction 3 is too strong.** Being an establisher in another background does not guarantee success in a mixed seed or domination over another establisher. Cooperative rescue may occur without cell (iii) outperforming cell (i), or without the faker usually winning.

### 3. Missing controls/cheap additions

- Extract target–faker–D–ALLC payoff tables first; distinguish strict D disadvantage from neutrality.
- Add target + neutral inserted-copy controls to separate exploitation from replacement/dilution.
- Log target/faker/D frequencies around ALLC extinction and extinction order; terminal outcomes alone cannot test the proposed mechanism.
- Report cell counts and ratio uncertainty; use minimum-sample rules and simultaneous intervals for “every cell” claims. Wilson intervals alone do not cover ratios.
- Add a small target/faker dosage grid: one-copy insertion does not represent natural multiplicities.

### 4. Alternative explanations not ruled out

Rescue by unrelated establishers; faker removal by third-party residents rather than D; drift eliminating either rare lineage; background-dependent alliances; and cutoff-dependent classification or evaluator changes.

### 5. Beyond this experiment

A useful lemma must compare **integrated target–faker selection through the scramble**, uniformly over backgrounds and cutoff—not merely bound instantaneous advantage by target frequency. This suggests a quantitative certificate to seek before extrapolating the mechanism.
