# Review of `specs/2026-10-16-annealed-mutation.md` by gemini-4-argon

**1. Design flaws or confounds**

* **Fixed $t_0 = 50$ confounds the scaling limit with the establishment scramble:** At $t_0 = 50$, 50% of all annealed arrivals occur by $t = 50$ and 80% by $t = 200$. However, the neutral fixation / shadow-drift time on an island scales as $O(N)$ (meaning $T_{\text{fix}} \approx 800$ at $N = 800$). Thus, at $N = 800$, almost the entire mutation budget $\Lambda_N$ is dumped into the initial establishment scramble *before* islands have settled or drifted to shadows, rather than testing late-stage maintenance vs. drift. 
  * *Fix:* Either scale $t_0 \propto N$ (e.g., $t_0 = N/4$), or delay the onset of the post-seed schedule until after initial island establishment ($t_{\text{start}} \approx 100$), or explicitly decompose statistics into "scramble-phase" ($t < 200$) vs. "post-settlement" ($t \ge 200$) colonizations.
* **Initial-rate regime violation at $N = 800$:** Because $\int_0^\infty \varepsilon N(t)\,dt \approx a t_0 = N \Lambda_N \propto N^{1/2}$, keeping $t_0 = 50$ fixed forces the initial arrival rate $a = N \Lambda_N / t_0$ to grow as $N^{1/2}$. At $N = 800, \Lambda_0 = 0.03$, $a \approx 0.24$ per island-generation (nearly 1 mutant every 4 generations per island), violating the rare-mutation regime where the $1/N$ fixation approximation holds.
  * *Fix:* Scaling $t_0 \propto N^{1/2}$ or $N$ keeps $a \le O(1)$ and prevents early clonal interference.
* **Scale guard drops arm (iv) before testing Prediction 5:** Dropping arm (iv) (constant rain) at $N=800$ makes Prediction 5 ("Only $\Lambda$ matters, not the shape") untestable in the asymptotic regime where time-scale separation actually matters.
  * *Fix:* Keep arm (iv) at $\Lambda_0 = 0.01$ across all $N$, and drop $\Lambda_0 = 0.03$ across all arms at $N = 800$ first if compute binds.

**2. Predictions that are wrong**

* **Prediction 5 (that arm (iv) matches arm (i) within uncertainty) is likely wrong on shadow-fed identity takeovers and target cures:** While pure neutral drift depends only on integrated $\Lambda_N$, *predator cures of target shadows* require a two-step sequential process: (1) the target island drifts to an unconditional shadow (taking $O(N)$ generations), and (2) a predator/identity mutant arrives *after* the shadow has fixed. Under annealing with $t_0 = 50$, >90% of arrivals occur before $t = 450$, before $N \in \{400, 800\}$ islands have drifted to shadows. Constant rain (iv) spreads arrivals uniformly to $T = 10,000$, hitting late-drifting shadows.
  * *My prediction:* Constant rain (iv) will produce significantly *more* secondary takeovers of target shadows (and thus more late identity takeovers) than annealed rain (i) at $N \ge 400$.
* **Prediction 2 ($\ge 0.8$ cure rate at $N = 800, \Lambda_0 = 0.03$) is likely too high:** Using the brief's formula $1 - \exp(-\rho \mu_{\text{pred}} N \Lambda_N)$ with $\rho = 0.26$ and $N \Lambda_N = 12$ at $(800, 0.03)$ requires $\mu_{\text{pred}} \ge 0.52$ to reach $0.8$. Against non-constant exploitable rivals, $\mu_{\text{pred}}$ under the length prior is much smaller than $0.5$.
  * *My prediction:* Cure rate of non-shadow exploitable rivals will be $< 0.5$ unless $\Lambda_0$ is raised or "exploitable rival" is almost exclusively ALLC.

**3. Missing controls or cheap additions**

* **Time-of-colonization histogram:** Log the generation $t$ at which each drift and selected colonization occurs (zero extra compute). This immediately separates scramble-phase arrivals from true post-establishment drift/cures and tests the sequential shadow-feeding mechanism.
* **Analytical $\mu_{\text{pred}}$ plug-in:** In `notes/annealed.md` §1, explicitly compute $\mu_{\text{pred}}$ for each rival class before committing the numerical threshold in Prediction 2.

**4. Alternative explanations not ruled out**

* If annealing (i) shows fewer identity takeovers or fewer cures than constant rain (iv), the brief cannot distinguish whether this is due to the *light tail* preventing drift (the RS's mechanism) or simply *front-loading* arrivals before target islands have had time to drift into exploitable shadows (a $t_0 \ll N$ timing artifact). The time-of-colonization log (item 3) rules this out.

**5. Ideas for the research program**

* Nothing material.
