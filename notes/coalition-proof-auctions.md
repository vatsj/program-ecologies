# Coalition-proof auctions from the leader-value notion (RE, 2026-10-21)

A swing at the RS's side quest (DEFERRED 14), in the RS's three lines: VCG is not coalition-proof; our equilibria
encode social choice; so they might suggest a refinement of VCG, ideally a single side-payment rule, that buys
coalitional robustness. Short answer: **yes for coalitions that can recontract with the seller, no for bidding rings,
and the program setting changes which of the two is the binding case.** The rule the RS hoped for exists, is derived
below from the RS's notion, and is already deployed (core-selecting payments in spectrum auctions). Its limits are
known theorems. What is new is (§5–6) the response structure: in an open-source auction the RS's "the complement
gets to respond" is literal, and ring enforcement and collusion policing turn out to be the same program shape.

Setting: a seller 0 owns items M; bidders i = 1..n have quasilinear values v_i over packages; TU. Welfare of a
coalition: w(S) = max welfare from allocating M within S∖{0} if 0 ∈ S, else 0. VCG pays bidder i its **individual
marginal contribution** u_i^V = w(N) − w(N∖i).

## 1. The bridge: the notion in the auction economy is the core

With the seller as a player who owns the items and bidders who own money, the auction is an allocation game in the
RS's sense (notes/leader-value-core.md, "Allocation games"): every player chooses who gets its goods, an outsider's
only credible response is to keep its own, and the leader-value core is the classical core. In TU, an outcome with
bidder payoffs u and revenue π_0 = w(N) − Σu is in the core iff for every set S of bidders

  Σ_{i∈S} u_i ≤ w(N) − w(N∖S),

the coalition {0} ∪ (N∖S) not blocking. **Reading: no group of bidders is paid more than its joint marginal
contribution.** The RS's grand-coalition clause gives efficiency as before.

## 2. The side-payment rule

VCG pays every bidder its individual marginal contribution, and a group's individual contributions can sum to more
than its joint contribution (complements: two item bidders who jointly displace a package bidder each "contribute"
the whole gap). The minimal repair is a **surcharge** on winners, the smallest that brings every group's payment
down to its joint contribution:

  p = p^V + δ, δ ≥ 0 minimal (in total) such that Σ_{i∈S} (u_i^V − δ_i) ≤ w(N) − w(N∖S) for all S,

with ties among minimal δ broken by distance to VCG. This is the **minimum-revenue core, VCG-nearest point**: the
quadratic rule of Day–Cramton (2012), with Erdil–Klemperer's (2010) reference rules as the alternative tie-breaks;
Day–Milgrom (2008) and Ausubel–Milgrom (2002) for core-selecting and proxy auctions. The surcharge is zero iff
Σ_{i∈S} u_i^V ≤ w(N) − w(N∖S) for every S (bidders are substitutes; gross-substitutes valuations suffice), and then
the rule *is* VCG. So the RS's hope comes true: one surcharge rule on top of VCG, derived from the notion as the
statement "pay groups no more than their joint marginal contribution."

**What it buys.** The pathologies that are blocking-by-the-seller go away. The canonical case
(Ausubel–Milgrom 2006, "The lovely but lonely Vickrey auction"): bidder 1 values AB at 2, bidders 2 and 3 value A
and B at 0.5. Under VCG, 1 wins and pays 1. If 2 and 3 jointly overbid to 2 each, they win and VCG charges each 0;
each nets 0.5 and bidder 1 loses its 1. Under the surcharge they must pay together at least bidder 1's reported 2,
so the collusion nets −0.5 each. The same arithmetic removes the two-shill version, in which one bidder splits into
fake A and B bidders, and VCG's revenue non-monotonicity. (Numbers checked by script; shill immunity is stated in
general in the core-selecting literature, which the run should verify rather than cite.)

