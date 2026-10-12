# Review of `specs/2026-10-12-provenance.md` by gpt-6.1-sol

### 1. Design flaws/confounds and fixes
- **S-k is underspecified, and its stated mechanism contradicts “distinct partners.”** Define distinctness (individual or structural source), candidate generation, tie-breaking, whether zero-validity candidates are admissible, and behavior if k partners never arrive. With source-distinct partners, at most one can equal the producer; two-of-three own-copy encounters are impossible. Require the retained candidate to validate against at least two source-distinct partners if that is the intended safeguard.
- **Mixed provenance may change source identity itself.** Specify whether the rule trait and acquired/cache state enter quoted source and structural `eq`. Otherwise assigning rules can split formerly identical copies, changing clique abundance independently of production. Separate behavioral source, provenance metadata, and mutable inventory; report equality-class frequencies.
- **Blocking self-production also changes acquisition timing and opportunity.** A benefit cannot automatically be attributed to certificate generality. Add S-self with acquisition delayed to the matched nonself encounter, then produced against self; log attempts, waiting, candidate validity and first acquisition separately.
- **The cache needs an explicit validity and charging contract.** Key negatives by every input affecting the gate, including source/script state and budgets; distinguish rejection from timeout and specify invalidation. Charge lookup, storage and repeated misses consistently. Otherwise “feasible” could mean unsound negative reuse or unpriced memory.
- **These runs measure a finite-horizon lottery, not large-population universality.** Doubling N or I at fixed migration and horizon changes nucleation/resolution opportunities. Keep the finite-size label, extend unresolved runs, and report island efficiency separately from global universality.

### 2. Predictions likely wrong
- **Prediction 3:** majority voting over *source-distinct* partners is not governed by repeated-copy binomial probabilities. S-2 may tie systematically; S-3 may retain a narrow certificate valid for two partners but not a broad population. I predict strong dependence on candidate coverage and tie-breaking, not reliable monotone ordering.
- **Prediction 5:** neutrality after acquisition does not imply neutral holder composition. Differential acquisition, establishment, founder effects and linkage can enrich rules before scripts are held; cooperative holders are a selected subset. I predict departures from ¼, potentially systematic enrichment of faster-acquiring rules.
- **Prediction 4:** initial diversity does not bound later waiting costs. A producer in a near-monoclonal island may wait indefinitely for a nonself source. I predict heavy-tailed acquisition delays, even if median cost remains low.
- **Prediction 2:** removing seeded cliques does not isolate the residual gap: it redistributes prior mass and may remove other useful behaviors. I expect improvement, but ≥30/40 is unsupported.

### 3. Missing controls / cheap additions
- Add a **mass-matched prior ablation**, replacing clique mass with specified nonclique carriers rather than silently renormalizing.
- Audit S-nonself’s zero-self-only claim over the full supported carrier set, including copying/adoption. Define “self-play-only” by script validity, not observed encounters.
- Use event-indexed random streams for paired seeds; report paired outcome differences and intervals, not only marginal Wilson intervals.
- Report full rule frequencies alongside cooperative-holder frequencies, stratified by carrier and initial equality class.
- Predeclare primary contrasts and treatment of indeterminate endpoints. Twenty runs per size cannot resolve modest differences reliably.

### 4. Alternative explanations not ruled out
Reduced universality loss could reflect suppressed acquisition, demographic pruning during waiting, altered equality classes, or timeout-induced effective prior filtering—not broader certificates. Donor advantages could reflect guaranteed early availability rather than exogenous provenance. Finite-horizon patchworks may reflect slow bridge spread rather than permanent incompatibility.

### 5. Beyond this experiment
nothing material
