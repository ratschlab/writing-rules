# Shared writing guides

These guides help people and agents write documentation, interface text, engineering messages and teaching material. A further guide covers what a project adds, keeps and removes. Each principle names its sources and the kind of evidence behind it.

## Guides

| Guide | Use it for | IDs |
|---|---|---|
| [PRINCIPLES](guides/PRINCIPLES.md) | Documentation and interface text that helps people act | P1–P10 |
| [ENGINEERING](guides/ENGINEERING.md) | Agent replies, pull requests, reviews, commit messages, issues and release notes | By section |
| [TEACHING](guides/TEACHING.md) | Algorithm articles, tutorials and other text meant to teach | E1–E13 |
| [STEWARDSHIP](guides/STEWARDSHIP.md) | Deciding whether a project adds, keeps or removes a feature, option or API field | D1–D9 |
| [LLM_CODE](guides/LLM_CODE.md) | Writing and reviewing code, tests and pull requests produced with LLM agents | C1–C10 |
| [ADOPTING](guides/ADOPTING.md) | Pointing a repository's people and agents to these guides | |

Pin a revision as a git submodule when you adopt the guides. [ADOPTING](guides/ADOPTING.md) shows a short entry point for `AGENTS.md`. It also shows how to record where a project differs from the guides.

## How evidence is graded

Each principle states its basis with one or more of these labels:

- **Research:** empirical studies and reviews of them, such as experiments, field studies and meta-analyses.
- **Standard:** a normative standard or specification, such as WCAG or Semantic Versioning.
- **Practice:** maintained guidance from a style guide, vendor or project.
- **Opinion:** the argued view of a named expert, without new data.
- **House judgment:** our own choice where the sources do not decide. Variants such as house guidance, house workflow and house practice mean the same.

A cited source supports the stated principle. It does not support every way to apply it. [Sources and limits](sources/README.md) explains how sources are selected. It also lists the sources by guide. Source IDs S1–S165 are stable.

## Linter

The [linter](linter/README.md) is an optional helper. It runs Vale with a shared style package and checks a few surface patterns, such as vague error phrases and project terminology. Each project chooses which checks to enable. The linter cannot check the principles in the guides. They need a reader's judgment.

`ratschlab/metagraph` runs the linter in CI, and `AlgOptGroup/apxchol` runs it as a local check. Other projects pin the guides without it.

## License and authorship

MIT License. Copyright (c) 2026 ETH Zurich. See [LICENSE](LICENSE).
Created by Oleksandr Kulkov with assistance from Claude and Codex.
External tools and dependencies retain their own licenses.
