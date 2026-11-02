# Predictions: an annealed mutation tail on the unequal basin of majority division (queue 71, 2026-11-01)

Committed before any counted cell and before any validation run of this experiment. Spec
`specs/2026-11-01-annealed-tail-dollar3.md` (reviewed by gemini-4-argon, then gpt-6.1-sol in `--mode amended`, both
folded; the folded spec is the authority). The static numbers below come from `src/annealed_tail_static.py`
(`runs/annealed_tail/static.json`); no ODE of this experiment had been run when this file was written.

## The RS's message

> RS (2026-11-01), after the RE pointed out that queue 70 was run without the tail the object keeps: "Go ahead w the
> annealing run"

## Static numbers (computed first)

Arm L / M (same law in every slot; the tail law p is the founding prior, S3-invariant to 0.0 exactly, p restricted to the
state set S3-invariant to 0.0 exactly, support and core S3-closed):

| quantity | value (per slot) |
|---|---|
| prior mass of the nine constants | 0.9760 (0.10844 each) |
| prior mass per canonical conditional | 1.85 × 10⁻⁵ (1,296 of them, 0.0240 together) |
| mass of conditionals in the S3-union support (1,240 of 1,296) | 0.02299 |
| mass of conditionals in the 48-core | 8.9 × 10⁻⁴ |
| mass of conditionals in the support but outside the core | 0.02210 (null events when the island already holds a conditional) |
| mass outside the union support entirely (null events always) | 1.04 × 10⁻³ |
| mass restricted to the state set of object P (support programs) | 0.99896 |
| offering constants of slot E toward a given Lw (name Lw at ⅓ or ½) | 2 constants, 0.2169 |
| exit constant of Lw toward a given E (names E at ½) | 1 constant, 0.1084 |
| victim constants (name a slot partner at ⅓), either partner | 2 constants, 0.2169 (0.1084 for a given H) |
| Trojan bullies (`exploiter-fair`) | 2 programs, 3.707 × 10⁻⁵ |
| other `exploiter` / `yielder` / `fair-reader` families | 16 programs each, 2.97 × 10⁻⁴ each |
| ratio offering constants : bullies | 5,850 : 1 (one constant : bully family 2,925 : 1) |

Arm T, main dose: 27 programs in every slot, all in the state set (restricted mass 1.0): nine constants 0.9 (0.1 each),
eight single readers 0.06, eight two-atom readers 0.03, two exploiters 0.01.

First-order per-arrival yields in a settled U island (N = 100, w = 0.3, from the 1/30-dollar fixation table): an arrival
is an offering constant in the excluded slot with probability ⅓ × 0.2169 = 0.0723, fixing neutrally (0.01): 7.2 × 10⁻⁴
per arrival; the second step, Lw's exit constant arriving in slot Lw once E offers, has probability ⅓ × 0.1084 = 0.0361
and fixes at +⅙ (0.0491): 1.8 × 10⁻³ per arrival. In a settled fair island the direct tail supply of bullies (neutral,
~10⁻⁷ per arrival) is negligible against the victims' (−⅙, 0.035 of neutral: ~2.5 × 10⁻⁵ per arrival), and a ⅓-victim
beside a fair half-demander is a wasteful pair (class W), not U.

## Scoring conventions (frozen before any run; the spec silent or open)

- **Endpoint class.** "V\*" is the F share (the three fair pairs); "endpoint" is the spec's converged state under the
  convergence criterion of queue 70 and a remaining-tail dose below 10⁻⁴ per island, or the censored protocol (spec: capped
  runs continued tail-free and with the remaining dose delivered at once, classified only if they agree). A run whose
  criterion-(a) state arrives while the remaining dose is still above 10⁻⁴ is checked by the burst continuation alone (the
  tail-free continuation is the state itself); this is a stated implementation choice, reported if it ever matters.
