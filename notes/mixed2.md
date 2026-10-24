# Mixed actions in two-role games: the inspection game and Basic Endgame (notes, 2026-10-23)

Spec `specs/2026-10-23-two-role-mixed.md` (reviewed by gemini-4-argon, then gpt-6.1-sol in amended mode; both folded).
Builds on `specs/2026-10-23-rps-mixed.md`, `specs/2026-10-23-rps-priced.md`, `notes/rps.md`, `notes/rps-priced.md`.
§1 is written by hand before any code of this run and before any counted cell. §2 (choices where the spec is silent,
and deviations) is appended with the code, before any counted cell. Everything numerical in §1 is derived on paper from
the semantics of §1.0; the code is checked against it afterwards (tests), never the other way round. Where §1 uses a
pair that has a guard (a `coin` around a reader) the value is not derived by hand: such pairs are checked in the tests
against an independent exact-rational reference evaluator.

## 1. Hand derivations

### 1.0 Semantics used in the derivations

* **Roles.** Two fixed roles, one population per role. Role 0 is the inspector (inspection) or player I (Endgame); role 1
  is the inspectee or player II. A program is the body of one role. `THEM(ME)` run by a program a against opponent b is
  b's body run with b's opponent being a; `THEM(^B)` is b's body run against the lifted program B of a's own role. One
  depth counter per root evaluation, D = 12, each application consumes one level; an application met at depth 0
  forfeits (F), and the opponent's body inside an application runs on the remaining budget.
* **Action distributions.** `G(a, b)` is the distribution of a's action against b over (its two actions, F), computed
  exactly; the two players' coins are independent. In Endgame I's distribution is conditional on I's card (W with
  probability P = 1/3, L with 2/3). When II reads I, the simulation draws a *fresh* card independent of the real one, so
  II sees the card-averaged action distribution, and `cr` of II sees the joint (card, action) distribution.
* **`cr A`.** The exact best response to A's action distribution conditional on A acting (A being the opponent's action
  expression, normally `THEM(ME)`); ties within 1e-9 are broken by the reader's own fair coin; it forfeits with the
  forfeit mass of A. Endgame II's `cr` uses the joint (card, action) of the simulated I (the posterior that a bet is a
  bluff); if I never bets II is payoff-indifferent and the tie is broken by its coin. Endgame I's `cr` best-responds
  card by card.
* **`sr A`** (the matched control). One draw from A's distribution (the full run: card and action), then the pure best
  response to that draw, ties by own coin; `sr_k` draws k times and best-responds to the empirical distribution.
* **`if THEM(..) = α then A else B`** (the operator carries α; size = 1 + |Q| + |A| + |B|). The test draws one sample of
  Q, independent of the branches' coins; if Q forfeits the whole program forfeits.
* **Payoffs with forfeits.** A forfeiter plays its worst action against the realized opponent action (and realized
  card); the opponent receives the payoff of that profile. If both forfeit, each receives the worst entry of its own
  payoff table (inspection: inspector −4, inspectee −3; Endgame: −3 each). This makes mutual non-play the worst
  outcome in the game itself, as the RS asked (a mutual forfeit is not a free tie).
* **Price.** A program pays c per serial application level its root evaluation executes (§2 of `notes/rps-priced.md`
  extended: a coin or `card` counts the branch taken, `cr` counts the deepest branch of its exact computation, and
  `if` adds the test's depth to the chosen branch's). A forfeit along a chain pays exactly c·D. For every program of
  this section depth and serial work coincide.
* **Sizes.** Constants, `X` 1 node; `coin A B`, `card A B`: 1 + |A| + |B|; `cr A`, `sr A`: 1 + |A|; `THEM(ME)` 3;
  `THEM(^B)` 3 + |B|; `X` is the fair coin over the role's two actions, so `coin N X` (inspect with probability 1/4) has
  3 nodes.

### 1.1 The inspection game

**Payoffs** (inspector, inspectee): (I, C) = (−1, 0); (I, K) = (−1, −3); (N, C) = (0, 0); (N, K) = (−4, +1). With the
inspector inspecting with probability p and the inspectee cheating with probability q, independently,

    U_insp(p, q) = −p − 4(1 − p) q,          U_ee(p, q) = q (1 − 4p).

