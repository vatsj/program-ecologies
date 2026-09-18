# Program Ecologies: Stochastic Stability in Open-Source Games

Operating hypothesis for how the model works. Rejected alternatives live in REJECTED.md. Update this file, not the conversation, when the model changes.

---

## 1. The object

**Base game.** A finite symmetric game $G$, or an asymmetric game symmetrized by `ROLE` (§3). Currently 2-player; $k$-player is a stated goal (§9).

**Strategies.** Programs in a weakly extensional language $\mathcal{L}$ (§2): a program may condition on the opponent's behavior — what the opponent plays against anyone — but never on the opponent's source text. A program applied to an opponent yields a (possibly random) action. $u(p,q)$ is the expected base-game payoff.

**Payoffs.** Computed exactly. Runtime budget $T \to \infty$: terminating pairs get exact payoffs; divergent pairs receive the minimax action. Runtime is not a selection pressure. Finite $T$ with the $\kappa t/T$ override is a computational device only; extrapolate.

**Prior.** $\mu(p) = 2^{-|p|}$, with $|p|$ in **bits under an optimal code for $\mathcal{L}$**. Exponent fixed at 1 — the weakest simplicity assumption that yields a proper universal prior. Not a knob. Always use bits: $2^{-(\text{node count})}$ is improper for this grammar (growth ~5.66×/node needs ≥2.5 bits/node). The optimal code sits at exactly the critical exponent plus a $\sim 2\log_2 L$ length prefix, so the tail of $\mu$ is polynomial ($\sim 1/(L\log^2 L)$); roughly half the mutation mass lies beyond 7 nodes (§7).

## 2. Extensionality

Three levels of opponent access, one semantics (every arm evaluates programs by the same grounded iteration), one of them canonical.

**Weak extensionality — canonical.** Oracle access to the opponent's behavior: a program may condition on what the opponent plays against anyone, including third parties and itself. In the DSL: `THEM(P)` for any program-sort $P$. Behavior depends on the opponent's input-output function, never on source. $\pi$ is defined on this language.

**Strong extensionality — baseline arm.** Condition only on what the opponent plays *against you*. In the DSL: `THEM(ME)` is the sole opponent-referencing form; the program is effectively a function $A \to A$. This is the response-function framework the project started with. It is kept as a formal arm, not a parable, because (1) it is the minimal hypothesis for the deterrence half of the efficiency argument, (2) its failure is the empirical argument that weak is canonical and that argument needs a run, and (3) its program space is dozens, so it is exhaustively provable by hand.

**Source access — contrast arm.** Adds syntactic `eq`. Behavior is no longer a small object, equivalence is no longer a congruence, and `eq(THEM, ME)` is a 3-node self-recognizing clique (short, strict Nash, exploits ALLC). Only a computational certificate is available here, never a characterization.

**What weak extensionality buys.** (1) *Behavior against fixed incumbents is a small object* — a distribution over base-game actions per probe — so "what can an invader do" is finitely enumerable and the behavioral characterization (§7) is a proof. (2) *Behavioral equivalence is a congruence*, so dedup is sound. (3) *No syntactic cliques.* (4) *Unfakeable handshakes* (§3): passing "do you play $a^*$ against $a^*$-players" requires playing $a^*$.

**Strong vs weak: three jobs, weak does all of them.** *Deterrence* needs only on-path conditioning (strong suffices). *Invasion of inefficient outcomes* (the handshake, §3) needs a channel separate from the on-path action; third-party probes provide one; under strong access the handshake shares the grounding anchor with the on-path action and either collapses to the incumbent action or pays a tax. *Drift stability* (distinguishing reciprocators from unconditional cooperators) needs a third-party probe. So strong deters but neither invades cleanly nor stabilizes; weak does all three.

