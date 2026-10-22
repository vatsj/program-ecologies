# When the Vickrey-nearest point is the centroid

Write
\[
r=v_P,\qquad V=v_A+v_B+v_C,\qquad d=V-r>0,
\qquad m=\min(v_A,v_B,v_C).
\]
For nonnegative valuations, the exact condition is
\[
\boxed{\quad
\#\{i\in\{A,B,C\}:v_i>0\}\le2
\quad\text{or}\quad r\le m
\quad\text{or}\quad d\le m
\quad\text{or}\quad v_A=v_B=v_C.
\quad}
\]
In particular, when all three winner values are positive, the first alternative disappears. The centroid means uniform Euclidean area on a two-dimensional face, uniform length on a segment, and the point itself on a singleton.

## Proof

### 1. The minimum-revenue face

The core is precisely
\[
0\le p_i\le v_i,\qquad \sum_i p_i\ge r.
\]
Indeed, the stated core constraints include these inequalities; conversely, for every subset \(T\),
\[
\sum_{i\in T}p_i
=\sum_i p_i-\sum_{j\notin T}p_j
\ge r-\sum_{j\notin T}v_j,
\]
and payments are nonnegative. Because \(0\le r<V\), the box contains a point with total \(r\), so \(R=r\) and
\[
F=\{p:0\le p_i\le v_i,\ \sum_i p_i=r\}.
\]

Let
\[
\ell_i=(v_i-d)_+=p_i^{\mathrm{VCG}},\qquad
u_i=v_i-\ell_i=\min(v_i,d),\qquad
s=r-\sum_i\ell_i=\sum_i u_i-d.
\]
On \(F\), the other payment caps imply \(p_i\ge\ell_i\). Thus translating by \(\ell\) gives exactly
\[
K=F-\ell=\{y:0\le y_i\le u_i,\ \sum_i y_i=s\}.
\]
Translation preserves centroids and distances. The Vickrey-nearest point therefore corresponds to the point of \(K\) nearest the origin.

### 2. A capped-simplex observation

Suppose \(u_i>0\) for all three coordinates and \(0<s<\sum_i u_i\). Then \(K\) has positive area: \(y_i=s u_i/\sum_j u_j\) satisfies every box inequality strictly. Consequently its centroid \(c\) satisfies
\[
0<c_i<u_i\qquad\text{for every }i.
\]
The point of \(K\) nearest the origin has the form
\[
y_i^*=\min(u_i,t),\qquad \sum_i\min(u_i,t)=s.
\]
This follows directly by minimizing \(\sum_i y_i^2\) with a fixed sum: all coordinates below their caps must be equal. Consequently, if \(y^*=c\), no cap can bind, and every coordinate of \(c\) equals \(s/3\).

We next characterize when the centroid has equal coordinates. If
\[
u_i<u_j\quad\text{and}\quad u_i<s,
\]
then
\[
c_i<c_j. \tag{*}
\]
To prove this, interchange coordinates \(i,j\) by the area-preserving reflection \(\sigma\). The overlap \(K\cap\sigma K\) is invariant under this reflection, so the integral of \(y_j-y_i\) over that overlap vanishes. On the remainder,
\[
K\setminus\sigma K=\{y\in K:y_j>u_i\},
\]
and \(y_j-y_i>0\). This remainder has positive area: the largest possible \(y_j\) is \(\min(u_j,s)>u_i\), and the slice has a relative interior. Hence its integral is strictly positive, proving (*).

It follows that
\[
c_1=c_2=c_3
\quad\Longleftrightarrow\quad
u_1=u_2=u_3\ \text{ or }\ \min_i u_i\ge s.
\]
For necessity, if the smallest cap is below \(s\) and some cap is larger, use (*). For sufficiency, equal caps give permutation symmetry; when every cap is at least \(s\), \(K\) is the ordinary simplex \(y_i\ge0,\sum_i y_i=s\). In either case the centroid and nearest point are both \((s/3,s/3,s/3)\). Thus
\[
\boxed{y^*=c\ \Longleftrightarrow\ u_1=u_2=u_3\ \text{ or }\ \min_i u_i\ge s.} \tag{1}
\]

### 3. Translate (1) back to the values

Assume all winner values and \(r\) are positive. Then all \(u_i>0\) and \(0<s<\sum_i u_i\), so (1) applies.

Since \(u_i=\min(v_i,d)\), all three \(u_i\) are equal exactly when either all three values are equal or all three values are at least \(d\).

Also, \(\min_i u_i\ge s\) is equivalent to \(r\le m\). To see necessity, if some \(u_k=d\), then
\[
s=\sum_{i\ne k}u_i>\min_i u_i,
\]
using positivity of the other two coordinates. Thus every \(u_i<d\), which means \(u_i=v_i\), \(\ell_i=0\), and \(s=r\). Conversely, if \(r\le m\), then for each \(i\), the other two values sum to at least \(2r>r\), so \(v_i<d\); hence \(u_i=v_i\), \(s=r\), and \(\min_i u_i\ge s\).

This proves the stated condition for positive values. If \(r=0\), the face is the singleton \(0\), and the alternative \(r\le m\) already applies.

If exactly two winner values are positive, discard the zero coordinate. Since \(u_i\le d\),
\[
s=u_1+u_2-d\le\min(u_1,u_2).
\]
The translated face is therefore the full segment \(y_1+y_2=s\), \(y_i\ge0\), whose midpoint \((s/2,s/2)\) is nearest the origin. With just one positive winner value, the face is a singleton. This proves the remaining alternative.

In the three positive-value equality cases, the common point is \((r/3,r/3,r/3)\) when \(r\le m\) or all values are equal, and is \((v_i-d/3)_i\) when \(d\le m\).

## Worked counterexample, with no cap binding at the nearest point

Take
\[
(v_P,v_A,v_B,v_C)=(2,1,2,2).
\]
Here \(V=5>2\), \(d=3\), and \(p^{\mathrm{VCG}}=(0,0,0)\). The face is
\[
F=\{p\ge0:p_A+p_B+p_C=2,\ p_A\le1\},
\]
since the other two caps are automatic. The equal-coordinate point is feasible, so the Vickrey-nearest point is
\[
p^{\mathrm{VN}}=(2/3,2/3,2/3).
\]
All three value caps are strict at this point.

Parametrize \(F\) by
\[
p=(x,y,2-x-y),\qquad 0\le x\le1,\quad 0\le y\le2-x.
\]
The surface-area factor is the constant \(\sqrt3\), so it cancels in centroid ratios. Hence
\[
\bar p_A=
\frac{\int_0^1 x(2-x)\,dx}{\int_0^1(2-x)\,dx}
=\frac{2/3}{3/2}=\frac49.
\]
Symmetry between \(B,C\) and the fixed total give
\[
\boxed{\bar p=(4/9,7/9,7/9)\ne(2/3,2/3,2/3)=p^{\mathrm{VN}}.}
\]

## Verification

One independent check built the face directly from all seven core constraints, verified the minimum revenue, and used exact rational arithmetic to compute polygon centroids and nearest points in 20,000 random instances. A second check used floating-point polygon triangulation and water-filling in all 2,052 instances with integer winner values in 1..6 and integer v_P in 1..V−1. Both checks matched the boxed condition throughout.
