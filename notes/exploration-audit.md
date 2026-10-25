# Exploration-cap audit of the published ε → 0 chains (notes, 2026-10-24)

Spec `specs/2026-10-24-exploration-audit.md` (reviewed by gpt-6.1-sol, then gemini-4-argon in amended mode; both folded).
§1 is the inventory and triage, committed before any re-solve and before any prediction is scored. §2 (deviations and
facts found while running) is appended after the audited cells began.

*Provenance of §1.* Compiled by reading the RESULTS section text, the producing `src/` module and its stored `runs/`
records. Six read-only helper passes split RESULTS.md by line range (1–1242, 1243–2087, 2088–3113, 3114–3625,
3626–4572, 4573–end); I spot-checked the cap facts that drive the triage against the stored records (modal fixed-role
dollar: `runs/modal_dollar/fixed_modal_n7_N{100,1000}_th1e-12.json` n_states = 8000, cut 9.8e-4 and 5.2e-3, K = 205;
mixed2 cap contrast; dollar3 `rel_cut`). Anything marked "unknown" or "not stored" was not stored. Class counts K are
behavioural (payoff-row) classes as each producing module built them; ∏_r K_r is the number of monomorphic states of
the model's own state space (K for one population).

## 1. Inventory

### 1.0 Status codes

* **C** complete: every monomorphic state expanded and no polymorphic states in the model, or every reachable state
  expanded. Excluded from re-solving (the closure is over all permitted transitions).
* **M** monomorphic-complete, polymorphic states θ-pruned or seeded (the chain expands every monomorphic class as a seed;
  only polymorphic targets are expanded by inflow above θ, or by seeds). Eligible; stage (c) is trivial, stage (d) is the
  question.
* **R** monomorphic-restricted: a θ threshold, `max_states` cap or seed list leaves part of the monomorphic space
  unexpanded. Eligible; stages (b) and (c) are the question.
* **N** not a chain / not reproducible (listed so the inventory is exhaustive).

"Restricted exploration" in the spec's sense (θ threshold on inflow, log-θ, `max_states`/`max_rounds`, top-k invaders, a
capped closure) covers M and R. No chain in the inventory uses a top-k invader restriction: every mutant class is
enumerated at every expanded state (checked in `chain.Chain.expand`, `TwoPop`, `Chain3`, `LogChain`, `TwoPopChain`).

### 1.1 Table

Solvers: `Chain` = `src/chain.py` lumped-resident chain (θ 1e-6, max_states 30,000, max_rounds 60, p_eager 0.3 unless
stated; `eager_poly=False` where stated); `LogChain` = `src/chain_log.py`; `Chain3`/`UChain`/`GChain` = `src/dollar3_chain.py`,
`src/union_chain.py`, `src/gene_arm.py` hybrid explorers; `TwoPopChain` = `src/mixed2.py`. "Cut" is the stored unexplored
flux (`cut_flow`, `rel_cut`, `log10_cut`, as that module defines it). All models are lumped-resident unless "twins".

