# Spec: the demographic lemma, the factorized spoiler bound, and the establishment formula (theory with measurement), 2026-10-05

Status: reviewed by gpt-6.1-sol (`reviews/2026-10-05-demographic-lemma-gpt-6.1-sol.md`) and revised; changes marked
[after review]. To be run by an Opus subagent. Mostly theory, with instrumented-kernel measurements at
N = 100, 400, 1,600.

## Why

RESULTS "The scramble lemma and Claim A" left the per-island bound for "almost all seeds" (THEORY §3) in a weak
state: the first-moment bound B1 on a co-seeded faker's survival is vacuous for probe-fakers (which are mean-neutral
to first order, so they die by demography, not selection), and the union step P(A ∩ F) ≤ Σ_q E[K_q | E]·q̄_q loses a
factor 1/P(A) ≈ 7–20 because the target itself survives the scramble in only 5–14% of islands. The combined bound was
non-positive in 16 of 18 cells. Two repairs were identified there and are queue item 3 (CLAUDE.md): a *demographic*
survival bound for a lineage at or below the population mean, and a bound on P(A ∧ F) that does not pay 1/P(A).

While drafting this spec the RE noticed that the same demographic argument predicts the per-island establishment
chance itself, which has so far only been measured (p(100, n) = 0.083–0.092, p ∝ N^0.55 over N = 100–400, RESULTS
"Almost all seeds: cutoff sensitivity in n"). That is task 3 below and is the part of this spec that matters most if
it holds: it would turn the establishment half of "almost all seeds" from a measurement into a formula with no free
parameter.

## Setting (as in the scramble-lemma run)

One island of size N, seeded iid from μ at cutoff n (modal arm, free box). Kernel: birth–death Moran (parent ∝
f = exp(w·payoff), victim uniform), w = 0.3, PD payoffs T = 1, R = 0, P = −1, S = −2; a generation is N events.
E = {x_A(0) ≥ 0.3, x_D(0) ≥ 0.3} (fails with probability ≤ 2e^{−0.042N}). τ = ALLC extinction ∧ freeze ∧ 2,000
generations. For a target establisher x: A = {x alive at τ}; F = {some co-seeded faker of x alive at τ}; h_q the
conditional harm, defined in `notes/scramble-lemma.md`; ρ̃ the faker-free establishment chance. Instrumented kernel:
`src/scramble_lemma.py` (`_scramble`, `run_local`, ghost control with fitness pinned to the mean).

**Payoff bookkeeping used below.** During the scramble the population is ALLC + D + a remainder of mass x_o. Against
{ALLC, D} an establisher that cooperates with ALLC (every member of the prover family P does) earns R·x_A + P·x_D =
−x_D; the mean payoff is −x_A·x_D − x_D² + O(x_o); so the establisher's payoff minus the mean is −x_D·x_o: **a prover
is payoff-neutral to first order during the scramble**, exactly like a probe-faker (B3). [after review] Payoff
neutrality is not fitness neutrality: fitness is e^{w·payoff} and the mean fitness is the mean of exponentials, so
by Jensen a payoff-neutral lineage has relative fitness e^{w·π̄}/mean(e^{w·π}) < 1; at x_A = x_D = 1/2 it is
1/cosh(0.15) = 0.989. Over a scramble of τ ≈ 15–20 generations this curvature costs about 10–20% of the expected copy
count, and it is part of the formula, not a remainder. After the scramble (D sea), a prover at frequency f earns
−1 + f·(R − P) against D's −1: a frequency-dependent advantage s(f) = e^{w·(R − P)·f} − 1 ≈ w·(R − P)·f, with no
constant term.

## Tasks

