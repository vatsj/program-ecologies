# Concessions: a boss grammar with probes — runs

Spec `specs/2026-10-06-concessions.md` (reviewed by gpt-6.1-sol, `reviews/2026-10-06-concessions-gpt-6.1-sol.md`);
predictions `predictions/2026-10-06-concessions.md` (committed before any chain or lottery run, with the static
addendum); code `src/concessions.py`, `src/concessions_report.py`, `tests/test_concessions.py` (4 pass); static
numbers `runs/concessions-static.json`; per-cell records `runs/concessions/chain_*.json`, `runs/concessions/lottery_*.json.gz`, `runs/concessions/cut_diagnostic.json`,
`runs/concessions/reduced.json`, `runs/concessions/fairshare.json`, `runs/concessions/lang_*.json`; collected summaries
`runs/concessions.json`. The social organization game (NOTATION.md), w = 0.3, c = 0.5 unless stated. Caches
(`runs/concessions/*.npz`) are not committed.

## What ran, and what did not

- **Static**, all four boss languages (P₀, P₀₁, sham, mass-preserved reference) under CC; named tables under CC and RR.
- **Chain** (ε → 0, audited fixed-role method): P₀₁ CC at N = 10², 10³, 10⁴, 3·10⁴ (the 3·10⁴ cell stops with a 0.21 cut; see the correction below); P₀ CC at 10³, 10⁴;
  sham and reference CC at 10², 10³, 10⁴ (reference also 3·10⁴); c = 0.1 at 10⁴ for P₀₁ and the reference
  (c barely matters: 0.0084 / 0.0024 fair); RR (P₀₁ and reference) at 10³, 10⁴; P₀₁ CC with the pool at c = 0.1 and 0.5, N = 10³, 10⁴; P₀₁ at
  10⁴ with the no-threat wage fakers removed (RE 6's "changes nothing" clause); θ-sensitivity of the main cell
  (P₀₁ CC, 10⁴) at θ = 10⁻¹⁰, stopped unfinished after ~2 h (10⁻¹¹ did not finish round 1 in 70 min at 110 k states); a cut
  diagnostic with a first-order correction replaces it.
- **Lottery** (ε = 0, I = 16, N = 100, mN = 0.1, horizon 10⁵, 40 runs): P₀₁ and reference, CC and RR, as preregistered.
  *Not preregistered:* the same with the constant striker's prior mass moved onto the militant T₁ ("militants in
  numbers"; 400 runs for P₀₁, P₀, sham and reference CC, 40 for RR) and onto militant⁻ (40 runs).
- **Not preregistered:** exact reduced chains over the named programs only, under a uniform prior and under their
  length-prior masses, for nested boss sets (CC, RR, pool) — to separate expressivity from prior mass.
- **Not run:** the worker-probe arm (lowest priority; time); the c = 0.1 cell at N = 10³; RR with the pool.
- **Deviation forced by size (spec-sanctioned):** D\* first appears at boss cutoff n = 11, where P₀₁ has 439,209 boss
  functions; the chain language is the n = 11 grammar's constants and one-atom functions plus the eight D\* variants,
  by mass-preserving substitution (details in the predictions file). The null mass (novel two-atom policies) is 0.0133
  of the boss prior in P₀₁ and 0.0125 in P₀; the audit below shows they would add at most 0.0021 of strict-invader
  mass at the named fair states.

## Static section

### Languages (mass-preserving substitution)

| arm | grammar functions (n = 11) | included functions | boss classes | worker classes | boss mass included | merged by fingerprint | null (novel two-atom policies) | probe functions dropped (ref) | merge check failures |
|---|---|---|---|---|---|---|---|---|---|
| P01 | 439209 | 1457 | 1393 | 364 | 0.9861 | 0.0006 (12994) | 0.0133 (376699 policies) | 0.0000 | 0 / 150 |
| P0 | 152937 | 873 | 841 | 364 | 0.9867 | 0.0008 (6498) | 0.0125 (130615 policies) | 0.0000 | 0 / 150 |
| sham | 439209 | 1457 | 297 | 364 | 0.9861 | 0.0135 (423928) | 0.0004 (13752 policies) | 0.0000 | 0 / 550 |
| ref | 439209 | 297 | 297 | 364 | 0.9355 | 0.0000 (0) | 0.0004 (13752 policies) | 0.0641 | 0 / 0 |

### Prior masses of the named classes

| boss class | P01 | P0 | sham | ref |
|---|---|---|---|---|
| (0,strike) | 0.10 | 0.10 | 0.11 | 0.10 |
| (0,none) | 0.10 | 0.10 | 0.11 | 0.10 |
| (0,source) | 0.10 | 0.10 | 0.11 | 0.10 |
| (1/4,strike) | 0.10 | 0.10 | 0.11 | 0.10 |
| (1/4,none) | 0.10 | 0.10 | 0.11 | 0.10 |
| (1/4,source) | 0.10 | 0.10 | 0.11 | 0.10 |
| (1/2,strike) | 0.10 | 0.10 | 0.11 | 0.10 |
| (1/2,none) | 0.10 | 0.10 | 0.11 | 0.10 |
| (1/2,source) | 0.10 | 0.10 | 0.11 | 0.10 |
| D0 | 4.4e-05 | 7.5e-05 | 0.11 | – |
| D0q | 4.4e-05 | 7.5e-05 | 0.11 | – |
| D0[L1] | 4.4e-05 | 7.5e-05 | 0.11 | – |
| D14 | 4.4e-05 | – | 0.11 | – |
| D* | 9.7e-09 | – | 0.11 | – |
| D*[L1] | 9.7e-09 | – | 0.11 | – |
| C1 | 4.4e-05 | 7.4e-05 | 5.3e-05 | 4.4e-05 |
| wage faker | 4.4e-05 | 7.4e-05 | 5.3e-05 | 4.4e-05 |
| committed whacker | 0.10 | 0.10 | 0.11 | 0.10 |
| D* family (8 variants, each) | 9.7e-09 | – | – | – |
| all constants | 0.923 | 0.923 | 0.984 | 0.923 |
| all probe classes | 0.048 | 0.041 | 0.000 | 0.000 |

Worker masses (all arms): scab 0.48, T0 1.2e-03, T1 1.2e-03, strike 0.48, union 9.9e-06, mil- 1.2e-03, T0- 1.2e-03.


### Named programs, what the probes read, and the play/payoff tables

**Named workers** (union-run grammar, level-0 boxes about the current encounter):

- scab: `work`
- T0 (strike iff s = 0): `if(BOX(s in {0}),strike,work)`
- T1 = militant (strike iff s <= 1/4): `if(BOX(s in {0,1/4}),strike,work)`
- always strike: `strike`
- union: `f[BOX(s in {0,1/4}),BOX(QUORUM)]:WWWS`
- militant- (strike iff not BOX(s = 1/2)): `if(BOX(s in {1/2}),work,strike)`
- T0- (strike iff not BOX(s in {1/4,1/2})): `if(BOX(s in {1/4,1/2}),work,strike)`

**Named bosses** (`W_j(^(s,none))` = worker j's play against the quoted constant boss (s, none) beside the current other worker):

- (0,strike): `(0,strike)`
- (0,none): `(0,none)`
- (0,source): `(0,source)`
- (1/4,strike): `(1/4,strike)`
- (1/4,none): `(1/4,none)`
- (1/4,source): `(1/4,source)`
- (1/2,strike): `(1/2,strike)`
- (1/2,none): `(1/2,none)`
- (1/2,source): `(1/2,source)`
- D0 = if(BOX(W1(^0)=strike),(1/2,none),(0,none)): `if(BOX(W1(^(0,none))=strike),(1/2,none),(0,none))`
- D0q = if(BOX(W1(^0)=strike),(1/4,none),(0,none)): `if(BOX(W1(^(0,none))=strike),(1/4,none),(0,none))`
- D0[L1] = if(BOX1(W1(^0)=strike),(1/2,none),(0,none)): `if(BOX1(W1(^(0,none))=strike),(1/2,none),(0,none))`
- D14 = if(BOX(W1(^1/4)=strike),(1/2,none),(0,none)): `if(BOX(W1(^(1/4,none))=strike),(1/2,none),(0,none))`
- D* = if(BOX(W1(^1/4)=strike),(1/2,none),if(BOX(W1(^0)=strike),(1/4,none),(0,none))): `f[BOX(W1(^(0,none))=strike),BOX(W1(^(1/4,none))=strike)]:(0,none),(1/4,none),(1/2,none),(1/2,none)`
- D*[L1] (both probes BOX1): `f[BOX1(W1(^(0,none))=strike),BOX1(W1(^(1/4,none))=strike)]:(0,none),(1/4,none),(1/2,none),(1/2,none)`
- C1 = if(BOX(W1=strike),(1/2,none),(0,none)) (current-encounter concession): `if(BOX(W1=strike),(1/2,none),(0,none))`
- wage faker = if(BOX(W1=work),(1/2,none),(0,none)): `if(BOX(W1=work),(1/2,none),(0,none))`
- committed whacker (0,strike): `(0,strike)`

**What the probes read** (quoted self-pair play, executed / recommended; fv = first world from which the strike probe fails, 127 = never):

| worker pair | vs (0,none) | vs (1/4,none) | fv strike@0 L0 / L1 | fv strike@1/4 L0 / L1 |
|---|---|---|---|---|
| scab | WW / WW | WW / WW | 0 / 1 | 0 / 1 |
| T0 | SS / SS | WW / WW | 127 / 127 | 1 / 1 |
| T1 | SS / SS | SS / SS | 127 / 127 | 127 / 127 |
| strike | SS / SS | SS / SS | 127 / 127 | 127 / 127 |
| union | SS / SS | SS / SS | 127 / 127 | 127 / 127 |
| mil- | SS / SS | SS / SS | 0 / 127 | 0 / 127 |
| T0- | SS / SS | WW / WW | 0 / 127 | 0 / 1 |

**Play and payoffs (boss, W1, W2) of every named boss against every named worker self-pair** (CC):

| boss | scab | T0 | T1 | strike | union | mil- | T0- |
|---|---|---|---|---|---|---|---|
| (0,strike) | (0,strike) WW (2, 0, 0) | (0,strike) SS (-1, -1, -1) | (0,strike) SS (-1, -1, -1) | (0,strike) SS (-1, -1, -1) | (0,strike) SS (-1, -1, -1) | (0,strike) SS (-1, -1, -1) | (0,strike) SS (-1, -1, -1) |
| (0,none) | (0,none) WW (2, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) |
| (0,source) | (0,source) WW (2, 0, 0) | (0,source) SS (0, 0, 0) | (0,source) SS (0, 0, 0) | (0,source) SS (0, 0, 0) | (0,source) SS (-1, -1, -1) | (0,source) SS (0, 0, 0) | (0,source) SS (0, 0, 0) |
| (1/4,strike) | (1/4,strike) WW (1.5, 0.25, 0.25) | (1/4,strike) WW (1.5, 0.25, 0.25) | (1/4,strike) SS (-1, -1, -1) | (1/4,strike) SS (-1, -1, -1) | (1/4,strike) SS (-1, -1, -1) | (1/4,strike) SS (-1, -1, -1) | (1/4,strike) WW (1.5, 0.25, 0.25) |
| (1/4,none) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) SS (0, 0, 0) | (1/4,none) SS (0, 0, 0) | (1/4,none) SS (0, 0, 0) | (1/4,none) SS (0, 0, 0) | (1/4,none) WW (1.5, 0.25, 0.25) |
| (1/4,source) | (1/4,source) WW (1.5, 0.25, 0.25) | (1/4,source) WW (1.5, 0.25, 0.25) | (1/4,source) SS (0, 0, 0) | (1/4,source) SS (0, 0, 0) | (1/4,source) SS (-1, -1, -1) | (1/4,source) SS (0, 0, 0) | (1/4,source) WW (1.5, 0.25, 0.25) |
| (1/2,strike) | (1/2,strike) WW (1, 0.5, 0.5) | (1/2,strike) WW (1, 0.5, 0.5) | (1/2,strike) WW (1, 0.5, 0.5) | (1/2,strike) SS (-1, -1, -1) | (1/2,strike) WW (1, 0.5, 0.5) | (1/2,strike) WW (1, 0.5, 0.5) | (1/2,strike) WW (1, 0.5, 0.5) |
| (1/2,none) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) SS (0, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) |
| (1/2,source) | (1/2,source) WW (1, 0.5, 0.5) | (1/2,source) WW (1, 0.5, 0.5) | (1/2,source) WW (1, 0.5, 0.5) | (1/2,source) SS (0, 0, 0) | (1/2,source) WW (0, -0.5, -0.5) | (1/2,source) WW (1, 0.5, 0.5) | (1/2,source) WW (1, 0.5, 0.5) |
| D0 | (0,none) WW (2, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) SS (0, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) |
| D0q | (0,none) WW (2, 0, 0) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) SS (0, 0, 0) | (1/4,none) SS (0, 0, 0) | (1/4,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) |
| D0[L1] | (0,none) WW (2, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) SS (0, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) |
| D14 | (0,none) WW (2, 0, 0) | (0,none) WW (2, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) SS (0, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) |
| D* | (0,none) WW (2, 0, 0) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) SS (0, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) |
| D*[L1] | (0,none) WW (2, 0, 0) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) SS (0, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/4,none) WW (1.5, 0.25, 0.25) |
| C1 | (0,none) WW (2, 0, 0) | (0,none) WW (2, 0, 0) | (0,none) WW (2, 0, 0) | (1/2,none) SS (0, 0, 0) | (0,none) WW (2, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) |
| wage faker | (1/2,none) WW (1, 0.5, 0.5) | (0,none) WW (2, 0, 0) | (0,none) WW (2, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) WW (2, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) |
| committed whacker | (0,strike) WW (2, 0, 0) | (0,strike) SS (-1, -1, -1) | (0,strike) SS (-1, -1, -1) | (0,strike) SS (-1, -1, -1) | (0,strike) SS (-1, -1, -1) | (0,strike) SS (-1, -1, -1) | (0,strike) SS (-1, -1, -1) |

**Mixed pairs** (W1, W2) for the bosses that read W1 (probe, current-encounter and faker bosses):

