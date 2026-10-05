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
