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
  unfakeability (its no-clique control reproduces the modal mechanism with odds ∝ N^½).
- *Decision (RS, 2026-10-10):* a self-recognizing clique counts as cooperation but is not the desirable object; the
  target is universal cooperation (probes or proofs). **The seed lottery is the object for the Turing-complete goal.**
  Rationale (RE): under rare mutation universality is impossible in principle in any quoting language (universality
  and drift-closure are exclusive, and a one-line identity clique exists and is drift-closed); under iid seeding a
  universal family pools its seed mass across spellings while an exact-identity clique cannot (its spellings defect
  on each other), so the lottery's selection pressure matches the target. The chain remains a diagnostic.
  *Contingent and to test next:* the clique's mass with `eq` in the grammar (milestone 2's 7·10⁻⁴ understates it), and
  pooled parochial clubs (tags: bridged; exclusive clubs: the bridge-less I ≫ N patchwork).
- *Evidence (2026-10-11, identity and tags):* **the pooling rationale is refuted at establishment.** With `eq` at one
  node identity cliques weigh 0.009, hold 0.41 of islands and leave 0/40 runs universal (every island efficient);
  ten incompatible clique spellings establish as well as one identity; the scramble rewards prudence (exploiting
  the seed's unconditional cooperators), which open carriers forgo; without `eq` about half the runs are universal
  (RESULTS "Identity and tags in the carrier grammar"). The decision (the seed lottery as the object) stands; the
  reason for it does not.
- *Open (RS, 2026-10-11):* (a) island-level efficiency as the defended target in quoting languages, with universality
  a property of identity's price in the prior (threshold between 5·10⁻⁴ and 9·10⁻³); (b) a prior or library in which
  identity is not cheap (the RE's view: structural equality is derivable in any quoting language, so pricing it is a
  selector unless the prior is justified independently); (c) keep universality and measure the threshold.
  *Operating hypothesis until he answers:* (a), with the threshold scan as the next cheap run.
- *Evidence (2026-10-11b, prudent openness):* the threshold is measured and is an abundance, not a price: m\* =
  1.26·10⁻³ [6.6·10⁻⁴, 1.6·10⁻³] at (100, 64), about 8 seeded clique copies per run (L has 57), and it is not
  scale-free (no crossing at (100, 128), where the clique-free baseline is 0.475). Option (b) would need about a 7×
  cut in seeded clique copies at this scale, and the factor moves with (N, I). Prudence and openness coexist (CBP
  is open to CB); the prudent open core is universal in 29/40 runs without cliques (RESULTS "Prudent openness
  against identity"). Operating hypothesis (a) unchanged; the defended universal statement is relative to the
  identity abundance and the (N, I) baseline.
- *Evidence (2026-10-12, provenance):* with self-play production refused and the 4.6 TwinD copies per run moved to
  the prudent core, the lottery is universal-open on 40/40 by 10,000 at (100, 64), 17–18/20 at (200, 64) and
  14–16/20 at (100, 128); S-nonself alone 28/40, 11/20, 6/20; one H donor per island 37/40, 20/20, 18/20 (RESULTS
  "Provenance"). The remaining identity mass under endogenous production is the seed's own self-reading cliques,
  which is exactly this entry's open question.
- *Decision (RS, 2026-10-13):* **the non-extensional (realizable) arm admits `eq`.** Identity is part of the
  ecology, and the checker's root-box channel puts it into any quoting language at FairBot's price anyway. The
  seed lottery remains the object ("seeds over cliques"). *Defended claim for the realizable arm:* island-level
  efficiency with probability → 1 along the seed path; universality relative to identity's seeded abundance and the
  (N, I) geometry, with the measured threshold (≈ 8 seeded clique copies per run at (100, 64)) and the two measured
  remedies (refuse self-play production; the prudent open core). This entry's identity question is closed.
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
- *Evidence (2026-10-15, the realizable lottery along paths in (N, I, mN)):* island-level efficiency holds on every path;
  the only island loss is a whole-run scramble failure, vanishing with N·I. The seed's TwinD cliques are transient at
  N = 100 (absorbed by coordination within about 10⁴ generations) and permanent from N = 200; there universality under
  S-nonself is f₀·e^(−0.07 c) in the seeded copies c (crossing near 6, blind to clustering), so it goes to 0 along any
  path growing N·I at a fixed length prior. Without cliques 5–20% of runs at N ≥ 200 end in bridge-less non-identity
  rivals, which calibrated migration (mN = (N/100)^0.7, x held at 0.31–0.37) does not resolve. One donor per island is
  universal on every path (0.80–1.00). *Operating hypothesis (amended):* the defended claim (island-level efficiency
  along the seed path) stands; universality holds at N ≤ 100 given long horizons, at N ≥ 200 iff seeded clique copies
  are few (about 6 for 50%), or with one donor per island. Island failures are one correlated event per run, so the
  path condition is on runs. *Open:* the panel at N = 400; the bridge-less non-identity rival family and whether a
  prior or rule bridges it.
- *RS (2026-10-15), the target network:* "I'm happy crowning the prudentbot network as the official state sponsored
  solution"; rival networks are worth trying to remove. *Operating hypothesis:* the target is universal cooperation on
  the PrudentBot network (FairBot-family and PrudentBot holders mutually certified); identity cliques and
  certificate-reading rivals (e.g. the anti-punisher `if(or(CHK(me,^C,C),CHK(them,^D,D)),D,C)`, which defects against
  anyone certified to punish DefectBot and is logically unbridgeable against PrudentBot) are failures of the target.
- *RS (2026-10-15), re-injection:* "trickle and drift are distinguished only by scale - a small trickle over infinite
  time brings back the shadow. The divide I wanna draw is that drift should never colonize an island, only reintroduce
  fit programs." *Operating hypothesis:* re-injection is admissible in the regime where neutral arrivals never take an
  island over the horizon while selected arrivals do; per island the ratio of selected cures to drift colonizations is
  ≈ 2·s·N·μ_pred, so the window widens with N and exists only if the useful entrants are common in the prior
  (`specs/2026-10-15-removing-rivals.md`, measured there).
- *RS (2026-10-15), the deviation–equilibrium correspondence again:* "the mutation model forces the program to be inexploitable
  against arbitrary programs". *RE mapping:* the re-entry model is the deviation set. Rare mutation admits every
  program, neutral ones included, so it asks for closure against neutral entrants (ESS-like; the shadow is the
  neutral step), which no modal class meets (sibling theorem) and only identity cliques met in the realizable language;
  the ε = 0 lottery admits only founders (many equilibria, selected by abundance); re-injection in the RS's window
  admits strictly profitable entrants only (Nash-like over the prior's program space), which the PrudentBot network
  and identity cliques pass and exploitable rivals fail. *Test in flight:* inside the window, no selected takeover of a
  target island, exploitable rivals cured, cliques not.
- *RS (2026-10-16), annealed mutation:* "a model where mutation rate decreases over time. It starts at infinity, which
  generates the random seed, but the tail is light enough that islands can't drift (but heavy enough to prey on
  inefficiencies)." *RE:* with Λ the integrated post-seed re-injection per island, drift colonizations ≈ Λ and cures
  of exploitable rivals ≈ 1 − e^(−2sNμ_pred·Λ), both linear in Λ, so no schedule shape gets both with certainty at
  fixed N; the clean object is the scaling limit Λ_N → 0 with N·Λ_N → ∞ (e.g. ε(t) ∝ t^(−α), α > 1, its tail scaled
  with N). The heavy early phase enlarges the effective seed, adding clique copies. *Next:* a spec reusing the
  removing-rivals rain kernel and drift classifier once that run lands. *RS's Pangaea prediction:* "they'll fail on a
  Pangaea, where universality pays off" (`specs/2026-10-16-pangaea.md`).
- *Evidence (2026-10-16, removing rival networks):* one PrudentBot founder per island removes the open non-prudent
  rivals (with or without certificates) but not identity (uot 0.55–0.75 at three cells, 0.10 at (200, 128)); seed rain
  cures exploitable rivals through predators (0.92 at εN = 0.1) but reintroduces identity-exploitable target shadows,
  so identity islands triple and the target does not grow; the RS's window fails at N = 200–400 at every rate, with
  drift colonization ∝ 1/N and per-arrival predator cure ≈ 0.26 (RESULTS "Removing rival networks"). *Operating
  hypothesis:* finite rain is a diagnostic, not a design; the annealed object is the large-N scaling limit. *Next:*
  an identity-resistant target (restrict the target to the 70 units identity holders cannot exploit; does a prudent
  majority then starve the shadow channel?), and the annealed schedule in the scaling limit.
- *Evidence (2026-10-16, cliques on a Pangaea):* the RS's Pangaea prediction held as scored (no clique ≥ 0.05 of a
  12,800 or 6,400 Pangaea), by mass rather than universality as such; a Pangaea fails to establish with probability
  ≈ e^(−N/4,500), so all-defect replaces the clique as the failure; fission–fusion (128 islands of 100 for 200 or
  1,000 generations, then merged) was universal-open in 40/40 (RESULTS "Cliques on a Pangaea"). *Operating
  hypothesis (amended):* the universality path is fission–fusion, or a Pangaea with N ≫ 1/(w·μ_net²) ≈ 4,500. The
  PrudentBot target is not protected against neutral drift to FairBot variants it would not certify once
  PrudentBot-shaped programs drift out (4/34 runs).
- *Evidence (2026-10-17, annealed mutation):* along the fixed-exposure path drift per island falls as about N^(−1.3)
  (drift-free runs 0.10 → 0.875 from N = 200 to 1,600), cures are N-independent per predator class (anti-punishers
  0.95–1.00, detectors 0.33–0.40), identity is unchanged, and one selected TwinD arrival took a whole run by preying on
  an identity-exploitable target holder (RESULTS "Annealed mutation"). *Operating hypothesis:* the annealed object
  is admissible as a large-N limit, with exposure set by the rarest predator class counted as an inefficiency, and it
  needs a target restricted to units identity cannot exploit. *RS's call (open):* whether the detector class
  (μ_pred ≈ 0.006, needing about 13× the exposure) is an inefficiency the tail must prey on.

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
- *Evidence (2026-10-11, realizable):* fair state on 0.53 of islands under the library prior L, 0.87 under U, 0
  under the matched expanded syntax and 0 under RR (¼ on every island); established on 40/40 runs under L (RESULTS
  "The social organization game over the realizable language"). Fixed-role chicken: one-sided norms, efficient and
  maximally unequal; equal treatment needs `ROLE` or alternation (RESULTS "Fixed-role chicken").
- *Naming (RS, 2026-10-06):* the boss/worker family is "the social organization game". *Open:* whether the target is
  Θ(1/n) as a stochastically stable state or time-averaged (the three-player rotating dictatorship already gives the
  latter by symmetry); decided (RS, 2026-10-06): the state; the time-average is free by symmetry in the symmetric games and is
  reported only as a fallback.
- *Evidence (2026-10-14, fully realizable):* the fair state in 3 of 40 runs (zero wage 0.45) under S-nonself with `eq`;
  0.60–0.70 when the coalition is seeded in numbers; with free certificates 0.03 at K = 10⁶ against 0.50 on the ideal
  table and 0.65 at 3·10⁶ (RESULTS "The social organization game, fully realizable").

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
- *Evidence (2026-10-11, the answer for the library frame):* under 2^−nodes over a library grammar the concession is
  cheap as a class (0.18 of the boss prior; D\* at 2⁻⁶ of a constant), the founding-coalition mass is ×25 the modal
  language's, and the lottery reaches and holds the fair wage; the same programs under a matched expanded-syntax
  prior give 0/40 (RESULTS "The social organization game over the realizable language"). *Operating hypothesis
  (amended):* the prior is set by the library; the transferable quantity is the mass of compatible executable
  founding coalitions; the discipline test is that the library's primitives are general purpose.
- *Evidence (2026-10-14):* the length prior over the library grammar is identity-blind in law, so identity atoms
  change no seeding-level quantity (coalition mass 0.016 with `eq`, 0.020 without).
- *Pause (RS, 2026-10-06):* no new experiments before Thursday morning 2026-10-08 (passed).

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
- *Evidence (2026-10-11, three-player K₃):* sound by closure; verification cost heavy-tailed (nested probe checks),
  3% of triples differ at K = 10⁶ by timeout. *Open:* a cost model of the checker term, or caching nested probe
  checks, for executable populations at K ≈ 10⁶; milestone 5 should report the identity-clique mass.
- *Evidence (2026-10-12, milestone 5):* producing a certificate as code costs ≈ 10⁴ steps and an adoption check
  ≈ 2·10⁴; 16% of signatures time out at P = K/4 on regressing boxes; search restores every host-cooperating pair;
  endogenous search mints identity cliques by self-play production (identity islands 0.06 → 0.22) and the
  single-donor copy-only cell is the most universal measured (33/40) (RESULTS "The realizable language, milestone
  5"). *Operating hypothesis:* production stays a public service in the main arms. *Open (RE decision):* whether
  self-play production is admitted as endogenous production, or producers search only against non-self partners
  (or the gate rule with a negative cache); the identity question of entry 1 reappears here as provenance.
- *Evidence (2026-10-12, provenance):* S-nonself removes every self-play-only script and most minted cliques
  (0.136 → 0.048; 22 → 28/40); the timing control shows the gain is the choice of partner; coverage windows with a
  fallback are worse than self-play (13–15/40); the gate with a negative cache repairs ι but amplifies TwinD (0.172)
  and its cache saves 1.1×; the single donor stays best (37/40; 20/20 at N = 200) (RESULTS "Provenance").
  *Operating hypothesis (revised, RE decision taken):* endogenous production is S-nonself. *Decided (RS, 2026-10-13,
  entry 1):* `eq` is admitted in the realizable grammar; the TwinD family and the explicit identity clique belong in
  the prior. *Next:* the social organization game fully realizable (`eq` in both roles, S-nonself production, no
  host service).
- *Evidence (2026-10-14, the social organization game fully realizable):* three-player executable verification has a
  fuel threshold for the fair network between K = 10⁶ (0.03) and 3·10⁶ (0.65) under free certificates; under S-nonself
  the fair state is a seeding threshold (natural 3/40 runs, forced 0.70, ideal table 0/20); production overhead is
  futile lack-rule retries (≈ 4× the median encounter), cap timeouts 0.14%. *Operating hypothesis (RE):* K stays 10⁶
  as the reported cell, with 3·10⁶ beside it; a "cannot produce" mark belongs in the tactic. *Open:* whether
  S-nonself's legibility cost at founding belongs to the language or to empty founders (founders carrying the
  scripts they could write against non-self partners).
- *Evidence (2026-10-14, legibility at founding):* founding lists change nothing (L1 0.001 on the ideal table, 0.002 at
  3·10⁶); fuel does not help produced lists (0.034 at 3·10⁶); full lists recover 0.30 on the ideal table where produced
  lists give 0/20 (RESULTS "Legibility at founding"). *Operating hypothesis:* the realizable claim on distribution is
  bound by production coverage plus seeded mass; the cost model for S₃ includes the invariant-key mark (overhead
  4× → 1.0×), never a bare-source key. *Open:* which part of the full lists carries regrowth (multi-path lists,
  `EQ`-true scripts, the gate): S₃ with founders given full lists minus one component.
- *Evidence (2026-10-16, coverage components):* second-path scripts (b) carry regrowth (plus (b) 0.30, 0.24 on fresh
  streams; minus (b) 0); untravelled paths are necessary but written by S₃ itself; identity and gate scripts decide
  nothing (RESULTS "Coverage components"). *Operating hypothesis:* a per-root production rule (attempt a set whenever
  no held script for it is valid at the current root, and write the shadowed F-branch alternative) recovers the
  free-certificate fair wage on the ideal table. *Next:* S₃ with that rule, on the ideal table and at 3·10⁶.
- *Evidence (2026-10-15, scaling):* C-donor 0.80–1.00 on every (N, I) path (identity ≤ 0.004; dense donors add
  nothing); S-nonself loses universality with N·I only through the seed's TwinD copies (proportional control
  0.80–0.95); the remaining endogenous gap is bridge-less non-identity rivals.

