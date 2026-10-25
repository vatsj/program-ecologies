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
- *Asked 2026-10-17, no answer within the 15-minute window; operating hypotheses (RE):* (i) curing the detector class
  is optional, so the tail is set by the anti-punishers and stays light; (ii) the target is narrowed to members identity
  holders cannot exploit (those whose cooperation requires certified cooperation with themselves), tested by a
  prior that moves identity-exploitable target mass to resistant members and by fission–fusion
  (`specs/2026-10-17-identity-resistant-target.md`). Either moves without ceremony if the RS decides otherwise.
- *Evidence (2026-10-17, an identity-resistant target):* the prey channel is real (a TwinD arrival takes an
  exploitable holder's island at ≈ 0.25 per arrival, a resistant one's never) but fired once in 160 length-prior rain
  runs; closing it gains nothing; moving exploitable mass to resistant members raises uot by 0.25–0.33 under rain at
  N ≥ 800, all through the seed, does nothing at (200, 64), and hurts the sponsored PrudentBot, which feeds on the
  exploitable members in the scramble (RESULTS "An identity-resistant target"). *Operating hypothesis (amended):*
  the target stays the full PrudentBot network; narrowing it is not a remedy. The bridge to the RS's prior question is
  the seeded mass of resistant establishers. Fission–fusion fails only when a clique is already a majority at the
  merge (1 of 120 runs).
