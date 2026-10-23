# vNM stable sets of three-player majority divide-the-dollar on a finite grid: literature check

Date: 2026-10-22. Method: web search only (about 12 queries), plus a small independent computation to test the claim. Full texts of several paywalled papers (Bott 1953, Lucas handbook chapter, Anesi, Harsanyi) were not accessible; statements about them rest on abstracts and secondary sources and are marked as such.

## Verdict: not found

I found no source that treats the three-player majority game restricted to a grid of multiples of 1/k, and none that states uniqueness (or non-uniqueness, or non-existence) of the stable set for any k. The nearest literature is the continuum theory (vNM 1944, Bott 1953, Shapley's discriminatory solutions, Lucas's handbook chapter) and abstract-game results about finite digraphs (Richardson). The grid claim is therefore "not found in the literature I could reach", not "refuted". An absence of search hits is weak evidence that it is unpublished; a paper in the older (1950s to 1990s) cooperative-game literature could have it without being indexed by these queries.

## Independent check I ran (not from the literature)

Setup: imputations (a,b,c) with a+b+c = k, nonnegative integers; x dominates y via a pair {i,j} iff x_i > y_i and x_j > y_j (strict, both) and x_i + x_j <= k (always true); singletons cannot dominate (v = 0); the grand coalition cannot dominate. Exhaustive subset search for k = 3, 4, 5 and a backtracking kernel search for k = 2..9:

| k | stable sets found |
|---|---|
| 2, 4, 6, 8 | exactly one: {(0,k/2,k/2), (k/2,0,k/2), (k/2,k/2,0)} |
| 3, 5, 7, 9 | none |

So under this definition, for odd k there is no stable set at all, and uniqueness of the symmetric-type set holds at least for even k <= 8. This matters if our computations reported a set "for all k"; check that the odd-k cells were not handled by an ad hoc grid (for example a set of the near-halving points (m, m+1, 0)), which is not stable under the definition above.

Why the discriminatory sets disappear on the grid (hand derivation, consistent with the computation): in the continuum V_c = {(c, t, 1-c-t)} with c < 1/2 is externally stable because any y with y_1 > c is beaten by some (c, t, 1-c-t) with t > y_2 and 1-c-t > y_3, which needs y_1 > c. On the grid the same argument needs y_1 >= c + 2/k. A point with y_1 = c + 1/k is neither in V_c nor dominated by it. The boundary layer one grid step wide kills external stability, and filling it in with extra points creates internal conflicts (the computation shows no completion exists for k <= 9).

## Sources

1. Jordan, "Majority rule with dollar voting", Review of Economic Design 6 (2001), 343-352. https://pure.psu.edu/en/publications/majority-rule-with-dollar-voting/ . A different game (voting weight equals payoff, any n); abstract says the stable set consists of allocations where one player holds half, or wealth is split equally among a power-of-two number of players. Shows that stable-set uniqueness results for majority-type dividing games exist in the continuum; nothing on discreteness (the abstract does not mention it).

2. Lecture notes, IISc game theory lab, chapter on other topics. https://gtl.csa.iisc.ac.in/gametheory/ln/web-cp6-othertopics.pdf . Textbook statement of the symmetric stable set {(150,150,0) and permutations} for the three-player majority game; no uniqueness or grid discussion. Only a pedagogical source.

3. Lucas, 1968 ten-player game with no stable set (Pacific J. Math. 1969 write-up; RAND memo 1967), see https://msp.org/pjm/1969/28-3/p12.xhtml and https://apps.dtic.mil/sti/pdfs/ADA066730.pdf (the DTIC item is a report on discriminatory vNM solutions of simple games; I confirmed only its topic from a snippet). Shows non-existence is possible in general; Lucas and Rabie (Math. Oper. Res. 7 (1982), https://pubsonline.informs.org/doi/10.1287/moor.7.4.491) give games with no stable set and empty core. Relevance: non-existence at odd k in our check is of a different (tiny, explicit) kind, a cyclic finite dominance digraph, not Lucas's construction.

4. Chang, "Discriminatory stable sets for (n,k) games", Proc. AMS 97 (1986). https://www.ams.org/proc/1986-097-04/S0002-9939-1986-0845991-2/ (page returned 403; known only from the search listing). Continuum discriminatory solutions for symmetric majority (n,k) games. No grid version known to me from it.

