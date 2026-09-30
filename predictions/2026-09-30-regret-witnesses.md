# Predictions: regret witnesses of persistent states, 2026-09-30

Written before computing. This is a post-hoc analysis of existing runs, with no new simulation. For a
population mixture σ over behavioural classes, the regret of program q is

r(q) = u(q, σ) − u(σ, σ),

which is the large-N fitness advantage of one q against the population. The **regret witness** is the
argmax q, and a state is **no-regret** iff max_q r(q) ≤ 10⁻⁹. Since u is linear in σ, the regret against a
global island mixture equals the island-averaged regret.

States come from:
- the lim_N chain support (`runs/limN_pd.json`);
- the frozen PD island runs (`runs/islands_pd.json`, global final mixture);
- Chicken with `ROLE`: all-`ROLE`, all-`not(ROLE)`, and the self-referential mutual-Swerve classes;
- Chicken without `ROLE`:
  - the mixed-equilibrium state, 9/11 `not(THEM(ME))` with 2/11 Straight;
  - the three-class cool state (`not(THEM(THEM))`, Straight, `not(THEM(^Straight))` at 0.659 / 0.195 / 0.146);
  - the two-class state `not(THEM(ME))` 0.627 with `not(or(X,THEM(ME)))` 0.372.

## Verdicts

1. **PD all-D is no-regret.** D is dominant against D.
2. **PD all-`THEM(^C)` has max regret exactly 1 = T − R**, attained by fakers (`THEM(^D)` and others). Its
   shadow C has regret 0.
3. **PD all-X and all-`ROLE`** (lim_N support at w = 0.1, N = 100) have positive regret, with D among the top
   witnesses.
4. **PD frozen island states.**
   - Cooperative runs (all-`THEM(^C)`) have regret 1 from an extinct faker.
   - Exploitation-probe runs have positive regret.
   - Mutual-defection runs have regret 0 iff their share of `THEM(^D)`-type programs, which cooperate with
     suckers, is at most 1/3. Above that, `not(THEM(^C))` is a witness: it cooperates with D, defects on
     `THEM(^D)`, and has regret f·1 + (1 − f)(−2) + 1 for share f of `THEM(^D)` against D.
5. **Chicken with `ROLE`.** The conventions are no-regret. The mutual-Swerve islands have positive regret
   with a Straight-playing witness, so they persisted at ε = 0 only because the witness was extinct.
6. **Chicken without `ROLE`.**
   - The mixed-equilibrium state has regret of about 2 − 3h − (−h) = 2 − 2h ≈ 1.6. Its witness is
     `not(THEM(^Straight))`, which goes straight against the swerver and swerves against Straight. That
     explains the observed three-class state: the witness invades and becomes a resident.
   - The three-class cool state has positive regret, since it pays −0.341, below the mixed equilibrium.

**Falsifier.** Any of the following would falsify these predictions:
- all-D has positive regret;
- the top witness of all-`THEM(^C)` is not a faker;
- a `ROLE` convention has positive regret;
- the mixed-equilibrium state's top witness is not `not(THEM(^Straight))` or a class playing identically
  against the residents.
