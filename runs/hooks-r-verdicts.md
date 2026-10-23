# Hooks, Part R: verdicts (2026-10-23)

Scored against `predictions/2026-10-18-hooks-r.md` (committed before any counted cell) with the numbers of
`runs/hooks-r.md` / `.json` (regenerated 2026-10-23 from complete rows) and the identity audit
(`runs/hooks_r/idaudit_*.json`). Every number is an ε = 0 lottery statistic at finite (N, I, horizon): (200, 64), world K,
S-nonself production, w = 0.3, 20 replicates (10 for the secondary tier), paired founders. UO = universal-open runs,
UOT = universal on the PrudentBot target. "n/20" counts runs; Δ is the difference of fractions; p is exact McNemar.

## Read this first: three scoring conventions forced by the run

1. **Horizons.** The predictions say "10,000" (main cells) and "2,000" (ablations). The cost plan of notes §2.5 item 8
   declared main cells B, I, M at **2,000** and every ablation at **1,000**, scored against M's generation-1,000
   snapshot. Verdicts below use those horizons and say which one. Nothing was run at 10,000.
2. **M is slow, not different, at the first horizon.** In M the scramble is not over at 1,000 (UO 2/20, unheld islands
   0.040, mean island P(C,C) 0.953; median generation at which P(C,C) first reaches 0.99: 1,250, against 250 in B and I);
   by 2,000 it is over (UO 11/20, unheld 0.000, P(C,C) 0.997). Every ablation comparison made at 1,000 against M@1,000
   therefore mixes a final-state effect with a speed effect. I report each against M@1,000 (the registered pairing),
   against I@1,000 and against M@2,000 (not a matched horizon; descriptive).
3. **Identity is counted after the audit.** The mass classifier's "identity" label over-counts (it labels monomorphic
   rival islands, notes §2.7). Audit (`hooks_r_run.py idaudit`, 30 reruns of counted runs, 29 reproduced their stored
   class string, the exception being M-source rep 16, notes §2.8; strict identity = the island's majority type is mutual
   with none of 300 reference self-cooperating units, no panel unit and no living type of another spelling): **1 of 250
   raw-labelled identity or rival islands in B, I, M (its three rival-bearing runs of six) and the S-nonself ablations
   was strict identity (M-history rep 17); the other 249 are mutual with 9 to 267 of the 300 reference units.** The clone
   diagnostic is the exception in the other direction: 95 of 192 islands in three audited runs are strict identity
   (0.49 per island), including 34 islands the classifier had labelled rival. Raw labels and strict counts are both in
   the report.

## Scorecard

| id | prediction (short) | verdict | the number |
|---|---|---|---|
| RE 2 | history fills protect gentle programs | **failed** (sign) | removing the history scope raises the PrudentBot share 0.62 → 0.77 and UO 2 → 10 of 20 |
| RE 3 | source-keyed fills bring identity back; UO falls ≥ 0.2; source off restores | **failed** on the mechanism, UO clause held | identity 0; UO(M) − UO(B) = −0.40; source off does not restore (3/20) |
| RE 4 | threat fills fit while untested (SOG) | **not scored** | SOG wing not run |
| RE 5 | fission–fusion ≥ 0.9 | **not scored** | dropped (notes §2.5 item 9) |
| RE 6 | source-scope ablation (idroutes) removes identity, restores UO to within 0.1 of I | **partial** | identity 0; UO 15/20 vs I 11/20 (+0.20) |
| RE 7 (sol) | wing differences; history benefit conditional; efficiency uncertain | **held, weakly** | history effect negative and non-uniform; efficiency lost in six cells |
| RE 8 (argon) | no seeded identity; any identity from contracts or thanks among clones | **held**, second clause only half resolved | M identity 0; clone cell 0.49 per island; thanks versus contracts not separated |
| R1 | gate | **held** | 598/598, 223 certificates 0 false atoms, 1,800/1,800 |
| R2 | seeded keys nearly inert | **held** | 0.05 SELF fills per run; 1.7% of keyed fills name a resident spelling |
| R3 | grammar dilution within ±0.2; no identity in I | **failed** (UO clause) | UO(I) − UO(B) = −0.35 at 2,000 (p = 0.016) |
| R4 | no seeded identity (≤ 0.005 per island) | **held** | strict identity 0 in B, I, M; 1 island in 1,280 in M-history |
| R5 | UO(M) − UO(I) ≤ −0.1 | **inconclusive at the registered horizon**; held at 1,000 | −0.05 at 2,000; −0.45 at 1,000 (p = 0.012) |
| R6 | loss located in root and behaviour | **failed** (location) | M-root +0.10, M-behaviour +0.15 vs M@1,000; the loss is in history writes |
| R7 | history decides little | **failed** | writes inert vs M@1,000: +0.60 (p = 0.004) |
| R8 | thanks the most held kind | **held** | history 0.83 of held fills at 2,000 |
| R9 | islands stay efficient (≥ 0.98; falsifier < 0.95) | **failed** (falsifier fired in five cells) | 0.770, 0.856, 0.930, 0.935, 0.946; B, I, M at 2,000 ≥ 0.995 |
| R10 | fission–fusion ≥ 18/20 | **not scored** | dropped |
| R11 | clone route mints identity | **held** | 0.49 per island (strict), raw 0.48 over 20 runs |
| R12 | other sources add commitments, not losses | **failed** | UO(M) − UO(seedonly) = −0.65 at 1,000 (−0.20 against M@2,000) |
| R13 | conflict rule matters little | **not scored** | dropped |
| R14 | size check | **not scored** | dropped (infeasible) |
| R15 | verification cost ≤ 2× the inert control's | **held under the registered model** | 1.05× to 1.2× (lists priced alike); 75× an empty list |

