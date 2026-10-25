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
- **Gene** (RS, 2026-10-11) — the broader name for a certificate or contract: a declared modification of a program's
  behaviour at special-cased points (a quorum strike, a carried derivation, a committed threat); **credible gene** —
  one whose execution is ex-post rational at the point it fires (DEFERRED 12); **spontaneous generation** — a gene
  arising on the spot as a credible deviation from an equilibrium condition, modelled as a structured mutation
  kernel from a declared prior.
- **Identity and tags:** **`eq(me, them)`** — structural quote equality, one node; **marker ^t / `tag_t(them)`** — a
  no-op let around the body (one node) and the atom reading it; **⌜CB⌝** — the named quote inside check atoms (an
  identity channel: it certifies only against the exact CB quote); **EQ** — `if(eq(me,them),C,D)`, the one-line
  identity clique; **TC_t / TC_t^t** — the tag club without / with its own marker; **MC^t** — the marked carrier (CB
  with marker t), the non-exploitable bridge between CB and the tag club; **AF / OF** — the and-form and or-form
  tagged carriers (not a bridge / an exploitable bridge); **XC** — the exclusive club (certified cooperation with me
  and certified defection against ⌜CB⌝), bridge-less by soundness; **τ′-unit** — a τ-type modulo markers (Lemma R:
  a check depends on markers only through the tags read); **exact-identity clique** — a pairwise-compatible set of
  one class; **F_CB, M** — the heaviest pairwise-compatible set containing CB and its pooled mass; **holder / held
  island** — an island's majority class and the islands it holds (the endpoint under migrant load); **islands per
  seeded copy** — held islands per seeded copy of a label; **seed payoff** f = U·μ — expected payoff against the iid
  seed, the scramble diagnostic; **universal-open** — a run in which the open carrier family holds every island.
