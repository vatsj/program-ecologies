# DEFERRED.md — decisions punted to a later Fable

Started 2026-10-04 at the RS's request. Each entry is a decision the program has *not* committed to. It records the
options, the current **operating hypothesis** (what we act on meanwhile, revisable without ceremony), the evidence so
far with RESULTS pointers, and what would settle it. Nothing here is a commitment; THEORY.md holds the claims we defend,
REJECTED.md the ones we dropped.

## 1. The object: stochastic stability under rare mutation, or almost-sure efficiency under seeding?
- *Options:* (a) π of the ε→0 chain in lim_N, mutation re-injecting every type forever; (b) the ε = 0 absorption
  lottery with iid seeding from the prior, where "good" means P(efficient) → 1 along a path in (N, I); (c) both.
- *Operating hypothesis (RS, 2026-10-04):* (c), with (b) primary for the Turing-complete goal and (a) kept as the stress
  test that identifies unfakeable cooperators.
- *Evidence:* Corollary 1 is a theorem about re-injection: the leak x → FairBot → ALLC → D needs ALLC re-supplied. At
  ε = 0 ALLC is eaten once and never returns, and the modal arm ends efficient in 40/40 runs at both end cells
  (RESULTS "Almost all seeds?"). Under mutation the universal network leaks at 1/N forever (RESULTS "Universality
  against drift-closure").
- *Evidence (2026-10-05):* the per-island chance is flat in the cutoff at n = 6–9 and tracks the mass of D-entering
  self-cooperators, fakeable or not (RESULTS "cutoff sensitivity in n"). Unfakeability belongs to the mutation object.
- *Evidence (2026-10-05b):* μ_est ≥ 0.0207 at every cutoff, rigorously (establisher status only accumulates), with a
  1/s² tail and an extrapolated limit ≈ 0.027; the resident-conditioned spoiler exposure is 0.27 at n = 12 and
  flattening; at I = 4 the mN = 0.1 − mN = 10 contrast is 0.18 [0.005, 0.35], by merging during nucleation, not by
  spoilers (RESULTS "the tail in n").
- *Evidence (2026-10-05c):* a co-seeded faker is a bounded discount at n ≤ 12 (d ≈ 1.1; forced k = 1 null; k = 10 ≤ 0.41), because fakers of the main provers die in the scramble (RESULTS "Spoiler-conditioned establishment").
- *Evidence (2026-10-05d):* Claim A proved (no dangerous fakers for the prover family, by soundness alone); the
  scramble kills fakers by demography (per copy ≈ 1/(1 + τ_A), τ_A ∝ log N), not selection, so the spoiler term for
  *fakeable* establishers grows like N/log N unless post-scramble harm falls (RESULTS "The scramble lemma").
- *Operating hypothesis (RE, 2026-10-05):* carry "almost all seeds" on the fakerless establishers, FairBot's pair
  (μ_core ≈ 0.0102, rigorous and uniform in n), and treat the fakeable provers as a measured bonus.
- *Evidence (2026-10-05e):* compatibility resolves on one island (0 of 3,814 co-seeded incompatible pairs failed; two self-cooperators cannot hold a stable mixture), but mutually-defecting establishers can be held on separate islands, each efficient (RESULTS "compatibility").
- *Evidence (2026-10-05f):* rival networks between islands are a metastable patchwork, not a frozen one: the hazard
  is ≈ mN·ρ_DD(N) with ρ_DD falling exponentially in N (1.85·10⁻⁵ at N = 100), and at mN ≥ 1, N = 100 migration
  resolves them by majority within 10³–10⁴ generations while every island stays efficient (RESULTS "Rival networks
  across islands"). *The mN rule the data support:* keep x = mN·T_nuc/N ≲ 0.3 (replacement fraction during
  nucleation; the control collapses N = 100 and 400), i.e. mN ≲ 0.3·N/T_nuc(N) ∝ N^0.7.
- *Open item (2026-10-05h, partly settled by RESULTS "A path in (N, I, mN)"):* on the calibrated boundary
  mN = 0.3·N/T_nuc independent nucleation (q ≈ 0.82–0.97) and resolution coexist for rivals the prior *bridges*
  (a class neutral to both absorbs the minority polynomially, and its scramble survival → 1 in I), and fail for
  bridge-less rivals (P*-type, ≈ 1/4 of rival mass at n = 9), which form permanent patchworks at N ≥ 200. No natural
  run in 1,000 ended separated. Propagules are not a scaling fix (barrier ≈ N·w·(1/2 − k/N)²).
  *Operating hypothesis (RE, 2026-10-05, refined):* island-level efficiency is the claim; metapopulation
  universality is claimed for rival pairs the prior bridges and conceded beyond N ≈ 100 for bridge-less pairs.
  *Would settle it:* the prior mass of bridge-less rival establishers as n grows, and natural runs at N ≥ 200 large
  enough to sample one.
- *Evidence (2026-10-05g):* (i) is done and stronger than conjectured: Lemma D′ is proved for any lineage and any
  stopping time with no fitness hypothesis (Lemma D is the killed fixed-time case); (ii) is done: the per-founder
  union bound replaces 1/P(A) by a measured r_q = 0.8–1.7 and the bound is positive in 27/27 cells; the per-island
  establishment chance has a formula (near-critical founders, pooled two-type escape) and tends to 1 along N at fixed
  n (0.087 → 0.980 over N = 100 → 25,600). The N ≫ I path now has a formula-backed route to P(efficient) → 1 on a
  single island (RESULTS "The demographic lemma").
- *Would settle it:* whether any question the program cares about needs π rather than the lottery; the between-island
  tension of the open item above.

## 2. The observation channel: behaviour probes, source reading, or certificates?
- *Options:* extensional probes (simulation), source reading through a sound (bounded) prover, honest certificates,
  partial-disclosure certificates.
- *Operating hypothesis:* source reading through a sound bounded prover. Fakers are artifacts of probes (a faker mimics
  on the probes you run and defects where you don't look); soundness rules them out at any budget.
- *Evidence:* E1 matched control; the certificates-only arm; the sibling theorem's dependency ledger (RESULTS
  "Conjecture 4"), whose mechanism is extensional and whose transfer to bounded proof search is conditional on budget.
- *Evidence (2026-10-04):* a sound stabilization-cost gate preserves the free arm in both objects at n ≤ 8 and creates no fakers (RESULTS "Bounded provers"); the proxy does not charge the Löb step, so it barely binds on occupied states.
- *Evidence (2026-10-05):* proof-carrying contracts need provability semantics; with it they equal the ungated free box among carriers; where a gate removes legibility (b = 0) they restore cooperation to 0.95–0.99 by production or inheritance, not swapping (RESULTS "Proof-carrying contracts v1"). The RS's contract pitch is confirmed for legibility and refuted as a selector.
- *Evidence (2026-10-05b):* carried proofs make legibility heritable at b = 0: a 1–3% prover-carrier seed establishes, contracts cross lineages within a source class by swapping; but the invasion advantage rests on non-carriers reading contracts while staying unreadable (RESULTS "Prover-carrier seed at b = 0"). *Closed (2026-10-05c):* the symmetric gate was run (RESULTS "The symmetric gate"); the asymmetric rule inflated establishment by about 0.1–0.2 and did not create it. *Operating hypothesis:* the symmetric rule is the default for future contract experiments, since a program without a checker should not read contracts; the asymmetric rule is kept only as a comparison.
- *Evidence (2026-10-05d):* an explicit proof system now exists for both readings (RESULTS "Proof length"): GLS+Def reproduces the free box with certified lengths, and K, a sound bounded calculus decided exactly by search, preserves the n = 6 arm from FairBot's distinct-budget threshold up, closes nothing and creates no strict invader, where a matched random perturbation does. *Operating hypothesis refined:* source reading through a prover sound for its own derivability semantics; a weaker sound prover can cooperate more than the free oracle.
- *Evidence (2026-10-05e):* K at n = 8 keeps and improves the free arm from b = 4; the gain is Gödel-sentence faker
  removal; K loses exactly Con-dependent and 4-axiom cooperation and keeps PrudentBot from b = 11 (RESULTS "K at
  n = 8"). *Operating hypothesis refined:* a prover sound for its own derivability semantics, whose incompleteness
  removes Gödelian and Con-dependent cooperation; the realizable core is FairBot's family plus PrudentBot.
- *Would settle it next:* a K with a sound 4-axiom rule (□A ⊢ □□A), to see whether PB2 and the ladder return and
  whether fakers return with them; K beyond the modal fragment.

## 3. Roles: `ROLE` or fixed roles with separate populations?
- *Operating hypothesis (RS, 2026-10-04):* fixed roles with separate slot populations for every social-choice question;
  `ROLE` kept only as the symmetric control, since it internalizes the externality by fiat ("a cheap trick").
- *Evidence:* THEORY §3 "Distribution"; the ultimatum fixed-role results; the three-player spec.
- *Evidence (2026-10-05):* divide-the-dollar (RESULTS "Divide-the-dollar partitions"): fixed roles give a rotating
  dictatorship of the largest demand (0.99 of π at N ≥ 300); `ROLE` keeps 50–50 at 0.69–0.83 until N ≈ 2·10⁴; one
  population without `ROLE` 0.91–1.00 until 5·10³; both one-population arms then lose efficiency to the greedy
  polymorphism. The role structure decides which split; the population structure decides whether efficiency
  survives in lim_N; the no-`ROLE` control shows the 50–50 advantage comes from the structure, not the signal.

## 4. The form of a compute price
- *Options:* none; atoms/depth pricing; lazy (copy subsidy); certificate pricing (decidability = monotonicity); amortized
  verification (caching); proof budgets.
- *Operating hypothesis:* free box with amortized verification, which is the α = 1 price path and behaves as free
  proofs (THEORY §9.2); realizability enters through proof budgets, not per-match prices.
- *Evidence (2026-10-05):* carried contracts are the realization of amortized verification; they are inert where legibility is free and restorative where it is not (RESULTS "Proof-carrying contracts v1").
- *Constraints established:* a price is harmless in the limit iff it vanishes faster than N^(−1/2) of the stakes or is
  exactly zero on the ladder's rungs; copy subsidies are moats; any price that beats 1/N is incumbency (Proposition 3).
- *Proof budgets (2026-10-04):* at this level of idealization a budget neither prices nor closes; it is harmless, and proof length is not a moat because leaks run through cheaper neighbours (RESULTS "Bounded provers").

- *Evidence (2026-10-05, K prices):* in K, amortized and cache-accounting prices keep P(C,C) at 0.56–0.60 for c ≤ 0.1
  (0.42 at c = 1, N = 10⁴, rising with N) with exit slope −1 and a weakly selected ALLC exit (ratio 1 + w·c·b/2);
  per-match pricing gives all-D; lazy pricing locks in PrudentBot@16 at n = 8 even at c = 0.01 (RESULTS "K at n = 8").
  *Operating hypothesis kept:* amortized verification; the schedules are imposed, verification events uncounted.

## 5. Imposed fixed points
- *Options:* Löb only (unique fixed points, no rule); greatest-fixed-point rules (C-seeded certificates, the club).
- *Operating hypothesis:* avoid imposed fixed points; Löb is the selection-free route to outcome symmetry. The gate's own semantics needed a choice too (world-indexed trace vs a cycling joint fixed point); the world-indexed trace selects nothing and was adopted. The club is
  run as an oracle benchmark only. The RS objects to the club normatively: it punishes the merely tolerant.
- *Evidence:* RESULTS "Certificates-only arm" (gfp vs Löb differ by one fakeable probe); RESULTS "The closed club": the club is a clique over a declared predicate, its fixed point is one of 2^|K*| and the choice decides which member holds π. "Black-magic fixed points" re-closed for membership-level rules. The RS's objection stands on structural grounds as well.

## 6. The normative target
- *Options:* Pareto efficiency in the limit (the standing goal); universality (cooperate with FairBot's network) vs a
  closed club; Θ(1/n) fair partition as a stochastically stable *state*; democracy as May's axioms with anonymity
  deliberately violable; "threats hard to enforce" ≡ a symmetric threat point.
- *Operating hypothesis:* efficiency first; for distribution, Θ(1/n) as a stable state with anonymity violable by slot
  asymmetry; universality over the club, accepting the 1/N leak as a mutation artifact (entry 1). The club is dropped as a target: it is a clique by declaration (RESULTS "The closed club").
- *Evidence:* THEORY §3 "Distribution"; the club spec; RESULTS "Three-player majority divide-the-dollar" (2026-10-05): the pure chain with fixed roles selects rotating, mostly unfair pairs (a rotated dictatorship of the pivot); the grand coalition at thirds gets ≤ 0.017 and leaks through "accept a pair offer" bridges; source reading does not change it. Democracy as a stable state needs something beyond the pure chain. The union game (RESULTS "The union game", 2026-10-05) did not supply it: a quorum precondition is FairBot's handshake on strikes, the fair share is set by the prior (0.31 uniform vs 0.001 length prior), and the strike pact's wage check is fakeable (the polarity dilemma). The enforcement run (RESULTS "Incentive-compatible enforcement", 2026-10-05) reads "threats hard to enforce" as ex-post rationality on both sides and gets the smallest positive wage (0.75 intermediate under the length prior, workers 0.19), not equal division; a non-credible committed threat deters because the chain never tests it; equal division is unsupported under every commitment structure except a uniform named-program prior with a rational boss (0.55). Divide-the-dollar (RESULTS "Divide-the-dollar partitions", 2026-10-05): a Θ(1/n) fair split is not stochastically stable under fixed roles (≤ 0.003 of π at N ≥ 10³, the accommodator ratchet) but is the modal island outcome of the seed lottery (0.23–0.78; 0.94–1.00 with one population and migration). If the target is a fair *state*, the seed lottery delivers it and the mutation object does not: entry 1's choice of object decides this entry.

## 7. Rates
- *RS:* no normative opinion. *RE's opinion:* the relevant quantity is the cost of a given confidence; in the seeds run
  failure fell exponentially in the island count and polynomially in island size, so buy islands, not island size.

## 8. Ablating myopia
- *Operating hypothesis (RS, 2026-10-04):* island-level selection on boss populations (w_g), not free punishment (tilts
  toward repression by fiat) and not lookahead fitness (builds the phenomenon into the selector).
- *Evidence (2026-10-05):* island selection on the boss slot spreads cheap exploitation and the deterrent strike-targeting policy, not realized repression (0.002–0.004 throughout); the all-slot effect is larger (RESULTS "The union game"). It is spatial selection on realized payoff differences, not a horizon ablation.

## 9. Paper
- *RS (2026-10-04):* no paper, no draft. The title in CLAUDE.md is a working title only.

## 10. The worker grammar and prior for wage reading
- *Options:* set atoms over the wage (as run), PA + Con(PA) boxes, a uniform prior over behaviours, or a prior that does
  not give the constant striker and scab 0.48 each.
- *Operating hypothesis (RE, 2026-10-05):* distribution results are stated relative to both the prior and the
  commitment structure; under committed play the prior decides (0.31 uniform vs 0.001 length prior), under ex-post
  rational enforcement on both sides the length prior no longer pins the wage to zero (intermediate 0.75).
- *Evidence:* RESULTS "Incentive-compatible enforcement": the unfakeable-polarity pact cannot activate without a
  world-0 condition in the two-level language, and PA + Con^k only moves the faker up a world (the sibling theorem's
  regress), so that route is closed.
- *Would settle it:* a worker language whose strike handshake does not need a world-0 condition (none known).
