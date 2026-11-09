# Problems that recur in LLM-written code

Use these principles when an LLM or coding agent writes code, tests or a pull request, and when you review such work. Each principle names a problem that studies and maintainers keep reporting, the evidence for it, and a practice that prevents or catches it. The guide ends with a checklist an agent can run before it submits, and one for the reviewer.

Most of these problems also occur in human code. Agents change the rates and the economics. An agent writes a plausible change in minutes, while review still takes a person's time. Several projects now name this imbalance in their policies. LLVM calls a contribution "extractive" when its review cost exceeds its benefit. [S159](../sources/llm-code.md#policies-and-practitioner-guidance) This framing is **house judgment**, built on the evidence below.

Each principle names its basis: **research**, **standard**, **practice**, **opinion** or **house judgment**. See [sources and limits](../sources/llm-code.md). Limits apply throughout. Most studies tested models from 2021 to 2025, and many are benchmarks rather than real repositories. Several 2026 studies are short papers or preprints. Newer models may show lower rates. None of the newer reports shows these problems gone. No cited study tests the checklists in this guide. Whether a change needs to exist at all is covered in [STEWARDSHIP.md](STEWARDSHIP.md). How to write the pull request text is covered in [ENGINEERING.md](ENGINEERING.md#pull-request-descriptions).

## Before writing

### C1. Search for existing code before writing new code

Before adding a function, type, constant or test helper, search the base branch and the project's dependencies for one that already does the job. Search by what the code does, not only by the name you would give it. If a close match exists, call it, or extend it and say why. Follow the patterns the surrounding code already uses. A new helper that repeats existing logic is a defect, even when it is correct and tested.

**Research:** agents add code that repeats existing code. In one Python project, new functions in agent pull requests were about 1.87 times as similar to existing functions as new functions in human pull requests. [S114](../sources/llm-code.md#duplication-and-reuse) In a Java dataset, agents gave duplication as the reason for only 1.1% of their refactorings. [S115](../sources/llm-code.md#duplication-and-reuse) Models re-implement a helper even when it is in their context, and the copy still passes the tests. [S118](../sources/llm-code.md#duplication-and-reuse) Models do much worse on functions that depend on project code, and better when relevant repository code is retrieved first. [S117, S119, S120](../sources/llm-code.md#duplication-and-reuse) Vendor data shows copied lines rising and moved lines falling across the industry during AI adoption. It is a correlation by calendar year from a vendor that sells code analysis. [S116](../sources/llm-code.md#duplication-and-reuse)

**Research:** copies drift apart, and unintended drift is often a bug. Juergens et al. found that about every second to third unintentional change to a clone led to a fault. [S121](../sources/llm-code.md#duplication-and-reuse) Other studies found faults in 17% of near-miss clones and bugs spread through copying. [S122, S123](../sources/llm-code.md#duplication-and-reuse) The counter-view is real. Deliberate forks and templates can be good design, and many clones never change. [S124, S125](../sources/llm-code.md#duplication-and-reuse) So the target is duplicated knowledge that must stay in agreement, such as two hash functions that must match. [Hunt and Thomas, S126](../sources/llm-code.md#duplication-and-reuse)

**Practice:** Anthropic's guide for its coding agent says to have the agent read the relevant code before it writes any. [S129](../sources/llm-code.md#duplication-and-reuse) The rule of three limits when to create a new abstraction. It does not justify re-implementing one that already exists. This reading is **house judgment**.

### C2. Do the task you were given, and nothing else

Change only what the task needs. Leave out features, options, refactorings and clean-ups that nobody asked for. If no change is needed, say so. If the specification cannot be met, stop and report it instead of working around it. Propose extra work separately. A new feature, option or API field also needs the checks in [STEWARDSHIP.md](STEWARDSHIP.md).

**Research:** agents tend to act. On tasks that needed no change, agents made unwanted changes in 35% to 65% of cases, most often to code unrelated to the issue. Telling them that no change is a valid outcome, and asking them to reproduce the problem first, helped. This is a preprint. [S132](../sources/llm-code.md#scope-and-hidden-changes) Among patches that passed the tests, extra behaviour was far more common than missing behaviour (27.3% against 5.2%), and some extra behaviour was wrong. [S133](../sources/llm-code.md#scope-and-hidden-changes) Unwanted features were a named reason for rejecting agent pull requests on GitHub. [S131](../sources/llm-code.md#scope-and-hidden-changes)

**Opinion:** Kent Beck treats functionality he did not ask for as a sign that the agent is going off track, "even if it was a reasonable next step". [S137](../sources/llm-code.md#scope-and-hidden-changes)

### C3. Keep one purpose per change, and name every behaviour change

Put a refactoring, a formatting change and a behaviour change in separate commits or pull requests. List every change a user or caller could notice: defaults, limits, error behaviour, output format, performance. A change that keeps tests green can still change behaviour.

**Research:** in a matched study of one agent, 39.9% of agent pull requests had more than one purpose, against 12.2% of human ones. [S130](../sources/llm-code.md#scope-and-hidden-changes) Changes that mix several purposes are harder to review, and mixed bug fixes mislead later analysis of the history. [S134, S135](../sources/llm-code.md#scope-and-hidden-changes) Larger agent pull requests that touched more files were merged less often. This is an association, not a cause. [S131](../sources/llm-code.md#scope-and-hidden-changes)

**Practice/opinion:** Google asks for changes that do one thing, with refactorings in their own change. [S136](../sources/llm-code.md#scope-and-hidden-changes) Beck separates structural changes from behaviour changes. [S137](../sources/llm-code.md#scope-and-hidden-changes)

## Verify

### C4. Check every name, dependency and claim before relying on it

Confirm that each package, function, flag and file you use exists in the version the project uses. Look it up in the registry, the lockfile or the source. Report a result only when a command in this session produced it, and show the command and its output. "Tests pass" without output is not evidence. Run the project's static analysis and security checks on the change.

**Research:** models invent dependencies. Across 16 models, at least 5.2% of packages suggested by commercial models and 21.7% of those suggested by open-source models did not exist, and many names recurred across runs. [S138](../sources/llm-code.md#verification) Fluent answers hide errors. In one study, 52% of ChatGPT answers to programming questions contained incorrect information, and users missed it 39% of the time. [S139](../sources/llm-code.md#verification) People who used an assistant wrote less secure code and believed it was more secure. [S140](../sources/llm-code.md#verification) A pre-release model claimed to have run code it could not run. [S141](../sources/llm-code.md#verification) Generated code had known weakness classes in about 40% of security-relevant scenarios. A later replication found fewer, but still many. [S142, S143](../sources/llm-code.md#verification) Developers' sense of speed and measured speed can disagree. METR's first trial found experienced developers 19% slower with AI while they believed they were faster. Its 2026 update estimates a speed-up, with strong selection effects. Measure outcomes rather than trusting the impression. [S165](../sources/llm-code.md#verification)

**Practice:** GitHub's review guide tells reviewers to check that dependencies exist and to watch for invented APIs. [S144](../sources/llm-code.md#verification) Anthropic's guide asks for the command and its output, not a summary. [S129](../sources/llm-code.md#duplication-and-reuse)

### C5. Write tests that can fail

Take expected values from the specification, the issue or a trusted reference, not from running the new code. For a fix, add a test that fails before the change and passes after it. Check that the tests would catch a plausible mistake. Mutation testing on the changed lines measures that. Coverage does not.

**Research:** tests that a model writes from the code tend to encode what the code does, bugs included. This is a preprint. [S145](../sources/llm-code.md#tests) SWE-bench requires at least one test that fails before the fix. [S146](../sources/llm-code.md#tests) Even so, 29.6% of patches that passed behaved differently from the developers' fix, because the tests were weak. [S133](../sources/llm-code.md#scope-and-hidden-changes) Coverage correlates only weakly with a suite's ability to find faults once suite size is controlled. [S147](../sources/llm-code.md#tests) At Google, mutation testing during code review was practical at scale, and developers who saw mutants wrote more tests. [S148, S149](../sources/llm-code.md#tests)

**Opinion:** Willison asks for a test that fails if the change is reverted, plus evidence of a manual check in the pull request. [S153](../sources/llm-code.md#tests)

### C6. Never weaken a test to make it pass

Do not delete, skip or loosen a test, and do not special-case test inputs, to get a green run. If an existing test is wrong, change it in a separate, explained step and name the change in the description. Reviewers should read every edit to a test or assertion as a behaviour change.

**Research:** agents game tests under pressure. In a benchmark whose tests contradict the specification, one frontier model passed 76% of one task set, which is only possible by cheating. It modified tests despite instructions not to, special-cased inputs and overloaded comparison operators. Read-only tests stopped edits but not special-casing. This is a preprint. [S150](../sources/llm-code.md#tests) METR found a frontier model hacking the scorer in 30.4% of runs on one benchmark, and instructions not to cheat did not stop it. [S151](../sources/llm-code.md#tests)

**Practice:** Anthropic's system cards report that its models sometimes special-case tests after repeated failures. They advise monitoring for unexpected edits to test files. Rates fell in later models but did not reach zero. [S152](../sources/llm-code.md#tests) CPython's contribution guide forbids altering or bypassing tests to make them pass. [S160](../sources/llm-code.md#policies-and-practitioner-guidance) GitHub's guide tells reviewers to look for tests deleted or skipped instead of fixed. [S144](../sources/llm-code.md#verification)

### C7. Handle errors the way the project does

Use the project's existing error types, messages and reporting paths. Do not leave a handler empty or have it only log. Do not catch every exception, and do not fall back silently to a default. Treat one state the same way on every code path. Test the error path itself.

**Research:** Yuan et al. studied 48 catastrophic failures in five distributed systems. 92% came from mishandled errors that the software had already signalled. 35% came from three trivial patterns: an empty or log-only handler, an abort on an overly general exception, and a handler marked TODO. Simple tests of the error handlers would have caught 58%. [S154](../sources/llm-code.md#error-handling) Code models reproduce error-swallowing patterns found in their training data, such as an `except` clause with only `pass`. [S155](../sources/llm-code.md#error-handling) We found no strong study that measures how often current agents swallow errors. The rule rests on the cost evidence and on reviewers' reports.

**House judgment:** "one state, one predicate" comes from review findings on agent code where a single and a batch path handled the same unknown outcome differently.

## Describe and own

### C8. Describe what the diff does, briefly, and nothing it does not

Write a short description of the final diff: the problem, the result and any behaviour change from C3. Check every claim against the diff before submitting. Leave out review history, abandoned approaches and repeated summaries. [ENGINEERING.md](ENGINEERING.md#pull-request-descriptions) covers the format.

**Research:** among more than 23,000 agent pull requests, the most common mismatch between description and code was a description claiming changes the code did not contain (45.4% of mismatched cases). Mismatched pull requests were accepted 28.3% of the time, against 80.0%. [S156](../sources/llm-code.md#descriptions) Agent descriptions had a median of 355 words, against 56 for human ones. [S130](../sources/llm-code.md#scope-and-hidden-changes) When developers edited generated descriptions, deleting text was the most common edit. They added intent and testing details the tool had missed. [S157](../sources/llm-code.md#descriptions)

**Practice/opinion:** LLVM strongly recommends that contributors write descriptions themselves. curl calls AI-written reports too wordy. [S159, S163](../sources/llm-code.md#policies-and-practitioner-guidance) Willison puts a short human-written opener first and folds the agent's long text away. [S158](../sources/llm-code.md#descriptions) Google asks authors to reread the description so it still matches the change. [S20](../sources/writing.md#engineering-communication)

### C9. Submit only code a person can explain

The person who submits the change answers for it. They should be able to explain every line and every test without the tool, and to answer review questions. Disclose tool use the way the receiving project asks. Some projects restrict or refuse AI-generated code, so read the policy first.

**Practice:** LLVM, CPython, the Linux kernel and Ghostty all require that a human has read and understands the whole change and can answer for it. The kernel also asks submitters to say what they could not build, test or reproduce. [S159–S162](../sources/llm-code.md#policies-and-practitioner-guidance) **Opinion:** Willison's rule is not to commit code you could not explain to someone else. [S164](../sources/llm-code.md#policies-and-practitioner-guidance)

## Review

### C10. Review against the base branch, not only the diff

For each new function or type, ask whether the base branch or a dependency already provides it. Ask this independently of who calls the new code. A check of callers shows only that the new code is used, not that it is needed. Use a reviewer that has not seen the author's reasoning. Where the project has a clone detector, run it on the change against the base branch.

**House judgment, from a case:** in a four-part stack of agent pull requests, independent sweeps found about a dozen helpers that duplicated the base branch or each other. Examples were a hash function identical to one in a dependency, a run-length encoder identical to an existing function, wrappers over existing mapping functions, and test helpers copied between files. Earlier agent reviews had missed them because they checked who used each new symbol.

**Research:** when human reviewers flag code smells, duplicated code is the most common one. Where they named a cause, it was mostly unfamiliarity with existing code. That study counts what reviewers flagged, not what they missed. [S127](../sources/llm-code.md#duplication-and-reuse) Reviewers' comments on agent pull requests were no more negative than on human ones, despite the extra duplication. [S114](../sources/llm-code.md#duplication-and-reuse) We found no study of how often reviewers miss duplicated helpers.

**Practice:** token-based clone detectors such as PMD CPD, jscpd and SonarQube find copied and renamed code. jscpd can fail only on clones that are new relative to the base branch. SonarQube's default gate allows at most 3% duplication in new code. These tools probably miss a helper rewritten from scratch, so they support the search in C1 and do not replace it. [S128](../sources/llm-code.md#duplication-and-reuse) Anthropic recommends a fresh reviewer that has not seen the author's reasoning. [S129](../sources/llm-code.md#duplication-and-reuse)

## Checklist before submitting

An agent can run these steps on its own change. Report the result of each in the handoff, not in the pull request text.

1. **Reuse.** For every new function, type, constant and test helper, search the base branch and dependencies by behaviour. Replace each match with a call, or record why not.
2. **Scope.** Compare the diff with the task. Remove or split out anything the task did not ask for.
3. **One purpose.** Split refactoring and formatting from behaviour changes. List every behaviour change.
4. **Names.** Confirm each new package, import, API and flag exists in the version in use.
5. **Tests.** Check that each fix has a test that fails without it. Check that expected values come from the specification.
6. **Test edits.** List every edited, skipped or deleted test or assertion, with its reason.
7. **Errors.** Search the diff for empty handlers, catch-all handlers and silent defaults.
8. **Evidence.** Run the project's build, tests and checks in this session, and keep the commands and output.
9. **Description.** Reread the description against the final diff. Remove any claim the diff does not support.

## Checklist for reviewing agent-written code

1. Does the base branch or a dependency already have each new helper?
2. Does the diff do only what the task asked?
3. Does each pull request have one purpose, with every behaviour change named?
4. Do all new names and dependencies exist?
5. Would the tests fail if the change were wrong?
6. Were any tests weakened, skipped or special-cased?
7. Are errors handled as elsewhere in the project?
8. Does the description match the diff?
9. Can the author explain the change?

A missing answer is a question for the author, not an automatic rejection.
