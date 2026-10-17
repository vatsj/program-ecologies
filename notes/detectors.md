# Legitimate detectors: a grudge rule for gentle source-readers, and what decides them against PrudentBot's network (notes, 2026-10-17)

Spec `specs/2026-10-17-legitimate-detectors.md` (reviewed by gpt-6.1-sol and gemini-4-argon; its "Amendments after
review" supersede the earlier text where they conflict). §1 is written by hand before any code of this run and before
any counted cell. §2 (the executed soundness gate, the keyed tables, validation, controls, projected costs) is appended
after the code and before any counted cell.

Base, imported unchanged: milestone 4's checker K_T^cert (`src/lt_cert.py`), milestone 5's genes and tables
(`src/lt_genes*.py`), provenance's S-nonself rule and kernel (`src/provenance*.py`), the realizable-scaling cells, the
removing-rivals predator classifier, the Pangaea fission–fusion merge and the annealed schedules, on grammar P (n = 7,
12,546 spellings, 4,162 run trees, prior L), w = 0.3, payoffs CC 0, CD −2, DC 1, DD −1. Every ε = 0 number is a lottery
statistic at finite (N, I, horizon); every tail number is a finite-ε diagnostic, never π.

*Disclosure (before this section).* Before writing it I read the spec, CLAUDE.md, the RESULTS sections named in the
brief, the removing-rivals and Pangaea notes, milestone 4's notes §1 (the checker) and the code; cloned the untracked
cached tables read-only from the identity-resistant worktree (copy-on-write; `runs/lt_genes/static/`,
`runs/provenance/{static/, OSV.npy, SPO.npy, prod_exec.json, sets.npz}`); and made table lookups with throwaway
scripts: the run trees that read `CHK(me,them,D)`, the detector's units and scripts, its row of the ideal table, the
stored exploitable-detector holders, and the D scripts that use a hypothesis rule. No dynamics of any kind have been
run. Those lookups changed the design (§1.1, §1.3), and the change is stated before any code.

## 1. Design

### 1.0 The object in one paragraph

The RS's question: is the certified-defection detector `if(or(CHK(them,them,D),CHK(me,them,D)),D,C)` a legitimate,
gentler-than-PrudentBot network that would survive if it could evolve evidence against its predators? The spec's
answer to "evidence" is a **grudge rule**: after being defected against, a reader appends a certificate that it defects
against the defector's source, keyed to that source and inherited. The run (a) settles the detector's actual phenotype
in the realizable ecology, (b) builds the grudge certificate in the realizable checker and gates the run on its
soundness, (c) measures what grudges do to predator establishment, and (d) asks what decides detectors against the
PrudentBot network at equal mass and from natural seeds, labelling every removal by cause (RS, 2026-10-17: predation,
inefficiency and the prudence premium are good reasons; abundance alone is not).

### 1.1 The detector in the stored ecology (L): not gentle (table lookups)

The spec's premise is that the detector cooperates by default, its cooperation is uncertifiable, and it is exploitable
(predator mass ≈ 0.0057). The cached tables say otherwise for every detector that has met anyone:

- **Its first D step writes a self-hypothesis defection.** Under S-nonself the D step runs at the first encounter
  (PROD(x, ⌜D⌝, D) while the list has no D entry). For the detector the frozen tactic returns
  δ = `EvR*; ChkR[RunNeg · EvR*@1; ChkR[EvR*; Ax · Hyp]]`: evaluate to the first call (`CHK(them,them,D)`), refute it
  (RunNeg), evaluate to the second call (`CHK(me,them,D)`, the root's own box R at a D root) and close it by Hyp^self.
  The E unit 4648 becomes unit 544 = (τ 544, C (), D (δ)).
- **δ is opponent-generic.** Scripts mention no source, so δ validates at every root (det, m) where the first box is not
  T: the detector is *certified to defect against every partner*, and since it reads that certificate, it does. Unit
  544 cooperates with **187 of 11,365 reachable units**, and every one of those is a check timeout (the nested RunNeg's
  check regresses, so CHK(me,them,D) returns TO, not T). It defects against CooperateBot (H and E), DefectBot, FairBot,
  PrudentBot and the anti-punisher; it cooperates with its own quote (at the self root the first box *is* R, which
  RunNeg may not run, so δ fails) and defects against its twin (same unit, other spelling). Unit 12431 (δ plus a C
  script written before δ) behaves the same.
- **So in L the detector is a near-identity clique**, not a gentle network. The stored "exploitable detector islands"
  (117 of the 260 exploitable rival islands in removing-rivals) are held by units 544 and 12431; their "predators"
  (mass 0.0054–0.0058) are units whose checks of the detector time out. The RE's play matrix (cooperates with FairBot,
  PrudentBot, CooperateBot; defected against by FairBot and PrudentBot) holds only for the E unit 4648, which exists for
  at most one encounter.
- **A grudge rule changes nothing in L**: a keyed grudge against P is a restriction of δ, which the detector already
  holds unkeyed.
- **It is a class, not one program.** 155 run trees (402 spellings, μ = 0.0308) read `CHK(me,them,D)` with D on T
  (the *own-D readers*); 546 run trees (μ = 0.128) carry a D script that uses a hypothesis rule after their D step.
  Hypothesis-closed D scripts are 7 of the 13 D scripts in the universe.

### 1.2 The grudge certificate in the realizable checker, and the soundness gate

**A Key rule.** The checker has no lookup by opponent: it tries the entries of the asked outcome in list order and
accepts the first script that validates (milestone 4 §1.1). A certificate bound to one partner therefore needs one new
rule, added to the script language:

    Key (code 27):  node (27, (k, (p, 0))).  Conclusion = premise sequent.
                     Side condition: k = bare(m), where m is the opponent quote of the check's root (read from the
                     root box R's argument) and bare(q) is q's code with its certificate list stripped: for a carrier
                     λme.λthem.(λcerts. BODY) CERTS, the encoding of BODY; for any other quote, q's whole encoding.

In the checker term, `cchk` gains one `cond` clause, placed after every existing clause and before `else 0`:
`((eq rule 27) (if (eq j (bareof m)) (cchk cx (fst ps) L R) 0))`, with `bareof` the `getcerts` walk returning the body
instead of the list. The host replay checker gets the same clause.

- **Conservative.** For every script without a node 27 the check performs literally the same computation as before (the
  new clause is reached only by rule 27, which no existing script contains), so every value *and every step count* of
  every existing check is unchanged. The gate tests this on a sample (§2).
- **Sound.** The Key node's obligation is its premise's (same sequent); its side condition only removes derivations.
  Theorem S^cert's induction goes through with one more trivial case, so every accepted certificate, keyed or not,
  implies its exact fuel-indexed atom against arbitrary opponents. Lemma Sym is untouched: the key test is a syntactic
  predicate of (k, the root's opponent quote), and the swap check rebuilds its root from the swapped argument, so the
  partner validation of a keyed script tests the key against the reader, as it should.
- **Keying.** k is the partner's *bare* source, so acquiring certificates does not evade a grudge (amendment 2); a
  respelled partner (another spelling, same behaviour) does (a fresh source; the control in Part A). The holder side is
  the whole quote, as for every certificate: the atom is about the holder's run with its actual list at budget K.

**The grudge certificate.** For a holder x and a defector P, the grudge is **Key_{bare(P)}[δ_x]**, a keyed copy of the
holder's own D-step script: no new derivation is searched for, the cost is one script copy plus the key. For the
detector at root (det, P, D): Key passes; δ evaluates to `CHK(P,P,D)`, refutes it (RunNeg: P is not a certified
self-defector), evaluates to `CHK(det,P,D)` = R and closes it by Hyp^self. It is accepted exactly when the first box is
not T. **Self-fulfilling:** the reader's own `CHK(me,them,D)` call is that very check, so it returns T and the detector
plays D, which makes the atom true. Where the first box is T the grudge fails but the detector defects through its first
disjunct anyway.

**Adversarial cases (by hand; executed in the gate).**
- *Non-readers* carrying Key_P[δ] (CooperateBot, FairBot): their run reaches no `CHK(me,them,D)` call, so δ's ChkR and
  Hyp nodes do not match the run (EvR* reaches a value or a different call) and the check returns F. The certificate is
  inert.
- *Negated readers* `if(CHK(me,them,D),C,D)`: ChkR at the own box puts R on the left with ρ_T = C = ⊥ on the right;
  nothing closes Γ, R ⊢ ⊥ (RunNeg may not run R), so the script is rejected. No accepted script ever claims D for a run
  that plays C.
- *A keyed copy at another opponent*: rejected by Key. *Two holders with grudges against each other*: each check is a
  Hyp^self closure on its own root; no Hyp^pair is involved, both play D, both atoms true.

**The gate (amendment 1), go/no-go before any cell.** Executed at the term level with the extended library at K = 10⁶,
V = K/4: (g1) conservativeness: values and step counts of a sample of existing checks equal before and after the
extension; (g2) the detector with Key_P[δ] against P: check T, play D, atom true; (g3) against a respelling of P and
against other partners: no change; (g4) against P carrying certificates: still D; (g5) the non-readers and negated
readers above carrying forged grudges: rejected, play unchanged; (g6) mutual grudges between two own-D readers: both
D, both atoms true; (g7) the host replay equals the term on every gate check; (g8) verification steps of a detector
check against list length (0, 1, 3, 16 grudges). Also executed: the L detector (unit 544) against CooperateBot plays D
(§1.1 by execution). **No-go** if any accepted certificate's atom is false, or (g1) shows any difference.

### 1.3 Deviation 1 (forced by §1.1): the keyed world K

A grudge needs an unkeyed δ *not* to exist, otherwise the detector is a clique and the grudge is moot. The minimal
change consistent with the spec's keying (amendment 2) is to read every self-hypothesis D certificate as what the
production step that wrote it actually established: **in world K every D script whose derivation uses a hypothesis node
(Hyp^self or Hyp^pair) is keyed to the bare source of the partner it was produced against.** The D step's partner is
⌜D⌝ (DefectBot's quote, a non-carrier), so the D step writes Key_{⌜D⌝}[δ]: "I defect against DefectBot", which is the D
step's literal content and exactly what PrudentBot's guard `CHK(them,^D,D)` asks. Hypothesis-free D scripts (FairBot's
`EvR*; ChkR[RunNeg · EvR*@1; Ax]`, DefectBot's `EvR*; Ax`) are true of the run wherever they validate and stay
opponent-generic; C scripts are unchanged (keying them would end opponent-generic cooperation, which every network
uses). World L (the stored ecology) is kept as the reference. K is a production convention, uniform for every program,
like S-nonself; it is disclosed as the run's main deviation, and its cost to the rest of the ecology is measured (the
L-vs-K contrast at equal founders, Part C).

**The canonical detector in K (by hand).**
- *Production at its first encounter* (S-nonself: C step, then D step). The C tactic at root (det, m, C) meets
  `CHK(m,m,D)`, refutes it if m is not a certified self-defector, then meets `CHK(det,m,D)`: at a C root this box is
  neither R nor S, so RunNeg may run it, and the check of det's (still empty, later keyed) D list returns F. So det
  writes σ_C = `EvR*; ChkR[RunNeg · EvR*@1; ChkR[RunNeg · EvR*@1; Ax]]` (a script already in the universe), then the
  D step writes Key_{⌜D⌝}[δ]. **Its cooperation becomes certifiable** (the spec's premise fails in K too).
- *Plays at its natural unit* (σ_C, Key_{⌜D⌝}[δ]): cooperates with CooperateBot (gentle), defects against certified
  self-defectors (DefectBot), cooperates with FairBot and is certified to (FairBot cooperates back), and is certified both
  to cooperate with PrudentBot and to defect against ⌜D⌝, so **PrudentBot cooperates with it**. In K the detector is a
  member of the PrudentBot network, not a rival, once certified.
- *Its predators in K:* every partner that defects against it without being a certified self-defector (keying removes
  self-certification from defectors whose D script was hypothesis-closed), and anti-punishers (`if(CHK(them,^D,D),D,C)`
  now sees the detector's ⌜D⌝ certificate and defects; the detector cooperates with it).
- *Grudges in K* protect against those, and also record the defections it suffered while uncertified: at its first
  encounters FairBot- and PrudentBot-shaped partners defect against an uncertified detector. A grudge then makes the
  pair feud permanently: the detector defects (grudge), and its σ_C no longer validates against that spelling (RunNeg on
  its own D box fails), so the partner defects back. **Grudges can split the network they protect.** The RE's
  head-to-head (Part B) is therefore a test of whether bootstrap grudges make detectors a rival, not of two rival networks.

### 1.4 The grudge rule in populations

Units, the lack rule, S-nonself production and the ideal table are milestone 5's / provenance's; in K the tables are
rebuilt by the same closure with the keyed reading (§2). An individual is (unit, rule, spelling, grudge list G).

- **Writers.** A unit whose D block is a hypothesis-closed script δ (keyed to ⌜D⌝ in K). Only own-D readers can ever
  write a grudge that changes play (§1.2); other writers' grudges are never valid while they cooperate (soundness).
- **Write.** At a production encounter between x and y (spellings s, s'), with the pre-encounter plays a_xy, a_yx: after
  x's S-nonself production (C step, D step) giving unit u', x appends s' to G if a_xy = C, a_yx = D, s' ≠ s, s' ∉ G, u'
  is a writer, and Key_{s'}[δ_{u'}] validates for the would-be self at root (x', y) (the table W, host-computed). "Was
  defected against while cooperating" is the trigger; a mutual defection writes nothing (the writer already defects).
  A grudge against one's own spelling is never written (S-nonself's rule, applied to grudges).
- **Cap.** G holds at most 3 keys (the per-root run's bundle cap, k = 3), FIFO eviction; evictions are counted. A cap of
  16 is a diagnostic in Part A.
- **Vertical** transmission: a newborn copies its parent's type, G included. **Horizontal** (arm KGh): at an encounter
  between two writers with the same δ (skeleton copying), each adopts the other's keys not held, if Key_k[δ] validates
  for its would-be self at root (self, ⌜k⌝) (k's bare source with an empty list: the table W at k's E unit); FIFO cap.
- **Play with grudges is exact.** A pair's checks read only the two lists at the roots (x,y), (y,x), the self roots and
  ⌜C⌝/⌜D⌝, and a keyed entry is live only where its key is the root's opponent. So a pair's plays depend on the two units
  and two bits, b_xy = [s' ∈ G_x], b_yx = [s ∈ G_y], plus the relation. The tables AG1 (one bit) and AG2 (both bits,
  writer × writer) are host-computed with explicit keyed lists, like the base table. Payoffs and P(C,C) use them.
- **Controls.** *Sham* (KGs): the same writing, cap, cost and inheritance, with the bits ignored in play (checking
  disabled). *Prewritten* (KGp): no writing; a writer holds, from birth, a valid grudge against every spelling that
  would defect against it while it cooperates (b_xy = 1 iff W and base a_xy = C and base a_yx = D): perfect memory, the
  upper bound on certificate efficacy without production or transmission.
- **Logged.** Grudges written (writer class, target class, generation; whether the target's natural unit is mutual with
  the writer's natural unit, a *bootstrap grudge*), held per program, evictions, adoptions; protected (holding a grudge
  against a present predator) against unprotected detector mass over time; repeat encounters (a predator meeting an
  already-marked detector).

### 1.5 Classes, removals and causes (frozen now)

- **Natural unit** of a spelling in K: E unit → S-nonself C step then D step against FairBot's H unit (unit 3, unchanged
  in K). **DET** (the detector network): own-D-reader spellings whose natural unit self-cooperates, defects against
  DefectBot-H and cooperates with CooperateBot-H (gentle). **PBN**: spellings whose natural unit is in 𝒯_K
  (self-cooperating, mutual with PrudentBot's H unit) and not in DET. Holder labels for an island or population: DET,
  PBN, other open (mutual with FairBot-H), identity, other held, unheld.
- **Removal events.** *Islands* (I > 1): an island held by network X whose holder label leaves X and stays out for ≥ 25
  generations (six 5-generation checkpoints). *Network removal:* X holds no island (I > 1), or X's share of a merged
  population falls below 0.01 and stays there to the horizon. The window of a removal is the 500 generations before it
  (or from the merge).
- **Labels** (descriptive, overlap allowed): *inefficiency*: the island (population) P(C,C) at the window's start is
  < 0.95; *predation*: in the window, a type that strictly exploits the modal resident (cooperated with by it, defects
  against it) reaches ≥ 0.3 of the island (population); *prudence premium*: in the window, the winner's per-capita
  fitness edge over the loser is positive and its third-party part (payoffs against types in neither network) is
  positive and decisive (the edge without third parties is ≤ 0); *abundance*: the winner was the island's (population's)
  majority network at the window's start or arrived as a migration/merge majority, with none of the above;
  *unresolved*: otherwise. **Headline precedence** (amendment 4): inefficiency, predation, prudence premium, abundance.
  **Good reasons** (RS, 2026-10-17): inefficiency, predation, prudence premium; reported apart from abundance.
- **Sucker exposure** (the RS's decision): per cell and schedule, unconditional-cooperator encounters (production
  encounters with a type that cooperates with DefectBot-H) and unconditional-cooperator island-generations, reported
  beside every prudence-premium removal.
- **Replays** (amendment 4): for up to 5 removals per labelled class per cell, a matched replay from the window's start
  with the same kernel seed and arrivals in which the suspected edge is suppressed: prudence premium → every
  unconditional cooperator replaced by DefectBot-H at the window's start; predation → the exploiting types removed
  (replaced by the modal resident). The label is *confirmed* if the removal does not occur within the window's length.

### 1.6 Cells (as amended)

r = 100 production encounters per Moran event everywhere; world K unless stated; arms K0 (no grudge rule), KG
(vertical), KGh (vertical + horizontal), KGs (sham), KGp (prewritten).

- **A, predator assays.** One island (I = 1) of the canonical detector spelling at its natural unit, empty grudge lists.
  One fresh predator founder (E unit, S-nonself, the arm's rule) replaces a random resident; the run stops when the
  predator's spelling reaches 0.5 of the island (*established*), is lost, or at 1,000 generations. Predators: the top 3
  spellings by prior mass among the detector's predators in K (the removing-rivals classifier on K tables). N ∈ {200,
  800}, arms K0, KG, KGh, KGs, KGp, 100 replicates each; cap-16 diagnostic for KG at N = 800. **Second arrivals** (KG,
  KGh, N = 200): after a first arrival is lost, the same spelling (exact source) or a synonym (another spelling of its
  run tree) arrives; 100 each. **Scaling diagnostic** (amendment 6): N = 3,200, K0, KG, KGh, top predator, 50 each.
- **B, head-to-head.** Fission–fusion (128 islands of 100, mN = 1, merged at 200, horizon 10,000). B1: 6,400 founders
  ∝ μ within DET and 6,400 ∝ μ within PBN, in one random partition; B2: 12,800 founders ∝ μ over DET ∪ PBN (natural
  shares). Arms K0, KG; schedules ε = 0 and the post-merge annealed tail at K = 1 (εN(t) = a(1 + (t − 200)/t₀)^−2 per
  merged population, t₀ = N/2 with N = 12,800, total A = K/(ρ μ_AP) = 52 arrivals, cut at 10,000); **the RS's tail
  comparison:** B1 also at K = 3, so B1 runs at K ∈ {0, 1, 3}. 20 runs per cell.
- **C, natural seeds under L, unsponsored.** Fission–fusion as B with L founders, and islands (200, 64) (calibrated
  mN, horizon 10,000, tail per island: A = K/(ρ μ_AP), t₀ = N/2, onset 200). Arms K0, KG at ε = 0 and K = 1; KGh and
  KGs at ε = 0 on fission–fusion only. World L at the same founders and seeds (the stored S-nonself kernel; this is also
  the reproduction check). 20 runs per cell.
- **Reference:** the sponsored PrudentBot founder (C-donor positions, rule H, its H list) in C's fission–fusion cell, KG,
  ε = 0.
- **Drop order** (spec), applied only if the projected total exceeds ~24 hours on 3 workers and disclosed in §2: B2's
  tail cells, then C at (200, 64), then the reference.

### 1.7 Statistics

Per run: the holder label of every island (or the merged population's network shares) at checkpoints every 5
generations to 1,000, then every 50; winner (the network holding ≥ 0.95 of held islands or of the population at the
horizon; else *coexistence*), every removal with its labels and window, universal-open, DET and PBN shares, P(C,C)
(efficiency is reported, never selected on), grudges (written, held, evicted, adopted, by class pair), sucker exposure,
arrivals by class under the tail. Per cell: counts with exact (Clopper–Pearson) 95% intervals; paired contrasts by
McNemar on matched replicates; support and transition structure (which labels follow which), including unresolved
coexistence.

### 1.8 Hand predictions (mine; the numbered ones go to the predictions file)

- The gate passes; (g1) shows zero differences; the L detector plays D against CooperateBot by execution.
- In K the canonical detector's natural unit is mutual with FairBot-H, PrudentBot-H and CooperateBot-H and defects
  against DefectBot-H, so it is in 𝒯_K: the "detector network" is a gentle sub-family of PrudentBot's network.
- Predator assays: K0 establishment ≈ 0.26 (strict dominance, removing-rivals' exact ρ); KG cuts it, more at N = 200
  than at 800 (a predator meets 200 partners per generation whatever N, so marking covers a 200-island in about a
  generation and an 800-island in about four); KGh near 0; sham equal to K0; prewritten near 0; a synonym arrives as a
  first arrival does.
- Head-to-head at ε = 0: without grudges the two families are one network and nothing is removed (coexistence by
  drift); with grudges, bootstrap feuds are capped at 3 keys per detector against hundreds of PBN spellings, so most
  pairs stay mutual and removals stay rare. The tail brings predators (detectors lose ground without grudges) and
  suckers (the prudence premium favours PBN in proportion to the sucker supply).
- Natural seeds: K is more universal than L (it removes a 0.03-mass family of near-cliques); grudges change little at
  ε = 0 (predators die in the scramble whatever the detectors do).

## 2. The executed gate, world K's tables, validation, controls and costs (appended after the code, before any counted cell)

Code: `src/detectors.py` (the Key rule in the checker term and the host replay, world K's reading, grudge certificates,
the gate, the K and grudge table builders, the run object), `src/detectors_kern.py` (the grudge kernel),
`src/detectors_run.py` (gate, static, ext, grudge, statics, validate, audit, cells), `src/detectors_report.py`;
`tests/test_detectors.py` (6 tests, passing; 3 need the cached tables).

### 2.1 The soundness gate: GO (`runs/detectors-gate.json`)

- **(g1) Conservative:** 240 sampled stored checks (126 T, 103 F, 11 TO; median 12,582 inner steps) give the same value
  and the same step count before and after the Key clause: **0 differences**.
- **The L detector by execution:** with its D-step script δ (stored script 10, reproduced by the tactic) it plays D
  against CooperateBot, FairBot-H and PrudentBot-H and C against its own quote (§1.1 confirmed by execution).
- **(g2–g4):** with Key_P[δ] (P = `if(CHK(them,me,C),D,C)`, empty list, not a certified self-defector) the check is T
  (25,485 steps), the detector plays D against P and the atom is true; against the respelling
  `if(not(CHK(them,me,C)),C,D)` and against CooperateBot the grudge is skipped (F) and it plays C; against P carrying a
  certificate it still plays D (bare-source key). Its C certificate against P fails once the grudge is held (RunNeg on
  its own D box).
- **The K detector is legible:** σ_C = `EvR*; ChkR[RunNeg · EvR*@1; ChkR[RunNeg · EvR*@1; Ax]]` (produced by the tactic
  against FairBot-H) validates against FairBot-H (35,883 steps) and PrudentBot-H (57,280); it plays (C, C) with both,
  and Key_⌜D⌝[δ] answers PrudentBot's ⌜D⌝ guard (T).
- **(g5) Forged grudges are rejected:** CooperateBot with Key_P[δ]; FairBot with Key_P[δ] (F, though FairBot plays D
  anyway); the negated reader `if(CHK(me,them,D),C,D)` with five forged keyed scripts (δ, `EvR*; ChkR[EvR*; Ax · Hyp]`,
  `Hyp`, `EvR*; ChkR[Hyp · Hyp]`, `EvR*; ChkR[Ax · Hyp]`): all F, plays unchanged.
- **(g6) Mutual grudges** between the detector and `if(CHK(me,them,D),D,C)`: both T, both play D, both atoms true.
- **(g7) Host replay = term** on all 26 gate checks. **Accepted false atoms: 0.**
- **(g8) Cost of grudges** (verification steps of the detector's checks; keyed grudges ahead of a matching one):

| grudges held | CHK(det, P, D) | CHK(det, C, C) (its C certificate) | play vs CooperateBot |
|---|---|---|---|
| 0 | F 1,202 | T 17,176 | 1,307 |
| 1 | T 25,485 | T 27,659 | 2,384 |
| 3 | T 44,457 | T 48,625 | 4,538 |
| 16 | T 166,735 | T 184,904 | 18,539 |

  Each grudge adds about 10⁴ steps to every check of the holder's list (the list is converted to data and every key is
  compared): at the cap of 3 the detector's C certificate costs 2.8× and its play 3.5×; at about 22 grudges its C check
  would exceed the cap V = 250,000 and FairBot-shaped readers would stop cooperating with it. The ideal-table
  populations below do not charge these costs; they are reported, not selected on.

### 2.2 World K's tables

- **Closure** (`runs/detectors/K/static.log`): milestone 5's closure with every check under the keyed reading converged
  in 2 rounds: 17,375 units (L: 17,391), 11,260 reachable (L: 11,365), 29 scripts, 25.1 M host checks, 874 s on 3
  workers.
- **Executed production** (`ext.json`): 23,130 production memo keys, 22,958 shared with L (their stored executed
  outcomes reused; 60 re-executed in K, 60 agree), 172 new (120 cap timeouts, all at signatures containing a TO box, in
  trees reading `CHK(them,^D,C)`-type atoms, none in an own-D reader). OSV and SPO are placeholders (used only by S-k
  windows and counters, which this run does not use).
- **Grudge tables** (`grudge.json`): 155 own-D-reader run trees, **275 writer units** (reachable, D block a
  hypothesis script). W (Key_v[δ_w] valid at (w, v)) is true for 2,425,149 of 3,096,500 writer × unit pairs, and the
  grudge changes the pair's play in 2,155,985 of them. AG1 and AG2 fully determined; the sham audit (1,000 pairs, key
  matching no quote) reproduces the base table exactly.
- **The two-bit reduction against explicit terms** (`audit.json`): 54 live pairs from a B1 and a C fission–fusion run
  at generation 250 (individuals' own spelling bodies, full grudge lists of up to 3 keys, host replay): **54/54 agree**
  with the kernel.

### 2.3 Statics (`runs/detectors-static.json`; natural unit = E unit after the C and D steps against FairBot-H)

| | L | K |
|---|---|---|
| the detector's natural unit | (σ_C, δ) | (σ_C, Key_⌜D⌝[δ]) |
| cooperates with (reachable units) | 187 of 11,365 (all check timeouts) | 10,186 of 11,260 |
| (det, them) vs CooperateBot-H / DefectBot-H / FairBot-H / PrudentBot-H / anti-punisher-H | D,C / D,D / D,D / D,D / D,D | C,C / D,D / C,C / C,C / C,D |
| in 𝒯 (mutual with PrudentBot-H) | no | **yes** |
| accessible predator mass (removing-rivals classifier) | 0.0058 (74 spellings) | **0.260** (3,319) |
| exploiter mass (self-cooperators included) | 0.0063 | 0.318 |
| DET (gentle own-D-reader establishers) | 11 spellings, μ 0.0007 | 21 spellings, μ 0.0018 |
| PBN | 484, μ 0.039 | 619, μ 0.049 |
| 𝒯 units | 235 | 298 |
| S-nonself identity units / the TwinD family Q | 8 / 10 spellings, μ 7.1·10⁻⁴ | **0 / none** |

- **K dissolves the seed's identity cliques.** The TwinD family of every earlier S-nonself run
  (`if(or(CHK(me,me,D),CHK(me,them,D)),D,C)` and its 9 relatives) is a set of own-D readers whose clique property *is* the
  generic self-hypothesis δ (D against every distinct quote, C at the self root where the RunNeg would hit R). Keyed,
  they become gentle readers; no identity unit is reachable under S-nonself in K. This is a consequence of deviation 1,
  not a design aim, and it changes Part C's baseline.
- **K's predators.** Keying removes the self-certification of defectors whose D certificate was hypothesis-closed, so
  they become predators of every gentle reader: the top three are `if(CHK(them,them,D),D,D)`, `if(CHK(me,^D,D),D,D)`,
  `if(CHK(me,^D,D),D,C)` (5.2·10⁻⁴ each). The anti-punisher exploits the K detector (the detector is certified to defect
  against ⌜D⌝) but self-cooperates, so it is an exploiter, not a classifier predator.
- **DET is two families.** 9 of the 21 DET spellings (μ 0.0007) are mutual with PrudentBot-H and FairBot-H (the
  canonical detector's tree and those whose other atom is `CHK(them,them,D)` or a `CHK(them,me,C)` guard); 12 (μ 0.0010)
  read `CHK(them,me,D)` or `CHK(them,^C,D)` as the other disjunct and defect against FairBot and PrudentBot, whose
  generic D certificates satisfy it: a rival sub-family.
- **PBN contains anti-gentle members.** 144 of 619 PBN spellings (μ 0.011 of 0.049) defect against the K detector,
  e.g. `if(CHK(them,^C,D),C,D)`: cooperate only with those certified to defect against CooperateBot. Mutual with
  PrudentBot, they punish gentleness; they are the detector's predators inside the PrudentBot network.

### 2.4 Validation

- **ε = 0, no grudge rule, world L reproduces stored runs draw for draw** (`validate.json`): the realizable-scaling
  (200, 64) S-nonself runs, replicates 0 and 1, to generation 1,000 (21 checkpoints each, P(C,C) and type counts); the
  Pangaea fission–fusion cell (100, 128) merged at 200, replicates 0 and 1, to 1,000 (60 checkpoints each, P(C,C) and
  present types); the annealed rain cell (200, 8) at K = 3, replicates 0 and 1 (generations 200 and 1,000: type counts
  and every island's holder). **0 differences.**
- **Grudge types are recycled** (a free list); the merge orders types by base type, so recycling cannot change a
  trajectory (the first version ordered by id and diverged after the merge in the validation; fixed before any cell).
  Consistency (counts, dictionary, free list) is a test.
- Tests: the grudge is sound, self-fulfilling and keyed to the bare source; inert for non-readers and negated readers;
  every logged write followed (writer C, target D) in that encounter's play and never targets the writer's own spelling;
  lists never exceed the cap; gmode 0 holds only the empty list; sham lists never change a play.

### 2.5 Deviations and conventions (declared before any cell)

1. World K (§1.3) for every grudge arm; L is the reference.
2. The write trigger is "cooperated and was defected against in the encounter's (pre-production) play"; mutual
   defections write nothing (§1.4).
3. The cap is 3 keys, FIFO (oldest evicted), not LRU; the cap-16 diagnostic of §1.6 is dropped (the kernel interns
   lists of at most 4 keys), and the prewritten oracle is the perfect-memory bound.
4. Checkpoints every 10 generations to 1,000 and every 50 after (not 5): "stays out ≥ 25 generations" is evaluated on
   them; window statistics use the checkpoints inside the 500-generation window.
5. Network removal in a merged population = extinction (the predictions' convention). Before the merge a network's share
   is the mean over islands (islands are equal-sized).
6. The post-merge tail is defined for the merged population as a whole (N = 12,800, t₀ = 6,400, A = 52 or 156
   arrivals); on (200, 64) islands per island as in the annealed run (A = 52, t₀ = 100). Arrivals carry no grudges.
7. Part A residents sit at the detector's K natural unit with empty lists; the predator arrives as an E unit under the
   arm's rule; the island is closed (I = 1); a run stops at establishment (≥ N/2), loss, or 1,000 generations.
   Predators: the top three K predators above.
8. The matched counterfactual replays of §1.5 run after the cells, on samples, from a rerun of the same seed to the
   window's start (the kernel is deterministic); they are labelled as such.
9. *Probes before the counted cells:* rep 0 of B1_KG_e0, B1_K0_t3, B2_KG_t1, Cff_KG_e0, Cff_KG_t1, Cis_KG_e0, Cis_KG_t1
   and Cff_L_e0 ran as timing probes (to 2,000 or 10,000 generations); Part A was probed on 7 single runs. The runs are
   deterministic, so the counted rep 0 equals the probe; I saw, for example, that B1_KG_e0 rep 0 ended with DET at 1.000
   and B1_K0_t3 rep 0 with DET extinct by 2,000. Nothing in the design or predictions was changed after the probes.

### 2.6 Costs and the drop order

Probes: a Part A run takes 0.01–0.1 s (N ≤ 3,200); a fission–fusion run to 10,000 takes 1.5–3 min (B1_KG_e0 187 s,
Cff_KG_t1 114 s), an island run (200, 64) about 1.7 min. Projected: A ≈ 3,700 runs ≈ 0.3 worker-h; B 200 runs ≈ 8
worker-h; C 240 runs ≈ 7 worker-h; reference 20 runs ≈ 0.7 worker-h; replays ≈ 1 worker-h: **≈ 17 worker-h, about 6 h on
3 workers, under the 24-hour line: nothing is dropped.**
