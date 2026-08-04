# Portfolio copy — framed cases

Muneeb Ur Rehman · FlyRank ML internship, Applied Search Intelligence track

## Voice card

> **Plain, specific, honest about the limits.**

Standing instruction for the Claude Project:

> Write in my voice: plain, specific, honest about the limits. Short sentences. Real numbers with
> the split and the sample size attached. Name the decision, not the technology. Never write
> "results-driven", "passionate", "leveraging", "cutting-edge", "seamlessly", or "impact" as a noun.
> If a claim needs a hedge, hedge it in the sentence — don't drop the claim and don't inflate it.
> If I can't say it out loud to a skeptic, cut it.

**Who this site talks to:** one hiring manager at a small data team — someone deciding whether to
spend 45 minutes interviewing a junior ML hire.

**The one action:** email me.

---

## Sitemap — what this document covers

| # | Piece | Source work |
|---|---|---|
| 1 | Home / hero | — |
| 2 | Case 1 — The review queue that beat the rule | `w04_baseline_score`, `w05_model` |
| 3 | Case 2 — The model that scored 1.000 and was worthless | `w03_data_contract` |
| 4 | Case 3 — Two assumptions behind the rule, tested | `w04_baseline_score` §1 |
| 5 | About / bio | — |
| 6 | Contact / CTA | — |

Not included, because they aren't finished: the validation audit (ML-09), the action playbook
(ML-10), and the capstone paper. When those land they become Case 4.

---

## 1. Home / hero

> ### I build ranking tools that tell an editor what to look at first.
>
> I'm Muneeb Ur Rehman, an ML intern on FlyRank's Applied Search Intelligence track. I work on one
> problem: a content team has 120,000 pages and time to review fifty. Which fifty?
>
> Three cases below. Each one has the numbers, the split they were measured on, and the part that
> didn't work.
>
> [Email me →](mailto:muneebkhokher38@gmail.com)

---

## 2. Case 1 — The review queue that beat the rule

### The problem

A content team can't review every page. They review the top of a list, so the only thing that
matters is what's at the top of the list. The usual list is a hand-written rule: flag anything
stale and still getting traffic. Nobody had checked whether that rule actually puts declining pages
at the top, or how much better anything else would do.

I framed it as a ranking problem, not a classification problem. The output isn't a verdict on a
page. It's an order.

### What I did, and what I decided

I built the hand-written rule first, on purpose, so I'd have something to lose to. The rule:
stale (180+ days since update) **and** visible (500+ impressions in the prior 30 days), scored by
impression volume. One reason code — `stale_but_visible`. On 120,507 pages from the February and
March 2026 partitions, it flagged 32.

Thirty-two pages out of 120,507. The rule wasn't wrong, it was absent.

Then the model. Three decisions I'd defend:

- **Precision@50 as the metric.** Recall across 120,507 pages is a number nobody acts on. The
  editor opens the top of the queue and stops. So I measured the top of the queue.
- **Split grouped by client, not by row.** Pages on one site move together — same site health, same
  algorithm update. A random row split lets the model see a page's twin in training and then score
  its sibling in test. That's not a model, that's a lookup. `GroupShuffleSplit` on `client_hash_id`:
  59,836 train, 21,610 test.
- **Features restricted to the prior 30-day window.** Everything the model sees was knowable before
  the outcome window opened. The label — impressions down 20%+ — is computed from the later window
  only, and never touches the feature table.

Logistic regression first, because I wanted a readable coefficient story. Random forest second,
because the rule's failure was specifically about combining signals, and that's what a forest does.

### What came of it

**The headline is leave-one-client-out.** Every client held out in turn, the model trained on all the
others and scored on the one it had never seen. Every figure below is printed in the committed output
of [`w06_validation_audit.ipynb`](notebooks/w06_validation_audit.ipynb), over a window pinned to
`2026-03-31`.

| Leave-one-client-out | |
|---|---|
| Clients in the panel | 36 |
| Clients scoreable (≥50 rows, both classes present) | 24 |
| **Scoreable clients beating their own base rate** | **21 of 24** |
| **Mean lift over each client's own base rate** | **2.17×** (median 1.78×) |
| Mean Precision@50 across held-out clients | 0.291 (median 0.240) |
| Range across clients | 0.04 – 0.72 |

