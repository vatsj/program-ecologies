# Implementation Handoff

Companion to THEORY.md, which defines the model. This file says what to build, in what order, and how to know it's right. Read THEORY.md §2 (extensionality), §5 (dynamics), and §7 (predictions) first.

---

## 0. Plan

Five phases. Each ends with a check that must pass before the next starts.

| Phase | Deliverable | Check |
|---|---|---|
| **0. Language** | Enumerator producing the tape; slow recursive reference evaluator | Hand-verify a dozen programs at $n\le 3$: `C`, `D`, `X`, `or(X, THEM(ME))` vs itself → cooperation prob 1; pure `THEM(ME)` vs itself → non-convergent → minimax; match-vs-swap → non-convergent |
| **1. Evaluator** | Batched value-iteration evaluator; program×program matrix | Exact agreement with reference at $n\le 4$ on all pairs; strong-arm $n=6$ matrix in seconds |
| **2. Chain** | Attractor discovery, selection dynamics, stationary distribution; PD strong arm | Predictions (a) and (b) in THEORY.md §7: no stable cooperation at $n=5$; bistable switching at $n=6$ |
| **3. Weak arm** | Program×attractor incremental evaluation to $n=9$; PD and Stag Hunt | Prediction (c): PrudentBot appears at $n=9$ and collapses the FairBot–ALLC edge. Stag Hunt under both protocols |
| **4. Source arm + sweep** | `eq` arm; full sweep; report generator | Prediction (d): `eq(THEM,ME)` wins. Support+transition reports for every cell |
| **5. Test games** | Chicken (with `ROLE`), divide-the-dollar, zero-sum, Nash demand, exchange game, a `ROLE`-symmetrized asymmetric game | Verdicts written to `predictions/` and committed *before* each first run |

Don't skip Phase 0. The batched evaluator has enough index arithmetic that you want an oracle, and the reference evaluator is also the divergence-detector's ground truth.

## 1. The DSL

```
A ::= C | D | X | not A | and A A | or A A | P P | eq P P
P ::= ME | THEM | ↑A
```

Action labels `C`/`D` are game-relative: they are the two base-game actions in the order given by the game config. For Stag Hunt they read Stag/Hare. Everything else is game-independent.

**Semantics, in evaluation order:**

- `C`, `D`: constant actions. `X`: independent fair coin per evaluation, i.e. cooperation probability ½.
- `not A`: swap. In probability terms, $1 - v$.
- `and A B`: **short-circuit left-to-right.** Evaluate `A`; if it is `D`, return `D` without evaluating `B`. Probability: $v_A \cdot v_B$.
- `or A B`: short-circuit. Evaluate `A`; if `C`, return `C` without evaluating `B`. Probability: $1 - (1-v_A)(1-v_B)$.
- `P Q` (application): run program `P` with `Q` as its opponent. `THEM(ME)` = what the opponent plays against me. `THEM(↑D)` = what the opponent plays against always-defect. `THEM(THEM)` = what the opponent plays against itself. `ME(...)` = run my own program against something. `↑A` applied to anything ignores its argument and evaluates `A` — but `A` may itself contain `THEM`/`ME`, resolved with `ME = ↑A` and `THEM =` the argument.
- `eq P Q`: syntactic equality of source strings. `C` if equal, else `D`. Source-arm only.
- `ME`: quotation — the program's own source. `THEM`: the opponent's source. Both are program-sort leaves.

Short-circuiting is not an optimization; it is what makes recursion terminate. `or(X, THEM(ME))` against itself stops with probability ½ per level. `or(THEM(ME), X)` never stops. `and`/`or` are therefore **non-commutative** and must not be canonicalized by argument order.

**`ROLE`** (asymmetric games and Chicken only): an additional A-sort atom returning `C` for one player and `D` for the other, drawn once per match, opposite for the two players. Inert in PD; ~3.75× enumeration cost. Omit unless the game config requests it.

**Arms as grammar restrictions.**

