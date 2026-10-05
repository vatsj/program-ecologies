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

## Added 2026-10-04: almost all seeds (RESULTS.md, "Almost all seeds?")

**Reversal note on "Seeding randomness as a substitute for mutation" (2026-09-30).** Partly reversed. Its evidence (L6R, uniform-over-programs seeding, I ≫ N at N = 100) stands but does not carry to iid seeding from μ. Under μ-seeding the ε = 0 lottery rises with I in every arm: modal to 1.00, W0 to 0.55, L6R to 0.15. For unfakeable languages, seeding randomness does substitute for mutation; for fakeable ones the lottery is a faker-extinction race and is not monotone toward defection. Do not cite the old entry as "ε = 0 is canonically inefficient".

**"Modal efficient fraction ≥ 0.5 at N = 400, I = 4" (Fable, prediction 4).** 0.45 [0.26, 0.66]. The RE addendum's 0.5–0.8 at (6,400, 4) was also too low: it was 1.00 [0.91, 1.00]. The per-island chance does scale like √N as the addendum said; the survival-through-scramble factor was underestimated.

**"The weak efficient fraction falls along I ≫ N and stays ≤ 0.15" (Fable, prediction 6; falsifier fired).** W0 rises 0.03 → 0.55 and L6R 0 → 0.15. Without mutation the faker is a finite stock, neutral on D islands, and `THEM(^C)` enters D islands at FairBot's rate.

**"Weak ≤ 0.05 at N = 6,400" and "W0 falls on the diagonal" (Fable, predictions 6, 7).** 0.25 (W0), 0.10 (L6R); diagonal 0.15 → 0.20.

**"The replicator from μ predicts the ε = 0 island outcome" (implicit in the N ≫ I reasoning).** Holds for the modal arm only. The replicator stays a diagnostic (sol).

**"The thin-margin prior is uniform-over-programs at n ≥ 8" (Fable).** It is tempered-2: squaring the prior starves the provers.

**"No cooperative island is lost after ALLC dies" (subagent, S3).** 69 were lost, all fakeable probe-reading classes, to `BOX(THEM(^D))`-type fakers.

**Integrator endpoints as persistence certificates.** The replicator's pruning at 10⁻⁹ gave endpoints that failed the persistence check at modal n = 8, 9 and in every weak arm. Persistence must be checked on closed endpoints or without pruning.

## Added 2026-10-04: the closed club (RESULTS.md, "The closed club")

**"Semantic membership is a selection-free route to closure that is not a clique" (Fable, the spec's re-opening justification).** Rejected. The club is a clique over a declared predicate: about 99% of its mass is `CLUB(THEM)`, the semantic CliqueBot; its exit rate e^(−wN/4), entry and hitting times match the m = 1 clique's within 5%; and its fixed point is chosen, not derived.

**"Black-magic fixed points", re-opened by the club spec: re-closed for membership-level fixed points.** New evidence: membership of every guarded program is self-fulfilling, so every subset of the full-set limit is a fixed point (512 at n = 8); F is not monotone at n ≥ 8, so even "greatest" needs a search; and the choice decides which member holds π (K_max gives `and(CLUB(THEM),not(BOX1(THEM(THEM))))`, the smaller K′ gives `CLUB(THEM)`). The imposed fixed point does hidden work twice. Löb-guarded self-reference remains the only selection-free route, as in "Certificates-only arm".

**"The club K is drift-closed member by member" (Fable, prediction 2).** From n = 8, `CLUB(THEM)` is suckered by the member `and(CLUB(THEM),not(BOX(THEM(ME))))`. Only the set is closed; Corollary 1's leak returns inside it.

**"The empty set is the only fixed point besides the maximum" (Fable, 2b)** and **"iterating F from the full set gives the greatest fixed point" (spec design).** Wrong: 32 fixed points at n = 7; F is deflationary but not monotone, and the full-set start misses four BOXD-guarded members at n = 8, 9.

**"Every exit from the top club state is deleterious below e^(−0.2N)" (Fable, 3).** There is a neutral exit inside K at μ/N, and the exit out of K is e^(−0.075N), a symmetric coordination against FairBot.

**"Collateral at least 10× K's mass" (Fable, 5).** It is 2.0×.

**"The club reaches K faster than the clique" and "F is monotone in the positive-only grammar" (subagent, S7, S9).** Within ±5%; monotonicity fails in ~26% of nested pairs at n = 8 in both grammars.

## Added 2026-10-04: the legibility gate (RESULTS.md, "Bounded provers: a semantic legibility gate")

**Joint fixed-point semantics for the gate (spec design).** The synchronous iteration cycles with period 2 at every finite b. Replaced by the world-indexed gate, which settles, is sound, and selects no fixed point; choosing among fixed points of the non-monotone operator would have been an imposed fixed point (DEFERRED 5).

**"FairBot's threshold is b = 2, PrudentBot's and P\*'s are 4" (Fable, prediction 1; falsifier fired).** They are 1, 2 and 4: a stable self-proof has settle world 0, so FairBot's self-cost is 1. The proxy never charges the Löb step.

**"Tight budgets give the first drift-closed classes, at b = 4" and the "soft clique by proof length" hypothesis in this proxy (Fable, predictions 2, 4, 7; falsifiers fired).** No class is drift-closed at any b at n ≤ 8. Siblings are priced out (cost ratio ≥ 2), but every unsuckerable class leaks through a neighbour cheaper than itself (ALLC for FairBot, `BOX(THEM(THEM))` for PrudentBot, `not(BOX(THEM(ME)))` for P*), and a cost-monotone reader cannot cut those. Proxy-specific: real proof length is not measured.

**"The lottery weakens at b = 2 and is zero at b = 1" (Fable, prediction 6).** Paired differences at b = 1–3 are within ±0.07; the gate does not fragment the core because the provers' mutual costs are 1.

**Subagent S2 (no cycle) and S3's second clause (FairBot's sibling legible at b ≥ 8; it costs 15).**

