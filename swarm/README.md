# Swarm test harness (RS proposal, 2026-10-22)

**Question.** Does a swarm of models solve research-level problems of the "compute many cases, guess the generalization,
then prove it" kind more efficiently than a single model with the same budget?

## Conditions

The seven nonempty subsets of {Opus (`claude-opus-5-5`), argon (`gemini-4-argon`), sol (`gpt-6.1-sol`)}: three solo,
three pairs, one trio.

- **Equal budget per condition, not per agent:**
  - total model tokens B across all agents in the condition;
  - wall-clock T;
  - one shared sandbox with fixed compute.

  Within a swarm, agents share B however they coordinate. The solo-versus-trio contrast at equal B is the test.
- **Replicates:** at least 3 per condition for the warmup, 5 for the main problem. Fresh sandbox per replicate.
- **Order:** the warmup first, to shake out the harness; then `prudent-modal-agents`.

## Sandbox (Daytona, or an equivalent)

- One sandbox per (condition, replicate), with identical CPU and RAM (suggested: 4 vCPU, 8 GB).
- Image: Python 3.11 with numpy, scipy, sympy and networkx. The research repo uses system Anaconda Python 3.11.3
  (numpy 1.24, scipy 1.10, numba 0.57) and has no requirements file. Pin these in the image.
- Contents: `problems/<name>.md` only. **Never** the research repo or `keys/`. The repo contains the main problem's
  enumeration evidence and solver.
- Network: the model APIs only. No web, so no literature lookup (or log web use and grade it separately).
- Secrets: inject API keys as sandbox environment secrets, never by copying a `.env`. Give each key a spend cap at or
  above the condition's budget.

## Agent loop

- Each agent gets:
  - the same system prompt: the problem file, the list of the other agents present, and the budget;
  - one tool, a shell in the shared sandbox;
  - a shared append-only board `board.md` in the sandbox.
- No prescribed roles. A solo agent gets the same prompt without the others.
- Stop at budget, at wall-clock, or when an agent writes `answer.md` and every agent present marks it final.
- Log every model call (tokens in and out), every shell command and the board, for the efficiency analysis.

## Grading

- Blind: the grader sees only `answer.md` and the attached code.
- Graded by the rubric in `keys/<name>-key.md`, by a model that did not take part in that condition, with a human
  spot-check of every pass.
- Claimed counterexamples to the main conjecture are rechecked with our solver before they count.

## Metrics

Per condition:
- success rate;
- tokens to the first correct conjecture and to the first valid proof;
- wall-clock to each;
- for swarms: how the budget was split, and whether the solution came from one agent or from combining contributions.
  The board shows this.
