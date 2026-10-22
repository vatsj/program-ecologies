# Exact condition

Assume the values are nonnegative, and let
\[
x\le y\le z
\]
be the three winner values in increasing order. Under the given assumption \(v_P<x+y+z\), the Vickrey-nearest point equals the **area centroid** of the minimum-revenue polygon if and only if
\[
\boxed{\quad x=0\quad\text{or}\quad x=y=z\quad\text{or}\quad
v_P\le x\quad\text{or}\quad v_P\ge y+z.\quad}
\]
For a segment or point, “centroid” means its length centroid or the point itself. Thus, with strictly positive winner values, equality occurs exactly when all three values are equal, the package value is at most the smallest winner value, or the package value is at least the sum of the two largest winner values. All boundary equalities are included.

## Proof

Write \(t=v_P\), \(S=v_A+v_B+v_C\), and \(d=S-t>0\).

**1. Identify the minimum-revenue face.** The core constraint for all three winners gives \(\sum_i p_i\ge t\). Conversely, any vector satisfying
\[
0\le p_i\le v_i,\qquad \sum_i p_i=t
\]
satisfies every core constraint: for any subset \(T\),
\[
\sum_{i\in T}p_i=t-\sum_{j\notin T}p_j
\ge t-\sum_{j\notin T}v_j,
\]
and the left side is also nonnegative. Such vectors exist because \(0\le t<S\). Consequently,
\[
R=t,\qquad F=\{p:0\le p_i\le v_i,\ \sum_i p_i=t\}.
\tag{1}
\]
If \(t=0\), this is a singleton and the claimed condition holds. For now, suppose \(t>0\) and all three winner values are positive.

**2. Translate VCG to the origin.** Define
\[
u_i=\min(v_i,d),\qquad
\ell_i=v_i-u_i=\max(0,v_i-d)=p_i^{\mathrm{VCG}},
\qquad h=\sum_i u_i-d.
\]
Every point of \(F\) satisfies \(p_i\ge\ell_i\), since
\(p_i=t-\sum_{j\ne i}p_j\ge t-\sum_{j\ne i}v_j\).
Therefore the translation \(r=p-\ell\) takes \(F\) exactly onto
\[
H=\{r:0\le r_i\le u_i,\ \sum_i r_i=h\}.
\tag{2}
\]
Here \(0<h<\sum_i u_i\): if every \(v_i<d\), then \(h=t>0\); otherwise one \(u_i=d\) and the other two are positive. The upper inequality follows from \(d>0\).

The Vickrey-nearest point translates to the point of \(H\) nearest the origin, and the centroid translates to the centroid of \(H\). The latter is strictly inside all six bounds in (2). Indeed, \(r_i=hu_i/\sum_j u_j\) is strictly inside them, so \(H\) has positive area, and averaging over that area gives \(0<\bar r_i<u_i\).

If this centroid minimizes \(\sum_i r_i^2\), perturbations in every direction \(e_i-e_j\) imply \(\bar r_i=\bar r_j\). Conversely, the point \((h/3,h/3,h/3)\), whenever feasible, minimizes squared distance over the entire plane \(\sum_i r_i=h\). Hence
\[
\text{centroid = nearest point}
\quad\Longleftrightarrow\quad
\bar r_A=\bar r_B=\bar r_C.
\tag{3}
\]

**3. Determine when the centroid coordinates are equal.** We use the following elementary fact about the capped triangle (2):
\[
\boxed{\quad
\bar r_A=\bar r_B=\bar r_C
\quad\Longleftrightarrow\quad
u_A=u_B=u_C\ \text{ or }\ h\le\min_i u_i.
\quad}
\tag{4}
\]
For sufficiency, equal caps give permutation symmetry. If \(h\le\min_i u_i\), the caps do not cut the triangle \(r_i\ge0,\ \sum_i r_i=h\), whose centroid has equal coordinates.

