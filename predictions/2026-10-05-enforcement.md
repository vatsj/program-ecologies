# Predictions: incentive-compatible enforcement in the union game, and the unfakeable-polarity pact (2026-10-05)

Spec: `specs/2026-10-05-enforcement.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-05-enforcement-gpt-6.1-sol.md`;
where they differ the spec's [after review] text is the resolution). Committed before any counted run. Measured so
far: only that the modified evaluator (`src/union_enforcement.py`) stabilizes every encounter of the union run's
language (297 boss × 452 worker functions) in all 8 (arm, pool) combinations at c = 0.5, and that its CC arm
reproduces the union run's tensor exactly. No Part A table, reduced chain or full chain has been looked at.

## Design choices fixed before the run (the spec left these open)

- **Override.** At each world: recommendations from the box atoms; then a rational boss keeps its wage and whacks
  each striker iff (1 − s) − c > 0 with the pool, never without it (gain −c); a rational boss never whacks a working
  worker (gain −c with or without the pool). Its implemented whack policy is 'strike' or 'none'. Then a rational
  worker best-responds to the implemented boss action from the full table (work: s − L·[h′ = source ∧ tagged];
  strike: −L·[h′ = strike ∨ (h′ = source ∧ tagged)]). Indifference → the program's recommendation. Boundary
  1 − s = c (s = 1/2, c = 1/2 with the pool): declared 'whack' (primary), 'nowhack' reported as the alternative. The
  third reading ("tie → the recommendation" at the boundary) is not run: for a source-targeting recommendation it
  would need a fourth policy, "whack tagged strikers only".
- **Boxes refer to implemented actions** (the flags are updated with the implemented joint code).
- **Pool.** A whacked striker is replaced by an outside scab paid s; the boss gets 1 − s for it (net 1 − s − c per
  whacked striker). A whacked *working* worker is not replaced (it works). Pool and commitment are crossed.
- **Reduced canonical chain** exactly as in the union run: boss over the 9 constants, workers over {scab, militant,
  union}; uniform prior, and the length prior restricted to these programs with the union run's class masses (frozen
  across arms). Exact dense log-GTH. c ∈ {0.1, 0.5}, N ∈ {10², 10³}. 8 cells per prior and c.
- **Evaluation point.** Unless a prediction says otherwise, shares are read at N = 10³; c = 0.5 for predictions that
  name it; prediction 3 (no c named) is read at c = 0.5 (primary) and reported at c = 0.1.
- **Part A** uses the union run's evaluator (committed play; Part A is about the wage check and the handshake, not
  enforcement) on the boss language at n = 6 with box levels {0, 1} (so that fair-until-world-1 classes exist), and
  reports the union run's level-0 boss language as well. The negated single-wage box is expressible in the union
  grammar (`not` over `BOX(s ∈ {1/2})`), so no atom is added; union⁻ costs 11 nodes, one above the union run's
  worker cutoff, which is irrelevant for a static table.
