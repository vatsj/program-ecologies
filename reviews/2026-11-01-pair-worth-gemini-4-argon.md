### 1. Design flaws or confounds

**The exclusion-bid fallback fails on the grid in $G\frac{1}{3}$ (and asymmetric $\sigma$), breaking the selection mechanism.**
The spec defines $B(\sigma; c)$'s pair fallback as "dividing the pair's worth in proportion to the two players' shares in $\sigma$, rounded down to the grid." In $G\frac{1}{3}$ on sixths, a pair is worth $a = 2/6$. At the equal split $\sigma = (2/6, 2/6, 2/6)$, proportional shares are $(1/6, 1/6)$. However, for 12 of the 19 core splits (e.g., $\sigma = (4/6, 1/6, 1/6)$), a pair between the $4/6$ and $1/6$ players gives shares $\frac{4}{5}(2/6) = 8/30$ and $\frac{1}{5}(2/6) = 2/30$. Rounded down to sixths, these are $(1/6, 0)$, wasting $1/6$ of the pair's value and giving one bidder **zero** payoff. A bidder getting 0 has no selective advantage over an excluded player, breaking the "exclusion fallback makes bidding selected" mechanism and biasing core coverage away from boundary core points.
*Fix:* Replace proportional rounding with a deterministic grid-efficient division rule (e.g., split $a$ as equally as the grid allows, giving the odd tick in $G\frac{2}{3}$ or $G\frac{1}{3}$ to the player with the larger $\sigma$ share, or by slot index on ties), or move $G\frac{1}{3}$ to twelfths so $a/2 = 2/12$ is always available via equal pair splits.

**Blocker handshake symmetry vs. asymmetric $\sigma$ bids.**
In $G\frac{5}{6}$, $K(\sigma; c)$ always blocks at $(5/12, 5/12)$, while the bid set includes $(5, 4, 3)/12$ permutations. For a player getting $5/12$ in the grand split $\sigma$, switching to $K(\sigma; c)$ yields $5/12 - 5/12 = 0$ gain—blocking is neutral, not selected! Only the players getting $4/12$ and $3/12$ strictly gain from blocking. 
*Fix:* State explicitly in the spec and predictions that on $(5,4,3)/12$ islands, $K$ is only positively selected in the $4/12$ and $3/12$ slots, or restrict $G\frac{5}{6}$ bids to the equal split $(4,4,4)/12$ so the $+1/12$ blocker gain applies uniformly across slots.

**Transfer cell bid sets test the wrong hypothesis.**
In $G\frac{2}{3}'$ and $G\text{gl}'$ (on 24ths), the spec keeps "the same splits as their sixths cells." On 24ths, the one-step strict ring is at $1/24$ outside the core, whereas the old sixths splits sit $4/24$ away. If you only seed bids on sixths splits, you are not testing whether a finer grid shrinks the ring under $C+B$; you are just leaving the $1/24$-ring unseeded.
*Fix:* For $C$, the transfer cells work as written. For $C+B$, either include the 24ths core boundary/ring splits or restrict the transfer-cell ring prediction (Prediction 4) to arm $C$.

---

### 2. Predictions that are wrong

**RS Conjecture & RE Prediction 2 (All 19 core points observed in $G\frac{1}{3}$ at $mN = 1$).**
*Reason:* At $mN = 1$ with $I = 64$, migration links the islands strongly enough to cause consensus or strong concentration on a few splits within each run (as seen in Queue 60 and 64, where $mN = 1$ collapsed diversity across the 3 fair pairs). Across 20 runs, risk-dominant/central core splits like $(2,2,2)/6$ will win the founding scramble far more often than extreme splits like $(4,2,0)/6$ (where one player gets 0 and has no strict incentive to join the grand coalition!). Some extreme core points with a 0 share will go unobserved across 20 runs at $mN=1$.
*My prediction:* Core proper share will be $\ge 0.90$ in $C+B$, but pooled core coverage at $mN = 1$ will be $\le 15/19$ (leaving the 0-share boundary points empty), whereas $mN = 0$ will observe all 19.

---

### 3. Missing controls or cheap additions

- **Report core coverage separately for $mN = 0$ vs $mN = 1$.** Since $mN = 0$ is already in the secondary cells, explicitly scoring the RS's coverage conjecture at $mN = 0$ vs $mN = 1$ cleanly separates founding-scramble coverage from migration-induced homogenization.
- **Track 0-share core splits separately in $G\frac{1}{3}$.** Splits like $(4,2,0)/6$ are in the core proper ($4/6 \le 1 - 1/3$), but the third player gets 0—identical to being excluded. A bidder for $(4,2,0)/6$ in the 0-share slot has **zero** selection pressure (+0 against 0) to complete the three-way bid! Stratifying core coverage by minimum share ($\min_i \sigma_i > 0$ vs $= 0$) will immediately explain any coverage failure.

---

### 4. Alternative explanations not ruled out

- **Dose saturation vs. neutral path (Predictions 2 & 7).** At $\delta = 0.05$, $C+B+K$ has 10% of the seed law in named families, and each specific $\sigma$ in $G\frac{1}{3}$ gets only $\delta / 19 \approx 0.0026$ per slot (so three-slot coincidence at founding is $\approx 10^{-8}$). If $C+B$ succeeds in $G\frac{5}{6}$ (7 splits, $\delta/7 \approx 0.007$) but underperforms in $G\frac{1}{3}$ (19 splits), it will be due to per-split dilution ($1/19$ vs $1/7$), not game mechanics. Fix: add a per-split matched dose diagnostic or note the dilution factor.

---

### 5. Ideas that matter beyond this experiment

Nothing material.
