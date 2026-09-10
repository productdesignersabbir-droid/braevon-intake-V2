# Braevon — Intake Assessment, v2

**The flow is the MEDVi QUAD intake, screen for screen** — same questions, same
options, same branching, same safety rules, same order — rendered in Braevon's
font, palette and button. The client asked for the reference's questions
wholesale on 2026-09-02 and will say screen by screen which become Braevon's
own.

**This repo is deliberately separate from `braevon-intake` (v1), which is live.
Nothing here touches it.**

Static HTML. No framework, no dependencies, no network calls. Open `index.html`
in a browser.

## Files

```
├── index.html          the click-through prototype (= interactive.html)
├── all-screens.html    35 static frames, top to bottom, for the Figma import
├── assets/
│   ├── fonts/          Plus Jakarta Sans (variable woff2)
│   ├── images/         carried over from v1
│   └── video/          hero.mp4 goes here — see its README
├── docs/
│   └── medvi-reference.md   the reference teardown, with measured numbers
├── src/
│   ├── extract_medvi.py  parses the reference into medvi-flow.json
│   ├── medvi-flow.json   the reference's screens, exactly as extracted
│   ├── braevon_q.py      Braevon's questions, laid over those screens
│   ├── groups.json       where the "none of these" sits, per screen
│   ├── extract_v1.py   pulls v1's question set out of a v1 build
│   ├── questions.json  …into here. NOT wired in — see the note below
│   ├── flow_v1.py      reshapes questions.json for the renderer. NOT wired in
│   ├── logo.py         the Braevon wordmark, lifted from v1
│   ├── checkout.py     screen 48, the approval / checkout page
│   ├── consent.py      screen 50, informed consent — v1's copy, v2's dress
│   ├── chart.svg       the onset chart, as supplied; recoloured on the way out
│   ├── theme.py        the stylesheet
│   └── build.py        renders the two HTML files
└── vercel.json         /screens → all-screens.html, plus noindex headers
```

## Building

The HTML files are **generated**. Don't hand-edit `index.html`,
`interactive.html` or `all-screens.html` — edit `src/` and rebuild:

```bash
cd src && python3 build.py
```

Python 3, standard library only. `questions.json` is committed, so the site
builds with no v1 checkout present.

To pull a content change across from v1, point the extractor at that build:

```bash
cd src && python3 extract_v1.py /path/to/v1/interactive.html && python3 build.py
```

To preview locally:

```bash
python3 -m http.server 4173
```

## Where the questions come from

`extract_medvi.py` parses the reference's server-rendered HTML
(`../reference/medvi/medvi.html`) into `medvi-flow.json`: 47 screens, each with
its heading, its options, the note under each option, and the `name` attributes
the reference uses as field ids. It is a parser rather than a retype, so the
copy cannot drift and a change over there shows up as a diff:

```bash
cd src && python3 extract_medvi.py ../../reference/medvi/medvi.html
```

Two things it derives rather than takes literally:

- **The branching**, from the reference's own page names. "5.a.1" is the
  follow-up to option 1 of question 5, "13.a.2" the one behind the alpha
  blocker on 13. Six branches in all: one "how well did it work" and one
  side-effect list per ED medication tried, the two blood-pressure readings,
  the A1C screen behind diabetes, and the nitroglycerin and alpha-blocker
  follow-ups.
