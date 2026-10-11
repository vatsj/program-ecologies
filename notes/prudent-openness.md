# Prudent openness against identity: the CBP tilts, the identity abundance threshold (notes, 2026-10-11)

Spec `specs/2026-10-11-prudent-openness.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-11-prudent-openness-gpt-6.1-sol.md`;
the [after review] text is the resolution). Base: the identity-and-tags run (`notes/identity-tags.md` §1, `runs/identity-tags.md`,
`src/identity_tags*.py`), whose grammar, production, checker, catalogue, identity-aware classes (3,974), lottery kernel,
holder-based endpoint and L prior are reused unchanged; the cached class table (`runs/identity_tags/static_n7.npz`,
`lists_n7.pkl`) is reused and not recomputed. §1 is written before any project code of this experiment and before any
counted cell. §1.14 (code validation) is appended after the code exists and before any counted cell; §2 (costs) after
that.

*Disclosure.* The spec's hand reading of CBP against CB had to be checked before anything could be designed (whether CBP's
family is prudent decides what the tilts measure). Before writing this section I therefore queried the cached class table
and the ideal checker from a scratch script: CBP's class and its row against the named classes, the maximal cliques
containing CBP, the families' overlaps and compatibility paths, 15 named check values, 7 whole plays, and the class
masses and seed payoffs under the tilt laws below. No lottery or chain cell was run. The hand derivations below were done
first; every number quoted as "table" comes from those queries and is re-derived by the project code in §1.14.

## 1. Design

### 1.0 Scope

The identity run found that the scramble rewards prudence: identity cliques and the exclusive club XC win islands by
defecting on the seed's unconditional cooperators (0.35 of L) while cooperating with their own kind, and the open carrier
CB, which cooperates with unconditional cooperators, converts seeded copies into islands about 3× worse. This experiment
asks (1) whether a *prudent open* carrier, one that refuses unconditional cooperators but cooperates with every certified
prudent reader, establishes like a clique and pools like a family; and (2) where the identity abundance threshold for
universality lies, as a curve in seeded clique copies. Every lottery number is ε = 0, finite-(N, I, horizon) evidence;
the chain is a diagnostic; the two are never pooled.

### 1.1 CBP and two meanings of "plain C"

**CBP** = `if(and(CHK(them,me,C), CHK(them,⌜C⌝,D)), C, D)`: 6 nodes (if, and, two atoms, two leaves). Its class (table)
has three spellings: the and-form (6 nodes), the nested form `if(CHK(them,me,C), if(CHK(them,⌜C⌝,D),C,D), D)` (7) and the
negation `if(not(and(…)), D, C)` (7); class mass 9.68·10⁻⁵ under L (half of CB's 1.94·10⁻⁴); S-guarded (every path to
C passes a true S = `CHK(them,me,C)`), so by Lemma G (milestone 2) no class strictly invades it. It is **not** milestone
4's probe also named CBP (`if(S, if(CHK(them,⌜D⌝,D),C,D), D)`, which reads defection against ⌜D⌝); here "CBP" is always
the spec's program and the probe is called CBP₄.

"Plain C" names two different objects, and the spec's hand reading conflates them:
- **Cc**, the catalogue program `C`: a carrier with the produced list [(C, ε)], i.e. it *certifies* that it cooperates
  with everyone (ε is opponent-generic). It is the seed's main unconditional cooperator (class mass 0.068; all
  unconditional cooperators together 0.352).
- **⌜C⌝ = `PROG_C`**, the constant quoted inside check atoms: the bare λλC term with **no certificate list**. Any check
  `CHK(⌜C⌝, X, a)` has nothing to verify and is F.

The atom `CHK(them,⌜C⌝,D)` asks about the opponent's play against the *certificate-less* ⌜C⌝, not against Cc.

### 1.2 Hand plays (K = 10⁶, V = K/4; scripts in milestone 4's notation)

CBP's list from the frozen tactic: the D script against ⌜D⌝ is δ = `EvR*; ChkR[RunNeg · EvR*; Ax]` (S's box is false
against ⌜D⌝); its C scripts against the probes are the two-check skeleton σ_P = `EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Run] ·
Hyp]` (S closed by Hyp^pair, the ⌜C⌝ check closed by Run). So CBP carries [(C, σ_P), (D, δ)], the same shape as XC.

