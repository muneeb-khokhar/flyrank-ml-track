# Prompt ladder — reading a model result

Muneeb Ur Rehman · FlyRank ML internship, Applied Search Intelligence track

**The task I'm prompting for:** I have a model comparison table from `w05_model.ipynb` and I need
to work out whether the result is good enough to act on. This is a thing I do every week, and for a
long time I did it by typing two words and hoping.

**How these were run:** Claude Opus 5, each version run exactly as written, one layer added per
version. Outputs are excerpted for length — trimmed at paragraph boundaries, nothing reworded.

**The layers, in the order I added them:**

| Version | Layer added | Why that one |
|---|---|---|
| Baseline | — | The two words I used to type |
| V1 | A clearer goal | Baseline didn't know what the explanation was *for* |
| V2 | Real context | V1 was reasoning about data it had never seen |
| V3 | Quality criteria | V2 believed every number equally |
| V4 | Constraints | V3 was 900 words of hedging |
| V5 | Review instructions | V4's constraints ate the caveats that made V3 good |

---

## Baseline

### Prompt

```
Explain this data
```

### Output (excerpt)

> I'd be happy to help you explain your data. To give you a useful explanation, it would help to
> know a bit more. In the meantime, here's a general framework for explaining any dataset:
>
> **1. Understand the structure.** How many rows and columns? What does one row represent?
> **2. Check data types.** Which columns are numeric, categorical, dates?
> **3. Look at distributions.** Calculate mean, median, standard deviation for numeric columns.
> **4. Find missing values.** Which columns have nulls, and how many?
> **5. Explore relationships.** Correlation matrices and scatter plots can reveal patterns.
> **6. Identify outliers.** Values far from the norm may be errors or genuinely interesting.
>
> Could you share the dataset or describe what it contains? Then I can give you specifics.

### Notes

**What changed in the prompt:** Nothing — this is the starting point.

**What actually improved in the output:** Nothing. It's a textbook table of contents. It doesn't
know what my data is, what decision I'm making, or that "explain" for me means "tell me whether to
trust this." It's also mildly insulting — step 1 is "how many rows."

**What still failed:** Everything. It ended by asking me the question I should have answered in the
prompt. Half the response is a request for the prompt I should have written.

**What I'd try next:** Tell it what the explanation is *for*. Right now it has no way to know
whether I want an intro-to-pandas tutorial or a decision.

---

## V1 — added a clearer goal

### Prompt

```
I have results from a model that ranks web pages for a content editor to review.
I need to decide whether the result is good enough to hand to that editor.
Explain the data with that decision in mind.
```

**Layer added:** a clearer goal. Nothing else — still no numbers, no audience spec, no format.

### Output (excerpt)

> To decide whether a ranking model is ready to hand to an editor, focus on these questions:
>
> **Is it better than what they'd do without it?** Compare against a baseline — random ordering, or
> whatever heuristic they use today. If your model isn't clearly beating that, it isn't ready.
>
> **Is it measured where it's used?** If an editor only reviews the top 20 or 50 items, then
> precision at that cutoff is your metric. A good overall AUC can hide a bad top-of-list.
>
> **Was it validated honestly?** If related pages can appear in both training and test, your
> numbers are optimistic. Grouped splits usually matter here.
>
> **What's the cost of a wrong item?** For a review queue, a false positive costs a few minutes.
> That's a forgiving error profile, which means you can ship at a lower bar than you would for
> something automated.
>
> If you share your actual metrics — baseline comparison, precision at your review depth, and how
> you split — I can tell you whether the numbers clear that bar.

### Notes

**What changed in the prompt:** One layer — I stated the decision the explanation serves.

**What actually improved in the output:** It stopped being a data-exploration tutorial and started
being a readiness checklist. The row-counting and correlation-matrix filler vanished completely.
More usefully, it independently raised precision-at-review-depth and grouped splits — the two
things that actually matter for my problem — without me naming them. The framing did that.