- **The safety rules**, from the notes under the options. The reference writes
  them two ways — a note on one answer saying it disqualifies ("Never", "More
  than 3 years ago"), or a note on the exclusive answer saying everything else
  does ("Select this to continue. All other answers will make you ineligible").
  Both flatten into one list of stopping answers per screen. Twelve screens
  carry one.

`build.py` renders that data. It does not know what any question means — which
is the point: the design is `theme.py`'s, and what the screens ask is data.

**Since 2026-09-04 what they ask is Braevon's own, not the reference's.**
`braevon_q.py` lays Braevon's questions over the reference's screens —
headline, sub-head, answers and follow-ups — and nothing else. Screen numbers
are deliberately untouched, so every per-screen table in `build.py`
(`TILE_SCREENS`, `BAND_SCREENS`, `GROUPS`, `DEFAULTS`, `SCREEN_IMAGE`, the
conditionals, the progress bar's step map) still points at the screen it was
written for. `medvi-flow.json` stays exactly as extracted; the overlay is
applied on top of it in one line:

```python
FLOW = braevon_q.apply(FLOW)
```

Source: *Braevon Intake v2 — All Prototype Questions (for Design)*, 10 August
2026. Every screen in `braevon_q.py` carries a `doc=` with that document's own
screen number, so any entry can be checked against it line by line.

`extract_v1.py`, `questions.json` and `flow_v1.py` stay in the repo but are not
wired in. They are a different, older question set (v1's 24) and are not what
`braevon_q.py` renders — do not confuse the two.

## What is not carried across

- **Brand names.** QUAD becomes BRAEVON throughout, via `brandify()`.
- **The two customer quotes** (screens 32 and 44) are MEDVi's named customers.
  Presenting another company's reviews as Braevon's would be fabricating
  testimonials, so the cards keep the reference's shape with copy written for
  this concept — the same call v1 made about DirectMeds' reviews.
- ~~The captions inside long safety lists~~ - restored. `src/groups.json`
  carries them, read off the live reference on 2026-09-03.
- **The extractor's catch-all textarea.** Every multi-answer screen in the
  extraction carries a hidden `answer_*` free-text field. The reference never
  renders one, so neither does v2 — the options are the answer.

## Control shapes

Not every screen is a stacked list. Measured off the live reference, seven ask
their question as **two cards side by side** — 208x190 rather than 432x51 —
and they are listed in `TILE_SCREENS`: sex (3), morning erections (7), blood
pressure diagnosis (24), the two allergy screens (39, 40), current medications
(41) and the note to the doctor (42). The sex screen's cards carry a 64px icon
bubble in the reference's own blue and pink; the other six carry a small mark
that reads as decoration and are left plain.

The reference's subtitle is a plain `<p class="framer-text">` under the h1, not
a heading — reading only headings dropped lines like "QUAD medication is only
suitable for males" off the sex screen. `heads()` takes the first such
paragraph between the h1 and the first option, so captions inside an option
list are not mistaken for it.
- **The 137% partner figure** on screen 33 is the reference's and has no
  Braevon source. It is marked as such on the screen.

## The design

Full teardown with measured numbers in `docs/medvi-reference.md`. In short:

- **One 480px column, centred, at every viewport width.** The reference has no
  desktop layout — a 1280px window shows the same phone column on white. v1's
  three breakpoint tiers and its two-column marketing splits are gone.
- **Cards are a shadow, not a border.** `0 4px 20px rgba(0,0,0,.08)` on white,
  over a white page. v1's 1px border on grey is retired; `--border` now only
  dresses inputs and rules.
- **One rhythm:** 32px between blocks, 16px between options, 24px from title to
  the first control.
- **Five progress segments** rather than one continuous bar. A segment fills
  whole when you enter its section, so question 1 already shows one full segment
  — a fifth-of-a-fifth sliver on the opening screen reads as broken rather than
  as progress. No "Question N of 24" counter.
- **Masthead: wordmark left, rating right.** v1's inline SVG mark
  (`src/logo.py`) and a Trustpilot-style rating — a white star on a green tile,
  the tile square-cornered since 2026-09-08 at the client's ask (it carried a
  2px radius before). The same `.stars` mark serves the checkout's product
  rating; the testimonial stars are a different, yellow, untiled one.
- **The back arrow heads the progress row**, aligned with the wordmark above it,
  with the bar running from there to the rating's right edge — the reference's
  arrangement. It keeps its slot when hidden, so the bar does not shift between
  a screen with an arrow and one without.
- **Braevon keeps:** Plus Jakarta Sans, the orange `#E6430D` (still restricted to
  the CTA, progress fill, selection, the section eyebrow and one emphasis per
  marketing screen), and the v1 button — 10px radius, weight 800, 56px, arrow
  glyph. Not the reference's 16px-radius blue pill.

Deliberate departures from the reference, with reasons, are at the foot of
`docs/medvi-reference.md`: the section eyebrow, the back control, and keeping
blood pressure on one screen instead of two.

## Screen 1

The reference's opening layout: a looping video with the product render breaking
out of its bottom-right corner, a two-line headline whose second line carries the
accent, the tinted claim strip, then the goal list with an icon per row.

- **The video file is not in this repo.** Screen 1 plays `assets/video/hero.mp4`;
  until that lands, the `poster` fills the frame at the right size, so the screen
  renders correctly and simply does not move. See `assets/video/README.md`. The
  reference's own clip is MEDVi footage with their actors and product in shot, so
  it is not reused — the same call v1 made about DirectMeds' photography.
- **The product is `product-tablet.png`**, v1's three-quarter copper render, in
  the slot the reference gives its bottle. Transparent PNG, so its lift is a
  layered `drop-shadow()` filter and never a `box-shadow` — a box-shadow follows
  the element box and paints a rectangle behind the cut-out.
- **The goal wording is v1's, not the reference's.** The five map one to one onto
  the reference's, so the layout takes them unchanged.
- **The goal question is single-select here, where v1 asked it as "select all
  that apply".** The reference asks for one primary goal and pre-picks the
  second; the client asked for both. This is the one place v2 changes a v1
  question's *shape* rather than its dress — the second option arrives already
  chosen — no longer true as of 2026-09-08, when every default was dropped and
  the screen began arriving unanswered like the rest. Revert by dropping the
  `dict(goals, mode='single')` line in `hero_screen()`.
- **The patient's name carries the accent where it is echoed back.** Screen 47
  opens "SABBIR, how can you be reached if necessary?" with the name in orange
  and the rest of the clause in the title ink — the reference marks the name the
  same way in its own blue. `fillSummary()` in `engine.js` builds it out of
  nodes rather than a string: the name is whatever the patient typed, and
  `innerHTML` would make that markup.
- **The terms row on 47 is small print, not an answer.** 13px in the caption
  grey against the 16px an option label takes, and the box sits against the
  first line rather than the middle of the four-line paragraph. `.opts.terms`,
  and it is that screen's alone.
- **Icon bubbles carry the reference's five hues**, read out of its own design
  tokens. A deliberate exception to the orange-carries-emphasis rule, at the
  client's request; nothing else in the flow takes them.
- **Screen 8's comparison bars draw themselves in**, asked for on 2026-09-08 to
  match the reference, which plays the comparison rather than printing it. Each
  bar grows from nothing out to its own width, staggered 140ms apart, and the
  brand bar lands last at 740ms - the point the screen builds to. It is CSS
  only: `@keyframes adv-grow` carries a `from{width:0}` and no `to`, so the end
  is whatever inline width `build.py` set and the numbers stay in one place.
  No observer is needed - a step is `display:none` until shown and animations
  start at frame zero when it is displayed, the same thing `rise` relies on.
  `prefers-reduced-motion` prints the bars instead, and so does `body.frames`:
  the export is a still, and an import taken inside that 1.6s would otherwise
  carry half-drawn bars into Figma.

## Type scale

Every font size is **15% smaller than the reference's**, at the client's
request on 2026-09-02 — option labels and the small copy land on 14px, the
headline on 34px, the section eyebrow on 10px. This is a deliberate divergence
from the reference, not drift: measured at matched viewports the two were
identical before this change.

Audited screen by screen on 2026-09-07, measuring every frame's computed
styles against the reference's own, read first-hand off
`reference/medvi/medvi.html` rather than off the teardown. Four values had
never had the 15% applied and still carried the reference's raw numbers:

| | was | now | why |
|---|---|---|---|
| `.opt.tile .lbl` | 16px | 14px | the reference's own option size, unscaled |
| `.opt.tile .lbl small` | 12px | 10px | the reference's own sub-label, unscaled |
| reveal tile `.lbl` | 15px | *(rule gone)* | a third size for one role |
| `.sub` | 16px | 14px | the reference's caption is 16px/400 |

**Superseded on 2026-09-08.** The client asked for the whole scale up again,
in four parts: option labels **+2px**, titles **+5%**, description text and
everything else **+8%** (rounded to whole px). The numbers below are what the
audit left, not what ships now — read them as the base the bump was applied to.
Option labels are **16px**, the question head 23px, the hero h1 36px, `.sub`
15px. The 15% reduction is therefore no longer the relationship to the
reference; the build now sits a little above it on body copy and a little
under on headlines.

**Superseded for the first screen on 2026-09-10.** The client put our first
screen beside the reference's and asked for the opening block to match it. That
block is now set to the reference's own measured numbers rather than to a
percentage of ours — read off `reference/medvi/medvi.html`, where the hero `h1`
carries them inline and the three lines under it resolve through Framer style
presets:

| | ours was | reference | now |
|---|---|---|---|
| `.hero-h1` | 36px / 600 / 1.05 | **44px / 600 / 1.1em** (inline on its `<h1>`) | 44px / 600 / 1.1 |
| `.strip` | 13px / 400 | **14px / 400 / 1.35em** (preset `1w1iu1y`, mobile variant) | 14px |
| `.ask` | 18px / **400** | **20px / 600**, `strong` 700 (preset `h5suse`) | 20px / 600 |
| `.ask-sub` | 15px | **16px / 400 / 1.45em** (preset `zcdy1q`) | 16px |
| `.ask-hint` | 13px | *(no counterpart — the reference has one caption line, we have two)* | 14px |

`.ask` is the one that was doing the damage. The reference sets that whole line
semibold and only steps the product name up to 700; ours ran the line at 400
with the name bold, so at a glance the line read as a caption rather than as
the question it is. Size was half the gap and weight was the other half.

`.ask-hint` has no reference number because the reference asks one question
where we ask two ("What are you looking to improve?" / "Select all that
apply."). It goes to 14px so the pair doesn't fall away under a 16px sibling.

The narrow breakpoints moved with the base, not independently: `.hero-h1` is
40px under 420px and 34px under 379px (was 33/28). Checked on the served page
at 480/390/360/320 — the headline holds two lines at every width and nothing
overflows. **Only the first screen changed.** The question head is still 23px
against the reference's 26px; that gap is untouched and still open.

**A second pass the same day.** Three more, from the client looking at the
built screen rather than at the reference:

- **`.ask` again — 20px/600 to 22px/700**, `strong` 700 to 800. The numbers
  matched the reference exactly and still read lighter than it, because Plus
  Jakarta Sans's 600 is perceptibly thinner than the Inter the reference sets
  it in. This is the one place on the first screen that is now deliberately
  *not* the reference's number: matched by eye, not by measurement. `.ask-sub`
  and `.ask-hint` went up a px each (17/15) to stay in proportion; their weight
  and colour are untouched, and `--muted` (#4B5568) was already within a shade
  of the reference's #4B5563.
- **The claim strip is a fade again, and hugs its sentence.** Solid-and-
  full-width was a client call on 2026-09-02; this reverses it. It is now
  `--accent-soft` dissolving into `--page`, so the right end of the box has
  become the background by the time it ends, and `width:fit-content` sizes it
  to the text with the padding doing the "a little bigger than the text". Below
  379px `white-space` goes normal and it fills the column over two lines, as
  before.
- **The fact interstitial opens 20px under the progress bar**, not 84px. It
  used to sit centred in its `min-height:525px` on two auto margins; only the
  button keeps one now, so the button stays at exactly the depth it already sat
  at and the copy rises to meet the bar. Written as
  `calc(20px - var(--gap-block))` rather than a flat -12px, because
  `--gap-block` is 26px below 379px and a fixed number lands on 14px there.
  Verified 20px on both fact screens at both gap values.

**The freed space did not disappear, it moved.** Because the CTA keeps its auto
margin, everything the top gave up now sits between the copy and the button:
105px on the two-figure screen, **217px on the 137% screen**. That is the
documented behaviour — the reference does drop its CTA to a consistent depth —
but at 217px it reads as a hole rather than as air. Closing it means lowering
`min-height` on `.col.fact` (or dropping it and letting each screen size to its
content), which moves the button and is a separate decision from the 20px.

**Measure on the SERVED page, never on the file.** `.claude/serve.py` (port
4173) exists for this. Opening `index.html` straight from disk — or through a
tool that renders it as a `data:` URL — fails the `@font-face`, because its src
is relative and does not resolve; the page then falls back to the system font,
whose metrics are narrower than Plus Jakarta Sans. Every line-count and wrap
measurement taken that way is wrong, and wrong in the optimistic direction: a
headline that measures two lines off the file can be three on the real page.
`document.fonts.check('21px "Plus Jakarta Sans"')` tells you which one you are
looking at in one line.

`.qhead.tight` (22px) is the answer to a headline long enough to leave an orphan
on a third line — screen 8's is the only one so far, and it went on at the
client's word on 2026-09-09. It is applied per title through `head(tight=True)`,
never globally. It fixes the 480px column; **below about 448px that headline
still takes three lines**, and pulling it onto two there would need about 17px,
under the 16px option label. That is a copy question rather than a type one.

`.sub.lead` — the interstitial's claim line, set as a second heading rather
than a caption — is the one exception. The 8% put it at 22px against a 23px
`.qhead`, near enough that the two read as a single block, so it was taken back
10% to **20px** and the pair given an 18px gap (`.qhead + .sub.lead`). An
ordinary `.sub` at 15px against 23px needed neither.

Every option label in the build is now **16px**, whatever shape the card is.
Only weight varies — 600 on the blood-pressure bands, 700 on the exclusive
"None of these" — and the reference does the same: its own "None of these"
measures 14px/700 against 16px/500 for a plain option.

The two-up tiles and the goal rows were retuned at the same time, on the same
ask — the mark grows, the card gives back the padding: the tile is 132px tall
(was 170px) around a 44px bubble (was 32px), and a goal row is 56px (was 58px)
around a 42px bubble (was 36px). Both stay over the 44px touch target.

Spacing was never part of the reduction and was already right: 32px between
blocks, 24px title to first option, 16px between rows, 8px radius, 480px
column, 24px padding — all matching the teardown. Row height is 45px against
the reference's 51px because both the type and the padding are scaled
(16px → 13px), which is the sanctioned trade below.

**One exception, and it is load-bearing: form controls stay at 16px.** iOS
Safari zooms the page in on any focused `input`, `select` or `textarea` under
16px and does not zoom back out — a bug the client hit on a real iPhone during
v1. The rule at `.field input, .field select, .field textarea, .reveal
textarea, .reveal input` in `theme.py` is excluded from the scale and must
stay excluded. Take room out of padding instead if a value has to fit a
narrower box.

## The screens

**34 screens, 27 counted questions, 37 frames in `all-screens.html`.**

Not every patient sees 33. Four screens are conditional, so the shortest walk
through the flow — answering in a way that opens no branch — is **29 screens
plus the checkout: 31**. The floor was 29 until the consent screen was added on
2026-09-08 and 30 until the pain question was promoted to a screen of its own on
2026-09-09; that number is the one the client works in, and the mapping below is
written in it. Consent is a screen but not a question, so it does not move the
counted-question total; the pain screen does, and that total is 27.

| Floor | `n` | Screen | Doc |
|---|---|---|---|
| 1 | 1 | What are you looking to improve? | S1 |
| 2 | 2 | ▸ 10–15 minutes | *kept* |
| 3 | 3 | Male or female | *kept* |
| 4 | 4 | Erection confidence | S7 |
| 5 | 5 | ▸ How the 4-in-1 works | *kept* |
| 6 | 6 | Performance factors | S9 |
| 7 | 7 | Do you get erections? | S8 |
| 8 | 8 | ▸ The 4-in-1 advantage | *kept* |
| 9 | 9 | Ever taken ED medication? | S10 |
| 10 | 23 | Physical exam | S13 |
| 11 | 24 | Blood pressure diagnosis | *kept* |
| 12 | 27 | Conditions | S22 |
| 13 | 28 | Curve & foreskin | S20 + S21 |
| 14 | 51 | Pain with erections or ejaculation | S20 |
| 15 | 29 | Diagnoses | S19 |
| 16 | 30 | Cardiovascular risk | S24 |
| 17 | 32 | ▸ Customer quote | *kept* |
| 18 | 33 | ▸ 137% | *kept* |
| 19 | 34 | Cardiovascular symptoms | S23 |
| 20 | 35 | Medicines (nitrates) | S17 |
| 21 | 38 | Recreational drugs | S18 |
| 22 | 39 | Conditions & surgeries | S14 |
| 23 | 40 | Allergies | S16 |
| 24 | 41 | Current medications | S15 |
| 25 | 42 | Doctor notes | S27 |
| 26 | 43 | Date of birth | *kept* |
| 27 | 50 | Informed consent | S30 |
| 28 | 44 | ▸ Customer quote | *kept* |
| 29 | 45 | Medical review | *kept* |
| 30 | 47 | Submission | *kept* |
| 31 | 48 | Approval & checkout | *kept* |

The four conditional screens are 10 and 22 (ED side effects and last use,
behind a Yes on floor 9) and 25 and 26 (the two blood-pressure readings, behind
a Yes on floor 11). Three more frames sit outside the walk: the checkout is 48,
"Assessment received" is 49, and the eligibility stop is 46.

### The prototype's skip-to-checkout control

**This must come out before launch.** A grey pill in the bottom-right corner,
labelled PROTOTYPE, that jumps straight to the checkout so it can be reviewed
without walking the flow. Asked for on 2026-09-07.

It calls `show()` directly rather than `advance()`, so it walks past every
screen without validating or disqualifying on the way, and the checkout echoes
back whatever answers the flow started with — which, since defaults were
dropped on 2026-09-08, is nothing: skipping to the checkout now lands on a page
whose echoed goals and answers are em dashes. It hides itself
once the checkout is on screen, and it is emitted **only** into `index.html` /
`interactive.html` - never into a frame.

Removing it is deleting `SKIP_TO_CHECKOUT` in `build.py`, the line that adds it
to `body` in `emit_interactive()`, the `.proto-skip` block in `theme.py`, and
the skip block at the foot of `engine.js`. Nothing else refers to it.

### What changed on 2026-09-04

Sixteen screens took Braevon's questions; thirteen were left exactly as they
were. The client's own list, in the floor numbering above:

    keep    1 2 3 5 8 11 16 17 25 26 27 28 29
    change  4 6 7 9 10 12 13 14 15 18 19 20 21 22 23 24

Three things that list did not settle, decided by the client when asked:

- **Floor 12** appeared in both halves of it. It changes.
- **Document screen 26** ("other health concerns" — weight loss, hair loss,
  sleep) had no slot left. It is **dropped**, to hold the floor at 29. It is
  the only question in the document that is not clinical screening.
- **Floor 24** was in neither half. It takes the document's wording.

**Fourteen conditional screens were dropped**, none of them on the floor:

- **11–21**, the reference's per-drug follow-ups ("How well did Viagra work for
  you?" and its five siblings, twice over). The document asks one Yes/No on
  floor 9 and hangs two screens off it instead, which is what 10 and 22 now
  are. The flow went from 46 screens to 32 on this change alone.
- **31**, the A1C screen behind diabetes — the document asks it inline on the
  cardiovascular risk screen, one of that screen's three follow-ups.
- **36 and 37**, the nitroglycerin and alpha-blocker follow-ups — the document
  stops the flow on those answers rather than asking more.

### Two pieces of copy here are not the client's

- **Floor 13's headline.** It merges the document's screens 20 and 21 (penile
  curve, tight foreskin) into the one slot the floor allows, and a merged
  screen has no headline in the source. Rather than write one, it keeps the
  headline that screen already had: *"Thank you. Now, please check any of the
  following that apply."* Worth a look.
- **The medical review's third read-back row**, which used to read "Duration
  Satisfaction:". The document has no duration question, and floor 6 now asks
  what affects performance, so the label follows the question and reads
  "Performance Factors:". Floor 27 is otherwise untouched.

### Stopping answers

**Six screens can stop the flow**: `data-dq` carries the reason, `data-dq-on`
narrows what triggers it. Every rule below is transcribed from the document's
own NOTE lines and **has still never had a prescriber's sign-off** — see
*Known gaps*.

| Floor | Stops on |
|---|---|
| 3 | Female |
| 4 | "Very confident" |
| 12 | a heart attack in the last 3 months, or a stroke in the last 6 |
| 13 | a tight foreskin; active bending in the last 12 months |
| 14 | pain with erections or ejaculation — **asked of everyone since 2026-09-09** |
| 20 | any of the five nitrate / alpha-blocker / riociguat answers |
| 11→25 | "I Don't Know" on the blood-pressure reading |

Two of those are new machinery. On floors 12 and 13 the answer that stops the
flow is not on the list itself but in a **yes/no follow-up** that opens
underneath it — ticking "a prior heart attack or heart failure" does not
disqualify anyone, but answering "Yes" to *"Have you had a heart attack within
the last three months?"* does. Each such follow-up's Yes carries a value of its
own (`Q_heart_attack_recent_yes`) which sits on the screen's stopping list, so
the engine's existing check catches it with no new code. A follow-up that has
closed again is skipped, so an answer left behind in a hidden reveal cannot
strand someone on the stop screen.

## Screen 48 — the approval / checkout page

Added 2026-09-04, at the client's word, after the note above said it was out of
scope. It is **not** v1's checkout restyled and it is **not** in
`medvi-flow.json`: the reference serves it from `/approval?flow=org`, a separate
page the questionnaire hands off to, and `extract_medvi.py` only walks
`/intake-s`. `src/checkout.py` builds it; `build.py` appends it to the flow as
one more step so Submit walks onto it the way Continue walks onto any screen.

**Layout, block order, geometry and type are the reference's.** Every number in
the `.ck` block of `theme.py` was read off the live page with
`getBoundingClientRect` / `getComputedStyle` on 2026-09-04 — the same method
`docs/medvi-reference.md` used on the questionnaire. Verified after the build:
each of the sixteen blocks lands within about 40px of the reference's own height
over a 7,400px page, and the pack cards are exactly its 208x121.

Its sixteen blocks, in order:

| | | | |
|---|---|---|---|
| 0 | headline | 8 | pack radios + product card |
| 1 | goals card | 9 | HSA mark + HIPAA card |
| 2 | intro copy + the onset chart | 10 | cancellation promise |
| 3 | the programme card | 11 | *(empty — see below)* |
| 4 | five benefit rows | 12 | three quotes |
| 5 | what's included | 13 | "Are you ready?" + Checkout |
| 6 | what happens next | 14 | cancellation promise (again) |
| 7 | countdown pill | 15 | FAQ, then the footer |

**Everything inside those blocks is Braevon's**, from v1's own checkout (screen
34 of `v1/src/steps.py`, built from the client's `Checkout Page 2.pdf`): the
product, the render (`product-prime.png`, the flat orange tablet from that PDF —
not `product-tablet.png`, the copper render the rest of the flow uses), the FAQ,
the rating and the customer count.

**Prices come from the client's own Figma**, `Braevon — Checkout page`, node
5-2, read on 2026-09-04:

| | price | per tablet | |
|---|---|---|---|
| 6 tablets/mon | $99.00 | $16.50 | |
| 12 tablets/mon | $132.00 | $11.00 | **Most popular** · save 33% per tablet |

That file **supersedes v1's `QTY_PRICES`** (three tiers of 6/10/20 uses at
$119/$159/$189), which is what this screen shipped with until the client said
the packs were wrong. The badge sits on the 12, not the 6, because that is where
the Figma puts it; the sub-line is the per-tablet price rather than the
reference's "hour coverage" (those hours were a derivation, pack × the 36-hour
window); and the rendered string is the Figma's, decimals included.

**The price lives on the card as `data-price`** and the rendered figure is never
the source of truth, so a change is one edit.

**Its chrome is its own.** The reference drops the Trustpilot rating and the
progress bar here and shows a centred wordmark over a countdown bar, so the
screen is `data-bare` like the medical review and prints its own masthead.
Three blocks bleed to the column edge — the masthead, the clock bar and the
footer — with the negative-margin trick `.rv-head` already uses.

**One clock, three faces.** `startClock()` in `engine.js` runs a single 10:00
interval and paints every `[data-countdown]` on the screen, because the
reference states the same deadline in three places. It starts when the checkout
is first reached rather than on load, so the time cannot have run down while the
questionnaire was being filled in, and walking back and forward picks the
running clock up rather than restarting it — a deadline that resets on every
visit reads as a trick. At zero it holds at 00:00; nothing is withdrawn.

### The onset chart

`src/chart.svg` is the chart **as supplied**, and `checkout.chart()` applies four
recolours and one rule change on the way out, so a new export drops in and the
recolour still applies:

| from | to | |
|---|---|---|
| `fill="white" fill-opacity="0.32"` | `fill="none"` | the chip underlay |
| `fill="#01000C" fill-opacity="0.56"` | white + a `#DEE2EA` hairline | the chip pill |
| `fill="white"` | `#4B5568` | the four tick labels |
| `fill="#FDFCFC"` | `#171D2C` | the chip lettering |

The rule change: the 2x chip scale was behind `@media (max-width: 600px)` and is
now unconditional. **Inside an inline SVG a media query still measures the
viewport, not the drawing**, and this chart is ~432px wide at every viewport
width because the column is — so at 1x on a desktop the lettering renders at
about 4.7px, which is the case the 2x scale exists for. Measured after the
change: all four chips sit inside the 432×193 box and the tightest pair
(BRAEVON's bottom to SILDENAFIL's top) clears by 3.8px, which is the artwork's
own stated margin.

**The `braevon-hold` wrapper, its `<style>` and its IntersectionObserver are
dropped.** They exist to hold the chart at frame zero until it is scrolled to;
here it lives inside a `display:none` step, CSS animations do not run on a
`display:none` subtree and start from frame zero when it is shown, so the step
machinery already does the observer's job — and an observer on a hidden element
would never fire, which would hold the chart for ever.

### The footer

braevon.com's own footer, read off the live site's **phone** variant on
2026-09-04 — the right one to copy, because this page is a 480px column at every
width. Two changes, both the client's: it is white rather than the site's
`#141414`, and **the full-width BRAEVON wordmark the site prints at the very
bottom is gone**. Everything else is the site's, wording and order unchanged —
the tagline, `support@braevon.com`, the Orlando address, the five legal
paragraphs, the LegitScript seal, the four policy links, the copyright and the
two social links. `assets/images/footer-seal.png` is the site's own seal file.

### Where this screen departs from the reference on purpose

All the client's, all from 2026-09-04:

| | reference | here |
|---|---|---|
| countdown bar | its brand blue, column width | full-strength `--accent`, **full window width** |
| type ramp | 26/20/18/17/16/15/14 | one step down — Plus Jakarta Sans reads larger than its Inter at the same px |
| the chart | 392×280 in the column | breaks out to 640×285, so the artwork keeps its own proportions |
| goals card | three fixed glyphs | three glyphs, the first following the answer |
| tag chips | — | primary `--accent`, not `--accent-deep` |
| "reserved for" pill | a blue gradient | **v1's mint** — `#41D8A6` on `#00462F`, from `Approval page.pdf` |
| "Choose your medication preference" | left, section size | centred, one step smaller |
| the tablet in "what's included" | 66px | 96px |
| the HSA mark | a supplied image | drawn as it draws it — a circled tick and the words |
| block 11 | a research-logo row | empty |

### Two colour tokens this screen added

`--accent-deep` (#B8300A) and `--accent-deeper` (#8E2405). `#E6430D` is 4.06:1
against white — clear for large text, short of AA for the 10-16px white labels
the clock bar, the pills, the strip and the tags carry. Those chips take
`--accent-deep` at 6.1:1 instead, so the page does not gain a second orange for
anything that carries large type. `--green-ink` (#15803D) is the same fix for
green as small type: `#16A34A` is 3.36:1. Nothing else may use any of the three.

Checked after the change — every text/ground pair on this screen is at or above
AA: the bar and pills 6.1:1, the pack badges 6.1 and 5.2, the green price 5.0,
the press marks 5.3, the footer greys 7.5.

## Behaviour

Carried from v1: "None of these" is exclusive in both directions; Yes and Other
reveal a follow-up; conditional screens are skipped in both directions; the
blood-pressure screen estimates a reading from the chosen band, takes a typed
reading instead, and warns at both extremes; the state chosen on screen 4 is
echoed into screen 5; the first name from screen 28 titles the result.

**Answering advances the screen.** Continue — labelled *Next*, as the reference
labels it — stays on screen and still works, so this is a shortcut past it
rather than a replacement. Four things hold it back: a multi-select waits unless
the answer is the exclusive "None of these" (on "select all that apply" the
patient may want two or three, and leaving on the first tick collects exactly
one); unticking never advances; **any open follow-up holds the screen**
(2026-09-04 — see below); 
and the blood-pressure screen never jumps, because it exists precisely so
someone who knows their real reading can type it. Everything else falls out of
`stepValid`, so the eligibility and patient-info screens hold on their own while
their inputs are empty. It routes through `advance()`, the same function the
button calls, so a disqualifying answer still opens the stop screen.

An open follow-up holds the screen whether or not it is optional. *Optional*
means the box does not gate *Next* — the patient can move on without typing —
which is a different thing from letting the screen leave on its own while the
box is sitting there open. The two were conflated until 2026-09-04: answering
"Yes" is the click that opens the box, and auto-advance fired on that same
click, so the box appeared and the screen left underneath it. Every Yes/No
screen with a detail box was affected (9, 10, 23, 39–42, and the multi-answer
screens with a "tell us more"). "No" opens nothing and still advances on the
answer, as before.

**Selection is an outline and a glow, never a fill** — a 1px `--accent` stroke
with a soft orange halo, over the resting `--hairline` grey. A tinted row reads
heavy next to four white ones and fights the icon bubbles, which carry colour of
their own.

**There is no HIPAA line under the button.** v1 ran one on every screen; the
reference has none and the client asked for it out.

New in v2, from the reference: the two processing screens carry no button and
hand off on their own. **The hand-off is on a timer, not on the animation
frame** — a background tab stops serving `requestAnimationFrame`, and with no
button on the screen, driving the advance from the frame loop strands anyone who
switches tabs mid-processing.

The Continue button never greys out — client request, carried from v1. It stays
orange while the screen is unanswered and refuses to advance, so it has to
receive the click in order to point at what is missing.

## Deploying

Vercel, as a static site: no framework preset, no build command, output directory
is the repo root. `/screens` serves the frame grid.

Send the **production** URL, never a URL with a deployment hash in it — those are
per-build previews, Vercel puts Deployment Protection on them by default, and
anyone without a Vercel account is bounced to a login. That has already cost a
round trip with the client on v1.

Commits must be authored with the GitHub noreply address; the account has email
privacy on and a commit with the real address is rejected at push time.

## Known gaps

- **"Cancel Anytime" was removed from the checkout on 2026-09-07, but the
  cancellation claim is still on the page three times.** The block that came
  out was rendering TWICE (once under the HIPAA line, once before the FAQ),
  which is why the promise appeared in two places. What remains: the "What's
  included" list ("Cancel anytime, come back anytime"), the note under the
  Checkout button ("No contracts, cancel anytime"), and the FAQ's shipping and
  cancellation answer. **Ask the client whether those three should go too** -
  removing only the block may not be what they meant.
- **One checkout icon is not the reference's.** "Increased Confidence" takes
  the shield-and-tick the build already uses for that goal on screen 1, because
  the reference's flexed arm does not survive being stroked at 18px - two
  attempts both read as a blob at the size it actually renders. The other four
  (bolt, brain, heart, battery) are the reference's.

- **The checkout's operational promises are not signed off.** "Most prescriptions
  are approved in less than 24 hours" and "tracking information within 2 business
  days" are the reference's timings with Braevon's name on them (`NEXT_STEPS` in
  `checkout.py`). Nobody at Braevon has confirmed either. Same for
  "24/7 medical support" and "free express shipping" in `INCLUDED` — those at
  least restate claims v1's own checkout makes.
- **The money-back guarantee is now a refund promise, at the client's word
  (2026-09-07).** This had been an open question: the reference promises money
  back, a refund is a commercial commitment only the client can make, and what
  Braevon itself says — in v1's FAQ — is that a plan can be cancelled from the
  patient portal. The client asked for the reference's wording, so the block on
  the checkout now says money back. **It is a promise Braevon has to be able to
  honour and it still needs someone commercial to sign it.**
- **"BACKED BY RESEARCH FROM" is built (2026-09-07) and asserts something
  nobody has evidenced yet.** The client asked for it after this block had been
  left empty on purpose. Two things about it are still open, and both are
  theirs: (1) it says five real institutions — Mayo Clinic, Stanford Medicine,
  WebMD, Harvard University and the NIH — back this product. If what is meant is
  "these bodies have published research on the PDE5 molecules", the heading
  should say so; as written a reader takes it as Braevon being endorsed. It
  needs evidence or a rewording. (2) The names are **type-set, not logo files** —
  those marks are trademarks we do not have, and drawing an approximation of the
  Mayo Clinic or Harvard mark would be worse than showing none. v1 made the same
  call for its press row. Real artwork has to come from the client, with
  permission to use it.
- **The checkout's card fields are a mock-up and must be replaced by Stripe's
  Element.** Added 2026-09-07. Email, full name, state and phone carry forward
  from screens 45 and 47; address, city and ZIP are asked here. The card number,
  expiry and CVC are **ordinary inputs with no form, no action and no script** —
  nothing is collected, stored or sent anywhere, and the page cannot take a
  payment. They were built at the client's explicit request after being left out
  once; the document's own screen 31 says the real fields are Stripe's ("card
  fields go to Stripe only — never stored by Braevon"). **Do not wire these up
  and do not deploy this page anywhere a real patient could reach it** — a
  realistic card form is a thing people type into. Swap the block for Stripe's
  Element before launch.
- ~~**The checkout spreads to 860px on a wide screen.**~~ Reverted on
  2026-09-09, the same day it went in: the checkout is the 480px column again,
  like every other screen. One column at every width is back to being true of
  the whole build with no exceptions.
- **The research row now renders the client's supplied logo strip**
  (`assets/images/research/row.png`, added 2026-09-09), not the type-set names.
  It is a screenshot of the reference's own row, cropped to the marks and capped
  at its natural 494px so it is never enlarged — soft on a 2x display, and the
  permission question under it is untouched by having artwork. See the note in
  that folder; deleting the file brings the names back.
- **The payment-method and card-brand marks are type and shapes, not the
  trademark artwork.** Google Pay, Amazon Pay, Visa, Mastercard, Amex and
  Discover all publish brand kits with usage rules. What is here says *which*
  methods are taken without passing off an approximation as the real mark.
  Swap in the official artwork before launch.
- **The skip-to-checkout control is still in the build.** See the section above.
  It is the one thing here that must not ship.
- **The pain question now stops the flow for everyone, and that is a widened
  rule.** "Do you experience pain with erections or with ejaculation?" was a
  follow-up revealed by the curve / Peyronie's answer on floor 13 — where the
  client's own document (screens 20 and 21) and v1 both put it, and where the
  reference has it as one checkbox among five. It became a screen of its own on
  2026-09-09 at the client's word. Yes still ends the assessment, as it did as a
  follow-up, but it is now asked of every patient rather than only of the ones
  reporting a curve, so **anyone answering Yes is stopped**. Dropping the stop
  instead would have been the other silent change and the narrower one: the
  patients it already covered would stop being caught. Neither direction is a
  design call — put it in front of the prescriber with the rest of the rules.
- **Every per-screen stop message was invisible until 2026-09-09.** The overlay
  had no `[data-dq-reason]` slot, so `stop()` in `engine.js` looked for one,
  found nothing, and silently kept the generic fallback. Around twenty specific
  messages — the nitrate one, the blood-pressure one, the male-only one — had
  been written, emitted onto each section as `data-dq`, read by the engine and
  dropped. The slot exists now and the copy reaches the patient. **Worth
  re-reading those messages with fresh eyes before launch: they have never
  actually been seen on screen.**
- **The checkout's warm panels are grey since 2026-09-09.** The testimonial
  cards, the FAQ, the pack panel, the product shot and the success-probability
  panel all sat on their own warm off-white gradients; stacked, they read as the
  page going orange. They share `--neutral-tint` now. Orange is left where it is
  carrying something — the CTA, the figures, the marks.
- ~~**Screen 1's goals question is a multi-select with one answer pre-ticked.**~~
  **Settled on 2026-09-08**: nothing is pre-ticked anywhere, screen 1 included,
  so the question now matches the document's own "select all that apply" with no
  default. This overrides the 2026-09-03 ask for a default on this screen.
- **`assets/video/hero.mp4` is missing** — screen 1 falls back to its poster.
- **The testimonial copy is placeholder**, as it was in v1. Three reviews written
  for this concept, not real ones. Say so before showing anyone who might take
  them at face value.
- **The disqualification rules have never had a prescriber's sign-off.** Since
  2026-09-04 they are transcribed from Braevon's own document's NOTE lines
  rather than read off the reference, which is an improvement in provenance and
  no improvement at all in clinical review. The nitrate interaction on floor 19
  is a genuine, well-established contraindication; the rest are the document's
  judgement calls, faithfully copied. Get a prescriber to confirm the list and
  the wording before this goes near a real patient.
- **One question in the document is not built.** Screen 26, "other health
  concerns", was dropped to hold the floor at 29 — it is a cross-sell question,
  not a screening one, and it can be added back in a few minutes if the client
  wants it.

  ~~Screen 30, **informed consent**, has no equivalent anywhere in v2.~~
  **Built on 2026-09-08** and now floor 26, `n` 50. The reference's flow has no
  consent step, so there was no screen to lay it over; it is v1's screen, copy
  verbatim, in v2's components. See `src/consent.py`, and the two content
  questions recorded in its docstring — the contraindications sit behind a tap,
  and the two side-effect sections say the same thing twice. Both are inherited
  from the client's own `Consent box.pdf` and both are still worth a decision.
- **The photograph on floor 23 is the client's own**, supplied 2026-09-04, and
  replaced a stand-in. Its box is **square** (asked for on 2026-09-04 —
  the 168px band it replaced cropped a tall portrait down to a strip across the
  eyes), set with `aspect-ratio` so it stays square at every shell width. The
  bias is `object-position: 50% 15%`, slightly high because a face sits above
  the middle of a portrait; tuned to that file (`man-portrait.jpg`, 1045×1400)
  — retune it in `theme.py` if the photograph is replaced. `.qshot-top` is this
  screen only; the testimonial figures use `.qshot`, which is untouched. It is deliberately a separate file
  from `stat-hero.jpg`, which is still the testimonial avatar on floor 26.
- **Buttons have no hover state and there is one orange.** Asked for on
  2026-09-03: `--accent-hover` is gone, so `#E6430D` is the colour at rest, on
  hover and while pressed. The only other oranges in the build are
  `--accent-tint` (the in-progress progress segment) and `--accent-line` (the
  selected row's outline), both of which are deliberate lighter shades rather
  than a second primary.
- **The 4.6 masthead rating is a placeholder**, carried from v1's header. It needs
  a real figure or it should come out. (braevon.com does show "Excellent 4.6 out
  of 5", so this may now be the real figure - worth confirming.)
- **The formula is Braevon's four**, taken from braevon.com on 2026-09-03:
  Sildenafil, Tadalafil, Vardenafil, Apomorphine, with that site's own
  descriptions. The reference's L-Citrulline is gone. Two things about the
  product copy are still NOT reconciled with braevon.com:
  - the **onset figure**. These screens carry the reference's "10-15 minutes";
    braevon.com says "Starts in 15 Minutes" in one place and "8 min activation
    time" in another. Someone has to say which is right.
  - the **product name**. braevon.com calls it BRAEVON PRIME(TM); this build
    calls it "BRAEVON 4-in-1" throughout, from the reference's "QUAD 4-in-1".
  - the dose column in `MOLECULES` is not rendered and its figures were never
    verified; it is em-dashes now rather than invented numbers.
- **The 137% figure is the reference's, not Braevon's.** Screen 33 presents it
  as Braevon's own result. It needs a Braevon source or it should come out
  before this is shown to a patient. The on-screen asterisk that used to flag
  this was removed to match the reference's layout, so this note is now the
  only record of it.
- **Three of the four "Yes" detail boxes are our wording.** Screens 39-42 open a
  box to list the detail when you answer Yes, as the reference does. The
  reference renders those only after Yes is picked, so they are not in the DOM
  extraction: screen 40's label is its own, read off the live screen; 39, 41 and
  42 follow the same pattern and are ours. Like the reference's, the box does
  not gate the step - worth asking a prescriber whether it should.
- **The 94% success probability is the reference's number, not Braevon's** -
  same problem as the 137%. Screen 45 presents it as a result of this
  assessment; nothing computes it. It needs a source or it should come out.
- **Screen 47's button walks onto the checkout; the checkout's own button ends
  the flow.** It reads **"Check Eligibility"** — the reference's own label,
  asked for on 2026-09-09; it said "Submit" until then. Its terms line names the
  button, so that moved with it: "By clicking Check Eligibility, I agree…". The
  reference does NOT do that — its own small print still says 'By clicking
  "Submit,"' under a Check Eligibility button — so this is one place v2 is
  deliberately more consistent than what it copies. Put "Submit" back in both
  places if the client wants the reference's wording exactly. Screen 47 shows
  screen 48; that page's "Checkout" shows the "Assessment Received" state. **Nothing is charged and nothing is posted** —
  there is no backend here and no payment step at all. The reference hands off
  to Stripe at this point; wiring that up is separate work.
- **Screen 41's photograph is a stand-in.** The reference opens that one
  question screen with a photo (the only question screen that has one - checked
  by listing every image in its DOM). It uses a man at his bathroom cabinet: an
  ordinary moment, not a clinician. There is no such photograph in this repo,
  so the screen points at `stat-hero.jpg` - the nearest register available, and
  otherwise unused. **A bathroom/medicine-cabinet shot is needed to match.**
- **The testimonial photos and names are placeholders.** Screens 32 and 44
  point at `hero-benefits.jpg` and `braevon-hero.jpg` from the existing asset
  folder; the reference uses shot-for-purpose photography. Each testimonial's
  avatar is its own photograph cropped to the face, so the small circle and the
  picture above it are the same person - except screen 44, whose photograph is
  a couple and cannot crop to one face, so its avatar borrows `stat-hero.jpg`
  from screen 41's banner. `doctor.jpg` is now unused: a white coat and a
  stethoscope read as a clinician, not as the customer giving the quote.
  The quotes and the names on them (Ethan Caldwell, Ryan Mitchell) are written
  for this concept and are not real people or real reviews - say so before
  showing anyone who might take them at face value.
- ~~**Screen 43's "LAST STEP" is now the reference's gradient pill.**~~ The pill
  came off on 2026-09-08, when the consent screen was added after it and made
  the claim false. It is not moved onto the consent screen either: that screen's
  own headline is "One last step — your consent", and a pill under it would say
  the same thing twice. Screen 43 keeps its privacy panel — the same tinted
  component the blood-pressure screen uses, with the reference's longer HIPAA
  wording.
- **No question screen opens on an answer** — asked for on 2026-09-08, and it
  reverses what the reference does. Walking the reference, its sex screen
  arrives with "Male" already selected and Next enabled without anything being
  clicked, and every other single-answer screen the same; a multi-answer screen
  arrives on its "none of these". `DEFAULTS` is now an empty table. Nothing
  else had to change: `stepValid()` in `engine.js` already refused to advance a
  screen with no `.opt.selected`, and `cta(blocked=...)` reads the same table,
  so every question screen's Next now carries `data-blocked` until it is
  answered. Refill `DEFAULTS` and both behaviours come back.

  **This retires the clinical note that stood here.** Screens 24 and 39-42 open
  on "No" and every safety checklist opened on "none of these", so a patient
  clicking straight through used to submit "no hypertension, no allergies, no
  medications, no conditions" without having read a single one. They now have
  to answer each one. It was the thing in this build most in need of a
  prescriber's sign-off, and it is gone.

  One consequence for the export: the frames in `all-screens.html` now show
  every question unanswered, where they used to show the default picked.
- **Female stops the flow on screen 3.** The medication is male-only and that
  screen's own sub-head says so, so the reference does not carry on into
  questions that cannot apply. The DOM extraction does not carry the rule; it
  is in `DQ_EXTRA` with the blood-pressure one.
- **Where "None of these" sits is per screen, not a rule.** The reference puts
  it last on the ED-treatments, sex-organ, cardiovascular, heart-symptom and
  medication screens, and first - on a green card, under "Select this to
  continue. All other answers will make you ineligible." - on the six
  side-effect screens and on 27, 29 and 38, where every other answer is
  disqualifying. `src/groups.json` carries this per screen, along with the
  section captions. Read off the live reference on 2026-09-03.
- **The progress bar follows the reference's own step numbers.** Every screen
  name in the extraction ends in one - "A2 - 03", "Blood Pressure 2 - 07.a",
  "Birth Date - 20" - running 1 to 21, and the bar is divided over those, not
  over our 40 questions. Two traps: the step is the LAST number in the name
  ("FACT-2 - 12" is step 12, not 2), and an interstitial is not a step even
  when its name carries one, which is why the reference's "137%" screen and the
  question after it both say "12" but sit in different segments.
  `SEGMENT_STARTS` = [1, 7, 12, 16, 19]. Every boundary up to 12 is confirmed
  against the live page (steps 3, 5, 6 in segment 1; 7, 8, 11 in segment 2; 12
  in segment 3), and 16 is confirmed too - the reference's "any other
  allergies?" screen (step 16) shows three solid segments and one current, and
  so does ours. **Only 19 is unverified**, being the remaining steps split
  evenly.
