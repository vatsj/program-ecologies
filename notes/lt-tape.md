# A private random tape in the realizable language (notes, 2026-10-24)

Spec `specs/2026-10-24-realizable-randomizer.md` (reviewed by gpt-6.1-sol, then gemini-4-argon in amended mode; both
folded). Builds on `notes/realizable-language.md` (L_T and K_T, milestone 1), `notes/certificates-as-code.md` (milestone
4), `notes/rps.md`, `notes/rps-priced.md` and `notes/mixed2.md` (the DSL games this transfers). §1 is written by hand
before any code of this run and before any counted cell; nothing in §1 has been run. §2 (choices where the spec is
silent, and deviations) is appended with the code, before any counted cell. Everything numerical in §1 was derived on
paper from the semantics of §1.0; the code is checked against it afterwards (tests), never the other way round.

## 1. Hand derivations

### 1.0 Semantics used in the derivations

**Terms and steps.** As L_T (`src/lt.py`): untyped call-by-value de Bruijn λ-calculus, small-step, one step per
contraction (β, `if`, `eq`, `fst`, `snd`, `mk`, ...). A program is `λme.λthem. BODY`; the play of p against q is the
value of `p ⌜p⌝ ⌜q⌝`, so **every evaluation starts with 2 β-steps** and a constant program costs exactly 2. A node is
any tuple of a term (`lam`, `app`, `if`, `con`, `nat`, `pair`, `eq`, `tape`, `mk`, `prove`, `prp`, `chk`, `hq`, `run`, `v`,
`quote`); sizes below count nodes this way. Charging is the **search-charged** semantics of milestone 1: a `prove` costs
W (the number of node expansions of the frozen exhaustive K_T search) in place of one step, charged to the global fuel K
and to every enclosing sim; a call whose cost exceeds any enclosing counter times out (the whole play is ⊥ if the global
counter, `TO` if a sim's). The price is c per step of the program's own evaluation (including every step it spends
inside simulations, searches, enumerations and checks). A play that does not end in an action constant (fuel
exhausted, stuck, another value) is a **forfeit**.

**The private tape.** At the start of each root evaluation the runtime draws m independent uniform digits over an
alphabet {0, ..., r−1}: (r, m) = (3, 3) for RPS, (2, 3) for inspection. `tape i` (i < m) returns digit i; the first
read of position i in an invocation draws it, later reads of i in the same invocation return the same digit (reads
cost 1 step each, repeated or not). **Randomness is indexed by (invocation, position).** An invocation is a root
evaluation or one `run`; `run k x y` creates a new invocation with its own fresh m digits independent of everything
else, so a simulation samples and cannot predict. The opponent's quote never contains a tape. The two players'
root evaluations are separate invocations on independent tapes, so **the two actions are independent given the
programs**: a pair's joint outcome is the product of the two marginals, and everything below is computed per player.
A program's own evaluation is a finite random decision tree over the digits it actually reads; its leaves are
*cylinders* (prefixes in order of first read) of weight r^(−length).

**Lazy mixers.** Over m = 3 binary digits, `M{j}` (j = 1..7) plays I (inspector) or K (inspectee) iff v = 4d₀ + 2d₁ + d₂
< j, with probability j/8, implemented as the *shortest* decision tree: read digit ℓ only if the cylinder so far
straddles j. A decision is `if eq(tape ℓ, 0) then <digit 0 subtree> else <digit 1 subtree>`: **3 steps** (tape read,
`eq`, `if`), 5 nodes (`if`, `eq`, `tape`, `nat ℓ`, `nat 0`). A tree with ℓ leaves has ℓ−1 decisions, so BODY has 6ℓ−5 nodes
and a mixer program 6ℓ−3 nodes. A leaf at depth d costs 2 + 3d steps. (Mixer = the shortest tree is a choice, §2; the
cost difference to a full-read tree is the route comparison of §1.4.)

**Counted probability.** For a state s (a program pair at a fuel K) let Ω be the padded space of all invocations' m
digits; the evaluation of s is a finite random tree; pr(s, a) is the weight of the cylinders whose leaf is the action
a, an exact rational (`fractions.Fraction`). The threshold is written k/den with den = r^m (8 or 27); the padded
exponent M of the spec only matters for denominators and is absorbed by exact rationals. Two proof routes, both
implemented as charged primitives:

* `prp b x y a k` (**enumeration**): replays the evaluation of x against y on *every* leaf of the decision tree,
  from scratch, under the same fuel K and the same charging as actual play; returns T iff pr ≥ k/den. **Charge =
  1 + Σ over all leaves of (1 + steps of the leaf's replay)**, capped at b (over the cap: F, charge b). A `prp`
  reached inside a replay (nested enumeration) returns F for 1 step: an enumeration does not enumerate.
* `chk x y a k` (**certificate check**): x must be a *carrier* `λme.λthem. (λcerts. BODY) CERTS` whose literal CERTS is
  `(stamp, ((a, (prefix₁, prefix₂, ...)), ...))` with prefixes lists of digits and stamp the fuel K the certificate is
  minted for. The checker (i) rejects unless stamp = the running K, (ii) replays x against a **wildcard opponent** (a
  poison value that fails the replay if any operation touches it), which makes the certificate opponent-generic and
  verifies that the replay never reads the opponent, (iii) replays each listed prefix with those digits forced in order of
  first read (never fresh draws), requiring that the replay ends within K steps in the action a and consumes *exactly*
  the prefix (no unread digits, none missing), (iv) rejects duplicates and any prefix that is a prefix of another (disjoint
  cylinders), and (v) accepts iff Σ r^(−length) ≥ k/den. **Charge = 1 + Σ over listed prefixes of (1 + steps of the
  replay).** Only the a-producing leaves need be listed (a `≥` certificate), so the check pays for fewer replays than
  the enumeration. A non-carrier fails at once (charge 1).

**Reasoning in K_T (for-all-tapes atoms).** The calculus keeps all rules of K_T (EvR/EvL, PrvR/PrvL, BoxEq, Nec, JLöb).
A state is (term, store) with the store a partial assignment of (invocation, position) ↦ digit; the atom ⟨s⟩⇒a is true iff
**for every tape** the idealized evaluation of s reaches a (prove steps resolved by box truth). When the next redex of s
is `tape i` with (invocation, i) unassigned, the atom has r children (the state with each digit assigned) and

    truth(⟨s⟩⇒a) = ∧_d truth(⟨s_d⟩⇒a),

an equivalence. Two new rules express it, both sound because they are this equivalence: **TapeR** (premises Γ ⊢ Δ, ⟨s_d⟩⇒a
for all d; conclusion Γ ⊢ Δ, ⟨s⟩⇒a) and **TapeL** (Γ, ⟨s_0⟩⇒a, ..., ⟨s_{r−1}⟩⇒a ⊢ Δ gives Γ, ⟨s⟩⇒a ⊢ Δ). The rest of the
soundness proof is unchanged because the other rules mention atoms only through their truth (evaluation steps) and
boxes only through provability in the standard model. A tape-reading program is therefore *derivably* playing a only if
every branch does: a uniform mixer's atom ⟨X plays R⟩ is not derivable, a constant's is. A `prp` or `chk` redex inside an
idealized atom is **opaque**: the atom has no rule, so it is neither derivable nor refutable (not "stuck", which would make
its negation derivable and unsound); its truth, for the soundness audit, is computed by the same enumeration. `hq` is a
deterministic step. The simulator leak of milestone 1 (a sound reader's idealized proof about a simulator's play versus
the simulator's fuel-limited real run) is still present, because K_T's atoms are idealized in the cost of `prove`.

**Pseudo-random control.** `hq m q`: a deterministic hash of the canonical encoding of the quoted value q, mod m, at a
cost of one step per node of q (a hash of the opponent's quote is a function of its source: predictable by a simulator
that can afford its cost). Hash digit i of a program is `hq r (i, ⌜opponent⌝)`.

**Payoffs and forfeits.** RPS: +1 / −1 / 0; a forfeit loses to every action and ties with a forfeit. Inspection
(inspector, inspectee): (I, C) = (−1, 0), (I, K) = (−1, −3), (N, C) = (0, 0), (N, K) = (−4, 1). With inspection
probability p and cheating probability q, independently,

    U_insp(p, q) = −p − 4(1 − p) q,       U_ee(p, q) = q (1 − 4p).

A forfeiter plays its worst action against the realized opponent action (the opponent gets the payoff of that
profile); if both forfeit each gets the worst entry of its own table (−4 inspector, −3 inspectee) (`notes/mixed2.md`
§1.0). **Price:** c per step; c₀ = 0.12 / K₀ so that exhausting the fuel K₀ costs 0.12 (K₀ is fixed in §2 after
measuring); c = 0 is the control. **Selection uses the exact expected net payoff over tapes** (game payoff − c × expected
steps), not sampled encounters.

### 1.1 The grammar (template families; the full list is the code's catalogue, sizes by the formulas of §1.0)

Inspection, inspector (20 templates): constants `I0`, `N0` (3 nodes); `M{1..7}` (I with probability j/8; by the formula 6ℓ−3 with
ℓ = 4, 3, 4, 2, 4, 3, 4 leaves for j = 1..7: 21, 15, 21, 9, 21, 15, 21 nodes); carriers `CARR{1,2,3,4,6}`
(a mixer plus a certificate for the action I, §1.0; size 4 + (6ℓ−5) + |CERTS|); hash inspectors `HI{0,1}` (inspect iff
hq 2 ⌜them⌝ = h); simulating inspectors `SI{20,100}` (inspect iff `run k them me` = K; default N on `TO`); the
responsive inspector `RI` = `if prove 8 (them plays C against me) then N else I`; `RIM` = the same with a one-digit
`M{4}` instead of I on failure. Inspectee (22): `C0`, `K0`; `Mc{1..7}` (K with probability j/8); `HE{0,1}`; `SE{20,100}`
(comply iff `run k them me` = I); `PE` (cheat iff provable that the inspector plays N); `PEC` (comply iff provable that the
inspector plays I); `PR{2,3,4}` = `if prp b_e them me I k then C else K`; `CR{2,3,4}` the same with `chk`;
`PCR3` (`chk`, and if that fails `prp`).
RPS (24): `R0`, `P0`, `S0`; `U` (`if eq(tape 0, 0) then R else if eq(tape 0, 1) then P else S`, 15 nodes); `B(a₁,a₂)`
(6 ordered pairs; `if eq(tape 0, 2) then a₂ else a₁`, so a₁ with probability 2/3); carriers `CB(a₁,a₂)` (certificate for
a₁); hash programs `H{0,1,2}` (the action rotation j applied to hq 3 ⌜them⌝); simulators `SIM{20,100}` (play the action
that beats the sample; default R on `TO`); `PB` (for a in R, P, S: if `prove 8` that the opponent plays a then play the
action that beats it, else uniform); `PRR` (the same with `prp` at threshold 12/27 per action) and `CRR` (with `chk`).
Prior: the repo's length prior over template spellings: size s with probability ∝ 1/(2s²) over the sizes present, uniform
among the templates of that size (`src/rps.py length_prior_sizes`).

### 1.2 Hand table: constants, mixers, carriers (steps and leaves, inspection, r = 2, m = 3)

Steps of a play = 2 + 3 × (leaf depth); a carrier adds the β-step that binds `certs`: 3 + 3 × depth. Leaves are
(prefix → action, weight, depth).

| program | leaves | E[steps] | P(I) | I-cert prefixes (carrier), CERTS nodes |
|---|---|---|---|---|
| `I0`, `N0`, `C0`, `K0` | one | 2 | 1, 0, ... | — |
| `M{1}` | (000)→I 1/8, (001)→N 1/8, (01)→N 1/4, (1)→N 1/2 | 7.25 | 1/8 | [(0,0,0)], 15 |
| `M{2}` | (00)→I 1/4, (01)→N 1/4, (1)→N 1/2 | 6.5 | 1/4 | [(0,0)], 13 |
| `M{3}` | (00)→I 1/4, (010)→I 1/8, (011)→N 1/8, (1)→N 1/2 | 7.25 | 3/8 | [(0,0), (0,1,0)], 21 |
| `M{4}` | (0)→I 1/2, (1)→N 1/2 | 5 | 1/2 | [(0)], 11 |
| `M{5}` | (0)→I 1/2, (100)→I 1/8, (101)→N 1/8, (11)→N 1/4 | 7.25 | 5/8 | [(0), (1,0,0)], 19 |
| `M{6}` | (0)→I 1/2, (10)→I 1/4, (11)→N 1/4 | 6.5 | 3/4 | [(0), (1,0)], 17 |
| `M{7}` | (0)→I 1/2, (10)→I 1/4, (110)→I 1/8, (111)→N 1/8 | 7.25 | 7/8 | [(0), (1,0), (1,1,0)], 25 |

A prefix of length ℓ is a list of ℓ digits, 2ℓ + 1 nodes (ℓ pairs, ℓ nats, the nil `nat 0`); a list of n prefixes has
|plist| = 2n + 1 + 2Σℓᵢ nodes; one entry (action constant, plist) has 2 + |plist|; the entries list has 4 + |plist|; and
CERTS = (stamp, entries) has **6 + |plist|** nodes (the column above). Carrier sizes 4 + (6ℓ−5) + |CERTS| (`lam`, `lam`, `app`, `lam`, BODY,
CERTS): `CARR{1}` 4 + 19 + 15 = 38, `CARR{2}` 4 + 13 + 13 = 30, `CARR{3}` 4 + 19 + 21 = 44, `CARR{4}` 4 + 7 + 11 = 22, `CARR{6}` 4 + 13 + 17 = 34.

Inspectee mixers `Mc{j}` are the same trees with K at the cheat leaves and C elsewhere; probability of K is j/8.

### 1.3 The values over tapes (inspection)

Payoffs are U_insp(p, q), U_ee(p, q) of §1.0 with p = j/8 for `M{j}` (I0: 1, N0: 0) and q = j'/8 for `Mc{j'}` (C0: 0, K0: 1):

| | `C0` | `K0` | `Mc{4}` | `Mc{1}` |
|---|---|---|---|---|
| `I0` | (−1, 0) | (−1, −3) | (−1, −3/2) | (−1, −3/8) |
| `N0` | (0, 0) | (−4, 1) | (−2, 1/2) | (−1/2, 1/8) |
| `M{4}` | (−1/2, 0) | (−5/2, −1) | (−3/2, −1/2) | (−3/4, −1/8) |
| `M{3}` | (−3/8, 0) | (−23/8, −1/2) | (−13/8, −1/4) | (−3/8 − 4(5/8)(1/8), (1/8)(−1/2)) = (−11/16, −1/16) |

**The compliance threshold.** The inspectee prefers to comply iff 4p − 1 > 0, i.e. p > 1/4; at p = 1/4 it is
indifferent (U_ee = 0 for every q). On the 1/8 grid the smallest p above 1/4 is 3/8. A reader `PR{k}`/`CR{k}` complies iff
P(inspect) ≥ k/8: `PR{3}` is the exact best responder (complies at j ≥ 3, cheats at j ≤ 2, where its payoff
1 − 4p = 1/2 at j = 1 and 0 at j = 2); `PR{2}` also complies at p = 1/4 (payoff 0 either way, so it is payoff-equivalent
to `PR{3}` for the inspectee, and strictly better for the inspector, who then pays −1/4 instead of −13/4 at j = 2);
`PR{4}` complies only from 1/2, so it cheats against `M{3}` (U_ee = −1/2 < 0, a mistake) and, harmlessly, against `M{2}` (payoff 0 either way). So certificates
"below, at and above 1/4" are `M{1}`/`CARR{1}`, `M{2}`/`CARR{2}`, `M{3}`/`CARR{3}`.
Commitment: an inspector visibly at p > 1/4 deters a best-responding inspectee and earns −p (−3/8 at p = 3/8).
Nash (1/4, 1/4) gives (−1, 0); the lazy `M{2}` is the Nash inspector.

### 1.4 The two routes, step by step (inspection)

(a) **Responsive inspector against a constant, by search.** `RI` against `C0`: 2 β-steps; the `mk` that builds the formula
(1); the `prove` (cost W); the `if` (1); total 4 + W. The atom: state₀ = `C0 ⌜C0⌝ ⌜RI⌝` →(EvR) state₁ →(EvR) value C →
⊤, closure [A₀, A₁, ⊤], `pred(A₁) = [A₀]`. **W is the number of memo-miss expansions of the iterative-deepening search,
traced by hand** (each `ms` call that is not answered by an exact or sufficiently high memo entry costs 1, each fresh
`J` costs 1):

| n | calls (work counter after it) |
|---|---|
| 1 | `ms(∅,{A₀},1)` (1): EvR needs `ms(·,{A₁},0)` = 1 > 0, `J(A₀,1)` = 2; result (2, inexact) |
| 2 | `ms(∅,{A₀},2)` (2) → `ms(∅,{A₁},1)` (3), result (2, inexact) → `J(A₀,2)` (4) → `ms({[2]A₀},{A₀},1)` (5), result 2 > 1 so the JLöb instance has size ≥ 3: `J(A₀)` = (3, inexact); `ms(∅,{A₀},2)` = (3, inexact) |
| 3 | `ms(∅,{A₀},3)` (6) → `ms(∅,{A₁},2)` (7) → `ms(∅,{⊤},1)` (8) = 1 (axiom) so A₁ has size 2 (EvR, Ax); `J(A₀,2)` answered from the memo; A₀ has size 3: found |

**W = 8**, so `RI` against `C0` costs 4 + 8 = **12 steps** and plays N (and `PB` against `R0` the same, 12; `PE` against `N0`, `PEC`
against `I0`). The derivation size is 3 (EvR, EvR, Ax). A refutation (`RI` against `K0`, or against any mixer that has a
K leaf) pays the whole iterative deepening up to b = 8 and is **not derived by hand**; it is measured and reported
(§1.6 says what the hand table predicts about it).
(b) **Enumeration of a one-digit mixer** (`PR` on `M{4}`): 2 leaves, 5 steps each: charge 1 + 2 × 6 = 13; the reader
total is 2 + 13 + 1 = **16 steps**. **Certificate check** on `CARR{4}` (cert [(0)]): one replay of 3 + 3 = 6 steps: charge
1 + 1 × 7 = 8; total 2 + 8 + 1 = **11**. (The spec's "two-assignment check" is the enumeration; a certificate that lists
both leaves would charge 1 + 2 × 7 = 15.)
(c) **A three-digit mixer** (`M{3}`/`CARR{3}`): enumeration on `M{3}` has leaves of 8, 11, 11, 5 steps, charge 1 + (9 + 12
+ 12 + 6) = 40, total **43**; on `CARR{3}` (one more β per leaf: 9, 12, 12, 6) charge 1 + (10 + 13 + 13 + 7) = 44, total **47**;
the check lists the two I leaves (9 and 12 steps): charge 1 + (10 + 13) = 24, total **27**.

| reader (total steps) on | committed inspector p = 1/4 (`j`=2) | 3/8 (`j`=3) | 1/2 (`j`=4) | 3/4 (`j`=6) |
|---|---|---|---|---|
| `PR` (enumeration) on the carrier | 31 | 47 | 18 | 31 |
| `CR` (check) on the carrier | 14 | 27 | 11 | 21 |
| `PR` (enumeration) on the plain mixer | 28 | 43 | 16 | 28 |

Arithmetic: enumeration total = 2 + [1 + Σ over all leaves (1 + steps)] + 1, a plain leaf at depth d has 2 + 3d steps and a carrier leaf
3 + 3d; the check total = 2 + [1 + Σ over listed I-leaves (1 + carrier steps)] + 1. E.g. `CARR{6}`: enumeration leaves 6, 9, 9 steps:
1 + 7 + 10 + 10 = 28, total 31; check lists (0) and (10): 1 + 7 + 10 = 18, total 21. The tests recompute these from the leaf
lists; where this prose and the code disagree the code is the erratum.

**Check against the plain mixer:** `CR` on a non-carrier fails at once: 2 + 1 + 1 = **4 steps**, and plays K (reader defaults
to cheating); `CR` is blind to uncertified mixers.
(d) **Costs of the readers against constants.** `PR` on `I0`: one leaf of 2 steps: charge 4, total 7. `CR` on `I0`: 4.
`SI`/`SE` against a constant: 2 + run (1) + the constant's 2 + unwrap (1) + `eq` (1) + `if` (1) = **8**, needing sim fuel k ≥ 3.

**Route summary (hand).** Search for a constant: 12; check: 11 (one digit) to 27 (three digits); enumeration: 16 to 47. The
hand table makes the **certificate check the cheapest route** to a probability, the **enumeration the dearest** by a
factor 1.45 to 1.74 over the check on the same carrier, and the **responsive inspector's search** (12) as cheap as a
one-digit check against constants and, against everything that is not provably compliant, a full iterative-deepening
refutation of unknown size.

### 1.5 RPS (r = 3, m = 3)

`U`: leaves (0)→R, (1)→P, (2)→S with steps 5, 8, 8: E[steps] 7; every program earns exactly 0 against `U` (and `U` against
everything) in the absence of forfeits. `B(a₁,a₂)`: 5 steps on every leaf; plays a₁ with probability 2/3. `H{j}`: 2 + n(y) + 1 + 2
(digit 0) or + 4 (digits 1, 2) steps against an opponent y with n(y) nodes. `SIM{k}` against a constant y: 2 + [run 1 + 2 + unwrap
1] + β 1 + (2 per comparison) = 9 for the first comparison, 11, 13 for the next two. `PB` against `R0`: **12** (the same
chain as `RI` against `C0`) and the action P; against `P0`: W_ref (the first, refuted, search) + 14, playing S.
Values over tapes: a₁ against the biased `B(a₁,a₂)` has no advantage; the best response to `B(R,P)` is the constant P with
payoff 2/3·1 + 1/3·0 = **2/3** (= the bias); `SIM{100}` plays the action that beats one sample, so against `B(R,P)` it plays P with
probability 2/3 and S with 1/3 and earns (2/3)(2/3) − (1/3)(2/3) + (1/3)(1/3) = **1/3**, "exploited to the extent of its bias" (half the
best response); against `U` it earns 0 (a fresh sample of a uniform tape predicts nothing), against `H{j}` it earns **+1** when
its fuel affords the hash (cost n(SIM) nodes, so `SIM{100}` does and `SIM{20}` does not: on `TO` it plays R). `PRR` and `CRR` at threshold
12/27 play the best response P to `B(R,P)` (18/27 ≥ 12/27), earn **2/3**, and 0 against `U` (9/27 < 12/27).

### 1.6 What the hand table predicts, ahead of the code

* The statics: derived atoms true; sims earn 1/3, 2/3, +1, 0 as above; the pseudo-random control is beaten by an affordable
  simulator and by `PB` (its evaluation is deterministic and provable); the uniform mixer by nothing.
* Routes: check < enumeration on the same carrier (27 vs 47 for p = 3/8), search 12 against a constant.
* The refutation cost of a responsive search against anything that is not a provably compliant constant is the number
  the hand table cannot give; it is measured before the lottery and it decides whether search is the dearer route in the
  population (prediction 6's explicit comparison).
* The price: c₀ = 0.12/K₀ with K₀ ~ 10³ prices 10–50 steps at 10⁻³ to 10⁻², small against the payoff gaps of a game
  played at selection intensity 0.3, so the hand table predicts that the fixed-c fuel panel (smaller K at the same c)
  is the cell that can separate the routes.
