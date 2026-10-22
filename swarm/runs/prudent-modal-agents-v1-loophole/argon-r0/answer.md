FORMULA: (B(d) | B(~d)) -> B(F)
DEPTH: 1

---

# Prudent Modal Agents: Solution, Proofs, and Characterization

## 1. Existence and Minimal Modal Depth (Question 1)

**Yes, prudent agents exist, and the smallest possible modal depth of a prudent agent is $d = 1$.**

### 1.1 Minimal-Depth Prudent Agents ($d = 1$)

Below are prudent agents of **modal depth $1$** attaining the minimum possible formula sizes in each syntactic class (where symbol count is the number of atoms, constants, connectives, and box operators, excluding parentheses):

1. **Minimal size at modal depth 1 (with constants — 9 symbols):**
   $$\varphi_X \;=\; (\Box d \lor \Box \neg d) \to \Box \bot \qquad\text{(`(B(d) | B(~d)) -> B(F)`)}$$
   *(Equivalently, using only atom $a$: `(B(a) | B(~a)) -> B(F)`.)*

2. **Minimal size at modal depth 1 (without constants — 12 symbols):**
   $$\varphi_X \;=\; (\Box d \lor \Box \neg d) \to \Box(d \land \neg d) \qquad\text{(`(B(d) | B(~d)) -> B(d & ~d)`)}$$
   *(Equivalently, using only atom $a$: `(B(a) | B(~a)) -> B(a & ~a)`.)*

3. **Minimal size at modal depth 1 using only 2 distinct boxed subformulas (without constants — 13 symbols):**
   $$\varphi_X \;=\; (\Box d \to \Box \neg d) \land (\Box \neg d \to \Box d) \qquad\text{(`(B(d) -> B(~d)) & (B(~d) -> B(d))`)}$$
   *(Equivalently, $\Box d \leftrightarrow \Box \neg d$, or using only atom $a$: `(B(a) -> B(~a)) & (B(~a) -> B(a))`.)*

Running `python3 check.py "(B(d) | B(~d)) -> B(F)"` (and likewise on the constant-free formulas above) outputs:
```text
depth 1; vs CooperateBot D, vs DefectBot D, vs FairBot C, vs itself C; prudent: YES
```

### 1.2 Outcome Table and World-by-World Evaluation

For both $\varphi_X = (\Box d \lor \Box \neg d) \to \Box \bot$ and $\varphi_X = (\Box d \to \Box \neg d) \land (\Box \neg d \to \Box d)$, the stabilized outcome table and the world-by-world actions $x_Y(n) = \text{act}(X, Y, n)$ and opponent actions $a_Y(n) = \text{act}(Y, X, n)$ across worlds $n = 0, 1, 2, \dots$ are:

| Opponent $Y$ | World $n=0$ ($X, Y$) | World $n=1$ ($X, Y$) | World $n=2$ ($X, Y$) | World $n \ge 3$ ($X, Y$) | **Stabilized Outcome ($X$ vs $Y$)** |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **CooperateBot** ($\top$) | $(\text{C}, \text{C})$ | $(\text{D}, \text{C})$ | $(\text{D}, \text{C})$ | $(\text{D}, \text{C})$ | **D** ($X$ defects, CB cooperates) |
| **DefectBot** ($\bot$) | $(\text{C}, \text{D})$ | $(\text{D}, \text{D})$ | $(\text{D}, \text{D})$ | $(\text{D}, \text{D})$ | **D** ($X$ defects, DB defects) |
| **FairBot** ($\Box a$) | $(\text{C}, \text{C})$ | $(\text{D}, \text{C})$ | $(\text{C}, \text{D})$ | $(\text{C}, \text{D})$ | **C** ($X$ cooperates, FB defects*) |
| **Itself** ($X$) | $(\text{C}, \text{C})$ | $(\text{D}, \text{D})$ | $(\text{C}, \text{C})$ | $(\text{C}, \text{C})$ | **C** ($X$ cooperates with itself) |

