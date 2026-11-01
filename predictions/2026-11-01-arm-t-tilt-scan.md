# Predictions: arm T's unequal boundary u* (follow-up check to queue 70), 2026-11-01

Context. "Where the unequal basin comes from" (queue 70) found that arm T's nine constants alone (dose 0) end on unequal
pairs from an unequal tilt of 0.7 or more, while "Arm T under islands to infinity before time" tested only the tilt 0.6.
So arm T's claim "every island on a fair pair from every tested start" holds below some boundary u* that was never located
for the full library. This check locates it with arm T's own code (`src/many_islands_t_ode.py`, `tilt(..., target=u)`),
exact symmetric ODE, pool 0, cells main|0.1|0 (migration charge 0.1, the default) and main|0|0 (charge 0), u in
{0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95}; u* = the smallest scanned u whose endpoint has U >= 0.5. Run by the RE inline.

1. A basin exists in the full library: u* <= 0.95 at both charges (0.6). Falsifier: every scanned u ends with V* >= 0.5.
2. Readers raise the boundary above the constants' (dose 0 boundary between 0.6 and 0.7): u* >= 0.75 at both charges
   (0.6). Falsifier: u* <= 0.7 at either charge.
3. The charge moves u* by at most one scan step (0.05) (0.6). Falsifier: |u*(0.1) - u*(0)| >= 0.1.
