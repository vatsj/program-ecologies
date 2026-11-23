# Review of `reviews/tiered-best-response-RESULTS-draft.md` by gemini-4-carbon

1. **Empty arrival-set range in T and M**
- **Draft:** "In T and M, most residents never met an on-path equivalent: the arrival sets are empty in 55–96% of cases."
- **Evidence:** In stage 1 (the RE 4 pool), empty arrival sets in M at $N=400$ are 68 of 287 = 23.7% (`M|main|400|100|1`, `ar_empty: 68`, `n_cases: 287`), and across all cells in the table they range from 16.9% (372/2197 in T at $mN=0.1$) to 100% (183/183 in T at $\Lambda=0$, 2/2 in T at $mN=3$, 235/235 in T stage 3). Even in T stage 1 alone the range is 67.5%–96.0% (185/274, 96/100, 255/280).
- **Correction:** Replace "55–96%" with "68–96% in T and 24–91% in M (stage 1)" (or "24–96% across stage-1 cells").

2. **RE 4 pool composition and how empty arrival sets enter the pooled verdict**
- **Draft:** "It is mostly supply (RE 4 holds by rule, on few cases)... In P the founder-weighted control removes about a quarter of the excess."
- **Evidence:** `runs/tiered-best-response.json` (`verdicts.RE4`) scores RE 4 on the pooled excess 0.090 vs 0.185 (threshold $< 0.0923$). Because empty arrival sets are dropped in T and M (leaving only $25+4+89=118$ cases in T and $44+219=263$ in M) while all 3,017 cases in P (dense + natural) are retained under the founder-weighted control, ~89% of the RE 4 pool is arm P, and the pooled supply excess (0.08995) barely clears half of 0.1846 (0.0923). Also, in the RE 3/RE 4 pool, P's excess is 0.178 (pooling dense 0.199 and natural 0.000), reduced to 0.135 by the founder control; the draft's earlier RE 3 bullet cites only P dense (0.47 vs 0.28, excess 0.20) without noting P natural (0.44 vs 0.44, excess 0.00) is in the RE 3/RE 4 pool.
- **Correction:** Note in the RE 3 bullet that P's stage-1 pool includes natural (excess 0.00, giving P pooled excess 0.18), and in RE 4 / Scope (v) state that dropping empty arrival sets leaves 118 T and 263 M cases alongside 3,017 P founder-control cases (pooled supply excess 0.090 vs 0.185).

3. **Prior tier zero-regret share description**
- **Draft:** "In consensus worlds residents' zero-prior-regret share is within 0.03 of the control."
- **Evidence:** 0.031 [$-0.027, +0.095$] is the *pooled* excess across T and M at $\Lambda = 100$ (`verdicts.RE7`). Per cell at $\Lambda = 100$, arm T's T-weighted excess is 0.024–0.120 (0.089 at $N=100$, 0.064 at $N=200, mN=1$, 0.060 at $mN=3$, 0.120 at $mN=10$, 0.024 at $N=400$), and arrival-weighted is 0.037–0.196 (`runs/tiered-best-response.md`, Summary & Prior tier table).
- **Correction:** Change to "In consensus worlds at $\Lambda = 100$, residents' pooled T-weighted zero-prior-regret share is 0.031 above the control (0.00–0.03 in M, 0.02–0.12 in T)."

4. **Stage 1b arm T label and neutral-tester error range**
- **Draft:** "(P 51 of 51, T 19 of 22 against N·ρ = 1)" and "A neutral tester does not: ... errors from −64% to +218%".
- **Evidence:** In stage 1b, 19 of 22 is the exploratory `T_diverse` run; the registered stage-1b arm T run had 4 of 4 (and arm M had 0 of 0, no $|\sigma| \ge 0.5$ cases). In stage 0b, relative errors across *all* tester cases reach $-87\%$ (`rq0.9_better`, $N=400, \sigma=-3$, rel. error $-0.87$) and $+124\%$ (`rq0.9_worse`), while for `rq0.7` at $N=400$ two points are $+41\%$ (which also triggered `off40` in `verdicts.RE2`, though RE 2's 25%/40% rule applied only to the neutral tester).$-64\%$ to $+218\%$ is specifically the neutral-tester range; that part is accurate as written, whereas `T 19 of 22` in stage 1b omits that it is the exploratory diverse-world set (registered T is 4 of 4).
- **Correction:** In the Frozen natives bullet, write "T 4 of 4 (19 of 22 in the exploratory diverse-world set)".
