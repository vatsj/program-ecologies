# Answer

1. A stable set exists **iff K is even**.
2. For K = 2m the stable set is **unique**: V = {(0,m,m), (m,0,m), (m,m,0)}. For odd K there is none.
   (Brute-force search for K = 2..9 agrees; script in the work notes.)

# Proof

Notation: "x dominates y" means x_i>y_i for at least two coordinates i. All allocations have coordinate sum K.

**Lemma 1 (internal stability).** Two distinct allocations u,v, neither dominating the other, agree in exactly one coordinate.
Proof: neither dominates, so u>v in at most one coordinate and v>u in at most one. Since sums are equal and u≠v, there is exactly one coordinate with u>v and exactly one with v>u. The third coordinate is equal. ∎
So V is internally stable iff any two distinct elements agree in exactly one coordinate.

**Fact 2.** y is not dominated by v iff y_i ≥ v_i for at least two coordinates i.

**Existence for K=2m.** Internal: (0,m,m) and (m,0,m) agree in the third coordinate and differ elsewhere, so by Lemma 1 neither dominates (same for the other pairs). External: (0,m,m) dominates y iff y_2<m and y_3<m, and similarly for the other two elements. Suppose y is dominated by none. Then for each i some coordinate j≠i has y_j≥m. If no coordinate is ≥m, y is dominated, so some coordinate, say y_1≥m. For i=1 we need y_2≥m or y_3≥m; say y_2≥m. Then y_1+y_2≥2m=K forces y_1=y_2=m, y_3=0, so y∈V. Hence every y∉V is dominated. ∎

**Non-existence and uniqueness.** Let V be stable. V is nonempty (an allocation y∉V would need a dominator in V, and V=∅ dominates nothing). By Lemma 1 any two elements of V agree in exactly one coordinate.

*Case A: some coordinate k and value c with x_k=c for all x∈V.* Take k=3.
- If y_3=c and y∉V, a dominator v∈V has v_3=c=y_3, so it would need v_1>y_1 and v_2>y_2. This is impossible because v_1+v_2=y_1+y_2. So all allocations with third coordinate c lie in V.
- If c<K, take y with y_3=c+1. A dominator v∈V has v_3<y_3, so it needs v_1>y_1 and v_2>y_2. Then K-c=v_1+v_2≥y_1+y_2+2=K-c+1, a contradiction. (Such y∉V because V⊆{x_3=c}.) So c=K and V={(0,0,K)}.
- Then y=(1,0,K-1)∉V is not dominated by (0,0,K), which exceeds y only in coordinate 3. Contradiction. So Case A is impossible.

*Case B: no common (coordinate, value).* Take u,v∈V agreeing in coordinate 3, with value c. Since the family is not a star on coordinate 3, there is w∈V with w_3≠c. Then w agrees with u in one of coordinates 1,2 and with v in one of coordinates 1,2. They cannot be the same coordinate, else u,v would agree in two coordinates and hence be equal. So w agrees with u in one of coordinates 1,2 and with v in the other, and w is determined by u and v. Any z∈V with z_3≠c is also such a point. Writing u=(a,b,c), v=(a+d,b-d,c), the candidates are w⁺=(a,b-d,c+d) and w⁻=(a+d,b,c-d). These two disagree in every coordinate, so they are not both in V. Any z∈V with z_3=c, z≠u,v must agree with w in coordinate 1 or 2. This forces z=u or z=v. So V={u,v,w} has exactly 3 elements.

Relabel the shared values: V={A,B,C} with A=(s,t,·), B=(s,·,r), C=(·,t,r). That is, A and B share coordinate 1 (value s), A and C share coordinate 2 (value t), and B and C share coordinate 3 (value r). Let σ=s+t+r and δ=σ-K. Then A=(s,t,r-δ), B=(s,t-δ,r), C=(s-δ,t,r). The three are distinct, so δ≠0.

- σ≤K-2 (δ≤-2): every y≥(s,t,r) coordinatewise with sum K has y≥A in coordinates 1,2, y≥B in coordinates 1,3, and y≥C in coordinates 2,3. By Fact 2 no element of V dominates y, so all such y are in V. There are C(K-σ+2,2)≥6 such y, but |V|=3. Contradiction.
- σ=K-1 (δ=-1): V={(s,t,r+1),(s,t+1,r),(s+1,t,r)}, and s+t+r=K-1. Then t=r=0 and s=0 are forced as follows. If r≥1, take y=(s+1,t+1,r-1)∉V. It is ≥A, B, C in coordinates 1,2, so it is undominated. So r=0. By symmetry (use y=(s+1,t-1,r+1) for t≥1, and the analogous point for s≥1) s=t=0. Then K=1, contradicting K≥2.
- σ=K (δ=0): excluded, since the points would coincide.
- σ≥K+1 (δ≥1): nonnegativity of A,B,C gives s,t,r≥δ. Any y with y_1≥s and y_2≥t has y≥A, y≥B (coordinate 1 and coordinate 2≥t≥t-δ), and y≥C (coordinates 1,2) in two coordinates each. So y is undominated and must lie in V. Such y have the form (s+i,t+j,r-δ-i-j), i,j≥0. Among them only A∈V (B has second coordinate t-δ<t, C has first coordinate s-δ<s). So the only such y is A, i.e. r-δ=0. By symmetry s=t=δ as well. Hence s=t=r=m=δ and K=σ-δ=2m, and V={(m,m,0),(m,0,m),(0,m,m)}.

So a stable set exists only if K is even and then only equals the set above. For odd K neither Case A nor Case B can occur, so no stable set exists. ∎
