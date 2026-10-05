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

## 3. The factorized spoiler bound (Task 2)

### 3.1 Exact per-founder union bound [proved]

Fix a seeded establisher x (the target), the seed event E, τ = ALLC extinction ∧ local freeze ∧ 2,000 generations.
A = {class x alive at τ}; for each founder j of a faker class q of x (every seeded copy of q is a founder), F_j =
{j's lineage alive at τ} (genealogical survival: in the untagged kernel a birth from j's lineage onto a copy of i's
lineage of the same class is a null event at the class level and a replacement at the lineage level, so tagging every
founder as its own payoff-identical class leaves the class-level law unchanged and makes F_j observable);
F = ∪_j F_j; Est = {x's class in the final support}. With h = P(Est | A, Fᶜ) − P(Est | A, F) (absolute harm) and
N_q = Σ_{j ∈ q} 1{F_j} the number of q-founders alive at τ:

  P(Est | E) = P(A | E)·P(Est | A, Fᶜ, E) − P(A ∩ F | E)·h            (identity, notes/scramble-lemma.md §4)
  P(A ∩ F | E) ≤ Σ_j P(A ∩ F_j | E) = P(A | E)·Σ_q E[N_q | A, E]       (union over founders, linearity)

Define the per-founder survival q̄_q = E[N_q | E]/E[K_q | E] (K_q the number of q-founders) and the **per-founder
dependence correction r_q = E[N_q | A, E]/E[N_q | E]**. Then, exactly,

  **P(Est | E) ≥ ρ̃·[1 − Σ_q E[K_q | E]·q̄_q·r_q·h_q^rel],   ρ̃ = P(A | E)·P(Est | A, Fᶜ, E),  h^rel = h⁺/P(Est | A, Fᶜ, E) ∈ [0, 1],**

with the harm charged to each faker class at the cell's h (the union over-counts when several fakers are alive, which
keeps it valid). Nothing here is assumed beyond the definitions. The old step (RESULTS "The scramble lemma") used
P(A ∩ F) ≤ P(F), i.e. it charged q̄_q/P(A) where this charges q̄_q·r_q; since E[N_q | A] ≤ E[N_q]/P(A), **r_q ≤ 1/P(A)
always**, so the new bound is never worse, and the 1/P(A) loss is replaced by the measured association r_q.

In the forced design (one inserted target founder, one inserted faker founder, tagged; the paired faker class only)
K_q = 1 + bg_q and r_q is measured on the inserted founder: r = P(F_j | A, E)/P(F_j | E). By exchangeability of the
founders of one class (identical rates, symmetric initial state), the inserted founder's r and q̄ equal the per-founder
averages over all q-founders.

### 3.2 What can be said about r_q [proved under named hypotheses]

- (H_ci) Suppose there is a σ-field 𝒢 (the "environment") given which A and F_j are conditionally independent. Then
  r = E[P(A|𝒢)P(F_j|𝒢)]/(P(A)P(F_j)) = 1 + Cov(P(A|𝒢), P(F_j|𝒢))/(P(A)P(F_j)) **[proved given H_ci]**, and by
  Cauchy–Schwarz **r ≤ 1 + CV(P(A|𝒢))·CV(P(F_j|𝒢))**.
- (H_mono) If in addition both conditional probabilities are nonincreasing functions of one scalar statistic of 𝒢 (the
  scramble duration τ is the natural one: Lemma D gives survivals ≈ 1/Φ_τ ≈ 1/(1 + τ) for both near-neutral lineages),
  Chebyshev's association inequality gives **r ≥ 1**: a shared background makes the target's and the faker's survival
  positively associated.
- Neither hypothesis is proved for the kernel. H_ci fails in two known ways: *slot competition* (one lineage's births
  remove the other's copies; negative, of order the lineages' joint share k/N) and *direct interaction* (a faker earns T
  against the target, so a large surviving target helps the faker; positive). So r is **[measured]**, and the
  shared-background part is estimated by r_env = E[s_A(τ)s_F(τ)]/(E[s_A(τ)]E[s_F(τ)]), s_·(τ) the conditional survivals
  in τ bins: the value r would take if the association ran through τ alone.
- Under H_ci with s(τ) = 1/(1 + τ) for both and τ with coefficient of variation v, r ≈ 1 + v²·(τ̄/(1 + τ̄))² ≈ 1 + v²:
  a scramble-duration spread of 20–30% gives r ≈ 1.04–1.09. A larger measured r points at direct interaction.

### 3.3 The confidence-qualified empirical bound (not a theorem)

