# Review of `specs/2026-10-05-dollar-partitions.md` by gpt-6.1-sol

## 1. Design flaws/confounds and fixes

- **“Outcome-frozen” is not an absorbing state.** On-path shadows can drift without changing the partition, then enable a different convention; migration can also restart change. Stopping there biases both partition frequencies and coexistence lifetimes. Stop only at a verified closed class under the actual kernel, or continue to the horizon and report censoring plus post-freeze escape rates.
- **The role comparison changes several things simultaneously:** population structure, available syntax, correlation, and potentially prior normalization. It cannot attribute differences to `ROLE`. Add a one-population/no-`ROLE` arm; where feasible, cross signal availability with population structure. Report the induced prior over behavioral classes in every arm, including constants-only baselines.
- **Specify the fixed-role mutation chain before running it.** Its states must be *joint* resident configurations, with mutations and fixation occurring in a specified slot. State slot-update rates, fitness mapping, and whether N means per-slot or total population. Validate the sequential-fixation approximation against small joint-population simulations; persistent polymorphism would invalidate a monomorphic reduction.
- **The primary comparison is last in the execution queue.** The budget could expire after only the `ROLE` arm. Run static tables and N=100 chains for both role structures first, then matched lotteries.
- **Two reporting definitions are incorrect.** In `dollar5`, \(|d-1/2|\ge1/3\) includes only 1/6–5/6, not 1/3–2/3. Also, slot symmetry implies equal *expected slot payoffs*, not payoff 1/2 unless efficiency is certain. Define demand, realized payoff, and normalized share separately.

## 2. Predictions likely wrong

- **Prediction 4’s “fewer exits ⇒ more stationary mass” argument fails.** Stationary weights depend on incoming rates too. A continuous-time nearest-neighbor walk with symmetric edge rates has uniform stationary mass despite endpoints having fewer exits. Establish which moves are actually adjacent, then compute prior-weighted entry and exit rates. My prediction: unequal splits may collectively dominate simply because there are four unequal ordered splits versus one fair split; endpoint enrichment is unestablished.
- **Prediction 1 overextends two-strategy risk dominance.** The 5/8 crossing supports 50–50 against `ROLE`, not against the full reader/shadow transition network. Mutation-entry weights and neutral paths can determine the large-N distribution. I predict a fair advantage in the restricted contest, but no justified ≥0.6 bound for the full grammar.
- **Prediction 3 is directionally plausible but overstated.** At 40% S3, the stated payoffs are 0.35 versus 1/3: only a small advantage. Fixation probability depends on N, fitness mapping, and resident shadows. Predict S3 wins increasingly reliably with N for pure-constant merges, not a universal probability across arbitrary island end states.

## 3. Missing controls/cheap additions

- Sweep merge shares around the predicted S3 threshold, **3/8**, using both pure representatives and sampled end states.
- Add **m=0** lotteries to separate seed-basin selection from migration.
- Keep n matched across arms; report cutoff sensitivity before claiming large-population behavior.
- Use run-level uncertainty intervals: islands within a run are not independent replicates.
- Include direct constant-to-constant transitions alongside conceder paths, and quantify their rates.

## 4. Alternative explanations not ruled out

Observed fairness or inequality could reflect syntax/prior multiplicity, cutoff artifacts, finite-time trapping, founder sampling, or migration-mediated basin selection—not stochastic stability or a generic advantage of source reading. Total unequal mass alone is especially weak evidence for an inequality preference.

## 5. Beyond this experiment

Nothing material.
