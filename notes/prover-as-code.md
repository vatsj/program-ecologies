# The prover as code: the calculus K_T^code (notes, 2026-10-06)

Spec `specs/2026-10-06-prover-as-code.md` (reviewed by gpt-6.1-sol; the spec's [after review] text is the
resolution). §1 is the spec's gate: the language change, the fuel-consumption rules, every rule of K_T^code with
its semantic obligation, the soundness theorem (and the exact point where its classical form fails), JLöb's budget
conditions on hand-checked instances with corrupted side conditions, and the visibility question. Written before any
code of this milestone and before any counted cell; §1.10 (code validation of the hand instances) is appended after
the code exists and before any counted cell. §2 (benchmarks and costs) comes after.

## 1. K_T^code

### 1.0 What changes, in one paragraph

In L_T (milestone 1) `prove_b` was a primitive and K_T's atoms were about the *idealized* evaluation, in which a
prove call is one step answered by box truth. Here there is no prove primitive: a program that wants a proof calls
a library function `SEARCH`, an ordinary L_T term (the checker and the iterative-deepening search, written in the
language and run by the language's own evaluator, step by step). The atoms of the calculus are about the **actual,
fuel-indexed run**: ⟨σ, f⟩⇓a is true iff configuration σ, given f more evaluator steps, reaches the constructor a.
There is no idealization left: the truth of every atom is a fact about a finite run. The price is that a reader who
wants to say something about an opponent's run must say something about the *cost* of every search the opponent
performs, because that cost is part of the run. §1.4–1.6 work out what that does to every rule of K_T. The short
answer: K_T's rules whose obligation concerned the *existence* of a derivation (Nec, BoxEq (ii)/(iii), budget
monotonicity, joint JLöb) have no sound code-level replacement, because existence of a derivation does not imply
that a search with finite fuel finds it; JLöb survives in exactly one form, **self-fulfilling Löb** (JLöb^self),
whose hypothesis is the checking search's own success; the box obligation of a search call is discharged by that
hypothesis or by **running** the other search (Run/RunNeg); and a search call can be passed over in one proof node
only because the search **declares a static step cap** U, which turns its unknown cost into a known bound.

### 1.1 The language L_T^code

L_T (notes/realizable-language.md §1.1) with these changes, all fixed here:

- **Removed:** `prove`, `sprove`, the formula builders `mk` and formula values `fv`. Formulas are ordinary data
  (nested pairs, §1.3), built by programs with `pair`, inspected by the checker with `fst`/`snd`/`eq`.
- **Added primitives** (one step each, stuck on ill-typed arguments): arithmetic `op(o, a, b)` on naturals,
  o ∈ {add, sub (truncated), mul, div, mod, le, lt} (div/mod by 0 stuck; le/lt return T/F). L_T had no arithmetic;
  unary arithmetic would make fuel and hashing infeasible, so this is a cost-model choice (a RAM-style unit cost).
- **`capk(k, f, v)`** → `sim(k, app(f, v))` in one step: a bounded call of a function value on a value. It generalizes
  `run(k, x, y)` (kept), which can only run a quoted program on quotes.
- **The library.** A fixed public table LIB of closed λ-terms, referenced by `lib(n)` (a value). `app(lib(n), v) →
  body_n[0 := v]` in one step (β through the table). `libsrc(i)` returns, in one step, the quote of the i-th
  library body: the library's source is visible to every program. A program's quote contains `lib(n)`, not the
  inlined code; this is let-binding the library at the top of every program, with the binding public. The library
  contains the self-interpreter, the checker, the search and their helpers; three search entry points SEARCH_i,
  i ∈ {0 (sound), 1 (sloppy, SC_code), 2 (sound without JLöb, the control)}.
- **eq** compares *full encodings*: a quote compares as its nested-pair encoding, a pair componentwise, a natural or
  constructor as itself, and a function value (lam, fix, lib) as the encoding of its own term. (This differs from
  L_T only on `eq(λ…, ⌜λ…⌝)`, which no program uses.)

**Quote encoding** as in L_T: `fst(⌜t⌝)` is the tag of t as a natural and `snd(⌜t⌝)` its payload, with children as
quotes, so a program can walk any quoted term lazily; tags are extended with lib, op, capk, libsrc.

