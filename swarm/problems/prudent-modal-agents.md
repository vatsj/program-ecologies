# Problem: prudent modal agents

## Background

Programs that can read each other's source can cooperate in a one-shot prisoner's dilemma by proving things about
each other. FairBot cooperates with an opponent iff it can prove that the opponent cooperates with it. By Löb's
theorem two FairBots cooperate with each other. But FairBot also cooperates with CooperateBot (always C), which it
could have exploited. Can a provability-based agent do better?

## Definitions

**Agents.** Each agent X is given by a formula φ_X of the modal logic GL (the provability logic of Peano arithmetic,
□ = "PA proves"). The formula is built from:
- three atoms, each read relative to the current opponent Y:
  - `a` = "Y cooperates with X";
  - `c` = "Y cooperates with CooperateBot";
  - `d` = "Y cooperates with DefectBot";
- the constants ⊤ and ⊥, the connectives ¬, ∧, ∨ and →, and the box □.

Every atom must occur inside at least one □ (φ_X is fully modalized). X cooperates with Y iff φ_X holds. The
**modal depth** of φ_X is the maximum nesting of boxes.

**Computing outcomes.** Evaluate on the finite linear Kripke frames of GL: worlds 0, 1, 2, …. A formula □ψ is true at
world n iff ψ is true at every world m < n, so every □ψ is vacuously true at world 0. Compute all relevant actions
world by world. Each action's truth value is eventually constant, and that stable value is the actual outcome (by the
de Jongh–Sambin fixed-point theorem, this is the unique solution of the system of mutually referential sentences).

**Named agents.**
- CooperateBot: φ = ⊤.
- DefectBot: φ = ⊥.
- FairBot: φ = □a.

**Prudent.** X is prudent if it:
- defects against CooperateBot;
- defects against DefectBot;
- cooperates with FairBot;
- cooperates with itself.

## Questions

1. Does a prudent agent exist? If so, give one of the smallest possible modal depth, with its outcome table against
   CooperateBot, DefectBot, FairBot and itself.
2. Prove that no agent of smaller modal depth is prudent, for formulas of any size.
3. If you can: characterize the prudent agents of that minimal depth, or bound their minimal size.

## Evidence

All 801 pairwise-inequivalent fully modalized formulas over a, c and d were enumerated, up to modal depth 2 and 7
symbols and without constants, each combined with either default (cooperate unless the formula holds, or defect unless
it holds). None is prudent.

## Deliverable

A file `answer.md` with your answers, proofs, and any code you used. Mark partial results clearly.
