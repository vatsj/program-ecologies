# Review of `specs/2026-10-21-hooks-followups-weak.md` by gemini-4-argon

### 1. Design flaws and confounds

1. **Part 1 — Circularity and exploitation of behaviour-keyed contracts:**
   - *Flaw:* "Behaviour class" (the 3 PA boxes) is defined by the base program, or by program + fills? If by the base program (e.g., $\beta = \text{ALLD}$), then two default defectors signing "cooperate with $\beta$" immediately become unconditional cooperators toward *all* base-ALLD programs, including each other and newly arriving naive ALLDs. Worse, once they hold the fill, their effective behaviour changes, creating a mismatch if PA boxes read effective behaviour. Conversely, if $\beta$ is evaluated *including* fills, the key is self-referential at contract-signing time.
   - *Fix:* Specify in the spec that $\beta$ is the *effective* PA-box signature of the partner *before* the new contract is written, OR that the contract is a *conditional* fill: "cooperate with partner iff partner's effective behaviour toward me (given its fills) is C". If it is merely keyed on the static 3-bit box tuple, state explicitly how conflicts between the base box and held fills are resolved.

2. **Part 2 — Credible-response (C) definition and tie-breaking:**
   - *Flaw:* "Among the actions its program and fills can express, given the joint fill" is underspecified. A boss's program + current fills is deterministic for a fixed worker pair. It can only "express" one action unless you mean: (a) the boss's base program reads the workers' new joint fill (via a probe/box) and reacts, or (b) the boss can *also* adopt a new fill/action as a best response. In the weakly extensional wing without probes, a boss cannot read a worker's fill unless the boss has a hook or box that inspects it. If the boss's action is evaluated by *allowing the boss to pick the best wage fill* in response to the union fill, say so. Also, when $s = 1/2$, paying $1/2$ gives the boss $1 - 1/2 - 1/2 = 0$, which ties with being struck ($0$). How the boss breaks ties ($0$ vs $0$) completely determines whether $s=1/2$ is ever paid!
   - *Fix:* Explicitly define the boss's choice set in (C) (e.g., the set of wages achievable by the boss adopting any single valid boss fill, or the boss's best response over $\{0, 1/4, 1/2\}$ with strict tie-breaking in favour of not being struck / paying the demanded wage).

3. **Part 2 — Confound between union contracts and boss–worker contracts under (C):**
   - *Flaw:* The brief states: "Boss–worker contracts are also judged under the same rule in (C)." If fair share rises in (C), you won't know whether union (worker–worker) contracts or farsighted boss–worker contracts caused it.
   - *Fix:* Either keep boss–worker contracts myopic in the main (C) cell, or add a control cell: Part W's maximal (boss–worker only, no union contracts) evaluated under rule (C).

### 2. Predictions I think are wrong

- **Prediction 1 & 2 (Open contracts ≥ 0.5 / ≥ 0.65 universal-open):** Likely **wrong** if $\beta$ is just the 3-bit PA box class. Two default defectors belong to class $\beta_D$ (provably D). If they sign a contract "cooperate with $\beta_D$", they now cooperate with *every* uncontracted ALLD in the population and get suckered to death in the scramble, or they form a mutual-C club of $\beta_D$-programs that is immediately invaded by any $\beta_D$ program that *refuses* contracts (a shadow). Either way, provers or defectors will displace them, or they will lock in an unbridgeable $\beta$-clique that doesn't count as `universal-open` (which requires cooperation with open provers like FairBot).
- **Prediction 5 (Credible-response union contracts reach fair share ≥ 0.2):** Likely **wrong** for $s = 1/2$ unless tie-breaking is fixed. At $s = 1/2$ (each worker gets $1/2$, or total wage $1/2$? In the union game, wages are usually total $0, 1/4, 1/2$ or per-worker; if $s=1/2$ leaves the boss with $>0$ surplus over strike, it works; if it leaves 0, tie-breaking decides). Even with positive boss surplus, under lineage keys, a worker-union contract keyed on Boss Lineage $L$ dies whenever Boss $L$ is replaced by drift/migration or when workers meet another boss lineage. Prediction 6 (role-keyed beats lineage-keyed by a wide margin, not just "at least as well") is much stronger: lineage-keyed (C) will likely fail ($\le 0.10$) while role-keyed (C) succeeds ($\ge 0.30$).

### 3. Missing controls or cheap additions

- **Part 1:** Log the *sucker rate* (C against D) of holders of behaviour-keyed contracts. This immediately tests whether open contracts turn defectors into exploitable suckers against non-signers of the same behaviour class.
- **Part 2:** Separate adoption rates and active shares of $s = 1/4$ vs $s = 1/2$ union contracts. Under (C), $s = 1/4$ and $s = 1/2$ compete; if $s = 1/4$ is signed first, does a subsequent $s = 1/2$ contract overwrite it as a strict Pareto improvement for both workers? Make sure the conflict/overwrite rule allows $s = 1/2$ to supersede $s = 1/4$.

### 4. Alternative explanations not ruled out

- In Part 1, if `universal-open` recovers in *Open maximal*, it might be because behaviour-keyed contracts are *suicidal* (holders get exploited by their own behaviour class and die out), effectively reducing *Open maximal* to the *no-contract* ablation (0.675), rather than contracts functioning as "legible conditional promises." Track contract survival/fixation on winning islands to distinguish "open contracts are benign/helpful" from "open contracts self-destruct so provers win by default."

### 5. Ideas beyond this experiment

- Nothing material.
