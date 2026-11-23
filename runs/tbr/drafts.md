# Queue 81 drafts for the shared docs (for the RE to merge; not edited in place)

Source: `runs/tiered-best-response.md`, `runs/tiered-best-response.json`, `notes/tiered-best-response.md`,
predictions `predictions/2026-11-23-tiered-best-response.md`. All population numbers are finite-schedule statistics,
not π.

## RESULTS draft: "Do surviving programs best-respond in tiers?" (queue 81)

The RS's statement (OH doc, 2026-11-23): after a long time each program best-responds lexicographically, first to the
island's natives, then to the distribution of migrants, then to the mutation prior. Mechanism: PROOFS P10, the
tiered fixation lemma, under assumption A (testers form a stationary field unaffected by the variant). Arms: T
(27-program L_T library, A_f at 0.1) and M (n ≤ 6 modalPA DSL) of queue 74 at I = 64, seed lottery plus annealed
tail. P: queue "Bridge-less rivals", modal PD at n = 9, N = 200, I = 64, mN = 1.091. Published worlds were
regenerated with saved compositions; every arm T and M run-cell reproduces queue 74's stored V\* series and
migration count exactly (120 of 120). Arm P was checked draw for draw with lumping on (35 of 35) and rerun
lump-free (same law), matching the published cells' headlines (dense P\* separated 0.95–1.00 against 0.97).

- **The lemma (stage 0).** Under A by construction, P10 is exact: 18 of 18 points contain the finite-N value
  (RE 1 holds). With real tester lineages, selected-against testers (relative fitness 0.7, 0.9) keep the sign and
  roughly the size. A neutral tester does not: its long-lived lineages establish and truncate replicates, giving a
  wrong sign at N = 100, σ = 0.5 and errors from −64% to +218% (RE 2 falsified).
- **The migrant tier exists in arms T and P, not in M (RE 3 holds).** In program-diverse worlds at mN = 1, settled
  residents with zero native regret are T-weighted best replies to the migrants among their on-path equivalents at
  0.96–1.00 in T against 0.44–0.69 for a seed-law draw from the same equivalence class (excess 0.42), and at 0.47
  against 0.28 in P (dense). In M the excess is 0.02. Pooled excess 0.18 [0.09, 0.30].
- **It is mostly supply (RE 4 holds by rule, on few cases).** In T and M, most residents never met an on-path
  equivalent: the arrival sets are empty in 55–96% of cases. Where equivalents did arrive, they were at zero regret
  as often as residents (excess over the arrival control −0.01 in T, 0.00 in M). The one place the tail supplies
  equivalents (T, Λ = 1,000) shows a real filter: 0.19 of the arrivals at zero regret against 1.00 of residents
  (33 cases). In P the founder-weighted control removes about a quarter of the excess.
- **Dose (RE 5 holds, arm T only).** Arm T's zero-regret share in diverse worlds is 0.69 at mN = 0.1 and 0.96 at
  mN = 1. At mN = 0.1 it rises over the run (0.42 → 0.57 → 0.69) against a flat control (0.29). At mN ≥ 3 worlds
  reach program consensus and the tier empties. Arm M has no diverse world at mN = 1 (N = 200) and no tier at 0.1.
  [Arm P: fill in from the stage-2 table.]
- **Outcome consensus is not program consensus (RE 6 falsified).** Arm T's worlds are at fair consensus by outcome
  (queue 74) but 0.25–0.60 stay diverse in programs at mN = 1. Nearly all of that is among on-path equivalents: 6 of
  27 program-diverse worlds differ in outcome. The migrant tier acts exactly on off-path differences.
- **Routes (RE 9 holds).** Zero-regret residents held their island from 25% of the horizon (T 0.64, M 0.72, P 1.00)
  or came with a whole profile that took the island over (T 0.28, M 0.21, almost all migrant-borne). Replacement of
  an on-path equivalent with positive regret on the same island is 0.009 (T) and 0 (M, P). The pattern is
  differential persistence and colonization, not within-island refinement of threats.
