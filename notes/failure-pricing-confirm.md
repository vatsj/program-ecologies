# Confirming failure pricing as the default compute charge (notes, 2026-10-25)

Spec `specs/2026-10-25-failure-pricing-confirmation.md` (reviewed by gemini-4-argon, then gpt-6.1-sol in amended mode; both
folded). Builds on `notes/pricing-rules.md` (the ledger semantics §1.0, the four rules, the PD play-step model) and the merged
code `src/pricing_rules*.py`. §1 is written by hand before any code of this run and before any counted cell: nothing in §1
has been run (the only arithmetic done on a machine is the Wilson interval of a count out of 40, a calculator use, and
the stored tables quoted with their source). The code is checked against §1 afterwards by
`tests/test_failure_pricing_confirm.py`, never the other way round. §2 (choices where the spec is silent, deviations,
caches) is appended with the code, before any counted cell.

Object. The default under test is **rule A (failure pricing)**: a raw payoff charge P_fail for each timed-out read call of a
play, root steps and finishing reads free. Every game is read as in `notes/pricing-rules.md` §1.0: a *timed-out call* is a
simulation frame closed on `TO` (fuel, partial cap, stuck term) or a `prp` that hits its cap; nested timed-out calls are
counted each. LOTTERY objects at fixed geometry, never π.

## 1. Hand derivations

### 1.1 Who pays for a failed read (RPS, inspection)

The play of x against y is the evaluation of x's code with fuel K (10⁴). **All timed-out calls inside x's evaluation are
charged to x**, whoever's code issues them: a call x starts is x's; a call started inside the frame in which x simulates y's
code (a nested simulation) is also inside x's evaluation, so it is x's charge too. y's own evaluation of y against x is a
separate play with a separate ledger, charged to y. The simulated copy of y pays nothing (it is a frame, not a player).
Hand cases (notes/pricing-rules.md rows 4 and 6). `SIM100R` against `SIM100R` (row 4): x's root call has k = 100 and times
out; the inner frames, in which the opponent's code simulates x, are closed by the enclosing timeout and are not separate
timed-out calls. So x pays P once and, by symmetry, so does y: each side pays P per play. `SIM100R` against `SIM20R` (row 6):
x's call (k = 100) finishes with value R, but inside it y's code starts a call of its own (k = 20) that times out (22
steps): that call is x's (it lies inside x's evaluation), so x pays P once for a timed-out call nested *inside a finishing
call*; y, evaluating `SIM20R` against `SIM100R`, has its own root call time out and pays P once (row 5). A timed-out call
nested inside another *timed-out* call can occur only where the inner frame runs out of its own fuel strictly before the
enclosing frame does and the enclosing frame then also times out; the instrumented forest decides the count, and the run
reports it (topmost, nested inside a timed-out call, issued from the opponent's code).
Caching does not change A's charge: A has no cache; every timed-out call of every play is charged.

### 1.2 The three scores with hand examples

All three are run-level values (a run is one lottery at the cell's geometry: 64 islands of 100 programs per role at (100,
64); 16 islands of 400 at (400, 16)); the island values at generation 2,000 are averaged over the islands of the run. Cell
intervals are run-clustered percentile bootstrap (4,000 resamples, seed 20261025) for means and Wilson for counts of runs.
Status of a target with threshold θ and direction as in the registered targets (`predictions/2026-10-25-pricing-rules.md`):
met if the interval lies on the good side of θ, failed if it lies on the bad side, undetermined otherwise.

**(a) RPS by mixing.** Statistics per island: e_gross = max over the exploiter set (all programs but the disabled) of the
gross payoff against the island's population; forfeit = the fraction of plays that are forfeits (fuel exhausted at the root).
Run values are the means over islands. **By-mixing status:** met if the interval of e_gross has upper bound ≤ 0.10 **and**
the interval of the forfeit rate has upper bound ≤ 0.05; failed if either interval lies above its threshold; undetermined
otherwise. (Forfeiting is payoff-negative in this game: `rps_payoffs` sets u[forfeit, action] = −1 and u[action, forfeit]
= +1; so a population that "survives" by non-play is exploitable by any constant.) The *net* target (registered) is the
same with the net payoff (e_prog ≤ 0.10); a rule can meet the net target by mutual non-play, which the by-mixing score
excludes.
*Hand examples.* (i) An island of `PRR` only (a guarded mixer, uniform digits): the best constant response earns the
expectation of a uniform opponent, 0 against any action, so e_gross = 0; forfeit = 0; by mixing: met. (ii) An island of the
constant `R0` only: `P0` earns +1, so e_gross = 1: failed. (iii) An island whose programs all forfeit against each other:
a constant earns +1 against a forfeiter, so e_gross = 1 and forfeit = 1: failed by both. (iv) From the stored
run (`runs/pricing-rules.md`, RPS detail): A at 1 has e_prog 0.029 [0.010, 0.052] (net target *met*) but e_gross 0.515
[0.417, 0.613] and forfeits 0.418 [0.321, 0.523]: by mixing **failed**; A at 10: e_prog 0.093 (undetermined) but e_gross
0.800 and forfeits 0.631: failed. A at 0.1: e_gross 0.000, forfeits 0.000, individual mixing 1.000: met. This is the
pattern prediction 4 expects to reproduce on fresh runs.
*Modal programme.* The programme with the largest count on an island (ties to the lowest index); the PRR share is the
fraction of islands (pooled over the run, then over runs) whose modal programme is `PRR`. Stored A 0.1: 2,331 of 2,560
islands (0.91) had `PRR` as the modal programme (a count from the stored `dom2000`).

