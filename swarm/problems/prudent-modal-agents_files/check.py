#!/usr/bin/env python3
"""Reference checker for the prudent-modal-agents problem: the problem's own semantics in code.

Usage:  python3 check.py "B(a) & ~B(c)"

Syntax: atoms a, c, d (about the current opponent); constants T, F; ~ (not), & (and), | (or), -> (implies);
B(...) is the box (PA proves). Every atom must be inside some B(...). Precedence: ~ binds tightest, then &, then |,
then -> (right-associative); use parentheses freely.

Prints the formula's modal depth, its stabilized actions against CooperateBot (T), DefectBot (F), FairBot (B(a)) and
itself, FairBot's action against it, and whether it is prudent.
"""
import sys, re
from functools import lru_cache
sys.setrecursionlimit(100000)
TOK = re.compile(r"\s*(->|[()~&|]|B|[acdTF])")
def tokenize(s):
    out, i = [], 0
    s = s.strip()
    while i < len(s):
        m = TOK.match(s, i)
        if not m: raise SyntaxError(f"bad character at {i}: {s[i:i+10]!r}")
        out.append(m.group(1)); i = m.end()
        while i < len(s) and s[i].isspace(): i += 1
    return out
class P:
    def __init__(self, toks): self.t, self.i = toks, 0
    def peek(self): return self.t[self.i] if self.i < len(self.t) else None
    def eat(self, x=None):
        tok = self.peek()
        if x and tok != x: raise SyntaxError(f"expected {x}, got {tok}")
        self.i += 1; return tok
    def imp(self):
        l = self.orr()
        if self.peek() == "->": self.eat(); return ("or", ("not", l), self.imp())
        return l
    def orr(self):
        l = self.andd()
        while self.peek() == "|": self.eat(); l = ("or", l, self.andd())
        return l
    def andd(self):
        l = self.un()
        while self.peek() == "&": self.eat(); l = ("and", l, self.un())
        return l
    def un(self):
        tok = self.peek()
        if tok == "~": self.eat(); return ("not", self.un())
        if tok == "B": self.eat(); self.eat("("); f = self.imp(); self.eat(")"); return ("box", f)
        if tok == "(": self.eat(); f = self.imp(); self.eat(")"); return f
        if tok in ("a", "c", "d", "T", "F"): self.eat(); return (tok,)
        raise SyntaxError(f"unexpected {tok}")
def parse(s):
    p = P(tokenize(s)); f = p.imp()
    if p.peek() is not None: raise SyntaxError(f"trailing input at token {p.i}")
    return f
def depth(f):
    if f[0] == "box": return 1 + depth(f[1])
    return max([depth(g) for g in f[1:]], default=0)
def modalized(f, inside=False):
    if f[0] in ("a", "c", "d"): return inside
    if f[0] == "box": return modalized(f[1], True)
    return all(modalized(g, inside) for g in f[1:])
def outcomes(formula_text, worlds=None):
    X = parse(formula_text)
    if not modalized(X): raise ValueError("not fully modalized: every atom must be inside B(...)")
    agents = {"CB": ("T",), "DB": ("F",), "FB": ("box", ("a",)), "X": X}
    W = worlds or (6 * (depth(X) + 2) + 10)
    @lru_cache(maxsize=None)
    def act(x, y, n):                      # does agent x cooperate with agent y, at world n?
        return ev(agents[x], n, x, y)
    def ev(f, n, me, opp):
        t = f[0]
        if t == "T": return True
        if t == "F": return False
        if t == "a": return act(opp, me, n)
        if t == "c": return act(opp, "CB", n)
        if t == "d": return act(opp, "DB", n)
        if t == "not": return not ev(f[1], n, me, opp)
        if t == "and": return ev(f[1], n, me, opp) and ev(f[2], n, me, opp)
        if t == "or": return ev(f[1], n, me, opp) or ev(f[2], n, me, opp)
        if t == "box": return all(ev(f[1], m, me, opp) for m in range(n))
    res = {}
    for key, (x, y) in {"CB": ("X", "CB"), "DB": ("X", "DB"), "FB": ("X", "FB"), "X": ("X", "X"),
                        "FB_reply": ("FB", "X")}.items():
        seq = [act(x, y, n) for n in range(W)]
        tail = seq[W // 2:]
        if len(set(tail)) != 1: raise RuntimeError(f"no stable value for {x} against {y} within {W} worlds")
        res[key] = "C" if tail[-1] else "D"
    return depth(X), res
if __name__ == "__main__":
    if len(sys.argv) != 2: print(__doc__); sys.exit(2)
    d, r = outcomes(sys.argv[1])
    prudent = r["CB"] == "D" and r["DB"] == "D" and r["FB"] == "C" and r["FB_reply"] == "C" and r["X"] == "C"
    print(f"depth {d}; vs CooperateBot {r['CB']}, vs DefectBot {r['DB']}, vs FairBot {r['FB']} (FairBot replies "
          f"{r['FB_reply']}), vs itself {r['X']}; prudent: {'YES' if prudent else 'no'}")
