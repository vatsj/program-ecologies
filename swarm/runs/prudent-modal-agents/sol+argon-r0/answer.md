FORMULA: B(a & (d -> B(F)))
DEPTH: 2

Let X have the formula

    □(a ∧ (d → □⊥)).

It is fully modalized and has modal depth 2. Its stable outcomes are:

| Opponent | X's action | Opponent's action |
|---|---|---|
| CooperateBot | D | C |
| DefectBot | D | D |
| FairBot | C | C |
| X | C | C |

## Verification

The formula □⊥ is true exactly at world 0. Thus d → □⊥ is true at world 0, regardless of d; at every world m ≥ 1 it is equivalent to ¬d. X cooperates with every opponent at world 0 because its outer box is vacuous.

Against CooperateBot, a and d are always true. The boxed conjunction is true at predecessor world 0 but false at predecessor world 1. Consequently X cooperates at worlds 0 and 1, and defects at every world n ≥ 2.

Against DefectBot, a is always false. Thus the boxed conjunction is false at predecessor world 0, and X defects at every world n ≥ 1.

Against FairBot, d is FairBot's action against DefectBot. It is true at world 0 and false at every world m ≥ 1. Therefore d → □⊥ holds at every world. X's formula against FairBot is consequently equivalent, world by world, to □a, the rule FairBot also uses. Induction on n shows both actions are true at every world: at world 0 both boxes are vacuous, and at each subsequent world each agent has cooperated at every predecessor.

Against itself, d is X's action against DefectBot, again true at world 0 and false thereafter. Thus d → □⊥ again holds at every world. The self-action satisfies x(n) = ∧_{m<n} x(m), so induction gives cooperation at every world.

The reference checker reports:

    depth 2; vs CooperateBot D, vs DefectBot D, vs FairBot C (FairBot replies C), vs itself C; prudent: YES

## Impossibility at every smaller depth, regardless of formula size

Let Z be any fully modalized formula of depth at most 1. Because every atom is boxed and boxes cannot be nested, Z is a Boolean combination of constants and formulas □ψ, where ψ is propositional in a,c,d (possibly with constants).

Against CooperateBot, the triple (a,c,d) is (1,1,1) at every world. At any world n ≥ 1, therefore, each □ψ has the fixed truth value ψ(1,1,1). It follows that Z's action against CooperateBot is constant from world 1 onward. If Z defects against CooperateBot in the stable outcome, it must defect against it at world 1.

At world 0, FairBot cooperates with every opponent, since its defining box is vacuous. In particular, when Z faces FairBot, its opponent-relative triple (a,c,d) at world 0 is also (1,1,1): these are FairBot's actions against Z, CooperateBot, and DefectBot. At world 1, every box □ψ in Z consequently has exactly the same truth value against FairBot as against CooperateBot. Their Boolean combinations agree as well. Thus

    Z(FairBot, 1) = Z(CooperateBot, 1) = D.

But FairBot's action against Z at world n is the conjunction of Z's actions against FairBot at all worlds m < n. The defection at world 1 forces FairBot to defect against Z at every world n ≥ 2. This contradicts the required stable mutual cooperation with FairBot.

This argument covers every depth-at-most-1 formula, including depth 0, and imposes no size bound. Hence the smallest possible modal depth is exactly 2.

## Minimal size bound and characterization at depth 2

Counting each atom, constant, unary operator ($\neg, \square$), and binary connective ($\wedge, \vee, \to$) as one syntax-tree node (ignoring parentheses):
- **With constants ($\top, \bot$): the minimum size of a prudent agent is exactly 7**, achieved (uniquely up to commutativity of $\wedge$) by
  $$\square(a \wedge (d \to \square \bot)).$$
- **Without constants: the minimum size of a prudent agent is exactly 8**, achieved by the six formulas
  $$\square(a \wedge (d \to \square \neg p)) \quad \text{and} \quad \square((d \to \square \neg p) \wedge a) \quad \text{for } p \in \{a, c, d\}.$$
  This directly explains the empirical observation in the problem statement that none of the formulas up to depth 2 and 7 symbols without constants is prudent.

**Why these bounds are tight:** Any syntax tree with $L$ leaves (atoms/constants), $B_{\text{bin}} = L - 1$ binary connectives, and $U$ unary operators has total size $S = 2L - 1 + U$. Since modal depth is at least $2$, at least two $\square$ operators must appear ($U \ge 2$), giving $S \ge 2L + 1$.
1. Any prudent formula must contain the atom $d$: if $d$ is absent, then under mutual cooperation with FairBot we have $(a, c) = (1, 1)$ at every world against both CooperateBot and FairBot, so $X$ cannot defect against CooperateBot while cooperating with FairBot. It must also reference $a$ (to distinguish DefectBot from FairBot/itself) and have a leaf inside the inner box $\square \chi$ that evaluates to $0$ at world $0$, requiring $L \ge 3$ leaves and thus $S \ge 7$. (Exhaustive enumeration of all fully modalized depth-2 formulas of size $\le 6$ with constants confirms 0 are prudent.)
2. Without constants, if $L = 3$ and $S = 7$, then $U = 2$, so the only unary operators are the two $\square$'s and no $\neg$ occurs anywhere. Since $\wedge, \vee, \to$ are all truth-preserving ($f(1,1)=1$) and $(a,c,d)=(1,1,1)$ at world $0$ against CooperateBot and FairBot, every subformula evaluates to $1$ at world $0$, so the inner box remains $1$ at world $1$ and cannot distinguish world $0$ from world $1$. Hence at least one $\neg$ ($U \ge 3$, giving $S \ge 8$) or a fourth leaf ($L \ge 4$, giving $S \ge 9$) is required.

**Characterization of depth-2 prudent agents:** At depth 2, an inner box $\square \chi$ (such as $\square \bot$ or $\square \neg p$) acts as a *world-0 detector*: because $(a, c, d) = (1, 1, 1)$ at world $0$ against CooperateBot, FairBot, and (for prudent $X$) $X$ itself, any inner formula $\chi$ that is false on $(1, 1, 1)$ makes $\square \chi$ true at world $0$ and false at all worlds $m \ge 1$. Combining this world-0 exception with $\neg d$ at worlds $m \ge 1$ (via $d \to \square \chi$ inside an outer $\square$, or $\square \square \chi \vee \neg \square d$ outside) allows $X$ to forgive the vacuous world-0 cooperation with DefectBot ($d(0) = 1$) that FairBot and $X$ exhibit, while punishing CooperateBot's persistent cooperation with DefectBot ($d(1) = 1$) at world $n = 2$—late enough that FairBot has already verified $X(1) = C$—and simultaneously requiring $\square a$ to defect against DefectBot at world $1$ and sustain mutual cooperation with FairBot and itself.
