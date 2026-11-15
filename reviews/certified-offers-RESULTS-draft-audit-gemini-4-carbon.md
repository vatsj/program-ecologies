# Review of `notes/certified-offers-RESULTS-draft.md` by gemini-4-carbon

1. **RE 4 verdict classification.**
   - *Draft:* "Falsified: RE 4 (third clause), RE 5 (no gain), RE 6, E4, E6. Failed without the falsifier firing: RE 10, E5, E11."
   - *Evidence:* In `predictions/2026-11-15-certified-offers.md`, RE 4's stated falsifier is: "carriers exclude Bc (ρ·N < 0.1 in a pair slot)." In `runs/certified-offers.json`, RE 4 has `"falsifier_fired": false` (ρ·N in pair slots was `[1, 1]`, while clause `c` failed: `27.86` vs `1.0`).
   - *Correction:* Move `RE 4 (third clause)` from "Falsified" to "Failed without the falsifier firing".

2. **RE 10 verdict classification.**
   - *Draft:* "Failed without the falsifier firing: RE 10, E5, E11."
   - *Evidence:* `predictions/2026-11-15-certified-offers.md` specifies RE 10's scoring rule: "The mixed arm's V\* lies between its two pure arms' (within 0.05 outside)... scored on the mean over cells of the signed distance outside the interval". In `runs/certified-offers.json`, `"mean signed distance outside 0.010"`, which satisfies the ≤ 0.05 rule (the script scored per-cell instead of the registered mean).
   - *Correction:* Move `RE 10` to "Held" (or explicitly note that the mean signed distance outside was 0.010, meeting the registered scoring rule, while 3 of 20 individual cells exceeded 0.05).

3. **C0 step count.**
   - *Draft:* "C0 (the check written out in L_T^code, 167 steps)"
   - *Evidence:* `runs/certified-offers.md` and `predictions/2026-11-15-certified-offers.md` state "167–168 steps per accepted quote" / "167–168 steps on carriers".
   - *Correction:* Change "167 steps" to "167–168 steps".

4. **Ablation difference at δ < 0.01.**
   - *Draft:* "(ablated to ⅓ constants: equal at δ ≥ 0.01, −0.10 below)"
   - *Evidence:* In `runs/certified-offers.md` (Step 2 table): at δ = 0.003, Fc+Oc+Rc is `0.81` vs Fc+Oc+C⅓ `0.70` (`−0.105` in `certified-offers.json`); at δ = 0.001, `0.65` vs `0.55` (`−0.099`). Rounding `0.105` gives `0.11` (and E11 failed its `≤ 0.1` check specifically because `0.105 > 0.1`).
   - *Correction:* Change "−0.10 below" to "−0.10 to −0.11 below" (or "−0.105 and −0.099 below").

5. **Mass under `lib CARRY`.**
   - *Draft:* "written out with `lib CARRY` 18 nodes and 10⁻²⁰ of a reader"
   - *Evidence:* `runs/certified-offers.md` Step 1 table: fair single reader mass under R1 written is `1.6e-11`; Oc is `1.6e-30` (ratio `1.0 × 10⁻¹⁹`) and Rc is `1.8e-30` (ratio `1.1 × 10⁻¹⁹`). The run report text states "every carrier is 10⁻²⁰–10⁻²⁹ of the reader" (spanning Oc/Rc at `~10⁻¹⁹` down to Fc/Bc at `~10⁻²⁹`).
   - *Correction:* Change "10⁻²⁰ of a reader" to "10⁻¹⁹ of a reader" (since the subject of the clause is Oc and Rc at 18 nodes).

6. **Scramble scope (Finding 3).**
   - *Draft:* "and 0.991 of islands keep their 30N class to 120N."
   - *Evidence:* `runs/certified-offers.md` and `runs/certified-offers.json` (RE 8): `0.991` is specifically for the "Main arm, β = 3, φ = ½, all δ and N", not across all arms/parameters.
   - *Correction:* Specify the scope: "and 0.991 of islands (main arm, β = 3, φ = ½) keep their 30N class to 120N."
