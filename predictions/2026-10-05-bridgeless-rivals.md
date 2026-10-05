# Predictions: bridge-less rivals, their prior mass in n, and mediation before loss at N ≥ 200 (2026-10-05)

Spec `specs/2026-10-05-bridgeless-rivals.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-05-bridgeless-rivals-gpt-6.1-sol.md`;
where the two differ the spec's [after review] text is the resolution). Code: `src/bridgeless_rivals.py` (kernel
`rival_islands._kern` unchanged). Committed after the static screening (allowed by the brief, since the forced rivals
are chosen from it) and before any counted lottery run.

## RE predictions (copied verbatim from the spec)

1. **More rivals gain bridges at larger cutoffs, so literally bridge-less mass (τ = 0) falls as a fraction of rival
   mass from n = 9 to 15, while the τ = 10⁻⁴ ratio stays in [0.1, 0.5]** (sol's expectation adopted; the RE's
   first-draft monotonicity rationale was invalid). *Falsifier:* the τ = 0 fraction rising from n = 9 to 15, or the
   τ = 10⁻⁴ ratio outside [0.05, 0.6] at n = 15.
2. **A dense forced bridge-less rival separates the archipelago; the same treatment with a bridged rival does
   not:** in (a) the bridge-less rivals give horizon separation ≥ 0.5 of runs and the bridged ones ≤ 0.1; in (c)
   removing the bridges raises the bridged rival's horizon separation to ≥ 0.4; in (b) sparse seeding gives
   separation between the two. *Falsifier:* a bridge-less rival in (a) with horizon separation ≤ 0.2, or (c) not
   above (a)'s bridged value by ≥ 0.2.