### 1.2 Fuel-consumption rules

A **configuration** is a closed term σ, possibly with sim frames `sim(k, ·)` inside evaluation contexts. A run of σ
with **global fuel** f: every contraction (β, fix, lib-β, if, fst/snd, eq, op, run, capk, libsrc, sim return, sim
timeout) costs one step of the global counter and one step of the fuel of **every** enclosing sim frame. Precisely
(the L_T rules, unchanged): `sim(k, t)` with t a value returns t (one step, charged to the frames *outside* it); with
k = 0, or t stuck, it returns the constructor TO (one step, charged outside); otherwise one inner contraction gives
`sim(k − 1, t′)`. The global counter is checked before every step; at 0 the run ends (the play is ⊥).

- **Nested evaluation.** `run(k, ⌜x⌝, ⌜y⌝)` and `capk(k, f, v)` open a frame with fuel k. Its steps are charged to
  it and to every enclosing frame and the global counter. If an enclosing counter is exhausted first, the outermost
  exhausted frame times out (the global counter: the whole play is ⊥). The spec's "min(k, f_rem)" is this rule: a
  nested simulation can never run more steps than its caller has left; but exhaustion of the caller is the caller's
  timeout, not the simulation's.
- **Timeout-to-action conversion.** TO is an ordinary value. A program converts it to an action by its own code
  (SF_k: `if eq(run(k, them, me), C) then C else D`, so TO ↦ D, at the cost of the eq and if steps).
- **Search.** `SEARCH_i = λarg. if eq(capk(U, lib CORE_i, arg), T) then T else F`, arg = (c, (ψ, U)): the search
  runs its core inside a frame of fuel U (the **declared cap**, read from its own argument) and converts a core
  timeout to F. Counting the steps (β 1, snd snd 2, capk 1, at most U inner steps, return-or-timeout 1, eq 1, if 1),
  **every search call costs at most u(U) := U + 7 steps**, whatever the formula, and exactly
  W_core + 7 when the core returns within U. The core is deterministic, so a search call's run is a fixed function
  of (i, c, ψ, U).

**Parameters.** b — derivation-size bound (the core's iterative deepening enumerates sizes n = 1..b). W — search work:
the core's evaluator steps, reported with its node expansions and rule-instance count. K — execution fuel (the
encounter's global counter). U — the declared cap of a search, a source parameter; frozen catalogue choice
U = ⌊K/4⌋ (a reader with two searches, PB, needs 2(U + 7) + O(1) ≤ K).

### 1.3 Formulas and the standard model

**Formulas (data).** ⊤ = (0, 0); ⊥ = (1, 0); ¬A = (2, A); A∧B = (3, (A, B)); A∨B = (4, (A, B)); A→B = (5, (A, B));
**atom** ⟨σ, f⟩⇓^m a = (6, (σ̂, (f, (a, m)))) with σ̂ the encoding of a configuration, f ∈ ℕ, a ∈ {C, D},
m ∈ {0 (exact), 1 (monotone, written ⇓⁺)}; **box** ⊡^U_{c,i} ψ = (7, (i, (c, (U, ψ)))). The program-level
`plays_K(x, y, a)` is the exact atom ⟨x ⌜x⌝ ⌜y⌝, K⟩⇓a, built by the program from the quotes it holds; K is a
constant in the program's source (the encounter's fuel is public, like the payoffs).

**Truth.** Defined outright, with no reference to derivability (no fixed point, no selection):
- ⟨σ, f⟩⇓a (exact): the actual run of σ with global fuel f reaches the value a.
- ⟨σ, f⟩⇓⁺a (monotone): the run reaches a, and no frame of the run times out *outside a search call*, and every
  search call encountered starts with every counter ≥ u(U) (so it can never exhaust a counter outside itself). A
  search call is opaque to this condition: what happens inside its own cap frame is its own business.
- ⊡^U_{c,i} ψ: the run of `capk(U, lib CORE_i, (c, (ψ, U)))` from a fresh context returns T. (Since the core runs
  in its own frame, "fresh context" only means: no outer counter interferes.) This is a fact about a finite run.
