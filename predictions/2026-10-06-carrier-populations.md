# Predictions: the realizable language, milestone 2: populations of carriers (2026-10-06)

Spec `specs/2026-10-06-carrier-populations.md` (reviewed by gpt-6.1-sol; the [after review] text is the resolution).
Committed after `notes/carrier-populations.md` §1 (commit 80b39b6) and before any project code of this milestone, any
measurement and any counted cell. Every number below is a hand calculation from notes §1 or a guess labelled as such.

## Frozen design (notes §1)

1. **Language and fuel:** L_T^code with milestone 4's library, the sound checker CHK_S at entry 0 (and CHK_S2 at
   entry 5 under E), K = 10⁶, V = ⌊K/4⌋ in every source. A play is the actual run; ⊥ scores as D. PD payoffs of the
   modal arm (D/D −1, D/C 1, C/D −2, C/C 0), w = 0.3.
2. **Grammar (cutoff n = 7, fallback n = 6 as a different experiment):** A ::= C | D | if(B, A, A); B ::= CHK_e(p, q, a)
   | not B | and(B, B) | or(B, B); p ∈ {them, me}, q ∈ {me, them, ⌜C⌝, ⌜D⌝}, a ∈ {C, D}; one node per constant, atom
   and connective; ⌜C⌝, ⌜D⌝ are milestone 4's plain PROG_C / PROG_D.
3. **Production:** milestone 4's frozen tactic and passes (D script vs ⌜D⌝ with an empty list, then C scripts vs the
   probes CB, CB1, CBP); P: list free; O: `none | produced`, one bit; E: mode 0 vs entry-0 probes then mode 5 vs
   entry-5 probes.
4. **Tables:** the ideal table (host replay `HostCheck`, no EvR* budget) on every pair of run-tree types τ; the
   executable table (checker term at K = 10⁶) on the lumped classes' representatives; plays by composition of clean
   check values (validated against whole plays); Lemma T (τ-symmetry) extends both to spellings.
5. **Lumping:** rows and columns against every spelling equal, self and cross-twin cells included; class mass = sum.
6. **Priors:** L = 2^−nodes (O: +1 node per list choice; E: +1 node per CHK_5 atom; E-eq: +1 per atom); U = uniform
   over lumped classes; L_std = the repo's Elias-gamma μ (labelled sensitivity, notes §1.6).
7. **Chain:** LogChain over classes, seeded (monomorphic, stable candidates ≤ 3 classes, invasion closure),
   θ_log = 10⁻¹⁴ (10⁻¹² / 10⁻¹⁶ at N = 10⁴), N ∈ {10³, 10⁴, 3·10⁴, 10⁵}, arms L×P, U×P, L×O, L×P×E (+ E-eq, L_std).