*(Note: For `(B(a) | B(~a)) -> B(F)` and `(B(a) -> B(~a)) & (B(~a) -> B(a))`, the only change is at world $n=2$ against FairBot, where $X$ plays $\text{D}$ before stabilizing at $\text{C}$ for all $n \ge 3$. Against a prudent agent $X$ of modal depth $2$ such as `B(a & (d -> B(F)))` or `B(a & (d -> B(~d)))`, $X$ cooperates at every world $n \ge 0$ against both FairBot and itself: see Section 3.3 below.)*

**Why $(\Box d \lor \Box \neg d) \to \Box \bot$ (or $\Box d \leftrightarrow \Box \neg d$) works:**
- **At world $n = 0$:** Every boxed formula $\Box \psi$ is vacuously true ($1$) because there are no worlds $m < 0$. Because $\Box d$, $\Box \neg d$, and $\Box \bot$ are all $1$ at $n = 0$, the formula evaluates to **$1$ ($\text{C}$)** at world $0$ against every opponent.
- **Against CooperateBot ($n \ge 1$):** CooperateBot cooperates with DefectBot at every world ($d = 1$ for all $m \ge 0$). Thus for all $n \ge 1$, $\Box d = 1$, $\Box \neg d = 0$, and $\Box \bot = 0$, so $\varphi_X$ evaluates to **$0$ ($\text{D}$)**.
- **Against DefectBot ($n \ge 1$):** DefectBot defects against DefectBot at every world ($d = 0$ for all $m \ge 0$). Thus for all $n \ge 1$, $\Box d = 0$, $\Box \neg d = 1$, and $\Box \bot = 0$, so $\varphi_X$ evaluates to **$0$ ($\text{D}$)**.
- **Against FairBot ($n \ge 1$):** FairBot ($\Box a$) cooperates with DefectBot vacuously at world $0$ ($d = 1$ at $m = 0$) and defects against DefectBot at all worlds $m \ge 1$ ($d = 0$ for $m \ge 1$). At world $n = 1$, only $m = 0$ ($d = 1$) is visible, so $\Box d = 1, \Box \neg d = 0 \implies \varphi_X = 0$ ($\text{D}$). For all worlds $n \ge 2$, both $m = 0$ ($d = 1$) and $m = 1$ ($d = 0$) lie below $n$, so **both** $\Box d = 0$ and $\Box \neg d = 0$, making $\varphi_X$ evaluate to **$1$ ($\text{C}$)** for all $n \ge 2$.
- **Against itself ($n \ge 1$):** Because $X$ cooperated with DefectBot at world $0$ and defected against DefectBot at world $1$, $X$'s own action against DefectBot has $d = 1$ at $m = 0$ and $d = 0$ at $m = 1$. Thus for all $n \ge 2$, both $\Box d = 0$ and $\Box \neg d = 0$, so $\varphi_X$ evaluates to **$1$ ($\text{C}$)** for all $n \ge 2$.

---

## 2. Impossibility of Smaller Modal Depth (Question 2)

### Theorem 1 (Impossibility at Modal Depth $0$)
*No agent of modal depth $0$ (for formulas of any size) is prudent.*

**Proof.**
By definition, an agent's formula $\varphi_X$ must be **fully modalized**: every occurrence of an atom $a, c, d$ must lie inside at least one box $\Box$. A formula of modal depth $0$ contains no occurrences of $\Box$, and therefore cannot contain any atoms $a, c, d$. Consequently, any fully modalized formula $\varphi_X$ of modal depth $0$ (regardless of size) is a pure propositional combination of the constants $\top$ and $\bot$ using $\neg, \land, \lor, \to$.

Every such formula evaluates to a constant truth value $v \in \{\text{True}, \text{False}\}$ across all worlds $n \ge 0$ and against all opponents $Y$:
- If $v = \text{True}$, then $X$ is equivalent to CooperateBot and cooperates with CooperateBot and DefectBot (violating prudence).
- If $v = \text{False}$, then $X$ is equivalent to DefectBot and defects against FairBot and itself (violating prudence).

