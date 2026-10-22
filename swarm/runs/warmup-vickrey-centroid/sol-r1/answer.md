# When the Vickrey-nearest point is the centroid

Write
\[
S=v_A+v_B+v_C,\qquad m=\min(v_A,v_B,v_C),\qquad D=S-v_P>0.
\]
As usual, assume valuations are nonnegative. For a lower-dimensional face, use its centroid with respect to length, or the point itself if it is a singleton.

**Exact condition.** The Vickrey-nearest point equals the centroid of the minimum-revenue face if and only if
\[
\boxed{\quad
m=0
\quad\text{or}\quad
v_P\le m
\quad\text{or}\quad
v_P\ge S-m
\quad\text{or}\quad
v_A=v_B=v_C.
\quad}
\]
In particular, with strictly positive winner values, equality occurs precisely when the package value is at most the smallest winner value, is at least the sum of the two largest winner values, or all three winner values are equal. The boundary inequalities are inclusive.

## Proof

### 1. The minimum-revenue face

The core constraints are equivalent to
\[
0\le p_i\le v_i,\qquad \sum_i p_i\ge v_P.
\]
Indeed, the total constraint is one of the stated coalition constraints. Conversely, for every subset \(T\), these inequalities imply
\[
\sum_{i\in T}p_i
\ge v_P-\sum_{j\notin T}p_j
\ge v_P-\sum_{j\notin T}v_j,
\]
and the left side is also nonnegative.

Since \(v_P<S\), total payment \(v_P\) is feasible (for example, take \(p_i=v_Pv_i/S\)). Thus
\[
R=v_P,\qquad
F=\{p:0\le p_i\le v_i,\ \sum_i p_i=v_P\}.
\]
If \(v_P=0\), this is the singleton \(\{0\}\), and the claimed condition holds. For now suppose \(v_P>0\) and every \(v_i>0\).

Use normalized surplus coordinates
\[
x_i=\frac{v_i-p_i}{D},\qquad
u_i=\min\left(\frac{v_i}{D},1\right).
\]
The face becomes
\[
K(u)=\{x:x_i\ge0,\ x_i\le u_i,\ \sum_i x_i=1\}.
\]
Replacing the original upper bounds \(v_i/D\) by \(u_i\) changes nothing, because nonnegative coordinates summing to one are already at most one. We have \(u_i>0\) and \(\sum_i u_i>1\), so this polygon has positive area.

The VCG surplus vector in these coordinates is exactly \(u\):
\[
\frac{v_i-p_i^{\rm VCG}}D
=\frac{v_i-\max(0,v_i-D)}D=u_i.
\]
The coordinate change is a translation, reflection, and uniform scaling. It therefore preserves centroids and nearest points. Our question becomes: **when is the centroid \(g\) of \(K(u)\) the Euclidean projection of \(u\) onto \(K(u)\)?**

The centroid is in the relative interior of the polygon, so all its coordinate bounds are strict. Consequently it is the nearest point exactly when \(u-g\) is perpendicular to the plane \(\sum_i x_i=1\), or equivalently
\[
u_1-g_1=u_2-g_2=u_3-g_3. \tag{1}
\]
Necessity follows by differentiating squared distance along the plane at an interior minimizer. Sufficiency follows because (1) makes \(g\) the orthogonal projection onto the whole plane, and \(g\) is feasible.

### 2. A capped-simplex centroid calculation

We show that, for positive caps \(u_i\le1\) with sum greater than one, condition (1) holds exactly when
\[
\text{all three caps are equal, or the two largest caps sum to at most one.} \tag{2}
\]

Here are the area and moment formulas needed for this claim. Put \(h_T=(1-\sum_{i\in T}u_i)_+\), where \(z_+=\max(z,0)\), and define
\[
Z=\sum_{T\subseteq\{1,2,3\}}(-1)^{|T|}h_T^2>0.
\]
Inclusion-exclusion applied to the triangle \(x_i\ge0,\ \sum_i x_i=1\) gives
\[
Zg_i=
\sum_T(-1)^{|T|}
\left(\frac{h_T^3}{3}
+\mathbf 1_{\{i\in T\}}u_i h_T^2\right). \tag{3}
\]
To see this geometrically, the region violating every bound indexed by \(T\) is a translated triangle of area proportional to \(h_T^2\). Its centroid has coordinate \(h_T/3+\mathbf 1_{\{i\in T\}}u_i\). All area factors are the same and cancel in (3).

