FORMULA: B(a) & B(B(F) | ~d)
DEPTH: 2

## 1. A prudent agent of depth 2
X = □a ∧ □(□⊥ ∨ ¬d)   (a PrudentBot analogue). `check.py` output:
`depth 2; vs CooperateBot D, vs DefectBot D, vs FairBot C (FairBot replies C), vs itself C; prudent: YES`

| opponent | X's action | note |
|---|---|---|
| CooperateBot | D | d = T always, and □⊥ fails at world 1, so the second conjunct fails from world 2 on |
| DefectBot | D | a = F |
| FairBot | C | FairBot also replies C. FairBot's d is □⊥, so ¬d holds at every world m≥1. The second conjunct then holds at all worlds, and the first conjunct is Löb's argument |
| itself | C | same Löb argument; the second conjunct holds because X's action against DefectBot is D at every world m≥1 |

(For contrast, `B(a) & B(B(F) | ~c)` is not prudent: against FairBot, c = T.)

## 2. No agent of modal depth ≤ 1 is prudent (any size)
Let X have depth ≤ 1. Then φ_X = Φ(□ψ_1, …, □ψ_k), where Φ is a Boolean function (constants allowed) and each ψ_i is a Boolean combination of a, c, d and constants. Depth 0 is the case k = 0.

Write x_n for X's action against FairBot at world n, and f_n for FairBot's action against X at world n. FairBot is □a with a = "X cooperates with FairBot", so f_n = ∀m<n. x_m.

*Step 1: X against CooperateBot.* CooperateBot's actions against X, and against CooperateBot, are T at every world. So a = c = d = T at every world. Hence □ψ_i at world n≥1 is true iff ψ_i(1,1,1) holds, because world 0 is the only world below n=1 and later worlds repeat the same value. So X's action against CooperateBot at every world n≥1 is Φ(ψ_1(111), …, ψ_k(111)). That is the stable value. If X defects against CooperateBot, then this value is F.

*Step 2: X against FairBot at world 1.* The box □ψ_i at world 1 looks only at world 0. At world 0 the atoms against FairBot are:
- a = f_0 = T, since □a is vacuously true at world 0;
- c = (FairBot's action against CooperateBot at world 0) = T;
- d = (FairBot's action against DefectBot at world 0) = □⊥ at world 0 = T.

So the atoms are (1,1,1) and □ψ_i is ψ_i(111) at world 1, exactly as in Step 1. Hence x_1 = Φ(ψ_i(111)) = F.

*Step 3: FairBot against X.* f_n = ∀m<n. x_m includes m=1, so f_n = F for all n≥2. FairBot's stable action against X is D.

So an X that defects against CooperateBot cannot also be cooperated with by FairBot. Prudence requires both, so no agent of depth ≤ 1 is prudent. ∎

This does not use the DefectBot or self-play conditions. It also covers the 801-formula and 523,264-agent searches in the Evidence section, which found no prudent agent. Depth 2 is therefore minimal.

## 3. Remarks (partial)
The proof gives a structural reason for the depth-1 failure. At world 1, a depth-1 agent cannot tell FairBot from CooperateBot, because both look like (1,1,1). The depth-2 agent separates them. The second box looks at worlds m≥1 through the atom d. For FairBot, d = □⊥ is false from world 1 on. For CooperateBot, d = T.

Depth-2 agents that separate FairBot from CooperateBot use the fact that FairBot proves nothing about DefectBot (□⊥ is false), whereas CooperateBot does cooperate with DefectBot (c = d = T). Obstruction in general: the agent must defect against CooperateBot while FairBot cooperates with it, so the agent's φ must differ between the two at some world ≥ 2. That needs depth ≥ 2.

The formula above has 11 symbols in the checker's syntax counted as tokens B, a, &, B, B, F, |, ~, d (about 9 atoms and operators, ignoring parentheses). I did not prove it minimal in size, and I did not characterize all depth-2 prudent agents.
