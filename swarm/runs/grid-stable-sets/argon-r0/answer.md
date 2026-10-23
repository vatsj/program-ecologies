# Stable Sets of Majority Division on a Grid

## Summary of Answers

Let $\Delta_K = \{(x_1, x_2, x_3) \in \mathbb{Z}_{\ge 0}^3 : x_1 + x_2 + x_3 = K\}$ denote the set of all allocations for a fixed integer $K \ge 2$.

1. **Existence (Question 1):** A stable set exists if and only if $K$ is **even**.
2. **Classification (Question 2):**
   - For every **even** integer $K = 2m$ ($m \ge 1$), there is a **unique** stable set:
     $$V_K = \{(m, m, 0),\; (m, 0, m),\; (0, m, m)\} = \{(K/2, K/2, 0),\; (K/2, 0, K/2),\; (0, K/2, K/2)\}.$$
   - For every **odd** integer $K \ge 3$, there are **no** stable sets.
   *(Remark: Unlike the continuum game, no "discriminatory" stable sets exist for any $K \ge 2$, because the minimum positive integer increment prevents two coalition partners with fixed total share $K - d$ from simultaneously strictly improving upon an allocation with $y_i = d + 1$, which leaves only $1$ indivisible unit of slack between them.)*

---

## Complete Proofs (Question 3)

### 1. Characterization of Internal Stability

We first characterize when two distinct allocations do not dominate each other.

**Lemma 1 (Incomparability Criterion).** *Two distinct allocations $x, y \in \Delta_K$ do not dominate each other if and only if they agree in at least one coordinate, i.e., $x_i = y_i$ for some $i \in \{1, 2, 3\}$.*

*Proof.* Let $\delta_i = x_i - y_i$ for $i \in \{1, 2, 3\}$. Since $x, y \in \Delta_K$ are distinct, we have $\delta_1 + \delta_2 + \delta_3 = K - K = 0$ and $(\delta_1, \delta_2, \delta_3) \ne (0, 0, 0)$.
- **($\Leftarrow$)** Suppose $x_i = y_i$ for some $i$, so $\delta_i = 0$. The remaining two differences $\delta_j, \delta_k$ satisfy $\delta_j + \delta_k = 0$ and are nonzero, so one is strictly positive and the other is strictly negative. Thus $x$ is strictly greater than $y$ in only one coordinate, and $y$ is strictly greater than $x$ in only one coordinate. Neither dominates the other.
- **($\Rightarrow$)** Suppose $x_i \ne y_i$ for all $i \in \{1, 2, 3\}$, so $\delta_1, \delta_2, \delta_3$ are all nonzero. Because their sum is $0$, they cannot all have the same sign. By the pigeonhole principle, either two of $\{\delta_1, \delta_2, \delta_3\}$ are positive and one is negative (so $x$ dominates $y$), or one is positive and two are negative (so $y$ dominates $x$). $\blacksquare$

---

### 2. Classification of All Internally Stable Sets

Using Lemma 1, we classify all internally stable subsets $V \subseteq \Delta_K$.

