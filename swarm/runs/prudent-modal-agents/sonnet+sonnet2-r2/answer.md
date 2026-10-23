# Prudent modal agents

FORMULA: B(a & (B(F) | ~d))
DEPTH: 2

In symbols: φ = □(a ∧ (□⊥ ∨ ¬d)). This is PrudentBot: it cooperates iff PA proves "Y cooperates with me" and PA+Con(PA) proves "Y defects against DefectBot".

## Q1. Outcome table (check.py: "depth 2; prudent: YES")
| X vs | X's action | opponent's action vs X |
|---|---|---|
| CooperateBot | D | C |
| DefectBot | D | D |
| FairBot | C | C |
| X itself | C | C |

Hand check. Against CB, a=c=d=⊤, so φ = □(□⊥ ∨ ⊥) = □□⊥, which is false at every world n ≥ 2, so the stable value is D. Against DB, a=⊥, so the inner conjunction is ⊥ and φ = □⊥, true only at world 0 and the stable value is D. Against FairBot and against itself, see checker output (C, C, C). Löb-type reasoning: with a = □(...) for FairBot, the stable solution is all-C.

## Q2. No agent of modal depth ≤ 1 is prudent (any formula size)

Let φ have depth ≤ 1. Then φ = F(□ψ_1,…,□ψ_k) where F is a Boolean combination (constants allowed) and each ψ_i is a Boolean function of the atoms a,c,d only (no boxes inside; k=0 allowed for depth 0). Put p_i = ψ_i(a=1,c=1,d=1) (1 = true/cooperate). Write x_n for "X cooperates with FairBot" at world n.

**Step 1: X vs CooperateBot.** CB cooperates at every world, so at every world a=c=d=1 (for CB the atoms are: CB cooperates with X, with CB, with DB: all ⊤). Hence □ψ_i is true at world n ≥ 1 iff p_i (ψ_i is evaluated at world 0 … n−1, always at the constant assignment (1,1,1)). So at every world n ≥ 1 X's action vs CB is F(p_1,…,p_k), constant, so it is the stable value. Prudence (defect against CB) forces **F(p) = 0**.

**Step 2: X vs FairBot at world 1.** x_1 = F(□ψ_i at world 1), and □ψ_i at world 1 is ψ_i evaluated at world 0 only. At world 0: FairBot's action vs X is □(…) , vacuously true, so a_0 = 1; c = (FairBot vs CB) = □⊤ = 1 at every world; d = (FairBot vs DB) = □⊥ which is true at world 0, so d_0 = 1. So ψ_i is evaluated at (1,1,1), giving value p_i, and x_1 = F(p) = 0 by Step 1.

**Step 3: FairBot's reply.** FairBot's action vs X at world n is a_n = ∧_{m<n} x_m, which is non-increasing in n. If FairBot eventually cooperates with X then a_n = 1 for some (all large) n, hence x_m = 1 for all m, in particular x_1 = 1. But x_1 = 0 by Step 2. So FairBot's stable reply is D, contradicting prudence ("X and FairBot cooperate with each other").

Hence no agent of depth 0 or 1 is prudent, and depth 2 is minimal. ∎
(Note this uses only the CB and FairBot conditions; the other conditions are not needed. It confirms the exhaustive-search evidence.)

## Q3. Partial remarks
Depth-1 impossibility is robust (above). For depth 2, B(a & (B(F) | ~d)) works with 7 symbols excluding constants Characterization/minimal size not attempted (partial).
