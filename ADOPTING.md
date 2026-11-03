# Adopting the guide for people and agents

Start with [PRINCIPLES.md](PRINCIPLES.md). It is the human-readable source of guidance. [GUIDE.md](GUIDE.md) describes the lint contract, and [REVIEW.md](REVIEW.md) explains changes to inherited rules. A repository selects its audience, vocabulary and house style explicitly. Adoption does not import another repository's approval, security or release policy.

## A small entry point

Keep a short instruction in the consuming repository's `AGENTS.md`. Pin the shared revision and make the guide available locally for offline work. A tracked snapshot of a few guidance files is simpler than requiring a submodule or assuming every agent can browse. Keep the license with that snapshot. Update it and the tool pin together through a reviewed change.

Example (replace the path with the repository's actual snapshot):

```markdown
## Writing for people

Before changing documentation or user-facing text, read
`docs/writing/PRINCIPLES.md` and the applicable local vocabulary below.
Write for the reader's task. Preserve facts, uncertainty and necessary detail.
Treat length and wording warnings as review prompts, not reasons to change meaning.
Check changed UI text in context and run the documented text check.
Our local terminology and development/approval instructions take precedence.
Before preparing contributions, issues, reviews or commit messages, read the relevant section of
`docs/writing/ENGINEERING.md`.
Check the receiving project's contribution requirements before submission.
```

This is an explicit read instruction. A URL alone does not ensure that an agent has loaded the linked text. Include a source revision and paths in the snapshot record, and check loading in the actual agent environment.

## AGENTS.md, CLAUDE.md and skills

**Codex:** its documented discovery walks applicable `AGENTS.md` files and has a combined-size limit. Use the root entry point for stable expectations, with detailed guidance read when relevant. [OpenAI instructions documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

**Claude Code:** instruction loading depends on version and configuration. Where needed, use a small `CLAUDE.md` importing `@AGENTS.md`; its documented local-file import mechanism avoids maintaining a second copy. Check the loaded files in `/memory`. Imports consume context too. [Anthropic memory documentation](https://code.claude.com/docs/en/memory)

**Optional skill:** a repeatable writing-review workflow can load relevant sections and examples on demand. A skill should identify when it applies (draft/revise/review human-facing text), gather audience and verified facts, choose UI versus documentation guidance, revise, then verify meaning and run appropriate checks. It should not trigger on code-only maintenance or authorize publication. Keep one workflow source, installed where each harness discovers skills. [OpenAI skills documentation](https://learn.chatgpt.com/docs/build-skills)

A skill is not required to read this guide. Establish the short repository entry point first; add a skill when a repeated workflow benefits from it. No claim that either mechanism guarantees adherence is intended.

## Instruction design and evaluation

Use positive goals, boundaries and a few contrasting examples. Avoid long inventories of banned words and generic instructions the agent can infer from the task. Anthropic recommends clear, appropriately scoped instructions and diverse canonical examples. This is vendor engineering guidance, not a controlled evaluation of our text workflow. [Context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

Empirical evidence about repository context files is mixed and concerns coding tasks, not prose quality. Gloaguen et al.'s [Evaluating AGENTS.md](https://arxiv.org/abs/2602.11988) finds costs and benefits differ between generated and human instructions.
[Lulla et al.](https://arxiv.org/abs/2601.20404v2) report efficiency benefits in their coding-task sample, while
[Khatri](https://aclanthology.org/2026.realm-1.5/) reports no measurable correctness improvement in a smaller cross-agent study.
Their tasks, metrics and settings differ; none evaluates this writing guide. Do not infer that adding more instructions improves outcomes. Test the smallest useful instruction set on actual writing tasks before expanding it.

Compare three conditions on the same frozen tasks and facts: existing project instructions, the short entry point plus principles, and an optional skill. Keep model/harness, tools and sampling settings fixed, repeat runs, and randomize output order for reviewers. Score factual preservation and missing decision-critical information first, then actionability, audience fit, accessibility and concision. Record cost/time and which guidance was loaded. Do not use fewer words or a clean Vale result as the sole success metric. OpenAI's [skill evaluation guidance](https://developers.openai.com/blog/eval-skills) motivates repeatable task-based evaluation.

The [evaluation cases](evals/writing.json) are a proposed rubric, not measured agent results. A model comparison has not been run for this revision.

## Project profiles

| Context | Starting point | Local adaptation |
|---|---|---|
| Technical docs / MetaGraph / apxchol | P1–P6 and P10 | Preserve algorithms, units, commands and domain vocabulary; test math/code exclusions. |
| UI / Keylee | All principles | Add approved terminology and risk model; verify Go/templates/TSX extraction and rendered accessibility. |
| Mathematical exposition / cp-algorithms | P1–P4, P6, P10 | Preserve proofs, notation and legitimate “we”/“may”; evaluate Markdown extensions. |
| Legal/privacy notices | Clear structure and truthful scope | Jurisdiction-specific review; no automatic modal-verb or defined-term rewrites. |

These are proposed starting points, not adopted policies for those projects. Keep exact budgets, terminology substitutions and punctuation preferences local. Trial selected Google/Microsoft/proselint Vale rules before substituting implementations; [SOURCES.md](SOURCES.md#existing-implementations) records the existing ecosystem.

For engineering communication, also snapshot [ENGINEERING.md](ENGINEERING.md)
and route to its relevant section from the local entry point. Keep full guides
out of always-loaded instructions; load them when the corresponding task arises.
