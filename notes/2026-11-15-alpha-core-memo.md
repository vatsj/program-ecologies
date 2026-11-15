# Decision memo: drop "credible" from domination and commit to the α-core? (2026-11-15)

Not a run spec. A static-theory design decision for the RS; the reviewers are asked for independent opinions on
the decision, errors in the derivation, and literature the memo misses or misstates.

## Setting

A *technology* maps a game to a set of acceptable outcomes. A *realization* gives each player a strategy set Σᵢ ⊇ Aᵢ
of programs that output actions. Decided today (DEFERRED 15 addendum): static theory is stated only for realizations
*closed under reading*: every player's strategy is a program that reads every other player's program. The
leader-value core (a coalition commits to actions, the complement best-responds in its own interest) and the
follower-value core are retired as theory objects.

The theory's domination relation currently reads: S dominates y with x when S can commit to its part of x, *the rest
answer with a credible response*, and every member of S ends strictly better off. Strong internal stability
(acceptable outcomes are undominated) is the core; the relative pair of axioms is the stable set.

## The derivation under review

1. At level 0 (strategies are actions) a leader fixes an action; at level 1 it fixes a response function, and the
   complement faces an ordinary reduced game. Level k leaves a level k−1 game, so the levels are not closed under
   fixing. Programs with source access are.
2. In the closed space a coalition's deviation (rewriting its source) is read by programs that are already fixed.
   There is no reduced game left to solve; "no coalition gains by rewriting its source against fixed text" is strong
   equilibrium in program space.
3. Fixed text can tailor its answer to the deviation, so a deviating S gets max over its actions of min over the
   complement's: its α-worth. Claim: the outcomes supportable as strong program equilibria are the α-core
   (analogue of the commitment folk theorem, Kalai, Kalai, Lehrer, Samet 2010, for coalitions). Unverified.
4. "Credible" has no free meaning there: the punishing text is fixed before the deviation and never run on-path.

## The proposal

Drop "credible" from the domination relation. Domination becomes α-domination; strong internal stability becomes the
α-core; the stable-set target at a = 1 (majority division, empty core under any convention) is unchanged.

## Pros

- P1. One notion, no timing convention, no leader/follower twin, no optimistic/pessimistic selection of the
  complement's equilibrium. It is what the closed space literally implies.
- P2. Existence: non-empty for a wide class (Scarf 1971 for convex NTU games, from memory), including trade with
  gains, where level-1 commitment-proofness is empty through incompatible ultimatum claims.
- P3. No effect on the theory's running examples: in the pair-worth game and majority division worth does not
  depend on the complement, so α-, β- and leader-domination coincide.
- P4. Honest division of labour: the static notion is a wide envelope and the ecology (prior, founding scramble,
  drift) does the selecting, which is what the runs already show ("commitment technologies alone support every
  feasible individually rational outcome").
- P5. Matches the ε→0 chain as built: it scores committed policies without executing them, so untested threats deter.

## Cons

- C1. It selects little. In the PD the α-core contains every outcome giving each player at least mutual defection's
  payoff and no pair less than it can guarantee; in trade any refusal threshold is self-supporting. "Efficient"
  becomes nearly empty of content as a static prediction outside no-externality games.
- C2. It endorses threats the program has found unstable: a program identical on-path without the punishment is a
  neutral shadow, drifts in, and the outcome is then dominated in the credible sense. The static notion accepts
  states the dynamics leave. (Unconditional shadow; sibling theorem: no class in the unbounded modal language is
  drift-closed.)
- C3. It contradicts recorded results taken as normative: with both sides' enforcement ex-post rational the chain
  selects the smallest positive wage, not the committed-play outcome; the RS's social organization target (the fair
  wage) was argued from credible threats. Dropping "credible" removes the theory's ground for calling the whacker's
  threat illegitimate.
- C4. α versus β is itself a choice. If the complement's text reads the deviator's *program* but the deviator can
  randomize privately or diagonalize, the deviator gets more than its α-worth (toward β). The realizable language
  has a private tape (RESULTS "A private random tape"), so "α" is exact only for deterministic, fully legible
  deviators.
- C5. Realizability: tailoring a punishment to an arbitrary rewritten source requires the fixed text to resolve the
  deviator's behaviour within fuel. With bounded readers the reachable punishments are fewer, the worth a deviator
  can secure is higher, and the realized set is smaller than the α-core and machine-dependent.
- C6. Coalitional rewriting presumes a two-slot (multi-program) deviation; the island dynamics mutate one slot at a
  time. Strong equilibrium in program space is a static condition the current mutation law never tests.

## Alternatives

- A1. Keep "credible", defined as: the complement's answer must itself be acceptable to the technology on the game
  after S's rewrite (recursive consistency; coalition-proof Nash in the Bernheim–Peleg–Whinston sense is the
  nearest relative). Smaller set, existence problems return, definition is recursive.
- A2. α-core as the static envelope plus a separate dynamic axiom ("survives neutral drift" / tested threats),
  with the envelope making no selection claim. This is P4 made explicit and leaves C2–C3 to the second axiom.
- A3. β-core instead of α (answers C4 in the deviator's favour).

## RE's leaning

A2: adopt α-domination as the static envelope, say explicitly that it is an envelope, and carry credibility as a
dynamic condition (DEFERRED 13), not as a word in the static relation. Open in that case: whether the drift
condition can be stated as an axiom on technologies rather than a property of one realization.

## Questions for the reviewer

1. Is step 3 right? Is "strong program equilibrium outcomes = α-core" a known result, and under what conditions
   (pure versus mixed, NTU versus TU, α versus β)? Cite what exists.
2. Which of the cons is most damaging, and is any pro or con wrong or missing?
3. Would you drop "credible", keep it (A1), or split (A2)? One paragraph of reasons.
