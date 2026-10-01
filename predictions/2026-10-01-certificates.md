# Predictions: a certificates-only arm (tags, D-seeded and C-seeded reasoned certificates), 2026-10-01

Status: reviewed by astra (`reviews/2026-10-01-certificates-gpt-6-astra.md`) and fable
(`reviews/2026-10-01-certificates-fable.md`), then revised; changes are marked [after review]. Committed before any
chain cell is run beyond the declared smoke test. Only static single-edge rates have been computed, and they are
quoted.

Code:
- `src/certificates.py`: the language and the evaluators;
- `src/certificates_limN.py`: static rates with `--static`, and the chain cells otherwise;
- `tests/test_certificates.py`: the reference check.

**Question.** Without simulation and without provability, are certificates enough for lim_N efficiency in the
PD? And is the cooperation they support universal or parochial?

## The arm

**Certificates.** Each program publishes a certificate. It observes only its opponent's certificate, never its
source or its behaviour.

Certificates are honest by construction: the certificate *is* the rule. It is a propositional formula over
certificate atoms, and the program's action against an opponent is the formula's value. So "holding certificate K"
and "behaving as K describes" are the same thing, and a program cannot hold K without K's behaviour.

**Language and node costs.** Node for node, this is the grammar of the matched control (W0 / M0,
`src/matched_control.py`). So the length prior μ over syntax is identical to M0's.

    A   ::= C | D | not A | and A A | or A A | ATOM(App)
    App ::= THEM(ME) | THEM(THEM) | THEM(^A)

- `C`, `D`: 1 node.
- `not A`: 1 + |A|.
- `and A B` and `or A B`: 1 + |A| + |B|.
- `ATOM(THEM(ME))` and `ATOM(THEM(THEM))`: 3 nodes, since the atom is the application node.
- `ATOM(THEM(^A))`: 3 + |A|.
- Bits: log2 a(|p|) + 2 log2 |p| + 1, as in every arm.

There are 666 / 2,796 / 11,462 / 49,852 / 216,292 / 965,158 programs at n = 6 to 11. There is no X and no `ROLE`.

**Variants.** Only the meaning of an atom differs between them.

| variant | atoms | meaning |
|---|---|---|
| **tag** | `EQ(ME)`, `EQ(^A)`; `EQ(THEM)` is a tautology and folds to C | "I cooperate with holders of K": the opponent's certificate is equivalent to mine, or to A. Equivalence is propositional, over atoms treated as independent. |
| **tageq** [after review, fable] | the same | Equivalence uses the *equality axioms*: the atoms of one certificate are equalities of the opponent's certificate to distinct certificates, so at most one is true. Two certificates are equivalent iff they agree when no atom is true and when exactly one atom (up to equivalence of its argument) is true. Behaviour is read off that exclusive assignment. So `and(EQ(ME),not(EQ(^D)))` ≡ `EQ(ME)`. |
| **lfp** (D-seeded) | `IMP(THEM(ME))`, `IMP(THEM(THEM))`, `IMP(THEM(^A))` | "The opponent's certificate implies it plays C against me / itself / A", read *inductively*: synchronous Kleene iteration of the joint system v[x, y] = f_x(atoms read off v), seeded at all-D. On monotone parts this is the least fixed point, so a loop with no grounding resolves to D. |
| **gfp** (C-seeded) | the same | Read *coinductively*: seeded at all-C. On monotone parts this is the greatest fixed point, so a positive loop resolves to C. |
| **lob** | `BOX(THEM(·))` | Provability in PA (`modal.py` with the PA box only). This is M0 of the matched control, and the reference. Its fixed points are unique up to provable equivalence. |
| **lob1** [after review, fable] | `BOX1(THEM(·))` | Provability in PA + Con(PA), at the same grammar. This is the reader-strength control for verdict 7. |

[after review, astra] With negation the system is not monotone, so "lfp" and "gfp" are names for the D-seeded and
C-seeded iterations. They are exact least and greatest fixed points only on `not`-free programs.

