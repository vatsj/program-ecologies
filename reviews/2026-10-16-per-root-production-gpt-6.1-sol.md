# Review of `specs/2026-10-16-per-root-production.md` by gpt-6.1-sol

### 1. Design flaws/confounds and fixes

- **The cache/trigger semantics are underspecified.** If the invariant key includes the mutable script list, appending or evicting a script can invalidate the mark and restart failed attempts. Conversely, a persistent mark can suppress regeneration after eviction. Specify production, validation, marking, and eviction order; test repeated failure, append, eviction, and return to an earlier root. Establish a retry bound—or explicitly report that none exists.
- **R2 needs a realizability audit, not just an ideal-table success.** “One extra check” must include constructing the shadowed alternative, locating the branch, checking it, and making it available within fuel. Require a source-executed trace showing that every appended script is produced without host-only branch information and remains sound after list changes.
- **Executed comparisons risk historical confounding and winner selection.** Rerun matched R0 and H-full at each fuel under the same implementation, rather than relying only on earlier cells. Predeclare how “best R3” is selected; choose on the 20 development streams and evaluate untouched confirmation streams.
- **The acceptance criteria and falsifiers disagree.** For example, R2 can miss H-full by substantially more than 0.1 without triggering prediction 1’s falsifier. Define success, failure, and inconclusive regions for each prediction, including interval treatment and whether both stream sets must pass. Specify whether “fair share” means terminal share or a time average.

### 2. Predictions likely wrong

- **“No overhead returns” does not follow from invariant marking.** Root-specific failures can create many distinct keys; list changes and eviction may cause further work. I predict low median overhead can coexist with expensive regrowth encounters and fuel failures. Measure cumulative charged work and upper quantiles, not just medians.
- **The k = 2 cap is not yet justified.** Two pivotal paths need not mean at most two scripts suffice across a program’s encountered roots. FIFO may evict precisely the script needed when an earlier root recurs. My prediction is that k = 2 works only if the static analysis establishes a small validity cover; otherwise its loss will be history-dependent.
- **R2 ≥ 0.4 at 3·10⁶ is overconfident.** Free certificates establish neither endogenous production timing nor the remaining fuel margin. I expect improvement over R0, but potentially a substantial gap from matched H-full.

### 3. Missing controls / cheap additions

- Add **S₃ + shadowed alternatives without the per-root trigger** on ideal confirmation streams. This completes the factorial test and separates the two changes and their interaction.
- On a few fixed encounter traces, compare rules without evolutionary feedback: eligible roots, successful writes, valid coverage, checks, and fuel exhaustion.
- Replace “pivotal-script fraction” alone with a checkpoint intervention: suppress each newly written script at the first fair nucleation event and replay. Provenance alone is not causal attribution.
- Report wage-state occupancy and transitions, first-fair time, loss/regrowth counts, and persistence. Extend a small subset beyond 10,000 to distinguish recovery from delayed transients.

### 4. Alternative explanations not ruled out

- R2 may work through redundant fallback scripts or altered script-search order rather than specifically second-path coverage.
- A higher terminal fair share may reflect earlier nucleation rather than greater stability.
- Results may depend on the library prior’s particular branch structures and founder coalitions; the optional N = 200 panel cannot establish large-population behavior.

### 5. Beyond this experiment

Derive the minimum script-validity cover over reachable roots, plus its production cost. This would turn the cap choice from a heuristic into a structural criterion and distinguish memory-limited from fuel-limited realizability.
