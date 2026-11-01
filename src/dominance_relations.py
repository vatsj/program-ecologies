"""Strict vs weak dominance: stable sets in the pair-worth-a game (a = 1/3, grids 1/6 and 1/12) and in majority division.
Static check behind the OH doc Theory tab, section 1 (2026-11-01). Run: python3 src/dominance_relations.py"""
from fractions import Fraction as F
import itertools
P=[(0,1),(0,2),(1,2)]
def outcomes(a,g,grand_any=True,pair_vals=None):
    q=[F(i,g) for i in range(g+1)]; out=set([(F(0),)*3])
    for x in itertools.product(q,repeat=3):
        if sum(x)<=1 and grand_any: out.add(x)
    for (i,j) in P:
        for x in q:
            for y in q:
                if x+y<=a and (pair_vals is None or (x,y) in pair_vals):
                    v=[F(0)]*3; v[i]=x; v[j]=y; out.add(tuple(v))
    return sorted(out)
def mkdom(a,weak):
    caps={(0,1):a,(0,2):a,(1,2):a,(0,1,2):F(1)}
    def dom(x,y):
        for S,c in caps.items():
            if sum(x[i] for i in S)>c: continue
            if weak:
                if all(x[i]>=y[i] for i in S) and any(x[i]>y[i] for i in S): return True
            elif all(x[i]>y[i] for i in S): return True
        return False
    return dom
def analyse(R,a,weak,label):
    dom=mkdom(a,weak)
    D={y:[x for x in R if dom(x,y)] for y in R}
    und=[y for y in R if not D[y]]
    core=[y for y in R if sum(y)==1 and all(y[i]+y[j]>=a for i,j in P)]
    ext=all(any(c in D[y] for c in und) for y in R if y not in und)
    print(f"{label} {'weak' if weak else 'strict'}: outcomes {len(R)}, undominated {len(und)}, core proper {len(core)}, undominated==core {set(und)==set(core)}, undominated externally stable (=> unique stable set) {ext}")
    return D,und
for g in (6,12):
    R=outcomes(F(1,3),g)
    for w in (False,True): analyse(R,F(1,3),w,f"a=1/3 grid 1/{g}")
# majority division as implemented: demands in {1/3,1/2,2/3}; grand only at thirds; pairs any compatible pair of demands
dem=[F(1,3),F(1,2),F(2,3)]
pv={(x,y) for x in dem for y in dem if x+y<=1}
R=sorted(set([(F(0),)*3,(F(1,3),)*3]+[v for v in outcomes(F(1),6,grand_any=False,pair_vals=pv)]))
for w in (False,True):
    D,und=analyse(R,F(1),w,"majority division")
# brute-force stable sets for majority division (20 outcomes) under each relation
def stable_sets(R,dom):
    res=[]
    n=len(R); idx={r:i for i,r in enumerate(R)}
    for k in range(1,5):
        for V in itertools.combinations(R,k):
            if any(dom(x,y) for x in V for y in V): continue
            if all(any(dom(x,z) for x in V) for z in R if z not in V): res.append(V)
    return res
for w in (False,True):
    ss=stable_sets(R,mkdom(F(1),w))
    print('majority division', 'weak' if w else 'strict', 'stable sets of size<=4:', [[tuple(int(6*t) for t in v) for v in V] for V in ss][:8], len(ss))
print('--- exhaustive, majority division')
for w in (False,True):
    dom=mkdom(F(1),w); n=len(R)
    by=[sum(1<<i for i in range(n) if dom(R[i],R[j])) for j in range(n)]   # dominators of j
    out=[sum(1<<j for j in range(n) if dom(R[i],R[j])) for i in range(n)]  # dominated by i
    found=[]
    full=(1<<n)-1
    for V in range(1,1<<n):
        cover=0; ok=True; m=V
        while m:
            i=(m&-m).bit_length()-1; m&=m-1
            if out[i]&V: ok=False;break
            cover|=out[i]
        if ok and (cover|V)==full: found.append(V)
    print('weak' if w else 'strict', len(found), [[tuple(int(6*t) for t in R[i]) for i in range(n) if V>>i&1] for V in found])

# --- Minimal sets closed under dominance (absorbing sets of the dominance digraph), 2026-11-01
def absorbing(R,dom):
    n=len(R); succ=[[j for j in range(n) if dom(R[j],R[i])] for i in range(n)]  # i -> j if j dominates i
    reach=[]
    for i in range(n):
        seen={i}; st=[i]
        while st:
            u=st.pop()
            for v in succ[u]:
                if v not in seen: seen.add(v); st.append(v)
        reach.append(seen)
    classes=[]
    for i in range(n):
        if all(i in reach[j] for j in reach[i]):  # i's reach set is strongly connected back to i => closed class
            c=frozenset(reach[i])
            if c not in classes: classes.append(c)
    return classes
def show(R,cls,scale):
    return [sorted(tuple(int(scale*t) for t in R[i]) for i in c) for c in cls]
R13=outcomes(F(1,3),6)
for w in (False,True):
    cls=absorbing(R13,mkdom(F(1,3),w))
    print('a=1/3 sixths', 'weak' if w else 'strict', 'absorbing sets:',len(cls),'sizes',sorted(len(c) for c in cls)[:5],'... union is core proper:', set(R13[i] for c in cls for i in c)=={y for y in R13 if sum(y)==1 and all(y[i]+y[j]>=F(1,3) for i,j in P)})
for w in (False,True):
    cls=absorbing(R,mkdom(F(1),w))
    print('majority division', 'weak' if w else 'strict', 'absorbing sets:', show(R,cls,6))
