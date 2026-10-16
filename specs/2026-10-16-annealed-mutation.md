# Spec: annealed mutation: a decaying re-injection schedule along the scaling limit Λ_N → 0, N·Λ_N → ∞, 2026-10-16

Status: draft by the RE (Fable); to be reviewed by gpt-6.1-sol and gemini-4-argon; to be run by an Opus subagent.
The RS's proposal (DEFERRED 1, 2026-10-16); follow-up to RESULTS "Removing rival networks". REJECTED.md checked: the
RS's criterion failed at N ≤ 400 under constant rain (2026-10-16); this spec tests the scaling limit that the 1/N
behaviour points to, which is new evidence, and says so.

## The RS's proposal and criterion (verbatim, registered)

> I propose a model where mutation rate decreases over time. It starts at infinity, which generates the random
> seed, but the tail is light enough that islands can't drift (but heavy enough to prey on inefficiencies).

> drift should never colonize an island, only reintroduce fit programs.

## Why

Under constant rain at N = 200–400, drift colonizations per island-generation halved when N doubled (≈ 1/N neutral
fixation per arrival), while an injected predator colonized a rival island with ρ ≈ 0.26 regardless. With Λ the
integrated post-seed re-injection per island (fresh founders per island ÷ N), drift colonizations per island ≈ c₁·Λ
and the cure of an exploitable rival ≈ 1 − exp(−ρ·μ_pred·N·Λ). So the RS's object is the limit Λ_N → 0 with
N·Λ_N → ∞; along Λ_N = Λ₀·(200/N)^{1/2}, drift per island falls as N^{−1/2} while the cure exponent grows as N^{1/2}.
What the constant-rain run also showed: rain feeds identity cliques through exploitable target shadows (165 of 235
target units), so annealing alone is not expected to reach the target; the sponsored PrudentBot founder is the
prevention arm to combine with it.

## Design

**Machinery.** `src/removing_rivals*.py` (rain kernel, drift classifier, target definition), `src/realizable_scaling*.py`,
`src/provenance*.py` (import only; a new kernel may copy the rain kernel to make ε time-dependent). Cached tables
copied from a read-only worktree or rebuilt; ε = 0 reproduction verified first.

**Schedule.** Generation 0 is the seed (ε = ∞). Afterwards fresh founders arrive per island-generation at
εN(t) = a·(1 + t/t₀)^(−2) (finite tail), t₀ = 50, with a set so that the integrated arrivals per island equal N·Λ_N.
Path: N ∈ {200, 400, 800} at I = 16 and calibrated mN, Λ_N = Λ₀·(200/N)^{1/2}, Λ₀ ∈ {0.01, 0.03}. Horizon 10,000
generations (the schedule has delivered ≥ 99% of its arrivals by then). 20 runs per cell, paired founder streams.

**Arms.** (i) S-nonself + annealing; (ii) the sponsored PrudentBot founder + annealing; (iii) both at ε = 0 (the
matched baselines); (iv) **constant rain** delivering the same Λ_N uniformly over the horizon (does the schedule's
shape matter, or only Λ?).

**Statistics.** Drift and selected colonizations per island by class (shadow on target, on rivals, other), predator
cures of exploitable rivals, identity islands and identity takeovers of target islands, uot and universal-open,
island efficiency; all as functions of N along the path, with run-clustered intervals; whether the RS's criterion
(zero drift colonizations over the horizon) holds per run.

**Scale guard.** ≤ 3 workers; two sibling runs (`coverage_components`, `pangaea`) use up to 3 each: check `ps` first.
N = 800 at I = 16 costs about 4× a (200, 64) generation per island-generation: report projected costs first; drop
Λ₀ = 0.03 at N = 800 first, then arm (iv).

## Required outputs

`src/annealed.py` (+ `_kern.py`, `_run.py`, `_report.py`), `tests/test_annealed.py` (the schedule integrates to
N·Λ_N; ε = 0 reproduction; drift classifier agrees with the removing-rivals one on stored lineages), `notes/annealed.md`
(§1 the scaling argument with the measured ρ and μ_pred, hand predictions; §2 costs), `runs/annealed.md` and `.json`,
predictions committed before any counted cell with the RS's statements first, and the usual hand-back.

## RE predictions (with falsifiers)

1. **Drift scales away along the path** [revised: on the amended path the expected slope is −1]: drift colonizations per island fall as N^(−1/2) within a factor 2 from
   N = 200 to 800, and the fraction of runs with zero drift colonizations rises with N. *Falsifier:* no decrease.
