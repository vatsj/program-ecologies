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

## Result (`src/case3_static.py`, `runs/case3-static.json`; seconds of CPU)

All six predictions hold, at every n = 5–9, with both proof levels and with PA-level boxes only.

| game | α-core | β-core | strong Nash outcomes in the catalogue (profiles at n = 5 / 7 / 9) |
|---|---|---|---|
| PD | CC | CC | CC only (9 / 121 / 637) |
| MP (pure) | all four | none | none |
| Q | CC, CD, DD | CC, DD | CC (26 / 613 / 13,055) and DD (17 / 1,943 / 37,037); CD never |
| majority division | none | none | all 729 action profiles α-blocked by a pair of constants |

Who reads whom:
- No program matches, and none mismatches, every opponent's actual action (axiom T fails).
- Against every resident in the catalogue (mass 1.0, every n) some deviator matches its actual action and some
  deviator mismatches it (axiom R holds on the catalogue).
- The best mirrors match the actual action of 0.994–0.997 of prior mass (`BOX1(THEM(ME))`; from n = 8
  `and(BOX1(THEM(ME)), not(BOXD(THEM(ME))))`); the best anti-mirrors mismatch 0.992–0.994 (`not(BOX1(THEM(ME)))`).
  The exceptions are what decide the static question.
- Never-exploited cooperators exist at every n (3 → 61 classes, about 0.010–0.015 of prior mass) and include FairBot.

## Reading

The provability arm sits at the β end: with sound but incomplete reading, a deviator can always be unreadable and
can always read the resident, so punishments cannot be tailored and the deviator replies last. Strong Nash in
program space is then the β-core in the three two-player games tested. Nothing here tests three or more players
beyond the theorem that an empty α-core leaves nothing (majority division), and nothing tests coins. A finite
catalogue under-counts deviations, so the positive findings (CC in the PD; CC and DD in Q) are upper bounds on the
language; for the PD and Q they are backed by soundness (a FairBot-type resident cannot be exploited by any program).
