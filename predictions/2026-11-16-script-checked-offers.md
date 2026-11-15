# Predictions: script-checked offers in majority division (queue 80), 2026-11-16

Spec: `specs/2026-11-16-script-checked-offers.md` (reviewed by gemini-4-carbon, then gpt-6.1-sol `--mode amended`, both
folded). Per the spec's amendment "Registration in two commits", this file is committed in two stages: RE 1 now, before
construction of the checker begins; RE 2–12 and the subagent's E-series after the gates and before any step-0 assay, mass or
counted step-2 cell. All step-2 statistics will be finite-schedule approach-rate statistics, not π.

## Stage 1 (committed before any construction)

Disclosure: before this commit I read the spec, the two reviews, and queue 79's run report and notes. No code for this queue
has been written or run.

- **RE 1 (the checker can be built).** S0 exists, is sound (G1) and accepts every listed spelling (G2), at a worst accepted
  cost between 10³ and 10⁵ steps. Falsifier: any false acceptance, or a listed spelling with no acceptable script, or the
  time box (two days of engineering).

Scoring rule (registered): RE 1 holds iff all three of (a) 0 false acceptances on S0 and S1 over the catalogue cube and every
forger rejected, (b) every listed spelling accepted with a script, (c) the worst accepted S0 check cost κ_S lies in
[10³, 10⁵] steps. If (a) and (b) hold and (c) fails, RE 1 fails on cost without its falsifier firing; that will be said.