Hence no agent of modal depth $< 1$ is prudent. $\blacksquare$

*(Note: Moreover, as we prove in Theorem 2 and Corollary 1 below, even at modal depth $1$, no formula with fewer than $3$ occurrences of $\Box$—in particular, no formula of the form $\Box \psi$ or $\neg \Box \psi$ for a depth-$0$ formula $\psi$ of any size—can be prudent. Thus, if an agent is required to have a single outer box $\varphi_X = \Box \psi$, the minimal modal depth is $d = 2$, achieved by `B(a & (d -> B(F)))`.)*

---

## 3. Complete Characterization and Minimal Size Bounds (Question 3)

### 3.1 Exact Characterization of All Prudent Agents of Modal Depth $1$

For any opponent $Y \in \{\text{CB}, \text{DB}, \text{FB}, \text{X}\}$ and world $m \ge 0$, let
$$\sigma_Y(m) \;=\; \bigl(a_Y(m),\; c_Y(m),\; d_Y(m)\bigr) \;\in\; \{0, 1\}^3$$
be the atomic valuation at world $m$ when $X$ plays against $Y$, where $a_Y(m) = \text{act}(Y, X, m)$, $c_Y(m) = \text{act}(Y, \text{CB}, m)$, and $d_Y(m) = \text{act}(Y, \text{DB}, m)$. Let $x_Y(n) = \text{act}(X, Y, n) \in \{0, 1\}$.

Any fully modalized formula $\varphi_X$ of modal depth $1$ is a boolean combination $G(\Box \psi_1, \dots, \Box \psi_k)$ of boxed modal-depth-$0$ formulas $\psi_i(a, c, d)$. At world $n$, each $\Box \psi_i$ holds iff $\psi_i(\sigma_Y(m)) = 1$ for all $m < n$, which depends **only on the set of atomic valuations occurring below $n$**:
$$S_Y(n) \;=\; \{\sigma_Y(m) : 0 \le m < n\} \;\subseteq\; \{0, 1\}^3.$$
Thus every depth-$1$ formula $\varphi_X$ induces a boolean function $f : \mathcal{P}(\{0, 1\}^3) \to \{0, 1\}$ such that $x_Y(n) = f(S_Y(n))$ for all $Y$ and $n \ge 0$. Conversely, every function $f : \mathcal{P}(\{0, 1\}^3) \to \{0, 1\}$ is realizable at modal depth $1$, because for each $v \in \{0, 1\}^3$ the indicator $\mathbb{I}[v \in S_Y(n)]$ is expressed by the depth-$1$ formula $\neg \Box \neg \delta_v$, where $\delta_v$ is the minterm conjunction of literals over $a, c, d$ defining $v$.

#### Theorem 2 (Characterization of Prudent Depth-$1$ Agents)
*A fully modalized formula $\varphi_X$ of modal depth $1$, with induced subset function $f : \mathcal{P}(\{0, 1\}^3) \to \{0, 1\}$, is prudent if and only if $f$ satisfies the following six conditions:*
$$\begin{aligned}
\text{\textbf{(C1)}} &\quad f(\{(1, 1, 1)\}) = 0, &
\text{\textbf{(C2)}} &\quad f(\{(0, 0, 0)\}) = 0, &
\text{\textbf{(C3)}} &\quad f(\emptyset) = 1, \\
\text{\textbf{(C4)}} &\quad f(\{(1, 1, 1), (0, 0, 0)\}) = 1, &
\text{\textbf{(C5)}} &\quad f(\{(1, 1, 1), (0, 0, 0), (1, 0, 0)\}) = 1, &
\text{\textbf{(C6)}} &\quad f(\{(1, 1, 1), (1, 1, 0), (0, 1, 0)\}) = 1.
\end{aligned}$$