## The numbers behind each verdict

**Main cells (20 runs each).**

| cell | g | UO | UOT | rival / island | unheld / island | island P(C,C) | target share |
|---|---|---|---|---|---|---|---|
| B (no hooks) | 1,000 / 2,000 | 17 / 19 | 14 / 16 | 0.007 / 0.006 | 0 / 0 | 0.998 / 0.999 | 0.93 / 0.95 |
| I (inert hooks) | 1,000 / 2,000 | 11 / 12 | 8 / 9 | 0.028 / 0.026 | 0 / 0 | 0.996 / 0.995 | 0.92 / 0.90 |
| M (maximal) | 1,000 / 2,000 | 2 / 11 | 0 / 3 | 0.087 / 0.008 | 0.040 / 0 | 0.953 / 0.997 | 0.62 / 0.72 |

Paired (exact McNemar): I − B −0.30 (p = 0.070) at 1,000 and −0.35 (p = 0.016) at 2,000; M − I −0.45 (p = 0.012) at 1,000
and −0.05 (p = 1) at 2,000; M − B −0.75 (p < 10⁻⁴) and −0.40 (p = 0.022); M@2,000 − M@1,000 +0.45 (p = 0.004).
Universality on the target is where M pays at 2,000: UOT 3/20 against I 9 and B 16.

**RE 2 (history protects gentle programs): failed in sign.** Removing the history scope (M-history) raises UO from 2 to
10 of 20 against M@1,000 (+0.40, p = 0.022; against I@1,000 −0.05), raises the PrudentBot share from 0.62 to 0.77, and
the open share from 0.88 to 0.89; removing the writes (nowrite) raises UO to 14/20 (+0.60) and the target share to 0.80;
seeding only gives 15/20 and 0.94. The history fills are the ones that slow and thin the target. Reciprocity versus
inherited labels: shuffled keys (10 runs) UO 2/10, mean P(C,C) 0.856, unheld 0.147; learned-not-inherited UO 3/10, P(C,C)
0.991; grudge-only UO 2/10, P(C,C) 0.770, unheld 0.253. With 10 runs none of the three controls separates from M on UO
(|Δ| ≤ 0.2, p ≥ 0.5), but shuffled and grudge-only fills visibly damage efficiency inside the window, and inheritance
matters for speed (not-inherited keeps P(C,C) at 0.991). The "higher repeat-encounter rates" clause was not measured
(no per-island repeat-encounter statistic was recorded): untested.

