# Review of `specs/2026-10-05-island-path.md` by gpt-6.1-sol

## 1. Design flaws/confounds and fixes

- **The experiment does not directly test Pareto efficiency.** Rival persistence, network universality, and efficiency are different outcomes. Report local and metapopulation \(P(C,C)\), explicitly specifying whether interactions are within islands or include cross-island encounters. Do not treat failed homogenization as failed efficiency.

- **The “boundary path” is not calibrated, and pre-seeded cells cannot establish independent nucleation.** The rule uses an extrapolated \(T_{\rm nuc}\), although migration itself can change nucleation times. Define \(q\), its denominator, and the nucleation stopping event. Calibrate no-migration iid nucleation times at all three \(N\), including their distributions; use iid ancestry-tagged controls to measure migration-induced loss of local establishment. A seeded survival statistic is not that control.

- **The hazard’s unit is unspecified.** \(mN\,\rho_{DD}\) is a per-recipient approximation, not automatically the metapopulation separation-loss hazard. Source composition, recipient counts, establishment, and subsequent colonization all matter. Specify the exposure denominator and report successful invasions separately from global resolution. Treat bridge absorption and rival replacement as competing mechanisms; define whether “both-present” means any individuals, island holders, or majority networks.

- **Propagule sampling changes more than clustering unless implemented carefully.** Specify sampling with/without replacement, mixed-source composition, simultaneous replacement, and whether donors lose individuals. Validate against an unskipped implementation in small cells; default-kernel regression tests do not validate the new batch kernel.

## 2. Predictions likely wrong

- **Prediction 2 lacks the relevant scaling variable.** \(k=30\) is 15% of an \(N=200\) island but only 7.5% at \(N=400\), versus the cited successes at 20–40% for \(N=100\). Constant \(k\) need not defeat a barrier growing with \(N\). I predict materially less resolution at 400 than 200, potentially missing the stated threshold.

- **Equal flux does not imply a small nucleation penalty.** Bursts can destroy near-critical founder clusters or import already coordinated competitors. Conversely, long migration-free intervals may help nucleation. I predict a substantial, potentially nonmonotone change in \(q\), not a justified bound of 0.15.

- **Prediction 3 is overconfident at increasing \(I\).** More islands create more opportunities for early rival establishment. Compare measured colonization time with the interval between first and second rival establishment. I predict separation increases with \(I\) unless colonization demonstrably outruns that interval.

- **Bridge majority is not implied by bilateral cooperation.** It requires an invasion advantage against each rival and resistance to displacement. Predict bridge growth during conflict, but not necessarily majority in 60% of runs.

## 3. Missing controls / cheap additions

- Add \(k/N\)-matched propagules, e.g. \(k=60\) at \(N=400\), alongside fixed-\(k\) cells.
- Measure static invasion probabilities in both directions for A, B, and bridge, at actual \(N,k\).
- Record first establishment, first immigrant-founded island, second rival establishment, and extinction times.
- Report binomial intervals: 40 runs poorly distinguish several prediction and falsifier thresholds. Predeclare verdicts for the gaps.
- Fix cell priority and stopping rules before runtime-based truncation.

## 4. Alternative explanations not ruled out

Bridge success could reflect prior abundance or intrinsic dominance rather than conflict mediation. Homogenization could reflect initial occupancy asymmetry rather than nucleation-time advantage. Merge winners are conditional on survival and on changing interaction structure; they do not identify the island mechanism.

## 5. Beyond this experiment

Nothing material.
