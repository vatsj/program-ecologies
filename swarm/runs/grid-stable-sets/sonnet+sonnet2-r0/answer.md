# Answer

1. A stable set exists **iff K is even**.
2. For even K the stable set is **unique**: V = {(K/2,K/2,0), (K/2,0,K/2), (0,K/2,K/2)}.
   For odd K there is none. (Confirmed by exhaustive search for K = 2..9, `enum.py`.)

# Proof

Write x ≤_i-count: "x dominates y" iff x>y in at least two coordinates. So x does NOT dominate y iff x ≤ y in at least two coordinates.

## Step 0: the symmetric set is stable when K is even
Let h=K/2, V={(h,h,0),(h,0,h),(0,h,h)}.
*Internal:* two distinct elements, e.g. (h,h,0) and (h,0,h), are equal in coordinate 1, so the first exceeds the second only in coordinate 2. No domination.
*External:* let y∉V. (h,h,0) dominates y iff y1<h and y2<h; similarly for the other two pairs. If y is dominated by none, then no two coordinates of y are both <h, so at least two coordinates are ≥h. Sum is 2h=K, so those are exactly h and the third is 0, i.e. y∈V. Contradiction. So V is stable.

## Step 1: structure of internally stable sets
Let V be stable (V is nonempty since allocations exist and must be dominated). For distinct x,y∈V, x≤y in ≥2 coordinates and y≤x in ≥2 coordinates; these two sets of coordinates intersect, so x,y **agree in some coordinate**. Since sums are equal, in the other two coordinates one is strictly larger for x and the other strictly larger for y (they differ, else x=y).

Take x,y∈V distinct, agreeing in coordinate i with value a. Either
(A) every element of V has coordinate i equal to a ("line case"), or
(B) some u∈V has u_i≠a. Then u agrees with x in some coordinate j and with y in some coordinate k. j≠i,k≠i. If j=k, then x_j=u_j=y_j, so x,y would agree in two coordinates and hence be equal; contradiction. So j≠k: wlog i=1, j=2, k=3. Write x=(a,b,c). y=(a,b+d,c−d) with d≠0, u=(u1,b,u3) with u3=y3=c−d, so u=(a+d,b,c−d). So V⊇{x,y,u}, a "triangle":
 x=(a,b,c), y=(a,b+d,c−d), u=(a+d,b,c−d), d≠0.
 A fourth element w must agree with each of x,y,u in some coordinate. If w1=a: w differs from u at coordinate 1, so w2=b (then w=x) or w3=c−d (then w=y). If w1≠a: w agrees with x and with y in coordinates from {2,3}; if w2=b then (y2≠b) w3=c−d and w=u; if w3=c then y3≠c forces w2=b+d, w=(a−d,b+d,c), which disagrees with u everywhere, impossible. So V={x,y,u} exactly.

## Step 2: case (A) is impossible
V⊆L={z: z_i=a}. Two points of L never dominate each other (they tie in coordinate i). A point of L not in V can be dominated only by an element of V⊆L, which can't happen, so V=L. Take i=1 wlog.
- If a<K: the allocation w=(a+1, w2, w3), w2+w3=K−a−1, is not on L. It is dominated by (a,s,K−a−s)∈L only if a>w1 (false) or both s>w2 and K−a−s>w3, which needs w2+w3+2≤K−a=w2+w3+1, false. So w is not dominated: contradiction.
- If a=K: V={(K,0,0)}. Then (0,K,0) is not dominated (the only element has coordinates 2,3 equal to 0, never greater than K, 0... needs two strictly greater coordinates; (K,0,0) exceeds (0,K,0) only in coordinate 1). Contradiction.

## Step 3: case (B), triangle, d>0 is impossible
Put u0=a, v0=b, t0=c−d (all ≥0): x=(u0,v0,t0+d), y=(u0,v0+d,t0), u=(u0+d,v0,t0), u0+v0+t0+d=K. Any w=(u0+p,v0+q,t0+r), p,q,r≥0, p+q+r=d is ≥x in coords 1,2, ≥y in coords 1,3, ≥u in coords 2,3, so no triangle element dominates it. Hence (V being stable) w∈V for all such w, but there are C(d+2,2) of them, >3 unless d=1. So d=1 (and these w are the triangle). If t0≥1, w=(u0+1,v0+1,t0−1) is a valid allocation, not in the triangle, and it is ≥x in coords 1,2; ≥y in 1,2... precisely: x3=t0+1>t0−1 only one coordinate exceeds; y: only coordinate 3 exceeds; u: only coordinate 3 exceeds. So it's undominated: contradiction. So t0=0, and symmetrically (the triangle is symmetric under coordinate permutations) u0=v0=0, giving K=1, contradicting K≥2.

## Step 4: case (B), d<0
Let e=−d>0, U=a, W=b, T=c+e: x=(U,W,T−e), y=(U,W−e,T), u=(U−e,W,T), all ≥0, K=U+W+T−e.
Any w with w1≥U and w2≥W is not dominated by x (≥ in coords 1,2), y (coords 1,2 since w2≥W>W−e), or u (coords 1,2). Such w exist as allocations (e.g. x itself) with w3=K−w1−w2≤T−e. Those must all lie in V, but among triangle points only x has w1≥U,w2≥W (y2=W−e<W, u1<U). So (U,W) must be the only pair: the pair (U+1,W) must not be an allocation, i.e. U+W+1>K, i.e. x3=T−e<1, so T−e=0. By the symmetric argument with coordinate pairs (1,3) and (2,3) (using y and u): y2=W−e=0 and u1=U−e=0. So U=W=T=e, K=2e is even and V={(e,e,0),(e,0,e),(0,e,e)}, the symmetric set.

## Conclusion
Every stable set is the symmetric set with K even (Steps 1–4), and for K even it is stable (Step 0). Hence stable sets exist iff K is even, and then the stable set is unique; for odd K none exists. (No discriminatory solutions survive discretization for K≥2.) ∎