Per cell (N, n, faker type), in the forced design: ρ̃ and h^rel measured on the faker runs (run to local freeze);
q̄ from Lemma D′ on the faker founder (binned form, Φ on the Poisson clock, measured distribution), which is a proved
inequality evaluated at a measured distribution; r measured. Point version: all at their estimates. Conservative
version: ρ̃ at its 95% lower bound, q̄ from the binned bound with each bin's probability at its Wilson upper bound, r
and h^rel at their 95% upper bounds. Label: **confidence-qualified empirical bound**; proved: the inequality in 3.1 and
Lemma D′; measured: every number plugged in.

*Correction made after the first report (declared in the run file):* the binned form Σ_i min{P(Φ ∈ bin_i), k₀/φ_i}
charges one cap k₀/φ_i per bin, so when Φ_τ ≈ 1 + τ is spread over ~20 unit bins it sums to ≈ 0.8–1 (vacuous). The
single-level form inf_φ [1 − (1 − 1/φ)^{k₀} + P(Φ_τ < φ)] is the inequality of Lemma D′ itself; the bound used is the
smaller of the two (both valid). Averaging the single-level bound over a mixing measure on φ cannot beat its infimum,
so within this family the single level is optimal; what it pays is the spread of τ (the bound is ≈ 1/(1 + τ_low) +
P(τ < τ_low), where the true survival is ≈ E[1/(1 + τ)]).

## 4. The establishment formula (Task 3)

**4.1 Post-scramble escape is two-type [proved formula, measured applicability].** At ALLC extinction the island is D
plus a remainder plus surviving establisher lineages. If the largest mutually-cooperating establisher block has K copies
and the remainder is treated as D, the exact birth–death formula gives the escape u_N(K) (§2). Applied island by island
to the measured state at τ, it predicts the per-island cooperative-fixation chance within 0–4% at N = 100 … 25,600 and
is calibrated in every bin of predicted u (runs file). **[measured]** Pooling is real: the "independent founders after
the scramble" form 1 − Π_j(1 − u(k_j)) under-predicts by 11% at N = 6,400 and 13% at 25,600.

**4.2 The scramble as near-critical branching [coupled + measured].** Each establisher founder is a lineage with per-copy
rates b = a(N − k)/N, d = 1 − ak/N (§0). Approximating it by a linear birth–death process in a deterministic
environment (the *coupling assumption*: the lineage's own effect on the environment and its frequency-dependent term are
dropped) gives Kendall's law: alive at τ with probability 1/Φ(τ), Φ(τ) = 1 + ∫_0^τ e^{−R}, and geometric with mean
e^{R(τ)}Φ(τ) given alive; so E[k_τ] = e^{R(τ)} per seeded copy. Measured: P(alive at τ) ≈ E[1/(1 + τ)]-like values
(0.069 / 0.052 / 0.040 / 0.033 / 0.029 at N = 100 … 25,600) and E[k_τ | alive] ≈ 20 / 30 / 34 / 39 / 46, close to 1 + τ.

**4.3 What sets E[k_τ] [measured, with a mean-field account].** E[k_τ]/k₀ for ALLC-cooperating establishers is
1.41 / 1.55 / 1.36 / 1.26 / 1.32 at N = 100 / 400 / 1,600 / 6,400 / 25,600 (lottery; forced targets 1.36 / 1.45 / 1.17),
not the curvature value 0.93. Two positive terms the spec omitted:
- *the family's own advantage:* in {ALLC, D, E}, π_E − π̄ = x_D·x_E, so an establisher gains w·x_D·x_E per generation
  from the other establishers it cooperates with; it grows as D replaces ALLC and does not vanish with N. The kernel's
  replicator flow from the full seed x = μ (n = 9) gives e^{R(τ)} = 1.03 / 1.09 / 1.15 / 1.22 / 1.30 at the mean-field
  τ for N = 100 … 25,600 (curvature included): it matches the measured E[k_τ] at N ≥ 6,400. **[derived numerically,
  post hoc]**
- *a survivor's own frequency:* a lineage with k copies gains ≈ w x_D (k − 1)/N; since E[k(k − 1)] ≈ 2t for a critical
  lineage, this adds ≈ (w x̄_D/N)·τ² to E[k_τ]: ≈ +0.4 / +0.2 / +0.1 at N = 100 / 400 / 1,600 (measured excess over the
  mean field: +0.38 / +0.46 / +0.21). It fades as τ²/N → 0.

