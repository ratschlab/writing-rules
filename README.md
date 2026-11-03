# Shared writing rules

Use one Vale style package across projects, with local vocabulary and scope.
The Python runner adds decoded C++/Python diagnostic strings, explained
exceptions and an optional per-file baseline.

This is an experimental package intended for `ratschlab/writing-rules`.
No existing project has adopted this replacement.

## Guidance and adoption

Start with [citation-based principles](PRINCIPLES.md), their
[sources and limitations](SOURCES.md), and [agent integration](ADOPTING.md).
The [28-rule review](REVIEW.md) separates general principles from local choices.
The linter checks selected surface patterns; it does not certify writing quality.

## License and authorship

MIT License. Copyright (c) 2026 ETH Zurich. See [LICENSE](LICENSE).
Created by Oleksandr Kulkov with assistance from Claude and Codex.
External tools and dependencies retain their own licenses.

## Requirements

- Python 3.11 or newer. The prepared candidate is tested on Python 3.12 and 3.14.
- Vale 3.26.0, installed separately from its official release.
- Dependencies in pyproject.toml are pinned, including Tree-sitter 0.25.2.
- Docutils is installed with the runner for reStructuredText support.

Tree-sitter 0.26.0 crashed on the MetaGraph corpus under Python 3.12 and 3.14
during evaluation. The candidate uses 0.25.2. Do not update that pin without
running the source extraction and corpus tests.

## Local use

Install this checkout in an isolated environment:

```sh
python3 -m venv .venv
.venv/bin/pip install .
.venv/bin/writing-rules export-package WritingRules.zip
```

Each consumer installs the Python package and points Vale to the same version
of the style archive. A `.vale.ini` can contain:

```ini
StylesPath = styles
Packages = path/to/WritingRules.zip
```

Run `vale sync --no-global` from the consumer root. A published version should
use a pinned release URL. A local style adds project terms, as demonstrated
by `examples/metagraph/styles/MetaGraph/R8.yml`. Local configuration can turn
rules on or off and set their levels. R1, R4, R5, R7 and R9 are off unless a project enables them.
R2 and R6 remain advisory. Existing consumers must explicitly enable their
house checks when upgrading.

`writing-rules.json` names the tracked files to scan. See the MetaGraph example.
Run from the consumer's environment, where `vale` and `rst2html` are on PATH:

```sh
writing-rules check --report
writing-rules check
writing-rules check --update-baseline
```

`--report` emits findings and exits successfully after a complete scan.
Python parse errors, Vale diagnostics, configuration and missing-file errors still fail. Normal check mode
fails if any file/rule count increases. A decrease passes with a reduction
listed in the JSON output. Update mode never raises the baseline.

The first adoption needs a reviewed baseline generated from report counts.
The CLI does not have a switch that automatically blesses new errors.

## Exceptions

Use an explanation and a term on the same comment line:

```md
<!-- text-rules-allow: R8 kmer the published identifier -->
The identifier is kmer.
```

The comment applies to the same or following source line, only to the named
rule and a finding matching that term. `kmer` does not exempt `kmers`.
Malformed exceptions fail explicitly. Native Vale suppression directives
are rejected by the runner; otherwise they could bypass the reason check.
Raw Vale remains useful for editor suggestions, but the runner is the CI gate.

## Source coverage

C++ extraction uses Tree-sitter. It selects logger error/warning/critical
arguments, stderr output and thrown-call strings. A consumer can opt selected
files into all-string scanning. Adjacent literals, escapes and raw strings are
decoded before linting. Python uses its standard AST for configured calls and
keywords. Source findings point to the message's starting line, not an exact
character span within a concatenated message.

Markdown and RST use Vale's parsers. TS/TSX Views are included as starting
profiles for toast/setError/alert and JSX text. They have fixture coverage,
not full frontend adoption coverage. Projects must choose their user-facing
call sites explicitly. Source parsing does not perform data-flow analysis.
Tree-sitter syntax recovery is reported as a warning for review. The MetaGraph
corpus has five such files, including macro and template constructs. This
recovery warning does not claim that the C++ compiler rejects the source.

## Baseline semantics

Counts are per file and rule. Removing one hit can offset adding another in
the same file, as with the original scanner. Added-line enforcement would be
a different policy. Vale counts each occurrence, so changing from a scanner
that counts one hit per paragraph requires a reviewed migration.

## Tests

```sh
VALE=/path/to/vale python -m unittest discover -s tests -v
```

The suite includes source extraction, exact exception boundaries, suppression
rejection, baseline transitions, package installation, local overrides, and
48 named integration fixtures. Baseline transition cases are retained in the test suite. See GUIDE.md for automatic versus manual review responsibilities.

Prepared with Codex. This draft has not received human review.
