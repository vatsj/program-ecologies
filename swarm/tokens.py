import json, os, re, sys, glob
def _objs(txt):
    dec=json.JSONDecoder(); i=0; out=[]
    while True:
        k=txt.find('{',i)
        if k<0: return out
        try: o,e=dec.raw_decode(txt,k); out.append(o); i=e
        except Exception: i=k+1
def claude(p):
    inp=out=0; usd=0.0
    for j in _objs(open(p).read()):
        if isinstance(j,dict) and j.get('type')=='result':
            u=j.get('usage',{}); inp+=u.get('input_tokens',0)+u.get('cache_creation_input_tokens',0)+u.get('cache_read_input_tokens',0)
            out+=u.get('output_tokens',0); usd+=j.get('total_cost_usd') or 0
    return dict(inp=inp,out=out,usd=round(usd,4))
def codex(p):
    inp=out=0
    for l in open(p):
        try: j=json.loads(l)
        except: continue
        if j.get('type')=='turn.completed':
            u=j['usage']; inp+=u.get('input_tokens',0); out+=u.get('output_tokens',0)+u.get('reasoning_output_tokens',0)
    return dict(inp=inp,out=out)
def gemini(p):
    inp=out=0
    for j in _objs(open(p).read()):
        if isinstance(j,dict) and 'stats' in j:
            for m,st in j['stats'].get('models',{}).items():
                t=st.get('tokens',{}); inp+=t.get('prompt',0); out+=t.get('candidates',0)+t.get('thoughts',0)
    return dict(inp=inp,out=out)
F={'opus':claude,'sol':codex,'argon':gemini}
def run_tokens(d):
    r={}
    for m,f in F.items():
        p=os.path.join(d,f'{m}.out')
        if os.path.exists(p): r[m]=f(p)
    return r
if __name__=='__main__':
    base=sys.argv[1]
    for d in sorted(glob.glob(base+'/*/')):
        print(os.path.basename(d.rstrip('/')), run_tokens(d))