8. **Lottery:** (N, I) = (100, 64), mN = 1, 40 runs per arm (L×P, U×P, L×O, L×P×E), horizon 2,000 generations.
9. **Workers ≤ 3; ≤ 2 while pid 74221 or 74545 (another experiment's chain) is alive** (both alive at commit time).

## Endpoint revision (before any cell; replaces the closure test of notes §1.9)

Z(island) = closure of the island's residents under "a class present anywhere joins if U(q, z) ≥ U(z, z) for some
z ∈ Z". **Resolved cooperating** iff every class in Z self-cooperates; **resolved non-cooperating** iff no class in Z
self-cooperates; otherwise unresolved. *Reason:* the committed test ("every pair in Z × Z has the same outcome") would
call a CB island unresolved whenever Cc and CBP are both present, although CBP strictly beats Cc and every endpoint is
cooperative. The new test is sound: if every z ∈ Z self-cooperates, any class outside Z earns ≤ −1 against every z,
while any mixture of self-cooperators averages > −1 among themselves (a pair of self-cooperators sums to ≥ −2, and the
diagonal is 0), so nothing outside Z enters any Z-mixture, and among self-cooperators the only non-(C, C) pairs are
dominance (1, −2) or coordination (−1, −1), so the replicator ends monomorphic or in an all-(C, C) mixture.

Three endpoints, all reported for every lottery arm:
- **E1 (the spec's):** every island monomorphic and resolved (Z from its incumbent). Polymorphic islands censored.
- **E2 (the spec's wording read one-step):** every island monomorphic in a; no present class q with U(q, a) > U(a, a);
  no present q with U(q, a) = U(a, a) and U(q, q) > U(a, q).
- **E3 (polymorphic islands allowed):** Z seeded with every resident; every island resolved.
RE 1 is scored on E1 as the spec defines it; E3 is reported beside it, and my S14 is about E3.

## Static numbers by hand

- Spellings: P 130 / 2,242 / 12,546 at n ≤ 5 / 6 / 7; O twice that; E 258 / 8,578 / 49,666. At most two atoms per
  program at n ≤ 7, so at most two check calls per run, and the global counter cannot bind (2(V + 6) + 10³ < K).
- Raw mass under L (P) by shell: n = 1: 1, 4: 4, 5: 2, 6: 33, 7: 80.5 (total 120.5). Each constant 0.0041; CB
  (`if(S_C, C, D)`) 5.2·10⁻⁴; CBP 6.5·10⁻⁵. Under L_std: each constant 0.434, CB 8.5·10⁻⁴, CBP 1.7·10⁻⁶.
- Run trees with only C leaves (unconditional cooperators by construction): 1 + 16 + 16 + 528 + 2,064 spellings,
  mass 26.375/120.5 = **0.219** under L; the same for only-D leaves (by the C↔D leaf symmetry). Certified shadows of
  CB are a subset (frozen-tactic coverage).
- CB's run tree (node(S_C, C, D)) has four spellings (`if(S_C, C, D)`, `if(not S_C, D, C)` and the double and triple
  negations), mass (1/16 + 1/32 + 1/64 + 1/128)/120.5 = 9.7·10⁻⁴. Guess (not a count): all establishers together
  ≈ 0.3–1% under L.
- Shadow-to-establisher mass ratio under L ≈ 20–70 (guess from the two numbers above), against ≈ 500 under L_std
  (each constant 0.434 against establishers ≈ 10⁻³).
- Lemma G (notes §1.7): no S-guarded establisher has a strict invader.
- Hand plays among Cc, Dc, CB, CB1, CBP, LöbC, CBdef: notes §1.7 table.

## RE predictions (verbatim from the spec, with falsifiers)

[after review: the numerical clauses are kept as the RE's bets but the predictions are scored on their mechanism
clauses; a number missed with the mechanism intact is recorded as a miss of the number.]

1. **Almost all seeds, realizably:** under L×P the lottery's success interval excludes 0.5 and the point estimate is
   ≥ 0.8 (my bet: ≥ 0.9), with establishment within 100 generations in most runs; the winning classes are CB- and
   CBP-shaped carriers. *Falsifier:* the success interval excluding 0.7 from above, or a run won by a non-carrier.
2. **The chain transfers by the same mechanism:** under L×P the top cooperative state's exit is neutral drift into a
   shadow (Ccert-type or C) followed by D's strict entry, ∝ 1/N, and no exit is N-independent, so P(C,C) rises over
   the N range (my bet for the local odds slope: [0.3, 0.6], against the modal arm's 0.44). *Falsifier:* an
   N-independent exit out of the top cooperative state, or P(C,C) falling over the range.
3. **No false atom, but exploitable establishers** [split after review]: (a) 0 false accepted atoms in the whole
   table (soundness); (b) for the hand-proved subclass (CB-, CB1- and CBP-shaped carriers over entry 0) no class
   strictly exploits them except through a shadow; (c) at least one establisher *outside* that subclass (a Boolean
   template cooperating for a reason other than certified opponent cooperation) is strictly exploited. *Falsifier for
   (a):* any false atom; *for (b):* a strict non-shadow entry into a CB/CB1/CBP population; *for (c):* no exploited
   establisher in the catalogue.
4. **Optional production is a defector tax, not a shadow:** under L×O certificate-less spellings are refused by
   carriers, so they enter no carrier population neutrally; P(C,C) at 10⁴ is lower than under L×P (my bet: by at most
   0.15) and the exponent keeps its sign; in the lottery L×O's success is lower than L×P's by establishment, not by
   π. *Falsifier:* a certificate-less spelling entering a carrier population neutrally, or the exponent changing sign.
5. **The checker entry is a convention; bridges decide separation** [revised after review]: under E, bridges (classes
   cooperating with carriers on both entries) exist in the catalogue only as unconditional cooperators (C, Ccert)
   or as two-atom `or` templates, and every bridge is a shadow of one side (exploitable); so the chain puts ≥ 0.9
   of cooperative π on one entry at every N and the lottery ends with both entries alive on a positive fraction of
   runs (my bet ≥ 0.3), metastably. *Falsifier:* a non-shadow bridge (a class cooperating with both entries and not
   strictly invaded by D) stable on an island, or cooperative π split between entries at ≥ 0.3 each at N = 10⁵.
6. **The prior does not flip the verdict here** (unlike concessions): U×P and L×P are both cooperative at N = 10⁴
   (P(C,C) ≥ 0.5 in both), because carriers are the bulk of the lumped classes under either prior. *Falsifier:* one
   arm ≥ 0.5 and the other ≤ 0.2.
7. **Executable verification costs a constant, not the mechanism** [added after review]: the matched
   ideal-verification table differs from the executable table only in timeout cells (plays whose checks exceed V at
   K = 10⁶), and the chain's P(C,C) under the ideal table is within 0.1 of the executable one at every N. *Falsifier:*
   a cell differing for a non-timeout reason, or a P(C,C) gap above 0.25.

## Subagent predictions (with falsifiers)

S1. **Soundness:** 0 accepted false atoms among all T checks of the ideal τ table and the executable class table, at
    K = 10⁶ and in the K-sensitivity cells. *Falsifier:* one.
S2. **No timeouts at K = 10⁶:** the executable class table equals the ideal table in every cell, and the largest
    inner cost of any executable check is < 10⁵ (V = 2.5·10⁵). *Falsifier:* a differing cell, or a check ≥ 10⁵.
S3. **Lemma G, exhaustively:** no S-guarded establisher class has a strict invader (in every arm). *Falsifier:* one.
S4. **No exploited establisher (against RE 3(c)):** no establisher class of L×P at n = 7 is strictly exploited by any
    class. *Falsifier:* one exploited establisher. (Confidence 0.6.)
S5. **Mass split under L×P:** classes that cooperate with every class hold ≥ 0.1 of the mass; establishers ≤ 0.03.
    *Falsifier:* either bound violated.
S6. **The top cooperative state is prudent:** under L×P at N = 10⁴ the most probable cooperative state is a
    monomorphic establisher that refuses Cc (CBP-like) or a polymorphism containing one; every exit from it is
    neutral (Δ1 = 0). *Falsifier:* a non-prudent top state, or a strict exit.
S7. **Level and slope under L×P (guess):** P(C,C) at N = 10⁴ in [0.1, 0.7], rising over 10³ → 10⁵ with a local
    log-odds slope in [0.2, 0.7] between 10⁴ and 10⁵. *Falsifier:* outside either interval.
S8. **Bor is a non-shadow bridge** (notes §1.7): it cooperates with CB on entry 0, with CB on entry 5, with itself,
    defects on D, and has no strict invader in the E catalogue. *Falsifier:* any clause fails.
S9. **Entries share cooperative π under E (against RE 5):** at N = 10⁵ each entry's establishers hold ≥ 0.2 of
    cooperative π under L×P×E (entry 0 the larger, about 2:1 by the label's price), and 0.4–0.6 each under E-eq.
    *Falsifier:* one entry below 0.2 under E, or outside [0.4, 0.6] under E-eq.
S10. **O:** every certificate-less spelling is either a D-twin against carriers ((D, D) with every establisher) or a
    sucker; none enters a carrier population neutrally; L×O's P(C,C) is within 0.1 of L×P's at every N.
    *Falsifier:* a neutral entry, or a gap > 0.1.
S11. **Ideal = executable chain:** identical class tables, so identical π (to 10⁻⁹). *Falsifier:* any difference.
S12. **K sensitivity:** the establishers' mutual plays and the top state's exit edges are identical at
    K = 3·10⁵, 10⁶ and 3·10⁶. *Falsifier:* a change in any decisive cell.
S13. **U×P (guess):** under U×P P(C,C) at 10⁴ is lower than under L×P (unconditional cooperators split into few
    classes while D-like and conditional-defecting classes are many). *Falsifier:* U×P ≥ L×P at 10⁴.
S14. **Lottery under E3 (guess):** under L×P at least 0.5 of runs resolve cooperating by the horizon under E3, and
    E1 censors at least half the runs (neutral cooperating variants keep islands polymorphic). *Falsifier:* E3
    success < 0.5, or E1 censoring < 0.5.
S15. **Twin-expanded = unlumped on n ≤ 5:** class-aggregated P(C,C) agrees to 10⁻⁶ relative at N = 10³ and 10⁴.
    *Falsifier:* a larger difference.

The RS has not added predictions (none in the spec).