- **Every S-guarded carrier defects against ⌜C⌝ and certifies it.** Against ⌜C⌝ the S check is F (⌜C⌝ carries nothing),
  so the run reaches D, and δ closes the S box by RunNeg. Hence chk_D(CB, ⌜C⌝) = chk_D(CBP, ⌜C⌝) = chk_D(XC, ⌜C⌝) = T.
- **Unconditional cooperators cooperate with ⌜C⌝**, so by soundness chk_D(Cc, ⌜C⌝) = F for every such program: CBP refuses
  them all. (One catalogue class is unconditional against the catalogue yet defects on ⌜C⌝, `if(CHK(me,them,C),
  if(CHK(me,⌜C⌝,C),C,C), D)`, mass 9.7·10⁻⁵; CBP cooperates with it. It is the only exception.)
- **CBP vs CB: mutual C.** CBP's second atom is T against CB (first bullet). Its S atom against CB and CB's S atom
  against CBP are one pair rule: CB's σCB closes ⊡(CBP, CB, C) by Hyp^pair, CBP's σ_P closes ⊡(CB, CBP, C) by Hyp^pair
  and ⊡(CB, ⌜C⌝, D) by Run; partner validation succeeds both ways. **So CBP and CB are compatible, and the spec's reading
  ("CB lacks the certified defection against C") fails: CB lacks a certified defection against Cc, which CBP never asks
  for.**
- **CBP vs Cc:** CBP plays D (second atom F); Cc plays C. CBP exploits Cc exactly as EQ and XC do.
- **CBP vs D:** D/D (S is F). **CBP vs EQ:** D/D (EQ defects on every other source; S is F both ways). **Self:** C
  (Hyp^self on S, Run on the ⌜C⌝ box, true by δ).
- **CBP vs XC:** XC cooperates with CBP iff chk_C(CBP, XC) and chk_D(CBP, ⌜CB⌝). CBP cooperates with CB, so no sound D
  script against ⌜CB⌝ exists: chk_D(CBP, ⌜CB⌝) = F and XC defects on CBP. CBP cooperates with XC iff chk_C(XC, CBP)
  (its second atom is T against XC): F by soundness, since XC defects on CBP. **Mutual D.**

