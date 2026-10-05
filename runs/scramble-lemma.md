# The scramble lemma and Claim A (2026-10-05)

Spec `specs/2026-10-05-scramble-lemma.md` (reviewed by gpt-6.1-sol); predictions `predictions/2026-10-05-scramble-lemma.md`
(committed before the checks, 5123206); proofs `notes/scramble-lemma.md`; code `src/scramble_lemma.py`; numbers
`runs/scramble-lemma.json`. The per-run rows (`runs/scramble-lemma-rows.json.gz`, 102 MB) are not committed: they are
regenerated deterministically by `python3 src/scramble_lemma.py run` (6 min, 3 workers) after
`python3 src/spoiler_conditioned.py build`.

Modal arm, PD, w = 0.3, single islands, the seeds_in_n kernel. Finite-cell evidence at n ∈ {6, 9, 12}, N ∈ {100, 400}.

## 1. Claim A (proved; exhaustive check at n ≤ 12)

Proved for all six members of P, at every box level of an evaluator with the shared-chain convention and at every
cutoff, without Löb (`notes/scramble-lemma.md` §0–1). The single lemma used is *box soundness at the stable world*
(Lemma 0): the evaluator stops at a global fixed point of one chain shared by every pair, so a box that is true at
the stable world quantifies over a world where the boxed pair already plays its stable value. This covers the nested
call `THEM(THEM)` (pair (q, q), same world index). Consequences:
- FairBot, `BOX1(THEM(ME))`: no fakers at all.
- `BOX(THEM(^C))`, `BOX1(THEM(^C))`: every faker cooperates with ALLC.
- `BOX(THEM(THEM))`, `BOX1(THEM(THEM))`: every faker self-cooperates, so it is an establisher or a D-cooperator.
  The case is not vacuous (sol's dichotomy): `not(BOX(THEM(ME)))` is a D-cooperating faker of `BOX1(THEM(THEM))`.

| n | member | fakers (mass) | non-establisher fakers: coop D only / ALLC only / both | establisher-fakers (mass) | counterexamples |
|---|---|---|---|---|---|
| 6 | FairBot, BOX1(THEM(ME)) | 0 | – | 0 | 0 |
| 6 | BOX(THEM(THEM)) | 0 | – | 0 | 0 |
| 6 | BOX1(THEM(THEM)) | 3 (2.6·10⁻³) | 3 / 0 / 0 | 0 | 0 |
| 6 | BOX(THEM(^C)), BOX1(THEM(^C)) | 6 (3.0·10⁻³) each | 0 / 6 / 0 | 0 | 0 |
| 9 | FairBot pair | 0 | – | 0 | 0 |
| 9 | BOX(THEM(THEM)) | 24 (2.8·10⁻⁵) | 0 / 0 / 20 | 4 (1.2·10⁻⁵) | 0 |
| 9 | BOX1(THEM(THEM)) | 49 (2.9·10⁻³) | 23 / 0 / 20 | 6 (1.0·10⁻⁵) | 0 |
| 9 | BOX(THEM(^C)) / BOX1 | 101 / 95 (3.6·10⁻³) | 0 / 75 / 22 ; 0 / 69 / 22 | 4 (1.2·10⁻⁵) | 0 |
| 12 | FairBot pair | 0 | – | 0 | 0 |
| 12 | BOX(THEM(THEM)) | 488 (5.2·10⁻⁵) | 0 / 0 / 374 | 114 (1.7·10⁻⁵) | 0 |
| 12 | BOX1(THEM(THEM)) | 735 (3.1·10⁻³) | 310 / 0 / 333 | 92 (2.0·10⁻⁵) | 0 |
| 12 | BOX(THEM(^C)) / BOX1 | 1,964 / 1,820 (3.9·10⁻³) | 0 / 1,280 / 566 ; 0 / 1,183 / 529 | 118 / 108 (1.7·10⁻⁵) | 0 |

Independent evaluator (`conj4.play`): all 24,981 (x, q) pairs with x ∈ P cooperating with q at n = 12, re-evaluated on
(x,q), (q,x), (q,q), (q,D), (q,C): 0 disagreements with the cache, 0 Claim A failures.

**The spec's example establisher-faker is wrong.** `and(BOX(THEM(THEM)),not(BOX(THEM(^C))))` defects on itself: its
self-play is p ↔ □p ∧ ¬□⊥, whose unique fixed point is ⊥ (on the chain, every box is vacuously true at world 0, so
the conjunction is D there). Checked by conj4: q vs q = D. Working examples (by enumeration, checked by conj4):
`BOX1(THEM(^not(BOX(THEM(ME)))))` fakes `BOX(THEM(THEM))`, and `and(BOX(THEM(THEM)),BOXD1(THEM(^D)))` fakes
`BOX1(THEM(THEM))`; both self-cooperate and defect on D.

## 2. Claim B (proved form; measured content)

**Kernel.** `seeds_in_n._run` is a **birth–death** Moran process (parent ∝ count·exp(w π), uniform victim), not the
death–birth the spec names. For a class q with k copies, E[Δk | state] = (k/N)(f_q/F̄ − 1) exactly, per event.

**B1 (proved, exact).** k_t·exp(Λ_t), Λ_t = −Σ_{events} log(1 + r/N), r = f_q/F̄ − 1, is a martingale. By optional
stopping at the bounded stopping time τ = τ_A ∧ freeze ∧ 2,000 generations, for any seed event E and any level Λ:
P(q alive at τ | E) ≤ P(Λ_τ < Λ | E) + E[k_0 | E]·e^{−Λ}. Λ_τ is the *net* integrated relative deficit (exposure
before the faker drops below the mean included, with its sign). The stopping-time correlation is handled exactly.
**B2:** Λ_τ ≥ w ∫[c_w (π̄ − π_q)⁺ − C_w (π_q − π̄)⁺] dt, c_w = 0.659, C_w = 1.615 at w = 0.3. **B3:** in {D, ALLC, q}
with q rare, π̄ − π_q = x_A·x_q for the probe-faker (mean-neutral to first order), x_D² − x_A² for the D-cooperator
(above the mean while ALLC outnumbers D), x_D(x_D + x_A) for the both-cooperator.

**Checks.** The instrumented kernel reproduces the spoiler run's (b) islands draw for draw (124 of 124 tC and
faker-alive-at-tC matches; 2 skipped, frozen). The martingale identity E[k_τ e^{Λ_τ}] = E[k_0] holds:
ratios 0.96–1.07 (±0.02–0.06) in 14 of 15 cells, 0.77 ± 0.09 in one (heavy-tailed estimator). The ghost (neutral
lineage) keeps E[k_τ] = k (ratio 0.99–1.01).

