# Drafts for the RE (encounter contracts; not merged into the shared docs)

## RESULTS section (draft)

### Contracts that form in encounters, with the responders' programs answering: every island is efficient within a few events, but the fair pairs are not held: each island cycles between fair and unequal pairs, the long-run law is 0.40 fair / 0.60 unequal, and coverage of all three pairs holds only at a high genesis rate (2026-10-26)

Spec `specs/2026-10-25-encounter-contracts.md` (queue 66; the RS: contracts as situation-keyed overrides that "trigger on the rare special cases where
they apply", formed when every signer does strictly better after the responders' programs answer; reviewed by gemini-4-argon then gpt-6.1-sol, three addenda each),
predictions `predictions/2026-10-25-encounter-contracts.md`, notes `notes/encounter-contracts.md`, report `runs/encounter-contracts.md` and `.json`, validation
`runs/encounter-contracts-validate.json`, cells `runs/encounter_contracts/`. Code `src/encounter_contracts*.py`, 27 tests (`tests/test_encounter_contracts.py`). Run by a Sonnet subagent.

**Object.** `dollar3`, weak arm, L seeds, N = 100, w = 0.3, ε = 0. An individual is a program plus up to 8 entries (key = the override-free action profile of
the encounter, fill = the carrier's action); stage 1 plays the programs, carriers whose key matches play their fills, the others re-run their programs against the fills
(the substitution reaches nested simulation). Genesis at rate ν per island-generation draws one individual per slot, a coalition and a new action profile and installs it on the
signers if each signer strictly gains after the responders answer. Order of limits: founding, 2,000 generations of relaxation with genesis, then one-migrant-at-a-time
islands at mN = 10⁻³ per slot per generation (one migrant per island per 333-generation round; clock = rounds), islands made large by pool size (I = 128 to 2,048); the strict
m → 0 object is the no-migrant island chain. Arms R, NR, BR (robust acceptance over pure equilibria), BRx (BR also executed), B (broadcast to 9 copies), C (copied proposals), H and
H-top and H-inert (hooks), S (no acceptance test), S-low (S at R's acceptance rate).

**Deviations (disclosed).** The spec's literal settlement rule is never met at ν = 1 (a firing contract forms on every fair island every ≈ 280 generations); a class is settled
after 500 generations in the same `_classify` class; the migration rate is the explicit mN = 10⁻³ (no class is a certified closed class); pools are 128–2,048 islands (founders
paired across arms by island index); eviction by installation order, not firing recency; 160 types per slot (never full); arm V, the recombination variant of C, the unmatched B cell and
A = 150 not run; **S at ν = 1 cut** (190 s per round at 512 islands; a 128-island 30-round pool and a 30-island no-migrant run show that no island settles a class); secondary-arm paired runs 6,000
events; the first two R cells predate three added counters; tracked-bundle aggregates include the 2,000-generation relaxation (under 1%); `settled` shares are among settled islands.
Validation: ν = 0 reproduces `many_islands.island_run` draw for draw (12/12 founders, 6/6 with arrivals); the exhaustive oracle against 30,000 Monte Carlo draws on 12 islands within
1.9σ; arm 0 against the stored chain: V\* increments 0.215 against 0.221 over 1,000 events (level 0.025 lower from the founding sample).

**Efficiency is reached and fast.** Wasteful plus disagreement islands drain within the 2,000-generation relaxation at ν = 1 (R: 0.011 at event 0, 0.000 at 10; arm 0: 0.31 at 0, 0.292 at 10,
0.026 at 1,000) and by event 100 at ν = 0.1 (0.022; 0.214 at 0); encounter efficiency 0.998 and 2% of islands with a Pareto-dominated payoff vector at ν = 1.

**Fairness is not reached.** R's V\* (the three fair pairs) is 0.39–0.42 at ν = 1 from event 0 to 1,000 (arm 0: 0.254 → 0.469); 0.32 → 0.40 (100) → 0.325 (1,000) at ν = 0.1; U about 0.6. The uplift over arm
0 at 1,000 events is −0.054 (ν = 1) and −0.144 (ν = 0.1). The no-migrant island chain (200 islands × 3·10⁵ generations at ν = 1; 3·10⁶ at ν = 0.1) has long-run occupancy 0.400 fair / 0.599 unequal /
0.001 W + D at ν = 1 and 0.395 / 0.601 at ν = 0.1: the stationary law does not depend on ν, the rates scale with it (fair-island exit 3.6·10⁻⁵ per generation at ν = 1, 3.7·10⁻⁶ at ν = 0.1; 99% of
exits to an unequal pair; unequal islands exit at 5.4·10⁻⁵, 43% to a fair pair, 54% to another unequal pair, the rotating dictator). No fair island is contract-stable (exhaustive oracle: 0 of 404 at
round 0, 0 of 414 at round 1,000; mean acceptance probability per draw 0.0043–0.0064). In the stable-set reading: the Pareto test counts only the signers, and on every fair island the excluded slot and
one pair member strictly gain from "demand ⅔ of the excluded slot, who takes ⅓" whatever the third member's program is (two accepted proposals of 560, 3.6·10⁻³ per draw, confirmed by the oracle); the excluded half
is neutral and the pair member's half underdominant until the excluded half is common (threshold ¾), so the deal is carried by a neutral drift followed by a selected sweep (fair → unequal),
and the same deal one level up (victim and excluded slot) takes an unequal island to a fair or a different unequal pair. Of 84,000 two-signer contracts formed on fair islands 0.45% fix in both slots, median half lifetime 2 generations; of the 13,000 singleton
contracts 31% fix (the sweeps after the excluded half has fixed). On settled fair islands 81% (round 1,000; 95–99% in the long runs) play the fair pair only through overrides (stage-1 fair mass 0.19 to 0.01).

**Migrant-attributed moves.** Paired migrant / no-migrant branches (same seed, 1,500 generations, 2·10⁴ events, cluster bootstrap over recipient islands): κ (to the donor's pair) 1.5–2.7·10⁻³ per migrant excess,
α (to the third pair) 0.65–0.90·10⁻³ at ν = 1 (excess intervals [0.25, 1.06]·10⁻³ and [0.55, 1.38]·10⁻³, both excluding 0), 1·10⁻⁴ at ν = 0.1 ([0, 2.5]·10⁻⁴); arm 0: 6·10⁻⁴ and 3·10⁻⁴.

**Arms.** NR and R are indistinguishable (V\*, within-chain occupancy, rates), so the response does not matter on this seed law (97% constants). BR accepts more per attempt (0.0074 against 0.0057) yet clears dominated
islands worse (W + D 0.070 and 0.145 against 0.002 and 0.034): with two uncommitted responders the pure equilibria include the responders pairing with each other, so singleton moves fail the robust test; BRx (responders
execute best replies) puts the within-chain law at 0.048 fair / 0.942 unequal. B (broadcast to 9 copies) raises the fair-island exit rate 4.7× and the fair occupancy to 0.536 (pool V\* 0.576 at 300). C (copying) changes nothing
(within occupancy 0.435; copied acceptance 0.005–0.009 against 0.006–0.010 uniform, half the copies unmatched). H blocks 0.31 / 0.52 / 0.67 of proposals by |S| (hooks at two thirds of leaves), halves the transition rate (0.43× R), lowers the fair
occupancy to 0.287 and leaves W + D at 0.04–0.075; H-top equals R, H-inert equals arm 0 (V\* 0.480 against 0.469); hooked programs gain 5–8 points of share. S at ν = 0.1 (512 × 1,000): V\* 0.365 with 24% of islands Pareto-dominated; at ν = 1 no island
holds a class. S-low (installation at R's acceptance rate): V\* 0.357 at ν_eff = 6·10⁻³ (round 300), 0.555 at 8.5·10⁻⁴ (round 1,000, arm 0 0.469).

**Order of limits and coverage.** At ν = 1 all three pairs are present from every start by event 300 (tilted starts forget the tilt) and at every pool size tested (I = 128 to 2,048, to 3,000–8,000 rounds; V\* 0.38–0.45 in four of five replicates at I ≥ 512; one
founder set drifts to V\* 0.17–0.23 with every pair at 0.04–0.07, with or without contracts carried by migrants). At ν = 0.1 the pool's V\* fluctuates with s.d. 0.085 (I = 128, 512) and 0.033 (I = 2,048), mean 0.23 at 2,048, and F0 falls to 0.023 at 10⁴ rounds
(trend, not resolved). At ν ≤ 0.01 pairs are lost by 10⁴ rounds (ν = 0.001: 0.000 / 0.381 / 0.006; ν = 0.01: 0.002 / 0.016 / 0.109), as in arm 0 (F1 = 0.000, V\* 0.975). Mixed starts are not a rescue.

**Verdicts** (full table in the report). Held: 3, 4 (ν = 1), 4c, 5c, 6 (ν = 1), 7c, E1–E4, E6, E10, E14. Failed: 2, 7, E13, and 8's second clause. Partial: 1 (fails at ν = 1, holds at ν = 0.1), 1c, 5, 8, E5, E7, E8, E9, E11, E12. 2c held.

**Reading.**
- Contracts make every island efficient quickly and give up the fair pairs: the Pareto test of the signers alone makes both the fair and the unequal pairs targets of the excluded slot's deals, so islands cycle (rate ∝ ν; stationary 0.40 / 0.60 whatever ν).
- Coverage in the weak sense (all three pairs present) holds at ν = 1 and is finite-pool; efficiency holds; fairness and crispness (a settled state) fail. The statement "every island efficient and all three pairs present" is true in the coverage-plus-efficiency sense and false as a statement of the fair, settled outcome.
- NR ≈ R; BR/BRx show that the response matters only through the equilibrium rule; H, C, S do not repair it; B shifts the law toward fair (a dilution, not a mechanism).
- Caveats: finite N, finite pools, one seed law (97% constants: responders almost never read), the migration rate is explicit, S at ν = 1 not run to its end, coverage at small ν unresolved at 10⁴ rounds.

## REJECTED entries (draft)

- **Encounter contracts with a signers-only Pareto test as the repair for the fair pairs (RS, 2026-10-25).** Dropped as a repair: R's V\* is 0.40 against 0.47 for no contracts at 1,000 events (ν = 1), 0.325 at ν = 0.1; the within-island law is 0.40 fair / 0.60 unequal for every ν; no fair island is contract-stable (oracle). It stays as an efficiency mechanism (W + D drains within the relaxation). RESULTS "Contracts that form in encounters…".
- **The RE's prediction 2 (+0.15 V\* from contracts), prediction 1 at ν = 1, E7 (BR acceptance 0.3–1.0 of R's), E8 (α interval includes 0), E9 (tilt forgotten at ν = 0.1), E13 (copying acceptance 5×), E11 (S-low within 2×): wrong as registered.** The signers-only structure was in the RE's examples but the dynamical consequence (rotating pairs) was not drawn.
- **Arm C (copying as a proposal source):** no effect on any statistic; copied proposals are re-proposals of carried fills and 90% are unmatched or already carried.
- **Arm H as a restriction that helps:** H lowers the fair occupancy (0.287) and leaves dominated islands (W + D 0.04–0.075); no gain over R.
- **Arm S at ν = 1 (selection alone with one random install per generation):** no island holds a class; the arm is dropped at that rate (S-low and S at ν = 0.1 are what is measured).
- **Prediction 8, original (silent halves drifting up neutrally):** withdrawn before the run; keys use override-free play, so both halves fire at once.

## THEORY paragraph (draft, for the RS's reading)

A myopic deviation rule that tests only the signers ("Pareto-improve even after the responders answer") makes a fair pair of three-player majority division dominated by the deal of the excluded slot with one pair member; the same rule applied to the new state moves it again. Without a farsighted clause (counter-threats) the rule has no stable set among the pair outcomes: the island process is a rotating walk among fair and unequal pairs with stationary law 0.40 / 0.60 (a hand estimate from the accepted-proposal counts gives about one third / two thirds; the run gives 0.40). The rule keeps efficiency and loses the V\* of the stable-set reading. The mismatch lies between the encounter-level test and the dynamics: acceptance is decided on the signers' encounter, selection on expected payoffs against the island's composition (the pair member's half is underdominant, so deals pass the test and then spread only through the excluded slot's neutral half). A stable-set statement for the ecology needs the counter-threat to be part of the test (the farsighted arm the RS excluded) or the veto-like guard of the stored contract layer; the order of limits adds a second issue (V\* at small ν is set by migration-driven drift and loses pairs at long times).

## NOTATION entries (draft)

- **contract entry / key / fill / carrier**: an entry of an individual's heritable list: (key p, fill a), p the override-free action profile of the encounter, a the carrier's own action; a carrier plays a when the stage-1 profile is p.
- **bundle**: the content of one accepted genesis (key, coalition, fill per signer); the identity used by arm C.
- **stage 1 / stage 2**: the encounter without overrides / with the carriers' fills, the others re-running their programs against them.
- **ν**: genesis attempts per island per generation. **round**: 333 generations (one migrant per island at mN = 10⁻³ per slot per generation); the clock is rounds = events per island.
- **arms**: R (response by programs), NR (responders hold stage-1 actions), BR (robust acceptance over pure best replies / equilibria of the remaining game), BRx (BR also executed), B (broadcast to 9 copies), C (copied proposals, q = 0.5), H / H-top / H-inert (writes into exposed hooks / also a top-level wrapper / hooks without genesis), S (no acceptance test), S-low (S at R's acceptance rate), R16 (cap 16).
- **settled class (operational)**: the `_classify` class held 500 consecutive generations. **cur**: the instantaneous class.
- **coordination-needing / coordination-free bundle**: a half's lone-carrier fitness change against the island's present populations is negative / not negative for some / no signer.
- **override-dependent fair island**: stage-1 (override-free) fair mass below 0.5 on a settled fair island.
- **oracle (contract-stability)**: exhaustive search over present type triples, coalitions and profiles for an accepted improving contract.
- **κ, α (this experiment)**: per-migrant excess probability, over the matched no-migrant branch, that a fair island ends in the donor's pair / in the third pair within 1,500 generations.
