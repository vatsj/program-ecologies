# Drafts for the shared docs, from the arm-T islands run (2026-10-29)

Hand-back of the engineer. Nothing here is in RESULTS, REJECTED, THEORY, NOTATION, DEFERRED or CLAUDE.md. Sources: `runs/many-islands-t.md`
and `.json`, `runs/many_islands_t/`, `notes/many-islands-t.md`, `predictions/2026-10-29-many-islands-t.md`; code `src/many_islands_t*.py`,
`tests/test_many_islands_t.py` (18 tests).

## 0. The plain statement for the RS

In the order of limits "annealed mutation, rare migration, islands to infinity before time", at the default charge A_f (P_fail = 0.1), the
Turing-complete readers arm (27 programs of L_T^code, fixed fuel caps) **meets the target's first clause exactly**: the exact mean-field equation puts
every island on a fair pair (V\* = 1 - 6·10^-8 at worst, grand coalition the only residue) from the natural law and from every tilted start
(fair, unequal at 0.6, wasteful or disagreement at 0.6), at P_fail 0, 0.03 and 0.1, at all three doses, at A = 0 and 150; V\* ≥ 0.99 by about
5·10^3 events per island. The charge changes the composition of the limit (readers 100% of programs at P_fail 0, 50% at 0.1) and slows
conversion by 0.015 of V\* at 10^3 events, nothing more. The **second clause** (each pair equally likely across worlds) holds in the form
the restated target asks for: the symmetric state with the three pairs present is exactly a knife-edge (growth rate 5.5·10^-4 per event per island,
the same at 0.1, a sampling tilt of 0.3-2% breaks it by 10^4 events), finite worlds end on one pair and the three pairs are equally likely across worlds
(155 single-pair worlds, chi-square p = 0.41). **Where it fails:** (i) small worlds: at P_fail 0.1 an *unequal* consensus ends 5, 2, 2 and 0 of 20 worlds at I = 64, 256, 1,024 and 4,096 (to 10^5 events per island;
5, 1, 0 in the long runs; 0 of 10 at 16,384); (ii) constants alone reach V\* = 1 in the mean field from every start, which contradicts the
"constants are bistable" prediction, but finite worlds of constants end on an unequal consensus in 8-11 of 20 at every I from 64 to 4,096 and in 1 of 10 at
16,384 (the incidence falls only above 4,096); the readers are what makes the finite worlds robust. A positive result of this size is a property of this
27-program library, these fuel caps and this order of limits.

## 1. RESULTS draft

