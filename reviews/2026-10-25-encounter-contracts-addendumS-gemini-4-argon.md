# Review of `specs/2026-10-25-encounter-contracts.md` by gemini-4-argon

1. **Errors, contradictions or unsound mechanisms**

- **Clock-mixing contradiction in the pool dynamics.** The brief says both: *"any class change during holdouts is a spontaneous (genesis-driven) transition, counted and included in the dynamics explicitly"* and *"The two clocks are not added: in the rare-migration limit genesis is within-island dynamics... and only migrant transitions are jumps on the migration clock. Classes identified from holdouts are labelled provisional, with an escape-rate upper bound propagated into the share dynamics."* A per-generation spontaneous rate (within-island clock) and a per-migrant jump rate (migration clock) have different units; you cannot propagate a per-generation escape rate into a pure per-migrant ODE without specifying the ratio $m/\nu$ (which the $m \to 0$ limit eliminates). **Fix:** Keep the rare-migration limit strict in the ODE (only migrant jumps between verified closed classes), and report the holdout escape rate per generation as a separate diagnostic bound on how much mass is non-settled at finite $T_{\text{holdout}}$, rather than mixing the two rates into one differential equation.

- **Missing baseline for singleton coalitions ($|S|=1$) in arm H.** Under **H**, *"a contract is a set of fills, one per member... a member that reaches no hook cannot join the coalition. ... Arm R is the special case where every program is wrapped in one top-level hook"*. Under **R**, any individual can unilaterally deviate ($|S|=1$) via a contract. Under **H**, an unhooked individual cannot even perform a unilateral deviation in stage 2. This conflates coalitional contractibility ($|S| \ge 2$) with individual plasticity ($|S|=1$). **Fix:** Either allow $|S|=1$ proposals in **H** to write to a free top-level override (restricting the hook requirement to $|S| \ge 2$ coalitional agreements), or explicitly log $|S|=1$ vs $|S|\ge 2$ blocked proposals separately so individual vs coalitional restriction is not confounded.

2. **Design flaws or confounds**

- **Arm C's conditioning starves copying.** In **C**, *"a copied proposal is an actual surviving bundle drawn by the frequency of its carriers... and made in an encounter drawn from the island only if that encounter's situation is p"*. If the encounter triple $(i,j,k)$ is drawn first and its stage-1 profile is $p$, and then a bundle is drawn by carrier frequency and rejected unless its key is $p$ (or vice versa), almost all copied proposals for off-path/migrant keys $p$ will fail to match and be wasted, turning $q=0.5$ into an effective $\nu$ reduction of $\approx 50\%$ on rare encounters. **Fix:** Draw the encounter triple $(i,j,k)$ first (yielding stage-1 profile $p$), and if at least one bundle with key $p$ exists on the island, draw the copied proposal *conditionally among surviving bundles with key $p$* weighted by carrier count; if none exists for $p$, fall back to a uniform proposal.

3. **Predictions**

- **Prediction 8 (Arm Sconversion rate and silent phase) is likely wrong on the mechanism.** On a monomorphic dominated island, an accepted or proposed contract for the on-path key $p$ is *immediately on-path* for its signers in every encounter against residents. For a $|S|=2$ contract to pass through a "silent phase in both slots," its key $p$ must be off-path, which means it cannot convert a resident dominated island unless the stage-1 programs themselves are still mutating/drifting. **My prediction:** In **S**, conversions out of dominated islands are driven by *Directly firing* $|S|=1$ fills or $|S|=2$ fills where one slot's stage-1 program already accommodates (as in Prediction 3), so fewer than 0.5 of **S**'s conversions will come from two silent halves drifting up neutrally.

4. **Missing controls or cheap additions**

- **Split genesis and conversion attributions by $|S|=1$ vs $|S|\ge 2$.** Because a $|S|=1$ contract is just a conditional individual mutation tested against opponent responses (no partner coordination needed), it will dominate conversions in **R**, **H**, and **S**. Report the share of $V^*$ conversions caused by $|S|=1$ vs $|S|=2,3$ contracts.

5. **Alternative explanations**

- If **R** beats **0** on $V^*$ share, it may be entirely due to $|S|=1$ individual best-response overrides (which need no coalitional coordination and suffer no $1/N$ partner-dilution barrier), rather than two-player coalitional contracts. Stratifying conversions by $|S|$ rules this out.
