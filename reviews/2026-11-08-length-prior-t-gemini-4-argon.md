# Review of `specs/2026-11-08-length-prior-t.md` by gemini-4-argon

1. **Design flaws or confounds**
- **Missing junk and constant-tilt in Step 2 (breaks the Step 3 join):** Step 1 notes that under a length prior, junk mass (>0.50 predicted in RE 7) defaults to code 8 `(ALL, 2/3)` and pays $P_{\text{fail}} = 0.1$, and valid constants will naturally skew toward code 0 `(0, 1/3)` under Elias-$\gamma$ coding. Yet Step 2 keeps constants at arm T’s clean, hand-set within-family proportions and simulates zero junk. Also, the Step 3 formula $\delta_{\text{LP}} = \rho_R / (1 + \rho_R + \beta\rho_R)$ divides by constants + readers + bullies, ignoring junk and lost mass!
  *Fix:* Define $\delta_{\text{LP}}$ as the conditional probability among *halting/valid* programs, OR explicitly include a junk program (code 8 minus $0.1$) in $T^+$ at the Step 1 measured mass. In Step 2, add a control series where constants are weighted by their Step 1 Elias-$\gamma$ distribution rather than T's main-dose proportions.
- **Unreachable $\delta^*$ at high $\beta$:** At $\beta = 3$, $\delta = 0.1$ gives $1 - 0.1 - 0.3 - 0.011 < 1$ (valid), but if $\delta^* > 0.1$ at $\beta = 3$, the grid tops out and $\delta^*$ is censored.
  *Fix:* Add $\delta = 0.2$ for $\beta \in \{0, 0.3, 1, 3\}$ (where valid, i.e., $\delta(1 + \beta + 1/9) \le 1$).
- **Superficial tree explosion in Step 1:** Uniform tag drawing over 18 tags where binary/ternary nodes outnumber leaves makes the branching process supercritical (lost mass near 1, exhaustive enumeration $s_0=9$ capturing tiny mass).
  *Fix:* Verify expected branching factor of `lt_code.py` tags before running; if supercritical, report conditional distribution on finite trees alongside the raw semimeasure.

2. **Predictions I think are wrong**
- **RE 4 ($\beta \ge 0.3$ under R0):** Likely wrong. A fair single-partner reader only needs to read one partner and branch on whether they play $1/2$ (or copy/accommodate). A Trojan bully ("if $j$ names me at $1/3$, name $j$ at $2/3$, else name $k$ at $1/2$") requires an extra conditional check on a specific $1/3$ code and two distinct non-default action branches. In $L_T$, each extra `if`/`eq` and literal adds 3–5 nodes $\approx (1/18)^4 \approx 10^{-5}$ relative mass. *My prediction:* $\beta < 0.05$ under both R0 and R1.

3. **Missing controls or cheap additions**
- **Two-partner reader share:** Step 2 fixes single- to two-partner readers at 2:1. Under R0 and R1, two-partner readers are much longer than single-partner readers, so the length prior ratio is $\approx 1 : 0$. Run a cheap Step 2 slice at $N=200, I=64, \beta=0$ with *only* single-partner readers to verify they carry $V^*$ alone.
- **Founder vs. tail separation:** At threshold $\delta^*$, test one cell with founders at $\delta^*$ and tail $\Lambda=0$ (and vice versa) to see whether $c^* = I N \delta^*$ (founders) or $I \Lambda \delta^*$ (tail) is the binding copy count.

4. **Alternative explanations the brief does not rule out**
- **Elias-$\gamma$ constant bias vs. reader scarcity:** If R1 fails to reach $V^*$ in reality, it might not be because $\delta_{\text{LP}} < \delta^*$, but because Elias-$\gamma$ heavily weights code 0 (a $1/3$-naming constant, since $\gamma(1)=1$ bit vs $\gamma(9)=7$ bits). Queue 74 showed $1/3$-naming constants are what feed bullies and sink M. Step 2 misses this by keeping T's constant proportions.

5. **Ideas that matter beyond this experiment**
- Nothing material.
