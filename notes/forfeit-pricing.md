# Charging forfeits like failed reads, exact simulators, and the security fallback (notes, 2026-10-26)

Spec `specs/2026-10-26-forfeit-pricing.md` (reviewed by gemini-4-argon, then gpt-6.1-sol in amended mode, folded; with the
RS's addendum on A_m, reviewed the same way, folded; merged from main at 21402ed before any code of this run). Builds on
`notes/pricing-rules.md` (ledger semantics §1.0), `notes/failure-pricing-confirm.md` (the scores, §1.2-1.3) and
`notes/lt-tape.md`. §1 is written by hand before any code of this run and before any counted cell: nothing in §1 has been
run (the only machine use is a calculator: template sizes and the length-prior masses of the catalogue, quoted below with
their source, `lt_tape_games.prior_masses`). The code is checked against §1 afterwards by `tests/test_forfeit_pricing.py`,
never the other way round. §2 (choices where the spec is silent, deviations, caches) is appended with the code, before any
counted cell.

## 1. Hand derivations

### 1.0 The three rules and what they charge

Notation. One root evaluation of x against y (fuel K = 10⁴ in RPS and inspection). Its **trace** is the sequence of
failure events in x's own evaluation:

* a **capped read timeout**: a simulation frame that was opened by `run k a b` with a cap k below the caller's remaining
  fuel and is closed on `TO` (own fuel, partial cap, stuck inner term), or a `prp` that hits its enumeration cap; counted as
  in `notes/pricing-rules.md` §1.0, nested closed calls each, a frame closed by an enclosing timeout not separately;
* a **forfeit**: the root's own fuel runs out (`K` or `K-search`: a primitive whose charge exceeds the root's remaining
  fuel); the stored `fuel` statistic;
* an **uncapped read**: a `run` whose fuel is the caller's whole remaining fuel less the steps reserved for the response
  (§1.2). It has no cap of its own, so its failure *is* the root's running out: it closes on `TO` only at the reserved
  boundary and the program has no default for it. An uncapped read that fails is a forfeit event, never a read timeout.

The charges, in payoff units, as a function of P = P_fail:

| rule | charge of one root evaluation | game outcome of a forfeit |
|---|---|---|
| **A** (the merged default) | P × (capped read timeouts) [+ P × uncapped timeouts the program survives, 0 in this catalogue] | the game's own forfeit outcome (RPS: −1 against any action, the opponent +1) |
| **A_f** (the RS, 2026-10-26) | P × (capped read timeouts + [forfeit] + survived uncapped timeouts): one charge per distinct failure event | the game's own forfeit outcome, as A |
| **A_m** (the RS addendum) | the same charge as A_f | the forfeiter is replaced by its security (maximin) strategy |

*One failure, one charge.* An uncapped read that exhausts the root is the forfeit: one P under A_f (zero under A, where
forfeits are free and the failed read is not a capped timeout). A root that times out a capped read and later forfeits for
another reason has two failure events: 2P under A_f.

*Which failures are the root's.* The existing accounting (`notes/failure-pricing-confirm.md` §1.1, the merged `n_to`) is
kept: every capped read timeout in the forest of x's evaluation is x's, including a call issued from the opponent's code
inside the frame in which x simulates the opponent (hand row 6 of `notes/pricing-rules.md`). What the amended spec means by
"failures inside a simulated execution are not charged to anyone" is the *forfeit* of a simulated copy: a simulated root
that runs out of its fuel is a frame closing on `TO`, charged to the simulator only as its own read's outcome (a capped
timeout if capped, the forfeit if uncapped), and the simulated copy pays nothing. Reading the sentence more broadly would
make A_f differ from A on plays without forfeits, which contradicts "nothing else changes" and the planned draw-for-draw
validation; the choice is flagged for the RS in §1.7.

*Worked plays (charges, in P).*

