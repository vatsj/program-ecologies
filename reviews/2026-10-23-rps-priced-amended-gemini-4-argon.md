# Review of `specs/2026-10-23-rps-priced.md` by gemini-4-argon

**1. Errors, contradictions or unsound mechanisms**

* **Depth cap vs. work charge.** "The default price is a cost per application level... Each player pays c per application node its own root evaluation executes... Evaluation stops at the depth cap D; a forfeit pays for the applications executed up to the cap (D for a linear recursion)." 
  * *Issue:* A depth cap $D$ bounds recursion *depth*, not application *nodes* (work). A tree-recursive program (or `cr` evaluating both branches of a nested `coin` program, or a program calling `THEM(ME)` twice per level) executes $O(2^D)$ application nodes before hitting depth $D$. Under a per-node work price, such a program pays up to $c \cdot 2^{12} \approx 4096c$ (which is $>200$ at $c=0.05$), not $c \cdot D$, and blows up evaluation time. Furthermore, the **depth panel** ("holding $c \cdot D = 0.12$ fixed at $D \in \{8, 16\}$") assumes timeout cost is $c \cdot D$, which is false for branching evaluation unless the cap itself is on work or the forfeit cost is capped.
  * *Fix:* State explicitly whether $D$ caps recursion depth or total work, and whether a player's cost per match is capped at $c \cdot D$ or uncapped. If uncapped, verify the maximum node count in the grammar so payoffs don't explode and break the $w=0.3$ chain scaling.

* **Dominant-class resolution vs. polymorphic islands.** "The game is no longer zero-sum, so the chain may now hold polymorphic states." vs. "An island is *resolved* when its dominant class has not changed over the last 500 generations; the unresolved fraction is reported, and runs with any unresolved island continue to 10,000 generations."
  * *Issue:* In RPS, if an island settles into a polymorphism of constants (R, P, S) or a reader–constant cycle, the dominant (plurality) class will fluctuate by finite-$N$ drift or replicator cycling forever. This is a genuine polymorphic regime, not an "unresolved" transient, and will needlessly force every run to 10,000 generations.
  * *Fix:* Define island resolution by stationarity of the *support* (e.g., top-3 classes or K-L divergence over 500-gen windows) or cap the extension to islands without cyclic/polymorphic support.

* **Paired founders across split classes.** "...paired founders with the unpriced run (same seeds)... Classes are recomputed from the priced payoff rows and columns".
  * *Issue:* If founders are drawn at the class level in `src/rps*.py`, splitting classes changes the sampling index and breaks RNG pairing.
  * *Fix:* Ensure founders are drawn at the *program* level (prior over syntax) and mapped to the new classes *after* seeding.

**2. Design flaws or confounds**

* **Exploitability baseline.** "exploitability is measured on the game payoff alone... net exploitability (the exploiter's game payoff minus its own cost) is reported beside it".
  * *Issue:* The predictions (2, 3, 5, 7) still score "exploitability" without specifying which one. Under a work price, an island of constants that is unexploitable *net* of reading cost (e.g., when $c$ is high or for deep `cr` readers) will be scored as highly exploitable by the unpriced metric.
  * *Fix:* Specify that Predictions 2, 3, 5, and 7 are scored on *net* exploitability (or report both and bind the falsifiers to net).

**3. Predictions I think are wrong**

* **Prediction 6 (`X` beats all source-readers combined in the lottery at $c=0.01$).**
  * *Reason:* `X` earns 0 against constants. A 1-step reader like `next(coin(THEM(ME), R))` or a coin-guarded reader pays $c \approx 0.01$ to read a constant and earns $+0.5$ or $+1$ against the constant-heavy founding scramble, while avoiding the $c \cdot D$ self-forfeit at least 3/4 of the time. In the founding scramble, exploiting constants at cost $0.01$ easily beats `X`'s flat $0$.
  * *My prediction:* Coin-guarded readers hold more lottery mass than `X` at $c = 0.01$; `X` only dominates at $c = 0.05$ or in the large-$N$ chain.

**4. Missing controls or cheap additions**

* Nothing material (the first review's `forfeit-only` and `depth panel` controls are the right ones, once the work vs. depth cap in #1 is fixed).

**5. Alternative explanations not ruled out**

* If `exact` ($cr$) underperforms `sample` at $c \ge 0.01$, it may be entirely because $cr$ pays for *all* coin branches (exponentially more work nodes than `sample` at the same depth) rather than any strategic property of distributional reading. A cheap diagnostic reporting `exact` evaluated under the *expected-branch* work cost (same cost rule as `sample`) would isolate semantics from the branching tax.