**What still failed:** It's reasoning about a model it has never seen. Every sentence is
conditional: "if your model isn't beating that," "if related pages can appear in both." It's a good
checklist and a useless answer, and it still ends by asking for the numbers.

**What I'd try next:** Give it the actual numbers. It has told me exactly which ones it needs.

---

## V2 — added real context

### Prompt

```
I have results from a model that ranks web pages for a content editor to review.
I need to decide whether the result is good enough to hand to that editor.
Explain the data with that decision in mind.

Here are the results. 120,507 pages from the Feb + Mar 2026 partitions. Label is
"impressions dropped 20%+ vs the prior 30 days". Split is GroupShuffleSplit on
client_hash_id: 59,836 train / 21,610 test. Test base rate 0.161.

Method                 Precision@50
base_rate (random)     0.161
baseline_rule          0.180
logistic_regression    0.260
random_forest          0.620

Permutation importance on the forest:
imp_prev30 0.047 | rare_share 0.014 | pos_prev30 0.005 | days_since_update 0.003
clk_prev30 0.003 | anon_share 0.0006 | days_active_prev30 -0.001
```

**Layer added:** real context. The goal statement from V1 is unchanged.

### Output (excerpt)

> These are strong results. Here's the read:
>
> **The forest is the clear winner.** At 0.620 Precision@50 against a 0.161 base rate, it's finding
> declining pages at roughly 3.8× the rate of random ordering. In practical terms, 31 of the top 50
> pages an editor opens will be genuinely declining, versus 8 if they picked at random.
>
> **Your baseline rule is barely working.** 0.180 against a 0.161 base rate is almost nothing —
> the rule is contributing about one extra correct page per 50 reviewed. That's a useful finding in
> itself: the heuristic your team may already trust isn't doing much.
>
> **The split is honest.** Grouping on client prevents pages from the same site leaking across
> train and test, which is the right call for this data.
>
> **Feature importance is concentrated.** `imp_prev30` dominates at 0.047, an order of magnitude
> above everything else. `days_active_prev30` is slightly negative, meaning it's contributing noise.
> You could likely drop it with no loss.
>
> **Verdict: ship it to the editor.** The lift over both random and the existing rule is large, the
> validation design is sound, and the cost of a false positive is low.

### Notes

**What changed in the prompt:** One layer — I pasted the actual numbers, split design, and label
definition.

**What actually improved in the output:** Every conditional collapsed into a statement. It did the
arithmetic I hadn't done — converted 0.620 into "31 of the top 50," and 0.161 into "8" — which is
the form I actually need to explain this to a non-technical editor. It also spotted on its own that
`days_active_prev30` at −0.001 is noise, and read the rule's 0.180 as the interesting finding rather
than a footnote.

**What still failed:** It believes every number equally. "These are strong results" and "the split
is honest" are both delivered flat, with no sense that Precision@50 is measured on 50 rows out of
21,610 — a slice thin enough that a handful of pages moves it. It never asked where the label comes
from or whether the features could see past it. And it ended on "ship it," which no one should say
about a model they've seen one table from.

**What I'd try next:** Tell it what a trustworthy answer has to do. Right now it has no standard to
hold the numbers against, so it holds them against nothing.

---

## V3 — added quality criteria

### Prompt

```
[V2 prompt, unchanged, plus:]

A good answer meets these criteria:
- Every claim names the specific number it rests on and the split that number
  was measured on.
- Every number gets a note on how much weight it can bear — sample size,
  how easily it moves, what it isn't measuring.
- Anything that could be inflated by leakage or by the metric's own definition
  is flagged explicitly, even if you're not sure.
- If the data doesn't support a verdict, say that instead of giving one.
```

**Layer added:** quality criteria.

### Output (excerpt)

