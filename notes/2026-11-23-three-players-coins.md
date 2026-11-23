# Three players and coalition coins: do the two cores still differ, and which end does sound reading pick? (2026-11-23)

Follows `notes/2026-11-23-case3-static.md` and PROOFS P6–P9. Static only.

## The game G3

Players 1 and 2 choose N, X or Y; player 3 chooses L or R. Payoffs (u1, u2, u3):
- both N: (1, 1, 1) whatever 3 does (the status quo);
- both X: (2, 2, 0) against L, (2, 0, 0) against R;
- both Y: (0, 2, 0) against L, (2, 2, 0) against R;
- anything else: (0, 0, 0).

The pair {1, 2} wants to match player 3 (X with L, Y with R); only the pair can gain on the status quo.

## Predictions (the RE's; nothing has been run)

1. **The gap survives coins for a pair.** In pure actions and also when every coalition has its own coin, the status
   quo is in the α-core and not in the β-core: no joint mixture of the pair beats (1, 1) against both L and R, while
   against every mixture of player 3 some joint mixture of the pair does. Checked on a grid of mixtures. Falsifier:
   a grid point contradicting either half.
2. **The gap closes for single players.** For every player of G3 the maxmin and the minmax value against a correlated
   complement coincide (linear programs). Falsifier: a difference above 10⁻⁶.
3. **The coalition coin is not sugar.** If player 3 mixes ½–½ with a private coin, a pair with private coins only
   (independent mixing) cannot make both members strictly better than (1, 1); a pair with a shared coin can.
   Falsifier: an independent pair of mixtures with both payoffs above 1, or no correlated one.
4. **Sound reading picks the β end with three players too.** In a three-player arm with a free sound box (PA and
   PA + Con(PA), atoms "it is provable that slot j plays x in this encounter", decision trees with at most two
   atoms), every program of player 3 that plays L against two constant N's is matched by some deviating pair with at
   most two atoms each, so the status quo is not strong Nash in pure actions. Falsifier: a player-3 program no such
   pair matches.
5. No deviating pair (≤ 1 atom each) matches every such player-3 program. Falsifier: one does.

## Result (`src/three_coins_static.py`, `runs/three-coins-static.json`; under a minute)

All five predictions hold.

1. The pair's best guaranteed gain over (1, 1) with a shared coin is 0 (no α-block: the status quo itself is the best
   it can guarantee), and against every mixture of player 3 it can gain at least 0.5 (β-block); in pure actions the
   same signs. The status quo is in the α-core and not in the β-core, with or without coalition coins.
2. For each single player maxmin and minmax against a correlated complement are both 0.
3. Against player 3's private ½–½ mix, the best an independently mixing pair can do is a gain of exactly 0 for its
   worse-off member (it cannot make both strictly better); with a shared coin the pair gains 0.5 each. The coalition
   coin changes whether the status quo is blocked.
4. Three-player sound-reading arm: 1,082 programs for player 3, 541 of which play L at the status quo. Every one is
   matched by some deviating pair with one atom each (63 programs per member); the hardest residents are matched by
   162 of the 3,969 pairs. The status quo is not strong Nash in pure actions: the β end again.
5. No one-atom pair matches every resident; the best matches 0.856 of them.

Reading. With three players and no transfers, coalition coins do not close the gap between the two cores for a
pair, sound reading still picks the β end, and the coin a coalition holds decides whether it can block a privately
mixing outsider. Scope: one constructed game; decision trees with at most two atoms; pure actions in the program arm
(the coin results are for the base game).
