# When Does the Vickrey-Nearest Core Point Equal the Centroid of the Minimum-Revenue Face?

## 1. Exact Condition

Assume the standard non-degenerate setting where $v_P > 0$, $v_A, v_B, v_C > 0$, and $v_A + v_B + v_C > v_P$, so that the minimum-revenue face $F$ is a two-dimensional polygon in the plane $p_A + p_B + p_C = v_P$.

**Theorem.** *The Vickrey-nearest core point $p^{\text{VN}}$ equals the centroid (center of mass) $p^{\text{cent}}$ of the polygon $F$ if and only if at least one of the following three conditions holds:*

1. **No value cap binds on $F$:**
   $$v_P \le \min(v_A, v_B, v_C).$$
   *(In this regime, $p^{\text{VCG}} = (0,0,0)$ and $F$ is the full equilateral simplex triangle of side length $\sqrt{2}\,v_P$.)*

2. **Every two-winner coalition falls short of $v_P$ (all pairwise standalone caps bind to the threshold):**
   $$v_P \ge \max(v_A + v_B,\; v_A + v_C,\; v_B + v_C).$$
   *(In this regime, all three VCG payments $p_i^{\text{VCG}} = v_P - \sum_{j \ne i} v_j \ge 0$ are active, and $F$ is an inverted equilateral triangle whose vertices have two winners paying their full standalone values $v_i$.)*

3. **Symmetric single-item valuations:**
   $$v_A = v_B = v_C.$$
   *(In this regime, when $v_A < v_P < 2v_A$, $F$ is a $3$-fold rotationally symmetric hexagon centered at $p^{\text{VN}}$.)*

Equivalently, let $E = v_A + v_B + v_C - v_P > 0$ be the efficiency surplus, $d_i = v_i - p_i^{\text{VCG}} = \min(v_i, E)$ be winner $i$'s maximum payment above VCG, $D = v_P - \sum_{i} p_i^{\text{VCG}} = d_A + d_B + d_C - E$ be the VCG revenue deficit, and $a_i = \max(0, D - d_i)$ be the truncation depth at corner $i$. Then:
$$p^{\text{VN}} = p^{\text{cent}} \iff a_A = a_B = a_C.$$

*(Degenerate boundary cases: If $v_P \le 0$, then $R = 0$ and $F = \{(0,0,0)\}$ is a single point, so $p^{\text{VN}} = p^{\text{cent}} = (0,0,0)$. If $v_P > 0$ and one winner has $v_i = 0$, then $p_i = 0$ and the problem reduces to the two-winner line segment on which $p^{\text{VN}}$ always equals the midpoint of $F$.)*

---

## 2. Proof

### Step 1: Algebraic Characterization of the Core and the Minimum-Revenue Face $F$

Let $W = \{A, B, C\}$. By definition, a payment vector $p = (p_A, p_B, p_C)$ lies in the core if and only if $0 \le p_i \le v_i$ for each $i \in W$ and, for every subset $T \subseteq W$,
$$\sum_{i \in T} p_i \ge \max\!\Big(0,\; v_P - \sum_{j \notin T} v_j\Big).$$

Examine these inequalities by the size of $T$:
- **$T = \emptyset$:** $0 \ge \max(0, v_P - (v_A + v_B + v_C)) = 0$ (since $v_A + v_B + v_C > v_P$), which is trivial.
- **$|T| = 1$ ($T = \{i\}$):** $p_i \ge \max(0, v_P - \sum_{j \ne i} v_j) = p_i^{\text{VCG}}$. Since $p_i^{\text{VCG}} \ge 0$, this subsumes $p_i \ge 0$. Let $L_i = p_i^{\text{VCG}}$.
- **$T = W$:** $p_A + p_B + p_C \ge \max(0, v_P) = v_P$ (for $v_P > 0$).
- **$|T| = 2$ ($T = \{i, j\}$ with $k \notin T$):** $p_i + p_j \ge \max(0, v_P - v_k)$. Note that whenever $p_A + p_B + p_C = v_P$, we have $p_i + p_j = v_P - p_k$; since $p_k \le v_k$ and $p_i, p_j \ge 0$, both $p_i + p_j = v_P - p_k \ge v_P - v_k$ and $p_i + p_j \ge 0$ hold automatically.