> **Precision@50 = 0.620 (random forest, 21,610-row grouped test split).** This is the headline, and
> it's the number carrying the least weight per unit of attention it attracts. Precision@50 is
> computed on 50 rows. Fifty. Out of 21,610. Moving four pages in or out of that cutoff swings it by
> 0.08 — larger than the entire gap between your logistic regression and your baseline rule. I would
> not report this number without a confidence interval or a Precision@100 and @200 alongside it.
>
> **Precision@50 = 0.180 (baseline rule, same split).** Same fragility, and one thing more: your rule
> is a hard filter, so if it flags far fewer than 50 pages, the "top 50" is mostly ties being broken
> arbitrarily. That would make 0.180 a measurement of your sort order, not your rule. Worth checking
> how many pages the rule actually fires on.
>
> **Base rate 0.161 vs. overall 0.281.** Your test split's base rate is well below the population
> rate quoted for the full 120,507 rows. That's what grouped splitting does — you didn't get a random
> sample, you got whichever clients landed in test. It's the honest choice, but it means this number
> is specific to those clients, and a different `random_state` could hand you a materially different
> figure.
>
> **Leakage flags — two, neither certain.** First, the label is defined from `imp_last30` and your
> dominant feature is `imp_prev30`. These aren't the same column, but they're the same quantity
> measured in adjacent windows, and the label is a *ratio* between them. A model leaning that hard on
> the denominator of its own label deserves a hard look. Second, `days_since_update` at 0.003 is
> suspiciously inert for a feature that should matter enormously to a staleness problem. That usually
> means the feature is broken, not that staleness is irrelevant.
>
> **Verdict: I can't give you one from this table.** What you have is evidence that the forest orders
> pages better than random on one split at one cutoff. That's genuinely something. It is not evidence
> that the ranking holds at the depth an editor actually reviews, or across other clients.

### Notes

**What changed in the prompt:** One layer — four criteria defining what a trustworthy answer does.

**What actually improved in the output:** It stopped agreeing with me. V2's "these are strong
results" became a specific, checkable objection: 0.620 is computed on 50 rows and moves 0.08 if four
pages shift. It caught the tie-breaking problem with the rule's 0.180 — which is real, my rule fires
on 32 pages out of 120,507, so that number *is* mostly ties. I hadn't seen that myself until it
said so. It also flagged the `imp_prev30` / label-ratio relationship, which is the sharpest thing
anything in this ladder produced. And it refused the verdict instead of inventing one.

**What still failed:** It's 900 words to say "don't trust the headline yet." The good insight is
buried in the fourth paragraph. If I paste this into a thread, nobody reads to the leakage flags.
It also hedges compulsively now — "neither certain," "worth checking," "usually means" — which is
appropriate individually but exhausting in aggregate.

**What I'd try next:** Force it to be short. The insight is there; the delivery is unusable.

---

## V4 — added constraints — *this one made it worse*

### Prompt

```
[V3 prompt, unchanged, plus:]

Constraints: under 200 words. No "significant", "strong", "robust", or "clearly".
No causal verbs — nothing "drives", "causes", "leads to", or "improves" anything.
```

**Layer added:** constraints.

### Output (excerpt — this is nearly the whole thing)

> **Random forest: Precision@50 = 0.620**, test base rate 0.161, on a 21,610-row grouped split. Of
> the top 50 pages, 31 were labelled declining; random ordering gives 8.
>
> **Baseline rule: 0.180.** Barely above the base rate.
>
> **Logistic regression: 0.260.** Between the two.
>
> **Caveat:** Precision@50 rests on 50 rows. Small shifts move it.
>
> **Feature weight** sits almost entirely on `imp_prev30` (0.047). `days_active_prev30` is negative
> and can be dropped.
>
> **Read:** the forest orders pages better than random on this split at this cutoff. Whether that
> holds at review depth is untested.

### Notes

**What changed in the prompt:** One layer — a word ceiling and a banned-word list.

