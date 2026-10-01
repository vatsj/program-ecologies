# Review of `predictions/2026-10-01-modal-followups.md` by Fable (Claude subagent), before the run

1. **Design / bugs.**
   - *Crash (stale):* E3's `'allR'` seeding would crash `islands.run_one`. Note: this was already patched before
     the run, but the review read an older file.
   - *Robustness:* use `imap_unordered` with incremental dumps.
   - *Wrong statistics:* `R_2nd` tracks only FairBot, though the cooperative mass is split over four provers.
     `allc_coop` is ALLC's share of the whole population, not of the cooperators.
2. **E3 mechanism.** "Nothing removes ALLC" is false at finite ε.
   - The standing D fringe, d ≈ εμ_D/w ≈ 1.6·10⁻³, prunes ALLC at a rate of the same order as its input.
   - A deterministic mutation–selection ODE on the 51-class matrix gives P(C,C) = 0.99, with ALLC pinned at
     x* = μ_C/(1 + μ_D) = 0.32 and no cycle. The weak arm's ODE goes to all-D from both starts.
   - Collapses on the big island need a drift excursion of ALLC past ½. The OU estimate for the sd of the ALLC
     share is 0.15 at ε = 10⁻³ and 0.48 at 10⁻⁴.
   - Predicted modal big island: 0.6–0.95 at ε = 10⁻³, and lower at 10⁻⁴.
3. **E1 is decided statically.**
   - The grammars are isomorphic: μ(C) = μ(D) = 0.488 in both.
   - Two-state reduction, M0: P(C,C) ≈ 0.11 at N = 100 and 0.70 at 3·10⁴, with exponent 0.50 ± 0.03.
   - Two-state reduction, W0: peak near N ≈ 950, and 0.009 at 3·10⁴.
   - The channel effect combines unfakeability with 7× cheaper entry: the FairBot class has μ = 0.0148 against
     W0's `THEM(^C)` at 0.002. E1 cannot separate them.
4. **E2.**
   - The single-edge reduction holds for FairBot to 4%. It fails for PrudentBot by about 3×, and N-dependently.
   - The plateau still extrapolates to about 0.038–0.042.
   - `BOX(THEM(THEM))` has N-independent strict invaders at n = 8. Expect P(C,C) ≈ 0.80 at 10⁵ and 0.86 at 3·10⁵,
     with the ratio exponent near 0.42.
   - Report π of each member of the prover family.
5. **Islands.** Modal at 64 islands with w_g = 0 should reach at least 0.7: FairBot has no faker.
6. **Beyond.** The finite-ε pinning of ALLC is an ε-independent shadow equilibrium: mutation supplies its own
   pruner. If it survives the agent-based runs, it is a third regime, and it belongs in THEORY §9.5.
