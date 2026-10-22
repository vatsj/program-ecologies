# Vickrey-nearest point vs. centroid of the minimum-revenue face (3 winners)

Notation: V = v_A+v_B+v_C, D = V − v_P > 0 (surplus of efficient allocation), all values > 0.
p^VCG_i = max(0, v_i − D).

## Answer

The Vickrey-nearest point equals the centroid of F **iff at least one of the following holds**:

- **(a)** v_P ≤ v_i ≤ V − v_P for every i (equivalently: all VCG payments are 0 *and* v_P ≤ min v_i; F is the full triangle {p ≥ 0, Σp = v_P}, no value cap binds);
- **(b)** v_P ≥ v_j + v_k for every pair j≠k (equivalently v_i ≥ D for all i);
- **(c)** v_A = v_B = v_C.

Compact form: let x_i = min(v_i, D) and E = v_P − Σ p^VCG_i. The points coincide iff
the numbers h_i = ((E − x_i)^+)^2 · x_i are all equal. That happens iff all x_i ≥ E (case (a)) or x_A = x_B = x_C (cases (b), (c)).

## Proof

**1. Reduce F.** Put r_i = p_i − p^VCG_i. The core constraint for T, Σ_T p_i ≥ Σ_T v_i − D, becomes, with q_i = v_i − p_i ≥ 0, Σ_T q_i ≤ D. With T = all winners, Σq ≤ D, i.e. Σp ≥ V − D = v_P; and Σp = v_P is reachable (any q with 0 ≤ q_i ≤ v_i, Σq = D satisfies all subset constraints because q ≥ 0). So R = v_P and
F = {p : 0 ≤ q_i ≤ v_i, Σq = D}. Single-coalition constraints give q_i ≤ D, so q_i ≤ x_i := min(v_i, D) and note v_i − x_i = p^VCG_i. Hence
F = {p : p^VCG_i ≤ p_i ≤ v_i, Σp = v_P}, i.e. in r-coordinates **F = {0 ≤ r_i ≤ x_i, Σr = E}** with E = v_P − Σp^VCG = Σx_i − D > 0.
p^VCG is r = 0. F is always 2-dimensional (0 < E < Σx).

**2. Vickrey-nearest point.** It is the Euclidean projection of r=0 onto F: r_i = min(x_i, t) with t chosen so Σ = E ("water-filling"; KKT). If all x_i ≥ E/3 it is m = (E/3, E/3, E/3), the projection of p^VCG onto the plane Σp = v_P. Otherwise some r_i = x_i lies on the boundary of F, while the centroid of a 2-D convex polygon is in its interior — so they differ. Conversely if the centroid equals m then m ∈ F and it is the nearest point. So: **points coincide ⇔ centroid(F) = m.**

**3. Centroid.** F = triangle T = {r ≥ 0, Σr = E} minus the corner triangles K_i = {r ∈ T: r_i > x_i}, nonempty iff a_i := E − x_i > 0. The corners are disjoint: K_i ∩ K_j ≠ ∅ needs x_i + x_j < E, i.e. x_k > D, impossible since x_k ≤ D. K_i is similar to T with ratio a_i/E, so area ∝ a_i^2 (T ∝ E^2), and its centroid is g_i = m + ((E−a_i)/3)(3e_i − 𝟙). So
centroid(F) − m = − Σ_i a_i^2 (E − a_i)/3 · (3e_i − 𝟙) / (E^2 − Σ a_i^2).
The three vectors 3e_i − 𝟙 sum to 0 and any two are independent, so Σ w_i(3e_i−𝟙) = 0 ⇔ w_A = w_B = w_C. With E − a_i = x_i this is the condition h_i = ((E−x_i)^+)^2 x_i all equal.

**4. Solve h_A = h_B = h_C.** f(x) = x(E−x)^2 is positive on (0,E), increasing on (0,E/3), decreasing on (E/3,E); h_i = 0 iff x_i ≥ E.
- All h_i = 0: all x_i ≥ E. 
- All positive and equal: at most one x_i can be < E/3 (since x_i + x_j ≥ E). If x < E/3 ≤ y, z with equal f, then y = z and y ≥ E − x, so f(y) ≤ f(E−x) = x^2(E−x) < x(E−x)^2 = f(x), contradiction. So all x_i lie on the decreasing branch where f is injective: x_A = x_B = x_C (see the translation below for x_i < E).
- Mixed zero/positive is impossible by equality.

Translate. *All x_i ≥ E:* if every v_i ≤ D then x = v, E = v_P, giving v_P ≤ v_i ≤ V − v_P (case (a)). If some v_i > D, then x_i = D and E = (k−1)D + Σ_{v_j ≤ D} v_j where k = #{v_i > D}; for k ≥ 2, E > D ≥ x_i fails; for k = 1, E = v_j + v_l > v_j = x_j fails. *x_A = x_B = x_C:* either all v_i ≥ D (case (b); then x = D, E = 2D > x) or all v_i < D and equal (case (c); then E = v_P, and x < E or else we are in (a)). Mixed v_i ≥ D > v_j gives x_i = D > x_j. ∎

(Geometrically: (a) F is the whole triangle; (b) F is the inverted medial triangle of T; (c) F is a 3-fold-symmetric hexagon/triangle — in every equality case F is centrally "balanced" around m. Unlike two winners, a cut-off corner shifts the centroid by an amount ∝ a_i^2(E−a_i) while leaving the Vickrey-nearest point at m.)

Verified numerically: exhaustive integer grid v_i ∈ {1..8}, v_P ∈ {1..V−1} (6400 cases, 2620 coincidences) — the condition matches exactly; plus random real instances.

## Worked examples

**Differ:** v_P = 6, (v_A, v_B, v_C) = (1, 3, 4). V = 8, D = 2, p^VCG = (0, 1, 2), R = 6, E = 3, x = (1, 2, 2).
F = {0 ≤ p_A ≤ 1, 1 ≤ p_B ≤ 3, 2 ≤ p_C ≤ 4, Σp = 6}: a quadrilateral with vertices (0,2,4), (0,3,3), (1,3,2), (1,1,4) in (p_A,p_B,p_C).
- Vickrey-nearest: p^VCG + (1,1,1) = **(1, 2, 3)** (on the edge p_A = 1 = v_A).
- Centroid: a = (2,1,1), centroid − m = (−4/9, 2/9, 2/9), so **(5/9, 20/9, 29/9)** ≈ (0.556, 2.222, 3.222). Different.

**Coincide (case a):** v_P = 2, v = (3, 4, 5): p^VCG = 0, F = full triangle {p ≥ 0, Σp = 2}; both points = (2/3, 2/3, 2/3).
**Coincide (case b):** v_P = 10, v = (2, 4, 6): D = 2, p^VCG = (0, 2, 4), x = (2,2,2), E = 4; F = {p^VCG ≤ p ≤ p^VCG + 2, Σp = 10} (inverted medial triangle); both points = p^VCG + (4/3)(1,1,1) = (4/3, 10/3, 16/3).
