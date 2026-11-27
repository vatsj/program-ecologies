"""Two 2x3 examples on independence of irrelevant alternatives: the leader-value core and program equilibrium
(strong Nash in program space, beta end) under removal of a base action never played in an acceptable outcome.
PROOFS P5, remark of 2026-11-27."""
import itertools
def lvc(U, A1, A2):
    # leader value core, NTU, 2 players, pure; followers best-respond (ties: report both pess/opt)
    def lead1(pess):
        best=None
        for a in A1:
            m=max(U[a,b][1] for b in A2); r=[U[a,b][0] for b in A2 if U[a,b][1]==m]
            v=min(r) if pess else max(r); best=v if best is None else max(best,v)
        return best
    def lead2(pess):
        best=None
        for b in A2:
            m=max(U[a,b][0] for a in A1); r=[U[a,b][1] for a in A1 if U[a,b][0]==m]
            v=min(r) if pess else max(r); best=v if best is None else max(best,v)
        return best
    out={}
    for pess in (True,False):
        v1,v2=lead1(pess),lead2(pess); core=[]
        for a in A1:
            for b in A2:
                x=U[a,b]
                if v1>x[0] or v2>x[1]: continue
                if any(U[c,d][0]>x[0] and U[c,d][1]>x[1] for c in A1 for d in A2): continue
                core.append((a,b))
        out['pess' if pess else 'opt']=(v1,v2,core)
    return out
def beta(U,A1,A2):
    # outcomes supportable as strong Nash in program space when punishers respond to the deviator's action (beta end)
    res=[]
    for a in A1:
        for b in A2:
            x=U[a,b]
            d1=all(any(U[c,d][0]<=x[0] for d in A2) for c in A1)   # every deviation c of 1 has a punishment d
            d2=all(any(U[c,d][1]<=x[1] for c in A1) for d in A2)
            par=any(U[c,d][0]>x[0] and U[c,d][1]>x[1] for c in A1 for d in A2)
            if d1 and d2 and not par: res.append((a,b))
    return res
U={('P','Acc'):(2,3),('P','C'):(0,0),('P','F'):(0.5,-1),('A','Acc'):(3,0),('A','C'):(2.5,2.5),('A','F'):(0,3)}
print('G   LVC',lvc(U,['P','A'],['Acc','C','F'])); print('G-  LVC',lvc(U,['P','A'],['Acc','C']))
print('G   prog',beta(U,['P','A'],['Acc','C','F'])); 
U2=dict(U); U2['P','F']=(-5,-5); U2['A','F']=(-5,-5)
print('burn G  prog',beta(U2,['P','A'],['Acc','C','F']),' G- prog',beta(U2,['P','A'],['Acc','C']))
print('burn G  LVC',lvc(U2,['P','A'],['Acc','C','F'])['pess'],' G- LVC',lvc(U2,['P','A'],['Acc','C'])['pess'])
