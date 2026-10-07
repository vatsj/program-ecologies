# The guard margin as a heritable trait: runs, 2026-10-06

Spec `specs/2026-10-06-guard-trait.md` (reviewed by gpt-6.1-sol); predictions `predictions/2026-10-06-guard-trait.md`
(commit 6a1ca6b, before any chain; addendum fc6e670, after the catalogue and static screening, before any chain);
code `src/guard_trait.py` (one bug fix in `src/k_cut.py`, commit 35e3cf5); tests `tests/test_guard_trait.py` (3 pass);
machine-readable `runs/guard-trait.json`; per-block files in `runs/guard-trait/`. Designed by the RE, reviewed by
gpt-6.1-sol, run by an Opus subagent.

## 0. What ran, and what did not

Ran, in the spec's priority order: the (source, g) catalogue at n = 8, b = 16 under K_c4 with mixed-guard semantics
(all four blocks, from one semantics); soundness checks and the independent checker with Lemma C witness replay; the
static screening (twins, the action-change table, P\*-type sources, fakers, the four encounter payoffs and exact N·ρ,
establishers, incompatible pairs, rivals, bridges); the ε → 0 chain at N = 10³, 10⁴, 3·10⁴ under both kernels with the
uniform prior, at N = 10⁴ under the 0.9/0.1 prior, with the g = 0-only and g = L-only references; the sham bit under
both kernels and both priors; the three attribution cells; the lottery (3 cells × 20 paired seeds); the amortized
price sweep c ∈ {0, 0.01, 0.1, 1}.

Not run / changed:
(i) **The catalogue is targeted, with a stated residual.** A single mixed K closure at cap 2b + 8 thrashed at 32 GB and
was killed; the closure was split into the four blocks (00, LL, 0L, L0), each its own K closure at cap b (§1, Lemma
Cap). K_c4 was searched on every *relevant* uncertified content (one entering a pair whose play is undecided under
three-valued evaluation) whose undecided pairs include a source of μ ≥ 10⁻⁵: 8,858 contents. The other 37,944 relevant
contents enter only pairs of sources with μ < 7.6·10⁻⁶ (μ²-weight 2.4·10⁻⁷) and keep K's value. A third tier
(μ ≥ 10⁻⁶, 188 chunks) ran 3.5 hours on two workers and completed no chunk (the long, low-μ programs are the expensive
ones; the first two tiers took 6.7 CPU-hours); it was stopped and changes nothing used here.
(v) **Price c = 0.1 is lazy-solver only.** Its seeded log-domain solve was still expanding polymorphic states after 5
CPU-hours (π(poly) 0.05 in the lazy chain at N·w·δ = 1.2) and was abandoned at hand-back; the lazy linear-domain
number is reported, unaudited.
(ii) **Design choice 8 (attribution sets) was degenerate as written** and was replaced before any chain (predictions
addendum): the literal "newly enabled faker" set has 1,005 genotypes of μ 0.53 (C, D, FairBot, …).
(iii) **3-type deep states were not seeded** (2-type deep-state search on every catalogue: 0 found in every cell, as in
K-cut); the lazy linear-domain chain serves as the independent state discovery.
(iv) The JLöb sibling closure (§1) was added after two chunks flagged soundness inconsistencies; those chunks were
rerun with it; tier-1 chunks rerun with it changed no searched goal (0 gained, 0 lost of 3,080).

**Incident.** None. Other experiments' processes were left alone; every kill in this run was by pid.

## 1. Proved, and method facts

**Mixed-guard semantics.** Genotype (s, g), g ∈ {0, L}. A g = L reader's level-k atoms read ¬□_{2b+8}^k⊥, a g = 0
reader's ¬□_b^k⊥. A quoted argument ^A of x is A at x's budget and x's guard. P[y, x] unfolds to y's definition with
y's guard, so in a cross-guard block the opponent's guard is part of the proposition the reader proves. A source with
no level ≥ 1 atom anywhere (quotes included) has a definition that does not mention g: its two genotypes are the same
program. At n = 8, 154 of 610 sources are guard-free (FairBot, `BOX(THEM(THEM))`, C, D, the Gödel sentence
`not(BOX(THEM(ME)))`, `BOX(THEM(^C))`, …).

