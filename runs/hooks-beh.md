# Behavioural hooks: verdicts (run 2026-10-21)

Spec `specs/2026-10-21-behavioural-hooks.md`; predictions `predictions/2026-10-21-behavioural-hooks.md` (with the addendum of the gate); notes `notes/hooks-beh.md`. All numbers are finite-(N, I, horizon) lottery statistics at eps = 0 over runs paired by index, not pi. Universal-open = every island efficient (P(C,C) >= 0.95) and every pair of island-majority types cooperating as strangers; Wilson 95% intervals in brackets.

## Cells

| cell | runs | universal-open | efficient islands | P(C,C) | lineage-closed | wall s/run | overflow |
|---|---|---|---|---|---|---|---|
| open-max | 40 | 37/40 = 0.925 (0.801, 0.974) | 0.995 | 0.999 | 0.000 | 5 | 0 |
| inert | 40 | 11/40 = 0.275 (0.161, 0.428) | 0.275 | 0.275 | 0.000 | 2 | 0 |
| beh-max | 30 | 21/30 = 0.700 (0.521, 0.833) | 0.802 | 0.936 | 0.000 | 541 | 0 |
| beh-max-noA | 20 | 2/20 = 0.100 (0.028, 0.301) | 0.163 | 0.460 | 0.000 | 308 | 0 |
| beh-max-hostile | 20 | 16/20 = 0.800 (0.584, 0.919) | 0.834 | 0.915 | 0.000 | 486 | 0 |
| beh-written-only | 20 | 18/20 = 0.900 (0.699, 0.972) | 0.966 | 0.994 | 0.000 | 517 | 0 |
| ff-beh-max | 6 | 5/6 = 0.833 (0.436, 0.97) | 0.833 | 0.970 | 0.000 | 3125 | 0 |
| beh-max-N200 | 10 | 6/10 = 0.600 (0.313, 0.832) | 0.738 | 0.880 | 0.000 | 1027 | 0 |
| M-open-max | 40 | 38/40 = 0.950 (0.835, 0.986) | 0.997 | 0.999 | 0.000 | 5 | 0 |
| M-thanks-only | 40 | 40/40 = 1.000 (0.912, 1.0) | 1.000 | 1.000 | 0.000 | 4 | 0 |
| M-grudge-only | 40 | 23/40 = 0.575 (0.422, 0.715) | 0.959 | 0.994 | 0.000 | 3 | 0 |
| M3a-thanks-noinherit | 40 | 8/40 = 0.200 (0.105, 0.348) | 0.200 | 0.209 | 0.000 | 1 | 0 |
| M3b-thanks-nocopy | 40 | 22/40 = 0.550 (0.398, 0.693) | 0.550 | 0.550 | 0.000 | 1 | 0 |
| M3c-thanks-neither | 40 | 18/40 = 0.450 (0.307, 0.602) | 0.450 | 0.450 | 0.000 | 2 | 0 |
| M3d-thanks-noevict | 40 | 40/40 = 1.000 (0.912, 1.0) | 1.000 | 1.000 | 0.000 | 3 | 0 |
| M3e-thanks-single | 40 | 39/40 = 0.975 (0.871, 0.996) | 0.994 | 0.999 | 0.000 | 4 | 0 |
| M3a-max-noinherit | 40 | 12/40 = 0.300 (0.181, 0.454) | 0.300 | 0.627 | 0.000 | 3 | 0 |
| M3b-max-nocopy | 40 | 40/40 = 1.000 (0.912, 1.0) | 1.000 | 1.000 | 0.000 | 2 | 0 |
| M3c-max-neither | 40 | 21/40 = 0.525 (0.375, 0.671) | 0.525 | 0.738 | 0.000 | 3 | 0 |
| M3d-max-noevict | 40 | 37/40 = 0.925 (0.801, 0.974) | 0.992 | 0.998 | 0.000 | 3 | 0 |
| M3e-max-single | 40 | 39/40 = 0.975 (0.871, 0.996) | 0.998 | 0.999 | 0.000 | 4 | 0 |
| M4-early | 40 | 10/40 = 0.250 (0.142, 0.402) | 0.830 | 0.959 | 0.000 | 3 | 0 |
| M4-late | 40 | 32/40 = 0.800 (0.652, 0.895) | 0.984 | 0.998 | 0.000 | 4 | 0 |
| M5-sham | 20 | 3/20 = 0.150 (0.052, 0.36) | 0.556 | 0.811 | 0.000 | 390 | 0 |