| id | RESULTS section (headline chain numbers) | solver; exploration | cap / cut stored | K; ∏K_r | status | claim size / twin risk |
|---|---|---|---|---|---|---|
| I-01 | Exponential fitness map sweep, lim_N weak N = 1000, prior diagnostic, BoS tie-break, Moran-check chain half (PD all-D 0.977–0.999, `THEM(^C)` 0.006–0.018, Stag basin flip, n ≤ 6 games) | `Chain` via `run.run_cell`, square mode, seeds = all classes, defaults | cut ≤ 4.5e-5; poly_flow ≤ 6e-2 at N = 10; 62–92 indeterminate in exchange | K 21–220; ∏ = K | M | headline (B fails well-mixed); low |
| I-02 | Original clamped sweep (void cells, "The chain", PD, Stag, test games, source arm) | same, clamped fitness | cut ≤ 4.7e-5; indeterminate ≤ 183 | as I-01 | N | superseded, void, **not reproducible** (`fixation()` is exp-only, `run.py` hard-codes `fmap='exp'`) |
| I-03 | n = 7 robustness cells in PD (strong and weak, 12 cells each) | `Chain` sparse mode: seeds = programs of size ≤ 4 (91 weak / 86 strong), lazy beyond | cut ≤ 2.6e-5; n_expanded 89–251, below the probe-class count in six weak cells | probe "K" 44/45 and 105/106; true L_7 K not stored | **R** | robustness only; medium-low |
| I-04 | Ultimatum arm (a), ROLE one population (all-M 0.372, all-L 0.349) | `Chain` via `run_ult.role_arm`; all classes | cut 1.4e-5; poly 5e-4 | K = 81 | M | low |
| I-05 | Ultimatum fixed-role arms (b) mutual, (c) one-sided ((L\|L) 0.387 / 0.391, (M\|M) 0.191 / 0.193) | `TwoPop` (`src/twopop.py`): seeds = top-12 × top-12 by prior, then θ-lazy (θ 1e-6, max_states 20,000) | 152 and 144 pair states expanded; cut 2.6e-5 and 7.0e-6 | 44×44 = 1,936; 24×18 = 432 | **R** | secondary headline (falsifies the (M,M) prediction); low–medium |
| I-06 | Ultimatum with outside option ((M\|M) 0.234) | `TwoPop`, as I-05 | 160 states; cut 2.9e-5 | 44×45 = 1,980 | **R** | secondary |
| I-07 | lim_N of the chain with `ROLE` (weak L_6 + ROLE, 18 cells, N 100–30,000, w ∈ {0.1, 0.3, 1}; cooperation peak 0.013–0.014 then N^(−1/2)) | `limN.main` → `run_cell`, square, all 112 classes | cut 8e-9–4.3e-7; poly ≤ 4.3e-7; 112–113 expanded | K = 112 | M | **headline** (THEORY §9.2); the N = 10⁴, w = 0.3 cell was re-solved in the Solver audit (0.0073 unchanged) |
| I-08 | Modal (Löbian) arm lim_N in the PD (n = 6, 8, 9, N ≤ 3·10⁴; P(C,C) 0.73 at 3·10⁴; entry/exit slopes) | `Chain` via `modal_limN.cell`, `eager_poly=True`, θ 1e-6 | cut ≤ 1.8e-6; poly ≤ 1.9e-6 (text says 3e-7); n_expanded not stored; the n = 8 N ≥ 3000 cells ran 7,606–15,217 s (cap not excluded) | K = 51 / 471 / 863 | M | **headline**; n = 9 at 10⁴, 3·10⁴ re-solved in the audit; free-arm P* deep-modulo-twins states found there |
| I-09 | E1 matched control (W0 0.009–0.027, M0 0.13–0.70) | `Chain`, `eager_poly=False`, all classes | cut ≤ 2.1e-7 | W0 12/19, M0 8/10 | M | headline-supporting; low |
| I-10 | E2 ratchet (n = 8, N = 10⁵, 3·10⁵: 0.8135, 0.8733) | `Chain` via `modal_limN.cell`, `eager_poly=False` | cut 1.5e-8, 8.4e-9 | 471 | M | low |
| I-11 | Priced arm Exp 1 (atoms/depth/lazy; n = 6, 8; c ∈ {10⁻³, 10⁻², 10⁻¹}; lazy n = 8 → 0.9985) | `Chain` via `priced_limN.cell`, `eager_poly=False` | cut ≤ 2.7e-5; poly ≤ 7.6e-2 (pre-fix c = 10⁻³) / 1.9e-2; **11 indeterminate transitions dropped silently** in depth n = 8 c = 10⁻² N = 100 | 52/66 (n = 6); 586/583/610 (n = 8) | M | headline; audit re-solved only c = 10⁻², N = 10⁴ |
| I-12 | Priced arm Exp 3, cliques (π(cliques) = 1 in 12 cells) | `Chain` | cut ≤ 1.7e-15 | n = 8 priced + 1 or 4 clique classes | M | absorbing by construction; low |
| I-13 | Addendum, chain polish fix (24 c = 10⁻³ cells) | `Chain` (a49a007) | cut ≤ 2.6e-6; poly ≤ 1.2e-2 | as I-11 | M | low–medium (about 1% polymorphic mass) |
| I-14 | Certificates-only arm (n = 10, 11; tag 1.000, lfp, gfp, lob; N ≤ 3·10⁴) | `Chain` + `floor_transitions` (transitions < 10⁻¹³ floored); `eager_poly=False` | cut ≤ 5.5e-7; n_terminal 2–5 (tag cells are an absorption lottery, not π) | n = 10: 25–82; n = 11: 35–158 | M | medium; the tag result is a lottery |
| I-15 | Price scaling paths (c_N = c₀N^(−α); slopes; free arm 0.814/0.883) | `Chain` via `priced_limN.cell`, `eager_poly=False` | cut ≤ 2.5e-6 | 52 / 586 | M | low |
| I-16 | Certificate pricing (decidability-based free set; n = 6, 8; N ≤ 10⁵) | `Chain` via `cert_limN.cell`; θ 1e-6 (1e-7 repeats) | cut ≤ 4.7e-6; n_states = n_classes + 0–3 (no polymorphic state expanded); lock-in cells have exits below double precision | 51–66 (n = 6); 471–610 (n = 8) | M | medium; lock-in claims sit on P\*/PrudentBot deep monomorphic states |
| I-17 | Rival networks under lazy pricing on graphs: R2 partially lumped chain (self-cooperating 0.661 / 0.821 / 0.956); `wmchain` reference | R2: `rival_static.partial_pi` GTH over **16 resident states** with Monte Carlo rates, all other mutants routed to a label's primary representative; `wmchain`: `Chain` | wmchain cut ≤ 5.9e-7; R2 has no flux concept | 610 (lazy n = 8); R2 uses 16 | **R** (by design) | medium–high claim (prior mass picks the network on graphs); not a cap; needs new MC rates to extend |
| I-18 | Ergodic islands part A (two-level ε → 0 chain; weak 0.125/0.069/0.024; modal odds ∝ I) | `ergodic_islands.chain_row`: dense K×K rate matrix with rare-migration Φ, GTH; no exploration | none; polymorphic states not modelled (734 coexistence pairs in the weak arm) | 112 (weak), 51 (modal) | C (model choice) | medium |
| I-19 | Universality against drift-closure (102 cells; n = 6, 8, 9; N 10²–10⁶; slopes 0.43–0.50, exits −1 to −22) | `Chain` via `moat_limN.cell`, θ 1e-6, `eager_poly=False` | cut ≤ 2.7e-5 (five cells > 1e-5); indeterminate ≤ 140; top-state `kept_exit_share` ≈ 0 in μ-fringe n = 8, 9 | 51 / 471 / 863 | M | medium; exit-slope claims rest on dropped one-copy-twin exits |
| I-20 | The closed club (club / clique / free; n = 6, 8; N ≤ 10⁵) | `Chain` + log-GTH over the complete K×K matrix | cut ≤ 1.9e-9 (free 1.0–1.3e-6); n_states = K | 66 / 581; 51 / 471; 53 / 485 | M (mono complete; GTH over all K agrees to 10⁻⁸) | low |
| I-21 | Bounded provers (136 cells; n = 8, N = 10⁵: P(C,C) 0.847–0.8135) | `Chain` via `bounded_chain.cell`, `eager_poly=False` | cut ≤ 1.3e-6; n_states = K | 148–1,838 (n = 8) | M | low–medium |
| I-22 | Three-player majority divide-the-dollar (constants / weak / modalPA; N 10²–10⁴; grand 0.003/0.016, pairs 0.99, unfair 0.6) | `Chain3.explore_hybrid`: seeds 729 constant triples; θ = 10⁻⁷/N; promote 1e-5; core_max 2500; max_states 400k; 4–5 rounds | rel_cut 0.16–0.43%; outcome-changing 0.31–1.08%; core_max reached at N = 10³; modalPA N = 100 stopped with 276 candidates unadded; **grand-coalition share moves 10× with θ** (0.0016 at θN = 10⁻⁶ vs 0.0161 at 10⁻⁷) | per slot 903 / 1,179 / 2,475; ∏ = 7.4e8 / 1.6e9 / 1.5e10 | **R** (~4·10⁴ states explored) | **high**: restricted, θ-sensitive, prior audit incomplete |
| I-23 | The union game (27 full cells; fair 0.004 → 0.001, zero wage 0.46–0.64) | `UChain.explore_hybrid`: θ = 10⁻⁹ at every N (not N-scaled), seeds named programs | outcome-changing cut 0.12–0.19% (N = 10²), 0.33–0.49% (10³), 1.1–1.4% (10⁴), total ≤ 1.8%; 4.4–13.4k states | 297 × 364² = 3.9e7 (noquorum 2.9e7, blind 1.3e7) | **R** | medium–high; audit re-solved only QUORUM c = 0.5, N = 10³ |
| I-24 | Incentive-compatible enforcement: Part B (192 reduced cells), Part C (CC / RC / CR / RR; RR intermediate 0.75, RC fair 0.005) | Part B `dense_chain` exact over 81 states; Part C `UChain.explore_hybrid`, θ 1e-9 (CC) / 1e-11 (CR, RC, RR) | Part C outcome cut 3.5e-6–5e-3; RC+pool at θ 10⁻⁹: 610 states, cut 5.2% vs 4,320 states at 10⁻¹¹ | (boss/worker): CC 297/364, CR 87/260, RC 27/122, RR 13/62; ∏ = 3.9e7 / 5.9e6 / 4.0e5 / 5.0e4 | Part B C; Part C **R** | high (headline for enforcement); RR and RC small enough for a much larger solve |
| I-25 | Proof length: K arm and priced budgets (n = 6, N 10³–3·10⁴; K b = 4: 0.404/0.682/0.788) | `Chain`, `eager_poly=False` | cut ≤ 1.4e-7 (3.2e-6 control b = 2) | free 51; K 5–48; control 66 | M | low; K play tables not stored (regenerate) |
| I-26 | Divide-the-dollar partitions (fixed-role exact; one-population `Chain` θ 1e-7; N scans) | fixed: `fixed_chain` exact dense over K×K; one-pop `Chain` with `ClassProvider`, θ 1e-7 | cut 8.7e-19–1.5e-6 — **not a certificate** (dollar5 role N = 10⁴ cut 6e-10 hid a state with all of π); N = 10²,  3·10³ and scans not audited | dollar5 78 / 140; dollar3 45 / 80; fixed ∏ = 6,084 / 2,025 | fixed C; one-pop M | high, but N = 10³, 10⁴, 3·10⁴ already re-solved in the Solver audit |
| I-27 | K at n = 8 lim_N PD chain (K b = 4: .414/.679/.774; b8, b16, b54; free .371/.617/.725; controls) | `Chain` via `k_at_n8.chain_cell`, `eager_poly=False`; w = 0.3 | 24 rows: n_states == n_classes (no polymorphic state expanded), cut ≤ 2.1e-7 | free 471; K b4 83, b8 371, b16 476, b54 255 | M | headline-supporting; b16 re-solved in the audit and the K-cut chains (≤ 2·10⁻⁵); b4, b8 not |
| I-28 | K priced (n = 6 budgets × prices; n = 8 catalogue; lazy PrudentBot copy-clique) | `Chain`, `eager_poly=False` | cut ≤ 1e-6; n_states not stored | 158/191/386; 589/594/1,218 | M | medium (budget copies are payoff twins) |
| I-29 | Modal dollar one-population paired chains, n = 7 (P(eff) modal/weak at N 10²–10⁵) | (a) lazy `Chain`, θ 1e-7/1e-9; (b) `modal_dollar.seeded_chain` (log GTH; all K monomorphic + 47 deep polymorphisms from ≤ 3-class search + one layer; max_states 4000) | (a) cut 1e-15 gave 0.445 vs 0.653 truth; (b) log10_cut −25 to −200 | modal 205; weak 77 | M | **high**, N = 10⁴, 10⁵ audited; N = 10², 10³, 3·10⁴ and the weak n = 7 comparator (1.000) not audited |
| I-30 | Modal dollar augmentation (P, P′, twins at 10⁻⁴–10⁻²) | `seeded_chain`, lumped | n_states 333–376; log10_cut −6 to −65 | ~207 | M | medium–low |
| I-31 | Reduced subsystems {S3, S5, A5(, P′, P)} | `full_chain`: θ = −1, every reachable state expanded | max_states 6000 never reached | 4–5 | C | excluded |
| I-32 | Modal dollar **fixed-role** chain (modal N = 10³: 50–50 0.292, 1/3-type 0.474, endpoints 0.233; weak 0.293/0.479/0.228; "no ratchet") | `fixed_chain_lazy`: θ 1e-12, **max_states 8,000**, started from 25 constant pairs; weak arm `fixed_chain_full` (5,929 states) | **CAP HIT**: n_states = 8000, cut 9.8e-4 (N = 100), 5.2e-3 (N = 10³); constant pairs hold 0.93; a sparse full solve was stopped after 42 CPU-min; no modal solve at N ≥ 10⁴ | modal 205² = 42,025; weak 77² = 5,929 (complete) | **R** | medium–high; never audited |
| I-33 | K+4m chains (n = 8 b16, b54; n = 6; Part C) | `Chain` via `k_four` | n_states == n_classes; cut ≤ 1.9e-7 | 474/255/476/461; 51, 32 | M | low |
| I-34 | K with cut: chains (n = 8; K, Kc, free) | `chain_log` seeded, log_theta −27.6, `deep_states(max_types = 2)` (n_deep = 0); lazy `Chain` as discovery audit | n_states 320–918; log10_cut −9.9 to −11; lazy vs seeded ≤ 3e-6 | 253–478 | M | best-audited chain in the inventory; low |
| I-35 | K-cut factorial and long-guard graft | `chain_log(lazy=False)` | n_states 603–694; log10_cut ≈ −10 | 476–481 | M | low–medium |
| I-36 | Concessions (P01 fair share 0.0086 / 0.0091 explored, cut-corrected 0.0020 / 0.0008; zero wage 0.48; RR ¼ wage 0.76) | `UChain.explore_hybrid`: θ 1e-9, max_states 400k, core_max 2500, promote 1e-6; 1,457 mutated boss functions (98.6% of mass) | `rel_cut_change` 0.094 (N = 10⁴), 0.216 (3·10⁴); 21.9k states of 1.85e8; θ 10⁻¹⁰, 10⁻¹¹ never finished; published fair values are first-order cut-corrected, not re-solved | KcB 1,393 (P01) / 841 / 297; KcW 364; ∏ = 1.85e8 / 1.11e8 / 3.9e7 | **R** | **high** (headline "the concession loses to the prior"); correction lowers fair |
| I-37 | Guard margin as a heritable trait (P(C,C) .392/.671/.791 g0-only; mixed .384/.647/.761) | `KChain` (`guard_trait.seeded_chain_k`), log_theta ln 1e-12, max_states 6000 | 598–1,834 states; n_deep_poly 0; log10_cut ≈ −10; lazy solver agrees; polymorphic states carry 4e-7 | 479–1,158 | M | low (exposure is the K_c4 table, not the chain) |
| I-38 | Milestone 2 carrier populations (P(C,C) = 1 by ten TwinD cliques at N = 10³–10⁵; no-clique controls .503–.908) | `LogChain`/`FastChain`, twins, log_theta ln 1e-14 (controls ln 1e-8), MAX_STATES 60,000 | controls cut_rel .0003–.0086 except U×P no-clique N = 10⁵ **0.1086**; U×P N = 10³ main cell 0.107; 578–705 expanded; closure complete, no stable polymorphism | K = 588 / 701 / 3,115 | M | medium; the absorption claim is robust, the U×P control is uncorroborated |
| I-39 | Identity and tags (reduced-support chain absorbed by cliques; no-clique control .56/.78) | `LogChain`/`FastChain`, ln 1e-8, cap 60,000; **hand-restricted support** (1,500 heaviest + 322 cliques; 500-class variant) | cut_rel .0007–.0022; the full 3,974-class chain did not finish one cell in 90 min; the 500- vs 1,500-class check moves P(C,C) .78 → .47 | 3,974 full; supports 1,818 / 821 / 1,496 / 499 | **R** (by hand) | medium for the controls; support-sensitive |
| I-40 | Prudent openness (reduced chain P(C,C) .589 / .800) | `LogChain`/`FastChain`, θ 1e-8, 4000 cap; support 1,587 | cut_rel .002; omitted exits mass 0.033 | 1,587 of 3,974 | **R** | medium–low (stated diagnostic) |
| I-41 | Fixed-role chicken / hawk–dove: two-population chain | `two_pop_chain` exact K² | cut ≤ 7e-31 | 46 / 51 / 12 / 8: K² 2,116 / 2,601 / 144 / 64 | C | excluded |
| I-42 | Fixed-role chicken: one-population modal chains (payoff per player −0.10 chicken, 0.02 hd3, 0.83 hd6) | `onepop_chain`, `LogChain`, ln 1e-14, max_states 3000 + seeds, closure never complete | **cap hit** (n_cand_left > 0): chicken N = 10², hd3 N = 10², 10³, **10⁴** (16 left, log10 cut −14.7), hd6 N = 10², 10³; lumped vs twin-expanded differ 4× (chicken −0.398 vs −0.098) | one-population K = 51 | M (cap-limited polymorphic search) | medium–low |
| I-43 | SOG over the realizable language: N = 10⁴ chain "not converged", no π published | `FChain` on `UChain`, θ 1e-9, core_max 2500, 5 rounds | ring 34,722 states, rel_cut 0.829 | 77,211 × 318² = 7.8e9 | R (nothing published) | nothing to audit; record |
| I-44 | Gene arm (uniform-prior named catalogue: G-cred fair 0.914; length-prior CC arms zero wage 0.45–0.48) | uniform: `FullChain` (complete triples); length prior: `GChain` hybrid θ 1e-9, max_states 400k, core_max 2500 | uniform cut 0 (**C**); length `cut_total_rel` ≤ 0.041; `fair_cut_corrected` stored (G-all .0153 → .0099) | uniform G-all 87×28; length G-all 706×80 | uniform C; length **R** | medium (the headline 0.914 is a complete solve) |
| I-45 | Milestone 5 certificates as genes (frozen-inventory chain, P(C,C) = 1.000, H-list cliques) | `LogChain`/`FastChain`, twins, ln 1e-14, max_states 20,000 | 701 expanded; cut not stored | 7,895 types → 701 classes | M | diagnostic; low |
| I-46 | Stable sets on islands (one chain line: dollar3 weak N = 100 rerun, fair .373, unfair .590) | `Chain3` hybrid via `dollar3_run.py`, θ 1e-9 | rel_cut .0037; 31,989 states | 903 per slot; 7.4e8 | **R** | low (reproduces I-22 to four decimals) |
| I-47 | Dominance contracts (stationary mass of V\* = 1/3) | `np.linalg.eig` on a 20-state matrix | none | 20 | C | excluded |
| I-48 | RPS and mixed actions (e = 0.666/0.291/0.017/0.002 at N = 10²–10⁷; exact 0.703/0.432/0.055/0.010; π(Z0)) | `LogChain` via `rps_run.chain_cell`, twins (n_twin_moves = 0: all monomorphic), log_theta ln 1e-14, max_states 20,000 + seeds, closure 6000 | closure_complete True everywhere; n_expanded = n_recurrent = K; n_seeded 0; no cut | pure 18; sample, matched 87; exact 125; n = 7: 24 / 254 / 376 | M (no stable polymorphism) | headline (2026-10-23); twin risk absent (zero-sum tournament) |
| I-49 | RPS with a compute price (π(X) .24/.43/.84/.98; forfeit-only readers .27–.39 at N = 10⁵) | `LogChain` via `rps_priced_run.chain_cell_p`, twins (≤ 65,942 moves), log_theta ln 1e-8 (1e-6, 1e-10 sensitivities), max_states 40,000; seeds from `discover()` (exhaustive pairs and triples, invasion closure branch 8 / 6000 nodes, 1000-start attractor search ≤ 6) | `log10_cut` −7.2 to −9.3 (c ≤ 0.01), −5.5 to −6.9 (c = 0.05; forfeit-only N = 10⁵); closure_complete False for exact c = 0.01, exact_br, c = 0.05; polymorphic mass 5e-5–4e-4 (c = 0.01, N = 10⁴), 0.11–0.17 (forfeit-only, N = 10⁵) | 18 / 88 / 126 / 124 | M | headline (2026-10-23); medium–low for c = 0.01, medium for forfeit-only and c = 0.05 |
| I-50 | Mixed actions in two-role games: whole-space chains (inspection exact c = 0 −0.777/−0.496/−0.471; c = 0.01 −0.632/−0.623; matched; sample; blind; Endgame exact/sample/blind) | `TwoPopChain.solve_full` (jump-chain GTH, holding-time corrected) | `capped` False | 24,649 / 27,889 / 9,409 / 11,236 / 6,889 / 7,396 / 289 (inspection); 14,472 / 16,146 / 5,311 / 1,411 (Endgame) | C | the **positive control** family; inspection exact c = 0.01 at N = 100 never run whole-space |
| I-51 | Mixed2 exploration-capped cells (inspection sr4, sr16 at c = 0; Endgame matched c = 0.01; exact c = 0.01 N = 100): marked "not converged" in RESULTS | `TwoPopChain.explore`, relative θ ln 1e-10, max_states 1,500, max_add 400 | `log10_unexplored` −2 to ~0; sr16 at N = 10⁴ reports −2.46 (outside the payoff range); sr4 N = 10⁴ single-state π | sr4 533² = 284,089; sr16 436 × 412 = 179,632; end-matched 440 × 197 = 86,680 | **R** | not cited numerically; dense solves need 60–650 GB |
| I-52 | Social organization game under the seed lottery: "chain π (control)" column | hard-coded text quoted from I-23, I-24 runs | n/a | n/a | N | not a chain computed there |