**(b) PD cost-inclusive.** *Payoff range.* The PD payoff matrix of the kernel is PAYM[my action][their action] with D = 0,
C = 1: [[−1, +1], [−2, 0]] (D against D −1, D against C +1, C against D −2, C against C 0). The range is max − min =
1 − (−2) = **3** (the temptation minus the sucker's payoff, T − S). Stakes-normalized charge 0.1 × 3 = **0.3**; the
registered cost-inclusive cap is 0.1 of the range = 0.3 per play; Prediction 5's cap is 0.01 of the range = **0.03** per
play. **The stakes-normalized PD point A_s = 0.3 is the same price as the band's A at 0.3**; the PD A_s cell is the A 0.3
cell, not a separate run (a design fact, not a prediction).
*End-state charge per play.* At the last generation g_end of the run, for each island the mean over ordered pairs of
distinct individuals (a, b) of the charge of a's play against b (play plus production acts; zero when nothing times out),
weighted by counts (each ordered pair of individuals once); the run value is the mean over the 64 islands (all islands have
N = 100, so this is the encounter-weighted mean over the final population). This is `pop_ledger[:, 3]` of the merged code.
*Reported beside it:* the **scramble charge** = the mean over checkpoints with g ≤ 200 of the same population charge per
play (right-endpoint rule: a checkpoint's state stands for the interval it closes; checkpoints every 10 generations to
g = 1,000, so 20 checkpoints of weight 10), and the **cumulative run-average charge** = the same mean over every
checkpoint of the run weighted by the interval length. The scramble charge is the statistic that can show a price acting as
an entry filter. For a stored row the scramble and cumulative charges are unavailable (only the end-state ledger was kept).
*Persistence.* The registered PD verdict reads the universal-open class at the run's last checkpoint (generation 10,000 or
the frozen stop). Here a run is **persistent universal-open** if the last checkpoint is universal-open and the state has been
universal-open for the last 500 generations: if the run is frozen (a single global type whose own encounters change nothing;
absorbing) it counts; if it is not frozen it counts only if the last change of the universal-open indicator is at least 500
generations before the last generation or never happened. A run that ends universal-open but changed to it within the last
500 generations is *late* (not counted, reported). A non-frozen run at 10,000 is *censored* (it did not reach an absorbing
state); censored runs are kept, scored by the same rule and reported by number. Example: last indicator change at g = 9,800
and the run ends at 10,000 unfrozen: late. Frozen at 4,200 with the last change at 4,150: persistent.
*Scores.* Three counts per cell, out of 40 runs: **(A)** end-snapshot universal-open (the registered style);
**(B)** persistent universal-open (the cost-blind verdict of this run); **(C)** persistent universal-open and end-state
charge per play ≤ 0.3 (the cost-inclusive verdict, the PD score of the classification). Status of (B) and (C) against the 0.70
line by the Wilson interval, as registered. Wilson intervals of counts out of 40: 33/40 = 0.825 [0.680, 0.913]
(undetermined), 34/40 = 0.850 [0.709, 0.929] (met), 35/40 = 0.875 [0.739, 0.945], 30/40 = 0.750 [0.598, 0.858]
(undetermined); **34 of 40 is the smallest count that meets the line**. If the true rate is 0.85 the chance that 40 runs
reach 34 is 0.61; at 0.875, 0.77; at 0.90, 0.90 (a binomial calculation): a true rate near 0.85 classifies as met only
about 60% of the time, undetermined otherwise, which is the reviewers' point.
*Hand examples on stored cells* (`runs/pricing-rules.md`, supplementary table, mean end-state charge per play): F 10⁻² has
91.8 per play (≫ 0.3), so every run fails (C) although 20 of 20 are universal-open; F 10⁻³ has 8.7 and fails; F 10⁻⁵ has
0.188 and passes the charge cap but only 9 of 20 are universal-open; B 10⁻² has 0.040 (four root steps at 0.01) and
passes. A 0.1 has 1.8·10⁻⁵ and passes. A cell's charge is a mean, the cap applies to the run's value.
*A single timing-out individual.* If one individual of an island of 100 times out in every one of its plays at P = 0.1, the
ordered pairs with it as the first player are 99 of 9,900 (1%), so the mean charge per play is 0.001 (0.00033 of the range).
To reach 0.03 per play at P = 0.1 about 30% of plays must time out, at P = 10 only 0.3%. Prediction 5's 0.03 cap is
therefore a statement about how often the *final* population's plays time out.

