# Vickrey-nearest point vs. centroid of the minimum-revenue face (3 winners)

Assume v_A, v_B, v_C > 0 and v_A + v_B + v_C > v_P ≥ 0.

## Answer

The Vickrey-nearest point (VN) equals the centroid of F **if and only if** at least one of these holds:

1. **v_P ≤ min(v_A, v_B, v_C)** (VCG charges everyone 0, and F is the full triangle {p ≥ 0, Σp = v_P});
2. **v_P ≥ v_i + v_j for every pair i ≠ j**, i.e. v_P + min(v_A,v_B,v_C) ≥ v_A + v_B + v_C (F is again a triangle);
3. **v_A = v_B = v_C** (full symmetry).

In every other case the two points differ. Example: v_P = 4, (v_A, v_B, v_C) = (2, 3, 4) gives VN = (4/3, 4/3, 4/3) and centroid = (31/33, 46/33, 5/3).

## Reduction

Let d = v_A + v_B + v_C − v_P > 0 (the efficient surplus), and write s_i = v_i − p_i for winner i's surplus. The core constraint for a set T of winners, Σ_T p_i ≥ v_P − Σ_{j∉T} v_j = Σ_T v_i − d, becomes **Σ_{i∈T} s_i ≤ d**. The "max(0, ·)" part is just Σ_T s_i ≤ Σ_T v_i, which already follows from s_i ≤ v_i. Because s ≥ 0, the constraint for T = all winners implies all the others. So

core = { s : 0 ≤ s_i ≤ v_i, s_A + s_B + s_C ≤ d }.

Since Σ v_i > d, the maximum total surplus d can be reached. Hence R = Σv_i − d = v_P and

F = { s : 0 ≤ s_i ≤ v_i, Σ s_i = d } = { s : 0 ≤ s_i ≤ m_i, Σ s_i = d },  where m_i := min(v_i, d).

(On F we have s_i ≤ d automatically.) The VCG surplus is s_i^VCG = v_i − max(0, v_i − d) = m_i. Now put t_i = m_i − s_i and E = m_A + m_B + m_C − d. We have E ≥ 0, and E < Σm_i because d > 0. The map is a translation plus reflection, so it is an isometry and keeps centroids and nearest points. It gives

F ≅ { t : 0 ≤ t_i ≤ m_i, t_A + t_B + t_C = E },  VCG ↦ t = 0.

The VN point is the Euclidean projection of the origin onto this capped simplex. By the KKT conditions this is **water-filling**: t*_i = min(λ, m_i), where λ ≥ 0 solves Σ min(λ, m_i) = E.

If E = 0, F is a single point and the two points trivially agree. If 0 < E < Σm_i (with all m_i > 0), F is a genuine 2-dimensional polygon in the plane Σt = E. It has a point with every coordinate strictly inside its range (take t = (E/Σm)·m), so it is not contained in any face t_i = m_i.

## Claim: VN = centroid ⇔ E ≤ min_i m_i, or m_A = m_B = m_C

**(⇐) E ≤ min m_i.** F is the triangle with vertices E·e_A, E·e_B, E·e_C, so its centroid is (E/3, E/3, E/3). Water-filling gives λ = E/3 ≤ min m_i, so t* = (E/3, E/3, E/3) as well.

**(⇐) m_A = m_B = m_C.** F and the origin are both invariant under every permutation of coordinates. The centroid is therefore symmetric. So is the projection, because it is unique and the symmetries are isometries. Both points lie on the line t_A = t_B = t_C inside the plane Σt = E, which meets the plane in the single point (E/3, E/3, E/3).

**(⇒) Suppose E > min m_i and the m_i are not all equal.** Let i have m_i = min m, and choose j with m_j > m_i. Write c for the centroid.

*Step 1: c_j > c_i.* Split F into S = F ∩ {t_i ≤ m_i, t_j ≤ m_i} and its complement F \ S = F ∩ {t_j > m_i}. S is mapped onto itself by swapping coordinates i and j: the constraints on S are 0 ≤ t_i, t_j ≤ m_i and 0 ≤ t_k = E − t_i − t_j ≤ m_k, all symmetric in i and j. Hence ∫_S (t_j − t_i) = 0. On F \ S we have t_j > m_i ≥ t_i, so t_j − t_i > 0 there. F \ S is non-empty: the largest value of t_j on F is min(m_j, E), which exceeds m_i. It is also relatively open in the 2-dimensional convex set F, so it has positive area. Therefore ∫_F (t_j − t_i) > 0, which means c_j > c_i.

