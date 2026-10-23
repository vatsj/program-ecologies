# Stable sets of three-player majority division on the grid

## Answer

1. A stable set exists **if and only if K is even**.
2. For even K = 2m the stable set is **unique**:
   V* = { (0,m,m), (m,0,m), (m,m,0) }.
   For odd K there is no stable set.

(Computer check: `python3 enum.py 14` lists every stable set for K = 2..14 by exhaustive search. It finds exactly
the set above for even K and nothing for odd K. `check.py` confirms V* for each even K tested.)

## Proof

Notation: e_1, e_2, e_3 are the unit vectors, and x ~ y means that x and y agree in some coordinate (x_i = y_i for
some i). All allocations have coordinate sum K.

### Lemma 1 (internal stability means sharing a coordinate)
For distinct allocations x and y, neither one dominates the other if and only if x ~ y.

*Proof.* Let d = x − y. Then d is a nonzero integer vector with sum 0.
- If d has no zero coordinate, it has three nonzero coordinates summing to 0. Two of them have the same sign. If they
  are positive, x dominates y; if negative, y dominates x.
- If d_i = 0 for some i, the other two coordinates are t and −t. So x is strictly better for exactly one player and y
  for exactly one player, and neither dominates. ∎

So V is internally stable iff every two distinct elements of V share a coordinate. Two distinct allocations share at
most one coordinate: if two coordinates are equal, the sum forces the third to be equal too.

### Lemma 2 (structure of internally stable sets)
Let V be internally stable. Then one of the following holds:
- (A) V lies in a "line" L_{i,c} = {x : x_i = c}; or
- (B) V = {R + u e_1, R + u e_2, R + u e_3} for some integer vector R and integer u ≠ 0 with sum(R) = K − u. Call this a
  triangle.

*Proof.* Suppose (A) fails. Then |V| ≥ 2, so take distinct x, y ∈ V. They share exactly one coordinate. Relabel so
that this is coordinate 1, with x = (a,b,c) and y = (a,b',c'), where b ≠ b' and c ≠ c'. Since V is not inside x_1 = a,
there is z ∈ V with z_1 ≠ a. z must share a coordinate with x and one with y, both among coordinates 2 and 3. It cannot
match both in the same coordinate, because x_2 ≠ y_2 and x_3 ≠ y_3. After swapping labels 2 and 3 if needed, z_2 = b
and z_3 = c'.

Put t = c − c' ≠ 0. The sum condition gives y = (a, b+t, c−t) and z = (a+t, b, c−t). With R = (a, b, c−t) and u = t
this reads x = R + u e_3, y = R + u e_2, z = R + u e_1, and sum(R) = K − u. So V contains the triangle
T = {P_1, P_2, P_3}, where P_i = R + u e_i.

Now let w ∈ V \ T. Matching P_i in coordinate i means w_i = R_i + u. Matching P_i in a coordinate j ≠ i means
w_j = R_j.
- Suppose w_i = R_i + u for some i, say i = 1. Since u ≠ 0, w_1 ≠ R_1. So for P_2, w must have w_2 = R_2 + u or
  w_3 = R_3.
  - If w_3 = R_3, the sum forces w_2 = R_2, so w = P_1.
  - If w_2 = R_2 + u, then w_3 = R_3 − u. Then w matches P_3 in no coordinate, since w_1 ≠ R_1, w_2 ≠ R_2 and
    w_3 ≠ R_3 + u. This is a contradiction.
- So w_i ≠ R_i + u for every i. Then each P_i needs some j ≠ i with w_j = R_j.
  - If this holds for two indices j, the sum forces the third coordinate k to equal R_k + u, so w = P_k.
  - Otherwise exactly one j has w_j = R_j, and then P_j is matched in no coordinate. This is a contradiction.

So V = T. ∎

### Existence for K = 2m
V* is internally stable because any two of its elements share the value m in one coordinate (Lemma 1).

For external stability, let y ∉ V*. The element (0,m,m) dominates y exactly when y_2 < m and y_3 < m, and the other
two elements behave the same way by symmetry. So y is undominated only if at least two of its coordinates are ≥ m.
Those two coordinates sum to at least 2m = K, so both equal m and the third is 0. Then y ∈ V*, a contradiction. Hence
V* is stable.

### Uniqueness, and non-existence for odd K
Let V be stable. V ≠ ∅, because the empty set is not externally stable. We rule out case (A) of Lemma 2 and every
triangle except V*.

**Case (A): V ⊆ L_{3,c}** (the other values of i are symmetric).
1. **V is the whole line.** Take y ∈ L_{3,c} with y ∉ V. Some x ∈ V must dominate y. But x_3 = y_3, so x would need
   x_1 > y_1 and x_2 > y_2, which is impossible because x_1 + x_2 = y_1 + y_2. Hence V = L_{3,c}.
2. **If c < K, the line fails.** Take y = (K−c−1, 0, c+1). For x ∈ L_{3,c} we have x_3 < y_3, so x dominates y only
   if x_1 > y_1 and x_2 > y_2. That would give x_1 + x_2 ≥ y_1 + y_2 + 2 = K − c + 1. But x_1 + x_2 = K − c, so y is
   undominated. Also y ∉ V.
3. **If c = K, the line also fails.** Then V = {(0,0,K)}, which does not dominate (K,0,0), because its first two
   coordinates are 0.

So case (A) is impossible: the grid allocation one unit above the line cannot be dominated.

**Case (B), u > 0.** Here V = {P_i = R + u e_i} with R ≥ 0. For an allocation y, P_i dominates y iff at least two of
the following hold: y_i < R_i + u, y_j < R_j, y_k < R_k, where {i,j,k} = {1,2,3}.
- **u ≥ 2:** take y = R + e_1 + (u−1)e_2. Then y ≥ R coordinatewise, so for each i only the condition y_i < R_i + u
  can hold. Hence y is undominated. Also y ∉ V, since y − R = (1, u−1, 0) is not u·e_i.
- **u = 1:** sum(R) = K − 1 ≥ 1, so some R_k ≥ 1; say k = 3. Take y = R + (1, 1, −1) ≥ 0, which is not in V.
  - P_1: y_1 ≥ R_1 + 1 and y_2 ≥ R_2, so only y_3 < R_3 holds.
  - P_2: y_2 ≥ R_2 + 1 and y_1 ≥ R_1, so only y_3 < R_3 holds.
  - P_3: y_1 ≥ R_1 and y_2 ≥ R_2, so only y_3 < R_3 + 1 holds.

  So y is undominated.

Either way V is not stable.

**Case (B), u = −s < 0.** Write Q = R. Then V = {Q − s e_i}, sum(Q) = K + s, and Q_i ≥ s (since
P_i ≥ 0). Suppose Q_3 > s; the other indices are symmetric. Take y = Q − s e_3 + e_1 − e_3 = (Q_1 + 1, Q_2, Q_3 − s − 1).
Then y ≥ 0 and y ∉ V. Write d = y − Q = (1, 0, −s−1). The element Q − s e_i dominates y iff at least two of
d_i < −s, d_j < 0, d_k < 0 hold. Only the third coordinate of d is negative, so for each i exactly one of these
conditions holds. Hence y is undominated, which is a contradiction.

Therefore Q_1 = Q_2 = Q_3 = s. Then 3s = sum(Q) = K + s, so K = 2s, and V = {(0,s,s), (s,0,s), (s,s,0)} = V*.

**Conclusion.** Every stable set equals V* with K = 2m. So for odd K no stable set exists, and for even K the set V*
is the unique stable set. This set was shown to be stable above. ∎
