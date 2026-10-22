# Vickrey-nearest point vs. centroid of the minimum-revenue face (three winners)

Notation: D = v_P, s = v_A + v_B + v_C > D, δ = s − D > 0. "Centroid" means the area centroid of the polygon F.

## Answer

The Vickrey-nearest point equals the centroid of F **if and only if** at least one of these holds:

1. **min(v_A, v_B, v_C) ≥ v_P.** Then every VCG price is 0, F is the whole triangle {p ≥ 0, Σp = v_P}, and both points are (v_P/3, v_P/3, v_P/3). This is the three-winner version of "no value cap binds".
2. **v_A = v_B = v_C.** Then F is symmetric under every permutation of the winners.
3. **v_P ≥ v_i + v_j for every pair of winners.** Then every VCG price is v_i − δ ≥ 0, every cap slack v_i − p_i^VCG equals δ, and F is a hexagon whose centre lies on the symmetry axis.

In all other cases the two points differ. Put another way: with u_i = min(v_i, s − v_P) and M = v_P − Σ_i p_i^VCG, the points agree iff either all u_i ≥ M or u_A = u_B = u_C.

## Proof

**Step 1: what F looks like.** For a set T of winners, the core constraint is Σ_T p_i ≥ D − Σ_{j∉T} v_j.
- With T equal to all three winners, this says Σp ≥ D.
- The point p with p_i = l_i := max(0, v_i − δ) = p_i^VCG for each i satisfies Σl ≤ D, and Σv = s > D.

So R = D. On the plane Σp = D:
- The pair constraint for {i, j} becomes p_k ≤ v_k.
- The singleton constraint for {i} becomes p_i ≥ D − s + v_i.

Together with 0 ≤ p_i ≤ v_i this gives

  F = { p : Σp = D, l_i ≤ p_i ≤ v_i }.

Substitute q = p − l. Then F becomes {q : Σq = M, 0 ≤ q_i ≤ u_i}, where
- u_i = v_i − l_i = min(v_i, δ), and
- M = D − Σl.

Since min(v, δ) + max(0, v − δ) = v, we get Σu = M + δ > M. So F is a genuine 2-dimensional polygon. Geometrically, F is the triangle T = {q ≥ 0, Σq = M} with the corner at each vertex i cut off. The corner cut at i is the small triangle {q_i ≥ u_i}, with side k_i = max(0, M − u_i).

Two cut corners never overlap. Because u_i ≤ δ = Σu − M, we have u_j + u_k ≥ M for every pair. So the regions {q_j ≥ u_j} and {q_k ≥ u_k} meet in at most a point.

**Step 2: the Vickrey-nearest point.** In q-coordinates, VCG is the vertex q = 0. Projecting it onto F is a water-filling problem: q_i = min(u_i, τ), with τ chosen so that Σq = M.

**Step 3: the case where some u_i ≤ M/3.** Then τ ≥ u_i for that i, so the Vickrey-nearest point lies on the edge q_i = u_i, which is on the boundary of F. The centroid of a 2-dimensional convex polygon lies strictly inside it. So the two points differ.

**Step 4: the case where every u_i > M/3.** Then τ = M/3, and the Vickrey-nearest point is the centre c = (M/3)(1,1,1) of T. Let w_i = e_i − (1/3)(1,1,1). These vectors satisfy w_A + w_B + w_C = 0, and any two of them are linearly independent.
- Take areas in units where the area of a triangle of side x is x².
- The cut corner at i has area k_i². Its centroid has q_i = M − 2k_i/3 and q_j = k_i/3 for j ≠ i, which equals c + (M − k_i) w_i.
- T has area M² and centroid c.

So the centroid of F is

  g = c − [Σ_i k_i² (M − k_i) w_i] / (M² − Σ_i k_i²).

Because the w_i sum to zero and any two are independent, g = c iff the three numbers f(k_i) = k_i²(M − k_i) are equal. Now u_i > M/3 means k_i ∈ [0, 2M/3). On that interval f′(k) = k(2M − 3k) > 0 for k > 0, so f is strictly increasing there. Hence g = c iff k_A = k_B = k_C. That happens exactly when:
- (a) all u_i ≥ M, so no corner is cut, or
- (b) u_A = u_B = u_C < M. Here u_i = (M + δ)/3 > M/3 holds automatically.

If u_A = u_B = u_C ≥ M, case (a) already covers it. Together with Step 3, the two points coincide iff (a) or (b) holds.

**Step 5: translate back to the values.**
- **(b)** says min(v_i, δ) is the same for all three winners. That means either v_A = v_B = v_C, or every v_i ≥ δ. The second option is equivalent to D ≥ v_j + v_k for every pair, which is condition 3.
- **(a)** says p_i^VCG + M ≤ v_i for all i, i.e. the full triangle fits under the caps. This is impossible if any VCG price is positive:
  - If only l_A > 0, then M = v_B + v_C > v_B.
  - If l_A and l_B are positive and l_C = 0, then M = δ + v_C > v_C.
  - If all three are positive, then M = 2δ > δ = u_i.

  So (a) requires all l_i = 0, hence M = D, and then (a) reads v_i ≥ D for all i. Conversely, if every v_i ≥ D then every l_i = 0. So (a) is exactly condition 1. ∎

A randomized check over 20,000 integer instances (values 1–10, v_P < s) compared exact polygon centroids with the water-filling projection. The iff matched every instance.

## Worked examples

**Example where the points differ:** v_P = 10, (v_A, v_B, v_C) = (6, 5, 4).
- s = 15 and δ = 5.
- p^VCG = (1, 0, 0), so M = 9 and u = (5, 5, 4).
- F = {Σp = 10, 1 ≤ p_A ≤ 6, 0 ≤ p_B ≤ 5, 0 ≤ p_C ≤ 4}, a hexagon.
- Vickrey-nearest point: water-filling gives τ = 3, so q = (3, 3, 3) and **p = (4, 3, 3)**. This is interior, since 3 < u_i.
- Centroid: the corners cut off have k = (4, 4, 5), so f(k) = (80, 80, 100). Then Σ f(k_i) w_i = 20 w_C, and the remaining area is 81 − 57 = 24. So g − c = −(20/24) w_C = (5/18, 5/18, −10/18). Hence q_g = (59/18, 59/18, 44/18) and **p_g = (77/18, 59/18, 22/9) ≈ (4.278, 3.278, 2.444)**.
- The two points differ. The centroid is pulled away from C, whose cap cuts the largest corner.

**Examples where the points agree:**
- v_P = 10, (4, 4, 4): condition 2. p^VCG = (2, 2, 2), and both points are (10/3, 10/3, 10/3).
- v_P = 12, (3, 4, 7): condition 3. p^VCG = (1, 2, 5), M = 4, u = (2, 2, 2). Both points are (7/3, 10/3, 19/3).
- v_P = 5, (6, 7, 8): condition 1. Both points are (5/3, 5/3, 5/3).
