# Answer

A stable set exists **if and only if (K) is even**. For (K=2m), the **unique** stable set is
\[
V_m=\{(m,m,0),(m,0,m),(0,m,m)\}.
\]

We prove both uniqueness and existence below.

## 1. The form of an internally stable set

For two distinct allocations (x,y), neither dominates the other **if and only if they share a coordinate**, meaning (x_i=y_i) for some (i\).

Indeed, if they share a coordinate, their other two coordinate differences have opposite signs, since their sums are equal. Neither allocation can therefore be strictly larger in two coordinates. If they share no coordinate, all three differences are nonzero and sum to zero. Two of them have the same sign, so one allocation dominates the other.

We next show that every nonempty internally stable set has one of the following forms:

* all its allocations have the same value of one fixed coordinate; or
* it consists of exactly three allocations, of the form
  \[
  (p+t,q,r),\qquad(p,q+t,r),\qquad(p,q,r+t),                 \tag{1}
  \]
  where (t\ne0) is an integer and all displayed coordinates are nonnegative.

For a set with at most one element, the first alternative holds. Otherwise choose distinct members (x,y\). They share exactly one coordinate: sharing two would make them equal. Relabel coordinates so that
\[
x=(a,b,c),\qquad y=(a,b+d,c-d),\qquad d\ne0.
\]
If all members have first coordinate (a\), we have the first alternative. Otherwise take a member (z) whose first coordinate differs from (a\). It must share a coordinate with each of (x,y\). Those agreements must use coordinates 2 and 3, one for each point. Interchanging coordinates 2 and 3 if needed, we may write
\[
z=(a+d,b,c-d).
\]

Any member (w) with first coordinate (a) must agree with (z) in coordinate 2 or 3. The sum condition then makes (w=x) or (w=y\). Any member with first coordinate different from (a) must agree with both (x) and (y) through coordinates 2 and 3. The only possibilities are
\[
z=(a+d,b,c-d),\qquad z'=(a-d,b+d,c).
\]
But (z,z') differ in all three coordinates, so they cannot both belong to an internally stable set. Thus the set is exactly \(\{x,y,z\}\). Taking
\[
p=a,\qquad q=b,\qquad r=c-d,\qquad t=d
\]
gives (1). In particular (p,q,r\ge0\), since they occur as coordinates of these allocations.

## 2. A stable set cannot have a coordinate fixed throughout

The empty set is not externally stable. Suppose a nonempty set (V) has, after relabeling players, (x_1=a) for every (x\in V\).

If (a<K\), choose any allocation (y) with (y_1=a+1\). It is outside (V\). A member (x\in V) could dominate (y) only by improving both coordinates 2 and 3. Since the coordinates are integers, this would require
\[
x_2+x_3\ge y_2+y_3+2=K-a+1,
\]
whereas (x_2+x_3=K-a\). Thus (y) is undominated, contrary to external stability.

If (a=K\), the only possible member is ((K,0,0)\), which does not dominate ((K-1,1,0)\). External stability again fails.

Consequently every stable set must be a three-point set (1).

## 3. Classifying the three-point candidates

Let (V) have form (1). The common allocation sum is
\[
K=p+q+r+t.
\]

### Case (t>0)

Every allocation (y) with (y_1\ge p\), (y_2\ge q\), and (y_3\ge r) is undominated by (V\): each member of (V) exceeds ((p,q,r)) in only one coordinate, so it cannot exceed (y) in two coordinates.

If (t\ge2\), the allocation
\[
y=(p+t-1,q+1,r)
\]
has sum (K\), satisfies those inequalities, and is not in (V\). Hence external stability fails.

If (t=1\), then (p+q+r=K-1\ge1\). By relabeling coordinates, assume (p\ge1\). Consider
\[
y=(p-1,q+1,r+1).
\]
It is a nonnegative allocation of sum (K) and is outside (V\). Every member of (V) has second coordinate at most (q+1) and third coordinate at most (r+1\). Therefore a member can exceed (y) only in coordinate 1, so none dominates (y\). This also contradicts external stability.

Thus no candidate with (t>0) is stable for (K\ge2\).

### Case (t=-s<0)

Here (s\ge1\), and the candidate is
\[
V=\{(p-s,q,r),(p,q-s,r),(p,q,r-s)\},                 \tag{2}
\]
with (p,q,r\ge s) and (K=p+q+r-s\).

Suppose (p>s\). Then
\[
y=(p-s-1,q+1,r)
\]
is a nonnegative allocation of sum (K) outside (2). Every member of (2) has second coordinate at most (q) and third coordinate at most (r\). None can therefore exceed (y) in either of those coordinates, so none dominates (y\). External stability fails.

The same argument, after permuting coordinates, rules out (q>s) and (r>s\). Consequently external stability forces
\[
p=q=r=s.
\]
It follows that (K=2s) and (2) is precisely
\[
\{(0,s,s),(s,0,s),(s,s,0)\}.
\]
This proves that odd (K) admits no stable set and that for even (K) the stated symmetric set is the only possible one.

## 4. Verifying existence for even (K)

Let (K=2m\), where (m\ge1\). Every pair of members of (V_m) shares a coordinate, so (V_m) is internally stable.

Take an allocation (y\notin V_m\). At least two coordinates of (y) are strictly less than (m\). Indeed, if two coordinates were at least (m\), their sum, together with the nonnegative third coordinate, could equal (2m) only if those two coordinates were exactly (m) and the third were zero. That would put (y) in (V_m\).

The member of (V_m) paying (m) to the two players whose shares in (y) are below (m) strictly improves both of their shares, and hence dominates (y\). Thus (V_m) is externally stable as well, completing the proof.
