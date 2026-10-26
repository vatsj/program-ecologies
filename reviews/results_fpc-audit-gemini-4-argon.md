# Review of `/private/tmp/claude-501/-Users-jstav-code-program-ecologies/eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/results_fpc.md` by gemini-4-argon

* **Draft sentence:** "The largest PD end-state charge per play in any priced run is 0.0039 (against the 0.3 cap), the scramble charge 0.0009."
* **Evidence:** In `runs/failure-pricing-confirm.md` (PD detail table), 0.0039 is the single-run maximum end-state charge (`max run` at A 0.1), whereas 0.00089 (0.000895 in the stakes table) is the *cell-mean* scramble charge per play (`scramble charge/play (g<=200)` at A 0.3 and A 1, with 95% CIs up to 0.00135), not a single-run maximum. The parallel phrasing equates a run-level maximum with a cell-level mean.
* **Correction:** Change "the scramble charge 0.0009" to "and the largest cell-mean scramble charge is 0.0009."

* **Draft sentence:** "At 0.3, 3 of 40 RPS runs are taken over by the prover `PB`, which forfeits on about 0.9 of its plays; a forfeit that exhausts the root fuel is not a timed-out read, so A does not charge it. ... (0.5: 0.619 [0.475, 0.759], with bimodal run-level fractions; no mechanism identified)."
* **Evidence:** `runs/failure-pricing-confirm.md` reports only the pooled cell-level shares and means: at A 0.3, `PB` is modal on 0.06 of islands and cell-mean forfeits are 0.056 [0.000, 0.126]; at A_s (0.5), inspection net efficiency is 0.619 [0.475, 0.759]. Neither the "3 of 40 RPS runs", the "0.9 of its plays" forfeit rate for `PB`, nor "bimodal run-level fractions" appear in the run report.
* **Correction:** Either add the run-level distributions and `PB`'s play-level forfeit rate to `runs/failure-pricing-confirm.md`, or replace these specifics in the draft with the reported cell summaries (e.g., "At 0.3, the prover `PB` becomes modal on 0.06 of RPS islands, lifting cell-mean forfeits to 0.056...").

* **Draft sentence:** "...and the engineer's E5, E6 and E9." (in the **Verdicts** paragraph, which omits E1–E4, E7, E8, and E10).
* **Evidence:** `runs/failure-pricing-confirm.md` (Verdicts table) scores ten engineer predictions: E1, E2, E3, E4, E7, E8, and E10 **held**, while E5, E6, and E9 **failed**. The draft lists only the three failures and omits the seven that held.
* **Correction:** In the "Held:" sentence of **Verdicts**, append "and the engineer's E1–E4, E7, E8 and E10."