**What actually improved in the output:** The prose. It's scannable, the numbers lead, and the
banned-word list did exactly what I wanted — no "strong results," no "the model improves precision."
The last line survives intact and is honest.

**What still failed — and this is the version that went backwards.** The 200-word ceiling didn't
compress the analysis, it deleted it. Both leakage flags are gone. The `imp_prev30`-is-the-
denominator-of-its-own-label observation — the single most valuable thing in this entire ladder — did
not survive. The tie-breaking problem with the rule's 0.180 is gone; it's back to "barely above the
base rate," which is what V2 said before it knew anything. Even `days_since_update` being
suspiciously inert became "can be dropped," which is the opposite conclusion: V3 read 0.003 as
evidence the feature is *broken*, V4 read it as evidence the feature is *unimportant*. That's not a
shorter answer, it's a wrong one.

What I actually learned: the model spends its word budget on structure first. Given 200 words it
writes headings and bullets and one caveat, because that *looks* like a complete answer. The
criteria from V3 were still in the prompt and it silently traded them away to fit. Constraints and
quality criteria compete, and constraints win.

**What I'd try next:** Stop making them compete. Give the caveats their own space outside the word
limit rather than hoping they survive inside it.

---

## V5 — added review instructions

### Prompt

```
[V4 prompt, unchanged, plus:]

After you finish the main answer, stop and review your own draft. Then add two
sections, which do not count against the word limit:

REVIEW — every claim in your answer that you can't tie to a specific number in
the table, and every number you used that carries less weight than its
prominence suggests.

CANNOT SHOW — what this data cannot tell me, regardless of how the numbers came
out. Include anything you suspect might be leakage even if you're unsure.
```

**Layer added:** review instructions.

### Output (excerpt)

> **Random forest: Precision@50 = 0.620**, test base rate 0.161, 21,610-row grouped split. Of the top
> 50 pages, 31 were labelled declining. Random ordering gives 8.
>
> **Baseline rule: 0.180.** Roughly one extra correct page per 50 reviewed, over random.
>
> **Logistic regression: 0.260.**
>
> **Feature weight** sits almost entirely on `imp_prev30` (0.047), an order of magnitude above the
> next feature.
>
> **Read:** on this split, at this cutoff, the forest orders pages better than random and better than
> the rule. That is the full extent of what the table shows.
>
> ---
>
> **REVIEW**
>
> - *"Better than the rule"* — the rule's 0.180 assumes 50 pages were actually ranked by it. If your
>   rule is a hard filter firing on fewer than 50, the top 50 is mostly arbitrary tie-breaks and
>   0.180 measures your sort order, not your rule. Check the fire rate before repeating this claim.
> - *Precision@50, all four rows* — computed on 50 observations. Four pages moving across the cutoff
>   swings it ~0.08, wider than the logistic-regression-to-rule gap. Every comparison in this table
>   is within the noise of the metric.
> - *Base rate 0.161* — a property of whichever clients landed in test under this seed, not of your
>   population. A different `random_state` gives a different denominator for everything above.
> - *`days_active_prev30` is negative* — I said nothing about dropping it. −0.001 is indistinguishable
>   from zero at this sample size; it's uninformative, not harmful.
>
> **CANNOT SHOW**
>
> - Whether ranking holds at the depth an editor reviews. @50 says nothing about @200.
> - Whether refreshing a flagged page recovers traffic. Nothing here is causal; that needs an
>   experiment.
> - **Possible leakage.** Your label is a ratio of `imp_last30` to `imp_prev30`. Your dominant feature
>   *is* `imp_prev30` — the denominator of the label. Not the same column, but the same quantity in
>   an adjacent window, and a model leaning this hard on it may be reading the shape of its own
>   target. This alone would make me hold the result.
> - **Possible broken feature.** `days_since_update` at 0.003 is near-inert for a staleness problem.
>   The likelier explanation is a defective column than an irrelevant concept. Check for negative
>   values — content edited after the feature window closes would produce exactly this.

