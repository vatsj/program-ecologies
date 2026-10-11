# Review of `specs/2026-10-11-certificates-as-genes.md` by gpt-6.1-sol

## 1. Design flaws/confounds and fixes

- **C-only has no specified source of certificates.** With empty founding lists, copying cannot create the first script; the empty-list state is invariant. Any preloaded scripts instead constitute an exogenous seed subsidy. **Fix:** specify initialization explicitly; distinguish empty C-only, C-only with a declared certificate seed, and CS-only with empty lists. Track host ancestry, not just the most recent transmission.

- **The executable object and soundness boundary are underspecified.** Does quoted “own code” include mode and mutable lists? Do certificates prove behavior under production charges and subsequent list changes? Soundness of milestone-4 carriers does not automatically cover stateful wrappers or depleted fuel. **Fix:** define the certified proposition, quote identity, state semantics, and fuel allocation; prove adoption preserves it. Test accepted scripts followed by production-induced timeouts and list mutations.

- **“Charged fuel” is not necessarily a selective price.** If steps only consume a cap and do not reduce fitness below that cap, the ALLC price-ladder analogy is invalid. **Fix:** specify the steps-to-payoff mapping separately from timeout behavior; report both.

- **Static payoff tables and source-only lumping are inadequate for inherited lists.** Identical sources with different lists have different transitions; encounters change future payoffs. **Fix:** key state by source, mode, and certificate inventory, with explicit encounter/update ordering. The chain diagnostic must include that state or be labeled a frozen-inventory approximation.

- **The proposed scaling conclusion lacks a scaling design.** One population size plus a chain at another size cannot establish an α = 1 schedule; encounter novelty, reproduction, and horizontal transfer determine amortization. **Fix:** add a small matched size sweep and measure acquisition cost per lineage, turnover, and encounters before replacement.

## 2. Predictions likely wrong

- **1 and 5:** Two empty C-carriers cannot bootstrap each other. Even a donor’s valid script need not validate against every distinct recipient. Predict no certificate-mediated cooperation from empty C-only, and restoration only along empirically verified script-transfer edges.

- **4:** Calling H a host subsidy does not remove its advantage from the experiment. H receives free production and can seed C; C pays acquisition costs. With identical inventories and play, modes may become neutral. Predict H advantage during acquisition, followed by neutrality or inventory-dependent selection—not systematic C/CS dominance.

- **3:** Refusal establishes nonacceptance, not high cost or deleteriousness. Invalid scripts may reject cheaply; a defector may still earn exploitation payoffs. Predict zero acceptance only under the established soundness assumptions; relative fitness remains empirical.

- **6:** An 80% inherited fraction depends strongly on replacement rate and provenance conventions. No skeleton-count bound follows without canonicalization or a demonstrated bound on accepted script variants.

## 3. Missing controls / cheap additions

- Pair seeds and encounter schedules across arms; compare **identical initial inventories** as well as empty inventories.
- Add C with publication disabled, inheritance disabled, and one explicitly introduced donor: separate horizontal transfer, vertical inheritance, and bootstrapping.
- Measure the directed script-transfer compatibility graph before populations.
- Add repeated invalid-script encounters and negative-result caching; measure checker burden on both parties.
- Report unconditional establishment probabilities and censoring-aware establishment times, not medians only among successful runs.

## 4. Alternative explanations not ruled out

Apparent C success could reflect host-seeded ancestry, inventory incumbency, or demographic copying rather than endogenous production. Failure of universality could arise from identity cliques rather than acquisition costs. Increased cooperation could reflect selective timeouts suppressing defectors rather than cheaper verification.

## 5. Beyond this experiment

Nothing material.
