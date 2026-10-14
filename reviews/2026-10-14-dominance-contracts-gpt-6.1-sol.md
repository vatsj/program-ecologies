# Review of `specs/2026-10-14-dominance-contracts.md` by gpt-6.1-sol

## 1. Design flaws/confounds and fixes

- **The installation rules are inconsistent with atomic jumps and the positive control.** With installation restricted to non-refusers, β = 1 cannot replace an entire slot when refusal carriers exist; at f_r = 1 there are no eligible recipients—even for offers the guard accepts. Distinguish *carrying r* from *refusing this offer*. Specify replacement fractions and eligibility precisely. Test β = 1 jumps separately at every f_r; do not claim exact M dynamics where replacement is partial.
- **R2 is not absorbing under the full ecology.** The guard blocks M exits, not relation-P drift or migration. Low R2 occupancy therefore does not imply dominance-unreachability. Add a contracts-only R2 reachability control, then measure escape hazards under the full kernel.
- **Dominance of modal outcomes is not dominance for sampled individuals.** In polymorphic islands, consenting individuals may receive different payoffs from the modal representative; source-reading complements may change behavior when partners acquire overrides. Evaluate x using effective installed phenotypes and the actual complement population. Record realized payoff changes and departures from predicted x; restrict the exact-M validation to homogeneous islands.
- **The static walk may not match the proposal kernel.** Uniform contracts, uniform dominating successors, and uniform accepted moves give different transition rates; rejected draws also change residence times. Build the exact contract-induced generator, including multiplicities and null proposals. Baseline residence times alone do not justify interleaving P and M: contracts change the genotype composition underlying P.
- **The estimand is ambiguous.** Define horizon “support,” treatment of unclassified islands, and whether either migration cell suffices for recovery. Run all replicates to a common primary horizon; extending only “unresolved” runs creates outcome-dependent observation windows.

## 2. Predictions likely wrong

- **RE5’s explanation is wrong:** failure of R2 can reflect ongoing P/migration leakage, not failed reachability. I predict full-kernel R2 can remain below its threshold despite certain contracts-only hitting.
- **RE4 overstates selection against refusal.** Consent creates island-wide externalities; genotype linkage and role-specific subsequent gains can offset forgone installation. The r-blind arm changes exposure as well as the alleged cost. I predict heterogeneous, potentially nonmonotone trajectories, not uniform decline across slots.
- **RE6’s sparsity argument is weak.** At N = 100, founders supply roughly 30 contract copies per island. Relevant coverage—not raw menu size—determines scarcity. I predict potentially substantial early effects followed by depletion.
- **RE7 is unsupported by endpoint dominance.** At β = 0.25, intermediate mixtures need not benefit either coalition, and one slot may fix while the other fails. I predict strong contract-specific variation and asynchronous fixation.
- **RE3 need not be monotone.** Competing transition kernels can create traps or resonance. D2 need not lie between baseline and D1.

## 3. Missing controls / cheap additions

- Contracts-only, homogeneous-outcome runs using the exact proposal kernel.
- Forced assays for every dominating edge: immediate payoffs, joint fixation, one-sided fixation, and reversal.
- Log effective phenotype alongside retained program identity; classify outcomes from actual play.
- Preserve the N panel before dropping D2: finite-N occupancy cannot establish large-population recovery.

## 4. Alternative explanations not ruled out

Apparent recovery could be transient synchronization, forced mass replacement, contract multiplicity bias, or menu depletion—not stable-set selection. Apparent cycling could be independent island turnover rather than recurrent directed cycles; report transition graphs and return sequences.

## 5. Beyond this experiment

nothing material
