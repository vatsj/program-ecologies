"""Tests for certificates as genes (notes/certificates-as-genes.md §1.12)."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.setrecursionlimit(1000000)

import lt_code as L
import lt_cert as C
import lt_genes as G

K = 10 ** 6
V = K // 4
PC = K // 4
CAT = G.named_catalogue(K, V)


def run(xn, xm, yn, ym, E=3, xstart='mode', ystart='mode', cat=CAT, K=K, V=V, P=PC, alloc='post', rule='lack', ac='full'):
    x = G.make_prog(cat, xn, xm, xstart)
    y = G.make_prog(cat, yn, ym, ystart)
    hist = []
    for _ in range(E):
        r = G.encounter(x, y, K, V, P, alloc=alloc, rule=rule, ac=ac)
        hist.append(r)
        x, y = r['nx'], r['ny']
    return hist, x, y


def test_adoption_after_passed_check():
    hist, x, y = run('CB', 'C', 'CB', 'H')
    assert (hist[0]['ax'], hist[0]['ay']) == ('D', 'D')
    assert [(a, how) for a, s, how in hist[0]['accx'].adopted] == [('C', 'copy'), ('D', 'copy')]
    assert x.cseq == CAT['CB'][1] and x.dseq == CAT['CB'][2]
    assert (hist[1]['ax'], hist[1]['ay']) == ('C', 'C')
    # nothing left to copy at steady state: production costs nothing
    assert hist[2]['accx'].total() == 0
    # the adoption check itself is a sound check of x_s against the donor
    xs = G.make_prog(CAT, 'CB', 'C', 'empty').single('C', CAT['CB'][1][0])
    v, n = G.check_term(xs.term(), G.make_prog(CAT, 'CB', 'H').term(), 'C', V, K, K)
    assert v == 'T' and n <= V + 6


def test_two_empty_copiers_never_bootstrap():
    hist, x, y = run('CB', 'C', 'CB', 'C', E=4)
    assert all((h['ax'], h['ay']) == ('D', 'D') for h in hist)
    assert x.cseq == () and y.cseq == ()


def test_refusal_across_skeletons_and_copied_faker():
    hist, x, y = run('CB', 'C', 'CB1', 'H', E=3)
    assert x.cseq == () and len(x.dseq) == 1              # δ fits CB, CB1's C script does not
    assert all((h['ax'], h['ay']) == ('D', 'D') for h in hist)
    for donor in ('CB', 'CB1', 'CBP', 'Cc', 'LobC', 'CBmut', 'Dcert', 'CBsloppy'):
        hist, x, y = run('CF', 'C', donor, 'H', E=2)
        assert x.cseq == (), donor                          # CF never adopts a C script (Theorem S^cert)
        assert all(h['ax'] == 'D' for h in hist)
    hist, x, y = run('CF', 'C', 'Dc', 'H', E=1)
    assert x.dseq == CAT['Dc'][2]                           # a true D script is adopted


def test_lemma_A_F1_list_mutation_invalidates_an_adopted_script():
    """LöbC in mode C adopts σCB (Hyp^self) and δ (valid on the single-entry quote); in the adopted object δ is
    invalid because LöbC' now cooperates with ⌜D⌝ (notes §1.5 F1).  Soundness: the check of the D claim is F."""
    hist, x, y = run('LobC', 'C', 'CB', 'H', E=1, ac='full')
    assert len(x.cseq) == 1 and len(x.dseq) == 0              # the full-quote check refuses δ (notes §1.15)
    hist, x, y = run('LobC', 'C', 'CB', 'H', E=1, ac='single')
    assert len(x.cseq) == 1 and len(x.dseq) == 1
    xd = x.single('D', x.dseq[0])
    v1, _ = G.check_term(xd.term(), L.PROG_D, 'D', V, K, K)
    v2, _ = G.check_term(x.term(), L.PROG_D, 'D', V, K, K)
    assert v1 == 'T' and v2 == 'F'
    a, _ = L.play(x.term(), L.PROG_D, K)
    assert a == 'C'                                         # the truth the F check reports
    # positive case of A1: CB's σCB stays valid when an unrelated entry is appended
    cb = G.make_prog(CAT, 'CB', 'C', 'host')
    extra = CAT['CBP'][1][0]
    cb2 = cb.with_list(cb.cseq + (extra,), cb.dseq)
    yh = G.make_prog(CAT, 'CB', 'H').term()
    assert G.check_term(cb.term(), yh, 'C', V, K, K)[0] == 'T'
    assert G.check_term(cb2.term(), yh, 'C', V, K, K)[0] == 'T'


