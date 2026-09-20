# Standing-variance verdict — written 2026-09-20, before the run

Agent-based Moran process (src/abm.py): N = 100, weak arm n = 6 with ROLE,
PD, f = exp(w·payoff), w = 0.3, mutation per birth at ε with εN ∈ {0.1, 1, 10},
mutants drawn from μ over the behavioural classes of L_6; burn-in 10⁴
generations, 10⁵ sampled, 5 seeds each.  Cooperative share is
(mean payoff − u(D,D)) / (efficient − u(D,D)), i.e. mean payoff + 1 in the PD.

**Verdict:** the cooperative share rises monotonically in εN but stays
< 0.10 at εN = 1 and < 0.25 at εN = 10.  The shadow mechanism (THEORY §3) is
expected to survive standing variance at these mutation rates: the
conditional cooperator `THEM(^C)` is still on-path indistinguishable from
ALLC most of the time, and ALLC still enters at μ(C)/N.

**Falsifier:** cooperative share > 0.25 at εN = 1.
