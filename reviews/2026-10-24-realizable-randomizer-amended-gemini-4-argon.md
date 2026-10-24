# Review of `specs/2026-10-24-realizable-randomizer.md` by gemini-4-argon

**1. Errors, contradictions, or unsound mechanisms**

* **Certificate binding vs. inspectee reading in the Inspection Game.**
  *Quote:* "the certificate is bound to both quotes, the checker version, the fuel budget and the evaluation context" vs. "certificate carriers: a tape mixer carrying a count certificate for its own probability, so that readers check rather than search" and "comply iff I can prove the inspector inspects me with probability $\ge k/r^M$".
  *Issue:* A tape mixer is opponent-independent (its decision tree depends only on its own root tape, $M=m$). If its carried count certificate is literally bound to *both* quotes, a single carried certificate cannot be checked by arbitrary inspectees with different quotes, and a static template cannot carry certificates for every possible opponent in the grammar. Furthermore, if the checker replays the evaluation of `(x, y)` using `x`'s carried certificate, and `x` is a constant/mixer, `y` is never invoked, so the proof depends only on `x`.
  *Fix:* Specify that for an opponent-independent mixer (or any program whose replay trace never invokes the opponent quote), the count certificate is opponent-generic (bound to `x`'s quote, checker version, budget, and a wildcard for `y`, verified by checking that the replay never reads `y`), matching Milestone 4's opponent-generic certificates.

* **Completeness vs. Soundness of partial count certificates for `≥`.**
  *Quote:* "a new atom `pr(x, y, a) ≥ k / r^M`... the checker replays exactly those assignments (never fresh draws), checks coverage, uniqueness and weights".
  *Issue:* For an inequality `≥ k / r^M`, a sound certificate only needs to list a disjoint set of $a$-producing prefix assignments whose weights sum to *at least* $k / r^M$ (uniqueness/disjointness and lower-bound weight, not full coverage of the assignment space). Requiring full coverage forces the carrier to pay for replaying losing branches too.
  *Fix:* Clarify whether "coverage" means "weights of listed disjoint $a$-branches sum to $\ge k/r^M$" (sufficient for soundness and cheaper) or "full partition of $r^M$". Fix it in the hand table before coding.

**2. Design flaws or confounds**

* **Disabled-template default in fixed-role vs. symmetric games.**
  *Quote:* "a disabled template plays a fixed default and keeps its prior mass, so founder abundances are matched across arms".
  *Issue:* In RPS, dumping the disabled mass of provers/simulators/carriers onto a single constant (say `R`) creates a massive founder bias toward `R`, distorting the early scramble and rewarding `P` constants. In Inspection, dumping disabled inspector templates onto `N` vs `I` directly shifts the baseline compliance payoff.
  *Fix:* Specify the exact default action per disabled class (e.g., in RPS, cycle defaults `R, P, S` across disabled templates or use the renormalized arm as co-primary if founder skew is large; in Inspection, state explicitly whether disabled inspectors default to `N` and disabled inspectees to `K`, and verify in the renormalized control that the default choice doesn't drive the arm comparison).

**3. Predictions**

* **Prediction 3 & 6 (Responsive inspector vs. compliant constants vs. compliant readers).**
  *Quote:* "Efficient islands are at least 0.3... held by the responsive inspector over compliant constants".
  *Issue:* A responsive inspector ("inspect unless I can prove the inspectee complies against me") paired with a *constant* `C` achieves `(N, C) = (0, 0)`, which is invaded by constant `K` (earning 1 against `N` when the proof fails). Wait—against constant `K`, the proof of `C` fails, so the responsive inspector plays `I`, giving `K` a payoff of $-3 < 0$. However, in $L_T$, proving that a constant `C` plays `C` by *search* (`prove` without a certificate) vs. *certificate check* has vastly different step costs. If the responsive inspector uses bounded search, its step cost at $c_0$ may exceed the count-certificate check of a 1-digit mixer (2 replays), flipping Prediction 6 unless the responsive inspector checks a certificate carried by `C` or search on depth-1 constants is trivial. Make sure the §1 hand table explicitly prices depth-1 constant search vs. 2-branch replay.

**4. Missing controls or cheap additions**

* Nothing material. (The fuel-cap sweep, renormalized prior, and sampled-encounter checks from the first review cover the needed controls.)

**5. Alternative explanations**

* Nothing material.
