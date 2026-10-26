# What compute should cost: three pricing rules across three games (notes, 2026-10-25)

Spec `specs/2026-10-25-pricing-rules.md` (reviewed by gemini-4-argon, then gpt-6.1-sol in amended mode; both folded;
the RS's two statements are quoted at its top). Builds on `notes/lt-tape.md` (L_T with a private tape, the exact engine
`src/lt_tape.py`), `notes/rps-priced.md`, `notes/certificates-as-genes.md` (the PD encounter, `COSTS`),
`notes/provenance.md` and `notes/world-k.md`. §1 is written by hand before any code of this run and before any
counted cell: nothing in §1 has been run. Every number in §1 is derived on paper from the semantics of §1.0 (or
quoted from a stored note, with its source); the code is checked against it afterwards by `tests/test_pricing_rules.py`,
never the other way round. §2 (choices where the spec is silent, deviations, caches rebuilt) is appended with the code,
before any counted cell.

## 1. Hand derivations

### 1.0 Semantics used

**Evaluation (RPS, inspection).** As `notes/lt-tape.md` §1.0. A program is `λme.λthem. BODY`; the play of p against q
is the value of `p ⌜p⌝ ⌜q⌝`, so **every root evaluation starts with 2 β-steps** and a constant costs exactly 2. Every
contraction is one step; a tape read, an `eq`, an `if`, a `let` (one β) each cost 1. A root evaluation has fuel K; if
it is exhausted the play is a forfeit (as now, under every rule).

**Reads.** A *read call* is a nested evaluation the program starts and whose result it receives:
* `run k a b` (a **simulation**): one RUN step creates a frame with own fuel k that evaluates `a ⌜a⌝ ⌜b⌝` (the
  opponent playing against me); every step executed while the frame is open decrements the fuel of **every** enclosing
  frame, so an outer frame is exhausted first; when the inner value arrives, or the fuel reaches 0, one *closing step*
  replaces the frame by its value, or by `TO`. **The call's steps** are the RUN step, the steps executed while the
  frame is open, and the closing step: a call that times out on fuel costs exactly **k + 2** steps (1 + k + 1). A
  frame that is closed by a timeout of an enclosing frame never closes by itself and is not a separate timed-out call.
* `prove b φ`, `prp b x y a k`, `chk x y a k` (**primitive reads**): one multi-step charge W (search work, enumeration
  1 + Σ(1 + leaf steps), certificate check 1 + Σ(1 + prefix steps)). If W exceeds the remaining fuel of the innermost
  frame that cannot afford it, that frame times out and is charged its remaining fuel + 1 (a *partial-cap* timeout:
  the call has used the fuel it had left); if the culprit is the root's own fuel the play forfeits. `prp` past its own
  cap b returns F at charge b; I count this as a timed-out read as well (§2 states it; it is logged apart).
* A *timed-out call* is a simulation frame closed with `TO` (fuel, partial cap, or a stuck inner term), or a `prp` that
  hit its cap. Nested timed-out calls are counted each (A) and the topmost ones replace their subtrees (F+A).

**The four rules, for one root evaluation.** Let S be its steps, T the set of timed-out calls, T* ⊆ T those not nested
inside another timed-out call (topmost), s(t) the steps of call t including its nested calls, K the game's fuel cap of
a root evaluation.

| rule | charge |
|---|---|
| **F** (every step) | c · S |
| **A** (failure only) | P_fail · \|T\| (root steps and finishing reads are free; a forfeit is not charged beyond A's own events) |
| **F+A** (every step, failure at the cap) | c · ( S − Σ_{t ∈ T*} s(t) + K · \|T*\| ) |
| **B** (every step, amortized) | c · ( S − Σ over read calls whose key is cached at that moment, taken topmost, of their subtree steps ), then the keys of the calls that were executed are cached |

For B a read call's key is (the quote of the program whose code issues the call, the quote of the program read:
`a` in `run k a b`, the target in `prove/prp/chk`), both with the carried certificates; a cache hit makes the whole
call and everything inside it free (no deeper keys are inserted); a miss is paid at its **own** steps (the subtree
minus the subtrees of cached children) and inserted. The cache belongs to the island, is empty at the start, is never
shared across islands and dies with the island; a pre-warmed cache holds every key the catalogue can produce.

