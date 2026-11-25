# Maximal factorizations of the PD in the provability arm (static; 2026-11-23)

Question (RS): replace off-path refinement by maximality of the factored technology. Static check on the catalogue of
`src/provability.py`, n = 5–9: enumerate maximal symmetric factorizations A × A of the PD (every cell strong Nash in
the catalogue), report count, prior mass, members. Script `src/max_factorizations.py`.

Predictions (the RE's, written before the run):
- F1. Every factorization is strongly equipotent at CC (P11). Falsifier: a clique with a non-CC cell.
- F2. At every n the largest by prior mass contains FairBot and PrudentBot where both exist. Falsifier: either missing.
- F3. From n = 8 there are at least two maximal factorizations, one of them a P*-type family disjoint from
  FairBot's. Falsifier: a unique maximal factorization at n = 8 or 9.
- F4. The largest holds at least 0.8 of the mass of all programs that sit in any factorization. Falsifier: below 0.8.

## Results (`runs/max-factorizations.json`)

| n | classes | members of any factorization | their prior mass | maximal factorizations (sizes) | largest's share of that mass |
|---|---|---|---|---|---|
| 5 | 34 | 3 | 0.0147 | 1 (3) | 1.0000 |
| 6 | 66 | 9 | 0.0149 | 1 (9) | 1.0000 |
| 7 | 218 | 11 | 0.0102 | 1 (11) | 1.0000 |
| 8 | 610 | 19 | 0.0102 | 3 (15, 8, 3) | 0.9995 |
| 9 | 1210 | 27 | 0.0104 | 3 (21, 10, 5) | 0.9993 |

- F1 is vacuous as run: the script requires CC in every cell (the only outcome the pair does not block), so equipotence at CC is built in.
- F2 **falsified**: PrudentBot (`and(BOX(THEM(ME)),BOXD1(THEM(^D)))`, present from n = 8) is not in the largest factorization. It is the one member of the second factorization that the largest lacks; the second overlaps the largest on FairBot's `BOX` family and excludes the `BOX1` family.
- F3 holds: three maximal factorizations at n = 8 and 9, one of them the P\*-type family (`and(BOX1(..),not(BOX(..)))`), disjoint from the largest, mass 4–5·10⁻⁶.
- F4 holds: the largest holds 0.999 of the factorizing mass at n = 8 and 9 (1.000 where it is unique).

Scope: symmetric factorizations A × A only; Nash is checked against deviations inside the catalogue; the free sound oracle arm; mass is the length prior's. Factorizing programs are about 1% of the prior (the rest is mostly constants).

## Addendum (2026-11-24): equipotence alone, anchored on FairBot and PrudentBot (RS's internal/external reading)

Equipotent set here: every cell CC (self-play included); no Nash requirement. Computed inline, same catalogue.

| n | anchor | maximal equipotent sets | largest: members / prior mass / members some catalogue program exploits |
|---|---|---|---|
| 8 | none | 5,804 | 131 / 0.490 / 116 |
| 8 | FairBot | 3 | 131 / 0.490 / 116 |
| 8 | FairBot + PrudentBot | 1 | 24 / 0.0102 / 16 |
| 9 | none | 50,836 | 239 / 0.490 / 218 |
| 9 | FairBot | 6 | 239 / 0.490 / 218 |
| 9 | FairBot + PrudentBot | 1 | 42 / 0.0103 / 32 |

- The RS's claim holds: the maximal equipotent set containing FairBot and PrudentBot is unique and excludes
  CooperateBot (PrudentBot exploits it).
- Outsiders of that set by prior mass (n = 8; n = 9 the same to 0.001): prey of some member 0.482, predators of some
  member 0.034, neither (mutual loss or failed self-play) 0.475.
- The RE's guess that this set equals the strong Nash factorization containing both (8 and 10 members) was wrong:
  the equipotent set is three to four times larger. Removing the members that some catalogue program exploits gives
  exactly that factorization.

## Addendum (2026-11-24): iterated elimination of weakly dominated programs, PD catalogue

Computed inline (all weakly dominated programs removed each round, dominance against surviving programs only).

| n | classes | rounds | eliminated (prior mass) | survivors | CooperateBot | DefectBot | FairBot | PrudentBot | CC share among survivor pairs |
|---|---|---|---|---|---|---|---|---|---|
| 7 | 218 | 2 | 48 (0.018) | 170 | survives | survives | eliminated | absent | 0.10 |
| 8 | 610 | 1 | 130 (0.479) | 480 | eliminated | survives | survives | survives | 0.18 |

The result flips between cutoffs (FairBot out and CooperateBot in at n = 7, the reverse at n = 8) because dominance
depends on which opponents the catalogue contains. It leaves DefectBot and most of the catalogue. Not searched:
order dependence (only the maximal-elimination order was run).

## Addendum (2026-11-24): the RS's recipe (strong Nash, a maximal factorization, then weak-dominance elimination)

Elimination among the members of each maximal strong Nash factorization, dominance judged against the whole
catalogue (the same result against outsiders only).

| n | FairBot's largest | FairBot + PrudentBot | P\* |
|---|---|---|---|
| 8 | 15 → 15 | 8 → 8 | 3 → 3 |
| 9 | 21 → 17 | 10 → 9 | 5 → 5 |

FairBot survives in both of its factorizations, so the recipe does not pick PrudentBot over FairBot here.
PrudentBot earns more than FairBot against 0.474 of the prior (the unconditional cooperators) and less against
0.0085 (the PA+1 provers, e.g. `BOX1(THEM(ME))`, where it gets DD and FairBot CC), so it does not weakly dominate.

## Addendum (2026-11-25): the stable set of the PD program game (`src/stable_set_pd.py`, `runs/stable-set-pd.json`)

Dominance: deviation without response in program space (one player switches and gains strictly, or both switch and
both gain strictly). The construction decides every profile, so the stable set is unique on each catalogue; internal
and external stability checked.

| n | profiles | core (strong Nash) profiles | stable set | of which CC / exploitation / DD | prior mass CC / exploitation |
|---|---|---|---|---|---|
| 5 | 1,156 | 9 | 104 | 16 / 88 / 0 | 0.0004 / 0.471 |
| 6 | 4,356 | 81 | 296 | 144 / 152 / 0 | 0.0004 / 0.469 |
| 7 | 47,524 | 121 | 4,260 | 576 / 3,684 / 0 | 0.0004 / 0.468 |
| 8 | 372,100 | 319 | 42,728 | 1,894 / 40,834 / 0 | 0.0004 / 0.467 |

The stable set contains the core and is, by prior mass, almost entirely profiles in which one program defects on a
program that cooperates with it (first example: DefectBot against CooperateBot). The base PD has no stable set under
the same dominance (CC is dominated by DC, DC by DD, DD by CC).
