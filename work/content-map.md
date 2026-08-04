# The through line — claim, content map, gather list

Muneeb Ur Rehman · ML · Search Intelligence

**The one person:** a hiring manager at a small data team, deciding whether to spend 45 minutes
interviewing me.
**The one action:** email me — `muneebkhokher38@gmail.com`.

Every call to action on every page is that same email. There is no second ask.

---

## 1. The one-line claim

### The ten I generated

1. I build models on messy real data and know their limits.
2. I rank what a team should look at first, and say when the ranking is wrong.
3. I turn 120,000 pages into the fifty worth an editor's morning.
4. I find the pages losing traffic before anyone notices.
5. I make models that survive a skeptic.
6. I threw away a perfect score because it was cheating. That's the job.
7. I build decision-support you can argue with.
8. Search-content models, honest numbers, and the split they were measured on.
9. I put the right fifty pages in front of an editor, and show my working.
10. I build ranking models and report the number that isn't flattering.

### Choosing

Most of these fail one of two ways. **1, 5, 7, 8** describe a posture, not a result — any junior
candidate could paste them onto any portfolio, which makes them worth nothing. **6** is the most
memorable sentence on the list and I rejected it: opening a portfolio by announcing a failure asks
the reader to trust me before I've given them a reason.

**3** was the only one carrying a real number and a real job. It fails on one thing — it says
nothing about judgment, which is half of what I'm claiming.

### Sharpening

> **v1** — I turn 120,000 pages into the fifty worth an editor's morning.
> **v2** — I turn 120,000 pages into the fifty worth an editor's morning, and I tell you how often that ranking is wrong.
> **final** ↓

## → **I turn 120,000 pages into the fifty worth an editor's morning — and I tell you when I'm wrong.**

Two clauses, one job each. The first is the work and carries a number a reader can picture. The
second is the differentiator: everyone's portfolio says the model worked, almost none say when it
didn't. v2 said "how often that ranking is wrong," which is more precise and slower to read; "when
I'm wrong" is the version I'd actually say out loud.

---

## 2. Content map

Five pages. Home carries the whole argument for a 30-second skimmer; the three case pages exist for
the reader who wants depth before emailing.

### Page 1 — Home `/`

| # | Section | Contains | Image |
|---|---|---|---|
| 1 | Hero | The claim, one supporting line, primary CTA | `hero-texture.svg` |
| 2 | **Case 1 summary** — The review queue that beat the rule | Title, one-line summary, the LOCO headline as **"21 of 24 held-out clients, 2.28× mean lift"** (never a single-split decimal — see note below), three beats compressed to one line each, "Read the full case →" | `fig-queue-precision.svg` |
| 3 | Case 2 summary — The model that scored 1.000 and was worthless | Same shape, stat pair `1.000 / 0.486` | `fig-leaky-vs-honest.svg` |
| 4 | Case 3 summary — Two assumptions behind the rule, tested | Same shape, stat pair `0.342 → 0.204` | `fig-volume-vs-decline.svg` |
| 5 | About (short) | Three sentences from the bio + headshot | `headshot.jpg` |
| 6 | Contact | The claim restated in one line, then the CTA | — |

**CTA:** *Email me* — in the hero and repeated at section 6. Twice on the page, nowhere else.

**Why Case 1 leads:** it carries the whole three-act validation story in one case — I caught a
target leak, then found my own "final" metric was unstable and rebuilt evaluation as
leave-one-client-out, then found the rebuilt evaluation had its own silent reproducibility bug and
pinned the window. Case 2 is the sharper single story about honesty, but as an opener it asks the
reader to admire a failure before they know I can ship. It earns more in position 3, once Case 1 has
bought the credibility.

**No single-split decimal anywhere on the site.** `0.500` on one seed-42 split became `0.30–0.62`
across seven seeds — it was one draw, not a measurement. So the cards and the hero carry the LOCO
result (21 of 24 held-out clients, 2.28× mean lift), and the single-split table appears only inside
the case page, explicitly labelled as the thing that *prompted* the audit rather than a co-equal
result. The through-line for the whole site: **every number that follows exists because an earlier
number made me suspicious of itself.**

### Page 2 — Case 1 `/cases/review-queue`

| # | Section |
|---|---|
| 1 | Title + stat pair + one-line summary |
| 2 | The problem |
| 3 | What I did, and what I decided — the three defended decisions |
| 4 | What came of it — LOCO first (21/24, 2.28×, 10 outside the 95% band all positive), then the single-split table labelled as the trigger, then the date-pinning bug |
| 5 | The receipts — `capture-w05-results.png` (**must be re-captured post-pin**) and the `w06` LOCO output once committed |
| 6 | What this doesn't say |
| 7 | CTA |

