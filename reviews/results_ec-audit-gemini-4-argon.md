# Review of `/private/tmp/claude-501/-Users-jstav-code-program-ecologies/eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/results_ec.md` by gemini-4-argon

1. **Unequal-island exit shares at $\nu = 0.1$ omitted.**
- *Draft:* "unequal islands exit at $5.4 \cdot 10^{-5}$, 43% to a fair pair, 54% to another unequal pair, the rotating dictator"
- *Evidence:* Report §4 (`within` R): at $\nu = 1$, U exit rate is $5.40 \cdot 10^{-5}$ (43.1% to F, 54.0% to U, 2.9% to W+D). At $\nu = 0.1$, U exit rate is $5.4 \cdot 10^{-6}$ and only 34.5% of exits are to F and 44.9% to U (leaving 20.6% to W+D).
- *Correction:* Specify that $5.4 \cdot 10^{-5}$ and the 43% / 54% split are for $\nu = 1$, and report the $\nu = 0.1$ rate ($5.4 \cdot 10^{-6}$) and split (34.5% to F, 44.9% to U).

2. **Stage-1 fair mass conflated with override-independent island share.**
- *Draft:* "On settled fair islands 81% (round 1,000; 95–99% in the long runs) play the fair pair only through overrides (stage-1 fair mass 0.19 to 0.01)."
- *Evidence:* Report §6d: 0.812 (at round 1,000, $\nu = 1$, $I = 1024$) and 0.986–1.000 (at round 10,000, $\nu = 0.1$; 0.820–0.883 at round 3,000, $\nu = 1$) are the *shares of settled fair islands* whose fair play is override-dependent. The report's other column is "mean encounter mass where a contract fires" (0.957 at $\nu = 1$ round 1,000; 0.948–1.000 in the long runs). Neither is "stage-1 fair mass 0.19 to 0.01".
- *Correction:* Drop "(stage-1 fair mass 0.19 to 0.01)" or replace with the reported mean encounter mass where a contract fires (0.95–1.00).

3. **Arm H fair-island exit rate ratio vs R.**
- *Draft:* "H blocks 0.31 / 0.52 / 0.67 of proposals by $|S|$ (hooks at two thirds of leaves), halves the transition rate ($0.43\times$ R)..."
- *Evidence:* Report §4: at $\nu = 1$, within-island `class changes / island-gen` is $0.0000149$ for H vs $0.0000477$ for R ($0.31\times$); at $\nu = 0.1$ it is $0.0000017$ vs $0.0000055$ ($0.31\times$). It is specifically the *fair-island exit rate* that is $0.43\times$ R ($0.0000154 / 0.0000359$ at $\nu = 1$; $0.0000015 / 0.0000037 = 0.41\times$ at $\nu = 0.1$). Also, hooks are 18 of 27 size-1 programs (two thirds of size-1 constants, not all leaves in the grammar).
- *Correction:* Change "halves the transition rate ($0.43\times$ R)" to "cuts the fair-island exit rate to $0.43\times$ R (overall class-change rate $0.31\times$ R)".

4. **Prediction 6 and E9 verdicts.**
- *Draft:* "Held: 3, 4 ($\nu = 1$), 4c, 5c, 6 ($\nu = 1$), 7c, E1–E4, E6, E10, E14. ... Partial: ... E9 ..."
- *Evidence:* Report §7 scores Prediction 6 as **held** across all tested starts at both $\nu = 1$ (round 300) and $\nu = 0.1$ (round 1,000), where every fair pair is $\ge 0.047 > 0.02$. E9's falsifier ("a fair pair below 0.02 at 1,000 events from some start") also did not trigger (and the report omits E8, E9, and 6c from §7). Pair losses only occur at $\nu \le 0.01$ at $10^4$ rounds, or in 2 of 19 checkpoints $\ge 1000$ for $\nu = 0.1$ rep 1.
- *Correction:* Score 6 as held at the 300/1,000-round checkpoints (noting failure at $\nu \le 0.01$ by $10^4$ rounds), and state why E9 is partial (e.g., tilted starts at $\nu = 1$ only run to 300 rounds, or $\nu = 0.1$ tiltF0 still $>2\times$ unequal at round 1,000: 0.186 vs 0.047). Also include E15 in Verdicts.

5. **E8 verdict.**
- *Draft:* Lists E8 under "Partial".
- *Evidence:* Predictions file: E8 predicts $\alpha$'s excess interval includes 0 and upper bound $< 10^{-3}$, with falsifier "an excess with an interval excluding 0 and a point estimate above $10^{-3}$ per migrant." At $\nu = 1$, the interval excludes 0 (falsifying the first clause of the prediction), while at $\nu = 0.1$ E8 holds ($[0.00000, 0.00025]$).
- *Correction:* Explicitly note for E8 (as done for 1) that it fails on the interval at $\nu = 1$ and holds at $\nu = 0.1$.
