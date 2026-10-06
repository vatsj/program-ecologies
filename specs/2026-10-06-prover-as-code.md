# Spec: the realizable language, milestone 3: the prover as code, and the simulator leak, 2026-10-06

Status: reviewed by gpt-6.1-sol (`reviews/2026-10-06-prover-as-code-gpt-6.1-sol.md`) and revised; changes marked
[after review]. To be run by an Opus subagent. The RS's stated end state (2026-10-06, DEFERRED 11): programs run
their own proof search as code in the language, so the budget is the program's own step count and the checker's
source is visible. Milestone 1 made this urgent: the calculus describes the primitive-assisted idealization, and
under real charging a fuel-limited simulator exploits a sound reader's true proof about its idealized play (the
simulator leak). Milestone 2 (a population prior) waits on this. [after review] The experiment is gated on §1 of
the notes: every revised rule with its semantic obligation, stated before any counted cell; if a rule's obligation
cannot be discharged, that is reported as a failure, not repaired silently.

## Why

With `prove_b` as a primitive, two cost models disagree where it matters: the reader's proof is about the
opponent's *idealized* evaluation, while the opponent's *actual* run is fuel-limited and may time out inside a
simulated prove. A simulator SF_k that runs FairBot_b against itself for k steps times out before FairBot's inner
search completes, returns ⊥, defects, and is paid T by a reader that proved, correctly for the idealization, that SF
cooperates. With the prover as code there is one evaluator: proving is running the checker term, simulating a
prover means running its checker inside the simulation, and the proposition a reader proves is about an actual,
fuel-indexed run. Whether the leak closes is then a question about the calculus, not an external choice of cost
model.

## Definitions [after review: three budgets, fuel-indexed propositions]

- **b** — the derivation-size bound the search enumerates up to (`search_b` enumerates candidate derivations by
  size and stops at size b). **W** — search work: candidate generations and checks, reported separately. **K** —
  execution fuel: evaluator steps, consumed by every step including those inside `search` and inside `run`.
- **Fuel-indexed evaluation atom** `⟨σ, f⟩⇓a`: configuration σ with remaining fuel f reduces to the constructor a
  within f steps (⊥ if the fuel runs out). A program's play is `⟨p ⌜p⌝ ⌜q⌝, K⟩⇓·`. A nested simulation
  `run_k(⌜p⌝, ⌜q⌝)` evaluates `⟨p ⌜p⌝ ⌜q⌝, min(k, f_rem)⟩` where f_rem is the caller's remaining fuel, and its result
  (C, D or TO) is converted to an action by the caller's code; the fuel it consumes is charged to the caller. A
  proposition a reader proves names the fuel in the quoted target, so "SF cooperates" is `⟨SF ⌜SF⌝ ⌜r⌝, f⟩⇓C` for
  the f that the actual encounter supplies, not a fresh top-level allowance. The notes state the fuel-consumption
  rules for nested evaluation, search and timeout-to-action conversion.
- **Refuted** means "no derivation within size b exists in the candidate set", not semantic falsity.
- **Coverage** per cell: finished (found / refuted) vs interrupted (fuel exhausted during search), reported so that
  the difficult cases are visibly tested rather than censored; some nontrivial positive and negative queries must
  complete in every table.

## Design

**The prover as an L_T term.** A derivation **checker** `check : Deriv → Formula → Bool` for the code-level
calculus K_T^code (EvR/EvL by one evaluator step on the quoted fuel-indexed configuration, performed by running the
evaluator term; the prove-step rules replaced by the search term's actual return value as an evaluation step; BoxEq
along chains; Nec; JLöb with its side condition; no cut), and an **enumerator** `search_b` generating candidates
exactly as the host prover of milestone 1 does (same candidate set, so the host prover is the oracle for the
term's correctness on queries that finish). `prove_b(φ)` becomes `search_b(φ)` as an ordinary call. The **sloppy
checker** SC_code checks rule shapes but not side conditions (frozen in the predictions file).

**§1 of the notes, before any counted cell** [after review]: every rule of K_T^code with its semantic obligation
(what the rule asserts about fuel-indexed runs, and why it holds), with particular care for the replacements of
PrvR/PrvL, Nec and JLöb, whose obligations concerned the primitive's semantics and may now require bounded
reflection (a derivation that unfolds the opponent's search must account for the fuel that search consumes);
JLöb's budget conditions validated independently (hand-checked small instances with corrupted side conditions
rejected); the soundness theorem for fuel-indexed atoms by size induction, or the exact point where it fails. The
visibility question is posed, not assumed: *can a reader certify a run longer than its own proof-and-check
computation?* (Structural or Löbian reasoning can, in principle; the notes say whether K_T^code's rules allow it.)

**Correctness of the term prover.** On every query of milestone 1 (the named catalogue, b ≤ 64): outcome (found /
refuted / interrupted) and found size equal to the host prover's for every finishing query, with the **coverage**
of finishing queries reported per program and per budget; the independent replay checker validates every returned
derivation; **exhaustive small tests independent of the host prover** (hand-enumerated spaces at b ≤ 6; an
independently implemented evaluator); **corrupted-side-condition tests** (the checker must reject them).
**Benchmarks:** checking a supplied witness vs searching for it, per derivation node, with candidate counts; the
FairBot self-proof's total steps.

**Cells.** The named catalogue (FB, FB1, PB, G, P\*, SF_k, SC_code, Vlet, Vwrap, C, D), K ∈ {10⁵, 10⁶, 10⁷},
b ∈ {8, 12, 16, 24, 32, 64}: every ordered pair's play (C / D / ⊥), search outcome and coverage; self-cooperation
thresholds in b and in total steps; the FairBot distinct-budget grid {8, 12, 16, 32}²; **the leak cells**: SF_k
against every sound reader at k ∈ {10³, 10⁴, 10⁵, 10⁶}, recording the reader's certified target (the fuel-indexed
proposition it proved), SF's actual action, and whether the certified target matches the executed run; **fuel
boundary cells** [after review]: identical sources at different K and at nested residual fuel just across timeout
boundaries (k and f_rem one step below and above the search's completion); SC_code against G and FB; the
JLöb-disabled control; the K at which each cell stabilizes, labelled finite-K plateau, not stabilization.

**Scale guard** [after review: predictions frozen before any reduction]: report the FairBot self-proof's total
steps and the candidate count first; if it exceeds K = 10⁷, reduce the catalogue to FB, SF, G, SC_code, C, D and
keep the mandatory semantic tests (§1, correctness, corrupted side conditions) on the full catalogue. ≤ 3 workers.

## Required outputs

`src/lt_code.py`, `tests/test_lt_code.py`, `notes/prover-as-code.md` (§1 rules and obligations; §2 benchmarks and
costs), `runs/prover-as-code.md` and `.json`, a predictions file from the spec committed before any counted cell
(after the §1 notes), the usual hand-back (draft RESULTS, REJECTED, THEORY §9.2 and DEFERRED 2 and 11 edits,
NOTATION, ≤ 5 lines, branch from `git branch --show-current`, commits).

## RE predictions (with falsifiers) [after review]

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

The RS is invited to add predictions; the uncertain one is 3.