**Proof.**
1. **Against $\text{CB}$ and $\text{DB}$:**
   For all $m \ge 0$, $\sigma_{\text{CB}}(m) = (1, 1, 1)$ and $\sigma_{\text{DB}}(m) = (0, 0, 0)$. Hence for all $n \ge 1$, $S_{\text{CB}}(n) = \{(1, 1, 1)\}$ and $S_{\text{DB}}(n) = \{(0, 0, 0)\}$. Thus $x_{\text{CB}}(n) = f(\{(1, 1, 1)\})$ and $x_{\text{DB}}(n) = f(\{(0, 0, 0)\})$ for all $n \ge 1$. Defecting against $\text{CB}$ and $\text{DB}$ is therefore equivalent to **(C1)** and **(C2)**.

2. **Necessity of $f(\emptyset) = 1$ (World $0$):**
   At $n = 0$, $S_Y(0) = \emptyset$ for all $Y$, so $x_{\text{CB}}(0) = x_{\text{DB}}(0) = x_{\text{FB}}(0) = x_{\text{X}}(0) = v_0 := f(\emptyset)$.
   When $Y = X$, $\sigma_X(m) = (x_X(m), x_{\text{CB}}(m), x_{\text{DB}}(m))$. Thus $\sigma_X(0) = (v_0, v_0, v_0)$.
   Suppose $v_0 = 0$. Then $\sigma_X(0) = (0, 0, 0)$. By induction on $n \ge 1$, if $\sigma_X(m) = (0, 0, 0)$ for all $m < n$, then $S_X(n) = \{(0, 0, 0)\}$, so by (C2) $x_X(n) = f(\{(0, 0, 0)\}) = 0$, and since $x_{\text{CB}}(n) = x_{\text{DB}}(n) = 0$ for all $n \ge 1$, $\sigma_X(n) = (0, 0, 0)$ as well. Hence $x_X(n) = 0$ for all $n \ge 0$ ($X$ defects against itself). Thus prudence requires **(C3)** $f(\emptyset) = 1$.

3. **Trajectory against itself ($Y = X$) given (C1)–(C3):**
   With $f(\emptyset) = 1$, we have $\sigma_X(0) = (1, 1, 1)$, so $S_X(1) = \{(1, 1, 1)\}$. By (C1), $x_X(1) = f(\{(1, 1, 1)\}) = 0$, which gives $\sigma_X(1) = (0, 0, 0)$ and hence $S_X(2) = \{(1, 1, 1), (0, 0, 0)\}$.
   - If $f(\{(1, 1, 1), (0, 0, 0)\}) = 0$, then $x_X(2) = 0 \implies \sigma_X(2) = (0, 0, 0) \implies S_X(n) = \{(1, 1, 1), (0, 0, 0)\}$ and $x_X(n) = 0$ for all $n \ge 2$. Thus **(C4)** $f(\{(1, 1, 1), (0, 0, 0)\}) = 1$ is necessary.
   - Given (C4), $x_X(2) = 1$, so $\sigma_X(2) = (1, 0, 0)$ and $S_X(3) = \{(1, 1, 1), (0, 0, 0), (1, 0, 0)\}$. At every $n \ge 3$, $\sigma_X(n-1) = (x_X(n-1), 0, 0) \in \{(0, 0, 0), (1, 0, 0)\} \subseteq S_X(3)$, so $S_X(n) = S_X(3)$ is constant for all $n \ge 3$. Thus $x_X(n)$ stabilizes at $1$ iff **(C5)** $f(\{(1, 1, 1), (0, 0, 0), (1, 0, 0)\}) = 1$ holds.

