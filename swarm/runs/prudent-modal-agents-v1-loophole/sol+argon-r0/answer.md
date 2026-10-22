FORMULA: B(F)|(~B(d)&~B(~c))
DEPTH: 1

Let X have the formula

\[
\varphi_X=\Box\bot\;\lor\;(\neg\Box d\land\neg\Box\neg c).
\]

All atoms are boxed, and the modal depth is 1. The reference checker reports:

```
depth 1; vs CooperateBot D, vs DefectBot D, vs FairBot C, vs itself C; prudent: YES
```

## Outcomes and proof

Write C=1 and D=0. At world 0, the disjunct \(\Box\bot\) is true, so X cooperates with every opponent. At every world n≥1 that disjunct is false. The other disjunct says that among earlier worlds the opponent has defected against DefectBot at least once and cooperated with CooperateBot at least once.

Against CooperateBot, d is always true, so \(\neg\Box d\) is always false. Against DefectBot, c is always false, so \(\neg\Box\neg c\) is always false. Thus X defects against both at every world n≥1.

FairBot cooperates with CooperateBot at every world: the statement that CooperateBot cooperates with FairBot is always true. FairBot cooperates with DefectBot at world 0 and defects at every world n≥1, since DefectBot never cooperates. Consequently X defects against FairBot at world 1, and cooperates at every world n≥2: world 0 witnesses c, and world 1 witnesses ¬d.

In self-play, c at world m is X's action against CooperateBot at m, and d is its action against DefectBot at m. Both are true at m=0 and false at every m≥1, by the already established constant-opponent outcomes. Thus X defects against itself at world 1 and cooperates at every world n≥2, with the same two witnesses.

| Opponent | X at world 0 | X at world 1 | X at every world n≥2 | Stable outcome (X, opponent) |
|---|---|---|---|---|
| CooperateBot | C | D | D | (D,C) |
| DefectBot | C | D | D | (D,D) |
| FairBot | C | D | C | (C,D) |
| X | C | D | C | (C,C) |

The FairBot entry deserves attention: FairBot defects against X from world 2 onward because X defected against it at world 1. Prudence as defined asks that X cooperate with FairBot, not that their cooperation be mutual. The displayed stable outcomes use exactly the specified semantics.

## Minimal depth, for formulas of arbitrary size

A fully modalized formula of depth 0 contains no atoms: any atom would have to occur inside a box, forcing positive depth. It is therefore a Boolean combination of ⊤ and ⊥. Its truth value is constant, independent of the opponent and world. Such an agent either cooperates with every opponent or defects against every opponent, so it cannot satisfy prudence. Hence depth 1 is the smallest possible depth.

## Complete characterization at depth 1

This also answers the optional characterization question. Let V={0,1}³, with coordinates ordered (a,c,d). Every fully modalized formula of depth at most 1 is a Boolean combination of constants and expressions \(\Box p\), where p is propositional in a,c,d. Associate to it a function

\[
f:\mathcal P(V)\longrightarrow\{0,1\}
\]

by evaluating each \(\Box p\) as true exactly when p is true at every valuation in S. At world n, S is precisely the set of atom valuations appearing at worlds m<n; hence the action is f(S). In particular, S=∅ at world 0.

**The characterization:** such a formula is prudent if and only if all six conditions hold:

\[
\begin{aligned}
f(\varnothing)&=1,\\
f(\{111\})&=0,\\
f(\{000\})&=0,\\
f(\{111,000\})&=1,\\
f(\{111,000,100\})&=1,\\
f(\{111,110,010\})&=1.
\end{aligned}
\]

Here strings such as 110 denote valuations, not worlds.

**Proof.** Let t=f(∅), the action against every opponent at world 0. Against CooperateBot and DefectBot the valuation is respectively 111 and 000 at every world. Their stable actions are therefore f({111}) and f({000}), respectively. Prudence forces both to be 0.

If t=0, X's actions against both constant agents are 0 at all worlds. In self-play, induction then shows that X also defects at every world: its initial action is 0; if all earlier self-actions were 0, every earlier self-play valuation was 000, and its next action is f({000})=0. Thus prudence requires t=1.

Now assume these first three conditions. In self-play, the valuation at world 0 is 111, and the action at world 1 is f({111})=0. From world 1 onward c=d=0. Thus the valuation at world 1 is 000. If f({111,000})=0, this valuation repeats forever and self-play never cooperates again. If f({111,000})=1, the action at world 2 is 1, adding valuation 100 to the history. From world 3 onward the history-set is {111,000,100}: either possible subsequent valuation, 000 or 100, is already present. Therefore stable self-cooperation is equivalent to the fourth and fifth conditions.

Against FairBot, its (a,c,d) valuation at world 0 is 111. At world 1 it is 110: FairBot's action against X depends only on X's initial cooperation, its action against CooperateBot is true, and its action against DefectBot is false. X's world-1 action is f({111})=0, so FairBot's action against X is false from world 2 onward. Hence the valuation is 010 at every world n≥2. From world 3 onward X's action is consequently f({111,110,010}), proving the last condition is necessary and sufficient. Together these observations prove the characterization.