| play | events | A | A_f / A_m |
|---|---|---|---|
| constant against anything (2 steps) | none | 0 | 0 |
| `SIM100R` against `R0`: read finishes | none | 0 | 0 |
| `SIM100R` against `SIM100R`: root's call times out, default played | 1 capped timeout | 1 | 1 |
| `SIM100R` against `SIM20R`: the inner call (cap 20) times out inside a finishing call | 1 capped timeout, issued from the opponent's code | 1 | 1 |
| `PB` against a program whose proof search exceeds the root's fuel (`K-search`) | 1 forfeit | 0 | 1 |
| `SIMX` against `SIMX`: the uncapped read exhausts the root, forfeit | 1 forfeit (the read's failure *is* it) | 0 | 1, not 2 |
| a program that times out a capped read, then loops: `let v = run 20 them me in Ω` | 1 capped timeout + 1 forfeit | 1 | 2 |
| `SIMX` against `SIM100R`: the opponent's cap-100 read times out inside SIMX's finishing read | 1 capped timeout | 1 | 1 |

### 1.1 Forfeit payoff tables, entry by entry (before any P)

All tables list (payoff to the forfeiter or to the row player, payoff to the other), gross of charges, charges after.

**RPS** (`rps_payoffs`: u(F, a) = −1, u(a, F) = +1, u(F, F) = 0). x forfeits, y plays a pure action a:

| | x's game payoff | y's game payoff | x's charge |
|---|---|---|---|
| A | −1 | +1 | 0 |
| A_f | −1 | +1 | P |
| A_m | 0 (the referee's uniform draw has expectation 0 against any pure a) | 0 | P |

Both forfeit: A (0, 0), no charge; A_f (0, 0) with P charged to each, so (−P, −P); A_m both replaced by independent uniform
draws, expectation (0, 0), (−P, −P) after charges. So A_f differs from A only by P on the forfeiter, and from A_m
by the ±1 on every unilateral forfeit: under A and A_f a program that makes its opponent run out of fuel gains +1; under
A_m it gains 0. A forfeiter's realized action under A_m is a uniform draw independent of everything.

**Inspection** (`insp_payoff_tensors`; P0 = [[−1, −1], [0, −4]] rows I, N against columns C, K, P1 = [[0, −3], [0, 1]]).
Stored convention: a forfeiter plays its worst action against the realized opposing action (ties averaged), both forfeit:
each its worst table entry.

| situation | A, A_f (stored): outcome, (inspector, inspectee) | A_m: forfeiter plays security |
|---|---|---|
| inspector forfeits, inspectee C | worst for inspector against C: I (−1 against 0): (−1, 0) | I (security: min(−1,−1) = −1 beats N's −4, pure): (−1, 0) |
| inspector forfeits, inspectee K | worst against K: N (−4): (−4, +1) | I: (−1, −3) |
| inspectee forfeits, inspector I | worst against I: K (−3): (−1, −3) | C (security 0, pure): (−1, 0) |
| inspectee forfeits, inspector N | worst against N: C (0): (0, 0) | C: (0, 0) |
| both forfeit | (−4, −3) | (I, C): (−1, 0) |

Charges: P to each forfeiter under A_f and A_m, 0 under A. Where A_m's pure security action differs from the stored forfeit
outcome (the entries (inspector forfeits, K): (−4, +1) against (−1, −3); (inspectee forfeits, I): (−1, −3) against (−1, 0);
both forfeit: (−4, −3) against (−1, 0)) inspection under A_m is a separate treatment of the game, not an equivalence check
of A_f. The gap to A_f comes from the inspectee's +1 for an inspector forfeit (stored), which A_m removes.

**PD** (PAYM[mine][theirs], D = 0, C = 1: D–D −1, D–C +1, C–D −2, C–C 0). The kernel has no forfeit outcome: a play is at
most two checks capped at 250,006 steps each plus 4 root steps (500,016), a production at most two acts of 250,005 (500,010);
the sum can exceed the encounter budget 10⁶ only by 26 steps and only if all four reads time out. A and A_f therefore have no
stored forfeit payoff to state; if one occurred it would cost P under A_f. A_m would replace it by the security action D.
The PD is run under A_f only (spec), with a read-only recorder of the maximum encounter steps to show that the forfeit
charge is exactly zero in every run.

### 1.2 The exact (uncapped, shared-fuel) simulators

*What "exact" means here* (spec, after the second review). A simulation that runs on the caller's remaining fuel less the
steps reserved for its own response; the simulated opponent runs on that shared fuel, which can differ from its own root
budget; a private tape is drawn fresh for the simulated invocation. "Exact" is exact for a deterministic opponent that
finishes within that fuel. Against a tape mixer it reproduces one sample, not the actual play.

*Construction in L_T.* There is no new primitive: `run k them me` with k = K − ρ, ρ the fixed steps that cannot be spent
on the read. A frame's fuel is decreased by every step executed while it is open and the root's fuel by the same steps, so
the frame closes (value or `TO`) no later than the point at which the reserved ρ steps remain to the root.

RPS `SIMX = λme.λthem. let v = run (K − 11) them me in beat(v, Ω)` with the ladder beat(v, d) of the capped simulators
(`beat_case`) and the default Ω = (λx. x x)(λx. x x), which loops until the root's fuel runs out (a forfeit by running out).
Steps: 2 (the two root β's) + 1 (RUN) + inner + 1 (closing) + 1 (let β) + ladder. The ladder takes 2, 4, 6 steps for v = R,
P, S and 6 for `TO` and then loops. So after the frame closes at most 1 + 6 = 7 steps are needed, and ρ = 2 + 1 + 1 + 7 = 11,
k = K − 11. Check: inner = k finished with v = S uses 2 + 1 + (K − 11) + 1 + 1 + 6 = K steps and the value is reached with
the root's fuel exactly spent (the engine tests `used ≥ K` only for non-values, so a value reached at used = K is a play).
On `TO` the closing step brings used to K − 7, the let β and 6 ladder steps to K, and Ω is a non-value at used = K: a
forfeit with reason `K`.
Inspection `SIMX_I = λme.λthem. let v = run (K − 9) them me in if v = K then I else if v = C then N else Ω` (inspect iff the
simulated inspectee cheats), `SIMX_E` = `… if v = I then C else if v = N then K else Ω` (cheat iff the simulated
inspector does not inspect). After the close: let β 1 and at most 4 ladder steps (`TO` takes 4 then Ω; the successful
branches 2 and 4), so ρ = 2 + 1 + 1 + 5 = 9. The same boundary check holds.
*Nested simulation.* The fuel passed is a constant of the term, so a SIMX that is itself simulated inside another read
opens its own frame with k = K − 11 inside a frame with less fuel: the outer frame closes first. `SIMX` against `SIMX`:
frame 1 (fuel K − 11) closes on `TO` at used K − 7 with frame 2 inside it closed by the enclosing timeout (not a separate
call): one forfeit each. Against a capped simulator SIM_k d (k ∈ {20, 100}) the opponent's inner read closes on its own cap
k, the opponent's code continues with its default d, and SIMX's read finishes having seen d.
*Failure accounting.* Under A_f and A_m the forfeit is the failure event and the uncapped frame's `TO` is not charged again;
under A the failure of an uncapped read is the forfeit and is free (the RS's framing: exact simulation fails by running
out, and under A forfeits are free). This makes X's cost under A the game's own forfeit outcome only.

*Prior masses* (the length prior over template spellings, `lt_tape_games.prior_masses`: P(size s) ∝ 1/(2 s²) over the sizes
present, uniform among the templates of the size; calculator values). The SIMX templates take half of their capped
counterpart's mass; no other mass changes, in particular the constants' (RPS 0.27307 each, inspection I0/N0 0.36296, C0/K0
0.35288) is unchanged:

| game | exact simulator | capped counterpart | counterpart's mass | each after the split |
|---|---|---|---|---|
| RPS | `SIMX` | `SIM100u` (same fuel class, default a uniform mix) | 0.00190 | 0.00095 |
| inspection (inspector) | `SIMX_I` | `SI100n` (the same rule with default N) | 0.01080 | 0.00540 |
| inspection (inspectee) | `SIMX_E` | `SE100k` (the same rule with default K) | 0.00583 | 0.002915 |

Founders for an X arm are the standard founders of the same run index (the same draws of the base catalogue, so the
concurrent no-X cells are paired on them) with each founder of a counterpart template replaced by its exact twin with
probability ½ (an independent fair coin per founder). X-sham: the same replacement, the twin a capped simulator identical to the counterpart (same fuel class and default, a different spelling), so that the seeded
behaviour mass is unchanged and only the template bookkeeping differs; the sham separates the bookkeeping of the split from
the capability; it does not by itself separate the halving of the capped class, which the X arm shares with it only through
the counterpart's half (disclosed). Expected founders per run (64 islands × 100 programs, 6,400 per role): SIMX 6.1, SIMX_I
34.6, SIMX_E 18.7: the exact simulators start at 0.1–0.5 per island, so a result that "nobody simulates exactly" can mean
scarcity. The report therefore gives the share of runs and islands in which an exact simulator is present at all, its mass
(not only its modal share) and, where it is present, whether it fixes.

### 1.3 Hand payoffs of `SIMX` against the RPS catalogue (before any code)

The play of SIMX against y; "k" is the charge count to SIMX, "k_opp" the opponent's charge count in its own play against SIMX.
Each row: SIMX's expected game payoff g and the net at each level. For every row the net is g − P × k under A_f and A_m and
g − P × k under A (the exceptions are the forfeit rows, stated).

| opponent y | y's action as read | SIMX's play | g | k | k_opp | derivation |
|---|---|---|---|---|---|---|
| `R0`, `P0`, `S0` | the constant, exactly | beats it | +1 | 0 | 0 | the read finishes in 2 inner steps; 9 steps in all |
| `U` | one fresh uniform sample | uniform | 0 | 0 | 0 | the simulated U draws its own tape; independent of the actual play |
| `B_ab` (6, 2:1 mixers) | one sample of the 2:1 law | beats the sample | +1/3 | 0 | 0 | P(sample = a1) = 2/3: e.g. B_RP: P beats R (2/3 · 2/3 = 4/9), S loses to R and beats P (1/3 · (−2/3 + 1/3) = −1/9): 4/9 − 1/9 = 1/3; the other five likewise |
| `CB_ab` (6 carriers) | as B_ab | beats the sample | +1/3 | 0 | 0 | the certificate is inert for a play |
| `H0`, `H1`, `H2` | exactly (the hash of SIMX's own quote, the same in the simulation and the play) | beats it | +1 | 0 | 0 | deterministic given the opponent's source |
| `SIM20R/P/S`, `SIM100R/P/S` | the default d (the opponent's inner read, closed on its own cap, returns TO) | beats d | +1 | 1 | 1 | the opponent's inner call times out inside SIMX's finishing read (charged to SIMX); the opponent's own root call times out (charged to it); it plays d |
| `SIM20u`, `SIM100u` | a uniform sample (the default, drawn in the simulation's invocation) | uniform | 0 | 1 | 1 | as above; the actual play is an independent uniform |
| `PRR` | uniform (its three `prp` tests fail: SIMX's play law against PRR is uniform = 1/3 < 12/27) | uniform | 0 | 0 | 0 | the enumeration charges ≈ 105 each < cap 400, no cap event |
| `CRR` | uniform (SIMX carries no certificate: `chk` rejects at once) | uniform | 0 | 0 | 0 | |
| `PB` | not derivable by hand: its three `prove` calls cost the prover's W against SIMX's quote; if the total exceeds the 10⁴ fuel PB forfeits, otherwise PB's fallback is U | | | | | tabulated by the engine; compared to the structural bound (g ∈ {0, +1}) |
| `SIMX` | none (both forfeit) | forfeit | A 0; A_f, A_m −P (the game's mutual forfeit payoff (0, 0) plus P) | 0 | 0 | frame 1 closes on `TO`; both forfeit; the failure is the forfeit, charged once |

Net payoffs of SIMX (rows with a charge), per level of P:

| row | 0.03 | 0.1 | 0.3 | 1 | 10 |
|---|---|---|---|---|---|
| against `SIM*R/P/S` (g = +1, k = 1) | 0.97 | 0.90 | 0.70 | 0 | −9 |
| against `SIM*u` (g = 0, k = 1) | −0.03 | −0.10 | −0.30 | −1 | −10 |
| against `SIMX`, A_f and A_m (g = 0, one forfeit) | −0.03 | −0.10 | −0.30 | −1 | −10 |
| against `SIMX`, A | 0 | 0 | 0 | 0 | 0 |
| against constants, hash programs (g = +1, k = 0) | +1 | +1 | +1 | +1 | +1 |
| against `B_ab`, `CB_ab` | +1/3 | +1/3 | +1/3 | +1/3 | +1/3 |
| against `U`, `PRR`, `CRR` | 0 | 0 | 0 | 0 | 0 |

The opponents' side: constants −1, `U` 0, `B_ab` −1/3, hash −1, `SIM*R/P/S` −1 − P, `SIM*u` −P, against SIMX; a capped
simulator against SIMX therefore loses 1 + P and SIMX gains 1 − P: reading a capped simulator is worth +1 to SIMX only
below P = 1. The capped family against itself: `SIM100d` against `SIM100d'` plays d against d' and pays P: net u(d, d') − P.

*Advantage on completed plays against loss on failed ones.* SIMX completes against everything except readers that are
themselves uncapped: its advantage is +1 against constants, hash programs and capped sims with a fixed default (at P < 1),
+1/3 against biased mixers, 0 against the private-tape mixers and guards (U, PRR, CRR); its loss on failed plays is P (A_f,
A_m) and an additional 1 and a +1 gift to the opponent under A_f (the game's forfeit payoff, which A_m removes). Under A the
loss is the game's −1 only. Prior abundance decides whether an exact simulator meets another: with SIMX at 0.00095 of
founders, SIMX–SIMX plays are a vanishing share of encounters unless SIMX fixes.

*Recursive reader pairs at nearby budgets.* SIMX against SIMX forfeits for every K (a regress without a base); against a
capped simulator it finishes for every K ≥ k + 40 or so. The static check at K = 9,000, 10,000, 11,000 (built in the code) must show
identical action laws and failure counts, only the step totals moving.

### 1.4 The three scores and the new statistics (fixed here)

The scores of `notes/failure-pricing-confirm.md` §1.2 (RPS net and by mixing, inspection net of charges, PD cost-inclusive)
and the classification (§1.3) are used unchanged. New or changed by the RS addendum and the reviews:

* **Exploitability for the actual policy** (`e_gross`): the best constant's gross payoff against the population, with the arm's
  own game payoff table (forfeit outcomes of A and A_f, the security replacement of A_m), fallbacks included.
* **Exploitability on completed plays** (`e_comp`): the same for plays in which neither side forfeits, i.e. a ratio of
  expectations Σ_y X_y N(x, y) / Σ_y X_y D(x, y) with N(x, y) = Σ_{a,b ∈ {R,P,S}} G[x,y,a] G[y,x,b] u(a, b) and
  D(x, y) = P(x completes) P(y completes); undefined (NaN, never zero) on an island with no completed plays; run values are
  means over the defined islands and the number of undefined islands is reported.
* **Fallback share** = the forfeit rate (A_m: the share of plays in which a forfeiter is replaced; A, A_f: the share of
  forfeits). Fallback plays are never counted as the programme's own mixing: individual mixing (`mix`) is the share of programmes
  whose *whole* play law, forfeit mass included as a separate outcome, is within 0.05 total variation of the uniform law
  on R, P, S, so forfeit mass counts against mixing; the coin share is computed on non-fallback plays.
* **By mixing** (RPS): e_gross upper bound ≤ 0.10 and fallback share upper bound ≤ 0.05, as in the confirmation run
  (A_m: with its own `e_gross`; `e_comp` reported beside it).
* **Intervals** are run-clustered 95% percentile bootstrap (4,000 resamples, the confirmation run's seed); **equivalence** at a
  margin δ is two one-sided tests: the paired difference's 90% bootstrap interval lies inside ±δ (the TOST at level 5%);
  "equivalent" otherwise unresolved, and "different" if the 95% interval excludes zero beyond the margin. "Above 0.05 by upper bound" means the upper bound of the 95% interval exceeds 0.05, i.e. not demonstrated below.
* Generation 2,000 is the primary endpoint; extensions to 4,000 cover every member of a matched comparison and are secondary.
* For every forfeit of an exact simulator: the opponent's family (population expectation at the end state) and whether the
  exact read finished, closed on `TO` (the root's fuel) or consumed a private tape inside the simulated execution.

### 1.5 Seeds and freshness

The confirmation run used L_T runs 100-139 and PD reps 200-239; the stored runs 0-79 (primary), 0-19 (size), PD 0-39.
**Fresh L_T indices: runs 300-339; fresh PD reps: 300-339** (kernel seeds rep·1,000,003 + 21,268,176: 321,269,… for 300, up to
360,270,… for 339), none used before by any module under `src/` (grep for the index ranges and a guard that recomputes the
stored seeds, as in `tests/test_failure_pricing_confirm.py`). Founder seeds are price- and rule-independent
(`run_seed('founders|cell|role', run)`), so every rule and every X arm of a run index start from the same base draw; the dynamics seed
carries a rule label (`A@P`, `Af@P`, `Am@P`, with `+X`, `+S` for the X and sham arms) so dynamics streams differ between rules,
as in the earlier runs.

### 1.6 Caches

The PD cells need the untracked world-K caches of `notes/failure-pricing-confirm.md` §1.6, copied read-only from a sibling
worktree, hashed before and after, never committed. The L_T games need nothing untracked.

### 1.7 Flags for the RS

1. **The game's own forfeit payoff stays under A_f** (the spec's reading). In RPS a forfeiter then loses 1 *and* pays P, and the
   opponent gains 1, so an uncapped simulator that fails costs P + 1 where a capped one that times out costs P and plays a
   default worth about 0: the two failures are charged equally but not paid equally. The RS's addendum (A_m: the forfeiter is
   replaced by its security strategy) is exactly the remedy and this run measures both.
2. **Under A the failure of an uncapped read is a free forfeit**, not a capped timeout: the merged rule counted frames, but
   an uncapped frame is the root's own fuel (§1.2). If A instead counted it, A and A_f would charge SIMX's failures
   identically and "A with X" would carry no information.
3. **Nested failures** are the root's under all rules (the existing accounting), the broader reading of "not charged to anyone"
   is not adopted (§1.0).
4. The exact simulators are seeded at 0.1–0.5 per island by the prior; "no one simulates exactly" is first a statement about
   abundance, and the report separates it from selection.

## 2. Choices where the spec is silent, deviations, caches (appended with the code, before any counted cell)

**Caches.** The L_T games need nothing untracked beyond the numeric tables, which are cached after the first build in
`runs/forfeit_pricing/_cache/base_<game>_K10000.pkl` (untracked, never committed: pickles). The PD needs the untracked world-K caches
(`runs/provenance/{static, sets.npz, OSV.npy, SPO.npy, prod_exec.json}`, `runs/detectors/K/{static, sets.npz, OSV.npy, SPO.npy,
prod_exec.json, grudge.npz, sync}`): the main checkout has none, so they were copied (`cp -Rn`, read-only on the source side) from
the sibling worktree `.claude/worktrees/agent-a77da45eb47c729f4`; untracked, never committed (named files only are added);
pre- and post-run sha256 digests go to `runs/forfeit_pricing/provenance_hashes.json` (`forfeit_pricing_batch.py hashes pre|post`).

**Code layout (nothing existing edited).** `src/forfeit_pricing.py` (the exact simulators' terms, the instrumented engine
`LedgerEngineX` that classifies reads as capped or uncapped and flags tape reads inside an uncapped frame, the leaf event rule,
`TablesX`/`BaseX`: the merged catalogue extended by the exact twins and the sham twins, built once, cached),
`src/forfeit_pricing_run.py` (the three forfeit payoff conventions, arms, founders, views, the statistics of §1.4, the cell runner),
`src/forfeit_pricing_pd.py` (the PD run object with a read-only recorder of encounter steps), `src/forfeit_pricing_batch.py` (the
driver), `src/forfeit_pricing_static.py` (the nearby-budget check), `src/forfeit_pricing_report.py`, `tests/test_forfeit_pricing.py`
(29 tests).

**Definitions the spec left open.**
1. *Uncapped means within 16 steps of the root's fuel.* `LedgerEngineX` classifies a `run` as uncapped when its fuel k >= K - 16. The
   exact simulators use k = K - 11 (RPS) and K - 9 (inspection); every capped simulator of the catalogue has k <= 100. No program in the
   catalogue has a read with k in (100, K - 16).
2. *Under A the failure of an uncapped read is a free forfeit* (§1.7 flag 2). The merged `n_to` counts only capped timeouts; an uncapped
   timeout in a non-forfeiting leaf (impossible for the exact simulators) would be charged as a read timeout under every rule.
3. *The counterparts and the sham.* SIMX splits `SIM100u`; SIMX_I splits `SI100n`; SIMX_E splits `SE100k` (§1.2). The sham twins
   are `SIM100u~`, `SI100n~`, `SE100k~`: the same term with fuel 101 instead of 100. They agree with the counterparts in play law, capped
   timeouts and forfeits against every program of the merged catalogue *except the hash programmes* (`H*`, `HE*`, `HI*`), which key on
   the opponent's source and so see a different quote (a test asserts exactly this). "Behaviourally identical" therefore holds up to
   the hash programmes. The sham controls the template bookkeeping of the split, not the halving of the capped class (the X arm and the
   sham arm both halve the counterpart's founders); a control that isolates the halving would split the counterpart with an inert
   template, which would change the constants' or another family's mass and is not run.
4. *Founders.* The standard founders of the run index (the merged `draw_founders`, so the concurrent no-X cells are the merged
   pipeline's cells draw for draw) with an independent fair coin per founder of a counterpart (§1.2). The twin coin is the same in
   the X and sham arms.
5. *Dynamics labels.* A (no X): `A@P`, the merged label (so a no-X A cell on a stored run index reproduces the stored cell: tested on
   the confirmation run's runs 100 and 101); every other cell `<rule>@P` with `+X` or `+S`. Because the inspection catalogue has no
   forfeits, A, A_f and A_m cells without X share their tables there: the differences among them are dynamics-seed noise (a noise floor,
   E8).
6. *e_comp and the fallback statistics* as in §1.4; the classification uses the arm's own `e_gross`.
7. *The PD under A_f.* The model's forfeit would need all four reads of an encounter to hit their caps (steps 1,000,026 > 10^6, §1.1),
   so A_f runs the merged rule-A PD run object with a read-only recorder (`forfeit_pricing_pd.pop_steps`: the maximum steps of one
   side's play plus production over ordered pairs of present individuals, and the weight above 10^6, at every checkpoint). A test
   shows the recorder does not change the trajectory (draw for draw against the merged `pd_cell`, 60 generations). If any run
   recorded a forfeit weight > 0 it would be reported and the cell's reading changed; the PD rows carry `ffe`.
8. *PD freshness.* Reps 300-339 (kernel seeds rep*1,000,003 + 21,268,176 = 321,269,... to 360,270,...), disjoint from the stored 0-39
   and 200-239; a test recomputes them.
9. *Extra cells* beyond the spec's list (cheap, disclosed): a concurrent A cell at 10 (the confirmation run had it on other runs),
   A_m + X in RPS at every level, and in inspection A_m + X at 0.1 and 1 and A_m at 1 (the spec asks for A_m at 0.1 and 1 without X;
   A_m + X in inspection is an addition). Not run: an A_m sham.
10. *An equivalence.* A_m with SIMX equals a capped exact simulator with a coin default under A_f (the failed read is a charged
   timeout and the program plays a uniform tape): same charge, same game outcome up to the referee's draw versus the program's own
   tape. This follows from the definitions; it is not an extra cell.

**Static facts found while building the tables** (not in §1.3 because §1.3 could not derive them): SIMX against `PB` is a *mutual
forfeit* (PB's three `prove` calls exceed the root's fuel, and the read of PB dies with it), so SIMX's row against PB is the same
as against SIMX; the capped `SIM100u~` row is identical to `SIM100u`'s apart from the hash programmes. In inspection the merged
catalogue has no forfeits; `SIMX_I` forfeits only against `SIMX_E`, `SIMX_E` against `SIMX_I` and `RIM` (RIM's prover search exceeds
the fuel against SIMX_E), and `RIM` against `SIMX_E`; `SIMX_I` gets a finishing exact answer against every merged inspectee, a
private-tape inspectee (`Mc1`..`Mc7`) included (and then the simulated draw is not the actual play); `SIMX_E` finishes against every
merged inspector, the tape mixers `M*` and `CARR*` included. The table builds: RPS 202 s, inspection 395 s (the SIMX-SIMX regress costs
about 90 s per ordered pair per engine); mismatch against the stored engine 0 pairs in both games (the instrumented totals equal
`Engine.dist` exactly).

**Validation (before any counted cell).**
* `tests/test_forfeit_pricing.py` (29 tests, all passing; the PD test needs the world-K caches): leaf events (neither, forfeit,
  timed-out read, both, uncapped exhausting the root: one charge); hand-built plays against a looping opponent; the ledger equals
  the engine on hand pairs; SIMX on constants, a tape mixer and a looping reader (9 steps against a constant); exact boundary budgets
  (the read that just fits leaves exactly the response steps; one step more closes on TO and forfeits) for the three exact simulators;
  SIMX against SIMX at K = 200, 300, 1000; the clone; the §1.3 hand table at all five levels (every row, SIMX against SIMX and SIM
  against SIM); the forfeit payoff tables of §1.1 entry by entry (A, A_f, A_m) for RPS and inspection; fallback independence of the
  opponent's action; e_comp undefined with no completed plays; the founders (paired, split, same coin); **A_f without forfeits
  reproduces an A cell draw for draw** (RPS runs 300, 301; inspection run 300, also A_m); **the confirmation run's A 0.1 cell (runs
  100, 101) reproduced through the new pipeline exactly** (modal programmes at 2,000 and 4,000 and the statistics); the fresh-index
  guard; the PD recorder (not altering the trajectory, zero forfeit weight at 60 generations).
* Static check at nearby budgets (`forfeit_pricing_static.py`, K = 9,000, 10,000, 11,000), run with the counted cells.
