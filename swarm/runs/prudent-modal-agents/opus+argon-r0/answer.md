# Prudent modal agents — answer

FORMULA: B(a & (d -> B(F)))
DEPTH: 2

(i.e. φ_X = □(a ∧ (d → □⊥)): "PA proves that Y cooperates with me, and that if Y cooperates with DefectBot then PA is
inconsistent". Equivalent in spirit to PrudentBot `B(a) & B(~B(F) -> ~d)`, which is also prudent.)

## 1. Outcome table (check.py: `depth 2; vs CooperateBot D, vs DefectBot D, vs FairBot C (FairBot replies C), vs itself C; prudent: YES`)

| opponent     | X's action | opponent's action vs X |
|--------------|-----------|------------------------|
| CooperateBot | D         | C                      |
| DefectBot    | D         | D                      |
| FairBot      | C         | C                      |
| X itself     | C         | C                      |

Hand check. Write X(n) for X's value at world n.
- vs CooperateBot: a=c=d=⊤ at all worlds, so d→□⊥ is false at worlds ≥1, hence X(n)=⊥ for n≥2. Defects.
- vs DefectBot: a=⊥ everywhere, so X(n)=⊥ for n≥1. Defects.
- vs FairBot: c=⊤, d = □⊥ (FairBot vs DefectBot) which is true exactly at world 0, so d→□⊥ holds at every world.
  Inductively, if X(m) for all m<n then FairBot(m)=□X holds for m≤n, so a holds at all m<n and X(n) holds.
  So X and FairBot are ⊤ at all worlds: mutual cooperation.
- vs itself: here d = "X cooperates with DefectBot", and by the DefectBot row X vs DefectBot is □(⊥ ∧ …), true
  exactly at world 0. So d(m)=⊤ iff m=0, and □⊥ is also true exactly at world 0, so d→□⊥ holds at every world. Then
  by the same induction as for FairBot (a(m) = X(m)), X(n)=⊤ for all n: X cooperates with itself.
  (Against FairBot, d = □⊥ is likewise true iff m=0, which is why d→□⊥ holds there too.)

## 2. No agent of modal depth < 2 is prudent (any size)

**Key fact.** vs FairBot at world 0: a = FairBot's action vs X at world 0 = □(…) = ⊤; c = FairBot vs CooperateBot = □⊤ = ⊤;
d = FairBot vs DefectBot = □⊥ at world 0 = ⊤. So the atom triple at world 0 against FairBot is (⊤,⊤,⊤),
the same as against CooperateBot (where it is (⊤,⊤,⊤) at every world).

**Depth 0.** A fully modalized formula without boxes contains no atoms, so it is a constant. ⊤ cooperates with
CooperateBot; ⊥ defects against FairBot. Neither is prudent.

**Depth 1.** Then φ_X is a Boolean combination of constants and boxes □ψ_1,…,□ψ_k where each ψ_i is a Boolean
(box-free) formula in a, c, d and constants. At world n, □ψ_i is true iff ψ_i is true at every world m<n, and ψ_i at
world m depends only on the atom triple at world m.

- Against CooperateBot the atom triple is (⊤,⊤,⊤) at every world, so for every n ≥ 1, □ψ_i(n) = ψ_i(⊤,⊤,⊤).
  Hence X's value vs CooperateBot is the same at all worlds n ≥ 1; call it v. That is the stable outcome, and
  prudence requires v = ⊥.
- Against FairBot at world 1: □ψ_i(1) = ψ_i(atoms at world 0) = ψ_i(⊤,⊤,⊤) by the key fact. So X's value vs FairBot at
  world 1 equals v = ⊥.
- FairBot's action vs X at world n ≥ 2 is □(X vs FairBot) = ⋀_{m<n} X(m), which is ⊥ since X(1)=⊥. So FairBot defects
  against X (stable value ⊥), contradicting prudence.

Hence no agent of depth ≤ 1 is prudent, regardless of formula size, and the minimal depth is exactly 2. ∎

(Intuition: a depth-1 agent can only look at what the opponent does "in world 0", and at world 0 FairBot is
indistinguishable from CooperateBot — both cooperate with everything, including DefectBot. Distinguishing them needs
"PA+Con(PA)", i.e. a nested box.)

## 3. Minimal size at depth 2

Size = number of symbols counting each atom, constant, ~, &, |, ->, and B(...) as 1 (parentheses free).

Exhaustive search (no semantic deduplication) over **all** fully modalized formulas of depth ≤ 2 with
connectives {~, &, |, ->}, atoms a, c, d, constants T, F, sizes 1–7 (`/work/opus/raw.py`, evaluator
`/work/opus/fastcheck.py`, cross-checked against `/work/check.py` on 3000 random formulas with 0 mismatches):

| size | formulas | prudent |
|------|----------|---------|
| 1 | 2 | 0 |
| 2 | 7 | 0 |
| 3 | 29 | 0 |
| 4 | 203 | 0 |
| 5 | 1168 | 0 |
| 6 | 8522 | 0 |
| 7 | 59492 | 2 |

The only size-7 prudent agents are `B(a & (d -> B(F)))` and its commuted form `B((d -> B(F)) & a)`.
So the minimal size of a prudent agent is **7**, attained uniquely (up to commuting ∧) by □(a ∧ (d → □⊥)).
Note it needs the constant ⊥ — consistent with the given evidence that no constant-free formula of ≤7 symbols works.

Without constants, exhaustive search up to size 8 shows the minimal size is **8**, with 52,626 fully modalized depth-2 formulas and exactly 6 prudent ones: `B(a & (d -> B(~x)))` and `B((d -> B(~x)) & a)` for `x` ∈ {`a`, `c`, `d`} (verified prudent by `check.py`). This explains why the Evidence's constant-free search up to 7 symbols found nothing.

**Analytical proof of the size-7 lower bound (and necessity of $d$ at any depth).**
1. *Necessity of atom $d$ (any depth):* For FairBot ($\square a$) to cooperate with $X$ in the limit, $X$ must cooperate with FairBot at *every* world $m \ge 0$, which inductively implies FairBot cooperates with $X$ at every world $m \ge 0$. Since FairBot also cooperates with CooperateBot at every world $m \ge 0$, the atom pair $(a, c)$ is $(\top, \top)$ at every world $m \ge 0$ against both FairBot and CooperateBot. Thus any prudent formula (of any depth) must contain $d$.
2. *Non-monotonicity and $\ge 2$ binary connectives:* Across all worlds $m \ge 0$, the atom triples $(a,c,d)_m$ satisfy the pointwise ordering $\text{DefectBot } (0,0,0) \le \text{FairBot} \le \text{CooperateBot } (1,1,1)$, whereas $X$'s stable outcome must map $(\text{DefectBot}, \text{FairBot}, \text{CooperateBot}) \mapsto (0, 1, 0)$. Since $\square$ is monotone, $\varphi_X$ cannot be monotone or anti-monotone in the atoms, so it requires at least 2 leaves (and in fact at least 2 binary connectives: one to allow $d_0=1$ at world $0$ while forbidding $d_1=1$ at world $1$ via a nested box as in $d \to \square\bot$, and a second to rule out DefectBot where $d=0$ everywhere, since $\square(d \to \square\bot)$ alone has size 5 and cooperates with DefectBot). With $\ge 2$ boxes (depth $\ge 2$), $\ge 2$ binary connectives, and therefore $\ge 3$ leaves, the symbol count is at least $2 + 2 + 3 = 7$ (and $8$ without constants, since the inner box needs a negated atom $\neg x$ to be false at world $0$ against FairBot where all atoms are $\top$).

Characterization remark: all these agents work because, at depth 2, the conjunct "d → □⊥" (or □(d → □¬d)) is
exactly "PA+Con(PA) proves Y defects against DefectBot": it holds along any run where the opponent's action vs
DefectBot is ⊤ only at world 0 (FairBot, X itself) and fails at world 1 against CooperateBot, the one place where
FairBot and CooperateBot differ (world 1 sees FairBot's d=□⊥ already false).
