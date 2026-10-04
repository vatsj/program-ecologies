# Predictions: three-player majority divide-the-dollar with separate slot populations, 2026-10-04

Spec: `specs/2026-10-04-three-player-dollar.md` (reviewed by gpt-6.1-sol,
`reviews/2026-10-04-three-player-dollar-gpt-6.1-sol.md`). Committed before any invasion table, chain cell or
agent-based run. Before this commit only the following were computed: language sizes, canonical-function counts,
behavioural class counts (`src/dollar3_classes.py`, `runs/dollar3_classes*.json`), and evaluator sanity checks
(the relabeling-invariance test, and two hand-built encounters to check the semantics: a Löbian pair handshake and a
cyclic three-way handshake).

## Design choices left to the subagent

### Grammar and cost convention

One grammar per slot, absolute slot labels, every slot's language the image of slot 1's under a slot permutation:

    A ::= a                       9 constant actions, 1 node
        | if(B, A, A)             1 + |B| + |A| + |A|
    B ::= BOX_L(THEM_j = a)       3 nodes
        | not B | and B B | or B B

The atom's 3 nodes are: the box node, with the level L and the tested action a folded in, as BOX, BOXD and BOX1 fold
kind and level in `src/modal.py`; THEM_j; and ME. Here j is an other slot and a is one of slot j's 9 actions. The atom
speaks about the current encounter only, as the spec states. The prior is the length prior of every other arm,
bits = log2 a(|p|) + 2 log2 |p| + 1, per slot. Programs are merged into canonical functions: essential atoms plus a
table of actions.

Nine actions need a selector node, so the smallest conditional program has 6 nodes, not 3 as FairBot does in the PD.
The spec's "expect n ≤ 5" therefore does not carry over: at n ≤ 5 the language is the 9 constants.

### Arms

- **modal** (primary): BOX_L is provability on the linear GL Kripke chain over the encounter, at L = 0 (PA) and
  L = 1 (PA + Con(PA)), with `src/modal.py` semantics. The language has 36 atoms.
- **modalPA**: the same with the PA box only, 18 atoms. It is the grammar of the weak arm, as M0 is W0's in the E1
  matched control.
- **weak**: the same grammar as modalPA, with the atom evaluated by simulating slot j in the current encounter
  (budget iteration from bottom, `src/evaluate.py` semantics). A slot whose value stays bottom diverges and plays the
  minimax disagreement action (ALL, 2/3). That action names no partner, so it gives the divergent slot 0 and does not
  block a pair between the other two.

The spec suggested extending the ultimatum game's k-ary DSL (min/max/flip over ordered levels) for the weak arm. I
did not, because the 9 actions are (partner, demand) pairs with no natural order, and min/max over an arbitrary order
would build in an arbitrary structure. The matched design isolates simulation against provability, as E1 did. Its
limitation: the weak arm has no third-party probes (`THEM_j(^A)`, `THEM_j(THEM_k)`), so it has no fakers. Its
conditional programs can only shadow constants or diverge against each other. The weak-arm verdicts are about
simulation without probes.

- **constants**: the nine constant actions alone (spec baseline), as the ε→0 chain over 729 triples.

### n

**n = 6**, for every arm except constants.
- At n = 6 to 9 the canonical function sets are identical: one-atom conditionals `if(atom, b, c)` and constants. Only
  the prior changes, because longer spellings (`not` chains) of the same functions are added.
- n = 10 adds two-atom conditions, with 23,337 (PA) or 93,321 (PA + Con) canonical functions per slot. The chain over
  triples (K³ states) is then out of reach.
- So n = 6 is the smallest language with any conditional program, and the largest whose triple chain fits the budget.

