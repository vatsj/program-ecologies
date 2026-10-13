# Spec: the social organization game, fully realizable: identity admitted, production refused against self, no host service, 2026-10-13

Status: draft by the RE (Fable); to be reviewed by gpt-6.1-sol; to be run by an Opus subagent. Follow-up to RESULTS
"The social organization game over the realizable language", "Provenance" and the RS's decision of 2026-10-13
(DEFERRED 1: the realizable arm admits `eq`; the seed lottery is the object).

## Why

The distribution line has one gap left under the standing rules. The realizable social organization run reached the
fair wage on every run and held it on half the islands, but with two idealizations the later runs removed: a free
host service wrote every certificate, and the grammar had no identity. Under the rules now in force (production
refused against self, `eq` admitted) three things change and are worth measuring together. (i) Production is
endogenous and costly in a three-player game whose certificates are already heavy-tailed, so the first question is
feasibility: does the fair coalition still establish when its members must write their own certificates against
non-self partners within the match's fuel? (ii) Identity enters both roles. A worker that strikes only beside exact
copies of itself is a union as a greenbeard, perfectly coordinated and parochial; a boss that pays fair only to
exact copies of a known militant is a closed shop. Do identity cliques help the fair wage (coordination) or hurt it
(the unread slot's scab is now a stranger the boss cannot distinguish)? (iii) The three-player cost model is the
one realizability gap still open (DEFERRED 11): per-encounter verification cost, with production added, against
the fuel.

## Design

**Base.** The realizable social organization run (`src/sog_realizable*.py`: K₃, the path tactic, the lottery law,
the founding-coalition mass, the fakers classification) with: production modes H (the reference) and
**S-nonself₃** [after review, specified for triples]: a program produces a certificate for an encounter only when
*every other participant's* source differs from its own (a worker's coalition certificate is about "I strike beside
w2 against b", so an identical coworker would make it self-play-only; the gate is on both the boss and the other
worker), the tactic as code with cap P = K/4, run after the play in the residual budget, the lack rule, inheritance;
the certificate's target is the actual encounter's quotes, and non-producibility claims (prediction 2) are
established statically before any cell. The grammar of both roles extended by `eq(me, w2)` / `eq(me, them)` atoms (one
node) and by the named quote ⌜T₁⌝ in boss probes; K = 10⁶, V = K/4. [after review] **Lumping correctness:** source
identities and certificate inventories are retained in the population state (as in the provenance run); classes
merge only where no program in either role's catalogue, including `eq`- and ⌜T₁⌝-readers, distinguishes two
spellings and their inventories, with tests on distinct-source twins and on identical sources with different
inventories. [after review] **Arms isolate identity:** besides H + no eq and H + eq, a **matched-prior identity-disabled
control** (the `eq` atoms replaced by a sham literal at equal node cost, so the prior's mass over open militants and
concessions is the same as with `eq`), and an **eq-without-⌜T₁⌝** arm, so that identity's effect is separated from
prior dilution and from the named quote.

**Named classes.** The fair coalition (D\*, T₁, T₁); **the greenbeard union** U_eq = `if(eq(me, other), strike-iff-
wage < ½, work)` (strike only beside an exact copy); **the closed shop** B_eq = pay ½ iff w1 is ⌜T₁⌝ exactly, else 0;
the exclusive militant (strike unless the boss certifies fair *and* the other worker is an exact copy); the
world-0-free fakers of the realizable run (none expected); the unread-slot scab.

**Static** (before any cell): class counts per role with `eq`; the prior mass of the greenbeard union, the closed shop
and the open militant family; the founding-coalition mass with and without the identity classes; hand plays of
the named triples; which certificates each named class can produce against non-self partners (the greenbeard
union's strike certificate against a non-copy is "work", so its coalition certificate exists only beside a copy:
can it ever be written under S-nonself?); the per-encounter cost model: verification steps (checks and their
nested probe checks) plus production steps, as a distribution over the L-weighted triples, with the fraction
exceeding K at K ∈ {3·10⁵, 10⁶, 3·10⁶}.

**Lottery** (the realizable run's law: islands of one boss and two worker populations, N = 100 per slot, I = 64,
mN = 1, horizon 2,000, 40 runs per cell, run-level uncertainty, unresolved runs extended to 10,000): arms **H + no
eq** (the realizable run's cell, rerun on paired seeds), **H + eq**, **S-nonself + no eq**, **S-nonself + eq** (the
fully realizable cell), and **S-nonself + eq at (200, 64)** (20 runs, finite size). Report: fair establishment and
persistence, the wage distribution over islands, the share of fair islands held by open militants vs greenbeard
unions vs mixtures, the closed shop's share of the boss slot, identity islands (either role), exits of fair
islands classified (unread-slot drift, boss cut, false certificate, timeout, substitution, production failure),
the production statistics (acquisitions, waiting, cap timeouts, self-play-only certificates: 0 expected under
S-nonself), cross-island P(fair) and cross-island compatibility of unions, and the cost model realized
(per-encounter steps against K, fraction of encounters that time out).

