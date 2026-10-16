# Review of `specs/2026-10-15-removing-rivals.md` by gpt-6.1-sol

## 1. Design flaws/confounds and fixes

- **Static exploitability is not operational accessibility.** The 17,394 units include certificates, whereas rain introduces empty-list founders. A positive code prior does not imply that the required predator phenotype can arise before extinction under S-nonself production. **Fix:** classify predators by reachable certificate state; report arrival, certificate acquisition, establishment, and successful replacement separately. Compute arrival rates from operationally eligible founder mass, not certified-unit counts.

- **The predator conditions do not establish the proposed invasion chain.** They omit predator payoffs against copies and target payoffs against predators. Non-self-cooperation can permit a stable rival–predator mixture rather than rival elimination; target defection against predators alone does not establish target invasion. **Fix:** calculate frequency-dependent payoffs for rival/predator/target triples, then test promising triples with the actual production and migration kernel.

- **B1 lacks a contemporaneous counterfactual.** Old failures can resolve through delayed migration, certificate production, or drift without rain. **Fix:** branch each generation-2,000 checkpoint into matched ε = 0 and rain continuations. Analyze differences conditional on those selected checkpoints, not unconditional cure probabilities.

- **Endpoints are underspecified under rain.** “Leaving the target” could mean one immigrant birth or loss of target dominance. “Mutually certified with PrudentBot” also need not define a pairwise-cooperative network. **Fix:** freeze membership rules before running; distinguish transient contamination, holder replacement, and sustained island takeover. Report within-target compatibility and actual \(P(C,C)\).

## 2. Predictions likely wrong

- **Prediction 2 is too optimistic.** At εN = 0.1, an island receives about 1,000 founders over the treatment window. If accessible predator mass is \(q\), direct arrivals average \(1{,}000q\); successful chains are fewer. Ignoring migration, 80% even receiving a predator requires \(q \ge 0.00161\). **Prediction:** cure varies sharply with accessible predator mass and establishment probability; many statically exploitable rivals remain unresolved.

- **Predictions 5–6 overstate universality.** One privileged founder can die during the scramble; rare per-island failures compound across 64–256 islands. Earlier donor success supports optimism, not these near-certain thresholds. **Prediction:** sponsorship substantially reduces clique establishment, but residual failures and geometry dependence remain; rain need not improve universal-on-target probability.

- **Prediction 3’s mechanism is stronger than its evidence.** “No strict predator” does not imply no replacement through finite-population excursions or repeated immigration. **Prediction:** cliques resist much more strongly than exploitable rivals, without necessarily satisfying the same numerical bound at every rain rate.

## 3. Missing controls/cheap additions

- Add a PrudentBot donor with **empty certificates**, separating sponsorship of code from sponsorship of inherited information.
- From a few checkpoints, inject one reachable predator and a matched nonpredator. This separates arrival scarcity from establishment failure.
- Record target→rival as well as rival→target transitions, residence times, and certificate provenance.
- Use run-clustered uncertainty: islands share migration and are not independent replicates. Twenty runs cannot substantiate ≥0.95 success reliably; even 20/20 has a two-sided 95% lower bound near 0.83.

## 4. Alternative explanations not ruled out

Rain may cure through direct target arrivals, demographic dilution, or certificate transfer—not predators. Apparent cures may be temporary low-efficiency collapses. Sponsorship may work through privileged certificate coverage rather than PrudentBot-specific strategic superiority.

## 5. Beyond this experiment

Nothing material.
