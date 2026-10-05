# Club arm: debugging runs (not scored)

Kept apart from the scored runs (`runs/club.md`, `runs/club*.json`), as the spec requires.

1. **Base-language reproduction** (scratch `dbg1.py`). `club.Club(n, club=False)` against `modal.ModalLanguage` /
   `modal.evaluate` at n = 6 and 8: identical source strings, identical prior (max |Δμ| = 0), identical play table.
   The `CLUB` evaluator costs 0.03 s for one P_K at n = 8 (708 canons).
2. **Validation of the log-domain tools** (scratch). `club_chain.gth_log` (GTH elimination with logaddexp) against a
   dense linear solve on a random 30-state chain with rates spread over e^(±9): max relative error 6·10⁻¹⁵, balance
   residual 3·10⁻¹⁵. The closed-form `log_rho_fast` (quadratic exponent, windowed log-sum-exp) against
   `ergodic_islands.log_fixation` on 900 random payoff quadruples at N = 10², 10³, 10⁴: max relative error 1.1·10⁻¹².
3. **Chain smoke test** (`python3 src/club_chain.py --smoke`; club and clique at n = 6, N = 10²). Ran clean. Linear chain
   and log-domain GTH chain agree on π(K) to 2·10⁻⁸ (0.998702 both). Output discarded.
4. **Monotonicity counterexample hunt** (scratch). At n = 8, 200 random nested pairs; every violation is a guarded
   program `and(CLUB(THEM),BOXD(THEM(^D)))` (or its `^C` / `BOXD1` variants) that self-cooperates when D (or ALLC) is
   outside K and defects on itself when D is inside K. This led to `src/club_maximal.py` (scored).
