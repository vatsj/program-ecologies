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
- *Would settle it:* (i) a demographic lemma, survival ≤ k₀/(1 + b_min·τ) for supermartingale lineages (conjectured;
  matches the ghost within 12%); (ii) a bound on P(target alive ∧ faker alive) that avoids the 1/P(A) loss of the
  union step, by conditioning on the target's path; (ii) a rule for scaling mN along the I ≫ N path: migrants per island during nucleation must
  be small relative to N (mN·T_nuc ≈ 6 / 60 / 600 against N = 400 gave independent / partly merged / merged); and
  whether migration along the I ≫ N path merges or separates rival networks held on different islands; and whether
  any question the program cares about needs π rather than the lottery.

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
- *Would settle it:* an explicit proof system with measured proof length and a sound checker; the stabilization proxy is exhausted.

## 3. Roles: `ROLE` or fixed roles with separate populations?
- *Operating hypothesis (RS, 2026-10-04):* fixed roles with separate slot populations for every social-choice question;
  `ROLE` kept only as the symmetric control, since it internalizes the externality by fiat ("a cheap trick").
- *Evidence:* THEORY §3 "Distribution"; the ultimatum fixed-role results; the three-player spec.

## 4. The form of a compute price
- *Options:* none; atoms/depth pricing; lazy (copy subsidy); certificate pricing (decidability = monotonicity); amortized
  verification (caching); proof budgets.
- *Operating hypothesis:* free box with amortized verification, which is the α = 1 price path and behaves as free
  proofs (THEORY §9.2); realizability enters through proof budgets, not per-match prices.
- *Evidence (2026-10-05):* carried contracts are the realization of amortized verification; they are inert where legibility is free and restorative where it is not (RESULTS "Proof-carrying contracts v1").
- *Constraints established:* a price is harmless in the limit iff it vanishes faster than N^(−1/2) of the stakes or is
  exactly zero on the ladder's rungs; copy subsidies are moats; any price that beats 1/N is incumbency (Proposition 3).
- *Proof budgets (2026-10-04):* at this level of idealization a budget neither prices nor closes; it is harmless, and proof length is not a moat because leaks run through cheaper neighbours (RESULTS "Bounded provers").

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
- *Evidence:* THEORY §3 "Distribution"; the club spec; RESULTS "Three-player majority divide-the-dollar" (2026-10-05): the pure chain with fixed roles selects rotating, mostly unfair pairs (a rotated dictatorship of the pivot); the grand coalition at thirds gets ≤ 0.017 and leaks through "accept a pair offer" bridges; source reading does not change it. Democracy as a stable state needs something beyond the pure chain. The union game (RESULTS "The union game", 2026-10-05) did not supply it: a quorum precondition is FairBot's handshake on strikes, the fair share is set by the prior (0.31 uniform vs 0.001 length prior), and the strike pact's wage check is fakeable (the polarity dilemma).

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
- *Operating hypothesis:* none yet. The reduced chain shows the prior decides the fair share (0.31 uniform vs 0.001
  length prior), so any distribution result must be stated relative to the prior.
- *Would settle it:* sol's follow-up, incentive-compatible enforcement (repression that must pay for itself within
  the encounter), and a wage check in the unfakeable polarity that can still carry a pact (needs PA + Con?).