- Connectives classically; a sequent Γ ⊢ Δ is true iff ∧Γ → ∨Δ.

Box truth is no longer "a derivation exists within c": it is "the code search *finds* one within its cap". The two
differ (a derivation may exist that the search does not reach within U), and every K_T rule whose obligation was
about existence has to be re-examined (§1.5).

**Lemma M (monotonicity of ⇓⁺).** If ⟨σ, f⟩⇓⁺a and σ′ is σ with every sim fuel in σ increased by any amounts and
f′ ≥ f, then ⟨σ′, f′⟩⇓⁺a and ⟨σ′, f′⟩⇓a. *Proof.* The decomposition of a configuration depends on fuels only through
the tests "k = 0" and "global = 0". Along a ⇓⁺ run no counter present in σ is ever tested at 0 outside a search call
(no timeout conversion, no global exhaustion), and a search call starts with all counters ≥ u(U), so it ends (after
at most u(U) steps) without any outer counter reaching 0 inside it; frames created later have fuels fixed by the code.
So σ′ takes the same contractions in the same order and reaches the same value, with no new timeout. ∎

Exact atoms are *not* monotone: SF_k's TO-to-D conversion reads D at small sim fuel and C at large.

### 1.4 Reading of a step, and the search-call state

Each configuration σ is a value, stuck, a **search-call state** (its next contraction is `app(lib SEARCH_i, v)` with
v a value), or has a unique next contraction σ → σ′ (a deterministic step; recorded is whether it is a timeout
conversion). **Reading** ρ(σ, f, a, m): ⊤ if σ is the value a; ⊥ if σ is another value or stuck; ⊥ if f = 0 (the
run has no step left) and σ is not a value; otherwise the atom ⟨σ, f⟩⇓^m a.

**(E1) Deterministic steps.** If σ → σ′ is not a search call: ⟨σ, f⟩⇓a ↔ ρ(σ′, f − 1, a, 0) (for f ≥ 1); and
⟨σ, f⟩⇓⁺a ↔ (the step is not a timeout conversion) ∧ ρ(σ′, f − 1, a, 1). Both are the definitions read one step.

**(E2^code) Search calls.** Let σ = E[app(lib SEARCH_i, (c, (ψ, U)))] with global fuel f and enclosing sim fuels
k_1…k_j (j ≥ 0), and suppose f ≥ u and every k_l ≥ u, u = u(U). Let E↓u be E with every sim fuel decreased by u.
The search call takes W ≤ u steps, returns r = T iff ⊡^U_{c,i} ψ (by definition of the box and the wrapper), and no
outer counter is exhausted during it. The actual successor after the call is E↓W[r] with fuel f − W. By Lemma M,
- ρ(E↓u[r], f − u, a, 1) true ⇒ ⟨σ, f⟩⇓⁺a and ⟨σ, f⟩⇓a,
because E↓W[r] has every counter ≥ that of E↓u[r]. So: (⊡ψ ∧ ρ(E↓u[T], f − u, a, 1)) ∨ (¬⊡ψ ∧ ρ(E↓u[F], f − u, a, 1))
implies ⟨σ, f⟩⇓^m a for either m. (Only this direction is used; the converse fails because the minimal-residual
reading is conservative.)

If some counter is < u the call may or may not exhaust it (W is not known without running the search), and the
calculus says nothing about σ: **this is the static cap at work**. Without a declared cap no search call could be
passed over in one node at all (§1.6).

### 1.5 The rules of K_T^code, each with its semantic obligation

Sequents Γ ⊢ Δ over formula data; size |D| = number of sequent nodes; s, s₁, s₂ premise sizes. Every derivation is
checked **relative to a root call** (ψ₀, b, U₀, i): the search call that is checking it. Side conditions marked
*(syntactic)* are decided by the checker from the data; *(computational)* ones by running code.

