# Answer

FORMULA: B(a) & B(B(F) | ~d)
DEPTH: 2

(In symbols: φ = □a ∧ □(□⊥ ∨ ¬d). This is PrudentBot: cooperate iff PA proves "Y cooperates with me" and PA+1 proves "Y defects against DefectBot". ¬Con(PA) is □⊥, and PA+1 proves ψ iff PA proves (¬□⊥→ψ).)

## 1. Outcome table (check.py output)

`depth 2; vs CooperateBot D, vs DefectBot D, vs FairBot C (FairBot replies C), vs itself C; prudent: YES`

| opponent | X's action |
|---|---|
| CooperateBot | D |
| DefectBot | D |
| FairBot | C (FairBot replies C) |
| X itself | C |

## 2. No agent of depth < 2 is prudent, for formulas of any size

Notation: worlds 0,1,2,…; □ψ holds at n iff ψ holds at all m<n. Atom values are written (a,c,d).

**Depth 0.** There are no atoms outside a box, so φ is a Boolean combination of ⊤,⊥ only, i.e. a constant. φ=⊤ cooperates with CooperateBot. φ=⊥ does not cooperate with FairBot. So no depth-0 agent is prudent.

**Depth 1.** Then φ = F(□β_1,…,□β_k) for a Boolean function F, where each β_i is a Boolean combination of a, c, d, ⊤, ⊥ (no boxes). Write β_i(a,c,d) for its truth value. We use only two of the four prudence conditions: X defects against CooperateBot, and X and FairBot cooperate with each other. We show these already contradict each other.

*X against CooperateBot.* CooperateBot cooperates with everyone, so at every world the atoms for CB as opponent are (a,c,d) = (1,1,1). Hence at world n, □β_i is true iff n=0 or β_i(1,1,1). For every n ≥ 1 the value of X against CB is therefore F(β_1(1,1,1),…,β_k(1,1,1)) =: G. The value is constant from world 1 on, so the stable value is G. X defects against CB, so **G = 0**.

*X against FairBot.* Let x(n) be X's action against FairBot at world n, and f(n) FairBot's action against X, with f(n) = ∀m<n x(m) because FairBot is □a.
- FairBot's stable action against X must be C. If x(m)=0 for some m, then f(n)=0 for all n>m, and the stable value is D. So x(m)=1 for all m. In particular x(1)=1.
- Now compute x(1). The atoms for X's evaluation at world m are:
  - a(m) = f(m),
  - c(m) = "FairBot cooperates with CooperateBot" = □⊤ at m = 1,
  - d(m) = "FairBot cooperates with DefectBot" = □⊥ at m = [m=0].
  - At world 0 these are f(0)=1 (vacuous), 1, 1. So (a,c,d)(0) = (1,1,1).
- At world 1, □β_i is true iff β_i holds at world 0 only, which is β_i(1,1,1). So x(1) = F(β_1(1,1,1),…,β_k(1,1,1)) = G.

So x(1)=G=0, contradicting x(1)=1. Hence no depth-1 agent is prudent, regardless of size. (Even the CooperateBot and FairBot conditions alone are incompatible at depth 1: at world 1 an opponent's behaviour only reflects its behaviour at world 0, and FairBot and CooperateBot are indistinguishable at world 0.)

Combined with depth 0, no agent of depth < 2 is prudent, and the depth-2 formula above is prudent, so the minimal modal depth is exactly 2. This is consistent with the enumeration evidence in the problem.

## 3. Partial remark

Mechanism of the depth-2 solution: against CooperateBot, d is true at every world, so □(□⊥ ∨ ¬d) fails at world 2 (□⊥ is false at world 1) and X defects. Against FairBot, d = □⊥ is false from world 1 on, so ¬d holds there and the second conjunct is true. Against DefectBot, □a fails at world 1. I have not characterized all prudent depth-2 agents or bounded the minimal size. The formula above has 11 symbols without parentheses (a, B, B, F, B, d, ~, |, &, B, ...), which is only an upper bound.
