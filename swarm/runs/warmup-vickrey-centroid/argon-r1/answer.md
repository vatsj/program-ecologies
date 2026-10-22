# When Does the Vickrey-Nearest Core Point Equal the Centroid of the Minimum-Revenue Face?

## 1. Main Result (Exact Condition)

Assume $v_P \ge 0$, $v_A, v_B, v_C \ge 0$, and $v_A + v_B + v_C > v_P$. The Vickrey-nearest core point $p^{\text{VN}}$ equals the centroid $p^{\text{cent}}$ of the minimum-revenue face $F$ **if and only if** $(v_P, v_A, v_B, v_C)$ satisfies at least one of the following four conditions:

1. **No value cap binds on $F$:**
   $$v_A + v_B \le v_P, \quad v_A + v_C \le v_P, \quad \text{and} \quad v_B + v_C \le v_P$$
   *(Equivalently, all three VCG payments are non-negative without truncation: $p_i^{\text{VCG}} = v_P - \sum_{j \ne i} v_j \ge 0$ for all $i \in \{A, B, C\}$.)*

2. **No stand-alone value cap binds at $v_P$:**
   $$v_A \ge v_P, \quad v_B \ge v_P, \quad \text{and} \quad v_C \ge v_P$$
   *(Every winner can single-handedly afford the entire threshold $v_P$, so $F$ is the full simplex $\{p \ge 0 : p_A + p_B + p_C = v_P\}$.)*

3. **Equal valuations:**
   $$v_A = v_B = v_C$$
   *(By three-fold permutation symmetry, both $p^{\text{VN}}$ and $p^{\text{cent}}$ equal $(v_P/3, v_P/3, v_P/3)$.)*

4. **One winner has zero valuation (degenerate two-winner reduction):**
   $$\min(v_A, v_B, v_C) = 0$$
   *(The bidder with $v_i = 0$ must pay $p_i = 0$, reducing $F$ to a line segment in the remaining two coordinates where the two-winner midpoint property holds.)*

---

## 2. Proof

### Step 1: Reduction of the Core and the Minimum-Revenue Face $F$

By definition, a payment vector $p = (p_A, p_B, p_C)$ lies in the core if and only if
$$0 \le p_i \le v_i \quad \forall i \in \{A,B,C\}$$
and for every subset $T \subseteq \{A, B, C\}$,
$$\sum_{i \in T} p_i \ge \max\left(0, \, v_P - \sum_{j \notin T} v_j\right).$$

Let $\ell_i = p_i^{\text{VCG}} = \max(0, v_P - \sum_{j \ne i} v_j)$ for each $i \in \{A,B,C\}$.
- For $|T| = 0$ ($T = \emptyset$), the constraint is $0 \ge \max(0, v_P - (v_A + v_B + v_C)) = 0$, which is trivial since $v_A + v_B + v_C > v_P$.
- For $|T| = 1$ ($T = \{i\}$), the constraint is $p_i \ge \ell_i$.
- For $|T| = 3$ ($T = \{A,B,C\}$), the constraint is $p_A + p_B + p_C \ge \max(0, v_P) = v_P$.
- For $|T| = 2$ ($T = \{i, j\}$ with $k \notin T$), the constraint is $p_i + p_j \ge \max(0, v_P - v_k)$. Note that $p_i + p_j \ge 0$ follows from $p_i \ge \ell_i \ge 0$, and $p_i + p_j \ge v_P - v_k$ is **redundant** once $p_A + p_B + p_C \ge v_P$ and $p_k \le v_k$ hold, because
  $$p_i + p_j = (p_A + p_B + p_C) - p_k \ge v_P - v_k.$$

Next, we verify that the minimum total core revenue is $R = v_P$, and specifically that $\ell_A + \ell_B + \ell_C \le v_P$:
- If all three $\ell_i > 0$, then $\ell_A + \ell_B + \ell_C = 3v_P - 2(v_A + v_B + v_C) < v_P$ because $v_A + v_B + v_C > v_P$.
- If two $\ell_i > 0$, say $\ell_A, \ell_B > 0$ and $\ell_C = 0$, then $v_A + v_B \ge v_P$, so $\ell_A + \ell_B + \ell_C = 2v_P - (v_A + v_B) - 2v_C \le v_P - 2v_C \le v_P$.
- If one $\ell_i > 0$, say $\ell_A = v_P - v_B - v_C > 0$ and $\ell_B = \ell_C = 0$, then $\ell_A + \ell_B + \ell_C = v_P - v_B - v_C \le v_P$.
- If $\ell_A = \ell_B = \ell_C = 0$, then $\ell_A + \ell_B + \ell_C = 0 \le v_P$.

