## Summary and verdicts

The ε→0 chain at n = 6 is a rotating-pair chain in every arm. Pairs hold 0.98–0.99 of π, unfair pairs hold about 0.6, the grand coalition holds 0.003 among constants and 0.010–0.017 with conditional programs, and disagreement is 10⁻⁴ or less. The shares are N-independent from N = 10³ on. Provability changes nothing measurable: modalPA equals the weak arm to three decimals at N = 10² and 10³.

The mechanism is the same in every arm:
- The excluded slot drifts neutrally (rate ∝ 1/N) to an offer that pays a member more.
- That member, the pivot, takes the offer by a strict move.
- Pivots only ever move up: 1/3 → 1/2, 1/2 → 2/3, 1/3 → 2/3, and neutral 1/2 → 1/2.
- No program in a pair can stop its partner's own slot from defecting, so reading source cannot plug this exit.

There is a nonzero net current around the outcome types, fair → unfair → wasteful → fair. It is equal on each edge and ∝ 1/N: 1.9·10⁻⁵, 3.6·10⁻⁶ and 3.9·10⁻⁷ per mutation event at N = 10², 10³, 10⁴. The net circulation among the three labelled pair states is exactly 0, as relabeling symmetry requires.

The grand coalition behaves differently in the two kinds of language:
- *Constants only:* it is drift-closed, since every exit costs a member 1/3.
- *n = 6:* it is not. One-atom conditionals give it 54 bridges (108 with PA + Con), for example `if(BOX(2=(1,1/2)),(2,1/3),(ALL,1/3))`, which plays (ALL, 1/3) on path and accepts slot 2's pair offer. Their bridge mass is 3.3·10⁻⁴ per mutation event, against 0.149 for a constant pair. Readers of the form "join the grand coalition iff slot j does" open neutral-plus-strict entries. So conditionals raise the grand coalition's share 3–6×, with entry and exit both ∝ 1/N.

