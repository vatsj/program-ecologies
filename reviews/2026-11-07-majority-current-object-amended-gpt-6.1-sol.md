# Review of `specs/2026-11-07-majority-current-object.md` by gpt-6.1-sol

## 1. Errors, contradictions, unsound mechanisms

- **Outcome weighting is not a stricter success measure.** “expected-payoff-weighted outcome distribution puts ≥ 0.9 on fair pairs (a stricter reading)” conflicts with measuring actual play: payoff weighting suppresses disagreement and waste, and need not imply that modal programs form a fair pair. **Fix:** use the unweighted encounter distribution induced by population frequencies; report modal classification separately, without claiming nesting.

- **The counter’s timing mechanism is arithmetically false:** “over half of the tail’s arrivals come later” than consolidation at “10N–20N.” Approximately 94% arrive before 10N; only about 3.2% of delivered arrivals occur after 15N. **Fix:** mark this timing explanation refuted analytically before running; score its numerical outcome prediction separately.

- **Reproduction gate permits unjustified relaxation.** “reproduces … per-run records exactly” becomes “within the stored interval” if “horizon, snapshots” change. Extra observations and a later endpoint should not change the trajectory through 100N. **Fix:** require exact prefix reproduction with observational snapshots and separate RNG streams; distributional agreement is not a substitute unless an actual kernel change is specified and independently validated.

- **Establishment attribution is undefined:** “for each family the number of arrivals that reach > N/2 copies.” Arriving programs may already exist, and subsequent arrivals/migration add identical copies. **Fix:** track neutral lineage IDs through reproduction and migration, or explicitly measure genotype-frequency crossings rather than arrival establishment.

## 2. Design flaws/confounds

- **D2 does not isolate a founding mechanism generally.** “D2 against D1 isolates what the founding seed holds” identifies only the founding intervention *conditional on a clean tail*. Renormalization also increases every retained family’s mass. **Fix:** add clean founding/full tail to complete the factorial, plus a matched-mass removal control before attributing effects specifically to victims/bullies.

- **M–T contrasts change library, prior, evaluator and costs simultaneously.** They describe two packages, not the causal benefit of realizable reasoning. **Fix:** retain that descriptive interpretation; add a constants-only T control with matched constant proportions.

- “the a = 1 case is settled” and “the mean-field result … does not describe the object” overstate finite-schedule evidence. Fixed I = 64 and horizon proportional to N cannot distinguish a basin from slow escape or establish a large-population limit. **Fix:** restrict conclusions to tested cells and schedules.

## 3. Predictions likely wrong

- **RE 8b:** expecting the same ≥0.15 clean-tail improvement at N = 200 ignores the reported threshold growing faster than N. **My prediction:** improvement decreases with N; Λ = 100 may be insufficient at 200.

- **RE 5:** a beneficial demand increase does not establish a ≥0.10 aggregate reduction. Its arrival probability, establishment probability and tail-free cleanup remain unspecified. **My prediction:** effects depend strongly on residual W composition; the common quantitative bound across arms fails.

## 4. Missing controls / cheap additions

- Extend selected failing/successful cells to 240N without further arrivals.
- Compute exact fair-pair encounter probabilities and total material surplus; unequal pairs and grand coalitions can be Pareto-efficient despite missing V*.
- Verify slot-permutation equivariance of priors, tables and modal tie-breaking. Use exact multinomial tests and confidence intervals for pair probabilities; failure to reject uniformity does not establish equality.
- Validate V5’s claimed neutrality across intermediate mutant frequencies, not only the single-mutant endpoint.

## 5. Alternative explanations

Founder sampling, migration-driven consolidation, transient polymorphism and prior-mass redistribution can explain observed differences without tail-mediated basin escape or a source-reading advantage. The proposed endpoint and post-arrival association measurements do not distinguish these mechanisms.
