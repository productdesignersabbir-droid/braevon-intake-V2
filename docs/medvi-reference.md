# MEDVi QUAD — reference teardown

Source: `https://quad.medvi.org/intake-s?flow=org` (captured 2026-09-02).

Every number below was read off the live page with `getComputedStyle` and
`getBoundingClientRect`, not estimated from a screenshot. Where v2 departs from
one of them it is because the brief says to keep Braevon's font, colour and
button — those departures are listed at the bottom.

The site is built in Framer. The whole questionnaire ships in the DOM at once as
47 sibling "pages" under `[data-framer-name="Pages"]`, with all but the current
one set to `display:none`.

## Layout

| | |
|---|---|
| Page background | `#FFFFFF` |
| Column | `max-width: 480px`, centred, **the same at every viewport width** |
| Column padding | `0 24px 24px` → 432px of content |
| Gap between blocks in the column | `32px` |
| Header | `space-between`, `padding: 12px 24px`, ~46px tall |
| Header content | wordmark on the left, Trustpilot rating on the right |
| Divider | 1px rule under the header |

There is no desktop layout. A 1280px window shows the same 480px phone column,
centred on white — no two-column split anywhere in the flow, on any screen.

## Progress

Five segments, not one bar.

| | |
|---|---|
| Segment | `58 × 12px`, `border-radius: 6px` |
| Gap | 24px |
| Track | `#E5E7EB` |
| Fill | `#2563EB` |

Each segment fills across its own section, so the bar reads as five chapters
rather than one long crawl. No "Question N of M" counter anywhere.

## Type

| Role | Size | Weight | Line height | Colour |
|---|---|---|---|---|
| Question `h1` | 26px | 600 | 31.2px (1.2) | `#111827` |
| Option label | 16px | 500 | 19.2px (1.2) | `#111827` |
| Option sub-label | 12px | 400 | 15.6px (1.3) | `#4B5563` |
| Rating text | 10px | 600 | — | `#6B7280` |

Typeface is Inter. Gap from title to the first option is 24px.

## Option rows

| | |
|---|---|
| Background | `#FFFFFF` |
| Border | **none** |
| Radius | `8px` |
| Shadow | `0 4px 20px rgba(0,0,0,.08)` |
| Padding | `16px` (24px 16px on the taller first-screen rows) |
| Gap, control to label | 10px |
| Gap between rows | 16px |
| Height | 51px single-line, 67px with a sub-label |

White cards on a white page, separated by shadow alone. Two-up questions (the
male/female screen) use the same card as a 2-column grid with deeper padding.

## Primary button

| | |
|---|---|
| Width | full column (432px) |
| Height | 54px |
| Background | `#2563EB` |
| Radius | **16px** |
| Type | 18px / 600, white |
| Disabled | pale lavender fill, faded label |

## Flow shape (47 pages)

Roughly: goal → fact card → sex → symptom questions, interleaved with
interstitials (a 4-in-1 explainer, an onset comparison chart, two customer
quote cards, two "fact" stat cards) → prior-ED-treatment branch (six parallel
"how well did X work" and six parallel side-effect screens) → physical exam →
blood pressure (systolic and diastolic on separate screens) → the safety
checklists → allergies and medications → date of birth → **Medical Review**
(an "Assessment Complete" card with a success-probability figure and a read-back
of the answers) or **NO RX** (the eligibility-stop screen) → contact submission.

Behaviours worth copying:

- Safety lists lead with an exclusive **"None of these"**, captioned *"Select
  this to continue. All other answers will make you ineligible."*
- A disqualifying option carries its warning inline, under the label: *"This
  answer will disqualify you from medication."*
- The stop screen offers **"Made a mistake? Review your answer"** rather than a
  dead end.
- Interstitials sit between questions and carry no progress segment of their own.

## What v2 keeps, and what it changes

Kept from the reference: the 480px single column at every width, white page,
32px block rhythm, 16px option gap, 8px shadowed borderless cards, 26px/600
titles, 16px/500 option labels, five-segment progress, full-width bottom CTA,
inline disqualification warnings, exclusive "None of these" at the top of a
list, the auto-advancing processing screen, the assessment-complete read-back
and the full-bleed stop screen.

Changed, per the brief ("keep our font, colour and button style"):

| Reference | v2 |
|---|---|
| Inter | Plus Jakarta Sans (Braevon) |
| `#2563EB` blue | `#E6430D` orange (Braevon) |
| Button radius 16px, 18px/600, 54px | Braevon's button: radius 10px, 15.5px/800, 56px, arrow glyph |
| Grey `#111827` ink | Braevon's `#171D2C` / `#2B313C` |

Three further deliberate differences, none of them cosmetic drift:

1. **Section eyebrow above each question.** The reference has none. v1 does, and
   it is one of the five sanctioned uses of Braevon orange, so it stays.
2. **A back control.** The reference has none; the Braevon client asked for one
   on every screen. It sits as a chevron at the left of the masthead — the only
   place it fits this layout without adding a row.
3. **Blood pressure on one screen, not two.** The reference splits systolic and
   diastolic across two screens. v1 puts both on one with a live estimate and a
   direct-entry option, which is the better control and is already approved.