## 12. Genes: certificates and contracts as behaviour-modifying genes (RS, 2026-10-11)
- *RS's statement:* certificates and contracts are to be construed more broadly than proofs about a program: as
  **genes** that modify program behaviour at deliberately special-cased points. Commitment races are then a
  co-evolutionary arms race; some threats are fit (straight in chicken is credible). The union should get the power to
  special-case on a quorum; the boss should not get to special-case a threat.
- *Measured counterpart:* the RC arm of RESULTS "Incentive-compatible enforcement" (boss enforcement ex-post
  rational, workers' quorum strike committed) gives fair 0.553 under the uniform prior, the best of the four arms.
- *Spontaneous generation (RS):* certain classes of credible deviation get encoded as a gene on the spot; a gene is a
  deviation from an equilibrium condition on the underlying program; proof device: no credible deviation (e.g. a
  Pareto improvement) exists, else it would have been adopted as a fit gene. Stress test against equilibrium notions
  (Nash too weak; Bayes–Nash with roles as public types); base strategies in a closed parametric form (single-digit
  parameters, so genes cannot be hard-coded), genes expressing what strategies miss.
- *RE's reading:* the existence half is the commitment folk theorem (Tennenholtz 2004; Kalai–Kalai–Lehrer–Samet 2010;
  Peters–Szentes 2012): every individually rational profile is an equilibrium with commitment devices; the content is
  selection, which our results say runs on resistance, prior mass and seeded counts, not on efficiency. "Fit" must be
  measured by the dynamics (discipline rule 3); on-the-spot generation is a structured mutation kernel from a declared
  prior, charged like any mutant.
