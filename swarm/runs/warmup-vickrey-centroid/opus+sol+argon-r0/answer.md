# Exact condition

Write \(V=v_A+v_B+v_C\), and assume the usual nonnegative valuations, with \(v_P<V\). If all three winner values are positive, then

\[
\boxed{\quad p^{\rm VN}=\operatorname{centroid}(F)
\iff
v_P\le \min_i v_i
\quad\text{or}\quad
v_P\ge V-\min_i v_i
\quad\text{or}\quad
v_A=v_B=v_C.\quad}
\]

The inequalities include their endpoints. If a winner has value zero, the two points always coincide (using length measure for a segment and its sole point for a singleton).

## Proof

If \(v_P=0\), \(F=\{0\}\), so suppose first that \(v_P>0\) and all winner values are positive.

**Reduce the core to a capped simplex.** The full-set constraint requires total payment at least \(v_P\). Conversely, any vector with
\[
\sum_i p_i=v_P,\qquad 0\le p_i\le v_i
\]
satisfies every core constraint: for every \(T\),
\[
\sum_{i\in T}p_i=v_P-\sum_{j\notin T}p_j
\ge v_P-\sum_{j\notin T}v_j,
\]
and its coordinates are nonnegative. Such vectors exist because \(0<v_P<V\). Thus \(R=v_P\) and this capped simplex is exactly \(F\).

Set
\[
d=V-v_P>0,\qquad
\ell_i=(v_i-d)_+=p_i^{\rm VCG},\qquad
h_i=v_i-\ell_i=\min(v_i,d),
\]
\[
y_i=p_i-\ell_i,\qquad
r=v_P-\sum_i\ell_i=\sum_i h_i-d.
\]
Every point of \(F\) has \(p_i\ge\ell_i\): this follows from its total and the other two value caps. Translation therefore identifies \(F\) with
\[
K=\{y\in\mathbb R^3: \sum_i y_i=r,\quad 0\le y_i\le h_i\}.
\]
Under this translation, the Vickrey-nearest point becomes the point of \(K\) nearest the origin. Here \(h_i>0\) and \(0<r<\sum_i h_i\), so \(K\) has positive area in its plane.

**A geometric lemma.** For any such capped simplex \(K\), its centroid equals its nearest point to the origin if and only if
\[
\boxed{h_A=h_B=h_C\quad\text{or}\quad r\le\min_i h_i.}
\]

To prove the lemma, its centroid \(c\) is in the relative interior of \(K\). If it minimizes squared distance to the origin, derivatives in every direction tangent to \(\sum_i y_i=r\) vanish. Hence
\[
c_A=c_B=c_C=r/3.
\]
Conversely, if the centroid has these coordinates, it is the nearest point to the origin in the entire plane, so it is also nearest in \(K\).

It remains to characterize when the centroid coordinates are equal. Suppose \(h_i<h_j\). On the part of \(K\) with \(y_j\le h_i\), swapping coordinates \(i,j\) preserves the region and area, so its integral of \(y_j-y_i\) is zero. On the remaining part, \(y_j>h_i\ge y_i\), so that integral is strictly positive whenever this part has positive area. It has positive area exactly when \(r>h_i\): if \(r\le h_i\), it is empty; if \(r>h_i\), choose
\[
\max\{h_i,r-h_i-h_k\}<y_j<\min\{h_j,r\},
\]
where \(k\) is the third index, and then choose \(0<y_i<h_i\), \(0<y_k<h_k\) with sum \(r-y_j\). The interval is nonempty because \(r<\sum h_i\). These strict inequalities give a relatively open set of positive area. Consequently,
\[
h_i<h_j\ \text{and}\ r>h_i\quad\Longrightarrow\quad c_i<c_j.
\]
Thus, if the caps are unequal and their minimum is less than \(r\), the centroid cannot have equal coordinates. In the other cases it does: equal caps give permutation symmetry; if \(r\le\min h_i\), all caps are redundant and \(K\) is the symmetric triangle \(y_i\ge0,\sum y_i=r\). This proves the lemma.

**Translate the lemma into values.** Order the values as \(a\le b\le c\). The condition \(r\le\min h_i\) is equivalent to
\[
\min(b,d)+\min(c,d)\le d.
\]
Since \(b>0\), this forces \(c<d\), and the inequality becomes \(b+c\le d=V-v_P\), or \(v_P\le a\). Conversely, \(v_P\le a\) makes that inequality hold.

For the equal-cap condition, if \(d\le a\), all caps equal \(d\); this is exactly \(v_P\ge b+c=V-a\). If \(d>a\), equality of all caps forces \(a=b=c\), and equal winner values clearly suffice. This proves the stated condition.

**Zero values.** If just two winner values \(a,b\) are positive, the zero-valued winner pays zero. The face is the segment
\[
p_1+p_2=v_P,\qquad
\max(0,v_P-b)\le p_1\le\min(a,v_P).
\]
Its endpoints are
\[
(\ell_1,v_P-\ell_1),\qquad(v_P-\ell_2,\ell_2),
\]
where \(\ell_1=(v_P-b)_+\), \(\ell_2=(v_P-a)_+\). Relative to the VCG vector, these endpoints are \((0,r)\) and \((r,0)\), so the nearest point is their midpoint, also the segment's centroid. With at most one positive winner value, \(F\) is a singleton.

## Worked example where the points differ

Take
\[
(v_A,v_B,v_C)=(1,2,3),\qquad v_P=2.
\]
Then \(V=6>2\), VCG is \((0,0,0)\), and
\[
F=\{p\ge0:p_A+p_B+p_C=2,\ p_A\le1\}.
\]
(The other two caps are redundant.) The nearest point to zero in its plane is feasible, so
\[
\boxed{p^{\rm VN}=(2/3,2/3,2/3).}
\]

For the centroid, start with the full triangle having vertices \((2,0,0),(0,2,0),(0,0,2)\). Its centroid is \((2/3,2/3,2/3)\). The removed triangle has vertices \((2,0,0),(1,1,0),(1,0,1)\), centroid \((4/3,1/3,1/3)\), and one quarter of the original area. Therefore
\[
\operatorname{centroid}(F)
=\frac{(2/3,2/3,2/3)-\tfrac14(4/3,1/3,1/3)}{1-\tfrac14}
=\boxed{(4/9,7/9,7/9)}.
\]
These points differ, as the condition predicts: \(1<2<5\), and the winner values are unequal.
