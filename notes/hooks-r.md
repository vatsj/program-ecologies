# Hooks, Part R: a hook primitive with maximal fills in the realizable language (notes, 2026-10-18)

Spec `specs/2026-10-18-hooks.md` (reviewed by gpt-6.1-sol, then gemini-4-argon in amended mode; the two amendment
sections supersede the earlier text where they conflict, the later one winning). This file covers **Part R only**
(Part W is run separately). §1 is written by hand before any code of this run and before any counted cell. §2 (the
executed gate, validation, statics and projected costs) is appended after the code and before any counted cell.

Base, imported unchanged: milestone 4's checker K_T^cert (`src/lt_cert.py`), milestone 5's genes, tables and
universe (`src/lt_genes*.py`), the detectors run's Key rule and world K (`src/detectors.py`: hypothesis-closed D
scripts keyed to the bare source of their production partner, which is the literal ⌜D⌝), provenance's S-nonself
rule and kernel (`src/provenance.py`), the annealed kernel and world K's island run (`src/annealed*.py`,
`src/world_k.py`), the scaling classifier (`src/realizable_scaling*.py`) and the Pangaea fission–fusion merge
(`src/pangaea.py`); grammar P (n ≤ 7, 12,546 spellings, 4,162 run trees, prior L), w = 0.3, payoffs CC 0, CD −2,
DC 1, DD −1, K = 10⁶, V = K/4, r = 100 production encounters per Moran event. Every number here is an ε = 0 lottery
statistic at finite (N, I, horizon).

*Disclosure (before this section).* Before writing it I read the spec, CLAUDE.md, the RESULTS sections named in the
brief and the code; cloned the untracked cached tables read-only (copy-on-write) from the world-K worktree
(`runs/lt_genes/static/`, `runs/provenance/{static/, OSV.npy, SPO.npy, prod_exec.json, sets.npz}`,
`runs/detectors/K/{static/, sync/, OSV.npy, SPO.npy, prod_exec.json, sets.npz, grudge.npz}`, `runs/world_k/full/`);
and ran three throwaway scripts (`scratch/`, untracked): (i) counts and prior masses of the hooked grammar (§1.1);
(ii) the number of distinct spellings among 12,800 and 25,600 founder draws from it (§1.4); (iii) a host-replay
probe of a "baked" carrier whose body dispatches on the opponent's quote (§1.6), checked against FairBot and
PrudentBot H units in world K (it showed, among other things, that a program which switches to a call-free branch at
the ⌜D⌝ root is not certified to defect there by a script produced on its other branch, so PrudentBot defects
against it). No dynamics of any kind have been run.

## 1. Design

### 1.0 The object in one paragraph

The RS's paradigm (DEFERRED 12): base programs leave **hooks**, points where a gene decides the action; fills are
genes; maximalism about which hooks are expressible. In the realizable language a hook is a check call of the program
on itself at a **gene site**, and a **fill** is a keyed self-hypothesis certificate stored in the program's
certificate list: the hook plays ā₀ exactly when the checker accepts a fill claiming ā₀ there, so every fill is
self-fulfilling and sound, and the checker alone decides which fills apply (the Key rules of six scopes and one
conflict rule). Populations then run world K's ε = 0 island lottery with founders drawn from the extended grammar,
fills seeded from a declared gene prior, and four fill sources (seeding, history writes, copying, pair contracts),
with every hook kind and every source ablated by making its fills **inert** (held, inherited, capped, never applied)
so that supply does not shift.

### 1.1 The HOOK node and the hooked grammar H

- **Node.** `HOOK(t, a₀)` is an *action leaf* (one node, like `C` or `D`), t ∈ {1, 2} its tag, a₀ ∈ {C, D} its
  default. A program carries at most 2 tags. Tags are canonical: the first hook leaf in left-to-right order has tag
  1, and tag 2 may appear only after a tag-1 leaf; a later leaf may reuse tag 1 (both leaves are then one gene site
  with possibly different defaults). Grammar H = grammar P with the leaves `HOOK(1, C)`, `HOOK(1, D)`,
  `HOOK(2, C)`, `HOOK(2, D)` added to the action sort, n ≤ 7, node counting unchanged.
- **Counts (scratch (i)).** 99,588 spellings: P's 12,546 plus 87,042 hooked (one tag 54,018 + … by layer: n = 1: 2;
  n = 4: 192 + 64; n = 5: 192 + 64; n = 6: 6,336 + 2,112; n = 7: 47,296 + 30,784, one-tag + two-tag).