- *RS (2026-10-17), rivals:* "Detectors seem like a perfectly legitimate network in and of themselves- in fact, they're
  even gentler than prudentbot! They're exploitable, so if we wanted to keep em around we'd need em to evolve
  certificates that predators detect. Worth an experiment imo" and "'Outnumbered networks die' makes me worry we're
  rigging the odds - 'good reasons' to kill off network factor thru dynamics in robust ways. With that in mind,
  proposal to remove prudentbot's state sponsorship? Detectors feel like a legitimate rival". *Decided:* the sponsored
  PrudentBot founder leaves the object (kept only as a reference arm); the target becomes efficient networks that
  survive for good reasons, so network removals are labelled by cause (predation, inefficiency, abundance) and only
  the first two count toward it; selection by abundance (majority at a merge, a Pangaea's coordination) is reported but
  is not a good reason. *RE reading of "certificates that predators detect":* certificates that let detectors detect
  predators (a grudge rule; `specs/2026-10-17-legitimate-detectors.md`).
- *RS (2026-10-17), the prudence premium:* "I'd call prudence a good reason, proportionate to the presence of suckers,
  which is itself a live modeling decision by way of mutation rate / schedule". *Decided:* removals by prudence premium
  count toward the target, reported per unit of sucker exposure; the sucker supply is set by the re-injection schedule,
  so the schedule is a modelling knob on how much prudence is rewarded (at ε = 0 the premium is spent once the seed's
  suckers are eaten).
- *Evidence (2026-10-18, legitimate detectors):* the stored detector is a near-identity clique (its first D certificate
  validates at every root); keying hypothesis-closed D certificates to their production partner (world K) makes it
  gentle, legible and a PrudentBot-network member, dissolves the TwinD cliques (universal-open 11 → 19 of 20 at
  (200, 64)), and gives gentle readers predator mass 0.26; grudges stop tested predators (0/650) and win the equal-mass
  contest 13/20, but detectors are extinct in 19–20 of 20 natural-seed runs; what removes them at equal mass is the
  PrudentBot network's anti-gentle members; with grudges, PrudentBot's loss is abundance (RESULTS "Legitimate
  detectors"). *Decision for the RS:* whether world K (keyed self-hypothesis defection) becomes the realizable arm's
  default production convention; if so, the identity-related cells are rerun under K. *Operating hypothesis:* K is a
  diagnostic until he decides.
- *RS (2026-10-18), world K:* "I'd say adopt it for now and we'll have a broader conversation about certificates soon".
  *Decided (provisional):* world K (hypothesis-closed D certificates keyed to the bare source of their production
  partner) is the realizable arm's default production convention; world L is kept as the reference arm; the
  identity-dependent results are rerun under K (`specs/2026-10-18-world-k-reruns.md`) and receive addenda; a broader
  conversation about certificates is pending.
  *For that conversation (gemini-4-argon, review of the reruns spec):* source-keying replaces a semantic flaw with a
  combinatorial one (one keyed certificate per distinct defector quote, thrashable under a capped list); keying to the
  canonical sub-tree used in the proof is the structural alternative.
- *Evidence and a correction (2026-10-18, identity-dependent results under world K):* as implemented, K's only key is
  the literal ⌜D⌝ (the D step's partner), which no population member carries, so K switches self-certified defection off
  in play; the RE's description to the RS ("counts only against the opponent it was written about") was operationally
  wrong in this grammar. Under K identity vanishes under S-nonself (universal-open 0.75–0.95 at every scaling cell, flat
  in N·I within these cells), self-play production still mints C-identity cliques, the Pangaea's establishment failure
  is not detectably changed, and the anti-punisher network is the residue; certified unconditional cooperators pass
  PrudentBot's ⌜D⌝ guard (RESULTS "Identity-dependent results under world K"). *For the certificates conversation:* a
  variant keyed to population DefectBot sources, or a guard that reads a population defector rather than the literal,
  is the open design question; the combinatorial concern does not arise in K as implemented. *Operating hypothesis:*
  K stays the provisional default on its measured effects.

- *Evidence (2026-10-22, RESULTS "Rewarding prudence under world K"):* a light annealed tail after fission–fusion does
  not deliver the prudence premium as a share at A = 52 per 100 programs (standing suckers 1–4%; guarded members earn
  slightly less in mixtures); at A = 156 the prudent share rises by 0.11–0.19, mostly through residents, with no control
  that isolates a premium. World K and L carry the same per-arrival premium. *Operating hypothesis (unchanged, refined):*
  the premium needs a sucker supply set by the schedule; this schedule's supply is too thin at A ≤ 52. Next levers: a
  depleted control at A = 156, a complete sucker-depletion control, and an exposure scan above 52.

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
- *Decided (RS, 2026-10-23):* self-play production is admitted **in the `eq` wing** and refused outside it. The self-play
  certificate ι is the degenerate Löbian loop, valid only when the two quotes are the same source: it is `eq` written
  as a proof, so the identity tools come as one package per wing (`eq`, self-play production and, by the same
  reasoning, self-keyed hook fills, DEFERRED 12). Consequences: the PD carrier grammar P has no `eq`, so provenance,
  world K, the scaling paths, prudence and hooks Part R are no-`eq`-wing results and stand under S-nonself; the clone
  cell of Part R is read as the `eq`-wing hooks cell; the social organization game fully realizable (`eq` in both
  roles, S-nonself₃) is an `eq`-wing result under the old rule; its S-opp cell (no worker gate) is exactly self-play
  production there and already answers the rerun: no fair run of 20 against about 0.07 persistence under S-nonself₃,
  no greenbeard island, no self-play-only script held (RESULTS addendum, 2026-10-23).
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
- *Evidence (2026-10-18, per-root production):* R2 (per-root lack plus shadowed alternatives) gives 0.40–0.45 of islands
  fair on confirmation streams (free full lists 0.30 on the same 40) with no zero wage, and 0.30 at 3·10⁶ executed;
  median encounter cost 4.1× play from root validation; a capped list thrashed (RESULTS "A per-root production rule").
  *Operating hypothesis:* endogenous production is S-nonself₃ under R2 (root validation, alternatives written first,
  list-free mark). *Open:* a cheaper realizable validation (caching validity per root, or validating only the sets a
  partner reads).
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
- *RS (2026-10-18), two kinds of gene:* "I posit there are 2 types 1. Genes as proofs of behavior 2. Genes as
  overwriting behavior for special cases. How much of 2 can 1 cover by lob's theorem? Is it enough to relegate 2 to a
  wing rather than the main experimental paradigm? ... Note that some special-casing actively contradicts the program
  so can't be covered by proofs". *RE's analysis:* (i) at a *hooked* point (the code defers to its own certificate:
  "if certified to play a against X, play a") every override is a proof gene: the certificate is self-fulfilling by
  Löb and sound because the code obeys it (grudges were exactly such overrides; the unkeyed detector certificate was an
  over-general one, which world K keys back to a special case); (ii) without a hook a proof gene can only certify what
  the code already does (soundness), so a contradicting override is not a gene of type 1 but a different program, the
  code plus a branch, which the program prior already contains; what the override arm adds is a cost model (a cheap
  special case instead of nodes) and horizontal transmission of non-legible patches; (iii) proof genes are legible
  commitments a partner can check, and copying gives them horizontal transmission at hooked points, so within the
  hooked part of program space they cover both halves of the override arm; (iv) caveats: hooks are rare under the
  length prior (own-D readers ≈ 0.03 of the realizable PD prior); self-fulfilling certificates encode threats as
  readily as promises (entry 13 applies unchanged); two-party patches need both parties hooked and the pair rule.
  *Operating hypothesis:* the main paradigm is programs plus proof genes (keyed as in world K); override genes are a
  wing, interpreted as code variants with a different cost and horizontal transmission. *Would re-open it:* a behaviour
  class that needs horizontal transmission of non-legible special cases, or evidence that hook scarcity in the prior
  makes certificate-mediated special-casing negligible where it matters (then the prior, not the gene type, is the
  lever). To be taken up in the broader conversation about certificates (entry 1).
- *RS (2026-10-18), hooks:* "I'm excited about the design paradigm of the modal operator leaving 'hooks' in the base
  program that genes can fill. I'm reluctant to express too much opinion on what kinds of hooks should be expressible -
  at least in this design phase I'd prefer maximalism." *RE:* a hook has four independent parameters (the decision it
  governs; its scope or key: none (L), partner source (K), root (per-root), history (grudges), third party or probe; who
  fills it: self, copying, or both parties via the pair rule; its default). Maximalism with four guardrails that are not
  opinions about hooks: every fill checked (soundness unconditional); one checker-level conflict rule; equal node cost
  for every hook kind (so the length prior does not choose among them); results reported per hook kind with one-kind
  ablations. Expected returns: identity (a fill keyed on one's own source is a clique), self-fulfilling threats
  (entry 13), and verification cost. *Next (on the RS's go):* a design note and a first experiment with a first-class
  hook primitive, maximal fills and one-kind ablations, on the PD and the social organization game.
- *Evidence (2026-10-18, hooks, Part W):* maximal scopes are not neutral in the weak wing: history scope plus pair
  contracts decides outcomes in both games (PD universal-open 1.00 → 0.00 through lineage contracts among default
  defectors; union-game wage ¼ on 0.85 of islands through tested worker grudges); behaviour fills are nearly inert;
  hook leaves alone dilute the provers (RESULTS "Hooks in the weakly extensional wing"). *Decision for the RS:* are
  lineage- or history-keyed overrides and pair contracts admissible in the object? They are the weak wing's analogue of
  identity (entry 1). *Operating hypothesis until he decides:* admissible, reported per kind with strict ablations;
  source ablations use provenance-preserving copies. Part R is still running.
- *Evidence (2026-10-21, RESULTS "Hooks follow-ups in the weak wing"):* with fills keyed on the behavioural open
  predicate ("provably cooperates with me") instead of lineage, the PD lottery recovers in every configuration tested
  (0.875–1.00 universal-open, fission–fusion 1.00); open contracts are rare and unnecessary; in the union game lineage-
  keyed credible-response contracts give no fair island at generation 1,000 and role-keyed ones 8 of 40 runs, while
  protecting the boss's contracted wage alone gives ¼ everywhere. *Operating hypothesis (moved):* behaviour-keyed
  overrides and contracts are admissible and benign in the weak wing; the lineage key is the parochial tag by descent,
  admissible but reported as the identity analogue. *Decision for the RS (narrowed):* admit behaviour-keyed (open)
  fills as a hook scope, given they need only the free sound box?
- *Decided (RS, 2026-10-21):* behaviour-keyed fills are admitted. The family admits PrudentBot's competitors
  (TrustingBot, "cooperate unless you provably defect", which FairBot exploits; the Gödel predator, "defect if they
  provably cooperate", which cooperates with itself and is suckered by FairBot) but no identity, since keys contain no
  quote-equality atom. *Fallback (RS):* if the maximal behavioural-key run (`specs/2026-10-21-behavioural-hooks.md`)
  spooks the RS or the RE, the decision is deferred to Fable 5.5 here.
- *Evidence (2026-10-22, RESULTS "Every behavioural predicate as a hook key"):* at reduced geometry the maximal
  behavioural family gives 0.70 universal-open (inert hooks 0.275, legacy open writes 0.925), no rival network is
  observed, and the recovery needs the prover's guard to be expressible (a-free 0.10). The winners are generous provers;
  prudence does not arise. *RE:* nothing here spooks the admission; it stands. The prudence premium needs a family in
  which prudent keys have prior mass.
- *Evidence (2026-10-23, RESULTS "Hooks in the realizable language (Part R)"):* in the realizable PD under S-nonself,
  maximal hooks give no gain (universal-open 19 / 12 / 11 of 20 for no hooks / inert / maximal at 2,000; on the
  PrudentBot target 16 / 9 / 3); the surviving fills are history fills and identity appears only when fills may key to
  one's own spelling (0.49 strict identity per island in the clone cell). *Decision for the RS:* are self-keyed fills
  admissible? *Operating hypothesis until he decides:* no, by analogy with S-nonself production (provenance); the
  clone cell is reported as a diagnostic.
- *Decided (RS, 2026-10-23):* self-keyed fills are admissible, like `eq` ("feels like eq"). Consequence under the
  2026-10-13 decision: the clone cell's identity islands (0.49 per island, universal-open 0/20, a persistent 7%
  in-island inefficiency) count as cooperation but not as the target, and maximal hooks with self-keys are one more
  identity route whose cost is measured, not excluded. *RE:* S-nonself production is unchanged. It is a rule of the
  machinery (whom certificates are written against), not a strategy the prior offers; self-keyed fills and `eq` are
  strategies, available to selection.

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
- *RS (2026-10-21):* coalition-proof auction theory: VCG is not coalition-proof, our equilibria encode social choice,
  so they might suggest a refinement of VCG, ideally one side-payment rule; the RS's example "2XL" (one toy, two
  players, the loser inflates its value to be paid more). *RE (notes/coalition-proof-auctions.md):* with the seller
  as a player the notion gives the core, and the rule is VCG plus the minimal surcharges that pay no group of bidders
  more than its joint marginal contribution (the core-selecting, VCG-nearest rule already used in spectrum auctions);
  it removes blocking-by-the-seller collusion (losers' and winners' overbids, shills) and opens singleton shading;
  rings are beyond any rule (efficiency, dominant-strategy truthfulness and ring-proofness: pick two), and in the
  notion the seller must be a responding player; on reporting games the verdict turns on whether an indifferent
  loser's spite counts; in open-source auctions ring enforcement and policing are the same program shape; 2XL's
  compensation rule has an empty leader-value core (a commitment race) and the repair is ownership (shared ownership:
  Cramton–Gibbons–Klemperer). *Operating hypothesis:* the side-payment answer is the surcharge rule, with the ring
  frontier as the open question the program setting can address (CLAUDE.md queue item 48).
- *Evidence (2026-10-21, RESULTS "Coalition-proof auctions"):* the surcharge buys core membership w.r.t. reports and
  nothing more: every winner with a price-setting loser is a ring under both rules (truth robust on 0/3,000 in
  substitutes), spite deters same-side coalitions only, and in an ecology singleton shading is selected under the
  surcharge (efficiency 0.48); police are a payoff-neutral shadow (ring suppression is founder share), the reading audit
  ends enforced losers' rings but is no general remedy; under first-price a responder exploiting underbidders is
  selected. *RS (2026-10-21):* the relevant program is to rediscover the core in our machinery; stage 1 is queue item 49. *Stage 1 evidence (RESULTS "Rediscovering the core"):* the ε = 0 first-price lottery stops about 4 ticks short of the core price; the losing bidder's honest threat is selected out early; rain or migration restores about half the islands; a best-reply responder works only as the last mover. *Operating hypothesis:* stage 2 gives the responder a certificate semantics (checked mutual reading, as in milestone 4) before moving to private values. *Stage 2 evidence (RESULTS "Rediscovering the core, stage 2"):* certified threats hold the price against non-following item programs (0.62–0.70), but accommodating followers untest and freeze them (0.08); rain did not restore the test. *Open:* a threat-testing mechanism, or followers that stay exploitable until the threat is tested; the RS's call whether accommodation of a read commitment is a legitimate program behaviour or a ring. *RS (2026-10-22):* the equilibrium notion should recover VCG when VCG is in the core; a secondary thread, with weaker normative weight, recovers optimal auctions with the seller as a player; not to dwell on auctions. *RE:* within the core, VCG is the unique bidder-optimal point when VCG is in the core, so recovering it is the bidder-optimal selection: bidders lead and the seller follows (Bernheim–Whinston's coalition-proof first-price outcomes). Optimal auctions are the same notion with leadership flipped (the seller commits); they need private values and are inefficient by design, so they conflict with the efficiency the grand-coalition clause builds in and stay an evaluation, not a target. Other preferences: hold efficiency, participation and shill-robustness (identity manipulation, the clique problem in auction form); revenue monotonicity comes free from the core; drop truthfulness (incompatible with core selection unless VCG is in the core, and tied to the revelation principle); equal treatment as a tie-break only. *Operating hypothesis:* the auction target is core outcomes with bidder-optimal selection, outcome-level under complete information.

- *RE (2026-10-23), stage 3 parked:* a seller program was the proposed next step, and working it out shows two
  routes, neither cheap. (a) A seller that follows the bids and may recontract with the loser (offer it the bundle at
  a price q it accepts up to its value) puts P's acceptance level under test only while winners underbid; once
  winners read and accommodate the seller's offer, it is untested and drifts, as the threat did in stage 2. (b) A
  seller that leads by posting a reserve read by followers is selected up to the seller-optimal core point (revenue 30
  in threshold), the secondary thread, not the bidder-optimal point the RS prefers (20). So the thread hinges on the
  RS's open call (is accommodation of a read commitment a ring?), not on another run. *Operating hypothesis:* parked
  until the RS asks; the RS's attention moved to mixed actions (entry 16).
- *RE derivation (2026-10-24, the RS asked whether the ring question follows from existing rulings; pending the RS's
  confirmation):* accommodating a read commitment is admissible *behaviour* (the line of the `eq`, behaviour-key and
  self-keyed-fill admissions: realizable behaviour is in the ecology and outcomes are judged); its *outcome* at a frozen
  threat below the loser's value is outside the RS's notion (DEFERRED 15 with the seller as a player gives the core,
  and {seller, loser} blocks any revenue below v_P even after the winners respond); and it survives by being untested,
  which the 2026-10-17 target ruling does not count as a good reason. So stage 2's state is a failure of the dynamics,
  not a legitimate outcome, and the auction thread's remaining question (what tests a read commitment?) is the
  prudence premium's (entry 1).

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

- *RS (2026-10-24), target for majority division:* "all island outcomes are efficient and all stable sets show up";
  "I'd like our island models to be expressive enough for the entire stable set to coexist. Disconnected components
  reduces my goal to 'everything shows up w some probability' for ~free so I'll allow it for the time being", with
  the caveat that "the disconnected components will still have to be large in general, else we won't have meaningful
  migrant effects". *Operating hypothesis:* components of at least 16 islands count; coexistence within one large
  connected component is the goal (queue 60, 61).
- *Evidence (2026-10-25, RESULTS "A migration window for stable sets on islands"):* migration alone gives no window
  in one connected component; the hand-written veto meets the stated target at every migration rate tested; the
  derived farsighted guard only at mN ≤ 0.003; 16-island components help at N = 200, mN = 0.1 but never reach V\*.
  Next: a derived immigrant-rejection guard (queue 61).
- *Evidence (2026-10-25, RESULTS "Deriving immigrant rejection, Step 0"):* the veto keeps all three fair pairs present by
  churn (islands rotate members through fair-to-fair contracts), not by rejecting immigrants; a farsighted table with
  weak consent matches it (1.00 / 1.00 / 0.90). *Decision for the RS:* does coverage by churn, with islands changing
  member about every 150 generations at mN = 1, count as "all stable sets show up"? *Operating hypothesis:* yes at a
  snapshot, reported with the churn rate; the locking candidates are set aside.
- *RS (2026-10-25):* the veto is "an experimental artifact rather than a core part of our equilibrium notion"; the churn
  must be shown in the primary object (extensional or Turing-complete) to count (queue 64). The stored primary-object
  runs (weak and modalPA, n = 6) kept no coverage under migration.
  *Result (2026-10-25, RESULTS "Churn among the fair pairs in the primary object"):* with flexible readers seeded
  (library priors, 9–16%) the DSL and the Turing-complete arm churn without contracts (2.8–21× the baseline's flips) and
  put 0.89–1.00 of islands on a fair pair at mN ≥ 0.1, but no cell keeps all three pairs present at mN = 1; the n = 10
  length prior does not churn. *Operating hypothesis:* the target's efficiency half is reachable without the veto;
  coverage under steady migration is not, in the primary object as tested, and needs either founders (low mN),
  components, or a mechanism that resists consolidation (the veto's refusal of exits plays that role).
- *RS (2026-10-25):* islands must not be transient; the limit should be crisp. Order of limits proposed: annealed
  mutation (decaying, finite total) to bring predators, migration → 0 more slowly than mutation, and the number of
  islands → ∞ before time (preferred over disconnected components, "the sharper choice deriving a stronger
  statement"); anything needing several simultaneous migrants is eventually lost, as with mutants. *Operating
  hypothesis:* the object for coverage of the stable set is lim_t lim_I of the rare-migration jump chain after an
  annealed tail; tested in queue 65.
- *RS (2026-10-25), contract genesis:* contracts should form per encounter on the programs that stand to benefit, not
  by an aggregate test over the population, and only replace actions "at that point" (situation-keyed overrides that
  stay silent elsewhere); a coalition deviates when it Pareto-improves after the responders answer its new actions
  ("the responders get to see the contracts mutate into existence, and they only actually do if they earn their
  keep"); this is the extensional wing's reading of "the opponent coalition gets a chance to respond" in the notion
  above; best-reply response is the control; no farsighted arm; holders need not meet each other. *Operating
  hypothesis (RE):* the situation key is the encounter's program-action profile, the response one round by
  behavioural substitution, further reactions through later contracts (queue 66).
- *RS (2026-10-24):* component size matters little here, "since there's only 3 real candidate equilibria to choose
  from. It'll matter more in games w good migrants - maybe PD?" *RE:* in the PD migration carries good migrants
  (fission–fusion universal 40/40, one donor per island, bridge-mediated merging), so component size trades
  per-component establishment against rival lock-in at component boundaries; an optional follow-up (queue 61).

## 16. Mixed actions and adversarial games (RS, 2026-10-23)
- *RS:* "I suspect we're gonna need strong notions of mixed actions to recover equilibria in adversarial games. I
  propose rock paper scissors for starters? We should recover the mixed-strategy equilibrium pretty
  straightforwardly."
- *Open (the RS's call):* what a mixed action is in the object: a population mixture of pure programs, a private coin
  read only by simulation, or a coin whose distribution exact readers see; and what non-termination yields (forfeit or
  a uniform action, the latter a coin built into the evaluator). *Operating hypothesis:* run all three as arms with
  forfeit as the main rule (`specs/2026-10-23-rps-mixed.md`); "recovery" means unexploitable individual play, not
  uniform time-averaged play, which symmetry gives for free.
- *Evidence (2026-10-23, RESULTS "Rock–paper–scissors and mixed actions"):* under forfeit, the seed lottery is held by
  readers whose self-play forfeits (the stochastic arms forfeit 0.52–0.69 of plays, the pure arm all), so the ecology
  reaches the value by mutual non-play; the chain approaches unexploitable mixing only near N ≈ 10⁷; exact reading
  adds nothing; a uniform default manufactures mixing without protection. *Open for the RS:* is mutual non-termination
  an admissible tie, or should non-play cost something (which a zero-sum game cannot express without changing the
  game)? and should the next test be a non-zero-sum game with an RPS-like cycle, where a reader could earn its place
  against the coin?
- *Decided (RS, 2026-10-23):* non-play is not free ("compute costs nontrivial"); the default depth price (a forfeit
  costs the cap) was accepted. *Evidence (RESULTS "Rock–paper–scissors with a compute price"):* forfeits vanish at
  c = 0.01, individual mixing reaches 0.85–0.93 of the lottery, and the free coin `X` holds most of it; the exact reader
  adds nothing. *Open:* whether a realizable language offers a randomizer that opponents can see and simulate but not
  predict, free to its user; the next tests are the inspection game (queue 55) and Basic Endgame in poker (queue 56),
  where reading the other side's randomization can be worth more than flipping blind.
- *Evidence (2026-10-24, RESULTS "Mixed actions in two-role games"):* in the inspection game reading pays in proportion
  to what the reader sees; with both roles reading the lottery's modal island is the efficient outcome (a responsive
  inspector over compliant constants), commitment appears when only the inspectee reads, and the chain loses the
  efficient pair to the inspector's unconditional shadow; Basic Endgame's equilibrium is not recovered in any arm.
  *Open:* whether a realizable reader keeps the responsive inspector unfakeable (the DSL cannot tell simulation from
  play; `cr` is a free oracle).
- *Evidence (2026-10-24, RESULTS "A private random tape in the realizable language"):* the RS's private tape is a sound
  realizable randomizer, but at the calibrated step price simulators hold the RPS lottery and the inspection islands,
  because a timed-out read returns a default rather than forfeiting; the coin wins at about 80× the price. *Open for
  the RS:* the timeout convention (what a timed-out read returns: the reader's default, a forfeit of the reader, or a
  charge) and the price scale; and whether the checker should become library code (milestone 4's convention).
- *RS (2026-10-24), compute cost:* "I'm comfortable with a capped simulator primitive. It's a bash command and we're
  aiming for Turing-completeness, so I see no principled reason to withhold it." On pricing failure rather than work:
  "it points the finger more directly at the reason we need the restriction in the first place: infinite loops. I
  don't think I have an answer to your question; I'm hoping we find experiments that answer the question for us."
  *Operating hypothesis:* the timeout convention stays (a timed-out read returns to the reader); the cost notion is
  open, informed by queue 63's cross-game robustness test.

