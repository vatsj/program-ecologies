# Predictions: what compute should cost, three pricing rules across three games, 2026-10-25

Spec `specs/2026-10-25-pricing-rules.md` (reviewed by gemini-4-argon, then gpt-6.1-sol in amended mode; both folded).
Hand derivations: `notes/pricing-rules.md` §1 (committed before any code, `9146608`). Written and committed before any
code of this run exists and before any counted cell. Everything here is an ε = 0 seed-lottery statistic at finite
(N, I, horizon) on fixed catalogues, never π and never a large-population claim. Scoring: held / failed / partial /
undetermined / not scored, each with the number, in `runs/pricing-rules.md` and `.json`.

## The RS's statements (2026-10-24; quoted in the spec)

1. "I'm comfortable with a capped simulator primitive. It's a bash command and we're aiming for Turing-completeness, so I
   see no principled reason to withhold it."
2. "One point in favor of A [a timed-out read pays the full cap] is that it points the finger more directly at the reason
   we need the restriction in the first place: infinite loops. I don't think I have an answer to your question [does
   'compute costs are nontrivial' mean every step should cost, or only wasted computation?]; I'm hoping we find
   experiments that answer the question for us (ie meaningfully inform it)."

The RE's reading: the experiment informs the RS's open question by a robustness criterion, not by a theorem. **A pricing
rule is better if one price level delivers every game's target at once, over a wide band of levels, and worse if each game
needs its own level.** The result is stated as robustness under these conventions (K, stakes, catalogues, the PD cost
model below), not as an intrinsic ranking of cost notions. Capped simulators are in every cell (the RS's ruling 1).

## Conventions fixed here (engineer, before any code), so no threshold can move afterwards

* **Rules** (as in the spec, with the ledger of `notes/pricing-rules.md` §1.0): F (c per step), A (P_fail per timed-out
  read call), F+A (c per step; each topmost timed-out call charged c·K in place of its subtree), B (c per step; a read
  call keyed on (issuer quote, read quote) is paid once per island lifetime at its first execution, later executions
  are free including their subtree). Controls: the zero price; the zero price is also the "timeout-free bounded
  simulator" control, because a read that returns a default after a small fixed budget without being a charged timeout
  is exactly an uncharged read (stated, not run separately); a constant per-read toll τ per read call (finishing or
  not) at τ ∈ {0.1, 1}; B with a pre-warmed cache against B with a cold cache (RPS).
* **Levels.** F, F+A, B at c ∈ {10⁻⁵, 10⁻⁴, 10⁻³, 10⁻²}; A at P_fail ∈ {0.01, 0.1, 1, 10}; zero price as the reference.
  **The complete cross-game panel**: every rule at c = 10⁻⁴ and 10⁻³ and A at P_fail ∈ {0.1, 1}, in all three games,
  runs before any optional cell. Optional, in the spec's cut order, cut last first: c = 10⁻² (all rules), B in
  inspection, F+A in inspection, PD at c = 10⁻⁵. Everything cut is disclosed in the report.
* **Cells.** RPS: full arm, 30 programs, r = 3, N = 100, I = 64, mN = 1, w = 0.3, 40 runs, generation 2,000 (4,000
  beside it), K = 10⁴, founders paired across rules. Inspection: full arm, fixed roles, N = 100 per role, I = 64, mN = 1,
  40 runs, same K. PD: the world-K S-nonself lottery at (N, I) = (100, 64), r = 100, 20 runs, generation 10,000 (stopped
  early only by the stored kernel's frozen test), founders as the stored `wk_Snon_100_64` cell. Dynamics seeds are the
  stored ones with the price replaced by a rule-and-level label, so the zero price reproduces the stored draws exactly.
  Larger geometry for any level that meets all three: RPS and inspection (N, I) = (400, 16), 20 runs; PD (200, 64), 20
  runs.
* **Targets and scoring.** RPS: the population's net exploitability e_prog (the best program's expected net payoff
  against the island's population, net of the rule's own charge; island mean, then run mean) ≤ 0.10. Inspection:
  the fraction of efficient islands (both roles' mean game payoff ≥ −0.05) ≥ 0.60. PD: the fraction of runs that are
  universal-open at generation 10,000 ≥ 0.70. Run-level 95% intervals (bootstrap over runs, 4,000 resamples; Wilson for the
  PD proportion). A target is **met** if the whole interval is on the good side of the threshold, **failed** if it is
  entirely on the bad side, **undetermined** otherwise. A joint band is the set of levels at which all three games are met;
  the **possible band** (reported beside it) is the levels at which no game is failed. Adjacent means adjacent in the rule's
  level grid.
* **Reported beside every target:** support and transition structure (resolved fraction, support unchanged 1,500 to
  2,000), non-play (forfeits), gross and net payoffs, PD P(C,C), the steps per encounter, the timeout frequency per play,
  the charge paid per encounter (raw and in stakes), the share of U (RPS) and of simulators.
* **Statics.** A fine grid (c from 10⁻⁶ to 10⁻¹; P_fail from 10⁻³ to 10²) on the exact tables of RPS and inspection:
  RPS: does a monomorphic `U` population resist invasion by every other program (net)? inspection: the fraction of
  efficient resident pairs that resist invasion in both roles.
* **PD cost model** (stated before the code; `notes/pricing-rules.md` §2 will give the numbers): the stored kernel has no
  play-step table, so a play costs 10 + one charge per atom of the unit's decision tree on the evaluated path, by the
  stored check outcome (no list: 101; true or false with a list between distinct quotes: 15,815; same quote: 9,513; against a
  constant quote: 2,415 for ⌜C⌝ and 245 for ⌜D⌝; TO: 250,006), a production act costs the stored medians (13,743 for
  C, 9,058 for D, 250,005 at the cap). The model is calibrated on the stored named-pair records and checked on executable
  plays where feasible; its error is reported.
* **Conjunctive rules.** A prediction with sub-claims is *held* if all sub-claims hold, *failed* if the stated falsifier
  trips, *partial* otherwise (*undetermined* when the intervals do not decide; *not scored* when a required cell was cut).

## Predictions (the RE's, verbatim from the spec; falsifiers in brackets), with scoring rules added by the engineer

1. *F has no joint band.* No c in the panel meets all three targets under F [some c does]. **Scoring:** held if every c
   in the panel has at least one game *failed*; failed if some c has all three *met*; undetermined otherwise.
2. *A has a joint band.* Under A, at least two adjacent P_fail levels meet all three targets [no adjacent pair does].
   **Scoring:** held if two adjacent levels each have all three games met; failed if every adjacent pair has a failed game at
   one of its levels; undetermined otherwise.
3. *A's mechanism.* Under A the RPS simulators lose to `U` at every P_fail ≥ 0.1, because a mutual simulation times out and
   pays P_fail [`U` below 0.5 at P_fail = 0.1]. **Scoring:** the share of `U` (run mean, interval) at each panel P_fail ≥ 0.1;
   held if ≥ 0.5 at all of them with the intervals above 0.5 at P_fail = 0.1, failed if the P_fail = 0.1 interval is below
   0.5. *Counter-prediction (gpt-6.1-sol), registered:* timeout-heavy simulators decline, but readers that finish (against
   `U`, against constants, or with bounded reads that do not time out) can keep RPS off its target. **Scoring:** held if at
   some P_fail ≥ 0.1 the RPS target is failed or undetermined while the timeouts per play have fallen to at most half of the
   zero-price value.
4. *B helps the PD and hurts the coin.* B keeps the PD target at c = 10⁻³ (repeated checks amortized), and in RPS it
   amortizes the simulators' reads too, so `U`'s share under B is at most its share under F at every c [B above F at some
   c by more than 0.1]. **Scoring:** PD target met at B, c = 10⁻³; and for each c of the panel, share_U(B) − share_U(F) ≤
   0.1 (point estimates; interval reported). *Counter-prediction (gpt-6.1-sol), registered:* subsidized reads change a
   frequency-dependent ecology, predators of simulators included, so `U`'s share need not be ordered against F's.
   **Scoring:** held if the ordering fails at some c in either direction by more than 0.1.
5. *F+A against F.* Charging timeouts at the cap widens F's RPS band downward (the coin wins at lower c) but leaves F's PD
   failure at high c, so F+A also has no joint band [F+A has one]. **Scoring:** the lowest panel c at which the RPS target
   is met under F+A is below F's; the PD target is failed at c = 10⁻³ under F+A; F+A has no joint band (the prediction
   fails if F+A has one).

## The engineer's own predictions (registered before any code)

E1. *The stored RPS dose is reproduced.* Under F, `U` holds at least 0.5 of the RPS lottery at c = 10⁻³ and below 0.5 at
    10⁻⁴ [the stored values were 0.91 and 0.09 at generation 2,000, 40 runs; falsifier: either side of 0.5 reversed].
E2. *The PD under F fails by arithmetic.* The PD universal-open fraction is below 0.35 at c = 10⁻⁴ and 10⁻³ under F
    [falsifier: ≥ 0.35 at either]. (A distinct-pair check costs 1.6 and 16 against stakes of 3.)
E3. *The PD under A is the zero-price PD.* Universal-open under A is within 0.15 of the zero-price value at every P_fail
    in the panel, because plays rarely time out [falsifier: a difference above 0.15 at some panel P_fail].
E4. *Inspection under A.* The efficient-island fraction is at least 0.6 at every panel P_fail: efficient islands are held
    by simulating inspectors against compliers and constants, and mutual simulations that time out are penalized, not the
    efficient path [falsifier: below 0.6 at some panel P_fail].
E5. *The pre-warmed cache is the zero price in the long run.* B warm and B cold differ by less than 0.1 in the RPS
    target statistic and the share of `U` at every panel c [falsifier: a difference above 0.1].
E6. *Joint band summary (the headline).* F has no joint band; A has the widest joint band (at least three of its four
    levels possible, two adjacent met); F+A and B each have a possible band narrower than A's. **Falsifier of E6:** A's
    possible band is narrower than B's, or A has no adjacent pair met (the latter is also prediction 2's falsifier).
E7. *The constant per-read toll τ* behaves like A in RPS (it charges the finishing reads as well) and breaks inspection
    at τ = 1 (efficient islands fall below 0.6), because the efficient islands are held by readers [falsifier: efficient
    islands at τ = 1 at least 0.6].
E8. *Which games bind.* Under F the PD binds at the high end of the panel (fails from c ≥ 10⁻⁴ upward) and RPS binds at
    the low end (fails below 10⁻³), so the two do not overlap; under F+A the PD binds harder than under F (K = 10⁶ makes a
    timed-out check cost c·10⁶) [falsifier: F+A's PD target met at a c at which F's is failed].

## Falsifier notes

What would change the program: if A had no adjacent pair met, the failure-only notion would not be robust here either, and
the question "every step or only wasted steps" would have no answer in this panel; if F had a joint band, the single-price
worry that motivated the experiment is not borne out; if B or F+A had bands as wide as A's, the distinction between the
notions would be one of degree. Every verdict above carries its number in the report.
