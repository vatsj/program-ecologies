# Queue 79: certified offers in majority division (engineer's notes)

Spec `specs/2026-11-15-certified-offers.md` (both reviews folded). Section 1 is written after building the catalogue's programs and
smoke-testing a handful of plays (disclosed below), and before any gate, assay or counted cell.

*Disclosure.* Before writing this section I ran (a) the check on the carriers and forgers in both machines, (b) eleven hand triples
under C1 and C0, and (c) one table row per program type for timing. Nothing else was looked at. Section 1.4 quotes what (a) and (b)
showed, because κ is set from them.

## 1. Design and the structural soundness argument

### 1.1 What a certificate is here

Code: `src/certified_offers.py` (imports queue 78's catalogue; edits nothing existing). Two library entries are appended to
`lt_code`'s library (milestone 3's indices unchanged):

- `CARRY cert fb me n p`: the certified rule. `cert = (fn . (fp . pref))`, three bits: fn = 1 offers toward next, fp = 1 toward prev,
  pref 0 = next, 1 = prev. It computes
  E = {next : fn = 1 and CHK(⌜n⌝, 1)} ∪ {prev : fp = 1 and CHK(⌜p⌝, 0)},
  names the preferred member of E at ½ if |E| = 2, the only member at ½ if |E| = 1 (code 1 = next, 4 = prev), and otherwise
  evaluates `fb me n p`.
- `CHK (x . w)`: T iff the quote x has the **carrier skeleton**
  `λme. λn. λp. (((((lib CARRY) CERT) FB) me) n) p`, where CERT is a literal `(pair (nat b) (pair (nat b) (nat b)))` with every
  b ∈ {0, 1}, FB is a λ (a value), the three trailing arguments are the bound variables v2 v1 v0 in that order, and the head is
  the library index of `CARRY` itself; and x's flag toward my side is 1 (w = 1 reads x's fp, used when x is my next, so I am its
  prev; w = 0 reads x's fn).

A **carrier** is any program whose quote passes the skeleton test. Its **certificate** is the literal CERT; its **fallback** is FB.
The "script" of the spec is degenerate here: the statement is the certificate, and its proof is the skeleton itself, because the
code that executes the statement is one shared library term. This is milestone 4's "call skeleton" convention pushed to the whole
body. The spec's statement form ("my eligibility set E is the partners whose certified rule makes me eligible for them; if E is
non-empty I name my preferred member of E at ½; otherwise I play my fallback") is exactly `CARRY`'s code.

**Machines.** C0: `CHK` is the L_T^code term in `CO_SRC` (a walk of the quote by `fst`, `snd`, `eq`, `lt`), charged step by step.
C1: `CHK` is a primitive with the same input-output map (`host_skel`), charged KAPPA ticks plus the application tick. The quotes are
identical in both machines (the same library index), so C0 and C1 differ only in what a check costs. Dynamics run on C1 tables.

### 1.2 The statement

For an accepted program t with certificate (fn, fp, pref) and fallback FB, in any profile where t is run as
t ⌜t⌝ ⌜x⌝ ⌜y⌝ (x its next, y its prev) with root fuel KR = 1,200:

**S(t).** Let E = {next : fn = 1, x accepted, fp(x) = 1} ∪ {prev : fp = 1, y accepted, fn(y) = 1}. If |E| = 2, t returns code 1 if
pref = 0 and 4 if pref = 1; if |E| = 1, it returns 1 (next) or 4 (prev); if E = ∅, it returns the value of `FB ⌜t⌝ ⌜x⌝ ⌜y⌝`
evaluated inside `CARRY` with the fuel left (and plays code 8 if that value is not an action code, as every program does).

The certified, relied-on part is the E ≠ ∅ branch. The fallback clause only says that t plays its fallback, run with reduced root
fuel (the check overhead, at most about 150 steps in C1 and 400 in C0, is spent first).

### 1.3 Soundness (structural; the gates are regression tests)

**Lemma 1 (the check map).** The C0 term and the C1 primitive compute the same total function of the quote (`host_skel` followed by
the flag read). The C0 term reads a bounded prefix of the quote: three λ tags, five application nodes, three variable leaves, one
library leaf, one λ tag, and the certificate's five leaves. It recurses nowhere, calls no `run`, `capk` or `sim`, and so terminates
in a bounded number of steps on every quote (measured: 167–168 on accepted quotes, 24–134 on rejected ones). Every rejection branch
returns 99 → F, and the only accepting branch builds the triple from the three leaves after checking each is a natural number below
2. The Python map is the same decision list. Gate 1 checks the two maps agree on every catalogue program and forger, for both w.

