# Spec: from arm T to a length prior: the reader mass a length prior gives, and the reader mass the dynamics needs, 2026-11-08

Status: reviewed by gemini-4-argon (folded [after review]) and gpt-6.1-sol (`--mode amended`, folded [after second
review]); run by a Sonnet
subagent on Daytona. Queue 75. The RS asked (2026-11-08) "how do we get from 'arm T works' to 'using the Solomonoff
prior'?"; the RE proposed the three-step path below; the RS: "Sgtm", accepting the RE's default reference machines.

## Context

Queue 74 (RESULTS "Majority division in the current object"): in the current object (seed lottery, annealed tail,
I = 64, migration mN = 1) arm T lands in V\* at N = 100–400 (1.000 / 1.000 / 0.999 at Λ = 100) while the length-prior
DSL arm M does not (0.80 / 0.48 / 0.45). T's library prior is hand-set: constants 0.90, single-partner readers 0.06,
two-partner readers 0.03, exploiters 0.01, no Trojan bullies (`churn_primary_t.FAMILY_WEIGHT`). T's constants alone (T0)
fall with N like M (0.83 / 0.73 / 0.26), so the readers carry T (T − T0 = +0.74 at N = 400). M's failure is the founding
supply of ⅓-naming constants and Trojan bullies (clean founders: 0.975 at N = 200).

The OH doc (h03, RS 2026-11-02): the founding and mutation priors are the length prior of the language; the language (the
reference machine) is the free parameter, checked across reasonable choices; the library prior is the exception to
justify or replace with a length prior over the real syntax. By the invariance theorem the library prior is itself a
length prior of some machine (one where those 27 programs are short), so the question is quantitative: how much reader
mass does a reasonable machine give, and how much does the dynamics need?

What is known about the gap: in L_T^code the library's constants are 4 nodes, single-partner readers 18–23, two-partner
readers 32–42, exploiters 23 (`churn_primary_t.library()`, `sog_realizable.term_nodes` counting) over 18 constructor
tags (`lt_code.py:28-35`). In the n ≤ 10 `dollar3` DSL, churn-capable reader classes carry about 10⁻³ of a slot and
two-partner readers are absent (`notes/churn-primary.md`). No enumerator of raw L_T terms exists (DEFERRED 11 chose
templates); the queue-24 "expanded-syntax" prior was over template spellings and gave 0/40.

**What it is for.** It measures, on a finite grid, how the reader threshold moves with N and I and where a length
prior's reader mass sits against it. [after second review: the two readings below are competing hypotheses about scaling,
not an exhaustive dichotomy; conclusions are stated for the tested grid] Hypothesis (i): the threshold behaves like an
absolute copy count (≈ I·N·δ), so a small positive mass suffices in large enough worlds and the realizability measure is
the world size; hypothesis (ii): it behaves like a fraction, so a length prior far below it fails at every tested size. It also says whether the length prior's Trojan bullies, which sank M,
appear in L_T at a mass that matters.

REJECTED.md checked. Re-opens nothing; it is not the queue-24 expanded-syntax comparison (that was over templates and a
different game).

## Step 1 (static): the length prior over L_T syntax for `dollar3`

**Reference machines** (RS default, 2026-11-08):
- **R0, L_T as it stands:** the 18 term tags of `lt_code.py`, programs in the arm-T frame `lam me. lam n. lam p. body`
  (only `body` is drawn), reading through `(capk 400 (run 400 n p) me)` and its mirror as written out in full.
- **R1, L_T plus a read primitive:** R0 plus one tag `readn` / `readp` (arity 0) that evaluates to the named partner's
  output code under the same cap and charge, so a single-partner reader is a few nodes. R1 brackets how short reading
  can be; R0 brackets how long.

