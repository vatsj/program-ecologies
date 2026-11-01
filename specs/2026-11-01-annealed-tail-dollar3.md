# Spec: an annealed mutation tail on the unequal basin of majority division, islands → ∞ before time, 2026-11-01

Status: draft by the RE; to be reviewed by gemini-4-argon (folded [after review]), then gpt-6.1-sol (`--mode amended`,
folded [after second review]); to be run by a Sonnet subagent. Queue 71. Agreed by the RS:

> RS (2026-11-01), after the RE pointed out that queue 70 was run without the tail the object keeps: "Go ahead w the
> annealing run"

and, on the object, the RS's correction of the tracker the same day: "I thought we were keeping the eps -> 0 'mutation
tail' as a means of trickling in predators?" (DEFERRED 1: the annealed tail, 2026-10-16/17; tracker rows h01, h03).

## Context

The stable-set target (DEFERRED 15; tracker h11): in majority division every island lands in V\* (the three fair
pairs), each member equally likely across worlds. Its stated object is lim_t lim_I of the rare-migration chain **after
an annealed tail**. Every infinite-island run so far (queues 65, 69, 70) was tail-free: ε = 0 after founding.

RESULTS "Where the unequal basin comes from" (queue 70, 2026-10-31) found, in that tail-free object:
- the nine constants have an unequal basin with boundary u\* ≈ 0.69 (u = the unequal share of a within-class tilt of
  the natural start);
- the length prior's two Trojan bullies per slot (`exploiter-fair`: name j at ⅔ if j names me demanding ⅓, else name k
  at ½; seed mass 3.7·10⁻⁵ per slot) pull u\* to 0.55 (L) and 0.425 (M), just under M's natural 0.429, so M's natural
  start ends at V\* 0.10 / U 0.90 (metastable; class-changing eigenvalues −3.6·10⁻³ / −2.3·10⁻³);
- each outcome is a ratchet: on U islands the ½-offerers fall to 10⁻¹⁷, on fair islands the ⅓-demanders do, and at
  ε = 0 nothing re-supplies them;
- arm T (27 L_T^code programs) shows no crossing up to u = 0.95.

The ratchet is an ε = 0 statement. A tail re-supplies both depleted sides: the excluded-slot offerers that let an
underpaid member leave U, and the victims and bullies that carry fair islands into U. This experiment asks which wins.

**A structural point the run should check.** In the PD the RS's admissibility rule for the tail ("drift should never
colonize an island, only reintroduce fit programs") separates by N: drift colonizations fall with N while selected
predator cures do not (RESULTS "Annealed mutation"). Here both directions start with a neutral step (constants-only
analysis, `notes/unequal-basin.md` §1.3–1.4):
- U → V\*: the excluded slot E drifts (fixation 1/N) to a constant offering ≤ ½ to the underpaid member Lw, then Lw's
  switch is selected (+⅙, 4.9× neutral);
- V\* → U: a Trojan bully enters neutrally where its fallback is the island's fair pair, then a victim's arrival is
  selected for the bully (+⅙), or a victim enters at −⅙ (0.035 of neutral).
So if these paths dominate, the tail's per-arrival effect in both directions scales as 1/N at large N and the RS's
window does not separate them; the net direction is set by the prior's composition. [after second review] Competing
deleterious paths exist on both sides (a victim entering a fair pair at −⅙; H conceding out of U at −⅙, 0.035 of
neutral at N = 100) and are suppressed as e^(−wN/6); the run enumerates the paths and computes their rates separately
rather than assuming the neutral bottleneck. The prior is about 97.6% constants (`notes/unequal-basin.md`
§1.4), and the constants' boundary is 0.69, so the RE expects the tail to push toward V\*.