**The divergence rule.** A pair whose iteration enters a cycle of period greater than 1 gets D, the minimax action,
as divergent pairs do in the weak arm. The cycle comes from negated self-reference, for example
`not(IMP(THEM(ME)))` against itself. Detection is exact: the whole matrix is iterated until it repeats, and pairs
that vary on the terminal cycle are divergent.

At n = 10 there are 819 divergent pairs out of 8,836 canonical pairs (3,313 at n = 11). [after review, astra and
fable] The D fallback can break the equations of settled pairs that read a divergent pair:
- 8 settled pairs at n = 10 (77 at n = 11) are not reproduced by one more Kleene step;
- their μ×μ weight is 1.6·10⁻¹⁰ (2·10⁻¹⁰ at n = 11);
- this is negligible, and is reported per cell.

**Stratified certificates are not run.** These can mention only lower-level certificates: no `ME` and no
`THEM(THEM)`. They contain only third-party probes such as `IMP(THEM(^C))`, which are the lfp arm's cooperators and
are fakeable (below). So stratification lands on the lfp result, not on tags.

**The design issue, and what it re-opens.** Reasoned certificates are self-referential. FairBot's certificate,
`IMP(THEM(ME))`, says "I cooperate with you if yours implies you cooperate with me", and two copies refer to each
other. A decidable logic without Löb's rule must pick a fixed point:
- D-seeded picks mutual defection between copies.
- C-seeded picks mutual cooperation.
- Löb picks nothing: the fixed point is unique (de Jongh–Sambin).

Choosing C-seeding is a selection rule. **This re-opens REJECTED "Black-magic fixed points"**, which asked that any
such arm state its rule. The rule here is: C-seeded synchronous iteration, with D on pairs that never settle. The
justification for re-opening is that, at an identical grammar and prior, the arms separate what the modal arm's
result owes to its semantic regime.

[after review, astra] The contrast is between *semantic regimes*, not only between fixed points of one equation
system. Provability and truth on stable values are different operators, and lob1 and the ablation below isolate
the mechanism.

C-seeding also **partly re-opens REJECTED "Forced-cooperate on timeout"**. With a finite budget, C-seeded iteration
*is* "out of budget → C". With T → ∞ only genuine loops are affected; verdict 8 tests the exploitation question.

**Order of limits** [after review, astra]:
1. ε → 0 at fixed N and fixed n;
2. then the N grid, at n = 10 and n = 11.

Claims about lim_N are statements about these finite languages. One claim holds at every n: in the gfp arm,
FairBot's mirror property (below) is semantic, so no program in any L_n has a strict or faker exit from all-FairBot.

**Evaluator checks (done).**
- `tests/test_certificates.py` enumerates syntax trees and evaluates every pair without canonical forms. It covers
  lfp and gfp (Kleene iteration over tree pairs), tag (an independent truth-table equivalence check) and tageq
  (signatures computed on trees). Every pair agrees with the canonical evaluator: all 182 programs at n = 5, and
  for lfp, gfp and tag all 666 at n = 6. On `not`-free programs there are no divergent pairs, both results are
  fixed points, and gfp ≥ lfp.
- lob reproduces M0 by construction, since it calls the same evaluator.
- lfp is **not** W0. They differ on 1,140 of 443,556 program pairs at n = 6, for example `or(THEM(ME),C)` against
  itself. W0's operational evaluation lets a divergent left operand poison the whole pair; lfp sets the looping
  atom to D locally.

## Static structure (n = 10)