There are no further restrictions on f: any function on subsets of V is expressible at depth 1. For each valuation v, take a propositional formula χ_v true exactly at v; then \(\neg\Box\neg\chi_v\) tests whether v belongs to S. Boolean combinations of these eight membership tests express every such function. Thus the six displayed conditions are also an unrestricted semantic parametrization of all prudent depth-1 agents.

## Exact minimal formula size at depth 1

Measuring formula size by total symbol count (AST nodes: atoms, constants, unary operators \(\neg, \Box\), and binary connectives \(\land, \lor, \to\), excluding parentheses):

- **With constants (\(\top, \bot\)):** the exact minimum size of a depth-1 prudent formula is **9 symbols**, achieved by
  \[
  (\Box a \lor \Box \neg a) \to \Box \bot \qquad \text{(`(B(a) | B(~a)) -> B(F)`)}
  \]
  (as well as `(B(d) | B(~d)) -> B(F)` and `(B(d) | B(~c)) -> B(F)`).
- **Without constants:** the exact minimum size of a depth-1 prudent formula is **12 symbols**, achieved by
  \[
  (\Box a \lor \Box \neg a) \to \Box(a \land \neg a) \qquad \text{(`(B(a) | B(~a)) -> B(a & ~a)`).}
  \]

**Proof of the lower bounds.**
1. *At least three \(\Box\) occurrences are required.* Suppose a depth-1 formula \(\varphi\) contains at most two box subformulas \(B_1 = \Box p_1\) and \(B_2 = \Box p_2\). Then \(\varphi = g(B_1, B_2)\) where \(g\) is a read-once Boolean formula over the basis \(\{\neg, \land, \lor, \to, \top, \bot\}\). Every read-once formula over this basis is unate (monotone increasing or decreasing) in each variable. However, for any \(p_i\), \(B_i(\varnothing) = 1\) and \(B_i(\{111, 000\}) = B_i(\{111\}) \land B_i(\{000\})\). To satisfy the characterization \(f(\varnothing) = 1\), \(f(\{111\}) = f(\{000\}) = 0\), and \(f(\{111, 000\}) = 1\), the pair \((B_1, B_2)\) must take values \((1,0)\) and \((0,1)\) on \(\{111\}\) and \(\{000\}\), and \((0,0)\) on \(\{111, 000\}\). This forces \(g(1,1)=1, g(1,0)=0, g(0,1)=0, g(0,0)=1\), i.e., \(g(B_1, B_2) \equiv (B_1 \leftrightarrow B_2)\), which is not unate in either variable—a contradiction. Thus \(\varphi\) has at least 3 occurrences of \(\Box\).
2. *Minimum size 9 with constants.* Three boxes require at least three inner atom/constant leaves and two binary connectives joining the boxed subformulas, totaling at least 8 symbols. Four boxes already require at least 11 symbols. Thus a formula of size at most 8 would have exactly three boxes, each applied directly to an atom or constant, with only two outer binary connectives. For every such inner leaf x, we have x(000) ≤ x(111). Consequently each box has the same value on {000} and {111,000}, and so does the whole formula. This contradicts the required respective values 0 and 1. Hence at least 9 symbols are necessary, and the displayed example achieves this bound.
3. *Minimum size 12 without constants.* Classify each boxed propositional formula \(\Box p\) by the pair (p(111),p(000)). The four possible types are 11 (true on all four history-sets under consideration), 10 (call this B₊), 01 (call this B₋), and 00. On the four sets (∅,{111},{000},{111,000}), their respective value vectors are (1,1,1,1), (1,1,0,0), (1,0,1,0), and (1,0,0,0).

   If there is no box of type 00, replacing type-11 boxes by true and type-10/type-01 boxes by variables B₊/B₋ shows that the outer formula must compute XNOR of those two variables. Each variable must occur at least twice: a variable occurring only once in a formula over {¬,∧,∨,→} is unate, whereas XNOR is nonunate in both variables. Thus there are at least two type-10 boxes and two type-01 boxes. A constant-free type-10 inner formula needs at least one symbol, and a type-01 inner formula needs at least two (a single atom has type 10). These require at least 6 inner symbols, 4 boxes, and 3 outer binary connectives: at least 13 symbols.

   If there is a box of type 00, its inner formula needs at least 4 symbols. Indeed, constant-free formulas of size at most 3 are atoms, negated atoms, double-negated atoms, or a binary connective applied to two atoms; none has value 0 at both 111 and 000. There must also be a type-10 box and a type-01 box. To see this, let U and V be the vectors of all box-values on {111} and {000}. Neither vector can be coordinatewise below the other: otherwise their coordinatewise meet, the box-vector on {111,000}, would equal one of them, contradicting the different required outputs. Thus there is a coordinate of type 10 and another of type 01. Their inner formulas need at least 1 and 2 symbols respectively. In total the formula needs at least 4+1+2 inner symbols, 3 boxes, and 2 outer binary connectives, giving 12 symbols. The displayed constant-free example achieves 12.

*(Remark on the Evidence and depth 2: this also explains why enumerating formulas up to 7 symbols without constants found no prudent agent; at modal depth 2, `\text{B(a & (d -> B(F)))}` has 7 symbols with constant `F`, and `\text{B(a & (d -> B(~d)))}` has 8 symbols without constants, and both also achieve mutual cooperation \((C,C)\) with FairBot.)*