Next, we verify that the minimum core revenue is $R = v_P$. Let $E = v_A + v_B + v_C - v_P > 0$. Because $v_P - \sum_{j \ne i} v_j = v_i - E$, we can write
$$L_i = \max(0, v_i - E), \qquad d_i := v_i - L_i = \min(v_i, E) > 0.$$
Summing $L_i + d_i = v_i$ over $i \in W$ gives
$$D := v_P - (L_A + L_B + L_C) = d_A + d_B + d_C - E.$$
Could $D \le 0$ when $v_P > 0$? If $d_i < E$ for all $i$, then $L_i = 0$ for all $i$, so $D = v_P > 0$. If $d_k = E$ for at least one winner $k$, then $D = d_i + d_j > 0$ because $d_i, d_j > 0$. Thus $L_A + L_B + L_C < v_P = \sum_i (L_i + d_i) = v_A + v_B + v_C$, so the hyperplane $p_A + p_B + p_C = v_P$ always intersects the box $[L_A, v_A] \times [L_B, v_B] \times [L_C, v_C]$. Therefore $R = v_P$, and the minimum-revenue face is
$$F = \Big\{\, p \in \mathbb{R}^3 \;:\; p_A + p_B + p_C = v_P,\;\; L_i \le p_i \le v_i \text{ for } i \in \{A, B, C\} \,\Big\}.$$

---

### Step 2: Shifted Coordinates and the Truncated-Simplex Geometry of $F$

Translate the origin to the VCG point by setting $y_i = p_i - L_i$. Both Euclidean distance from $p^{\text{VCG}} = L$ and the centroid are equivariant under translation: $p^{\text{VN}} = L + y^{\text{VN}}$ and $p^{\text{cent}} = L + y^{\text{cent}}$, where
$$F_y = \Big\{\, y \in \mathbb{R}^3 \;:\; y_A + y_B + y_C = D,\;\; 0 \le y_i \le d_i \text{ for } i \in \{A, B, C\} \,\Big\},$$
and $y^{\text{VN}} = \operatorname{argmin}_{y \in F_y} \|y\|_2^2$.

Consider the full equilateral simplex triangle
$$T_0 = \Big\{\, y \in \mathbb{R}^3 \;:\; y_A + y_B + y_C = D,\;\; y_A, y_B, y_C \ge 0 \,\Big\}$$
with vertices $(D,0,0)$, $(0,D,0)$, and $(0,0,D)$. For each $i \in \{A,B,C\}$, the upper cap $y_i \le d_i$ removes from corner $i$ of $T_0$ the smaller homothetic equilateral triangle
$$T_i = \Big\{\, y \in T_0 \;:\; y_i > d_i \,\Big\}$$
of side length proportional to
$$a_i := \max(0, D - d_i).$$
Notice that for any two distinct corners $i \ne j$ (with third index $k$),
$$(D - d_i) + (D - d_j) = D + (D - d_i - d_j) = D + (d_k - E) \le D$$
because $d_k = \min(v_k, E) \le E$. Consequently, $a_i + a_j \le D$, which means $d_i + d_j \ge D$: **the three corner cut-off triangles $T_A, T_B, T_C$ have pairwise disjoint interiors** (touching at a single boundary vertex if and only if $d_k = E$). Furthermore, since $d_i > 0$ and $D - d_i = d_j + d_k - E$, we have $a_i < D$ for each $i$, and $\text{Area}(T_0) > \sum_i \text{Area}(T_i)$, so $F_y = T_0 \setminus (T_A \cup T_B \cup T_C)$ is a non-degenerate polygon.

---

### Step 3: Necessary and Sufficient Condition for $y^{\text{VN}} = y^{\text{cent}}$

We split the analysis according to whether the unconstrained projection $y^* = (D/3, D/3, D/3)$ of the origin onto the plane $y_A + y_B + y_C = D$ lies in $F_y$.

