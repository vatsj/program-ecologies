# Review of `/private/tmp/claude-501/-Users-jstav-code-program-ecologies/eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/results_audit.md` by gemini-4-argon

1. **Draft sentence:** `| one-population modal hd3, N = 10⁴ | 0.016 | 0.183 at 5,469 states (converged) |`
   **Evidence:** `specs/2026-10-24-exploration-audit.md` and `predictions/2026-10-24-exploration-audit.md` specify: `Results are labelled monomorphic-complete, polymorphism-search-limited when (c)–(d) ran, and stable under this enlargement when only (b) ran; neither is called converged.`
   **Correction:** Replace `(converged)` with `(0 candidates left; stable under this enlargement)`.

2. **Draft sentence:** `The engineer's E2 and E3 failed (the mover was a one-population cell).`
   **Evidence:** In `predictions/2026-10-24-exploration-audit.md`, E2 and E3 are framed around M-status (monomorphic-complete) vs R-status (monomorphic-restricted) cells, not one-population vs multi-role: E2's falsifier is `none of these five moves by more than 0.05 while some M-status cell does` and E3's is `any other M cell moves by more than 0.02`. `runs/exploration-audit.md` states: `the mover was an M-status one-population cell whose cap limits the polymorphic search`.
   **Correction:** Change the parenthetical to `(the mover was an M-status one-population cell whose cap limits the polymorphic search)`.

3. **Draft sentence:** `A1. ... hd6 at N = 10^3 failed numerically at 12,000 states, and hd3 at N = 10^3 failed the same way at a 24,000-state cap after 1.5 h (onepop_chain finds no recurrent class in the capped set: np.argmax of an empty sequence) ...`
   **Evidence:** `notes/exploration-audit.md` §2 records that for `hd6 N = 10^3 at 12,000 states`, `the exit-analysis step found no recurrent class in the capped set; the solve itself had finished`.
   **Correction:** Clarify that for hd6 at N = 10^3 the solve finished, and it was the exit-analysis step in `onepop_chain` that failed with no recurrent class in the capped set.
