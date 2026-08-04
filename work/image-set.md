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
| 3 | Case 1 | Notebook capture — the results table in `w05_model` | **Real screenshot** | ⬜ you capture |
| 4 | Case 2 | Leaky 1.000 vs honest 0.486 | Figure from my committed numbers | ✅ `images/fig-leaky-vs-honest.svg` |
| 5 | Case 2 | Notebook capture — the two AUC prints in `w03_data_contract` | **Real screenshot** | ⬜ you capture |
| 6 | Case 3 | Decline rate by traffic volume | Figure from my committed numbers | ✅ `images/fig-volume-vs-decline.svg` |
| 7 | About | Headshot | **Real photo** | ⬜ you supply |
| 8 | Site-wide | Favicon / monogram | Generated (SVG) | ✅ `identity/favicon.svg` |
| 9 | Site-wide | Wordmark | Generated (SVG) | ✅ `identity/logo-wordmark.svg` |

Six of nine are done. The three open ones are the three that **cannot** be generated — two real
captures and one real photo. That split is the point of the assignment, so I've left them open
rather than filling them with something that looks close enough.

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

**Items 3 and 5 have to be actual screenshots** — a figure I drew is my rendering of my numbers; a
screenshot of the notebook is evidence the code ran and produced them. The figure is the legible
version, the screenshot is the receipt. A case card gets the figure; the case body links the
screenshot.

**Item 7 has to be a real photo of me.** A generated portrait on an About page is the one lie that
invalidates everything around it — if the face is fake, a reader is entitled to assume the metrics
are too. Bad light and a plain wall beat a flawless synthetic face.

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
  hero-texture.svg               keeper · hero
  _rejected-hero-gradient.svg    rejected, kept as evidence
  contact-sheet.html             all five, side by side
work/identity/
  favicon.svg                    keeper · site-wide
  logo-wordmark.svg              keeper · site-wide
```

**Still to capture:** two notebook screenshots (`w05_model` results table, `w03_data_contract` AUC
prints) and one real headshot. Crop tight, keep the text legible at the width it'll actually be
shown, and don't scale a screenshot up.

**One known limitation:** the SVGs name Space Grotesk and Inter with a system fallback, so they'll
render in a substitute face anywhere those fonts aren't loaded. Fine on the site, where the kit
loads them; convert the text to outlines before using any of these standalone.