### 1.2 Counts

* Chain-result groups inventoried: **52** (I-01 … I-52), plus the Solver audit itself (RESULTS "Solver audit"), which is
  a re-solve of 15 groups' cells rather than a new chain.
* Excluded as complete (**C**): I-18, I-31, I-41, I-47, I-50 (5 groups), plus the uniform-prior arm of I-44 and Part B of I-24
  (parts of groups that also have restricted parts). Not reproducible/superseded or not a chain (**N**): I-02, I-52.
* Chain results with capped or thresholded exploration (M or R): **45 groups** (52 − 5 complete − 2 N) (spec prediction 1 threshold: 10), of which
  **R** (monomorphic space itself restricted): I-03, I-05, I-06, I-17, I-22, I-23, I-24C, I-32, I-36, I-39, I-40, I-43,
  I-44 (length prior), I-46, I-51 = **15**, and **M**: the remaining **30**.
* Hit a hard cap in the stored record: I-32 (`max_states` 8,000), I-42 (`n_cand_left` > 0), I-22 (`core_max` 2,500 at
  N = 10³), I-51 (1,500), I-08 possibly (n = 8, N ≥ 3000: the record does not store n_expanded).
* Already re-solved, wholly or in part, by the 2026-10-05 Solver audit (cells listed there): I-07 (N = 10⁴ w = 0.3), I-08
  (n = 9, N = 10⁴, 3·10⁴), I-11 (c = 10⁻², N = 10⁴: atoms n = 6, 8; lazy n = 8), I-26 (dollar5/dollar3 N = 10³, 10⁴, 3·10⁴),
  I-27 (K b16 N = 10⁴), I-23 (QUORUM c = 0.5, N = 10³), I-22 (modalPA N = 10³: re-run exact, lower-θ re-solve unfinished),
  I-29 (modal N = 10⁴, 10⁵).

