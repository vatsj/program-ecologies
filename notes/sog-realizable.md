# The social organization game over the realizable language (notes, 2026-10-10)

Spec `specs/2026-10-10-sog-realizable.md` (reviewed by gpt-6.1-sol; the [after review] text is the resolution).
§1.1–1.3 are written before any code of this experiment and before any counted cell: the three-quote extension of
milestone 4's checker and tactic with every rule's obligation, the shared predicate of mutual checks, Theorem
S^cert₃ with the timeout and substitution lemmas, the corrupted-instance plan, the grammar of both roles with the
named classes and their hand plays, the prior as a source distribution with the expanded-syntax encoding, and the
frozen lottery and chain conventions. §1.4 (static invasion analysis) is written after the predictions file is
committed; §1.x (code validation) after the code exists and before any counted cell; §2 (costs) after that.

Base: `notes/certificates-as-code.md` §1 ("milestone 4": L_T^code, check boxes, Lemma N, Lemma Sym, Theorem S^cert,
the frozen tactic), `notes/prover-as-code.md` §1 ("milestone 3": fuel rules, Lemma M, the regress lemma),
`notes/carrier-populations.md` §1 ("milestone 2": templates compiled to carriers, composition of clean check values,
`ExactHost`), RESULTS "The union game", "Incentive-compatible enforcement", "The social organization game under the
seed lottery", "Concessions" (the game, payoffs, CC/RR, lottery conventions).

*Disclosure.* Before writing this section I ran a scratch enumeration of the two template grammars (sizes, run
trees, raw truth tables; nothing about plays) to decide which computation of the three-player table is feasible.
The counts are quoted in §1.3.

## 1. Design

### 1.0 Readings of the spec, stated before any code

- **The game** is the committed social organization game of RESULTS "The union game" with the union run's three
  whack policies: boss action b = 3·si + hi, wage s = si/4 ∈ {0, ¼, ½}, policy hi ∈ {0 strike-targeting, 1 none,
  2 source-targeting}; c = 0.5, L = 1; payoffs `union.payoff_table(0.5)`. The spec's "h ∈ {none, 1, 2}" is read as
  these three policies, since the spec counts 9 boss constants and names the whacker `pay(0, strike-targeting)`.
  *Tag* (what source targeting reads): a worker is tagged iff its template contains an atom about the other worker
  (the realizable analogue of "QUORUM is an essential atom").
- **Run forms.** Boss `b ⌜b⌝ ⌜w1⌝ ⌜w2⌝`; worker in slot j: `w ⌜w⌝ ⌜b⌝ ⌜o⌝`. Sources are milestone 4's carriers with
  three abstractions: `λme. λx. λy. (λcerts. BODY) CERTS`. Outputs: the boss returns the natural 3si + hi; a worker
  returns the constructor `C` (work) or `D` (strike). Each run has fuel K = 10⁶; a run that ends without a value of
  its role (global fuel exhausted, stuck, wrong value) plays the **default**: boss `pay(0, none)` (code 1), worker
  `work`. Defaults are recorded.
- **Slots are absolute.** As in the union run ("absolute slot labels are filled in per slot"), a worker template is
  compiled once per slot: the slot-j compilation builds every encounter it asks about in slot order
  (`(b, me, o)` for j = 1, `(b, o, me)` for j = 2). The two slot populations are separate, so a slot-1 program never
  meets a slot-1 program; the same template has the same prior in both slots.
- **The boss grammar reads probes only**: the spec's boss grammar is "`if(B, A, A)` over probe atoms about w1 and
  w2", with the 9 constants as leaves ("the `whack(j)` outputs" read as the whack component of the leaves). Unlike
  the modal P₀₁, there is no current-encounter boss atom (`BOX(W_j = a)`); the current-encounter concession C₁ is
  analysed by hand as an out-of-grammar program (§1.2.6).

### 1.1 The three-quote extension: language, rules, obligations, production

#### 1.1.1 Library entries

Appended to milestone 4's library (milestone 4's and milestone 3's indices unchanged; milestone 4's `iswrap` is
redefined in place to also recognize the new wrappers, so the check-aware self-interpreter `cstep` stops at their
calls; nothing else of milestone 4 changes):