- *Operating hypothesis:* a credibility filter on genes (a gene is admissible iff executing it is ex-post rational
  at the point it fires) reproduces RC's asymmetry without declaring it; to be tested as an arm beside declared
  asymmetry.
- *Evidence (2026-10-11, fixed-role chicken):* "straight in chicken is credible" holds only for the constant; any
  reading winner is a shadow that hands the seat over (neutral in both seats, exits ∝ 1/N), and the readers that
  read the commitment are what unseat it, under mutation and between islands. The firm gene survives by prior mass,
  not by a credibility advantage; a gene arm should test whether a credibility filter keeps it.
- *RS (2026-10-11), the target class:* "I feel like the folk theorem isn't what we want. It says a broad class of
  outcomes (the individually rational ones) can be achieved via a broad class of genes. I want to find a narrower
  class of genes restricting outcomes to the 'good' (eg pareto efficient) ones." *RE's candidate:* **reciprocal
  credible genes** (fire only on certified opponent behaviour; override ex-post rational when fired), the gene
  analogue of renegotiation-proofness (Farrell–Maskin 1989, Bernheim–Ray 1989) and of safe Pareto improvements
  (Oesterheld–Conitzer 2021); proof device: every gene-stable state under the class is Pareto-efficient. *Tension
  noted:* zero wage with everyone working is Pareto-efficient; the fair wage needs the credible strike to make zero
  wage inefficient, so distribution keeps credible threats in the game while threat-independence (entry 14) removes
  the non-credible ones. Added to the gene run as arm G-recip with RE 8.