### 1.3 Reproducibility facts that bind the plan

* This machine: 10 cores, 16 GB RAM. Dense matrix of s states costs 8 s² bytes: 4.9 GB at 24.6k states, 20 GB at 50k.
  The earlier whole-space mixed2 jobs used 3–5 GB.
* Gitignored caches (`runs/*.pkl`, `runs/*.npz`) exist only in the main checkout `/Users/jstav/code/program-ecologies/runs/`;
  `runs/dollar3_classes_*_slot1.npz` and `runs/guard-trait/vK_n8_b16.npy` are tracked. K tables absent from both checkouts
  (must be rebuilt, 2–15 min each): `kval_n8_b*.npy`, `runs/modal_dollar/classes_*.npz`, `proof-length-karm.npz`,
  concessions `lang_*.npz`, carrier-population and identity static caches, `lt_genes` statics, `classes_quorum.npz`.
* `run.py`, `run_ult.py`, `limN.py`, `modal_limN.main` and others overwrite tracked `runs/` files: every audit call must
  go through functions that return results rather than `main()`.
* `chicken_norole.yaml`/`demand_norole.yaml` run with ROLE unless `--norole` is passed (commit 7f2aac6).

## 1.4 Triage order

Order: first the mixed2 positive and negative controls (they gate everything), then by (monomorphic-restricted, large
payoff-twin grammar reached through reading programs, headline size), then the cheap monomorphic-complete cells whose
claim is a headline. Cells that cannot be reached are marked *unresolved* in the run report, never passed.