def test_lemma_A_F0_preplay_production_timeout():
    """Pre-play allocation: y accepts x's σCB (an atom about x's fuel-K run) and x's production eats the fuel, so
    x's actual play times out: y is exploited.  The post-play allocation (main) has x cooperate."""
    V2, K2 = 25000, 25012
    cat = G.named_catalogue(K2, V2)
    cb = cat['CB']
    x = G.Prog('CB', cb[0], 'S', cb[1], ())                 # holds σCB, lacks a D script: the D production runs
    y = G.Prog('CB', cb[0], 'H', cb[1], cb[2])
    r = G.encounter(x, y, K2, V2, K2, alloc='pre', rule='gate')
    assert r['ay'] == 'C' and r['ax'] == 'D' and r['botx']  # accepted, then timed out (gate + D production)
    v, _ = G.check_term(x.term(), y.term(), 'C', V2, K2, K2)
    assert v == 'T'                                          # the certificate y accepted
    r = G.encounter(x, y, K2, V2, K2, alloc='post', rule='gate')
    assert (r['ax'], r['ay']) == ('C', 'C')


def test_search_producer_within_cap_and_term_equals_host():
    prod, pr = G.probes(K, V)
    for nm in ('CB', 'CB1', 'CBP', 'LobC', 'Cc', 'Dc', 'CBPr', 'CBdef'):
        x = G.make_prog(CAT, nm, 'S', 'empty')
        for y, a in ((G.make_prog(CAT, 'CB', 'H').term(), 'C'), (L.PROG_D, 'D')):
            s, n, oc = G.produce_term(x.term(), y, a, V, K, PC, K)
            assert s == prod.produce(0, x.term(), y, a, K, V), (nm, a)
            assert n <= PC + 5
    x = G.make_prog(CAT, 'CBP', 'S', 'empty')
    y = G.make_prog(CAT, 'CB', 'H').term()
    s, n, oc = G.produce_term(x.term(), y, 'C', V, K, 10000, K)   # a cap below the tactic's cost
    assert s is None and oc == "capTO" and n <= 10000 + 5
    # an S program adopts what it produces; it is used from the next encounter
    hist, x, y = run('CB', 'S', 'CB1', 'H', E=2)
    assert [(a, how) for a, s, how in hist[0]['accx'].adopted] == [('C', 'search'), ('D', 'search')]
    assert (hist[1]['ax'], hist[1]['ay']) == ('C', 'C')
    assert set(x.anc) == {'search'}


def test_ancestry_and_cost_accounting():
    hist, x, y = run('CB', 'CS', 'CB', 'H', E=2, rule='lack')
    assert set(x.anc) == {'host'} and hist[1]['accx'].total() == 0      # 'lack': nothing to do once both are held
    hist, x, y = run('CB', 'CS', 'CB', 'H', E=2, rule='gate')
    assert set(x.anc) == {'host'}                           # copied from an H donor
    acc = hist[0]['accx']
    assert acc.total() == sum(acc.steps.values()) > 0
    ev = {k: n for k, v, n, d in acc.events}
    assert acc.steps['ac'] == sum(n for k, v, n, d in acc.events if k == 'ac')
    assert acc.steps['gate'] == sum(n for k, v, n, d in acc.events if k == 'gate') and 'gate' in ev
    assert all(n <= V + 6 for k, v, n, d in acc.events if k in ('ac', 'gate'))
    # steady state of a CS copier: the gate check every encounter, no production
    acc2 = hist[1]['accx']
    assert acc2.steps['prodC'] == 0 and acc2.steps['gate'] > 0
    # a copy from a search-produced donor carries the search tag
    _, s_, _ = run('CB', 'S', 'CB', 'H', E=1)
    yS = s_
    xC = G.make_prog(CAT, 'CB', 'C', 'empty')
    r = G.encounter(xC, yS, K, V, PC)
    assert r['nx'].cseq and set(r['nx'].anc) == {'search'}


def test_full_quote_check_lets_a_prudent_copier_adopt():
    """CBP copying CBPh's script: the single-entry quote lacks the copier's D script, which the donor's partner
    validation reads, so it is refused forever; the would-be self carries it from encounter 2 on (notes §1.15)."""
    hist, x, y = run('CBP', 'C', 'CBPh', 'H', E=3, ac='single')
    assert x.cseq == () and all(h['ax'] == 'D' for h in hist)
    hist, x, y = run('CBP', 'C', 'CBPh', 'H', E=3, ac='full')
    assert x.cseq and (hist[2]['ax'], hist[2]['ay']) == ('C', 'C')


def test_transfer_graph_sample():
    """Same skeleton: an edge; a different skeleton: no C edge; LöbC accepts CB's script (Hyp^self)."""
    def c_edge(xn, yn):
        _, x, _ = run(xn, 'C', yn, 'H', E=1)
        return bool(x.cseq)
    assert c_edge('CB', 'CBlet') and c_edge('CBlet', 'CB') and c_edge('CB', 'MC1') and c_edge('CB1', 'CB1r')
    assert not c_edge('CB', 'CB1') and not c_edge('CB1', 'CB') and not c_edge('CBP', 'CB') and not c_edge('CBP', 'CBPr')
    assert c_edge('LobC', 'CB')
