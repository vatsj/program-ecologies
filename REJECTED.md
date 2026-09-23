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