1. **Controls:** mixed2 inspection exact c = 0, N = 10⁴ (positive: −0.009 at 1,500 states, −0.47 whole-space); a small
   complete cell (blind inspection 289 states, and a small `Chain` cell) as the negative control; compare caps and
   exploration seeds on two tractable cells (mixed2 inspection blind and sample).
2. **R cells with a stored cap or large published cut, reachable:** I-32 (modal fixed-role dollar; cap hit), I-05/I-06
   (ultimatum two-population; whole space 1,936 / 432 / 1,980), I-24C (RR and RC enforcement: 5·10⁴ and 4·10⁵ states),
   I-36 (concessions; cut 0.09–0.22), I-22 (three-player dollar; θ sensitivity), I-23 (union at N = 10⁴, θ not N-scaled),
   I-44 length prior, I-03 (n = 7 sparse seeds), I-46.
3. **M cells that are headlines or twin-heavy grammar (stage d, polymorphic search plus twin-expanded where the published
   model was lumped and pre-2026-10-05):** I-48/I-49 (RPS, 2026-10-23), I-29 (modal dollar N = 10², 10³, 3·10⁴ and the weak
   comparator), I-42 (capped one-population chicken), I-38 (U×P control), I-16/I-28 (P\*/PrudentBot deep states), I-19
   (μ-fringe exits), I-27 (K b4, b8).
