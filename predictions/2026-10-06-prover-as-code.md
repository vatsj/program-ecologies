# Predictions: the realizable language, milestone 3: the prover as code (2026-10-06)

Spec `specs/2026-10-06-prover-as-code.md` (reviewed by gpt-6.1-sol; the spec is the resolution where it and the
review differ). Committed after `notes/prover-as-code.md` §1 (commit f98a556) and before any code of this milestone,
any measurement, any counted cell and any performance-driven catalogue reduction. Nothing has been run; every
number below is a hand calculation from notes §1 or a guess labelled as such.

## Frozen design

1. **Language L_T^code** (notes §1.1): L_T without `prove`, `sprove`, `mk`, formula values; plus arithmetic
   `op(o, a, b)` (add, sub truncated, mul, div, mod, le, lt; one step), `capk(k, f, v)` → `sim(k, app(f, v))` (one
   step), the public library `lib(n)` (`app(lib n, v)` → body_n[0 := v], one step) and `libsrc(i)` (the quote of
   body_i, one step); eq by full encodings. Fuel rules of notes §1.2 (L_T's, unchanged).
2. **Search** `SEARCH_i = λarg. if eq(capk(U, lib CORE_i, arg), T) then T else F`, arg = (c, (ψ, U)), cost ≤ U + 7.
   CORE_0 sound, CORE_1 sloppy (SC_code), CORE_2 sound without JLöb^self (the control). Box ⊡^U_{c,i} ψ := the run of
   `capk(U, lib CORE_i, (c, (ψ, U)))` returns T.
3. **Calculus K_T^code** (notes §1.5): Ax; G3; EvR/EvL (exact and ⇓⁺ atoms, deterministic non-search steps);
   SrchR (static fit: global and every enclosing sim fuel ≥ U + 7; readings ⇓⁺ at the minimal residual); Run /
   RunNeg (computational, never on the root call); JLöb^self (hypothesis the root call's own box, conclusion the root
   or a deterministic downstream reduct). No SrchL, Nec, BoxEq (ii)/(iii), budget monotonicity, joint JLöb, cut.
4. **The core's algorithm** (frozen; the host prover implements the same, so the host is the oracle):
   - Closure by BFS from the root; successors: an atom at a deterministic step → its reading; an atom at a fitting
     search call → [B, ρ_T, ρ_F]; a non-fitting search call → none (CORE_1: treated as fitting); a box → none; ¬A →
     [A]; ∧, ∨, → → [left, right]. Formulas are interned in discovery order; L and R are kept sorted by it.
   - `ms(L, R, cap)`: cap < 1 → 1. Memo (exact value, or "fails at cap c", stored as c + 1). Otherwise one
     **expansion**: axioms (⊥ ∈ L, ⊤ ∈ R, a shared atom or box) → 1; Run on right boxes, RunNeg on left boxes (in
     order; each box's core run done once per core run and cached) → 1; then instances in order: left formulas
     (¬L, ∧L one premise; ∨L, →L two; EvL), right formulas (¬R, ∨R, →R one; ∧R two; EvR; SrchR two), and after each
     right formula its JLöb^self instance if eligible. One-premise instance at lim = min(cap, best − 1) − 1; two
     premises s₁ at lim − 2 then s₂ at lim − 1 − s₁ with lim = min(cap, best − 1) (milestone 1's order); JLöb^self
     = 1 + ms({H}, {ψ₀}, lim − 1).
   - Iterative deepening n = 1..c on ⊢ ψ with one memo per core run; returns T at the first n with a derivation,
     F after n = c. The core never returns a derivation to a program; an audit entry CORE_W returns the witness.
5. **SC_code (frozen sloppy checker):** CORE_1 = CORE_0's code with every side-condition predicate replaced by
   true: SrchR's fit test, Run/RunNeg's root exclusion and their runs (Run accepted on every right box, RunNeg on
   every left box, without running anything), and JLöb^self's eligibility (a JLöb leaf at every right formula other
   than ⊤/⊥, premise ⊡^U_{c,1} ψ₀ ⊢ that formula). Rule shapes (premise structure, sizes, the step function) are
   checked as in CORE_0. SC_code = `λme.λthem. if SEARCH_1(b, plays_K(them, me, C), U) then C else D`.
6. **Catalogue** at cell (K, b): U = ⌊K/4⌋, plays_K(x, y, a) = the exact atom ⟨x ⌜x⌝ ⌜y⌝, K⟩⇓a.
   C, D; FB = `if SEARCH_0(b, plays_K(them, me, C), U) then C else D`; FB1: query Con → plays_K(them, me, C),
   Con = ¬⊡^U_{b,0}⊥; PB: query 1 plays_K(them, me, C), then query 2 Con → plays_K(them, ⌜D⌝, D); G: FB with
   branches swapped; P\*: query 1 Con → plays_K(them, me, C), then query 2 plays_K(them, me, C) with D/C swapped;
   SF_k = `if eq(run(k, them, me), C) then C else D` with k = ⌊K/2⌋ in the main table; SC_code; Vlet (the query
   bound by a let); Vwrap (FB's body inside an identity application); **FB2** (searches the same query twice:
   `if S(q) then (if S(q) then C else D) else D`, the visibility probe); **FBx** (FB naming the fresh fuel K′ = 10K in
   its query, cap U = ⌊K/4⌋: the mismatched-target reader). Control: every SEARCH_0 replaced by SEARCH_2.
7. **Cells:** K ∈ {10⁵, 10⁶, 10⁷}, b ∈ {8, 12, 16, 24, 32, 64}, every ordered pair (play C / D / ⊥, each search's
   outcome: found / refuted / interrupted (core cap reached) / cut (an outer counter exhausted), steps); the FairBot
   grid {8, 12, 16, 32}² at each K; leak cells SF_k for k ∈ {10³, 10⁴, 10⁵, 10⁶} against every reader; fuel
   boundary cells; SC_code against G and FB; the control; per-cell coverage and the finite-K plateau.
8. **Scale guard:** FB's self-search total steps and candidate counts at b = 8 are reported first; if FB's self-search
   needs more than 10⁷ steps the catalogue is reduced to FB, SF, G, SC_code, C, D (the semantic tests stay on the
   full catalogue).

## RE predictions (verbatim from the spec, with falsifiers)

1. **The term prover is correct on every finishing query, and feasibility is set by candidate count, not witness
   length** (sol's point adopted): checking a supplied FairBot self-proof costs ≤ 10⁴ steps, but the search's
   candidate generation dominates, and the RE guesses the full FairBot self-search finishes within K = 10⁷ (the RE
   does not predict the constant). *Falsifier:* a correctness mismatch surviving debugging, a corrupted side
   condition accepted, or the FairBot self-search not finishing at K = 10⁷ (then the reduced catalogue runs and the
   result is reported as infeasible at this K).
2. **The leak closes exactly where the certified target matches the executed run:** no cell in which a sound reader
   cooperates with an SF that defects or times out *and* the reader's certified proposition names the fuel SF
   actually ran with; mismatched-target cells (the reader proved a statement about a fresh-K run) are reported
   separately as the residual leak, and the RE predicts the fuel-indexed atoms make them impossible by construction.
   *Falsifier:* a matched-target cell with the reader on the C side and SF not cooperating.
3. **No universal visibility theorem** [after review: sol's reading adopted]: the notes report whether K_T^code lets
   a reader certify a run longer than its own computation; the RE predicts that Löbian self-reference does (FairBot
   certifies its copy's run without unfolding it) while a simulation cannot be certified without unfolding it, so
   SF-type targets obey a fuel bound and prover-type targets do not. The cooperation region on the FairBot grid is
   symmetric; its shape (min-rule or not) is reported, not predicted. *Falsifier:* an asymmetric (C, D) cell with
   both searches finished.
4. **Soundness survives, with the obligations discharged** (§1; 0 checker violations on every returned derivation)
   **and bounded Gödel II transfers** (P\* never self-cooperates). *Falsifier:* an obligation that cannot be
   discharged, or P\* self-cooperating.
5. **The sloppy checker is a faker of G, not of sound readers** [after review]: SC_code cooperates with G while G
   defects on it; sound FB may correctly prove that SC_code cooperates (replay rejection of SC_code's own
   derivation does not force FB to defect), so FB–SC_code can be (C, C). *Falsifier:* G cooperating with SC_code, or
   FB exploited by SC_code (FB on the C side, SC_code defecting) with FB's search finished.

**Subagent's reading of RE 4 before the run:** notes §1.5 already records four K_T obligations that cannot be
discharged at the code level (Nec, BoxEq (ii)/(iii), budget monotonicity, joint JLöb), so RE 4's falsifier fires
by the notes alone; the run decides the rest of RE 4 (0 violations on returned derivations; P\* never
self-cooperating). RE 3's falsifier is about finished searches; the subagent expects the RE's dichotomy itself to
fail (notes §1.8) without the falsifier firing (S2, S5).

## Subagent predictions (with falsifiers)

- **S1 (thresholds by hand, notes §1.7).** On finishing searches the copy thresholds are b\* = 7 (FB), 8 (FB1,
  Vlet), 10 (PB, Vwrap, FB2), with one JLöb^self each; G and P\* never find; SC_code finds at b ≥ 6.
  *Falsifier:* a different b\* on a finishing search, or a twin derivation with more than one JLöb^self.
- **S2 (twins only).** No two distinct sound-reader sources mutually cooperate in any cell (FB–FB1, FB–PB, FB–Vlet,
  FB–Vwrap, FB–FB2, PB–FB1, …, and every off-diagonal FairBot grid cell); in each such pair at b ≥ b\* at least one
  search is interrupted by its cap (the Run regress of notes §1.7). The FairBot grid's cooperative region is the
  diagonal from b\* = 7 (where searches finish). *Falsifier:* any (C, C) between distinct sound-reader sources, or a
  refuted (finished) search in a distinct-source pair at b ≥ b\* where the hand argument predicts the regress.
- **S3 (costs; guesses).** FB's self-search at b = 8 costs between 10⁵ and 3·10⁶ evaluator steps; checking FB's
  supplied 7-node witness by the checker term costs between 2·10³ and 3·10⁴ steps; FB's search tries at most 5,000
  rule instances. *Falsifier:* any of the three outside its range.
- **S4 (feasibility in K; a guess).** FB self-cooperates at b = 8 at K = 10⁶ and 10⁷ (U ≥ 2.5·10⁵) and not at
  K = 10⁵ (U = 25,000, search interrupted). *Falsifier:* (C, C) at K = 10⁵, or no (C, C) at K = 10⁶.
- **S5 (static fuel boundary for simulators).** FB vs SF_k is (C, C) iff k ≥ U + 9 (and FB's search finishes), and
  (D, D) otherwise; the boundary cells k = U + 8 / U + 9 flip exactly there, not at the inner search's actual
  completion point (k ≈ W + 9 < U + 9, where SF's inner search would complete but no reader can certify it).
  *Falsifier:* a flip at any other k.
- **S6 (prudence and Gödel).** PB self-cooperates from b = 10 wherever its search and its two nested runs fit; PB vs
  D is (D, D); G–G is (C, C) by non-finding; P\* never self-cooperates; SF–SF is (D, D). *Falsifier:* any of these
  failing in a finishing cell.
- **S7 (control).** Under CORE_2 no twin, simulator or distinct-source cooperation remains; the remaining mutual
  cooperation is with C (by evaluation), with G (by non-finding) and with SC_code. *Falsifier:* a prover–prover or
  prover–SF (C, C) in the control.
- **S8 (correctness).** On every finishing query the term core and the host core agree in outcome, minimal size and
  number of expansions (the algorithms are the same); every returned derivation replays in the independent checker;
  every corrupted instance of notes §1.9 is rejected by the checker term and the host. *Falsifier:* any mismatch.
- **S9 (no mismatched leak in this catalogue).** No cell has FBx (or any reader naming K′ ≠ K) on the C side against
  a non-cooperating SF: the certified run at K′ and the executed run at K coincide for every catalogue target,
  because their length is dominated by search calls of cost ≤ U + 7 ≪ K. *Falsifier:* such a cell.
- **S10 (sloppy checker).** SC_code is exploited by G at every finishing b (SC C, G D); FB, FB1, Vlet, PB and SC_code
  are (C, C); SC_code defects against D. *Falsifier:* G cooperating with SC_code, a sound reader exploited by SC_code,
  or SC_code cooperating with D.

## Verdict rules

A prediction **holds** if no falsifier fires on the cells it names; **fails** if one fires (reported with the cell);
**not tested** if the cells could not be computed (e.g. infeasible at every tested K), which is itself reported.
Correctness (S8, RE 1) is judged on finishing queries only, with coverage reported. "Refuted" in any table means
"no derivation within size b in the candidate set", never semantic falsity.
