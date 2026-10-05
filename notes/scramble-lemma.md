# The scramble lemma and Claim A (2026-10-05)

Spec `specs/2026-10-05-scramble-lemma.md`, predictions `predictions/2026-10-05-scramble-lemma.md`, numbers in
`runs/scramble-lemma.{md,json}`, code `src/scramble_lemma.py`.

## 0. Definitions and the evaluator's conventions

**Play.** `V[a, b] = 1` iff program a plays C against b, at the stable world of `modal._evaluate` (the packed
evaluator `moat_static_big` used for the n = 12 cache has the same semantics). PD payoffs `PD = [[-1, 1], [-2, 0]]`,
i.e. T = 1, R = 0, P = −1, S = −2 (T − R = 1, P − S = 1).

**Faker.** q fakes x iff `V[x, q] = 1` and `V[q, x] = 0` (`spoiler_conditioned.fakers_of`).

**Establisher.** q is an establisher iff `V[q, q] = 1` and `V[q, D] = 0` (`spoiler_conditioned.cdata`, `est`). A
*non-establisher* is any q that is not: it defects on itself, or it cooperates with D (or both).
*Note on the spec's wording:* the spec's parenthetical in Claim A reads "q does not self-cooperate", which is a slip:
its own THEM(THEM) argument treats self-cooperating non-establishers. The code's definition is used throughout.

**Claim A, made precise.** For x ∈ P and every non-establisher faker q of x: `V[q, D] = 1` or `V[q, C] = 1`.
Consequence: in any population whose only other types are D and ALLC, with shares x_D, x_A,
f_D − f_q = (P − S)·V[q,D]·x_D + (T − R)·V[q,C]·x_A (q's payoff against D is S if it cooperates, P if not; against ALLC
it gets R or T; D gets P and T), so f_q < f_D whenever the corresponding share is positive.

### The evaluator's world convention (`src/modal.py`, `_evaluate`)

- One global linear chain of worlds n = 0, 1, 2, … shared by **every** ordered pair (p, q). At world n, a box atom of
  kind C (resp. D) at level L with argument pair (p, q) is true iff `hc[L, p, q]` (resp. `hd`), i.e. iff
  `val_m[p, q] = C` (resp. D) at **every** world m with L ≤ m < n.
- Argument pairs: `THEM(ME)` in x's program played against y reads the pair (y, x); `THEM(THEM)` reads (y, y);
  `THEM(^A)` reads (y, A) with A the canonical class of the probe.
- The values val_n are computed from hc/hd at world n; then hc/hd are updated with val_n. The loop returns at the first
  n ≥ 2 at which no hc/hd entry changes.

**Lemma 0 (box soundness at the stable world, every level, every nested call).** Let n* be the world returned. Then
(i) val_m = val_{n*} for every m ≥ n*; (ii) for every atom (kind, L, p, q) that is true at n*, the stable value
val_{n*}[p, q] is the boxed action.

*Proof.* (i) val_{n+1} is a function of (hc, hd) after the update at world n. At n* the update changes nothing, so the
(hc, hd) used for world n* + 1 equal those used for world n*; hence val_{n*+1} = val_{n*}, and the update at n* + 1
again changes nothing; induct. (ii) The atom is true at n* iff the boxed action held at every m with L ≤ m < n*. The
update at n* folds val_{n*} into hc/hd and changed nothing, so the boxed action also holds at m = n* (here n* ≥ 2 ≥ L,
so world n* is inside the level-L range: the `if n < L: continue` guard does not skip it). By (i) the stable value
of the pair is val_{n*}[p, q]. ∎

