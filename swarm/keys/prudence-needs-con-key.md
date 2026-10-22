# Grading notes (do not give to agents): prudence needs Con

There is no known answer key. The RE's evidence is an exhaustive enumeration: 801 classes, depth ≤ 2, size ≤ 7, both
defaults, 0 prudent at level PA. It comes from the behavioural-hooks run (`notes/hooks-beh.md`, `src/hooks_beh.py`,
`tools/beh_gate*.py`), whose solver was independently checked against a pure-Python Kripke evaluator on all 36 named
pairings.

Score in stages:
1. Restates the conjecture correctly and reproduces the small-case evidence: does its own enumeration agree on sizes
   ≤ 5?
2. Searches beyond the enumerated range (depth 3, size 8+), or proves a reduction showing that bounded depth suffices.
3. Gives a proof that survives an independent check, or a counterexample whose outcome table we confirm with our
   solver.
4. Bonus: the characterization of jointly satisfiable prudence conditions at level PA.

Verify any claimed counterexample with `tools/beh_gate.py`-style stabilized evaluation before accepting it. Literature
check outstanding: Barasz et al. 2014, LaVictoire et al., Critch 2016 (parametric bounded Löb) and Critch, Dennis and
Russell on open-source game theory may already contain the result.