**Lemma H (high-budget certificate rule).** Let X = K_c4, E a set of budget-b contents, B_E its extension closure
(notes/k-cut.md §1.7), ⊡E = ∧_{Y∈E}(Y ∧ □Y). Every (Y, e) ∈ B_E satisfies GL+Def ⊢ erase(⊡E → Y), at every e.
*Proof.* Induction on the closure. Std: X ⊢ Y and every K_c4 sequent erases to a GL+Def-valid one (Dist⁺ erases to
the K4 rule, admissible in GL). E-leaves: trivial. BoxEq (i)–(iii): the output content is provably equivalent under
Def. Dist⁺: by induction ⊡E → A_i; GL ⊢ ⊡E → □⊡E (□(Y ∧ □Y) ≡ □Y ∧ □□Y and □Y → □□Y), so ⊡E → □A_i; the premise
Π ⊢ B (Π ⊆ {A_i, □A_i}) erases to a GL-valid sequent; so ⊡E → B. ∎ *Use:* a box query above b + 1 is false in I_E when
its content is Std-false and GL+Def ⊬ erase(⊡E → Y). Theorem E is unchanged, so the certificate now covers the long
guard. On P\*'s self-play at g = L (E = {P}) GL proves (P ∧ □P) → ⊥, so P\* is left uncertified (correct: Dist⁺ reaches
□_{2b+7}⊥); at g = 0 Lemma E1 certifies it (tests).

**Lemma Cap.** For every value ≤ b, the search at cap b equals the search at any larger cap, in K and in K_c4. Sizes
are additive and monotone (every sub-derivation, Nec premise, JLöb premise, Dist⁺ premise and lemma-cut leaf of a
size-≤ b derivation has size ≤ b) and the Dist⁺ side condition compares premise sizes with the right box's *budget*
(e.g. 2b + 8), not with the cap. (The K-cut long-guard sweep used cap 2b + 8; at n = 6 the cap-b targeted table equals
the cap-2b + 8 full closure.)

**Value-preserving accelerations of the Dist⁺ search** (subclass, no core edit): a per-phase cache of Dist instances
(within one phase memo the T/J/M values are fixed, and premise registration is idempotent) and GL pruning by weakening
(if erase(Π_max ⊢ B) is not GL-valid for the union of every content and box an instance could use, no subset is). Both
leave every value unchanged (n = 6: identical T values on all 168 derived goals).

**JLöb sibling closure.** A JLöb instance (S, b) of size v concludes every member of S, but K's candidate rule
searches S from one member only. At n = 8 this left two chunks inconsistent: P[x, y] derived (x =
`and(BOXD(THEM(THEM)),BOX1(THEM(ME)))`/L, y = `not(BOXD(THEM(ME)))`) by an instance containing the content of x's own
level-1 atom, whose search alone failed, so the computed model made x defect while the calculus proved it cooperates
(flagged by the soundness check, 3 + 3 formulas). After every fixpoint each member of a recorded instance now gets
J ≤ v and the fixpoint resumes; values only decrease and each is witnessed. Both chunks rerun: 0 violations.

**Validation.** At n = 6, b = 16 the targeted mixed table (blocks, Lemma H, relevance filter, accelerations, sibling
closure) equals the full K_c4 closure over the mixed catalogue at cap 2b + 8: 0 of 17,424 plays differ.

**Lumping.** Joint kernel: resident-independent, so every partition is kernel-lumpable; lumping by identical payoff
rows and columns of the full 1,220-genotype table is exact, and within a lump π splits ∝ μ. **Hence under the joint
kernel the neutral twin allocation equals the prior share exactly, for the guard and the sham alike: a theorem, not a
measurement** (observed: 0.5000 and 0.1000 in every joint cell). Separate kernel: resident-dependent, so the chain runs
on label-pure behavioural classes refined until every member of a block has the same kernel row over blocks (strong
lumpability; 1,158 blocks, sham 958).

