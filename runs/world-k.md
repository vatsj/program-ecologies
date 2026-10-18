# Run report: identity-dependent results under world K (2026-10-18)

Spec `specs/2026-10-18-world-k-reruns.md`; notes `notes/world-k.md` (§1 static analysis by hand, §2 code, validation,
mechanism checks, costs, addenda); predictions `predictions/2026-10-18-world-k-reruns.md` (committed before any cell).
Code `src/world_k{,_run,_report}.py`, tests `tests/test_world_k.py` (6, passing). Rows `runs/world_k/cells_{A,B,C,D,N}.json.gz`
(A's per-island change log slimmed to class changes plus each island's last record; the report is identical on the full
and slim files); summary `runs/world-k.json`; validation `runs/world-k-validate.json`; statics
`runs/world-k-static.json`. Every ε = 0 number is a lottery statistic at finite (N, I, horizon), never π; the rain cell
is a finite-ε diagnostic. "Universal-open" is the scaling classifier's; runs are the units; paired differences are
K − L on identical founders and kernel seeds with McNemar exact p and a conditional exact 95% interval.

## What K is here (notes §1.1)

Every hypothesis-closed D certificate is the D step's, produced against the literal ⌜D⌝, so in K it is keyed to ⌜D⌝,
which is no population member's bare source (a population DefectBot is a carrier of the grammar body). Self-certified
defection is therefore never live in play: own-D atoms are F against every population member (term-level tests). In
the tables: hypothesis-closed D certificates live against non-partners 0.278 (L) → 0 (K); no unit reachable under
S-nonself is an identity unit (8 in L); the minted C-identity class (10 run trees, μ 0.00195) survives under S-self;
μ_net = 0.0280 → 0.0277; the former TwinD family becomes certified CooperateBots inside PrudentBot's network (predator
mass 0.44, DefectBot itself the top predator); Dill → AP network moves 0.0126 of prior mass.

## Disclosures

- Cached tables cloned read-only from the detectors worktree. World L reproduces stored scaling (N = 200) and Pangaea
  rows draw for draw; world K reproduces the detectors run's K0 island cell (200, 64) draw for draw to 10,000; lineage
  tracking is inert; K tables equal the detectors run's (notes §2.1).
- In K the static set's `Q` is L's Q (the former TwinD family), used for tracking and for the proportional control's
  founder slots (identical in both worlds).
- **The rain cell was run twice.** The first batch stopped frozen runs before the schedule ended (9 of 40 runs); it was
  set aside unscored before any D number was tabulated and the cell rerun with the stop disabled under rain (notes §2.6).
- **One r = N/2 run capped:** K (6,400, 1) r = N/2 replicate 1 ran 3.7 h without finishing (all others ≤ 18 min); the
  cell is scored on 19 K runs. One unflushed row lost by the kill was rerun and reproduced exactly.
- Horizons: island cells 10,000 (scored at 2,000 and 10,000); Pangaea cells 2,000 extended to 10,000 unless frozen;
  r = N/2 cells 2,000. N = 100 cells ran at r = 100 (the stored ones at r = 50), so L numbers at N = 100 and 400 are
  this run's, not the stored ones.
- About 33 worker-hours on 3 workers (counted rows: A 13.6, B 1.2, C 4.0, C′ 7.3, D 0.7; the set-aside rain batch 0.7, the
  capped run 3.7, probes and validation ≈ 1); nothing dropped.

## A. The scaling path (universal-open runs at 2,000 / 10,000; S-nonself and the proportional control, both worlds)

| (N, I) | L S-nonself | K S-nonself | K − L at 10,000 [95%], p | L prop | K prop | K S-nonself − L prop | identity islands L (K) at 10,000 |
|---|---|---|---|---|---|---|---|
| (100, 64) | 25 / 29 of 40 | 34 / 37 of 40 | +0.20 [−0.01, 0.32], 0.057 | 20 / 20 | 19 / 20 | −0.10 [−0.10, 0.07] | 0.052 (0) |
| (200, 64) | 11 / 11 | 19 / 19 | +0.40 [0.06, 0.50], 0.022 | 16 / 16 | 18 / 18 | +0.15 [−0.11, 0.25] | 0.056 (0) |
| (400, 64) | 9 / 9 | 17 / 18 | +0.45 [0.15, 0.45], 0.004 | 19 / 19 | 18 / 18 | −0.05 [−0.05, 0.05] | 0.060 (0) |
| (100, 128) | 5 / 9 | 12 / 16 | +0.35 [−0.05, 0.59], 0.092 | 14 / 17 | 17 / 19 | −0.05 [−0.28, 0.22] | 0.083 (0) |
| (200, 128) | 4 / 4 | 19 / 19 | **+0.75 [0.42, 0.75], 10⁻⁴** | 15 / 16 | 15 / 16 | +0.15 [−0.11, 0.25] | 0.074 (0) |
| (100, 256) | 2 / 6 | 8 / 15 | +0.45 [0.10, 0.55], 0.012 | 9 / 14 | 10 / 16 | +0.05 [−0.29, 0.37] | 0.011 (0) |