**Lemma 2 (binding).** If t is accepted, t's root evaluation is CARRY applied to t's own CERT and FB and to the three quotes it was
given, in the frame's order. *Proof.* Acceptance fixes t's body syntactically: three λs, then
`(((((lib CARRY) CERT) FB) v2) v1) v0`. Under the call-by-value evaluator the three outer applications bind me, n, p. The body then
evaluates `lib CARRY` (a value), the literal CERT (a pair of naturals, a value after its pair steps), FB (a λ, a value; this is why
an application in FB's place is rejected: it could diverge or depend on evaluation), and the variables. The head is CARRY's index,
not any other library entry (a lookalike combinator, FAKECARRY, is rejected by the index test). So the values reaching CARRY are
t's own certificate and fallback and the quotes ⌜t⌝, ⌜x⌝, ⌜y⌝ in the right order (the order test rejects swapped variables).

**Lemma 3 (the rule).** CARRY's code computes E by at most two CHK calls on ⌜x⌝ and ⌜y⌝ and returns as S(t) states. CHK depends
only on the partner's quote: no simulation, no reference to anyone's play, no reference to t's own quote. Hence no fixed point,
no mutual regress, and no dependence on what the partner will do; the pair rule is a symmetry (both sides compute E from the same
two certificates), as in milestone 4.

**Fuel.** At root (KR = 1,200) the E ≠ ∅ branch costs at most 3 + (certificate steps) + 2 × (check) + (CARRY's own steps): about
150 steps in C1 and about 360 in C0 (measured on hand triples below), so the certified branch can never run out of root fuel. Inside
another program's simulation the same evaluation may be cut by the simulator's cap; that is the simulator's read timing out (it
sees TO), not a false statement about t's play. Fuel exhaustion in the fallback branch is part of "plays its fallback".

**Competing offers.** Two eligible partners: the preference bit picks one, as S(t) states. The partner not chosen may still name
t at ½; then no pair forms between them. Mutual naming is derived, not certified: carriers A and B form the fair pair iff each is
the other's chosen member. Three mutually pointing carriers form a cycle in 2 of the 8 preference triples (all pref next or all
prev), as the spec records.

**Theorem (unconditional soundness).** For every accepted t and every profile, t's root play satisfies S(t). (Lemmas 1–3 and the
fuel bound.) Nothing in the argument depends on the catalogue: the gates' catalogue cube is a regression test of the code.

**The faker.** Bc (a carrier whose fallback is the simulating bully) is accepted and its certificate is true: it offers ½ to every
carrier that points at it and bullies only in its fallback. Certificates cannot exclude it, by construction.

**Incompleteness (not unsoundness).** Certification is syntactic. A program that implements the same rule with different spelling
(an inlined copy of CARRY's body, the skeleton under an `if T`) is rejected. The certifiable programs are exactly {skeleton(cert, FB)}:
8 certificates × any λ fallback. This is the "the model can't express" item for this queue: a certified rule spelled in any other
way, or any certified statement other than the conditional ½ offer.

### 1.4 κ and C0's cost (recorded before the gates)

- **κ = 50 ticks** per check in C1 (plus the application tick: 51 measured), the spec's upper bound cap/8 with the cap KS = 400.
  With it a simulated carrier's E-branch costs 70–125 steps and its fallback branch 70–144 steps plus the fallback, so a carrier whose
  fallback is a constant is legible to any simulating reader within one outer cap.
- **C0's check cost** (the written-out term, measured): 167 (w = 0) and 168 (w = 1) on accepted quotes; 24 (non-λ heads such as a
  constant), 39 (simulating readers), 41–134 (forgers) on rejections. C0 is therefore about 3.3× dearer per check than C1. V3 compares
  C1's and C0's tables at the same caps and classifies every disagreement; where a check's cost decides a read (a carrier simulated
  inside a cap), C1 is the idealized primitive and the conclusion is labelled as holding for it.
- Hand triples (disclosed): under both machines (Bn, Rcn, Ocp) is the fair pair (Rcn, Ocp) with the bully's read of Rcn completing;
  (Bn, Rcn, Snzn) stays unequal with no timeout; (FcSnzn, FcSpzn, C8) is the fair carrier pair; (FcSnzn)³ is the all-next cycle;
  (Bn, Rcsn, Snzn) times out (the hybrid re-creates the regress).

### 1.5 Programs (appended after queue 78's 59; the first 59 unchanged; K = 87)

| family | names | certificate (fn, fp, pref) | fallback |
|---|---|---|---|
| Oc (c_open) | Ocn, Ocp | (1,0,0), (0,1,1) | C1, C4 (the ½ constant naming the offered partner) |
| Fc (c_firm) | Fc + each of T's 16 firm readers (8 singles, 8 two-partner) | (1,1, first-read direction) | that firm reader |
| Rc (c_acc) | Rcn, Rcp | (1,0,0), (0,1,1) | C3, C0 (⅓ to the other partner) |
| Rcs (c_accs) | Rcsn, Rcsp | (1,0,0), (0,1,1) | Rnn, Rpn (queue 78's R) |
| Bc (c_bully) | Bcn, Bcp | (1,1,0), (1,1,1) | Bn, Bp |
| Pc (c_prud) | Pc + Pnzy, Pnzn, Ppzy, Ppzn | (1,1, read direction) | that prudent reader |

Matched orientation in a bully-held unequal island: with the simulating bully Bn in slot b, the victim sits in b + 1 and the excluded
slot is b + 2 = the victim's next, so the matched accepter is Rcn and the matched certified offerer in e is Ocp (it offers toward its
prev, the victim); mirror for Bp (Rcp, Ocn). Fc offers toward both partners and needs no orientation.

Forgers (gate 1 only): XmBn (the bully's body with Ocp's certificate data in milestone 4's carrier shape), XfakeBn (the skeleton
calling a lookalike combinator that ignores the certificate), XswapBn (n and p swapped), XappBn (fallback an application), XbitBn
(a flag of 2), XopBn (a computed flag), XifBn (the skeleton under `if T`), Xconst (returns certificate data as its value).

## 2. Deviations and implementation choices

- Worktree fast-forwarded to `main-t69lqz` (7bf523b) before starting.
- The certificate system is a skeleton-bound shared combinator (section 1.1), not milestone 4's script checker over a
  self-interpreter. The spec's "script" is the certificate literal; the proof obligation is discharged by the skeleton. C0 is the
  skeleton check written out in L_T^code; it was built (V3 is therefore not the time-boxed failure branch), but a milestone-4-style
  checker that certifies arbitrary spellings of the rule was not built.

## 3. Operations log

## 4. Budget