- **Wrappers** `CHK3 = λarg. if eq(capk(fst arg, CC3, arg), T) then T else F` (sound) and `CHK3N` (the same over
  `CC3N`, the naive control). A call costs at most u(V) = V + 6 steps, exactly W + 6 when the core returns after W
  inner steps (milestone 4's accounting, unchanged).
- **Argument** arg = (V, (enc, (j, (A, K)))): V the cap, **enc = (⌜b⌝, (⌜w1⌝, ⌜w2⌝))** an encounter of three quotes,
  **j ∈ {0, 1, 2} the subject** (0 the boss, 1 and 2 the workers), **A a non-empty list of outcome values** (the
  outcome set), K the subject's fuel.
- **Root.** conf₀(enc) = `b ⌜b⌝ ⌜w1⌝ ⌜w2⌝`, conf₁(enc) = `w1 ⌜w1⌝ ⌜b⌝ ⌜w2⌝`, conf₂(enc) = `w2 ⌜w2⌝ ⌜b⌝ ⌜w1⌝`.
  ψ(arg) = ⟨conf_j(enc), K⟩⇓A: the run returns a value in A within K steps (exact atom, m = 0).
- **Box** ⊡₃(arg) = (8, (n₃, arg)) (n₃ the wrapper's library index): *the clean run of capk(V, CC3, arg) returns T*,
  a fact about a finite run. The **encounter** of a box is e(arg) = (V, enc, K). The **encounter boxes** of a box X
  are the boxes with X's wrapper and X's encounter (any subject, any outcome set, X itself included).
- **Extraction** `getcerts3(t)`: tag λ, tag λ, tag λ, tag app with a λ function part; the argument's encoding,
  converted by `full`, is the certificate list; anything else carries nothing. Entries are (A′, script); an entry
  answers a question about outcome set A iff A′ = A as data.
- **Outcome sets used.** Workers are asked `[C]` (works) and `[D]` (strikes). The boss is asked `≥¼ = [3..8]`,
  `=½ = [6, 7, 8]`, `≤¼ = [0..5]` (lists of action codes in increasing order).

#### 1.1.2 Formulas and truth

As milestone 4 §1.3 with the outcome set in place of the outcome: atom ⟨σ, f⟩⇓^m A = (6, (σ̂, (f, (A, m)))) is true
iff the run of σ under fuel f (with milestone 3's ⇓⁺ conditions for m = 1) returns a value v with v ∈ A. Check
boxes as above. A sequent Γ ⊢ Δ is true iff ∧Γ → ∨Δ.

#### 1.1.3 The rules of K₃ (validating a box X with argument x; R_X = ⊡₃(x) its own root)

| rule | code | conclusion | premises | side condition | obligation |
|---|---|---|---|---|---|
| Ax | 0 | Γ ⊢ Δ | — | ⊥ ∈ Γ, ⊤ ∈ Δ, or an atom/box in both *(syntactic)* | trivial |
| EvR* | 26 | Γ ⊢ A, Δ | Γ ⊢ φ, Δ | milestone 4's EvR*, stopping at a value v with ⊤ iff v ∈ A *(syntactic)* | milestone 3's (E1), iterated |
| ChkR | 25 | Γ ⊢ A, Δ, A at a call state E[app(lib CHK3 or CHK3N, v)] | Γ, B ⊢ ρ_T, Δ and Γ ⊢ B, ρ_F, Δ | v a pair with first component a natural V′; fit f ≥ V′ + 6 and every enclosing sim fuel ≥ V′ + 6; B = ⊡(full v); readings at A *(syntactic)* | (E2^cert) with Lemma N₃ |
| Run | 1 | Γ ⊢ B, Δ | — | B a CHK3/CHK3N box, **B ≠ R_X**, cap V_B ≥ V_X, and its clean run returns T *(computational)* | B's truth (Lemma N₃(b)) |
| RunNeg | 2 | Γ, B ⊢ Δ | — | as Run; the clean run returns F or TO | B's falsity (Lemma N₃(b)) |
| Hyp | 3 | Γ ⊢ B, Δ | — | **B an encounter box of X** (same wrapper, V, enc, K; any subject and outcome set) *(syntactic)*; B is recorded as *used* | **Lemma Sym₃** (mode 0); none in mode 1 |

Two differences from milestone 4, both forced by three subjects. (i) **Hyp closes any encounter box, not one swap
box.** Milestone 4's S = swap(R) exists because two programs ask each other the *same* question; here a worker asks
the boss about a wage set and the other worker about an action, and a boss (outside this grammar) could ask each
worker something else, so no single "partner" box is canonical. The guard is the *closure* (below), not a fixed
partner. (ii) **Run/RunNeg may apply to encounter boxes** (any box but the validated box's own root). Milestone 4
excluded R and S from Run because they were exactly its Hyp-able boxes; here forbidding Run on every encounter box
would make a militant's strike against a low-paying boss uncertifiable (its strike is reached through a failed
check of the boss, which only RunNeg closes), which kills every probe. §1.2 shows that allowing both on the same
box is sound: a closure that Hyp-uses a box and also RunNegs it dies by a regress.

**The check (mode 0, `CC3`).** Validate the root X: try X's entries for its outcome set in list order; the first
entry whose script satisfies the rule table (syntactic side conditions, Run/RunNeg clean values) is *selected*;
none → F. Then the **closure**: every box Hyp-used by a selected script is validated the same way (its own first
valid entry, its own encounter boxes as hypotheses), transitively; T iff every box of the closure has a selected
entry. Bookkeeping is **uniform-cost**: the set of validated boxes is a fixed-capacity list of M = 8 slots, every
membership test scans all M slots, insertion fills the next slot, a worklist is a stack onto which each selected
script's used boxes are pushed; a closure of more than M boxes is F. (In this catalogue a closure has at most 7
boxes: 2 worker subjects × 2 action sets + 3 wage sets.) **Mode 1 (`CC3N`, naive):** the root's validation only,
no closure (milestone 4's unguarded rule, as a control).

#### 1.1.4 Production: the path tactic

Milestone 4's frozen tactic chooses rules by box *values* against probe opponents, in the priority order Ax, Hyp,
RunNeg, Run, EvR*/ChkR. Two things change in a three-player encounter. Every same-encounter box is Hyp-able, so the
frozen priority would close the F-premise of every encounter call by Hyp and never follow an F-branch; and probe
opponents would make certification depend on the probe set. Production is therefore **the frozen tactic driven by
an assignment instead of by probes** (public, uncharged, DEFERRED 11's operating hypothesis):

for each outcome set A in the role's question family and each assignment α of truth values to the program's atoms
(atoms in source order, assignments in binary order, T before F), follow the run from the root: EvR* to the next
call; at a call with box B, ChkR, and
- if α(B) = T: premise 1 continues on ρ_T; premise 2 closes B on the right by **Hyp if B is an encounter box about a
  worker** (subject 1 or 2), and by **Run otherwise** (a box about the boss, or a box of another encounter);
- if α(B) = F: premise 1 closes B on the left by **RunNeg**; premise 2 continues on ρ_F;
- at a value: Ax if it is in A (⊤), else no script for this (A, α).

The list holds the distinct scripts found, **ordered by the number of Hyp nodes (grounded scripts first), then by
α**, then the role's entries in the order of its question family. Lists depend only on the template (the scripts
are opponent-generic: positions and rule names do not depend on the quotes in the encounter), so a run tree has one
list. Hyp is used only where the dependence can be cyclic: in this grammar the only cycles are between the two
workers of one encounter (bosses read probes, which are other encounters). The quoted probe constants
⌜pay(s′, none)⌝ carry their own produced lists (EvR*; Ax for every wage set containing their code).

### 1.2 Soundness

#### 1.2.1 Lemma N₃ (in-context runs are clean runs)

Milestone 4's Lemma N, unchanged in statement and proof: cap monotonicity (every Run/RunNeg box has cap ≥ the
validated box's cap, so every check frame nested in a root has a later deadline than the root), fit at ChkR in
plays, and the regress lemma give: (a) a nested check returns its clean value or an enclosing frame times out
first; (b) in a check whose root returns T no regress occurred anywhere inside it and every nested run returned its
clean value. *Corollary:* the in-play value of a check call is its box's truth. The closure adds no frames: the
validations of the closure are ordinary computations inside the root's frame, and only Run/RunNeg (and ChkR in
plays) create frames. **Every regress anywhere inside a root kills the root** (the regress fast-forwards to the
earliest enclosing deadline, the root's), and a nested check that times out costs at least V ≥ the root's remaining
budget, so inside a root that returns T every RunNeg saw the clean value F, never TO.

#### 1.2.2 The shared predicate of mutual checks

For a box Y of encounter e let sel(Y) be its first entry valid under the rule table (Hyp syntactic, Run/RunNeg on
clean values; a function of Y alone) and used(Y) the encounter boxes sel(Y) Hyp-closes. The check of X computes

  **Φ(X) = [every Y ∈ H*(X) has sel(Y)]**, H*(X) = the reflexive-transitive closure of `used` from X.

Two checks X, X′ of one encounter compute *one* predicate whenever each is in the other's closure: then
H*(X) = H*(X′) and Φ(X) = Φ(X′). If X′ ∈ H*(X) only, Φ(X) ⇒ Φ(X′). This is the exact form of milestone 4's "the two
checks are the same computation": the boss's check of a worker and the worker's check of the boss are *not* mutual
in this grammar (a boss asks about a different encounter); two workers asking about each other in one encounter
are, and they compute Φ over the same closure.

#### 1.2.3 Lemma Sym₃

*If the clean run of CC3 on x returns T within V, then for every Y in the closure it computed, the clean run of
CC3 on Y returns T within V.*

*Proof.* (Values.) sel and used are functions of a box, so H*(Y) ⊆ H*(x), and every member of H*(Y) has a selected
entry; the run on Y (call it ρ_Y) validates exactly H*(Y). It remains to show that every validation inside ρ_Y
behaves as inside ρ_x. The two contexts differ only by the root frame's key (κ_Y against κ_x). (1) No nested call
inside ρ_x has key κ_x (Lemma N₃(b)). (2) Suppose some nested computation inside ρ_Y reaches a call with key κ_Y
(the only way ρ_Y can differ: a regress on its own key). Its chain starts at a Run/RunNeg W made by the validation
of some Z ∈ H*(Y). The same validation runs inside ρ_x (Z ∈ H*(x)), makes the same call W, and W's computation
reaches the same κ_Y call, which inside ρ_x starts a nested Y-check frame (κ_Y is not on ρ_x's stack). That frame
validates H*(Y): by (b) every nested value inside ρ_x is the clean one, so these validations succeed as at ρ_x's top
level and in particular the frame reaches Z's validation and its call W, whose key is now on the stack: a regress,
which kills ρ_x's root. Contradiction. The case W = Y (Z Runs Y directly) is the same argument with an empty chain.
(3) Calls with keys of other frames on ρ_Y's stack are calls nested in the same validations in both contexts. So
every validation of ρ_Y returns as in ρ_x, and Φ(Y) holds.
(Cost.) ρ_Y's steps are: the validations of H*(Y) (each the same computation as in ρ_x, so the same steps), plus
bookkeeping. Each pop of the worklist costs the same fixed scan of M slots whatever the set's contents; insertions
cost 0 + 1 + … + (|H*| − 1) slot traversals, a function of |H*| only; pushes cost the size of each used list. The
number of pops is 1 + Σ_{Z ∈ H*} |used(Z)|. Each of these is monotone in the closure, and H*(Y) ⊆ H*(x), so
steps(ρ_Y) ≤ steps(ρ_x) ≤ V. ∎

This is why the bookkeeping is uniform: with an early-exit membership test, the order in which a closure is visited
(which depends on the root) changes the cost, and a partner check could exceed V where the root did not.

#### 1.2.4 Theorem S^cert₃ (unconditional soundness)

*For every arg = (V, (enc, (j, (A, K)))) with arbitrary quotes in enc, if the clean run of capk(V, CC3, arg) returns
T, then ψ(arg) is true: the actual fuel-bounded run of conf_j(enc) under K returns a value in A.*

*Proof.* The run returned T, so (Lemma C₃: the code implements §1.1.3) every Y in its closure has a selected script
whose syntactic side conditions hold at every node, whose Run/RunNeg side conditions held in the run, and whose Hyp
nodes close encounter boxes of Y that are in the closure. By Lemma Sym₃ every box in the closure is true. By strong
induction on expanded size, every sequent of every selected script is true: Ax and EvR* as in milestone 3 (EvR* with
set membership at values); ChkR by (E2^cert) and Lemma N₃; Run/RunNeg because inside a T-returning root nested runs
return clean values (Lemma N₃(b)); Hyp because the closed box is in the closure, hence true. The root sequent ⊢ ψ(x)
is therefore true. ∎ It holds for CC3 and fails for CC3N (Hyp without the closure; counterexample §1.2.6(d)).

*What it says, exactly:* the accepted atom is about **the actual fuel-bounded run of the subject on the quotes in
the argument**. It says nothing about any other encounter. Whether that encounter is the one being played is a
property of the program that built the argument (Lemma Sub below), not of the checker.

#### 1.2.5 Timeout safety and substitution safety

**Lemma TO (timeouts).** (a) ψ requires a value in A within K; a run that times out has no value, so no timed-out
run is ever certified (by S^cert₃): a militant that times out is never *certified* to work or strike. (b) In a play,
a run that times out plays the role's default (worker: work; boss: pay(0, none)). (c) For every program of the
catalogue (§1.3: at most 3 check calls per run, each costing at most V + 6 = 250,006, plus fewer than 10³ other
steps), a run needs at most 3V + 10³ < K = 4V steps, and every call fits (f ≥ V + 6 at each call: at most two
earlier calls). So **no catalogue run times out globally**; timeouts occur only inside checks (a check exceeding V
returns F, so its caller takes the F-branch). (d) Hence a low-wage work by timeout requires a program outside the
catalogue (≥ 4 calls), and the report classifies every low-wage work as: *false certificate* (the work leaf reached
through a T check whose atom is false: impossible by S^cert₃), *timeout* (a global timeout default), *substitution*
(the work leaf reached through a T check about an encounter other than the actual one), or *uncertified default*
(the work leaf reached through an F-branch: the worker works because a check failed, e.g. "strike iff certified
low" against a boss whose low wage is not certified).

**Lemma Sub (substitution).** Every check call a slot-j worker template makes is about the encounter
(⌜b⌝, ⌜w1⌝, ⌜w2⌝) in slot order, which is the actual encounter, because the compiled call builds enc from the
program's own three arguments in its slot's order. Every boss check is a probe about (⌜pay(s′, none)⌝, ⌜w1⌝, ⌜w2⌝),
an encounter different from the actual one, and is used by the boss as a probe (a counterfactual), never by a worker.
Hence **no worker's action in the catalogue rests on a certificate about a non-actual encounter**, and substitution
low-wage work is zero by construction. The design hazards it guards against are tested as corrupted instances
(§1.2.6): a slot-misordered compilation, and a certificate valid for a quoted constant opponent presented for the
actual one.

**Lemma 0₃ (the militant cannot be faked).** A worker whose every work leaf lies on the T-branch of a wage check
`CHK3(enc, 0, A)` with A ⊆ {wages ≥ s} works only if its boss is certified, hence (S^cert₃) actually pays, at least s
in the actual encounter (Lemma Sub), or by a global timeout (impossible in the catalogue, Lemma TO(c)). So no boss
class gets work below s from it.

#### 1.2.6 Trying to break it: the corrupted instances (to be validated by code before any counted cell)

1. **Slot-2 ordering.** (a) D\* (reading w1) against (T₁, scab) pays ½; D\*'s =½ script, accepted for the encounter
   (D\*, T₁, scab), is rejected for (D\*, scab, T₁) (its Run on the probe box about w1 = scab fails), by the checker
   term and the host replay. (b) A *misordered* T₁ (the slot-1 compilation placed in slot 2) against (D\*, scab, ·)
   asks about (D\*, T₁, scab), is certified ½ there, and works at the actual wage 0: low-wage work by
   **substitution**, the checker sound. The correctly compiled T₁ in slot 2 strikes.
2. **Opponent substitution.** (a) T₁'s strike script (valid in (⌜pay(0, none)⌝, T₁, ·) and (⌜pay(¼, none)⌝, T₁, ·):
   RunNeg on the boss's =½ box) is rejected for (pay(½, none), T₁, ·), where its RunNeg fails. (b) D\*'s =½ script,
   valid in (D\*, T₁, T₁), is rejected in (D\*, scab, scab) (Run on a false probe box).
3. **Unequal branches.** (a) A script whose ChkR premises are exchanged (the T-continuation's closing put on the
   F-premise) is rejected. (b) A script claiming the T-leaf where the run takes the F-branch (Run on a false box) is
   rejected; one claiming the F-leaf where the box is true (RunNeg on a true box) is rejected. (c) An *unequal*
   mutual pair: x = `if(O:S, strike, work)` against y = `if(O:W, work, strike)` (x asks "y strikes", y asks "x works"):
   every check either returns its atom's truth or is F; no accepted atom is false.
   (d) **The naive control:** QN = `if(CHK3N(o strikes), strike, work)` carrying its list, against QN0 (same code, no
   list). QN0 asks "QN strikes": QN's strike script Hyp-closes "QN0 strikes" without validation: T, so QN0 strikes;
   QN asks "QN0 strikes": no list, F, QN works. The accepted atom "QN strikes" is **false**. The sound version (CC3 on
   the same shapes) validates QN0's absent script: F, both work.
4. **Exhausted fuel.** (a) Fit: a worker compiled with V and run at K = V + 9 (the static boundary of milestone 4)
   gets no valid script (ChkR inapplicable); at K = V + 10 it does. (b) A check whose closure exceeds the cap
   (V too small for the nested Runs) returns F, and the caller takes the F-branch. (c) An out-of-catalogue militant
   with four sequential wage checks exceeds K = 4V: global timeout, default work at a low wage, classified as
   **timeout**. (d) An atom asked at fuel K′ below the subject's actual run length is rejected (EvR* reaches f = 0).
5. **Regress through a mixed closure.** x = `if(O:S, strike, work)`, y = `if(O:W, work, strike)`: "x strikes"
   Hyp-uses "y strikes", whose script RunNegs "x works", whose script RunNegs "y strikes": the nested frame meets
   its own key and the root dies. Expected: every check of this pair returns F or its atom's truth; none is accepted
   false.
6. **Out-of-grammar C₁** = `if(CHK3(w1 strikes in this encounter), pay(½, none), pay(0, none))` against (T₁, T₁): T₁'s
   strike is reached only through RunNeg on the boss's =½ box; inside the boss's check that box's own check is on
   the stack, so the closure regresses: no strike certificate, C₁ pays 0, T₁ strikes: **(pay 0, strike, strike)**,
   not the modal (pay 0, work). Probes and current-encounter reads have no world 0: there is no world-0 faker.

### 1.3 Grammar, named classes, prior

#### 1.3.1 Grammar (both roles; cutoff n = 7, prespecified; n = 6 is a different experiment)

Milestone 2's template form: **A ::= leaf | if(B, A, A); B ::= atom | not(B) | and(B, B) | or(B, B)**; one node per
leaf, atom and connective; compiled as milestone 2 (`not(B)` = `if B then F else T`, `and`, `or` as `if` chains), the
atom the call `app(lib CHK3, (V, (enc, (j, (A, K)))))` with V = ⌊K/4⌋ = 250,000, K = 10⁶.

**Workers** (leaves `work`, `strike`; 5 atoms, all about the actual encounter):
`B≥¼` = CHK3(enc, 0, ≥¼), `B½` = CHK3(enc, 0, =½), `B≤¼` = CHK3(enc, 0, ≤¼) ("the boss is certified to pay me a
wage in the set" — one wage per encounter, paid to every working worker); `O:S` = CHK3(enc, o, [D]),
`O:W` = CHK3(enc, o, [C]) ("the other worker is certified to strike / work in this encounter").
Counts by node shell n = 1, 4, 5, 6, 7: 2, 20, 20, 220, 1,020; **1,282 spellings, 422 run trees, 264 of them with
an O-atom** (scratch count).

**Bosses** (leaves the 9 constants `pay(s, h)`; 8 probe atoms):
`P_j^{s′}:a` = CHK3((⌜pay(s′, none)⌝, ⌜w1⌝, ⌜w2⌝), j, [a]) for j ∈ {1, 2}, s′ ∈ {0, ¼}, a ∈ {work, strike}: "worker j
is certified to do a against a boss paying s′ (no whack), beside the other actual worker".
Counts: 9, 648, 648, 11,016, 125,064; **137,385 spellings, 93,969 run trees, 69,453 truth tables** over the atoms
each reads (scratch count).

Every template makes at most 3 check calls (three atoms need `and(·, and(·, ·))` or the nested-if form: 7 nodes).

#### 1.3.2 Exact lumping, by lemmas (identity-aware)

Classes must be interaction-preserving: no program of either role's catalogue distinguishes two merged sources,
within-class plays included. With separate slot populations there are no within-slot plays (a slot-1 program never
meets a slot-1 program), so the condition is on cross-slot interactions only. Three lemmas make it computable.

- **Lemma T₃ (τ-symmetry).** Spellings with the same run tree (hence the same produced list) are interchangeable:
  replacing one by the other in every quote of every encounter leaves every check value unchanged (milestone 2's
  Lemma T: checks consult quotes only through the self-interpreter's steps, `getcerts3`, and syntactic box equality,
  all preserved by a bijection on quotes; the three quotes of an encounter are never equal across roles, and the
  only coincidence across worker slots is the constant `work`/`strike`, whose boxes differ by the subject index).
- **Lemma B (probe-only bosses).** A boss's play against (w1, w2) depends on the workers only through the probe vector
  P(w1, w2) ∈ {T, F, TO}⁸ (the clean values of its 8 possible atoms; its own run reads TO as F, the wrapper's
  convention). *What workers can learn about the boss is its action, or nothing*: under the path tactic every T-node
  of a boss script is closed by Run on a probe box and every F-node by RunNeg, and no boss script Hyp-closes
  anything. If no probe on the boss's actual path is TO, the actual path's script is valid and every valid script is
  true, so `CHK3(enc, 0, A)` = [action ∈ A]. If some probe on the actual path is TO, the RunNeg on it kills every
  check of the boss (a nested TO costs the whole cap: Lemma N₃), so every `CHK3(enc, 0, A)` is TO: the boss is
  *uncertifiable* in that encounter. Probe boxes belong to another encounter and never involve the actual one.
  Hence a boss's interaction with a worker pair is the pair (action, certifiable) as a function of the probe code,
  and two bosses with the same pair on every probe code *realized by a worker pair of the catalogue* are
  indistinguishable: **boss classes are maps from realized ternary probe codes to (action, certifiable).**
- **Lemma W (boss-only workers).** A worker template with only wage atoms has, under the path tactic, only grounded
  scripts (Run/RunNeg on boss boxes). Against a certifiable boss its actual path's script is valid and every valid
  script is true, so it is certified exactly for its action, and its action is a function of the wage alone (its
  wage function (a₀, a¼, a½) ∈ {W, S}³); against an uncertifiable boss every check is TO, so it takes its all-F leaf
  and is itself uncertifiable. So boss-only workers have at most 16 behaviours (wage function × all-F leaf).
  **Lumping is computed, not assumed:** every worker run tree is a candidate class, and two are merged iff their
  full interaction tables (below, all ten boss columns, ternary certification, tag) agree; Lemma W predicts the
  result for boss-only workers and is checked against it. Tagged workers are never merged with untagged ones.
- **Lemma F₃ (factorization).** Against a probe-only boss b, a worker pair's play (actions and certification) equals
  its play against the constant boss pay(a) if b is certifiable with action a, and against an *uncertifiable boss*
  (every boss check TO) otherwise: the workers see the boss only through `CHK3(enc, 0, A)` (Lemma B), and the boss's
  probes involve no box of the actual encounter. So **the three-player table is J(b, x, y) = (a, E_κ(x, y))** with
  (a, cert) = b(P(x, y)) and κ = a if cert else ⊥, where E_κ(x, y) (κ one of the 9 constants or ⊥) is the
  worker-pair table: both actions and the ternary certification values of `[C]` and `[D]` for both workers. P(x, y) is
  read off E_{pay(0, none)} and E_{pay(¼, none)}. The play table by composition is validated against whole runs
  (§1.x).

The table is therefore lazy in the boss slot: E is computed once for every pair of worker run trees (422² pairs ×
10 columns, by slot symmetry once), and a triple's play is two table lookups. No truncation by mass anywhere.

#### 1.3.3 Named classes and hand plays (CC)

**Bosses.** The 9 constants; **D₀** = `if(P_1^0:S, pay(½, none), pay(0, none))` (4 nodes); **D₀q** (the same paying
¼); **D14** = `if(P_1^¼:S, pay(½, none), pay(0, none))` (4); **D\*** = `if(P_1^¼:S, pay(½, none), if(P_1^0:S,
pay(¼, none), pay(0, none)))` (7); **D14₂** = `if(and(P_1^¼:S, P_2^¼:S), pay(½, none), pay(0, none))` (6, the
both-slot concession that fits); **D\*₂** = `if(and(P_1^¼:S, P_2^¼:S), pay(½, none), if(and(P_1^0:S, P_2^0:S),
pay(¼, none), pay(0, none)))` (**11 nodes: does not fit n = 7**; kept as a named out-of-catalogue class with zero
prior mass, used only in the forced cells); **WF** = `if(P_1^0:W, pay(½, none), pay(0, none))` (the modal probe
wage faker's spelling); the whacker `pay(0, strike)`.

**Workers.** scab = `work`; striker = `strike`; **T₁** = `if(B½, work, strike)` (the militant; "strike unless
certified fair", so militant⁻ is the same program, as the spec notes; wage function S S W); **T₀** = `if(B≥¼, work,
strike)` (S W W); **R** = `if(B≤¼, strike, work)` ("strike iff certified low", the modal militant's polarity; wage
function S S W, the same class as T₁ by Lemma W); **Q** = `if(O:S, strike, work)` (quorum-type, tagged);
**U** = `if(B½, work, if(O:S, strike, work))` (7 nodes, a tagged union).

Hand plays (boss action; W1, W2), from the rules and the path tactic:

| encounter | play | why |
|---|---|---|
| (D\*, T₁, T₁) **F\*** | (½, none; W, W) | T₁ strikes against ⌜pay(¼)⌝ (RunNeg on the constant's false =½ box), so P_1^¼:S; T₁'s =½ check of D\* Runs D\*'s path script, whose Run on the probe box is T |
| (D\*, T₀, T₀) | (¼, none; W, W) | T₀ works at ¼, strikes at 0 |
| (D\*, scab, scab) | (0, none; W, W) | scab never strikes |
| (D\*, T₁, scab) | (½, none; W, W) | **the one-slot leak**: D\* reads only w1 |
| (D\*, scab, T₁) | (0, none; W, S) | w1 = scab, so D\* pays 0 |
| (D₀, T₀, T₀) | (½, none; W, W) | T₀ strikes at 0; pay(¼, none) then gets 1.5 > 1: the ratchet |
| (WF, T₁, T₁) | (0, none; S, S) | T₁ is certified to strike at 0, so P_1^0:W is false: **no probe wage faker** |
| (pay(½, ·), T₁, scab) | (½; W, W) | |
| (b, Q, Q), any b | (b; S, S) | Q's strike script Hyp-closes "the other strikes", whose script Hyp-closes it back: the closure validates; Q's work script RunNegs a true box |
| (b, Q, scab) | (b; W, W) | scab has no strike entry: Q's RunNeg holds, Q certified to work |
| (b, U, U) | (½: W, W; lower: S, S) | U works iff certified ½, else the strike pact (as Q) |
| (b, R, R) | as T₁ against certifiable bosses | Lemma W: certification is exact, so polarity does not matter against certifiable probe-only bosses; against an uncertifiable boss R works (its all-F leaf) and T₁ strikes |

**Invasion structure by hand (CC).** F\* has **no strict invader**: the boss's best payoff against (T₁, T₁) is 1
(T₁ works only at ½); no worker earns more than ½. Its neutral substitutes: any boss paying ½ to the T₁ pair
(constant ½ bosses, D14, …), any slot-1 worker certified to strike against ⌜pay(¼)⌝ and working at ½, and **in the
unread slot 2 anything that works at ½, the scab first (the one-slot leak)**. After the scab fixes in slot 2,
(D\*, T₁, scab) is neutrally entered by pay(0, none) (T₁ strikes, the scab works: 1 = 1), not strictly: the boss's
cut is neutral here, where the modal run had a strict cut. (D₀, T₀, T₀) is strictly invaded by pay(¼, none)
(+0.5, the ratchet); at (D\*, T₀, T₀) a T₁ in the read slot strictly invades (+¼). With D\*₂ the unread slot's scab
is deleterious (D\*₂ pays 0 unless both are certified to strike at ¼). The **unfakeable fair state** the spec names
(D\*-type with militant⁻ in both slots) is F\* itself, since militant⁻ = T₁ here.

#### 1.3.4 RR, derived before any RR cell

RR (both sides ex post rational, `union_enforcement.override` without pool): the boss's whack is overridden to
`none` (whacking costs c and gains nothing); each worker's *executed* action best-responds to the implemented boss
action (s, none): work if s > 0; at s = 0 work and strike tie at 0 and the recommendation is kept. **Realizable
semantics:** every certificate is about a program's run, i.e. about recommendations; the override is the
evaluator's and is not a run of any program. So probes certify recommendations, and the boss's wage (its stage-1
choice) is its program's output. Consequences by hand: D\* pays ½ to a T₁ pair (whose *recommendation* at ¼ is
strike), and the T₁ pair executes work at ½; but **pay(¼, ·) strictly invades F\* under RR** (rational workers
execute work at ¼: boss 1.5 > 1), and pay(0) against T₁ pairs gets 0 (they keep their strike recommendation at 0).
So the 1/4 probe certifies militants' *recommendations*, which bind nothing at s = ¼: in the sense of prediction 6
the probe "certifies rational workers" (their recommendation), the condition of prediction 6 fails, and the
prediction is void with the derived table as the result. Expected RR π and lottery: the 1/4 wage, as in the modal
and enforcement runs. **Modal-matched variant (labelled extra cell):** probes read *executed* actions in the quoted
encounter (at s′ = ¼ every worker executes work, so P_j^¼:S is false for every worker; at s′ = 0 the recommendation
stands); then D\* pays ¼ to T₁ pairs and the prediction's condition holds.

#### 1.3.5 The prior as a source distribution, and the expanded-syntax encoding

- **L (main):** every spelling (source) of a role's catalogue has weight 2^−nodes, normalized per role:
  Z_W = 2/2 + 20/16 + 20/32 + 220/64 + 1020/128 = 14.281; Z_B = 9/2 + 648/16 + 648/32 + 11016/64 + 125064/128 =
  1,214.44. A class's mass is the sum over its spellings (aggregated); the *representative-length* mass is
  2^−(fewest nodes of a member)/Z. Spellings are kept as the seed draw; a spelling's class is its exact lumping class,
  so class counts are exact sums of spelling counts (the twin-expanded distribution: spellings of one class are
  neutral twins in every encounter, and the class-level dynamics is exact). Named spelling masses under L:
  each boss constant 0.5/Z_B = **4.12·10⁻⁴**; D₀, D14, WF 2⁻⁴/Z_B = 5.1·10⁻⁵; **D\* 2⁻⁷/Z_B = 6.43·10⁻⁶ = 2⁻⁶ of a
  constant** (the modal run: 9.7·10⁻⁹ against 0.1025, 2^−23.3); D14₂ 2⁻⁶/Z_B = 1.3·10⁻⁵; scab and striker
  0.5/Z_W = **0.0350**; **T₁, T₀, R, Q 2⁻⁴/Z_W = 4.38·10⁻³ = 2⁻³ of the striker**; U 2⁻⁷/Z_W = 5.5·10⁻⁴.
  Aggregated class masses are computed in §1.4.
- **U (control):** uniform over the lumped classes of each role.
- **Expanded syntax (matched control).** The same compiled programs, the same classes and the same dynamics; the
  prior is 2^−(expanded nodes) per spelling, normalized per role, where a spelling's expanded node count is that of
  its compiled body term with every check atom spelled out: the call's argument term built literally (pairs,
  naturals, variables, constructors, and for probes the literal quote of the constant boss with its list) and the
  wrapper inlined as its body (`(λarg. if eq(capk(fst arg, lib CC3, arg), T) then T else F) ARG`, 12 nodes; the core
  CC3 stays one `lib` node), `not` 3 nodes, `and`/`or` 2, `if` 1, leaves 1; the certificate list is not counted
  (public production, as under L). Counted by hand from the term structure (one node per term constructor):
  argument of a wage atom 12 + |A|, |A| the outcome list's term size (≥¼, ≤¼: 13; =½: 7); of an O-atom 15; of a probe
  14 + q(s′) with q the literal quote's size (q(0) = 34, q(¼) = 60: `λλλ((λ.nat) CERTS)` with one and two list entries
  of 25 nodes each, plus list spine). **Expanded atom sizes: B≥¼, B≤¼ 37; B½ 31; O:S, O:W 27; P^0 60; P^¼ 86.**
  Named expanded sizes: constants 1; T₁ 34 (2⁻³³ of the striker), T₀ 40, Q 30, D₀ 63, D14 89, **D\* 151 (2⁻¹⁵⁰ of a
  constant)**. These counts are re-derived by code from the compiled terms before any cell (§1.x); the expanded
  prior puts essentially all mass on constants.

#### 1.3.6 Ideal and executable values

As milestone 2: the **ideal** table answers every check by the host replay (`ExactHost` semantics extended to K₃,
no step cost); the **executable** table answers it by the clean run of the checker term at K = 10⁶. They can differ
only where a check exceeds its cap V or a run exceeds K. The cost risk is new here: a worker's check of a concession
boss Runs the boss's script, whose Run on a probe box nests a worker check in the probe encounter, which may itself
nest the constant's check and a closure over the other worker (depth up to 4, up to three probes per boss); my
guess is 3–15·10⁴ steps for D\*, against V = 2.5·10⁵. The lottery runs on the **ideal** table only if executable =
ideal is measured on every named encounter, on every (boss class, worker pair) combination occurring in a sample of
lottery seeds, and on the largest-cost cases found, with the margin to V reported; otherwise it runs on the
executable values wherever they differ. The fuel sweep (K ∈ {3·10⁵, 10⁶, 3·10⁶}, V = K/4) recomputes the named
states and the near-cap programs.

#### 1.3.7 Frozen lottery and chain conventions (after review)

- **Islands:** I islands, each with three slot populations of N (boss, W1, W2); iid seeds per slot from the role
  prior over spellings (W1 and W2 independently), mapped to classes; ε = 0.
- **Dynamics:** `sog_lottery`'s kernel: a birth event picks an (island, slot) unit uniformly; with probability
  m = mN/N the parent comes from a uniformly chosen other island's same slot; parent drawn with weight
  count·exp(w·f), f the expected payoff against a uniform draw of one member of each other slot of the source island;
  victim uniform; w = 0.3; mN = 1; a generation is 3IN births; exact event skipping. The table is J(b, x, y) of
  Lemma F₃ with tags.
- **Checks** every 10 generations; horizon 2,000; a run stops early only if globally closed (sog_lottery's closure:
  every present class of every slot gives the same realized play key against every combination of the other slots'
  present classes), and is then frozen in play to the horizon.
- **Fair island at a check:** the island's encounter distribution (one uniform draw per slot) has the *fair* summary
  (wage ½, both work, no realized whack) as its strict plurality summary (`union.SUMM`). **Fair island:** fair at 10
  consecutive checks. **Establishment:** the end of the first 10-check fair window on any island (the window's start
  reported too). **Persistence:** fraction of islands fair at the final check (and fair at all of the last 10).
  **Residence time:** checks × 10 from a fair island's first window to its first non-fair check.
- **Endpoint (E3-type, polymorphic islands allowed):** at the horizon, for each island, Z = (Z₀, Z₁, Z₂) seeded with
  its residents and closed under entry by globally present classes (q in slot s joins if for some residents' triple
  in Z of the other two slots and some z ∈ Z_s, u_s(q) ≥ u_s(z)); the island is *resolved* with summary k iff every
  triple in Z₀ × Z₁ × Z₂ has summary k; otherwise *unresolved* (censored). Runs: *universal fair* iff every island is
  resolved fair; censored runs counted in the denominator as not-success and reported.
- **Run-level uncertainty only:** 40 runs per cell; Wilson intervals on run-level outcomes; run-level means of island
  fractions with bootstrap intervals over runs (2,000 resamples); never pooled-island intervals.
- **Exits of fair islands** (each island's first exit after a fair window), classified from the per-check modal
  classes: *unread-slot drift then boss cut* (a worker slot's modal class changed to a non-militant during the fair
  window, then the boss's modal class changed to a non-½ payer), *boss cut* (the boss modal class changed first),
  *worker drift* (a worker modal class changed and the play left fair without a boss change), *migration* (the class
  that changed the play was absent from the island at the previous check and present in a migrant source), and
  *false certificate / timeout / substitution* (by the static audit, which must find none for the classification to
  be zero).
- **Chain (diagnostic):** the ε→0 chain over monomorphic triples (with separate slots a mutant's payoff depends only
  on the two other residents, so fixation is constant-selection Moran), mutant drawn from the role prior's class
  masses, `union_chain.UChain`'s hybrid explorer with the J of Lemma F₃ supplied on the fly, N = 10⁴, θ = 10⁻⁹, seeded
  with every named state and every strict-NE triple found by the static analysis, with the cut diagnostic
  (`concessions_cutdiag.py`'s quantities) recorded.
