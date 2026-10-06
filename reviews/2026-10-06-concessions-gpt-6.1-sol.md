# Review of `specs/2026-10-06-concessions.md` by gpt-6.1-sol

### 1. Design flaws/confounds and fixes
- **Two sequential neutral substitutions do not automatically yield an extra \(1/N\) resistance.** Once the first substitution fixes, the second competes with other transitions; if those also scale as \(1/N\), its conditional success probability can remain constant. **Fix:** compute effective basin-to-basin rates, including intermediate-state residence times, return paths, and hitting probabilities. Do not infer the log-odds exponent from counting neutral steps.
- **Probes-on changes the mutation prior as well as expressivity.** Adding many atoms at fixed cutoff changes normalization, syntax multiplicity, and incumbent mutation masses. The probes-off catalogue is not a matched mechanistic control. **Fix:** add an equally expanded sham-probe grammar, and a comparison preserving the old programs’ mutation masses.
- **RR counterfactual semantics are unspecified.** Does a probe predict committed worker code or the worker’s action after rational enforcement? These can disagree precisely where deterrence matters. **Fix:** define the order of proof evaluation and enforcement, including zero-payoff ties, and tabulate both predicted and executed actions.
- **The lottery object is ambiguous.** Specify whether mutation continues after seeding, the seed distribution, horizon, and “fair island” criterion. With continuing mutation, this is not the mutation-free absorption lottery. Report establishment and persistence separately.

### 2. Predictions likely wrong
- **Prediction 1’s unique-neutral-exit claim:** consider a worker who strikes only at zero wage, or below \(1/4\). Against D it receives \(1/2\) and works, just like the militant, so it can enter neutrally. Once such workers replace militants, a boss paying \(1/4\) to certified zero-wage strikers strictly improves on D. Check catalogue representability, but this looks like a simple worker-side accommodation ratchet. **Prediction:** additional neutral worker exits and downward wage paths, not just the constant-fair boss shadow.
- **Prediction 2’s exponent and numerical thresholds:** neither follows from the stated path argument, especially given that ratchet. **Prediction:** multiple wage basins; no justified positive exponent until their effective transition rates are calculated.
- **“RR keeps it because concessions are ex-post rational”:** rationality against a committed militant does not establish rationality of the militant’s threatened strike. At positive wages, costly strikes may be overridden. **Prediction:** RR favors the smallest positive wage, consistent with the earlier enforcement result, unless probe semantics preserve commitment.
- **Prediction 6 conflates soundness with cross-context commitment.** Soundness certifies behavior against the quoted boss, not every low-paying boss. Moreover, D itself cannot pay low to a worker satisfying its positive probe. **Prediction:** the important spoilers are accommodating workers and alternative bosses, not the stated contradictory “D faker.”

### 3. Missing controls / cheap additions
- Explicitly test wage-threshold workers at \(0,1/4,1/2\), and bosses paying each wage conditional on the zero-wage probe.
- Ablate to **only the zero-wage strike probe**; the proposed grammar adds considerably more than one atom.
- Report wage-specific occupancy separately from Pareto efficiency: full production at \(1/4\) and \(1/2\) can both be efficient.
- Give binomial uncertainty and censored time-to-establishment estimates for the 40 lottery runs.

### 4. Alternative explanations not ruled out
- Apparent fairness could reflect cutoff-dependent prior mass, favorable seeding, or metastable residence rather than large-\(N\) selection.
- Rapid establishment could reflect island selection or initial striker abundance, rather than counterfactual reasoning.

### 5. Beyond this experiment
- The relevant robustness criterion may be **preservation of demands under neutral worker substitution**, not merely unfakeability of strike certificates. A perfectly sound concession rule can still lose its distributional target through accommodating workers.