**The atom-count control as specified.** Trivial at n ≤ 8 because k ≤ 2.

## Added 2026-10-05: seeds cutoff sensitivity (RESULTS.md, "Almost all seeds: cutoff sensitivity in n")

**"The ε = 0 per-island chance tracks the unfakeable core's prior" (Fable, prediction 1 and the μ_core·√N predictor).** Dropped. p(100, n) is 0.083 / 0.090 / 0.092 / 0.090 at n = 6–9 with no step at n = 7; μ_core misses by +57% to +89%. The core's drop is `BOX(THEM(THEM))` becoming fakeable through fakers of mass ~10⁻⁵, and at ε = 0 an unseeded faker does not matter. Replacement: the mass of D-entering self-cooperators, with p ∝ N^0.55.

**"Frozen efficient islands are held mostly by FairBot and `BOX1(THEM(ME))`, with the fakeable share falling in n" (Fable, prediction 4; falsifier fired).** Composition is μ × establishment; the four D-entering provers split the islands about evenly, and the fakeable share rises to 0.51 at n = 9.

**"Island-level ALLC extinction median 15–60" (Fable, prediction 5, range clause).** 13–14 at N = 100.

**"Run-level = 1 − (1 − p)^I at I = 4, mN = 1" as a quantitative law (Fable, prediction 2).** Fails at (400, 4) (0.42 vs 0.56); migration partly merges four islands during nucleation. Keep it for I ≥ 16.

**Design choice dropped: "core = unfakeable" as the class set the seed lottery selects on.** Unfakeability predicts only the absence of strict invasions, not establishment, composition or persistence at ε = 0.

**Subagent S3 and S4.**

## Added 2026-10-05: the seed lottery's tail (RESULTS.md, "Almost all seeds: the tail in n")

**Global probe-faker mass as the lottery's spoiler measure (Fable, prediction 2; subagent S1; falsifier fired).** μ_pf(12) = 0.064 and r = 2.5 against predicted ≤ 0.006 and ≤ 0.25. The union is dominated by the fakers of two near-universal suckers and counts FairBot as a faker. Dropped for resident-conditioned exposure (P(K_pf > 0 | A), μ-weighted exposure), as sol argued.

**"Shell fraction of D-entering self-cooperators is 0.03–0.06" (Fable, prediction 1 clause).** 0.061–0.091 at s = 6–12; the 1/s² form held.

**"Retained mass → 1" (spec wording).** The infinite length prior totals π²/12; limits are stated in inf units with raw(∞) ≤ raw(n) + ω(n).