## 2. The catalogue (n = 8, b = 16, K_c4, 1,220 genotypes, 1,066 programs)

| block | contents | GL-true | K-derived | K misses | certified (E1 / Lemma H) | uncertified | relevant | searched | newly derived (≤ b) | plays ≠ K | soundness (K / K_c4) | checker: goals, Dist nodes, witnesses replayed, failures |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 00 | 260,656 | 59,982 | 24,469 | 35,513 | 31,491 | 4,022 | 3,333 | 271 | 43 | 52 | 0/78,340 · 0/2,404 | 55, 131, 63, 0 |
| LL | 260,656 | 59,982 | 24,469 | 35,513 | 7,389 | 28,124 | 19,615 | 4,080 | 1,761 | 5,887 | 0/78,340 · 0/19,985 | 2,617, 3,087, 235, 0 |
| 0L | 260,944 | 60,084 | 23,875 | 36,209 | 25,112 | 11,097 | 7,758 | 1,264 | 588 | 1,312 | 0/115,411 · 0/8,950 | 779, 974, 155, 0 |
| L0 | 260,944 | 60,084 | 23,875 | 36,209 | 13,972 | 22,237 | 16,096 | 3,243 | 1,266 | 4,449 | 0/115,409 · 0/16,968 | 1,877, 2,410, 295, 0 |

(Rows: reader block, opponent block. K closures 4.5–15 min each at cap b; K_c4 search 6.7 CPU-hours. 0 size mismatches
between the search and the independent checker.) The g = 0 block equals the published K table except 52 plays
(K_c4 acceleration); against K_c's published b = 16 table it differs in 147 plays of μ² 1.2·10⁻⁹ (K_c's own changes
in low-μ pairs that this run left unsearched). The L–L block differs from g = 0 in 5,835 plays (μ² 2.1·10⁻⁴); the cross
blocks in 1,803 (g = 0 reader vs g = L opponent) and 4,940 (g = L reader vs g = 0 opponent). **11,700 plays of the
mixed table differ from K's mixed table.**

## 3. Static screening (uniform prior)

**Twins.** Of 610 g = L genotypes, 257 are exact twins of their g = 0 partner (154 guard-free by construction, 103
guarded sources the long guard does not change) and carry 0.970 of the prior mass; 353 are active (μ 0.030).

**Guard-induced action changes** (every ordered pair with a g = L member whose play differs from the guard-erased pair;
weight μ(x)μ(y)):

| new outcome of the pair | cells | weight | share |
|---|---|---|---|
| x newly suckered (enabled exploitation by y) | 4,879 | 7.07·10⁻⁵ | 0.67 |
| x newly exploits y (enabled exploitation by x) | 2,081 | 1.49·10⁻⁵ | 0.14 |
| new mutual C (enabled cooperation) | 3,014 | 1.04·10⁻⁵ | 0.10 |
| new mutual D (protection) | 2,604 | 0.91·10⁻⁵ | 0.09 |

Enabled exploitation 8.6·10⁻⁵ against enabled cooperation 1.0·10⁻⁵: **ratio 0.12**. By direction: L reader vs L
opponent 5.3·10⁻⁵, L reader vs g = 0 opponent 4.8·10⁻⁵, g = 0 reader vs L opponent 0.4·10⁻⁵ (the long guard acts
mostly on its own carrier).

**What the margin buys and who exploits it.** Newly self-cooperating at g = L (P\*-type, the partners): 7 sources, μ
1.4·10⁻⁵ — P\*, its three THEM-variants and three `BOX1(THEM(^not(…)))` readers (exactly the K-cut long-guard R_coop).
Fakers (non-establishers newly strictly invading an establisher): 118 genotypes, μ 0.0031, headed by
`not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))`, `not(BOX(THEM(^C)))` at both labels; 25 of the 37 Gödel/Con-set classes
of K at n = 8 are among them; 77 of the fakers' victim lists contain only g = L readers. Victims: `BOX1(THEM(THEM))`/L
(the core reader whose g = L version is fakeable), `or(…BOX1…)` readers, probe readers.

