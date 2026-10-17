# Spec: legitimate detectors: can a gentle network become unexploitable by a grudge rule, and what decides it against PrudentBot's?, 2026-10-17

Status: draft by the RE (Fable); to be reviewed by gpt-6.1-sol and gemini-4-argon; to be run by an Opus subagent.
The RS's proposal (DEFERRED 1, 2026-10-17): detectors are a legitimate network, gentler than PrudentBot; to survive
they must evolve certificates that let them detect predators; state sponsorship is removed; network removals are
judged by cause, and abundance alone is not a good reason. REJECTED.md checked: nothing re-opened.

## The RS's statements (verbatim, registered)

> Detectors seem like a perfectly legitimate network in and of themselves- in fact, they're even gentler than
> prudentbot! They're exploitable, so if we wanted to keep em around we'd need em to evolve certificates that
> predators detect. Worth an experiment imo

> "Outnumbered networks die" makes me worry we're rigging the odds - "good reasons" to kill off network factor thru
> dynamics in robust ways.

## Why

The certified-defection detector `if(or(CHK(them,them,D),CHK(me,them,D)),D,C)` cooperates by default and defects
only on certified evidence (the partner certified to defect against itself, or I certified to defect against the
partner). It never exploits unconditional cooperators (gentler than PrudentBot), its cooperation is on the default
branch and uncertifiable (so FairBot and PrudentBot defect against it, and it is a rival), and it is exploitable by
programs that defect against it without certified evidence (predator mass ≈ 0.0057). A **grudge rule** gives it the
missing evidence: after an encounter in which the partner defected, the program produces a certificate that it
defects against the partner's source, appended and inherited. For a detector that certificate is self-fulfilling (its
defection is conditional on it), so a lineage retaliates against a predator's copies after one strike while never
defecting first. The rule is uniform: every program may run it; for programs that do not read `CHK(me,them,D)` the
certificate is inert.

## Design

**Machinery.** `src/removing_rivals*.py` (predator classifier, rain kernel), `src/pangaea*.py` (fission–fusion, r = 100),
`src/annealed*.py` (the schedule), `src/realizable_scaling*.py`, `src/provenance*.py` (import only; a new kernel copies
and extends production with the grudge rule). Cached tables copied read-only or rebuilt; reproduction verified first.

**Static (notes §1, before any cell).** The detector family's spellings and mass; the play matrix among detector
spellings, against the PrudentBot network, against FairBot variants, against unconditional cooperators, and against
its predators; whether the grudge certificate is derivable and checkable by the realizable checker (which rule
certifies "I defect against X" for a program whose defection is conditional on that certificate; if the checker needs
a self-hypothesis rule, state it and its soundness argument), its production cost in steps, and whether S-nonself's
gate interacts with it; which other families read the grudge certificate.

**Cause labels (frozen before any cell).** Every island or network removal is labelled: *predation* (a lineage that
strictly exploits the residents reached ≥ 0.5 before the island changed hands), *inefficiency* (the losing state had
P(C,C) < 0.95), *prudence premium* (the winner's edge came from exploiting third parties, e.g. PrudentBot feeding on
unconditional cooperators in a mixed island), or *abundance* (migration or merge majority with none of the above).

**Cells.**
- **A, predator assays.** Forced detector islands at N ∈ {200, 800}; single predator arrivals (each of the top
  predator spellings), with and without the grudge rule; establishment probability per arrival and grudges written.
- **B, head-to-head at equal mass.** Fission–fusion (128 islands of 100, merge at 200), founders split 50/50 between
  the detector network's spellings and the PrudentBot network's spellings (by their prior proportions within each
  network), plus (B2) the same with each network at its natural prior share of the seed; each with and without the
  grudge rule, at ε = 0 and with the light post-merge annealed tail (K = 1 tuned to anti-punishers, onset at the merge).
  No sponsorship. 20 runs per cell.
- **C, natural seeds under L, unsponsored.** Fission–fusion and (200, 64) islands, with and without the grudge rule,
  ε = 0 and with the tail; detector-held islands and networks over time, removals by cause.
- **Reference:** the sponsored PrudentBot founder in C's fission–fusion cell only.

**Statistics.** Winner per run and the cause of every removal; detector share and PrudentBot share over time; grudges
written (by whom against whom; any between members of the same network is a false grudge); predator establishment per
arrival; universal-open and the share held by each network; efficiency reported, never selected on.

**Scale guard.** ≤ 3 workers; the per-root run uses up to 3: check `ps` first; one job per process. Drop order: B2's tail
cells, then C at (200, 64), then the reference.

