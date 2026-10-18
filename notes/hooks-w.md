# Hooks, Part W: a first-class hook primitive in the weakly extensional wing (notes, 2026-10-18)

Spec `specs/2026-10-18-hooks.md` (reviewed by gpt-6.1-sol, then gemini-4-argon; the two amendment sections supersede
the earlier text, the later one winning). This file covers Part W only; Part R is run separately. §1 is written by hand
before any code of this run and before any counted cell. §2 (the built language, validation, projected costs, any
deviation) is appended after the code and before any counted cell.

Machinery imported unchanged: the modal arm (`src/modal.py`: the free sound box, GL on the linear Kripke chain, the
length prior), the ε = 0 island lottery of `src/almost_all_seeds.py` (its kernel is the stored baseline), and the
union game's grammar, payoff table and evaluator semantics (`src/union.py`, the CC arm of `src/union_enforcement.py`)
with the seed-lottery kernel of `src/sog_lottery.py` (its stored baseline). No existing file is edited.
Every ε = 0 number in this run is a lottery statistic at finite (N, I, horizon); nothing here is π.

## 1. Design

### 1.0 The object in one paragraph

The RS's paradigm (DEFERRED 12): a base program leaves **hooks** that **genes (fills)** fill, with maximalism about
which hooks are expressible. In the weakly extensional wing a fill is a parameter of the program, so a filled program
is a modal program with parameters and "proof genes" and "override genes" coincide: every fill is read by the free
sound box exactly as the program's own syntax is, so soundness is by construction (Lemma 0 still holds: no hooked
program can exploit a sound prover). The run asks what the extra, length-free expressivity of fills does to the
seed lottery in the PD (islands and fission–fusion) and to the wage in the social organization game, per hook kind,
against an inert-hooks control with the same grammar, prior and storage.

### 1.1 The primitive in the modal PD grammar (n = 6)

    A   ::= C | D | HOOK(t, a0) | not A | and A A | or A A | BOX(App) | BOXD(App) | BOX1(App) | BOXD1(App)
    App ::= THEM(ME) | THEM(THEM) | THEM(^A)

- `HOOK(t, a0)` is a leaf of one node, t ∈ {0, 1} (so a program has at most two tags), a0 ∈ {C, D} the default.
  Four hook leaves join the two constants; **every hook costs one node whatever the scope of the fill that ends up
  filling it** (the scope lives in the fill, not in the node), which is the spec's equal-node-cost rule.
- Semantics. At a world of the Kripke chain, `HOOK(t, a0)` evaluates to the action of the fill selected for tag t
  in the current match (§1.4), if one applies, else to a0. Internally each tag carries two derived atoms, A_t ("a fill
  for t applies") and V_t ("the selected fill's action is C"), so `HOOK(t, C)` = ¬A_t ∨ V_t and `HOOK(t, D)` =
  A_t ∧ V_t, and every program is a boolean function of its box atoms and these four hook atoms. Programs are
  merged into canonical functions as in `modal.py`; two spellings with the same canonical function are one base type.
- **Quoted programs carry no fills.** In `THEM(^A)` the quoted A is bare source: its hooks evaluate to their
  defaults (A_t = 0). So the probe set of the box atoms is the plain modal canon of A with hooks at default, and the
  box-atom set at n = 6 is the plain arm's (quoted A has at most 3 nodes).
- Prior: the length prior of the arm, bits(p) = log2 a(|p|) + 2 log2 |p| + 1 with a(s) the number of spellings of
  size s in the hooked grammar; the mass of a base type is the sum over its spellings. The hooked grammar has six
  leaves, so hook-carrying spellings take most of the mass (at size 1 the four hook leaves alone carry 4/6 of it).
- No `ROLE` and no X: the modal arm has neither (§1.3 for what "role scope" means here).

### 1.2 The primitive in the weak social organization grammar

The union game's grammar (boss n = 6 over BOX(W_j = work | strike); workers n = 10 over the wage, whack, OTHER and
QUORUM atoms; level 0; CC evaluation, c = 0.5, L = 1), extended by hook leaves:

    A ::= a | HOOK(t, a0) | if(B, A, A),     t ∈ {0, 1}, a0 ∈ the role's actions

