# Review of `specs/2026-11-03-pair-worth-n.md` by gemini-4-argon

**1. Design flaws or confounds**

* **Level-0 exclusion fallback in F (repeats the queue-72 bug).** F's `elif` branches check `□(j = (i, π_j(σ_i; i, j)))`—that $j$ *unconditionally* plays the pair action. As proved in queue 72, two conditional bidders will never trigger a level-0 pair handshake when the third player defects or mismatches; they fall through to `c`. Worse, because $\pi$ is parameterized only by $\sigma_i$, $i$ expects $j$ to demand $\frac{1}{2}(1-\sigma_i)$ while $j$ (with $\sigma_j \neq \sigma_i$) expects $i$ to demand $\frac{1}{2}(1-\sigma_j)$. Even a level-1 handshake fails when $\sigma_i \neq \sigma_j$. **Fix:** Use the queue-72 level-1 repaired handshake for the `elif` branches, and make the exclusion fallback flexible too (accepting any pair offer $(i, a)$ from $j$ where $a \le \frac{1}{3} - \pi_i(\sigma_i)$, or using a canonical split of the $\frac{1}{3}$ pair worth such as $(1/6, 1/6)$ independent of $\sigma_i$).
* **Prior skew across shares in C+F.** The brief says F is indexed by $\sigma_i \in \{0..6\}/6$ and seeded "uniform over its $(\sigma_i, c)$ pairs." In C+G and C+B\*, uniform seeding over the 28 splits gives $\sigma_i = 0$ prior weight $7/28$, while $\sigma_i = 1$ gets $1/28$, heavily favoring compatible low demands. Uniform seeding over the 7 values of $\sigma_i$ gives $\sigma_i = 1$ weight $1/7$, making random F triples mostly infeasible ($\mathbb{E}[\sum \sigma_i] = 1.5 > 1$) and skewing F toward non-core demands ($\sigma_i > 2/3$). **Fix:** Weight F's seed distribution over $\sigma_i$ by the marginal distribution of the 28 simplex splits, $(7 - 6\sigma_i)/28$, to match C+G and C+B\*.
* **Paired-founder index mismatch at $N=100$.** Stored C+G has runs 0–19; Section 3C adds runs 20–39 (total 0–39). For C+F at $N=100$, Section 3C specifies "runs 20–59". Then C+F and C+G only overlap on runs 20–39, halving the paired sample for Prediction 4. **Fix:** Run C+F on 0–39 (or 0–59) so all C+G runs are paired.

**2. Predictions I think are wrong**

* **RE 1 ($N=400, \delta=0.0125$ within $0.15$ of C).** At $I=64$ islands, $T \approx 0.16$ per island means $\sim 10$ islands across the metapopulation get a compatible bid triple at founding. At $N=400$, once a single island locks into a grand bid ($s=1/6$, $N\cdot s \approx 20$), it is nearly immune to drift and spreads across all 64 islands via migration ($mN=1$). Metapopulation supply $I \cdot T$, not single-island $T$, governs $mN=1$ at large $N$. **My prediction:** C+B\* at $N=400, \delta=0.0125$ reaches core $\ge 0.50$, exceeding C by $> 0.15$.
* **RE 4 ($|(\text{C+F}) - (\text{C+G})| \le 0.15$).** If F's prior is not marginal-matched (Flaw 1), C+F will fail badly due to infeasible demands. Even if matched, F accepts feasible splits with $\sigma_i \le 1$ when partners demand $0$, stabilizing the 9 non-core efficient splits ($\sigma_i > 2/3$) wherever F's fallback deters pair deviations. **My prediction:** Uncorrected C+F is $> 0.20$ below C+G; corrected C+F has $> 0.15$ efficient-dominated share.

**3. Missing controls or cheap additions**

* **Core-only grand constants (C+G\_core, 19 splits) or core-bounded F ($\sigma_i \le 4/6$).** C+B tests the 19-split menu for bids; C+G and C+F include the 9 dominated grand splits ($\sigma_i > 4/6$). Adding C+F restricted to $\sigma_i \le 4/6$ at $N=200$ cheaply isolates whether failures of the RS's conjecture come from non-core grand splits vs. pair traps.

**4. Alternative explanations not ruled out**

* **Metapopulation rescue ($I \cdot T$ vs. $T$).** Prediction 1 attributes the $N=400$ gain at $mN=1$ to per-island $T$. Because one established core island can colonize the rest when $N\cdot s$ is large, the scaling lever at $mN=1$ can be fixation probability of a single island's triple times migration, even when $T \ll 1$. Comparing $\delta=0.0125$ at $mN=0$ vs. $mN=1$ separates local $T$ from metapopulation rescue.

**5. Ideas for the research program**

* Nothing material.
