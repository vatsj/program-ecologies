# Predictions: a per-root production rule for the fully realizable social organization game (2026-10-16)

Spec `specs/2026-10-16-per-root-production.md` (reviewed by gpt-6.1-sol and gemini-4-argon; the "Amendments after
review" supersede the earlier text where they conflict). Committed after `notes/per-root.md` §1 (commit ac7684b) and
before any code of this run and any counted cell. Numbers are hand calculations from the notes, the scratch static
computation disclosed in notes §1, readings of stored runs, or guesses (labelled). Lottery results are ε = 0 evidence at
finite (N, I, horizon); fairness is scored, productive efficiency is reported beside it and selects nothing; outcomes
are all-or-nothing by run, so contrasts rest on a few runs.

**Scoring conventions.** "Fair share" is the fraction of islands fair at generation 10,000 (the terminal share,
primary; time averages beside it). "Development" = founder streams 0–19 (paired with the stored `Ni` and `cell_Hfull`
0–19: S₃ 0.000, H-full 0.300); "confirmation" = streams 20–59 (stored H-full 0.299). Both stream sets are reported;
where a cell runs on both, **the confirmation set decides** (amendment 7). Rules as frozen in notes §1.0: R0 = S₃; R1 =
per-root lack (validity = root validation `vone4`, Hyp nodes as hypotheses); R2 = R1 + PROD3A's alternative (the
first succeeding Hyp choice point's F branch, written before its primary); R0 + alternatives (the factorial); R3 = R2
with k bundles per set, LRU read as CLOCK (notes §1.0 item 6), FIFO as one control. Executed cells run on the
development streams. **Outcome regions:** supported / contradicted (falsifier fired) / inconclusive, as notes §1.3; a
paired contrast whose bootstrap interval spans both the predicted effect and zero is inconclusive; observed-threshold
verdicts are kept apart from statistical evidence.

## RE predictions (verbatim from the spec; revised ones marked)

1. **R2 recovers the free-certificate fair wage on the ideal table:** within 0.1 of H-full on the paired streams (H-full
   0.30 / 0.30), and zero wage ≤ 0.05. *Falsifier:* R2 ≤ 0.1 on both stream sets.
   *Regions:* supported iff |R2 − H-full| ≤ 0.1 and R2 zero wage ≤ 0.05 on the confirmation streams; contradicted iff
   R2 ≤ 0.1 on both stream sets; inconclusive otherwise (e.g. within 0.1 on one set only, or zero wage above 0.05).
2. **R1 alone is partial:** between S₃ and R2, near the producible-half grant (0.10). *Falsifier:* R1 ≥ R2.
   *Regions:* supported iff R0 ≤ R1 < R2 and R1 ≤ 0.2 on the confirmation streams; contradicted iff R1 ≥ R2 there;
   inconclusive otherwise.
3. **The cap is cheap** [revised after review: R2 writes two scripts per attempt, so the cap counts attempts]: R3 with
   k = 2 bundled attempts and LRU eviction within 0.05 of R2, cost ≤ 1.5× play. *Falsifier:* below R2 by ≥ 0.15.
   *Regions (scored on the R3 k = 2 CLOCK-LRU cell, development streams, and on the confirmation streams if it is the
   best R3):* supported iff |R3 − R2| ≤ 0.05 and its median encounter cost ≤ 1.5× play (at 3·10⁶ if it runs there,
   else on the ideal table's charged steps); contradicted iff R3 ≤ R2 − 0.15; inconclusive otherwise.
4. **Fuel still binds when executed:** R2 at 10⁶ ≤ 0.1 (as free certificates gave 0.03) and at 3·10⁶ ≥ 0.4.
   *Falsifier:* R2 at 3·10⁶ ≤ 0.15. *Regions:* supported iff both clauses hold; contradicted iff R2 at 3·10⁶ ≤ 0.15;
   inconclusive otherwise (if K = 10⁶ is dropped, the first clause is unscored).
5. **No overhead returns:** under the invariant mark, the median encounter cost under R2 ≤ 1.5× play [revised after
   review: the upper quantiles and cumulative charged work are reported too, and judged separately]. *Falsifier:*
   median ≥ 2×. *Regions (R2 at 3·10⁶, the kernel's stride sample of executed encounters; the ideal table's charged
   steps beside it):* supported iff median ≤ 1.5×; contradicted iff median ≥ 2×; inconclusive between. The upper
   quantiles (90th, 99th) and the cumulative ratio are judged separately and reported as such.
6. **Counter-predictions registered.**
   - *Sol:* (a) low median overhead can coexist with expensive regrowth encounters and fuel failures; (b) k = 2 works
     only if a small validity cover exists; (c) R2 improves on R0 but may stay well below matched H-full at 3·10⁶.
   - *Gemini:* (d) unbundled FIFO k = 2 drops ≥ 0.10 below R2; (e) R2 at 3·10⁶ gives 0.25–0.35 under linear checking,
     ≥ 0.4 only with root-keyed dispatch; (f) R2 may lag H-full by arrival timing (second scripts acquired after fair
     bosses die).
   *Scored:* (a) holds iff the median under R2 at 3·10⁶ is ≤ 1.5× while the 99th percentile is ≥ 3× or fuel or cap
   timeouts occur at ≥ 1% of regrowth-phase encounters; (b) holds iff k = 2 is within 0.05 of R2 exactly when the
   validity cover is ≤ 2 for ≥ 0.9 of the prior mass (or both fail); (c) holds iff R2 > R0 at 3·10⁶ and R2 ≤ H-full −
   0.15 at 3·10⁶; (d) is scored on the bundled FIFO k = 2 cell (the only FIFO cell, amendment 4; noted in the verdict):
   holds iff FIFO ≤ R2 − 0.10; (e) holds iff 0.25 ≤ R2 (linear) ≤ 0.35 at 3·10⁶ and R2 (dispatch) ≥ 0.4 (unscored if
   dispatch is dropped); (f) holds iff R2 < H-full on the confirmation streams and, in the R2 runs that do not regrow,
   the nucleus classes of the H-full partner first appear after the fair bosses' extinction check.

## Subagent predictions (mine), with falsifiers and regions

**S1. R0 reproduces S₃.** The new kernel's R0 reproduces the stored `Ni` on replicates 0–4 in every dynamic summary
field (fair masks, plays, holders, exits, the 10,000 extension); only the mark's counters differ. *Falsifier:* any
dynamic difference. (Supported / contradicted only.)

**S2. Static reach.** From code: R2 can hold all of (b) ∩ S₃^static and ≥ 0.9 of (b) \ S₃^static (prior mass); the
validity cover is ≤ 2 for ≥ 0.9 of the worker prior mass and of the boss prior mass. *Falsifier:* the cover is ≤ 2 for
< 0.8 of either role's mass, or R2 reaches < 0.8 of the shadowed part. *Inconclusive:* 0.8–0.9.

**S3. R1 is near S₃.** R1 ≤ 0.10 on the confirmation streams (development: ≤ 0.15). *Falsifier:* R1 ≥ 0.2 on the
confirmation streams. *Inconclusive:* 0.10–0.2.

**S4. R2 rescues partially.** 0.10 ≤ R2 ≤ 0.30 on the confirmation streams, and R2 − R0 > 0 with a paired interval
excluding 0. *Falsifier:* R2 < 0.05 or R2 > 0.40 on the confirmation streams. *Inconclusive:* otherwise (e.g. in range
with an interval spanning 0).

**S5. The two changes are complements.** R0 + alternatives ≤ 0.05 on both stream sets, and the interaction
(R2 − R1) − (R0+alt − R0) > 0. *Falsifier:* R0 + alternatives ≥ 0.15 on the confirmation streams.

**S6. R2 removes most zero-wage islands.** Zero-wage share under R2 ≤ 0.2 on the confirmation streams (R0 about 0.5).
*Falsifier:* ≥ 0.4.

**S7. Validation is the overhead.** At 3·10⁶ the median encounter cost under R2 is 1.3–2.5× play, its cumulative
charged work at least 1.5× R0's, and validation accounts for more than half of R2's charged non-play steps after
generation 50. *Falsifier:* median < 1.1× or > 3×, or validation < 0.25 of non-play steps after generation 50.

**S8. Executed fuel.** R2 at 10⁶ ≤ 0.05; at 3·10⁶, R0 ≤ R2 ≤ H-full (all at 3·10⁶). *Falsifier:* R2 at 10⁶ ≥ 0.2, or R2
at 3·10⁶ > H-full at 3·10⁶ + 0.1.

**S9. Nuclei use second paths.** In R2's regrowing runs, ≥ half of the first fair encounters have at least one pivotal
per-root or alternative script, and per-root scripts are pivotal in more nuclei than alternatives. *Falsifier:* no
R2 nucleus has a pivotal per-root or alternative script (if R2 has ≥ 3 regrowing runs). *Inconclusive:* < 3 regrowing
runs.

**S10. The cap binds little.** R3 k = 2 (CLOCK-LRU) within 0.05 of R2 and FIFO k = 2 within 0.10 on the development
streams; R3 k = 3 within 0.05 of R2. *Falsifier:* k = 2 CLOCK-LRU ≤ R2 − 0.15.

**S11. Second scripts arrive early; fair bosses die early.** In every R1 and R2 run some per-root script is held by
generation 10, and in every R2 run some alternative by generation 10; in ≥ half the runs of every rule, no island has a
½-paying boss against its modal workers at some check in generations 10–200. *Falsifier:* per-root scripts first held
after generation 50 in most R1/R2 runs.

**S12. Realizable as code.** PROD3A as code returns the symbolic primary and alternative on every sampled encounter; the
cost model's error on its steps has median ≤ 2% (after any fitted correction, which is reported); whole encounters with
R2 lists match the evaluator's plays and steps on ≥ 99% of samples; 0 soundness violations across appends and
evictions. *Falsifier:* a primary or alternative mismatch, a soundness violation, or < 95% encounter matches.

**S13. Dispatch is a cost change only.** R2 with root-keyed dispatch at 3·10⁶ is within 0.1 of R2 linear at 3·10⁶.
*Falsifier:* ≥ 0.2 apart.

**S14. The mark is a cost fix.** At the ideal table mark-sensitive productions are 0 (Lemma M); at 3·10⁶ they are
< 1% of examined productions in every cell. *Falsifier:* any at the ideal table, or ≥ 5% at 3·10⁶.