**Four encounter payoffs of a g = L mutant in a g = 0 resident of the same source** (PD, w = 0.3; N·ρ exact):

| source | guard-free | twin | rr, rm, mr, mm | N·ρ (N = 10³ / 10⁴) |
|---|---|---|---|---|
| FairBot `BOX(THEM(ME))` | yes | yes | 0, 0, 0, 0 | 1.000 / 1.000 |
| `BOX(THEM(THEM))` | yes | yes | 0, 0, 0, 0 | 1.000 / 1.000 |
| `BOX1(THEM(ME))` | no | no (differs vs third parties) | 0, 0, 0, 0 | 1.000 / 1.000 |
| `BOX1(THEM(THEM))` | no | no | 0, 0, 0, 0 | 1.000 / 1.000 |
| PrudentBot `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` | no | no | **0, −1, −1, 0** | 2.8·10⁻³² / 0 |
| `and(BOX(THEM(ME)),BOX1(THEM(^C)))` | no | no | 0, −1, −1, 0 | 2.8·10⁻³² / 0 |
| P\* | no | no | −1, −1, −1, 0 | 13.6 / 43.5 |

**PrudentBot's guard variants form a soft clique.** PB_0 and PB_L mutually defect at b = 16: their mutual-cooperation
derivation has size 20 (same-guard: 11), so b = 16 sits below the cross-guard threshold; at b = 24, 32, 40 they
cooperate (checked). The trait creates a budget soft clique of the kind "Rivals under K" found for FairBot vs
`BOX1(THEM(ME))` at b = 4. P\*_L strictly invades no g = 0 core program (it mutually defects with all of them).

**Establishers, incompatible pairs, rivals, bridges** (cores = supported self-cooperators, π ≥ 10⁻³, of the g = 0-only
and g = L-only chains at N = 10⁴). Establishers: 230 genotypes (113 g = 0, 117 g = L of which 80 active), μ 0.024.
g = 0 core: FairBot, `BOX1(THEM(ME))`, `BOX(THEM(THEM))`, `BOX1(THEM(THEM))`, PrudentBot, `BOX(THEM(^C))`,
`BOX1(THEM(^C))`, `and(BOX(THEM(ME)),BOX1(THEM(^C)))`; g = L core: the guard-free core, `BOX1(THEM(ME))`/L,
`BOX1(THEM(THEM))`/L, PrudentBot/L, the P\* family /L, `BOX(THEM(^C))`/L, `BOX1(THEM(^C))`/L and two probe readers.
**36 incompatible pairs** between the cores: every g = 0 core program against the P\* family /L (mutual defection),
and PrudentBot (and `and(BOX(THEM(ME)),BOX1(THEM(^C)))`) against the g = L versions of `BOX1(THEM(ME))`,
`BOX1(THEM(THEM))`, PrudentBot and the probe readers. Rivals of the g = 0 core: 73 establishers (μ 0.0043; 37 active
g = L); **bridge-less: the P\* family /L and `not(BOXD1(THEM(^not(…))))`/L readers (μ 7.5·10⁻⁶)** — the bridge-less
P\*-type rival network that K removed at b ≥ 12 ("Rivals under K") returns with the long-guard trait. Strict invaders of
the g = 0 core: `or(BOXD…, BOX(THEM(^D)))`-type readers and two P\*-type partners against `BOX(THEM(THEM))`.

## 4. Chains (ε → 0, PD, w = 0.3; seeded log-domain GTH; uniform prior unless stated)

