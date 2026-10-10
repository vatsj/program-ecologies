# Spec: the social organization game over the realizable language: does a library-rich prior make the concession cheap, and does the seed lottery then reach the fair wage?, 2026-10-10

Status: draft by the RE (Fable); to be reviewed by gpt-6.1-sol; to be run by an Opus subagent after the identity-and-tags
run reports. Follow-up to RESULTS "Concessions: a boss grammar with probes" and "The realizable language, milestone 2",
and to the RS's restatement of the prior question (DEFERRED 10, 2026-10-06: "how do we design a prior that lets us
cheaply point at good programs?") and his decision of 2026-10-10 (DEFERRED 1: the seed lottery is the object).

## Why

In the modal social organization game the concession "pay fair to those who would strike if paid low" works as a
mechanism and vanishes under the length prior, because the two-probe boss D\* is a 439,209-function grammar away from
a constant (mass 10⁻⁸ against 0.1). The RE's operating frame for the prior is description length in a language with a
public library of general-purpose primitives. Over the realizable language with milestone 4's library (quotes,
evaluation, a sound checker, carried certificates), a probe is one check atom and D\* is about seven nodes, so under
the same 2^−nodes prior it is 2⁻⁶ of a constant, not 10⁻⁷. Two further things change in the realizable setting and
are worth measuring on their own: (i) certificates are facts about actual runs, with no Kripke world structure, so
the *world-0 probe fakers* of the modal run (probes vacuously true at the bottom world) have no counterpart; (ii) the
one-slot leak (a one-wage boss protects only the slot it reads) is a property of the game and should survive. The
run asks whether the seed lottery, now the object, reaches and keeps the fair wage under a library-rich prior with no
mass tilt, which the modal run could not (0/40 under length-prior seeds).

## Design

**Game.** The committed social organization game of RESULTS "The union game" / "Concessions" (boss wage s ∈ {0, 1/4,
1/2} and whack h ∈ {none, 1, 2} at cost c = 0.5, loss L = 1; two workers work/strike; payoffs as there; CC commitment
as main, RR as one cell), played by L_T^code programs: the boss runs `b ⌜b⌝ ⌜w1⌝ ⌜w2⌝` and each worker runs
`w ⌜w⌝ ⌜b⌝ ⌜other⌝`, each under fuel K = 10⁶, timeouts scoring as the game's default (pay 0 / work) and reported.