#### Case A: $\min(d_A, d_B, d_C) < D/3$ (so $y^* \notin F_y$)

We show that $y^{\text{VN}} \ne y^{\text{cent}}$ is impossible to avoid here. Let $i \in \operatorname{argmin}_{j} d_j$, so $d_i < D/3$.
1. To find $y^{\text{VN}}$, we minimize $\|y\|_2^2$ over $F_y$. By strict convexity, since the unconstrained minimum $(D/3, D/3, D/3)$ violates $y_i \le d_i$, KKT optimality for orthogonal projection onto a simplex with box bounds sets $y_i^{\text{VN}} = d_i$ (Specifically, $y_j^{\text{VN}} = \min(d_j, \max(0, \lambda))$ where $\sum_j y_j^{\text{VN}} = D$; because $d_i < D/3$ is the smallest upper bound, $\lambda > D/3 > d_i$, forcing $y_i^{\text{VN}} = d_i$).
2. On the other hand, every point $y \in F_y$ satisfies $y_i \le d_i$, and since $F_y$ is a two-dimensional polygon of positive area, the set of points in $F_y$ with $y_i < d_i$ has full measure. Therefore, the centroid of $F_y$ satisfies the strict inequality
   $$y_i^{\text{cent}} = \frac{1}{\text{Area}(F_y)} \int_{F_y} y_i \, dA < d_i = y_i^{\text{VN}}.$$

Hence $y^{\text{VN}} \ne y^{\text{cent}}$ whenever $\min(d_A, d_B, d_C) < D/3$.

#### Case B: $\min(d_A, d_B, d_C) \ge D/3$ (so $y^* \in F_y$)

Here $y^* = (D/3, D/3, D/3) \in F_y$, so the Vickrey-nearest point is simply the unconstrained orthogonal projection:
$$y^{\text{VN}} = \left(\frac{D}{3}, \frac{D}{3}, \frac{D}{3}\right).$$
 Note that $d_i \ge D/3$ is equivalent to $a_i = \max(0, D - d_i) \le \frac{2}{3}D$ for all $i \in \{A, B, C\}$.

Now compute $y^{\text{cent}}$ by decomposing $T_0$ into $F_y$ and the three interior-disjoint corner triangles $T_A, T_B, T_C$:
- In normalized area units (where an equilateral triangle of coordinate span $s$ has area $s^2$), $\text{Area}(T_0) = D^2$ and its centroid is $c_0 = (D/3, D/3, D/3) = y^{\text{VN}}$.
- The corner triangle $T_A$ has vertices $(D, 0, 0)$, $(D - a_A, a_A, 0)$, and $(D - a_A, 0, a_A)$. Its normalized area is $a_A^2$ and its centroid is the average of its three vertices:
  $$c_A = \left(D - \frac{2}{3}a_A,\; \frac{1}{3}a_A,\; \frac{1}{3}a_A\right) = y^{\text{VN}} + \frac{D - a_A}{3}(2, -1, -1).$$
  Similarly, $T_B$ and $T_C$ have normalized areas $a_B^2$ and $a_C^2$ and centroids
  $$c_B = y^{\text{VN}} + \frac{D - a_B}{3}(-1, 2, -1), \qquad c_C = y^{\text{VN}} + \frac{D - a_C}{3}(-1, -1, 2).$$

