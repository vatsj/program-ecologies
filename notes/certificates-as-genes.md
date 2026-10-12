# Certificates as genes: the realizable language, milestone 5 (notes, 2026-10-11)

Spec `specs/2026-10-11-certificates-as-genes.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-11-certificates-as-genes-gpt-6.1-sol.md`;
the [after review] text is the resolution). §1 is written before any code of this milestone and before any counted
cell: the four production modes and their costs, the certified object and Lemma A, fuel allocation, steps against
price, initialization and host ancestry, the state and the frozen encounter/update ordering, the copied-script faker,
the hand-derived first and second encounters of the named pairs, and the transfer compatibility graph. §1.12 (code
validation) is appended after the code exists and before any counted cell; §2 (costs) after that.

Base, imported unchanged: `notes/certificates-as-code.md` §1 ("milestone 4": K_T^cert, the checker term CC, Lemma N,
Lemma Sym, Theorem S^cert, the frozen tactic of §1.9), `notes/prover-as-code.md` §1 ("milestone 3": L_T^code, the fuel
rules, the cap semantics of a library call), `notes/carrier-populations.md` §1 ("milestone 2": the template grammar,
composition of clean check values, Lemma T, the lottery and endpoint E3), `notes/identity-tags.md` ("the identity
run": no-op markers, the holder-based endpoint).

*Disclosure.* Before writing this section I ran one scratch count on milestone 2's P catalogue (no plays, no cell):
the frozen tactic's lists over the 4,162 run trees contain **25 distinct (outcome, script) entries** (24 scripts), and
every list holds at most one C entry and one D entry (list shapes: D only 1,638 run trees, C only 1,500, neither 581,
both 443). This number decides how large the inventory state can get (§1.8).

## 1. Design

### 1.0 What changes, in one paragraph

Milestones 2 and 4 attached each carrier's certificate list at birth by a host tactic that nobody paid for. Here the
list is a **gene**: a per-individual, heritable, transmissible part of the genotype, and how a program gets its
scripts is a heritable **production mode**. A script can arrive four ways: from the host (H, the old baseline), by the
program's own in-language production run inside its encounter budget (S), by checking a script the opponent publishes
against its own code and adopting it if the check passes (C), or copy-then-search (CS). Three facts organize what
follows. (i) **Soundness never depends on where a script came from**: Theorem S^cert holds for every quote, so every
check a reader makes at play time certifies the actual object it reads, whatever its history (§1.5). What adoption
can break is *validity*, not soundness: a script checked on one list can stop validating after the list changes; Lemma A
says exactly when (§1.5). (ii) **Copying moves a script only along a call skeleton**: a script is a derivation
skeleton, so it validates on another code only if that code's run has the same calls in the same branch positions;
the transfer graph is therefore made of skeleton blocks (§1.11), and copy-and-check cannot create the first script of a
skeleton (§1.7). (iii) **Production as code costs about what a check costs**: milestone 3's 10⁵–10⁶ steps were the
cost of *reading by search* (a reader searching for a proof about the opponent, which re-enters the opponent's
search); producing a script for *one's own* run never runs the opponent's search, so the tactic as code costs
10⁴-ish steps (a guess, §1.3) and the realizability gap the spec names closes for production as it did for checking.

### 1.1 Programs: the gene triple

A program is **(code, mode, list)**: code a milestone-2 template (or a named milestone-4 carrier body), mode
μ ∈ {H, S, C, CS}, list a certificate list (outcome, script) entries.

- **Quote.** The quote a program publishes, and that every check reads, is the carrier term
  `λme. λthem. (λcerts. BODY_μ) CERTS` with **the mode as a no-op marker**: BODY_μ = `(λ_. body↑) ⟨9100 + μ⟩`
  (μ = 0, 1, 2, 3 for H, S, C, CS; ↑ shifts the body's free variables certs, them, me by one), exactly the identity
  run's marker construction. So the quote is (code, mode, list), as the spec requires. Nothing in the grammar reads
  the marker (no tag atoms here); it costs one β step of the program's own run, absorbed by EvR*, and it makes two
  individuals with the same code and list but different modes *distinct quotes* (twins, not self-play).
- **Canonical list.** CERTS is the C block followed by the D block, each in acquisition order; an adopted or produced
  entry is appended to its outcome's block. The checker filters entries by the asked outcome and tries them in order
  (milestone 4 §1.4), so only the order *within* a block can matter (§1.5, F2). H's lists already have this form
  ("C scripts then the D script").
- **Unit.** For the population tables the behavioural object is the **unit** u = (dt, Cseq, Dseq): the code's run tree
  (milestone 2 §1.3) and the two blocks. Lemma T (milestone 2), with τ = (dt, list) and the marker as another source
  feature that no program reads, makes every check value a function of the units involved, of which pairs are the
  same quote (self-play), and of nothing else (§1.8).

### 1.2 The encounter, the fuel allocation, and steps against price

An **encounter** of x and y: each side gets the budget **K = 10⁶** steps (V = ⌊K/4⌋ in every source, as before). The
quotes ⌜x⌝, ⌜y⌝ are fixed at the start of the encounter. Frozen order, per side:

1. **Play.** The actual run of `x ⌜x⌝ ⌜y⌝` with global fuel K (milestone 4 semantics, unchanged): W_play steps, an
   action (⊥ scores as D).
2. **Production.** x's mode procedure (§1.3) runs **after** the play, as ordinary L_T^code evaluations charged to the
   **same budget**: it gets the residual K − W_play. Each production act is a library call with a declared cap (a
   check: ≤ V + 6; a production search: ≤ P + 4). If an act would exhaust the residual, it times out and adopts
   nothing (a **production timeout**, classified and counted by mode). Since W_play ≤ 2(V + 6) + 10³ and the acts are
   sequential, the residual is ≥ K/2 − 10³.
3. **Update.** Adopted entries are appended; the new list is x's list from the next encounter on.

**Why production after play.** The certified proposition (§1.4) is about the fuel-K play run of the quoted object.
If production ran *before* the play in the same budget, the actual play would get K − W_prod while every reader's
certificate is about the fuel-K run: a reader could accept "x cooperates" and meet a timeout (D). That is the exact
point where soundness of the *encounter* fails under pre-play allocation (§1.5, F0), demonstrated by a test, not run
in the populations. The **reserved variant** (production first, but the program declares K_play = K − (P + 7) in its
check atoms, so readers certify the run it actually gets) is sound and is reported in the single-pair tables only.

**Steps against price.** In the main cells steps only consume the budget: a production timeout adopts nothing, and no
step is a fitness cost. So "charged" is not a selective price there, and the ALLC-ladder analogy is not claimed.
The separate **price arm** subtracts c · (production steps)/K from the per-match payoff of the producing side,
c ∈ {0.01, 0.1} (the spec's), with c ∈ {1, 10} as labelled extras because the spec's values are tiny against drift
(§1.10). Only the price arm is compared with RESULTS "Price scaling paths". Play steps are never priced here (a
per-match price on reading is RESULTS "K at n = 8"'s ladder, already measured), so the price arm prices production
only.

### 1.3 The four production modes: semantics and costs

Notation: CHK(t, q, a) is the sound check wrapper call `app(lib CHK_S, (V, (⌜t⌝, (⌜q⌝, (a, K)))))`, cost W + 6 ≤ V + 6
(milestone 4 §1.1); x_s := (x's code, x's mode, [(a, s)]) the **single-entry quote** of x carrying only s.

- **H (host).** The list is milestone 2's frozen production (the milestone 4 tactic against ⌜D⌝ for the D script and
  the probes CB, CB1, CBP for C scripts), fixed for life, inherited unchanged, **free** (not charged to any encounter:
  a host service, as in milestones 2 and 4). Production effort per run tree is reported, never charged.
- **S (search, the in-language producer).** After the play:
  1. *Gate:* g = CHK(x, y, C) — "am I already certified as a cooperator against this opponent?". If g = T, skip 2.
  2. *Produce C:* s = PROD(P; x, y, C). If s is a script and (C, s) is not in x's list, append it.
  3. *Produce D:* if x's list (as updated) has no D entry, s = PROD(P; x, ⌜D⌝, D); append if a script.
  **PROD** is a new library entry, `PROD = λarg. capk(fst arg, PCORE, snd arg)`, arg = (P, (V, (⌜t⌝, (⌜q⌝, (a, K))))),
  cost W + 4 ≤ P + 4; a core timeout returns TO, which adopts nothing. **PCORE is milestone 4's frozen tactic (§1.9)
  written in L_T^code**: it builds the root ψ = ⟨t ⌜t⌝ ⌜q⌝, K⟩⇓a and the boxes R, S exactly as CC does, and applies,
  at each sequent, Ax; Hyp on the first right box in {R, S}; RunNeg on the first left box (not R or S, cap ≥ V) whose
  check runs to F or TO; Run on the first right box whose check runs to T; otherwise the first right atom by EvR* (a
  deterministic step) or ChkR (a fitting check call, premise 1 first); else fail; bound 64 nodes. Run/RunNeg run the
  box's check in-language (`callcheck`), nested in PROD's frame. It uses the checker's own helpers (cstep, evstar,
  chkstate, fadd, fdel), so its formulas are the checker's formulas. The host `Producer` is its reference
  implementation; the term must equal it on every catalogue query (validation, §1.12).
  *Deviation from the spec's text, stated:* the spec names "the search CORE of milestone 3" as the in-language
  producer. Milestone 3's CORE searches K_T^code derivations, a calculus with no rule for check calls whose
  self-interpreter treats a check wrapper as an ordinary β step (milestone 4 §1.5, §1.8: searchers' queries about
  carriers are never found); it cannot output a K_T^cert script, and an explicit derivation of one's own run cannot
  be carried at all (milestone 4, Lemma F). So the only in-language producer of a carriable certificate is a search
  over K_T^cert scripts; I use the frozen tactic (a deterministic, non-backtracking proof search; CLAUDE.md's queue
  item 25 calls this milestone "the tactic as code, charged"), with milestone 3's cap semantics. S therefore runs the
  same algorithm as H, against the actual opponent instead of the probes, charged, after the encounter.
  *Cost guess (not a computation):* the tactic visits 2–8 script nodes (milestone 4: 20–29 tactic nodes per source
  over all probes), each EvR*/ChkR node the price of the checker's node (a few hundred to a few thousand steps), plus
  one nested check per Run/RunNeg (≤ 10⁴; a certificate-less target costs a few hundred): **5·10³–3·10⁴ steps per
  produced script**, below 10⁵ and far below P = K/4. The gate costs one check (≈ 10³ if x has no C entry, the full
  check, 0.9–4·10⁴, if it has one).
- **C (copy-and-check).** After the play, for each entry (a, s) of ⌜y⌝'s list (as quoted at the encounter, in its
  order): skip it if x already adopted an a-entry in this encounter or if (a, s) is already in x's list; otherwise run
  the **adoption check** AC(x, s, a) := CHK(x_s, q_a, a) with q_C = ⌜y⌝ (the donor) and q_D = ⌜D⌝ (the probe of every
  D script, as in H); if T, append (a, s). Cost per tried entry: the check (W + 6) plus the construction of ⌜x_s⌝
  from ⌜x⌝ (quote surgery on the CERTS literal: one step per encoded node of the new list, ≈ 10²), charged.
  **Publication disabled** (control): x sees no donor entries (no horizontal transfer); plays are unchanged.
- **CS.** C's step, then S's step on the updated list (the gate reads the updated x).

**Negative-result caching** (sol): a refused (s, donor) pair is refused again at the next identical encounter, since
the check is deterministic. The *dynamics* do not cache (state stays (code, mode, list), so refusals are re-paid);
the single-pair tables report the per-match cost with and without a per-individual negative cache, and the population
cost statistics are the uncached ones.

### 1.4 The certified object

The quote a program publishes is (code, mode, list as of the encounter). A sound check CHK(x, q, a) = T certifies
⟨x ⌜x⌝ ⌜q⌝, K⟩⇓a: the fuel-K run of *that* quoted object against *that* quoted opponent. Under the post-play
allocation this run **is** the encounter's play, because production happens after the action is fixed and the list
change takes effect only from the next encounter (with a new quote). So every acceptance at play time is about the
actual play (Theorem S^cert, unchanged), whatever x's mode and history.

### 1.5 Lemma A: what adoption preserves, and where it fails

Let x = (c, μ, L), s a script, a an outcome, q a quote, and suppose the adoption check passed: CHK(x_s, q, a) = T.
Let x' = (c, μ, L ⊕ (a, s)) be the adopted object.

**(A0) Soundness is preserved unconditionally.** For every quote z and every opponent r, CHK(z, r, b) = T implies
⟨z ⌜z⌝ ⌜r⌝, K⟩⇓b (Theorem S^cert holds for arbitrary quotes). So no adoption, inheritance, or production ever makes
a reader accept a false atom about x'. *This is the sense in which adoption preserves soundness, and it needs no
lemma about adoption.*

**(A1) Validity transfers when no Run/RunNeg box reads x's list.** Let 𝒟 be the derivation that s encodes at the
root (x_s, q, a) and, if s closes S, the partner's derivation found by the partner validation at (q, x_s, a). Suppose
every box b on which 𝒟 applies Run or RunNeg (in either derivation, at any depth of the nested checks those rules run)
has the same clean value when x_s is replaced by x' in b's argument. Then s is valid at the root (x', q, a), with
the same usesS, and the partner validation at (q, x', a) returns the same value. If moreover no entry of L's a-block
is valid at (x', q, a) before s is reached, CHK(x', q, a) = T.
*Proof.* A script check consults the target's quote in four ways (milestone 2, Lemma T's proof): (i) the
self-interpreter steps along the target's run; (ii) `getcerts`; (iii) syntactic equality of boxes (Hyp: box = R or S;
Ax: a box or atom in both lists; fadd/fdel deduplication); (iv) nested checks through Run/RunNeg. The run of c's body
never reads the let-bound list (BODY does not use `certs`), so the runs of x_s and x' against q take the same steps in
the same order, reach the same call states with arguments that differ only by the quote substitution x_s ↦ x', and
have the same step counts (the list is an inert literal inside a quote; `eq` and quotes are unit cost), so every fit
side condition (ChkR, EvR*'s f ≥ 1) is decided identically. The roots R, S are rebuilt from the two quotes, so the
substitution maps R to R and S to S: Hyp nodes stay valid. Ax and fadd/fdel are equality tests, preserved by the
substitution because it is injective (x_s ≠ q and x' ≠ q: a quote with a different list or mode marker is a different
quote, and if q were x_s itself the encounter would be self-play, where the adoption check is not run since x would
already hold s). Run/RunNeg nodes are valid iff their boxes' clean values are, assumed unchanged. The same argument
applies to the partner's derivation. So the validator returns the same (valid, usesS), the partner validation the
same value, and since `tryents` accepts the first valid entry of the a-block, if none precedes s the check returns T. ∎

**(A2) Exactly where it fails.**
- **F0, fuel allocation (the encounter, not the check).** Under pre-play production the accepted atom is about the
  fuel-K run while the actual play gets K − W_prod; a script accepted by a reader can be followed by a
  production-induced timeout and the reader exploited. Excluded by the post-play allocation (§1.2); demonstrated by a
  test with a pre-play encounter; repaired by the reserved variant.
- **F1, list-dependent boxes.** A Run/RunNeg box whose clean value depends on x's own list: a box with x as target
  (x's run checks itself, e.g. an atom `CHK(me, ⌜D⌝, D)` or `CHK(me, them, D)` on the non-root outcome), or a box with
  x as opponent whose target's run or validation reads x's list (e.g. ⊡(q, x, D): q's run against x checks x's
  certificates). Adding s can flip such a box. *Natural instance (hand):* LöbC = `if(CHK(me, them, C), C, D)` in mode C
  meeting an H-carrier CB with list [(C, σCB), (D, δ)]. It adopts σCB (the call's box is the root's R at (x_s, CB, C):
  Hyp^self, valid, no partner validation). It then tries δ: x_δ = (LöbC, [(D, δ)]) at (x_δ, ⌜D⌝, D): LöbC's call box
  ⊡(x_δ, ⌜D⌝, C) asks the other outcome, so it is not R; RunNeg needs it false; x_δ has no C entry, so it is false; the
  F-branch reaches D: **valid, adopted**. But in x' = (LöbC, [(C, σCB), (D, δ)]) the same box ⊡(x', ⌜D⌝, C) is true
  (σCB closes it by Hyp^self, so LöbC' now cooperates with ⌜D⌝), RunNeg fails, and **δ is invalid in x'**. Soundness is
  intact: a reader asking "does LöbC' defect against ⌜D⌝?" finds δ invalid and gets F, which is the truth.
- **F2, first-valid order.** An earlier entry e of L's a-block that is valid at (x', q, a) decides instead of s; if e
  closes S and s does not, x' needs a partner validation that x_s did not, and the check can return F where AC
  returned T. (If e and s both close S, the partner validation is the same computation, Lemma Sym's argument, so the
  outcome is the same.) Requires two valid scripts of one outcome for one code with different hypothesis use; under
  the frozen tactic lists hold one entry per outcome (disclosure), so F2 can only arise through copying or
  production against several opponents.
- **F3, cost.** The check of x' walks a longer list (failed earlier entries cost their failed validation), so its
  step count can exceed x_s's; a value change only if it crosses V.
- **F4, the probe.** AC certifies against the donor as quoted at that encounter. A script is a call skeleton, so its
  validity against a later opponent is a fresh question (partner validation and Run boxes about that opponent);
  every reader asks it anyway at play time, so this is a statement about usefulness, not soundness.

**Corollary (what the populations measure).** For every adoption event the dynamics record whether the adopted
object is certified against the donor (CHK(x', donor, a) = T), i.e. whether Lemma A's transfer succeeded; the
fraction of adoptions that fail transfer, by failure type, is reported. Lemma A predicts 0 failures for scripts whose
derivations have no list-dependent Run/RunNeg box (F1) and no earlier valid same-outcome entry (F2).

### 1.6 The copied-script faker, and the donor's exposure

**CF = (code D, mode C, empty list).** Claim: CF never adopts a C script, in any cell, against any donor. *Proof.*
Adoption needs CHK(CF_s, q, C) = T for some s, q; by Theorem S^cert (A0) that implies ⟨CF_s ⌜CF_s⌝ ⌜q⌝, K⟩⇓C; but
the D code's run reaches D. ∎ So "0 accepted copied C scripts against a code that defects" is a theorem, the
spec's falsifier for RE 3 cannot fire unless the checker term is wrong (Lemma C). More generally, **no code adopts a
script certifying an outcome its run does not produce against the probe** (same argument), and a list obtained by
inheritance is re-validated by every reader at every play (Lemma A0), so a program carrying scripts it did not produce
cannot be accepted for anything it does not do. *What CF can adopt:* true D scripts (e.g. ε = `EvR*; Ax` from a
certificate-carrying defector), which certify that it defects against ⌜D⌝: true, and useful only to PB-shaped
readers, which then still refuse it (CF never cooperates).
*Refusal cost (hand):* the adoption check of σCB on CF's code walks D's run to its value (a handful of interpreted
steps), fails at the first ChkR (no call state), and returns F: getcerts, root construction, one EvR*, ≈ 10³ steps
(a guess); paid by CF, every encounter with a carrier donor (no negative cache in the dynamics).
*CF's fitness* is not predicted: refusal is cheap and CF is a defector, so it earns what D earns.

**Donor exposure.** A copier's adoption check runs in the copier's budget; partner validation inside it validates the
donor's script on the donor's run, also in the copier's budget. The donor pays nothing for being copied. A copier
that adopts a C script and then defects on the donor is impossible (A0: the adoption check certified that the new
object cooperates with the donor, against the donor as quoted). A copier that adopts and cooperates is a new partner
(and a neutral competitor if it has the donor's code).

### 1.7 Initialization, host ancestry, controls

- **Empty C-only is an invariant.** If every founder is in mode C with an empty list, every list stays empty: C adopts
  only entries of the opponent's list, all empty; inheritance copies empty lists. ∎ The cell is run (40 runs) to
  confirm it; every check in it returns F, so it is milestone 2's catalogue with every program certificate-less.
- **Declared seed f₀ ∈ {0.05, 0.25}:** each founder of the C-only cell independently carries its H-produced list
  with probability f₀ (mode C, labelled an **exogenous subsidy**); the rest empty.
- **Single donor:** every founder in mode C with an empty list, except one slot per island, which holds an
  **H-mode establisher** (a spelling drawn from the prior restricted to establishers that carry a C script; its
  offspring are H). The donor's identity is reported.
- **CS-only and S-only** start empty; **H-only** is milestone 2's L×P ecology (with mode markers).
- **Host ancestry.** Every held script instance carries a tag: *host* if it descends (by copying or inheritance) from
  an H-produced instance, *search* if from an S production. Copying takes the donor instance's tag; inheritance the
  parent's; production writes *search*. The tag is bookkeeping (not in the quote, so it changes no play). "Endogenous"
  = the fraction of held script instances tagged *search*. Tags are tracked as part of the individual's state in the
  cells where both tags can occur (mixed modes, identical-inventory mixed); elsewhere they are determined by the arm
  (H-only, seeded and single-donor C-only: all host; S-only, CS-only: all search). Most recent transmission is
  counted as events (copies, productions, births), not stored per instance.
- **Controls (paired seeds and encounter schedules across arms):** C with publication disabled (seeded f₀ = 0.25:
  only vertical transfer); C with inheritance disabled (seeded f₀ = 0.25: offspring start empty, only horizontal
  transfer); **identical initial inventories** (mixed modes, every founder starting with its H list regardless of
  mode) beside the empty-inventory mixed cell. Paired seeds: replicate r of every arm at the same (N, I) uses the same
  founder spellings and the same random stream for the Moran and encounter draws (they diverge once the dynamics
  differ).

### 1.8 State, units, and the frozen ordering per Moran event

**State of an individual:** (spelling, mode, list, ancestry tags). **Lemma T with inventories:** two individuals
whose (dt, Cseq, Dseq) agree play every opponent alike and are played alike, provided they are distinct quotes (twin)
or identical quotes (self), by milestone 2's Lemma T with τ = (dt, list), since the mode marker is a source feature
nothing reads. Every production result is also a function of the units involved: the gate is a check value; AC is
a check value of the unit (dt_x, [(a, s)]); PROD's output is the tactic's, whose choices are Hyp (syntactic: which
atom is R or S), Run/RunNeg (check values of units) and EvR*/ChkR (the run tree). So the population is computed on
**units** u = (dt, Cseq, Dseq) with three exact tables over units: the action table A[u, v] (composition, twin play on
the diagonal), the self-play vector, and the transition tables TR_μ[u, v] (the unit x becomes after meeting v, by
mode). An individual's **type** is (unit, mode, spelling if the unit's twin play differs from its self play, ancestry
tags); two individuals are the same quote iff same spelling, same mode and same list.
*Identity:* for a unit whose twin play equals its self play the spelling is dropped (lumping over spellings with
identical inventories and transitions, as the spec asks); for a split unit (milestone 2's TwinD family: the R/S
coincidence makes self-play special) the spelling is kept, and an individual of another mode with the same spelling
and list is its twin, not itself.
*The universe of units* is the closure, over all run trees, of {(dt, H list), (dt, ∅)} under TR_S, TR_C, TR_CS
(computed once, with every check value needed by A and TR; §1.12 reports its size). The 24-script disclosure bounds
it: a unit's blocks are sequences of distinct scripts valid for its run tree.

**Frozen ordering per Moran event** (I·N events per generation, milestone 2's kernel otherwise):
1. **Encounters (play, then adoption):** r encounters; each picks an island uniformly, a focal individual uniformly on
   it and a partner uniformly among the other N − 1 residents; both play (the payoffs enter fitness through the mean
   payoff below, not through the sample); then both run their mode procedure against the other's pre-encounter quote,
   and their types are updated.
2. **Reproduction:** milestone 2's: an island i uniformly; a source island (i, or with probability m = mN/N another
   island uniformly); a parent from the source by weight exp(w · mean payoff against the source's other residents),
   w = 0.3; a uniform victim on i; the child inherits the parent's (spelling, mode, list, tags) exactly (inheritance
   disabled: the child gets the mode's founding list, ∅ for S/C/CS, the H list for H).

**Encounter rate.** Fitness is the expected per-match payoff (the mean over residents), so matches are an
expectation, and r sets how many sampled matches feed adoption per event. Main: **r = N/2 = 50** (≈ 100 matches per
individual per generation, about one with every island resident, the round robin that the mean payoff stands for).
Sensitivity: **r = 1** (≈ 2 matches per individual per generation; slow transfer) on the mixed, seeded C-only and
single-donor cells.

### 1.9 Hand-derived first and second encounters (K = 10⁶, V = 2.5·10⁵, P = K/4)

Scripts (milestone 4): σCB = `EvR*; ChkR[EvR*; Ax · Hyp]`; σCB1 = `EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Hyp] · Hyp]`;
σCBP = `EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Run] · Hyp]`; δ = `EvR*; ChkR[RunNeg · EvR*; Ax]` (the common D script of
every carrier whose first call asks the opponent about me); ε = `EvR*; Ax`. Inner check costs (milestone 4, K = 10⁷;
the K = 10⁶ values differ by a few steps): CB self-play (R = S, one validation) 8,782; a pair of distinct quotes
running two σCB validations ≈ 2 × 8,782 ≈ 1.8·10⁴ (guess); CB–CB1 21,541; CB–CBP 30,491; CB1–CBP 37,140; a check of a
listless target ≈ 10³ or less (guess: getcerts, the root, an empty `tryents`). Play cost = the side's check calls
(W + 6 each) + O(10).

**Same code, distinct quotes (CB as copier or searcher, CB-H as the other side).**
| modes (x, y) | encounter 1 | x's production after 1 | encounter 2 | to steady (C, C) | x's steady per-match cost |
|---|---|---|---|---|---|
| H, H (same spelling: one quote) | (C, C), self-play | — | (C, C) | 1 | 8.8·10³ |
| C, H | (D, D): x has no list, so CB-H's check of x fails, and x's check of CB-H fails at partner validation | AC(σCB) vs CB-H: T (σCB closes S, partner validation of CB-H's σCB closes R) ≈ 1.8·10⁴; AC(δ) vs ⌜D⌝: T ≈ 10⁴; adopts both | (C, C) (distinct quotes: two validations) | 2 | ≈ 1.8·10⁴ play, 0 production (both entries held) |
| S, H | (D, D) | gate ≈ 10³ (F); PROD(x, CB-H, C) = σCB; PROD(x, ⌜D⌝, D) = δ | (C, C) | 2 | ≈ 1.8·10⁴ play + gate ≈ 1.8·10⁴ |
| CS, H | (D, D) | as C; the gate on the updated list is T, no production | (C, C) | 2 | play + gate |
| C, C (both empty) | (D, D) | nothing to copy | (D, D) forever | never | AC 0 (no entries), play ≈ 2·10³ |
| C, C⁺ (y seeded with the H list) | (D, D) | as C, H | (C, C) | 2 | as C, H |
| S, S (same spelling: one quote) | (D, D), self-play | both produce σCB, δ (identical) | (C, C), self-play (Hyp^self) | 2 | 8.8·10³ + gate 8.8·10³ |

So the steady per-match cost of a copier against a same-spelling H partner is about **2×** H–H's (a pair check
against a self-play check), and equal to H's against a distinct spelling (H–H is then also a pair).

**Distinct skeletons (CB–CB1, CB–CBP, CB1–CBP, in either role).** C, H: encounter 1 (D, D); the copier adopts δ only
(σCB1 and σCBP do not fit CB's run: after CB's call the T-branch reaches C where they expect a second ChkR; σCB does not
fit CB1's or CBP's run: its Ax meets a call state); (D, D) forever, **off the graph**. S, H: encounter 1 (D, D); x
produces its own skeleton's script against y (CB1: the second call's box is the root's R, Hyp^self; CBP: the second
call's box ⊡(y, ⌜D⌝, D) is Run, true since CB/CB1 carry δ) and δ; **encounter 2 (C, C)**. S, S (both empty, distinct
codes): CB–CB1 (C, C) from encounter 2; **CBP–CB and CBP–CB1 from encounter 3**: in encounter 1 the partner carries no
δ yet, so ⊡(y, ⌜D⌝, D) is false, CBP's tactic closes premise 1 by RunNeg and cannot close premise 2 (the F-branch
reaches D), and returns nothing; in encounter 2 the partner has δ but CBP has no C script, so (D, D) again (the
partner's σCB closes S and its partner validation finds no C script of CBP); CBP's gate fails, it now produces σCBP;
encounter 3 (C, C). CS: as S (nothing to copy across skeletons except δ, which the D step would have produced).
**Respellings with the same skeleton** (CB–CBlet, CB–CBwrap, CB1–CB1r, CB–MC¹ (CB with a tag marker), CBP–CBPh): C, H
is **on the graph**, (C, C) from encounter 2 (milestone 4: the class script validates on CBlet2, CBw2, CB1h, CB1r,
CBPh). **CBPr** (PB-shaped, the D check first) has its own skeleton: off the graph from CBP.

**Named fakers and oddities (mode of the first program; the second is H).**
- **CF (D code, C) vs CB-H:** (D, D) every encounter; AC(σCB) F, AC(δ) F (δ's ChkR meets D's value); 0 adoptions.
  vs Dc-H (D code with [(D, ε)]): adopts ε (true). vs Cc-H (C code with [(C, ε)]): AC(ε) F (its run reaches D).
- **LöbC (C) vs CB-H:** adopts σCB (Hyp^self, valid without partner validation) and δ (§1.5 F1: δ is invalid in the
  adopted object). Encounter 2: (C, C); LöbC' is a certified CooperateBot (C against ⌜D⌝ too).
- **CBdef (C) vs CB-H:** adopts nothing (σCB: the T-branch reaches D; δ: CBdef cooperates with ⌜D⌝).
- **CB (C) vs CBmut-H** ([σCBP, σCB], no D script): σCBP refused, σCB adopted; no D script to copy.
- **CB (C) vs Dcert-H:** every bogus script refused. **vs CBsloppy-H:** its C script Runs the sloppy box at CB's S
  position (Run on S is forbidden): refused; its D script is the same data as δ: adopted.
- **Searchers** (milestone 3's FB_code etc.) have no CERTS slot, so they cannot carry, copy or produce; against
  carriers they play (D, D) as in milestone 4. They are opponents only.

### 1.10 Populations: cells and statistics

Milestone 2's P grammar at n = 7 (12,546 spellings), prior L (2^−nodes per spelling), K = 10⁶, the sound checker,
PD payoffs (D/D −1, D/C 1, C/D −2, C/C 0), w = 0.3. The seed lottery at (N, I) = (100, 64), complete island graph,
mN = 1, 40 runs per arm, horizon 2,000 generations, checkpoints every 10, r = 50, P = K/4. Mode prior ¼ each where
modes segregate.

**Arms:** H-only; mixed (modes iid ¼ each, empty except H); S-only; C-only with f₀ = 0.05 and 0.25; C-only single
donor; C-only empty (the invariant); CS-only; C f₀ = 0.25 with publication disabled; C f₀ = 0.25 with inheritance
disabled; mixed with identical (H) initial inventories; the price arm (mixed, c ∈ {0.01, 0.1}; extras c ∈ {1, 10});
the size sweep N ∈ {50, 200} at I = 64 for mixed and C f₀ = 0.25; r = 1 for mixed, C f₀ = 0.25 and single donor.

**Statistics per run** (ε = 0 finite-(N, I, horizon) evidence; never pooled with the chain):
- *Establishment:* the first checkpoint with an island at P(C,C) ≥ 0.9 (milestone 2's); unconditional establishment
  probability = established runs / 40 with Wilson intervals; establishment times with censoring at 2,000 (the
  Kaplan–Meier estimate is the empirical distribution with a mass beyond the horizon; medians reported only where
  defined).
- *Persistence:* the fraction of ever-≥ 0.9 islands that are ≥ 0.9 at the horizon; mean island P(C,C) at the horizon.
- *Endpoints:* E3 (milestone 2's closure test, polymorphic islands allowed) and the holder-based outcome of the
  identity run (holder = an island's majority type when it self-cooperates and island P(C,C) ≥ 0.5; universal = every
  island held and every pair of holders mutually cooperating; patchwork; failed); **universal-open** = universal with
  every holder mutually cooperating with CB-H; cross-island P(C,C); **identity islands** = islands whose holder
  cooperates with no other establisher type present.
- *Modes:* the mode composition of individuals of self-cooperating holder types on held islands at checkpoints
  10, 50, 200, 1,000, 2,000.
- *Costs:* mean production steps per match by mode (play steps reported beside), production timeouts by mode, play
  timeouts by mode (0 by construction under post-play; reported).
- *Scripts:* distinct scripts held at the horizon and over time, by provenance (host / search) and their
  host-ancestry fractions; the number of (skeleton, outcome) pairs present (a skeleton is identified with the script
  data, so the number of distinct scripts *is* the number of (skeleton, outcome) pairs unless one code holds two
  scripts for one outcome; both counts are reported); copy events, productions, births.
- *Lemma A in the population:* adoptions whose transfer failed (§1.5 Corollary), by type.

**Chain diagnostic (labelled a frozen-inventory approximation):** milestone 2's LogChain over units with inventories
frozen at their founding values (no adoption: an S/C/CS program stays certificate-less), N = 10⁴, for the mixed arm and
H-only. A static table cannot carry inherited lists, so this is not the ε→0 object of the gene dynamics; it is
reported only as a diagnostic of what the founding inventories alone would select.

### 1.11 The directed transfer compatibility graph

**Definition.** Donors: every unit (dt, H list) of the P catalogue. Recipients: every run tree dt in mode C with an
empty list. **C-edge** y → x iff some C entry s of y's list passes AC(x, s, C) against y (the adoption check of x's
code carrying only s, against y as the partner). **D-edge** y → x iff some D entry s of y's list passes AC(x, s, D)
against ⌜D⌝ (independent of y beyond carrying s). The **script-level graph** is bipartite: script s → run tree dt iff s
validates for dt against at least one donor carrying s; with the screening of §1.12 (a wildcard pass that treats
every Run/RunNeg box as either value and assumes partner validation) as an upper bound and the exact AC as the
graph. Reported: the number of edges, the strongly connected components on establishers, the block structure by
script, the C-edge in-degree of every establisher, whether every on-graph pair cooperates under C from encounter 2,
and (named sub-catalogue) the hand predictions below.

**Hand predictions.** σCB → exactly the run trees whose first call is S_C or R_C with a C leaf on the T-branch
reached directly (CB's family, LöbC-shaped self-readers, and any tree with that first node whatever its F-branch);
σCB1 → the run trees S_C?(R_C?C:·):· and R_C?(S_C?C:·):· (CB1, CB1r); σCBP → S_C?(Y_D-type Run box ? C : ·):·; δ →
every tree whose first call's box is false against ⌜D⌝ and whose F-branch reaches D directly (very many: the D edges
are dense); ε (C) → the unconditional cooperators' trees whose run reaches C without a call. **No C edge between
distinct skeletons**, so the C-edge graph is a disjoint union of skeleton blocks plus the self-trusting readers that
accept a foreign skeleton through Hyp^self (LöbC accepts σCB).

### 1.12 Validation plan (before any counted cell)

1. PCORE (the tactic as code) equals the host Producer on every (catalogue program, opponent, outcome) of the
   single-pair catalogue and on a random sample of P units; its cost ≤ P + 4.
2. The mode marker changes no H list and no play (sample of spellings, whole plays).
3. The unit tables: composition against whole actual plays (sample of unit pairs including adopted units, twins and
   self-plays); TR_C and TR_S against direct encounters executed by the term (sample).
4. H-only units equal milestone 2's τ table (every τ pair, by the host).
5. Tests (`tests/test_lt_genes.py`): adoption after a passed check; refusal of a copied script against a different
   code; Lemma A's cases (F1 by the LöbC instance; a pre-play production-induced timeout after an accepted script, F0;
   a list mutation); the search producer within P (and its timeout below the cost); inheritance of lists; host-ancestry
   tracking; cost accounting (gate, production, AC, quote surgery); the transfer graph on a sample.
6. The scale guard: the size of the unit universe, the number of checks the tables need, and the time to compute
   them, before any population cell.

### 1.13 Revision before any counted cell: the scale guard and the population rule

*Written after the scale guard (notes §1.12 item 6) and before any counted cell; the predictions file has an
addendum of the same date.*

**Scale guard under the rules of §1.3 as written ("gate" rule).** The closure of §1.8 (host replay checker, 3
workers) grew the unit universe from 7,743 base units to 16,505 after round 0 (2,020 s; 3.7 M D checks for the
signatures, 1.3 M adoption checks, 2.5 M D checks, 33.3 M gate-row checks) and to 21,890 after round 1 (6,300 s;
92.4 M gate-row checks), with round 2 projected at ≥ 10⁸ further checks and the universe still growing. The growth is
the gate itself: an S or CS program collects a new script whenever its own check against a partner fails, and a C
program collects every script that validates against some donor, so inventories become sequences of several
scripts per outcome, and every S/CS unit with a C entry needs a full row of gate values against every reachable unit.
The run was stopped there (log kept as `runs/lt_genes/static_gate_semantics.log`).

**Population rule ("lack" rule), used in every population cell.** A program acts on an outcome only while its list
has no entry of that outcome: C tries the donor's entries of an outcome (in the donor's order, adopting the first that
passes AC) only if it holds no entry of that outcome; S produces a C script (PROD against the partner) only if it
holds no C entry, and a D script (against ⌜D⌝) only if it holds no D entry; CS copies, then searches, under the same
test. The S "gate" is therefore a list inspection, not a check. Consequences, by construction: every program holds at
most one C and one D entry (the shape of every H list, §0 disclosure), so the certificate is a gene with one allele
per outcome, acquired once and then inherited; production is paid at acquisition (and by C copiers on every encounter
in which they still lack an entry and try a donor's scripts), never as a per-match gate; F2 (first-valid order)
cannot arise in the populations. The single-pair tables are run under **both** rules (the gate rule exactly as §1.3
was written, and the lack rule), so the gate semantics is measured where it is cheap.

**Other corrections and conventions fixed here.**
- PROD's wrapper costs at most **P + 5** steps (lib-β, `fst`, `snd`, `capk`, at most P inner steps, return or
  timeout), not P + 4 as §1.3 said (the `snd arg` step); a timeout returns TO and adopts nothing (tests).
- **Cost model in the populations:** production steps per act are the median term costs measured on samples of the
  population tables (adoption check + quote surgery, tactic for a C script, tactic for a D script; `costs.json`);
  the per-match cost by mode and the price arm use these modelled costs. The single-pair tables use exact term costs.
- **Identity in the kernel:** a type keeps its spelling only for run trees with a split unit (twin play ≠ self play);
  otherwise two individuals of one unit and mode interact as twins (exact for plays, since twin play = self play
  there); the units whose S transition differs between self-play and twin play are counted in validation.
- **Encounter rate:** r = N/2 encounters per Moran event (25, 50, 100 at N = 50, 100, 200), about one match with
  every island resident per generation; r = 1 as the slow-transfer sensitivity.

### 1.14 Code validation of §1 (after the code, before any counted cell)

From `tests/test_lt_genes.py` (8 tests, all passing), `lt_genes_run.py validate` (`runs/lt_genes/validate.json`),
`graph` (`runs/lt_genes/graph.json`) and the static build (`runs/lt_genes/static.log`). No lottery cell and no
single-pair table had run.

- **The tactic as code equals the host tactic.** On the named catalogue (10 programs × {against CB-H for C, against
  ⌜D⌝ for D} and the tests' cases) PCORE returns exactly the host Producer's script; costs: σCB 4,613 steps, δ 4,850,
  σCB1 8,169, σCBP 27,574 (one nested Run of the partner's D check), CBPr's script 46,847–59,035, ε 1,220. On the
  population tables, every one of the 23,840 signature representatives was produced by the term: **0 disagreements
  wherever the term finished**; **3,898 (16%) exceed the cap P = K/4** and return TO (1,862 of them where the host
  finds a script). They are the signatures whose tactic path meets a box whose check regresses (TO): a regressing
  nested check burns its whole cap V = P, so the executable producer times out where the ideal one does not. The
  populations use the executable outcome (no script, counted as a production timeout). Median production cost (term)
  13,743 steps for C scripts (q90 at the cap) and 9,058 for D scripts. *Signature codes were extended to three box
  values (F, T, TO) for this reason before the final static build.*
- **Plays by composition = whole actual plays:** 1,300 unit pairs (600 random reachable pairs, 400 with an acquired
  inventory, 150 twins, 150 self-plays) played whole by the term: 0 mismatches.
- **Transitions = direct encounters:** 750 encounters of S, C and CS units against random reachable units, executed by
  the term (`lt_genes.encounter`, lack rule): 749 agree with the kernel's tables. The one disagreement is a C
  production that fits its cap for the signature's representative opponent but exceeds it for this opponent (the box
  check costs nearly V for it); cap timeouts are assigned per signature, an approximation measured here at 1/750.
- **Executable = ideal checks:** 492 sampled adoption and gate-type checks where the ideal table has the value: 0
  mismatches.
- **Mode markers change no H list:** 300 random spellings produced with the S marker: lists identical to milestone 2's.
- **Identity:** 97 reachable units are split (twin play ≠ self play; 48 run trees); a further 790 units on non-split
  run trees have an S transition that differs between self-play and twin play (e.g. the tactic at a self-play root,
  where R = S). The kernel therefore keeps the spelling in the type for **704 run trees** (every run tree with either
  property), so same-quote encounters are exact there; elsewhere twin and self behave identically.
- **Static build (lack rule):** base 7,743 units; the closure converges after 2 rounds at 15,532 units (11,379
  reachable in some mode; the rest are single-entry units used only by adoption checks), 29 scripts (25 host + 4
  produced only by S); 24.7 M host checks, 1,229 s on 3 workers; plus 239,488 checks for the Lemma A transfer
  statistic. Split units 97, PD (D production) undefined for 12 unreachable units only.
- **Kernel:** a synthetic universe checks the incremental payoff sums against direct sums after Moran events,
  adoptions and the inheritance-disabled rule; a 100-generation smoke run of the mixed and seeded C-only cells takes
  12–17 s (not a counted cell; discarded).
- **Cost model** (`costs.json`, term medians on samples): adoption check 17,626 steps (+56 for quote surgery), tactic
  for a C script 13,743, for a D script 9,058, a production cap timeout P + 5; the gate-rule check against a partner
  15,648, against a listless target 101.
- **The transfer graph** (exact, every run tree as recipient against every H list as donor): 681,834 C edges between
  distinct run trees (1,083 self edges) and 1,154,418 D edges; δ is accepted by 45% of run trees. Among the 345
  establisher run trees (mass 0.061) the C-edge graph has 22 components (largest 128 and 117 run trees), median C
  in-degree 28, 18 establishers with none. Of the establisher pairs that cooperate under (H, H) but not at the first
  (C, H) encounter, 1,554 are on the graph (18 do not cooperate at encounter 2) and 11,173 are off it (14 do
  cooperate at encounter 2, through an adopted D script read by a defection-detecting donor).

### 1.15 Revision after the first single-pair table, before any population cell: the adoption check reads the would-be self

*Written after the single-pair tables had run once with the adoption check of §1.3 (`runs/lt_genes/pairs_acsingle.json`,
kept as a result) and before any population cell had produced a result (the first lottery launch was stopped before
any run finished).*

**Finding (counted, single-pair table).** With AC on the single-entry quote x_s = (code, mode, [(a, s)]), a
PB-shaped copier can never adopt a PB-shaped donor's C script: CBP and CBPh in mode C against CBP-H or CBPh-H play
(D, D) in all five encounters and end holding only δ. The donor's partner validation of x_s runs the donor's σCBP on
the donor's run against x_s, whose second call asks "x_s defects against ⌜D⌝"; x_s carries no D script, so that box
is false and the validation fails, at every encounter, because the single-entry quote never contains the copier's own
δ even after it has adopted one. This is a fifth failure point of Lemma A's single-entry form, **F5: the checked
object lacks the carrier's other genes, which a prudent partner reads.** (F1 is the converse case: the other genes
falsify a box the check assumed.)

**Revision for every later table and every population cell.** AC checks the **would-be self**:
AC(x, s, a) := CHK(x', q_a, a) with x' = (code, mode, the current list with (a, s) appended). Then the adopted object
is exactly the checked object (A1 holds trivially at the adoption encounter; F1 and F5 cannot occur there), and the
statistic "adopted object certified against the donor" measures only what later appends in the same encounter (the D
entry after the C entry) do to it. Under the lack rule x' differs from x_s only by x's D entry when it copies a C
script. The wildcard screen (§1.11) still uses the single-entry unit (it ignores box values and partner validation,
so it is an upper bound for x' as well). The single-pair tables are rerun with the revised check; the first table is
reported beside them. Tests: `test_full_quote_check_lets_a_prudent_copier_adopt` (CBP copies CBPh's script from
encounter 2, (C, C) at encounter 3) and the LöbC instance, where the revised check refuses δ.

*Validation rerun under §1.15 (before any population cell):* static build 17,391 units (11,362 reachable), 29 scripts,
25.5 M host checks, 1,027 s; plays 1,300/1,300 and encounters **750/750** equal to the tables (the earlier single
disagreement was resolved by the TO-aware signatures); productions 23,840 representatives, 0 disagreements where the
term finishes, 3,898 cap timeouts; executable = ideal on 500 compared checks; adoption check median 19,443 steps.