**Strong extensionality as a recombination model.** Under strong access, behavior toward incumbents (observed) and toward outsiders (unobserved) are separable loci — the architecture greenbeard theory needs. The unobserved locus drifts and produces falsebeard-like variants (ALLC) without crossover. Two-step destabilization where biology's is one-step; bears on the strong arm only; `eq`-cliques have no free locus.

**Why global extensionality is inconsistent and the fragments aren't.** All extensional functions would give $B \cong (B \to A)$, ruled out by Cantor; the computational shadow is Rice. The DSL is a *fragment* — extensional primitives without closure — and finite at each truncation.

## 3. The efficiency theorem

**Statement (target).** *In a symmetric game under weak extensionality, every stable ecology is Pareto efficient in the correlated feasible set. In a `ROLE`-symmetrized asymmetric game, it maximizes the unweighted utilitarian sum.*

**Deterrence is not the route.** In a general game, $a^*$ is deterrable iff $u(a^*,a^*) \ge \max_a\min_b u(a,b)$ — individual rationality, the folk theorem. Every IR outcome, efficient or not, is supportable by a harsh enough punisher. This holds in separable games too: grim-with-the-harshest-action ($\arg\min g$, which need not equal $a^d$) supports inefficient outcomes. Efficiency comes from two selection arguments, not from deterrence.

**Engine 1 — harsh punishers lose.** A harsh punisher pays $f(a^d) - f(a^{\text{worst}})$ per punishment; a mild punisher earns strictly more against the same defector and is neutral on-path. When defectors are present — and the drift leak guarantees they periodically are — mild outcompetes harsh by drift-then-invasion. Selection favors the *mildest deterring response*, which is matching, which supports only efficient outcomes (§4). This is the credibility criterion the early project sought by axiom, delivered by the population: non-credible threats are outcompeted, not forbidden.

**Engine 2 — the secret handshake, unfakeable.** Robson (1990): in a symmetric game with a costless signal, any diagonal-dominated symmetric outcome is invaded by a mutant that signals, plays $a^*$ with fellow signalers, and mimics incumbents otherwise — neutral against incumbents, strictly better against itself, so it drifts in and wins. Robson's defect is that fakers (signal, then defect) invade once handshakers dominate. In a program game the handshake is behavioral and cannot be faked. Consistent with Tennenholtz's folk theorem: Nash-of-programs checks one deviant against a fixed profile, where a lone handshaker is merely neutral; the population catches what Nash doesn't — the standard ESS-vs-Nash gap.

**Proof outline.** (1) *Invasion:* any diagonal-dominated symmetric outcome is invaded by a probe-based handshake mutant (Robson; needs weak). (2) *Fakers fail:* behavioral handshakes are unfakeable. (3) *Drift stability:* the ALLC leak is plugged by a second probe — PrudentBot — needs weak. (4) *Termination:* each invasion strictly raises the diagonal payoff; finitely many actions; ends at a diagonal maximum (compactness for continuous games). (5) *Efficiency:* with `ROLE`, the diagonal of the symmetrized game ranges over symmetric correlated outcomes and its maximum is Pareto efficient in the convex hull.

**The weights.** `ROLE` makes every program play both roles equally often, so a monomorphic ecology's fitness is $\frac12[u_1(a,b) + u_2(a,b)]$ and the stable outcome maximizes the unweighted utilitarian sum. This is not an interpersonal comparison; it is *intrapersonal across roles* — the same program behind a veil of ignorance about which side it will occupy. Harsanyi's impartial observer (1953, 1955). $\lambda = (1,1)$ is derived.

**Fixed roles.** Two populations that never swap roles still reach the frontier (Engine 2 applies to any Pareto-dominated outcome), but the point on it is selected by the dynamics rather than by symmetry. Prediction (Young 1993): Nash bargaining relative to the endogenous threat point — where only threats that persist as stable programs count. The framework distinguishes drawn roles (impartiality) from assigned roles (power) by a modeling choice with a clear normative reading.

