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
- *Evidence (2026-10-05i):* the bridge-less share of rival mass is stable (0.21 / 0.26 / 0.26 at n = 9 / 12 / 13;
  n = 15 does not fit), 0.98–0.99 of it P*-family, and none of it gains a bridge; forced P*-family rivals at
  (200, 64) separate in 0.97 of runs with no loss in 2·10⁸ minority-island-generations, unchanged at (400, 64),
  (200, 256) and horizon 3·10⁵; a surviving bridge resolves every bridged rivalry (0 of 525), so
  mediation-before-loss is the bridge's scramble survival; natural horizon separations are 9 of 3,000 (8 P*-family)
  at μ_bl·N·I·p₁ (RESULTS "Bridge-less rivals").
  *Operating hypothesis (RE, 2026-10-05, refined again):* island-level efficiency is the claim. Metapopulation
  universality is **not** claimed along I ≫ N at N ≥ 200: it fails with probability → 1 once I ≫ 1/(μ_bl·N·p₁)
  ≈ 10⁴ at N = 200, because about a quarter of rival mass is bridge-less and permanent; for bridged rivals it holds
  with probability → 1 in I.
- *Evidence (2026-10-05j):* under K at n = 8 the bridge-less share of rival mass is 0 at b = 16 and 54 (free 0.221),
  no new rival appears by source, natural horizon separation at (200, 64) is 0/3,000 against free's 8/3,000 at the
  same and the calibrated mN, and forced P* dies like an inert defector; at b = 4 K's soft cliques split FairBot's
  pair and 0.80 of natural runs end separated (RESULTS "Rivals under the bounded prover K").
  *Operating hypothesis (RE, 2026-10-05, refined):* island-level efficiency is the claim for the free box; for a
  sound bounded reader with budgets above every establisher pair's distinct-budget threshold, metapopulation
  universality along I ≫ N is not obstructed at n = 8 and is the candidate claim.
- *Evidence (2026-10-06, carrier populations):* for realizable carriers the two objects disagree outright: the ε→0
  chain is absorbed at every N by a drift-closed twin clique (source identity through the checker; `eq` in L_T), while
  the seed lottery is won by FairBot-shaped carriers 40/40 (RESULTS "The realizable language, milestone 2").
  *Operating hypothesis (RE, 2026-10-06):* the seed lottery is the object for the Turing-complete goal because the
  rare-mutation object is parochial by construction in any quoting language; the chain remains the stress test for
  unfakeability (its no-clique control reproduces the modal mechanism with odds ∝ N^½). *Open (RS):* whether a
  self-recognizing clique counts as cooperation for the goal (it is efficient and sound, and not universal).