Furthermore, setting $p_i = v_i$ gives $\sum p_i = v_A + v_B + v_C > v_P$ with $p_i = v_i \ge \ell_i$ (as $v_A + v_B + v_C > v_P$). Thus the core is non-empty, the minimum core revenue is $R = v_P$, and the minimum-revenue face is
$$F = \left\{ p \in \mathbb{R}^3 : \ell_i \le p_i \le v_i \text{ for } i \in \{A,B,C\}, \; p_A + p_B + p_C = v_P \right\}.$$

---

### Step 2: Shift to Excess Payments above VCG

Translate coordinates by $p^{\text{VCG}} = (\ell_A, \ell_B, \ell_C)$: let
$$x_i = p_i - \ell_i, \qquad u_i = v_i - \ell_i, \qquad D = v_P - (\ell_A + \ell_B + \ell_C) \ge 0.$$
Both the Euclidean projection onto $F$ and the centroid of $F$ are equivariant under translations. In $x$-coordinates, $p^{\text{VCG}}$ becomes the origin $0$, and $F$ becomes
$$F_x = \left\{ x \in \mathbb{R}^3 : 0 \le x_i \le u_i \text{ for } i \in \{1,2,3\}, \; x_1 + x_2 + x_3 = D \right\}.$$
Without loss of generality, label the bidders so that $v_1 \ge v_2 \ge v_3 \ge 0$. Since $v_i \mapsto \ell_i = \max(0, v_P - \sum_{j \ne i} v_j)$ is non-decreasing in $v_i$ and $v_i \mapsto u_i = v_i - \ell_i = \min(v_i, v_A + v_B + v_C - v_P)$ is also non-decreasing in $v_i$, we have:
$$\ell_1 \ge \ell_2 \ge \ell_3 \ge 0 \qquad \text{and} \qquad u_1 \ge u_2 \ge u_3 \ge 0.$$

Let us check a crucial structural property of $(u_1, u_2, u_3)$ and $D$: **for every pair $i \ne j$, $u_i + u_j \ge D$.**
Indeed, for $\{i,j,k\} = \{1,2,3\}$,
$$D - (u_i + u_j) = v_P - \ell_i - \ell_j - \ell_k - (v_i - \ell_i) - (v_j - \ell_j) = (v_P - v_i - v_j) - \ell_k \le 0$$
because $\ell_k = \max(0, v_P - v_i - v_j) \ge v_P - v_i - v_j$.

In particular, since $u_1 \ge u_2 \ge u_3$ and $u_2 + u_3 \ge D$, we always have
$$2 u_2 \ge u_2 + u_3 \ge D \implies u_1 \ge u_2 \ge \frac{D}{2}.$$

---

### Step 3: Degenerate Cases ($D = 0$ or $u_3 = 0$)

- **If $D = 0$:** Then $F_x = \{(0,0,0)\}$ is a single point, so $x^{\text{VN}} = x^{\text{cent}} = (0,0,0)$ trivially. Notice $D = 0$ occurs either when $v_P = 0$ (which satisfies Condition 1 and Condition 2) or when one $\ell_i = v_P$ and the other two are $0$, i.e., $v_2 = v_3 = 0$ (which satisfies Condition 4, and also Condition 1).
- **If $u_3 = 0$ and $D > 0$:** Since $u_3 = \min(v_3, v_1 + v_2 + v_3 - v_P)$ and $v_1 + v_2 + v_3 > v_P$, $u_3 = 0$ occurs if and only if $v_3 = 0$ (**Condition 4**). In this case, $x_3 = 0$ on $F_x$, so $F_x = \{(x_1, D - x_1, 0) : D - u_2 \le x_1 \le u_1\}$ is a 1D line segment. Specifically, when $v_3 = 0$, we have $\ell_1 = \max(0, v_P - v_2)$, $\ell_2 = \max(0, v_P - v_1)$, and $\ell_3 = 0$ (since $v_1 + v_2 = v_1 + v_2 + v_3 > v_P$).
  Thus $D - u_2 = (v_P - v_2 - v_3) - \ell_1 = (v_P - v_2) - \max(0, v_P - v_2) \le 0$, and similarly $D - u_1 = (v_P - v_1) - \max(0, v_P - v_1) \le 0$.
  Hence $u_1 \ge D$ and $u_2 \ge D$, so neither upper bound $x_1 \le u_1$ nor $x_2 \le u_2$ binds! Therefore $F_x$ is the full segment $\{(x_1, D - x_1, 0) : 0 \le x_1 \le D\}$, whose midpoint (centroid) and closest point to $0$ are both $(D/2, D/2, 0)$. Thus $p^{\text{VN}} = p^{\text{cent}}$ whenever $\min(v_A, v_B, v_C) = 0$.