By additivity of first moments,
$$\text{Area}(F_y)\,(y^{\text{cent}} - y^{\text{VN}}) = D^2(c_0 - y^{\text{VN}}) - \sum_{i \in \{A,B,C\}} a_i^2(c_i - y^{\text{VN}}).$$
Define $f(a) := a^2(D - a)$. Then the above equation becomes
$$3\,\text{Area}(F_y)\,(y^{\text{cent}} - y^{\text{VN}}) = \begin{pmatrix} -2f(a_A) + f(a_B) + f(a_C) \\ f(a_A) - 2f(a_B) + f(a_C) \\ f(a_A) + f(a_B) - 2f(a_C) \end{pmatrix}.$$
Thus $y^{\text{cent}} = y^{\text{VN}}$ if and only if
$$f(a_A) = f(a_B) = f(a_C).$$
On the interval $\big[0, \frac{2}{3}D\big]$, the derivative of $f(a) = Da^2 - a^3$ is
$$f'(a) = a(2D - 3a) > 0 \quad \text{for all } a \in \Big(0, \frac{2}{3}D\Big).$$
Hence $f$ is **strictly increasing** on $\big[0, \frac{2}{3}D\big]$. Since $a_A, a_B, a_C \in \big[0, \frac{2}{3}D\big]$ in Case B, $f(a_A) = f(a_B) = f(a_C)$ holds if and only if
$$a_A = a_B = a_C.$$
Conversely, if $a_A = a_B = a_C = a$, then since $a_i = \max(0, D - d_i) = \max(0, d_j + d_k - E)$ and $D = d_A + d_B + d_C - E$, symmetry implies either $a = 0 \le \frac{2}{3}D$ (when $D \le d_i$) or $d_A = d_B = d_C = d$, in which case $D = 3d - E \le 2d$ so $d \ge D/2 > D/3$ and $a = D - d \le D/2 < \frac{2}{3}D$; thus $\min_i d_i \ge D/3$ is automatically satisfied whenever $a_A = a_B = a_C$.

---

### Step 4: Translating $a_A = a_B = a_C$ into $(v_P, v_A, v_B, v_C)$

Since $a_i = \max(0, D - d_i)$, equality $a_A = a_B = a_C$ occurs in exactly two ways:

1. **$a_A = a_B = a_C = 0$:**
   This holds if and only if $D - d_i \le 0$ for all $i \in \{A, B, C\}$. Using $D = v_P - L_A - L_B - L_C$ and $d_i = v_i - L_i$, we have
   $$D - d_i = v_P - v_i - L_j - L_k.$$
   If $D - d_i \le 0$ for all $i$, could any $L_m > 0$? Suppose $L_A = v_P - v_B - v_C > 0$. Then $v_B + v_C < v_P$, so $L_B = \max(0, v_P - v_A - v_C)$ and $L_C = \max(0, v_P - v_A - v_B)$. In fact, using $D - d_i = d_j + d_k - E \le 0$ for all pairs $\{j,k\}$, since $d_m = \min(v_m, E) > 0$, no $d_m$ can equal $E$ (otherwise $d_m + d_k = E + d_k > E$). Thus $d_m = v_m < E$ for all $m$, so $L_A = L_B = L_C = 0$. Then $D - d_i = v_P - v_i \le 0$ for all $i$, which is precisely **Condition 1**:
   $$v_P \le \min(v_A, v_B, v_C).$$

2. **$a_A = a_B = a_C > 0$:**
   This holds if and only if $D - d_A = D - d_B = D - d_C > 0$, which is equivalent to
   $$d_A = d_B = d_C \quad \text{and} \quad D > d_A.$$
   Since $d_i = \min(v_i, E)$ and $D - d_A = d_B + d_C - E = 2d_A - E$, there are two subcases:
   - **Subcase 2a ($d_A = d_B = d_C = E$):** Then $D - d_i = 2E - E = E > 0$ always holds, and $d_i = \min(v_i, E) = E$ for all $i$ means $v_i \ge E = v_A + v_B + v_C - v_P$ for all $i$, i.e., $v_P \ge v_j + v_k$ for every pair $\{j, k\}$. This is **Condition 2**:
     $$v_P \ge \max(v_A + v_B,\; v_A + v_C,\; v_B + v_C).$$
   - **Subcase 2b ($d_A = d_B = d_C < E$):** Since $d_i = \min(v_i, E) < E$, we must have $d_i = v_i$ for all $i$, which means
     $$v_A = v_B = v_C$$
     (and $D > d_A$ is $2v_A - E = v_P - v_A > 0$, while $v_A < E$ is $v_P < 2v_A$). Combining this with Conditions 1 and 2 covers all $v_P$ whenever $v_A = v_B = v_C$, giving **Condition 3**.

