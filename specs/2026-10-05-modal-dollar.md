# Spec: the modal arm on two-player divide-the-dollar, one population: does sound reading rescue efficiency, or help the greedy?, 2026-10-05

Status: reviewed by gpt-6.1-sol (`reviews/2026-10-05-modal-dollar-gpt-6.1-sol.md`) and revised; changes marked
[after review]. To be run by an Opus subagent. Follow-up to RESULTS "Divide-the-dollar partitions".

## Why

In the weak arm, one-population divide-the-dollar loses efficiency in lim_N: an *accommodating shadow* of the fair
convention (`flip(THEM(^S3))`, on-path identical to S3, conceding 1 − d to any constant d) enters neutrally, the
greedy constant S5 invades it strictly, and the S5–accommodator Hawk–Dove polymorphism (efficiency 0.41) absorbs π
from N ≈ 5·10³. Re-entry of the fair demand is deleterious with a barrier growing in N. This is the dilemma's lim_N
failure in a bargaining game. In the PD the modal arm rescued efficiency because a sound reader can cooperate with
provers and punish everyone else, and no faker exists for FairBot's pair (Lemma 0).

[after review] The RE's first draft proposed a rescue program P that accepts a provable greedy demand (1/6 against
S5), exploits provable conceders (5/6), and demands 1/2 against its own kind by the Löbian fixed point. Sol's
objection is decisive and is now the hypothesis under test: **S5 strictly invades a monomorphic P population** with
no shadow needed (S5 earns 5/6 against P, more than P's 1/2 against itself); in the P/S5 subsystem the stable
mixture is x_P = 1/3 with encounter efficiency 5/9. Sound reading *certifies* greed, and the best reply to a
certified commitment is to concede, which rewards it. So in bargaining, correctly recognizing commitment can make
exploitation easier: unfakeability and resistance to profitable certified demands are different properties. The
candidate that survives this objection is a program P′ that **refuses** a certified greedy demand (clashes with
S5, as S3 does), exploits certified conceders (demands 5/6 against an opponent that provably concedes S1 to it),
and demands 1/2 against its own kind; whether it can re-enter the greedy polymorphism (it earns 5/6 only against the
accommodator fraction and 0 against S5) is a static number, not an argument, and the spec makes it a go/no-go
checkpoint.

Caveat for the write-up: the modal arm's box is free and sound; this is the idealized reading as everywhere else.

## Design

**Game.** `dollar5` (`games/dollar5.yaml`). **Role structures:** one population without `ROLE` (primary); fixed
roles (secondary).

**Grammar.** The two-slot restriction of `src/dollar3.py`'s grammar, reusing its evaluator: A ::= a (5 constants)
| if(B, A, A); B ::= BOX_L(THEM = a) (3 nodes; a one of the opponent's 5 demands; L ∈ {PA, PA + Con}) | not B | and
B B | or B B; modal semantics on the GL Kripke chain over the encounter; the **matched weak arm** (simulation atoms,
same grammar, same prior) as the control. Cutoffs: n = 7 (one-atom conditionals) as the baseline for both arms;
n = 11 (the smallest cutoff containing P′ = `if(BOX(THEM = S1), S5, if(BOX(THEM = S5), S3, S3))` and P) if its class
count admits the chain. [after review] If n = 11 does not fit, *augmentation* is a separate arm: add P, P′ and their
policy duplicates as named classes at a swept mass (10⁻⁴, 10⁻³, 10⁻²) to **both** the modal and the weak n = 7
languages with identical syntax masses, keep the un-augmented n = 7 comparison, and report that any rescue in the
augmented arm may be a prior effect.

**Static go/no-go checkpoint** [after review], before any chain: for every efficient candidate (S3, P, P′, and any
other self-efficient program at the cutoff) its invasion by each of the five constants and by its neutral
neighbours; its payoff entering the greedy polymorphism (composition measured in the weak arm, and recomputed in
the modal arm) against the polymorphism's mean; the fixation probabilities at N = 10³ and 10⁴. Representative
recursive encounters (P′ vs P′, P′ vs the accommodator, P′ vs P, P vs S5) are verified with the proof checker of
`src/gl_proofs.py` (GLS+Def certificates for the box atoms), not by informal fixed-point argument. The exact
reduced subsystem {S3, S5, accommodator, P, P′} chain at N = 10³, 10⁴, 3·10⁴ (dense GTH) is the interpretable
reference and is compared with the full chain's stationary weights and transitions.

**Chains.** ε→0, w = 0.3, N ∈ {10², 10³, 10⁴, 3·10⁴, 10⁵}: π by partition, P(efficient), E[max share], support,
transitions, the top state's exit and its N-scaling. Order [after review]: static → **paired modal/weak at n = 7**
→ the reduced subsystem → n = 11 or augmentation (paired) → fixed roles (modal, N ≤ 10⁴). The lazy state exploration
of `src/dollar_partitions.py` is run at θN ∈ {10⁻⁷, 10⁻⁹} and the stationary weights reported under both (convergence,
not just cut flow), with transitions through the named shadows, the greedy constants and their polymorphisms
retained explicitly. Entry/exit rates of the efficient state and of the polymorphism are reported against N so
that the barrier controlling the odds is identified; finite-N efficiency is reported as such.

**Lottery.** ε = 0, (100, 64) and (400, 16), mN ∈ {0, 0.1}, 40 runs per cell, modal and matched weak with identical
initialization and stopping rules, verified closure distinguished from long residence, run-level intervals.

Priority as in "Chains"; ≤ 3 workers; stop where time runs out and say where.

## Required outputs

`runs/modal-dollar.md` and `.json`, code in `src/modal_dollar.py` (reusing `src/dollar3.py`,
`src/dollar_partitions.py`, `src/gl_proofs.py`; no edits to core files except bug fixes in their own commits), a
predictions file from the spec committed before any counted run, the usual hand-back (draft RESULTS, REJECTED,
THEORY §3 and §9.2 edits, DEFERRED 2, 3 and 6 edits, NOTATION, ≤ 5 lines, branch from `git branch --show-current`,
commits).

## RE predictions (with falsifiers) [after review: the hypothesis reversed]

1. **At n = 7 both arms leak by the same mechanism.** One-atom accommodators are neutral shadows of S3 in both arms,
   S5 invades them, and the greedy polymorphism holds ≥ 0.8 of π by N = 3·10⁴ in the modal arm and in the matched
   weak arm; the weights need not agree within 0.1 (sol's point), the mechanism must. *Falsifier:* modal
   P(efficient) ≥ 0.7 at N = 3·10⁴ at n = 7.
2. **P is strictly invaded by S5 and does not rescue efficiency** (sol's objection, adopted): with P in the
   language the modal arm's P(efficient) ≤ 0.6 at N = 3·10⁴, and the reduced subsystem shows P entering the old
   polymorphism and ending in a P/S5 mixture near x_P = 1/3. *Falsifier:* P(efficient) ≥ 0.8 at 3·10⁴ with P and
   without P′.
3. **P′ cannot re-enter the greedy polymorphism:** its invasion payoff is within 0.05 of the polymorphism's mean
   (it earns 5/6 only against the accommodator fraction, ≈ 0.25, and 0 against S5), so it is at best neutral there,
   and the modal arm with P′ keeps P(efficient) ≤ 0.6 at N = 3·10⁴. **Sound reading does not rescue bargaining
   efficiency; certified commitment helps the greedy.** *Falsifier:* P′'s invasion payoff exceeds the mean by
   ≥ 0.1, or modal P(efficient) ≥ 0.8 at N = 3·10⁴ with P′ (then the RE's first-draft hypothesis is back).
4. **Fixed roles keep the accommodator ratchet under sound reading** (endpoints ≥ 0.9 of π at N ≥ 10³ in the modal
   fixed-role chain), and **the modal lottery matches the weak one** (50–50 ≥ 0.8 of islands at (100, 64),
   mN = 0.1, in both arms). *Falsifier:* endpoints ≤ 0.6 at N = 10³, or the arms' 50–50 shares differing by ≥ 0.2.

The RS is invited to add predictions; the uncertain one is 3 (the static checkpoint decides it before any chain).