Hand table (row's action against column):

| row \ col | Cc | D | CB | EQ | XC | CBP |
|---|---|---|---|---|---|---|
| Cc | C | C | C | C | C | C |
| D | D | D | D | D | D | D |
| CB | C | D | C | D | D | C |
| EQ | D | D | D | C | D | D |
| XC | D | D | D | D | C | D |
| CBP | D | D | C | D | D | C |

Table check (scratch, disclosed): the class table gives exactly these 36 cells; the ideal checker gives chk_D(CB, ⌜C⌝) =
T, chk_D(CBP, ⌜CB⌝) = F, chk_C(XC, CBP) = F, chk_C(CBP, CB) = chk_C(CB, CBP) = T, chk_D(Cc, ⌜C⌝) = F; whole plays agree.
The tests play this table by whole runs (`lt_code.play`).

### 1.3 Consequence for the design

CBP is prudent (it refuses every unconditional cooperator: CB cooperates with 0.316 of the 0.352 unconditional mass
under L, CBP with 9.7·10⁻⁵) **and open to CB**: it cooperates with every S-guarded carrier that refuses certificate-less
cooperators, which is every S-guarded carrier. So "universal among verifiers" includes the nice carriers, and the
question (1) of the spec has a cleaner form than the spec expected: **within one compatible family, do the prudent
members establish better than the nice ones?** The frozen family (§1.4) is mostly nice, so the spec's P1 measures a
family tilt, not prudence; the matched pair P1p/P2n (§1.6) is added to answer (1) as intended. RE prediction 4's
clause (i) is falsified statically (§1.5), before any cell.

### 1.4 CBP's family by the frozen rule

**Rule (frozen before any cell):** F_P := the maximal clique of the establisher compatibility graph (identity run §1.7:
vertices = establishers, edge = mutual cooperation) that contains CBP and has the largest pooled L mass; ties broken by
enumeration order. The bridge-connected component containing CBP is reported separately.

**Table values:** 106 maximal cliques contain CBP. F_P has **147 classes, 537 spellings, L mass 0.01551** (runner-up
0.01549, 146 classes; the top eight differ in a handful of members). Every member is labelled *open* (mutual C with CB),
and **CB ∈ F_P**. Composition:
- **prudent core** F_P^pr (members that refuse Cc): **38 classes, mass 0.00218** (14% of F_P): CBP, its order twin and
  marked versions, the ⌜D⌝-reading variants, and the probe-readers `if(and(CHK(them,⌜CB⌝,C), CHK(them,⌜C⌝,D)),C,D)` etc.;
  16 S-guarded, 22 exploitable;
- **nice part** F_P^n = F_P \ F_P^pr: **109 classes, mass 0.01333**, heaviest `if(CHK(them,⌜CB⌝,C),C,D)` 0.0030,
  `if(not(CHK(them,me,C)),D,C)` 0.0027, MC¹, MC², CB itself.
- 39 members S-guarded (mass 0.0057); 108 have a strict invader (mass 0.0098); the main invaders are named-quote
  self-readers such as `if(and(CHK(me,them,C),CHK(me,⌜CB⌝,C)),C,D)` (they cooperate with ⌜CB⌝-readers by the R-box
  coincidence while defecting on others).

**Overlaps:** with F_CB (the identity run's open family, 216 classes, M = 0.03144): 105 classes, 0.01324; with N(CB) ∪
{CB} (329): all 147 (F_P ⊂ the open neighbourhood); with P_open read as "open and refuses Cc" (the identity run's 39
classes, 0.00225): 38; with P_open read as the spec words it, "S-guarded establishers that defect on Cc" (28 classes,
0.0014; labels open 16, exclusive 7, tag 4, other 1): 16; with XC's family F_X: 0. The bridge-connected component of
CBP: 568 classes, mass 0.066, **containing XC** (through XB, §1.5) and not EQ.

**XC's family** F_X (same rule): 9 classes, mass 5.81·10⁻⁴ = exactly the *exclusive* label.

### 1.5 CBP against XC

(i) *Executable actions:* CBP plays C against CB (not D, as the spec assumed); CBP and XC mutually defect.
(ii) *Certificate availability under the frozen tactic:* CBP's list is [(C, σ_P), (D, δ)]. A D script against ⌜CB⌝
would have to certify that CBP defects against CB, which it does not; by soundness no script can, so chk_D(CBP, ⌜CB⌝) = F
and XC's check refuses CBP. The RE's bet in prediction 4 (ii) ("the tactic produces CBP's D script against ⌜CB⌝ and XC
accepts it") fails because its premise (CBP defects against CB) fails.
(iii) *Compatibility paths of length ≤ 3 between F_P and F_X* (establisher graph):
- **length 1: 72 edges, all through one member of F_X, XB = `if(CHK(me,⌜CB⌝,C), D, if(CHK(them,me,C), C, D))`** (mass
  1.45·10⁻⁴, no strict invader). XB is mutual with CBP, with 71 other F_P members (18 of the core), with XC, XC′, MC¹,
  OF¹ and Cc, but not with CB: it reads its own certified play against the named quote, which the R-box coincidence
  makes an identity test for CB. So CBP–XB–XC is a path of length 2, and **XB is the only pairwise bridge between CBP and
  XC** (mass 1.45·10⁻⁴). The identity run's "bridge-less by soundness" is a statement about CB and XC; it does not hold
  for F_P and F_X.
- length 2 through a class outside both families: 150 classes, mass 0.0144 (open-labelled detector-type classes, 104 of
  them reaching F_X only through XB);
- length 3: 37,000 (a, b) pairs.
These are reported with every XC result; whether XB is ever seeded on a separated pair is logged (bridge fate).

### 1.6 Seed payoffs and the tilt laws

**One fixed rule for every tilt:** a tilt is a list of blocks and a list of removed sets. Each block is a set of
spellings given a total mass, spread by the L prior's relative spelling weights (or, for the T1c/T1b-type blocks, equal
mass per listed spelling, as in the identity run); every spelling of a removed set outside the blocks is set to 0; all
other spellings are rescaled proportionally to 1 − (total block mass). Class masses are sums over spellings. M = 0.03144
(the identity run's F_CB mass, as the spec fixes). Seeds are paired: the same random stream per replicate across cells.

Removed sets: *identity* = the 322 identity-labelled classes (exact-identity cliques); *allc* = the 421 unconditional
cooperators (rows all C, mass 0.352); N(CB)+ = the open neighbourhood with CB (329 classes).

| cell | blocks | removed |
|---|---|---|
| L | – | – |
| **P1** | F_P at M | – |
| **P2** | ten heaviest CB-run-tree spellings at M/10 each (= the identity run's T1c) | N(CB)+ |
| **P3** | F_P at M | identity |
| **P4** | F_P at M | allc |
| **P4′** | as P2 | N(CB)+, allc |
| **P5** | F_P at M/2; T1b's ten EQ spellings at M/20 each | – |
| *P1p* (added) | F_P^pr at M | F_P^n |
| *P2n* (added) | F_P^n at M | F_P^pr |
| *P3p* (added) | F_P^pr at M | F_P^n, identity |
| *P4p* (added) | F_P^pr at M | F_P^n, allc |
| *P4n* (added) | F_P^n at M | F_P^pr, allc |
| *P5p* (added) | F_P^pr at M/2; ten EQ spellings at M/20 each | F_P^n |

*Why the added cells (design elaboration before any cell):* F_P is 86% nice by mass and contains CB, so P1 against P2
compares a mixed family with ten CB spellings, not prudence with niceness. P1p and P2n put M on the prudent and the nice
part of one frozen clique with an identical background (the whole of F_P otherwise removed), which is the matched
comparison the spec's question (1) and RE prediction 2 need; P4p/P4n repeat it without unconditional cooperators; P3p
and P5p are the prudent versions of P3 and P5. The spec's cells are run and scored exactly as written.

Block masses (table) and expected seeded copies per run at (N, I) = (100, 64) (6,400·mass):

| cell | F_P | core | nice | CB set | identity | ten EQ | allc | D |
|---|---|---|---|---|---|---|---|---|
| L | 0.0155 (99) | 0.0022 (14) | 0.0133 (85) | 0.0041 (26) | 0.0090 (57) | 7.3e-4 (4.6) | 0.352 | 0.062 |
| P1 | 0.0314 (201) | 0.0044 (28) | 0.0270 (173) | 0.0082 (53) | 0.0088 (57) | 7.1e-4 | 0.347 | 0.061 |
| P2 | 0.0314 (201, all CB set) | 0 | 0.0314 | 0.0314 (201) | 0.0090 (58) | 7.3e-4 | 0.355 | 0.062 |
| P3 | 0.0314 | 0.0044 | 0.0270 | 0.0082 | 0 | 0 | 0.350 | 0.061 |
| P4 | 0.0314 | 0.0044 | 0.0270 | 0.0082 | 0.0138 (88) | 0.0011 | 0 | 0.095 |
| P4′ | 0.0314 | 0 | 0.0314 | 0.0314 | 0.0143 (91) | 0.0012 | 0 | 0.098 |
| P5 | 0.0157 (101) | 0.0022 | 0.0135 | 0.0041 | 0.0238 (153) | 0.0157 (101) | 0.347 | 0.061 |
| P1p | 0.0314 (201, all core) | 0.0314 | 0 | 0 | 0.0088 (57) | 7.1e-4 | 0.347 | 0.061 |
| P2n | 0.0314 (201, all nice) | 0 | 0.0314 | 0.0096 (61) | 0.0088 (57) | 7.1e-4 | 0.347 | 0.061 |
| P3p | 0.0314 (core) | 0.0314 | 0 | 0 | 0 | 0 | 0.350 | 0.061 |
| P4p | 0.0314 (core) | 0.0314 | 0 | 0 | 0.0138 (88) | 0.0011 | 0 | 0.095 |
| P4n | 0.0314 (nice) | 0 | 0.0314 | 0.0096 | 0.0138 (88) | 0.0011 | 0 | 0.095 |
| P5p | 0.0157 (core) | 0.0157 (101) | 0 | 0 | 0.0238 (153) | 0.0157 (101) | 0.347 | 0.061 |

("CB set" = the five classes of CB's run tree, 12 spellings; "ten EQ" = T1b's ten spellings, ten classes.)

**Seed payoff** f = U·μ (expected PD payoff against the iid seed; PD: C/C 0, D/C 1, C/D −2, D/D −1), table:

| cell | CBP | CB | EQ | XC | D | F_P (mass-weighted) | core | nice |
|---|---|---|---|---|---|---|---|---|
| L | −0.043 | −0.441 | +0.001 | −0.025 | +0.001 | −0.393 | −0.089 | −0.442 |
| P1 | −0.042 | −0.434 | −0.015 | −0.040 | −0.015 | −0.386 | −0.088 | −0.435 |
| P2 | −0.061 | −0.444 | −0.009 | −0.038 | +0.008 | −0.429 | – | −0.429 |
| P3 | −0.033 | −0.429 | −0.006 | −0.031 | −0.006 | −0.381 | −0.079 | −0.430 |
| P4 | −0.605 | −0.730 | −0.545 | −0.585 | −0.546 | −0.727 | −0.636 | −0.742 |
| P4′ | −0.656 | −0.758 | −0.556 | −0.602 | −0.529 | −0.758 | – | −0.758 |
| P5 | −0.057 | −0.449 | −0.013 | −0.040 | −0.015 | −0.402 | −0.104 | −0.451 |
| P1p | −0.042 | −0.434 | −0.011 | −0.038 | −0.015 | −0.088 | −0.088 | – |
| P2n | −0.042 | −0.434 | −0.015 | −0.040 | −0.015 | −0.435 | – | −0.435 |
| P4p | −0.605 | −0.730 | −0.542 | −0.583 | −0.546 | −0.636 | −0.636 | – |
| P4n | −0.605 | −0.730 | −0.546 | −0.585 | −0.546 | −0.742 | – | −0.742 |

Hand reading: CBP earns what EQ earns against the unconditional cooperators (+0.352 under L) and loses 0.044 more
than EQ against the rest of the seed (table: −0.395 against −0.351); CB earns only +0.036 from the cooperators because it cooperates back. **The
prudent core's seed advantage over the nice part is 0.35 with cooperators and 0.11 without** (P4p/P4n): removing the
cooperators removes about 70% of it, the rest being the core's lower exposure to exploiters.

### 1.7 The identity abundance scan (Part 2)

Groups (disjoint by construction, checked by code): **I** = the 322 identity-labelled classes (an identity class has no
mutual cooperator among establishers, while every F_P member cooperates mutually with CBP, so I ∩ F_P = ∅); **F** = F_P
(second curve only); **R** = the rest. Rule: I's spellings are rescaled together to total mass m (relative L weights
kept); in the second curve F's spellings are rescaled to total M; R's spellings are rescaled proportionally to
1 − m (first curve) or 1 − m − M (second). Scan points m ∈ {0, 2·10⁻⁴, 5·10⁻⁴, 10⁻³, 2·10⁻³, 5·10⁻³, m_L, 2·10⁻²},
where **m_L = 0.008979 is L's own identity mass** (the spec's "9·10⁻³ (= L)"), so the first curve's m_L point *is* the
L cell and the second curve's m_L point *is* P1 (same priors, same seeds: they are run once and shared, stated). The m = 0
point of the first curve is exactly the identity run's "identity cliques removed" prior.

Expected seeded clique copies per run (N·I·m at (100, 64)) and the chance that a run has none (e^{−6,400 m}):

| m | 0 | 2·10⁻⁴ | 5·10⁻⁴ | 10⁻³ | 2·10⁻³ | 5·10⁻³ | 8.98·10⁻³ | 2·10⁻² |
|---|---|---|---|---|---|---|---|---|
| copies per run | 0 | 1.28 | 3.2 | 6.4 | 12.8 | 32 | 57.5 | 128 |
| copies per island | 0 | 0.02 | 0.05 | 0.1 | 0.2 | 0.5 | 0.9 | 2 |
| P(no clique seeded) | 1 | 0.28 | 0.041 | 0.0017 | 3·10⁻⁶ | ≈ 0 | ≈ 0 | ≈ 0 |

*A rough calibration from the identity run (hand, guessed):* universal-open at 10,000 was 30/40 with no cliques and 3/40
under L. If each seeded clique copy independently leaves a persistent clique island with probability q and the clique-free
runs are universal with probability f₀, then f(m) ≈ f₀·e^{−6,400 m q}; f₀ = 0.75, f(m_L) = 0.075 give q ≈ 0.040, and the
50% crossing at m ≈ ln(1.5)/(6,400·0.040) ≈ 1.6·10⁻³.

### 1.8 Lottery law and kernel

The identity run's ε = 0 island process unchanged: complete island graph, I islands of N, Moran birth–death with parent
weight exp(w · mean payoff) on the source island, migrant parent from a uniformly chosen other island with probability
m = mN/N (mN = 1), uniform victim, w = 0.3, iid seeding per slot from the cell's class prior; one generation = I·N
births; checks every 10 generations. **Seeds:** the identity run's streams (`default_rng([N, I, rep, 20261010])` for the
seed, numba seed 7919·rep + 13N + I), so cells with the same prior reproduce the identity run's runs exactly (L, P2 = T1c,
scan m = 0 = "identity cliques removed"); this is a validation of the kernel (§1.13). **Horizon:** every run goes to
10,000 generations unless frozen (U constant on the global support: nothing can change any realized play; the frozen
state is carried to the remaining checkpoints). **Common checkpoints** 500, 1,000, 2,000, 5,000, 10,000 for every cell;
there is no outcome-conditioned extension.

