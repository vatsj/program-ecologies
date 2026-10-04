# Spec: three-player majority divide-the-dollar with separate slot populations, 2026-10-04

Status: reviewed by gpt-6.1-sol (`reviews/2026-10-04-three-player-dollar-gpt-6.1-sol.md`) and revised; changes are
marked [after review]. Committed before launch. To be run by an Opus subagent.

## Why

The RS wants the selection process judged as a social choice system: does stochastic stability over source-reading
programs select democratic outcomes (equal shares, grand coalition) or dictatorial ones (a pivot extracting rent, or a
majority cutting out a minority)? The PD cannot ask this, since everyone agrees on the best outcome. The three-player
majority divide-the-dollar game has an empty core: every allocation can be beaten by a two-player coalition. Fixed slots
with separate populations make the externalities real. `ROLE` is not used: it internalizes the externality by fiat.

## The game

Three slots, 1, 2, 3. Each slot submits an action (partner, demand):
- partner ∈ {the other two slots, ALL};
- demand ∈ {1/3, 1/2, 2/3}.

Outcome rule:
- A **pair** forms if two slots name each other and their demands sum to at most 1. Each gets its demand; the third slot
  gets 0. Any unused surplus is wasted.
- The **grand coalition** forms if all three name ALL and demands sum to at most 1, which on this grid means (1/3, 1/3,
  1/3).
- Otherwise every slot gets 0.

Nine actions per slot. Efficient outcomes: the pairs (1/2, 1/2, 0), (2/3, 1/3, 0) and their permutations, and the grand
coalition at thirds. Pairs at (1/3, 1/3) waste a third.

## Populations and programs

- Three separate populations, one per slot, each of size N, fixed roles. A slot-1 program only ever meets a slot-2 and a
  slot-3 program. So there is no self-play and no self-recognition clique: coalitions must be built by reading the
  *partner's* source or behaviour.
- Programs are binary: they observe the two opponents. This is the k-player extension of THEORY §9.9: payoffs form a
  3-tensor, programs are (k−1)-ary, enumeration is the cost.
- **Encounter semantics** [after review]. An encounter is an ordered triple (p₁, p₂, p₃). A program in slot i is
  evaluated in the encounter, and its applications refer to the *current encounter* with one substitution:
  - `THEM_j(ME)`: slot j's action in the current encounter (the recursive self-reference);
  - `THEM_j(^A)`: slot j's action in the encounter where slot i is replaced by the constant action A, with the third slot
    unchanged;
  - `THEM_j(THEM_k)`: slot j's action in the encounter where slot i is replaced by slot k's program (k the third slot).
  Slot indices are absolute, so argument order is fixed by slot. Divergent self-reference resolves to the minimax action,
  which here is any disagreement action with payoff 0. Modal atoms are `BOX(THEM_j = a)` for an action a, in the current
  encounter, at the PA and PA + Con(PA) levels as in `src/modal.py`. The subagent must test relabeling invariance: permuting
  slot labels must permute payoffs, class counts and π exactly.
- Two arms, if feasible:
  - **weak arm** (simulation), extending the ultimatum game's multi-level action handling (`src/run_ult.py`);
  - **modal arm** (provability).
  If only one arm fits the budget, run the modal arm: the coalition question is cleaner without fakers.
- Prior: the same length prior as the other arms, per slot. The subagent must state the language sizes and class counts at
  each n before choosing n. Expect n ≤ 5. [after review] Conclusions are language-relative: a neutral bridge may exist
  only above the n run. State that with every verdict.
- **Baseline** [after review]: the nine constant actions alone, as the ordinary bargaining-coordination control.

## The ε→0 object

[after review] Order of limits: ε → 0 at fixed N gives the embedded chain over monomorphic triples; N then varies over
{100, 10³, 10⁴}. A mutation hits one slot, chosen uniformly; its fixation is computed within that slot's Moran population
of size N with the other two slots fixed, under f = exp(w·payoff), w = 0.3.

[after review] **Frequency independence.** A slot-i program's payoff depends only on the two opponent residents, never on
other slot-i programs, since there is no self-play. So within a slot, mutant and resident payoffs are constant in the
mutant's frequency: fixation is the exact constant-selection Moran formula, ρ = (1 − 1/r)/(1 − r^(−N)) with r the
fitness ratio, 1/N for neutral mutants, and no interior rest points exist. Polymorphic states arise only by neutral
drift. The subagent should use the closed form and report analytic large-N rates.

Report:
- π over triples, with support and the transition structure.
- [after review] **Currents, not "cycles".** The chain is finite and irreducible, so π exists. Rule 4 applies to
  *probability currents*: report the net directed flow π(a)P(a,b) − π(b)P(b,a) among coalition states, the dominant
  metastable sequences, and a mixing-time estimate. "Rotation" means a consistent nonzero circulation around the three
  pair states.
- The mass on each outcome type: grand coalition at thirds; fair pair (1/2, 1/2, 0); unfair pair (2/3, 1/3, 0); wasteful
  pair; disagreement.
- [after review] **Distribution statistics at encounter level.** Mean slot share is efficiency/3 by symmetry and is only
  a check. Report instead: E[max_i x_i] over π (thirds → 1/3, fair pair → 1/2, unfair pair → 2/3); the exclusion
  probability (some slot gets 0); and coalition persistence (expected dwell in each coalition type, in mutation events).
- Efficiency: expected total payout.
- For each monomorphic efficient triple: entry rate from disagreement, exit rate, the neutral-bridge prior mass (μ of
  neutral entrants that open a strict exit two steps on), and the static invasion table by slot.
- [after review] Order of operations: commit `predictions/` with the RE's numbers *before* computing invasion tables;
  language sizes and class counts are the only static numbers allowed before the commit, since invasion tables already
  reveal the outcome.

## Agent-based check

[after review] Three seeds per cell. N = 100 per slot, mutation 10⁻³ per birth (εN = 0.1 per slot per generation),
10⁵ generations, from a uniform-random seed and from the grand coalition, labelled as approach rates. Report the time
series of outcome types, dwell times with intervals across seeds.

## RE predictions (Fable)

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

**What it would mean.** If 1–5 hold, stochastic stability over source-reading programs with fixed roles gives
*rotating majorities*: no single fair state is stable, and the fairness is only in the time average. Democracy would then
need something beyond the pure chain, for example an intolerance of coalition defection, the analogue of PrudentBot, or a
correlating device. If the grand coalition instead holds (falsifying 2 and 5), the three-way Löbian handshake is more
drift-resistant than the two-player network, and that is worth a theorem. [after review] Rising grand-coalition mass
would not by itself establish drift-closure; the neutral-bridge mass and exit rates decide that.

## RS predictions (Jacob)

(To be added if he wants to make them before the run; the subagent does not need them.)

## Procedure for the subagent

Follow CLAUDE.md discipline. Measure language sizes and class counts; write and commit
`predictions/2026-10-04-three-player-dollar.md` carrying the RE predictions above; only then compute invasion tables and
run the chain; at most 3 workers; stop cells projected beyond 2 hours; do not edit RESULTS.md, REJECTED.md, THEORY.md or
CLAUDE.md; hand back draft RESULTS, REJECTED and THEORY text, at most 5 lines on what matters, and the branch and commits.
