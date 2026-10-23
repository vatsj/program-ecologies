# Grid stable sets (2026-10-22)

Problem: `problems/grid-stable-sets.md` (strict pair-domination on integer allocations of K units; for which K does a
stable set exist, find all, prove for every K). The answer was computed beforehand (exists iff K even, then unique and
symmetric) but unproved, and a Sonnet literature pass found no published statement. 60-minute cap, Daytona 4 vCPU / 8 GB.
Two batches ran at once: the 7 subsets of {opus, sol, argon} (1 replicate) and Sonnet alone vs a Sonnet pair (3 each).

**Every condition solved it.** 13/13 stated the right answer, and the RE read every proof: 12 complete, 1 with a
one-line gap (sonnet-r2 omits the case where a fourth point matches x in its third coordinate; the sum argument closes
it). All 13 found the same proof:
1. two allocations are undominated by each other iff they share a coordinate;
2. so an internally stable set is a "line" (one coordinate fixed) or exactly a "triangle" {v ± d·e_i};
3. a line fails because the allocations one unit above it cannot be dominated (two extra units needed, one available);
4. every triangle except the symmetric one leaves a point that each vertex beats in at most one coordinate.
The cleanest write-ups are `sol-r0/answer.md` and `opus-r0/answer.md`.

| condition | wall time incl. setup (s) | input tokens | output tokens | proof |
|---|---|---|---|---|
| opus | 145 | 145,014 | 11,723 | complete |
| sol | 165 | 123,029 | 9,870 | complete |
| argon | 518 | 616,193 | 22,910 | complete |
| opus+sol | 246 | 751,609 | 21,108 | complete |
| opus+argon | 306 | 390,674 | 16,126 | complete |
| sol+argon | 287 | 606,573 | 14,769 | complete |
| opus+sol+argon | 237 | 1,171,622 | 22,485 | complete |
| sonnet r0 / r1 / r2 | 125 / 105 / 125 | 102,262 / 79,784 / 179,691 | 15,033 / 11,365 / 13,092 | complete / complete / one-line gap |
| sonnet pair r0 / r1 / r2 | 236 / 125 / 135 | 335,470 / 452,019 / 251,465 | 27,742 / 26,907 / 24,580 | complete ×3 |

Sonnet cost: alone $0.16–0.21 per replicate; the pair $0.36–0.61.

**Reading.** This is the third problem that every model solves alone in minutes. Swarms again bought nothing and cost
more, and so did the Sonnet pair. The problem's by-product is a proof of the repo's computed claim (RESULTS
"Stable sets on islands", addendum on odd grids). To separate swarms from solo agents the next problem has to defeat
the solo agents; calibrate it by running one solo agent first.
