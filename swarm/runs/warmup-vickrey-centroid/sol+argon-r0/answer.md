# When the Vickrey-nearest point is the centroid

Write
\[
V=v_A+v_B+v_C,\qquad D=V-v_P>0,\qquad m=\min(v_A,v_B,v_C).
\]
As usual, values are nonnegative. For **strictly positive winner values**, the exact condition is
\[
\boxed{\quad v_A=v_B=v_C\quad\text{or}\quad v_P\le m\quad\text{or}\quad D\le m.\quad}
\]
Equivalently, either the winner values are equal or \(m\ge\min(v_P,V-v_P)\).
If any winner value is zero, the two points always coincide, using the length centroid for a segment and the point itself for a singleton.

When \(v_P\le m\), the common payment is \((v_P/3,v_P/3,v_P/3)\). When \(D\le m\), it is \(p_i=v_i-D/3\). If all winner values are equal, symmetry gives \(p_i=v_P/3\) throughout.

## Proof

**1. Reduce the core to a box section.** The constraint for all three winners gives \(\sum_i p_i\ge v_P\). Conversely, if \(0\le p_i\le v_i\) and \(\sum_i p_i\ge v_P\), then for every subset \(T\),
\[
\sum_{i\in T}p_i
=\sum_i p_i-\sum_{j\notin T}p_j
\ge v_P-\sum_{j\notin T}v_j,
\]
and nonnegativity supplies the other part of the stated core constraint. Since \(0\le v_P<V\), payments totaling \(v_P\) exist inside the box. Thus
\[
R=v_P,\qquad F=\{p:0\le p_i\le v_i,\ \sum_i p_i=v_P\}.
\]
If \(v_P=0\), this is the singleton \(0\), so the condition holds. Henceforth suppose \(v_P>0\) and all winner values are positive.

Set
\[
w_i=\min(v_i,D),\qquad q_i=p_i^{\mathrm{VCG}}=v_i-w_i,
\qquad h=\sum_iw_i-D.
\]
For \(p\in F\), the deficits \(u_i=v_i-p_i\) have sum \(D\), so \(0\le u_i\le w_i\). Consequently the translation \(y=p-q=w-u\) identifies \(F\) with
\[
G=\{y:0\le y_i\le w_i,\ \sum_i y_i=h\}.
\]
Here \(h>0\): if every \(v_i<D\), then \(h=V-D=v_P>0\); otherwise one \(w_i=D\) and the other two are positive. Also \(h<\sum_iw_i\), so \(G\) has positive area and its centroid lies strictly between every pair of coordinate bounds.

The Vickrey-nearest point minimizes \(\|y\|^2\) on \(G\). If it equals the centroid, it is in the relative interior of \(G\); the first-order condition in the plane \(\sum_i y_i=h\) therefore forces
\[
y=(h/3,h/3,h/3).
\]
Conversely, if this is the centroid, it is feasible and is the unique minimum-norm point in that plane. It remains to determine when the centroid of \(G\) is this equal-coordinate point.

**2. Compute the centroid by removing corner triangles.** Start with the triangle
\[
\Delta=\{y_i\ge0:\ \sum_i y_i=h\},
\]
whose centroid is \(c_0=(h/3,h/3,h/3)\). To obtain \(G\), remove the corner triangle \(y_i>w_i\) for each \(w_i<h\). These removed triangles have disjoint interiors, because
\[
w_i+w_j=\sum_k w_k-w_k=h+D-w_k\ge h.
\]
Put \(t_i=(h-w_i)_+\). The removed triangle at corner \(i\) has area proportional to \(t_i^2\), and, when nonempty, centroid
\[
r_i=\frac{t_i}{3}(1,1,1)+w_i e_i
=c_0+w_i\left(e_i-\frac13(1,1,1)\right).
\]
Subtracting its first moment from that of \(\Delta\) shows that the centroid of \(G\) equals \(c_0\) exactly when
\[
\boxed{\quad w_A(h-w_A)_+^2=w_B(h-w_B)_+^2=w_C(h-w_C)_+^2.\quad} \tag{*}
\]

If their common value is zero, positivity of the \(w_i\) implies \(w_i\ge h\) for every \(i\). Equivalently, every pair satisfies \(w_i+w_j\le D\).

If the common value is positive, all \(w_i\) lie in \((0,h)\). The function \(f(x)=x(h-x)^2\) increases on \((0,h/3)\) and decreases on \((h/3,h)\), so equal function values permit at most two distinct coordinate values. Suppose there are two, \(x<z\). From \(f(x)=f(z)\), taking positive square roots and factoring gives
\[
h=x+z+\sqrt{xz}.
\]
But the three coordinates are either \((x,x,z)\) or \((x,z,z)\), up to permutation. Since \(h=\sum_iw_i-D\), these cases respectively imply
\[
x-D=\sqrt{xz}\qquad\text{or}\qquad z-D=\sqrt{xz},
\]
contradicting \(x,z\le D\). Thus all three \(w_i\) must be equal. Conversely, equal \(w_i\) satisfy \((*)\) by symmetry.

We have proved that equality of the two points is equivalent to
\[
\text{all }w_i\text{ equal}\qquad\text{or}\qquad w_i+w_j\le D\text{ for every pair}.
\]
The first alternative means either all \(v_i\) are equal or every \(v_i\ge D\). For the second, positivity excludes any \(w_i=D\), so \(w_i=v_i\); the pair inequalities become
\[
V-v_k\le D=V-v_P\quad\text{for every }k,
\]
which is exactly \(v_P\le m\). Conversely, \(v_P\le m\) implies these pair inequalities. This proves the stated condition.

**3. Zero winner values.** If only one winner has positive value, \(F\) is a singleton. If exactly two have positive values, the same translation gives \(y_3=0\) and
\[
y_1+y_2=h=w_1+w_2-D,\qquad 0\le h\le\min(w_1,w_2),
\]
since \(w_i\le D\). Thus \(G\) is the segment from \((h,0,0)\) to \((0,h,0)\). Its midpoint \((h/2,h/2,0)\) is also its unique minimum-norm point. This proves the remaining cases.

## Worked example where the points differ

Take
\[
(v_A,v_B,v_C)=(1,2,3),\qquad v_P=3.
\]
Then \(V=6\), \(D=3\), and \(q=p^{\mathrm{VCG}}=(0,0,0)\). The minimum-revenue face is
\[
F=\{(p_A,p_B,3-p_A-p_B):0\le p_A\le1,\ 0\le p_B\le2\}.
\]
It is a parallelogram with vertices
\[
(0,0,3),\ (1,0,2),\ (1,2,0),\ (0,2,1).
\]
Its area centroid is therefore
\[
\boxed{c_F=(1/2,1,3/2).}
\]
Every point in the plane \(\sum_i p_i=3\) satisfies \(\sum_i p_i^2\ge3\), with equality only at \((1,1,1)\). This point respects all value caps, so
\[
\boxed{p^{\mathrm{VN}}=(1,1,1)\ne c_F.}
\]
Here the winner values are unequal and \(m=1<\min(v_P,D)=3\), as the condition predicts.
