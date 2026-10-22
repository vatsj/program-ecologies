# When Does the Vickrey-Nearest Core Point Equal the Centroid of the Minimum-Revenue Face?

## 1. Exact Condition

Assume $v_P > 0$, $v_A, v_B, v_C > 0$, and $v_A + v_B + v_C > v_P$, so that the minimum-revenue face $F$ is a non-degenerate two-dimensional convex polygon in the plane $p_A + p_B + p_C = v_P$. Let
$$E = v_A + v_B + v_C - v_P > 0$$
denote the total social surplus (the excess value of the winners over $P$).

**Theorem.** *The Vickrey-nearest point $p^{\text{VN}}$ equals the area centroid $\operatorname{centroid}(F)$ of the polygon $F$ if and only if at least one of the following three conditions holds:*

1. **No value cap binds on $F$:**
   $$v_A \ge v_P, \quad v_B \ge v_P, \quad \text{and} \quad v_C \ge v_P.$$
   In this case, $F$ is the full simplex (an equilateral triangle) with vertices $(v_P,0,0)$, $(0,v_P,0)$, $(0,0,v_P)$, $p^{\text{VCG}} = (0,0,0)$, and
   $$p^{\text{VN}} = \operatorname{centroid}(F) = \left(\frac{v_P}{3},\, \frac{v_P}{3},\, \frac{v_P}{3}\right).$$

2. **No zero-payment floor binds on $F$ (every pair of winners has combined value at most $v_P$):**
   $$v_A + v_B \le v_P, \quad v_B + v_C \le v_P, \quad \text{and} \quad v_C + v_A \le v_P$$
   *(equivalently, $\min(v_A, v_B, v_C) \ge E$, or $p_i^{\text{VCG}} = v_P - \sum_{j \ne i} v_j \ge 0$ for all $i \in \{A,B,C\}$).*
   In this case, even when $v_A, v_B, v_C$ are all distinct, $F$ is an inverted equilateral triangle with vertices $(v_A - E, v_B, v_C)$, $(v_A, v_B - E, v_C)$, $(v_A, v_B, v_C - E)$, $p^{\text{VCG}} = (v_A - E, v_B - E, v_C - E)$, and
   $$p^{\text{VN}} = \operatorname{centroid}(F) = \left(v_A - \frac{E}{3},\, v_B - \frac{E}{3},\, v_C - \frac{E}{3}\right).$$

3. **Full symmetry among the three winners:**
   $$v_A = v_B = v_C.$$
   In this case, $F$ is a regular hexagon (when $\frac{1}{2}v_P < v_i < v_P$) or an equilateral triangle (when $v_i \ge v_P$ or $v_i \le \frac{1}{2}v_P$), and
   $$p^{\text{VN}} = \operatorname{centroid}(F) = \left(\frac{v_P}{3},\, \frac{v_P}{3},\, \frac{v_P}{3}\right).$$

Equivalently, from a geometric standpoint, $p^{\text{VN}} = \operatorname{centroid}(F)$ for a 2D polygon $F$ **if and only if $F$ has 3-fold rotational symmetry** (i.e., $F$ is either an equilateral triangle or a regular hexagon).

*(Degenerate boundary cases: If $v_P \le 0$, then $R = 0$ and $F = \{(0,0,0)\}$ is a single point, so the two coincide trivially. If $v_P > 0$ and one of the winners has $v_i = 0$, say $v_C = 0$, then $p_C = 0$ across the core and $F$ degenerates to a 1-dimensional line segment; the problem reduces to the 2-winner case for $A$ and $B$, where $p^{\text{VN}}$ always equals the midpoint of $F$.)*

---

## 2. Proof

### Step 1: Simplification of the core and the minimum-revenue face $F$

A vector $p = (p_A, p_B, p_C)$ is in the core if and only if $0 \le p_i \le v_i$ for $i \in \{A,B,C\}$ and
$$\sum_{i \in T} p_i \ge \max\left(0,\, v_P - \sum_{j \notin T} v_j\right) \quad \text{for all } T \subseteq \{A, B, C\}.$$
For $T = \{A, B, C\}$, this requires $p_A + p_B + p_C \ge v_P$ (since $v_P > 0$). Conversely, if $0 \le p_i \le v_i$ for all $i$ and $p_A + p_B + p_C = v_P$, then for EVERY subset $T \subseteq \{A, B, C\}$ we automatically have $\sum_{i \in T} p_i \ge 0$ and
$$\sum_{i \in T} p_i = v_P - \sum_{j \notin T} p_j \ge v_P - \sum_{j \notin T} v_j.$$
Since $v_A + v_B + v_C > v_P > 0$, this set is non-empty. Therefore, the minimum core revenue is $R = v_P$, and the minimum-revenue face is simply
$$F = \left\{ (p_A, p_B, p_C) \in \mathbb{R}^3 : p_A + p_B + p_C = v_P, \;\; 0 \le p_i \le v_i \text{ for } i \in \{A, B, C\} \right\}.$$

