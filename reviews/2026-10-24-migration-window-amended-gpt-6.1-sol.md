# Review of `specs/2026-10-24-migration-window.md` by gpt-6.1-sol

## 1. Errors, contradictions, unsound mechanisms

- **Component benchmark arithmetic is wrong.** “P(all three present) = 1 − 3(2/3)^C + 3(1/3)^C (0, 0.22, 0.56, 0.88, 0.99…).” The formula gives **0, 0, 0.4444, 0.8834, 0.9954**. Two consensus components cannot cover three members. Fix the table and add a benchmark unit test.

- **“Cleared for good” is not observable at a finite horizon.** “last-passage times for waste (cleared for good), Kaplan–Meier medians under right-censoring” conflates retrospective last exits with ordinary censored first-passage events. Fix: report “last observed waste through T,” explicitly horizon-dependent; reserve survival analysis for defined first-hitting events or provably absorbing clearance.

- **The lifetime statistic does not measure target duration.** “the target’s lifetime as their difference when positive” can count time before coverage is established, ignore disagreement, and miss exits/re-entry. Coverage may already be absent initially. Fix: derive contiguous target episodes directly from the target indicator; report first entry, episode lengths, and cumulative occupancy. Treat clearance-minus-coverage-loss only as a diagnostic.

- **Temporal precision is overstated.** “modal outcome logged every 50 generations, so first-passage times are exact to 50 generations.” Short excursions can occur entirely between observations. Fix: log target-state changes each generation, or call these sampled-grid passage times and occupancy estimates.

## 2. Design flaws or confounds

- **Changing C changes both isolation and component size**, from 64 to four islands. Increased target success could reflect faster within-component consensus, altered invasion/extinction, or preserved founding diversity. Fix: add a small fixed-islands-per-component panel, varying total islands, and report founding coverage and per-component efficient-absorption probabilities.

- **Modal efficiency is not population efficiency.** An island with substantial inefficient minority play can pass. Keep the registered modal target, but report encounter-weighted inefficient mass and a high-purity target beside it.

- **Two N values at fixed I cannot establish large-population behavior.** Explicitly label this a finite-size transient-window experiment, not evidence of asymptotic efficient selection. Define mN operationally and report realized migrant exposure across N.

## 3. Predictions likely wrong

- **Prediction 5 lacks a defensible ceiling.** “gV … meets the target at mN = 1” conflicts with the supplied prior finding that “the veto … spreads under migration in every run.” A guard can protect membership while destroying coverage. I predict high V*-occupancy but declining three-member coverage at high migration. Verify the reference against stored trajectories before using it as a positive control.

- **Inverse-migration scaling need not produce a widening separation.** If both times scale as 1/mN, lowering migration merely stretches the same trajectory; the fivefold separation requires independent evidence. I predict approximate time-rescaling only after establishment, with low-migration deviations from local dynamics.

## 4. Missing controls or cheap additions

- Run a balanced, pure-three-member initialization to isolate coverage erosion from waste clearance; separately seed waste among efficient islands to measure clearance.
- Report paired uncertainty intervals and distinguish unmet predictions from stated falsifiers; several leave an unclassified middle.
- Freeze numerical L, w, founding distribution, migration topology, and code revisions rather than “as in those runs.”

## 5. Alternative explanations not ruled out

Apparent windows may be delayed founding relaxation; component coverage may simply preserve initial diversity; guard benefits may reflect altered founding composition or contract availability rather than selective immigrant rejection. Transition counts alone do not establish neutrality—compare invasion success conditional on donor/recipient states and measured payoff differences.
