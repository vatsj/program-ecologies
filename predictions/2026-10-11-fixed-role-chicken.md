# Predictions: chicken and hawk–dove with fixed roles and without `ROLE` (2026-10-11)

Spec `specs/2026-10-11-fixed-role-chicken.md` (reviewed by gpt-6.1-sol; the [after review] text is the resolution).
Committed after `notes/fixed-role-chicken.md` §1 (commit 62f2594) and before any project code of this experiment and
any counted cell. Every number below is a hand calculation from notes §1 or a guess labelled as such.

## The RS's prediction (verbatim, registered first)

> I'll predict (for chicken) that some islands will learn norms where one side "wins" the straight play and the
> other role is forced to swerve.

*Scored* (spec, after review) on the per-island establishment probability of a one-sided norm by play (notes §1.6):
it holds if, in fixed-role chicken under the seed lottery, a positive fraction of islands is established at R1 or R2
(by play, tolerance 0.95, held through the last tenth of the horizon), with the fraction and its run-level interval
reported per cell.

## The RE's predictions (verbatim from the spec)

[after review: the RS's qualitative claim is scored on per-island establishment of a one-sided norm by play; my
numbers are bets on top of it, and success and falsifier ranges meet.]

1. **The RS's prediction holds in the lottery at mN = 0:** in every game and arm the per-island probability of
   ending at a one-sided convention (by play) is ≥ 0.6 (my bet ≥ 0.9), the role-1/role-2 split is within [0.25, 0.75],
   and the constants-only control already produces the norms (ordinary anti-coordination), with source reading
   changing the per-island probability by ≤ 0.1. *Falsifier:* per-island probability < 0.6, or a split outside
   [0.25, 0.75]; a reading effect ≥ 0.25 is a miss of the control clause. (Both conventions appearing somewhere among
   64 islands is near-automatic and is not scored.)
2. **Migration does not simply merge the norms** [revised after review]: at mN = 1 the two conventions are rival
   networks; identical readers in opposite roles anti-coordinate only through the role signal, so candidate bridges
   are role-specific; my bet is that ≥ 0.4 of runs are still patchworks at 4,000 generations, and that resolutions
   that do occur run through demographic takeover by the majority convention (migration-driven), not through reader
   mediation; the forced-island control with bridges removed changes the resolution rate by ≤ 0.1. *Falsifier:*
   ≤ 0.1 of runs patchworks at 4,000, or the bridges-removed control cutting resolutions by ≥ 0.4.
3. **Neutral neighbourhoods, exits by the full escape path** [revised after review]: π splits between the two
   conventions; each convention has a neutral neighbourhood (readers matching the on-path action) and its exit
   scaling is set by the complete escape path, which I bet is neutral entry then a strict switch (∝ 1/N) in chicken
   and may pass through a polymorphic trap in hawk–dove; no genuine limit cycle; crash states ≤ 0.05 of π.
   *Falsifier:* a cycle, a crash state ≥ 0.2, or an exit that is N-independent.
4. **Provable commitment does not change the norm:** on the matched grammar/prior control with paired seeds the
   modal arm's per-island convention probabilities are within 0.1 of the weak arm's. *Falsifier:* a difference
   ≥ 0.25.
5. **The crash parametrization lowers crash exposure, not convention frequency** [revised after review]: the C = 6
   hawk–dove has per-island convention probabilities within 0.1 of chicken's and a lower on-island crash rate; no
   claim on exit speed. *Falsifier:* a convention-probability difference ≥ 0.25, or a higher crash rate at C = 6.

