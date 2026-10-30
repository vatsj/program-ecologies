# Review of `/private/tmp/claude-501/-Users-jstav-code-program-ecologies/eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/results_mit.md` by gemini-4-argon

* **Draft:** "Crossing founding and migration charges shows the migration charge alone sets this; the founding charge moves V\* by 0.006."
  **Evidence:** In `runs/many-islands-t.md` §8 (crossed table), holding migration charge fixed and varying founding charge from 0 to 0.1 moves V\*(end) by 0.0000 and V\*(10⁵) by 0.0001; at 10³ events it moves V\* by 0.0065 (`0|0.0` 0.8886 vs `0.1|0.0` 0.8821) and 0.0059 (`0|0.1` 0.8797 vs `0.1|0.1` 0.8738) from the natural start, or 0.0058 at founding (`0.5282` vs `0.5224`).
  **Correction:** Specify the time horizon: "...the founding charge moves V\* by 0.006 at founding and at 10³ events (and 0 at the limit)."

* **Draft:** "Long runs (to 10⁶–10⁷) give the same incidence."
  **Evidence:** Comparing `runs/many-islands-t.md` §7 (to 10⁵) and §7b (to 10⁶–10⁷), unequal consensus counts (`>= 0.99 unequal`) change in several cells: `main|0.1|0` at I = 256 (2 vs 1) and I = 1,024 (2 vs 0); `main|0|0` at I = 64 (4 vs 2); `0|0|0` at I = 64 (8 vs 11) and I = 256 (9 vs 8).
  **Correction:** Change "the same incidence" to "similar incidence (e.g. 0/20 at I = 1,024 with readers, 8–11/20 at dose 0)".

* **Draft:** "- What readers add over constants is visible only at finite I: constants-only worlds of up to 4,096 islands fall into an unequal consensus in about 40% of runs, worlds with readers in none from 1,024 islands."
  **Evidence:** In `runs/many-islands-t.md` §7 (to 10⁵ events), `main|0.1|0` at I = 1,024 has 2/20 worlds ending `>= 0.99 unequal` (and 1/20 from the unequal tilt at both `main|0.1|0` and `main|0|0`). Also, in the ODE (infinite I), readers accelerate conversion at finite time (at 10³ events, V\* is 0.503 at dose 0 vs 0.874–0.958 with readers).
  **Correction:** Change "visible only at finite I" to "visible in finite time and at finite I", and change "in none from 1,024 islands" to "in 0–2 of 20 at 1,024 islands and 0 of 20 at 4,096".
