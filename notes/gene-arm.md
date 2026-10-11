# The gene arm: parametric bases, special-case genes, a credibility filter, spontaneous generation (notes, 2026-10-11)

Spec `specs/2026-10-11-gene-arm.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-11-gene-arm-gpt-6.1-sol.md`; the
[after review] text is the resolution). §1 is written before any project code of this experiment and before any
counted cell; every number in it is derived by hand. §1.14 (code validation of the hand claims) is appended after the
code exists and before any counted cell; §2 (costs) after that.

*Disclosure.* No scratch computation was run for §1. The evaluator semantics used in the hand traces are those of
`src/union.py` (linear GL Kripke chain: at world n, `BOX(P)` holds iff P held in the implemented play at every world
m < n; play stops when no box changes and n ≥ 2), `src/union_enforcement.py` (the per-world override of the RC / RR
arms) and `src/concessions.py` (probe atoms read a quoted encounter with a constant boss).

## 1. Design

### 1.1 Games

**Social organization game (SOG)**, the union run's game unchanged: boss B and workers W1, W2 in three separate slot
populations; the boss pays a wage s ∈ {0, ¼, ½} to each working worker and holds a whack policy h ∈ {strike (whack
strikers), none, source (whack every tagged worker)}; a working worker produces 1. Payoffs (c = 0.5, L = 1, no pool):
worker: s if working, −L if whacked; boss: Σ_working (1 − s) − c per whack. Joint code j = 4(3·s_i + h_i) + 2a1 + a2.
The spec's "h ∈ {none, 1, 2}" is read as the union run's three policies {none, strike, source}.

**Fixed-role chicken**, the `chicken` table of RESULTS "Fixed-role chicken": (St/St, St/Sw, Sw/St, Sw/Sw) =
(−10, 2, −1, 0); two populations (roles), no `ROLE`; a role-1 program a against a role-2 program b earns U[a, b].

Fitness map, fixation: w = 0.3, ρ(Δ) = (1 − e^{−wΔ}) / (1 − e^{−NwΔ}), one member of each slot per encounter, so a
slot mutant's payoff depends only on the other slots' residents (Lemma F of the chicken notes; the union run's test).

### 1.2 Base grammars (closed parametric forms) and counts

All atoms are level-0 boxes on the encounter's own world chain (3 nodes each, as in the union run).

**Workers, (t, q), 8 bases.** t ∈ {0, ¼, ½, ∞} is the wage threshold below which the worker strikes; q ∈ {0, 1} the
quorum flag. Recommendation (the frozen threshold–quorum interaction):

    strike  iff  W(t)  or  (q and Q*)
    W(0) = false,  W(¼) = BOX(s ∈ {0}),  W(½) = BOX(s ∈ {0, ¼}),  W(∞) = true
    Q* = BOX(s ∈ {0, ¼} and OTHER = strike)

*Why Q\* and not the union run's QUORUM = BOX(s < ½ → OTHER = strike):* under the frozen "or", the union run's
QUORUM is vacuously true at the fair wage, so a q = 1 worker would strike at s = ½ for ever. The union run's union
conjoined QUORUM with BOX(low); in GL, BOX(low) ∧ BOX(low → X) ≡ BOX(low) ∧ BOX(X) ≡ BOX(low ∧ X). Q\* is that
conjunction as one atom, so (0, 1) is the union run's union (and union′) exactly, at 6 nodes. **Tag** (what source
targeting reads): the Q\* atom occurs in the program text (q = 1, or any gene with trigger Q\*).

| base | name | text | nodes |
|---|---|---|---|
| (0, 0) | scab | `work` | 1 |
| (∞, 0) | striker | `strike` | 1 |
| (¼, 0) | T0 (refuser) | `if(BOX(s∈{0}), strike, work)` | 6 |
| (½, 0) | militant | `if(BOX(s∈{0,¼}), strike, work)` | 6 |
| (0, 1) | union | `if(Q*, strike, work)` | 6 |
| (∞, 1) | tagged striker | `if(Q*, strike, strike)` (dead clause, tagged) | 6 |
| (¼, 1) | T0-union | `if(or(BOX(s∈{0}), Q*), strike, work)` | 10 |
| (½, 1) | tagged militant | `if(or(BOX(s∈{0,¼}), Q*), strike, work)` (≡ militant in play, Q\* ⇒ BOX(low)) | 10 |