- **Box audit** (every arm): an independent history-based evaluator recomputes every atom from the implemented play
  of earlier worlds and checks (i) the stable play equals the evaluator's, (ii) box monotonicity, (iii) Lemma 0 at the
  stable world (every true box's proposition holds in the stable play), (iv) a rational slot's stable move is a best
  response. Run on every boss × named-worker pair and on a random sample of the full language; plus the full tensor's
  stabilization. 0 violations required.

## RE predictions (copied verbatim from the spec)

1. **No polarity in the two-level language carries a pact against every low-paying boss** [after review: replaces
   the RE's first draft, which conflated soundness with pact activation]. union⁻₀ pairs never strike (¬□fair is
   false at world 0); union⁻₁ pairs strike against every *constant* low-paying boss and work against the
   bottom-world wage faker; no boss class is judged fair while paying low at the stable world (0 counterexamples);
   and the self-harming errors (fair bosses struck by militant⁻) have μ mass < 0.05 of the boss language.
   *Falsifier:* a union⁻ variant that strikes against every low-paying class including the fakers, or a boss judged
   fair while paying low.
2. **Commitment ablation under the uniform prior, c = 0.5, no pool: the workers' commitment carries the fair share,
   the boss's does not.** (CR) and (RR) give fair ≤ 0.05 and zero wage ≥ 0.8; (RC) is within 0.05 of (CC) on every
   share. *Falsifier:* (CR) fair ≥ 0.2, or (RC) differing from (CC) by ≥ 0.15 on the fair share.
3. **The pool suppresses the wage through restored production, in both CC and RC alike** [after review: sol's
   reading; the RE's "free of the commitment cost" rationale was wrong, since rational repression still pays c when
   executed]. With the pool, fair falls by ≥ 0.1 relative to the matched no-pool arm in both (CC) and (RC), and
   (RC with pool) is within 0.05 of (CC with pool); repression conditional on a strike rises with the pool while
   strike incidence falls. *Falsifier:* the pool not lowering fair in (CC), or (RC) and (CC) with pool differing by
   ≥ 0.15.
4. **Under the length prior every cell gives zero wage ≥ 0.95:** no commitment structure or pool rescues the
   workers from the prior. *Falsifier:* any cell with fair ≥ 0.1 under the length prior.
5. **Part C:** the full-chain (RC with pool) cell has repression conditional on a strike ≥ 0.5 and fair ≤ 0.01.
   *Falsifier:* repression conditional on a strike < 0.2.

## Subagent predictions (Opus)

- **S1 (rational refusal only where free).** In CR and RR, under both pools and priors, an implemented strike occurs
  only at s = 0 (a rational strike is never strictly better than working, and ties only at s = 0), so the boss's cut
  1/2 → 1/4 is strict from every fair state and fair ≤ 0.01 in every CR and RR cell at N = 10³. *Falsifier:* an
  implemented strike at s > 0 anywhere in a CR/RR tensor of the full language, or a CR/RR cell with fair > 0.01.
- **S2 (RR without the pool settles on the smallest positive wage).** Uniform prior, c = 0.5, no pool: RR gives
  intermediate ≥ 0.3 and zero wage < 0.8, so prediction 2's zero-wage clause fails for RR. Mechanism: the rational
  boss never whacks, strikes are credible only at s = 0, so against any refuser the boss's best wage is 1/4.
  *Falsifier:* RR intermediate < 0.3 or zero wage ≥ 0.8.
- **S3 (committed strike targeting is a free deterrent against rational workers).** CR, uniform prior, c = 0.5, no
  pool: states whose boss is (0, strike) hold ≥ 0.5 of π, and realized repression is ≤ 0.01 (the threat is never
  executed on path because rational workers do not strike into it). *Falsifier:* (0, strike) states < 0.5 or realized
  repression > 0.01.
- **S4 (rational repression with a reserve army closes the zero-wage entry).** Uniform prior, c = 0.5: RC with pool
  gives fair ≤ 0.01, because every zero-wage boss then whacks strikers and the militant's neutral entry at s = 0
  becomes deleterious (−1 against 0); CC with pool gives fair ≥ 0.05, because (0, none) and (0, source) still admit
  the militant. So prediction 3's "(RC with pool) within 0.05 of (CC with pool)" fails. *Falsifier:* RC-with-pool
  fair > 0.01, or CC-with-pool fair < 0.05.
- **S5 (the boundary is off-path in the reduced chain).** Every reduced-chain cell's π and summaries are identical
  (to 10⁻⁹) under tie = 'whack' and tie = 'nowhack', since no named worker strikes at s = 1/2 in any arm. In the full
  chain (Part C, always-strike present) the boundary is on path. *Falsifier:* any reduced-chain summary differing by
  more than 10⁻⁹ between the tie rules.
- **S6 (length prior).** Every Part B cell under the length prior has fair ≤ 0.01 and intermediate ≤ 0.05.
  *Falsifier:* any length-prior cell with fair > 0.01 or intermediate > 0.05.
- **S7 (Part C).** Full chain, RC with pool, length prior, c = 0.5, N = 10³: strike + scab split ≤ 0.05 (0.51 in the
  union run's CC cell), zero wage ≥ 0.9, repression conditional on a strike = 1 exactly under tie = 'whack', worker
  mean payoff ≤ 0.01, slot efficiency ≥ 1.85 (1.37 in the union run). Incentive-compatible repression with a reserve
  army raises efficiency and leaves equal division at zero. *Falsifier:* zero wage < 0.9, or strike + scab split > 0.05.
- **S8 (Part A, the union⁻ pair's activation rule).** Of the six union⁻/militant⁻ variants, only union⁻ with the PA
  wage check and the level-1 handshake (`and(not(BOX(s = 1/2)), BOX1(OTHER = strike))`) has a self-pair that ever
  strikes, and it strikes iff the boss pays low *at world 0*, whatever it pays later. So it also strikes, forever,
  against a boss that pays low only at world 0 and fair at the stable world (a self-harming error of the pact itself,
  not only of militant⁻). *Falsifier:* a union⁻(0,1) self-pair striking against a boss with s(world 0) = 1/2, or
  working against one with s(world 0) < 1/2; or any other union⁻ self-pair striking.

## Verdict rules

A prediction **holds** if every clause holds at its evaluation point; **fails** if its falsifier fires; otherwise
**partial**, with the clause that failed named. Failures are reported as failures and get REJECTED entries. Shares
are the union run's disjoint summaries computed from the *implemented* joint action. Every π is reported with its
support and transition structure.
