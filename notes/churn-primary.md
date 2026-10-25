# Does churn among the fair pairs happen in the primary object? (notes, 2026-10-25)

Spec `specs/2026-10-25-churn-primary.md` (the RS: the veto "is an experimental artifact", replicate the dynamics in the
primary object; reviewed by gemini-4-argon, then gpt-6.1-sol in `--mode amended`; the [after review] text is the
resolution). Follows RESULTS "Deriving immigrant rejection for stable sets on islands, Step 0", "A migration window for
stable sets on islands", "Stable sets on islands", "Three-player majority divide-the-dollar". §1 is written by hand
before any code of this experiment and before any counted cell; §2 (deviations, choices where the spec is silent,
costs) is appended as they arise.

## 1. Hand predictions, the churn-capable readers, priors, arm T's frozen settings

### 1.0 Disclosure about order

Before writing this section I ran four **scratch queries** (scripts outside the repository, in the session scratchpad;
no population dynamics, no counted cell): (i) the standing `src/dollar3.py` prior and catalogue at n = 6, 10, 11 (class
counts, constant mass, distinct classes in 6,400 draws); (ii) a static scan of every canonical function against all
81 pairs of constant opponents, to find which classes can take a fair-pair island to another fair pair (§1.2.1);
(iii) the prior mass of the exact reciprocal readers at n = 6, 10, 11; (iv) a feasibility run of the arm-T template
programs in `src/lt_code.py` (about twenty three-program executions, to fix the fuel caps and to hand-check the paths of
§1.2.3), plus the timing of one baseline run (`migration_window`, N = 100, mN = 1, 2,000 generations) and of one n = 10
joint table. Everything quantitative below that depends on them is stated as such; the predictions of §1.6 were written
after (i)-(iv) and are therefore informed by the static facts, not by any trajectory of the new arms.

**One premise of the spec is false and is corrected here before any run.** The spec says the n = 10 grammar contains
two-partner readers ("name j iff j provably names me at 1/2, else name k iff k does, else name j"). It does not: that
reader is `if(Bj, A, if(Bk, A', A''))`, a size-11 program, and no canonical function of that shape exists at n ≤ 10
(§1.3). The n = 10 grammar adds 21,000 canonical functions, almost all conjunctions/disjunctions of two atoms that
choose between two actions, and they carry mass 0.0075. What n = 10 does contain, as does n = 6, are the *single-atom
switchers* ("if j names me at 1/2 then j else k"). The two-partner reader is therefore tested in the control arm E-min
(§1.4), which is built to contain exactly it; arm E at n = 10 is kept as the spec states it.

### 1.1 The object, frozen now

Everything of `src/dollar3.py` (game, DSL, evaluators), `src/stable_sets.py` (kernel inputs, seed laws, joint tables),
`src/dominance_contracts_run.py` (`tables()`: the 20 outcomes, payoffs in dollar units), `src/migration_window.py` and
`src/migration_window_kernels.py` (the kernel `kern_mw` with the per-generation records, the analysis) and
`src/lt_code.py` (the L_T^code evaluator) is imported; nothing is edited. The primary-object dynamics are exactly those
of the stored baseline: the **ε = 0 seed lottery**, three slot populations per island, mean-field expected payoffs
against one uniformly drawn member of each other slot, Moran birth-death with fitness weight exp(w·payoff), **w = 0.3**,
**N = 100** per slot population, **I = 64** islands in one connected component, m = mN/N per birth with
**mN ∈ {0, 0.01, 0.1, 1}**, **40 runs**, **10,000 generations** (extended to 20,000 for runs not resolved only if the
cut order allows), founders common across mN within a run. There are **no contracts, no guard and no veto**: an
"encounter" is one program per slot reading the other two and choosing, and what differs between the arms is only the
set of programs and how they read each other.

### 1.2 Churn-capable readers, with executable paths

