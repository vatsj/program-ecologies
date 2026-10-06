# Certificates as code: the calculus K_T^cert (notes, 2026-10-06)

Spec `specs/2026-10-06-certificates-as-code.md` (reviewed by gpt-6.1-sol; the [after review] text is the resolution).
§1 is the spec's gate: the carrier programs as L_T^code terms, the certificate language and the checker term, every
rule of K_T^cert with its semantic obligation, the pair rule and its guard, and Theorem S^cert in the unconditional
semantic form. It was written before any code of this milestone and before any counted cell. §1.11 (code validation
of the hand instances) is appended after the code exists and before any counted cell; §2 (costs) after that.

Base: `notes/prover-as-code.md` §1 (L_T^code, fuel rules, Lemma M, the regress lemma of §2.1) is assumed throughout;
"milestone 3" means that note.

## 1. K_T^cert

### 1.0 What changes, in one paragraph

A carrier publishes, inside its own source, a list of certificates; a reader *checks* the opponent's certificate
for the reader's question instead of searching for a proof. Three facts shape everything below. (i) **A certificate
for a carrier's own run cannot be an explicit derivation** (Lemma F, §1.2): the root sequent of such a derivation
contains the carrier's initial configuration, which contains the carrier's source, which contains the certificate.
Certificates are therefore **scripts**: derivation skeletons (rule names and principal-formula positions) from which
the checker reconstructs every formula, starting from a root it builds itself out of the two quotes it holds. Scripts
mention no source, so self-reference disappears instead of being encoded, and the program's quote (code plus script
list plus checker reference plus its fuel constants) is the whole behavioural object. (ii) **The fact a reader needs
about its opponent is a fact about a check run**, not about a search: the opponent's code branches on "my check of
your script returns T". A check is a deterministic computation over finite data with a declared cap, so its box is a
fact about a finite run, as in milestone 3. (iii) **The pair rule is sound because the two checks are the same
computation.** Reader Y checking X's script may close X's check-call box on Y's own script (the *swap* of Y's root)
as a hypothesis, *provided Y's check validates Y's own script one level, with the two roots as the only hypotheses*.
Then X's check of Y and Y's check of X run the same two validations in the opposite order, so they return the same
value (Lemma Sym), and that is what discharges the hypothesis. No fixed point is selected: both checks evaluate one
syntactic predicate of the pair of scripts. The guard the RE predicted (the hypothesis must be the checker's *own*
call) is sound but yields twins only, as in milestone 3; the unguarded rule (assume the partner's check without
validating it) is unsound, with an explicit counterexample (§1.7). Search calls get no rule: a program that searches
cannot carry a certificate.

### 1.1 The language and the library extension

L_T^code is unchanged (milestone 3 §1.1–1.2). The library is milestone 3's (indices and terms unchanged; the
constant NLIB grows) followed by new entries, all ordinary L_T^code terms, public, readable by `libsrc`:

- **Check wrappers** `CHK_x = λarg. if eq(capk(fst arg, CC_x, arg), T) then T else F`, one per checker variant x,
  with argument **arg = (V, (t, (m, (a, K))))**: V the declared cap (a natural), t the quote whose script is checked,
  m the quote of the opponent it is checked against, a ∈ {C, D} the asked outcome, K the fuel of the asked atom.
- **Check cores** `CC_x = λarg. ccore(x, arg)` (§1.4) and their helpers: the check-aware self-interpreter `cstep`
  (milestone 3's `step` with one change: an application of a check wrapper, like an application of a search wrapper,
  is a **call state** rather than a β step), `evstar`, `chkstate`, the script checker `cchk`, the validator `vone`,
  `getcerts`, and the dispatcher `callcheck(n, arg)` that runs `capk(fst arg, CC_n, arg)`.

**Checker variants** (the mode x; each wrapper is a distinct library entry, so a call names its checker):

| x | name | hypotheses a script may close | partner validation |
|---|---|---|---|
| 0 | **sound** (CHK_S) | R and S | yes (§1.4) |
| 5 | sound copy (CHK_S2) | its own R and S | yes; identical code, a different library entry |
| 1 | naive (CHK_N) | R and S | **no** (the unguarded pair rule) |
| 2 | self-only (CHK_O) | R only (the RE's guard; milestone 3's JLöb^self) | — |
| 3 | none (CHK_X) | none (acyclic scripts only: the control) | — |
| 4 | sloppy (CHK_L) | — accepts iff t's list has an entry for a (the spec's "end sequent matches") | — |

**Fuel of a check call.** With V = fst arg a natural: lib-β 1, `fst` 1, `capk` 1, at most V inner steps, the frame's
return or timeout 1, `eq` 1, `if` 1. **Every check call costs at most u(V) := V + 6 steps** and exactly W + 6 when the
core returns within V after W inner steps. A core timeout or a stuck core becomes F.

