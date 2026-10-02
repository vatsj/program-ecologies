# Predictions: universality against drift-closure (moats without copy subsidies), 2026-10-02

Status: reviewed by astra (`reviews/2026-10-02-drift-closure-gpt-6-astra.md`) and fable
(`reviews/2026-10-02-drift-closure-fable.md`), then revised; changes are marked [after review]. Committed before the run.
Before the commit only the following were run:
- static computations over the enumerated modal languages (`src/moat_static.py`, `runs/drift_closure_static.md/json`);
- static single-edge rates with `Chain.expand` on single states (`src/moat_rates.py`, `runs/drift_closure_rates.json`);
- a *local estimate* for every planned cell: the chain restricted to all-D plus every monomorphic state within three
  transitions of it, built only from `Chain.expand` on single states and solved by GTH (`src/moat_estimates.py`,
  `runs/drift_closure_estimates*.json`). [after review, fable 1.1] At n = 8 depth 3 reaches all 471 classes, so this is
  the *unpruned monomorphic chain*. The driver differs from it only by polymorphic states and θ-pruning. The cell
  predictions below are therefore a computational cross-check of the driver, not independent predictions (astra §1);
  the independent content is in Part 1 and in the static map. Where driver and estimate disagree, the driver is
  suspect unless polymorphic flow is non-zero;
- one declared driver smoke cell (listed at the end).

## Background

- In the free modal arm, cooperation rises toward 1 with odds ∝ N^(1/2). The cooperative state's exit is neutral
  drift into ALLC at rate ∝ 1/N, after which D invades (RESULTS.md, "Modal (Löbian) arm", "E2 ratchet").
- Every mechanism so far that makes the exit decay faster than 1/N is a moat: a copy subsidy (lazy pricing,
  cert0diag) or a clique. A moat locks in whichever ALLC-punishing family it reaches first (RESULTS.md, "Priced arm",
  "Certificate pricing").
- Certificate pricing without a copy subsidy gives one cooperative network containing FairBot, at the free arm's rate.
- Open problem (THEORY §9.2, last paragraph of "Certificate pricing"): one cooperative network *and* an exit faster
  than 1/N, without copy subsidies or self-recognition. THEORY §9.7's regress is the suspected obstruction.

This brief has two parts. Part 1 states the trade-off precisely and proves it for the pure game, with a rate law and a
statement about prices. Part 2 tests the mechanisms that the propositions leave open.

## Part 1. The object, the trade-off and its proof

**Setting.** PD with T > R > P > S (here 1, 0, −1, −2), deterministic programs, the free modal arm (`modal.build`), the
ε→0 chain (`src/chain.py`): single mutants, Moran fixation with fitness exp(w·payoff), mean-field payoffs without
self-play. A state is *cooperative* if its residents play (C, C) among themselves.

**Definitions** (all over behavioural classes of L_n).
- *Mutual-cooperation graph G*: vertices are self-cooperating classes; x–y is an edge iff x and y play (C, C).
- *Suckerable*: x is suckerable iff some y in L_n has x(y) = C and y(x) = D. Such a y is a *faker* of x.
- *Neutral closure* of x: the classes reachable from x by neutral single-mutant substitutions (Lemma 1 shows these are
  exactly the G-edges).
