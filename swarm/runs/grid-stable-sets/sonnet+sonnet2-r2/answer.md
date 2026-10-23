# Answer

**A stable set exists iff K is even. For K = 2h it is unique: V = {(h,h,0), (h,0,h), (0,h,h)}.** For odd K there is none.
(Verified by exhaustive search for K = 2..12 with /work/bf.py, and by the proof below for all K.)

## Proof

Notation: x dom y iff x_i>y_i for at least two coordinates. Two distinct allocations cannot dominate each other
(the two pairs of players would share a player, giving x_i>y_i and y_i>x_i). 

### Sufficiency (K=2h)
Internal: two points of V differ by ±h in two coordinates and agree in the third, so each beats the other in only one coordinate.
External: let y∉V. If y_i<h and y_j<h for some i≠j, then the point of V with 0 in position k (the third) dominates y.
Otherwise at least two coordinates are ≥h; their sum is ≥2h=K, so they equal h and the third is 0, i.e. y∈V. Contradiction. So V is stable.

### Step 1: structure from internal stability
For distinct x,y∈V, neither dominates the other, so x beats y in ≤1 coordinate and y beats x in ≤1; since sums are equal both counts are exactly 1,
so x,y **agree in exactly one coordinate**; call its index c(x,y), and they differ by ±d in the other two (d≠0).

Triples: for x,y,z∈V, either c(x,y)=c(y,z)=c(x,z) ("collinear": same coordinate c has the same value on all three), or all three c's are distinct ("triangle").
(If c(x,y)=c(y,z)=i then z_i=x_i, and c(x,z)=i, else x,z would agree in a second coordinate position and be equal... precisely: x_i=y_i=z_i so c(x,z)=i because they agree in exactly one coordinate. If c(x,y)=1, c(y,z)=2 then c(x,z)≠1 (else z_1=x_1=y_1 and z_2=y_2 give z=y), and ≠2 similarly, so =3.)

**|V|≥4 implies all points collinear.** If every triple is collinear, all c's coincide. Otherwise some triple x,y,z is a triangle with c(x,y)=1,c(y,z)=2,c(x,z)=3, i.e.
x=(a,b,c), y=(a,b2,c2), z=(a3,b2,c). Fourth point w. Triple (x,y,w): if collinear, c(x,w)=c(y,w)=1; then (y,z,w) must be a triangle, giving c(z,w)=3, and then (x,z,w) has c's (3,1,3), neither collinear nor triangle — impossible. So (x,y,w) is a triangle: {c(x,w),c(y,w)}={2,3}; likewise (x,z,w) gives c(x,w)∈{1,2}, so c(x,w)=2, c(y,w)=3, c(z,w)=1 (by the same reasoning for (y,z,w), it is consistent). Then w=(a3,b,c2). Put b2=b+s, c2=c−s, a3=a−s (from sums for y and z). The sum for w: a3+b+c2=a+b+c−2s=K forces s=0, so y=x, contradiction.

Hence a stable V is either (L) contained in a line {y: y_c=t} (this includes |V|≤2, and V≠∅ since otherwise any point is undominated), or (T) a 3-point triangle.

### Step 2: line type is never stable
V⊂{y_c=t}, with t<K (if |V|=1 choose c with x_c<K; if |V|≥2 then t<K as the line has ≥2 points). Take y with y_c=t+1 (e.g. y_c=t+1 and the rest anything summing to K−t−1). y∉V. For x∈V, x_c=t<y_c; x dominating y would need x_i>y_i, x_j>y_j for the other two indices, but x_i+x_j=K−t > K−t−1 = y_i+y_j only guarantees... precisely x_i≥y_i+1, x_j≥y_j+1 would give x_i+x_j≥y_i+y_j+2=K−t+1, contradiction. So y is undominated: V not stable.

### Step 3: triangle type
Relabel so that V={x,y,z}, x=(a,b,c), y=(a,b+s,c−s), z=(a−s,b+s,c), s≠0 integer (derived from x_1=y_1, y_2=z_2, x_3=z_3 and sums).
In each coordinate i the points take two values L_i<H_i=L_i+|s|, with |s|=:s>0.

*Case s<0 in the above parametrisation ("up"):* each point has exactly one coordinate low: x^i=(L_i at i, H_j,H_k elsewhere), K=ΣL+2s.
Suppose some L_k≥1. Take {i,j}={1,2,3}\{k} and y=(H_i+1 at i, H_j at j, L_k−1 at k) (sum K, nonneg). y∉V (its k-th coordinate is below L_k).
Check no x^m beats y in two coordinates: x^k has H_i,H_j≤y_i,y_j so beats only possibly at k; x^i has L_i<y_i and H_j≤y_j, beats at most at k; x^j likewise. So y is undominated, V not stable.
Thus all L=0, K=2s is even, and V={(s,s,0),(s,0,s),(0,s,s)}: the claimed solution.

*Case s>0 ("down"):* each point has exactly one high coordinate: x^i=L+s·e_i, K=ΣL+s.
Any y=L+e with e≥0, Σe=s is undominated by V (x^k has L_i≤y_i for i≠k, so beats y only in coordinate k at most).
If s≥2 there are C(s+2,2)≥6>3 such y but |V|=3, so some such y∉V is undominated: not stable.
If s=1: K≥2 gives ΣL=K−1≥1, so some L_i≥1; y=L+(−1)e_i+e_j+e_k... i.e. y_i=L_i−1, y_j=L_j+1, y_k=L_k+1 is a valid allocation, not in V,
and each x^m beats y in at most one coordinate (x^i=L+e_i beats only at i; x^j=L+e_j: at i (L_i>L_i−1) only, since at j L_j+1=y_j and at k L_k<y_k; x^k similarly). Undominated: not stable.

### Conclusion
Every stable set is of type (T)-up with L=0, i.e. K=2s and V is the symmetric set. So: stable sets exist iff K is even, and then the unique one is {(K/2,K/2,0),(K/2,0,K/2),(0,K/2,K/2)}. ∎
