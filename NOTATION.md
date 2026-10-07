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
- **K with the 4-rule:** **K+4 / K+4m** — K with the literal 4-rule Γ, □_a A ⊢ □_{a+1}□_a A, Δ / with its monotone
  closure (cases i–iv); **Lemma V** — the literal rule never fires on DSL formulas; **Lemma G** — PB2 needs bounded
  self-consistency at equal budgets (□_b⊥ ⊢ □_b□_b⊥), the second incompleteness theorem in bounded form; **guard
  convention / X-arm (`goff` = 1)** — whether BOXk at budget b reads ¬□_b^k⊥ (own budget) or ¬□_{b+1}^k⊥ (one up);
  **C_spec / C_pair** — the frozen trace classifier on the invader's play / on either play of the invasion;
  **G-trigger / C-trigger** — a used self-play Gödel hypothesis / a used Con statement under a box; **structural /
  finite-budget failure** — not K-derivable up to 2L + 10 / derivable at some larger budget; **restored
  cooperators / restored exploiters** — self-cooperating in K+4m but not K / strictly invading a supported
  self-cooperator in K+4m but not K.
- **Bridge-less rivals:** **pairwise bridge** of (A, R) — a cooperative class (self-cooperates, not ALLC) mutually
  cooperating with FairBot, `BOX1(THEM(ME))` and R; **safe bridge** — a pairwise bridge that is an establisher;
  **bridge mass** — the total cut μ of R's pairwise bridges; **τ** — a sensitivity threshold on the heaviest
  bridge (τ = 0 is the literal case, the right object); **prey** of R — a class that cooperates with R while R
  defects on it; **mediator** — a cooperative non-bridge class against which FairBot, `BOX1(THEM(ME))` and R all
  cooperate; **A-faked rival** — a rival some member of A strictly invades; **hard bridge-less mass** — rival mass
  with no bridge, no mediator, not A-faked (0.21 / 0.26 / 0.26 of rival mass at n = 9 / 12 / 13); **half-rival /
  full rival** — mutually defects with one / both members of A; **P\* family** — `and(BOX1(THEM(x)),not(BOX(THEM(y))))`
  rivals, cooperating iff cooperation is provable from PA + Con but not from PA, 0.98–0.99 of the bridge-less mass;
  **μ_bl** — the bridge-less rival mass; **p₁** — per-copy establishment probability of a rival (0.048 for P\* at
  N = 200); **mediation event** — a rival-network island strongly taken by a bridge class; **mediation-before-loss
  probability** — among runs in which the rival established, the fraction with a mediation event before a network
  is lost or the horizon reached (equal to the bridge's scramble survival); **q_est** — local establishments
  relative to the m = 0 reference, the nucleation statistic (holder-form q also counts later neutral replacement
  and is retired). Forced-rival labels **P\***, **P\*′**, **S\***, **B₁**, **H**, **B₄** as in RESULTS.
- **Rivals under K:** **direct bridge / direct-bridge-less** — the pairwise bridge of (A, R) / none; **mediator path**
  — a path of length ≤ 3 from R to A in the establisher mutual-cooperation graph; **zero transition / below
  threshold** — one-migrant fixation exactly 0 (empty under the kernel) / below 10⁻¹²; **new rival by source** — a
  canonical source that is a rival under K's table and not under the free table; **lumping validity** — identical
  directed rows and columns within each class, preserved masses and seed law, and agreement of establisher, rival
  and bridge tests between lumped and source tables; **common mN** — the free arm's calibrated boundary value
  (1.091 at N = 200, n = 8) used for both tables; **tracked lineage** — forced founders followed as a tagged
  duplicate column with no dynamic effect; **cooperative establishment / lineage survival** — an island certified
  cooperative with the lineage as holder / the lineage present at the horizon; **inert-defector control** — one D
  founder per island under the same replacement rule; **budget soft-clique rival** — a rival created by a budget
  below a pair's distinct-budget threshold (FairBot vs `BOX1(THEM(ME))` at b = 4).
- **K with cut:** **K_c / K_c4** — K + Cut + UnfId + Dist (bounded K-rule: from A₁…A_k ⊢ B infer □_{a_i}A_i ⊢ □_d B
  when d ≥ s + Σa_i + k) / + Dist⁺ (bounded K4-rule); **UnfId** — Γ, P ⊢ φ(P), Δ; **lemma cut / MP** — the Lemma C
  witness composition; **extension model / structural certificate** — a model refuting a sequent in every extension
  of the calculus by witness-composing rules (Theorem E; Lemmas E1, E2: every such rule puts its conclusion at least
  two budgets above a budget-b hypothesis); **targeted table** — K's closure plus certificates, then the K_c search
  on uncertified misses only; **long guard** — the level-k guard read at 2b + 8 (a reflection margin of about 2b),
  the one switch that returns P\* and its fakers together; **long-guard graft** — family plays grafted into K's
  table for a descriptive chain.
- **Solver audit:** **deep: strict / modulo twins / with penalty only** (tolerance 10⁻⁹) — every outside class has
  invasion fitness below the resident mean by more than 10⁻⁹ / every outside class is strictly deleterious or a
  payoff twin of a member / no outside class is advantageous and every first-order-neutral non-twin class loses at
  second order; **invasion closure** — the saturated rest points reached from the monomorphic states, and from
  enumerated candidates with two branches, by repeatedly adding a strict invader at 10⁻³ and running the replicator
  to rest (N-independent, no chain probabilities); **θ_log** — the log-domain threshold on π-weighted relative
  inflow into an unexpanded state; **G4** — the `dollar5` greedy polymorphism (S5 3/4 with three accommodators);
  **R5** — the `dollar5 role` five-class hawk polymorphism (`max(S4,ROLE)` with four accommodators); **H5** — the
  modal-dollar twin-expanded five-class S4-hawk polymorphism; **W** — a strictly invadable state made sticky by the
  lumped polymorphic-target fixation; **establishment floor** (diagnostic) — the fixation probability of a
  first-order-advantageous invader floored at 1 − e^{−wd}; **`chain_log.LogChain`** — the audited solver.
- **The social organization game** (RS, 2026-10-06) — the name for the boss/worker family of fixed-role games with a
  monopoly on force (wage, strike, repression, replacement pool); "the union game" names only the 2026-10-05 run of
  it with the QUORUM atom, and "the enforcement run" its commitment ablation.
- **Social organization lottery:** **strike-whacker / any-whacker** — a boss class realizing a whack on a constant
  striker within {scab, striker}² / additionally on {militant, union}; **early decline** — the strike-whacker share
  at generation 0 minus its minimum over generations 0–100; **closure-verified (global play-key closure)** — every
  slot's globally present classes give the same (a₁, a₂, whacks, paid wage) against all present combinations,
  which implies one play everywhere; **island wage / wage patchwork** — the offered wage with the most
  working-encounter mass / ≥ 2 island wages in a run (possible only at mN = 0 under global closure); **three-role
  distribution threshold** — the fraction of positive-surplus islands with minimum role share ≥ 1/6, reachable
  only at the fair wage since a both-working island pays (2(1 − s), s, s); **refuser** —
  `if(BOX(s ∈ {0}), strike, work)`; **xref / xmil seeds** — the constant striker's prior mass moved onto the refuser
  or the militant; **phantom slot** — the single-worker variant's frozen W₂.
- **Realizable language:** **L_T** — the untyped call-by-value de Bruijn λ-calculus with quoting, `prove_b`, `run_k`
  and a step-counting evaluator; **K_T / K_T⁻** — its bounded calculus with / without JLöb; **⟨σ⟩⇓a** — a
  configuration atom, with plays(⌜p⌝, ⌜q⌝, a) := ⟨p ⌜p⌝ ⌜q⌝⟩⇓a; **ρ(σ, a)** — the reading ⊤/⊥ at terminal states;
  **EvR/EvL, PrvR/PrvL** — evaluation and prove-step rules; **box obligation** — the □_c ψ owed on the not-found
  branch of a prove step; **A ≻_k B** — B is k deterministic steps downstream of A (BoxEq along chains); **idealized
  vs actual evaluation**; **primitive-assisted / search-charged** charging; **W(ψ, b)** — search work in node
  expansions; **found / refuted / timeout**; **sim frame, TO**; **Lemma W_T, Lemma U, merge**; programs **FB_b,
  FB1_b, PB_b, G_b, P\*_b, SF_k, SC_b, Vlet_b, Vwrap_b**; **b\*** in L_T: FB 8 (distinct budgets 12), FB1 13, PB 25,
  Vlet 9, Vwrap 11; **simulator leak** — a sound reader's true idealized proof about a simulator, exploited by the
  simulator's fuel-limited run under search-charged charging.
- **Prover as code:** **L_T^code** — L_T without prove/sprove/mk/fv, plus arithmetic, `capk`, `lib`/`libsrc`;
  **SEARCH_i / CORE_i** — the search wrapper and core in the library (i = 0 sound, 1 sloppy SC_code, 2 sound without
  JLöb^self, the control); **U** — a search's declared cap, u = U + 7 its maximum cost; **⟨σ, f⟩⇓a / ⇓⁺a** —
  fuel-indexed exact and monotone atoms; **⊡^U_{c,i}ψ** — "the code search CORE_i on (c, ψ) returns T within U
  steps"; **K_T^code** — the calculus (Ax, G3, EvR/EvL, SrchR, Run/RunNeg, JLöb^self); **SrchR** — the search-call
  rule with the static fit condition (every counter ≥ u) and minimal-residual readings; **Run / RunNeg** — a box
  verified by running its core, never on the root call; **JLöb^self** — the self-fulfilling Löb rule (hypothesis =
  the root call's own box), sound ex post (Theorem S^code); **root call** — (ψ₀, b, U, i); **Run regress** — mutual
  verification re-entering the reader's own query, costing U + 1; **regress lemma** — the evaluator fast-forward;
  **matched / mismatched certified target** — the reader's proof names the fuel the target actually ran with, or
  not; **static boundary** — k = U + 10 for FB vs SF_k; **FB2** — the visibility probe; **FBx** — the
  mismatched-target reader; **twins** — programs whose search calls are the same root query, the only pairs that
  cooperate under the code semantics.
- **Certificates as code:** **script** — a derivation skeleton (rule names and principal-formula positions) the
  checker expands from a root built out of the two quotes; **Lemma F** — a carrier's explicit self-derivation is
  not finite data; **CHK / CC_x** — the check wrapper and core, modes x = 0 sound, 1 naive (unguarded pair rule),
  2 none (control), 3 self-only, 4 sloppy, 5 sound copy at another entry; **V** — the check cap, u(V) = V + 6 the
  check's maximum cost, W its actual inner steps; **K_T^cert** — Ax, EvR\*, ChkR, Run/RunNeg (cap ≥ root), Hyp^self,
  Hyp^pair; **R** — the box of this check (its root); **S** — the swap, the checked program's own check of the
  reader's script; **Hyp^pair** — closes S, guarded by partner validation; **Lemma N** — nested runs return their
  clean values or the root times out; **Lemma Sym** — reader's and partner's checks compute the same two validations
  and agree; **Theorem S^cert** — unconditional soundness of modes 0, 2, 3, 5; **call skeleton** — the sequence of
  check calls a source makes, the coverage class of a script; **carriers** CB (FB-shaped), CB1 (self-auditing),
  CBP (prudent), CBlet, CBwrap; held-out CBlet2, CBw2, CB1h, CB1r, CBPh, CBPr; **Ccert** (C with an acyclic script),
  **Dcert** (D with cyclic scripts), **CBfake**, **CBdef**, **CBmut**, **LöbC** (self-trust: a certified
  CooperateBot), **CBsloppy**, **CBN / CBN0** (naive, with and without a list), **CB0** (sound, empty list),
  **CBS2** (sound copy entry), **SFc** (certificate-carrying simulator).

- **Probe atom** `BOX_L(W_j(^(s,none)) = a)` (concessions) — worker j's executed action against the quoted constant
  boss (s, none), beside the current encounter's other worker, boxed on the quoted encounter's own world chain (true
  at world n iff it held at every world in [L, n)); level L ∈ {0 (PA), 1 (PA + Con)}; executed = after the arm's
  enforcement rule (RR: per-world rational override, ties to the committed recommendation).
- **P₀ / P₀₁ / sham / mass-preserved reference** — boss grammars: base atoms plus the zero-wage probes / plus probes at
  0 and 1/4 / P₀₁'s function list with every probe a literal constant at every world / P₀₁'s prior with probe-carrying
  functions nulled. **Mass-preserving substitution** — chain language = the n = 11 grammar's constants and one-atom
  functions plus named two-atom classes, each class carrying the n = 11 mass of every function with its behaviour; the
  remaining two-atom policies are null mutations.
- **T₀** = `if(BOX(s ∈ {0}),strike,work)`; **T₁** = the militant; **T₀⁻** = `if(BOX(s ∈ {1/4,1/2}),work,strike)`.
- **D₀** = `if(BOX(W1(^(0,none))=strike),(1/2,none),(0,none))`; **D₀q** the same paying 1/4; **D0[L1]** with BOX1;
  **D14** = `if(BOX(W1(^(1/4,none))=strike),(1/2,none),(0,none))`; **D\*** (full price discriminator) = pay 1/2 iff
  provably strikes at the 1/4-boss, else 1/4 iff provably strikes at the 0-boss, else 0; **D\*[L1]** with both probes
  BOX1; **D\*_j L_{a}{b}** its eight variants (slot read, probe levels). **C₁** = `if(BOX(W1=strike),(1/2,none),(0,none))`
  (the current-encounter concession; a world-0 wage faker). **Probe wage faker** =
  `if(BOX(W1(^(0,none))=work),(1/2,·),(0,·))` and kin. **Concession boss** — a probe-carrying boss paying 1/2 to the
  militant pair and 0 to the scab pair.
- **F\*** = (D\*, T₁, T₁); **F\*⁻** = (D\*[L1], militant⁻, militant⁻), the unfakeable fair state.
- **Accommodation ratchet** (sol) — a worker that strikes only at lower wages enters neutrally beside a discriminator
  that pays it the same, after which a lower wage strictly invades. **Preservation of demands** (sol) — for a fair
  state, the set of neutral worker substitutes and whether a demand-lowering one opens a strict boss move; reported as
  the fair π-fraction with a demand-lowering neutral substitute, and with one after which a boss strictly invades.
- **Basin-to-basin rate** k[A→B] — Σ_{i∈A} π_i Σ_{j∉A} q_ij h_B(j) / π_A per mutation event, h_B the hitting probability
  of basin B before any other basin; basins by outcome summary (fair, 1/4, zero wage, whacking); residence = 1/escape.
- **Fair island** (lottery) — locally closed with play (1/2, W, W) and no whack; **establishment** = first check with a
  fair island; **persistence** = fraction of islands fair at the stop. **Militants in numbers** — seeds with the
  constant striker's prior mass moved onto T₁ (or militant⁻).
- **Mixed budgets:** **source@b** — a budgeted establisher (a genotype of K's catalogue with its own budget);
  **incompatible pair** — two establisher classes that mutually defect, the screening unit; **structural bridge** —
  a class in the catalogue cooperating with both members of an incompatible pair (prior-present if its prior mass is
  positive); **copy threshold** — the smallest b at which source@b self-cooperates with its own copies at other
  budgets (FairBot 4, `BOX1(THEM(ME))` 8, PrudentBot 16); **cheap-heavy / uniform / above-threshold priors** — budget
  priors (0.6, 0.3, 0.1), (1/3, 1/3, 1/3), (0, 0.5, 0.5) over {4, 8, 16}; **composition distance** — TV between the
  island-weighted budget composition of strong cooperative holders (≥ 0.9 of an island) and the prior, at the first
  checkpoint after every island is established and at the horizon; **A₁₆** — the above-threshold rivals of the b = 16
  core (secondary statistic); **resolution hazard** — resolutions per separated run-generation.
- **Guard trait:** **genotype (s, g)** — a source plus its guard offset g ∈ {0, L} (read Con at one's own budget,
  or 2b + 8 up); **guard twin / neutral guard mass** — an (s, L) whose row and column match (s, 0)'s, and the π on
  such genotypes; **active guard mass** — π on non-twin (s, L); **near-twin** — an active (s, L) whose four encounter
  payoffs equal (s, 0)'s; **allocation** — the label-L share of the π of twin pairs (exactly the prior under the
  joint kernel); **joint / separate kernel** — a mutant redraws (s, g) together, or changes one trait with
  probability ½ each; **sham bit** — a label that changes neither proofs nor costs; **Lemma H** — the high-budget
  certificate (GL ⊢ ⊡E → □⊡E); **Lemma Cap** — values ≤ b are exact at cap b; **JLöb sibling closure** — an instance
  concludes every member of S; **relevant content / tiered residual** — an uncertified content in a pair whose play
  is undecided under three-valued evaluation, and the μ of the unsearched part; **cross-guard soft clique** — same
  source, different guards, mutual defection below a cross-guard threshold (PrudentBot: 20).
- **Carrier populations (milestone 2):** **template grammar** — `C | D | if(B, A, A)` over check atoms
  `CHK_e(p, q, a)` under `not/and/or`, cutoff n = 7; **arms** P (public production) / O (optional, one node) / E
  (entry label, one node for `CHK_5`) and **priors** L (2^−nodes), U (uniform over classes), L_std (the repo's
  Elias-gamma μ); **τ-type** — spellings with the same run tree and certificate list (Lemma T: interchangeable up to
  quote identity); **S-guarded establisher** — every path to a C leaf passes a true "them certifies cooperation with
  me" atom (Lemma G: no strict invader); **defection detector** — an establisher that cooperates unless the opponent
  is certified to defect against a constant, exploitable by certificate-less defectors; **TwinD** — the twin clique
  `if(or(CHK(me,me,D),CHK(me,them,D)),D,C)` and its nine 7-node spellings: cooperate iff the opponent is one's exact
  source, by the R/S coincidence (Run/RunNeg forbidden on the root box), drift-closed; **Bor** —
  `if(or(CHK(them,me,C),CHK_5(them,me,C)),C,D)`, the unexploitable bridge across checker entries; **E1 / E2 / E3** —
  lottery endpoints (every island monomorphic and resolved / one-step reading / polymorphic islands allowed,
  resolved cooperating iff every class in the closure of present entrants self-cooperates); **ExactHost** — the
  host replay with dependency-tracked regress detection; **FastChain** — closed-form two-type fates in monomorphic
  states (equals `LogChain` on the P cells); **no-clique control** — the chain with the ten closed classes removed
  (not preregistered).