**What is not yet in hand.** The handshake mutant is 7–9 nodes: reachable under $\mu$ but rare, so time-to-efficiency may be long. Step (3)'s regress — which self-referential reciprocator the chain selects — is open (§9). Fixed-role weights need the demand-game result run, not cited.

## 4. Separable games — the illustrative class

Separability is no longer the theorem's hypothesis; it is where the structure is cleanest.

**Definition.** $u(a_i, a_j) = f(a_i) + g(a_j)$. Dominant $a^d = \arg\max f$; efficient $a^* = \arg\max(f+g)$. The PD in use: defecting gives self $+1$, other $-2$.

**Utilitarian coefficient.** In a separable game, "weight the opponent's payoff by $\lambda$" is a well-defined action $a(\lambda) = \arg\max_a[f(a) + \lambda g(a)]$, with $a(0) = a^d$ and $a(1) = a^*$. In a general game the analogous object depends on $a_j$ and cannot be separated from strategic interaction. A scalar $\lambda$ per behavior is meaningful only here. Asymmetric case: maximizing $\lambda_1 u_1 + \lambda_2 u_2$ decouples, and each player's action is set by the ratio $\lambda_{-i}/\lambda_i$.

**Matching supports only efficient outcomes.** A reciprocator with $\rho(a^*) = a^*$ and $g(\rho(a)) \le g(a)$ deters all invaders iff $a^*$ is efficient: an invader playing $a$ earns $f(a) + g(\rho(a)) \le f(a) + g(a) \le f(a^*) + g(a^*)$, the last step being efficiency. Grim-with-$a^d$ is the stingiest such $\rho$; matching $\rho(a) = a$ is the most generous. This is the *matching* half of Engine 1 in closed form. It is **not** a claim that all stable ecologies are efficient — harsher punishers support more (§3).

**Matching over grim.** Same deterrence; matching earns 5-for-5 from partial cooperators where grim earns 0-for-0, and is noise-robust. With $\varepsilon$-grounding anchored at $a^*$, mutual matching converges to $a^*$. In continuous games pure matching against a slightly stingy partner (returns 0.9 of what it receives) collapses to zero; generous matching $\rho(a) = a + \delta$ stabilizes at $9\delta$ (Roberts & Sherratt; Killingback & Doebeli). No natural grim threshold in continuous games; matching is canonical because it is the identity.

**Matching rate as price.** In an exchange game, matching at rate $k$ is an exchange rate. Any complete trade is efficient; the rate is distributional. So the rate is the $\lambda$-ratio, the stable rate is the bargaining outcome, and the First Welfare Theorem analogy is literal: the ecology's response function plays the role of prices.

**Assortment and Hamilton's rule.** From the Price equation with $w = w_0 - c\,z_{\text{self}} + b\,z_{\text{partner}}$: cooperation increases iff $rb > c$, where $r = \text{Cov}(z_{\text{partner}}, z_{\text{self}})/\text{Var}(z_{\text{self}})$ is assortment — a statistic, not a genetic quantity (Fletcher & Doebeli 2009). Source observation is a fourth assortment mechanism after kinship, space, and tags. For a FairBot/ALLD mix, $r = 1$; with $b=2, c=1$ Hamilton's rule reproduces FairBot's weak dominance over ALLD. $r$ is endogenous to the language's recognition power.

**Greenbeards are cliques.** Biology's greenbeards fall to falsebeards because tag and behavior sit at separate loci (Gardner & West 2010). Under syntactic `eq` the tag is the whole program — no separate locus — so `eq`-cliques are unfalsifiable greenbeards and strict Nash where biological ones aren't.

## 5. The dynamics

**Population.** $N$ agents, each holding a program.

**Selection.** Fitness-proportional reproduction against the population mix (Moran). Fitness is mean-field: $F(p; s) = \frac{1}{N-1}\sum_{j\ne i} u(p, q_j)$.