**Design.** The spoiler run's forced backgrounds and treatment (b) insertion (k fakers beside k targets), rebuilt
with the same RNG; 3,000 backgrounds per pair (reps 0–999 are the spoiler's own), six forced pairs plus the
supplement, n ∈ {6, 9, 12}, N ∈ {100, 400}, k ∈ {1, 3} and {1, 3, 10}. **Neutral control:** the same seed and stopping
rule with the k inserted fakers replaced by *ghosts*: they play exactly as the faker, but their fitness is pinned to
the population mean (r ≡ 0). Restricted to E = {x_A(0), x_D(0) ≥ 0.3} (P(E^c) ≤ 7·10⁻³ at N = 100, 4·10⁻¹⁰ at 400).
"Clean": backgrounds with no background copy of the faker's class, so the faker class has exactly k copies.

### Survival to the island's ALLC extinction, k = 1, clean, pooled over n

| N | faker type (pairs) | islands | faker alive at τ | ghost alive at τ | ghost/faker | selection share of −log s | median Λ_τ | B1 bound | bound/measured | median τ (gens) | E[1/(1+τ)] |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | D-cooperator (`not(BOX(THEM(ME)))` etc.) | 15,722 | 0.038 [0.035, 0.041] | 0.082 [0.078, 0.086] | 2.14 | 0.23 | 2.19 | 0.41 | 10.7× | 13.4 | 0.073 |
| 100 | probe-faker (`BOX(THEM(^D))` etc.) | 30,878 | 0.071 [0.068, 0.074] | 0.072 [0.070, 0.075] | 1.02 | 0.01 | 0.12 | 1.00 | (vacuous) | 13.6 | 0.072 |
| 100 | establisher-faker (FairBot of a sucker) | 5,459 | 0.082 | 0.074 | 0.91 | −0.04 | 0.06 | 1.00 | (vacuous) | 13.6 | 0.072 |
| 400 | D-cooperator | 10,717 | 0.0077 [0.0063, 0.0096] | 0.052 [0.048, 0.057] | 6.75 | 0.39 | 3.63 | 0.15 | 19.7× | 19.0 | 0.051 |
| 400 | probe-faker | 19,349 | 0.046 [0.043, 0.049] | 0.048 [0.045, 0.051] | 1.05 | 0.02 | 0.13 | 1.00 | (vacuous) | 19.1 | 0.051 |
| 400 | establisher-faker | 1,164 | 0.052 | 0.065 | 1.25 | 0.07 | 0.03 | 1.00 | (vacuous) | 19.1 | 0.051 |

Per n (k = 1, clean, ghost/faker): D-cooperator 1.87 / 2.06 / 2.61 (N = 100) and 6.71 / 6.27 / 7.36 (N = 400);
probe-faker 1.01 / 1.03 / 1.02 and 1.15 / 1.02 / 0.98; Λ, τ and ∫x_A flat in n to two digits. k = 3 and 10 give the
same per-copy picture (D-cooperator ratio 2.0 / 5.5 / 4.0; probe-faker 0.97–1.07).
Unrestricted to clean backgrounds the faker *looks* better than the ghost (ratios 0.39–0.91) only because background
copies of its class count as survivors; the clean comparison removes that.

**Per-copy survival vs the spoiler run.** All fakers: 0.008–0.08 per copy, matching the spoiler run's 0.014–0.06
(disadvantaged) and 0.05–0.09 (neutral) (which were conditioned on the target alive at tC). **The ghost survives
like a critical lineage: P(alive at τ) ≈ E[1/(1 + τ)]** (0.082 vs 0.073 at N = 100, 0.052 vs 0.051 at N = 400).

### Payoffs along the scrambles (N = 400, k = 1, in E; integrals in generations up to τ; pooled pattern, every n)

| pair type | faker vs target / itself / D / ALLC | ∫x_D | ∫x_A | ∫x_target | contribution to ∫(π̄ − π_q): from D / from ALLC / from others | mean Λ_τ |
|---|---|---|---|---|---|---|
| D-cooperator | 1 / 0 / −2 / 1 | 16.4 | 2.4 | 0.2–0.3 | +14.1–14.5 / −0.62 / +0.5–0.8 | 3.8–3.95 |
| probe-faker | 1 / −1 / −1 / 0 | 16.5 | 2.4 | 0.1 | +1.68–1.76 / −1.61–1.64 / ≈ 0 | 0.08–0.12 |
| establisher-faker (FairBot) | 1 / 0 / −1 / 0 | 16.5 | 2.4 | 0.06 | +1.24–1.28 / −1.70 / −0.12 | −0.10 |

The ALLC exposure ∫x_A dt is 2.4–2.6 generations (5% quantile 1.1 at N = 100, 1.65 at 400). D holds 85% of the
scramble. The probe-faker's loss to D through ALLC is cancelled by its gain over ALLC: B3's x_D x_A − x_A x_D.

## 3. The combined per-island bound (spoiler forced (b) islands, k = 1)

P(target survives) = ρ̃ − P(A ∩ F)·h exactly, ρ̃ = P(A)·P(surv | A, F^c), h = P(surv | A, F^c) − P(surv | A, F). The
union bound replaces P(A ∩ F) by P(F) ≤ B1.

| N | type | P(surv) | ρ̃ | P(A) | h | P(F) measured | P(F) B1 | bound with B1 | bound with measured P(F) |
|---|---|---|---|---|---|---|---|---|---|
| 100 | D-cooperator | 0.048–0.052 | 0.048–0.056 | 0.09–0.11 | 0.02–0.39 | 0.04 | 0.44–0.45 | −0.12 to 0.04 | 0.037–0.047 |
| 100 | probe-faker | 0.039–0.043 | 0.043–0.047 | 0.08 | 0.43–0.45 | 0.08 | 1.00 | −0.40 | 0.007–0.012 |
| 100 | establisher-faker | 0.027–0.031 | 0.031–0.035 | 0.06–0.08 | 0.23–0.55 | 0.11–0.12 | 1.00 | < 0 | < 0.01 |
| 400 | D-cooperator | 0.064–0.068 | 0.063–0.069 | 0.14 | (3–5 joint islands) | 0.012 | 0.21 | −0.04 to 0.06 | 0.063 |
| 400 | probe-faker | 0.032 | 0.033–0.034 | 0.08 | 0.16–0.22 | 0.07 | 1.00 | −0.12 to −0.19 | 0.016–0.022 |
| 400 | establisher-faker | 0.012–0.020 | 0.013–0.023 | 0.05–0.06 | 0.29–0.38 | 0.14 | 1.00 | < 0 | < 0 |

The bound is flat in n wherever it is defined. With B1's q̄ it is non-positive in 16 of 18 cells. Even with the
measured P(F) it is positive for the two non-establisher types and negative for establisher-fakers. The union step
P(A ∩ F) ≤ P(F) loses the factor 1/P(A) ≈ 7–20, because the target survives the scramble in only 5–14% of islands
and the faker's survival is nearly independent of it.

## 4. Verdicts

| # | prediction | outcome |
|---|---|---|
| 1 | Claim A for all six members at every n | **Held** (proved for every level and cutoff, no Löb; exhaustive at n ≤ 12, 0 counterexamples; independent evaluator 0 disagreements). The THEM(THEM) case is one line, not a case analysis; the spec's establisher-faker example is wrong (it defects on itself) |
| 2 | first-moment bound within 10× of measured; selection ≥ half of the log-survival deficit | **Failed.** The bound is proved and exact as a martingale inequality, but: for probe-fakers (most non-establisher faker mass of the probe-readers) Λ ≈ 0.1 and the bound is vacuous, and the faker survives like the neutral ghost (ratio 1.01–1.05: falsifier "within 1.5" met). For D-cooperators the bound is 10.7× (N = 100) and 20× (N = 400) off, and selection carries 0.23 / 0.39 of the log deficit, not ≥ 0.5 |
| 3 | combined bound positive and uniform in n | **Failed on positivity, held on uniformity.** Every input is flat in n (no n-dependence beyond μ's normalization; falsifier not met). But the union bound with B1 is non-positive in 16 of 18 cells, and with the measured P(F) it is positive only for non-establisher fakers |
| RE note | THEM(THEM) case not vacuous | Held (310–643 non-establisher fakers at n = 12, all D-cooperators) |
| RE note | B1 loose by the neutral survival factor | Held: the ghost tracks E[1/(1+τ)], and the D-cooperator's survival is the ghost's times about e^{−(0.35–0.53)·median Λ} |
