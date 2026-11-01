# Operating hypotheses

The ledger of operating hypotheses and of the theorems and desiderata we test on them. It replaces the tracker artifact
(RS, 2026-11-01: "make it markdown … I'd like to hand-edit alongside you").

**How to edit.** Both of us edit this file directly; git resolves conflicts.
- Each hypothesis carries its state (*decided*: the RS's call; *operating*: acted on, not defended; *provisional*) and
  its source in DEFERRED.md.
- Each criterion is a checkbox: `[x]` means done (proved, or settled for the program's purposes). The bold label gives
  the kind (theorem / desideratum) and the status (proved, supported, partial, open, refuted).
- The RE updates entries whenever a RESULTS section or a DEFERRED decision changes them, citing the section.
- The **Games** section at the end records what happens in each game we have tested.

## Object and target

### h01. The seed lottery is the object

*Decided* · DEFERRED 1 · RS 2026-10-04, 2026-10-10, 2026-10-16, 2026-10-17

For the Turing-complete goal the object is the seed lottery: islands seeded i.i.d. from the prior (the annealed schedule's ε = ∞ start), then selection and migration under a light, vanishing mutation tail that trickles in predators and suckers (h03), with P(efficient) → 1 along a path in (N, I). The pure ε = 0 lottery is the tail-free reference case; the stationary ε → 0 chain under rare mutation is kept as a diagnostic and as the stress test for unfakeability.

- [ ] **Theorem, supported.** Island-level efficiency: along the seed path, the probability that every island ends efficient tends to 1.  
  Evidence: Holds on every (N, I, mN) path tested (RESULTS “The realizable lottery along paths in (N, I, mN)”); no proof.
- [x] **Theorem, proved.** Lemma D′ (the scramble): for any lineage and stopping time, demography and selection form one martingale.  
  Evidence: RESULTS “The demographic lemma”.
- [x] **Theorem, proved.** Establishment is positive uniformly in the cutoff n (μ_est ≥ 0.0207 in the modal arm).  
  Evidence: Rigorous lower bound, RESULTS “Almost all seeds: the tail in n”.
- [ ] **Theorem, supported.** Per-island establishment p(N) → 1 at a fixed cutoff.  
  Evidence: Formula derived (near-critical founders, then pooled two-type escape); 0.98 at N = 25,600 (RESULTS “The demographic lemma”).
- [x] **Theorem, proved.** Corollary 1 (the leak x → FairBot → ALLC → D) does not bind at ε = 0; under the annealed tail it binds only through drift colonization.  
  Evidence: The leak needs ALLC re-supplied; at ε = 0 it is eaten once and never returns (DEFERRED 1). Under the tail, re-supplied ALLC can open it only by drifting in, which vanishes as about N^(−1.3) (h03, RESULTS “Annealed mutation”).

### h02. Efficient networks that survive for good reasons

*Decided* · DEFERRED 1 · RS 2026-10-15, 2026-10-17

The target is universal cooperation on the PrudentBot network, with no state sponsorship. A network may be removed by predation, by inefficiency, or by the prudence premium (in proportion to the sucker supply the mutation schedule sets); removal by abundance alone does not count. Identity cliques count as cooperation, not as the target; detectors are a legitimate rival.

- [ ] **Desideratum, partial.** Universality along growing (N, I) paths at a fixed prior.  
  Evidence: World L: goes to 0 with seeded clique copies (crossing near 6 at N ≥ 200). World K under S-nonself: universal-open 0.75–0.95 at every scaling cell (RESULTS “Identity-dependent results under world K”).
- [ ] **Theorem, partial.** No bridge-less rival family under the default reader.  
  Evidence: Free box: a quarter of rival mass (the P* family) is bridge-less, so universality fails along I ≫ N at N ≥ 200. Bounded prover K at b ≥ 12: 0/3,000 separations (RESULTS “Rivals under the bounded prover K”).
- [ ] **Desideratum, open.** The prudence premium is delivered by the dynamics, in proportion to the sucker supply.  
  Evidence: No premium at A = 52; a rise at A = 156 without a control that isolates it (RESULTS “Rewarding prudence under world K”).
- [ ] **Desideratum, partial.** Rival networks are removed for good reasons, not by abundance.  
  Evidence: Cliques lose on a Pangaea by mass (abundance); fission–fusion is universal in 40/40 (RESULTS “Cliques on a Pangaea”).

### h03. Mutation stays in the object as an annealed tail

*Decided* · DEFERRED 1 · RS 2026-10-15, 2026-10-16, 2026-10-17; RE 2026-10-17

Mutation starts at ε = ∞ (which generates the seed) and decays. The tail is kept as the channel that trickles in predators and suckers: it lets predation remove exploitable rivals and sets the sucker supply that the prudence premium is paid from. It is admissible where drift never colonizes an island while selected arrivals do (RS: “drift should never colonize an island, only reintroduce fit programs”). The clean object is the large-N scaling limit, with exposure set by the rarest predator class; the schedule's form is a modelling knob.

- [ ] **Desideratum, supported.** Drift colonizations vanish while selected cures persist.  
  Evidence: Drift falls as about N^(−1.3) along the fixed-exposure path; cures are N-independent per predator class (RESULTS “Annealed mutation”).
- [ ] **Desideratum, partial.** The target cannot be taken over through identity-exploitable holders.  
  Evidence: The prey channel is real and narrow; narrowing the target buys nothing (RESULTS “An identity-resistant target”).

## Reading and realizability

### h04. Source reading through a sound checker of carried certificates

*Operating* · DEFERRED 2, 5 · RE, refined 2026-10-06

Programs read each other's source through a shared sound checker of carried scripts (certificates as code). Soundness buys unfakeability; Löb buys self-cooperation without an imposed fixed point. The checker is a convention, as the proof system was.

- [x] **Theorem, proved.** Lemma 0: soundness buys unfakeability, Löb buys self-cooperation.  
  Evidence: RESULTS “Conjecture 4: the sibling theorem”.
- [x] **Theorem, proved.** Sibling theorem: no class in the unbounded modal language is drift-closed; the obstruction is extensionality, not GL.  
  Evidence: RESULTS “Conjecture 4: the sibling theorem”.
- [x] **Theorem, proved.** Universality and drift-closure are exclusive, and β = 1/2.  
  Evidence: Proved in the pure PD (RESULTS “Universality against drift-closure”).
- [ ] **Theorem, supported.** Checked carriers are sound unconditionally; the pair rule is sound by symmetry, not by self-fulfilment.  
  Evidence: Argued in RESULTS “The realizable language, milestone 4”; 0 false atoms in populations (milestone 2). Not written as a proof.
- [ ] **Desideratum, supported.** Distinct source-readers cooperate within realizable fuel.  
  Evidence: Checks of 2–4·10⁴ steps under a shared checker (milestone 4).

### h05. The realizable language admits identity

*Decided* · DEFERRED 1, 12 · RS 2026-10-13, 2026-10-23

L_T admits `eq` and self-keyed hook fills; identity cliques are part of the ecology. The defended claim is island-level efficiency along the seed path plus universality relative to identity's seeded abundance and the (N, I) geometry.

- [ ] **Desideratum, supported.** Every island stays efficient when identity is cheap.  
  Evidence: Identity cliques hold 0.41 of islands and every island is efficient (RESULTS “Identity and tags in the carrier grammar”).

### h06. World K is the certificate convention

*Provisional* · DEFERRED 1 · RS 2026-10-18

Hypothesis-closed D certificates are keyed to the bare source of the partner they were produced against; in the realizable PD grammar this switches self-certified defection off in play. World L is the reference arm. A broader conversation about certificates is pending.

- [ ] **Desideratum, supported.** K removes identity cliques under S-nonself.  
  Evidence: Universal-open 0.75–0.95 at every scaling cell (RESULTS “Identity-dependent results under world K”).
- [ ] **Desideratum, open.** K's effect does not hinge on the literal DefectBot quote.  
  Evidence: As implemented K's only key is the literal quote; keying to population defectors or to the proof's sub-tree are the alternatives (DEFERRED 1).

### h07. Endogenous production: S-nonself under the per-root rule

*Operating* · DEFERRED 11 · RE 2026-10-18; RS 2026-10-23

Programs produce their own certificates as code, never against their own copies (S-nonself; self-play production only in the `eq` wing), and re-produce whenever no held certificate is valid at the current root (R2).

- [ ] **Desideratum, supported.** The realizable PD lottery is universal.  
  Evidence: Every run at (100, 64) once the seed's TwinD mass moves to the prudent core (RESULTS “Provenance”).
- [ ] **Desideratum, partial.** The fully realizable social organization game reaches the fair wage.  
  Evidence: 0.40–0.45 of islands on the ideal table, 0.30 at 3·10⁶ fuel; encounters cost about 4× play (RESULTS “A per-root production rule”).
- [ ] **Desideratum, open.** A cheaper realizable validation.  
  Evidence: Caching validity per root, or validating only the sets a partner reads (DEFERRED 11).

## Compute

### h08. Default compute charge: A_f at P_fail = 0.1

*Decided* · DEFERRED 16 · RS 2026-10-25, 2026-10-28

A timed-out read and a forfeit each cost P_fail = 0.1, one charge per failure event, with the game's own forfeit payoff kept. A read that finishes is free whatever its budget. Cheaper reads have no wing for now.

- [ ] **Desideratum, supported.** RPS is met by unexploitable individual mixing.  
  Evidence: Exploitability 0.000 from 0.1 to 1, held by a guarded mixer (RESULTS “Charging forfeits like failed reads”).
- [ ] **Desideratum, supported.** The PD target is unaffected.  
  Evidence: 37/40 at 0.1 (same section).
- [ ] **Desideratum, open.** The inspection target is met.  
  Evidence: 40-run cells undetermined (0.64–0.71); met only on post-hoc pooled readings.
- [ ] **Desideratum, supported.** The charge sponsors no solution.  
  Evidence: The security fallback A_m was rejected because it sponsors the coin at 0.03–0.1.
- [ ] **Desideratum, supported.** Majority division is unaffected.  
  Evidence: V* unmoved by the charge in arm T (RESULTS “Arm T under islands to infinity before time”).

### h09. Prices are harmless only below N^(−1/2)

*Operating* · DEFERRED 4 · RE

Verification is amortized and behaves as free proofs (the α = 1 path). A price is harmless in the limit iff it vanishes faster than N^(−1/2) of the stakes or is zero on the ladder's rungs; copy subsidies are moats.

- [ ] **Theorem, supported.** Along c_N = c₀·N^(−α), cooperation → 1 iff α > 1/2.  
  Evidence: The chain follows the two-edge reduction (RESULTS “Price scaling paths”).
- [x] **Theorem, proved.** Proposition 3: with free constants, a price beats 1/N only through incumbency.  
  Evidence: RESULTS “Universality against drift-closure”.

## Distribution and stable sets

### h10. Fixed roles, separate slot populations

*Decided* · DEFERRED 3, 6, 10 · RS 2026-10-04, 2026-10-06

Every social-choice question uses fixed roles with one population per slot; `ROLE` is kept only as the symmetric control. The distributional target is a fair division as a stable state, and results are stated relative to the prior, the commitment structure and the seeding.

- [ ] **Desideratum, partial.** A fair division as a stable state in the social organization game.  
  Evidence: Fair wage on 0.53 of islands under the library prior; 0/40 under a matched expanded syntax (RESULTS “The social organization game over the realizable language”).

### h11. Stable sets: every island in V*, members equally likely

*Decided* · DEFERRED 15 · RS 2026-10-25, 2026-10-29, 2026-10-31

In majority division every island lands in the stable set V* (the three fair pairs; the grand coalition reported separately), each member equally likely across independent worlds; a lottery across worlds suffices. The object is lim_t lim_I of the rare-migration chain after an annealed tail. Farsighted clauses are out of the object.

- [x] **Theorem, proved.** The symmetric vNM set is the unique stable set of three-player majority division on every even grid.  
  Evidence: Odd grids have none (RESULTS “Stable sets on islands” and addendum).
- [ ] **Theorem, partial.** In the mean field every island ends in V*.  
  Evidence: Holds from starts on the fair side of a boundary the library sets, not from every start. Arm T: no crossing up to an unequal share of 0.95. Constants alone cross near 0.69, and the length-prior DSL arm M's natural start lies inside its basin (RESULTS “Arm T under islands to infinity before time” and addendum; “Where the unequal basin comes from”).
- [x] **Theorem, proved.** Each member of V* is equally likely across worlds.  
  Evidence: By the rotation symmetry of game and prior; observed 44 / 54 / 57 over 155 worlds.
- [ ] **Theorem, supported.** The state with all three pairs present is a knife-edge.  
  Evidence: Jacobian λ = 5.56·10⁻⁴ per event on the non-invariant sector, matched by perturbations (same section).
- [x] **Desideratum, supported.** Explain the unequal basin of the length-prior arms.  
  Evidence: The constants already have the unequal basin (crossing near an unequal share of 0.69). Two Trojan-bully programs per slot (on-path fair, exploit ⅓-offerers) lower it to 0.55 (L) and 0.425 (M, under M's natural 0.429); fair readers raise it. Each outcome is a ratchet. Mechanism partly inferred, on a validated truncation (RESULTS “Where the unequal basin comes from”).
- [ ] **Desideratum, refuted.** Myopic encounter contracts reach V*.  
  Evidence: A rotating walk, 0.40 fair (RESULTS “Contracts that form in encounters”).

## Threats, commitments and mixed actions

### h12. Disarming threats is a testing-rate condition

*Decided* · DEFERRED 13, 14 · RS 2026-10-11, 2026-10-29

An untested threat is not disarmed by drift (it re-enters as soon as it pays); it dies where it is called often enough to cost its holder. Accommodating a read commitment is admissible, and a frozen, untested threat below the core price counts as a failure of the dynamics.

- [ ] **Desideratum, supported.** Threats die where they are tested.  
  Evidence: Strikers arriving in numbers kill the whacker within 25 generations (RESULTS “The social organization game under the seed lottery”).
- [ ] **Desideratum, open.** Something tests a commitment everyone accommodates, so the core price holds.  
  Evidence: Followers freeze a certified threat near 13 against the core price 20 (RESULTS “Rediscovering the core, stage 2”).

### h13. Mixed actions: recovery means unexploitable individual play

*Decided* · DEFERRED 16 · RS 2026-10-23

A mixed equilibrium is recovered when individual programs play unexploitably, not when the population's time average is uniform, which symmetry gives for free. Non-play is not free.

- [ ] **Desideratum, supported.** RPS: individual mixing in the lottery.  
  Evidence: Under A_f, a guarded mixer holds RPS at every price 0.03–10 (RESULTS “Charging forfeits like failed reads”).
- [ ] **Desideratum, partial.** Inspection game: the efficient outcome holds.  
  Evidence: The lottery's modal island under a responsive inspector; the chain loses it (π(E) 0.047 at N = 10⁵; RESULTS “The inspection game's enforcer and its shadow”).
- [ ] **Desideratum, refuted.** Basic Endgame: the mixed equilibrium is recovered.  
  Evidence: Bluff 0.15 against 0.25, call 0.39 against 0.5 (RESULTS “Mixed actions in two-role games”).

### h14. The RS's equilibrium notion is a static menu

*Operating* · DEFERRED 15 · RE 2026-10-13

Read along f's own prescriptions, the response-function notion diagnoses which games have a commitment-stable efficient outcome; the ecology decides the cases it leaves open.

- [ ] **Theorem, supported.** Under reading (ii) the PD's unique equilibrium is (C, C) and chicken has none.  
  Evidence: The RE's argument (DEFERRED 15); not written as a proof.
- [ ] **Desideratum, refuted.** The ecology respects the static menu.  
  Evidence: 0.72 of islands sit on dominated outcomes without migration (RESULTS “Stable sets on islands”).

## Games

What happens in each game we have tested, by object, with the programs that decide it. Objects: the **seed lottery**
(islands seeded from the prior, then selection and migration; tail-free unless said), the **ε → 0 chain** (stochastic
stability under rare mutation, the diagnostic), and **islands → ∞ before time** (the exact mean-field ODE on island
states, majority division only). Arms: the weak DSL, the modal DSL (a free sound provability box), the bounded prover
K, and the realizable Turing-complete language L_T.

### Prisoner's dilemma

The main game. Target (h02): universal cooperation on the PrudentBot network.

- **ε → 0 chain.** The weak arm fails in the limit: cooperation peaks near N ≈ 10³ and falls like N^(−½). Two exits:
  - the unconditional shadow (ALLC drifts into a reciprocator world, then is eaten), whose exit vanishes as 1/N;
  - the faker, whose exit is N-independent and binds.

  The modal arm rises with no peak, to 0.73 at N = 3·10⁴, because sound provers are unfakeable. Löb gives
  self-cooperation (FairBot), soundness gives unfakeability. In any quoting language, source identity makes a
  drift-closed CliqueBot that absorbs the chain, so the chain is parochial by construction.
- **Seed lottery.** Islands end efficient on every path tested. Universality is the hard part:
  - the P\* family (cooperates iff provable from PA + Con) forms bridge-less permanent rivals under the free box; the
    bounded prover K removes them;
  - identity cliques decide universality in the realizable language through their seeded abundance.
- **Realizable language.** Checked carried certificates restore cooperation between distinct source-readers (2–4·10⁴
  steps), with unconditional soundness. Refusing self-play production (S-nonself) and world K remove most identity
  cliques: universal-open 0.75–0.95.
- **Programs that decide it:**
  - FairBot (Löbian self-cooperator, the establisher);
  - PrudentBot (cooperates with FairBot, exploits ALLC; the target network);
  - ALLC (the shadow);
  - the Gödel-sentence faker (removed by K);
  - P\* (the bridge-less rival);
  - CliqueBot / TwinD (identity).

### Chicken and hawk–dove (fixed roles, no `ROLE`)

- **Lottery.** Constants alone learn one-sided norms (one slot firm, the other yields) on 0.78–1.00 of islands, split
  ½/½ between the two orientations across islands.
- **Chain.** The firm constant is the only uninvadable winner. Conditional straights are neutral bridges that unseat it
  (exits ∝ 1/N) and merge island norms under migration; the winner is a coin flip.
- **One population.** It cannot learn the norm. This holds for chicken and hd3 at N = 10⁴, and not for hd3 at 10³
  (exploration-cap audit).

### Two-player divide-the-dollar (`dollar5`, `dollar3` two-player)

- **Fixed roles, chain.** π is a rotating dictatorship of the largest demand: 0.99 on the endpoint splits (1/6 | 5/6),
  by an accommodator ratchet.
- **One population, chain.** 50–50 is a finite-N state and loses to greedy hawk polymorphisms by N ≈ 10⁴. Under the
  modal box, Löbian hawks (meek with their copies) make a deep trap at 0.65 efficiency.
- **Lottery.** 50–50 is the modal island in every role structure, and nearly universal with one population and
  migration (risk dominance, crossing 3/8).
- **The two objects disagree on distribution.** The lottery gives the fair state; the chain does not.

### Three-player majority division (`dollar3`)

**The game.** Each slot names a partner (or all three) and a demand in {⅓, ½, ⅔}; two slots that name each other with
compatible demands split, and the third gets 0. Target (h11): every island lands in V\* (the three fair pairs), each pair
equally likely across worlds.

**Framing note: the ⅓ – ½ – ⅔ grid.** Inside one pair the three demands play a Nash demand game, not a dilemma:

| row \ column | ⅓ | ½ | ⅔ |
|---|---|---|---|
| ⅓ | ⅓, ⅓ (wasteful) | ⅓, ½ (wasteful) | ⅓, ⅔ (unequal) |
| ½ | ½, ⅓ (wasteful) | **½, ½ (fair)** | 0, 0 (disagreement) |
| ⅔ | ⅔, ⅓ (unequal) | 0, 0 (disagreement) | 0, 0 (disagreement) |

Read the demands against the PD: ½ is cooperation, ⅔ is defection, and ⅓ is submission. Three consequences frame every
result in this game:

1. **The fair demand enforces itself.** In the PD, cooperating against a defector is the sucker's payoff, so
   cooperation needs reading to protect it. Here, insisting on ½ against ⅔ ruins both players: the fair demand is
   already a grim punisher, and a constant can hold it. That is why nine constants alone reach V\* from a fair start.
2. **Exploitation needs a submitter, and submission is a best reply.** ⅔ pays only against ⅓, and ⅓ is the best reply
   to a committed ⅔. So the unequal pair (⅔, ⅓) is a second equilibrium, as efficient as the fair one (it pays out the
   whole dollar). An unequal state is a coordination failure, not a waste.
3. **Reading's role flips.** In the PD, reading is what makes cooperation safe. Here reading is what makes exploitation
   safe. A constant ⅔ risks disagreement against a fair partner; a reader can demand ⅔ only from those who would settle
   for ⅓ and stay fair with everyone else.

The third slot is what majority division adds. An unequal pair is left only when the excluded slot offers the
underpaid member ½ (a neutral drift step), and the underpaid member then switches (selected, +⅙). Exclusion pays 0, so
the excluded slot is the only outside option in the game.

**The prudent Trojan bully** (RS's name; `exploiter-fair` in queue 70). Slot i, keyed on partner j, with k the third slot:
*if j names me demanding ⅓, name j demanding ⅔; otherwise name k demanding ½.* It is point 3 in program form, and the
PD's PrudentBot transposed: it takes the surplus from whoever accepts exploitation and is fair to whoever insists.
- **Mass and effect.** Its seed mass is 3.7·10⁻⁵ per slot (two per slot, one per choice of j). It lowers the unequal
  basin's boundary u\* from the constants' 0.69 to 0.55 (L) and 0.425 (M). M's natural start sits at 0.429, so M ends
  unequal (V\* 0.10).
- **Where the analogy holds.** On fair islands it waits neutrally where its fallback is the fair pair. It is selected
  (+⅙) as soon as a submitter appears in slot j.
- **Where the analogy breaks, twice:**
  - *It is prudent toward k, not toward j.* Offered ½ by j, it walks off to k and gets 0, so fair-splitters in slot j
    purge it. PrudentBot never breaks a cooperative pairing. The strictly prudent variant ("otherwise name j at ½") is
    in queue 70's broader `exploiter` family (any fallback), whose removal raised u\* to 0.75 / 0.76; its own effect was
    not measured separately.
  - *Its prey survives.* PrudentBot's victim, ALLC, earns less than its neighbours and is selected out, so the
    prudence premium is transient: it cleans the sea and leaves an efficient state. The bully's victim earns ⅓, more
    than the 0 that exclusion pays, so it keeps its slot. The exploitation is the island's permanent outcome, and each
    outcome ratchets (unequal islands deplete the ½-offerers, fair ones the ⅓-demanders).

  So the prudence premium that h02 counts as a good reason in the PD is, in this game, what fails the stable-set target.

**Results by object:**
- **Chain.** It selects rotating, mostly unfair pairs; source reading adds nothing.
- **Lottery.** Dominated outcomes hold most islands without migration; migration picks one element.
  - Contracts: a veto on exits from members puts every island in V\*, but it works by churn.
  - Flexible readers: churn without contracts.
  - Myopic encounter contracts: a rotating walk.
- **Islands → ∞.**
  - The readers arm and arm T meet the target as a lottery across worlds: the symmetric state is a knife-edge, and
    across worlds the pair is uniform (44 / 54 / 57).
  - Arm T shows no unequal crossing up to an unequal share of 0.95. The length-prior DSL arms have the Trojan-bully
    basin.
  - Every run is tail-free so far; the annealed tail is queue 71.

### The union / social organization game (boss and workers, three roles)

- **Chain.** It puts π at zero wage; a strike quorum is FairBot's handshake on strikes.
  - With both sides' enforcement ex-post rational, the smallest positive wage is selected (0.75 under the length prior).
  - A replacement pool drives the wage to zero.
  - A strike pact's wage check is fakeable (the polarity dilemma).
- **Lottery, DSL.** Mostly zero wage (0.825 of islands): the abundant striker is wage-blind, and fair bosses die by
  demography.
  - Concessions ("pay fair to those who would strike") work as a mechanism but have no prior mass under the length
    prior.
  - Probes are vacuously true at world 0, which creates wage fakers.
- **Realizable language.** Under a library prior a fifth of boss programs are concessions. The lottery reaches the fair
  wage on every run and holds it on half the islands; a matched expanded-syntax prior gives 0/40.
  - Fully realizable, the fair wage is a fuel threshold (10⁶ – 3·10⁶ steps) under free certificates.
  - Under endogenous production it is a seeding threshold.
- **Genes.** The union/boss asymmetry is structural (two slots against one), not a credibility property.

### Rock–paper–scissors

- **Chain.** A tournament: the coin holds exactly its prior mass. Unexploitable individual mixing is approached only
  near N ≈ 10⁷.
- **Lottery, non-play free.** Readers whose self-play forfeits hold it.
- **Lottery, non-play priced** (the default charge A_f at 0.1, h08). Forfeits vanish and the free coin carries
  individual mixing on 0.85–0.93 of the lottery. Exact reading adds nothing.
- **Realizable private tape.** A sound coin. A timed-out read returns a default, so at the calibrated price simulators
  beat the coin; this is the RS's lever (DEFERRED 16).
- **What it decided.** RPS is the game that discriminates between compute rules (h08).

### The inspection game

- **Lottery.** Reading pays in proportion to what the reader sees: the modal island is the efficient outcome held by a
  responsive inspector. Commitment appears only when the inspectee alone reads.
- **Chain.** It loses the efficient state:
  - to the inspector's shadow at N ≤ 10³;
  - beyond that, to light cheaters below the inspection threshold and to bounded-read exploiters (π(E) 0.047 at
    N = 10⁵).

  Zero-tolerance and sampling inspectors help only at one depth cap (D = 12).

### Basic Endgame (poker; Ferguson & Ferguson)

The mixed equilibrium is not recovered in any arm: value to I −0.15, bluff 0.15 against 0.25, call 0.39 against 0.5.
The exact posterior reader gains against off-equilibrium populations; the coin stays unexploitable.

### Auctions

- **Static notion.** Coalition-proofness with the seller as a player gives the core, and the deployed surcharge rule
  stops exactly the coalitions that recontract with the seller.
- **Ecology.**
  - Police are a neutral shadow, and the surcharge's shading costs efficiency (0.48).
  - The first-price lottery erodes about 4 ticks below the core price, because the loser's honest threat is selected
    out early.
  - Certified threats hold the price against constant bidders (0.62–0.70), but followers that read and accommodate
    them leave them untested and frozen (core 0.08).
- **Target** (h12). Core outcomes with bidder-optimal selection. A frozen, untested threat below the core price counts
  as a failure of the dynamics.

### Cooperative games (leader-value core sweep)

A static existence sweep, not an ecology run. The leader-value core exists for owned endowments and aligned complements.
It fails by timing on unowned surplus, by coalition size under mixed-sign externalities, and by incompatible claims
with no timing; without transfers it is usually empty in substitutes games.
