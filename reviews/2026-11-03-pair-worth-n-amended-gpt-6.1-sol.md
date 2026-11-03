# Review of `specs/2026-11-03-pair-worth-n.md` by gpt-6.1-sol

## 1. Errors and unsound mechanisms

- **Transition counts are not ε-free rates.** “core entry and exit events per island-generation … these are encounter-level, ε-free quantities” conflicts with “annealed tail ε(t).” These are composition-dependent population transitions, potentially caused by mutation or migration; debouncing also changes their count. **Fix:** call them finite-schedule transition rates, report at-risk exposure, separate tail-on/chase periods, and estimate ε-free per-mutant rates with controlled introductions.

- **Confirmatory scoring is impossible as specified.** “Scored on confirmatory runs (20–59)” conflicts with “C+B\* at δ ∈ {0.0125, 0.15, 0.5}, 20 runs each” and other 20-run prediction cells. Mandatory cells can also be cut despite predictions requiring complete samples. **Fix:** give every prediction an explicit cell/run-index manifest; designate cut predictions unscored, not failed.

- **Self-consistency does not establish modal play.** “the disjunct containing the true tuple holds self-consistently” is not a Löbian argument. Moving only the fallback atoms to level 1 does not prove the grand guard works. **Fix:** specify the grand guard’s box level, prove the joint implication needed for Löb, and make evaluator agreement a launch gate. Exhaust all share triples, including infeasible ones, rather than merely sampling them.

- **F₄ is not core-restricted.** “σ_i ≤ 4/6 only … separates failures from non-core grand splits” overlooks feasible triples whose demands sum below 1. Bounding individual demands does not ensure core membership. **Fix:** report slack separately; describe F₄ as removing excessive individual demands, not non-core outcomes generally.

## 2. Design flaws and confounds

- **T is a count, not an establishment probability.** In mean-field payoff evaluation, founder triples are not discrete encounters. Ten compatible triples can share the same scarce lineage and disappear together. **Fix:** report probability of any compatible founding support, occupied split types, minimum slot abundance, and establishment conditional on those statistics.

- **Matched T does not isolate supply from N.** Changing δ with N also changes bidder frequency, constant displacement, mixed-bid interactions, and selection during establishment. **Fix:** retain a small factorial N×δ panel and add fixed-count, same-split founder inoculations across N. Treat matched-T comparisons as suggestive, not causal identification.

- **F versus G changes fallback behavior as well as reading.** Their equivalence holds only against compatible grand constants. **Fix:** add F without pair fallback and a matched infeasibility-response control.

## 3. Predictions likely wrong

- **RE 7’s neutral-exit scaling is unjustified.** A neutral mutant’s fixation probability scales as 1/N; aggregate exits additionally depend on arrival flux, migration, resident diversity, and observation time. **Prediction:** raw per-generation hazards will not generally follow 1/N; controlled per-introduction exits may.

- **RE 4’s near-equivalence is too strong.** F activates a mutually compatible pair fallback exactly where G cannot coordinate. **Prediction:** differences concentrate in infeasible encounters and can generate a substantial pair excess, not necessarily a reading premium.

- **Argon’s I·T mechanism is insufficient.** Migration transfers individuals, not assembled triples. **Prediction:** rescue depends on lineage survival and assembly times, not simply total compatible-triple count.

## 4. Missing controls or cheap additions

- Log mutation/migration ancestry at transitions.
- Add a small longer-chase subset: the current horizon grows with N.
- Fix common-random-number coupling explicitly; arm-dependent seeds alone do not establish pairing.
- Separate Pareto efficiency, full allocation, and core membership throughout.

## 5. Alternative explanations not ruled out

N-dependent transient duration; migration-assisted lineage assembly; neutral replacement by constants; selection among splits rather than increased grand-coalition supply; and annealed-tail exposure interacting with population size.