From now on, assume **$D > 0$ and $u_3 > 0$**. Then $F_x$ is a non-degenerate 2D polygon in the plane $x_1 + x_2 + x_3 = D$.

---

### Step 4: Exact Formulas for $x^{\text{VN}}$ and $x^{\text{cent}}$

#### A. The Vickrey-Nearest Point $x^{\text{VN}}$
The point $x^{\text{VN}}$ minimizes $\|x\|_2^2 = x_1^2 + x_2^2 + x_3^2$ subject to $0 \le x_i \le u_i$ and $x_1 + x_2 + x_3 = D$. Since $u_1 \ge u_2 \ge D/2 > D/3$, the upper bounds $x_1 \le u_1$ and $x_2 \le u_2$ never bind at $x^{\text{VN}}$. Only $x_3 \le u_3$ can bind:
$$x^{\text{VN}} = \begin{cases}
\left(\dfrac{D}{3}, \, \dfrac{D}{3}, \, \dfrac{D}{3}\right) & \text{if } u_3 \ge \dfrac{D}{3}, \\[1em]
\left(\dfrac{D - u_3}{2}, \, \dfrac{D - u_3}{2}, \, u_3\right) & \text{if } u_3 < \dfrac{D}{3}.
\end{cases}$$

#### B. The Centroid $x^{\text{cent}}$ of $F_x$
Let $\Delta = \{x \in \mathbb{R}_{\ge 0}^3 : x_1 + x_2 + x_3 = D\}$ be the equilateral triangle of side length $\sqrt{2}D$. The polygon $F_x$ is obtained from $\Delta$ by intersecting with the half-spaces $x_i \le u_i$ for $i = 1, 2, 3$.
Each constraint $x_i \le u_i$ chops off a smaller equilateral corner triangle
$$\Delta_i = \{x \in \Delta : x_i > u_i\}$$
of side length $\sqrt{2} a_i$, where
$$a_i = \max(0, \, D - u_i) \in [0, D).$$
Crucially, **any two corner triangles $\Delta_i$ and $\Delta_j$ ($i \ne j$) have disjoint interiors**, because if $x \in \Delta_i \cap \Delta_j$ then $x_i + x_j > u_i + u_j \ge D$, contradicting $x_1 + x_2 + x_3 = D$ with $x_k \ge 0$.

Therefore, $F_x = \Delta \setminus (\Delta_1 \cup \Delta_2 \cup \Delta_3)$ is a decomposition with disjoint interiors:
- The area of $\Delta$ is proportional to $D^2$, and its centroid is $c(\Delta) = (D/3, D/3, D/3)$.
- For each $i$ with $a_i > 0$, $\Delta_i = u_i e_i + \{y \in \mathbb{R}_{\ge 0}^3 : y_1 + y_2 + y_3 = a_i\}$, whose area is proportional to $a_i^2$ and whose centroid is
  $$c(\Delta_i) = u_i e_i + \frac{a_i}{3}(1,1,1) = (D - a_i)e_i + \frac{a_i}{3}(1,1,1).$$
  Subtracting $c(\Delta) = \frac{D}{3}(1,1,1)$ gives the centroid displacement of $\Delta_i$:
  $$c(\Delta_i) - c(\Delta) = \frac{D - a_i}{3}(3 e_i - (1,1,1)).$$

By the additivity of first moments over disjoint regions, the area of $F_x$ is proportional to $D^2 - a_1^2 - a_2^2 - a_3^2 > 0$, and the centroid $x^{\text{cent}}$ of $F_x$ satisfies:
$$x^{\text{cent}} - \left(\frac{D}{3}, \frac{D}{3}, \frac{D}{3}\right) = \frac{-w_1 (2, -1, -1) - w_2 (-1, 2, -1) - w_3 (-1, -1, 2)}{3(D^2 - a_1^2 - a_2^2 - a_3^2)},$$
where
$$w_i = a_i^2 (D - a_i) \quad \text{for } i \in \{1, 2, 3\}.$$

---