**Mutation.** At rate $\varepsilon$, an agent's program is replaced by a fresh draw from $\mu$.

**Regime.** Intermediate: $\varepsilon$ small enough that at most one mutant lineage is alive at a time (mutants win or lose on fitness; coalitions are structurally impossible), but not so small that drift out of polymorphic attractors dominates. The strict $\varepsilon\to 0$ limit at fixed $N$ forces monomorphism only for $\varepsilon \ll e^{-cN}$, which is unphysical.

**Attractors.** The rest points of selection: configurations where every present type has equal fitness ("cool" states). Includes monomorphic states, stable polymorphisms, and neutral sets (e.g. the FairBot–ALLC edge, all at payoff 0).

**Attractor chain.** A single mutant $q\sim\mu$ perturbs attractor $A$; selection carries the population to attractor $B$ (possibly $A$, a different rest point, or a new coexistence including $q$). Transitions require $q\in B$: a mutant that dies returns the population to $A$. $P(A\to B) \propto \sum_q \mu(q)\Pr[\text{selection from } A{+}q \text{ settles at } B]$. Attractors are discovered by reachability from the monomorphic seeds.

**The ecology.** $\pi$, the stationary distribution of the attractor chain: the fraction of time the population spends in each stable configuration. $\pi$ is $\varepsilon$-independent within the regime.

**Indeterminacy rule.** If selection from some perturbed state does not converge to a rest point (a genuine limit cycle — rock-paper-scissors under replicator), the chain's premise fails and the result is reported as **indeterminate, citing the cycle**. Bistable switching — two rest points with mutation-driven transitions between them, such as the FairBot–ALLC edge and the all-ALLD sink — is *not* a cycle: selection converges every time, $\pi$ is well-defined, and the model predicts time-shares.

**Reporting.** Always report the **support and transition structure** of $\pi$ alongside its weights — which rest points, which single mutants move between them. A $\pi$ spread over qualitatively different states is where weights alone mislead ("60/40" reads as a mixture that never occurs), and the transition structure is where the mechanism lives.

## 6. The canonical object

$\pi$ is defined on the full weakly extensional language. $\mu$ is summable and the convergence bound (§7) makes the countable chain well-defined. The canonical ecology is $\Sigma = \lim_{N\to\infty}\pi_N$.

**One limit, $N$.** Truncation $n$ is a computational device (§7), $\beta$ is fixed at 1, $T$ is infinite, $\varepsilon$ is in regime.

**Why the limit of finite-$N$ chains.** $\mu(q)$ is a first-order weight on every transition at every $N$, so length is always charged. What $N$ controls is which transitions have positive probability: at finite $N$ a mutant that loses on-path can fix by drift ($\sim e^{-cN}$); at $N=\infty$ it cannot. Whether $\lim_N\pi_N$ equals the $N{=}\infty$ chain is open (§9).

**Priority structure.** On-path fitness is lexicographically first in that it *defines the state space*: attractors are rest points of selection. Length and off-path fitness then jointly weight transitions — $\mu(q)$ times the tipping probability — as a product.

**Language dependence.** $\mathcal{L}$ enters only through the Kolmogorov constant: vanishes for universal $\mathcal{L}$, small for a DSL fitted to the game.

## 7. Proof and computation

**Truncation and convergence.** Let $\pi_n$ be the chain on programs of length $\le n$. $\|\pi_n - \pi\|_1 \le \kappa_n r_n$ where $r_n = \sum_{|q|>n}\mu(q)$ and $\kappa_n$ is a condition number of the truncated chain (standard stationary-distribution perturbation bound). The support of $\pi$ is infinite — a long program behaviorally equivalent to a short fit one persists neutrally with tiny mass — so "ecologies have a maximum length" is false; what stabilizes is any fixed-precision approximation, in particular the mode.

