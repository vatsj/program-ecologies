# Vickrey-nearest point vs. centroid of the minimum-revenue face (three winners)

Write $P=v_P$. Sort the winners' values as $v_1\le v_2\le v_3$ (a relabelling of $v_A,v_B,v_C$). Assume $P>0$, all $v_i>0$, and $v_1+v_2+v_3>P$. If some $v_i=0$, then $F$ degenerates to a segment or a point, and "centroid" should be read as its midpoint or the point itself.

## Answer

The Vickrey-nearest point equals the centroid of $F$ **if and only if at least one of these holds:**

1. $v_P \le \min(v_A,v_B,v_C)$. In this case $F$ is the whole triangle $\{p\ge 0,\ \sum p=v_P\}$, $p^{VCG}=0$, and both points equal $(v_P/3)(1,1,1)$.
2. $v_P \ge$ the sum of the two largest values, i.e. $v_P\ge v_2+v_3$. Equivalently, every $v_i\ge s:=v_A+v_B+v_C-v_P$. Then $F$ is the triangle $\{y\ge0,\ \sum y=s\}$ in the coordinates $y=v-p$, and both points equal $p_i=v_i-s/3$.
3. $v_A=v_B=v_C$, by symmetry.

In every other case the two points differ. Cases 1 and 2 are exactly the cases where $F$ is a full (uncut) triangle. Otherwise $F$ is a quadrilateral, pentagon or hexagon, and only the fully symmetric profile makes the two points agree.

## Proof

### Step 0: describing $F$
The constraint for $T=\{A,B,C\}$ gives $\sum p_i\ge P$.

Take any $p$ with $0\le p\le v$ and $\sum p=P$. Such a $p$ exists because $P<\sum v$. For every $T$:
$$\sum_{T}p_i = P-\sum_{j\notin T}p_j\ \ge\ P-\sum_{j\notin T}v_j,$$
and $\sum_T p_i\ge 0$. So $p$ is in the core. Hence $R=v_P$ and
$$F=\{p:\ \textstyle\sum p_i=P,\ 0\le p_i\le v_i\}.$$
This is the plane slice of a box. Write $c=p^{VCG}$, with $c_i=\max(0,P-v_j-v_k)=\max(0,v_i-s)$.

### Key lemma
Let $G$ be the centroid of $F$ and $H=\{\sum p=P\}$. Then
$$\text{VN}=G \iff G-c\ \parallel\ (1,1,1) \iff G_i-c_i \text{ is the same for } i=A,B,C.$$

Proof: $(1,1,1)$ is normal to $H$.
- If $G-c\parallel(1,1,1)$, then $G$ is the orthogonal projection of $c$ onto $H$. Since $G\in F\subset H$, $G$ is the closest point of $F$ to $c$, so $G=$ VN.
- Conversely, suppose $G=$ VN. $G$ lies in the relative interior of the 2-dimensional polygon $F$. The nearest-point optimality condition at a relative-interior point forces $c-G\perp H$.

### Lemma (centroid of a triangle with disjoint corners cut off)
Let $\Delta_L=\{x\ge0,\ \sum x=L\}$. Remove the corner triangles $\{x_i>L-b_i\}$, where $b_i\in[0,L)$ and $b_i+b_j\le L$, so the corners are disjoint.

The corner at vertex $i$ has area proportional to $b_i^2$. Its centroid has $i$-coordinate $L-2b_i/3$ and the other two coordinates $b_i/3$. The full triangle has area proportional to $L^2$ and centroid $(L/3)(1,1,1)$. Put $Q=\sum b^2$ and $C=\sum b^3$. Subtracting moments gives
$$G_i\,(L^2-Q)=\tfrac{L^3}{3}-Lb_i^2+b_i^3-\tfrac{C}{3},\qquad\text{so}\qquad G_i-G_j=\frac{h(b_i)-h(b_j)}{L^2-Q},\quad h(b)=b^3-Lb^2 .$$

### Sufficiency
- **Case 1.** $c=0$. Here $F=\Delta_P$, so $G=(P/3)\mathbf 1$ and $G-c\parallel\mathbf 1$.
- **Case 2.** In $y=v-p$ coordinates, $F=\{\sum y=s,\ 0\le y_i\le v_i\}=\Delta_s$ because $v_i\ge s$. So $G_y=(s/3)\mathbf 1$. Also $c_i=v_i-s$, i.e. $c_y=s\mathbf 1$. The difference is parallel to $\mathbf 1$.
- **Case 3.** $F$ and $c$ are invariant under every permutation of the coordinates, so $G-c$ is a symmetric vector, i.e. a multiple of $\mathbf 1$.

### Necessity
Assume none of 1–3 holds, i.e. $v_1<P<v_2+v_3$ and the $v_i$ are not all equal. We show that $G-c\not\parallel\mathbf 1$.