```
## Arm T under islands to infinity before time: the exact mean-field limit puts every island on a fair pair from every start and at every charge, the symmetric state is the same knife-edge, and the readers (not the charge) decide whether finite worlds stay fair (2026-10-29)

Spec `specs/2026-10-29-many-islands-t.md` (queue number to be set by the RE; the RS: "Sgtm - I see farsightedness as a band-aid antithetical to the rest of the
program"; the target restated, DEFERRED 15: every island in V\*, each member equally likely across independent worlds; reviewed by gemini-4-argon then
gpt-6.1-sol, folded), predictions `predictions/2026-10-29-many-islands-t.md`, notes `notes/many-islands-t.md`, report `runs/many-islands-t.md` and
`.json`, rows `runs/many_islands_t/`. Run by a Sonnet subagent (`src/many_islands_t*.py`; 18 tests).

**Object.** Arm T of the churn experiment (27 programs per slot of L_T^code, cyclic frame, simulation cap 400, root fuel 1,200; the nine constants, eight
single-partner readers, eight two-partner readers, two exploiters) in the exact object of "Islands to infinity before time": a settled island is a program
triple (27^3 = 19,683 states); one migrant is a constant-fitness two-type Moran process with the closed-form fixation probability; the I → ∞ dynamics are an exact
ODE on the triple simplex (time in migrant events per island), the finite-I dynamics the jump chain with the same kernel. The default charge A_f is a payoff in
dollars (the unit of the stored PAY, on which w = 0.3 acts): P_fail per failed read in the root's own trace plus P_fail per forfeit. Only founding plus annealing are
simulated (3 pools of 16,384 islands per cell, 11 cells: doses 0, lo, main, hi at P_fail 0 and 0.1, main at 0.03, main at A = 150).

**Validation.** The 27^3 table reproduces the stored arm-T tables on every triple (0 mismatches in action, steps and joint code; the step-price path agrees to
0); the failed-read counter obeys the A_f rules on hand programs (one charge per failed read, an enclosing expiry not double counted, a forfeit once, a failed read
followed by a loop twice); **the table has no forfeit in 3 × 19,683 root evaluations** (the root fuel 1,200 is never reached; two expired reads cost 821 steps), so the two ODE controls
(failed reads without the forfeit charge, forfeits without failed reads) are A_f itself and the zero-charge table; failed reads occur only in triples whose root reaches a read cycle
(0 violations in 59,049 roots) and are at most 0, 1, 2 for constants, single readers and exploiters, two-partner readers; the table is exactly rotation-equivariant (0
violations in payoff, charge, steps, class, excluded slot and the 3 × 27^4 kernel tensor). The exact kernel agrees with simulated relaxation of the island kernel in 10 strata
(selection × timeout pattern, 200 injections each, 475,415 draws from the post-anneal law and from the ODE at 10^3 events, all |z| < 0.8); the ODE reproduces the logistic and voter
solutions, conserves mass to 2·10^-15, and agrees with the archipelago at I = 4,096 to 0.002 (P_fail 0) and 0.0003 (0.1) in V\* at 10^3 events. Founding at main, P_fail 0 gives
V\* 0.528 ± 0.004 against the churn experiment's 0.532 [0.511, 0.552].

**The mean-field limit.** All 162 symmetric trajectories (11 cells × 4 starts × 3 pools, the crossed charges and the ablations) meet criterion (a) (||dx/dt||_1 < 10^-9
and every class share moving < 10^-4 over the last decade) at 3·10^6-10^7 events per island with V\* ≥ 0.9999998 and the grand coalition ≤ 6·10^-8; at 10^4 events V\* is ≥ 0.9959 and at 10^5
≥ 0.9979 in every trajectory. V\* by events per island, natural start, mean over pools:

| cell | 0 | 10^2 | 10^3 | 10^4 | 10^5 | limit |
|---|---|---|---|---|---|---|
| dose 0 | 0.281 | 0.350 | 0.503 | 0.9971 | 0.9981 | 1 |
| lo, P_fail 0 | 0.523 | 0.625 | 0.883 | 0.9984 | 0.9991 | 1 |
| main, 0 | 0.528 | 0.631 | 0.889 | 0.9985 | 0.9992 | 1 |
| main, 0.03 | 0.527 | 0.629 | 0.883 | 0.9988 | 0.9993 | 1 |
| main, 0.1 | 0.522 | 0.622 | 0.874 | 0.9989 | 0.9993 | 1 |
| hi, 0 | 0.690 | 0.784 | 0.958 | 0.9990 | 0.9995 | 1 |
| hi, 0.1 | 0.666 | 0.759 | 0.944 | 0.9992 | 0.9995 | 1 |
| main, A = 150, 0 / 0.1 | 0.599 / 0.590 | 0.648 / 0.638 | 0.878 / 0.862 | 0.9984 / 0.9984 | 0.9991 / 0.9990 | 1 |

From the tilted starts (main, P_fail 0.1: unequal 0.293, fair 0.600, wasteful/disagreement 0.258 at t = 0) V\* reaches 0.99 at 5·10^3 events and 0.999 at 1-5·10^4 on all four starts; there is **one basin
at every cell**, including dose 0 (constants only), where the unequal tilt (V\* 0.196) goes to V\* 1 and U to 0. The solver checks (tolerance 10^-8 against 10^-10, backward Euler 8 against 16 steps per decade) move no class
share by more than 3.2·10^-9. The conversion carriers (exact rates at the post-anneal law): wasteful and disagreement islands become fair at 0.0068 and 0.011 per event, unequal ones at
0.0010; per migrant the single-reader and two-partner families convert 2.5-3.5 times as fast as constants (wasteful: 0.0156 and 0.0166 against 0.0050; disagreement: 0.0253 and 0.0264 against 0.0083) and exploiters 1.7 times.
Ablations at the main dose (a family removed, mass to the constants): every limit is V\* 1; at 10^3 events V\* is 0.889 (none), 0.781 (switchers S..o.. removed), 0.819 (two-partner removed), 0.883 (exploiters removed).

**The limit is built of readers when reading is free.** At P_fail 0 the limit holds 1,046 triples, all of them reader triples (the switchers Snoy and Spoy, which accept a timed-out read, plus a little Dpfy), reader marginal 1.0000
(0.176 at the start, 0.29 at 10^3, 0.57 at 10^4, 0.999 at 10^5); dose 0's limit is the six fair triples of C1 and C4 (names the neighbour at one half). At P_fail 0.1 the limit holds 133 triples, reader marginal 0.501 (0.166, 0.237, 0.265, 0.501 at the same times),
the pairs built of a constant C4 and a reader that does not cycle (Snon, Snoy, 0.34% failed reads per play); the share of encounters with a failed read in some slot is 0.0017 against 0.0118 at the founding law.
The charge does not touch V\* (any pool, any start), moves the limit's composition, and slows conversion slightly; founding at 0.1 against 0 changes the post-anneal reader marginal by 6% and V\* by 0.006, and crossing the founding and migration charges (four cells) shows the migration charge alone sets the limit's composition.

**The knife-edge.** On the rotation-non-invariant sector the Jacobian at the symmetric limit has largest real part 5.556·10^-4 per event at P_fail 0 (= 0.01/18), 5.508·10^-4 at 0.1 and 4.635·10^-4 at 0.03 (the same at every dose and at A = 150 for a given charge; one positive eigenvalue at 0, two at 0.1; the full-space Arnoldi
gives the same numbers), the leading eigenvector is entirely on the fair-pair classes (one pair up, one down, the phases 2π/3 apart) and the other eigenvalues are negative or zero (leak out of the support 10^-14).
Symmetry-breaking perturbations of 10^-6, 10^-4 and 10^-2 along the eigenvector and along a random non-invariant direction grow at 5.55·10^-4 (fitted; 5.50·10^-4 at 0.1), the Jacobian's rate to three digits, in every cell.
The raw pool laws, with a pair imbalance of 0.1-2.3%, put more than half of V\* on one pair by 1-5·10^4 events and end (10^6) with one pair holding 0.46-1.0 of V\*, at every cell. Finite worlds: the time to the first loss of a fair pair
grows slowly with I (medians at P_fail 0, I = 64 / 256 / 1,024 / 4,096: 2.4 / 8.0 / 13.5 / 18.8·10^3 events per island; 3.1 / 7.9 / 11.2 / 16.0·10^3 at 0.1), only 1 of 20 worlds keeps all three pairs ≥ 0.05 at I = 1,024 (both charges), and the pairs a world ends on are
equally likely (44 / 54 / 57 over the three, chi-square p = 0.41; per cell p ≥ 0.16). At I = 1,024, 20 of 20 worlds (P_fail 0) and 18 of 20 (0.1) end with ≥ 0.99 of islands on fair pairs.

**Where finite worlds depart from the limit.** Worlds that end on an *unequal* consensus (≥ 0.99 of islands on one unequal pair), of 20, by I = 64 / 256 / 1,024 / 4,096 (to 10^5 events per island; independent long runs to 10^6-10^7 give the same incidence for the readers):
main at P_fail 0.1: 5 / 2 / 2 / 0 (and 5 / 1 / 0 in the long runs, 0 of 10 at 16,384); main at 0: 4 / 0 / 0 / 0 (2 / 0 / 0 long); **dose 0 (constants only): 8 / 9 / 9 / 8, 11 / 8 / 9 in the long runs, 1 of 10 at 16,384, 0 of 6 at 65,536 (to 3·10^4 only)**.
The same constants-only ODE has one basin: the finite worlds disagree with the mean field at the times probed, not by a linear instability of the limit (all eigenvalues of the single-pair endpoint are zero within 10^-6) but by drift of single triples to absorbing consensus states at I ≤ 4,096; unequal-tilted worlds give the same picture. With readers the incidence falls with I
and is zero from I = 1,024 (both charges), so the readers are what protects the fair consensus against that drift, not the charge.

**Arm T against the DSL readers arm R, a description.** One reader and two constants: the two tables give the same outcome in all 3,888 triples (modalPA and weak). Two readers and a constant: they differ in 2,649 of 6,912 triples (modalPA; 38%, 2,397 changing the outcome class)
and 1,845 (weak; 27%); three readers: 2,100 of 4,096 (51%) and 1,728 (42%). Fuel decides whether a fallback runs, so the differences are not attributed to the timeout action.

**Verdicts.** P1 held (V\* 1.00000 at convergence in all three pools); P2 held (1.00000 from the unequal and the wasteful/disagreement tilts); **P3 failed** (dose 0: the unequal tilt goes to V\* 1, U to 0, at both charges; the bistability of the DSL L arm is not a property of constants alone in the mean field);
P4 held (lambda > 0 at both charges; 1 of 20 worlds keep three pairs at I = 1,024; 20/20 and 18/20 worlds ≥ 0.99 fair; the finite-world clause scored since lambda·10^5 = 55 > ln √1024 = 3.5); P5 held (V\* 1.00000 at P_fail 0.1 from the natural law and from the unequal tilt; **both counter-predictions fail on V\***: gemini-4-argon's (V\* < 0.9 from the unequal tilt, readers repel each other under the charge) and gpt-6.1-sol's V\* caveat;
the part of gpt-6.1-sol's that holds is the lower reader marginal and slightly slower conversion, 0.501 against 1.000 at the limit and V\* 0.874 against 0.889 at 10^3); P6 partial (the limits do not separate, both ablations leave V\* 1; at finite time the switchers matter more than the two-partner readers, 0.781 and 0.819 against 0.889 at 10^3);
engineer E1-E9 all held (E6-E8 are vacuous at the limit, held also at 10^3 events, where V\* is monotone in the charge and the dose); the zero-forfeit prediction E1 made the forfeit-charge controls vacuous.

**Scope.** A positive result for this 27-program library, these fuel caps, the cyclic frame and this order of limits; the table is a hand-built library, not a general realizable language. Cuts: none of the spec's cut order was applied; the ablations were run at natural start only and the switchers S..z.. were not ablated. Added beyond the spec: tilted worlds,
long worlds and worlds at I = 16,384 and 65,536, the DSL table comparison, per-migrant conversion rates.
```