**Nash.** U_ee is indifferent iff p = 1/4; ∂U_insp/∂p = −1 + 4q is zero iff q = 1/4. The mixed equilibrium is
(p*, q*) = (1/4, 1/4) with payoffs (−1, 0) (check: −1/4 − 4(3/4)(1/4) = −1). It is the unique equilibrium (no pure
equilibrium: (I, C) invites N, (N, C) invites K, (N, K) invites I, (I, K) invites C).

**Commitment.** If p > 1/4 then U_ee < 0 for q > 0, so a best-responding inspectee complies and U_insp = −p. The
supremum over visible p is −1/4, not attained. At exactly p = 1/4 the reader is indifferent and its own coin gives
q = 1/2: U_insp(1/4, 1/2) = −1/4 − 4(3/4)(1/2) = −7/4. A reader that visibly reads a committed inspector is a best
responder; its action is C.

**The dyadic grid (blind programs, i.e. constants, `X`, `coin`).** `coin A B` has probability (p_A + p_B)/2 and size
1 + |A| + |B|; atoms I, N, X have p = 1, 0, 1/2 at size 1. Blind sizes are odd.
* size 1: {0, 1/2, 1};
* size 3: {1/4 (`coin N X`), 3/4 (`coin I X`)} plus the old values;
* size 5: odd multiples of 1/8: 1/8, 3/8, 5/8, 7/8 (3/8 is `coin X (coin N X)`);
* size 7: odd multiples of 1/16: 1/16, 3/16, **5/16** (`coin X (coin N (coin N X))`), 7/16, 9/16, ...;
* size 9: odd multiples of 1/32.

So with `X` an atom, p = 3/8 already exists at size 5, and at n = 8 (blind sizes up to 7) the **smallest expressible
p > 1/4 is 5/16** (commitment payoff −0.3125), then 3/8 (−0.375), 7/16, 1/2 (`X`, −0.5). The spec's text names 3/8
as the commitment point and counts denominators for fair binary coins without the atom `X`; both 5/16 and 3/8 are
reported beside 1/2, and the commitment reference is −5/16 (the value at the smallest grid point), with −3/8 as the
spec's.

**Named programs.** Inspectors: `I`, `N`, `X` (p = 1/2), `P14 = coin N X` (1/4), `P516` (5/16), `P38 = coin X (coin N X)`
(3/8), `RI = if THEM(ME) = K then I else N` (6 nodes; inspect iff a sampled inspectee cheats), `CRI = cr(THEM(ME))` (4;
inspect iff the cheat probability exceeds 1/4, p = 1/2 at 1/4). Inspectees: `C`, `K`, `X` (q = 1/2),
`CRC = cr(THEM(ME))` (comply iff p > 1/4, q = 1/2 at p = 1/4, cheat if p < 1/4), `RC = if THEM(ME) = I then C else K`
(6; a one-sample responder: q = 1 − p). `sr(THEM(ME))` is behaviourally identical to `RC` for the inspectee and to `RI`
for the inspector: a one-draw best response in this game is the conditional program.
A non-reading inspector has its own p, a non-reading inspectee its own q; a reader of a non-reader is a best response
to (or sample of) that probability. Reader against reader: each reads the other's reading, to the cap, and both forfeit
with probability 1.

**Payoff table** (inspector, inspectee), rows inspectors, columns inspectees; derived from U_insp, U_ee with the
effective (p, q):

