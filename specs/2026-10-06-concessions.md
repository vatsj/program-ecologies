# Spec: concessions: a boss grammar with probes ("pay fair to those who would strike"), 2026-10-06

Status: reviewed by gpt-6.1-sol (`reviews/2026-10-06-concessions-gpt-6.1-sol.md`) and revised; changes marked
[after review]. From the RS's proposal (2026-10-06): "real unions demand higher wages and get them quickly; I'd
like to see bosses adopting concessions like 'if they strike, give them what they want'". To be run by an Opus
subagent. The social organization game; the ε→0 chain and the mutation-free seed lottery.

## Why

The boss grammar of the union run reads only the current encounter: `BOX(W_j = strike)` is "this worker provably
strikes against me", and a concession conditioned on it cannot fire against a militant (the Löb loop lands at
(pay 0, strike): the strike is provable only if the wage is low, and the wage is low only if the strike is
unprovable). The concession the RS describes is counterfactual: "pay fair to those who *would* strike if paid
low", a probe `BOX(W_j(^(0, ·)) = strike)`, the worker's play against a quoted zero-wage boss. The PD arm has probes
(PrudentBot's `BOX(THEM(^D))`); the boss grammar does not.

**The hand analysis, corrected after review.** With the zero-wage probe alone, the discriminating boss
D₀ = "pay 1/2 iff provably strikes against the zero-wage boss, else 0" pays 1/2 to every worker who would strike at
zero wage, including a worker who strikes *only* at zero wage (the threshold worker T₀ = "strike iff s = 0"). T₀
earns 1/2 from D₀ exactly as the militant does, so it enters the worker slot neutrally, and once it has replaced
the militants a boss paying 1/4 to certified zero-wage strikers strictly improves on D₀: **a worker-side
accommodation ratchet to the smallest positive wage** (sol). The concession that resists it is the **full price
discriminator** D\* = "pay each worker the smallest wage it provably accepts": 1/2 to a worker that provably strikes
against the 1/4-boss, 1/4 to one that strikes against the 0-boss but works for 1/4, 0 otherwise. Against D\*,
demanding more is strictly better for a worker (the militant earns 1/2, T₀ earns 1/4, the scab 0), so accommodating
workers are deleterious, not neutral, and the fair state's only neutral exit is on the boss side (D\*'s on-path
shadow, the constant-fair boss), after which T₀ can drift in and a wage cut fire. Whether that gives the fair state
an extra resistance factor is **not** to be inferred from counting neutral steps [after review]: it is to be
computed as effective basin-to-basin rates with residence times, return paths and hitting probabilities between
the named basins (fair, 1/4, zero-wage, whacking). The pool (a whacker that recovers a militant's product earns
1 − c > 1/2) breaks every version: the cost of repression stays the wage floor. [after review] Sol's robustness
criterion, **preservation of demands under neutral worker substitution**, is reported for every fair state: the set
of neutral worker substitutes and whether some boss strictly profits once they have fixed.

**RS prediction (2026-10-06, as stated):** bosses adopt concessions of the form "if they strike, give them what they
want", and unions demand higher wages and get them quickly.

## Design

