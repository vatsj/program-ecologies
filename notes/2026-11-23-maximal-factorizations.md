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
