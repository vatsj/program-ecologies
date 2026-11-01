"""Stable sets (kernels of the dominance digraph, via MILP) and chain ends in the hard band a > 2/3 of the pair-worth game. OH doc Theory tab section 3 (2026-11-01)."""
import sys,io,contextlib; sys.path.insert(0,'src')
with contextlib.redirect_stdout(io.StringIO()):
    import dominance_relations as d
from fractions import Fraction as F
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
def kernels(R,dom,maxn=6,obj=None):
    n=len(R); arcs=[(i,j) for i in range(n) for j in range(n) if i!=j and dom(R[i],R[j])]
    rows=[];lb=[];ub=[]
    A=lil_matrix((len(arcs)+n,n))
    for k,(i,j) in enumerate(arcs): A[k,i]=1;A[k,j]=1
    for j in range(n):
        A[len(arcs)+j,j]=1
        for (i,jj) in arcs:
            pass
    domby=[[] for _ in range(n)]
    for i,j in arcs: domby[j].append(i)
    for j in range(n):
        for i in domby[j]: A[len(arcs)+j,i]=1
    lo=np.r_[np.full(len(arcs),-np.inf),np.ones(n)]; hi=np.r_[np.ones(len(arcs)),np.full(n,np.inf)]
    cons=[LinearConstraint(A.tocsr(),lo,hi)]
    found=[]
    c=np.zeros(n) if obj is None else obj
    for _ in range(maxn):
        r=milp(c,constraints=cons,integrality=np.ones(n),bounds=Bounds(0,1))
        if r.status!=0: break
        S=[i for i in range(n) if r.x[i]>0.5]; found.append(S)
        cut=lil_matrix((1,n))
        for i in range(n): cut[0,i]= 1 if i in S else -1
        cons.append(LinearConstraint(cut.tocsr(),-np.inf,len(S)-1))
    return found
def outcomes(a,g):
    return d.outcomes(a,g)
def desc(R,S,a):
    pts=[R[i] for i in S]
    grand=[p for p in pts if sum(p)==1 and all(x>0 for x in p) or (sum(p)>a and min(p)==0 and False)]
    kinds={'grand(3 positive or sum>a)':0,'pair':0,'zero':0}
    for p in pts:
        if all(x==0 for x in p): kinds['zero']+=1
        elif sum(1 for x in p if x>0)==3 or sum(p)>a: kinds['grand(3 positive or sum>a)']+=1
        else: kinds['pair']+=1
    return len(pts),kinds,sorted(tuple(str(x) for x in p) for p in pts)[:6]
for a,g in [(F(3,4),12),(F(5,6),6),(F(5,6),12),(F(1),6)]:
    R=outcomes(a,g)
    for w in (False,True):
        ks=kernels(R,d.mkdom(a,w),maxn=4)
        cls=d.absorbing(R,d.mkdom(a,w))
        print(f"a={a} 1/{g} {'weak' if w else 'strict'} ({len(R)} outcomes): stable sets found {len(ks)}{' (search capped at 4)' if len(ks)==4 else ''}; chains end in {len(cls)} set(s) of sizes {sorted(len(c) for c in cls)}")
        for S in ks[:2]: print('   ',desc(R,S,a))
