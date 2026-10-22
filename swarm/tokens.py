import json, os, re, sys, glob
def claude(p):
    try:
        j=json.loads(open(p).read().strip().splitlines()[-1]); u=j.get('usage',{})
        return dict(inp=u.get('input_tokens',0)+u.get('cache_creation_input_tokens',0)+u.get('cache_read_input_tokens',0), out=u.get('output_tokens',0), usd=j.get('total_cost_usd'))
    except Exception as e: return dict(err=str(e)[:60])
def codex(p):
    inp=out=0
    for l in open(p):
        try: j=json.loads(l)
        except: continue
        if j.get('type')=='turn.completed':
            u=j['usage']; inp+=u.get('input_tokens',0); out+=u.get('output_tokens',0)+u.get('reasoning_output_tokens',0)
    return dict(inp=inp,out=out)
def gemini(p):
    try:
        txt=open(p).read(); j=json.loads(txt[txt.index('{'):])
        inp=out=0
        for m,s in j.get('stats',{}).get('models',{}).items():
            t=s.get('tokens',{}); inp+=t.get('prompt',0); out+=t.get('candidates',0)+t.get('thoughts',0)
        return dict(inp=inp,out=out)
    except Exception as e: return dict(err=str(e)[:60])
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