| | tag | tageq | lfp | gfp | lob | lob1 |
|---|---|---|---|---|---|---|
| classes | 43 | 33 | 82 | 82 | 25 | 25 |
| main conditional cooperator | `EQ(ME)` | `EQ(ME)` | `IMP(THEM(^C))` | `IMP(THEM(ME))` | `BOX(THEM(ME))` | `BOX1(THEM(ME))` |
| μ of its class | 0.0077 | 0.0077 | 0.0024 | 0.0078 | 0.0079 | 0.0079 |
| conditional cooperators (self-C, D on D), μ | 8, 0.0082 | 5, 0.0082 | 7, 0.0024 | 25, 0.018 | 5, 0.018 | 5, 0.018 |
| mutual-cooperation components among them | **6** | **4** | 1 | 1 | 1 | 1 |
| main mutually cooperates with … of the others | **0 of 7** | **0 of 4** | 5 of 6 | 21 of 24 | 4 of 4 | 4 of 4 |
| μ-weighted pairwise coverage among them [after review] | 0.000 | 0.000 | 0.908 | 1.000 | 1.000 | 1.000 |

Here μ(C) = μ(D) = 0.487 in every reasoned variant, and 0.495 / 0.489 in the tag variants. In lfp,
`IMP(THEM(ME))` defects on itself.

**The gfp FairBot is a mirror.** `IMP(THEM(ME))` plays against y exactly what y plays against it, under any
consistent fixed point. So every pair it plays is (C,C) or (D,D). Two consequences follow, by construction, like
soundness in the modal arm:
- it has no faker or strict invader;
- it enters all-D neutrally.

Its "universality" is the same identity, so it carries no further information [after review, fable]. The 3
conditional cooperators it does not cooperate with are probes against a rival reference program, such as
`IMP(THEM(^not(IMP(THEM(^C)))))`, with total μ 2·10⁻⁶. They defect on FairBot, and FairBot mirrors that.

The Löb FairBot is not a mirror. It defects on cooperators whose cooperation PA cannot prove; that is one-way
exploitation *by* FairBot.

**The coinductive probe is fakeable where the provability probe is not.**
- *The faker.* `IMP(THEM(THEM))` means "cooperate iff you cooperate with yourself". The 5-node program
  `not(IMP(THEM(^C)))`, "cooperate iff you defect against ALLC", fakes it. It cooperates with itself, defects on
  `IMP(THEM(THEM))`, and is cooperated with.
- *Its rate.* The μ-weighted rate is 1.1·10⁻⁴ per mutation event, independent of N.
- *Under provability.* The same program does not fake `BOX(THEM(THEM))` or `BOX1(THEM(THEM))`. Its
  self-cooperation rests on a negative fact, that it defects on ALLC, which no consistent reader proves.
  C-seeded truth sees it.
- *Remaining fakers.* Löbian fakers of the probe have total μ 3·10⁻⁷ under PA and 1.2·10⁻⁶ under PA + Con(PA),
  against 4.5·10⁻⁴ under gfp.
- *Interpretation.* "Fakeable" is not dishonesty: the faker's certificate is true. The probe is a bad test, as
  `THEM(^C)` was in the weak arm.

**Static single-edge rates, w = 0.3**, per mutation event: μ × the Moran fixation probability.

| N | ρ(main \| all-D), every arm | gfp FairBot: faker / neutral | gfp `IMP(THEM(THEM))`: faker / neutral | lfp `IMP(THEM(^C))`: faker / neutral | tag `EQ(ME)`: any exit above 10⁻¹³ |
|---|---|---|---|---|---|
| 10² | 0.0421 | 0 / 5.0·10⁻³ | 1.2·10⁻⁴ / 5.0·10⁻³ | 6.4·10⁻⁴ / 4.9·10⁻³ | none (deleterious, 9·10⁻⁹) |
| 10³ | 0.0136 | 0 / 5.0·10⁻⁴ | 1.2·10⁻⁴ / 5.0·10⁻⁴ | 6.3·10⁻⁴ / 4.9·10⁻⁴ | none (10⁻⁴⁰) |
| 10⁴ | 0.0044 | 0 / 5.0·10⁻⁵ | 1.2·10⁻⁴ / 5.0·10⁻⁵ | 6.3·10⁻⁴ / 4.9·10⁻⁵ | none |
| 3·10⁴ | 0.0025 | 0 / 1.7·10⁻⁵ | 1.2·10⁻⁴ / 1.7·10⁻⁵ | 6.3·10⁻⁴ / 1.6·10⁻⁵ | none |

