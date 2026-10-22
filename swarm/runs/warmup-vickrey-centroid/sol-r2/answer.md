# Exact condition

Write the three item values in increasing order as \(a\le b\le c\), and put \(P=v_P\). For positive item values and \(0\le P<a+b+c\),
\[
\boxed{\quad
p^{\mathrm{VN}}=\operatorname{centroid}(F)
\quad\Longleftrightarrow\quad
P\le a\ \text{ or }\ P\ge b+c\ \text{ or }\ a=b=c.
\quad}
\]
Thus equality holds for sufficiently low or sufficiently high package values, and also for equal item values. All endpoints are included.

If zero item values are allowed, equality also always holds when \(a=0\). As usual, item values are assumed nonnegative. If a negative package value is allowed, \(P\le0\) gives the singleton \(F=\{0\}\), so equality is immediate.

Here and below, a polygon's centroid means its uniform **area centroid**, with the corresponding length centroid for a segment.

# Proof

## 1. The minimum-revenue face and a translation

Assume first that all item values and \(P\) are positive. Write
\[
V=v_A+v_B+v_C,\qquad D=V-P>0.
\]
The core constraint for all three winners requires total payment at least \(P\). Conversely, any vector satisfying
\[
0\le p_i\le v_i,\qquad \sum_i p_i=P
\]
is in the core: for any subset \(T\),
\[
\sum_{i\in T}p_i
=P-\sum_{j\notin T}p_j
\ge P-\sum_{j\notin T}v_j,
\]
and its payments are nonnegative. Such vectors exist since \(0<P<V\). Consequently,
\[
R=P,\qquad F=\{p:0\le p_i\le v_i,\ \sum_i p_i=P\}.
\]

Let
\[
\ell_i=p_i^{\mathrm{VCG}}=(v_i-D)_+,\qquad
u_i=v_i-\ell_i=\min(v_i,D),\qquad
s=P-\sum_i\ell_i=\sum_i u_i-D.
\]
Every point of \(F\) satisfies \(p_i\ge\ell_i\). Translating by \(\ell\), therefore, identifies \(F\) with
\[
Q=\{q:0\le q_i\le u_i,\ \sum_iq_i=s\}.
\]
Here \(u_i>0\) and \(0<s<\sum_i u_i\), so \(Q\) has positive area. Translation preserves centroids, and the Vickrey-nearest point becomes the point of \(Q\) nearest the origin.

## 2. A capped-simplex lemma

**Lemma.** For positive \(u_1,u_2,u_3\) and \(0<s<\sum_i u_i\), the centroid of \(Q\) is its point nearest the origin if and only if
\[
\boxed{\quad s\le\min_i u_i\quad\text{or}\quad u_1=u_2=u_3.\quad}
\]

**Proof.** The centroid lies strictly between each coordinate's bounds. If it minimizes \(\sum_iq_i^2\), the first-order conditions within the plane \(\sum_iq_i=s\) require
\[
q_1=q_2=q_3=s/3.
\]
Conversely, whenever the centroid has these coordinates, it is the unique minimum-norm point, by \(\sum_iq_i^2\ge s^2/3\).

If \(s\le\min_i u_i\), the upper bounds do not cut the simplex \(q_i\ge0,\sum_iq_i=s\), whose centroid is \((s/3,s/3,s/3)\). If all caps are equal, permutation symmetry gives the same centroid.

For necessity, suppose the caps are unequal and \(s>\min_i u_i\). Choose indices \(i,j\) with \(u_i=\min_k u_k<u_j\), and let \(k\) be the remaining index. Conditional on \(q_k=t\), put \(r=s-t\). Uniform area measure on \(Q\) induces uniform length measure on the segment
\[
q_i\in[L,U],\qquad
L=\max(0,r-u_j),\qquad U=\min(u_i,r),\qquad q_j=r-q_i.
\]
Thus
\[
\mathbb E[q_j-q_i\mid q_k=t]=r-L-U\ge0.
\]
This expression is strictly positive when \(u_i<r<u_i+u_j\). Such slices occur over an interval of positive length: indeed,
\[
\max(u_i,s-u_k)<\min(s,u_i+u_j),
\]
because \(s>u_i\), all caps are positive, and \(s<\sum_i u_i\). Hence the centroid satisfies \(\bar q_j>\bar q_i\). It cannot have three equal coordinates, proving the lemma. \(\square\)

## 3. Translate the lemma into values

First,
\[
u_A=u_B=u_C
\quad\Longleftrightarrow\quad
v_A=v_B=v_C\ \text{ or }\ D\le\min_i v_i.
\]
To see this, if the common cap is below \(D\), every original value equals that cap; otherwise every value is at least \(D\). Since \(D=V-P\), the second alternative is precisely \(P\ge b+c\).

Next,
\[
s\le\min_i u_i\quad\Longleftrightarrow\quad P\le a.
\]
For the forward implication, if any \(u_i=D\), the other two positive caps give
\(s=\sum_j u_j-D>\min_j u_j\), a contradiction. Thus every value is below \(D\), so \(u_i=v_i\) and \(s=P\), giving \(P\le a\). Conversely, if \(P\le a\), then \(D=V-P\ge b+c>c\), so again \(u_i=v_i\) and \(s=P\le a\).

The lemma now gives exactly the stated condition. If \(P=0\), the face is the origin, already covered by \(P\le a\).

For completeness, suppose exactly two item values are positive. In the translated description the zero coordinate is fixed, and the two remaining caps satisfy \(u_1,u_2\le D\). Hence
\[
s=u_1+u_2-D\le\min(u_1,u_2).
\]
The face is therefore the segment \(q_1,q_2\ge0,\ q_1+q_2=s\). Both its centroid and its nearest point to the origin are \((s/2,s/2)\). With only one positive item value the face is a singleton. This proves the assertion about zero values.

# Worked example: the points differ

Take
\[
(v_A,v_B,v_C)=(2,3,4),\qquad v_P=3.
\]
Here \(D=6\), so all VCG payments are zero. The minimum-revenue face is
\[
F=\{p\ge0:p_A+p_B+p_C=3,\ p_A\le2\},
\]
with vertices
\[
(0,0,3),\quad(2,0,1),\quad(2,1,0),\quad(0,3,0).
\]
The equal-payment point is feasible, and
\(\sum_i p_i^2\ge(\sum_i p_i)^2/3=3\), with equality only there. Thus
\[
\boxed{p^{\mathrm{VN}}=(1,1,1).}
\]

To compute the centroid, start with the full triangle \(p\ge0,\sum_i p_i=3\), whose centroid is \((1,1,1)\). The cap removes the triangle with vertices
\[
(3,0,0),\quad(2,1,0),\quad(2,0,1).
\]
This removed triangle has \(1/9\) of the full triangle's area and centroid \((7/3,1/3,1/3)\). Subtracting its first moment gives
\[
\boxed{
\operatorname{centroid}(F)
=\frac{(1,1,1)-\frac19(7/3,1/3,1/3)}{1-\frac19}
=\left(\frac56,\frac{13}{12},\frac{13}{12}\right).
}
\]
The points differ even though no value cap binds at the Vickrey-nearest point. Consistently with the condition, \(3>2\), \(3<3+4\), and the item values are unequal.
