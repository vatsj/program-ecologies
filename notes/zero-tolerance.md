# Zero-tolerance, suspicious and sampling inspectors (notes, 2026-10-24)

Spec `specs/2026-10-24-zero-tolerance.md` (reviewed by gemini-4-argon, then gpt-6.1-sol in amended mode; both folded).
Builds on `notes/inspection-shadow.md`, `runs/inspection-shadow.md` and RESULTS "The inspection game's enforcer and its
shadow". §1 is written by hand before any code of this run and before any counted cell. §2 (choices where the spec is
silent, and deviations) is appended with the code, before any counted cell. §3 records facts found while running.

**What §1 used.** No chain was solved, no lottery was run and no repository code was written for §1. The numbers below are
evaluations of the formulas written next to them, made with an independent pure-python scalar evaluator in an
uncommitted scratch directory (the level recursion of `notes/mixed2.md` written again from scratch, one program pair at a
time, plus the added operators of §1.0). Before it was used, it reproduced the stored exact-arm numbers (c = 0, D = 12) to
5·10⁻¹³ on a 5 × 8 grid of inspector/inspectee pairs (payoffs, expected costs, forfeit masses), and its rows for
`cr(THEM(ME))` and `if(THEM(ME)=C,N,I)` coincide with the stored class rows of those two inspectors over all 2,150
inspectee programs (so it also decides class membership correctly). The code of step 3 recomputes every number here and
a test pins them. The stored class tables of the previous run (`mixed2.get_arm('insp', 'exact', 8, c)`) were read
(read-only) for prior masses and for the list of strict invaders of the resident (`cr(THEM(ME))`, `C`).

## 1. Hand derivations

### 1.0 The added programs, exactly

Notation: game as in `notes/inspection-shadow.md` §1.0 (inspector I or N, inspectee C or K; (I,C) = (−1, 0), (I,K) =
(−1, −3), (N,C) = (0, 0), (N,K) = (−4, +1)). With inspection probability p and cheating probability q: inspector
−p − 4(1−p)q, inspectee q(1 − 4p). A reader's child `THEM(ME)` at level d is the opponent's value (P(C), P(K), P(forfeit))
against the reader at level d−1; at level 0 it is a forfeit (the depth-cap convention of the stored arm). Let a child
have value (p_C, p_K, p_f) and z = 1 − p_f.