### Step 5: Comparing $x^{\text{VN}}$ and $x^{\text{cent}}$

Since $u_1 \ge u_2 \ge u_3 > 0$ and $u_1 \ge u_2 \ge D/2$, we have
$$0 \le a_1 \le a_2 \le \frac{D}{2} \qquad \text{and} \qquad a_2 \le a_3 < D.$$
We consider the two cases for $x^{\text{VN}}$:

#### Case A: $u_3 \ge D/3$ (equivalently, $a_3 \le 2D/3$)
Here $x^{\text{VN}} = (D/3, D/3, D/3) = c(\Delta)$. From the centroid formula above,
$$x^{\text{cent}} = x^{\text{VN}} \iff w_1(2,-1,-1) + w_2(-1,2,-1) + w_3(-1,-1,2) = (0,0,0) \iff w_1 = w_2 = w_3.$$
Consider the cubic function $f(a) = a^2(D - a)$ on the interval $[0, 2D/3]$. Its derivative is
$$f'(a) = a(2D - 3a) > 0 \quad \text{for all } a \in (0, 2D/3).$$
Thus $f$ is **strictly increasing** on $[0, 2D/3]$. Since $a_1, a_2, a_3 \in [0, 2D/3]$, we obtain:
$$w_1 = w_2 = w_3 \iff a_1 = a_2 = a_3.$$

#### Case B: $u_3 < D/3$ (equivalently, $2D/3 < a_3 < D$)
We show that **$x^{\text{cent}} = x^{\text{VN}}$ never occurs** when $0 < u_3 < D/3$.
Here $x^{\text{VN}} = ((D - u_3)/2, (D - u_3)/2, u_3)$, so its first two coordinates are equal ($x_1^{\text{VN}} = x_2^{\text{VN}}$).
For $x_1^{\text{cent}} = x_2^{\text{cent}}$ to hold, we must have $w_1 = w_2$. Since $0 \le a_1 \le a_2 = D - u_2 \le u_3 < D/3 < 2D/3$ and $f(a)$ is strictly increasing on $[0, 2D/3]$, $w_1 = w_2$ forces $a_1 = a_2 =: a$, with $0 \le a \le u_3$ (as $a + a_3 = a_2 + a_3 \le D$).

Setting $a_1 = a_2 = a$ and $a_3 = D - u_3$, the third coordinate of $x^{\text{cent}}$ minus $x_3^{\text{VN}} = u_3$ simplifies algebraically to:
$$x_3^{\text{cent}} - x_3^{\text{VN}} = \left(\frac{D}{3} - \frac{2(w_3 - w_1)}{3(D^2 - 2a^2 - a_3^2)}\right) - u_3 = \frac{(3D - u_3)u_3^2 - 2a^2(3u_3 - a)}{3(D^2 - 2a^2 - a_3^2)}.$$
Since $0 \le a \le u_3 < D/3$, we have $2a^2(3u_3 - a) \le 2u_3^2(2u_3) = 4u_3^3$, whereas $(3D - u_3)u_3^2 > (9u_3 - u_3)u_3^2 = 8u_3^3$. Thus the numerator is strictly positive ($> 4u_3^3 > 0$), so $x_3^{\text{cent}} > x_3^{\text{VN}}$, and the two points cannot coincide.

---

### Step 6: Translating $a_1 = a_2 = a_3$ Back to $(v_P, v_A, v_B, v_C)$

For $D > 0$ and $u_3 > 0$, we have established that $p^{\text{VN}} = p^{\text{cent}}$ if and only if
$$a_1 = a_2 = a_3, \quad \text{where } a_i = \max(0, \, D - u_i).$$
Recall that for $\{i,j,k\} = \{1,2,3\}$,
$$D - u_i = (v_P - v_j - v_k) - \ell_i + (v_j - \ell_j) + (v_k - \ell_k) \implies D - u_i = v_P - v_i - \ell_j - \ell_k.$$
Let us examine the four possible regimes for the number of positive VCG payments among $\ell_1 \ge \ell_2 \ge \ell_3 \ge 0$:

1. **All three $\ell_1, \ell_2, \ell_3 \ge 0$ without truncation binding ($v_1 + v_2 \le v_P$):**
   Here $\ell_i = v_P - v_j - v_k \ge 0$ for all $i$. Then for every $i \in \{1,2,3\}$,
   $$u_i = v_1 + v_2 + v_3 - v_P, \qquad D = 2(v_1 + v_2 + v_3 - v_P) = 2u_i,$$
   so $a_1 = a_2 = a_3 = v_1 + v_2 + v_3 - v_P = D/2 \le 2D/3$. Thus $a_1 = a_2 = a_3$ **always holds** in this regime. This gives **Condition 1** ($v_A + v_B \le v_P$, $v_A + v_C \le v_P$, $v_B + v_C \le v_P$). Geometrically, $F$ is an inverted equilateral triangle where no value cap $p_i \le v_i$ is redundant.

2. **Exactly two VCG bounds are strictly positive ($\ell_1, \ell_2 > 0$ and $\ell_3 = 0$, so $v_1 + v_3 < v_P$ and $v_1 + v_2 \ge v_P$):**
   Substituting $\ell_1 = v_P - v_2 - v_3$, $\ell_2 = v_P - v_1 - v_3$, $\ell_3 = 0$ yields:
   $$D - u_1 = v_3, \qquad D - u_2 = v_3, \qquad D - u_3 = v_1 + v_2 + v_3 - v_P.$$
   Since $v_3 > 0$ and $v_1 + v_2 + v_3 - v_P > 0$, all three $D - u_i$ are positive, so $a_1 = a_2 = a_3$ holds if and only if
   $$v_3 = v_1 + v_2 + v_3 - v_P \iff v_1 + v_2 = v_P,$$
   which is the boundary already included in **Condition 1**.

3. **Exactly one VCG bound is strictly positive ($\ell_1 > 0$ and $\ell_2 = \ell_3 = 0$, so $v_2 + v_3 < v_P$ and $v_1 + v_3 \ge v_P$):**
   Substituting $\ell_1 = v_P - v_2 - v_3$ and $\ell_2 = \ell_3 = 0$ yields:
   $$D - u_1 = v_P - v_1, \qquad D - u_2 = v_3, \qquad D - u_3 = v_2.$$
   Since $v_2 \ge v_3 > 0$, we have $a_2 = v_3 > 0$ and $a_3 = v_2 > 0$. For $a_1 = a_2 = a_3$ to hold, we must have $v_P - v_1 = v_3 = v_2$, i.e., $v_1 + v_3 = v_P$ and $v_2 = v_3$, which implies $v_1 + v_2 = v_P$—again on the boundary of **Condition 1**.

4. **All three VCG bounds are zero ($\ell_1 = \ell_2 = \ell_3 = 0$, so $v_2 + v_3 \ge v_P$):**
   Here $D = v_P$ and $u_i = v_i$, so
   $$a_i = \max(0, \, v_P - v_i) \quad \text{for } i = 1, 2, 3.$$
   Note that $a_3 = \max(0, v_P - v_3) \le v_P - v_P/2 = D/2 \le 2D/3$ only if $v_3 \ge v_P/2$, or even if $v_3 < v_P/2$, we already know $a_1 = a_2 = a_3 \le 2D/3$ is required. Since $v_1 \ge v_2 \ge v_3$, the equality $\max(0, v_P - v_1) = \max(0, v_P - v_2) = \max(0, v_P - v_3)$ holds in exactly two ways:
   - Either $\max(0, v_P - v_i) = 0$ for all $i$, which means $v_1 \ge v_2 \ge v_3 \ge v_P$ (**Condition 2**);
   - Or $v_P - v_1 = v_P - v_2 = v_P - v_3 > 0$, which means $v_1 = v_2 = v_3$ (**Condition 3**).
   *(Note that if $v_1 = v_2 = v_3 = v$, then $v_2 + v_3 = 2v \ge v_P \implies u_3 = v \ge v_P/2 = D/2 > D/3$, so $a_3 \le D/2 < 2D/3$ is automatically satisfied.)*

Combining Steps 3, 5, and 6 completes the proof that $p^{\text{VN}} = p^{\text{cent}}$ if and only if at least one of Conditions 1–4 holds. $\blacksquare$

---

## 3. Worked Examples Where $p^{\text{VN}} \ne p^{\text{cent}}$

### Example 1: Zero VCG Payments, Asymmetric Value Caps (Trapezoidal Face $F$)

Take
$$v_P = 6, \qquad v_A = 6, \qquad v_B = 4, \qquad v_C = 2.$$
Here $v_A + v_B + v_C = 12 > 6 = v_P$, so $A, B, C$ are the efficient winners. None of Conditions 1–4 hold: $v_A + v_B = 10 > 6$, $v_C = 2 < 6$, the valuations $(6,4,2)$ are distinct, and $\min(v_A, v_B, v_C) = 2 > 0$.