Notice that on $F$, the tight lower bound on each coordinate $p_i$ is
$$l_i := \max\left(0,\, v_P - \sum_{j \ne i} v_j\right) = \max(0,\, v_i - E) = p_i^{\text{VCG}}.$$

---

### Step 2: Shifting the origin to $p^{\text{VCG}}$

Introduce the translated coordinates
$$x_i = p_i - l_i = p_i - p_i^{\text{VCG}} \quad (i \in \{A, B, C\}).$$
Because $x = p - p^{\text{VCG}}$ is a translation, both Euclidean projection and the centroid are equivariant under it:
$$p^{\text{VN}} = \operatorname{centroid}(F) \quad \Longleftrightarrow \quad x^{\text{VN}} = \operatorname{centroid}(F_x),$$
where $x^{\text{VN}} = p^{\text{VN}} - p^{\text{VCG}}$ is the point in $F_x = F - p^{\text{VCG}}$ closest to the origin $(0,0,0)$.

Let us express $F_x$ explicitly. Define the VCG revenue shortfall
$$S := v_P - (l_A + l_B + l_C) > 0$$
and the maximum VCG-relative payment of each winner
$$w_i := v_i - l_i = \min(v_i, E) > 0 \quad (i \in \{A, B, C\}).$$
(To see that $S > 0$: if $l_i = 0$ for all $i$, $S = v_P > 0$; if $l_A > 0$ and $l_B = l_C = 0$, $S = v_B + v_C > 0$; if $l_A, l_B > 0$ and $l_C = 0$, $S = E + v_C > 0$; if all $l_i > 0$, $S = 2E > 0$.)

**Lemma 1.** *In the $x$-coordinates, the minimum-revenue face is*
$$F_x = \left\{ (x_A, x_B, x_C) \in \mathbb{R}^3 : x_A + x_B + x_C = S, \;\; 0 \le x_i \le w_i \text{ for } i \in \{A, B, C\} \right\},$$
*and for every pair of distinct indices $j \ne k$, we have*
$$w_j + w_k \ge S.$$

*Proof of Lemma 1.* If $p \in F$, then $\sum_i x_i = v_P - \sum_i l_i = S$, $x_i = p_i - l_i \ge 0$ (since $p_i \ge l_i$ on $F$), and $x_i = p_i - l_i \le v_i - l_i = w_i$. Conversely, if $x \in F_x$, setting $p_i = l_i + x_i$ gives $\sum_i p_i = v_P$ and $0 \le l_i \le p_i \le v_i$, so $p \in F$. Finally, for any permutation $(i, j, k)$ of $(A, B, C)$,
$$(w_j + w_k) - S = (v_j - l_j) + (v_k - l_k) - (v_P - l_i - l_j - l_k) = l_i - (v_P - v_j - v_k) \ge 0$$
because $l_i = \max(0, v_P - v_j - v_k) \ge v_P - v_j - v_k$. $\blacksquare$

---

### Step 3: Exact formulas for $\operatorname{centroid}(F_x)$ and $x^{\text{VN}}$

Consider the full equilateral simplex in $x$-coordinates:
$$\Delta_S = \left\{ (x_A, x_B, x_C) \in \mathbb{R}_{\ge 0}^3 : x_A + x_B + x_C = S \right\}.$$
Each upper bound $x_i \le w_i$ slices off the corner region $T_i = \{ x \in \Delta_S : x_i > w_i \}$, which is a smaller equilateral triangle of coordinate height
$$c_i := \max(0,\, S - w_i) \in [0, S).$$
By Lemma 1, $w_j + w_k \ge S$, which implies
$$c_j + c_k \le S \quad \text{for all } j \ne k.$$
Consequently, if $x \in \Delta_S$ satisfies $x_j > w_j$ and $x_k > w_k$, then $x_j + x_k > w_j + w_k \ge S$, which is impossible on $\Delta_S$. Thus **the three cut-off corner triangles $T_A, T_B, T_C$ have pairwise disjoint interiors**:
$$F_x = \Delta_S \setminus (T_A \cup T_B \cup T_C).$$

