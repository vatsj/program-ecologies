# Spec: rewarding prudence: fission–fusion with a light post-merge tail under world K, 2026-10-21

Status: draft by the RE; to be reviewed sequentially by gpt-6.1-sol then gemini-4-argon (`--mode amended`); to be run by
a Sonnet subagent. Run under the RS's 24-hour autonomy window (2026-10-21). Follow-up to the RS's wish that the
dynamics reward prudence (DEFERRED 1, 2026-10-17: the prudence premium is a good reason, proportional to the sucker
supply set by the schedule), RESULTS "Cliques on a Pangaea", "Annealed mutation" and "Identity-dependent results under
world K". REJECTED.md checked: nothing re-opened.

## Why

At ε = 0 the prudence premium is spent once the seed's suckers are eaten; PrudentBot and FairBot are then neutral, and
FairBot variants PrudentBot would not certify drift in (4 of 34 non-lost Pangaea runs ended off the target). A light
re-injection tail keeps supplying suckers, so prudence keeps paying; after a fission–fusion merge, cliques cannot grow
from a beachhead in one population. Under world K, however, certified unconditional cooperators (the former TwinD
family) pass PrudentBot's ⌜D⌝ guard, so PrudentBot cooperates with them instead of exploiting them, which may shrink
the premium. The run measures the premium per unit of sucker exposure in both worlds.

## Design

**Machinery.** `src/world_k*.py`, `src/pangaea*.py`, `src/annealed*.py`, `src/removing_rivals*.py` (import only; a new
kernel may combine fission–fusion with the annealed schedule). S-nonself, r = 100, w = 0.3, 128 islands of 100 merged at
generation 200 into one population of 12,800; after the merge, fresh founders arrive at εN(t) = a·(1 + (t − 200)/t₀)^(−2)
with t₀ = N/2 for the merged N, delivering a total of A arrivals per 100 programs, A ∈ {0, 52, 156} (the annealed run's
K = 0, 1, 3 exposures); horizon 10,000 after the merge plus a 2,000-generation chase without arrivals. Worlds K and L,
paired founders and paired fresh-founder sequences; 20 runs per cell.

**Statistics.** Over time: the PrudentBot network's share, PrudentBot's own share, the share of FairBot variants that
PrudentBot would not certify, the sucker share split into certified and uncertified suckers, identity and anti-punisher
shares; universal-open and universal-on-target at the end; the prudence premium per sucker encounter (PrudentBot's
payoff edge over FairBot-family programs in encounters with suckers) and per unit of fresh-founder exposure; drift and
selected colonizations as in the annealed run; whole-population losses.

**Scale guard.** ≤ 3 workers; a sibling weak-wing run uses up to 3; check `ps` first; one job per process. **Waiting:**
watch short commands; for long batches wait on one background command that exits at completion, or end the turn with
outputs on disk; never poll periodically.

## Required outputs

`src/prudence.py` (+ `_run.py`, `_report.py`), `tests/test_prudence.py` (A = 0 reproduces the stored world-K and world-L
fission–fusion cells; the schedule integrates to A), `notes/prudence.md` (§1 hand predictions; §2 costs),
`runs/prudence.md` and `.json`, predictions committed before any counted cell, and the usual hand-back.

## RE predictions (with falsifiers)

1. **A light tail rewards prudence:** PrudentBot's share at the end rises with A (A = 52 above A = 0 by ≥ 0.1 in world L).
   *Falsifier:* no rise in either world.
2. **The tail reduces target drift** [revised after review]: off-target residence time (population-generations on
   uncertified FairBot variants) falls at A = 52 against A = 0, in the paired difference. *Falsifier:* no decrease or an
   increase.
6. **Counter-predictions registered (gpt-6.1-sol).** Off-target residence falls where exploitable suckers remain, but
   terminal off-target failures are not reliably zero; PrudentBot's share responds more clearly to uncertified-sucker
   exposure than to total A, weakly or non-monotonically in K; merging does not by itself preclude clique invasion, and
   world L remains vulnerable.
7. **Counter-prediction registered (gemini-4-argon).** In world L at A = 156 universal-open falls below 0.85, because
   repeated identity arrivals prey on identity-exploitable target holders.
3. **World K shrinks the premium:** the premium per sucker encounter is smaller in K than in L, because certified suckers
   pass PrudentBot's guard. *Falsifier:* K's premium at least L's.
4. **Universality stays high:** universal-open ≥ 0.9 at every A in both worlds (one population after the merge).
   *Falsifier:* ≤ 0.75 at A = 52.
5. **No clique takes the merged population** under the tail in world K. *Falsifier:* any run with an identity share ≥ 0.05
   at the end.

## Amendments after the first review (gpt-6.1-sol; these supersede the text above where they conflict)

1. **Exposure is delivered exposure.** A is the number of fresh founders per 100 programs actually delivered by the end
   of the tail (10,000 generations after the merge); the schedule is normalized on the discrete generations so that its
   delivered integral equals A; arrivals replace a uniformly drawn individual at the birth step, as in the annealed run;
   realized counts are reported.
2. **Decomposition and a sucker-depleted control.** Ancestry of every individual (immigrant lineage versus resident) is
   logged and frequency changes are decomposed into immigration and reproduction. A sucker-depleted arrival control runs
   at A = 52 in both worlds: arrivals drawn from the prior with unconditional and certified cooperators removed and the
   rest renormalized, at the same rate.
3. **The premium, two ways.** PrudentBot's payoff edge over FairBot-family programs is computed against a fixed, paired
   list of opponent sources (identical in K and L) and encounter-weighted over the realized population, beside the
   total population-level selection advantage.
4. **Scope.** The chase is kept (never dropped); outcomes are reported at the tail's end and the chase's end; conclusions
   are finite-horizon statements at N = 12,800. Target membership is fixed in advance (the frozen 235-unit target of
   "Removing rival networks" and its world-K counterpart from the detector run). P(C,C), support, transitions and losses
   are reported unconditionally; claims of zero are read with their binomial upper bounds.
5. **Drop order revised:** A = 156 in world L first, then the sucker-depleted control in world L.

## Amendments after the second review (gemini-4-argon; these supersede the text above where they conflict)

1. **The schedule anneals.** t₀ = 1,000 generations (not N/2), so the schedule decays within the window and the delivered
   fraction by 10,000 is at least 0.9; normalized on delivered arrivals as before.
2. **The sucker-depleted control is the same syntactic set in both worlds:** arrivals with uncertified unconditional
   cooperators removed (programs that cooperate on every probe and carry no certificate), renormalized, at the same rate;
   the TwinD family is not removed, so identity arrivals in L are unchanged.
3. **The premium's primary measure** is the fixed-list payoff edge and the edge per arriving uncertified-sucker founder;
   the encounter-weighted average is secondary (it is inflated in K by certified suckers that survive).
4. **Predictions 1 and 2 are judged against the sucker-depleted control at A = 52** as well as against A = 0, so that
   resilience to arriving predators is not read as the prudence premium.
5. **Composition at the merge** (generation 200) is logged, separating the island-scramble premium from the post-merge
   tail.
