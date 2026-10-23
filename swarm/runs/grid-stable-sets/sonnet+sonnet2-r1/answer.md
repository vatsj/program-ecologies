# Answer

**A stable set exists iff K is even. For K = 2m it is unique: V = {(0,m,m), (m,0,m), (m,m,0)}. For odd K there is none.**
(Brute-force enumeration with `/work/enum.py` for K = 2..11 agrees: exactly one stable set for even K, none for odd K.)

## Proof

**Lemma 1 (internal stability).** For distinct x, y, let d = x−y. Its entries sum to 0 and d≠0. If d has two positive entries, x dominates y. If d has two negative entries, y dominates x. The only sign pattern left is one +, one −, one 0. So distinct x, y do not dominate each other iff they **agree in some coordinate (same position, same value)**. Hence V is internally stable iff any two elements agree somewhere.

**Step 1: V is not a star.** Suppose all elements of V share one value in one position. By symmetry say x_1 = c for all x∈V, so V lies on the line L_c = {x_1 = c}. Two points of L_c never dominate each other (Lemma 1). So a point of L_c outside V would be undominated, and V = L_c. Now there are two cases.
- If c = K, then V = {(K,0,0)}. The point (K−1,1,0) is undominated by it, since it is strictly better only for player 1.
- If c < K, take y = (c+1, y_2, y_3) with y_2+y_3 = K−c−1. An element (c,b,K−c−b) of V could dominate y only through players 2 and 3. That needs b > y_2 and K−c−b > y_3, so y_2+y_3+2 ≤ K−c. But y_2+y_3+2 = K−c+1. So y is undominated and not in V.

Either way V is not externally stable. So a stable set is not a star.

**Step 2: V has exactly three elements, of the form P_k = v + e·e_k.** Since V is not a star, |V| ≥ 2. Take x ≠ y in V. By Lemma 1 they agree in some position, say 3. Write x = (a,b,c) and y = (a',b',c). Then a≠a' and b≠b'. Since V is not a star, there is z∈V with z_3 ≠ c.
- z must agree with x and with y in position 1 or 2.
- z_1 cannot equal both a and a', so z = (a,b',·) or z = (a',b,·).
- Swapping the names of x and y, assume z = (a,b',d).

Put v = (a, b', c) and σ = v_1+v_2+v_3. Put e = K−σ. Then:
- x = (v_1, K−v_1−v_3, v_3) = v + e·e_2
- y = (K−v_2−v_3, v_2, v_3) = v + e·e_1
- z = (v_1, v_2, K−v_1−v_2) = v + e·e_3

Write P_k = v + e·e_k. We have x ≠ y, and x_2 = K−a−c while y_2 = b'. These differ exactly when e ≠ 0, so e ≠ 0.

Now let w ∈ V be arbitrary. Put M = {i : w_i = v_i} and T = {k : w_k = v_k+e}. Then M∩T = ∅ because e≠0. Position k of P_k holds v_k+e, and every other position i holds v_i. By Lemma 1, w agrees with each P_k. So for every k, either M∖{k} ≠ ∅ or k∈T.
- If |M| ≥ 2: w agrees with v in two positions, so the third coordinate is forced by the sum, and w = P_k for the remaining k.
- If |M| = 1, M = {i}: then k = i needs i∈T, but i∈M, a contradiction.
- If |M| = 0: then T = {1,2,3}. The sum gives σ+3e = K = σ+e, so e = 0, a contradiction.

So V = {P_1, P_2, P_3} with P_k = v + e·e_k, v_i ≥ 0, σ+e = K and e ≠ 0. Write each u as u = v+f with Σf = e.

**Step 3a: e > 0 is impossible.**
- If e ≥ 2, take f = (1, e−1, 0) and u = v+f. Then u ≥ v and u ∉ V. P_k exceeds u in at most one coordinate (k). So u is undominated.
- If e = 1, then σ = K−1 ≥ 1, so some v_i ≥ 1, say v_1 ≥ 1. Take f = (−1,1,1) and u = v+f ≥ 0. Then u ∉ V. P_1 = v+e_1 is not strictly larger than u in coordinates 2 or 3, so it cannot dominate u. P_2 and P_3 exceed u in coordinate 1 only for k=2 (P_2 has v_1 > u_1 = v_1−1). But in the other coordinates P_2 has v_3 < v_3+1 = u_3 and v_2+1 = u_2. So P_2 beats u only in coordinate 1. The same holds for P_3. So u is undominated.

**Step 3b: e = −g < 0.** Then v_k ≥ g for all k, because P_k ≥ 0. Let u = v+f with Σf = −g, and let N = {i : f_i < 0}.
- P_k dominates u iff two of these hold: f_i < 0 for i≠k, or f_k < −g.
- If |N| ≥ 2, some P_k dominates u: take k to be a third index, or any k if |N| = 3.
- If |N| = 1, N = {i}, then no P_k dominates u. Indeed for k≠i the only available strict coordinate is i, and for k = i, f_k < −g would need the other entries to be negative.
- |N| = 0 is impossible, since Σf < 0.

So every u with exactly one negative f_i must lie in V, and V's elements are f = −g·e_k. Suppose some v_i ≥ g+1. Take f_i = −g−1, f_j = 1 and f_k = 0 for the other two indices. Then u ≥ 0 has |N| = 1 and u ∉ V. This contradicts external stability. So v_i = g for all i. Then K = 3g − g = 2g, and V = {(0,g,g),(g,0,g),(g,g,0)} with g = m.

Hence odd K has no stable set, and for even K = 2m any stable set equals the symmetric set S_m.

**Step 4: S_m is stable for K = 2m.**
- Internal: any two of its elements agree in a coordinate (value m or 0), so by Lemma 1 neither dominates the other.
- External: (0,m,m) dominates y iff y_2 < m and y_3 < m, and similarly for the other two elements. So y is undominated by S_m iff, for each i, some coordinate other than i is ≥ m. In particular, then at least two coordinates are ≥ m. With sum 2m, y is a permutation of (m,m,0), which lies in S_m. So every y ∉ S_m is dominated.

∎
