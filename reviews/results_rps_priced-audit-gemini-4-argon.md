# Review of `/private/tmp/claude-501/-Users-jstav-code-program-ecologies/eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/results_rps_priced.md` by gemini-4-argon

1. **Draft sentence:** "**Deviations.** Chain exploration threshold 10⁻⁸ (10⁻⁶ and 10⁻¹⁰ differ by about 10⁻⁴ at N = 10⁴; cut mass reported per cell)."
   **Evidence:** In `runs/rps-priced.md` §2 ("Chain sensitivities (N = 10^4, c = 0.01)"), across θ = 10⁻⁶, 10⁻⁸, and 10⁻¹⁰, the primary statistics (`e net`, `mixing`, `plays forfeited`, `pi(X)`) differ by at most 10⁻⁴ in the sample arm (where `mixing` goes from 0.8512 to 0.8511 and `pi(X)` from 0.8448 to 0.8447) and by 0.0000 in the pure, matched, and exact arms; it is `polymorphic mass` that sits around 10⁻⁴ (and changes by up to 2.7 × 10⁻⁴).
   **Correction:** Change "differ by about 10⁻⁴" to "differ by at most 10⁻⁴ on the headline statistics (and ~3 × 10⁻⁴ on polymorphic mass)".

2. **Draft sentence:** "`X` holds 0.87 / 0.84 of the population, all source-reading classes together 0.06 / 0.015; about 0.83 of islands are at least 95% `X`."
   **Evidence:** The statistic "about 0.83 of islands are at least 95% `X`" does not appear in `runs/rps-priced.md`, `notes/rps-priced.md`, or `predictions/2026-10-23-rps-priced.md` (whereas homozygosity is 0.969 / 0.948 and islands with `e net <= 0.05` is 0.876 / 0.817).
   **Correction:** Either add the "islands ≥ 95% `X`" statistic to `runs/rps-priced.md` (with its sample / exact breakdown) or remove the clause from the draft.

3. **Draft sentence:** "**Chain, c = 0.01.** π(`X`) is 0.24 / 0.43 / 0.84 / 0.98 at N = 10² / 10³ / 10⁴ / 10⁵ (prior mass 0.23): ..."
   **Evidence:** In `runs/rps-priced.md` §1 and §2, the prior mass of `X` (`prior X`) is 0.2206 (0.221) in the sample arm and 0.2275 (0.227) in the matched and exact arms. The draft gives the trajectory without naming which arm it is from (at two decimals 0.24 / 0.43 / 0.84 / 0.98 matches both sample 0.2392 / 0.4329 / 0.8447 / 0.9812 and exact 0.2449 / 0.4300 / 0.8384 / 0.9802), while stating "(prior mass 0.23)", which rounds only the exact/matched prior.
   **Correction:** Specify the arm or give both priors: "(prior mass 0.221 sample, 0.228 exact)".

4. **Draft sentence:** "Mixing peaks at c = 0.01 and falls at 0.05 (0.84 sample, 0.76 exact), because coin-guarded readers, which also mix, are priced out."
   **Evidence:** In `runs/rps-priced.md` §3, between c = 0.01 and c = 0.05 in the exact lottery, `mixing` falls by 0.091 (from 0.849 to 0.758), while `guarded` falls by only 0.013 (from 0.014 to 0.001) and `X` itself falls by 0.085 (from 0.843 to 0.758, with `classes alive` rising from 1.23 to 1.30 as constant polymorphisms survive on islands once readers are priced out, as noted in `predictions/2026-10-23-rps-priced.md` item 4). Even in the sample arm, `guarded` falls by 0.055 (0.055 to 0.000) while `X` also falls by 0.029 (0.870 to 0.841) and `mixing` falls by 0.086 (0.927 to 0.841).
   **Correction:** Change "because coin-guarded readers, which also mix, are priced out" to "because c = 0.05 prices out the coin-guarded readers (0.055 → 0 sample, 0.014 → 0.001 exact) and, with readers gone, leaves more islands in constant mixtures (`X` 0.87 → 0.84 sample, 0.84 → 0.76 exact)".