**Bosses, (s, h, p), 27 bases.** p is the probe level; probes read W1 only (as D₀ and D\* in RESULTS "Concessions"):
P_j(s′) = BOX(W_j(^(s′, none)) = strike), "W_j strikes in the quoted encounter ((s′, none), W1, W2)".

    p = 0:  (s, h)                                                 1 node
    p = 1:  if(P1(0), (½, h), (s, h))                              6 nodes   ((0, none, 1) = D₀)
    p = 2:  if(P1(¼), (½, h), if(P1(0), (max(¼, s), h), (s, h)))   11 nodes  ((0, none, 2) = D*)

With s = ½ the probes are dead (p = 1, 2 are syntactic twins of the constant (½, h)).

**Chicken, (a, b), 4 bases per role.** Recommendation: `Swerve if (b and BOX(THEM = Straight)) else a`. (St, 0) the
firm constant (1 node), (Sw, 0) the swerver (1), (St, 1) "straight unless provably facing a straight" (6), (Sw, 1)
(≡ swerver in play; 6).

### 1.3 The gene grammar

A gene is (trigger τ, override o), text `if(τ, o, ·)` spliced ahead of the base: 1 + 3 + 1 = **5 nodes** (≤ 6, the
spec's n). The override names the special-cased point (the action component it replaces) in the program text.

| role | triggers | overrides | genes |
|---|---|---|---|
| worker | BOX(s∈{0}), BOX(s∈{0,¼}), BOX(s∈{½}), BOX(h∈{strike}) ("threat"), BOX(h∈{source}), BOX(OTHER=work), BOX(OTHER=strike), Q* | work, strike | 16 |
| boss | BOX(W1=strike), BOX(W2=strike), BOX(W1=work), BOX(W2=work), P1(0), P2(0), P1(¼), P2(¼) | wage 0, ¼, ½; whack strike, none, source | 48 |
| chicken | BOX(THEM=Straight), BOX(THEM=Swerve) | Straight, Swerve | 4 |

"A whack having occurred" (spec) is read as the worker trigger BOX(h ∈ {strike}): in the one-shot world chain the
nearest event is the boss's implemented policy whacking strikers.

**Programs** = base + an ordered list of ≤ k genes (k the cap; distinct genes; same-trigger pairs allowed, the second
then dead). Counts: cap 2: workers 8·(1 + 16 + 16·15) = **2,056**; bosses 27·(1 + 48 + 48·47) = **62,235**; chicken
4·(1 + 4 + 12) = **68** per role. Cap 1: workers 8·17 = **136**, bosses 27·49 = **1,323**, chicken 4·5 = **20**.

**Named genes.**
- *whack* `w_j = (BOX(W_j = strike), whack strike)`;
- *quorum* `q = (Q*, strike)`;
- *probe concession* `π = (P1(0), wage ½)`;
- *firm* (chicken) `f = (BOX(THEM = Straight), Straight)`;
- for reference: *bridge* `(BOX(THEM = Swerve), Straight)`, *yield* `(BOX(THEM = Straight), Swerve)`, *threat
  accommodation* `(BOX(h ∈ {strike}), work)`, *de-escalation* `(BOX(W_j = strike), whack none)`.

### 1.4 Frozen operational semantics

1. **Evaluation.** At each world every atom's truth is computed (boxes from the implemented play at earlier worlds;
   probes from the quoted encounter's executed play, exactly as `src/concessions.py`, including its minimum-world
   rule). The program's recommendation is: the override of the **first listed gene whose trigger holds**, applied to
   its component; every other component is the base's. One gene is operative per world (a boss gene overriding the
   wage and a later one overriding the whack do not combine: the first firing gene wins outright).
2. **World 0.** Every box is vacuously true at world 0, so the first listed gene is always operative at world 0.
3. **Cap replacement.** A mutation that adds a gene to a program below the cap appends it (lowest precedence); at the
   cap it replaces the last listed gene.
4. **Threshold–quorum interaction:** §1.2, "or".
5. **Probe counterfactuals:** the quoted encounter ((s′, none), W1, W2) is evaluated on its own under the arm's
   execution rule; the probe reads W_j's executed action (ties to the recommendation, as in the concessions run).
6. **Execution rules:** CC (everything committed), RC (the boss's whack ex-post rational per world), RR (both slots'
   stage-2 moves ex-post rational per world), as `union_enforcement.override` (c = 0.5, no pool, tie "whack"). The
   wage is stage 1 and is committed in every rule. Chicken: committed play only.
