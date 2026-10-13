# The social organization game, fully realizable: identity admitted, production refused against self (notes, 2026-10-13)

Spec `specs/2026-10-13-sog-fully-realizable.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-13-sog-fully-realizable-gpt-6.1-sol.md`;
the [after review] text is the resolution). §1 is written before any code of this run and before any counted cell:
readings of the spec, the language change, the production rule for triples, the named classes with hand plays and
producible certificates, the lumping condition, the coalition masses' definitions, the cost model, the fixed
definitions, the executable semantics and its validation plan, the forced coalitions and the local assays. §1.x (code
validation and static numbers) is appended after the code and before any counted cell; §2 (costs) after the cells.

Base, imported unchanged: the realizable social organization run (`src/sog_realizable.py`: K₃, the closure, the path
tactic, the abstract evaluator, the factorized table of Lemma F₃, the lottery law; `notes/sog-realizable.md` §1),
the provenance run (`notes/provenance.md` §1: S-nonself, the lack rule, own-side validity, self-play-only scripts,
identity bookkeeping, event-indexed streams, the exact skip), milestone 5 (`notes/certificates-as-genes.md` §1: the
tactic as code, Lemma A, inheritance), the identity run (`src/identity_tags.py`: `eq` as one evaluator step,
identity-aware lumping).

*Disclosure.* Before writing this section I ran six scratch measurements, none on a counted cell and none with a new
checker: (i) template counts with the `eq` atoms (both roles, n ≤ 7); (ii) whole plays of three named triples by the
realizable run's term, for wall time (10–30 ms each, nested checks replayed from the evaluator's clean-run cache);
(iii) term check costs of the realizable run's named triples (every check of the encounter and both probe
encounters); (iv) the same checks with the unread co-worker varied (scab, striker, T₁, Q, U, T₀); (v) respellings of
T₁ and D\* (`not`, double `not`, `and`); (vi) closure checks of Q and U pairs. Their content is quoted where used
(§1.1, §1.7).

## 1. Design

### 1.0 Readings of the spec, stated before any code

1. **Sources are slot-independent (a language change, forced by the question).** In the realizable run a worker
   template was compiled once per slot (the slot-1 and slot-2 terms differ in the order they build the encounter), so
   a T₁ in slot 1 and a T₁ in slot 2 are different terms. Then `eq(me, other)` is false across slots for every worker,
   the greenbeard union cannot exist, and S-nonself₃'s gate never fires (the other worker is always another source):
   both of the spec's identity questions would be empty by an encoding accident. Here every program is a carrier with
   **four abstractions**, `λme. λx. λy. λs. (λcerts. BODY) CERTS`, run as `p ⌜p⌝ ⌜x⌝ ⌜y⌝ s` with the **public slot
   label** s ∈ {0, 1, 2} supplied by the evaluator (boss `b ⌜b⌝ ⌜w1⌝ ⌜w2⌝ 0`, worker j `wj ⌜wj⌝ ⌜b⌝ ⌜o⌝ j`). A worker's
   check atoms build the actual encounter as `if s = 1 then (b, me, o) else (b, o, me)`, so one compiled body serves
   both slots and an exact copy in the other slot is the same source. Plays are the realizable run's (the per-slot
   compilations computed the same encounters); step counts change by a few steps per atom. The slot label is a public
   correlating signal of the kind `ROLE` already is (CLAUDE.md, "`ROLE` is first-class"); the boss ignores it.
2. **`eq` compares sources, not quotes.** A quote carries its certificate list (the checker reads certificates from
   the quote), and under S-nonself₃ inventories differ between copies of one source. The spec says source identities
   and inventories are separate state ("identical sources with different inventories"), so the identity atoms compare
   **code**: `EQS(q₁, q₂)` = structural equality of `srcof(q₁)` and `srcof(q₂)`, where `srcof` strips the certificate
   argument (walks λ⁴, returns the function part of the application). A library primitive; one template node; a fixed
   number of evaluator steps whatever the quotes (`eq` is one tick in `lt_code`).
