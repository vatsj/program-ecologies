# Review of `specs/2026-10-17-legitimate-detectors.md` by gemini-4-argon

### 1. Design flaws or confounds

* **Lineage vs. individual grudge propagation (Cell A confound):** The brief says a grudge is "appended and inherited" after a partner defects. In Cell A (one predator arrives in a detector island of $N \in \{200, 800\}$), only the *single* detector struck in round 1 acquires the certificate and passes it to its offspring. The remaining $N-1$ naive detectors have no certificate and continue to be exploited by the predator (and its offspring) until they are individually struck. If matching is random, the predator lineage grows at the expense of the $N-1$ naive detectors much faster than the single immunized detector lineage grows.
  * *Fix:* Specify in the brief whether grudge genes spread only vertically (inheritance) or also horizontally via the existing skeleton-copying / donor machinery (`milestone 5`). If vertical-only, compute the expected strikes before a predator meets an immunized detector in §1 Static; otherwise Cell A tests vertical selective sweep speed, not network unexploitability.
* **Certificate-dependent source identity:** `CHK(me, them, D)` checks whether `me` defects against `them`. If `them`'s source code includes its carried certificates, then as soon as predator $P$ acquires *any* new certificate (e.g., under the uniform grudge rule or S-nonself production), its source changes to $P'$, invalidating the detector's grudge against $P$.
  * *Fix:* State explicitly in §1 Static that `CHK` and grudge certificates key on the *bare program AST* (skeleton/root), stripping the carried certificate bundle, consistent with how carriers work in Milestone 4/5.
* **Cause-label non-exclusivity and order dependence:** In Cell B2/C, an island with detectors and unconditional cooperators (ALLC) has $P(C,C) = 1.0$. If PrudentBot invades by feeding on ALLC (prudence premium) while defecting against detectors, does that trigger *predation* or *prudence premium*? Also, *predation* requires the exploiter to reach $\ge 0.5$ before changing hands, which misses multi-predator invasions or 3-way splits.
  * *Fix:* Freeze a strict precedence order for cause labels (e.g., *Inefficiency* $\to$ *Predation* [strictly exploits the *modal* resident, threshold $\ge 0.3$ of island] $\to$ *Prudence premium* $\to$ *Abundance*).

### 2. Predictions I think are wrong

* **Prediction 1 (Establishment falls to $\le 0.05$ in Cell A):** Likely **wrong** at $N=800$ if grudges are only vertically inherited without horizontal copying. A predator gets $O(N)$ free meals before its lineage regularly encounters the descendants of the few detectors it has already struck. With selection $w=0.3$, a predator starting at $1/800$ that gets free meals on $>95\%$ of encounters will establish well above $0.05$ (my prediction: $\ge 0.15$ at $N=800$ under vertical-only inheritance; $\le 0.05$ only if horizontal gene-copying is active).
* **Prediction 4 (With tail and grudge, back to near a coin flip in B):** Likely **wrong**. The annealed tail (rain) injects unconditional cooperators (shadows) alongside predators. Detectors do not exploit ALLC; PrudentBot does. Even if grudges neutralize predators, the tail continuously feeds PrudentBot a *prudence premium* on the shadow drift. My prediction: PrudentBot wins $\ge 0.75$ of tail+grudge runs, with removals shifting from *predation* to *prudence premium*.

### 3. Missing controls or cheap additions

* **Grudge list cap (LRU interaction):** Under the annealed tail, thousands of distinct mutant spellings arrive. If every defection appends a certificate per partner spelling, certificate bundles will bloat and hit the LRU cap (Item 41) or step budget, causing amnesia against older active predators. Log `max_grudges_held` and `grudge_evictions`.
* **Horizontal sharing toggle in Cell A:** Run Cell A both with and without horizontal certificate copying among detector siblings to isolate individual immunization from network immunization.

### 4. Alternative explanations the brief does not rule out

* **Step-cost asymmetry:** If checking `or(CHK(them,them,D), CHK(me,them,D))` against a growing list of grudges costs more fuel or hits the verification cap under `realizable_scaling`, detectors may fail to verify and default to $C$ (or time out) in late generations, losing by *verification exhaustion* rather than ecological dynamics.

### 5. Ideas that matter for the research program beyond this experiment

* **Behavioral vs. syntactic provenance:** The RS's statement notes detectors need to "evolve certificates that predators detect" (or vice versa). A grudge rule is an *episodic memory* of past play masquerading as a static proof certificate. If Turing-complete open-source cooperation requires shared episodic state (reputation/grudge ledgers) to protect gentle networks (`ALLC`-tolerant), the program is moving from pure static source-reading (one-shot program equilibrium) to repeated-game reputation over lineages. That distinction should be made explicit in `THEORY.md`.
