# Review of `specs/2026-10-04-bounded-provers.md` by gpt-6.1-sol

### 1. Design flaws/confounds and fixes

- **The bounded evaluator is underspecified and potentially circular.** Is `settle(y,x)` computed in the free game or the bounded game? Free-game costs may certify cooperation that disappears after bounding; bounded-game costs depend on the very interaction being evaluated. Masking a free `BOX` value is not automatically sound about bounded opponents. **Fix:** specify the semantics before running; check that `BOX_b(THEM(ME))` implies the opponent’s *actual bounded* cooperation for every enumerated pair. Test the other box operators against their intended propositions separately.

- **This is not yet a bounded prover.** Semantic stabilization is neither proof length nor proof-search work. Charging all boxes the same opponent-level cost ignores which proposition is being proved; constants costing zero further builds in a computational exemption. **Fix:** call this a *semantic legibility gate*, not a bounded-Löb implementation. Restrict conclusions accordingly. A realizability claim needs an explicit proof system, resource measure, and sound checker.

- **Per-program budgets confound legibility with language support and prior.** Charging budget nodes changes which prover skeletons fit at \(n=6,8\), not merely their weight. **Fix:** separate fixed-support budget comparisons from length-penalized comparisons; report missing families and their total prior mass.

- **Neither finite-\(n\) closure nor four population sizes establishes the advertised limits.** A budget may create apparent closure by pushing neutral mutants beyond the enumeration cutoff. Failure at \(b=2\) cannot resolve uniformity in \(n\). **Fix:** label conclusions finite-language; extend targeted sibling enumeration beyond \(n\), and distinguish fitted slopes from asymptotic claims.

### 2. Predictions likely wrong

- **Prediction 1:** below its self-cooperation threshold, FairBot need not be behaviourally ALLD: it can still cooperate with zero-cost ALLC. Predict failed self-cooperation but selective cooperation.

- **Predictions 2–4:** an added disjunct need not add an essential atom or increase stabilization depth. Some siblings may remain legible. Moreover, predicting prudent thresholds of 4 conflicts with attributing efficient closure at \(b=2\) to those provers unless a distinct cheaper family exists. Predict heterogeneous sibling exclusion; no justified quantitative stationary-mass forecast before the static map.

- **Prediction 5:** larger budgets can buy cooperation with mutants and improve entry. Prior penalties alone do not determine stationary mass. Predict dependence on transition advantages and grammar support, not universally \(b=2,3\).

- **Predictions 6–7:** unfakeability does not guarantee unchanged entry, survival, or basin size. Bounded provers can stop cooperating with other legitimate provers during the scramble. Predict budget-dependent lottery outcomes even above the self-threshold. Nor does absent self-cooperation alone imply zero efficient outcomes.

### 3. Missing controls / cheap additions

- Add **budget-matched random gates** and atom-count-only gates to distinguish structured legibility from generic interaction pruning.
- Use identical genotype support and prior for finite versus infinite budgets, including budget annotations.
- Measure mixed-prover compatibility and time-resolved loss of seeded core members.
- Twenty lottery runs cannot support tight equivalence claims. Predefine an equivalence margin and use paired seeds with adaptive replication; record unresolved runs rather than treating timeouts as failures.

### 4. Alternative explanations not ruled out

Apparent closure could reflect truncation or altered logical semantics; stationary concentration could reflect lost competitors or prior redistribution; lottery changes could reflect smaller cooperative basins rather than fakers. Agreement with the free arm could merely mean the gate rarely binds on occupied states.

### 5. Beyond this experiment

nothing material
