# Spec: the realizable language, milestone 5: certificates as genes: endogenous production by search, by copying, and charged, 2026-10-11

Status: draft by the RE (Fable); to be reviewed by gpt-6.1-sol; to be run by an Opus subagent. Follow-up to
milestones 3 and 4 and DEFERRED 11 and 12 (the RS's "gene" framing).

## Why

In every realizable-language population so far, certificates are a free host service: a frozen tactic produces
each program's scripts outside the match. Milestone 3 showed that producing a certificate by search costs 10⁵–10⁶
steps and, within a cap, finds only twins; milestone 4 showed that checking a carried script costs 10⁴. So the
realizability gap is production. The RS's framing suggests the route: certificates are genes, and genes spread by
**copying**. A program that meets an opponent whose published script fits its own call skeleton can copy that script
after checking it (the check is what milestone 4 already charges), and carry it from then on. Production then
happens by horizontal transfer with no search, charged at the check's cost, and the population's certificates are
endogenous. The run measures the three production modes against each other, in the single-pair tables and in
populations, and asks whether copy-and-check restores distinct-source cooperation at check cost, what the
production cost as a heritable trait does, and whether copied scripts admit a new faker (a program that carries
scripts it did not produce and cannot honour: refused by soundness, since a copied script is checked against the
carrier's own code, but the refusal costs the checker fuel).

## Design

**Language.** L_T^code with milestone 4's library (`src/lt_cert.py`: the checker CC, the search CORE of milestone 3
as the in-language producer, quotes, `capk`), K = 10⁶, V = K/4. A program is (code, script list, **production mode**),
the mode a trait: **H** (host: the frozen tactic, free, the baseline); **S** (search: the program calls the library
search on its own root query within a declared production cap P ≤ K/2 when it lacks a script for the encounter, and
carries what it finds; cost charged to the match's fuel); **C** (copy-and-check: when the opponent's published list
holds a script for the same call skeleton and outcome, the program checks that script against *its own* code at the
checker's cost and, if accepted, adopts it into its list for later encounters; cost charged); and **CS** (copy first,
search if nothing to copy). Lists persist across a program's lifetime (a per-individual state, as the cache
accounting of RESULTS "K at n = 8" was), and are inherited by offspring under reproduction as part of the genotype
(the RS's gene: a script is heritable and transmissible).

[after review] **The certified object and its soundness.** The quote a program publishes and that others check is
(code, mode, the list *as of the encounter*); the certified proposition is about the fuel-K run of that quoted object
against the quoted opponent at that time. Adoption changes the list, hence the quote, so the notes' §1 must prove
**adoption preserves soundness**: a script accepted against (code, mode, list) remains valid for (code, mode,
list ∪ {script}) because the checker's root and the run it certifies do not read the list beyond lookup (Lemma A), or
state exactly where this fails; tests cover an accepted script followed by a production-induced timeout and by a list
mutation. **Fuel allocation** is stated: production (search or check-for-adoption) draws from the same K as the
match, so a producing program can time out where a non-producing one does not; those timeouts are classified.
[after review] **Steps and payoff:** in the main cells steps only consume the cap (a timeout plays the default), so
"charged" is not a selective price and the ALLC-ladder analogy is *not* claimed there; a separate **price arm**
maps steps to fitness (c · steps/K per match, c ∈ {0.01, 0.1}) and is the only arm compared with RESULTS "Price
scaling paths"; both are reported.

[after review] **Initialization.** C-only with empty founding lists is an invariant (copying cannot create the first
script) and is run once to confirm it; the C-only cells proper use a **declared certificate seed** (a stated fraction
f₀ ∈ {0.05, 0.25} of founders carry H-produced scripts, labelled an exogenous subsidy) and a **single-donor** cell
(one H-carrier introduced per island); CS-only runs with empty lists. Every script in circulation carries its
**host ancestry** (the H-produced script it descends from, by copy or inheritance) beside its most recent
transmission, so "endogenous" is measured as the fraction of held scripts with no host ancestor (S-produced) and the
rest is labelled as host-seeded. **Controls, paired seeds and encounter schedules across arms:** C with publication
disabled (no horizontal transfer), C with inheritance disabled (no vertical transfer), and identical initial
inventories across modes beside empty ones; **the directed script-transfer compatibility graph** (which donor
scripts validate against which recipient codes) is measured before any population cell; repeated invalid-script
encounters with negative-result caching, and the checker burden on both parties, are measured.

**Single-pair tables** (the milestone-4 catalogue: CB, CB1, CBP₄, Vlet, Vwrap, FB2, twins and distinct pairs, SF_k,
the fakers, plus the identity-run's CB with markers): for each mode, the first encounter's play and cost, the second
encounter's play and cost (after adoption), the number of encounters to the (C, C) steady state, and the per-match
cost at steady state; S against the cap P ∈ {K/8, K/4, K/2}; **the copied-script faker** CF (code D, list empty, mode
C: it copies cooperative scripts; does any check accept a copied C-script against D's code? by Theorem S^cert no, and
the cost of the refusal is reported); **the donor's exposure** (does publishing scripts cost a carrier anything? a
copier that adopts a C-script and then defects is impossible by soundness; a copier that adopts and cooperates is a
new partner).

**Populations** (the milestone-2 template grammar at n = 7, production mode as a trait with prior ¼ each; [after
review] **state keyed by (source, mode, certificate inventory)** with the encounter/update ordering frozen (play,
then adoption, then reproduction), lumping only over spellings with identical inventories and transitions; the seed
lottery at (100, 64), mN = 1, 40 runs per arm, horizon 2,000, E3 and holder-based outcomes, run-level uncertainty;
the chain at N = 10⁴ as a diagnostic **labelled a frozen-inventory approximation** since a static table cannot
carry inherited lists): arms **H-only** (the milestone-2 baseline), **mixed modes** (the trait segregating),
**S-only**, **C-only** (seeded and single-donor), **CS-only**. Report: unconditional establishment probabilities with
censoring-aware establishment times, persistence, universal-open, identity islands, the mode composition of
cooperative holders over time, the mean per-match cost by mode, the number of distinct scripts in circulation and
their provenance and host ancestry, and the fraction of plays that time out by mode.

**Costs and scaling** [after review]. Per-match production cost under S is a price on reading only in the price arm;
under C it is a one-time cost per (skeleton, outcome), the cache accounting. No α = 1 conclusion is drawn from one
population size: a **matched size sweep** N ∈ {50, 100, 200} at I = 64 measures acquisition cost per lineage, script
turnover, and encounters before replacement, and the realized per-match cost schedules are reported against RESULTS
"Price scaling paths" as finite-size evidence.

**Scale guard.** The single-pair tables are cheap; the population cells reuse the milestone-2 table where the mode is
H and need per-individual lists otherwise (an evaluator change; report its cost before any cell). ≤ 3 workers; kill
pool children by pid.

## Required outputs

`src/lt_genes.py` (+ `_run.py`, `_report.py`), `tests/test_lt_genes.py` (adoption after a passed check; refusal of a
copied script against a different code; the search producer within P; inheritance of lists; cost accounting),
`notes/certificates-as-genes.md` (§1 the modes' semantics and costs, the copied-script faker argument from Theorem
S^cert, the hand-derived first- and second-encounter plays for the named pairs, before any cell; §2 costs),
`runs/certificates-as-genes.md` and `.json`, a predictions file from the spec committed before any counted cell, the
usual hand-back (draft RESULTS, REJECTED, THEORY §9.2 / DEFERRED 11 and 12 edits, NOTATION, ≤ 5 lines, branch name,
commits).

## RE predictions (with falsifiers)

[after review: success and falsifier ranges meet; an outcome in neither is a miss of the number.]

1. **Copy-and-check restores distinct-source cooperation along verified transfer edges** [revised after review]: a
   distinct pair cooperates under C from the second encounter iff the donor's script is an edge of the measured
   transfer graph for the recipient's code (same call skeleton, script validates against the recipient), and every
   such pair then cooperates at a steady-state per-match cost within 2× of H's; pairs off the graph never do; two
   empty C-carriers never bootstrap each other. *Falsifier:* an on-graph pair that never cooperates under C, an
   off-graph pair that does, or a steady-state cost ≥ 5× H's.
2. **Search alone is twins-only in populations,** as in milestone 3: S-only cooperates only among exact copies within
   P and its lottery success is ≤ 0.2 of H-only's. *Falsifier:* S-only within 0.5 of H-only.
3. **No copied-script faker, under the stated soundness** [revised after review]: CF's copied C-scripts are refused
   against its own code in every cell (0 accepted, by Theorem S^cert plus Lemma A); its fitness is empirical and not
   predicted (refusal may be cheap and CF still earns exploitation payoffs). *Falsifier:* an accepted copied script
   against a code that defects.
4. **H leads during acquisition, then the modes are neutral or inventory-selected** [revised after review]: in the
   mixed-mode population H-carriers establish first (free scripts), C/CS-carriers adopt from them, and by the
   horizon the mode composition of cooperative holders is within 0.2 of the prior's ¼ each among H, C and CS (neutral
   once inventories coincide), with S ≤ 0.1; in the price arm C/CS exceed H. *Falsifier:* H ≥ 0.6 of cooperative
   holders at the horizon in the main cells (a persistent subsidy advantage), or C/CS ≥ 0.8 (my earlier guess of
   systematic dominance).
5. **Seeded C-only establishes later than H-only and persists as H-only; empty C-only never establishes** [revised
   after review]: unconditional establishment under C-only (f₀ = 0.25) is ≥ 0.8 of H-only's with censoring-aware
   establishment times ≥ 2× H-only's; the single-donor cell establishes on ≥ 0.5 of runs; empty C-only 0/40.
   *Falsifier:* seeded C-only establishment ≤ 0.4 of H-only's, or the single-donor cell ≤ 0.2, or empty C-only ≥ 1/40.
6. **Scripts in circulation are few, and their host ancestry is total in the main cells** [revised after review]:
   the number of distinct scripts held at the horizon is ≤ 3× the number of (skeleton, outcome) pairs present (no
   claim on inheritance fraction, which depends on turnover; it is reported with the turnover), and in the C-only
   and mixed cells every held script has a host ancestor, while in CS-only and S-only the host-free fraction is
   positive only among twins. *Falsifier:* ≥ 10× (skeleton, outcome) pairs, or a host-free script held by a
   distinct-source cooperating pair.

The RS is invited to add predictions; the uncertain ones are 4 (whether the host subsidy persists) and 5.