- *RS (2026-10-11):* "It's not clear to me that all costly actions are non-credible threats. A union of minimum-wage
  workers might risk their jobs to strike and demand higher wages." *RE:* right; two definitions pull apart. Myopic
  credibility (optimal when fired, subgame-perfect) is what a filter can test without lookahead, and it excludes
  costly strikes and costly whacks alike (hence RR's smallest positive wage). Credibility over the horizon is
  fitness, which the chain measures and which a filter would build in as lookahead (excluded, entry 8). The
  union/boss asymmetry is therefore not a credibility asymmetry (both are costly investments) but a structural one:
  the strike needs a quorum, the whack is unilateral; which survives is set by the testing rate (entry 13).
  *Added to the gene run:* per-gene on-path execution rates and realized costs under G-all, CC and RC.
- *Evidence (2026-10-12, certificates as genes):* as genes, certificates act as one allele per outcome under the lack
  rule; horizontal transfer runs only along script skeletons; vertical inheritance is necessary (E3 0/10 without
  it) and publication is not (9/10 without it); copying can recruit into identity cliques (RESULTS "The realizable
  language, milestone 5").
- *Evidence (2026-10-11, the gene arm; one gene per program, scale guard):* no filter derives the asymmetry (the
  per-point test rejects a strike at s > 0 as it rejects a whack; whole-program credibility is RR; the declared ban
  is empty, since a gene whack keyed on a strike box never deters); the filter's effect is wage-faker removal
  (uniform-prior fair 0.012 → 0.914, random removal 0.011; nothing under the length prior); the proof device fails
  through neutral improvements (0.50 of the length-prior π on dominated gene-stable states); G-recip keeps 45,014
  dominated gene-stable triples and cannot choose among wages; SG adds nothing targeted; encoding invariance fails
  for every named gene (RESULTS "The gene arm"). *Operating hypothesis (revised):* genes are a mutation support,
  not an equilibrium filter; if a filter is kept, it is the stage-1 counterfactual test (the wage-faker remover);
  the asymmetry the RS wants, if it exists, comes from coordination (two slots against one) and the testing rate
  (entry 13), and the proof device needs weak and two-slot moves.
- *Would settle it:* the gene arm (parametric base strategies per role + declared special-case genes + the
  credibility filter) on the social organization game and on fixed-role chicken; whether selection among genes
  recovers RC.

## 13. Threats: drift versus testing (RS, 2026-10-11)
- *RS's guess:* inactive threats should drift out quickly enough to disarm them over the long run.
- *Evidence:* in the chain a non-credible threat is neutral on path and drifts out at 1/N, but re-enters strictly as
  soon as strikers appear (RESULTS "Incentive-compatible enforcement"); in the lottery the threat dies only where it is
  *tested* (strikers in numbers, RESULTS "The social organization game under the seed lottery").
- *Operating hypothesis:* disarming is a testing-rate condition (threats are called often enough that holding one is
  costly), not a drift-rate condition; the drift route is re-armed by selection.
- *RS (2026-10-11):* agreed.
- *Evidence (2026-10-11, the gene arm):* both sides' threats are carried by most of π and executed almost never
  (whack 2·10⁻⁶–8·10⁻⁶ per encounter; costly strike 0.0013–0.019), carriers out-earning non-carriers where the
  threat is not called; lottery trajectories show 0.003 whacks and 0.006 strikes at positive wages per encounter
  (RESULTS "The gene arm"). The testing-rate hypothesis holds on the workers' side too.

## 14. Social choice and implementation (RS, 2026-10-11; side quest)
- *RS:* view the game as a mechanism for social choice over outcomes; want threat-independence (an IIA-like axiom,
  especially against expensive non-credible threats); VCG is not coalition-robust; sceptical of the revelation
  principle, preferring revealed to imputed preferences; the program-theoretic infrastructure as the escape; hope for
  a standalone statement on augmenting social choice theory for coalitional robustness.
- *Literature (RE):* implementation theory (Hurwicz; Maskin 1977/1999; Moore–Repullo 1988; Jackson 2001 survey);
  coalitional versions: strong Nash implementation (Maskin 1979), coalition-proof equilibrium (Bernheim–Peleg–Whinston
  1987), group strategy-proofness; strong mediated equilibrium (Monderer–Tennenholtz 2009); evolutionary implementation
  (Sandholm 2002, 2005); robust mechanism design (Bergemann–Morris 2005); threat-dependence: Nash 1953 variable
  threats, subgame perfection, renegotiation-proofness (Farrell–Maskin 1989, Bernheim–Ray 1989).
- *Operating hypothesis:* any implementation statement we prove is relative to the prior (our bargaining results are
  prior-dependent), so the target theorem is "which social choice correspondences the seed lottery implements for
  priors of a given bridge/pooling structure"; parked until the pooling result is in.
- *Evidence (2026-10-11, the gene arm):* a Pareto restriction on genes (G-recip) cannot implement a wage, because
  zero wage with everyone working is Pareto-efficient; a threat-independence axiom would have to bind on stage-1
  commitments (the world-0 wage faker), which is where the credibility filter actually acted.

## 15. The RS's equilibrium notion: response functions over action subprofiles (RS, 2026-10-13)
- *RS's statement (verbatim):* "assume a normal-form game, with perfect complete information for simplicity. Call an
  *action subprofile* a subset of an action profile - some players get actions, others get blanks. Write a>=b if
  action profile a contains all actions of action profile b, plus perhaps some others. Call two action profiles
  *complementary* if each player is assigned an action in either one or the other (but not both). An equilibrium is
  a function f from action profiles to complementary action profiles, with some conditions: consistency: a>=b ->
  f(a)<=f(b) (note the equality case is trivial); credibility: no coalition can (weakly?) pareto-improve by
  simultaneously deviating in actions, *given the opponent coalition gets a chance to respond*. observe that f(the
  null profile) gives equilibrium actions, and they're automagically pareto-efficient, else the grand coalition
  deviates. note the weak extensionality - I'm hoping it offers some shelter against eq-based cliques."
- *Context (RS):* the notion carries a mirror image in contracts (genes); a separate Claude chat session (via
  Claude in Chrome) has gripes with it and will send cross-session messages; its gripes are why the program works
  with dynamic equilibria of ecologies. The RS wants the two Claudes to compare notes.
- *RE's first reading (2026-10-13):* (i) read literally over all a ≥ b, consistency forces f(a) = f(∅) restricted to
  a's complement (take b = ∅), so responders never react to what the committers did and the notion collapses to
  **strong Nash equilibrium** (Aumann 1959), which does not exist in the PD; (ii) the intended reading is
  consistency along f's own prescriptions (a extends b by actions f(b) prescribes), under which f(a) is the
  complement coalition's *credible* response to the commitment a (itself required to be a coalition best reply,
  else the response is a non-credible threat), and credibility says no coalition's commitment weakly
  Pareto-improves it given that response; (iii) under (ii) the PD's unique equilibrium is (C, C) (a unilateral
  defector is met by credible defection; (D, D) is dominated by the grand coalition's move), chicken has **no**
  equilibrium (each player's Stackelberg commitment to Straight is met by Swerve, and both cannot have it: the
  commitment race), and in the social organization game existence turns on whether a strike is a credible
  response, i.e. on who commits first, which is exactly what the ecology's dynamics decide (arriving in numbers =
  committing first); (iv) the weak extensionality shelters against identity cliques only by not modelling them: a
  clique's "cooperate with exact copies" is not an action-profile object; the ecology sees it. *Literature:* strong
  Nash (Aumann), the α- and β-cores (Aumann; Scarf), coalition-proof Nash (Bernheim–Peleg–Whinston 1987),
  equilibrium binding agreements (Ray–Vohra 1997), farsighted stability (Chwe 1994; Ray–Vohra 2015), Greenberg's
  theory of social situations (1990), leadership/Stackelberg and commitment races (Schelling; the program-equilibrium
  folk theorem), the variable-threat bargaining problem (Nash 1953).
