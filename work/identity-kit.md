# Identity kit

Muneeb Ur Rehman · ML · Search Intelligence · v1

<img src="identity/logo-wordmark.svg" alt="Muneeb Ur Rehman — ML, Search Intelligence" width="420">

> **Quiet system, loud work.** Two fonts, four colours, one mark — all chosen to sit still so that a
> number on the page is the thing you notice.

The rendered version, with the real fonts loaded, is [`work/identity/index.html`](identity/index.html).
Open it in a browser; GitHub's markdown viewer substitutes its own type.

---

## Type

Two fonts, four weights total. Both free, both Google Fonts, both SIL Open Font License.

| | Font | Used for |
|---|---|---|
| **Heading** | **Space Grotesk** | Headings, the wordmark, and every number |
| **Body** | **Inter** | Body copy and small labels |

| Role | Size / weight | Detail |
|---|---|---|
| Page title | 34px · 600 | letter-spacing −0.02em |
| Case title | 19px · 600 | letter-spacing −0.01em |
| Section label | 13px · 600 | uppercase, +0.12em |
| Body | 16px · 400 | line-height 1.6, max 62 characters |
| Small label | 11px · 600 | uppercase, +0.14em |
| Numbers | Space Grotesk 600 | tabular figures, so digits align between cards |

Inter is here for one specific reason: it holds up at 11px on a phone, which is where the one
visitor who matters is reading.

---

## Palette

Four colours. Measured contrast, not estimated — computed against Paper with the WCAG
relative-luminance formula.

| Role | Hex | Job | Contrast on Paper |
|---|---|---|---|
| **Ink** | `#14161A` | All text | 17.35:1 |
| **Paper** | `#FBFAF7` | Every background — warm, not white | — |
| **Slate** | `#2F4858` | Main colour: rules, labels, the mark | 9.19:1 |
| **Signal** | `#A8461F` | Accent: links and the one CTA, nothing else | 5.65:1 |

Every pair above clears 4.5:1 for normal text. **Never Slate on Ink** — 1.89:1, the one combination
in this palette that fails, and the one a careless dark section would reach for.

---

## Mark

<img src="identity/favicon.svg" alt="MR monogram" width="64"> <img src="identity/favicon.svg" alt="" width="32"> <img src="identity/favicon.svg" alt="" width="16">

Initials in the heading font on a Slate square, with a single Signal rule beneath. That rule is the
only decoration in the entire system, and it earns its place by being what survives at 16px.

Files: [`identity/favicon.svg`](identity/favicon.svg) · [`identity/logo-wordmark.svg`](identity/logo-wordmark.svg)

Before production, convert the monogram text to outlines so it renders identically where Space
Grotesk isn't loaded.

---

## Style note (two lines)

> Space Grotesk for headings and numbers, Inter for body and labels; Ink `#14161A` on Paper
> `#FBFAF7`, Slate `#2F4858` for structure, Signal `#A8461F` for links and the single call to action.
>
> Calm, technical, and unfussy — the page should feel like a well-kept lab notebook, so the numbers
> and the honest caveats are the loudest things on it.

### The version that goes in the Claude Project

```
Build everything in this system.

TYPE   Headings + numbers: Space Grotesk 600. Page title 34px/-0.02em,
       case title 19px, section label 13px uppercase +0.12em.
       Body + labels: Inter. Body 16px/1.6, small label 11px
       uppercase +0.14em. Max measure 62 characters.
       Numbers use tabular figures so digits align between cards.

COLOUR Text #14161A. Background #FBFAF7. Structure - rules, labels,
       the mark - #2F4858. Links and the one CTA #A8461F, and nothing
       else. Never #2F4858 on #14161A (1.89:1).

SPACE  56px between sections, 24px inside cards, 14px between a
       heading and its paragraph. When unsure, add space rather than
       a border, and a border rather than a background.

MOOD   Calm, technical, unfussy - a well-kept lab notebook. No
       gradients, no shadows beyond a hairline border, no icons, no
       decoration that isn't load-bearing. The numbers are the
       loudest thing on the page.
```

---

## Rules this system lives by

- One accent, used twice per page at most. If Signal is everywhere, nothing is signalled.
- Space before borders, borders before backgrounds. Most separation problems are spacing problems.
- Numbers get the heading font and tabular figures. They're the evidence; they should look like it.
- No gradient, no shadow deeper than a hairline, no icon set. Nothing decorative that isn't doing a job.
- If a colour choice needs a paragraph of justification, it's the wrong colour.

---

## Why this and not something else

The voice card on my case studies says *plain, specific, honest about the limits*. A portfolio that
says that in words and then arrives in gradients and drop shadows is arguing with itself. So the
system is deliberately close to a lab notebook: warm paper, one structural colour, one accent held
in reserve for the single thing I want clicked.

Signal is the only warm colour, and it appears twice per page at most — once on a link, once on the
CTA. It's there so that when a hiring manager's eye lands on something orange, it's the thing I
wanted them to land on.