**Carriers.** A carrier's source is `λme. λthem. (λcerts. BODY) CERTS`, a let whose bound value CERTS is a literal
data term (pairs, naturals, constructors): the **certificate list**, a list of entries (a, script). BODY never uses
`certs`; the binding exists only so that the list is part of the source at a fixed position. The canonical body is

  CB:  `if CHK_S(V, (them, (me, (C, K)))) then C else D`

and the catalogue's other shapes (§1.8) are built the same way. **Extraction** `getcerts(t)` walks the quote t: tag
λ, tag λ, tag app whose function part has tag λ; its argument's encoding is converted to data by milestone 3's `full`.
Any other shape gives NONE (the program carries nothing). There is no lookup by opponent: the checker tries the
entries with outcome a in list order and accepts the first script that validates.

**Identity.** Play depends on code, list, checker entry, V and K, and all of them are in the quote; atoms are about
configurations that contain the quote; so a certificate certifies the complete object. A program with the same code
and another list (CBmut) is another program, and every check about it is a check about its own run.

### 1.2 Lemma F: explicit self-certificates are not finite

*An explicit derivation (every node carrying its sequent) of ⊢ plays_K(x, y, a), carried in x's source, does not
exist as finite data.* The root sequent contains the atom ⟨x ⌜x⌝ ⌜y⌝, K⟩⇓a, whose configuration contains ⌜x⌝, whose
encoding contains x's certificate list, which contains the derivation: a proper sub-datum equal to itself. ∎ The same
holds for any certificate that writes down a configuration reached before the let-binding is consumed. Placeholders
for "my own source" are not enough either: the configurations after the first β contain *parts* of the source (the
body with the list), not the whole quote. So the certificate must omit the formulas, and the checker must rebuild
them. That is a script, and with scripts the spec's "literal certificates" (sources and fuel-indexed atoms written
out) do not arise. A script also contains no opponent: §1.8 shows the carriers' scripts are opponent-generic.

### 1.3 Formulas, truth, scripts

**Formulas (data).** ⊤ = (0, 0); ⊥ = (1, 0); atom ⟨σ, f⟩⇓^m a = (6, (σ̂, (f, (a, m)))) as in milestone 3 (m = 0
exact, 1 monotone); **check box** ⊡_n(arg) = (8, (n, arg)), n the library index of a check wrapper and arg a data value
(V, (t, (m, (a, K)))). Milestone 3's search boxes (tag 7) and connectives do not occur: the root is an atom, and every
rule's premises are atoms, check boxes, ⊤ or ⊥.

**Truth.**
- Atoms exactly as in milestone 3 §1.3, with "search call" generalized to **call** (search or check): ⟨σ, f⟩⇓⁺a
  requires that no frame times out outside a call and that every call starts with every counter ≥ its u (u(U) = U + 7
  for a search, u(V) = V + 6 for a check).
- ⊡_n(arg): the clean run (fresh context) of `capk(V, CC_n, arg)` returns T. A fact about a finite run.
- A sequent Γ ⊢ Δ is true iff ∧Γ → ∨Δ.

