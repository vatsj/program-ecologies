# Review of `specs/2026-10-23-rps-mixed.md` by gemini-4-argon

**1. Design flaws and confounds**

* **Undefined semantics of `next` and `br` on forfeit:** If subexpression `A` produces positive probability of `forfeit`, what do `next A` and `br A` evaluate to? 
  * *Fix:* Declare explicitly: `next(forfeit) = forfeit` (propagating non-termination in `sample` and `pure`). For `br A`: specify whether `br` optimizes expected payoff against A's *full* distribution (including forfeit, which any R/P/S beats with +1, making `br(forfeit) = X` by tie-breaking) or whether `br` is strict and forfeits if A's forfeit mass is 1 (or > 0). Wait: if `br(forfeit) = X`, then `br(THEM(ME))` against itself does *not* forfeit at even depths! At D=0 it forfeits; at D=1 `br(forfeit)` becomes `X`; at D=2 `br(X)` becomes `X`, so `br(THEM(ME))` self-play terminates as `X`! To preserve Prediction 1 (`br(THEM(ME))` self-play forfeits), `br` must propagate forfeit: if A draws `forfeit` with probability $p_f$, `br A` forfeits with probability $p_f$ and best-responds to the conditional non-forfeit distribution with probability $1 - p_f$ (or `br A` forfeits whenever $p_f > 0$). Pin this down before coding.
* **Lottery horizon vs. neutral cyclic drift:** In RPS, an island without `X` or `br` (or where constants beat out rare readers early) will undergo neutral stochastic cycling ($R \to P \to S \to R$) on each island, while migration $mN=1$ couples them into a spiral wave or polymorphic soup. Measuring "individual mixing" and "in-population exploitability" at a single snapshot $T=2,000$ confounds (M) polymorphic population mixtures with (I) individual mixers.
  * *Fix:* Keep the statistics separate, and also log the time-averaged within-island homozygosity (or number of distinct active behavioural classes per island) over $[1500, 2000]$ to distinguish a monomorphic `X` island from a 3-constant polymorphic island.

**2. Wrong predictions**

* **Prediction 3 (Pure arm holders are forfeiting readers, $\pi(\text{constants}) \le 0.2$):** Likely wrong. `next(THEM(ME))` ($M$) earns 0 against itself (mutual forfeit), +1 against constants ($R, P, S$), and **+1 against `next(M)`** because `next(M)` against $M$ evaluates $M(M) \to \text{forfeit}$, so `next(M)` forfeits while $M$ plays $M(\text{next}(M)) = \text{next}(\text{forfeit}) \to \text{forfeit}$... wait: both forfeit! Actually, what beats $M$? If $M$ against $C$ plays `next(C)`, what if a program $P$ plays $R$ against constants but loops against $M$? In the `pure` grammar without `eq` or conditionals, every program is just $next^k(\text{head})$. A program with head `ME` or `THEM` loops against every other reader! Thus *all* readers mutually forfeit (0) and beat constants (+1) or lose to `next`-shifted readers. Check by hand whether `THEM(THEM(ME))` beats `next(THEM(ME))` by 1 step of depth at cap $D=12$: at a hard depth cap $D$, a shallower reader terminates against a deeper reader that hits $D$ and forfeits!
  * *My prediction:* Hard depth cap $D=12$ creates a **depth-cap ladder** in the pure arm (analogous to the price ladder), where shallower readers beat deeper readers right at the boundary $D$, or constants cycle because readers all mutually tie at 0 and drift neutrally among themselves.

**3. Missing controls or cheap additions**

* **Depth-parity check ($D=11$ vs $D=12$):** In zero-sum cyclic recursion (`next(THEM(ME))`), odd vs. even depth caps flip who hits the base case first when two programs of different syntactic nesting depths meet. Add $D=11$ and $D=13$ to the 1,000-pair check to verify that payoffs don't depend on $D \bmod 2$ or $D \bmod 3$.
* **Unconditional `X` shadow in the exact arm:** In `exact`, `X` (1 node) and `coin X (br(THEM(ME)))` (6 nodes) tie in self-play (0), and `X` is completely unexploitable (earns 0 against everything). Thus `X` is a **1-node neutral shadow** of every guarded mixer! Report $\pi(X)$ vs $\pi(\text{guarded readers})$ explicitly: if `X` dominates by prior weight ($2^{-1}$ vs $2^{-6}$), then `exact` won't select `X` much more than `sample` does, because `X` *already* exists in `sample`!

**4. Alternative explanations**

* **Why `exact` beats `sample` (if it does):** `X` is already in `sample` at 1 node and is unexploitable. In `sample`, `X` drifts out to constants (neutral 0 vs 0 against $R$), and constants get eaten by `next(THEM(ME))`. In `exact`, `br` also ties `X` (0 vs 0)! The only way `exact` holds `X` better than `sample` is if `br` kills biased `coin` mixers that `next` only partially exploits—OR simply because adding `br` adds more reader mass to the prior that punishes constants faster. Control for total reader prior mass when comparing `sample` and `exact`.

**5. Ideas for the research program**

* Nothing material.
