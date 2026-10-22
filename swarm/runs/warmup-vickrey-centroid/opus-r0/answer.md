# When is the Vickrey-nearest point the centroid of the minimum-revenue face? (three winners)

Write S = v_A + v_B + v_C, so S > v_P. Assume v_P > 0. If v_P = 0, then F = {0} = p^VCG and the claim is trivial.

## Answer

The Vickrey-nearest point equals the centroid of F **if and only if at least one of these holds:**

1. **v_P ≤ min(v_A, v_B, v_C).** Every VCG price is 0 and no value cap touches F.
2. **v_P ≥ the sum of the two largest values**, i.e. v_P ≥ v_i + v_j for every pair. Every VCG price is positive, and F is
   the whole triangle {p ≤ v, Σp = v_P}.
3. **v_A = v_B = v_C** (any v_P). This is the fully symmetric case.

In every other case the two points differ. Example: v = (1, 2, 3), v_P = 3. The centroid is (1/2, 1, 3/2) and the
Vickrey-nearest point is (1, 1, 1). Details are below.

## Proof

### Step 1: R = v_P and F = {Σp = v_P, 0 ≤ p_i ≤ v_i}

Taking T = all winners gives Σp ≥ v_P, so R ≥ v_P. Now restrict to the plane Σp = v_P:

- The pair constraint for T = {i, j} reads p_i + p_j ≥ v_P − v_k. Since p_i + p_j = v_P − p_k, this is exactly p_k ≤ v_k.
- The singleton constraint p_i ≥ v_P − v_j − v_k becomes v_P − p_j − p_k ≥ v_P − v_j − v_k. This follows from p_j ≤ v_j
  and p_k ≤ v_k. The constraint p_i ≥ 0 is listed separately.

So on that plane the core is exactly {0 ≤ p ≤ v, Σp = v_P}. This set is non-empty: p = (v_P/S)·v belongs to it. Hence
R = v_P and F is as stated.

### Step 2: switch to slack coordinates

Let s = S − v_P > 0 and q_i = v_i − p_i. In these coordinates:

- F = {Σq = s, 0 ≤ q_i ≤ v_i}.
- VCG is p^VCG_i = max(0, v_i − s), so q^VCG_i = m_i := min(v_i, s).
- Since q_i ≤ s already holds on Σq = s, q ≥ 0, we can write F = {Σq = s, 0 ≤ q_i ≤ m_i}. This is a slice of the box
  [0, m] whose corner farthest from the origin is the VCG point m.
- Σm > s, because either every m_i = v_i, giving Σm = S > s, or some m_i = s while the others are positive. Every m_i > 0.
  So F is a genuine 2-dimensional polygon. Its centroid g therefore lies in the relative interior, and in particular
  g_i > 0 for every i: if q_i = 0 held on all of F, F would be a segment.

### Step 3: the Vickrey-nearest point

This is the Euclidean projection of m onto box ∩ hyperplane. By the KKT conditions it is q*_i = clip(m_i − t, 0, m_i),
with t chosen so that Σq* = s. Because Σm ≥ s we have t ≥ 0, so q*_i = max(m_i − t, 0).

Let τ = (Σm − s)/3 and G = m − τ·1, the projection of m onto the plane.

- If m_i ≥ τ for all i, then q* = G.
- Otherwise some coordinate gets clipped, and q* has a zero coordinate. Then q* ≠ g, because g_i > 0.

### Step 4: the centroid

Let T = {Σq = s, q ≤ m}, using only the upper caps. It is a triangle with vertices V_i = m − 3τ e_i and centroid
(V_1 + V_2 + V_3)/3 = G. We have F = T ∩ {q ≥ 0}.

On T, q_i runs from m_i − 3τ (at V_i) to m_i (on the opposite side). So the half-plane q_i < 0 cuts off a corner
triangle at V_i that is homothetic to T with ratio

  r_i = max(0, 1 − m_i/(3τ)) ∈ [0, 1).

Two corners never overlap. If q_i < 0 and q_j < 0, then q_k = s − q_i − q_j > s ≥ m_k, which is impossible in T.

Write A for the area of T. Corner i has area r_i²·A, and its centroid is c_i = V_i + r_i(G − V_i). This gives
c_i − G = (1 − r_i)(V_i − G), and V_i − G = τ(1 − 3e_i). Removing the corners from T:

  g − G = − τ / (1 − Σ r_j²) · Σ_i w_i (1 − 3 e_i),  where w_i = r_i²(1 − r_i).

