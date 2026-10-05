# Predictions: the symmetric gate, 2026-10-05

Spec: `specs/2026-10-05-symmetric-gate.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-05-symmetric-gate-gpt-6.1-sol.md`,
and revised). Committed before the static diagnostics and before any run. These are trajectory and lottery outcomes at
finite sizes, not π: the window, mutation, migration and seed counts are stated per object.

## Design choices fixed before the run (where the spec leaves room)

1. **Where the rule acts.** In `contracts._eval_types` a box atom of reader t against opponent u with target τ is a
   contract read iff u and τ both carry. The new evaluator (`src/symmetric_gate.py`) adds one per-reader flag rc(t):
   the atom is a contract read iff rc(t) = 1 and u and τ both carry; otherwise it is a source read through the gate
   (b = 0: legible iff u's source is a constant). Asymmetric: rc ≡ 1 (must reproduce `runs/contracts_types_b0.npz`
   bit for bit). Symmetric: rc(t) = 1 iff t carries. Quenched q: rc(t) = 1 iff t carries or t's source is assigned
   "reads contracts".
2. **"Reader" is the executing program at every level.** A box is a statement about the opponent's actual play; that
   play is the opponent's own execution, so boxes inside it are evaluated under the opponent's access, not the outer
   reader's. Soundness (Lemma 0) requires this; the certified-implication audit is rerun under every rule and must
   show 0 violations. Unit tests (`tests/test_symmetric_gate.py`) cover: a non-carrier's box about a carrier
   (reciprocal: FairBot non-carrier vs FairBot carrier, both directions), a non-carrier's box about a carrier's box
   about it (`BOX(THEM(THEM))` and `BOX(THEM(^C))` against carriers), literal targets, constants (legible from source
   under every rule), and the carrier–carrier block (contract reads under every rule).