**(c) Inspection net of charges.** Per island: gross means u0g = Σ_a X0[a] (X1 · UAg[a, ·]) and u1g similarly for the
inspectee (the stored `u0g`, `u1g`); **net means** u0n = same with the net matrix UA = UAg − charge0 and u1n with UB = UBg −
charge1, where charge0[a, b] = P_fail × (expected timed-out calls of the inspector program a in its play against
inspectee b) and charge1 likewise for the inspectee (the stored `u0`, `u1`). The charge is paid by the role that evaluates
the program, as in §1.1. **Efficient (gross)** iff u0g ≥ −0.05 and u1g ≥ −0.05 (the registered criterion); **efficient (net)**
iff u0n ≥ −0.05 and u1n ≥ −0.05. The criterion is absolute: there is no comparison set and no frontier adjustment (the
frontier is the efficient pair (0, 0), the payoff-sum maximum of the game, and a charge only lowers the payoffs available
to both). Since the charge is ≥ 0, net-efficient ⊆ gross-efficient on every island. The run value is the fraction of
efficient islands; the target is the registered ≥ 0.60 on the interval of the run values.
*What the net criterion costs.* An island with gross payoffs (0, 0) can afford a charge of 0.05 per role per play, i.e. at
most 0.05/P timeouts per play on average: 0.5 at P = 0.1, 0.17 at 0.3, 0.05 at 1, 0.005 at 10. The inspector's mean game
payoff in the stored A 0.1 cell was −0.042 [−0.084, 0.000] (close to the −0.05 line), so an inspector charge of 0.003 can
move a borderline island across the line: the stored charge per play was 0.0031 for inspectors and 0.0000 for inspectees.
Example (notes/pricing-rules.md row 11): an island of mutual simulators `SI100n` vs `SE100k` has one timed-out call per play
on each side (the inspector's root call times out; the inspectee's too), so at P = 0.1 both pay 0.1: gross → net shift −0.1
for both roles, which turns any island with gross ≤ 0.05 for a role into a net-inefficient one.
*Stored rows.* Island-level net efficiency needs the island counts, which the stored rows do not keep (they keep run means
of u0, u1): the stored table marks the inspection net score **unavailable**. The run means (u0g − u0, u1g − u1) give the
charges, reported.

### 1.3 Classification of the default (frozen)

The default is **A at P_fail = 0.1**, classified at the primary geometry (100, 64) on the fresh runs.
* *RPS component statuses:* the net target (e_prog ≤ 0.10) and the by-mixing score. The game's status is the worst of
  its components in the order failed < undetermined < met.
* *Inspection:* the net-of-charges efficient fraction (target ≥ 0.60); the gross fraction is reported beside it.
* *PD:* score (C) against the 0.70 line.
* **confirmed** iff all three games are *met*; **refuted** iff any game is *failed*; **unresolved** otherwise.
The geometry (400, 16) (RPS and inspection only; the PD at (200, 64) was not rerun) is classified separately with the same
rules on the two games and reported as a qualifier: the headline label is the (100, 64) label, and a *failed* at (400, 16)
is stated in the headline as a limit. The band: the same statuses at each level 0.03, 0.1, 0.3, 1, 10, with the by-mixing
and cost-inclusive columns. Conclusions are restricted to these geometries, grammars, caps and world K.

### 1.4 Stakes-normalized point

A_s sets P_fail = 0.1 × the game's payoff range. Ranges from `notes/pricing-rules.md` §1.1: RPS 2 (±1) → **0.2**;
inspection 5 (from −4, the inspector's payoff for N against a cheat, to +1, the inspectee's payoff for cheating unpunished) →
**0.5**. The payoff tables P0 = [[−1, −1], [0, −4]] and P1 = [[0, −3], [0, 1]] have per-role ranges of 4 each, so a per-role
normalization would give 0.4; the spec's 0.5 is kept and the difference is below the resolution of the grid. PD 3 → **0.3**
(the same price as A at 0.3). The test is one point per game, not a band: the question is whether the verdicts at the
normalized price agree with the verdicts at the raw 0.1 (and with the grid values on either side).