| | C (q=0) | K (q=1) | X (q=1/2) | CRC | RC (q=1−p) |
|---|---|---|---|---|---|
| I (p=1) | (−1, 0) | (−1, −3) | (−1, −3/2) | (−1, 0) | (−1, 0) |
| N (p=0) | (0, 0) | (−4, 1) | (−2, 1/2) | (−4, 1) | (−4, 1) |
| X (p=1/2) | (−1/2, 0) | (−5/2, −1) | (−3/2, −1/2) | (−1/2, 0) | (−3/2, −1/2) |
| P14 (p=1/4) | (−1/4, 0) | (−13/4, 0) | (−7/4, 0) | (−7/4, 0) | (−5/2, 0) |
| P516 (p=5/16) | (−5/16, 0) | (−49/16, −1/4) | (−27/16, −1/8) | (−5/16, 0) | (−141/64, −11/64) |
| P38 (p=3/8) | (−3/8, 0) | (−23/8, −1/2) | (−13/8, −1/4) | (−3/8, 0) | (−31/16, −5/16) |
| RI (p=q) | (0, 0) | (−1, −3) | (−3/2, −1/2) | (−4, −3) | (−4, −3) |
| CRI | (0, 0) | (−1, −3) | (−1, −3/2) | (−4, −3) | (−4, −3) |

(The last two columns of RI and CRI are mutual forfeits at payoff (−4, −3). CRC against P14 is the tie, q = 1/2; RC
against P14 has q = 3/4.) Worked entries: P38 against K: U_insp = −3/8 − 4(5/8) = −23/8, U_ee = 1 − 4(3/8) = −1/2;
P516 against RC: q = 11/16, U_insp = −5/16 − 4(11/16)(11/16) = −141/64, U_ee = (11/16)(−1/4) = −11/64.

**Depths** (levels executed by the row program, the price is c times these): non-readers 0. `RI`, `CRI` against a
non-reader: 1; against a reader (`CRC`, `RC`, and each other): 12. `CRC`, `RC` against a non-reader: 1, against a
reader: 12. `sr_k(THEM(ME))` against a non-reader: k.

**Hand statics.** (i) Against any visible p > 1/4 the best response of every reader inspectee is C, so `CRC` is a
shadow of `C` there: equal game payoff (0), and at c > 0 `C` strictly dominates (`CRC` pays one level). (ii) The ladder:
against (P38, CRC), `CRC` and `C` earn 0 and `K` earns −1/2, so `K` does not invade and `C` is neutral at c = 0;
against (P38, C) the inspector `N` earns 0 against −3/8 and invades; against (N, C) the cheat `K` earns +1 against 0
and invades; against (N, K) the inspector `I` earns −1 against −4 and invades; against (I, K) `C` earns 0 against −3
and invades; against (I, C) `N` earns 0 against −1 and invades: (I, C) → (N, C) → (N, K) → (I, K) → (I, C) is a strict
best-response cycle among constants, the two-population matching-pennies cycle.

### 1.2 Basic Endgame

**Payoffs to I** (P = 1/3, a = 1, b = 2): check with a winner +1, with a loser −1; bet and fold +1; bet and call +3
with a winner, −3 with a loser; II receives the negative. For I's strategy (w, l) = (P(bet | winner), P(bet | loser))
and II's call probability q, independently,

    U_I(w, l, q) = −1/3 + (2/3) w q + (4/3) l (1 − 2q).

(Derivation: winner, prob 1/3: w[3q + (1 − q)] + (1 − w) = 1 + 2wq. Loser, prob 2/3: l[−3q + (1 − q)] − (1 − l) =
l(2 − 4q) − 1.)

