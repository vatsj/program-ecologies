# Vickrey-nearest point vs. centroid of the minimum-revenue face (three winners)

Assume all values are positive and V := v_A+v_B+v_C > v_P > 0. Put d := V − v_P > 0 (the efficiency margin).

## Answer

The Vickrey-nearest point equals the centroid of F **if and only if** at least one of the following holds:

1. v_P ≤ min(v_A, v_B, v_C)  (no corner of the payment triangle is cut off by a value cap; VCG prices are all 0);
2. d ≤ min(v_A, v_B, v_C), i.e. v_P ≥ v_j + v_k for every pair of single-item bidders (every cap min(v_i, d) equals d);
3. v_A = v_B = v_C.

Equivalently: with u_i := min(v_i, d), m := Σu_i − d and corner cuts c_i := max(0, m − u_i), the two points coincide iff
c_A = c_B = c_C. In every case of equality the common point is p^VCG + (m/3)(1,1,1). Otherwise they differ.

**Degenerate cases** (if values may be 0): if v_P = 0, F is the single point 0. If some v_k = 0, then p_k = 0 and, in
the shifted coordinates of Step 2, u_k = 0 so the key fact m ≤ u_i + u_k gives m ≤ u_i and m ≤ u_j: F − p^VCG is the
whole segment {q_i + q_j = m, q ≥ 0}, whose nearest point to 0 and centroid are both its midpoint. So with nonnegative
values the full condition is: v_P = 0, or min v_i = 0, or one of 1–3 (checked exhaustively for integer values 0..5).

## Proof

**Step 1 (the face).** For a subset T of winners the core constraint reads Σ_T p_i ≥ Σ_T v_i − d. Taking T = all winners
gives Σp ≥ v_P, and p_i = v_i·v_P/V attains it, so R = v_P. On the plane Σp = v_P, the constraint for T is equivalent to
Σ_{j∉T} p_j ≤ Σ_{j∉T} v_j, implied by p_j ≤ v_j. Hence

  F = { p : Σ p_i = v_P, 0 ≤ p_i ≤ v_i }.

On F, p_i = v_P − p_j − p_k ≥ v_P − v_j − v_k = v_i − d, so p_i ≥ max(0, v_i − d) = p_i^VCG automatically.

**Step 2 (shift to VCG).** Let q = p − p^VCG. Then u_i := v_i − p_i^VCG = min(v_i, d) and

  F − p^VCG = Q := { q : Σ q_i = m, 0 ≤ q_i ≤ u_i },  m = v_P − Σ p^VCG = Σ u_i − d.

Since u_i ≤ d we get **m ≤ u_j + u_k for every pair** (key fact). Also m > 0 for positive values (if all v_i ≤ d then
m = v_P; otherwise some u_i = d and m = u_j + u_k > 0), and Σu − m = d > 0,
so Q is a genuine 2-dimensional polygon.

**Step 3 (Vickrey-nearest point).** It minimizes Σ q_i² over Q (VCG is the origin). By KKT (or water-filling) the
minimizer is q_i = min(u_i, t) with t chosen so Σ min(u_i, t) = m. It lies in the relative interior of Q iff no cap
binds, i.e. iff it equals (m/3)(1,1,1) with u_i > m/3 for all i; otherwise some q_i = u_i and it is on the boundary.

**Step 4 (centroid).** Q is the triangle Δ = {q ≥ 0, Σq = m} minus the corner triangles K_i = {q ∈ Δ : q_i > u_i}, of
side length proportional to c_i = max(0, m − u_i). By the key fact, K_i ∩ K_j = ∅ (a common point would need
q_i + q_j > u_i + u_j ≥ m). The centroid of K_i is ((m+2u_i)/3) e_i + (c_i/3)(e_j + e_k), its area is proportional to c_i²,
so with D = m² − Σ c_i² > 0,

  g − (m/3)(1,1,1) = −(1/(3D)) Σ_i f(c_i) (2e_i − e_j − e_k),  f(c) = c²(m − c),

equivalently g_i − g_j = (f(c_j) − f(c_i))/D.