## Prediction verdicts

1. *Statics.* Held, with the PrudentBot reading fixed by the RE (d-clause under box1): FairBot defects against TrustingBot, the Godel predator cooperates with itself and is suckered by FairBot, PrudentBot exploits TrustingBot and CooperateBot and cooperates with FairBot; the solver (vacuous box at world 0) and an independent reference agree on all 49 entries (`tools/beh_gate.py`). With the level-PA reading PrudentBot defects with FairBot (gate failed, addendum to the predictions).

2. **PARTIAL.** beh-max universal-open >= 0.75 [< 0.5]. 21/30 = 0.700; same-geometry references: open-max 37/40 = 0.925 (0.801, 0.974), inert-hooks 11/40 = 0.275 (0.161, 0.428)

3. **FAILED.** FairBot/PrudentBot-equivalent through a fill on winning islands at the end >= 50% [< 30%]. 0.003 through a fill (0.044 counting unhooked FairBot-equivalents)

4. **PARTIAL.** hostile keys founded on >= 90% of islands and held by < 5% at the end under both priors [>= 20% under the hostile prior]. beh-max: founded 0.375 of islands, held at end 0.0018 (winning islands 0.0002); beh-max-hostile: founded 0.928 of islands, held at end 0.0105 (winning islands 0.0003)

5. **FAILED.** PrudentBot-equivalents outnumber FairBot-equivalents on winning islands at generation 200, with TrustingBots and CooperateBots still present [fewer]. winning-island individuals at 200 (summed over runs, 383 islands): FairBot-eq 1876, PrudentBot-eq 0, CooperateBot-like 13884, TrustingBot-like 1; the counter-prediction (FairBot-eq > PrudentBot-eq) held; production events into FairBot-eq 230581, PrudentBot-eq 498; births with a FairBot-eq child 575287, PrudentBot-eq child 574 (births are the reproductive output; class shares by generation are in M1)

6. **HELD.** beh-max-noA <= 0.70 universal-open [>= 0.85]. 2/20 = 0.100 (inert-hooks control at this geometry 11/40 = 0.275 (0.161, 0.428); beh-max 21/30 = 0.700 (0.521, 0.833))

7. **PARTIAL.** ff-beh-max >= 0.9 [< 0.7]. 5/6 = 0.833 (a cell cut at 6 of 10 planned runs for cost; the stored legacy ff-open-max at the stored geometry was 20/20)

8. **FAILED.** contagion (H1): copying is the carrier; inheritance, eviction and multi-hook programs are not. copy-ancestry share of FairBot-equivalents carrying a thanks fill at 200: 0.020; M3a-thanks-noinherit 8/40 = 0.200 (0.105, 0.348) (needs >= 0.85); M3b-thanks-nocopy 22/40 = 0.550 (0.398, 0.693) (needs <= 0.70); M3c-thanks-neither 18/40 = 0.450 (0.307, 0.602) (needs <= 0.70); M3d-thanks-noevict 40/40 = 1.000 (0.912, 1.0), difference to M-thanks-only +0.000 (needs within 0.1; falsified by a fall of more than 0.2); M3e-thanks-single 39/40 = 0.975 (0.871, 0.996), difference to M-thanks-only -0.025 (needs within 0.1; falsified by a fall of more than 0.2); stated falsifier (copy share below 25% or M3b >= 0.9) TRIPPED; clauses held: M3b, M3c, M3d, M3e

9. **FAILED.** grudge writes convert CooperateBot-like carriers (suckers); DefectBot-like majorities hold the failed islands [failed islands have no DefectBot-like majority]. from-class of class-changing grudge writes: CooperateBot-like 0.919, predator-like 0.008, other 0.072; failed-island majority class DefectBot-like on 0.000 of 26 failed island-records (universal-open 23/40 = 0.575 (0.422, 0.715)); first clause (converted carriers are CooperateBot-like): held; DefectBot-like share on failed islands 0.046 against 0.001 on efficient ones

10. **FAILED.** writes in generations 0-50 alone recover >= 80% of open-max universal-open [< 50%]. M4-early 10/40 = 0.250 (0.142, 0.402) vs M-open-max 38/40 = 0.950 (0.835, 0.986) (ratio 0.263); M4-late 32/40 = 0.800 (0.652, 0.895)

11. **HELD.** sham writes (unconditioned, matched keys) <= 0.70 universal-open [>= 0.85]. 3/20 = 0.150 (beh-max 21/30 = 0.700 (0.521, 0.833))