### 1.9 Outcomes (holder-based, as in the identity run's endpoint revision)

An island is **held** by its majority class when that class self-cooperates and the island's P(C,C) ≥ 0.5. At each
checkpoint: *failed* (some island resolved non-cooperating, E3, or a held-majority class that does not self-cooperate
after E3 resolution); *universal-open* (every island held, every pair of holders mutually cooperating, every holder
mutually cooperating with CB); *universal-other* (the same with some holder not mutual with CB); *patchwork* (every
island held, some pair of holders mutually defecting); *unresolved* (otherwise). For a set S of classes:
**S-universal** = every island held by a member of S (for a clique S, holders then pairwise cooperate). Reported for
S = F_P (**universal-prudent** in the spec's words), F_P^pr (core-universal) and the CB set. **Identity islands** /
**XC islands** = fraction of islands held by identity-labelled / F_X classes.

**Cross-island P(C,C)** (role-free, mean over ordered island pairs i ≠ j of x_iᵀ PCC x_j): *overall*; *among readers*
(restricted to individuals of classes whose action row in the catalogue is not constant: 3,260 classes, L mass 0.30; the
714 constant-row classes are unconditional cooperators and defectors); *within the frozen family*: over pairs of islands
both held by F_P members, on their full compositions. (Restricted to pairs of F_P individuals it is 1 by construction,
since F_P is a clique; the island-pair version is the informative one.)

**Largest-established-set predictor** (the identity run's pooling check, unchanged): the maximal cliques among the run's
seeded establishers; the set with the largest established mass (individuals alive when every island is first held) and
the set with the largest seeded count; whether each won (universal with every holder in the set), at 2,000 and 10,000.

### 1.10 Stages (logged separately per labelled family and run)

Families logged: F_P, F_P^pr, F_P^n, the CB set, the open neighbourhood N(CB)+, the identity group (aggregated), T1b's
ten EQ spellings, F_X. A class may belong to several (bitmask). Per island i and family f the kernel keeps the family's
count c_{i,f} at every event and records:
- **initial copies** n₀ = Σ_i c_{i,f}(0); **seed islands occupied** O_f = #{i : c_{i,f}(0) > 0};
- **first zero** z_{i,f} = the first generation at which c_{i,f} hits 0 (event-resolved);
- **first hold** h_{i,f} = the first check (10-generation grid) at which f holds i (holder ∈ f);
- **seeded establishment** on an occupied seed island: h_{i,f} exists and z_{i,f} does not precede it (the family held
  the island before its seeded lineage ever vanished there); its **establishment time** is h_{i,f};
- **lineage extinction** on an occupied seed island: z_{i,f} < h_{i,f} (or no hold by 10,000);
  **extinction probability** = extinct / O_f; **established islands per occupied seed island** = seeded
  establishments / O_f (the founder-success estimator sol asks for);
- **persistence** at checkpoint T: seeded-established islands (h ≤ T) still held by f at T, over seeded-established
  islands by T;
- **spread** at T: islands held by f at T that are not seeded establishments of f (reached by migration or recolonized
  after a lineage vanished);
- **islands per seeded copy** at T (held islands / n₀, the identity run's statistic), reported beside these, not instead.

For the aggregated identity group, lineage continuity is per group (two different cliques on one island count as one
lineage); stated with its numbers.

### 1.11 The threshold statistic and the scaling panel

f(m) := the fraction of the 40 runs that are universal-open at **10,000** (primary; 2,000 reported too). **50% crossing**
m*: the first m at which f falls through 0.5, by linear interpolation in log m between adjacent points (linear in m on
[0, 2·10⁻⁴]); **95% interval** by a paired bootstrap over replicate indices (2,000 resamples of the 40 replicate indices,
the same resample at every scan point, since seeds are paired); a resample without a crossing is reported as "≥ 2·10⁻²"
or "< 2·10⁻⁴" and counted at the boundary. **Refinement:** only if m* falls between two scan points more than 2× apart,
two extra points at the geometric thirds of that interval. **Fits** (on the scan's f at 10,000): the RE's form
f = e^{−6,400 m q} (one parameter, least squares on m ≤ 10⁻³) with its residuals at every point; and f = f₀ e^{−6,400 m q}
(two parameters, same points). **Shift factor** = m* with F_P at M over m* without. **Scaling panel:** at the two scan
points bracketing m* on the first curve, (N, I) ∈ {(50, 64), (100, 32), (100, 128)}, 40 runs each; the crossing at each
(N, I) by interpolation between the two points (or a bound when f is on one side of 0.5 at both), reported in m and in
seeded copies per run N·I·m.

### 1.12 The chain (Part 3, diagnostic)

The identity run's reduced-support no-clique control with CBP's family added: support = the 1,500 heaviest classes under
L ∪ the 322 identity cliques ∪ F_P (56 of whose members are already among the 1,500; CBP ranks 959th), then closed leak
components removed iteratively (milestone 2); `FastChain` with twin drift, θ = 10⁻⁸, ≤ 4,000 states, N = 10³ and 10⁴
(the identity run's settings). Reported: P(C,C), π(all-D), π by label and by F_P^pr / F_P^n / F_X / XB, the top states
with their exits (transition structure: target, log₁₀ rate, mutants), the top cooperative state and whether it is
prudent-open (∈ F_P^pr), nice-open or XC, and the unexplored-flow fraction. **Closure check:** for each top state, the
classes outside the support that invade it neutrally or better (U(q, x) ≥ U(x, x)), with their L mass: the omitted exits
named as the caveat. **Twin-drift check:** the same cells with twin drift off.

### 1.13 Validation plan (before any counted cell)

1. The hand table of §1.2 by whole plays (tests) and against the class table.
2. F_P, F_P^pr, F_P^n, F_X, XB and the §1.4–1.5 counts reproduced by the module.
3. Every tilt and scan prior: block masses equal to the target to machine precision, removed sets at 0, the rest
   proportional to L; 2·10⁵ multinomial draws within sampling error; P2 equals the identity run's T1c prior exactly,
   the scan's m_L point equals L, m = 0 equals the identity run's no-clique prior.
4. The stage logger on a constructed run (two islands, known events) and on a real run against a direct recount from
   the kernel's snapshots.
5. The kernel reproduces the identity run's L and T1c runs at 2,000 (outcome and cross P(C,C) per replicate, from
   `runs/identity_tags/lottery_main.json`) before any counted cell.
6. The 50% crossing and its bootstrap on constructed curves with a known crossing.
