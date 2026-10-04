# Rejected Proposals

Bookkeeping. Each entry: what was proposed, why it was dropped, and what replaced it. Purpose is to flag re-proposals, not to be read for the operating hypothesis — that's THEORY.md.

---

## Solution concepts

**Response-function equilibrium** (coalitions submit $\rho_S : A_{N\setminus S}\to A_S$, consistency across nested coalitions, grand coalition's response to nothing is the outcome). Consistency alone supported any profile; adding a deviation clause gave either collapse to Nash (if subcoalition responses had to be optimal) or a folk theorem down to the *pure* maximin (since responses see realized actions, mixing gives no protection). Now understood as the strongly extensional arm, whose structural leak is that it cannot distinguish reciprocators from unconditional cooperators. Replaced by the attractor chain.

**Static credibility clauses** — "punishment must weakly Pareto-improve the punisher over passivity," "no deviation may profit by baiting," etc. Every ordinal version either left the folk theorem intact (renegotiation-proofness prunes threats without weakening deterrence) or collapsed to Nash (full best-reply credibility) or emptied the set (Chicken under mutual-Stackelberg). The one that worked — passivity baseline — became manipulable once deviations were to programs rather than actions (the deviator can make passivity look bad). The population supplies the criterion instead: non-credible threats are outcompeted, not forbidden.

**Deadweight-loss minimization as the selector.** Selects a monoculture of self-recognizing CliqueBots, which is perfectly efficient because it never meets anyone it doesn't recognize. Efficiency rewards brittleness. Also silent on the Nash demand game (all splits tie at zero DWL) and non-covariant under separate affine rescaling. Efficiency is now an *evaluation*, never a selector.

**Non-exclusivity as the normative axiom** ("cooperate with everyone who cooperates with you"). Rules out PrudentBot, which defects on ALLC — and PrudentBot is the drift-plug the efficiency theorem needs. User is fine with self-interested players. Replaced by efficiency-as-evaluation plus $\lambda$-as-finding.

**Deterrence as the route to efficiency.** In general games $a^*$ is deterrable iff IR (the folk theorem); harsh punishers support inefficient outcomes even in separable games (grim-with-$\arg\min g$). The separable one-line proof was about matching-type $\rho$, not about all stable ecologies. Replaced by two selection engines: harsh punishers lose to mild ones; inefficient outcomes are invaded by unfakeable handshakes.

**$\lambda = 1$ as canonical.** Only the symmetric case. Asymmetric ratios are set by the endogenous threat point (fixed roles) or by `ROLE`-symmetrization (drawn roles → unweighted sum via veil of ignorance). The user's "I can unsubscribe, you can't" is fixed-role.

## Dynamics

**KMR best-reply with resistance trees.** Multi-mutant coalitions of short programs compete with single long mutants; the mutation *prior* drops out of the exponent unless put there by hand ($\varepsilon^{\beta|q|}$); needs Edmonds over $|S|^2$ edges. Retained as a comparison arm only.

**Fudenberg–Imhof small-mutation chain** (monomorphic almost always). True only for $\varepsilon\ll e^{-cN}$, which is unphysical; in Chicken and in any program game with frequency-dependent coexistence the population sits at polymorphic attractors. Replaced by the attractor chain over rest points, including polymorphic ones.

**$N\to\infty$ first.** Under KMR resistance analysis this made direct-best-reply hops free relative to $\Theta(N)$ escapes, so long programs arrived without paying for length. Under the attractor chain the concern dissolves — $\mu$ is a first-order rate at every $N$ — but drift-only transitions still vanish at $N=\infty$, so $\Sigma=\lim_N\pi_N$ is the definition and equality with the $N{=}\infty$ chain is open.

**Aggregating genuine cycles into a time-average.** If selection from a perturbed state doesn't converge to a rest point, the attractor chain's premise fails and the result is *indeterminate*. (Bistable switching between rest points is not a cycle and $\pi$ is well-defined there.)

**Black-magic fixed points for the strong arm** (an oracle resolving $a_1=\rho_1(\rho_2(a_1))$ rather than grounded iteration). Differs on non-convergent pairs (match-vs-swap: Brouwer gives ½, iteration oscillates → minimax) and needs a selection rule for non-unique fixed points (both-match: a continuum). That rule does hidden work. If wanted, a fourth arm with its rule stated; precedent Bastianello–Ismail.

## Complexity and priors

**$\beta$ as a knob.** No canonical value other than 1 bit: $\beta<1$ is improper in the Kolmogorov setting, $\beta>1$ is a stronger simplicity bias than the universal prior. $\beta=1$ is the *weakest* assumption that yields a proper prior.

**$n$ as a modeling parameter.** It's the index of an approximation sequence; canonical value $\infty$. A computational and proof device only.

**Node-count prior $2^{-|p|_{\text{nodes}}}$.** Improper: the grammar grows ~5.66×/node, so mass per level diverges. Always use bits.

**Levin complexity $Kt = |p| + \log t$ as the mutation cost.** Canonical for *search* (the log is forced by Levin's time-sharing allocation), not for evolution: length is paid once at mutation, runtime is paid every match, and nothing combines them additively. Also, runtime is opponent-dependent; self-play runtime is pathological (diverges for `THEM(ME)`, instant for `↑D`) and CliqueBot-shaped (short-circuit on self-recognition, slow otherwise). Length in $\mu$, runtime in fitness, separately.

**$\beta\to\infty$ (length lexicographically first) for canonicality.** Not needed; $\beta=1$ bit is canonical. $\beta\to\infty$ is a *different* canonical object — "the simplest stable ecology" — with a strong preference the user didn't want.

**Eventual constancy / "ecologies have a maximum length $\bar n$."** False: behaviorally equivalent long programs persist neutrally with positive mass; support of $\pi$ is infinite. Correct statement is convergence with a tail bound; what stabilizes is the mode.

**Certification via max resistance-tree edge $W<7\log 2$.** Wrong units (node-count prior) and wrong framework (KMR). Under the attractor chain, certification is "does any new program at $n+1$ tip any attractor."

## Runtime and grounding

**Finite $T$ as a modeling feature.** In Stag Hunt, minimax = Hare = the risk-dominant action, so the timeout rule pushed toward the KMR answer and confounded the test. Also reproduced Fortnow's pure-minimax folk theorem by making hanging a punishment. $T\to\infty$; divergent pairs → minimax.

**Forced-cooperate on timeout.** Makes slowness exploitable — the opponent captures it — and is game-specific (C/D are PD labels). Replaced by forced-minimax action, which generalizes.

**Shared budget.** Lets a program threaten to think forever. Per-program budgets.

**Docking both players on divergence "because attribution is impossible."** Attribution isn't impossible, it's ambiguous — step-count, call-order, and a unilateral divergence probe are all non-arbitrary. Made a sweep parameter; moot under $T\to\infty$ with the analytic solve.

**ε-grounding as the passivity baseline.** Not needed: the on-path action $a^*_V$ is already designated by the equilibrium object. (ε-grounding *is* needed for extensionality — full extensionality is inconsistent by Cantor/Rice; dropping totality is the escape and grounding is that drop — and for termination.)

## Language

**Shared `X` for correlation.** Breaks grounding (one coin for the whole recursion: terminates w.p. ½, not 1) and can't reach antisymmetric outcomes (both players compute symmetric functions of the same bit). Replaced by `ROLE`, a per-match antisymmetric tag.

**Biased-coin library `X_θ`.** Independent duplicates are behaviorally identical and only inflate enumeration; biases would let programs choose their own grounding rate, which is interesting but eats headroom (~30%/atom/level). Deferred.

**Behavioral `eq`** (bisimulation-defined). Semantics become indexed by the family; strengthens cliques by making them mutation-robust; `not` breaks partition-refinement monotonicity. Behavioral equivalence is an analysis tool applied after solving.

**Eager evaluation / "X evals first."** Diverges: `or(X, THEM(ME))` always evaluates `THEM(ME)`. Short-circuit left-to-right is the grounding; `and`/`or` become non-commutative.

**Barring lifts inside `eq` to shrink enumeration.** Buys ~23% of pairs at $n=7$; a level needs ~82%. Trim nothing.

**IESDS to prune the program space.** In any source-observing space closed under discrimination, no program is dominated: $q_p$ = "cooperate iff opponent is $p$" makes $p$ strictly better than any $p'$. Dominance is frequency-independent; discrimination is inherently frequency-dependent. Wrong tool.

**Strong extensionality as a parable rather than an arm.** Kept as an arm: minimal hypothesis for deterrence, empirical argument for weak being canonical, and exhaustively provable.

## Methodology

**Preregistering the definition of "main ecology."** Preregister *verdicts on test games*, not definitions — that's the normative component stated extensionally, and it's the only falsifiable form. Fit the definition freely on train games (PD, Stag Hunt).

**Hand-picking the strategy family.** The leakage channel that preregistration doesn't cover. Fix the family by closure conditions on generators (a size bound in a DSL), not enumeration.

**ROLE in PD.** Inert (no correlated outcome beats $(C,C)$) and ~3.75× cost. Add for asymmetric games and Chicken only.

**$\kappa$ (override strength) as a sweep dimension.** A smoothing detail; run $\kappa\in\{0,1\}$ as a robustness check at one $T$, not as a grid axis. Moot under $T\to\infty$.

## Added 2026-09-18 to 2026-09-23 (after the ledger stopped being updated in-repo)

**Unfakeable handshake as the efficiency engine (Engine 2).** False as stated. Fakeability is not the binding constraint: `THEM(^D)` exits a reciprocator world at 1/40 the rate ALLC does, and fakers sit at μ-weight in every setting tried (chain, ABM, lattice). The binding constraint is the unconditional shadow. Do not re-propose faker-resistance as the fix.

**Fakers as the spatial/island spoiler.** Refuted on the lattice. The spoiler is the ALLC-subsidized D front (a D with two ALLC and two `THEM(^C)` neighbours earns 0 against the bordering reciprocator's −0.25). Carry this into the island-model predictions.

**Conjecture B in its original form** (supported outcomes Pareto efficient, independent of prior and structure). Refuted under mutation in PD and exchange (1–2% cooperation), in fixed-role ultimatum (SPE mode), and on the lattice at 32²–128². Surviving statement is B′ (efficient among outcomes the language can stably express, with `ROLE`), itself unproven for dilemmas.

**`ROLE` as rescuing dilemmas.** It resolves coordination (Chicken, BoS, Nash demand) and nothing else; $(C,C)$ is already symmetric. `ROLE` is first-class, but as a modeling commitment (environment supplies a public correlating signal), not a game primitive.

**Nash bargaining solution / Young's result in fixed-role ultimatum.** Refuted: mode is subgame-perfect `(L|L)` 0.39, NBS 0.19. Mechanism is the shadow in bargaining form: `(THEM(ME)|H) → (H|H)` by neutral drift → `(H|L)` neutral → `(L|L)`.

**Commitment power via source observation (Tennenholtz-style) surviving selection.** Refuted in the ε→0 chain and at finite εN: a reader is neutral to the constant with the same on-path behaviour whenever the read population is monomorphic.

**Standing variance (finite εN) as the rescue.** Tested: `THEM(^C)` peaks at 1.6% at εN ≈ 1 and falls to μ-weight at εN = 10. Closed.

**Linear-clamped fitness $f = 1 + w\cdot$payoff.** Clamping at 10⁻⁶ voided all $w=1$ dilemma cells and manufactured the "29% cooperation at N = 1000." Use $f=\exp(w\cdot\text{payoff})$.

**"Cooperative share" (mean payoff / efficient) as the dilemma statistic.** In this PD $T+S=-1>2P=-2$, so exploited pairs beat mutual defection and the statistic counts mutation load as efficiency. Use $P(C,C)$.

**"$M_{\text{exit}}\propto N$, so the lattice is efficient in $\lim_N$" (Claude, 2026-09-20).** Falsified: pre-collapse ALLC density falls with side (0.13 → 0.06); collapse nucleates locally, so entry and exit are both per-area and the duty cycle is N-independent for `THEM(^C)`. Open only for the FairBot regime (per-mutant rates pending).

**Reading the 128² lattice number as π.** Seed spread 0.25–0.96 over a window shorter than mixing time; it is a window average over basins, not the ε→0 object. Use per-mutant rates (ρ_enter, M_exit) for thread-1 claims.

**Uniform prior as rescue.** Raises cooperation only 6×; class size (≈40×) dominates. Mutation acts on syntax; the prior isn't a free knob.

**FairBot pruning: "grounding noise makes roaming D neutral, so lone D prune ALLC and keep enforcement exercised" (Claude, 2026-09-21).** Falsified by the per-mutant rates (RESULTS.md, "Per-mutant rates"): a lone D in a FairBot sea lives 5 generations, not 10× a lone D in `THEM(^C)` (2–2.6), and ALLC lifetimes in the two seas are indistinguishable (medians ≈ 1 generation; means dominated by rare long lineages and flipping sign between sides). FairBot's advantage on the lattice is not pruning; it is that its D front is neutral (D earns 0 = FairBot's self-payoff) so a collapse cannot be subsidized — but it is unreachable from all-D by single-copy nucleation (ρ_enter ≈ 0.005, μ ≈ 4·10⁻⁵).

**"Pair nucleation at ρ ≈ ¼" as the lattice entry rate.** The measured ρ_enter(`THEM(^C)`) is 0.11 at both 32² and 64². The ¼ was the win probability of one death-birth event, not the probability that a lineage reaches half the torus. Use the measured per-mutant rates.

## Added 2026-09-23: island model (RESULTS.md, "Island model"; predictions/2026-09-23-islands.md)

**"Fakers as the spatial/island spoiler" — re-opened and reversed for the island model.** The entry above
stands for the chain and the lattice, where fakers arrive at μ-weight. It does not carry over when migration
replaces mutation. Arrivals are then set by what neighbouring islands hold, not by class size under μ, and
`THEM(^C)`'s 15 advantageous invaders are all fakers (ρ up to 0.26). Of 2,358 island exits out of
`THEM(^C)`, 2,338 went to strict or weak fakers, 18 to D and 0 to the shadow.

**Subsidized D fronts as the island spoiler (THEORY §9.5, CLAUDE.md queue).** Refuted at ε = 0. ALLC is
eaten in the first within-island scramble: extinct in 320 of 320 PD runs, at a median of generation 40. No
`THEM(^C)` island ever passed to a shadow.

**B′ on islands at ε = 0** ("every persistent island-state is Pareto efficient among outcomes the language
can stably express").
- *PD:* falsified in all 16 cells. Every run absorbs, and 261 of 320 absorb into mutual defection or into
  exploitation-probe states such as `THEM(^ROLE)` and `THEM(^X)`.
- *Chicken with `ROLE`:* falsified narrowly. Self-referential mutual-Swerve islands, at payoff 0, persist
  beside the `ROLE` conventions, and one run froze globally at payoff 0.

**The migration game (the equilibrium set of ρ − ρᵀ over monomorphic island-states) as the island model's
ε-free object (Claude, 2026-09-23).** It mispredicted all three games:
- *PD:* its equilibrium set is all mutual defection, yet 17.5% of runs absorb into all-`THEM(^C)` and 52%
  into exploitation-probe states outside the set. With 64 islands, global extinctions come within about 10³
  generations, and at ε = 0 each is permanent, so the time average never forms.
- *Chicken without `ROLE`:* it predicted mutual Swerve, but the islands hold a Straight minority among
  self-referential best-responders at the mixed equilibrium, a polymorphism the monomorphic game cannot
  represent.
- *Downstream verdicts that failed with it:* "PD P(C,C) < 0.2 in every cell" (observed 0.06–0.43) and
  "`THEM(^C)`-extinct runs freeze into on-path defection" (40 of 64 froze into exploitation probes instead).

**Conjecture A verdicts (Claude, 2026-09-23).** I predicted A would hold at the outcome level in the PD
and fail in Chicken with `ROLE`. The reverse happened:
- *PD:* placement matters. Clustered seeding absorbs cooperatively in 6 of 80 runs against 50 of 240
  shuffled (p = 0.006). Composition does not: the hostile seeding, with every spare slot D, gives 16 of 80.
- *Chicken with `ROLE`:* the seedings agree within 0.07 in payoff.
- *Also failed:* "the hostile seeding raises the D-dominated share by more than 0.2".

## Added 2026-09-28: lim_N of the chain (RESULTS.md, "lim_N of the chain with `ROLE`")

**"The PD limit is answered at N = 1,000: 1.5–2.4% cooperation" (THEORY §9.1).** N = 1,000 is the peak of a
rise-and-fall. π(all-`THEM(^C)`) → 0 like N^(−1/2), from 0.013 at N = 1,000 to 0.0044 at N = 30,000 at w = 0.3.

**The unconditional shadow as the lim_N obstruction.** The ALLC-drift exit is μ(C)/N and vanishes. The
N-independent exit is the faker: `THEM(^D)`, `THEM(^X)` and `THEM(^ROLE)` strictly invade `THEM(^C)`.
Faker exits are 0.92–0.99 of exits at N = 30,000. The shadow remains the dominant exit below N ≈ 300–3,000,
depending on w.

## Added 2026-09-28: cool check (RESULTS.md, "Cool check")

**"The payoff spread among programs on an island shrinks to zero as migration → 0, and tracks migration load"
(conversation, 2026-09-28; my predictions 1 and 3).** Not at fixed N. At N = 400 the spread is 0.142 over a
100-fold range of mN, with no load. The spread is drift around a cool rest point and scales like N^(−1/2):
0.267 at N = 100 against 0.142 at N = 400 in the same state. Migration changes which state the islands hold,
not how cool they are. The surviving statement is the time-averaged one: island compositions sit on cool rest
points, and the instantaneous spread vanishes as N → ∞.

## Added 2026-09-30: regret witnesses (RESULTS.md, "Regret witnesses")

**"The islands' inefficient persistent states are ε = 0 artifacts, held only because their invaders went
extinct" (my predictions 5 and 6).** Wrong for Chicken. The self-referential mutual-Swerve states (`THEM(ME)`
family) and the three-class no-`ROLE` state at −14/41 are exact no-regret states, meaning symmetric Nash
equilibria of the program game. They persist because nothing strictly invades them. The artifact reading
holds only for the PD states with positive regret: all-`THEM(^C)` and the exploitation probes.

**"A frozen PD defection state has positive regret iff its share of sucker-cooperating defectors exceeds 1/3"
(prediction 4).** Only the "only if" direction survives. Other witnesses give positive regret at share 0.

## Added 2026-09-30: island-level selection (RESULTS.md, "Island-level selection on emigration")

**"Payoff-weighted emigration at w_g = 3 gives P(C,C) ≥ 0.5, and the exit mix flips to the shadow by about
20 : 1" (Claude, 2026-09-30).** At w_g = 3 the result is 0.233 and faker exits still dominate. The rescue
needs w_g ≈ 10, a between-island intensity about 30× the within-island one. The flip to shadow exits is 3 : 1.
My rate estimates left out the faker states `THEM(^X)` and `THEM(^ROLE)`, which are exported by migration
at intermediate w_g.

**"Plain islands with mutation stay below 0.1 P(C,C)."** They reach 0.13.

## Added 2026-09-30: multilevel scaling (RESULTS.md, "Multilevel threshold vs island size and count")

**"The multilevel threshold is flat in island count" (Claude).** It is flat from 64 to 256 islands, 4.8 at
both, but rises to 10.5 at 16 islands.

**"2·10⁵ generations mixes every cell at N ≤ 100" (Claude).** Seven cells differ by more than 0.1 between
halves. Later scaling runs need longer horizons or more replicates.

**"P(C,C) is monotone in w_g" (implicit in the previous section's design).** There is an interior optimum
at N = 50 and at I = 256.

## Added 2026-09-30: ε = 0 islands vs island count (RESULTS.md, "ε = 0 islands vs island count")

**Seeding randomness as a substitute for mutation** (conversation, 2026-09-30). At ε = 0 the absorption
lottery concentrates as the island count grows: 100% mutual defection at 1,024 islands, and no cooperative
end state at 256. The canonical ε = 0 answer in the PD is inefficient. Mutation stays in the object.

**"The ε = 0 lottery shifts monotonically with I" and "freeze time grows with I" (Claude).** Both fail at
small I, because iid seeding misses programs at I = 16. Freeze time is flat from I = 64 upward at mN = 0.1.

## Added 2026-09-30: modal arm (RESULTS.md, "Modal (Löbian) arm")

**"Black-magic fixed points" (above), re-opened as the modal arm.** New justification: self-reference
guarded by provability has a unique fixed point (de Jongh–Sambin), so no selection rule does hidden work.
The arm is an instrument; it is not adopted into the theory.

**"A free provability box is an upper bound" (Claude).** It is not. The arm adds a capability and also
removes X, `ROLE` and unboxed simulation. It is a distinct idealization, raised by the astra review.

**My modal-arm magnitude predictions (Claude).**
- *Cooperation magnitudes:* I predicted P(C,C) 0.04–0.45, counting FairBot's entry alone. Three or four
  unfakeable provers enter at equal μ, and P(C,C) was 0.19–0.73.
- *PrudentBot:* I predicted π(PrudentBot) < 0.01; it reached 0.0127.
- *The "no strict exits" falsifier:* it cannot fire, because soundness guarantees it.

## Added 2026-10-01: modal follow-ups (RESULTS.md, "E2 ratchet" and "E3 finite-εN")

**"At finite ε the modal arm cycles through ALLC flooding, at P(C,C) 0.2–0.6" (Claude, pre-review draft).** Wrong.
A standing D fringe prunes ALLC, and the big island holds P(C,C) = 0.99. The fable review caught this before
the run.

**"Modal big island at 0.6–0.95, with excursions" (revised prediction).** It came out at 0.989, with no
collapses observed.

**"The shadow is pinned at x* = μ_C/(1 + μ_D) ≈ 0.32, independent of ε" (from the fable review).** It holds at
ε = 10⁻³ (0.26) and fails at 10⁻⁴ (0.13).

**"The support ratchets from FairBot to PrudentBot as N grows" (fable, 2026-09-30 review).** No. The ratio
plateaus near 0.04. What does shift is the fakeable `BOX(THEM(THEM))`, which leaves the family.

## Added 2026-10-01: priced arm (RESULTS.md, "Priced arm")

**"Priced provers recover cooperation if the population is spatially structured" (Claude, 2026-10-01).** Half
right. Structure makes entry N-independent even at c = 0.1, but the price ladder survives on the torus and
hypercube: ALLC invades FairBot at about its well-mixed rate. Under atom pricing, structure alone does not
rescue universal provers.

**"Lazy pricing reproduces the free arm" (Claude, prediction 6).** It does at n = 6. At n = 8 it overshoots, to
P(C,C) = 1, through cost-based incumbency: copies are free and newcomers pay. That is a parochial lock-in, not
the free arm's mechanism.

**The original clique verdicts 8–10 (Claude, draft).** Withdrawn before the run (fable): a clique world has no exit,
so π(cliques) = 1 is foreordained. Also: "four spellings fragment entry" was wrong for a monomorphic ε→0 chain,
and "hitting time ∝ 1/m with mass per spelling" failed (0.39–0.44, not 0.25).

**Literal ALLC as the dominant ladder exit (draft wording).** Correct, but restated over the class of cheaper
on-path-equivalent programs (astra), since several classes can carry the flux.

## Added 2026-10-01: certificates arm (RESULTS.md, "Certificates-only arm")

**"The C-seeded rule adds no loop-only exploitation" (Claude, draft verdict 8).** False before the run (fable). Loop-only fakers of compound residents exist, for example `not(IMP(THEM(^IMP(THEM(ME)))))` against `IMP(THEM(THEM))`, which cooperates with itself only through FairBot's C-seeded loop. The surviving statement covers FairBot alone: a mirror has no faker. Loop-only flux elsewhere is at most 1.1% of faker flux.

**"A stronger reader is more exploitable through its probe" (Claude, draft reading of verdict 7).** Wrong (fable). PA + Con(PA) gives exactly PA's numbers. The gap separates truth from provability, not strong logic from weak.

**"C-seeded cooperation is universal" (draft wording).** Replaced by pairwise coverage: 0.999, with 3 rival-reference probes (μ 2·10⁻⁶) in mutual D with FairBot. Universality is also tautological for a mirror (astra, fable).

**"Certificates suffice for lim_N efficiency" (stratified or D-seeded).** No. Both have only third-party probes, which are fakeable, so they reproduce the weak arm's faker limit (0.009 at N = 3·10⁴).

**Tags as a universal route.** Honest tags are efficient (P(C,C) = 1) but parochial: `EQ(ME)` cooperates with no other conditional cooperator, with or without the equality axioms. Tags are the clique arm again.

## Added 2026-10-01: price scaling paths (RESULTS.md, "Price scaling paths")

**Self-play as the fix for reciprocator entry (RS proposal).** Dropped. Letting programs play themselves gives a lone reciprocator (R − P)/N, which is Hamilton's rule with r = 1/N. That is one copy's worth of advantage. It changes ρ(FairBot | all-D) by 0.4–6.5% (static), and flips FairBot's sign against all-D only when c < 1/(2N). Entry still scales as N^(−1/2), and the barrier is unchanged to leading order.

**lim_N lim_c as the object (RS proposal).** Dropped as the object, kept as a limiting case. At fixed N the chain is continuous in c, so the iterated limit is the free arm and pricing has no bite. The informative object is the joint path c_N = c0·N^(−α), with boundary α = 1/2.

**"The α = 1/2 boundary is set by entry, not the ladder" (Claude, in chat before the brief).** Wrong. On this grid the ladder sets the decline (odds ∝ N^(α−1+β)). The barrier, c²N, also has its boundary at 1/2 but only binds at larger N or c0. The two 1/2's coincide for different reasons (fable).

**"A neutral lineage reaches about √N copies" (Claude, draft brief).** Wrong as a statement about typical lineages: the reach-k probability is 1/k (astra). √N is where accumulated selection in the fixation integral becomes order one.

**"Barrier below 0.3 along α = 0.25" and "strict exits ≥ 0.9 of FairBot's exits" as a falsifier (Claude, draft verdict 1).** The first is wrong: 2wc²N reaches 1.04 by N = 3·10⁵. The second holds by construction (fable). Both were replaced by per-path slope predictions, which held.

## Added 2026-10-01: certificate pricing (RESULTS.md, "Certificate pricing (decidability-based free set)")

**"Certificate pricing rewards legibility rather than sameness" (draft).** Too broad. On the GL chain "PA decides y's action toward me" is, to 3.6·10⁻³ of μ⊗μ, "y is monotone in its box atoms". It charges only for cooperation conditional on non-provability. The rival P* block is removed by the atom ladder acting on non-monotone programs, not by the free set: with a flat price (cert0flat) the block survives at its free-arm share.

**"cert0 ≈ 0.60 / 0.71, two-level static estimate" (draft).** Replaced before the run by fable's renewal identity. The two-level estimate gave the P* block 4% of cooperative mass against the chain's 13–15%, because it ignored moves among cooperative states. The identity missed by +0.013 at one cell, where the block partly sits in a polymorphic rung.

**Self-decidability as the criterion** (x is free iff its own action toward y is PA-decided). FairBot's defection on D is decided only in PA + Con(PA), so FairBot would pay against D and the entry barrier would return.

**The opponent's settle world as the criterion.** It is retrospective, and it prices the opponent's computation rather than what the reader must check.

**A small positive verification cost on certified checks.** It rebuilds the ladder: ALLC strictly invades FairBot at 1.4·10⁻⁴ (c = 10⁻²), independent of N (static).

**"Removing P\*'s copy subsidy suffices for one network" (implicit in the brief).** Partly. cert0diag keeps the subsidy for copies whose self-play PA decides, and it locks in PrudentBot instead. Copy subsidies lock in whichever ALLC-punishing family they reach.

## Added 2026-10-01: rival networks on graphs (RESULTS.md, "Rival networks under lazy pricing on graphs")

**"Cost incumbency locks in P\* under lazy pricing" (RESULTS, "Priced arm"), as a claim about the arm rather than about well-mixed populations.** On the torus, P*'s shadow `not(BOX(THEM(ME)))` invades P* at 0.8–2.1 × 2/N at c = 10⁻², and at an N-independent 0.005–0.0075 at c = 10⁻¹; the well-mixed rate is 4·10⁻²¹. In the ε→0 representative chain on the torus, P*-net holds ≤ 0.025. The lock-in survives only as hypercube degree grows (d = 10, c = 10⁻¹).

**"With equal priors the torus splits FB/P\* near even" (subagent, prediction 7).** Given FB-net's prior mass, P*-net takes 0.95–0.98. FB-net's torus dominance is its prior mass, not universality.

**"The torus ALLC load is 0.02–0.10 because pruning is local" (fable; adopted as verdict 19).** It is 0.20 at ε = 10⁻³ and 0.10 at 10⁻⁴.

**"P\* advances on a front iff bulk x > 4c/(3+4c)" (subagent, static; verdict 17).** On the torus without mutation, front ALLC is eaten and not refilled: the crossing is 0.05–0.15 at c = 10⁻² and above 0.4 at c = 10⁻¹. The mean-field threshold holds on the hypercube and at finite ε.

**"Rival-border welfare loss is about 1/side and below the D fringe" (verdicts 15, 23).** Borders roughen to 3–4/side. While both networks hold at least 10%, border mutual defection is 0.032–0.040 of edges on the 128² torus, 6× the D fringe.

**Narrow misses:**
- torus-16 rival nucleation (0.005 × 2/N);
- FB | P* at c = 10⁻¹ (5–9·10⁻⁵, ratio 0.29);
- the torus π(D) slope (−0.74);
- the torus-16 self-cooperating mass (0.66);
- the P*-shadow ratio at hypercube 10, c = 10⁻² (0.58).

## Added 2026-10-02: ergodic islands (RESULTS.md, "Ergodic islands")

**"Finite-ε weak islands are flat in I at fixed per-island rates" (subagent, verdict 10).** P(C,C) falls 0.15 → 0.14 → 0.040 from I = 16 to 256 at εN = 0.1, and R-dominant time falls 0.051 → 0.008. The global faker supply grows with I. This is the opposite of the ε→0 chain, where π_R rises.

**"≥ 0.3 of finite-ε P(C,C) comes from polymorphic, no-dominant islands" (fable, adopted).** The share is 0.12. The excess over reciprocity is probe self-play (0.049) and ALLC islands (0.036).

**"At mN = 10 islands merge, so entry is 1–3× the well-mixed ρ_IN" (subagent, verdicts 8 and 9).** Entry is 0.50 × ρ_N, which is 3.9× ρ_6400, and the patched π_R is 3.5× well-mixed.

**Verdict 12 reversed after review, "N = 25 ≤ N = 100 + 0.02" (fable: D immigrants take small R islands).** It failed at I = 256 (0.076 against 0.040). The pre-review direction would have held.

**"Lower ε at fixed m shifts R-island exits toward the faker" (subagent, pre-review).** Dropped before the run; the data go the other way (0.78 → 0.68 and 0.84 → 0.77).

**"Modal odds = I·o(N) ± 15%, with no faker exits" (subagent, pre-review).** Wrong before the run (fable). The n = 6 family has six fakeable provers, and the odds fall to 0.65 × I·o(N) by I = 1024.

**"Finite-ε islands sit above the ε→0 value (0.13 against 0.06)" (draft).** This compared different statistics. R-dominant island-time is 0.029, below π_R = 0.062.

**Minor:** weak + other exits < 0.01 everywhere (fails at small M); support and entry claims at every N (fail at N ≤ 16, I = 1).

## Added 2026-10-02: universality against drift-closure (RESULTS.md, "Universality against drift-closure")

**"Higher-order behavioural prudence beats the shadow's 1/N exit" (the §9.7 ladder as a fix).** Rejected by Corollary 1 and Proposition 2. Every class that cooperates with FairBot has a leak floor of about 0.9·μ(FB)/N, and no class is drift-closed at n ≤ 11. P12b's apparent 3,000× advantage was language coverage; with its siblings it is 4–7×.

**"A price that subsidizes no copies can give one network and a faster exit."** Rejected by Proposition 3: any successful price gives the incumbent a local advantage, which is a moat.

**"A fringe rescues universality"** (standing variance re-opened in ε→0 form). Partly rejected. The D fringe keeps exponent 1/2 and hands the network to P* at n ≥ 8. The μ fringe closes families but, at n ≥ 8, ends on the parochial P*: a fixed ordering that rewards exploiting the background.

**"Positive universality implies FairBot's leak floor" (draft).** Wrong (astra). P* has universality 0.10 through D-cooperating mates, not through FairBot. The floor applies only to classes that cooperate with FairBot itself.

**"The fringe is a behavioural moat" (draft).** Wrong (fable). It is an opponent-independent price that charges constants, so it is a fixed ordering, not incumbency.

**"If P\* fails to take over, the deep chain found routes the local estimate missed" (draft).** Backwards (fable). At depth 3 the local estimate covers all 471 classes, so a disagreement would point at the driver.

**"μ-fringe closure is a property of the language" (draft).** Wrong (fable). It is a crossover at N ≈ 1/(wδΔf), and it is not uniform in n.

## Added 2026-10-04: Conjecture 4 (RESULTS.md, "Conjecture 4: the sibling theorem")

**"The sibling's extra disjunct is a provable-cooperation test" (Fable, prediction 1).** The reverse: it is an undecidedness test, two negated boxes. Any test that is true when every box is true fires at world 0, and against prudent readers it makes the sibling cooperate with D. Membership in the mutual-cooperation graph comes from mimicry, not from a cooperation test.

**"The shell contribution to FairBot's leak decays geometrically, ratio below 0.7" (Fable, prediction 3).** Under the length prior each shell has mass 1/(2s²) and a constant 0.42 of each shell leaks, so the ratios are 0.83–0.86, a 1/s² tail.

**A uniform leak/μ bound as an open question.** Trivial under the length prior (≤ 27π²). The question with content is the limit value, about 89–90.

**Conjecture 4 as a statement about source-reading programs in general.** False with syntactic equality: CliqueBot is drift-closed. The theorem is about extensional readers.