## Mechanism summary: ablations against their paired reference (universal-open share; difference = reference minus ablation is shown as ablation minus reference)

| cell | universal-open | difference to the reference (paired by run) | efficient islands |
|---|---|---|---|
| **M-thanks-only** (reference) | 40/40 = 1.000 (0.912, 1.0) |  | 1.000 |
| M3a-thanks-noinherit | 8/40 = 0.200 (0.105, 0.348) | -0.800 | 0.200 |
| M3b-thanks-nocopy | 22/40 = 0.550 (0.398, 0.693) | -0.450 | 0.550 |
| M3c-thanks-neither | 18/40 = 0.450 (0.307, 0.602) | -0.550 | 0.450 |
| M3d-thanks-noevict | 40/40 = 1.000 (0.912, 1.0) | +0.000 | 1.000 |
| M3e-thanks-single | 39/40 = 0.975 (0.871, 0.996) | -0.025 | 0.994 |
| **M-open-max** (reference) | 38/40 = 0.950 (0.835, 0.986) |  | 0.997 |
| M3a-max-noinherit | 12/40 = 0.300 (0.181, 0.454) | -0.650 | 0.300 |
| M3b-max-nocopy | 40/40 = 1.000 (0.912, 1.0) | +0.050 | 1.000 |
| M3c-max-neither | 21/40 = 0.525 (0.375, 0.671) | -0.425 | 0.525 |
| M3d-max-noevict | 37/40 = 0.925 (0.801, 0.974) | -0.025 | 0.992 |
| M3e-max-single | 39/40 = 0.975 (0.871, 0.996) | +0.025 | 0.998 |
| M4-early | 10/40 = 0.250 (0.142, 0.402) | -0.700 | 0.830 |
| M4-late | 32/40 = 0.800 (0.652, 0.895) | -0.150 | 0.984 |
| **beh-max** (reference) | 21/30 = 0.700 (0.521, 0.833) |  | 0.802 |
| M5-sham | 3/20 = 0.150 (0.052, 0.36) | -0.550 | 0.556 |
| beh-max-noA | 2/20 = 0.100 (0.028, 0.301) | -0.600 | 0.163 |
| beh-max-hostile | 16/20 = 0.800 (0.584, 0.919) | +0.100 | 0.834 |
| **inert** (reference) | 11/40 = 0.275 (0.161, 0.428) |  | 0.275 |
| open-max | 37/40 = 0.925 (0.801, 0.974) | +0.650 | 0.995 |
| M-open-max | 38/40 = 0.950 (0.835, 0.986) | +0.675 | 0.997 |
| M-thanks-only | 40/40 = 1.000 (0.912, 1.0) | +0.725 | 1.000 |
| M-grudge-only | 23/40 = 0.575 (0.422, 0.715) | +0.300 | 0.959 |
| beh-max | 21/30 = 0.700 (0.521, 0.833) | +0.400 | 0.802 |
| beh-written-only | 18/20 = 0.900 (0.699, 0.972) | +0.650 | 0.966 |


## M1: response classes against the fixed panel (share of individuals, run-averaged)


### beh-max (21/30 = 0.700 (0.521, 0.833))

| gen | FairBot | PrudentBot | CooperateBot-like | DefectBot-like | TrustingBot-like | predator-like | other | ambiguous |
|---|---|---|---|---|---|---|---|---|
| 0 | 0.007 | 0.000 | 0.455 | 0.457 | 0.002 | 0.010 | 0.067 | 0.002 |
| 10 | 0.024 | 0.000 | 0.159 | 0.300 | 0.005 | 0.006 | 0.497 | 0.009 |
| 20 | 0.024 | 0.000 | 0.162 | 0.266 | 0.005 | 0.004 | 0.530 | 0.009 |
| 50 | 0.027 | 0.000 | 0.253 | 0.123 | 0.003 | 0.002 | 0.580 | 0.011 |
| 100 | 0.036 | 0.000 | 0.300 | 0.043 | 0.001 | 0.001 | 0.605 | 0.015 |
| 200 | 0.049 | 0.000 | 0.329 | 0.011 | 0.000 | 0.001 | 0.593 | 0.017 |
| 500 | 0.054 | 0.000 | 0.292 | 0.010 | 0.001 | 0.001 | 0.617 | 0.027 |


Deciding origin of the response at generation 200 (individuals summed over runs; the last column counts fills with a copy in their ancestry):