**Certificates for three-player runs.** Milestone 4's checker and tactic (`src/lt_cert.py`) extended to roots built
from three quotes; atoms ⟨w ⌜w⌝ ⌜b⌝ ⌜o⌝, K⟩⇓a and ⟨b ⌜b⌝ ⌜w1⌝ ⌜w2⌝, K⟩⇓(s, h). The notes' §1 must state the extended
rules with their obligations and re-prove Theorem S^cert for three-quote roots (the pair rule's symmetry argument
has to be restated: a worker's check of the boss's script and the boss's check of the worker's script are the two
validations; the second worker is a quoted parameter). Probes are check atoms about *quoted constant* opponents:
`CHK(w1, ⌜pay(s)⌝, ⌜w2⌝, strike)` ("w1 is certified to strike against a boss paying s beside w2") and
`CHK(b, ⌜me⌝, ⌜w2⌝, pay ≥ 1/4)` ("the boss is certified to pay me at least 1/4"). Production by the frozen tactic,
public and not charged (DEFERRED 11's operating hypothesis).

[after review] **Three-player soundness gates the run.** The pair rule's symmetry is not a routine extension: the
boss's check and a worker's check concern different programs, different outputs and (for probes) counterfactual
opponents. The notes' §1 must state the exact shared predicate that two mutual checks compute, prove that every
accepted certificate implies the *actual fuel-bounded root's* output (Theorem S^cert₃), and show by test that
slot-2 argument ordering, opponent substitution (a certificate about a quoted constant opponent is not a certificate
about the actual one), unequal branches, and exhausted fuel are handled: corrupted instances of each kind rejected by
the checker term and the host replay. **Timeout and substitution safety** are stated as separate lemmas: a militant
that times out plays the default (work), which is a low-wage work with no false atom; the report classifies every
low-wage work as false certificate (a soundness failure), timeout, or substitution (a probe about a constant boss
read as if about the actual one). No counted cell before this passes.

**Template grammar.** Bosses: `pay(s, h)` constants (9); `if(B, A, A)` over probe atoms about w1 and w2 and the
`whack(j)` outputs; named: D₀ (zero-wage probe, pay 1/2 iff w1 certified to strike at 0), D\* (probes at 0 and
1/4, read on w1), D\*₂ (both slots, if it fits the cutoff; else noted), the whacker `pay(0, strike-targeting)`.
Workers: `work`, `strike`; `if(CHK(b, ⌜me⌝, ⌜o⌝, pay ≥ s), work, strike)` (militant family: T₁ at s = 1/2, T₀ at
s = 1/4); militant⁻ "strike unless certified fair" = the s = 1/2 member; the scab; QUORUM-type `if(CHK(o, ⌜b⌝, ⌜me⌝,
strike), strike, work)`. Cutoff n = 7 for both roles (prespecified; n = 6 is the fallback and a different experiment).
Lumping identity-aware as in `specs/2026-10-10-identity-and-tags.md`. [after review] **The prior is a source
distribution:** L puts 2^−nodes on every *source* (spelling) of each role's grammar, normalized per role; a class's
mass is the sum over its sources, classes being proven interaction-preserving (no program in either role's catalogue
distinguishes two merged sources, within-class plays included); source multiplicities are retained for drift (the
twin-expanded distribution); the report gives representative-length and aggregated masses separately. U (uniform
over classes) as the control. [after review] **Matched expanded-syntax control:** the same executable programs and
the same interactions re-encoded in a syntax where the library's primitives are inlined (a probe spelled as the
check wrapper's body rather than one atom), with the 2^−nodes prior on *that* syntax; the lottery is run on the
same classes under that prior, so that the difference between the two priors on identical dynamics isolates
library richness from everything else that changed (language, certificate semantics, faker availability, free
production).

**Static.** Class counts per role; the 3-player play table (boss class × worker class × worker class) by composition
of clean check values (Lemma N) validated against whole runs on a sample; the named states' plays (the fair state
(D\*, T₁, T₁), the zero-wage state, the whacking state); **fakers**: boss classes that get work from a militant at a
wage below 1/2 (Lemma 0 analogue: should be none by soundness), and specifically whether any class reproduces the
modal "probe wage faker" (pay 1/2 where the probe is vacuously true); strict invaders of the fair state in each slot;
the one-slot leak (neutral substitutes of the unread worker slot); the unfakeable fair state (D\*-type with
militant⁻ in both slots) and its strict invaders. The prior masses of D₀, D\*, T₁, militant⁻ and the constants, with
the ratios against the modal run's (9.7·10⁻⁹ / 0.1025 for D\*). [after review] **The transferable quantity:** the
**mass of compatible, executable founding coalitions**, i.e. for every (boss class, worker class, worker class)
triple that is a fair state with no strict invader among the classes present, the product of the three masses,
summed; reported under L, under the expanded-syntax prior, and under U, beside the modal run's value, and
decomposed into seed occupancy (P(a coalition is co-seeded on an island)), establishment conditional on occupancy,
and survival after establishment. Actual execution costs and certificate-production costs are recorded separately,
with a fuel sweep (K ∈ {3·10⁵, 10⁶, 3·10⁶}) on the named states and on adversarial near-cap programs.

**Lottery** (primary; `src/sog_lottery.py` conventions, frozen in notes §1 [after review]: islands of one boss slot
population and two worker slot populations, N = 100 per slot, I = 64, iid seeds from the role priors, Moran updating
with payoff-weighted selection and migration mN = 1 exactly as in RESULTS "The social organization game under the
seed lottery", horizon 2,000; **fair island** = wage 1/2 and both workers working as the island's modal play for
10 consecutive checks; **establishment** = first check at which some island is fair; endpoint E3-type with mixtures
on an island scored by the closure rule of milestone 2; **run-level uncertainty** only: 40 runs per cell with Wilson
intervals on run-level outcomes and run-level means with bootstrap intervals for island fractions, never pooled-island
intervals): L (main) and U at (100, 64); L at (200, 64) and (100, 256); the expanded-syntax prior at (100, 64); CC
main, RR at (100, 64) with the RR play table derived first (rationality includes the whack decision and the
opponent-dependent continuation); no mass tilt in the main cells, plus one militants-in-numbers tilt as the link to
the modal run. [after review] **Controls:** forced matched seeds of D\* against D\*₂ (same worker seeds), followed by
migration-off persistence assays of the established fair islands (residence time); a matched-mass faker-removal
control and a concession-ablation control (D-family bosses nulled, mass preserved), to separate better seeding from
better protection. Report: establishment, persistence, residence time of fair islands (migration on and off), the
concession bosses' share of the boss slot over time, zero-wage and whacking shares, the three-role threshold
(minimum share ≥ 1/6), cross-island P(fair) kept distinct from efficiency and from cross-island compatibility,
censoring and hazards, and for every fair island that dies, the exit (unread-slot drift, false certificate, timeout,
substitution, boss cut, migration). [after review] **No truncation by mass in the main cells:** the three-player table
is evaluated lazily on encountered triples (with a cache); if a truncated worker catalogue is ever used it is a
separate experiment with the omitted mass reported, and the named adversaries are retained regardless of mass.

