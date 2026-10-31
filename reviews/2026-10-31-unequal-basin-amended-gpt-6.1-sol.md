# Review of `specs/2026-10-31-unequal-basin.md` by gpt-6.1-sol

## 1. Errors / unsound mechanisms

- **The founding limit is not implemented.** “I → ∞ before time” conflicts with “reachable state space is the product of the post-anneal slot supports” estimated from 16,384-island pools. A program absent from a finite sample can have positive founding probability at infinite I. **Fix:** distinguish the empirical-start ODE from the infinite-founding-law ODE. Establish analytical support closure, or add pool-size/rare-support sensitivity and restrict conclusions accordingly.

- **Ablations can invalidate the quotient.** “Because the supports cannot grow, this lumping is exact for all time” conflicts with replacement “by each constant”: replacement may introduce constants outside the original supports. **Fix:** include every possible replacement constant before lumping. Also retain syntax-family membership and within-class mass: a behavioural class can contain several syntactic families. Family ablations must operate on those constituent masses, not delete mixed classes.

- **The boundary definition assumes monotonicity.** “u\* is the smallest u” followed by “refined by bisection” is unjustified without monotone endpoint classification. Multiple basin crossings are possible. **Fix:** report all sampled intervals and bisect each observed transition; call u\* only the first detected crossing, with its search range.

## 2. Design flaws / confounds

- **Symmetric stability is not ecological stability.** Projected trajectories and a “Jacobian … on its support” can miss symmetry-breaking and missing-program invasion. **Fix:** distinguish invariant-subspace, full-simplex, and transverse spectra. Test small asymmetric perturbations explicitly. State which absent programs are excluded by the empirical-support approximation.

- **Finite-horizon stillness can mimic convergence.** Tiny surviving donor masses can produce extremely delayed rescue, precisely the proposed distinction from Monte Carlo extinction. A small derivative and flat outcome shares do not certify an attracting limit. **Fix:** inspect rare-class relative growth rates, endpoint residuals under tighter tolerances, and time-to-rescue estimates. Report metastability when asymptotics remain uncertified.

- **V3 is not a matched validation.** Rebuilt pools matching initial V\* need not match correlations or rare carriers; agreement within 0.01 with a historical trajectory could fail despite correct code. **Fix:** run fresh Monte Carlo from exactly the same empirical law, with uncertainty bands. Treat historical agreement as replication, not a correctness gate.

## 3. Predictions likely wrong

- **Prediction 6 is too strong.** Strictly negative class-changing eigenvalues do not follow from persistent unequal outcomes. At ε = 0, missing-donor faces are invariant; neutral directions and nonhyperbolic attraction are plausible. **Prediction:** at least one arm has a near-zero mode, or support stability fails to extend to transverse directions.

- **Prediction 3 overstates V1.** V1 validates one constants-only start, not every correlated law produced by replacement and subsequent tilting. **Prediction:** constants-only probably still reaches fairness, but “nearly a check” is unwarranted.

## 4. Missing controls / cheap additions

- Add matched-mass random conditional knockouts; otherwise large u\* shifts may reflect abundance rather than a distinctive carrier mechanism.
- Restore a proposed carrier after knockout at several doses. Necessity plus dose-dependent rescue is stronger than knockout ranking.
- Report total omitted donor rate and repeat decisive cells without donor skipping; skipped inflow alone is not a propagated trajectory-error bound.
- Record full unequal-endpoint program-role associations, not only marginal class masses.

## 5. Alternative explanations

The brief does not exclude correlation destruction by replacement, collective effects involving rare classes outside the endpoint top 20, or donor-supply changes rather than local rescue blocking. A failed single-family knockout also cannot distinguish redundancy from irrelevance.
