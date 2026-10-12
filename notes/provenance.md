# Provenance: who writes the first certificate, and against whom (notes, 2026-10-12)

Spec `specs/2026-10-12-provenance.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-12-provenance-gpt-6.1-sol.md`; the
[after review] text is the resolution). §1 is written before any code of this run and before any counted cell: the
rules exactly, the identity bookkeeping, the validity notion and the self-play-only audit, the hand scripts, the
self-encounter arithmetic, the ablation's redistribution rule, the cells, the paired streams and the primary contrasts.
§1.12 (code validation) is appended after the code and before any counted cell; §2 (costs) after that.

Base, imported unchanged: milestone 5 (`notes/certificates-as-genes.md` §1 with §1.13 and §1.15: the gene triple, the
post-play encounter, the lack rule, the would-be-self adoption check, Lemma A with F0–F5, the tactic as code
PROD/PCORE, the unit tables over 17,391 units, host-ancestry bits, the holder-based endpoint and E3); its cached static
tables (`runs/lt_genes/static/`, 25.5 M host checks, not recomputed); the identity run's stage statistics
(`runs/identity-tags.md` §3).

*Disclosure.* Before writing this section I ran four scratch counts on milestone 5's cached tables and catalogue (no
plays, no cell, nothing new computed by a checker): (i) the tactic's productions by signature code per run tree,
split into self-root codes (≥ 25) and non-self codes; (ii) the 21 reachable identity units of milestone 5 and their
run trees; (iii) an analogue of the prudent open core in milestone 5's grammar; (iv) milestone 5's per-run identity
islands by cell. They are quoted where used (§1.5, §1.6).

## 1. Design

### 1.0 What changes, in one paragraph

Milestone 5 let a searching program (mode S) write its C certificate against whichever partner it met first while it
still lacked one, and found that endogenous search mints identity cliques: a producer that meets an exact copy writes
a script valid only at the self-play root (R = S) and keeps it for life. Here the *provenance rule*, which partners a
program may write its first C certificate against and how it chooses among candidates, becomes a property of the
program (a cell-wide law, or a heritable trait in the mixed cell). Everything else is milestone 5: the grammar
(milestone 2's P at n = 7, 12,546 spellings, prior L), the post-play encounter, the lack rule, the would-be-self
adoption check, the kernel's Moran step, the lottery law and the endpoints. Three facts organize what follows.
(i) **Self-play-only is a property of a (run tree, script) pair, not of a script:** `EvR*; ChkR[EvR*; Ax · Hyp]` is
σCB for CB at every root, but for `if(CHK(them,them,C),C,D)` it closes only where ⌜them⌝ = ⌜me⌝, so the audit must be
run per run tree (§1.3). (ii) **At the seed, a producer's first partner is almost never its own copy** (0.86 such
events per run over all 6,400 founders, §1.5); minting happens later, inside lineages that grow on an island while
still lacking a certificate, so the rule that matters is the one that governs those late producers. (iii) **For one
class of run trees the self-play root is the only root at which the tactic can write any C script at all** (97 run
trees, mass 0.018 under L, about 114 seeded copies per run, e.g. `if(and(CHK(me,me,C),CHK(me,them,C)),C,D)`): no rule
that keeps a candidate written against a copy can avoid their cliques, and only a rule that refuses such a candidate
removes them (§1.4).

### 1.1 Identity bookkeeping

**The quote.** A program's published quote is the carrier term of milestone 5 with its code and its certificate list,
`λme. λthem. (λcerts. BODY) CERTS`, **without a mode marker**: the production mode (H, S, C, CS) and the provenance
rule are metadata, not source. The list stays in the quote because every check reads the target's certificates from
its quote (`getcerts`), so Theorem S^cert certifies exactly the quoted object; a certificate that was not in the quote
could not be checked. This is the one point where I read the spec's "the acquired inventory is metadata, not part of
the quoted behavioural source" as a statement about **structural eq on the behavioural source** (below), not about the
checker's quote: the certificate list is part of the checked object in milestones 4 and 5, and taking it out would
change the language (the spec says the language is unchanged).