**Case A: $P\le v_1+v_2$.** Then every $c_i=0$, and $F$ is $\Delta_P$ with corners $b_i=(P-v_i)^+$ removed. These are disjoint because $b_i+b_j\le P \iff P\le v_i+v_j$. By the lemma, $G\parallel\mathbf 1$ iff $h(b_i)$ is the same for all $i$. Note $h(b_i)=-g(v_i)$, where
$$g(v)=v\,\big((P-v)^+\big)^2 .$$
- If some $v_i\ge P$, then $g(v_i)=0$, so all $g$ values are $0$, all $v_j\ge P$, and we are in Case 1. Contradiction.
- Otherwise all $v_i<P$. On $(0,P)$, $g$ increases on $(0,P/3]$ and decreases on $[P/3,P)$. For equal $g$ values with the $v$'s not all equal, we would need $v_1<P/3<v_2=v_3$. But $v_2\ge P-v_1>2P/3$, so
$$g(v_2)\le g(P-v_1)=(P-v_1)v_1^2<v_1(P-v_1)^2=g(v_1),$$
using $g(x)-g(P-x)=x(P-x)(P-2x)>0$ for $x<P/2$. Contradiction.

**Case B1: $v_1+v_2<P<v_3$.** Here $c=(0,0,P-v_1-v_2)$. The cap $p_3\le v_3$ never binds, so $F$ is the rectangle $[0,v_1]\times[0,v_2]$ (with $p_3=P-p_1-p_2>0$). Its centroid is $G=(v_1/2,\ v_2/2,\ P-(v_1+v_2)/2)$, so
$$G-c=\big(v_1/2,\ v_2/2,\ (v_1+v_2)/2\big).$$
This is parallel to $\mathbf 1$ only if $v_1=v_2=v_1+v_2$, i.e. $v_1=v_2=0$. Impossible.

**Case B2/B3: $v_1+v_2<P$ and $v_3\le P$** (and $P<v_2+v_3$). Work in $y=v-p$ coordinates:
$$F=\Delta_s\setminus\{\text{corners } a_i=(s-v_i)^+\}.$$
The corners are disjoint because $a_i+a_j\le s \iff P\ge v_k$. In these coordinates $c_y=v-c=\min(v,s)=s\mathbf 1-a$, so the condition is
$$G_{y,i}-G_{y,j}=-(a_i-a_j)\quad\text{for all } i,j.$$
By the lemma, for a pair with $a_i\ne a_j$ this condition reduces to
$$s^2-s(a_i+a_j)+a_ia_j+a_i^2+a_j^2-Q=0 \iff (s-a_i)(s-a_j)=a_k^2,$$
that is, $\min(v_i,s)\min(v_j,s)=a_k^2$. Here $a_3=(v_1+v_2-P)^+=0$, $a_1=v_2+v_3-P>0$ and $a_2=(v_1+v_3-P)^+$.
- **B3: $P\ge v_1+v_3$.** Then $a_2=0\ne a_1$. The pair $(1,2)$ needs $\min(v_1,s)\min(v_2,s)=a_3^2=0$. Impossible.
- **B2 with $v_1<v_2$.** Then $a_1-a_2=v_2-v_1\ne0$. The pair $(1,2)$ again needs $\min(v_1,s)\min(v_2,s)=0$. Impossible.
- **B2 with $v_1=v_2=x$.** Then $a_1=a_2=s-x>0=a_3$. The pair $(1,3)$ needs $x\cdot s=(s-x)^2$, i.e. $s=\tfrac{3\pm\sqrt5}{2}x$. But $x<s\le 2x$, because $s=2x+v_3-P$ and $P\ge v_3$, $P<x+v_3$. Neither root lies in $(x,2x]$. Impossible.

These cases cover every non-triangle profile: $v_1<P<v_2+v_3$ and either $P\le v_1+v_2$ (A), or $P>v_1+v_2$ with $P<v_3$ (B1) or $P\ge v_3$ (B2/B3). $\blacksquare$

Remark: the two-winner fact in the problem is the one-dimensional analogue. There $F$ is a segment, and $G-c\parallel(1,1)$ holds automatically when no cap binds.

## Alternative unified proof (from argon; checked by opus)
Let $D=v_P-\sum_i c_i>0$ and $z=(p-c)/D$. On $F$ we have $p_i=P-p_j-p_k\ge P-v_j-v_k$ and $p_i\ge 0$, so $p\ge c$. Hence
$$F_z=\{z\in\Delta:\ z_i\le w_i\},\qquad \Delta=\{z\ge0,\ \textstyle\sum z=1\},\qquad w_i=\min(v_i,s)/D .$$
The VCG point becomes $z=0$.

**The corners never overlap.** The corner cut at vertex $i$ has side $\lambda_i=\max(0,1-w_i)$. Because $w_i+w_j-1=(s-\min(v_k,s))/D\ge0$, we get $\lambda_i+\lambda_j\le1$. Order $\lambda_1\ge\lambda_2\ge\lambda_3$; then $\lambda_2,\lambda_3\le 1/2$.

