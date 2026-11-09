# Mechanical checks and house styles

Read [PRINCIPLES.md](../guides/PRINCIPLES.md) for citation-based guidance and
[REVIEW.md](REVIEW.md) for the reassessment of the inherited rules.
Projects select the applicable mechanical checks and keep domain vocabulary locally.
These rules guide prose, user-facing messages, PR descriptions and reviews.
The linter only checks files selected by the consumer. It does not automatically
lint GitHub discussions or certify factual correctness.

Write one idea per sentence. Put the result or action first. Use direct language
and name the actor when that helps. Keep terms consistent and explain unfamiliar
internal names. Errors should explain the failure and give a useful next step.
Numbers, defaults and promises must agree with the implementation.

## Mechanical checks

| Rule | Check | Default level |
|---|---|---|
| R1 | Semicolons in prose | Disabled, project opt-in |
| R2 | Sentences longer than 30 words | Suggestion |
| R4 | Vague failure/apology phrases | Disabled, project opt-in |
| R5 | Snake-case jargon in prose | Disabled, project opt-in |
| R6 | Passive-voice heuristic | Suggestion |
| R7 | Vague timing/modal terms and selected written numbers before units | Disabled, project opt-in |
| R8 | Project terminology | Supplied by each project |
| R9 | Unnamed first-person plural | Disabled, project opt-in |

These are linter check IDs. Vale reports them as `Writing.R1` to `Writing.R9`.
They reuse the numbers of the inherited rules in [REVIEW.md](REVIEW.md).
The guides use P, E, D, C and S IDs instead.

R7's terms are `may`, `might`, `soon`, `shortly`, `a while` and `eventually`.
Its number list is two through ten, twelve, twenty, thirty and sixty.
Units are second, minute, hour, day, week, month, thread, file, step and result,
including plurals, plus times, GB, MB and TB. Number/unit matching ignores case.
This is a lexical check; it cannot distinguish permission from uncertainty.
Use a documented exception or a project-specific rule where that distinction matters.

## Manual review

Reviewers assess whether sentences have one idea, whether the outcome comes
first, and whether explanations help the intended reader. They verify facts,
units, defaults, compatibility promises and error recovery advice against code.
They also judge headings, paragraph length, link wording, unnecessary detail,
and when passive voice is appropriate. These judgments cannot be certified by
passing a regular-expression check.

Repository development instructions, approval requirements, performance gates
and release procedures stay in that repository's AGENTS.md. Adopting a writing
package does not adopt another project's development policy.