Lift is the column that matters. Absolute Precision@50 varies hugely between clients because their
base rates do — a client where 1.6% of pages decline cannot produce the same P@50 as one where 50%
do. Each client compared against *its own* base rate is the only version of the question that means
anything, and 21 of 24 came out ahead.

The three that didn't are all small: 143, 72 and 228 rows, each missing by a single page in the top
50. I'd rather show them than round them away.

Twelve of the 36 clients weren't scoreable at all — under 50 rows, or every page in one class. I
report 36 and 24 separately instead of quietly using the smaller number as the denominator.

**The single-split table is not a co-equal result. It's the thing that made me suspicious.**

| Method | Precision@50 — one split, seed 42 |
|---|---:|
| Random order (test base rate) | 0.161 |
| The hand-written rule | 0.160 |
| Logistic regression | 0.260 |
| Random forest | 0.600 |

That split put **9 clients** on the test side. Nine. 21,610 rows sounds like plenty until you notice
the split is really a draw of nine clients, and pages within a client move together.

So I ran the same design across seven seeds: **0.34 to 0.66, mean 0.509, sd 0.111** — and every one
of those splits also held exactly nine clients. The model never changed. Only which nine landed on
the test side. A number that swings by 0.32 on the draw was never a measurement.

That table appears here as the trigger for the audit, not as a result. Every number after it exists
because an earlier number made me suspicious of itself.

**The broken feature was actively hurting.** `days_since_update` is measured against the window end,
so a page edited after the window closes comes out negative — **65,211 of 81,446 rows, 80.1%**. Not
an edge case: for four fifths of the panel the feature describes an edit that hadn't happened at
decision time. The two groups differ in decline rate (0.165 where negative, 0.214 where not), so
it's structured error, not noise. Dropping the feature entirely raised the seed-sweep mean from
**0.509 to 0.566**. It wasn't dead weight, it was a thumb on the scale.

**Then the audit had its own bug — twice.**

First, the extraction window came from `MAX(report_date)`, which resolves against whatever the
warehouse holds at run time. An earlier LOCO run gave 22 of 24 at 2.37×. I attribute the shift to
partition drift — **and I can't prove it**, because I never logged what the old window resolved to.
That missing log is itself the defect. The window is now hardcoded and printed into every notebook's
output.

Second, and I only caught this by comparing two notebooks that should have agreed: `w05` reports
0.600 for the seed-42 split and `w06` reports 0.620. Same seed, same 81,446 rows, same split design.
The cause is that DuckDB gives no row-order guarantee without an `ORDER BY`, and `GroupShuffleSplit`
works on positional indices — so a fixed seed on an unordered frame is not actually reproducible. The
queries now sort by `(client_hash_id, content_hash_id)`. One confirming re-run is outstanding; until
it lands, treat 0.600 and 0.620 as the same number measured twice through a defect I've since fixed.

Then the part I'd actually talk about in an interview. At a 0.8 confidence threshold the model had
zero confident mistakes, which made me suspicious rather than pleased. I dropped the threshold to
0.5 and found three. All three had a **negative** `days_since_update` — the page was edited after
my feature window closed, so "days since update" was measuring nothing. Permutation importance had
already been telling me this: `days_since_update` contributed 0.003, and `days_active_prev30`
contributed −0.001. One feature was broken and one was noise. The model was carrying almost all of
its weight on prior-window impression volume (0.047).

That's a limitation of my feature table, not a quirk of the model, and it's the first thing I'd fix.

**What this doesn't say:** it doesn't predict Google's ranking algorithm, and it doesn't show that
refreshing a page recovers its traffic — that needs an experiment I haven't run. It ranks pages for
a human to look at.

It also doesn't say the model scores 0.600, or any single number. Across seven seeds of that same
split design it ranged 0.34 to 0.66. The claim I'll defend is the LOCO one — 21 of 24 scoreable
held-out clients beat their own base rate at a mean lift of 2.17× — because that's the only version
where every client got tested rather than one draw of nine of them.

It also doesn't cover the 12 clients too small or too one-sided to score. Whatever the model does on
a client with 40 pages, this doesn't measure it.

