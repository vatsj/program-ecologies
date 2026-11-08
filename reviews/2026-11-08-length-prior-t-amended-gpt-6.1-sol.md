# Review of `specs/2026-11-08-length-prior-t.md` by gpt-6.1-sol

## 1. Errors, contradictions, unsound mechanisms

- **2b does not specify a normalized law.** “Constants at the step-1 measured constant law, a junk program J … at the step-1 junk mass, bullies at the measured β, and readers at δ” conflicts with “constants … total 1 − δ − βδ − 0.01·δ/0.09,” which leaves no junk allocation. **Fix:** hold junk mass \(j\) fixed, allocate readers \(\delta\), bullies \(\beta\delta\), explicitly specify exploiters, and assign the remaining nonnegative mass to constants using their conditional proportions. Define what happens to omitted families.

- **The coding probabilities and claimed lengths disagree.** “A prefix-free code … each node draws its tag uniformly” over 18 tags conflicts with “class mass, \(2^{-\text{code length}}\).” Equiprobable tags cannot each have an integer-length binary code. Elias-γ also excludes zero. **Fix:** specify an actual binary prefix code, including a zero-to-positive mapping, or retain the branching probability model and use products of probabilities—not integer code lengths.

- **The proposed conclusion is a false dichotomy.** “Any positive length-prior mass suffices” versus “the length prior fails at every size” does not follow from copy-count versus fraction thresholds. A fractional threshold may lie below the prior’s mass; establishment, spatial coverage, and spoiler supply may scale differently. **Fix:** state finite-grid findings only; treat scaling laws as competing hypotheses, not exhaustive asymptotic conclusions.

## 2. Design flaws/confounds

- **The join is not a length-prior experiment.** Family masses are insufficient when dynamics retains T’s within-reader 2:1 mixture, although “a length prior makes [two-partner readers] far rarer,” and omits other conditionals. The single-reader-only slice does not validate the actual mixture. **Fix:** use measured within-family distributions in 2b; add a sampled finite-term-prior arm or label the join a library projection, not evidence that the length prior succeeds.

- **Behavioural equivalence ignores selection-relevant costs and source interactions.** Output probes do not capture failed-read charges; one forfeiting J need not reproduce junk with multiple failed reads. Matching against library probes does not establish equivalence against newly sampled programs. **Fix:** classify output *and charge* signatures, test representative sampled-program interactions, and retain separate junk cost classes.

- **Rare-class estimates cannot support the join.** Shortest-spelling lower bounds and counts over three sizes provide no useful upper bound on all longer spellings. Uncertainty in \(\delta_{\rm LP}\) and β can straddle the entire dynamic threshold. **Fix:** require certified residual-mass bounds or validated rare-event estimation; otherwise report only one-sided conclusions.

## 3. Predictions likely wrong

- **RE1–2:** raw reader count is unlikely to collapse thresholds across N and I. Readers must establish locally, and increasing I adds islands to colonize; fixed \(mN\) and horizon do not preserve migration geometry. Predict imperfect collapse and weaker improvement with I than RE2 asserts.
- **RE4:** library-term node gaps do not bound behavioural class masses. Shorter implementations, redundant spellings, and payload costs matter. Predict the stated \(10^{-8}\) bound will remain unsupported without a shortest-program/class-mass argument.

## 4. Missing controls/cheap additions

Add matched-count cells holding \(IN\delta\) fixed; independently vary founder and tail reader doses. Extend near-threshold runs in time. Report nonmonotone dose responses rather than automatically interpolating a unique threshold. Validate the full binary code and mass accounting without pruning ill-typed/stuck terms out of the prior.

## 5. Alternative explanations

Apparent count scaling could reflect finite-time colonization or suppression of unequal founders, rather than reader supply alone. R1 gains could come from altered junk/constant distributions rather than cheaper reading. Controlled mixture swaps would distinguish these.
