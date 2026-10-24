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
