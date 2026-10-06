# NOTATION.md — running glossary (started 2026-10-05 at the RS's request)

Add to this whenever a symbol or name is introduced. Values in brackets are the defaults used in most runs.

## Sizes and limits
- **n** — the program-size cutoff: the language L_n contains every program with at most n syntax nodes. Class counts
  grow fast (modal arm: 51 / 172 / 471 / 863 / 1,752 / 5,545 / 13,514 / 27,189 classes at n = 6 … 13). Static maps
  go to n = 12–13; chains to n = 8–9; the modal evaluator at n = 12 takes ~1 minute and 2.7 GB.
- **N** — population size of one well-mixed population, or of one island, or of one slot's population in the
  fixed-role games. "lim_N" means N → ∞ at ε → 0.
- **I** — number of islands. **M = I·N** — total population.
- **k** (in k-player) — number of player slots; the three-player game has k = 3 with separate populations per slot.
- **s** — a length shell: all programs of exactly s nodes. Under the length prior shell s has mass 1/(2s²).
- **b** — a legibility (verification) budget; **K** (in the club) — the club set; **k(x)** — essential box atoms of x.

## Dynamics
- **ε** — mutation probability per birth; **εN** — mutations per generation per island. "ε → 0" is the rare-mutation
  limit, where the population is monomorphic between mutations and the object is the chain over monomorphic states.
  "ε = 0" is no mutation at all: the absorption lottery over seeds.
- **w** — selection strength: fitness = exp(w · payoff) [0.3].
- **ρ(q | a)** — fixation probability of one mutant q in a population of a (Moran, size N). ρ ∝ N^(−1/2) for a
  mutant neutral at one copy and advantageous at two (FairBot into all-D); 1/N for a neutral mutant; e^(−Θ(N)) for a
  deleterious one.
- **π** — the stationary distribution of the ε → 0 chain; π(x) is the long-run fraction of time in all-x.
- **mN** — migrants per island per generation [1]; per-capita migration m = mN/N. A generation is I·N births.
- **w_g** — strength of island-level (payoff-weighted emigration) selection; 0 means none.
- **σ, s, f₀** (contracts) — swap probability per birth, search probability at birth, initial carrier frequency.
- **c, α** (pricing) — compute price per atom-world, and the exponent in the path c_N = c0·(N/10³)^(−α).
- **β** — the free arm's odds exponent: cooperative/defecting odds ∝ N^β (β = 1/2, derived).

## Statistics
- **P(C,C)** — probability that a random pair mutually cooperates; the dilemma statistic (never mean payoff share).
- **p = p(N, n)** — per-island establishment chance in the seed lottery (no migration): the chance one seeded island
  ends cooperative. ∝ N^0.55, ≈ 0.09 at N = 100.
- **d** — spoiler discount: establishment with a co-seeded faker divided by establishment without (≈ 1.1 measured).
- **q̄, h** — per-copy chance a faker survives the scramble; its post-scramble harm to the target (harm ≈ 1 − q̄·h).
- **rival share** — 1 minus the largest mutually-cooperating block's share of the cooperative π mass; **X** — the
  π-weighted probability that two cooperative programs cooperate with each other.
- **leak** — μ-mass of neutral entrants into x's world that are suckerable; **leak/μ** — divided by μ(x).
- **exit slope** — fitted d log(exit rate)/d log N; −1 is neutral drift, steeper is a moat.
- **certified-frozen / metastable / unresolved** — absorption categories for ε = 0 runs.

## Prior
- **μ** — the length prior over programs: shell s has total mass 1/(2s²), split equally among its programs; a class's
  mass is the sum over its programs. The infinite total is π²/12 ≈ 0.822. Three units: **raw** (unnormalized), **inf**
  (raw/(π²/12)), **cut** (raw/retained mass at cutoff n; the usual published unit). μ(ALLC) ≈ μ(D) ≈ 0.47 (cut, n ≥ 6).
- **μ_est** — mass of *establishers* (self-cooperating classes that defect on D); **μ_core** — mass of unfakeable
  establishers; **μ_pf** — mass of probe-fakers.

## Payoffs
- PD: T = 1 (exploit), R = 0 (mutual cooperation), P = −1 (mutual defection), S = −2 (exploited). T + S = R + P, so a
  faker's advantage is constant in frequency.

## Programs and classes (modal arm unless stated)
- **ALLC** (`C`), **D** — the constants; the ALLC *class* includes everything behaviourally identical to C.
- **FairBot** `BOX(THEM(ME))` — cooperate iff the opponent provably cooperates with me. **`BOX1`** — provable in
  PA + Con(PA). **`BOXD`** — provably defects.
