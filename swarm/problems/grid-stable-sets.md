# Problem: stable sets of majority division on a grid

## Background

Three players divide one unit of money. Any two of them can impose a division. Von Neumann and Morgenstern's stable
sets are a classical solution concept for this game. On the continuum they found the symmetric solution
{(1/2, 1/2, 0), (1/2, 0, 1/2), (0, 1/2, 1/2)} and also infinitely many "discriminatory" solutions. Here the money comes
in indivisible units.

## Definitions

Fix an integer K ≥ 2.
- An **allocation** is a triple x = (x_1, x_2, x_3) of nonnegative integers with x_1 + x_2 + x_3 = K (shares in units
  of 1/K).
- Allocation x **dominates** y if there are two distinct players i, j with x_i > y_i and x_j > y_j (both strictly better
  off, so they can impose x).
- A set V of allocations is **stable** if:
  - it is internally stable: no element of V dominates another element of V;
  - it is externally stable: every allocation not in V is dominated by some element of V.

## Questions

1. For which K does a stable set exist?
2. For each such K, find all stable sets.
3. Prove your answers for every K ≥ 2.

## Checker

`/work/check.py` tests a proposed set: `python3 check.py K "a,b,c a,b,c ..."`. It reports internal and external
stability, with a witness when either fails.

## Success and stopping

You have succeeded, and should stop, when all of the following hold:
1. `/work/answer.md` states the exact answer to questions 1 and 2 for every K ≥ 2.
2. `/work/answer.md` contains complete proofs, covering both existence (or non-existence) and the completeness of your
   list of stable sets for every K.
3. You have written the file `/work/SUBMIT` (any content). Writing `SUBMIT` ends the attempt immediately for everyone
   working on it, so write it only when 1 and 2 are done.

If time runs out before you submit, whatever is in `answer.md` at that moment is graded.

## Deliverable

`/work/answer.md` as described above, with any code you used in `/work`. Mark partial results clearly.
