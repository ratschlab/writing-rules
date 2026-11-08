# Writing that helps people learn

Use these principles for text whose goal is understanding: algorithm articles, tutorials on concepts, lecture notes and design explanations. [PRINCIPLES.md](PRINCIPLES.md) covers text that helps people act. Its rules on accuracy, uncertainty, terminology and review still apply here. This guide covers what changes when the reader's goal is to learn.

The main difference is the measure of success. Task text succeeds when the reader acts correctly and leaves. Teaching text succeeds when the reader can later explain the idea, apply it to a new problem and notice when it does not apply. That often needs more words, examples and reasoning, not fewer. [Diátaxis, S3, S58](SOURCES.md)

Each principle names its basis: **research**, **practice**, **opinion** or **house judgment**. See [sources and limits](SOURCES.md#teaching-and-explanation). Most research cited here tested school or university novices in short lessons. Applying it to self-paced articles read by novices and experts alike is an inference. These principles need a reader's judgment. A linter cannot check them.

## E1. Decide what the reader knows and what they should understand

Name the prerequisites and the understanding the text should produce. Write to the gap between them. Link prerequisites instead of reteaching them. **Practice:** Su and Google's technical-writing course both put the audience first and warn that experts skip steps they no longer notice. [S53, S59](SOURCES.md#teaching-and-explanation) **Research:** the expertise reversal effect shows that the right amount of guidance depends on the reader. Support that helps novices can hinder experts. [S34](SOURCES.md#teaching-and-explanation)

For example, an article on centroid decomposition can list depth-first search and subtree sizes as prerequisites in one line. It then spends its length on why the recursion depth is logarithmic.

## E2. State the problem and the central idea before the details

Open with the question the reader should be able to answer: the input, the goal and the constraint that makes it hard. Then give the key idea in a sentence or two. Details make sense only once the reader knows what they serve. **Opinion/practice:** Halmos advises organizing before writing and saying something definite. Tao asks authors to motivate a paper before its technical content. [S52, S54](SOURCES.md#teaching-and-explanation) **Research:** signaling the structure of a lesson reduces the effort spent finding it, mostly shown in multimedia lessons. [S44](SOURCES.md#teaching-and-explanation)

A reader of an automaton-based string algorithm needs to learn early what a state represents. Without it, the transitions and links that follow have no meaning.

## E3. Show a worked example before the general rule

Work a small concrete instance step by step, then state the general method. Move from the concrete to the abstract explicitly. Show how each symbol corresponds to the example. **Research:** studying worked examples helps novices more than solving equivalent problems unaided, and concreteness fading supports a deliberate move from concrete to abstract. [S31, S32, S40](SOURCES.md#teaching-and-explanation) **Opinion:** Gowers argues for examples first, and he warns against applying this to every definition. [S55](SOURCES.md#teaching-and-explanation)

Boundaries: gains in the original studies were limited to problems shaped like the examples. One example can mislead by suggesting a pattern that is not general. Add a contrasting case or an edge case. Experts may want to skip the example, so keep it in its own paragraph or block. [S31, S34](SOURCES.md#teaching-and-explanation)

## E4. Make the reason for each step recoverable

A reader should be able to answer "why does this hold?" at every step. Name the invariant, the property being used or the earlier result. For a long example, label what each group of steps achieves. Optionally, ask the reader to justify a step before you do. **Research:** students who explain examples to themselves learn more, and prompting for such explanations improved understanding in a small experiment. [S36, S37](SOURCES.md#teaching-and-explanation) Labeling subgoals in programming examples helped novices in one study and gave mixed results in a follow-up. [S47, S48](SOURCES.md#teaching-and-explanation)

Prefer "We go over $j$ in decreasing order. Then $f_{j-w}$ still holds the value from the previous item" to "Loop backwards."

## E5. Show the process, not only the result

For an algorithm, trace its state on a small input. A table with one row per step often shows more than another paragraph. State the invariant that the trace illustrates. **Research:** reviews of programming education argue that learners need an explicit model of how execution changes state. A study of developers found code examples among the documentation factors that most affect learning. [S49, S50](SOURCES.md#teaching-and-explanation) No controlled study found here tests traces inside algorithm articles. **House judgment:** keep the trace short enough to check by hand.

## E6. Treat notation as part of the explanation

Introduce each symbol where it is first needed, in words, and keep one meaning per symbol. Separate formulas with words. Make sentences read correctly when a reader skims the formulas. Choose notation that stresses the quantities that matter. Follow the field's and the project's conventions. **Practice/opinion:** Knuth's rules, Halmos's "resist symbols" and Tao's notation advice agree on these points. No experiments were found. [S51, S52, S54](SOURCES.md#teaching-and-explanation)

Avoid "$n$ is the number of points" in one section and "$n$ is a multiple of $p$" in the next. Write "Let $m$ be a multiple of $p$."

## E7. State every claim at its true strength

Separate what is proved, what is expected under stated assumptions and what is observed in practice. Give each complexity bound with its kind: worst case, expected or amortized. Say what randomness affects: running time or correctness. Mark open questions as open and link the source. A wrong bound teaches the wrong model, and readers rarely recheck it. **House judgment**, applying [P4](PRINCIPLES.md#p4-preserve-facts-and-uncertainty) to teaching. **Opinion:** Lamport argues that structured proofs catch errors that prose proofs hide. [S57](SOURCES.md#teaching-and-explanation)

## E8. Address the likely misconception directly

When readers commonly hold a wrong idea, state it, say that it is wrong and explain why. Then give the correct idea. Show the tempting incorrect step when it is natural and instructive. **Research:** a meta-analysis of 44 comparisons found refutation texts improved learning over other conditions, with a moderate effect. Most studies concerned science concepts. [S41–S43](SOURCES.md#teaching-and-explanation) Refute misconceptions readers actually hold. Repeating a myth without a clear correction was not what these studies tested.

## E9. Keep what serves understanding, cut what only decorates

Motivation, history that explains a design choice and a second view of the same idea serve understanding. Anecdotes, decorative images and tangents compete with it. **Research:** meta-analyses of the seductive details effect found that interesting but irrelevant additions reduce learning. [S45, S46](SOURCES.md#teaching-and-explanation) **Opinion/practice:** Thurston and Knuth value stating a key idea in more than one way. Diátaxis treats context and reasons as the substance of explanation. [S51, S56, S58](SOURCES.md#teaching-and-explanation)

Two views of an idea are different from one statement repeated. The redundancy effect concerns duplicate presentations of the same content. It does not argue against a complementary view. [S33, S44](SOURCES.md#teaching-and-explanation)

## E10. Spend length on what is new or hard

Give the hard step the most space. Keep routine steps short, but do not drop them. A step obvious to the author may be the one the reader is missing. Offer optional depth, such as a full proof or a general variant, in a separate, clearly labeled block. **Opinion:** Tao and Halmos favor economy on routine material. Lamport favors exhaustive structured proofs and suggests reading them level by level. [S52, S54, S57](SOURCES.md#teaching-and-explanation) **Research:** expertise reversal is the reason the right level depends on the reader. [S34](SOURCES.md#teaching-and-explanation)

## E11. Give the reader something to do

End with problems that need the idea, ordered by difficulty, or with questions that ask the reader to recall or apply it. **Research:** learners benefit from moving from worked examples to problems they solve themselves. Practice testing produced better retention after a delay than restudying. A review rates it among the most useful study techniques. [S35, S38, S39](SOURCES.md#teaching-and-explanation) That evidence measures retention of studied material. That linked practice problems improve learning from an article is an inference. Choose problems where the technique is a natural part of the solution.

## E12. Check the text as a learner would read it

Before publishing, read as someone who knows the prerequisites but not the topic. Check that each symbol is defined before use, that the example agrees with the general method and the code, and that each claim is proved, cited or qualified. When possible, ask such a reader to explain the idea back. Revise where they stall. **House workflow**, extending [P10](PRINCIPLES.md#p10-review-meaning-before-mechanical-style).

## Where task and teaching guidance differ

| Question | Task text ([PRINCIPLES.md](PRINCIPLES.md)) | Teaching text (this guide) |
| --- | --- | --- |
| Success | The reader acts correctly | The reader understands and can transfer |
| Opening | The result or action | The problem and the central idea |
| Examples | A working command or input | A worked instance, then the general rule |
| Length | As short as the task allows | As long as the reasoning needs |
| Background | Deferred or linked | Relevant reasons kept, decoration cut |
| Review | Can they find the point and act? | Can they explain it and apply it? |

House style rules from a consuming project, such as sentence length or punctuation, apply to teaching text only where they keep the meaning. A proof, derivation or worked example may need longer connected reasoning.