## 2. REJECTED draft entries

- **"Constants alone are bistable in the mean field" (RE prediction 3, 2026-10-29).** Failed as registered: at dose 0 (the nine constants only) the exact ODE reaches V\* = 1 from the natural law, the fair tilt, the unequal tilt (V\* 0.196 at the start) and the wasteful/disagreement tilt, at P_fail 0 and 0.1 (RESULTS "Arm T under islands to infinity before time"). The DSL L arm's unequal basin needs the length prior's conditional programs. Finite worlds of constants are bistable in outcome (unequal consensus in 8-11 of 20 at I ≤ 4,096), which is a finite-size effect, not a second basin of the mean field.
- **gemini-4-argon's counter-prediction to prediction 5 (readers repel each other under A_f; V\* < 0.9 from the unequal tilt, possibly from the natural law).** Failed: V\* = 1.00000 at P_fail 0.1 from every start and pool; the charge halves the readers' share of the limit (1.0 to 0.5) and slows conversion by 0.015 of V\* at 10^3 events. Same section.
- **gpt-6.1-sol's counter-prediction (V\* ≥ 0.95 not confidently predicted at A_f; conversion slower, possibly basin-dependent).** Partial: the reader marginal is lower and conversion slower, by little, with one basin; the V\* caveat did not materialize. Same section.
- **RE prediction 6 (removing the switchers lowers the V\* limit more than removing the two-partner readers).** Partial: no ablation moves the limit (every limit is V\* 1); at 10^3 events the direction holds (0.781 against 0.819 against 0.889).
- **The "forfeits charged without failed reads" and "failed reads charged without forfeits" ODE controls of question 5.** Dropped as vacuous: the 27-program table has no forfeit (E1), so they equal the zero-charge cell and A_f.
- **Engineer E6-E8 as tests.** Vacuous at the limit (V\* = 1 everywhere); they hold at 10^3 events, where V\* is monotone in the charge, the dose and (within 0.011) the annealing.

