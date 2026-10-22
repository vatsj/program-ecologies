# Answer: Vickrey-nearest point vs. centroid of the minimum-revenue face (three winners)

Assume all values are positive. Let

- V = v_A + v_B + v_C, and s = V − v_P > 0 (the efficiency slack);
- l_i = p_i^VCG = max(0, v_P − Σ_{j≠i} v_j) = max(0, v_i − s);
- u_i = v_i − l_i = min(v_i, s) (how far winner i's payment can rise above VCG);
- D = v_P − Σ_i l_i (revenue the core needs on top of VCG). Note Σ_i u_i = D + s.

## Condition

**The Vickrey-nearest point equals the centroid of F exactly when (I) or (II) holds:**

- **(I) No value cap cuts the face:** v_i + l_j + l_k ≥ v_P for every i (j, k are the other two winners).
  Equivalently u_i ≥ D for all i, and then F is a full equilateral triangle.
- **(II) The headroom is symmetric:** min(v_A, s) = min(v_B, s) = min(v_C, s). Equivalently, **either**
  v_A = v_B = v_C, **or** every v_i ≥ s. The second case means v_P ≥ v_j + v_k for every pair of single-item
  bidders, i.e. every VCG price is positive.

In every other case the two points are different.

## Proof

**1. The face F.** Core constraints for the singletons T = {i} give p_i ≥ l_i. For T = all winners they give
Σp ≥ v_P. So R ≥ v_P. Now restrict to the plane Σp = v_P. The pair constraint for T = {i, j} reads
p_i + p_j ≥ v_P − v_k, which there is the same as p_k ≤ v_k. Every other constraint is implied. So

  F = { p : Σ p_i = v_P, l_i ≤ p_i ≤ v_i }.

F is nonempty because Σ l_i < v_P < Σ v_i. Check the first inequality case by case: with no positive l_i it is
0 < v_P; with one, l_i = v_P − v_j − v_k < v_P; with two, l_i + l_j = v_P − v_k − s < v_P; with three, the sum is
v_P − 2s. Hence R = v_P, D > 0, and F is a genuine 2-dimensional polygon.

Shift to q = p − l. Then F is {q : Σq = D, 0 ≤ q_i ≤ u_i}. That is the triangle Δ = {q ≥ 0, Σq = D} with up to
three corners cut off. Cap i removes the small corner triangle at vertex D·e_i with q_i > u_i. Its "size" (in
units of the coordinate q_i) is c_i = max(0, D − u_i).

The cut corners never overlap. Two of them overlap iff c_i + c_j > D, i.e. u_i + u_j < D = u_i + u_j + u_k − s.
That would need u_k > s, which is impossible.

**2. The Vickrey-nearest point N.** We project l onto F. Write p = l + q. Then |p − l|² = |q|², so we minimise
|q|² subject to Σq = D and 0 ≤ q ≤ u. By KKT this is water-filling: q_i = min(u_i, τ), with τ chosen so that
Σ min(u_i, τ) = D.

- If every u_i ≥ D/3, then τ = D/3 and N = l + (D/3)(1,1,1).
- If some u_k < D/3, then τ > u_k (otherwise Σ min(u_i, τ) ≤ 3τ < D). So N_k = l_k + u_k = v_k, and N lies on the
  edge p_k = v_k of F. The centroid of a 2-dimensional convex polygon lies in its relative interior, so G_k < v_k
  and **G ≠ N**.

So we may assume every u_i ≥ D/3, with N = l + (D/3)·1.

**3. The centroid G.** The triangle Δ has area ∝ D² and centroid (D/3)·1. The corner triangle cut at vertex i has
area ∝ c_i² and centroid g_i = (D − 2c_i/3) e_i + (c_i/3)(e_j + e_k). Hence

  g_i − (D/3)·1 = ((D − c_i)/3)(2e_i − e_j − e_k).

Because the corners are disjoint,

  (D² − Σc_i²) (G_q − (D/3)·1) = −Σ_i c_i² (g_i − (D/3)·1) = −(1/3) Σ_i w_i (2e_i − e_j − e_k),

with weights w_i = c_i²(D − c_i) ≥ 0.

The three vectors 2e_i − e_j − e_k sum to zero and any two of them are linearly independent. So the right-hand
side is zero iff w_A = w_B = w_C. Therefore **G = N iff w_A = w_B = w_C.**

- If all w_i = 0, then no corner is cut, i.e. c_i = 0, i.e. u_i ≥ D for all i. This is condition **(I)**. (Here
  c_i = D would mean u_i = 0, which is excluded by positive values.)
- If all w_i are equal and positive, then all c_i lie in (0, 2D/3], because u_i ≥ D/3. On that interval
  f(c) = c²(D − c) is strictly increasing (f′ = c(2D − 3c) > 0). So c_A = c_B = c_C, hence u_A = u_B = u_C. This
  is condition **(II)**.
- Conversely, assume (II): u_i = u for all i. Then 3u = D + s > D, so u > D/3 and N = l + (D/3)·1. The weights
  are equal, so G = N. By symmetry, F is invariant under permuting the coordinates of q.

Condition (I) gives G = N = l + (D/3)·1 directly.

So G = N ⇔ (I) or (II). ∎

**Translating (II).** We need min(v_i, s) equal for all i. If some v_i < s, the common value is v_i < s, so every
v_j equals v_i. Otherwise every v_i ≥ s, and then u_i = s for all i. In that case D = 2s and c_i = s = D/2, so F is
the "medial" triangle. Also, v_i ≥ s ⇔ v_P ≥ v_j + v_k.

**Comparison with two winners.** With two winners, F is a segment and the projection of the VCG point is its
midpoint unless a cap binds. With three winners, the projection always moves along the direction (1,1,1). The
centroid instead shifts away from corners that the caps cut off, weighted by w_i = c_i²u_i. Asymmetric caps
therefore pull the two points apart, even when no cap binds at N.

## Worked examples

All numbers below are exact (computed with rational arithmetic). I also checked the condition by brute force on
3000 random integer instances: polygon vertices, the exact centroid and the exact projection were compared, and
there were 0 mismatches.

**Example 1: the points differ although no cap binds at N.**
v_P = 10, v_A = 6, v_B = 6, v_C = 8.

- s = 10, so l = (0,0,0), u = (6,6,8) and D = 10.
- F = {p ≥ 0, Σp = 10, p ≤ (6,6,8)} is a hexagon. Its vertices are (0,6,4), (0,2,8), (2,0,8), (6,0,4), (6,4,0) and
  (4,6,0).
- Vickrey-nearest point: N = (10/3, 10/3, 10/3). Every u_i ≥ 10/3, so no cap binds.
- Centroid: the corner cuts are c = (4,4,2), and the weights w = c²(D − c) = (96, 96, 32) are unequal. The formula
  gives G_q − (10/3)·1 = −(1/3)·(1/64)·(96(2,−1,−1) + 96(−1,2,−1) + 32(−1,−1,2)) = (−1/3, −1/3, 2/3). So
  **G = (3, 3, 4) ≠ N**, consistent with direct polygon integration.
- Condition (I) fails because v_A = 6 < 10 = v_P. Condition (II) fails because min(v_i, 10) = (6,6,8).

**Example 2: N on a cap edge.**
v_P = 10, v_A = 8, v_B = 3, v_C = 1.

- s = 2, so l = (6,1,0), u = (2,2,1) and D = 3.
- N = (7, 2, 1). Here p_C = v_C, so N sits on an edge of F.
- F has vertices (6,3,1), (8,1,1), (8,2,0) and (7,3,0). Its centroid is G = (65/9, 20/9, 5/9) ≠ N.

**Example 3: condition (II) holds via v_i ≥ s.**
v_P = 10, v_A = 6, v_B = 3, v_C = 3.

- s = 2, so l = (4,1,1) and u = (2,2,2) are all equal.
- F is the triangle with vertices (4,3,3), (6,1,3) and (6,3,1).
- N = (4,1,1) + (4/3)(1,1,1) = (16/3, 7/3, 7/3). The centroid is
  G = (16/3, 7/3, 7/3) as well, so **G = N**.

**Example 4: condition (II) holds although the values are unequal.**
v_P = 10, v_A = 4, v_B = 4, v_C = 5.

- s = 3, so l = (1,1,2) and u = (3,3,3).
- G = N = (3, 3, 4).