**PD (the realizable carrier lottery, world K, S-nonself).** Per encounter each side gets K = 10⁶ steps; a check is
capped at V = 250,000 and a production search at P = 250,000 (so a check or production cap timeout costs V + 6 =
250,006, `COSTS[5]` = 250,005). A unit's play is a decision tree of at most 2 atoms (`natoms` ∈ {0,1,2},
depth ≤ 2 for all 4,162 run trees), so a play evaluates 0–2 check calls plus O(10) steps. The stored kernel carries
outcomes (`A`, `CHC`, `CHD`, `UVt`) and the median production costs `COSTS` = (adoption check 19,499; gate 15,815;
gate on a listless target 101; produce-C 13,743; produce-D 9,058; cap timeout 250,005), but **no play-step table**.
The stored named-pair records (`runs/lt_genes/pairs.json.gz`, K = 10⁶) give play steps by pair, e.g. CB against itself
(same quote) 9,513, against a distinct CB1 23,372, against CBP 33,042, against a listless target (CBdef) 100, against
the constants Cc 2,415 and Dc 245. Prices act in the Moran fitness (a type's mean payoff against its island) through
per-pair charges; there is no individual-level cost history in this kernel.

### 1.1 Each game: K, stakes, timeouts

| game | K (root fuel) | payoff range ("stakes") | timeouts on the efficient path | what a timeout is |
|---|---|---|---|---|
| RPS (L_T, tape, r = 3, 30 programs) | 10,000 | 2 (±1) | none for the coin or constants; certain for a mutual simulation; the sim's k (20, 100) is the inner cap | a `run` frame closed on TO |
| inspection (L_T, tape, r = 2; 22 + 24 programs) | 10,000 | 5 (−4 … +1) | none for a checking inspectee against a certified mixer; certain for simulating inspectors against simulating inspectees | a `run` frame closed on TO; a `prp` past its cap |
| PD (carrier lottery, K world, S-nonself) | 10⁶ per encounter | 3 (−2 … +1) | rare in plays (132 of 31,510 stored named-pair encounters); production cap timeouts for units whose tactic does not finish | a check or production act that reaches its cap and returns TO |

Prices are reported raw and normalized: c·K is the cost of exhausting the root fuel; c·K / range is that cost in stakes.
At c = 10⁻³: RPS c·K = 10 (5 stakes), inspection 10 (2 stakes), PD 1,000 (333 stakes). At c = 10⁻⁴: 1 (0.5), 1
(0.2), 100 (33). At c = 10⁻⁵: 0.1, 0.1, 10 (3.3). **The fuel caps differ by a factor of 100, so one numeric c means
very different things in the L_T games and the PD.** P_fail is the same number in every game by construction, and is
read against the stakes directly (P_fail = 1 is half an RPS range, 20% of the inspection range, a third of the PD
range).

### 1.2 Hand table of charges (steps S; charges as multiples of c, or P_fail)

*RPS.* Constants: 2 steps. `U` (`if eq(tape 0,0) then R else if eq(tape 0,1) then P else S`): digit 0: tape, eq, if →
2 + 3 = 5; digits 1, 2: 2 + 6 = 8; expected (5 + 8 + 8)/3 = 7. `SIMkd` = `let v = run k them me in beat(v, default d)`,
beat = eq/if ladder: 3 eq + 3 if = 6 steps on TO; on R: eq, if = 2; the let is 1 β.

| row | encounter | S | read calls (steps incl. RUN and closing) | timed-out | F | A | F+A | B first / B repeat |
|---|---|---|---|---|---|---|---|---|
| 1 | `R0` against anything | 2 | – | 0 | 2c | 0 | 2c | 2c / 2c |
| 2 | `U` against anything | 7 (E) | – | 0 | 7c | 0 | 7c | 7c / 7c |
| 3 | `SIM100R` vs `R0` (a read that finishes) | 9 | call 1: 1 + 2 + 1 = 4 | 0 | 9c | 0 | 9c | 9c / 5c |
| 4 | `SIM100R` vs `SIM100R` (mutual, the root's call times out) | 111 | call 1: 1 + 100 + 1 = 102; the inner frames die with it | 1 | 111c | P | (9 + K)c | 111c / 9c |
| 5 | `SIM20R` vs `SIM100R` (k = 20 side) | 31 | call 1: 22 (k + 2) | 1 | 31c | P | (9 + K)c | 31c / 9c |
| 6 | `SIM100R` vs `SIM20R` (inner call times out, outer handles it and finishes) | 38 | call 1: 33 (finishes with value R; inside it: RUN 1, 2 β, call 2 = 22 (TO), let, 6 beat steps, closing); call 2: 22, TO | 1 (call 2 only) | 38c | P | (38 − 22 + K)c = (16 + K)c | 38c − (cached part) / 5c |
| 7 | `SIM20R` vs `PB` (partial cap, **conditional**: the prover's W for "SIM20R plays R" exceeds the 17 steps of fuel left after 2 β and the `mk`) | 31 (2 + 22 + 1 + 6) | call 1 = k + 2 = 22 (3 inside + 18 charged as remaining fuel + 1) | 1 | 31c | P | (9 + K)c | 31c / 9c |

Row 6 detail: root 2 β + call 1 (33) + let β (1) + beat on R (2) = 38. B keys: call 1 is (SIM100R, SIM20R), call 2 is
(SIM20R, SIM100R) — the same key as row 5's call 1, so after row 5 has been played call 2 is cached and the first
execution of row 6 pays 38 − 22 = 16c, and the repeat pays the root's 5c. The F+A charge for row 7 is the same as row 5's
because the timed-out call has the same k + 2 steps; whether W > 17 for this pair is checked by the code, not derived.

*Inspection* (r = 2, m = 3; `notes/lt-tape.md` §1.2). The compliance check `CR3` = `if chk(them, me, I, 3) then C else K`;
`CARR3` carries the I-certificate of `M{3}` with prefixes (0,0) and (0,1,0).

| row | encounter (inspectee first) | S | primitive reads | timed-out | F | A | F+A | B first / B repeat |
|---|---|---|---|---|---|---|---|---|
| 8 | `CR3` vs `CARR3` (a successful check) | 27 | check: 1 + (1 + 9) + (1 + 12) = 24, replay of (0,0) is 3 + 6 = 9 steps, of (0,1,0) is 3 + 9 = 12 | 0 | 27c | 0 | 27c | 27c / 3c |
| 9 | `CR3` vs `M3` (not a carrier: rejected at once) | 4 | check: 1 | 0 | 4c | 0 | 4c | 4c / 3c |
| 10 | `PR3` vs `M3` (enumeration of 4 leaves: depths 2, 3, 3, 1 → 8, 11, 11, 5) | 43 | prp: 1 + 9 + 12 + 12 + 6 = 40 | 0 | 43c | 0 | 43c | 43c / 3c |
| 11 | `SI100n` vs `SE100k` (mutual simulation) | 106 | call 1: 102 (TO) | 1 | 106c | P | (4 + K)c | 106c / 4c |
| 12 | `SI100n` vs `K0` (finishing read) | 8 | call 1: 1 + 2 + 1 = 4 | 0 | 8c | 0 | 8c | 8c / 4c |

(`CARR3` as a play: carrier β + 3 + 3·depth steps per leaf, mean 7.25 as in `notes/lt-tape.md`; the 3 B-repeat steps of
rows 8–10 are 2 β + the `if`.) Rows 8 and 10 reproduce the stored 27 and 43. A *repeated* check of the same partner is
the B-repeat column: the root pays only 3 steps. Under F the repeat costs the same 27c.

*PD* (from the stored costs; the play-step model is a disclosed approximation, §2):

| row | encounter | S | read calls | timed-out | F | A | F+A | B first / B repeat |
|---|---|---|---|---|---|---|---|---|
| 13 | FairBot `if(CHK(them,me,C),C,D)` vs a distinct carrier, check true | ≈ 10 + 15,815 | one check | 0 | ≈ 1.6·10⁴ c | 0 | same | same / 10c |
| 14 | the same program against its own quote | ≈ 10 + 9,513 | one self check | 0 | ≈ 9.5·10³ c | 0 | same | same / 10c |
| 15 | FairBot vs a listless target (no entry) | ≈ 10 + 101 | one check, rejected at once | 0 | ≈ 111 c | 0 | same | same / 10c |
| 16 | a check that reaches its cap (TO) | ≈ 10 + 250,006 | one check | 1 | ≈ 2.5·10⁵ c | P | (10 + K)c = 1.00001·10⁶ c | same / 10c |
| 17 | a lacking S-nonself producer, C then D act, both finishing | 13,743 + 9,058 | two production acts | 0 | 22,801 c | 0 | same | first only, free thereafter in the type-level kernel |
| 18 | a producer whose C act hits the cap | 250,005 + 9,058 | two acts | 1 | 259,063 c | P | (K + 9,058)c | as row 17 |

Reading the PD rows: at c = 10⁻³ a single distinct-pair check costs 16 against stakes of 3; at 10⁻⁴ it costs 1.6; at
10⁻⁵ it costs 0.16. So F cannot keep a source-reading PD (a certified cooperation costs more than it earns) above
about c = 10⁻⁵, while the RPS coin needs c ≥ 10⁻³ (stored dose: U holds 0.91 at 10⁻³, 0.09 at 10⁻⁴): the bands of F
do not overlap, **by arithmetic**, if the stored RPS dose and this PD cost model are right; the experiment tests the
other rules, and whether F's RPS and PD bands meet under the lottery rather than the arithmetic.

### 1.3 The audit: do the stored records suffice?

* **RPS and inspection.** The stored cells (`runs/lt_tape/*.json.gz`) hold island-mean statistics; the exact engine's
  `Engine.dist` returns, per pair, the action distribution, the expected steps, a route split and the forfeit
  probability. It does not record read calls, their nesting, which are timed out, or their keys. F is computable from
  the stored tables; **A, F+A and B are not**: they need the nested-call forest of every leaf of the decision tree. A
  fresh instrumented engine records, per leaf: steps, the forest of read calls (kind, key, own and subtree steps,
  timed-out or not) and the forfeit flag. Its totals must reproduce the stored `dist` and `steps` exactly (a test).
* **PD.** The stored kernel and tables have no play-step table and no per-play timeout record; the production steps
  are a median cost model (`COSTS`) and are counted, not priced, in the stored runs. Production, retries and checks are
  priced like any other steps (§2: no exemption). The play-step model of §2 uses the stored decision trees, the
  stored check outcomes, and call-cost medians calibrated on the named-pair records.
* **No stored record** prices a read by its outcome, caches across encounters, or charges anything at the cap.

## 2. Choices where the spec is silent, deviations, caches (appended with the code, before any counted cell)

**Caches.** The L_T games need nothing untracked. The PD needs the untracked world-K caches (`runs/provenance/{static,
sets.npz, OSV.npy, SPO.npy, prod_exec.json}`, `runs/detectors/K/{static, sets.npz, OSV.npy, SPO.npy, prod_exec.json,
grudge.npz, sync}`, 1.7 GB). They were **copied, not rebuilt**, from a sibling worktree (read-only on its side); the
copies are untracked and never committed (explicit `git add` of named files only). The tracked JSON in those directories
was already in this checkout.

**Code layout (nothing under `src/` or `tests/` edited).**
`src/pricing_rules.py` (instrumented ledger engine: a copy of `lt_tape.Engine.explore` that records the forest of read calls;
`LedgerEngine.ledger`), `src/pricing_rules_lt.py` (RPS and inspection: statics, priced views, exact-kernel lotteries, records),
`src/pricing_rules_kern.py` (sampled-encounter lotteries with island ledgers), `src/pricing_rules_pd_model.py` (the PD
play-step model and priced payoff), `src/pricing_rules_pdkern.py` (a generated copy of `provenance._change`,
`provenance.init_paysum` and `annealed_kern.segment_ann` with `pay` replaced by `pay_net`; no other change),
`src/pricing_rules_pd.py` (PD run object and driver), `src/pricing_rules_pd_validate.py` (calibration and validation of the
model against executable plays), `src/pricing_rules_batch.py`, `src/pricing_rules_report.py`.

**Definitions the spec left open.**
1. *What counts as a timed-out read.* A `run` frame closed on `TO` (fuel, partial cap, or a stuck inner term; the stuck case
   is counted and logged apart, expected 0), and a `prp` that hits its enumeration cap b (returns F at charge b; logged
   apart as `cap`). A root evaluation that exceeds K forfeits as now and pays no extra under A. Primitive `prove` and `chk`
   that exceed a *sim's* fuel time that sim out (a partial-cap timeout, charged its remaining fuel + 1 = the call's k + 2).
   `hq` is an ordinary step, not a read.
2. *F+A's K* is the game's root fuel (10⁴ in RPS and inspection, 10⁶ per encounter in the PD), also for a `prp` cap hit that
   used only b = 400 steps (the spec: "charged c·K in place of its own steps").
3. *Call keys (B).* Issuer = the program whose code issues the call (the root program, or the program running inside the
   enclosing frame), read = the program simulated (`run`), or the target and parameters (`prove`, `prp`, `chk`); programs
   include their carried certificates (they are terms). A key hit makes the call and its subtree free and inserts nothing
   below it; a miss is charged the call's own steps (its subtree minus its nested calls' subtrees) and inserted.
4. *B cold* is run in a sampled-encounter kernel with a real ledger per island (empty at the start, island-bound, shared by
   both roles); *B warm* (the pre-warmed cache, `Bw`) is the steady-state table charge c · (root steps outside every read call)
   in the exact kernel. B cold uses 10 encounters per individual per generation and stops at generation 2,000. Because the
   kernel differs from the stored one, the matched bridges `Zs` (zero price) and `Fs` (F) go through the same sampled kernel
   at the panel levels, and B is read against them. Rejection sampling of the parent (exact, against a running upper bound).
5. *Controls.* The timeout-free bounded simulator is the zero price (a read that returns a default after a small fixed
   budget without being a charged timeout is an uncharged read): the zero-price cells are that control. The per-read toll τ
   charges every read call (finishing or not) a constant τ: τ ∈ {0.1, 1}, exact kernel in RPS and inspection, type level in the
   PD (calls = atoms evaluated plus production acts).
6. *Seeds.* Founders as the stored cells (paired across rules). Dynamics seeds are the stored formula with the price label:
   `'%g' % c` for F and Z (so F and Z reproduce the stored cells draw for draw: tested on four stored cells), `rule@level` for
   the other rules.
7. *Targets* as in the predictions file. The RPS statistic is `e_prog` (net of the rule's charge; for rule B cold the net
   uses the warm-cache charge table); the inspection statistic is the fraction of efficient islands at 2,000; the PD statistic
   is `universal_open` at the run's end (generation 10,000 or the frozen stop).
8. *Larger geometry.* RPS and inspection (N, I) = (400, 16), 20 runs, the stored `size` cell; PD (200, 64), 20 runs.

**The PD play-step model (a disclosed approximation, not a stored record).** The stored kernel has no play-step table, so
each play is priced by the decision-tree evaluator of `pricing_rules_pd_model.py`: the atoms on the evaluated path, each
charged by its class. The action it computes equals the stored action table on 200,000 random distinct pairs and the
self-play table on 5,000 units (0 mismatches; a test). The class costs were fitted by non-negative least squares on 30,000
executed plays (`lt_genes.play_side` at K = 10⁶, units drawn from the types of three zero-price lotteries advanced 300
generations; the nolist check fixed at 101 and the root's steps at 4; TO fixed at 250,006). Fitted class costs (steps):

| nolist | dist T | dist F | same T | same F | self T | self F | vsC T | vsC F | vsD T | vsD F | TO | root |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 101 | 18,843 | 25,865 | 18,304 | 21,523 | 17,616 | 15,767 | 13,277 | 12,739 | 12,955 | 13,672 | 250,006 | 4 |

Held-out error (8,000 plays): mean predicted 9,439 against executed 9,364; median ratio executed/predicted 0.95; q10–q90
0.63–3.9; 75% within a factor 2 (the first, median-based model: mean 5,258, 58% within a factor 2). The model's action
disagrees with the executable evaluator on 1.5% of plays (⊥ and timeouts of the executable play). Production acts use the
stored medians (`COSTS`): produce-C 13,743, produce-D 9,058, cap 250,005. The charges act on the Moran fitness at the type
level: a type's payoff against a partner is the stored pair payoff minus the rule's charge of that ordered pair (play plus
S-nonself production); the production charge is paid every encounter by a type that lacks an entry (futile retries
included), as in the stored cost accounting. Rule B in the type-level kernel charges only the root's 4 steps per play: a
read or production act is amortized to zero in steady state, and the first-execution charges (one per key per island) are not
representable in a kernel whose fitness has no individual history; their size is bounded in the report by the number of
distinct keys times their cost against the payoff mass of a generation. Nothing else in the PD differs from the stored
cell: founders, r = 100, w = 0.3, mN = 1, the frozen stop and the statistics. Zero price returns `PV.pay` exactly (draw for
draw with the stored run: a test on a 400-generation run).

**Statics.** `src/pricing_rules_report.py` computes, from the instrumented tables, the grid c ∈ [10⁻⁶, 10⁻¹] and P_fail ∈
[10⁻³, 10²] (8 points per decade): RPS, which programs invade a monomorphic `U` population (net) and the largest invasion
gain; inspection, the fraction of efficient resident pairs (both roles' game payoff ≥ −0.05) that no single mutant of either
role invades.

**Cuts and disclosures** are listed in the report. Measured costs: a PD run is about 0.5 minutes when it freezes early and
about 3.5 minutes at 10,000 generations when it does not (0.9 GB resident); an RPS or inspection exact-kernel run takes seconds,
a sampled run about 8 seconds (0.12 GB). At most 2 worker processes were used while any other agent's process was alive.

### 2.1 Additions made during the run (disclosed; none changes a registered threshold)

**A stale numba cache priced the first PD batch wrongly; it was discarded.** The generated PD kernel and the model functions were
compiled with `cache=True`; after the model's class table was restructured, a dependent kernel's cached compile read the old
index layout, so the first batch of priced PD cells (everything except the zero price) used wrong class costs (a TO charged
17,616 steps, the root's steps charged 15,767). They were noticed because B's end-state charge per play was not c times the root
steps. All priced PD cells from that batch were discarded (kept out of the report) and rerun after the dependents and the model
functions were set to `cache=False`. A test now runs a priced PD job through the run object and checks the end-state charge
against the rule's form, and the report carries an audit of every PD cell's recorded charge against its form (all ok). Two cells
(`A 0.1`, `B 0.01`) of the rerun batch had a ledger inconsistent with their rule (an F-like charge in the end-state statistic;
their dynamics looked unaffected) and were rerun after the model went uncached; the rerun values replace them. Intermittent
crashes of PD processes (exit -11 or -6, early, with an empty log) were retried by the driver, at most twice; no cell was
dropped.

**B-own and the logging kernel (the addendum).** `Bo` (a per-program memo) and `Bl` (the island ledger of B run through the
kernel that logs sizes and payments; draw for draw with `B`, a test) are in the sampled kernel for RPS and inspection (a bit-row
per individual, empty for founders, copied to offspring and carried by migrants; certificates are fixed in the carriers, so no
payment is caused by a certificate update, 0 by construction). In the PD the memo is per (island, lineage, type), the island
ledger `Bi` per island; both are individual-level: payments are made at generation boundaries by groups that have not paid for a
partner quote present on their island, the type-level fitness of the stored kernel becomes individual-level for these rules, and
parents are drawn individual by individual (rejection against the island's best type fitness). A migrant child copies its old
group's memo entries for the partner types present on the new island. A type change by production is a new reader quote and
starts a cold memo. PD `B` (type-level steady state: reads amortized to zero) is kept beside `Bi`, which is the like-for-like
partner of `Bo`. `Bow` starts each founder lineage with every present partner quote already cached (the pre-warmed memo).

**Supplementary runs.** The registered intervals left some cells undetermined at 20 PD runs (and RPS A at 10 at 40 runs). New run
indices were added in files tagged `_ext` (PD reps 20–39; RPS reps 40–79) for the PD zero price, F at 10⁻³, A at 0.1, 1 and 10,
and RPS A at 10; the report pools them with the registered runs under the same scoring rule and labels the result
supplementary. The registered cells are untouched. Wall times of some `_ext` cells in the batch log include hours in which the
host was asleep.

**Larger geometry** was run for the only level that met all three targets on pooled runs (A at 0.1) and for the zero price:
RPS and inspection (400, 16), 20 runs; PD (200, 64), 20 runs.

**No `multiprocessing.Pool` was used** (one process per cell; the stored `world_k_run.py` pool driver was not called).