This completes the proof. $\blacksquare$

*(Remark on the vertex average: If "centroid" were instead taken to mean the arithmetic mean of the vertices of $F$, Conditions 1, 2, and 3 still yield equality, and the only additional cases of equality occur when $F$ is a trapezoid or pentagon whose vertex count jump happens to balance—for instance, when a single cap binds with $a_A = D/3$ and $a_B = a_C = 0$, i.e., $v_A = \frac{2}{3}v_P$ and $v_B, v_C \ge v_P$. For the standard geometric centroid of the polygon $F$, no such accidental cancellation occurs because $f(a) = a^2(D-a)$ is strictly monotone on $[0, 2D/3]$.)*

---

## 3. Worked Examples Where $p^{\text{VN}}$ and $p^{\text{cent}}$ Differ

### Example 1: Zero VCG Payments, One Value Cap Binds ($F$ is a Trapezoid)

Let
$$(v_P, v_A, v_B, v_C) = (6, 3, 6, 6).$$
Since $v_A + v_B + v_C = 15 > 6 = v_P$, the efficient winners are $A, B, C$. None of the three conditions holds ($v_P = 6 > \min v_i = 3$, $v_P = 6 < \max(v_i + v_j) = 12$, and $v_A \ne v_B$).

1. **VCG payment vector:**
   $$p_A^{\text{VCG}} = \max(0, 6 - 12) = 0, \quad p_B^{\text{VCG}} = \max(0, 6 - 9) = 0, \quad p_C^{\text{VCG}} = \max(0, 6 - 9) = 0.$$
   Thus $p^{\text{VCG}} = (0, 0, 0)$.

2. **Minimum-revenue face $F$:**
   The minimum core revenue is $R = v_P = 6$, and
   $$F = \big\{\, (p_A, p_B, p_C) \;:\; p_A + p_B + p_C = 6,\;\; 0 \le p_A \le 3,\;\; 0 \le p_B \le 6,\;\; 0 \le p_C \le 6 \,\big\}.$$
   Geometrically, $F$ is the simplex triangle with vertices $(6,0,0), (0,6,0), (0,0,6)$ with the top corner $p_A > 3$ truncated. It is an isosceles trapezoid with **4 vertices**:
   $$V_1 = (3, 3, 0), \quad V_2 = (3, 0, 3), \quad V_3 = (0, 6, 0), \quad V_4 = (0, 0, 6).$$

3. **Vickrey-nearest point $p^{\text{VN}}$:**
   The unconstrained closest point to $p^{\text{VCG}} = (0,0,0)$ on the plane $p_A + p_B + p_C = 6$ is $(2, 2, 2)$. Since $0 \le 2 \le 3$, this point lies in $F$. Therefore:
   $$p^{\text{VN}} = (2, 2, 2).$$

4. **Centroid $p^{\text{cent}}$ of $F$:**
   The full triangle $T_0$ has normalized area $6^2 = 36$ and centroid $(2, 2, 2)$. The truncated corner triangle $T_A = \{p \in T_0 : p_A \ge 3\}$ has vertices $(6,0,0), (3,3,0), (3,0,3)$, normalized area $3^2 = 9$, and centroid $(4, 1, 1)$. By area-weighted subtraction:
   $$p^{\text{cent}} = \frac{36\,(2, 2, 2) - 9\,(4, 1, 1)}{36 - 9} = \frac{(36, 63, 63)}{27} = \left(\frac{4}{3},\; \frac{7}{3},\; \frac{7}{3}\right) \approx (1.333, 2.333, 2.333).$$
   *(Even if one took the average of the 4 vertices, one would get $\frac{1}{4}(V_1 + V_2 + V_3 + V_4) = (\frac{3}{2}, \frac{9}{4}, \frac{9}{4}) = (1.5, 2.25, 2.25) \ne (2, 2, 2)$.)*