**What it costs.** Individual truthfulness, whenever the surcharge is positive. Winners free-ride on each other's
surcharge (the threshold problem): with values 2 / 1.5 / 1.5 the VCG-nearest payments are 1 and 1; bidder 2
shading to 1.2 moves them to 0.85 and 1.15, a gain of 0.15 taken from bidder 3. Day–Milgrom: a core-selecting rule
is dominant-strategy truthful iff VCG is in the core, and incentives to deviate are minimized at bidder-optimal core
points. Goeree–Lien (2016): with incomplete information, if VCG is not in the core no auction has core outcomes in
equilibrium. **In the RS's terms: the surcharge makes groups robust and singletons fragile; VCG is the reverse.**
In the AM family VCG is fragile to the item pair whether its members lose or win at truth: bidding at least v_P each
zeroes both VCG prices. With values 2 / 1.5 / 1.5 the winners pay 0.5 each, and after overbidding to 2 they pay 0.
The pair profits exactly when v_P > min(v_A, v_B), which holds on 0/1,000 mismatches on the integer grid. (Corrected
after gpt-6.1-sol's review: the first draft said VCG was robust to the winners' coalition, which holds for joint
shading but not for joint overbidding.) The surcharge rule removes both overbids and opens the singleton shade.

## 3. Coalition-proof equilibria already land here

Bernheim–Whinston (1986, menu auctions): under complete information, in the first-price package auction the
coalition-proof Nash equilibria (Bernheim–Peleg–Whinston 1987) coincide in payoffs with truthful equilibria and
give the **bidder-optimal frontier of the core**. So the BPW notion applied to the *reporting game* of the
first-price package auction selects the same set the RS's notion gives on the *outcome game*. The VCG-nearest
minimum-revenue core point is one selection from that frontier, made direct. That is two independent routes to the
same rule, which is evidence the rule is the right "coalitional VCG."

## 4. The wall: rings

A **ring** is a coalition that includes the competition and *underbids* (Graham–Marshall 1987; McAfee–McMillan
1992). Nothing in §2 stops it, and nothing can:

*Proposition (two-bidder ring).* For one item and two bidders with values in [0, V], no Groves mechanism, hence by
Holmström no efficient dominant-strategy mechanism on a convex domain, makes truthful reporting optimal for the
coalition {1, 2} with side payments. *Proof.* Groves payments are p_i = b_j·x_i − h_i(b_j). When 1 wins, the ring
gets v_1 − b_2 + h_1(b_2) + h_2(b_1); truth must maximize this over b_2 < b_1 and over b_1 > b_2 for all v_1 > v_2,
so h_1(b) − b and h_2 are constant on [0, V). When 2 wins, symmetrically h_2(b) − b and h_1 are constant on
(0, V]. Then h_1 is both constant and constant-plus-identity on (0, V), a contradiction. ∎

The literature has the general forms: Schummer (2000), where bribe-proof rules are constant on rich domains;
Goldberg–Hartline (2005), where truthful, collusion-proof mechanisms are posted prices, with efficiency loss
unbounded. **In the RS's notion this is the grand-coalition clause turned against the seller:** if the seller is a
fixed mechanism rather than a player, the bidders' grand coalition can always report its way to the efficient
allocation at the reserve, so the notion's equilibria have revenue equal to the reserve for every mechanism. The
notion bites only when the seller is a *player who responds*. Under complete information the responding seller
restores the core (§1). Strong-equilibrium implementation of core-like correspondences is classical:
Kalai–Postlewaite–Roberts (1979), and Moulin–Peleg (1982), who characterize strong-implementable choice through
cores of effectivity functions. Under incomplete information the seller's value-blind response is a reserve price,
which costs efficiency.

**The trilemma.** Among efficiency, dominant-strategy truthfulness and robustness to rings, pick two. VCG keeps the
first two. Posted prices keep the last two. The surcharge rule gives up the second to buy robustness against every
coalition that can recontract with the seller, but not against rings. The RS's hope, "as simple as a side-payment
rule," holds exactly up to that line.

## 5. The tie rule decides the RS's notion on reporting games

Apply the notion to the *reporting game* (seller fixed, bidders as players, complete information), the complement
responding by best reply. Both failures of §2 come with a responder who is **indifferent**, and who can punish:

