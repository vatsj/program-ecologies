# Predictions: rewarding prudence, fission–fusion with a light post-merge tail under world K, 2026-10-21

Spec `specs/2026-10-21-prudence-world-k.md` (reviewed by gpt-6.1-sol and then gemini-4-argon; the amendments supersede
the earlier text). Notes `notes/prudence.md` §1 (committed before any code). Written and committed before any code and
any counted cell. Everything is an ε = 0 seed lottery followed by a finite-(N = 12,800, horizon) re-injection
diagnostic, never π. "L" and "K" are the worlds of `src/world_k.py`; "t" is the generation after the merge (merge at
generation 200); "tail's end" is t = 10,000, "chase's end" t = 12,000. A = fresh founders per 100 programs delivered by
t = 10,000 (expected 128 A in the population of 12,800). SD52 is A = 52 with uncertified unconditional cooperators removed
from the arrival prior.

## The RE's predictions (verbatim from the spec, with the revision and the registered counter-predictions)

1. **A light tail rewards prudence:** PrudentBot's share at the end rises with A (A = 52 above A = 0 by ≥ 0.1 in world
   L). *Falsifier:* no rise in either world.
2. **The tail reduces target drift** [revised after review]: off-target residence time (population-generations on
   uncertified FairBot variants) falls at A = 52 against A = 0, in the paired difference. *Falsifier:* no decrease or an
   increase.
3. **World K shrinks the premium:** the premium per sucker encounter is smaller in K than in L, because certified
   suckers pass PrudentBot's guard. *Falsifier:* K's premium at least L's.
4. **Universality stays high:** universal-open ≥ 0.9 at every A in both worlds (one population after the merge).
   *Falsifier:* ≤ 0.75 at A = 52.
5. **No clique takes the merged population** under the tail in world K. *Falsifier:* any run with an identity share
   ≥ 0.05 at the end.
6. **Counter-predictions registered (gpt-6.1-sol).** Off-target residence falls where exploitable suckers remain, but
   terminal off-target failures are not reliably zero; PrudentBot's share responds more clearly to uncertified-sucker
   exposure than to total A, weakly or non-monotonically in K; merging does not by itself preclude clique invasion, and
   world L remains vulnerable.
7. **Counter-prediction registered (gemini-4-argon).** In world L at A = 156 universal-open falls below 0.85, because
   repeated identity arrivals prey on identity-exploitable target holders.

Amendments from the two reviews that bear on scoring (the spec's text, summarized): exposure is *delivered* exposure
(normalized on the discrete generations); a sucker-depleted control at A = 52 in both worlds, the same syntactic set;
predictions 1 and 2 are judged against SD52 as well as against A = 0; the premium's primary measure is the fixed-list
payoff edge and the edge per arriving uncertified-sucker founder, the encounter-weighted average secondary; the chase
is kept; the target is frozen in advance; composition at the merge is logged; t₀ = 1,000.

## Scoring conventions (declared now; they do not change the wording above)

- **"PrudentBot's share" (predictions 1 and 6)** is scored two ways and both verdicts are reported: (a) the PrudentBot
  *network* = the frozen target T (self-cooperating units mutual with PrudentBot-H: 235 units in L, 298 in K); (b)
  PrudentBot's own tree. The headline reading is (a), because the spec lists "the PrudentBot network's share" first.
  I add (c) the **prudent (guarded) target** = T members that defect against certified CooperateBot, and judge the
  premium's effect on *which* target members win by it (declared in notes §1.2 before any cell). Verdicts for 1 and 6
  are given on all three.
- **Prediction 2 (off-target residence)** = ∫ over t ∈ [0, 10,000] of the population share of the class `CBo` (self-
  cooperating, mutual with FairBot-H, not in T, not a sucker), by the rectangle rule at the checkpoint spacing; the
  paired difference is over runs with the same founders and merge seed. "Falls" requires the paired mean difference
  (A52 − A0) < 0 *and* a sign test against A0 and against SD52 not in the other direction at p < 0.1; in each world
  separately (a world where A = 0 has zero off-target residence cannot fall).
- **Prediction 3 (premium per sucker encounter)** is scored on the **fixed-list edge per arriving uncertified-sucker
  founder** (primary), with the encounter-weighted edge reported beside it; "smaller in K" needs the K value below the
  L value by at least 1% of the L value (tie otherwise ⇒ the falsifier fires).
- **Prediction 4**: universal-open at the tail's end in each world and arm; the A = 156 cells count too.
- **Prediction 5**: identity share = `decompose`'s `ident` at any checkpoint of any K run, the spec's end-of-run reading
  applied at the tail's end and the chase's end; I also report the maximum over time.
- **Prediction 7**: universal-open at A = 156 in L at the tail's end (and the chase's end as a check).
- Counts of zero are read with binomial upper bounds (0 of 20 ⇒ ≤ 0.14 at 95%). Paired tests are exact (sign /
  McNemar) and paired bootstrap for means.