so the boss has 9 actions and 18 hook leaves, a worker 2 actions and 4 hook leaves, each one node. Fill actions are
the role's actions (boss: a wage in {0, 1/4, 1/2} with a whack policy in {strike, none, source}; worker: work or
strike). The union tag (an essential QUORUM atom, what source targeting reads) is a property of the base program and is
unchanged by fills. Payoffs are the union table.

The grammar *with probes* in this wing is supplied by the behaviour scope (§1.3): a behaviour-keyed fill is exactly a
probe ("pay 1/2 to a worker who would strike against the zero-wage boss" is HOOK(0, (0, none)) with the fill
(0, behaviour, (W_j, β), (1/2, none)) for the matching β). Concessions' n = 11 boss grammar is not rebuilt: the
behaviour scope gives the same reads at no node cost, which is the design question.

### 1.3 Scopes and key domains (finite)

| scope | PD key domain | social organization key domain | applies when |
|---|---|---|---|
| none | one key | one key | always |
| role | one key (the PD is one symmetric population with one role) | the holder's slot: boss {B}, worker {W1, W2} | key = the holder's role |
| history | founder lineages of the run (N·I) | founder lineages of the run (3·N·I) | some partner of the match descends from that founder |
| behaviour | the 8 classes β (below) | (partner position, β): 2 × 8 = 16 keys | the named partner's class is β |

- **Behaviour class** (the spec's "partner's play against ⌜C⌝, ⌜D⌝ and the program itself", read by the prover):
  three boxes. PD: β = (□ partner plays C against ⌜C⌝, □ partner plays C against ⌜D⌝, □ partner plays C against
  me), all at level PA. Social organization: for holder h reading partner p in the current encounter E,
  β = (□ p favourable to h in E[h := ⌜C_h⌝], □ p favourable to h in E[h := ⌜D_h⌝], □ p favourable to h in E), where
  E[h := q] is E with h's slot replaced by the constant q (the other slots keep their actual programs, as concessions'
  quoted encounters did); ⌜C⌝/⌜D⌝ are work/strike for a worker and (1/2, none)/(0, none) for the boss; a worker is
  favourable to anyone iff it works; the boss is favourable to worker j iff j is not whacked and, if j works, s ≥ 1/4.
  A boss's two partners are W1 and W2; a worker's are the boss and the other worker.
- **Role scope in the PD** has a single key, so a role fill applies always and differs from a none fill only by its
  priority. I do not import `ROLE` into the modal PD through hooks: the modal arm has no `ROLE`, and adding a
  correlating device only through hooks would confound hook semantics with that capability (dropped design, §1.10).
- **History keys** are the partner's founder ID (its lineage; amendment 2 of the second review), not its behaviour.
  A copy of oneself has one's own lineage, so a program can hold a grudge against its own lineage.
- A fill on a tag its holder does not carry is held and inherited but never applies.

### 1.4 Fill resolution and the conflict rule

For each tag t of the holder in a match: the candidate fills are those of tag t that are *active* in the cell (§1.8)
and *apply* (table above). **Most specific scope wins:** behaviour > history > role > none (the spec's order with the
Part R scopes removed); ties by recency (the most recently written or refreshed fill). **Ablation "recency only":**
the most recent applicable fill wins whatever its scope. With no candidate the hook takes its default. In the social
organization game two behaviour fills can match at once (one per partner); recency decides.

### 1.5 Evaluation, circularity and recursion fuel

All reads are boxes on the linear GL chain, so every self-reference is guarded and the fixed point is unique (box truth
is monotone non-increasing in the world, so every match stabilizes; no selection rule).