**Grammars** [after review: the probe ablation, a sham-probe control, and mass preservation].
- *P₀:* boss atoms as in the union run plus the zero-wage probe only, `BOX_L(W_j(^(0,none)) = a)`, a ∈ {work,
  strike}, j ∈ {1, 2}, L ∈ {PA, PA + Con} (sol's ablation; D₀ is expressible as a one-atom conditional).
- *P₀₁:* probes at the 0-boss and the 1/4-boss, at the smallest boss cutoff that admits D\* for one worker slot
  (a two-atom conditional; report the cutoff and class count; if the chain does not fit, add D\* and its policy
  duplicates as named classes by **mass-preserving substitution** and say so).
- *Sham:* the same number of added atoms as P₀₁, each evaluating to a fixed value (inert), so the prior's
  normalization and syntax multiplicity match P₀₁ without its expressivity; and the union run's grammar with the
  old programs' mutation masses preserved as the matched reference.
- Workers unchanged; a secondary arm gives them the symmetric probe `BOX_L(B(^strike) = s)`.
- **Named workers** [after review]: scab; T₀ (strike iff s = 0); T₁ (strike iff s ≤ 1/4, the militant); the
  always-striker; the union; and **named bosses**: the constants; D₀; D\*; "pay 1/4 iff strikes at 0"; the
  committed whacker; with every named pair's play and payoff printed in the predictions file.
- **RR semantics** [after review]: a probe reads the *executed* action of the quoted encounter under the arm's
  enforcement rule (committed in CC; after the rational override in RR), evaluated inside the per-world evaluator
  as in the enforcement run, with ties resolved to the committed recommendation; both the predicted and the
  executed actions are tabulated.

**Static first.** Full play and payoff tables; the Löb loop of the current-encounter concession; D₀'s and D\*'s
plays against every named worker; the accommodation ratchet (T₀ neutral against D₀; the 1/4-boss strict after it;
T₀ deleterious against D\*) checked by the evaluator; the fakers of D₀ and D\* by exhaustive search (workers that
satisfy the probe but work for a lower wage than the probe implies, and bosses that make workers' probes true while
paying low), with Lemma 0 as the reference; and, from the chain's transition model, the **effective
basin-to-basin rates** among the named basins at N = 10³ and 10⁴ (hitting probabilities and residence times by the
audited solver's generator), reported before any π.

**Chain** (seeded log-domain solver, closure-seeded discovery, twin-expanded beside lumped, per IMPLEMENTATION §4):
N ∈ {10², 10³, 10⁴, 3·10⁴}, w = 0.3, c ∈ {0.1, 0.5}; arms P₀ CC, P₀₁ CC (main), sham CC, mass-preserved reference,
P₀₁ RR, P₀₁ with the pool, P₀₁ with worker probes. Report wage-specific occupancy (0 / 1/4 / 1/2) separately from
efficiency (full production at 1/4 and at 1/2 are both efficient), the disjoint summaries, the fair share's
N-scaling (log odds against log N, descriptive), support, transitions, the exits of each basin, payoffs, the
three-role distribution threshold, and the preservation-of-demands statistic.

**Lottery** [after review: the mutation-free object]: ε = 0, seeds iid from each slot's length prior, N = 100 per
slot, I = 16, mN = 0.1, c = 0.5, horizon 10⁵, the verified-closed stop (global support, as in the social-organization
lottery spec), 40 runs, P₀₁ and the reference, CC and RR; a **fair island** = a closed island at wage 1/2 with both
workers working; report establishment (first fair island, censored time-to-establishment with intervals) and
persistence (fair islands at the horizon) separately, with the striker/militant share trajectory.

Priority: static (including the basin rates) → P₀₁ CC at N = 10³, 10⁴ → P₀ CC → sham and reference → N-scaling
cells → RR → pool → lottery → worker probes. ≤ 3 workers; stop where time runs out and say so.

## Required outputs

`runs/concessions.md` and `.json`, code in `src/concessions.py` (extending `src/union.py`'s grammar with probe
atoms; reusing `src/union_chain.py`, `src/union_enforcement.py`, `src/chain_log.py`, `src/sog_lottery.py` if merged;
no core edits except bug fixes in their own commits), a predictions file from the spec committed before any counted
run (static tables may precede it as an addendum), the usual hand-back (draft RESULTS, REJECTED, THEORY §3
"Distribution" and §9.9 edits, DEFERRED 6 and 10 edits, NOTATION, ≤ 5 lines, branch from
`git branch --show-current`, commits).

## RE predictions (with falsifiers) [after review]

1. **The accommodation ratchet is real with the zero-wage probe alone and absent with the full discriminator:**
   in P₀, T₀ is neutral against D₀ and the 1/4-boss strictly invades after it, so P₀ CC's π sits at the smallest
   positive wage (1/4 occupancy ≥ 0.5 at N = 10⁴, fair ≤ 0.1); in P₀₁, T₀ is deleterious against D\* and the fair
   state's only neutral exit is the boss shadow. *Falsifier:* P₀ fair ≥ 0.3 at 10⁴, or a neutral worker exit from
   (D\*, militant, militant) other than through the boss shadow.
2. **With the full discriminator the fair share grows with N under the length prior:** P₀₁ CC at c = 0.5 gives fair
   ≥ 0.3 at N = 10⁴ with a positive log-odds slope, against ≤ 0.005 for the reference and ≤ 0.05 for the sham
   grammar (expressivity, not prior mass). The exponent is not predicted; the basin-rate calculation is the claim.
   *Falsifier:* P₀₁ fair ≤ 0.1 at 10⁴, or the sham grammar within 0.05 of P₀₁. Grey zone 0.1–0.3.
3. **No quorum is needed:** union mass in P₀₁'s fair support ≤ 0.1. *Falsifier:* ≥ 0.5.
4. **RR gives the smallest positive wage** (sol's reading adopted: the militant's strike at 1/4 is overridden, so D\*
   pays 1/4; 1/4 occupancy ≥ 0.5, fair ≤ 0.1 at N = 10⁴) **and the pool gives zero wage** (fair ≤ 0.05). *Falsifier:*
   RR fair ≥ 0.3, or pool fair ≥ 0.2.
5. **Quickly, in the lottery:** P₀₁ CC reaches a fair island within 500 generations in ≥ 0.6 of runs against ≤ 0.1
   for the reference, and ≥ 0.5 of its islands are fair at the horizon. *Falsifier:* ≤ 0.3 of runs reaching a fair
   island by 10⁴, or fair persistence ≤ 0.2.
6. **The spoilers are accommodating workers and alternative bosses, not fakers** [after review]: D\*'s fakers have
   mass ≤ 10⁻³ and change nothing by more than 0.05; the preservation-of-demands statistic shows that every neutral
   worker substitute of the P₀₁ fair state is a militant twin (same demands), and that P₀'s fair state has T₀ as a
   demand-lowering neutral substitute. *Falsifier:* a faker of mass ≥ 10⁻² strictly invading the P₀₁ fair state, or a
   demand-lowering neutral substitute in P₀₁'s fair state.

The RS's prediction is item 5 and the direction of 2; the RE invites him to put numbers on them.
