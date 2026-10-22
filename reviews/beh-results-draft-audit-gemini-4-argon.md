# Review of `/private/tmp/claude-501/-Users-jstav-code-program-ecologies/eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/beh-results-draft.md` by gemini-4-argon

1. **Draft:** "...notes `notes/hooks-beh.md` (§2: every deviation, declared before the counted cells)..."
   **Evidence:** `notes/hooks-beh.md` §2.5 is titled "Run record and changes after the declaration in 2.3" and documents mid-queue changes made after seeing the initial run times and results: cutting `beh-max-noA`, `beh-max-hostile`, `beh-written-only`, and `M5-sham` from 30 to 20 runs; killing `ff-beh-max` after the 6th run; and adding the `inert` control after seeing that plain provers won many `beh-max` islands.
   **Correction:** Change to "(§2: every deviation, with mid-queue cuts and the added `inert` control in §2.5)".

2. **Draft:** "...fission–fusion 6 of a planned 10 (16 × 100, merged at 200, horizon 400); N = 200 at (200, 8), 10 runs."
   **Evidence:** `notes/hooks-beh.md` §2.3 states the spec's geometry and run counts for these cells: fission–fusion was specified as 32 × 100, merged into 3,200, horizon 600, 20 runs (first reduced to 10 in §2.3, then cut at 6 in §2.5); N = 200 was specified as horizon 2,000, 20 runs (reduced to horizon 600, 10 runs).
   **Correction:** State the spec's targets alongside the reduced geometries and run counts: "fission–fusion 6 of a spec-planned 20 (16 × 100 merged at 200, horizon 400, against 32 × 100 and horizon 600); N = 200 at (200, 8) and horizon 600, 10 runs (against horizon 2,000, 20 runs)."

3. **Draft:** "Run by a Sonnet subagent (`src/hooks_beh*.py`, 17 tests)."
   **Evidence:** `notes/hooks-beh.md` §2.2 states: "tests `tests/test_hooks_beh.py` (17) and `tests/test_hooks_beh_kern.py` (20)."
   **Correction:** Change "17 tests" to "37 tests (17 + 20)".

4. **Draft:** "Hostile constructions at 10× prior mass, and written-only behavioural keys, were also run (`runs/hooks-beh.md`)."
   **Evidence:** `runs/hooks-beh.md` reports `beh-max-hostile` universal-open 16/20 = 0.800 and `beh-written-only` 18/20 = 0.900 (higher than `beh-max`'s 0.700 when seeded behavioural fills are removed). The draft omits their universal-open shares.
   **Correction:** Report the outcomes: "`beh-max-hostile` gives 16 of 20 (0.80) and `beh-written-only` gives 18 of 20 (0.90)."

5. **Draft:** "On winning islands at generation 200, FairBot-equivalents through a fill number 1,876 and PrudentBot-equivalents 0. FairBot- or PrudentBot-equivalents through a fill are 0.003 of winners (0.044 counting unhooked FairBot-equivalents), and about 59% of winners fall in no named panel class."
   **Evidence:** `runs/hooks-beh.md` (Prediction 5 and M1): 1,876 is the total FairBot-equivalent count on winning islands at generation 200, not "through a fill" (M1 shows 1,872 of 2,373 FairBot-equivalents at gen 200 have deciding origin `none`, i.e., unhooked). Second, Prediction 3's 0.003 (and 0.044) is measured on winning islands *at the end* (generation 500), whereas M1's 59.3% `other` is across *all* islands at generation 200 (at generation 500, `other` is 61.7%).
   **Correction:** Separate the generation-200 and end-of-run statistics, drop "through a fill" from 1,876 (note that most are unhooked), and clarify that 59% (62% at gen 500) is the run-averaged share across all islands.
