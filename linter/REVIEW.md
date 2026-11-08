# Reassessment of the original 28 rules

Scope: all 28 inherited rules, including their later clarifications. This is a generalization review, not adoption or repeal of any project's existing policy. Decisions below cite the new [principles](../guides/PRINCIPLES.md) and their [sources](../sources/README.md). Each row separates the useful intent from thresholds and implementation choices. No historical measurement of a particular product is treated as evidence about other products.

In this file, R1–R28 name the inherited rules. The linter checks in [GUIDE.md](GUIDE.md) reuse the numbers R1–R9 of the rules they came from, and Vale reports them as `Writing.R1` to `Writing.R9`. The guides use other prefixes: P for writing principles, E for teaching, D for stewardship and S for sources.

| ID | Disposition for shared guidance | Reason and replacement |
|---|---|---|
| R1 | Relax; punctuation bans opt-in | Prefer understandable sentences (P3). Microsoft's guidance allows semicolons in some contexts (S5). No general colon or em-dash ban follows. |
| R2 | Advisory | Sentence length can prompt review, but 20/30/40-word budgets are house choices. Preserve technical precision (P1, P3). |
| R3 | Keep intent, remove two-word test | Lead with useful information (P1). A meaningful opening need not fit exactly two words. |
| R4 | Revise | Describe the problem and known recovery (P5). Do not invent a cause; do not hide identifiers needed for diagnosis. |
| R5 | Scope vocabulary locally | Reader expertise determines jargon (P3). Token, scope and API names can be the correct words. |
| R6 | Prefer, not require | Use active voice for responsibility; allow outcome-focused passive voice (P3, S4/S5). |
| R7 | Split | Keep precise known quantities (P4). Remove blanket uncertainty-word bans; digits everywhere are a house style. Privacy-notice wording does not generalize to scientific uncertainty. |
| R8 | Keep consistency, localize terms | Same function should have a consistent name (P6). Approve/authorize and login/sign-in distinctions belong to the product. |
| R9 | Relax | Make the referent clear (P3). First person is useful in team explanations and mathematical exposition. |
| R10 | Keep and strengthen | Preserve truth, uncertainty and units (P4); inspect the source of changing claims. This is a verification practice, not a regex check. |
| R11 | Move out of universal rules | Plain legal language is desirable, but jurisdiction and legal meaning require specialist review. Do not mechanically remove defined terms or modal verbs. |
| R12 | Local UI budgets only | Test actual labels, translation and layout (P9). No reviewed source establishes universal 8-word titles or 4-word buttons. |
| R13 | Keep review, remove mandatory verdict phrase | Use P10. Reporting “pass” cannot certify semantic or accessibility quality; report material findings and limitations. |
| R14 | Replace fixed width | Evaluate rendered prose width (P9). `em` and `ch` both depend on typography; one sampled font measurement is not font-independent. |
| R15 | Correct standards claim | AA text spacing is tolerance of user overrides (S16). AAA visual presentation is separate (S17); selected default spacing is a design choice. |
| R16 | Optional implementation guidance | Wrapping properties are progressive enhancements, not writing principles. Check current browser support when implementing; no blanket six-line rule. |
| R17 | Relax | Use coherent paragraphs and parallel lists (P1/P6). Word/sentence limits are local heuristics, not universal comprehension boundaries. |
| R18 | Relax | Descriptive headings and parallel lists (P6). Questions are valid for question-oriented content; two-line limits depend on viewport and language. |
| R19 | Keep with context | Defer secondary detail, retain decision-critical information (P7). Do not require exactly one Details fold or force all identifiers inside it. |
| R20 | Remove universal viewport/word budget | Preserve task information and validate responsive layout (P9). The 120-word/375×667 proxy was a local estimate, not a general research finding. |
| R21 | Split | Keep essential text accessible and maintainable (P6/P9). A CSS regex cannot establish accessibility; legitimate CLI paths and codes can belong in visible prose. |
| R22 | Keep consistency, scope conventions | Use product terminology and predictable components (P6). Cross-product vocabulary and navigation need not be identical. |
| R23 | Revise | Give controls clear action/purpose (P6). Counts or state can clarify labels; no universal word cap or single-primary-action rule for dashboards. |
| R24 | Product risk policy | Explain consequential actions (P7). Confirmation/undo decisions depend on reversibility and risk; the writing package grants no operational permissions. |
| R25 | Keep contextual empty states | Distinguish empty/filter/error cases (P8). A bare “none” can be correct in a labeled table cell. |
| R26 | Revise | Provide truthful, accessible feedback (P8). Do not fabricate progress/ETAs or announce every update. Component APIs and timing budgets are local. |
| R27 | Retain accessibility objective, fix coverage claim | Apply relevant WCAG criteria with their exceptions (P9). A few contrast/token checks and axe do not establish AA conformance. |
| R28 | Design-system option | Use notices sparingly (S12), place task information where needed (P7). Banner count and width are local conventions. |

Reviewed 28/28. New emphasis: documentation purpose (P2), uncertainty preservation (P4), truthful state distinctions (P8), and verification of rendered behavior (P9). New agent-specific guidance is in [ADOPTING.md](../guides/ADOPTING.md).

## Mechanical migration

R1/R4/R5/R7/R9 remain available for compatibility but are disabled in the shared default. R2/R6 remain suggestions. Project vocabulary is supplied locally as R8. As of 2026-11-08, MetaGraph enables only `Writing.R4` and supplies its own R8 terms. A punctuation detector identifies punctuation; it does not identify bad writing.

## Evidence not carried forward

The original legal-source chain, font metrics, contrast samples, viewport estimates and mutation-test counts are not independently reproduced here and are not used to claim general efficacy. This review checks the rule dispositions against the cited primary guidance, not every historical citation. The full ISO plain-language standard was not inspected; no claim of compliance with it is made. Treat old percentage improvements as results of their original study conditions, not expected gains from this guide.