- **Prior.** Prior L over H: weight 2^−nodes per spelling, normalized over H. **Equal node cost:** a hook leaf is
  one node whatever its tag, default or future fills; a spelling's prior weight depends only on its node count.
  Mass shares under L: plain P programs 0.136, one-tag 0.549, two-tag 0.315; by number of hook leaves 0 / 1 / 2 / 3:
  0.136 / 0.306 / 0.414 / 0.144. Each one-node spelling (C, D, HOOK(1,C), HOOK(1,D)) has mass 5.6·10⁻⁴.
- **Resolution.** For a hooked spelling x and an assignment h of each tag to "unfilled", C or D, x[h] is x with
  every hook leaf of tag t replaced by h(t) (its own default where h(t) is unfilled). x[h] is a P spelling of the
  same node count (leaves are replaced by leaves), so it has a P run tree τ(x[h]) with at most two atoms.
- **The no-hook baseline** is grammar P itself (world K, S-nonself): the stored cell `wk_Snon_200_64` (K).
  The **inert-hooks control** uses grammar H, the same fill draws and storage, and never applies a fill: every
  hooked program plays x[defaults]. The shift baseline → inert is the **grammar-dilution effect** (amendment 2.5),
  reported separately; claims about hook semantics are judged against the inert control.

### 1.2 Compilation and the gene-site check

- A hooked program is a milestone-4 carrier `λme. λthem. (λcerts. BODY) CERTS`. A hook leaf compiles to
  `if CHKH(⟨V, me, them, ā₀, 4K + t⟩) then ā₀ else a₀`, a call of a **new library wrapper** CHKH with its own core
  (appended after every existing library entry; `iswrap` and `callcheck` are redefined in place to recognize it,
  exactly as the realizable SOG run extended them; every earlier index unchanged). The argument has milestone 4's
  shape with the fuel field carrying the tag (4K + t), so the gene-site box ⊡_H(x, m, ā₀, t) differs from every
  CHKS box: no top-level root R and no swap box S is ever a gene-site box.
