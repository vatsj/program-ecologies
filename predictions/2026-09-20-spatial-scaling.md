# Spatial scaling verdict — written 2026-09-21 (file dated per task spec 2026-09-20), before the run

Same death-birth torus process as predictions/2026-09-20-spatial.md (weak
n = 6 with ROLE, PD, w = 0.3, von Neumann k = 4, burn-in 10⁴ generations,
10⁵ sampled, 5 seeds), now at sides {32, 64, 128} for εN = 1 and at side 32
for εN ∈ {0.3, 3}.  Traces of the tracked class shares every 100
generations; collapse events = THEM(^C) share crossing 0.5 downward after
having exceeded 0.8, with the ALLC share recorded 500 generations before the
crossing; duty cycle = fraction of sampled generations with THEM(^C) > 0.5.

**Verdicts:**
1. P(C,C) increases monotonically in side at εN = 1.
   Falsifier: 64² below 32² by more than one sd.
2. The pre-collapse ALLC share is > 0.15 and within a factor of 1.5 across
   sides.
3. P(C,C) versus εN (side 32) is unimodal with its peak between 0.3 and 3.