1. **Lemma D (demographic survival).** For a lineage q in the kernel whose fitness is at or below the population mean
   throughout a window [0, T] (f_q(t) ≤ F̄(t)), **killed on first reaching size K ≤ N/4** [after review: the cap is a
   killing convention, not a conditioning on a future event; actual survival is then ≤ the killed process's survival
   plus P(hit K before T), and P(hit K) for a supermartingale from k₀ is ≤ k₀/K], prove
   P(k_T > 0 | k_0 = k₀) ≤ k₀ / (1 + d_min·T), with d_min an explicit per-copy death rate per generation
   (for a rare lineage the per-copy death probability per event is (1/N)(1 − k·f_q/(N·F̄)) ≥ (1 − K/N)/N, so
   d_min ≈ 1 − K/N per generation; derive it, do not assume it). Suggested route: the continuous-time linear
   birth–death process with rates b(t) ≤ d(t) has P(alive at T | 1) = 1 / (e^{ρ(T)} + ∫_0^T d(s) e^{ρ(s)} ds) with
   ρ = ∫(d − b), which is ≤ 1/(1 + d_min·T); then dominate the kernel's lineage by such a process (per-event
   birth/death ratio is ≤ 1 iff f_q ≤ F̄; the (1 − k/N) factors only lower the birth rate), handling the discrete event
   clock (events versus generations, stated once and used throughout) and the time-varying background. [after review]
   Conditioning on the background path does not by itself make the lineage an independent branching process, because
   the background is endogenous (the lineage's own births displace background copies); state the comparison as a
   per-event domination of the lineage's birth/death probabilities given the full state, with the (1 − k/N) and
   f_q ≤ F̄ inequalities doing the work, and say exactly what is proved and what remains a coupling assumption. For k₀
   copies, 1 − (1 − 1/(1 + d_min T))^{k₀} ≤ k₀/(1 + d_min T) is immediate.
   *Check:* the ghost control (3,000 backgrounds per pair at N = 100, 400; add N = 1,600 at 1,000 backgrounds) at
   fixed t = 5, 10, 20, 40 generations against the bound (ratio measured/bound with intervals). The stopped version
   (survival at τ = ALLC extinction ∧ freeze ∧ cap) is **measured and reported separately**, with the three stopping
   reasons separated; a stopped-process inequality is to be derived only if it follows (e.g. optional stopping for the
   killed supermartingale gives E[k_τ] ≤ k₀, which bounds P(alive at τ) only through a lower bound on E[k_τ | alive]),
   and otherwise the fixed-time lemma is the proved object [after review: survival-dependent τ cannot replace T].

2. **The factorized spoiler bound.** [after review: exact first, assumptions named one by one.] Write the exact
   per-founder conditional union bound: P(A ∩ F | E) ≤ Σ_q Σ_{founders j of type q} P(A ∩ {j alive at τ} | E)
   = P(A | E) · Σ_q E[K_q | E] · q̄_q^{A}, where q̄_q^{A} = P(founder alive at τ | A, E) is the *per-founder conditional
   survival*; the per-island bound is then exactly P(x fixes | E) ≥ ρ̃ · [1 − Σ_q E[K_q | E] · q̄_q^{A} · h_q] with
   every term defined (ρ̃ and h_q as in `notes/scramble-lemma.md`). Define r_q = q̄_q^{A} / q̄_q, the per-founder
   dependence correction [after review: an event-level ratio P(F_q | A)/P(F_q) is not the same quantity], so that
   Lemma D's unconditional q̄_q can be used once r_q is bounded. The RE's expectation is that the dependence between A
   and a founder's survival runs through the shared background path (ALLC exposure helps the target and an
   ALLC-cooperating faker alike, a positive association) and through slot competition (negative); neither sign is
   proved. Do: (a) *measure* r_q in the instrumented kernel (co-seed one target copy and one faker copy, 3,000
   backgrounds, N = 100, 400, 1,600, n = 6, 9, 12, the three faker types), recording the background duration and
   exposure so the association can be decomposed; (b) state any inequality you can prove for r_q (e.g. conditional on
   the background path, under an explicit exchangeability or negative-association hypothesis, with the hypothesis
   named as an assumption); (c) recompute the 18 cells of the combined bound with Lemma D's q̄ and the measured r,
   labelled as a **confidence-qualified empirical bound, not a theorem**, and extrapolate the sum
   Σ_q N μ_q q̄_q r_q h_q in N with the measured h(N).

