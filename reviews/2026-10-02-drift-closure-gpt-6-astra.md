# Review of `/Users/jstav/code/program-ecologies/.claude/worktrees/agent-a6406f269565d9ef7/predictions/2026-10-02-drift-closure.md` by gpt-6-astra

## 1. Design flaws/confounds and fixes

- **Stationarity versus numerical absorption is the largest risk.** At finite \(N\), exponentially small transitions can determine stationary weights between near-closed classes. Dropping them and reporting an absorption lottery changes the object. Absolute cut-flow tolerances \(10^{-5}\) can also exceed the escape flux being measured. **Fix:** separate finite-\(N\) stationary results from explicitly initialized metastable lotteries; retain rare links in log space, and demonstrate threshold convergence relative to each relevant escape flux.

- **Proposition 2 is not established at its stated generality.** Lemma 1 classifies individual edges, not network residence times or entry scaling. “Non-closed” alone does not guarantee a \(1/N\) network exit: a network consisting only of suckerable states can exit at constant rate. Neutral-at-one-copy entry needs a positive slope, and competing noncooperative traps matter. **Fix:** state sufficient assumptions—fixed finite language/prior, an unsuckerable cooperative core, successful paths into it, and dominance of all-D outside it—and derive rates from the reduced chain.

- **The proposed “corner” falsifier does not test the corollary.** The corollary concerns neutral closure in the pure game; verdict 11 concerns finite-window slopes and family weights in modified games. **Fix:** distinguish theorem checks, asymptotic mechanism tests, and finite-\(N\) performance criteria. No fringe cell can falsify the pure-game corollary.

- **This is chiefly computational validation, not an independent prediction test.** Every cell already has a chain-derived estimate, sharing transition machinery with the full run. **Fix:** label it accordingly and add independently calculated fixation/hitting-probability checks.

## 2. Predictions I think are wrong

- **“Prior and grammar change constants, never exponents unless they create closure” is too broad.** Grammar changes can alter entrance barriers and noncooperative recurrent structure without creating cooperative closure. My prediction: boostPB preserves the exponent; the general grammar claim requires additional conditions.

- **The universal leak floor is overstated.** Positive universality does not imply direct cooperation with FairBot—P* is your own example. Even a direct \(x\to FB\to ALLC\) path does not establish a per-event network escape floor without residence-time accounting. I predict \(1/N\) scaling for the listed pure-game cores, but not the advertised uniform constant.

- **Proposition 3’s conclusion exceeds its argument.** The ALLC inequality is sound, but positive universality does not make FairBot an on-path-neutral newcomer. Prices may interrupt an indirect path elsewhere. Predict local incumbency along a blocking edge, not necessarily \(c(FB,y)>c(y,y)\).

## 3. Missing controls / cheap additions

- Repeat representative high-\(N\) cells with substantially tighter truncation thresholds.
- Add one larger \(N\) for D, CD, and μ; compare \(N\,r_{\rm exit}\) and exponential-barrier fits, rather than treating a two-point slope as asymptotic.
- For addP12b, include its natural siblings/fakers at ordinary grammar-induced masses. Adding a single advanced program conflates prudence with asymmetric language coverage.
- Publish explicit residual-leak paths and independently computed barrier heights for each claimed closed/nonclosed family.

## 4. Alternative explanations not ruled out

- P* dominance may reflect entry accessibility or basin size, not minimum leakage.
- μ-fringe success may be externally imposed strategy-specific fitness ranking rather than an endogenous standing-variation mechanism.
- Multiple observed blocks may be metastability, not multiple asymptotic stationary networks.

## 5. Beyond this experiment

The crucial extension is **uniformity in language size**: characterize how leakage constants and crossover populations scale with \(n\). Fixed-\(n\) \(N^{1/2}\) laws can coexist with different joint-limit behavior as increasingly prudent programs become available.