3. **Identity atoms.** Workers: **`EQ` = `EQS(me, o)`** ("the other worker is an exact copy of my source"; the spec's
   `eq(me, w2)`). Bosses: **`N1` = `EQS(w1, ⌜T₁⌝)`**, **`N2` = `EQS(w2, ⌜T₁⌝)`** (the named quote: T₁'s code as a literal
   quote in the boss's source) and **`EQW` = `EQS(w1, w2)`** ("the two workers are one source"). The spec's
   `eq(me, them)` for a boss would compare a boss with a worker, which is false by construction (roles differ), so the
   boss's identity atom is read as `EQW`. "The named quote ⌜T₁⌝ in boss probes" is read as the boss's atoms against
   ⌜T₁⌝ (the closed shop B_eq is defined by exactly this atom), not as probe encounters with a quoted co-worker.
4. **The sham (matched-prior identity-disabled control).** Each identity atom is replaced by a **sham atom** of one
   node, evaluated as `EQS(q, ⌜Z⌝)` against a fixed quote Z that is no catalogue source: always false, at the same
   evaluator cost. One sham per identity atom (workers: `SW`; bosses `S1`, `S2`, `S3`), so the sham grammar's
   spellings are in bijection with the `eq` grammar's and **every spelling's prior mass is identical**; founders are
   seeded identically under paired streams. A spelling with a sham atom plays as its `eq` twin would if no identity
   relation ever held.
5. **eq without ⌜T₁⌝:** `N1`, `N2` replaced by the shams `S1`, `S2`; `EQ` and `EQW` kept. Same bijection. The ladder
   no-eq → sham → eq-without-⌜T₁⌝ → eq separates prior dilution (no-eq vs sham), identity among workers and bosses'
   `EQW` (sham vs eq-without-⌜T₁⌝) and the named quote (eq-without-⌜T₁⌝ vs eq).
6. **Tag** (what source-targeting whacks read): a worker is tagged iff its run tree contains an atom about the other
   worker: an O-atom or `EQ` (the realizable definition extended). Sham atoms do not tag.
7. **H in this run** is the realizable run's public, uncharged path tactic over every assignment, extended to the
   identity atoms (each identity value is part of the assignment, §1.1.4): full lists, fixed per run tree.
8. **S-nonself₃** (§1.2): after the play, a program lacking an entry for an outcome set of its question family runs
   the tactic as code (PROD3, §1.1.5) for that set at the actual encounter, with cap P = K/4, in the residual budget;
   a worker does so only if the other worker's source differs from its own (the gate); a boss always may (the other
   participants are workers, never its source). Lack rule, vertical inheritance, founders empty.
9. **Encounter rate.** r = N/3 encounters per Moran event (each encounter one uniform member of each slot of a
   uniform island), so each individual takes part in ≈ N encounters per generation, as in the provenance run
   (≈ 100 at N = 100). A generation is 3IN Moran events (the realizable run's).
10. **Scale guard, read.** The realizable run already had 77,211 boss classes without `eq`, so "more than 2,000 classes
    per role" fires literally before any change. I read the guard as applying to the **worker** role (318 classes per
    slot in the realizable run, the role in which identity enters as a pair relation) and to the executable machinery
    (the number of cost tables that must be measured). If worker classes exceed 2,000 with `eq`, the named quote is
    dropped and the arm is reported as a different experiment. Scratch count (i): 1,826 worker spellings and 602 run
    trees with `EQ` (1,282 / 422 without); 258,399 boss spellings and 177,318 run trees with the three boss identity
    atoms (137,385 / 93,969 without).
11. **Executable semantics on the full support.** The spec allows a reduced support if the full executable table is
    infeasible. The cost model of §1.7 composes exact per-program step counts measured by the term, so the
    executable table is computed for every realized triple; there is no support reduction. The spec's validation
    (≥ 200 encounters replayed whole) is applied to the composition instead (§1.9).

### 1.1 The language: K₃′

#### 1.1.1 What changes in the library

K₃ (`notes/sog-realizable.md` §1.1) with exactly these changes, in a new library build (the realizable module's build
is not modified; this run installs its own):
- `getcerts4` reads four abstractions, then the application whose function part is a λ (the certificate argument);
  `mkconf4(enc, j)` builds `app⁴(b, b, w1, w2, 0)`, `app⁴(w1, w1, b, w2, 1)`, `app⁴(w2, w2, b, w1, 2)`.
- `vone4` takes its two arguments as one pair (so the evaluator's library entry can be instrumented for step counts,
  §1.7); its body is `vone3`'s.
- `srcof`, `EQS`, and the sham constant Z (a fixed one-abstraction quote).
- **PROD3 / PCORE3**, the tactic as code (§1.1.5).
Every rule of K₃ (Ax, EvR\*, ChkR, Run, RunNeg, Hyp with the closure), the uniform-cost closure bookkeeping, the
wrapper `CHK3` (now over CC3′) and its accounting (a call costs W + 6) are unchanged. The naive control is not used.

#### 1.1.2 Templates and compilation

Milestone 2's template form, cutoff n = 7, one node per leaf, atom and connective. Worker atoms: `B≥¼`, `B½`, `B≤¼`
(the boss certified to pay a wage in the set), `O:S`, `O:W` (the other worker certified to strike / work in this
encounter), and `EQ` (or `SW`). Boss atoms: the 8 probes `P_j^{s′}:a` of the realizable run (probe constants
re-carried with four abstractions and their constant lists) and `N1`, `N2`, `EQW` (or their shams). An identity atom
compiles to `if EQS(..) then .. else ..` evaluated by the program itself: it is not a check call, so the program's run
still makes at most 3 check calls (Lemma TO(c) of the realizable run holds: no catalogue run times out globally at
K = 10⁶).

#### 1.1.3 Soundness

