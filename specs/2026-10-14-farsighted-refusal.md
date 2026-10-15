# Spec: farsighted refusal: can programs derive the guard that recovers the stable set?, 2026-10-14

Status: draft by the RE (Fable); to be reviewed by gpt-6.1-sol and gemini-4-argon; to be run by an Opus subagent.
Follow-up to RESULTS "Dominance contracts and refusal on islands" (Gemini's suggestion there) and DEFERRED 15.
REJECTED.md checked: nothing re-opened. DEFERRED 8 excludes lookahead *fitness* (it builds the phenomenon into the
selector); here lookahead lives inside a program's consent rule and fitness stays realized payoff, so entry 8 is not
re-opened.

## Why

Atomic pair contracts give the generator's walk (exactly 1/3 on V\*); a hand-written veto on exits from V\* recovers
the set and spreads under migration. Gemini asked whether a program can *derive* that veto: refuse κ iff accepting
provably leads to its own exclusion. **RE static check (before this spec):** on the 20 realizable outcomes, the
one-step exposure rule ("refuse κ iff after x some dominating contract excluding me would leave me below my status
quo", or below x) freezes *every* pair outcome, not only V\*: each pair member is exposed at every pair outcome, since
the excluded player plus the other member can always dominate. So the naive derived guard is "refuse everything",
which freezes islands wherever they first form a pair and singles out nothing. The candidate that could single out
V\* is the farsighted one with values: Anesi (2010) shows, for majority voting with a status quo and patient
players, that stable sets are the absorbing sets of Markov equilibria of a dynamic bargaining process (Konishi–Ray
2003 style). The test: programs whose consent rule is the Konishi–Ray (KR) value comparison, on islands.

## Design

**Machinery.** `src/dominance_contracts.py` unchanged (import only): `dollar3`, ε = 0, L seeds, N = 100, I = 64,
mN ∈ {0, 1}, menu F (all 27 contracts), β = 1, ν = 0.1, public consent (one drawn individual per S slot), 40 runs,
horizons 2,000 (all runs) and 10,000 (main cells, all runs), occupancy by the 0.95 classifier and by modal play.

**Guards (heritable consent traits; play unaffected).**
- **g0:** accept every proposed (dominating) contract (= D1).
- **gV:** the hand-written veto on exits from V\* (= R2 / R1-public reference).
- **g1:** one-step exposure (refuse iff after x a dominating contract excluding me leaves me below y_i), with the
  "below x_i" variant reported statically.
- **gKR(δ):** accept κ iff W_i(x) > W_i(y), where W is the discounted value (δ per contract event) of the contract
  process in which *every* consent decision uses gKR(δ): a fixed point (a KR equilibrium process under our protocol:
  a uniform draw from the 27 contracts, dominance required for proposal, consent by S). Ties: refuse. Multiple
  fixed points: enumerate from several initializations (myopic, all-refuse, random), report all, and use the one
  reached from the myopic process as the default program, with the others as cells if they differ in absorbing set.
- **gKR-read(δ):** the source-reading version: W is computed under the guards the island's programs actually carry
  (the consent probabilities implied by current guard frequencies per slot, read from sources), recomputed when the
  island's guard composition changes. Against a monomorphic gKR island it equals gKR.

**Static first (notes §1, before any cell).** For δ ∈ {0.5, 0.8, 0.9, 0.95, 0.99}: every KR fixed point found, its
absorbing set, stationary V\* mass and hitting times; whether some fixed point has absorbing set exactly V\* (the
Anesi analogue under our protocol); which outcomes the farsighted sets of the stable-sets run (game effectiveness:
V\* plus held-player pairs such as {(4,2,0), (0,2,4)}) correspond to; the g1 freezing set (reproduce the RE's
check); the computational cost of gKR and gKR-read per decision in evaluator steps (value iteration on 20 states).

**Cells.** U-g1, U-gKR(0.9), U-gKR(0.99), U-gKR-read(0.99): the guard universal, mN ∈ {0, 1}. M-gKR: gKR(0.99) at
frequency ½ against g0 (public consent), mN ∈ {0, 1}, with the frequency trajectory and the immigrant-rescue
decomposition of the dominance-contracts run. C3: gV, gKR(0.99) and g0 each seeded at ⅓, mN = 1 (which guard
spreads). M-read: gKR-read against gKR at ½ each, mN = 1. Baselines D1 and R2 rerun on paired seeds (bit-identical
check against the stored runs). N panel: U-gKR(0.99) at N ∈ {50, 200}, 20 runs.

**Statistics.** Occupancy (both definitions), support ⊆ V\*, coverage, class distribution, consensus; contract events
proposed / refused / installed by guard; transition matrix among classes; guard frequencies with run-level
uncertainty; efficiency reported, never a selector.

**Scale guard.** ≤ 3 workers; two sibling runs may use up to 3 each: check `ps` for their drivers before any
multi-worker step. If the KR fixed point fails to converge at δ = 0.99, report it and run δ = 0.95 instead.

## Required outputs

`src/farsighted_refusal.py` (+ `_run.py`, `_report.py`), `tests/test_farsighted_refusal.py` (g1 freezing set; the
KR fixed-point equations hold at the reported solutions; gKR-read equals gKR on monomorphic islands; g0 reproduces
D1 draw for draw), `notes/farsighted-refusal.md` (§1 static before any cell, §2 costs), `runs/farsighted-refusal.md`
and `.json`, predictions committed before any counted cell, and the usual hand-back (draft RESULTS, REJECTED,
THEORY §3 / DEFERRED 15 edits, NOTATION, ≤ 5 lines for the RS, branch, commits).

## RE predictions (with falsifiers)

1. **The one-step derived guard singles out nothing:** U-g1 freezes islands at their first pair outcome; occupancy at
   mN = 0 within 0.05 of the no-contract baseline's (0.28) plus the share of disagreement islands converted, and far
   below gV. *Falsifier:* U-g1 occupancy ≥ 0.6.
2. **Some KR fixed point has absorbing set exactly V\* at δ ≥ 0.9**, and others absorb on held-player unequal pairs
   [after review by sol: Anesi's protocol is not ours, so this is a bet, not an inference]. *Falsifier:* *certified*
   nonexistence of a V\*-absorbing fixed point at every δ ≤ 0.99 ("not found" by search is reported as such, not as a
   falsification).
3. **The default (myopic-start) fixed point is not the V\* one at δ = 0.9** (uncertain): at moderate patience
   members still accept unequal offers, so U-gKR(0.9) sits between D1 and gV. *Falsifier:* its absorbing set is
   exactly V\*.
4. **Where the static fixed point absorbs on V\*, the universal guard recovers the set on islands** (occupancy ≥ 0.9
   at mN = 0, modal ≥ 0.9 at mN = 1). *Falsifier:* occupancy ≤ 0.7 with the static absorbing set equal to V\*.
5. **gKR spreads like the hand-written veto:** in M-gKR its frequency is neutral at mN = 0 and rises in ≥ 0.8 of
   runs at mN = 1. *Falsifier:* it falls in ≥ 0.5 of runs at mN = 1.
6. **In C3 the hand-written veto and gKR coexist; g0 is lost** (both refusers rise; neither wins outright by 2,000).
   *Falsifier:* g0 above ⅓ at the horizon in ≥ 0.5 of runs.
7. ~~Reading pays in M-read~~ [withdrawn after review by gemini-4-argon: on an island of gKR and gKR-read only,
   both make identical decisions, so M-read is neutral by construction]. **Revised, on C3-read:** with g0 present,
   gKR-read rises against gKR at mN = 1 (uncertain). *Falsifier:* it falls in ≥ 0.5 of runs. **Gemini's
   counter-prediction (registered):** in M-read the two drift neutrally (kept as a sanity cell).
8. **The guard is cheap:** gKR-read costs ≤ 10⁵ evaluator steps per decision, so realizability is not the bind here.
   *Falsifier:* > 10⁶.

The RS is invited to add his own; the uncertain ones are 3 and 7.

## Amendments after review (gpt-6.1-sol and gemini-4-argon; these supersede the text above where they conflict)

1. **The process, written out (notes §1 before any computation).** Discounting advances on every contract event
   (each ν-event, null draws and refusals included); the flow payoff per event is the status quo's;
   W_i(y) = (1 − δ) u_i(y) + δ Σ_κ (1/27) [A(κ, y) W_i(x_κ) + (1 − A(κ, y)) W_i(y)], with A the joint consent of S
   under the policy. Refusal does not stop the clock. The status quo y on an island is its modal outcome, as in the
   dominance-contracts run.
2. **Equilibria are certified, not sampled.** Stationary Markov consent policies (one bit per state, dominating
   contract and S-member), with mixing allowed only at exact indifference. Existence and the full list of fixed
   points are established by exhaustive search with pruning or a constraint solver, with exact rational policy
   evaluation; the default-selection rule (the fixed point reached by iterating best responses from the myopic
   policy, with cycle detection) is frozen before any computation. Report each recurrent class, absorption
   probabilities from every outcome and from the seeded outcome distribution, hitting-time distributions, and the
   minimum consent margin (near-zero margins at δ = 0.99 flagged).
3. **gKR-read is a plug-in, lagged reader.** It treats every gKR and gKR-read copy as playing the default gKR policy,
   tallies each slot's consent probabilities from the island's current guard frequencies, and solves the 20-state
   linear system once per composition change. It is labelled as such, not as a mutual fixed point (the joint
   mixed-composition fixed point is the regress the RS's program must eventually face; sol's beyond-the-experiment
   point, recorded for DEFERRED 15).
4. **Realizability.** The guards run host-side here: an idealized oracle experiment. Cost is benchmarked separately
   by an executable implementation of the 20-state solve in the realizable evaluator (steps, precision, failure
   behaviour); prediction 8 is scored on that benchmark only.
5. **Cells added.** C3-read (gKR-read, gKR, g0 at ⅓ each, mN = 1) replaces M-read as the test of reading (M-read kept
   as a neutrality sanity cell). M-g1 (g1 against g0 at ½, mN = 1) and, if a certified fixed point absorbs on an
   unequal pair, M-gKR-unequal against g0: these separate generic caution from V\* geometry (does any guard that
   lowers churn spread equally fast?). Rare-invasion starts (gKR at 0.05 against g0, mN = 1). Forced starts at every
   outcome for U-gKR(0.99), separating recovery from persistence. The g1 "below x_i" variant runs as U-g1-x at mN = 0
   only if its static freezing set differs from g1's (the RE's check says it does not).
6. **Statistics added.** Guard–outcome association at founding and its trajectory (guard–play linkage), and the
   placement of guards across slots at the horizon.