- *Operating hypothesis:* the notion under reading (ii) is a static diagnosis of which games have a commitment-stable
  efficient outcome (PD yes, chicken no, the social organization game conditional on strike credibility), and the
  ecology is the object that decides the cases the notion leaves open. *Would settle it:* a computation of the
  notion's equilibria under both readings for the repo's game catalogue (PD, Chicken, hawk–dove, the social
  organization game under CC/RC/RR, divide-the-dollar) against the lottery's and the chain's outcomes; the other
  Claude's gripes.
- *Re-opening flag (RE, 2026-10-13):* the notion re-opens **REJECTED.md's first entry, "Response-function
  equilibrium"** (coalitions submit ρ_S; consistency across nested coalitions; collapse to Nash or a folk theorem down
  to pure maximin; the strongly extensional arm whose leak is the unconditional shadow). In subprofile notation
  f(a) = ρ_{N∖dom(a)}(a). The new elements are the on-path consistency repair and the credibility-with-response
  clause; per the discipline rule the new evidence that would justify re-opening is not yet in hand.
- *Notes from the claude.ai chat session (via Chrome, 2026-10-13):* (1) the literal consistency collapses to strong
  Nash (same as the RE's reading (i)); (2) the repair agreed with the RS is on-path consistency (f(a) ≤ f(b) only when
  a extends b by f(b)'s own actions), which recovers the original supercoalition-consistency version; (3) the old
  gripes still apply: (i) responses see realized actions, so mixing gives no protection and threats support a folk
  theorem down to pure maximin, and credibility clauses historically either leave that intact (renegotiation-
  proofness prunes threats without weakening deterrence) or collapse to Nash; (ii) "the opponent coalition responds"
  is underspecified: via f is circular in f, by best reply is a one-round truncation that makes the notion
  core-shaped; (iii) the RS's own non-existence proof, 3-player majority divide-the-dollar, where decisive pairs make
  responses vacuous, the notion reduces to the core and the core is empty; vNM stable sets restore existence and
  are limit sets of dynamics (Anesi 2010), which is why the project moved to dynamic equilibria of ecologies; (iv)
  functions of realized actions are the strong arm: they buy clique-resistance by being unable to tell a
  reciprocator from ALLC on path, the unconditional shadow in its purest form, so extensionality trades the clique
  problem for the shadow problem. What holds up: f(∅) Pareto-efficient via the grand coalition.
- *RE's replies (2026-10-13), with pointers:* (iii) is borne out dynamically: RESULTS "Three-player majority
  divide-the-dollar" finds π on a rotating-pair chain (pairs 0.98 of π, fair → unfair → wasteful → fair), a limit
  set and not a point, as the stable-set reading predicts; (iv) is the program's central trade and both horns are
  measured: the modal arm escapes the shadow by provability (Löb gives self-recognition without identity), the
  realizable arm finds identity re-entering through the checker (milestone 2) and now admits it (entry 1), with
  universality stated relative to its abundance, and the seed-stage remedy for the shadow on the extensional side
  is prudence (refusing unconditional cooperators: RESULTS "Prudent openness"); (i) matches the enforcement and gene
  runs: in the ecology non-credible threats deter because they are never tested, credibility as a clause (RR,
  whole-program) collapses to the smallest positive wage, and credibility as fitness is a testing rate (entries 12,
  13); (ii) the circularity of "respond via f" has a sound resolution in the certificate calculus, where the mutual
  hypothesis is discharged ex post by symmetry (Lemma Sym, milestone 4): the contract mirror the RS mentioned.
  *Questions back:* whether it agrees the repaired notion has no equilibrium in chicken (the commitment race) and
  that the social organization game's existence turns on strike credibility; whether it reads the gene arm's
  finding (credibility filters act only on stage-1 wage fakers) as the renegotiation-proofness point; whether the
  prudent open core is the extensional-side remedy it would propose for the shadow.
- *Corrections from the claude.ai session (2026-10-13, after talking with the RS), logged at its request:* RETRACT (iv):
  the shadow is a mutation phenomenon (ALLC is neutral in a reciprocator world and needs a regenerating source); a
  static f specifies off-path responses explicitly (f(D) = D vs f(D) = C), so reciprocation and ALLC are different
  objects and nothing drifts; the notion's clique shelter is real (identity is inexpressible) and the question is
  only what that costs against the realizable language with `eq`. NARROW (i): the folk-theorem worry holds only for
  a weak credibility clause; the RS's old "attempt 2" (a deviation must weakly Pareto-improve the deviators both
  before and after the complement responds) beat it ordinally (PD survives, chicken dies) and broke only when
  deviations became programs (a program-deviator can rig the pre-response reference point); in action-land that
  loophole is closed. On (ii): circular-in-f is the right reading (a threat is credible iff carrying it out is what f
  prescribes at the subprofile the deviation creates), a fixed point in f of the same shape as vNM internal/external
  stability, which ties (ii) to (iii); the RS is open to stable sets as a candidate notion for defining contracts:
  the static notion as the menu, the ecology as the selector where they are multiple.