**Vickrey-nearest point.** It is the projection of $0$. Caps 2 and 3 never bind, which gives
$$z_1=\min(1/3,\ 1-\lambda_1),\qquad z_2=z_3=\max(1/3,\ \lambda_1/2).$$

**Centroid.** By the corner-cutting moment computation,
$$G_{z,i}=\frac13-\frac{\alpha_i-\bar\alpha}{1-\sum_m\lambda_m^2},\qquad \alpha_i=\lambda_i^2(1-\lambda_i),$$
where $\bar\alpha$ is the mean of the $\alpha_m$.

**Comparison.**
- If $\lambda_1>2/3$, the Vickrey-nearest point lies on the boundary edge $z_1=1-\lambda_1$, while the centroid is in the relative interior. They differ.
- Otherwise the Vickrey-nearest point is $(1/3)\mathbf 1$. It equals the centroid iff $\alpha_1=\alpha_2=\alpha_3$. Since $t^2(1-t)$ is strictly increasing on $[0,2/3]$, this holds iff $\lambda_1=\lambda_2=\lambda_3$.

**Back to the condition.** Suppose $\lambda_A=\lambda_B=\lambda_C$.
- If all $\lambda_i=0$, then $w_i\ge 1$ for all $i$, i.e. $\min(v_i,s)\ge D=\sum_m\min(v_m,s)-s$. Summing any two gives $\min(v_j,s)+\min(v_k,s)\le s$, which means $v_j+v_k\le s$, i.e. $v_P\le v_i$ for all $i$ (condition 1).
- If the common value is positive, then $w_A=w_B=w_C<1$, so $\min(v_A,s)=\min(v_B,s)=\min(v_C,s)$. Either some $v_i\ge s$, which forces all $v_j\ge s$ (condition 2, where $D=2s$, $w_i=1/2$, and $\lambda_A=\lambda_B=\lambda_C=1/2$, leaving the medial triangle of $\Delta$), or all $v_i<s$ and hence $v_A=v_B=v_C$ (condition 3).

Conversely, each of conditions 1–3 makes the $\lambda_i$ equal: in 1 they are all $0$, in 2 they are all $1/2$, and in 3 they are equal by symmetry. This equivalence was also checked numerically on 50,000 random profiles with no mismatch. So:

> **VN = centroid $\iff$ $\lambda_A=\lambda_B=\lambda_C$, where $\lambda_i=\max\big(0,\ 1-\min(v_i,s)/(v_P-\sum_j c_j)\big)$, which is equivalent to conditions 1–3 above.**

## Worked examples
(All numbers below were computed with exact rational arithmetic in `/work/opus/c.py`.)

**Example 1 (they differ).** $v_A=1,\ v_B=v_C=10,\ v_P=3$, so $s=18$.
- VCG: $c=(0,0,0)$.
- $F=\{p_A+p_B+p_C=3,\ 0\le p_A\le1,\ p_B,p_C\ge0\}$ is the trapezoid with vertices $(0,3,0),(0,0,3),(1,2,0),(1,0,2)$.
- **Vickrey-nearest:** $(1,1,1)$, the projection of $0$ onto the plane, which lies in $F$.
- **Centroid:** $(7/15,\ 19/15,\ 19/15)$. Check: the full triangle has area weight $9$ and centroid $(1,1,1)$. The removed corner $p_A>1$ has weight $4$ and centroid $(5/3,2/3,2/3)$. So $G_A=(9\cdot1-4\cdot5/3)/5=7/15$.

The points differ: the Vickrey-nearest rule charges A, the low-value bidder, $1$, its full value, while the centroid charges it $7/15$.

**Example 2 (they differ, VCG nonzero).** $v=(2,3,10),\ v_P=8$ (Case B1).
- VCG: $c=(0,0,3)$.
- $F$ is the rectangle $p_A\in[0,2]$, $p_B\in[0,3]$, $p_C=8-p_A-p_B$.
- **Vickrey-nearest:** $c+\tfrac53\mathbf 1=(5/3,\ 5/3,\ 14/3)$.
- **Centroid:** $(1,\ 3/2,\ 11/2)$.

**Example 3 (they agree, symmetric).** $v=(4,4,4),\ v_P=7$. $F$ is a hexagon, and both points equal $(7/3,7/3,7/3)$.

**Example 4 (they agree, Case 2).** $v=(5,6,7),\ v_P=14$, so $s=4\le\min v$.
- VCG: $c=(1,2,3)$.
- $F$ is a triangle, and both points equal $c+\tfrac{14-6}{3}\mathbf 1=(11/3,\ 14/3,\ 17/3)$.

## Numerical check
Exact rational experiments over about 200,000 random profiles, including half-integer $v_P$ and ties, matched the condition "1 or 2 or 3" with no exceptions. Sympy region-by-region symbolic formulas (`/work/opus/sym.py`) agree as well.
