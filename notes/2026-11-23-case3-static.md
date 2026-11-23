# Strong Nash in the provability arm against the two cores: static check (2026-11-23)

Question (RS, 2026-11-23): under sound on-path reading ("case 3"), PROOFS P6–P9 put the strong Nash outcomes of a
program game between the β-core and the α-core of the base game, the end depending on who reads whom. Which end does
our provability arm sit at?

Object. `src/provability.py` (free sound box, PA and PA + Con(PA), probes `THEM(ME)`, `THEM(THEM)`, `THEM(^A)`), the
catalogue of canonical functions at n = 5–9 (34 / 66 / 218 / 610 / 1,210 classes), both players drawing from it, pure
actions, deviation without response, strict domination (every member of the coalition strictly gains). Static only: no
dynamics, no π. A finite catalogue can only under-count deviations, so "strong Nash in the catalogue" is an upper
bound on strong Nash in the language; "not strong Nash" is exact.

Games (actions C = 1, D = 0; payoffs (u1, u2) at (a1, a2)):
- PD: CC (0, 0), CD (−2, 1), DC (1, −2), DD (−1, −1). α-core = β-core = {CC}.
- MP, pure matching pennies: player 1 gets +1 on a match, −1 otherwise; player 2 the opposite. α-core = all four
  outcomes; β-core = ∅.
- Q: CC (1, 1), CD (0, 2), DC (0, 0), DD (1, 0). α-core = {CC, CD, DD}; β-core = {CC, DD}. CD separates the ends:
  player 1's pure maxmin is 0 and pure minmax is 1.
- Majority division on the ⅓ grid (`src/dollar3.py` action set): α-core = ∅.

Run before these predictions: only the catalogue sizes above and evaluation timing.

## Predictions (the RE's)

1. PD: the set of strong Nash outcomes in the catalogue is {CC} at every n. Falsifier: any other outcome, or none.
2. MP: no strong Nash profile at any n. Falsifier: one exists.
3. Q: the set of strong Nash outcomes is {CC, DD}, the β-core, at every n; CD never. Falsifier: CD strong Nash at
   some n, or CC or DD missing.
4. Who reads whom. No program matches every opponent's actual action and none mismatches every opponent's (no
   universal mirror or anti-mirror: axiom T fails), at every n. Against at least 0.99 of the catalogue's prior mass
   at n ≥ 7, some deviator matches and some deviator mismatches the resident's actual action (axiom R holds on that
   mass). Falsifiers: a universal mirror or anti-mirror exists; or the mass is below 0.99.
5. Exposure. Programs that are never exploited (no opponent gets D against their C) exist at every n and include
   FairBot `BOX(THEM(ME))`. Falsifier: FairBot exploited by a catalogue program.
6. Majority division: every outcome of the grid game is α-blocked by a pair playing constants (so by P6 no program
   game over it has a strong Nash profile). Falsifier: an unblocked outcome.

Exploratory, no prediction: the same with PA-level boxes only.