| class | total | none | seeded | thanks | grudge | contract | several | copied-untracked | copied |
|---|---|---|---|---|---|---|---|---|---|
| FairBot | 2373 | 1872 | 0 | 291 | 48 | 121 | 41 | 0 | 8 |
| CooperateBot-like | 15781 | 11817 | 0 | 3759 | 3 | 86 | 116 | 0 | 43 |
| DefectBot-like | 540 | 464 | 0 | 17 | 59 | 0 | 0 | 0 | 12 |
| TrustingBot-like | 22 | 0 | 0 | 2 | 20 | 0 | 0 | 0 | 3 |
| predator-like | 29 | 0 | 0 | 9 | 15 | 5 | 0 | 0 | 1 |
| other | 28447 | 1163 | 0 | 15381 | 1163 | 755 | 9985 | 0 | 282 |
| ambiguous | 808 | 642 | 0 | 124 | 23 | 11 | 8 | 0 | 3 |


### M-open-max (38/40 = 0.950 (0.835, 0.986))

| gen | FairBot | PrudentBot | CooperateBot-like | DefectBot-like | TrustingBot-like | predator-like | other | ambiguous |
|---|---|---|---|---|---|---|---|---|
| 0 | 0.007 | 0.000 | 0.482 | 0.478 | 0.001 | 0.005 | 0.026 | 0.001 |
| 10 | 0.720 | 0.000 | 0.107 | 0.160 | 0.000 | 0.005 | 0.007 | 0.001 |
| 20 | 0.830 | 0.000 | 0.093 | 0.068 | 0.000 | 0.001 | 0.007 | 0.001 |
| 50 | 0.859 | 0.000 | 0.117 | 0.018 | 0.000 | 0.000 | 0.006 | 0.001 |
| 100 | 0.846 | 0.000 | 0.145 | 0.002 | 0.000 | 0.000 | 0.007 | 0.000 |
| 200 | 0.807 | 0.000 | 0.190 | 0.001 | 0.000 | 0.000 | 0.002 | 0.000 |
| 500 | 0.760 | 0.000 | 0.239 | 0.001 | 0.000 | 0.000 | 0.000 | 0.000 |


Deciding origin of the response at generation 200 (individuals summed over runs; the last column counts fills with a copy in their ancestry):

| class | total | none | seeded | thanks | grudge | contract | several | copied-untracked | copied |
|---|---|---|---|---|---|---|---|---|---|
| FairBot | 51660 | 137 | 501 | 33100 | 16264 | 106 | 1463 | 89 | 17392 |
| CooperateBot-like | 12162 | 8408 | 40 | 925 | 6 | 1 | 585 | 2197 | 2264 |
| DefectBot-like | 44 | 27 | 14 | 0 | 3 | 0 | 0 | 0 | 14 |
| predator-like | 9 | 0 | 9 | 0 | 0 | 0 | 0 | 0 | 9 |
| other | 125 | 56 | 43 | 0 | 6 | 0 | 20 | 0 | 43 |


### M-thanks-only (40/40 = 1.000 (0.912, 1.0))

| gen | FairBot | PrudentBot | CooperateBot-like | DefectBot-like | TrustingBot-like | predator-like | other | ambiguous |
|---|---|---|---|---|---|---|---|---|
| 0 | 0.007 | 0.000 | 0.482 | 0.478 | 0.001 | 0.005 | 0.026 | 0.001 |
| 10 | 0.051 | 0.000 | 0.058 | 0.864 | 0.000 | 0.009 | 0.017 | 0.000 |
| 20 | 0.118 | 0.000 | 0.012 | 0.845 | 0.001 | 0.003 | 0.021 | 0.001 |
| 50 | 0.361 | 0.000 | 0.012 | 0.605 | 0.000 | 0.001 | 0.020 | 0.002 |
| 100 | 0.750 | 0.000 | 0.024 | 0.212 | 0.000 | 0.001 | 0.011 | 0.002 |
| 200 | 0.904 | 0.000 | 0.073 | 0.013 | 0.000 | 0.000 | 0.005 | 0.004 |
| 500 | 0.897 | 0.000 | 0.099 | 0.000 | 0.000 | 0.000 | 0.002 | 0.003 |


Deciding origin of the response at generation 200 (individuals summed over runs; the last column counts fills with a copy in their ancestry):

