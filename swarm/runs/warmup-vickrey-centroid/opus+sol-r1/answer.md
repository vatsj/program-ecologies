# Exact condition

Write
\[
V=v_A+v_B+v_C,\qquad D=V-v_P>0,\qquad m=\min(v_A,v_B,v_C).
\]
For strictly positive winner values, the Vickrey-nearest point equals the (uniform area) centroid of the minimum-revenue face **if and only if**
\[
\boxed{\quad v_P\le m\quad\text{or}\quad D\le m\quad\text{or}\quad v_A=v_B=v_C.\quad}
\]
As usual, values are nonnegative. If zero winner values are allowed, add the case \(m=0\): equality always holds then, with centroid understood using length on a segment or as the point itself.

# Proof

First, the minimum revenue is \(R=v_P\), and
\[
F=\{p:0\le p_i\le v_i,\ \sum_i p_i=v_P\}.
\]
Indeed the full-set core constraint gives \(\sum p_i\ge v_P\). Conversely, any point in the displayed slice satisfies every core constraint, since
\[
\sum_{i\in T}p_i=v_P-\sum_{j\notin T}p_j
\ge v_P-\sum_{j\notin T}v_j,
\]
and its coordinates are nonnegative. The slice is nonempty because \(0\le v_P<V\).

Suppose first that all winner values and \(v_P\) are positive. Define
\[
u_i=\min(v_i,D),\quad \ell_i=v_i-u_i=p_i^{\rm VCG},
\quad s=\sum_i u_i-D=v_P-\sum_i\ell_i>0.
\]
Every point of \(F\) satisfies \(p_i\ge\ell_i\). Thus translating by VCG, \(y_i=p_i-\ell_i\), identifies \(F\) with
\[
G=\{y:0\le y_i\le u_i,\ \sum_i y_i=s\}.
\]
The Vickrey-nearest point minimizes \(\sum_i y_i^2\) on \(G\). Notice that
\[
u_i+u_j\ge s\quad(i\ne j),
\]
because the remaining cap is at most \(D\).

The polygon has positive area, and its centroid has \(0<y_i<u_i\) for every coordinate. If this centroid minimizes squared distance to the origin, variations in the plane \(\sum y_i=s\) imply that its coordinates must all be \(s/3\). Conversely, if its centroid has equal coordinates, it is the unique minimum-norm point on the whole plane and hence on \(G\). Therefore equality of the two points is equivalent to the centroid of \(G\) having equal coordinates.

We calculate exactly when that happens. Start with the triangle \(y_i\ge0\), \(\sum y_i=s\). The constraint \(y_i\le u_i\) removes a corner triangle of side parameter
\[
d_i=(s-u_i)_+.
\]
The removed triangles have disjoint interiors, by \(u_i+u_j\ge s\). Their areas are proportional to \(d_i^2\), while the original area is proportional to \(s^2\). Corner \(j\)'s centroid has coordinate \(d_j/3\) in coordinates other than \(j\), and coordinate \(u_j+d_j/3\) in coordinate \(j\). Subtracting these moments gives the centroid coordinates
\[
\bar y_i=
\frac{s^3-\sum_j d_j^3-3u_i d_i^2}
{3\bigl(s^2-\sum_j d_j^2\bigr)}.
\]
Thus \(\bar y_A=\bar y_B=\bar y_C\) if and only if
\[
u_A(s-u_A)_+^2=u_B(s-u_B)_+^2=u_C(s-u_C)_+^2. \tag{1}
\]

Condition (1) holds exactly when **all corners are uncut** (\(s\le\min u_i\)) or **all caps are equal** (\(u_A=u_B=u_C\)). To see necessity, if one cap is at least \(s\), its expression in (1) is zero, so all expressions must be zero. Otherwise all caps lie in \((0,s)\). Suppose the smallest and largest are \(a<c\). They satisfy \(a+c\ge s\). For \(f(t)=t(s-t)^2\),
\[
f(a)-f(c)=(c-a)\bigl[ac-(a+c-s)^2\bigr]>0,
\]
because \(0\le a+c-s<a\le c\). Hence (1) fails. Sufficiency of the two stated alternatives is immediate from (1).

Finally translate these alternatives back to values:

- \(s\le\min u_i\) is equivalent to \(v_P\le m\). In fact, the former condition forces every \(u_i<D\): if one equaled \(D\), the sum of it and another positive cap would exceed \(D\), contradicting \(s\le u_k\) for the third coordinate. Hence \(u_i=v_i\) and \(s=v_P\). The converse follows directly from \(v_P\le m\).
- \(u_A=u_B=u_C\) is equivalent to either \(D\le m\) or \(v_A=v_B=v_C\). If the common cap is \(D\), all values are at least \(D\); if it is below \(D\), all values equal that cap.

This proves the boxed condition. If \(v_P=0\), \(F=\{0\}\), and the first alternative covers it.

For completeness, suppose one winner has value zero. There are at most two positive winner values, say \(a,b\). The face is the segment
\[
(p_1,p_2,p_3)=(t,v_P-t,0),\qquad
L=\max(0,v_P-b)\le t\le U=\min(a,v_P).
\]
VCG is \((L,v_P-U,0)\), so squared distance along the segment is
\[
(t-L)^2+(U-t)^2,
\]
uniquely minimized at \(t=(L+U)/2\), precisely the segment's centroid. This also covers a singleton segment.

# Worked example where they differ

Take
\[
(v_P,v_A,v_B,v_C)=(3,1,2,3).
\]
Then \(V=6>3\), \(D=3\), and VCG is \((0,0,0)\). The face is the parallelogram
\[
F=\{(x,y,3-x-y):0\le x\le1,\ 0\le y\le2\}.
\]
Its area centroid is the image of the rectangle's center (the affine map has constant area scale):
\[
\boxed{\bar p=(1/2,1,3/2).}
\]
For any point in the plane \(\sum p_i=3\), Cauchy--Schwarz gives \(\sum p_i^2\ge3\), with equality uniquely at \((1,1,1)\). This point belongs to \(F\), so
\[
\boxed{p^{\rm VN}=(1,1,1)\ne\bar p.}
\]
