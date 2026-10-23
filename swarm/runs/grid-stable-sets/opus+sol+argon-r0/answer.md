A stable set exists **if and only if \(K\) is even**. For \(K=2m\), the **unique** stable set is
\[
V=\{(0,m,m),(m,0,m),(m,m,0)\}.
\]

We prove both the assertion and completeness of this list.

### 1. The structure imposed by internal stability

Two distinct allocations are mutually nondominating if and only if they share a coordinate. Indeed, if they share a coordinate, their other two coordinates change in opposite directions, so neither improves two coordinates. If they share no coordinate, all three coordinate differences are nonzero and sum to zero; two therefore have the same sign, giving domination in one direction.

Consequently, any internally stable nonempty set has one of the following forms:

* all its points have one fixed coordinate; or
* it consists of exactly three points of the form
  \[
  (a+d,b,c),\quad(a,b+d,c),\quad(a,b,c+d),
  \tag{1}
  \]
  where \(a,b,c\geq0\), \(d\ne0\), \(a+b+c+d=K\), and all three displayed points are nonnegative.

Here is a proof that these possibilities exhaust the sets. If there are at most two points, they share a coordinate. Otherwise, take two distinct points, and permute coordinates to write them as
\[
A=(r,s,t),\qquad B=(r,s+u,t-u),\qquad u\ne0.
\]
If every point has first coordinate \(r\), we have the first possibility. Otherwise a point \(C\) with first coordinate different from \(r\) must share one of its last two coordinates with each of \(A,B\). The only possibilities are
\[
C_+=(r+u,s,t-u),\qquad C_-=(r-u,s+u,t).
\]
These two possibilities share no coordinate, so at most one can belong to the set. If \(C=C_+\), any point on the line \(x_1=r\) sharing a coordinate with \(C\) must equal \(A\) or \(B\); the same conclusion holds for \(C=C_-\). Thus the set is exactly \(\{A,B,C\}\). These are of form (1): for \(C_+\) take \((a,b,c,d)=(r,s,t-u,u)\); for \(C_-\) take \((a,b,c,d)=(r,s+u,t,-u)\).

The empty set is not externally stable, so it needs no further consideration.

### 2. No set with a fixed coordinate is stable

Suppose every point of \(V\) has first coordinate \(q\). No allocation with first coordinate \(q\) can be dominated by \(V\), so external stability forces \(V\) to contain the entire line of allocations with that coordinate.

If \(q<K\), take any allocation \(y\) with \(y_1=q+1\). A point \(x\in V\) could dominate \(y\) only by increasing both coordinates 2 and 3. Integer strictness would imply
\[
x_2+x_3\geq y_2+y_3+2=K-q+1,
\]
contradicting \(x_2+x_3=K-q\). This \(y\) is outside \(V\) and undominated. If \(q=K\), then \(V=\{(K,0,0)\}\), which dominates no allocation and is again not stable. The same argument applies to either other fixed coordinate.

### 3. Triangles with \(d>0\) cannot be stable

For (1), every allocation satisfying
\[
y_1\geq a,\qquad y_2\geq b,\qquad y_3\geq c
\tag{2}
\]
is undominated by \(V\): each point of \(V\) exceeds the base vector \((a,b,c)\) in only one coordinate. The allocations (2) are obtained by distributing \(d\) nonnegative integer units among three coordinates. If \(d\geq2\), for example \((a+1,b+d-1,c)\) is one such allocation outside the three vertices, contradicting external stability. Hence \(d=1\) is necessary.

Since \(K\geq2\), now \(a+b+c=K-1\geq1\). Suppose, after permuting coordinates, that \(a\geq1\). The allocation
\[
y=(a-1,b+1,c+1)
\]
is nonnegative, sums to \(K\), and is outside \(V\). Every vertex of (1) exceeds \(y\) only in coordinate 1, if anywhere: its second coordinate is at most \(b+1\), and its third at most \(c+1\). Thus \(y\) is undominated. This excludes \(d>0\).

### 4. Triangles with \(d<0\) force the stated solution

Write \(d=-h\), where \(h>0\). The triangle is
\[
V=\{(a-h,b,c),(a,b-h,c),(a,b,c-h)\},
\tag{3}
\]
with \(a,b,c\geq h\) and \(a+b+c=K+h\).

An allocation \(y\) is dominated by \(V\) exactly when at least two of
\[
y_1<a,\qquad y_2<b,\qquad y_3<c
\tag{4}
\]
hold. Necessity follows because these are the coordinatewise maxima of \(V\). For sufficiency, each pair of these maxima occurs together in one of the three vertices.

Thus every allocation with \(y_1\geq a\) and \(y_2\geq b\) is undominated. Among the three vertices, only \((a,b,c-h)\) satisfies these two inequalities. If \(c-h\geq1\), however, the distinct allocation
\[
(a+1,b,c-h-1)
\]
also satisfies them and is nonnegative, producing an undominated point outside \(V\). External stability therefore forces \(c=h\). Applying the same argument to the other two pairs forces \(a=b=h\). Consequently \(K=2h\), and (3) is precisely the asserted symmetric triple.

### 5. Verification of existence

Let \(K=2m\). The three displayed symmetric allocations share a coordinate pairwise, so they are internally stable. If an allocation \(y\) has at least two coordinates at least \(m\), its sum \(2m\) forces those coordinates to be exactly \(m\) and the remaining coordinate to be zero; thus \(y\in V\). Every allocation outside \(V\) consequently has at least two coordinates strictly below \(m\). The vertex giving \(m\) to those two players dominates it. This proves external stability and completes the proof.
