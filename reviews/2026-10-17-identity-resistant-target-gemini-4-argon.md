# Review of `specs/2026-10-17-identity-resistant-target.md` by gemini-4-argon

### 1. Design flaws or confounds

* **Control vs. drop-order contradiction:** Prediction 5 explicitly requires "the R-proportional control's identity takeovers under rain", yet the **Cells** section omits the control from the Rain cells ("under L and R-move"), and the **Scale guard** lists "the control under rain" as the first item to drop. If dropped or not run, Prediction 5 is untestable and you cannot tell whether R-move works by *removing* exploitable target shadows or by *amplifying* resistant founders. **Fix:** Explicitly include R-proportional control in the `(800, 8)` rain cell and move it *after* `N = 1,600` rain in the drop order.
* **Target-definition confound (`uot`):** The brief narrows the normative target (from 235 to 70 units), while `R-move` zeroes out the prior mass of the 165 exploitable target units. Is `uot` (universal-on-target) scored on the old 235-unit target or the new 70-unit resistant target? If scored on the 70-unit set, `L` is heavily penalized for drifting into the 165 neutral shadows that `R-move` cannot even generate—making a comparison of `uot` tautological. **Fix:** Report both `uot_235` and `uot_70` across all priors, or evaluate `R-move` solely via `universal-open` and `identity_share`.
* **"Paired founders" across different supports:** You cannot literally pair initial founder draws across `L` and `R-move` when `R-move` sets 165 positive-mass units in `L` to zero. **Fix:** Specify the coupling: draw uniform $U(0,1)$ seeds per individual and map via the inverse CDF of each prior, or explicitly remap any founder drawn from the 165 exploitable units under `L` to a resistant unit in `R-move` proportionally.

### 2. Predictions you think are wrong

* **Prediction 1 (Syntactic property):** Likely **wrong** (falsifier ≥ 10% will trigger). "Exploitable" is defined semantically against identity holders with positive prior mass in the finite grammar cutoffs. Some target units will lack a literal `CHK(them, me, C)` guard—e.g., guarding on a behavioral or structural check that happens to exclude the specific TwinD/identity templates present at this cutoff—and will therefore be classified as semantically *resistant* without having the syntactic signature. **My prediction:** Semantic resistance will be a strict superset of the syntactic signature, violating the exact correspondence on >10% of the 70 resistant units.

### 3. Missing controls or cheap additions

* **Non-target unconditional shadow takeover rate (Static / Rain):** When the 165 exploitable target units are removed in `R-move`, does neutral drift out of the 70 resistant units simply route into non-target unconditional cooperators (`ALLC` equivalents) during rain? Log the rate at which resistant islands drift to *any* unconditional cooperator under rain, not just the 165 target shadows.
* **Scramble establishment rate of the 70 resistant units:** In the static/scramble analysis, compare the per-founder establishment rate of the 70 resistant units vs. the 165 exploitable ones. `if(CHK(them,^D,D),C,D)` is a defection-detector that exploits the sucker fringe during the scramble; removing it might unexpectedly raise scramble failure rates at $\varepsilon=0$.

### 4. Alternative explanations the brief does not rule out

* **Founder-boosting vs. channel-closing:** If `R-move` improves `uot` under rain (Prediction 4), it may not be because the rain entry channel is closed, but because concentrating all 235 units' prior mass onto the 70 strictly prudent units acts like a massive seeding boost (similar to the sponsored PrudentBot founder), crushing rivals at $t=0$ before rain even matters. The `R-proportional control` *must* be run under rain to rule this out.

### 5. Ideas that matter for the research program

* **Prior surgery vs. endogenous evolutionary pruning:** Zeroing out 165 syntactic templates in the mutation prior (`R-move`) violates the RS's commitment to keeping $\mu =$ length prior fixed and finding structural/ecological remedies (CLAUDE.md, 2026-09-30). If `R-move` works, it only proves a diagnostic ("these 165 units are the leak"). For the Turing-complete goal, you cannot hand-curate the compiler's prior to forbid `if(CHK(them,^D,D),C,D)`; you will need an *ecological* mechanism (e.g., an endogenous probe or a runtime cost on uncertified cooperation) that selects against the 165 units under the standard length prior `L`.