**4.4 The formula.** With founders M ~ Bin(N, μ_est), τ the island's ALLC-extinction time, and each founder independently
alive with probability 1/Φ(τ) and geometric with mean ℓ(τ)Φ(τ),

  **p(N) ≈ E[u_N(K_τ)],  K_τ = Σ_{j ≤ M} k_j.**

- With ℓ = the curvature-only path (the spec's correction): under-predicts by 1.21–1.27 at N = 100–1,600 (S6).
- With ℓ = the full-seed mean field [post hoc, no fitted parameter]: ratio measured/predicted 1.17 / 1.16 / 1.07 / 1.01
  / 1.02 at N = 100 … 25,600. The residual at small N is the own-frequency term.
- Linear regime (N μ_est u₁ ≪ 1): p ≈ N μ_est·ℓ·u₁·κ_N with κ_N = E[u(k_τ)]/(u₁E[k_τ]) the concavity factor (measured
  0.59 / 0.66 / 0.80 / 0.93 / 0.97): the gap closes with N, which is why the local exponent (0.533 [0.495, 0.571] over
  100–1,600) exceeds 1/2. Since u₁ ≈ √(2c/(πN)), the leading behaviour is the naive √N law times ℓκ_N.
- Saturation: K_τ/N → μ_est·ℓ(τ_N) in probability as N → ∞ (the number of surviving founders, ~N μ_est/Φ(τ_N) with
  Φ ~ log N, grows like N/log N, so the compound sum concentrates) and u_N(x) = erf(x√(Nc/2))/erf(√(Nc/2)) → 1 for
  every fixed x > 0, so **p(N) → 1 at fixed cutoff**, with 1 − p decaying like erfc(μ_est ℓ √(Nc/2)) once K_τ
  concentrates. Measured: 0.686 at 6,400, 0.980 at 25,600; the pooled-family form 0.719 / 0.969 tracks it, the
  independent-founder form 0.577 / 0.821 does not. **[the limit statement is a consequence of the formula: proved for
  u_N, measured for the formula's applicability, heuristic (Kendall coupling) for the concentration of K_τ]**

## 5. Dependency ledger

| statement | status | rests on |
|---|---|---|
| Lemma D′ (P(alive at τ, Φ_τ ≥ φ) ≤ 1 − (1 − 1/φ)^{k₀}, any stopping time) | proved | kernel rates; Poisson clock; optional stopping for a bounded supermartingale |
| Lemma D (fixed T, killed at K and at f_q > F̄): ≤ k₀/(1 + d_min T), d_min = 1 − (K − 1)/N | proved | Lemma D′'s proof with deterministic θ |
| Unkilled survival ≤ Lemma D + k₀/K (if f_q ≤ F̄ on reachable states) | proved | supermartingale k, optional stopping |
| Event-clock transfer (factor ≤ 1.10 at N ≥ 100, T ≥ 5) | proved | monotonicity of S(m); Poisson independence of the event count |
| Stopped lower-tail form P(alive at τ) ≤ Lemma D(t₁) + P(hit K) + P(τ < t₁) | proved | inclusion; P(τ < t₁) measured |
| Per-founder union bound P(Est) ≥ ρ̃[1 − Σ E[K_q] q̄ r h^rel]; r ≤ 1/P(A) | proved | identity + union bound; definitions |
| r = 1 + Cov/(…) ≤ 1 + CV·CV; r ≥ 1 under H_mono | proved under H_ci (and H_mono) | hypotheses not proved for the kernel |
| r_q values (0.64–2.01 per cell; pooled 0.80–1.66) | measured | 10,000 forced backgrounds per (N, n, type) |
| Combined bound positive in 27/27 cells | confidence-qualified empirical | Lemma D′ evaluated at measured Φ; r, h, ρ̃ measured |
| Exact u_N(K) for a prover in a D sea | proved | kernel's birth–death ratios with self-excluded payoffs |
| Diffusion u(x) = erf/erf | derived (standard diffusion limit, not proved here) | drift c x²(1 − x), variance 2x(1 − x)/N |
| Post-scramble escape is two-type (semi-empirical within 4%) | measured | 17,400 lottery islands |
| Kendall form of the scramble (alive 1/Φ, geometric) | coupled (assumption: environment deterministic, own effects dropped) | measured sizes ≈ 1 + τ |
| ℓ = E[k_τ]/k₀ ≈ full-seed mean-field e^{R} at large N | derived numerically, post hoc; measured agreement at N ≥ 6,400 | replicator flow of the kernel |
| p(N) → 1 at fixed n | consequence of the formula; heuristic in the concentration step | u_N proved; formula measured to N = 25,600 |
| ρ̃ ≈ faker-free establishment | assumed (as in the scramble lemma) | — |
