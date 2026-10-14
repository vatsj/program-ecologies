# Review of `specs/2026-10-13-stable-sets-on-islands.md` by gemini-4-argon

**1. Design flaws and confounds**

* **Grid mismatch between symmetric and discriminatory stable sets:** On the 1/6 demand grid, if the excluded player gets $c = 1/6$, the remaining $5/6$ cannot be split equally by the winning pair; their closest split is $(3/6, 2/6, 1/6)$. Thus, at $mN = 0$, a $(3/6, 3/6, 0)$ island cannot flip to a discriminatory element without *two* slots changing demands, whereas in a $(3/6, 2/6, 1/6)$ state, the excluded player ($1/6$) and the junior partner ($2/6$) can form a $(3/6, 3/6, 0)$ pair where both strictly improve ($2/6 \to 3/6$ and $1/6 \to 3/6$). On a 1/6 grid, $(3/6, 2/6, 1/6)$ is actually *dominated* by $(3/6, 3/6, 0)$! The discriminatory stable set only exists when $1 - c$ is divisible or in continuous space; on the 1/6 grid, $c = 2/6$ gives $(2/6, 2/6, 2/6)$ (the fair split, not a pair). **Fix:** Either use an even-remainder grid (e.g., 1/8 grid with $c = 2/8$, so the pair splits $6/8$ into $3/8, 3/8$, or 1/10 with $c = 2/10$), or explicitly check in `test_stable_sets.py` whether *any* discriminatory stable set is internally and externally stable on the discrete 1/6 grid before running.
* **Single-migrant vs. coalitional transitions at $mN = 1$:** An external-stability move from $(3,3,0)$ to $(0,4,2)$ requires the excluded player (slot 3) to demand 2 *and* slot 2 to demand 4. Under $mN = 1$ (without mutation $\varepsilon = 0$), a single migrant from another island only imports one slot's demand unless slot 2 already has latent conditional responders or polymorphic diversity, or migrants from two different islands arrive. If islands are monomorphic constants, a single migrant changing slot 3 from $\ge 3$ to $2$ does nothing unless slot 2 already wants 4. **Fix:** Log whether flips at $mN = 1$ are triggered by single-slot migrations exploiting conditional programs, or two-slot coincidences, and include a **constants-only control** at $mN = 0$ and $mN = 1$.

**2. Predictions that are likely wrong**

* **Prediction 1 & 2 (Symmetric 50–50 dominance vs. unequal pairs):** The brief notes that in the $\varepsilon \to 0$ chain (`dollar3`), π put 0.98 on pairs, which were *mostly unfair* (from `RESULTS`: "stochastic stability selects rotating, mostly unfair pairs... fixed-role π is a rotating dictatorship of the largest demand by an accommodator ratchet"). At $mN = 0$ in the seed lottery, 3-player fixed-role islands are much more likely to absorb into **unequal pairs** $(4/6, 2/6, 0)$ or $(5/6, 1/6, 0)$ than $(3/6, 3/6, 0)$, because in fixed-role scramble dynamics, greedy demands establish against accommodators. **My prediction:** The strict symmetric vNM set $\{(3,3,0), (3,0,3), (0,3,3)\}$ will hold $< 0.4$ of islands at $mN = 0$ (falsifying Pred 1); *all pairs combined* (including unequal ones) will hold $> 0.7$, and the unequal pairs will be labeled "discriminatory" or "interlopers" depending on how the classifier treats $(4,2,0)$.
* **Prediction 4 (No global norm at $mN = 1$):** With $I = 64$ and $mN = 1$, finite-island neutral drift / contagion can easily cause one pair (or a 2-pair cycle) to sweep the metapopulation by $T = 10,000$ unless the three pairs actively re-invade each other in a rock-paper-scissors rock-cycle. If they cycle, coverage stays high; if constants fixate and lock out third-slot entrants, one pair absorbs.

**3. Missing controls or cheap additions**

* **Classify $(4/6, 2/6, 0)$ and $(5/6, 1/6, 0)$ explicitly:** In a 3-player majority game where a pair's agreement is implemented by majority regardless of the third player's demand, any unequal pair $(4,2,0)$ has the third player getting $0$, not $c > 0$. Do not conflate **unequal pairs** $(x, 6-x, 0)$ with **discriminatory stable sets** (where the third player gets $c > 0$ across two different pairs, e.g., $(1-c)/2, (1-c)/2, c$). Report their island shares separately.
* **Constants-only arm:** Cheaply run the pure constant-demand subgrammar to see if conditional programs (weak arm) or provers (modal arm) play any role in mediating the coalitional transitions at $mN = 1$.

**4. Alternative explanations not ruled out**

* **Pairwise risk-dominance / accommodator ratchet vs. vNM stability:** If all three pairs show up on islands at $mN = 0$, that follows trivially from **role symmetry of the prior** + **efficiency of pairwise coordination** (any two players whose demands sum to 6 win the pot, whereas 3-way splits require 3-way coordination). It does not distinguish vNM stability from simple 2-player coordination basin size. The true test of the vNM mechanism is $mN = 1$ (whether dominated states are actively replaced via external-stability coalitional moves).

**5. Ideas beyond this experiment**

* Nothing material.