REJECTED.md checked: nothing re-opened. The nearest entry ("An annealed tail of three founders restores at least 60% of
islands", auctions, RESULTS "Rediscovering the core") is a different game and a finite-I island model.

Why it matters for the long-term goal: if a vanishing tail of prior arrivals undoes the length prior's unequal basin,
the DSL arms' failure of the stable-set target is a property of the tail-free object, not of the library; if it does
not, a realizable library must keep Trojan-bully mass below the prior's fair-reader mass even with re-supply.

## The object

Exactly queue 70's object (`specs/2026-10-31-unequal-basin.md`, `notes/unequal-basin.md`, `src/unequal_basin*.py`), plus
a tail:

- **Game, arms, founding.** `dollar3`, N = 100, w = 0.3, payoffs in dollars. Arms L (weak evaluator, length prior, n ≤ 6)
  and M (modalPA, same law) at A = 0, P_fail 0 (queue 70's primary cells), on queue 70's founding pools (scratchpad
  `ub/pools`; rebuild with `unequal_basin_core.build_pool2` if absent, same seeds). Arm T (27 programs, main dose,
  P_fail 0.1 and 0) on queue 69's pools with `src/many_islands_t_ode.py`.
- **Truncation (L, M).** Object P: the reflecting m-truncation, m = 3 on queue 70's 48-conditional core, all constants
  in every slot. A migration or tail arrival that would leave the state set is a null event; report its flux as
  blocked flux, separately for migrants and tail arrivals.
- **Tail.** After founding (t = 0 is the post-anneal, post-relaxation law), prior arrivals per island at rate ε(t) per
  migrant event, each to a uniformly random slot, the program drawn from that slot's founding prior (the arm's seed law;
  for arm T the dose's founding library law), fixing with the same closed-form Moran kernel as a migrant against the
  island's current triple. Since the migration field G(x; q) is linear in the donor law q,

      dx/dt = G(x; q(x)) + ε(t) · G(x; p),

  with q(x) the slot marginals and p the prior restricted to the state set's programs. Prior mass on programs outside
  the state set (the conditionals outside the core) gives null events; report the restricted mass per slot.
  [after review] Both x(0) and p are S₃-symmetrized and `field` is called with `sym=True` throughout (queue 70 found
  the unsymmetrized pool-0 law ending at U 1.0 where the symmetrized start ends at V\* 0.9997); check that p restricted
  to the state set is S₃-invariant to 10⁻¹².
- **Schedule.** ε(t) = (Λ/t₀)·(1 + (t − t_s)/t₀)^(−2) for t ≥ t_s, 0 before, so Λ is the total number of tail arrivals
  per island and t₀ sets how early they come. t_s = 0 (the tail starts at founding) except in the late arm.
- **Statistics.** As queue 70: class shares V\* / U / W / D / grand by events per island at the checkpoint grid and at
  the milestones t − t_s = 10⁴, 10⁵, 10⁶, 10⁷ [after review], the endpoint (convergence criterion of queue 70, after the
  tail's remaining arrivals ∫_t^∞ ε = Λ/(1 + (t − t_s)/t₀) fall below 10⁻⁴ per island [after review: 10⁻⁶ forced
  t ≈ 3·10¹² at Λ = 300, t₀ = 10⁴]; integration capped at t − t_s = 10⁸, reporting the remaining tail where the cap binds; [after second review] capped
  runs are *censored*, not endpoints: continue each tail-free from the cap, and once more with the remaining dose
  delivered at once, and classify only if both agree; unresolved Λ\* brackets are reported as such),
  support and transition structure at the endpoint (discipline 4), Λ\* where defined.

## Design

1. **Validation (before any counted cell).**
   - V1: Λ = 0 reproduces queue 70's stored endpoints (L natural V\* 0.9997; M natural V\* 0.1004 / U 0.8996; M and L
     unequal tilt u = 0.6) and queue 69's arm-T natural endpoint, to 10⁻⁴.
   - V2: linearity, G(x; a·q₁ + b·q₂) = a·G(x; q₁) + b·G(x; q₂) to 10⁻¹², and mass conservation of the full field with
     the tail.
   - V3: the tail kernel against simulation. Extend `src/unequal_basin_mc.py` (the matched truncated Monte Carlo) with
     prior arrivals; at I = 4,096 and one cell (M natural, t₀ = 10², Λ = the smallest flipping value found in a pilot,
     or 10 if none), compare V\* at 10², 10³, 10⁴ events, 4 worlds; agreement within 0.02.
   - V4: a single-arrival assay on the two key triples (a U triple and a fair triple of M's endpoint support): the
     fixation of each prior program as computed by the field against direct Moran simulation (10⁵ draws per stratum,
     strata by payoff difference), |z| < 3.
2. **Main cells (counted).** Arms M and L, natural start and the unequal tilt u = 0.6; arm T natural and u = 0.8.
   [after review] Read the early columns (t₀ ≤ 10²) as a boundary-perturbation test: the tail acts before the ratchet
   settles (≈ 10⁴ events), and M's natural start is 0.004 in u inside its basin, so a small Λ\* there may only move the
   effective start across u\*. The M u = 0.6 start (0.175 inside) and the late arm (3) are the ratchet-rescue tests.
   - t₀ ∈ {1, 10², 10⁴} events per island (early, matched to the tail-free approach time, late);
   - Λ ∈ {0.1, 0.3, 1, 3, 10, 30, 100, 300};
   - endpoint class shares for each (arm, start, t₀, Λ); Λ\*(t₀) = the smallest Λ whose endpoint has V\* ≥ 0.5,
     bisected in log Λ to a factor 1.25 where the scan brackets one.
3. **Late tail.** Start from M's tail-free endpoint (t_s = 10⁶ events, V\* 0.10) with t₀ ∈ {1, 10², 10⁴}, same Λ grid:
   can a tail undo a settled ratchet, and at what Λ compared with the early tail? [after review] Report the donor
   marginal mass at t_s of the excluded-slot offering constants and of the underpaid member's exit constant (the
   constant naming E at ½), and estimate the small-Λ response directly [after second review: event labels cannot assign the
   scaling, since migrants from tail-rescued islands are themselves order Λ]: fit the exponent of the late tail's
   rescued U mass against Λ on Λ ∈ {0.01, 0.03, 0.1, 0.3} (added for this arm), separating a baseline donor supply
   (present at t_s) from tail-generated supply by rerunning with the baseline offering and exit-constant marginal mass
   set to zero at t_s.
