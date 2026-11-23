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
