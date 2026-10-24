# Review of `/private/tmp/claude-501/-Users-jstav-code-program-ecologies/eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/results_mixed2.md` by gemini-4-argon

1. **Unreported deviation on `sr_k` controls and Prediction 4.**
   - *Draft:* "and the inspection controls `sr_4`, `sr_16`." / "- *Reading is graded by information:* exact > sr_16 > sr_4 > matched > blind; exact − matched 0.343 [0.175, 0.506]." / "Held: ... 4 (graded ordering, exact − matched 0.343)"
   - *Evidence:* `specs/2026-10-23-two-role-mixed.md` specified `sr_4` and `sr_16` as "inspectee controls in the inspection exact arm" to test whether "the commitment payoff is graded in the responder's information". However, `notes/mixed2.md` §2.5 discloses that `sr_k` replaced `cr` in **both** roles, "not only for the inspectee". Furthermore, in `sr16` (`runs/mixed2.md`), `islands at (0,0)` is 0.023 (vs 0.648 in `exact`, 0.265 in `sr4`, and 0.321 in `matched`), while `islands committed+compliant` jumps to 0.196 (vs 0.109 in `exact` and 0.008 in `sr4`).
   - *Correction:* Disclose in Deviations that `sr_4` and `sr_16` replaced `cr` in both roles rather than acting as inspectee-only controls, and note under Inspection / Verdicts that the graded payoff ordering across `exact`, `sr_16`, `sr_4`, and `matched` reflects a shift between the reactive `(0, 0)` regime (`exact`, `sr_4`, `matched`) and commitment (`sr_16`), not simply inspectee responder precision.

2. **Omitted `islands at (0, 0)` values and missing `sample` arm in Inspection lottery.**
   - *Draft:* In the inspection lottery table, the `islands at (N, C) = (0, 0)` column is left blank for `sr_4 / sr_16` and states `(0.91 committed and compliant)` instead of the `(0, 0)` share for `only the inspectee reads`; the `sample` arm is omitted from the inspection lottery section.
   - *Evidence:* `runs/mixed2.md` gives `islands at (0,0)` as `0.265` for `sr4`, `0.023` for `sr16`, and `0.002` for `exact_ee` (`c = 0`); `insp sample` has game payoff `-0.641` (`c = 0`, `0.260` at `(0,0)`) and `-0.679` (`c = 0.01`, `0.247` at `(0,0)`).
   - *Correction:* Fill in `0.27 / 0.02` for `sr_4 / sr_16` and `0.002` for `only the inspectee reads` in the table, and report the `sample` arm (`-0.641` at `c = 0`, `0.26` at `(0,0)`).

3. **Unverified chain numbers in Inspection.**
   - *Draft:* "with inspector mass above 1/4 at 0.54 and the reactive pair at 0.06–0.14."
   - *Evidence:* `runs/mixed2.md` chain tables do not contain columns for inspector mass above 1/4 or reactive-pair share (only `u0`, `u1`, `p / bluff`, `q / call`, `readers (1)`, `mixing 0`, `mixing 1`).
   - *Correction:* Verify these numbers against `runs/mixed2/*.json` or replace them with statistics present in `runs/mixed2.md` (e.g., `p = 0.28–0.44`, `q = 0.05–0.17`).

4. **Difference between net and game payoffs.**
   - *Draft:* "Payoffs are game payoffs (net differs by at most 0.003 in the cells reported)."
   - *Evidence:* `runs/mixed2.md` reports `insp exact, c = 0.01` game payoff `-0.207` vs net `-0.215` (diff `0.008`), `size` game `-0.376` vs net `-0.382` (diff `0.006`), `insp sample, c = 0.01` diff `0.005`, `insp matched, c = 0.01` diff `0.004`, and `end exact, c = 0.01` II price paid `0.006`.
   - *Correction:* Change "at most 0.003" to "at most 0.008".

5. **Endgame lottery CI and `c` label for `sample`.**
   - *Draft:* "value to I −0.148 [−0.194, −0.102]" and "Matched −0.03, sample −0.14, blind −0.149."
   - *Evidence:* `runs/mixed2.md` lottery table for `end exact, c = 0.01` gives `[-0.195, -0.100]` (`[-0.1937, -0.1025]` is in the verdict JSON from a separate bootstrap draw). For `end sample`, game payoff is `-0.142` at `c = 0.01` and `-0.122` at `c = 0`.
   - *Correction:* Align the CI with the table (`[-0.195, -0.100]`) and specify the price for `sample` (`-0.142` at `c = 0.01`, `-0.122` at `c = 0`).
