# Review of `specs/2026-10-05-scramble-lemma.md` by gpt-6.1-sol

### 1. Design flaws/confounds and fixes

- **Claim B’s payoff lower bound does not follow from Claim A.** A faker cooperating only with D loses \((P-S)x_D\), not a constant times \(x_A\). Cooperation with ALLC gives \((T-R)x_A\). Other seeded programs can reverse the overall payoff ranking. **Fix:** derive the full payoff difference against the actual population; separately analyze D-only, ALLC-only, and both-cooperating fakers.

- **Relative disadvantage to D is not subcriticality.** Moran lineage growth depends on fitness relative to population-average fitness, not D’s fitness. A faker can lose to D while increasing in an ALLC-rich population. **Fix:** specify the update rule and derive lineage birth/death rates from the full state. Use a branching approximation only where rarity and demographic assumptions hold.

- **The scramble exposure lacks the asserted deterministic lower bound.** ALLC may be absent initially or disappear quickly; extinction time and \(\int x_A\,dt\) depend on seed composition and trajectory, not N alone. The stopping time is correlated with faker survival. **Fix:** condition on a defined seed-composition event and prove a probabilistic exposure bound, including its failure probability.

- **The combined bound is not yet a valid composition.** Multiple faker types/copies, conditional seeding, and establishment–survival dependence are unaccounted for. **Fix:** define \(h,\rho,\bar q\) precisely and derive the inequality using conditional probabilities or a union bound over seeded lineages.

### 2. Predictions likely wrong

- **Prediction 2:** integrated log-fitness disadvantage alone generally does not determine survival. For a continuous-time branching process,
  \[
  \Pr(Z_t>0)\le E[Z_t]=\exp\!\left(\int_0^t[b(s)-d(s)]\,ds\right).
  \]
  Turning this into the proposed exponent requires demographic-rate bounds and a clock convention. Even a valid upper bound need not approximate measured survival within a factor of three. **Prediction:** a useful bound requires exposure plus demographic information and may be loose.

- **Prediction 3:** under a normalized truncated length prior, a fixed finite family’s mass generally decreases as the cutoff grows; its \(n=6\) mass is not automatically a lower bound. **Prediction:** uniform positivity may hold, but needs a bound on the limiting normalization and all conditional seed probabilities.

- **THEM(THEM) argument:** if the relevant box is sound for actual self-cooperation, cooperation by x already implies q self-cooperates, excluding *all* non-establisher fakers. Otherwise the proposed inference needs repair. **Prediction:** this case is either vacuous or exposes a level/world mismatch—not the advertised sucker case analysis.

### 3. Missing controls/cheap additions

- Verify box soundness and the world/level used for every nested opponent call.
- For each faker, tabulate responses to x, itself, D, ALLC, and its payoffs along recorded scrambles.
- Measure neutral survival under matched seed compositions and stopping rules.
- Report faker-copy multiplicity, ALLC-exposure distributions, and censoring; enumeration through \(n=12\) is validation, not an all-cutoff proof.

### 4. Alternative explanations not ruled out

Low survival may reflect neutral demographic extinction or long scramble duration rather than selection. Conditional seeding may enrich friendly backgrounds. Self-cooperation does not establish cooperative fixation: an establisher-faker may sustain a parochial network with inefficient cross-play. A uniform per-island establishment chance also does not prove efficient global absorption without spread and competition guarantees.

### 5. Beyond this experiment

nothing material