Thus $p^{\text{VN}} = (2, 2, 2) \ne \left(\frac{4}{3}, \frac{7}{3}, \frac{7}{3}\right) = p^{\text{cent}}$. Because $A$'s value cap truncates the $A$-corner of $F$, the center of mass of $F$ shifts toward $B$ and $C$, whereas the orthogonal projection of $p^{\text{VCG}}$ onto $F$ remains unaffected until the cap reaches $p_A = 2$.

---

### Example 2: Positive VCG Payments, Value Cap Binds on $p^{\text{VN}}$ Itself

Let
$$(v_P, v_A, v_B, v_C) = (6, 1, 4, 4).$$
Here $v_A + v_B + v_C = 9 > 6 = v_P$ and $E = 9 - 6 = 3$.

1. **VCG payment vector:**
   $$p_A^{\text{VCG}} = \max(0, 6 - 8) = 0, \quad p_B^{\text{VCG}} = \max(0, 6 - 5) = 1, \quad p_C^{\text{VCG}} = \max(0, 6 - 5) = 1.$$
   Thus $p^{\text{VCG}} = (0, 1, 1)$, and the VCG deficit is $D = 6 - (0 + 1 + 1) = 4$.

2. **Minimum-revenue face $F$:**
   $$F = \big\{\, (p_A, p_B, p_C) \;:\; p_A + p_B + p_C = 6,\;\; 0 \le p_A \le 1,\;\; 1 \le p_B \le 4,\;\; 1 \le p_C \le 4 \,\big\}.$$
   In shifted coordinates $y = p - (0,1,1)$, we have $y_A + y_B + y_C = 4$ with $0 \le y_A \le 1$, $0 \le y_B \le 3$, $0 \le y_C \le 3$, and truncation depths $a_A = 4 - 1 = 3$, $a_B = 4 - 3 = 1$, $a_C = 4 - 3 = 1$. The polygon $F$ is a trapezoid with **4 vertices**:
   $$(1, 4, 1), \quad (1, 1, 4), \quad (0, 4, 2), \quad (0, 2, 4).$$

3. **Vickrey-nearest point $p^{\text{VN}}$:**
   The unconstrained projection of $p^{\text{VCG}} = (0,1,1)$ onto $p_A + p_B + p_C = 6$ is $(0,1,1) + (\frac{4}{3}, \frac{4}{3}, \frac{4}{3}) = (\frac{4}{3}, \frac{7}{3}, \frac{7}{3})$, which violates $p_A \le 1$. Clamping $p_A = 1$ and splitting the remaining deficit $6 - 1 - 2 = 3$ equally between $B$ and $C$ gives:
   $$p^{\text{VN}} = \left(1,\; \frac{5}{2},\; \frac{5}{2}\right) = (1, 2.5, 2.5).$$

4. **Centroid $p^{\text{cent}}$ of $F$:**
   Using the moment formula with $D = 4$ and $(a_A, a_B, a_C) = (3, 1, 1)$, the normalized area is $D^2 - a_A^2 - a_B^2 - a_C^2 = 16 - 9 - 1 - 1 = 5$, and $f(a_A) = 3^2(4 - 3) = 9$, $f(a_B) = f(a_C) = 1^2(4 - 1) = 3$. Hence
   $$y^{\text{cent}} = \left(\frac{4}{3}, \frac{4}{3}, \frac{4}{3}\right) + \frac{1}{3 \times 5}\begin{pmatrix} -18 + 3 + 3 \\ 9 - 6 + 3 \\ 9 + 3 - 6 \end{pmatrix} = \left(\frac{8}{15},\; \frac{26}{15},\; \frac{26}{15}\right),$$
   so in payment coordinates:
   $$p^{\text{cent}} = (0, 1, 1) + \left(\frac{8}{15},\; \frac{26}{15},\; \frac{26}{15}\right) = \left(\frac{8}{15},\; \frac{41}{15},\; \frac{41}{15}\right) \approx (0.533, 2.733, 2.733).$$

Here $p^{\text{VN}}$ pins $A$ at its maximum value $p_A^{\text{VN}} = v_A = 1$ (leaving $A$ zero utility), whereas the centroid of $F$ gives $A$ a strictly lower payment $p_A^{\text{cent}} = \frac{8}{15} < 1$.