- **Prudent openness:** **CBP** (this run) = `if(and(CHK(them,me,C),CHK(them,⌜C⌝,D)),C,D)`, the prudent open
  carrier (distinct from milestone 4's probe, now **CBP₄**); **⌜C⌝ vs Cc** — the certificate-less constant against
  which S-guarded carriers certify defection, vs the catalogue's certificate-carrying unconditional cooperator;
  **F_P / F_P^pr / F_P^n** — CBP's frozen family (the heaviest maximal pairwise-compatible set containing it), its
  prudent core and its nice part; **F_X, XB** — the exclusive club's family and its one bridge to CBP; **m, m_L, m\*** —
  identity seed mass, its value under L (9·10⁻³, 57 copies per run at (100, 64)), and the 50% crossing of the
  universal fraction (the abundance threshold); **f₀, q** — the clique-free baseline and the per-copy persistence
  rate in f ≈ f₀·e^(−6,400·m·q); **established islands per occupied seed island** and **persistence** — the stage
  statistics (arrival → establishment → persistence → spread).
- **Social organization, realizable:** **K₃ / CHK3** — milestone 4's checker on three-quote roots, argument
  (V, encounter, subject, outcome set, K); **encounter box** — a box about one run of the three-player encounter;
  **closure Φ** — the set of boxes a check validates after closing any box of the same encounter by Hyp; **Lemma
  Sym₃, Theorem S^cert₃** — the symmetry and unconditional soundness for three-quote roots; **path tactic** — the
  frozen production driven by assignments (Hyp only for worker–worker boxes); **boss view β** — the boss's probe
  reading; **concession boss** — pays ½ to the T₁ pair and less to the scab pair (0.184 of the boss prior under L);
  **WF\*** — the synthetic faker re-injected at the modal faker mass (0.0116); **uncertified default** — the play a
  program falls to when no certificate applies; **L / U / X priors** — 2^−nodes over library spellings / uniform
  over classes / 2^−nodes over the matched expanded syntax; **founding-coalition mass** — Σ over fair, strict-
  invader-free (boss, worker, worker) class triples of the product of their masses.
- **Fixed-role chicken:** **chicken / hd3 / hd6** — the three payoff tables (Straight, Swerve); **R1 / R2 / crash /
  dove / mixed** — outcome classes by play at tolerance 0.95; **bridge (anti-coordination)** — a conditional
  straight, Straight iff the opponent would swerve; **firm** — Straight against both constants; **soft commitment**
  — firm against constants, swerving against readers; **f\*** = (S − P)/(T − P), the bridge share at which the
  loser's Straight wins the seat; **Lemma F** — within a role selection is constant, so the two-population chain is
  monomorphic on K² pairs; **W0 / M0** — the matched weak/modal pair on one grammar and prior.
- **RC = rational commitment** (RS, 2026-10-11): the enforcement arm with the boss's enforcement ex-post rational and
  the workers' quorum strike committed (RESULTS "Incentive-compatible enforcement"); **reciprocal credible gene** —
  a gene whose trigger is a certificate about the opponent's play in the encounter and whose override is ex-post
  rational when it fires (DEFERRED 12; the gene run's arm G-recip).
- **Gene arm:** **gene (τ, o)** — a special-case clause `if(τ, o, ·)` placed ahead of a parametric base; the first
  firing gene wins; it fires at world 0; 5 nodes; **Q\*** = BOX(s ∈ {0, ¼} ∧ OTHER = strike), the gene arm's quorum
  atom; **arms** G-all (every gene admissible), G-cred (the per-point override filter), G-cred-whole (the RR execution
  rule applied to the whole program), G-asym (no boss whack genes), G-recip (reciprocal triggers passing the filter),
  random (removal of as many genes as G-cred removes), -ctl (bosses restricted to h = none); **continuation best
  reply** — the per-point test with others' actions held fixed; **mutant-program best reply** — the whole encounter
  re-evaluated with the carrier's program replaced; **gene-stable** — strict: no admissible gene strictly improves its
  carrier; weak: none weakly improves its carrier and strictly improves someone; **SG** — the mutation kernel proposing
  the best-reply gene on each trigger true in the stable play with probability ½; **C₁ as a gene** =
  (BOX(W1 = strike), wage ½), the world-0 wage faker; **ε\*** — the mutation rate above which the coalition kernel is
  faster than the sequential path; **on-path execution rate** — the fraction of encounters at the top states and along
  lottery trajectories in which a gene's override is actually executed.
- **Certificates as genes (milestone 5):** **gene triple** (code, mode, list), the mode a no-op marker in the quote;
  **modes** H (host tactic, free) / S (PROD, the tactic as code, cap P = K/4, run after the play in the residual
  budget) / C (copy-and-check against one's own would-be self) / CS (copy, then search); **PROD / PCORE** — the
  tactic as an L_T^code term (cost ≤ P + 5); **AC(x, s, a)** — the would-be-self adoption check (current list plus
  the script); **lack rule / gate rule** — act on an outcome only while the list lacks an entry of it / one's own check
  against each partner; **unit** (τ, Cseq, Dseq) — run tree × C block × D block, the population state; **signature**
  — (box values F/T/TO, R, S, self flag), the key of production outcomes; **Lemma A** with failure points **F0**
  (fuel allocation), **F1** (list-dependent boxes), **F2** (first-valid order), **F3** (cost), **F5** (missing genes);
  **transfer graph** — the directed graph of (donor list, copier run tree) pairs whose script validates; **host
  ancestry** — whether a held script descends from an H-produced one; **CF** — the copied-script faker (D code in
  mode C); **self-play-only script** — `EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Ax] · Hyp]`, valid only at R = S, minted
  when a producer's first partner is its own copy.
- **Provenance:** **provenance rule** — which partners a program may write its first C certificate against and how
  it chooses among candidates; metadata, not part of the quote; **S-nonself** — produce the first C certificate only
  against another spelling; **S-self-delayed** — produce against the actual partner, self included, at encounters
  where an independent shadow draw is non-self (the timing control); **S-k / S-3 strict** — a window of k
  source-distinct partners, keeping the earliest candidate own-side valid against two, else the earliest admissible
  (the fallback); strict has no fallback; **own-side validity (OSV)** — the candidate's derivation closes at the root
  with the partner's side assumed; **self-play-only (SPO)** — a (run tree, C script) pair valid at a self-play root
  and at no distinct-quote root; **ι** — `EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Ax] · Hyp]`, the identity script;
  **only-self class** — the 97 run trees (mass 0.018) whose only producible C script is the self-root one; **TwinD
  family** — the seed's self-reading identity cliques (μ = 7.1·10⁻⁴, 4.6 copies per run at (100, 64)); **settled /
  futile individual** — one whose encounters cannot change it, skipped exactly by the kernel.
- **Stable sets on islands:** **R** — the 20 realizable payoff vectors of `dollar3`; **V\*** — the symmetric stable set
  (the three fair pairs); **M / C / P** — strict majority dominance / commitment with credible every-best-reply
  response / the ecology's programmed single-slot response; **G6, G8 (=)** — classical grids of step 1/6 and 1/8 (the
  efficient subsets); **R6x, R8x** — the constants extensions with unequal grand coalitions; **Lemma G** — exact
  discriminatory lines are never externally stable on a grid; **Lemma I** — C is outcome-invariant; **member
  occupancy q** — the fraction of islands on V\*; **coverage** — all three members held somewhere; **strong / weak
  form** of the RS's claim — island support ⊆ a stable set / coverage; **member-mixed / other-mixed** — an island
  below the 0.95 tolerance with ≥ 0.95 of encounters on V\* / otherwise; **held class** — ≥ 25 consecutive
  generations; **flip triggers** — pure drift, drift-prepared, two-slot coincidence, conditional, single-slot strict;
  **TU vs game effectiveness** — the two effectiveness notions for farsighted sets.
- **Dominance contracts:** **κ = (S, a_S)** — a pair contract, a winning pair and a demand pair installed as a heritable override; **ν** — contract events per island-generation; **β** — installed fraction (β = 1 atomic, containing relation M on homogeneous islands); **r** — the refusal bit (refuses exits from V\*); **menus F / G** — all 27 contracts / contracts carried by living individuals (ε = 0); **consent variants public / private / blind** — a drawn refuser vetoes for its slot / each refuser opts out alone / the bit is inert; **Q** — the proposal generator (a uniformly drawn pair-dominator with probability n(y)/27); **β\*_static / β\*_flow** — joint-entry thresholds for immediate fitness / for the kernel's flow; **modal-play occupancy** — islands whose argmax outcome is a member, beside the 0.95-classified occupancy; **immigrant rescue** — atomic contracts keep immigrant refusal bits on moving islands.
- **Social organization game, fully realizable:** **S-nonself₃** — production refused for a worker whose co-worker has its source, bosses never; **S-opp** — refused only against the opponent (no worker gate here); **EQS(q₁, q₂)** — equality of two quotes' sources with certificate lists stripped; **`EQ`, `N1`, `N2`, `EQW`** — worker "my co-worker is my source", boss "w_j is ⌜T₁⌝", boss "the two workers are one source"; **sham** — a one-node identity atom with equal steps that reads false; **U_eq, XM, B_eq, B_id** — the greenbeard union, the exclusive militant, the closed shop, the identity boss; **identity-blind prior** — the prior law of behaviour does not depend on the identity atoms' values; **futile retry** — a production attempt repeated at every encounter under the lack rule for a script that does not exist on the program's path; **scramble-fair** — an island fair at founding without a coalition.
- **Farsighted refusal:** **g0, gV, g1, g1-x** — accept every dominating contract / the hand-written veto on exits from V\* / one-step exposure (below y_i; below x_i); **gKR(δ)** — Konishi–Ray consent, accept iff W_i(x) > W_i(y) at the default fixed point; **gKR-read(δ)** — the plug-in, lagged reader re-solving under the island's guard composition; **gKRu** — a KR guard at a rotating-triad fixed point; **W_i(y)** — discounted value per contract event; **A(κ, y)** — joint consent; **default (frozen rule)** — simultaneous best responses from the myopic policy, then asynchronous, then minimum Hamming distance; **rotating triad** — the recurrent class {(4,2,0), (0,4,2), (2,0,4)} and its mirror.
- **Leader-value core sweep:** **E_C(a_S)** — the complement's response set given S's commitment; **ind / coord** — followers as individuals in Nash equilibrium / as one coalition; **pess / opt** — S facing the worst / best follower equilibrium; **ε\*** — the least-core value (empty iff ε\* < 0, **tight** iff ε\* = 0); **v_sim(S)** — the simultaneous-partition (γ) worth; **v_F(S), FMA(S) = v(S) − v_F(S)** — S's payoff moving second, and its first-mover advantage; **follower dominance** — followers earn at least the leaders per capita at S's leader outcome; **B_S(z), B̃_S** — the NTU blocking margin and its weighted bound.
- **Legibility at founding:** **L1** — the founding pass (each founder runs S-nonself₃ production on M = 10 non-self triples against a frozen empty-list snapshot); **L1-withheld** — the same lists delivered at generation 10; **L2 / the mark** — a NONE-only negative cache keyed on the program's type, the set and every encounter value production reads; **mark-sensitive production** — a production whose outcome a mark would change (none in 3.4·10⁷); **generation-0 yield** — the fraction of seeded coalitions certified and fair at founding.
- **Realizable scaling:** **T_ext** — the main cells' horizon, 10,000·I·N^0.3/(64·100^0.3), capped at 40,000; **calibrated mN** — (N/100)^0.7; **c** — seeded TwinD-family copies per run; **q_c** — per-copy universality cost in f = f₀e^(−q_c c); **ē, q_fail** — mean fraction of islands at P(C,C) ≥ 0.95, and 1 − ē (not the island-path q); **whole-run scramble failure** — an all-defect metapopulation in which no establisher survived; **proportional control** — TwinD founders redrawn from the non-identity prior ∝ μ; **crossed panel** — the TwinD count fixed at c; **static absorbing check** — labels absorbing / coordination / bridged / reachable bridge; **ρ_N(Z→X)** — the exact two-type fixation probability under the kernel's step.
- **Removing rivals:** **𝒯, uot** — the target (holders mutual with PrudentBot's H unit and pairwise mutual; 235 units) and universal-on-target runs; **closed-open / exploitable / identity** — rival labels (open S-guarded non-prudent holders neutral through FairBot; certificate readers with a predator; identity cliques); **predator** — a unit the rival cooperates with that defects against it, does not cooperate with its own copies, and is defected against by the target; **μ(Pred_X)** — accessible predator prior mass (empty-list arrivals); **εN** — fresh founders per island-generation (seed rain); **drift / shadow colonization** — a rain lineage reaching ≥ 0.5 of an island while neutral or deleterious at arrival / a neutral one on a target island; **exploitable shadow** — a target unit that an identity holder exploits.
- **Pangaea:** **Pangaea** — one well-mixed population of N·I; **μ_net** — the prior mass of a mutually compatible establisher network (≈ 0.028 for the FairBot network); **AP** — `if(CHK(them,^D,D),D,C)`; **fission–fusion** — islands for T generations, then merged into one population; **nested founder partition** — one founder list per replicate cut into every geometry of a total; spelling classes D, Dill, S, S−, PBn, CBo, BR, APn, TW as in `notes/pangaea.md` §1.1.
- **Coverage components:** **canon(t, A)** — S₃'s canonical script for set A, produced at the default root (every box and identity atom false); **S₃^static** — PROD3's path-free range under the gate; **(a) untravelled, (b) second paths, (c) identity-true, (d) gate copies** — the partition of H \ canon; **plus X / minus X** — X granted with production on top / H \ X with X barred; **complement control** — a count-matched draw of non-canonical scripts from outside X; **pivotal script** — a held script whose removal changes a nucleus's fair play; **per-root lack** (proposed) — attempt a set whenever no held script for it is valid at the current root.
- **Annealed mutation:** **A** — arrivals per island, N·Λ_N; **t₀** — the schedule's time scale (N/2); **K** — cure exposure A·ρ·μ_pred; **AP / DET** — the anti-punisher and certified-defection-detector rival classes; **drift-free run** — no drift colonization over the horizon; **identity prey** — a target holder exploited by a fresh TwinD founder; **scramble rescue** — a whole-run scramble failure recovered by re-injection.
- **Identity-resistant target:** **E / Res** — exploitable and resistant target spellings (165 / 70 of the 235 units); **𝒬** — the identity challenge set (21 units); **uot₂₃₅ / uot₇₀** — universal on the full or the resistant target; **Rm / Rp** — R-move (exploitable target mass moved to resistant members) and R-proportional (moved to all non-identity units), diagnostic priors; **κ** — composite takeover per identity arrival; **the guard** — cooperation requires `CHK(them,me,C)`.
- **Legitimate detectors:** **Key** — script node 27, a script valid only at roots whose opponent's bare source equals its key; **bare(q)** — a quote with its certificate list stripped; **world L / world K** — the stored convention / hypothesis-closed D certificates keyed to the partner they were produced against; **DET** — gentle own-D readers (the certified-defection detector family); **PBN** — the PrudentBot network; **grudge Key_k[δ]** — a keyed copy of the holder's own D-step script, written after being defected against while cooperating; **KG / KGh / KGs / KGp** — vertical grudges / plus horizontal copying / sham / prewritten; **anti-gentle member** — a PBN member that exploits or punishes gentle readers.
- **Per-root production:** **R0 / R1 / R2 / R3** — S₃'s lack rule / per-root lack (attempt a set whenever no held script validates at the current root) / R1 plus shadowed alternatives / R2 with a capped list of bundles; **PROD3A** — PROD3 plus the shadowed F-branch alternative, written before its primary; **SELFVAL** — validation at the root as code; **valid at the root** — accepted by the checker at the current root with hypothesis nodes as hypotheses; **list-free mark** — the negative cache keyed on (role, spelling, set, root); **bundle** — a primary script with its alternative; **thrash** — re-production of evicted scripts each time their root returns.
- **World K as implemented:** D-step certificates keyed to the literal ⌜D⌝, live against no population member (self-certified defection off in play); **former TwinD family** — L's Q, tracked under K; **minted C-identity class** — 10 run trees (μ 0.00195) minted by self-play production, untouched by K.
- **Hooks (Part W):** **`HOOK(t, a₀)`** — a one-node hook with tag t and default a₀; **fill** — (tag, scope, key, action, origin); scopes **none, role, history** (keyed on the partner's founder lineage), **behaviour** (keyed on three PA boxes: the partner's play against ⌜C⌝, ⌜D⌝ and me); **inert discipline** — disabled fills held, inherited and written but never applied; **grammar-dilution effect** — the shift from the no-hook baseline to inert hooks; **lineage-closed island**; **threat fill held / challenged / executed**; **leaky vs strict source ablation** — copies relabelled vs provenance-preserving copies.

- **Coalition-proof auctions:** **surcharge rule** — minimum-revenue core payments w.r.t. reports, VCG-nearest (LP then QP); **R1 / R2** — singleton / coalition complement responders; **T-strict / T-weak / T-weak-literal** — response tie rules (closest to truthful in L1 over the strict-improvement graph; worst for the deviators over the any-best-reply graph; worst for the deviators over the strict graph); **notion-robust** — no proper bidder coalition profits under a rule, mode and tie; **mixed coalition** — a winner with a loser whose report sets the winner's price (a ring); **grand ring** — the whole bidder coalition's best joint report; programs **`T`, `SH`, `PAIR`, `PAIRU`, `POL`** (truthful; singleton best reply to truthful others; enforced pair deviation; unenforced; police, the spiteful best reply to the items' intended bids); **reading audit** — reading programs replaced by their non-reading default; priors **U, S, M**; **tested** — a deviating pair present after `POL` became P's only program.
- **Hooks follow-ups (weak wing):** **open key p** — the partner's predicate "provably cooperates with me", evaluated with both parties' fills in force; **open promise / grudge / thanks** — fills (t, open, p = 1, C), (t, open, p = 0, D) and the written thanks on observed p; on `HOOK(t, D)` the open promise is FairBot; **demand-s fill** — a worker fill "work iff the boss provably pays at least s"; **union contract** — the two workers' joint demand pair; **(M) / (C)** — myopic / credible-response acceptance; **boss response fill**; **protected fill** — a contract-origin fill only a later accepted contract may overwrite; **raise / taming** — an accepted demand above / at or below the pre-contract wage; **sucker rate**.
- **Rediscovering the core:** **`PRU(c)`** — the responder: best reply in expected payoff to the others' resolved bids (ties to the lower bid, the seller's random tie counted), else default c; **evaluator order** — the role order in which responders resolve (P, A, B; reversed; order-free); **eroded** — island revenue more than one tick below the minimum-revenue core; **core / edge / at-VN** — the island's mean payoff vector satisfies every true-value core inequality / and revenue within one tick of the minimum / and each winner within one tick of its Vickrey-nearest payoff; **no-overbid / unrestricted** bid spaces; **skew** — the post-hoc instance (14, 16, 8).
- **Core stage 2:** **`TX(t)`** — certified threat-exploiter: bids T + 1 if T + 1 ≤ t, else t, its policy checked against its source over T ∈ 0..80; **`F(δ)`** — follower: reads P's certified threat (or constant) c and bids ⌊δ(c + 1) + ½⌋, floored at 1 and capped at its value; **T** — the winners' total; **R** — the required total; **qualifying island** — P fixed on `TX(t)`, both items fixed on followers, T > t; **core_enc** — encounter-level core probability; **m_items** — item-role follower mass where it differs from m.
- **Behavioural hooks:** **key family** — modalized formulas over a, c, d with □ and `BOX1` (the level-1 box, ignoring world 0), size ≤ 7, depth ≤ 2, quotiented on linear frames (GL.3), length prior by shortest member; **registry state** — the vector of boxed-subformula values at a world; **sham write** — an unconditioned key matched in size and panel applicability; **response class** — signature against the fixed panel (CooperateBot, DefectBot, FairBot, TrustingBot, PrudentBot, Gödel predator, own stranger copy); **deciding origin** — the newest fill whose removal changes the signature; **generous prover** — a winner cooperating with CooperateBot, FairBot and TrustingBot and defecting against PrudentBot.
- **Rewarding prudence:** **A** — delivered fresh founders per 100 programs after the merge; **t** — generations after the merge; **G** — mean share of the prudent target; **prudent (guarded) target** — members of the PrudentBot network T that defect against certified CooperateBot; **SD set / SD52** — the 4,673 uncertified unconditional-cooperator spellings removed from the arrival prior at A = 52; **fixed-list edge** — PrudentBot's payoff minus FairBot's against a fixed spelling; **R-reward / R-resilience / R-null / R-harm** — the registered outcome regions.
- **Hooks Part R:** **B / I / M** — no-hook baseline (grammar P) / inert-hooks control (hook nodes whose fills are held but never applied) / maximal hooks; **gene site** — a hook's check call on its own fill list, evaluated by the CHKH check; **fill (t, scope, key, action, source)** — scope ∈ {none, role, behaviour, history, source, root}, source ∈ {seed, write, copy, contract}; **ablation cells** (each makes the named fills inert without shifting supply) — seedonly, nowrite, nocopy, nocontract, shuffle, noinherit, grudgeonly, idroutes, renorm, clone (fills may key to one's own spelling), M-⟨scope⟩; **UO / UOT** — universal-open / universal on the PrudentBot target; **strict identity (audit)** — an island whose majority type is mutual with none of 300 reference self-cooperating units, no panel unit and no living type of another spelling; **t99** — median generation at which a run's mean island P(C,C) first reaches 0.99; **Lemma H (Part R)** — per-root-kind resolution of fills used in populations, distinct from the high-budget certificate Lemma H above.
- **RPS and mixed actions:** **F** — forfeit (non-termination within the depth cap D; loses to every action, ties with F); **`next A`** — the action that beats A's; **`coin A B`** — a private fair coin; **`cr A`** — the exact counter: best response to A's exact action distribution conditional on A acting, forfeiting with A's forfeit probability; **`br A`** — the genuine best response (exact-br sensitivity arm); arms **pure / sample / sample-matched / exact / exact-uniform / exact-br / constants / constants + X**; **TM, N, GN, GC** — `THEM(ME)`, `next(TM)`, `coin X N`, `coin X (cr TM)`; **e** — π-weighted statewise exploitability Σ_c π_c max_k U(k, c) over the arm's own grammar (chain) or the best payoff any program earns against an island's population (lottery); **e_exset** — e with exploiters from the exact grammar; **mixing** — mass within 0.05 total variation of uniform play; **Z0** — the classes no program of the grammar can exploit.
- **RPS with a compute price:** **c** — price per application level; **H(a, b)** — expected application depth of a's root evaluation against b; **HW(a, b)** — work (applications executed, all branches of a `cr`); **depth price** U − c·H; **forfeit-only price** U − c·D·P(forfeit); **work price** U − c·HW; **net / gross exploitability** — against the population, with / without the exploiter's own cost; **e_indiv** — statewise exploitability Σ_p x_p max_k U_c(k, p); **resolved / cycling / unresolved island** — support (classes ≥ 0.05) unchanged / revisiting an earlier support / otherwise, over 500 generations.
- **Two-role mixed games:** **`card A B`** — A if Endgame I's card wins, else B; **`if Q = α then A else B`** — branch on the opponent's simulated action (fresh card in simulation); **`sr A` / `sr_k A`** — best response to one / to the empirical distribution of k simulated runs; **`exact_ee` / `exact_er`** — only the inspectee (Endgame II) / only the inspector (Endgame I) reads; **responsive (reactive) inspector** — `cr(THEM(ME))`, inspect iff the inspectee would cheat; **efficient island** — both mean game payoffs ≥ −0.05; **committed and compliant island** — inspector p > 1/4 and inspectees complying; **whole-space chain** — the jump-chain GTH solve over all pairs of monomorphic role classes.
- **Private tape (L_T^tape):** **`tape i`** — digit i of the evaluating invocation's m-digit private tape over r symbols; **invocation** — a root evaluation or one `run`, each with a fresh tape; **`hq m q`** — hash of a quote mod m (the pseudo-random control); **`prp`** — counted-probability proof by enumerating the decision tree; **`chk`** — the same atom checked from a carried count certificate (disjoint producing prefixes, replayed against a wildcard opponent, bound to the fuel stamp); **TapeR / TapeL** — rules for "plays a on every tape" atoms; **carrier** — a tape mixer with its count certificate; **K₀, c₀** — fuel cap 10⁴ and step price 0.12/K₀; **`RI` / `RIM`** — inspect unless provably compliant (budget 8) / the same with a coin fallback; **`U`** — the uniform RPS tape mixer; **e_prog / e_indiv** — exploitability of an island's population / of each resident.
- **Inspection shadow:** **E / R** — class pairs with both mean game payoffs ≥ −0.05 / E with an inspector that deters the constant cheater K (P(inspect | K) > 1/4); **light cheater** — an inspectee mixer cheating with probability in (0, 1/4]; **bounded-read exploiter** — a reader that exploits `cr`'s bounded read (e.g. `cr(coin(N, THEM(ME)))`); **N\*** — the N above which strict exits from R exceed the shadow's neutral exit (between 10³ and 10⁴); **h_X** — conditional exit hazard from a set X per mutation event.
- **Zero-tolerance inspectors:** **`zt(THEM(ME))`** — inspect iff the inspectee cheats against me with positive probability (exact read, forfeits on timeout like `cr`); **`cr_s`, `zt_s`** — `cr` / `zt` with the *suspicious default* (the timed-out mass of the read is inspected instead of forfeited); **`sr_k`** — inspect iff any of k independent simulated draws of the inspectee cheats (stops at the first cheating draw; `sr_1` is the stored `if(THEM(ME)=C,N,I)`), **`sr_k,s`** its suspicious variant; **q\*_k** — 1 − (3/4)^{1/k}, the cheating probability below which a light cheater still profits against `sr_k` (0.25 / 0.0694 / 0.0178 for k = 1 / 4 / 16); **ZT, SUS, ZT+SUS, SR1/SR4/SR16, control, comparator** — the arms (the added program, the same total mass m = 0.00135 moved onto `cr(THEM(ME))` itself, onto the unconditional inspector `I`); **gain** — an arm's π(E) minus the control's at the same (N, c); **depth phase** — the period-4 residue of the evaluator's depth cap D under which the bounded-read exploit of `cr` works (D ≡ 0 mod 4) or of `cr_s` works (D ≡ 3 mod 4); **fixed-weight hazard** — a hazard computed with the control's stationary weights embedded in the arm's class space; **lrho_safe** — `mixed2.lrho` with the deleterious branch evaluated without overflow (needed at c = 0.01 for `sr_k`).
- **Churn in the primary object:** **B6w / B6m** — the matched contract-free baseline at n = 6 (weak / modalPA), stored `L1` founders; **E, E′** — the `dollar3` DSL at n = 10 under modalPA / weak; **E-min** — n ≤ 6 plus explicit reader families, doses **lo / main / hi**; **S / Z / D readers** — single-partner reader whose fallback names the other slot (switcher) / with the null fallback / two-partner reader; **R2** — the two-partner DSL class; **T-S\*, T-D\*, T-X\*** — arm T's single-partner, two-partner and exploiting reader families; **cyclic frame** — arm T's (next, prev) argument convention; **m→m flip** — a debounced (25 generations) change of an island's modal outcome from one fair pair to another; **hazard** — m→m flips per 10⁴ fair-pair island-generations; **V\* share** — fraction of islands on a fair pair; **KS = 400, KR = 1,200, c₀ = 1.2·10⁻⁴** — arm T's read cap, root fuel and calibrated price.
- **Migration window:** **target (as stated) / target (V\*)** — every island's modal outcome efficient / on a fair pair, and all three fair pairs present; **high-purity target** — every island ≥ 0.95 on such outcomes; **T_clear / T_lost** — debounced waste-cleared and coverage-lost times; **C16 / Z4, Z64** — 16-island components (C = 1, 2, 4, 8) / four components of 4 or 64 islands; **balanced / waste-seeded start** — the two controls.
- **Immigrant rejection, Step 0:** **m→m flip** — a debounced change of an island's modal outcome between two fair pairs; **contract-mediated flip** — one preceded by an installed contract within three generations; **FX / FP / FXP / FI** — freezes of the excluded slot's offers / the pivot's partner choice / both / fiat rejection of play-changing immigrants on member islands; **gVs** — the strict veto (also refuses fair-to-fair contracts); **gKRw** — the farsighted consent table with weak consent ("accept if not worse"; a plug-in); **Δ** — (target_gV − target_gVs) / (target_gV − target_B).