(The K − L columns of the proportional control are within ±0.10 everywhere, p ≥ 0.5.)

- **K removes every identity island** of the S-nonself and proportional cells, at every checkpoint of every run (L:
  up to 97 identity islands in a run). The former TwinD lineages are extinct by generation 100 in every K run (their
  share is ≤ 0.0025 to generation 50; L: mean 0.05–0.13 of the population at 200, as clique holders).
- **K S-nonself sits at the level of L's proportional control** (0.75–0.95 at 10,000) and is flat along the size and
  diagonal paths: 19 / 18 / 19 at (200, 64) / (400, 64) / (200, 128), against L's 11 / 9 / 4.
- **No copy-count law remains in K.** Within the K S-nonself cells at N ≥ 200, universal-open does not fall with the
  former TwinD copies (logistic slope +0.12 per copy, p = 0.33, cell as stratum).
- **The residue is non-identity rivals, mostly the AP network.** K's failing runs (16 of 160 S-nonself runs at 10,000)
  end in rival islands, except one scramble failure at (100, 64) (as in L). Of K's 74 rival islands at the end, the
  heaviest holders are AP-network readers of the partner's or the literal ^D box: `if(CHK(them,me,D),D,if(CHK(them,me,C),C,D))`
  (13), `if(and(not(CHK(them,^D,C)),CHK(them,^D,D)),D,C)` (12), `if(and(CHK(them,^D,D),CHK(me,^C,C)),D,C)` (6); by unit
  class, AP network 13/18, 18/21, 12/12 and 12/12 of the rival islands at (100, 128), (100, 256), (200, 128) and
  (400, 64). L's residue includes the stored detector family (`if(or(CHK(them,them,D),CHK(me,them,D)),D,C)` and its
  relatives), near-cliques in L. Rival islands per run at N ≥ 200: K 0.55, L prop 0.65 (pooled).
- **Static labels at 10,000:** K S-nonself failures are absorbing at N ≥ 200 (1 / 2 / 1 runs) and coordination
  (unresolved) at N = 100 (2 / 4 / 5 runs at I = 64 / 128 / 256); at N = 100 universal-open still rises after 2,000
  (+3 / +4 / +7 runs), so those cells are censored at 10,000.
- **Island efficiency:** excluding scramble failures, mean island P(C,C) is 0.998–0.9999 in every K cell and
  0.990–0.998 in L S-nonself; the fraction of islands ≥ 0.95 is 0.993–0.999 (K) and 0.93–0.99 (L).
- **The K proportional control equals K S-nonself** to within 3 runs everywhere (+2, −1, 0, +3, −3, +1 by geometry):
  the former TwinD mass is suckers that die in the scramble, so redrawing it changes nothing.

**Removing-rivals classes** (held non-target islands at 10,000, summed over 20 runs; uot = universal on target):

| cell | identity | exploitable | closed-open | closed-nonopen | uot |
|---|---|---|---|---|---|
| (200, 64) L / K | 72 / 0 | 14 / 0 | 202 / 64 | 0 / 9 | 11 / 18 |
| (400, 64) L / K | 77 / 0 | 5 / 12 | 24 / 45 | 0 / 0 | 9 / 14 |
| (200, 128) L / K | 190 / 0 | 26 / 12 | 31 / 239 | 0 / 0 | 3 / 14 |
| (200, 64) L prop / K prop | 0 / 0 | 16 / 2 | 237 / 12 | 0 / 13 | 11 / 17 |

K turns identity islands into universal runs; part of the gain lands on closed-open holders (open, not certified by
PrudentBot), so uot (14–18) trails universal-open (18–19) at N ≥ 200.