**Static estimate of P(C,C).** This is the embedded monomorphic chain built from these single-edge fixation
probabilities, with kstar = N and no replicator fates. Transitions below 10⁻¹³ are dropped (see "Numerics"). The
"ablated" column suppresses the faker edges out of `IMP(THEM(THEM))` [after review, astra and fable].

| N | tag, tageq | lfp | gfp n=10 | gfp n=11 | gfp ablated | lob n=10 | lob1 n=10 |
|---|---|---|---|---|---|---|---|
| 10² | 1.000 | 0.020 | 0.136 | 0.137 | 0.137 | 0.138 | 0.138 |
| 10³ | 1.000 | 0.029 | 0.299 | 0.299 | 0.319 | 0.319 | 0.319 |
| 10⁴ | 1.000 | 0.015 | 0.478 | 0.477 | 0.584 | 0.584 | 0.584 |
| 3·10⁴ | 1.000 | 0.009 | 0.575 | 0.575 | 0.707 | 0.706 | 0.706 |

The static support at N = 3·10⁴ is as follows:
- *gfp:* FairBot 0.50, `IMP(THEM(THEM))` 0.06, D 0.42. Ablated, the probe holds 0.35.
- *lob:* FairBot 0.36, `BOX(THEM(THEM))` 0.35, D 0.29.
- *tag:* `EQ(ME)` 0.9999.
- *tageq:* `EQ(ME)` 1.0000.

**The static estimate is effectively the prediction** [after review, fable]. Exits in lfp, gfp and lob are pure
dominance or neutral drift, and `eager_poly=False` was exact for M0. So the chain cells validate the static table,
and fable's two-state estimate was exact for M0. The new content is in three places:
- the mechanism ablation;
- the lob1 control;
- the tag structure.

**Smoke test (declared).** The chain driver was run once at n = 6, N = 100. P(C,C) came out tag 1.000, lfp 0.0171,
gfp 0.1285 and lob 0.1292, the last equal to M0's committed 0.1292. In the gfp cell the π-weighted faker flux was
6.4·10⁻⁴, with a loop-only part of 0. No other chain cell has been run.

**Numerics.** A clique's exits are deleterious fixations of order e^(−Θ(N)). At N ≥ 10³ they are below double
precision next to a self-loop of 1 − O(e^(−Θ(N))), so the stationary solve cannot resolve them. Unfloored, the static
solve put all mass on a 10⁻⁴-μ clique at N = 10³, which is noise. So the driver:
- drops transition probabilities below 10⁻¹³ relative to their row;
- reports the largest dropped stationary flow;
- recomputes π.

Clique states then become closed. With several closed classes the chain is an absorption lottery from the
μ-weighted seeds (rule 5), and it is reported as such: as the *metastable* split, not as π [after review, astra].

Alongside it, each tag cell reports an effective inter-clique split, π_A ∝ lottery_A / escape_A [after review,
astra]. Here escape_A is the log-space total exit rate of all-A, computed without underflow. This is a one-step
approximation: an escape is assumed to be re-absorbed by the global lottery. The tolerance is also rerun at 10⁻¹¹.

## The run

ε→0 chain, PD, w = 0.3, N ∈ {10², 10³, 10⁴, 3·10⁴}, `eager_poly=False`, at most 3 worker processes. Cells:
- tag, tageq, lfp, gfp and lob at n = 10 (43 / 33 / 82 / 82 / 25 classes);
- the same five at n = 11 (68 / 50 / 158 / 158 / 35 classes);
- lob1 at n = 10.

Each cell reports:
- P(C,C), π(all-D), and the support at π ≥ 10⁻³.
- The main cooperator: the self-cooperating monomorphic state with the largest π. For it, π, ρ(· | all-D), and
  exits split into four kinds:
  - **faker**: u(q,a) > u(a,a);
  - **strict**: neutral against the resident, favoured among its own kind;
  - **neutral**, of which **shadow** means the mutant cooperates with D;
  - **other**: deleterious.
