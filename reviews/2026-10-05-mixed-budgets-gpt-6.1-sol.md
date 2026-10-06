# Review of `specs/2026-10-05-mixed-budgets.md` by gpt-6.1-sol

## 1. Design flaws/confounds and fixes

- **A is not a compatibility network.** Its budget-4 members conflict with other members. “Rival of A” and “bridge to A” can therefore conflate distinct pairwise rivalries with failure to cooperate with an entire incompatible set. **Fix:** make incompatible pairs of budgeted establishers the primary screening unit; report pairwise bridges and reachable mediator paths. Keep A₁₆ as a separately defined reference clique.

- **Incompatibility is not bridge-lessness.** The stated thresholds establish missing edges, not the absence of a third program connecting the endpoints. Moreover, FairBot₄ cooperates with FairBot₁₆ under the stated min-budget threshold. **Fix:** require exhaustive pairwise bridge enumeration before labeling either low-budget copy a hard rival. Distinguish direct-bridge-less from disconnected through mediator paths, and structural bridges from bridges actually seeded and surviving.

- **Fixed N, I, and horizon cannot settle large-population universality or permanent isolation.** Horizon separation can reflect slow bridge arrival or neutral absorption. **Fix:** call the main result finite-horizon incidence; add a small scaling panel for the decisive forced pair, varying I and horizon with the declared migration scaling. Report exposure-conditioned resolution hazards and censoring.

- **Prior changes also change establishment and migration timescales.** A common mN can compare different nucleation regimes rather than compatibility alone. “At the calibrated boundary” is specified but not operationalized in the run list. **Fix:** explicitly run both common-migration and prior-calibrated cells, reporting T_nuc and x = mN·T_nuc/N.

## 2. Predictions likely wrong

- **Prediction 1’s FairBot₄ claim is too strong.** It is already compatible with FairBot₁₆; whether it rivals the reference *pair* depends on the set-level definition. My prediction: budget-4 BOX creates genuine incompatible pairs, but the fraction that is bridge-less requires catalogue enumeration; the supplied thresholds do not justify either mass bound.

- **Zero hard mass above threshold is unsupported.** Budget 8 clears the two named programs’ thresholds, not every n = 8 establisher’s threshold; the context explicitly places PrudentBot’s survival threshold at 11. My prediction: the named core becomes connected, while catalogue-wide zero hard mass remains uncertain.

- **Prediction 3’s “budget is free, therefore no selection” reasoning is wrong.** Budget changes compatibility and hence colonization opportunities even without a direct cost. My prediction: holder budgets become establishment- and compatibility-biased; direction may depend on initial frequencies. No defensible quantitative bound follows from the prior.

## 3. Missing controls/cheap additions

- Add homogeneous-budget controls at 4, 8, and 16 using the same kernel and horizon.
- Report budget composition immediately after establishment, then at later checkpoints; this separates founder filtering from subsequent selection.
- Force one incompatible-but-bridged pair alongside the bridge-less pair; include bridge-present and bridge-absent seeds.
- Define composition distance, island weighting, separation, and efficiency denominators before running. Align falsifiers with predictions, especially prediction 1’s uncovered intervals.
- Use paired seeds across priors where feasible; report exact rare-event intervals rather than treating 0 versus a few events as categorical evidence.

## 4. Alternative explanations not ruled out

Persistent islands may reflect absent bridges in finite seeds, slow neutral takeover, prior-weighted founder success, or holder-rule artifacts—not a structural budget obstruction. High within-island P(C,C) may conceal extensive failed establishment or inefficient cross-island encounters; report both.

## 5. Beyond this experiment

nothing material