Remarks for the ledger.
- The argument uses only that (a) all pairs share one chain, (b) box truth at world n quantifies over worlds below n
  from L up, (c) the evaluator stops at a global fixed point. It does not use Löb, uniqueness of fixed points, or the
  level being 0 or 1: it holds for every level L ≤ n*, so for BOX_k at any Con^k level in an evaluator with the same
  convention (`conj4.py`'s independent evaluator; checked below).
- The nested call `THEM(THEM)` reads the pair (y, y) at the **same** world index as the outer call. There is no
  separate "inner" chain, so no level/world mismatch can arise; the step sol flagged as the one that could fail is
  covered by Lemma 0 (ii) applied to the pair (y, y).
- Canonical classes: two programs with the same reduced box function play identically against everything (the
  modal.py docstring's induction on worlds), so "q plays C against ^C" is "q plays C against the population's ALLC".

(`conj4.play` uses the same convention per pair: `BOX_L` at world n is "the pair played the boxed action at every
m with L ≤ m < n", and the stable value is the trace's settled value; Lemma 0 (ii) holds there because a box true at a
world beyond the settling point quantifies over a world where the pair already plays its settled value.)

## 1. Claim A, case by case

Each member x ∈ P is a single box atom with the identity truth table (`tt = 2`), so `V[x, q]` is the stable value of
that atom when x plays q.

**A1 (FairBot `BOX(THEM(ME))`, and `BOX1(THEM(ME))`): no faker exists.** If `V[x, q] = 1`, the atom "q plays C against
x" (pair (q, x), level 0 or 1) is true at n*, so by Lemma 0 (ii) `V[q, x] = 1`. Hence no q has `V[x,q] = 1, V[q,x] = 0`.
Claim A holds vacuously. *Ledger:* Lemma 0 only (shared chain, stable-world fixed point). No Löb, no uniqueness of
fixed points, no level-specific fact. Löb is needed for x to *self-cooperate* (to be an establisher), not for it to be
unfakeable. Holds at every level L and every cutoff n (the argument never looks at q's syntax).

**A2 (`BOX(THEM(^C))`, `BOX1(THEM(^C))`): every faker cooperates with ALLC.** If `V[x, q] = 1`, the atom "q plays C
against the class C" is true at n*, so `V[q, C] = 1`: q cooperates with ALLC. This holds for every q with
`V[x, q] = 1`, faker or not, establisher or not. So every faker (non-establisher or not) is strictly worse than D
against ALLC: f_D − f_q ≥ (T − R)·x_A > 0. *Ledger:* Lemma 0 and canonicalization of the probe class (the probe `^C`
is the population's ALLC class). Every level, every cutoff. Generalizes: a faker of `BOX_L(THEM(^A))` cooperates with
A, for every probe A.

**A3 (`BOX(THEM(THEM))`, `BOX1(THEM(THEM))`): every non-establisher faker cooperates with D.** If `V[x, q] = 1`, the
atom "q plays C against q" (pair (q, q), the nested call, same world index) is true at n*, so `V[q, q] = 1` by
Lemma 0 (ii). A non-establisher with `V[q, q] = 1` must have `V[q, D] = 1` (definition). So every non-establisher faker
cooperates with D, and f_D − f_q ≥ (P − S)·x_D > 0 when x_D > 0. *Ledger:* Lemma 0 for the nested pair (q, q) and the
definition of establisher. No Löb. Every level, every cutoff. Sol's dichotomy (vacuous, or a level/world mismatch)
is neither: the box *is* sound for actual self-cooperation (so every faker self-cooperates), but that does not exclude
non-establisher fakers — it forces them to be self-cooperators that cooperate with D, e.g. `not(BOX(THEM(ME)))` and
`not(BOX(THEM(THEM)))` against `BOX1(THEM(THEM))` (RESULTS "Spoiler-conditioned establishment", the disadvantaged
forced pairs). They exist and are all D-cooperators.
- The same argument also says more: a faker of the THEM(THEM) pair can never be *neutral* (defect on D and on itself),
  since it self-cooperates. Its only types are "disadvantaged" (cooperates with D) and "advantaged" (an establisher).
- *Establisher-fakers exist, but not the spec's example.* The spec's q = `and(BOX(THEM(THEM)),not(BOX(THEM(^C))))` is
  **not** an establisher. PA proves q(C) = D, so the second conjunct is ¬□⊥ = Con(PA), and q's self-play is the
  fixed point p ↔ □p ∧ ¬□⊥, whose unique solution is ⊥: q defects on itself. On the chain: at world 0 every box is
  vacuously true, so q vs q = and(T, not T) = D at world 0, and `BOX(THEM(THEM))` is false from world 1 on. My first
  repair, `and(BOX(THEM(THEM)),BOXD1(THEM(^C)))`, also fails: q vs C is C at worlds 0 *and* 1 (BOXD1 is vacuous at
  both), so "q defects on C" is not provable even in PA + Con(PA) on the chain, and q vs q is D from world 2 (conj4's
  evaluator: q vs q = D). Both failures are the same fact: an ALLC-punishing clause that refers to the program's own
  play against ALLC costs a Con level per self-reference step. Working examples, found by enumeration and checked by
  conj4's evaluator: `BOX1(THEM(^not(BOX(THEM(ME)))))` fakes `BOX(THEM(THEM))` (an establisher that cooperates with
  ALLC and defects on D: it cooperates iff PA + Con(PA) proves the opponent cooperates with `not(FairBot)`, which
  self-cooperates from world 1 on; `BOX(THEM(THEM))` defects on `not(FairBot)` because the latter's self-play is D at
  world 0, so q defects on x, while x sees q self-cooperate at every world and cooperates), and `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` fakes
  `BOX1(THEM(THEM))` (self-cooperates, defects on D and on ALLC). Such a q is not dangerous for cooperative fixation (it is itself an
  establisher) but is for target identity; sol's caveat stands: an establisher-faker could in principle hold a
  parochial network with inefficient cross-play (not observed at n ≤ 12: cooperative fixation and efficiency coincided
  in every spoiler cell).

**Conclusion (proved).** Claim A holds for all six members of P, at every level of an evaluator with the shared-chain
convention and at every cutoff, with no use of Löb. Stronger forms: the FairBot pair has no fakers; every faker of a
probe-reader cooperates with ALLC; every faker of the THEM(THEM) pair self-cooperates, hence is either an establisher
or a D-cooperator.

**What Claim A does not give.** It is about play against D and ALLC only. In a scramble with other seeded programs
the faker's fitness relative to the mean also depends on them; that is Claim B's job (§3). And the probe-readers'
fakers (type "neutral" against D) lose only through x_A: once ALLC is extinct they are payoff-identical to D among
{D, faker}, which is why their per-copy survival is the highest of the non-establisher types.

**Static check (exhaustive, n = 6, 9, 12; `scramble_lemma.py static`, `xcheck`).** 0 counterexamples to Claim A over
every faker of every member of P. Non-establisher faker counts at n = 12: FairBot pair 0 / 0; `BOX(THEM(THEM))` 374
(all cooperate with D *and* ALLC), `BOX1(THEM(THEM))` 643 (310 cooperate with D only, 333 with both); `BOX(THEM(^C))`
1,846 and `BOX1(THEM(^C))` 1,712 (all cooperate with ALLC; 566 / 529 also with D). Establisher-fakers at n = 12: 114,
92, 118, 108 classes, mass ≈ 1.7–2.0·10⁻⁵ each (cutoff units). Every faker of the THEM(THEM) pair self-cooperates and
every faker of the probe pair cooperates with ALLC, as A2/A3 say. Independent evaluator (`conj4.play`): every class
that a member of P cooperates with at n = 12 (24,981 (x, q) pairs) re-evaluated on (x,q), (q,x), (q,q), (q,D), (q,C):
0 disagreements with the cache, 0 Claim A failures.

## 2. The kernel (read from `seeds_in_n._run` and `almost_all_seeds._sample_parent`)

Single island, N individuals, no mutation or migration. One *event*: draw a parent class j with probability
k_j f_j / Σ_i k_i f_i, where f_j = exp(w π_j) and π_j = (Σ_i k_i U[j, i] − U[j, j]) / (N − 1) (average payoff against
the others, self excluded); draw a victim uniformly from the N individuals; if the victim's class is j nothing changes,
else the victim is replaced by a j. A *generation* is N events (the clock of `tC`, `ext_t`, and the flog rows).
**This is a birth–death Moran process (fitness at birth, uniform death), not death–birth as the spec says.**

**Lineage rates (exact).** For class q with k copies, write F̄ = Σ_i k_i f_i / N. Per event,
P(k → k + 1) = (k f_q / N F̄)·(N − k)/N and P(k → k − 1) = (k/N)·(1 − k f_q / N F̄). Hence
E[k' − k | state] = (k/N)·(f_q/F̄ − 1) =: (k/N)·r, exactly, with no rarity assumption. Per generation the per-capita
drift is r = f_q/F̄ − 1 and the per-capita birth and death rates are each ≈ 1 (b = f_q(N − k)/(N F̄), d = 1 − k f_q/(N F̄)).

## 3. Claim B: the scramble lemma

### B1 (proved): the exponential martingale
Let r_e = f_q/F̄ − 1 evaluated on the state before event e (for an absent q, π_q is computed as for one copy; k = 0
then, so the choice does not matter), and Λ_t = −Σ_{e < tN} log(1 + r_e/N) (t in generations; 1 + r/N ≥ 1 − 1/N > 0).
Then M_t = k_t · e^{Λ_t} is a martingale: E[k_{e+1} | F_e] = k_e (1 + r_e/N) and Λ is predictable.
*Consequence.* For every bounded stopping time τ (e.g. τ = τ_A ∧ T_max, τ_A the island's first ALLC extinction) and
every constant Λ ≥ 0,
  **P(q alive at τ, Λ_τ ≥ Λ | F_0) ≤ k_0 e^{−Λ},**
because on that event k_τ ≥ 1 and k_τ ≤ M_τ e^{−Λ}, and E[M_τ | F_0] = k_0 by optional stopping. Hence, for any seed
event E (F_0-measurable) and any Λ,
  **P(q alive at τ | E) ≤ P(Λ_τ < Λ | E) + E[k_0 | E]·e^{−Λ},**
and, binning Λ_τ at levels 0 = a_0 < a_1 < …, P(q alive at τ | E) ≤ Σ_i min{P(Λ_τ ∈ [a_i, a_{i+1}) | E), k̄_0 e^{−a_i}}.
- The correlation between the stopping time and survival that sol flagged is handled by optional stopping at a bounded
  stopping time; no fixed-time window is needed (a fixed T can be used too: P(alive at τ_A) ≤ P(alive at T) + P(τ_A < T)).
- Λ_τ is the **net** integrated relative deficit, so the exposure before the faker drops below the mean (where r > 0)
  is inside the statement, with its sign. Λ_τ ≥ ∫_0^τ (1 − f_q/F̄) dt since −log(1 + x) ≥ −x.
- It is a first-moment (union-over-copies) bound: per seeded copy it is e^{−Λ}. It is *not* sharp for a neutral
  lineage: with r ≡ 0, Λ ≡ 0 and the bound is k_0, while the true survival of a critical lineage to time t decays like
  1/(1 + t) per copy. The demographic (critical-branching) factor is exactly what the first moment discards.
*Ledger:* the kernel's update rule (read from code) only. No approximation; no rarity, no branching limit.

### B2 (proved): from relative fitness to payoffs
By Jensen, F̄ = Σ (k_i/N) e^{w π_i} ≥ e^{w π̄} with π̄ = Σ (k_i/N) π_i, so f_q/F̄ ≤ e^{−w(π̄ − π_q)}. With payoffs in
[S, T] = [−2, 1], |π̄ − π_q| ≤ Δ = 3, and on [−wΔ, wΔ]:
  1 − f_q/F̄ ≥ w·[c_w (π̄ − π_q)^+ − C_w (π_q − π̄)^+],  c_w = (1 − e^{−wΔ})/(wΔ), C_w = (e^{wΔ} − 1)/(wΔ).
At w = 0.3: c_w = 0.659, C_w = 1.615. So Λ_τ ≥ w ∫_0^τ [c_w (π̄ − π_q)^+ − C_w (π_q − π̄)^+] dt.
*Ledger:* the fitness map f = exp(w π) and the payoff range. These are the "demographic constants" of the spec.

### B3 (identity): the type-specific deficit
π̄ − π_q = Σ_j x_j (π_j − π_q) with x_j = k_j/N, and π_j − π_q = Σ_i x̃_i (U[j, i] − U[q, i]) (x̃ the self-excluded
shares). In the reduced population {D, ALLC, q} with q rare (x_q → 0) and its self-term dropped:
- *probe-faker* (C on ALLC, D on D and on itself; e.g. `BOX(THEM(^D))`, "neutral" against D):
  π_D − π_q = (T − R) x_A = x_A, π_A − π_q = (S − P) x_D + (R − R) x_A = −x_D, so
  **π̄ − π_q = x_D x_A − x_A x_D + O(x_q) = x_A x_q**. The probe-faker is *exactly at the mean* to first order: it loses
  to D by x_A but beats ALLC by x_D, and the mean is the x-weighted average. Its Λ is second order in its own share.
- *D-cooperator* (C on D and on itself, D on ALLC; e.g. `not(BOX(THEM(ME)))`, "disadvantaged"):
  π_D − π_q = (P − S) x_D + (T − T) x_A = x_D (+ x_q), π_A − π_q = (S − S) x_D + (R − T) x_A = −x_A (− 2x_q), so
  **π̄ − π_q = x_D² − x_A² + O(x_q)**: above the mean while ALLC outnumbers D, below once D overtakes ALLC, and still
  below after ALLC is gone (x_D²).
- *both* (C on D and on ALLC): π_D − π_q = x_D + x_A, π_A − π_q = 0·x_D... (S − S) x_D + (R − R) x_A = 0, so
  π̄ − π_q = x_D (x_D + x_A) ≥ 0 throughout.
Losing to D (Claim A) is therefore not the same as losing to the mean (sol's second point), and the probe-faker is the
extreme case: Claim A makes it strictly worse than D, but in {D, ALLC} it is mean-neutral. Other seeded programs add
Σ_{j ∉ {D, A, q}} terms bounded by 3·(their mass) per unit time; these are measured along the trajectories below.

### B4: the seed event E and the exposure
**E** = {x_A(0) ≥ 0.3 and x_D(0) ≥ 0.3}. μ(ALLC) = μ(D) = 0.469 / 0.466 / 0.464 at n = 6 / 9 / 12 (cutoff units), so by
Chernoff P(E^c) ≤ 2 exp(−N·KL(0.3 ‖ 0.464)) = 7.3·10⁻³ at N = 100 and 3.5·10⁻¹⁰ at N = 400 (exact binomial:
5.6·10⁻⁴ and 1.4·10⁻¹¹). Inserting k ≤ 10 forced copies moves x_A, x_D by ≤ 0.1 at N = 100 and 0.025 at 400.
*In inf units* (the fixed infinite length prior), μ_inf(ALLC) and μ_inf(D) are fixed positive constants (each ≥ the
n = 12 cutoff mass times Z_12/Z_∞, where shell s carries prior mass 1/(2s²), so Z_12/Z_∞ = Σ_{s≤12} s⁻² / (π²/6) = 0.951;
hence μ_inf(ALLC), μ_inf(D) ∈ [0.441, 0.490]), so P(E^c) ≤ 2 exp(−c N) uniformly in n with c = KL(0.3 ‖ 0.441) = 0.042.

**Exposure lemma (proved, weak).** Let K = k_A(0). For t ≤ 1/2 generation, the number of original ALLC individuals
killed is dominated by Bin(N/2, K/N) (each event kills a uniform individual), so with probability ≥ 1 − e^{−K/24}
(Chernoff, δ = ½), k_A(t) ≥ K/4 on [0, ½] and ∫_0^{1/2} x_A dt ≥ x_A(0)/8. The same holds for D. This is what can be
proved by elementary coupling: the exposure is *positive* with failure probability e^{−Θ(N)} on E. It is
quantitatively useless (Λ ≳ 10⁻³), because the deficit that matters builds over tens of generations as D eats ALLC.
A quantitative version needs the density process to stay near its mean-field (replicator-type) path over a bounded
horizon T: standard for density-dependent Markov chains (Kurtz; Darling–Norris 2008), with failure probability
≤ C exp(−c N η² e^{−2LT}) for a deviation η, L a Lipschitz constant of the drift (≤ 2wΔ·e^{wΔ} here). Those constants
are not computed. **So the distribution of Λ_τ under E is measured, not proved.** The proved content is B1–B3: the
inequality holds for whatever Λ_τ the trajectory realizes, with the stopping-time correlation handled exactly.

## 4. The combined per-island bound (union over seeded faker lineages)

Fix a member x ∈ P seeded in the island, the seed event E, and the stopping time τ = τ_A ∧ (local freeze) ∧ T_max.
Events: A = {x alive at τ}; F_q = {class q alive at τ} for each faker class q of x present in the seed; F = ∪_q F_q;
Est_x = {x's network wins the island} ⊆ A. (Cooperative fixation through another establisher only helps; dropping it
makes the bound conservative.)

*Identity.* P(Est_x) = P(Est_x | A, F^c)·P(A) − P(A ∩ F)·h, with h = P(Est_x | A, F^c) − P(Est_x | A, F), the
absolute harm.

*Bound.* P(A ∩ F) ≤ P(F) ≤ Σ_q P(F_q) (union over lineages), and by B1, for each class q with K_q seeded copies,
P(F_q | E) ≤ inf_Λ [P(Λ^{(q)}_τ < Λ | E) + E[K_q | E] e^{−Λ}] =: E[K_q | E]·q̄_q. Hence

  **P(Est_x | E, x seeded) ≥ ρ̃_x(N) − Σ_q E[K_q | E]·q̄_q·h_q⁺,   ρ̃_x(N) := P(A | E)·P(Est_x | A, F^c, E),**

with h_q⁺ = max(h_q, 0) ≤ P(Est_x | A, F^c) ≤ 1. Equivalently ρ̃_x·[1 − Σ_q E[K_q|E]·(q̄_q/P(A|E))·h_q^rel], with
h^rel = h/P(Est_x | A, F^c) ∈ [0, 1] the relative harm (measured ≤ 0.9 in the spoiler run). (With several fakers alive
the harm is not additive; the union bound charges each the full h_q, which over-counts and stays valid.)
Every quantity: E[K_q | E] = N μ_q (iid seeding, up to the O(e^{−cN}) effect of conditioning on E); q̄_q from B1 with
the measured distribution of Λ under E; ρ̃_x(N) from the establishment side (rigorously positive uniformly in n,
RESULTS "the tail in n", via μ_est ≥ 0.0207); h_q measured.

**What is proved, measured, assumed.**
- Proved: the identity and the union bound; B1 (martingale, optional stopping at a bounded stopping time, no
  approximation); B2 (constants c_w = 0.659, C_w = 1.615 at w = 0.3); B3 (type decomposition, exact in {D, ALLC, q});
  Claim A (all six members, every level, every cutoff); P(E^c) ≤ 2e^{−0.042 N} uniformly in n; the weak exposure lemma.
- Measured: the distribution of Λ_τ under E (hence q̄_q); h_q; P(A | E) and P(Est_x | A, F^c, E).
- Assumed (measured null in the spoiler run: replacement by D within ±0.004, k = 1 effects null): that ρ̃_x(N),
  defined with the faker present but dead by τ, equals the faker-free establishment chance ρ_x(N) up to a negligible
  in-scramble effect of the faker on the target.
- **N-dependence, stated plainly:** E[K_q | E] = N μ_q grows linearly in N. The spoiler term is
  N·Σ_q μ_q q̄_q(N) h_q, so the bound stays positive as N grows only if q̄_q(N) falls faster than 1/N or Σ_q μ_q is
  small against ρ̃/N. For the FairBot pair there is no spoiler term (no fakers, A1), so the bound is ρ̃(N) itself.

## 5. What the numbers say (runs/scramble-lemma.md)

- B1's martingale identity checks (E[k_τ e^{Λ_τ}]/E[k_0] = 0.96–1.07), and the instrumented kernel reproduces the
  spoiler run draw for draw. So the rates are right; the bound is valid.
- **The scramble kills fakers by demography, not selection.** The neutral ghost (faker's play, fitness pinned to the
  mean) survives to τ_A with probability ≈ E[1/(1 + τ)]: the critical-branching survival over τ ≈ 13 (N = 100) to 19
  (N = 400) generations. Probe-fakers survive exactly as the ghost (ratio 1.01–1.05), as B3 predicts (mean-neutral to
  first order). D-cooperators survive 2.1× (N = 100) and 6.8× (N = 400) less than the ghost; selection is 0.23–0.39 of
  their log deficit.
- So B1 as a bound on per-copy survival is vacuous for probe-fakers and 10–20× loose for D-cooperators. The right
  object is *demography × selection*, and the first moment drops the demography.

### B5 (stated, not proved): the demographic factor
Conjecture: for a class q with r ≤ 0 on [0, τ] (a supermartingale lineage) and per-capita birth rate ≥ b_min,
P(q alive at τ | F_0) ≤ k_0 / (1 + b_min·τ) up to the density-dependent correction (for k ≪ N, b ≈ f_q/F̄ ∈
[e^{−wΔ}, e^{wΔ}]). This is exact for the linear critical birth–death process (1/(1 + b t) per copy). A proof route:
the embedded jump chain of k is a ±1 supermartingale walk while r ≤ 0, so P(it survives M jumps) ≤ C k_0/√M, and the
number of jumps in [0, τ] is at least a Poisson-type count with rate 2 b_min k per generation. Not done. Measured: the
ghost matches E[1/(1+τ)] to within 12%. Combined with B1 by conditioning on the lineage's path (r ≤ −δ on a window),
one would get q̄ ≲ e^{−Λ}/(1 + b_min τ) only heuristically: the data give s_faker ≈ s_ghost·e^{−(0.35–0.53)Λ_med}.

### The N-dependence this exposes
τ_A grows like log N (13.4 → 19.0 generations from N = 100 to 400), so the per-copy survival of a probe-faker falls
only like 1/log N, while its expected number of seeded copies is N μ_q. The spoiler term N Σ μ_q q̄_q h_q therefore
grows like N/log N for the probe-readers unless h falls (it did fall, 0.44 → 0.16–0.22, from N = 100 to 400), and
only the D-cooperators (whose Λ grows with N: 2.2 → 3.6) are suppressed faster. **For the fakeable members of P, a
per-island bound uniform in N cannot come from the scramble alone.** It must come from what happens after it (h, rescue
by other establishers) or from the FairBot pair, which has no fakers. (Extrapolation from two N values; τ ∝ log N is
the deterministic decay time of ALLC to O(1) copies, not measured beyond N = 400.)