**Executable dynamics** [after review: the feasibility verdict requires executable dynamics, since timeouts change
play, acquisition and selection]. The S-nonself₃ cells run on executable dynamics at K = 10⁶ (production and
verification steps charged, timeouts playing the default), on a **reduced support** if the full executable table is
infeasible: the support is the classes with prior mass ≥ 10⁻⁴ plus every named class and every class present at
seeding in the paired H runs, and the reduction is validated on sampled executable trajectories (≥ 200 encounters
replayed whole). Ideal-table results, where run, are labelled separately and never carry the feasibility verdict.
[after review] **Definitions fixed before any cell:** establishment = first check at which some island's modal play
is (½, W, W); persistence = the fraction of islands fair at the common horizon 2,000 (the 10,000 extension is a
separate column); plurality = the wage with the largest island share; holder classification by play, with the
holder's source identity reported; productive efficiency (no strikes, no whacks) reported separately from wage
fairness. [after review] **Forced coalitions:** the fair coalition forced on an island with empty inventories, and
with valid preloaded certificates, to separate bootstrap failure from the inability to sustain cooperation.
[after review] **Costs:** uncensored required-cost estimates (what a completed production or verification would
cost) reported separately from capped execution costs, failed attempts, and amortized production expenditure per
lineage. [after review] **Local transition assays:** unread-slot substitution, boss replacement and union invasion
at the fair state, each as a forced one-step transition with the causal sequence classified, beside the final-exit
classification.

[after review by gemini-4-argon] **Support and gate.** The executable reduced support includes the union of all
initial founders across the 40 paired seeds plus at least one distinct-source copy or synonym of each named militant
and concession class, so that non-self production is always syntactically possible when seeded. Production
"starved by play/verification" (K − play steps < production steps ≤ P) is logged separately from "exceeded P". The
S-nonself₃ gate refuses production whenever w1 = w2, which penalizes homogeneous worker slots after fixation (a
post-fixation certificate deadlock: an uncertified militant entering an island fixed on its own spelling can never
produce); a diagnostic arm **S-nonself-opp** requires non-self only against the opponent (b ≠ w1 for a worker;
either worker for the boss), the static analysis says which gate blocks which named triples, and a forced assay of
one uncertified T₁ entering a fixed-T₁ island runs under both gates. Gemini's counter-prediction to RE 2 is scored:
"U_eq holds < 0.05 of fair islands even in H + eq, because both worker slots must co-fix the same spelling"; RE 6's
conditioning may then be vacuous, so B_eq's invasion fitness on resident compositions is reported unconditionally
as well.

**Scale guard.** Report class counts, the executable support's cost and the production universe's size before any
cell; if the `eq` grammar exceeds 2,000 classes per role, drop the named-militant quote and report it as a
different experiment. ≤ 3 workers; kill pool children by pid before any driver.

## Required outputs

`src/sog_full.py` (+ `_run.py`, `_report.py`), `tests/test_sog_full.py` (the `eq` atoms in both roles; the greenbeard
union's and closed shop's hand plays by whole runs; S-nonself production in the three-player setting on the named
classes; the cost model on a sample), `notes/sog-fully-realizable.md` (§1 the grammar extension, the named classes'
hand plays and producible certificates, the coalition masses, the cost model's definition, before any cell; §2
costs), `runs/sog-fully-realizable.md` and `.json`, a predictions file from the spec committed before any counted
cell, the usual hand-back (draft RESULTS, REJECTED, THEORY §3 and §9 item 12 / DEFERRED 6, 10, 11 edits, NOTATION, ≤ 5
lines, branch name, commits).

## RE predictions (with falsifiers)

1. **Feasibility:** under S-nonself the fair coalition still establishes on ≥ 0.8 of runs (H: 40/40), with
   establishment delayed by ≤ 2× and ≤ 10% of encounters timing out at K = 10⁶. *Falsifier:* establishment ≤ 0.5,
   or timeouts ≥ 25%.
2. **The greenbeard union cannot write its coalition certificate under S-nonself** (its strike beside a non-copy is
   "work", so the only certificate of a coordinated strike is self-play-only), hence it holds ≤ 0.05 of fair islands
   in the S-nonself + eq cell, while under H + eq (free certificates) it holds ≥ 0.2. *Falsifier:* ≥ 0.15 under
   S-nonself, or ≤ 0.05 under H.
3. **Identity's effect on persistence has an uncertain sign, and it does not act through B_eq's unread slot**
   [revised after review: B_eq reads w1, so substituting w2 leaves its wage unchanged]: against the matched-prior
   identity-disabled control, H + eq changes persistence by ≤ 0.1 in either direction; the local assays show the
   unread-slot substitution leaves the closed shop's wage unchanged and acts, if at all, through the open boss D\*
   (whose cut after a scab is neutral, as in the realizable run); any identity effect runs through worker-side
   coordination (greenbeard unions) or boss replacement. *Falsifier:* a persistence change ≥ 0.25 against the
   matched control, or the unread-slot assay showing a strict B_eq cut.
4. **The fully realizable cell is still fair on a plurality of islands:** S-nonself₃ + eq persistence ≥ 0.3
   (realizable run 0.53), with zero-wage plurality ≤ 0.2 and productive efficiency ≥ 0.9. *Falsifier:* persistence
   ≤ 0.15, or zero wage ≥ 0.5.
5. **The cost model: modest median overhead, failures in the tail** [revised after review]: production adds ≤ 2× to
   the L-weighted median per-encounter cost, while the failures (cap timeouts, failed attempts) concentrate in the
   top decile of required cost; the fraction of triples whose required cost exceeds K = 10⁶ is reported, with
   static evidence, and no fixed tail multiple is claimed. *Falsifier:* production ≥ 4× the median, or failures
   spread uniformly over the cost deciles.
6. **Closed shops are conditionally fit** [revised after review]: B_eq's invasion fitness on actual resident
   compositions is positive on islands held by exact-T₁ unions and negative elsewhere, so its share of the boss slot
   exceeds its prior share in cells where greenbeard unions hold ≥ 0.2 of fair islands and not otherwise.
   *Falsifier:* B_eq above 2× its prior share in a cell with greenbeard unions ≤ 0.05 of fair islands, or below
   its prior share where they hold ≥ 0.2.

The RS is invited to add predictions; this run closes his distribution line under the rules he set, and the
uncertain ones are 2 and 3.
