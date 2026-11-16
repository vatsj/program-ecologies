# Review of `reviews/script-checked-offers-RESULTS-draft.md` by gemini-4-carbon

1. **Finding 1: uncertified control V\* bound**
- *Draft:* "The uncertified controls at the same fuel have none (V\* ≤ 0.2 at every δ, except 0.42–0.50 at the smallest δ = 0.001), so fuel alone does nothing."
- *Evidence:* In `runs/script-checked-offers.md` (Step 2 table): at β = 1, `U: F+R` has V\* = `0.30` at δ = `0.003` (`0.15 / 0.05 / 0.10 / 0.30 / 0.50`); at β = 0, `U: F` and `U: F+R` reach `0.50–1.00` with δ\* = `0.03`. Even at β = 3 alone, `U: F+R` at δ = `0.001` is `0.45` (`U: F` is `0.15`), whereas `0.42–0.50` comes from β = 1 (`0.42`, `0.50`) and β = 3 (`0.45`).
- *Correction:* Restrict the claim to β ≥ 1 and include the `0.30` cell (or restrict to β = 3 where V\* ≤ `0.15` except `0.45` in `U: F+R` at δ = `0.001`). E.g., "At β = 3 the uncertified controls at the same fuel have none (V\* ≤ 0.15 at every δ, except 0.45 in F+R at δ = 0.001; also no δ\* at β = 1)."

2. **Predictions / Scope: RE 1 evaluator replacement omitted**
- *Draft:* "`RE 1 before any code` ... `Held: RE 1, ...`" (Scope lists deviations `(v)` and `(vi)`, omitting RE 1's evaluator swap).
- *Evidence:* `predictions/2026-11-16-script-checked-offers.md` and `runs/script-checked-offers.json` disclose that the first direct-style checker cost up to `166,456` ticks—outside RE 1's registered `[10³, 10⁵]` cost requirement—and was replaced by a continuation-passing evaluator (`κ_S = 15,141`) before the gates, on which RE 1 was scored.
- *Correction:* Disclose in **Gates**, **Scope**, or **Predictions** that the initial direct-style checker exceeded RE 1's `10⁵`-step bound (`166,456` steps) and was replaced by the continuation-passing version before the gates were run.

3. **Predictions: mischaracterization of RE 8's prediction**
- *Draft:* "Falsified: RE 8 on both clauses (the RE expected prudence to exclude the bully at no gain in V\*; the bully's share rose and V\* was higher at δ = 0.003)"
- *Evidence:* `predictions/2026-11-16-script-checked-offers.md` states RE 8 clause 2 as: "V\* at δ = 0.003 is lower than A2's by 0.1 or more. Falsifiers: ... A4's V\* at δ = 0.003 at or above A2's." Thus RE 8 predicted a *loss* in V\* of at least `0.1`, whereas "at no gain in V\*" describes the falsifier threshold rather than the prediction.
- *Correction:* Change "at no gain in V\*" to "and lower V\* at δ = 0.003 by at least 0.1".