3. **Quenched assignment.** Unit = canonical source (the evaluator's non-carrier type (p, none)). One uniform u_p per
   canonical source, `numpy.random.default_rng(20251005).random(610)` in source-index order; source p reads contracts
   iff u_p < q. The assignments are therefore nested (q = 0.25 readers ⊂ q = 0.5 readers), with q = 0 the symmetric
   and q = 1 the asymmetric rule. The same assignment is used in every cell.
4. **Frozen backgrounds** (non-carrier only, computed once and shared by every rule; the non-carrier block is
   rule-independent, which is checked): μ; the ε = 0 non-carrier Moran-replicator flow at the moment ALLC first falls
   below 10⁻³ ("post-scramble"); and the ε = 10⁻³ mutation–selection equilibrium of the non-carrier system. Growth
   rate of a rare carrier group (mix composition: establishers ∝ μ, own signature) at f = 10⁻³ is
   F̄_carrier / F̄ − 1 per generation with F = exp(w·payoff), net of contract stripping at ε = 10⁻³ on that
   background, exactly as `src/prover_carrier_static.py` defines it.
5. **The fringe and its intervention.** Fringe pairs = (non-carrier t, carrier u) with t cooperating with u under the
   asymmetric rule, not under the symmetric rule, and u defecting on t. The intervention sets exactly those actions to
   D in the asymmetric table, holding every other action and the background composition fixed. The other changed
   entries (mutual cooperation lost, or a non-carrier that cooperates under illegibility but defects on reading the
   contract) are reported as separate components.
6. **Deterministic invasion threshold** = smallest f at which carrier fitness exceeds the background's mean fitness
   (f*, NOTATION), and the threshold of the full type-level flow from each seeded state; **establishment threshold** =
   the seed frequency giving establishment probability 0.5, by interpolation in log f₀ of the run success fractions.
7. **Definitions** (spec). *Established:* carriers ≥ 50% of the population for at least 1,000 consecutive generations
   within the window (the second half of the run); the whole-run variant is also reported. *Extinct:* zero carriers;
   at s = 0 absorbing, so the run stops there (as in the previous experiment). *Censored:* neither by the window's end.
   ε = 0 twins and lottery runs stop at the outcome freeze; there "efficient" is P(C,C) ≥ 0.95 at the freeze (the
   previous convention), with carriers at the freeze and extinction also reported; a run that does not freeze by its
   horizon is censored.
8. **Seeds.** 'mix', σ = 0, s = 0, w = 0.3, b = 0, PD, `prover_carrier_seed` kernel unchanged; populations depend only
   on (f₀, N, I, rep), so the four rules are paired on identical initial populations and RNG seeds. Reps 0–19.
   Wilson 95% intervals; paired differences per rep (success indicator, rule A − rule B) with a 95% interval from
   the paired sign data (exact McNemar on discordant pairs, plus a Newcombe-style interval for the difference).
9. **Lottery:** (100, 64), mN = 1, ε = 0, k ∈ {1, 3}, 40 runs per rule × 4 rules, `prover_carrier_seed.lottery_state`
   populations (paired across rules; the asymmetric cells should reproduce the published 37/40 and 40/40).
10. **Invasion challenge:** one island of N = 100, ε = 0, 99 carriers drawn from the establishers ∝ μ with their own
    signatures (one fixed draw per rep, shared across rules and invaders) plus one invader (D, ALLC or non-carrier
    FairBot) at a uniform slot; 100 runs per (invader, rule), run until the freeze. Reported: the invader lineage's
    share at the stop, invader extinct / fixed, P(C,C) at the stop. A resident-only control (no invader, the 100th
    slot also a carrier) is run per rule.
11. **b = ∞ baseline:** symmetric vs asymmetric payoff tables compared entry by entry (exact equality, not trajectory
    similarity).
12. **Window.** One run is timed first; any reduction of the 2·10⁴-generation window or of seed counts is predeclared
    in an addendum below before the grid starts.

## RE predictions (Fable, from the spec, verbatim in substance)

1. **The symmetric rule removes the frequency-independent advantage, leaving only the linear one.** Symmetric
   rare-carrier growth at 10⁻³ after the scramble is in [0, +0.002]; the fringe-to-D intervention on the asymmetric
   rule reproduces the symmetric growth within 0.002. *Falsifier:* symmetric growth at 10⁻³ above +0.005, or the
   intervention leaving growth above +0.005.
2. **Establishment under the symmetric rule is drift-limited and needs a larger seed.** The establishment threshold
   moves from ≈ 0.01 to 0.03–0.1: success at f₀ = 0.01 falls from ≈ 0.5 to below 0.2, at f₀ = 0.03 to 0.2–0.6, and at
   f₀ = 0.1 stays ≥ 0.8 (bets from the linear-advantage picture; the paired differences with intervals are the test).
   *Falsifier:* symmetric success at f₀ = 0.01 above 0.4, or at f₀ = 0.1 below 0.6.
3. **The advantage is dosed by q, on the frozen background.** Rare-carrier growth after the scramble is monotone in q,
   with q = 0.5 within 0.003 of the asymmetric value; success at f₀ = 0.01 monotone in q as a point estimate (full-run
   non-monotonicity reported, not scored). *Falsifier:* frozen-background growth non-monotone in q.
4. **Once established, carriers hold under either rule:** carrier–carrier P(C,C) = 1.00 and population P(C,C) ≥ 0.9
   in every established run (the mutation-fed ALLC shadow not counted against this), and no established run collapses
   within the window. *Falsifier:* a collapse, or population P(C,C) below 0.8 in an established run.
5. **The lottery at (100, 64) with k = 1 falls under the symmetric rule** from 0.925 to 0.3–0.7; with k = 3 it is ≥ 0.8
   under both rules. *Falsifier:* symmetric k = 1 above 0.85, or symmetric k = 3 below 0.5.

## RS predictions (Jacob)

None recorded.

## Subagent predictions (Opus, before the static diagnostics)

Hand calculation. At b = 0 a source read is legible only if the opponent's source is a constant, so the gate mask does
not depend on settle times and needs no fixed point. Under the symmetric rule a non-carrier treats a non-constant
carrier exactly as it treats a non-constant non-carrier (every box false), so it plays its *illegible default* against
it. Post-scramble, carriers then differ from D only by f·(R − P) from meeting each other, by T − P = 2 against
default-C programs (which defect on the legible D but cooperate with the illegible carrier) and by R − T = −1 against
ALLC; both of the last two are O(ε) in mass at the ε = 10⁻³ equilibrium. The diffusion fixation probability of a
carrier group with s(f) = w·f − ε (mutation strips 99.5% of carrier contracts), variance 2f(1 − f)/N per generation,
gives ψ(y) = exp(−N(w y²/2 − ε y)) and success ≈ 0.09 / 0.31 / 0.74 / 1.00 at f₀ = 0.003 / 0.01 / 0.03 / 0.1 for
N = 6,400, 0.55 at N = 25,600, f₀ = 0.01; and at ε = 0, 0.10 / 0.35 / 0.81 / 1.00. The same calculation with a constant
s = 0.01 gives 0.47 at f₀ = 0.01, the asymmetric result (0.50). A scramble discount (carriers lag D while ALLC lives)
lowers these somewhat.

- **S1 (where the rule acts).** At b = 0 the only entries that change between rules are non-carrier → non-constant
  carrier actions; the carrier rows and the non-carrier–non-carrier block are identical under all four rules.
  *Falsifier:* any changed entry outside that block.
- **S2 (b = ∞ baseline).** Hedged: a contract read is the box over the representative's free-GL trace, a source read
  is the box over the carrier's actual trace, which among carriers is the stable action from world 0. Level-0 boxes
  (`BOX`) about carrier pairs can therefore differ (FairBot's free trace defects at world 0). I predict the tables are
  **not** exactly equal at b = ∞, that the differing entries are confined to non-carrier readers against carriers, and
  that their μ×μ mass is below 0.01. *Falsifier:* exact equality (then the baseline holds as the spec intends), or
  differing mass above 0.05.
- **S3 (static).** Symmetric post-scramble growth at 10⁻³ in [0, +0.002] (with RE 1); symmetric growth at the μ
  background below the asymmetric −0.006. The fringe intervention accounts for ≥ 80% of the asymmetric − symmetric
  growth gap post-scramble. q-growth is close to linear in the *fringe mass* assigned to read, not in q, so q = 0.5
  is within 0.003 of the asymmetric value only if the realized assignment covers ≥ 70% of the fringe mass.
  *Falsifier:* the intervention explaining < 50% of the gap.
- **S4 (finite ε, N = 6,400).** Symmetric success 0–3 / 2–9 / 10–17 / 18–20 of 20 at f₀ = 0.003 / 0.01 / 0.03 / 0.1;
  asymmetric 1–6 / 7–14 / 15–20 / 20 (the previous cells); paired asymmetric − symmetric difference at f₀ = 0.01
  positive with an interval excluding 0. *Falsifier:* symmetric at f₀ = 0.01 ≥ 12/20, or at f₀ = 0.1 < 16/20.
- **S5 (N = 25,600, f₀ = 0.01).** Symmetric success rises with N relative to N = 6,400 (diffusion: 0.55) but stays
  below asymmetric. *Falsifier:* symmetric at N = 25,600 below its N = 6,400 point estimate.
- **S6 (twins).** Same ordering as finite ε; symmetric twins 0.2–0.5 at f₀ = 0.01, ≥ 0.9 at 0.1.
- **S7 (lottery).** Symmetric k = 1 at (100, 64) in 0.5–0.85 (one establishing island suffices, spread is one-way and
  a single carrier on N = 100 is near-neutral, per-island ≈ 0.02–0.04); k = 3 ≥ 0.9 under every rule.
  *Falsifier:* symmetric k = 1 below 0.3.
- **S8 (invasion challenge).** Under every rule: D fixes in 0/100; non-carrier FairBot fixes in 0/100 (exploited
  under the asymmetric rule, mutually defecting under the symmetric); ALLC is near-neutral and fixes in ≤ 5/100.
  *Falsifier:* D or non-carrier FairBot fixing in any run.

## Addendum before the grid (2026-10-05): timing, tables, no window reduction

Committed after the static diagnostics (`runs/symmetric_gate_static.json`, `runs/symmetric_gate_tables_info.json`) and
before any grid run. Disclosed: two timing runs (mix, f₀ = 0.03, N = 6,400, rep 0, 2·10⁴ generations; symmetric and
asymmetric; both established). The asymmetric one reproduces the published row of the previous experiment exactly
(P(C,C) 0.98907, carriers 0.7303, t₅₀ 184), so the kernel and table installation are bit-identical to the run being
paired against.

- **Timing:** 11–14 s per 2·10⁴-generation run at N = 6,400 with load ≈ 5. **No reduction:** the spec's window
  (2·10⁴ generations, second half), 20 seeds per cell, N = 25,600 at 10 seeds. ε = 0 twins, lottery and challenge
  runs stop at the freeze with a 10⁵-generation horizon (unresolved runs are censored).
- **Tables** (static, before runs): the asymmetric tables reproduce `contracts_types_b0.npz` and `val_inf` bit for bit;
  the certified-implication audit has 0 violations under every rule at b ∈ {0, ∞}. At b = 0 every changed entry is a
  non-carrier → carrier action (107,188 entries under the symmetric rule); 1,352 of them are against *constant-source*
  carriers carrying a non-constant contract valid for that constant, so S1's sub-clause "non-constant carrier" is
  already false (recorded, not re-scored later). At b = ∞ the tables are **not** equal (172,517 entries, 47,372 of them
  carrier → non-carrier, μ×μ mass 0.0006 / 0.0004 against own-signature carriers); S2's inequality held, its
  confinement clause failed.
- **Added set, because the exact b = ∞ check failed:** `inf_pair`, b = ∞, f₀ = 0.01, asymmetric vs symmetric, 20
  seeds, finite ε, same window, to show the outcome-level size of the inexactness. Run last.
- **Order:** main → twins → N = 25,600 → lottery → invasion challenge → inf_pair, 3 workers. Any cell projected beyond
  about 2 hours is stopped and recorded as censored.
- No prediction or threshold changes.
