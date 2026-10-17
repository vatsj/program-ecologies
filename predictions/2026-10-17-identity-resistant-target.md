# Predictions: an identity-resistant target (narrowing the PrudentBot network to members identity cannot exploit), 2026-10-17

Spec `specs/2026-10-17-identity-resistant-target.md` (reviewed by gpt-6.1-sol and gemini-4-argon; the amendments
supersede the earlier text). Notes `notes/identity-resistant.md` §1 (committed before any code). Written and committed
before any code of this run and before any counted cell. ε = 0 cells are lottery statistics at finite (N, I, horizon);
rain cells are finite-ε approach-rate diagnostics, never π. R-move (Rm) and the R-proportional control (Rp) are
counterfactual surgery on the mutation prior (amendment 1), not designs; the realizable claim is judged on the arms
under L.

*Disclosure.* RE 1 concerns a static property that the notes' §1 lookup has already computed (50 of 70 resistant units
guarded; 0 of 165 exploitable units guarded). It was registered in the spec before that lookup; its verdict is
determined by §1, not by a cell, and is reported as such.

## The RE's predictions (verbatim from the spec, with the revision marks)

1. **Resistance is mostly a syntactic property** [revised after review: resistance is defined semantically; the
   syntax is a test of it]: the certified self-cooperation guard is sufficient for resistance, and ≥ 0.9 of resistant
   units carry it; exceptions are listed. *Falsifier:* < 0.7 carry it, or any guarded unit exploitable.
2. **Fission–fusion is universal-open in ≥ 0.95 of runs under every prior, and universal on target (235) in ≥ 0.9 with
   the sponsored founder under L** [revised after review: the Pangaea result was universal-open, and open rivals are not
   identity prey, so the sponsor carries the target]. *Falsifier:* universal-open ≤ 0.8, or sponsored uot under L ≤ 0.7.
3. **R-move alone on islands does little at ε = 0:** (200, 64) uot within 0.1 of L, because identity's main channel at
   ε = 0 is the seed's own islands. *Falsifier:* a gain ≥ 0.25.
4. **R-move closes the prey channel under rain** [revised after review: the combined bound and the cross-regime uot
   claim are dropped]: selected identity takeovers of target islands per identity arrival fall to ≤ 0.2 of L's.
   *Falsifier:* ≥ 0.5 of L's.
5. **The control does not do it:** the R-proportional control's identity takeovers under rain stay ≥ 0.5 of L's.
   *Falsifier:* ≤ 0.2.
6. **Counter-predictions registered.** *Sol:* semantic resistance is not captured by the syntax; under rain direct prey
   takeovers decline but the combined bounds fail; the sponsor matters materially and unsponsored R-move can be
   universal-open without being on target. *Gemini:* semantic resistance strictly contains the syntactic signature,
   violating it on > 10% of resistant units; R-move may work by founder boosting rather than channel closing.

## Scoring conventions (declared now; they do not change the wording above)

Definitions are notes §1.2 (exploitable / resistant, challenge set 𝒬 frozen), §1.7 (uot₂₃₅, uot₇₀, universal-open on
islands and on the merged population, identity takeovers and their attribution, per-arrival and per-island-generation
rates). Paired comparisons across priors use the same replicates (0–19, or 0–39 in Part III).

- **RE 1** (static): *supported* if ≥ 0.9 of resistant units are guarded and no guarded unit is exploitable;
  *contradicted* if < 0.7 are guarded or any guarded unit is exploitable (semantic exploitability, ideal table or
  executed); *inconclusive* otherwise. "Exceptions are listed" is met by the notes' list.
- **RE 2** (Part I, horizon 2,200): "every prior" means L, Rm and Rp, unsponsored and sponsored (six cells).
  *Supported* if universal-open ≥ 19/20 in all six cells and sponsored-L uot₂₃₅ ≥ 18/20; *contradicted* if
  universal-open ≤ 16/20 in any cell or sponsored-L uot₂₃₅ ≤ 14/20; *inconclusive* otherwise. (The two clauses are
  also reported separately.)
- **RE 3** (Part II, unsponsored, uot₂₃₅ at 10,000): gain g = (uot_Rm − uot_L)/20 (paired). *Supported* if |g| ≤ 0.10;
  *contradicted* if g ≥ 0.25; *inconclusive* otherwise (0.10 < g < 0.25, or g < −0.10). The sponsored arms and uot at
  2,000 are reported beside it.
- **RE 4** (Part III): the rate ρ_X = (prey identity takeovers of target islands) / (identity arrivals), pooled over
  (800, 8) and (1,600, 8) and both schedules, for X = L and Rm; ratio ρ_Rm / ρ_L. *Primary (counts):* if L has ≥ 3
  prey takeovers, *supported* if the ratio ≤ 0.2, *contradicted* if ≥ 0.5, *inconclusive* otherwise. *If L has < 3*
  (expected, notes §1.10): the count verdict is *inconclusive* and the prediction is scored on the **composite**
  per-arrival rate κ_X = mean over identity arrivals of P_M1(takeover | class of the island's holder at arrival), with
  P_M1 from the M1 assay at the arrival's N (exploitable holder: the pooled exploitable-holder takeover probability;
  resistant holder or not a target island: the pooled resistant-holder probability, or 0 if the island is not a target
  island); same thresholds on κ_Rm / κ_L. Both are reported. **Extension (amendment 8):** none — the counts are
  limited by the channel's rarity under L, not by replicates, and the composite is the decisive reading.
