# Review of `specs/2026-10-25-encounter-contracts.md` by gpt-6.1-sol

## 1. Errors, contradictions, unsound mechanisms

- **Spontaneous dynamics are conditioned away.** “Spontaneous transitions do not enter the migration chain as jumps” and “relaxed further until a genesis-stable state is reached” conflict with genesis remaining active indefinitely. A 5,000-generation holdout cannot distinguish absorption from metastability. Repeated relaxation can bias the sampled states toward unusually long-lived classes. **Fix:** retain spontaneous transition rates on physical time; collapse only verified closed recurrent classes. Report unresolved metastability rather than declaring genesis stability.

- **BR lacks executable encounter semantics.** “Stage-2 actions are the encounter’s outcome,” but BR specifies that “S’s contract forms only if every member gains under every such reply.” Does BR change only acceptance, or actual play too? In the former case, installed contracts need not deliver their tested gains; in the latter, equilibrium selection and no-pure-equilibrium encounters remain undefined. **Fix:** specify BR play, fitness, tie selection, and no-equilibrium behavior; replay every accepted proposal under those exact semantics.

- **Capacity invalidates locality.** Contracts “don’t hinder the program elsewhere,” yet installation uses “least-recently-fired eviction.” A new contract can delete protection at another key. **Fix:** include eviction in candidate evaluation and the exhaustive oracle; log displaced entries and their subsequent consequences. Qualify the locality claim.

## 2. Design flaws or confounds

- **Occupation distributions do not automatically define migration states.** A recurrent island’s outcome-class frequencies omit hidden contract configurations and phase-dependent migrant susceptibility. Keeping full states helps, but does not specify how recurrent states are sampled. **Fix:** estimate the invariant distribution over full configurations and average migrant transitions against it; verify mixing relative to migration. Otherwise retain internal dynamics explicitly.

- **H versus R changes both access and prior.** H adds priced syntax, while R receives a free wrapper. Differences cannot be attributed solely to exposed-hook restrictions. **Fix:** use the same hooked-program population and prior in matched arms, varying only write eligibility; include inert-hook controls.

- **Large-population conclusions remain unsupported.** Mostly N = 100, with 50–200 sensitivity, cannot establish the large-N coordination barrier or efficiency limit. **Fix:** label conclusions finite-N and derive proposal-exposure/establishment scaling, with larger-N targeted tests if feasible.

## 3. Predictions likely wrong

- **Prediction 1 is partly circular:** settlement already requires no newly formed contract firing on path for 500 generations. Quietness measured in that window is selection by definition. **Own prediction:** selected quiet states can still have appreciable later hazards. Test fresh, fixed-duration windows without discarding failures.

- **Prediction 7 has no monotonicity basis.** Restricting hooks changes reachable attractors, and contractibility can expose holders to exploitation or replacement costs. **Own prediction:** H need not lie between 0 and R; hooked programs need not increase even where contracts fire.

- **Prediction 4’s falsifier measures power, not absence.** An interval including zero does not establish α = 0. **Own prediction:** rare positive transitions may remain unresolved. Predeclare an exposure budget and a scientifically meaningful upper-bound threshold.

## 4. Missing controls or cheap additions

- Replay accepted installations across **all affected encounter types**, not just the founding encounter; report signers’ expected-fitness changes.
- Pair R with a no-response substitution arm to isolate response from encounter-conditioned acceptance.
- Validate exhaustive-oracle stability against capacity, replacements, H eligibility, and the arm’s actual response semantics.

## 5. Alternative explanations not ruled out

Efficiency gains could reflect directed, payoff-filtered mutation rather than selection favoring contracts. Coverage could be maintained by spontaneous genesis rather than migration-mediated coexistence. R–BR differences could arise from BR’s worst-equilibrium acceptance rule rather than non-best-reply programs.