7. **Stable world:** the world at which the evaluator stops; "the play" of an encounter is its implemented joint code
   there; a gene **fires** (is operative) in an encounter iff it is the first listed gene whose trigger is true at the
   stable world.

### 1.5 Two best replies

The encounter's extensive form (as in the enforcement run): stage 1 the boss's wage; stage 2, simultaneously, the
boss's whack and the workers' work/strike. Chicken has one stage.

- **Continuation best reply** (the filter's notion; "credible when it fires"). At the stable world of an encounter in
  which the gene fires, hold the history and the other slots' stable actions fixed and ask whether the override is
  payoff-maximal (ties allowed, tolerance 10⁻¹²) among the alternatives for its component:
  - stage-2 component (whack, work/strike, chicken action): the other slots' implemented actions fixed, the wage fixed;
  - stage-1 component (wage): the continuation of the subgame after an alternative wage s″ is the workers'
    executed play in the quoted encounter ((s″, h_imp), W1, W2) (the probe counterfactual; h_imp the carrier's
    implemented whack policy), so the boss compares Σ_working (1 − s″) − c·whacks over s″ ∈ {0, ¼, ½}.
- **Mutant-program best reply** (gene-stability, SG, every evolutionary deviation). Replace the carrier's program by
  the mutant and re-evaluate the whole encounter under the arm's execution rule (others' certificates, probes and
  actions change with the readable program); compare the carrier's payoff.

### 1.6 Arms

| arm | catalogue | execution | admissible genes |
|---|---|---|---|
| base-CC, base-RC, base-RR (references) | bases only | CC / RC / RR | none |
| **G-all** | all programs | CC | all |
| G-all-RC (reference) | all programs | RC | all |
| **G-cred** (override filter) | programs whose genes pass the filter | CC | genes passing §1.7 |
| **G-cred-whole** (whole-program credibility) | all programs | RR | all (stage-2 behaviour of base and gene alike rationalized per world; the wage committed for base and gene alike) |
| **G-asym** (declared asymmetry) | workers: all genes; bosses: no gene whose override is whack strike or whack source | CC | as stated |
| random removal (control) | the same number of genes per role as G-cred removes, drawn uniformly (seed 20261011) | CC | the rest |
| *-ctl (base-commitment controls) | the arm's catalogue with bosses restricted to h = none | as the arm | as the arm |

Filtered arms keep the original prior masses: removed programs are null mutations (the removed mass per slot is
reported; the renormalized variant is a reporting line, not a separate cell).

**Why G-cred-whole is the RR rule (by hand).** "The same test applied to every behaviour, base and gene alike, at every
point." (i) *Stage 2.* The per-point test of a stage-2 action is exactly the RR override, applied at execution to
whatever the program recommends; packaging (base or gene) is invisible to it, so the arm is encoding-invariant by
construction. (ii) *Stage 1.* Applied as a filter to base wages against the full reference catalogue, the test
empties the boss set: every constant wage is beaten somewhere by the counterfactual continuation: s = 0 against the
militant pair (0 → both strike, payoff 0; ½ → both work, payoff 1), s = ¼ and s = ½ against the scab pair (0 → 2).
So the wage stays committed for base and gene alike (as in the RR arm), and G-cred-whole = RR on the G-all catalogue.
This is the REJECTED "Static credibility clauses" outcome ("emptied the set") reproduced at stage 1; the stage-2
version is the RR execution rule, which the population then selects over.