#### Formula for $\operatorname{centroid}(F_x)$
- The triangle $\Delta_S$ has area proportional to $S^2$ and centroid $g(\Delta_S) = \left(\frac{S}{3}, \frac{S}{3}, \frac{S}{3}\right)$.
- Each corner triangle $T_i$ (for $c_i > 0$) has vertices $(S, 0, 0)$ (at slot $i$) and $S - c_i$ at slot $i$ with $c_i$ at one of the other two slots. Thus $T_i$ has area proportional to $c_i^2$, and its centroid has $i$-th coordinate $S - \frac{2}{3}c_i$ and other two coordinates $\frac{1}{3}c_i$. Relative to $g(\Delta_S)$, its displacement is
  $$g(T_i)_i - \frac{S}{3} = \frac{2}{3}(S - c_i), \qquad g(T_i)_j - \frac{S}{3} = -\frac{1}{3}(S - c_i) \quad (j \ne i).$$
- By additivity of first moments, with $m_i := c_i^2 (S - c_i)$ and $\bar{m} := \frac{1}{3}(m_A + m_B + m_C)$, the centroid of $F_x$ has coordinates
  $$\operatorname{centroid}(F_x)_i = \frac{S}{3} + \frac{\bar{m} - m_i}{S^2 - c_A^2 - c_B^2 - c_C^2} \quad (i \in \{A, B, C\}). \tag{1}$$

#### Formula for $x^{\text{VN}}$
The point $x^{\text{VN}}$ minimizes $\|x\|_2^2 = x_A^2 + x_B^2 + x_C^2$ over $F_x$. The unconstrained minimizer on the plane $x_A + x_B + x_C = S$ is $\left(\frac{S}{3}, \frac{S}{3}, \frac{S}{3}\right)$. Since $c_j + c_k \le S$ for all $j \ne k$, at most one $c_i$ can exceed $\frac{2}{3}S$ (equivalently, at most one $w_i$ can be less than $\frac{S}{3}$). This yields two cases:

- **Case 1 ($\max(c_A, c_B, c_C) \le \frac{2}{3}S$, i.e., $\min(w_A, w_B, w_C) \ge \frac{S}{3}$):**
  The unconstrained minimizer lies in $F_x$, so
  $$x^{\text{VN}} = \left(\frac{S}{3},\, \frac{S}{3},\, \frac{S}{3}\right). \tag{2a}$$

- **Case 2 ($c_i > \frac{2}{3}S$ for a unique index $i$, i.e., $w_i < \frac{S}{3}$):**
  Here $x^{\text{VN}}$ is constrained by the active cap $x_i \le w_i = S - c_i$, and splits the remaining $c_i$ equally between $j$ and $k$ (which is feasible since $c_j, c_k \le S - c_i < \frac{1}{3}S < \frac{c_i}{2}$):
  $$x^{\text{VN}}_i = w_i = S - c_i, \qquad x^{\text{VN}}_j = x^{\text{VN}}_k = \frac{c_i}{2}. \tag{2b}$$

---

### Step 4: Solving $x^{\text{VN}} = \operatorname{centroid}(F_x)$

First, consider **Case 2** ($w_i < \frac{S}{3}$). Because $F_x$ is a non-degenerate 2D convex polygon ($w_i > 0$), its centroid lies in the strict relative interior of $F_x$, so $\operatorname{centroid}(F_x)_i < w_i$. However, $x^{\text{VN}}_i = w_i$ lies on the boundary edge $x_i = w_i$. Thus $x^{\text{VN}} \ne \operatorname{centroid}(F_x)$ throughout Case 2.

Next, consider **Case 1** ($\max(c_A, c_B, c_C) \le \frac{2}{3}S$). Comparing (1) and (2a), we have
$$x^{\text{VN}} = \operatorname{centroid}(F_x) \quad \Longleftrightarrow \quad m_A = m_B = m_C,$$
where $m_i = f(c_i)$ for the cubic function
$$f(c) = c^2(S - c) \quad \text{on } \left[0,\, \frac{2}{3}S\right].$$
Differentiating with respect to $c$ gives
$$f'(c) = 2Sc - 3c^2 = c(2S - 3c) > 0 \quad \text{for all } c \in \left(0,\, \frac{2}{3}S\right).$$
Therefore, $f$ is **strictly increasing** on $\left[0, \frac{2}{3}S\right]$! Consequently, $m_A = m_B = m_C$ on $\left[0, \frac{2}{3}S\right]$ holds **if and only if**
$$c_A = c_B = c_C.$$
(Notice also that if $c_A = c_B = c_C = c$, then $c_A + c_B \le S \implies c \le \frac{1}{2}S < \frac{2}{3}S$, so Case 1 is automatically satisfied.)

