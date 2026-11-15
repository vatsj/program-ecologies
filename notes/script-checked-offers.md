# Queue 80: script-checked offers in majority division (engineer's notes)

Spec `specs/2026-11-16-script-checked-offers.md` (both reviews folded; the section "Amendments after the second review" overrides).
Section 1 was written after building the checker and the catalogue's programs and before any gate was run. Code:
`src/script_offers.py` (library, machines, programs, host reference, tactic), `src/script_offers_cat.py` (catalogues, forgers, S1
table, execution tables).

*Disclosure (what was run before this section).* RE 1 was committed first (8d6bfb3), before any code. Then, while building: (a) the
check (S0 and the host reference) on every carrier and statement code, twice (a first direct-style evaluator, then the
continuation-passing one in the code), to measure costs; (b) the 23 forgers against S0 and the host; (c) timing rows of the
execution tables (8 programs × 625 sampled profiles, S0 and S1, regress key on and off); (d) the exactness test of the regress key
(section 2). No gate table, assay, mass or dynamics cell had been computed.

## 1. Design and the structural soundness argument

### 1.1 Carriers and the packaging

A **carrier** is any program together with a script. The packaging (the gene convention, a fixed syntactic frame for where a script
lives, not for how the program is spelled) is

    λme. λn. λp. (if T B SCRIPT)

The root evaluation contracts the `if` (one tick) and evaluates B; SCRIPT, a data literal of nested `pair` and `nat`, is never
evaluated by the program. B is any L_T^code term. A program without the packaging has no script; every check of it is rejected.

### 1.2 Statements, the open atoms, the eligibility predicate

Statement codes c, asked about the checked program x (x is run as x ⌜x⌝ ⌜n⌝ ⌜p⌝, n its next, p its prev):

| c | statement |
|---|---|
| 1 / 2 | x holds an offer toward its next, **S_off(next; R)**, with requirement R ⊆ h, h = ∅ / {S_nx} |
| 3 / 4 | the same toward its prev |
| 5 | **S_nx**: in no profile does x play an action with demand ⅔ (codes 2, 5, 8; a non-code value, a stuck term or exhausted root fuel plays 8) |

`chk(y, c)` denotes the value (T or F) of the library call `CHKS (⌜y⌝ . c)`. These values, for y ∈ {n, p} and literal c, are the
**open atoms** of a derivation. (Inside a partner read, an unknown read result h compared by `eq` with a concrete number or constant
is the other kind of open atom; see 1.4.)

**Eligibility (one predicate; used verbatim in code, statement and proof).** For x with declared parameters (O_x, pref_x, H_x, R_x)
(O_x ⊆ {next, prev} the sides it offers toward, H_x ∈ {∅, {S_nx}} its declared holding, R_x ∈ {∅, {S_nx}} its requirement), the
partner s ∈ {n, p} is in x's eligibility set E_x iff

    s's side ∈ O_x   and   chk(s, OFF(toward x; h = H_x)) = T   and   (R_x = {S_nx} → chk(s, NX) = T).