And the date-drift explanation is a hypothesis, not a finding. I can't prove partition drift caused
the earlier 22/24 → 2.37× result to move, only that nothing else changed between the runs.

---

## 3. Case 2 — The model that scored 1.000 and was worthless

### The problem

Before building features against the full warehouse (~9.8M rows in the March 2026 partition alone),
I had to write down the data contract: what one row is, which fields are features, which are label,
which are excluded and why. The tempting move is to write the contract, believe it, and move on.

### What I did, and what I decided

I verified every claim in the contract with a query instead of a sentence. Grain check on
`(report_date, client_hash_id, content_hash_id)` — zero violations across 9,841,378 rows spanning
2026-03-01 to 2026-03-31.

Then I decided to attack my own feature set rather than defend it. I trained the honest version —
five features, all from the prior 30-day window — and then deliberately trained a second version
with `imp_last30` added, the column the label is derived from.

Two other exclusions I'd argue for:

- **`gsc_avg_position` on zero-impression days.** A 0 there means "no data", not "ranked zeroth".
  Averaging it in silently drags every position down.
- **Clients with no GA4 start date.** Filtered on `ga4_data_start IS NOT NULL` rather than
  `!= FALSE`, because the flag can be NULL and NULL isn't FALSE. That dropped 60,333 content items
  to 46,016 — a quarter of my data, on purpose.

### What came of it

| Feature set | AUC |
|---|---:|
| Honest (prior-window only) | 0.486 |
| With `imp_last30` added | 1.000 |

A perfect 1.000. The model wasn't predicting anything; it was reading the answer off the label's own
arithmetic.

And the honest number is 0.486 — slightly worse than a coin flip. I kept it. That result told me
those five features, on that one-month slice, carry no usable signal for that label, which is why
the Case 1 model uses a two-month window, a wider feature set, and a different framing. Reporting
0.486 was more useful than reporting 1.000, because 1.000 would have sent me forward on a model that
was going to fall apart the first time it saw a page whose outcome wasn't already in its inputs.

**What this doesn't say:** 0.486 is one month, one label definition, five features. It's evidence
that this particular setup didn't work, not that the problem is unlearnable.

---

## 4. Case 3 — Two assumptions behind the rule, tested

### The problem

The "stale and visible" rule rests on two claims nobody had checked against the data: that older
pages decline more, and that high-traffic pages are the ones worth reviewing. Both sound obviously
true. I wanted to know if they were.

### What I did, and what I decided

I bucketed 120,507 pages by days-since-update and by prior-window impressions, and measured the
observed decline rate in each bucket. No model, just group-and-count — because if the assumption
fails here, no amount of modelling downstream repairs it.

### What came of it

**Staleness — doesn't rise cleanly, and the table is smaller than it looks.**

| Days since update | Decline rate | Pages |
|---|---:|---:|
| 0–90 | 0.432 | 29,601 |
| 91–180 | 0.270 | 278 |
| 181–365 | 0.983 | 1,277 |

Read the Pages column before the Decline rate column. Those three buckets hold 31,156 pages — **26%
of the 120,507 I started with.** The other 89,351 have a negative `days_since_update`, so `pd.cut`
dropped them to `NaN` and the group-by silently discarded three-quarters of my data without raising
anything.

That's the same broken feature from Case 1, showing up somewhere I wasn't looking for it. In Case 1
it cost me three wrong predictions. Here it quietly deleted most of the evidence, and the table still
rendered and still looked like a finding.

On what's left: the 181–365 bucket is almost entirely declining, which supports the rule. But the
middle bucket drops below the freshest bucket while holding 278 pages against 29,601. I'd call that
**mixed**, not confirmed — and I'd weight it lightly, because a test run on a quarter of the rows,
where the exclusion is caused by a defect rather than by chance, isn't a sample I can reason about.
The honest verdict on staleness is *not yet tested*.

**Traffic volume — runs backwards.**

| Prior-30d impressions | Decline rate | Pages |
|---|---:|---:|
| Low | 0.342 | 39,321 |
| Moderate | 0.299 | 33,103 |
| Good | 0.226 | 33,175 |
| Excellent | 0.204 | 14,908 |

