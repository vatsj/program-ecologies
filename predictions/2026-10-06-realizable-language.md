# Predictions: the realizable language L_T, milestone 1 (bounded-proof FairBot in a λ-calculus), 2026-10-06

Spec: `specs/2026-10-06-realizable-language.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-06-realizable-language-gpt-6.1-sol.md`,
and revised; where they differ the spec is the resolution). Committed before any code, notes, table or search. Nothing
has been computed; every number below is a hand calculation from the design fixed in this file.

## Design choices fixed before the run

1. **Terms** (de Bruijn, Python tuples; `src/lt.py` must reproduce the named terms below exactly, tested):
   `('v', i)` variable; `('lam', t)`; `('app', f, a)`; `('con', n)` with n ∈ {C, D, T, F, TO}; `('nat', n)`;
   `('pair', a, b)`, `('fst', a)`, `('snd', a)`; `('if', c, t, e)` (lazy branches, dispatch on T/F);
   `('fix', t)` (t under one binder for the recursive self; `('app', ('fix', t), v)` → `('app', t[0 := ('fix', t)], v)`,
   one step); `('quote', t)` a quoted closed term, a value, opaque to substitution, behaving under fst/snd as its
   nested-pair de Bruijn encoding (tag, payload); `('eq', a, b)` structural equality of values (quotes compared by
   encoding) → T/F; formula builders `('mk', k, …)` with k ∈ {plays, not, and, or, imp, box, bot, top}
   (`('mk','plays', x, y, a)` needs quotes x, y and a ∈ {C, D}; `('mk','box', n, f)`); `('prove', n, f)`;
   `('sprove', n, f)` (the sloppy checker's primitive); `('run', k, x, y)` → `('sim', k, x̂ x y)` in one step, where
   x̂ is the term x quotes. Runtime-only forms: `('sim', k, t)` and formula values.
2. **Evaluator.** Call-by-value, left to right, small-step substitution on closed terms; one step per contraction
   (β, fix, if, fst/snd, mk, eq, run, sim return/timeout, sprove, prove). `sim(k, t)`: if t is a value it returns t
   (one step); else if k = 0 or t is stuck it returns TO (one step); else one inner step is one outer step and
   gives `sim(k − 1, t′)`. Nested sims are charged at every level. A play is `eval_K(p ⌜p⌝ ⌜q⌝)`: C, D, or ⊥
   (K exhausted, or a non-C/D value, or stuck); ⊥ pays as D. `sprove(n, f)` returns T in one step for n ≥ 1 (see 6).
3. **Charging.** *Primitive-assisted:* `prove` costs one step and returns found/not-found exactly (host search).
   *Search-charged:* `prove_b(ψ)` costs W(ψ, b), the number of node expansions of the frozen iterative-deepening
   search (§ 5), charged to the global K and to every enclosing sim fuel; if W exceeds the smallest remaining
   counter, the outermost exhausted frame times out (the global frame: the play is ⊥ and the prove outcome is
   **timeout**; a sim frame: that sim returns TO). A timed-out prove never branches: the program has no steps left.
   K ∈ {10⁴, 10⁵, 10⁶}.
4. **K_T and its standard model.** Atoms ⟨σ⟩⇓a (σ a non-terminal machine state, a ∈ {C, D});
   plays(⌜p⌝, ⌜q⌝, a) := ⟨p ⌜p⌝ ⌜q⌝⟩⇓a. Terminal states are read as ⊤ (the value a) or ⊥ (any other value, TO,
   stuck). Truth in T: □_c ψ iff K_T derives ⊢ ψ within c sequents; ⟨σ⟩⇓a iff the **idealized** evaluation of σ
   (primitive-assisted, no global step bound, sim fuels counted, prove answered by box truth) reaches a. Rules:
   G3 propositional; EvR/EvL (one deterministic step, +1); PrvR/PrvL at a prove state (two premises, branch on
   □_c ψ with the after-step states); Ax on atoms and boxes; BoxEq: □_a A ⊢ □_c B for A = B or A, B atoms on one
   deterministic chain (a ≤ c if B is downstream of A; a + k ≤ c if B is k steps upstream); Nec(c); JLöb(S, m),
   1 ≤ |S| ≤ 3, premises exactly □_m S ⊢ A_j, side condition m ≥ 1 + Σ s_j, conclusion a member or a deterministic
   downstream reduct of a member; members drawn from the root's reachable box contents and their deterministic
   chains. No cut. The **JLöb-disabled control** is K_T without JLöb.
5. **The search** (frozen): `minsize(seq, cap)` over all rule instances (no normal-form prune), memoized on the
   sequent with exact values and lower bounds, called by iterative deepening n = 1, 2, …, b on ⊢ ψ with one fresh memo
   per prove call. W = number of expansions (memo misses). Found at the first n with a derivation; refuted when
   n = b completes without one. Minimal sizes are certified because every lower n completed exhaustively.
6. **SC's candidate generator** (frozen). Candidates are labelled sequent trees enumerated by iterative deepening on
   size; SC accepts the first candidate whose end sequent is ⊢ ψ without checking rule applications. The first such
   candidate is the one-node tree, so `sprove_b(ψ)` returns found for every ψ at every b ≥ 1, at cost 1 node: SC_b is
   extensionally CooperateBot with a prove-shaped source. (This is the literal reading of the spec; a checker that
   checks rule shapes but not side conditions is a different program and is not in this milestone.)
7. **Harmless variants.** Under de Bruijn syntax a renamed λ-variable spelling is the same term as FairBot_b (a copy
   by construction); it is reported as such and replaced by a **let variant** with a distinct source. The wrapper is
   as in the spec.
8. **Grids.** b ∈ {2, …, 64}; SF_k with k = b in the pairwise tables plus a k sweep {5, 10, 20, 64, 200, 10³}; FairBot
   copy/distinct grid {4, 8, 16, 32}²; both charging semantics; K ∈ {10⁴, 10⁵, 10⁶}.

## Frozen named programs (exact terms)

Abbreviations: ME = `('v', 1)`, THEM = `('v', 0)` inside `λme. λthem.`; B = `('nat', b)`; `C`, `D`, `T`, `F` are
`('con', ·)`; `PL(x, y, a)` = `('mk', 'plays', x, y, a)`; `CON_b` = `('mk', 'not', ('mk', 'box', B, ('mk', 'bot')))`.

| name | term |
|---|---|
| C | `('lam', ('lam', C))` |
| D | `('lam', ('lam', D))` |
| FairBot_b (FB_b) | `('lam', ('lam', ('if', ('prove', B, PL(THEM, ME, C)), C, D)))` |
| FairBot1_b (FB1_b) | `('lam', ('lam', ('if', ('prove', B, ('mk', 'imp', CON_b, PL(THEM, ME, C))), C, D)))` |
| PrudentBot_b (PB_b) | `('lam', ('lam', ('if', ('prove', B, PL(THEM, ME, C)), ('if', ('prove', B, ('mk', 'imp', CON_b, PL(THEM, ('quote', D), D))), C, D), D)))` |
| G_b | `('lam', ('lam', ('if', ('prove', B, PL(THEM, ME, C)), D, C)))` |
| P\*_b | `('lam', ('lam', ('if', ('prove', B, ('mk', 'imp', CON_b, PL(THEM, ME, C))), ('if', ('prove', B, PL(THEM, ME, C)), D, C), D)))` |
| SF_k | `('lam', ('lam', ('if', ('eq', ('run', ('nat', k), THEM, ME), C), C, D)))` |
| SC_b | `('lam', ('lam', ('if', ('sprove', B, PL(THEM, ME, C)), C, D)))` |
| Vlet_b | `('lam', ('lam', ('app', ('lam', ('if', ('prove', B, ('v', 0)), C, D)), PL(THEM, ME, C))))` |
| Vwrap_b | `('lam', ('lam', ('app', ('lam', ('v', 0)), ('app', ('app', FB_b, ME), THEM))))` |

The ∧ of PrudentBot and P\* is short-circuit (nested if). The catalogue at budget b is these eleven plus the
quoted sources they mention (only D, inside PB_b).

## RE predictions (verbatim from the spec)

1. **K_T is sound and the witness is executable** (§1 proved; 0 checker violations; for every found box the
   search-charged arm finds it within K = 10⁶), **and FairBot_b cooperates with itself from a finite threshold** in
   the primitive-assisted arm with Λ = 1. The RE guesses b\* ≤ 64 but does not predict its value (representation-
   dependent, as sol says). *Falsifier:* a soundness gap, a found box the search-charged arm cannot find at any
   tested K, or no self-cooperation at any b ≤ 64 (reported as "threshold above the grid", with the certified
   lower bound).
2. **Budget structure:** no (C, D) cell on the FairBot grid under completed searches (soundness forbids
   exploitation), copies cooperate from a budget no higher than distinct budgets, and the RE guesses the distinct-
   budget condition is a threshold on min(b_x, b_y) but allows that source length enters. *Falsifier:* a (C, D) cell
   with both searches completed, or distinct budgets cooperating strictly below the copy threshold.
3. **The Gödel-sentence program is suckered, not disarmed** [after review: corrected]: FairBot_b defects on G_b
   (no derivation of G's cooperation exists, so the search refutes) and G_b then cooperates; FairBot1_b likewise;
   G_b's victim, if any, is a level-1 self-cooperation reader as in the modal arm. **The simulation FairBot pair
   mutually defects or times out at every k**, and **P\*_b never self-cooperates** (bounded Gödel II transfers).
   *Falsifier:* FairBot_b cooperating with G_b under a completed search, or P\*_b self-cooperating.
4. **PrudentBot_b self-cooperates at a finite threshold with Λ ≤ 5**, at most 8× FairBot's (K: 11 against 4).
   *Falsifier:* no self-cooperation at b ≤ 64 while FairBot's threshold is ≤ 16, or a threshold > 8× FairBot's.
5. **The sloppy checker is exploited by G_b** (SC cooperates while G defects) **and sound FairBot_b may defect on it
   while it cooperates** (sol's point: SC can cooperate before FairBot can certify it). **The JLöb-disabled control
   shows no cooperation between any two conditional programs**, and **the harmless variants cooperate with FairBot_b
   at FairBot's own threshold within +4** (cooperation is not copy recognition). *Falsifier:* SC not exploited by G,
   cooperation in the JLöb-disabled control, or a harmless variant needing > 2× FairBot's threshold.

Operationalization (fixed now): "FairBot's own threshold" = b\*(FB) (the copy threshold); "conditional programs" =
every catalogue program other than C and D; RE 5's control clause is scored literally, and a cooperation cell in the
control whose proof uses no JLöb and whose opponent is extensionally constant (SC) is reported separately.

## Subagent predictions (hand calculations under the design above)

Step counts used: FB reaches its prove state in 3 steps (β, β, mk), FB1 and G-like guards in 7 (β, β, five mk),
Vlet in 4, Vwrap in 5, SF's inner prove in 6 (β, β, run, then three sim steps); the cooperative branch costs 2
sequents (EvR to the value, ⊤), 3 for Vwrap, 5 for SF (if, sim return, eq, if, ⊤).

- **S1 (FairBot copies).** b\*(FB) = 8 (primitive-assisted), Λ = 1; certified minimal size of ⊢ plays(FB_8, FB_8, C) = 8.
  *Falsifier:* b\*(FB) ≠ 8, or Λ ≠ 1.
- **S2 (distinct budgets).** FB_x vs FB_y with x ≠ y cooperate iff min(x, y) ≥ 12 (joint JLöb over the two prove-state
  atoms, instance 9, BoxEq + 3), symmetric in every cell; on {4, 8, 16, 32}²: C on (8, 8), (16, ·≥16), (32, 32);
  D elsewhere. *Falsifier:* any off-diagonal cell violating min ≥ 12, or an asymmetric cell.
- **S3 (guards and prudence).** b\*(FB1) = 13; b\*(PB) = 25 ± 3 with Λ = 1 (the Con conjunct is closed by Nec on a
  9-sequent derivation using BoxEq into ⊥, no Löb); ratio b\*(PB)/b\*(FB) ∈ [2.5, 4]. *Falsifier:* b\*(FB1) ≠ 13,
  b\*(PB) outside [22, 28], or Λ(PB) ≠ 1.
- **S4 (Gödel and P\*).** G_b plays C against FB, FB1, PB, P\*, G and SF (no catalogue reader proves G's cooperation),
  and D against SC from b = 6 (plays(SC, G, C) has a 6-sequent evaluation proof) and against C from b = 3. P\*_b plays
  D against every catalogue program at every b. *Falsifier:* any deviation.
- **S5 (simulation).** SF_k vs SF_k is (D, D) with no global timeout at every k in the sweep (each nesting level is
  charged; the outer fuel runs out first). SF_k vs FB_b is mutual cooperation under primitive-assisted iff b ≥ 14 and
  k ≥ 5. Under search-charged, SF_k with k ≤ 10³ cannot afford FB's inner search (W > k), so the sim times out and
  **FB_b cooperates while SF_k defects**: a (C, D) cell with both searches completed, an exploitation that is a gap
  between the idealized semantics of the calculus and the charged run, not a soundness failure of K_T.
  *Falsifier:* no such cell at any (b ≥ 14, k ≤ 10³, K) under search-charged, or any (C, D) cell with a sound
  prover on the C side under primitive-assisted.
- **S6 (harmless variants).** b\*(Vlet) = 9, b\*(Vwrap) = 11 (copies); FB_b vs Vlet_b mutual cooperation iff
  b ≥ 13, FB_b vs Vwrap_b iff b ≥ 15, Vlet vs Vwrap iff b ≥ 16 ± 1. So RE 5's "+4" clause fails for Vwrap (+7) while
  its falsifier (> 2× = 16) does not fire. *Falsifier:* any of these thresholds off by more than 1.
- **S7 (JLöb-disabled control).** No cell of mutual cooperation between two programs both outside {C, SC}; the only
  cooperation is readers against C and SC (FB, FB1, Vlet, Vwrap from b ≥ 3–9) and SF against C and SC; G exploits SC
  as in the full calculus. RE 5's control clause is therefore scored *failed on the literal operationalization*
  (FB–SC mutual cooperation) while no Löbian cooperation exists. *Falsifier:* any mutual cooperation between two
  programs outside {C, SC}.
- **S8 (audits).** 0 soundness violations over every derived box and every sequent of every witness derivation;
  the independent evaluator agrees on every step used (witness EvR/EvL/Prv steps and every play trace); the replay
  checker accepts every witness. *Falsifier:* any disagreement or violation.
- **S9 (search work).** Every found box in the catalogue at b ≤ 64 is found with W < 10⁴, so search-charged
  self-cooperation of FB, FB1, Vlet, Vwrap and PB is stable from K = 10⁴; refutations at large b are the expensive
  searches (some refutation at b = 64 needs W > 10⁴, so search-charged timeouts exist at K = 10⁴ and the readers'
  defections against G turn into ⊥). *Falsifier:* a found box with W ≥ 10⁴, or no timeout at K = 10⁴ anywhere.
- **S10 (sloppy checker).** SC_b plays C against everything at every b ≥ 1; PB_b defects on SC (SC fails PB's
  D-probe), FB_b cooperates with SC from b = 6 and defects on it at b < 6. *Falsifier:* any deviation.

## Verdict rules

A prediction **held** if no falsifier fired and its positive content was observed; **failed** if a falsifier fired;
**partly** if the falsifier did not fire but a stated positive clause failed. Point predictions with a tolerance
fail outside it. Every RE clause is scored separately where the falsifier is a disjunction. Search outcomes are
reported as found / refuted / timeout throughout; a timeout is never scored as a refutation.