**"Migration hurts at I = 4 by importing spoilers" / "an intermediate maximum in mN" (spec framing; sol's alternative).** 0 losses in 180 runs and a monotone decline: migration hurts only by merging islands during nucleation.

**The seed-membership label for local nucleation (design choice).** Uninformative when every island seeds about 9 establishers; nucleation is identified by timing against the no-migration window.

## Added 2026-10-05: spoiler-conditioned establishment (RESULTS.md, "Spoiler-conditioned establishment")

**"The faker's share falls after ALLC extinction while the target's rises" (Fable, prediction 4, log clause).** The faker is already extinct at ALLC extinction in 90–99% of surviving islands. Replaced by "the faker dies during the scramble".

**"Probe-fakers (neutral against D) are strongly harmful at single dose" (subagent S1; falsifier fired).** The relative reduction at k = 1 is −0.32 to 0.35 with intervals including 0; the 2×2 argument ignores that a probe-faker cooperates with ALLC and loses to D before ALLC is gone.

**Cell-level target-survival ratio as the spoiler discount.** Confounded by target identity across cells (0.33–0.56 raw vs ≈ 1 matched). Use cooperative fixation or survival matched on target.

**Single-copy forced design to resolve flatness in n at 0.15 (Fable, prediction 2).** Per-cell intervals are ±0.4–0.6 at k = 1; trends need k = 10 or more backgrounds.

**Spec treatment (c), "k copies of the target's own class", as the replacement control.** Changes target dosage; replaced by replacement with D (cD).

**Subagent S3 and S4 (neutral part).**

## Added 2026-10-05: the scramble lemma (RESULTS.md, "The scramble lemma and Claim A")

**"Fakers die in the scramble because they are strictly worse than D" (RESULTS "Spoiler-conditioned establishment", THEORY §3 as written on 2026-10-05).** Corrected. Probe-fakers are mean-neutral to first order (π̄ − π_q = x_A·x_q) and survive exactly as a fitness-pinned ghost does (ratio 1.02–1.05). The scramble kills by demography: a critical lineage over τ ≈ 13–19 generations survives with probability ≈ 1/(1 + τ). Selection contributes only for D-cooperating fakers (factor 2–7).

**"The first-moment bound q̄ ≤ exp(−integrated deficit) is within 10× of measured survival" (Fable, prediction 2; falsifier fired).** Vacuous for probe-fakers, 10–20× loose for D-cooperators: the first moment discards the demographic factor.

**"The combined per-island bound ρ[1 − ΣKq̄h] is positive" (Fable, prediction 3).** Non-positive in 16 of 18 cells: the union step loses 1/P(A) ≈ 7–20.

**The spec's example establisher-faker `and(BOX(THEM(THEM)),not(BOX(THEM(^C))))` (Fable, in chat and in the spec).** Wrong: it defects on itself; its self-play fixed point is ⊥. Working example: `BOX1(THEM(^not(BOX(THEM(ME)))))`.

**"Death–birth" as the kernel's update rule (spec).** It is birth–death (parent by fitness, victim uniform).

**"Almost all seeds" on all establishers.** Narrowed to the fakerless establishers (FairBot's pair): for fakeable establishers the spoiler term grows like N/log N unless the post-scramble harm falls.

## Added 2026-10-05: proof-carrying contracts (RESULTS.md, "Proof-carrying contracts v1")

**Truth-table contract semantics (spec, v1 as first implemented).** Paradoxical: a period-4 cycle with 16% of entries divergent. Contracts must carry provability semantics, as the Löb certificate arm does.

**"Contracts restore legibility at b = 2" (Fable, P1's premise).** The settle-cost gate is inert for b ≥ 1 (FairBot's self-cost is 1), so nothing was lost at b = 2. The legibility question is posed only at b = 0, where the supplement answered it.

**"Under swapping the universal contract wins on validity breadth" (Fable, P2).** Validity binds each contract to about one source (427 of 610 sources valid for exactly one), so swaps are no-ops or rejections and contract composition equals source composition. Breadth favours D and ALLC-like contracts and plays no measurable role.

**"Swapping spreads a contract from a 1% seed" (Fable, P3) and "a small seed spreads to every program that can carry it" (RS, in chat).** A μ-drawn 1% seed holds about one prover carrier at N = 6,400 and dies by drift at every σ, N and budget, including b = 0. Untested: a 1% seed of *prover* carriers.

**"Source-ALLC load 0.2–0.35, coinciding with contract load when f₀ = 1" (Fable, P4).** 0.155–0.283; the loads coincide when s = 1.

**"The neutral label concentrates less than the FairBot-contract" (Fable, P6; falsifier fired).** The label fixes at 1.00; copying alone concentrates more than contracts, which validity pins to sources.

**The all-D start (144 cells).** Not run, by the RE's decision after the gate proved inert at b = 2.

**The μ-drawn carrier seed as the design for testing spread (Fable, spec).** It conflates carrier rarity with prover rarity: 94% of a μ-seed is ALLC and D. A carrier seed drawn over provers is the right design for that question.

## Added 2026-10-05: three-player divide-the-dollar (RESULTS.md, "Three-player majority divide-the-dollar")

**"The bidding war is capped at the fair pair; unfair pairs below fair" (Fable, prediction 3; falsifier fired).** Unfair pairs hold 0.59–0.63 in every arm and N: each pair has two unfair orientations, and pivots only ratchet up because the excluded slot buys a member with 2/3 at its own cost of 1/3.

**"A net current around the three pair states" as a statistic (Fable, prediction 2).** It vanishes identically under relabeling symmetry. Replaced by currents between outcome types (fair → unfair → wasteful → fair) and moves by pivot role.

**"The constant grand coalition needs a three-step neutral path, so fair pairs ≥ 0.5" (Fable, prediction 8).** Its entry and exit both cost 1/3 (deleterious), so its share is N-independent at 0.003; fair pairs are 0.37.

**"Grand coalition entry is three neutral steps" (Fable, prediction 5).** It runs through a "join iff j joins" reader and a strict step, flat in N.

**"The weak arm has ≥ 2× the modal arm's disagreement" (Fable, prediction 6).** Identical: at n = 6 provability and simulation differ only on handshakes, which carry no mass.

**"The grand start decays into pairs within 10⁴ generations" (Fable, prediction 7).** It holds for 26k, 67k and > 10⁵ generations.

**"Unfakeability is the condition for coalition stability" (implicit in the spec's framing).** In k ≥ 3 games the binding exit is a partner's strict defection to a third party's offer, which reading the partner cannot police.

**Solver designs dropped:** sparse LU on the generator at N ≥ 10³ (assigned grand = 1.0); row-scaled linear GTH at N = 10⁴ (loses classes bridged by underflowing rates); an excursion-only ring without ring-to-ring edges (underestimates the grand coalition 3× at N = 100); MMD ordering (hours); a k-ary min/max DSL for the weak arm (the 9 actions have no natural order).

## Added 2026-10-05: compatibility (RESULTS.md, "Almost all seeds: compatibility among co-seeded establishers")

**"Anti-coordinators are rare (co-seeding < 0.02 at N = 400)" (Fable, prediction 4).** They carry 2–3% of μ; some pair is co-seeded on 89–93% of islands and a both-defect-on-D pair on 2.4–7.3%. They are harmless because they almost never outlive D together, not because they are rare.

**"The μ background changes pair outcomes in fewer than 20% of cases" (Fable, prediction 4).** TV 0.19–1.0: the background feeds ALLC to ALLC-exploiting establishers and lets D remove anti-coordinators. Pair-only competitions do not stand in for island outcomes.

**"Island co-seeding of an incompatible pair below 0.1 at N = 400" (Fable, first draft of prediction 2; withdrawn after sol's review).** 0.26 at n = 12, N = 400, rising to 0.99 at N = 6,400.

**Connected components as a compatibility measure (spec design).** One component at every n; no information.

**"Frozen cooperative islands below P(C,C) = 0.95" as a diagnostic.** Vacuous under pairwise-payoff-identity certification in the PD, which forces all-CC or all-DD.

## Added 2026-10-05: the union game (RESULTS.md, "The union game")

**"The chain alternates fair ↔ low wage with an N-independent fair share in [0.2, 0.6] and intermediate ≥ 0.2" (Fable, prediction 2; falsifier fired).** Fair is 0.002–0.005 and intermediate ≤ 0.022 under the length prior. The mechanism was wrong too: a second union is deleterious at s = 1/4, and at s = 0 refusal is neutral for every program, so the constant striker and the scab (0.48 mass each) dominate. The 0.31 fair share appears only under a uniform prior over named programs.

**"Without QUORUM the chain settles at the intermediate wage" (Fable, prediction 6; falsifier fired).** union′, with `BOX(OTHER = strike)` in place of QUORUM, is the same program at the same size, untagged. QUORUM is not a new capability: in GL, □low ∧ □(low → X) ≡ □low ∧ □X.

**"Fair share falls by ≥ 0.1 as c drops" (Fable, prediction 3).** Direction held, magnitude not; the c effect runs through strike-targeting discipline of strikers, not source targeting.

**"Boss-slot island selection lowers the fair share by ≥ 0.15" (Fable, prediction 4).** There was no fair share to lower; selection spreads cheap exploitation and the deterrent policy (sol's alternative), and the all-slot effect is larger.

**"First fair phase within 10⁴ generations in all seeds" (Fable, prediction 5).** 77,580 in one seed.

**Design choice dropped: QUORUM as the union's distinguishing atom.** Equivalent in GL to FairBot's strike handshake given □low; source targeting reads only a spelling.

**Design choice dropped: a wage check of the form "strike iff provably low".** Fakeable by bosses that pay fair only at the bottom world (72 classes, mass 0.006), an N-independent strict exit of 2.7·10⁻⁴ per event.

**Not run (declared):** the PA + Con(PA) worker language (1,462 classes).

## Added 2026-10-05: prover-carrier seed (RESULTS.md, "Prover-carrier seed at b = 0")

**"Carrier spread has a carrier–carrier encounter threshold f* ≈ 0.003–0.01" (Fable, prediction 1 mechanism).** After the scramble f* = 0: the carrier's advantage (≈ 0.01 per generation at every frequency) comes from a sucker fringe of non-carriers that trust contracts but cannot be read. The barrier is stochastic, survival through the first ~100 generations.

**"Swapping inert: acceptance < 10⁻⁴ per birth and σ effect < 0.05 in every cell" (Fable, prediction 2).** Acceptance reached 1.2·10⁻⁴; a cell-level σ effect of 0.30 arose by sampling noise (five seeds cannot resolve 0.05). Pooled, σ is inert in outcome but not in lineage: contracts cross lineages within a source class.

**"1 carrier per island on (100, 64) beats 16 per island on (100, 4); k = 0 < 0.1" (Fable, prediction 4).** 0.925 vs 0.95, unresolved; k = 0 on (100, 64) is 0.125 because of non-carrier `not(BOXD…)` cooperators.

**"Mutation stripping sets a finite-ε threshold" (subagent S1) and "no cross-lineage transfer" (subagent S5).** The fringe outweighs stripping and standing ALLC; acquirers' lineages sometimes win.

**The extinction stop applied in the b = ∞ control (subagent's bug).** Invalid where sources are readable; fixed and rerun.

**The asymmetric read rule as a test of "carrying is heritable legibility" (spec design).** Non-carriers read contracts while remaining unreadable; this one-sided rule powers the invasion. A symmetric gate is the needed control.

## Added 2026-10-05: the symmetric gate (RESULTS.md, "The symmetric gate")

**"Under a symmetric gate the carrier seed's establishment threshold moves to 0.03–0.1" (Fable, prediction 2).** It moved from about 0.013 to 0.017 at finite ε and from 0.009 to 0.016 in the ε = 0 twins (100-seed exploratory extension). Symmetric success at f₀ = 0.01 is 0.35 at 20 seeds and 0.26 at 100. The fringe was a secondary contributor to establishment, worth about 0.1–0.2, not the mechanism; the mechanism is the race through the scramble, and a per-generation advantage after it barely moves establishment.

**"The k = 1 lottery at (100, 64) falls to 0.3–0.7 without the fringe" (Fable, prediction 5; falsifier fired).** 39/40 under the symmetric rule. One near-neutral carrier per island suffices on 64 islands because spread is one-way. The subagent's S7 range (0.5–0.85) fails for the same reason.

**"After the scramble a symmetric carrier has only the linear carrier–carrier advantage" (Fable, prediction 1, range clause).** A transient legibility shield adds about +0.0023 per generation at ε = 0: illegible carriers are cooperated with by `not(BOXD…)` programs that defect on the legible D. It vanishes at the ε equilibrium.

**"The b = ∞ baseline is exact under the symmetric rule" (spec design 5).** A contract read (the box over the representative's free trace) is not a source read (the box over the carrier's actual trace); they coincide only among carriers. 172,517 table entries differ, μ×μ mass 0.0006, outcome difference +0.011 in P(C,C).

**Subagent S1** (changes confined to non-constant carriers): 1,352 entries against constant sources carrying a non-constant contract also change. **S2 confinement clause:** carrier → non-carrier entries change at b = ∞. **S4 paired clause at 20 seeds, S5 "below asymmetric" at N = 25,600, S6 twins 0.2–0.5 at f₀ = 0.01 (0.60).**

**Design choice: 20 paired seeds for a rule contrast on establishment.** Cannot resolve a 0.1 effect (sol's warning, confirmed). Use about 100 paired seeds.


## Added 2026-10-05: rival networks across islands (RESULTS.md, "Rival networks across islands, and the mN rule")

**"Separation between rival networks is long-lived under migration: hazard < 10⁻⁵ at mN ≤ 1, both present at the horizon in ≥ 0.8 of runs" (Fable, prediction 1; falsifier fired).** Mutual defection between two self-cooperators is a symmetric coordination game with a barrier of only about N·w/4, so one migrant fixes with probability 1.85·10⁻⁵ at N = 100 (not the 10⁻⁸ of D into FairBot that the intuition borrowed), and migrant load at mN = 1 multiplies the hazard by 10–20. Both networks survived the horizon in 0 of 40 runs in every mN ≥ 1 cell. The single-migrant intuition holds only at mN = 0.1. Lifetimes grow exponentially in N (≈ 1,000× from N = 100 to 200).

**"Majorities are decided by prior mass: FairBot's family holds ≥ 0.8 of islands" (Fable, prediction 2; falsifier fired narrowly).** A rival pre-seeded on one island wins the majority in 0.32 of runs. Colonization from the pre-seeded islands decides majorities; local nucleation rates correlate (Spearman 0.70) but do not determine the outcome.

**"Natural separation at the horizon ≈ 1 − (1 − p_B)^I and flat in mN" (Fable, prediction 3, those clauses).** The formula fits *ever* separated; separation at the horizon is that times survival, which is zero at mN = 1 within 10⁵ generations. The (100, 256) band 0.01–0.05 missed at n = 9 (0.003).

**Subagent S1** (minority hazard = mN·ρ_DD within ×3; off by 14–200× at mN ≥ 1), **S3** (losses dominated by nucleation; 415 of 485 came after generation 10³), **S4** (two clauses at N = 200).

**Design choices dropped:** the literal "three heaviest pairs" (a four-way tie replicating one rival; one pair per rival instead); island local-frozenness as the horizon "unresolved" criterion (counts transient migrants; holder rule instead); run-level efficient fraction as the mN-rule response at I ≥ 64 (at its ceiling; island-level local nucleation q instead); the arrival count mN·T_nuc as the scaling control (fails to collapse N by 4.6×; the replacement fraction m·T_nuc does).


## Added 2026-10-05: the demographic lemma (RESULTS.md, "The demographic lemma, the per-founder spoiler bound, and the establishment formula")

**"r_q ∈ [0.8, 1.6] in every cell, larger for ALLC-cooperating fakers" (Fable, prediction 2; falsifier fired narrowly).** D-cooperating fakers have the larger r (1.15–1.66, one cell at 2.01 [1.22, 2.74]); 5 of 27 cells fall outside the interval. There is no universal interval, as sol expected. Kept: r ≤ 1/P(A) (proved) and the measured r.

**"E[k_τ]/k₀ ≈ 0.75–0.95 from fitness curvature" (Fable, prediction 4; falsifier fired).** The mean-field curvature loss is only about 7% because x_A·x_D shrinks along the scramble, and the establisher family's own advantage w·x_D·x_E plus a survivor's own frequency push E[k_τ] to 1.26–1.55 at every N. Dropped: "provers are payoff-neutral during the scramble" as a basis for E[k_τ].

**"Saturation follows the independent-founder form" (Fable, prediction 5; falsifier fired).** 0.686 at N = 6,400 and 0.980 at 25,600 against 0.58 and 0.82; survivors pool after the scramble, and sol's erf form fits. Also dropped: the spec's concavity example (0.49 vs 0.65), which used independent copies; the exact pooled u₁₅ ≈ 0.58.

**The spec's Kendall expression 1/(e^{ρ(T)} + ∫ d e^{ρ}) (Fable).** Has d where Kendall has b; with b < d it over-claims. The correct equivalent is 1/(1 + ∫ d e^{ρ}).

**The binned evaluation of a stopping-time bound, Σ_i min{P(bin_i), cap_i} (subagent, and the scramble lemma's B1 before it).** Valid but sums one cap per bin and is vacuous when the statistic is spread (12–50× the measured survival); replaced by the single-level infimum inf_φ [k₀/φ + P(Φ_τ < φ)]. Addendum to RESULTS "The scramble lemma": B1's binned numbers were loose for this reason too.

**Subagent S2** (E[k_τ] decreasing in N toward 0.93; it stays ≈ 1.3, the family advantage is N-independent), **S4** (pooled r ∈ [0.9, 1.6] with the shared background explaining half of r − 1; r_env is 1.07 against r = 1.39), **S8** (Lemma D′ within 2× of founder survival; 2.1–7.9×), **S9** (h^rel for probe-reader pairs < 0.15 at N = 1,600; 0.40).


## Added 2026-10-05: incentive-compatible enforcement (RESULTS.md, "Incentive-compatible enforcement in the union game")

**"The workers' commitment carries the fair share; the boss's does not" (Fable, prediction 2; falsifier fired).** Making the boss's whack ex-post rational raises the uniform-prior fair share from 0.306 to 0.553 (+0.247 against a 0.15 threshold). The committed strike-targeting threat is non-credible (worth −c if called), is never executed on path, and still holds 0.53 of π, because it makes the militant's zero-wage entry deleterious: the ε→0 chain scores committed policies without testing them. The RR clause ("zero wage ≥ 0.8") also failed: RR gives the intermediate wage 0.668.

**"The prior decides the fair share" as a general statement (RESULTS "The union game", Reading; Fable).** Holds under committed play only. Under RR the full chain under the length prior gives the intermediate wage 0.75 with workers 40× better off; the constant striker is a free enforcer of the smallest positive wage once strikes are credible only where free.

**The union⁻ pact (`not(BOX(s = 1/2))` wage check with a BOX or BOX1 handshake) as a remedy for the polarity dilemma (Fable, first draft of the spec; withdrawn after sol's review and confirmed by Part A).** union⁻₀ never activates (every box is vacuously true at world 0), union⁻₁ activates only on a world-0 low wage and is faked by 72 classes (fair only while provably struck), and the BOX1 wage twins never activate.

**"Rational repression is free of the commitment cost" (Fable, first-draft rationale for prediction 3; withdrawn after review).** Rational repression still pays c when executed; its advantage is avoiding unprofitable executions, and with the pool it is worth 0.03 of fair share at most.

**Subagent S4** (CC + pool keeps fair ≥ 0.05; it is 0.031: with the pool the committed (0, strike) is a strict invader against any striker).

**Design choice dropped: the tie reading "boundary 1 − s = c → recommendation".** Needs a fourth whack policy for source targeting; the boundary is off-path in the reduced chain and was reported as whack/nowhack in Part C.


## Added 2026-10-05: proof length (RESULTS.md, "Proof length: an explicit GL calculus on the free arm, and a sound bounded calculus K")

**"The proxy's ordering survives: Spearman ≥ 0.7" (Fable, prediction 2).** Spearman is −0.22 / +0.05 at n = 6 and −0.34 / −0.07 over every n = 8 pair measured. The proxy charges settling worlds, which are large exactly where an atom is undecided or Con-dependent; proof length charges what is provable. Different quantities.

**"L(x → sibling) ≥ 1.5·L(x → x) for every member of P" (Fable, prediction 2).** Held for FairBot, `BOX1(THEM(ME))`, PrudentBot, P\*, P2 and the level-2 ladder (2.0–2.6); failed for the four probe-readers (1.14–1.33). No sibling was cheaper than self.

**"The cost of cooperation is linear in frozen syntax and Löb-light" (Fable, prediction 3).** Slope 0.49 per node, residual sd 0.58 of the mean, a negative quadratic term preferred by AIC, Spearman with size 0.08, Λ ≥ depth + 3 in 1,478 pairs. The cost comes from boxed obligations re-proved in every Löb branch (cut-free GLS shares no lemmas), not from node count.

**"Above max L over P the free numbers return within 0.05" (Fable, prediction 4, one clause).** K is +0.06 to +0.08 above the free arm at N = 10⁴: its incompleteness removes the Gödel-sentence fakers of `BOX1(THEM(THEM))`. Falsifier (> 0.1) not fired.

**"Under a price, ≥ 0.5 of π within 2 of the minimal cooperating budget" (Fable, prediction 5, pricing clause).** π(all-D) = 1.000 at c = 0.01 and 0.1: ALLC strictly invades every priced prover world, the price ladder. Sol's alternative, that pricing favours zero-budget players, held. The grid clauses held.

**Subagent S3** (`BOX1(THEM(ME))` self-cooperation costs 6; it costs 5), **S4** (siblings additive ≤ 6; +19 to +50), **S5** (proxy Spearman in [0.2, 0.7); −0.22), **S6** (PrudentBot Λ ∈ {3, 4}; 5), **S9** (Spearman(L_C, size) ≥ 0.5; 0.08), **S7** (thresholds 5/5/9; 3/4 and 4/7), **S8** (K chain within 0.05 of free; +0.084 at b = 6).

**Design choices dropped:** Knuth on the full sequent graph as the production method (4% of random n = 8 pairs exceed 2·10⁶ sequents; exact iterative deepening with oracle pruning and the normal form instead, cross-checked against Knuth where it fits); identity axioms on constants only (would charge a spurious GLR for every □A ⊢ □A and put FairBot at Λ = 2; boxed formulas are initial too); K with cut and a distribution rule (the spec's c₁; derivability within b then cannot be decided by a finite analytic search and a contextual bounded Löb rule is unsound; replaced by joint Löb with a self-witness, c₁ = 0, c₂ = 1, at the price of incompleteness against GL); the μ-weighted n = 8 sample alone (89% constant opponents; a uniform 5,000-pair sample was added).


## Added 2026-10-05: divide-the-dollar partitions (RESULTS.md, "Divide-the-dollar partitions")

**"One population without `ROLE`: 50–50 ≥ 0.7" (Fable, prediction 1, control (ii); falsifier fired at N = 10⁴).** All-S3 holds 0.999 at N = 10³ and 0.0004 at 10⁴: an accommodating shadow `flip(THEM(^S3))` enters at μ/N, S5 exploits it, and the S5–accommodator polymorphism (efficiency 0.41) absorbs π. The `role` clause collapses the same way at 3·10⁴. The stated mechanism, risk dominance, was also wrong at N ≥ 10³: direct S3 ↔ `ROLE` moves are negligible next to accommodator exits and re-entry from inefficient states.

**"Seed lottery with `ROLE` is a patchwork: 50–50 0.4–0.7, `ROLE` 0.1–0.4 at (100, 64), mN = 0.1" (Fable, prediction 2, band clauses).** 1.000 / 0. Each island receives ≈ 10⁴ migrants over the horizon and one S3 migrant takes a `ROLE` island with probability 4.7·10⁻³; a patchwork survives only at (400, 16).

**"Equal-share merges at N = 400 go to 50–50 with probability ≥ 0.9" (Fable, prediction 3, one clause; subagent S8 at ≥ 0.98).** 0.86 [0.78, 0.91], exact 0.87: the selection term is ≈ 5.6, so risk dominance sharpens only as √N.

**"π(1/3|2/3) ≥ π(1/2|1/2) per ordered state at N ≥ 10³" (Fable, prediction 4, one clause).** Failed at 10⁴ (0.0010 vs 0.0013), both residues next to the endpoints' 0.99.

**"Fixed-role lottery: 1/6–5/6 ≥ 50–50, 50–50 ≤ 0.2" (Fable, prediction 5; falsifier fired).** 50–50 holds 0.766 of islands at mN = 0.1 and 0.225 at m = 0. The lottery does not run on the ratchet: seeds are near-uniform over the constants, against which S3 is the best reply; endpoint islands occur only where an accommodator was seeded.

**Subagent S3** (norole 50–50 ≥ 0.9 at 10⁴; 0.0004), **S4** (no `role` growth 10³ → 10⁴; 0.69 → 0.81), **S5** (the scramble is fair; 50–50 0.225 at m = 0, drift-dominated, deterministic basins 0.92–0.99 overstate it), **S6** (escape < 10⁻⁵; 2.4·10⁻⁵ and 8·10⁻⁵), **S8** (as above).

**Design choices dropped:** n = 6 for `dollar5` (29 GB); island labels at 0.99 (migrant lineages trip them); counting every label flicker as an escape; the two-step adjacent-move table as a predictor of fixed-role π (implies ≈ 0.7 on the endpoints against the exact hitting's 0.99; kept as a static number); deterministic replicator basins as a proxy for the N = 100 scramble.