- **PrudentBot** `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` — FairBot that also requires the opponent to provably defect on D.
- **P\*** `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` — a prudent family that exploits ALLC and defects on FairBot.
- **probe-readers** `BOX(THEM(^C))` etc. — cooperate iff the opponent provably cooperates with a constant; fakeable.
- **shadow** — the unconditional cooperator (ALLC) that drifts into a cooperative world neutrally; **faker** — a
  program that defects on x while x cooperates with it (strict invader); **sucker** — a program that cooperates with
  something that defects on it; **establisher** — self-cooperates and defects on D; **drift-closed** — no member of
  x's mutual-cooperation component is suckerable; **universality** — μ-weighted share of FairBot's component that x
  mutually cooperates with.
- **sibling** y = or(x, ψ_K) — x plus a dormant clause that fires only on an undecidedness probe; invisible to x.
- **arms**: weak (simulation, X and `ROLE`), **W0** (weak without X and `ROLE`), **L6R** (L_6 with X and `ROLE`),
  **M0** (modal with `BOX` only), modal (all four box kinds), priced, lazy, certificates-only, club, gate, contracts.
- **`ROLE`** — a public coin assigning roles each match; **X** — a private coin.

## Objects (DEFERRED.md 1)
- **mutation object** — π of the ε → 0 chain as N → ∞; selects on establishment + unfakeability.
- **seed lottery** — ε = 0, iid seeds from μ; P(efficient) along a path in (N, I); selects on establishment +
  compatibility among the establishers present.
- **τ_A** — the island's ALLC-extinction time (≈ 13–19 generations at N = 100–400, ∝ log N); **ghost** — a control
  lineage that plays as a faker but has fitness pinned to the population mean; **Λ_t** — a lineage's integrated
  relative fitness deficit; **Lemma 0** — box soundness at the evaluator's stable world.
- **κ** — compatibility index: P(mutual cooperation | two iid μ-draws are both establishers), denominator μ_est²,
  same-class draws counting as cooperation. **Incompatible pair** — two establisher classes that mutually defect or
  where one exploits the other; **consequential** if co-seeded with probability ≥ 0.01 at N = 400.
  **Anti-coordinators** — x(y) = y(x) = C and x(x) = y(y) = D; never establishers. **Unresolved incompatibility
  risk** — P(co-seed) × P(resolution fails). **Near-universal suckers** — `not(BOXD(THEM(^C)))`, `not(BOXD1(THEM(^C)))`.
- **Union game:** boss actions (s, h) with wage s ∈ {0, 1/4, 1/2} and whack policy h ∈ {strike targeting, none,
  source targeting}; **c** the per-whack cost, **L** = 1 the striker's loss; **scab** = work always; **militant** =
  strike iff s < 1/2; **union** = strike iff s < 1/2 and QUORUM; **QUORUM** = BOX(s < 1/2 → OTHER = strike);
  **union′** = the same with BOX(OTHER = strike), untagged and behaviourally identical; **wage faker** =
  `if(BOX(W_j = work), (1/2, ·), (s < 1/2, ·))`; summaries fair / intermediate / zero wage / strike / scab split /
  repression; **w_g^B** = island selection on the boss slot only; **polarity dilemma** = a strike pact needs □(low
  wage), which is fakeable, while □(fair) is unfakeable but cannot carry a pact.
- **sucker fringe** (carrier seeds) — non-carrier programs that cooperate with a carrier through contract reads while
  being illegible to it; **cross-lineage share** — the fraction of final carriers whose contract came from another
  lineage by swapping; **f\*** — the carrier frequency at which carrier fitness first exceeds the population mean.
- **Symmetric gate** (carrier seeds) — the access rule under which a non-carrier's box atoms about a carrier are
  gated like its atoms about anyone else (rc(t) = 1 iff t carries); the **asymmetric** rule lets every program read
  contracts (rc ≡ 1); **quenched q** — a fixed fraction q of canonical sources, nested in q, may read contracts.
  **Legibility shield** — the transient advantage an illegible defector has over a legible one against programs that
  cooperate unless defection is provable (`not(BOXD…)`); gone at the ε equilibrium. **f\*_net** — the deterministic
  carrier threshold net of contract stripping at finite ε (≈ 0.004 under the symmetric rule).
