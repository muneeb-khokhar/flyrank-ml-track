# Prompt iteration log — building the case-studies section

Muneeb Ur Rehman · FlyRank · Front-end AI Engineering track

---

## The task

**Build the case-studies section of my portfolio site.**

This comes straight off my FL-01 audit. FL-01 was *Environment and AI toolchain* — setting up the
stack and naming what I'd actually use AI for. The FE track's first project type is "a personal
website with responsive pages, polished sections, and a public link," and the section that does the
work on that site is the one holding my three case studies. I already wrote the copy for those
cases. Turning that copy into a responsive component is the task I repeat every time I add a case,
which is what makes it worth engineering a prompt for instead of retyping one.

**Stack:** React + Tailwind, single file, no dependencies.
**Real constraint:** the reader is a hiring manager skimming on a phone for about 30 seconds.

**The five techniques, one per version:**

| Version | Technique | Why I reached for it there |
|---|---|---|
| V0 | — | The one-liner I'd have typed a month ago |
| V1 | Role assignment | V0's markup was `<div>` soup with no accessibility at all |
| V2 | Context and motivation | V1 built a beautiful generic site for nobody in particular |
| V3 | Few-shot examples | V2 had the right structure filled with lorem ipsum |
| V4 | Output structure | V3 copied my example instead of generalising from it |
| V5 | Step decomposition | V4 was drop-in but shipped real responsive and a11y bugs |

---

## V0 — the naive prompt

### Prompt

```
Build me a portfolio website
```

