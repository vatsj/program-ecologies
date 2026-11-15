# Review of `specs/2026-11-15-certified-offers.md` by gemini-4-carbon

### 1. Design flaws or confounds

* **Rc’s read of the excluded slot breaks legibility and soundness:** The spec says Rc "also accepts a plain ½ constant naming it, as R does." To do this, Rc’s fallback must *simulate* the excluded slot $e$! This violates the spec's own fallback semantics ("otherwise I play a (a named constant action)") and ruins legibility: if a simulating reader ($F$ or $B$) sits in $e$ and a simulating bully ($B$) holds the ⅔ seat, $B$ simulates Rc, which simulates $e$, which simulates $B$—recreating the exact mutual regress and timeout ($P_{\text{fail}} = 0.1$) from Queue 78. **Fix:** Either drop Rc's simulation of plain ½ constants (pure certificate check + constant fallback "name partner at ⅓"), or include two variants: pure-certificate `Rc0` and hybrid `Rc_sim`, and fix RE 2 accordingly.
* **Fc and Bc fallbacks recreate mutual regress:** Fc and Bc fall back to bounded simulation of non-carriers. Thus, simulating bully $B$ against Fc (or Bc against $F$) will time out, charging $P_{\text{fail}}$ and dropping offers. Furthermore, `check` costs $\kappa$ inside the read cap: if $B$ simulates Fc, and Fc runs `check` ($\kappa$) *plus* fallback simulations of two non-carriers, Fc will easily exceed $B$'s nested read cap even without regress. **Fix:** Specify $\kappa$ small enough (e.g., $\kappa \ll \text{cap}/3$) so a simulated carrier's checks + fallbacks fit inside one outer read cap, and explicitly gate-check $B \times \text{Fc}$ and $\text{Bc} \times F$ for cap exhaustion.
* **Three-carrier tie-breaking underspecified:** Leaving the 3-player rule open ("uses $K_3$'s closure or a simpler rule") risks turning $3/4$ of three-carrier profiles into $n \to n \to n$ cycles if preferences are independent. Under `sog_realizable.py` closure, outcomes differ from naive local preference breaking. **Fix:** Lock the exact rule in the spec before coding: if each carrier checks only pairwise certificate existence and breaks ties by its own `next`/`prev` orientation, $2$ of $8$ orientation triples cycle ($1/4$). State this explicitly rather than treating a cycle as an open engineering surprise.

### 2. Predictions that look wrong

* **RE 2 (legibility):** *Wrong as written if Rc simulates $e$ for ½ constants.* If $e$ is a simulating reader ($F, O, B$), $B$'s read of Rc will re-enter $B$ through $e$ and time out, driving $\rho \cdot N \ll 0.1$ (falsifying RE 2). It holds *only* for a pure non-simulating `Rc0` or when $e$ is a constant/pure-carrier.
* **RE 10 (mixed worlds):** *Likely wrong (too pessimistic) at $\beta \ge 1$ if pure carriers don't simulate.* Unlike $F \times O$, pure carriers (`Oc`, `Rc0`) do not time out when read by $F$ or $O$; legibility is one-way safe. The mixed arm should sit *between* the pure arms, not below the lower one, unless Fc's fallback simulation dominates.

### 3. Missing controls or cheap additions

* **Pure vs. hybrid Rc (`Rc0` vs `Rc`):** Cheap addition in Step 0 and one seeded start. Isolates whether accepting plain ½ constants helps (abundant offerers) or hurts (restores bully read timeouts when readers occupy $e$).
* **$\varphi = 1$ seeded unequal start with `Fc+Oc+Rc`:** You already seed all-unequal with Bc, so ensure $\varphi = 1$ (all incoming tail bullies are Bc) is tested there too—otherwise $\varphi = 1/2$ mixes simulating bullies into a Bc-seeded test.

### 4. Alternative explanations not ruled out

* **Three-carrier coordination cycles ($1/4$ of (`Fc`, `Fc`, `Fc`) encounters):** If `Fc` fails to lift $V^*$ at $\beta = 1$ or $3$, you will attribute it to the founding scramble or two-step pacing, when it could partly be `Fc` losing fitness in the scramble to $n \to n \to n$ disagreement cycles that constants avoid. Check mean payoff of `(Fc, Fc, Fc)` averaged over orientations in Gate 2; RE 9 ($\beta=0$) bounds this weakly at $\delta=0.03$, not at $\delta=0.1$.

### 5. Broader ideas

Nothing material.