- **Λ\*(t₀)** = the smallest Λ whose endpoint has V\* ≥ 0.5, bisected in log Λ to a factor 1.25 where the scan brackets
  one on the grid; "none" if no grid value reaches it; "0" if the Λ = 0 endpoint already does.
- **Prediction 2 with an unbracketed late Λ\*.** If no Λ ≤ 300 flips the late arm, the ratio is scored as ≥ 300/Λ\*(early):
  held iff Λ\*(t₀ = 1) ≤ 30 (the ratio is then above 10), failed otherwise.
- **Prediction 4** is scored on L natural and arm T natural and u = 0.8 at P_fail 0.1 and 0, every grid Λ, every t₀, and cell
  7; the L u = 0.6 start is not in its scope (it is the rescue test of prediction 7).
- **Prediction 5 operationalization.** "Tail-induced flux" cannot be assigned from class-to-class events of the direct tail
  alone (a neutral arrival in the excluded slot does not change the island's class, the class change is Lw's selected switch,
  by migrant or by tail). So the score uses two measured quantities, both reported: (i) the direct tail flux by class
  transition, arrival slot role and arriving family; (ii) the whole U → V\* (and V\* → U) class flux of the tail run,
  decomposed by the family of the excluded slot's program (offering constant or not) in the source state, with the
  difference to the tail-free run's flux. The shares are scored on (ii) integrated over the tail window t ≤ 100 t₀ + 10⁴;
  the ablation Λ\* ratios are the causal check. An empty denominator (no tail-induced flux in a direction) scores the
  clause "unscorable".
- **Prediction 6 with a moved Λ = 0 endpoint.** Changing N changes the migrant dynamics too. If the Λ = 0 endpoint of M
  natural at N = 400 is already V\*-dominated, Λ\*(400) is "0" and prediction 6 fails (ratio outside the interval); the
  same at N = 200 is reported and does not enter the ratio.
- Verdicts: held / failed / partial (stated parts) / unscored.

## The RE's predictions (spec), as registered

1. **The tail pushes toward V\*.** For M natural at t₀ = 1 and 10², there is Λ\* ≤ 30 above which the endpoint has V\* ≥
   0.99, and V\* at the endpoint is non-decreasing in Λ on the grid. *Falsifier:* no Λ ≤ 30 reaches V\* ≥ 0.99 at either t₀,
   or the endpoint V\* falls below the tail-free 0.1004 at any Λ, or any decrease of endpoint V\* between adjacent grid
   points by more than 0.01. (0.6)
2. **Early beats late.** Λ\*(late, t_s = 10⁶) ≥ 10 · Λ\*(t₀ = 1). *Falsifier:* ratio below 10, or the late tail flips M at a Λ
   where the early one does not. (0.65)
3. **Shape matters less than total.** For M natural, constant rain over [0, 10⁴] and the annealed t₀ = 10² tail have Λ\*
   within a factor 3. *Falsifier:* a ratio above 3. (0.55)
4. **No harm to the fair arms.** L natural and arm T (natural and u = 0.8) end with V\* ≥ 0.999 at every Λ and t₀ on the
   grid, cell 7 included. *Falsifier:* any endpoint below 0.999. (0.7)
5. **The rescue is carried by excluded-slot offering constants.** Offering constants in the excluded slot of U triples carry
   ≥ 0.7 of the tail-induced U → V\* flux, victims (with bullies) ≥ 0.7 of the V\* → U flux; removing the bullies from the
   tail moves Λ\* by less than 1.25×; removing the victims lowers it by at least 1.5×. *Falsifier:* either share below 0.7, the
   bully ablation moving Λ\* by 1.25× or more, or the victim ablation by less than 1.5×. (0.5)
6. **Both directions start neutral, so Λ\* grows with N.** Λ\*(400)/Λ\*(100) ∈ [2.5, 6] at t₀ = 10². *Falsifier:* ratio outside,
   or no Λ\* at N = 400 on the grid. (0.45)
7. **The unequal tilt of L.** L at u = 0.6 (tail-free U 0.9949) flips to V\* at Λ\* ≤ 10 for t₀ = 1. *Falsifier:* Λ\* > 10 or
   none. (0.55)