2. ~~Cures scale up to ≥ 0.8 at N = 800, Λ₀ = 0.03~~ [withdrawn after review by both: N·Λ_N = 12 arrivals per island
   needs predator mass ≥ 0.52 for a 0.8 cure, against ≈ 0.075]. **Revised (on the amended path):** with N·Λ_N held at
   K/(ρ·μ_pred) arrivals per island, the cure of exploitable rivals is ≥ 0.8 at every N. *Falsifier:* ≤ 0.5 at any N.
3. **The RS's criterion holds at the largest cell in a majority of runs** [revised: on the amended path]: no
   post-establishment drift colonization in ≥ 0.5 of runs at N = 1,600, with cures ≥ 0.8 there (uncertain).
   *Falsifier:* ≤ 0.2 of runs drift-free at N = 1,600.
4. **Annealing does not remove identity:** identity islands under (i) are ≥ the ε = 0 baseline's at every N;
   annealing plus sponsorship leaves uot below 0.85 at every N. *Falsifier:* uot ≥ 0.9 anywhere.
5. ~~Only Λ matters~~ [withdrawn after review by both: shadows take O(N) generations to form, so a front-loaded
   schedule meets fewer of them]. **Revised:** the schedule's shape matters for identity: constant rain gives more late
   identity takeovers of target islands than annealing at N ≥ 400, while drift colonization per island is equal within
   an equivalence margin of ±30% at matched total arrivals. *Falsifier:* identity takeovers equal within ±0.01 per
   island, or drift outside the margin.
6. **Counter-predictions registered.** *Gemini:* constant rain produces significantly more secondary takeovers of
   target shadows, and more late identity takeovers, than annealing at N ≥ 400; on the original path the cure of
   non-shadow exploitable rivals is < 0.5. *Sol:* outcomes are schedule-dependent in a direction not predictable
   before measuring state-conditioned hazards; identity effects are heterogeneous across founder regimes, not
   monotone in N.

## Amendments after review (gpt-6.1-sol and gemini-4-argon; these supersede the text above where they conflict)

1. **The path holds cure exposure fixed.** Measured values (removing-rivals run): per-arrival predator colonization
   ρ ≈ 0.26 and accessible predator mass μ_pred ≈ 0.075 (anti-punishers; notes §1 recomputes both per rival class
   before any cell). Arrivals per island are fixed at N·Λ_N = K/(ρ·μ_pred) with K = 3 (≈ 150; cure ≈ 0.95 if the formula
   holds), so Λ_N ∝ 1/N: drift colonizations per island ≈ p₀·N·Λ_N fall as 1/N while the cure exposure stays constant.
   Path: N ∈ {200, 400, 800, 1,600} at **I = 8** (aggregate drift scales with I·Λ_N; conclusions are restricted to
   fixed I), calibrated mN. A second exposure, K = 1, at N = 200 and 800 only.
2. **Timing.** The schedule starts after establishment: the seed at generation 0, no arrivals before generation 200,
   then εN(t) = a·(1 + (t − 200)/t₀)^(−2) with **t₀ = N/2** (so a = 2·N·Λ_N/N stays ≤ 1.5 per island-generation and the
   schedule is not dumped into the scramble), horizon 10,000 + a 2,000-generation mutation-free chase so that late
   lineages resolve; the fraction of arrivals delivered by the horizon is reported per N (≥ 0.9 at N = 1,600).
3. **Production held constant per program**, r = 100 per Moran event at every N (as in the Pangaea run), so island
   size does not change production intensity; validated against native r at N = 200.
4. **Arms.** (i) S-nonself + annealing; (ii) sponsored PrudentBot founder + annealing; (iii) both at ε = 0; (iv)
   constant rain from generation 200 delivering the same total, kept at every N for K = 3 (dropping K = 1 cells first
   if compute binds). Schedules are paired by founder identities and by the sequence of fresh-founder draws, not just
   the seed; actual arrival counts are reported.
5. **Assays and logs.** Single-arrival assays on frozen target and rival residents at each N (neutral fixation,
   predator establishment, completion times); every colonization logged with its arrival generation, the resident
   state at arrival and its fate (including unresolved at the horizon); cures reported per initially eligible rival,
   direct versus migrant-mediated.
6. **Outcome regions.** Each prediction states supported / contradicted / inconclusive regions in the predictions file
   before any cell; the scaling claim is a finite-size diagnostic over 200–1,600 at I = 8, judged by the log-log slope of
   drift per island against N (prediction 1: slope in [−1.3, −0.7]).