| cell | kernel | prior | N | P(C,C) | π(D) | π active L | of which core near-twins / P\*-type partners / fakers / other | π neutral L | twin allocation | coop π: g = 0 / L neutral / L active | blocks | states | residual | lazy P(C,C) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| mixed | joint | 91 | 10000 | 0.665545 | 0.3343 | 0.0265 | 0.0215 / 0.0040 / 0.0000 / 0.0010 | 0.0647 | 0.1000 | 0.608 / 0.031 / 0.026 | 903 | 1184 | 9e-15 | 0.665543 |
| mixed | joint | u | 1000 | 0.383551 | 0.6160 | 0.0880 | 0.0654 / 0.0153 / 0.0000 / 0.0073 | 0.4059 | 0.5000 | 0.197 / 0.097 / 0.088 | 903 | 1767 | 9e-15 | 0.383549 |
| mixed | joint | u | 10000 | 0.646739 | 0.3531 | 0.1404 | 0.1033 / 0.0323 / 0.0000 / 0.0048 | 0.3401 | 0.5000 | 0.343 / 0.163 / 0.140 | 903 | 1229 | 2e-14 | 0.646735 |
| mixed | joint | u | 30000 | 0.761093 | 0.2388 | 0.1838 | 0.1409 / 0.0383 / 0.0000 / 0.0047 | 0.2984 | 0.5000 | 0.398 / 0.179 / 0.184 | 903 | 1166 | 2e-14 | 0.761090 |
| mixed | separate | 91 | 10000 | 0.661803 | 0.3380 | 0.0396 | 0.0203 / 0.0183 / 0.0000 / 0.0010 | 0.0736 | 0.1125 | 0.589 / 0.033 / 0.040 | 1158 | 1369 | 1e-14 | 0.661919 |
| mixed | separate | u | 1000 | 0.384508 | 0.6150 | 0.1015 | 0.0699 / 0.0242 / 0.0000 / 0.0074 | 0.4104 | 0.5064 | 0.184 / 0.097 / 0.101 | 1158 | 1734 | 3e-14 | 0.384530 |
| mixed | separate | u | 10000 | 0.641341 | 0.3585 | 0.1657 | 0.0976 / 0.0632 / 0.0000 / 0.0049 | 0.3600 | 0.5218 | 0.307 / 0.169 / 0.166 | 1158 | 1449 | 2e-14 | 0.641376 |
| mixed | separate | u | 30000 | 0.752964 | 0.2469 | 0.1943 | 0.1118 / 0.0781 / 0.0000 / 0.0044 | 0.3243 | 0.5264 | 0.370 / 0.189 / 0.194 | 1158 | 1359 | 1e-14 | 0.752999 |
| L | joint | u | 1000 | 0.381343 | 0.6182 | 1.0000 | — | 0.0000 | — | 0.000 / 0.000 / 0.380 | 579 | 1178 | 1e-14 | 0.381341 |
| L | joint | u | 10000 | 0.631910 | 0.3679 | 1.0000 | — | 0.0000 | — | 0.000 / 0.000 / 0.632 | 579 | 857 | 8e-15 | 0.631905 |
| L | joint | u | 30000 | 0.737776 | 0.2621 | 1.0000 | — | 0.0000 | — | 0.000 / 0.000 / 0.738 | 579 | 777 | 2e-14 | 0.737772 |
| delF | joint | u | 10000 | 1.000000 | 0.0000 | 1.0000 | — | 0.0000 | 0.5000 | 0.000 / 0.000 / 1.000 | 782 | 782 | 0e+00 | 1.000000 |
| delFP | joint | u | 10000 | 0.671072 | 0.3287 | 0.1804 | — | 0.3194 | 0.5000 | 0.336 / 0.155 / 0.180 | 768 | 1065 | 3e-14 | 0.671069 |
| delP | joint | u | 10000 | 0.636993 | 0.3628 | 0.1114 | — | 0.3512 | 0.5000 | 0.356 / 0.170 / 0.111 | 896 | 1222 | 3e-14 | 0.636989 |
| g0 | joint | u | 1000 | 0.392046 | 0.6075 | 0.0000 | — | 0.0000 | — | 0.390 / 0.000 / 0.000 | 479 | 923 | 1e-14 | 0.392045 |
| g0 | joint | u | 10000 | 0.670962 | 0.3289 | 0.0000 | — | 0.0000 | — | 0.671 / 0.000 / 0.000 | 479 | 661 | 9e-15 | 0.670959 |
| g0 | joint | u | 30000 | 0.790923 | 0.2090 | 0.0000 | — | 0.0000 | — | 0.791 / 0.000 / 0.000 | 479 | 598 | 2e-14 | 0.790922 |
| sham | joint | 91 | 10000 | 0.670962 | 0.3289 | 0.0000 | — | 0.1000 | 0.1000 | 0.604 / 0.067 / 0.000 | 479 | 661 | 9e-15 | 0.670959 |
| sham | joint | u | 10000 | 0.670962 | 0.3289 | 0.0000 | — | 0.5000 | 0.5000 | 0.335 / 0.335 / 0.000 | 479 | 661 | 9e-15 | 0.670959 |
| sham | separate | 91 | 10000 | 0.670962 | 0.3289 | 0.0000 | — | 0.1000 | 0.1000 | 0.604 / 0.067 / 0.000 | 958 | 1120 | 2e-14 | 0.670959 |
| sham | separate | u | 10000 | 0.670962 | 0.3289 | 0.0000 | — | 0.5000 | 0.5000 | 0.335 / 0.335 / 0.000 | 958 | 1162 | 2e-14 | 0.670959 |