4. **Constant rain control.** ε constant at Λ/10⁴ on [0, 10⁴], then 0; same Λ grid, M natural only. Separates the
   schedule's shape from the total.
5. **Attribution.** For M natural at t₀ = 10² and Λ = Λ\* (or Λ = 100 if none): the integrated tail-induced flux by
   transition type (U → V\*, V\* → U, into and out of W and D), and by the arriving program's family (offering
   constants, victims (⅓-demanding constants), Trojan bullies, the other exploiters, fair readers, other); and three
   tail-composition ablations, the tail drawn from the prior with (a) the Trojan bullies removed, (b) the victims
   removed, (c) both, (d) constants only [after review]; founding unchanged. [after second review] Primary
   ablations are matched-dose: the removed prior mass becomes null events, so the remaining families keep their dose;
   renormalized versions are secondary. For (a) and (b), bisect the ablated Λ\* as in cell 2, so prediction 5's
   threshold ratios are measured, not read off one Λ.
6. **N scaling of the tail (secondary).** Recompute the fixation kernel at N = 200 and 400 (founding law unchanged: a
   hybrid object, disclosed as such) and find Λ\*(t₀ = 10²) for M natural. [after second review] Changing N changes the
   migrant dynamics as well as the tail's fixation: report the Λ = 0 endpoint and the distance to u\* at each N, add the
   late-tail Λ\* at each N, and a single-island assay of the neutral entry probability per arrival at each N. Tests the structural point: if both
   directions start neutral, Λ\* in arrivals should grow ∝ N.