For necessity, suppose \(u_i<u_j\). Partition \(H\) into the part where \(r_j\le u_i\) and the part where \(r_j>u_i\). The first part is invariant under exchanging coordinates \(i,j\); this exchange preserves area, so the integral of \(r_j-r_i\) over it is zero. On the second part, \(r_j-r_i>0\).

If \(h>u_i\), the second part has positive area. To see this explicitly, with \(k\) the remaining index, choose
\[
r_j\in\bigl(\max\{u_i,h-u_i-u_k\},\ \min\{u_j,h\}\bigr).
\]
This interval is nonempty because \(u_i<u_j\), \(u_i<h\), and \(h<u_i+u_j+u_k\). The remaining total can then be split with \(0<r_i<u_i\) and \(0<r_k<u_k\), giving an interior point with \(r_j>u_i\). Thus \(\bar r_j>\bar r_i\). Taking \(u_i\) smallest and \(u_j\) largest proves necessity in (4).

**4. Express (4) in the original values.** If all the \(u_i\) are equal, either all the \(v_i\) are equal, or every \(v_i\ge d\). The latter condition is
\[
d\le x\quad\Longleftrightarrow\quad t\ge S-x=y+z.
\]
Conversely, each of these conditions makes all the \(u_i\) equal.

Next, \(h\le\min_i u_i\) is equivalent to \(t\le x\). In fact, if some \(v_i\ge d\), then \(u_i=d\) and \(h\) is the sum of the other two positive caps, strictly larger than the smallest cap. Thus \(h\le\min_i u_i\) forces every \(v_i<d\); then \(h=t\) and \(\min_i u_i=x\). Conversely, if \(t\le x\), then \(d=S-t\ge y+z>z\), so again \(u_i=v_i\) and \(h=t\le x\).

Together with (3)–(4), this proves the asserted condition for positive winner values.

**5. Zero winner values.** If, for example, \(v_A=0\), then \(p_A=0\). Write \(\ell_B=\max(0,t-v_C)\) and \(\ell_C=\max(0,t-v_B)\). The face is the segment
\[
p_B\in[\ell_B,t-\ell_C],\qquad p_C=t-p_B.
\]
Let \(k=t-\ell_B-\ell_C\ge0\). Relative to VCG, this segment is
\[
(p_B-\ell_B,p_C-\ell_C)=(s,k-s),\qquad 0\le s\le k.
\]
Both its midpoint and its point nearest the origin have \(s=k/2\). This also covers a segment collapsing to a point, and completes the proof.

## Worked example where the points differ

Take
\[
(v_A,v_B,v_C)=(1,2,3),\qquad v_P=3.
\]
The winning total is \(6>3\), and all VCG payments are zero:
\[
p^{\mathrm{VCG}}=(0,0,0).
\]
The minimum-revenue face is the parallelogram with vertices
\[
(0,0,3),\quad(1,0,2),\quad(1,2,0),\quad(0,2,1).
\]
Its area centroid is its center,
\[
\boxed{\bar p=(1/2,1,3/2).}
\]
For any point with total payment \(3\), Cauchy–Schwarz gives
\[
p_A^2+p_B^2+p_C^2\ge\frac{3^2}{3}=3,
\]
with equality exactly at \((1,1,1)\). This point respects all caps, so
\[
\boxed{p^{\mathrm{VN}}=(1,1,1)\ne\bar p.}
\]
Here the values are unequal and \(1<3<2+3\), as required by the condition.

For comparison, with the same winner values and \(v_P=5\), we have \(d=1\) and \(p^{\mathrm{VCG}}=(0,1,2)\). The surplus coordinates \(v_i-p_i\) form the full triangle with nonnegative coordinates summing to \(1\). Both its centroid and the Vickrey-nearest point give
\[
\bar p=p^{\mathrm{VN}}=(2/3,5/3,8/3),
\]
in agreement with the boundary case \(v_P=y+z\).
