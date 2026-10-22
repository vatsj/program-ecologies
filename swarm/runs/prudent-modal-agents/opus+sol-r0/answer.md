FORMULA: B(a & (d -> B(F)))
DEPTH: 2

Let X be the agent with formula
\[
\varphi_X=\Box\bigl(a\land(d\to\Box\bot)\bigr).
\]
It is fully modalized and has modal depth 2. The reference checker reports it prudent.

| Opponent Y | X against Y | Y against X |
|---|---|---|
| CooperateBot | D | C |
| DefectBot | D | D |
| FairBot | C | C |
| X | C | C |

### Verification at every world

Write X(Y,n) for X's action against Y at world n, with C=true and D=false. On the specified frames, \(\Box\bot\) is true exactly at world 0. Therefore X cooperates against Y at world n precisely when, at every m<n:

1. Y cooperates against X at m; and
2. if m>0, Y defects against DefectBot at m.

In particular X cooperates against every opponent at world 0.

Against CooperateBot, condition 1 always holds, but condition 2 fails at m=1. Thus X(CB,n) is C for n=0,1 and D for every n>=2.

Against DefectBot, condition 1 fails already at m=0. Thus X(DB,0)=C and X(DB,n)=D for every n>=1.

FairBot cooperates against DefectBot exactly at world 0. Consequently condition 2 is always satisfied against FairBot. Induction on n now proves that both X(FB,n) and FB(X,n) are C for every n: both are C at n=0; if both are C at all earlier worlds, the defining box of each agent is true at n.

Against itself, the already computed sequence X(DB,m) is C at m=0 and D thereafter, so condition 2 again always holds. Induction gives X(X,n)=C for every n, since condition 1 asks only for X(X,m)=C at earlier worlds.

All claimed stable outcomes follow.

### No smaller modal depth is possible

A fully modalized depth-0 formula contains no atoms and is therefore a constant Boolean value. Such an agent cannot both defect against CooperateBot and cooperate against FairBot.

Now suppose X has modal depth at most 1 and FairBot's stable action against X is C. By FairBot's definition,
\[
FB(X,n)=\bigwedge_{m<n}X(FB,m).
\]
If X(FB,k) were D at any world k, then FB(X,n) would be D for every n>k. Thus **X(FB,n)=C at every world n**, in particular at n=1.

Every depth-1 fully modalized formula is a Boolean combination of constants and boxes \(\Box\theta(a,c,d)\), where \(\theta\) is propositional. At world 0, FairBot cooperates against every opponent, because its box is vacuous. Hence the triple (a,c,d) supplied by FairBot at world 0 is (C,C,C). This is exactly the triple supplied by CooperateBot at every world.

At world 1, each box \(\Box\theta\) against FairBot therefore has value \(\theta(C,C,C)\). Against CooperateBot, the same box has that same value at **every** world n>=1: its nonempty past consists entirely of the triple (C,C,C). All Boolean combinations preserve this equality. Consequently
\[
X(CB,n)=X(FB,1)=C\qquad(n\ge1).
\]
This contradicts the requirement that X defect against CooperateBot. The proof applies to formulas of arbitrary size, including arbitrary Boolean combinations of arbitrarily many boxes. Thus the minimal prudent modal depth is exactly 2.

### Size bound

Counting each atom, constant, connective, and box as one syntax-tree node (parentheses do not count), the displayed formula has 7 nodes: two boxes, one conjunction, one implication, and the three leaves a, d, and F. Thus a prudent agent of the minimal depth has size at most 7 under this convention.

### Size optimality (Q3, exhaustive search)

With the same node-count convention (alphabet: atoms a,c,d; constants T,F; ~; B; binary &, |, ->), the script `/work/opus/search.py` enumerates **every** syntax tree with at most 7 nodes, keeps those that are fully modalized of depth exactly 2, and evaluates them on worlds 0..19. It was also cross-checked against `check.py` on 3,000 random formulas from the 22,840 candidates, with 0 disagreements (`/work/opus/xval.py`).

Here is a sufficient bound justifying the finite simulation. A depth-2 syntax tree with at most 7 nodes has at most four boxes: if it has at least two binary nodes then at most two nodes remain for boxes; if it has one binary node, each of its two root-to-leaf paths contains at most two boxes; with no binary node it has at most two boxes. Track the truth of each box in each of the four X matchups, and the box defining FairBot against X. There are at most 4*4+1=17 Boolean state bits, and every such bit can change only once, from true to false. From world 1 onward their update rule is deterministic and independent of the world index: CB and DB are constant, FB against CB is always C, and FB against DB is D from world 1 onward. If one update changes no state bit, all subsequent updates leave the state fixed. Thus after at most 17 changing updates starting at world 1 the state is fixed; in particular all actions at world 19 have their stable values.

Result:

- sizes 1–6: no prudent formula;
- size 7: exactly two, `B(a & (d -> B(F)))` and its commuted form `B((d -> B(F)) & a)`.

Hence the minimum size of a prudent depth-2 agent is **exactly 7** nodes, and up to commutativity of & the minimum-size prudent agent is unique: □(a ∧ (d → □⊥)). (Equivalent variants such as □a ∧ □(□⊥ ∨ ¬d), the classical PrudentBot "□a ∧ □(¬□⊥ → ¬d)", are also prudent but larger.)
