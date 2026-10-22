# Exact condition

Write $V=v_A+v_B+v_C$ and $m=\min(v_A,v_B,v_C)$, with nonnegative winner values and $v_P<V$. If all three winner values are positive, then

$$
\boxed{\quad p^{\mathrm{VN}}=\operatorname{centroid}(F)
\quad\Longleftrightarrow\quad
v_P\le m\ \ \mathrm{or}\ \ v_P\ge V-m\ \ \mathrm{or}\ \ v_A=v_B=v_C.\quad}
$$

Thus, if the winner values are unequal, equality holds exactly when the package value is at most the smallest winner value, or at least the sum of the two largest winner values. The endpoints are included.

If any winner value is zero (or if $v_P\le 0$), equality always holds: the face is a segment or a point, and the Vickrey-nearest point is its centroid. Here and below, a lower-dimensional face has its centroid with respect to its own dimension.

## Proof

First suppose all winner values and $v_P$ are positive. Set

$$
d=V-v_P>0,\qquad
\ell_i=(v_i-d)_+=p_i^{\mathrm{VCG}},\qquad
w_i=v_i-\ell_i=\min(v_i,d),\qquad
r=v_P-\sum_i\ell_i=\sum_iw_i-d.
$$

**Reduction to a capped simplex.** Let $W=\{A,B,C\}$. The core constraint for all three winners requires total payments at least $v_P$. Conversely, every vector satisfying

$$
0\le p_i\le v_i,\qquad \sum_i p_i=v_P
$$

is in the core: for any subset $T\subseteq W$,

$$
\sum_{i\in T}p_i
=v_P-\sum_{j\in W\setminus T}p_j
\ge v_P-\sum_{j\in W\setminus T}v_j,
$$

and its payments are nonnegative. Such vectors exist because $0<v_P<V$. Consequently, the minimum revenue is $v_P$, and these vectors constitute $F$.

The singleton constraints imply $p_i\ge\ell_i$. Translating by $\ell$ therefore identifies $F$ with

$$
K=\{x\in\mathbb R^3:0\le x_i\le w_i,\quad x_A+x_B+x_C=r\}.
$$

Translation preserves centroids, and the Vickrey-nearest point becomes the point of $K$ minimizing $\sum_i x_i^2$. Here all $w_i>0$ and $0<r<\sum_iw_i$ (if all $v_i\le d$ then $r=v_P>0$, while if some $v_k>d$ then $w_k=d$ and the other two $w_i>0$, so $r=\sum_i w_i-d>0$), so $K$ has positive area in its plane.

**A centroid fact.** For positive caps $w_i$ and $0<r<\sum_iw_i$, the centroid $c$ of $K$ has equal coordinates if and only if

$$
\boxed{\quad r\le\min_i w_i\quad\mathrm{or}\quad w_A=w_B=w_C.\quad} \qquad (1)
$$

Sufficiency follows from symmetry: in the first case all upper bounds are redundant, giving an equilateral triangle; in the second case $K$ is invariant under every coordinate permutation.

For necessity, suppose $w_i<w_j$. Slice $K$ at a fixed value of the remaining coordinate $x_k=t$, and put $s=r-t$. The feasible interval for $x_i$ is

$$
\max(0,s-w_j)\le x_i\le\min(w_i,s).
$$

The mean of $x_j-x_i$ along this segment is

$$
s-\max(0,s-w_j)-\min(w_i,s)
=\min(s,w_j)-\min(s,w_i)\ge0.
$$

If $r>w_i$, it is strictly positive on a positive-area collection of slices. Indeed, choose

$$
\max(0,r-w_i-w_j)<t<\min(w_k,r-w_i).
$$

This interval is nonempty because $r>w_i$ and $r<\sum_iw_i$. These slices have positive length and $s>w_i$. Integrating the slice means (weighted by their lengths) gives $c_j>c_i$. Thus, if the caps are unequal and $r>\min_iw_i$, choose a smallest cap and a larger cap to see that the centroid coordinates cannot all be equal. This proves (1).

**When the centroid minimizes distance.** The centroid is in the relative interior of $K$. If it minimizes $\sum_i x_i^2$, differentiation along each direction $e_i-e_j$ gives $c_i=c_j$. Conversely, if its coordinates are equal, it is $(r/3,r/3,r/3)$, the unique minimum of that squared norm on the entire plane $\sum_i x_i=r$. Hence (1) is precisely the condition for the two points to agree. When they agree, their payment vector is

$$
p_i=\ell_i+\frac r3.
$$

**Translate the condition back to values.** Sort the winner values as $a\le b\le c$. Their effective caps are ordered in the same way. Since $r=\sum_iw_i-d$,

$$
r\le\min_iw_i
\quad\Longleftrightarrow\quad
\min(b,d)+\min(c,d)\le d
\quad\Longleftrightarrow\quad
b+c\le d
\quad\Longleftrightarrow\quad
v_P\le a.
$$

For the middle equivalence, if $c\ge d$, the left side is strictly greater than $d$ because $b>0$; otherwise both caps equal their original values. Also,

$$
\min(a,d)=\min(b,d)=\min(c,d)
\quad\Longleftrightarrow\quad
d\le a\ \ \mathrm{or}\ \ a=b=c.
$$

The condition $d\le a$ is exactly $v_P\ge b+c=V-m$. These are the three alternatives in the theorem.

Finally, $v_P\le 0$ gives minimum revenue $R=0$ and $F=\{(0,0,0)\}$. If a winner value is zero and $v_P>0$, its payment and VCG payment are fixed at zero; omitting its coordinate, at most two caps $w_1,w_2\le d$ remain (padding with a zero cap if necessary) in the same translation and $r=w_1+w_2-d$. Thus $r\le w_1,w_2$, so all upper bounds are redundant: the translated face is the segment from $(r,0)$ to $(0,r)$, or a point if $r=0$. Its minimum-norm point is its midpoint, proving the zero-value assertion.

## Worked example where they differ

Take

$$
(v_P,v_A,v_B,v_C)=(2,1,2,2).
$$

Here $V=5$, $m=1$, and neither $2\le1$ nor $2\ge4$ holds; the winner values are unequal. VCG charges zero to every winner, and

$$
F=\{p_A+p_B+p_C=2,\quad 0\le p_A\le1,\quad p_B,p_C\ge0\}.
$$

(The caps $p_B,p_C\le2$ follow from these constraints.) The equal-payment point is feasible and minimizes the squared distance to zero, so

$$
\boxed{p^{\mathrm{VN}}=(2/3,2/3,2/3).}
$$

To compute the area centroid, start with the triangle having vertices $(2,0,0),(0,2,0),(0,0,2)$, whose centroid is $(2/3,2/3,2/3)$. Remove the triangle having vertices $(2,0,0),(1,1,0),(1,0,1)$, whose centroid is $(4/3,1/3,1/3)$. The removed triangle has one quarter of the original area. Therefore

$$
\operatorname{centroid}(F)
=\frac{4(2/3,2/3,2/3)-(4/3,1/3,1/3)}3
=\boxed{(4/9,7/9,7/9)},
$$

which differs from the Vickrey-nearest point.