- **Behavioural source and structural eq.** The behavioural source of a program is its spelling (the code: an
  enumerated term of the P grammar). "Source-distinct" (S-nonself, S-k, the mixed cell's stratification) means a
  different spelling. Two programs of the same spelling are the *same source* whatever their lists, modes and rules;
  two spellings with the same run tree (respellings, e.g. CB and `if(not(CHK(them,me,C)),D,C)`) are distinct
  sources. The rules' test reads only the spelling, never the list, mode, rule, cache or candidate state.
- **Same quote** (the checker's R = S coincidence, self-play): same spelling and same certificate list. Mode and rule
  never split a quote: an S-self and an S-nonself individual of one spelling holding the same list are one quote.
- **Twin:** same unit (run tree and list), distinct quotes (different spellings).
- **Metadata per individual:** rule (and its mode), host-ancestry bits per entry, and the rule's mutable state (S-k's
  candidate window, the gate cache, the producer's waiting log). None of it enters a quote or a check. Mutable state is
  not inherited (a newborn starts with an empty window, cache and log); the rule, the list and the ancestry bits are.
- **Kernel consequence.** Milestone 5 kept the spelling in an individual's type only for the 704 run trees where twin
  play or the S transition differed from self play, and kept the mode marker in the quote. Here the type is (unit,
  rule, spelling, ancestry) for **every** individual, and two individuals are the same quote iff (unit, spelling)
  agree. On the other 3,458 run trees twin and self values agree in every table (milestone 5 §1.14), so tracking the
  spelling there changes no play and no transition; it is needed only for the rules' source test.
- **Equality classes** reported per cell: distinct spellings present, distinct quotes present, quotes per spelling,
  and (mixed cell) the rule composition inside each equality class. The *initial equality class* of an individual is
  its spelling (every founder of a cell starts with the cell's founding list, so founders of one spelling are one
  quote at generation 0).
- **Consequences for the references.** H-only: no change (one mode). C-donor: the H donor and a C copier of the same
  spelling that has adopted the donor's whole list are now one quote (milestone 5 kept them distinct by the marker);
  the adoption check of a copier whose would-be self equals the donor's quote is therefore a self-play check
  (UVt self value), which the kernel now applies exactly (milestone 5's kernel used the twin value there). The cell is
  otherwise milestone 5's single-donor cell, rerun on these seeds.

### 1.2 The provenance rules

Common to every producing rule (S-type): the encounter is milestone 5's (play at fuel K = 10⁶, then production in the
residual; V = P = K/4); the lack rule (act on an outcome only while the list has no entry of it); **the D script is
produced exactly as in milestone 5** (PROD(x, ⌜D⌝, D) at every encounter while the list has no D entry, whatever the
partner), so the rules differ only in the provenance of the C script. "Produce against y" means PROD(x, y, C) after the
play of the encounter with y, the tactic's script by signature (milestone 5 §1.8), appended if it is a script; a cap
timeout or `none` appends nothing. Founders of every S-type cell start with empty lists.

- **S-self** (milestone 5's S): at every encounter while lacking a C entry, produce against the partner, whoever it is
  (a same-quote partner gives the self-root signature, code ≥ 25).
- **S-nonself:** at every encounter while lacking a C entry, produce against the partner **iff the partner's spelling
  differs from one's own**; otherwise skip the C step (the D step runs). A same-spelling partner with a different list
  (a twin of one's own source) is skipped too. Searching continues until a production succeeds.
- **S-self-delayed** (the timing control): at every encounter while lacking a C entry, draw a **shadow partner**
  uniformly among the other N − 1 residents of the island (an event-indexed draw independent of the actual partner);
  produce against the **actual** partner, whoever it is, self included, iff the shadow's spelling differs from one's
  own. The production *times* are distributed exactly as S-nonself's under the same island composition (an attempt
  happens with probability equal to the fraction of non-self residents, encounter by encounter), while the partner
  written against is unconstrained. So S-self-delayed − S-self isolates timing and opportunity, S-nonself −
  S-self-delayed isolates who the script is written against.
- **S-k, k ∈ {2, 3}** (the coverage rule): while lacking a C entry the producer keeps a **window**: the source-distinct
  partners met since the window opened (at most one of them can share the producer's spelling) and the candidates
  written against them. At an encounter whose partner's spelling is not yet in the window, the partner is added and a
  candidate is produced against it (a cap timeout or `none` adds the partner without a candidate); a partner whose
  spelling is already in the window adds nothing. The window **closes** when it holds k partners, or after 50
  encounters since it opened (logged "k not reached"). At closing each candidate gets a **score**: the number of the
  window's partners against which it is valid in the own-side sense of §1.3 (a candidate is always valid against the
  partner it was written against, so every candidate scores ≥ 1 and none is inadmissible under own-side validity).
  *Selection:* keep the earliest candidate with score ≥ 2 (the safeguard: validates against two distinct sources); if
  none scores ≥ 2, the spec's tie-break applies: keep the earliest candidate (score 1), and log "safeguard not met".
  If the window has no candidate, it is cleared and a new one opens. After a window closed by the 50-encounter
  deadline, the next window again needs k partners. The cost charged: one production per candidate plus one
  own-side validation per (candidate, other partner) pair at the adoption-check cost (§1.8).
  *Reading stated.* The spec says "keep the candidate that validates against at least two source-distinct partners,
  ties broken by the earliest candidate" and the RE's revised prediction 3 has S-2 "tie systematically" and keep a
  candidate by the tie-break; I read the tie-break as covering the case in which no candidate reaches two (the
  fallback above). The **strict** reading (the safeguard as a requirement: a window whose best candidate scores 1 is
  cleared without keeping anything) is run as one labelled extra cell, **S-3 strict**, because the two readings
  disagree exactly on the run trees of §1.0 (iii).
- **S-gate+cache** (milestone 5 §1.3 as written, with a negative cache): after the play, the **gate** g = CHK(x, y, C)
  (one's own full check against the partner, at the self root if the partner is one's own quote); if g ≠ T, produce
  against y and append the script if it is not already held (so a C block can hold several scripts, first valid
  decides); the D step as above. The **cache contract**:
  - *Key:* every input the gate and the production read: the partner's quote (spelling and list), one's own list
    state (one's unit), and the budgets (K, V, P; constant within a cell, so they are part of the key but never
    distinguish two entries).
  - *Value:* `rejected` (gate F and the production added nothing: `none` or a script already held) or `timeout` (gate
    TO, or a production cap timeout). The two are stored and counted separately.
  - *Invalidation:* any change of one's own list clears the cache (the key's own-list component changes).
  - *Use:* at an encounter whose key is cached, neither the gate nor the production runs.
  - *Charging:* a lookup costs 1 + e steps, e the number of entries scanned (a linear list, one unit-cost quote `eq`
    per entry); a store costs 3 steps; a miss pays the lookup, then the gate and the production in full; memory is
    reported as entries held. Repeated misses on distinct keys are paid in full each time.
  - *Lemma C (the cache changes costs, not dynamics).* The gate, the tactic and the cap are deterministic functions of
    (own quote, partner quote, budgets). So a cached negative is exactly what recomputation would return: a hit skips
    a computation whose result would leave the list unchanged. Hence the cached and uncached gate rules have the same
    transitions encounter by encounter, and the cell's dynamics are the gate rule's; the cache changes only the
    charged steps. (Soundness is untouched in any case: Lemma A0.)
  - Not inherited, capacity 64 entries per individual (an overflow is a miss without a store, counted).
- **CS-nonself:** milestone 5's C step (copy-and-check of the partner's published entries, would-be-self check,
  unrestricted by source), then the S-nonself step on the updated list.
- **C-donor** (reference): one H donor per island (an establisher spelling with a C script, drawn from the prior
  restricted to such spellings; its offspring are H), every other founder in mode C with an empty list; milestone 5's
  single-donor cell.
- **H-only** (reference): every founder in mode H with its frozen host list (milestone 2's L×P ecology).

**What each rule can write at a self-play root** (by construction): S-self, S-self-delayed and S-gate+cache can
produce against a same-quote partner; S-k can (at most one per window) and keeps such a candidate when it is the
earliest with the top score; S-3 strict keeps it only if it is valid against a second source; S-nonself and the S step
of CS-nonself never produce at a self-play root (the partner's spelling is their own there). H never meets itself
(fixed probes). A self-play-only script can still **enter** a list by copying (§1.3).

### 1.3 Validity, self-play-only scripts, and the audit

**Two validity notions.** For a program x lacking a C entry, a candidate script s and a partner y, let x' = x with s
appended (the would-be self, milestone 5 §1.15).
- *Full validity:* CHK(x', y, C) = T: the derivation s at the root ⟨x' ⌜x'⌝ ⌜y⌝⟩⇓C closes **and**, if it uses the
  S hypothesis, the partner validation of y's own C certificate at (y, x', C) succeeds.
- *Own-side validity* OSV(x', y): the derivation s closes at that root with the S hypothesis accepted (milestone 4's
  `vone` with the real check values of every Run/RunNeg box, without the partner validation). Own-side validity is
  a function of the run tree, the script and the root's **signature** (milestone 5 §1.8: which atoms are R or S and the
  F/T/TO values of the others), so it is tabulated as OSV[τ, s, code] over the signature codes that occur in the unit
  universe, from one representative pair per code (validated on sampled other pairs, §1.12).

**Lemma V (full validity cannot bootstrap a window).** At founding every list is empty. A candidate that uses the S
hypothesis (every reader of its partner: σCB, σCB1, σCBP, …) is fully valid against y only if y holds a C script
valid at (y, x', C); an empty y holds none. So under full validity every reading candidate scores 0 against every
empty partner except an exact copy that would carry the same candidate, which an empty copy does not: in an
all-empty population no reading candidate is admissible and S-k never acquires. *Proof:* the check's partner
validation reads y's C block (`getcerts`), which is empty. ∎ So the spec's safeguard is read with own-side validity:
it asks whether the producer's own derivation closes at a second source's root, which is exactly the property a
self-play-only script lacks, and it does not ask the partner to have certified itself first. (Full validity is used
everywhere else: plays, adoption checks, the gate.)

**Self-play-only, by validity.** A (run tree τ, C script s) pair is **self-play-only (SPO)** iff s is own-side valid
at some self-root signature of τ (code ≥ 25) and at **no** distinct-quote signature of τ (code < 25) occurring
anywhere in the unit universe (every reachable partner unit, twins of one's own unit included). Examples by hand:
- σCB on CB's run tree: valid at code 15 (S atom) and 35 (self): **not SPO**.
- σCB on `if(CHK(them,them,C),C,D)`: its box ⊡(them, them, C) is R only when ⌜them⌝ = ⌜me⌝; at distinct roots the
  tactic writes `EvR*; ChkR[EvR*; Ax · Run]` instead, and σCB's Hyp fails: **SPO for this run tree**.
- `EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Ax] · Hyp]` (written by the tactic at the self root of CB1, CB1r,
  `if(and(CHK(me,them,C),CHK(them,me,C)),C,D)` and `if(and(CHK(me,me,C),CHK(me,them,C)),C,D)`): its inner Ax closes
  the second call because the second box equals the first, which holds only when R = S: **SPO** on every such tree.
- The TwinD family (`if(or(CHK(me,me,D),CHK(me,them,D)),D,C)` and three relatives): its non-self C script
  `EvR*; ChkR[RunNeg · EvR*@1; ChkR[RunNeg · EvR*@1; Ax]]` is own-side valid at distinct roots: **not SPO**, yet the
  unit holding it is an identity clique (milestone 5's identity units 12603, 12997, 13497, 13499). Identity cliques and
  SPO scripts are different things: the TwinD family is an identity clique by its run's self-reading, written against
  non-self partners.

**How an SPO script can enter a list:** (a) production at a self-play root (S-self, S-self-delayed, S-k under the
fallback, S-gate); (b) copying, when the copier's would-be self *is* the donor's quote (same spelling, same resulting
list), since the adoption check is then a self-play check; under the lack rule this needs a same-spelling donor with
the same D block; (c) inheritance of a list that contains one. **Claim N (S-nonself never writes an SPO script):** an
S-nonself production happens only against a partner of another spelling, i.e. at a distinct-quote root, and the
tactic's output is own-side valid at the root it was written at; an SPO script is valid at no distinct-quote root.
So S-nonself never writes one; in a cell where every individual is S-nonself (no copying) no individual ever holds
one. ∎ (CS-nonself can still acquire one by route (b) from a same-spelling relative that holds one; this happens
only in the mixed cell.)

**The audit.** (1) *Static, over the full supported carrier set:* OSV for every (τ, s) with s a C script held by some
unit of τ in the 17,391-unit universe (this includes every script that can enter by copying, since the universe is
closed under C and CS) or produced by the tactic for τ at any code; list the SPO pairs, their trees and prior mass;
for each rule, the set of SPO pairs it can write (the codes it can reach). (2) *Dynamic:* in every cell, the fraction
of held C-script instances that are SPO at each checkpoint, split by route (produced, copied, inherited), and the
number of SPO acquisition events by route. (3) *Claim N by code:* every S-nonself production in every S-nonself
cell is checked against the SPO table (0 expected).

### 1.4 Hand scripts: each rule, named carriers, each first-partner type

From milestone 5's production table (scratch count (i)); script names as in milestone 5 §1.9 (σCB = `EvR*; ChkR[EvR*;
Ax · Hyp]`, σCB1 = `EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Hyp] · Hyp]`, σCBP = `EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Run] ·
Hyp]`, σCBPr = `EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Hyp] · Run]`, ι = `EvR*; ChkR[EvR*; ChkR[EvR*; Ax · Ax] · Hyp]` (the
identity script), τ₁ = `EvR*; ChkR[RunNeg · EvR*@1; ChkR[RunNeg · EvR*@1; Ax]]` (TwinD's non-self C script),
τ₀ = `EvR*; ChkR[RunNeg · EvR*@1; ChkR[Ax · EvR*; Ax]]` (TwinD's self-root C script)). Named carriers: CB =
`if(CHK(them,me,C),C,D)`; CB1 = `if(CHK(them,me,C),if(CHK(me,them,C),C,D),D)`; CBP₄ =
`if(CHK(them,me,C),if(CHK(them,^D,D),C,D),D)`; CBPr = `if(CHK(them,^D,D),if(CHK(them,me,C),C,D),D)`; the
identity-prone spellings of this grammar (it has no `eq` atom; the R = S coincidence is its identity channel): AND2 =
`if(and(CHK(me,them,C),CHK(them,me,C)),C,D)` (CB1r's run tree), MM = `if(and(CHK(me,me,C),CHK(me,them,C)),C,D)`,
TwinD. First-partner types at founding (every list empty): *self* (same spelling: the self root, code ≥ 25); *twin
spelling* (another spelling of the same run tree, e.g. CB against `if(not(CHK(them,me,C)),D,C)`: a distinct quote,
the same signature as a distinct partner); *distinct carrier* (another establisher); *C* (`C`); *D* (`D`). At founding
no partner holds δ yet, so the ⌜D⌝-box of CBP₄/CBPr is F against every first partner except one that has already
produced its D script.

| carrier | self | twin spelling / distinct carrier | C | D |
|---|---|---|---|---|
| CB | σCB (not SPO) | σCB | σCB | σCB |
| CB1, AND2 (CB1r tree) | **ι (SPO)** | σCB1 | σCB1 | σCB1 |
| MM | **ι (SPO)** | none (no script at any distinct root) | none | none |
| CBP₄ / CBPr | none at encounter 1 (own ⌜D⌝ box F); σCBP / σCBPr once both carry δ | none until the partner carries δ, then σCBP / σCBPr | none (C cooperates with ⌜D⌝) | none until D carries ε_D, then σCBP / σCBPr |
| TwinD | τ₀ (self root) | τ₁ (not SPO; the unit is an identity clique) | τ₁ | τ₁ |

**Per rule, at the first encounter with that partner type:**
- *S-self:* the table's entry for the partner met. Only CB1/AND2 against a copy and MM against a copy write an SPO
  script among the named ones.
- *S-nonself:* the table's entry for every non-self column; against self, nothing (the D step runs). MM never
  acquires a C script under S-nonself (it is a certificate-less defector for life); CB1/AND2 always end with σCB1.
- *S-self-delayed:* the table's entry for the actual partner, at a shadow-matched encounter.
- *S-k:* candidates per the table; scores by own-side validity: σCB is valid at self and distinct roots (scores k);
  σCB1 is valid at the self root too (Hyp closes both calls when R = S), so in a window {copy, distinct} CB1 keeps σCB1
  (score 2) over ι (score 1) **whichever came first**; MM's window holds at most one candidate, ι from the copy
  (score 1): kept under the fallback, refused under S-3 strict. CBP₄/CBPr: candidates appear only from partners
  holding δ; σCBP is not own-side valid against a partner whose ⌜D⌝ box is F, so a window mixing δ-holders and
  δ-less partners gives σCBP a score equal to the number of δ-holders in it.
- *S-gate+cache:* as S-self at the first encounter; afterwards the gate re-checks against every partner: CB1 holding ι
  meets a distinct partner, its gate fails (ι is invalid at distinct roots), it produces σCB1 and appends it
  ([ι, σCB1]: open from then on, first valid decides); MM holding ι meets a distinct partner, its gate fails and its
  production returns none: MM stays an identity clique, and the negative is cached. A CB holding σCB meets an empty
  partner: the gate fails at partner validation, production returns σCB (already held): a cached `rejected`.
- *C-donor:* milestone 5 §1.9 (copying along the skeleton graph from the island's H donor).

**Which rules can write an SPO script at all:** S-self, S-self-delayed, S-k (fallback), S-gate; not S-nonself, not
S-3 strict *as a kept script* (it can produce one as a candidate and discard it), not H. CS-nonself and C can acquire
one only by same-quote copying (§1.3 (b)).

### 1.5 Self-encounter arithmetic

**At founding** (scratch count, prior L over 12,546 spellings, founders iid): a founder of spelling σ meets an exact
copy as its first partner with probability E[(n_σ − 1)/(N − 1)] = μ_σ. Per island the expected number of
self-first-partner founders is N Σ_σ μ_σ² = 0.0135, per run (64 islands) **0.86**. Restricted to the spellings whose
self-root script differs from every non-self one: 0.059 per run for trees that also produce at distinct roots (405
trees, mass 0.099, about 632 seeded copies per run) and **0.011 per run** for the trees that produce only at self roots
(97 trees, mass 0.018, about **114 seeded copies per run**, 228 spellings). Islands seeded with ≥ 2 copies of one
only-self spelling: 0.55 per run. So the founding encounter cannot be what mints the identity islands milestone 5
measured (0.226 of 64 islands, about 14 per run).

**During the scramble.** Every producer first meets a partner within about 0.01 generation (≈ 100 encounters per
individual per generation), and a run tree with a non-self production then holds its general script for life; its
lineage is open. A run tree whose only C script is the self-root one (MM's class) cannot acquire one until two copies
of one spelling meet; until then it is a certificate-less program, most of which defect (its checks fail), and a
defecting lineage grows early by exploiting the seed's unconditional cooperators (0.35 of the prior). Once it has two
copies on an island, each copy meets the other with probability about 1/99 per encounter, so within a generation
(≈ 100 encounters) the lineage writes ι with probability ≈ 0.63 and becomes a self-cooperating identity clique.
Hand estimate: the minted cliques of milestone 5 come almost entirely from this class (scratch count (iv): MM holding
ι is the most frequent identity holder in milestone 5's S and CS cells), not from first encounters of the
CB1/AND2 class. The chance that a producer's partner is its own copy is the lineage's island frequency **at the time
it produces**, not the seed frequency μ_σ.

**Consequence for the rules (hand):** S-nonself refuses exactly that partner; S-self-delayed meets it at a
shadow-matched time and writes ι anyway; S-k under the fallback keeps ι (the only candidate it can ever have); S-3
strict refuses it; S-gate writes it and cannot repair it (no non-self production exists). The TwinD family (4 run
trees, mass 7.1·10⁻⁴, **≈ 4.6 seeded copies per run**) is an identity clique under every producing rule, S-nonself
included, and under H; in milestone 5's H-only cell it was the only source of identity islands, present in 12 of 40
runs (scratch count (iv)), and 11 of the 14 non-universal H-only runs had an identity island.

### 1.6 The mass-matched ablation

**Clique set Q (frozen rule, computed by code before any cell):** the spellings whose run tree has an identity unit
reachable under S-nonself, where *reachable under S-nonself* = the closure of the empty units under the S-nonself
transitions (non-self codes only, plus the D step) against every unit of milestone 5's universe, and *identity unit*
= milestone 5's definition (self-cooperating, mutually cooperating with no other reachable unit of that closure, twin
play D). By hand Q contains the TwinD family; the code reports Q exactly.

**Receiving set R:** the **open prudent core** of RESULTS "Prudent openness", transposed to this grammar (that run's
core is a set of classes of the identity grammar, which has `eq`, tags and ⌜CB⌝ quotes; P has none of them, so the
same defining properties are applied here): run trees whose H unit is an establisher (self-cooperates, defects
against D-H), open (mutual cooperation with CB-H) and prudent (defects against the certificate-carrying unconditional
cooperator C-H). Scratch count (iii): 11 run trees, mass 0.0024, e.g. `if(and(CHK(them,me,C),CHK(them,^D,D)),C,D)`
and `if(CHK(them,me,C),if(CHK(them,^C,C),D,C),D)`.

**Redistribution:** the ablated prior is μ' = μ on spellings outside Q ∪ R, 0 on Q, and μ_r (1 + μ(Q)/μ(R)) on each
spelling r ∈ R (the clique mass moved onto R in proportion to R's own mass). Nothing else is renormalized. **Paired
seeding:** founders are drawn from μ with the same stream as every other cell; a founder whose spelling lies in Q is
replaced by a draw from R ∝ μ (a separate stream). This draws exactly from μ' and leaves every non-Q founder
identical to S-nonself's replicate. The ablation runs under S-nonself.

### 1.7 Cells, streams, endpoints and contrasts

**Main cells** at (N, I) = (100, 64), mN = 1, w = 0.3, r = N/2 = 50 encounters per Moran event, horizon 2,000
generations, checkpoints every 10, 40 runs each, prior L: S-self, S-nonself, S-self-delayed, S-2, S-3, S-3 strict
(extra), S-gate+cache, CS-nonself, the mixed-provenance cell (rule iid ¼ each over {S-self, S-nonself, S-2,
CS-nonself}, heritable, every founder empty), C-donor, H-only, and the ablation (S-nonself, μ'). **Size panel:**
S-self, S-nonself and C-donor at (200, 64) (r = 100) and (100, 128) (r = 50), 20 runs each, labelled finite-size;
runs unresolved at 2,000 (not universal, or E3 censored) are continued to 10,000 generations as the budget allows,
and every size number is reported at 2,000 with the censoring stated.

**Paired seeds and event-indexed streams.** Replicate r of every cell at one (N, I) has the same founder spellings
(numpy stream [N, I, r, 20261012]), the same donor placements (C-donor), the same rule draws (mixed) and the same
replacement draws (ablation, separate streams). Every random number of the dynamics is a counter-based function of
(replicate seed, Moran event index, draw index) (splitmix64): event e uses draws 0–4 for the birth–death step (island,
migration coin, source island, parent, victim) and draws 8 + 4q + {0, 1, 2, 3} for encounter q (island, focal,
partner, shadow). So two cells consume identical numbers at identical events whatever their states; they diverge only
where their states differ (e.g. a parent chosen by the same uniform from different fitness profiles).

**Endpoints** (milestone 5's, on quotes): island P(C,C); *held* island = its majority quote self-cooperates and island
P(C,C) ≥ 0.5; *universal* = every island held and every pair of holders mutually cooperating; *universal-open* =
universal with every holder mutually cooperating with CB-H; *patchwork*; *unheld*; *identity island* = a held island
whose holder unit is an identity unit (milestone 5's definition over the universe); cross-island P(C,C); E3 (the
polymorphic closure test) with indeterminate (polymorphic) islands censored. **Island-level efficiency** (E3 success,
mean island P(C,C)) is reported separately from **global universality** (universal-open).

**Primary contrasts (predeclared):** (a) S-nonself vs S-self; (b) S-nonself vs S-self-delayed; (c) S-nonself vs
C-donor; each on universal-open (paired: discordant counts and the exact McNemar p, the mean paired difference with
a bootstrap 95% interval) and on identity islands (mean paired difference of the per-run fraction, bootstrap 95%
interval), beside the marginal Wilson intervals. Everything else is secondary.

**Statistics per run:** establishment (first checkpoint with an island at P(C,C) ≥ 0.9) with censoring; E3; the
endpoints above at 10, 50, 200, 1,000, 2,000; held-script SPO fractions by route; host ancestry (search / host bits as
milestone 5); rule composition of all individuals and of cooperative individuals on held islands (mixed cell:
stratified by holder run tree and by initial equality class); equality classes; production attempts, successes, cap
timeouts, gate hits/misses, cache size, S-k window outcomes (closed by k / by deadline; safeguard met or not;
cleared), per rule; per-producer waiting and acquisition logs (§1.8). **Stage statistics** as the identity run's, for
three groups (identity units; SPO-holding units; the open carriers, i.e. units mutual with CB-H): *arrival* (seeded
copies of the group's spellings and SPO acquisition events per run), *establishment* (runs and islands in which the
group ever held an island), *persistence* (held at the horizon), *spread* (islands held at the horizon per arrival,
pooled).

### 1.8 Costs, waiting and acquisition logs

Steps are modelled from milestone 5's term medians (`runs/lt_genes/costs.json`): a C production 13,743, a D production
9,058, a cap timeout P + 5, an adoption check 19,443 + 56, a gate check against a partner 15,815 (101 when the list
has no C entry); per rule: S-k adds one own-side validation per (candidate, other window partner) at the adoption-check
cost and stores the window's partner quotes (2 steps per stored quote); the cache charges as in §1.2. Steps never
change a play (post-play production; no price arm in this run).

**Producer log** (a *producer* = an individual of a producing rule that lacks a C entry at birth or at founding):
encounters until its first C-production attempt (the *wait*; 0 for S-self), encounters and modelled steps until it
first holds a C entry (*acquisition*), or censoring by death or by the horizon; whether its island was near-monoclonal
in its spelling at its first encounter (its spelling's frequency among the other residents ≥ 0.9). Histograms per rule
(exact counts at the predeclared thresholds 20 encounters and "never by the horizon"), split by capability: *capable*
producers (run trees with some non-self production) and the rest. Per-match and per-acquisition modelled steps per
rule; production cap timeouts per rule; the fraction of signature codes a rule reaches that time out at P = K/4
(static, from milestone 5's executable producer).

### 1.9 The gate cell's tables and its budget

The gate rule grows C blocks, which milestone 5's lack-rule universe does not contain. In an S-only population from
empty founders the gate can only append scripts the tactic writes for the program's own run tree (1–4 per tree; 780
trees have 2, 203 have 3, 25 have 4), so the gate universe is the closure, from the empty units, of the S-gate
transitions alone (no copying), seeded with milestone 5's cached check tables so that only the missing entries
(gate rows of multi-entry units, their columns, their signatures and productions) are computed. **Budget (declared
now):** the static closure must converge within 6 hours of wall time on ≤ 3 workers and the 40 runs within 12 hours;
the program-level feasibility is reported separately (per-match steps with and without the cache, against K). The
cell is run last. If the closure does not converge in budget, the cell is reported as infeasible with the closure's
growth and projected cost, and RE 6's falsifier fires.

### 1.10 What is not done

No frozen-inventory chain (the spec drops it); no price arm; no rerun of milestone 5's static tables, single-pair
tables or transfer graph.

### 1.11 Validation plan (code, before any counted cell)

1. OSV: every tactic output is own-side valid at the signature it was written at; OSV by representative equals OSV
   on sampled other pairs with the same (τ, code); the hand SPO classifications of §1.3 by code.
2. Each rule on the named carriers against each first-partner type by whole runs of the term (milestone 5's
   `encounter` with the rule's partner filter): the scripts of §1.4; S-nonself never writes an SPO script (Claim N)
   over the named catalogue; S-k's selection and tie-break on constructed windows; S-3 strict; the cache contract
   (a hit equals recomputation; invalidation on a list change; rejection vs timeout recorded separately); S-self-
   delayed's attempt probability against the non-self fraction; identity bookkeeping (assigning rules never changes
   an equality class; same spelling and same list = one quote in the kernel).
3. Kernel transitions against Python mirrors on sampled encounters per rule; the event-indexed streams (two cells with
   identical rules reproduce identically; a state change in one cell leaves the other's draws unchanged).
4. The ablation's masses (μ'(Q) = 0, μ'(R) = μ(R) + μ(Q), the rest unchanged) and its paired seeding.
5. The scale guard: per-run time of a 100-generation smoke run per rule (discarded), the gate closure's size.

### 1.12 Validation by code (after the code, before any counted cell)

From `src/provenance_run.py` `static`, `osv`, `sets`, `pairs`, `validate` (`runs/provenance/{static_ext,osv,sets,
validate}.json`, `pairs.json`) and `tests/test_provenance.py` (10 tests, passing). No counted cell had run; two
100–200-generation smoke runs and a profile run (replicates 997–999, discarded) were used for the scale guard.

- **Universe.** S-k can keep a candidate written while the list was empty after the D step has added δ; 3 such units
  were missing from milestone 5's lack-rule universe. Added and closed (0 rounds, 24,489 new host checks, 0 new
  production signatures): 17,394 units, 11,365 reachable, 29 scripts. Everything else reused.
- **Own-side validity.** 28,283 (τ, script, code) values. The signature reduction holds on 4,005 of 4,014 sampled
  other pairs (9 mismatches, 0.2%: the partner's boxes about the would-be self are not fully encoded by the
  signature of the program without the script). **Correction to §1.2:** the tactic's own output is *not* own-side
  valid at its would-be self in 468 of the 19,102 (τ, code) signatures (F1: the appended script flips a box that
  reads the program's own list, e.g. `if(CHK(them,^C,C),C,C)` at its self root). Such a candidate scores 0 against
  the partner it was written against and is inadmissible, as the spec says; the fallback keeps only admissible
  candidates (score ≥ 1). §1.2's sentence "every candidate scores ≥ 1" is wrong for these signatures.
- **SPO audit, static.** 484 SPO (τ, s) pairs on 480 run trees (mass 0.111; most are trees that end in C on both
  branches, where the script changes no play); **every one is written only at self-root codes, 0 at non-self codes**
  (Claim N over the full universe, including every script that enters by copying); 782 units hold only SPO C
  entries. Only-self trees 97 (mass 0.0178); capable trees (some non-self production or cap timeout) 3,284 (0.787).
- **The ablation's sets (frozen rule of §1.6).** The S-nonself closure has 10,953 units and 8 identity units, all of
  the TwinD family: **Q = 4 run trees, 10 spellings, μ(Q) = 7.13·10⁻⁴, 4.56 seeded copies per run** (the hand value).
  **R = 11 run trees, 33 spellings, μ(R) = 0.0024** (scratch count (iii) confirmed).
- **Hand scripts by whole runs** (`pairs.json`, 7 rules × 7 carriers × 5 first-partner types, 4 encounters; S-k with
  partner sequences first type → distinct → D → C): every entry of the §1.4 table holds (CB writes σCB against every
  partner; CB1 and AND2 write ι against a copy and σCB1 otherwise; MM writes ι against a copy and nothing elsewhere;
  CBP₄/CBPr write nothing at encounter 1 and σCBP/σCBPr from encounter 2 against δ-holders, never against C; TwinD
  writes τ₀ at the self root and τ₁ elsewhere; S-nonself writes nothing against itself). S-k: CB1's window {copy,
  distinct} scores ι 1 and σCB1 2 and keeps σCB1; MM's window has the single candidate ι (score 1), kept by the
  fallback, refused by S-3 strict; TwinD's candidates are valid against one partner only (score 1): the fallback
  keeps them, S-3 strict refuses them (TwinD then carries δ only, its H list, which is still an identity clique).
- **Kernel = term.** 728 sampled encounters (S-self, S-nonself, S-self-delayed with the shadow both ways, CS-nonself,
  C; distinct, twin and self partners) executed by the term give exactly the kernel's transitions (0 mismatches).
- **Settled encounters are skipped, exactly.** An encounter between two individuals that hold a C and a D entry under
  a lack rule (or H) changes nothing; the kernel skips them (and every encounter on an island with no unsettled
  resident) without consuming draws, since draws are event-indexed. Identical trajectories with and without the skip
  over 150 generations in 6 cells (S-self, S-3, mixed, C-donor, S-self-delayed, CS-nonself). Per-match costs use the
  expected side-encounters per rule as the denominator. Speed: 0.26 s per generation before establishment,
  ≈ 0.001 s after (at (100, 64)).
- **Deviations from §1.7, stated:** each encounter uses five draws (island, focal, partner, and one shadow per side,
  so both sides of an S-self-delayed pair have independent shadows); §1.7 said four.
- **Scale guard.** Types created per run ≈ 10⁴ (cap 150,000); a 2,000-generation run at (100, 64) ≈ 1 min. The gate
  cell's universe is built next (§1.9 budget).
- **Addendum (before any counted cell; the first launch of the main batch was stopped after 18 runs because islands
  holding *futile* programs could never be skipped, which made 10,000-generation extensions too slow; those 18 runs
  are kept aside as `lottery_main_aborted_v1.json` and not used).** The skip now also covers *futile* individuals:
  a non-copying lack rule that still lacks an entry its rule can never produce (no C script at any code the rule
  reaches, all codes for S-self/S-self-delayed/S-k, non-self codes for S-nonself; and no D script, deterministic in
  the unit), whose encounters change no type. Dynamics are unchanged (identical trajectories with and without the
  skip over 300 generations in 10 cells, `validate.json`; kernel = term 728/728 again). Their futile production
  attempts are no longer executed one by one: the expected number of side-encounters of futile individuals per rule
  is accumulated per event (`enc_futile`) and reported beside the executed costs; producer logs of futile
  individuals count encounters only on processed islands (a lower bound), while their "never acquired" status is
  exact. Producer statistics are reported for capable producers (run trees with a non-self production), whose logs
  are exact.