**RE 3: failed on the mechanism.** Identity islands in M: 0 (raw 0, strict 0); its 6 audited rival-bearing islands (3 of its 6 runs
with rivals) are all non-identity. UO(M) − UO(B) = −0.40 at 2,000 (≥ 0.2: the deficit clause holds, and the falsifier "UO within 0.1 of
baseline" does not fire), but the deficit is not identity, and ablating the source scope does not restore it:
M-source UO 3/20 against B@1,000 17/20 (−0.70) and M@1,000 2/20 (+0.05).

**RE 6 (idroutes): partial.** Source, history and contracts inert: raw identity labels 0.0023 per island (3 labels in 2
runs, all audited, 0 strict, so the ≤ 0.005 clause holds), UO 15/20 against I@1,000 11/20 (+0.20, p = 0.34) and B@1,000
17/20 (−0.10). The "within 0.1 of the inert control" clause is missed on the high side. The ablation is not informative
about identity, since M had none to remove; it is informative about speed: idroutes is as fast as seeding only
(median generation to P(C,C) ≥ 0.99: 250 in both).

**RE 7 (sol).** Wing differences: not scored here (Part W is separate). History benefit conditional and not a uniform
+0.1: in Part R the history scope's net effect on UO within the window is large and negative (above), conditional on
writes being on, not on inheritance (not-inherited +0.20, p = 0.5 vs M@1,000). Held-share rankings sensitive to prior and
list retention: the renormalised-prior cell (source scope off at seeding) has UO 3/10, P(C,C) 0.935; the seeded
non-history scopes are gone by generation 200 in every cell, so the ranking is a statement about what the writes and
copies produce, not about the prior. Efficiency preservation uncertain: borne out (R9).

**RE 8 (argon): held.** Seeded source fills do not restore identity (M raw 0 and its 6 audited rival islands 0 strict; seeding-only,
whose only fills are seeded, 0 strict among 13 audited labelled islands), and the only identity anywhere is in the clone cell, where thanks and contracts may key to one's own
spelling: 0.49 strict identity per island, UO 0/20. Seeded SELF fills are 0.05 per run. Whether thanks fills or
contracts mint the cliques is not separated (the clone cell enables both; no cell turns one off with S-self fills on).

**R1: held.** `runs/hooks-r-gate.json`: 60/60 conservative checks; 598/598 gene-site checks agree between the term's CHKH,
the host replay and the host-side conflict rule; 223 accepted certificates, 0 false atoms; Lemma H audit 1,800/1,800 pairs
and 900/900 behaviour classes. Disclosure unchanged: executed plays (fuel K) differ from ideal ones in 2 of 360 sampled
pairs (nested gene-site checks can exhaust the cap), a cost matter, not a Lemma H failure.

**R2: held.** 20 replicates of founders: 0.05 seeded SELF fills per run (bound 0.3); 60.4 of 3,629 keyed seeded fills per
run (1.7%) name a spelling present on the holder's island (bound 5%).

**R3: failed.** UO(I) − UO(B) = −0.30 at 1,000 and −0.35 at 2,000 (falsifier |Δ| ≥ 0.3); identity in I: 27 raw labels in 8
audited runs (rep 1, 2, 13, 14, 15 at one or both horizons), 0 strict (the "identity" islands are monomorphic rivals,
mutual with 32 to 253 of 300 reference units), so the identity clause holds. The grammar-dilution effect (the same
founders with hooks that never act) is larger than predicted and is carried by rivals (0.026 against 0.006 per island) and
by the target (UOT 9 against 16).

**R4: held.** Strict identity per island: B 0, I 0, M 0 (raw 0; 6 of its 10 rival islands audited, 0 strict), seedonly 0, idroutes
0, M-source 0, M-root 0, M-behaviour 0, nocopy 0, nocontract 0 (raw 48 islands in one run, 0 strict), grudge-only 0, and
M-history 1 island in 1,280 (rep 17, one island, 0.0008). The bound is 0.005. The one genuine island is reported, not
dismissed.

**R5.** At the registered horizon (2,000): −0.05, in (−0.1, 0): inconclusive by the registered rule, and 6 of M's 9 non-UO
runs fail through rival islands (10 rival islands, 0 identity), 3 through a cross-island split between individually open
islands (cross-island mutual-cooperation mass 0.05, 0.32, 0.47). At 1,000: −0.45 (p = 0.012), held. So hooks cost
universality in the window and not at 2,000; they cost the PrudentBot target at 2,000 (UOT 3 against 9).

**R6: failed (location).** Against M@1,000 (UO 2) the gap to I is 9 runs; half is 4.5. M-root 4/20 (+0.10, a 22% recovery)
and M-behaviour 5/20 (+0.15, 33%): neither reaches half, and both exceed M's UO, so the falsifier "neither exceeds M"
does not fire. Source inert: M-source 3/20 (+0.05), within the ≤ 0.1 clause. What recovers the gap is the history scope and
the writes: M-history +0.40 (89% of the gap), nowrite and seedonly +0.60 / +0.65 (more than the gap, since they also beat
I), contracts inert +0.50 (n = 10, 6/10), copying inert 0. Role-inert and none-inert do nothing (+0.00, +0.10). Behaviour
fills do not even survive: their held share is 0.00 by generation 200 in M.

**R7: failed.** Writes inert (nowrite) − M@1,000: +0.60 (p = 0.004; against M@2,000 +0.15, p = 0.55). The falsifier (|Δ| ≥
0.3) fires against the registered pairing. Shuffled: +0.10 and not-inherited +0.20 (10 runs, p ≥ 0.5): within the 0.15
and under the 0.3 respectively, so only the writes control falsifies. The window caveat applies: nowrite also has the
highest unheld share of any 20-run cell at 1,000 (0.102) and one lost run (mean P(C,C) 0.910 with it, 0.958 without), so its UO 14/20 is
over runs some of which are still unsettled.

**R8: held.** Held fills by scope in M (individual-weighted): history 0.77 / 0.88 / 0.83 and source 0.22 / 0.12 / 0.17 at 200 /
1,000 / 2,000; none, role, behaviour, root < 0.01. By source: writes 0.25 to 0.41, copies 0.50 to 0.74, contracts 0.00 to 0.09.
The executed share is history 0.48 / 0.70 / 0.75 and source 0.50 / 0.27 / 0.22.

**R9: failed, in the window; not at the end state.** Mean island P(C,C) (runs lost to a scramble failure excluded):
grudge-only 0.770, shuffle 0.856, clone 0.930, renorm 0.935, M-history 0.946, M-none 0.950, nowrite 0.958; all others ≥ 0.98.
Five cells are below 0.95 (the falsifier). For the first four unheld islands are 0.05 to 0.25 per island (the scramble
is not over at 1,000), so this is the speed effect again. The clone cell is different: unheld 0.001, held-island P(C,C)
0.931, constant from generation 200 (0.916, 0.927, 0.930): the 7% is permanent inefficiency inside held islands, the
price of identity cliques sharing an island. B, I and M at 2,000: 0.999 / 0.995 / 0.997.

**R11: held.** Clone fills (S-self writes and contracts, production S-nonself): raw identity labels 0.482 per island in
20 runs (0 of 20 runs UO, 20 of 20 with identity); audit of the 3 cheapest runs: 95 strict identity islands of 192 (0.49),
61 of the 99 raw identity labels and 34 of the 86 rival labels (so the classifier also under-counts here).

**R12: failed.** UO(M) − UO(seeding only): −0.65 at 1,000 (2/20 against 15/20, p = 0.0002); against M@2,000 −0.20 at
mismatched horizons. Seeding-only is at the baseline's level and speed (UO 15/20; B 17/20; median generation to 0.99
250 in both). The registered claim (other sources add commitments, not losses) is wrong in the window.

