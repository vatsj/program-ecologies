# Problem: does prudence require reading one level up?

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
- the connectives ¬, ∧ and ∨, and the box □.

Every atom must occur inside at least one □ (φ_X is fully modalized). X cooperates with Y iff φ_X holds. A match
between two agents, together with their behaviour against CooperateBot and DefectBot, is a system of mutually
referential sentences. By the de Jongh–Sambin fixed-point theorem it has a unique solution up to provable equivalence,
and that solution decides every outcome.

**Computing outcomes.** Evaluate on the finite linear Kripke frames of GL: worlds 0, 1, 2, …. A formula □ψ is true at
world n iff ψ is true at every world m < n, so every □ψ is vacuously true at world 0. Compute all relevant actions
world by world. Each action's truth value is eventually constant, and that stable value is the actual outcome.

**Level PA+1.** Write □₁ for provability in PA + Con(PA). On the frames, □₁ψ is true at world n iff ψ is true at every
world m with 1 ≤ m < n.

**Named agents.**
- CooperateBot: φ = ⊤.
- DefectBot: φ = ⊥.
- FairBot: φ = □a.
- PrudentBot: φ = □a ∧ □₁¬d.

**Prudent.** X is prudent if it:
- defects against CooperateBot;
- defects against DefectBot;
- cooperates with FairBot;
- cooperates with itself.

PrudentBot is prudent.

## Conjecture

**No agent whose formula uses only □ (level PA, no □₁) is prudent.** Prudence needs at least one guard read in
PA + Con(PA).

## Evidence

All 801 pairwise-inequivalent fully modalized formulas over a, c and d were enumerated, up to modal depth 2 and 7
symbols, each combined with either default (cooperate unless the formula holds, or defect unless it holds). None is
prudent at level PA. With □₁ allowed, PrudentBot appears at 6 symbols.

## What we want

Prove the conjecture for all fully modalized formulas over a, c and d at level PA, of any depth and size, or find a
counterexample. Stronger results are welcome: a characterization of which of the four prudence conditions can be met
together at level PA, or the conjecture with more atoms (behaviour against other fixed reference agents).

The heuristic is that telling FairBot apart from CooperateBot seems to need "the opponent defects against DefectBot".
For FairBot that statement is equivalent to Con(PA), which PA cannot prove (Gödel's second incompleteness theorem). A
proof has to turn this heuristic into an argument about every formula.

## Deliverable

A file `answer.md` containing one of:
- a proof;
- a counterexample formula with its outcome table against CooperateBot, DefectBot, FairBot and itself, computed as
  defined above;
- partial results, clearly marked as such.

Include any code you used.
