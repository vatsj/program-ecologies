# Review of `notes/patient-accepters-RESULTS-draft.md` by gemini-4-carbon

- **Incomplete disclosure of Addendum 2 ("imported" redefinition):**
  - *Draft:* "Addendum 2 discloses that the exit classifier was changed after half the grid had been seen (slot roles taken from the seeded triple; all 200 seeded cells rerun, deterministic and identical)."
  - *Evidence:* Addendum 2 also changed the definition of "imported" from requiring the two holders to take their slots within one debounce window (`0.25N`) to requiring only that both presences began with migrants, "whatever the timing." This directly affects the 4,822 imported exits used to score `sol` and `E6`.
  - *Correction:* Add that Addendum 2 also dropped the `0.25N` coincidence window from the definition of "imported" (which scores `sol` and `E6`).

- **Incomplete report of `E4` falsifiers:**
  - *Draft:* "E4 falsified (bullies above 3 in 16% of R-paired fair islands with charged residents; the clean (R, C4) island is neutral)."
  - *Evidence:* `predictions/2026-11-14-patient-accepters.md` sets E4's falsifier at > 3 for *any* of four sub-claims. `step0.md` and `runs/patient-accepters.md` show three more fired: ⅔-demanders (`C2`/`C5`/`C8`) entering the excluded slot of R-paired fair islands reach `5.9`–`11.6` (and up to `20.8` in pair slots); R entering the unpaired slot of fair firm-reader islands (`FI`) reaches `5.93` (25% > 3); and R entering a pair slot of `FI` reaches `0.075` (failing the `< 0.01` prediction, though ≤ 3).
  - *Correction:* State all fired falsifiers in E4: bullies into R-paired fair islands (up to 22.6), ⅔-demanders into their excluded slots (up to 11.6), and R into `FI` out-slots (up to 5.9).

- **Ambiguous scope on "every reader" in the mutual-read gate:**
  - *Draft:* "with R as the victim and any reader in the excluded slot, the bully's read of R also times out. The bully drops R and names the reader at ½: fair (bully, reader) in 3/8 of reader triples, disagreement otherwise."
  - *Evidence:* `gates.md` shows `3/8` (9/24) holds only for `Fs`, `Ft`, and `O`. Other readers in the excluded slot give `1/2` (`B`: 3/6; `Po`: 6/12), `1/4` (`F2`: 3/12; `R`: 3/12, with 3 `W` unequal-other outcomes rather than `D`), `0` (`Pz`, `Q`, `X`), or stay bully-held unequal (`Jr`: 3/3).
  - *Correction:* Specify `3/8` is for single/two-partner readers and openers (`1/2` for `B`/`Po`, `1/4` for `F2`/`R` with some `W`, `0` for `Pz`/`Q`/`X`).

- **Omission of `E15` and `I = 256` scope:**
  - *Draft:* Lists `E1`–`E14` in Verdicts (omitting `E15`); states `(and I = 256 for F+R)` under Step 2.
  - *Evidence:* `runs/patient-accepters.md` scores `E15` ("fails, falsifier not fired" because carbon (b) was false). `step2_report.md` also ran `F` at `I = 256`.
  - *Correction:* Add `E15 fails, falsifier not fired` to Verdicts, and write `(and I = 256 for F and F+R)`.

- **Unverified CPU-hours:**
  - *Draft:* "About 98 sandbox-CPU-hours (86 of cell time) plus about 1 local CPU-hour."
  - *Evidence:* Not present in the provided run files (presumably in `notes/patient-accepters.md`). Verify against `notes/` before commit.
