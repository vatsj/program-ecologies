# Verdicts: hooks follow-ups in the weak wing (open vs parochial keys; union contracts), 2026-10-21

Predictions: `predictions/2026-10-21-hooks-followups-weak.md` (committed 87b6e8b, before any counted cell). Numbers: `runs/hooks-w2.md`
and `runs/hooks-w2.json` (rows `runs/hooks_w2/*.json.gz`). PD (100, 64), 40 runs, generation 1,000; fission–fusion 32 × 100
merged at 200, horizon 600, 20 runs; union game (30, 16), horizon 1,000, 40 runs. All ε = 0 lottery statistics at finite
(N, I, horizon). Reproduction: `lineage-max` 40/40, `ff-lineage-max` 20/20 and `myopic-ref` 40/40 runs identical to Part W's stored
maximal rows. Probes seen before the counted cells are disclosed in notes §2.3 point 7 (they bore on A4, B4 and A2/A7).

Key: **held** = claim and falsifier-side both fine; **failed** = the claim is false (falsifier fired where stated); **partial** = some clauses hold.

## The RE's predictions

| # | claim | number | verdict |
|---|---|---|---|
| RE 1 (amended) | open maximal universal-open ≥ 0.65 against lineage maximal ≈ 0; falsifier ≤ 0.2 | `open-max` 0.875 [0.74, 0.95]; `lineage-max` 0.000; paired +0.875 | **held** |
| RE 2 (amended) | open contracts only ≥ 0.5; open history only ≤ 0.3; falsifier: reverse ordering | `open-contract` 0.000, `open-history` 0.975 (paired −0.975 [−1.00, −0.93]) | **failed, falsifier fired** (the reverse ordering, by a wide margin) |
| RE 3 | `ff-open-max` ≥ 0.7; falsifier ≤ 0.4 | 1.000 [0.84, 1.00] against `ff-lineage-max` 0.050 | **held** |
| RE 4 (restated) | (M) fair share ≤ 0.05; "never" restated as against non-conceding constant bosses | `union-M` fair 0.000; 680 of 161,864 accepted union contracts (0.42%) were demands above the pre-contract wage against a boss classified constant (the hand table says 0) | fair clause **held**; the "never" clause **partial** (0.42%, not 0; not traced) |
| RE 5 | (C) fair share ≥ 0.2 with strikes ≤ 10⁻²; falsifier fair ≤ 0.05 | `union-C` fair 0.000; execution 0.0009 at s = ¼ but 0.125 at s = ½ | **failed, falsifier fired** |
| RE 6 | role-keyed does at least as well as lineage-keyed under (C); falsifier lower by ≥ 0.2 | `union-C-role` fair 0.200 vs `union-C` 0.000 (paired +0.200 [0.075, 0.325]) | **held** |
| RE 7, clause 1 | static class keys make open contracts fail | the technology was replaced by amendment 1 | **superseded, not scored** (the logged sucker rate 0.0006 in `open-max` shows no exploited-promise mechanism for the amended key) |
| RE 7, clause 2 | lineage-keyed (C) ≤ 0.10; role-keyed (C) ≥ 0.30 | 0.000 and 0.200 [0.075, 0.325] | lineage clause **held**; role clause **failed** (0.20 < 0.30, the interval spans it) |

## My predictions