- The mutual-cooperation graph over self-cooperating monomorphic states with π ≥ 10⁻⁵: its components, the largest
  component's share of cooperative mass, the π-weighted pairwise coverage, and whether cross-component pairs are
  mutual D or one-way C.
- Polymorphic π, terminal classes, cut flow and dropped flow, P(C,C) at tolerance 10⁻¹¹, and the expected number
  of mutation events from all-D until the chain first enters a conditional cooperator.
- For gfp, lob and lob1: P(C,C) with the faker edges out of the probe's world suppressed.
- For gfp: the π-weighted faker flux, split by resident (FairBot, or other) and by its loop-only part. Loop-only
  means lfp says the resident defects on the faker, weighted over canonical members by μ.

## Verdicts

**Tags.**

1. **Tags are efficient, through a single clique.** At every N, both n, and both tag variants:
   - P(C,C) ≥ 0.99;
   - `EQ(ME)` holds at least 0.99 of the cooperative mass;
   - `EQ(ME)` has no faker, strict or neutral exit, since it defects on ALLC and so has no shadow;
   - ρ(`EQ(ME)` | all-D) is FairBot's: 0.0421 / 0.0136 / 0.0044 / 0.0025, ±2%.

   *Falsifier:* P(C,C) < 0.99 in any cell, or a non-deleterious exit from all-`EQ(ME)`.
2. **Tags are parochial, with or without the equality axioms.**
   - `EQ(ME)` mutually cooperates with none of the language's other conditional cooperators: 0 of 7 under tag and 0
     of 4 under tageq at n = 10. Their μ-weighted coverage is 0.
   - Under tag that includes `and(EQ(ME),not(EQ(^D)))`, the same commitment in other words. tageq merges those two,
     yet still has 4 mutually defecting components.
   - Every cross-component pair in the π-support is mutual D or one-way C, never mutual C.
   - The parochialism is latent in π: the length prior gives the shortest clique about 10⁴ times its rivals' mass.

   *Falsifier:* `EQ(ME)` mutually cooperates with another conditional cooperator under either equivalence.
3. **Hitting time.** The expected number of mutation events from all-D until the chain first enters a conditional
   cooperator is within ±30% of 1/(Σ μρ): 2.9·10³ / 9.0·10³ / 2.8·10⁴ / 4.9·10⁴ at n = 10. The effective
   inter-clique split puts at least 0.99 on `EQ(ME)`, and P(C,C) at tolerance 10⁻¹¹ is within 10⁻³ of the
   10⁻¹³ value.

**lfp.**

4. **lfp behaves like W0: a peak, then a fall.**
   - P(C,C) within ±30% of 0.020 / 0.029 / 0.015 / 0.009, peaking at N = 10³.
   - The main cooperator is the probe `IMP(THEM(^C))`.
   - Faker exits, led by `IMP(THEM(^D))`, are at least 0.9 of its exits at N ≥ 10⁴ (static 0.93 and 0.97).

   *Falsifier:* no peak, or P(C,C) above 0.05 at 3·10⁴.

**gfp.**

5. **gfp rises with no peak.**
   - P(C,C) within ±0.03 of the static values, 0.136 / 0.299 / 0.478 / 0.575, at n = 10.
   - n = 11 is within 0.02 of n = 10.
   - FairBot is the main cooperator, with zero faker and zero strict exits at every N.
   - Its exits are neutral, with the shadow taking at least 0.9 of them; their slope in N is −1.00 ± 0.05.
   - Its entry slope is −0.50 ± 0.05.

   *Falsifier:* a faker or strict exit from gfp FairBot, which given the mirror would mean an evaluator bug; or
   P(C,C) at 3·10⁴ below its value at 10⁴.