**R15: held under the registered model, with a caveat that matters.** Gene-site checks per fill encounter times steps
per check (gate costs: empty list 71; history or source fills about 1,340 steps each, none/role/root 224 to 232,
behaviour 28,866), lists priced alike in the inert and live cells (inert fills are held, scanned, never applied):
steps per fill encounter I 7,146 / 7,522 (g 1,000 / 2,000), M 8,686 / 7,903: ratio 1.2 at 1,000, 1.05 at 2,000. The
caveat: a check on a list of about four history or source fills costs about 5,400 steps against 71 for an empty list
(75×), and the cost is dominated by the fills; behaviour fills would cost 29,000 each, but none survives. Mean, not
median (the snapshot has no per-list distribution), so this is a mean-based model.

## Not scored, and why

RE 4 (SOG wing), RE 5 and R10 (fission–fusion), R13 (recency-only conflict rule), R14 ((400, 64)): dropped by the drop order
of the spec (notes §2.5 items 9 and 10). The conflict rule's role is therefore untested here; the surviving fills are
nearly all from two scopes (history, source), where rank matters only between them.

## Interim numbers that changed since the interim report (2026-10-21)

M-source 2/18 → 3/20 (UO); M-root 3/16 → 4/20; seedonly 14/19 → 15/20; nowrite 14/19 → 14/20; idroutes 15/19 → 15/20;
clone 0/19 → 0/20 (raw identity per island 0.4877 → 0.4820); eight secondary cells (M-none, M-role, nocopy, nocontract,
shuffle, noinherit, grudge-only, renorm) did not exist in the interim. Verdict-relevant: R6 (M-root, M-source), R7
(+0.63 → +0.60), R12 (−0.63 → −0.65), R11 (audit added). No verdict flipped.

## Cautions

- 20 replicates give wide intervals: a UO of 11/20 has a 95% interval [0.32, 0.77]. The 10-replicate cells score nothing
  registered except as stated (RE 2's controls, R7's controls) and are inconclusive where 10 runs cannot decide.
- The ablations are scored at 1,000 where M is mid-scramble. The registered ablation comparison at 2,000 does not exist.
- Rows are single draws of the lottery: one counted row (M-source rep 16) did not reproduce on rerun (notes §2.8); it stays as counted.