Audit, every cell: residual ‖πQ‖/‖π·out‖ ≤ 3·10⁻¹⁴; seeded and lazy chains agree to ≤ 4·10⁻⁵ in P(C,C) except the
separate kernel at 0.9/0.1 (1.2·10⁻⁴) and price c = 1 (1.0·10⁻⁴, where the seeded chain carries π 1.5·10⁻³ on
polymorphic states the lazy one never expands); elsewhere the seeded chain carries π ≤ 3·10⁻⁶ on states the lazy one
lacks, and the lazy chain finds no state the seeded one lacks; 0 two-type deep states in any catalogue; top-exit
fixation probabilities recomputed by an independent mpmath Moran sum agree to ≤ 2·10⁻¹⁶. π(poly) ≤ 3·10⁻⁶ except
price c = 1 (1.5·10⁻³). Table columns: "near-twins" = active g = L genotypes of g = 0 core sources (`BOX1(THEM(ME))`,
`BOX1(THEM(THEM))`, PrudentBot); delete-cells and the g = L-only cell use their own catalogues (breakdown —).

**Support and transitions (mixed, joint, N = 10⁴).** D 0.353 (D and D/L 0.177 each); FairBot 0.167 (twins
0.083 + 0.083); `BOX(THEM(THEM))` 0.155; `BOX1(THEM(ME))` 0.083 and `BOX1(THEM(ME))`/L 0.083 (near-twins: identical in
the four encounters, differing only against third parties); `BOX1(THEM(THEM))` 0.076, its g = L version 0.005;
PrudentBot 0.015 and PrudentBot/L 0.015 (no neutral path between them: the soft clique); P\*/L 0.015 and its
THEM-variant 0.015. Exits: the core's are neutral drift into ALLC, N·exit 0.485–0.54 at every N; PrudentBot's 0.010
(neutral into FairBot); **P\*_L's 0.002, neutral into the Gödel sentences** (its only doors); **`BOX1(THEM(THEM))`/L's
N·exit 1.2 / 7.9 / 22.7 at N = 10³ / 10⁴ / 3·10⁴, 94–98% strict, into `not(BOX(THEM(ME)))`, `not(BOX(THEM(THEM)))`,
`not(BOX(THEM(^C)))`**: an N-independent per-event faker exit (N·exit ∝ N^0.86), the K-at-n8 Gödel exit restored for
long-guard carriers only. Entry D → core: N·ρ 13.6 / 43.5 / 75.5 (∝ N^0.50) for every self-cooperator, both labels.

**N-scaling (mixed, joint).** P(C,C) deficit against the g = 0-only chain: −0.008 / −0.024 / −0.030 at N = 10³ / 10⁴ /
3·10⁴ (separate: −0.008 / −0.030 / −0.038). Active g = L mass 0.088 / 0.140 / 0.184 (π ∝ N^0.22, the core's own
slope); within it the P\*-type partners 0.015 / 0.032 / 0.038 (π slope 0.32) and `BOX1(THEM(THEM))`/L 0.018 / 0.005 /
0.002 (π slope −0.63). PrudentBot (both labels) 0.003 / 0.031 / 0.084 against 0.004 / 0.053 / 0.148 in the g = 0-only
chain: the soft clique halves each label's neutral recruitment from FairBot.

