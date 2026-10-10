# Review of `specs/2026-10-10-sog-realizable.md` by gpt-6.1-sol

## 1. Design flaws/confounds and fixes

- **Three-player certificate soundness is a gating result, not a routine extension.** Boss and worker checks concern different programs, outputs, and sometimes counterfactual opponents; “two validations” does not establish symmetry. State the exact shared predicate and prove that accepted certificates imply the *actual fuel-bounded root’s* output. Test slot-2 argument ordering, opponent substitution, unequal branches, and exhausted fuel. Do not launch counted cells until this passes.
- **The prior is underspecified after lumping.** Assigning \(2^{-nodes}\) once per behavioral class differs from summing that weight over source programs; identity-sensitive programs also make ordinary behavioral equivalence unsafe. Specify the source distribution, aggregate its mass into proven interaction-preserving classes, and retain source multiplicities for drift. Report representative-length and aggregated masses separately.
- **Dropping workers below mass \(10^{-4}\) changes the lottery and its transition support.** Rare classes can be essential spoilers or bridges. Prefer lazy evaluation of encountered triples. If truncation is unavoidable, make it a separate experiment, report total omitted mass, and retain named adversaries regardless of mass.
- **This is not an isolated test of library richness.** Language, certificate semantics, faker availability, grammar, and free certificate production all change. Add a matched expanded-syntax encoding of the same executable programs and interactions. Otherwise conclude only that this particular library-plus-certificate ecology performs differently.
- **Freeze operational definitions and replication.** Specify run count, initial sampling, migration/selection rules, “fair island,” establishment duration, and endpoint treatment of mixtures. Islands within a run are dependent: use run-level uncertainty, not pooled-island Wilson intervals. Keep fair distribution, universal cross-island compatibility, and Pareto efficiency distinct.

## 2. Predictions likely wrong

- **Prediction 2 is stronger than soundness.** A sound check prevents false accepted atoms, not a militant timing out into the default **work**, nor certification of a substituted rather than actual encounter. Predict zero *false-certificate* fakers; low-wage work remains possible unless timeout and substitution safety are proved.
- **Prediction 3’s ≥0.6 establishment is unsupported by relative description length.** Absolute compatible-founder masses and three-role nucleation determine establishment. Predict a large improvement only conditional on sufficient militant and concession-boss co-seeding; no defensible numerical probability yet.
- **Prediction 5 conflates invasion resistance with persistence.** Reading both slots can remove that particular leak without preventing neutral replacement, subsequent exploitation, or migration. Predict improved residence time, not ≥0.9 persistence.
- **Prediction 6’s rationale is incomplete.** “Rational” must include the whack decision and the opponent-dependent continuation. Derive the RR play table before predicting its wage distribution.

## 3. Missing controls/cheap additions

- Forced matched seeds for D\* versus D\*₂, then migration-off persistence assays.
- Separate seed occupancy, establishment conditional on occupancy, and subsequent survival.
- Fuel sweep plus adversarial near-cap programs; record actual execution and certificate-production costs separately.
- Matched-mass faker-removal and concession-ablation controls to distinguish better seeding from improved protection.
- Pre-register predictions before static dynamical/invasion analysis, or label later predictions explicitly as conditional on those results.

## 4. Alternative explanations not ruled out

Success could come from removing modal fakers, privileging certificate-compatible templates, free tactic subsidies, or increasing the number of opportunities for one lucky island—not cheap concessions. Failure could reflect incomplete certificate production or fuel defaults rather than evolutionary instability.

## 5. Beyond this experiment

The useful prior quantity is **mass of compatible, executable founding coalitions**, not shortest concession length alone. Measuring that mass and conditional establishment would make the prior-design question transferable across libraries.