| class | total | none | seeded | thanks | grudge | contract | several | copied-untracked | copied |
|---|---|---|---|---|---|---|---|---|---|
| FairBot | 57872 | 2358 | 1640 | 52623 | 0 | 0 | 867 | 384 | 3183 |
| CooperateBot-like | 4663 | 1136 | 0 | 993 | 0 | 0 | 34 | 2500 | 2640 |
| DefectBot-like | 857 | 461 | 0 | 15 | 0 | 0 | 70 | 311 | 326 |
| predator-like | 9 | 0 | 0 | 9 | 0 | 0 | 0 | 0 | 5 |
| other | 327 | 166 | 148 | 1 | 0 | 0 | 0 | 12 | 160 |
| ambiguous | 272 | 272 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |


### M-grudge-only (23/40 = 0.575 (0.422, 0.715))

| gen | FairBot | PrudentBot | CooperateBot-like | DefectBot-like | TrustingBot-like | predator-like | other | ambiguous |
|---|---|---|---|---|---|---|---|---|
| 0 | 0.007 | 0.000 | 0.482 | 0.478 | 0.001 | 0.005 | 0.026 | 0.001 |
| 10 | 0.317 | 0.000 | 0.069 | 0.587 | 0.000 | 0.006 | 0.020 | 0.002 |
| 20 | 0.487 | 0.000 | 0.030 | 0.453 | 0.000 | 0.002 | 0.026 | 0.002 |
| 50 | 0.735 | 0.000 | 0.033 | 0.184 | 0.000 | 0.001 | 0.045 | 0.003 |
| 100 | 0.845 | 0.000 | 0.062 | 0.025 | 0.000 | 0.000 | 0.065 | 0.003 |
| 200 | 0.787 | 0.000 | 0.135 | 0.005 | 0.000 | 0.000 | 0.068 | 0.005 |
| 500 | 0.665 | 0.000 | 0.221 | 0.002 | 0.000 | 0.000 | 0.100 | 0.011 |


Deciding origin of the response at generation 200 (individuals summed over runs; the last column counts fills with a copy in their ancestry):

| class | total | none | seeded | thanks | grudge | contract | several | copied-untracked | copied |
|---|---|---|---|---|---|---|---|---|---|
| FairBot | 50364 | 1348 | 581 | 0 | 42499 | 0 | 1208 | 4728 | 47340 |
| CooperateBot-like | 8639 | 7209 | 293 | 0 | 0 | 0 | 723 | 414 | 707 |
| DefectBot-like | 313 | 257 | 0 | 0 | 7 | 0 | 0 | 49 | 49 |
| other | 4365 | 1612 | 1397 | 0 | 1234 | 0 | 0 | 122 | 2695 |
| ambiguous | 319 | 319 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |


## M2: conversions (class-changing events, summed over runs; evicted = the write evicted a fill; multi = several hook nodes with one tag)


### beh-max

| event | class changes | of which evicting | of which multi-hook programs | largest conversions |
|---|---|---|---|---|
| write-thanks | 2187340 | 2126172 | 12789 | other->CooperateBot-like 959144; CooperateBot-like->other 714127; FairBot->other 179190; other->FairBot 118786; ambiguous->other 50512 |
| write-grudge | 515582 | 447356 | 787 | CooperateBot-like->other 249346; other->DefectBot-like 93778; CooperateBot-like->TrustingBot-like 37237; CooperateBot-like->FairBot 22089; other->FairBot 12539 |
| copy | 70257 | 58265 | 387 | DefectBot-like->other 17762; other->CooperateBot-like 15471; other->DefectBot-like 9593; CooperateBot-like->other 8387; other->FairBot 4705 |
| contract | 292256 | 0 | 1712 | DefectBot-like->other 118476; other->CooperateBot-like 66190; other->FairBot 32478; DefectBot-like->FairBot 28247; FairBot->other 16810 |


Births (victim class -> child class), child-class totals: FairBot 575287, PrudentBot 574, CooperateBot-like 6934905, DefectBot-like 849788, TrustingBot-like 24062, predator-like 26934, other 13723062, ambiguous 167883


### M-open-max

