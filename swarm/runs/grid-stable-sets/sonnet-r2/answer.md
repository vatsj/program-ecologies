# Answer

1. A stable set exists **iff K is even**.
2. For K = 2m the stable set is **unique**: V0 = {(m,m,0), (m,0,m), (0,m,m)}. For odd K there is none.
   (In particular there are no "discriminatory" stable sets on the grid.)

Brute-force enumeration (`enum.py`, K=2..12) agrees: exactly one stable set for even K, none for odd K.

Notation: x dom y iff x beats y in at least two coordinates.

## Existence for K = 2m (V0 is stable)
*Internal.* For two distinct elements of V0, e.g. (m,m,0) and (m,0,m), the first beats the second only in coordinate 2 (coordinate 1 is equal), so there is no domination.
*External.* Let y=(a,b,c) ∉ V0. (m,m,0) dominates y iff a<m and b<m; likewise (m,0,m) iff a<m and c<m, and (0,m,m) iff b<m and c<m. Suppose none dominates y. Then at most one of a,b,c is < m. So at least two are ≥ m. They sum to at most 2m, so they equal m and the third is 0. Then y ∈ V0, a contradiction.

## Uniqueness and non-existence
Let V be stable. V is nonempty, since otherwise nothing is dominated.

**Step 1 (internal stability).** Take distinct x,y∈V and let d=x−y, so d≠0 and Σd=0. Neither dominates the other, so d has at most one positive and at most one negative coordinate. Hence d has exactly one positive, one negative and one zero coordinate. So **any two distinct elements of V agree in exactly one coordinate.**

**Step 2 (structure).** Take three points x,y,z∈V. Let c(·,·) denote the unique coordinate in which a pair agrees.
- If c(x,y)=c(x,z), then y and z agree in that coordinate too, so all three share that coordinate value ("line triple").
- Otherwise c(y,z) cannot equal c(x,y). If it did, x and z would also agree in that coordinate, contradicting c(x,z)≠c(x,y). Likewise c(y,z)≠c(x,z). So the three coordinates are all distinct ("triangle"). Then x=(p,q,·), y=(p,·,r), z=(·,q,r) with x₁=y₁=p, x₂=z₂=q, y₃=z₃=r.

*A triangle admits no fourth point.* Write x=(p,q,x₃), y=(p,y₂,r), z=(z₁,q,r) with z₁≠p, y₂≠q, x₃≠r. Let w=(u,v,t) be a fourth point.
- If u=p, then w agrees with x and with y in coordinate 1, so it may not agree with them elsewhere. Also w agrees with z in none of coordinates 1, 2, 3 (u=p≠z₁, v≠q, t≠r), contradicting Step 1.
- If v=q, the same argument applies to y.
- If t=r, the same argument applies to x.
- If none of u=p, v=q, t=r holds, then w agrees with x in no coordinate.

So either |V|=3 and V is a triangle, or no three points of V form a triangle. In the second case all triples are line triples. For |V|≥3 the common coordinate is determined by any pair, so all of V lies on one line {x_i=c}. For |V|≤2 this holds trivially.

**Step 3 (no stable V lies on a line {x_i=c}).** By symmetry take i=1. If c=K the line is {(K,0,0)}, and y=(0,K,0) is not dominated by (K,0,0) and not in V. If c<K, let y=(c+1,0,K−c−1), which is not in V. A point x of the line has x₁=c<y₁. To dominate y, x would need x₂>y₂ and x₃>y₃, so x₂+x₃ ≥ y₂+y₃+2 = K−c+1. But x₂+x₃=K−c. So y is undominated, contradicting external stability.

**Step 4 (triangles).** Let V={x,y,z} be a triangle. Put s=p+q+r−K. Then x₃=K−p−q=r−s, y₂=q−s, z₁=p−s. So
x=(p,q,r−s), y=(p,q−s,r), z=(p−s,q,r), with s≠0 because the points are distinct.

*Case s<0.* Put t=−s>0. Then p+q+r=K−t and x=(p,q,r+t), y=(p,q+t,r), z=(p+t,q,r). Let u=(p+a,q+b,r+c) with a,b,c≥0 and a+b+c=t. Then x can beat u only in coordinate 3 (x₁=p≤u₁, x₂=q≤u₂), and similarly y and z each beat u in at most one coordinate. So every such u is undominated by V.
- If t≥2, there are C(t+2,2)≥6>3 such u, so some u∉V is undominated.
- If t=1, then K=p+q+r+1≥2, so some coordinate of (p,q,r) is positive. By symmetry say r≥1. Let u=(p+1,q+1,r−1). It is not in V. x, y and z each beat u only in coordinate 3, so u is undominated. Either way external stability fails.

*Case s>0.* Nonnegativity of the points gives p,q,r≥s. Suppose p>s. Take u=(0,q+a,r+b) with a,b≥0 and a+b=p−s>0. Then Σu=q+r+p−s=K. Each of x,y,z has first coordinate p or p−s, which is >0, and second and third coordinates ≤ those of u. So each beats u only in coordinate 1, and u is undominated. u∉V because all three points of V have first coordinate >0. This contradicts external stability. By symmetry q>s and r>s are also impossible, so p=q=r=s. Then K=p+q+r−s=2s is even, and V={(s,s,0),(s,0,s),(0,s,s)}=V0 with s=K/2.

**Conclusion.** Every stable set is V0, which requires K even. For odd K no stable set exists, and for even K=2m the unique stable set is {(m,m,0),(m,0,m),(0,m,m)}. ∎

(Code: `enum.py` is the exhaustive search, and `tri.py`/`tri2.py` explore triangles.)