This one is whole: those four buckets sum to 120,507, every row accounted for. And it's monotonic in
the opposite direction to the assumption. High-traffic pages decline *less*. So the "visible" half of
the rule isn't finding pages at risk — it's finding the pages least likely to be at risk, and it's
doing it consistently across the full dataset.

That reframes what the rule is for. It isn't a risk filter, it's a value filter: it says "if this
page does slip, it matters." That's a defensible thing to want. It's just not what the rule was
described as doing, and the difference changes how you'd tune it.

**What this doesn't say:** these are observed associations on two months of one panel. Declining
pages aren't declining *because* of their traffic level, and I haven't controlled for anything. The
volume result stands on all 120,507 rows; the staleness result stands on 26% of them and should be
re-run once `days_since_update` is fixed.

---

## 5. About

> I'm Muneeb Ur Rehman. I'm an ML intern on FlyRank's Applied Search Intelligence track, working on
> one question: out of 120,000 pages, which fifty should an editor open this week?
>
> Most of what I've learned so far is about not fooling myself. I've had a model score a perfect
> 1.000 AUC and had to work out that it was reading the answer off its own inputs. I've had a
> feature turn out to be measuring nothing for a large share of rows, and found it by chasing three
> wrong predictions instead of celebrating zero. Every number I report comes with the split it was
> measured on, because a number without a split is a guess with a decimal point.
>
> Python, pandas, scikit-learn, DuckDB over Parquet, Colab, git. I write things down so someone
> else can re-run them.
>
> I'm looking for a junior data or ML role on a small team, where I'd be close enough to the
> decision to know whether the model actually helped.

**Short version, for a header or a LinkedIn line:**

> Muneeb Ur Rehman — ML intern working on search-content ranking. I report the split with the number.

---

## 6. Contact / CTA

> ### If this looks like the kind of thinking your team needs, email me.
>
> I'll send the notebooks — they run top to bottom, numbers included.
>
> **[muneebkhokher38@gmail.com](mailto:muneebkhokher38@gmail.com)** · [GitHub](https://github.com/muneeb-khokhar/flyrank-ml-track)

One action, one address, on every page. No form, no calendar link, no newsletter.

---

## 7. Before / after

**Before — generic AI first draft:**

> As a results-driven ML intern, I leveraged cutting-edge machine learning techniques to build a
> powerful content prioritization engine, driving significant impact by helping content teams
> seamlessly identify high-value optimization opportunities at scale and unlock measurable SEO
> growth.

**After — my edit:**

> I built a ranked review queue for a content team with 120,000 pages and time for fifty. Held out
> one client at a time, it beat that client's own base rate for 21 of 24 scoreable clients, averaging
> 2.17×. I report that instead of my first number, which looked better and turned out to be a draw of
> nine clients.

What changed and why:

- **"Results-driven", "cutting-edge", "powerful", "significant", "seamlessly"** — five adjectives
  carrying no information. A hiring manager has read all of them a hundred times today.
- **"Drove impact at scale"** → the actual scale: 120,000 pages, fifty reviewed. "At scale" is a
  word you use when you don't have the number.
- **"Unlock measurable SEO growth"** → cut entirely. I didn't measure growth. I measured queue
  precision. Claiming growth is claiming an experiment I never ran.
- **Named the validation design.** "Held out one client at a time" is the difference between a
  number a reviewer can check and one they have to take on faith. A bare decimal with no split named
  is a number any reviewer worth working for will assume was cherry-picked.
- **Reported the worse number.** The last sentence is the only line a generic draft would never
  produce — no AI first draft volunteers that its headline figure was one lucky split. It's also the
  only line that says something true about how I work.

**Words cut from the whole document on the read-aloud pass:** passionate, journey, robust,
state-of-the-art, deep dive, actionable insights, game-changing, empowering, holistic, synergy,
best-in-class, "I'm excited to".

---

## Read-aloud checklist

- [ ] Every case names a decision a person makes, not a technology I used.
- [ ] Every number has its sample size or its split next to it.
- [ ] Every case has one sentence about what it can't claim.
- [ ] Nothing here would be true of anyone else's project.
- [ ] One audience, one action, on every page.
- [ ] I can say each line out loud to someone who'll push back.