*Scoring conventions I fix now (where the spec is silent).* RE 1 is scored on every two-population cell at mN = 0
(arms weak, modal, W0, M0, const; games; N ∈ {25, 50, 100}), the split pooled over the cell's convention islands.
RE 2 is scored on the natural-seed cells at mN = 1, N = 100 (weak and modal, each game), the patchwork fraction per
cell, and on the forced-island control (resolution rate with bridges minus without). RE 3 on the two-population
chains (weak, modal, W0, M0) at N ∈ {10², 10³, 10⁴}; the arm-(c) one-population chain is reported beside it. RE 4 on
the W0/M0 lottery at mN ∈ {0, 1}, N = 100. RE 5: "on-island crash rate" is the second-half time average of the
islands' crash probability J(St, St), pooled per cell, at mN = 1 and N = 100 in the weak and modal arms (at mN = 0 it
is ≈ 0 after establishment and is reported, not scored); since the spec's comparison class is ambiguous, I score it
against chicken (the literal sentence) and report the comparison with hd3 (the C = 3 hawk–dove) beside it.

## My predictions (subagent; S-numbered, each with a falsifier)

**S1 (static closure).** In every arm with bridges (weak, modal, W0, M0) and every game, the Δ ≥ 0 graph on the K²
monomorphic pairs has exactly one closed class that contains a convention, and it contains both conventions; the
constants-only control has two closed classes, one per convention. *Falsifier:* a closed class containing exactly one
convention in a reader arm, or a closed class with no convention holding ≥ 0.05 of π at any N.

**S2 (chain π).** In every two-population chain π(R1) = π(R2) to 10⁻⁶ (role-exchange symmetry), the two conventions
together hold ≥ 0.98 of π at N ≥ 10³ and ≥ 0.95 at N = 10², and crash states hold ≤ 10⁻³. *Falsifier:* conventions
< 0.95 at N ≥ 10³, an asymmetry > 10⁻⁶, or crash > 10⁻².

**S3 (exit and its path).** Each convention's exit rate per unit mass satisfies N·exit ≈ ½ μ_B (notes §1.4: weak
9.3·10⁻⁴, modal 1.55·10⁻², W0 and M0 1.98·10⁻³), within a factor 1.5 at N = 10³ and 10⁴, the same in the three games;
≥ 0.9 of the exit flux leaves through a state whose winner is a bridge, by the loser's strict step with
Δ = T − S (N·Δ = 3N chicken, 2N hawk–dove; ρ_∞ 0.593 and 0.451), after a neutral step (N·ρ = 1). The constants-only
exit is deleterious (log rate ∝ −N). *Falsifier:* N·exit changing by more than 2× between 10³ and 10⁴, off ½ μ_B by
more than 3× at 10⁴, or non-bridge exits carrying > 0.1 of the exit flux.

**S4 (lottery, mN = 0).** Per-island establishment of a one-sided norm ≥ 0.97 at N = 100 and ≥ 0.9 at N = 25 in
every two-population cell including constants-only; the role-1 share of convention islands within 0.5 ± 0.06 per
cell (pooled over its 40 runs, 2,560 islands); dove and crash islands ≤ 0.02. *Falsifier:* < 0.9 at N = 100 in any
cell, or a split outside [0.4, 0.6].

**S5 (lottery, mN = 1, natural seeds: who mediates).** At N = 100 in the reader arms, ≥ 0.8 of island flips are
reader-mediated (winner bridge share ≥ f* at the last convention sample; f* = 0.75, 0.2, 0.5) and the patchwork
persistence at 4,000 is ordered by f*: patchwork fraction chicken ≥ hd6 ≥ hd3 within each arm. *Falsifier:* < 0.6 of
flips reader-mediated (with ≥ 20 flips in the cell), or hd3's patchwork fraction above chicken's by more than 0.15 in
either arm.

**S6 (forced islands).** With bridges removed there are no island flips at N = 100 in any game (the deleterious
fixation of a loser-seat Straight migrant is ≤ 5·10⁻⁸ per migrant: hd3 4.9·10⁻⁸, hd6 and chicken smaller); with
bridges included (β = 0.1) flips occur in every game in the modal arm, and the resolution-rate difference
(included − removed) is ≥ 0.4 in at least one game. *Falsifier:* any flip with bridges removed in more than 1 of 40
runs of a cell, or no flips with bridges included in any modal cell.