Compare two caps \(a\le b\), and call the remaining cap \(c\). Write \(g_a,g_b\) for their centroid coordinates, set \(d_a=a-g_a\), \(d_b=b-g_b\), and put \(r=1-c\). Subtracting the two moment formulas gives
\[
Z(d_b-d_a)
=(b-a)(ab-r^2)+b(r-a)_+^2-a(r-b)_+^2.
\]
Equivalently,
\[
Z(d_b-d_a)=
\begin{cases}
0,&r\ge b,\\[2pt]
a(b-r)^2,&a\le r\le b,\\[2pt]
(b-a)(ab-r^2),&r\le a.
\end{cases} \tag{4}
\]
In particular, if \(a<b\), positivity of \(a\) shows that
\[
d_a=d_b\quad\Longleftrightarrow\quad b+c\le1. \tag{5}
\]
Equal caps always have equal deficits by symmetry.

Now order the caps \(a\le b\le c\). If \(a<b\), equality of all deficits forces \(b+c\le1\) by (5). If \(a=b<c\), compare \(a\) and \(c\), with remaining cap \(b\), to obtain the same requirement. This proves necessity of (2), unless all caps are equal. Conversely, when \(b+c\le1\), every pair satisfies (5), or has equal caps, so all deficits are equal. Equal caps also give equal deficits by symmetry. This proves (2).

### 3. Translating the condition back to values

First, all the caps \(u_i=\min(v_i/D,1)\) are equal exactly when either all winner values are equal or every winner value is at least \(D\). The latter is
\[
D\le m\quad\Longleftrightarrow\quad v_P\ge S-m.
\]

Second, the two largest caps sum to at most one exactly when \(v_P\le m\). Indeed, since every cap is positive, such a sum precludes any cap from being one. Thus there is no truncation, and the sum of the two largest caps is \((S-m)/D\). Hence
\[
\frac{S-m}{D}\le1
\quad\Longleftrightarrow\quad v_P\le m.
\]
Conversely, \(v_P\le m\) implies \(D\ge S-m\), which is at least every winner value, and the same calculation applies. This proves the classification for positive winner values.

Finally, suppose a winner value is zero. Its payment is fixed at zero. Denote the other two values by \(w_1,w_2\), and their VCG payments by
\[
\ell_1=(v_P-w_2)_+,\qquad \ell_2=(v_P-w_1)_+.
\]
The face is the segment with endpoints
\[
(\ell_1,v_P-\ell_1),\qquad(v_P-\ell_2,\ell_2).
\]
The orthogonal projection of \((\ell_1,\ell_2)\) onto the total-payment line is
\[
\left(\frac{v_P+\ell_1-\ell_2}{2},
      \frac{v_P-\ell_1+\ell_2}{2}\right),
\]
which is exactly the segment's midpoint and is feasible. This also covers a singleton when another value is zero. Therefore equality always holds when \(m=0\), completing the proof.

## Worked counterexample: no cap binds at the nearest point

Take
\[
(v_P,v_A,v_B,v_C)=(2,1,2,2).
\]
Then \(S=5>2\), all VCG payments are zero, and
\[
F=\{p\ge0:p_A+p_B+p_C=2,\ p_A\le1\}.
\]
(The other two value caps are automatic.) The point on the total-payment plane nearest the origin is feasible, so
\[
\boxed{p^{\rm VN}=(2/3,2/3,2/3).}
\]
All three value caps are strict at this point.

To compute the centroid, start with the full payment triangle of total two. Its centroid is \((2/3,2/3,2/3)\). Remove the triangle where \(p_A>1\), whose centroid is \((4/3,1/3,1/3)\). The removed triangle has one quarter of the full triangle's area. Subtracting its first moment gives
\[
\operatorname{centroid}(F)
=\frac{4(2/3,2/3,2/3)-(4/3,1/3,1/3)}{3}
=\boxed{(4/9,7/9,7/9).}
\]
Thus the two points differ, even though no cap binds at the Vickrey-nearest point. This agrees with the condition: \(m=1\), \(S-m=4\), and \(1<v_P=2<4\), while the winner values are unequal.
