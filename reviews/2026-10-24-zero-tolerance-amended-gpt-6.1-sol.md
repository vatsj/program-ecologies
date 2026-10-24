# Review of `specs/2026-10-24-zero-tolerance.md` by gpt-6.1-sol

1. **Errors and unsound mechanisms**
   - “The stored partial ablations bound what each fix can do” and “its ceiling is about 0.24” are unjustified. Deleting mutants and adding a responsive strategy change different transition rates; stationary efficiency has no such monotonicity bound. **Fix:** call these benchmarks, not ceilings.
   - “Its read cannot be gamed through the bounded-read path” is unsupported by “payoffs are computed exactly over its draws.” Exact averaging does not make the simulated opponent terminate. **Fix:** specify sampling fuel, timeout action, recursion handling, independent random tapes, and what opponent-visible distribution includes. Test the existing bounded-read exploiters directly. Without this, SR may merely hide the same vulnerability behind an oracle.
   - “Against the control (0.047)” conflates the old baseline with the new mass-boosted control. **Fix:** use the newly computed control for every contrast; retain 0.047 only as historical context.

2. **Design flaws/confounds**
   - “R is defined per arm to include the arm’s added inspectors” makes exit-hazard comparisons potentially compositional: adding a protected resident can reduce aggregate hazard without protecting existing residents. **Fix:** report resident-specific per-mutant fixation/exit rates, plus aggregate rates under both fixed reference weights and arm-specific stationary weights.
   - Equal added prior mass does not equal equal *effective* responsive-inspector mass. An added program may duplicate an existing behavioral class, differ only off-path, or alter twin drift. **Fix:** report behavioral-class membership, aggregated mutation masses, and twin handling; preserve source distinctions wherever opponents can distinguish them.
   - Two lottery sizes at horizon 20N cannot establish eventual outcomes or a large-population limit. **Fix:** label results finite-horizon, report unresolved islands and late transition activity, and extend only unresolved runs. For chains, report entry/exit scaling and support, not just stationary weights.

3. **Predictions likely wrong**
   - SR does not generally eliminate light cheating. With independent draws and cheating payoff +1 when uninspected and −3 when inspected, cheating earns \(q(1-4p)\), where \(p=1-(1-q)^k\). It remains profitable when
     \[
     q<1-(3/4)^{1/k}.
     \]
     For \(k=16\), that is approximately 0.0178. **My prediction:** SR leaves a low-q escape channel whenever the grammar contains such mixers; its benefit depends on the available q grid, not sampling alone.
   - “ZT+SUS reaches at least 0.5” is overconfident. Blocking direct invasions does not remove neutral shadows or guarantee entry into the protected family. **My prediction:** direct targeted exit rates fall more reliably than stationary inefficiency; remaining flow concentrates through shadows and other routes.
   - The price prediction assumes SR pays all 16 levels on the relevant selected paths. **My prediction:** its disadvantage depends on encounter composition and early stopping, not simply nominal k.

4. **Missing controls/cheap additions**
   - Add hand tests against every stored exploiter, timeout-triggering compliant programs, and mutually reading programs—not just constants and light cheaters.
   - Add a small q-grid payoff/invasion sweep around each SR profitability threshold.
   - Report realized read costs, timeout frequencies, entry rates, shadow routes, and paired lottery uncertainty at the **run**, not island, level.
   - Include an unconditional-inspect comparator to distinguish detection benefits from commitment.

5. **Alternative explanations**
   - Gains could reflect displaced inspector prior mass, favorable timeout conventions, or increased accessibility of a protected class rather than robust inspection.
   - Unchanged lottery efficiency could mask substantial changes in winners, establishment probability, or transient duration.
