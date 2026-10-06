# Run: the realizable language, milestone 3: the prover as code (2026-10-06)

Spec `specs/2026-10-06-prover-as-code.md` (reviewed by gpt-6.1-sol); predictions
`predictions/2026-10-06-prover-as-code.md` (committed after notes §1 and before any code); notes
`notes/prover-as-code.md` (§1, the gate: L_T^code, the fuel rules, K_T^code with every rule's obligation, soundness,
visibility, the hand-checked JLöb instances, committed before any code; §1.10, their code validation, and §2.1,
the evaluator's exact accelerations, committed before any counted cell; §2.2, the benchmarks). Code:
`src/lt_code.py` (language, reference stepper, compiled evaluator, s-expression compiler, the library in L_T:
self-interpreter, checker, search; the catalogue; the host oracle; the independent replay checker; the brute-force
prover), `src/lt_code_run.py` (driver, 3 workers), `src/lt_code_report.py` (tables), `tests/test_lt_code.py`.
Raw per-task JSON in `runs/prover_as_code/` (62 tasks, 903 s of compute); summary JSON `runs/prover-as-code.json`.

**What was run.** Every program searches by calling `SEARCH_i`, a library term: a wrapper that runs the core
(closure by the self-interpreter, then an iterative-deepening memoized minimal-size search over K_T^code, all in
L_T^code) inside a frame of its declared cap U = ⌊K/4⌋. A play is the actual run of `p ⌜p⌝ ⌜q⌝` with global fuel K;
nothing is answered by the host. Cells: the 13-program catalogue (C, D, FB, FB1, PB, G, P\*, SF with k = K/2, SC_code,
Vlet, Vwrap, FB2, FBx) at K ∈ {10⁵, 10⁶, 10⁷} × b ∈ {8, 12, 16, 24, 32, 64}, every ordered pair, in the calculus and
in the JLöb-disabled control (CORE_2); thresholds on b = 2..20 at each K; the FairBot grid {8, 12, 16, 32}² at each K;
leak cells SF_k (k ∈ {10³, 10⁴, 10⁵, 10⁶, U + 8, U + 9, U + 10, U + 11}) against ten readers in both orders at every
(K, b); fuel-boundary cells; the benchmark of each program's first self-play query at K = 10⁷. Every core query
any task produced (6,354) went through the correctness harness.

**Decisions made before any counted cell** (notes §1.10, §2.1): (i) the evaluator's two exact accelerations, a cache
of core runs replayed with exact charging and the regress fast-forward (a call with the key of an enclosing frame
never returns before an enclosing counter is exhausted), both tested against the reference stepper; (ii) hand
instance 6 (SrchR's fit) replaced by the sim-frame case, the only one where the fit test is load-bearing.
**After the first launch** (a crash, before any table was read): the harness's audit entry COREW (the same search
plus witness reconstruction) ran under the program's cap U and was cut on queries that finished near U; it now runs
under 4U + 10⁶ (the search's trajectory is unchanged: the outer cap is not observed by the code). The SF boundary
cells were moved from K = 10⁶ to K = 10⁷ after the boundary task showed FB's search on plays(SF, FB, C) is
interrupted at U = 2.5·10⁵ (it needs about 3.5·10⁵ steps), so the 10⁶ cells could not test the boundary; the leak
task gained k = U + 10, U + 11 (the hand boundary had been U + 9). All tasks were then re-run from scratch.

**Coverage, in one line.** Of 6,354 core queries, 2,007 finished (1,164 found, 843 refuted) and 4,347 were
interrupted by their cap (at K = 10⁵ almost everything, since U = 25,000 is below FairBot's 1.12·10⁵; at 10⁶ and 10⁷,
almost all interruptions are the Run regress of distinct sources, which burns exactly U + 1 steps); no program-level
search was ever cut by an outer counter. Every table below reports f / r / i / x per search.

**Realizability caveat.** Nothing runs in the host as an oracle: searches, checks, the self-interpreter's steps and
nested runs are L_T^code steps, charged to the program's own fuel. What the host contributes is (a) the evaluator
itself (closure compilation, checked step-for-step against the substitution semantics), (b) two exact accelerations
of deterministic computations (cache replay, regress fast-forward; the step counts they charge are exact), and
(c) unit-cost primitives the language grants: structural `eq` on arbitrarily large values in one step (inherited
from L_T), RAM-style arithmetic, and `libsrc`. The search's 2,800 steps per node expansion are therefore an optimistic
constant for a "real" machine (an honest `eq` on configurations would cost their size). K_T^code remains a bounded
calculus for these terms' evaluation, not a bounded PA prover.
## 1. Benchmarks: search vs checking a supplied witness (K = 10⁷, U = 2.5·10⁶)

| program | b | result | search steps | expansions | rule instances | closure | witness size | check steps | check steps/node | rules |
|---|---|---|---|---|---|---|---|---|---|---|
| FB | 7 | T | 111930 | 40 | 70 | 8 | 7 | 12174 | 1739.1 | jlob EvR EvR SrchR EvR ax ax |
| FB | 8 | T | 112008 | 40 | 70 | 8 | 7 | 12174 | 1739.1 | jlob EvR EvR SrchR EvR ax ax |
| FB | 10 | T | 111904 | 40 | 70 | 8 | 7 | 12174 | 1739.1 | jlob EvR EvR SrchR EvR ax ax |
| FB | 12 | T | 111917 | 40 | 70 | 8 | 7 | 12174 | 1739.1 | jlob EvR EvR SrchR EvR ax ax |
| FB | 16 | T | 111930 | 40 | 70 | 8 | 7 | 12174 | 1739.1 | jlob EvR EvR SrchR EvR ax ax |
| FB | 24 | T | 111943 | 40 | 70 | 8 | 7 | 12174 | 1739.1 | jlob EvR EvR SrchR EvR ax ax |
| FB | 32 | T | 111930 | 40 | 70 | 8 | 7 | 12174 | 1739.1 | jlob EvR EvR SrchR EvR ax ax |
| FB | 64 | T | 111930 | 40 | 70 | 8 | 7 | 12174 | 1739.1 | jlob EvR EvR SrchR EvR ax ax |
| FB1 | 7 | F | 241447 | 66 | 108 | 11 |  |  |  |  |
| FB1 | 8 | T | 307156 | 86 | 135 | 11 | 8 | 9489 | 1186.1 | jlob impR EvR EvR SrchR EvR ax ax |
| FB1 | 10 | T | 310790 | 86 | 135 | 11 | 8 | 9489 | 1186.1 | jlob impR EvR EvR SrchR EvR ax ax |
| FB1 | 12 | T | 314502 | 86 | 135 | 11 | 8 | 9489 | 1186.1 | jlob impR EvR EvR SrchR EvR ax ax |
| FB1 | 16 | T | 321796 | 86 | 135 | 11 | 8 | 9489 | 1186.1 | jlob impR EvR EvR SrchR EvR ax ax |
| FB1 | 24 | T | 336449 | 86 | 135 | 11 | 8 | 9489 | 1186.1 | jlob impR EvR EvR SrchR EvR ax ax |
| FB1 | 32 | T | 351102 | 86 | 135 | 11 | 8 | 9489 | 1186.1 | jlob impR EvR EvR SrchR EvR ax ax |
| FB1 | 64 | T | 409649 | 86 | 135 | 11 | 8 | 9489 | 1186.1 | jlob impR EvR EvR SrchR EvR ax ax |
| PB | 7 | F | 123996 | 38 | 71 | 12 |  |  |  |  |
| PB | 8 | F | 478058 | 47 | 86 | 12 |  |  |  |  |
| PB | 10 | T | 564574 | 68 | 115 | 12 | 10 | 385929 | 38592.9 | jlob EvR EvR SrchR EvR SrchR EvR ax run ax |
| PB | 12 | T | 598514 | 68 | 115 | 12 | 10 | 419934 | 41993.4 | jlob EvR EvR SrchR EvR SrchR EvR ax run ax |
| PB | 16 | T | 666433 | 68 | 115 | 12 | 10 | 487853 | 48785.3 | jlob EvR EvR SrchR EvR SrchR EvR ax run ax |
| PB | 24 | T | 802167 | 68 | 115 | 12 | 10 | 623574 | 62357.4 | jlob EvR EvR SrchR EvR SrchR EvR ax run ax |
| PB | 32 | T | 937901 | 68 | 115 | 12 | 10 | 759321 | 75932.1 | jlob EvR EvR SrchR EvR SrchR EvR ax run ax |
| PB | 64 | T | 1480941 | 68 | 115 | 12 | 10 | 1302361 | 130236.1 | jlob EvR EvR SrchR EvR SrchR EvR ax run ax |
| Vlet | 7 | F | 126454 | 44 | 83 | 9 |  |  |  |  |
| Vlet | 8 | T | 153643 | 55 | 100 | 9 | 8 | 16051 | 2006.4 | jlob EvR EvR EvR SrchR EvR ax ax |
| Vlet | 10 | T | 153578 | 55 | 100 | 9 | 8 | 16051 | 2006.4 | jlob EvR EvR EvR SrchR EvR ax ax |
| Vlet | 12 | T | 153552 | 55 | 100 | 9 | 8 | 16051 | 2006.4 | jlob EvR EvR EvR SrchR EvR ax ax |
| Vlet | 16 | T | 153565 | 55 | 100 | 9 | 8 | 16051 | 2006.4 | jlob EvR EvR EvR SrchR EvR ax ax |
| Vlet | 24 | T | 153578 | 55 | 100 | 9 | 8 | 16051 | 2006.4 | jlob EvR EvR EvR SrchR EvR ax ax |
| Vlet | 32 | T | 153565 | 55 | 100 | 9 | 8 | 16051 | 2006.4 | jlob EvR EvR EvR SrchR EvR ax ax |
| Vlet | 64 | T | 153565 | 55 | 100 | 9 | 8 | 16051 | 2006.4 | jlob EvR EvR EvR SrchR EvR ax ax |
| Vwrap | 7 | F | 141041 | 46 | 91 | 12 |  |  |  |  |
| Vwrap | 8 | F | 173658 | 58 | 113 | 12 |  |  |  |  |
| Vwrap | 10 | T | 241674 | 85 | 158 | 12 | 10 | 25578 | 2557.8 | jlob EvR EvR EvR EvR SrchR EvR EvR ax ax |
| Vwrap | 12 | T | 241687 | 85 | 158 | 12 | 10 | 25578 | 2557.8 | jlob EvR EvR EvR EvR SrchR EvR EvR ax ax |
| Vwrap | 16 | T | 241661 | 85 | 158 | 12 | 10 | 25578 | 2557.8 | jlob EvR EvR EvR EvR SrchR EvR EvR ax ax |
| Vwrap | 24 | T | 241674 | 85 | 158 | 12 | 10 | 25578 | 2557.8 | jlob EvR EvR EvR EvR SrchR EvR EvR ax ax |
| Vwrap | 32 | T | 241661 | 85 | 158 | 12 | 10 | 25578 | 2557.8 | jlob EvR EvR EvR EvR SrchR EvR EvR ax ax |
| Vwrap | 64 | T | 241661 | 85 | 158 | 12 | 10 | 25578 | 2557.8 | jlob EvR EvR EvR EvR SrchR EvR EvR ax ax |
| FB2 | 7 | F | 120921 | 38 | 71 | 11 |  |  |  |  |
| FB2 | 8 | F | 145556 | 47 | 86 | 11 |  |  |  |  |
| FB2 | 10 | T | 196202 | 68 | 115 | 11 | 10 | 20620 | 2062.0 | jlob EvR EvR SrchR EvR SrchR EvR ax ax ax |
| FB2 | 12 | T | 196176 | 68 | 115 | 11 | 10 | 20620 | 2062.0 | jlob EvR EvR SrchR EvR SrchR EvR ax ax ax |
| FB2 | 16 | T | 196189 | 68 | 115 | 11 | 10 | 20620 | 2062.0 | jlob EvR EvR SrchR EvR SrchR EvR ax ax ax |
| FB2 | 24 | T | 196202 | 68 | 115 | 11 | 10 | 20620 | 2062.0 | jlob EvR EvR SrchR EvR SrchR EvR ax ax ax |
| FB2 | 32 | T | 196189 | 68 | 115 | 11 | 10 | 20620 | 2062.0 | jlob EvR EvR SrchR EvR SrchR EvR ax ax ax |
| FB2 | 64 | T | 196189 | 68 | 115 | 11 | 10 | 20620 | 2062.0 | jlob EvR EvR SrchR EvR SrchR EvR ax ax ax |
| SC | 7 | T | 22181 | 4 | 6 | 8 | 2 | 306 | 153.0 | jlob runneg |
| SC | 8 | T | 22285 | 4 | 6 | 8 | 2 | 306 | 153.0 | jlob runneg |
| SC | 10 | T | 22194 | 4 | 6 | 8 | 2 | 306 | 153.0 | jlob runneg |
| SC | 12 | T | 22207 | 4 | 6 | 8 | 2 | 306 | 153.0 | jlob runneg |
| SC | 16 | T | 22207 | 4 | 6 | 8 | 2 | 306 | 153.0 | jlob runneg |
| SC | 24 | T | 22220 | 4 | 6 | 8 | 2 | 306 | 153.0 | jlob runneg |
| SC | 32 | T | 22207 | 4 | 6 | 8 | 2 | 306 | 153.0 | jlob runneg |
| SC | 64 | T | 22207 | 4 | 6 | 8 | 2 | 306 | 153.0 | jlob runneg |
| G | 7 | F | 111483 | 38 | 69 | 8 |  |  |  |  |
| G | 8 | F | 133548 | 46 | 82 | 8 |  |  |  |  |
| G | 10 | F | 177418 | 62 | 108 | 8 |  |  |  |  |
| G | 12 | F | 221405 | 78 | 134 | 8 |  |  |  |  |
| G | 16 | F | 309366 | 110 | 186 | 8 |  |  |  |  |
| G | 24 | F | 485275 | 174 | 290 | 8 |  |  |  |  |
| G | 32 | F | 661158 | 238 | 394 | 8 |  |  |  |  |
| G | 64 | F | 1364742 | 494 | 810 | 8 |  |  |  |  |
| P* | 7 | F | 250852 | 65 | 108 | 15 |  |  |  |  |
| P* | 8 | F | 316339 | 83 | 136 | 15 |  |  |  |  |
| P* | 10 | TO | 2500001 |  |  |  |  |  |  |  |
| P* | 12 | TO | 2500001 |  |  |  |  |  |  |  |
| P* | 16 | TO | 2500001 |  |  |  |  |  |  |  |
| P* | 24 | TO | 2500001 |  |  |  |  |  |  |  |
| P* | 32 | TO | 2500001 |  |  |  |  |  |  |  |
| P* | 64 | TO | 2500001 |  |  |  |  |  |  |  |

## 2. Thresholds on b = 2..20 (copies and selected pairs)

Entry: first b with (C, C) for the pair (both orders), "—" if none ≤ 20.

| pair | K = 1e5 | K = 1e6 | K = 1e7 |
|---|---|---|---|
| FB–FB | — | 7 | 7 |
| FB1–FB1 | — | — | 8 |
| PB–PB | — | — | 10 |
| G–G | 2 | 2 | 2 |
| P*–P* | — | — | — |
| SC–SC | 2 | 2 | 2 |
| Vlet–Vlet | — | 8 | 8 |
| Vwrap–Vwrap | — | 10 | 10 |
| FB2–FB2 | — | 10 | 10 |
| FBx–FBx | — | 7 | 7 |
| FB–SF | — | — | 13 |
| FB–FB1 | — | — | — |
| FB–PB | — | — | — |
| FB–Vlet | — | — | — |
| FB–Vwrap | — | — | — |

## 3. Main catalogue: every (K, b)

| K | b | mutual (C, C) pairs (unordered, excluding pairs with C) | exploitation of a sound reader (reader C, other not C) | program-level searches: found / refuted / interrupted / cut |
|---|---|---|---|---|
| 1e5 | 8 | G–G, G–SF, G–SC, SC–SC | — | 14 / 0 / 118 / 0 |
| 1e5 | 12 | G–G, G–SF, G–SC, SC–SC | — | 14 / 0 / 118 / 0 |
| 1e5 | 16 | G–G, G–SF, G–SC, SC–SC | — | 14 / 0 / 118 / 0 |
| 1e5 | 24 | G–G, G–SF, G–SC, SC–SC | — | 14 / 0 / 118 / 0 |
| 1e5 | 32 | G–G, G–SF, G–SC, SC–SC | — | 14 / 0 / 118 / 0 |
| 1e5 | 64 | G–G, G–SF, G–SC, SC–SC | — | 14 / 0 / 118 / 0 |
| 1e6 | 8 | FB–FB, FB–SC, FB1–SC, G–G, G–SF, SF–SC, SC–SC, SC–Vlet, SC–Vwrap, SC–FB2, SC–FBx, Vlet–Vlet, FBx–FBx | — | 38 / 17 / 81 / 0 |
| 1e6 | 12 | FB–FB, FB–SC, FB1–SC, G–G, G–SF, SF–SC, SC–SC, SC–Vlet, SC–Vwrap, SC–FB2, SC–FBx, Vlet–Vlet, Vwrap–Vwrap, FB2–FB2, FBx–FBx | — | 39 / 8 / 89 / 0 |
| 1e6 | 16 | FB–FB, FB–SC, G–G, G–SF, SF–SC, SC–SC, SC–Vlet, SC–Vwrap, SC–FB2, SC–FBx, Vlet–Vlet, Vwrap–Vwrap, FB2–FB2, FBx–FBx | — | 38 / 7 / 91 / 0 |
| 1e6 | 24 | FB–FB, FB–SC, G–G, G–SF, SF–SC, SC–SC, SC–Vlet, SC–Vwrap, SC–FB2, SC–FBx, Vlet–Vlet, Vwrap–Vwrap, FB2–FB2, FBx–FBx | — | 38 / 0 / 98 / 0 |
| 1e6 | 32 | FB–FB, FB–SC, G–G, G–SF, SF–SC, SC–SC, SC–Vlet, SC–Vwrap, SC–FB2, SC–FBx, Vlet–Vlet, Vwrap–Vwrap, FB2–FB2, FBx–FBx | — | 38 / 0 / 98 / 0 |
| 1e6 | 64 | FB–FB, FB–SC, G–G, G–SF, SF–SC, SC–SC, SC–Vlet, SC–Vwrap, SC–FB2, SC–FBx, Vlet–Vlet, Vwrap–Vwrap, FB2–FB2, FBx–FBx | — | 38 / 0 / 98 / 0 |
| 1e7 | 8 | FB–FB, FB–SC, FB1–FB1, FB1–SC, G–G, G–SF, SF–SC, SC–SC, SC–Vlet, SC–Vwrap, SC–FB2, SC–FBx, Vlet–Vlet, FBx–FBx | — | 39 / 25 / 72 / 0 |
| 1e7 | 12 | FB–FB, FB–SC, FB1–FB1, FB1–SC, PB–PB, G–G, G–SF, SF–SC, SC–SC, SC–Vlet, SC–Vwrap, SC–FB2, SC–FBx, Vlet–Vlet, Vwrap–Vwrap, FB2–FB2, FBx–FBx | — | 44 / 21 / 73 / 0 |
| 1e7 | 16 | FB–FB, FB–SF, FB–SC, FB1–FB1, FB1–SF, FB1–SC, PB–PB, G–G, G–SF, SF–SC, SF–Vlet, SF–Vwrap, SF–FBx, SC–SC, SC–Vlet, SC–Vwrap, SC–FB2, SC–FBx, Vlet–Vlet, Vwrap–Vwrap, FB2–FB2, FBx–FBx | — | 49 / 16 / 73 / 0 |
| 1e7 | 24 | FB–FB, FB–SF, FB–SC, FB1–FB1, FB1–SF, FB1–SC, PB–PB, G–G, G–SF, SF–SC, SF–Vlet, SF–Vwrap, SF–FBx, SC–SC, SC–Vlet, SC–Vwrap, SC–FB2, SC–FBx, Vlet–Vlet, Vwrap–Vwrap, FB2–FB2, FBx–FBx | — | 49 / 16 / 73 / 0 |
| 1e7 | 32 | FB–FB, FB–SF, FB–SC, FB1–FB1, FB1–SF, FB1–SC, PB–PB, G–G, G–SF, SF–SC, SF–Vlet, SF–Vwrap, SF–FBx, SC–SC, SC–Vlet, SC–Vwrap, SC–FB2, SC–FBx, Vlet–Vlet, Vwrap–Vwrap, FB2–FB2, FBx–FBx | — | 49 / 15 / 74 / 0 |
| 1e7 | 64 | FB–FB, FB–SF, FB–SC, FB1–FB1, FB1–SF, FB1–SC, PB–PB, G–G, G–SF, SF–SC, SF–Vlet, SF–Vwrap, SF–FBx, SC–SC, SC–Vlet, SC–Vwrap, SC–FB2, SC–FBx, Vlet–Vlet, Vwrap–Vwrap, FB2–FB2, FBx–FBx | — | 49 / 10 / 79 / 0 |

Play matrix at K = 10⁷, b = 16 (row's play against column; subscript: the row's program-level searches, f found, r refuted, i interrupted by the cap, x cut by an outer counter):

| row plays vs column | C | D | FB | FB1 | PB | G | P* | SF | SC | Vlet | Vwrap | FB2 | FBx |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **C** | C | C | C | C | C | C | C | C | C | C | C | C | C |
| **D** | D | D | D | D | D | D | D | D | D | D | D | D | D |
| **FB** | C<sub>f</sub> | D<sub>r</sub> | C<sub>f</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | C<sub>f</sub> | C<sub>f</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> |
| **FB1** | C<sub>f</sub> | D<sub>r</sub> | D<sub>i</sub> | C<sub>f</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | C<sub>f</sub> | C<sub>f</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> |
| **PB** | D<sub>fr</sub> | D<sub>r</sub> | D<sub>i</sub> | D<sub>i</sub> | C<sub>ff</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>r</sub> | D<sub>fr</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> |
| **G** | D<sub>f</sub> | C<sub>r</sub> | C<sub>i</sub> | C<sub>i</sub> | C<sub>i</sub> | C<sub>r</sub> | C<sub>i</sub> | C<sub>r</sub> | D<sub>f</sub> | C<sub>i</sub> | C<sub>i</sub> | C<sub>i</sub> | C<sub>i</sub> |
| **P*** | D<sub>ff</sub> | D<sub>r</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>r</sub> | D<sub>ff</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> |
| **SF** | C | D | C | C | D | C | D | D | C | C | C | D | C |
| **SC** | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> |
| **Vlet** | C<sub>f</sub> | D<sub>r</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> |
| **Vwrap** | C<sub>f</sub> | D<sub>r</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | C<sub>f</sub> | C<sub>f</sub> | D<sub>i</sub> | C<sub>f</sub> | D<sub>i</sub> | D<sub>i</sub> |
| **FB2** | C<sub>ff</sub> | D<sub>r</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>r</sub> | C<sub>ff</sub> | D<sub>i</sub> | D<sub>i</sub> | C<sub>ff</sub> | D<sub>i</sub> |
| **FBx** | C<sub>f</sub> | D<sub>r</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | C<sub>f</sub> | C<sub>f</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | C<sub>f</sub> |

Play matrix at K = 10⁷, b = 8:

| row plays vs column | C | D | FB | FB1 | PB | G | P* | SF | SC | Vlet | Vwrap | FB2 | FBx |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **C** | C | C | C | C | C | C | C | C | C | C | C | C | C |
| **D** | D | D | D | D | D | D | D | D | D | D | D | D | D |
| **FB** | C<sub>f</sub> | D<sub>r</sub> | C<sub>f</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>r</sub> | C<sub>f</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> |
| **FB1** | C<sub>f</sub> | D<sub>r</sub> | D<sub>i</sub> | C<sub>f</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>r</sub> | C<sub>f</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> |
| **PB** | D<sub>fr</sub> | D<sub>r</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>r</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>r</sub> | D<sub>fr</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> |
| **G** | D<sub>f</sub> | C<sub>r</sub> | C<sub>i</sub> | C<sub>i</sub> | C<sub>i</sub> | C<sub>r</sub> | C<sub>i</sub> | C<sub>r</sub> | D<sub>f</sub> | C<sub>i</sub> | C<sub>i</sub> | C<sub>i</sub> | C<sub>i</sub> |
| **P*** | D<sub>ff</sub> | D<sub>r</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>r</sub> | D<sub>r</sub> | D<sub>ff</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> |
| **SF** | C | D | D | D | D | C | D | D | C | D | D | D | D |
| **SC** | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> |
| **Vlet** | C<sub>f</sub> | D<sub>r</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>r</sub> | C<sub>f</sub> | C<sub>f</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> |
| **Vwrap** | C<sub>f</sub> | D<sub>r</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>r</sub> | C<sub>f</sub> | D<sub>i</sub> | D<sub>r</sub> | D<sub>i</sub> | D<sub>i</sub> |
| **FB2** | C<sub>ff</sub> | D<sub>r</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>r</sub> | C<sub>ff</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>r</sub> | D<sub>i</sub> |
| **FBx** | C<sub>f</sub> | D<sub>r</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>r</sub> | C<sub>f</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | C<sub>f</sub> |

Finite-K plateau (smallest tested K from which an ordered cell is constant at every larger tested K; a plateau, not stabilization): 1e5: 839, 1e6: 120, 1e7: 55

Coverage of program-level searches by searching program (all K, b):

| program | found | refuted | interrupted | cut |
|---|---|---|---|---|
| FB | 46 | 12 | 176 | 0 |
| FB1 | 30 | 7 | 197 | 0 |
| PB | 40 | 27 | 202 | 0 |
| G | 30 | 23 | 181 | 0 |
| P* | 38 | 10 | 205 | 0 |
| SC | 192 | 0 | 42 | 0 |
| Vlet | 46 | 12 | 176 | 0 |
| Vwrap | 44 | 14 | 176 | 0 |
| FB2 | 80 | 18 | 176 | 0 |
| FBx | 46 | 12 | 176 | 0 |

Coverage by (K, b):

| K | b | found | refuted | interrupted | cut |
|---|---|---|---|---|---|
| 1e5 | 8 | 14 | 0 | 118 | 0 |
| 1e5 | 12 | 14 | 0 | 118 | 0 |
| 1e5 | 16 | 14 | 0 | 118 | 0 |
| 1e5 | 24 | 14 | 0 | 118 | 0 |
| 1e5 | 32 | 14 | 0 | 118 | 0 |
| 1e5 | 64 | 14 | 0 | 118 | 0 |
| 1e6 | 8 | 38 | 17 | 81 | 0 |
| 1e6 | 12 | 39 | 8 | 89 | 0 |
| 1e6 | 16 | 38 | 7 | 91 | 0 |
| 1e6 | 24 | 38 | 0 | 98 | 0 |
| 1e6 | 32 | 38 | 0 | 98 | 0 |
| 1e6 | 64 | 38 | 0 | 98 | 0 |
| 1e7 | 8 | 39 | 25 | 72 | 0 |
| 1e7 | 12 | 44 | 21 | 73 | 0 |
| 1e7 | 16 | 49 | 16 | 73 | 0 |
| 1e7 | 24 | 49 | 16 | 73 | 0 |
| 1e7 | 32 | 49 | 15 | 74 | 0 |
| 1e7 | 64 | 49 | 10 | 79 | 0 |

## 3b. JLöb-disabled control (CORE_2): every (K, b)

| K | b | mutual (C, C) pairs (unordered, excluding pairs with C) | exploitation of a sound reader (reader C, other not C) | program-level searches: found / refuted / interrupted / cut |
|---|---|---|---|---|
| 1e5 | 8 | G–G, G–SF, G–SC, SC–SC | — | 14 / 0 / 118 / 0 |
| 1e5 | 12 | G–G, G–SF, G–SC, SC–SC | — | 14 / 0 / 118 / 0 |
| 1e5 | 16 | G–G, G–SF, G–SC, SC–SC | — | 14 / 0 / 118 / 0 |
| 1e5 | 24 | G–G, G–SF, G–SC, SC–SC | — | 14 / 0 / 118 / 0 |
| 1e5 | 32 | G–G, G–SF, G–SC, SC–SC | — | 14 / 0 / 118 / 0 |
| 1e5 | 64 | G–G, G–SF, G–SC, SC–SC | — | 14 / 0 / 118 / 0 |
| 1e6 | 8 | FB–SC, FB1–SC, G–G, G–SF, SF–SC, SC–SC, SC–Vlet, SC–Vwrap, SC–FB2, SC–FBx | — | 35 / 28 / 73 / 0 |
| 1e6 | 12 | FB–SC, FB1–SC, G–G, G–SF, SF–SC, SC–SC, SC–Vlet, SC–Vwrap, SC–FB2, SC–FBx | — | 35 / 23 / 78 / 0 |
| 1e6 | 16 | FB–SC, FB1–SC, G–G, G–SF, SF–SC, SC–SC, SC–Vlet, SC–Vwrap, SC–FB2, SC–FBx | — | 35 / 15 / 86 / 0 |
| 1e6 | 24 | FB–SC, FB1–SC, G–G, G–SF, SF–SC, SC–SC, SC–Vlet, SC–Vwrap, SC–FB2, SC–FBx | — | 35 / 7 / 94 / 0 |
| 1e6 | 32 | FB–SC, FB1–SC, G–G, G–SF, SF–SC, SC–SC, SC–Vlet, SC–Vwrap, SC–FB2, SC–FBx | — | 35 / 7 / 94 / 0 |
| 1e6 | 64 | FB–SC, G–G, G–SF, SF–SC, SC–SC, SC–Vlet, SC–Vwrap, SC–FB2, SC–FBx | — | 32 / 0 / 103 / 0 |
| 1e7 | 8 | FB–SC, FB1–SC, G–G, G–SF, SF–SC, SC–SC, SC–Vlet, SC–Vwrap, SC–FB2, SC–FBx | — | 35 / 29 / 72 / 0 |
| 1e7 | 12 | FB–SC, FB1–SC, G–G, G–SF, SF–SC, SC–SC, SC–Vlet, SC–Vwrap, SC–FB2, SC–FBx | — | 35 / 28 / 73 / 0 |
| 1e7 | 16 | FB–SC, FB1–SC, G–G, G–SF, SF–SC, SC–SC, SC–Vlet, SC–Vwrap, SC–FB2, SC–FBx | — | 35 / 28 / 73 / 0 |
| 1e7 | 24 | FB–SC, FB1–SC, G–G, G–SF, SF–SC, SC–SC, SC–Vlet, SC–Vwrap, SC–FB2, SC–FBx | — | 35 / 28 / 73 / 0 |
| 1e7 | 32 | FB–SC, FB1–SC, G–G, G–SF, SF–SC, SC–SC, SC–Vlet, SC–Vwrap, SC–FB2, SC–FBx | — | 35 / 28 / 73 / 0 |
| 1e7 | 64 | FB–SC, FB1–SC, G–G, G–SF, SF–SC, SC–SC, SC–Vlet, SC–Vwrap, SC–FB2, SC–FBx | — | 35 / 26 / 75 / 0 |

Play matrix at K = 10⁷, b = 16 (row's play against column; subscript: the row's program-level searches, f found, r refuted, i interrupted by the cap, x cut by an outer counter):

| row plays vs column | C | D | FB | FB1 | PB | G | P* | SF | SC | Vlet | Vwrap | FB2 | FBx |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **C** | C | C | C | C | C | C | C | C | C | C | C | C | C |
| **D** | D | D | D | D | D | D | D | D | D | D | D | D | D |
| **FB** | C<sub>f</sub> | D<sub>r</sub> | D<sub>r</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>r</sub> | C<sub>f</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> |
| **FB1** | C<sub>f</sub> | D<sub>r</sub> | D<sub>i</sub> | D<sub>r</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>r</sub> | C<sub>f</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> |
| **PB** | D<sub>fr</sub> | D<sub>r</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>r</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>r</sub> | D<sub>fr</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> |
| **G** | D<sub>f</sub> | C<sub>r</sub> | C<sub>i</sub> | C<sub>i</sub> | C<sub>i</sub> | C<sub>r</sub> | C<sub>i</sub> | C<sub>r</sub> | D<sub>f</sub> | C<sub>i</sub> | C<sub>i</sub> | C<sub>i</sub> | C<sub>i</sub> |
| **P*** | D<sub>ff</sub> | D<sub>r</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>r</sub> | D<sub>ff</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> |
| **SF** | C | D | D | D | D | C | D | D | C | D | D | D | D |
| **SC** | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> | C<sub>f</sub> |
| **Vlet** | C<sub>f</sub> | D<sub>r</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>r</sub> | C<sub>f</sub> | D<sub>r</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> |
| **Vwrap** | C<sub>f</sub> | D<sub>r</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>r</sub> | C<sub>f</sub> | D<sub>i</sub> | D<sub>r</sub> | D<sub>i</sub> | D<sub>i</sub> |
| **FB2** | C<sub>ff</sub> | D<sub>r</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>r</sub> | C<sub>ff</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>r</sub> | D<sub>i</sub> |
| **FBx** | C<sub>f</sub> | D<sub>r</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>r</sub> | C<sub>f</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>i</sub> | D<sub>r</sub> |

Finite-K plateau (smallest tested K from which an ordered cell is constant at every larger tested K; a plateau, not stabilization): 1e5: 918, 1e6: 95, 1e7: 1

Coverage of program-level searches by searching program (all K, b):

| program | found | refuted | interrupted | cut |
|---|---|---|---|---|
| FB | 30 | 28 | 176 | 0 |
| FB1 | 23 | 21 | 190 | 0 |
| PB | 30 | 41 | 193 | 0 |
| G | 30 | 28 | 176 | 0 |
| P* | 46 | 16 | 195 | 0 |
| SC | 192 | 0 | 42 | 0 |
| Vlet | 30 | 28 | 176 | 0 |
| Vwrap | 30 | 28 | 176 | 0 |
| FB2 | 60 | 29 | 175 | 0 |
| FBx | 30 | 28 | 176 | 0 |

Coverage by (K, b):

| K | b | found | refuted | interrupted | cut |
|---|---|---|---|---|---|
| 1e5 | 8 | 14 | 0 | 118 | 0 |
| 1e5 | 12 | 14 | 0 | 118 | 0 |
| 1e5 | 16 | 14 | 0 | 118 | 0 |
| 1e5 | 24 | 14 | 0 | 118 | 0 |
| 1e5 | 32 | 14 | 0 | 118 | 0 |
| 1e5 | 64 | 14 | 0 | 118 | 0 |
| 1e6 | 8 | 35 | 28 | 73 | 0 |
| 1e6 | 12 | 35 | 23 | 78 | 0 |
| 1e6 | 16 | 35 | 15 | 86 | 0 |
| 1e6 | 24 | 35 | 7 | 94 | 0 |
| 1e6 | 32 | 35 | 7 | 94 | 0 |
| 1e6 | 64 | 32 | 0 | 103 | 0 |
| 1e7 | 8 | 35 | 29 | 72 | 0 |
| 1e7 | 12 | 35 | 28 | 73 | 0 |
| 1e7 | 16 | 35 | 28 | 73 | 0 |
| 1e7 | 24 | 35 | 28 | 73 | 0 |
| 1e7 | 32 | 35 | 28 | 73 | 0 |
| 1e7 | 64 | 35 | 26 | 75 | 0 |

## 4. FairBot distinct-budget grid {8, 12, 16, 32}² (row's play / column's play, row's search outcome)


K = 1e5:

| b_row \ b_col | 8 | 12 | 16 | 32 |
|---|---|---|---|---|
| 8 | D/D i | D/D i | D/D i | D/D i |
| 12 | D/D i | D/D i | D/D i | D/D i |
| 16 | D/D i | D/D i | D/D i | D/D i |
| 32 | D/D i | D/D i | D/D i | D/D i |

K = 1e6:

| b_row \ b_col | 8 | 12 | 16 | 32 |
|---|---|---|---|---|
| 8 | C/C f | D/D i | D/D i | D/D i |
| 12 | D/D i | C/C f | D/D i | D/D i |
| 16 | D/D i | D/D i | C/C f | D/D i |
| 32 | D/D i | D/D i | D/D i | C/C f |

K = 1e7:

| b_row \ b_col | 8 | 12 | 16 | 32 |
|---|---|---|---|---|
| 8 | C/C f | D/D i | D/D i | D/D i |
| 12 | D/D i | C/C f | D/D i | D/D i |
| 16 | D/D i | D/D i | C/C f | D/D i |
| 32 | D/D i | D/D i | D/D i | C/C f |

Asymmetric grid cells with both searches finished: 0 []

## 5. Leak cells: SF_k against every reader

Entry per (K, b, k): readers with (reader play / SF play); "matched" = the reader's certified target names the fuel SF ran with. Exploitation = reader C, SF not C.

| K | b | k | reader/SF plays | matched exploited | mismatched exploited |
|---|---|---|---|---|---|
| 1e5 | 8 | 1000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC D/D | G | — |
| 1e5 | 8 | 10000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC D/D | G | — |
| 1e5 | 8 | U+8 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC D/D | G | — |
| 1e5 | 8 | U+9 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC D/D | G | — |
| 1e5 | 8 | U+10 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC D/D | — | — |
| 1e5 | 8 | U+11 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC D/D | — | — |
| 1e5 | 8 | 100000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC D/D | — | — |
| 1e5 | 8 | 1000000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC D/D | — | — |
| 1e5 | 12 | 1000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC D/D | G | — |
| 1e5 | 12 | 10000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC D/D | G | — |
| 1e5 | 12 | U+8 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC D/D | G | — |
| 1e5 | 12 | U+9 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC D/D | G | — |
| 1e5 | 12 | U+10 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC D/D | — | — |
| 1e5 | 12 | U+11 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC D/D | — | — |
| 1e5 | 12 | 100000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC D/D | — | — |
| 1e5 | 12 | 1000000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC D/D | — | — |
| 1e5 | 16 | 1000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC D/D | G | — |
| 1e5 | 16 | 10000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC D/D | G | — |
| 1e5 | 16 | U+8 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC D/D | G | — |
| 1e5 | 16 | U+9 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC D/D | G | — |
| 1e5 | 16 | U+10 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC D/D | — | — |
| 1e5 | 16 | U+11 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC D/D | — | — |
| 1e5 | 16 | 100000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC D/D | — | — |
| 1e5 | 16 | 1000000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC D/D | — | — |
| 1e5 | 24 | 1000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC D/D | G | — |
| 1e5 | 24 | 10000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC D/D | G | — |
| 1e5 | 24 | U+8 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC D/D | G | — |
| 1e5 | 24 | U+9 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC D/D | G | — |
| 1e5 | 24 | U+10 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC D/D | — | — |
| 1e5 | 24 | U+11 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC D/D | — | — |
| 1e5 | 24 | 100000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC D/D | — | — |
| 1e5 | 24 | 1000000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC D/D | — | — |
| 1e5 | 32 | 1000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC D/D | G | — |
| 1e5 | 32 | 10000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC D/D | G | — |
| 1e5 | 32 | U+8 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC D/D | G | — |
| 1e5 | 32 | U+9 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC D/D | G | — |
| 1e5 | 32 | U+10 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC D/D | — | — |
| 1e5 | 32 | U+11 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC D/D | — | — |
| 1e5 | 32 | 100000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC D/D | — | — |
| 1e5 | 32 | 1000000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC D/D | — | — |
| 1e5 | 64 | 1000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC D/D | G | — |
| 1e5 | 64 | 10000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC D/D | G | — |
| 1e5 | 64 | U+8 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC D/D | G | — |
| 1e5 | 64 | U+9 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC D/D | G | — |
| 1e5 | 64 | U+10 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC D/D | — | — |
| 1e5 | 64 | U+11 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC D/D | — | — |
| 1e5 | 64 | 100000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC D/D | — | — |
| 1e5 | 64 | 1000000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC D/D | — | — |
| 1e6 | 8 | 1000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/D | G, SC | — |
| 1e6 | 8 | 10000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/D | G, SC | — |
| 1e6 | 8 | 100000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/C | G | — |
| 1e6 | 8 | U+8 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e6 | 8 | U+9 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e6 | 8 | U+10 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e6 | 8 | U+11 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e6 | 8 | 1000000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e6 | 12 | 1000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/D | G, SC | — |
| 1e6 | 12 | 10000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/D | G, SC | — |
| 1e6 | 12 | 100000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/C | G | — |
| 1e6 | 12 | U+8 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/C | G | — |
| 1e6 | 12 | U+9 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/C | G | — |
| 1e6 | 12 | U+10 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e6 | 12 | U+11 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e6 | 12 | 1000000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e6 | 16 | 1000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/D | G, SC | — |
| 1e6 | 16 | 10000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/D | G, SC | — |
| 1e6 | 16 | 100000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/C | G | — |
| 1e6 | 16 | U+8 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/C | G | — |
| 1e6 | 16 | U+9 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/C | G | — |
| 1e6 | 16 | U+10 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e6 | 16 | U+11 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e6 | 16 | 1000000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e6 | 24 | 1000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/D | G, SC | — |
| 1e6 | 24 | 10000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/D | G, SC | — |
| 1e6 | 24 | 100000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/C | G | — |
| 1e6 | 24 | U+8 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/C | G | — |
| 1e6 | 24 | U+9 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/C | G | — |
| 1e6 | 24 | U+10 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e6 | 24 | U+11 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e6 | 24 | 1000000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e6 | 32 | 1000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/D | G, SC | — |
| 1e6 | 32 | 10000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/D | G, SC | — |
| 1e6 | 32 | 100000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/C | G | — |
| 1e6 | 32 | U+8 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/C | G | — |
| 1e6 | 32 | U+9 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/C | G | — |
| 1e6 | 32 | U+10 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e6 | 32 | U+11 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e6 | 32 | 1000000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e6 | 64 | 1000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/D | G, SC | — |
| 1e6 | 64 | 10000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/D | G, SC | — |
| 1e6 | 64 | 100000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/C | G | — |
| 1e6 | 64 | U+8 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/C | G | — |
| 1e6 | 64 | U+9 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/C | G | — |
| 1e6 | 64 | U+10 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e6 | 64 | U+11 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e6 | 64 | 1000000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 8 | 1000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/D | G, SC | — |
| 1e7 | 8 | 10000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/D | G, SC | — |
| 1e7 | 8 | 100000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/C | G | — |
| 1e7 | 8 | 1000000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 8 | U+8 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 8 | U+9 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 8 | U+10 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 8 | U+11 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 12 | 1000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/D | G, SC | — |
| 1e7 | 12 | 10000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/D | G, SC | — |
| 1e7 | 12 | 100000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/C | G | — |
| 1e7 | 12 | 1000000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 12 | U+8 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 12 | U+9 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 12 | U+10 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 12 | U+11 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 16 | 1000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/D | G, SC | — |
| 1e7 | 16 | 10000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/D | G, SC | — |
| 1e7 | 16 | 100000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/C | G | — |
| 1e7 | 16 | 1000000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 16 | U+8 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 16 | U+9 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 16 | U+10 | FB C/C, FB1 C/C, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx C/C, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 16 | U+11 | FB C/C, FB1 C/C, PB D/D, Vlet C/C, Vwrap D/D, FB2 D/D, FBx C/C, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 24 | 1000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/D | G, SC | — |
| 1e7 | 24 | 10000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/D | G, SC | — |
| 1e7 | 24 | 100000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/C | G | — |
| 1e7 | 24 | 1000000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 24 | U+8 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 24 | U+9 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 24 | U+10 | FB C/C, FB1 C/C, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx C/C, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 24 | U+11 | FB C/C, FB1 C/C, PB D/D, Vlet C/C, Vwrap D/D, FB2 D/D, FBx C/C, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 32 | 1000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/D | G, SC | — |
| 1e7 | 32 | 10000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/D | G, SC | — |
| 1e7 | 32 | 100000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/C | G | — |
| 1e7 | 32 | 1000000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 32 | U+8 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 32 | U+9 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 32 | U+10 | FB C/C, FB1 C/C, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx C/C, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 32 | U+11 | FB C/C, FB1 C/C, PB D/D, Vlet C/C, Vwrap D/D, FB2 D/D, FBx C/C, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 64 | 1000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/D | G, SC | — |
| 1e7 | 64 | 10000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/D | G, SC | — |
| 1e7 | 64 | 100000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/C | G | — |
| 1e7 | 64 | 1000000 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/D, P* D/D, SC C/C | G | — |
| 1e7 | 64 | U+8 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 64 | U+9 | FB D/D, FB1 D/D, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx D/D, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 64 | U+10 | FB C/C, FB1 C/C, PB D/D, Vlet D/D, Vwrap D/D, FB2 D/D, FBx C/C, G C/C, P* D/D, SC C/C | — | — |
| 1e7 | 64 | U+11 | FB C/C, FB1 C/C, PB D/D, Vlet C/C, Vwrap D/D, FB2 D/D, FBx C/C, G C/C, P* D/D, SC C/C | — | — |

Totals: certified_C_matched 20, certified_C_mismatched 8, exploit_G_suckered_matched 71, exploit_SC_sloppy_matched 24, matched 1296, matched_reader_C 260, mismatched 144, mismatched_reader_C 8

## 7. Fuel-boundary cells

- **FB7 self, named K0=1e6**: {"need": 111900, "play_at_need": "C", "K=need-1": "BOT", "K=need+0": "C", "K=need+1": "C"}
- **FB8 self, named K0=1e6**: {"need": 111913, "play_at_need": "C", "K=need-1": "BOT", "K=need+0": "C", "K=need+1": "C"}
- **FB16 self, named K0=1e6**: {"need": 111900, "play_at_need": "C", "K=need-1": "BOT", "K=need+0": "C", "K=need+1": "C"}
- **K=1e7 FB16 vs SF k=U+7**: {"reader": "D", "sf": "D"}
- **K=1e7 FB16 vs SF k=U+8**: {"reader": "D", "sf": "D"}
- **K=1e7 FB16 vs SF k=U+9**: {"reader": "D", "sf": "D"}
- **K=1e7 FB16 vs SF k=U+10**: {"reader": "C", "sf": "C"}
- **K=1e7 FB16 vs SF k=U+11**: {"reader": "C", "sf": "C"}
- **K=1e7 FB16 vs SF k=U+12**: {"reader": "C", "sf": "C"}
- **SF inner completion k***: {"k_star": 425230, "value_at_k_star": "D", "U": 2500000, "static_boundary_hand": 2500010}
- **visibility FB2 b=10**: {"FB2_self": "C", "FB2_steps": 392420, "FB_self": "C", "FB_steps": 111913}
- **visibility FB2 b=16**: {"FB2_self": "C", "FB2_steps": 392394, "FB_self": "C", "FB_steps": 111939}

## 8. Correctness harness (every core query of every task)

check_term_ok 1164, finishing 2007, found 1164, found_checked 1164, interrupted 4347, outcome_agree 2007, queries 6354, refuted 843, replay_nodes 4727, replay_ok 1164, same_tree 1164, work_agree 2007

Mismatches: 0

## 9. Verdicts

| # | prediction | outcome |
|---|---|---|
| RE 1 | term prover correct on every finishing query; feasibility set by candidate count; checking FB's proof ≤ 10⁴; FB's self-search finishes within 10⁷ | **held** (falsifier not fired): 2,007/2,007 finishing queries agree with the host oracle in outcome and in expansions and rule instances; 1,164/1,164 found boxes replay, give the host's tree, and are accepted by the checker term; all corrupted instances rejected; FB's self-search costs 1.12·10⁵ steps (finishes from K = 10⁶). The "≤ 10⁴" guess for checking failed narrowly (12,174 steps). |
| RE 2 | no matched-target cell with a sound reader on C and SF not cooperating; mismatched cells reported separately, predicted impossible | **held** on the catalogue: 20 matched and 8 mismatched cells with a certified C, 0 exploited. Exploited cells exist only for G (71, suckered by non-finding) and SC_code (24, cooperates with everything); neither is certified. "Impossible by construction" for mismatched targets is not established (notes §1.7: possible when the target's run length falls in (K, K′] and the certificate passes over it with search calls); none in this catalogue. |
| RE 3 | Löb certifies a copy's run without unfolding; simulations need unfolding (SF-type targets obey a fuel bound, prover-type do not); grid symmetric | **falsifier not fired** (0 asymmetric grid cells with finished searches), **dichotomy wrong**: copies are certified by JLöb^self without unfolding; SF is certified without unfolding its inner search (SrchR + JLöb^self, FB–SF (C, C) from b = 13 at K = 10⁷, k ≥ U + 10); both kinds obey the same static cap condition. The grid's cooperative region is the diagonal: no distinct budgets cooperate. |
| RE 4 | soundness with the obligations discharged; bounded Gödel II transfers (P\* never self-cooperates) | **failed, falsifier fired** (by the notes, before the run): Nec, BoxEq (ii)/(iii), budget monotonicity and joint JLöb have obligations that cannot be discharged for search-run boxes and were removed. What remains is sound (0 violations: 1,164 replays), and P\* never self-cooperates, but by the Run regress (interrupted from b = 10), not by a Gödel argument. |
| RE 5 | SC_code a faker of G, not of sound readers; FB–SC_code can be (C, C) | **held**: G defects on SC_code, which cooperates (every K ≥ 10⁶, every b); FB, FB1, Vlet, Vwrap, FB2, FBx and SC_code are (C, C); no sound reader is exploited by SC_code. PB defects on SC_code (it certifies that SC_code cooperates with D). |
| S1 | b\* = 7 (FB), 8 (FB1, Vlet), 10 (PB, Vwrap, FB2), one JLöb^self each; G, P\* never; SC_code from b = 6 | **failed on the SC clause** (SC_code finds from b = 2: JLöb with an unchecked RunNeg on its own hypothesis); every other threshold exact, one JLöb^self each. |
| S2 | twins only: no distinct sound sources cooperate; each such pair has an interrupted search; grid diagonal | **held** (every distinct-source pair interrupted by the regress; grid diagonal at 10⁶ and 10⁷). |
| S3 | FB self-search 10⁵–3·10⁶ steps; checking 2·10³–3·10⁴; ≤ 5,000 instances | **held** (111,930; 12,174; 70). |
| S4 | FB self-cooperates at 10⁶ and 10⁷, not 10⁵ | **held**. |
| S5 | FB vs SF_k flips exactly at k = U + 9, not at the inner search's completion point | **failed, falsifier fired** (the flip is at U + 10: the minimal-residual reading needs one more sim step after the search); the mechanism held: the flip is at the static boundary, while SF's simulation actually completes from k\* = 425,230 (with value D, since the identical inner search cannot certify either). |
| S6 | PB from b = 10 where it fits; PB–D (D, D); G–G (C, C); P\* never; SF–SF (D, D) | **held** (PB at K = 10⁷ only; at 10⁶ its nested Run does not fit). |
| S7 | control: no twin, simulator or distinct-source cooperation; only C, G, SC_code remain | **held**. |
| S8 | term = host on outcome, size and expansions on every finishing query; replay; corrupted rejected | **held** (0 mismatches). |
| S9 | no mismatched leak in the catalogue | **held** (8 certified mismatched cells, 0 exploited). |
| S10 | SC_code exploited by G; FB, FB1, Vlet, PB, SC_code (C, C); SC_code defects against D | **failed, falsifier fired**: SC_code cooperates with D (it proves everything), and PB defects on it. |
