# Queue 80 gates (`src/script_offers_gates.py`; tables at (KR', cap') = (384,000, 128,000))

Fuel: KCHK = 16,000, W = 16,005, cap' = 128,000, KR' = 384,000. **κ_S = 15141** (worst accepted S0 check; worst over every catalogue check and forger, rejections included: 15141).

## G1 soundness

- Check map: S0 (the L_T^code term) and the independent host reference agree on all 910 (program, code) entries (159 catalogue programs + 23 forgers, codes 1–5); S1 uses S0's map and counts.
- Cube: every accepted (program, code) against every (next, prev) of the 159-program catalogue: 7862391 checks per machine; **false acceptances S1 0, S0 0**.
- Forgers (accepted / allowed true statements):

  - q79XmBn: accepted `–`, allowed `–` — queue 79 forger: bully body with Ocp certificate data in milestone-4 shape
  - q79XfakeBn: accepted `–`, allowed `–` — queue 79 forger: skeleton calling a lookalike combinator (ignores cert) with Ocp cert, bully fallback
  - q79XswapBn: accepted `–`, allowed `–` — queue 79 forger: skeleton with n and p swapped
  - q79XappBn: accepted `–`, allowed `–` — queue 79 forger: fallback an application (not a value)
  - q79XbitBn: accepted `–`, allowed `–` — queue 79 forger: certificate flag 2 (malformed)
  - q79XopBn: accepted `–`, allowed `–` — queue 79 forger: certificate computed (op), not a literal
  - q79XifBn: accepted `–`, allowed `–` — queue 79 forger: skeleton under an if (semantically the carrier)
  - q79Xconst: accepted `–`, allowed `–` — queue 79 forger: returns certificate data as its value
  - XscrBn: accepted `–`, allowed `–` — Ocn's valid script on the simulating bully's body
  - XnxBc: accepted `1234`, allowed `1234` — Fc+'s script (offers and S_nx) on Bc's body with H = 1
  - XfakeBc: accepted `–`, allowed `–` — FAKEOFFER (ignores the certificate) with Bcn's script
  - XswapBc: accepted `–`, allowed `–` — n and p swapped in the canonical call, unswapped script
  - XfuelOc: accepted `12`, allowed `12` — S_nx script on a program that names 2/3 only when its read exhausts the root fuel
  - XassumeBc: accepted `–`, allowed `–` — a tree node asserting an atom value
  - XvacBc: accepted `–`, allowed `–` — VAC on a branch where the guard can hold
  - XwrongBc: accepted `34`, allowed `34` — names prev when next is the preferred eligible partner (E = {next})
  - XbadR: accepted `–`, allowed `–` — requirement flag 2 (malformed)
  - XopScr: accepted `–`, allowed `–` — script computed by an op term
  - XselfC: accepted `–`, allowed `5` — calls CHKS on its own quote
  - XidC: accepted `–`, allowed `125` — identity test eq n me
  - XfixC: accepted `–`, allowed `5` — body uses fix
  - XinspC: accepted `–`, allowed `–` — body inspects the partner's quote (fst n)
  - XconstC1: accepted `125`, allowed `125` — the 1/2 constant naming next with a one-leaf tree (true statements)

## G2 completeness on spellings

- Every one of the 100 carriers is accepted for exactly its statements (mismatches: 0). Script sizes and S0 check costs per spelling: `gates.json` G2.spellings.
- Pairs beside every non-carrier (59), every seat pattern (6), both machines: every certified-eligible pair (eligibility predicted from the parameters) forms the fair pair: 0 eligible-but-not-paired, 0 timed-out reads by the pair (S1); S0: 0, 0.
- Extra gates: (Pc⁺, Pc⁺), (Pc⁺, Oc⁺), (Pc⁺, Rc⁺), (Pc⁺, Fc⁺) eligible and paired in every such triple; (Pc⁺, Bc), (Pc⁺, Oc), (Pc⁺, Rc) never eligible.
- **Fallback pairs** (not eligible, yet the fair pair forms through the two fallbacks):

| pair | triples | eligible | fair pair observed (all by fallbacks) |
|---|---|---|---|
| s_bully|s_openR+ | 35400 | 0 | 8400 |
| s_bully|s_prud+ | 35400 | 0 | 10050 |
| s_firm|s_openR+ | 35400 | 0 | 12000 |
| s_firm|s_prud+ | 35400 | 0 | 13200 |
| s_openR+|s_bully | 35400 | 0 | 8400 |
| s_openR+|s_firm | 35400 | 0 | 12000 |
| s_openR+|s_open | 35400 | 0 | 8850 |
| s_open|s_openR+ | 35400 | 0 | 8850 |
| s_open|s_prud+ | 35400 | 0 | 12000 |
| s_prud+|s_bully | 35400 | 0 | 10050 |
| s_prud+|s_firm | 35400 | 0 | 13200 |
| s_prud+|s_open | 35400 | 0 | 12000 |

  Pc⁺'s fallback is a firm reader that accepts any partner naming it at ½; Bc's fallback (the simulating bully) names its prev at ½ unless its next names it at ⅓, and Oc's fallback is the ½ constant naming the offered partner. Certified exclusion therefore does not prevent a fair pair between Pc⁺ and Bc when the third slot does not name Bc at ⅓.
- Three carriers (every ordered all-carrier triple), outcome by family multiset: `gates.json` G2.triples3; S0 = S1: True.

## G3 the skeleton check on the same catalogue

- Queue 79's CHK accepts the 8 canonical K-world carriers and rejects all 32 non-canonical K-world spellings and every world-S program (accepted in world S: none).

## G4 mixed worlds at the new fuel

- Outcome triples among the first 59 programs that differ from queue 78's old-fuel table: **0 of 205379**.
- Reader–reader profiles (root reader, a reader partner): 161280; timed out at the old fuel 135168, at (KR', cap') 135168; persist 135168, vanish 0, appear 0. The mutual-read timeouts persist at 320× caps.
- A simulating reader reading a carrier times out in 29.4% of profiles; a carrier (in its fallback) beside a reader in 18.7%.

## V3

- S1 against S0 on all 4601142 profiles (159 + 23 forger rows × 159²): code 0, steps 0, failed reads 0, forfeits 0 differences.
- Interruption: every tabulated check at residual fuel one below and at its cost, at root and inside a capk frame: 3640 tests, 0 differences.

