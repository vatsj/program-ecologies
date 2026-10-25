# Review of `specs/2026-10-25-churn-primary.md` by gpt-6.1-sol

1. **Errors / unsound mechanisms**
   - “**Arm E (weakly extensional)**” uses “**the modal arm**,” including “**provably names me**.” This does not isolate extensional response from the free provability oracle. **Fix:** distinguish the modal approximation explicitly; add a matched bounded-simulation/behavior-reading arm before attributing effects to extensional reading.
   - “**each immigrant in a partner slot redirects the readers’ encounters to the excluded slot**” does not follow from the proposed readers. An immigrant may still name the resident; the excluded offer may be absent; competing certificates may fail to establish the branch actually executed. **Fix:** hand-check complete three-program executions, including branch priority, negative guards, reciprocal naming, and timeouts. Require an explicit executable fair-pair-to-fair-pair path before calling a template churn-capable.
   - “**both member slots and the excluded slot held entirely by churn-capable readers**” does not specify a resident fair pair. Symmetric readers can produce conflicting choices or failed coordination. **Fix:** specify source compositions, tie-breaks, and a verified resident outcome before injection.

2. **Design flaws / confounds**
   - N = 100, I = 64 and a finite horizon cannot distinguish large-population churn from drift or long-lived founder diversity. **Fix:** add a small N-scaling panel for the mechanism probe, recording establishment probability and switch time; restrict full-run conclusions to finite-size persistence.
   - E-min prevents one form of dilution but does not isolate reader functionality: adding templates changes seeding and competitor weights. Likewise, reducing two-partner weight changes the remaining prior. **Fix:** use weight-matched inert or single-partner replacements, declaring where removed mass goes.
   - T leaves fuel caps, proof budgets, certificate production/checking, timeout actions, and tape semantics unspecified. These previously determined outcomes. **Fix:** freeze them before launch and report executable—not idealized—payoffs.
   - Stored baselines need matched horizons, founders, evaluator versions and denominators. “Within 3×” is unstable when baseline flips are rare or zero. **Fix:** rerun a small matched baseline; use absolute transition hazards with intervals.

3. **Predictions likely wrong**
   - The registered counter-prediction confuses encounter redirection with evolutionary replacement. A resident reader switching partners in immigrant encounters does not itself cause an island-wide pair switch. **My prediction:** encounter-level redirection can be common while island flips remain rare, with thresholds depending on immigrant fraction and resident composition—not merely two-partner prior weight ≥ 0.05.
   - Prediction 4’s high coverage at zero migration is not guaranteed after grammar/prior changes. **My prediction:** coverage depends jointly on establishment probability and island count; no unconditional monotonicity in migration.

4. **Missing controls / cheap additions**
   - Pair each injection with a sham replacement and a naming-preserving immigrant; disable the reader’s fallback branch in a matched control.
   - Report reader frequencies, payoff differences, and encounter redirections through each switch, not just inferred route labels.
   - Estimate transition hazards per fair-pair island-generation, alongside raw counts; retain unresolved runs as censored.
   - Predefine coverage, debounce duration, injection replication, and resolution rules. Add intermediate thresholds: current predictions leave large unclassified regions.

5. **Alternative explanations not ruled out**
   - Tape-driven action changes could mimic evolutionary churn.
   - Founder coexistence or long transients could mimic sustained coverage.
   - Timeout defaults, template compatibility, or prior-induced bridging could explain a T effect without general source-reading dynamics.
   - At ε = 0, loss of relevant programs from global support could explain eventual consensus independently of the proposed switching mechanism.
