# Review of `/private/tmp/claude-501/-Users-jstav-code-program-ecologies/eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/results_insp_shadow.md` by gemini-4-argon

- **Draft sentence:** "The never-inspecting `N`, a payoff twin of the responsive inspector `cr(THEM(ME))` against compliant inspectees, leaves R at 0.155/N per mutation event (measured slope −1.07). It is the largest exit from R only at N = 10³."
  - **Evidence:** In `runs/inspection-shadow.md`, 0.155/N is the reference one-state hazard at `(CRI, C)` (1.55e-03, 1.55e-04, 1.55e-05, 1.55e-06 at N = 10²–10⁵, slope −1.00). The stationary conditional exit hazard from R (category A) is 1.495e-03 / 1.365e-04 / 1.137e-05 / 1.002e-06 at N = 10² / 10³ / 10⁴ / 10⁵, which has the measured slope −1.07, and category A is the largest exit at both N = 100 and N = 1000.
  - **Correction:** Separate the one-state rate from the stationary hazard, and include N = 10²: "...leaves `(CRI, C)` at 0.155/N per mutation event (stationary R-exit hazard 0.150/N to 0.100/N over N = 10²–10⁵, slope −1.07). It is the largest exit from R only at N ≤ 10³."

- **Draft sentence:** "Mass outside E sits mostly on committed-and-compliant states (0.45–0.60) and tolerated light cheaters (0.09–0.30); shadow excursions hold under 0.02."
  - **Evidence:** The preceding sentence covers N = 10²–10⁵, but these ranges omit N = 10², where `runs/inspection-shadow.md` reports committed-and-compliant = 0.4321, light cheater = 0.0094, and shadow excursion = 0.0507.
  - **Correction:** Qualify the ranges with "For N ≥ 10³, mass outside E sits..." (or widen to 0.43–0.60, 0.01–0.30, and under 0.051 across N = 10²–10⁵).

- **Draft sentence:** "Shadow-holding efficient islands stay at 0–0.05: without mutation nothing supplies the shadow or the light cheaters." (and in **Reading**: "...because without mutation neither the shadow nor the light cheaters arrive; the two objects disagree for that reason.")
  - **Evidence:** In the ε = 0 seed lottery (`runs/inspection-shadow.md`), `N` and light cheaters are supplied at founding: at c = 0, `share N` is 0.000–0.095 (up to 0.150 at c = 0.01) and `light-cheater islands` occupy 0.100–0.290 of all islands (0.097–0.352 at c = 0.01). What is absent without mutation is ongoing arrival/drift after the founding scramble.
  - **Correction:** Replace "without mutation nothing supplies the shadow or the light cheaters" with "without ongoing mutation nothing replenishes the shadow after the founding scramble (though founding light-cheater islands still hold 0.10–0.29)", and revise the second Reading bullet accordingly.

- **Draft sentence:** "The一點... blind 0.02..." [in "Inspector-only reading 0.58, blind 0.02;"]
  - **Evidence:** `runs/inspection-shadow.md` runs the blind control across all four c = 0 lottery cells: 0.022 at (100, 64), 0.006 at (400, 16), 0.119 at (800, 8), and 0.017 at (400, 64).
  - **Correction:** Specify the cell ("blind 0.02 at (100, 64), 0.01–0.12 across sizes").

- **Omission:** The spec (`specs/2026-10-24-inspection-shadow.md` §3) required 24 direct-start cells (`(CRI, C)` and `(N, C)` at N = 100, 400 with injected twins and a generation-100 `K` arrival) to directly measure shadow fixation, cheater establishment, and recovery. They were run and tabulated in `runs/inspection-shadow.md`, but the draft omits them entirely.
  - **Correction:** Add a brief clause in the Lottery/Controls paragraph summarizing the direct-start results (e.g., twin fixation matches the injected share n/N, and a single K arrival into `(N, C)` with 1/N responsive inspectors establishes K-majority on ~0.25 of islands with 0.013–0.002 recovery, vs ≥ 0.90 recovery when responsive inspectors hold ≥ 0.90).