**Lemma 2 (Structure of Internally Stable Sets).** *If $V \subseteq \Delta_K$ is internally stable, then one of the following holds:*
1. **(Collinear Case):** *There exist a player $i \in \{1, 2, 3\}$ and an integer $d \in \{0, 1, \dots, K\}$ such that $x_i = d$ for all $x \in V$.*
2. **(Triangular Case):** *$|V| = 3$, and there exist nonnegative integers $a, b, c, a', b', c'$ satisfying*
   $$a + b + c' = a + b' + c = a' + b + c = K \quad \text{and} \quad a \ne a'$$
   *such that*
   $$V = \{(a, b, c'),\; (a, b', c),\; (a', b, c)\}.$$

*Proof.* Suppose $V \subseteq \Delta_K$ is internally stable and does not fall into the Collinear Case. Note that if $|V| \le 2$, then $V$ trivially falls into the Collinear Case (by Lemma 1 if $|V| = 2$). Thus $|V| \ge 3$.

Choose two distinct elements $x, y \in V$. By Lemma 1, they share a coordinate; by symmetry of the three coordinates, assume $x_1 = y_1 = a$ for presentation, and write
$$x = (a, b, c'), \qquad y = (a, b', c).$$
Since $x \ne y$ and $x_1 = y_1 = a$, we have $b \ne b'$ and $c \ne c'$.

Because $V$ is not contained in the line $\{u \in \Delta_K : u_1 = a\}$, there exists an element $z \in V$ with $z_1 \ne a$. By Lemma 1, $z$ must share a coordinate with $x$ and a coordinate with $y$. Since $z_1 \ne a = x_1 = y_1$, $z$ must share coordinate $2$ or $3$ with $x$, and coordinate $2$ or $3$ with $y$:
- $z$ cannot share coordinate $2$ with both $x$ and $y$, since $x_2 = b \ne b' = y_2$;
- $z$ cannot share coordinate $3$ with both $x$ and $y$, since $x_3 = c' \ne c = y_3$.

Hence either $(z_2 = b \text{ and } z_3 = c)$ or $(z_2 = b' \text{ and } z_3 = c')$. By swapping the labels of $x$ and $y$ if necessary, we may assume $z_2 = b$ and $z_3 = c$. Setting $a' = K - b - c$, we have $z = (a', b, c)$ with $a' \ne a$.

We now show that no fourth element $w \in V \setminus \{x, y, z\}$ can exist:
- Suppose first that $w_1 = a$. Then $x, y, w$ are three distinct allocations in $V$ with first coordinate $a$, so their second coordinates $\{x_2, y_2, w_2\}$ are pairwise distinct and their third coordinates $\{x_3, y_3, w_3\}$ are pairwise distinct. By Lemma 1, $z$ (which has $z_1 = a' \ne a$) must share coordinate $2$ or $3$ with each of $x, y, w$. By the pigeonhole principle, $z$ would have to share the same coordinate ($2$ or $3$) with at least two of $\{x, y, w\}$, which is impossible.
- Thus $w_1 \ne a$. Applying the previous paragraph's deduction to $w$ in place of $z$, and noting that $w \ne z = (a', b, c)$, we are forced to have $w_2 = y_2 = b'$ and $w_3 = x_3 = c'$, so $w = (K - b' - c', b', c')$.
- Finally, by Lemma 1, the distinct elements $w, z \in V$ must share a coordinate. However, $w_2 = b' \ne b = z_2$ and $w_3 = c' \ne c = z_3$, so we must have $w_1 = z_1$, i.e.,
  $$K - b' - c' = a'.$$
  Substituting $b' = K - a - c$, $c' = K - a - b$, and $a' = K - b - c$ yields
  $$K - (K - a - c) - (K - a - b) = K - b - c \iff 2(a + b + c - K) = 0 \iff a + b + c = K,$$
  which contradicts $a' = K - b - c \ne a$.

Thus $V = \{x, y, z\}$ has the required form. $\blacksquare$

---

### 3. Elimination of the Collinear Case

**Lemma 3 (No Collinear Stable Set Exists).** *No set $V$ from the Collinear Case of Lemma 2 is externally stable.*

*Proof.* By symmetry, suppose $V \subseteq \{x \in \Delta_K : x_1 = d\}$ for some $d \in \{0, 1, \dots, K\}$.
- **Case 3a ($d = K$):** Here $V \subseteq \{(K, 0, 0)\}$. Consider the allocation $y = (0, K, 0) \in \Delta_K \setminus V$. Any $x \in V$ equals $(K, 0, 0)$ and satisfies $x_2 = 0 \le y_2$ and $x_3 = 0 \le y_3$, so no element of $V$ dominates $y$.
- **Case 3b ($0 \le d \le K - 1$):** Consider the allocation $y = (d + 1, K - d - 1, 0) \in \Delta_K$. Since $y_1 = d + 1 \ne d$, we have $y \notin V$. For any $x = (d, x_2, x_3) \in V$, we have $x_1 = d < d + 1 = y_1$. Therefore, for $x$ to dominate $y$, both of the remaining coordinates must be strictly greater:
  $$x_2 > y_2 \quad \text{and} \quad x_3 > y_3.$$
  Because all shares are integers, this requires $x_2 \ge y_2 + 1$ and $x_3 \ge y_3 + 1$. Summing these inequalities gives
  $$K - d = x_2 + x_3 \ge (y_2 + 1) + (y_3 + 1) = (K - d - 1) + 2 = K - d + 1,$$
  a contradiction. Hence $y$ is not dominated by any element of $V$. $\blacksquare$

---

### 4. Analysis of the Triangular Case

Now suppose $V = \{x, y, z\}$ is an internally stable set from the Triangular Case of Lemma 2:
$$x = (a, b, c'), \qquad y = (a, b', c), \qquad z = (a', b, c),$$
where $a, b, c, a', b', c' \in \mathbb{Z}_{\ge 0}$ and $a + b + c' = a + b' + c = a' + b + c = K$ with $a \ne a'$. Observe that
$$a - a' = b - b' = c - c' = a + b + c - K =: \delta \ne 0.$$

**Lemma 4 (Necessary Conditions for External Stability in the Triangular Case).** *If $V = \{x, y, z\}$ is externally stable, then $K = 2m$ is even and $V = \{(m, m, 0), (m, 0, m), (0, m, m)\}$.*

*Proof.* We analyze the sign of $\delta = a + b + c - K \ne 0$.

- **Case 4a ($\delta < 0$):** Here $a < a'$, $b < b'$, and $c < c'$.
  - **Subcase 4a(i) ($\delta \le -2$):** Then $c' - c = -\delta \ge 2$, so $c' - 2 \ge c \ge 0$. Consider the allocation
    $$w = (a + 1,\; b + 1,\; c' - 2) \in \Delta_K,$$
    which sums to $(a + 1) + (b + 1) + (c' - 2) = a + b + c' = K$. Every element $u \in V$ has either $u_1 = a$ or $u_2 = b$, whereas $w_1 = a + 1 > a$ and $w_2 = b + 1 > b$; thus $w \notin V$. Furthermore, no element of $V$ dominates $w$:
    - $x = (a, b, c')$ has $x_1 = a < w_1$ and $x_2 = b < w_2$;
    - $y = (a, b', c)$ has $y_1 = a < w_1$ and $y_3 = c \le c' - 2 = w_3$;
    - $z = (a', b, c)$ has $z_2 = b < w_2$ and $z_3 = c \le c' - 2 = w_3$.
    Hence $w$ is undominated by $V$.
  - **Subcase 4a(ii) ($\delta = -1$):** Here $a' = a + 1$, $b' = b + 1$, $c' = c + 1$, and $a + b + c = K - 1 \ge 1$ (since $K \ge 2$). Thus at least one of $a, b, c$ is at least $1$; by symmetry assume $a \ge 1$. Consider the allocation
    $$w = (a - 1,\; b + 1,\; c + 1) \in \Delta_K,$$
    which has $w_1 = a - 1 \ge 0$ and sums to $a + b + c + 1 = K$. Since every $u \in V$ has $u_1 \in \{a, a + 1\}$, we have $w \notin V$. Moreover, every $u \in V$ satisfies $u_2 \le b + 1 = w_2$ and $u_3 \le c + 1 = w_3$, so no $u \in V$ can be strictly greater than $w$ in two coordinates. Thus $w$ is undominated by $V$.

- **Case 4b ($\delta > 0$):** Here $a > a' \ge 0$, $b > b' \ge 0$, and $c > c' \ge 0$. Notice that every $u \in V$ satisfies
  $$u_1 \le a, \qquad u_2 \le b, \qquad u_3 \le c.$$
  - Suppose $a' \ge 1$. Consider the allocation
    $$w = (a' - 1,\; b,\; c + 1) \in \Delta_K,$$
    which has $w_1 = a' - 1 \ge 0$ and sums to $a' + b + c = K$. Because $w_3 = c + 1 > c \ge u_3$ for all $u \in V$, we have $w \notin V$. Moreover, every $u \in V$ has $u_2 \le b = w_2$ and $u_3 \le c < w_3$, so at most one coordinate of $u$ (namely $u_1$) can exceed that of $w$. Thus no element of $V$ dominates $w$.
  - By the exact same reasoning (permuting coordinates), if $b' \ge 1$, then $w = (a + 1, b' - 1, c) \in \Delta_K \setminus V$ is undominated by $V$; and if $c' \ge 1$, then $w = (a, b + 1, c' - 1) \in \Delta_K \setminus V$ is undominated by $V$.

  Therefore, external stability requires
  $$a' = 0, \qquad b' = 0, \qquad c' = 0.$$
  Substituting these into $a + b + c' = a + b' + c = a' + b + c = K$ gives
  $$a + b = K, \qquad a + c = K, \qquad b + c = K.$$
  Adding all three equations yields $2(a + b + c) = 3K$, and subtracting each equation from $a + b + c = \frac{3}{2}K$ yields
  $$a = b = c = \frac{K}{2}.$$
  Since $a, b, c$ must be integers, no solution exists when $K$ is odd. When $K = 2m$ is even, the unique solution is $a = b = c = m$ and $a' = b' = c' = 0$, which gives $V = \{(m, m, 0), (m, 0, m), (0, m, m)\}$. $\blacksquare$

---

### 5. Sufficiency for Even $K = 2m$

**Lemma 5 (Stability of $V_{2m}$).** *For every even integer $K = 2m$ ($m \ge 1$), the set*
$$V_{2m} = \{(m, m, 0),\; (m, 0, m),\; (0, m, m)\}$$
*is a stable set.*

*Proof.*
- **Internal stability:** Any two distinct elements of $V_{2m}$ share a coordinate equal to $m$, so neither dominates the other by Lemma 1.
- **External stability:** Let $w = (w_1, w_2, w_3) \in \Delta_{2m} \setminus V_{2m}$.
  - If at least two coordinates of $w$ are strictly less than $m$, say $w_i < m$ and $w_j < m$ for distinct $i, j \in \{1, 2, 3\}$, then the element $u \in V_{2m}$ having $u_i = u_j = m$ satisfies $u_i > w_i$ and $u_j > w_j$, and therefore dominates $w$.
  - Otherwise, at most one coordinate of $w$ is strictly less than $m$, which means at least two coordinates of $w$ are at least $m$, say $w_i \ge m$ and $w_j \ge m$. Since $w_1, w_2, w_3 \ge 0$ and $w_1 + w_2 + w_3 = 2m$, this forces $w_i = m$, $w_j = m$, and the remaining coordinate to be $0$, so $w \in V_{2m}$, a contradiction.

Combining Lemmas 2, 3, 4, and 5 completes the proof for every $K \ge 2$. $\blacksquare$

---

## Computational Verification

The scripts `/work/explore.py` and `/work/verify_simple.py` exhaustively search for all stable sets for $2 \le K \le 15$, confirming that:
- For odd $K \in \{3, 5, 7, 9, 11, 13, 15\}$, there are $0$ stable sets.
- For even $K = 2m \in \{2, 4, 6, 8, 10, 12, 14\}$, there is $1$ stable set, namely $\{(0, m, m), (m, 0, m), (m, m, 0)\}$.