**The tail is slow in the worst case.** Under the canonical prior $r_n \sim 1/\log n$, so the perturbation bound is weak at feasible $n$. The *effective* tail is far thinner: most long mutants die on arrival. Measurable as the fraction of length-$n$ programs that tip any attractor; if it decays geometrically the practical error does too. Making that rigorous is open (§9).

**Certification.** Under single-mutant transitions each transition costs exactly $|q|$ bits for the tipping mutant, so the question at level $n$ is: does any program in $\mathcal{L}_{n+1}\setminus\mathcal{L}_n$ tip any attractor of the $n$-chain? If none does, $\pi_{n+1} = \pi_n$ up to neutral mass. Mechanics in IMPLEMENTATION.md.

**The theorem: behavioral characterization.** For a candidate ecology, enumerate what an invader can *do* against it and show every such behavior loses or is neutral. Quantifies over behaviors, not programs; never touches $n$; available in the extensional arms; exhaustive by hand in the strong arm. The separable matching result (§4) and the handshake theorem (§3) are the instances.

**The computation: DSL simulation.** Attractor chain on the DSL at small $N$. Generates the candidate ecology the theorem is about; checks that finite behavior agrees with the characterization. It is not the proof. The DSL, arms, evaluator, chain algorithm, sweep, and repo layout are specified in IMPLEMENTATION.md.

**Predictions for the first run.** (a) The strong arm at $n=5$ has no stable cooperation: `or(X, THEM(ME))` grounds at $\varepsilon=\frac12$, where ALLD earns 0 against it (equal to FairBot-vs-FairBot) and $-1$ against ALLD (better than FairBot's $-1.5$), so ALLD weakly dominates it. The first viable reciprocator is the 6-node `or(and(X,X), THEM(ME))` at $\varepsilon=\frac14$. Report grounding rate with every result. (b) The strong arm at $n=6$ exhibits bistable switching between the FairBot–ALLC neutral edge and the all-ALLD sink. (c) The weak arm at $n\ge 9$ admits PrudentBot, which collapses the neutral edge to a point. (d) `eq(THEM,ME)` wins the source arm outright.

## 8. Evaluation — never selection

Reported as findings about $\pi$; never used to choose it:

- **Efficiency:** deadweight loss per interaction. Prediction: small but positive (the maintenance cost of conditionality).
- **Distribution:** on the Nash demand game, does the ecology land on the Nash split (Young 1993)? In separable form: which $\lambda$-ratio is selected among reciprocators at different rates? With `ROLE`: does it maximize the unweighted sum (§3)?
- **Coolness:** holds by construction (attractors are cool states); a rest-point diagnostic. Compatible with pairwise exploitation.

The moment any of these becomes a selector, the ecology reports back what was put in.

## 9. Open questions

1. **Does $\lim_N\pi_N$ exist, and does it equal the $N{=}\infty$ chain?**
2. **Effective tail.** Prove the fraction of length-$n$ mutants that tip any attractor decays geometrically, or find the counterexample.
3. **Drift stability / the regress.** A variant that punishes ALLC but tolerates ALLC-tolerators is itself a leak. The fixed point is the fully self-referential reciprocator resolved by grounding. Which one the chain selects is the second half of the efficiency theorem.
4. **Which $\lambda$ in multi-action separable games, and in fixed-role games.** Reciprocators at every rate are mutually neutral under best-reply; imitation with finite matching should select $\lambda\to 1$ (Robson–Vega-Redondo). Fixed-role prediction: Nash bargaining at the endogenous threat point.
5. **$k$-player generalization.** Programs become $(k{-}1)$-ary; payoff object is a $k$-tensor; attractor chain unchanged; behavioral characterization scales; DSL enumeration does not. The original coalitional question is answered by the process: only single mutants, by construction.
6. **Formal regime for $\varepsilon$.** "Small but $\gg e^{-cN}$" as a joint asymptotic.
7. **Time to efficiency.** The handshake mutant is 7–9 nodes. The theorem says where the population ends up; it says nothing about how long it takes.