## 5. The sham bit

Sham allocation is exactly the prior share in every cell (0.5000 uniform, 0.1000 under 0.9/0.1, both kernels), and
the sham chains reproduce the g = 0-only P(C,C) to 10⁻⁹. Guard twins: 0.5000 / 0.1000 under the joint kernel (the
lumping theorem), **0.5218 (uniform) and 0.1125 (0.9/0.1) under the separate kernel**: gaps 0.022 and 0.013. Under the
separate kernel a guard flip carries the source's mutational neighbourhood with it (from FairBot/L, source mutations
land on g = L programs, among them the long-lived P\* family), so twin allocation tilts toward L by a few percent. The
neutral guard mass is neither a selection signal nor kernel-invariant, and its deviation from the sham is small.

## 6. Attribution (N = 10⁴, uniform, joint)

| cell | P(C,C) | π(D) | π active L | top state |
|---|---|---|---|---|
| mixed | 0.6467 | 0.353 | 0.140 | D 0.353 (FairBot 0.167) |
| delete fakers (118 genotypes, μ 0.0031) | **1.0000** | 0 | 1.000 | **P\*/L 0.500 + its THEM-variant 0.500, absorbing** |
| delete partners (7 genotypes, μ 6.9·10⁻⁶) | 0.6370 | 0.363 | 0.111 | D 0.363 |
| delete both | 0.6711 | 0.329 | 0.180 | D 0.329 |
| g = 0 only (K_c4; = K_c) | 0.6710 | 0.329 | — | D 0.329 |

The faker deletion is degenerate: P\*_L's only exits are neutral drift into the Gödel sentences; without them it has
no exit at all, the chain is reducible and π sits on the absorbing P\* pair. Read through the non-degenerate cells:
removing the partners costs 0.010; removing the fakers from the partner-free catalogue gains 0.034; removing both
returns K to 10⁻⁴ (+0.024 over mixed). **The guard trait's whole net effect is the fakers and the partners, and the
fakers dominate.**

## 7. Prior 0.9/0.1 (N = 10⁴)

Mixed, joint: P(C,C) 0.6655 (deficit −0.005), active L 0.027, allocation 0.1000; separate: 0.6618, active L 0.040,
allocation 0.1125. The deficit and the active mass scale roughly with the prior's L share.

## 8. Lottery (ε = 0, (N, I) = (100, 64), mN = 1, 20 paired seeds)

| cell | efficient | Wilson 95% | holders g = 0 / g = L active / g = L twin | mean freeze generation | strong-island losses |
|---|---|---|---|---|---|
| g = 0 only | 20/20 | [0.84, 1.00] | 1.00 / 0 / 0 | 243 | 0 |
| mixed, uniform | 20/20 | [0.84, 1.00] | 0.41 / 0.33 / 0.25 | 264 | 6 |
| mixed, 0.9/0.1 | 20/20 | [0.84, 1.00] | 0.90 / 0.06 / 0.04 | 259 | 5 |

Paired differences (mixed − g = 0, same founders' sources): 0 discordant seeds of 20 in both priors (efficient
indicator and efficient-island fraction both 0; the exact sign-test bound on the discordance probability is ≤ 0.17).
Holders are spread across twins and near-twins by founder drift (`BOX1(THEM(ME))`/L 219 islands, `BOX1(THEM(ME))` 166,
FairBot/L 138, `BOX(THEM(THEM))`/L 135, `BOX1(THEM(THEM))`/L 121 …); no P\*-type holder. Establishment (global
P(C,C) ≥ 0.9) at generation 170–181, ALLC extinction ≈ 50 in every cell.

## 9. Amortized price sweep (imposed; N = 10⁴, uniform, joint; c·(2b + 8)/N per match on guarded g = L genotypes)

