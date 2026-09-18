# Test-game verdicts — written 2026-09-18, before the first run of any of these games

Model: attractor chain with deterministic replicator, single-mutant transitions, prior
mu(p) = 2^-bits with bits = log2 a(|p|) + 2 log2 |p| + 1.  Node counting follows
IMPLEMENTATION.md §2 (every constructor is a node, application included), so
`or(X,THEM(ME))` is 5 nodes and `or(and(X,X),THEM(ME))` is 7.

Arms run: strong and weak at n=6 (square), weak at n=7 (incremental) where feasible.
N in {10, 100, 1000}.

## Chicken with ROLE (games/chicken.yaml)
Utilitarian max is the correlated outcome (one swerves, one goes straight): 0.5 per
player per match under role averaging.  `ROLE` (1 node) plays Swerve in role 0 and
Straight in role 1; against itself it realises that outcome exactly and is a strict
Nash of programs (`not(ROLE)` crashes into it, constants lose to it).
**Verdict:** pi concentrates on the monomorphic states all-`ROLE` and all-`not(ROLE)`
(and behavioural equivalents), bistable between the two, deadweight loss 0.  Any
support state with loss > 0 falsifies this.

## Chicken without ROLE (games/chicken_norole.yaml, control)
No correlation device.  Unconditional types settle at the Hawk–Dove polymorphism
(Straight at frequency 1/11, payoff -1/11 ... i.e. below 0) or all-Swerve.
**Verdict:** deadweight loss strictly positive (>= 0.5 - 0 = 0.5 relative to the
correlated optimum); the mode is either all-Swerve or a Swerve/Straight polymorphism.

## Nash demand (0.4/0.6) with ROLE (games/demand.yaml)
Same structure as Chicken: `ROLE` realises (Low, High) alternation, 0.5 each, sum 1.
**Verdict:** mode all-`ROLE` / all-`not(ROLE)`, loss 0, split 0.5/0.5 across roles.

## Nash demand without ROLE (games/demand_norole.yaml)
Hawk–Dove among unconditional types: High invades all-Low (0.6 > 0.4), the interior
polymorphism has High at 1/3 with payoff 0.4.
**Verdict:** mode is a Low/High polymorphism with High near 1/3 (or all-Low with a
`THEM(ME)`-based deterrent at larger n), payoff 0.4, deadweight loss 0.1.

## Divide the dollar (games/dollar.yaml, control)
`Half` strictly dominates.
**Verdict:** pi ~ all-`Half` (plus neutral equivalents), loss 0.

## Zero-sum matching pennies with ROLE (games/zerosum.yaml)
u(p,q) = -u(q,p) for every pair, so every monomorphic state has payoff 0 and the sum
is always 0: efficiency is vacuous.  Best-response chains among conditional
programs can cycle (rock–paper–scissors structure).
**Verdict:** either the indeterminate flag is raised (a replicator cycle is found) or
pi is spread over a neutral set of mutually-zero types.  No state with strictly
positive self-payoff exists, so no strict attractor.  Deadweight loss 0 by construction.

## Exchange game (games/exchange.yaml)
PD with b=3, c=1.  A reciprocator grounding at rate e is stable against Keep iff
3e < 2, so the 5-node `or(X,THEM(ME))` (e = 1/2) is already strictly stable, unlike
in the PD (where e = 1/2 is exactly neutral against D).
**Verdict:** cooperation appears one level earlier than in the PD: at n=5/6 the
support includes an `or(X,THEM(ME))`-based cooperating attractor (with the Give
neutral edge) bistable with all-Keep; in the PD at n=6 there is none.

## Battle of the sexes with ROLE (games/bos.yaml)
Under role averaging both constants earn 1.5 against themselves (sum 3, the maximum);
`ROLE`-conditioned alternation mis-coordinates and earns 0.
**Verdict:** bistable between all-`A` and all-`B` (plus equivalents), loss 0; the
split between the two is set by absorption from the seed distribution, roughly even.
