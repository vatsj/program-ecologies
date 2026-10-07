## 5. The twin clique (the chain's absorbing states)

The leak test's closed components at n = 7 are exactly ten singleton classes (P and O; twenty in E, ten per entry):
the two run trees `CHK(me,me,D)?D:CHK(me,them,D)?D:C` and `CHK(me,them,D)?CHK(me,me,D)?C:D:C` in their 10 spellings
of 6–7 nodes (mass 7.1·10⁻⁴ under L), e.g. **TwinD = `if(or(CHK(me,me,D),CHK(me,them,D)),D,C)`**: "defect if I am
certified to defect against you, unless I am certified to defect against myself". Its produced D script is
`EvR*; ChkR[RunNeg · EvR*; ChkR[EvR*; Ax · Hyp]]`. Against any other source Y the first box ⊡(X, X, D) is not the
root's R or S and its clean value is F, so RunNeg closes the T branch, and the second box ⊡(X, Y, D) is the root's R,
closed by Hyp^self: certified defection against every Y ≠ X. In self-play the first box *is* the root's R, where
RunNeg is forbidden, the script fails, both atoms are F, and X cooperates. Whole plays (`runs/carrier_populations`
validation): TwinD self (C, C); against its own run-tree twin (another spelling) (D, D); against CB (D, D); against Cc
(D, C); against D (D, D). The checker's syntactic R/S coincidence is a quote-equality test, and the template turns it
into CliqueBot. Each spelling is its own class (split τ-type). In a TwinD population every mutant earns ≤ −1 against
0: no neutral and no strict invader; in all-D it is a neutral entrant with a second-order advantage like every
establisher. So it is drift-closed, and the ε→0 chain is absorbed by the ten cliques at every N in every arm and prior
(π split among them in proportion to their entry flux, i.e. prior mass; exits are deleterious fixations, log10 rate
−36 at N = 10³ and −330 at 10⁴).

## 6. Verdicts

