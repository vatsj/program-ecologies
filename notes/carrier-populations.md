# Populations of carriers: the realizable language, milestone 2 (notes, 2026-10-06)

Spec `specs/2026-10-06-carrier-populations.md` (reviewed by gpt-6.1-sol; the [after review] text is the resolution).
§1 is written before any project code of this milestone and before any counted cell: the grammar and its counting,
production, the reduction that makes the play table computable and the lumping criterion, the named classes with
their hand-derived plays, establishers, shadows, suckers, exploitation and bridges, the priors, the chain and the
lottery endpoint. §1.10 (code validation of the hand derivations) is appended after the code exists and before any
counted cell; §2 (costs) after that. Base: `notes/certificates-as-code.md` §1 ("milestone 4"), whose calculus
K_T^cert, checker term, frozen production tactic and host replay checker are used unchanged (imported from
`src/lt_cert.py`, not modified).

*Disclosure.* Before writing this section I ran a scratch enumeration (not a cell, nothing about plays) to learn how
many distinct run trees the grammar has, because that number decides which computation of the play table is
feasible (§1.4). The counts are reported in §2.

## 1. Design

### 1.0 Scope (after review)

This is a **finite template ecology run inside a Turing-complete evaluator**. Programs are templates over check
atoms (§1.1) compiled to L_T^code terms; their certificate lists are supplied by milestone 4's frozen host tactic,
which is not charged to matches. The experiment tests whether *executable verification* (checks run by the
language's own evaluator, charged step by step) supports the population results of the modal arm. It does not test
unrestricted program evolution or endogenous certificate discovery, and the write-up says so.

### 1.1 The grammar

Two sorts. **Actions** A ::= `C` | `D` | `if(B, A, A)`. **Conditions** B ::= atom | `not(B)` | `and(B, B)` |
`or(B, B)`. **Atoms** `CHK_e(p, q, a)` with p ∈ {them, me}, q ∈ {me, them, ⌜C⌝, ⌜D⌝}, a ∈ {C, D}: "the checker
certifies that p's run against q's quote returns a". Under P and O, e = 0 (the sound checker CHK_S); under E,
e ∈ {0, 5} (5 the sound copy CHK_S2, identical code at another library entry). Nodes: one per constant, atom and
connective (`if`, `and`, `or`, `not`); the entry label is not a node for the cutoff (it is priced in the prior, §1.6).
So CB = `if(CHK(them, me, C), C, D)` has 4 nodes and CBP = `if(CHK(them, me, C), if(CHK(them, ⌜D⌝, D), C, D), D)` has 7.

**Cutoff (prespecified): n = 7.** Fallback n = 6, a different experiment if used.

**Counts by hand.** Let b(n) be the number of conditions and a(n) of actions with exactly n nodes, over an alphabet of
k atoms. b(1) = k, b(n) = b(n − 1) + 2 Σ_{i+j=n−1} b(i) b(j); a(1) = 2, a(n) = Σ_{i+j+l=n−1} b(i) a(j) a(l).
With k = 16 (P): b = 16, 16, 528, 1552, 35856; a(1..7) = 2, 0, 0, 64, 64, 2112, 10304.

| catalogue | n ≤ 5 | n ≤ 6 | n ≤ 7 |
|---|---|---|---|
| P (k = 16) | 130 | 2,242 | 12,546 |
| O (each spelling with list `none` or `produced`) | 260 | 4,484 | 25,092 |
| E (k = 32) | 258 | 8,578 | 49,666 |

(E: a(4) = a(5) = 128, a(6) = 8,320, a(7) = 41,088.) At n ≤ 7 an action has at most two atoms (three atoms need
`and(·, and(·, ·))` plus `if` and two leaves: 8 nodes), so every run makes at most two check calls.

**Compilation.** A spelling compiles to the carrier `λme. λthem. (λcerts. BODY) CERTS` of milestone 4 (inside BODY:
certs = v0, them = v1, me = v2), with `C`, `D` the constructors, `if` native, `not(B) = if B then F else T`,
`and(B1, B2) = if B1 then B2 else F`, `or(B1, B2) = if B1 then T else B2`, and the atom the check call
`app(lib CHK_e, (V, (P, (Q, (a, K)))))` exactly as milestone 4's `CALL` (P, Q the variables me/them or the literal
quotes of milestone 4's plain `PROG_C`, `PROG_D`, which carry no list). K = 10⁶, V = ⌊K/4⌋ in every source. A play is
the actual run of `p ⌜p⌝ ⌜q⌝` under K; a non-constructor result (⊥, a global timeout) scores as D.

### 1.2 Production

Milestone 4's frozen tactic and two-pass procedure (`lt_cert.produce_list`), unchanged: a program's D script is
produced against ⌜D⌝ with an empty list; its C scripts against the probes CB, CB1, CBP (milestone 4's sources, which
carry their own C and D scripts), in probe order, distinct scripts only; list = C scripts then the D script. The
probe sources are milestone 4's `body_CB/CB1/CBP` at (K, V); the catalogue's spelling of CB is the same term as the
probe's body. Skeletons for which the tactic finds nothing get an empty list (reported with their mass).

- **P (public):** every spelling carries its produced list at no node cost.
- **O (optional):** every spelling exists twice, with `none` (empty list, the CB0 type) and with `produced`.
- **E (entry):** production in mode 0 against the entry-0 probes, then in mode 5 against the entry-5 probes
  (CB, CB1, CBP with CHK_S2), distinct C scripts in that order, then the distinct D scripts (mode 0, mode 5).

Production effort (tactic nodes, host check emulations, host time) is measured per skeleton (§2).

### 1.3 Run trees, τ-types and the symmetry lemma

**Run tree.** dt(x) is the decision tree of x's run: dt(C) = C, dt(D) = D, dt(if(B, X, Y)) = bt(B, dt(X), dt(Y)) with
bt(atom, t, f) = node(atom, t, f), bt(not B, t, f) = bt(B, f, t), bt(and(B1, B2), t, f) = bt(B1, bt(B2, t, f), f),
bt(or(B1, B2), t, f) = bt(B1, t, bt(B2, t, f)). This is the order and branching of the check calls the run makes
(the compiled `if` chain makes exactly these calls). **τ(x) = (dt(x), list(x)).**

**Lemma T (τ-symmetry).** Let x ≠ x′ be spellings with τ(x) = τ(x′), and assume every check call of every run in
question has fit slack (f − u > 0 at the call; at K = 4V with at most two calls the slack is ≥ V). Then for every
check argument, replacing x by x′ throughout (and x′ by x) leaves the value of the clean run of every check
unchanged, and so every play: U(x, y) = U(x′, y) and U(y, x) = U(y, x′) for y ∉ {x, x′}; U(x, x) = U(x′, x′);
U(x, x′) = U(x′, x).
*Proof sketch.* A check consults its quotes only through (i) the self-interpreter's steps along the target's run,
which stop at the same call states with the same boxes up to the renaming (step counts differ, which matters only
through the fit side condition, slack assumed); (ii) `getcerts`, equal lists; (iii) syntactic equality of boxes
(Hyp: box = R or S; Ax: a box in both lists; fadd/fdel deduplication), which the renaming preserves because it is a
bijection on quotes; (iv) nested checks, by induction (regress is a repeated key, preserved by a bijection). ∎
So the spelling-level table is determined by a **τ-level table**: G(τ1, τ2) = the play of two *distinct* spellings of
types τ1, τ2 (including τ1 = τ2), and Self(τ) = the play of a spelling against itself. It is computed on one or two
representative spellings per type. Lemma T is tested on a random sample of spelling pairs executed directly (§1.10).

**The cutoff by τ-type.** Spelling count by hand above; the τ-type count is a property of the grammar reported in §2.

### 1.4 The two tables (executable and ideal) and how they are computed

- **Ideal (the matched ideal-verification control, after review):** every check answered by milestone 4's host
  replay checker (`HostCheck`) with no step cost (its EvR* budget removed), same sources, lists, cutoff, priors.
- **Executable:** every check is the clean run of the checker term at K = 10⁶ (V = 2.5·10⁵).

**Composition.** By Lemma N and E2^cert of milestone 4, in a play every check call returns its clean value when it
fits (always, here); a template's run is then its decision tree evaluated on those values, and the global counter
cannot run out (≤ 2 calls of ≤ V + 6 steps, plus fewer than 10³ other steps, < K). So a play is the composition
"evaluate dt(x) on clean check values". The tables are computed that way: the per-pair check matrices
chk_a(t, m) (a ∈ {C, D}) are computed only where some program asks them — x's atom (them, me, a) asks chk_a(y, x),
(me, them, a) asks chk_a(x, y); the per-program values chk_a(y, y), chk_a(y, ⌜C⌝), chk_a(y, ⌜D⌝) once per program
— and a target without an a-entry in its list gets F without running (the code returns F at `tryents` on an empty
selection; checked on a sample). Composition is validated against whole actual plays (`lt_code.play`) on every named
pair, on a sample of class pairs and on every pair of the n ≤ 5 sub-catalogue (§1.10).

**Order of computation (forced by size).** The ideal table is computed on every τ-type pair (host checks are fast);
the lumped classes (§1.5) are formed from it; the executable table is computed on the class representatives (term
checks are 10–100× slower); every class cell where the two tables differ is classified (§1.8). Executable and ideal
can differ only by a check exceeding its cap or a play exceeding K; the largest executable check cost, its margin to
V, and a direct-execution sample of spelling pairs (not representatives) are reported, so that "the executable
table equals the ideal on every spelling pair" is a measured claim with a stated margin, not an assumption.

### 1.5 Lumping (after review)

Two spellings x, x′ merge iff their payoff rows and columns against **every original spelling** agree, including the
self and cross-twin cells: U(x, z) = U(x′, z) and U(z, x) = U(z, x′) for all z ∉ {x, x′}, and U(x, x) = U(x, x′) =
U(x′, x) = U(x′, x′). With Lemma T this is computable at the τ level: a τ-type whose G(τ, τ) ≠ Self(τ) splits into
singleton classes (each spelling plays its twins differently from itself), and is reported; otherwise spellings are
merged by their τ-level rows and columns plus self. A class's prior mass is the explicit sum over its spellings.
ModalProvider's criterion on the spelling-level matrix (rows and columns of the full matrix equal) is the same
criterion; it is applied to the τ-expanded matrix.

**Small-catalogue verification (before any counted cell):** on the n ≤ 5 sub-catalogue (130 spellings, every pair
executed by the term), (i) the τ-composed table equals the direct table; (ii) the ε→0 chain over unlumped spellings
(each spelling its own class) and the lumped chain with twin drift (`LogChain(twins=True)`, IMPLEMENTATION 4) give the
same class-aggregated π and P(C,C) at N = 10³ and 10⁴ (to 10⁻⁶ relative on P(C,C)), and the lumped chain without
twin drift is reported beside them.

### 1.6 Priors (complete, after review)

- **L (main):** weight 2^−(nodes) per spelling, normalized over the catalogue. **O:** each of the two list choices
  costs one node (weight 2^−(nodes+1) each: the choice is one bit). **E:** one extra node per CHK_5 atom
  (2^−(nodes + #CHK_5)); **E-eq (second cell):** the entry is a fair bit per atom (2^−(nodes + #atoms)).
- **U:** every lumped class equal weight.
- *Flagged ambiguity.* The spec calls L "the length prior on node counts (the standing μ)" and then specifies
  2^−(nodes). The repo's standing μ (`dsl.py`) is the Elias-gamma length prior, bits(p) = log2 a(|p|) + 2 log2|p| + 1,
  uniform within a length; with 16 atoms per atom node the two differ sharply (under 2^−nodes the n = 7 shell holds
  80.5/120.5 of the raw mass and each constant 0.4%; under the standing μ each constant holds 43%). I follow the
  explicit [after review] formula for L and run the standing μ as a labelled sensitivity arm **L_std** (chain at
  every N, lottery), so the reader can see whether the verdict depends on the choice.

Unnormalized mass by node shell under L (P): n = 1: 1; 4: 4; 5: 2; 6: 33; 7: 80.5 (total 120.5).

### 1.7 Named classes and hand derivations (P, entry 0, K = 10⁶)

Notation for x's atoms: S_a = (them, me, a), R_a = (me, them, a), Y_a = (them, them, a), X_a = (me, me, a),
Yc_a, Yd_a = (them, ⌜C⌝ / ⌜D⌝, a), Xc_a, Xd_a likewise. chk_a(t, m) is the clean check that t's run against ⌜m⌝
returns a (t's list validated; partner validation when t's script closes S).

**Lists (hand, from the tactic).** Cc := the spelling `C` (list [(C, EvR*; Ax)], no D script: it cooperates with ⌜D⌝);
Dc := `D` ([(D, EvR*; Ax)], no C script: it defects on every probe); CB, CB1, CBP: milestone 4's scripts; LöbC =
`if(R_C, C, D)`: C script EvR*; ChkR[EvR*; Ax · Hyp] closing R (valid against everyone without partner validation),
and a D script produced while its list was empty (RunNeg on R's box, which is false then), which fails at play time
because the box is true; CBdef = `if(S_C, D, C)`: no script at all (its T-branch reaches D with S on the left, where
no rule closes it; it cooperates with ⌜D⌝, so no D script).

**Plays (row's action against column):**

| | Cc | Dc | CB | CB1 | CBP | LöbC | CBdef |
|---|---|---|---|---|---|---|---|
| Cc | C | C | C | C | C | C | C |
| Dc | D | D | D | D | D | D | D |
| CB | C | D | C | C | C | C | D |
| CB1 | C | D | C | C | C | C | D |
| CBP | D | D | C | C | C | D | D |
| LöbC | C | C | C | C | C | C | C |
| CBdef | D | C | C | C | C | D | C |

(CB1 against Cc: S closed by Hyp, R closed by Hyp, partner validation of Cc's acyclic script succeeds. CBP refuses Cc
and LöbC: neither has a valid D script against ⌜D⌝. CBdef defects exactly on certified cooperators; readers' checks of
it fail, so it is suckered by CB, CB1, CBP and by D.)

**Establishers** (self-C and D against D): CB, CB1, CBP and their τ-variants (e.g. `if(and(S_C, R_C), C, D)` has
CB1's run tree). Cc, LöbC (C against D) and CBdef (C against D) are not establishers.

**Lemma G (S-guarded establishers are unexploitable).** Call x *S-guarded* if every root-to-C-leaf path of dt(x)
passes through the T-branch of an S_C atom (on a sound entry). If x plays C against y, some chk_C(y, x) = T, so by
Theorem S^cert y plays C against x. Hence U(y, x) ≤ 0, and for an S-guarded establisher (U(x, x) = 0) **no class
strictly invades**: every invader is neutral (cooperates with x and is cooperated with). CB, CB1, CBP are S-guarded.
This is RE 3(b), proved for the whole S-guarded subclass, not only for CB/CB1/CBP-shaped carriers.

**Exploited establishers (RE 3(c)).** An exploited establisher must be non-S-guarded: a C-leaf reached on a path with
no T S_C atom, and an exploiter y that defects while satisfying that path. Candidate family: `if(or(S_C, Y_C), C, D)`
("cooperate if them certifies cooperation with me, or them is a certified self-cooperator"; establisher: S_C is
Hyp^self in self-play, and D fails both). Its exploiter must be a certified self-cooperator that defects on it. My
hand analysis: a certified self-cooperator gets its C scripts from cooperating with a probe, and at two atoms every
atom it can ask about this establisher (S_a, R_a, Y_a, Yc_a, Yd_a) has the same value as about CB (both certify
cooperation through a Hyp(S) script, both are certified self-cooperators, both certifiably defect against ⌜C⌝ and
⌜D⌝, and both fail the D-question against a certified self-cooperator). So I expect **no exploited establisher at
n ≤ 7** (an own prediction, against RE 3(c)); the code enumerates all establisher–exploiter pairs.

**Shadows.** Classes on-path identical to C against an incumbent and entering it neutrally. In a CB population: Cc,
LöbC and every spelling that cooperates unconditionally with a certificate a CB-shaped reader accepts (e.g.
`if(S_C, C, C)`, whose script closes S by Hyp; `if(R_C, C, C)`; constant-C run trees in general). They are then
strictly invaded by Dc, CBdef and by prudent readers (CBP exploits Cc). **CBP admits no unconditional shadow**: it
defects on any class without a valid D script against ⌜D⌝, so its neutral entrants are other establishers (the CB
family), whose own shadows then complete the exit: CBP → CB (neutral) → Cc (neutral) → Dc (strict). *Frozen-tactic
coverage matters for shadows:* `if(Yd_D, C, C)` always plays C, but its produced script closes the F-branch by Run on
"them defects against ⌜D⌝", so it is certified only against opponents that do; Cc does not certify it.

**Suckers (CBdef type).** Cooperate where sound readers defect: CBdef cooperates with Dc and is defected on by every
establisher; it strictly invades Cc and LöbC populations (it defects on certified cooperators).

**LöbC type.** Certified CooperateBots by self-trust (Hyp^self): C against everyone, accepted by FB-shaped readers,
refused by CBP. Behaviourally I expect LöbC and Cc in one class.

**Entry into D.** In a Dc population every establisher is neutral at first order (D against Dc, Dc against it) with a
second-order advantage (0 > −1 among themselves): the modal arm's FairBot entry. Cc and CBdef are deleterious.

**Bridges under E (enumerated by code before any E cell; hand candidates).** Carriers on the two entries play (D, D)
(milestone 4 §1.7(e)). *Bor* = `if(or(CHK_0(them, me, C), CHK_5(them, me, C)), C, D)` (6 nodes; the nested-if
spelling `if(A0, C, if(A5, C, D))` has the same run tree): against CB0 the first atom is a pair-rule check on entry 0
(Hyp(S); partner validation succeeds, Bor's mode-0 script closes the same S); against CB5 the first atom is F
(CB5's script closes a box of entry 5, not the entry-0 root's R or S) and the second is a mode-5 pair-rule check whose
partner validation runs Bor's mode-5 script, which closes the entry-0 box by RunNeg (its clean value is F) and the
entry-5 box by Hyp. So **Bor cooperates with CB0 and with CB5, self-cooperates and defects on D, and is S-guarded
(Lemma G): a non-shadow bridge.** RE 5's premise ("every bridge is a shadow of one side") is therefore expected to
fail at n = 7, and with a neutral bridge cooperative π should flow between the entries in proportion to establisher
mass (π(x)/π(y) ≈ μ(x)/μ(y) along neutral edges), so the split need not be ≥ 0.9 on one entry. `if(and(A0, A5), C, D)`
is not a bridge (a carrier on one entry fails the other atom). Unconditional cooperators (Cc, LöbC on either entry)
bridge as shadows.

**Leak test** (as `k_at_n8.leak_test`): components of mutual cooperation among self-cooperating classes; a component
is closed iff no member cooperates with a class that defects on it.

### 1.8 Statistics, costs and cell classification

Payoffs: the modal arm's PD (D/D −1, D/C 1, C/D −2, C/C 0), w = 0.3, f = exp(w·payoff). Per class pair: steps of each
side's run; checks made and their inner steps; timeouts. Every cell where executable and ideal differ, and every
non-cooperative cell between establishers, is classified as **false certification** (a T check whose atom is false:
a soundness failure), **failed certification** (the needed check is F in both tables: no valid script), or
**timeout** (a check over V, or a play over K, in the executable table only). Soundness audit: every T check in both
tables against the actual play.

**K sensitivity (after review):** sources and lists rebuilt at K = 3·10⁵ and 3·10⁶ (V = K/4); recomputed: the
establishers' mutual plays and every exit edge of the top cooperative state at N = 10⁴ (mutant against resident).

### 1.9 Chain and lottery

**Chain.** `chain_log.LogChain` over the lumped classes (ClassProvider), w = 0.3, N ∈ {10³, 10⁴, 3·10⁴, 10⁵}; seeds:
every monomorphic state, every stable candidate without strict invader from `solver_audit.enumerate_candidates_fast`
(≤ 3 classes), and the saturated rest points of `solver_audit.invasion_closure`; `explore_log` at θ_log = 10⁻¹⁴ with
the 10⁻¹² / 10⁻¹⁶ sensitivity at N = 10⁴; twin-expanded and lumped distributions both reported. Arms: L×P (main),
U×P, L×O, L×P×E (and E-eq, L_std as labelled extras). Reported per cell: P(C,C), π(all-D), support (π ≥ 10⁻³) with
compositions, transition structure (top exits per supported state with mutants), the top cooperative state's exits
split into neutral (Δ1 = U(q, r) − U(r, r) = 0) and strict (Δ1 > 0), with ρ, N·ρ, Δ1, Δ2 = U(q, q) − U(r, q) and
N·Δ1 for the decisive edges (entry into all-D, the top state's exits), and the local slope of the cooperative/D odds
in N between consecutive N. A slope from four points spanning two decades is a local slope; where the decisive edges
are neutral (ρ ∝ 1/N) or carry a fixed Δ, their asymptotics are stated from Δ, not fitted. Cut diagnostic (as
`concessions_cutdiag.py`): the flow leaving the explored set under the solved π, by source and destination, for any
cell whose unexplored flow exceeds 2%.

**Lottery (ε = 0; `almost_all_seeds` conventions).** (N, I) = (100, 64), complete island graph, mN = 1, w = 0.3, iid
seeding: every slot of every island drawn from the arm's prior over spellings, mapped to classes; 40 runs per arm
(L×P, U×P, L×O, L×P×E), horizon 2,000 generations (I·N events each), checks every 10 generations.
*Endpoint exactly as the spec defines it:* an island is **resolved** when it is monomorphic in a class that no class
present anywhere in the run can invade under the actual migration process: no present class has a strictly higher
payoff against the island than the incumbent has against itself, and the incumbent does not drift to any present
class with higher payoff against the residents. *My precise reading of the drift clause (stated before any cell):*
let Z be the closure of {incumbent} under "a present class q joins if U(q, z) ≥ U(z, z) for some z ∈ Z" (strict or
neutral entry, iterated, so a drift into a shadow that is then invaded is caught); the island is resolved iff every
pair in Z × Z has the same cooperation outcome (all (C, C), a *cooperating* resolution; or none, a *non-cooperating*
one), so that nothing the run still contains can change the island's P(C,C). A run **succeeds** when every island is
resolved cooperating; **fails** when every island is resolved and some is non-cooperating, or when a non-cooperating
class is fixed globally; otherwise it is **right-censored** at the horizon, as are runs with any polymorphic island
there. Wilson intervals on the success fraction over the 40 runs (censored runs counted in the denominator as
not-success and reported separately). *A non-preregistered generalization* (reported beside, never in its place):
the same closure test applied to polymorphic islands (Z seeded with every resident), since neutral cooperating
mixtures cannot change P(C,C). For E: the fraction of runs ending with both entries' establishers alive; where
merges (one entry's last establisher lost) occur, the separation hazard from their times.

### 1.10 Validation plan (before any counted cell)

1. Grammar counts reproduce §1.1 (P, O, E at n = 5, 6, 7).
2. Production reproduces milestone 4's lists for CB, CB1, CBP, LöbC, Cc.
3. The play table reproduces milestone 4's K = 10⁶ cells among CB, CB1, CBP, LöbC, Ccert, CBdef where the programs
   coincide, and the §1.7 table above (with Dc and CBdef under their own production).
4. Composition = whole actual play on every named pair and on every n ≤ 5 spelling pair; ideal = executable there.
5. Lemma T on a random sample of n = 7 spelling pairs (direct execution vs the τ table), including same-τ pairs.
6. The empty-list shortcut against the term on a sample.
7. Lemma G: no strict invader of any S-guarded establisher (exhaustive).
8. Bor against CB0, CB5, itself and D on the E catalogue.
9. Twin-expanded lumped chain = unlumped chain on n ≤ 5.

### 1.10 Code validation of §1 (after the code, before any counted cell)

From `tests/test_carrier_populations.py` (8 tests, all passing) and `carrier_populations_run.py validate`
(`runs/carrier_populations/validate.json`), run on the static tables before any chain or lottery cell.

- **Counts** reproduce §1.1 (P 130 / 2,242 / 12,546; E at n ≤ 6 8,578; the recurrences with k = 16 and 32).
- **Production** reproduces milestone 4's lists for CB, CB1, CBP, LöbC and Ccert, and the catalogue's CB spelling is
  milestone 4's CB term exactly.
- **The §1.7 hand table** (Cc, Dc, CB, CB1, CBP, LöbC, CBdef) is reproduced cell for cell by whole actual plays.
- **Composition and Lemma T:** on the n ≤ 5 sub-catalogue every one of the 16,900 spelling pairs, played whole by the
  term, equals the τ-composed table, and the ideal and executable τ tables are identical. Lemma T by direct plays
  (no table) on 40 random same-τ quadruples at n ≤ 6. At n = 7: 2,750 random spelling pairs (including 500 same-τ
  cross-twin pairs and 250 self-plays) played whole against the τ table, 0 mismatches; 1,600 class-table cells played
  whole, 0 mismatches; the empty-selection shortcut against the term on 201 checks, 0 mismatches.
- **A bug found here and fixed before any cell: milestone 4's host replay memo is order-dependent.** `HostCheck`
  memoizes clean check values and returns them when the same check recurs nested inside another; but a nested check
  whose clean run called (transitively) a key that is now on the stack, or whose clean value is TO, does not return
  its clean value in context: it regresses and kills the root (Lemma N). Found as two cells of the n ≤ 5 τ table where
  the ideal table said C and the term said D (`if(CHK(them,me,D),C,D)` against CB-shaped opponents: the shared memo
  held a TO from an earlier top-level check and let RunNeg close on it). `ExactHost` records the keys each memoized
  check called and raises the regress in those cases; the ideal table and production use it. Production through
  `Producer` used the same memo, so production became order-dependent across a catalogue; with `ExactHost` every
  host value in production is the clean term value. The named lists (CB, CB1, CBP, LöbC, Ccert) are unchanged.
  Milestone 4's audit compared host and term per check with its own instance order, so its published cells are not
  affected as far as I can see, but its host-agreement claim was order-dependent.
- **Lemma G exhaustively at n = 7:** 101 establisher classes, 14 of them S-guarded; no S-guarded establisher has a
  strict invader.
- **Exploited establishers: my §1.7 expectation was wrong.** 75 of the 101 establisher classes are strictly
  exploited (9,044 exploiter pairs). The exploitable ones are not `or(S_C, Y_C)` templates but *defection
  detectors*: e.g. `if(CHK(them, ⌜C⌝, D), D, C)` ("defect iff them is certified to defect against plain C") cooperates
  with itself, defects on D (D carries a certified D script), and is exploited by every defector that carries no
  certificate for the question, e.g. `if(CHK(me, ⌜D⌝, D), D, C)`. RE 3(c) holds; my S4 is falsified (recorded in the
  run report, not changed here).
- **The n ≤ 5 chain check** (§1.5): the unlumped chain over 130 spellings, the lumped chain over 31 classes and the
  lumped chain with twin drift give P(C,C) 0.328200897 / 0.328200897 / 0.328200898 at N = 10³ and 0.599591006 (all
  three, to 3·10⁻¹⁰) at N = 10⁴. (π of the single spelling `D` in the unlumped chain is a different object from π of
  the D class and is not compared.)
- **Bor** (E production): (C, C) with CB on entry 0, with CB on entry 5 and with itself; (D, D) against D; CB0 against
  CB5 (D, D). The hand derivation holds.

## 2. Implementation and costs

`src/carrier_populations.py` (grammar, run trees, production, catalogue, `ExactHost`/`IdealCheck`, the checker
wrapper for both tables, composition, lumping); `src/carrier_populations_run.py` (static tables with ≤ 3 worker
processes, validation, chain, lottery); `src/carrier_populations_report.py` (tables). Raw arrays in
`runs/carrier_populations/*.npz` (not committed).

**Scale guard (P, n = 7, K = 10⁶, 2 workers while the foreign chains were alive):** 12,546 spellings, 4,162 τ-types
(the scratch count of run trees; lists are a function of the run tree here, so τ-types = run trees), catalogue and
production 4 s; the ideal τ table needs 3,828,352 pair checks (targets without an entry for the asked outcome are F
without running), 194 s; lumping gives **588 classes** (18 split τ-types, i.e. types whose spellings play their twins
differently from themselves, giving 54 singleton classes); the executable class table needs 122,744 term checks,
247 s. Total 447 s, far under the 2-hour guard, so the cutoff stays at n = 7. **Executable = ideal on every class
cell.** Executable check costs (inner steps): median 21,962; 99th percentile below V 67,683; the largest check that
did not time out 101,644 (V = 250,000); 13,982 checks end at exactly V: every one a regress (the evaluator
fast-forwards a regress to the root's deadline), and the ideal table, which has no step limit, gives TO for the same
checks.

### 2.1 Additions during the run (each before the cells that use it)

- **Exact lumping with hashed keys** (E): the lumping keys rows and columns by hash and then verifies every group
  exactly against its first member (the first E attempt's byte keys ran out of memory; the result is identical).
- **E's class table is the ideal table.** The full executable E table needed 4.07 M term checks (≈ 3 h at 3
  workers); it was computed on 291 classes (the 150 heaviest and 150 random; 24,702 term checks), identical to the
  ideal table there, as in P (588 classes) and O (701 classes) where it was computed in full.
- **`FastChain`** (`carrier_populations_run.fast_chain_class`): `LogChain` with closed-form two-type fates in
  monomorphic states (q fixes unless c > a and b > d, where the stable mixture is the target; a first-order-dying q
  gets the chain's own drift/valley target mono(q)); polymorphic states unchanged. On the P cells at N = 10³ and 10⁴
  it reproduces `LogChain` exactly (π(all-D), entry rates, exits, support to all printed digits). Used for E and the
  no-clique control.
- **The no-clique control** (not preregistered): the ten closed leak components removed (iterated until none is
  closed: one pass), θ = 10⁻⁸, ≤ 4,000 explored states; cut diagnostic recorded per cell.
- **Process note:** killing a driver with `pkill -f` left its pool workers running as orphans; four such workers ran
  for up to four hours beside the permitted three before I found and killed them (by pid).