The second conjunct is "s holds an offer statement toward x's slot whose requirement x holds" (elig(s, x)'s offer part and elig(x, s)'s
requirement part); the third is "s holds every statement in x's requirement"; the first is x's own offer (elig(x, s)'s offer part).
With truthful parameters, s ∈ E_x ⟺ x ∈ E_s (the spec's E_y = {x : elig(x, y) and elig(y, x)}). OFF(toward x) is code 3 + H on n
(x is n's prev) and 1 + H on p.

**S_off(d; R)** (with x's parameters): *if d ∈ E_x and (pref_x = d or the other partner ∉ E_x), x names d at ½* (code 1 for next, 4
for prev). The statement is quantified over every profile (n, p). **S_nx**: *x's root play is never in {2, 5, 8}*.

The script entry for S_off carries the parameters (R, H, O as two bits, pref); the checker requires R ⊆ h for the asked code and
d ∈ O (an entry offering nothing toward d cannot pass as an offer toward d).

### 1.3 The checker CHKS (S0)

Library (appended after queue 79's; `CHK_SRC` in `src/script_offers.py`):

- `CHKS (x . c) = (if (eq (capk KCHK CCORE (x . c)) T) T F)`. It returns T or F in at most KCHK + 5 ticks in every context (one
  application, one `capk` tick, at most KCHK + 1 inside the frame, one exit tick, `eq`, `if`). KCHK = 16,000.
- `CCORE (x . c)`: reads x's quote (three λ, then `if` with the literal condition T), converts the third branch to data, finds the
  entry of the asked kind, checks the parameter conditions, and walks the entry's tree:
  - the tree's nodes are LEAF (0 . 0), SPLIT (1 . (t_T . t_F)), VAC (2 . 0);
  - at each node the checker resumes the symbolic evaluation of x's body (`sev`, continuation-passing; section 1.4) under the
    literals of the path; if the evaluation stops at an unassigned atom, the node must be SPLIT (both values are then explored, each
    child resuming the same continuation with the literal added) or VAC; if the evaluation reaches a value, the node must be LEAF or
    VAC; if it is rejected, the whole check fails;
  - LEAF accepts iff the statement's guard is false under the path's literals or (the counted ticks ≤ KR' and the value is in the
    statement's mask: {1} for S_off(next), {4} for S_off(prev), {0, 1, 3, 4, 6, 7} for S_nx); VAC accepts iff the guard is false.
  - The guard is evaluated in Kleene three-valued logic over the literals (unassigned atoms unknown): "false" means false for every
    completion. S_nx's guard is T.
- CCORE contains no `capk`, `run`, `sim` and calls no CHKS: **it reads no one and runs no one**. It is not recursive through CHKS.

Reused: milestone 4's architecture (a carried script checked by a shared library entry against the carrier's own source; case splits
on check atoms (its ChkR) between deterministic evaluation segments (its EvR*); the check wrapper as a bounded `capk` around a core)
and lt_code's term encoding and evaluator. Not reused: milestone 4's `cstep` self-interpreter (it steps closed configurations by
substitution and cannot keep a partner's quote opaque; it would also cost about 20 ticks per object step and per context level) and
K_3's three-quote wrappers (its checks concern pairwise play against given partners; here statements quantify over all partners).

### 1.4 The symbolic evaluator and the soundness argument

`sev` evaluates x's body with the environment (p, n, me) = (opaque partner 1, opaque partner 0, ⌜x⌝) and counts ticks exactly as the
compiled evaluator charges them (`app` 1, `if` 1, `fst`/`snd` 1, `eq` 1, `op` 1, and 0 for variables, λ, literals, pairs, quotes,
library constants), plus three ticks for the frame's three applications. Its values are numbers, constants, pairs, closures,
quotes (concrete), library entries, the two opaque partners, and havoc values. It rejects (the whole check fails) on every operation
whose concrete outcome it does not model:

| construct | S0's symbolic rule |
|---|---|
| application of a closure or a library entry other than CHKS | as the evaluator (library bodies via `libsrc`) |
| `CHKS (s . c)`, s an opaque partner, c a number | atom (s, c): its literal if assigned, else stop (need); charged KCHK + 5 |
| `capk k f v` with k a number and f a havoc value | a fresh havoc value; charged k + 2 |
| `run k x y` with k a number, x an opaque partner, y an opaque partner or a quote | a fresh havoc value; charged k + 2 |
| `eq a b`, both numbers / constants | as the evaluator |
| `eq a b`, both concrete quotes | as the evaluator (canonical equality) |
| `eq h v` with h havoc and v a number / constant | literal (h, v), else stop (need) |
| anything else on an opaque partner or a havoc value (`fst`, `snd`, `if`, `op`, application, `eq` with a quote or a partner) | reject |
| `fix`, `sim`, `libsrc` in the body, `capk` / `run` on concrete arguments, `CHKS` on anything but (partner . number) | reject |
| `op` as the evaluator (division by zero rejects) | |

**Lemma 1 (atoms are functions of the partner's quote).** At root, `CHKS (⌜y⌝ . c)` evaluates CCORE inside its own `capk` frame. CCORE
pushes no frame, reads no partner and calls no CHKS, so its run depends only on (⌜y⌝, c) and the frame's deadline; at root no enclosing
frame exists except those the carrier itself pushed and closed earlier, and the regress key of the `capk` (CCORE, KCHK, arg) cannot be
active (CCORE never calls CCORE). Hence the value is chk(y, c), the same in every profile and in every call of the same path, and the
call costs at most KCHK + 5 ticks.

**Lemma 2 (reads).** At root, a `capk k f v` or `run k x y` frame entered at tick u returns control by tick u + k + 2 (the deadline is
u + 1 + k; a SimTO on it returns TO, a normal return or a Stuck inside costs one exit tick; the regress fast-forward and the cache
replay jump to the smallest active deadline, which is inside the frame). The returned value is some value or TO: havoc covers it.

**Lemma 3 (simulation).** Along any path (an assignment of the atoms and havoc literals), every concrete step of `sev` is the
evaluator's step on the same values, every havoc or atom stands for the actual value (which satisfies the path's literals), and the
counted ticks are an upper bound of the actual ticks (exact for concrete steps, upper bounds k + 2 and KCHK + 5 for reads and atoms).
Each rejected construct is excluded, so no path of the actual root evaluation leaves the modelled fragment unnoticed: when the actual
evaluation does something `sev` rejects, the check fails.

**Lemma 4 (fuel).** If a LEAF's counted ticks are ≤ KR', the actual root evaluation on every profile consistent with the path finishes
within KR' ticks and returns the leaf's value (no OutOfFuel, no stuck term).

**Theorem (unconditional soundness).** If CCORE accepts (x, c), then for every profile (n, p) the root play of x with fuel KR' satisfies
the statement asked by c. *Proof.* Fix a profile; it determines every atom's value (Lemma 1) and every read's actual result. The tree's
SPLIT nodes partition the atom/havoc assignments, so the actual evaluation follows one root-to-node path consistent with its
literals. If that node is VAC (or a LEAF accepted through its guard), the guard is false under literals that the profile satisfies,
so the statement's premise is false in this profile. Otherwise the node is a LEAF whose counted ticks are ≤ KR' and whose value is in
the mask; by Lemmas 3 and 4 the actual root play is that value. Nothing depends on the catalogue; the gates' cube is a regression test.

**Not claimed.** Statements say nothing about play inside another program's simulation (a simulator's cap can cut the carrier off;
that is the simulator's read timing out). H_x is declared, not checked: a carrier that declares H = {S_nx} without holding S_nx only
hurts itself (partners requiring S_nx test chk(x, NX) directly and do not name it). Completeness is not claimed: S0 rejects sound
programs outside the modelled fragment (self-checks, identity tests, recursion, reads with concrete closures).

**Competing offers.** Two eligible partners: pref picks one (as the statement says). Mutual naming is derived: the pair forms iff each is
the other's chosen member. Three mutually pointing carriers may cycle (gate tables tabulate every orientation).

**The certified bully.** Bc (fallback the simulating bully) holds S_off honestly; it cannot hold S_nx (its fallback names ⅔). A carrier
with R = {S_nx} (Pc⁺; A5's OcR⁺, RcR⁺) excludes it; carriers with R = ∅ still pair with it.

### 1.5 S1

S1 replaces CCORE's code by a primitive with S0's input-output map and S0's exact tick count c(x, code), both tabulated on the
catalogue and the forgers (rejections and stuck runs included; 795 + 115 entries). The primitive applies lt_code's replay rule: if
the remaining fuel to the first deadline (root fuel or any open frame) is below c, it fails at exactly the tick at which S0's run would
fail (same exception, same tick count); otherwise it advances c ticks and returns the value. Because CCORE in S0 pushes no frame,
touches no other machine state and ticks one at a time in the frame of its caller, S1 and S0 are identical in every context (values,
tick counts, timeouts, failed-read counts). V3 tests this on the tables and at residual fuel c − 1 and c for every tabulated check.

### 1.6 Costs and fuel (recorded before the gates)

S0's check cost per (program, code), continuation-passing evaluator: accepted checks 1,668 – 15,141 ticks (Oc/Rc 1.7–3.9k; Fc/Bc
3.1–7.2k; Oc⁺/Rc⁺ 1.8–3.9k; Fc⁺ 4.0–7.6k; OcR⁺/RcR⁺ 2.8–5.4k; Pc⁺ 10.6–15.1k; the canonical and guard spellings dearest, `noelig`
cheapest); rejections 23 (no packaging) to 6,937 (a forger). **κ_S = 15,141** (Pc⁺Spoy.guard, S_nx). The first, direct-style
evaluator (re-evaluating each path from the root) cost up to 166,456 on the same check; it was replaced before any gate.

Fuel: KCHK = 16,000 (the smallest multiple of 1,000 above the worst catalogue check, rejections and forgers included); per-call bound
W = KCHK + 5 = 16,005. **cap' = 8 × KCHK = 128,000** (≥ 8 κ_S = 121,128; a simulated carrier's checks, at most four, plus a fallback
reading a constant fit in one read). **KR' = 3 cap' = 384,000.** Every program of both worlds runs at (KR', cap'): queue 78's 59
programs with their read caps rewritten from 400 to 128,000.

### 1.7 Programs

World S (A arms; K_S = 159): queue 78's 59 at cap', then 10 families × 2 directions (or fallbacks) × 5 spellings:

| family | params (O, pref, H, R) | fallback | holds |
|---|---|---|---|
| Oc n / p | next / prev only | C1 / C4 (½ naming the offered partner) | S_off |
| Rc n / p | next / prev only | C3 / C0 (⅓ naming the other partner) | S_off |
| Fc Snoy / Spoy | both, pref = the reader's direction | the firm reader Snoy / Spoy | S_off ×2 |
| Bc n / p | both, pref n / p | Bn / Bp | S_off ×2 |
| Oc⁺, Rc⁺, Fc⁺ | as above, H = {S_nx}, R = ∅ | as above | S_off, S_nx |
| Pc⁺ Snoy / Spoy | both, H = R = {S_nx} | Snoy / Spoy | S_off ×2, S_nx |
| OcR⁺, RcR⁺ (A5) | as Oc⁺, Rc⁺ with R = {S_nx} | as Oc, Rc | S_off, S_nx |

Spellings (all implement the same rule; all but `canon` and `guard` avoid `lib OFFER`; every one is rejected by queue 79's skeleton
check): `canon` ((((((lib OFFER) CERT) FB) me) n) p) — the shared library rule; `inl` OFFER inlined with constants folded,
eligibility through `lib ELIG`; `rord` inlined with the prev partner's test first and the branches reordered; `guard` the canonical call
under `(if T … 0)`; `noelig` inlined with direct CHKS calls. Scripts are produced by a host tactic (the host reference evaluator,
written independently in Python, explores the paths) and checked by S0; scripts are 23–209 data nodes.

Fallback pool: the firm readers Snoy and Spoy (fallback o, timeouts accepted; one per direction). S_nx is derivable for T's four
single readers with fallback o (Snoy, Snon, Spoy, Spon) and for none with fallback z (they play 8); for the two-partner readers it is
not derivable at KR' = 3 cap' (two worst-case reads cost 4 cap' + 8 > KR').

World K (K, K2; K_K = 99): the same 59, then queue 79's skeleton carriers built with `CARRY` and the same fallbacks (Oc n/p, Rc n/p, Fc
Snoy/Spoy, Bc n/p) in five spellings: `canon` (queue 79's skeleton, accepted by CHK) and four that CHK rejects: `inl`, `rord`, `guard`,
`alias` (CHK through a let-bound name). Non-canonical K-world programs are written as their authors would write them: they call CHK on
partners, so they see canonical partners' certificates while being invisible themselves (one-sided offers), and act as their fallbacks
among themselves. The spec's phrase "so they act as their fallbacks" holds only among non-canonical programs; deviation, section 3.

Forgers (gate rows only): queue 79's eight verbatim (no packaging), and fifteen script forgers (`forgers_s`): a valid script on
another program (Ocn's script on the bully); Fc⁺'s script on Bc's body (offers true, S_nx false); FAKEOFFER with Bc's script; n and p
swapped; S_nx on a program that plays 8 only when its read exhausts the root fuel; a tree node asserting an atom; VAC where the guard
can hold; a program that names prev when next is the eligible preferred partner; malformed and computed scripts; self-certification
(CHKS on me); an identity test; recursion; inspection of the partner's quote; and the ½ constant with true one-leaf trees (allowed).

## 2. Engineering deviations and implementation choices

- **The closure regress key (an evaluator extension).** At cap' = 128,000 a mutual read between simulating readers is a tower of
  `capk` frames whose function is a closure; lt_code gives such frames no regress key, so the tower runs level by level to the
  outermost deadline (about 90 ms per profile at cap', against 1 ms with the key; the table cube has 4·10⁶ profiles). `do_capk_keyed`
  gives closure frames the key (cap, canonical closure, canonical argument, type-aware), so milestone 3's regress lemma fast-forwards
  them exactly as it already does `run` frames. Exactness test (`src/script_offers_exact.py`, `runs/script_offers/exact.json`):
  queue 78's 59-program tables at the old fuel rebuilt with the key equal the stored ones in action code and steps on all 205,379
  profiles; failed-read counts differ on 928 profiles, **every one containing Jr** (a cap-0 read that fails at every tower level; the
  counter counts timeouts inside nested simulations, and the key skips repeated levels). Jr has zero mass in every law of queues
  78–80. At the new fuel, 300 sampled world-S profiles agree exactly with the key on and off. All tables of this queue, at both fuels,
  are built with the key on.
- **Execution steps are stored as int32** (KR' = 384,000 exceeds int16).