*Step 2: c ≠ t*.*
- If λ < m_i, then λ < m_k for all k and t* = (E/3, E/3, E/3), so t*_i = t*_j. But c_i < c_j.
- If λ ≥ m_i, then t*_i = m_i. But F lies in {t_i ≤ m_i} and is not contained in {t_i = m_i}, so the centroid of the 2-dimensional set F satisfies c_i < m_i = t*_i.

Either way VN ≠ centroid. ∎

## Translating back to values

- **E ≤ min m_i** means m_j + m_k ≤ d for every pair. If some v_j ≥ d, then m_j = d and m_k ≤ 0, which is impossible. So all v_i < d, m = v, and the condition reads v_j + v_k ≤ v_A + v_B + v_C − v_P for every pair, i.e. **v_P ≤ v_i for every i**. Conversely, v_P ≤ v_i for every i implies v_i < d (since d − v_i = v_j + v_k − v_P > 0). This is condition 1.
- **m_A = m_B = m_C = x.** If x < d, then v_A = v_B = v_C = x (condition 3). If x = d, then v_i ≥ d for all i, i.e. v_P ≥ v_j + v_k for every pair (condition 2). In case 2, s^VCG = (d, d, d) and F = {s ≥ 0, Σs = d} is the full triangle. Both points equal s = (d/3, d/3, d/3), i.e. p_i = v_i − d/3.

In condition 1, F in p-coordinates is {p ≥ 0, Σp = v_P}, and both points are (v_P/3, v_P/3, v_P/3).

## Worked examples

**Different points: v_P = 4, (v_A, v_B, v_C) = (2, 3, 4).** Here d = 5, R = 4 and p^VCG = (0, 0, 0). F is the pentagon {0 ≤ p_A ≤ 2, 0 ≤ p_B ≤ 3, p_C ≥ 0, Σp = 4} with vertices

(0,0,4), (0,3,1), (1,3,0), (2,2,0), (2,0,2).

- **VN:** the projection of 0 onto the plane is (4/3, 4/3, 4/3). It satisfies every cap, so VN = (4/3, 4/3, 4/3) ≈ (1.333, 1.333, 1.333).
- **Centroid:** project onto (p_A, p_B). The region is the rectangle [0,2]×[0,3] (area 6, centroid (1, 1.5)) minus the corner triangle {p_A + p_B > 4} with vertices (1,3), (2,3), (2,2) (area 1/2, centroid (5/3, 8/3)). The area is 11/2, and
  c_A = (6·1 − ½·5/3)/(11/2) = 31/33, c_B = (6·1.5 − ½·8/3)/(11/2) = 46/33, c_C = 4 − 77/33 = 5/3.
  So the centroid is (31/33, 46/33, 5/3) ≈ (0.939, 1.394, 1.667), which is not VN.

  Note that no cap binds at VN, yet the two points still differ. The two-winner "midpoint" intuition does not carry over to three winners.

**Equal points (condition 2): v_P = 15, (v_A, v_B, v_C) = (3, 6, 9).** Here d = 3 and p^VCG = (0, 3, 6). F is the triangle with vertices (0,6,9), (3,3,9), (3,6,6). The centroid is (2, 5, 8), and the nearest point to (0,3,6) on F is also (2, 5, 8), at squared distance 12.

**Equal points (condition 1): v_P = 1, v = (3, 3, 3).** F is the triangle {p ≥ 0, Σp = 1}, and both points are (1/3, 1/3, 1/3).

**Equal points (condition 3): v_P = 2.5, v = (1, 1, 1).** p^VCG = (0.5, 0.5, 0.5). F is the triangle with vertices (0.5,1,1), (1,0.5,1), (1,1,0.5), and both points are (5/6, 5/6, 5/6).

## Numerical check

`/work/opus_check2.py` enumerates F directly from the original core constraints (LP for R, vertex enumeration, polygon centroid) and computes VN with SLSQP. It ran over 3000 random integer instances. The condition above predicted equality vs. inequality correctly on all of them, except 4 cases (all permutations of v = (3,6,9), v_P = 15) where SLSQP stopped at a wrong point (1,5,9), at squared distance 14 instead of 12. The true VN there equals the centroid, as shown above. `/work/opus_scan.py` checks the reduced (m, E) form on 20000 instances.

Remark: if some v_i = 0, then m_i = 0, F lies in the face t_i = 0, and the problem falls back to the two-winner case.