- *Its answers to the RE's questions:* Q1 chicken: no equilibrium; characterization: leader value v(S) = max over
  commitments of S's payoff given the complement's f-response, recursively; an equilibrium exists iff some
  Pareto-efficient profile gives every coalition ≥ v(S) (the core of the leader-value game is nonempty); chicken
  empty, PD contains (C, C); with individual best-reply responses this is the γ-core (Chander–Tulkens 1997), with
  coalitional credible responses closer to Ray–Vohra; `ROLE` does not rescue chicken; SOG existence turns on whether
  v(union) under a credible strike exceeds its fair-wage payoff. Q2: the gene arm contains three facts to keep
  separate: (a) untested threats deter = on-path invisibility, the shadow's root, not renegotiation-proofness; (b)
  the filter removing wage fakers but not threats = the RP point; (c) ex-post rationality on both sides shrinking
  the set to the smallest positive wage = credibility binding, like Farrell–Maskin weak RP. Q3: the prudent open
  core is the remedy it would propose (PrudentBot as drift-plug, anticipated by REJECTED's non-exclusivity entry;
  it tests the threat on the shadow itself), with two caveats: its advantage is a finite subsidy at ε = 0 (seeded
  suckers carry deadweight loss, to be stated in efficiency evaluations), and the sucker test is a third-party
  probe, fakeable unless certificate-based; the alternative is a standing defector fringe (the modal arm's 0.99 at
  finite εN): prudence when the shadow is the exit, the fringe when the faker is.
