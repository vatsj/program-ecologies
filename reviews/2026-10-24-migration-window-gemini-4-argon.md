# Review of `specs/2026-10-24-migration-window.md` by gemini-4-argon

**1. Design flaws or confounds**

* **Target definition admits dominated outcomes (Critical):** The brief defines "efficient islands" as including *unequal pairs* and the *grand coalition* (both of which are outside $V^*$ and dominated by fair pairs in `dollar3`). It then defines "target met" as "every island efficient and all three members present." By this rule, an archipelago with 61 islands on unequal pairs and 3 islands on the three fair pairs meets the target! Yet the RS's normative target ("all island outcomes are efficient and all stable sets show up") and Prediction 3 ("unequal pairs take over... narrowing the window") clearly treat unequal pairs as a failure mode.
  * *Fix:* Separate **Pareto-efficient** (no waste/disagreement) from **$V^*$-supported** (modal outcome is one of the three fair pairs). Define two distinct statistics: `target_pareto` (all islands Pareto-efficient + 3 members present) and `target_Vstar` (all islands on $V^*$ + 3 members present). State explicitly which one is scored in Predictions 1, 3, 4, and 5 (Prediction 3 requires `target_Vstar` to make sense).
* **Coarse snapshot grid vs. first-passage times (FPT):** Measuring FPTs and their log-log slopes (Prediction 2) only at snapshots $\{1\text{k}, 2\text{k}, 5\text{k}, 10\text{k}, 20\text{k}\}$ will introduce massive quantization error, especially at $mN \in \{0.1, 0.3, 1\}$ where waste clears well before 1,000 generations. Furthermore, at $mN = 0.01$, coverage loss via neutral voter-model coalescence over $I=64$ islands takes $O(I / mN) \approx 6,400+$ generations, and at $mN = 0.003$ it will right-censor past 20,000 in most runs, biasing median FPTs.
  * *Fix:* Log island modal outcomes every 50 or 100 generations (cheap in memory/disk: just 64 integers per interval) to get exact FPTs, while keeping full population snapshots at the 5 listed horizons. Handle right-censoring explicitly by reporting Kaplan–Meier medians or restricting the Prediction 2 regression to uncensored $mN \in \{0.03, 0.1, 0.3\}$.

**2. Predictions I think are wrong**

* **Prediction 4 (`U-gKR(0.99)` beats baseline at every $mN$):** In "Farsighted refusal", any refusing guard spreads under migration and settles one member everywhere. Because `U-gKR(0.99)` actively locks in its member upon colonizing, it may accelerate consensus (coverage loss) relative to the unguarded baseline at intermediate-to-high $mN$ ($0.1, 0.3$), *reducing* the share of runs meeting the target at a fixed generation like 10,000.
  * *My prediction:* `U-gKR(0.99)` beats baseline at low $mN$ (where it clears waste internally without needing migration) and has a longer *lifetime*, but loses to or ties baseline at $mN \in \{0.1, 0.3\}$ at $t = 10,000$ due to faster consensus.
* **Prediction 2 (Coverage-lost slope in $[-1.3, -0.7]$):** If unequal pairs invade fair pairs under migration (the mechanism cited in Prediction 3), coverage loss is driven by *selection/invasion* by unequal pairs rather than neutral drift among the three fair pairs, compressing the separation factor below 5.

**3. Missing controls or cheap additions**

* **Outcome breakdown:** Alongside "efficient islands", log the exact share of islands on (a) fair pairs ($V^*$), (b) unequal pairs, (c) grand coalition, and (d) wasteful/disagreement. This costs nothing and directly tests the mechanism of Prediction 3.
* **Non-monotonicity in time:** A single island can clear waste, then revert to disagreement during a later immigrant invasion. Log both *first-passage* to 0 waste and *last-passage* (permanent clearance), or score the window as total generations spent in the target state.

**4. Alternative explanations not ruled out**

* **Founder-diversity failure vs. migration consensus:** With 28% of islands starting on $V^*$ at $mN=0$ ($\approx 18$ islands across 3 members, $\sim 6$ per member), coverage loss at low $mN$ could occur because one fair pair is rapidly eaten by *unequal* pairs before it can colonizewasteful islands, not by neutral coalescence among fair pairs. Tracking transitions between island modal states ($A \to B$ upon colonization) rules this out.

**5. Ideas for the research program**

* Nothing material.
