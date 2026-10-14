# Predictions: stable sets on islands (2026-10-13)

Spec `specs/2026-10-13-stable-sets-on-islands.md` (reviewed by gpt-6.1-sol and gemini-4-argon); design and
definitions in `notes/stable-sets-on-islands.md` §1 (committed before this file). Committed before any code of this
experiment and before any counted cell. The lottery is finite-size ε = 0 evidence; the chain (rare mutation) is a
separate object and is never pooled with it.

## The RS's claim (verbatim, first)

> vNM stable sets lend themselves to a very natural claim on our island model: each element of the stable set shows
> up on an island.

Scored per run in two forms: **strong** (the run's island support, the set of non-mixed island classes at the
horizon, lies inside some stable set of the enumeration on the game's realizable outcomes R) and **weak** (every
element of the symmetric stable set V\* is held by some island = coverage). Scored at 500 / 1,000 / 2,000 and at
10,000 for unresolved runs, in every cell; the headline is L at mN = 0 and mN = 1.

## The RE's predictions (verbatim from the spec)

1. **Coverage holds at mN = 0, and is a weak test** [revised after review: with member occupancy q the independence
   baseline is 1 − 3(1 − q/3)^64 + 3(1 − 2q/3)^64 − (1 − q)^64, near certain for modest q]: every element of the
   symmetric set is held by some island in ≥ 0.9 of runs, and the informative number is member occupancy, which I
   bet is ≥ 0.6 of islands at the horizon. *Falsifier:* coverage ≤ 0.7, or members ≤ 0.4 of islands.
2. **Role symmetry across runs is robust; within-run symmetric selection is not guaranteed** [revised after review]:
   across runs each pair is the modal member on ≈ ⅓ of runs under the symmetric seeds (within 0.1), while within a
   run the island support lies inside the symmetric set alone in my bet ≥ 0.5 of runs, inside some discriminatory
   set as well in the rest; under the tilted seed the support populates a discriminatory line (the tilted slot at
   c) on ≥ 0.3 of islands. *Falsifier:* role asymmetry ≥ 0.2 across runs under a symmetric seed, or the tilted seed
   leaving the discriminatory line at ≤ 0.1 of islands.
3. **Non-member outcomes are transient:** islands reaching the fair three-way or a wasteful outcome leave it within a
   median of 200 generations (censoring reported), and ≤ 0.1 of islands sit on a non-member at the horizon.
   *Falsifier:* a non-member holding ≥ 0.25 of islands at 10,000.
4. **Flips between members pass through an outsider, and migration can still produce consensus** [revised after
   review: members of one set cannot dominate each other directly]: every member-to-member flip traverses at least
   one non-member state, ≥ 0.8 of the steps out of that state are external-stability moves under relation (M), and
   consensus on one member across every island happens in ≤ 0.3 of runs at 10,000, through bridge classes as in
   chicken where it happens. *Falsifier:* ≤ 0.5 of exit steps following the arrows, or consensus in ≥ 0.6 of runs.
5. **Source reading changes nothing here:** the modal cell's coverage, selection and transience are within 0.1 of
   the weak arm's. *Falsifier:* a difference ≥ 0.25.
6. **Myopic beats farsighted:** where the farsighted and myopic sets differ on this grid, islands sit on the myopic
   set's elements. *Falsifier:* ≥ 0.2 of islands on farsightedly stable outcomes that are not myopically stable.
7. **Gemini's counter-prediction, registered** [after review by gemini-4-argon]: at mN = 0 the strict symmetric set
   holds < 0.4 of islands, all pairs combined (unequal ones included) hold > 0.7, because fixed-role scramble
   dynamics establish greedy demands against accommodators (the chain's rotating dictatorship); and at mN = 1 one
   pair or a two-pair cycle sweeps the metapopulation by 10,000 unless the three pairs re-invade each other. The
   RE's prediction 1 and this are scored against each other: if the symmetric set holds < 0.4 and unequal pairs
   dominate, the ecology sits on dominated outcomes and the RS's claim fails in its strong form (the stable set's
   elements may still each appear somewhere, which is the weak form, scored separately).

**Scoring notes fixed now (from notes §1, before any data).** (i) "Discriminatory set" in RE 2 and the tilted-seed
clause: the game's realizable outcomes contain no three-positive allocation except (2, 2, 2) (notes §1.1), so on R
no discriminatory element is realizable; RE 2's tilted clause is scored as stated (fraction of islands on a
discriminatory-line element with the tilted slot at c > 0), and it can only fire. (ii) RE 4's first clause is scored
on the flip's sequence of non-mixed classes; mixed spells whose support is ≥ 0.95 members ("member-mixed") are not
non-member states; the notes predict the clause fails (member flips are pure drift through member-mixed states).
"Steps out of the non-member state" are the steps from a non-mixed non-member class to the next non-mixed class.
(iii) RE 6 is scored against the farsighted sets the enumeration finds; if no outcome is farsightedly but not
myopically stable, RE 6 is void. (iv) RE 7's first clause is scored at the 2,000 horizon of L, mN = 0; "unequal pairs
dominate" = unequal pairs hold more islands than fair pairs; its sweep clause = consensus on one class at 10,000.

## The subagent's predictions (S1–S15), with falsifiers