4. **Hand-restricted supports and by-design restrictions:** I-39, I-40 (support sensitivity), I-17 (R2 by design), I-51
   (sr4, sr16, end-matched: dense solves infeasible).
5. **Left unaudited unless time allows (low risk, complete monomorphic space, no polymorphic mass):** I-01, I-04, I-07 (other
   cells), I-09, I-10, I-12, I-13, I-14, I-15, I-20, I-21, I-25, I-30, I-33–I-35, I-37, I-45.

Twin-network risk flag (spec prediction 3 names it): large payoff-twin networks reached through reading programs occur
in I-08, I-16, I-19, I-22, I-23, I-24, I-29, I-32, I-36, I-38–I-40, I-49, I-50, I-51.

## 2. Deviations and facts found while running (written after the audited cells began)

**Method.** Stages follow the spec: (a) the published configuration re-run with the published code; (b) every active restriction
enlarged together (cap, threshold, rounds, with the memory limit stated where 10x was not possible); (c) the whole monomorphic
space where it fits (mixed2 and the two-population ultimatum arms only); (d) polymorphic states added from the recurrent monomorphic
classes, in the bounded form of the spec (`src/exploration_audit.py::sa_bounded`: published `Chain` re-run, then `LogChain` seeded
with the published polymorphic states, every monomorphic class expanded, their targets, then inflow rounds at log10 theta -14, cap
8,000) or with the solver-audit pipeline (`solver_audit.run_cell`, exhaustive pairs and triples plus the invasion closure) where K was
small; (e) twin-expanded only where the published cell was lumped and a twin-expanded `LogChain` exists (dollar arms). All code is in
`src/exploration_audit.py` (adapters, no existing file edited) and `src/exploration_audit_run.py` (CLI, one job per process, one thread
each); records in `runs/exploration_audit/` (small json). The shared host was loaded by other sessions (load average 8-9, 7.6 GB swap in
use), so wall times are inflated, which is why several hour-scale cells were stopped.