Status of the cells:
- **modal arm (PA + Con), full chain: not finished.** It was projected beyond 2 hours under machine load (load average up to ~260, swap full). In its place:
  - the matched modalPA arm (PA box only, the weak arm's grammar) at every N;
  - one-ring runs of modal and modalPA at N = 100, which agree within 0.01;
  - static comparisons: the named and handshake triples have identical bridge masses and exit rates in modal and modalPA.
- **Also stopped:** modalPA at N = 10⁴ (still in round 1 after 1 h 54 min) and a three-round modal N = 100 rerun (still in round 1 after 1 h 04 min). For N = 10⁴ only constants and weak are available.

| # | prediction | verdict | numbers |
|---|---|---|---|
| 1 | no efficient monomorphic triple drift-closed at n = 6 | **held** at n = 6 (language-relative) | 0 of 150 efficient states with π ≥ 10⁻⁶ closed at depth 2, in every weak/modalPA cell. Constant grand: 54 (weak, modalPA) / 108 (modal) bridges, mass 3.3·10⁻⁴; constant pairs: mass 0.149. At n = 1 (constants) the grand coalition **is** drift-closed (no strict or neutral exit), so sol's "language-dependent trapped networks" exists one language down. |
| 2 | pairs ≥ 0.6 and grand ≤ 0.2 at N = 100 (modal), nonzero net current around the three pair states | **mass clause held; current clause failed as stated** | modalPA N = 100: pairs 0.990, grand 0.0099. The net circulation around the labelled pair states is 0 (1e−20), as forced by symmetry. The nonzero current is around outcome types (fair → unfair → wasteful → fair), driven by the excluded slot bidding for a pivot. |
| 3 | unfair pairs in [0.1, 0.4] and below fair | **failed** (falsifier met) | unfair 0.59–0.63 against fair 0.36–0.38 in every arm and N. That is the 2:1 orientation multiplicity, and pivots ratchet up to 2/3. |
| 4 | E[max share] ∈ [0.45, 0.60], exclusion ≥ 0.6 | **held in modalPA (N = 10², 10³), at the upper edge; falsifier (> 0.62) not met anywhere** | E[max]: modalPA 0.5964 / 0.5998; weak 0.5964 / 0.5998 / 0.6005 (above 0.60 by 5·10⁻⁴ at N = 10⁴); constants 0.5987 / 0.6035 / 0.6043. P(some slot gets 0) 0.983–0.998; P(pair) 0.983–0.997. The interval holds only because the 2:1 unfair/fair split sits at E[max] ≈ 0.6 by arithmetic. |
| 5 | grand coalition < 0.2 at every N, exits neutral ∝ 1/N into accept-pair programs then strict pair formation, entry needs three neutral steps | **share held; mechanism half held** | grand 0.0099 / 0.0161 / not finished (modalPA) and 0.010 / 0.016 / 0.017 (weak). Exits: the constant grand coalition's only non-deleterious exits are the bridges, at rate 2.67·10⁻³/N; the next step is pair formation, strict (offer 1/2) or neutral (offer 1/3). Entry: not three neutral steps. It goes through a conditional "join iff slot j joins" reader and a strict last step, at a rate of 6.5–9.4·10⁻⁵ per event spent in disagreement, flat in N. |
| 6 | weak arm disagreement ≥ 2× modal at each N | **failed** | disagreement 4·10⁻⁴ / 1·10⁻⁴ / < 10⁻⁴ in both weak and modalPA, identical. Weak-arm handshakes diverge, but they carry no mass. |
| 7 | finite ε: pair-to-pair turnover, mean pair dwell 10²–10⁴ generations; grand start decays into pairs within 10⁴ generations in all 3 seeds | **turnover clause held; decay clause failed** | mean interior pair dwell 1.1–1.7·10³ generations (median 480–1,250); pair-to-pair switches 5–37 per run. Grand start: P(pair) first exceeds 0.5 at 26,440 and 67,100 generations, and never by 10⁵ in one seed, in both arms. |
| 8 | constants: fair pairs ≥ 0.5, grand < 0.1 | **failed** (fair clause); grand clause held | fair 0.376 / 0.371 / 0.368, unfair 0.596 / 0.624 / 0.629, grand 0.0025 / 0.0029 / 0.0029. Entry into and exit from the grand coalition both cost 1/3, so its share is N-independent, not a matter of path length. |

### Method notes

- **Solver.** At N ≥ 10³ the rates span e⁻¹⁰⁰⁰ and beyond, and sparse LU on the generator fails: on the 729-state
  constants chain at N = 10³ it puts all mass on the grand coalition, against 0.003 from GTH. Row-scaled linear GTH is
  exact through N = 10³. At N = 10⁴ only log-space GTH is right, because a rate negligible within its row can be the
  only bridge between closed classes. The non-constant cells use a "hybrid": the core (the 729 constant triples plus
  promoted states) is solved by dense GTH (log-space at N = 10⁴), and the ring of explored non-core states is
  eliminated exactly as a stochastic complement, by sparse LU on its jump chain.
- **Exploration.** New ring states are those with π-weighted inflow above θ, with θN = 10⁻⁷ throughout.
  - The outcome-changing cut (outcome-changing transitions that leave the explored set, relative to all
    outcome-changing transitions) is 0.3–1.1% in the final cells.
  - Relabeling invariance of π holds to 10⁻¹³ (top 2,000 states, all 6 permutations).
  - The grand coalition's share is sensitive to exploration depth, because the reader states that open entries into
    it have small inflow. At N = 10³, θN = 10⁻⁶ gives 0.0016 and θN = 10⁻⁷ gives 0.0161. The hybrid without
    ring-to-ring edges (`*_ringonly`) gives 0.003 at N = 100, against 0.010 with them. The ring-only method breaks down
    at N = 10⁴ and was discarded.
  - The pair shares move by ≤ 0.01 across all of these checks.
- **Handshakes** (two or three conditional slots) have zero mass in the explored sets. Their inflow is below θ, and the
  hand-built handshakes leak at least as fast as their constant counterparts (handshake table below). So leaving them
  out does not bias the outcome shares.
- **Machine load.** Load average reached ~260 and swap filled, from other jobs, so cells ran 5–10× slower than on an
  idle machine. That is why the modal (PA + Con) chain and modalPA at N = 10⁴ did not finish.