**Definition (mechanical, fixed now).** Let V\* be the three fair pairs. A class q in slot i is *churn-capable* iff there
are constant programs c_j, c'_j (slot j) and c_k (slot k) such that the joint play (q, c_j, c_k) is the fair pair {i, j}
and (q, c'_j, c_k) is the fair pair {i, k} (**type A**, a reader switching in response to its partner's play), or
constants c_j, c_k, c'_k such that (q, c_j, c_k) is {i, j} and (q, c_j, c'_k) is {i, k} (**type B**, a reader taking the
excluded slot's offer). A template is *counted* as churn-capable in a grammar only if the three-program execution
below, checked by hand (branch priority, negative guards, reciprocal naming, timeouts), takes a fair-pair island to
another fair pair; the tests re-check each path by code.

#### 1.2.1 Arms E, E-min (the DSL of `dollar3`; slots 0, 1, 2 are the notes' i, j, k as labelled)

Atoms are `BOX(THEM_j = a)` with a one of slot j's nine actions; "j names i at 1/2" is the atom whose action is
(partner i, 1/2) in j's coordinates. Constants: C(i,1/2) = name slot i at 1/2.

- **E-A (single-atom fair switcher, size 6).** `if(BOX(THEM_j = (i,1/2)), (j,1/2), (k,1/2))`, i.e. "accept j's fair
  offer, otherwise take k". *Path.* Residents: slot i = E-A, slot j = C(i,1/2), slot k = C(i,1/2). Slot i's box is true
  (j provably names i), so i names j; j names i: fair pair {i,j}, k excluded at 0. A mismatched immigrant X in slot j
  that names k at 1/2: the box is false for the encounters in which X is drawn, so i names k, and k (C(i,1/2)) names
  i: fair pair {i,k} (payoffs 3,0,3). The same holds in the weak arm (the opponents are constants and the simulation
  terminates). Two such classes per slot (j = either other).
- **E-A′ (single-atom, arbitrary atom).** Any size-6 `if(BOX(THEM_j = a), (j,1/2), (k,1/2))` or the swapped table: the
  path is the same with an immigrant whose play changes the atom's truth value; 9 atoms × 2 others × 2 tables, of
  which the 252 classes of the n = 10 catalogue (126 type A, 126 type B) are listed by the scan; they are churn-capable
  only through arbitrary plays of the partner, and only the exact reciprocal ones react to a *fair offer*.
- **E-B (excluded-slot taker).** `if(BOX(THEM_k = (i,1/2)), (k,1/2), (j,1/2))`: names the excluded slot when it
  provably offers a fair share, otherwise j. *Path.* Residents (E-B, C(i,1/2), C(j,1/2)): k offers nothing to i, the
  box is false, i names j: pair {i,j}. An immigrant X in slot k that names i at 1/2 (a "fair offer to a member"): the
  box is true in X's encounters, i names k and X names i: pair {i,k}; j is now at 0 in those encounters. This is the
  spec's churn step in the DSL.
- **E-R2 (two-partner reader, n = 11; built explicitly in E-min).** Slot i: atoms A_j = THEM_j (names i at 1/2),
  A_k likewise; table by (A_j, A_k): (1,·) → (j,1/2); (0,1) → (k,1/2); (0,0) → fallback f ∈ {(j,1/2), null}. Four
  per slot (first partner j or k, fallback "stay with the first" or "null (ALL, 2/3)"). *Path (first = j, fallback
  stay), modal arm.* Residents (R2, C(i,1/2), C(i,1/2)): A_j true, i names j, j names i: {i,j}. Immigrant X in slot j
  naming k: A_j false, A_k true (k is C(i,1/2)), so i names k: {i,k}. Branch priority matters in the other direction:
  with both j and k offering, i takes j. Negative guard: A_k is only consulted when A_j fails. No timeout in the DSL.
  In the weak arm the program is bottom when either atom reads a bottom value (no short-circuit, `eval_weak` needs all
  atoms), which is the arm's own convention and is reported as such.

The atoms are slot-label-relative: "first = j" means the lower-numbered other slot.

#### 1.2.2 The modal arm reads mutually through the free oracle; the weak arm does not

Two readers that read each other cooperate in the modal arm (Löb on the linear GL chain) and diverge in the weak arm
(the least fixed point is bottom, and a bottom slot plays (ALL, 2/3)). So a fair pair *between two readers* exists in the
modal arm and not in the weak arm; in the weak arm a reader pairs only with a constant (or any program that terminates).
This is why arm E′ (weak) is kept beside E (modal): effects of the free oracle are not to be attributed to extensional
reading.

#### 1.2.3 Arm T (L_T^code, cyclic frame; §1.4 gives the frozen settings)

Each program is a closed term `lam me. lam n. lam p. body`, run as `p(⌜p⌝)(⌜next⌝)(⌜prev⌝)` where *next* is slot s+1 and
*prev* slot s−1 (mod 3). An action is a code 0-8 = 3·partner + demand, partner 0 = next, 1 = prev, 2 = ALL, demand
0, 1, 2 = 1/3, 1/2, 2/3 (relative to the program's own slot). Reading the next slot: `SIMN = capk k (run k n p) me`
(the next slot's own arguments are (prev-of-me, me)); reading the previous slot: `SIMP = capk k (run k p me) n`.
"Next names me at 1/2" is the simulated code 4; "prev names me at 1/2" is code 1. The frame is rotation-symmetric,
which a program can use and which the DSL's label order cannot: the DSL breaks the three-way symmetry by labels, arm T
by the programs' own orientations.

- **T-S (single-partner readers, 8):** S{n,p}{o,z}{y,n}. Read the partner (n or p); if it names me at 1/2 (timeout
  counts as "yes" for suffix y, "no" for n), name it at 1/2; otherwise the fallback: o = name the *other* slot at 1/2
  (the switcher), z = null (ALL, 2/3). Churn-capable: the four with fallback o. *Path.* Slot 0 = Sno*, slot 1 = C(4)
  (names its prev = slot 0 at 1/2), slot 2 = C(1) (names its next = slot 0): slot 0's read of slot 1 returns 4, so it
  names slot 1 (code 1): pair {0,1}. Immigrant X in slot 1 = C(1) (names its next = slot 2): the read returns 1 ≠ 4,
  the fallback names prev = slot 2 (code 4), slot 2 names slot 0: pair {0,2}. (Checked by execution: 14 and 15 steps.)
- **T-D (two-partner readers, 8):** D{n,p}{f,z}{y,n}. Read the first partner; accept → name it; else read the second;
  accept → name it; else fallback f = name the first at 1/2, z = null. All eight are churn-capable. *Path.* Slot 0 =
  Dnf*, slot 1 = C(4), slot 2 = C(1): pair {0,1} (read of next accepted, 14 steps). Immigrant in slot 1 = C(3) (names slot 0 at 1/3): the
  first read is rejected, the second read (prev = slot 2 = C(1), names its next = slot 0 at 1/2) is accepted: slot 0
  names slot 2 (code 4), slot 2 names slot 0: pair {0,2} (26 steps). Branch priority: with both partners offering,
  the first wins. Negative guard: the second read happens only after the first fails.
- **T-X (exploiting readers, 2):** X{n,p}: read the partner; if it names me at 1/3 name it at 2/3, if it names me at
  1/2 name it at 1/2, otherwise null. They pair with constants and extract the unfair split; not churn-capable.
- **Timeouts.** Two readers that read each other regress (the same `run` key repeats), the enclosing simulation fuel
  runs out and the read returns TO: the readers then act on their timeout rule. With "yes" they accept, with "no" they
  take the fallback. Three identical orientations therefore *cycle* (every slot names its next at 1/2 and no pair
  forms), whereas a mixed orientation pairs: (Dnfy, Dpfy, ·) forms {0,1} because slot 0 accepts its next and slot 1 its
  prev after the timeouts (414 steps each). This is the T-specific symmetry-breaking fact.

### 1.3 Prior masses at n = 10 (DSL) and the arm-T library prior

Standing DSL, level-0 atoms (`modalPA` and `weak` share them), per slot, from the scan and the prior (scratch (i)-(iii)):

| | n = 6 | n = 10 | n = 11 |
|---|---|---|---|
| canonical functions | 1,305 | 23,337 | 353,817 |
| constants (mass) | 0.9760 | 0.9295 | 0.9228 |
| distinct classes in 6,400 draws (per slot) | about 160 | 380-405 | n/a |
| constants naming a partner at 1/2 (fair establishers) | 0.2169 | 0.2066 | - |
| classes that can form a fair pair with some constants (incl. non-constants) | 0.2246 | 0.2289 | - |
| churn-capable by the mechanical definition (type A + type B) | 18 classes, 3.3·10⁻⁴ | 252 classes, 9.6·10⁻⁴ | - |
| exact reciprocal fair switchers (E-A, 2 per slot) | 1.85·10⁻⁵ each | 4.86·10⁻⁵ each | 4.89·10⁻⁵ each |
| two-partner readers E-R2 | absent | **absent** | 7.2·10⁻⁸ (fb stay), 1.2·10⁻⁸ (fb null), each |

Expected copies per run (64 islands × 100 founders = 6,400 draws per slot): churn-capable 6.1 per slot at n = 10
(2.1 at n = 6), exact fair switchers 0.6, two-partner readers 0. The n = 10 grammar therefore dilutes the
fair-establishing constants by 5% (0.2169 → 0.2066) and raises the churn-capable mass threefold, to under 0.1% of a
slot; nearly every one of those copies sits alone in its island (one of 100). **Prediction in advance: arm E cannot churn
for lack of resident readers**, which is exactly the objection of the spec's reviewers; hence E-min and T.

### 1.4 Arm E-min and arm T: the programs and their prior weights (frozen)

**E-min.** The n ≤ 6 catalogue (1,305 classes) plus, for each slot s, an explicit reader family built in absolute terms
and added to the catalogue (Slots arrays set by hand; three slots × 8 classes): the two exact fair switchers (already in
the catalogue; E-min raises their weight), the two single-atom readers with fallback null, and the four E-R2 classes.
Slot s's seed law: (1 − w_S − w_D)·μ₆ + w_S·uniform{4 single-partner readers of slot s} + w_D·uniform{4 two-partner
readers of slot s}. Doses: **lo** (w_D = 0.003, w_S = 0.087), **main** (0.03, 0.06), **hi** (0.10, 0.06). The mass removed
from the n ≤ 6 prior is removed proportionally (constants lose the same fraction as everything else), and the doses
shift mass only between single-partner and two-partner readers at lo: "weight-matched single-partner replacements".
E-min runs under both evaluators (modal = E-min, weak = E′-min).

**T.** The library of 27 programs, same families as §1.2.3:

| family | programs | main | lo | hi |
|---|---|---|---|---|
| constants C(0)...C(8) | 9 | 0.900 | 0.900 | 0.830 |
| single-partner readers S{n,p}{o,z}{y,n} | 8 | 0.060 | 0.087 | 0.060 |
| two-partner readers D{n,p}{f,z}{y,n} | 8 | 0.030 | **0.003** | **0.100** |
| exploiting readers X{n,p} | 2 | 0.010 | 0.010 | 0.010 |

Within a family the weight is uniform. The main prior keeps the non-constant mass (0.100) in the range of the DSL's
n = 10 prior (0.07) and puts two-partner readers (0.03) below the 0.05 at which the registered counter-prediction of
gemini-4-argon applies. **lo** is the spec's "two-partner readers at one tenth of their weight" (0.003); the removed
0.027 goes to single-partner readers (weight-matched replacements), so the total of flexible readers (singles plus
two-partner) is 0.090 at main and at lo. **hi** (0.10, flexible total 0.160) is the manufactured prior that seeds
islands with flexible readers, at twice the counter-prediction's threshold, to measure the dose response directly.
Expected copies per island-slot population of 100: main 3.0 two-partner and 3.0 churn-capable singles (fallback o); hi
10 two-partner. The same three doses are used for E-min (§1.4 above), so the DSL and the Turing-complete arm are
compared at equal flexible mass.

**Frozen arm-T settings (executable, not idealized).**

- Language L_T^code (`src/lt_code.py`), evaluator `lt_code.evaluate` with its exact step accounting; each program's
  action is the value of its **root evaluation** with fuel **K_R = 1,200** steps (all steps, including every enclosed
  simulation, count). A value that is not a natural number 0-8, or an evaluation that runs out of fuel or gets stuck,
  plays the **timeout action (ALL, 2/3)** (code 8), the same minimax disagreement action as the weak arm.
- Simulation (`run`/`capk`) cap **k = 400** steps per read. A read that exhausts its cap returns the constant TO; the
  template's timeout rule (y/n suffix, X: reject) decides. Nested reads use absolute deadlines, as the evaluator defines.
- **No tape, no certificates, no proofs** in arm T (disclosed in §2.1): reading is by capped simulation, as the RS
  ruled. Tie-breaks are fixed priorities (first partner), both orientations present.
- Price: c = 0 (primary) and, as a sensitivity, **c₀ = 1.2·10⁻⁴ dollars per step**, i.e. 0.12/K₀ with K₀ = 10³, the
  smallest power of ten above the dearest finishing encounter of this library (821 steps, Dnfn against itself);
  a program's payoff is its mark in dollar units minus c × its own root-evaluation steps.
- Encounter payoffs come from executing the 3 programs of each ordered triple (a in slot 0, b in slot 1, c in slot 2):
  slot 0 runs a(next = b, prev = c), slot 1 runs b(next = c, prev = a), slot 2 runs c(next = a, prev = b); the cyclic
  action codes are translated to the game's slot-relative action indices (a swap of the two partner codes in slot 1)
  and the joint outcome is read from `dollar3.outcome`. The 27³ joint table is built once per price.
- Seeds: iid per slot and island from the stated law, `multinomial(N, law)`, founders common across mN.

### 1.5 The homogeneous-reader cell (composition fixed now, outcome verified by the tests)

An island whose three slot populations are entirely churn-capable readers, with 1% and 5% of one *member* slot
replaced by an immigrant class. The aim is to separate "such readers are too rare to win a founding" from "even when
resident, encounter-level switching does not move the island".

- **E, modal:** slot 0 = E-R2(first = lower other = slot 1, fallback stay), slot 1 = E-R2(first = slot 0, stay), slot 2 =
  E-R2(first = slot 0, stay). Hand execution (the GL chain): at world 0 all atoms are vacuously true, slots 0 and 1 play
  names-each-other at 1/2 and that is stable at every later world; slot 2's atoms read slot 0 and slot 1's play (they
  name each other, not slot 2): false, false, fallback stay = name slot 0. Outcome **(3,3,0), pair {0,1}**, slot 2
  excluded. Immigrant classes: the nine constants and the churn-capable singles and E-B.
- **E′, weak:** not realizable as a fully homogeneous cell: two readers that read each other diverge (§1.2.2) and
  play (ALL, 2/3), so a reader pair never pairs. The weak cell is "readers plus a constant partner": slot 0 = E-A(j =
  slot 1), slot 1 = C(slot 0, 1/2) (a constant, not a reader), slot 2 = E-R2(first = slot 0, stay). Hand execution: slot 1 is a constant;
  slot 0's atom reads it and is true, so slot 0 names slot 1 (it does not depend on slot 2); slot 2 reads slot 0 (names
  slot 1, not slot 2: false) and slot 1 (names slot 0: false) and falls back to naming slot 0. Outcome **(3,3,0), pair
  {0,1}**. Labelled as such; it is the nearest weak-arm analogue.
- **T:** slot 0 = Dnfy, slot 1 = Dpfy, slot 2 = Dpfy. Hand execution: slot 0 reads its next (slot 1), which reads its prev
  (slot 0) ...: regress, TO, accept: slot 0 names slot 1 (code 1); slot 1 reads its prev (slot 0), same regress, accept:
  names slot 0 (code 4); slot 2 reads its prev (slot 1), regress through the other two, accept: names slot 1 (code 4),
  unreciprocated. Outcome **(3,3,0), pair {0,1}**. Tie-breaks: first-partner priority; the cyclic triple (Dnfy ×3)
  gives no pair (every slot names its next), which is why the orientations differ.
- **Injection:** the immigrant fraction (1%, 5%) is put into slot 1; immigrant classes are the nine constants and the
  library's churn-capable readers; the island is closed (I = 1, mN = 0) and run for 3,000 generations (§2).

### 1.6 Hand predictions (written after the static scans of §1.0, before any dynamics of the new arms)

Baseline reference (stored migration-window rows, weak arm n = 6; confirmed by the matched rerun): member-to-member flips
per run 2 / 55 / 215 at mN = 0.01 / 0.1 / 1 (mN = 0: none, drift cannot move a closed island); coverage at generation
10,000 of 1.00 / 0.975 / 0.625 / 0.00 at mN = 0 / 0.01 / 0.1 / 1; consensus 0 / 0 / 0 / 0.95.

1. **Arm E (n = 10), modal and weak:** flips per run within 0.7-1.5× of the baseline at mN = 0.01, 0.1, 1 (that is,
   about 1-3, 40-80, 150-320); coverage at mN = 1 equal to 0.00-0.05; the share of islands on V\* roughly the
   baseline's. Reason: 6 churn-capable copies per slot per run, one per island, at 1% of a slot.
2. **E-min:** lo within 0.7-1.5×; main within 1-3×; hi within 1.5-5× at mN = 1, and a flip excess concentrated at mN =
   0.1; coverage at mN = 1 at most 0.10 in all doses. I do not expect the dose to produce 10× churn: a reader that is
   resident in a member slot changes its own encounters when a mismatched immigrant arrives, but the immigrant's slot
   population is 99% resident, and selection acts on populations.
3. **Arm T, c = 0:** lo within 1-2×, main within 1-3×, hi within 2-6× of the baseline's flips; coverage at mN = 1 at
   most 0.10 (hi at most 0.25). The cyclic symmetry makes some resident reader triples pairless (a cost of flexibility),
   and a pairless island is dominated by whichever pair a migrant restores. The c₀ sensitivity changes a readers-only
   island's payoff by up to 0.1 (the regress costs) and should lower reader shares, not raise flips.
4. **Probe (excluded slot's fair offer):** a single reader in a member slot or a single immigrant of any class switches
   the island's pair in under 5% of injections in the stratum with constant members; with churn-capable member
   residents, 5-15% at an immigrant share of 1% and higher at 5% in the homogeneous-reader cell, because the reader's
   redirect gives the excluded slot a positive payoff that selection can use; sham replacements (injecting a copy of a
   resident) switch the island in under 1%. Naming-preserving immigrants switch under 3%.
5. **Coverage and mN:** high at mN = 0 and 0.01 in all arms (founder diversity, 1.00 and ≥ 0.9) and falling to ≤ 0.1
   by mN = 1; it is not a measure of churn (it falls because consensus is reached). Island-level flips are *not*
   expected to follow the veto's 20-60× excess in any arm; the highest ratio I expect is in T-hi (2-6×).
6. **Where I am least sure:** T-hi and E-min hi (resident two-partner readers in many islands), and the probe stratum
   with reader members. Those are the cells where a ≥ 10× excess would not surprise me; if one appears the
   mechanism question (redirect versus drift versus exploitation of unconditional seeds) is what the report must answer.