- **PD.** One match x vs y is evaluated on a finite node set: the probe nodes (the plain canons that are quoted
  anywhere, plus ⌜C⌝ and ⌜D⌝, which carry no fills) and the two instance nodes x and y. An instance plays a node q with
  its fills resolved for that opponent: against a probe node no history key matches (a quote has no lineage), against
  the other instance the key is its lineage, and against a copy of itself (needed when the partner reads
  `THEM(THEM)`) the key is its own lineage. Behaviour atoms of x against q read hc[q, ⌜C⌝], hc[q, ⌜D⌝] and hc[q, x] at
  level PA. The node set is closed (a probe's boxes read only nodes of the set), so **no recursion fuel is needed**;
  the probe that would "exhaust" a fuel does not exist here.
- **Social organization.** One encounter (b, w1, w2) is evaluated on the closure of slot substitutions: every
  encounter whose slots are each the actual program, ⌜C⌝ or ⌜D⌝ of that role (27 nodes). Base atoms are boxes of
  propositions about the node's own joint action (the union semantics); behaviour atoms read the favourable-propositions
  of the nodes E[h := ⌜C⌝], E[h := ⌜D⌝] and E. A slot replaced by a constant has no lineage. Again closed: no fuel.
- **Payoffs** of the actual match from the stable joint action (PD: the arm's table D/D −1, D/C 1, C/D −2, C/C 0;
  social organization: the union table with c = 0.5).
- Probes against self use the prover (the third behaviour bit and every `THEM(ME)` read is a box).

### 1.6 Fills: storage, inheritance, eviction

- A program carries at most 4 fills, in recency order. A new fill whose (tag, scope, key) matches a held fill
  **updates that fill in place** (action and recency) and evicts nothing (second review, amendment 1); otherwise it is
  appended and the oldest fill is evicted beyond 4 (FIFO). Evictions are counted per encounter.
- Fills are inherited by offspring (and by migrants' offspring) and never expire otherwise. Bare source excludes fills.
- Each fill records its origin (seeded, written, copied, contract), which decides activity under the fill-source
  ablations; origin does not change what a fill does.

### 1.7 Fill sources

1. **Seeding (the gene prior).** Each founder carries k fills, P(k) ∝ e^(−1)/k! on k ∈ {0, …, 4} (Poisson(1)
   truncated at 4 and renormalized: 0.3695, 0.3695, 0.1847, 0.0616, 0.0154). Each fill draws its tag uniformly from
   the program's tags (a founder with no tag carries none), its scope uniformly from the four scopes, its key uniformly
   from that scope's domain (§1.3) and its action uniformly from the role's actions. Per fill and action the prior is
   therefore 1/4 per scope, spread over 1 key (none, PD role), 1–2 keys (social role), N·I or 3·N·I lineages
   (history) or 8 / 16 classes (behaviour). Fills are drawn from a per-founder stream, so base programs and fill
   draws are coupled across every cell of a part (amendment 3).
2. **History-triggered writes.** A sampled encounter (§1.9) may fire one write per program:
   - *PD:* the program cooperated and the partner defected → a grudge (t, history, partner's lineage, D);
     both cooperated → a thanks (t, history, partner's lineage, C). The tag t is drawn uniformly from the writer's
     tags; a tagless program writes nothing.
   - *Social organization (second review, amendment 4):* a worker that works and receives zero wage or is whacked
     writes a grudge (strike) keyed on the boss; a worker paid at least 1/4 while working writes a thanks (work)
     keyed on the boss; a boss writes a grudge against a striking worker's key with action (0, strike), and a thanks
     against a worker who works at a positive wage with the action it just played. A boss with two triggering workers
     writes about one of them, drawn uniformly.
   - **Grudge-only arm:** thanks writes are not made.
3. **Copying.** After a sampled encounter, a party that wrote nothing copies, with probability q = 0.1, one fill drawn
   uniformly from those of the partner's fills whose tag it carries (verbatim, origin "copied"). PD: from its one
   partner; social organization: only between the two workers (bosses have no same-role partner).
4. **Pair contracts (a two-slot joint fill).** In a sampled encounter, two parties that both carry tags may write
   a joint pair of history fills keyed on each other's lineage, one each, *both or neither*: accepted iff the
   encounter re-evaluated with both fills gives each party at least its current payoff and one party more (the
   third party, if any, fixed). Among accepted candidates one is drawn uniformly (no candidate is preferred for its
   efficiency). PD candidates: every (t_x, a_x, t_y, a_y) over the two parties' tags and actions (at most 16; the
   fill's action is not always the realized play, since a hook may sit under a negation or a box; at the outcome
   level only (D, D) → (C, C) can be accepted in the PD); social organization: boss–worker fill pairs "boss fill
   (s, none) with s ∈ {1/4, 1/2}, worker fill work" over both parties' tags (at most 8), with one worker drawn per
   encounter (a declared restriction of the candidate set, for cost). Contract fills are history-scoped, so the history ablation silences them too.
- At most one fill change per program per encounter, priority contract > triggered write > copy.

### 1.8 Cells and the inert discipline (amendment 3)

Founders and fill draws are identical across the cells of a part (paired by run index). Disabling a scope or a source
makes those fills **inert**: held, inherited, counted, written and copied as before, never applied. Cells:

| cell | change from maximal |
|---|---|
| baseline | the plain modal n = 6 grammar (PD) / the stored union classes (SOG), stored kernel, no hooks |
| inert | every fill inert (the inert-hooks control: identical grammar, prior and storage) |
| maximal | all scopes and sources active, specific-wins conflict rule, grudge + thanks |
| grudge-only | no thanks writes |
| −behaviour, −role, −history | that scope inert |
| −behaviour (renorm.), −history (renorm.) | that scope removed from the seeding prior (scope uniform over the other three) and inert |
| −seed, −writes, −copy, −contract | fills of that origin inert |
| seeding-only | written, copied and contract fills inert (never dropped) |
| history: shuffled | trigger writes keyed on a lineage drawn uniformly from the island's present lineages instead of the partner's |
| history: not inherited | written fills are not passed to offspring |
| recency only | conflict rule ablation |

"−writes" is the spec's "history disabled" control. The shift baseline → inert is the **grammar-dilution effect**,
reported separately; claims about hook semantics are judged against inert (second review, amendment 5).

### 1.9 Objects and dynamics

- **PD islands:** ε = 0, (N, I) = (100, 64), complete island graph, mN = 1, w = 0.3, 40 runs, founders iid from the
  hooked prior over base types, each founder its own lineage. The island Moran birth–death of `almost_all_seeds`
  (parent ∝ count · exp(w f), f the exact mean payoff against the island's other residents, migration with
  probability mN/N from a uniform other island, uniform victim), generalized from classes to **types** = (base type,
  fill list, lineage). After each birth event on island i one encounter is sampled on island i: two distinct
  residents drawn uniformly play one match, and writes, copies and contracts fire (§1.7). That is about two sampled
  encounters per program per generation; fitness stays the exact mean payoff under current fills, so sampled
  encounters only move fills. Horizon 2,000 generations (the stored baseline froze by generation 200–360).
- **PD fission–fusion:** 128 islands of 100 with mN = 1, merged into one population of 12,800 at generation 200,
  horizon 2,000, 20 runs (the Pangaea cell's geometry). Cells: baseline (plain grammar under the hook kernel), inert,
  maximal, grudge-only.
- **Social organization:** the stored seed lottery's CC kernel law (three slot populations per island, parent ∝
  count · exp(w f) with f the expected payoff against a uniform draw of the other two slots, migration per slot) at
  (N, I) = (100, 16), mN = 1, the stored cell CC-mN1, 40 runs, horizon 2,000 generations, one sampled encounter (one
  member per slot, uniform) after each birth event on that island. The spec's (100, 64) is not used for this game: the
  three-slot payoff sums cost O(n₁ n₂) per event with fill-carrying types, and CC-mN1 is the stored run the baseline
  must reproduce (deviation disclosed here, before any code).
- **The ε→0 chain is not run.** Trigger writes change a program within its life and lineage-keyed history makes the
  type space unbounded, so there is no tractable support; I record this as a design limit, not a result.

### 1.10 Statistics

- *Island efficiency* (reported, never a selector): P(C,C) of the island (mean field over pairs) ≥ 0.95.
- *Universal-open (PD):* every island efficient, and every pair of island-majority types (including a type with
  itself on another island) cooperates mutually **as strangers**: both with fresh lineages, so lineage-keyed fills do
  not apply. *Universal-on-target:* additionally every majority type cooperates mutually with an unhooked FairBot
  stranger. *Universal-current:* every island efficient and every pair of island majorities cooperates under their
  actual lineages and fills (cooperation that needs a prior contract or thanks counts here, not in universal-open).
- *Lineage-closed islands* (the wing's analogue of identity islands): efficient islands whose majority type
  cooperates with its own lineage but not with the same type as a stranger. *Rival islands:* efficient islands whose
  majority does not mutually cooperate, as strangers, with the largest stranger-compatible group of majorities.
- *Social organization:* fair-wage, intermediate, zero-wage, strike and scab-split shares of islands at the horizon
  (the stored lottery's island labels); **threat fills** (worker fills whose action is strike; boss fills whose whack
  policy is strike or source) with their held counts, the number of sampled encounters in which one is selected and
  its hook is reached on path (*challenged*), and those in which the threatened act is realized (*executed*).
- *Per hook kind (scope) and per origin:* prior mass (share of seeded fills), share of held fills at the horizon,
  and in sampled encounters: held, applicable (a key matches), selected (wins the conflict rule on a carried tag),
  executed (the match outcome differs from the same match with that party's fills inert); the paired effect of
  ablating it (run-level, paired by run index, with a sign-test or bootstrap interval).
- *Gentle programs* (prediction RE 2): a type is gentle if, as a stranger with its history fills inapplicable, it
  cooperates with a stranger DefectBot (it is suckerable); a *gentle holder* is a gentle type holding at least one
  history fill. *Repeat-encounter rate* of an island: the probability that two independent sampled partners of a
  program share a lineage, Σ_ℓ share(ℓ)², time-averaged over the run.
- Writes, in-place updates, evictions, copies and contracts per encounter; founder establishment (lineages alive at
  the horizon); persistence (island states at 1,000 vs 2,000).

### 1.11 Dropped or not built (with reasons)

- `ROLE`-keyed fills in the PD (§1.3): would import a correlating device into an arm without `ROLE`.
- Fill costs: fills are free in this wing (no runtime price); "costed" in the inert rule has no content here.
- The ε→0 chain (§1.9).
- Concessions' n = 11 boss grammar: replaced by behaviour-keyed fills (§1.2).
- Social organization at (100, 64) and in fission–fusion: cost (§1.9); fission–fusion is spec'd in both wings but its
  social-organization half is not built here.

### 1.12 Hand predictions (before any number)

What I expect the hooks to do, by mechanism:

- **Hooks are mostly constants in disguise.** Under the length prior the four hook leaves carry most of the size-1
  mass, so most hook-carrying founders are bare `HOOK(t, a0)`; their none/role fills re-randomize them between ALLC
  and D. The inert control dilutes the provers' prior mass several-fold relative to the plain grammar (FairBot's
  size-3 count stays 1 while a(3) grows), so I expect a visible grammar-dilution effect on the per-island chance,
  but at I = 64 the run-level outcome should stay near the baseline's 1.00.
- **Contracts are the strongest new mechanism in the PD.** Two default-defecting hook carriers that meet at (D, D)
  write a mutual C contract keyed on each other's lineage; a lineage that meets itself writes a self-contract and
  becomes a kin clique (cooperates with its own lineage, defects on strangers). That is the wing's analogue of an
  identity clique: no source access, but lineage-keyed history plus inheritance is a tag by descent. I expect
  lineage-closed islands under maximal hooks and a drop in universal-open that the −contract and −history ablations
  remove.
- **Behaviour fills are probes without length cost** and cannot exploit a sound prover (Lemma 0 is untouched); I
  expect them to be the most *applicable* kind but not the most *held* at the horizon: in a converged FairBot-family
  island most held fills will be written history fills (thanks), because writes are continuous and seeded fills are
  diluted by FIFO eviction.
- **Grudges protect suckerable hook carriers** (`HOOK(t, C)` is ALLC until a defector lineage marks it) and take food
  from defectors in the scramble; the effect needs repeated lineages, which on an island arrive with coalescence.
- **Social organization:** worker grudges against zero-wage bosses are strike fills that fire on path whenever the
  boss's lineage recurs, so threats here are tested, not idle; I expect worker strike fills to be *executed* at
  rates far above 10⁻², boss whack fills to be rarely challenged, and the fair share to move little (the zero-wage
  boss is not hurt by a striker it does not pay), with contracts lifting the intermediate wage.

These are qualitative; the numbered predictions with falsifiers are in `predictions/2026-10-18-hooks-w.md`.