- **Rival islands:** **ρ_DD(N)** — fixation probability of one migrant of a self-cooperating class into an island
  held by a mutually-defecting self-cooperator (a symmetric coordination game; 1.85·10⁻⁵ at N = 100, barrier ≈ N·w/4);
  **bridge** — a class that mutually cooperates with both rival networks (`BOX1(THEM(THEM))` for the FairBot pair's
  heaviest rivals); **separated** — two certified islands at the horizon whose cooperative holders mutually defect,
  **ever separated** — at any time; **x = m·T_nuc = mN·T_nuc/N** — the expected replacement fraction of an island
  during nucleation, the control of the mN rule; **q** — local nucleation rate relative to m = 0; **T_nuc** — median
  per-island establishment time (45 / 70 generations at N = 100 / 400).
- **Demographic lemma:** **Φ_t** = 1 + ∫_0^t d·e^{−R}, with per-copy death rate d = 1 − ak/N, a = f_q/F̄, net
  rate r = a − 1 and R = ∫r; **Lemma D′** — P(k_τ > 0, Φ_τ ≥ φ) ≤ 1 − (1 − 1/φ)^{k₀} for any lineage and stopping
  time; **Lemma D** — the killed fixed-time case, survival ≤ k₀/(1 + d_min·T); **event clock / Poisson clock** — N
  events per generation versus events at rate N (same embedded chain); **r_q** — per-founder dependence correction
  E[N_q | A]/E[N_q] (≤ 1/P(A)); **r_env** — the part of r explained by the shared scramble duration; **h^rel** —
  relative harm; **K_τ** — pooled count of the largest mutually-cooperating establisher block at ALLC extinction;
  **u_N(k)** — exact escape of k pooled prover copies from a D sea; **c = w(R − P)** — the frequency-dependent
  advantage slope (0.3); **ℓ = E[k_τ]/k₀** — per-copy mean size of an establisher lineage at ALLC extinction
  (≈ 1.3); **κ_N** — concavity factor E[u(k_τ)]/(u₁·E[k_τ]); **p_corr / p_corr2** — the compound establishment
  formula with the curvature-only / full-seed mean-field scramble; **semi-empirical predictor** — E[u_N(K_τ)] from
  the measured state at τ; **pooled erf form** — p(N) ≈ erf(μ_est·ℓ·√(Nc/2)) / erf(√(Nc/2)).
- **Enforcement arms:** **CC / RC / CR / RR** — first letter the boss's whack, second the workers' strike; C =
  committed (program output), R = ex-post rational (best response inside the per-world evaluation, boxes on
  implemented actions); the wage is always committed. **Replacement pool** — a whacked striker is replaced by an
  outside scab paid s, the boss netting 1 − s − c. **Tie rule** at 1 − s = c: whack (declared) or nowhack.
  **militant⁻** = `if(not(BOX(s = 1/2)), strike, work)`; **union⁻_ℓ** = the same with `and(…, BOX_ℓ(OTHER = strike))`;
  **polarity faker** = `if(BOX(W_j = strike), (1/2, ·), (s < 1/2, ·))`, fair only while provably struck. **Threat
  advantage** — payoff of an executed (or if-called) committed enforcement move minus the feasible deviation.
- **Proof length:** **GLS+Def** — cut-free G3 GL calculus with definitional constants P_xy unfolded from the DSL
  source as written; BOXk(s) ↦ □(¬□^k⊥ → s). **L_C, L_D** — minimal sizes (in sequents) of ⊢ P_xy and of P_xy ⊢;
  **L_C¹, L_D¹** — the same with the Con antecedent ¬□⊥. **Λ** — number of GLR (Löb-rule) applications in a minimal
  derivation. **L_read(x, y)** — sum of the minimal sizes of x's true atoms against y; **L_out(x, y)** — minimal size
  of x's actual outcome against y. **Trichotomy** — C-provable / D-provable / neither. **K** — the bounded calculus:
  boxes carry budgets □_b, true iff K derives ⊢ A within b sequents; rules G3 + unfolding, BoxEq, Nec and
  **JLöb(S, b)** (|S| ≤ 3, side condition b ≥ 1 + Σ premise sizes); **T(A)** — minimal K size of ⊢ A; **x_b** —
  program x at budget b. **Copy threshold / distinct-budget threshold** — FairBot 3 / 4, `BOX1(THEM(ME))` 4 / 7;
  **soft clique** — a budget just above the copy threshold, cooperating only with copies. **Matched random control**
  — the free table with as many plays flipped at random per stratum (opponent class × free play × reader has boxes)
  as the K arm changes.
