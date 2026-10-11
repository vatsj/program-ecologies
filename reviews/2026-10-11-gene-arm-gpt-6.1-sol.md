# Review of `specs/2026-10-11-gene-arm.md` by gpt-6.1-sol

### 1. Design flaws/confounds and fixes
- **The credibility filter is bypassable through bases.** Boss bases retain committed whacks; chicken bases retain Straight. Filtering overrides cannot reproduce RC’s execution rule when equivalent noncredible behavior remains admissible without genes. **Fix:** add whole-program credibility and execution-time best-response arms, or remove equivalent base commitments in matched controls. Otherwise call this “override filtering,” not recovered enforcement asymmetry.
- **“Best reply” conflates execution and source-visible mutation.** At an execution point, others’ actions may be fixed; replacing a readable program can change their certificates, probes, and actions. **Fix:** calculate separately continuation best replies holding the appropriate history fixed and mutant-program payoffs after reevaluating the whole encounter. Use the latter for gene-stability and evolutionary deviations.
- **Catalogue-wide admissibility is underspecified and endogenous.** Which catalogue supplies witnesses: all unfiltered programs, admitted programs, or residents? Filtering against survivors risks circularity and order dependence; never-fired threats pass vacuously. **Fix:** freeze an explicit reference catalogue, report firing witnesses and vacuous admissions, and test reference-catalogue sensitivity.
- **The experiment lacks complete operational semantics.** Specify precedence when two genes fire, gene insertion/replacement at the cap, threshold–quorum interaction, probe counterfactuals, and retaliation’s memory/matching process. A “next encounter” trait cannot silently enter a memoryless payoff table.
- **Lumping may change this experiment’s dynamics.** SG depends on syntactic gene accessibility, not merely identical current payoffs. **Fix:** establish lumpability for both payoff and mutation kernels; otherwise retain syntactic twins and use the audited log-domain, closure-seeded solver.

### 2. Predictions likely wrong
- **1: G-cred recovers RC.** Not with noncredible commitments surviving in bases. I predict retained boss threats and substantial departures from RC unless credibility governs execution throughout.
- **3: SG finds whacks first under G-all.** SG’s targeted half proposes best replies; the brief says costly executed whacks are not best replies. They can arise through the prior half or vacuous triggers, not preferential credible generation. I predict targeted SG favors concessions/accommodation, with no guaranteed fairness increase.
- **4: Gene-stability lies between Nash and Pareto.** Restricted unilateral gene deviations imply neither action-game Nash nor Pareto efficiency. Public roles alone add no substantive Bayesian uncertainty. I predict incomparability unless gene completeness and the deviation game are specified. Fair-state instability under G-all also needs an actual profitable, source-reevaluated witness.
- **5: Quorum strikes are Pareto improvements and chain exits.** A strike can hurt the boss; coordinated profitable worker deviations are not automatically Pareto improvements. A unilateral rare-mutation chain cannot directly take a simultaneous two-worker mutation. I predict any escape needs an identified sequential path, neutral intermediate, or separately modeled coalition kernel.

### 3. Missing controls/cheap additions
- Compare every named gene with its behaviorally equivalent base encoding; filtering should not depend on packaging.
- Run a matched random-removal filter and preserve original prior masses without renormalization changes hidden from reporting.
- Add a uniform admissible-local-mutation kernel to separate SG targeting from mutation support.
- Report actual Pareto frontiers, establishment uncertainty, and decisive-edge scaling beyond two population sizes. Align falsifiers with predicted thresholds rather than leaving large unclassified gaps.

### 4. Alternative explanations
Fairness could reflect removed prior mass, catalogue-relative certification, redundant gene spellings, mutation accessibility, or discriminatory probes—not evolved credible enforcement. Apparent stability could reflect the two-gene cap rather than absence of improving deviations.

### 5. Beyond this experiment
Make **encoding invariance** a prerequisite for the proposed equilibrium notion: equivalent behavior moved between base code and genes should not change credibility or stability. Otherwise the “proof device” certifies a representation convention, not an equilibrium property.