**Paired island transitions** (L class → K class, o open, i identity, r rival, u unheld; all runs of the cell):
at (200, 64) the 72 L identity islands of generation 2,000 were open in K at 2,000 in 72/72 cases (L's 69 identity
islands at 200 were 60 open and 9 unheld in K at 200); at (400, 64) 74/77 open, 3 rival; at (200, 128) 188/191 open, 3
rival; at (100, 64), (100, 128), (100, 256) 174/175, 346/354, 263/268 open. **Lineages:** an island's holder at its first open record is descended from a founder of that island in only
5–13% of islands in either world (the network spreads by migration at the calibrated mN), and L's identity islands are
themselves local in only 5–21% of cases (cliques are exported by migration). The K counterparts of L's identity
islands are local at their first open record in 3–13%, the same as the baseline. So the lineage log does not single out
a conversion step: in K the clique founder never establishes (it is a sucker) and its export never happens; the island
is taken by the open network's migrants like every other island. W13's "local establishment" clause failed.

**Gentle readers.** Own-D reader individuals at 200 in K S-nonself cells: 0 exploited (mutual C 0.84–0.96, mutual D
otherwise, except (100, 64), where the 173 surviving readers' encounters were all mutual D) and none acting through a
matching keyed certificate (0 by construction); in L 0–0.005 exploited.
The exposed readers (the former TwinD family, certified CooperateBots) are dead before 200 in K.

## B. The provenance rule (S-self against S-nonself, paired on founders and seed)

| cell | L S-nonself | L S-self | L diff [95%], p | K S-nonself | K S-self | K diff [95%], p | K S-self identity islands (2,000) |
|---|---|---|---|---|---|---|---|
| (100, 64) at 2,000 | 25 | 14 | +0.275 [0.03, 0.44], 0.027 | 34 | 24 | +0.25 [0.02, 0.39], 0.031 | 0.090 (L 0.136) |
| (100, 64) at 10,000 | 29 | 19 | +0.25 [0.02, 0.39], 0.031 | 37 | 26 | +0.275 [0.07, 0.36], 0.007 | 0.076 (L 0.119) |
| (200, 64) at 10,000 | 11 | 5 | +0.30 [−0.09, 0.53], 0.15 | 19 | 9 | **+0.50 [0.19, 0.50], 0.002** | 0.032 (L 0.133) |

- **The provenance rule matters as much in K as in L, or more.** K S-self's identity islands are all held by the minted
  C-identity class (230/230 and 41/41 at 2,000), never by the former TwinD templates (extinct by 100). In L they were
  205 minted + 143 TwinD at (100, 64).
- **S-self also mints near-cliques the identity label does not count:** K S-self's rival islands at (100, 64) are
  mostly `if(and(CHK(them,me,C),CHK(me,me,C)),C,D)` (34 of 61) and `if(and(CHK(me,me,C),CHK(them,me,C)),C,D)` (19),
  FairBot with a self-play-only conjunct; rival islands per run 1.5 (K S-self) against 0.05 (K S-nonself).
- **A whole run can be taken:** in K S-self (100, 64) replicate 39 a minted clique held all 64 islands from generation
  340 to the end.
- **Production budget under S-self:** the expected self-root share of lacking S-self producers' C attempts is 0.0001 at
  the seed, 0.22 / 0.47 / 0.58 at generations 10 / 50 / 200 at (100, 64) (0.12 / 0.31 / 0.42 at (200, 64)): the
  producers still lacking are concentrated in certificate-less lineages that meet themselves. Identity entries per run
  (kernel counter): K S-self 4.3 and 5.5, L S-self 8.6 and 16.4, at (100, 64) and (200, 64).
- No former TwinD template reaches a self-defecting unit: the D step is partner-free under every rule (notes §1.6).

## C. The Pangaea continuum (N·I = 12,800 unless stated; universal-open at the end; all-defect runs; paired K − L)

| cell | L uo | K uo | K − L, p | L lost | K lost | target ≥ 0.9 L / K | max identity share L / K | max AP share L / K |
|---|---|---|---|---|---|---|---|---|
| (200, 64) | 8 | **20** | +0.60, 0.0005 | 0 | 0 | 9 / 20 | 0.62 / 0 | 0.13 / 0.10 |
| (800, 16) | 13 | **20** | +0.35, 0.016 | 0 | 0 | 14 / 15 | 0.82 / 0 | 0.06 / 0.06 |
| (3,200, 4) | 17 | 19 | +0.10, 0.63 | 1 | 1 | 13 / 17 | 1.00 / 0 | 0.06 / 0.06 |
| (12,800, 1) | 19 | 18 | −0.05, 1.0 | 1 | 2 | 16 / 16 | 0.026 / 0 | 0.23 / 0.08 |
| fission–fusion (100, 128) → 200 | 20 | 20 | 0 | 0 | 0 | 19 / 20 | 0.25 / 0 | 0.08 / 0.07 |
| Pangaea 6,400 | 15 | 12 | −0.15, 0.51 | **5** | **8** | 14 / 11 | 0.017 / 0 | 0.09 / 0.06 |
| Pangaea 3,200 | 10 | 10 | 0 | 9 (+1 clique-held) | 10 | 10 / 9 | 1.00 / 0 | 0.06 / 0.07 |

- **In K the continuum is flat and islands are at least as good as the Pangaea.** 20 / 20 / 19 / 18 along (200, 64) /
  (800, 16) / (3,200, 4) / (12,800, 1): the clique's cost along I is gone (L: 8 / 13 / 17 / 19), and the Pangaea is no
  longer the best geometry, because its one establishment ticket remains.
- **K does not change the Pangaea's establishment law.** Pooled over the three Pangaeas, K lost 20 of 60 and L 15
  (paired +0.08 [−0.07, 0.21], p = 0.36); establishment medians are unchanged (140 vs 150 generations at 12,800). L's
  one clique-held Pangaea at 3,200 is an all-defect run in K: without the clique the same race has no winner.
- The AP network never wins a Pangaea in either world and never exceeds 0.10 of a K Pangaea.

**C′. r = N/2 control** (overlap-free kernel, 2,000; universal-open / all-defect):

| cell | L r = 100 | L r = N/2 | K r = 100 | K r = N/2 |
|---|---|---|---|---|
| (800, 16) | 13 / 0 | 15 / 0 | 20 / 0 | 18 / 1 |
| (3,200, 4) | 17 / 1 | 17 / 0 | 19 / 1 | 17 / 2 |
| (6,400, 1) | 15 / 5 | 12 / 8 | 12 / 8 | 13 / 6 (of 19) |

Production rate moves no count by more than 3 runs in either world. K − L is positive at (800, 16) in both arms, 0 or
+2 at (3,200, 4), and changes sign at (6,400, 1) (−3 at r = 100, +1 of 19 at r = N/2), both not significant: K's keying
is not confounded with production at large N; the Pangaea differences are noise.

## D. Rain under K and L ((200, 64), the annealed schedule at K = 3 exposure from generation 200, 9,909 arrivals per run; paired with the ε = 0 cell)

| | L ε = 0 | L rain | K ε = 0 | K rain |
|---|---|---|---|---|
| universal-open at 10,000 | 11 | 11 | 19 | 18 |
| universal on target | 11 | 11 | 18 | 16 |
| identity islands per island | 0.056 | 0.074 (paired +0.018) | 0 | 0 |
| exploitable rival islands (summed) | 14 | 16 | 0 | 7 |
| closed-open islands (summed) | 202 | 102 | 64 | 106 |
| mean island P(C,C) | 0.992 | 0.991 | 0.999 | 0.999 |

- **In L rain feeds identity** (+0.018 identity islands per island, paired), as the removing-rivals run found.
- **In K rain feeds no clique sink** (0 identity islands), but it has nothing to cure: K's ε = 0 cell has no
  exploitable rival island, and rain *creates* 7; K rain's 11 rival islands are held by the anti-punisher
  `if(CHK(them,^D,D),D,C)` (7) and `if(CHK(them,me,D),D,if(CHK(them,me,C),C,D))` (4), AP-network arrivals; universal-open 19 → 18, uot 18 → 16 (paired,
  not significant). K rain is more universal than L rain (18 vs 11, +0.35, p = 0.065).

## Verdicts

| # | prediction | outcome |
|---|---|---|
| RE 1 | identity islands ≤ 0.005 in every K cell | **held in every S-nonself, proportional and rain cell** (exactly 0); **falsifier fired in the S-self cells** (0.090 at (100, 64), 0.032 at (200, 64): the minted C-identity class) |
| RE 2 | K S-nonself within 0.1 of L prop at (200, 64), (400, 64), (200, 128); falsifier ≤ 0.6 | level held (0.95 / 0.90 / 0.95; falsifier not fired); "within 0.1" **held at (400, 64)** (−0.05 [−0.05, 0.05]) and **failed by exceeding** at (200, 64) and (200, 128) (+0.15, n.s.); residue non-identity rivals, held |
| RE 3 | K − L gain larger at (200, 128) than at (200, 64) | **held** (+0.75 vs +0.40); falsifier not fired (K 19 → 19) |
| RE 4 | S-self and S-nonself within 0.1 under K | **falsifier fired** (+0.25 / +0.275 at (100, 64), +0.50 at (200, 64)) |
| RE 5 | Pangaea 6,400 all-defect ≤ 2 under K against 5 under L | **falsifier fired** (K 8, L 5; μ_net unchanged; pooled over Pangaeas +0.08, p = 0.36) |
| RE 6 | fission–fusion 20/20 in K | **held** |
| Sol 8 | copy-count dependence remains; Pangaea improvement smaller or undetectable; hidden S-self/S-nonself differences | copy count **failed** (slope +0.12, p = 0.33; K flat in N·I); Pangaea clause **held** (no improvement); hidden-differences clause untestable as worded (no K cell with both rules ≥ 0.85) |
| Gemini 7 | S-self turns TwinD templates into self-defectors; Pangaea all-defect within 1–2 runs at 6,400 and 12,800 | mechanism **failed** (impossible by construction; 6 of 10 templates become illegible suckers, all extinct by 100); S-self and S-nonself do differ in mechanism (minted C-identity); Pangaea clause held at 12,800 (2 vs 1), **failed narrowly at 6,400** (3 runs, n.s.) |
| W1 | 0 identity islands in K S-nonself, prop, rain at every checkpoint | **held** |
| W2 | K S-self identity ≥ 0.03 / ≥ 0.02, ≥ 0.9 minted | **held** (0.090 / 0.032; 100% minted) |
| W3 | K S-nonself bounds per cell | **held** in all six |
| W4 | |K − L prop| ≤ 0.15; RE 2 mostly inconclusive | held (max 0.15); the RE 2 clause partly (one held, two failed by exceeding, none inconclusive) |
| W5 | K prop − K S-nonself ≤ 2 runs | **failed at 2 cells** (+3 at (100, 128), −3 at (200, 128)); falsifier (≥ 4) not fired |
| W6 | residue non-identity; AP holders in ≥ ¼ of failing runs; K rival islands ≥ L prop's | first two held (2 of 4 failing runs at N ≥ 200); third **failed** (0.55 vs 0.65); falsifier not fired |
| W7 | RE 3 by ≥ 3 runs | **held** (+15 vs +8) |
| W8 | RE 4 fails, ≥ +0.1 and ≥ +0.2 | **held** |
| W9 | no self-defecting Q unit under K S-self | **held** (by construction; Q extinct by 100) |
| W10 | K − L all-defect in [−2, +2] at 3,200 and 6,400 | **failed at 6,400** (+3); held at 3,200 (+1); falsifier (≥ 4) not fired |
| W11 | K Pangaea 12,800 ≥ 18/20; AP never wins, ≤ 0.2 | **held** (18; max 0.08) |
| W12 | fission–fusion 20/20 in both worlds | **held** |
| W13 | L identity islands' K counterparts open ≥ 0.6, local ≥ 0.6 | open **held** (0.96–1.00); local **failed** (0.03–0.13, the baseline for every island) |
| W14 | Q share ≤ 5·10⁻⁴ at 200; exposure ≥ 2× L's; keyed match 0 | Q share **held** (0); exposure **failed** (0 in K: the exposed readers are dead by 200); keyed match 0 held |
| W15 | rain: K identity 0, cures exploitable rivals; L identity rises ≥ +0.01; K rain uo ≥ ε = 0 − 3 | identity clauses **held** (0; +0.018); cure clause **failed** (K had no exploitable rivals to cure; rain created 7); uo held (18 vs 19) |
| W16 | r arms within 3 runs, K − L same sign; efficiency ≥ 0.98; scramble within 2 | within 3 **held**; same sign **failed** at (6,400, 1) (both n.s.); efficiency and scramble **held** |

## Reading

- **In this grammar world K removes identity under S-nonself entirely, and with it the scaling copy law and the
  clique's cost along the Pangaea continuum.** Universality is 0.75–0.95 at every geometry tested, flat in N·I, equal
  to the proportional control's level; island efficiency ≥ 0.998.
- **It does so by making self-certified defection dead in play, not by keying it to partners.** The key is the literal
  ⌜D⌝; the former TwinD family become certified CooperateBots that PrudentBot accepts and DefectBot eats; they die in
  the scramble. K is a convention that makes own-D readers blind.
- **The provenance rule still matters**, more in K than in L at N = 200: self-play production mints C-identity cliques
  that K does not touch. S-nonself stays necessary under K.
- **The Pangaea's establishment ticket is untouched** (μ_net unchanged); with the cliques gone, mid-sized islands
  (200–800) now beat the Pangaea (20/20 against 18/20), and fission–fusion stays 20/20.
- **The residue is the AP network** (readers of the partner's or the literal ^D box), which rain now feeds instead of
  identity; it is the next rival to remove.
- *Caveats:* finite (N, I, horizon); 20 runs per cell (40 at (100, 64)); N = 100 cells still changing at 10,000; the
  ideal table charges no verification cost; conclusions are relative to grammar P and to K's literal key.
