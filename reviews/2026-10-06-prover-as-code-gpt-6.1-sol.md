# Review of `specs/2026-10-06-prover-as-code.md` by gpt-6.1-sol

### 1. Design flaws/confounds and fixes

- **“Actual run under K” is underspecified.** A nested simulation’s local fuel, the outer evaluator’s remaining fuel, and a fresh top-level allowance are different quantities. A proof about a fresh-K run need not describe a simulation interrupted by its caller. **Fix:** index evaluation propositions by configuration and explicit remaining fuel; specify fuel consumption through nested evaluation, search, and timeout-to-action conversion. Include K in the quoted target where necessary.

- **Inlining the prover does not establish soundness by construction.** PrvR/PrvL, Nec, and especially JLöb previously concerned the primitive’s semantics. Their code-level replacements may require new bounded reflection obligations; ordinary derivation-size induction does not automatically discharge these. **Fix:** state every revised rule and its semantic obligation before running counted cells. Independently validate JLöb’s budget conditions. If they fail, report failure rather than silently repairing the calculus.

- **Three budgets are conflated:** derivation-size bound b, search work, and execution fuel K. `search_b` both enumerates by size and “stops at budget b,” while predictions compare b with execution steps. **Fix:** use separate symbols and stopping conditions. Report candidate generation, checking, and total search work separately. Node-checking cost alone cannot predict search completion.

- **The correctness criterion censors expensive failures.** Agreement only on queries finishing within K can leave the difficult cases entirely untested. **Fix:** report coverage, exhaustion, and interruption separately; ensure some nontrivial positive and negative catalogue queries complete. Define `Refuted`: exhausted bounded search means “no proof within this bound,” not semantic falsity.

### 2. Predictions likely wrong

- **Prediction 3’s visibility theorem is not generally valid.** Proofs need not reproduce an execution trace: structural reasoning or Löbian reasoning can certify runs much longer than the proof/checking computation. **My prediction:** no universal runtime lower bound without a restrictive trace-only calculus. Cooperation regions will depend on search order and fuel semantics; neither a rectangle nor departure from a min-rule follows automatically.

- **Prediction 1 estimates search cost from an eight-node witness.** Enumerating candidates before finding that witness may dominate checking by orders of magnitude. **My prediction:** compilation overhead and candidate count, not witness length alone, determine feasibility.

- **Prediction 2’s high-k conclusion does not follow.** SF simulates FairBot against itself, not necessarily the current reader; completing that simulation does not imply every sound reader reciprocates. **My prediction:** soundness rules out certified cooperation with an actually defecting target *only when the certified target matches the executed run*. Mutual cooperation requires additional program-specific arguments.

- **Prediction 5 mistakes proof validity for behavior.** Sound FB may correctly prove that SC cooperates even when SC’s own derivation is invalid. **My prediction:** replay rejection alone does not force FB to defect. Bounded Gödel II likewise requires re-establishing the relevant code-level assumptions.

### 3. Missing controls or cheap additions

- Test identical source with different K and nested residual fuel, especially just across timeout boundaries.
- Benchmark checking a supplied witness separately from searching for it.
- Add deliberately corrupted side conditions and small exhaustive evaluator/checker tests independent of the host prover.
- Freeze predictions before performance-driven catalogue reduction; retain mandatory semantic tests after reduction.

### 4. Alternative explanations not ruled out

Apparent leak closure could be universal timeout or lost self-cooperation. Budget asymmetry could reflect syntax-dependent enumeration order rather than visibility. Host/term agreement could preserve a shared checker bug. Finite-K plateaus do not establish eventual stabilization.

### 5. Beyond this experiment

nothing material