5. Bott, "Symmetric solutions to majority games", Contributions to the Theory of Games II, Annals of Math. Studies 28 (1953), pp. 319-323/324. Bibliographic record only (e.g. https://biblioteca.confindustria.it/ricerca/dettaglio/contributions-to-the-theory-of-games-vol-ii-autori-vari/7613). Secondary sources say it characterizes the symmetric solutions of symmetric majority games. I could not read it; continuum only as far as I can tell.

6. Harsanyi, "An equilibrium-point interpretation of stable sets and a proposed alternative definition", Management Science 20 (1974), 1472-1495. https://pubsonline.informs.org/doi/pdf/10.1287/mnsc.20.11.1472 . Argues the vNM definition ignores indirect dominance; in "absolutely stable" games (simple games included) the proposed definition agrees with vNM. Nothing on grids seen in the abstract.

7. Anesi, "Committees with farsighted voters: a new interpretation of stable sets", Soc. Choice Welf. 27 (2006), 595-610. https://ideas.repec.org/a/spr/sochwe/v27y2006i3p595-610.html . Absorbing equilibrium points of a dynamic committee game lie in stable sets of the underlying (finite-alternative) game; the setting is a finite alternative set, so it treats finite abstract games, but no divide-the-dollar grid example is stated in what I saw. Also Anesi, "Noncooperative foundations of stable sets in voting games", Games Econ. Behav. 70 (2010), 488-493 (CeDEx 2010-04/08, https://www.nottingham.ac.uk/cedex/documents/papers/2010-08.pdf); Anesi and Duggan, "Dynamic bargaining and stability with veto players", GEB (2017), https://www.nottingham.ac.uk/economics/research/publications/dynamic-bargaining-stability-veto-players.aspx . Useful for the finite-alternative framework and for the fact that vNM sets of finite weak tournaments may fail to exist; they are the natural place to look for a grid statement but I found none.

8. Diamantoudi and Xue, "Farsighted stability in hedonic games", Soc. Choice Welf. 21 (2003), 39-61. https://ideas.repec.org:443/a/spr/sochwe/v21y2003i1p39-61.html . Farsighted vNM sets in hedonic games (finite). Not about divide-the-dollar. Related: Ray and Vohra, "The farsighted stable set", Econometrica (2015), https://jstor.econometricsociety.org/publications/econometrica/2015/05/01/The-Farsighted-Stable-Set . Farsighted sets are a different concept; do not conflate with vNM sets.

9. Ciardiello (2009), finiteness of vNM majority stable sets for three players in spatial voting. https://ideas.repec.org/p/ufg/qdsems/16-2009.html . Continuous multidimensional policy space; no divide-the-dollar grid.

10. Brams and Taylor, "Divide the dollar: three solutions and extensions", Theory and Decision (1994). https://link.springer.com/article/10.1007/BF01079266 . Discrete (whole cents) divide-the-dollar but a two-player noncooperative bidding game; name collision only.

11. Richardson (1953, kernels of digraphs; I did not locate a direct URL). Folklore statement: a finite digraph with no odd directed cycles has a kernel (a vNM stable set of the dominance relation); with odd cycles a kernel may fail to exist. Relevance: the grid dominance digraph has odd cycles, and non-existence at odd k is consistent with this, but Richardson gives no uniqueness and does not apply directly. If dominance were acyclic the kernel would be unique (vNM themselves), which is not our case.

## Is it a fair research-level test problem?

Yes, with caveats.
- It is self-contained, small, and checkable exhaustively for modest k (done above to k = 9 for the full set of stable sets).
- It is not "known" in a way that gives the answer away; I found no stated result. A proof for all even k looks feasible by hand: show internal stability of the symmetric set, then external stability, then uniqueness by a case analysis on the corner points and the boundary layer. Whether someone already did this is unknown (probable but not found), so it should be framed as "likely folklore or an exercise-level result", not "novel theorem".
- The claim "unique symmetric-type set for all k" is false as stated for odd k under the standard definition (no stable set at all), so the problem statement must fix k parity. This is the most useful finding for the test design.

## Definitions a problem statement must fix

1. Strict versus weak domination: use strict improvement for both members of a pair (the standard vNM definition). With the weak form (each member at least as well, at least one strictly) the discriminatory sets and the odd-k behaviour change; I did not test the weak form.
2. Parity of k: even k admits (k/2, k/2, 0) and permutations; odd k has no half-grid point, and my search finds no stable set at all. State whether odd k is in scope.
3. Imputation set: nonnegative integers summing to k (no slack, no free disposal). If waste is allowed, the grand coalition and effectivity change.
4. Effectivity: dominance via S requires x(S) <= v(S); with v(pair) = k this is automatic, so only coordinates matter. A "majority" variant requiring a strict majority of votes weighted by shares (Jordan's game) is a different game.
5. Whether the stable set is required to lie in the imputation set (individually rational, here x_i >= 0 which is trivial since v(i) = 0) or in all feasible allocations; equal here.
6. Existence versus uniqueness: state both separately, since odd k fails existence.