**Equilibrium.** U_I is independent of q iff (2/3) w = (8/3) l, i.e. l = w/4; U_I is increasing in w for q > 0, so w = 1
and l = 1/4. II is indifferent over l iff (4/3)(1 − 2q) = 0, so q = 1/2. The value is U_I(1, 1/4, q) = −1/3 + 2q/3 +
(1/3)(1 − 2q) = 0 (the paper's 2aP(2a+2b)/(2a+b) − a with these numbers is 2(1/3)(6)/4 − 1 = 0). With a loser, I bluffs
with probability π = (b/(2a+b)) P/(1−P) = (1/2)(1/2) = 1/4; II calls with probability 1 − b/(2a+b) = 1/2. The
all-strategies-active case applies (P = 1/3 < 2/3).

**The equilibrium programs.** I: `EQ = card BET (coin X CHECK)` (5 nodes: the loser bets with probability
(1/2)(1/2) = 1/4); the spec's 7-node spelling `card BET (coin (coin BET CHECK) CHECK)` is the same behaviour. II: `X`
(call 1/2).

**Named programs.** I: `BET`, `CHECK`, `XI` (blind coin, w = l = 1/2), `HON = card BET CHECK` (w = 1, l = 0),
`BL = card BET BET` (behaves as `BET`), `EQ`, `EXP = card BET cr(THEM(ME))` (6; the loser bets iff II's call
probability is below 1/2, tie at 1/2), `CRI = cr(THEM(ME))` (4; card by card: winner bets iff q > 0, loser bets iff
q < 1/2, ties by coin). II: `CALL`, `FOLD`, `X`, `CRII = cr(THEM(ME))` (4; calls iff 4 l > w, tie at 4 l = w),
`RII = if THEM(ME) = BET then CALL else FOLD` (6; calls with probability P(sampled I bets) = w/3 + 2l/3),
`SRII = sr(THEM(ME))` (4; one draw of (card, action): bet by a winner → FOLD, by a loser → CALL, check → coin, so
q = 1/2 + l/3 − w/6).

**Payoff to I** (row I program, column II program), by U_I with the effective q:

| | CALL (q=1) | FOLD (q=0) | X (q=1/2) | CRII | RII | SRII |
|---|---|---|---|---|---|---|
| BET (1,1) | −1 | +1 | 0 | −1 | −1 | −1/3 |
| CHECK (0,0) | −1/3 | −1/3 | −1/3 | −1/3 | −1/3 | −1/3 |
| XI (1/2,1/2) | −2/3 | 1/3 | −1/6 | −2/3 | −1/6 | −1/4 |
| HON (1,0) | 1/3 | −1/3 | 0 | −1/3 | −1/9 | −1/9 |
| EQ (1,1/4) | 0 | 0 | 0 | 0 | 0 | 0 |
| EXP | 1/3 | 1 | 0 | −3 | −3 | −3 |
| CRI | 1/3 | 1 | 0 | −3 | −3 | −3 |

(CRII's q: BET 1, CHECK 1/2, XI 1, HON 0, EQ 1/2. RII's q: BET 1, CHECK 0, XI 1/2, HON 1/3, EQ 1/2. SRII's q: BET 2/3,
CHECK 1/2, XI 7/12, HON 1/3, EQ 5/12. EXP and CRI against a non-reader: EXP has w = 1 and l = 1, 0, 1/2 at q = 0, 1,
1/2, CRI has w = 1/2, 1, 1 at q = 0, 1, 1/2... precisely CRI: q=1: (w, l) = (1, 0); q = 0: (1/2, 1); q = 1/2: (1, 1/2).
The last three columns of EXP and CRI are mutual forfeits, −3 to I and −3 to II.) II's payoff is −U_I except in a
mutual forfeit.

**Minimax checks.** `EQ` earns exactly 0 against every non-forfeiting II program (U_I is independent of q when l = w/4,
w = 1, and EQ does not read, so no II program can fail to terminate against it). II's `X` earns −U_I(w, l, 1/2) =
(1 − w)/3 ≥ 0 against every I program that terminates, whatever l, with equality iff w = 1: II's coin gains strictly
when I checks a winner (`CHECK`: +1/3, `XI`: +1/6). A reading I cannot beat the coin: a sample of X's action is
independent of X's real action.

**Depths.** Non-readers 0. `CRII`, `RII`, `SRII`, `CRI` against a non-reader: 1; `EXP` against a non-reader: the winner
branch costs 0 and the loser branch 1, so the expected depth is (2/3)(1) = 2/3 under the real card; reader against
reader: 12.

### 1.3 What this section fixes for the tests

* Both payoff tables (§1.1 and §1.2) to 10⁻⁹, the effective-q formulas of every II reader against every named I
  program, the Nash and Endgame equilibrium identities, the grid of §1.1, and the depth entries.
* The posterior in II's `cr`: indifference at (w, l) = (1, 1/4), call iff 4l > w, with the P(BET) = 0 tie.
* The fresh card in simulation: `RII` and `SRII` against `HON` use w/3 + 2l/3 and 1/2 + l/3 − w/6, not the real card.
* The price at c = 0 reproduces the game tables; the mutual-forfeit entry (−4, −3) / (−3, −3).