| c | price per match on a guarded g = L reader | N·w·δ | P(C,C) | π(D) | π active L | π neutral L (guard-free twins) | solver |
|---|---|---|---|---|---|---|---|
| 0 | 0 | 0 | 0.6467 | 0.353 | 0.1404 | 0.340 | seeded log-domain (= mixed cell) |
| 0.01 | 4·10⁻⁵ | 0.12 | 0.6440 | 0.356 | 0.1334 | 0.343 | seeded log-domain |
| 0.1 | 4·10⁻⁴ | 1.2 | 0.6261 | 0.374 | 0.0857 | 0.361 | **lazy linear-domain only** (π(poly) 0.052; the seeded solve had not finished after 5 CPU-hours) |
| 1 | 4·10⁻³ | 12 | 0.5973 | 0.403 | 0.0140 | 0.390 | seeded log-domain (lazy: 0.5972) |

Reference: g = 0 only 0.6710.

The price works on the active mass and kills it at c = 1, but P(C,C) falls *below* the g = 0 reference (0.597 at
c = 1): a priced long-guard reader is strictly invaded by its unpriced twin-source and by ALLC (the price ladder of
"Priced arm"), so the guard bit becomes a costly label that feeds a ladder. N·w·δ = 0.3·c·40 = 12c, N-independent on
the amortized path. The price result is about the imposed schedule.

## 10. Verdicts

| prediction | statement (short) | measured | verdict |
|---|---|---|---|
| RE 1 | active g = L π ≤ 0.2 at N = 10⁴ (uniform, both kernels); sham allocation within 0.05 of the neutral twins' | active 0.140 (joint) / 0.166 (separate); allocation gap 0 (joint, by theorem) / 0.022 (separate) | **held** |
| RE 2 | P(C,C) within 0.03 of K; faker deletion's gain > partner deletion's loss | 0.6467 vs 0.6710 (−0.024; separate −0.030); faker effect +0.353 (degenerate: P\* absorbing) or +0.034 without partners, partner effect +0.010 | **held** (the fixed faker cell is degenerate; the non-degenerate reading agrees) |
| RE 3 | FairBot_L exactly neutral in FairBot_0; P\*_L strictly invades no g = 0 core program | four payoffs 0,0,0,0, N·ρ = 1.000 (FairBot is guard-free: true by construction); P\*_L invades none (mutual defection with all) | **held** (PrudentBot, a guarded core program, is not neutral: 0, −1, −1, 0) |
| RE 4 | lottery paired difference's interval includes 0 and g = 0 holders ≥ 0.5 | 0 discordant of 20 (both priors); g = 0 holders 0.41 of islands (0.55 of non-twin holders), g = L active 0.33 | **inconclusive** (first half holds, second fails, falsifier not met) |
| RE 5 | active L decreases monotonically in c and ≤ 0.05 at c = 0.1 | 0.140 / 0.133 / 0.086 (lazy solver) / 0.014: monotone; 0.086 at c = 0.1 | **inconclusive** (grey 0.05–0.2; the c = 0.1 cell is lazy-solver only) |
| S1 | P\* (and P2) self-cooperate at g = L; ≥ 10 Gödel/Con classes newly invade; g = 0 block within μ² 10⁻⁶ of K_c | P\* yes (P2 is not in L_8: untestable); 25 classes; 147 plays, μ² 1.2·10⁻⁹ | **held** (P2 part not testable) |
| S2 | enabled exploitation > enabled cooperation (μ-weighted) | 8.6·10⁻⁵ vs 1.0·10⁻⁵ | **held** |
| S3 | joint allocation = prior to 10⁻⁶; separate gap to sham ≤ 0.05 | exact; 0.022 / 0.013 | **held** |
| S4 | P\*-type at g = L ≤ 0.05; guard-free core ≥ 0.25 (N = 10⁴, joint) | 0.032; 0.322 | **held** |
| S5 | active L at c = 1 ≤ half its c = 0 value | 0.014 vs 0.140 | **held** |
| S6 | every lottery cell ≥ 0.85 efficient | 20/20, 20/20, 20/20 | **held** |
| S7 | active L changes < 3× between N = 10³ and 3·10⁴ | 0.088 → 0.184 (2.1×) | **held** |
