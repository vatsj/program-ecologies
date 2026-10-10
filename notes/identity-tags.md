# Identity and tags in the carrier grammar: the pooling test (notes, 2026-10-10)

Spec `specs/2026-10-10-identity-and-tags.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-10-identity-and-tags-gpt-6.1-sol.md`;
the [after review] text is the resolution). §1 is written before any project code of this experiment and before any
counted cell: the grammar extension and its counting, compilation of the new atoms and of markers, production, the
τ-types with the marker reduction, identity-aware lumping, the named classes with hand-derived reciprocal plays, the
families and bridges by hand, the priors and tilts, the pooling argument as a calculation, the lottery endpoint,
censoring and hazards, the chain diagnostic and the validation plan. §1.13 (code validation) is appended after the code
exists and before any counted cell; §2 (costs) after that. Base: `notes/carrier-populations.md` §1 ("milestone 2") and
`notes/certificates-as-code.md` §1 ("milestone 4"); their calculus K_T^cert, checker term, frozen tactic, `ExactHost`
and `IdealCheck` are imported unchanged (`src/lt_cert.py`, `src/carrier_populations.py`, not modified).

*Disclosure.* Before writing this section I ran a scratch enumeration of the extended grammar (counts of bodies, run
trees, run trees with tag or `eq` atoms, and how many distinct marker-reduced check keys the table needs; nothing about
plays), because those numbers decide whether the table is computable at n = 7 (§1.4). They are quoted below.

## 1. Design

### 1.0 Scope

Milestone 2's finite template ecology inside a Turing-complete evaluator, extended by three source-reading devices
that L_T already has or can express: structural quote equality (`eq`), syntactic tags (markers read by quote
inspection), and a literal quote of a named program (⌜CB⌝). Certificates still come from the frozen host tactic,
uncharged. The experiment tests the pooling argument for the seed lottery (DEFERRED 1, RS 2026-10-10): whether iid
seeds reward a family that cooperates across spellings over an exact-identity clique made as cheap as FairBot, and what
pooled parochial clubs (tag clubs, exclusive clubs) do to universality. It is not a test of unrestricted program
evolution, and every lottery number is finite-(N, I, horizon) evidence.

### 1.1 The grammar

