# The leader-value core over the game catalogue (2026-10-13)

A static companion to DEFERRED 15 (the RS's response-function equilibrium, on-path repair), using the
characterization proposed by the claude.ai chat session: define a coalition's **leader value** v(S) = max over
commitments a_S of S's payoff given the complement's credible response; an equilibrium exists iff some
Pareto-efficient profile gives every coalition at least v(S), i.e. the **core of the leader-value game** is nonempty.
With the complement responding by individual best reply this is the γ-core (Chander–Tulkens 1997); with a
coalitional credible response it is closer to Ray–Vohra. Computed here for two-player games with individual best
replies and ties broken as stated; three-player cases by the known core results. Pure-action games, no `ROLE`
(each realization is still the same game and responses see realized actions, so `ROLE` does not change the answer).

| game (payoffs as in the repo) | v(player) | efficient profiles meeting every v | verdict | what the ecology does |
|---|---|---|---|---|
| PD (C/C 0, D/C 1, C/D −2, D/D −1) | −1 each (commit D, met by D) | (C, C) | **exists, unique: (C, C)** | the modal and realizable arms reach it (RESULTS "Almost all seeds?", milestones 2, 4) |
| chicken (−10, 2, −1, 0) | 2 each (commit Straight, met by Swerve) | none (sum of leader values 4 > max total 1) | **empty: the commitment race** | one-sided norms per island, a coin flip (RESULTS "Fixed-role chicken") |
| hawk–dove hd3 (−½, 2, 0, 1), hd6 (−2, 2, 0, 1) | 2 each | none (4 > 2) | **empty** | same as chicken |
| two-player divide-the-dollar (demands 1/6..5/6, disagreement 0) | 5/6 each (commit 5/6, met by 1/6) | none (5/3 > 1) | **empty** | fixed roles: the rotating dictatorship of the largest demand (RESULTS "Divide-the-dollar partitions"); one population: 50–50 at finite N by risk dominance, then polymorphisms |
| social organization, one-shot normal form (boss wage s ∈ {0, ¼, ½} vs work/strike; output 1) | boss 1 with ties for the leader (wage 0, work) or ¾ with ties against (wage ¼); worker 0 (an unconditional strike has no leader value) | (0, work), and (¼, work) under ties against the leader | **exists at wage 0 or ¼; never at ½** | RR: the smallest positive wage (RESULTS "Incentive-compatible enforcement"); the chain's zero wage under CC |
| three-player majority divide-the-dollar | decisive pairs make responses vacuous | the core | **empty** (the RS's non-existence proof) | the rotating-pair chain, a limit set (RESULTS "Three-player majority divide-the-dollar") |

**Reading.** In action-land the notion diagnoses exactly the split the ecology shows: it exists where the dynamics
reach an efficient point (PD) and is empty where the dynamics settle on a limit set or a coin flip (anti-coordination,
bargaining, majority division). In the social organization game it exists only at the boss's leader wage, because
a one-shot strike is an unconditional action with no leader value; the fair wage needs a *contingent* commitment
(strike iff s < ½), which is a program or gene, not an action, and that is where the RS's "attempt 2" broke (a
program-deviator can rig the pre-response reference point). So the fair wage lives outside action-land by
construction, which is consistent with the enforcement result that credibility imposed as a clause gives the
smallest positive wage, and with the lottery result that it takes strikers arriving in numbers (committing first).

**Caveats.** *Credibility applies to responses to deviations only, not to the prescribed play* (claude.ai
session, 2026-10-13): under on-path consistency f({1: C}) must be player 2's prescribed C, and C is not a best reply
to C, so if "f(a) is the complement's credible response" were imposed at every a, including on-path extensions, the
equilibrium would have to be Nash and the notion would collapse to Nash ∩ Pareto, which is empty in the PD. The
table uses the reading in which play is simultaneous on path and only off-path responses must be credible; that is
exactly the γ-core, and it is part of the definition, not an implicit choice. Ties in the SOG are the whole difference between wage 0 and ¼ (a strike is free at zero wage); with
coalitional rather than individual responses the two-player tables do not change (the complement is one player);
`ROLE`-symmetrized games were not recomputed since each realization is the same game.

## Allocation games (the RS's definition, 2026-10-13)

*Definition (RS):* every player gets some goods, from which everyone has nonnegative marginal utility, and chooses who
gets those goods. *Reading:* an exchange economy with gift actions and own-bundle utilities; the only credible
response of an outsider to anything is to keep its own goods (giving away never raises own utility), so the
complement's response is trivial and a coalition's leader value is what it can reach by reallocating its own
endowments internally. The leader-value core is then **the classical core of the exchange economy** (a coalition
blocks with its own endowment). *Existence:* for concave (more generally, convex-preference) utilities the economy
is a balanced NTU game and the core is nonempty by Scarf (1967); the trade needed to beat autarky is mutual gifts,
and a unilateral withdrawal is met by the credible "keep", so individually rational trades are not undone by
commitment. *Why this class differs from divide-the-dollar:* the goods have owners, so "keep" is a default that
caps every leader value at autarky; the dollar has no owner, and the largest demand is a first-mover commitment on
unowned surplus. (The social organization game's output is likewise unowned before the wage is set.)

*Preliminary discrete check* (`python3`, integer units, square-root utilities with random weights): 2 players × 2
goods, 0/30 empty cores; 3 players × 2 goods, 3/20, 7/20 and 2/20 empty at 2, 3 and 4 units per good, non-monotone
in the grid and consistent with indivisibility artefacts rather than a continuum failure (Scarf's theorem needs
divisible goods); nonconcave (square) utilities with 2 players, 0/30 (two-player cores are rarely empty). A proper
continuous test (a convex program for the core) belongs to the sweep.