Every verdict is relative to this language. In particular:
- programs that condition on *both* other slots (a grand-coalition FairBot that needs both partners, "accept the
  better of two offers") first appear at n = 10 and are absent;
- the grand coalition can be held conditionally only by one-atom conditionals, for example a cyclic handshake
  (1 reads 2, 2 reads 3, 3 reads 1) or two readers plus a constant;
- a neutral bridge may exist only above n = 6.

### Language sizes and class counts

Programs of each size, a(s):
- PA (18 atoms): a(1) = 9, a(2–5) = 0, a(6–9) = 1,458 each, a(10) = 53,946, a(11) = 631,314, a(12) = 1,261,170.
- PA + Con (36 atoms): a(1) = 9, a(6–9) = 2,916 each, a(10) = 212,868, a(11) = 2,522,340.

Canonical functions (distinct programs after reduction) and the prior mass on the 9 constants, per slot:

| language | n = 1–5 | n = 6 | n = 7 | n = 8 | n = 9 | n = 10 |
|---|---|---|---|---|---|---|
| PA: canonical | 9 | 1,305 | 1,305 | 1,305 | 1,305 | 23,337 |
| PA: mass on constants | 1 | 0.976 | 0.959 | 0.947 | 0.937 | — |
| PA + Con: canonical | 9 | 2,601 | 2,601 | 2,601 | 2,601 | 93,321 |
| PA + Con: mass on constants | 1 | 0.976 | 0.959 | 0.947 | 0.937 | — |

Behavioural classes at n = 6, per slot. These are computed over all K² opponent pairs (K³ encounters); the
payoff-class relation is the chain's exact lumping.

| arm | canonical | action classes | payoff classes |
|---|---|---|---|
| weak | 1,305 | 1,305 | 903 (slot 1 = slot 2) |
| modalPA | 1,305 | 1,305 | 1,179 |
| modal | 2,601 | 2,601 | 2,475 |

The relabeling-invariance test passes in both evaluators. Under all 6 slot permutations, on 20,000 random triples per
arm, permuting slot labels permutes payoffs and outcome types exactly (0 mismatches). Class counts agree across slots
where computed. π invariance under relabeling is checked after the run.

### The ε→0 object

ε → 0 at fixed N gives the embedded chain over monomorphic triples of payoff classes:
- a mutation event picks a slot with probability 1/3 and draws a mutant class from that slot's prior;
- it fixes with the exact constant-selection Moran probability ρ = (1 − 1/r)/(1 − r^(−N)), where
  r = exp(w(u_mutant − u_resident)), and ρ = 1/N when neutral;
- payoffs are in units of the dollar;
- w = 0.3, N ∈ {10², 10³, 10⁴}.

The state space is K³ (7.4·10⁸ weak, 1.6·10⁹ modalPA, 1.5·10¹⁰ modal), so π is computed on a subset explored from the 729 constant
triples by inflow:
- a state is added when its π-weighted inflow exceeds θ, with θ = 10⁻⁹ unless a cell needs more;
- transitions out of the explored set are folded into the self-loop, which is a reflecting boundary;
- their total π-weighted flow is reported as the cut flow;
- cells with cut flow above 10⁻³ are flagged, and a cell projected beyond about 2 hours is stopped and reported as not
  finished.

Order of runs: constants, weak, modalPA and modal, at N = 10², 10³, 10⁴, at most 3 worker processes.

### Statistics

These follow the spec:
- π over triples, with support and transition structure;
- π mass by outcome type: grand, fair pair, unfair pair, wasteful pair, disagreement;
- efficiency, as expected total payout;
- E[max_i x_i] and the exclusion probability (some slot gets 0), over π at encounter level;
- mean slot share, as a check only;
- net currents between coalition states (grand; each of the three pairs; disagreement), and the circulation around
  the three pair states;
- dwell per visit in each coalition type, in mutation events;
- a mixing-time estimate (relaxation time of the π-weighted lumped chain over coalition types, labelled as an
  estimate);
- for each of the top efficient triples:
  - entry from disagreement;
  - exit rates split into strict, neutral that changes the outcome, neutral that keeps it, and deleterious;
  - the neutral-bridge prior mass: the μ of neutral entrants that open a strict exit to another outcome one step on;
  - the static invasion table by slot;
- analytic large-N rates: strict ρ → 1 − 1/r, neutral 1/N, deleterious ~ (1/r − 1) r^N.

### Operational definitions for the verdicts

- **Drift-closed (P1)**, at depth two. An efficient monomorphic triple is drift-closed if:
  - it has no strict exit and no outcome-changing neutral exit, and
  - no outcome-preserving neutral entrant (in any slot) opens a strict exit, or an outcome-changing neutral exit,
    from the resulting triple.

  I check this for every efficient triple in each cell's explored set and for all efficient constant triples. Any
  closed triple found also gets the depth-three check.
- **Nonzero net current (P2):** the circulation C = J(12→13) + J(13→23) + J(23→12), with |C| at least 1% of the total
  flow among pair states, and not an artefact of slot asymmetry (π is relabeling-invariant, so a circulation has two
  orientations that cancel unless the dynamics prefer one rotation; see the note below).
- **Finite ε (P7):** dwell is the length of a run of a constant dominant-coalition label. The label is the outcome of
  the triple of majority classes, recorded every 10 generations, or "mixed".
  - "Decays into pairs within 10⁴ generations": the encounter-level pair probability first exceeds 0.5 before
    generation 10⁴.

Note on P2. The game and language are invariant under all slot permutations, and a transposition reverses the
direction of rotation around the three pair states. A consistent nonzero circulation would break that symmetry, so
the exact π must give zero net circulation. P2's current clause can then hold only in a finer sense: currents
between pair states *with a given pivot*. I keep P2 as written and evaluate it literally, with C = 0 by symmetry
expected as the literal outcome. I also report the directed flows by pivot role (which pair forms after which, and
which slot moves), which is the meaningful "excluded slot bids for a pivot" structure. This is the subagent's
reading, recorded before the run.

### Agent-based check (finite εN, approach rates, not π)

- Three populations of N = 100, mutation 10⁻³ per birth (εN = 0.1 per slot per generation), w = 0.3, 10⁵ generations,
  3 seeds per cell.
- Two starts:
  - *uniform-random*: every individual an independent uniform draw over the slot's payoff classes;
  - *grand coalition*: all three populations the constant (ALL, 1/3).
- Arms: modal and weak.
- Outcome time series and dwell times are reported with intervals across seeds.

## RE predictions (Fable, verbatim from the spec)

1. **No efficient monomorphic triple is drift-closed at the n run.** For every one, some slot has a neutral entrant (a
   program that plays the same on path but accepts a better offer, or accepts pair offers while in the grand coalition)
   that opens a strict exit. *Falsifier:* an efficient triple with no such entrant. [after review] Sol expects some
   language-dependent trapped networks instead; this is a live disagreement.
2. **Pairs hold most of the mass, with circulation.** At N = 100 in the modal arm, fair plus unfair pairs hold at least
   0.6 of π; the grand coalition holds at most 0.2. There is a nonzero net current around the three pair states, driven
   by the excluded slot bidding for a pivot. *Falsifier:* grand coalition at least 0.5 at any N, or pair mass below 0.4.
3. **The bidding war is capped at the fair pair.** Unfair pairs hold between 0.1 and 0.4 of π, less than fair pairs.
   *Falsifier:* unfair pairs above fair pairs. [after review] Sol notes the cap needs coordination between the excluded
   slot and the low-paid slot; I keep the prediction.
4. **No dictatorship, at encounter level** [after review: restated]. E[max_i x_i] lies in [0.45, 0.60], and the
   exclusion probability is at least 0.6. *Falsifier:* E[max share] above 0.62, meaning unfair pairs dominate.
5. **The grand coalition leaks like the shadow.** Its exits are neutral drift at rate ∝ 1/N into programs that also
   accept pair offers, followed by strict pair formation; its entry from disagreement is neutral at one copy per slot,
   so three neutral steps are needed. Its π share stays below 0.2 at every N. *Falsifier:* grand coalition share above
   0.3 at N = 10⁴. [after review] Sol says the direction is unresolved until entry and exit are compared; both are
   reported.
6. **The weak arm, if run, has more disagreement.** Disagreement mass at least 2× the modal arm's at each N.
7. **Finite ε:** the agent-based runs show pair-to-pair turnover with mean dwell of 10²–10⁴ generations per pair, and the
   grand-coalition start decays into pairs within 10⁴ generations in all three seeds.
8. **Constants-only baseline** [after review]: pairs at (1/2, 1/2) dominate (≥ 0.5), the grand coalition is below 0.1,
   because three simultaneous ALL constants need a three-step neutral path while a pair needs two.

How each is scored:
- P2–P5 in the modal arm (PA + Con, the primary arm), at every N unless the prediction names one;
- P4 at every N;
- P6 compares the weak arm with modalPA (the matched pair) and with modal;
- P1 in every arm;
- P8 in the constants cell (N = 10², 10³, 10⁴).

Conclusions are relative to the language: n = 6, current-encounter atoms only, and one-atom conditionals.

## Subagent's own expectations (not the RE's; recorded for calibration)

- *Constants:* a constant pair (½, ½) has no strict exit, since the excluded slot cannot enter a pair of constants.
  Its only exits are neutral or deleterious, so it should be the main sink. Disagreement states are left strictly at
  N-independent rates.
  - The constant grand coalition has no strict or neutral exit either: a lone deviator gets 0, so every exit costs a
    member 1/3. The fair pair's members would lose 1/2. So among constants the fair pair should be the stickiest
    state, the grand coalition and the unfair pair (whose low side loses 1/3) less so.
  - I expect P8 to hold, with the fair pair taking most of the mass and the unfair pair second.
- *Modal:* conditional readers let the excluded slot buy in. A neutral bridge in a paired slot (accept slot 3's offer
  when it is provable) opens a strict entry for slot 3. So pairs leak at ∝ 1/N, as P1 and P5 say. Whether pairs or
  the grand coalition leak more slowly is the open question, as sol says; I lean to pairs.