**CTA:** *Email me.* Secondary, not competing: "the notebook is in the repo" as an inline link.

### Page 3 — Case 2 `/cases/leakage-trap`

Same seven sections. Section 4 is the two-row AUC table; section 5 is
`capture-w03-leakage.png`.

### Page 4 — Case 3 `/cases/testing-the-rule`

Same seven sections, with one addition at 4: both tables, and the note that the staleness table
covers 26% of rows because `pd.cut` dropped the negatives. Section 6 carries more weight here than
anywhere else on the site.

### Page 5 — About `/about`

| # | Section |
|---|---|
| 1 | Headshot + the claim |
| 2 | Bio — the full version, not the three-sentence cut |
| 3 | How I work — the voice card and what it means in practice |
| 4 | Tools — Python, pandas, scikit-learn, DuckDB over Parquet, git |
| 5 | What I'm looking for — junior data/ML role on a small team |
| 6 | CTA |

**CTA:** *Email me.*

### The ladder

Every CTA on all five pages is the same mailto. Case pages point at Home only through the nav; they
never route to each other, because a reader deep in a case is closer to emailing than to reading a
second case. Nothing on the site asks for a newsletter signup, a calendar booking, or a LinkedIn
follow — those would be second actions competing with the one that matters.

---

## 3. Still need to gather

Honest list, so build week isn't blocked by a surprise.

### Have it

- All nine images — three figures, two notebook captures, headshot, hero texture, favicon, wordmark
- Case copy for all three cases, edited
- Bio, contact copy, voice card
- Identity kit — fonts, hex codes, spacing, the mark
- Public repo link

### Need it, and it exists — just needs doing

| Item | For | Blocker |
|---|---|---|
| ~~Deployed site URL~~ | Everything | **Done** — live at `https://muneeb-khokhar.github.io/`, verified on a second device |
| Custom domain | Nav, contact | Optional; the github.io URL is fine for now |
| `favicon.ico` fallback | Older browsers | 5 minutes from the SVG |
| Monogram converted to outlines | The mark rendering off-site | Space Grotesk isn't loaded outside the site |

### Need it, and it does not exist yet

| Item | For | Status |
|---|---|---|
| **Re-run `w05_model` under the pinned window** | Case 1's single-split table, and the screenshot | **Blocking.** The committed notebook and `capture-w05-results.png` still show the pre-pin `0.180 / 0.620`; the case now reports `0.200 / 0.500`. A receipt that disagrees with the write-up is worse than none |
| **Re-capture `capture-w05-results.png`** | Case 1 | Follows directly from the re-run above |
| **Run `w06_validation_audit` and commit its outputs** | Case 1's LOCO headline | The 21/24 and 2.28× figures are stated in the case but have no committed output behind them yet. The notebook is written; it needs one Colab run |
| **FlyRank policy on per-client detail** | Whether the LOCO table can be shown at all | **External blocker — ask a person, don't assume.** If per-client rows can't be published, the LOCO section becomes an aggregate finding described rather than shown, which reshapes the case page |
| **Case 4** — validation audit | A fourth case, or depth on Case 1 | ML-09 not started. The three rows above are its natural content |
| **Case 5** — the action playbook | Would be the most "hireable" case: model → recommendation | ML-10 not started |
| **Capstone paper + deployed URL** | The strongest single link on the site | Not written; `submission/paper_url.txt` is still the placeholder |
| Live demo of the ranked queue | Hero, Case 1 | Doesn't exist — would need a hosted app, not planned |
| Mentor testimonial | About page | Not asked for yet |

### Will never exist, and the site must not imply otherwise

- **Before/after traffic numbers from a real client.** The data is anonymized by design and
  `DATA_USE.md` forbids client-identifying detail. I can show queue precision; I cannot show that
  refreshing a page recovered its traffic, because I never ran that experiment.
- **A causal claim.** Everything on the site is observed, measured, directional, decision-support.

### One thing that will break during build week if I ignore it

Four notebooks — `w03_feature_leakage_check`, `w04_signal_audit`, `w06_validation_audit`,
`w07_action_playbook` — are untouched skeletons whose boilerplate comment cells exceed the CI's
200-character "looks filled in" threshold with no outputs. They pass today only because
`submission/paper_url.txt` still holds the placeholder. The moment I paste a real capstone URL
there, `smoke-test.yml` fails the build. Two of the four are retired cards and can be deleted; the
other two resolve when I do the work.

---

## What the map is actually enforcing

One claim, one audience, one action, repeated five times without variation. The strongest case
leads, the most memorable case sits where it can be believed, and the case with the biggest caveat
gets the most space for that caveat. Nothing on the site asks the reader to do anything except send
one email.
