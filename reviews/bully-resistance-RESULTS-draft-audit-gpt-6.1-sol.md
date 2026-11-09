# Review of `notes/bully-resistance-RESULTS-draft.md` by gpt-6.1-sol

- **“Both the unequal and the fair state are absorbing against single-slot invasion”** (title, mechanism, conclusion). Evidence: UB assays exceed 3/N in 3% of firm-reader cases (maximum ρN = 9.75), 2% for P_z and 3% for O; unpaired-slot medians are neutral, not extinction. Seeded-fair exits at beta 3 are 5–25%. Correction: report strong, configuration-dependent invasion resistance and finite-schedule persistence, not absorption or universal stability.

- **“Not one island becomes fair … both states absorb … loss … decided before 30N.”** Evidence: entry hazard measures fairness **at 120N**, not whether an island ever became fair. Holding runs include 122/31 U→F and 27/15 F→U transitions between 30N and 120N. The omitted transition table also records substantial bidirectional changes during the tail. Correction: say no seeded-unequal islands were fair at the endpoint; most final unequal outcomes were already unequal at 30N, not irrevocably fixed then.

- **“V* falls with delta, 0.75–0.85 … N = 100 … 0.00–0.20 above 0.01.”** Evidence: at delta 0.0003, N=100, O reaches only 0.50 and FPO 0.55 at beta 3; PO is 0.70 at beta 1. Responses are not uniformly monotone. Correction: use 0.50–0.85; include nonmonotonicity and qualify the overall trend.

- **“P+O 0.00 / 0.00 / 0.40, F+P+O 0.00 / 0.05 / 0.55.”** Evidence: at beta 3, N=200, delta=0.01, PO is 0.00 and FPO 0.05, as quoted; however the preceding FO sequence incorrectly gives **0.00 / 0.05 / 0.36** only if interpreted correctly. No correction is needed to these sequences; the material numerical error is instead **E10’s location**: its two 0.20 gaps occur in **tail-only cells at delta=0.003**, not 0.03.

- **“All within the run noise of F (intervals overlap)” / “failure is not a charge or timeout artefact.”** Evidence: overlapping marginal intervals do not establish equivalence; diagnostics cover only selected cells, and the idealized table freezes unresolved profiles. Correction: no clear improvement was demonstrated in these diagnostics; do not exclude charge/timeout contributions generally.

- **“The length prior makes P … exponentially rarer … therefore needs … two slots at once.”** Evidence: masses are exact-member lower bounds, their ratios are not bounds on total behavioral-class ratios, and dynamics use grammar-conditioned projections. Correction: restrict rarity claims to counted spellings; present the proposed requirement as a model-dependent hypothesis.

- **“Monte Carlo 6 × 10^6 draws”; “about 130 … hours.”** Evidence: R0 uses 12 million draws; notes total approximately 135 CPU-hours. Correction: distinguish R0 from R1/R2 and use 135.

- **Omitted design restriction:** all arms retain exploiter mass 0.01δ/0.09. Disclose this and the literal-only probe/no-punishment restrictions when interpreting “smarter third party” impossibility.