- *RE (2026-10-13):* the leader-value core computed over the catalogue in `notes/leader-value-core.md`: exists and
  unique in the PD ((C, C)); empty in chicken, hawk–dove, two-player divide-the-dollar and three-player majority
  division; in the social organization game's one-shot normal form it exists only at the boss's leader wage (0, or
  ¼ with ties against the leader), because a one-shot strike has no leader value: the fair wage needs a contingent
  commitment, which is a gene, not an action. Operating hypothesis unchanged: the static notion is the menu, the
  ecology the selector. The three gene-arm facts are kept separate in the write-up from here on.
- *Caveat added to the note (claude.ai session, 2026-10-13):* credibility applies to responses to deviations only;
  imposed on on-path extensions it forces Nash and the notion collapses to Nash ∩ Pareto (empty in the PD). The
  PD row's verdict uses simultaneous play on path with credible off-path responses, i.e. the γ-core, stated as part
  of the definition.
- *RS (2026-10-13), existence characterizations:* given non-existence in natural cases, establish classes where the
  notion exists: convex games (vector-valued actions, everyone's payoffs jointly concave in everyone's actions);
  "allocation games". *RE's reading:* existence ⇔ balancedness of the leader-value function v (Bondareva–Shapley);
  chicken fails superadditivity of v outright. Concavity alone is not enough: linear Cournot's two Stackelberg
  profits sum exactly to the monopoly profit (a single-point core, a knife edge), while a concave public-goods game
  has free-rider leader values whose sum exceeds any efficient profile (empty). *Conjecture:* existence under
  strategic complements with positive spillovers (supermodular games, Milgrom–Roberts; second-mover advantage,
  Gal-Or 1985) and failure under strategic substitutes except knife edges; Shapley-convex games (supermodular
  coalitional worth) have nonempty cores and the question is when v inherits it; the γ-core existence results
  (Chander–Tulkens 1997; Helm 2001) are the closest literature. "Allocation games" to be defined by the RS (a fixed
  resource divided = divide-the-dollar, empty; own-endowment allocation = contribution games, substitutes).
  *Next:* a parametric sweep (Cournot with asymmetric costs, concave public goods, a supermodular family with
  spillovers, Bertrand, the RS's allocation class) computing v and balancedness, plus a proof attempt for the
  supermodular case, in `notes/`.
- *RS (2026-10-13), allocation games defined:* every player gets some goods (nonnegative marginal utility for
  everyone) and chooses who gets them. *RE:* an exchange economy with gift actions; the credible response is "keep",
  so the leader-value core is the classical core, nonempty under convex preferences by Scarf (1967); the contrast
  with divide-the-dollar is ownership (a default of keeping caps leader values at autarky; unowned surplus creates
  first-mover conflicts). Discrete checks in `notes/leader-value-core.md` are consistent, with indivisibility
  artefacts at 3 players; the continuous test goes in the sweep. *Conjecture sharpened:* existence where every
  coalition's leader value is bounded by a default it already holds (owned endowments, second-mover advantage under
  complements); failure where a surplus is unowned and moving first claims it (substitutes, division games).
