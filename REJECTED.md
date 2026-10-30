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


## Added 2026-10-05: the island path (RESULTS.md, "A path in (N, I, mN)")

**"Propagules resolve rivals when k/N ≥ 0.15" (Fable, prediction 2; falsifier fired).** (400, 60) left both networks present in 0.82 of runs. k/N is not a scaling variable: the coordination barrier is ≈ N·w·(1/2 − k/N)², so fixed k/N < 1/2 loses exponentially in N (6·10⁻⁵ → 3·10⁻⁸ from N = 200 to 400). (200, 30) resolved only through stacking of near-simultaneous propagules (6× the single-propagule reference).

**"Natural separation grows with I at N = 200 and reaches ≥ 0.05 at (200, 256)" (Fable, prediction 3).** 0 of 100 at the horizon, 1 of 100 ever; every N = 200 natural rival sampled had a bridge and was absorbed. The colonization-before-rival clause failed at N = 100 (equal medians).

**"The bridge grows during conflict by ≥ 0.1 over the bridge-alone control" (Fable, prediction 4; falsifier fired).** The shares were equal (0.62). Design dropped: the bridge-alone control, which confounds conflict with prior abundance; the matched A, A, bridge control shows conflict mediation of +0.32. The majority band 0.3–0.6 also failed (0.65).