| event | class changes | of which evicting | of which multi-hook programs | largest conversions |
|---|---|---|---|---|
| write-thanks | 33403 | 335 | 33 | other->FairBot 27971; CooperateBot-like->predator-like 3698; predator-like->DefectBot-like 1246; FairBot->DefectBot-like 139; other->CooperateBot-like 101 |
| write-grudge | 21380 | 5242 | 36 | CooperateBot-like->FairBot 17506; predator-like->DefectBot-like 2095; CooperateBot-like->other 991; other->DefectBot-like 530; other->predator-like 220 |
| copy | 238386 | 129891 | 141 | FairBot->CooperateBot-like 83666; CooperateBot-like->FairBot 67016; FairBot->DefectBot-like 43762; FairBot->other 39593; FairBot->predator-like 1084 |
| contract | 69966 | 0 | 57 | DefectBot-like->FairBot 58466; other->FairBot 11173; other->CooperateBot-like 297; DefectBot-like->CooperateBot-like 22; DefectBot-like->other 4 |


Births (victim class -> child class), child-class totals: FairBot 21564952, PrudentBot 13, CooperateBot-like 4523681, DefectBot-like 273711, TrustingBot-like 89, predator-like 11774, other 72345, ambiguous 4121


### M-thanks-only

| event | class changes | of which evicting | of which multi-hook programs | largest conversions |
|---|---|---|---|---|
| write-thanks | 76802 | 1706 | 59 | other->FairBot 68369; CooperateBot-like->predator-like 4380; predator-like->DefectBot-like 2008; other->DefectBot-like 814; FairBot->DefectBot-like 408 |
| write-grudge | 0 | 0 | 0 |  |
| copy | 176687 | 88167 | 456 | FairBot->other 71466; FairBot->CooperateBot-like 43705; CooperateBot-like->FairBot 33147; DefectBot-like->FairBot 10382; DefectBot-like->CooperateBot-like 5998 |
| contract | 0 | 0 | 0 |  |


Births (victim class -> child class), child-class totals: FairBot 20666517, PrudentBot 0, CooperateBot-like 1992152, DefectBot-like 3009391, TrustingBot-like 1118, predator-like 21799, other 154669, ambiguous 33150


### M-grudge-only

| event | class changes | of which evicting | of which multi-hook programs | largest conversions |
|---|---|---|---|---|
| write-thanks | 0 | 0 | 0 |  |
| write-grudge | 39858 | 17170 | 138 | CooperateBot-like->FairBot 32689; other->DefectBot-like 2655; CooperateBot-like->DefectBot-like 2007; CooperateBot-like->other 1924; predator-like->DefectBot-like 309 |
| copy | 288694 | 221453 | 537 | FairBot->CooperateBot-like 127977; CooperateBot-like->FairBot 89615; FairBot->DefectBot-like 21344; FairBot->other 12672; other->CooperateBot-like 7788 |
| contract | 0 | 0 | 0 |  |


Births (victim class -> child class), child-class totals: FairBot 20063149, PrudentBot 0, CooperateBot-like 4183066, DefectBot-like 1298866, TrustingBot-like 82, predator-like 7047, other 1394640, ambiguous 74063


## M6: stranger compatibility of winning-island majorities at the end

| cell | cooperate with the panel FairBot stranger | cooperate with an own stranger copy | rival-network islands |
|---|---|---|---|
| open-max | 1.000 | 1.000 | 0.000 |
| inert | 1.000 | 1.000 | 0.000 |
| beh-max | 1.000 | 1.000 | 0.000 |
| beh-max-noA | 1.000 | 1.000 | 0.000 |
| beh-max-hostile | 1.000 | 1.000 | 0.000 |
| beh-written-only | 1.000 | 1.000 | 0.000 |
| ff-beh-max | 1.000 | 1.000 | 0.000 |
| beh-max-N200 | 1.000 | 1.000 | 0.000 |
| M-open-max | 1.000 | 1.000 | 0.000 |
| M-thanks-only | 1.000 | 1.000 | 0.000 |
| M-grudge-only | 1.000 | 1.000 | 0.000 |
| M3a-thanks-noinherit | 1.000 | 1.000 | 0.000 |
| M3b-thanks-nocopy | 1.000 | 1.000 | 0.000 |
| M3c-thanks-neither | 1.000 | 1.000 | 0.000 |
| M3d-thanks-noevict | 1.000 | 1.000 | 0.000 |
| M3e-thanks-single | 1.000 | 1.000 | 0.000 |
| M3a-max-noinherit | 1.000 | 1.000 | 0.000 |
| M3b-max-nocopy | 1.000 | 1.000 | 0.000 |
| M3c-max-neither | 1.000 | 1.000 | 0.000 |
| M3d-max-noevict | 1.000 | 1.000 | 0.000 |
| M3e-max-single | 1.000 | 1.000 | 0.000 |
| M4-early | 1.000 | 1.000 | 0.000 |
| M4-late | 1.000 | 1.000 | 0.000 |
| M5-sham | 1.000 | 1.000 | 0.000 |


