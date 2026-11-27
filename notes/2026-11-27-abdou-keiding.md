# Abdou and Keiding, *Effectivity Functions in Social Choice* (Kluwer 1991): reading note

Read from the PDF the RS supplied (not committed): contents, §1.4–1.5, ch. 3 §2–5, ch. 8. Not read: ch. 2 (structure),
ch. 4–7 (implementation, strong Nash, exact and strong consistency, coalition-proof), ch. 9 (values, correlated
strategies, repeated games).

**Effectivity function.** E(S) is the family of sets B of alternatives that coalition S can force the outcome into.
From a game form: α (S has a strategy that lands in B whatever the others do) and β (for whatever the others do, S
has a reply landing in B); E_α ⊆ E_β; the game form is *tight* if they are equal (Defs 1.4.1–1.4.4).
**Core.** a is dominated by B via S if a ∉ B, B ∈ E(S) and every member of S strictly prefers every b in B to a;
Core(E, R) is the undominated set (Def 3.2.1). The derived characteristic function is
V(S) = {z : some B ∈ E(S) has z_i ≤ min over B of u_i} (Def 1.5.2).
**Stability** = nonempty core at *every* preference profile (Def 3.2.3). Results: no upper cycle (disjoint coalitions
forcing sets with empty intersection) and no lower cycle are necessary (Props 3.3.1, 3.3.3); convex implies stable
and strongly stable (Thms 3.4.3, 3.4.6), convex meaning B1 ∈ E(S1), B2 ∈ E(S2) gives B1∩B2 ∈ E(S1∪S2) or
B1∪B2 ∈ E(S1∩S2); **stable iff acyclic** (Keiding; Thm 3.5.3 finite, 3.5.4 topological). Simple games: stable iff the
Nakamura number exceeds the number of alternatives (Ex 3.3.4). Three-voter majority is unstable (Ex 3.2.4).
**Responses by the complement (ch. 8).** γ-effectivity: S can move the outcome into B and the complement cannot
restore the status quo; E_α ⪯ E_γ ⪯ E_β (Lemma 8.2.3). Cooperative equilibrium of type 1 (an improvement counts
unless the complement can restore the status quo), type 2 (unless it can leave some improver no better off; needs
effectivity for *pairs* (B, C), β for B and α for C), type 3 (the complement's reply must not hurt the complement):
"clearly the most satisfactory ... a matter of future research" (p. 167).

**For us (the RE's reading).**
- The RS's leader-value equilibrium with rational replies is a type-3 notion, which the book leaves open.
- A leader effectivity function depends on the followers' preferences, so it is one effectivity function per payoff
  profile; the stable-iff-acyclic theorem (uniform over profiles) does not transfer verbatim. For a fixed game the
  tool is the derived V(S) and Scarf/Bondareva–Shapley balancedness.
- First-mover conflicts are upper cycles: two disjoint coalitions each forcing sets that do not meet.
- Program games: P6–P9 (strong Nash between the β- and α-cores) is the statement that reading makes the game form
  behave as tight at one end.