1. **VCG payments:**
   $$\begin{aligned}
   p_A^{\text{VCG}} &= \max(0, \, 6 - (4 + 2)) = 0, \\
   p_B^{\text{VCG}} &= \max(0, \, 6 - (6 + 2)) = 0, \\
   p_C^{\text{VCG}} &= \max(0, \, 6 - (6 + 4)) = 0.
   \end{aligned}$$
   Thus $p^{\text{VCG}} = (0, 0, 0)$.

2. **Minimum-revenue face $F$:**
   The minimum revenue is $R = 6$, and
   $$F = \left\{ (p_A, p_B, p_C) \in \mathbb{R}^3 : 0 \le p_A \le 6, \; 0 \le p_B \le 4, \; 0 \le p_C \le 2, \; p_A + p_B + p_C = 6 \right\}.$$
   This polygon is a trapezoid with $4$ vertices:
   $$V_1 = (6, 0, 0), \quad V_2 = (2, 4, 0), \quad V_3 = (0, 4, 2), \quad V_4 = (4, 0, 2).$$

3. **Vickrey-nearest point $p^{\text{VN}}$:**
   The unconstrained projection of $p^{\text{VCG}} = (0,0,0)$ onto the plane $p_A + p_B + p_C = 6$ is
   $$p^{\text{VN}} = (2, 2, 2).$$
   Since $0 \le 2 \le 6$, $0 \le 2 \le 4$, and $0 \le 2 \le 2$, the point $(2, 2, 2)$ lies inside $F$ (specifically, at the midpoint of the top edge connecting $V_4 = (4,0,2)$ and $V_3 = (0,4,2)$). Therefore,
   $$p^{\text{VN}} = (2, 2, 2).$$

4. **Centroid $p^{\text{cent}}$ of $F$:**
   Parameterizing $F$ by $(p_B, p_C) \in [0, 4] \times [0, 2]$ (note that $p_A = 6 - p_B - p_C \in [0, 6]$ holds automatically over the entire rectangle $[0, 4] \times [0, 2]$!), $F$ is the affine image of the rectangle $[0, 4] \times [0, 2]$ under the linear map $(p_B, p_C) \mapsto (6 - p_B - p_C, p_B, p_C)$.
   Since the centroid of a rectangle is its center $(p_B, p_C) = (2, 1)$ and affine maps preserve centroids, the centroid of $F$ is immediately:
   $$p^{\text{cent}} = (6 - 2 - 1, \, 2, \, 1) = (3, 2, 1).$$
   *(Using our general formula with $D = 6$ and $a = (0, 2, 4)$ gives $w = (0, 16, 32)$ and $3(D^2 - a_A^2 - a_B^2 - a_C^2) = 3(36 - 0 - 4 - 16) = 48$, yielding $p^{\text{cent}} = (2,2,2) + \frac{1}{48}(48, 0, -48) = (3, 2, 1)$.)*

Thus,
$$p^{\text{VN}} = (2, 2, 2) \ne (3, 2, 1) = p^{\text{cent}}.$$
Intuitively, bidder $C$'s tight cap $p_C \le 2$ truncates the top of the simplex $p_A + p_B + p_C = 6$ at $p_C = 2$, shifting the area centroid of $F$ downward in $p_C$ and upward in $p_A$, while $p^{\text{VN}} = (2,2,2)$ remains unshifted because the cap $p_C \le 2$ is just barely satisfied at $(2,2,2)$.

---

### Example 2: Positive VCG Payment

To illustrate a case with a strictly positive VCG payment, take
$$v_P = 7, \qquad v_A = 7, \qquad v_B = 4, \qquad v_C = 2.$$
Here:
- $p^{\text{VCG}} = (\max(0, 7 - 6), \max(0, 7 - 9), \max(0, 7 - 11)) = (1, 0, 0)$.
- $R = 7$, $D = 7 - 1 = 6$, and $u = v - p^{\text{VCG}} = (6, 4, 2)$, so $F = p^{\text{VCG}} + F_x$ where $F_x$ is the exact same trapezoid as in Example 1.
- Therefore:
  $$p^{\text{VN}} = (1, 0, 0) + (2, 2, 2) = (3, 2, 2),$$
  $$p^{\text{cent}} = (1, 0, 0) + (3, 2, 1) = (4, 2, 1).$$
Again, $p^{\text{VN}} = (3, 2, 2) \ne (4, 2, 1) = p^{\text{cent}}$.