### Notes

**What changed in the prompt:** One layer — a self-review pass with two named sections, explicitly
exempt from the word limit.

**What actually improved in the output:** Both things V4 deleted came back, and sharper than in V3.
The leakage flag is now a named recommendation ("this alone would make me hold the result") rather
than a hedge in paragraph four. The `days_since_update` note went further than V3 did — it predicted
*negative values from content edited after the window closes*, which is the exact bug I found by
hand in `w05_model` while chasing three wrong predictions. It arrived there from the importance
score alone. The main answer stayed at V4's length, so I got the scannable version and the careful
version in one response instead of choosing.

It also corrected V4's error unprompted. V4 said drop `days_active_prev30`; the REVIEW section says
−0.001 is indistinguishable from zero and shouldn't be acted on. The review pass caught the previous
version's mistake.

**What still failed:** The REVIEW section audits the answer, not the analysis — it checks claims
against the table, but it can't check the table against the data. It has no way to verify my split
was implemented the way I described it, and it takes my word that the label never touched the
features. And it's now three sections; for a quick sanity check mid-notebook this is more ceremony
than I want.

**What I'd try next:** A verification layer — have it name the specific query or cell I should run
to settle each REVIEW item, so the output ends in a to-do list instead of a doubt list. That's the
sixth rung, and it's the one I'd build next.

---

## What the ladder actually taught me

The layer I expected to help most was constraints, and it was the only one that went backwards.
Word limits don't compress an answer, they select what to drop — and the model drops the
uncertainty first, because caveats are the least *answer-shaped* part of a response. V4 read like a
better answer and was a worse one, which is the failure mode I'd never have caught by reading V4
alone. I only saw it by putting V3 and V4 side by side and noticing that the leakage flag was gone.

Quality criteria (V3) bought the most and cost the most. Review instructions (V5) were the cheapest
real win — they didn't add analysis, they stopped the constraints from eating it.

---

## Final reusable prompt

Copy this, replace the three bracketed blocks, delete this line. Works for any model-comparison
table on this track.

```
I have results from a model on the FlyRank search data, and I need to decide
whether the result is good enough to act on.

THE DECISION
[Who acts on this output, and what they do with it. One or two sentences.
 e.g. "A content editor opens the top 50 pages of a ranked queue and reviews
 each one for refresh. A wrong page costs a few minutes of their time."]

THE SETUP
[Row count and which partitions. How the label is defined, in words.
 Split design and train/test sizes. Test base rate.]

THE RESULTS
[Paste the metric table. Paste feature importances if you have them.]

A GOOD ANSWER MEETS THESE CRITERIA
- Every claim names the specific number it rests on and the split that number
  was measured on.
- Every number gets a note on how much weight it can bear — sample size, how
  easily it moves, what it isn't measuring.
- Anything that could be inflated by leakage or by the metric's own definition
  is flagged explicitly, even if you're not sure.
- If the data doesn't support a verdict, say that instead of giving one.

CONSTRAINTS ON THE MAIN ANSWER
Under 200 words. No "significant", "strong", "robust", or "clearly". No causal
verbs — nothing "drives", "causes", "leads to", or "improves" anything.

THEN REVIEW YOUR OWN DRAFT
Add these two sections. They do not count against the word limit.

REVIEW — every claim in your answer you can't tie to a specific number in the
table, and every number you used that carries less weight than its prominence
suggests.

CANNOT SHOW — what this data cannot tell me regardless of how the numbers came
out. Include anything you suspect might be leakage even if you're unsure.
```

**Why the sections are in that order:** the criteria have to arrive before the constraints, or the
model treats them as optional and trades them for brevity. The review pass has to be explicitly
exempt from the word limit, or it gets compressed into the thing it was added to prevent. Both of
those are V4's lesson, and they're the only reason the final prompt works.