**Step 5 (comparison).** The centroid is in the relative interior of the 2-dimensional polygon Q. So if the two points
coincide, the nearest point is interior, hence (Step 3) it is (m/3)(1,1,1); so equality holds iff g = (m/3)(1,1,1) iff
f(c_A) = f(c_B) = f(c_C) — and in that case automatically the projection is interior (shown below), so the condition is
also sufficient. Now f is strictly monotone on the relevant pairs: for a, b ≥ 0 with a + b ≤ m (true for cuts: if both are positive,
c_i + c_j = 2m − u_i − u_j ≤ m; if one is 0, the other is < m because u_i > 0),

  f(a) − f(b) = (a − b)[m(a+b) − (a² + ab + b²)],  and m(a+b) − (a²+ab+b²) ≥ (a+b)² − (a²+ab+b²) = ab ≥ 0,

with strict positivity unless a = b = 0 or (one is 0 and the other is m, i.e. some u_i = 0, i.e. some v_i = 0 — excluded).
Hence f(c_i) = f(c_j) ⇔ c_i = c_j, and g = centre ⇔ c_A = c_B = c_C. Sufficiency: if all c_i = c then all u_i are equal
(= m − c) or all u_i ≥ m; either way u_i > m/3 (equal caps: 3u − m = d > 0), so the projection is (m/3)(1,1,1) = g.

**Step 6 (translate to values).** All c_i = 0 ⇔ u_i ≥ m ∀i. If every v_i ≤ d, then u = v, m = v_P: condition is
v_P ≤ min v_i (case 1). If some v_i > d, then u_i = d and m = u_j + u_k, so u_j ≥ m forces u_k = 0: impossible.
All c_i equal and positive ⇔ u_A = u_B = u_C < m: either all v_i ≥ d (u_i = d, m = 2d > d; case 2) or all v_i < d and
equal (case 3); mixed cases give u = (d, d, v_k<d) or similar, not equal. ∎

(The conditions were also checked numerically: exact polygon centroid vs. projection on 20,000 random integer instances,
zero mismatches against both the c-equality and the 3-case form.)

## Worked examples

**Different.** v_P = 10, v_A = 8, v_B = 4, v_C = 2. V = 14, d = 4, p^VCG = (4, 0, 0), u = (4, 4, 2), m = 6, R = 10.
F = {p_A+p_B+p_C = 10, 4 ≤ p_A ≤ 8, 0 ≤ p_B ≤ 4, 0 ≤ p_C ≤ 2}, a quadrilateral with vertices
(8,2,0), (8,0,2), (4,4,2), (6,4,0).
- Vickrey-nearest: water-fill q = min(u, t) with t = 2 → q = (2,2,2), **p = (6, 2, 2)** (C's cap binds; boundary point).
- Centroid: c = (2, 2, 4), f(c) = (16, 16, 32), D = 36 − 24 = 12, so g − (2,2,2) = (4/9, 4/9, −8/9) and
  **centroid = (58/9, 22/9, 10/9) ≈ (6.444, 2.444, 1.111)**. Distance between them = √96/9 ≈ 1.089.

**Different, with no cap binding at the nearest point** (the contrast with two winners; example due to sol).
v_P = 3, v = (2, 3, 3): d = 5, p^VCG = (0,0,0), u = (2,3,3), m = 3, c = (1,0,0). F has vertices (0,0,3), (2,0,1),
(2,1,0), (0,3,0). Nearest point = **(1, 1, 1)** (interior; no cap binds). f(c) = (2,0,0), D = 9 − 1 = 8, so
**centroid = (1,1,1) + (−1/6, 1/12, 1/12) = (5/6, 13/12, 13/12)**. So even when no value cap binds the Vickrey-nearest
point, a cap that merely cuts the face (v_A < v_P) pulls the centroid away from it.

**Equal (case 3).** v_P = 10, v = (7, 7, 7): d = 11, p^VCG = 0, u = (7,7,7), m = 10, c = (3,3,3);
F is the hexagon {Σp = 10, 0 ≤ p_i ≤ 7}, and both points equal (10/3, 10/3, 10/3).

**Equal (case 2, unequal values).** v_P = 30, v = (16, 14, 12): d = 12 ≤ min v ✓. p^VCG = (4, 2, 0), u = (12,12,12),
m = 24, c = (12,12,12): F is the triangle with vertices (16,14,0), (16,2,12), (4,14,12) and both points are
p^VCG + (8,8,8) = **(12, 10, 8)**.

**Equal (case 1).** v_P = 3, v = (4, 5, 6): F is the full triangle {p ≥ 0, Σp = 3}; both points are (1,1,1).