**Chicken G-cred-whole is void (by hand).** A program that is a continuation best reply at every encounter must play
Swerve against a stable Straight and Straight against a stable Swerve; against its own copy in the other role it is
the same deterministic reader, and identical deterministic readers in opposite roles never anti-coordinate (RESULTS
"Fixed-role chicken"), so it fails against itself. The whole-program filter therefore empties the chicken catalogue
(again the REJECTED entry's "emptied the set (Chicken under mutual-Stackelberg)"); a per-world execution rule has no
stage order to break the simultaneity (both slots best-responding to the other's recommendation turn mutual Swerve into
a crash). Chicken runs G-all, G-cred, G-cred-ctl (bases (Sw, b) only), random removal, the base catalogue and the
constants reference.

**Re-opening check (REJECTED, "Static credibility clauses").** That entry dropped static credibility clauses *as
solution concepts* (they leave the folk theorem, collapse to Nash, or empty the set). Here the filter restricts the
mutation support and the chain remains the selector, which is what the entry recommended ("non-credible threats are
outcompeted, not forbidden"); the arm measures whether forbidding adds anything to outcompeting. The whole-program
versions reproduce the entry (empty set at stage 1 and in chicken); no new evidence re-opens it as a solution concept.

### 1.7 The override filter (G-cred) and the frozen reference catalogue

A gene g is **admissible** iff at every encounter of the frozen reference catalogue in which g fires, its override is a
continuation best reply for its carrier. *Reference catalogue:* all unfiltered programs of the arm's cap (every carrier
of g, with g in any list position, against every program of the other slots), under CC. *Firing witnesses:* for each
gene, the prior-heaviest encounter in which it fires and fails (or passes), recorded. *Vacuous admission:* a gene that
fires in no reference encounter. *Sensitivity checks:* (a) admitted-only (iterate A_{k+1} = filter(catalogue(A_k)) from
A_0 = all genes; report convergence or a cycle), (b) residents-only (the reference is the support (99% of π) of the
G-cred prior-kernel chain at N = 10⁴, length prior); both report verdict changes only, no chains.

**Hand facts about the filter.**
- *Worker overrides.* At any stage-2 point, work − strike = s + L·[h_imp = strike] ≥ 0 (a tagged worker under source
  targeting is whacked either way). So **every worker gene with override work passes**, and a strike gene passes iff it
  fires only at s = 0 with h_imp ≠ strike.
- *Boss whack overrides.* `whack none` is always a (weak) best reply; `whack strike` passes iff no striker is present
  where it fires; `whack source` iff no tagged worker is present.
- *Boss wage overrides.* Constant strikers make raises pointless (the striker strikes at every wage) and readers make
  cuts costly, so a wage gene passes only if its trigger fires on a narrow set of worker pairs.

**Hand verdicts on the named genes (G-cred, cap 1, CC reference):**

| gene | verdict | failing witness (stable play; continuation comparison) |
|---|---|---|
| whack `w_1` | **fails** | (0, none, 0)+[w_1] vs (striker, striker): w0 trigger vacuous, both strike; trigger stays true; play (0, strike, S, S); whack strike −2c = −1 vs none 0 |
| quorum `q` | **fails** | (¼, none, 0) vs (scab+[q], scab+[q]) (≡ the union pair): w0 Q* vacuous, both strike; s = ¼ low and the other strikes, so Q* stays true; play (¼, S, S); strike 0 vs work ¼. (At (0, none) it is a tie and passes; at (0, strike) it fails, −1 vs 0.) |
| probe concession `π` | **fails** | (0, none, 0)+[π] vs (T0, T0): the quoted 0-boss makes both T0 strike, so P1(0) holds at every world; the main play is (½, W, W), boss 1; counterfactuals: s″ = 0 → both strike, 0; s″ = ¼ → both work, 1.5; s″ = ½ → 1 |
| firm `f` | **fails** | (St, 1)+[f] (≡ the constant Straight) vs (St, 0): play (St, St); Straight −10 vs Swerve −1 |
| bridge | passes | fires only where the opponent stably swerves: Straight 2 vs Swerve 0 |
| yield | passes | fires where the opponent stably goes straight: Swerve −1 vs −10 |
| threat accommodation, de-escalation | pass | work and whack none are always continuation best replies |

The RE's rationale ("a quorum strike at zero wage costs nothing, so it passes") holds at (0, none) only: the reference
catalogue contains ¼-paying bosses against which Q\* fires, and there a strike forgoes ¼. **Hand corollary:** a strike
at a positive wage is no more credible than a whack; G-cred keeps the accommodating half of the gene grammar (work
overrides, whack none, and whatever fires vacuously) and removes every named commitment gene, union's included.

### 1.8 Encoding invariance (named genes)

| named gene on carrier | equivalent base encoding | play identical? | G-cred verdict, gene / base | G-cred-whole |
|---|---|---|---|---|
| `q` on scab (0, 0) | union (0, 1) | yes, identical text semantics and tag | fails / unfiltered (admitted) | identical (RR acts on play) |
| `π` on (0, none, 0) | D₀ = (0, none, 1) | yes | fails / admitted | identical |
| `w_1` on (0, none, p) | (0, strike, p) | **no**: the gene whacks only while W1 has struck at every earlier world (it never whacks a W2-only striker, and a W1 that worked once switches it off); nearest, not equal | fails / admitted | identical (both rationalized to "none") |
| `f` on (St, 1) | (St, 0) | yes ((St, 1)+[f] plays Straight at every world) | fails / admitted | void |

**Hand verdict: encoding invariance fails for every named gene under the override filter** (the filter sees the gene's
override point and never the base's), and holds under G-cred-whole by construction. The equilibrium notion "no
admissible gene improves" is therefore representation-relative unless whole-program credibility is used. The code
reports, for each pair, the fraction of reference encounters (by prior mass) on which the two encodings play
differently.

### 1.9 Gene-stability, gene-completeness, Nash, Pareto

**Gene-stable** (arm X): a monomorphic state (B, W1, W2) at which, for every slot and every gene admissible in X, the
mutant "resident + gene" (cap rule §1.4.3) is not a strict mutant-program improvement for its carrier (re-evaluated
under X's execution rule).

**Gene-completeness** (what one gene can and cannot express from a resident), listed:
1. a gene acts at world 0 always (§1.4.2), so it cannot defer an action to "after the opponent has shown its hand";
2. no unconditional move: a base change (a constant boss becoming another constant, a scab becoming a militant) is not
   a gene deviation; there is no ⊤ trigger;
3. one component per world: a joint change of wage and whack needs two genes (cap 2), and at cap 1 is inexpressible;
4. conditions outside the vocabulary: negated boxes (militant⁻ = strike unless provably fair), level-1 boxes, probes at
   ½ or of work, conjunctions other than Q\*, probes of the other worker in the base;
5. at cap 1, adding a gene replaces the resident's gene, so "resident + gene" can also delete behaviour.
So **program-Nash ⇒ gene-stable** (gene mutants are programs of the grammar) but not conversely.

**Nash of the role game.** The stage game: boss strategies (s, h) ∈ 9, worker strategies {work, strike},
simultaneous, payoffs of §1.1 with the state's tags. A state is *Nash* iff its stable play is a pure Nash equilibrium of
that game. Hand: a worker's work − strike = s + L[h = strike] ≥ 0, so in any pure NE no worker strikes at s > 0 or under
h = strike unless indifferent; the boss's wage is a best reply only at s = 0 (if anyone works, cutting to 0 gains;
if nobody works, every wage ties); a realized whack is never a boss best reply (dropping it saves c), and a whacked
striker would rather work. **Pure NE plays = zero wage with no realized whack** (both working under any h; a split or
both striking under h = none, or source with untagged strikers). Bayes–Nash with roles as public
types adds no uncertainty and coincides with Nash; it is noted, not scored.

**Pareto frontier** (over stable plays): SOG: the three both-work, no-whack plays (2, 0, 0), (1.5, ¼, ¼), (1, ½, ½)
(every other play is dominated by one of them); chicken: (St, Sw) (2, −1), (Sw, St) (−1, 2), (Sw, Sw) (0, 0).
A Pareto improvement exists exactly from strikes, splits, realized whacks and crashes.

**Named states by hand** (G-all = CC; G-cred ⊂ G-all genes; G-cred-whole = RR):

| state | play (CC) | Nash | Pareto | G-all | G-cred | G-cred-whole | witness |
|---|---|---|---|---|---|---|---|
| Z = (0, none, 0) \| scab \| scab | (0, W, W) | yes | yes | stable | stable | stable | the boss is at its maximum 2; a constant boss pays 0 to every worker program |
| Z_w = (0, strike, 0) \| scab \| scab | (0, W, W) | yes | yes | stable | stable | stable | as Z |
| S = (0, none, 0) \| striker \| striker | (0, S, S) | yes | **no** (Z dominates) | stable | stable | stable | strikers are constant; a worker's switch to work is neutral (0 → 0) |
| F = (½, none, 0) \| militant \| militant | (½, W, W) | no | yes | **stable** | stable | **unstable** | CC: every wage-cutting gene fires at world 0, the militants strike at world 0 (vacuous BOX(low)), so `BOX(W_j = work)` dies and the base pays ½ again, or the cut sticks and both strike (payoff 0). RR: `(BOX(W1 = work), wage ¼)`: at w0 the wage is ¼, the rational militant works, the trigger stays true, play (¼, W, W), boss 1.5 > 1 |
| F_u = (½, none, 0) \| union \| union | (½, W, W) | no | yes | stable | stable | unstable | as F (Q\* vacuous at w0 plays the role of BOX(low)); RR witness the same gene |
| I = (¼, none, 0) \| T0 \| T0 | (¼, W, W) | no | yes | stable | stable | stable | every cut either dies at world 1 or makes T0 strike (CC and RR alike; under RR the cut to 0 ties at w0 and T0 strikes) |
| F\* = D\* \| militant \| militant | (½, W, W) | no | yes | stable | stable | – (under RR D\* pays ¼: P1(¼) is false for rational militants) | as F |
| Z_D₀ = D₀ \| scab \| scab | (0, W, W) | yes | yes | **unstable** | stable | **unstable** | W1 adds `(BOX(s∈{0}), strike)`: the quoted 0-boss sees a strike, D₀ pays ½, W1's box dies at world 1 and it works: ½ > 0. Under G-cred the gene is removed (it fires at s = 0 against (0, strike) bosses, −1 vs 0); under RR the strike at s = 0 is a tie and is executed |
| chicken R1 = (St, 0) \| (Sw, 0) | (St, Sw) | yes | yes | stable | stable | – | the loser's genes either crash (firm) or are overruled at w1 |
| chicken R1′ = (St, 1) \| (Sw, 0) | (St, Sw) | yes | yes | **unstable** | **unstable** | – | role 2 adds the bridge `(BOX(THEM = Sw), St)`: w0 (Sw, St); the reader yields from w1; play (Sw, St), role 2 gets 2 > −1. The bridge passes the filter |
| chicken crash (St, 0) \| (St, 0) | (St, St) | no | no | unstable | unstable | – | yield gene: −1 > −10 |
| chicken dove (Sw, 0) \| (Sw, 0) | (Sw, Sw) | no | yes | unstable | unstable | – | bridge gene: 2 > 0 |

So, by hand: **gene-stable and Nash are incomparable** (F, F_u, I, F\* gene-stable but not Nash; Z_D₀ Nash but not
gene-stable under G-all and G-cred-whole); **the fair state is gene-stable under G-all and gene-unstable under
G-cred-whole**, the reverse of the RE's prediction 4 clause (the rational worker's work at world 0 is what makes the
cut stick; committed militants poison the cut's trigger at world 0); **S is gene-stable, Nash and Pareto-dominated**:
the proof device "a Pareto improvement would have been adopted as a fit gene" fails at S because the improving move
(a worker switching to work) is neutral for its carrier, so it is adopted by drift, not by selection.

### 1.10 Kernels

Every kernel is a mutation kernel; fitness is the chain's (ρ(Δ) on the mutant-program payoff difference).

- **Prior kernel.** A mutation event picks a slot (⅓ each) and draws a program from the arm's prior (null mass for
  filtered programs).
- **SG (spontaneous generation).** With probability ½ the prior kernel; with probability ½ the *targeted* proposal:
  the set T of the slot's triggers whose proposition holds in the state's stable play (for probes: in the quoted
  encounter's stable play) — *the stable-play reading*, chosen because it is a function of the classes (below) — and
  for each τ ∈ T one override o\*(τ): the mutant-program best reply among the arm's admissible overrides for τ, ties
  broken toward the override equal to the carrier's own implemented action component (the conservative gene), then by
  the fixed order (wage 0, ¼, ½, whack strike, none, source; work, strike; Straight, Swerve). Mass ½/|T| on each
  mutant "resident + (τ, o\*(τ))" (cap rule). If T is empty the targeted half is the prior kernel. A targeted proposal
  is *strict* if its payoff exceeds the resident's, *conservative* otherwise; the report separates them.
- **Uniform admissible-local kernel.** With probability ½ the prior kernel; with probability ½ a uniformly drawn
  admissible gene of the slot (any trigger) added to the resident (cap rule).
- **Coalition kernel** (labelled separate cell). A coalition event (rate ε² per pair of slots) places one mutant in
  each of two slots simultaneously; its fixation probability ρ₂ is the exact two-slot Moran process with the third slot
  fixed (states (k1, k2) ∈ [0, N]², each step a birth–death in a uniformly chosen one of the two slots with weights
  exp(w f), f the expected payoff against the other slots' current composition; when one slot is absorbed the other
  finishes as a one-slot constant-selection process). Its rate ε²·⅓·μ(q1)μ(q2)·ρ₂ is compared with the sequential path
  through the neutral intermediate, rate ε·⅓μ(q1)·ρ₁ × P(second step before the intermediate is left), so "faster" is
  a statement about ε (the threshold ε\* is reported); computed exactly at N = 10², 10³ (10⁶ states at 10³).

### 1.11 Lumping

- **Payoff kernel.** Programs are lumped into behavioural classes per execution rule: workers by (tag, the stable joint
  code against every (boss, other worker) pair), bosses by the stable code against every worker pair. Lemma F makes
  the three-slot chain monomorphic and exact on class triples (no polymorphic traps, no twin drift issue: within a
  class every member has the same payoff against every resident pair, and a member-to-member move is a null event).
- **Prior kernel.** State-independent; class mass = Σ member masses. Lumpable.
- **SG and the uniform-local kernel.** The mutant depends on the resident's text, not only its class. At cap 1 the
  mutant "resident + g" is (base(resident), [g]) whatever the resident's gene, so the proposal depends on (class, base);
  with the stable-play reading the trigger set T depends only on the state's classes (the stable play, and for probes
  the workers' stable play against the quoted constant bosses, are class functions); the override's payoff is a
  function of the mutant's class. **Hence the local kernels are exactly lumpable on refined classes (behaviour class ×
  base) at cap 1**; at cap 2 the refinement is (class, base, first gene, gene count ≥ 1). The box-at-stable-world
  reading of "true at that state" is *not* lumpable on behaviour classes (transient histories differ within a class);
  that is why the stable-play reading is frozen. The refined classes are the retained syntactic twins.
- **Lottery.** Classes per execution rule (the ε = 0 kernel is payoff-only), except SG innovation, which runs on
  refined classes.

### 1.12 Controls and cells

- *Base-commitment controls:* SOG bosses restricted to h = none (9 bases), for G-cred, G-cred-whole and G-asym;
  chicken bases (Sw, b) only, for G-cred.
- *Random removal:* per role, the same number of genes as G-cred removes, drawn uniformly (seed 20261011); the removed
  prior mass and the renormalized variant are reported.
- *Scale guard:* class counts per arm before any chain; if an arm's larger slot exceeds 3,000 classes, the SOG cells run
  at cap 1 and are reported as a different experiment (a lower bound by fingerprints over sampled opponent pairs
  suffices to fire the guard). Chicken runs at cap 2 (68 programs per role).
- *Chain:* ε → 0; N = 10³, 10⁴; uniform prior (uniform over program texts of the arm's grammar; the base references
  uniform over bases) and the length prior (bits = log₂ a(|p|) + 2 log₂|p| + 1, a(s) the number of G-all programs of
  size s at the cap). Solver: the union run's hybrid exploration (θ = 10⁻⁹, log-domain GTH; exact under Lemma F),
  seeds = named states + every class triple with no strict exit; the cut diagnostic wherever the unexplored flow
  exceeds 2%. Chicken: the exact two-population K² chain (`fixed_role_chicken.two_pop_chain`, log check).
- *Lottery:* SOG (N, I) = (100, 64), mN = 1, 40 runs per arm (G-all, G-cred, G-asym; CC execution), seeds iid from the
  arm's length prior renormalized over admissible programs, the concessions kernel (`concessions.kern_c`), closure stop
  as in the social organization lottery; SG innovation (per (island, slot) unit, probability 1/N per generation, the
  child replaced by an SG proposal at the triple (parent, the island's majority residents of the other slots)) as a
  separate finite-ε object. Chicken: I = 64, N = 100, mN ∈ {0, 1}, 40 runs (`fixed_role_chicken.sim_two_pop`).

### 1.13 What the hand analysis predicts for the arms

- **G-cred removes every named commitment gene** (§1.7) but the bases keep committed whacks (h = strike, source),
  committed strikes (t ∈ {¼, ½, ∞}) and both probe concessions (p = 1, 2): G-cred ≈ G-all minus fakers' and
  commitments' gene spellings, plus accommodation genes.
- **G-cred on the base-commitment control** has no whack anywhere and committed worker strikes: ≈ RC.
- **G-cred-whole = RR**: the rational strike is free only at s = 0, so the smallest positive wage (¼) is the
  expected attractor, as in the enforcement run (uniform reduced chain ¼ 0.668; full chain under the length prior 0.75).
- **The RS's asymmetry is not a credibility property:** a committed strike at s > 0 fails the same continuation test as
  a committed whack. G-asym (declared) is the arm that can show the asymmetry's effect; no filter derives it.
- **Proof device:** strict gene-stability cannot exclude Pareto improvements reachable only by neutral steps (S → Z),
  and on the frontier (every both-work play) it is vacuous: the device has content only at strikes and crashes.

### 1.15 G-recip: reciprocal credible genes (added at the RS's request, 2026-10-11, before any code or cell)

*RS:* "I want to find a narrower class of genes restricting outcomes to the 'good' (eg pareto efficient) ones."

**Definition (frozen).** A gene is admissible in G-recip iff (i) its trigger is a certificate about the opponent's play
in this encounter and (ii) its override passes the per-point continuation test (§1.5, the test G-cred-whole applies at
every point) at every encounter of the frozen reference catalogue where it fires (§1.7). Execution CC (genes filtered,
bases as written, as in G-cred); the base-commitment control (bosses h = none) is reported beside it.
Reciprocal triggers (i):
- workers: the boss's wage toward me, BOX(s∈{0}), BOX(s∈{0,¼}), BOX(s∈{½}); the other worker's play, BOX(OTHER=work),
  BOX(OTHER=strike), Q\*. Excluded: BOX(h∈{strike}), BOX(h∈{source}) (the bare "whacked" condition: a policy, not
  play toward me in this encounter);
- bosses: BOX(W_j = strike), BOX(W_j = work). Excluded: the probes P_j(0), P_j(¼) (certificates about a quoted
  constant, not about this encounter);
- chicken: both triggers.
So G-recip ⊂ G-cred (same test, fewer triggers).

**Admitted genes by hand.** Workers: the six reciprocal triggers with override work (work is always a continuation best
reply, §1.7); no reciprocal strike gene (each fires at a positive wage or under a strike-whacker somewhere: Q\* at ¼,
BOX(s∈{0}) against (0, strike), BOX(OTHER=·) at ½). Bosses: the four reciprocal triggers with override whack none;
whack strike / source and every wage override fail (§1.7 witnesses: the whack gene against the striker pair; wage
cuts against (scab, T0); raises against (striker, scab)) unless a code count finds a vacuous one. Chicken: bridge
`(BOX(THEM=Sw), St)` and yield `(BOX(THEM=St), Sw)` pass, firm and `(BOX(THEM=Sw), Sw)` fail (Swerve against a stable
swerver, 0 < 2).

**Is every gene-stable state under G-recip Pareto-efficient? No, by hand.**

| gene-stable, Pareto-dominated state | dominated by | admissible gene that would leave it (weakly) |
|---|---|---|
| S = (0, none, 0) \| striker \| striker, play (0, S, S), payoffs (0, 0, 0) | Z (2, 0, 0) | worker `(BOX(s∈{0}), work)` (or any reciprocal work gene with a true trigger): neutral for the carrier (0 → 0), strict for the boss; then the other worker likewise |
| scab split (0, none, 0) \| scab \| striker, (1, 0, 0) | Z | the striker's `(BOX(s∈{0}), work)`, neutral |
| the same with a constant (s, none) boss, s > 0, both striking, (0, 0, 0) | the both-work play at s | the work gene is strict there (s > 0), so these are *not* gene-stable |

The device fails only through neutral improvements: G-recip's admissible genes include the move that leaves S, but
it is weak for its carrier, so strict gene-stability does not exclude S. Under the weak version ("no admissible gene
weakly improves its carrier and strictly improves someone") S and the zero-wage splits are not stable; the code
reports both versions.

**Which Pareto-efficient states G-recip still admits.** Every both-work, no-whack play is on the frontier (§1.9), so
G-recip cannot select among wages: Z (zero wage, everyone working) is efficient and gene-stable; F and I are gene-stable
under CC execution because their bases carry the committed strikes; under any execution that rationalizes the strike
(RR), F is gene-unstable (§1.9). **The fair wage needs a credible strike to make zero wage inefficient, and no strike
at a positive wage is credible in this game** (work − strike = s + L[h = strike] ≥ 0): Pareto restriction alone
cannot pick fair over zero wage, because the zero-wage play is Pareto-efficient.
