# An annealed mutation tail on the unequal basin of majority division (notes, 2026-11-01/02)

Spec `specs/2026-11-01-annealed-tail-dollar3.md` (queue 71; RS: "Go ahead w the annealing run"; reviewed by gemini-4-argon then
gpt-6.1-sol in `--mode amended`, both folded; the folded spec is the authority). Engineer: Claude Opus 5.5 subagent (the
launch message says Opus; the commits carry that trailer). Follows `notes/unequal-basin.md`. Results and tables are in
`runs/annealed-tail.md` and `.json`; the drafts for the shared documents are in `notes/annealed-tail-drafts.md`.
Every deviation from the spec is listed in section 2 and again in the report to the RE.

## 1. Order of work and what was written before any counted cell

1. I read the spec, both reviews, `notes/unequal-basin.md`, the queue-70 modules (`unequal_basin*.py`, `many_islands_t_ode.py`) and the
   RESULTS section "Where the unequal basin comes from".
2. `src/annealed_tail_static.py` computed the static numbers (restricted prior mass, offering / victim / bully masses, S3 invariance of the
   prior) with no ODE. `predictions/2026-11-01-annealed-tail.md` was written from them, with the RE's seven predictions as registered, the
   reviewers' counter-predictions (a)-(e) and seven engineer predictions E1-E7, and committed (c004eb4) before any validation run or counted
   cell. The predictions file also froze the scoring conventions (Lam* definition, the unbracketed-late rule for prediction 2, the
   operationalization of prediction 5, the moved-Lam=0-endpoint rule for prediction 6).
3. Validations V1, V2 (before the grid), V3 and V4 (after the first grid pilots were available; V3 needed the Monte Carlo extension), then the
   counted cells. Nothing counted was run before the predictions commit.

## 2. Deviations from the spec, choices where the spec was silent, and what changed the plan

**2.1 The grid was run as specified and then extended, because the specified grid gave no flip (the largest change).** On the specified
Lam grid {0.1 ... 300} nothing happens: every M and L endpoint equals the tail-free endpoint (V* 0.1004 / 0.9997 / 0 / 0, to 1e-5) and arm T keeps V* >= 0.99999.
So the specified bisections of Lam* have no bracket. I extended the grid, as disclosed additions that do not replace any specified cell:
- M natural at t0 = 100 (to Lam = 1e5) and t0 = 1 (to 1e4), and L natural at t0 = 1 and 100 (to 1e5), (L natural at t0 = 100 flips to U between 2.4e4 and 3.2e4: the harm
  threshold, bisected to a factor 1.33); M late tail at t0 = 1 and 100 to 1e5; arm T to 1e3 (and 1e4 once).
- The tail-composition ablations were bisected for **Lam\***, which required a bracket the full tail never gives. The ablations that flip M natural (victim-less, bully-less, both, constants-only)
  have Lam* in the tens to hundreds (RESULTS draft table); their Lam* are bisected to a factor 1.25 as the spec asks for (a) and (b), and for (c), (d).
- Clean-tail (victim- and bully-less) Lam* at t0 = 1 and 1e4, the same tail at the deep tilts L / M u = 0.6 (t0 = 1 and 100, bisected to a factor 1.25), and victim-less Lam* at N = 200 / 400 (bisected to 1.25 at N = 200, 1.155 at N = 400), to carry the early/late, deep-ratchet and N tests
  (predictions 2, 7, 6 and reviewers (c), (d)) that the full tail leaves vacuous.

**2.2 Numerics: the explicit phase runs to 4e4 events, not 1e4.** Queue 70's integrator is explicit to 1e4 and backward Euler after. For M natural the F -> U transition
sits at 1.2e4 events; the first backward-Euler step there (h = 3.3e3) falls on a spurious root and the halving cascade cost more than eight minutes per
step. I use explicit DOP853 to 4e4 events (the transition is over by 2e4), then backward Euler on a decade lattice 10^(k/8) with a fail-fast Newton (inexact GMRES, rtol 1e-4;
the residual must contract after two iterations or the step is halved). The tail's dose is delivered exactly: on each backward-Euler step the mean tail rate is the exact integral of eps over the step divided by h.
The two first rows computed with queue 70's settings (explicit to 1e4) are kept in `runs/annealed_tail/rows_old_numerics/`: M natural Lam = 0.1 and 0.3, t0 = 100: V*/U identical to 1e-6 with the new settings. The ablation bracket points were rerun at rtol 1e-10 and half the
backward-Euler step (spd 16): all eight endpoints reproduce (report table).

**2.3 V3 gate at 1e4 events not met, and why.** The spec's V3 compares V* at 1e2, 1e3, 1e4 events within 0.02. At 1e2 and 1e3 the agreement is <= 0.012 (I = 4,096) and <= 0.001 (I = 16,384).
At 1e4 it fails (0.20 at Lam = 10; **0.62 at Lam = 0**): M natural is on a sharp F -> U transition at 1.2e4 events in object P, and the full-dynamics chain makes it earlier (0.36 / 0.26 at 1e4
tail-free), so the 1e4 point measures transition timing (object P against the full chain), not the tail kernel. The tail-free control fails identically. That timing difference between object P and the
full chain is itself a caveat on object P that queue 70 did not see (its V3 stopped at 3e3). To test what matters I added V3b: the central contrast (victim-less tail flips M, full tail does not, Lam = 300, t0 = 100) against the full-dynamics chain
with no truncation, I = 8,192, two worlds each, to 4e4 events.