4. **Trajectory against FairBot ($Y = \text{FB}$) given (C1)–(C3):**
   At $m = 0$, $\sigma_{\text{FB}}(0) = (1, 1, 1)$ because $\Box a$ holds vacuously at world $0$. Thus $S_{\text{FB}}(1) = \{(1, 1, 1)\}$, and by (C1), $x_{\text{FB}}(1) = f(\{(1, 1, 1)\}) = 0$.
   - At $m = 1$: since $x_{\text{FB}}(0) = 1$, FairBot cooperates with $X$ ($a_{\text{FB}}(1) = 1$), cooperates with $\text{CB}$ ($c_{\text{FB}}(1) = 1$), and defects against $\text{DB}$ ($d_{\text{FB}}(1) = 0$), so $\sigma_{\text{FB}}(1) = (1, 1, 0)$ and $S_{\text{FB}}(2) = \{(1, 1, 1), (1, 1, 0)\}$.
   - For all $m \ge 2$: because $x_{\text{FB}}(1) = 0$, FairBot defects against $X$ at every world $m \ge 2$ ($a_{\text{FB}}(m) = \bigwedge_{j < m} x_{\text{FB}}(j) = 0$), so $\sigma_{\text{FB}}(m) = (0, 1, 0)$ for all $m \ge 2$.
   Consequently, for all $n \ge 3$, $S_{\text{FB}}(n) = \{(1, 1, 1), (1, 1, 0), (0, 1, 0)\}$, so $x_{\text{FB}}(n)$ stabilizes at $1$ iff **(C6)** holds. $\blacksquare$

**Sufficient 2-Box / 3-Box Criterion:**
Let $\psi_1, \psi_2$ be any two modal-depth-$0$ formulas such that:
- $\psi_1(1, 1, 1) = 1$, $\psi_1(0, 0, 0) = 0$, and $\psi_1$ is false on at least one of $(1, 1, 0)$ or $(0, 1, 0)$ (for instance, $\psi_1 = d$ or $\psi_1 = a$);
- $\psi_2(1, 1, 1) = 0$ and $\psi_2(0, 0, 0) = 1$ (for instance, $\psi_2 = \neg a$, $\neg c$, or $\neg d$).

Then for any modal-depth-$0$ formula $\psi_3$ with $\psi_3(1, 1, 1) = \psi_3(0, 0, 0) = 0$ (e.g., $\psi_3 = \bot$ or $\psi_3 = d \land \neg d$), both
$$(\Box \psi_1 \lor \Box \psi_2) \to \Box \psi_3 \qquad\text{and}\qquad (\Box \psi_1 \to \Box \psi_2) \land (\Box \psi_2 \to \Box \psi_1)$$
satisfy (C1)–(C6) and are therefore prudent agents of modal depth $1$.

---

### 3.2 Exact Minimal Formula Size Bounds at Modal Depth $1$

#### Corollary 1 (Minimum Box Occurrences and Exact Symbol Counts at Modal Depth $1$)
*Let $\varphi_X$ be any prudent formula of modal depth $1$, written as $G(b_1, \dots, b_m)$ where $b_1, \dots, b_m$ ($b_i = \Box \psi_i$) are all $m$ occurrences of $\Box$ in $\varphi_X$ and $G$ is a read-once formula over $b_1, \dots, b_m$ in the basis $\{\neg, \land, \lor, \to, \top, \bot\}$. Then:*
1. *$m \ge 3$ (no formula of modal depth $1$ with $1$ or $2$ occurrences of $\Box$ is prudent; in particular, no single-box formula $\Box \psi$ or $\neg \Box \psi$ of modal depth $1$ is prudent).*
2. *If constants $\top, \bot$ are allowed, the minimum symbol count of a prudent depth-$1$ formula is **$9$** (attained by the $12$ formulas `(B(x) | B(~y)) -> B(F)` and `(B(~y) | B(x)) -> B(F)` for $x \in \{a, d\}$ and $y \in \{a, c, d\}$).*
3. *If constants $\top, \bot$ are not allowed, the minimum symbol count of a prudent depth-$1$ formula is **$12$** (attained e.g. by `(B(d) | B(~d)) -> B(d & ~d)` and `(B(a) | B(~a)) -> B(a & ~a)`), and if restricted to $2$ distinct boxed subformulas ($m = 4$ occurrences), the minimum symbol count is **$13$** (attained e.g. by `(B(d) -> B(~d)) & (B(~d) -> B(d))`).*

