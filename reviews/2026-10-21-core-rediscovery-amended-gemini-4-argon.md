# Review of `specs/2026-10-21-core-rediscovery.md` by gemini-4-argon

### 1. Errors, contradictions or unsound mechanisms

- **Overbidding `PRU` defaults in the unrestricted arm:**
  > "It plays the best reply to the others' resolved bids when that reply is strictly profitable, else its default c, capped at its value."
  > "its default uniform over the grid."
  In the unrestricted space (0..40), capping `PRU(c)`'s default at its value $v_i$ while constants remain uncapped means `PRU` can never hold a losing overbid (e.g. $c = 25$ for P in *threshold*) and piles prior mass onto $c = v_i$. **Fix:** Cap $c$ at $v_i$ only in the *no-overbid* arm; in the *unrestricted* arm let `PRU(c)` play $c \in 0..40$ when no winning bid is strictly profitable, or explicitly restrict Stage 1b to the *no-overbid* space.

- **Under-specified best reply on integer grid with random ties:**
  > "It plays the best reply to the others' resolved bids when that reply is strictly profitable... For P, the best reply wins AB at the item bids' total plus one. ... Ties use the seller's random tie rule"
  Because ties win with probability $1/2$, tying at $S = b_A + b_B$ gives P payoff $\frac{1}{2}(v_P - S)$, whereas outbidding at $S+1$ gives $v_P - S - 1$. When $S = v_P - 1$ (e.g. $S = 19$), $S+1$ gives $0$ (not strictly profitable), while tying at $S = 19$ gives $+0.5$ (strictly profitable). When $S = v_P - 2$ ($S = 18$), tying and outbidding tie in expected payoff ($+1.0$). **Fix:** State whether "best reply" maximizes expected payoff over all grid points (breaking ties in favor of winning outright, or lower bid) or uses the literal $+1$ formula (which misses profitable ties at $v_P - 1$).

- **Payoff-weighted migration in a 3-role asymmetric game:**
  > "and the stored mN rule (secondary; state the migration weighting and which role's payoff it uses)."
  The brief defers a design choice to the subagent. Worse, in *collusion* (where A and B get 0 in the core) or *threshold* (where P gets 0), weighting whole-island emigration by a single losing role's payoff reduces to neutral migration, while summing bidder payoffs selects *against* seller revenue (favoring eroded rings). **Fix:** Specify per-role independent migration weighted by that role's own payoff, or cut the migration arm from Stage 1.

### 2. Design flaws or confounds

- **Generation-scale mismatch:** Running $N=100$ for $5,000$ generations is $50N$ generations. At $\varepsilon = 0$, neutral drift of a losing role fixes in $\sim 2N = 200$ generations, so $5,000$ is fine. Under constant rain ($\varepsilon N = 0.05$) or the annealed tail, $50N$ is only ~2.5 neutral turnover times—too short to distinguish stationary core maintenance from slow erosion. **Fix:** Either report the constant-rain arm as a short-horizon diagnostic or extend it to $20,000$ generations.

### 3. Predictions you think are wrong

- **Prediction 5 (`PRU` holds the losing role on most core islands at $\varepsilon = 0$):** Wrong on mechanism. Once the winning roles (A and B) lock into bids summing to $\ge 20$, `PRU(c)` in role P never triggers its best-reply branch and behaves identically to constant $c$. It has no selective advantage over constant $c$ once in the core, and having prior mass $m = 0.2$, it will only fix in the losing role on roughly $\sim 20\%–35\%$ of core islands (slightly above prior due to early scramble wins), not "most" ($>50\%$). **My prediction:** Core islands will exceed 50%, but `PRU` will hold the losing role on $< 40\%$ of them; its main effect is weeding out underbidding A/B early so high-bidding P constants survive.

### 4. Missing controls or cheap additions

- **Asymmetric-instance `PRU` cell:** Running Stage 1b on *asymmetric* (not just *threshold*) cheaply tests whether `PRU`'s sequential evaluation order (P, A, B) biases the core split between A and B (Prediction 6).

### 5. Alternative explanations the brief does not rule out

- **Truncation bias in the unrestricted arm:** In *threshold*, P's losing bids in the core can drift over $20..30$, whereas eroded losing bids can drift over $0..19$. Upward vs. downward drift of the losing bid is confounded by the asymmetric available grid space above and below $v_P = 20$. The *no-overbid* arm rules out the upper range, but comparing erosion rates between the two arms must account for the fact that 25% of P's uniform prior in the unrestricted arm starts at $\ge 30$ (blocking A and B entirely).