| # | claim | number | verdict |
|---|---|---|---|
| A1 | reference reproduces Part W: universal-open ≤ 0.10, island eff ≤ 0.35, lineage-closed ≥ 0.10, rows identical | 0.000; 0.224; 0.179; 40/40 identical | **held** |
| A2 | `open-max` universal-open ≈ 0.85 (≥ 0.6), up ≥ 0.2, island eff ≥ 0.9; falsifier ≤ 0.4 | 0.875; paired +0.875 (up); island eff 0.997 | **held** |
| A3 | lineage-closed ≤ 0.02 under `open-max` | 0.000 [0.000, 0.000] | **held** |
| A4 | `open-contract` ≥ 0.5, `open-history` ≤ 0.3, gap ≥ 0.2; falsifier reverse ordering | 0.000 and 0.975 | **failed, falsifier fired** (the mechanism was wrong: the open *writes*, not the open contracts, carry the recovery; see Reading) |
| A5 | sucker rate of open-contract holders ≤ 0.02; ≥ 0.5 of winning-island majorities hold an open contract-origin fill or are plain provers; falsifiers ≥ 0.10 or ≤ 0.25 | sucker 0.0006 (742,471 holder-encounters; 419 events) in `open-max`; survival 0.000 (the majorities are bare hooks holding open *written* fills, 0.90 of individuals, and are all FairBot-compatible, 1.000) | sucker clause **held**; survival clause **failed, falsifier fired** as worded (the survival I defined was contract-origin) |
| A6 | open contract fills executed per held ≥ 5× lineage contracts' rate; falsifier ≤ 2× | `open-max` 0.526 vs `lineage-max` 0.167 = 3.2×; (`open-contract` 0.918 = 5.5×) | **failed** (the ≥ 5× clause; falsifier not hit); holds only in the cell where contracts carry the dynamics |
| A7 | `ff-open-max` ≥ 0.6 (est. 0.8), `ff-lineage-max` ≤ 0.15; falsifier ≤ 0.3 | 1.000 and 0.050 | **held** |
| A8 | acceptance per attempt, open ≥ lineage | `open-max` 0.357, `open-contract` 0.378, `open-history` 0.390 (open-contract cell), against `lineage-max` 0.362; `ff` 0.245 vs 0.373 | **partial** (descriptive; equal within noise, lower in the ff cell) |
| B1 | `myopic-ref` ¼ share in [0.75, 0.95], fair ≤ 0.02, rows equal | 0.850; 0.000; 40/40 identical | **held** |
| B2 | (M): ≤ 5% of acceptances raise the wage against constant bosses; fair ≤ 0.05; ¼ modal in 0.65–0.9 | 0.42%; 0.000; ¼ share 0.808 | **held** (with the nonzero 680 noted) |
| B3 | (C) lineage: fair ≤ 0.15; realized wage short of predicted in ≥ 0.3 of challenges; execution ≥ 0.1; falsifier fair ≥ 0.3 or execution ≤ 10⁻² | fair 0.000; shortfall 0.12 at s = ½ (demand met 0.881), 0.001 at s = ¼; execution 0.125 at s = ½, 0.0009 at s = ¼, 0.005 pooled | fair clause **held**; mechanism clauses **partial/failed** (the mismatch is real only for the ½ demand, at 0.12 not 0.3; pooled execution under 10⁻², the falsifier's second clause fires) |
| B4 | (C) role: fair ≈ 0.30 (region [0.2, 0.6]); execution ≤ 0.05; role − lineage ≥ 0.2; falsifier fair ≤ 0.10 | fair 0.200 [0.075, 0.325] (8 of 40 runs, all 16 islands each); execution 0.205 (s = ¼) and 0.366 (s = ½); gap +0.200 | **partial** (fair at the edge of the region, gap met, execution clause failed by a wide margin) |
| B5 | `bw-only-C` flat against `myopic-ref` (|Δ| ≤ 0.1) on the ¼ and fair shares; falsifier ≥ 0.2 | fair Δ 0.000; ¼ share 1.000 (Δ +0.150 [0.05, 0.275], grey); zero-wage 0.000 | **failed** (the ¼ share clause; falsifier not hit) |
| B6 | acceptance rules reproduce §1.5's hand table; R1, R2 stable plays | all 36 grid cases, R1 (work, ½), R2 (strike, 0): 0 mismatches (54 tests) | **held** |
| B7 | (M) adoption ≤ 0.01 per encounter; (C) role ≥ 3× `union-M`; falsifier ratio ≤ 1.5 | `union-M` 0.0028; `union-C` 0.0044 (1.6×); `union-C-role` 0.00048 (0.17×) | M clause **held**; (C) clause **failed, falsifier fired** |

## Registered post-hoc diagnostics (not scored; my registered hand expectations)

| cell | universal-open | hand expectation (notes §2.3 point 8) | outcome |
|---|---|---|---|
| `open-max-nocontract-strict` | 1.000 | (no expectation; the contract is not needed) | contract fills inert: still 1.000 |
| `open-writes-only` | 0.950 | ≥ `open-history` − 0.1 (0.875) | **held** |
| `open-grudge-only` | 0.500 (island eff 0.982) | ≥ `open-history` − 0.1 | **failed** |
| `open-thanks-only` | 1.000 | lower than `open-grudge-only` | **failed** (higher, 1.000 vs 0.500; the grudge-converts-suckers story is not the mechanism) |

## Reading

- **In the PD the collapse follows lineage-keyed *writes*, not contracts as such.** Open writes alone recover the lottery (`open-writes-only` 0.95, `open-thanks-only` 1.00, `open-history` 0.975 even with lineage contracts held and active, 0.12 per sampled encounter), while open contracts with lineage writes do not (`open-contract` 0.000, lineage-closed 0.29, island eff 0.72). The mechanism behind open writes is not isolated: thanks alone does better than grudges alone, so exploited suckers turning into provers is not the main route. I did not test why.
- **Contracts are not needed under open keys:** `open-max` held 0.001 of individuals with open contract-origin fills at the horizon (accepted 0.0013 per encounter), `open-max-nocontract-strict` is 1.000, and the majorities are bare `HOOK(t, ·)` programs holding open written fills (0.90), all FairBot-compatible. Promises that work (sucker rate 0.0006), written by behaviour.
- **Union contracts do not reach the fair wage by a lineage key.** `union-M` ≈ Part W (¼ 0.81); `union-C` ¼ 0.89 with the boss's response implemented (114,161 of 255,235 acceptances) and no fair island, because the demand binds a boss lineage that is outcompeted by other lineages paying ¼, leaving dead-letter demands. Role keying reaches the fair wage in 8 of 40 runs (the demand binds every boss) but with high strike execution (0.37 at s = ½); the free-rider problem (holders of the ½ demand strike against bosses that do not concede) limits spread.
- **Protection alone locks the ¼ wage:** `bw-only-C` (Part W's maximal plus the (C) protection of the boss's contracted wage) gives ¼ on every island in all 40 runs (worker 0.25, boss 1.50): a commitment property, not a credible-response one.
- **The hand table was right** on the 36 constant-boss grid cases and on R1/R2; the 680 (M) wage-raising acceptances against "constant" bosses are unexplained (the definition of constant, nat = 0 and no behaviour fill, may be too narrow; untraced).
- Finite lotteries only; one encounter per birth; reduced geometries; no ε → 0 object here.