Milestone 2's two sorts, unchanged: actions A ::= `C` | `D` | `if(B, A, A)`; conditions B ::= atom | `not(B)` |
`and(B, B)` | `or(B, B)`; one node per constant, atom and connective. **Atoms (k = 23):**
- the check atoms `CHK(p, q, a)`, p ∈ {them, me}, **q ∈ {me, them, ⌜C⌝, ⌜D⌝, ⌜CB⌝}**, a ∈ {C, D} (20; sound checker
  CHK_S, entry 0 only; ⌜C⌝, ⌜D⌝ are milestone 4's plain `PROG_C`, `PROG_D`; ⌜CB⌝ is §1.2);
- the **identity atom** `eq(me, them)` (1);
- the **tag atoms** `tag_1(them)`, `tag_2(them)` (2): true iff the opponent's source carries marker t.

**Markers.** A program is a body x (an action) and a **marker set** M ⊆ {1, 2}: 0, 1 or 2 markers, distinct (a source
carrying the same marker twice is indistinguishable from carrying it once by every tag atom, and is excluded as a
redundant spelling). A marker is a no-op subterm of the source (§1.2) and **costs one node, counted in the cutoff**:
nodes(x, M) = nodes(x) + |M| ≤ 7. Markers are part of the source, so they enter quotes, `eq`, check boxes and
certificates exactly as any other part of the code does.

**Counts by hand** (milestone 2's recurrences with k = 23): b(1..5) = 23, 23, 1,081, 3,197, 103,707 conditions;
a(1..7) = 2, 0, 0, 92, 92, 4,324, 21,252 bodies; 25,762 bodies at n ≤ 7, of which 4,510 at n ≤ 6 (two marked
versions each) and 186 at n ≤ 5 (one doubly marked version each): **34,968 spellings**. At n ≤ 7 a body still has at
most two atoms, so a run makes at most two check calls. Scratch counts (§ disclosure): 8,558 distinct run trees (dt)
at n ≤ 7, 1,416 of them with a tag atom and 724 with `eq`; **17,304 τ-units** (dt, M) (§1.4), 17,305 with CB singled
out.

**Named classes** (S = `CHK(them, me, C)`, Ycb = `CHK(them, ⌜CB⌝, D)`; a superscript is the marker set):

| name | spelling | nodes |
|---|---|---|
| Cc, D | `C`, `D` | 1 |
| D¹ (marked D) | `D` with marker 1 | 2 |
| CB | `if(S, C, D)` (milestone 4's CB, unmarked) | 4 |
| MC¹ (the marked carrier) | CB with marker 1 | 5 |
| EQ (the eq-clique) | `if(eq(me,them), C, D)` | 4 |
| EQ′ (a respelling) | `if(not(eq(me,them)), D, C)` (the same run tree) | 5 |
| TC1, TC1¹ (tag club 1, unmarked / marked) | `if(tag_1(them), C, D)`, with no marker / marker 1 | 4 / 5 |
| AF¹ (the and-form) | `if(and(tag_1(them), S), C, D)` with marker 1 | 7 |
| OF¹ (the or-form) | `if(or(tag_1(them), S), C, D)` with marker 1 | 7 |
| TwinD | `if(or(CHK(me,me,D), CHK(me,them,D)), D, C)` | 6 |
| XC (the exclusive club) | `if(and(S, Ycb), C, D)` | 6 |
| XC′ (its order twin) | `if(and(Ycb, S), C, D)` | 6 |

The spec puts XC at 7 nodes; it has 6 (if, and, two atoms, two leaves), so XC¹ (7) is also in the catalogue. The
**prudent exclusive club** `if(and(S, and(CHK(them,⌜C⌝,D), Ycb)), C, D)` has three atoms and 8 nodes: **not in the
catalogue at n = 7** (noted, as the spec asks).

### 1.2 Compilation

A spelling (x, M) compiles to milestone 4's carrier `λme. λthem. (λcerts. BODY_M) CERTS` with
- **markers as no-op lets around the body:** BODY_∅ = body(x); BODY_{t} = `(λ_. body(x)↑) ⟨t⟩`; BODY_{1,2} =
  `(λ_. (λ_. body(x)↑↑) ⟨2⟩) ⟨1⟩` (marker 1 always outermost), where ⟨t⟩ = the natural 9000 + t (a value) and ↑ shifts
  the body's free variables (certs, them, me) by one. Each marker costs one β step of the program's own run and nothing
  else; `getcerts` (λ, λ, app of a λ) is unchanged, so the list is found as before.
- `eq(me, them)` = the L_T primitive `eq` on the two quote variables: one evaluator step, structural (canonical
  encoding) equality, so **true exactly in self-play** (two distinct spellings are distinct terms).
- `tag_t(them)` = a guarded walk of the opponent's quote with L_T's `fst`/`snd` on quotes: check the tags λ, λ, app,
  λ along the carrier shape (any other shape gives F, so `PROG_C`, `PROG_D` and non-carriers read as unmarked), take
  the body B, and return T iff B is an application whose argument is ⟨t⟩, or (for t = 2) B's argument is ⟨1⟩ and the
  inner body is an application with argument ⟨2⟩. About 15–30 deterministic steps; no check call.
- ⌜CB⌝ = the literal quote of the catalogue's unmarked CB term with its produced list (milestone 4's CB at K = 10⁶,
  V = K/4). So **CB is ⌜CB⌝**: a program reading `CHK(them, ⌜CB⌝, a)` against CB asks about CB's self-play.
- Check atoms, `not/and/or`: milestone 2's compilation, with the role variables offset by |M|.

### 1.3 Production (extended probe list; a design elaboration the spec's hand claims require)

Milestone 4's frozen tactic and two-pass procedure (`lt_cert.produce_list`, unchanged): D script against ⌜D⌝ with an
empty list, then C scripts against the probes in order, distinct scripts only, list = C scripts then the D script. The
probe list is **extended**: **CB, CB1, CBP** (milestone 4's), then **CB¹, CB², CB¹²** (CB with markers), then **XC**.
*Why:* the tactic finds a C script only against an opponent the program cooperates with. A tag club cooperates with
no unmarked probe, so under milestone 2's probes it carries no C script and the marked carrier would read it as a
defector; an exclusive club cooperates with no CB-family probe (no probe certifiably defects against CB), so it would
carry no C script and could not even cooperate with itself through S. The spec's hand claims ("it cooperates with the
tag club through the club's valid 'I cooperate with tagged you' script"; the exclusive club as a self-cooperating
family) need a probe from each new family, in the role CB/CB1/CBP play for the open family. Probes carry their own
produced lists (two passes as in milestone 4; XC's C script is produced against XC with its D-only list). *Rejected
alternative:* a self-probe (every program produces a script against itself). It also realizes the clubs, but it
changes milestone 2's programs that read their own certificates (e.g. `if(CHK(me,me,C), C, D)` becomes a Löbian
unconditional cooperator), so it is a different ecology; it is recorded in REJECTED, not run. *Consequence to report:*
the number of milestone-2-shaped spellings (no new atom, no marker) whose list differs from milestone 2's production
(expected 0 or a handful: scripts are opponent-generic, and the new probes add a script only to programs that cooperate
with a new probe on a new path). Families without a probe of their own get no certificates; this asymmetry is part of
the design and is stated with every club result.

**Lists depend on (dt, M ∩ tags(dt)) only.** A program's runs against the probes read the probes' markers (tag atoms)
and the probes' identity (`eq` false); its own markers matter only where its run reads its own quote's tags, i.e.
through M ∩ tags(dt). So production is done once per (dt, M ∩ tags(dt)) and copied (checked on a sample, §1.12).

### 1.4 τ-units, Lemma T′ and the marker reduction

**τ(x, M) = (dt(x), list, M, [x = CB])**: milestone 2's τ plus the marker set and the CB flag (the single spelling CB
is the named quote, so the bijection argument below must fix it). Since the list is a function of (dt, M ∩ tags),
τ-units are (dt, M, cb): **17,305**.

**Lemma T′ (τ-symmetry with identity and tags).** Milestone 2's Lemma T holds for τ′: if two spellings have the same τ′,
renaming one to the other throughout (and back) is a bijection on quotes that fixes ⌜C⌝, ⌜D⌝, ⌜CB⌝; it preserves every
check value (milestone 2's four cases), every `eq` value (equality is preserved by a bijection) and every tag value
(equal marker sets). So plays are determined by a τ-level table G(τ1, τ2) (two *distinct* spellings, including τ1 = τ2:
the twin play) and Self(τ).

**Lemma R (marker reduction).** For distinct spellings t ≠ m, the clean check value chk_a(t, m) depends on the marker
sets only through M_t ∩ G and M_m ∩ G, G = tags(dt_t) ∪ tags(dt_m). *Proof sketch:* the check touches runs among
{t, m, ⌜C⌝, ⌜D⌝, ⌜CB⌝} (roots, partner validation, nested Run/RunNeg boxes); the constants carry no tag atom and no
marker; a tag atom of t or m reads the marker set of whichever of these quotes is its opponent, and only tags in G are
ever read; replacing t and m by t′, m′ with the same dt, list and CB flag and the same markers inside G is a bijection
on the quotes in play (t′ ≠ m′ because t ≠ m and the reduction keeps them distinct or uses a distinct instance, below)
that preserves every value read. ∎ So the pair table is computed on **reduced keys** (dt_t, M_t ∩ G, cb_t, dt_m,
M_m ∩ G, cb_m) with one representative pair of distinct spellings per key (when both sides reduce to the same τ-unit
the instance is two distinct spellings of it: its first two spellings, or the original pair when it has one). Scratch
count: **1.57·10⁷ reduced keys per outcome a** (against 4.8·10⁷ τ-unit pairs asked), before removing targets that carry
no a-entry (F without running, as in milestone 2). Unit values (self, against ⌜C⌝, ⌜D⌝, ⌜CB⌝) are computed per
(dt, M ∩ tags(dt), cb). Lemma R is tested by whole plays on random marked pairs (§1.12).

**Composition** (milestone 2's, extended): x's action against a distinct y evaluates dt(x) with S-type atoms
`CHK(them, me, a)` = chk_a(y, x), R-type `CHK(me, them, a)` = chk_a(x, y), `CHK(them, them, a)` = y's self value,
`CHK(me, me, a)` = x's, `CHK(·, ⌜q⌝, a)` the unit values, **`eq` = F**, **`tag_t(them)` = [t ∈ M_y]**. Self-play: `eq` =
T, tags read M_x, S and R atoms read x's self value. Twin play (distinct spellings of one τ-unit): `eq` = F, tags read
the common M, S and R atoms read the twin instance. At most two check calls, so the global counter cannot bind (milestone
2 §1.4).

### 1.5 Identity-aware lumping

Two spellings merge iff their payoff rows and columns against **every spelling of the catalogue** agree, including the
self and cross-twin cells (milestone 2 §1.5): U(x, z) = U(x′, z), U(z, x) = U(z, x′) for z ∉ {x, x′}, and U(x, x) =
U(x, x′) = U(x′, x) = U(x′, x′). The catalogue contains identity-sensitive (`eq`, TwinD-type), tag-sensitive and
⌜CB⌝-sensitive opponents, so the criterion already is the identity-aware one sol asks for: it is applied to the
τ′-expanded matrix. Consequences, by hand:
- **a τ-unit whose twin play differs from its self play splits into singleton classes**; every `eq`-clique run tree
  (C only under `eq` = T) is such a unit, so **every spelling of the eq-clique is its own class** (EQ and EQ′ share a
  run tree and still do not merge: EQ against EQ′ is (D, D), EQ against itself (C, C));
- marked and unmarked spellings are different τ-units; every marker is read by some `tag_t` program of the catalogue
  (TC1, TC2 play C against a marked source and D against an unmarked one), so **a marked spelling never merges with its
  unmarked version**; whether two units merge is decided by the table, never assumed;
- two singleton-type identity cliques of different run trees never merge (each has its C in its own diagonal cell).
The lottery and the chain run on these classes, so identities are exact where they matter.

### 1.6 Named classes: hand-derived lists and reciprocal plays (K = 10⁶, V = K/4)

Scripts (milestone 4's notation): σCB = `EvR*; ChkR[EvR*; Ax · Hyp]`; δ = `EvR*; ChkR[RunNeg · EvR*; Ax]` (the
carriers' D script); ε = `EvR*; Ax` (acyclic: the run reaches the asked constant); σXC = `EvR*; ChkR[EvR*; ChkR[EvR*;
Ax · Run] · Hyp]` (CBP's skeleton); σXC′ = `EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Hyp] · Run]`.

**Lists (hand, from the tactic with the probes of §1.3).**
- CB, MC¹: [(C, σCB), (D, δ)] (the marker β step is absorbed by EvR*; every probe gives σCB; milestone 4's list).
- TC1, TC1¹: [(C, ε), (D, ε)]: against CB¹/CB¹² the run reads tag 1, reaches C; against ⌜D⌝ the guarded walk fails
  (λλD is not a carrier), so tag 1 is F and the run reaches D.
- AF¹: [(C, σCB), (D, ε)] (against CB¹: tag T, then S at a call closed by Hyp; against ⌜D⌝: tag F, reaches D).
- OF¹: [(C, σCB), (C, ε), (D, δ)] (against CB: tag F, S closed by Hyp; against CB¹: tag T, reaches C; against ⌜D⌝:
  tag F, S's box ⊡(D, OF, C) is false, RunNeg).
- Cc: [(C, ε)]; D, D¹: [(D, ε)]; EQ, EQ′: [(D, ε)] (they defect on every probe; no C script); TwinD: [(D, τD)] with
  milestone 2's τD = `EvR*; ChkR[RunNeg · EvR*; ChkR[EvR*; Ax · Hyp]]`, no C script.
- XC: [(C, σXC), (D, δ)]. Against the probe XC (D-only list in the first pass): S's box ⊡(XC₀, XC, C) is the root's S
  (Hyp); on its T branch Ycb's box ⊡(XC₀, ⌜CB⌝, D) is Run, true because XC₀'s δ against CB closes ⊡(CB, XC₀, C) by
  RunNeg (CB's partner validation of XC₀ finds no C script). Against CB, CB1, CBP and the marked CBs XC defects (they
  cooperate with CB), so σXC is its only C script. XC′: [(C, σXC′), (D, δ)].

**Key checks (hand).**
- chk_C(CB, XC) = **F**: CB's σCB closes ⊡(XC, CB, C) by Hyp^pair; partner validation runs σXC on XC's run against CB,
  whose T branch needs Run on ⊡(CB, ⌜CB⌝, D) = CB's self-play D-check, which is F. Hence **chk_D(XC, CB) = T** (δ: the
  box ⊡(CB, XC, C) is false, RunNeg).
- chk_C(XC, XC) = **T** (twin root R = S = ⊡(XC, XC, C): Hyp^self; then Run on ⊡(XC, ⌜CB⌝, D) = T). chk_C(XC′, XC) = T
  (σXC′: Run on ⊡(XC, ⌜CB⌝, D), Hyp^pair on S; XC's partner validation: Hyp on R, Run on ⊡(XC′, ⌜CB⌝, D), true by δ
  since ⊡(CB, CB, D) is false).
- chk_C(MC¹, CB) = T: MC¹'s σCB, its call's box ⊡(CB, MC¹, C) is S (markers are part of both quotes, consistently),
  Hyp^pair; CB's σCB on CB against MC¹ closes R. Markers never break the pair rule.
- chk_C(TC1¹, MC¹) = T (ε on TC1¹'s run against the marked MC¹ reaches C); chk_C(TC1¹, CB) = F (reaches D).
- chk_C(OF¹, MC¹) = T through its second script ε (the first, σCB, meets the value C where it expects a call).

**Reciprocal plays (row's action against column; marker sets as in the table above):**

| row \ col | Cc | D | D¹ | CB | MC¹ | TC1 | TC1¹ | AF¹ | OF¹ | EQ | EQ′ | TwinD | XC | XC′ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Cc | C | C | C | C | C | C | C | C | C | C | C | C | C | C |
| D | D | D | D | D | D | D | D | D | D | D | D | D | D | D |
| D¹ | D | D | D | D | D | D | D | D | D | D | D | D | D | D |
| CB | C | D | D | C | C | D | D | D | C | D | D | D | D | D |
| MC¹ | C | D | D | C | C | C | C | C | C | D | D | D | D | D |
| TC1 | D | D | C | D | C | D | C | C | C | D | D | D | D | D |
| TC1¹ | D | D | C | D | C | D | C | C | C | D | D | D | D | D |
| AF¹ | D | D | D | D | C | D | C | C | C | D | D | D | D | D |
| OF¹ | C | D | C | C | C | C | C | C | C | D | D | D | D | D |
| EQ | D | D | D | D | D | D | D | D | D | C | D | D | D | D |
| EQ′ | D | D | D | D | D | D | D | D | D | D | C | D | D | D |
| TwinD | D | D | D | D | D | D | D | D | D | D | D | C | D | D |
| XC | D | D | D | D | D | D | D | D | D | D | D | D | C | C |
| XC′ | D | D | D | D | D | D | D | D | D | D | D | D | C | C |

Derivations of the less obvious cells: CB against OF¹: OF¹'s σCB on OF¹'s run against CB (tag F, call ⊡(CB, OF¹, C) =
S, Hyp^pair, partner validation σCB on CB against OF¹ closes R): C, and OF¹ cooperates back by S. MC¹ against TC1
(unmarked): TC1's ε on its run against MC¹ (marked) reaches C. OF¹ against TC1 (unmarked): C by S (TC1's ε against
the marked OF¹ reaches C). XC against Cc: S is T (ε) but chk_D(Cc, ⌜CB⌝) is F (Cc carries no D script): D; so XC
exploits Cc. XC against OF¹: OF¹'s σCB at S needs partner validation by σXC, whose T branch needs Run on ⊡(OF¹, ⌜CB⌝,
D), false: D. TwinD against everything but itself: D (its D script closes ⊡(X, X, D) by RunNeg and ⊡(X, Y, D) = R by
Hyp^self, milestone 2). EQ and EQ′ cooperate only in self-play (`eq` is T only there); against each other (D, D).

**Properties read off the table.**
- *Self-cooperators:* Cc, CB, MC¹, TC1¹, AF¹, OF¹, EQ, EQ′, TwinD, XC, XC′. TC1 (unmarked) defects on itself.
  *Establishers* (self-C, D against D): all of them except Cc.
- *Exploitation:* **TC1¹ and OF¹ are exploited by D¹** (they cooperate with every source carrying marker 1); AF¹ is not
  (it also needs S). CB, MC¹, AF¹, XC, XC′ are S-guarded (every path to C passes a true S), so by Lemma G (milestone 2)
  no class strictly invades them. EQ, EQ′, TwinD are strictly invaded by nobody (they defect on every other source).
- *Suckers:* Cc (by D, EQ, TwinD, XC, …), TC1 (by D¹).

### 1.7 Families, bridges and rivals (definitions; the named sub-catalogue by hand)

- **Compatibility graph:** vertices the establisher classes (self-C, D against the unmarked D, the D-entering
  self-cooperators that carry the lottery, RESULTS "cutoff sensitivity in n"); edge iff mutual cooperation.
  (Non-establisher self-cooperators, e.g. Cc-type shadows, are reported but are not family members: they cannot
  nucleate against D.)
- **Pairwise-compatible sets** = maximal cliques of that graph (sol's fix: mutual cooperation is not transitive, so
  components would merge the rivals). Each is reported with its pooled seed mass (sum of its classes' masses) and
  spelling count. An **exact-identity clique** is a maximal clique of one class consisting of a single spelling.
  **Bridge-mediated connectivity** = the components of the graph, reported separately.
- **Rivals:** two pairwise-compatible sets with some cross pair of members that mutually defect.
- **Bridge** between two rival sets P, Q: a class that mutually cooperates with every member of P ∪ Q. For maximal
  cliques this is exactly P ∩ Q (a class outside both that cooperated with all of P would extend P). A **pairwise
  bridge** of two named establishers (e.g. CB and TC1¹) is a class mutually cooperating with both. A bridge is
  **exploitable** if some class of the catalogue strictly invades it (U(q, b) > U(b, b)).
- **The open carrier family** F_CB := the maximal clique containing CB with the largest pooled L-mass; **M** := its
  pooled L-mass. CB's neighbourhood N(CB) (establishers mutually cooperating with CB) is reported beside it.
- **Leak test:** milestone 2's (components of mutual cooperation among self-cooperators; closed iff no member cooperates
  with a class that defects on it).

**By hand on the named sub-catalogue** (establishers CB, MC¹, TC1¹, AF¹, OF¹, EQ, EQ′, TwinD, XC, XC′): edges CB–MC¹,
CB–OF¹, MC¹–TC1¹, MC¹–AF¹, MC¹–OF¹, TC1¹–AF¹, TC1¹–OF¹, AF¹–OF¹, XC–XC′. Maximal cliques: **{CB, MC¹, OF¹}**,
**{MC¹, TC1¹, AF¹, OF¹}**, **{XC, XC′}**, {EQ}, {EQ′}, {TwinD}. Rivals: the first two (CB–TC1¹, CB–AF¹ mutually defect),
and every pair involving XC's set or a singleton clique. **Bridges:** between the open set and the tag-1 club, P ∩ Q =
{MC¹, OF¹}: **MC¹ is the non-exploitable bridge** (S-guarded), **OF¹ is a bridge exploitable by D¹**, and **AF¹ is not a
bridge** (it defects on the unmarked CB). Between XC's set and the open set there is **no bridge, by soundness**: a
bridge b would need chk_C(b, CB) = T (CB cooperates with b), so b cooperates with CB (Theorem S^cert), and chk_D(b, ⌜CB⌝)
= T (XC cooperates with b), so b defects against CB: contradiction. This holds for every program in the catalogue, not
only the named ones (bridge-less by construction). The singleton cliques have no bridge either (nobody else is
cooperated with by EQ, EQ′, TwinD). Components: {CB, MC¹, OF¹, TC1¹, AF¹} (joined through the bridges), {XC, XC′},
and the three singletons.

*Expected shadows of XC (hand, checked by code):* `if(Ycb, C, D)` ("cooperate iff you certifiably defect against CB")
mutually cooperates with XC and cooperates with D (D's ε certifies defection against everything), so it is a neutral
entrant into XC that D then exploits: XC's islands are not closed.

### 1.8 Priors, tilts and ablations (complete)

- **L (main):** weight 2^−(nodes(x) + |M|) per spelling, normalized over the catalogue. Normalizer (by hand):
  Z = Σ_n a(n) 2^−n (1 + 2·½·[n ≤ 6] + ¼·[n ≤ 5]) = 2.25 + 12.9375 + 6.46875 + 135.125 + 166.03125 = **322.8125**.
  Normalized spelling weights: `C`, `D` 1.549·10⁻³ each (D¹, D² 7.74·10⁻⁴, D¹² 3.87·10⁻⁴); **CB 1.936·10⁻⁴, EQ
  1.936·10⁻⁴** (both 4 nodes: ratio 1); MC¹, TC1¹, EQ′ 9.68·10⁻⁵; TwinD, XC, XC′ 4.84·10⁻⁵; AF¹, OF¹, XC¹ 2.42·10⁻⁵.
  Shell masses (raw): 1 node 2.25, 4: 12.94, 5: 6.47, 6: 135.1, 7: 166.0 (shells by body size, markers included in
  each). A class's mass is the sum over its spellings.
- **U (control):** every lumped class equal weight.
- **Tilts** (seed-composition interventions; each fixes a block of mass M on named spellings and renormalizes the rest
  of L to 1 − M; paired seeds: the same random streams per replicate across tilts):
  - **T1a:** M on the single spelling EQ.
  - **T1b:** M/10 on each of the ten heaviest spellings of the eq-clique run tree `eq ? C : D` (EQ with its four marker
    sets, EQ′ with three, the double negation with three; eleven exist, ties broken by enumeration order); every pair of
    them is (D, D).
  - **T1c:** M/10 on each of the ten heaviest spellings of CB's run tree `S ? C : D` (CB with four marker sets, its
    negated respelling with three, the double negation with three; mutually compatible), **and the open carrier family
    otherwise removed**: every establisher class in N(CB) ∪ {CB} loses all its other spellings' mass.
  - **T2:** M on TC1¹ (the self-cooperating tag club).
  - **T3:** M on XC.
  T1a against T1c is "one identity against a compatible family at equal mass"; T1b against T1c is the pooling
  comparison proper (sol: the first T1 let one identity pool within the intervention).
- **Ablations** (L restricted to a sub-catalogue and renormalized; paired seeds): *identity-only* (no tag atom, no
  marker, no ⌜CB⌝ atom; `eq` kept), *tags-only* (no `eq`, no ⌜CB⌝; tags and markers kept), *named-⌜CB⌝-only* (no `eq`,
  no tag, no marker). Classes are the full catalogue's (finer than a sub-catalogue's own lumping, still exact); a class's
  ablation mass is the sum over its spellings inside the sub-catalogue.

### 1.9 The pooling argument as a calculation

Let a set P have seed mass μ_P. On an island of N slots the seeded count of P is K_P ~ Binomial(N, μ_P) ≈ Poisson(N μ_P),
independently across islands, so the expected seeded count is **N μ_P per island and I N μ_P per run**. A pairwise-
compatible set counts all its spellings together (its founders are mutual cooperators, so they reinforce each other in
the D sea and their islands unite under migration); an exact-identity clique counts one spelling, and two clique
spellings are rivals of each other.

Write q(k) for the chance that k co-seeded founders of one set establish an island in the scramble. Stage 1 (islands
nucleated by P) has mean I·E q(K_P). If q were linear, q(k) = q₁k, splitting mass would not matter at stage 1:
Σ_j I q₁ N μ_j = I q₁ N μ. Pooling enters (i) through the super-linear part of q (near-critical founders help each
other: q(2) > 2q(1), milestone 2's demographic formula), and (ii) at stage 2, where established networks compete by
migration and **the larger network wins a two-network merge with probability ≈ 0.94** (RESULTS "Rival networks across
islands", merge test): a family's islands all belong to one network, while each clique spelling is its own network and
competes with the family and with the other spellings separately.

Hand numbers (N = 100, I = 64; M is computed by code, guessed 0.01–0.03, written m below):

| prior | set | per-island seeded count | per run |
|---|---|---|---|
| L | CB's spelling / EQ's spelling | 0.019 / 0.019 | 1.24 / 1.24 |
| L | MC¹, TC1¹ | 0.0097 | 0.62 |
| L | XC | 0.0048 | 0.31 |
| L | D¹ + D¹² (marked-1 defectors) | 0.116 | 7.4 |
| L | F_CB | 100 m (1–3) | 64–190 |
| T1a | EQ | 100 m | 64–190 |
| T1b | each of ten EQ spellings | 10 m (0.1–0.3) | 6.4–19 |
| T1c | the ten CB spellings together | 100 m | 64–190 |
| T2 | TC1¹ / MC¹ / D¹ + D¹² | 100 m / 0.0097 (1 − m) / 0.116 (1 − m) | – / 0.6 / 7.4 |
| T3 | XC | 100 m | 64–190 |

So under L the clique's stage-1 count is about 1/(50–150) of the family's; under T1a they are equal; under T1b each
clique spelling has a tenth of the family's count and the ten fight each other; under T2 the marked carrier, the only
non-exploitable bridge, is seeded on about 0.6 islands per run (so it is often absent when the rivalry forms), while
marked defectors are seeded on about 7.

### 1.10 Lottery (primary)

Kernel: milestone 2's ε = 0 island process (`src/islands.py` conventions as implemented in
`carrier_populations_run._lottery_numba`): complete island graph, I islands of N, Moran birth–death with parent weight
exp(w · mean payoff) on the source island, a migrant parent from a uniformly chosen other island with probability
m = mN/N, uniform victim, w = 0.3, PD payoffs (D/D −1, D/C 1, C/D −2, C/C 0), iid seeding (each slot drawn from the
cell's prior over spellings, mapped to classes); one generation = I·N births; checkpoints every 10 generations. At
ε = 0 no class appears after seeding, so the payoff matrix is restricted to the seeded classes (exact).

- **Endpoint E3** (milestone 2's, unchanged): Z(island) = closure of the island's residents under "a class present
  anywhere joins if U(q, z) ≥ U(z, z) for some z ∈ Z"; resolved cooperating iff every class in Z self-cooperates;
  resolved non-cooperating iff none does. **E3 success** = every island resolved cooperating.
- **E3 is island-level**: a patchwork of rival cooperative islands is E3-success (a rival migrant earns −1 < 0). So the
  run does **not** stop at E3. It stops when **frozen** (U is constant on the global support: no payoff difference
  remains, so nothing can change any realized play) or at the horizon.
- **Universality, measured directly:** cross-island P(C,C) = the mean over ordered island pairs (i ≠ j) of
  x_iᵀ PCC x_j (x_i the island's composition), reported beside **open-carrier occupancy** (the share of islands whose
  majority class mutually cooperates with CB).
- **Run outcome at a horizon:** *universal-open* (every island at P(C,C) ≥ 0.9, cross-island P(C,C) ≥ 0.99, occupancy
  1); *universal-other* (the same with a non-open holder everywhere, e.g. a clique or a club); *patchwork* (every island
  at P(C,C) ≥ 0.9, cross-island P(C,C) < 0.99: two islands' majority classes mutually defect); *failed* (some island
  resolved non-cooperating, or a non-cooperating class fixed globally); *unresolved* (anything else). **Separated** at a
  checkpoint = two cooperative islands (P(C,C) ≥ 0.9) whose majority classes mutually defect.
- **Censoring:** a run not frozen and not universal at the horizon is censored for the universality score (counted in
  the denominator as not-universal and reported separately). **Separated runs at generation 2,000 are continued to
  10,000** (same random stream), reported as a separate column.
- **Hazards:** separation hazard per island pair h_sep = −ln(1 − P(ever separated))/C(I, 2) (a per-pair rate of rival
  co-establishment over the run); resolution hazard = (separated runs that become unseparated) / (separated
  run-generations), with the minority-island loss rate (losses per minority-island-generation) beside it.
- **Family labels** of an establisher class, in priority: *open* (mutual C with CB), *exclusive* (mutual C with XC),
  *tag1* / *tag2* (mutual C with TC1¹ / TC2²), *identity* (no mutual cooperation with any other establisher class),
  *other*. Patchworks are named by the labels of the islands' majority classes.
- **Pooling check** per run: the maximal cliques of the compatibility graph restricted to the seeded establishers;
  for each, the seeded count globally and the maximum per island; its **established mass** = individuals of its members
  alive at the first checkpoint at which every island is at P(C,C) ≥ 0.9; a set **won** iff every island ends at
  P(C,C) ≥ 0.9 and every establisher alive at the end belongs to it. Reported: whether the set with the largest seeded
  count won, and whether the set with the largest established mass won.
- **Bridge fate** (T2 and L): global counts of the marked carriers (CB's run tree with marker t), the or-forms and the
  and-forms, their extinction generation, and whether the bridge was alive at the first separation.
- **Cells** (40 runs each, Wilson intervals): L at (N, I) = (100, 64), (200, 64), (100, 256), mN = 1; at (100, 64): U,
  T1a, T1b, T1c, T2, T3 and the three ablations.

### 1.11 Chain (diagnostic only)

`chain_log.LogChain` with twin drift over the lumped classes, L, N = 10⁴, closure-seeded (milestone 2's seeds:
monomorphic states, stable candidates on the 120 heaviest classes, invasion closure), θ_log = 10⁻¹⁴; `FastChain` for the
monomorphic fates if the class count makes `LogChain` too slow (milestone 2 validated it). Reported: top states,
absorption, the absorbing clique's name and mass. **No-clique control** at N = 10³ and 10⁴ (closed leak components
removed iteratively), with the odds slope from those two points only.

### 1.12 Validation plan (before any counted cell)

1. Grammar counts reproduce §1.1 (bodies 25,762; spellings 34,968; τ-units 17,304 + CB).
2. Compilation: `eq` is T exactly in self-play; `tag_t` returns the marker set on every marked/unmarked carrier and F
   on `PROG_C`, `PROG_D`; a marker changes no play of a tag-free program (whole plays, marked vs unmarked, on a sample).
3. Production: CB, CB1, CBP lists equal milestone 4's (and ⌜CB⌝ is the catalogue's CB term); the named lists of §1.6;
   lists depend on (dt, M ∩ tags) only (sample of marked spellings produced directly); the count of milestone-2-shaped
   spellings whose list changed under the extended probes.
4. The §1.6 hand table, cell for cell, by whole actual plays (`lt_code.play`).
5. Composition and Lemmas T′, R: random spelling pairs (including marked pairs, same-τ twins, self-plays and pairs
   whose markers differ only outside G) played whole against the composed table: 0 mismatches.
6. Identity-aware lumping on a sample: every eq-clique spelling is a singleton class; marked/unmarked CB are separate
   classes; the spelling-level criterion holds on a random sample of merged pairs (rows and columns against a sample
   of opponents played whole).
7. Families on the named sub-catalogue reproduce §1.7 (maximal cliques, bridges, AF¹ not a bridge, OF¹ exploitable).
8. The ideal table equals the executable table on a sample of classes (the heaviest, a random set, every named class).
9. The tilts' seed laws: empirical seed frequencies of the tilted blocks match M, M/10 and the renormalized rest.

### 1.13 Code validation of §1 (appended after the code, before any counted cell)

*(to be appended)*

## 2. Implementation and costs

*(to be appended)*
