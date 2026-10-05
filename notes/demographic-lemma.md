# The demographic lemma, the factorized spoiler bound, and the establishment formula (2026-10-05)

Spec `specs/2026-10-05-demographic-lemma.md` (reviewed by gpt-6.1-sol), predictions
`predictions/2026-10-05-demographic-lemma.md`, numbers in `runs/demographic-lemma.{md,json}`, code
`src/demographic_lemma.py` (extends `src/scramble_lemma.py`). Notation and kernel as in `notes/scramble-lemma.md` §0, §2.

Dependency ledger tags used below: **[proved]** (a complete argument from the kernel's update rule), **[coupled]**
(proved for a comparison process; the comparison step is stated), **[measured]** (a number from simulation, with an
interval), **[assumed]** (used but neither proved nor measured here).

## 0. Clock conventions (stated once, used throughout)

- **Event clock.** One *event* of the kernel: parent class j drawn with probability k_j f_j / Σ_i k_i f_i
  (f = e^{wπ}, π self-excluded), victim uniform over the N individuals, victim replaced by a j unless it already is a j
  (a *null event*). Events are indexed e = 0, 1, 2, …; a *generation* is N events, so "time t" in the simulator means
  event ⌊tN⌋. This is the discrete clock of every run file.
- **Poisson clock.** The same chain with events at the jump times of a rate-N Poisson process that is independent of
  everything else. Because the total event rate is N in *every* state (null events count as events), the embedded
  chain of the Poisson-clocked process is exactly the event-clocked kernel, and the number of events by time t is
  Π_t ~ Poisson(Nt), independent of the embedded chain. All continuous-time statements below are about the Poisson
  clock; §1.4 transfers them to the event clock.
- **Lineage rates.** For a class (or a tagged lineage) q with k copies and a = f_q/F̄ (F̄ = Σ_i k_i f_i / N), the
  per-event probabilities are p₊ = a·k(N − k)/N² and p₋ = (k/N)(1 − a k/N) (notes/scramble-lemma.md §2). Under the
  Poisson clock the *per-copy* rates per generation are
  b = N p₊/k = a(N − k)/N and d = N p₋/k = 1 − a k/N, so **b − d = a − 1 =: r exactly** (no rarity assumption), and
  b ≤ d iff f_q ≤ F̄. Note d ≥ 0 always (a k ≤ N because k f_q ≤ Σ_i k_i f_i).

## 1. Lemma D (demographic survival)

### 1.1 The general martingale (Lemma D′) [proved]

Let q be any class or tagged lineage, k_t its size, and under the Poisson clock let r_t = a_t − 1, d_t = 1 − a_t k_t/N
(both functions of the full state at time t; for k = 0 take a_t as for one copy, so d_t = 1), R_t = ∫_0^t r_s ds and

  **Φ_t := 1 + ∫_0^t d_s e^{−R_s} ds**   (nondecreasing in t, Φ_0 = 1).

**Lemma D′.** For every bounded (or a.s. finite) stopping time τ of the Poisson-clocked process, every k₀ and every
φ ≥ 1,

  **P(k_τ > 0, Φ_τ ≥ φ | F_0) ≤ 1 − (1 − 1/φ)^{k₀} ≤ k₀/φ,**   hence   **P(k_τ > 0 | F_0) ≤ k₀/φ + P(Φ_τ < φ | F_0).**

*Proof.* Fix φ. Let u_t solve u' = r_t u − b_t with u_0 = φ (b_t = a_t(N − k_t)/N the per-copy birth rate), i.e.
u_t = e^{R_t}(φ − J_t) with J_t = ∫_0^t b_s e^{−R_s} ds. Since e^{−R_t} = 1 − ∫_0^t r_s e^{−R_s} ds and b − r = d,
e^{−R_t} + J_t = 1 + ∫_0^t d e^{−R} = Φ_t, so u_t > 1 ⟺ Φ_t < φ (and then u_t > 0). Put θ_t = 1/u_t while
Φ_t < φ, and θ_t = 1 from the first time σ_φ at which Φ_t = φ on (θ is continuous, adapted and of finite variation, with
θ' = −θ r + b θ² before σ_φ and θ' = 0 after). Let x_t = 1 − θ_t ∈ [0, 1) and Y_t = 1 − x_t^{k_t}.
Between events Y changes only through θ: dY/dt = k x^{k−1} θ'. At an event, k → k ± 1 at per-copy rates b, d, so the
jump drift is k b·x^k(1 − x) − k d·x^{k−1}(1 − x) = k x^{k−1} θ (b x − d). Total drift:

  k x^{k−1} [θ' + θ(b(1 − θ) − d)] = k x^{k−1} [θ' + θ r − b θ²],

which is 0 before σ_φ (by the choice of θ') and equals 1{k = 1}·(r − b) = −1{k = 1}·d ≤ 0 after (θ = 1, x = 0,
0⁰ = 1). Rates are bounded (≤ N per generation), Y ∈ [0, 1], so Y is a bounded supermartingale and optional stopping
applies at any a.s. finite stopping time: E[Y_τ | F_0] ≤ Y_0 = 1 − (1 − 1/φ)^{k₀}. On {k_τ > 0, Φ_τ ≥ φ} we have θ_τ = 1,
so Y_τ = 1. ∎

*Ledger.* Only the kernel's per-event probabilities (read from code) and the Poisson clock. No rarity, no branching
approximation, no hypothesis on the sign of r, no independence between the lineage and the background: the rates may
depend on the full endogenous state, because the drift computation is done state by state (this is the "per-event
domination given the full state" the review asked for; nothing is coupled). The background path enters only through
the random variable Φ_τ.

*Remarks.*
- With r ≡ 0 and d ≡ 1 (a critical lineage far from the cap), Φ_t = 1 + t and Lemma D′ is the exact critical
  survival 1 − (1 − 1/(1+t))^{k₀}. For constant rates it reproduces Kendall's formula: Φ_t = e^{ρ(t)} + ∫_0^t b e^{ρ}
  with ρ = −R. (The spec's form 1/(e^{ρ(T)} + ∫ d e^{ρ}) has d where Kendall has b; with b < d it would over-claim.
  The correct equivalent is 1/(1 + ∫ d e^{ρ}).)
- Φ_t ≥ e^{−R_t} always (because Φ_t − e^{−R_t} = ∫ b e^{−R} ≥ 0), so Lemma D′ dominates the exponential-martingale
  bound B1 (notes/scramble-lemma.md §3) in its continuous-clock form: it is "demography × selection" in one
  statement, with the stopping-time correlation handled by optional stopping, as B1 was.
- The binned form used on data: P(k_τ > 0) ≤ Σ_i min{P(Φ_τ ∈ [φ_i, φ_{i+1})), k₀/φ_i}.

### 1.2 Lemma D (fixed time, killed process) [proved]

**Lemma D.** Let K ≤ N and let the lineage be *killed* (sent to a cemetery state that counts as dead) at the first
time its size reaches K, and also at the first time the state has f_q > F̄. Then under the Poisson clock, for every T,

  **P(killed lineage alive at T | k_0 = k₀) ≤ 1 − (1 − 1/(1 + d_min T))^{k₀} ≤ k₀/(1 + d_min T),  d_min = 1 − (K − 1)/N.**

*Proof.* Same Y with the deterministic θ_t = 1/(1 + d_min(T − t)), θ' = d_min θ², and Y := 0 in the cemetery.
In a live state (k ≤ K − 1, a ≤ 1): d = 1 − a k/N ≥ 1 − (K − 1)/N = d_min and b ≤ d, so the drift is
k x^{k−1} θ [θ(d_min − b) + (b − d)] ≤ k x^{k−1} θ [θ(d − b) − (d − b)] = −k x^{k−1}θ(1 − θ)(d − b) ≤ 0. Jumps into the
cemetery set Y to 0, which only lowers it. At T, θ = 1 and Y_T = 1{alive}. ∎

**Actual (unkilled) survival.** If f_q ≤ F̄ on every state reachable before T, then
P(alive at T) ≤ k₀/(1 + d_min T) + P(hit K before T), and P(hit K before T) ≤ P(hit K before 0) ≤ k₀/K because k is
then a nonnegative supermartingale (E[Δk] = (k/N) r ≤ 0 per event) and optional stopping at the hitting time of
{0, K} gives K·P(hit K) ≤ k₀. **[proved]** For K = N/20, d_min ≥ 0.95; for K = N/4, d_min ≥ 0.75.

**d_min derived, not assumed.** The per-copy death rate is d = 1 − a k/N; with a ≤ 1 (the hypothesis) and k ≤ K − 1
(the killing) it is ≥ 1 − (K − 1)/N. Without the hypothesis a ≤ 1 there is no uniform lower bound (d → 0 as a k → N),
which is why the cap is needed: an unkilled neutral lineage fixes with probability k₀/N, so no bound tending to 0 in T
can hold for it.

### 1.3 Stopped versions [proved]

- **Weighted identity.** Applying the proof of Lemma D at a stopping time τ ≤ T (killed process, θ_t = 1/(1 + d_min(T − t))):
  E[1{alive at τ} / (1 + d_min(T − τ))] ≤ k₀/(1 + d_min T). This does not bound P(alive at τ) without a lower bound on τ;
  survival-dependent τ cannot replace T (the review's point).
- **Lower-tail decomposition.** For every t₁, {alive at τ} ⊆ {alive at t₁} ∪ {τ < t₁} (alive at τ ≥ t₁ implies alive at
  t₁), so P(alive at τ) ≤ P(alive at t₁) + P(τ < t₁) ≤ k₀/(1 + d_min t₁) + P(hit K before t₁) + P(τ < t₁), whenever the
  hypothesis a ≤ 1 holds up to t₁. P(τ < t₁) is the lower tail of the ALLC-extinction time: **[measured]** here (a
  density-process bound in the sense of Kurtz/Darling–Norris would make it proved with uncomputed constants, as in
  notes/scramble-lemma.md B4).
- **Lemma D′ at τ** needs no hypothesis on a and no lower tail: P(alive at τ) ≤ k₀/φ + P(Φ_τ < φ). This is the
  stopped-process inequality used on data in Task 2; the distribution of Φ_τ is **[measured]**.

### 1.4 From the Poisson clock to the event clock [proved]

Let S(m) = P(lineage alive after m events) (killed or not, any fixed rule). S is nonincreasing in m (alive after m + 1
implies alive after m). Under the Poisson clock, P(alive at time t) = Σ_m P(Π_t = m) S(m) ≥ S(m*)·P(Π_t ≤ m*), with
Π_t ~ Poisson(Nt) independent of the embedded chain. Hence, for the event clock at T generations (m* = NT events),

  **S(NT) ≤ inf_{0 < t ≤ T} [1 − (1 − 1/(1 + d_min t))^{k₀}] / P(Poisson(Nt) ≤ NT).**

With t = T(1 − η) the denominator is a Poisson tail evaluated exactly (scipy), so the event-clock bound is the
Poisson-clock bound at a slightly shorter time, η = O(√(log(NT)/(NT))). Computed (`lemmaD_event_bound`, runs json
`static.lemmaD_event_clock`): the event-clock bound exceeds 1/(1 + d_min T) by a factor 1.10 / 1.08 / 1.06 / 1.05 at
N = 100 and T = 5 / 10 / 20 / 40, by 1.05–1.02 at N = 400 and by 1.03–1.01 at N = 1,600 (best t = 4.54, 4.73, 4.85 at
T = 5). The transfer costs at most 10%, and nothing at large N.
For stopping times defined by event counts (ALLC extinction is an event), Lemma D′ holds verbatim with Φ computed on
the Poisson clock of the same path; the simulator draws the exponential holding times from a separate generator so that
the event chain is unchanged, and reports Φ on both clocks (the event-clock Φ, with Δt = 1/N per event, is the natural
estimator; the two differ by a law-of-large-numbers fluctuation).

## 2. Static numbers for Task 3 (exact, before any simulation)

**Exact escape from a D sea [proved].** For a prover q (self-cooperates, defects on D) with j copies among N − j D,
self-excluded payoffs give π_q(j) − π_D = (j − 1)/(N − 1)·(R − P) = (j − 1)/(N − 1) (one copy is exactly neutral). In the
birth–death kernel P(j → j+1)/P(j → j−1) = f_q(j)/f_D(j) exactly (both moves need a non-null event; the (N − j)/N and
j/N victim factors cancel against the parent factors), so the standard birth–death formula is exact:
u_k = Σ_{i<k} Π_{j≤i} γ_j / Σ_{i<N} Π_{j≤i} γ_j with log γ_j = −w(j − 1)/(N − 1), i.e. Π_{j≤i} γ_j = e^{−w i(i−1)/(2(N−1))}.
(This is `chain.fixation` with kstar = N, the ρ = 0.0421 / 0.0214 / 0.0108 of earlier runs.)

**Diffusion [derived].** With x = j/N, the per-generation drift is x(f_q/F̄ − 1) ≈ c x²(1 − x) (c = w(R − P) = 0.3) and
the per-generation variance 2x(1 − x)/N (each non-null event moves j by ±1; the non-null rate per generation is
2N x(1 − x) to leading order). The backward equation (V/2)u'' + M u' = 0 is u'' = −N c x u', so
u(x) = erf(x√(Nc/2))/erf(√(Nc/2)) and u₁ = u(1/N) = √(2c/(πN))·(1 + O(c/N))/erf(√(Nc/2)). At N ≥ 100 the erf correction is
< 10⁻⁷ (Nc/2 ≥ 15). The diffusion overstates the exact u₁ by 3.8% / 2.0% / 1.0% / 0.5% at N = 100 / 400 / 1,600 /
6,400 (the exact process treats the first copy as neutral: s(j) ∝ j − 1, not j).

| N | u₁ exact | u₁ diffusion | u₄ exact | 1 − (1 − u₁)⁴ | u₁₆ exact | 1 − (1 − u₁)¹⁶ | 16 u₁ |
|---|---|---|---|---|---|---|---|
| 100 | 0.04206 | 0.04368 | 0.1677 | 0.1579 | 0.6083 | 0.4972 | 0.6729 |
| 400 | 0.02141 | 0.02185 | 0.0856 | 0.0829 | 0.3337 | 0.2927 | 0.3425 |
| 1,600 | 0.01081 | 0.01093 | 0.0432 | 0.0425 | 0.1718 | 0.1596 | 0.1730 |
| 6,400 | 0.00543 | 0.00546 | 0.0217 | 0.0216 | 0.0868 | 0.0835 | 0.0869 |

**Finding (static): pooled copies escape almost linearly.** u_k for k copies of one class (pooled) is within 1–10% of
k·u₁ for k ≤ √N, and well above the independent-copies form 1 − (1 − u₁)^k, because the frequency-dependent advantage
s ∝ (k − 1)/N grows with the pooled count. The spec's illustration (u₁ ≈ 0.044, k ≈ 15 → 0.49 against 0.65) used the
independent-copies form; the exact pooled value is u₁₅ ≈ 0.58. Concavity of u_k is real but enters only at k of order
√N/√c and through saturation at N; the spec's "independent-founder" form is therefore an assumption about *founders*,
not about copies.

**Mean-field curvature loss [derived numerically].** In {ALLC, D} (renormalized from 0.466/0.466) with the kernel's
replicator flow, a payoff-neutral ALLC-cooperating establisher has r = 1/(x_A e^{−w x_D} + x_D e^{w x_A}) − 1 ≈
−(w²/2) x_A x_D, and the flow has dx_A/dt ≈ −w x_A x_D, so ∫ r dt ≈ −(w/2)·x_A(0) ≈ −0.07: **e^{R} = 0.926–0.928 at
every N** (the integrand vanishes as ALLC dies, so the loss does not grow with τ). The spec's 10–20% (1 − 1/cosh(0.15)
per generation over τ) overstates it, because x_A x_D shrinks along the scramble. Not included here and of the opposite
sign: (i) the establisher family's own advantage, π_E − π̄ = x_D x_E in {ALLC, D, E} (≈ +w·x_D·μ_est per generation, the
same order as the curvature at x_E ≈ 0.025); (ii) a surviving lineage's own frequency, which adds ≈ (w x̄_D/N)·E[k(k−1)]
≈ (w x̄_D/N)·τ² to E[k_τ] (≈ +0.4 / +0.2 / +0.1 / +0.04 at N = 100 / 400 / 1,600 / 6,400 for τ ≈ 13 / 19 / 25 / 30).
These are order-of-magnitude estimates that motivate predictions S2 and S6; they are not used as results.