- *Drift-closed* (the lead's definition): no class in x's neutral closure has a strict invader.
- *Universality* of x: the μ-weighted share of FairBot's component of G (ALLC excluded) that x mutually cooperates
  with. Also reported: whether x cooperates with FairBot itself. An evaluation, never a selector.
- *Leak* ℓ(x): the prior mass of x's suckerable mutual cooperators. The world all-x moves to them at rate ℓ(x)/N per
  mutation event.

**Lemma 1 (single-mutant exits from a cooperative world).** Let all-x be cooperative and y a single mutant. With
g(k) the payoff gap of y at k copies, g(k) = [(k−1)u(y,y) + (N−k)u(y,x) − k·u(x,y) − (N−k−1)R]/(N−1), which is linear in k:
[after review, fable] Assumes the four PD payoffs are distinct, so u(y,x) = R identifies (C, C). A single mutant in a
cooperative PD world has no interior attractor, so the chain's polymorphic and valley-crossing routes add nothing
beyond e^(−Θ(N)) (the retry from 1/2 gives e^(−wN/4) for self-cooperating rivals: 5·10⁻⁴ at N = 100, so
"exponentially small" is honest from N ≈ 10³).
1. *y fakes x* (u(y,x) = T). Then u(x,y) = S and u(y,y) ∈ {R, P}, so g(1) → T − R > 0 and g(N−1) → u(y,y) − S > 0. The
   gap is positive at every count, and ρ → 1 − e^(−w(T−R)): an N-independent exit.
2. *y plays (C, C) with x.* Then g(k) = (k−1)(u(y,y) − R)/(N−1). If y cooperates with itself, g ≡ 0 and ρ = 1/N exactly.
   Otherwise g(k) = −(k−1)(R−P)/(N−1), and ρ ≤ e^(−Θ(N)).
3. *Otherwise* u(y,x) ∈ {P, S} < R. Then g(1) < 0, and the accumulated log-ratio up to the first count where g turns
   positive (if any) is −Θ(N), so ρ ≤ e^(−Θ(N)).

So the only sub-exponential exits from a cooperative world are fakers (Θ(1)) and self-cooperating mutual cooperators
(exactly 1/N). In the chain's language, neutral moves are exactly the G-edges, and they are symmetric.

**Proposition 1 (neutral closure).** The neutral closure of x is its component K(x) in G. x is drift-closed iff K(x)
has no suckerable member. If x is drift-closed, every transition out of K(x) has probability e^(−Θ(N)).

**Corollary 1 (the trade-off; THEORY §9.7 made exact).** FairBot cooperates with ALLC, and ALLC is suckerable (by D).
If x mutually cooperates with FairBot, or with any member of K(FairBot), then K(x) = K(FairBot) ∋ ALLC, so x is not
drift-closed. Equivalently, every drift-closed class has universality exactly 0. *Proof:* the definitions and Lemma 1.
The regress in §9.7 is this statement for a ladder: a program that punishes ALLC but cooperates with an ALLC-tolerator
y has y, hence ALLC, in its closure. The trade-off is not a frontier with interior points; it is a corner.
[after review, astra/fable] The corollary is definitional once Lemma 1 is granted; its content is the static fact
ALLC ∈ K(FB). It is checked statically, not by any chain cell, and no fringe cell can falsify it. The dynamical
content is Proposition 2.

**Proposition 2 (rate law in the pure game).** [after review: assumptions stated, astra §1, fable (a)] Assume a fixed
finite language and prior; a cooperative network whose mass sits on an unsuckerable core entered from all-D by a
program that is neutral at one copy there; every suckerable member's faker leads out of the network with probability
bounded below; and all-D holding the non-cooperative mass. Then:
- For any self-cooperating x, the probability per mutation event of leaving all-x for a suckerable world is at least
  ℓ(x)/N.
- *Leak floor* [narrowed after review, astra]: if x cooperates with FairBot itself, all-x moves to all-FairBot at
  μ(FB)/N, and from all-FairBot ALLC (μ(C) ≈ 0.47) is reached before a return to x with probability ≥ 0.9. So such a
  class leaks at least about 0.9·μ(FB)/N ≈ 4.6·10⁻³/N, whatever its own leak. Positive universality alone does not
  give this floor (P* has universality 0.10 through D-cooperating mates, not through FairBot).
- *Uniform ratio* [after review, fable §5]: statically, min over unsuckerable classes of ℓ(x)/μ(x) is 96 / 94 / 94 /
  93 / 93 at n = 6 / 8 / 9 / 10 / 11, and it is attained by FairBot. Every prudent class has a larger ratio (PrudentBot
  about 3,700, P* about 1,100). So, per unit of prior mass, no order of prudence improves on FairBot's leak in the pure
  game; it lowers the leak only by lowering the mass.
- The quantity the chain measures is the *network exit*, not ℓ. ℓ over-counts where a faker is itself cooperative
  (BTT's faker is).
Two consequences:
- *Exponent.* Entry into all-D is at most Θ(N^(−1/2)). By Lemma 1 applied to all-D, no mutant has a positive gap at
  one copy, since u(y, D) ≤ P. The best is neutral at one copy with a positive slope. A non-closed network exits at
  Θ(1/N). Its unsuckerable members leave only by neutral drift, and its suckerable members hold O(1/N) of its mass,
  since they are left at Θ(1). Flux balance between the network and the rest then gives cooperative odds Θ(N^(1/2)),
  provided all-D holds the non-cooperative mass. This makes β = 1/2, which the price-scaling proposition (THEORY §9.2)
  took as an empirical premise, a consequence of Lemma 1 for any non-closed network entered by a program that is
  neutral at one copy in all-D.
- *Constants.* Prior and grammar choices that keep these assumptions change ℓ and μ, and so the constant, not the
  exponent. [after review, astra] A grammar change can also change entry barriers or add non-cooperative traps, which
  the assumptions exclude; the claim is for the two choices tested here.

**Proposition 3 (prices cannot close the shadow edge).** Let fitness payoffs be U(x,y) − c(x,y), with c ≥ 0 and
c(constant, ·) = 0: constants read nothing. In any world all-x with x(ALLC) = C:
- ALLC earns R against x, and R ≥ R − c(x,x);
- x earns R − c(x,C) ≤ R against ALLC.

So ALLC weakly dominates x, and ρ(ALLC | x) ≥ 1/N. D then invades ALLC strictly, since D pays nothing. For a family
to exit faster than 1/N, its π-mass must therefore avoid ALLC-tolerant worlds, and every neutral-in-the-game path from
its worlds to an ALLC-tolerant world must be blocked. [corrected after review, astra] A block is an edge y → z where z
is on-path neutral to y but strictly deleterious as a newcomer: c(z, y) > c(y, y), or equality with an adverse slope,
which gives exponential suppression, not a 1/N correction (fable). The incumbent reads itself more cheaply than the
newcomer reads it. That is a local incumbency advantage, which is what a moat is. For a family that cooperates with
FairBot, the edge y → FairBot itself must be blocked, so c(FB, y) > c(y, y). Work-monotone prices give the opposite
sign there, because FairBot has one atom. Copy subsidies are one way to get the sign; any way is a moat.

**What the propositions leave open.** Lemma 1 and Proposition 3 cover payoffs from the pure game and prices that leave
constants free. The remaining class is a payoff term that *charges the shadow itself*: something that makes ALLC
strictly worse than FairBot in a FairBot world. The natural instance is off-path exposure, a background of other
programs (a *fringe*). [after review, fable 1.4] A fixed fringe is exactly an opponent-independent price
c(x) = −δ·f(x) that charges constants: the class Proposition 3's hypothesis excludes. It is neither a copy subsidy nor
self-recognition. It imposes a fixed, world-independent fitness ordering, so where it closes several families it
favours the f-maximal one rather than whichever arrives first. Part 2 tests it, along with prior and grammar choices
as diagnostics of Proposition 2.

**Conjecture 4 (no drift-closed class in the unbounded modal language).** Every self-cooperating modal program has a
suckerable mutual cooperator in L_n for n large enough. Static evidence is below. The suggested construction is the
THEM(THEM)-sibling x̃ = x[THEM(ME) → THEM(THEM)], which judges opponents by their self-play. In every row of the
frontier below, a sibling of this kind, or a non-provability sibling that cooperates with D, is among the top leaks.
Not proved.

### Static map (`runs/drift_closure_static.md`)

**The graph G is one component at every n tested,** with or without ALLC. No class is drift-closed. Every
self-cooperating class is suckerable or one neutral step from a suckerable class (maximum drift distance 1). The
corollary's checks hold at every n: universality > 0 implies membership in K(FB), and K(FB) has a suckerable member.

| n | classes | self-cooperating | components of G | drift-closed classes | unsuckerable classes (μ) | max drift distance |
|---|---|---|---|---|---|---|
| 6 | 51 | 18 | 1 | 0 | 3 (0.0149) | 1 |
| 8 | 471 | 237 | 1 | 0 | 9 (0.0102) | 1 |
| 9 | 863 | 405 | 1 | 0 | 13 (0.0104) | 1 |
| 10 | 1,752 | 764 | 1 | 0 | 15 (0.0104) | 1 |
| 11 | 5,545 | 2,520 | 1 | 0 | 38 (0.0104) | 1 |
| 8, boxes to PA + Con² | 1,132 | 554 | 1 | 0 | 20 | 1 |
| 9, boxes to PA + Con² | 2,275 | 1,025 | 1 | 0 | 36 | 1 |

The rival "networks" of earlier runs (the P* block against FairBot's) are blocks of the π-support. In the language
they are joined: P* ← `not(and(BOX(THEM(ME)),BOXD(THEM(ME))))` ← FB1 ← FairBot.

**The frontier: leak against universality** (n = 10, PA + Con; n = 8–11 agree within 10%):

| class | order of prudence | cooperates with FairBot | universality | leak ℓ | leak not via D-cooperators | top leaks |
|---|---|---|---|---|---|---|
| FairBot | 0 | yes | 0.769 | 0.479 | 0.0138 | ALLC, `BOX(THEM(THEM))` |
| PrudentBot `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | 1: defects on D-cooperators | yes | 0.326 | 5.2·10⁻³ | 5.2·10⁻³ | `BOX(THEM(THEM))` |
| P* `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` | 2: defects on ALLC-cooperators | no | 0.104 | 3.3·10⁻³ | 3.0·10⁻⁶ | `not(BOX(THEM(ME)))` |
| P12b `and(and(BOX1(THEM(ME)),not(BOX(THEM(^C)))),BOXD2(THEM(^D)))` (probe, size 14, PA + Con²) | 1 and 2 | no | ≈ 10⁻⁴ | 2.0·10⁻⁶ (L_8) | — | its own THEM(THEM) siblings |

Lower leak comes with lower universality at every rung, and the order is monotone. The more prudent the class, the
more parochial.

**What n and proof strength each rung needs** (candidates probed against L_9 and L_10 at prior mass 0):
- *Order 1 (PrudentBot):* n = 8, PA + Con.
- *Order 2 (defect on ALLC-cooperators):* n = 8 as P*, or n = 9 as `and(BOX1(THEM(ME)),not(BOX(THEM(^C))))`, which is
  behaviourally P*'s sibling `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))`. So the P* family *is* second-order prudence.
- *The positive form of order 2, `and(BOX(THEM(ME)),BOXD_L(THEM(^C)))`, never cooperates with itself,* at L = 1, 2, 3.
  Its own defection on ALLC appears only from world L + 1, so PA + Con^L cannot prove it.
- *Orders 1 and 2 together* (P12, P*1) do not self-cooperate with PA + Con. They self-cooperate with PA + Con², at
  sizes 13–14 (P*1b, P12b).
- *PrudentBot plus punishment of the self-prover's cooperators* (`PB_BTT`, size 15): not self-cooperating at PA + Con
  or PA + Con².

Each added order of prudence costs a Con level as well as size. This is the regress expressed in proof strength.

**Leak rates confirm Proposition 2** (`runs/drift_closure_rates.json`, static). Exits per mutation event from fixed
worlds, n = 8, free arm:

| world | N = 10⁴ | 10⁵ | per-N constant |
|---|---|---|---|
| FairBot | 4.85·10⁻⁵ | 4.85·10⁻⁶ | 0.485, of which ALLC 0.466 |
| PrudentBot | 1.02·10⁻⁶ | 1.02·10⁻⁷ | 0.0102 = μ(FB) + μ(BTT); the leak floor |
| P* | 3.11·10⁻⁷ | 3.11·10⁻⁸ | 3.1·10⁻³ |

The same arithmetic gives the order of the E2 plateau without any N-dependence: [μ(PB)/0.0102]/[μ(FB)/0.485] = 0.013,
counting direct entry from all-D only, against the measured 0.04. The difference is inflow from other cooperative
worlds, which this two-state arithmetic omits.

## Part 2. Mechanisms the propositions leave open

### Arms (`src/fringe.py`, `src/moat_limN.py`)

1. **free** (reference): the free modal arm, n = 6, 8, and n = 9 at N = 10⁵.
2. **boostPB** (labelled prior choice, a diagnostic of Proposition 2): PrudentBot gets FairBot's prior mass, as if it
   were a 3-node primitive; renormalized. Order-1 prudence, universal. n = 8.
3. **addP12b** (labelled grammar choice): P12b, which needs size 14 and PA + Con², is added to L_8 at FairBot's prior
   mass. Orders 1 and 2, parochial. n = 8.
   **addP12bsib** [after review, fable §2, astra §3]: P12b *and its same-size siblings*, each at FairBot's mass. The
   siblings put the first atom over {THEM(ME), THEM(THEM)} and the negated box over {^C, THEM(ME), THEM(THEM)}; two
   merge with others, leaving five classes. addP12b alone measures uneven language coverage: P12b's own THEM(THEM)
   siblings, which are suckerable and mutually cooperate with it, do not exist in L_8. addP12bsib is the fair test of
   whether high-order prudence buys anything per unit of prior mass.
4. **Fringe arms.** Every program also meets a fixed background ν with weight δ:
   U′(x, y) = U(x, y) + δ·f(x), with f(x) = Σ_q ν(q)·u(x, q).
   - *Status:* the fringe does not evolve. These are ε→0 chains of a *modified game*, not the base model's ε→0
     object. The fringe stands in, heuristically and at leading order only, for the standing mutant fringe at finite
     ε (E3). [after review, fable §5] The real standing variance is resident-dependent (μ weighted by mutant
     lifetimes against the resident), which a frozen fringe omits. [after review, fable 1.4] Formally the fringe is an
     opponent-independent price c(x) = −δf(x) that charges constants.
   - *Variants:*
     - **D**: ν = DefectBot. f = u(x, D) charges cooperation with D, so it charges the shadow by δ(P − S) = δ and
       charges nothing else. FairBot, PrudentBot, P* and D all get f = −1.
     - **CD**: ν = ½ ALLC + ½ DefectBot. It also rewards exploiting ALLC. f is 0 for D, PB and P*, −0.5 for FairBot,
       −1 for ALLC. So FairBot pays δ/2 to enter all-D: a barrier like a price of c = δ/2.
     - **μ**: ν = the mutation prior (diagnostic). Full support, so on-path-neutral pairs are generically split. f:
       D 0, P* −0.011, PB −0.027, FairBot −0.49, ALLC −1 (n = 8).
   - *Grid:* δ ∈ {10⁻³, 10⁻²} for D, CD and μ (μ at 10⁻³ added after review, fable 3.1), at n = 6, 8. Also n = 9 for
     D and μ at N ∈ {10⁴, 10⁵}.
   - [after review, astra §3, fable 3.2] *Larger N:* D, CD and μ at n = 8, δ = 10⁻², N = 3·10⁵; μ at n = 6, δ = 10⁻²,
     N = 3·10⁵ and 10⁶.
5. **Dpath** (n = 6): the D fringe along δ_N = 10/N (wδN = 3), the boundary path. The shadow's edge then keeps a fixed
   suppression factor.

N ∈ {10², 10³, 10⁴, 3·10⁴, 10⁵} unless stated, w = 0.3, `eager_poly=False`, θ = 10⁻⁶. [after review] Repeats at
θ = 10⁻⁸ for D and μ (n = 8, δ = 10⁻², N = 10⁵). 102 cells, at most 3 workers.

### Statistics
- P(C,C), π(all-D), and π split into families over monomorphic self-cooperating states:
  - *FBfam:* cooperates with FairBot and with ALLC;
  - *prudent:* cooperates with FairBot, defects on ALLC;
  - *rival:* defects on FairBot.
- *Network exit:* the stationary flux from cooperative states to the rest, per unit of cooperative mass and per
  mutation event. Its N-slope is the test of "faster than 1/N". *Network entry* is the reverse flux.
- Local odds slopes; X, blocks and rival share as in `runs/cert_pricing.md`.
- Exits from the FairBot, FB1, PB, P*, BTT and P12b worlds, split strict / neutral / other.
- Terminal and near-closed classes, absorption error, polymorphic flow and cut flow. Where two or more near-closed
  cooperative classes hold the mass, the split between them is an absorption lottery, not π (rule 5), and is labelled
  as such. [after review, fable §4] Where two classes are both closed inside the grid, their split is set by entry and
  by a ratio of two suppressed leaks; it is reported as such even when the chain finds one terminal class.
- [after review, fable 1.2] *Kept exit share:* for every state with π > 10⁻³, the share of its exit weight whose
  targets were expanded. Every class is a seed of `explore`, and seeds are expanded in its eager phase, so every
  monomorphic state is expanded (the smoke cell expanded 471 of 471). θ-pruning can drop only polymorphic targets. The
  diagnostic checks this, and the θ = 10⁻⁸ repeats check its effect.

### Static local estimates (validated on the free arm)
The local estimate reproduces the published free-arm values: n = 6: 0.1693 / 0.3452 / 0.5869 / 0.7068 / 0.8137; n = 8:
0.1821 / 0.3707 / 0.6172 / 0.7246 / 0.8135. Published: 0.1693 / 0.3453 / 0.5869 / 0.7068 / 0.814 and 0.1821 / 0.3707 /
0.6172 / 0.7246 / 0.8135.

| arm | n | δ | P(C,C) at N = 10² / 10³ / 10⁴ / 3·10⁴ / 10⁵ | families FB / prudent / rival at 10⁵ | network-exit slope 3·10⁴→10⁵ |
|---|---|---|---|---|---|
| free | 8 | 0 | 0.182 / 0.371 / 0.617 / 0.725 / 0.814 | 0.86 / 0.01 / 0.12 | −0.92 |
| boostPB | 8 | 0 | 0.752 / 0.924 / 0.976 / 0.986 / 0.992 | 0.04 / 0.95 / 0.00 | −0.99 |
| addP12b | 8 | 0 | 1 − P = 1.5·10⁻³ / 2.6·10⁻⁵ / 7.7·10⁻⁶ / 4.4·10⁻⁶ / 2.4·10⁻⁶ | 0 / 0 / 1.00 | −1.00 |
| D | 6 | 10⁻² | 0.189 / 0.730 / 0.9885 / 0.9933 / 0.9963 | 1.00 / 0 / 0 | −1.00 |
| D | 6 | 10⁻³ | 0.171 / 0.376 / 0.890 / 0.9928 / 0.9963 | 1.00 / 0 / 0 | −1.05 |
| D | 8 | 10⁻² | 0.203 / 0.756 / 0.9986 / 0.9991 / 0.9995 | 0.05 / 0 / 0.95 | −0.98 |
| D | 8 | 10⁻³ | 0.184 / 0.403 / 0.894 / 0.9972 / 0.9995 | 0.05 / 0 / 0.95 | −1.93 (transient) |
| CD | 6 | 10⁻² | 0.176 / 0.509 / 0.9855 / 0.9898 / 0.9914 | 1.00 / 0 / 0 | −1.00 |
| CD | 8 | 10⁻² | 0.189 / 0.541 / 0.9990 / 0.9995 / 0.9998 | 0.01 / 0.78 / 0.21 | −1.56 |
| CD | 8 | 10⁻³ | 0.183 / 0.385 / 0.774 / 0.968 / 0.9997 | 0.03 / 0.40 / 0.57 | −4.3 (transient) |
| μ | 6 | 10⁻² | 0.176 / 0.512 / 0.9863 / 0.9914 / 0.9954 | 1.00 / 0 / 0 | −1.37 |
| μ | 8 | 10⁻² | 0.189 / 0.544 / 0.9986 / 0.9995 / 1 − 3.1·10⁻⁵ | 0.00 / 0.18 / 0.82 | −3.1 |
| Dpath | 6 | 10/N | 0.517 / 0.730 / 0.890 / 0.933 / 0.962 | 1.00 / 0 / 0 | −1.00 |
| D | 9 | 10⁻² | — / — / 0.9980 / 0.9988 / 0.9993 | 0.07 / 0 / 0.93 | −0.96 |
| μ | 9 | 10⁻² | — / — / 0.9985 / 0.9995 / 0.9999 | 0.01 / 0.61 / 0.39 | −2.2 |
| *added after review* | | | | | |
| addP12bsib | 8 | 0 | 0.966 / 0.9887 / 0.9959 / 0.9972 / 0.9982 | 0.02 / 0.19 / 0.79 | −0.84 |
| μ | 6 | 10⁻³ | 0.170 / 0.359 / 0.759 / 0.973 / 0.9963 | 1.00 / 0 / 0 | −2.2 (shadow switch-off) |
| μ | 8 | 10⁻³ | 0.183 / 0.386 / 0.776 / 0.968 / 0.9995 | 0.04 / 0.56 / 0.40 | −4.0 (shadow switch-off) |
| μ | 6 | 10⁻² | 1 − P at 3·10⁵ / 10⁶: 1.3·10⁻³ / 3.4·10⁻⁵ | 1.00 / 0 / 0 (BTT 0.98 at 10⁶) | −2.4 (10⁵→3·10⁵), −5.7 (→10⁶) |
| D | 8 | 10⁻² | 1 − P at 3·10⁵: 2.9·10⁻⁴ | 0.05 / 0 / 0.95 | −0.97 (10⁵→3·10⁵) |
| CD | 8 | 10⁻² | 1 − P at 3·10⁵: 1.2·10⁻⁴ | 0.00 / 0.86 / 0.14 | −1.8 (10⁵→3·10⁵) |
| μ | 8 | 10⁻² | 1 − P at 3·10⁵: 9.5·10⁻¹⁰ | 0.00 / 0.00 / 1.00 | −8.5 (10⁵→3·10⁵) |

[after review] With its siblings present, P12b's advantage per unit of prior mass collapses: addP12bsib's odds are 7×
boostPB's at N = 10³ and 4.4× at 10⁵, against about 3,000× for addP12b alone. The prudent share rises with N in
addP12bsib (0.01 → 0.19), and the network exit slope over [3·10⁴, 10⁵] is −0.84, not yet at −1.

**Generalized closure** (static, `moat_static.closure`, at tolerance 10⁻¹²): a class is closed if no path of
sub-exponential transitions from it reaches a non-self-cooperating class. [after review, fable 1.3] Under μ, closure
is a crossover at N* ≈ 1/(wδΔf). Many mate gaps are 10⁻⁷–10⁻⁴, so a closed class at tolerance 10⁻¹² is closed only
for N ≫ N*. At the dynamical tolerance 3.3·10⁻⁵ (wgN = 1 at 10⁵), only P* at n = 8 is closed (all its mate gaps are
≤ −5·10⁻³). PB's closure at n = 8 rests on one edge at gap −1.6·10⁻⁵. P* at n = 9 has a mate at gap −3·10⁻⁸ that the
chain treats as exactly neutral, so it is not closed in the driver's object. Under D and CD the mate gaps are exactly 0
or ≥ δ/2, so static closure and the chain agree.
- *None* in the free arm at n ≤ 11, nor under the D or CD fringes at n ≤ 10.
- *Under μ at n = 6:* FairBot, FB1 and BTT are closed.
- *Under μ at n = 8–10:* PrudentBot and P* are closed, and, at n = 10, one more PB-like class.

So the D and CD fringes leave every family a residual 1/N leak through rare non-D-suckerable mates. Their faster
slopes in the table are transients, while the shadow edge switches off at wδN ≈ 1 or while FairBot's entry barrier
bites. Only μ creates closed classes.

## Verdicts

[after review, astra §1] Three kinds of claim, kept apart:
- *theorem checks* (Lemma 1, Corollary 1): static, already reported above, and not scored by the chain;
- *asymptotic mechanism tests* (exponents and slopes of the network exit);
- *finite-N performance numbers* (P(C,C), family shares). These are cross-checks of the driver against the unpruned
  monomorphic chain (fable 1.1), with tolerances for polymorphic states and pruning.

1. **The references reproduce.** free n = 6 and n = 8 are within 10⁻³ of the published values at every shared N. free
   n = 9 at N = 10⁵ is 0.814 ± 0.01. This checks the driver.
2. **A prior choice changes the constant and the family, not the exponent** (boostPB, universal).
   - *P(C,C):* 0.752 / 0.924 / 0.976 / 0.986 / 0.992, with ±0.01, or 1 − P within a factor of 1.5.
   - *Family:* prudent ≥ 0.90 of the cooperative mass at every N ≥ 10³.
   - *Slopes:* network exit over [3·10⁴, 10⁵] is −1.0 ± 0.1; odds slope 0.50 ± 0.08.
   - *Leak floor:* PB's world exits are neutral and equal (0.0102 ± 10%)/N, half of it into FairBot.
3. **High-order prudence buys nothing per unit of prior mass once its own siblings are in the language.**
   [revised after review, fable §2]
   - *addP12b (as run, uneven coverage):* 1 − P(C,C) within a factor of 2 of 1.5·10⁻³ / 2.6·10⁻⁵ / 7.7·10⁻⁶ /
     4.4·10⁻⁶ / 2.4·10⁻⁶; rival ≥ 0.99; network exit slope over [10⁴, 10⁵] −1.0 ± 0.1. Reported as the coverage
     artefact it is.
   - *addP12bsib (fair test):* 1 − P(C,C) within a factor of 2 of 3.4·10⁻² / 1.1·10⁻² / 4.1·10⁻³ / 2.8·10⁻³ /
     1.8·10⁻³. Its odds are between 2× and 20× boostPB's at every N ≥ 10³ (estimate 4–7×), against about 3,000× for
     addP12b. Rival ≥ 0.7 at every N, with the prudent share rising with N.
   - *Slope:* addP12bsib's network exit over [3·10⁴, 10⁵] is in [−1.1, −0.7].
4. **The D fringe closes the shadow edge only. n = 6 stays universal; the exponent stays 1/2.**
   - *Family:* FBfam ≥ 0.99 of the cooperative mass.
   - *P(C,C), δ = 10⁻²:* 0.9885 / 0.9933 / 0.9963 at N = 10⁴ / 3·10⁴ / 10⁵, with 1 − P within a factor of 1.5.
   - *Slopes:* network exit over [3·10⁴, 10⁵] is −1.0 ± 0.1 at δ = 10⁻².
   - *Exits:* ALLC takes < 0.01 of FairBot's exits at N ≥ 10⁴ (δ = 10⁻²). FairBot's exits are neutral, at
     (0.0186 ± 20%)/N, into FB1, BTT and the faked probes.
5. **The D fringe at n = 8 hands the network to the parochial P\* family, still at exponent 1/2.**
   - *Family:* rival ≥ 0.85 of the cooperative mass at N ≥ 10⁴ for δ = 10⁻², and ≥ 0.75 at N ≥ 3·10⁴ for δ = 10⁻³.
     The top cooperative state is in the P* family. [after review, fable §2] A two-state balance gives about 0.80;
     the unpruned chain gives 0.93–0.95. The run reports which mates carry P*'s residual leak of 1.4·10⁻⁶ and whether
     they feed back into P*.
   - *Slopes:* network exit over [3·10⁴, 10⁵] is −1.0 ± 0.15, and over [10⁵, 3·10⁵] −1.0 ± 0.1, at δ = 10⁻².
   - *P(C,C), δ = 10⁻²:* 0.9986 / 0.9991 / 0.9995, with 1 − P within a factor of 2.
   - *n = 9:* rival ≥ 0.85 at both N.
6. **The CD fringe at n = 8 gives two rival blocks, moving toward the prudent one.**
   - *Families at δ = 10⁻², N ≥ 10⁴:* prudent and rival each ≥ 0.1 of the cooperative mass up to N = 10⁵; FBfam ≤ 0.05;
     prudent rising with N (0.45 / 0.61 / 0.78 / 0.86 ± 0.12 at 10⁴ / 3·10⁴ / 10⁵ / 3·10⁵).
   - *Structure:* X ≤ 0.85 and rival share ≥ 0.1 at 10⁴ ≤ N ≤ 10⁵.
   - *P(C,C):* ≥ 0.998 at N ≥ 10⁴.
7. **The CD fringe at n = 6 shows FairBot's entry barrier.**
   - *Slopes:* at δ = 10⁻², the odds slope over [3·10⁴, 10⁵] is ≤ 0.35 (estimate 0.14; the barrier exp(−wδ²N/8)
     alone gives about 0.28, fable). FairBot pays δ/2 against D, and at n = 6 there is no barrier-free entrant.
   - *P(C,C):* 0.9898 / 0.9914 ± 0.005 at 3·10⁴ / 10⁵.
8. **The μ fringe closes families as a crossover, and the closed family it ends on is parochial.**
   [restated after review, fable 1.3]
   - *n = 8, δ = 10⁻²:*
     - network exit slope over [3·10⁴, 10⁵] ≤ −1.5 (estimate −3.1), and over [10⁵, 3·10⁵] ≤ −3 (estimate −8.5);
     - 1 − P(C,C) at 10⁵ ≤ 2·10⁻⁴;
     - both prudent and rival ≥ 0.1 of the cooperative mass at N = 10⁴ and 3·10⁴;
     - rival ≥ 0.9 at 3·10⁵ (estimate 1.000), when only P* is closed at the dynamical tolerance;
     - the split at 10⁵ is reported, not scored.
   - *n = 9:* not scored (P* is not closed in the driver's object); reported.
   - *δ = 10⁻³ (control):* the window slope is dominated by the shadow edge switching off (wδN·½ ≈ 15 at 10⁵), so it
     is reported, not scored.
9. **The μ fringe at n = 6 gives one universal network with an exit faster than 1/N, as a crossover.**
   - *Family:* FBfam ≥ 0.99 at every N ≥ 10⁴, up to 10⁶.
   - *Slopes:* network exit over [10⁵, 3·10⁵] ≤ −2 and over [3·10⁵, 10⁶] ≤ −3 (estimates −2.4, −5.7). If not, the
     closure test is wrong (fable 3.2).
   - *P(C,C):* 0.9914 / 0.9954 ± 0.005 at 3·10⁴ / 10⁵; 1 − P ≤ 10⁻⁴ at 10⁶.
   - *Why:* n = 6 has no parochial alternative to close instead. At n ≥ 8 (verdict 8) the same fringe ends on P*.
10. **The boundary path** (Dpath, n = 6).
    - *P(C,C):* 0.890 / 0.933 / 0.962 ± 0.01 at 10⁴ / 3·10⁴ / 10⁵.
    - *Slopes:* odds slope 0.50 ± 0.05 over [10⁴, 10⁵]; network exit slope −1.0 ± 0.05.
    - *Constant:* the odds are 5.8 ± 1 times the free arm's at N ≥ 10⁴ (fable's hand estimate 5.2).
11. **The open problem stays open at n ≥ 8.** No cell at n ≥ 8 has both:
    - (a) FairBot-cooperating families (FBfam + prudent) holding ≥ 0.95 of the cooperative mass, with rival < 0.05;
    - (b) a network exit slope ≤ −1.3 over its last two N.

    This is a finite-N mechanism criterion, not a test of Corollary 1 (astra).
12. **Numerics.**
    - No indeterminate transitions.
    - Absorption error < 10⁻⁶ and cut flow < 10⁻⁵ in every cell.
    - Kept exit share ≥ 0.99 for every state with π > 10⁻³.
    - The θ = 10⁻⁸ repeats match θ = 10⁻⁶: 1 − P(C,C) within 5% and family shares within 0.01.
    - Polymorphic flow < 10⁻³ of the mass, except where reported.

## Falsifiers
- *Of Proposition 2's dynamic content* (a prior choice changes constants only): boostPB has a network exit slope
  outside [−1.15, −0.85] over [3·10⁴, 10⁵].
- *Of "prudence buys nothing per unit of prior mass"* (verdict 3): addP12bsib's odds exceed boostPB's by more than 50×
  at any N ≥ 10³.
- *Of "the D fringe hands the network to P\*"*: D, n = 8, δ = 10⁻², has rival < 0.5 at any N ≥ 10⁴.
- *Of "the D fringe keeps exponent 1/2"*: a D-fringe cell at δ = 10⁻² (n = 6 or 8) has a network exit slope ≤ −1.3
  over [3·10⁴, 10⁵] or [10⁵, 3·10⁵].
- *Of "μ closure is a crossover"*: the μ fringe at n = 6 does not steepen past −2 by [3·10⁵, 10⁶], or at n = 8 has a
  slope > −1.2 over [3·10⁴, 10⁵].
- *Of the open-problem statement:* a cell at n ≥ 8 meets both (a) and (b) of verdict 11.

## What each outcome would mean
- **If 2–5 and 11 hold.**
  - *In the pure game,* universality and drift-closure are exclusive by Corollary 1. Rates follow Proposition 2:
    behavioural prudence of any order, and prior or grammar choices, change only constants and which family holds the
    mass. Per unit of prior mass, FairBot has the smallest leak of any unsuckerable class at n ≤ 11, and high-order
    prudence gains nothing once its siblings are present.
  - *Charging the shadow* (the D fringe) is not a copy subsidy and not self-recognition. It does not change the
    exponent, because every family keeps a residual leak through rare mates. At n ≥ 8 it hands the network to the
    least leaky family, which is parochial. [after review, fable §4] That is a leak-ratio effect with a 10⁻⁶
    denominator, and one extra sibling could change it; it illustrates the trade-off and does not prove it.
  - *So:* without moats, "one network" and "faster than 1/N" are not obtained together at n ≥ 8. The obstruction is
    proved for the pure game (Corollary 1, Proposition 2) and for prices that leave constants free (Proposition 3).
- **If 8 and 9 hold.** A full-support fringe produces closed families as a crossover in N: the first exits faster than
  1/N without copy subsidies or self-recognition. It is an exogenous fitness ordering, not a moat [after review, fable
  1.4]. It favours the family with the highest fringe payoff. That family is the parochial P* at n = 8, because
  exploiting the fringe's naive members pays more than cooperating with its few reciprocators. At n = 6, where no
  parochial alternative exists, the same fringe gives the one universal network with a fast exit. The crossover N
  depends on prior masses that shrink with n, so μ-closure is not uniform in n.
- **If 5 fails** (P* does not take over under the D fringe). The unpruned chain says it should, so the first suspect is
  the driver (pruning or polymorphic states), not the theory [corrected after review, fable 1.1].
- **If a cell meets verdict 11's (a) and (b) at n ≥ 8.** The open problem would be solved by that mechanism. Check
  that it is not a local incumbency advantage in disguise (Proposition 3).

## Re-openings of REJECTED.md
- **"Standing variance (finite εN) as the rescue. Closed."** The fringe arms re-open it in a different form: a frozen
  background inside the ε→0 chain, not a finite-εN simulation. *New evidence:* E3 (modal arm at finite εN, 0.99,
  with a defector fringe pruning the shadow). Proposition 3 identifies the fringe, an opponent-independent price on
  constants, as the one mechanism class it does not cover. The fringe chain is labelled a modified game, not the base
  model's ε→0 object, and the frozen fringe omits the resident-dependence of real standing variance.
- **"Uniform prior as rescue" / "the prior isn't a free knob."** boostPB and addP12b are diagnostics of
  Proposition 2, labelled prior and grammar choices. They are not proposals to change μ.
- **"Non-exclusivity as the normative axiom."** Universality is reported as an evaluation only.

## Smoke test run before commit (declared)
- *D fringe, n = 8, δ = 10⁻², N = 10⁴, full chain* (driver check): P(C,C) 0.9986, rival family 0.934. The local
  estimate gave 0.9986 and 0.934. 471 states, 24 s.