## Event counters (mean per run)

| cell | encounters | thanks writes | grudge writes | copies | contracts | evictions | behavioural writes | rejected (no-evict) | no true key | outside window |
|---|---|---|---|---|---|---|---|---|---|---|
| open-max | 800000 | 1459231 | 1197 | 102024 | 1274 | 13636 | 1460429 | 0 | 0 | 0 |
| inert | 800000 | 1687 | 3738 | 48120 | 17115 | 30473 | 0 | 0 | 0 | 0 |
| beh-max | 800000 | 1282376 | 30624 | 17842 | 13392 | 748452 | 1313000 | 0 | 0 | 0 |
| beh-max-noA | 800000 | 515206 | 162946 | 44602 | 71260 | 431491 | 678153 | 0 | 0 | 0 |
| beh-max-hostile | 800000 | 1331758 | 29952 | 17562 | 12152 | 763395 | 1361710 | 0 | 0 | 0 |
| beh-written-only | 800000 | 1439919 | 14258 | 16151 | 6121 | 807979 | 1454177 | 0 | 0 | 0 |
| ff-beh-max | 640000 | 1102970 | 23678 | 13297 | 9593 | 630400 | 1126648 | 0 | 0 | 0 |
| beh-max-N200 | 960000 | 1403139 | 49916 | 23309 | 23787 | 848652 | 1453056 | 0 | 0 | 0 |
| M-open-max | 800000 | 1469342 | 1257 | 102061 | 1651 | 13620 | 1470600 | 0 | 0 | 0 |
| M-thanks-only | 800000 | 1302877 | 0 | 103974 | 0 | 13344 | 1302877 | 0 | 0 | 0 |
| M-grudge-only | 800000 | 0 | 2538 | 86834 | 0 | 17541 | 2538 | 0 | 0 | 0 |
| M3a-thanks-noinherit | 800000 | 19767 | 0 | 4402 | 0 | 17 | 19767 | 0 | 0 | 0 |
| M3b-thanks-nocopy | 800000 | 338594 | 0 | 0 | 0 | 11 | 338594 | 0 | 0 | 0 |
| M3c-thanks-neither | 800000 | 259823 | 0 | 0 | 0 | 9 | 259823 | 0 | 0 | 0 |
| M3d-thanks-noevict | 800000 | 1266330 | 0 | 94223 | 0 | 0 | 1290472 | 33088 | 0 | 0 |
| M3e-thanks-single | 800000 | 1277857 | 0 | 100170 | 0 | 13606 | 1277857 | 0 | 0 | 0 |
| M3a-max-noinherit | 800000 | 559226 | 19946 | 19876 | 267582 | 110 | 579173 | 0 | 0 | 0 |
| M3b-max-nocopy | 800000 | 1383595 | 962 | 0 | 353 | 62 | 1384558 | 0 | 0 | 0 |
| M3c-max-neither | 800000 | 686147 | 8480 | 0 | 221070 | 62 | 694628 | 0 | 0 | 0 |
| M3d-max-noevict | 800000 | 1481444 | 1129 | 95306 | 1418 | 0 | 1486758 | 13862 | 0 | 0 |
| M3e-max-single | 800000 | 1423733 | 1170 | 98483 | 1124 | 12885 | 1424903 | 0 | 0 | 0 |
| M4-early | 800000 | 124849 | 1097 | 91529 | 423 | 17695 | 125947 | 0 | 0 | 1347760 |
| M4-late | 800000 | 1333144 | 323 | 98837 | 1916 | 13808 | 1333468 | 0 | 0 | 48254 |
| M5-sham | 800000 | 882873 | 74744 | 21404 | 27863 | 651213 | 957618 | 0 | 0 | 0 |


## Counter-predictions and disputes