| boss | T1, scab | scab, T1 | T1, T0 | T0, T1 | T1, strike | strike, scab | scab, strike | mil-, scab |
|---|---|---|---|---|---|---|---|---|
| D0 | (1/2,none) WW (1, 0.5, 0.5) | (0,none) WW (2, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WS (0.5, 0.5, 0) | (1/2,none) SW (0.5, 0, 0.5) | (0,none) WS (1, 0, 0) | (0,none) SW (1, 0, 0) |
| D0q | (1/4,none) SW (0.75, 0, 0.25) | (0,none) WS (1, 0, 0) | (1/4,none) SW (0.75, 0, 0.25) | (1/4,none) WS (0.75, 0.25, 0) | (1/4,none) SS (0, 0, 0) | (1/4,none) SW (0.75, 0, 0.25) | (0,none) WS (1, 0, 0) | (0,none) SW (1, 0, 0) |
| D0[L1] | (1/2,none) WW (1, 0.5, 0.5) | (0,none) WW (2, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WS (0.5, 0.5, 0) | (1/2,none) SW (0.5, 0, 0.5) | (0,none) WS (1, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) |
| D14 | (1/2,none) WW (1, 0.5, 0.5) | (0,none) WW (2, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (0,none) WW (2, 0, 0) | (1/2,none) WS (0.5, 0.5, 0) | (1/2,none) SW (0.5, 0, 0.5) | (0,none) WS (1, 0, 0) | (0,none) SW (1, 0, 0) |
| D* | (1/2,none) WW (1, 0.5, 0.5) | (0,none) WW (2, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/2,none) WS (0.5, 0.5, 0) | (1/2,none) SW (0.5, 0, 0.5) | (0,none) WS (1, 0, 0) | (0,none) SW (1, 0, 0) |
| D*[L1] | (1/2,none) WW (1, 0.5, 0.5) | (0,none) WW (2, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/2,none) WS (0.5, 0.5, 0) | (1/2,none) SW (0.5, 0, 0.5) | (0,none) WS (1, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) |
| C1 | (0,none) WW (2, 0, 0) | (0,none) WW (2, 0, 0) | (0,none) WW (2, 0, 0) | (0,none) WW (2, 0, 0) | (0,none) WS (1, 0, 0) | (1/2,none) SW (0.5, 0, 0.5) | (0,none) WS (1, 0, 0) | (0,none) SW (1, 0, 0) |
| wage faker | (0,none) WW (2, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (0,none) WW (2, 0, 0) | (0,none) WW (2, 0, 0) | (0,none) WS (1, 0, 0) | (0,none) SW (1, 0, 0) | (1/2,none) WS (0.5, 0.5, 0) | (1/2,none) WW (1, 0.5, 0.5) |
| committed whacker | (0,strike) SW (0.5, -1, 0) | (0,strike) WS (0.5, 0, -1) | (0,strike) SS (-1, -1, -1) | (0,strike) SS (-1, -1, -1) | (0,strike) SS (-1, -1, -1) | (0,strike) SW (0.5, -1, 0) | (0,strike) WS (0.5, 0, -1) | (0,strike) SW (0.5, -1, 0) |

Under RR (the 1/4-probe reads the executed play, and a rational worker works at 1/4, so no worker is certified to
strike at 1/4; at 0 the strike is a tie and resolves to the committed recommendation):

**Named workers** (union-run grammar, level-0 boxes about the current encounter):

- scab: `work`
- T0 (strike iff s = 0): `if(BOX(s in {0}),strike,work)`
- T1 = militant (strike iff s <= 1/4): `if(BOX(s in {0,1/4}),strike,work)`
- always strike: `strike`
- union: `f[BOX(s in {0,1/4}),BOX(QUORUM)]:WWWS`
- militant- (strike iff not BOX(s = 1/2)): `if(BOX(s in {1/2}),work,strike)`
- T0- (strike iff not BOX(s in {1/4,1/2})): `if(BOX(s in {1/4,1/2}),work,strike)`

**Named bosses** (`W_j(^(s,none))` = worker j's play against the quoted constant boss (s, none) beside the current other worker):

- (0,strike): `(0,strike)`
- (0,none): `(0,none)`
- (0,source): `(0,source)`
- (1/4,strike): `(1/4,strike)`
- (1/4,none): `(1/4,none)`
- (1/4,source): `(1/4,source)`
- (1/2,strike): `(1/2,strike)`
- (1/2,none): `(1/2,none)`
- (1/2,source): `(1/2,source)`
- D0 = if(BOX(W1(^0)=strike),(1/2,none),(0,none)): `if(BOX(W1(^(0,none))=strike),(1/2,none),(0,none))`
- D0q = if(BOX(W1(^0)=strike),(1/4,none),(0,none)): `if(BOX(W1(^(0,none))=strike),(1/4,none),(0,none))`
- D0[L1] = if(BOX1(W1(^0)=strike),(1/2,none),(0,none)): `if(BOX1(W1(^(0,none))=strike),(1/2,none),(0,none))`
- D14 = if(BOX(W1(^1/4)=strike),(1/2,none),(0,none)): `if(BOX(W1(^(1/4,none))=strike),(1/2,none),(0,none))`
- D* = if(BOX(W1(^1/4)=strike),(1/2,none),if(BOX(W1(^0)=strike),(1/4,none),(0,none))): `f[BOX(W1(^(0,none))=strike),BOX(W1(^(1/4,none))=strike)]:(0,none),(1/4,none),(1/2,none),(1/2,none)`
- D*[L1] (both probes BOX1): `f[BOX1(W1(^(0,none))=strike),BOX1(W1(^(1/4,none))=strike)]:(0,none),(1/4,none),(1/2,none),(1/2,none)`
- C1 = if(BOX(W1=strike),(1/2,none),(0,none)) (current-encounter concession): `if(BOX(W1=strike),(1/2,none),(0,none))`
- wage faker = if(BOX(W1=work),(1/2,none),(0,none)): `if(BOX(W1=work),(1/2,none),(0,none))`
- committed whacker (0,strike): `(0,strike)`

**What the probes read** (quoted self-pair play, executed / recommended; fv = first world from which the strike probe fails, 127 = never):

| worker pair | vs (0,none) | vs (1/4,none) | fv strike@0 L0 / L1 | fv strike@1/4 L0 / L1 |
|---|---|---|---|---|
| scab | WW / WW | WW / WW | 0 / 1 | 0 / 1 |
| T0 | SS / SS | WW / WW | 127 / 127 | 0 / 1 |
| T1 | SS / SS | WW / SS | 127 / 127 | 0 / 1 |
| strike | SS / SS | WW / SS | 127 / 127 | 0 / 1 |
| union | SS / SS | WW / WW | 127 / 127 | 0 / 1 |
| mil- | SS / SS | WW / SS | 0 / 127 | 0 / 1 |
| T0- | SS / SS | WW / WW | 0 / 127 | 0 / 1 |

**Play and payoffs (boss, W1, W2) of every named boss against every named worker self-pair** (RR):

| boss | scab | T0 | T1 | strike | union | mil- | T0- |
|---|---|---|---|---|---|---|---|
| (0,strike) | (0,none) WW (2, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) |
| (0,none) | (0,none) WW (2, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) |
| (0,source) | (0,none) WW (2, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) |
| (1/4,strike) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) |
| (1/4,none) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) |
| (1/4,source) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) |
| (1/2,strike) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) |
| (1/2,none) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) |
| (1/2,source) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) |
| D0 | (0,none) WW (2, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) |
| D0q | (0,none) WW (2, 0, 0) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) |
| D0[L1] | (0,none) WW (2, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) |
| D14 | (0,none) WW (2, 0, 0) | (0,none) WW (2, 0, 0) | (0,none) WW (2, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) WW (2, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) |
| D* | (0,none) WW (2, 0, 0) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) |
| D*[L1] | (0,none) WW (2, 0, 0) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) |
| C1 | (0,none) WW (2, 0, 0) | (0,none) WW (2, 0, 0) | (0,none) WW (2, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) WW (2, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) |
| wage faker | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) |
| committed whacker | (0,none) WW (2, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) |

**Mixed pairs** (W1, W2) for the bosses that read W1 (probe, current-encounter and faker bosses):