**The prior.** A branching-probability model on terms [after second review: masses are products of probabilities, not
integer code lengths]: each node draws its tag uniformly among the machine's tags (arity fixes the tree); de Bruijn
indices and `nat` literals n ≥ 0 are drawn with the Elias-γ probabilities of n + 1; `quote` carries its term. Mass(term) =
product of the per-node probabilities. Ill-typed or stuck terms stay in the prior (as junk); pruning is only an
enumeration shortcut, and pruned mass is counted, not dropped; the prior is a semimeasure (mass of infinite trees is lost; report it).
[after review] Before enumerating, compute the expected arity of a uniformly drawn tag; if the branching process is
supercritical, report class masses both raw (semimeasure) and conditional on a finite tree. The Elias-γ code makes small
output codes cheap (code 0 = (next, ⅓) is a ⅓-naming constant): report the induced constant law; it is a property of the
machine, not corrected.
The output convention is kept: anything not in 0–8, out of fuel or stuck plays code 8 (ALL, ⅔) and is charged A_f
(P_fail = 0.1 per failed read and per forfeit). [RE note: under a length prior, junk mass maps onto code 8 by this
convention, so it can dominate the (ALL, ⅔) constant's mass; report junk separately from the true constant.]

**Behaviour classes.** [after second review] Classify by output *and* charge signature (failed reads and forfeits per
encounter, since A_f makes them selection-relevant); junk is split by cost class (forfeit; failed reads; plain default).
Then check a sample of 10³ non-junk sampled programs against each other (not only against the library probes): a
program's assigned family must reproduce its sampled interactions, else it is reported as "other". Probe set: the 9 constants as partners in both other
slots (81 profiles), plus the 27 library programs as partners (27² profiles), in each of the three slots. Families,
behavioural, as in `majority_tail.dsl_family_data` translated to L_T: constants (by code), junk (forfeits or code 8 by
default), fair single-partner readers, two-partner readers, Trojan bullies ("if j names me at ⅓, name j at ⅔, else name
k at ½"), exploiters, yielders, other conditionals.

**Estimation.**
1. Exhaustive enumeration up to the largest size s₀ reachable in the budget (target s₀ ≥ 9 nodes for R0, with type and
   arity pruning), exact class masses to s₀.
2. Above s₀: (a) plain Monte Carlo from the prior for classes with mass ≥ 10⁻⁶ (constants, junk); (b) for reader,
   bully and exploiter classes, the shortest spellings found by size-ordered targeted search and the count of spellings
   at the minimal size and the next two sizes: a **lower bound** on class mass. [after second review] Without a
   certified bound on the residual mass of longer spellings, every rare-class conclusion is one-sided (a reader share of
   at least so much), and the join says so.
3. Report per machine: the mass of each family, the reader / constant mass ratio ρ_R, the bully / reader ratio β, the
   shortest reader and bully, the lost (infinite-tree) mass, and the junk mass.

## Step 2 (dynamic): the reader mass the dynamics needs

[after review] Step 2 has two series. **2a (main grid)** keeps T's constant proportions, for comparability with queue 74.
**2b (length-prior shaped)**, the one step 3 joins: for each machine, [after second review: normalized] junk at its
measured mass j, split into junk programs by cost class (J_f: always code 8, charged one forfeit; J_r: code 8 after one
failed read), readers at total δ with single- and two-partner readers at the **measured** within-reader ratio, bullies at
βδ (β measured), exploiters at the measured exploiter/reader ratio times δ, and constants taking the remaining mass in
their measured conditional proportions; families the step-1 prior has but T⁺ lacks ("other conditionals") are omitted
and their mass reported. N = 200 and 400, I = 64, the δ grid below. The join is therefore a **projection of the length
prior onto T⁺'s behaviours**, not a sampled length-prior arm, and is labelled so.

The queue-74 simulator (`src/majority_tail*.py`), arm T, mN = 1, Λ = 100 tail drawn from the same law as founding,
horizon 100N + 20N chase, CRN as in queue 74. New: a two-parameter seed law over an extended library T⁺ = the 27
programs plus Trojan bullies written in L_T (two per slot direction, as in the DSL), with
- constants at their main-dose within-family proportions, total 1 − δ − βδ − 0.01·δ/0.09 (exploiters keep their ratio to
  readers),
- readers (single- and two-partner at the main 2 : 1 ratio) at total δ,
- bullies at total βδ.

Grid (2a): δ ∈ {2·10⁻¹ (where δ(1 + β + 1/9) ≤ 1) [after review], 10⁻¹, 3·10⁻², 10⁻², 3·10⁻³, 10⁻³, 3·10⁻⁴, 10⁻⁴}; β ∈ {0, 0.3, 1, 3}; N ∈ {100, 200, 400}; I ∈ {64, 256};
20 runs per cell. **Threshold:** δ\*(N, I, β) = the smallest δ on the grid with mean V\* share ≥ 0.9 at 120N (interpolated
in log δ between the bracketing grid points; reported with the bracket). Also: δ\*'s dependence on N and I, and the
expected reader copies per world at threshold, c\* = I·N·δ\* (founders) and I·Λ·δ\* (tail).

[after review] Two cheap slices: (i) N = 200, I = 64, β = 0, single-partner readers only (no two-partner readers,
which a length prior makes far rarer); (ii) at the δ just above δ\*(200, 64, 0), founders at δ with a reader-free tail,
and founders reader-free with the tail at δ, to say which copy count binds.

[after second review] **Matched copy counts:** add cells holding I·N·δ fixed at c ∈ {64, 640} founder copies per world
across (N, I) ∈ {(100, 64), (200, 64), (400, 64), (100, 256), (200, 256)} (β = 0), and cells varying founder and tail
reader doses independently at c = 64; near-threshold cells (the two grid points bracketing δ\*) continue to 240N. δ\* is
interpolated only where V\* is monotone in δ across the bracket; non-monotone dose responses are reported as such.

**Cut order** (record before running): I = 256 at N = 400 first, then β = 3, then δ = 10⁻⁴ at N = 100. Budget ceiling
300 sandbox-CPU-hours (queue 74 used 18 for 740 jobs).

## Step 3 (join)

For each machine, compare the length prior's (ρ_R, β) with δ\*(N, I, β): the smallest (N, I) on the tested grid at which
δ_LP ≥ δ\*, where [after review] δ_LP is the reader share of the prior conditional on finite terms (junk, i.e. forfeits
and default code 8, included in the denominator), and δ\* is taken from series 2b (the length-prior-shaped law); if none, the (N, I) at which the fitted
c\* law would reach it, labelled extrapolation. This is the claim the RS asked for, stated per machine.

## Validations

- **V1:** with δ and β set to T's main dose (δ = 0.09, β = 0), N = 100 and 200, mN = 1, Λ = 100, runs 0–39 reproduce
  the stored queue-74 rows exactly.
- **V2:** the new bully programs in L_T behave on the probe set exactly as the DSL bully's definition; the extended
  table T⁺ reproduces the 27-program table on every triple of library programs.
- **V3:** the step-1 enumerator's mass for the 27 library terms equals the code-length formula; total enumerated mass
  plus lost mass plus mass above s₀ sums to 1 within 10⁻⁹ (exhaustive part).
- **V4:** behavioural classification of the 27 library programs by the probe set returns their library families.

## Predictions (the RE's; copied to `predictions/2026-11-08-length-prior-t.md` before any counted cell)

- **RE 1 (the threshold is a copy count in N).** At I = 64, β = 0, δ\* falls with N by a factor ≥ 1.5 per doubling
  (N = 100 → 200 → 400). Falsifier: a factor < 1.2 per doubling at both steps.
- **RE 2 (and in I).** At β = 0, δ\*(N, 256) ≤ δ\*(N, 64) / 2 at N = 100 and 200. Falsifier: ratio > 0.8 at both.
- **RE 3 (bullies raise the threshold).** At N = 200, I = 64, δ\*(β = 1) ≥ 3·δ\*(β = 0). Falsifier: < 1.5×.
- **RE 4 (R0 is far below).** Under R0, ρ_R ≤ 10⁻⁸ (readers are ≥ 14 nodes longer than constants at ≈ 1/18 per node),
  and β ≥ 0.3 (bullies are the same size as fair readers). Falsifier: ρ_R > 10⁻⁶ or β < 0.1.
- **RE 5 (R1 brackets it).** Under R1, ρ_R ≥ 10⁻³. Falsifier: < 10⁻⁴.
- **RE 6 (join).** Under R0 no tested (N, I) reaches δ\*; under R1 some tested cell does at β = the measured R1 bully
  ratio. Falsifier: the reverse in either machine.
- **gemini-4-argon's counter (recorded, scored):** β < 0.05 under both R0 and R1 (a bully needs an extra comparison and
  two distinct branches, 3–5 more nodes than a fair reader).
- **gpt-6.1-sol's counters (recorded, scored):** RE 1–2's thresholds do not collapse onto one copy count across N and
  I (scored: the matched-count cells' V\* spread exceeds 0.2 at c = 64 or 640), and the improvement with I is weaker
  than RE 2 asserts (ratio > 0.5); RE 4's 10⁻⁸ bound stays unsupported (scored: only a lower bound on ρ_R is obtained,
  above 10⁻⁸ or not certified below it).
- **RE 7 (junk).** Under R0, junk (forfeits and default code 8) carries more than half of the prior's mass. Falsifier:
  < 0.25.

## Required outputs

- `predictions/2026-11-08-length-prior-t.md` (before any counted cell; pilots disclosed).
- Step 1: `src/lt_prior*.py` (enumerator, sampler, targeted search, behavioural classifier), `runs/lt-prior.md` and
  `.json` (per machine: family masses with how each was obtained, ρ_R, β, shortest spellings, lost and junk mass).
- Step 2: extensions to `src/majority_tail*.py` for the T⁺ law, `runs/length-prior-t.md` and `.json` (V\* per cell with
  bootstrap-over-runs intervals, consensus counts, δ\* table with brackets, c\* table, transition rates in the tail window
  and chase at the 0.25·N debounce), rows under `runs/length_prior_t/`.
- Step 3 in the same report.
- `tests/test_lt_prior.py`; `notes/length-prior-t.md` with every deviation and the budget record.
- Drafts for the RE: a RESULTS section, REJECTED entries, NOTATION entries.

## Caveats known in advance

- A length prior over a hand-chosen tag set is still a machine choice; R0/R1 bracket one axis (the cost of reading),
  not all.
- Class masses above s₀ are bounds or estimates, not exact.
- The dynamic step keeps T's 27-program behaviours plus bullies; a length prior also brings other conditionals, which
  the "other conditionals" mass in step 1 reports but step 2 does not simulate.
- Finite schedules; the threshold is a finite-schedule statistic, not π.
