# Review of `specs/2026-10-14-core-existence-sweep.md` by gpt-6.1-sol

## 1. Design flaws/confounds and fixes

- **The coalition object is underspecified.** In NTU games, “best S can guarantee” is generally a payoff set, not a scalar \(v(S)\). Summing utilities silently introduces transferable utility. Specify feasible coalition payoff sets, whether transfers are permitted, and whether blocking requires every member strictly better off. Use Bondareva–Shapley only for a genuine TU characteristic-function game.
- **“Credible best response” needs an explicit selection rule.** Does the complement play a Nash equilibrium among its members or coordinate as one coalition? With multiple equilibria, does S face the best or worst credible response? These choices can change core existence, especially in supermodular and Bertrand games. Define the correspondence and report optimistic/pessimistic bounds. Do not identify the object with the Chander–Tulkens γ-core without establishing matching conventions.
- **Grid feasibility cannot certify continuous emptiness.** Discretization can eliminate feasible outcomes or miss profitable deviations. Use analytic solutions where available; otherwise report certified feasibility/blocking margins, refinement checks, and “unresolved” cases. Homogeneous Bertrand additionally needs rationing rules and careful treatment of nonattained optima.

## 2. Predictions likely wrong

- **Prediction 1 is false in standard symmetric linear Cournot.** Let demand be \(p=a-Q\), common cost \(c<a\), no binding capacities, and \(m=a-c\). With coordinated leadership by a k-member coalition and independent Nash followers,
  \[
  v(S)=\frac{m^2}{4(n-k+1)}.
  \]
  The monopoly outcome with equal outputs gives each player \(m^2/(4n)\). Every coalition receives at least its leader value because \(k(n-k+1)\ge n\). This supplies a nonempty core for every n, without requiring transfers. Predict nonempty symmetric cases; investigate how asymmetry changes this.
- **Prediction 6 confuses timing advantage with incompatible coalition claims.** Core existence depends on jointly satisfying all blocking constraints, not simply their comparison with reverse timing. First-mover advantage alone does not imply emptiness. Predict disagreements; replace the proposed equivalence with a balancedness or NTU-balancedness condition.
- **Predictions 2 and 4 are overgeneralized.** Strategic complementarity alone does not establish the needed balance condition; positive spillovers also do not specify equilibrium selection or feasibility. Predict assumption-dependent results, not family-wide existence.
- For universal claims, **one certified counterexample is a falsifier**. “Positive share” and the 10% threshold can conceal genuine mathematical failures.

## 3. Missing controls/cheap additions

- Start with the analytic symmetric Cournot case above and verify every coalition constraint.
- For each empty TU case, output a violating balanced collection; for each nonempty case, output a feasible allocation and minimum coalition slack.
- Factorially vary transfers, follower coordination, and equilibrium selection on a small panel.
- For allocation games, verify that deviations really reduce to trading coalition-owned endowments. Check Scarf’s additional assumptions—continuity, feasibility, and appropriate preference conditions—not just convexity.

## 4. Alternative explanations not ruled out

- Apparent “ownership” effects may instead reflect transferable utility, convex feasible sets, follower fragmentation, or equilibrium-selection conventions.
- Cross-family comparisons change several of these features simultaneously.
- Agreement with the catalogue validates implementation consistency, not the claimed equivalence between response-function equilibria and this core.

## 5. Beyond this experiment

- Core existence is a static compatibility result, not evolutionary accessibility or selection. Keep that boundary explicit: any eventual ecology claim needs a separate mechanism showing how programs implement coalition deviations and how those deviations establish in a population.
