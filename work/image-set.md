# Image set

Muneeb Ur Rehman · ML · Search Intelligence

Every image the portfolio needs, what it's for, and whether it's a real capture, a figure from my
own data, a generated asset, or a real photo. Preview them all at
[`images/contact-sheet.html`](images/contact-sheet.html).

---

## 1. What the portfolio actually needs

Mapped to the content map — hero, three cases, about, contact.

| # | Where | Image | Source | Status |
|---|---|---|---|---|
| 1 | Hero | Ruled-grid texture with a ranked queue | Generated (SVG, my palette) | ✅ `images/hero-texture.svg` |
| 2 | Case 1 | Precision@50, four methods compared | Figure from my committed numbers | ✅ `images/fig-queue-precision.svg` |
| 3 | Case 1 | Notebook capture — the results table in `w05_model` | **Real screenshot** | ✅ `images/capture-w05-results.png` |
| 4 | Case 2 | Leaky 1.000 vs honest 0.486 | Figure from my committed numbers | ✅ `images/fig-leaky-vs-honest.svg` |
| 5 | Case 2 | Notebook capture — the two AUC prints in `w03_data_contract` | **Real screenshot** | ✅ `images/capture-w03-leakage.png` |
| 6 | Case 3 | Decline rate by traffic volume | Figure from my committed numbers | ✅ `images/fig-volume-vs-decline.svg` |
| 7 | About | Headshot | **Real photo** | ✅ `images/headshot.jpg` |
| 8 | Site-wide | Favicon / monogram | Generated (SVG) | ✅ `identity/favicon.svg` |
| 9 | Site-wide | Wordmark | Generated (SVG) | ✅ `identity/logo-wordmark.svg` |

All nine are done. Three of them — the two notebook captures and the headshot — could only ever be
real, and that split is the point of the assignment.

---

## 2. Where I chose a real capture over AI

**The work itself is never generated.** Every number in every figure traces to a committed cell
output:

| Figure | Numbers come from |
|---|---|
| `fig-queue-precision` | `w05_model.ipynb` — 0.161 / 0.180 / 0.260 / 0.620 on the 21,610-row grouped split |
| `fig-leaky-vs-honest` | `w03_data_contract.ipynb` — 1.000 leaky, 0.486 honest, 46,016 items |
| `fig-volume-vs-decline` | `w04_baseline_score.ipynb` — four buckets summing to all 120,507 pages |

These are **figures plotted from my results**, not screenshots and not AI images. I'm calling that
out because "AI-generated chart" and "chart drawn from real data" look identical at a glance, and
the difference is the entire claim my portfolio makes.

**Items 3 and 5 are actual screenshots** — a figure I drew is my rendering of my numbers; a
screenshot of the notebook is evidence the code ran and produced them. The figure is the legible
version, the screenshot is the receipt. A case card gets the figure; the case body links the
screenshot.

Both were captured from the notebooks as they render on GitHub, then cropped to the cell and its
output — no browser chrome, no file tree, no scaling up. They're worth checking against the
figures: `capture-w05-results.png` reads `0.161499 / 0.180000 / 0.260000 / 0.620000`, which is the
Case 1 table; `capture-w03-leakage.png` reads `60,333 | 46,016`, honest `0.486`, leaky `1.000`,
which is Case 2. The receipts and the write-ups agree, which is the only reason to publish either.

**Item 7 is a real photo of me.** A generated portrait on an About page is the one lie that
invalidates everything around it — if the face is fake, a reader is entitled to assume the metrics
are too.

I picked between two real photos rather than reaching for a generator. The first had sunglasses and
a saturated red studio background: better lit, and wrong twice over — an About photo exists so a
stranger can put a face to the work, which hidden eyes defeat, and a red field would have been the
loudest thing on a page whose palette is built to make the numbers loudest. The one I kept is a
phone photo in daylight, cropped to head-and-shoulders so the parked car and roadworks behind me
fall outside the frame. Worse photo, right photo.

---

## 3. Generated assets, and the one style they share

Only the connective tissue is generated: the hero texture, the monogram, and the wordmark.

