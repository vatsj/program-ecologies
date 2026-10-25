# Review of `specs/2026-10-25-churn-primary.md` by gemini-4-argon

**1. Design flaws or confounds**

* **Missing excluded-slot behavior in the Mechanism Probe:** A churn-capable reader in a member slot $i$ can only switch to the excluded slot $k$ if $k$'s resident population is *actually making* a fair offer to $i$ (or conditionally willing to). In the contract layer, the excluded slot proposes a deviation by construction; in the primary object, an excluded slot that gets 0 has been drifting or sitting on a founder that might be demanding $2/3$, naming $j$, or playing a constant. If you run the probe without controlling $k$'s resident program, a $<5\%$ switch rate is confounded: you won't know if the encounter-level mechanism failed (your Prediction 3) or if $k$ simply wasn't offering $(i, 1/2)$. 
  * *Fix:* Stratify the mechanism probe by the resident composition of the excluded slot $k$: (a) $k$ forced to a fair-offering reader/constant toward $i$, vs. (b) $k$ drawn from the natural $mN > 0$ steady state.
* **Prior dilution in Arm E at $n=10$:** Enlarging the `dollar3` grammar from $n=6$ to $n=10$ under the length prior exponentially dilutes the founding mass of the basic establishers that put islands on fair pairs in the first place. If Arm E at $n=10$ fails to reach high V* share even at $mN=0$, comparing its flip counts and coverage to the $n=6$ baseline or contract layer is uninterpretable.
  * *Fix:* Report the static prior mass of churn-capable readers and basic fair-pair establishers at $n=10$ in `notes/` before running. Add an Arm E control where the $n \le 6$ grammar is augmented *only* with the minimal churn-capable reader templates (matching Arm T's template approach).
* **Under-specified Arm T template grammar:** In `RESULTS "The social organization game over the realizable language"`, a template/library prior gave $40/40$ fair runs while expanded syntax gave $0/40$. If the new Arm T template grammar assigns $\sim O(1)$ prior weight to symmetric two-partner FairBot readers ("if $j$ names me at $1/2$ name $j$, else if $k$ does name $k$"), then at $mN=0$ the islands may naturally seed with flexible readers rather than rigid single-partner commitments, manufacturing churn by prior construction.
  * *Fix:* Explicitly specify the exact template list and prior weights for Arm T in the spec before launch, and bound the prior weight of multi-partner conditional readers relative to constants and single-partner readers.

**2. Predictions I think are wrong**

* **Prediction 2 (if Arm T's template prior is compact):** If the Arm T template grammar gives substantial prior mass ($\ge 0.05$) to symmetric conditional readers (which cooperate with *whichever* slot offers $1/2$, breaking ties by coin/order), islands will establish *with* these readers already resident in the member slots. When an immigrant enters partner slot $j$, the resident reader in $i$ immediately redirects to $k$ in that specific encounter (unlike Prediction 3's premise where only a *single* reader is injected). If $k$ is also a conditional reader, the $(i,k)$ pair immediately forms and outcompetes $j$. Thus, if the prior is compact, Arm T *will* churn and falsify Prediction 2.

**3. Missing controls or cheap additions**

* **Homogeneous resident-reader control in the probe:** In the mechanism probe, add a cell where the resident fair pair $(i,j)$ is composed *entirely* of the churn-capable reader (with $k$ also holding a fair reader), and then inject a 1–5% immigrant fraction into $j$. This cleanly separates: (i) "churn-capable readers are too rare in the length prior to win the founding scramble" from (ii) "even when resident at 100%, encounter-level switching does not destabilize the pair under single-immigrant perturbations."

**4. Alternative explanations the brief does not rule out**

* **Dominated-outcome absorption:** In `RESULTS "Stable sets on islands"`, $0.72$ of islands sat on dominated outcomes at $mN=0$ without contracts. Low coverage and low member-to-member flips in Arms E and T might simply reflect islands failing to sit on V* at all (or collapsing into the grand coalition / unequal splits under $n=10$), rather than one fair pair monopolizing the metapopulation. Prediction 1's falsifier and baseline comparison must condition on the fraction of islands actually in V*.

**5. Ideas that matter beyond this experiment**

* Nothing material.