## 3. THEORY draft

Add to §9.2 (or the realizable-arm paragraph of §5) with the reason "RESULTS 'Arm T under islands to infinity before time'": *In the order of limits (annealed mutation, rare migration, islands to infinity before time), a Turing-complete source-reading library that contains single-partner and two-partner readers with timeout-accepting fallbacks meets the first clause of the stable-set target in the exact mean field: every island lands on a fair pair from every start tested, at zero and at the default compute charge; the charge reshapes the limit (readers are half the programs, not all) and does not move V\*. The symmetric state with all three pairs present is exactly a knife-edge (growth rate 5.5·10^-4 per event per island, 1/1800 to four digits, independent of dose, a few per cent lower at 0.1), and the equal-likelihood clause is a lottery over pairs across worlds. Finite worlds depart from the mean field by an absorbing-consensus drift at small I, whose incidence falls with I only when readers are present. This is a statement about the tested 27-program library, not a theorem about realizable readers.* Operating hypothesis unchanged (DEFERRED 1, 15): the unequal basin of the DSL arms L and M is a property of the length prior's programs, not of reading.

## 4. NOTATION draft

- **Many islands, arm T:** **arm-T library** — the 27 programs of `churn_primary_t` (9 constants C0..C8; single readers S{n,p}{o,z}{y,n}; two-partner readers D{n,p}{f,z}{y,n}; exploiters Xn, Xp; names read direction, fallback, timeout flag: `y` accepts a timed-out read); **triple** — the program triple (a₀, a₁, a₂) of a settled island, 27³ = 19,683 states; **x** — the law of the island triple (the mean-field state), **q_s(y)** — its slot-s marginal (the donors); **PF[s, t, y]** — the exact fixation probability of a slot-s migrant y into the settled triple t; **R** — the cyclic rotation (a₀, a₁, a₂) → (a₂, a₀, a₁), **non-invariant sector** — functions with R = ω or ω̄ (ω = e^{2πi/3}); **symmetric / raw trajectory** — the ODE from the rotation-averaged pool law with the field projected on the invariant subspace / from the unsymmetrized pool law; **start nat / fair / uneq / wd** — the symmetrized post-anneal law, or with F / U / W + D rescaled to 0.6 keeping within-class frequencies; **criterion (a)** — ||dx/dt||₁ < 10⁻⁹ and every class share moving < 10⁻⁴ over the last decade of events (horizon extended to 10⁷), **(b)** V\* ≥ 0.99 at 10⁵, **(c)** finite-world consensus; **λ** — the largest real part of the Jacobian at the symmetric limit on the non-invariant sector; **S, leak rate** — the support of x\* (x\* ≥ 10⁻⁹) and the flux out of it; **failed read** — an `enter_sim` frame that closes on TO (an enclosing expiry is not counted separately); **forfeit** — a root that runs out of fuel, is stuck or returns a non-number; **P_fail** — the charge per failed read and per forfeit, in dollars (w = 0.3 acts on dollars, the unit of `stable_sets.Tables.PAY`); **founding × migration charge** — the P_fail used to settle the pools / in the kernel PF; **consensus** — a finite world with ≥ 0.99 of its islands on one pair; **unequal consensus** — ≥ 0.99 on unequal pairs.

## 5. For the RE (what changes the program)

1. The restated target's first clause holds in the exact mean field for arm T at the default charge, including from the unequal start: the unequal basin of L and M is a feature of the length prior. The charge does not matter for V\*.
2. The second clause is a knife-edge lottery, as in arm R (the growth rate 5.5·10^-4 per event is 0.01/18, set by the neutral 1% fixation, so it will not depend on the library).
3. The new finding is the finite-I behaviour at small I (an unequal consensus in 25% of worlds at I = 64 for the readers, ~45% for constants at every I ≤ 4,096): if the object is "islands to infinity first", the mean field is the answer, but the approach to it is slow and library-dependent. A follow-up could test whether a mutation-free finite metapopulation of 10³ islands with readers is already in the regime (it is: 0 of 20 worlds at I = 1,024).
4. Open item for the RS: whether "each member equally likely across independent worlds" is satisfied by a lottery that is symmetric in law but not within a world (it is the same lottery as arm R's).