**2.4 Late-arm start.** "t_s = 1e6 events" is the tail-free object's own state at tau = 1e6 (stored by the tail-free run at V* 0.10040, U 0.89952, G 8e-5), not its endpoint (V* 0.10041, U 0.89959). The tail clock
tau restarts at 0. The "baseline-zero" rerun is vacuous: at t_s the donor marginal of every offering constant and of the exit constant in slot 0 is <= 3e-17 (only the (ALL, 1/3) constant is at 1e-4).
The exponent fit on Lam in {0.01, 0.03, 0.1, 0.3} (against a Lam = 0 run from the same state): at t0 = 1 the response is exactly linear in Lam (log-log slope 1.001, 3.05e-10 of V* per arrival), at t0 = 100 and 1e4 it is below the stop tolerance (offsets <= 8e-6 from the stop rule); the rescued U mass is ten orders below anything that matters.

**2.5 Attribution is by direct class flux.** The pre-registered convention (predictions file) scores prediction 5 on (i) the direct tail flux by class transition, arrival role and family, and (ii) the U -> F flux by the excluded slot's program in the source state.
Both are computed with an exact kernel (class-changing Moran flux from sources grouped by payoff level, class, role, category; tested against the field). I did not build the counterfactual "tail-generated supply" decomposition: with no
rescue there is nothing to decompose, and for the victim-less tail the direct tail flux is within about 10% of the full tail's while the endpoints are opposite (attribution rows), so direct flux cannot assign the effect. The causal evidence is the matched-dose ablations.

**2.6 Ablation conventions.** Primary ablations are matched-dose (the removed prior mass becomes null events, remaining families keep their dose); renormalized versions are run at Lam = 100 as secondary (all four give the same class as the matched-dose version). "Victims" are the two constants that name a slot partner at 1/3
(mass 0.2169 per slot; the spec's 0.108 is one of them). "Bullies" are the two `exploiter-fair` programs per slot. "(d) constants only" removes all 1,240 conditionals of the support.
Ablation (a)-(d) were bisected at t0 = 100 only; the clean tail also at t0 = 1 and 1e4.

**2.7 N scaling** is the hybrid object: fixation table at N, migration and tail both, founding law of N = 100. The tail-free endpoint of M natural moves with N (V* 0.1004, 0.0580, 0.0325 at N = 100, 200, 400); Lam* is reported for the victim-less tail (the full tail has none). The "single-island neutral entry per arrival" is the closed form 1/N (0.01, 0.005, 0.0025), checked by V4's neutral strata at N = 100 (z within 1.6); I did not repeat the island simulation at N = 200, 400.

**2.8 Cell 8.** The S3-asymmetric perturbation is applied to **two** endpoints: the rescued endpoint (M natural, victim-less tail, Lam = 100, V* 1.0000) and, for comparison, L's tail-free fair endpoint; integrated tail-free without projection to 1e6 events (no early stop) at delta = 1e-6 and 1e-3.

**2.9 Object variants (6b).** The "m = 1 on the 48-conditional core" object is built as constants + the core's 48 conditionals per slot with at most one conditional per island (12,393 states; 6.4% of the start law is dropped), and "m = 1 over every conditional" is queue 70's (302,049 states). Both end fair tail-free (M natural V* = 1.0), as queue 70 found for m = 1; so the contrast with object P is the m, not the core, and the tail does not move either m = 1 object.

**2.10 Early classification** was not used (no `early` flag in any counted row). Rows classified through the burst protocol (the tail still delivering > 1e-4 arrivals per island when criterion (a) held) carry protocol "burst" and a star in the tables; the burst continuation (the remaining dose delivered at once) and the tail-free continuation agree in every row, so none is unresolved.

**2.11 Cuts.** None. The t0 = 1e4 columns of the main grid ran for all four DSL starts; the late arm ran at t0 = 1, 100, 1e4; 6, 6b and 8 ran.

## 3. Process incidents (disclosed)

- An early ad-hoc profiling script imported numpy before the thread-limit environment variables were set and ran at about 970% CPU for roughly ten minutes before I noticed and killed it by pid. No result of it is used.
- A chain script launched two extra workers for about three seconds (five processes in total) before I killed them by pid; they had taken locks on two jobs which I removed.
- Twice I killed all workers mid-job to reprioritize the queue (losing at most 10 minutes of three processes); the job files are append-only plans and finished rows are keyed by the job spec, so nothing was recomputed except the killed in-flight jobs.
- Two N = 200 / 400 `late0` jobs initially stored an empty state (the tail-free run had converged before tau = 1e6); fixed (the endpoint is the state at t_s when convergence precedes 1e6) and rerun.
- The rows for M natural t0 = 100 at Lam = 0.1 and 0.3 were computed with queue 70's numerics, then recomputed with the new numerics; both kept.

## 4. What the tail did, in one paragraph

At every dose on the specified grid, at every dose tested beyond it (M natural to 1e5 at t0 = 100 and 1e4 at t0 = 1; the late tail to 1e5), the **full** tail leaves M's endpoint exactly the tail-free one. The tail is not inert: a strong early tail drives a tail-dominated quasi-state (F 0.375, U 0.59) and the approach is slowed or reshaped,
and at Lam about 3e4 and t0 = 100 it carries the **fair** arm L into the unequal state. What decides the outcome is the tail's own composition: matched-dose removal of the two 1/3 constants (0.217 of the tail) turns the endpoint to V* = 1.0000 at Lam* in (75, 87], removing victims and bullies at (48.7, 56.2], removing only the two bullies (mass 3.7e-5) at (274, 316], removing every conditional at (750, 866]. The flips are step functions of Lam, survive 10x tighter tolerance and half step, and the central contrast is reproduced by the full-dynamics chain. The direct tail flux is two orders of magnitude below the migrants' class flux and nearly identical for the full and victim-less tails: the effect is a knife-edge in the donor composition that migration amplifies.
