# Spec: the realizable language, milestone 2: populations of carriers (does the modal arm's result survive in a Turing-complete language with the prover as code?), 2026-10-06

Status: draft by the RE (Fable); to be reviewed by gpt-6.1-sol; to be run by an Opus subagent. Follow-up to RESULTS
"The realizable language, milestone 4" (DEFERRED 11, operating hypothesis for milestone 2; DEFERRED 1 for the two
objects). The prior is partly the RS's decision (DEFERRED 10/11): both candidate priors run as arms, and the RS's
answer, if it comes, selects the main arm.

## Why

Milestones 1–4 are single-pair results. The program's claim since the modal arm is about populations: a sound
source-reader family enters neutrally, is unfakeable, and wins the seed lottery ("almost all seeds") while in the
ε→0 chain its cooperative odds grow with N (∝ N^0.44 in the modal arm; the weak arm falls like N^−1/2). Every one
of those results used a free sound oracle. Milestone 4 gives, for the first time, a realizable family that
cooperates across distinct sources: carriers over one shared sound checker, with scripts produced by a frozen
tactic and checked in 1–4·10⁴ steps. The question is whether the population results transfer: do carriers
establish from iid seeds, is the chain's exit the shadow's neutral drift (∝ 1/N) with no faker, and what the new
conventions (the checker entry, the call skeleton, the certificate list) do to the population.

## Design

**Language and fuel.** L_T^code with the milestone-4 library (`src/lt_cert.py`), the sound checker at entry 0 (and
the sound copy at entry 5 for the convention control), K = 10⁶, V = ⌊K/4⌋. Play = the actual run of `p ⌜p⌝ ⌜q⌝`
under K; a timeout is ⊥ and scores as D for the payoff (the PD payoffs of the modal arm, w = 0.3 as in
`src/modal_limN.py`).