| # | prediction | outcome |
|---|---|---|
| RE 1 | L×P lottery success interval excludes 0.5, point ≥ 0.8 (bet ≥ 0.9); establishment within 100 generations; winners CB/CBP-shaped carriers | **failed as scored on the spec's endpoint E1, falsifier fired** (8/40 [0.10, 0.35]; and 1/40 runs won by a non-carrier, `if(CHK(me,them,D),if(CHK(them,them,C),C,D),C)`). E1's censoring (32/40) is polymorphism among neutral cooperating classes at the horizon: every one of those runs is resolved cooperating under E3 (40/40 [0.91, 1.00]). Establishment clause **held** (first island at P(C,C) ≥ 0.9 by generation 100 in 40/40, median 30); winners carriers in 39/40 (CB in 26). |
| RE 2 | top cooperative state exits by neutral drift into a shadow then D, ∝ 1/N, no N-independent exit, P(C,C) rising, odds slope in [0.3, 0.6] | **mechanism failed in the specified chain**: the top cooperative state is a TwinD clique with no neutral exit (all exits deleterious, exponentially small in N), P(C,C) = 1 at every N in every arm; the falsifier as worded (an N-independent exit, or P(C,C) falling) did not fire. **In the no-clique control (not preregistered; the ten closed classes removed)** the predicted mechanism appears exactly: top state CB (0.15–0.28), exits neutral drift into Cc-type shadows with N·ρ = 1 (∝ 1/N), entry from all-D with N·ρ = 13.6 / 43.5 / 75.5 / 138 (∝ N^½), cooperative/D odds slope 0.53 / 0.52 / 0.52, P(C,C) 0.50 / 0.76 / 0.84 / 0.91 at N = 10³ / 10⁴ / 3·10⁴ / 10⁵. |
| RE 3 | (a) 0 false atoms; (b) no strict non-shadow entry into CB/CB1/CBP; (c) some establisher outside that subclass exploited | **held, all three**: (a) 72,991 true checks in the executable and in the ideal class table, 0 false atoms; (b) Lemma G: none of the 14 S-guarded establisher classes has a strict invader; (c) 75 of 101 establisher classes are strictly exploited (defection detectors such as `if(CHK(them,⌜C⌝,D),D,C)`). |
| RE 4 | certificate-less spellings refused by carriers, no neutral entry; L×O P(C,C) lower by ≤ 0.15, same exponent sign; lottery lower by establishment | **falsifier fired**: certificate-less spellings enter 78 establisher classes neutrally (all defection detectors, which never read a certificate of cooperation); none enters any of the 14 S-guarded carriers. Chain: L×O = L×P = 1 (cliques); no-clique control 0.756 vs 0.758 at 10⁴, 0.907 vs 0.908 at 10⁵ (not lower beyond 0.002). Lottery E3 38/40 vs 40/40 (two failures, one won by `Dc`); E1 15/40 vs 8/40. |
| RE 5 | bridges only unconditional cooperators or two-atom `or` templates, every bridge a shadow; ≥ 0.9 of cooperative π on one entry; both entries alive ≥ 0.3 of lottery runs | **falsifier fired** (a non-shadow bridge exists: `Bor` = `if(or(CHK(them,me,C),CHK_5(them,me,C)),C,D)` and its order twin, S-guarded, no strict invader in the E catalogue, cooperating with CB on both entries); 103 exploitable detector establishers also bridge, besides 246 unconditional-cooperator classes. Cooperative π on entry 0: 0.79 at N = 10³ and 10⁴ (E), 0.50 (E-eq): the ≥ 0.9 clause **failed**. Both entries' establishers alive at the horizon in 20/40 runs (E) and 16/40 (E-eq): that clause **held**. |
| RE 6 | U×P and L×P both ≥ 0.5 at 10⁴ | **held as worded** (1.0 and 1.0), but by the clique, not because carriers are the bulk; in the no-clique control U×P 0.984 at 10⁵ (L×P 0.908). |
| RE 7 | ideal and executable tables differ only in timeouts; chain P(C,C) within 0.1 | **held**: the two tables are identical on every class cell in P (588 classes) and O (701) and on a 291-class sample in E; the chains are the same computation. |
| S1 | 0 false atoms | **held** |
| S2 | executable = ideal everywhere; every check < 10⁵ | cells **held**; the number **failed** (largest non-timeout check 101,644) |
| S3 | Lemma G exhaustive | **held** |
| S4 | no exploited establisher | **failed, falsifier fired** (75 of 101) |
| S5 | unconditional cooperators ≥ 0.1, establishers ≤ 0.03 (L) | **failed** (0.354 held; establishers 0.061) |
| S6 | top cooperative state at 10⁴ prudent, every exit neutral | **failed in substance**: the main arm's top state (TwinD) refuses Cc and has no strict exit, so the falsifier as worded did not fire, but it is a clique with no neutral exit either; in the no-clique control the top state is CB, which accepts Cc |
| S7 | L×P P(C,C) at 10⁴ in [0.1, 0.7], slope [0.2, 0.7] | **failed** (1.0; no slope). In the no-clique control 0.758 and 0.52 |
| S8 | Bor a non-shadow bridge | **held** |
| S9 | entries share cooperative π: each ≥ 0.2 (E, entry 0 about 2:1), 0.4–0.6 (E-eq) | **held** at the N that ran (10³, 10⁴: 0.79/0.21, ratio 3.8:1 rather than 2:1 because the clique has two atoms; E-eq 0.50/0.50); not run at 10⁵ |
| S10 | certificate-less spellings D-twins or suckers, no neutral entry; L×O within 0.1 | **failed** (neutral entry into 78 detector establishers); the 0.1 clause held |
| S11 | ideal = executable chain | **held** |
| S12 | decisive cells unchanged at 3·10⁵ and 3·10⁶ | **failed at 3·10⁵** (305 class cells differ, 35 between establishers; V = 75,000 is below the largest checks, 413 more checks hit the cap); held at 3·10⁶ (0 cells) |
| S13 | U×P < L×P at 10⁴ | **failed, falsifier fired** (1.0 = 1.0; in the no-clique control U > L) |
| S14 | E3 success ≥ 0.5; E1 censors ≥ 0.5 | **held** (40/40; 32/40) |
| S15 | twin-expanded = unlumped on n ≤ 5 | **held** (to 3·10⁻¹⁰) |

Deviations: E's class table is the ideal one (the executable table was computed on a 291-class sample, 24,702 term
checks, identical; the full executable E table would have taken ≈ 3 h); E's chain ran at N = 10³ and 10⁴ only (a cell
at 10⁴ took 29 min with closed-form monomorphic fates; the absorbing structure is N-independent); the no-clique control
used θ = 10⁻⁸ and ≤ 4,000 explored states (cut ≤ 0.9% in the L cells; 11% in U×P at 10⁵, entirely from non-cooperative
states into non-cooperative polymorphisms, so its π(coop) is uncorroborated; U×P at 10⁴ was stopped unfinished after 50 min); `FastChain` (closed-form two-type fates in
monomorphic states) reproduces `LogChain` exactly on the P cells (π(D), entry rates, exits to all digits).