Finally, we translate $c_A = c_B = c_C = c$ back to $(v_P, v_A, v_B, v_C)$:

- **Subcase A ($c = 0$):** Here $S \le w_i$ for all $i$. If any $l_i > 0$, Lemma 1 gives $w_j + w_k = S$, which together with $w_j \ge S$ and $w_k \ge S$ would force $S \ge 2S$, impossible since $S > 0$. Thus $l_A = l_B = l_C = 0$, $S = v_P$, and $w_i = v_i \ge v_P$ for all $i$. This is **Condition 1** ($v_A, v_B, v_C \ge v_P$).

- **Subcase B ($c > 0$):** Since $c_i = \max(0, S - w_i) = c > 0$, we must have $S - w_A = S - w_B = S - w_C = c > 0$, so
  $$w_A = w_B = w_C < S, \quad \text{where } w_i = \min(v_i, E).$$
  - If $v_i \ge E$ for all $i \in \{A, B, C\}$, then $w_A = w_B = w_C = E$ holds automatically! Furthermore, $l_i = v_i - E \ge 0$ for all $i$, so $S = v_P - \sum_i (v_i - E) = 2E > E = w_i$ and $c_A = c_B = c_C = E = \frac{S}{2} > 0$. The inequality $v_i \ge E = v_A + v_B + v_C - v_P$ for all $i$ is equivalent to $v_j + v_k \le v_P$ for all $j \ne k$. This is **Condition 2**.
  - If $v_i < E$ for at least one $i$, then $\min(v_A, E) = \min(v_B, E) = \min(v_C, E)$ forces $v_A = v_B = v_C < E$. Combining this with the symmetric subcases of Conditions 1 and 2 gives **Condition 3** ($v_A = v_B = v_C$).

This completes the proof. $\blacksquare$

---

## 3. Worked Examples

### Example 1: The Two Points Differ — Asymmetric Trapezoid ($v_P = 6, v_A = 3, v_B = 6, v_C = 6$)

Suppose $v_P = 6$ and $(v_A, v_B, v_C) = (3, 6, 6)$. Here $v_A + v_B + v_C = 15 > 6$, so $A, B, C$ win.
None of the three conditions holds: $v_A = 3 < v_P$ (Condition 1 fails), $v_B + v_C = 12 > v_P$ (Condition 2 fails), and $v_A \ne v_B$ (Condition 3 fails).

1. **VCG payments:**
   $$p_A^{\text{VCG}} = \max(0, 6 - 12) = 0, \quad p_B^{\text{VCG}} = \max(0, 6 - 9) = 0, \quad p_C^{\text{VCG}} = \max(0, 6 - 9) = 0.$$
   Thus $p^{\text{VCG}} = (0, 0, 0)$.

2. **Minimum-revenue face $F$:**
   $$F = \{ (p_A, p_B, p_C) \in \mathbb{R}_{\ge 0}^3 : p_A + p_B + p_C = 6, \;\; p_A \le 3 \}.$$
   Geometrically, $F$ is an isosceles trapezoid with the four vertices $(0,6,0)$, $(0,0,6)$, $(3,0,3)$, and $(3,3,0)$, formed by starting from the equilateral triangle $\Delta_6 = \{p_A+p_B+p_C=6,\, p_i \ge 0\}$ and slicing off the top corner triangle $T_A = \{p \in \Delta_6 : p_A > 3\}$ (which has half the side length and $\frac{1}{4}$ the area of $\Delta_6$).

3. **Vickrey-nearest point $p^{\text{VN}}$:**
   The orthogonal projection of $p^{\text{VCG}} = (0,0,0)$ onto the plane $p_A + p_B + p_C = 6$ is $(2, 2, 2)$. Since $p_A = 2 \le 3$, this point already lies inside $F$. Therefore,
   $$p^{\text{VN}} = (2,\, 2,\, 2).$$