**Proof.**
For each box occurrence $b_i = \Box \psi_i$, let $u_i = \psi_i(1, 1, 1) \in \{0, 1\}$ and $v_i = \psi_i(0, 0, 0) \in \{0, 1\}$. On the four subsets $S_0 = \emptyset$, $S_1 = \{(1, 1, 1)\}$, $S_2 = \{(0, 0, 0)\}$, and $S_3 = \{(1, 1, 1), (0, 0, 0)\}$, the vector $b = (b_1, \dots, b_m)$ takes the four values:
$$\mathbf{1} = (1, \dots, 1), \qquad u = (u_1, \dots, u_m), \qquad v = (v_1, \dots, v_m), \qquad u \land v = (u_1 \land v_1, \dots, u_m \land v_m).$$
By (C1)–(C4), $G$ must satisfy $G(\mathbf{1}) = 1$, $G(u) = 0$, $G(v) = 0$, and $G(u \land v) = 1$.

1. **Why $m \ge 3$:**
   Since $G(u) = 0 \neq 1 = G(u \land v)$, we must have $u \neq u \land v$, so there exists $i$ with $(u_i, v_i) = (1, 0)$. Symmetrically, $v \neq u \land v$ implies there exists $j$ with $(u_j, v_j) = (0, 1)$. Thus $m \ge 2$ and at least two distinct $\psi_i, \psi_j$ are required.
   If $m = 2$, then up to swapping $b_1, b_2$, we have $\mathbf{1} = (1, 1)$, $u = (1, 0)$, $v = (0, 1)$, and $u \land v = (0, 0)$. Then $G(1, 1) = 1, G(1, 0) = 0, G(0, 1) = 0, G(0, 0) = 1$, so $G(b_1, b_2)$ is the biconditional $b_1 \leftrightarrow b_2$. However, every read-once binary formula in $\{\neg, \land, \lor, \to\}$ over $b_1, b_2$ has an odd number of $1$s ($1$ or $3$) in its $4$-row truth table, whereas $b_1 \leftrightarrow b_2$ has two $1$s. Thus no read-once formula in $m = 2$ variables can compute $G$, proving $m \ge 3$.

2. **Minimum symbol count with constants ($9$ symbols):**
   Any formula with $m \ge 3$ occurrences of $\Box$ requires at least $m - 1$ binary connectives outside the boxes, and each $B(\psi_i)$ has symbol count $1 + |\psi_i|$. Moreover, any depth-$0$ formula $\psi_j$ with $(u_j, v_j) = (0, 1)$ cannot be a constant or positive atom, so $|\psi_j| \ge 2$ (e.g., `~d`). For $m \ge 3$, the total symbol count is therefore at least
   $$\sum_{i=1}^3 (1 + |\psi_i|) + (m - 1) \;\ge\; (1 + 1) + (1 + 2) + (1 + 1) + 2 \;=\; 9.$$
   This lower bound of $9$ is matched by `(B(d) | B(~d)) -> B(F)`.

