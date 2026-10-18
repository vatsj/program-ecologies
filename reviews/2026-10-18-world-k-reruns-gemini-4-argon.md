# Review of `specs/2026-10-18-world-k-reruns.md` by gemini-4-argon

### 1. Design flaws or confounds

* **Production encounter starvation at large $N$ ($r=100$ fixed):** Fixing $r=100$ encounters per Moran event across all $N$ (to avoid an RNG overlap bug) confounds the scaling path and Pangaea continuum. Under world K, a D-certificate is keyed to the specific partner source it was produced against; unlike in L, a single production encounter does not generalize to the whole population. At $N=400$, $800$, $3,200$, and $12,800$, $r=100$ means a newly arrived or establishing lineage meets only a tiny fraction of the resident quotes per Moran event. If gentle detectors or other K-specific programs fail to establish or fail to recognize defectors at large $N$, you will not know whether it is due to population size or severe certificate-keying undersampling.
  * *Fix:* Fix the RNG stride/seed Partitioning in the code so $r$ can scale with $N$ (or test an $r=N$ control at $(800, 16)$ and $(3,200, 1)$) rather than capping $r=100$ everywhere for an implementation reason.

* **Provenance test (S-self vs. S-nonself) confounded by $r$-budget waste:** Under S-self, some of the $r=100$ production encounters occur against one's own clones. In world K, a self-play D-certificate is keyed only to one's own quote, making it useless against distinct opponents, while wasting part of the finite $r=100$ production budget as a lineage grows.
  * *Fix:* Ensure S-self vs. S-nonself compares *non-self* production capacity equally, or log the fraction of $r=100$ spent on self-encounters to separate "minted clique" effects from "wasted production budget" effects.

### 2. Predictions I think are wrong

* **Prediction 4 (Provenance rule stops mattering; S-self and S-nonself within 0.1):** Likely wrong at $(100, 64)$, or right for the wrong reason. In world K, a program that defects under self-hypothesis produces a D-certificate keyed to *its own quote* during self-play. That turns an own-D reader into a *self-defector* (destroying its own lineage's cooperation) rather than an identity clique (which cooperates with itself and defects against others, as in L). Conversely, if a program's syntax branches on whether it holds a D-cert for the partner *without* triggering on itself, S-self still alters the certificate state on the self-diagonal.
  * *My prediction:* In §1 (static analysis), you will find that S-self under K converts the former TwinD templates from *identity cliques* into *self-spoilers* (self-defectors), which could actually *help* universality by killing them off, or hurt establishment if any establisher mis-keys on itself. They will not be mechanistically equivalent, even if universality is near ceiling.

* **Prediction 5 (Pangaea establishment law strengthens; all-D at 6,400 $\le 2/20$ vs $5/20$):** Over-optimistic. In RESULTS "Cliques on a Pangaea", Pangaea failure is driven by the demographic scramble ($\approx e^{-N/4,500}$), which depends on the ratio of establishers to unconditional cooperators/spoilers in the seed. Moving TwinD (a small prior mass, $\sim 4.6$ copies across $6,400$ founders) into the gentle-reader network raises $\mu_{\text{net}}$ only marginally, and at $r=100$ on $N=6,400$, gentle detectors cannot key D-certificates against the ratusan of distinct defector quotes fast enough during the scramble to get the prudence premium.
  * *My prediction:* K and L all-D failure rates at $N=6,400$ and $12,800$ will be statistically indistinguishable (within 1–2 runs of each other).

### 3. Missing controls or cheap additions

* **Pairwise K vs. L transition matrix on founders:** Since runs use paired founders, report the $2\times 2$ contingency table of island outcomes (Open, Identity, Non-identity Rival, All-D) between L and K at the end of the scramble ($t=200$) as well as at $t=2,000/10,000$. This shows directly whether K converts L's identity islands into Open islands during establishment or during migration.
* **Include the `Removing rivals` rain/predator check (Part 1/2), not just Part 0 static classification:** In L, mutation ("rain") cured exploitable rivals but fed identity cliques via target shadows. A single cheap cell with rain under K at $(200, 64)$ would test whether rain now cleanly achieves 100% universality without feeding a clique sink.

### 4. Alternative explanations the brief does not rule out

* **Unkeyed fallback behavior acting as a shadow:** Under K, when a gentle detector meets a *new* defector quote it has not yet produced a keyed D-certificate against, its default action (likely C) makes it an unconditional cooperator on first encounter. In large populations ($N \ge 800$) with $r=100$, gentle detectors may survive or die as *ALLC shadows* rather than as prudent establishers. Logging the fraction of encounters where a gentle detector acts *with* vs. *without* a matching keyed certificate rules this out.

### 5. Ideas that matter for the research program beyond this experiment

* **Keyed certificates reintroduce the mutual-verification / coverage scaling bottleneck:** World K fixes the TwinD clique accident by keying D-certificates to partner bare sources, but this trades a *semantic* flaw (false generalization of self-defection) for a *combinatorial* one ($O(\text{distinct quotes})$ certificate table size). Under rare mutation or rich priors where neutral syntax drift creates many distinct quotes of defectors, a source-keyed certificate table with a finite LRU cap (from Queue 41) can be thrashed by quote-diverse defectors. The principled long-term fix is keying hypothesis-closed certificates to the *canonicalized sub-tree used in the proof* (structural/behavioral keying) rather than the partner's bare quote.