- **Prior tier (RE 7 holds).** In consensus worlds residents' zero-prior-regret share is within 0.03 of the control.
  Their mean prior regret is a third to a half of the control's, but it is the same at Λ = 0, 100 and 1,000, and only
  0.3% of tail arrivals land after half the horizon. The bias comes from the founding scramble (founders are prior
  draws), not from the annealed tail.
- **Frozen natives (stage 1b).** Against real migrant fields the sign of σ predicts the direction (P 51 of 51,
  T 19 of 22 against N·ρ = 1). Magnitudes saturate (σ between −4 and −6 gives N·ρ ≈ 0.3–0.4 against the formula's
  0.01–0.06). Testers establish often enough to drag the neutral control to 0.25–0.8, so assumption A fails where
  the migrant tier is active: testing by migrants and colonization by migrants are the same event in the island model.
- **Time (RE 8 holds).** Mean T-weighted migrant regret does not rise from 25% to 100% of the horizon (pooled paired
  change −0.03 [−0.08, +0.02] σ units, 168 runs).
- **Costly threats survive untested.** 0.61 (T) and 1.00 (M) of zero-regret residents carry a costly threat against
  some prior program. No migrant tests it, and the prior tier does not remove it at these doses.

**Reading.** The RS's lexicographic statement holds as a pattern in the arms where worlds stay program-diverse (T and
P): survivors are migrant-best replies among their on-path equivalents much more often than chance. The pattern is
made by which islands persist and colonize, and by which equivalents never arrive. It is not made by threats being
tested and replaced within islands. Each lower tier is a bias whose size P10 overstates once testers are real, and
the third tier's apparent effect is the founding scramble's. Credibility as a long-run property is therefore
supported only in the weak sense: carried threats that no present migrant tests are not removed, and their removal
would need a supply of on-path variants that the object does not provide.

## REJECTED draft

- **RE 2 (real testers within 25% for an indifferent tester; no wrong sign):** falsified. A neutral tester's lineages
  establish and truncate replicates (wrong sign at N = 100, σ = 0.5; errors −64% / +218%). What survives: the sign for
  selected-against testers. Lesson: P10's σ is a mean-field bias. With long-lived or invading testers it misstates
  the size and can flip the sign.
- **RE 6 (arm T at mN = 1 mostly in consensus):** falsified at N = 100 (0.60 diverse) and N = 400 (0.50). It held at
  N = 200 (0.25) and at mN = 10 (0). The RE conflated outcome consensus (queue 74) with program consensus.
  Off-path diversity among on-path equivalents persists under migration.
- **The idea that tier 3 acts through the annealed tail at our doses:** the residents' prior bias is dose-independent
  (Λ = 0 / 100 / 1,000) and the tail is 99.7% spent by half the horizon. Drop "the prior tier is the tail's" in
  favour of "the founding scramble is a prior tier".

## NOTATION draft

- **E(p; k)** (on-path equivalents): catalogue programs p′ that, put in p's slot on island k with the other slots at
  their majority programs, leave the whole payoff vector of the encounter unchanged (one population: u(p′,p) =
  u(p,p′) = u(p′,p′) = u(p,p)). **E_comp**: equality against every present combination.
- **Migrant regret** (arrival-weighted): best migrant payoff in E minus p's, the migrant payoff being the expected
  payoff when one other slot's resident is replaced by a draw from the other islands' majorities (island-count
  weights). **T-weighted migrant regret** (σ units): max over E of σ(p′) = w Σ_q m_q T_q Δ_q (P10's σ with w/f = w
  for fitness exp(w·payoff)), m_q = mN·n_q/(I − 1), T_q the exact single-arrival sojourn (copy-generations to
  extinction or N/2) on the island's native profile.
- **Prior regret** (in tier): the same against the tail law, within the migrant-argmax members of E.
- **Native regret:** best catalogue payoff against the island's majority profile (or composition) minus p's.
- **Prior-matched / founder / arrival controls:** E weighted by the seed law / by the run's founder counts / uniform
  over E members that arrived on the island while the horizon profile held.
- **Program-diverse world:** at least two majority program profiles each on ≥ 5% of islands (outcome-diverse: at least
  two payoff vectors so represented).
- **Routes** of a zero-regret resident: (c) island taken over, (a) replaced an on-path equivalent with positive
  regret, (b) held from 25% of the horizon, (u) other.