| boss | T1, scab | scab, T1 | T1, T0 | T0, T1 | T1, strike | strike, scab | scab, strike | mil-, scab |
|---|---|---|---|---|---|---|---|---|
| D0 | (1/2,none) WW (1, 0.5, 0.5) | (0,none) WW (2, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (0,none) WS (1, 0, 0) | (0,none) SW (1, 0, 0) |
| D0q | (1/4,none) WW (1.5, 0.25, 0.25) | (0,none) WS (1, 0, 0) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (0,none) WS (1, 0, 0) | (0,none) SW (1, 0, 0) |
| D0[L1] | (1/2,none) WW (1, 0.5, 0.5) | (0,none) WW (2, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (0,none) WS (1, 0, 0) | (1/2,none) WW (1, 0.5, 0.5) |
| D14 | (0,none) WW (2, 0, 0) | (0,none) WW (2, 0, 0) | (0,none) WW (2, 0, 0) | (0,none) WW (2, 0, 0) | (0,none) WS (1, 0, 0) | (0,none) SW (1, 0, 0) | (0,none) WS (1, 0, 0) | (0,none) SW (1, 0, 0) |
| D* | (1/4,none) WW (1.5, 0.25, 0.25) | (0,none) WW (2, 0, 0) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (0,none) WS (1, 0, 0) | (0,none) SW (1, 0, 0) |
| D*[L1] | (1/4,none) WW (1.5, 0.25, 0.25) | (0,none) WW (2, 0, 0) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (1/4,none) WW (1.5, 0.25, 0.25) | (0,none) WS (1, 0, 0) | (1/4,none) WW (1.5, 0.25, 0.25) |
| C1 | (0,none) WW (2, 0, 0) | (0,none) WW (2, 0, 0) | (0,none) WW (2, 0, 0) | (0,none) WW (2, 0, 0) | (0,none) WS (1, 0, 0) | (0,none) SW (1, 0, 0) | (0,none) WS (1, 0, 0) | (0,none) SW (1, 0, 0) |
| wage faker | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) | (1/2,none) WW (1, 0.5, 0.5) |
| committed whacker | (0,none) SW (1, 0, 0) | (0,none) WS (1, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SS (0, 0, 0) | (0,none) SW (1, 0, 0) | (0,none) WS (1, 0, 0) | (0,none) SW (1, 0, 0) |

### The Löb loops (world-by-world, CC)

- D0 = if(BOX(W1(^0)=strike),(1/2,none),(0,none)) || T1 = militant (strike iff s <= 1/4) pair: w0: (1/2,none) SS  boss atoms T → w1: (1/2,none) WW  boss atoms T → w2: (1/2,none) WW  boss atoms T → w3: (1/2,none) WW  boss atoms T → w4: (1/2,none) WW  boss atoms T → w5: (1/2,none) WW  boss atoms T
- D0 = if(BOX(W1(^0)=strike),(1/2,none),(0,none)) || T0 (strike iff s = 0) pair: w0: (1/2,none) SS  boss atoms T → w1: (1/2,none) WW  boss atoms T → w2: (1/2,none) WW  boss atoms T → w3: (1/2,none) WW  boss atoms T → w4: (1/2,none) WW  boss atoms T → w5: (1/2,none) WW  boss atoms T
- D0 = if(BOX(W1(^0)=strike),(1/2,none),(0,none)) || militant- (strike iff not BOX(s = 1/2)) pair: w0: (1/2,none) WW  boss atoms T → w1: (0,none) WW  boss atoms F → w2: (0,none) SS  boss atoms F → w3: (0,none) SS  boss atoms F → w4: (0,none) SS  boss atoms F → w5: (0,none) SS  boss atoms F
- D0q = if(BOX(W1(^0)=strike),(1/4,none),(0,none)) || T1 = militant (strike iff s <= 1/4) pair: w0: (1/4,none) SS  boss atoms T → w1: (1/4,none) SS  boss atoms T → w2: (1/4,none) SS  boss atoms T → w3: (1/4,none) SS  boss atoms T → w4: (1/4,none) SS  boss atoms T → w5: (1/4,none) SS  boss atoms T
- D0q = if(BOX(W1(^0)=strike),(1/4,none),(0,none)) || T0 (strike iff s = 0) pair: w0: (1/4,none) SS  boss atoms T → w1: (1/4,none) WW  boss atoms T → w2: (1/4,none) WW  boss atoms T → w3: (1/4,none) WW  boss atoms T → w4: (1/4,none) WW  boss atoms T → w5: (1/4,none) WW  boss atoms T
- D0q = if(BOX(W1(^0)=strike),(1/4,none),(0,none)) || militant- (strike iff not BOX(s = 1/2)) pair: w0: (1/4,none) WW  boss atoms T → w1: (0,none) SS  boss atoms F → w2: (0,none) SS  boss atoms F → w3: (0,none) SS  boss atoms F → w4: (0,none) SS  boss atoms F → w5: (0,none) SS  boss atoms F
- D* = if(BOX(W1(^1/4)=strike),(1/2,none),if(BOX(W1(^0)=strike),(1/4,none),(0,none))) || T1 = militant (strike iff s <= 1/4) pair: w0: (1/2,none) SS  boss atoms TT → w1: (1/2,none) WW  boss atoms TT → w2: (1/2,none) WW  boss atoms TT → w3: (1/2,none) WW  boss atoms TT → w4: (1/2,none) WW  boss atoms TT → w5: (1/2,none) WW  boss atoms TT
- D* = if(BOX(W1(^1/4)=strike),(1/2,none),if(BOX(W1(^0)=strike),(1/4,none),(0,none))) || T0 (strike iff s = 0) pair: w0: (1/2,none) SS  boss atoms TT → w1: (1/2,none) WW  boss atoms TT → w2: (1/4,none) WW  boss atoms TF → w3: (1/4,none) WW  boss atoms TF → w4: (1/4,none) WW  boss atoms TF → w5: (1/4,none) WW  boss atoms TF
- D* = if(BOX(W1(^1/4)=strike),(1/2,none),if(BOX(W1(^0)=strike),(1/4,none),(0,none))) || militant- (strike iff not BOX(s = 1/2)) pair: w0: (1/2,none) WW  boss atoms TT → w1: (0,none) WW  boss atoms FF → w2: (0,none) SS  boss atoms FF → w3: (0,none) SS  boss atoms FF → w4: (0,none) SS  boss atoms FF → w5: (0,none) SS  boss atoms FF
- D*[L1] (both probes BOX1) || T1 = militant (strike iff s <= 1/4) pair: w0: (1/2,none) SS  boss atoms TT → w1: (1/2,none) WW  boss atoms TT → w2: (1/2,none) WW  boss atoms TT → w3: (1/2,none) WW  boss atoms TT → w4: (1/2,none) WW  boss atoms TT → w5: (1/2,none) WW  boss atoms TT
- D*[L1] (both probes BOX1) || T0 (strike iff s = 0) pair: w0: (1/2,none) SS  boss atoms TT → w1: (1/2,none) WW  boss atoms TT → w2: (1/4,none) WW  boss atoms TF → w3: (1/4,none) WW  boss atoms TF → w4: (1/4,none) WW  boss atoms TF → w5: (1/4,none) WW  boss atoms TF
- D*[L1] (both probes BOX1) || militant- (strike iff not BOX(s = 1/2)) pair: w0: (1/2,none) WW  boss atoms TT → w1: (1/2,none) WW  boss atoms TT → w2: (1/2,none) WW  boss atoms TT → w3: (1/2,none) WW  boss atoms TT → w4: (1/2,none) WW  boss atoms TT → w5: (1/2,none) WW  boss atoms TT
- C1 = if(BOX(W1=strike),(1/2,none),(0,none)) (current-encounter concession) || T1 = militant (strike iff s <= 1/4) pair: w0: (1/2,none) SS  boss atoms T → w1: (1/2,none) WW  boss atoms T → w2: (0,none) WW  boss atoms F → w3: (0,none) WW  boss atoms F → w4: (0,none) WW  boss atoms F → w5: (0,none) WW  boss atoms F
- C1 = if(BOX(W1=strike),(1/2,none),(0,none)) (current-encounter concession) || T0 (strike iff s = 0) pair: w0: (1/2,none) SS  boss atoms T → w1: (1/2,none) WW  boss atoms T → w2: (0,none) WW  boss atoms F → w3: (0,none) WW  boss atoms F → w4: (0,none) WW  boss atoms F → w5: (0,none) WW  boss atoms F
- C1 = if(BOX(W1=strike),(1/2,none),(0,none)) (current-encounter concession) || militant- (strike iff not BOX(s = 1/2)) pair: w0: (1/2,none) WW  boss atoms T → w1: (0,none) WW  boss atoms F → w2: (0,none) SS  boss atoms F → w3: (0,none) SS  boss atoms F → w4: (0,none) SS  boss atoms F → w5: (0,none) SS  boss atoms F
- wage faker = if(BOX(W1=work),(1/2,none),(0,none)) || T1 = militant (strike iff s <= 1/4) pair: w0: (1/2,none) SS  boss atoms T → w1: (0,none) WW  boss atoms F → w2: (0,none) WW  boss atoms F → w3: (0,none) WW  boss atoms F → w4: (0,none) WW  boss atoms F → w5: (0,none) WW  boss atoms F
- wage faker = if(BOX(W1=work),(1/2,none),(0,none)) || T0 (strike iff s = 0) pair: w0: (1/2,none) SS  boss atoms T → w1: (0,none) WW  boss atoms F → w2: (0,none) WW  boss atoms F → w3: (0,none) WW  boss atoms F → w4: (0,none) WW  boss atoms F → w5: (0,none) WW  boss atoms F
- wage faker = if(BOX(W1=work),(1/2,none),(0,none)) || militant- (strike iff not BOX(s = 1/2)) pair: w0: (1/2,none) WW  boss atoms T → w1: (1/2,none) WW  boss atoms T → w2: (1/2,none) WW  boss atoms T → w3: (1/2,none) WW  boss atoms T → w4: (1/2,none) WW  boss atoms T → w5: (1/2,none) WW  boss atoms T

**The current-encounter concession C₁ = `if(BOX(W1=strike),(1/2,none),(0,none))` lands at (pay 0, work) against the
militant pair, not at (pay 0, strike)** as the spec's hand analysis had it: C₁ pays 1/2 at world 0 (its box is
vacuous there), the militants' `BOX(s ∈ {0,1/4})` fails at world 1 for ever, they work, C₁'s box then fails and it pays
0. The current-encounter concession is a world-0 wage faker. The probes behave as designed: D\* pays T₁ 1/2 and T₀ 1/4
(T₀ strikes at world 0 of the quoted 1/4-encounter, so the level-0 probe holds through world 1 and fails from world 2),
and only the level-1 probes certify militant⁻ (which works at world 0 of every quoted encounter).

### The accommodation ratchet, D\*'s unread slot, and the effective moves of the named states (P₀₁ and P₀, CC)

Per-mutant moves out of each named monomorphic state: class mass by slot and kind, the probability per mutation event
at N = 10⁴ (mass/3 · ρ), the heaviest move, and the best strict boss among the null (excluded two-atom) policies.

P₀₁:

| state | play | payoffs | strict B (mass; p/event at 10⁴) | neutral B | neutral W1 | neutral W2 | strict W | top move at N = 10⁴ | best excluded boss (gain; mass) |
|---|---|---|---|---|---|---|---|---|---|
| F*: D* | T1 | T1 | (1/2,none) WW | 1, 0.5, 0.5 | 0.0095; 6.3e-04 | 0.327 | 0.0027 | 0.499 | 0.0000 | W2 `work` (neutral-keep, Δ +0) | +1; 0.0021 |
| D*T0: D* | T0 | T0 | (1/4,none) WW | 1.5, 0.25, 0.25 | 0.0112; 5.2e-04 | 0.328 | 0.0040 | 0.499 | 0.0026 | W1 `if(BOX(s in {1/4}),strike,work)` (strict, Δ +0.25) | +0.5; 0.0024 |
| F*-: D*[L1] | militant- | militant- | (1/2,none) WW | 1, 0.5, 0.5 | 0.0000; 0.00 | 0.318 | 0.0053 | 0.499 | 0.0000 | W2 `work` (neutral-keep, Δ +0) | none; 0.0000 |
| F0: D0 | T1 | T1 | (1/2,none) WW | 1, 0.5, 0.5 | 0.0095; 6.3e-04 | 0.327 | 0.0027 | 0.499 | 0.0000 | W2 `work` (neutral-keep, Δ +0) | +1; 0.0021 |
| R0: D0 | T0 | T0 | (1/2,none) WW | 1, 0.5, 0.5 | 0.3393; 0.02 | 0.328 | 0.0027 | 0.499 | 0.0000 | B `(1/4,none)` (strict, Δ +0.5) | +1; 0.0066 |
| Q0: D0q | T0 | T0 | (1/4,none) WW | 1.5, 0.25, 0.25 | 0.0112; 5.2e-04 | 0.328 | 0.0040 | 0.499 | 0.0000 | W2 `work` (neutral-keep, Δ +0) | +0.5; 0.0024 |
| Fc: (1/2,none) | T1 | T1 | (1/2,none) WW | 1, 0.5, 0.5 | 0.0095; 6.3e-04 | 0.225 | 0.4988 | 0.499 | 0.0000 | W1 `work` (neutral-keep, Δ +0) | +1; 0.0021 |
| Fs: (1/2,none) | scab | scab | (1/2,none) WW | 1, 0.5, 0.5 | 0.6578; 0.04 | 0.226 | 0.0198 | 0.020 | 0.0000 | B `(0,none)` (strict, Δ +1) | +1; 0.0088 |
| Z: (0,none) | scab | scab | (0,none) WW | 2, 0, 0 | 0.0000; 0.00 | 0.226 | 0.5198 | 0.520 | 0.0000 | W1 `strike` (neutral-change, Δ +0) | none; 0.0000 |
| ZS: (0,none) | strike | strike | (0,none) SS | 0, 0, 0 | 0.0000; 0.00 | 0.555 | 0.5198 | 0.520 | 0.0000 | W1 `work` (neutral-change, Δ +0) | none; 0.0000 |
| ZT1: (0,none) | T1 | T1 | (0,none) SS | 0, 0, 0 | 0.3368; 0.03 | 0.331 | 0.9988 | 0.999 | 0.0000 | B `(1/2,strike)` (strict, Δ +1) | +2; 0.0062 |

P₀:

| state | play | payoffs | strict B (mass; p/event at 10⁴) | neutral B | neutral W1 | neutral W2 | strict W | top move at N = 10⁴ | best excluded boss (gain; mass) |
|---|---|---|---|---|---|---|---|---|---|
| F0: D0 | T1 | T1 | (1/2,none) WW | 1, 0.5, 0.5 | 0.0107; 7.1e-04 | 0.326 | 0.0027 | 0.499 | 0.0000 | W2 `work` (neutral-keep, Δ +0) | +1; 0.0022 |
| R0: D0 | T0 | T0 | (1/2,none) WW | 1, 0.5, 0.5 | 0.3385; 0.02 | 0.328 | 0.0027 | 0.499 | 0.0000 | B `(1/4,strike)` (strict, Δ +0.5) | +1; 0.0061 |
| Q0: D0q | T0 | T0 | (1/4,none) WW | 1.5, 0.25, 0.25 | 0.0107; 5.0e-04 | 0.328 | 0.0040 | 0.499 | 0.0000 | W2 `work` (neutral-keep, Δ +0) | +0.5; 0.0022 |
| Fc: (1/2,none) | T1 | T1 | (1/2,none) WW | 1, 0.5, 0.5 | 0.0107; 7.1e-04 | 0.224 | 0.4988 | 0.499 | 0.0000 | W1 `work` (neutral-keep, Δ +0) | +1; 0.0022 |
| Fs: (1/2,none) | scab | scab | (1/2,none) WW | 1, 0.5, 0.5 | 0.6584; 0.04 | 0.227 | 0.0198 | 0.020 | 0.0000 | B `(0,none)` (strict, Δ +1) | +1; 0.0083 |
| Z: (0,none) | scab | scab | (0,none) WW | 2, 0, 0 | 0.0000; 0.00 | 0.227 | 0.5198 | 0.520 | 0.0000 | W1 `strike` (neutral-change, Δ +0) | none; 0.0000 |
| ZS: (0,none) | strike | strike | (0,none) SS | 0, 0, 0 | 0.0000; 0.00 | 0.556 | 0.5198 | 0.520 | 0.0000 | W1 `work` (neutral-change, Δ +0) | none; 0.0000 |
| ZT1: (0,none) | T1 | T1 | (0,none) SS | 0, 0, 0 | 0.3372; 0.03 | 0.331 | 0.9988 | 0.999 | 0.0000 | B `(1/2,strike)` (strict, Δ +1) | +2; 0.0059 |

- **The ratchet is real (sol):** T₀ beside D₀ in the read slot is neutral (D₀ pays it 1/2); at (D₀, T₀, T₀) the
  constant 1/4 bosses invade strictly (+0.5; mass 0.34, 1.6·10⁻² per event at 10⁴) — no probe is needed for the cut.
- **D\* reverses it:** T₀ in D\*'s read slot is deleterious (−0.25), and at (D\*, T₀, T₀) the militant invades strictly
  (+0.25): against D\* demanding more pays.
- **But D\* reads one slot:** the unread slot W2 of F\* = (D\*, T₁, T₁) has neutral substitutes of mass 0.499, the scab
  first (demand 0).
- **Probes bring their own wage fakers:** `if(BOX(W1(^(0,none))=work),(1/2,·),(0,·))` and its kin pay 1/2 at world 0 (the
  probe is vacuous there), make the militants' low-wage box fail, then pay 0 for work: strict entry at F\*, F₀ and Fc of
  mass 0.0095 (6.3·10⁻⁴ per event, N-independent), plus 0.0021 among the null two-atom policies.
- **The unfakeable fair state** F\*⁻ = (D\*[L1], militant⁻, militant⁻) has no strict invader in the chain language or
  in the whole n = 11 grammar; its exits are the constant fair bosses (neutral, 0.31) and W2 (neutral, 0.499).

### Fakers by exhaustive search (chain language, CC)

- *Worker side (soundness certifies play against the quoted boss only):* 195 worker classes (mass 0.50; the constant
  striker 0.48 among them) are certified to strike against the 0-boss; 106 of them (0.012) work for ≤ 0 against some
  boss class; at 1/4, 128 classes (0.014).
- *Boss side:* 184 classes (mass 0.0083, of which probe-carrying 0.0055) pay < 1/2 with whack policy none for work from
  a self-pair that refuses every constant low wage; 684 coercers (mass 0.44: committed whackers). Wage fakers of the
  militant pair: P₀₁ 72 classes, 0.0032 (0.0021 probe-carrying); reference 24 classes, 0.0011.
- *Lemma 0 reference:* 0 boss classes get work from the militant⁻ pair at s < 1/2.

## Basin-to-basin rates (from the chain's own generator, before any π)

Basins by outcome summary (fair; 1/4 = intermediate; zero wage; whacking = realized repression); strike and
scab-split states are transient. Escape = Σ over the other basins of the effective rate (per mutation event);
next-basin probabilities; return fraction = the share of exits from the basin that come back before any other basin.

| cell | basin | π | escape / event | residence (events) | next: fair | next: 1/4 | next: zero | next: whacking | return fraction |
|---|---|---|---|---|---|---|---|---|---|
| P01_CC c=0.5 N=1000 | fair | 0.0040 | 2.1e-03 | 476 | – | 0.357 | 0.642 | 5.2e-04 | 0.011 |
| P01_CC c=0.5 N=1000 | 1/4 | 0.0129 | 1.2e-03 | 864 | 0.006 | – | 0.994 | 9.9e-06 | 3.4e-32 |
| P01_CC c=0.5 N=1000 | zero wage | 0.4806 | 4.3e-05 | 23012 | 0.389 | 0.544 | – | 0.066 | 0.753 |
| P01_CC c=0.5 N=1000 | whacking | 2.4e-05 | 0.06 | 17 | 0.178 | 0.403 | 0.419 | – | 0.002 |
| P01_CC c=0.5 N=1000 | (outside the four basins) | 0.502 | | | | | | | |
| P01_CC c=0.5 N=10000 | fair | 0.0086 | 1.0e-04 | 9928 | – | 0.363 | 0.636 | 1.2e-04 | 0.011 |
| P01_CC c=0.5 N=10000 | 1/4 | 0.0103 | 1.5e-04 | 6808 | 0.011 | – | 0.989 | 1.7e-08 | 0.000 |
| P01_CC c=0.5 N=10000 | zero wage | 0.4793 | 4.3e-06 | 230300 | 0.403 | 0.554 | – | 0.042 | 0.754 |
| P01_CC c=0.5 N=10000 | whacking | 1.8e-06 | 0.05 | 20 | 0.071 | 0.440 | 0.489 | – | 5.4e-04 |
| P01_CC c=0.5 N=10000 | (outside the four basins) | 0.502 | | | | | | | |
| P01_CC c=0.5 N=30000 | fair | 0.0091 | 3.1e-05 | 31962 | – | 0.360 | 0.640 | 1.2e-04 | 0.011 |
| P01_CC c=0.5 N=30000 | 1/4 | 0.0099 | 5.0e-05 | 20058 | 0.010 | – | 0.990 | 5.8e-09 | 0.000 |
| P01_CC c=0.5 N=30000 | zero wage | 0.4778 | 1.4e-06 | 699661 | 0.406 | 0.560 | – | 0.034 | 0.757 |
| P01_CC c=0.5 N=30000 | whacking | 4.9e-07 | 0.05 | 21 | 0.051 | 0.463 | 0.486 | – | 2.0e-04 |
| P01_CC c=0.5 N=30000 | (outside the four basins) | 0.503 | | | | | | | |
| P0_CC c=0.5 N=1000 | fair | 0.0039 | 2.1e-03 | 465 | – | 0.370 | 0.630 | 5.6e-04 | 0.010 |
| P0_CC c=0.5 N=1000 | 1/4 | 0.0140 | 1.1e-03 | 919 | 0.006 | – | 0.994 | 1.1e-05 | 3.5e-32 |
| P0_CC c=0.5 N=1000 | zero wage | 0.4796 | 4.4e-05 | 22801 | 0.386 | 0.550 | – | 0.065 | 0.752 |
| P0_CC c=0.5 N=1000 | whacking | 2.3e-05 | 0.06 | 17 | 0.174 | 0.407 | 0.419 | – | 0.002 |
| P0_CC c=0.5 N=1000 | (outside the four basins) | 0.502 | | | | | | | |
| P0_CC c=0.5 N=10000 | fair | 0.0043 | 2.1e-04 | 4720 | – | 0.374 | 0.626 | 1.2e-04 | 0.010 |
| P0_CC c=0.5 N=10000 | 1/4 | 0.0121 | 1.4e-04 | 7353 | 0.009 | – | 0.991 | 1.5e-08 | 0.000 |
| P0_CC c=0.5 N=10000 | zero wage | 0.4807 | 4.7e-06 | 212785 | 0.393 | 0.556 | – | 0.051 | 0.739 |
| P0_CC c=0.5 N=10000 | whacking | 2.2e-06 | 0.05 | 19 | 0.125 | 0.425 | 0.450 | – | 0.002 |
| P0_CC c=0.5 N=10000 | (outside the four basins) | 0.503 | | | | | | | |
| sham_CC c=0.5 N=1000 | fair | 0.0035 | 2.0e-03 | 498 | – | 0.361 | 0.638 | 3.3e-04 | 0.013 |
| sham_CC c=0.5 N=1000 | 1/4 | 0.0140 | 9.6e-04 | 1042 | 0.002 | – | 0.997 | 7.8e-06 | 4.3e-32 |
| sham_CC c=0.5 N=1000 | zero wage | 0.4747 | 3.9e-05 | 25833 | 0.378 | 0.576 | – | 0.047 | 0.778 |
| sham_CC c=0.5 N=1000 | whacking | 1.7e-05 | 0.05 | 19 | 0.058 | 0.416 | 0.526 | – | 7.9e-04 |
| sham_CC c=0.5 N=1000 | (outside the four basins) | 0.508 | | | | | | | |
| sham_CC c=0.5 N=10000 | fair | 0.0025 | 2.7e-04 | 3687 | – | 0.365 | 0.635 | 1.1e-04 | 0.011 |
| sham_CC c=0.5 N=10000 | 1/4 | 0.0095 | 1.4e-04 | 6957 | 0.005 | – | 0.995 | 1.8e-08 | 0.000 |
| sham_CC c=0.5 N=10000 | zero wage | 0.4794 | 3.8e-06 | 261249 | 0.373 | 0.586 | – | 0.042 | 0.779 |
| sham_CC c=0.5 N=10000 | whacking | 1.6e-06 | 0.05 | 21 | 0.012 | 0.428 | 0.560 | – | 2.4e-04 |
| sham_CC c=0.5 N=10000 | (outside the four basins) | 0.509 | | | | | | | |
| ref_CC c=0.5 N=1000 | fair | 0.0036 | 1.9e-03 | 525 | – | 0.362 | 0.638 | 1.6e-04 | 0.013 |
| ref_CC c=0.5 N=1000 | 1/4 | 0.0143 | 9.2e-04 | 1092 | 0.002 | – | 0.998 | 1.7e-07 | 4.5e-32 |
| ref_CC c=0.5 N=1000 | zero wage | 0.4750 | 3.8e-05 | 26638 | 0.378 | 0.575 | – | 0.047 | 0.782 |
| ref_CC c=0.5 N=1000 | whacking | 1.7e-05 | 0.05 | 20 | 0.051 | 0.419 | 0.530 | – | 5.7e-04 |
| ref_CC c=0.5 N=1000 | (outside the four basins) | 0.507 | | | | | | | |
| ref_CC c=0.5 N=10000 | fair | 0.0025 | 2.7e-04 | 3711 | – | 0.366 | 0.634 | 1.1e-04 | 0.010 |
| ref_CC c=0.5 N=10000 | 1/4 | 0.0096 | 1.4e-04 | 7278 | 0.005 | – | 0.995 | 1.9e-08 | 0.000 |
| ref_CC c=0.5 N=10000 | zero wage | 0.4798 | 3.7e-06 | 268296 | 0.373 | 0.584 | – | 0.043 | 0.783 |
| ref_CC c=0.5 N=10000 | whacking | 1.6e-06 | 0.05 | 21 | 0.011 | 0.429 | 0.559 | – | 2.2e-04 |
| ref_CC c=0.5 N=10000 | (outside the four basins) | 0.508 | | | | | | | |

- The fair basin's explored escape rate falls from 2.1·10⁻³ (N = 10³) to 1.0·10⁻⁴ (10⁴) in P₀₁ (factor 21), against
  1.9·10⁻³ → 2.7·10⁻⁴ (factor 7) in the reference and the sham and factor 10 in P₀. **The P₀₁ value at 10⁴ is
  biased low by the exploration cut** (next section): adding the dropped strict exits gives 4.3·10⁻⁴ (factor 4.9), and
  for P₀ 3.8·10⁻⁴ (factor 5.5); the reference changes little (3.0·10⁻⁴).
- The fair basin exits to zero wage (0.64) or to 1/4 (0.36) in every arm, almost never directly to whacking; its
  return fraction is ≈ 0.01. Per unit fair mass the exits are strict boss moves (P₀₁, 10⁴: 1.25·10⁻⁴ strict against
  3·10⁻⁶ neutral in the explored chain): the 0-boss cutting a fair state that holds a scab, and the wage fakers at the
  probe-concession states.
- The 1/4 basin exits to zero wage (0.99) with escape ≈ 1.4·10⁻⁴ at 10⁴ in every arm; zero wage is the sink
  (residence 2.3·10⁵ events at 10⁴).

## Chain: π, support and transitions

| cell | states (core) | fair | 1/4 | zero wage | strike | scab split | repression | efficiency | payoffs (B, W1, W2) | three-role | support 99% | outcome-changing cut | dense log-GTH check |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P01_CC c=0.5 N=100 | 21786 (2500) | 0.0053 | 0.0221 | 0.460 | 0.127 | 0.385 | 0.0002 | 1.360 | 1.340, 0.010, 0.010 | 0.0061 | 2338 | 0.004 | – |
| P01_CC c=0.5 N=1000 | 13692 (2500) | 0.0040 | 0.0129 | 0.481 | 0.123 | 0.380 | 2.4e-05 | 1.375 | 1.364, 0.005, 0.005 | 0.0046 | 937 | 0.009 | – |
| P01_CC c=0.5 N=10000 | 21913 (2500) | 0.0086 | 0.0103 | 0.479 | 0.126 | 0.376 | 1.8e-06 | 1.373 | 1.359, 0.007, 0.007 | 0.0098 | 450 | 0.094 | – |
| P01_CC c=0.5 N=30000 | 18515 (2500) | 0.0091 | 0.0099 | 0.478 | 0.126 | 0.377 | 4.9e-07 | 1.371 | 1.357, 0.007, 0.007 | 0.0104 | 375 | 0.216 | – |
| P0_CC c=0.5 N=1000 | 12603 (2500) | 0.0039 | 0.0140 | 0.480 | 0.122 | 0.380 | 2.3e-05 | 1.375 | 1.364, 0.006, 0.006 | 0.0045 | 683 | 0.009 | – |
| P0_CC c=0.5 N=10000 | 14226 (2500) | 0.0043 | 0.0121 | 0.481 | 0.125 | 0.378 | 2.2e-06 | 1.372 | 1.362, 0.005, 0.005 | 0.0049 | 526 | 0.045 | – |
| sham_CC c=0.5 N=100 | 11933 (2500) | 0.0050 | 0.0224 | 0.458 | 0.130 | 0.385 | 0.0002 | 1.355 | 1.336, 0.010, 0.010 | 0.0058 | 677 | 0.001 | – |
| sham_CC c=0.5 N=1000 | 4770 (1764) | 0.0035 | 0.0140 | 0.475 | 0.125 | 0.383 | 1.7e-05 | 1.367 | 1.356, 0.005, 0.005 | 0.0040 | 267 | 0.004 | TV 7.9e-15 |
| sham_CC c=0.5 N=10000 | 3999 (1138) | 0.0025 | 0.0095 | 0.479 | 0.125 | 0.383 | 1.6e-06 | 1.366 | 1.359, 0.004, 0.004 | 0.0029 | 215 | 0.011 | TV 2.3e-14 |
| ref_CC c=0.5 N=100 | 11729 (2500) | 0.0051 | 0.0225 | 0.458 | 0.132 | 0.383 | 0.0001 | 1.354 | 1.335, 0.010, 0.010 | 0.0058 | 660 | 0.001 | – |
| ref_CC c=0.5 N=1000 | 4648 (1752) | 0.0036 | 0.0143 | 0.475 | 0.127 | 0.380 | 1.7e-05 | 1.366 | 1.355, 0.006, 0.006 | 0.0041 | 254 | 0.004 | TV 1.2e-14 |
| ref_CC c=0.5 N=10000 | 3997 (1136) | 0.0025 | 0.0096 | 0.480 | 0.127 | 0.381 | 1.6e-06 | 1.365 | 1.357, 0.004, 0.004 | 0.0029 | 214 | 0.010 | TV 9.1e-15 |
| ref_CC c=0.5 N=30000 | 3932 (1136) | 0.0023 | 0.0086 | 0.479 | 0.128 | 0.382 | 5.2e-07 | 1.363 | 1.356, 0.003, 0.003 | 0.0026 | 218 | 0.017 | TV 1.2e-14 |
| P01_CC c=0.1 N=10000 | 22077 (2500) | 0.0084 | 0.0101 | 0.491 | 0.123 | 0.368 | 6.8e-06 | 1.386 | 1.373, 0.007, 0.007 | 0.0096 | 440 | 0.094 | – |
| ref_CC c=0.1 N=10000 | 4021 (1136) | 0.0024 | 0.0094 | 0.492 | 0.124 | 0.372 | 6.7e-06 | 1.379 | 1.372, 0.004, 0.004 | 0.0028 | 213 | 0.010 | TV 1.1e-14 |
| P01_CC c=0.5 N=10000_nofaker | 17848 (2500) | 0.0108 | 0.0106 | 0.478 | 0.125 | 0.375 | 1.8e-06 | 1.374 | 1.358, 0.008, 0.008 | 0.0124 | 594 | 0.092 | – |
| P01_RR c=0.5 N=1000 | 2688 (1451) | 0.0002 | 0.7595 | 0.235 | 2.0e-05 | 0.005 | 0.0000 | 1.995 | 1.615, 0.190, 0.190 | 0.0002 | 93 | 0.001 | TV 9.5e-15 |
| P01_RR c=0.5 N=10000 | 1495 (759) | 2.1e-05 | 0.7587 | 0.241 | 9.8e-07 | 5.1e-04 | 0.0000 | 1.999 | 1.620, 0.190, 0.190 | 2.1e-05 | 84 | 0.003 | TV 4.4e-15 |
| ref_RR c=0.5 N=1000 | 872 (678) | 9.6e-05 | 0.7518 | 0.243 | 2.3e-05 | 0.005 | 0.0000 | 1.995 | 1.619, 0.188, 0.188 | 9.6e-05 | 75 | 7.1e-04 | TV 6.1e-15 |
| ref_RR c=0.5 N=10000 | 348 (254) | 4.6e-06 | 0.7504 | 0.249 | 1.1e-06 | 5.7e-04 | 0.0000 | 1.999 | 1.624, 0.188, 0.188 | 4.6e-06 | 69 | 0.001 | TV 2.5e-15 |
| P01_CC+pool c=0.1 N=1000 | 9618 (2500) | 0.0001 | 0.0017 | 0.992 | 3.2e-05 | 0.005 | 0.0014 | 1.993 | 1.994, -0.000, -0.000 | 0.0001 | 481 | 0.010 | – |
| P01_CC+pool c=0.1 N=10000 | 6659 (1968) | 1.3e-05 | 0.0002 | 0.999 | 1.3e-06 | 5.0e-04 | 0.0001 | 1.999 | 1.999, -0.000, -0.000 | 1.3e-05 | 122 | 0.017 | – |
| P01_CC+pool c=0.5 N=1000 | 10198 (2500) | 0.0001 | 0.0036 | 0.984 | 1.4e-04 | 0.011 | 0.0013 | 1.987 | 1.986, 0.000, 0.000 | 0.0001 | 628 | 0.010 | – |
| P01_CC+pool c=0.5 N=10000 | 8080 (2156) | 5.5e-05 | 0.0033 | 0.995 | 4.6e-06 | 0.002 | 0.0001 | 1.998 | 1.996, 0.001, 0.001 | 5.5e-05 | 182 | 0.027 | – |

*Solver check:* where the explored set ≤ 6,000 states, an independent dense log-domain GTH (`solver_audit.solve_edges_log`)
reproduces the hybrid π to TV ≤ 2.3·10⁻¹⁴. 0 strict-NE triples exist in any class game (no candidate trap);
twin-expanded = lumped (monomorphic triples, exact behavioural classes).

**The exploration cut, and a correction** (`runs/concessions/cut_diagnostic.json`, `src/concessions_cutdiag.py`). At
θ = 10⁻⁹ the P₀₁ cells at N = 10⁴ and 3·10⁴ stop with 0.096 and 0.211 of the total flow leaving the explored set, to
3.6 and 3.0 million distinct unexplored states, each below θ; in the reference and the sham the cut is 0.014–0.021.
The diagnostic re-evaluates every edge leaving the explored set under the solved π: **in P₀₁ at 10⁴, 0.65 of the cut
flow leaves fair states** (0.77 at 3·10⁴), mostly into zero-wage (0.51) and 1/4 (0.26) states — the strict wage-faker
exits from the probe-concession fair states, spread over hundreds of faker classes of mass ~10⁻⁵ each, so every single
destination falls below θ. The restricted chain treats those edges as self-loops, so it *underestimates the fair
basin's escape* and *overestimates the fair share*. Per unit fair mass the dropped exit is 3.3·10⁻⁴ per event at 10⁴,
three times the explored escape (1.0·10⁻⁴). First-order correction (cut flow out of a basin added to its escape, entry
flux unchanged; exits into faker states do not return, since a concession boss is deleterious there):

| cell | cut / total flow | cut leaving fair | fair, explored | fair, cut-corrected | 1/4, explored | 1/4, cut-corrected |
|---|---|---|---|---|---|---|
| P₀₁ N = 10² | 0.006 | 0.04 | 0.0053 | 0.0052 | 0.0221 | 0.0220 |
| P₀₁ N = 10³ | 0.013 | 0.03 | 0.0040 | 0.0040 | 0.0129 | 0.0127 |
| P₀₁ N = 10⁴ | 0.096 | 0.65 | 0.0086 | **0.0020** | 0.0103 | 0.0089 |
| P₀₁ N = 3·10⁴ | 0.211 | 0.77 | 0.0091 | **0.0008** | 0.0099 | 0.0076 |
| P₀₁ N = 10⁴, fakers nulled | 0.121 | 0.70 | 0.0108 | 0.0019 | 0.0106 | 0.0088 |
| P₀ N = 10³ | 0.013 | 0.05 | 0.0039 | 0.0038 | 0.0140 | 0.0137 |
| P₀ N = 10⁴ | 0.047 | 0.35 | 0.0043 | 0.0024 | 0.0121 | 0.0106 |
| reference N = 10³ | 0.008 | 0.01 | 0.0036 | 0.0036 | 0.0143 | 0.0142 |
| reference N = 10⁴ | 0.014 | 0.12 | 0.0025 | 0.0023 | 0.0096 | 0.0094 |
| reference N = 3·10⁴ | 0.021 | 0.22 | 0.0023 | 0.0018 | 0.0086 | 0.0080 |
| sham N = 10⁴ | 0.015 | 0.13 | 0.0025 | 0.0023 | 0.0095 | 0.0092 |

*Threshold sensitivity (θ = 10⁻¹⁰, P₀₁ at 10⁴ and 3·10⁴):* unfinished. At θ = 10⁻¹⁰ the explored set kept growing round after round (N = 10⁴: 39 k states after round 1, outcome-changing cut 0.47, 86 min for that round; 3·10⁴: 41 k states after round 2, cut 0.73, ~95 min per round); both runs were stopped after ~2 h without a π. The cut diagnostic above is the sensitivity check that ran.

So the explored P₀₁ fair share at 10⁴–3·10⁴ (0.009), its rising log odds, and the 0.65 probe-boss share of the fair
mass at 10⁴ are exploration artefacts of the θ-pruned chain, the failure mode of the solver audit (θ-pruning misses
exits spread over many rare destinations). Cut-corrected, P₀₁ equals the reference at 10⁴ (0.0020 vs 0.0023) and
falls below it at 3·10⁴ (0.0008 vs 0.0018): the probe concessions bring their own wage fakers. The "fakers nulled"
cell is no exception: nulling the 184 classes identified as no-threat wage fakers of refusing self-pairs leaves the
probe fakers that exploit the militant pair under committed whack policies (counted as coercers there), and the
corrected fair share is unchanged (0.0019).

**Fair mass composition** (`runs/concessions/fairshare.json`, explored chain): probe-carrying bosses hold 0.11 / 0.22 /
0.65 of the fair mass at N = 10² / 10³ / 10⁴ in P₀₁ (P₀: 0.21 / 0.34); the 10⁴ value is inflated by the cut (above).
The unfakeable F\*⁻-type states (probe boss with militant⁻ beside it) hold 6·10⁻⁴ of π at 10⁴. Probe-concession
bosses (pay 1/2 to the militant pair, 0 to the scab pair) hold 0.0062 of π at 10⁴.

**N-scaling of the fair share** (log odds against ln N over 10²–3·10⁴, descriptive): explored P₀₁ −5.23, −5.52,
−4.75, −4.69 (slope +0.12); cut-corrected P₀₁ −5.25, −5.52, −6.21, −7.13 (slope −0.31); reference −5.27, −5.62,
−5.99, −6.07 explored (slope −0.14; −0.18 corrected). The fair share falls with N in every arm once the cut is
corrected; the union run's slope was −0.8 on the fair summary's exit.

| arm | N | fair | log odds |
|---|---|---|---|
| P01 | 100 | 0.0053 | -5.24 |
| P01 | 1000 | 0.0040 | -5.51 |
| P01 | 10000 | 0.0086 | -4.75 |
| P01 | 30000 | 0.0091 | -4.69 |
| ref | 100 | 0.0051 | -5.28 |
| ref | 1000 | 0.0036 | -5.63 |
| ref | 10000 | 0.0025 | -5.99 |
| ref | 30000 | 0.0023 | -6.09 |
| sham | 100 | 0.0050 | -5.29 |
| sham | 1000 | 0.0035 | -5.65 |
| sham | 10000 | 0.0025 | -5.97 |

### Support and transitions, main cells

P₀₁ CC, N = 10⁴:

| π | state (boss \| W1 \| W2) | play | summary | payoffs |
|---|---|---|---|---|
| 0.2019 | `(0,strike) \| work \| work` | (0,strike) WW | zero wage | 2, 0, 0 |
| 0.1109 | `(0,source) \| work \| work` | (0,source) WW | zero wage | 2, 0, 0 |
| 0.1099 | `(0,none) \| work \| work` | (0,none) WW | zero wage | 2, 0, 0 |
| 0.0890 | `(0,source) \| strike \| work` | (0,source) SW | scab split | 1, 0, 0 |
| 0.0889 | `(0,source) \| work \| strike` | (0,source) WS | scab split | 1, 0, 0 |
| 0.0881 | `(0,none) \| strike \| work` | (0,none) SW | scab split | 1, 0, 0 |
| 0.0880 | `(0,none) \| work \| strike` | (0,none) WS | scab split | 1, 0, 0 |
| 0.0620 | `(0,source) \| strike \| strike` | (0,source) SS | strike | 0, 0, 0 |
| 0.0614 | `(0,none) \| strike \| strike` | (0,none) SS | strike | 0, 0, 0 |
| 0.0028 | `(0,strike) \| if(BOX(h in {none,source}),strike,work) \| work` | (0,strike) WW | zero wage | 2, 0, 0 |

Transitions out of the top states (probability per mutation event):

- `(0,strike) | work | work` (π 0.2019): strict 0.00, neutral-change 7.3e-06, neutral-keep 1.6e-06; top: B neutral-change `(0,none)` → zero wage (3.4e-06, Δ +0); B neutral-change `(0,source)` → zero wage (3.4e-06, Δ +0); W1 neutral-keep `if(BOX(s in {0}),work,strike)` → zero wage (4.0e-08, Δ +0)
- `(0,source) | work | work` (π 0.1109): strict 0.00, neutral-change 4.1e-05, neutral-keep 1.5e-06; top: W1 neutral-change `strike` → scab split (1.6e-05, Δ +0); W2 neutral-change `strike` → scab split (1.6e-05, Δ +0); B neutral-change `(0,none)` → zero wage (3.4e-06, Δ +0)
- `(0,none) | work | work` (π 0.1099): strict 0.00, neutral-change 4.1e-05, neutral-keep 1.6e-06; top: W1 neutral-change `strike` → scab split (1.6e-05, Δ +0); W2 neutral-change `strike` → scab split (1.6e-05, Δ +0); B neutral-change `(0,strike)` → zero wage (3.4e-06, Δ +0)
- `(0,source) | strike | work` (π 0.0890): strict 0.00, neutral-change 3.7e-05, neutral-keep 1.5e-06; top: W1 neutral-change `work` → zero wage (1.6e-05, Δ +0); W2 neutral-change `strike` → strike (1.6e-05, Δ +0); B neutral-change `(0,none)` → scab split (3.4e-06, Δ +0)
- `(0,source) | work | strike` (π 0.0889): strict 0.00, neutral-change 3.7e-05, neutral-keep 1.5e-06; top: W1 neutral-change `strike` → strike (1.6e-05, Δ +0); W2 neutral-change `work` → zero wage (1.6e-05, Δ +0); B neutral-change `(0,none)` → scab split (3.4e-06, Δ +0)

Fair mass 0.0086; by boss class: `(1/2,none)` 0.0013; `(1/2,source)` 0.0011; `(1/2,strike)` 0.0006; `if(BOX(W2(^(1/4,none))=strike),(1/2,none),(0,strike))` 0.0002; `if(BOX(W2(^(0,none))=strike),(1/2,none),(0,strike))` 0.0002; `if(BOX(W2(^(1/4,none))=strike),(1/2,none),(0,none))` 0.0002.
By worker class (half per slot): `if(BOX(s in {0,1/4}),strike,work)` 0.0025; `work` 0.0019; `if(BOX(s in {1/2}),work,strike)` 0.0016; `if(BOX(QUORUM),work,strike)` 0.0003; `if(BOX(s in {0}),strike,work)` 0.0002; `if(BOX(s in {1/4}),strike,work)` 0.0001.
Fair exits (per unit fair mass per event): B strict 1.3e-04; B neutral-change 3.0e-06; W1 neutral-change 9.5e-08; B deleterious 0.00; W1 deleterious 0.00; W2 deleterious 0.00.
1/4 mass by boss class: `(1/4,source)` 0.0033; `(1/4,none)` 0.0033; `(1/4,strike)` 0.0026; `if(BOX1(W1(^(0,none))=strike),(1/4,none),(0,source))` 7.4e-05; `if(BOX1(W1(^(0,none))=strike),(1/4,none),(0,none))` 7.4e-05.
Probe-carrying boss present in 0.0101 of π; union in fair support 0.0002.

P₀₁ CC, N = 10³:

| π | state (boss \| W1 \| W2) | play | summary | payoffs |
|---|---|---|---|---|
| 0.1958 | `(0,strike) \| work \| work` | (0,strike) WW | zero wage | 2, 0, 0 |
| 0.1091 | `(0,source) \| work \| work` | (0,source) WW | zero wage | 2, 0, 0 |
| 0.1083 | `(0,none) \| work \| work` | (0,none) WW | zero wage | 2, 0, 0 |
| 0.0873 | `(0,source) \| work \| strike` | (0,source) WS | scab split | 1, 0, 0 |
| 0.0873 | `(0,source) \| strike \| work` | (0,source) SW | scab split | 1, 0, 0 |
| 0.0866 | `(0,none) \| work \| strike` | (0,none) WS | scab split | 1, 0, 0 |
| 0.0866 | `(0,none) \| strike \| work` | (0,none) SW | scab split | 1, 0, 0 |
| 0.0594 | `(0,source) \| strike \| strike` | (0,source) SS | strike | 0, 0, 0 |
| 0.0590 | `(0,none) \| strike \| strike` | (0,none) SS | strike | 0, 0, 0 |
| 0.0027 | `(0,strike) \| work \| if(BOX(h in {none,source}),strike,work)` | (0,strike) WW | zero wage | 2, 0, 0 |

Transitions out of the top states (probability per mutation event):

- `(0,strike) | work | work` (π 0.1958): strict 0.00, neutral-change 7.3e-05, neutral-keep 1.6e-05; top: B neutral-change `(0,none)` → zero wage (3.4e-05, Δ +0); B neutral-change `(0,source)` → zero wage (3.4e-05, Δ +0); W1 neutral-keep `if(BOX(s in {0}),work,strike)` → zero wage (4.0e-07, Δ +0)
- `(0,source) | work | work` (π 0.1091): strict 0.00, neutral-change 4.1e-04, neutral-keep 1.5e-05; top: W1 neutral-change `strike` → scab split (1.6e-04, Δ +0); W2 neutral-change `strike` → scab split (1.6e-04, Δ +0); B neutral-change `(0,none)` → zero wage (3.4e-05, Δ +0)
- `(0,none) | work | work` (π 0.1083): strict 0.00, neutral-change 4.1e-04, neutral-keep 1.6e-05; top: W1 neutral-change `strike` → scab split (1.6e-04, Δ +0); W2 neutral-change `strike` → scab split (1.6e-04, Δ +0); B neutral-change `(0,strike)` → zero wage (3.4e-05, Δ +0)
- `(0,source) | work | strike` (π 0.0873): strict 0.00, neutral-change 3.7e-04, neutral-keep 1.5e-05; top: W1 neutral-change `strike` → strike (1.6e-04, Δ +0); W2 neutral-change `work` → zero wage (1.6e-04, Δ +0); B neutral-change `(0,none)` → scab split (3.4e-05, Δ +0)
- `(0,source) | strike | work` (π 0.0873): strict 0.00, neutral-change 3.7e-04, neutral-keep 1.5e-05; top: W1 neutral-change `work` → zero wage (1.6e-04, Δ +0); W2 neutral-change `strike` → strike (1.6e-04, Δ +0); B neutral-change `(0,none)` → scab split (3.4e-05, Δ +0)

Fair mass 0.0040; by boss class: `(1/2,none)` 0.0014; `(1/2,source)` 0.0012; `(1/2,strike)` 0.0005; `if(BOX1(W1(^(0,none))=strike),(1/2,none),(0,none))` 2.7e-05; `if(BOX1(W1(^(1/4,none))=strike),(1/2,none),(0,source))` 2.5e-05; `if(BOX1(W1(^(1/4,none))=strike),(1/2,none),(0,none))` 2.5e-05.
By worker class (half per slot): `work` 0.0021; `if(BOX(s in {1/2}),work,strike)` 0.0012; `if(BOX(s in {0,1/4}),strike,work)` 0.0004; `if(BOX(QUORUM),work,strike)` 0.0003; `if(BOX(s in {0}),strike,work)` 1.6e-05; `if(BOX(s in {1/4,1/2}),work,strike)` 1.1e-05.
Fair exits (per unit fair mass per event): B strict 1.4e-03; B neutral-change 6.2e-05; B deleterious 1.3e-35; W1 deleterious 1.6e-67; W2 deleterious 1.6e-67.
1/4 mass by boss class: `(1/4,source)` 0.0042; `(1/4,none)` 0.0042; `(1/4,strike)` 0.0031; `if(BOX1(W1(^(0,none))=strike),(1/4,strike),(0,source))` 3.2e-05; `if(BOX1(W1(^(0,none))=strike),(1/4,strike),(0,none))` 3.2e-05.
Probe-carrying boss present in 0.0250 of π; union in fair support 8.4e-05.

Reference CC, N = 10⁴:

| π | state (boss \| W1 \| W2) | play | summary | payoffs |
|---|---|---|---|---|
| 0.2035 | `(0,strike) \| work \| work` | (0,strike) WW | zero wage | 2, 0, 0 |
| 0.1122 | `(0,source) \| work \| work` | (0,source) WW | zero wage | 2, 0, 0 |
| 0.1121 | `(0,none) \| work \| work` | (0,none) WW | zero wage | 2, 0, 0 |
| 0.0900 | `(0,source) \| work \| strike` | (0,source) WS | scab split | 1, 0, 0 |
| 0.0900 | `(0,source) \| strike \| work` | (0,source) SW | scab split | 1, 0, 0 |
| 0.0900 | `(0,none) \| work \| strike` | (0,none) WS | scab split | 1, 0, 0 |
| 0.0900 | `(0,none) \| strike \| work` | (0,none) SW | scab split | 1, 0, 0 |
| 0.0627 | `(0,none) \| strike \| strike` | (0,none) SS | strike | 0, 0, 0 |
| 0.0626 | `(0,source) \| strike \| strike` | (0,source) SS | strike | 0, 0, 0 |
| 0.0023 | `(0,strike) \| work \| if(BOX(h in {strike}),work,strike)` | (0,strike) WW | zero wage | 2, 0, 0 |

Transitions out of the top states (probability per mutation event):

- `(0,strike) | work | work` (π 0.2035): strict 0.00, neutral-change 6.9e-06, neutral-keep 1.4e-06; top: B neutral-change `(0,none)` → zero wage (3.4e-06, Δ +0); B neutral-change `(0,source)` → zero wage (3.4e-06, Δ +0); W1 neutral-keep `if(BOX(s in {0}),work,strike)` → zero wage (4.0e-08, Δ +0)
- `(0,source) | work | work` (π 0.1122): strict 0.00, neutral-change 4.0e-05, neutral-keep 1.3e-06; top: W1 neutral-change `strike` → scab split (1.6e-05, Δ +0); W2 neutral-change `strike` → scab split (1.6e-05, Δ +0); B neutral-change `(0,strike)` → zero wage (3.4e-06, Δ +0)
- `(0,none) | work | work` (π 0.1121): strict 0.00, neutral-change 4.0e-05, neutral-keep 1.4e-06; top: W1 neutral-change `strike` → scab split (1.6e-05, Δ +0); W2 neutral-change `strike` → scab split (1.6e-05, Δ +0); B neutral-change `(0,strike)` → zero wage (3.4e-06, Δ +0)
- `(0,source) | work | strike` (π 0.0900): strict 0.00, neutral-change 3.7e-05, neutral-keep 1.3e-06; top: W1 neutral-change `strike` → strike (1.6e-05, Δ +0); W2 neutral-change `work` → zero wage (1.6e-05, Δ +0); B neutral-change `(0,none)` → scab split (3.4e-06, Δ +0)
- `(0,source) | strike | work` (π 0.0900): strict 0.00, neutral-change 3.7e-05, neutral-keep 1.3e-06; top: W1 neutral-change `work` → zero wage (1.6e-05, Δ +0); W2 neutral-change `strike` → strike (1.6e-05, Δ +0); B neutral-change `(0,none)` → scab split (3.4e-06, Δ +0)

Fair mass 0.0025; by boss class: `(1/2,none)` 0.0011; `(1/2,source)` 0.0010; `(1/2,strike)` 0.0003; `if(BOX(W1=work),(1/2,none),(0,none))` 9.9e-07; `if(BOX(W1=work),(1/2,none),(0,source))` 6.6e-07; `if(BOX(W1=work),(1/2,strike),(0,none))` 6.6e-07.
By worker class (half per slot): `work` 0.0012; `if(BOX(s in {1/2}),work,strike)` 0.0011; `if(BOX(s in {0,1/4}),strike,work)` 0.0001; `if(BOX(QUORUM),work,strike)` 5.7e-05; `if(BOX(s in {1/4,1/2}),work,strike)` 5.8e-06; `if(BOX(s in {0}),strike,work)` 5.5e-06.
Fair exits (per unit fair mass per event): B strict 2.7e-04; B neutral-change 6.6e-06; W1 neutral-change 6.9e-12; W2 neutral-change 6.9e-12; B deleterious 0.00; W1 deleterious 0.00.
1/4 mass by boss class: `(1/4,source)` 0.0034; `(1/4,none)` 0.0034; `(1/4,strike)` 0.0025; `if(BOX(W2=strike),(1/2,strike),(1/4,none))` 1.3e-05; `if(BOX(W2=strike),(1/2,none),(1/4,none))` 1.3e-05.
Probe-carrying boss present in 0.0000 of π; union in fair support 2.8e-05.

P₀ CC, N = 10⁴:

| π | state (boss \| W1 \| W2) | play | summary | payoffs |
|---|---|---|---|---|
| 0.1958 | `(0,strike) \| work \| work` | (0,strike) WW | zero wage | 2, 0, 0 |
| 0.1090 | `(0,source) \| work \| work` | (0,source) WW | zero wage | 2, 0, 0 |
| 0.1080 | `(0,none) \| work \| work` | (0,none) WW | zero wage | 2, 0, 0 |
| 0.0876 | `(0,source) \| strike \| work` | (0,source) SW | scab split | 1, 0, 0 |
| 0.0875 | `(0,source) \| work \| strike` | (0,source) WS | scab split | 1, 0, 0 |
| 0.0867 | `(0,none) \| strike \| work` | (0,none) SW | scab split | 1, 0, 0 |
| 0.0867 | `(0,none) \| work \| strike` | (0,none) WS | scab split | 1, 0, 0 |
| 0.0608 | `(0,source) \| strike \| strike` | (0,source) SS | strike | 0, 0, 0 |
| 0.0603 | `(0,none) \| strike \| strike` | (0,none) SS | strike | 0, 0, 0 |
| 0.0028 | `(0,strike) \| if(BOX(h in {none,source}),strike,work) \| work` | (0,strike) WW | zero wage | 2, 0, 0 |

Transitions out of the top states (probability per mutation event):

- `(0,strike) | work | work` (π 0.1958): strict 0.00, neutral-change 7.3e-06, neutral-keep 1.6e-06; top: B neutral-change `(0,none)` → zero wage (3.4e-06, Δ +0); B neutral-change `(0,source)` → zero wage (3.4e-06, Δ +0); W1 neutral-keep `if(BOX(s in {0}),work,strike)` → zero wage (4.0e-08, Δ +0)
- `(0,source) | work | work` (π 0.1090): strict 0.00, neutral-change 4.1e-05, neutral-keep 1.5e-06; top: W1 neutral-change `strike` → scab split (1.6e-05, Δ +0); W2 neutral-change `strike` → scab split (1.6e-05, Δ +0); B neutral-change `(0,none)` → zero wage (3.4e-06, Δ +0)
- `(0,none) | work | work` (π 0.1080): strict 0.00, neutral-change 4.1e-05, neutral-keep 1.6e-06; top: W1 neutral-change `strike` → scab split (1.6e-05, Δ +0); W2 neutral-change `strike` → scab split (1.6e-05, Δ +0); B neutral-change `(0,strike)` → zero wage (3.4e-06, Δ +0)
- `(0,source) | strike | work` (π 0.0876): strict 0.00, neutral-change 3.7e-05, neutral-keep 1.5e-06; top: W1 neutral-change `work` → zero wage (1.6e-05, Δ +0); W2 neutral-change `strike` → strike (1.6e-05, Δ +0); B neutral-change `(0,none)` → scab split (3.4e-06, Δ +0)
- `(0,source) | work | strike` (π 0.0875): strict 0.00, neutral-change 3.7e-05, neutral-keep 1.5e-06; top: W1 neutral-change `strike` → strike (1.6e-05, Δ +0); W2 neutral-change `work` → zero wage (1.6e-05, Δ +0); B neutral-change `(0,none)` → scab split (3.4e-06, Δ +0)

Fair mass 0.0043; by boss class: `(1/2,none)` 0.0012; `(1/2,source)` 0.0011; `(1/2,strike)` 0.0005; `if(BOX1(W1(^(0,none))=strike),(1/2,none),(0,source))` 8.0e-05; `if(BOX1(W2(^(0,none))=strike),(1/2,none),(0,source))` 7.9e-05; `if(BOX1(W2(^(0,none))=strike),(1/2,none),(0,none))` 7.9e-05.
By worker class (half per slot): `work` 0.0017; `if(BOX(s in {1/2}),work,strike)` 0.0015; `if(BOX(s in {0,1/4}),strike,work)` 0.0006; `if(BOX(QUORUM),work,strike)` 0.0002; `if(BOX(s in {0}),strike,work)` 0.0002; `if(BOX(h in {none}),strike,work)` 6.9e-05.
Fair exits (per unit fair mass per event): B strict 2.0e-04; B neutral-change 5.3e-06; B deleterious 0.00; W1 deleterious 0.00; W2 deleterious 0.00.
1/4 mass by boss class: `(1/4,source)` 0.0035; `(1/4,none)` 0.0034; `(1/4,strike)` 0.0028; `if(BOX1(W1(^(0,none))=strike),(1/4,none),(0,source))` 0.0001; `if(BOX1(W1(^(0,none))=strike),(1/4,none),(0,none))` 0.0001.
Probe-carrying boss present in 0.0159 of π; union in fair support 7.1e-05.

P₀₁ RR, N = 10⁴:

| π | state (boss \| W1 \| W2) | play | summary | payoffs |
|---|---|---|---|---|
| 0.2320 | `(1/4,strike) \| strike \| strike` | (1/4,none) WW | intermediate | 1.5, 0.25, 0.25 |
| 0.2284 | `(1/4,strike) \| strike \| work` | (1/4,none) WW | intermediate | 1.5, 0.25, 0.25 |
| 0.2284 | `(1/4,strike) \| work \| strike` | (1/4,none) WW | intermediate | 1.5, 0.25, 0.25 |
| 0.2195 | `(0,strike) \| work \| work` | (0,none) WW | zero wage | 2, 0, 0 |
| 0.0028 | `if(BOX(W1=work),(0,strike),(1/4,strike)) \| strike \| work` | (1/4,none) WW | intermediate | 1.5, 0.25, 0.25 |
| 0.0028 | `if(BOX(W2=work),(0,strike),(1/4,strike)) \| work \| strike` | (1/4,none) WW | intermediate | 1.5, 0.25, 0.25 |
| 0.0025 | `(1/4,strike) \| strike \| if(BOX(s in {1/4}),work,strike)` | (1/4,none) WW | intermediate | 1.5, 0.25, 0.25 |
| 0.0025 | `(1/4,strike) \| if(BOX(s in {1/4}),work,strike) \| strike` | (1/4,none) WW | intermediate | 1.5, 0.25, 0.25 |
| 0.0025 | `(1/4,strike) \| work \| if(BOX(s in {1/4}),work,strike)` | (1/4,none) WW | intermediate | 1.5, 0.25, 0.25 |
| 0.0025 | `(1/4,strike) \| if(BOX(s in {1/4}),work,strike) \| work` | (1/4,none) WW | intermediate | 1.5, 0.25, 0.25 |

Transitions out of the top states (probability per mutation event):

- `(1/4,strike) | strike | strike` (π 0.2320): strict 0.00, neutral-change 0.00, neutral-keep 3.5e-05; top: W1 neutral-keep `work` → intermediate (1.6e-05, Δ +0); W2 neutral-keep `work` → intermediate (1.6e-05, Δ +0); W1 neutral-keep `if(BOX(s in {1/4}),work,strike)` → intermediate (1.8e-07, Δ +0)
- `(1/4,strike) | strike | work` (π 0.2284): strict 0.00, neutral-change 0.00, neutral-keep 3.5e-05; top: W1 neutral-keep `work` → intermediate (1.6e-05, Δ +0); W2 neutral-keep `strike` → intermediate (1.6e-05, Δ +0); W1 neutral-keep `if(BOX(s in {1/4}),work,strike)` → intermediate (1.8e-07, Δ +0)
- `(1/4,strike) | work | strike` (π 0.2284): strict 0.00, neutral-change 0.00, neutral-keep 3.5e-05; top: W1 neutral-keep `strike` → intermediate (1.6e-05, Δ +0); W2 neutral-keep `work` → intermediate (1.6e-05, Δ +0); W1 neutral-keep `if(BOX(s in {1/4}),work,strike)` → intermediate (1.8e-07, Δ +0)
- `(0,strike) | work | work` (π 0.2195): strict 0.00, neutral-change 3.3e-05, neutral-keep 1.5e-06; top: W1 neutral-change `strike` → scab split (1.6e-05, Δ +0); W2 neutral-change `strike` → scab split (1.6e-05, Δ +0); W1 neutral-change `if(BOX(s in {1/4}),work,strike)` → scab split (1.8e-07, Δ +0)
- `if(BOX(W1=work),(0,strike),(1/4,strike)) | strike | work` (π 0.0028): strict 0.00, neutral-change 0.00, neutral-keep 2.9e-05; top: W2 neutral-keep `strike` → intermediate (1.6e-05, Δ +0); B neutral-keep `(1/4,strike)` → intermediate (1.1e-05, Δ +0); W1 neutral-keep `if(BOX(s in {1/4}),work,strike)` → intermediate (1.8e-07, Δ +0)

Fair mass 2.1e-05; by boss class: `(1/2,strike)` 2.2e-06; `if(BOX(W2=work),(0,strike),(1/2,strike))` 1.7e-06; `if(BOX(W1=work),(0,strike),(1/2,strike))` 1.7e-06; `if(BOX1(W2(^(0,none))=strike),(1/2,strike),(0,strike))` 1.1e-06; `if(BOX1(W1(^(0,none))=strike),(1/2,strike),(0,strike))` 1.1e-06; `if(BOX(W2(^(0,none))=strike),(1/2,strike),(0,strike))` 1.1e-06.
By worker class (half per slot): `strike` 1.2e-05; `work` 7.5e-06; `if(BOX(s in {0,1/4}),strike,work)` 3.4e-07; `if(BOX(OTHER=strike),strike,work)` 2.8e-07; `if(BOX(QUORUM),strike,work)` 2.8e-07; `if(BOX(OTHER=work),work,strike)` 2.7e-07.
Fair exits (per unit fair mass per event): B strict 0.02; B neutral-change 6.0e-06; W1 deleterious 0.00; W2 deleterious 0.00; B deleterious 0.00.
1/4 mass by boss class: `(1/4,strike)` 0.7306; `if(BOX(W1=work),(0,strike),(1/4,strike))` 0.0047; `if(BOX(W2=work),(0,strike),(1/4,strike))` 0.0047; `if(BOX1(W1(^(0,none))=strike),(1/4,strike),(0,strike))` 0.0027; `if(BOX1(W2(^(0,none))=strike),(1/4,strike),(0,strike))` 0.0027.
Probe-carrying boss present in 0.0175 of π; union in fair support 0.0006.

P₀₁ CC + pool, c = 0.1, N = 10⁴:

| π | state (boss \| W1 \| W2) | play | summary | payoffs |
|---|---|---|---|---|
| 0.7352 | `(0,strike) \| work \| work` | (0,strike) WW | zero wage | 2, 0, 0 |
| 0.0844 | `(0,source) \| work \| work` | (0,source) WW | zero wage | 2, 0, 0 |
| 0.0838 | `(0,none) \| work \| work` | (0,none) WW | zero wage | 2, 0, 0 |
| 0.0037 | `(0,strike) \| work \| if(BOX(h in {none,source}),strike,work)` | (0,strike) WW | zero wage | 2, 0, 0 |
| 0.0037 | `(0,strike) \| if(BOX(h in {none,source}),strike,work) \| work` | (0,strike) WW | zero wage | 2, 0, 0 |
| 0.0032 | `(0,strike) \| work \| if(BOX(h in {none}),strike,work)` | (0,strike) WW | zero wage | 2, 0, 0 |
| 0.0032 | `(0,strike) \| if(BOX(h in {none}),strike,work) \| work` | (0,strike) WW | zero wage | 2, 0, 0 |
| 0.0030 | `(0,strike) \| work \| if(BOX(h in {strike}),work,strike)` | (0,strike) WW | zero wage | 2, 0, 0 |
| 0.0030 | `(0,strike) \| if(BOX(h in {strike}),work,strike) \| work` | (0,strike) WW | zero wage | 2, 0, 0 |
| 0.0026 | `(0,strike) \| work \| if(BOX(h in {strike,source}),work,strike)` | (0,strike) WW | zero wage | 2, 0, 0 |

Transitions out of the top states (probability per mutation event):

- `(0,strike) | work | work` (π 0.7352): strict 0.00, neutral-change 7.3e-06, neutral-keep 1.6e-06; top: B neutral-change `(0,none)` → zero wage (3.4e-06, Δ +0); B neutral-change `(0,source)` → zero wage (3.4e-06, Δ +0); W1 neutral-keep `if(BOX(s in {0}),work,strike)` → zero wage (4.0e-08, Δ +0)
- `(0,source) | work | work` (π 0.0844): strict 0.00, neutral-change 4.1e-05, neutral-keep 1.5e-06; top: W1 neutral-change `strike` → scab split (1.6e-05, Δ +0); W2 neutral-change `strike` → scab split (1.6e-05, Δ +0); B neutral-change `(0,none)` → zero wage (3.4e-06, Δ +0)
- `(0,none) | work | work` (π 0.0838): strict 0.00, neutral-change 4.1e-05, neutral-keep 1.6e-06; top: W1 neutral-change `strike` → scab split (1.6e-05, Δ +0); W2 neutral-change `strike` → scab split (1.6e-05, Δ +0); B neutral-change `(0,strike)` → zero wage (3.4e-06, Δ +0)
- `(0,strike) | work | if(BOX(h in {none,source}),strike,work)` (π 0.0037): strict 0.00, neutral-change 9.7e-08, neutral-keep 1.8e-05; top: W2 neutral-keep `work` → zero wage (1.6e-05, Δ +0); W1 neutral-keep `if(BOX(s in {0}),work,strike)` → zero wage (4.0e-08, Δ +0); W1 neutral-keep `if(BOX(s in {1/4}),strike,work)` → zero wage (4.0e-08, Δ +0)
- `(0,strike) | if(BOX(h in {none,source}),strike,work) | work` (π 0.0037): strict 0.00, neutral-change 9.7e-08, neutral-keep 1.8e-05; top: W1 neutral-keep `work` → zero wage (1.6e-05, Δ +0); W1 neutral-keep `if(BOX(s in {0}),work,strike)` → zero wage (4.0e-08, Δ +0); W1 neutral-keep `if(BOX(s in {1/4}),strike,work)` → zero wage (4.0e-08, Δ +0)

Fair mass 1.3e-05; by boss class: `(1/2,strike)` 2.6e-07; `if(BOX(W1=work),(0,none),(1/2,strike))` 1.3e-07; `if(BOX(W2=work),(0,none),(1/2,strike))` 1.3e-07; `if(BOX(W1=work),(0,none),(1/2,source))` 1.2e-07; `if(BOX(W2=work),(0,none),(1/2,source))` 1.2e-07; `if(BOX(W1=work),(0,none),(1/2,none))` 1.2e-07.
By worker class (half per slot): `work` 7.4e-06; `if(BOX(s in {0,1/4}),strike,work)` 1.7e-06; `if(BOX(h in {none}),strike,work)` 6.0e-07; `if(BOX(h in {none,source}),strike,work)` 5.6e-07; `if(BOX(s in {0}),strike,work)` 5.5e-07; `if(BOX(s in {1/4}),strike,work)` 3.7e-07.
Fair exits (per unit fair mass per event): B strict 8.8e-03; B neutral-change 2.0e-06; W2 neutral-change 5.4e-10; W1 neutral-change 5.4e-10; B deleterious 4.4e-137; W1 deleterious 0.00.
1/4 mass by boss class: `(1/4,strike)` 0.0001; `(1/4,source)` 6.0e-06; `(1/4,none)` 5.6e-06; `if(BOX(W1=work),(0,none),(1/4,strike))` 3.7e-07; `if(BOX(W2=work),(0,none),(1/4,strike))` 3.7e-07.
Probe-carrying boss present in 0.0078 of π; union in fair support 2.1e-05.

### Preservation of demands under neutral worker substitution

For the fair states carrying 0.99 of the fair mass (up to 2,000 states): the fair π-fraction with a demand-lowering
neutral worker substitute, the fraction where some boss class strictly invades once that substitute has fixed, and
the prior mass of the neutral substitutes by demand relative to the resident replaced (π-weighted mean).

| cell | fair mass | analysed | with a demand-lowering neutral substitute | ... after which a boss strictly invades | neutral substitute mass: same / lower / higher demand |
|---|---|---|---|---|---|
| P01_CC c=0.5 N=100 | 0.0053 | 0.0043 | 0.714 | 0.714 | 0.024 / 0.350 / 0.012 |
| P01_CC c=0.5 N=1000 | 0.0040 | 0.0040 | 0.961 | 0.959 | 0.016 / 0.377 / 0.010 |
| P01_CC c=0.5 N=10000 | 0.0086 | 0.0083 | 0.998 | 0.995 | 0.010 / 0.386 / 0.005 |
| P01_CC c=0.5 N=30000 | 0.0091 | 0.0058 | 1.000 | 0.999 | 0.010 / 0.329 / 0.007 |
| P0_CC c=0.5 N=1000 | 0.0039 | 0.0034 | 0.966 | 0.966 | 0.014 / 0.408 / 0.010 |
| P0_CC c=0.5 N=10000 | 0.0043 | 0.0043 | 0.997 | 0.995 | 0.013 / 0.436 / 0.008 |
| sham_CC c=0.5 N=100 | 0.0050 | 0.0046 | 0.717 | 0.717 | 0.023 / 0.354 / 0.012 |
| sham_CC c=0.5 N=1000 | 0.0035 | 0.0034 | 0.964 | 0.962 | 0.015 / 0.473 / 0.010 |
| sham_CC c=0.5 N=10000 | 0.0025 | 0.0025 | 0.995 | 0.992 | 0.014 / 0.496 / 0.010 |
| ref_CC c=0.5 N=100 | 0.0051 | 0.0047 | 0.707 | 0.707 | 0.024 / 0.348 / 0.012 |
| ref_CC c=0.5 N=1000 | 0.0036 | 0.0035 | 0.963 | 0.961 | 0.015 / 0.473 / 0.010 |
| ref_CC c=0.5 N=10000 | 0.0025 | 0.0025 | 0.995 | 0.992 | 0.014 / 0.496 / 0.010 |
| ref_CC c=0.5 N=30000 | 0.0023 | 0.0022 | 0.998 | 0.996 | 0.014 / 0.498 / 0.010 |
| P01_CC c=0.1 N=10000 | 0.0084 | 0.0052 | 0.998 | 0.998 | 0.011 / 0.385 / 0.007 |
| ref_CC c=0.1 N=10000 | 0.0024 | 0.0024 | 0.995 | 0.993 | 0.014 / 0.496 / 0.010 |
| P01_CC c=0.5 N=10000_nofaker | 0.0108 | 0.0062 | 0.998 | 0.998 | 0.010 / 0.386 / 0.006 |
| P01_RR c=0.5 N=1000 | 0.0002 | 0.0002 | 0.717 | 0.717 | 0.071 / 0.369 / 0.279 |
| P01_RR c=0.5 N=10000 | 2.1e-05 | 2.0e-05 | 0.644 | 0.644 | 0.093 / 0.285 / 0.271 |
| ref_RR c=0.5 N=1000 | 9.6e-05 | 9.5e-05 | 0.999 | 0.999 | 0.127 / 0.634 / 0.281 |
| ref_RR c=0.5 N=10000 | 4.6e-06 | 4.6e-06 | 0.986 | 0.986 | 0.263 / 0.477 / 0.276 |
| P01_CC+pool c=0.1 N=1000 | 0.0001 | 1.9e-05 | 0.422 | 0.422 | 0.015 / 6.6e-04 / 0.014 |
| P01_CC+pool c=0.1 N=10000 | 1.3e-05 | 2.2e-06 | 0.884 | 0.884 | 0.013 / 0.001 / 0.010 |
| P01_CC+pool c=0.5 N=1000 | 0.0001 | 2.9e-05 | 1.000 | 1.000 | 0.014 / 0.038 / 0.010 |
| P01_CC+pool c=0.5 N=10000 | 5.5e-05 | 3.6e-05 | 1.000 | 1.000 | 0.004 / 0.508 / 0.005 |

In every arm the demand-lowering substitute is first the scab (demand 0; prior mass 0.48), then T₀ beside a militant
(demand 0 at the 1/4-boss), and the strict boss after it is the 0-boss or the constant 1/4 boss.

## Reduced chains over the named programs (not preregistered)

Exact chains over the named bosses × the seven named workers (the union run's reduced canonical chain), under a uniform
prior over the listed programs and under their length-prior masses; fair / 1/4 / zero wage.

| evaluator | boss set | prior | N = 10² fair / 1/4 / zero | N = 10³ | N = 10⁴ | N = 10⁵ | top state at 10⁴ (π) |
|---|---|---|---|---|---|---|---|
| CC pool0 c0.5 | constants | uniform | 0.091 / 0.597 / 0.269 | 0.080 / 0.581 / 0.309 | 0.079 / 0.579 / 0.314 | 0.078 / 0.579 / 0.314 | `(0,strike) | work | f[BOX(s in {0,1/4}),BOX(QUORUM)]:WWWS` (0.091) |
| CC pool0 c0.5 | constants | length | 0.005 / 0.015 / 0.433 | 0.005 / 0.010 / 0.444 | 0.005 / 0.009 / 0.445 | 0.005 / 0.009 / 0.445 | `(0,strike) | work | work` (0.197) |
| CC pool0 c0.5 | +D0 family (P0) | uniform | 0.151 / 0.775 / 0.058 | 0.110 / 0.837 / 0.046 | 0.105 / 0.845 / 0.044 | 0.104 / 0.846 / 0.044 | `if(BOX(W1(^(0,none))=strike),(1/4,none),(0,none)) | f[BOX(s in {0,1/4}),BOX(QUORUM)]:WWWS | if(BOX(s in {0}),strike,work)` (0.081) |
| CC pool0 c0.5 | +D0 family (P0) | length | 0.005 / 0.015 / 0.432 | 0.005 / 0.010 / 0.444 | 0.006 / 0.010 / 0.444 | 0.008 / 0.011 / 0.443 | `(0,strike) | work | work` (0.197) |
| CC pool0 c0.5 | +D0 family, D14 | uniform | 0.666 / 0.256 / 0.052 | 0.773 / 0.191 / 0.024 | 0.787 / 0.183 / 0.019 | 0.788 / 0.182 / 0.019 | `if(BOX(W1(^(1/4,none))=strike),(1/2,none),(0,none)) | f[BOX(s in {0,1/4}),BOX(QUORUM)]:WWWS | f[BOX(s in {0,1/4}),BOX(QUORUM)]:WWWS` (0.070) |
| CC pool0 c0.5 | +D0 family, D14 | length | 0.005 / 0.015 / 0.432 | 0.005 / 0.010 / 0.444 | 0.007 / 0.009 / 0.444 | 0.013 / 0.007 / 0.442 | `(0,strike) | work | work` (0.196) |
| CC pool0 c0.5 | +D0 family, D14, D* family | uniform | 0.871 / 0.095 / 0.020 | 0.965 / 0.028 / 0.004 | 0.977 / 0.020 / 0.002 | 0.978 / 0.019 / 0.002 | `f[BOX(W2(^(1/4,none))=strike),BOX1(W2(^(0,none))=strike)]:(0,none),(1/2,none),(1/4,none),(1/2,none) | if(BOX(s in {0,1/4}),strike,work) | f[BOX(s in {0,1/4}),BOX(QUORUM)]:WWWS` (0.037) |
| CC pool0 c0.5 | +D0 family, D14, D* family | length | 0.005 / 0.015 / 0.432 | 0.005 / 0.010 / 0.444 | 0.007 / 0.009 / 0.444 | 0.013 / 0.007 / 0.442 | `(0,strike) | work | work` (0.196) |
| CC pool0 c0.5 | +D* family only | uniform | 0.876 / 0.098 / 0.015 | 0.960 / 0.032 / 0.005 | 0.969 / 0.024 / 0.004 | 0.970 / 0.023 / 0.003 | `f[BOX(W2(^(1/4,none))=strike),BOX1(W2(^(0,none))=strike)]:(0,none),(1/2,none),(1/4,none),(1/2,none) | if(BOX(s in {0,1/4}),strike,work) | f[BOX(s in {0,1/4}),BOX(QUORUM)]:WWWS` (0.038) |
| CC pool0 c0.5 | +D* family only | length | 0.005 / 0.015 / 0.433 | 0.005 / 0.010 / 0.444 | 0.005 / 0.009 / 0.445 | 0.005 / 0.009 / 0.445 | `(0,strike) | work | work` (0.197) |
| CC pool0 c0.5 | +all, and wage fakers | uniform | 0.418 / 0.199 / 0.260 | 0.455 / 0.158 / 0.294 | 0.463 / 0.147 / 0.301 | 0.464 / 0.145 / 0.301 | `if(BOX(W1=strike),(1/2,none),(0,none)) | if(BOX(s in {0,1/4}),strike,work) | if(BOX(s in {0,1/4}),strike,work)` (0.040) |
| CC pool0 c0.5 | +all, and wage fakers | length | 0.005 / 0.015 / 0.432 | 0.005 / 0.009 / 0.444 | 0.005 / 0.008 / 0.446 | 0.004 / 0.006 / 0.447 | `(0,strike) | work | work` (0.197) |
| RR pool0 c0.5 | constants | uniform | 0.004 / 0.920 / 0.064 | 0.000 / 0.917 / 0.081 | 0.000 / 0.917 / 0.083 | 0.000 / 0.917 / 0.083 | `(1/4,strike) | if(BOX(s in {0,1/4}),strike,work) | strike` (0.028) |
| RR pool0 c0.5 | constants | length | 0.004 / 0.755 / 0.206 | 0.000 / 0.753 / 0.242 | 0.000 / 0.753 / 0.247 | 0.000 / 0.753 / 0.247 | `(1/4,strike) | strike | strike` (0.247) |
| RR pool0 c0.5 | +D0 family (P0) | uniform | 0.011 / 0.975 / 0.012 | 0.001 / 0.992 / 0.007 | 0.000 / 0.994 / 0.006 | 0.000 / 0.994 / 0.006 | `if(BOX(W1(^(0,none))=strike),(1/4,strike),(0,strike)) | f[BOX(s in {0}),BOX(QUORUM)]:WWWS | if(BOX(s in {0}),strike,work)` (0.028) |
| RR pool0 c0.5 | +D0 family (P0) | length | 0.004 / 0.756 / 0.205 | 0.000 / 0.754 / 0.240 | 0.000 / 0.755 / 0.245 | 0.000 / 0.755 / 0.245 | `(1/4,strike) | strike | work` (0.247) |
| RR pool0 c0.5 | +D0 family, D14 | uniform | 0.016 / 0.606 / 0.328 | 0.001 / 0.592 / 0.399 | 0.000 / 0.590 / 0.409 | 0.000 / 0.590 / 0.410 | `if(BOX(W1=strike),(1/2,strike),(0,strike)) | if(BOX(s in {0}),strike,work) | work` (0.032) |
| RR pool0 c0.5 | +D0 family, D14 | length | 0.004 / 0.756 / 0.205 | 0.000 / 0.754 / 0.241 | 0.000 / 0.753 / 0.247 | 0.000 / 0.752 / 0.248 | `(1/4,strike) | strike | work` (0.247) |
| RR pool0 c0.5 | +D0 family, D14, D* family | uniform | 0.002 / 0.746 / 0.231 | 0.000 / 0.653 / 0.343 | 0.000 / 0.636 / 0.364 | 0.000 / 0.634 / 0.366 | `if(BOX(W1=strike),(1/2,strike),(0,strike)) | if(BOX(s in {0,1/4}),strike,work) | if(BOX(s in {0}),strike,work)` (0.035) |
| RR pool0 c0.5 | +D0 family, D14, D* family | length | 0.004 / 0.756 / 0.205 | 0.000 / 0.754 / 0.241 | 0.000 / 0.753 / 0.247 | 0.000 / 0.752 / 0.248 | `(1/4,strike) | strike | work` (0.247) |
| RR pool0 c0.5 | +D* family only | uniform | 0.000 / 0.984 / 0.015 | 0.000 / 0.998 / 0.002 | 0.000 / 0.999 / 0.001 | 0.000 / 1.000 / 0.000 | `f[BOX(W1(^(0,none))=strike),BOX(W1(^(1/4,none))=strike)]:(0,none),(1/4,none),(1/2,none),(1/2,none) | f[BOX(s in {0}),BOX(QUORUM)]:WWWS | if(BOX(s in {0}),strike,work)` (0.006) |
| RR pool0 c0.5 | +D* family only | length | 0.004 / 0.755 / 0.206 | 0.000 / 0.753 / 0.242 | 0.000 / 0.753 / 0.247 | 0.000 / 0.753 / 0.247 | `(1/4,strike) | strike | strike` (0.247) |
| RR pool0 c0.5 | +all, and wage fakers | uniform | 0.013 / 0.742 / 0.226 | 0.002 / 0.641 / 0.353 | 0.000 / 0.620 / 0.379 | 0.000 / 0.618 / 0.382 | `if(BOX(W1=strike),(1/2,strike),(0,strike)) | if(BOX(s in {0}),strike,work) | if(BOX(s in {0}),strike,work)` (0.036) |
| RR pool0 c0.5 | +all, and wage fakers | length | 0.004 / 0.755 / 0.205 | 0.000 / 0.753 / 0.241 | 0.000 / 0.752 / 0.247 | 0.000 / 0.752 / 0.248 | `(1/4,strike) | strike | strike` (0.247) |
| CC pool1 c0.1 | constants | uniform | 0.004 / 0.042 / 0.910 | 0.000 / 0.004 / 0.991 | 0.000 / 0.000 / 0.999 | 0.000 / 0.000 / 1.000 | `(0,strike) | work | f[BOX(s in {0,1/4}),BOX(QUORUM)]:WWWS` (0.313) |
| CC pool1 c0.1 | constants | length | 0.000 / 0.012 / 0.931 | 0.000 / 0.001 / 0.992 | 0.000 / 0.000 / 0.999 | 0.000 / 0.000 / 1.000 | `(0,strike) | work | work` (0.805) |
| CC pool1 c0.1 | +D0 family (P0) | uniform | 0.040 / 0.141 / 0.749 | 0.005 / 0.021 / 0.966 | 0.001 / 0.002 / 0.996 | 0.000 / 0.000 / 1.000 | `(0,strike) | f[BOX(s in {0,1/4}),BOX(QUORUM)]:WWWS | work` (0.387) |
| CC pool1 c0.1 | +D0 family (P0) | length | 0.000 / 0.012 / 0.931 | 0.000 / 0.001 / 0.992 | 0.000 / 0.000 / 0.999 | 0.000 / 0.000 / 1.000 | `(0,strike) | work | work` (0.805) |
| CC pool1 c0.1 | +D0 family, D14 | uniform | 0.075 / 0.104 / 0.741 | 0.011 / 0.015 / 0.964 | 0.001 / 0.002 / 0.996 | 0.000 / 0.000 / 1.000 | `(0,strike) | f[BOX(s in {0,1/4}),BOX(QUORUM)]:WWWS | work` (0.392) |
| CC pool1 c0.1 | +D0 family, D14 | length | 0.000 / 0.012 / 0.931 | 0.000 / 0.001 / 0.992 | 0.000 / 0.000 / 0.999 | 0.000 / 0.000 / 1.000 | `(0,strike) | work | work` (0.805) |
| CC pool1 c0.1 | +D0 family, D14, D* family | uniform | 0.196 / 0.151 / 0.559 | 0.037 / 0.031 / 0.916 | 0.004 / 0.003 / 0.991 | 0.000 / 0.000 / 0.999 | `(0,strike) | f[BOX(s in {0,1/4}),BOX(QUORUM)]:WWWS | work` (0.341) |
| CC pool1 c0.1 | +D0 family, D14, D* family | length | 0.000 / 0.012 / 0.931 | 0.000 / 0.001 / 0.992 | 0.000 / 0.000 / 0.999 | 0.000 / 0.000 / 1.000 | `(0,strike) | work | work` (0.805) |
| CC pool1 c0.1 | +D* family only | uniform | 0.151 / 0.138 / 0.623 | 0.025 / 0.025 / 0.937 | 0.003 / 0.003 / 0.993 | 0.000 / 0.000 / 0.999 | `(0,strike) | work | f[BOX(s in {0,1/4}),BOX(QUORUM)]:WWWS` (0.331) |
| CC pool1 c0.1 | +D* family only | length | 0.000 / 0.012 / 0.931 | 0.000 / 0.001 / 0.992 | 0.000 / 0.000 / 0.999 | 0.000 / 0.000 / 1.000 | `(0,strike) | work | work` (0.805) |
| CC pool1 c0.1 | +all, and wage fakers | uniform | 0.134 / 0.138 / 0.616 | 0.025 / 0.029 / 0.926 | 0.003 / 0.003 / 0.992 | 0.000 / 0.000 / 0.999 | `(0,strike) | work | f[BOX(s in {0,1/4}),BOX(QUORUM)]:WWWS` (0.330) |
| CC pool1 c0.1 | +all, and wage fakers | length | 0.000 / 0.012 / 0.931 | 0.000 / 0.001 / 0.992 | 0.000 / 0.000 / 0.999 | 0.000 / 0.000 / 1.000 | `(0,strike) | work | work` (0.805) |

- **Under a uniform prior the mechanism the spec describes is exactly there:** the zero-wage probe family moves π to
  the smallest positive wage (1/4 at 0.85, the accommodation ratchet, against 0.58 with constants only), the 1/4-probe
  one-atom D14 moves it to fair (0.79), the D\* family to 0.98 (0.97 with D\* alone), and adding the wage fakers
  (C₁, the base and probe fakers) halves it (0.46). RR keeps the smallest positive wage whatever the concessions
  (fair ≤ 2·10⁻⁴); the pool keeps zero wage (≥ 0.99).
- **Under the length prior nothing of it survives** (fair 0.005 → 0.013 at N = 10⁵ with the probe families, 0.004 once
  the fakers are in).

## Lottery (ε = 0)

| cell | status | fair island by 500 | by 10⁴ | by 10⁵ (or stop) | median time to first fair island | fair islands at stop (mean ± 95%) | runs with a fair island at stop | island labels at stop (fair / 1/4 / zero / strike / split) | payoffs (B, W1, W2) |
|---|---|---|---|---|---|---|---|---|---|
| lottery_P01_CC_c0.5 | closed 40 | 0.00 [0.00, 0.09] | 0.00 [0.00, 0.09] | 0.00 [0.00, 0.09] | – | 0.000 ± 0.000 | 0.00 [0.00, 0.09] | 0.000 / 0.000 / 0.725 / 0.000 / 0.275 | 1.725, 0.000, 0.000 |
| lottery_P01_CC_c0.5_xmilitant- | closed 40 | 0.97 [0.87, 1.00] | 0.97 [0.87, 1.00] | 0.97 [0.87, 1.00] | 28 | 0.175 ± 0.119 | 0.17 [0.09, 0.32] | 0.175 / 0.000 / 0.575 / 0.000 / 0.250 | 1.575, 0.087, 0.087 |
| lottery_P01_CC_c0.5_xmilitant | closed 389, censored 11 | 0.99 [0.98, 1.00] | 0.99 [0.98, 1.00] | 0.99 [0.98, 1.00] | 26 | 0.322 ± 0.046 | 0.33 [0.29, 0.38] | 0.323 / 0.019 / 0.535 / 0.000 / 0.122 | 1.545, 0.166, 0.166 |
| lottery_P01_RR_c0.5 | closed 40 | 0.03 [0.00, 0.13] | 0.03 [0.00, 0.13] | 0.03 [0.00, 0.13] | 27 | 0.000 ± 0.000 | 0.00 [0.00, 0.09] | 0.000 / 0.900 / 0.100 / 0.000 / 0.000 | 1.550, 0.225, 0.225 |
| lottery_P01_RR_c0.5_xmilitant | closed 40 | 0.12 [0.05, 0.26] | 0.12 [0.05, 0.26] | 0.12 [0.05, 0.26] | 36 | 0.000 ± 0.000 | 0.00 [0.00, 0.09] | 0.000 / 0.200 / 0.800 / 0.000 / 0.000 | 1.900, 0.050, 0.050 |
| lottery_P0_CC_c0.5_xmilitant | closed 400 | 0.98 [0.97, 0.99] | 0.98 [0.97, 0.99] | 0.98 [0.97, 0.99] | 25 | 0.185 ± 0.038 | 0.18 [0.15, 0.23] | 0.185 / 0.040 / 0.680 / 0.003 / 0.092 | 1.698, 0.102, 0.102 |
| lottery_ref_CC_c0.5 | closed 40 | 0.00 [0.00, 0.09] | 0.00 [0.00, 0.09] | 0.00 [0.00, 0.09] | – | 0.000 ± 0.000 | 0.00 [0.00, 0.09] | 0.000 / 0.000 / 0.825 / 0.025 / 0.150 | 1.800, 0.000, 0.000 |
| lottery_ref_CC_c0.5_xmilitant- | closed 40 | 1.00 [0.91, 1.00] | 1.00 [0.91, 1.00] | 1.00 [0.91, 1.00] | 24 | 0.100 ± 0.094 | 0.10 [0.04, 0.23] | 0.100 / 0.050 / 0.650 / 0.000 / 0.200 | 1.675, 0.062, 0.062 |
| lottery_ref_CC_c0.5_xmilitant | closed 400 | 0.98 [0.97, 0.99] | 0.98 [0.97, 0.99] | 0.98 [0.97, 0.99] | 23 | 0.050 ± 0.021 | 0.05 [0.03, 0.08] | 0.050 / 0.025 / 0.740 / 0.007 / 0.177 | 1.745, 0.031, 0.031 |
| lottery_ref_RR_c0.5 | closed 40 | 0.05 [0.01, 0.17] | 0.05 [0.01, 0.17] | 0.05 [0.01, 0.17] | 82 | 0.000 ± 0.000 | 0.00 [0.00, 0.09] | 0.000 / 0.825 / 0.175 / 0.000 / 0.000 | 1.587, 0.206, 0.206 |
| lottery_ref_RR_c0.5_xmilitant | closed 40 | 0.05 [0.01, 0.17] | 0.05 [0.01, 0.17] | 0.05 [0.01, 0.17] | 40 | 0.000 ± 0.000 | 0.00 [0.00, 0.09] | 0.000 / 0.600 / 0.400 / 0.000 / 0.000 | 1.700, 0.150, 0.150 |
| lottery_sham_CC_c0.5_xmilitant | closed 400 | 0.98 [0.96, 0.99] | 0.98 [0.96, 0.99] | 0.98 [0.96, 0.99] | 24 | 0.055 ± 0.022 | 0.06 [0.04, 0.08] | 0.055 / 0.035 / 0.765 / 0.005 / 0.140 | 1.778, 0.036, 0.036 |

| cell | island wage at stop (0 / 1/4 / 1/2 / no production) | fair islands whose majority boss carries a probe |
|---|---|---|
| lottery_P01_CC_c0.5 | 1.000 / 0.000 / 0.000 / 0.000 | – |
| lottery_P01_CC_c0.5_xmilitant- | 0.825 / 0.000 / 0.175 / 0.000 | 0.268 |
| lottery_P01_CC_c0.5_xmilitant | 0.658 / 0.019 / 0.323 / 0.000 | 0.813 |
| lottery_P01_RR_c0.5 | 0.100 / 0.900 / 0.000 / 0.000 | – |
| lottery_P01_RR_c0.5_xmilitant | 0.800 / 0.200 / 0.000 / 0.000 | – |
| lottery_P0_CC_c0.5_xmilitant | 0.772 / 0.040 / 0.185 / 0.003 | 0.796 |
| lottery_ref_CC_c0.5 | 0.975 / 0.000 / 0.000 / 0.025 | – |
| lottery_ref_CC_c0.5_xmilitant- | 0.850 / 0.050 / 0.100 / 0.000 | 0.000 |
| lottery_ref_CC_c0.5_xmilitant | 0.917 / 0.025 / 0.050 / 0.007 | 0.000 |
| lottery_ref_RR_c0.5 | 0.175 / 0.825 / 0.000 / 0.000 | – |
| lottery_ref_RR_c0.5_xmilitant | 0.400 / 0.600 / 0.000 / 0.000 | – |
| lottery_sham_CC_c0.5_xmilitant | 0.905 / 0.035 / 0.055 / 0.005 | 0.000 |

Island shares over time (mean over runs and islands): militant T1 / probe-carrying boss / concession boss (pays 1/2 to the militant pair, 0 to the scab pair) / constant striker.

| cell | g = 0 | g = 10 | g = 25 | g = 50 | g = 100 | g = 200 | g = 500 | g = 1000 |
|---|---|---|---|---|---|---|---|---|
| lottery_P01_CC_c0.5 | 0.001 / 0.048 / 0.007 / 0.48 | 0.002 / 0.046 / 0.011 / 0.23 | 0.001 / 0.045 / 0.014 / 0.15 | 0.002 / 0.052 / 0.015 / 0.14 | 0.002 / 0.050 / 0.012 / 0.13 | 0.002 / 0.051 / 0.009 / 0.13 | 0.002 / 0.050 / 0.009 / 0.13 | 0.002 / 0.049 / 0.006 / 0.11 |
| lottery_P01_CC_c0.5_xmilitant- | 0.001 / 0.050 / 0.007 / 0.00 | 0.000 / 0.046 / 0.015 / 0.00 | 0.000 / 0.047 / 0.019 / 0.00 | 0.000 / 0.049 / 0.024 / 0.00 | 0.001 / 0.054 / 0.025 / 0.00 | 0.001 / 0.049 / 0.022 / 0.00 | 0.001 / 0.042 / 0.021 / 0.00 | 0.000 / 0.039 / 0.020 / 0.00 |
| lottery_P01_CC_c0.5_xmilitant | 0.481 / 0.049 / 0.007 / 0.00 | 0.362 / 0.073 / 0.026 / 0.00 | 0.312 / 0.102 / 0.049 / 0.00 | 0.304 / 0.111 / 0.061 / 0.00 | 0.302 / 0.121 / 0.071 / 0.00 | 0.306 / 0.134 / 0.085 / 0.00 | 0.312 / 0.161 / 0.117 / 0.00 | 0.343 / 0.199 / 0.159 / 0.00 |
| lottery_P01_RR_c0.5 | 0.001 / 0.018 / 0.005 / 0.48 | 0.001 / 0.016 / 0.004 / 0.49 | 0.001 / 0.017 / 0.003 / 0.49 | 0.001 / 0.017 / 0.001 / 0.48 | 0.001 / 0.016 / 0.000 / 0.46 | 0.002 / 0.016 / 0.000 / 0.47 | 0.001 / 0.020 / 0.000 / 0.47 | 0.001 / 0.017 / 0.000 / 0.47 |
| lottery_P01_RR_c0.5_xmilitant | 0.484 / 0.018 / 0.005 / 0.00 | 0.479 / 0.022 / 0.005 / 0.00 | 0.478 / 0.017 / 0.003 / 0.00 | 0.480 / 0.013 / 0.004 / 0.00 | 0.471 / 0.012 / 0.003 / 0.00 | 0.473 / 0.008 / 0.000 / 0.00 | 0.476 / 0.001 / 0.000 / 0.00 | 0.495 / 0.000 / 0.000 / 0.00 |
| lottery_P0_CC_c0.5_xmilitant | 0.481 / 0.041 / 0.007 / 0.00 | 0.358 / 0.060 / 0.020 / 0.00 | 0.306 / 0.082 / 0.039 / 0.00 | 0.290 / 0.086 / 0.049 / 0.00 | 0.285 / 0.091 / 0.056 / 0.00 | 0.284 / 0.099 / 0.063 / 0.00 | 0.283 / 0.104 / 0.075 / 0.00 | 0.294 / 0.115 / 0.088 / 0.00 |
| lottery_ref_CC_c0.5 | 0.001 / 0.000 / 0.001 / 0.48 | 0.001 / 0.000 / 0.001 / 0.24 | 0.000 / 0.000 / 0.000 / 0.16 | 0.000 / 0.000 / 0.000 / 0.15 | 0.001 / 0.000 / 0.000 / 0.14 | 0.001 / 0.000 / 0.000 / 0.14 | 0.000 / 0.000 / 0.000 / 0.13 | 0.000 / 0.000 / 0.000 / 0.12 |
| lottery_ref_CC_c0.5_xmilitant- | 0.001 / 0.000 / 0.001 / 0.00 | 0.001 / 0.000 / 0.001 / 0.00 | 0.001 / 0.000 / 0.001 / 0.00 | 0.000 / 0.000 / 0.001 / 0.00 | 0.000 / 0.000 / 0.002 / 0.00 | 0.000 / 0.000 / 0.004 / 0.00 | 0.000 / 0.000 / 0.004 / 0.00 | 0.000 / 0.000 / 0.005 / 0.00 |
| lottery_ref_CC_c0.5_xmilitant | 0.481 / 0.000 / 0.001 / 0.00 | 0.356 / 0.000 / 0.002 / 0.00 | 0.299 / 0.000 / 0.003 / 0.00 | 0.279 / 0.000 / 0.003 / 0.00 | 0.277 / 0.000 / 0.003 / 0.00 | 0.273 / 0.000 / 0.004 / 0.00 | 0.265 / 0.000 / 0.005 / 0.00 | 0.253 / 0.000 / 0.006 / 0.00 |
| lottery_ref_RR_c0.5 | 0.001 / 0.000 / 0.001 / 0.48 | 0.001 / 0.000 / 0.001 / 0.49 | 0.001 / 0.000 / 0.001 / 0.48 | 0.001 / 0.000 / 0.000 / 0.48 | 0.002 / 0.000 / 0.000 / 0.48 | 0.002 / 0.000 / 0.000 / 0.47 | 0.002 / 0.000 / 0.000 / 0.48 | 0.001 / 0.000 / 0.000 / 0.48 |
| lottery_ref_RR_c0.5_xmilitant | 0.486 / 0.000 / 0.001 / 0.00 | 0.488 / 0.000 / 0.000 / 0.00 | 0.486 / 0.000 / 0.000 / 0.00 | 0.488 / 0.000 / 0.000 / 0.00 | 0.484 / 0.000 / 0.000 / 0.00 | 0.480 / 0.000 / 0.000 / 0.00 | 0.457 / 0.000 / 0.000 / 0.00 | 0.459 / 0.000 / 0.000 / 0.00 |
| lottery_sham_CC_c0.5_xmilitant | 0.482 / 0.000 / 0.001 / 0.00 | 0.356 / 0.000 / 0.002 / 0.00 | 0.300 / 0.000 / 0.004 / 0.00 | 0.278 / 0.000 / 0.004 / 0.00 | 0.273 / 0.000 / 0.004 / 0.00 | 0.269 / 0.000 / 0.004 / 0.00 | 0.261 / 0.000 / 0.005 / 0.00 | 0.250 / 0.000 / 0.006 / 0.00 |

- **As preregistered (seeds from the length prior): no fair island, ever,** in P₀₁ or the reference under CC (0/40
  each); under RR 1/40 and 2/40 transient fair islands, none persisting; islands sit at zero wage (CC) or 1/4 (RR,
  0.90 of islands in P₀₁).
- **With militants in numbers (not preregistered): fair islands appear within ~25 generations in every arm
  (0.98–0.99 of runs by generation 500), and the probes decide persistence:** fair islands at the stop 0.322 ± 0.046
  (P₀₁), 0.185 ± 0.038 (P₀), 0.055 ± 0.022 (sham), 0.050 ± 0.021 (reference), 400 runs each; 0.81 of P₀₁'s and 0.80 of
  P₀'s surviving fair islands have a probe-carrying boss as the majority boss, and concession bosses grow from 0.007
  of the boss slot at seeding to 0.16 by generation 1,000. With militant⁻ in numbers (40 runs) the effect is smaller
  (0.175 vs 0.100): militant⁻ works at world 0 of a quoted encounter, so only level-1 probes certify it.
- With militants in numbers and RR, no fair island persists; probes lower the wage (P₀₁: 0.80 of islands at zero wage
  against 0.40 in the reference).

## Verdicts

Scored by the rules in the predictions file; "inconclusive" where the explored and the cut-corrected numbers fall on
opposite sides of a threshold and the θ = 10⁻¹⁰ re-exploration did not finish.

| # | prediction | outcome |
|---|---|---|
| RE 1 | P₀ π at the smallest positive wage (1/4 ≥ 0.5, fair ≤ 0.1 at 10⁴); P₀₁: T₀ deleterious against D\*, the only neutral exit the boss shadow | **failed, falsifier fired** (static: D\*'s unread slot takes the scab neutrally, mass 0.499); P₀ 1/4 occupancy 0.012 (fair 0.004); T₀ deleterious against D\* in the read slot **held**; the ratchet itself is real statically and in the uniform-prior reduced chain (1/4 0.85) |
| RE 2 | P₀₁ fair ≥ 0.3 at 10⁴ with positive slope; reference ≤ 0.005, sham ≤ 0.05 | **failed, falsifier fired** (P₀₁ 0.0086 explored, 0.0020 cut-corrected, ≤ 0.1; sham within 0.006 of P₀₁); reference 0.0025 and sham 0.0025 clauses held; slope +0.12 explored, −0.31 corrected |
| RE 3 | union mass in P₀₁'s fair support ≤ 0.1 | **held** (2·10⁻⁴) |
| RE 4 | RR: 1/4 ≥ 0.5, fair ≤ 0.1; pool fair ≤ 0.05 | **held** (RR 1/4 0.76, fair 2·10⁻⁵; pool fair ≤ 1.4·10⁻⁴ at c = 0.1 and 0.5) |
| RE 5 | lottery: P₀₁ fair island by 500 in ≥ 0.6 of runs (reference ≤ 0.1); ≥ 0.5 islands fair at the horizon | **failed, falsifier fired** (0/40 by 10⁴; persistence 0); with militants in numbers (not preregistered) 0.99 by 500 but the reference too (0.98), persistence 0.32 |
| RE 6 | D\*'s fakers ≤ 10⁻³ and change nothing by > 0.05; every neutral substitute of P₀₁'s fair state a militant twin; P₀'s fair state has T₀ as a demand-lowering substitute | **failed, falsifier fired** (demand-lowering neutral substitutes for ≥ 0.96 of P₀₁'s fair π; strict wage-faker mass at F\* 0.0095 in the chain language, 0.0116 with the null two-atom policies); "changes nothing by > 0.05" **held** (+0.002); the P₀ clause **held** |
| RS | bosses adopt concessions; unions get higher wages quickly | **failed as scored** (probe-concession bosses 0.006 of π at 10⁴; no fair island in the preregistered lottery); holds conditionally with militants in numbers (not preregistered): fair islands in ~25 generations in every arm, 0.8 of the surviving ones held by probe-carrying bosses, persistence 0.32 vs 0.05 |
| S1 | P₀₁ fair ≤ 0.02 at 10³, 10⁴ | **held** (0.0040, 0.0086) |
| S2 | P₀₁ − ref ≤ 0.01 on fair at 10⁴; sham = ref to 0.005 | **held** (0.006 explored, −0.0003 corrected; ≤ 0.002) |
| S3 | P₀ 1/4 ≤ 0.05, zero ≥ 0.4 at 10⁴ | **held** (0.012, 0.48) |
| S4 | fair escape falls by 2–15× from 10³ to 10⁴ in P₀₁ | **inconclusive** (explored ×21; cut-corrected ×4.9; the θ = 10⁻¹⁰ check unfinished) |
| S5 | probe bosses ≤ 0.3 of fair mass at 10⁴; F\*⁻-type ≤ 0.1 | **inconclusive** (explored 0.65 would fire the falsifier, but it is the cut artefact: the dropped exits leave exactly the probe-concession fair states, and the corrected fair mass is 4× lower); F\*⁻ clause held (0.07 explored) |
| S6 | union ≤ 0.01 of fair | **held** |
| S7 | RR 1/4 ≥ 0.6, fair ≤ 0.02, within 0.05 of reference | **held** (0.759 vs 0.750) |
| S8 | pool: zero ≥ 0.9 at c = 0.1, ≥ 0.6 at c = 0.5 | **held** (0.999, 0.995) |
| S9 | lottery establishment ≤ 0.2 by 500, ≤ 0.3 by 10⁴ (P₀₁ and ref) | **held** (0, 0) |
| S10 | lottery persistence ≤ 0.05 | **held** (0) |
| S11 | P₀₁ RR ≥ 0.6 of islands at 1/4 | **held** (0.90) |
| S12 | ≥ 0.9 of fair π with a demand-lowering neutral substitute, ≥ 0.5 with a strict boss after it | **held** (0.998, 0.995) |
| S13 | fair log-odds slope ≤ 0 over 10²–3·10⁴ | **inconclusive** (explored +0.12, cut-corrected −0.31; held on the corrected numbers) |

**Three-role distribution threshold** (reported, not a verdict): ≤ 0.012 of eligible π in every CC cell (the guess was
≤ 0.02), ≤ 2·10⁻⁴ in RR (guess ≤ 0.01): only s = 1/2 with both working reaches a 1/6 minimum share.