**"Rivals resolve only at N = 100" (Fable, prediction 1's headline; its clauses held).** Bridged rivals resolve at N = 200 and 400 on I = 64 by neutral absorption. The statement that survives: *bridge-less* rivals resolve only at N = 100.

**Subagent S1** (pair 1 resolves at every N; 0.65 both-present at (200, 16) because the bridge dies in the scramble on 50–70% of 16-island runs), **S2** (q ≤ 0.95; 0.97 at (400, 16)), **S4** (k/N-matched propagules never resolve; ignored stacking), **S6** (separations survive longer at N = 200; degenerate, 0 survivors at both N), **S7** (bridge share set by prior abundance; conflict adds 0.32).

**Design choice dropped: the propagule-validation reference without the stopping rule.** It compared post-freeze neutral drift rather than the law of the process; replaced by the same-stop reference.


## Added 2026-10-05: K at n = 8 (RESULTS.md, "K at n = 8, lemma sharing, and non-per-match budget prices")

**"DAG sharing cuts PrudentBot from 24 to ≤ 16" (Fable, prediction 4, literal clause; falsifier fired).** Under exact sequent identity the DAG is 24: the re-proved Con lemma sits in different contexts (the Löb branch carries □P), so identity shares nothing, and it shortens no n = 6 root at all. Lemma reuse needs weakening-aware (subsumption) certificates, which reach 15.

**"Lazy pricing at c = 0.1 locks in a copy-clique" (Fable, prediction 5, lazy clause at n = 6; falsifier fired).** Top budget share 0.34. With no ALLC punisher the ALLC exit (a constant is free to read) stays neutral; lazy pricing only blocks prover-to-prover drift (N·Δ −300 to −3,000), so π splits by entry rates. The clause holds at n = 8, where PrudentBot punishes ALLC and PrudentBot@16 is absorbing even at c = 0.01.

**"π concentrated on budgets 3–4 as an effect of the price" (Fable, prediction 5 reading).** The share is 0.585 already at c = 0; it comes from the copy-threshold and prior structure, not the price.

**Subagent S3** ("unchanged over b ∈ {32, 54}"; 151 plays of μ-weight 10⁻⁹ change: the count keeps moving on rare disjunctive readers).

**Design choices dropped:** the all-orders Knuth graph with cut on every n = 6 pair (does not fit for a third of pairs; normal-form graph with cut on every pair plus an all-orders 1-in-10 sample instead); unpruned cross-budget closures for the price catalogue (pruned closures agree on four unpruned cells); cut search on all 6,422 n = 8 establisher pairs (a 200-pair sample capped at 10⁵ expansions; cut-free measures cover all); a frequency-dependent cache price (the spec's c·b·k/N with k = 2 on single-mutant transitions used instead). **Not reached:** certification of the cut minima for the P12b self-proof, PrudentBot's sibling and four other sibling and ladder roots (reported as brackets or upper bounds).


## Added 2026-10-05: the modal arm on divide-the-dollar (RESULTS.md, "The modal arm on two-player divide-the-dollar")

**"At n = 7 both arms leak by the same mechanism; the greedy polymorphism holds ≥ 0.8 of π" (Fable, prediction 1).** Neither arm does. The modal arm's π goes to Löbian hawk–dove mixtures (greedy ≤ 0.03); the matched weak arm has no reader shadow because self-simulation diverges, and S3 holds 1.000. The n = 5 weak leak ran on probe readers, which this grammar lacks.

**"P′ cannot re-enter the greedy polymorphism; at best neutral" (Fable, prediction 3, mechanism clause).** P′ is first-order neutral but positively frequency-dependent, with ρ = √(8w/(9πN)) ≫ 1/N; in {S3, S5, A5, P′} it rescues efficiency at odds ∝ N^0.5. The RE's first-draft idea, in its refusing form, holds where P is absent.

**"P(efficient) ≤ 0.6 at 3·10⁴ with P / with P′" (Fable, predictions 2 and 3, one clause each).** 0.653, the trap's efficiency, not a P or P′ effect.

**"Fixed roles keep the accommodator ratchet; endpoints ≥ 0.9" (Fable, prediction 4; subagent S7; falsifier fired).** Endpoints 0.23 in both arms: one-atom conceders target one demand each, so every split is two steps from every other; the ratchet needs universal conceders.

**Subagent S1** (modal ≥ 0.75 at 3·10⁴ with √N odds; 0.653 with exponentially falling odds), **S2 re-entry clause** (P′ carries re-entry; re-entry from the binding trap is a deleterious fixation), **S6** (the reduced subsystem has the full chain's top cycle; P breaks it and the trap lies outside), **S9** (θ-convergence of the lazy chain; 0.44 vs 0.75).

**Design choices dropped:** the n = 11 chain (8,118 classes); `eager_poly=True` in the lazy chain (did not finish); **the linear-domain lazy chain as the large-N instrument where deep polymorphisms exist** (underflow hides deep states behind tiny flows; the seeded log-domain chain replaces it); a full closure chain at N = 10⁴; a dense or sparse solve of the 42,025-state modal fixed-role chain at N ≥ 10⁴; the twin-corrected full stationary solve (4,000-state cap; replaced by exact best paths).


## Added 2026-10-05: K with the 4-rule (RESULTS.md, "K with the 4-rule, and a frozen classifier for what a sound bounded prover loses")

**"The 4-rule re-arms PB2 and the level-2 ladder" (Fable, prediction 1; falsifier fired).** The literal rule □_a A ⊢ □_{a+1}□_a A is vacuous on DSL formulas (Lemma V), and its sound monotone closure re-arms nothing at any b ≤ 54. PB2's missing step is □_b⊥ ⊢ □_b□_b⊥ at equal budgets, bounded self-consistency, which no sound rule supplies within budget b (Lemma G). Reopen only with a different guard convention (the X-arm re-arms PB2) or a calculus with distribution under a box.

**"A frozen proof-trace classifier (Gödel premise or Con under a box) characterizes what K loses" (Fable, prediction 3; subagent S6, S7; falsifiers fired).** Recall 0.42 at n = 8 and 0.33 at n = 6; precision 1.00 rests on the level cap (0.60 at cap 6). It misses Con sentences (K's failure there is missing distribution, invisible to both triggers), resident-side failures and level-≥ 3 plays; 6 of 31 flagged pairs have untriggered alternatives. Not usable as an independent faker control; the faker set has to come from K.

**"Deleting the flagged classes recovers most of the gap" (Fable, prediction 5, ≥ 0.5 clause, inconclusive at 0.39; subagent S9, falsified).** The flags miss more than half of the disarmed pairs.

**Design choices dropped:** the literal 4-rule as the counted arm (provably identical to K; K+4m used instead); the "used hypothesis" restricted search that forbade a triggering diagonal (fixed twice; not a change to the frozen classifier).


## Added 2026-10-05: bridge-less rivals (RESULTS.md, "Bridge-less rivals")

**"More rivals gain bridges at larger cutoffs, so the literally bridge-less share of rival mass falls from n = 9 to 15" (Fable, prediction 1, adopted from sol's review; falsifier fired on n = 9 → 13).** The τ = 0 share rose 0.214 → 0.252 → 0.253 and no bridge-less rival of n = 9 gained a bridge by n = 13 (from 12 to 13, 6 of 76 gained bridges of mass 2–4·10⁻¹⁰). By mass, 0.98–0.99 of the bridge-less rivals are the P\* family, whose cooperation condition, "provable in PA + Con, not in PA", no FairBot-compatible class satisfies at these cutoffs. n = 15 did not fit (140 GB).

**"Every bridge-less rival at τ = 10⁻⁴ separates the archipelago when forced densely" (Fable, prediction 2, bridge-less clause; falsifier fired for S\*).** S\* separated in 1 of 100 runs: it is bridge-less only at τ ≥ 10⁻⁵ and is a sucker of `BOX1(THEM(ME))`. The bridged clause (≤ 0.1) failed narrowly for B₁ (0.12 [0.07, 0.20]). **Design choice dropped:** the threshold τ on the heaviest bridge as the rival classifier; everything τ adds over τ = 0 is A-faked. Use literal bridge-lessness plus an A-faked / mediated flag.

**"|Δq| ≤ 0.1 against the iid control" (Fable, prediction 4, one clause; falsifier fired).** Holder-form q fell by 0.41–0.52 in every cell with an active bridge (neutral absorption replaces locally nucleated holders after nucleation) and by 0.21 with B₁'s bridges removed (faker captures); q_est stayed within ±0.10 everywhere. **Design choice dropped:** holder-form q as the nucleation statistic where bridges or fakers act after nucleation; report q_est.

**Subagent S1** (P\* family establishes in [0.55, 0.95] of dense runs; 0.98, since one copy per island at p₁ ≈ 0.048 gives 1 − 0.952⁶⁴ ≈ 0.96) and **S5** (B₁ without bridges within 0.15 of P\*; 0.67 against 0.97, because B₁'s faker captures it).

**Design choices dropped:** n = 15 and n = 14 for the static screening (140 GB / 16 GB); B₂ as the second forced bridged rival (B₁'s twin; B₄ instead); 40 runs per P\* scaling cell (capped at 12–13 under machine load).

**Operating hypothesis revised (DEFERRED 1):** "metapopulation universality is conceded beyond N ≈ 100 only for bridge-less pairs" is replaced by "metapopulation universality is not claimed along I ≫ N at N ≥ 200", since about a quarter of rival mass is bridge-less and permanent and independent P\* establishments accumulate linearly in I.


## Added 2026-10-05: rivals under K (RESULTS.md, "Rivals under the bounded prover K")

**"The direct-bridge-less share under K is below 0.05 at b = 4, 16 and 54" (Fable, prediction 4; falsifier fired at b = 4).** At b = 4 the share is 1.000: FairBot (copy/distinct thresholds 3/4) and `BOX1(THEM(ME))` (4/7) mutually defect, so A is not a network and nothing can bridge it; rival mass is 0.017 (budget soft cliques, not the P\* family) and 0.80 of natural runs at (200, 64) end separated. Held at b = 16 and 54 (0.000). The budget-independent form of "K removes the bridge-less obstruction" is rejected; it holds from b = 12 at n = 8 (bridge-less mass 2.9·10⁻⁴ at b = 6, 7.6·10⁻⁶ at b = 8, 0 from 12). Reopen only with a budget rule that guarantees each establisher pair's distinct-budget threshold.

**Design choices dropped:** "zero transition" as an operational category (the kernel's fixation is positive for any finite payoff; use the < 10⁻¹² category and the hazard bound); a 1,000-source lumping sample (the language has 610); forced cell (d) (no direct-bridge-less rival under K at b = 16); the K b = 4 natural cell at 1,000 runs (stopped at the complete 50-run prefix under machine load). No subagent prediction failed.


## Added 2026-10-06: K with cut (RESULTS.md, "K with cut and distribution under a box")

**"K_c restores P\* and P2" (Fable, prediction 1; falsifier fired).** Contextual cut does not even yield distribution under a box (Theorem D0), and primitive distribution cannot cross the guard's budget gap: every sound witness-composing rule lands two budgets above its hypotheses (Lemma E1). P\* and P2 are certified underivable at every b ≤ 200, at own and one-up guards, with or without 4m. Reopen only with a guard margin of at least 2b + 7 *and* a 4-rule (the long-guard arm restores P\* at b = 12). The spec's cost recurrence a + c + 1 for distribution was also wrong (a + c + 5).

**"Completeness buys fakers in K_c at b = 54" (Fable, prediction 2; falsifier fired).** In K_c nothing is completed (0/21 Gödel, 0/16 Con set). The claim holds in the long-guard arm (15/21, 12/16 at b = 16, against free-arm victims), where it was exploratory.

**"Guard convention × calculus interacts" (Fable, prediction 5; falsifier fired).** Interaction 0: the guard offset changes no play of L₈ in either calculus.

**"The RE's fixed victim panel as the faker detector" (Fable, design).** It contains none of the Gödel sentences' victims (`BOX1(THEM(THEM))`, `or(BOX(THEM(THEM)),BOX1(THEM(THEM)))`); free-arm victims are the right reference.

**Subagent S1** ("K_c = K at b = 54"; falsified by 2 plays: weakening under a box restores one structural pair).

**Design choices dropped:** distribution as a rule derived from cut (impossible, Theorem D0); the full n = 8 K_c closure (memory; targeted tables, exact by Corollary T); searching general contextual cut (upper-bound sizes; certificates cover it); the capped search to b = 200 (replaced by certificates valid at every size); 3-type deep-state seeding at 476 classes; the cross-budget K_c catalogue and a full long-guard table (not run). RE 3 is untestable in K_c (degenerate design), not rejected.


## Added 2026-10-06: solver audit (RESULTS.md, "Solver audit of the published ε→0 chains")

**"The PD cells have no deep state within coverage" (Fable, prediction 1, first clause; falsifier fired).** All-D is strictly deep under atom pricing at c = 0.01 (μ 0.47, π 0.98): every prover pays the price against D and every constant loses. The numbers clause held (≤ 4·10⁻⁴).

**"The greedy polymorphism stays absorbing; dollar P(efficient) moves < 0.1" (Fable, prediction 2; falsifier fired).** `dollar5 role` at 10⁴ moves by −0.38: a missed five-class role-conditioned hawk polymorphism (R5) absorbs π. "Deep states" holds only modulo twins.

**"Twin drift changes no absorbing state at 10⁴; effect < 0.05" (Fable, prediction 4; falsifier fired twice).** `dollar3 norole` moves from the greedy polymorphism to all-M (+0.37); the modal dollar moves from X+Z+V to an S4-hawk polymorphism (−0.11). In both, a twin that differs off the support exposes an exit 12–20 orders faster.

**Subagent S1** (near-closed classes in the linear solve; none), **S5** (the twin-expanded top state the same at 10⁵ as at 10⁴; R5 → G4 and H5 → a two-class family), **S8** (missed deep states carry < 10⁻³; R5 holds 1.000).

**Design choices dropped:** the ≤ 3-class enumeration as trap discovery in bargaining (traps have 4–6 classes; invasion closure added); the strict operational "deep" alone (empty wherever payoff twins exist); a 10⁻¹² neutrality tolerance on 9-decimal payoffs (flips on rounding; 10⁻⁹); random-start replicator search (200 starts found none of the deep states); expanding every stable candidate (≈ 1 s per seed, 16,000+ per table); θ_log = 10⁻³⁰ for dollar cells (explodes at N = 10³); θ_log = 10⁻¹² as converged (missed R5, put the W artefact on top); two-trap on-demand Dijkstra as the arbiter at 3·10⁴; independent dense solves of the union and three-player generators (did not finish); three-player re-solves at lower θ (stopped after 1.5–2 h at 43% of memory).

**Amended entry (reason: this audit).** The 2026-10-05 entry dropping "the linear-domain lazy chain where deep polymorphisms exist" stays dropped, with its reason corrected: underflow hides nothing that carries weight; what fails is θ-pruned exploration, which misses large-support traps, and lumping, which ignores twin drift.

**Published number corrected (append-only addendum in RESULTS "Divide-the-dollar partitions"):** `dollar5 role` at N = 10⁴, P(efficient) 0.968 → 0.585 and 1/2–1/2 0.806 → 0.000; at 3·10⁴, 1/2–1/2 0.074 → 0.0003. The claim "50–50 survives to N ≈ 2·10⁴ with `ROLE`" (RESULTS "Divide-the-dollar partitions", Reading; THEORY §3) is withdrawn.


## Added 2026-10-06: the social organization game under the seed lottery (RESULTS.md, "The social organization game under the seed lottery")

**"The lever is boss diversity" (Fable, prediction 3; falsifier fired narrowly).** Under a mostly hostile boss seed non-whackers establish on 0.183 (high striker mass) against 0.086 (low), a difference of 0.097; they gain only during the ~30-generation window while constant strikers live, and the diverse seed establishes non-whackers trivially because the initial strike-whacker share is 0.34. The comparison measured seed composition, not a lever.

**"A wage patchwork in ≥ 0.3 of runs at mN = 0.1" (Fable, prediction 5, one clause; falsifier fired).** 0 of 40, and impossible by construction for a closure-verified run at mN > 0 (global closure implies one play everywhere); patchworks appear only at mN = 0 (0.5 of runs), where zero-wage migrants would invade.

**"Arriving in numbers" as a route to Θ(1/n) (the RS's lever, 2026-10-06; the RE's spec).** It removes the cheap credible threat (strike-whackers cut from 0.34 to 0.14 of the boss slot within 25 generations, realized repression 0 everywhere) and leaves the wage at zero on 0.825 of islands, because the abundant striker is wage-blind; the fair wage appeared in 0 of 440 main-cell runs. Dropped as a route on its own; wage-conditional refusal in the prior is necessary (DEFERRED 10).

**Subagent S2** (decline on 0.15–0.55 of islands, policies on ≥ 0.25; 0.69 and 0.10), **S3 mechanism** (RR's intermediate wage from neutral worker drift; the boss race decides while workers stay polymorphic), **S9 N = 400 clause** (≥ 0.3 censored; 0), **S10 Pareto clause** ("RR Pareto-dominates CC in the lottery"; boss 1.55 vs 1.84).

**Design choices dropped:** single-draw matching noise (fitness is the expectation, as in `union_abm` and `rival_islands`); "patchwork at mN > 0 as a finite-horizon object" (not testable under global closure); the continuation of CC main (vacuous, no censoring); matched per-spelling weights for the single-worker variant (a phantom W₂ slot frozen at the scab with native length priors instead).


## Added 2026-10-06: the realizable language, milestone 1 (RESULTS.md, "The realizable language L_T, milestone 1")

**"The JLöb-disabled control shows no cooperation between any two conditional programs" (Fable, prediction 5, control clause; falsifier fired).** In K_T⁻ readers still prove an extensional constant (SC) cooperates by evaluation, and G cooperates with itself and with SF by refutation. What K_T⁻ removes is exactly the Löbian cooperation; the control's claim is stated that way.

**"Harmless variants cooperate with FairBot within +4 of FairBot's threshold" (Fable, prediction 5).** They need +5 (the `let` variant) and +7 (the wrapper): distinct sources pay the joint-JLöb price of distinct budgets plus their own evaluation steps.

**"G's victim, if any, is a level-1 reader" (Fable, prediction 3, partly).** In L_T, G exploits only unconditional cooperators (C, SC); the level-1 reader FB1 defects on G.

**Subagent S7** ("K_T⁻ has no mutual cooperation outside {C, SC}"; G–G and G–SF cooperate by refutation) and **S9** ("every found box has W < 10⁴"; 982 found boxes exceed 10⁴, up to 8.6·10⁵, and prudent self-cooperation needs K = 10⁶).

**Design choices dropped:** a "refuted-search" discharge as a calculus rule (unsound unless charged more than its budget); charging prove searches inside sims in the calculus (circular; the search-charged arm measures the gap instead); a merge-free completeness argument (merges occur; Lemma U); the renamed-variable harmless variant (identical under de Bruijn; a `let` variant instead); the literal sloppy checker as an interesting faker (under the frozen generator it is CooperateBot with a prove-shaped source; a checker that checks rule shapes but not side conditions is left for milestone 3); the "cap + 1" lower-bound memo (replaced before any table by instance-minimum bounds); **milestone 2 as "the length prior over L_T terms up to a node cutoff"** (infeasible as literal enumeration; a grammar or template prior is needed, DEFERRED 11).


## Added 2026-10-06: the realizable language, milestone 3 (RESULTS.md, "The realizable language, milestone 3: the prover as code")

**"Soundness survives with the obligations discharged" (Fable, prediction 4; falsifier fired, recorded in the notes before the run).** Four of K_T's obligations cannot be discharged when boxes mean that a fuel-limited code search finds a proof: Nec (existence is not finding within U); BoxEq (ii)/(iii) (searches on one chain have incomparable costs); budget monotonicity (⊡_b true and ⊡_{b+1} false for FairBot, since the search's own hypothesis changes with b); joint JLöb (a partner's success is not self-fulfilling). Removed, not repaired. P\* still never self-cooperates, by the Run regress rather than a Gödel argument.

**"Simulations cannot be certified without unfolding; SF-type targets obey a fuel bound and prover-type targets do not" (Fable, prediction 3, the dichotomy; falsifier not fired).** SF is certified without unfolding its inner search when that search is the reader's own query (FB–SF from b = 13, k ≥ U + 10); every target obeys the same static cap condition; what separates certifiable from uncertifiable targets is whether their search calls are the reader's own.

**"Checking a supplied FairBot proof costs ≤ 10⁴ steps" (Fable, prediction 1, a guessed constant).** 12,174.

**Milestone 1's min-rule and distinct-source thresholds (RESULTS "The realizable language L_T, milestone 1"; Fable, prediction 2 there).** Artefacts of the primitive-assisted idealization: with the prover as code, no two distinct sound-reader sources cooperate, and FairBot's distinct-budget grid is diagonal-only. The milestone-1 numbers stand as results about the idealization.

**Subagent S1** (SC_code from b = 6; from 2), **S5** (the boundary at U + 9; U + 10), **S10** (SC_code defects on D; it cooperates with everyone, and PB defects on it).

**Design choices dropped:** SrchL (its converse fails); a reflection rule (with JLöb^self it proves anything); an exact-cost side condition checked by running the search (re-enters itself); a static runtime bound for the uncapped search (sound but astronomic; the declared cap U instead); syntactic boxes with a "completeness within cap" assumption (sound only on a closed catalogue; an expensive true box becomes a cap faker); hand instance 6 as first written; the audit entry COREW run under U (now 4U + 10⁶); SF boundary cells at K = 10⁶ (moved to 10⁷); "every side condition true" as the sloppy checker (CooperateBot again; the fit-skipping checker is the meaningful one); the instance-minimum lower bounds of milestone 1's memo.


## Added 2026-10-06: the realizable language, milestone 4 (RESULTS.md, "The realizable language, milestone 4: certificates as code")

**"The guard for the pair rule is that the hypothesis names the checking program's own call" (Fable, RE 1, the guard clause).** Sound but twins-only, plus simulators carrying a self-certificate. The guard that admits distinct sources is partner validation of the swap box (Lemma Sym): the reader validates the partner's script one level deep, so the two checks compute the same predicate.

**"The unrestricted pair rule admits Dcert's cyclic certificate" (Fable, RE 1, the counterexample).** Dcert cannot be certified under any hypothesis rule, because its run has no check call and Hyp only closes boxes a call puts on the right. The unguarded rule's false atom is CBN0 (naive, no list) accepting CBN (naive, which defects on it).

**"Literal certificates do not transfer; quantified templates with checked instantiation cover every held-out same-shape carrier" (Fable, RE 5; falsifier fired).** Literal self-certificates do not exist (Lemma F: an explicit derivation of one's own run is not finite data). Scripts are opponent-generic with no instantiation and cover exactly the sources with their call skeleton; CBPr is PB-shaped but has reversed calls and is not covered.

**"Acyclic proofs certify carrier–SF_k; the pair rule adds exactly the carrier–carrier cells" (Fable, RE 6, two clauses).** SFc needs Hyp^self; the sound arm also adds twins, SFc and CB1–Ccert.

**Subagent predictions:** S3's arm-O twin clause (the frozen production gives self-only carriers no script); S8's regress clause (cross-checker pairs fail by Hyp not applying before any regress in the main cells); S9 as worded (Ccert and SFc are found by searchers); S10's "every production-set carrier" clause; S11's "the actual run succeeds below the boundary" clause; S12 as worded (milestone-3 cells change at 10⁷).

**Design choices dropped:** explicit-sequent certificates and placeholder quines (Lemma F); lookup by opponent key (scripts are opponent-generic); ChkR as one step (a check is charged V + 6, per sol's review); Run without a cap guard (Lemma N's proof needs it; necessity open); the "leaves unchecked" sloppy variant (not run); probes carrying only D scripts (a production bug fixed before any cell); an unbounded host replay (it loops on SFc's self-simulation; now bounded).


## Added 2026-10-06: concessions (RESULTS.md, "Concessions: a boss grammar with probes")

**"P₀'s π sits at the smallest positive wage; P₀₁'s fair state leaks only through the boss shadow" (Fable, prediction 1; falsifier fired).** The ratchet is real statically (T₀ neutral beside D₀, the constant 1/4 boss strictly invades after it) and in a uniform-prior reduced chain (1/4 at 0.85), but under the length prior P₀'s 1/4 occupancy is 0.012 at N = 10⁴ (fair 0.004, zero wage 0.48). The fair state's other neutral exit: D\* reads one worker slot, and the unread slot takes a scab neutrally (mass 0.499).

**"The full discriminator makes the fair share grow with N under the length prior" (Fable, prediction 2; falsifier fired).** P₀₁ fair 0.0086 at 10⁴ (0.0091 at 3·10⁴), within 0.006 of the sham and the reference. D\* weighs 9.7·10⁻⁹ against 0.1025 for each constant. The apparent growth of the explored P₀₁ fair share (0.004 → 0.009 between 10³ and 3·10⁴) is an exploration artefact: cut-corrected it is 0.0020 at 10⁴ and 0.0008 at 3·10⁴, at or below the reference.

**"Quickly, in the lottery: a fair island within 500 generations in ≥ 0.6 of P₀₁ runs; ≥ 0.5 of islands fair at the horizon" (Fable, prediction 5, the RS's direction; falsifier fired).** 0/40 runs ever had a fair island under length-prior seeds, in P₀₁ and in the reference. With militants in numbers (not preregistered) every arm reaches a fair island within ~25 generations; the probe raises persistence (0.32 against 0.05), short of 0.5.

**"The spoilers are accommodating workers and alternative bosses, not fakers; every neutral worker substitute of P₀₁'s fair state is a militant twin" (Fable, prediction 6; falsifier fired).** Demand-lowering neutral substitutes (the scab, T₀) exist for ≥ 0.96 of the fair π in every arm, and a boss strictly cuts after them. Fakers are a spoiler too, and probes add their own: strict wage-faker entry at F\* of mass 0.0095 (0.0116 with the null two-atom policies) against the predicted ≤ 10⁻³; nulling them moves fair by only +0.002 (the clause "changes nothing by more than 0.05" held).

**The RS's prediction** ("bosses adopt concessions of the form 'if they strike, give them what they want', and unions demand higher wages and get them quickly") **failed as scored** (probe-concession bosses 0.006 of π at 10⁴; no fair island in the preregistered lottery). It holds conditionally (not preregistered): with militants seeded in numbers, fair islands appear within ~25 generations in every arm, and 0.8 of the surviving ones are held by a probe-carrying boss.

**The spec's hand analysis of the current-encounter concession** ("the Löb loop lands at (pay 0, strike)"): the evaluator gives (pay 0, work). C₁ pays 1/2 at world 0, the militant's low-wage box fails for ever, and C₁ then pays 0: it is a world-0 wage faker.

Subagent S4, S5 and S13 are inconclusive (explored and cut-corrected numbers fall on opposite sides of their thresholds), not rejected.

**Design choices dropped:** reading a θ-pruned hybrid chain's π without a cut diagnostic (at θ = 10⁻⁹ the P₀₁ cells at 10⁴–3·10⁴ dropped strict faker exits worth three times the explored fair escape, spread over millions of destinations below θ; the explored fair share was 4–11× too high); the full n = 11 P₀₁ chain (439,209 boss functions; mass-preserving substitution instead, spec-sanctioned); a sham made of boxes of fixed sentences (a box of a false sentence is true at world 0 and acts as a world-0 wage faker; literals at every world instead); θ-lowering as the sensitivity check at this state-space size (10⁻¹¹ did not finish round 1 in 70 min; 10⁻¹⁰ did not converge in 2 h; the cut diagnostic instead); the worker-probe arm (not run); a "wage faker" definition counting committed whackers (coercion, not deception; reported separately).


## Added 2026-10-06: mixed budgets (RESULTS.md, "Mixed-budget populations under K")

**"Holder composition separates from the prior after founding by ≥ 0.1 TV" (Fable, prediction 3; falsifier fired narrowly).** Measured +0.030 [0.026, 0.034]. Founder filtering dominates at a horizon of 10⁵; post-founding selection toward higher budgets is real but small (+0.32 budget units). TV against the prior is also a poor detector here: its per-run and pooled versions move in opposite directions.

**"The above-threshold prior has ≤ 2 natural separations" (Fable, prediction 2's point guess; the prediction held on its falsifier).** 6 of 3,000, all through the b = 8 soft clique `and(BOX1(THEM(ME)),BOX1(THEM(THEM)))`@8.

**Subagent S1** (no FairBot or `BOX1(THEM(ME))` copy appears in an above-threshold bridge-less pair; falsifier fired: the b = 8 soft clique is bridge-less against both at 8 and 16) and **S3's reasoning** (holder budgets fall or stay because the budget-4 side is heavier; they rise, since compatibility favours copies with more partners even where budget-4 mass dominates).

**Design choices dropped:** the certified-holder composition vote (local frozenness drops minority islands receiving migrants; replaced by a strong cooperative holder ≥ 0.9 of the island, fixed before any counted run); trace-flag resolution counting (overcounts, 656 vs 438; replaced by the horizon holder test). **Not run** (compute, not design): the forced bridge-less and bridged pairs with their controls, the calibrated cheap-heavy cell, the uniform prior, the scaling panel; RE 4 is untested.


## Added 2026-10-06: the guard margin as a heritable trait (RESULTS.md, "The guard margin as a heritable trait")

No RE prediction failed outright (RE 4 and RE 5 inconclusive). **Design choices dropped, all before any chain:** a single mixed closure at cap 2b + 8 (thrashed at 32 GB; four block closures at cap b by Lemma Cap); the spec's literal faker set (design choice 8: degenerate, 1,005 genotypes of μ 0.53 containing C, D and FairBot; replaced by non-establishers newly invading an establisher, and newly self-cooperating partners); "delete the fakers" as an attribution magnitude (P\*/L's only exits are neutral drift into the Gödel sentences, so deleting them makes it absorbing, P(C,C) = 1; the delete-partners and delete-both contrasts are the measure); an exhaustive low-μ K_c4 tier (0 of 188 chunks in 3.5 h); the seeded solve at weak price selection (c = 0.1; polymorphic expansion did not finish; lazy solver only). **Refuted method claim:** "K's JLöb candidate rule yields a consistent model" fails at n = 8 under mixed guards; a sibling closure (an instance concludes every member of S) is now required and is in the code.


## Added 2026-10-06: the realizable language, milestone 2 (RESULTS.md, "The realizable language, milestone 2: populations of carriers")

**"Almost all seeds, realizably: success ≥ 0.8 on the monomorphic endpoint" (Fable, RE 1; falsifier fired as scored).** 8/40 [0.10, 0.35] under E1, and one run won by the non-carrier `if(CHK(me,them,D),if(CHK(them,them,C),C,D),C)`. The spec's monomorphic endpoint censors islands that stay polymorphic among neutral cooperating classes; with polymorphic islands allowed (E3, stated before any cell) 40/40 resolve cooperating. The establishment clause held.

**"The chain transfers by the same mechanism" (Fable, RE 2; the mechanism failed in the chain as specified).** The top cooperative state is the twin clique TwinD, drift-closed with deleterious exits only, at every N, arm and prior. The mechanism held exactly in the not-preregistered no-clique control (odds slope 0.52, neutral shadow exits ∝ 1/N).

**"Certificate-less spellings never enter carriers neutrally; optional production lowers P(C,C)" (Fable, RE 4; falsifier fired).** 78 neutral entries, all into defection-detector establishers (none into S-guarded carriers); L×O is not lower (−0.002).

**"Every bridge between checker entries is a shadow; ≥ 0.9 of cooperative π on one entry" (Fable, RE 5; falsifier fired).** `Bor` (or over both entries' FairBot atoms) and its order twin are non-shadow, unexploitable bridges of mass 1.2·10⁻⁴; cooperative π on entry 0 is 0.79. The lottery clause (both entries alive on a positive fraction of runs) held, 20/40.

**"The prior does not flip the verdict" (Fable, RE 6).** Held as worded, but through the clique, not the carriers; under the no-clique control U×P (0.98 at 10⁵, uncorroborated) and L×P (0.91) agree and L_std is lower (0.69).

**The sibling theorem's premise outside the modal fragment.** "No class is drift-closed; the obstruction is extensionality" (RESULTS "Conjecture 4") holds in the modal language and fails in any language with quotes: source identity is available (the checker's R/S coincidence here; `eq` in L_T itself), and a drift-closed CliqueBot has positive prior mass. The theorem stands as stated for the modal fragment.

**Subagent predictions:** S2's number (largest check 101,644 > 10⁵), S4 (no exploited establisher; 75), S5 (establisher mass ≤ 0.03; 0.061), S6 (the top cooperative state is prudent), S7 (L×P P(C,C) in [0.1, 0.7]; it is 1), S10 (certificate-less spellings never enter neutrally), S12 (unchanged at K = 3·10⁵; 305 cells change), S13 (U×P below L×P); the notes' §1.7 hand claim "no exploited establisher at n ≤ 7" missed the defection detectors.

**Design choices dropped:** the literal endpoint closure test of notes §1.9 (replaced before any cell by the closure-of-entrants rule); the executable table on every τ pair (infeasible; composition on class representatives); the full executable E table (≈ 3 h; a 291-class sample); E's chain at 3·10⁴ and 10⁵; byte-keyed lumping (memory; hashed keys with exact verification); milestone 4's `HostCheck` memo (order-dependent; `ExactHost`); the no-clique control at θ = 10⁻¹⁴ and the U×P no-clique cell at 10⁴ (unfinished); an unbounded invasion closure (branch 3 with 6,000 nodes instead). **Process:** `pkill` of a driver leaves its pool workers running as orphans; four ran for up to four hours beside the three permitted workers before being killed by pid (kill the pool's children by pid first).


## Added 2026-10-11: identity and tags (RESULTS.md, "Identity and tags in the carrier grammar")

**The pooling rationale for the seed lottery (Fable, DEFERRED 1, 2026-10-10; refuted at establishment).** "A universal family pools its seed mass across spellings while an exact-identity clique cannot, so the lottery's selection pressure matches the universality target." Ten mutually incompatible clique spellings at M/10 establish as well as one identity at M (islands per seeded copy 0.197 against 0.204), because each spelling nucleates and colonizes on its own, and a clique converts seeded copies into islands 2–4× better than an open carrier by playing D against the seed's unconditional cooperators. Pooling matters only for slow absorption among established islands. The RS's decision (the seed lottery as the object) stands; its rationale does not, and the lottery does not deliver universality at identity mass 0.009.

**"Families beat cliques by established mass; the open family holds every island on ≥ 0.7 of runs" (Fable, RE 2; falsifier fired).** 0/40 universal under L; identity cliques hold 0.41 of islands. The established-mass clause held (113/115).

**"Pooling, matched" (Fable, RE 3; falsifier fired).** T1b ≈ T1a on islands held; carriers won 0/40 and 1/40.

**"Tag clubs resolve through the marked carrier" (Fable, RE 4; falsifier fired as worded).** The club at mass M is extinct by median generation 110, eaten by marked defectors, before any rivalry forms; the bridge was never tested.

**"Exclusive clubs make permanent patchworks" (Fable, RE 5; falsifier fired).** XC, prudent and S-guarded, beat the open family by majority in 9/40 runs without a bridge.

**RE 6's resolution clause** (0 resolutions at I = 256).

**Subagent predictions** S7, S9, S12 (second clause), S13, S14 ("open top state"); two hand slips (the eq run tree has 12 spellings, not 11; XC has 6 nodes, not 7).

**Design choices dropped:** the self-probe for production (it turns `CHK(me,me,C)`-readers into Löbian cooperators, a different ecology); island P(C,C) ≥ 0.9 scoring (replaced by holder-based outcomes under the migrant load, before any counted cell); per-pair separation hazards (saturated: every run separates by generation 20–30); the full-catalogue chain (90 min without finishing a cell; the reduced-support diagnostic instead).


## Added 2026-10-11: prudent openness (RESULTS.md, "Prudent openness against identity")

**"CBP is not compatible with CB, and the tactic produces CBP's D script against ⌜CB⌝" (Fable, RE 4 (i) and (ii); failed statically).** The hand reading conflated the certificate-carrying cooperator Cc with the certificate-less constant ⌜C⌝: `CHK(them,⌜C⌝,D)` is certified by every S-guarded carrier, so CBP is open to CB, and no D script of CBP against ⌜CB⌝ exists. The spec's premise ("CBP's family excludes the nice carriers") was wrong, and its literal tilts measured a nice-dominated family; the matched core/nice cells added before any cell are the informative ones.

**"Prudent openness establishes like a clique; F_P universal ≥ 0.5" (Fable, RE 1; falsifier fired).** F_P-universal 0.175; the ≥ 0.35 islands-per-copy target was unreachable, since a block at M caps at 0.32.

**"Pooling beats identity head to head" (Fable, RE 3; falsifier fired for F_P).** 0.30 vs 0.39 of islands; the mechanism holds for the prudent core alone (0.52 vs 0.25).

**"The scaling panel moves the crossing by ≤ 2×" (Fable, RE 5, panel clause).** No crossing exists at (100, 128), where the clique-free baseline is 0.475; the 50% level is set by an (N, I)-dependent baseline. **"Prudent-open on top of the no-clique chain at 10³" (Fable, RE 6).** XC′ is on top at both N.

**"Universality in a quoting language is a property of identity's *price* in the prior" (Fable, THEORY §9.2 after the identity run; refined).** It is a property of identity's seeded *abundance* relative to an (N, I)-dependent baseline: about 8 seeded clique copies per run at (100, 64).

**Subagent predictions:** S1, S5 (the core without cliques badly underrated), S7, S12 missed on numbers; S10 indeterminate; the notes' §1.7 claim that the second curve's m_L point equals P1 (caught by a test).

**Design choices dropped:** "CBP's family" as the test of prudence (the matched core/nice pair instead); the two-point panel as a crossing locator (it cannot locate a crossing when the baseline moves; the m = 0 baseline was added at each panel setting); P_open as worded (28 classes, 12 outside the open family); a first launch whose numpy threads oversubscribed the shared machine (killed by pid, relaunched single-threaded).


## Added 2026-10-11: the social organization game over the realizable language (RESULTS.md, "The social organization game over the realizable language")

**"The founding-coalition mass exceeds the modal run's by ≥ 10³" (Fable, RE 3, coalition clause; the falsifier, ≤ 10×, not fired).** ×25: concession bosses carry 32% of the L mass and constant fair bosses 0.4%; the library's gain is in concession-like programs as a class (0.18 of the boss prior), not in D\* in particular.

**"Low-wage work occurs by timeout or substitution" (Fable, RE 2, wording).** In the catalogue it is acceptance (0.632 of triple mass) and uncertified default (0.034); 0 false-certificate fakers.

**"The dominant exit is unread-slot drift followed by a boss cut, ≥ 0.5" (Fable, RE 4; missed narrowly, 0.49).** **"D\*₂'s persistence with migration exceeds D\*'s" (Fable, RE 5; failed, 0.950 vs 0.999; residence censored).** **RE 6 void:** the ¼ probe certifies recommendations, not executed strikes, so under RR the table gives ¼ on every island.

**Subagent:** S4 (concession share < 5%: 32%), S5 (L establishment ≤ 0.35: 40/40; the seeding arithmetic ignored concession mass), S8 (persistence ≤ 0.5: 0.75), S2, S10, S13(b), S14 clauses; S1's aggregation argument (D\*/constant ≈ 2⁻⁹; it is 2⁻⁶ because constant classes are single spellings).

**Design choices dropped:** milestone 4's fixed swap partner (no canonical partner across three subjects; the closure instead); forbidding Run on encounter boxes (it kills every probe); the tactic with Hyp first (never follows an F-branch; the path tactic instead); probe-set production; the lottery on the executable K = 10⁶ table (needs a full cost model; the ideal table plus an audit instead); lazy triple caching (an exact factorized table made it unnecessary); rebuilding the modal P₀₁ n = 11 language for the coalition comparison. **Not run:** L at (100, 256); the diagnostic chain (stopped unconverged at cut 0.97).

## Added 2026-10-11: fixed-role chicken (RESULTS.md, "Fixed-role chicken and hawk–dove without `ROLE`")

**"Migration does not simply merge the norms; resolutions are demographic; removing bridges changes resolution by ≤ 0.1" (Fable, RE 2; falsifier fired).** Removing the conditional straights cuts resolution from 0.28–0.78 to 0 in every arm and game; demography matters only at N ≤ 50. My post-review bet reversed the wrong way: the readers do bridge the norms, through a coupled two-seat flip.

**"Per-island establishment ≥ 0.6 everywhere; reading changes it by ≤ 0.1" (Fable, RE 1; falsifier fired in weak hd3 at N = 25, 0.48).** The cause is seats frozen on an X-mixture at ε = 0, not reading. **"Provable commitment changes nothing" (Fable, RE 4; falsifier fired at mN = 1 in chicken, M0 − W0 = −0.35):** provability changes how norms merge under migration, not which norm forms. **"C = 6 lowers crash exposure" (Fable, RE 5; fired):** hd6 crashes more than chicken; cheaper crashes linger. **RE 3's hawk–dove trap clause:** impossible in the two-population chain (Lemma F).

**Subagent:** S3's flux clause, S4–S7, S8 at mN = 1, S9's dove clause and its arithmetic reason, S11's ±0.1 falsifier (ignored that islands within a run share a norm); the hand claim that W0/M0 differ only on matcher–bridge cells.

**Design choices dropped:** the frozen flip-attribution rule (last-sample bridge share; superseded post hoc by the window maximum and the forced control, disclosed); the one-population chain panel cut from 21 to 12 cells with the invasion closure capped at 2,000 nodes; the pooled Wilson interval for the role split (run-level instead).


## Added 2026-10-11: the gene arm (RESULTS.md, "The gene arm")

**The RS's proof device as stated** ("no credible deviation, say a Pareto improvement, exists at the stable state, else it would have been adopted as a fit gene"): fails on half the length-prior π, because the improving move out of a zero-wage split is neutral for its carrier and strict gene-stability cannot exclude it; it holds only under whole-program credibility, which selects ¼ and 0. **The RS's asymmetry as a credibility property** ("the union may special-case on a quorum, the boss may not special-case a threat"): no per-point test separates a committed strike at s > 0 from a committed whack; the asymmetry is structural (two slots against one). **The RS's target class G-recip** (RE 8; falsifier fired before any chain): 45,014 Pareto-dominated gene-stable triples; it cannot choose among wages, since zero wage with everyone working is Pareto-efficient.

**"The override filter alone does not recover RC; whole-program credibility does" (Fable, RE 1; both falsifier clauses fired).** The filter's effect is the removal of the world-0 wage faker (uniform-prior fair 0.012 → 0.914, random removal 0.011), and whole-program credibility is RR. **RE 2's** clauses "the whack gene deters" (a `BOX(W_j = strike)` whack never deters) and "zero wage ≥ 0.4 in every gene arm" (controls 0.28–0.30, RC 0.34, G-cred-whole 0.24). **RE 3** (targeted SG raises fair; SG −0.005, the untargeted kernel highest; the effect is mutation support). **RE 4's fair-state clause** (reverse: gene-stable under G-all, unstable under G-cred-whole, since the rational militant works at world 0). **RE 5's coalition clause** (ρ₂ = ρ₁ρ₂′, ε\* ≥ 21, never faster) and mechanism (the exit is a lone constant striker then the boss's raise, not a quorum gene). **RE 6's control clause** (bridge readers give absorbing mutual swerve, not a norm).

**Subagent:** S3 (|G-cred − G-all| ≤ 0.05; 0.90 under the uniform prior), S8 (conventions ≥ 0.95 in every chicken arm; the control gives mutual swerve), S14 (the weak version removes every dominated gene-stable state; 12,740 remain), S13's lottery clause, S4, S5; the notes' hand claim "S is gene-stable under G-cred-whole" (corrected by code before any cell).

**Design choices dropped:** the ≤ 2-gene social-organization chain (scale guard; one gene per program instead); the union run's QUORUM in the base (vacuous at the fair wage under "or"; Q\* instead); a stage-1 whole-program filter (empties the boss set); whole-program credibility in chicken (empties the catalogue); SG's box-at-stable-world reading (not lumpable); a uniform prior over program texts (too diffuse for the solver; a named catalogue instead, before any uniform cell was read); "every class triple with no strict exit" as seeds. **Not finished:** G-all with SG or the local kernel under the length prior.


## Added 2026-10-12: certificates as genes (RESULTS.md, "The realizable language, milestone 5: certificates as genes")

**"Search alone is twins-only in populations; S-only ≤ 0.2 of H-only" (Fable, RE 2; falsifier fired).** S-only E3 is 40/40, equal to H-only, and search restores every (H, H)-cooperating distinct carrier pair by encounter 2–3. Milestone 3's twins-only result belonged to reading by search (which re-enters the opponent's search), not to producing one's own script.

**"Every held script has a host ancestor in the mixed cell" (Fable, RE 6; falsifier fired).** 0.75 of held instances are host-free, and host-free scripts are held by types cooperating with other units in 28/40 runs.

**"S ≤ 0.1; H leads during acquisition; C/CS exceed H under a price" (Fable, RE 4 clauses).** Final shares S 0.29 and CS 0.38; at generation 10, S 0.44 and H 0.11; under the price arm H holds 0.27–0.32, since H is free and the price is ≈ 10⁻³ of the stakes. **"Seeded C-only establishes ≥ 2× later" (Fable, RE 5 timing clause):** 1.2×. **"C cooperates iff on the graph" as an exact catalogue-level law (Fable, RE 1; fired narrowly):** 18 F1 exceptions on the graph, 14 off-graph cooperations through D scripts.

**Milestone 3's search CORE as the producer (the spec's text).** It cannot output a K_T^cert script (no rule for check calls; Lemma F); the producer is milestone 4's tactic written in L_T^code. **The single-entry adoption check** (notes §1.3, revised §1.15 after a counted single-pair finding): blocks every PB-shaped copier (F5). **The S gate plus unbounded copying in populations** (notes §1.3, revised §1.13 after the scale guard): the unit universe grows without bound; measured in the single-pair tables only.

**Subagent:** S3 (a 116,877-step production and 16% cap timeouts), S4's S clause, S6 (scripts are not tied to codes), S13's inheritance clause (transient establishment in 6/10), S15 (CS cost 943 → 4,406 steps per match between N = 50 and 200); S5, S8, S9, S11, S14 missed numbers.

**Design choices dropped:** the gate rule in populations; the single-entry adoption check; an exact per-pair term cost model; exact per-opponent cap timeouts; the no-clique frozen chain (unfinished); 40 runs for the secondary cells. **Process:** a duplicated secondary batch ran 6 workers for ≈ 3.5 h (a queued shell believed dead); the worker formula in the prompt counted shell wrappers and single-process cells.


## Added 2026-10-12: provenance (RESULTS.md, "Provenance: who writes the first certificate, and against whom")

**"The majority rule depends on coverage, not on an ordering; S-3 within 6 of S-nonself; S-2 ties near S-self" (Fable, RE 3; falsifier fired).** S-3 is 15/40 against S-nonself's 28 and S-2 13/40, both below S-self (22): the fallback keeps the identity script ι for the only-self class, S-2 does not tie (σCB1 also validates at the self root), and the window's timing costs universality by itself (post hoc 12/40 and 18/40).

**RE 5's clauses (Fable):** S-2 is not enriched at establishment (0.229), frequencies do not drift back (S-2 rises to 0.301), and the mixture is below both pure rules (17/40). **RE 4's clause "≥ 1% never acquiring by the horizon":** no producer is still lacking at the horizon; 99% of capable producers die unacquired. **RE 2's premise "≈ 57 copies":** that figure is the identity grammar's; here 4.6 TwinD copies; the number held.

**The hand claim "the gate cannot repair the only-self class" (notes §1.4; subagent S12's reasoning).** Once a holder has ι its self-box is true and its production then succeeds at distinct roots; only 14 of 97 run trees remain only-self in the gate universe.

**Subagent:** S12 (cache ≥ 2×; 1.1×), S6 (S-k within 6 of S-self; 7–9 below), S8 (safeguard ≥ 0.8; 0.78), S9's mechanism clause, S11 and S14 universality clauses (C-donor 20/20 at N = 200), S13 (island P(C,C) 0.947 pulled down by two all-D runs).

**Design choices dropped:** full validity for the S-k safeguard (Lemma V: a window never fills from empty founders; own-side validity instead); "every candidate scores ≥ 1" (false for 468 of 19,102 signatures, F1); the mode marker in the quote; processing settled and futile encounters one by one (an exact skip instead); E3 at every checkpoint in extensions; extensions of all-defect runs; the gate cell's extensions after 15 replicates. **Process:** the main batch launched twice (18 runs set aside) and resumed once; the gate closure on 1 worker before 3; three post-hoc diagnostics added after seeing S-k.


## Added 2026-10-13: stable sets on islands (RESULTS.md, "Stable sets on islands")

**The RS's claim, "each element of the stable set shows up on an island."** Weak form: holds only without migration, as a role-symmetry and coordination fact that constants reproduce (0/40 with migration). Strong form: 0/40 without migration; with migration it holds at N ≤ 150 only by consensus on one member and fails at N ≥ 200 (0.25). The stable set is a menu the dynamics do not respect.

**"Member occupancy ≥ 0.6" (Fable, RE 1; falsifier fired).** 0.28; unequal pairs (0.42), frozen wasteful pairs (0.23) and disagreement (0.07) fill the rest. **RE 2's tilted clause:** no discriminatory element is realizable in `dollar3` and no discriminatory stable set exists on any grid (Lemma G); the within-run clause also failed at mN = 0. **"≤ 0.1 of islands on non-members" (Fable, RE 3; fired at mN = 0 and at N = 200):** wasteful islands are absorbing at ε = 0, not transient. **RE 4 (Fable; both clauses fired):** members switch by neutral drift through member-mixed states (1,342 of 1,350 flips), exits from outsiders follow arrows 0.45 of the time, consensus is reached in 0.95 of runs by constants alone; the spec's premise "a flip between members passes through an outsider" is dropped (internal stability forbids dominance between members, not drift). **"Myopic beats farsighted" (Fable, RE 6; fired at mN = 0 and N = 200):** unequal pairs are farsightedly stable (TU and game effectiveness) and hold 0.42 of islands. **RE 5's band clause at mN = 1** (missed narrowly). **RE 7's mechanism** (greed establishes against accommodators; the numbers held, constants reproduce them, and the sweep goes to fair pairs at N ≤ 150). **The "Anesi (2010) myopic" attribution** in the spec and DEFERRED 15: his result is about farsighted voters.

**Subagent:** S4 (fair ∈ [0.2, 0.45] at mN = 1; 0.74), S6 (member → unequal flips drift-prepared; 0.07, concurrent polymorphisms instead), S11's grand clause, S13's consensus clause, S15's "RE 6 void".

**Design choices dropped:** the literal uniform-over-demands control (duplicates L; uniform over programs instead); the 1/8 grid in the main grammar (`dollar3` hard-codes nine actions; a constants extension instead); the first forced-residence exit rule as the only measure (it counts migrant dips; a second measure reported beside it); the selection statistic "which stable set" (vacuous with one stable set).


## Added 2026-10-14: dominance contracts and refusal (RESULTS.md, "Dominance contracts and refusal on islands")

**The RS's prediction, "contracts deviating to dominating actions will recover the vNM stable set."** Failed at both migration rates on every definition (occupancy 0.338 / 0.091, modal 0.338 at mN = 1; support ⊆ V\* 0/40). Contracts reproduce the proposal generator's walk (V\* exactly 1/3); recovery needs a refusal guard on exits from V\*.

**"Refusal is lost where private and a martingale where public" (Fable, RE 4; failed).** Neutral at mN = 0 in both variants; at mN = 1 the bit rises in 40/40 runs in both (public 0.50 → 0.80, private 0.50 → 0.96) by immigrant rescue. **RE 5 at mN = 1** (fired on the 0.95 classifier, 0.33, by migration load, not escape). **RE 7 revised** (flow threshold 0.40, not > 0.5; fixation 0.13 at β = 0.25; D3 +0.12) and **Gemini's counter** (fixation < 0.05, D3 identical): both failed. **RE 7 as first drafted** (joint entry at β = 0.25 fixes in ≥ 0.5 of events) was withdrawn before the run after Gemini's coordination argument; the run confirms it would have failed (0.13). **RE 8's premise** (D1 higher at mN = 1) false.

**Subagent:** S2's mN = 1 interval (the hand chain ignored migration load), S4's same-member return clause, S5 (entries not by contract 0.014, not ≥ 0.4), S6 (member-exit fixation ≤ 0.05), S8 (the private bit rose), S9's mN = 1 interval. **Dropped:** the hand interleaving of the contract walk with measured relation-P rates at mN = 1 (ignores the migration load contracts create); the static coordination threshold as the operative one (the flow threshold is); the 0.95 classifier alone for mN = 1 contract cells.


## Added 2026-10-14: the social organization game, fully realizable (RESULTS.md, "The social organization game, fully realizable")

**"Under S-nonself₃ the fully realizable cell is fair on a plurality of islands: persistence ≥ 0.3, zero wage ≤ 0.2" (Fable, RE 4; falsifier fired).** 0.084 (3 of 40 runs), zero wage 0.45; the ideal table gives 0/20 and 20 forced coalition founders give 0.70, so under endogenous production the fair state is a seeding threshold, not cost or sustain. **"The greenbeard union holds ≥ 0.2 of fair islands under H + eq" (Fable, RE 2's H clause; fired).** 0.005, all strike-pact mixtures; no union-held island anywhere (Gemini's G held). **"Production adds ≤ 2× to the median encounter" (Fable, RE 5; fired).** 4.0×, futile lack-rule retries (0.97–0.99 of attempts return NONE), not timeouts (0.14%). **"Closed shops are conditionally fit" (Fable, RE 6; fired).** Neutral on T₁ islands; tracks prior mass. **The RS's clause (ii), "identity never takes the fair share from 0 to positive".** Failed narrowly in the S arm (0 → 3 of 40 runs); the falsifier (≥ 0.2) did not fire, so the prediction holds on its falsifier.

**Subagent (fired):** S1's dynamic clause (2,254 worker row classes in one run), S2 (identity does not dilute coalitions; the prior is identity-blind), S4 (executable within 0.05 of ideal under H: 0.025 vs 0.500), S7, S12, S14 (zero wage ≤ 0.10: 0.45–0.59), S16 (drift ≥ 0.6 of exits). **Clauses failed:** S6, S10, S11, S19; S15 missed its number. **Hand estimates dropped:** notes §1.5's "(d) ≤ (a)" and the dilution estimate of the coalition mass; U_eq at 6 nodes (it has 7). **Design choices dropped:** per-spelling cost tables; `EQS` against a fixed quote as the sham; prefilled production rows; the first-fair-check establishment as the only reading; 20 runs at (200, 64) (12). **Process:** the lottery batch was killed twice to change the summary (deterministic runs, 7 counted runs rerun); once the pool respawned three orphaned workers, killed by pid with no duplicate output; four diagnostics ran in a slot freed by SIGSTOP/SIGCONT of one lottery worker, keeping ≤ 3 processes.


## Added 2026-10-14: farsighted refusal (RESULTS.md, "Farsighted refusal")

**"U-g1 occupancy within 0.05 of the baseline plus converted disagreement" (Fable, RE 1, occupancy clause).** 0.188 against 0.292: early contract jumps out of disagreement-modal scramble islands land on V\* only 0.16 of the time and then freeze. **"Other KR fixed points absorb on held-player pairs" (Fable, RE 2, second clause).** None does (certified at δ ≤ 0.9); the unequal-absorbing ones absorb on rotating triads. **"U-gKR(0.9) lies between D1 and gV" (Fable, RE 3, second clause).** The δ = 0.9 default accepts every member exit and equals D1. **"The reader rises against gKR in C3-read" (Fable, RE 7 revised; falsifier fired).** Below gKR in 24/40 runs. **"A reader's decision costs ≤ 10⁵ steps" (Fable, RE 8).** 2.6·10⁵; the falsifier (> 10⁶) did not fire.

**Subagent:** S3 (U-g1 at mN = 1 in 0.55–0.80: 0.395, bimodal), S5 (no V\*-absorbing fixed point at δ = 0.8: one exists), S13's first clause (g1 rises in ≤ 0.6 of runs: 32/40), S14 (gV ≈ gKR in C3: gKR leads by 0.48 at 10,000), S16 (rare gKR rises in ≥ 0.7 of runs: 27/40), S19's derivation clause (≥ 10⁶ steps: 6.7·10⁵ at δ = 0.9); hand H1, H4 and the §1.6 cell numbers. **Dropped designs:** the plain certified branch and bound at δ ≥ 0.95 (did not terminate in 10⁶ nodes; a big-M MILP failed at δ = 0.9), replaced by a decomposition whose list is uncertified at 0.95 and 0.99; forced starts at mN = 1 (not run).


## Added 2026-10-14: the leader-value core existence sweep (RESULTS.md, "The leader-value core: where it exists")

**"Public goods empty on a substantial share" (Fable, RE 3 revised, share clause).** 0.041 pooled over n = 3–5, and 0 under 2√G and CRRA ½ (up to 0.32 under ρ = 2 at n = 3): production curvature and two dominant valuations decide, not substitutes as such; free riders are the violators wherever it is empty. **"Supermodular games with negative spillovers are empty somewhere" (Fable, RE 4, negative clause).** 0/643: aligned negative spillovers satisfy the same follower-dominance lemma as positive ones; emptiness needs mixed signs, where it is a coalition-size effect. **"Some coalition's first-mover advantage is necessary for emptiness" (Fable, RE 6, the weakened characterization; falsified).** Majority division under pess and allocation games under opt are certified empty with no first-mover advantage; it holds only within the timing families (199/199). **Cournot empty for n ≥ 3 at every cost profile and concave public goods nonempty** (Fable, RE 1 and RE 3 as first drafted) were withdrawn before the run on review (sol's symmetric-Cournot argument; Gemini's free-riding argument); the run confirms both withdrawals.

**Subagent:** S2's share clause (n = 3 TU-empty 0.030 < 0.05), S4's clause that every coalition has a second-mover advantage in differentiated Bertrand (coalitions of size n − 1 gain from leading at n ≥ 3), S7 (the γ-core nonempty at every generic point: empty at 13 mixed-spillover points), S11's second clause. **Dropped design:** direct Nelder–Mead NTU search for quadratic games (≈ 140 s per point, inconclusive), replaced by weighted-utilitarian candidates with bounds and a menu branch-and-bound. **Process rule:** every primal coalition value is checked for feasibility and paired with a dual bound (a first pass accepted an infeasible solver output and reported 19 spurious empty economies).


## Added 2026-10-14: legibility at founding (RESULTS.md, "Legibility at founding")

**"Legibility at founding is the mechanism where fuel does not bind: L1 ideal and L3 ≥ 0.3" (Fable, RE 1; falsifier fired).** 0.001 and 0.002, the scramble unchanged (|Δ| ≤ 0.01): founding lists equal first-encounter production, about 0.01 generation of selection. The run engineer's reading in "The social organization game, fully realizable" (legibility at founding) is dropped with it. **"Fuel and legibility compound" (Fable, RE 3; fired).** **Gemini's counter (L3 ≥ 0.3)** failed; its fallback (demographic mass) is untested here. **Sol's "L1 improves early militant survival"** failed (unchanged within ±0.01). **The amendment's bare-source key for the negative cache** (and the premise that production reads sources only): rejected, since checks read partners' lists and a replay found 27 suppressed successes in 320; replaced by the invariant key.

**Subagent:** S5 (natural generation-0 yield 0: it is 0.33), S12's natural clause (militant strike probability ≥ 0.95: 0.84), S1's 10⁶ clause (missed narrowly). **Hand claims dropped:** notes §1.3 (natural yield 0; strike-probe concessions never certified at generation 0). **Dropped designs:** L2 as the base for speed (no wall-time saving); L1 + L2 and the N panel (cost, the spec's drop order); L1-withheld beyond 5 runs (delivery empty); "withheld until the first selection event" (indistinguishable from L1; generation 10 instead).


## Added 2026-10-15: the realizable lottery along paths in (N, I, mN) (RESULTS.md, "The realizable lottery along paths in (N, I, mN)")

**"Under S-nonself universality goes to 0 along P2 and P3; ≤ 0.2 at (100, 256) and (200, 128)" (Fable, RE 2; falsifier fired at (100, 256)).** At N = 100 identity islands are absorbed by coordination (ρ ≈ 2·10⁻⁵ per open migrant) within about 10⁴ generations: (100, 256) is 0.10 → 0.30 → 1.00 at 2,000 / 10,000 / 40,000. Universality goes to 0 only along paths through N ≥ 200. **"q falls with N along P3; P2 plateaus" (Fable, RE 1 clauses).** Along P3 q rose through clique-border load; along P2 q fell to 0 as scramble failures vanish with I. **"Calibrated migration rescues bridged failures and no bridge-less ones" (Fable, RE 4).** Untestable as worded (no bridged failure at N ≥ 200); in paired form migration changes which rivals establish, not whether they resolve. **"The threshold collapses onto one copy curve everywhere" (Fable, RE 5's "everywhere" clause).** Fails at (100, 128), where coordination absorption leaves no crossing; the collapse holds where cliques are permanent. **"C-donor fails along P2 by identity" (Fable, RE 6, P2 clause; fired).** 0.80, failures mostly non-identity; C-donor identity islands ≤ 0.004 everywhere.

**Gemini G1 (P1 more universal than P2 at matched copies, by per-island clustering):** failed at the scoring horizon (0.55 vs 1.00), and clustering does not matter (0.127 vs 0.131 per island); the real difference is N. **Gemini G2 (C-donor (400, 64) < 0.75):** failed (10/10, calibrated arm, 10 runs).

**Subagent (fired):** R1 (ē ≥ 0.97 and all-island success ≥ 0.85 at N ≥ 100: scramble failures at (100, 32), clique-border load at (200, 128)), R6 (panel q_c within 2×: 0.018 at (100, 128)), R7 (multi-copy islands ≥ 2× singles: ratio ≈ 1), R10 (half of the controls' failures at N ≥ 200 bridged: none of 378). **Clauses missed:** R2 ((400, 64) 0.55), R3 (N = 50 identity failures absorbing, not coordination-limited), R4 (C-donor 0.80 at two cells), R5 (ablation − proportional +0.15 at (200, 64)). **Hand estimates dropped:** "C-donor removes the identity mechanism by construction" (a TwinD copier reaches its identity unit in at most one run per cell); f₀ ≈ 0.9, q_c ≈ 0.05. **Dropped designs (budget, disclosed):** the copying rules' 10,000 extensions; C-donor (400, 64) at mN = 1, dense donors at N = 400 and at mN = 1; half the C-donor (400, 64) calibrated runs; the 400-generation C-donor calibration horizon (150); the run-level T_nuc definition (per-island instead, both reported).


## Added 2026-10-16: removing rival networks (RESULTS.md, "Removing rival networks")

**The RS's criterion as a prediction, "drift should never colonize an island, only reintroduce fit programs".** False under seed rain at N = 200–400 at every rate tested: drift colonizes, mostly as neutral shadows of the target. Drift falls ∝ 1/N while predator cures do not, so the divide is a large-N (annealed) property, not one available at these sizes. **"≥ 0.8 of non-identity rivals are exploitable" (Fable, RE 1; fired).** 0.15 on the target definition; the dominant class is closed-open (FairBot-bridged neutral flux), which the scaling classifier counted inside the network. **"Rain does not break the network" (Fable, RE 4; fired).** Non-flip losses 0.09 / 0.20 per island at εN = 0.01 / 0.1, including permanent identity takeovers through exploitable shadows. **"The sponsored donor prevents cliques; sponsor plus rain ≥ 0.95" (Fable, RE 5 and 6; fired).** Identity remains (0.02–0.04 of islands); uot 0.10 at (200, 128). **"An admissible window exists at εN ≤ 0.1" (Fable, RE 8; fired).** **Gemini's counter (cure < 0.4 without a constant predator):** failed; no constant is a predator and the cure is 0.92. **Sol's "many exploitable rivals stay unresolved":** failed (0.07 at εN = 0.1).

**Subagent:** M1 (the target is broader than expected: 0.71 of universal-open runs on target), M3's ratio (6×, not 10×), M5's closed-open clause (not absorbing), M6, M7 (the residue is identity and exploitable, not closed-open), M8, M9, M4 at εN = 0.01 and 1, M10 at εN = 1 and N = 400. **Dropped designs (budget, disclosed):** B1 on the mN = 1 arm beyond 6 checkpoints; one slow checkpoint; C-donor rerun; 10 instead of 20 injection replicates at N = 400.


## Added 2026-10-16: cliques on a Pangaea (RESULTS.md, "Cliques on a Pangaea")

**The RS's mechanism, "universality pays off".** The prediction held as scored, but the mechanism is mass: a TwinD identity is a frequency-dependent self-cooperator like the open network, with about 1/300 of its mass, and wins a whole Pangaea when the network nearly fails (1/20 at 3,200 and at 25,600, post hoc). **"≤ 1/20 all-defect on a Pangaea; none under free certificates" (Fable, RE 2; fired).** 5/20 at 6,400 and 4/20 under free certificates: a Pangaea fails to establish with probability ≈ e^(−N/4,500), a demographic loss that "prudence is never worse than defection" ignored (also the subagent's §1.1, S1, S12, S15). **RE 1 at 6,400** (one network in ≥ 0.9): 15/20 by all-defect. **Gemini's counter (target share 0.75–0.90 in ≥ ¼ of runs):** 0 runs; neutral remnants are gone by 2,000. **Sol's clause (ii) (neither monotone nor the stated crossing):** both held.

**Subagent:** S2 (target ≥ 0.9 in ≥ 18/20; fired at 6,400), S3's max clause (0.026 > 0.02), S4 (AP 0.234 > 0.1), S5's band, S6 at (6,400, 1), S9, S10 (+5 at (100, 64) at 10,000, p = 0.18; coverage at island establishment 0.37–0.49), S11 (one donor suffices on a Pangaea: 5/20 and 7/20). **Dropped design:** the r-cap validation (superseded by constant production per program).


## Added 2026-10-16: coverage components (RESULTS.md, "Coverage components")

**"Untravelled paths carry regrowth" (Fable, RE 1; fired).** Granting them gave 0/20: production writes them itself at the first encounter that takes the path; they are necessary when barred, not sufficient. **"Second paths matter little" (Fable, RE 2's (b) clause; fired).** Barring (b) gave 0/20; (b) is the carrier. **"Only (a) is sufficient" (Fable, RE 4; fired).** Plus (b) gave 0.30, confirmed at 0.24 on 40 fresh streams. **Gemini's counter ((a)+(b) needed, ≥ 0.25)** and **sol's counter (a pair beats every singleton):** both pairs gave 0.10, below plus (b). **The spec amendment's literal partition** (components ⊆ H \ S₃^static with S₃^static path-free) was inconsistent ((a) empty) and replaced by H \ canon before any cell.

**Subagent:** S7 (pairs), S10's minus clause (a matched removal of other non-canonical boss scripts also kills H), S11 (the pivotal scripts were all writable there, blocked by the lack rule; all 3 replays regrew), S12 (minus (c) 0.48 → 0.35 between 2,000 and 10,000), D1 (the producible half of (b) alone gives 0.10). **Dropped designs:** stratified random controls (overlap 0.97–1.00 with the component); per-program complement controls (0.21–0.56 of the volume); the literal lack rule under grants (a grant counted as held). **Process rule:** run long batches with one job per process; reused workers leaked memory across masks.


## Added 2026-10-17: annealed mutation (RESULTS.md, "Annealed mutation")

**The RS's "drift should never colonize an island, only reintroduce fit programs", as a statement about a finite cell.** Drift colonizations occur in every rain cell along the path (0.29 → 0.022 per island from N = 200 to 1,600; drift-free runs 0.10 → 0.875); it holds at K = 1, N = 800, where the detector cure is 0.20. Its "only fit programs" half is not a sufficient guard: a selected identity arrival converted a whole run. The RS's tail statement is inconclusive at N = 1,600. **"Cure ≥ 0.8 at every N" (Fable, RE 2):** fails for the detector class (0.33–0.40); the exposure K/(ρ·μ_pred) is class-specific. **RE 3's cure clause** (0.65 at 1,600). **"The schedule's shape matters for identity; drift equal within ±30%" (Fable, RE 5; fired).** **Gemini's first clause** (more secondary and identity takeovers under constant rain): no difference. **Sol's schedule dependence:** not supported.

**Subagent:** A1 (per-arrival drift assumed suppressed at high rate; it was 3–4× higher at N ≤ 400 and the slope steeper), A2, A3 at N ≤ 400, A4, A7, A9, A10. **Dropped designs:** natural-cell cure measurement (rivals too rare at I = 8; replaced by forced archipelagos); arm (iv) for the sponsored founder (not run); the original Λ₀ path (superseded; its cure is extrapolated at 0.17).


## Added 2026-10-17: an identity-resistant target (RESULTS.md, "An identity-resistant target")

**The RE's operating hypothesis after the 15-minute window, "narrow the target to identity-resistant members".** Not needed as a remedy: closing the prey channel (by removing exploitable members, with or without moving their mass to resistant ones) gains nothing by itself; R-move's gains are seed-level founder boosting. **"The control does not close the prey channel" (Fable, RE 5; contradicted).** Removing the exploitable members closes it under either prior; the control separates boosting from removal, not removal from channel closing. **"≥ 0.9 of resistant units are guarded" (Fable, RE 1).** 0.714: resistance is challenge-relative; the guard tests universal unexploitability. **Sol's "the combined bounds fail"** (R-move raises uot by +0.25 to +0.33 under rain). **Gemini's founder-boosting clause as scored at (200, 64)** (no gain there; it holds under rain).

**Subagent:** S5 (R-move +3 to +7 runs at (200, 64): 0), S6 (Rp within ±2 runs: sponsored −8), S7 (sponsored R-move 17–20: 9), S9 (≥ 0.2 takeover into every exploitable holder: 0.09–0.10 for two; exploitation is per holder and TwinD tree), S11 (R-move drift ≥ L: 0.28×), S13 (rain uot within ±0.15: +0.25 to +0.33); the hand claim that R-move gains at (200, 64) by founder boosting. **Dropped designs:** the natural-count reading of RE 4 and RE 5 (one event in 160 runs cannot rank priors); the single-spelling challenge assay (per-tree instead).


## Added 2026-10-18: legitimate detectors (RESULTS.md, "Legitimate detectors")

**The spec's premise that the certified-defection detector cooperates by default and is uncertifiable** (the RE's, on the RS's description). Failed statically: in the stored ecology its first D step writes a self-hypothesis defection certificate that validates at every root, so it is a near-identity clique; it is gentle only in the keyed world K. **"Vertical inheritance cuts establishment by at most half at N = 800" (Fable, RE 1 clause).** 0/300: a predator marks its victims faster than it grows. **"Equal mass is a coin flip by abundance" (Fable, RE 3; fired in the no-grudge arm).** 0/20 for detectors without grudges. **RE 4 and RE 5 cause clauses** (predation; abundance and prudence premium): predation is never confirmed by replays (0 of 84), and the prudence premium never heads a confirmed Part B removal. **Gemini's counter-predictions** (vertical ≥ 0.15 at 800; PrudentBot network ≥ 0.75 by prudence premium): failed. **Sol's coverage clause** (grudge protection varies with N): no establishment at any N tested.

**Subagent:** D5 (trivially), D6, D7, D9, D13 fired; D8 and D10 partly. **Dropped designs:** the cap-16 diagnostic (replaced by the prewritten bound); the horizontal cell at 20 runs (closed at 4 for cost); the "two rival networks" framing (in K detectors are a sub-family of the PrudentBot network). **Method:** the frozen 500-generation window labels inefficiency on every scramble-phase removal; cause labels need mechanism tests (replays, sucker surgery) before reuse. **RE process:** the RE's first draft miscounted detector extinctions by reading a counter that excludes removals before generation 10; the first audit caught the conflict.


## Added 2026-10-18: a per-root production rule (RESULTS.md, "A per-root production rule")

**"No overhead returns under the invariant mark: median encounter ≤ 1.5× play" (Fable, RE 5; fired).** 4.1× at 3·10⁶: root validation charges nested calls at every encounter, which the mark (a skip of NONE) cannot remove. **"R2 ≥ 0.4 at 3·10⁶" (Fable, RE 4's second clause; missed, falsifier not fired).** 0.30. **"The cap is cheap" (Fable, RE 3):** not scorable; the capped rule R3 thrashed in pilots (type churn 16–48× R2's) and was dropped. **Sol's "low median overhead" and "R2 well below H-full at 3·10⁶":** failed (4.1×; R2 0.30 against H-full 0.35). **Gemini's dispatch clause (≥ 0.4 only with root-keyed dispatch):** failed (dispatch 0.20). **Gemini's arrival-timing lag:** failed (concession bosses persist under R2). **RE 1 on the full 20–59 confirmation set:** inconclusive (R2 exceeds H-full by +0.127, outside the ±0.1 band upward).

**Subagent:** S3 (R1 ≤ 0.10: 0.20), S4 (R2 ≤ 0.30: 0.40), S7 (median ≤ 2.5×: 4.1×) fired; S9 (second-path scripts pivotal at most nuclei: 1/7 and 1/8) and S11's second clause (fair bosses extinct early under R1/R2) failed; S12's step-equality criterion (98.2% against 99%). The subagent's hand mechanism "the rescue acts at the nucleus encounter" is replaced by boss persistence. **Dropped designs:** R3 at k = 2 and 3, CLOCK-LRU and FIFO (thrash); the (200, 64) panel (cost); confirmation streams 40–59 for R1 and R0 + alternatives (cost); per-script replays beyond two nuclei. **Process lesson:** test any capped-list rule for type churn on a small slice before projecting its cost.


## Added 2026-10-18: identity-dependent results under world K (RESULTS.md, "Identity-dependent results under world K")

**The RE's description of world K to the RS ("a self-certified defection counts only against the opponent it was written about").** Operationally wrong in this grammar: the only hypothesis-closed D certificate is written against the literal DefectBot quote, which no program carries, so K switches self-certified defection off in play. The RS's provisional adoption stands on K's measured effects; the description is corrected in DEFERRED 1. **"Identity ≤ 0.005 per island in every K cell" (Fable, RE 1; fired in the S-self cells).** K does not touch C-script identity minted by self-play production (0.090, 0.032). **RE 2's "within 0.1" clause** (K exceeded L's proportional control by +0.15, n.s., at two cells). **"The provenance rule stops mattering under K" (Fable, RE 4; fired).** S-nonself − S-self is +0.25 to +0.50: minted cliques were not only a TwinD effect. **"μ_net rises and all-defect Pangaeas fall" (Fable, RE 5; premise failed, falsifier fired).** μ_net 0.0280 → 0.0277; 8 against 5 lost at 6,400. **Sol's "copy dependence remains under K":** not detected (slope +0.12, p = 0.33). **Gemini's mechanism (S-self turns the TwinD templates into self-defectors):** impossible in this convention (the D step is partner-free); its 6,400 Pangaea clause failed narrowly.

**Subagent:** W5, W6, W10, W13 (conversion by local establishment: holders are migrant-descended in every island class), W14, W15 (no exploitable rival to cure under K; rain created 7), W16. **Dropped design:** the rain cell's frozen stop (a run must not stop while arrivals continue; the first batch was set aside).


## Added 2026-10-18: hooks, Part W (RESULTS.md, "Hooks in the weakly extensional wing")

**"In the weak wing hooks keep efficiency and add commitment; behaviour fills are the most held" (Fable, RE 1; fired).** Universal-open fell 1.00 → 0.00 under maximal hooks, through inherited lineage contracts among default defectors; held fills are all history; behaviour fills die out. **"History fills protect gentle programs where partners recur" (Fable, RE 2), in the PD.** No gentle holders to protect (zero contrasts). **RE 4's execution clause** (worker threats untested, ≤ 10⁻²): history-keyed strikes execute at 0.06–0.08 of held fill-encounters. **"Fission–fusion keeps universality with maximal hooks" (Fable, RE 5; fired).** 0.05. **The RS's maximalism as a neutral default** (recorded as an expectation, not his claim): in the weak wing maximal scopes are not neutral; history scope plus pair contracts decides outcomes in both games.

**Subagent:** W2 (contracts make efficient lineage-closed cliques: efficiency 0.22, lineage-closed 0.18), W3 as scored on the declared leaky cell, W6 partly, W10 except its low maximal bound, W12's fair clause. **Dropped designs:** `ROLE`-keyed fills in the PD (would import a correlating device); fill costs (no runtime price in this wing); the ε→0 chain (write-induced types make the support unbounded); concessions' n = 11 boss grammar (replaced by behaviour-keyed fills); fission–fusion at 128 × 100 and the union game at N = 100 (cost; reduced to 32 × 100 and (30, 16)); horizon 2,000 for ablation cells. **Method:** relabelling copies as "copied" leaks a disabled source back in; source ablations need provenance-preserving copies.


## Added 2026-10-21: coalition-proof auctions (RESULTS.md, "Coalition-proof auctions")

**"Substitutes are a control: VCG is in the core, so truth is robust to every proper coalition" (RE 1; failed).** 0/3,000
robust: the winner and the runner-up on an item form a ring (the loser lowers its report at no cost), which the core does
not block. **"Spite deters at least 80% of the T-strict breaks" (RE 4; failed).** 0% of instances; spite deters same-side
coalitions (all of them under the surcharge) but never a mixed one, and under VCG the common report cap lets the pair
overbid out of reach. The strict-improvement reading of the response graph is not a model of spite (it equals T-strict).
**"Coalitional responders make first-price leader values exceed joint marginal contributions, so the notion's set is
mostly empty" (RE 5; failed).** Nonempty 1,000/1,000; leader values never exceed them. **"The one-round notion reproduces
the bidder-optimal core (Bernheim–Whinston)" (RE 6; failed).** 20.8% within one tick (every vector); the set contains the
zero-revenue ring profile on 88% of instances, and 0.6% of its vectors are in the true-value core. **"Police drive out a
co-founded pair on at least 70% of islands" (RE 11, second conjunct; failed).** 7.0% under matched mass: the policing seen
under the uniform prior is founder share. **The note's framing of the ring wall as the grand bidder coalition** (notes
§4): understated; any winner with a price-setting loser is a ring. **The note's first draft "VCG is robust to the winners'
coalition"** (corrected before the run, after gpt-6.1-sol's review: winners can jointly overbid to zero each other's
prices).


## Added 2026-10-21: hooks follow-ups in the weak wing (RESULTS.md, "Hooks follow-ups in the weak wing")

**"Open contracts carry the PD recovery; open history writes do not" (RE 2; falsifier fired).** The reverse: open
contracts with lineage writes 0.000, open writes with lineage contracts 0.975. **"Credible-response union contracts
reach the fair wage on at least 0.2 of islands with strikes ≤ 10⁻²" (RE 5; falsifier fired).** Fair 0.000 on a lineage
key; execution 0.125 at s = ½. **"Role-keyed (C) contracts at least 0.30 fair" (RE 7, role clause).** 0.20.
**Subagent:** A4 (contracts convert suckers into FairBot: wrong mechanism), A6 (open contract execution ≥ 5× lineage's:
3.2×), A5's survival clause, B3's mechanism clauses, B4's execution clause, B5 (`bw-only-C` flat against Part W: it
locks ¼ on every island), B7's (C) clause. **Dropped design:** the literal reading of "boss–worker contracts judged under
the same rule" (the boss's best reply to work is its lowest wage, so every positive-wage contract is rejected; not run).


## Added 2026-10-21: rediscovering the core (RESULTS.md, "Rediscovering the core")

**"The losing bid is a costless threat that drifts down" (RE, the spec's premise).** Wrong mechanism, by the
founding-payoff reading: the loser's honest high bids are selected out early, while it exploits the diverse founding
winners (best bid about 13 against a value of 20), and the winners then ratchet down. **"Efficient Nash revenues cover
the whole core and nothing below" (RE 1; partial).** The top two ticks drop out by tie deviations; in the collusion
instance one efficient equilibrium sits one tick below the core. **"The non-eroded islands sit inside the core,
spread over it" (RE 2; partial).** 6% / 10% in the core, the rest one tick below. **"An annealed tail of three
founders restores at least 60% of islands" (RE 4).** 2.4–4.5%. **"The responder restores the core at ε = 0" (RE 5),
and gemini-4-argon's counter-prediction.** 0.025 under the registered order; 0.71 under the reverse order;
order-dependent, not a program property. **"No preference for the Vickrey-nearest split" (RE 6).** Concentrated, and
the instances could not separate it from equal surplus or the middle of the edge. **"A single injected outbidder
restores the core" (RE 7; partial).** Establishes (0.86–0.94) and restores 0 of 9,744. **Engineer's skew guess (equal
surplus under migration).** 29 of 40 runs on Vickrey-nearest. **Dropped design:** order-dependent best-reply
responders as a model of mutual reading (cycles in 65% of two-responder triples).


## Added 2026-10-21: rediscovering the core, stage 2 (RESULTS.md, "Rediscovering the core, stage 2")

**"Certified threats and followers put 0.2–0.6 of islands in the core, with the threat shifted up at least 3 ticks"
(RE 2; partial, both headline clauses failed).** 0.082; shift +2.61. The freezing story held (prediction 3), but the
frozen level, about 13, is too low for the core. **"The sucker supply in rain restores the threat's honesty: at least 0.8
in the core, with safe-follower rain below 0.6" (RE 4).** Rain 0.117; the depleted controls lie within 0.05 of one
another and are not ordered as predicted. Dropped as stated. **gemini-4-argon's counter-prediction (follower-only rain
at least 0.6).** 0.086. **Default grammar:** followers that accommodate a certified threat are not a neutral item-role
default for core experiments; they spread when seeded in numbers and remove the threat's test.


## Added 2026-10-22: every behavioural predicate as a hook key (RESULTS.md, "Every behavioural predicate as a hook key")

**The spec's level-PA PrudentBot (RE).** At level PA, FairBot's vacuous world-0 cooperation poisons the DefectBot clause,
so the hand table's PrudentBot defects against FairBot. Replaced by a level-1 box, as in Barasz et al. **"FairBot- or
PrudentBot-equivalents through a fill are at least 50% of winners" (RE 3).** 0.003 (0.044 with unhooked FairBots); the
winners are generous provers. **"PrudentBot-equivalents outnumber FairBot-equivalents" (RE 5).** 0 against 1,876; the
prudent classes carry 10⁻⁴ of the prior. **"Verbatim copying carries the recovery" (RE 8, H1).** Copy-ancestry share 0.02;
inheritance is the main carrier in the legacy cells. **"Grudges leave DefectBot-like majorities on failed islands" (RE 9,
second clause).** 0 of 26. **"Conversion acts in the founding scramble" (RE 10).** Early writes alone 0.25 against 0.80
for late writes.


## Added 2026-10-22: rewarding prudence under world K (RESULTS.md, "Rewarding prudence under world K")

**"A light annealed tail after fission–fusion rewards prudence at A = 52" (RE 1; subagent S2, S3c).** The target network
and PrudentBot's own tree fell, and the prudent share did not rise in either world; standing suckers are 1–4% of the
population and guarded members earned slightly less in mixtures. Not re-opened without a heavier sucker supply and a
depleted control at the same exposure. **"The tail reduces off-target residence" (RE 2).** It rises (K p = 0.012, L
p = 0.003 by sign test). **"World K shrinks the premium per sucker encounter" (RE 3).** A tie on the primary measure
(0.6855 in both). **gemini-4-argon: "repeated identity arrivals break L at A = 156".** 40 of 40 universal. **Subagent
S4, S6, S9 and S7's timing clause.** Universality stays 1.00 at A156, growth is mostly resident-descended, and 0.917 of
arrivals land by t = 5,000. **Dropped design:** the SD52 arm as a clean sucker removal; it removes only the unconditional
cooperators.


## Added 2026-10-23: hooks in the realizable language, Part R (RESULTS.md, "Hooks in the realizable language (Part R)")

All at shortened horizons (2,000 for B, I, M; 1,000 for ablations). **"Source-keyed fills bring identity back in Part R"
(RE 3).** Strict identity 0 in the audited M runs under S-nonself; the universality deficit (−0.40) is real but
implicated in history writes and rivals, not identity. **"The loss is located in the root and behaviour scopes" (R6).**
Those inert recover 22% and 33% of the gap; history writes recover more than all of it. **"History decides little at
natural seeds" (R7) and "history fills protect gentle programs" (RE 2).** Removing the writes raises universal-open
2 → 14 of 20 and the PrudentBot share 0.62 → 0.80; the sign is the opposite of RE 2. **"Other fill sources add
commitments, not losses" (R12).** −0.65 against seeding only. **"Islands stay efficient at ≥ 0.98 with hooks" (R9).**
Five cells below 0.95 at 1,000; four are unfinished scrambles, the clone cell's loss persists. **"Grammar dilution
within ±0.2" (R3).** −0.35. Open, not rejected: whether thanks fills or contracts mint the clone cell's cliques.


## Added 2026-10-23: rock–paper–scissors and mixed actions (RESULTS.md, "Rock–paper–scissors and mixed actions")

**"Exact readers select for individual mixing" (RE 5).** At N = 10⁴ the exact arm's chain has e 0.432 and mixing 0.307;
0.25 of lottery islands are unexploitable; exact − matched exploitability is positive (+0.139 chain; +0.106 registered
lottery, +0.146 post-hoc replicate); mixing differences unresolved. Not re-opened without a game where a reader can
beat `X` on something other than the zero-sum value. **"Sample is more exploitable than exact, approaching more
slowly" (RE 4).** The reverse at every N from 10² to 10⁷. **The RS's statement in the scored reading** (unexploitable
individual mixers at N = 10⁴): failed in both objects; approached in the chain near N ≈ 10⁷. **gpt-6.1-sol's
counter-prediction** (substantial mixing in both stochastic arms at 10⁴): 0.31. **The RE's premise that the chain would
meet polymorphic or three-type-cycle states.** In a symmetric zero-sum game every two-type contest is dominance or
neutral; every state is monomorphic. **The run report's limit formula π_∞(c) = μ(c)/μ(Z0)** (subagent): it contradicts
the exact identity π(`X`) = μ(`X`) at every N.


## Added 2026-10-23: rock–paper–scissors with a compute price (RESULTS.md, "Rock–paper–scissors with a compute price")

**"Pricing makes the chain converge fast" (RE 3, speed clause).** By N = 10³ the chain is about 0.5 from its N = 10⁵
values; the binding rate is the neutral entry of free constants, not the forfeit. The level clause also missed (net
e 0.135 / 0.151 at N = 10⁴, not ≤ 0.1). **"c = 0.05 is at least as mixed as c = 0.01" (RE 4b).** 0.84 / 0.76 against
0.93 / 0.85: the higher price removes the guarded readers. **"Pure-arm individual exploitability stays ≥ 0.3 at every
c" (RE 5).** Net −0.04 at c = 0.05, since every exploiter pays the cap. **gemini-4-argon: guarded readers beat `X` at
c = 0.01.** 0.055 / 0.014 against 0.87 / 0.84. **The RS's reading (I) at c = 0.001.** Not met (lottery e 0.18 / 0.42).
**Spec claim that the hand table shows depth and work differing at n = 6.** It needs n ≥ 7. **The unpriced identity
π(`X`) = μ(`X`) carried over to a priced game.** It holds only at c = 0; with a price π(`X`) rises with N.


## Added 2026-10-24: mixed actions in two-role games (RESULTS.md, "Mixed actions in two-role games")

**"Reading inspectees sustain commitment" (RE 2).** In the primary exact cell inspectee readers are 0.19 of inspectees,
inspector mass at 3/8 is below 1/2, and the price does not lower the payoff at generation 2,000; the modal island is
the efficient outcome held by a responsive inspector. Commitment dominates only when the inspector cannot read. Not
re-opened without a reason the inspector should be unable to read. **gemini-4-argon on 2** (payoff below −0.5 at
c = 0.01): −0.21. **gpt-6.1-sol and gemini-4-argon on 4** (gap below 0.2, or near 0): 0.34. **"II's exact readers do
not beat the coin in Basic Endgame" (RE 6).** They hold 0.54 of II. **"The hand table matches" (RE 1).** One entry
was wrong (EXP against the reader columns); the evaluator caught it. **The registered chain criterion for
indeterminacy** (π on cycle classes ≥ 0.5): trivially met in every arm. **Exploration-capped chains as π in grammars
with large neutral networks:** −0.009 capped against −0.47 on the whole space.


## Added 2026-10-24: a private random tape in the realizable language (RESULTS.md, "A private random tape in the realizable language")

**"At the calibrated step price the tape coin holds the RPS lottery" (RE 2).** `U` 0.045 at c₀ = 0.12/K₀; simulators
0.87, because a timed-out read returns a default, not a forfeit. The coin held 0.91 at c = 10⁻³ (post-hoc). Not
re-opened without a price of that order or a timeout convention that forfeits. **gpt-6.1-sol: a quote-hash population
is balanced in aggregate.** Population exploitability 0.89. **"The responsive prover holds the efficient inspection
islands in L_T" (RE 3, mechanism).** `RI` holds 0; simulators hold all of them; `RIM` holds them only without
simulators. **The hand table's "a simulator earns half the best response against every biased mixer."** True for 3 of
6. **"The calibrated price leaves efficiency within 0.1" (S4).** −0.128, uncertain. **A check-only reader survives.**
Share 0. **A single timeout default for simulators.** A grammar artefact found in development.


## Added 2026-10-24: the inspection game's enforcer and its shadow (RESULTS.md, "The inspection game's enforcer and its shadow")

**"The binding exit of the efficient inspector state in the chain is the unconditional shadow" (RE 1, and the RE's
reading in RESULTS "Mixed actions in two-role games").** The shadow is the largest exit from R only at N ≤ 10³; at
N ≥ 10⁴ light cheaters and bounded-read exploiters (0.3% of the prior) bind, and removing the shadow alone changes
nothing. **"Efficient islands fall along the lottery size path" (RE 3).** 0.80 at (800, 8). **"Cheater rain prunes the
shadow" (RE 4).** −0.05 at c = 0. **"A ×10 prudent-inspectee prior raises chain P(E) by 0.1" (RE 5).** +0.013. **The
counter-predictions that P(E) rises with N** (gemini-4-argon, gpt-6.1-sol on 2). It falls (odds slope −0.51). **The
engineer's estimate that E \ R holds about 2.5/N.** 0.064 at N = 10³.


## Added 2026-10-25: a migration window for stable sets on islands (RESULTS.md, "A migration window for stable sets on islands")

**"An unguarded migration window exists and widens as mN falls" (RE 1, 2).** The best baseline share is 0.225 at
10,000 (0.375 at 20,000); clearance and consolidation both slow as mN falls. **"The window narrows with N" (RE 3).**
Reversed: 0.70 at N = 200. **"Small components beat large ones by preserving founding diversity" (RE 6c).** Reversed:
small components settle on unequal pairs more often. **"Components meet the independent-draw reference" (RE 6a).**
Below it at N = 100, mN = 1. **gemini-4-argon's mechanism that coverage is lost by unequal pairs invading fair
pairs.** Member-to-member transitions dominate. **The expectation that the veto meets the V\* target at every mN.**
0.85 at N = 100, mN = 1.


## Added 2026-10-25: deriving immigrant rejection, Step 0 (RESULTS.md, "Deriving immigrant rejection for stable sets on islands, Step 0")

**"The veto keeps coverage by making mismatched immigrants lose; no contracts exist between members" (RE 1).** Under the
veto every contract on a member island is fair-to-fair, islands rotate members 20–59× as often as the baseline, and the
exemption of those contracts carries the coverage. **Loyalty, status-quo tie-breaking and conformity as the route to
the RS's target.** Set aside, not tested: they lock islands and the veto does not; immigrant fiat and pivot freezes,
the benchmarks for locking, reach the V\* target only at mN = 1. **The reading that "locked islands reject
immigrants"** (RESULTS "Dominance contracts and refusal on islands"; the explainer "Stable Sets on Islands").
- **Zero tolerance alone lifts the inspection chain's π(E) to ≥ 0.1 at N = 10⁵ (RE, 2026-10-24, prediction 1).** Partial: +0.041 (0.088), light-cheater hazard cut 2.5×, not 10×; the bounded-read exit stays (RESULTS "Zero-tolerance, suspicious and sampling inspectors").
- **The suspicious default alone helps; the closures of the two exits are properties of the programs (engineer, notes §1).** SUS gains −0.010 at D = 12 and about 0 at D = 11 and 13; ZT+SUS's +0.487 at D = 12 is +0.001 at D = 11 and +0.022 at D = 13, so the closure is a coincidence of the depth cap's phase. Same section.
- **Counter-predictions 1c (gemini-4-argon: the bounded-read exit absorbs ZT's flow), 2c (gpt-6.1-sol: ZT+SUS stays below 0.5) and 3c (gpt-6.1-sol: SR16's gain fails through the q grid).** Failed as scored at D = 12 (largest exit still light cheaters; 0.534; gain +0.335 with the channel empty). Same section.
- **Engineer's E1, E2, E3, E5 (zero-tolerance run).** Aggregate bounded-read hazard cut ≥ 10× (1.4×; 3.5× and 22×), SUS's D = 11 gain 0.2 below its D = 12 gain (both about 0), light-cheater occupancy 3× below the control (1.2×), SR1 within 0.03 of the control (+0.044 at N = 10⁴). Same section.
- **The unconditional inspector separates detection from commitment.** It is dominated and gains nothing at this mass (−0.001); commitment in general is not tested. Same section.
- **The n = 10 `dollar3` grammar contains two-partner readers (spec premise, churn in the primary object).** False: the reader needs size 11 (mass 7·10⁻⁸ at n = 11); churn-capable classes are about 0.1% of a slot at n = 10 (RESULTS "Churn among the fair pairs in the primary object").
- **Engineer's E2, E3, E5 (no reader cell above 6× the baseline's flips).** Failed: 2.8–21×. Same section.
- **gemini-4-argon's counter-prediction that churn in arm T needs two-partner weight ≥ 0.05.** Failed by its rule (T-hi 7.0 / 4.3 against T-lo 5.9 / 4.0); single-partner switchers carry the churn. Same section.
- **Single immigrants as the measure of island switching.** Dropped: a mismatched immigrant dies in about 10 generations (switching 0.07–0.1%); the balanced start with resident readers is the better probe. Same section.
- **Readers' churn keeps all three fair pairs present (the hope behind the RS's test).** Not seen: coverage 0.00 in every cell at mN = 1. Same section.
- **The published one-population modal chicken / hawk–dove chain as converged at `max_states` 3,000 (`fixed_role_chicken.onepop_chain`, six of nine cells at the cap).**
  Dropped: with the cap raised to 12,000 states hd3 at N = 10^4 gives payoff per player 0.183 (not 0.016; no candidates left) and hd3 at N = 10^3
  gives 0.906 (not 0.234; 15 candidates still left). Evidence: `runs/exploration_audit/chk_modal_hd3_N{1000,10000}.json`, addendum A1.
  What survives: the fixed-role results and every lottery figure of the section; "one population cannot learn the norm" at hd3 N = 10^4 and chicken.
- **Reading a small `cut_flow` / relative cut as a convergence certificate for a capped or θ-pruned chain.** Dropped (extends the 2026-10-05 entry
  on θ-pruned exploration): the capped mixed2 exact cell had unexplored relative flux 0.999 (1,500 states) and moved by 0.46 payoff units (0.115 of the range)
  on enlargement; the hd3 N = 10^4 cell had a cut of 10^-14.7 at its cap and moved by 0.17 payoff units (0.067 of its range). The convergence flag of this audit is
  the number of candidates still above θ at the cap (`n_cand_left` / frontier mass), not the cut. Recommended solver default: raise an error or print UNCONVERGED
  when `n_cand_left` > 0 at exit; no existing file edited here.
- **The graded ordering exact > sr16 > sr4 > matched of the mixed2 chain (capped cells; sr_k at c = 0, Endgame matched at c = 0.01).** Dropped as a chain
  statement: sr16 N = 10^4 gives -2.456 at 1,500 states (outside the game's payoff range) and -0.361 at 15,000 (still capped); sr4 -0.764 → -0.352;
  Endgame matched -0.2019 → -0.2006. The lottery ordering is untouched.
- **Engineer predictions E2 and E3 of this audit** (that the cells to move would be the monomorphic-restricted cap-limited multi-role cells, and that no other
  M-status cell would move by more than 0.02 outside a known deep trap): wrong; the mover was an M-status one-population cell whose cap limits the polymorphic
  search (addendum A1). The registered counter-prediction of gemini-4-argon (shifts above 0.05 in enforcement, concessions, gene arm, auctions, RPS) was
  not supported on the cells reached.
- **Re-solving the union game, enforcement CC and the three-player dollar by lowering θ by four or more decades with this solver.** Dropped as infeasible,
  not as wrong: union N = 10^4 at θ = 10^-11 spent 81 min in round 1 (42,007 ring states, relative cut 0.175); the three-player weak N = 100 at θ = 10^-10 took
  4 h 45 min and 8 GB for a 3.7-fold cut reduction. A converged answer there needs a different solver, not a smaller θ.
- **Failure pricing makes the bare coin win RPS (pricing rules, prediction 3).** Failed: at P_fail ≥ 0.1 simulators vanish but the coin holds 0.084 of the lottery; the islands go to the guarded mixer `PRR` (0.911) and, at P_fail = 1, the prover `PB` (RESULTS "What compute should cost").
- **Amortized pricing helps the PD and hurts the coin pointwise (prediction 4).** Failed: the B − F difference in the coin's share changes sign across c. Same section.
- **The per-program memo sits between per-step and shared-cache pricing (prediction 6, the RS's B-own arm).** Failed: it is near B in RPS and inspection at the panel levels and above both in the PD at 10⁻⁴ and 10⁻³. gemini-4-argon's counter-prediction (cold memos kill establishment) also failed. Same section.
- **The PD under per-step pricing fails by arithmetic, monotonically (engineer E2), and warm and cold caches agree (E5).** Failed: 9, 0, 12, 20 of 20 from 10⁻⁵ to 10⁻²; RPS differs by 0.114 between warm and cold at 10⁻⁴. Same section.
- **The registered PD target (universal-open runs) as a score for priced arms.** Dropped for priced comparisons: it is cost-blind (per-step 10⁻² is "met" 20/20 while each play costs about 31 stakes and P(C,C) is 0.586). Same section.
- **The outcome-class ODE as the I → ∞ limit of the rare-migration chain (many islands).** Dropped: the class chain is not Markov (per-recipient exit hazards vary with CV 1.5–2.3), and the ODE gives V* 0.64 where the chain gives 0.998 (RESULTS "Islands to infinity before time"). The partial re-opening of "The migration game as the island model's ε-free object" stands only for the dynamics on program triples, not for class-level games.
- **Neutral (voter) scaling of the first loss of a fair pair, ∝ I.** Falsified: slope 0.27 [0.21, 0.34] in I (L A = 0). Same section.
- **α > 0 (third-pair moves) suffices for a unique interior attractor with all three fair pairs (RE, 2026-10-25).** Not sufficient: α/κ 0.09–0.13 > 0, yet any asymmetry breaks the symmetric state and an unequal basin competes. Same section.
- **RE predictions 1, 3, 5, 6, 7 and engineer E2, E4, E6, E10, E13 (many islands)**, and gemini-4-argon's counter on 5 and gpt-6.1-sol's 7c as registered. Same section.
- **Single-migrant conversion as the efficiency bottleneck (unequal islands nearly absorbing).** Wrong in the limit: unequal islands convert slowly but steadily; V* 0.96 by 10⁴ events per island in L A = 0. Same section.
- **RPS fails under failure pricing at P_fail = 0.03 (confirmation, prediction 3a).** Failed: by-mixing met, `PRR` modal on 0.90 of islands (RESULTS "Confirming failure pricing").
- **gpt-6.1-sol's counters: inspection at (100, 64) undetermined; the scramble's charges change which PD network establishes.** Failed: net efficient 0.825 [0.704, 0.929]; paired differences all include 0. Same section.
- **Engineer E5, E6, E9 (confirmation).** Failed (PRR share at 0.03 is 0.90; the stakes-normalized inspection point undetermined; the headline confirmed, not unresolved). Same section.
- **Encounter contracts with a signers-only Pareto test as the repair for the fair pairs (RS, 2026-10-25).** Dropped as a repair: V* about 0.40 against 0.47 with no contracts at 1,000 events (ν = 1), 0.325 at ν = 0.1; observed island occupancy 0.40 fair / 0.60 unequal at both rates; no fair island contract-stable (exhaustive oracle). It stays as a near-efficiency mechanism (RESULTS "Contracts that form in encounters").
- **RE predictions 2, 1 at ν = 1, and engineer E7, E8 (at ν = 1), E13 (encounter contracts).** Wrong as registered; the signers-only test's rotating walk was in the hand examples but its dynamical consequence was not drawn. Same section.
- **Arm H (contracts only into exposed hooks) as a restriction that helps.** It lowers fair occupancy (0.287) and leaves dominated islands (W + D 0.04–0.075). Same section.
- **Arm S at ν = 1 (the Pareto clause as selection, one random install per generation).** No island holds a class. Same section.
- **Failure pricing with free forfeits (A) as the default compute charge.** Superseded: a free forfeit is an exit that provers and exact simulators take (at P_fail 1 and 10 `PB` modal on 0.58 and 0.70 of RPS islands, forfeits 0.49 and 0.62); charging the forfeit (A_f) closes it (RESULTS "Charging forfeits like failed reads").
- **The security-strategy fallback (A_m) as the forfeit rule (the RS's alternative).** Not adopted as the default: at P_fail 0.03–0.1 provers forfeit into the referee's coin (fallback 0.10–0.21 of plays, by mixing failed or undetermined) and the free coin takes the middle of the band (modal 0.64–0.83 at 0.1–0.3); from 1 up it matches A_f on RPS status. Same section.
- **RE predictions 4 (at 0.03), 9 and 10, and engineer E2, E5–E9, E11, E12 (forfeit pricing).** Wrong as registered. Same section.
- **Encounter contracts with a readers seed law, as a route to the stable set (RE proposal, 2026-10-28; dropped before a spec).** The RS (2026-10-29): readers supply "how my opponents will respond", which the genesis test already accounts for, so "this won't help". Confirmed by the game's rule (`src/dollar3.py` `outcome`): a pair forms when two slots name each other, whatever the third plays, so the deal that drives the walk (a pair member and the excluded slot, both carriers with fixed fills) cannot be blocked by any answer of the lone responder. Readers can only change singleton moves; the missing foresight is about the next contract, which is the farsighted clause the RS excluded (RESULTS "Contracts that form in encounters"; DEFERRED 15).
- **Farsighted clauses as a route to the stable set (consent guards such as Konishi–Ray, look-ahead genesis tests).** The RS (2026-10-29): "a band-aid antithetical to the rest of the program". Kept only as the reference result of RESULTS "Farsighted refusal"; not part of the object (DEFERRED 15).
- **"Constants alone are bistable in the mean field" (RE prediction 3, many islands in arm T, 2026-10-29).** Failed: at dose 0 (the nine constants only) the exact ODE reaches V\* = 1 from the natural law and every tilt, the unequal tilt included, at P_fail 0 and 0.1. The unequal basin of the DSL arms L and M is not a property of constants (the RE's hypothesis: the length prior's conditional programs). Finite worlds of constants still end unequal in about 40% of runs at I ≤ 4,096, a finite-I effect. RESULTS "Arm T under islands to infinity before time".
- **gemini-4-argon's counter-prediction (readers repel each other under A_f, V\* < 0.9 from the unequal tilt).** Failed: V\* = 1 at P_fail 0.1 from every start and pool; the charge halves the readers' share of the limit and slows conversion by about 0.015 of V\* at 10³ events. Same section.
- **RE prediction 6 as registered (removing the switchers lowers the V\* limit more than removing the two-partner readers).** Partial: no ablation moves the limit; the ordering holds only at finite time. Same section.