- *VCG, losers' collusion* (values 2 / 0.5 / 0.5; 2 and 3 overbid to 2): bidder 1 now loses whatever it bids below
  4, so raising its AB bid to 3.9 is a best reply. It sets the colluders' VCG prices to 1.9 each, netting −1.4 each.
  The winners' overbid (2 / 1.5 / 1.5 → bids 2, 2) is deterred the same way: −0.4 each after the spite.
- *Surcharge rule, shading* (2 / 1.5 / 1.5; 2 shades to 1.2): loser 1 raising to 2.6 is again a best reply. It
  takes bidder 2 to 0.35, below its truthful 0.5. (It also hurts bidder 3, so it is a best reply for the singleton
  1, not for the complement {1, 3} jointly: who responds, singly or as a coalition, matters too.)

So under the **weak** reading (any best reply may respond, the spiteful one included) both rules' truthful
profiles survive these deviations. Under the **strict** reading (an indifferent responder plays its default) both
fail as in §2. This is the repo's old lesson in auction form: untested threats deter (RESULTS "Incentive-compatible
enforcement", "The gene arm"), and whether a costless threat counts is a modeling decision, not a theorem. In a
sealed-bid auction no response is possible, so the strict reading is the physical one. Spiteful bidding has its own
literature (Morgan–Steiglitz–Reis 2003; Brandt–Sandholm–Shoham 2007). Under incomplete information spite is risky,
since the spiter may win at a loss.

## 6. Open-source auctions: rings and police are the same program

If bids are **programs that read each other's source** (the repo's setting), responses become literal. Bidder 1's
program can say "if 2 and 3 provably overbid, bid 3.9" and so make the RS's weak reading physical: the threat costs
nothing when carried out and protects bidder 1's own surplus beforehand (deterrence, FairBot-shaped). The same
expressiveness enforces rings, which in a sealed-bid one-shot auction are not self-enforcing (each member wants to
outbid the agreed low bid). Two observations:

1. **Ring enforcement and collusion policing have the same shape:** a default bid, raised when a deviation is
   detected. The ring's default is low and "deviation" means outbidding; the police's default is truthful and
   "deviation" means colluding. No syntactic test (such as "reading may only raise my bid") separates them, because
   both punish by raising. They differ only in the reference profile they protect, so which one holds an island is
   a selection question: the ecology's question, not the mechanism's.
2. **A source-reading seller sees enforcement.** A one-shot ring must condition bids on the partners' sources. A
   mechanism can therefore treat bids that read other bidders as a separate class: posted prices for that class,
   the surcharge rule for the rest. This is Kudva–Dowling–Aswani's (2025, arXiv 2511.12456) VCG/posted-price split
   with a classifier that has no false negatives on enforced rings. But by observation 1 it also removes the police,
   and false positives are exactly what that paper finds costly. Rings enforced outside the mechanism (repeated
   play, side contracts) remain.

**Conjecture (to be tested).** Among bidder programs, rings are selected the way the PD's provers are: the ring
raises every member's payoff, as cooperation does among bidders, and it is cooperation *against* the seller. The
police earn only by deterrence, so they are a neutral shadow wherever no ring is seeded. So without a responding
seller the open-source auction is a ring ecology, and the repo's main positive result (source-reading programs
cooperate) is the seller's cartel problem. The interesting cells: (i) the surcharge rule against VCG, since it
removes the losers' ring and leaves the winners' free-riding; (ii) a seller program that responds by reading
(refusing ring-conditioned bids, or reserve-pricing them), which is the only route the RS's notion leaves open
(§4); (iii) the prudence analogue, where police that exploit rings (bid just enough to win cheaply against an
underbidding ring) earn strictly, as PrudentBot exploits suckers.

## 7. What to compute

- **A (static, cheap).** Small complete-information package auctions (two items; single-minded bidders, an
  Ausubel–Milgrom family with a package bidder and item bidders, plus substitutes and complements families; integer
  grids, exhaustive). For VCG, the VCG-nearest minimum-revenue-core rule and first-price: how often truth survives
  every proper coalition's deviation in the one-round notion, under weak versus strict ties and singleton versus
  coalitional responders; which coalitions break it; the grand-ring revenue; and whether the first-price reporting
  game's notion-outcomes sit on the bidder-optimal core (the Bernheim–Whinston check through the RS's notion).