4. **Centroid of $F$:**
   The full simplex $\Delta_6$ has centroid $(2, 2, 2)$, while the removed top triangle $T_A$ (with vertices $(6,0,0), (3,3,0), (3,0,3)$) has relative area $\frac{1}{4}$ and centroid $(4, 1, 1)$. By area-weighted subtraction (or Equation (1) with $S = 6, c_A = 3, c_B = c_C = 0$),
   $$\operatorname{centroid}(F) = \frac{1 \cdot (2, 2, 2) - \frac{1}{4} \cdot (4, 1, 1)}{1 - \frac{1}{4}} = \left(\frac{4}{3},\, \frac{7}{3},\, \frac{7}{3}\right) \neq (2, 2, 2).$$
   Cutting off the top corner shifts the centroid of $F$ away from $A$, whereas $p^{\text{VN}}$ does not move at all because the constraint $p_A \le 3$ is slack at $(2,2,2)$.

---

### Example 2: The Two Points Differ — Asymmetric Hexagon ($v_P = 10, v_A = 8, v_B = 7, v_C = 6$)

Suppose $v_P = 10$ and $(v_A, v_B, v_C) = (8, 7, 6)$, so all three value caps bind ($v_i < 10$) while every pair exceeds $v_P$ ($v_j + v_k > 10$).

1. **VCG payments:** $p^{\text{VCG}} = (0, 0, 0)$, so $S = 10$ and $(c_A, c_B, c_C) = (2, 3, 4)$.
2. **Minimum-revenue face $F$:** $F$ is a 6-gon with vertices $(8,2,0), (8,0,2), (4,0,6), (0,4,6), (0,7,3), (3,7,0)$.
3. **Vickrey-nearest point:** Since $\max(c_A, c_B, c_C) = 4 \le \frac{20}{3}$, the unconstrained projection lies in $F$:
   $$p^{\text{VN}} = \left(\frac{10}{3},\, \frac{10}{3},\, \frac{10}{3}\right) \approx (3.3333,\, 3.3333,\, 3.3333).$$
4. **Centroid of $F$:** By Equation (1), $S^2 - c_A^2 - c_B^2 - c_C^2 = 100 - 4 - 9 - 16 = 71$, $m_A = 4(8) = 32$, $m_B = 9(7) = 63$, $m_C = 16(6) = 96$, and $\bar{m} = \frac{191}{3}$, yielding
   $$\operatorname{centroid}(F) = \left(\frac{842}{213},\, \frac{718}{213},\, \frac{570}{213}\right) \approx (3.9531,\, 3.3709,\, 2.6761) \neq p^{\text{VN}}.$$

---

### Example 3: Non-Trivial Equality with Asymmetric Values — Condition 2 ($v_P = 10, v_A = 5, v_B = 4, v_C = 3$)

Suppose $v_P = 10$ and $(v_A, v_B, v_C) = (5, 4, 3)$. Here $v_A + v_B + v_C = 12 > 10$, so $E = 12 - 10 = 2 > 0$.
Even though $v_A, v_B, v_C$ are all distinct, every pairwise sum is at most $v_P$:
$$v_A + v_B = 9 \le 10, \quad v_A + v_C = 8 \le 10, \quad v_B + v_C = 7 \le 10 \quad (\text{Condition 2 holds}).$$

1. **VCG payments:**
   $$p_A^{\text{VCG}} = 10 - (4 + 3) = 3, \quad p_B^{\text{VCG}} = 10 - (5 + 3) = 2, \quad p_C^{\text{VCG}} = 10 - (5 + 4) = 1.$$
   Thus $p^{\text{VCG}} = (3, 2, 1)$.

2. **Minimum-revenue face $F$:**
   Since $p_i \ge p_i^{\text{VCG}} > 0$, the non-negativity constraints $p_i \ge 0$ never bind on $F$. In discount coordinates $d_i = v_i - p_i$, $F$ is simply $\{d_A + d_B + d_C = 2,\, d_i \ge 0\}$, an equilateral triangle with vertices
   $$(3, 4, 3), \quad (5, 2, 3), \quad \text{and} \quad (5, 4, 1).$$

3. **Vickrey-nearest point and Centroid:**
   Projecting $p^{\text{VCG}} = (3, 2, 1)$ onto $p_A + p_B + p_C = 10$ adds $\frac{10 - (3+2+1)}{3} = \frac{4}{3}$ to each coordinate, which equals the average of the three vertices of the triangle $F$:
   $$p^{\text{VN}} = \operatorname{centroid}(F) = \left(3 + \frac{4}{3},\, 2 + \frac{4}{3},\, 1 + \frac{4}{3}\right) = \left(\frac{13}{3},\, \frac{10}{3},\, \frac{7}{3}\right).$$