6. **gfp cooperation is broadly compatible** [after review: renamed from "universal", astra].
   - The cooperative π-support forms one mutual-cooperation component, holding at least 0.99 of cooperative mass.
   - The π-weighted pairwise coverage is at least 0.95.
   - Across the language, μ-weighted coverage among conditional cooperators is at least 0.99 (static 1.000).

   *Falsifier:* two or more mutually defecting components, each with at least 0.05 of cooperative mass.
7. **gfp falls behind Löb through the fakeable probe, and only through it.**
   - lob is within ±0.03 of 0.138 / 0.319 / 0.584 / 0.706, and within 0.02 of M0's committed 0.70 at 3·10⁴.
   - gfp is at least 0.10 below lob at 3·10⁴ (static gap 0.13).
   - π(`IMP(THEM(THEM))`)/π(FairBot) at 3·10⁴ is 0.06–0.25 (static 0.13), against at least 0.8 in lob (static 0.97).
   - The cooperative-to-D ratio over [10³, 3·10⁴] has slope 0.28–0.42 for gfp (static 0.34) and 0.45–0.52 for lob
     (static 0.48).
   - [after review, fable] *Mechanism:* with the probe's faker edges suppressed, gfp is within 0.02 of lob at every
     N (static: equal to 0.002).
   - *Reader strength:* lob1 is within 0.01 of lob at every N (static: equal).

   So the gap is truth versus provability, not the strength of the logic. *Falsifier:* ablated gfp differs from lob
   by more than 0.02, or lob1 differs from lob by more than 0.02.
8. **The C-seeded rule adds no exploitation of FairBot** [after review: restricted, astra and fable].
   - The π-weighted faker flux out of all-FairBot is 0 at every N, which is the mirror theorem.
   - For other residents, loop-only faker flux exists. An example is `not(IMP(THEM(^IMP(THEM(ME)))))` against
     `IMP(THEM(THEM))`: it cooperates with itself only because FairBot's self-loop is C-seeded. This flux is at
     most 5% of their total faker flux (static bound about 3%).

   *Falsifier:* any faker flux out of FairBot, or a loop-only share above 10%.
9. **Comparison with the free modal arm.** At N = 3·10⁴ the free modal arm reaches 0.73. Here:
   - gfp is 0.54–0.61, below it;
   - lob, at this grammar, is 0.68–0.73;
   - tags are at least 0.99, above it;
   - lfp is below 0.02.

**What each outcome would mean.**
- *If 1–9 hold,* certificates alone do not settle the question. At an identical grammar and prior, the semantic
  regime settles it:
  - *D-seeded (lfp).* This is what a conservative checker without Löb's rule gives. It has no working
    self-reference, its only cooperators are fakeable third-party probes, and it reproduces the weak arm's faker
    limit.
  - *C-seeded (gfp).* This gives a FairBot that is a mirror: unfakeable and neutral at entry. So it meets both
    conditions of THEORY §9.2, and cooperation rises in lim_N. The cost is a stated selection rule.
  - *Löb.* It gets the same FairBot without choosing a fixed point.
  - *The gfp-to-Löb gap* is entirely the probe faker. It reflects truth against provability: a reader that sees a
    true negative fact can be faked through its probe, and no consistent prover can be.
  - *Tags.* They are efficient only by being parochial. They are the clique arm again, with honest certificates
    ruling out label fakers by definition.
- *If 5 fails with a faker exit,* the mirror argument or the evaluator is wrong. Stop before reading anything else.
- *If the ablation in 7 leaves a gap,* something besides the probe channel separates C-seeded truth from
  provability. Candidates are class aggregation, routing, or the negation fallback (astra).
- *If 2 fails under tageq,* parochialism was an artefact of the weak equivalence.

**Not tested here.**
- *Label tags.* In this design the tag is a free label, separate from the rule. Holding K then does not imply
  behaving as K, and a label-holder that defects strictly invades at μ-weight. That is the weak arm's faker law by
  construction.
- *Tags checked by behavioural equivalence.* That is "behavioural `eq`", which REJECTED.md rules out.
- *Finite εN.*
- *Pricing.* Fable's suggestion of lazy pricing on the gfp arm is left for later.