Theorem S^cert₃ holds unchanged: its proof uses only that the root of a box is the actual fuel-bounded run of its
subject on the quotes in the argument (now with the slot label, which `mkconf4` supplies from j), Lemma N₃ and Lemma
Sym₃, none of which mentions the number of abstractions or the program's own deterministic steps. An identity atom is a
deterministic step; EvR\* passes through it. **Lemma Sub′:** every worker check builds the encounter in slot order from
its own arguments and the evaluator's slot label, so (with an honest evaluator) no worker certificate is about a
non-actual encounter; the corrupted instance is a worker run with the wrong slot label (it builds the swapped
encounter and can work at wage 0 beside a misread D\*, classed as substitution; checker sound). **Lemma 0₃ holds**
(the militant cannot be faked) since it is a statement about wage checks only.

#### 1.1.4 The H lists with identity atoms (the public path tactic, extended)

The path tactic of the realizable run (§1.1.4 there) with the identity atoms as part of the assignment: for each
outcome set A of the role's family and each assignment α to the run tree's atoms (identity atoms included; atoms in
source order, binary order, T before F), follow the run; at an identity atom take the branch α gives (EvR\* passes
through it, so the script records no node for it); at a call box proceed as before. The list holds the distinct
scripts, ordered by Hyp count then α. **A script records the identity values only implicitly**: it is valid at a root
iff the run's actual path matches its structure, so a script written on the `EQ`-true path of `if(EQ, X, Y)` fails at
an `EQ`-false root (EvR\* reaches Y's first call or leaf, where the script expects X's), unless X and Y have the same
call structure on that path. The abstract evaluator records each script with the set of identity assignments under
which it was produced (one script can arise from several), and validates it at a root iff the root's identity values
match one of them and its Run/RunNeg leaves hold. This is checked against the host replay and the term (§1.9).

#### 1.1.5 The tactic as code: PROD3 (the endogenous producer)

**Definition.** PROD3(P; arg), arg = the producer's own box argument at the actual encounter (V, enc, j, A, K), runs
under cap P = K/4 and returns a script for ⟨conf_j(enc), K⟩⇓A or NONE. It is the path tactic driven by the actual
values, with backtracking on the boxes that may be closed by Hyp:
- at an identity atom: the run's actual branch (EvR\*);
- at a call whose box is **not** Hyp-able (a worker's boss boxes; a boss's probe boxes): compute the box's value by
  calling the check (a nested check, charged); T → premise 1 continues on the T-branch and premise 2 closes the box by
  Run; F or TO → premise 1 closes the box by RunNeg and premise 2 continues on the F-branch;
- at a call whose box is **Hyp-able** (an encounter box about the other worker, subject ≠ the producer): first the
  T-branch with premise 2 closed by Hyp, without computing the box; if that subtree yields no script, compute the
  box's value and, if it is not T, take the F-branch (premise 1 closed by RunNeg);
- at a value: Ax if it is in A, else NONE.
The result is the first assignment, in lexicographic order over the boxes on the path (T before F for Hyp-able boxes),
consistent with the actual values; it is one of the H list's scripts. The 64-node bound of milestone 4 applies.

*Re-opened design, stated (REJECTED "the social organization game over the realizable language", design choices
dropped: "the tactic with Hyp first (never follows an F-branch; the path tactic instead)").* That entry dropped
milestone 4's frozen priority without backtracking, because it never followed an F-branch of a Hyp-able box. PROD3
is Hyp-first **with** backtracking, so it does follow F-branches (Q's work script is RunNeg on "the other strikes").
What justifies re-opening it: production is now endogenous, so it must be a function of the actual encounter (the
path tactic over all assignments is H, the free service); Hyp-first is milestone 5's endogenous rule, the one whose
provenance consequences were measured.

**Which sets are attempted.** After the play, for each set of the role's family the program still lacks (workers
[C] then [D]; bosses ≥¼, =½, ≤¼), in that order, one PROD3 call with cap P; a script found is appended (lack rule);
NONE or a cap timeout appends nothing. All of it runs in the residual of the encounter's fuel K after the program's
own play; when the residual is exhausted the remaining attempts are not made (fuel timeout, recorded).

### 1.2 S-nonself₃: the gate for triples, the target, inheritance

**The gate.** A worker produces in an encounter iff **the other worker's source differs from its own** (`srcof`
inequality, i.e. different spellings). The boss of the encounter can never share a worker's source, so the condition
"every other participant's source differs" reduces to the other worker for workers and is vacuous for bosses. The
probe constants inside a boss's probes are not participants. Two programs of one spelling with different
inventories are the same source (refused); two spellings of one run tree are different sources (allowed).