**S7 (constants-only, mN = 1).** At N = 100 every run is a permanent patchwork (≥ 0.95 patchworks at 4,000, 0 flips).
At N = 25 in hd3, demographic flips occur (hand: a loser-seat Straight migrant fixes with ρ = 3.9·10⁻³, about 2·10⁻³
first steps per island per generation, ≈ 8 per island by 4,000), so this is the one place where the RE's "demographic
takeover" can operate; chicken and hd6 have none at any N tried. *Falsifier:* any flip in a constants-only cell at
N = 100, or no flip in the hd3 N = 25 constants cell.

**S8 (matched control).** W0 and M0 per-island convention probabilities differ by ≤ 0.03 at mN = 0 and ≤ 0.1 at
mN = 1 (the two play tables differ in 0.45% of program pairs, all matcher–bridge cells; the bridge masses are equal).
*Falsifier:* a difference ≥ 0.1 at mN = 0.

**S9 (one population, modal, no `ROLE`).** No island of arm (c) reaches a one-sided norm (asymmetric outcome ≤ ½ by
arithmetic). In the chain π stays on hawk–dove-type polymorphisms (Straight with swervers or bridges; the matcher
`BOX(THEM(ME))`, "swerve iff you provably swerve against me", cannot enter them because it crashes into the Straight
share, a deleterious x*(S − P)); π-weighted P(dove, dove) ≤ 0.5 at every N in every game. *Falsifier:* π-weighted
mutual dove ≥ 0.5 in any game at N ≤ 10⁴.

**S10 (crash exposure).** At mN = 1, N = 100 the on-island crash rate is ordered by the crash's cost, chicken < hd6 <
hd3: a loser-seat Straight migrant is removed at rate ∝ w(S − P) = 2.7, 0.6, 0.15, so cheaper crashes linger. So RE 5's
crash clause fails against chicken (C = 6 crashes more than chicken) and holds against hd3. *Falsifier:* hd6's crash
rate below chicken's.

**S11 (implementation symmetry).** The swap test with a fixed seed gives the exact mirror image; the role-swapped
cells' role-1 share of convention islands lies within the unswapped cell's 95% interval and within 0.5 ± 0.06.
*Falsifier:* a mismatch in the mirror test, or a role-1 share outside 0.5 ± 0.1 in any cell.

## Hand numbers (from notes §1)

| quantity | chicken | hd3 | hd6 |
|---|---|---|---|
| T, S, P, R | 2, −1, −10, 0 | 2, 0, −½, 1 | 2, 0, −2, 1 |
| convention benchmark T + S (per encounter) | 1 | 2 | 2 |
| one-population mixed equilibrium x*, payoff | 2/11, −0.18 | 2/3, 0.33 | 1/3, 0.67 |
| loser-seat flip threshold f* = (S − P)/(T − P) | 0.75 | 0.2 | 0.5 |
| strict escape step Δ = T − S, ρ_∞ = 1 − e^{−wΔ} | 3, 0.593 | 2, 0.451 | 2, 0.451 |
| constants: loser-seat Straight migrant fixation, N = 25 / 50 / 100 | < 10⁻²⁸ | 3.9·10⁻³ / 9.0·10⁻⁵ / 4.9·10⁻⁸ | 2.5·10⁻⁷ / 2·10⁻¹⁴ / < 10⁻²⁵ |

| arm | classes | bridge mass μ_B | hand N·exit ≈ ½ μ_B | π(R1) = π(R2) |
|---|---|---|---|---|
| weak | 46 | 0.00185 | 9.3·10⁻⁴ | ½ each |
| modal | 51 | 0.0310 | 1.55·10⁻² | ½ each |
| W0 | 12 | 0.00396 | 1.98·10⁻³ | ½ each |
| M0 | 8 | 0.00396 | 1.98·10⁻³ | ½ each |
| const | 2 | 0 | e^{−Θ(N)} | ½ each |

Lottery at mN = 0: per-island one-sided norm ≈ 1 everywhere, split ≈ ½ (a symmetric saddle broken by drift).