- **Prediction 5, counter (gemini-4-argon, gpt-6.1-sol): FairBot-equivalents outnumber PrudentBot-equivalents. HELD**, by a wide margin: on winning islands at generation 200 FairBot-eq 1,876, PrudentBot-eq 0; production events into the two classes 230,581 against 498; births with a FairBot-eq child 575,287 against 574. The prior explains it: the two prudent key classes carry 1e-4 of the family's mass against 0.26 for the FairBot-signature keys, and no run grew the prudent class.
- **Prediction 1, disputed static (gemini-4-argon against the RE): the solver sides with the RE's reading** (box vacuously true at world 0): FairBot defects and the Godel predator cooperates, i.e. FairBot exploits the predator; the independent reference agrees on all 49 entries. The statics all hold with PrudentBot read with box1 on d; at level PA the PrudentBot entry fails (mutual defection) and no one-fill program is prudent (addendum to the predictions).
- **Prediction 7** is neither held nor failed: 5/6 = 0.833 sits between the thresholds, on 6 of the 10 planned runs (cut for cost); the one failing run had no efficient island.
- **Prediction 2** is neither held nor failed: 0.700 on 30 runs sits between 0.5 and 0.75. Same-geometry references: the inert-hooks control 11/40 = 0.275, legacy open-max 37/40 = 0.925. The family recovers most of the gap from inert to legacy, not all of it.
- **Secondary N = 200** (10 runs, (200, 8), horizon 600): beh-max 6/10 = 0.600, efficient islands 0.738; not scored against a prediction; at N = 100 the same family gave 0.70 (30 runs, 16 islands), so no sign of a rise with island size at this scale.
- **Scoring conventions.** Prediction 8 is scored by its stated falsifier (copy-ancestry share below 25 percent, or M3b >= 0.9): tripped, hence failed, although its sub-clauses on copying removal (M3b, M3c), eviction (M3d) and multi-hook programs (M3e) held. Prediction 9 is scored by its stated falsifier (a DefectBot-like majority on failed islands): tripped, hence failed; its first clause held (92 percent of class-changing grudge writes come from CooperateBot-like carriers), and failed islands do carry a DefectBot-like fringe (0.046 against 0.001 on efficient islands). Prediction 4 is partial: the held-at-end clause holds under both priors (0.0018 and 0.0105), the founding clause fails under the length prior (hostile constructions are founded on 0.375 of islands, 0.928 under the x10 prior).

## The mechanism of open writes, as far as M1-M6 identify it (plain language)

A program that has just cooperated writes a rule into its own four-slot list: "cooperate with partners like the one I just met", where "like" is a behavioural predicate of the partner (in the legacy cells, the single predicate that the partner provably cooperates with me). The rule is written only about a partner who really was cooperative (thanks) or defective (grudge), and that conditioning is necessary: replacing the conditioned key by a size- and applicability-matched random key drops universal-open from 0.70 to 0.15. A thanks rule on a default-defecting hook turns the writer into a FairBot-like cooperator; a grudge rule on a default-cooperating hook turns a sucker into one (92 percent of grudge conversions start from CooperateBot-like carriers). The rule is then **inherited**: with written fills stripped at birth universal-open falls to 0.20 (thanks-only) and 0.30 (open-max), and with copying also off to 0.45 and 0.525 (within-lifetime writes alone), against 1.00 and 0.95 with everything on. So the carrier is the writing individual's own lineage (H2, inheritance), with selection favouring the converted cooperators on islands where cooperation pays. **Verbatim copying (H1) is not the carrier:** removing it leaves 0.55 (thanks-only) and 1.00 (open-max), and only 2 percent of FairBot-equivalents in thanks-only carry a copied thanks fill; copying matters for grudges (94 percent of FairBot-equivalents in grudge-only carry a copied grudge fill), where the writers are rare suckers. Eviction (H3: no-eviction 1.00 and 0.925) and multi-hook programs (H4: single-hook prior 0.975 and 0.975) are not the mechanism. Timing: writes during generations 0-50 alone give only 0.25 and writes after generation 50 alone 0.80, so conversion is not confined to the founding scramble; the later writes carry more of the effect. Thanks beat grudges (1.00 against 0.575) because grudges convert suckers and leave a small DefectBot-like fringe (0.046 of failed islands) that blocks the 0.95 threshold, while thanks only ever move default-defectors toward cooperation. In the maximal family the winners are generous provers, not the named FairBot: the dominant response on a winning island (rep 0, generation 200) cooperates with CooperateBot, FairBot, TrustingBot and its own copy and defects with DefectBot, PrudentBot and the predator, and the type lists show four stacked friendly guards (box a, box1 a, box c, box1 c); plain base provers (BOX(THEM(ME)) and relatives) hold the rest. The a-free family (no guard on the partner's play towards me) fails (0.10, below the inert control's 0.275), so expressing the prover's guard is what the recovery needs; the winners are not rival networks (M6: every winning-island majority cooperates with the panel FairBot stranger and with an own stranger copy, rival-island share 0 in every cell).