6b. **Full-conditional check [after review; design per the second review].** One point (M natural, t₀ = 10², Λ = Λ\*
   or 100 if none) on three objects: object P, the m = 1 object on the 48-conditional core, and the m = 1 object over
   every conditional (queue 70's full-conditional object). The first contrast isolates m, the second the core, so a
   disagreement names its cause. Report blocked flux for each.
7. **Arm T at the high-tail end.** At Λ = 300, t₀ = 1, the endpoint V\* of arm T (natural and u = 0.8): a tail heavy
   enough to remake the composition must not cost arm T the target.

8. **Numerical and symmetry checks [after second review].** At the two grid points bracketing Λ\* for M natural
   (t₀ = 10²): rerun with tolerances 10× tighter and the backward-Euler step halved; the endpoint class must not change.
   At one rescued endpoint, apply an S₃-asymmetric perturbation of size 10⁻⁶ and 10⁻³ (one fair pair up, one down) and
   integrate tail-free with `sym=False` for 10⁶ events: report whether V\* holds and which pair grows.

**Cut order** (cut from the end if the budget binds): 6, the N = 400 point of 6, 6b, the t₀ = 10⁴ column of 3, the u = 0.8
start for arm T, the Λ = 300 column outside cell 7. Report every cut.

**Budget.** 3 workers. Queue 70's runs took about 1–20 minutes per trajectory on object P; the main grid is about
150 trajectories plus bisections. If a trajectory exceeds 1 hour, stop and report rather than truncating further.

## Required outputs

- `runs/annealed-tail.md` and `.json`; rows under `runs/annealed_tail/`; `notes/annealed-tail.md` (the engineer's
  notes, including every deviation from this spec, disclosed in the report, not only in the notes).
- Tables: endpoint V\* / U / W / D by (arm, start, t₀, Λ); Λ\*(t₀) per arm and start; the late tail and constant rain
  tables; the attribution flux table and the ablation endpoints; Λ\*(N); arm T's high-tail endpoints.
- Endpoint support and transition structure for M natural at Λ just below and just above Λ\*.
- The tail's restricted mass per slot (prior mass outside the state set) and blocked flux.
- Drafts for RESULTS, REJECTED (every failed prediction, the RE's and the engineer's), THEORY if a claim moves, NOTATION
  for Λ, t₀, t_s.

## Predictions (RE), with falsifiers

1. **The tail pushes toward V\*.** For M natural at t₀ = 1 and 10², there is Λ\* ≤ 30 above which the endpoint has
   V\* ≥ 0.99, and V\* at the endpoint is non-decreasing in Λ on the grid. *Falsifier:* no Λ ≤ 30 reaches V\* ≥ 0.99 at
   either t₀, or the endpoint V\* falls below the tail-free 0.1004 at any Λ on the grid; [after second review] every
   decrease of endpoint V\* between adjacent grid points by more than 0.01 is scored as a monotonicity failure. (0.6)
2. **Early beats late.** Λ\*(late, t_s = 10⁶) ≥ 10 · Λ\*(t₀ = 1). The settled ratchet has depleted the excluded-slot
   offerers, so a late tail must rebuild a rescue supply the early tail only has to tip. *Falsifier:* the ratio is below
   10, or the late tail flips M at a Λ where the early one does not. (0.65)
3. **Shape matters less than total.** For M natural, constant rain over [0, 10⁴] and the annealed t₀ = 10² tail have
   Λ\* within a factor 3. *Falsifier:* a ratio above 3. (0.55)
4. **No harm to the fair arms.** L natural and arm T (natural and u = 0.8) end with V\* ≥ 0.999 at every Λ and t₀ on
   the grid, cell 7 included. *Falsifier:* any endpoint below 0.999. (0.7)
5. **The rescue is carried by excluded-slot offering constants.** In the attribution cell, offering constants arriving
   in the excluded slot of U triples carry ≥ 0.7 of the tail-induced U → V\* flux, and victims (with bullies) carry
   ≥ 0.7 of the tail-induced V\* → U flux. [after review: the RE's draft predicted that removing the bullies from the
   tail lowers Λ\* by 2×; gemini-4-argon's objection holds statically, the tail's bully mass is 6,000 times below its
   constant mass, so the bullies act through the founding law and migrants, not the tail.] Removing the bullies from
   the tail moves Λ\* by less than a factor 1.25; removing the victims lowers it by at least 1.5×. *Falsifier:* either
   share below 0.7, the bully ablation moving Λ\* by 1.25× or more, or the victim ablation by less than 1.5×. (0.5)
6. **Both directions start neutral, so Λ\* grows with N.** Λ\*(400)/Λ\*(100) ∈ [2.5, 6] at t₀ = 10². *Falsifier:* a
   ratio outside that interval, or no Λ\* at N = 400 on the grid. (0.45)
7. **The unequal tilt of L.** L at u = 0.6 (tail-free U 0.9949) flips to V\* at Λ\* ≤ 10 for t₀ = 1: L's boundary (0.55)
   is closer to its start than M's settled state is to its boundary. *Falsifier:* Λ\* > 10 or none. (0.55)

**Reviewer counter-predictions (recorded, scored).** gemini-4-argon: (a) the bully tail ablation changes Λ\* by less
than 1.05× and the victim ablation lowers it by ≥ 1.5×; (b) Λ\*(400)/Λ\*(100) < 2.5 for the early tail, because larger N
suppresses the deleterious victim entries (−⅙) that feed V\* → U, while the late tail scales ∝ N.

gpt-6.1-sol: (c) early M-natural rescue is substantially easier than deep-U rescue (M u = 0.6, late arm), and the
prior's constant share alone will not predict the latter; (d) no clean proportional scaling of Λ\* across the three N;
(e) monotonicity in Λ is not guaranteed, since arrivals supply both rescue and exploitation.

The RS is invited to add predictions; the RE will ask him whether the tail flips M at all.

## Notes for the engineer

- Reuse, do not edit, queue 70's modules: write `src/annealed_tail*.py` importing `unequal_basin*` and
  `many_islands_t_ode`. The field `unequal_basin.field(obj, x, sym, q)` already takes the donor law, so the tail is a
  second call with q = p restricted to the state set; check linearity (V2) before relying on it.
- Integrate with the stiff integrator queue 70 used past 10⁵ events (`integrate_be`); the tail's early phase at t₀ = 1
  is fast, so use a fine explicit grid on [0, 10t₀].
- Never print, read or source `.env`. Do not commit `.npz`, `.pkl` or large `.npy` files; pools stay in the scratchpad.
  At most 3 workers. Kill only your own processes, by pid. No `timeout` or `setsid`.
- Write `predictions/2026-11-01-annealed-tail.md` from this spec (with the static numbers you compute first: restricted
  prior mass, the prior's offering and victim masses per slot) and commit it before any counted cell.
