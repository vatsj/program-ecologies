# Prudent modal agents — answer (opus)

FORMULA: (B(a)|B(~a))->B(F)
DEPTH: 1

i.e. φ_X = (□a ∨ □¬a) → □⊥, which is the same as □⊥ ∨ (¬□a ∧ ¬□¬a).

`python3 check.py "(B(a)|B(~a))->B(F)"` prints:
`depth 1; vs CooperateBot D, vs DefectBot D, vs FairBot C, vs itself C; prudent: YES`

| opponent      | X's action |
|---------------|-----------|
| CooperateBot  | D |
| DefectBot     | D |
| FairBot       | C |
| itself        | C |

Other prudent depth-1 agents (all confirmed by check.py): `(B(d)|B(~d))->B(F)`, `B(F) | (~B(d)&~B(~d))`,
`(B(d)&B(~d)) | (~B(d)&~B(~d))`.

## 1. Minimal depth is 1

A fully modalized formula of depth 0 has no boxes, so it cannot contain atoms. It is built from ⊤, ⊥ and connectives,
so it has the same truth value against every opponent. It cannot both defect against CooperateBot and cooperate with
FairBot. So no depth-0 agent is prudent. That covers formulas of every size. The formula above has depth 1, so the
minimal depth is exactly 1.

## 2. Why depth 1 works: reduction and full characterization

**Reduction.** Let φ have depth 1. Every atom sits inside a box, and no box is nested inside another. So φ is a Boolean
combination of ⊤, ⊥ and boxes □ψ, where each ψ is propositional in a, c, d. Fix an opponent Y and write t_m ∈ {0,1}^3
for the value of (a, c, d) at world m. At world n, □ψ is true iff ψ holds at every t_m with m < n. So X's action at
world n depends only on the set S_n = {t_m : m < n}. It equals f(S_n) for some f : P({0,1}^3) → {0,1} determined by φ.

Conversely, every f is realized by some depth-1 formula. Take ψ_S = the disjunction of the minterms of S. Then □ψ_S is
true at world n iff S_n ⊆ S. Boolean combinations of these boxes pin down S_n exactly.

Note that S_0 = ∅, so f(∅) is the value of φ when every box is true.

**The four games** (triples are written (a,c,d); x_n is X's action at world n):

- **CooperateBot:** t_n = 111 for every n. So S_n = {111} for n ≥ 1, and the outcome is f({111}).
- **DefectBot:** t_n = 000, and the outcome is f({000}).
- **FairBot:** a_n = □x holds iff x_m = 1 for all m < n. Also c = □⊤ = 1, and d_n = □⊥ holds iff n = 0. This gives:
  - t_0 = 111 and x_1 = f({111});
  - t_1 = (x_0, 1, 0) and t_n = (x_0 ∧ x_1, 1, 0) for n ≥ 2;
  - S_n is constant for n ≥ 3.
- **Itself:** a_n = x_n. Also c_n = X's action against CooperateBot at world n, which is f(∅) at n = 0 and f({111})
  after. Likewise d_n is f(∅) at n = 0 and f({000}) after.

**Characterization.** Prudence forces f({111}) = f({000}) = 0. We split on f(∅).

- **If f(∅) = 0:** in self-play t_0 = 000, so x_1 = f({000}) = 0. Then t_1 = 000 again, and by induction S_n = {000}
  and x_n = 0 forever. X defects against itself, so this case is not prudent.
- **If f(∅) = 1:**
  - **Against FairBot:** x_0 = 1 and x_1 = f({111}) = 0. So S_n = {111, 110, 010} for n ≥ 3, and the outcome is
    f({111,110,010}).
  - **Against itself:** t_0 = 111, x_1 = 0 and t_1 = 000. So S_2 = {111, 000}. If f(S_2) = 0, the triple 000 repeats
    forever and X defects. If f(S_2) = 1, then t_2 = 100 and S_3 = {111, 000, 100}. This set is constant afterwards, so
    the outcome is f(S_3).

**Theorem.** A depth-1 agent is prudent iff its f satisfies all six conditions:

f(∅)=1, f({111})=0, f({000})=0, f({111,110,010})=1, f({111,000})=1, f({111,000,100})=1.

Only these six values matter; the other 250 subsets are free. Since every f is realizable, the prudent depth-1 agents
are exactly the depth-1 formulas whose f takes these six values.

**Check of the answer formula.** φ = □⊥ ∨ (¬□a ∧ ¬□¬a):

- At ∅ every box is true, so □⊥ is true and φ = 1.
- On {111} and on {000}, a is constant and □⊥ is false, so φ = 0.
- Each of the other three sets contains triples with a = 1 and with a = 0, so φ = 1.

Intuition: X cooperates iff the opponent's response to X is "not settled at any finite stage" (□a and □¬a both fail)
or PA is inconsistent. CooperateBot and DefectBot are settled at once. FairBot and X itself flip once.

## 3. Minimal size (Q3)

`/work/opus/minsize.py` runs an exhaustive dynamic program over depth-1 formulas, using the six-value characterization
above. It returns the smallest formula for each reachable vector of values on the six sets.

- **Size measure:** the number of symbols — atoms, T, F, ~, &, |, ->, B. Parentheses are not counted.
- **With constants:** the minimum size is **9**, attained by `(B(a)|B(~a))->B(F)`.
- **Without constants** (`/work/opus/minsize_noconst.py`): the minimum is **12**, attained by
  `(B(a)|B(~a))->B(~(a->a))`.

Both results agree with the provided evidence that nothing with ≤ 7 symbols and no constants is prudent.

Proving optimality over all depths, not just depth 1, was not attempted. A depth-2 formula could in principle be
shorter, although the given evidence rules out ≤ 7 symbols without constants.