3. **Minimum symbol count without constants ($12$ symbols):**
   Suppose constants $\top, \bot$ are forbidden.
   - If $m = 3$: any read-once $3$-variable boolean formula $G(b_1, b_2, b_3)$ has the form $\ell_x \odot (\ell_y \star \ell_z)$ up to negation, where $\odot, \star \in \{\land, \lor\}$ and $\ell_x, \ell_y, \ell_z$ are literals. If $\odot = \land$, then $\ell_x = 1$ on both $\mathbf{1}$ and $u \land v$, forcing $u_x = v_x = 1$ and reducing $\ell_y \star \ell_z$ to a $2$-variable read-once XNOR, which is impossible. Thus $\odot = \lor$ and $\star = \land$, i.e. $G = \ell_x \lor (\ell_y \land \ell_z)$. Since $G(u) = G(v) = 0$, we must have $\ell_x = 0$ on both $u$ and $v$, so $u_x = v_x$, which implies $u_x \land v_x = u_x = v_x$. Hence $\ell_x = 0$ on $u \land v$ as well, forcing $\ell_x = 1$ on $\mathbf{1}$, i.e., $\ell_x = b_x$ and $u_x = \psi_x(1, 1, 1) = 0$, $v_x = \psi_x(0, 0, 0) = 0$.
     Without constants, any depth-$0$ formula $\psi_x$ satisfying $\psi_x(1, 1, 1) = \psi_x(0, 0, 0) = 0$ has size $|\psi_x| \ge 4$ (atoms have $(u, v) = (1, 0)$, negated atoms have $(0, 1)$, and binary combinations of two atoms have $u = 1$; size $4$ is achieved by `d & ~d` or `~(a -> a)`). Together with $|\psi_y| \ge 1$ (`d`) and $|\psi_z| \ge 2$ (`~d`), the total size for $m = 3$ is at least $(1+1) + (1+2) + (1+4) + 2 = 12$.
   - If $m \ge 4$: since at least two occurrences must have $u_i = 0$ (and without constants $u_i = 0 \implies |\psi_i| \ge 2$), the $m$ boxes contribute at least $2 + 2 + 3 + 3 = 10$ symbols (or $2 + 2 + 2 + 5 = 11$) plus $m - 1 \ge 3$ binary connectives $\implies \ge 13$ symbols.
   Hence $12$ symbols is the exact minimum without constants. $\blacksquare$

---

### 3.3 Modal Depth $2$: Global Minimum Symbol Count & Single-Box Agents

If we allow **modal depth $2$** (which is also the minimal modal depth among agents with a **single outer box** $\varphi_X = \Box \psi$), we obtain even shorter formulas that achieve the global minimum symbol count across **all** modal depths:

1. **Global minimum size with constants (7 symbols, modal depth 2):**
   $$\varphi_X \;=\; \Box\bigl(a \land (d \to \Box \bot)\bigr) \qquad\text{(`B(a & (d -> B(F)))`)}$$
2. **Global minimum size without constants (8 symbols, modal depth 2):**
   $$\varphi_X \;=\; \Box\bigl(a \land (d \to \Box \neg d)\bigr) \qquad\text{(`B(a & (d -> B(~d))`)}$$
   *(Equivalently `B(a & (d -> B(~a)))` or `B(a & (d -> B(~c)))`.)*

| Opponent $Y$ | World $n=0$ | World $n=1$ | World $n \ge 2$ | **Stabilized Outcome ($X$ vs $Y$)** |
| :--- | :---: | :---: | :---: | :---: |
| **CooperateBot** ($\top$) | $\text{C}$ | $\text{C}$ | $\text{D}$ | **D** |
| **DefectBot** ($\bot$) | $\text{C}$ | $\text{D}$ | $\text{D}$ | **D** |
| **FairBot** ($\Box a$) | $\text{C}$ | $\text{C}$ | $\text{C}$ | **C** |
| **Itself** ($X$) | $\text{C}$ | $\text{C}$ | $\text{C}$ | **C** |

Exhaustive enumeration (implemented in `/work/verify_prudent.py`) confirms that across all modal depths:
- With constants, $0$ prudent formulas exist of size $\le 6$, and exactly $2$ exist of size $7$: `B(a & (d -> B(F)))` and `B((d -> B(F)) & a)`.
- Without constants, $0$ prudent formulas exist of size $\le 7$, and exactly $6$ exist of size $8$: `B(a & (d -> B(~x)))` and `B((d -> B(~x)) & a)` for $x \in \{a, c, d\}$.
- This explains why the enumeration in the problem statement's *Evidence* section (up to modal depth $2$ and $7$ symbols, without constants) found no prudent agent: the minimum constant-free symbol count is $8$ (at depth $2$) and $12$ (at depth $1$).