- **RE 5** (Part III, (800, 8) only, where Rp runs): identity takeovers of target islands (all attributions, in total
  and per identity arrival), Rp against L, pooled over both schedules. If L has ≥ 3: *supported* if Rp / L ≥ 0.5,
  *contradicted* if ≤ 0.2, *inconclusive* otherwise. If L has < 3: *inconclusive* on counts, and scored on the
  composite κ_Rp / κ_L with the same thresholds.
- **Sol** (four clauses, each scored): (a) syntax misses semantics: *held* if any resistant unit is unguarded;
  (b) under rain direct prey takeovers decline under Rm (ρ_Rm ≤ ρ_L, or κ_Rm < κ_L) but "the combined bounds fail"
  (read: Rm does not raise uot₂₃₅ under rain by ≥ 0.1 at both N): *held* if both; (c) the sponsor matters materially:
  *held* if sponsored − unsponsored uot₂₃₅ ≥ 0.15 (paired) in at least one of Parts I and II under L; (d) unsponsored
  Rm can be universal-open without being on target: *held* if some unsponsored Rm run (Parts I or II) is universal-open
  at its horizon and not uot₂₃₅.
- **Gemini** (two clauses): (a) semantic resistance strictly contains the syntactic signature with > 10% of resistant
  units unguarded: *held* if no guarded unit is exploitable and > 7 of 70 are unguarded; (b) "R-move may work by
  founder boosting rather than channel closing": *held* if in Part II Rm's uot gain over L is accompanied by a fall in
  closed-open rival islands at 2,000 of ≥ 40% (founder boosting against non-identity rivals) while the exploitable
  target occupancy L has to lose is < 2% of target islands; *not supported* if Rm does not raise uot in Part II.

## The subagent's predictions (from notes §1.10; with falsifiers and regions)

S1. **The executed check agrees with the ideal table** on every (target, challenge) pair in both directions, so the
    partition is 165 / 70 under the union rule. *Falsifier:* any disagreement that changes a unit's class.
    (Supported: 0 class changes; contradicted: ≥ 1.)

S2. **Fission–fusion, unsponsored.** Universal-open ≥ 19/20 under L, Rm and Rp. uot₂₃₅: L 16–19, Rm 18–20, Rp 16–19.
    *Falsifier:* universal-open ≤ 17/20 in any prior, or Rm uot₂₃₅ < L uot₂₃₅ − 1. (Supported if every range holds;
    contradicted if a falsifier fires; inconclusive otherwise.)

S3. **Fission–fusion, sponsored.** uot₂₃₅ ≥ 19/20 under every prior. *Falsifier:* ≤ 17/20 in any prior.

S4. **uot₇₀ tracks uot₂₃₅ on the merged population:** uot₇₀ = uot₂₃₅ in ≥ 18 of 20 runs of every Part I cell
    (exploitable members are suckers and are gone before the merge); the exploitable target share of the merged
    population at 2,200 is ≤ 0.01 in every run. *Falsifier:* uot₇₀ ≠ uot₂₃₅ in ≥ 4 runs of some cell.

S5. **Part II, founder boosting.** Rm raises uot₂₃₅ at 10,000 over L by +3 to +7 runs (unsponsored); closed-open rival
    islands at 2,000 fall by ≥ 40% and identity islands by ≥ 30% (pooled over runs). *Falsifier:* uot gain ≤ +1 run,
    or closed-open islands fall by < 20%.

S6. **Part II, the control.** Rp's uot₂₃₅ at 10,000 is within ±2 runs of L (unsponsored and sponsored). *Falsifier:*
    |Rp − L| ≥ 4 runs in either.

S7. **Part II, sponsored.** L 15/20 (the stored value; this is reproduction); Rm 17–20. *Falsifier:* Rm < L.

S8. **M2 establishment.** Per seeded copy, resistant-target founders hold their island at 200 (Part I, L) at least 5×
    as often as exploitable-target founders. *Falsifier:* < 2×.

S9. **M1 assays.** TwinD into each exploitable holder takes over with probability ≥ 0.2 per arrival at N = 200 and
    800; into each resistant holder (guarded and unguarded) ≤ 0.003 (≤ 3 in 1,000). *Falsifier:* an exploitable holder
    < 0.1, or a resistant holder > 0.01.

S10. **Rain, counts.** Under L, prey identity takeovers of target islands total ≤ 3 in Part III (240 L runs); under
     Rm, 0. *Falsifier:* L ≥ 8 (the channel is not rare), or Rm ≥ 1 prey takeover (an exploitable target unit
     appeared under Rm, which the construction excludes; this would be a bug).

S11. **Rain, drift.** Drift colonizations of target islands per island: Rm ≥ L (pooled over cells); drift into
     unconditional cooperators per target island-generation: Rm / L in [0.7, 1.3] (pooled). *Falsifier:* Rm / L for
     unconditional-cooperator drift outside [0.5, 2].

S12. **Rain, identity islands.** Identity islands at 12,000 under Rm ≤ L (pooled per prior over schedules and N);
     Rp within ±30% of L. *Falsifier:* Rm > 1.5 × L.

S13. **Rain, uot.** uot₂₃₅ at 12,000 under Rm − L within ±0.15 at each N (pooled over schedules): the target at
     I = 8 already holds 95%+ of islands and its failures are seed cliques and scramble losses that R-move moves
     little. *Falsifier:* |Rm − L| > 0.25 at either N.
