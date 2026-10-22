import json, os, re, sys, glob
def _objs(txt):
    dec=json.JSONDecoder(); i=0; out=[]
    while True:
        k=txt.find('{',i)
        if k<0: return out
        try: o,e=dec.raw_decode(txt,k); out.append(o); i=e
        except Exception: i=k+1
def claude(p):
    """Sum usage over completed invocations (result lines) plus the calls of an unfinished one (assistant events)."""
    inp=out=0; usd=0.0; pending={}
    for j in _objs(open(p).read()):
        if not isinstance(j,dict): continue
        if j.get('type')=='result':
            u=j.get('usage',{}); inp+=u.get('input_tokens',0)+u.get('cache_creation_input_tokens',0)+u.get('cache_read_input_tokens',0)
            out+=u.get('output_tokens',0); usd+=j.get('total_cost_usd') or 0; pending={}
        elif j.get('type')=='assistant' and isinstance(j.get('message'),dict):
            m=j['message']; u=m.get('usage') or {}
            pending[m.get('id')]=(u.get('input_tokens',0)+u.get('cache_creation_input_tokens',0)+u.get('cache_read_input_tokens',0), u.get('output_tokens',0))
    for a,b in pending.values(): inp+=a; out+=b
    return dict(inp=inp,out=out,usd=round(usd,4),partial=bool(pending))
def codex(p):
    inp=out=0
    for l in open(p):
        try: j=json.loads(l)
        except: continue
        if j.get('type')=='turn.completed':
            u=j['usage']; inp+=u.get('input_tokens',0); out+=u.get('output_tokens',0)+u.get('reasoning_output_tokens',0)
    return dict(inp=inp,out=out)
def gemini(p):
    """stream-json: usage only in 'result' events; an invocation killed before its result is lost (flagged)."""
    inp=out=0; inits=results=0
    for j in _objs(open(p).read()):
        if not isinstance(j,dict): continue
        if j.get('type')=='init': inits+=1
        if j.get('type')=='result' or 'stats' in j:
            results+=1; st=j.get('stats',{})
            if 'input_tokens' in st: inp+=st.get('input_tokens',0); out+=st.get('output_tokens',0)
            else:
                for m,ms in st.get('models',{}).items():
                    t=ms.get('tokens',{}); inp+=t.get('prompt',0); out+=t.get('candidates',0)+t.get('thoughts',0)
    return dict(inp=inp,out=out,lost_invocations=max(inits-results,0))
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
