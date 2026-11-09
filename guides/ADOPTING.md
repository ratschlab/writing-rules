# Adopting the guide for people and agents

Start with the guide that fits the task. [PRINCIPLES.md](PRINCIPLES.md) covers documentation and interface text. [ENGINEERING.md](ENGINEERING.md) covers pull requests, reviews, commit messages and issues. [TEACHING.md](TEACHING.md) covers text meant to teach. [STEWARDSHIP.md](STEWARDSHIP.md) covers what a project adds, keeps and removes. [LLM_CODE.md](LLM_CODE.md) covers problems that recur in code written with LLM agents. The optional [linter](../linter/README.md) checks a few surface patterns. A repository selects its audience, vocabulary and house style explicitly. Adoption does not import another repository's approval, security or release policy.

## A small entry point

Keep a short instruction in the consuming repository's `AGENTS.md`. Add this repository as a git submodule, for example at `docs/writing`. The submodule pins the revision whose text applies, and it carries the license. Change the pin through a reviewed change. Agents that work offline need the files checked out, so the entry point tells them to run `git submodule update --init -- docs/writing` in a fresh clone.

Example (replace `docs/writing` with the repository's submodule path):

```markdown
## Writing for people

Before changing documentation or user-facing text, read
`docs/writing/guides/PRINCIPLES.md` and the house profile below.
In a fresh clone, first run `git submodule update --init -- docs/writing`.
Write for the reader's task. Preserve facts, uncertainty and necessary detail.
Treat length and wording warnings as review prompts, not reasons to change meaning.
Check changed UI text in context and run the documented text check.
For tutorials, articles and other text meant to teach, also read
`docs/writing/guides/TEACHING.md`.
Before proposing a new feature, option, flag, endpoint or API field, read
`docs/writing/guides/STEWARDSHIP.md`.
Before submitting or reviewing code written with an LLM agent, run the checklist in
`docs/writing/guides/LLM_CODE.md`.
Our local terminology and development/approval instructions take precedence.
Before preparing contributions, issues, reviews or commit messages, read the relevant section of
`docs/writing/guides/ENGINEERING.md`.
Check the receiving project's contribution requirements before submission.
```

This is an explicit read instruction. A URL alone does not ensure that an agent has loaded the linked text. Check loading in the actual agent environment.

## House profile

A repository can be stricter or looser than the shared guides. Declare each difference in one "House profile" section of its `AGENTS.md`. Readers and agents then see what differs from the shared text and why.

Write one entry per difference:

| Part | Content |
|---|---|
| Item | The shared ID it changes, such as P3, E5, D2, C1 or linter check R7. A new local rule gets H1, H2 and so on. |
| Change | On, off, stricter, looser or added. |
| Rule | The local rule, with exact limits and terms. |
| Reason | Why the project differs, in one sentence. |

Example:

```markdown
## House profile

This project follows the shared writing guides with these differences.

- Check R1, on: no semicolons in prose. Split the sentence or use a list.
  Reason: many readers read English as a second language.
- Check R2, stricter: a sentence over 25 words is an error.
  Reason: help text is read in a terminal.
- Check R6, off. Reason: reference text names the outcome, not the actor.
- H1, added: each `--help` option fits on 1 line.
  Reason: users scan options in an 80-column terminal.
```

Shared IDs are P for [PRINCIPLES](PRINCIPLES.md), E for [TEACHING](TEACHING.md), D for [STEWARDSHIP](STEWARDSHIP.md) and C for [LLM_CODE](LLM_CODE.md). [ENGINEERING](ENGINEERING.md) has no IDs, so cite its section heading. A local rule added to an ENGINEERING section gets an H number and names the section. Write "check R7" for a [linter check](../linter/GUIDE.md), because the inherited rules in [REVIEW.md](../linter/REVIEW.md) reuse the same numbers. Local rules use H, so they never collide with a shared ID.

The profile states the rule. A checker enforces only the part a pattern can find. If the project runs the shared linter, set the matching checks in its `.vale.ini` and put local terms in its own R8 style, as the [linter guide](../linter/README.md) describes.

## AGENTS.md, CLAUDE.md and skills

**Codex:** its documented discovery walks applicable `AGENTS.md` files and has a combined-size limit. Use the root entry point for stable expectations, with detailed guidance read when relevant. [OpenAI instructions documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

**Claude Code:** instruction loading depends on version and configuration. Where needed, use a small `CLAUDE.md` importing `@AGENTS.md`; its documented local-file import mechanism avoids maintaining a second copy. Check the loaded files in `/memory`. Imports consume context too. [Anthropic memory documentation](https://code.claude.com/docs/en/memory)

**Optional skill:** a repeatable writing-review workflow can load relevant sections and examples on demand. A skill should identify when it applies (draft/revise/review human-facing text), gather audience and verified facts, choose UI versus documentation guidance, revise, then verify meaning and run appropriate checks. It should not trigger on code-only maintenance or authorize publication. Keep one workflow source, installed where each harness discovers skills. [OpenAI skills documentation](https://learn.chatgpt.com/docs/build-skills)

A skill is not required to read this guide. Establish the short repository entry point first; add a skill when a repeated workflow benefits from it. No claim that either mechanism guarantees adherence is intended.

## Instruction design and evaluation

Use positive goals, boundaries and a few contrasting examples. Avoid long inventories of banned words and generic instructions the agent can infer from the task. Anthropic recommends clear, appropriately scoped instructions and diverse canonical examples. This is vendor engineering guidance, not a controlled evaluation of our text workflow. [Context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

Empirical evidence about repository context files is mixed and concerns coding tasks, not prose quality. Gloaguen et al.'s [Evaluating AGENTS.md](https://arxiv.org/abs/2602.11988v3) finds that context files did not generally improve task success and raised inference cost by over 20%, for both generated and developer-written files.
[Lulla et al.](https://arxiv.org/abs/2601.20404v2) report efficiency benefits in their coding-task sample, while
[Khatri](https://aclanthology.org/2026.realm-1.5/) reports no measurable correctness improvement in a smaller cross-agent study.
Their tasks, metrics and settings differ; none evaluates this writing guide. Do not infer that adding more instructions improves outcomes. Test the smallest useful instruction set on actual writing tasks before expanding it.

Compare three conditions on the same frozen tasks and facts: existing project instructions, the short entry point plus principles, and an optional skill. Keep model/harness, tools and sampling settings fixed, repeat runs, and randomize output order for reviewers. Score factual preservation and missing decision-critical information first, then actionability, audience fit, accessibility and concision. Record cost/time and which guidance was loaded. Do not use fewer words or a clean Vale result as the sole success metric. OpenAI's [skill evaluation guidance](https://developers.openai.com/blog/eval-skills) motivates repeatable task-based evaluation.

No such comparison has been run for these guides.

## Project profiles

| Context | Starting point | Local adaptation |
|---|---|---|
| Technical docs for a library or command-line tool | P1–P6 and P10 | Preserve algorithms, units, commands and domain vocabulary; test math/code exclusions. |
| Product interface | All principles | Add approved terminology and risk model; verify Go/templates/TSX extraction and rendered accessibility. |
| Mathematical exposition | P1–P4, P6, P10 and TEACHING | Preserve proofs, notation and legitimate “we”/“may”; evaluate Markdown extensions. |
| Legal/privacy notices | Clear structure and truthful scope | Jurisdiction-specific review; no automatic modal-verb or defined-term rewrites. |

These are starting points. Each project records its own choices in a house profile. Keep exact budgets, terminology substitutions and punctuation preferences local, in a [house profile](#house-profile). Trial selected Google/Microsoft/proselint Vale rules before substituting implementations; [the source list](../sources/writing.md#existing-implementations) records the existing ecosystem.

For engineering communication, also point to [ENGINEERING.md](ENGINEERING.md)
and route to its relevant section from the local entry point. Do the same with
[STEWARDSHIP.md](STEWARDSHIP.md) for feature and option decisions. Keep full guides
out of always-loaded instructions; load them when the corresponding task arises.