Here 1 denotes the all-ones vector. Coordinate k of Σ_i w_i(1 − 3e_i) is W − 3w_k, where W = Σw_i. So **g = G if and only
if w_1 = w_2 = w_3.**

### Step 5: putting it together

From Steps 3 and 4, q* = g holds iff m_i ≥ τ for all i and w_1 = w_2 = w_3.

The condition m_i ≥ τ is the same as r_i ≤ 2/3. On [0, 2/3] the function f(r) = r²(1 − r) is strictly increasing, since
f'(r) = r(2 − 3r) > 0 there. So the w_i are equal iff the r_i are equal. That happens in two ways:

- **All r_i = 0.** Then F = T and nothing is cut. This means m_i ≥ 3τ = Σm − s, i.e. s ≥ m_j + m_k for every i. If some
  v_i > s, then m_i = s and s ≥ s + m_k is impossible. So m = v, and the condition reads S − v_P ≥ S − v_i for all i,
  i.e. **v_P ≤ min v_i** (case 1). Here r_i = 0 ≤ 2/3 holds automatically.
- **All r_i equal and positive.** Then all m_i are equal, say to M, and τ = M − s/3 ≤ M, so r_i ≤ 2/3 holds. Equal
  m_i = min(v_i, s) means one of two things:
  - All v_i ≥ s. This is s ≤ min v, i.e. v_P ≥ S − min v, the sum of the two largest values (case 2). Here
    F = {q ≥ 0, Σq = s} is the full triangle.
  - All v_i are equal and below s (case 3).

  (Equal m_i with r_i = 0 is already covered by the first bullet.)

Conversely, in every case where these conditions fail, either some coordinate gets clipped (so q* ≠ g by Step 3), or the
w_i are unequal (so g ≠ G = q* by Step 4). ∎

In words: the two points coincide only when the face is an untruncated triangle whose position relative to VCG is
symmetric. That happens in cases 1 and 2, where F is a full triangle and the VCG point projects onto its centroid, and in
the fully symmetric case 3. Once F is a truncated triangle (a quadrilateral, pentagon or hexagon) and the values are not
all equal, the two points always differ. This is unlike the two-winner case, where the face is a segment and the
projection of VCG is its midpoint.

## Worked examples

**Example 1 (they differ): v = (1, 2, 3), v_P = 3.**

- S = 6 and s = 3. VCG = (max(0, 1−3), max(0, 2−3), max(0, 3−3)) = (0, 0, 0). R = 3.
- F = {p_A + p_B + p_C = 3, 0 ≤ p ≤ (1, 2, 3)}. This is the parallelogram with vertices (0,0,3), (1,0,2), (1,2,0),
  (0,2,1).
- **Centroid** (the vertex average, because F is a parallelogram) = **(1/2, 1, 3/2)**.
- **Vickrey-nearest**: project (0,0,0) onto Σp = 3 to get (1,1,1). It satisfies p ≤ v, so it is the point:
  **(1, 1, 1)**.
- They differ. The Vickrey-nearest point splits the payment equally, while the centroid is proportional to the values.

**Example 2 (they differ, VCG not zero): v = (4, 4, 1), v_P = 4.**

- s = 5 and VCG = (0, 0, 0). F has vertices (3,0,1), (4,0,0), (0,4,0), (0,3,1).
- Centroid = (37/21, 37/21, 10/21). Vickrey-nearest = (3/2, 3/2, 1) (the cap p_C ≤ 1 binds).

**Example 3 (they coincide, case 2): v = (2, 2, 3), v_P = 6 ≥ 2 + 3.**

- s = 1. VCG = (1, 1, 2). F = {p ≤ (2, 2, 3), Σp = 6}, the triangle with vertices (2,2,2), (2,1,3), (1,2,3).
- Centroid = (5/3, 5/3, 8/3) = VCG + (1/3)(1,1,1) = Vickrey-nearest.

**Example 4 (they coincide, case 1): v = (2, 3, 4), v_P = 2.** VCG = 0, F is the full simplex {p ≥ 0, Σp = 2}, and both
points are (2/3, 2/3, 2/3).

## Numerical check

Using exact rational arithmetic, I computed the polygon, its centroid and the water-filling projection for:

- every integer v ∈ {1..9}³ with every integer v_P < S;
- 30,000 random rational instances, 20% of them with two equal values.

The two points coincided exactly when the condition (case 1, 2 or 3) held, with no exceptions.