They're a set by construction rather than by luck — all three are hand-built SVG on the same four
tokens (Ink `#14161A`, Paper `#FBFAF7`, Slate `#2F4858`, Signal `#A8461F`), the same 4px corner
radius, the same one-accent rule, no gradients and no shadows anywhere. I used SVG rather than a
diffusion model deliberately: a generated raster hero would need re-prompting to hold the palette,
and would still drift. Geometry doesn't drift.

The hero texture is a faint ruled grid with a descending row of bars — a ranked queue, which is
literally what my work outputs. The top three bars are Signal; the rest fade into Slate. It reads
as texture at a glance and as a queue if you look, and it never competes with the headline on top
of it.

**Palette check, computed not eyeballed.** Slate and Signal appear together in
`fig-queue-precision`, so I ran the adjacent pair through OKLab ΔE:

| | ΔE | Floor | |
|---|---:|---:|---|
| Normal vision | 22.11 | 15 | pass |
| Deuteranopia | 33.16 | 8 | pass |
| Protanopia | 28.90 | 8 | pass |
| Tritanopia | 20.35 | 8 | pass |

Nothing in the set depends on colour alone: every bar is directly labelled with its value, so the
figures still read in greyscale or print.

---

## 4. What I rejected, and why

### Rejected: the gradient-mesh hero

Kept in the repo as [`images/_rejected-hero-gradient.svg`](images/_rejected-hero-gradient.svg) so
the rejection is checkable rather than asserted.

It's the default answer to "portfolio hero" — a blurred Signal-to-Ink gradient with soft orbs and
flowing lines. It is, honestly, the better-looking image of the two. I rejected it for three
reasons:

1. **It breaks the system it's supposed to belong to.** My style note bans gradients and shadows in
   the first line. An asset that violates the kit isn't connective tissue, it's a second design
   language on the same page.
2. **It puts the loudest thing on the page in the wrong place.** The palette exists so that the
   numbers are the loudest element. A full-bleed saturated gradient at the top guarantees the first
   thing a hiring manager's eye lands on is decoration.
3. **It's anonymous.** It would sit equally well on a crypto landing page, a yoga studio, or a
   consultancy. It says nothing about ranking pages. The one I kept is a picture of my actual
   output; this is a picture of nothing.

The tell was that I liked it. It was the more impressive image and the less useful one, and on a
page whose whole argument is restraint, "impressive" is the wrong axis.

### Rejected: the five charts already sitting in `outputs/charts/`

`action_mix.svg`, `confidence_mix.svg`, `top_feature_importance.svg`, `top_reason_codes.svg`,
`trend_distribution.svg` — five clean, finished, portfolio-ready charts, already in the repo.

I checked their provenance before using them:

```
git log --format='%h %an %s' -- outputs/charts
a486771 Initial commit
```

They came with the starter template. They're the reference pipeline's output on the bundled 30k
sample, not my work — and the numbers in them (Precision@50 0.240 → 0.740) are not my numbers,
which are 0.180 → 0.620 on a different split of a different dataset.

Using them would have been the single most damaging thing in this whole set: real-looking captures
of results I didn't produce, on a portfolio that argues I'm careful about exactly this. They're
excluded, and it took one `git log` to know.

---

## 5. Files

```
work/images/
  fig-queue-precision.svg        keeper · Case 1
  fig-leaky-vs-honest.svg        keeper · Case 2
  fig-volume-vs-decline.svg      keeper · Case 3
  capture-w05-results.png        keeper · Case 1 receipt (1515x700, real capture)
  capture-w03-leakage.png        keeper · Case 2 receipt (1530x760, real capture)
  headshot.jpg                   keeper · About (1000x1221, real photo)
  hero-texture.svg               keeper · hero
  _rejected-hero-gradient.svg    rejected, kept as evidence
  contact-sheet.html             the whole set, side by side
work/identity/
  favicon.svg                    keeper · site-wide
  logo-wordmark.svg              keeper · site-wide
```

Nothing outstanding. The full-resolution original of the headshot is kept outside the repo — the
committed file is the cropped 202 KB version, because a 7 MB phone photo has no business in git.

**One known limitation:** the SVGs name Space Grotesk and Inter with a system fallback, so they'll
render in a substitute face anywhere those fonts aren't loaded. Fine on the site, where the kit
loads them; convert the text to outlines before using any of these standalone.