### 1.5 Seeds and freshness

**PD** (world K, S-nonself, cell `wk_Snon_100_64`: N = 100, I = 64). Founders are drawn from
`default_rng([N, I, rep, SALT])` with SALT = 20,261,012; the kernel seed is
`kernel_seed(N, I, rep) = (rep·1,000,003 + N·10,007 + I·101 + SALT) mod 2⁶²`
= rep·1,000,003 + 1,000,700 + 6,464 + 20,261,012 = rep·1,000,003 + 21,268,176; the arrival-stream seed is a fixed linear map
of it. **None of these depends on the price or the rule**: the zero-price run and the priced run of the same `rep` start
from the same founders and the same random stream and differ only through the payoff. So price-minus-zero differences on the
same `rep` are **paired** on founders and seed stream. Stored indices: reps 0–19 (registered) and 20–39 (supplementary).
**Fresh PD indices: reps 200–239** (kernel seeds 221,268,776 … 260,268,893: for rep 200, 200 × 1,000,003 =
200,000,600, plus 21,268,176 = 221,268,776; for rep 239, 239,000,717 + 21,268,176 = 260,268,893). The seed is increasing in
rep, so the fresh seeds are disjoint from the stored 21,268,176 … 60,268,293 (reps 0–39); the founders' streams differ
because rep is an entry of the seed sequence.
**L_T (RPS, inspection).** Founders: `run_seed('founders|cell|role', run)` =
crc32(`'rps|founders|<cell>|<role>|<run>'`) & 0x7fffffff, price-independent; the dynamics seed is
crc32(`'rps|dynamics|<cell>|<game>|<arm>|<label>|<K>|<renorm>|<run>'`) & 0x7fffffff with the label `'0'` for the zero price
and `'A@<P>'` for failure pricing, so the dynamics stream differs between prices (the founders are paired; the
dynamics are not). Stored indices: primary 0–39 (RPS A 10 also 40–79), size 0–19. **Fresh L_T indices: runs 100–139** at
both geometries. The `test_fresh` guard recomputes the set of founder and dynamics seeds of the stored cells (all stored run
indices, all stored labels) and of the fresh cells and asserts that they are disjoint (a collision of 31-bit hashes has chance
~10⁻⁵ over these ~10³ pairs and is checked, not assumed).
**Seeds of the new price levels** (0.03, 0.3, 0.2, 0.5) use the same rule with their own labels; they have no stored
counterpart.

### 1.6 Caches are semantic accelerators, not price tables

The PD kernel loads world-K statics (`runs/provenance/{static,sets.npz,OSV.npy,SPO.npy,prod_exec.json}` and
`runs/detectors/K/…`), built on 2026-10-24 (file times 14:06–14:13), before the pricing study existed (2026-10-25). They
tabulate, per program and per pair of programs: decision trees, check outcomes (CHC, CHD, UVt), the production outcomes and
their step costs, the OSV/SPO tables: facts about the *calculus*, none of which has a price argument. Prices enter only in
`pricing_rules_pd_model.make_px` (the PX tuple: class costs, rule code, level, K), computed afterwards from these tables. The
imported caches are hashed (sha256) before and after the run and the hashes must agree (read-only use). The
zero-price run reproduces the stored zero-price run draw for draw (the validation), which would fail if the caches or the
payoff entry were price-dependent. Code is identified by the hash of every `src/pricing_rules*.py` module and the commit.

### 1.7 Further outputs, definitions (fixed before the run)

* **Paired differences** price − zero per run (PD: same rep, shared founders and seed stream; RPS and inspection: same run
  index, shared founders): bootstrap percentile intervals over the 40 runs for continuous run values, and for the PD counts
  the difference of proportions with the paired bootstrap.
* **Timeouts** by programme (the share-weighted expected timed-out calls per play of each program, island mean, at
  generations 500 = scramble and 2,000 = later), by depth (topmost / nested inside another timed-out call / issued from the
  opponent's code inside a simulation), per role in the inspection game. The PD has only primitive reads (≤ 2 per play,
  check or production, no nesting): its timeouts are reported by stage (g ≤ 200 and later) and not by program or depth.
* **Support and transitions:** per island the support (programs with share ≥ 0.05) at the checkpoints; a *transition* is a
  change of the modal programme or of the support set between consecutive checkpoints (500, 1000, 1500, 2000, 4000); per
  cell: the share of islands whose modal programme changed from 1,500 to 2,000 and the most frequent modal programmes and
  supports. For the PD: the holder spellings of the 64 islands at the end, the number of holder changes after generation
  500, and the class string.
* Conclusions never leave the tested geometries.