## Reviewer counter-predictions (recorded, scored)

- gemini-4-argon (a): the bully tail ablation changes Λ\* by less than 1.05× and the victim ablation lowers it by ≥ 1.5×.
- gemini-4-argon (b): Λ\*(400)/Λ\*(100) < 2.5 for the early tail (t₀ = 10²).
- gpt-6.1-sol (c): early M-natural rescue is substantially easier than deep-U rescue (M u = 0.6, late arm), and the prior's
  constant share alone will not predict the latter. Scored: Λ\*(M natural, t₀ = 10²) smaller than Λ\*(M u = 0.6, t₀ = 10²)
  and Λ\*(late) by at least a factor 3, and the constants-only tail (ablation d) failing to reproduce the late arm's Λ\*
  within a factor 2 (or the late arm having none).
- gpt-6.1-sol (d): no clean proportional scaling of Λ\* across the three N: the three Λ\*(N) are not within 25% of
  a power law Λ\* ∝ N^β through the three points (the middle point's deviation from the log-linear interpolation exceeds 25%).
- gpt-6.1-sol (e): V\* at the endpoint is not monotone in Λ somewhere on the grid (any decrease by more than 0.01), in at
  least one (arm, start, t₀) series.

## The engineer's predictions (Sonnet, after the static numbers; none computed from a run)

E1. **M natural is a boundary perturbation.** M's natural start is 0.004 in u inside its basin; Λ\*(M natural, t₀ = 1) ≤ 3
    and Λ\*(t₀ = 10²) ≤ 10 (the nudge needed is of the order 0.4% of islands, each arrival changes a few 10⁻³ of islands).
    *Falsifier:* either exceeds its bound or is "none". (0.5)
E2. **The late tail does not flip the settled ratchet on the grid.** At t_s = 10⁶ and t₀ = 1 the two-step path needs two
    rare arrivals on one island (7.2 × 10⁻⁴ then 1.8 × 10⁻³ per arrival, so about 6% of islands at Λ = 300 before
    migrant amplification): no Λ ≤ 300 has endpoint V\* ≥ 0.5 at any t₀. *Falsifier:* some late Λ ≤ 300 with V\* ≥ 0.5. (0.55)
E3. **The victims barely matter in the tail.** Matched-dose removal of the victim constants from the tail moves Λ\*(M natural,
    t₀ = 10²) by less than 1.25× (their direct yield, 2.5 × 10⁻⁵ per arrival, is 30× below the offering constants'). This
    disagrees with both the RE (≥ 1.5×) and argon (≥ 1.5×). *Falsifier:* a factor ≥ 1.25. (0.55)
E4. **The conditionals in the tail do nothing.** The constants-only tail (ablation d, matched-dose) has Λ\* within 1.25× of
    the full tail's. *Falsifier:* a ratio ≥ 1.25 either way. (0.7)
E5. **N = 400 does not leave M natural at U.** At Λ = 0 the hybrid object (N = 400 kernel, founding law of N = 100) has
    V\* < 0.5 for M natural at N = 200 and 400 (selection sharpens, the ratchet gets stronger). *Falsifier:* V\* ≥ 0.5 at
    N = 400 at Λ = 0 (then prediction 6 fails by the convention above). (0.6)
E6. **Monotone, to within 0.01, on every series with a Λ\* in the grid.** (0.65; opposes gpt-6.1-sol (e).)
E7. **The tail does not break the fair arms.** Arm T at Λ = 300, t₀ = 1 (cell 7), both pm, both starts: V\* ≥ 0.999. Agrees
    with prediction 4. (0.75)

## Falsifiers collected in one place

A single table of verdicts (RE 1–7, reviewers a–e, engineer E1–E7) with the number that scores each goes in the run report
and the RESULTS draft. Every failed prediction, the RE's, the reviewers' and the engineer's, goes to the REJECTED draft.
