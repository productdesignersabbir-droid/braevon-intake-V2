# Braevon — Intake Assessment, v2

A redesign of the Braevon intake, **not** a re-scope. The clinical content is
v1's, unchanged: the same 24 numbered questions in the same order, the same
conditional follow-ups, the same disqualification rules. What changes is the
design — layout, spacing and surface treatment follow the MEDVi QUAD intake
(`quad.medvi.org/intake-s?flow=org`), while the font, palette and button stay
Braevon's.

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
│   ├── extract_v1.py   pulls the question set out of a v1 build
│   ├── questions.json  …into here — the content this site renders
│   ├── logo.py         the Braevon wordmark, lifted from v1
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

`extract_v1.py` parses a v1 build and writes `questions.json`: per screen, an
ordered list of blocks (eyebrow, title, subtitle, legend, option group,
conditional reveal, field) plus the disqualification rule and the skip-unless
condition. It is a parser rather than a retype, so the clinical copy cannot
drift and a v1 correction comes across in one command.

`build.py` renders those blocks into the reference's markup. It does not know
what any question means — which is the point: the content is v1's, the design is
`theme.py`'s.

Verified 2026-09-02: all 24 questions here are **identical** to the live v1
build at `braevon-intake@39f50e3`.

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
- **Masthead: wordmark left, rating right.** v1's inline SVG mark (`src/logo.py`)
  and a Trustpilot-style rating. With the mark on the left the back control moved
  down beside the progress bar, where v1 also kept it.
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
  chosen, so the screen is answered on arrival. Revert by dropping the
  `dict(goals, mode='single')` line in `hero_screen()`.
- **Icon bubbles carry the reference's five hues**, read out of its own design
  tokens. A deliberate exception to the orange-carries-emphasis rule, at the
  client's request; nothing else in the flow takes them.

## Type scale

Every font size is **15% smaller than the reference's**, at the client's
request on 2026-09-02 — option labels and the small copy land on 14px, the
headline on 34px, the section eyebrow on 10px. This is a deliberate divergence
from the reference, not drift: measured at matched viewports the two were
identical before this change.

**One exception, and it is load-bearing: form controls stay at 16px.** iOS
Safari zooms the page in on any focused `input`, `select` or `textarea` under
16px and does not zoom back out — a bug the client hit on a real iPhone during
v1. The rule at `.field input, .field select, .field textarea, .reveal
textarea, .reveal input` in `theme.py` is excluded from the scale and must
stay excluded. Take room out of padding instead if a value has to fit a
narrower box.

## The 34 screens

24 numbered questions plus ten interstitials:

| # | Screen | # | Screen |
|---|---|---|---|
| 1 | Q1 What are you looking to improve? | 18 | Q14 Recreational drugs |
| 2 | ▸ 92% prefer BRAEVON | 19 | Q15 Prior diagnoses |
| 3 | ▸ Trusted by 250k+ men | 20 | Q16 Curve or bend |
| 4 | Q2 Eligibility — sex, DOB, height, weight, state | 21 | Q17 Tight foreskin |
| 5 | ▸ Available in your state | 22 | Q18 Conditions, current or past |
| 6 | ▸ Health intro / HIPAA | 23 | Q19 Cardiovascular symptoms |
| 7 | Q3 Erection confidence | 24 | Q20 Cardiovascular risk factors |
| 8 | Q4 Do you get erections? | 25 | Q21 Blood pressure |
| 9 | Q5 Performance factors | 26 | Q22 Other health concerns |
| 10 | Q6 Prior ED medication | 27 | Q23 Anything else for your doctor |
| 11 | Q7 Side effects *(only if Q6 = yes)* | 28 | Q24 Patient info |
| 12 | Q8 Last use *(conditional)* | 29 | ▸ Consent |
| 13 | Q9 Physical exam | 30 | ▸ Processing |
| 14 | Q10 Conditions & surgeries | 31 | ▸ The 4-in-1 |
| 15 | Q11 Current medications | 32 | ▸ 15 minutes / 89% |
| 16 | Q12 Allergies | 33 | ▸ Reviewing your assessment |
| 17 | Q13 Nitrates and alpha blockers | 34 | ▸ Assessment complete |

Plus the disqualification screen, which is a state rather than a step and is
appended as frame 35 in `all-screens.html`.

**Screens 17, 18, 22 and 23 can stop the flow**, on v1's rules: `data-dq` carries
the reason, `data-dq-on` narrows what triggers it, and with no `data-dq-on` any
answer other than the exclusive "None of these" is a contraindication.

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
one); unticking never advances; an open follow-up still has to be typed into;
and the blood-pressure screen never jumps, because it exists precisely so
someone who knows their real reading can type it. Everything else falls out of
`stepValid`, so the eligibility and patient-info screens hold on their own while
their inputs are empty. It routes through `advance()`, the same function the
button calls, so a disqualifying answer still opens the stop screen.

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

- **The v1 approval and checkout screens are not here.** Those were redesigned by
  the client in Figma in August 2026 and are not part of the reference's flow,
  which ends at an assessment-complete read-back. v2 ends the same way, at screen
  34. Carrying them over or restyling them is separate work.
- **`assets/video/hero.mp4` is missing** — screen 1 falls back to its poster.
- **The testimonial copy is placeholder**, as it was in v1. Three reviews written
  for this concept, not real ones. Say so before showing anyone who might take
  them at face value.
- **The disqualification rules have never had a prescriber's sign-off.** They are
  our reading of the reference flow, inherited from v1. The nitrate interaction
  on screen 17 is a genuine, well-established contraindication; the rest are
  judgement calls. Get a prescriber to confirm the list and the wording before
  this goes near a real patient.
- **The 4.6 masthead rating is a placeholder**, carried from v1's header. It needs
  a real figure or it should come out.