**Chain** (diagnostic): the ε→0 chain at N = 10⁴ under L (closure-seeded `chain_log` with the cut diagnostic), for π's
wage distribution and the fair state's exits, to compare with the modal run's 0.0020.

**Scale guard.** Report class counts per role and the lazy table's expected size before any cell; ≤ 3 workers;
kill pool children by pid before the driver. [after review] **Pre-registration order:** the predictions file is
committed after the calculus (§1.1–1.2) and the grammar (§1.3) but *before* the static invasion analysis; any
prediction added after the static tables is labelled conditional on them.

## Required outputs

`src/sog_realizable.py`, `src/sog_realizable_run.py`, `src/sog_realizable_report.py`, `tests/test_sog_realizable.py`
(three-quote roots in the checker and the host replay; corrupted three-player certificates rejected; the named
states' plays by whole runs; the play table by composition vs whole runs on a sample), `notes/sog-realizable.md`
(§1 the extended calculus and its soundness, the grammar, the named classes' hand plays, the prior masses and their
ratios to the modal run, the hand-derived fakers and the one-slot leak, before any cell; §2 costs),
`runs/sog-realizable.md` and `.json`, a predictions file from the spec committed after §1 and before any counted
cell, the usual hand-back (draft RESULTS, REJECTED, THEORY §3 and §9.9 / DEFERRED 6, 10, 11 edits, NOTATION, ≤ 5
lines, branch name, commits).

## RE predictions (with falsifiers)

1. **The library makes the concession cheap.** Under L, D\*'s mass is within 2⁻⁸ of a constant boss's (my bet 2⁻⁶)
   and the militant T₁'s within 2⁻⁴ of the constant striker's. *Falsifier:* D\* below 2⁻¹² of a constant.
2. **No false-certificate faker** [revised after review]: no boss class gets work from a militant at a wage below
   1/2 through an accepted false atom (0 by soundness), and no class reproduces the modal probe wage faker; low-wage
   work that does occur is by timeout or substitution, and each case is classified. *Falsifier:* a false-certificate
   faker; a substitution faker is a miss of the design (the probe semantics), recorded separately.
3. **Establishment is set by the founding-coalition mass, and the library raises it** [revised after review]: the
   mass of compatible executable founding coalitions under L exceeds the modal run's by ≥ 10³, and establishment
   conditional on co-seeding is ≥ 0.5; the unconditional establishment fraction at (100, 64) is my bet, not a
   derived number: ≥ 0.6 within 200 generations (modal run 0/40), with the expanded-syntax prior at ≤ 0.2 on the
   same dynamics. *Falsifier:* coalition mass within 10× of the modal run's, or establishment conditional on
   co-seeding ≤ 0.2, or the expanded-syntax prior establishing at least as often as L.
4. **The one-slot leak survives, so persistence is partial.** The run-level mean fraction of islands fair at the
   horizon is between 0.2 and 0.6, and the dominant exit of dying fair islands is unread-slot drift followed by a
   boss cut (≥ 0.5 of exits). *Falsifier:* persistence ≥ 0.8 (the leak is gone) or ≤ 0.1, or the dominant exit a
   false certificate.
5. **D\*₂ (both slots), if it fits, lengthens residence** [revised after review]: the migration-off residence time of
   islands held by D\*₂ with militants in both slots is ≥ 5× that of D\* islands on matched seeds, and that state has
   no strict invader; persistence with migration on is higher than D\*'s but need not exceed 0.9. *Falsifier:* a
   strict invader of that state, or residence within 2× of D\*'s.
6. **RR keeps the 1/4 wage,** conditional on the derived RR play table showing that the 1/4 probe certifies no
   rational worker: wage 1/4 on ≥ 0.7 of islands (modal run 0.90). *Falsifier:* fair ≥ 0.3 of islands under RR; if
   the derived table shows the 1/4 probe certifying rational workers, the prediction is void and the table is the
   result.
7. **The chain still says zero wage** (diagnostic): π(fair) at N = 10⁴ ≤ 0.1 under L. *Falsifier:* ≥ 0.3.

The RS is invited to add predictions; this run is the test of his prior question, and the uncertain ones are 3 and 4.