**Frontier outflow.** Defined as the pi-mass of explored states with an outgoing transition into an unexplored target whose
relative inflow exceeds the stage's own threshold (the targets the explorer would still add, i.e. the ones a cap, not the threshold,
left out); the strict count of states with any unexpanded out-rate share above 1e-6 is 1.0 in every capped mixed2 cell and is
recorded but not used as the flag. Flag: frontier mass above 0.01 means *unconverged*. For the hybrid chains (`Chain3`, `UChain`) the
relative outcome-changing cut stands in for it; for the log chains `n_cand_left` (candidates still above theta at exit).

**Reproduction record.** Reproduced exactly (state counts and statistics to the published digits): mixed2 inspection exact c = 0 at
1,500 states (-0.0093 vs -0.009), at 8,000 (-0.4707) and whole space (-0.4707 vs -0.471); inspection exact c = 0.01 N = 100 at 1,500
states (-0.7921); blind inspection (289 states); the three ultimatum arms (152 / 144 / 160 expanded, cut 2.56e-5 / 7.0e-6 / 2.89e-5);
the union game quorum c = 0.5 at N = 10^3 and 10^4; enforcement Part C RR (N = 10^3, 10^4) and RC; concessions P01 N = 10^4 (21,913
states, fair 0.008553); the modal fixed-role dollar at N = 100 and 10^3 (8,000 states, cut 9.78e-4 / 5.22e-3); the one-population modal
hd3 N = 10^4 cell (3,005 states, 16 candidates left, payoff 0.0158); three-player dollar weak at N = 100 (31,989 states, the stable-sets
re-run; the original had 32,259) and N = 10^3 (31,686 states); priced RPS exact forfeit-only c = 0.01 N = 10^5 (4,466 recurrent states,
polymorphic mass 0.109, log10 cut -5.5087); the K-arm and modal PD cells (kb4, kb8, modal6, modal8). **Not reproduced:** the
4,000-state point of the mixed2 contrast (-0.4708 here against the -0.31 in `notes/mixed2.md` §3; the 1,500 and 8,000-state points
reproduce, so the difference is in the earlier 4,000-state run's settings, which are not recorded).

**Inputs rebuilt or copied (all gitignored or in the scratch directory, none committed).** mixed2 class tables and the priced-RPS caches
were taken from the earlier runs' temporary caches on this machine; the enforcement run's `classes_CC.npz` (copied from the main
checkout's gitignored cache) is the quorum arm's class lumping and was used for the union game, which the exact reproduction of the
published union cells supports; the fixed-role chicken catalogues and the dollar evaluation tables were copied from the main checkout's
gitignored cache into the worktree's gitignored `runs/` paths; the ultimatum published rows predate `ROLE` becoming first-class
(7f2aac6), so the audit rebuilds the `Language` with `role=False` (902 programs, 44 classes), which reproduces them (`twopop.build`
itself now builds the ROLE language and would not).

**Jobs stopped before completion (each recorded here; no value from them is used).**
union quorum c = 0.5 N = 10^4 at theta 1e-11: round 1 alone took 81 min (42,007 ring states, relative cut 0.175, 10,427 new
candidates) and was stopped, and theta 1e-12 was not run; enforcement CC N = 10^3 at theta 1e-11 (42,902 candidates in round 0,
stopped); modal dollar N = 100 through the solver-audit pipeline (its published-rerun step is the lazy linear chain, which did not
finish in 33 min and is not the published configuration at that N; the published configuration, the seeded chain, was run instead);
modal dollar N = 10^2 theta 1e-12 twin-expanded (40 min) and N = 3·10^4 twin-expanded (38 min) stopped; the priced-RPS enlargement at
log10 theta -12 with 18,000 closure nodes, branch 16 and 4,000 starts ran 4 h 13 min without finishing and was replaced by a milder
enlargement (log10 theta -10, 12,000 nodes, branch 8, 2,000 starts); `pd-pr8-depth-c0.01` through the solver-audit pipeline (78 min)
and through the bounded pipeline (42 min) and the n = 8 drift-closure fringe cell (40 min) were stopped; the dollar-partition cells
(`dollar5-role` N = 100 through the solver-audit pipeline ran 2 h 30 min without finishing: unresolved); one-population chicken hd6
N = 10^3 at 12,000 states ended in an exception after 1 h (the exit-analysis step found no recurrent class in the capped set; the
solve itself had finished), hd3 at N = 10^3 with a 24,000-state cap failed the same way after 1.5 h (empty recurrent class; `np.argmax` of an empty sequence in `onepop_chain`), and hd3 / hd6 at
N = 100 were not run. after the outage the priced-RPS enlargement with theta alone lowered (log10 theta -11, everything else published) was run once more and stopped
at 2 h 15 min without finishing, so the I-49 enlargement is unresolved. **Bug fixed during the run:** `make_cell` recursed through the
patched `solver_audit.make_cell` in the first launch of the dollar-partition jobs (16 jobs failed at start; relaunched).

**Disclosure (order).** The harness was developed on the ultimatum arms and the modal fixed-role cell before the controls were
committed (commit "harness and controls"); those two families' stage (a) values were therefore seen before the commit; none of
them changed a prediction or a threshold. The mixed2 4,000-state discrepancy was seen at the control and is reported, not smoothed.