- **B (ecology).** Fixed-role islands (the Ausubel–Milgrom roles) of bidder programs from a named set (truthful,
  shade, losers' collusion, ring, police, ring-exploiting police) plus the length prior over a small conditional
  grammar, under each payment rule, with and without a source-reading seller rule. Seed lottery at ε = 0; island
  outcomes (ring, police, truthful, mixed), revenue, efficiency.

## 8. The RS's example: 2XL (RS, 2026-10-21)

*RS:* "we both wanna play with 2XL; I get my way because I'm people; you're a clever bastard, so you inflate your
valuation and get paid extra." *Reading (RE):* one indivisible toy, two players, no seller. The rule allocates
efficiently (the higher report wins, "I get my way") and compensates the loser with the loser's own report, i.e.
VCG with the Clarke payment paid to the other player instead of to an auctioneer. Truthfully I (value v_h) win and
pay you v_l. But you can report anything below v_h, still lose, and be paid up to v_h: the clever bastard.

*Why it is the no-seller corner of §4.* With no third party the grand coalition is the two of us, and the RS's
grand-coalition clause rules out burning money, so the notion demands budget balance. Efficiency, budget balance
and dominant-strategy truthfulness cannot coexist (Green–Laffont), and the inflation is that impossibility showing.

*What the notion says about the rule (computed).* Take the reporting game with complete information and a
best-replying follower. If you commit to a report r, I prefer winning and paying r to losing and being paid about r
iff r ≤ v_h/2, so **your leader value is v_h/2**. If I commit to r, you prefer losing and being paid about r to
winning and paying r iff r ≥ v_l/2, so **mine is v_h − v_l/2**. The two sum to v_h + (v_h − v_l)/2 > v_h whenever
the values differ, so the **leader-value core is empty**: the rule is a commitment race, like chicken. The clever
bastard's inflation is the follower's side of that race. The response clause caps it at half my value, because
past that I hand you the toy at your price: divide-and-choose logic. (Grid check, v = (10, 6): leader values 6.9 and
5.0, ticks 0.1; equal values give the 50–50 split, the only nonempty case.)

*The repair is property rights, not a payment rule.* If the toy is owned, "keep" is the owner's credible
response and the game is an allocation game with a nonempty core (§1). If you own it, I buy at a price in
[v_l, v_h]; if I own it, I keep it and you are paid nothing. "Getting paid extra" is then just where the price
falls inside the core, bounded by my value. Under incomplete information, single ownership gives
Myerson–Satterthwaite (no efficient, budget-balanced, individually rational trade), while **equal shared ownership
does allow efficient dissolution** with a budget-balanced, Bayesian incentive-compatible mechanism
(Cramton–Gibbons–Klemperer 1987, "Dissolving a partnership efficiently"). So for 2XL the coalitional notion points
to the endowment, unowned versus owned versus shared, as the design variable, which is the divide-the-dollar
lesson again (notes/leader-value-core.md: unowned surplus creates first-mover conflict).

References: Ausubel–Milgrom 2002 (B.E. J. Theor. Econ.), 2006 (in *Combinatorial Auctions*, MIT Press);
Bernheim–Whinston 1986 (QJE 101); Bernheim–Peleg–Whinston 1987 (JET 42); Day–Milgrom 2008 (IJGT 36);
Day–Cramton 2012 (Oper. Res. 60); Erdil–Klemperer 2010 (JEEA 8); Goeree–Lien 2016 (TE 11); Goldberg–Hartline 2005
(SODA); Graham–Marshall 1987 (JPE); McAfee–McMillan 1992 (AER); Schummer 2000 (JET); Kalai–Postlewaite–Roberts 1979
(JET 20); Moulin–Peleg 1982 (JME 10); Morgan–Steiglitz–Reis 2003 (B.E. J.); Brandt–Sandholm–Shoham 2007 (GEB);
Kudva–Dowling–Aswani 2025 (arXiv 2511.12456);
Green–Laffont 1977 (Econometrica 45); Myerson–Satterthwaite 1983 (JET 29); Cramton–Gibbons–Klemperer 1987 (Econometrica 55).
