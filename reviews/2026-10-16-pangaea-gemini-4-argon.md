# Review of `specs/2026-10-16-pangaea.md` by gemini-4-argon

**1. Design flaws or confounds**

* **The production-rate cap ($r$) confounds $N$ with per-generation certificate discovery.** In the baseline kernel ($r = N/2$), each individual participates in $N/2$ production encounters per Moran event, meaning $N^2/2$ encounters per generation on an island of size $N$. If you cap $r = 50$ on the Pangaea ($N = 12,800$), each individual participates in only $2r = 100$ encounters per generation—a $64\times$ reduction in the per-capita rate at which carriers meet and mint certificates during the scramble, and $4\times$ below even the $(200, 64)$ cell. Validating $r = 50$ on $(800, 16)$ and $(3,200, 4)$ does not prove it is harmless at $N = 12,800$, where any pair of compatible types is $4\times$ to $16\times$ more diluted per draw.
  * *Fix:* Do not cap $r$ per Moran step; instead, decouple production from Moran steps so that **per-capita encounters per generation** are held constant across the continuum (matching the $N = 200$ baseline, i.e., $r = 1$ production encounter per Moran step, or $N$ per generation). Run the $(200, 64)$ cell under both schedules to verify equivalence.

* **The `universal-open` threshold ($\ge 0.95$ on Pangaea) is vulnerable to neutral shadow/carrier polymorphism.** At $\varepsilon = 0$, unconditional cooperators (`ALLC`) and uncertified carriers surviving the scramble become neutral once defectors and rival exploiters are extinct. On a single population of $12,800$, neutral drift takes $\sim N = 12,800$ generations to resolve, so a leftover $>5\%$ neutral shadow at $t = 2,000$ or $10,000$ will register as a universality failure even when all rival networks and cliques are $0$.
  * *Fix:* Define Pangaea universality as: (a) totalcooperative share $P(C,C) \ge 0.95$, and (b) the dominant compatible network holds $\ge 0.99$ of all *certified carriers* (excluding neutral `ALLC`/shadow remnants), alongside the raw $\ge 0.95$ population share.

**2. Predictions I think are wrong**

* **Prediction 5 (PrudentBot network $\ge 0.9$ of the Pangaea in $\ge 0.8$ of runs, counting FairBot-family in).** Even counting compatible FairBot-family carriers in, the threshold is $\ge 0.90$ of the *entire population*. Because ` FairBot` does not punish `ALLC` (only `PrudentBot` does), as soon as `FairBot` and `PrudentBot` sweep defectors, selection against `ALLC` is proportional only to the `PrudentBot` share multiplied by the remaining uncertified/defector interaction rate. Once compatible carriers dominate, `ALLC` drifts neutrally with `FairBot`. Furthermore, under `S-nonself`, any non-target bridge-less rival with prior mass comparable to `PrudentBot` starts at its exact prior expectation on a Pangaea; while majority wins, the sum of neutral hitchhikers (`ALLC` + uncertified) at $t = 2,000$ on $N = 12,800$ will frequently exceed $0.10$.
  * *My prediction:* Universality among certified carriers will be $\ge 0.95$, but raw population share of the target network at $t = 2,000$ will sit between $0.75$ and $0.90$ in at least a quarter of runs due to slow-drifting neutral cooperators.

**3. Missing controls or cheap additions**

* **Exact initial-founder coupling across $(N, I)$:** Draw one master list of $12,800$ founders per seed ($20$ seeds) and partition that *exact* multiset into $I \in \{128, 64, 16, 4, 1\}$ islands. This removes sampling variance in `TwinD` and rival copy counts across the continuum, making the transition in $I$ a pure function of subdivision.
* **Free-certificate (ideal table) Pangaea control:** Run 20 seeds at $(12,800, 1)$ with pre-populated ideal certificates. This separates the pure frequency-dependent selection argument ($\mu_Q$ vs open mass) from any endogenous production lag on a large island.

**4. Alternative explanations the brief does not rule out**

* If cliques or rivals fail on the Pangaea under `S-nonself`, it could be driven by **production starvation of rare types** (a clique of $\sim 9$ copies in $12,800$ waits $\sim 1,400$ random encounters just to meet a twin, and under `S-nonself` cannot even produce against that twin) rather than payoff inferiority after certification. The free-certificate Pangaea control above rules this out.

**5. Ideas that matter for the research program**

* **Fission-fusion (temporary demes, periodic Pangaea mixing):** If small islands ($N = 100$) are optimal for rapid local certificate production and demographic purging of shadows, while a Pangaea ($I = 1$) deterministically purges cliques and resolves bridge-less rivals by majority, then a single round of global mixing after local establishment (or high migration after a burn-in) should achieve $1.0$ universality at any total population without needing donors.
