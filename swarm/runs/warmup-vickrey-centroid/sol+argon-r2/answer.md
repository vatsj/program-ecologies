# Exact condition

Write \(r=v_P\), \(S=v_A+v_B+v_C\), and \(a=\min(v_A,v_B,v_C)\). Values are taken to be nonnegative, as usual. The centroid means the uniform area centroid, or the uniform length centroid for a segment.

If all three winner values are positive, then
\[
\boxed{\quad
p^{\mathrm{VN}}=\operatorname{centroid}(F)
\quad\Longleftrightarrow\quad
v_A=v_B=v_C\quad\text{or}\quad r\le a\quad\text{or}\quad r\ge S-a.
\quad}
\]
In the regime \(r\le a\), the common point is \((r/3,r/3,r/3)\). In the regime \(r\ge S-a\), it is \((v_A-D/3,v_B-D/3,v_C-D/3)\), where \(D=S-r\). If all three winner values are equal, the common point is again \((r/3,r/3,r/3)\).

The assumption \(r<S\) remains in force. If a winner has value zero, the two points always agree; the face then has dimension at most one. Thus, allowing zero values, add \(a=0\) to the alternatives in the box.

# Proof

## 1. Reduce the core and shift by VCG

The displayed core inequalities in the question are equivalent to
\[
0\le p_i\le v_i,\qquad \sum_i p_i\ge r.
\]
Indeed, the inequality for all winners gives the revenue bound. Conversely, for any subset \(T\), the revenue bound and the caps imply
\[
\sum_{i\in T}p_i\ge r-\sum_{j\notin T}p_j
\ge r-\sum_{j\notin T}v_j,
\]
and nonnegativity supplies the other part of the maximum. Since \(0\le r<S\), the box contains points of total \(r\). Consequently,
\[
R=r,\qquad F=\{p:0\le p_i\le v_i,\ \sum_i p_i=r\}.
\]

Put
\[
D=S-r>0,\qquad
\ell_i=p_i^{\mathrm{VCG}}=(v_i-D)_+,\qquad
h_i=v_i-\ell_i=\min(v_i,D).
\]
Every point of \(F\) satisfies \(p_i\ge\ell_i\), by the other two value caps. Therefore the translation \(q=p-\ell\) identifies \(F\) with
\[
Q=\{q:0\le q_i\le h_i,\ \sum_i q_i=t\},
\qquad t=r-\sum_i\ell_i=\sum_i h_i-D.
\]
Translation takes the centroid of \(F\) to the centroid of \(Q\), and takes the Vickrey-nearest problem to minimizing \(\|q\|^2\) on \(Q\).

For now assume \(r>0\) and all \(v_i>0\). Then \(h_i>0\) and \(0<t<\sum_i h_i\), so \(Q\) has positive area and its centroid lies strictly between every pair of coordinate bounds. If its centroid minimizes \(\|q\|^2\), differentiation along each direction \(e_i-e_j\) forces its coordinates to be equal. Conversely, if its centroid is \((t/3,t/3,t/3)\), this point minimizes the squared norm, since
\[
\sum_i q_i^2\ge \frac{(\sum_i q_i)^2}{3}=\frac{t^2}{3}.
\]
It remains to characterize when the centroid of \(Q\) has equal coordinates.

## 2. A capped-simplex centroid lemma

For positive \(h_1,h_2,h_3\) and \(0<t<\sum_i h_i\), the centroid of \(Q\) has equal coordinates exactly when
\[
\boxed{\quad h_1=h_2=h_3\quad\text{or}\quad t\le\min_i h_i.\quad} \tag{1}
\]
Both conditions are sufficient by permutation symmetry: in the second case all upper bounds are redundant, so \(Q\) is the ordinary triangle \(q_i\ge0,\ \sum_iq_i=t\).

For necessity, take a point uniformly in \(Q\). Suppose \(h_i<h_j\), and condition on \(q_k\), where \(k\) is the third coordinate. With \(s=t-q_k\), the conditional distribution of \(q_i\) is uniform on
\[
[L,U]=[\max(0,s-h_j),\ \min(h_i,s)].
\]
Thus
\[
\mathbb E[q_j-q_i\mid q_k]=s-L-U
=\begin{cases}
0,&0\le s\le h_i,\\
s-h_i,&h_i<s\le h_j,\\
h_j-h_i,&h_j<s\le h_i+h_j.
\end{cases}
\]
This is nonnegative, and it is strictly positive whenever \(s>h_i\). If also \(t>h_i\), feasible values of \(s>h_i\) occur with positive area: the feasible interval for \(s\) is
\[
[\max(0,t-h_k),\ \min(t,h_i+h_j)],
\]
whose upper endpoint exceeds \(h_i\) and whose lower endpoint is strictly below its upper endpoint. Hence \(\mathbb E[q_j]>\mathbb E[q_i]\).

If the caps are not all equal and \(t>\min_i h_i\), choose \(i\) with the smallest cap and \(j\) with a larger cap. Their centroid coordinates differ. This proves (1).

## 3. Express (1) in the original values

Relabel the winner values as \(a\le b\le c\). If \(D\le a\), all three caps \(h_i\) equal \(D\); this is exactly \(r\ge S-a\).

If \(D>a\), the smallest cap is \(a\). All three caps are equal exactly when \(a=b=c\). The other alternative in (1) becomes
\[
t\le a
\quad\Longleftrightarrow\quad
\min(b,D)+\min(c,D)\le D.
\]
For positive \(b,c\), this is impossible when \(D\le c\), because \(\min(c,D)=D\) and \(\min(b,D)>0\). When \(D>c\), it is equivalent to \(b+c\le D\), or \(r\le a\). This proves the boxed condition.

If \(r=0\), the face is the singleton \(\{0\}\), covered by \(r\le a\). If some winner values are zero, discard their fixed zero coordinates. With two positive coordinates, the translated face has total
\[
t=h_1+h_2-D\le\min(h_1,h_2),
\]
because both \(h_i\le D\). It is therefore the segment from \((0,t)\) to \((t,0)\); its midpoint \((t/2,t/2)\) also minimizes the squared norm. With at most one positive coordinate, the face is a singleton. This proves the stated zero-value extension.

# Worked counterexample (no cap binds at the nearest point)

Take
\[
(v_A,v_B,v_C)=(1,2,2),\qquad v_P=2.
\]
Here \(S=5\), \(a=1\), and \(1<2<4=S-a\), with unequal winner values. VCG is \((0,0,0)\). On the plane \(p_A+p_B+p_C=2\), the squared norm is minimized at
\[
\boxed{p^{\mathrm{VN}}=(2/3,2/3,2/3).}
\]
This is feasible and strictly below every value cap.

To compute the centroid, start with the full nonnegative triangle of total payment 2, whose centroid is \((2/3,2/3,2/3)\). Only the cap \(p_A\le1\) removes positive area. The removed corner is a translated triangle of total 1, with centroid \((4/3,1/3,1/3)\). The full and removed triangles have areas in ratio \(4:1\), because their linear scales have ratio \(2:1\). Subtracting their first moments gives
\[
\boxed{
\operatorname{centroid}(F)
=\frac{4(2/3,2/3,2/3)-(4/3,1/3,1/3)}{4-1}
=(4/9,7/9,7/9).
}
\]
Thus the centroid and Vickrey-nearest point differ even when none of the value caps binds at the Vickrey-nearest point.
