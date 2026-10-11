# Spec: prudent openness against identity: can a universal verifier win the scramble, and where is the identity threshold?, 2026-10-11

Status: draft by the RE (Fable); to be reviewed by gpt-6.1-sol; to be run by an Opus subagent. Follow-up to RESULTS
"Identity and tags in the carrier grammar" and DEFERRED 1 (the RS's open decision of 2026-10-11; operating
hypothesis (a): island-level efficiency, universality as a threshold in identity's price).

## Why

The identity run showed that the scramble rewards prudence: an identity clique and the exclusive club win islands
by playing D against the seed's unconditional cooperators (a third of the length prior's seed) while cooperating
with their own kind, and the open carrier CB, which cooperates with unconditional cooperators, converts seeded
copies into islands 3× worse. Two questions follow. **(1)** Is openness itself the handicap, or only niceness to
unconditional cooperators? A *prudent open* carrier (CBP-type: cooperate iff the opponent certifies cooperation
with me and certified defection against plain C) refuses the seed's cooperators as a clique does, yet cooperates
with every certified prudent reader, so it is universal among verifiers. If it establishes like a clique and pools
like a family, the honest target for quoting languages is "universal among programs that verify", and the identity
run's 0/40 was about CB's niceness, not about openness. **(2)** Where is the identity threshold? The identity run
brackets it between 5·10⁻⁴ (about half the runs universal) and 9·10⁻³ (none); a scan at fixed everything turns the
bracket into a curve and says whether it is sharp.

## Design

**Language and law.** Exactly the identity run's grammar, production, checker, K = 10⁶, V = K/4, identity-aware
lumping, holder-based endpoint, lottery law (N = 100 per island, I = 64, mN = 1, iid seeds, horizon 2,000 → 10,000
on separated runs, 40 runs per cell, run-level uncertainty), and its L prior; nothing new is built except the
named-class tilts and the scan.

**Named classes.** CB (open, nice); **CBP** = `if(and(CHK(them,me,C), CHK(them,⌜C⌝,D)), C, D)` (open, prudent);
the prudent open set P_open (every S-guarded establisher that defects on plain C; the identity run's 39 classes of
mass 0.0023); EQ; XC (the exclusive club: prudent and closed); the defection detectors. Static, before any cell: the
seed payoff of each against the L seed; **CBP's family, by a frozen rule** [after review: compatibility is not
transitive]: the maximal pairwise-compatible set containing CBP with the largest pooled mass, chosen from the
compatibility graph before any cell, with its overlaps with CB's set, P_open and XC's set reported, and kept distinct
from the bridge-connected component; whether CBP and CB are compatible (CB certifies cooperation with CBP; CBP
requires CB's certified defection against C, which CB does not have, so my hand reading is that they are *not*
compatible and CBP's family excludes the nice carriers: to be checked); **CBP against XC, checked in two parts**
[after review: my soundness argument was wrong, since CBP defects against CB, which is exactly the behaviour XC
wants certified; soundness forbids false certificates, not certificates of true defection]: (i) executable actions
(does CBP defect against CB in the actual run?), (ii) certificate availability (does the frozen tactic produce
CBP's D script against ⌜CB⌝, and does XC's check accept it?), and then (iii) the enumeration of all compatibility
paths of length ≤ 3 between CBP's family and XC with their seed mass, since direct incompatibility does not exclude
intermediate bridges.

**Part 1: prudent openness.** Mass tilts at matched pooled mass M (the identity run's F_CB mass, 0.031), paired
seeds, each against the untilted L cell: **(P1)** M on CBP's pairwise-compatible set, spread by the prior's relative
weights; **(P2)** M on CB's set (the identity run's T1c reference, rerun on these seeds); **(P3)** M on CBP's set
*and* the identity cliques removed, to measure prudent openness without cliques; **(P4)** M on CBP's set with the
unconditional cooperators removed (mass redistributed by one fixed rule), and **(P4′)** [after review] M on CB's
set with the cooperators removed by the identical rule, so that the CBP–CB difference is estimated with and without
cooperators on matched backgrounds; **(P5)** M split equally between CBP's set and ten EQ spellings, the
head-to-head. Report: universal-prudent runs (the frozen prudent family holds every island), universal-open runs,
patchwork, identity islands, XC islands, seed payoffs, the largest-established-set predictor, cross-island P(C,C)
within the frozen prudent family, among all readers, and overall. [after review] **Stages logged separately:** for
each labelled family per run, the initial copies, the seed islands occupied, the establishment time per occupied
island, the extinction probability of an occupied island's lineage, established islands per occupied seed island,
persistence, and island spread by migration; "islands per seeded copy" is reported beside these, not instead of
them. All cells are reported at common checkpoints (500, 1,000, 2,000, 5,000, 10,000) with unresolved runs
labelled, so no observation time is conditioned on outcome.

**Part 2: the identity abundance threshold** [after review: the scan varies identity's abundance in the seed, not
its syntactic price; it is named so]. Identity-clique mass set to m ∈ {0, 2·10⁻⁴, 5·10⁻⁴, 10⁻³, 2·10⁻³, 5·10⁻³,
9·10⁻³ (= L), 2·10⁻²} by rescaling the 322 clique classes together, with CBP's family held at exactly M where it is
tilted and the remainder renormalized by one fixed rule (overlaps between the scaled and fixed sets resolved by
assigning each class to one group, stated), paired seeds, 40 runs each: the universal-open fraction, identity
islands and cross-island P(C,C) as curves in m, with the expected number of seeded clique copies per run (≈ 6,400·m)
beside them; the **threshold statistic** is the 50% crossing of the universal fraction in m, with a bootstrap
interval, refined by two extra scan points only if the crossing falls between two points more than 2× apart; the
same scan with CBP's family at M as a second curve. **A small scaling panel around the apparent transition:** at the
two scan points bracketing the crossing, (N, I) ∈ {(50, 64), (100, 32), (100, 128)}, to separate a selection
transition from founder occupancy and finite observation time.

**Part 3: the chain** (diagnostic, reduced support as in the identity run): the no-clique control with CBP's set
present, N = 10³ and 10⁴: support, transition structure, the closure and twin-drift checks, and whether the top
cooperative state is prudent-open or the exclusive club; omitted exits of the reduced support are named as the
caveat.

**Scale guard.** The table is the identity run's (reused, cached); the cost is the lottery cells (13 tilts + 8 + 8 =
29 cells of 40 runs). ≤ 3 workers; kill pool children by pid before any driver; check the sibling pids
(`sog_realizable_run`, `fixed_role_chicken_run`) and use 10 minus their worker count, capped at 3.