- **S1 (enumeration on R).** Under M (= C on R, notes C1) V\* is the **unique** stable set on R; unequal pairs,
  wasteful pairs, (2, 2, 2) and (0, 0, 0) are in no stable set. *Falsifier:* any second stable set.
- **S2 (classical grids).** V\* (and its 1/8 analogue {(4,4,0), …}) is stable on G6, G6=, G8, G8=; **no
  k-discriminatory stable set exists on G6 or G6=** at any c > 0 (Lemma G plus repair failure). No bet on G8.
  *Falsifier:* a k-discriminatory stable set on G6 or G6=.
- **S3 (L, mN = 0, at 2,000).** Member occupancy q ∈ [0.2, 0.45]; unequal pairs ∈ [0.3, 0.55]; all pairs > 0.7;
  coverage ≥ 0.95 of runs; the strong form of the RS's claim holds in ≤ 0.05 of runs, the weak form in ≥ 0.95.
  *Falsifier:* q > 0.6, or unequal < 0.2, or the strong form in ≥ 0.2 of runs.
- **S4 (L, mN = 1, at 2,000).** Fair pairs ∈ [0.2, 0.45] of islands, unequal pairs ≥ 0.5 of pair islands (the chain's
  ratchet: unfair/(fair + unfair) = 0.61 at N = 100); ≥ 20 flips per run by 2,000. *Falsifier:* fair ≥ 0.6, or
  unequal < 0.3 of pair islands.
- **S5 (member → member flips).** ≥ 0.8 traverse no non-member non-mixed class; ≥ 0.7 are pure drift by the trigger
  taxonomy. *Falsifier:* < 0.5 traverse no outsider.
- **S6 (member → unequal flips).** ≥ 0.7 are drift-prepared (a neutral change, typically the excluded slot, before the
  pivot's strict move). *Falsifier:* ≤ 0.4.
- **S7 (controls K and M at mN = 0).** |q_K − q_L| ≤ 0.05 and |q_M − q_L| ≤ 0.05 (paired seeds for M).
  *Falsifier:* a difference ≥ 0.15.
- **S8 (A, tilted slot 3).** Among islands held on a pair containing slot 3, slot 3 is the 2/6 member on ≥ 0.5 (L:
  ≈ 0.25 by symmetry: half the pair islands with slot 3 are unequal, half of those with slot 3 low); 0 islands on a
  discriminatory element (impossible on R). *Falsifier:* slot 3's 2/6 rate ≤ L's.
- **S9 (U, uniform over programs).** Conditional-rich seeds leave more islands mixed or in disagreement than L
  (≥ 0.1 more at 2,000, mN = 0). *Falsifier:* U's mixed + disagreement ≤ L's.
- **S10 (F-entry, β = 0.25, mN = 0).** The target's island rate rises to ≥ 0.5 for the member and the unequal pair, and
  stays ≤ 0.3 for the wasteful pair (a member raising 2 → 3 gains strictly) and ≤ 0.4 for the grand coalition.
  *Falsifier:* member entry ≤ 0.3, or wasteful ≥ 0.5.
- **S11 (F-residence, mN = 1).** Median residence: wasteful < unequal < member; the grand coalition (exits deleterious
  at first step) has the longest. *Falsifier:* member median residence below the unequal pair's.
- **S12 (code checks).** C = M on R (Lemma I, C1) and chicken's C-stable sets are exactly {R1}, {R2}. *Falsifier:* any
  mismatch.
- **S13 (resolution at mN = 1).** ≥ 0.8 of L mN = 1 runs are unresolved (not globally closed) at 2,000; at 10,000 at
  most 0.3 reach consensus. *Falsifier:* < 0.5 unresolved at 2,000.
- **S14 (extended grids, constants, mN = 0).** Grand outcomes (all discriminatory-line elements included) hold ≤ 0.1 of
  islands on both grids; pairs ≥ 0.7. *Falsifier:* grand outcomes ≥ 0.25.
- **S15 (farsighted contrast).** Some farsighted stable set on R is a singleton fair pair (notes §1.6), so the
  farsighted and myopic sets differ; on the islands, the member-occupancy profile cannot distinguish them (every
  singleton fair pair is inside V\*), so RE 6 is void on R. *Falsifier:* no farsighted stable set differs from V\*.

## Hand numbers

- Prior: constants 0.976 of each slot's length prior, each (partner, demand) constant 0.1084; a seeded island-slot
  holds ≈ 11 of each constant and ≈ 2.4 conditionals; ≈ 158 distinct canonical functions per slot per run.
- Coverage baseline at I = 64 (notes §1.9): q = 0.1 → 0.69; 0.15 → 0.89; 0.2 → 0.96; 0.3 → 0.996; 0.6 → 1 − 1.9·10⁻⁶.
  So RE 1's coverage clause is implied by q ≥ 0.2 and carries no information above it.
- The chain at N = 100 (published): fair pairs 0.373, unfair 0.590, wasteful 0.026, grand 0.010 of π; unfair share of
  pair mass 0.61. The fixed-role two-player `dollar3` lottery (m = 0): 50–50 0.30, 1/3–2/3 0.34 of islands.
- Selection scale on an island: N·w·Δu = 100 · 0.3 · 1/6 = 5 for a one-unit (1/6) gain; ρ(Δu = 1/6) = 0.049 at N = 100.