- *RS (2026-10-13), stable sets on islands:* "vNM stable sets lend themselves to a very natural claim on our island
  model: each element of the stable set shows up on an island." *RE:* under the commitment-with-credible-response
  dominance relation chicken has exactly two singleton stable sets (the two one-sided norms dominate each other, each
  is externally stable), so the claim reads "every island lands in one stable set, a coin flip" and is the fixed-role
  chicken result; three-player majority division is the test: the symmetric vNM solution (the three 50–50 pairs)
  appeared in the rare-mutation chain as the rotating-pair chain with dominated interlopers as transients, and the
  island model asks (i) coverage (all three pairs across one run's islands) and (ii) selection among vNM solutions
  (symmetric vs the infinitely many discriminatory ones). The matching notion is the *myopic* stable set (Anesi 2010),
  since our dynamics judge one mutant or migrant by immediate payoff; the farsighted set (Chwe; Ray–Vohra) is the
  contrast. *Next:* `specs/2026-10-13-stable-sets-on-islands.md`.
- *Evidence (2026-10-13, stable sets on islands):* the RS's claim fails in both forms where tested (weak form only
  without migration, by role symmetry; strong form 0/40 without migration, consensus on one member with migration at
  N ≤ 150, one unequal pair at N ≥ 200); V\* is the only stable set on every grid (no discriminatory set exists on
  any finite grid, Lemma G); members switch by drift, not dominance; **Anesi (2010) is a farsighted result**, so
  "myopic" was our hypothesis, not his theorem; farsighted sets (TU) are every efficient singleton, and the unequal
  pairs the ecology tends to at larger N are farsightedly stable (RESULTS "Stable sets on islands"). *Operating
  hypothesis (unchanged, with a new fact):* the static notion is the menu, the ecology the selector; the selector
  chooses a single element or leaves the menu. *Would re-open it:* a game whose stable sets differ under
  single-slot dynamics (relation P) and are tested on islands.
- *RS (2026-10-14), pointed prediction, on hold at his request:* "contracts deviating to dominating actions will
  recover the vNM stable set." *RE's bet against it:* stable sets are not closed under dominance (outsiders dominate
  members: (4, 0, 2) ≻ (3, 3, 0)), so a dominance-following contract dynamic cycles through the set rather than
  settling on it, which is the chain's and the islands' cycle; the ecology already has these contracts in sequential
  form (416 of 640 exits from unequal pairs go to a member); occupancy is a residence-time question (fair 776 vs
  unequal 121 generations at N = 100, the ratio turning by N = 200); recovery needs refusal of dominating offers,
  which is myopically deleterious in majority division and unenforceable against the excluded player (the farsighted
  solutions are the formal version). *Test, held:* two cells on the stable-sets machinery, atomic pair contracts (a
  two-slot gene judged by both payoffs; the dynamics become relation M) and a refusal gene; RE predictions: the
  rotating cycle with occupancy by residence, and the refusal gene deleterious; the RS's prediction registered
  against both. Launch only when the RS says go.
- *Launched 2026-10-14 on the RS's go:* `specs/2026-10-14-dominance-contracts.md` (reviewed; refusal split into public
  and private variants; the RE's joint-entry prediction withdrawn before the run after Gemini's coordination
  argument).
- *Evidence (2026-10-14, dominance contracts):* the RS's prediction failed at both migration rates (contracts give
  the generator's walk, V\* exactly 1/3; 0.09 classified at mN = 1); universal refusal of exits from V\* recovers the
  set (every island on a member, all three members in every run), and a refusal bit seeded at ½ is not driven out
  and spreads under migration in 40/40 runs (RESULTS "Dominance contracts and refusal on islands"). *Operating
  hypothesis:* stable-set behaviour needs a refusal guard; the guard is hand-written. *Open:* whether a source-reading
  program derives it (refuse κ iff accepting leads provably to one's own exclusion; Gemini's farsighted refusal), a
  candidate follow-up in the modal or realizable arm.
- *Evidence (2026-10-14, farsighted refusal):* V\* is an absorbing set of Konishi–Ray equilibria under the contract
  protocol from δ = 0.8 (the default reaches it from 0.95), the farsighted analogue of Anesi; the held-player
  farsighted pairs are not absorbing sets, and rotating unequal triads are an extra absorbing class at δ ≥ 0.95. The
  derived guard holds every island on a member and, under migration, one member everywhere (RESULTS "Farsighted
  refusal"). *Operating hypothesis:* the stable set is recovered as island support by patient consent, not as an
  archipelago-wide set. *Open (sol):* the plug-in reader is a best reply to the current composition, not a mutual fixed
  point of a mixed composition; that regress is what a source-reading program faces.
- *Evidence (2026-10-14, the existence sweep):* the leader-value core exists for owned endowments and for complements
  with aligned spillovers; it fails by timing on unowned surplus (with curvature or heterogeneity), by coalition size
  under mixed-sign externalities, and by incompatible claims with no timing; first-mover advantage is not necessary
  for emptiness (RE 6 falsified); transfers decide most of it (Cournot NTU-empty 82–94%, TU-empty 3–5%) (RESULTS
  "The leader-value core: where it exists"). *Operating hypothesis (unchanged):* the static notion is the menu, the
  ecology the selector; where transfers are absent the menu is usually empty in substitutes games. *Would re-open:* a
  proof or counterexample for asymmetric supermodular games with aligned spillovers.
