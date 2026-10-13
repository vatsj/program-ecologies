# Review of `specs/2026-10-13-sog-fully-realizable.md` by gpt-6.1-sol

### 1. Design flaws/confounds and fixes

- **Executable-table fallback changes the central question.** Ideal play plus an audit cannot establish fuel-bounded feasibility: timeouts alter play, certificate acquisition, and subsequent selection. **Fix:** require executable dynamics for the feasibility verdict, even on a reduced support. Label ideal-table results separately; validate any reduction on sampled executable trajectories.

- **Identity-aware lumping needs an explicit correctness condition.** Behaviorally equivalent but differently spelled programs need not be interchangeable under `eq` or ⌜T₁⌝. Certificate inventory and acquisition history can also change future behavior. **Fix:** retain source identities and relevant certificate states, or prove the aggregation preserves identity relations, transitions, and prior mass. Test distinct-source twins and identical sources with different inventories.

- **“Nonself” is underspecified for triples.** A worker has both a boss and another worker; production against a distinct boss might still certify a proposition involving an identical coworker. Prediction 2 depends on precisely which participant must differ. **Fix:** specify the production gate, certificate target, dependencies, and inheritance rules. Establish nonproducibility statically before treating it as a dynamical prediction.

- **The `eq` comparison also changes the prior and adds a named quote.** Raw arm differences cannot isolate identity’s effect from displaced open-militant/concession mass or the special status of T₁. **Fix:** add a matched-prior identity-disabled control and separate the named-quote addition.

### 2. Predictions likely wrong

- **Prediction 3’s mechanism is incorrect as stated.** B_eq reads w1; replacing the unread worker w2 cannot directly make it cut the wage. Indirect loss through worker behavior or subsequent boss replacement remains possible. **My prediction:** unread-slot substitutions leave B_eq’s immediate wage unchanged; the aggregate persistence effect of identity has uncertain sign.

- **Prediction 6 lacks a dominance argument.** B_eq avoids concessions to near-militants and can benefit from assortative matching or neutrally replace D* on exact-T₁ islands. Paying fair less often need not lower fitness. **My prediction:** closed shops can exceed their prior share in some cells; measure invasion fitness on actual resident compositions.

- **Prediction 5’s tail bounds are unsupported.** “One check” is not constant cost across triples; production may repeat expensive nested verification or fail within its cap. **My prediction:** median overhead can be modest while failures concentrate disproportionately in the tail. Fixed multiplicative bounds need static evidence.

### 3. Missing controls or cheap additions

- Define establishment, persistence, plurality, and holder classification before running; use common fixed-horizon endpoints despite adaptive extensions.
- Force a few named coalitions with empty inventories, then with valid preloaded certificates. This separates donor/bootstrap failure from inability to sustain cooperation.
- Report uncensored required-cost estimates separately from capped execution costs, failed attempts, and amortized production expenditure.
- Add local transition assays for unread-slot substitution, boss replacement, and union invasion; classify causal sequences rather than only the final exit event.

### 4. Alternative explanations not ruled out

- Certificate scarcity and bootstrap coordination, rather than identity incompatibility.
- Prior dilution and source-spelling abundance, rather than identity’s strategic value.
- Runtime-induced selection against complex open programs, rather than closed-shop superiority.
- Migration-driven replacement or long metastability, rather than durable persistence.
- Two population sizes at fixed island count and migration do not establish a large-population seed-path claim. Also report productive efficiency separately from wage fairness: an unfair wage can still yield Pareto-efficient production.

### 5. Beyond this experiment

Nothing material.
