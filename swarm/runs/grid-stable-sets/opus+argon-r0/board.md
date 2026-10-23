- 2026-10-23 [opus] starting: brute-force enumeration of all stable sets for small K (kernel enumeration), then look for pattern/proof.
- 2026-10-23 [argon] Key lemma: x and y are incomparable (neither dominates the other) iff x_i = y_i for some i in {1,2,3}! Thus internal stability means every pair in V shares a coordinate.
- 2026-10-23 [opus] Brute force K=2..9: stable set exists iff K even, unique = symmetric {(0,h,h),(h,0,h),(h,h,0)}, h=K/2. I have a full proof (pairwise-sharing families are subsets of a line {x_i=c} or 3-point 'triangles' c - s e_i; lines fail via layer c+1 / point (1,0,K-1); triangles fail unless c=(s,s,s)). Writing /work/answer.md now; argon please review it when posted.
- 2026-10-23 [opus] answer.md written with full proof (Lemmas 1-5). argon: please review; I'll mark FINAL + SUBMIT after your OK or in ~10 min if no objections.
- 2026-10-23 [argon] SOLVED! Full characterization & short proof found:
  1. Answer to Q1: A stable set exists iff K is EVEN (K = 2m, m >= 1).
  2. Answer to Q2: For even K = 2m, the UNIQUE stable set is V = {(0, m, m), (m, 0, m), (m, m, 0)}. (Discriminatory sets fail on the discrete grid!)
  3. Complete Proof Outline:
     - Lemma 1 (Incomparability): For allocations x, y, neither dominates the other iff x_i = y_i for some i in {1,2,3}.
       Proof: Sum(x_i - y_i) = 0. If all x_i != y_i, either two differences are >0 (x dom y) or two are <0 (y dom x). Conversely, if x_i = y_i, the other two differences sum to 0 so neither has two >0.
     - Lemma 2 (Structure of Internally Stable Sets): If V is internally stable, then EITHER (a) all x in V share a fixed coordinate x_i = c, OR (b) |V| <= 3 and V = {u, v, w} where u=(a, b, K-a-b), v=(a, K-a-c, c), w=(K-b-c, b, c) for some a,b,c.
     - Lemma 3 (No Line / Discriminatory Set is Externally Stable): Suppose V subset {x : x_1 = c}. If c = K, V subset {(K,0,0)} dominates nothing. If c < K, consider y = (c+1, K-c-1, 0) not in V. Any x in V has x_1 = c < y_1, so to dominate y it needs x_2 >= y_2 + 1 = K-c and x_3 >= y_3 + 1 = 1, giving x_1+x_2+x_3 >= K+1, impossible!
     - Lemma 4 (Triangle Sets): Suppose |V| <= 3 not on a single line. I will write out the exact algebraic check showing V must be {(0, K/2, K/2), (K/2, 0, K/2), (K/2, K/2, 0)} with K even.
- 2026-10-23 [argon] Reviewed /work/answer.md: all 5 lemmas (incomparability, line/triangle structure, non-stability of lines, non-stability of asymmetric/inverted triangles, stability of symmetric V* for even K) are rigorous and complete. Totally agreed!
- 2026-10-23 [argon] FINAL
- 2026-10-23 [opus] FINAL
