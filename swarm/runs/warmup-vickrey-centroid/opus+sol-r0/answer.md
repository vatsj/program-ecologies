# When the Vickrey-nearest point is the centroid

Write \(P=v_P\), and sort the three winner values as \(a\le b\le c\). Assume nonnegative values and \(P<a+b+c\), as in the question. The centroid means the uniform area centroid of the face, or the uniform length centroid when it is a segment.

The exact condition is
\[
\boxed{\quad a=0\quad\text{or}\quad P\le a\quad\text{or}\quad P\ge b+c\quad\text{or}\quad a=b=c.\quad}
\]
Thus, when all winner values are positive, equality holds exactly when the package value is at most the smallest winner value, at least the sum of the two largest winner values, or all three winner values are equal. Endpoints are included.

## Reduction to a capped triangle

Let \(V=v_A+v_B+v_C\). The stated core constraints are equivalent to
\[
0\le p_i\le v_i,\qquad \sum_i p_i\ge P.
\]
Indeed, the full-set constraint gives the revenue inequality, and that inequality together with the caps gives every other subset constraint:
\[
\sum_{i\in T}p_i\ge P-\sum_{j\notin T}p_j
\ge P-\sum_{j\notin T}v_j.
\]
Nonnegativity supplies the other part of the maximum. Since \(0\le P<V\), a capped payment vector with total \(P\) exists, for example \(p_i=Pv_i/V\). Consequently \(R=P\), and
\[
F=\{p:0\le p_i\le v_i,\ \sum_i p_i=P\}.
\]
If \(P=0\), this is a point and the claimed equality is immediate. Henceforth suppose \(P>0\).

Put
\[
D=V-P>0,\qquad w_i=\min(v_i,D),\qquad
\ell_i=v_i-w_i=\max(0,v_i-D)=p_i^{\rm VCG}.
\]
Every point of \(F\) satisfies \(p_i\ge P-\sum_{j\ne i}v_j\), hence \(p_i\ge\ell_i\). Translating by VCG, write \(p=\ell+y\). The translated face is exactly
\[
K=\{y:0\le y_i\le w_i,\ \sum_i y_i=H\},
\qquad H=P-\sum_i\ell_i=\sum_i w_i-D.
\]
The Vickrey-nearest point corresponds to the point of \(K\) minimizing \(\sum_i y_i^2\). Translation also preserves centroids.

## A centroid observation

For positive caps \(w_1,w_2,w_3\) and \(0<H<\sum_iw_i\), the polygon \(K\) has nonempty relative interior. Its centroid \(m\) is in that interior. If \(m\) minimizes squared distance to the origin, stationarity along its plane gives
\[
m_1=m_2=m_3=H/3.
\]
Conversely, if the centroid is \((H/3,H/3,H/3)\), it minimizes squared distance, since every point in the plane has squared norm at least \(H^2/3\). Thus the two points coincide precisely when the centroid has equal coordinates.

We claim that the centroid has equal coordinates exactly when
\[
\boxed{\quad w_1=w_2=w_3\quad\text{or}\quad \min_i w_i\ge H.\quad} \tag{*}
\]
Both conditions suffice: in the first case permutation symmetry forces equal centroid coordinates; in the second, the upper bounds do not cut the triangle \(y_i\ge0,\sum_i y_i=H\).

For necessity, suppose \(w_i<w_j\) and \(w_i<H\). Swap coordinates \(i,j\). On the part of \(K\) that is invariant under this swap, the integral of \(y_j-y_i\) vanishes. Every point remaining in \(K\) has
\[
y_j>w_i\ge y_i,
\]
so contributes positively. This remaining region has positive area: writing \(k\) for the third coordinate, choose
\[
\max(w_i,H-w_i-w_k)<y_j<\min(w_j,H),
\]
then choose \(0<y_i<w_i\) and \(0<y_k<w_k\) summing to \(H-y_j\). The interval is nonempty because \(w_i<w_j\), \(w_i<H\), and \(H<\sum w\). Therefore \(m_j>m_i\). Unless all caps are equal or the smallest cap is at least \(H\), such a pair exists. This proves (*).

## Translate the condition back to values

First suppose \(a>0\). For \(P>0\), all \(w_i>0\) and \(0<H<\sum_iw_i\), so (*) applies.

The caps are all equal exactly when either all winner values are equal or \(D\le a\). The latter is equivalent to \(P\ge b+c\).

The other alternative in (*) is
\[
\min(b,D)+\min(c,D)\le D.
\]
Because \(b>0\), this forces \(c<D\); it then becomes \(b+c\le D=a+b+c-P\), equivalently \(P\le a\). Conversely \(P\le a\) implies this inequality. These are exactly the three alternatives stated for positive winner values.

If \(a=0\), its payment is fixed at zero. If two winner values remain positive, call their caps \(w_1,w_2\). Then
\[
H=w_1+w_2-D\le\min(w_1,w_2),
\]
since each cap is at most \(D\). Thus the translated face is the entire segment \(y_1+y_2=H\), \(y_1,y_2\ge0\), whose midpoint \((H/2,H/2)\) is also nearest to the origin. With fewer positive winner values the face is a point. Equality therefore always holds when \(a=0\).

## Worked counterexample

Take
\[
(v_A,v_B,v_C)=(1,2,3),\qquad P=3.
\]
The total winner value is \(6>3\), and VCG is \((0,0,0)\). The minimum-revenue face is
\[
p_A\in[0,1],\qquad p_B\in[0,2],\qquad p_C=3-p_A-p_B.
\]
This is a parallelogram with vertices
\[
(0,0,3),\quad(1,0,2),\quad(0,2,1),\quad(1,2,0).
\]
Its area centroid is its center,
\[
\boxed{p^{\rm centroid}=(1/2,1,3/2).}
\]
Among all vectors with total \(3\), squared distance to VCG is minimized by \((1,1,1)\), which lies in the face. Hence
\[
\boxed{p^{\rm VN}=(1,1,1)\ne p^{\rm centroid}.}
\]
Indeed, none of the equality conditions holds: \(a=1>0\), \(P=3>a\), \(P=3<b+c=5\), and the winner values differ.