### Output (excerpt)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>John Doe | Full Stack Developer</title>
  <style>
    .hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .skill-bar { height: 8px; background: #eee; border-radius: 4px; }
  </style>
</head>
<body>
  <div class="hero">
    <h1>Hi, I'm John Doe</h1>
    <p>A passionate Full Stack Developer creating beautiful digital experiences</p>
    <button>View My Work</button>
  </div>

  <div class="section">
    <h2>Skills</h2>
    <div class="skill"><span>HTML/CSS</span><div class="skill-bar"><div style="width:90%"></div></div></div>
    <div class="skill"><span>JavaScript</span><div class="skill-bar"><div style="width:85%"></div></div></div>
    <div class="skill"><span>React</span><div class="skill-bar"><div style="width:80%"></div></div></div>
  </div>

  <div class="section">
    <h2>Projects</h2>
    <div class="card"><h3>Project One</h3><p>Lorem ipsum dolor sit amet, consectetur...</p></div>
    <div class="card"><h3>Project Two</h3><p>Lorem ipsum dolor sit amet, consectetur...</p></div>
  </div>

  <div class="section">
    <h2>Contact</h2>
    <form><input placeholder="Name"><input placeholder="Email"><textarea></textarea>
    <button>Send Message</button></form>
  </div>
</body>
</html>
```

### Notes

**What changed in the prompt:** Nothing — baseline.

**What actually changed in the output:** n/a, but worth naming what it produced. Five sections I
didn't ask for, a purple gradient, and a skills bar claiming I'm 85% at JavaScript — a number that
means nothing and that a hiring manager cannot verify. The projects are lorem ipsum. The contact
form posts nowhere. It's `<div>` soup: not one `<section>`, `<main>`, or `<nav>` in the file. It's
also plain HTML with an inline `<style>` block, when my stack is React and Tailwind — it had no way
to know, because I didn't say.

**What still failed:** All of it. The single worst part is the skills bars, because they're
confidently wrong rather than merely empty — I'd have had to notice and delete them.

**What I'd try next:** Tell it who it's supposed to be. The markup quality is the most mechanical
problem and a role should fix it.

---

## V1 — role assignment

### Prompt

```
You are a senior front-end engineer who ships accessible, responsive marketing pages.
You write semantic HTML with Tailwind utility classes and you optimise for a
first-time visitor arriving on a phone.

Build me a portfolio website.
```

**Technique:** role assignment. Nothing else added.

### Output (excerpt)

```jsx
<a href="#main" className="sr-only focus:not-sr-only focus:absolute focus:p-3">
  Skip to content
</a>

<main id="main">
  <section aria-labelledby="work-heading" className="px-5 py-12 sm:px-8 md:py-20">
    <h2 id="work-heading" className="text-2xl font-semibold tracking-tight sm:text-3xl">
      Selected work
    </h2>
    <ul className="mt-8 grid gap-6 sm:grid-cols-2">
      <li className="rounded-lg border border-slate-200 p-5">
        <h3 className="text-lg font-medium">Project One</h3>
        <p className="mt-2 text-sm leading-relaxed text-slate-600">
          A short description of the project and the problem it solved.
        </p>
      </li>
      ...
```

### Notes

**What changed in the prompt:** One layer — a role.

**What actually changed in the output:** The markup became real. `<div>` soup turned into `<main>`,
`<section aria-labelledby>`, and a `<ul>` of cards — a list is genuinely the right element for a
list of projects and V0 didn't get there. It added a skip link and `focus:` styles unprompted, moved
to mobile-first Tailwind (base styles, then `sm:`/`md:`), and dropped the fixed pixel widths. It
also quietly switched to JSX, having inferred React from "Tailwind utility classes."

**What still failed:** It's a well-built site for nobody. Still five sections, still a skills block
(now an accessible one, which is worse — it's a well-marked-up meaningless claim), still "Project
One" and a description-shaped placeholder. The role improved *how* it builds and changed nothing
about *what* it builds.

**What I'd try next:** Tell it who's reading and what the page has to achieve. A role fixed the
craft; only context can fix the content.

---

## V2 — context and motivation

### Prompt

```
[V1 prompt, unchanged, plus:]

This is for a junior ML engineer's portfolio. The one visitor who matters is a
hiring manager at a small data team deciding whether to spend 45 minutes on an
interview. They will skim on a phone for about 30 seconds. The page has one job:
make them believe I build models on messy real data and know their limits.
```

**Technique:** context and motivation.

### Output (excerpt)

```jsx
// Two sections. At 30 seconds of phone skimming, a five-section site spends the
// reader's attention on navigation instead of evidence.

<section aria-labelledby="cases-heading" className="px-5 py-12">
  <h2 id="cases-heading" className="text-2xl font-semibold">
    Three things I built, and what they cost me to learn
  </h2>

  <ol className="mt-8 space-y-8">
    <li className="border-l-2 border-slate-900 pl-5">
      <h3 className="text-lg font-medium">[Case title — lead with the surprising result]</h3>
      <dl className="mt-3 space-y-2 text-sm">
        <dt className="font-medium text-slate-900">The problem</dt>
        <dd className="text-slate-600">[What was broken or unknown]</dd>
        <dt className="font-medium text-slate-900">What I did</dt>
        <dd className="text-slate-600">[The decision, not the tooling]</dd>
        <dt className="font-medium text-slate-900">What came of it</dt>
        <dd className="text-slate-600">[The number, and what it cannot claim]</dd>
      </dl>
    </li>
```

### Notes

**What changed in the prompt:** One layer — audience, time budget, and what the page must prove.

**What actually changed in the output:** The skills bars are gone, and it said why in a comment:
a hiring manager can't verify a percentage. Five sections collapsed to two. It picked `<dl>` for the
three beats, which is a better call than my own copy doc makes — the beats genuinely are
term/description pairs. The placeholder text changed character too: V1 wrote "A short description of
the project," V2 wrote "[The decision, not the tooling]" and "[The number, and what it cannot
claim]" — the placeholders started coaching me toward the content the audience needs.

**What still failed:** Still no actual content. And the section heading it invented — "Three things
I built, and what they cost me to learn" — is doing a voice I never authorised. It's not bad, it's
just not mine, and I'd have shipped it without noticing if I weren't reading closely.

**What I'd try next:** Give it a real case so it stops guessing at tone.

---

## V3 — few-shot examples — *this one went backwards*

### Prompt

```
[V2 prompt, unchanged, plus:]

Here is one of the three cases, in full, so you can see the shape and the tone:

Title: The model that scored 1.000 and was worthless
Summary: A perfect AUC that turned out to be the model reading its own answer.
Problem: Before building features against a 9.8M-row partition, I had to write
  down the data contract — and the tempting move is to write it, believe it, and
  move on.
What I did: I verified every claim with a query instead of a sentence, then
  deliberately trained a second model with the column my label is derived from,
  to see what cheating would look like.
What came of it: Leaky AUC 1.000, honest AUC 0.486. I kept the 0.486.
Numbers: 1.000 leaky AUC / 0.486 honest AUC
```

**Technique:** few-shot examples.

### Output (excerpt)

```jsx
<ol className="mt-8 space-y-10">
  <li>
    <h3>The model that scored 1.000 and was worthless</h3>
    <p className="mt-1 text-slate-600">A perfect AUC that turned out to be the model
      reading its own answer.</p>
    <div className="mt-4 flex gap-6">
      <div><span className="block text-2xl font-semibold tabular-nums">1.000</span>
        <span className="text-xs uppercase tracking-wide text-slate-500">leaky AUC</span></div>
      <div><span className="block text-2xl font-semibold tabular-nums">0.486</span>
        <span className="text-xs uppercase tracking-wide text-slate-500">honest AUC</span></div>
    </div>
    ...
  </li>

  <li>
    <h3>The feature that scored 0.910 and was worthless</h3>
    <p className="mt-1 text-slate-600">A perfect F1 that turned out to be the feature
      reading its own answer.</p>
    <div className="mt-4 flex gap-6">
      <div><span className="block text-2xl font-semibold tabular-nums">0.910</span>
        <span className="text-xs uppercase tracking-wide text-slate-500">leaky F1</span></div>
```

### Notes

**What changed in the prompt:** One layer — one complete worked example.

**What actually improved in the output:** The tone landed. Headings stopped being motivational and
started being flat and factual, matching my copy. Better than that, it turned the numbers into a
visual element I hadn't asked for and now want — a stat pair with `tabular-nums` so the digits align
between cards. That's a real design decision the earlier versions never reached.

**What went backwards — and this is the version that got worse.** It read the example as a template
instead of as one instance. Cases 2 and 3 came back as near-copies of case 1 with the nouns swapped:
"The model that scored 1.000 and was worthless" became "The feature that scored 0.910 and was
worthless," same sentence rhythm, same "reading its own answer" clause. And 0.910 is invented. There
is no 0.910 anywhere in my work — it generated a plausible-looking metric to fill the slot the
example taught it to expect. The content is also hardcoded into the JSX, so adding a fourth case
means editing markup.

One rich example bought me the tone and cost me generalisation. If I'd skimmed this output I'd have
shipped a fabricated number onto a page whose entire claim is that I'm honest about numbers, which
is the most expensive possible place to make that mistake.

**What I'd try next:** Make the example structurally impossible to copy — force the content into
data and leave the component with nothing to hardcode.

---

## V4 — output structure

### Prompt

```
[V3 prompt, unchanged, plus:]

Output structure:
- Put the case content in a `cases` array at the top, separate from the
  presentational component. The example above is data, not a template — the
  component must render any case in that shape.
- Tailwind utility classes only. No external dependencies, no icon libraries,
  no images.
- One file, default export, no TypeScript.
- Return code only. No preamble, no explanation after.
```

**Technique:** output structure.

### Output (excerpt)

```jsx
const cases = [
  {
    title: "The model that scored 1.000 and was worthless",
    summary: "A perfect AUC that turned out to be the model reading its own answer.",
    beats: {
      problem: "Before building features against a 9.8M-row partition, I had to write down the data contract — and the tempting move is to write it, believe it, and move on.",
      did: "I verified every claim with a query instead of a sentence, then deliberately trained a second model with the column my label is derived from.",
      outcome: "Leaky AUC 1.000, honest AUC 0.486. I kept the 0.486.",
    },
    stats: [
      { value: "1.000", label: "leaky AUC" },
      { value: "0.486", label: "honest AUC" },
    ],
  },
  // TODO: add your remaining cases in this shape
];

function CaseCard({ item }) {
  return (
    <li className="border-l-2 border-slate-900 pl-5">
      <h3 className="text-lg font-medium tracking-tight">{item.title}</h3>
      <p className="mt-1 text-sm text-slate-600">{item.summary}</p>
      <div className="mt-4 flex gap-6">
        {item.stats.map((s) => (
          <div key={s.label}>
            <span className="block text-2xl font-semibold tabular-nums">{s.value}</span>
            <span className="text-xs uppercase tracking-wide text-slate-500">{s.label}</span>
          </div>
        ))}
      </div>
      ...
```

### Notes

**What changed in the prompt:** One layer — the shape of the return value.

**What actually improved in the output:** The fabricated 0.910 disappeared. That's the part worth
sitting with: I didn't tell it to stop inventing numbers, I told it to put content in an array, and
the invention stopped as a side effect. Once the example was one entry in a list rather than the
template for the whole section, it had somewhere honest to put "I don't have the other two" — a
`// TODO` comment — instead of filling the gap. The structural change removed the pressure to
fabricate.

The preamble also went. V3 opened with "Here's a beautiful, accessible portfolio section! ✨" and
closed with four paragraphs explaining Tailwind to me; V4 returned a file I could paste.

**What still failed:** It's drop-in and it's buggy. The heading order goes `h1` straight to `h3`
because the section heading is `h2` in a parent it can't see, so a screen-reader user hears a skipped
level. The two-stat row uses `flex gap-6` with no wrap — at 360px with a longer label the second stat
pushes out of the card. And `text-slate-500` on white for the stat labels is about 4.0:1, under the
4.5:1 minimum for text that size.

**What I'd try next:** Make it check its own work. Every one of those three is something it
demonstrably knows — it added a skip link unprompted in V1 — it just never looked back at what it
wrote.

---

## V5 — step decomposition

### Prompt

```
[V4 prompt, unchanged, plus:]

Work in these steps:
1. Restate the constraints you are building to, one line each.
2. Define the data shape for one case.
3. Build the single repeating unit (one case card).
4. Compose the section around it, including the responsive rules.
5. Self-check the result: heading order, colour contrast, tap-target size, what
   happens to long strings on a 360px screen, and whether a skimmer gets the gist
   in 30 seconds. Fix what you find, then return the final code.
```

**Technique:** step decomposition.

### Output (excerpt)

```jsx
// Step 5 — self-check, fixes applied:
// - Heading order: card titles were h3 under an h2 section heading, but this
//   component may mount without that h2. Made the heading level a prop
//   (default "h3") so the page owner controls the outline.
// - Long strings at 360px: stat row was `flex gap-6` with no wrap. Now
//   `flex flex-wrap gap-x-6 gap-y-3`, and titles get `break-words`.
// - Contrast: stat labels were text-slate-500 (~4.0:1). Moved to text-slate-600
//   (~5.7:1). Body summary was already compliant.
// - Tap targets: the card was not interactive, so nothing to fix. If you add a
//   link, give it `min-h-11` — I have not added one, because you did not ask
//   for a detail page and I don't know if one exists.
// - 30-second skim: title + stats are readable without touching the beats. The
//   three beats are visible rather than collapsed — a disclosure widget would
//   hide the strongest sentence behind a tap.

function CaseCard({ item, headingLevel: H = "h3" }) {
  return (
    <li className="border-l-2 border-slate-900 pl-5">
      <H className="text-lg font-medium tracking-tight break-words">{item.title}</H>
      <p className="mt-1 text-sm leading-relaxed text-slate-600">{item.summary}</p>

      <div className="mt-4 flex flex-wrap gap-x-6 gap-y-3">
        {item.stats.map((s) => (
          <div key={s.label}>
            <span className="block text-2xl font-semibold tabular-nums">{s.value}</span>
            <span className="text-xs uppercase tracking-wide text-slate-600">{s.label}</span>
          </div>
        ))}
      </div>

      <dl className="mt-5 space-y-3 text-sm">
        {BEATS.map(([key, label]) => (
          <div key={key}>
            <dt className="font-medium text-slate-900">{label}</dt>
            <dd className="mt-0.5 leading-relaxed text-slate-600">{item.beats[key]}</dd>
          </div>
        ))}
      </dl>
    </li>
  );
}
```

### Notes

**What changed in the prompt:** One layer — five named steps, the last one a self-check.

**What actually improved in the output:** All three V4 bugs are fixed, and one is fixed better than
I'd have fixed it. I'd have hardcoded `h3`; it made the heading level a prop, because a component
can't know what's above it on the page. That's the right answer and I didn't think of it.

`flex-wrap` plus `break-words` fixes the 360px overflow. `text-slate-600` clears 4.5:1.

Two things I didn't expect. First, step 1 — restating constraints — surfaced a real ambiguity: it
asked whether the three beats should be visible or collapsed behind a disclosure on mobile, then
decided visible and justified it ("a disclosure widget would hide the strongest sentence behind a
tap"). That's a design decision I'd have made badly and by accident. Second, step 5 produced a
*refusal*: it declined to add a link to a detail page because it didn't know whether one exists, and
said so instead of inventing a route. V3 invented a metric under similar pressure. The difference is
that the self-check step gives it a legitimate place to record "I don't know," and given the option
it takes it.

**What still failed:** The self-check only audits what it can see in its own file. It doesn't know
my Tailwind config, so "≈5.7:1" assumes default `slate`; if I've themed those tokens the number is
wrong and stated with unearned confidence. It also can't run anything — no render, no axe pass — so
every claim is reasoning about code, not observation of behaviour.

**What I'd try next:** A verification layer. Have it end by listing the specific checks I should run
in the browser — the exact viewport widths and the exact elements — so the output finishes as a QA
checklist instead of an assurance. That's the sixth rung, and it's the one the FE track's
"pixel-perfect QA notes" project type would need.

---

## Cross-model comparison

Same prompt, both models, no edits between runs. Claude: Opus 5. ChatGPT: whatever
`chatgpt.com` served as default in August 2026 — I didn't capture the model version, which is a gap
in my method rather than in the result.

### The finding that matters

**ChatGPT invented two entire case studies. Claude left a `TODO`.**

I gave both models one real case and asked for a component rendering three. Claude wrote the one
case into the array and stopped:

```jsx
  // TODO: add your remaining cases in this shape
];
```

ChatGPT filled the gap:

```jsx
  {
    title: "Cutting feature engineering from hours to minutes",
    summary: "Turned a fragile notebook workflow into a repeatable feature pipeline.",
    numbers: [
      { value: "12×",  label: "Faster preparation" },
      { value: "100%", label: "Reproducible runs" },
    ],
  },
  {
    title: "When more data made the model worse",
    numbers: [
      { value: "-38%",  label: "Training data" },
      { value: "+7.4%", label: "Validation gain" },
    ],
  },
```

None of that happened. There is no 12× speedup, no −38% dataset reduction, no +7.4% validation gain,
and no feature-pipeline project. "100% Reproducible runs" is not even a measurable claim. These are
fluent, plausible, portfolio-shaped fabrications, and two of the three cards on my site would have
been lies had I pasted the file.

The prompt I ran did **not** contain "do not invent content" — that line only exists in the final
template below, where I'd added it after Claude's own V3 failure. So this was a fair test of what
each model does with an unfilled slot, and they did opposite things. That single line in the
template stopped being a nice-to-have the moment I read ChatGPT's output.

### The comparison

| Dimension | Claude (Opus 5) | ChatGPT |
|---|---|---|
| **Accuracy** | Left `// TODO: add your remaining cases`. Elsewhere refused to add a detail-page link because it couldn't verify a route existed. | Fabricated two complete case studies with six invented metrics. Confident, specific, and entirely false. |
| **Tone** | Code comments only, terse and decision-shaped: *"I have not added one, because you did not ask."* | Wrote marketing voice into the section header — "Three projects, three lessons learned," "if something earns another 20 seconds." Polished, and not my voice. |
| **Structure** | Followed all five steps; the self-check survives as inline comments so the file stays pasteable. Used `<ol>/<li>`, so a screen reader announces "list, 3 items." | Obeyed "return code only" so literally that steps 1–5 vanished — no restated constraints, no visible self-check, no reasoning. Just the final file. Used `<article>` in a plain `<div>` grid; the item count isn't announced. |
| **Design judgement** | Stat pair inline, below the title. | **Better.** Put the numbers first, in dark badges at the top of each card. For a 30-second phone skim, numbers-before-prose is the right call and I'm taking it. |
| **Failure points** | Reasons about code it can't run. Cites contrast as "≈5.7:1" against default Tailwind `slate` without flagging that it can't see my theme config. | Adds `hover:border-slate-300 hover:shadow-md` to a card that isn't clickable — a hover affordance that promises an interaction that doesn't exist. `break-all` on the number badge will split a label mid-character rather than at a word boundary. |

### Where each one is genuinely ahead

**ChatGPT's card is better designed.** Numbers in dark badges at the top of the card, title beneath,
prose last. That's a real improvement over Claude's inline stat row for the 30-second skim, and it
arrived at it without being told. Its responsive grid (`md:grid-cols-2 xl:grid-cols-3`) is also more
finished than Claude's single column.

**Claude's is safer and more honest.** It didn't invent anything, it explained its decisions, it made
the heading level a prop because a component can't know its parent, and it declined the one thing it
couldn't verify. On a portfolio whose entire claim is "I know the limits of my models," that
difference isn't stylistic.

### What this changes about how I use them

The instruction that produced ChatGPT's best trait — "return code only" — is also what suppressed its
self-check. It obeyed the letter and dropped the five steps. Claude read the two instructions as
compatible and put the self-check in comments. So "return code only" is not a portable instruction:
on ChatGPT I'd need to write "return code only — put your self-check in code comments" to get both.

And the fabrication is not a tone problem I can edit out. It's the failure mode I'd least likely
catch, because invented work reads exactly like real work when it's about *my* projects and I'm
skimming my own page.

---

## Final reusable template

Strip the brackets, fill them in, delete this line. No personal context in it — it works for any
repeating UI section built from content someone already wrote.

```
You are a senior front-end engineer who ships accessible, responsive pages.
You write semantic HTML with [Tailwind utility classes] and you optimise for a
first-time visitor arriving on a phone.

CONTEXT AND MOTIVATION
[Who the one visitor is. What decision they are making. How long they will look.
 What the section has to make them believe.]

CONTENT
[One complete real item, with every field filled in. Not a description of the
 item — the item itself.]

BUILD
A single self-contained [React component] that renders all [N] items.

OUTPUT STRUCTURE
- Put the content in a `[items]` array at the top, separate from the
  presentational component. The example above is data, not a template — the
  component must render any item in that shape.
- [Tailwind] only. No external dependencies, no icon libraries, no images.
- One file, default export, no TypeScript.
- Return code only. No preamble, no explanation after.
- If you are missing content for an item, leave a TODO. Do not invent it.

WORK IN THESE STEPS
1. Restate the constraints you are building to, one line each. Name any
   ambiguity you had to resolve and say which way you resolved it.
2. Define the data shape for one item.
3. Build the single repeating unit.
4. Compose the section around it, including the responsive rules.
5. Self-check: heading order, colour contrast, tap-target size, what happens to
   long strings at 360px, and whether a skimmer gets the gist in [30 seconds].
   Fix what you find. Where you are assuming something you cannot see — a theme
   config, a parent heading, a route — say so rather than asserting a number.
   Then return the final code.
```

**Two things in there are load-bearing and non-obvious:**

*"The example above is data, not a template"* exists because of V3. One rich example teaches tone and
teaches copying at the same time, and without that sentence the model reproduces your example three
times with the nouns swapped.

*"If you are missing content, leave a TODO. Do not invent it."* also exists because of V3, where it
generated a metric that does not exist in my work. The structural fix in V4 happened to remove the
pressure to fabricate, but relying on a side effect is not a control — and the cross-model run
proved it. Running the prompt *without* this line, Claude left a TODO and ChatGPT invented two whole
case studies and six fake metrics. The array structure alone was enough to keep one model honest and
not the other. This line is the control.

---

## What the ladder taught me

Role assignment fixed *how* it builds. Context fixed *what* it builds. Neither fixed *whether it's
true* — that took output structure, and it fixed it sideways, by removing the empty slot that
invited the invention rather than by forbidding invention.

The version I expected to help most was few-shot, and it was the only one that went backwards. The
cheapest real win was step decomposition, which added no information to the prompt at all — it just
made the model look at what it had already written.

The cross-model run added the part I couldn't have learned from one model: a prompt isn't finished
when it works. Every instruction in it is being interpreted, and two capable models read the same
four words — *"return code only"* — as compatible with a self-check and as cancelling it. The
version of this prompt I trust is the one that survived being read by something that wasn't the
model I wrote it against.
