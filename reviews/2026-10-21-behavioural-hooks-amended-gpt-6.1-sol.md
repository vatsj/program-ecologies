# Review of `specs/2026-10-21-behavioural-hooks.md` by gpt-6.1-sol

1. **Errors, contradictions, unsound mechanisms**
   - **The hostile-key intervention also boosts FairBot.** “FairBot: … (□a → C)” and “Gödel predator: … (□a → D)” use the same key, yet “the prior mass of the hostile named keys … [is] multiplied by 10.” A key-only prior cannot distinguish these programs. **Fix:** reweight complete `(default, key, action)` constructions, or rename this a guard-frequency intervention and acknowledge that it boosts friendly constructions too.
   - **The trigger contradiction survives the amendment.** “Thanks is written only after *mutual* cooperation” conflicts with “thanks after mutual or received cooperation.” The latter permits a defecting recipient to write thanks, reopening direct self-conversion. **Fix:** specify and test mutual-cooperation-only thanks consistently.
   - **`noA` is representation-dependent after quotienting.** “Keys are deduplicated by GL-equivalence” conflicts with removing “every key containing the atom a”: equivalent representatives can contain different atoms. **Fix:** enumerate the a-free grammar separately, quotient it, and specify its weights independently of arbitrary canonical representatives.
   - **GL semantics is not an outcome convention.** “The solver decides, and the convention it uses is reported” cannot resolve a mathematical disagreement by implementation choice. World-zero vacuity is only an initialization fact, not the stabilized outcome. **Fix:** independently derive the named table using stabilized GL evaluation and make agreement a launch gate.

2. **Design flaws/confounds**
   - **M1 cannot identify friendly guards on-path.** Classification “against the island’s current population” makes FairBot, PrudentBot and CooperateBot indistinguishable in many cooperative populations. The categories overlap, undermining predictions 3 and 5. **Fix:** classify response signatures against a fixed diagnostic panel, retaining an explicit ambiguous category.
   - **Part K bundles several interventions:** seeded keys, written keys and contracts all change. A gain or loss cannot be attributed to admitting competitors. **Fix:** add source-separated replacements, at least a written-keys-only cell with founders and contract technology held fixed.
   - **M3 does not cleanly discriminate mechanisms.** Contracts remain an alternative conversion route; eviction occurs within writes/copies, not independently; inheritance changes offspring initialization. **Fix:** repeat decisive transmission ablations without contracts, record before/after states, and use a matched insertion rejected-versus-eviction counterfactual. Preserve fill ancestry separately from its latest transmission event.

3. **Predictions likely wrong**
   - **Prediction 5:** I expect FairBot-equivalents to exceed PrudentBot-equivalents under a fixed-panel classifier. The length prior strongly favors the shorter guard; conditioning writes adds another frequency bias. Prudence’s payoff advantage need not overcome that production advantage. Report production rates and conditional reproductive success separately.
   - **Prediction 8 overstates “breeding true.”** Its own expectation that inheritance-off remains ≥0.85 predicts inheritance is dispensable for recovery. My prediction is that copying can maintain the cooperative phenotype without substantial inheritance dependence; establish H2’s causal contribution rather than equating inherited presence with necessity.

4. **Missing controls / cheap additions**
   - For sham writes, match key length and pre-write applicability frequency. Otherwise M5 tests generic activation rates as well as partner conditioning.
   - Add fixed-panel probes including unconditional cooperators, defectors and named rivals; report fill activation and actual outcome changes.
   - Extend a subset to longer horizons and N=200. Report finite-lottery conclusions only; these cells do not establish a large-population limit.

5. **Alternative explanations not ruled out**
   - Recovery could reflect prior mass, founder demography or FIFO removal rather than selection for cooperative reasoning.
   - Removing quote equality excludes literal identity tests, not behavioural assortativity or modal rival networks. Stranger-compatible outcomes—not grammar inspection—must establish their absence.
