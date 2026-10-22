# Problem: does prudence require nested boxes?

## Background

Programs that can read each other's source can cooperate in a one-shot prisoner's dilemma by proving things about each
other. FairBot cooperates with an opponent iff it can prove the opponent cooperates with it. By Löb's theorem two
FairBots cooperate with each other (Barasz, Christiano, Fallenstein, Herreshoff, LaVictoire and Yudkowsky, 2014).
FairBot also cooperates with CooperateBot (always C), which it could have exploited. PrudentBot avoids that: it
cooperates iff it can prove the opponent cooperates with it **and** it can prove, in PA + Con(PA), that the opponent
defects against DefectBot.

## Definitions

**Agents.** Each agent X is given by a formula φ_X of the modal logic GL (the provability logic of Peano arithmetic,
□ = "PA proves"). The formula is built from:
- three atoms, each read relative to the current opponent Y:
  - `a` = "Y cooperates with X";
  - `c` = "Y cooperates with CooperateBot";
  - `d` = "Y cooperates with DefectBot";
- the constants ⊤ and ⊥, the connectives ¬, ∧ and ∨, and the box □.

Every atom must occur inside at least one □ (φ_X is fully modalized). X cooperates with Y iff φ_X holds. The
**modal depth** of φ_X is the maximum nesting of boxes.

**Computing outcomes.** Evaluate on the finite linear Kripke frames of GL: worlds 0, 1, 2, …. A formula □ψ is true at
world n iff ψ is true at every world m < n, so every □ψ is vacuously true at world 0. Compute all relevant actions
world by world. Each action's truth value is eventually constant, and that stable value is the actual outcome (by the
de Jongh–Sambin fixed-point theorem, this is the unique solution of the system of mutually referential sentences).

**Named agents.**
- CooperateBot: φ = ⊤.
- DefectBot: φ = ⊥.
- FairBot: φ = □a, modal depth 1.
- PrudentBot: φ = □a ∧ □(¬□⊥ → ¬d), modal depth 2. The guard □(¬□⊥ → ψ) means "PA + Con(PA) proves ψ".

**Prudent.** X is prudent if it:
- defects against CooperateBot;
- defects against DefectBot;
- cooperates with FairBot;
- cooperates with itself.

PrudentBot is prudent (Barasz, Christiano, Fallenstein, Herreshoff, LaVictoire and Yudkowsky 2014).

## Known results you may use

- Barasz et al. (2014), Theorem 4.10: a modal agent of rank 0 that cooperates with FairBot also cooperates with
  CooperateBot.
- The same paper remarks that PrudentBot's DefectBot clause must be checked in a stronger system than PA (hence the
  Con(PA) guard), or self-cooperation is lost.

Neither of these is a theorem about all formulas of a given modal depth.

## Conjecture

**No modal agent of depth 1 is prudent.** Prudence needs nested boxes, which is exactly what reading a guard in
PA + Con(PA) costs, and depth 2 suffices (PrudentBot).

## Evidence

All 801 pairwise-inequivalent fully modalized formulas over a, c and d were enumerated, up to modal depth 2 and 7
symbols and without constants, each combined with either default. None is prudent. This includes every depth-1
formula of up to 7 symbols. PrudentBot needs more symbols than that, which is why the enumeration found no
depth-2 example either.

## What we want

Prove that no depth-1 agent is prudent, of any size and with constants allowed, or find a depth-1 counterexample.
Stronger results are welcome:
- a characterization of the prudent agents of depth 2, or of their minimal size;
- which subsets of the four prudence conditions are jointly satisfiable at depth 1;
- the analogue with more reference agents than CooperateBot and DefectBot.

The heuristic is that telling FairBot apart from CooperateBot seems to need "the opponent defects against DefectBot".
For FairBot that statement is unprovable in PA and true. At depth 1, every box is vacuously true at world 0, where
FairBot and CooperateBot behave identically against all three reference points.

## Deliverable

A file `answer.md` containing one of:
- a proof;
- a counterexample formula with its outcome table against CooperateBot, DefectBot, FairBot and itself, computed as
  defined above;
- partial results, clearly marked as such.

Include any code you used.
