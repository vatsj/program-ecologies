# Review of `specs/2026-10-04-conjecture4.md` by gpt-6.1-sol

## 1. Design flaws/confounds and fixes

- **Finite drift-closure is not a falsifier of unbounded Conjecture 4.** A class closed within n ≤ 13 may acquire a suckerable neighbor at greater length or box depth. **Fix:** label such findings “truncation-closed candidates”; refutation requires proving closure against the full language. Likewise, nonexistence at successive cutoffs is evidence, not proof.

- **The theorem’s semantic universe is underspecified.** GL validity over arbitrary frames differs from validity on a linear chain; nested theories PA + Conᵏ require explicit cross-level axioms and an interpretation of opponent applications. **Fix:** specify syntax, admissible frames, designated evaluation point, fixed-point construction, and inter-box principles. State separately whether the result concerns evaluator semantics, modal validity, or arithmetic provability.

- **Mutual-cooperation connectivity need not represent neutral evolutionary accessibility.** Pairwise mutual cooperation gives neutral invasion into a homogeneous cooperative resident under the stated PD assumptions, but not necessarily into a polymorphic population. **Fix:** restrict the theorem’s evolutionary interpretation to the rare-mutation, monomorphic fixation chain; otherwise verify neutrality against resident mixtures.

- **“Leak/μ” lacks a reproducible measure specification.** Syntax multiplicity, class equivalence, cutoff normalization, and direct-neighbor versus whole-closure leakage can change the answer. **Fix:** give the exact numerator, denominator, prior, equivalence relation, and deduplication rule. Distinguish cutoff-restricted leakage from leakage in the full language.

## 2. Predictions likely wrong

- **Prediction 2’s transfer criterion is too weak.** Closure under disjunction and availability of a proof checker do not establish a usable sibling construction. Bounded provability depends on proof budgets, code lengths, theory strength, and self-reference overhead; bounded Löb is not a drop-in replacement for unbounded GL. **My prediction:** transfer needs quantitative budget assumptions and may hold only above explicit thresholds. Separate the potentially general Lemma/Corollary from the substantially stronger sibling claim.

- **Prediction 1’s proposed argument does not establish its crucial step.** Adding a cooperation disjunct may preserve self-cooperation while causing prudent neighbors to reject the sibling. Grammar closure does not imply closure-membership. **My prediction:** proving mutual cooperation with at least one incumbent—while establishing exploitability—is the bottleneck, not constructing the disjunction. The conjecture itself remains open.

- **A uniform leak bound is not supported by the observed plateau.** Cutoff ratios can remain stable before new families dominate either mass. **My prediction:** n = 12–13 will be weakly diagnostic of uniform boundedness unless accompanied by a summable-tail argument.

## 3. Missing controls/cheap additions

- Reproduce existing n ≤ 11 results before extending; cross-check small cases with an independent evaluator or explicit payoff-table checks.
- Report program counts and prior mass by length and box depth, including leak contributed by each new shell.
- For each truncation-closed candidate, search larger/deeper witnesses without enumerating the entire larger universe.
- Keep a dependency ledger for proofs: semantic theorem, arithmetic assumption, budget condition, or evaluator-only observation.
- Report both direct leak and closure-reachable leak if they differ.

## 4. Alternative explanations not ruled out

- FairBot’s apparent optimality may reflect unusually large syntactic prior mass rather than stronger evolutionary protection.
- Missing drift-closed classes may reflect enumerator restrictions or quotienting errors.
- Cooperation may depend on free, sound, unbounded provability rather than source access.
- Leakage magnitude alone does not determine stationary cooperation: return rates, subsequent exploitative transitions, and path structure also matter.

## 5. Beyond this experiment

**Qualitative non-closure need not imply asymptotic inefficiency.** The program needs a quantitative theorem relating witness complexity and mutation mass to escape rates as N grows. An arbitrarily tiny leak defeats exact closure without necessarily defeating Pareto-efficient concentration.
