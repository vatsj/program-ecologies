# Stable sets on the integer grid

For every integer \(K\geq2\), a stable set exists **if and only if \(K\) is even**. If \(K=2m\), the **unique** stable set is
\[
V_m=\{(m,m,0),(m,0,m),(0,m,m)\}.
\]
In particular, there are no discriminatory stable sets on this grid.

## 1. Structure of internally stable sets

Two distinct allocations are mutually undominating if and only if they share a coordinate (with the same player index). Indeed, if they share a coordinate, their other two coordinates move in opposite directions because their sums agree, so neither allocation improves two coordinates. If they share no coordinate, all three coordinate differences are nonzero; at least two have the same sign, giving dominance in one direction.

We claim that every internally stable set either has a coordinate common to all its members, or consists of exactly three allocations of one of these forms:
\[
\begin{aligned}
U(a,b,c;d)&=\{(a+d,b,c),(a,b+d,c),(a,b,c+d)\},
&&a+b+c+d=K,\\
D(a,b,c;d)&=\{(a,b+d,c+d),(a+d,b,c+d),(a+d,b+d,c)\},
&&a+b+c+2d=K,
\end{aligned}
\]
where \(a,b,c\) are nonnegative integers and \(d\) is a positive integer.

Here is a proof of the claim. Sets of at most two allocations have a common coordinate, so consider two distinct members of a larger set. After permuting coordinates and interchanging these two members if necessary, write them as
\[
x=(r,s,t+d),\qquad y=(r,s+d,t),\qquad d>0.
\]
If every member has first coordinate \(r\), we have the first alternative. Otherwise take a member \(z\) whose first coordinate differs from \(r\). It must share a coordinate with each of \(x,y\). These shared coordinates must be the second and third coordinates, in opposite orders. The sum condition then leaves precisely two possibilities:
\[
z_+=(r+d,s,t),\qquad z_-=(r-d,s+d,t+d).
\]
The latter is available only if \(r\geq d\). The two possibilities cannot both belong to an internally stable set, since \(z_-\) dominates \(z_+\).

Any further member whose first coordinate differs from \(r\) must again be one of these two possibilities, hence must equal the chosen \(z\). A member whose first coordinate equals \(r\) must share its second or third coordinate with \(z\); the sum condition then forces it to equal \(x\) or \(y\). Thus the set consists of exactly \(x,y,z\). With \(z=z_+\), it is \(U(r,s,t;d)\); with \(z=z_-\), it is \(D(r-d,s,t;d)\). This proves the claim.

## 2. No stable set has a common coordinate

Suppose a stable set \(V\) is contained in the coordinate line
\[
L=\{(h,u,K-h-u):0\leq u\leq K-h\}.
\]
No member of \(L\) dominates any other member of \(L\). External stability therefore forces \(V=L\).

If \(h<K\), consider the allocation
\[
y=(h+1,K-h-1,0).
\]
It is outside \(L\). For a member of \(L\) to dominate \(y\), it would have to increase both the second and third coordinates, since its first coordinate is smaller. Because shares are integers, its last two coordinates would then sum to at least
\[
(K-h-1)+0+2=K-h+1,
\]
whereas their sum is \(K-h\). Thus \(y\) is undominated, a contradiction.

If \(h=K\), the line consists solely of \((K,0,0)\), which dominates no allocation at all and so cannot be externally stable. The argument applies to any choice of the common coordinate. Consequently every stable set must be one of the triples in Section 1.

## 3. Eliminate all upper triples

Consider \(U(a,b,c;d)\). Every allocation with coordinates at least \((a,b,c)\) is undominated by this triple: each member of the triple can exceed such an allocation in at most its one boosted coordinate.

If \(d\geq2\), the allocation
\[
(a+d-1,b+1,c)
\]
has those coordinate bounds, has sum \(K\), and is not a member of the triple. Hence external stability fails.

If \(d=1\), then \(a+b+c=K-1\geq1\). After permuting coordinates, assume \(a\geq1\). The allocation
\[
y=(a-1,b+1,c+1)
\]
is outside the triple and is undominated: every member of the triple has second coordinate at most \(y_2\) and third coordinate at most \(y_3\), so can improve at most the first coordinate. This also contradicts external stability. No upper triple is stable.

## 4. Eliminate lower triples with a positive base coordinate

Consider \(D(a,b,c;d)\). If a base coordinate is positive, permute coordinates so that \(a\geq1\). Then
\[
y=(a-1,b+d+1,c+d)
\]
is a valid allocation of \(K=a+b+c+2d\), and is outside the triple because its first coordinate is below every member's first coordinate. Every member has second coordinate strictly below \(y_2\) and third coordinate at most \(y_3\), so none dominates \(y\).

Thus external stability forces \(a=b=c=0\). The only remaining possibility is
\[
K=2d,\qquad D(0,0,0;d)=\{(0,d,d),(d,0,d),(d,d,0)\}.
\]
This proves both nonexistence for odd \(K\) and uniqueness for even \(K\), subject only to verifying the remaining candidate.

## 5. Verify the surviving set

Let \(K=2m\). Any two members of \(V_m\) share a coordinate, so \(V_m\) is internally stable.

Take any allocation \(y\notin V_m\). At least two coordinates of \(y\) are strictly less than \(m\): otherwise two coordinates would be at least \(m\), and their sum together with the nonnegative third coordinate could equal \(2m\) only if those two coordinates were exactly \(m\) and the third were zero, placing \(y\) in \(V_m\). Choose two coordinates below \(m\). The member of \(V_m\) that gives \(m\) to those two players strictly improves both their shares, hence dominates \(y\). Therefore \(V_m\) is externally stable as well.

The stated classification follows for every \(K\geq2\).
