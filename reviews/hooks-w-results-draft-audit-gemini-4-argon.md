# Review of `/private/tmp/claude-501/-Users-jstav-code-program-ecologies/eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/hooks-w-results-draft.md` by gemini-4-argon

- **Draft sentence:** "Behaviour fills die with their carriers: at generation 1,000 history fills are all of the held fills in every hooked cell, and behaviour fills are never executed."
- **Evidence:** In `runs/hooks-w.md` ("Held fills, gentle programs and majority bases"), held shares by scope at generation 1,000 are `0.00, 0.00, 0.99, 0.01` in `hist-noinherit` and `0.00, 0.00, 0.98, 0.02` in `no-history-renorm` (so behaviour fills are 1%–2% of held fills there, not 0%). In "Fill levels per sampled encounter", behaviour fills are executed at `0.001` per encounter in `no-history-renorm` and `ff-grudge-only` (and only `0.000` to three decimal places in other cells).
- **Correction:** Change to: "at generation 1,000 history fills are ≥ 98% of the held fills in every hooked cell (100% in maximal), and behaviour fills are executed at ≤ 0.001 per encounter (0 in maximal)."

- **Draft sentence:** "Wait / Union game table and Verdicts W13: `baseline (stored kernel) | 0 | 0 | 0.77 | 0.23 | –`"
- **Evidence:** `runs/hooks-w.md` ("Social organization cells") also reports a `plain` cell (the new union-game module run with the plain grammar) with zero wage `0.816`, strike `0.050`, and scab split `0.134`, alongside `baseline` (`0.767`, `0.000`, `0.233`). Inaddition, the table omits the `strike` column, which is non-zero in `inert` (`0.045`), `seeding-only` (`0.013`), and `no-history` (`0.022`), making the row shares not sum to 1.
- **Correction:** Include the `plain` cell (or note its 0.82 zero-wage / 0.05 strike / 0.13 scab-split shares in the text/table) and note that the remaining island share in `inert`, `seeding-only`, and `no-history` (0.01–0.05) is in the `strike` outcome.

- **Draft sentence:** "PD ablation cells are compared at generation 1,000; only baseline, inert and maximal ran to 2,000."
- **Evidence:** `runs/hooks-w.md` reports `maximal (2,000)` (where efficient runs are 0.100, universal-open rises from 0.000 to 0.025, and P(C,C) is 0.492), as well as `no-behaviour-renorm` and `no-history-renorm`, none of which are mentioned in the PD results section.
- **Correction:** Briefly report the generation-2,000 numbers for `maximal` (universal-open 0.025, P(C,C) 0.49) and note that the prior-renormalized scope ablations (`no-behaviour-renorm` 0.00, `no-history-renorm` 0.825 universal-open) match the unrenormalized ablations.
