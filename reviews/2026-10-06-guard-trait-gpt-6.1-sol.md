# Review of `specs/2026-10-06-guard-trait.md` by gpt-6.1-sol

### 1. Design flaws or confounds, and fixes

- **Guard mass is not a selection statistic.** Behaviorally identical guard twins can drift neutrally; their stationary allocation can reflect mutation supply rather than benefits of reflection. Specify whether mutations redraw `(source,g)` jointly or change either trait separately. Report guard mass within behaviorally distinguishable source pairs, neutral-twin mass separately, and sensitivity to both mutation kernels. Apply both guard priors to the chain, not just the lottery.
- **Mixed-guard semantics need an explicit contract.** Does the opponent’s guard alter its public source, proof-budget annotation, or proposition being proved? Reusing homogeneous tables is invalid unless these identities match exactly. Build every cross-block from the actual mixed semantics; replay witnesses with the correct reader budget and opponent identity. Establish lumpability across *both* guard populations, not within each homogeneous block.
- **The price is undefined as an amortized cost.** A literal per-match deduction of \(0.1(2b+8)=4\) is not amortization and may dwarf PD incentives. Specify the payoff scale, amortization denominator, who pays, and whether expense depends on actual search. Include a zero-price reference and a cheap price sweep; one arbitrarily scaled cell cannot establish that realizable reflection is selected out.
- **The large-population conclusion exceeds the design.** Three finite \(N\) values can miss a crossover or deep metastable class. Estimate asymptotic entry/exit rates for the dominant bottlenecks. Make independent deep-state discovery from the ongoing solver audit a prerequisite for interpreting stationary weights.

### 2. Predictions likely wrong

- **Prediction 1’s rationale is insufficient.** The ≈0.05 partner mass and graft payoff decrement are evaluated in another ecology. Rare-mutation stationary weights depend on transition bottlenecks, not average marginal payoffs there. My prediction: substantial prior-sensitive neutral guard mass, with no justified directional prediction for the behaviorally active remainder.
- **Prediction 2 has no interpolation principle.** Mixed catalogues can introduce new invasion paths, bridges, or traps; their stationary cooperation need not lie between homogeneous endpoints. I predict that any displacement will be explained by changed transition structure rather than weighted interpolation.
- **Prediction 3’s neutrality justification is incomplete.** Check all four resident/mutant encounter payoffs, including mutant–mutant play, and any costs. If these are identical, neutrality should be exact: \(N\rho=1\), up to numerical error. Otherwise even a small difference can matter at \(N=10^4\).
- **Prediction 5 is uninterpretable until the price is fixed.** Under a sufficiently large unconditional charge, exclusion would mainly demonstrate imposed fitness disadvantage, not selection against completeness.

### 3. Missing controls or cheap additions

- Add a **sham heritable bit** that changes neither proofs nor costs, using the same mutation kernel: calibrate neutral label allocation and twin handling.
- Tabulate the complete set of **guard-induced action changes**, weighted by source prior; separate newly enabled cooperation from newly enabled exploitation.
- For attribution only, delete newly enabled fakers and newly enabled cooperative partners separately, retaining other catalogue weights.
- In lotteries, record establishment, loss, and coexistence times—not just horizon holders. Twenty seeds cannot support a sharp “unchanged” conclusion; report paired differences and binomial uncertainty.

### 4. Alternative explanations not ruled out

Mutation accessibility and catalogue multiplicity; source-tag recognition rather than reflection; transient founder advantage; guard-enabled bridges changing connectivity; and finite proof/cutoff thresholds rather than a general completeness tradeoff.

### 5. Beyond this experiment

nothing material
