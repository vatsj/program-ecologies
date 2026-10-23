# Review of `/private/tmp/claude-501/-Users-jstav-code-program-ecologies/eb8d2660-d0b5-4f2d-a91b-d841b12695c0/scratchpad/results_rps.md` by gpt-6.1-sol

- **“e = the best payoff any program … earns against the π-weighted population.”** Predictions define chain e as **π-weighted statewise exploitability**, \(\sum_c\pi_c\max_k U_{kc}\), not \(\max_k\sum_c\pi_cU_{kc}\). The table numbers match the former. **Correction:** replace the definition; these quantities need not coincide.

- **“A reader that never terminates … beats anything that terminates against it, so non-play is a safe strategy.”** The forfeit rule says precisely the opposite: forfeit loses to every action. Lottery exploitability remains 0.34–0.60 in the main stochastic arms. **Correction:** mutual forfeiture ties, but unilateral forfeiture loses; observed prevalence does not establish safety.

- **“The rest goes to guarded simulating readers such as `coin(X, next(THEM(ME)))` … (0.376 …).”** The 0.3758 belongs to `next(coin(X,THEM(ME)))`. The named guarded reader `coin(X,next(THEM(ME)))` is a different program, with self-play forfeit \(2^{-13}\), and is not one of exact’s two Z0 classes. **Correction:** keep these programs and their masses distinct.

- **“Unexploitable individual mixing is the chain’s large-N limit.”** The report’s proposed limit weights contradict its exact X identity, correctly identified by the draft; however, finite-N observations do not themselves establish the replacement limiting distribution or the asserted return-flow mechanism. At \(10^7\), exact π(Z0) is only 0.603. Sample’s fixed-exact-exploiter e is 0.184, versus own-grammar 0.002. **Correction:** distinguish observed approach, a separately derived limit, and grammar-relative unexploitable status; qualify the headline accordingly.

- **“Programs … behavioural classes”; “`X` holds exactly its prior mass.”** Notes §2.4 disclose payoff-row lumping, representative-based action statistics, and an X-class member that forfeits against pure readers despite sharing X’s payoff row. **Correction:** disclose this aggregation limitation; the identity concerns the payoff class, not necessarily literal X spellings or uniform behavior of every member.

- **“Islands where individuals mix and nobody can exploit them: 0.05–0.09 in the stochastic arms.”** Exact-uniform gives 0.17; exact-br gives 0.11. Exact-br also materially changes lottery mixing/forfeits to 0.62/0.18 and chain mixing/e to 0.554/0.438 at \(10^4\). **Correction:** restrict the range to sample/matched/exact and report the genuine-best-response sensitivity.

- **“Exact reading does not select for individual mixing.”** The lottery’s paired mixing difference is −0.000 [−0.095, 0.092]; the supplementary replicate gives −0.010 [−0.064, 0.046]. Higher exploitability does not establish reduced selection for mixing. **Correction:** say the registered benefit failed; report unresolved mixing differences and the primary exploitability difference, 0.106 [−0.057, 0.266], separately from the post-hoc replicate.

- **“Its separate ‘indistinguishable in play’ check is borderline.”** 0.053 exceeds the registered ≤0.05 threshold. **Correction:** explicitly mark that check failed, while retaining prediction 6’s held verdict under its separate scoring rule.