- **Headline outcome regions** (notes §1.7): R-reward, R-resilience, R-null, R-harm, per world, on G = the mean
  prudent-target share at the tail's end.

## My own predictions (numbered, with falsifiers and outcome regions)

Written after reading the stored tables and the stored A = 0 finals (disclosed in notes §1's preamble) and before any
arrival run.

**S1 (static; looked at before writing).** The fixed-list edge per arriving uncertified-sucker founder is the same in
K and L to within 1%: the prior-weighted edge over sucker spellings is 0.6828 in both (to the digits printed), 0.826 vs
0.824 over certified-sucker H-states, and +1 for `C`; the worlds differ only on Q (prior mass 0.0007) and the AP-network
mass K moves (0.0126). *Consequence:* RE prediction 3 is not supported on its primary measure. *Falsifier of S1:* a
relative difference above 5% on the computed list (the computed value, in notes §2, supersedes my looked-at number).

**S2 (the premium is paid by who wins among the target).** G(A0) reproduces the stored winner-guarded rates (L 5/20,
K 4/20 by the stored final winner; the mean prudent share at the tail's end within 0.1 of those). G(A52) ≥ 0.60 and
G(A156) ≥ 0.70 in both worlds; G(SD52) ≤ G(A0) + 0.15. So the outcome region is **R-reward in both worlds**.
*Falsifiers:* G(A52) ≤ 0.35 in either world (no reward); G(SD52) ≥ G(A0) + 0.25 (resilience, not prudence).

**S3 (the ceiling).** The target share T at the tail's end is at its ceiling at A = 0 (mean ≥ 0.95 in both worlds), so
RE prediction 1 read as (a) "network share up by ≥ 0.1" must fail by the ceiling in both worlds; read as (b) PrudentBot's
own tree, the rise at A52 over A0 is below 0.10 in both worlds (one of three guarded spellings that together are 0.023
of the prior); read as (c) the rise is ≥ 0.25 (S2). *Falsifier:* (a) T share gains ≥ 0.1 (would need A0's mean ≤ 0.9);
(b) a rise ≥ 0.10.

**S4 (universality).** Universal-open at the tail's end ≥ 0.90 at A52 in both worlds, and in [0.70, 0.95] at A156 in both
worlds (a heavy tail is not free). So RE prediction 4 holds at A52 and may fail at A156; gemini's counter-prediction 7
(L at A156 below 0.85) is a coin flip on my reading, a little more likely than not (0.55). *Falsifiers:* ≤ 0.75 at A52
(RE 4's own falsifier) in either world; ≥ 0.95 at A156 in L (gemini 7 fails).

**S5 (off-target residence is a neutral-arrival cost, not a cure).** At A0 off-target residence is carried by the stored
off-target runs: L's rep 5 only (stored final target share 0.56), K none. So the paired difference A52 − A0 is **positive
in K** (transient neutral arrivals) and **negative in L only if the tail cures rep 5**; in a pooled test RE prediction 2
fails in K. *Falsifier:* A52 − A0 < 0 in K at p < 0.1.

**S6 (ancestry).** In runs where the prudent share at the tail's end exceeds its value at the merge by ≥ 0.25, at least
0.8 of that share is arrival-descended (invasion by guarded arrivals, not reproduction of guarded residents); the
decomposition into immigration and reproduction credits immigration with at least half of the change over the first
2,000 generations of the tail. *Falsifier:* arrival-descended share < 0.5 in the majority of such runs.

**S7 (delivered exposure).** Realized arrivals are within 3% of 128 A in every run (binomial sd ≈ 1.2% at A = 52, 0.7% at
A = 156), and the realized fraction delivered by t = 5,000 is 0.78 ± 0.03 of the total (the shape's cumulative share).
*Falsifier:* a run outside 3%, or a systematic offset.

**S8 (identity and the clique channel).** No K run has an identity share ≥ 0.05 at any checkpoint (RE 5 holds by S1's
logic: Q arrives at prior mass 0.0007, about 4.7 founders per 6,656 arrivals at A52, and in K Q are certified suckers
exploited by every defector); in L, a Q arrival can bloom into a whole-population takeover (annealed run: one in 160
arrivals' worth of runs), so the L identity maximum over time is above 0.05 in at least one of the 60 non-SD L arrival
runs. *Falsifiers:* any K run ≥ 0.05 (RE 5 fails); no L run ≥ 0.05 in any arm (the clique channel is closed at this
exposure).

**S9 (losses).** Whole-population loss (all-defect, closure `lost`) is 0 of 20 at A0 in both worlds (stored: 20/20 and 20/20
universal-open), ≤ 2 of 20 at A52, and 1–6 of 20 at A156, in each world; losses at A156 exceed those at A52 in both worlds.
*Falsifier:* ≥ 3 at A52 (RE 4's reading too), or 0 at A156 in both worlds.

**S10 (the worlds agree).** On every paired endpoint (universal-open, universal-on-target, prudent majority, loss) the K
minus L difference is within ±0.15 in every arm. *Falsifier:* a difference above 0.25 in any arm at 20 paired runs.

**S11 (the control ranks).** SD52 is *not worse* than A52 on universal-open (arrivals with no unconditional cooperators
cannot build a sucker pool for defectors): universal-open(SD52) ≥ universal-open(A52) − 0.05 in both worlds, while
G(SD52) is lowest of the arrival arms. *Falsifier:* SD52 below A52 by more than 0.10 on universal-open.

**S12 (validation).** The ε = 0 arm reproduces the stored fission–fusion cells (pcc, living types, M, T share) at every
stored checkpoint in both worlds on reps 0–2; the arrival kernel at ε = 0 equals the Pangaea kernel state for state on
the merged population. *Falsifier:* any difference (then the run stops and no cell is counted).

## Outcome regions for the question "does the tail reward prudence?"

Per world, on G(a) = mean prudent-target share at t = 10,000 (and re-read at t = 12,000):

| region | condition | what it would say |
|---|---|---|
| **R-reward** | G(A52) ≥ G(A0) + 0.25 and G(A52) ≥ G(SD52) + 0.20 | the sucker supply pays prudence; the premium is real and survives K |
| **R-resilience** | G(A52) ≥ G(A0) + 0.25 and G(A52) − G(SD52) < 0.10 | arrivals raise the guarded share without suckers: guarded programs are better *arrivals*, not better *earners* |
| **R-null** | \|G(A52) − G(A0)\| < 0.10 | the tail does not move who wins among the target |
| **R-harm** | universal-open ≤ 0.75 at A52, or G falls | the tail costs more than it pays |
| intermediate | anything else | reported as such |

"The tail rewards prudence" needs R-reward in both worlds. I predict it (S2). The spec's prediction 3 (K shrinks it) I
predict will *not* hold (S1).

## What I expect to be wrong about

The size of G(A156) (the ladder can eat the sucker pool before guarded invaders arrive); the L identity maximum (one
event decides it); and whether guarded T programs are actually mutual with the resident unguarded winner pairwise (T is
defined against PrudentBot-H, not against each other), in which case invasion could stall at a polymorphism and G would
sit near 0.5, not near 1.
