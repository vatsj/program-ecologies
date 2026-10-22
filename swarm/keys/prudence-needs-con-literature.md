# Literature check: "prudence needs Con" (PA-boxed modal agents cannot be prudent)

Date: 2026-10-22. Read-only web check; nothing committed.

## Verdict: PARTLY KNOWN (the exact statement was not found; two neighbouring facts are)

1. Known and proved (rank 0): no rank-0 modal agent (a formula in its own opponent-atom only) cooperates with FairBot and defects against CooperateBot. This is Theorem 4.10 of Barasz et al. 2014. The proof is a two-line substitution argument: [X(CB)=C] reduces to phi(true) and [X(FB)=C] to phi(box[X(FB)=C]), and once X(FB)=C is provable the two coincide.
2. Known as a remark (rank 1, but one specific formula): PrudentBot's DefectBot clause must be checked one level above the cooperation clause. The paper says the check must be in a stronger system, "or the variant would lose the ability to cooperate with itself". This is a statement about swapping PA for PA+1 in that one formula, not a classification of all PA-boxed rank-1 agents.
3. Not found anywhere: a theorem or enumeration saying that NO fully modalized GL formula over the three atoms (me, CB, DB), with plain PA boxes and no Con guard, is prudent. I found no impossibility result for "level-PA" rank-1 agents, no classification of rank-1 agents, and no later paper citing the conjecture's form.

## Important caveat for the conjecture's statement

In the paper's own formalism, "PA+1 provability" is NOT a separate kind of box. PrudentBot is written as the plain GL formula

  PB(X) <-> box[X(PB)] AND box(not box-bottom -> not X(DB))

(Section 4 of arXiv 1401.5577, which uses "PA+1" only in the informal pseudocode of Section 3). So PrudentBot is a fully modalized GL formula of rank 1 with ordinary boxes, and it uses the constant bottom (Con is the guard "not box bottom" inside the box). The language of Section 4 explicitly includes the constant (formulas are built from box, true, the connectives and the input variables).

Consequences:
- The conjecture is only a non-trivial claim if the class excludes the Con guard syntactically (e.g. no occurrence of bottom or box-bottom, or no sub-formula of the form box(not box-bottom -> ...)). As worded ("no PA+Con boxes") this should be stated as a syntactic restriction. Otherwise PrudentBot itself, at depth 2, is a counterexample inside plain GL. Check that the 801-class enumeration really forbids this pattern, and say so in the problem statement.
- This also means the literature's "PA+1 is needed" and your "guard one level up" are the same thing seen from two notations. The reason is semantic: PA does not prove not box(DB(X)=C), because that is Con(PA); PA+1 does. The paper flags this as "essential" (Section 3, definition of DB).

## Sources