## Required outputs

`src/detectors.py` (+ `_kern.py`, `_run.py`, `_report.py`), `tests/test_detectors.py` (the grudge certificate is
sound and self-fulfilling for detectors and inert for non-readers; the rule never fires without an observed defection;
ε = 0 without the rule reproduces stored runs), `notes/detectors.md` (§1 static, cause labels, hand predictions; §2
costs), `runs/detectors.md` and `.json`, predictions committed before any counted cell with the RS's statements first,
and the usual hand-back.

## RE predictions (with falsifiers)

1. **The grudge rule cuts predator establishment** [revised after review: with vertical-only inheritance a predator
   meets O(N) unmarked detectors]: with vertical inheritance alone establishment falls by at most half at N = 800; with
   horizontal copying of grudges among detectors it falls to ≤ 0.05 at both N. *Falsifier:* horizontal copying ≥ 0.15.
2. **No unjustified grudges** [revised after review: scored against encounter traces]: every grudge is written after
   a defection that actually occurred, and no grudge is ever written between two programs that cooperate with each other
   in every reachable certificate state. *Falsifier:* any unjustified grudge.
3. **At equal mass without a tail the winner is a coin flip by abundance** (detector wins in 0.3–0.7 of runs, causes
   labelled abundance) with or without the grudge rule. *Falsifier:* outside [0.2, 0.8].
4. **With the tail and no grudge, PrudentBot wins by predation** (≥ 0.8 of runs, most detector removals labelled
   predation); **with the grudge, back to near a coin flip**. *Falsifier:* PrudentBot ≤ 0.6 without the grudge, or
   ≥ 0.9 with it.
6. **Counter-predictions registered.** *Sol:* protection depends on inheritance coverage, encounter rate and source
   diversity, not a universal bound; outcomes are path-dependent rather than coin flips; tail predators removing
   detectors would not make PrudentBot a predator. *Gemini:* with vertical-only inheritance establishment stays ≥ 0.15
   at N = 800; with the tail and grudges PrudentBot still wins ≥ 0.75 of runs, removals shifting from predation to
   prudence premium (the tail feeds it unconditional cooperators).
5. **At natural prior shares PrudentBot wins by abundance and prudence premium** (its seed mass is larger and it feeds
   on unconditional cooperators the detector spares), whatever the grudge rule. *Falsifier:* detectors win ≥ 0.3 of
   natural-share runs.

## Amendments after review (gpt-6.1-sol and gemini-4-argon; these supersede the text above where they conflict)

1. **Soundness is a go/no-go gate.** Before any cell, an executed derivation shows the grudge certificate is sound in
   the realizable checker: for a reader whose defection is conditional on it, the certificate certifies a true
   statement; it is bound to the bare program source (certificate lists stripped, as `EQS` does), the evaluation budget
   and the partner's bare source; adversarial non-readers and negated readers are tested. If no sound derivation
   exists in the current checker, the run stops and reports why, rather than adding an unsound rule.
2. **Keying and transmission.** Grudges key on the partner's bare source, so acquiring certificates does not evade them.
   Two transmission modes, both reported: *vertical* (inherited by the victim's descendants only) and *horizontal*
   (grudges also spread by the existing skeleton-copying machinery among programs that read them). Protected versus
   unprotected detector mass is logged over time.
3. **Controls.** Sham grudges (same cost and inheritance, checking disabled); prewritten valid grudges (an upper bound
   separating certificate efficacy from production and transmission); exact-source versus fresh synonymous predator
   arrivals; repeat-encounter frequency and grudge coverage.
4. **Causes.** Descriptive event labels with overlap allowed and an "unresolved" label, in a frozen precedence order for
   the headline (inefficiency, then predation at ≥ 0.3 of the island strictly exploiting the modal resident, then
   prudence premium, then abundance); for a sample of removals, matched counterfactual replays that suppress the
   suspected exploitative payoff edge or third-party prey with arrivals held fixed.
5. **Costs.** Grudges held per program, evictions under the bundled LRU cap of the per-root run if lists exceed it, and
   verification steps per detector check; verification exhaustion recorded apart from ecological loss.
6. **Scope.** Finite-size mechanism tests; a cheap retaliation scaling diagnostic (A at N ∈ {200, 800, 3,200}) before any
   size claim; support and transition structure reported, including unresolved coexistence; exact binomial intervals.
7. **Framing (for THEORY, recorded by the RE).** A grudge certificate is episodic memory carried as a gene: the
   experiment tests whether gentle networks need reputation across lineages, a step from one-shot source reading
   toward repeated-game structure, and the write-up says so.