- **The core (`hcore`)** reads the holder's quote t, the opponent quote m and the asked outcome a from the argument,
  extracts t's certificate list (milestone 4's `getcerts`), and scans the **fill entries** of tag t (entries whose
  script's top node is the new rule `Fill`, code 28). It selects the **winner** by the conflict rule (§1.3) among the
  fills whose Key side condition holds at (t, m), and returns T iff a winner exists, its outcome is a, and its premise
  validates (the premise is one `Hyp` node closing the gene-site box itself: milestone 4's Hyp^self, `chyp` with
  R = the gene-site box). Otherwise F. A call costs at most V + 6 steps, as every check.
- **A fill** (t, s, k, a) is the certificate list entry (a, Fill_{t,s,k}[Hyp]): tag, scope, key data and outcome.
  Fills live in the same list as production scripts but are never tried by CHKS (their top node is not a rule of
  milestone 4's table, so `cchk` returns 0 on them: inert to every existing check, by the same argument as the
  detectors run's Key clause); production scripts are never tried by CHKH (it reads only Fill entries).
- **Bare source excludes fills** (amendment 1.1): `bareof` strips the whole certificate list, so a program's source
  key is stable under writes; two programs with one spelling and different fills or certificates have one bare source
  and different quotes.
- **Production.** S-nonself's C step at a partner and D step at ⌜D⌝ are milestone 5's tactic (world K's reading).
  Gene-site boxes are never R or S, so the tactic never Hyp-closes a hook: it treats a hook call like any other check
  call of another box, Run if its value is T and RunNeg if not. **Production never fills a hook**; fills come only
  from the fill sources of §1.5. A production script certifies a path *through* a hook value, so it validates only
  where the hook still takes that value.
- **Re-checking after writes** (amendment 2.2) is automatic: no validity is cached across a change of the list; every
  check after a write replays the run and re-evaluates every hook call. A production C script written while a hook
  was C stops validating against the partners a later D fill covers (the gate shows it, §2).

### 1.3 The six scopes (Key rules), the self guard and the conflict rule

Key side conditions of a fill Fill_{t,s,k} at a gene-site root (holder t, opponent m):

| scope | rank | key domain | holds iff |
|---|---|---|---|
| source | 6 | the bare sources of the run's founder pool, and the token SELF (equal weight) | k = bareof(m), or k = SELF and bareof(m) = bareof(t) |
| root | 5 | {⌜C⌝, ⌜D⌝, self, other} | m is ⌜C⌝ / ⌜D⌝ / the holder's own quote (m = t) / anything else |
| behaviour | 4 | the 8 classes b = (b₁, b₂, b₃) | m ≠ t and b = ([CHKS(m, ⌜C⌝, C) = T], [CHKS(m, ⌜D⌝, C) = T], [CHKS(m, m, C) = T]) |
| history | 3 | bare sources (written by triggers; seeded from the founder pool) | k = bareof(m) |
| role | 2 | {the one role of the symmetric PD} | always |
| none | 1 | — | always |

- **Behaviour is certified play** against the fixed probe set (⌜C⌝, ⌜D⌝, the partner itself), read by the checker:
  the self probe is the partner's own self-check (the checker's self-hypothesis rule may close it). A non-carrier
  (⌜C⌝, ⌜D⌝) carries no certificates, so its class is 000. **The self guard** `m ≠ t` comes first: at the holder's
  own root the class would need the holder's self-check, which re-enters this very gene site (a regress that costs
  the whole cap); the guard makes a behaviour fill not apply there, at one comparison. This is amendment 2.2's
  "a probe that exhausts the fuel returns the default", made exact and free. Probes evaluate the probed program's
  hooks by its own fills (they are ordinary checks of its quote).
- **Root** is the root of the hook's own run: the root at which the gene site is evaluated, for every root the
  program meets (actual play, partners' checks of it, its own probe and self checks).
- **The conflict rule** (checker-level, one rule): among the tag-t fills whose keys hold, the winner has the highest
  rank; ties go to the most recent (the later list position). Ablation **recency only**: the most recent applicable
  fill wins, ranks ignored.
- **Soundness (by construction).** CHKH returns T only for a validated winner claiming the asked outcome; the leaf then
  plays exactly that outcome, so every accepted fill states a true fact about the gene site at that root, and the
  value is a deterministic function of (holder's list, opponent quote): every check and every run that reaches the
  call sees one value. Theorem S^cert's induction gains one case: Run/RunNeg on a gene-site box (clean value of a
  call that re-enters nothing but the opponent's own probe checks, which never involve the holder because of the self
  guard). A production script accepted at a CHKS root is therefore true of the actual run, hooks included.
- **Adversarial interacting fills (tested in the gate, §2):** overlapping keys with conflicting actions (none-D with
  source-C; behaviour-C with history-D; two none fills; SELF and an own-source key); a fill that falsifies another
  certificate (a D fill after a production C script on the hooked path); forged fills (a bare Hyp entry; a Fill with
  another tag; a Fill whose key holds nowhere; a fill on a program without that tag; a fill entry in a P program);
  behaviour fills at the self root; fills copied onto a program with the same and with another spelling.

### 1.4 Lemma H: resolution per root kind (the reduction the populations use)

The opponent of any root a pair's evaluation reaches is one of four kinds for each side: the partner, the program
itself (same quote), ⌜C⌝, ⌜D⌝ (grammar P's atoms name only me, them, ⌜C⌝, ⌜D⌝, and every nested root is an
atom's box). At a root of kind κ the gene sites of x take the values h_x(κ) given by the conflict winner; hence:

> **Lemma H.** For hooked quotes x and m, every check value and every play of the pair equals that of the *baked*
> pair x̂_m, m̂_x, where x̂_m is the carrier with x's certificate list whose body dispatches on the opponent's quote:
> `if them = ⌜C⌝ then B(τ_C) else if them = ⌜D⌝ then B(τ_D) else if them = me then B(τ_S) else B(τ_P)`, with
> τ_κ = τ(x[h_x(κ)]) and h_x(P) = h_x(m); production scripts correspond one to one (a hook call's Run/RunNeg node
> is absent from the baked script, whose EvR* absorbs the dispatch).

Proof sketch: the gene-site value at a root depends only on (x's fills, the root's opponent quote); every check and
run that reaches a hook call sees that value, and its Run/RunNeg node in a production script validates iff the
script's branch is the one the value selects; the dispatch reproduces the same branch at the same roots; the
dispatch has no call, so the baked script differs only by the absent hook nodes. On the ideal table no step is
charged, so costs do not enter. Two consequences used everywhere:

- **Uniform case.** If the τ_κ of every root kind a pair's evaluation *touches* are equal (and the fitted blocks
  equal), x behaves as the P unit (τ, fit(C block), fit(D block)) and every value is world K's table entry (Lemma T).
  The touched kinds are the fixpoint of the atom kinds of the trees at the touched roots: from x's partner root,
  (me,me) touches x's self root, (me,⌜q⌝) x's ⌜q⌝ root, (them,me) m's partner root, (them,them) m's self root,
  (them,⌜q⌝) m's ⌜q⌝ root; at x's self root every atom names x or a probe; at a probe root only x's own atoms
  (me,me), (me,⌜q⌝) touch anything. fit(·) drops scripts that cannot fit τ (milestone 5's wildcard screen SINGLE),
  which never validate on τ, preserving order.
- **Composite case.** Otherwise the values are computed by host replay (milestone 4's ideal host checker) on the
  baked terms, memoized by the pair of *composite profiles* (τ_P, τ_C, τ_D, τ_S, C block, D block) and the relation.
- **Validation (§2).** The Lemma is checked on a battery and on pairs sampled from actual runs: the true hooked
  carriers (CHKH and fills, host replay) against the baked pair and against the kernel's reduction; plays and every
  check value of the pair.

### 1.5 The evolving object (amendments 1.1, 2.1–2.6)

- **An individual** is (spelling, certificate blocks C and D as in world K's units, fill list, provenance rule
  S-nonself). At most 4 fills (FIFO beyond 4, evictions logged per encounter); each fill carries (tag, scope, key,
  action, source ∈ {seed, write, copy, contract}). Fills are inherited by offspring and never expire otherwise.
- **The gene prior (seeding; normalized):** a founder whose spelling has tags carries k fills, k ~ Poisson(1)
  conditioned on k ≤ 4 (P(k) = 0.368, 0.368, 0.184, 0.061, 0.015 / 0.9963, renormalized); each fill draws its tag
  uniformly from the spelling's tags, its scope uniformly from the six, its key uniformly from that scope's domain
  (source: the distinct bare sources of the run's founder pool plus SELF, equal weight; history: the distinct founder
  sources; behaviour: 8; root: 4; none and role: one), its action uniformly from {C, D}. Founders without tags carry
  none (their draws are still consumed, so fills are coupled across every cell). The draw is a function of the
  replicate and the founder's slot alone.
- **The fill encounters.** Of the r = 100 encounters of each Moran event, the first r_f = 10 are also fill encounters
  (each individual takes part in about 20 per generation); fill encounters are never skipped (production encounters
  keep world K's skip of settled pairs). Production first, then the fill operation on the pre-encounter quotes and
  plays. **At most one fill operation per program per encounter**, in the priority contract, history write, copy.
- **History writes (two-player triggers, amendment 1.1).** After an encounter in which x cooperated and its partner
  y defected, x writes a *grudge* (t, history, bareof(y), D); after mutual cooperation, a *thanks*
  (t, history, bareof(y), C). t is the tag of the hook leaf x's run reached in that encounter; if x's reached leaf is
  not a hook, nothing is written (no gene site was on the path). **S-nonself applies to writes** (the run's production
  convention, DEFERRED 1's operating hypothesis): no write when y has x's spelling. **No churn** (amendment 2.1): a
  write whose (tag, scope, key) is held updates that fill in place (action, and recency moved to the end) and evicts
  nothing; *deviation, declared now:* a write that would change neither the action nor anything else of a fill already
  in the last list position is a no-op, and an unchanged-action refresh does not move the fill (only FIFO order would
  change; this keeps types from churning by permutation). Grudge-only arm: thanks never written.
- **Copying (horizontal, "the existing skeleton rule").** With probability p_c = 0.05 per fill encounter and side, x
  draws one fill uniformly from y's list and adopts it if x has a gene site of that tag (the skeleton rule: the fill's
  script is Fill[Hyp] at a gene site of tag t, and it fits x iff x has tag t; milestone 5's would-be-self check is
  trivially passed by a self-hypothesis fill whose key holds, and inert where it does not). No copying from the same
  quote. SELF stays a token, so a copied SELF fill refers to the copier's own source. Adoption follows the write rule
  (update in place, else append with FIFO).
- **Pair contracts.** With probability p_k = 0.05 per fill encounter, if both reached leaves are hook leaves, the play
  was not (C, C) and the spellings differ, both write (t, source, partner's bare source, C) on their reached tag. Pair
  rule: both or neither; each fill is the other's certificate's mirror (the two gene-site checks evaluate the same
  predicate, keys swapped).
- **Three-player triggers** (amendment 2.4) belong to the SOG wing (§3).

### 1.6 Ablations, controls and coupling (amendments 1.3, 2.5, 2.6)

- **Coupling.** Founder spellings, fill draws, the kernel seed and every fill-operation draw (a separate counter
  stream) are identical across the hook cells of a replicate; only the inertness map changes.
- **Inert, not removed.** A disabled scope or source makes its fills inert (held, inherited, in the cap, logged,
  never applied by the conflict rule). Cells: each scope inert in turn (6); fill sources: **seeding only** (writes,
  copies and contracts inert; never dropped), writes inert, copies inert, contracts inert; inert-hooks control (all).
- **Renormalized comparison** for the identity-relevant ablation: the gene prior drawn over five scopes (source
  removed) — one cell.
- **History controls:** writes inert; **shuffled** (the key of each write is replaced by the bare source of a
  uniformly drawn resident of the island); **learned but not inherited** (a newborn receives the parent's fills minus
  those of source write); grudge-only.
- **Identity routes separated** (amendment 2.6): source scope inert; history scope inert; contracts inert; all three
  together.
- **Diagnostic, clone fills (S-self fills):** writes and contracts allowed against one's own spelling (production
  stays S-nonself). The clone route of the gemini-4-argon counter-prediction cannot fire under S-nonself fills; this
  cell gives it a chance. Labelled as a diagnostic.
- **Conflict-rule ablation:** recency only (first in the drop order).

### 1.7 Cells (PD), statistics, drop order

- **Machinery.** World K, S-nonself production, ε = 0, w = 0.3, r = 100, calibrated mN = (N/100)^0.7, world K's
  island run (annealed kernel with lineages, schedule zero), extended with hooked types (§1.5) in a new kernel.
- **(200, 64)**, 20 replicates per cell, paired founders: no-hook baseline (stored), inert, maximal to 10,000; every
  ablation and control to 2,000, scored against maximal's generation-2,000 snapshot (world K: no S-nonself run at
  N ≥ 200 changed status after 2,000 in the scaling run; the main cells' 2,000→10,000 changes are reported).
- **Fission–fusion** (128 islands of 100, merged at 200, to 2,000): baseline, inert, maximal.
- **(400, 64)** size check: baseline, inert, maximal to 2,000.
- **Statistics.** Universal-open and universal-on-target (world K's classifier with hooked holders' open/identity
  bits computed by the reduction), identity islands (held, self-cooperating, mutual with no panel unit and with no
  living type of another spelling; panel = FairBot-, PrudentBot-, CooperateBot-, DefectBot- and AP-H units), rival
  islands by class (hooked or plain holder; identity or not), island P(C,C) (reported, never selected on); per hook
  kind (scope) and per fill source: prior mass, held, applicable (key holds for some resident's root), selected (the
  winner at some resident's gene-site root), executed (the winner at the reached leaf of some resident pair), all
  weighted by counts; writes, evictions, copies, contracts; key coverage (founder sources present per island);
  founder establishment (holder descends from a local founder), holder changes, persistence beyond 2,000; modelled
  verification cost per encounter (gene-site checks per encounter × the gate's measured steps per check, by list
  length and scope; the ideal table charges none). Per cell: counts with Clopper–Pearson intervals; paired contrasts
  by McNemar (exact) on matched replicates; outcome regions predeclared in the predictions file.
- **Drop order** (spec, amended): the conflict-rule ablation, then fission–fusion, then (400, 64); the seeding-only
  control is never dropped.

### 1.8 Hand predictions (mine; the numbered ones go to the predictions file)

- The gate passes: conservative (existing checks identical), the gene-site value equals the resolution on the whole
  battery, 0 accepted false atoms, Lemma H exact on sampled pairs.
- **Seeded source and history keys are nearly inert.** About 11,800 of 12,800 founder spellings are distinct
  (scratch (ii)), so a seeded source key names a lineage with about one copy in the run, and SELF has weight 1/11,800
  inside the source scope: about 12,800 × 0.86 × 0.83 × 1/6 × 1/11,800 ≈ 0.13 seeded SELF fills per run, half of
  them C. **Seeded identity (RE 3) will not appear** (≤ 0.005 identity islands per island).
- **Identity needs a clone route**, and S-nonself fills close it: a D-default gene site reached against a clone gives
  (D, D), no thanks trigger, and contracts with one's own spelling are refused. In the clone-fills diagnostic, pair
  contracts between clones mint spelling cliques (`HOOK(1, D)`-like sites with C keyed to one's own source), so
  identity appears there (≥ 0.02 per island is my guess, uncertain).
- **Inert vs baseline:** the default-resolved prior favours trees with more leaves; I expect universal-open within
  ±0.2 of the baseline's 19/20, identity 0.
- **Maximal vs inert:** root and behaviour fills create partner-class-specific defection inside the network (e.g. D
  against class 001, FairBot's class), so some held islands are non-identity rivals; I expect universal-open to fall
  by 0.1–0.3, with identity islands still ≈ 0, and the scope ablations to locate the loss in root and behaviour.
  Islands stay efficient.
- **History** changes universal-open by less than 0.15 at 20 runs (the detectors run: grudges decided nothing at
  natural seeds); thanks are the most held kind at the horizon (they accumulate on hooked holders whenever two
  spellings of the network coexist).
- **Fission–fusion** stays universal-open ≥ 0.9 under maximal hooks.

### 1.9 Order of work

1. This section (commit). 2. Predictions file (commit). 3. Code: `src/hooks_r.py` (grammar H, compilation, the
   CHKH library extension and host replay, fills, Lemma H's baking, the static tables), `src/hooks_r_kern.py` (the
   island kernel with hooked types), `src/hooks_r_run.py` (gate, statics, validation, pilots, cells),
   `src/hooks_r_report.py`; `tests/test_hooks_r.py`; §2 (commit before any counted cell). 4. Cells, `runs/hooks-r.md`
   and `.json`. The SOG wing (§3) is designed, coded and validated after the PD cells are launched, with its own
   predictions addendum before its cells.

## 3. The social organization game wing (design summary; details appended before its code)

The same primitive on the realizable SOG (`src/sog_full*.py`, `src/per_root*.py` with R2 production, the ideal
table, (100, 64), 20 runs per cell): hook leaves in both roles (worker actions work/strike; boss actions the nine
pay/whack constants), fills as in §1.3 with role keys {boss, worker 1, worker 2}, behaviour keys the worker's certified
play against the two probe bosses and the boss's certified wage class, root keys the game's root classes (actual
encounter; each probe encounter), source and history keys bare sources (a boss's key holds if either worker carries
it, per slot), and amendment 2.4's three-player triggers (a worker grudges the boss when it works and receives zero
or is whacked, thanks when paid at least ¼ while working; a boss grudges a striking worker and thanks a worker who
works at a positive wage; one write per encounter per program). Statistics: fair-wage share, zero-wage share, threat
fills (worker fills with action strike, boss fills with a whack) held, applicable and executed on path, with the
number of challenges. If the factorized tables of the SOG run (Lemmas B and F₃, which assume probe-only bosses) cannot
carry source-keyed boss fills within the budget, the reduction used is stated before any SOG cell, and anything not
run is disclosed.

## 2. The executed gate, validation, statics, deviations and costs (appended after the code, before any counted cell)

Code: `src/hooks_r.py` (grammar H, fills and the conflict rule, the CHKH library and its host replay, Lemma H's
baked carriers and host values, founders and the gene prior, the run object with the mass-based classifier),
`src/hooks_r_kern.py` (the island kernel over hooked types; one jitclass state), `src/hooks_r_gate.py` (the gate and
the Lemma H audit), `src/hooks_r_run.py` (gate, statics, validate, audit, one, cells), `src/hooks_r_report.py`;
`tests/test_hooks_r.py` (6 tests, passing; 2 need the untracked world-K tables). Probes ran on the discarded replicate
990 (and 991 for the audit); no counted cell has run.

### 2.1 The gate: GO (`runs/hooks-r-gate.json`)

- **(g1) Conservative.** 60 sampled stored world-K checks give the same value and the same step count under the hook
  library (iswrap/callcheck extended in place, CHKH appended) as under world K's library; all 60 equal the stored
  table.
- **(g2) The primitive.** 21 fill lists (every scope; conflicting overlapping keys: none-D with source-C, behaviour-C
  with history-D in both orders, two none fills, SELF with an own-source key, root keys for ⌜C⌝/⌜D⌝/self/other,
  two-tag programs, a fill for a tag the program lacks, a key that holds nowhere) on six hooked programs against 12
  opponents: **598 gene-site checks, the term's CHKH, the host replay's CHKH and the host-side conflict rule agree on
  every one.**
- **(g3) Soundness.** With production lists (D step, C scripts against FairBot and PrudentBot), **223 certificates
  accepted at partner, probe and self roots, 0 false atoms** against the executed play. Re-checking after a write: a
  hooked FairBot's production C script (`EvR*; ChkR[EvR*; ChkR[RunNeg · EvR*@1; Ax] · Hyp]`, the hook refuted)
  validates against FairBot (T, play (C, C)); after a history D fill keyed to FairBot it stops validating (F, play
  (D, D)) and still validates against PrudentBot. Forged entries (a bare Hyp, a Fill for a missing tag, a Fill in
  FairBot's list) are inert.
- **(g4) Costs of a gene-site check (term steps):** empty 71; none/role/root fills 340 / 564 / 1,012 for 1 / 2 / 4
  fills; history/source 1,406 / 2,745 / 5,420; **behaviour 28,982 / 57,848 / 115,580** (three certified-play probe
  checks per behaviour fill). These are the cost model's inputs (R15); the ideal table charges nothing.

### 2.2 Lemma H audit (`runs/hooks-r-audit.json`)

On live runs (8 islands of 200, the maximal, clone-fill and recency-only rules, replicate 991) at generations 0, 30
and 200, 200 sampled pairs each of distinct co-resident types (one at least hooked): the kernel's plays against the
**true hooked carriers** (fills as Fill entries; the kernel's baked scripts translated by inserting the gene-site
ChkR with Run or RunNeg) evaluated on the ideal table: **1,800 / 1,800 pairs agree; behaviour classes 900 / 900.**
The executed plays (the term at fuel K with V = K/4) differ from the ideal ones in 2 of 360 sampled pairs: nested
gene-site checks can exhaust the cap. The ideal-table reduction is exact; executability is a cost question.

### 2.3 Validation (`runs/hooks-r-validate.json`)

Grammar P founders without hooks (cell B) against world K's annealed kernel (`world_k.IslandRun`), replicates 0 and 1
to 1,000 generations: **0 generations with any slot difference; island P(C,C) identical.** The mass-based classifier
(§2.5) and world K's type-level classifier give the same universal-open verdict at all 12 checkpoints and the same
island label on 755 of 768 island-checkpoints (the 13 others: mass 'open', type 'rival', islands in transition).

### 2.4 Statics (`runs/hooks-r-static.json`; 20 replicates of (200, 64) founders)

Grammar H 99,588 spellings (P 12,546; prior mass P 0.136, one-tag 0.549, two-tag 0.315). Per run: 11,854 distinct
founder spellings of 12,800; 11,063 hooked founders, 6,982 carrying fills; seeded fills ≈ 1,810 per scope (uniform);
**seeded SELF fills 0.05 per run**; of 3,629 seeded source and history fills keyed to a founder spelling, **60 (1.7%)
name a spelling present on the holder's island** (R2's bounds hold by construction of the prior).

### 2.5 Deviations and conventions (declared before any counted cell)

1. **Fill encounters r_f = 2, not 10** (§1.5): at r_f = 10 the scramble cost 30–80 s per generation at (200, 64)
   (every new fill list is a new type whose payoffs against ~200 co-resident types must be computed). Each individual
   takes part in about 4 fill encounters per generation.
2. **The island classifier is mass-based** (`HRun.net_stats`): fills fragment an island into many types of a few
   spellings (in a probe the majority *type* held 2.5–7.5% of its island), so world K's majority-type classifier labels
   islands by an arbitrary 3% type. Held: within-island P(C,C) ≥ 0.5; open share: residents mutual with FairBot-H;
   open: held and open share ≥ 0.5 and in the main network (cross-island mutual-cooperation mass ≥ 0.5 with the hub);
   identity: held, open share < 0.5, ≥ 0.95 of its residents' mutual cooperation with their own spelling; rival:
   held otherwise; universal-open: every island open and every pair of islands ≥ 0.5 cross mass; universal on target:
   also every island's PrudentBot-H share ≥ 0.5. Validated against the type classifier on P runs (§2.3).
3. **Settledness is exact:** an encounter is skipped only when production cannot change either side: a C entry or no
   C leaf in any resolution (structural), and a D entry or a D step that writes nothing (the D step is a function of
   the type). World K's FUT shortcut (no C script at any signature of the P closure) is not used: composite partners
   can present signatures the P closure never met (a probe using FUT changed the trajectory).
4. **Composite values on the ideal table** (host replay of baked carriers; Lemma H); composite productions use the host
   tactic without world K's executed-cap patch (`prod_exec.json`). Executed plays differ from ideal plays in 2/360
   audited pairs.
5. **Caches are per job** (no persistence across jobs: iterating multi-million-entry numba dicts from Python cost more
   than recomputing); a pair-value cache keyed by type and creation stamp inside a job.
6. **Two types that differ only in their fills' sources** (seed/write/copy/contract, metadata not in the quote) are the
   same quote but are treated as distinct quotes (twins). Rare (identical fills from two sources on one spelling and
   block).
7. **Inert updates:** an inert-source write that matches a held fill's (tag, scope, key) updates it in place (the
   fill takes the writer's source and becomes inert).
8. **Horizons and replicates** (cost, §2.6): main cells B, I, M to 2,000 (not 10,000; world K: no S-nonself run at
   N ≥ 200 changed status after 2,000); ablations to 1,000, paired with M's generation-1,000 snapshot.
9. **Dropped by the drop order** (projection > 24 h on 3 workers): the conflict-rule ablation (recency only),
   fission–fusion (and infeasible: a merged population of ~7,000 fragmented types puts every type change against all
   of them, projected ≥ 10 s per generation), and (400, 64) (infeasible: no generation 10 within 10 minutes in a
   probe). R10, R13, R14 and RE 5 are therefore not scored.
10. **The SOG wing is not run** (§3): its factorized tables (Lemmas B and F₃) assume probe-only bosses, which source-
    and history-keyed boss fills break, and the PD wing alone exhausts the budget. RE 4 is not scored for Part R.

### 2.6 Costs and the plan

Probes (replicate 990): M to 2,000: 2,654 s (host pair values 725 s for 1.96 M composite misses at a low memo cap,
since raised); the clone-fill diagnostic to 1,000: 1,436 s; I to 2,000: 357 s; B ≈ 0.1 s per generation. M-like runs
to 1,000 ≈ 20 min. Plan, in this order:

| tier | cells | replicates | horizon | projected worker-h |
|---|---|---|---|---|
| main | B, I, M | 20 | 2,000 | 17 |
| core ablations | seedonly (never dropped), M-source, M-root, M-behaviour, M-history, nowrite, idroutes, clone | 20 | 1,000 | 53 |
| secondary ablations | M-none, M-role, nocopy, nocontract, shuffle, noinherit, grudgeonly, renorm | 10 | 1,000 | 27 |

Main and core ≈ 70 worker-hours (≈ 23 h on 3 workers). The secondary tier runs after them with 10 replicates and is cut
(disclosed) if the wall clock requires; it scores no registered prediction except RE 2's and R7's history controls
(shuffle, not inherited), whose 10-replicate scores will be called inconclusive where 10 runs cannot decide them.

### 2.7 Addenda while the cells ran (each written before the cells it affects)

- **Batch 1** (`runs/hooks_r/batch_main.log`) stopped when a seed-only run overflowed the type table within one
  generation (kernel error 3); the pool died with two maximal runs unfinished. Garbage collection moved into the kernel
  (between Moran events) and the driver now survives single-job failures (commit "garbage collection inside the
  kernel"); a rerun of a counted inert run (I rep 1) reproduced its row exactly (classes, P(C,C), fills, trace), so
  type-id recycling changes no trajectory. Finished rows were kept; the batch resumed.
- **Batch 2** (`batch_main2.log`) ran main + core; it stalled on 2026-10-20 07:13 with all workers idle (the session
  stopped on an API spend limit; nothing was computing). The stalled pool was killed by pid. Nine core replicates had
  no row (seedonly 3; M-source 1, 15; M-root 3, 12, 15, 16; nowrite 19; idroutes 1; clone 17) and are rerun with
  identical seeds (deterministic kernel).
- **Batch 3** (`batch_main3.log`, launched 2026-10-21, detached): the nine missing core replicates, then the secondary
  tier at 10 replicates as planned in §2.6 (projected ≈ 8 h on 3 workers, under the remaining ≈ 12 h budget, so nothing
  further is dropped). Command:
  `nohup python3 -u src/hooks_r_run.py cells --workers 3 --cells seedonly:1000:20 M-source:1000:20 M-root:1000:20
  nowrite:1000:20 idroutes:1000:20 clone:1000:20 M-none:1000:10 M-role:1000:10 nocopy:1000:10 nocontract:1000:10
  shuffle:1000:10 noinherit:1000:10 grudgeonly:1000:10 renorm:1000:10 > runs/hooks_r/batch_main3.log 2>&1 &`.
  Expected outputs: `runs/hooks_r/rows_<cell>.json.gz` complete for every cell above.
- **The identity label is noisy (found in the main cells, before any audit):** the mass-based 'identity' class marks
  monomorphic rival islands whose spelling would cooperate with absent spellings (in B rep 13 the AP-network reader
  `if(CHK(them,me,D),D,if(CHK(them,me,C),C,D))`, a known non-identity rival in world K, is 'identity' on islands it
  holds at 99–100% and 'rival' elsewhere). A labelled post-hoc audit (`hooks_r_run.py idaudit`, written before it
  runs) reruns runs with identity labels deterministically and tests each such island's majority type against 300
  self-cooperating world-K units, the panel and every living type of another spelling; identity counts used in the
  verdicts are the audited ones, the raw labels are reported beside them.
