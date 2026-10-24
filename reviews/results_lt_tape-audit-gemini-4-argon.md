# Review of `/private/tmp/claude-501/-Users-jstav-code-program-ecologies/eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/results_lt_tape.md` by gemini-4-argon

1. **Draft:** "**Deviations.** ... Islands are only partly settled (support unchanged from 1,500 to 2,000 on 0.2–0.6 of islands)..."
   **Evidence:** In `runs/lt-tape.md`, the `resolved` fraction in primary cells goes down to `0.16 [0.11, 0.23]` (`insp_only` free) and up to `0.64 [0.51, 0.77]` (`prand` c0) (and `0.82`–`0.92` in post-hoc cells).
   **Correction:** Change `0.2–0.6` to `0.16–0.64` (in primary cells).

2. **Draft:** "**Inspection.** ... Only the inspectee reads: committed and compliant 0.974 [0.923, 1.000] (the DSL: 0.91)..."
   **Evidence:** `predictions/2026-10-24-realizable-randomizer.md` makes renormalized arms **co-primary** wherever disabled-template defaults shift a founder share by more than 0.05. In `notes/lt-tape.md` §2.2, `ee-only` shifts inspector `N` by 0.115 (`insp-only` shifts `C` by 0.173; `notape` and `noprover` also exceed 0.05). In `runs/lt-tape.md`, `ee_only (renorm)` free has committed+compliant `0.868 [0.765, 0.965]` (and at c0 `0.953`, carrier share `0.419`); `insp_only (renorm)` free has efficient `0.215` and inspector payoff `-0.721`. The draft omits the co-primary renormalized figures entirely.
   **Correction:** Report the co-primary renormalized values beside the default-in-place values for arms with founder shift > 0.05 (at minimum `ee_only (renorm)`: committed+compliant `0.868 [0.765, 0.965]`, carrier share `0.497`; `insp_only (renorm)`: efficient `0.215`, payoff `-0.721`).

3. **Draft:** "**Chain:** inspector payoff −0.36 to −0.42 against −0.07 in the lottery; the two objects disagree, as in the DSL."
   **Evidence:** In `runs/lt-tape.md`, `−0.36 to −0.42` is for the `full` arm across `N ∈ {100, 1000, 10000}` (`-0.359` to `-0.421`), and `−0.07` is specifically the `full` free lottery cell (at `c0`, the lottery inspector payoff is `-0.137`). Other chain arms have payoffs from `-0.263` (`nosim`) to `-0.810` (`ee_only`).
   **Correction:** Specify that these numbers are for the **full arm** (`−0.36 to −0.42` across N = 100..10⁴, against `−0.07` free / `−0.14` at c₀ in the lottery).

4. **Draft:** "**Verdicts.** Held: 1 (soundness, adversarial certificates, the hash control)..."
   **Evidence:** `predictions/2026-10-24-realizable-randomizer.md` P1(c) registered "half the best response 2/3", which was false for 3 of the 6 biased mixers (`B_RS`, `B_PR`, `B_SP`, where best response is 1/3) and withdrawn in `notes/lt-tape.md` §2.5.
   **Correction:** Note in Verdict 1 or Deviations that P1(c)'s parenthetical ("half the best response") was withdrawn as an erratum while the 1/3 payoff held.