- **Divide-the-dollar partitions:** **S1…S5** — `dollar5` demand levels 1/6 … 5/6 (**L/M/H** in `dollar3`); arms
  **`role` / `norole` / `fixed`** — one population with `ROLE` / one population without / two slot populations
  without `ROLE` (N per slot); **ordered split a|b** — slot 1 demands a, slot 2 demands b; **benchmark** — uniform
  over ordered efficient splits (50–50 = 1/5, E[max share] = 0.70 in `dollar5`); **E[max share]** — expected
  maximal realized payoff per encounter (ex post); **ex ante max** — the largest class-mean payoff in the state;
  **normalized share** — d_i/(d_i + d_j) of a compatible match. **Accommodator** — plays 1 − d against a constant
  demand d (`flip(THEM(ME))`, `flip(THEM(THEM))`, `flip(THEM(^S_k))`); **accommodating shadow** — an accommodator
  on-path identical to a convention (`flip(THEM(^S3))`); **accommodator ratchet** — the fixed-role mechanism (a
  neutral accommodator in one slot, the other slot's largest demand invades strictly, the accommodator drifts
  back; endpoints swap with each other and absorb the walk); **greedy polymorphism** — the S5–accommodator
  Hawk–Dove mixture (S5 ≈ 0.67–0.75, efficiency ≈ 0.41) that absorbs one-population π at large N.
  **Partition-frozen** — the first check at which every island is locally closed; **escape** — an island locally
  closed on one convention and later on another.
- **Island path:** **boundary path** — mN(N) = 0.3·N/T_nuc(N) with T_nuc calibrated at m = 0 (45 / 55 / 70
  generations at N = 100 / 200 / 400, giving mN = 0.667 / 1.091 / 1.714); **q (holder form)** — horizon holders of
  local ancestry relative to the paired m = 0 reference; **propagule (k)** — k fitness-weighted offspring from one
  source island replacing k residents at once, mN/k events per island-generation; **stacking** — near-simultaneous
  propagules acting as one of size 2k; **bridge absorption / replacement / capture** — loss of a minority island to
  the bridge, to the majority network, or to an untagged class; **migrant-load advantage** — the bridge's edge on
  islands receiving the rival's migrants; **separation-loss hazard** — losses per minority-island-generation;
  **coordination barrier** — ≈ N·w·(1/2 − k/N)² for k migrants into a rival island.
- **K at n = 8:** **GL-erasure prune** — K ⊢ A implies GL+Def ⊢ erase(A), so the search skips contents whose
  erasure is not a GL theorem; **b\*_K(x)** — the smallest global budget at which x self-cooperates in K (FairBot 3,
  `BOX1(THEM(ME))` 4, PrudentBot 11; P\*, P2, PB2 and the level-2 ladder never at b ≤ 54); **PB2** =
  `and(BOX(THEM(ME)),BOXD2(THEM(^D)))`, GL-provable but needing the 4-axiom under a box; **faker-removal control** —
  the free table with the classes that strictly invade a supported self-cooperator in the free arm but not in K
  deleted (37 classes, μ 0.0029; 21 Gödel sentences, 16 probe readers); **analytic cut** — cut restricted to
  reachable boxed formulas and their contents; **DAG size, exact / subsumption** — distinct sequents of a derivation
  under exact identity, or counting a weakening of an already-certified sequent as a free reference; **price
  schedules** — per-match (c·b per match), **amortized** (c·b/N), **cache accounting** (c·b per distinct opponent class
  per lifetime), **lazy** (c·b only against non-constant non-copy opponents, with copy rules (a) identical budgeted
  program, (b) same source at any budget, (c) extensionally identical play); **N·Δ** and **fixation ratio N·ρ** on
  the decisive edge (≈ 1 + w·c·b/2 for the amortized ALLC exit).
- **Modal divide-the-dollar:** **P / P′** — accept / refuse certified greed (P′ = `if(BOX(S1),S5,S3)`: exploit a
  certified conceder, otherwise demand 1/2); **A5** = `if(BOX(S5),S1,S3)`, the one-atom accommodator; **G** — the
  S5–A5 polymorphism (2/3 S5, mean 5/18); **Löbian hawk** — `if(BOX_L(S1),·,S4)`, provably meek with its own copies;
  **deep state** — a recurrent state every exit of which is deleterious (barrier linear in N); **support twin /
  twin drift** — a payoff-identical relabelling of a deep state's members, reachable by free drift at rate
  1/(x_r N), which the lumped chain under-weights; **seeded log-domain chain** — the chain solved in the log domain
  with every deep polymorphism expanded, the instrument to use where deep states exist; **resistance to profitable
  certified demands** — the property P′ has and P lacks, distinct from unfakeability.
