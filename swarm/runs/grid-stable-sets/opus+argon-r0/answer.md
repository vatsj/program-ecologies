# Stable sets of three-player majority division on the grid {x ∈ Z³_{≥0} : x₁+x₂+x₃ = K}

## Answer

1. A stable set exists **if and only if K is even**.
2. For even K = 2h the stable set is **unique**:
   V* = {(0,h,h), (h,0,h), (h,h,0)}.
   For odd K there are no stable sets.

Computer check: an exhaustive search over all kernels of the dominance digraph (`/work/opus/enum.py`) gives exactly
this for K = 2,…,11 (one stable set, the symmetric one, for even K; none for odd K). The proof below covers every K ≥ 2.

## Proof

Notation: e₁, e₂, e₃ are the unit vectors. "x dom y" means x dominates y.

### Lemma 1 (incomparability). For distinct allocations x, y: neither dominates the other ⇔ x and y agree in exactly one coordinate (x_i = y_i for exactly one i).

Let d = x − y ≠ 0, with d₁+d₂+d₃ = 0. x dom y ⇔ d has at least two positive entries; y dom x ⇔ d has at least
two negative entries. So neither holds ⇔ d has at most one positive and at most one negative entry. Because d ≠ 0 and
sums to 0, it has at least one positive and one negative entry, so this means exactly one of each and one zero. (Two
distinct allocations cannot agree in two coordinates, since the third would agree too.) ∎

So V is internally stable ⇔ every two distinct elements of V agree in exactly one coordinate.

### Lemma 2 (structure of internally stable sets). If V is internally stable, then either
(a) V ⊆ L_{k,c} := {x : x_k = c} for some k and c (a "line"), or
(b) up to a permutation of the players, V = {x, y, z} with x₃ = y₃, z₁ = x₁, z₂ = y₂ (a "triangle").

Proof. If |V| ≤ 1, (a) holds. If |V| = 2, the two points agree in some coordinate, so (a) holds. Otherwise suppose
V is not contained in any line. Pick distinct x, y ∈ V. By Lemma 1 they agree in some coordinate; after permuting
players, x₃ = y₃ = r. Let L = V ∩ L_{3,r}. Since V ⊄ L, some z ∈ V has z₃ ≠ r. Any such z must agree with each point
of L in coordinate 1 or 2. Points of L are pairwise distinct in coordinates 1 and 2 (two points of L agree in coordinate 3
and so cannot agree anywhere else). So z₁ equals the first coordinate of at most one point of L, and z₂ equals the second
coordinate of at most one point of L. Hence |L| ≤ 2, so L = {x, y}, and z agrees with x and with y in *different* coordinates
among {1,2}. (If z₁ = x₁ = y₁, then x and y would agree in two coordinates.) After possibly swapping the names x and y,
z = (x₁, y₂, K−x₁−y₂). The only other candidate off L would be z' = (y₁, x₂, K−y₁−x₂). If both were in V, then z and z'
would have to agree somewhere. They differ in coordinate 1 (x₁ ≠ y₁) and in coordinate 2 (x₂ ≠ y₂). Equality in
coordinate 3 means x₁+y₂ = y₁+x₂. Combined with x₁+x₂ = y₁+y₂ this gives x₁ = y₁, a contradiction. So V = {x, y, z}. ∎

**Parametrising triangles.** Write x = (p, ·, r), y = (·, q, r), z = (p, q, ·) and set s := p+q+r−K, c := (p,q,r).
Then x = c − s e₂, y = c − s e₁, z = c − s e₃, i.e.

  V = {c − s e₁, c − s e₂, c − s e₃},  c ∈ Z³_{≥0}, c₁+c₂+c₃ = K+s, s ≠ 0 (the points are distinct).

### Lemma 3. No V of type (a) is externally stable.

WLOG (permute players) V ⊆ L_{3,c}.
- If c < K, take any y with y₃ = c+1 (such y exist). Then y ∉ V. No v ∈ V dominates y: via players {1,3} or {2,3} this
  would need v₃ = c > y₃, which is false. Via players {1,2} it would need v₁+v₂ ≥ y₁+y₂+2, but v₁+v₂ = K−c = y₁+y₂+1.
- If c = K, then V ⊆ {(0,0,K)}, and y = (1,0,K−1) ∉ V is undominated, because (0,0,K) is better than y only for player 3.
∎

### Lemma 4. A triangle V = {c − s e_i} is externally stable only if s = K/2 and c = (s,s,s).

**Case s = −t < 0**, so V = {c + t e_i}, with Σc = K − t.
- *t ≥ 2.* Take w = c + (t−1)e₁ + e₂. It is an allocation, and w ∉ V. For each i, v = c + t e_i satisfies v_j = c_j ≤ w_j
  for every j ≠ i, so v is strictly better than w for at most one player. Hence w is undominated.
- *t = 1.* Here Σc = K − 1 ≥ 1, so c_k ≥ 1 for some k. Take w = c + (1,1,1) − 2e_k. It is ≥ 0, and w ∉ V. Write
  w = c + d with d = (1,1,1) − 2e_k. Then v = c + e_i is strictly better than w for player j exactly when
  (e_i − d)_j > 0:
  - for i = k this vector is (−1,−1,−1) + 3e_k, which is positive only in coordinate k;
  - for i ≠ k it is e_i − (1,1,1) + 2e_k, which is positive only in coordinate k.
  So no element of V dominates w.

**Case s > 0**, so V = {c − s e_i}, with Σc = K + s and c_i ≥ s. If c₁ = c₂ = c₃ = s, then 3s = K + s, so K = 2s and V = V*.
Otherwise, WLOG (permute players) c₁ > s. Take w = c − (s+1, −1, 0) = (c₁−s−1, c₂+1, c₃). It is ≥ 0, and w ∉ V: its
first coordinate is neither c₁−s nor c₁, so it is not c − s e₁, not c − s e₂, and not c − s e₃. Check each v ∈ V:
- v = c − s e₁ = (c₁−s, c₂, c₃) is better than w only for player 1.
- v = c − s e₂ = (c₁, c₂−s, c₃) is better than w only for player 1.
- v = c − s e₃ = (c₁, c₂, c₃−s) is better than w only for player 1.

So w is undominated. ∎

### Lemma 5. For K = 2h, V* = {(0,h,h),(h,0,h),(h,h,0)} is stable.

*Internal stability.* Any two elements of V* agree in exactly one coordinate (that coordinate equals h), so by Lemma 1
neither dominates the other.

*External stability.* Let w ∉ V*.
- If two coordinates of w are < h, say w₁, w₂ < h, then (h,h,0) dominates w via players {1,2}.
- Otherwise at least two coordinates are ≥ h, say w₁, w₂ ≥ h. Since w₁+w₂ ≤ 2h, this forces w = (h,h,0) ∈ V*,
  a contradiction. ∎

### Conclusion

Let V be any stable set. By Lemma 2 it is a subset of a line or a triangle. Lemma 3 rules out lines. Lemma 4 shows that
a triangle must be V* with K = 2s. Hence for odd K there is no stable set, and for even K the only candidate is V*.
Lemma 5 shows that V* is stable. This answers Questions 1 and 2 for every K ≥ 2.

(Contrast with the continuum: VNM's discriminatory solutions {x₃ = c} fail on the grid. The allocations with x₃ = c+1
cannot be dominated, because players 1 and 2 would need two extra units between them but only one is available.)
