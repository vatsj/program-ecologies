FORMULA: B(F) | ~(B(a) | B(~a))
DEPTH: 1

A prudent agent exists at modal depth 1, and this is the smallest possible depth.

## Construction and outcomes

Take

\[
\varphi_X=\Box\bot\;\lor\;\neg(\Box a\lor\Box\neg a).
\]

At world 0 this formula is true, because \(\Box\bot\) is vacuously true. At every world \(n\geq1\), it is true exactly when the opponent's actions against X at worlds below \(n\) include **both** cooperation and defection. Indeed, the first disjunct is then false, while the second says that neither all earlier actions were C nor all earlier actions were D.

The actions of X are:

| Opponent | World 0 | World 1 | World 2 | Every world ≥ 3 | Stable outcome |
|---|---|---|---|---|---|
| CooperateBot | C | D | D | D | D |
| DefectBot | C | D | D | D | D |
| FairBot | C | D | D | C | C |
| X | C | D | C | C | C |

For CooperateBot and DefectBot, every nonempty history is constant, so X defects at every positive world.

Against itself, X cooperates at world 0 and defects at world 1, since its history at world 1 contains only C. At every subsequent world its history contains those first two different actions, so it cooperates.

For FairBot, write \(x_n=X(\mathrm{FB},n)\) and \(f_n=\mathrm{FB}(X,n)\). FairBot's rule gives
\[
f_n=\bigwedge_{m<n}x_m.
\]
Thus \(f_0=f_1=\mathrm C\): the first is vacuous and the second follows from \(x_0=\mathrm C\). Consequently \(x_1=x_2=\mathrm D\), because the relevant FairBot histories contain only C. Since \(x_1=\mathrm D\), we have \(f_n=\mathrm D\) for all \(n\geq2\). X therefore sees both actions starting at world 3, and cooperates forever after that.

This proves all four prudence conditions. FairBot itself has stable action D against X; the stated definition of prudence requires X to cooperate with FairBot, and does not require reciprocal cooperation.

The reference checker reports:

```text
depth 1; vs CooperateBot D, vs DefectBot D, vs FairBot C, vs itself C; prudent: YES
```

## Impossibility at smaller depth

A fully modalized formula of depth 0 cannot contain any of the atoms a, c, d: each atom would have to occur inside a box, which would give positive depth. It is therefore a Boolean formula built only from constants, and has one constant truth value against every opponent at every world.

If that value is true, the agent fails to defect against CooperateBot and DefectBot. If it is false, the agent fails to cooperate with FairBot and itself. Hence no depth-0 agent, of any formula size, is prudent.

## Complete characterization at depth 1

There is also a finite truth-table characterization of every prudent agent of the minimal depth.

Let \(V=\{0,1\}^3\), with coordinates in the order \((a,c,d)\). Every fully modalized formula of depth at most 1 determines a function
\[
h:\mathcal P(V)\longrightarrow\{0,1\}.
\]
At a world, let \(S\) be the set of triples attained by \((a,c,d)\) at strictly earlier worlds. The formula's value is \(h(S)\). To see this, each boxed subformula has propositional content \(p(a,c,d)\), and its value is precisely whether every member of S satisfies p. The whole formula is a Boolean combination of these values and constants.

Conversely, **every** function h is expressible at depth at most 1. For each \(v\in V\), let \(\delta_v\) be the propositional formula specifying exactly that triple. Then \(\neg\Box\neg\delta_v\) tests whether \(v\in S\). An arbitrary Boolean function of these eight membership tests expresses h.

**Characterization.** Such an agent is prudent if and only if all six following conditions hold:

\[
\begin{aligned}
h(\varnothing)&=1,\\
h(\{111\})&=0,\\
h(\{000\})&=0,\\
h(\{111,000\})&=1,\\
h(\{111,000,100\})&=1,\\
h(\{111,110,010\})&=1.
\end{aligned}
\]

Here a string such as 100 denotes the triple \((1,0,0)\).

**Proof.** Against CooperateBot, every positive world has history set \(\{111\}\), and against DefectBot it has history set \(\{000\}\). Thus defection against these agents is equivalent to the second and third conditions.

Under these two conditions, \(h(\varnothing)=0\) would force perpetual self-defection: all initial actions are 0, and the self-play history then remains \(\{000\}\). Therefore prudence requires the first condition. Assume it from now on. X's actions against either constant agent are then 1 at world 0 and 0 at every positive world.

In self-play, the triple at world 0 is consequently 111, and X's action at world 1 is 0. The triple at world 1 is 000. At world 2, X's action is \(h(\{111,000\})\). If this is 0, its history remains that set forever, so self-cooperation fails. If it is 1, the world-2 triple is 100, since its actions against both constant agents are now 0. From world 3 onward its history set remains exactly \(\{111,000,100\}\): subsequent triples can only be 000 or 100, both already present. Hence stable self-cooperation is equivalent to the fourth and fifth conditions.

Against FairBot, the world-0 triple is 111. X's initial action is 1, so the world-1 triple is 110: FairBot cooperates with X and CooperateBot, but defects against DefectBot. X's world-1 action is \(h(\{111\})=0\), which makes FairBot defect against X at every world from 2 onward. Thus the triple is 010 at every such world. From world 3 onward, X's action is exactly \(h(\{111,110,010\})\). This proves the last condition and completes both directions of the characterization.

The six history sets are distinct, and all other values of h are unrestricted. Consequently there are exactly \(2^{250}\) prudent truth-table behaviors at depth 1, identifying formulas that give the same value on every possible history set. All these sets can occur on finite linear frames with suitable atom valuations, so distinct truth tables really are semantically distinct.
