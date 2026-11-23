## Do surviving programs best-respond in tiers? A migrant-tier bias shows in arm T and dense arm P, with routes pointing to island persistence and colonization and not to threats being tested; the prior-tier bias does not move with the tail's dose; P10 often gets the direction and mis-sizes fixation once testers are real (2026-11-23; queue 81)

Spec `specs/2026-11-23-tiered-best-response.md` (gemini-4-carbon, then gpt-6.1-sol, both folded). Predictions
`predictions/2026-11-23-tiered-best-response.md` (before stage 0, before stage 2, and stage 3's definition before its run). Run report
`runs/tiered-best-response.md`, verdicts `runs/tiered-best-response.json`, notes `notes/tiered-best-response.md`, data `runs/tbr/`,
`runs/tbr_rows/`. **All population numbers are finite-schedule statistics (I = 64), not π.** About 12.5 local CPU-hours; two Daytona
sandboxes sat idle for about 16 sandbox-CPU-hours through a quoting error and produced nothing.

The RS's statement (OH doc, 2026-11-23): after a long time each program best-responds lexicographically, first to the
island's natives, then to the distribution of migrants, then to the mutation prior. Mechanism: PROOFS P10, the
tiered fixation lemma, under assumption A (testers form a stationary field unaffected by the variant). Arms: T
(27-program L_T library, A_f at 0.1) and M (n ≤ 6 modalPA DSL) of queue 74 at I = 64, seed lottery plus annealed
tail. P: queue "Bridge-less rivals", modal PD at n = 9, N = 200, I = 64, mN = 1.091. Published worlds were
regenerated with saved compositions; every comparable arm T and M run reproduces queue 74's stored V\* series and
migration count exactly (120 of 120 in stage 1, 200 of 200 over all comparable cells; new cells have nothing to check against). Arm P was checked draw for draw with lumping on (35 of 35) and rerun
lump-free (same law), agreeing approximately with the published cells' headlines (dense P\* separated 0.95–1.00 against 0.97, measured here on settled holders and there on network tags).

- **The lemma (stage 0).** Under A by construction, P10 agrees with simulation: 18 of 18 intervals contain the finite-N value
  (RE 1 holds; e.g. 3.072 against 3.066 for the exact event process). Stage 0 uses linear fitness. With real tester lineages, selected-against testers (relative fitness 0.7, 0.9) keep the sign, with scored errors from −27% to +41% (−87% and +124% in unscored variants with feedback). A neutral tester does not: its long-lived lineages establish and truncate replicates, giving a
  wrong sign at N = 100, σ = 0.5 (0.935 [0.811, 1.078], establishments counted as non-fixations) and errors from −64% to +218% (RE 2 falsified on both the size and the sign criterion).
- **A migrant-tier bias exists in arm T and dense arm P, not in M or natural P (RE 3 holds).** RE 3 tests a pooled excess over a seed-law expectation within the catalogue, not three-tier optimality of each program. In program-diverse worlds at mN = 1, settled
  residents with zero native regret are T-weighted best replies to the migrants among their on-path equivalents at
  0.96–1.00 in T against 0.44–0.69 for a seed-law draw from the same equivalence class (excess 0.42), and at 0.47
  against 0.28 in P (dense). In M the excess is 0.02. P's natural start, also in the pool, has none (0.44 against 0.44), so P's pooled excess is 0.18; dense P's residents also have positive native regret in 46% of cases, and no prior tier was measured in P. Pooled excess over arms 0.18 [0.09, 0.30].
- **Much of it looks like supply (RE 4 recorded as holding; the weighting is not reconciled).** In T and M, most residents never met an on-path
  equivalent: the arrival sets are empty in 68–96% of stage-1 cases in T and 24–91% in M. Where equivalents did arrive, they were at zero regret
  as often as residents (excess over the arrival control −0.01 in T, 0.00 in M). The one place the tail supplies
  equivalents (T, Λ = 1,000) also shows a filter (exploratory dose): 0.19 of the arrivals at zero regret against 1.00 of residents
  (33 cases). In P the founder-weighted control removes about a quarter of the excess (0.18 → 0.135). With empty arrival sets dropped the RE 4 pool is 118 T, 263 M and 3,017 P cases, so the evaluable cases are about 89% arm P. The recorded pooled excess is 0.090, under the rule's 0.092; weighting arm excesses by evaluable cases instead gives about 0.12, which would fail it. "Mostly supply" is therefore the reading of the arrival counts, not a scored result. Arm T at mN = 0.1 exceeds its arrival control by 0.24 on 1,825 non-empty cases, a filter beyond supply.
- **Dose (RE 5 holds in T and P).** Arm T's zero-regret share in diverse worlds is 0.69 at mN = 0.1 and 0.96 at
  mN = 1. At mN = 0.1 it rises over the run (0.42 → 0.57 → 0.69) against a control of 0.29–0.33. At mN ≥ 3 worlds
  reach program consensus and almost no cases remain (two at mN = 3, none at 10; descriptive). Arm P (dense): 0.39 at mN = 0.1 against 0.47 at 1.091 (control
  0.27, 0.28); at mN = 3, 0.31 against 0.16, with 0.68 of worlds diverse. Arm M has no diverse world at mN = 1
  (N = 200) and no tier at 0.1.
- **Supply (stage 3; no registered prediction, arm T exploratory).** A Λ = 100 stream of on-path equivalents of the stage-1 holders (in-pair slots) doubles arm
  T's excess (0.76 against 0.38 without), almost entirely by lowering the control (0.58 → 0.24; residents 0.96 → 1.00; all 235 arrival sets empty) and raises program
  diversity (0.40 of worlds against 0.25). In arm M (the registered cell) it creates diverse worlds (4 of 20, none
  without) but no tier (0.973 against 0.971).
- **Outcome consensus is not program consensus (RE 6 falsified).** Arm T's worlds are at fair consensus by outcome
  (queue 74) but 0.25–0.60 stay diverse in programs at mN = 1. Nearly all of that is among on-path equivalents: 6 of
  27 program-diverse worlds differ in outcome (an exploratory comparison). The migrant-tier bias is measured on off-path differences.
- **Routes (RE 9 holds; proxies).** In T and M routes are read from checkpoints and payoff-vector changes, not continuous histories (7.4% / 6.2% unresolved); P uses holder logs. Zero-regret residents held their island from 25% of the horizon (T 0.64, M 0.72, P 1.00)
  or came with a whole profile that took the island over (T 0.28, M 0.21, almost all migrant-borne). Replacement of
  an on-path equivalent with positive regret on the same island is 0.009 (T) and 0 (M, P). The route frequencies point to
  differential persistence and colonization and away from within-island refinement of threats; they are not a causal attribution.
- **Prior tier (RE 7 holds).** In consensus worlds at Λ = 100 residents' pooled T-weighted zero-prior-regret share is 0.03 [−0.03, +0.10] above the control (0.00–0.03 in M, 0.02–0.12 in T by cell).
  Their mean prior regret is 0.26–0.38 of the control's in T and 0.49–0.76 in M, but it is the same at Λ = 0, 100 and 1,000, and only
  0.3% of tail arrivals land after half the horizon. A bias present without the tail makes the founding scramble (founders are prior
  draws) the plausible source; that is not established, and Λ = 1,000 is exploratory.
- **Frozen natives (stage 1b).** Against real migrant fields the sign of σ predicts the direction where |σ| ≥ 0.5 (P 51 of 51; T 4 of 4 in the registered run and 19 of 22 in the exploratory diverse-world set; against N·ρ = 1). Magnitudes saturate (σ between −4 and −6 gives N·ρ ≈ 0.3–0.4 against the formula's
  0.01–0.06). Testers establish often enough to drag the neutral control to 0.25–0.8, so assumption A fails where
  the migrant tier is active: testing by migrants and colonization by migrants are the same event in the island model.
- **Time (RE 8 holds).** Mean T-weighted migrant regret does not rise from 25% to 100% of the horizon (pooled paired
  change −0.03 [−0.08, +0.02] σ units, 168 runs; pooled only, M at N = 400 rises by 0.35).
- **Costly threats survive untested.** 0.61 (T) and 1.00 (M) of zero-regret residents carry a costly threat against
  some prior program. This is prevalence at the horizon; it shows neither permanence nor that no supply could remove them.

**Reading.** The RS's lexicographic statement is supported as a catalogue-relative bias, not as optimality: in arm T and
dense arm P survivors are migrant-best replies among their on-path equivalents more often than a seed-law draw. The
route proxies attribute it to which islands persist and colonize and to equivalents that never arrive, with
within-island replacement of a worse equivalent near zero. P10 often predicts the direction, mis-sizes fixation in
both directions once testers are real, and did not predict the population regret shares. The third tier's bias does
not move with the tail's dose. Credibility as a long-run property is therefore
supported only in the weak sense: costly threats are still carried at the horizon by most zero-regret residents.

**Scope.** (i) Finite schedules at I = 64; "after a long time" is tested only to the horizons of queue 74 and "Bridge-less rivals".
(ii) Fitness is exp(w·payoff) in all arms, so P10's w/f is w. (iii) Arm P was run without lumping (migrant regret is undefined under
it), its middle dose is the published 1.091, and its supply control is founder-weighted, an approximation. (iv) Stage 1b switches off
focal-slot migration; its diverse-world arm T version and stage 3's arm T cell are exploratory, and stage 3's supply is restricted to
in-pair slots. (v) RE 4's recorded pass depends on the pooling weights (above). (vi) Arm M contributes no diverse world at mN = 1, so RE 5 is scored
on T and P.

**Predictions.** Held: RE 1, 3, 4, 5, 7, 8, 9. Falsified: RE 2 (a neutral tester's lineages establish) and RE 6 (arm T stays
program-diverse in 0.60 of worlds at N = 100 and 0.50 at N = 400).

**What it says about realizable source-readers.** A source-reading ecology does not police its own threats. Programs that differ only
off the path are sorted by which islands last and spread, and costly threats are still there at the horizon. Stage 3 suggests a supply of on-path variants sharpens the sorting; the object as it stands supplies few.

**The model can't express:** a migrant that tests a resident without risking a takeover (testing and colonization are the same kind of event); a
supply of on-path variants beyond other islands' residents and a front-loaded prior; off-path testing in a world at program consensus.
