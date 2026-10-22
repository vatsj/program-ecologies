# When the Vickrey-nearest point is the centroid

Write \(V=v_A+v_B+v_C\), \(q=v_P\), and \(m=\min(v_A,v_B,v_C)\). Values are taken to be nonnegative, and \(V>q\) as in the question. The centroid means the uniform **area centroid** of a polygon, or the uniform length centroid of a segment.

If all three singleton values are positive, the exact condition is

\[
\boxed{\quad p^{\mathrm{VN}}=\operatorname{centroid}(F)
\iff q\le m\quad\text{or}\quad q\ge V-m\quad\text{or}\quad v_A=v_B=v_C.\quad}
\]

The weak inequalities include their boundary cases. If any singleton value is zero, the two points always coincide: the face is a segment or a point.

For positive singleton values, the common point is \((q/3,q/3,q/3)\) in the first or third alternative; in the second alternative it is \(p_i=v_i-(V-q)/3\).

## Proof

**1. The minimum-revenue face.** The core is exactly
\[
0\le p_i\le v_i,\qquad \sum_i p_i\ge q.
\]
Indeed, the full-winner coalition requires the total-payment inequality. Conversely, for every subset \(T\), these inequalities imply
\[
\sum_{i\in T}p_i
=\sum_i p_i-\sum_{j\notin T}p_j
\ge q-\sum_{j\notin T}v_j,
\]
while nonnegativity supplies the other part of the stated subset constraint. Since \(0\le q<V\), payments totaling \(q\) are feasible. Hence
\[
R=q,\qquad F=\{p:0\le p_i\le v_i,\ \sum_i p_i=q\}.
\]
If \(q=0\), this is a point and the claimed condition holds. For now suppose \(q>0\) and all \(v_i>0\).

Put
\[
D=V-q>0,\qquad \ell_i=p_i^{\mathrm{VCG}}=(v_i-D)_+,
\qquad u_i=v_i-\ell_i=\min(v_i,D).
\]
Every point of \(F\) satisfies \(p_i\ge\ell_i\), because the other payments total at most \(V-v_i\). Thus the translation \(y=p-\ell\) identifies \(F\) with
\[
K=\{y:0\le y_i\le u_i,\ \sum_i y_i=r\},
\qquad r=q-\sum_i\ell_i=\sum_i u_i-D.
\]
Here \(0<r<\sum_i u_i\), and all \(u_i>0\), so \(K\) has positive area in its plane. Translation preserves centroids, and the Vickrey-nearest point becomes the point of \(K\) minimizing \(\sum_i y_i^2\).

**2. A geometric criterion.** We claim that for this capped triangle,
\[
\operatorname{centroid}(K)=\underset{y\in K}{\arg\min}\ \sum_i y_i^2
\iff r\le\min_i u_i\quad\text{or}\quad u_A=u_B=u_C. \tag{*}
\]
For sufficiency, if \(r\le\min_i u_i\), the upper bounds impose no restriction beyond \(y_i\ge0\) and \(\sum_i y_i=r\). This is an equilateral triangle with centroid \((r/3,r/3,r/3)\), which also minimizes squared norm. If all upper bounds are equal, permutation symmetry makes the centroid this same point, and it is feasible and minimizes squared norm.

For necessity, the centroid of \(K\) satisfies every coordinate bound strictly: each boundary line has zero area, and \(K\) has positive area. Consequently, if it also minimizes squared norm, variations in the directions \(e_i-e_j\) imply that all its coordinates equal \(r/3\).

We show that this is impossible when the upper bounds are unequal and \(r>\min_i u_i\). Choose \(i,j\) with \(u_i=\min_k u_k<u_j\), and let \(k\) be the remaining coordinate. Let \(\tau\) swap coordinates \(i,j\). On \(K\cap\tau(K)\), symmetry gives
\[
\int_{K\cap\tau(K)}(y_j-y_i)\,dA=0.
\]
On the remainder \(K\setminus\tau(K)\), we have \(y_j>u_i\ge y_i\). This remainder has positive area. To see strictness, choose
\[
\max(u_i,r-u_i-u_k)<y_j<\min(u_j,r).
\]
This interval is nonempty because \(r>u_i\), \(u_j>u_i\), and \(r<u_i+u_j+u_k\). The other two coordinates can then be chosen strictly inside their bounds with sum \(r-y_j\); a neighborhood in the plane remains in the remainder. Therefore
\[
\int_K(y_j-y_i)\,dA>0,
\]
so the centroid's \(j\)-coordinate exceeds its \(i\)-coordinate. This proves (*).

**3. Translate the criterion back to values.** Order the singleton values as \(a\le b\le c\), with \(a>0\). The bounds \(u_i=\min(v_i,D)\) have the same order. The first alternative in (*) is
\[
r\le\min_i u_i
\iff \min(b,D)+\min(c,D)\le D
\iff b+c\le D
\iff q\le a.
\]
For the middle equivalence, if \(c\ge D\), the left side is strictly greater than \(D\), since \(b>0\); otherwise both minima are \(b,c\).

The second alternative is
\[
\min(a,D)=\min(b,D)=\min(c,D)
\iff D\le a\quad\text{or}\quad a=b=c.
\]
Since \(D\le a\iff q\ge V-a\), these are exactly the three alternatives in the box.

**4. Zero singleton values.** Suppose, for example, \(v_C=0\). Then \(p_C=\ell_C=0\), and \(F\) is the segment
\[
p_A+p_B=q,\qquad \ell_A\le p_A\le v_A,\qquad \ell_B\le p_B\le v_B.
\]
After translating by VCG, this is precisely
\[
y_A+y_B=r,\qquad y_A,y_B\ge0,
\]
with no additional effective caps: \(u_A,u_B\le D\) and \(r=u_A+u_B-D\le\min(u_A,u_B)\). Its centroid and nearest point are both \((r/2,r/2)\). If at most one singleton value is positive, \(F\) is a point. This completes all cases.

## Worked example where the points differ

Take
\[
(v_A,v_B,v_C)=(1,2,3),\qquad v_P=3.
\]
The efficient allocation has total value \(6>3\), and VCG charges \((0,0,0)\). The minimum-revenue face is the parallelogram
\[
p=(s,t,3-s-t),\qquad 0\le s\le1,\quad0\le t\le2,
\]
with vertices
\[
(0,0,3),\quad(1,0,2),\quad(1,2,0),\quad(0,2,1).
\]
The parametrization has constant area factor, so its area centroid is
\[
\boxed{\operatorname{centroid}(F)=(1/2,1,3/2).}
\]
For every point with total payment \(3\), Cauchy–Schwarz gives
\[
p_A^2+p_B^2+p_C^2\ge\frac{3^2}{3}=3,
\]
with equality exactly at \((1,1,1)\), which is feasible. Hence
\[
\boxed{p^{\mathrm{VN}}=(1,1,1)\ne(1/2,1,3/2).}
\]