- *Evidence (2026-10-06k, mixed budgets):* with budgets mixed in {4, 8, 16}, natural horizon separation is 0.683
  under a cheap-heavy prior, 0.002 above the copy thresholds and 0/300 at homogeneous b = 16; `BOX1(THEM(ME))`@4
  is in 0.94 of the separations and FairBot is compatible with itself at every budget pair; a living bridge resolves
  every bridged incompatibility (382/382) (RESULTS "Mixed-budget populations under K"). *Operating hypothesis
  (refined):* universality along I ≫ N is the candidate claim for budget priors supported on budgets at or above
  every copy's own copy threshold.
  *Would settle it:* K tables at n ≥ 9 (do new bridge-less rivals appear at larger cutoffs, as the P* family did
  under the free box?); the forced pairs and the scaling panel of the mixed-budgets spec (not run); the
  cross-budget catalogue lottery; whether the program wants universality at all (a separated patchwork has cf
  cross-island P(C,C) ≈ 0.6 while every island is efficient).
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
- *Evidence (2026-10-05f, bargaining):* a sound reader certifies commitments as well as cooperation; in one-population
  divide-the-dollar the free box at n = 7 does worse than the matched simulation grammar (Löbian shadows and hawks),
  and "sound reading preferred" holds there only with a refusal rule for certified greed (RESULTS "The modal arm on
  two-player divide-the-dollar").
- *Evidence (2026-10-05g):* the 4-rule adds no cooperator (vacuous on the DSL; its closure vanishes by b = 54); PB2 is
  decided by the guard convention (own budget: bounded Gödel II blocks it; one up: b* = 11, no faker returns); a
  trace classifier is a sufficient but not necessary sign of what K removes (RESULTS "K with the 4-rule").
  *Operating hypothesis (guard convention):* readers read Con one budget up; it costs nothing and returns no faker.
- *Evidence (2026-10-05h):* the sound bounded prover removes the free box's bridge-less rivals between islands as
  it removed its Gödel-sentence fakers within them; low budgets add a compatibility cost (soft cliques are permanent
  rivals) (RESULTS "Rivals under the bounded prover K"). *Operating hypothesis refined:* source reading through a
  sound bounded prover whose budget clears its partners' distinct-budget thresholds; incompleteness that removes
  Con-dependent cooperation is a feature across islands too.
- *Evidence (2026-10-06):* K with cut and distribution equals K up to 2 plays (μ 10⁻¹¹) and acceleration; P*, P2,
  the ladder and every faker are certified underivable at guard offsets 0 and 1 under any witness-composing rule;
  a long guard (2b + 8) with a K4 rule returns P* and the fakers together, and the net is below K (RESULTS "K with
  cut"). *Operating hypothesis refined:* read Con at one's own budget; distribution adds nothing Con-dependent, and
  the long guard trades P* for Gödel fakers.
- *Evidence (2026-10-06, L_T):* K's facts transfer to a Turing-complete evaluator with evaluation costs (8/12 against
  3/4); the realizable core is FairBot's family plus PrudentBot (b* = 25); the simulator leak is the new faker under
  real charging (RESULTS "The realizable language L_T, milestone 1"). *Operating hypothesis refined:* a sound bounded
  prover whose cost model matches the opponent's actual execution.
- *Evidence (2026-10-06, prover as code):* with the prover as code and fuel-indexed atoms the sound reader is never
  exploited (the leak closes) but cooperates only with twins; distinct sources fail by the mutual-verification
  regress, and the min-rule was an artefact of the idealization (RESULTS "The realizable language, milestone 3").
  *Operating hypothesis refined:* a sound bounded prover whose box means its own code search within a declared cap;
  cooperation between distinct sources needs certificates that are checked, not searched for.
- *Evidence (2026-10-06, certificates as code):* checked carried scripts restore distinct-source cooperation under
  a shared sound checker, with unconditional soundness; the pair rule is a symmetry (Lemma Sym), not a fixed point
  (RESULTS "The realizable language, milestone 4"). *Operating hypothesis refined:* source reading through a
  shared sound checker of carried scripts; the checker is a convention, as the proof system was.
- *Evidence (2026-10-06, carrier populations):* the R/S identity test in the checker is an observation channel the
  symmetric rule cannot hide: quote equality is one step, and it yields a drift-closed CliqueBot (RESULTS "The
  realizable language, milestone 2"). Soundness protects only S-guarded establishers.
- *Would settle it next:* bounded PA provers whose consistency strength is explicit; whether any checker design
  (symmetric closure of the self-box, no (me, me) atoms) removes identity without removing it from the base language
  (it cannot: `eq` is in L_T).
- *Evidence (2026-10-06, guard trait):* a heritable reflection margin is neither bought nor driven out; its active
  mass costs 0.02–0.04 P(C,C), growing with N, through restored Gödel fakers and cross-guard soft cliques, and brings
  back the bridge-less P\* rival (RESULTS "The guard margin as a heritable trait"). *Operating hypothesis:* read Con
  at one's own budget under a population-uniform guard convention; guard heterogeneity is a compatibility cost.
  *Would settle it next:* PrudentBot's cross-guard threshold as a function of b (does the deficit vanish at b ≥ 24?). (Earlier line, now settled: K with a sound distribution rule
  under a box; does P* return, and do Con-sentence fakers
  return with it?); K beyond the modal fragment; a bounded prover in bargaining (hawks need Löb above the copy
  threshold).

## 3. Roles: `ROLE` or fixed roles with separate populations?
- *Operating hypothesis (RS, 2026-10-04):* fixed roles with separate slot populations for every social-choice question;
  `ROLE` kept only as the symmetric control, since it internalizes the externality by fiat ("a cheap trick").
- *Evidence:* THEORY §3 "Distribution"; the ultimatum fixed-role results; the three-player spec.
- *Evidence (2026-10-05):* divide-the-dollar (RESULTS "Divide-the-dollar partitions"): fixed roles give a rotating
  dictatorship of the largest demand (0.99 of π at N ≥ 300); `ROLE` keeps 50–50 at 0.69 at N = 10³ and loses it below 10⁴ to a
  role-conditioned hawk polymorphism, then to the greedy one (corrected by RESULTS "Solver audit"); one population
  without `ROLE` 0.91–1.00 until 5·10³ and then the greedy polymorphism in `dollar5` (in `dollar3` the greedy state
  is a lumping artefact removed by twin drift). The role structure decides which split; the population structure decides whether efficiency
  survives in lim_N; the no-`ROLE` control shows the 50–50 advantage comes from the structure, not the signal. In the one-atom modal
  grammar (RESULTS "The modal arm on two-player divide-the-dollar") fixed-role π spreads over all splits (endpoints
  0.23), so the rotating dictatorship depends on universal conceders being in the language.

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
- *Evidence:* THEORY §3 "Distribution"; the club spec; RESULTS "Three-player majority divide-the-dollar" (2026-10-05): the pure chain with fixed roles selects rotating, mostly unfair pairs (a rotated dictatorship of the pivot); the grand coalition at thirds gets ≤ 0.017 and leaks through "accept a pair offer" bridges; source reading does not change it. Democracy as a stable state needs something beyond the pure chain. The union game (RESULTS "The union game", 2026-10-05) did not supply it: a quorum precondition is FairBot's handshake on strikes, the fair share is set by the prior (0.31 uniform vs 0.001 length prior), and the strike pact's wage check is fakeable (the polarity dilemma). The enforcement run (RESULTS "Incentive-compatible enforcement", 2026-10-05) reads "threats hard to enforce" as ex-post rationality on both sides and gets the smallest positive wage (0.75 intermediate under the length prior, workers 0.19), not equal division; a non-credible committed threat deters because the chain never tests it; equal division is unsupported under every commitment structure except a uniform named-program prior with a rational boss (0.55). Divide-the-dollar (RESULTS "Divide-the-dollar partitions", 2026-10-05): a Θ(1/n) fair split is not stochastically stable under fixed roles (≤ 0.003 of π at N ≥ 10³, the accommodator ratchet) but is the modal island outcome of the seed lottery (0.23–0.78; 0.94–1.00 with one population and migration). If the target is a fair *state*, the seed lottery delivers it and the mutation object does not: entry 1's choice of object decides this entry. Under sound reading the fair state also fails in lim_N for one population (Löbian hawk traps at 0.65 efficiency) while the lottery still makes 50–50 universal in both arms (RESULTS "The modal arm on two-player divide-the-dollar").

- *Evidence (2026-10-06, seed lottery):* zero wage 0.825 committed, intermediate 0.90 rational; the three-role threshold
  met on 0 islands (fair wage only, by arithmetic); time-averaged worker shares 0.003 (CC) and 0.113 (RR). Neither
  target is approached under fixed roles without a wage-conditional worker mass; the RS's "arrive in numbers" lever
  kills the threat, not the zero wage (RESULTS "The social organization game under the seed lottery").
- *Evidence (2026-10-06, concessions):* with an expressive concession language the fair state is stochastically
  stable under a uniform prior over the named programs (0.98) and absent under the length prior (≤ 0.01); in the
  lottery it needs strikers in numbers, then persists on 0.32 of islands with probes against 0.05 without (RESULTS
  "Concessions"). The fair *state* is a prior-and-seeding property in this game, not a grammar property, and the
  time-averaged target does no better.
- *Naming (RS, 2026-10-06):* the boss/worker family is "the social organization game". *Open:* whether the target is
  Θ(1/n) as a stochastically stable state or time-averaged (the three-player rotating dictatorship already gives the
  latter by symmetry); decided (RS, 2026-10-06): the state; the time-average is free by symmetry in the symmetric games and is
  reported only as a fallback.

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
- *Evidence (2026-10-06):* the seed lottery isolates the prior's role: the length prior gives wage-blind strikers 0.48
  and wage-conditional refusers 0.0065; reassigning the striker mass to refusers or militants raises intermediate to
  0.23 or fair to 0.05 under a diverse boss seed and to 0 under a hostile one (RESULTS "The social organization game
  under the seed lottery"). A prior that weights wage-conditional behaviour is necessary, not sufficient.
- *Evidence (2026-10-06, concessions):* the length prior weighs the full price discriminator D\* at 9.7·10⁻⁹ per
  variant against 0.1025 per constant boss; under a uniform prior over the named programs the same game puts 0.98
  of π on fair (RESULTS "Concessions"). The worker-probe arm (workers reading the boss's play against a quoted
  striker) was not run and is the remaining route to a worker-side counterfactual.
- *Operating hypothesis (amended, 2026-10-06):* distribution results are stated relative to the prior, the commitment
  structure, and (at ε = 0) the seed composition; the boss's expressivity changes π only when the concession is as
  likely as a constant.
- *Would settle it:* a principled prior over program *policies* (behaviour classes) rather than spellings, or a
  realizable-language prior (entry 11) under which a two-probe concession is not 10⁻⁷ times rarer than a constant.
- *Evidence (2026-10-06, carrier populations):* L (2^−nodes), U (uniform over classes) and the repo's L_std agree on
  the chain's verdict (the clique; without it 0.91 / 0.98 / 0.69 at N = 10⁵); L_std weakens the lottery (23/40)
  because its D class holds 0.45 of the mass.
- *The research question, restated by the RS (2026-10-06):* "how do we design a prior that lets us cheaply point at
  good programs?" Not length as such, but a million-line program is suspect. *Operating frame (RE):* description
  length in a language with a public library of general-purpose primitives (quotes, evaluation, a sound checker,
  probes of play against quoted opponents), so that the prior is set by the library, and the discipline test is that
  the primitives are general purpose, not the answer. *The seeding argument (RS: everything gets seeded, good
  strategies should not die out):* holds in three stages whose rate is set by the prior. (1) A seeded copy needs
  I ≈ 1/(p·N) islands (10⁶ at p = 10⁻⁸). (2) A device that needs a partner (the two-probe boss and the wage-conditional
  worker are each neutral alone) establishes only by a two-type coincidence on one island, so the island count is
  set by the product of the two masses; a self-sufficient device (FairBot against the seed mixture) does not pay
  this. (3) After establishment the one-slot leak killed two thirds of fair islands by the horizon; only the
  unfakeable fair state (D\*[L1], militant⁻, militant⁻) has no strict invader. Uniform priors over hand-named
  programs are not a finding but a choice (RESULTS "Concessions"); a uniform prior over all behaviour classes is
  cutoff-dependent and was abandoned at 1,393 classes.
- *Pause (RS, 2026-10-06):* no new experiments before Thursday morning 2026-10-08.

## 11. The realizable language: how to leave the modal fragment
- *Options:* extend the weak-arm DSL (self-application, divergence) with K boxes; a new small Turing-complete
  language (λ-calculus with quoting and a step-counting evaluator) with a bounded prover over its own evaluation
  rules; the prover as a primitive, or as code in the language.
- *Decision (RS, 2026-10-06):* the new language; the single-pair result (FairBot by bounded proof cooperates with
  itself above a budget threshold, Critch's bounded Löb in our ecology) as the first milestone, before any chain;
  the stated end state is that programs run their own proof search as code, so the budget is the program's own step
  count, the checker's source is visible, and soundness becomes a trait (sloppy checkers are a new faker class).
- *Operating hypothesis:* K's results transfer (thresholds, copies cheaper than distinct budgets, Gödel-sentence
  fakers disarmed, bounded Gödel II), with the search exponential and the cutoff small.
- *Evidence (2026-10-06):* milestone 1 held (sound; witness executable within K = 10⁶; thresholds FB 8 / FB1 13 /
  PB 25; the control removes exactly the Löbian cooperation); the hypothesis was right on transfer and wrong on
  "cutoff small" for prudent readers (PB needs W ≈ 3.7·10⁵). *Open (RE decision):* milestone 2's prior. Literal
  enumeration of L_T terms is infeasible (FB_b is ≈ 11 nodes over ≈ 20 constructors), so milestone 2 needs a
  restricted grammar or a template prior; the RE's operating hypothesis is a template grammar over the modal
  fragment's shapes (conditionals on prove_b and run_k atoms about quoted sources) with the length prior on its
  node counts, which reproduces the modal arm as a sub-language and adds the simulator atoms.
- *Evidence (2026-10-06, milestone 3):* the prover as code is feasible from K = 10⁶ (FairBot 1.1·10⁵ steps, b* = 7;
  PrudentBot 9·10⁵ at K = 10⁷), twins only, nothing at K = 10⁵. *Operating hypothesis for milestone 2, revised:*
  under the code semantics only exact query identity cooperates, so a population prior is judged by its mass on
  twins; milestone 2 waits on the certificate mechanism (milestone 4), which may restore distinct-source
  cooperation. *Open (RE decision):* the cap U as a heritable trait versus a fixed fraction of K.
- *Evidence (2026-10-06, milestone 4):* certificates as code restore distinct-source cooperation (10 of 10 distinct
  carrier pairs at K = 10⁶, checks of 1–4·10⁴ steps, twins no longer special). *Operating hypothesis for
  milestone 2:* a grammar of carriers by call skeleton over one shared checker, with the prior's mass on
  certificate-carrying sources, judged by cooperation among distinct skeletons. *Open (RE decisions):* whether
  production is part of the program (charged) or a public service; the cap V as a trait or a fixed fraction of K.
- *Operating hypotheses (RE, 2026-10-06, pending the RS's answer on the prior under the 15-minute rule):* production
  is a public service (the frozen tactic, free, like the library), with optional charged production as an arm; the
  cap V is a fixed fraction of K; the length prior over spellings is the main arm, uniform over classes the control.
- *Evidence (2026-10-06, milestone 2 done):* the machinery transfers (odds ∝ N^½ without cliques; lottery 40/40 under
  the polymorphic endpoint; L, U and L_std agree on the chain's verdict, L_std weakens the lottery to 23/40 since D
  holds 0.45 of that prior); a 6-node twin clique absorbs the chain (RESULTS "The realizable language, milestone 2").
  *Open (RS):* accept syntactic self-recognition as a realizable program (the RE's view: it is, since `eq` is in the
  base language, so the finding is about the object, not the checker), or change the checker or grammar so self-play
  is indistinguishable (which the base language would undo). *Next (after 2026-10-08):* the social organization game
  over the realizable language (the RS's prior question), and milestone 5, endogenous certificate production
  (charged search at production time, the tactic as code).
