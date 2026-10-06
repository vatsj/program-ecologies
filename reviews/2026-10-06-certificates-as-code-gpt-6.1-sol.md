# Review of `specs/2026-10-06-certificates-as-code.md` by gpt-6.1-sol

## 1. Design flaws/confounds and fixes

- **The stated soundness theorem is insufficient.** “If both checks return T then both hypotheses are true” follows from how the hypotheses are named; it does not establish that either certified cooperation atom is true. Circular assumptions can validate false conclusions unless discharge is independently justified. **Fix:** require unconditional semantic soundness: every accepted closed certificate implies its exact fuel-indexed execution atom, including against arbitrary non-carriers. Prove the pair rule without assuming checker soundness inside that proof. If this fails, stop before the catalogue run.
- **Program identity excludes behaviorally relevant data.** Execution depends on `(code, cert-list)`, yet certificates and lookup keys identify only code. Changing a certificate list can change play without changing the certified identity. **Fix:** bind claims to the complete behavioral object, including checker version, certificate environment and fuel convention. Specify how self-reference is represented finitely; do not hide it in host-generated pointers.
- **ChkR risks restoring the idealized oracle.** Treating a check as one proof-evaluation step plus a static fit condition is sound only if that condition bounds the actual evaluator run, including quotation, substitution, lookup and nested checking. **Fix:** charge actual runtime separately from proof-node counts and require a replayable witness for every summarized check.
- **Offline pairwise production confounds realizability with curated compatibility.** A finite table prepared using opponent knowledge can demonstrate cooperation without demonstrating an extensible language of cooperators. **Fix:** freeze a production procedure and templates, then test held-out sources. Report certificate/storage/production growth alongside match costs.

## 2. Predictions likely wrong

- **Prediction 3 contradicts soundness.** If CB defects against a certificate-less FB_code, a sound searcher cannot certify CB’s cooperation in that same match at that same fuel. Cheap checking makes the defection easier to establish, not cooperation. **Prediction:** finished sound searches do not produce that cooperation proof; both defect unless a different target or certificate-delivery mechanism is introduced.
- **Prediction 1 is not supported by the proposed justification.** Checker acceptance is syntactic, whereas truthful cooperation is semantic. **Prediction:** the unconditional proof exposes an additional guard/discharge requirement, or the unrestricted pair rule admits a false certificate.
- **Prediction 5 requires more than matching root shape.** Quoted sources and fuel-indexed runs are source-specific. **Prediction:** literal certificates do not transfer; quantified templates may, but require checked instantiation and explicit membership obligations.
- **Prediction 4 overstates CBsloppy.** Matching an end sequent does not supply a certificate when none exists. **Prediction:** exploitation depends on delivery of an appropriately rooted bogus certificate; D alone need not trigger cooperation.

## 3. Missing controls / cheap additions

- Attempt cyclic certificates for false atoms, especially `plays(D, opponent, C)`, not merely malformed certificates.
- Mutate certificate lists while holding code fixed; vary fuel immediately above and below claimed bounds.
- Compare ordinary acyclic carried proofs with JLöb-enabled proofs under identical accounting.
- Replace “twins only” in the disabled control with a measured result: direct proofs can certify distinct sources without Löb.
- Align prediction 2’s success threshold and falsifier: currently costs between \(5·10^4\) and \(2·10^5\) fall into a verdict gap.

## 4. Alternative explanations not ruled out

Cooperation could reflect a C-seeded cyclic acceptance convention, a precomputed compatibility club, or omitted verification costs—not sound realizable Löbian cooperation. Pairwise success also establishes neither invasion accessibility nor large-population efficiency.

## 5. Beyond this experiment

nothing material