**The certificate's target.** PROD3 is run on the producer's own box argument built from the actual encounter's three
quotes as of the play (the realizable run's absolute slot order), so a produced script is a derivation at the actual
root. It is appended to the producer's list and is then checked, like every entry, at whatever root a later check
names (scripts are opponent-generic in form; their validity at another root is a fact about that root).

**Inheritance.** A newborn inherits its parent's source and inventory; migrants carry theirs; founders of every
S-nonself₃ cell start with empty inventories (H cells: the full H list per run tree).

**Claim N₃ (what S-nonself₃ can never write).** For a worker run tree containing `EQ`, every script PROD3 writes under
S-nonself₃ is written at a root where `EQ` is false (the gate refuses the only roots where it is true). Hence any
script whose validity requires `EQ` true at its root is **non-producible** under S-nonself₃ by any program of that
source, at any encounter, ever; it can enter a list only by inheritance of a list that already holds it, which no
founder does. (Bosses are not gated; their identity atoms' true paths are producible.)

**Self-play-only scripts in this game.** The provenance run's SPO notion (valid only at self roots) transposes to: a
(run tree, script) pair valid only at roots where the other worker is a copy. By construction these are exactly the
scripts that need `EQ` = T or that close a box only because two of the encounter's quotes coincide (the R = S
coincidence of milestone 5; in K₃ a worker never checks itself, so the only such coincidence is `EQ`). Claim N₃ gives
0 SPO scripts held under S-nonself₃; the dynamic audit counts them.

### 1.3 Grammar, prior, named classes

**Prior.** L = 2^−nodes over spellings, normalized per role and per arm grammar (§1.0 items 3–5). Hand normalizers:
workers with `EQ` Z_W = 2/2 + 24/16 + 24/32 + 312/64 + 1464/128 = 19.5625 (no-eq 14.281); bosses with three identity
atoms Z_B = 9/2 + 891/16 + 891/32 + 20493/64 + 236115/128 = 2,252.9 (no-eq 1,214.4). Spelling masses: a constant boss
2.22·10⁻⁴ (no-eq 4.12·10⁻⁴), D\* 3.47·10⁻⁶, B_eq and B_id (4 nodes) 2.77·10⁻⁵; scab, striker 0.0256 (no-eq 0.0350),
T₁ 3.19·10⁻³, U_eq and XM (6 nodes) 7.99·10⁻⁴. Sham and eq-without-⌜T₁⌝ arms: identical spelling masses to the eq arm.

**Named classes.**
- Workers: scab `work`; striker `strike`; **T₁** = `if(B½, work, strike)` (the open militant; source ⌜T₁⌝ is this
  spelling only); T₀ = `if(B≥¼, work, strike)`; R = `if(B≤¼, strike, work)`; Q = `if(O:S, strike, work)`;
  U = `if(B½, work, if(O:S, strike, work))`; **U_eq** = `if(EQ, if(B½, work, strike), work)` (the greenbeard union:
  strike unless paid fair, only beside an exact copy; 6 nodes); **XM** = `if(and(B½, EQ), work, strike)` (the
  exclusive militant: strike unless the boss certifies fair and the other worker is an exact copy; 6 nodes); T₁′ =
  `if(not(B½), strike, work)` (a respelling of T₁: same run tree, different source).
- Bosses: the 9 constants; D₀, D14, **D\*** = `if(P_1^¼:S, pay(½), if(P_1^0:S, pay(¼), pay(0)))`, D14₂, WF (realizable
  definitions, all with `none` whacks); **B_eq** = `if(N1, pay(½, none), pay(0, none))` (the closed shop: fair iff w1 is
  exactly ⌜T₁⌝); **B_id** = `if(EQW, pay(½, none), pay(0, none))` (fair iff the two workers are one source).
- **The world-0-free fakers** (the realizable run: none; WF plays (0; S, S) against militants) and **the unread-slot
  scab** (a scab in slot 2 beside T₁ in slot 1 under D\*, or beside any slot-1 militant under a boss that reads w1).

#### 1.3.1 Hand plays (CC), under H and under S-nonself₃

Notation (wage; a1, a2), W work, S strike. "S₃ (acquired)" = the inventories each member reaches by S-nonself₃ in a
mixed island (§1.4); "S₃ (copies only)" = an island on which the members only ever meet each other.

| encounter | H | S₃ (acquired) | why |
|---|---|---|---|
| F\* = (D\*, T₁, T₁) | (½; W, W) | (½; W, W) | T₁'s [D] script is RunNeg on the boss's =½ box, written at any encounter beside a non-T₁ worker and a boss not certified =½, valid at the probe roots (⌜pay(¼)⌝, T₁, ·); D\* writes its =½ script at an encounter where its w1 probe is true; T₁ then works on D\*'s =½ certificate (Run) |
| F\* (copies only, empty) | – | **(0; S, S)** | the gate refuses every T₁ production (the other worker is always T₁); the probe is F, D\* pays 0 and writes ≤¼; T₁'s B½ check fails: **bootstrap failure by the gate on a monomorphic coalition** |
| F\* (copies only, preloaded) | – | (½; W, W) | as H; newborns inherit |
| (D\*, T₁, scab) | (½; W, W) | (½; W, W) | the one-slot leak (D\* reads w1 only); then pay(0) enters neutrally (T₁ strikes, scab works: boss 1 = 1) |
| (pay(½), U_eq, U_eq) | (½; W, W) | (½; W, W) | `EQ` true; U_eq's play reads only the boss's certificate (the constant writes its own) |
| (pay(½), U_eq, scab) | (½; W, W) | (½; W, W) | `EQ` false, U_eq works; **then pay(0) strictly invades (2 > 1)**: a greenbeard union cannot strike alone, so its unread-partner drift is followed by a strict cut |
| (D\*, U_eq, U_eq) | (½; W, W) | **(0; S, S)** | H: the probe (⌜pay(¼)⌝, U_eq, U_eq) has `EQ` true and U_eq is certified to strike (H lists hold the `EQ`-true script). S₃: that script needs `EQ` = T at its root, **non-producible (Claim N₃)**; the probe is F, D\* pays 0, the pair strikes |
| (D\*, U_eq, scab) | (0; W, W) | (0; W, W) | the probe beside a scab has `EQ` false: U_eq would work at ¼, so D\* pays 0, and U_eq (`EQ` false) works: the scab is **deleterious** in slot 2 under H's (D\*, U_eq, U_eq) (it gets 0 vs ½) |
| (B_eq, T₁, T₁) | (½; W, W) | (½; W, W) | B_eq reads N1 = T, its =½ script is `EvR*; Ax` written at that root (bosses are not gated); T₁ works |
| (B_eq, T₁′, T₁′) | (0; S, S) | (0; S, S) | T₁′ is not the source ⌜T₁⌝ |
| (B_eq, T₁, scab) | (½; W, W) | (½; W, W) | B_eq reads w1 only: **the unread-slot substitution leaves the closed shop's wage unchanged** (RE 3, after review) |
| (B_eq, scab, T₁) | (0; W, S) | (0; W, S) | |
| (B_id, U_eq, U_eq) | (½; W, W) | (½; W, W) | fully producible identity coalition: B_id's =½ script needs only `EQW` = T at its own root |
| (B_id, U_eq, scab) | (0; W, W) | (0; W, W) | the scab entering beside the union is deleterious (0 < ½); pay(0) against the union pair is deleterious (they strike); **a constant pay(½) boss enters neutrally**, after which the scab enters neutrally and pay(0) strictly: B_id protects the union only while it holds the boss slot |
| (pay(½), XM, XM) | (½; W, W) | (½; W, W) | |
| (pay(½), XM, scab) | (½; S, W) | (½; S, W) | XM strikes beside a non-copy; the scab gets ½ = the resident XM's: neutral entry, and XM's own payoff falls to 0 |
| (WF, T₁, T₁) | (0; S, S) | (0; S, S) | no probe wage faker (realizable run) |
| (b, Q, Q′), Q′ another spelling of Q's run tree | (b; S, S) | (b; S, S) | the strike pact between source-distinct spellings: Q's [D] Hyp script is written beside Q′ (non-copy), the closure validates |
| (b, Q, Q) copies | (b; S, S) | (b; S, S) if inherited, else (b; W, W) | Q's [D] script is generic (Hyp), so copies hold it if any ancestor wrote it beside a non-copy; a copies-only Q island from empty founders never writes it |

#### 1.3.2 Which certificates each named class can produce under S-nonself₃ (prediction 2 established here)

- **T₁:** [D] = `EvR*; ChkR[RunNeg · EvR*; Ax]` (RunNeg on the boss's =½ box), at any encounter beside a non-T₁ worker
  under a boss not certified =½; [C] = `EvR*; ChkR[EvR*; Ax · Run]` beside a non-T₁ worker under a boss certified =½.
  Both are valid at non-self roots (not SPO).
- **U_eq:** at every root it may produce at, `EQ` is false and its run is `work` without a call: [C] = `EvR*; Ax`
  (EvR\* to the value). [D] at such roots: none (no strike leaf on the `EQ`-false path). The `EQ`-true scripts ([D]
  `EvR*; ChkR[RunNeg · EvR*; Ax]` and [C] `EvR*; ChkR[EvR*; Ax · Run]` on the true path) are **non-producible**
  (Claim N₃). **The greenbeard union can never be certified to strike under S-nonself₃.** Its coordinated strike
  still happens (its play reads only the boss's certificate), but no probe boss can see it; only bosses that pay it
  without reading its certificate (constant pay(½), B_id) can hold a fair island with it. So RE 2's non-producibility
  claim is **established statically** for the strike certificate; whether the union can hold fair islands under
  S-nonself₃ is a separate, dynamical question (it can, with constant or `EQW`-reading bosses).
- **XM:** at producible roots `EQ` is false and XM strikes: [D] = `EvR*; ChkR[...]` on the path where `and(B½, EQ)` is
  false. Two sub-paths: B½ F (RunNeg on the boss box, then EQ not evaluated) or B½ T and EQ F (Run on the boss box,
  then EvR\* through `EQ` to strike). Its [C] (work, which needs `EQ` true) is non-producible. XM is certifiable to
  strike, and every probe boss sees it strike unless the probe's w2 is an XM copy (then the true path's script would
  be needed and the probe is F).
- **Q, U:** Hyp scripts written beside source-distinct partners; valid beside copies.
- **Bosses** (D\*, B_eq, B_id, constants): every path's script is producible at a root where the path is taken (no
  gate). Under the lack rule a boss holds one script per set, the first one it writes; a boss whose first ≥¼ script
  was written on its ½ path is not certifiable at ≥¼ on its ¼ path (path dependence; recorded as "uncertified
  default" when it costs a worker's work).

#### 1.3.3 Invasion structure by hand (CC)

F\* has no strict invader (realizable run); its neutral substitutes are as there. **The greenbeard state (pay(½), U_eq,
U_eq)** has no strict invader at the residents, but its unread partner drifts (any slot-2 non-copy that works at ½ is
neutral) and after a scab fixes in either slot pay(0) invades strictly: the greenbeard union is **less** protected than
the open militant against unread-slot drift (T₁ in slot 1 strikes alone; U_eq does not). **(B_id, U_eq, U_eq)** is
protected against worker drift while B_id holds the boss slot, and B_id is neutrally replaced by constant ½ bosses.
**(B_eq, T₁, T₁)** behaves as (pay(½), T₁, T₁) towards T₁ (T₁ is the only source it pays) and is neutrally replaced by
every boss paying ½ to the T₁ pair; it pays 0 to every respelling of T₁, so on an island held by T₁′ it is
deleterious. Under S₃, (D\*, U_eq, U_eq) is not fair and the union is held only by bosses that need no worker
certificate.

### 1.4 Lumping, inventories and identity (correctness condition and tests)

**State.** Each individual's type is (role, spelling, inventory). The spelling is kept for every individual (source
identity is a relation between spellings: `EQ`, `EQW`, `N1`, `N2` read it, and the S-nonself₃ gate reads it). The
inventory is a tuple of script indices per outcome set (into the run tree's H list; under the lack rule at most one
per set; under H the full list).

**Tables are computed on row classes, exactly.** A *row class* is (run tree, inventory) for bosses and workers, plus
the bit "is ⌜T₁⌝" for workers (only T₁'s spelling has it). The play and certification values of a triple depend on
(boss row class, w1 row class, w2 row class) and on three relation bits read from the spellings: same(w1, w2), and
"is ⌜T₁⌝" for each worker. **Correctness condition:** two individuals may share table rows iff no program of either
role's catalogue (`EQ`, `EQW`, `N1`, `N2` readers included) can distinguish them in any encounter; with every identity
read routed through the relation bits computed from spellings, the condition reduces to (a) Lemma T₃'s τ-symmetry
for scripts and boxes (spellings of one run tree with equal inventories give the same check values whenever the
relation bits agree), and (b) **costs**: step counts depend on the spelling (scratch (v): T₁′ costs +6% of T₁'s own
validation steps), so executable values are computed with **per-spelling** step tables composed onto the row-class
traces (§1.7). Nothing is merged across spellings in the population state; row classes only share the ideal tables.
**Tests (code, before any cell):** (1) distinct-source twins (T₁ and T₁′; U_eq and a respelling of it) against `EQ`-,
`EQW`- and `N1`-readers: the table's values equal whole runs, and the twins are distinguished exactly where the
relation bit differs; (2) identical sources with different inventories (T₁ with [D] only vs with [C] and [D]; D\*
with ≥¼ written on the ½ path vs on the ¼ path): distinct row classes, table = whole runs; (3) relation bits by
`srcof` equal to spelling equality on random pairs.

### 1.5 Founding-coalition masses

As the realizable run (§1.4 there): a **founding coalition** is a triple of classes whose play is (½; W, W) with no
strict invader in any slot among the catalogue's classes (only boss invaders matter: no worker earns more than ½), and
its mass is μ_B(b) μ_W(x) μ_W(y) summed. With identity, a triple's play depends on whether x and y are one spelling:
the mass splits as Σ_{x≠y spellings} μ_x μ_y [fair, uninvadable at rel = 0] + Σ_x μ_x² [at rel = 1]. Reported:
**(a) with identity classes** (the eq grammar, every triple); **(b) without identity classes** (triples in which no
member's run tree contains an identity atom; the same normalizer); **(c) the no-eq grammar**; **(d) under
S-nonself₃-producible inventories** (each member's inventory replaced by the scripts it can produce at a non-self
root of a mixed island: H lists minus the non-producible scripts of Claim N₃; a static upper bound on what the
fully realizable cell can found). *Hand estimates:* (c) ≈ the realizable run's 0.0171; (a) below (c) by the dilution of
both roles by identity spellings (each identity-free worker spelling ×14.281/19.5625 = 0.73, so pairs ×0.53; boss
spellings ×0.54, partly offset because a random identity-reading boss pays ½ on some codes) plus identity coalitions of
order Σ_x μ_x² ≲ 10⁻⁵ (copies are rare at the seed: μ_U_eq² ≈ 6·10⁻⁷); (d) ≤ (a), the difference being the U_eq-type
coalitions with probe bosses (small).

### 1.6 The cost model's definitions

- **Required (uncensored) cost** of a check, a play or a production: its step count if it ran to completion with no
  cap (the ideal semantics' computation, charged as the term charges it: every nested check replayed at its full
  cost). Defined for every check, including those that time out.
- **Capped execution cost:** min(required cost, the cap that applies) as actually charged: a check ≤ V + 6 (a timeout
  charges the cap), a production attempt ≤ P, a whole participant's encounter (play + production) ≤ K.
- **Failed attempts:** checks that time out (exec TO where the ideal value is T or F), productions that time out at P
  (cap timeouts), attempts not made for lack of residual fuel (fuel timeouts), productions that return NONE.
- **Amortized production expenditure per lineage:** a lineage = the descendants of one founder (or of one producer's
  acquisition event); its production steps (successful and failed attempts, including futile retries) divided by its
  acquisitions and by its total births.
- **Per-encounter cost** = the three participants' play steps (own run + calls) + their production steps.

### 1.7 The cost model: composition of measured step counts (executable semantics)

Scratch (iii)–(vi) show that the term's step counts are **additive**: a check's total = its own validation steps +
the full totals of the nested checks it replays (T₁'s work check under D\*, D14 and pay(½) is the boss's =½ check +
13,640 in all three; its own steps do not depend on the co-worker; a Q closure costs about twice one validation).
The model:
- **Validation steps** `vc(spelling, inventory, slot, A, ι, σ)`: the steps of one `vone4` call (getcerts, the entry
  scan, every script attempt up to its stop point), excluding nested replays; ι the root's identity values, σ the
  values of the nested boxes the attempts meet. Measured by the term (instrumented library entry), on demand, cached;
  nested checks are pre-cached at zero cost with the forced values σ, so the measurement isolates own steps.
- **A check's required cost** = Σ over the `vone4` calls of its closure (root and members, in the term's worklist
  order) of vc + the closure bookkeeping (a fixed function of the closure's trace: pops, membership hits, insertions,
  pushed list lengths; calibrated by code) + Σ over every Run/RunNeg occurrence of (the nested check's required cost),
  computed recursively on the abstract evaluator's trace.
- **Executable value** of a check: its ideal value if its required cost ≤ V (the exact boundary calibrated by code),
  else TO; a nested TO makes the root TO (its cost exceeds the root's cap). A program reads TO as F.
- **A play's steps**: the program's own run steps (measured likewise with its calls pre-cached) + Σ (call cost + 6).
- **A production's required cost**: PROD3's own steps (measured likewise, keyed by the values met) + Σ nested checks it
  calls. Cap timeout iff > P; fuel timeout iff the encounter's residual is exhausted.
- **K sweep:** step counts do not depend on K except through caps (scratch: the realizable run's costs are
  fuel-independent), so K ∈ {3·10⁵, 10⁶, 3·10⁶} are read off the same required costs.

The composition is exact if (1) own steps do not depend on anything but the keyed quantities, and (2) bookkeeping is
the stated function; both are tested against whole term runs (§1.9). Where it fails the mismatch is reported, not
patched.

### 1.8 Fixed definitions (before any cell)

- **An island's play** at a check: the joint play (wage, whack realized, a1, a2) with the largest probability under the
  island's encounter distribution (one uniform member of each slot; ties broken by code order). **Fair island** at a
  check: its play is (½, no whack realized, W, W).
- **Establishment** (per run): the first check (every 10 generations) at which some island is fair. Establishment
  time = that generation; censored at the horizon.
- **Persistence**: the fraction of islands fair at generation 2,000 (the common horizon). The 10,000-generation
  extension, run for runs not globally closed at 2,000 as budget allows, is a separate column; runs closed before
  2,000 are frozen in play.
- **Plurality** (per run): the wage with the largest island share at 2,000; zero-wage plurality = fraction of islands
  whose play has wage 0.
- **Productive efficiency** (per island): the probability that an encounter has no strike and no realized whack,
  reported separately from wage fairness (an island at (0; W, W) is productively efficient and unfair).
- **Holder classification by play** (fair islands at the horizon): the island's modal class in each slot. A worker
  class is an *open militant* if it strikes against a certified pay(0, none) beside a scab, a *greenbeard* if it
  strikes against pay(0, none) beside an exact copy of itself (same spelling and inventory) and works beside a scab,
  *unconditional* otherwise. Island holder: **open militants** (some slot's modal class is an open militant),
  **greenbeard union** (both modal classes greenbeards of one spelling), **mixture** (one greenbeard, one open),
  **unconditional** (no militant: held by the boss alone). The holders' spellings are reported (source identity).
- **Closed shop's share of the boss slot**: the fraction of boss individuals (pooled per run, then averaged over runs)
  whose class pays ½ to (T₁, T₁) and less than ½ to (T₁′, T₁′) with the same inventories (it reads the named quote).
- **Identity island**: a fair or held island whose modal triple's play changes when every identity atom is evaluated
  as false (the sham semantics on the same individuals).
- **Exits of fair islands** (first exit after fair, per island), classified from the per-check modal classes and play:
  *unread-slot drift then boss cut*, *boss cut*, *worker drift*, *migration* (realizable definitions); and from the
  executable audit: *timeout* (the exit play differs from the ideal play of the same modal triple), *production
  failure* (the modal triple's play is not fair only because a member lacks a script its source can produce),
  *false certificate* and *substitution* (0 by S^cert₃ and Lemma Sub′; the audit must find none).
- **Cross-island P(fair)**: the probability that a triple with each slot drawn from a different uniformly chosen island
  plays fair. **Cross-island union compatibility**: over pairs of fair islands held by greenbeard or open-militant
  pairs, the fraction of worker swaps (w1 from one island, w2 from the other, either boss) that stay fair.
- **Production statistics** (S-nonself₃): acquisitions per set, waiting (encounters from birth to first acquisition),
  attempts, cap timeouts, fuel timeouts, NONE results, gate refusals, SPO scripts held (0 expected).
- **Run-level uncertainty**: Wilson intervals on run-level outcomes; bootstrap over runs (2,000 resamples) for means
  of island fractions; paired contrasts by replicate (same founder streams): mean paired difference with a bootstrap
  interval and, for binary outcomes, the exact McNemar p.

### 1.9 Executable dynamics and their validation

The S-nonself₃ cells run on executable values (§1.7) at K = 10⁶ (timeouts play the default: a TO check reads as F, a
global timeout plays the role's default; no catalogue play times out globally), with production charged and capped.
The H cells run on executable values too (so the H/S₃ contrast is paired on one semantics); the H + no-eq cell is
also run on the ideal table as the link to the realizable run, labelled ideal. **Validation plan (before any counted
cell):** (1) the abstract ideal evaluator equals the host replay on sampled checks with inventories and identity
atoms; (2) PROD3 by the term equals its host mirror on every named class and on sampled (type, encounter) pairs;
(3) the composed required cost equals the term's step count exactly on sampled checks (≥ 2,000), plays and productions;
(4) **≥ 200 encounters replayed whole** (three plays and the productions by the term, with the actual programs and
inventories) drawn from smoke-run states, compared with the kernel's play, certification values, production results
and step counts; (5) the soundness audit: every T check in the samples compared with the actual run of its subject
(0 false atoms expected). Agreement rates are reported; a mismatch class found here is fixed in the model before any
counted cell or, if not fixable, reported as a deviation.

### 1.10 Forced coalitions and local transition assays

- **Forced coalitions** (S-nonself₃ + eq): (i) a lottery cell with 20 founders per slot per island replaced by the
  coalition (D\*, T₁, T₁) with **empty** inventories; (ii) the same with **valid preloaded** inventories (T₁ with its
  [D] and [C] scripts, D\* with its =½ and ≥¼ ½-path scripts and ≤¼ 0-path script); (iii) a single isolated island
  (I = 1, no migration) of the pure coalition, empty vs preloaded, 40 replicates each, 2,000 generations. Hand
  prediction: (iii)-empty never becomes fair (Claim N₃'s cousin: the gate refuses every T₁ production on a monomorphic
  island), (iii)-preloaded stays fair; (i) and (ii) both establish (in a mixed island T₁ meets non-copies at once).
- **Local transition assays** (forced one-step transitions at a fair state, both semantics where they differ): from
  the named fair states F\*, (B_eq, T₁, T₁), (pay(½), U_eq, U_eq), (B_id, U_eq, U_eq), and from a sample of the
  lottery's fair islands at the horizon (modal triples): **unread-slot substitution** (w2 replaced by a scab; then by
  each worker class ∝ prior: immediate play, wage change, the entrant's relative payoff), **boss replacement** (the
  boss replaced by pay(0, none), pay(¼, none), B_eq, D\*, ∝ prior: the entrant's relative payoff, strict / neutral /
  deleterious), **union invasion** (U_eq, XM, T₁, scab entering each worker slot: relative payoff). The causal
  sequence is classified as the composition of two steps: the substitution's sign, then the best boss replacement's
  sign at the substituted state (e.g. "neutral substitution → strict cut"). Under S₃ an entrant arrives with the
  inventory its source reaches after one encounter at that state (production applied) and with an empty one; both
  are reported.

### 1.11 Cells

(N, I) = (100, 64), mN = 1, w = 0.3, r = N/3, horizon 2,000, checks every 10 generations, 40 runs per cell on paired
founder streams (cells of one grammar share founders; the eq, sham and eq-without-⌜T₁⌝ grammars share them through the
spelling bijection; the no-eq grammar shares the stream only):
1. H + no eq (executable; and the ideal table, labelled);
2. H + eq;
3. H + sham (the matched-prior identity-disabled control);
4. H + eq without ⌜T₁⌝;
5. S-nonself₃ + no eq;
6. **S-nonself₃ + eq** (the fully realizable cell);
7. S-nonself₃ + eq at (200, 64), 20 runs (finite size);
8. forced coalitions (§1.10 (i), (ii)) and the isolated-island assays ((iii));
9. extra, labelled, if budget allows: S-nonself₃ + sham (the matched control under endogenous production).

Statistics per cell: everything of §1.8 at 2,000 and (separately) at 10,000; the static tables; the cost model
realized. The lottery is ε = 0 evidence at finite (N, I, horizon); island-level efficiency, productive efficiency and
wage fairness are reported separately.