| rule | conclusion | premises | size | side condition | obligation (why sound) |
|---|---|---|---|---|---|
| Ax | Γ, A ⊢ A, Δ (A atom or box); Γ, ⊥ ⊢ Δ; Γ ⊢ ⊤, Δ | — | 1 | equality of data *(syntactic)* | trivial |
| G3 | ¬L, ¬R, ∧L, ∨R, →R / ∧R, ∨L, →L | one / two | 1 + s / 1 + s₁ + s₂ | — | classical |
| EvR, EvL | Γ ⊢ ⟨σ,f⟩⇓^m a, Δ / Γ, ⟨σ,f⟩⇓^m a ⊢ Δ | Γ ⊢ ρ′, Δ / Γ, ρ′ ⊢ Δ | 1 + s | σ → σ′ a deterministic step, not a search call; ρ′ = ρ(σ′, f − 1, a, m), and ρ′ = ⊥ if m = 1 and the step is a timeout conversion *(syntactic: one run of the self-interpreter's step function)* | (E1) |
| SrchR | Γ ⊢ ⟨σ,f⟩⇓^m a, Δ | Γ, B ⊢ ρ_T, Δ and Γ ⊢ B, ρ_F, Δ | 1 + s₁ + s₂ | σ a search-call state (i, c, ψ, U); f ≥ u and every enclosing sim fuel ≥ u, u = U + 7 *(syntactic)*; B = ⊡^U_{c,i} ψ; ρ_r = ρ(E↓u[r], f − u, a, 1) | (E2^code) |
| Run | Γ ⊢ ⊡^U_{c,j} ψ, Δ | — | 1 | (c, ψ, U, j) ≠ the root call; the checker runs `capk(U, CORE_j, (c, (ψ, U)))` and gets T *(computational)* | the side condition is the box's truth |
| RunNeg | Γ, ⊡^U_{c,j} ψ ⊢ Δ | — | 1 | (c, ψ, U, j) ≠ the root call; the same run returns F or TO *(computational)* | the side condition is the box's falsity |
| JLöb^self | Γ ⊢ X, Δ | H ⊢ ψ₀ (nothing else on the left) | 1 + s | i ∈ {0, 1}; H = ⊡^{U₀}_{b,i} ψ₀ (the root call's own box, exactly); X = ψ₀, or ψ₀ an atom and X a deterministic downstream reduct of it *(syntactic)* | **self-fulfilment** (Theorem S^code) |

**SrchL is dropped** (a recorded design choice). Its premises would be the left counterpart of (E2^code), which
needs the converse direction: from ⟨σ, f⟩⇓a infer the minimal-residual reading ρ(E↓u[r], f − u, a, 1). That converse
fails: the actual continuation runs from E↓W[r] with W ≤ u, i.e. with *more* fuel than the minimal reading, and the
minimal reading can run out where the actual run does not (and for exact atoms TO conversions break it as well). So an
atom on the left at a search-call state has no rule; it can be closed only by Ax. (Milestone 1's PrvL is used by the
searches only for left atoms coming from implications such as Con → A; losing it costs nothing on the catalogue's
formulas, whose search-call atoms occur on the right.)

**K_T rules with no sound code-level replacement** (each is an obligation that cannot be discharged; the rule is
removed, not repaired):
- **Nec** (from ⊢ A within c infer □_c A). Obligation: a derivation of size ≤ c makes the box true. For ⊡ this
  needs the search to *find* it within U, which depends on the search's work, not on the derivation. Counterexample
  shape: any A whose minimal derivation is small but whose root closure is large (PB at b = 25 needs 3.7·10⁵ host
  expansions in K_T): at a small U the box is false while ⊢ A is derivable. Run replaces Nec (paid in full).
- **BoxEq (ii)/(iii)** (□_a A ⊢ □_c B along a deterministic chain). Obligation: finding A within (a, U) implies
  finding B within (c, U′). The searches for A and B are different computations over different universes; no
  inequality between their works holds in general. Removed.
- **BoxEq (i), budget and cap monotonicity** (□_a A ⊢ □_c A for a ≤ c). Obligation: the core on (A, a, V) finding
  implies the core on (A, c, U) finding, c ≥ a, U ≥ V. **False for search-run boxes**, because the core's own
  hypothesis depends on its budget: FB_b's copy owes ⊡^U_{b,0} A; the core on (A, b, U) closes it with its
  hypothesis ⊡^U_{b,0} A (equal), while the core on (A, b + 1, U) has the hypothesis ⊡^U_{b+1,0} A, which is not the
  owed box, so it cannot close it, and (with Run excluded on its own root and nothing else applicable) it does not
  find A. So ⊡^U_{b,0} A is true and ⊡^U_{b+1,0} A false: the box is not monotone in its budget. Only Ax (identity)
  survives.
- **Joint JLöb** (|S| ≥ 2 members). Obligation: the instance witnesses every hypothesis box. For ⊡, the hypothesis
  of a non-root member is "another search (the partner's, on another formula) finds within its cap", which the
  instance cannot make true and the checker cannot verify without running that search. Removed; this is what
  removes distinct-source Löbian cooperation (§1.7).
- **JLöb's size side condition** m ≥ 1 + Σ s_j is not needed by JLöb^self: its hypothesis is discharged by the
  search's success, not by the instance's size. The instance still counts toward the derivation's size ≤ b.

### 1.6 Soundness

**Box truth is outside the induction** as in K_T: ⊡ is a fixed fact (a finite run). A derivation D checked relative
to the root call (ψ₀, b, U₀, i) is **valid** iff every syntactic side condition holds, every Run/RunNeg side
condition holds (a fact about a run), and, if D uses JLöb^self, its hypothesis H = ⊡^{U₀}_{b,i} ψ₀ is true.

**Theorem S^code (soundness).** Every sequent of a valid derivation is true.
*Proof.* Strong induction on size. Ax, G3: as in K_T. EvR/EvL: (E1). SrchR: suppose Γ true and Δ false. If B is
true, premise 1 (true by IH) gives ρ_T, so (E2^code) gives the atom; if B is false, premise 2 gives ρ_F (B being
false), and (E2^code) gives the atom. Run/RunNeg: the side condition is the truth of the right box / falsity of the
left box. JLöb^self: by validity H is true; the premise H ⊢ ψ₀ is true by IH, so ψ₀ is true, and X, equal to ψ₀ or
deterministically downstream of the atom ψ₀ along non-search steps, is true by (E1). ∎

**Corollary (what a search call certifies).** If `capk(U₀, CORE_i, (b, (ψ₀, U₀)))` returns T, ψ₀ is true (i ∈ {0, 2}).
*Proof.* The core returns T only after accepting a derivation D of ⊢ ψ₀ of size ≤ b whose syntactic conditions it
checked and whose Run/RunNeg conditions it verified by actually running the named cores (a nested run that is cut
short by the core's own cap aborts the whole core, which then does not return T). Its JLöb^self hypothesis is
⊡^{U₀}_{b,i} ψ₀ — and that is exactly the statement that this run returns T, which it does. So D is valid and
Theorem S^code applies. ∎

**Where the classical form fails, exactly.** K_T's Theorem S says *every derivable sequent is true*, derivability
being a syntactic set. Here validity has two non-syntactic ingredients: (a) Run/RunNeg side conditions are facts
about runs (decidable by running, but at the cost of the run); (b) JLöb^self's hypothesis is not checkable by any
checker *before* the checking search finishes, because it is the statement that the checking search succeeds. A
checker that accepts JLöb^self instances is sound only **ex post**: a derivation it returns is valid because it
returned it. Another checker (the independent replay checker, a different search) can validate such a derivation
only by also verifying the root call's success (for the replay checker: the recorded T of the run that produced it).
The corollary is the soundness statement that matters for play: *a sound reader's cooperation is always justified by
a true statement about the actual run*.

**Why no reflection rule** (bounded Gödel II, code form). A rule "Γ, ⊡ψ, ψ ⊢ Δ / Γ, ⊡ψ ⊢ Δ" (the search is sound, so
use ψ) is true in the model (by the corollary) but cannot be added: with it, JLöb^self proves any root ψ₀ in three
nodes (H ⊢ ψ₀ by reflection on H and Ax), the search returns T, and ψ₀ may be false. Self-fulfilment and reflection
are jointly inconsistent: Löb's theorem in this calculus.

### 1.7 Consequences for the catalogue (derived by hand; predictions in the predictions file)

- **Twins self-certify.** FB_{b,U,K} against its copy: the copy's run is 2 steps to its search call on
  (0, b, A, U) with A = plays_K(FB, FB, C) — the reader's own root call. Derivation: JLöb^self over A [H ⊢ A: EvR,
  EvR, SrchR (side condition K − 2 ≥ U + 7) with P₁ = H, B ⊢ ⟨if(T,C,D), K−2−u⟩⇓⁺C (EvR⁺, then ⊤: 2) and
  P₂ = H ⊢ B, ⟨if(F,C,D), …⟩⇓⁺C (Ax, H = B: 1)] = 1 + 2 + (1 + 2 + 1) = 7. **b\*(FB) = 7**, provided the core finds it
  within U; (K_T: 8; the difference is that L_T^code's program reaches its search call in 2 steps, not 3, because
  building the formula is free: a pair of values is a value).
- **Distinct sources cannot certify each other** (FB_x vs FB_y, x ≠ y; FB vs FB1, PB, Vlet, Vwrap): the target's
  search call is on a formula other than the reader's root, so its box is owed in SrchR's second premise and can
  only be closed by Run, which runs the target's core, whose derivation needs the reader's box, which it can only
  close by Run on the reader's root call — a nested run of the outer computation. Each nesting is a new frame of fuel
  U inside the previous one; the outermost core's cap is exhausted first; the reader's search times out (returns
  F after spending U). Predicted: (D, D), both searches interrupted. The FairBot distinct-budget grid is diagonal.
- **Simulators.** FB vs SF_k: SF reaches FB's search call inside its sim with sim fuel k − 2 and global K − 5; the
  inner FB's search call is the reader's root call (FB builds plays_K(SF, FB, C) in both places). SrchR needs
  k − 2 ≥ U + 7; then JLöb^self closes the owed box and FB certifies ⟨SF ⌜SF⌝ ⌜FB⌝, K⟩⇓C. If k < U + 9 nothing
  certifies SF's run (the static condition fails), the reader's search (and the identical inner search) does not
  find, and SF's inner FB defects: (D, D). The certified target is SF's actual run (matched), so the leak closes by
  Theorem S^code. A **mismatched** reader (FBx: names fuel K′ = 10K, cap U = ⌊K/4⌋) certifies a run at K′; the
  certified run differs from the executed one only if the target's run length lies in (K, K′], which needs a run the
  calculus can pass over cheaply (search calls) of total length > K.
- **PB** needs a second search's box: Con → plays(PB, D, D). Its first search call is the reader's root (JLöb^self);
  the second is owed and closed by **Run** (the second query's core runs; its own derivation of PB-vs-D's defection
  closes the hypothetical "PB finds plays(D, PB, C)" branch by RunNeg, a nested run that refutes). Acyclic, so it
  terminates without regress; PB self-cooperates iff all three runs fit their caps.
- **G** (if found then D else C): JLöb^self cannot close the T-branch (the copy defects) and RunNeg on the root is
  excluded, so G's search does not find; G cooperates with every sound reader that does not find a proof, as in K_T.
- **P\*** needs ⊢ Con → A and then not-⊢ A for its copy: the second query is A, owed with the reader's root being
  Con → A; Run on A runs a core whose copy-run includes the search on Con → A — the outer root — so the regress
  of the distinct-source case: P\* does not self-cooperate (by cap exhaustion, not by a Gödel-sentence argument).
- **SC_code** (sloppy: every side-condition predicate returns true — fit, root exclusion, Run/RunNeg without running,
  JLöb at any formula with hypothesis ⊡^U_{b,1} X): proves every atom whose run reaches a search call (SrchR, the
  T-branch closed by unverified RunNeg, the F-branch by unverified Run), so SC_code cooperates with G and G (sound)
  certifies SC_code's cooperation by running SC_code's sloppy core (Run): SC_code is exploited by G. FB certifies
  SC_code the same way and SC_code proves FB cooperates: (C, C).
- **Control (CORE_2, no JLöb^self):** no prover certifies a twin or a simulator; only evaluation-based cooperation
  (C) and refutation-based cooperation (G) remain.

### 1.8 The visibility question

*Can a reader certify a run longer than its own proof-and-check computation?*

**Yes, through two mechanisms, and no otherwise.** (i) A search call is passed over in one node (SrchR) whatever its
length up to the cap, so a run containing m search calls of length ≈ W each is certified by a derivation of about
m·6 nodes. (ii) The *outcome* of such a call is certified without running it only when the call is the reader's own
root call (JLöb^self); any other search call's outcome must be run (Run/RunNeg), which costs the reader at least
that search's work. Every other step of the target is one EvR node, and derivations have at most b nodes. Hence:
**a reader can certify a run of length up to about m(U + 7) + b, longer than its own computation, if and only if
every search call in it is a copy of the reader's own root call (or a call whose run the reader pays for).** The
canonical example: a twin that searches the reader's query twice (FB2 below) runs for about 2W while the reader
computes for about W. A simulation is certifiable without unfolding its prover's search when that prover's search is
the reader's own root call; it is never certifiable by unfolding (W ≫ b). So the RE's dichotomy ("simulations obey a
fuel bound, provers do not") is replaced by: **every target obeys the static cap condition (counters ≥ U + 7 at each
search call); what separates certifiable from uncertifiable targets is whether their search calls are the reader's
own.**

### 1.9 JLöb^self's budget conditions: hand-checked instances and corrupted side conditions

JLöb^self has four conditions: the hypothesis core id, budget and cap are the root call's own (i, b, U₀), and its
content is the root ψ₀; the conclusion is ψ₀ or downstream of it. SrchR's static condition and Run's root exclusion
interact with it. Hand-checked instances (FB_{b,U,K}, root A = plays_K(FB, FB, C), A₀ → A₁ → A₂ = search call):

1. **Valid:** H = ⊡^U_{b,0} A; D = JLöb^self[H ⊢ A: EvR, EvR, SrchR(P₁: EvR⁺, ⊤; P₂: Ax H = B)]; size 7. Valid
   relative to (A, b, U, 0) whenever the core returns T — which it does when it finds D within U.
2. **Corrupted budget (H = ⊡^U_{b−1,0} A).** P₂ needs H = B = ⊡^U_{b,0} A: Ax fails (data differ). If accepted by a
   checker that only compares contents, the hypothesis would be "the core on (A, b − 1) finds" — which is false at
   b − 1 = 6 < 7 (no derivation of size ≤ 6), so the derivation would certify A on a false hypothesis. Must be rejected.
3. **Corrupted cap (H = ⊡^{U−1}_{b,0} A, the owed box has cap U).** Ax fails. A "cap-monotone" checker accepting
   V ≤ U would be unsound by the budget counterexample of §1.5 transposed to caps (the core at cap U − 1 has
   hypothesis ⊡^{U−1} and cannot close the copy's ⊡^U).
4. **Corrupted member (JLöb^self concluding A′ = plays_K(FB, FB1, C) with hypothesis ⊡ A′, inside the search for
   A).** The hypothesis is not the root call's: rejected. Accepting it would let any search assume any box — the
   sloppy checker's rule.
5. **Corrupted conclusion (X upstream of ψ₀, or X = the search-call state's after-state ⟨if(T, C, D)⟩⇓⁺C reached
   through the search call).** The downstream relation is along deterministic non-search steps only; a reduct reached
   through a search call is not downstream (its truth depends on the call's outcome). Rejected.
6. **Corrupted SrchR fit (K − 2 < U + 7, e.g. K = U + 8).** The static condition fails: rejected. If accepted, the
   copy's search call could be cut off by the global counter (the copy plays ⊥) while the reader certifies C.
7. **Corrupted Run (Run on the root call).** Excluded syntactically. If allowed, the search would run its own core
   inside itself; each nesting re-enters the same derivation; the regress ends only when the outermost cap is
   exhausted, so the search returns F after U steps — not unsound, but it destroys every self-proof whose search
   tries Run before JLöb^self (iterative deepening reaches the owed box at size ~4, before the size-7 JLöb instance).
   The exclusion is therefore a liveness condition, not a soundness one.

§1.10 records the code's verdicts on exactly these instances.