| program | rule | output (P(I), P(N), P(forfeit)) |
|---|---|---|
| `cr(x)` (stored) | inspect iff p_K / z > 1/4 (coin at exactly 1/4); forfeits with mass p_f | z·b, z(1−b), p_f |
| `zt(x)` | inspect iff p_K / z > 0 (strictly, tolerance 10⁻¹²); forfeits with mass p_f; no child mass (z = 0) forfeits entirely | z·b, z(1−b), p_f |
| `cr_s(x)` | as `cr`, but the timed-out mass p_f is **inspected** (the suspicious default); z = 0 gives I | z·b + p_f, z(1−b), 0 |
| `zt_s(x)` | as `zt`, with the suspicious default | z·b + p_f, z(1−b), 0 |
| `sr_k(x)` | k independent draws of the child, stopped at the first cheating draw: inspect; at the first timed-out draw: forfeit (the arm's default); all k compliant: N | p_K·g, p_C^k, p_f·g, with g = (1 − p_C^k)/(1 − p_C) (g = k if p_C = 1) |
| `sr_k,s(x)` | as `sr_k` with the suspicious default (a timed-out draw is inspected) | 1 − p_C^k, p_C^k, 0 |
| `I` (comparator) | the constant I, already in the grammar (class `0I`, prior 0.368) | 1, 0, 0 |

Costs (levels, the stored arm's price unit): `zt`, `cr_s`, `zt_s` are charged exactly like `cr` (the serial depth of the
child); `sr_k` is charged the expected number of draws actually simulated times the child's cost, `g · E(child)`
(short-circuit: the first draw is always read, draw i+1 only if the first i were compliant): k levels against a
compliant constant, 1 against K (the first draw already cheats), 1.875 (k = 4) and 2.0 (k = 16) against `X`, 3.64 and
10.30 against q = 1/16. The unconditional inspector is free.

**What "timeout" means in the stored evaluator (a correction to the spec's wording).** The spec says `cr` "falls back
to *not inspecting* when its read of the inspectee times out". In the evaluator a timed-out read is a *forfeit* of the
reader (the forfeiter is charged the opponent-favourable worst action, which for the inspector is I against C and N against
K); it is not "N". The bounded-read exploit is not a timeout fallback at all (§1.3): the read does not time out, it
returns the inspectee's level-(D−1) behaviour, which differs from its level-D behaviour. The suspicious variants are
therefore defined by the table above (timed-out mass becomes I, instead of a forfeit), and `zt`, `sr_k` keep the stored
forfeit convention as "the arm's default". The spec's "same timeout action as the arm's default (not inspecting, or
inspecting in the suspicious variant)" is read that way; this is disclosed in §2.

### 1.1 Payoffs against constants and light cheaters (D = 12, c = 0; u = (inspector, inspectee))

Against a non-reader that cheats with probability q the child is a constant (p_C = 1 − q, p_f = 0), so every row is a closed form.

| inspector | vs `C` | vs `K` | vs a light cheater q | vs `X` (q = ½) |
|---|---|---|---|---|
| `I` | (−1, 0) | (−1, −3) | (−1, −3q) | (−1, −1.5) |
| `N` | (0, 0) | (−4, +1) | (−4q, q) | (−2, 0.5) |
| `cr(THEM(ME))` | (0, 0) | (−1, −3) | q < ¼: (−4q, q); q > ¼: (−1, −3q); q = ¼: (−1, −¼) | (−1, −1.5) |
| `zt(THEM(ME))`, `zt_s` | (0, 0) | (−1, −3) | q > 0: (−1, −3q) | (−1, −1.5) |
| `cr_s(THEM(ME))` | as `cr` | as `cr` | as `cr` | as `cr` |
| `sr_k` (and `sr_k,s`), p_k = 1 − (1−q)^k | (0, 0) | (−1, −3) | (−p_k − 4(1−p_k)q, q(1 − 4p_k)) | k = 1: (−1.5, −0.5); 4: (−1.0625, −1.375); 16: (−1, −1.5) |

Numbers from the scalar evaluator (inspector payoff, inspectee payoff): `q = 1/8`: `cr` (−0.5, 0.125); `zt`, `zt_s`
(−1, −0.375); `sr_1` (−0.5625, 0.0625); `sr_4` (−0.7069, −0.0819); `sr_16` (−0.9410, −0.3160). `q = 1/16`: `cr`
(−0.25, 0.0625); `zt` (−1, −0.1875); `sr_1` (−0.2969, 0.0469); `sr_4` (−0.4206, 0.0056); `sr_16` (−0.7329,
−0.0985). `q = 3/16`: `sr_1` (−0.7969, 0.0469); `sr_4` (−0.8910, −0.2356); `sr_16` (−0.9910, −0.5354). `q = ¼`:
`cr` mixes ½/½ and gives the inspectee −¼; `sr_1` (−1, 0); `sr_4` (−1, −0.4336); `sr_16` (−1, −0.74).

**Zero tolerance pays for its rule.** Against a light cheater the exact reader `cr` earns −4q (it declines to inspect
because −4q > −1 for q < ¼); `zt` earns −1. At q = 1/16 the sacrifice is 0.75 per round; it is the inspection analogue of
PrudentBot's defection against CooperateBot. What `zt` buys is that the light cheater earns −3q instead of +q, so it is
deleterious against `zt` and cannot invade (`zt`, `C`). The state (`zt`, light q) is, however, not an equilibrium of
the inspector's own interest: `N` earns −4q > −1 against it and invades strictly, so zero tolerance moves the light-cheater
channel from "invades the efficient state" to "is parked in a state the unconditional shadow can strictly enter".

**The thresholds.** A light cheater with probability q earns q(1 − 4p_k) against `sr_k` and invades (`sr_k`, `C`)
iff q < q*_k = 1 − (3/4)^{1/k}:

| k | q*_k | non-reading grammar mixers (n = 8) with 0 < q < q*_k (inspectee classes; prior mass) |
|---|---|---|
| 1 | 0.2500 | q = 1/16, 1/8, 3/16: 3 classes, mass 0.002916 (the same set that invades `cr`) |
| 4 | 0.0694 | q = 1/16: 1 class, mass 0.000156 |
| 16 | 0.0178 | none: the smallest grammar mixer is q = 1/16 (size 7; q = 1/32 needs size 9), mass 0 |

The grammar's non-reading inspectee classes have q ∈ {0, 1/16, 1/8, 3/16, ¼, …, 1} (17 classes, mass 0.9939). The
counter-prediction on the q grid is therefore settled by the grammar for this arm: `sr_16` has no light-cheater escape
channel at n = 8, `sr_4` has one of mass 0.00016, `sr_1` has the whole stored channel (and is the stored sampled
responder, §1.5).

### 1.2 Unconditional inspector against everything

`I` earns −1 against every inspectee that does not cheat with probability 1, and −1 against `K`: it is a dominated
commitment. Against (`I`, `C`) the inspector pays 1 per round for nothing, so `N` (and every reading inspector) invades
by selection of size 1 at either price (wΔ = 0.3, ρ ≈ 0.26). The comparator therefore tests only the *prior mass* effect
of adding an inspecting class: it cannot sit in R for long, and any gain over the matched control would have to come
through the founders or the transitions it creates, not through holding the seat.

### 1.3 The bounded-read exploiters: a phase effect, not a timeout fallback

The stored exploiter `cr(coin(N, THEM(ME)))` (mass 0.00012; strict invader of (`cr(THEM(ME))`, `C`) with Δ = +0.992)
plays against `cr(THEM(ME))` as follows (level d from 0 to 12; the pair (inspector P(I), P(N), P(f) | inspectee P(C),
P(K), P(f)); levels ≥ 4 repeat with period 4 and halving forfeit mass):

* d = 0: inspector (0, 0, 1) | inspectee (0, ½, ½): its child is ½ N + ½ forfeit, conditional on completing it plays N, so K.
* d = 1: (½, 0, ½) | (0, ½, ½). d = 2: (½, 0, ½) | (¾, 0, ¼): the child ½ N + ½ (½ I, ½ forfeit) has inspection
  probability 1/3 among completed mass, and cheating (−1/3) loses, so C. d = 3: (0, ¾, ¼) | (¾, 0, ¼).
* d = 4: (0, ¾, ¼) | (0, ⅞, ⅛) (the child is now N-heavy: cheat). d = 5: (⅞, 0, ⅛) | (0, ⅞, ⅛). d = 6, 7: the inspectee
  is C again. And so on with period 4 in d: the inspectee cheats at d ≡ 0, 1 (mod 4) … precisely, at d = 12 the inspectee
  is (0, 0.9922, 0.0078) and the inspector, which read level 11 where the inspectee complied, plays (0, 0.9844, 0.0156).

So the exact reader plays N because the inspectee *complied at level 11 and cheats at level 12*. The forfeit mass is
only 1.6%. A *suspicious default does not repair a timeout here*, it changes the dynamics: with the timed-out mass
inspected the whole level sequence becomes deterministic (inspector I at d ≡ 0, 1 and N at d ≡ 2, 3 (mod 4);
inspectee K at d ≡ 3, 0 and C at d ≡ 1, 2), and at d = 12 the inspector's read (level 11: K) and the inspectee's
play (level 12: K) agree, so the inspector inspects and the exploiter earns −3 (table below). This is **a phase
coincidence of D = 12**: the same exploiter beats `cr_s` / `zt_s` at D ≡ 3 (mod 4) and beats `cr` / `zt` at D ≡ 0 (mod 4).

Payoff to the inspectee (u₁; the resident `C` earns 0 against each inspector) for the nine stored reading strict
invaders of (`cr(THEM(ME))`, `C`), the strongest first; D = 12, c = 0:

| inspectee \ inspector | N | `cr` | `zt` | `cr_s` | `zt_s` | `sr_1` | `sr_4` | `sr_16` | `sr_4,s` | `sr_16,s` |
|---|---|---|---|---|---|---|---|---|---|---|
| `cr(coin(N,THEM(ME)))` | 1.000 | 0.992 | 0.992 | −3.000 | −3.000 | 0.992 | 0.504 | −0.963 | −3.000 | −3.000 |
| `cr(coin(N,coin(X,THEM(ME))))` | 1.000 | 1.000 | 1.000 | −3.000 | −3.000 | 1.000 | 0.996 | **0.791** | −3.000 | −3.000 |
| `cr(coin(THEM(ME),coin(N,X)))` | 1.000 | 0.992 | 0.992 | −3.000 | −3.000 | 0.992 | 0.429 | −0.963 | −3.000 | −3.000 |
| `coin(C,cr(coin(N,THEM(ME))))` | 0.500 | 0.500 | 0.500 | −1.500 | −1.500 | −0.500 | 0.476 | −0.228 | −1.375 | −1.500 |
| `coin(C,coin(C,cr(THEM(ME))))` | 0.250 | 0.250 | 0.000 | −0.250 | 0.000 | 0.000 | −0.085 | −0.727 | −0.434 | −0.740 |
| `coin(C,if(THEM(ME)=I,C,X))` | 0.250 | 0.246 | −0.023 | −0.250 | 0.000 | 0.039 | −1.176 | −1.500 | −0.146 | −0.701 |
| `coin(C,if(THEM(ME)=I,K,X))` | 0.250 | 0.246 | −1.469 | −1.500 | −1.500 | −0.096 | −1.038 | −1.500 | −1.307 | −1.500 |
| `coin(C,if(THEM(ME)=I,X,X))` | 0.250 | 0.246 | −0.746 | −0.250 | −0.750 | 0.002 | −1.128 | −1.500 | −0.434 | −0.740 |
| `coin(coin(C,X),cr(THEM(ME)))` | 0.625 | 0.617 | −0.391 | −1.875 | −0.375 | −0.194 | −0.913 | −1.125 | −0.082 | −0.316 |

Reading the table:

* **`zt` and `sr_1` do not close the bounded-read channel; they do close the half-light ones** (rows 5–9: the
  `if(THEM(ME)=I, …)` and `cr(THEM(ME))`-halves are inspected and lose against `zt`, because they cheat with a small
  positive probability against it), so `zt` leaves the three strongest exploiters (mass 0.00013) and the fourth
  (`coin(C, cr(…))`, mass 0.000007) untouched. At D = 12 these are the E-category exits of the stored decomposition.
* **`cr_s` and `zt_s` close all nine** at D = 12 (every entry ≤ 0), by the phase coincidence above.
* **`sr_16` closes the first three** (the repeated-sample read destroys the clean parity: −0.963) **and not
  `cr(coin(N, coin(X, THEM(ME))))`** (+0.791). `sr_4` closes none of the first three (0.43–0.996).
* The same table at **D = 11**: `cr` and `zt` are not exploited by the first four (≈ 0), `cr_s` and `zt_s` **are**
  (u₁ = 1.000 for the first three, 0.500 for the fourth), and at **D = 13** the first three give `cr_s` / `zt_s` 0.000 (neutral
  twins of `C`, no strict invasion) while `cr` / `zt` lose (−2.97). The exploit is a property of the depth cap's residue
  mod 4; I propose a D-phase control (cells at D = 11 and 13; §2) because a closure that depends on the phase of the cap
  is not a closure of a realizable program.

### 1.4 Mutual readers and cost

Against an inspectee that reads the inspector (`cr(THEM(ME))`, `if(THEM(ME)=I,C,K)`: the mutual-reading classes) the stored
exact reader forfeits both ways: (`cr`, `cr(THEM(ME))`) = (−4, −3) with forfeit mass 1 on both sides (the nested read
regresses through all 12 levels). `zt` forfeits identically; `cr_s` and `zt_s` do not forfeit: the timed-out child is
inspected, the inspectee (which BRs to I) cheats at the resulting phase and earns −3 (payoffs (−1, −3)). `sr_k` (forfeit
default) forfeits as `cr` does; `sr_k,s` inspects. The mutual-reading states are therefore not E under `cr` / `zt` / `sr_k`
(forfeit payoffs (−4, −3)) and are non-E with an *inspected* inspectee under the suspicious defaults.

Costs (levels): against compliant constants `zt`, `cr_s`, `zt_s`, `sr_1` cost 1, `sr_4` costs 4, `sr_16` costs 16; against
`K` all cost 1 (the first draw is already a cheating draw); against `X`, `sr_4` costs 1.875 and `sr_16` costs 2; against
q = 1/16, `sr_4` costs 3.640 and `sr_16` costs 10.303. Against a reader the cost compounds through the nested simulation:
`sr_16` against the exploiter costs 8.9·10⁶ levels, `sr_4` 8,944 (the k-fold simulation of a program that itself simulates
the reader), so at c = 0.01 every state where `sr_k` meets a reading inspectee is catastrophic for it (the stored `sr4` /
`sr16` arms have the same arithmetic). Net payoffs at c = 0.01 against `C`: `zt`, `cr_s`, `zt_s`, `cr`, `sr_1` −0.01;
`sr_4` −0.04; `sr_16` −0.16; `N` 0; `I` −1. So at c = 0.01 against the resident (`sr_16`, `C`) both `N` (Δ = +0.16) and
`zt` (Δ = +0.15, a cheaper reader of the same compliant inspectee) invade strictly, while against (`zt`, `C`) only `N`
does (Δ = +0.01): prediction 4 holds at the one-state level by 0.15 per round.

### 1.5 Behavioural classes of the added programs

From the scalar evaluator's rows against all 2,150 inspectee programs (net payoff rows at c = 0 and at c = 0.01) compared
with the stored 157 (c = 0) and 167 (c = 0.01) inspector classes:

* `sr_1` is **the stored class of `if(THEM(ME)=C,N,I)`** (the single-sample responder `RI`; mass 0.000169): same
  payoffs and same cost against every inspectee class at both prices. Adding `sr_1` adds mass to an existing class; it
  creates no new class, and its arm is the control with the same mass moved to `RI` instead of `cr(THEM(ME))`.
* `zt`, `cr_s`, `zt_s`, `sr_4`, `sr_16` and the three `sr_k,s` are **new inspector classes** (no existing class has their rows).
* None splits an inspectee class at c = 0. At c = 0.01 `sr_4`, `sr_16`, `sr_4,s` and `sr_16,s` each split **3**
  inspectee classes (the cost of being read k times differs among spellings of the same behaviour); the others split none.
  The class tables confirm it: K₁ grows from 167 to 173 (three classes split in two, or more) at c = 0.01 in the `sr_4` / `sr_16` arms,
  and K₀ grows by 1 (0 for `sr_1`) in every arm.
* The comparator `I` and the control `cr(THEM(ME))` are existing classes (`0I`, `0CRI`; the class of `cr(THEM(ME))` has 7
  spellings, mass 0.0013517).

### 1.6 The matched prior

The added mass of every arm is m = 0.0013517, the stored class mass of `cr(THEM(ME))`. Each arm adds exactly one program
(`zt`, `cr_s`, `zt_s`, `sr_1`, `sr_4`, `sr_16`) with the whole mass m, so "split equally among the arm's added
programs" is trivial; the other inspector classes keep their mass scaled by (1 − m). The control gives m to the class of
`cr(THEM(ME))` (its spellings scaled proportionally; the other classes scaled by (1 − m)), and the comparator gives m to
`I`. For the lottery the founders of the arm are a coupling of the stored draw: each inspector slot is replaced, with
probability m and independently of the program drawn, by the arm's added program (the control: by a spelling of
`cr(THEM(ME))`), so all arms share the founders of every slot not replaced (about 9 of 6,400 slots at (100, 64)).

### 1.7 What §1 settles for the predictions

* **Prediction 1** (zero tolerance alone): the light-cheater category D of the stored decomposition falls to zero from
  (`zt`, `C`) (the three light cheaters are deleterious); the three strongest bounded-read exploiters (and `coin(C,
  cr(…))`) are still strict invaders, with Δ ≈ +0.99, so the E-category hazard is not removed. The stored decomposition
  at N = 10⁵ gives D 7.9·10⁻⁵ and E 3.0·10⁻⁵ per event of the stationary hazard from R; removing D alone leaves E as the
  largest exit and a total about 3.6× lower. The category-D hazard from the resident (`zt`, `C`) is exactly zero; the
  stationary R also contains `cr` residents (the control's mass is still there), so the arm-wide D hazard falls by less
  than the resident-specific figure but I expect it to fall by ≥ 10× because (`zt`, light) states are parked outside R.
  I expect π(E) to stay near or below 0.24 (the stored "non-reading light cheaters removed" benchmark). Engineer's expectation, not binding: the
  counter-prediction (π(E) below 0.10) is the likelier of the two readings.
* **Prediction 2**: `zt_s` and `cr_s` close the bounded-read channel at D = 12 for all nine stored exploiters; whether
  the closure survives other D phases is the control of §2.
* **Prediction 3**: `sr_16` has no light-cheater channel at n = 8 and closes three of the four strong exploiters;
  `cr(coin(N, coin(X, THEM(ME))))` (mass 0.000007, Δ = +0.79) remains. `sr_1` is the stored `RI`.
* **Prediction 4**: at c = 0.01, `sr_16` loses 0.16 per round on compliant inspectees against `zt`'s 0.01.
* **Prediction 5**: the lottery's founders contain about 9 of 6,400 replaced slots; the lottery was dominated by
  founding competition, so no arm moves by 0.1 unless the new program's row changes who wins the founding scramble.

## 2. Choices where the spec is silent, and deviations (written with the code, before any counted cell)

*Disclosure.* Before this section was committed I ran, besides the scratch evaluations of §1: (i) the unit tests of
`tests/test_zero_tolerance.py` (15, passing); (ii) the static summary `runs/zero_tolerance/static.json` (class tables of every arm at both prices,
no chain, no lottery); (iii) the validation job (`zero_tolerance_run.py validate`: arm `v0` against the stored chain at N = 10³ and 10⁴ and the
stored lottery runs 0–2), which gates every counted cell; (iv) one scratch lottery run of the ZT arm at (100, 64) and a 400-generation run at
(400, 64) to time the cells (not saved, not counted). None changed a prediction, a scoring rule or a cell of the spec. The predictions file was
committed before any code existed.

**Choices.**
1. **Evaluation without a new kernel.** The added inspectors are evaluated by the stored kernel `mixed2._eval_role` (for the inspectee side, one
   added inspector as the single opponent, level by level) and by a few vectorised numpy lines for the added inspector's own rule; the base
   program table is `mixed2.evaluate`. The arm's table is the base table with the added rows/columns appended, collapsed by `mixed2.collapse` over
   the arm's inspector set. Self-tests: the machinery reproduces the stored program rows of `cr(THEM(ME))` and of `if(THEM(ME)=C,N,I)` exactly
   (zero difference in payoffs, costs, forfeits, values and level D−1 values), the validation arm `v0` reproduces the stored class table exactly,
   and the added rows equal an independent scalar evaluator (`tests/zt_reference.py`) to 10⁻⁹ on 150 random inspectees (400 in scratch).
2. **Timeout semantics** (§1.0): `cr` and `zt` forfeit on a timed-out read (the stored convention; the spec's "not inspecting" does not describe
   it), the suspicious variants inspect the timed-out mass. The bounded-read exploit is a depth-phase effect, not a timeout (§1.3).
3. **Cost of `sr_k`: expected draws** (short-circuit), `g · E(child)` with g = (1 − p_C^k)/(1 − p_C), as the spec states ("stops at the first
   cheating draw"); the stored `sr4` / `sr16` arms charge `k · E(child)` always. The serial-depth measure M used by an inspectee that reads the
   sampler is `k · M(child)` (a bound, as in the stored arms). Against a reading inspectee the cost compounds through the nested simulation
   (8.9·10⁶ levels for `sr_16` against the first exploiter); at c = 0.01 such states are catastrophic for `sr_k`.
4. **Prior.** The added mass m is the class mass of `cr(THEM(ME))` at the same price (0.0013517 at both prices to four decimals); every arm adds one
   program with all of m; other inspector programs are scaled by 1 − m; the control scales the seven spellings of `cr(THEM(ME))` proportionally
   and adds m to them; the comparator adds m to the single spelling `I`. `sr_1` lands in the existing class of `if(THEM(ME)=C,N,I)` (12 members, class
   mass 0.000169 → 0.001521); this arm is the control with the mass given to the sampled responder instead of the exact one. The representative
   spelling of that class is now `sr1(THEM(ME))` (smaller size), which changes the printed name of the class, not its identity.
5. **Reporting.** Exit categories are the stored ones; "light cheaters" is category D, "bounded-read exploiters" E, "shadow" A, "others" the rest.
   Hazards from R are reported under the arm's own weights (the headline; scoring of predictions 1 and 2) and under the control's weights embedded
   by class names (fixed reference weights; the added class has weight zero; mass of control classes absent from an arm — the inspectee classes that
   split at c = 0.01 in the `sr_4`, `sr_16` arms — is dropped and the retained mass reported in the JSON). The aggregate hazard from R includes the
   control's `cr(THEM(ME))` residents, whose prior mass the arm keeps (1 − m of it); the resident-specific rates out of (added inspector, `C`) are
   therefore reported beside every aggregate. Prediction 3's counter-prediction (a low-q escape channel) is scored by the resident-specific D
   hazard of (`sr_16`, `C`), which is zero on this grammar (§1.1).
6. **Lottery.** Founders are coupled to the stored draw (§1.6); the dynamics seed is the stored cell's for every arm (so `v0` reproduces the stored
   cell bit for bit and the arms differ by the replaced slots, about 9 per run at (100, 64)); the founder-seed names are the stored ones
   (`primary`, `n400i64`). Unresolved islands: a role's top class below 0.9 of the island at the checkpoint. The horizon is 20N; late transitions
   are visible in the common-t trajectory in the JSON.
7. **Extras outside the spec** (clearly marked, never part of verdicts 1–5): (a) the D-phase control of §1.3 (cells at D = 11 and D = 13 for the
   control, SUS, ZT+SUS and ZT at c = 0, N = 10⁴ and 10⁵), scored as the engineer's E2; (b) the class tables of `sr_4,s` / `sr_16,s` (static only).
8. **Jobs.** `src/zero_tolerance_batch.py` runs the job file `runs/zero_tolerance/jobs.txt` as separate processes (no pool), 2 at a time (other
   subagents' processes are alive), one whole-space chain at a time, gated by memory; the batch exits with "STALL" if neither its log nor a running
   job's log has changed for 2 hours. Chains use float32 storage of the jump-chain matrix as in the previous run (`--f32`); the stored float32 values
   are reproduced by the validation job. The chain solver is the previous run's blocked GTH (`inspection_shadow.gth_blocked`); a chain cell takes
   6–7 minutes single-threaded.

**Cut order** (spec): the 400-island cell, N = 10⁵ at c = 0.01, `sr_4`. Decided and disclosed in §3 as the run proceeds.

## 3. Facts recorded while running (after the counted cells began)

1. **Counted batch.** The 85 jobs of `runs/zero_tolerance/jobs.txt` (chain cells, lottery cells at (100, 64) and five at (400, 64)), then 2 redo
   cells and 4 extra cells; all finished with return code 0 except the two redone ones below. Two workers throughout (other subagents were alive),
   one whole-space chain at a time; a chain cell took 3.5–8 minutes single-threaded, peak RSS 1.7–4.1 GB. No cell of the spec was cut. The
   scheduler started the cheap lottery cells first and the chains after them (memory gating), which changed the order, not the content.
2. **Overflow in `mixed2.lrho` at c = 0.01 for `sr_k`.** The first two `sr16` chain cells at c = 0.01 (N = 10⁴ and 10⁵) crashed in the exit
   decomposition: the nested k-fold simulation charges 8.9·10⁶ levels, so a payoff difference of 10⁵ makes `log(expm1(a))` overflow in the
   stored `lrho`. The fix is `lrho_safe` (an algebraically identical expression for a = −w·Δ > 30, installed as `mixed2.lrho` at import; a test pins
   its agreement with the stored function where that one is finite). No other cell has |Δ| > 100, so no completed cell changed (the validation arm
   was run before the fix and is unaffected by construction). The two cells were rerun after the fix; the `sr16` N = 10³ cell and all `sr4` cells at
   c = 0.01 were run after it. A tool outage interrupted the run for about nine hours between the main batch and the redo batch (nothing was running);
   the redo batch was launched when the outage ended.
3. **Post-hoc extras** (not in the spec, not scored in verdicts 1–5): (a) the validation arm `v0` at (400, 64), c = 0 reproduces the stored cell bit for
   bit (efficient islands 0.672, max |Δ| = 0 per run), so the control's 0.430 at (400, 64) and 0.725 at (100, 64) (stored 0.648) measure how much moving
   m = 0.00135 of inspector prior mass changes a lottery cell, not an error: the dynamics diverge after the first replaced founder, so a "paired" contrast is
   in effect an independent-sample contrast at this run count; (b) `sr16` at D = 11 and 13, c = 0, N = 10⁴ and 10⁵ (the D-phase control for the second
   arm that gains); (c) the restated phase comparison E2′ (descriptive).
4. **Scoring caveat found on the way.** The registered hazard statistics (predictions 1, 2 and E1, E3, E5) are *aggregate* hazards from R. R keeps the
   control's `cr(THEM(ME))` residents at their prior mass beside the arm's added inspector, so the aggregate falls less than the resident-specific rate
   of (added inspector, `C`). The scores follow the registered rule; the resident-specific rates are in the report beside every aggregate (for example
   (`zt`, `C`) has D-hazard exactly 0, (`cr_s`, `C`) has E-hazard exactly 0, (`zt_s`, `C`) has both exactly 0 at N = 10⁴ and 10⁵).