## Required outputs

`src/prudent_openness.py` (+ `_run.py`, `_report.py`, reusing `src/identity_tags*.py`), `tests/test_prudent_openness.py`
(the tilt seed laws; CBP's hand plays against CB, EQ, XC, C and D by whole runs; the scan's renormalization),
`notes/prudent-openness.md` (§1 the hand plays, the compatibility of CBP with CB and with XC, the seed-payoff
calculation for CBP, the expected copies per run at each m, before any cell; §2 costs), `runs/prudent-openness.md`
and `.json`, a predictions file from the spec committed before any counted cell, the usual hand-back (draft RESULTS,
REJECTED, THEORY §9.2 / DEFERRED 1 edits, NOTATION, ≤ 5 lines, branch name, commits).

## RE predictions (with falsifiers)

1. **Prudent openness establishes like a clique:** under P1 CBP's islands per seeded copy are ≥ 0.35 (identity
   run: EQ 0.47, CB 0.14), its seed payoff is within 0.05 of EQ's, and the prudent open family holds every island
   on ≥ 0.5 of runs at 10,000 (against 0/40 for CB's family under T1c at 2,000 and 7/40 at 10,000). *Falsifier:*
   islands per copy ≤ 0.2, or universal-prudent ≤ 0.2 of runs.
2. **Most of the advantage is made of refusing the seed's cooperators** [revised after review: a residual is
   expected, since CBP and CB also differ in compatibility and in exploitation by other readers]: on matched
   backgrounds the CBP − CB difference in established islands per occupied seed island is at least halved when the
   unconditional cooperators are removed (P4 against P4′, compared with P1 against P2); the sign of the residual is
   not predicted. *Falsifier:* the difference without cooperators ≥ 0.8 of the difference with them.
3. **Head to head, prudent openness beats identity by pooling once it establishes like it:** under P5 the frozen
   prudent family holds more islands than the ten EQ spellings at 10,000 (≥ 0.6 against ≤ 0.3), because its
   spellings absorb each other's islands and EQ's do not. *Falsifier:* EQ ≥ the prudent family at 10,000.
4. **CBP is not compatible with CB; CBP's standing against XC is open** [revised after review]: (i) CBP–CB
   incompatible (CB lacks the certified defection against C); (ii) my bet is that the tactic does produce CBP's D
   script against ⌜CB⌝ and XC accepts it, so XC cooperates with CBP while CBP cooperates with XC iff XC certifies
   cooperation with CBP, making the pair compatible one way or both; the report settles it. Universality is then
   claimed only within the frozen prudent family: its cross-island P(C,C) within the family ≥ 0.9 under P1, with
   no claim on reader-wide P(C,C). *Falsifier:* CBP–CB compatible, or within-family cross-island P(C,C) ≤ 0.7.
5. **The abundance threshold is exponential in copies at low m and saturates** [revised after review]: the
   universal-open fraction follows exp(−6,400·m·q) with one fitted q for m ≤ 10⁻³, deviates upward (saturation of
   establishment) above, and the 50% crossing lies in [3·10⁻⁴, 3·10⁻³]; the scaling panel at the bracketing points
   moves the crossing by ≤ 2× in m. *Falsifier:* a residual ≥ 0.3 at two points with m ≤ 10⁻³, or the crossing
   outside [10⁻⁴, 10⁻²], or the panel moving it by ≥ 4×.
6. **With CBP at M the crossing shifts right modestly, and XC persists in the chain** [revised after review]: the
   50% crossing moves right by a factor in [1.5, 5] (better establishment does not remove established identity
   islands), and in the no-clique chain the top cooperative state is prudent-open at 10³ but XC holds ≥ 0.2 of π
   at 10⁴. *Falsifier:* a shift ≤ 1.2× or ≥ 10×, or XC ≤ 0.05 of π at 10⁴.

The RS is invited to add predictions; the uncertain ones are 3 (whether pooling beats identity once establishment
is matched) and 4 (ii).
