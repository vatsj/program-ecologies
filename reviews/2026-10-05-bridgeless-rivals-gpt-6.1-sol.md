# Review of `specs/2026-10-05-bridgeless-rivals.md` by gpt-6.1-sol

## 1. Design flaws/confounds and fixes

- **The bridge/exploitation definitions conflict.** A bridge mutually cooperates with R, so “R cooperates while the bridge defects” cannot occur in that pairwise table—and describes exploitation *of R*, not by R. If both are cost-free self-cooperators, mutual cooperation also implies neutral two-type fixation. **Fix:** distinguish pairwise bridges from candidate mediators, correct payoff orientation, and specify which population contexts permit exploitation.

- **“Bridge-less” actually means “no individually heavy, safe establisher bridge.”** Numerous sub-threshold bridges, non-establishers carried by migration, or multistep compatibility paths could resolve rivalry. **Fix:** report literal bridge absence separately from threshold exclusion; report total safe-bridge mass and compatibility connectivity, alongside the heaviest bridge. Treat the threshold as a sensitivity parameter.

- **Three cutoffs and one finite dynamical cell cannot settle either asymptotic claim.** Survival to \(10^5\) at \(N=200,I=64\) establishes metastability, not permanence or failure along \(I\gg N\). Larger cutoffs can also add bridges to previously bridge-less rivals. **Fix:** frame this as finite-cutoff screening; add a small scaling panel in \(N,I\) and observation time before revising universality claims.

- **Forced seeding confounds bridge structure with rival identity and founder supply.** One selected rival on every island changes the lottery substantially; two different rivals can differ in establishment and migration fitness for unrelated reasons. **Fix:** test several matched rivals, and include sparse forced seeding. Ideally compare the same rival with its bridge available versus removed, controlling the removed mass.

## 2. Predictions likely wrong

- **Prediction 1’s monotonicity rationale is invalid.** Accumulating establisher support does not imply increasing normalized prior mass. Rivalhood and bridge status need not persist as the opponent universe expands. My prediction: more rivals gain detectable bridges at larger cutoffs; the threshold-defined ratio may nevertheless remain stable. No justified directional prediction for literal bridge-less mass.

- **Prediction 3’s “all bridge-less” is too strong.** Bridged rivals can survive a finite horizon because their bridges fail to seed, survive the scramble, or complete absorption. Predict some finite-horizon bridged separations if enough runs are sampled. Zero separations would bound their frequency, not falsify nonzero probability.

- **Prediction 4 lacks a mechanism.** Dense forced rival seeding may change global encounter cooperation while leaving within-island cooperation high. Predict greater robustness of local \(P(C,C)\) than of cross-island \(P(C,C)\); define exactly which object \(q\) summarizes.

## 3. Missing controls/cheap additions

- Report normalized and unnormalized prior masses, omitted-tail bounds, and whether class equivalence changes across cutoffs.
- Sweep bridge thresholds, including zero; report total bridge mass.
- Track bridge founders, establishment, and subsequent mediation—not merely final rival identity.
- Give confidence intervals using runs as independent units. With zero losses, a 95% upper hazard bound below \(10^{-6}\) requires approximately \(3\times10^6\) minority-island-generations of exposure; decompose exposure by rival and island configuration.
- Preregister separation, establishment, ancestry attribution, both \(P(C,C)\) objects, and \(q\).

## 4. Alternative explanations not ruled out

Finite-horizon censoring; ineffective rather than absent bridges; cutoff-dependent normalization; identity-specific founder advantages; higher-order ecological mediation; correlated island nucleation. Also, heterogeneous efficient islands refute homogenization, not necessarily Pareto efficiency—state which claim separation threatens.

## 5. Beyond this experiment

The more useful asymptotic object may be the probability of **successful mediation before rival loss or horizon**, incorporating aggregate bridge mass, demographic survival, and migration—not a binary bridge label. Deriving its scaling could separate prior-support obstructions from merely slow resolution.