| Arm | Allowed $P\,P$ forms | `eq` | Role |
|---|---|---|---|
| strong | `THEM(ME)` only | no | baseline |
| weak | any | no | **canonical** |
| source | any | yes | contrast |

## 2. Enumeration

Enumerate bottom-up by **node count** (each constructor is one node, including `↑`). Keep a hash-cons table `(op, lhs, rhs) → row` so structurally identical subterms are one row. This is identity dedup only, which is exactly right in the source arm; behavioral dedup is done later, per §4.

Sizes with the full grammar, no `ROLE`: $|S_6|\approx 2{,}800$, $|S_7|\approx 14{,}800$, $|S_8|\approx 74{,}600$, $|S_9|\approx 404{,}000$; growth ~5.5×/level. The strong arm is dozens of programs at any depth.

**Strip at enumeration:** `ME(...)` in applied position (direct self-application; diverges without grounding — legal but never useful), and any `↑A` applied to an argument (`(↑A)(P) ≡ A` for the body; keep the P-sort `↑A` itself, since it's a valid program).

**Bits, not nodes.** The mutation prior is $2^{-\text{bits}}$ under an optimal code. Compute bits per node as $\log_2$ of the empirical growth rate (~2.5), or use an arithmetic code over the grammar's actual branching. Node count is *not* an acceptable proxy — $2^{-\text{nodes}}$ is improper for this grammar.

## 3. Evaluation

**Goal:** $V[p][q]$ = probability program $p$ plays `C` against $q$, exactly, with $T\to\infty$.

**Representation: flat tape, not objects.** Rows are `(program, subterm)` pairs — not unique subterms — because `ME` resolves to the *enclosing* program and the same subterm inside two programs evaluates differently. Arrays: `op`, `lhs`, `rhs`, `size`, `owner` (which program this row belongs to). Rows topologically ordered by size so children precede parents. ~31K rows at $n=6$.

**Value iteration over budget.** $V_0 = $ minimax action everywhere (the base case: out of budget → forced minimax). $V_{b+1}$ is computed from $V_b$ by one pass over the tape:

```
V = full(minimax)                         # shape (S, S)
for b in range(B_max):
    W = empty((rows, S))                  # value of each row vs each opponent
    for sz in 1..n:                       # sizes ascending; children done
        r = rows_of_size[sz]
        W[const_rows(r)] = 0 or 1
        W[X_rows(r)]     = 0.5
        W[not_rows(r)]   = 1 - W[lhs]
        W[and_rows(r)]   = W[lhs] * W[rhs]
        W[or_rows(r)]    = 1 - (1-W[lhs]) * (1-W[rhs])
        W[app_rows(r)]   = V[row_idx, col_idx]     # reads previous budget
        W[eq_rows(r)]    = EQ[...]                 # precomputed boolean
    V_new = W[body_row_of[program]]
    if converged(V_new, V): break
    V = V_new
```

Batch per `(size, op)`: gather children indices, one vectorized op. ~36 numpy calls per budget level. Do **not** write the recursive version as the fast path.

**Application indexing.** For a row owned by program $i$, evaluated against opponent $j$:

| form | reads |
|---|---|
| `THEM(ME)` | `V[j][i]` |
| `ME(THEM)` | `V[i][j]` |
| `THEM(THEM)` | `V[j][j]` |
| `ME(ME)` | `V[i][i]` |
| `THEM(↑A)` | `V[j][lift(A)]` |
| `ME(↑A)` | `V[i][lift(A)]` |
| `(↑A)(P)` | stripped at enumeration |

`lift(A)` is the row index of the P-sort program `↑A`, which is a genuine program with its own matrix row.

**Convergence and divergence.** Iterate until $\|V_{b+1} - V_b\|_\infty < \text{tol}$ or $b = B_{\max}$. Grounded pairs converge geometrically; $B_{\max}=128$ is far past machine precision for grounding rate ¼. Pairs that have not converged at $B_{\max}$ are **divergent**: assign the minimax action and record them. Pure `THEM(ME)` against itself sits at $V_0$ forever (it reads its own base case), which is minimax already; match-vs-swap cycles with period 4. Report the divergence rate per arm.

**Runtime accumulators are optional.** With $T\to\infty$ there is no override, so only $P(\text{C})$ is needed. If you want $E[t]$ for diagnostics, add it as a second accumulator propagated linearly (short-circuit weights the right child's steps by the probability the left didn't short-circuit). Don't build the three-accumulator override machinery; it's obsolete.

**`eq` matrix.** With hash-consing, syntactic equality is row-index equality: `EQ[i][j] = (i == j)` plus the lifted-constant cases. Precompute once.

**Memory.** $n=6$, full grammar: 31K rows × 2,800 opponents × 4 bytes ≈ 350MB per pass. Chunk over opponents in blocks of ~500 if needed. At $n=7$ the square matrix is ~870MB per array; you won't need it (§4).

**Reference evaluator.** A separate, slow, recursive implementation with explicit memoization on `(program, opponent, budget)`. Used only to verify the batched one. Must agree exactly on every pair at $n\le 4$.

## 4. The attractor chain

**You never need the square matrix beyond $n=6$.** Testing whether mutant $q$ tips attractor $A$ needs only the $(|A|+1)^2$ sub-matrix. Cost is $|\mathcal{L}|\times\sum_A|A|$ — roughly $|\mathcal{L}|\times 600$ with a few hundred attractors of size ~3. At $n=7$ that is ~9M pairs, $n=8$ ~45M, $n=9$ ~240M. Batch per attractor: one rectangular evaluation of all programs against $A$'s members, with $A$'s internal matrix precomputed. New attractors discovered during exploration get their own batch.

**Selection dynamics: deterministic replicator as primary.** For a population over types $\{a_1..a_k\}$ with frequencies $x$ and payoff matrix $U$: $\dot x_i = x_i(U x)_i - x_i(x^\top U x)$. Integrate (RK4 or simple Euler with small step) to convergence. This is the mean-field limit; it makes "settles at $B$" deterministic and gives:

- advantageous mutant → grows to a new rest point (monomorphic or polymorphic)
- disadvantageous mutant → dies, return to $A$
- neutral mutant → stays at its initial frequency $1/N$; the neutral set is a continuum of rest points

**Rest-point detection.** Converged when $\|\dot x\| < \text{tol}$. Classify: monomorphic (one type), polymorphic (several, all with equal fitness — verify), or **non-convergent** (still moving at the iteration cap, or $\|\dot x\|$ not decreasing). Non-convergent → **indeterminate; record the trajectory** (THEORY.md §5). Do not average it.

**Neutral sets.** Discretize by $N$: positions $k/N$ along a neutral edge are distinct chain states. A mutant in a neutral set moves the position by $1/N$ toward its own type. Under the length prior, short types accumulate faster (ALLC is 1 node, FairBot 5–6), so the walk along the FairBot–ALLC edge is biased toward ALLC. Expect faster collapse than unbiased drift.

**Chain construction (exploratory):**

```
attractors = {all-p : p in L}
frontier = attractors
while frontier:
    for A in frontier:
        for q in L:                        # every program is a candidate mutant
            x0 = A with q at frequency 1/N
            B = replicator_converge(x0)    # or INDETERMINATE
            record edge A → B with weight μ(q)
            if B new: add to attractors and frontier
```

Then $P(A\to B)\propto\sum_q\mu(q)\,\mathbf 1[\text{settles at }B]$, normalize rows, solve $\pi$ as the stationary distribution (one sparse eigenvector / linear solve).

**Finite-$N$ Moran as a check.** Simulate the actual birth-death process at small $N$ and finite $\varepsilon$; compare empirical occupancy to $\pi$. Disagreement means a missed attractor or a neutral set handled wrong.

**Certification at level $n$.** For each $q\in\mathcal{L}_{n+1}\setminus\mathcal{L}_n$ and each attractor $A$ of the $n$-chain, does $q$ tip $A$? If no $q$ does, $\pi_{n+1}=\pi_n$ up to neutral mass. This is the incremental step itself, so it's free.

**Behavioral dedup (extensional arms only).** Two programs identical against every attractor are interchangeable for the chain. Collapse them *after* computing, and assign the merged class the summed $\mu$. Never in the source arm.

## 5. Games as config

```yaml
# games/pd.yaml
actions: [C, D]
payoffs:            # row player's payoff, [row action][col action]
  C: {C: 0, D: -2}
  D: {C: 1, D: -1}
minimax_action: D
role: false
```

Stag Hunt: `actions: [Stag, Hare]`, `minimax_action: Hare`, `role: false`. Chicken: `role: true`. Asymmetric games: two payoff tables plus `role: true`; the evaluator symmetrizes by averaging over role assignment.

The evaluator is game-independent; only §5 and the minimax action come from config.

## 6. Sweep

| Axis | Values | Where it enters |
|---|---|---|
| arm | strong, weak, source | enumeration |
| $n$ | up to 6 (square), up to 9 (incremental) | enumeration |
| $N$ | 10 … 10,000 | chain only — free |
| protocol | replicator (primary), Moran check | chain only |
| X-off | on/off | enumeration; cheap arm |
| game | per config | evaluation |

$T$ is not swept; iterate to convergence. $\beta$ is fixed at 1 bit. Cache the evaluation on `(arm, n, game, x_off)`; everything downstream reuses it.

## 7. Reporting

For every sweep cell, one row in a single results table with: config columns; the support of $\pi$ (attractors, with their compositions); the weights; the **transition structure** (which mutant moves which attractor to which); divergence rate; indeterminate flag with trajectory reference; mean description length in the support; deadweight loss per interaction; and, where applicable, the distributional statistic (split on the demand game; whether the `ROLE`-symmetrized outcome maximizes the unweighted sum).

Never report weights without support and transitions. A $\pi$ spread across qualitatively different states reads as a mixture that never occurs.

## 8. Repo layout

```
src/
  dsl.py           # grammar, enumerator, hash-consing, tape construction
  evaluate.py      # batched value iteration → V
  reference.py     # slow recursive evaluator (oracle)
  chain.py         # attractor discovery, replicator, stationary distribution
  moran.py         # finite-N simulation check
  report.py        # results table, support+transition rendering
games/
  pd.yaml  stag.yaml  chicken.yaml  ...
predictions/       # test-game verdicts, dated, committed before first run
runs/
  <config-hash>/   # cached V, attractors, π, report row
```

## 9. Performance budget

MacBook, Python + NumPy, under an hour for the PD/Stag sweep at $n=6$ across all three arms with $N$ swept. Weak arm to $n=9$ via the incremental path is a separate ~hour. Numba on the value-iteration inner loop is the escape hatch if the batched NumPy is slower than estimated; measure at $n=4$ and $n=5$ first and extrapolate — cost scales as $|\mathcal{L}|^2$ for the square matrix and $|\mathcal{L}|$ for the incremental path.

Stage 4 in the old plan (Edmonds over $|S|^2$ edges) is gone; the attractor chain replaces it with one stationary-distribution solve.

## 10. Things that will bite

- **`and`/`or` argument order matters.** Don't sort arguments. Don't canonicalize.
- **`ME` inside shared subterms.** Rows must be per-program. Sharing `ME`-free rows across programs is a valid later optimization; do it only after the per-program version agrees with the reference.
- **Divergent pairs are real data.** Don't silently assign minimax; log them, report the rate.
- **Neutral sets are continua.** A single "all-FairBot" rest point is wrong when ALLC is in the family; the edge is the state.
- **Indeterminate is a result.** If replicator doesn't converge, say so, keep the trajectory, move on.
- **Bits, not nodes.** For $\mu$. Every time.
- **`eq` is the only non-extensional primitive.** If a program's behavior depends on the opponent's source in any other way, that's a bug.