3. **Unconditional natural separation at (200, 64) is rare, and bridge-less rivals are over-represented among
   horizon separations:** 1–15 of 3,000 runs separated at the horizon; bridged rivals may appear among them when
   their bridge failed to seed or died in the scramble (sol's point), but the bridge-less share of horizon
   separations is ≥ 0.5 while their share of rival mass is ≈ 0.25. *Falsifier:* 0 of 3,000 (which only bounds the
   rate; reported as such), or bridge-less share ≤ 0.25 with ≥ 4 separations.
4. **Local P(C,C) is robust to the forced rival and cross-island P(C,C) is not:** island-level P(C,C) ≥ 0.95 in every
   cell, the counterfactual cross-island P(C,C) ≤ 0.8 in separated runs, and |Δq| ≤ 0.1 against (d). *Falsifier:*
   island-level P(C,C) < 0.9, or |Δq| ≥ 0.2.
5. **Scaling panel:** the bridge-less rival's separation persists at (400, 64) and at horizon 3·10⁵ (≥ 0.5), and
   the bridged rival's resolution is faster at (200, 256) than at (200, 64) (horizon separation lower). *Falsifier:*
   bridge-less horizon separation ≤ 0.2 at 3·10⁵.

## Static screening (ran before this commit; the addendum the brief allows)

`runs/bridgeless-rivals-static.json`, `src/bridgeless_rivals.py static`. The modal language was evaluated once at
n = 13 (51,234 canonical functions, 1,130 s on 3 threads under load) and n = 9, 12 are sub-blocks; the class data
reproduce the existing caches exactly (863 / 13,514 classes, identical V and μ at n = 9 and 12). **n = 15 does not
fit**: 374,074 canonical functions (140 GB at one byte per pair); n = 14 has 126,370 (16 GB, the machine's whole RAM).
The cutoff range is therefore 9 → 13, not 9 → 15. Definitions are the spec's (header of `src/bridgeless_rivals.py`);
rival = establisher mutually defecting with FairBot or `BOX1(THEM(ME))` (as `rival_islands`' static).

| n | classes | rivals (full) | rival μ cut / raw | τ = 0 bridge-less: n, frac of rival μ | τ = 10⁻⁵ | τ = 10⁻⁴ | τ = 10⁻³ | path length 1 / 2 / 3 |
|---|---|---|---|---|---|---|---|---|
| 9 | 863 | 20 (8) | 2.43·10⁻⁵ / 1.87·10⁻⁵ | 3, 0.214 | 13, 0.354 | 13, 0.354 | 13, 0.354 | 2 / 15 / 3 |
| 12 | 13,514 | 443 (241) | 4.14·10⁻⁵ / 3.24·10⁻⁵ | 76, 0.252 | 220, 0.417 | 252, 0.420 | 252, 0.420 | 58 / 379 / 6 |
| 13 | 27,189 | 839 (450) | 4.53·10⁻⁵ / 3.56·10⁻⁵ | 152, 0.253 | 445, 0.419 | 509, 0.425 | 509, 0.425 | 103 / 721 / 15 |

- Every rival is connected to A in the establisher mutual-cooperation graph (path ≤ 3).
- The τ-sensitive excess (0.14–0.17 of rival mass) is entirely rivals that `BOX1(THEM(ME))` itself fakes (the
  `not(BOXD1(THEM(^not(…))))` family: mutual defection with FairBot, a sucker of `BOX1(THEM(ME))`), each with
  mediator mass ≈ 0.007 (`BOX1(THEM(THEM))` fakes them too). The bridge-less mass that is neither A-faked nor mediated
  is 0.214 / 0.256 / 0.259 of rival mass at n = 9 / 12 / 13.
- Literally bridge-less rivals at n = 9 are the P\* family (`and(BOX1(THEM(ME)),not(BOX(THEM(ME))))`,
  `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))`, `and(BOX1(THEM(THEM)),not(BOX(THEM(^C))))`); none gains a bridge at
  n = 12 or 13 (two split into two classes, all parts still bridge-less). From n = 12 to 13, 6 of 76 bridge-less
  rivals gain a bridge, of mass 2–4·10⁻¹⁰ each. Every τ = 0 bridge-less rival preys on some bridge (typically
  `BOX1(THEM(THEM))`); none has a mediator except one at n = 12.

**Verdict on RE prediction 1 (decided by the static):** the τ = 0 fraction *rises* from n = 9 to the largest
computed cutoff (0.214 → 0.252 → 0.253), so the falsifier fires on the range 9 → 13 (n = 15 not computable here);
the τ = 10⁻⁴ ratio is 0.425 at n = 13, inside [0.1, 0.5] (that clause held, at n = 13 in place of 15). "More rivals
gain bridges" failed: none of the n = 9 bridge-less rivals gains one, and the n = 12 → 13 gains are negligible.

## Forced rivals (from the static; `runs/bridgeless-rivals-forced.json`)

Spec: three heaviest bridge-less rivals at τ = 10⁻⁴ and three heaviest bridged, matched on μ where possible (n = 9, cut
units).
- Bridge-less: P\* = `and(BOX1(THEM(ME)),not(BOX(THEM(ME))))` (3.16·10⁻⁶), P\*′ = `and(BOX1(THEM(ME)),not(BOX(THEM(THEM))))`
  (1.81·10⁻⁶), S\* = `not(BOXD1(THEM(^not(BOX1(THEM(THEM))))))` (6.76·10⁻⁷; first of a four-way tie; heaviest bridge
  3.6·10⁻⁶, so bridge-less only at τ ≥ 10⁻⁵; A-faked and mediated).
- Bridged: B₁ = `BOX1(THEM(^not(BOX(THEM(ME)))))` (5.36·10⁻⁶; bridge `BOX1(THEM(THEM))`, bridge mass 0.0053);
  H = `and(BOX(THEM(ME)),BOXD1(THEM(^D)))` (1.58·10⁻⁶; a half-rival: mutually defects with `BOX1(THEM(ME))` only, so
  FairBot itself bridges it, plus `BOX(THEM(THEM))`); B₄ = `BOX1(THEM(^not(BOX(THEM(^C)))))` (7.90·10⁻⁷, full rival,
  B₁'s bridge set). *Deviation:* the second-heaviest bridged rival, B₂ = `BOX1(THEM(^not(BOX(THEM(THEM)))))`, is B₁'s
  twin (identical bridge, prey and mediator structure, equal μ) and was replaced by the mass-matched B₄. Pairs by mass:
  P\* ↔ B₁, P\*′ ↔ H, S\* ↔ B₄.
- Kernel tags are taken against `BOX1(THEM(ME))` except for S\*, which mutually defects only with FairBot (tags
  against FairBot). Cell (c) removes B₁'s pairwise bridges plus the kernel's tag-3 classes: 73 classes, μ = 0.00530.
- Scaling panel: P\* (heaviest bridge-less) and B₁ (heaviest bridged).

## Operational definitions for the lottery (fixed before any counted run)

Kernel `rival_islands._kern` unchanged; n = 9, w = 0.3, ε = 0, N = 200, I = 64, mN = 1.091 (boundary), horizon 10⁵,
100 runs per cell. Forced copy = one individual of R replacing one of the N iid draws. Tags: 1 = A's network, 2 = R's
network, 3 = bridge (mutual cooperator with both), 0 = other.
- *Rival established:* tag 2 holds a certified island at some check. *Ever separated:* tags 1 and 2 each hold a
  certified island at the same check. *Horizon separated (the prediction's "horizon separation"):* tags 1 and 2 each
  hold a certified island (holder rule) at the horizon or stop; the generic separation (any two certified holders
  mutually defecting) is reported alongside.
- *Loss:* after the first ever-separated check, the first check at which tag 1 or tag 2 holds no island. *Hazard:*
  losses / Σ ∫ min(held₁, held₂) dt (per minority-island-generation), exact Poisson interval, so zero-loss cells give
  an upper bound. Decomposition of rival-island losses by strong-holder transition: 2>1 replacement, 2>3 absorption
  (mediation), 2>0 capture.
- *Mediation-before-loss probability:* among runs in which the rival established, the fraction with ≥ 1 mediation
  event (a tag-2 island strongly taken by a tag-3 class) at or before the loss check (or the horizon if no loss).
- *Bridge founders:* tag-3 copies in the seed (islands, copies, classes); bridge establishment = islands first
  certified with a tag-3 holder.
- *Island P(C,C):* mean over islands at the end (realized). *Counterfactual cross-island P(C,C):* global class
  frequencies under uniform mixing (a counterfactual; separation threatens this, not island efficiency).
- *q (holder form):* Σ islands whose end holder has local ancestry (established with ≥ 0.5 local holder share and
  still held by that class up to lumping) / the same in the m = 0 reference with the same initial states. Δq = q(cell)
  − q(d); interval from a run-pair bootstrap.
- *(f) natural runs:* every separation (the kernel's first separated pair, and every pair separated at the end) is
  classified by which member is in A's network, the other's static type at n = 9 (bridge-less at τ = 0 / τ = 10⁻⁴ /
  A-faked / bridged), the bridge classes of that pair (count, seeded copies and islands, held at the end, alive at the
  end, mediation transitions).

## Subagent predictions (made after seeing only the static screening and two timing runs; no lottery run)

- **S1 (P\* family is permanent once established).** Dense P\* and P\*′: the rival establishes in [0.55, 0.95] of runs,
  and among runs that are ever separated ≥ 0.9 are still separated at the horizon (0 losses; hazard upper bound
  ≤ 2·10⁻⁷). *Falsifier:* conditional horizon survival < 0.75, or establishment < 0.4.
- **S2 (an A-faked rival is not a rival).** Dense S\*: horizon separation ≤ 0.1 (`BOX1(THEM(ME))` and the mediators
  invade its islands strictly; rival-island losses dominated by 2>1 and 2>3, not neutral drift). *Falsifier:* ≥ 0.3.
- **S3 (bridged rivals resolve by mediation).** Dense B₁ and B₄: horizon separation in [0.03, 0.3] (the island path's
  pair 1 gave 0.15 at (200, 64) from a pre-seeded island); the mediation-before-loss probability ≥ 0.6 among
  rival-established runs. *Falsifier:* horizon separation > 0.4, or mediation-before-loss < 0.3.
- **S4 (the half-rival is bridged by FairBot).** Dense H: horizon separation ≤ 0.1. *Falsifier:* ≥ 0.3.
- **S5 (the bridge is the whole difference).** (c) B₁ with its bridges removed gives horizon separation within 0.15
  of dense P\*. *Falsifier:* differs by > 0.3.
- **S6 (sparse = fewer founders, same fate).** (b) For P\* and P\*′, sparse horizon separation is within ±0.15 of
  1 − (1 − p̂)^16, with p̂ the per-island rival establishment rate measured in (a). *Falsifier:* off by > 0.25.
- **S7 (natural).** (f) 2–12 of 3,000 runs separated at the horizon, and ≥ half of those separations have a τ = 0
  bridge-less (P\*-family) rival. *Falsifier:* > 25, or a P\*-family share ≤ 0.25 with ≥ 4 separations.
- **S8 (efficiency).** Island-level P(C,C) ≥ 0.97 in every cell; counterfactual cross-island P(C,C) in separated
  runs in [0.45, 0.85]. *Falsifier:* island P(C,C) < 0.93 in any cell.

## Verdict rules

Point estimates decide each clause; Wilson 95% intervals (runs as units) and exact Poisson intervals for hazards are
reported, and a clause whose point estimate satisfies it but whose interval crosses the falsifier boundary is marked
"held, not resolved". A falsifier fires only on the point estimate. Cells that do not run are "not tested", never
"held". The bridged-rival clause of RE 2 ("≤ 0.1") is evaluated for B₁ and B₄ (full rivals) and reported separately
for H; the bridge-less clause is evaluated for each of P\*, P\*′, S\*.