3. **The establishment formula.** Combine (i) near-neutrality of a prover lineage during the scramble, so
   E[k_τ | E] ≈ k₀·(1 − curvature loss) (the supermartingale from the fitness curvature above, plus the deficit
   −x_D·x_o from the remainder; both integrated over the scramble and bounded, not assumed away) [after review], with
   (ii) the escape probability of one copy from a D sea under s(f) ≈ c·f, c = w·(R − P): the Kimura/Moran diffusion
   gives u₁ ≈ (1/N)·√(2Nc/π) = √(2c/(πN)) when Nc ≫ 1 (backward equation u'' = −N·s(x)·u', u' ∝ exp(−N c x²/2)), and
   (iii) [after review] the post-scramble state: a survivor's size at τ is broad (a critical lineage conditioned on
   survival has mean size of order d_min·τ), and the escape probability from k copies, u_k ≈ 1 − (1 − u₁)^k, is
   concave in k, so E[u_{k_τ}] < u₁·E[k_τ]; the gap is largest at small N (at N = 100, u₁ ≈ 0.044 and k ≈ 15 give
   0.49 against 0.65) and shrinks with N, which would make the *local* exponent exceed 1/2. The naive formula
   **p(N) ≈ μ_est·√(2cN/π)** (0.10 at N = 100, 0.20 at N = 400 with μ_est = 0.023 and c = 0.3, against the measured
   0.083–0.092 and ≈ 0.19) is therefore an upper envelope; the prediction is the corrected one.
   Do: (a) derive u₁ for the kernel (Moran birth–death, f = e^{w·payoff}; state the diffusion's drift and variance per
   generation explicitly, and the small-Nc correction through erf(√(Nc/2))), and benchmark the direct D-sea
   simulation against the **exact finite-N birth–death fixation formula** for the kernel (product of ratios of
   transition probabilities, with the self-interaction convention stated) [after review]; (b) measure u_k directly by
   seeding k = 1, 2, 4, 8, 16 prover copies into an all-D island at N = 100, 400, 1,600, 6,400 (10⁴ runs per cell at
   the small N, fewer at 6,400) and compare with both u₁·k and 1 − (1 − u₁)^k; (c) in the iid lottery, save per island
   k_τ for every seeded establisher founder, cap crossings, background exposure ∫x_A dt and the stopping reason;
   report E[k_τ | E] per seeded copy split by establishers that cooperate with ALLC versus those that exploit it (the
   latter are above the mean during the scramble), and compare E[u_{k_τ}] with u₁·E[k_τ]; (d) predict p(N) from the
   measured post-scramble state distribution with the multi-type escape function (compatible establishers pool their
   frequency-dependent advantage; distinguish "any compatible family fixes" from "this labelled target fixes" [after
   review]) and compare with the measured per-island chance at N = 100, 400 and a new N = 1,600 cell (iid lottery,
   I = 1, n = 9, 2,000 runs), reporting the ratio and the fitted exponent over N = 100–1,600; (e) state the formula's
   domain (N μ_est u₁ ≪ 1) and its saturation: the independent-founder form 1 − exp(−μ_est √(2cN/π)) gives 0.56 at
   N = 6,400 and n = 9 before scramble losses and spoilers, while the pooled-family diffusion started at frequency
   μ_est gives u(μ_est) ≈ erf(μ_est √(Nc/2)) / erf(√(Nc/2)) ≈ 0.69 [after review: sol's form]; say which fits the
   (6,400, 4) lottery cell (measured 1.00 for the island set, i.e. 1 − (1 − p)⁴, which discriminates poorly) and
   add a (6,400, 1) cell with 200 runs so the two can be told apart.

## Required outputs

`notes/demographic-lemma.md` (the proofs, with a dependency ledger: proved / coupled / measured / assumed),
`runs/demographic-lemma.md` and `.json` (every measurement with intervals), code under `src/` (extend
`src/scramble_lemma.py` rather than copying it), a predictions file written from the spec before any run, and the
usual hand-back: draft RESULTS section, REJECTED entries, THEORY/DEFERRED/NOTATION edits, ≤ 5 lines on what matters,
branch name from `git branch --show-current` and commits. Work in small steps and write the notes incrementally; do not
reason for long stretches without writing to a file. ≤ 3 worker processes.

## RE predictions (with falsifiers)

1. **Lemma D holds with d_min ≥ 0.9 per generation for lineages that stay below N/20**, and the ghost control is within
   a factor 1.3 of 1/(1 + t) at every fixed t ≥ 5 at N = 400 and 1,600. *Falsifier:* measured ghost survival exceeds
   the proved bound at any (N, t) by more than its 95% interval, or the ratio to 1/(1 + t) is outside [0.5, 1.3] at
   some t ≥ 5.
2. **r_q ∈ [0.8, 1.6] in every cell, larger for ALLC-cooperating fakers than for D-cooperating ones** [after review:
   sol expects no universal interval; the RE keeps a numerical prediction so it can fail], and the recomputed
   empirical bound is **positive in all 18 cells** and extrapolates positive to N = 10⁴ for every member of P.
   *Falsifier:* any r_q outside [0.6, 2], or the bound non-positive in more than 2 of 18 cells, or the extrapolated sum
   exceeds 1 below N = 10⁴ for FairBot's family (which has no fakers and so should give 0 identically; that cell is
   the sanity check).
3. **The corrected establishment formula (curvature loss, broad k_τ, concave u_k) holds within a factor 1.25 at
   N = 100, 400, 1,600** (ratio measured/predicted in [0.8, 1.25]), the naive square-root formula overestimates by
   10–40% at N = 100–400, and the fitted exponent over N = 100–1,600 is in [0.45, 0.65]. The direct u₁ measurement is
   within a factor 1.2 of the diffusion value with the erf correction at every N, and the exact finite-N formula
   agrees with the simulation within intervals. *Falsifier:* corrected ratio outside [0.6, 1.6] at any N, or exponent
   outside [0.4, 0.7], or u₁ off by more than a factor 1.5.
4. **E[k_τ | E] per seeded copy is 0.75–0.95 for ALLC-cooperating establishers** (the curvature loss of about
   1 − 1/cosh(0.15) per generation over τ, partly offset because the loss shrinks as ALLC dies) **and > 1.2 for
   ALLC-exploiting ones.** *Falsifier:* the ALLC-cooperating value outside [0.6, 1.05].
5. [after review] **Saturation at N = 6,400 follows the independent-founder form (≈ 0.56 before scramble losses and
   spoilers) rather than the pooled-family form (≈ 0.69)**, because the seeded establisher copies are separate
   lineages that must each survive the scramble before they can pool. *Falsifier:* the (6,400, 1) cell above 0.66
   or below 0.35.

The RS is invited to add predictions; the RE's uncertain ones are 3's constant and 5 (sol's pooled form against the
RE's independent-founder form; the measurement in (b) and (c) decides it).
