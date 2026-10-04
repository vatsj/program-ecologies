# Review of `specs/2026-10-04-almost-all-seeds.md` by gpt-6.1-sol

## 1. Design flaws/confounds and fixes

- **The limits are conflated.** A persistent replicator endpoint does not establish efficient *finite-population absorption*: neutral drift can leave a non-strict equilibrium over arbitrarily long times. Fix: distinguish \(\lim_{N\to\infty}\lim_{t\to\infty}\) from \(\lim_{t\to\infty}\lim_{N\to\infty}\), and characterize reachable absorbing states and neutral escape routes. Treat replicator persistence as a diagnostic, not the candidate proof by itself.
- **Neither path establishes the proposed regime boundary.** Fixed \(I=4\) tests large islands, not a joint limit; fixed \(N=100\) tests increasingly many small islands. For a bad seed with probability approximately \(e^{-cN}\), its occurrence is controlled by \(I e^{-cN}\), not simply \(I/N\). Fix: add joint-growth paths and estimate bad-seed probabilities. Replace “\(N\gg I\) is necessary” with a hypothesis about those probabilities and subsequent spread.
- **“Freeze” needs an exact definition.** No observed changes, approximate replicator convergence, or within-island fixation need not mean absorption under migration. Fix: certify no accessible composition-changing transitions; separate certified absorption, metastability, and unresolved runs. Report time units and exactly how `mN=1` scales with \(N,I\).
- **The island comparison retains the acknowledged language confound.** Weak-with-X/`ROLE` versus modal cannot isolate unfakeability. Fix: include W0 in Object 2, using matched grammar/prior where possible.
- **Pre-registration currently excludes Object 1.** Commit predictions before static computation too. Predeclare budget reductions and report censored outcomes rather than comparing selectively shortened runs.

## 2. Predictions likely wrong

- **Prediction 4’s \(N^{-1/2}\) “neutral entry per landing” is unsupported.** A single neutral migrant’s fixation probability in the standard fixed-size neutral model is \(1/N\). The previously observed square-root scaling involved a different mutation/fringe balance. My prediction: isolated FairBot-versus-D entry is approximately \(1/N\), unless the island dynamics supply another mechanism; measure it directly.
- **Prediction 5 assumes survival implies takeover.** More islands increase opportunities for both cooperative and defecting configurations; takeover depends on directional migration fixation rates, not existence alone. I predict no guaranteed monotonic increase with \(I\).
- **Prediction 2’s argument is insufficient.** One faker invading one cooperator does not imply global convergence to defection across every prior and larger language. My prediction: low cooperation is plausible, but additional attractors or neutral faces must be checked.
- **“ALLC goes extinct first” is not literally a deterministic replicator event.** Positive coordinates remain positive at finite time. Specify asymptotic extinction or a numerical threshold; endpoint pruning can otherwise manufacture persistence.

## 3. Missing controls/cheap additions

- Add no-migration controls and reciprocal single-migrant fixation assays between the observed cooperative and defecting island states.
- Test endpoint perturbations toward neutral classes, especially ALLC, and small multi-class perturbations; zero invasion fitness does not imply nonlinear stability.
- Report binomial intervals: 20 runs cannot substantiate probability tending to one.
- Vary integration tolerances and verify residual growth rates. A coarse line toward uniform neither establishes a neighbourhood nor identifies a basin boundary.

## 4. Alternative explanations not ruled out

Efficient finite-horizon outcomes could reflect slow neutral leakage, favourable migration scheduling, cutoff-specific absence of spoilers, or the free sound oracle—not robust efficient absorption. Larger \(N\) can improve apparent success simply by delaying escape beyond the horizon. Averaged island cooperation can also conceal persistent heterogeneous states.

## 5. Beyond this experiment

The useful theorem target is a decomposition: **seed concentration + deterministic basin robustness + stochastic escape/spread bounds**, uniform in language cutoff. “Unfakeability” alone supplies none of those bounds.
