# Review of `notes/length-prior-t-RESULTS-draft.md` by gemini-4-argon

- **Draft sentence:** "Predictions `predictions/2026-11-08-length-prior-t.md` were committed before any counted cell of step 2 and before the final step-1 enumerations and Monte Carlo; pilots (V1 and V2, a one-cell timing, an R0 enumeration to size 4 and an R1 targeted search whose class table I read) are disclosed there, as are 14 Daytona pilot cells of the counted grid (identical on re-run)."
  - **Evidence:** `predictions/2026-11-08-length-prior-t.md` discloses only one timing run (`2a:d=0.03:b=0`, N = 200, I = 64, run 0) and explicitly states "no other new-law cell was run". The 14 Daytona pilot runs (14 runs across two cells: `2a, delta 0.03, beta 0; N = 100 runs 0-11, N = 400 runs 0-1`) are disclosed in `notes/length-prior-t.md`, not in the predictions file.
  - **Correction:** State that the 14 Daytona pilot runs are disclosed in `notes/length-prior-t.md` (and clarify they are 14 runs across two cells, not 14 cells).

- **Draft sentence:** "| other conditionals (R1) / constants-with-reads | 2.6e-6 / 1.7e-5 | 0.153 / 0.041 |"
  - **Evidence:** The table has columns for both R0 and R1, and this row reports R0 values (`2.6e-6 / 1.7e-5`) and R1 values (`0.153 / 0.041`), so the `(R1)` label in the row stub is misplaced.
  - **Correction:** Change the row label to `other conditionals / constants-with-reads`.

- **Draft sentence:** "Reproduction (1,000 non-junk sampled programs per machine, 30 sampled partner pairs each): every constant and every exact-member reader / bully reproduces its sampled interactions (24/24 single, 10/10 bully, 28/28 two-partner exact classes); the family-level classes that are not exact members mostly do not (R0 single 11 / 36, bully 20 / 28, two 0 / 12; R1 single 3 / 26, bully 0 / 12)..."
  - **Evidence:** `notes/length-prior-t.md` reports for R1 family-level non-exact classes: `R1: single 3 / 26, bully 0 / 12, two 0 / 12`. The draft omits `two 0 / 12` for R1.
  - **Correction:** Add `, two 0 / 12` to the R1 family-level list.

- **Draft sentence:** "Founders and tail copies bind together (200, 64, delta 0.03: founders only 0.95, tail only 0.70, both 0.90; at c = 64 each alone 0.65 at (200, 64))..."
  - **Evidence:** `runs/length-prior-t.md` (under *Independent founder / tail copies at c = 64*) reports `(200, 64) 0.65 / 0.65 / 0.76` (and `(200, 256) 0.65 / 0.55 / 0.75`). In the draft, omitting the `0.76` "both" value at `c = 64` while pairing it with the `0.95 / 0.70 / 0.90` cell (where founders alone at 0.95 beat both at 0.90) leaves the claim that they "bind together" unsupported by the numbers cited in the sentence.
  - **Correction:** Include the `both 0.76` figure for `c = 64` at `(200, 64)` (and optionally `(200, 256): 0.65 / 0.55 / 0.75`), and distinguish the `delta = 0.03` slice (where founders carry most of it) from `c = 64` (where neither binds alone at $N \ge 200$).
