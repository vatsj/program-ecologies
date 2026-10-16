# Review of `specs/2026-10-15-removing-rivals.md` by gemini-4-argon

**1. Design flaws or confounds**

* **Empty-certificate rain vs. S-nonself production timing (Part B):** Rain injects fresh founders with *empty* certificate lists. If a predator requires its own certificates to trigger the rival's cooperation (or to survive long enough to invade), it must produce them via S-nonself *after* arrival, against the resident rival. If the static predator definition in Part 0 assumes full/cached certificate tables rather than empty-list arrival + S-nonself production against the rival, the static classifier will overestimate exploitable rivals. **Fix:** In Part 0, classify predators using their post-S-nonself-against-rival phenotype (which for pure constants/defectors is unchanged, but for conditional predators may differ), and verify whether the 2,222 predators of the anti-punisher include unconditional `D` or non-certificate-needing programs.
* **Donor confounding in Part A:** The "sponsored PrudentBot donor" bundles two changes relative to S-nonself: (i) guaranteed presence of a PrudentBot code copy on every island, and (ii) pre-populated full certificate lists at founding (bypassing endogenous production). C-donor has full lists for C-seeded FairBot; S-nonself has neither. If Part A succeeds, you cannot tell whether prevention comes from PrudentBot's *code* (prudence during the scramble) or its *pre-filled certificates* (early legibility). **Fix:** Add a cheap control in at least one cell, e.g. `(200, 64)`: one PrudentBot founder per island with an *empty* certificate list under S-nonself production.

**2. Predictions that are wrong**

* **Prediction 2 (Rain at $\varepsilon N = 0.1$ cures $\ge 0.8$ of exploitable rivals by 10,000 gen):** Likely too optimistic for two reasons. First, if the predator self-defects ($P(C,C)=0$ with copies), then once it invades the rival island, the island's mean payoff drops to near the defector baseline, drastically reducing its emigration weight if migration is payoff-weighted, or making it a sink; worse, while the predator is invading, constant migration $mN \approx (N/100)^{0.7} \approx 1.62$ from the majority target network introduces target holders *into the rival+predator mixture*. Target holders defect against both rival and predator, cooperators with each other, and may be killed by the rival before the predator finishes sweeping. Second, let Part 0 compute the exact arrival + fixation hazard: if predator prior mass is $\mu_{\text{pred}}$, arrival rate per island is $\varepsilon N \cdot \mu_{\text{pred}}$ per generation. Unless $\mu_{\text{pred}} \gtrsim 10^{-2}$ (e.g., if `DefectBot` itself is a predator of the anti-punisher), waiting time at $\varepsilon N = 0.01$ or $0.1$ will exceed $10^4$ generations. **My prediction:** True only if simple high-prior programs (like `D`) are among the 2,222 predators; otherwise cure rate at $\varepsilon N = 0.1$ will be $< 0.4$.

**3. Missing controls or cheap additions**

* **Explicitly report whether `DefectBot` (`D`) is a predator in Part 0:** Looking at `if(or(CHK(me,^C,C),CHK(them,^D,D)),D,C)`, if `me` (the rival) has no `^C,C` certificate and `them` (`D`) has no `^D,D` certificate, this rival cooperates with `D`! If unconditional `D` is one of the 2,222 predators, it has huge prior mass ($\sim 0.1$) and needs no certificates—making the predator mechanism simply "defector invasion of an unguarded cooperator, followed by target colonization of defectors." State the top 3 predators by prior mass in Part 0.
* **Track *how* the predator island converts to the target in B1:** Does the predator fix first (turning the island all-`D`) and then get colonized by target migrants, or do target migrants sweep *during* the predator's rise? Log the intermediate holder at the rival island.

**4. Alternative explanations not ruled out**

* **Direct migrant swamping aided by rain drift:** At $\varepsilon N = 1$, 1 birth per generation is a random founder (mostly defectors/junk). This acts as a deleterious mutation load on the resident rival, lowering its effective population size and increasing the fixation probability of a migrating target-network propagule/cluster *without* any predator fixation step. B1's path-tracking ("predator step, direct invasion, other") addresses this, provided "predator step" requires a certified predator lineage to reach a threshold share (say $\ge 0.5$) before target takeover. Define that threshold explicitly in the spec.

**5. Ideas for the research program**

* Nothing material.