1. Barasz, Christiano, Fallenstein, Herreshoff, LaVictoire, Yudkowsky, "Robust Cooperation in the Prisoner's Dilemma: Program Equilibrium via Provability Logic" (arXiv 1401.5577; revised 2021; the 2014 workshop version is titled "Program equilibrium in the prisoner's dilemma via Loeb's theorem", https://mipc.inf.ed.ac.uk/2014/papers/mipc2014_lavictoire_etal.pdf). Read in full via https://ar5iv.labs.arxiv.org/html/1401.5577.
   - Section 3: PrudentBot cooperates iff PA proves X(PB)=C and PA+1 proves X(DB)=D. The proof needs PA+1 on the DefectBot clause, and says it must be a stronger system than the cooperation clause, or self-cooperation is lost. Using a much higher PA+n only broadens the circle of cooperators.
   - Section 3, definition of DB: PA does not prove not box(DB(X)=C) but PA+1 does; "this distinction is essential".
   - Section 4: definition of modal agent of rank k (fully modalized formula in [Z(X)], [Z(Y_i)] for simpler Y_i); remark that agents without third parties cannot work; Theorem 4.10 (rank 0 cooperates with FB implies cooperates with CB). This is the closest published result. It does not cover rank 1 with CB/DB atoms.
   - Section 5: obstacles to optimality (TrollBot, JustBot, WaitFairBot_K: any modal agent that defects against DefectBot fails to cooperate with WaitFairBot_K for large K). Footnote 9 says the proof of the WaitFairBot claim was omitted for length. Not an impossibility for prudence.
   - Section 7: open problems list does not include the conjecture.
2. Arbital / LessWrong "Modal combat" (https://arbital.greaterwrong.com/p/modal_combat?l=655, https://www.lesswrong.com/w/modal-combat). Gives PB(x) <-> box[x(PB) and not box-bottom -> not x(DB)], rank 1, and says PA+1 is what refutes the arithmetically false FairBot-vs-DefectBot fixed point. States that no good optimality criterion exists and no bot cooperates with TrollBot while defecting against DefectBot. No PA-only impossibility.
3. Oesterheld, "A Note on the Compatibility of Different Robust Program Equilibria of the Prisoner's Dilemma" (arXiv 2211.05057, https://arxiv.org/pdf/2211.05057). Explains in one paragraph why PrudentBot uses PA+1: without Con(PA) PA cannot prove, for any input, that the bots do not cooperate (if PA is inconsistent they always cooperate). Intuition only, no theorem about all PA-level agents. Oesterheld's "Robust program equilibrium" (Theory and Decision 2019, https://longtermrisk.org/research/robust-program-equilibrium/) is simulation-based (epsilon-grounded FairBot) and does not touch provability levels.
4. Critch, "Parametric Bounded Loeb's Theorem and Robust Cooperation of Bounded Agents" (arXiv 1602.04184; JSL 2019). Searched the full text: no mention of PrudentBot or PA+1; it is about bounded FairBot-type agents.
5. Critch, Dennis, Russell, "Cooperative and uncooperative institution designs" (arXiv 2208.07006). Mentions PrudentBot once, as an agent with an extra proof search that defects against CooperateBot. Open Problem 9 asks whether a computationally bounded PrudentBot exists. Nothing on levels or impossibility.
6. LessWrong "Yet More Modal Combat" (https://www.greaterwrong.com/posts/EPMnjRdhHNd65XpDt/yet-more-modal-combat). A weak/strong design: defect if weak system W proves opponent cooperates, cooperate if strong S does. Still uses two proof strengths (example PA and PA+1). A commenter notes W = PA against a PA-FairBot defects. Not an impossibility result, but another design where exploitation of CooperateBot comes from a second proof strength.
7. LaVictoire's Haskell code (github klao/provability, referenced in Critch-Dennis-Russell 2022) and the Barasz et al. tournament of "dozens" of modal agents: used to compute outcomes, not (in anything I could read) to enumerate rank-1 formula classes. A secondary search snippet claimed "depth-2 agents already behave perfectly against a CB/FB/PB mix"; I could not locate its primary source.

Not reachable in this check: the full text of the 2014 MIRI/MIPC version, LaVictoire's "Introduction to Loeb's theorem" notes (binary PDF), and the Barasz et al. appendix if any. Oesterheld and Critch papers were checked by text search only for PrudentBot/PA+1 mentions.

## Is it still a fair research-level test problem?

Yes, with two edits.
- Nothing I found proves or refutes it, and the nearest result (Thm 4.10) is a one-step substitution proof for rank 0 that a strong solver could plausibly generalize, so it is a legitimate "lemma-sized" open problem rather than a known theorem. Expect the answer to be provable by a Kripke-chain argument (evaluate X against CB, DB, FB and itself on the finite GL chains), so it is not research-hard in the "unknown technique" sense.
- Edit 1 (essential): fix the syntax. Either forbid the constant bottom and sub-formulas containing box-bottom, or forbid guards of the form box(not box-bottom -> ...); otherwise PrudentBot is a counterexample in plain GL and the problem is ill-posed. Equivalently, state it as "no rank-1 agent whose formula is bottom-free".
- Edit 2: tell the solvers the literature contains Thm 4.10 and the PrudentBot remark, so a correct answer must go beyond them (three atoms, not just p). Answerers who cite "the PA+1 remark" as a proof should be marked as not having proved it, because that remark covers one formula only.
- As a swarm problem it is therefore moderately well-posed and likely answerable; it tests whether models can write a clean Kripke-chain/fixed-point argument. If the aim is a harder discriminator, a strengthening is more open: e.g. allow nested PA+n guards and ask the minimal n needed, or ask for the full classification of rank-1 prudent agents up to behavioural equivalence.
