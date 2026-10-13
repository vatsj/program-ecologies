# Review of `specs/2026-10-13-sog-fully-realizable.md` by gemini-4-argon

### 1. Design flaws or confounds

* **Reduced-support pruning drops production stepping stones.** The executable support keeps classes with prior mass $\ge 10^{-4}$ plus named classes and those *present at seeding in the paired H runs*. Under **S-nonself₃**, a worker cannot write its certificate against a twin; it requires a distinct-source partner (often a rare variant or constant not needed when H supplies certificates for free). If the paired H run did not seed that donor, or if you prune to classes that *survive* in H rather than all initial founders, S-nonself₃ will suffer artificial bootstrap failure.
  * *Fix:* Ensure the executable support includes the union of *all initial founders* across the 40 seeds, plus at least one distinct-source copy/synonym for each named militant and concession class so non-self production is always syntactically possible if seeded.
* **Residual-budget coupling ($P = K/4$ inside $K$).** Running production in the "residual budget" after play means heavy verification ($\approx 3.75\cdot 10^5$ steps) starves production even when production itself takes $< P$ steps. This confounds verification cost with production feasibility.
  * *Fix:* Log and separate "production starved by play/verification ($K - \text{steps}_{\text{play}} < \text{steps}_{\text{prod}} \le P$)" from "production exceeded $P$."

### 2. Predictions I think are wrong

* **Prediction 2 (H + eq greenbeard share $\ge 0.2$) is likely wrong (too high).** In the three-player game, a greenbeard union $U_{\text{eq}}$ strikes only beside an *exact source copy* of itself in the other worker slot. Unlike the two-player PD where a clique can invade via self-recognition upon local fixation, here $w_1$ and $w_2$ are separate populations. For $U_{\text{eq}}$ to hold an island, *both* worker slots must simultaneously nucleate and fix the exact same spelling of $U_{\text{eq}}$. Under independent seeding of $w_1$ and $w_2$ at $N=100$, the probability of co-seeding and co-fixing the same rare greenbeard in both slots is tiny; before co-fixation, $U_{\text{eq}}$ mostly meets non-copies and acts as a scab (works at wage 0), undermining the strike threat and failing to trigger the boss's concession.
  * *My prediction:* $U_{\text{eq}}$ holds $< 0.05$ of fair islands even in **H + eq**, falsifying Prediction 2's H bound.
* **Prediction 6 (conditional fitness of $B_{\text{eq}}$) will be vacuous or falsified.** Because $B_{\text{eq}}$ checks for the literal quote $\ulcorner T_1 \urcorner$ (an open militant, not a greenbeard), tying $B_{\text{eq}}$'s boss-slot share to islands held by *greenbeard unions* ($\ge 0.2$) mismatches the target of the quote. Moreover, if greenbeard unions stay below $0.05$ in all arms (as predicted above), the $\ge 0.2$ condition will never be tested.

### 3. Missing controls or cheap additions

* **Pairwise vs. triple non-self gate ($S\text{-nonself}_2$ vs. $S\text{-nonself}_3$).** In $S\text{-nonself}_3$, a worker refuses to produce a certificate if *either* $w_2$ or $b$ shares its source. Since boss and worker grammars/roles are distinct, $\text{source}(w_1) = \text{source}(b)$ is impossible or vacuous, meaning the gate is effectively just $\text{source}(w_1) \neq \text{source}(w_2)$. However, if two workers are twins ($w_1 = w_2 = T_1$), they cannot produce a strike certificate against a distinct boss $b$, even though the strike is *against* $b$. Add a cheap static check (or diagnostic arm) where non-self is required only against the *opponent* ($b \neq w_1$) vs. the *coalition partner* ($w_1 \neq w_2$), as blocking production when $w_1 = w_2$ directly penalizes homogeneous worker slots after fixation.

### 4. Alternative explanations not ruled out

* **Worker-homogeneity deadlock under $S\text{-nonself}_3$.** If fair persistence drops in $S\text{-nonself}_3$ relative to H, the brief attributes it to bootstrap/production cost or identity cliques. An alternative is **post-fixation certificate loss**: once a single open militant $T_1$ sweeps both $w_1$ and $w_2$ on an island, $\text{source}(w_1) = \text{source}(w_2)$ holds in every encounter. Any new mutant or migrant without a pre-existing certificate (or if inheritance is imperfect across roles) cannot produce one because all coworkers are copies. Forced-coalition assays with *one* uncertified $T_1$ entering a fixed $T_1$ island are needed to rule this out.

### 5. Ideas beyond this experiment

* Nothing material.