**Root of a check.** A run of CC_x on arg = (V, (t, (m, (a, K)))) builds:
- ψ = ⟨t ⌜t⌝ ⌜m⌝, K⟩⇓a, the exact atom, from the two quotes (milestone 3's CONF encoding);
- R = ⊡_{n_x}(arg), the box of this very check (n_x the wrapper of mode x);
- S = ⊡_{n_x}(swap arg), swap (V, (t, (m, (a, K)))) = (V, (m, (t, (a, K)))): **the check the checked program makes
  on the checker's script**, under the same checker, cap, outcome and fuel.

**Scripts.** A node is (r, (j, ps)): rule code r, principal-formula position j (in R, or in L for RunNeg), premise
list ps. Sequents are lists (milestone 3's `fadd` prepends a formula not already present, `fdel` removes it), so
positions are deterministic. Script size = number of nodes; **expanded size** = size with each EvR* node counted as
the number of steps it takes.

### 1.4 The check

    ccore(x, arg):  R := ⊡_{n_x}(arg);  S := ⊡_{n_x}(swap arg);
                    (ok, usesS) := vone(x, arg, R, S)
                    if not ok: F
                    elif x ∈ {0, 5} and usesS: fst vone(x, swap arg, S, R)
                    else: T

`vone(x, arg, Rb, Sb)` extracts t's list (NONE → not ok), builds ψ and tries each entry (a′, s) with a′ = a in order:
`cchk` runs script s on the sequent ⊢ ψ with hypothesis boxes {Rb, Sb} (mode 0, 1, 5), {Rb} (mode 2) or none (mode 3)
and the cap V_root = V; it returns 0 (invalid), 1 (valid without Sb) or 2 (valid, closing Sb ≠ Rb). The first valid
script decides (ok = T, usesS = (result = 2)). Mode 4 (sloppy) returns ok iff some entry has a′ = a.

The partner validation is **one level**: the partner's script is checked with the same two boxes as hypotheses
(its own root S and the partner's R), and nothing is checked behind them. So no check ever runs its own call or its
swap; the cycle is closed syntactically, not by a nested run.

### 1.5 The rules of K_T^cert, each with its semantic obligation

Checked relative to a root (x, arg) with R, S as above. Positions j refer to the current sequent's lists.

| rule | code | conclusion | premises | side condition | obligation (why sound) |
|---|---|---|---|---|---|
| Ax | 0 | Γ ⊢ Δ | — | ⊥ ∈ Γ, or ⊤ ∈ Δ, or an atom or box in both *(syntactic)* | trivial |
| EvR* | 26 | Γ ⊢ A, Δ, A = ⟨σ, f⟩⇓^m a at position j | Γ ⊢ φ, Δ | f ≥ 1 and σ's next step is deterministic (not a call); φ = evstar(A): repeat the step while it is deterministic, f ≥ 1 and (m = 0 or the step is not a timeout conversion); stop at a value (⊤ if it is a, else ⊥), stuck (⊥), f = 0 (⊥), a timeout conversion in m = 1 (⊥), or a call state (the atom there) *(syntactic: runs of `cstep`)* | milestone 3's (E1), iterated |
| ChkR | 25 | Γ ⊢ A, Δ, A at a **check-call state** E[app(lib CHK_n, v)] | Γ, B ⊢ ρ_T, Δ and Γ ⊢ B, ρ_F, Δ | v is a pair whose first component is a natural V′; f ≥ u and every enclosing sim fuel ≥ u, u = V′ + 6; B = ⊡_n(full v); ρ_r = reading(E↓u[r], f − u, a, 1) *(syntactic)* | (E2^cert), §1.6 |
| Run | 1 | Γ ⊢ B, Δ, B a check box at j | — | B ∉ {R, S}; B's cap V_B ≥ V; the checker runs `capk(V_B, CC_n, arg_B)` and gets T *(computational)* | the side condition is B's truth (Lemma N) |
| RunNeg | 2 | Γ, B ⊢ Δ, B a check box at j in Γ | — | as Run; the run returns F or TO | B's falsity (Lemma N) |
| Hyp^self | 3 | Γ ⊢ R, Δ | — | the box at j equals R *(syntactic)*; modes 0, 1, 2, 5 | **ex post**: the check returns T only if R is true |
| Hyp^pair | 3 | Γ ⊢ S, Δ | — | the box at j equals S ≠ R; modes 0, 1, 5; in modes 0 and 5 the check also validates the partner (§1.4) | **Lemma Sym** (mode 0, 5); none in mode 1 (unsound, §1.7) |

**No rule for search calls**: an atom at a search-call state can only be closed by Ax. A program whose run searches
(milestone 3's FB, PB, …) carries no derivable certificate; nothing in its run is certifiable past the search.
**No EvL, SrchL, connectives, cut, reflection:** not needed (the formulas that occur are atoms, boxes, ⊤, ⊥; atoms
occur only on the right; boxes on the left come only from ChkR), and reflection would be unsound with Hyp^self for
the reason given in milestone 3 §1.6.

**Removed relative to the RE's sketch:** "ChkR is one evaluation step": a check call is charged u(V) = V + 6, a bound
on the actual run enforced by the cap frame, and its premises read the continuation at the minimal residual fuel.

### 1.6 Soundness

**(E2^cert) Check calls.** Let σ = E[app(lib CHK_n, v)] with global fuel f and enclosing sim fuels k₁…k_j, v a pair
whose first component is V, and suppose f ≥ u and every k_l ≥ u, u = V + 6. The call runs W + 6 ≤ u steps; by
**Lemma N** below its value is T iff ⊡_n(full v); no outer counter is exhausted during it. The actual successor is
E↓(W+6)[r] with fuel f − W − 6, and by **Lemma M** (milestone 3, with calls in place of search calls) reading the
continuation E↓u[r] at f − u true in the ⇓⁺ sense implies the atom ⟨σ, f⟩⇓^m a for either m. Hence
(B ∧ ρ_T) ∨ (¬B ∧ ρ_F) implies the atom, which is ChkR's obligation.

**Cap monotonicity (the Run guard).** In a check with root cap V every Run/RunNeg box has cap ≥ V; by induction every
check frame nested inside the root (at any depth) has cap ≥ V and starts later, so **the root frame has the earliest
deadline of every frame inside it**. In a play, ChkR's fit puts every outer counter at ≥ V + 6 at the call, later
than the root's deadline (V + 3 steps after the call starts).

**Lemma N (in-context runs are clean runs).** (a) In any run of a check frame F (clean or inside a play under the fit
condition), a nested check either returns the value of its own clean run, or F's frame (or one enclosing it) times out
first. (b) If the root returns T, no regress occurred anywhere inside it, and every nested run returned its clean
value. *Proof.* The only ways an in-context nested run can differ from its clean run are (1) an enclosing counter is
exhausted, or (2) a call inside it has the key of a frame enclosing it (the regress lemma, milestone 3 §2.1), so the
evaluator fast-forwards to the earliest enclosing deadline. Program-level frames (sim frames of `run`, wrapper frames
in plays) have keys no check computation produces (checks never run programs; a check frame inside a play is the call
itself). Within a check, the earliest deadline is the root's (cap monotonicity), and outer frames are later (fit). So
(1) and (2) end in the root's timeout, never in a different value delivered to the nested run's caller. In a run that
returns T the root did not time out, so neither happened. ∎ Corollary: the in-play value of a check call equals the
box's truth (used in E2^cert).

**Lemma Sym (the pair).** Let x ∈ {0, 5}. If the clean run of CC_x on arg returns T within V and vone(x, arg, R, S)
reported usesS, then the clean run of CC_x on swap arg returns T within V.
*Proof.* In the run on arg (call it ρ_R) both validations ran: P₁ = vone(x, arg, R, S), then P₂ = vone(x, swap arg,
S, R), both ok. The run on swap arg (ρ_S) performs P₂, and, if P₂ reported usesS (i.e. the partner's script closed R),
then P₁. These are the same computations on equal data (R and S are rebuilt from the argument: swap(swap arg) = arg),
so they agree in value and step count unless their nested runs behave differently in the two contexts. The two
contexts differ only in the root frame's key (κ_R against κ_S). By Lemma N(b) no call with key κ_R occurs in ρ_R. A
call with key κ_S inside P₂ would, in ρ_R, start a nested run of CC_x on swap arg that repeats P₂ up to that same call,
now a regress, killing ρ_R's root: impossible. A call with key κ_S inside P₁ forces, by the same argument, P₂ not to
report usesS (otherwise the nested run would repeat P₁ up to the regress), so ρ_S never runs P₁. Hence ρ_S's
computations contain neither key, behave as in ρ_R, and ρ_S's total is at most ρ_R's (P₂ + P₁ in the other order,
or P₂ alone, plus the same fixed overhead, or less): within V. ∎

**Theorem S^cert (unconditional soundness).** For every arg = (V, (t, (m, (a, K)))) with t, m arbitrary quotes (any
programs, carriers or not), if the clean run of `capk(V, CC_0, arg)` returns T then ⟨t ⌜t⌝ ⌜m⌝, K⟩⇓a is true. The same
holds for CC_5, CC_2 and CC_3. It fails for CC_1 and CC_4.
*Proof.* The run returned T, so (by the code, Lemma C below) some entry's script s is a valid derivation of ⊢ ψ in the
following sense: every syntactic side condition of §1.5 holds at every node, every Run/RunNeg side condition held in
the run, and every Hyp node closes R or S (S only in modes 0, 5). Show by strong induction on the expanded size that
every sequent of the derivation is true. Ax, EvR*: as milestone 3. ChkR: (E2^cert). Run/RunNeg: the in-run value
equals the clean value (Lemma N(b)), which is the box's truth. Hyp^self: the box is R, which is true because the run
returned T (ex post, as milestone 3's JLöb^self: the hypothesis is the statement that this run returns T). Hyp^pair:
the box is S; the run reported usesS, so it also validated the partner, and Lemma Sym gives S true. So the root
sequent ⊢ ψ is true. ∎

*What the proof does not assume.* It never uses "CHK accepts ⇒ true" for any check: Run/RunNeg use only the value of a
run (Lemma N), Hyp^pair uses only that two runs compute the same predicate (Lemma Sym), Hyp^self uses only that this
run returned T. It does use **Lemma C** (code correctness): `cchk` returns non-zero on a script only if the script
satisfies the rule table above, and `vone`/`ccore` have the control flow of §1.4. Lemma C is a property of the checker
term's code, verified by reading and tested against an independent host replay checker on every check in every cell
(§1.10).

**Where Theorem S^cert fails, exactly.** (i) Mode 1 (naive): Hyp^pair without partner validation, so S may be false
(§1.7(a)). (ii) Mode 4 (sloppy): no validation at all. (iii) Without the Run cap guard Lemma N(b) needs another proof
(a nested frame with an earlier deadline than the root could time out because of a regress on the root's key and hand
TO to RunNeg); the guard costs nothing in the catalogue (all carriers use V = ⌊K/4⌋), so whether it is necessary is
left open. (iv) If the pair rule allowed S with a different cap or fuel than R, Lemma Sym's cost argument fails (the
partner's check could time out where the reader's did not); swap keeps V and K, so this is excluded by construction.

### 1.7 Trying to break it

**(a) The unguarded pair rule is unsound (cyclic certificate for a false atom).** Mode 1, two naive carriers: CBN
(naive code, list [(C, s_FB), (D, s_D)]) and CBN0 (naive code, empty list). CBN0 checks CBN: root R = ⊡_N(V, CBN,
CBN0, C, K), S = ⊡_N(V, CBN0, CBN, C, K). s_FB runs CBN's code to its call, which is exactly S (CBN checking CBN0),
ChkR, T-branch to C, F-branch closed by Hyp(S). Accepted without validating CBN0's (absent) script: CBN0 cooperates.
CBN checks CBN0: no list, F, defects. The accepted atom plays(CBN, CBN0, C) is false. The sound checker on the same
pair (CB against CB0, CB0 the sound code with an empty list) validates the partner, finds no script, returns F:
both defect. *So partner validation is the guard*, and it is what distinguishes the pair rule from "assume the other
side's check".

**(b) Dcert: a cyclic script for "D-code cooperates".** Dcert's code is D (`λλ (λcerts. D) CERTS`) and its list holds
scripts rooted at the C question: [Hyp at 0], [EvR*; Hyp at 0], [Ax], [EvR*; ChkR …]. Against any sound, self-only or
none checker: the root is an atom (Hyp needs a box: invalid); EvR* reaches the value D, giving ⊥ (Hyp has no box to
close, Ax fails); ChkR needs a call state (Dcert's run has none). Hyp only ever closes a box *on the right*, and a box
reaches the right only through ChkR's second premise, i.e. only where the certified program's own run makes a check
call. **A run without a check call can only be certified by evaluation**, so no hypothesis rule (guarded or not)
certifies D's cooperation; Dcert fools only the sloppy checker. Mode 1 also rejects it.

**(c) Anti-self-checkers.** `if CHK_S(me, them, C) then D else C` (cooperate iff my own certificate fails): its
cooperation script would need the T-branch (box R on the left, run reaching D) closed, which only RunNeg could do,
and RunNeg on R is excluded; there is no script. So its own check returns F and it does cooperate: a true atom with
no certificate, like the Gödel sentence, and no false atom is certified. `if CHK_S(them, me, C) then D else C` (CBdef, G-shaped): its script
would need RunNeg on S, excluded; sound readers find none and defect; it cooperates with them (their scripts use
Hyp(S), whose partner validation fails), so it is suckered, as G was.

**(d) Self-trust.** LöbC = `if CHK_S(me, them, C) then C else D` checks *its own* script against the opponent. Its
script closes the F-branch by Hyp^self (its box is the reader's R): valid against every opponent, and true: its own
check validates the same script ex post, so it cooperates with everyone, D included. A certified CooperateBot; sound.

**(e) Different checkers.** CB (CHK_S) against CBS2 (CHK_S2, identical code, another library entry): each run's box
names the other checker, so it is not R or S of the reader's check; the script must Run it, the partner's check Runs
the first check back, and the regress kills the outermost frame. (D, D). The pair rule couples carriers **that share a
checker**; the checker entry is part of the convention, as the proof system was in the modal arm. Making two checkers
mutually admissible would need each to verify the other's code (an equivalence a checker cannot decide in general).

**(f) Fuel and cap mismatches.** A reader whose K or V differs from its partner's: S built by the reader carries the
reader's (V, K); the partner's call carries the partner's; they differ, Hyp^pair does not apply, Run regresses: (D, D).
A script whose ChkR fit fails (K too small for V + 6 plus the continuation): ChkR inapplicable, invalid.

No sound counterexample was found; Theorem S^cert stands for modes 0, 2, 3, 5.

### 1.8 Consequences for the catalogue (by hand)

Fuel: V = ⌊K/4⌋, SF's k = ⌊K/2⌋. Scripts are opponent-generic when the run reaches its calls by deterministic steps
that do not inspect the opponent, which holds for every carrier: EvR* stops at the next call, whatever the opponent.

| program | code (inside `λme.λthem.(λcerts. ·) CERTS`) | C script | nodes / expanded |
|---|---|---|---|
| CB | `if CHK(them, me, C) then C else D` | EvR*; ChkR[EvR*; Ax · Hyp] | 5 / 7 |
| CB1 (FB1-shaped, self-auditing) | `if CHK(them, me, C) then (if CHK(me, them, C) then C else D) else D` | EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Hyp] · Hyp] | 8 / 10 |
| CBP (PB-shaped) | `if CHK(them, me, C) then (if CHK(them, ⌜D⌝, D) then C else D) else D` | EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Run] · Hyp] | 8 / 10 |
| D script (all carriers) | — | EvR*; ChkR[RunNeg · EvR*; Ax] | 5 / 7 |
| Ccert | `C` | EvR*; Ax | 2 / 4 |

(CHK = CHK_S with arguments (V, (·, (·, (·, K)))); the D script answers "this carrier defects against ⌜D⌝": its call
checks D, which carries nothing, so RunNeg closes the T-branch.)

- **Distinct carriers cooperate**: CB–CB1, CB–CBP, CB1–CBP, and the harmless variants, at any K where the checks fit.
  CB1's run has two calls, S and R from its reader's side, both closed by Hyp. CBP's second call (the reader's D
  script) is closed by Run, a nested check one level deep, which itself runs one RunNeg (D's empty list): nesting
  depth 3, and no check re-enters its own call.
- **PB-shaped readers need a D script** from their partners; a carrier without one (CBmut) is refused by CBP.
- **Twins** need only Hyp^self (S = R); so do simulators: SFc (`if eq(run(k, them, me), C) then C else D` carrying
  the script EvR*; ChkR[EvR*; Ax · Hyp]) is certified by an FB-shaped reader because the reader's own check of SFc,
  run inside SFc's simulation, *is* the reader's root R. Fit inside the simulation: k − (steps before the call) ≥
  V + 6 holds at k = K/2, V = K/4. Against CB1 or CBP the simulated reader makes two calls, needing k ≥ 2(V + 6) +
  steps > K/2: no script.
- **Searchers and carriers: (D, D).** A carrier finds no list in a searcher's quote. A searcher's milestone-3 core
  meets the carrier's check call as an ordinary library β step (the milestone-3 self-interpreter does not know check
  wrappers), so it must unfold the whole check (≈ 10⁴ steps) by EvR: beyond any b ≤ 64; not found.
- **Controls.** Mode 3 (none): only acyclic scripts (Ccert, and the D scripts: RunNeg is acyclic): carriers cooperate
  with Ccert, with nobody else. Mode 2 (self-only): adds twins and SFc. Mode 0 adds the distinct-carrier pairs. That is
  the measured decomposition the spec asks for: evaluation, self-fulfilment, pair.
- **Fakers.** CBfake (D's code, CB's list): every script fails on its actual run: refused. CBdef: suckered (above).
  CBmut (CB's code, list [(C, s_CBP), (C, s_CB)], D script dropped): FB- and FB1-shaped readers skip the invalid first
  entry and accept the second; CBP refuses it (no D script). CBsloppy (CHK_L, its own produced script): sound readers
  certify it by Run (the sloppy check of their own script returns T), so they cooperate with it; it cooperates with
  every program that has any C entry, including Dcert and CBfake, which exploit it; plain D carries nothing and is
  refused. CBN0 is exploited by CBN (§1.7(a)). LöbC cooperates with everyone.
- **Cost estimate (a guess, not a computation):** a check validates two 5–8 node scripts; each EvR* step and each
  ChkR runs `cstep` on a configuration containing the program body with its list (hundreds of encoded nodes), a few
  hundred to a few thousand L_T steps per node. Guess: 5·10³–3·10⁴ steps per FB-shaped check, up to 6·10⁴ with PB's
  nested D check; all below 10⁵. Fit: K ≥ V + 10 for CB's static boundary (3 steps, u = V + 6, one step after), with
  V = K/4 at every K.

### 1.9 The frozen production procedure, and held-out sources

**Production** is a host procedure (Python, outside any match, not charged): for a program x and a *probe* opponent,
run the following deterministic tactic on ⊢ ψ (ψ = plays_K(x, probe, a), hypotheses R, S of the mode of x's own
checker, cap V), and record the script:

1. Ax if applicable; 2. Hyp on the first right box in {R, S}; 3. RunNeg on the first left box (not R, S; cap ≥ V)
   whose clean run is F or TO; 4. Run on the first right box (same conditions) whose clean run is T; 5. the first
   right atom: EvR* if its next step is deterministic, ChkR if it is at a fitting check call (premise 1 first);
   6. otherwise fail.

The tactic is total on the fragment (every rule except the leaves is applied only to the first eligible formula, and
the formulas that occur are deterministic) and is frozen here: no backtracking, script size bound 64 nodes. Probes
(frozen): CB, then CB1, then CBP (the production set's FB-, FB1- and PB-shaped carriers); D scripts use the probe ⌜D⌝.
Each program's list is the distinct C scripts found against the probes, in probe order, then its D script. Because
programs are built with their lists inside them and Run outcomes depend on the probes' lists, production runs in two
passes: D scripts first (they need nothing), then C scripts against probes that already carry theirs; every produced
script is re-validated by the checker term on the final programs.

**Held-out set** (never used as probes or production inputs): CBlet2 (CB respelled: the argument built in a second
let), CBw2 (a different checker wrapping: `(λf. if f(arg) then C else D) (lib CHK_S)`), CB1h (FB1-shaped, respelled),
CB1r (FB1-shaped, the two calls in the other order), CBPh (PB-shaped, respelled), CBPr (PB-shaped, the D-check
first). For each: (i) does the production-set script of its shape class (CB's, CB1's or CBP's) validate on it when it
carries that script? (ii) the fresh production (the same tactic) and its size and cost; (iii) do production-set
carriers cooperate with it with no new certificate on their side? Hand answers: (i) yes for CBlet2, CBw2, CB1h, CB1r
(a script is a call skeleton, and CB1r's skeleton has the same shape: both calls closed by Hyp); yes for CBPh; **no
for CBPr** (its skeleton has Run on the first call and Hyp on the second); (ii) every one produces a script of the
same size; (iii) yes, always: the production-set carriers' scripts are opponent-generic, so certificate count grows
by at most two per new source (its C and D scripts) and no existing carrier needs a new certificate.

### 1.10 Hand instances and corrupted instances (to be validated by code before any counted cell)

1. **Valid pair:** CB against CB1, K = 10⁶: both checks return T; the replay checker accepts both scripts; each
   check's run ≤ V.
2. **Wrong code:** CBfake carries CB's script: rejected (EvR* reaches ⊥; ChkR finds no call).
3. **Fuel mismatch:** a CB variant naming K′ = 10K in its call (its S differs from the reader's): Hyp^pair not
   applicable; the reader's check F.
4. **Fit violated:** CB at K = V + 9 (static boundary K ≥ V + 10): ChkR's continuation reading is ⊥ on the T-branch;
   the script is invalid; at K = V + 10 it is valid.
5. **Hypothesis not R or S:** a carrier whose call checks a third program (`CHK(⌜CB⌝, me, C)`): its box is neither;
   Hyp rejected; Run would need the third program's check.
6. **Partner validation fails:** CB0 (no list) checking CB: Hyp^pair accepted syntactically, partner validation finds
   no script: F (contrast (a) in mode 1: T).
7. **Run on R or S, or with a smaller cap:** rejected.
8. **Dcert's scripts:** rejected by modes 0, 1, 2, 3, 5; accepted by mode 4.
9. **Naive counterexample** (§1.7(a)): CC_1 accepts; the play shows the atom false.
10. **Lemma Sym, measured:** for every pair in which a check used Hyp^pair, the swap check returns T with the same
    step count when the partner also used Hyp^pair, and no more otherwise.

### 1.11 Code validation of §1.8–1.10, before any counted cell

From `tests/test_lt_cert.py` (16 tests, all passing), run after the code existed and before any counted cell. The
check costs quoted here come from the validation runs (measurements of single checks, not cells).

- **Production reproduces the hand scripts exactly** (K = 10⁶): CB, CBlet, CBwrap, CBN, CBS2, LöbC and SFc carry
  EvR*; ChkR[EvR*; Ax · Hyp] (5 nodes); CB1 EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Hyp] · Hyp] (8); CBP EvR*; ChkR[EvR*;
  ChkR[EvR*; Ax · Run] · Hyp] (8); every carrier's D script EvR*; ChkR[RunNeg · EvR*; Ax] (5); Ccert EvR*; Ax (2);
  SFc's D script EvR*; Ax; CBsloppy EvR*; ChkR[EvR*; Ax · Run] (its call names the sloppy checker, which sound readers
  Run). Held-out fresh productions: CBlet2 and CBw2 get CB's script, CB1h and CB1r get CB1's, CBPh gets CBP's, and
  **CBPr gets EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Hyp] · Run]**, a different call skeleton, as §1.9 derived.
- **A production bug fixed before any cell:** the first version gave the probes only their D scripts, so CBsloppy's
  Run (the sloppy check of a probe's C entry) failed and CBsloppy got no C script. The probes now carry their own C
  scripts (a third production pass, notes §1.9 as written: "probes that already carry theirs"). No other list changed.
- **Instance 1 (valid pair):** CB–CB1 both checks T, the host replay accepts, inner cost 21,542 ≤ V.
- **Instance 2:** CBfake and CBdef rejected against CB, CB1, CBP.
- **Instance 3 (fuel mismatch, K′ = 10K in the call):** the reader's check F, (D, D).
- **Instance 4 (fit):** with V = 25,000 in the sources, CB against itself: F at K = V + 8 and V + 9, T at V + 10 and
  V + 11, and the plays follow the check (D, D, C, C). The flip is at the static boundary because the program's own
  check implements it.
- **Instance 5 (a call on a third program):** Hyp rejected; F.
- **Instance 6 (partner validation):** CB0 checking CB: F (Hyp^pair is syntactically fine; the partner has no
  script). The naive checker on the same shape (CBN0 checking CBN): T, and the plays are CBN0 C, CBN D: **the accepted
  atom is false**, at K = 10⁵ and 10⁶.
- **Instance 7:** Run on S (CB's script with Run in place of Hyp) and on R (LöbC's) rejected; a sloppy carrier whose
  call has cap V/2 is refused by a sound reader (Run cap guard); CBsloppy at cap V accepted.
- **Instance 8 (Dcert):** rejected by modes 0, 1, 2, 3, 5 against CB, CB1, CBP, CBN, CBS2; accepted by mode 4; plain
  D refused by mode 4; CBsloppy plays C against Dcert, CB plays D.
- **Instance 10 (Lemma Sym):** every sampled sound or copy-checker check that closed S (16 sources, both modes): the
  swap check is T, with an equal step count when the partner's script closed R and no more otherwise.
- **The self-interpreter** `cstep` equals the host decomposition (value, stuck, deterministic successor with its
  timeout flag, call state with its library index, argument and frames, and the plugged T/F continuations) along 30
  play chains through check calls and simulation frames.
- **The evaluator** equals the substitution semantics in value and step count on four whole plays at K = 10⁵ (CB–CB,
  CB–CB0, CB–Ccert, CBN0–CBN), the checks run step by step.
- **The cost bound:** a wrapper call costs exactly W + 6 ≤ V + 6 (W the inner steps), also when the core times out.
- **Checker term against host replay:** every (target, opponent, outcome, mode) over the arm-S catalogue at K = 10⁶,
  all six modes, wherever the term finished: equal.
- **Host replay budget:** the host replay counts no fuel, so its EvR* is bounded by V/20 depth-weighted steps; the
  test confirms that one interpreted step at context depth d costs the term at least 20(1 + d) evaluator steps
  (sampled along SFc–SFc, SFc–CB, CB–CB1, CBP–CB and SF–SF chains), so a host abort implies a term timeout. Found
  necessary because SFc's script against SFc steps through a regress of simulations for up to K steps.
- **Fuzz audit (validation size):** 14 random carrier-like codes per mode with random and produced scripts, every
  ordered pair and outcome (512 checks per mode): accepted 99 / 66 / 103 / 112 / 90 in modes 0 / 1 / 2 / 3 / 5, false
  atoms accepted 0 in every mode (the naive checker's false atom needs a carrier paired with a script-less reader that
  runs the same checker, which random codes rarely produce; the designed counterexample is instance 6).

## 2. Implementation and costs

### 2.1 How it runs

`src/lt_cert.py` appends the K_T^cert library to milestone 3's (milestone 3's indices and terms unchanged except the
constant NLIB) and installs it into `lt_code`'s evaluator; the check cores are registered as deterministic cores, so
milestone 3's core-run cache and regress lemma apply to them unchanged (both exact under the cap guard, notes §1.6).
The host replay checker (`HostCheck`) is written from the rule table of §1.5 over the reference stepper with its own
call-state decomposition; it counts no fuel, emulates nested checks recursively (a key already on its stack aborts the
outermost check, as the term's regress does under cap monotonicity) and bounds EvR* by V/20 depth-weighted steps, a
bound below the term's cost (tested). Production (`Producer`) is the frozen tactic of §1.9 on the host.

### 2.2 Costs (runs/certificates-as-code.md §1; K = 10⁷)

| check (reader checks the target's script) | inner steps W | first K with V = K/4 |
|---|---|---|
| CB by CB (twin; one validation) | 8,782 | 35,128 |
| CB1 by CB1 (twin) | 12,757 | |
| CB by CB1 and CB1 by CB (pair; two validations) | 21,541 | 86,164 |
| CB by CBP and CBP by CB (two validations, one nested D check) | 30,491 | 121,964 |
| CB1 by CBP and CBP by CB1 | 37,140 | 148,563 |
| CBP by CBP (twin, nested D check) | 24,388 | 97,554 |
| Ccert by any sound reader (acyclic, 2 nodes) | 2,065 | |

A check costs W + 6 steps of its caller. The largest check returning T in any cell is 50,986 (CB1r checked by CBPh).
Checking a pair costs about 2× a twin's single validation, plus a nested 10⁴-step check per PB-shaped side. Against
milestone 3: FairBot's self-proof by search cost 1.1·10⁵ and PrudentBot's 9·10⁵, and distinct sources never finished;
here every distinct pair finishes in 2–4·10⁴ (a pair of FB-shaped carriers from K ≈ 8.6·10⁴). Scripts are 2–8 nodes,
two per carrier, ≈ 40–60 term nodes of storage per list, and production is 20–29 tactic nodes and at most 7 host check
emulations per source.