**Template grammar** (the operating hypothesis of DEFERRED 11). A program is an s-expression over: constants `C`,
`D`; atoms `CHK(p, q, a)` with p ∈ {them, me}, q ∈ {me, them, ⌜C⌝, ⌜D⌝}, a ∈ {C, D} ("the checker certifies that p's
run against q's quote returns a"); connectives `if`, `and`, `or`, `not`; nesting to a node cutoff n, nodes counted
one per constant, atom and connective (so `if CHK(them, me, C) then C else D` is CB at 4 nodes and the prudent
carrier CBP is 7). [after review] **The cutoff is prespecified:** n = 7, the smallest containing CBP, the
two-atom prudent and bridge shapes and their D-branch siblings; the fallback is n = 6, and a fallback run is a
*different experiment* reported as such, never as confirmation of a prediction made for n = 7. Report the class
count and the structural diagnostics (establisher mass, compatible establisher pairs, shadow mass, bridge mass)
for both catalogues. Each program's **certificate list** is produced by milestone 4's frozen tactic for its own
call skeleton (C and D scripts, opponent-generic); skeletons the tactic cannot produce for get no list, and their
number and mass are reported, with the production effort (tactic nodes, host time) per skeleton measured
separately. [after review] **Lumping is exact over spellings:** two spellings merge only if their action rows *and
columns* against every original spelling of the catalogue agree, including self and cross-twin cells (certificates
can depend on the opponent's exact skeleton, so equality against retained representatives is not enough); the
prior mass of a class is the explicit sum over its spellings; and the twin-expanded distribution (IMPLEMENTATION 4)
is verified to reproduce an unlumped chain on a small sub-catalogue (n ≤ 5) before any counted cell.

[after review] **Scope.** This is a finite template ecology run inside a Turing-complete evaluator, with
certificates supplied by an external frozen tactic. It tests executable verification in populations, not
unrestricted program evolution or endogenous certificate discovery; the write-up says so. **The prior is
specified completely:** under L a program's weight is 2^−(nodes) normalized over the catalogue, with the
certificate list free under P and one node under O, and the entry label under E one node for `CHK_5` and zero for
`CHK_0` (so entry 0 is the default spelling and entry 5 a costlier one; the equiprobable variant is a second cell);
under U every lumped class has equal weight.

**Priors, as arms.** (L) the length prior on node counts (the standing μ); (U) uniform over lumped classes (the
"policy prior" of DEFERRED 10). The RS's decision selects the main arm; absent it, L is main.

**Production, as arms.** (P) public: every program carries the scripts the tactic produces, at no node cost (the
library is public, so is production); (O) optional: the list is a grammar choice `none | produced` costing one node,
so certificate-less spellings of every skeleton exist (CB0-type programs, which carriers refuse).

**Checker entry, as a control.** (E) the atom carries the entry, `CHK_e` with e ∈ {0, 5} equiprobable under both
priors, so carriers on the two sound entries coexist in the grammar (they are (D, D) with each other, milestone 4).

**Static.** The class catalogue with representative spellings; the play table; establishers (self-C and D on D)
with their prior mass; compatible establisher pairs; shadows of each establisher (classes on-path identical to C
against the incumbent and entering neutrally: Ccert-type programs and C itself) with mass; the sucker fringe
(CBdef-type: cooperates where sound readers defect); **classes exploiting an establisher** (allowed by soundness:
an arbitrary Boolean template may cooperate for reasons other than certified opponent cooperation, so an
establisher can be exploited without any false atom; list each such pair with the reason) [after review]; **bridges**
(classes cooperating with carriers on both entries under E, enumerated before the E cells) [after review]; the leak
test (drift-closed components at the cutoff, as in RESULTS "K at n = 8"); the per-match step cost by class pair and
the fraction of plays that time out at K = 10⁶, with every non-cooperative cell classified as false certification
(a soundness failure), failed certification, or timeout. [after review] **Matched ideal-verification control:** the
same sources, certificates, cutoff and priors with checks answered by the host replay checker at no step cost
(milestone 4's host oracle), so that the difference between the two tables isolates executable verification from
the grammar change. [after review] **K sensitivity:** the decisive cells (the top cooperative state's exits and
the establishers' mutual plays) recomputed at K = 3·10⁵ and 3·10⁶ with V/K fixed.

**Chain** (ε→0, `src/chain_log.py` with closure-seeded discovery): N ∈ {10³, 10⁴, 3·10⁴, 10⁵} [after review: a
fourth point, or the decisive fixation-rate asymptotics derived from the decisive edges' Δ, since three nearby
points give a local slope and not an exponent]; arms L×P (main), U×P, L×O, L×P×E. Report P(C,C), π(all-D), support,
transition structure, the top cooperative state's exit with its rate's N-scaling (the exponent of cooperative/D odds
in N, against the modal arm's 0.44 and K at n = 8), and the decisive edges' Δ and N·Δ so that "neutral" and
"strict" are read off; say where the slope could be a crossover rather than an asymptote.

**Lottery** (ε = 0, `src/islands.py` conventions as in RESULTS "Almost all seeds?"): (N, I) = (100, 64), mN = 1,
40 seeds per arm for L×P, U×P, L×O [after review: optional production may act on establishment rather than on π]
and L×P×E. [after review] **Endpoint defined for the ε = 0 process:** an island is *resolved* when it is
monomorphic in a class that no class present anywhere in the run can invade under the actual migration process
(computed from the play table: no present class has a strictly higher payoff against the island than the incumbent
has against itself, and the incumbent does not drift to any present class with higher payoff against the residents);
a run *succeeds* when every island is resolved in a cooperating class; a run *fails* when every island is resolved
and some is non-cooperating or when a non-cooperating class is fixed globally; otherwise it is *right-censored* at
the horizon (2,000 generations) and reported as such, never as success or failure. Polymorphic islands at the
horizon are censored. Wilson intervals on 40 runs resolve 0.9 only coarsely; the report states the interval, and
the prediction is scored on its interval. For E, the fraction of runs ending with both entries alive is reported
with the caveat that a horizon snapshot shows metastability, not permanent coexistence; the separation hazard is
estimated from the merge times where merges occur.

**Scale guard.** Report the catalogue size, the play-table time at K = 10⁶ and the chain's class count before any
chain; if the play table exceeds 2 hours at 3 workers, drop the cutoff by one and say so. ≤ 3 workers.

## Required outputs

`src/carrier_populations.py` (grammar, enumeration, production, lumping, play table), `src/carrier_populations_run.py`
and `_report.py`, `tests/test_carrier_populations.py` (grammar counts, lumping exactness on a sample, play table vs
milestone 4's cells for the named carriers), `notes/carrier-populations.md` (§1 the grammar and its counting, the
named classes, the hand-derived establishers and shadows before any cell; §2 costs), `runs/carrier-populations.md`
and `.json`, a predictions file from the spec committed after §1 and before any counted cell, the usual hand-back
(draft RESULTS, REJECTED, THEORY §9.2 and DEFERRED 1/2/10/11 edits, NOTATION, ≤ 5 lines, branch name, commits).

## RE predictions (with falsifiers)

[after review: the numerical clauses are kept as the RE's bets but the predictions are scored on their
mechanism clauses; a number missed with the mechanism intact is recorded as a miss of the number.]

1. **Almost all seeds, realizably:** under L×P the lottery's success interval excludes 0.5 and the point estimate is
   ≥ 0.8 (my bet: ≥ 0.9), with establishment within 100 generations in most runs; the winning classes are CB- and
   CBP-shaped carriers. *Falsifier:* the success interval excluding 0.7 from above, or a run won by a non-carrier.
2. **The chain transfers by the same mechanism:** under L×P the top cooperative state's exit is neutral drift into a
   shadow (Ccert-type or C) followed by D's strict entry, ∝ 1/N, and no exit is N-independent, so P(C,C) rises over
   the N range (my bet for the local odds slope: [0.3, 0.6], against the modal arm's 0.44). *Falsifier:* an
   N-independent exit out of the top cooperative state, or P(C,C) falling over the range.
3. **No false atom, but exploitable establishers** [split after review]: (a) 0 false accepted atoms in the whole
   table (soundness); (b) for the hand-proved subclass (CB-, CB1- and CBP-shaped carriers over entry 0) no class
   strictly exploits them except through a shadow; (c) at least one establisher *outside* that subclass (a Boolean
   template cooperating for a reason other than certified opponent cooperation) is strictly exploited. *Falsifier for
   (a):* any false atom; *for (b):* a strict non-shadow entry into a CB/CB1/CBP population; *for (c):* no exploited
   establisher in the catalogue.
4. **Optional production is a defector tax, not a shadow:** under L×O certificate-less spellings are refused by
   carriers, so they enter no carrier population neutrally; P(C,C) at 10⁴ is lower than under L×P (my bet: by at most
   0.15) and the exponent keeps its sign; in the lottery L×O's success is lower than L×P's by establishment, not by
   π. *Falsifier:* a certificate-less spelling entering a carrier population neutrally, or the exponent changing sign.
5. **The checker entry is a convention; bridges decide separation** [revised after review]: under E, bridges (classes
   cooperating with carriers on both entries) exist in the catalogue only as unconditional cooperators (C, Ccert)
   or as two-atom `or` templates, and every bridge is a shadow of one side (exploitable); so the chain puts ≥ 0.9
   of cooperative π on one entry at every N and the lottery ends with both entries alive on a positive fraction of
   runs (my bet ≥ 0.3), metastably. *Falsifier:* a non-shadow bridge (a class cooperating with both entries and not
   strictly invaded by D) stable on an island, or cooperative π split between entries at ≥ 0.3 each at N = 10⁵.
6. **The prior does not flip the verdict here** (unlike concessions): U×P and L×P are both cooperative at N = 10⁴
   (P(C,C) ≥ 0.5 in both), because carriers are the bulk of the lumped classes under either prior. *Falsifier:* one
   arm ≥ 0.5 and the other ≤ 0.2.
7. **Executable verification costs a constant, not the mechanism** [added after review]: the matched
   ideal-verification table differs from the executable table only in timeout cells (plays whose checks exceed V at
   K = 10⁶), and the chain's P(C,C) under the ideal table is within 0.1 of the executable one at every N. *Falsifier:*
   a cell differing for a non-timeout reason, or a P(C,C) gap above 0.25.

The RS is invited to add predictions. The uncertain ones are 2 (whether the exponent survives the per-match step
cost and the timeouts) and 5 (whether two sound checkers can coexist on one island).
