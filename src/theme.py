# -*- coding: utf-8 -*-
"""v2 stylesheet.

Geometry, spacing and surface treatment come from the MEDVi QUAD reference
(`quad.medvi.org/intake-s?flow=org`), measured off the live page rather than
eyeballed — see `reference/medvi/design-notes.md` for the numbers.

Font, palette and button treatment stay Braevon's, carried over from v1.

The three things that changed shape from v1, and why:

1. **One column, 480px, on every screen size.** v1 had three breakpoint tiers
   and a two-column split on the marketing screens. The reference is a single
   480px column centred on a white page, identical from phone to desktop — a
   phone layout that a desktop simply centres. That is the layout, so the tiers
   are gone; what is left is one `--pad` that tightens under 380px.

2. **Cards are a shadow, not a border.** v1 was 1px borders on a grey page with
   no shadow. The reference is white-on-white separated only by
   `0 4px 20px rgba(0,0,0,.08)`. Keeping v1's border here would read as a
   different design, so the shadow wins and `--border` is now only for inputs
   and rules.

3. **Content is top-aligned under the progress bar.** Same as v1, and the
   reference agrees — it is not vertically centred.
"""

CSS = r"""
/* ---------------------------------------------------------------- font */
@font-face{
  font-family:'Plus Jakarta Sans';
  src:url('assets/fonts/PlusJakartaSans-Variable.woff2') format('woff2-variations');
  font-weight:400 800; font-style:normal; font-display:swap;
}

/* --------------------------------------------------------------- tokens */
:root{
  /* Braevon palette, unchanged from v1 ------------------------------- */
  --accent:#E6430D;        /* CTA, progress fill, selection, key emphasis */
  --accent-soft:#FDECE6;   /* selected-option fill                       */
  --accent-tint:#FF8B5E;   /* the accent on a dark surface               */
  /* The accent as a GROUND under small white type. #E6430D is 4.06:1 against
     white, which clears AA for large text and misses it for the 10-16px labels
     the checkout's bar, pills, strip and tags carry. This is the same hue two
     steps down at 6.1:1, so those chips pass without the page gaining a second
     orange - nothing else may use it, and nothing that carries large type
     should. */
  --accent-deep:#B8300A;
  --accent-deeper:#8E2405;  /* the far end of the same gradients            */
  --green-ink:#15803D;      /* green as SMALL type: #16A34A is 3.36:1       */
  --ink:#171D2C;
  --title-ink:#2B313C;
  --muted:#4B5568;
  --faint:#7A8299;
  --border:#DEE2EA;
  --neutral-tint:#F2F3F5;
  --green:#00B67A;         /* rating stars only */
  --error:#D92D20;
  --dark:#12151F;

  /* Reference geometry ----------------------------------------------- */
  --page:#FFFFFF;          /* the reference page is white, not v1's grey */
  --surface:#FFFFFF;
  --track:#E7EAED;         /* progress segment, unfilled                 */
  --wash:#EFF1F5;         /* an unfilled track, a secondary button      */
  --hairline:#EDEFF3;      /* the resting outline on an option row       */
  --accent-line:#F3A184;   /* the selected row's outline — the accent,
                              softened; never the accent at full strength  */
  --glow:rgba(230,67,13,.15);   /* the selected row's halo — the resting
                                   shadow, tinted; no second stroke        */
  --col:480px;             /* the column, at every width                 */
  --pad:24px;              /* its side padding                           */
  --radius:10px;           /* Braevon's one radius — buttons, inputs     */
  --radius-card:8px;       /* the reference's option/card radius         */
  --radius-media:16px;     /* the hero video — the reference's own value */
  --shadow:0 4px 20px rgba(0,0,0,.08);      /* every raised surface      */
  --shadow-img:0 18px 44px rgba(16,20,34,.16);

  /* Vertical rhythm. The reference runs one gap between blocks (32px)
     and one between options (16px); everything else is a local margin. */
  --gap-block:32px;
  --gap-opt:16px;
  --gap-title:24px;        /* title -> first control */
}

/* ---------------------------------------------------------------- reset */
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{
  background:var(--page); color:var(--ink);
  font-family:'Plus Jakarta Sans',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  font-size:14px; line-height:1.45;
  -webkit-font-smoothing:antialiased;
}
button{font-family:inherit}
img{max-width:100%;display:block}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}

/* ---------------------------------------------------------------- shell */
.shell{max-width:var(--col);margin:0 auto;min-height:100dvh;display:flex;flex-direction:column}

/* Wordmark left, rating right — v1's masthead, kept. */
/* Two columns. The back control is absolutely positioned in the gutter rather
   than taking a slot here, so the wordmark, the progress bar and every screen's
   content share one left edge at --pad. Giving it a column indented all three. */
.masthead[hidden],.navrow[hidden]{display:none}
.masthead{
  display:grid;grid-template-columns:1fr auto;align-items:center;
  gap:12px;padding:16px var(--pad);min-height:46px;
}
.logo{display:flex;align-items:center;flex:none}
.logo svg{height:22px;width:auto;display:block}

.rating{display:flex;align-items:center;gap:8px;white-space:nowrap}
.rating .txt{font-size:11px;font-weight:700;color:var(--ink)}
/* Trustpilot sets its mark as a white glyph on a green tile, not a green
   glyph on the page. The square is the mark; --green is reserved for it. */
.stars{display:flex;gap:3px}
.stars i{width:18px;height:18px;border-radius:2px;background:var(--green);
  display:grid;place-items:center}
.stars i svg{width:12px;height:12px;color:#fff;display:block}

.rule{height:1px;background:var(--border)}

/* The reference has no back control; v1 shipped one on every screen at the
   client's request. With the wordmark on the left it cannot sit in the
   masthead, so it rides beside the progress bar — where v1 kept it too. */
/* Three columns, not a flex row: the bar has to sit centred at its own width
   with the back button beside it rather than eating into it. 24px either side
   leaves the middle cell at 384px on a 432 column, which is the reference's
   386 to within two pixels. */
/* Arrow, then bar — the reference's arrangement. The arrow lines up with the
   wordmark above it and the bar runs from there to the rating's right edge. */
.navrow{display:flex;align-items:center;gap:12px;padding:16px var(--pad) 0;height:28px}
.back-btn{
  position:relative;flex:none;
  width:24px;height:24px;display:grid;place-items:center;
  background:none;border:none;padding:0;cursor:pointer;color:var(--muted);
  border-radius:var(--radius);
}
/* 44px of hit area without a 44px layout box. Padding cannot do this — the
   global border-box would take the padding out of the 24px and crush the
   glyph instead of growing the target. */
.back-btn::after{content:"";position:absolute;inset:-10px}
.back-btn svg{width:18px;height:18px}
/* Hidden, not removed: the bar must not shift sideways between a screen with a
   back button and one without. */
.back-btn[hidden]{display:grid;visibility:hidden}

/* ------------------------------------------------------------- progress */
/* Five segments, as the reference runs it: the 24 questions are grouped into
   five sections and each segment fills across its own section, so the bar
   reads as chapters rather than as one long crawl. */
/* 58px segments with 24px between them — the reference's own geometry, which
   comes to 386px and is centred rather than filling the column. Below that the
   segments share what room there is; the gap stays put. */
/* Full measure, so its ends line up with the wordmark and the rating above.
   It was 386px centred, the reference's own width, until the client asked for
   it flush on 2026-09-02. */
.progress{display:flex;gap:24px;width:100%;min-width:0}
.seg{flex:1;height:12px;border-radius:6px;background:var(--track);overflow:hidden}
/* The reference reads its bar in two tones: a segment already behind you is
   the full accent, the one you are inside is the same hue lightened, and the
   rest are track. So "how far" and "where exactly" are both legible at a
   glance, which one flat colour cannot do. */
.seg span{display:block;height:100%;width:0;border-radius:6px;background:var(--accent);
  transition:width .32s cubic-bezier(.4,0,.2,1),background-color .32s ease}
.seg.now span{background:var(--accent-tint)}
.progress[hidden]{display:none}

/* ---------------------------------------------------------------- stage */
.stage{flex:1;padding:0 var(--pad) 32px}
.step{display:none;padding-top:var(--gap-block);animation:rise .26s ease both}
.step.on{display:block}
@keyframes rise{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){
  .step{animation:none}
  .seg span{transition:none}
}
.col{display:flex;flex-direction:column}

/* ----------------------------------------------------------- typography */
.eyebrow{
  margin:0 0 8px; font-size:10px; font-weight:700; letter-spacing:.09em;
  text-transform:uppercase; color:var(--accent);
}
.qhead{
  margin:0; font-size:22px; line-height:1.2; font-weight:600;
  letter-spacing:-.01em; color:var(--title-ink);
}
.qhead.big{font-size:26px}
.sub{margin:10px 0 0;font-size:16px;line-height:1.45;color:var(--muted)}
.qhead + .sub{margin-top:12px}
/* On an interstitial the line under the headline is carrying the claim, not
   captioning a question, and the reference sets it as a second heading:
   20px/600 in near-black, tighter. */
.sub.lead{font-size:20px;line-height:1.3;font-weight:600;color:var(--ink)}
.legend{margin:var(--gap-title) 0 10px;font-size:12px;font-weight:700;color:var(--ink)}
.foot{margin:12px 0 0;font-size:10px;line-height:1.5;color:var(--faint)}
.hi{color:var(--accent);font-weight:700}

/* Every block that follows the head gets the same gap, so a screen with a
   subtitle and one without do not drift apart. */
.qhead + *, .sub + *, .legend + *{margin-top:var(--gap-title)}
.legend{margin-top:var(--gap-block)}
/* A legend and the hint under it are one unit; the block gap belongs above the
   pair, not between its two lines. */
.legend + .sub{margin-top:0}

/* -------------------------------------------------------------- options */
.opts{display:flex;flex-direction:column;gap:var(--gap-opt)}
.opt{
  display:flex;align-items:center;gap:12px;width:100%;text-align:left;
  background:var(--surface); border:1px solid var(--hairline);
  border-radius:var(--radius-card); box-shadow:var(--shadow);
  padding:13px 16px; cursor:pointer; color:var(--ink);
  transition:border-color .12s ease,box-shadow .16s ease;
}
.opt:hover{border-color:#C9CFDA}
.opt .lbl{flex:1;font-size:14px;font-weight:500;line-height:1.2}
.opt .lbl small{display:block;margin-top:5px;font-size:10px;line-height:1.35;
  font-weight:400;color:var(--muted)}
.inline-note{font-weight:400;color:var(--muted)}

/* The ring is the single-select mark and stays a circle; the checkbox takes
   3px. That contrast is what tells one-answer from many-answers apart, and it
   is the one place the single-radius rule is deliberately broken. */
.opt .ring{
  order:-1; flex:none; width:16px;height:16px;border-radius:50%;
  border:1.5px solid #C9CFDA; background:#fff; position:relative;
}
.opt.checkbox .ring{border-radius:3px}
/* Selected is an outline and a glow, never a fill. A tinted row at this size
   reads as heavy next to four white ones, and the tint fights the icon
   bubbles, which carry colour of their own.
   The reference does this with no extra weight at all: the resting 1px hairline
   just turns accent, and the resting 0 4px 20px shadow just turns accent-tinted
   (measured: `1px solid #31ABE8` + `0 4px 20px rgba(49,171,232,.3)`). A spread
   ring on top of that is what read as a hard second stroke, so there isn't one
   — the selected row is the same row, in colour. */
/* So: the resting hairline turns a softened accent and the resting shadow
   turns accent-tinted, and nothing else changes. Same 1px, same 0 4px 20px
   geometry, same padding - which is why there is no per-variant padding
   compensation here any more. A thicker stroke or a hotter colour is what made
   the chosen row shout at the four white ones beside it. */
.opt.selected{
  border-color:var(--accent-line);
  box-shadow:0 4px 20px var(--glow);
}
.opt.selected .ring{border-color:var(--accent);background:var(--accent)}
.opt.selected .ring::after{
  content:"";position:absolute;inset:0;margin:auto;
  width:4px;height:7.5px;border:solid #fff;border-width:0 1.8px 1.8px 0;
  transform:translateY(-1px) rotate(45deg);
}
.opt:not(.checkbox).selected .ring::after{
  width:6px;height:6px;border:none;border-radius:50%;background:#fff;transform:none;
}
/* Where the exclusive answer sits is per screen - see GROUPS. Trailing, it is
   split off by a rule in the gap above. Leading, the reference gives it a green
   card: this is the answer that lets you continue, and green says so where
   orange would only say "brand". */
.opt.last{margin-top:14px;position:relative}
.opt.last::before{content:"";position:absolute;left:0;right:0;top:-8px;
  height:1px;background:var(--hairline)}
.opt.safe{background:#F0FDF4;border-color:#BBF7D0}
.opt.safe:hover{border-color:#86EFAC}
.opt.safe .lbl{font-weight:700}
.opt.safe .lbl small{color:#3F6B50}
.opt.safe.selected{border-color:#4ADE80;box-shadow:0 4px 20px rgba(34,197,94,.18)}
.opt.safe.selected .ring{border-color:#22C55E;background:#22C55E}

/* A caption breaking a long safety list into sections. It is a list heading,
   so it takes the gap above and none below - the row under it is its own. */
.optcap{margin:18px 0 -2px;font-size:17px;font-weight:700;color:var(--ink)}
.opts > .optcap:first-child{margin-top:0}
.opt-note{margin:-4px 0 0;font-size:11px;color:var(--muted);font-weight:600}

/* ------------------------------------------------ the fact interstitial */
/* Screen 2, centred on white the way the reference sets it. */
/* The reference drops the CTA to a consistent depth on its fact screens rather
   than tucking it under the copy, so the shorter the screen the wider the gap:
   its "137%" screen leaves about twice the space its "10-15 minutes" one does.
   A min-height with the button pushed to the bottom reproduces that from one
   rule instead of a per-screen margin. */
.col.fact{text-align:center;min-height:525px}
/* Two auto margins - one above the content, one above the button - split the
   free space in half, so the block sits centred between the top of the screen
   and the button rather than bunched under the progress bar. */
.col.fact > :first-child{margin-top:auto}
.col.fact .cta{margin-top:auto}
/* The one-figure screen carries a single statement rather than two stacked
   ones, so it can breathe where the two-figure screen has to stay tight. */
.col.fact.solo .fact-pill{margin-top:20px}
.col.fact.solo .fact-k{margin-top:30px}
.col.fact.solo .fact-u{margin-top:14px;line-height:1.35}
.fact-name{margin:8px 0 0;font-size:14px;font-weight:500;color:var(--muted)}
.fact-pill{
  align-self:center;margin:12px 0 0;padding:8px 20px;border-radius:999px;
  font-size:17px;font-weight:500;color:#fff;
  background:linear-gradient(90deg,var(--accent) 0%,var(--accent-tint) 100%);
}
.fact-k{margin:16px 0 0;font-size:50px;line-height:1;font-weight:600;color:var(--ink)}
/* "10-15" is a whole accented line; "36 HRS" is a coloured number against ink
   units, so there the span carries it. nth-of-type would count every <p> in
   the column, not just the figures, so the first one is marked explicitly. */
.qhead .hl{color:var(--accent)}
.fact-k.accent{color:var(--accent)}
.fact-k span{color:var(--accent)}
.fact-u{margin:3px 0 0;font-size:24px;font-weight:700;letter-spacing:.02em;color:var(--ink)}
.fact-cap{margin:7px 0 0;font-size:17px;line-height:1.4;color:var(--ink)}
.fact-cap b{font-weight:700;font-style:italic}
.fact-rule{width:34px;height:2px;background:var(--border);margin:16px auto 0;border-radius:2px}

/* Two-up cards — the sex question. No ring: with only two choices side by side
   the fill and border carry the state on their own, and the reference draws its
   own male/female question the same way. */
.opts.tilegrid{display:grid;grid-template-columns:1fr 1fr;gap:var(--gap-opt)}
.opt.tile{flex-direction:column;justify-content:center;align-items:center;
  text-align:center;gap:14px;padding:24px 20px;min-height:170px}
.opt.tile .lbl{flex:none;font-size:16px;font-weight:500}
.opt.tile .lbl small{display:block;margin-top:8px;font-size:12px;font-weight:400;
  line-height:1.35;color:var(--muted)}
/* A Yes/No that opens inside a reveal is a follow-up, not the screen's own
   question, so it takes the tile's shape at a row's height rather than the
   170px card the sex question uses. Without this v1's four safety follow-ups
   each ate most of a phone viewport. */
.reveal .opts.tilegrid .opt.tile{min-height:56px;padding:14px 16px;gap:0}
.reveal .opts.tilegrid .opt.tile .lbl{font-size:15px}
.reveal .legend{margin-top:0}
.reveal > .legend + .opts{margin-top:12px}

/* --------------------------------------------------------------- fields */
.fields{display:flex;flex-wrap:wrap;gap:12px}
/* Two field groups in a row - v1's eligibility screen puts its date selects
   above the height/weight pair - need the same 12px between them that the
   fields inside a group get, or the two rows touch. */
.dob + .fields,.fields + .fields,.fields + .dob{margin-top:12px}
.field{flex:1 1 100%;min-width:0}
.field.half{flex:1 1 calc(50% - 6px)}
.field label,.dob-label{display:block;margin:0 0 8px;font-size:17px;font-weight:500;color:var(--ink)}
/* The placeholder state, in the reference's own treatment: a select still
   showing its first option reads grey, and turns to ink once a real answer is
   chosen. Without it "January / 01" looks like data the form filled in. */
.field select[data-empty]{color:var(--faint)}
.field input::placeholder,.field textarea::placeholder,
.reveal textarea::placeholder{color:var(--faint);opacity:1}

.field input,.field select,.field textarea,.reveal textarea,.reveal input{
  width:100%;font-family:inherit;font-size:16px;color:var(--ink);
  background:var(--surface);border:1px solid var(--border);
  border-radius:var(--radius-card);padding:13px 14px;min-height:52px;
  appearance:none;-webkit-appearance:none;
}
.field textarea,.reveal textarea{min-height:104px;resize:vertical;line-height:1.45}
.field select{
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%234B5568' stroke-width='2'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E");
  background-repeat:no-repeat;background-position:right 12px center;background-size:18px;
  padding-right:38px;
}
.field input:focus,.field select:focus,.field textarea:focus,.reveal textarea:focus{
  border-color:var(--accent);outline:none;box-shadow:0 0 0 3px var(--accent-soft)
}
/* Three boxes of equal width, as the reference sizes them. */
.dob{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px}

/* -------------------------------------------------------------- reveals */
/* The one question screen the reference opens with a photograph. It sits above
   the headline, full column width, at the card radius. */
/* The molecules named under a headline: two columns, bulleted, in the caption
   grey the reference uses. Column-major, so the pairs read down then across. */
.medlist{margin:14px 0 0;padding:0 0 0 18px;list-style:disc;
  columns:2;column-gap:20px;font-size:14px;line-height:1.7;color:var(--muted)}
.medlist li{break-inside:avoid}
/* The list is part of the question, so what follows it takes the block gap
   rather than sitting straight against the last bullet. */
.medlist + *{margin-top:var(--gap-title)}

.qshot-top{margin-bottom:var(--gap-title);border-radius:var(--radius-card);
  overflow:hidden;background:var(--neutral-tint)}
/* Square, asked for on 2026-09-04: the 168px band this used to be cropped a
   tall portrait down to a strip across the eyes. A square box is close enough
   to the photograph's own 3:4 that hair, face and shoulders all survive, and
   only a little off the top and bottom is lost. `aspect-ratio` rather than a
   fixed height, so it stays square at every shell width.
   The bias is still slightly high, because a face sits above the middle of a
   portrait - tuned to man-portrait.jpg (1045x1400); retune if it is replaced. */
.qshot-top img{display:block;width:100%;aspect-ratio:1;height:auto;
  object-fit:cover;object-position:50% 15%}

.reveal{display:none;margin-top:var(--gap-block)}
.reveal.on{display:block}
.reveal label{display:block;margin:0 0 10px;font-size:17px;font-weight:700;color:var(--ink);line-height:1.3}
.reveal-sub{margin:0 0 8px;font-size:11px;color:var(--muted)}
.err{margin:8px 0 0;font-size:13px;color:var(--error);font-weight:600}
.err[hidden]{display:none}
/* A field that failed validation carries the message and the outline together,
   so the eye lands on the same place twice. */
.field.bad input,.field.bad select,.field.bad textarea{border-color:var(--error)}
.field.bad input:focus,.field.bad select:focus,.field.bad textarea:focus{
  border-color:var(--error);box-shadow:0 0 0 3px rgba(217,45,32,.14)}
.err[hidden]{display:none}

/* ----------------------------------------------------------------- note */
.note{
  display:flex;gap:12px;align-items:flex-start;
  background:var(--neutral-tint);border-radius:var(--radius-card);
  padding:14px 16px;font-size:14px;line-height:1.45;color:var(--ink);
}
/* The mark sits on the first line of the text, not on the middle of the block:
   centring it against two wrapped lines is what read as misaligned. The offset
   is half the difference between the line box and the icon. */
.note svg{flex:none;width:18px;height:18px;stroke:var(--muted);margin-top:1.5px}
.note p{margin:0}
.note b{font-weight:700;color:var(--ink)}

/* The reference's helper panel under a question - a tinted block in the accent,
   an icon, a bold line and a body. Blue there, orange here; nothing else
   differs. */
/* The reference sets "LAST STEP" as a centred gradient pill, not a caption. */
.steppill{align-self:center;margin:0 0 var(--gap-title);padding:9px 22px;
  border-radius:999px;display:inline-flex;align-items:center;gap:8px;
  font-size:17px;font-weight:700;letter-spacing:.02em;color:#fff;
  background:linear-gradient(90deg,var(--accent) 0%,var(--accent-tint) 100%)}
.steppill svg{width:17px;height:17px;stroke:#fff}

.infonote{display:flex;gap:10px;align-items:flex-start;margin-top:var(--gap-title);
  background:var(--accent-soft);border-radius:var(--radius-card);padding:14px 16px}
.infonote svg{flex:none;width:18px;height:18px;stroke:var(--accent);margin-top:1px}
.infonote b{display:block;font-size:14px;font-weight:700;color:var(--accent)}
.infonote p{margin:4px 0 0;font-size:14px;line-height:1.5;color:var(--accent-hover-ink,#8A2F12)}
.infonote b{color:#8A2F12}
/* The reference gives the button noticeably more air after one of these than
   after an ordinary block. */
.infonote + .cta{margin-top:56px}
.note.warn{background:#FEF3F2;color:#912018}
.note.warn svg{stroke:var(--error)}
.note b{color:var(--ink)}
.darknote{background:var(--dark);color:#D7DBE4;border-radius:var(--radius-card);padding:18px}
.darknote h4{margin:0 0 6px;font-size:13px;color:#fff;font-weight:700}
.darknote p{margin:0;font-size:11px;line-height:1.5}
.darknote b{color:#fff}

/* ------------------------------------------------------------------ cta */
/* Braevon's button, unchanged from v1 — orange, 10px radius, weight 800,
   arrow glyph — at the reference's full-width placement. */
/* One orange, at rest and on hover - no second shade anywhere. */
.cta{
  width:100%;border:none;border-radius:var(--radius);
  background:var(--accent);color:#fff;
  font-weight:800;font-size:13px;letter-spacing:.01em;
  padding:17px 18px;min-height:56px;
  display:flex;align-items:center;justify-content:center;gap:9px;
  cursor:pointer;transition:background-color .14s ease;
  box-shadow:0 4px 16px rgba(230,67,13,.22);
  margin-top:var(--gap-block);
}
.cta svg{width:18px;height:18px}
/* The client asked that the button never grey out: it stays orange while the
   step is unanswered and refuses the advance instead, so the affordance reads
   as available before it is. Carried over from v1 deliberately. */
.cta[data-blocked]{cursor:pointer}


/* ------------------------------------------------------- blood pressure */
.bp{display:flex;align-items:flex-start;justify-content:center;gap:14px;margin-top:var(--gap-opt)}
.cellwrap{text-align:center}
.cell{
  width:96px;text-align:center;font-size:26px;font-weight:800;color:var(--ink);
  border:1px solid var(--border);border-radius:var(--radius);padding:10px 6px;
  background:var(--surface);font-family:inherit;
}
.cell:focus{border-color:var(--accent);outline:none;box-shadow:0 0 0 3px var(--accent-soft)}
.cap{margin-top:6px;font-size:9px;color:var(--faint)}
.slash{font-size:24px;color:var(--faint);line-height:1.6}
.bp-lead{margin:var(--gap-title) 0 0;font-size:11px;color:var(--muted);text-align:center}

/* ----------------------------------------------------- the opening screen */
/* Screen 1 carries the tallest stack in the flow — hero, two-line h1, claim
   strip, question and sub, all above six 67px option rows. At the reference's
   32px block rhythm that pushes the fourth goal below the fold on a phone and
   the third below it on a 800px laptop, so this one screen runs a tighter
   rhythm than the rest. Nothing else in the flow is compressed. */
.step.s1{padding-top:24px}
/* Video, with the product render breaking out of its bottom-right corner —
   the reference's opening layout. The render is a transparent PNG, so its lift
   is a drop-shadow filter and never a box-shadow: a box-shadow follows the
   element box and would paint a rectangle behind the cut-out. */
.hero{position:relative;margin-bottom:16px}
/* 432x196. The reference's own hero box measures 342x180 in a 390 viewport —
   a 1.9 ratio, not the 1.79 this used to run — and the crop goes a little
   past that to buy the fourth option row its place above the fold. Anchored
   to the top, 196 keeps the top 68% of the photograph, which is both faces
   down to his collar; centring it here would cut the foreheads. */
.hero-media{
  width:100%;aspect-ratio:432/196;object-fit:cover;display:block;
  border-radius:var(--radius-media);background:var(--neutral-tint);
  /* The photograph is taller than 16:9 and its faces sit in the top half, so
     the crop comes off the bottom. Never centre it — that cuts the foreheads. */
  object-position:center top;
}
.hero-product{
  position:absolute;right:-2%;bottom:-18%;width:36%;height:auto;
  filter:drop-shadow(0 18px 26px rgba(16,20,34,.28)) drop-shadow(0 3px 6px rgba(16,20,34,.18));
  pointer-events:none;
}

.hero-h1{
  margin:0;font-size:34px;line-height:1.05;font-weight:600;
  letter-spacing:-.02em;color:var(--title-ink);
}
.hero-h1 .hi{font-weight:600}

/* The claim strip. The reference fades a blue through a violet; this is a flat
   --accent-soft instead, carried the full width of the box — the client asked
   for solid rather than a fade on 2026-09-02. Same token the selected option
   row uses, so the two tints cannot drift apart. */
/* Padding runs light on the right, as the reference's does, so the line has
   the room it needs to stay a single line down to the narrow breakpoint. */
.strip{
  margin:12px 0 0;padding:8px 10px 8px 12px;border-radius:var(--radius-card);
  font-size:12px;line-height:1.35;color:var(--ink);white-space:nowrap;
  background:var(--accent-soft);
}
.strip strong{font-weight:700;font-style:italic}

.ask{margin:20px 0 0;font-size:17px;line-height:1.3;font-weight:400;color:var(--ink)}
.ask strong{font-weight:700}
.ask-sub{margin:4px 0 0;font-size:14px;line-height:1.45;color:var(--muted)}
.ask-sub + .opts{margin-top:20px}

/* Goal rows are taller than an ordinary option and carry a bubble instead of a
   ring — there is nothing to compare them against yet, so the icon does the
   work the radio would. */
.opt.goal{padding:11px 16px;gap:14px;min-height:58px}
.opt.goal .bubble,.opt.band .bubble{
  flex:none;width:36px;height:36px;border-radius:50%;
  background:var(--bub,var(--accent-soft));color:var(--gly,var(--accent));
  display:grid;place-items:center;
}
.opt.goal .bubble svg,.opt.band .bubble svg{width:19px;height:19px}
/* A band row is a goal row that also carries a caption, so it keeps the gap
   but not the fixed height. */
.opt.band{gap:14px}
.opt.band .lbl{font-size:14px;font-weight:600}
.bubble.big{width:32px;height:32px;border-radius:50%;flex:none;display:grid;
  place-items:center;background:var(--bub);color:var(--gly)}
.bubble.big svg{width:16px;height:16px}


/* ------------------------------------------------------------- markety */
.media{border-radius:var(--radius-card);overflow:hidden;box-shadow:var(--shadow-img)}
.media img{width:100%;height:auto}
.statnum{color:var(--accent);font-weight:800}

.rail{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;
  margin:var(--gap-title) calc(var(--pad) * -1) 0;padding:4px var(--pad) 12px}
.tcard{flex:0 0 268px;scroll-snap-align:start;background:var(--surface);
  border-radius:var(--radius-card);box-shadow:var(--shadow);padding:16px}
.tcard h3{margin:8px 0 6px;font-size:13px;font-weight:700}
.tcard p{margin:0;font-size:11px;line-height:1.5;color:var(--muted)}
.tcard .who{margin-top:10px;font-size:10px;font-weight:700;color:var(--faint)}
.railnote{margin:0;font-size:10px;color:var(--faint);text-align:right}


.factcard{background:var(--dark);color:#fff;border-radius:var(--radius-card);
  padding:26px 22px;text-align:center}
.factcard .k{font-size:39px;font-weight:800;line-height:1;color:var(--accent-tint)}
.factcard .u{margin-top:6px;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:#98A0B4}
.factcard p{margin:10px 0 0;font-size:12px;color:#D7DBE4;line-height:1.5}


/* The onset comparison on the "4-in-1 advantage" screen. A row per molecule,
   its window drawn as a bar, with Braevon's own row picked out. */
.cmp{display:grid;grid-template-columns:1fr 96px 44px;gap:10px;align-items:center;
  padding:10px 0;border-top:1px solid var(--border)}
.cmp:first-child{border-top:none}
.cmp-l b{display:block;font-size:12px;font-weight:700;color:var(--ink)}
.cmp-l span{display:block;font-size:10px;color:var(--muted)}
.cmp-bar{height:8px;border-radius:4px;background:var(--track);overflow:hidden}
.cmp-bar i{display:block;height:100%;border-radius:4px;background:var(--accent-tint)}
.cmp-v{font-size:11px;font-weight:700;color:var(--muted);text-align:right}
.cmp.on .cmp-l b,.cmp.on .cmp-v{color:var(--accent)}
.cmp.on .cmp-bar i{background:var(--accent)}

/* the processing screens */
.loader{text-align:center;padding:24px 0}
.dial{width:132px;height:132px;margin:0 auto;position:relative}
.dial svg{transform:rotate(-90deg)}
.dial .pct{position:absolute;inset:0;display:grid;place-items:center;
  font-size:22px;font-weight:800;color:var(--ink)}
.loader h2{margin:20px 0 0;font-size:16px;font-weight:700;color:var(--title-ink)}
.checklist{margin:var(--gap-title) 0 0;display:flex;flex-direction:column;gap:10px}
.checklist div{display:flex;align-items:center;gap:10px;font-size:12px;color:var(--muted)}
.checklist i{width:18px;height:18px;border-radius:50%;border:1.5px solid var(--border);flex:none}
.checklist div.done i{background:var(--accent);border-color:var(--accent);position:relative}
.checklist div.done i::after{content:"";position:absolute;inset:0;margin:auto;
  width:4px;height:8px;border:solid #fff;border-width:0 2px 2px 0;
  transform:translateY(-1px) rotate(45deg)}
.checklist div.done{color:var(--ink);font-weight:600}

/* the result screen */
.result-badge{align-self:flex-start;display:inline-flex;align-items:center;gap:7px;background:var(--accent-soft);
  color:var(--accent);border-radius:999px;padding:7px 13px;
  font-size:10px;font-weight:800;letter-spacing:.06em;text-transform:uppercase}
.reviewcard{background:var(--surface);border-radius:var(--radius-card);
  box-shadow:var(--shadow);padding:18px;margin-top:var(--gap-title)}
.reviewcard h3{margin:0 0 14px;font-size:13px;font-weight:700}
.rrow{display:flex;justify-content:space-between;gap:14px;padding:10px 0;
  border-top:1px solid var(--border);font-size:12px}
.rrow:first-of-type{border-top:none}
.rrow span{color:var(--muted)}
.rrow b{text-align:right;font-weight:700}
.mol{display:flex;justify-content:space-between;gap:10px;padding:11px 0;border-top:1px solid var(--border)}
.mol:first-child{border-top:none}
.mol b{font-size:12px}
.mol span{font-size:10px;color:var(--muted);display:block;font-weight:400}
.mol .dose{font-size:12px;font-weight:700;color:var(--accent);white-space:nowrap}

/* Screen 5's benefit rows. Same divided card as .mol, plus the goal screen's
   36px bubble so each benefit carries its own hue, as the reference does. */
.mech{display:flex;align-items:flex-start;gap:14px;padding:14px 0;
  border-top:1px solid var(--border)}
.mech:first-child{border-top:none}
.mech .bubble{flex:none;width:36px;height:36px;border-radius:50%;
  background:var(--bub);color:var(--gly);display:grid;place-items:center}
.mech .bubble svg{width:19px;height:19px}
.mech b{font-size:13px;font-weight:700;display:block}
.mech span:not(.bubble){font-size:12px;line-height:1.5;color:var(--muted);
  display:block;font-weight:400;margin-top:3px}

/* ------------------------------------------------ the 4-in-1 advantage */
/* The reference's comparison, rebuilt: a card headed by its own title and
   lead-in, one shared time axis, a row per single-ingredient pill, and the
   brand block the whole thing builds to. */
.adv{padding:18px 16px}
.adv-h{margin:0;font-size:14px;font-weight:800;letter-spacing:.01em;color:var(--ink)}
.adv-sub{margin:6px 0 0;font-size:12px;line-height:1.5;color:var(--muted)}

/* The axis is drawn, not measured — 10m and 15m sit crowded at the left and
   36hr hard against the right, exactly as the reference spaces them. Its marks
   are absolute, so the row bars below can use the same percentages. */
.axis{display:flex;align-items:flex-end;gap:8px;margin-top:20px}
.axis-ic{flex:none;width:20px;height:20px;border-radius:50%;border:1px solid var(--accent);
  display:grid;place-items:center;color:var(--accent)}
.axis-ic svg{width:12px;height:12px}
.axis-line{position:relative;flex:1;height:26px;
  border-bottom:1px solid var(--border)}
.axis-line i{position:absolute;bottom:0;width:1px;height:6px;background:var(--border);
  transform:translateX(-50%)}
.axis-line i b{position:absolute;bottom:9px;left:50%;transform:translateX(-50%);
  font-size:9px;font-weight:700;letter-spacing:.04em;color:var(--muted);white-space:nowrap}

.advrow{margin-top:16px}
.advrow-t{display:flex;justify-content:space-between;align-items:baseline;gap:10px;
  font-size:12px}
.advrow-t b{font-weight:700;color:var(--ink)}
.advrow-t b span{font-weight:500;color:var(--muted)}
.advrow-m{font-size:11px;color:var(--muted);text-align:right}
.track{position:relative;height:12px;border-radius:999px;background:var(--wash);
  margin-top:7px;overflow:hidden}
.track i{position:absolute;top:0;bottom:0;border-radius:999px}
.track i.grad{background:linear-gradient(90deg,var(--accent-tint) 0%,var(--accent) 100%)}

/* The brand block: the only part of this screen in Braevon orange, because it
   is the only part making Braevon's claim. */
.fullpot{margin-top:22px;border:1px solid var(--accent-soft);background:#FFF9F6;
  border-radius:var(--radius-card);padding:16px}
.fp-head{display:flex;justify-content:space-between;align-items:flex-start;gap:12px}
.fp-name b{display:block;font-size:15px;font-weight:800;color:var(--accent)}
.fp-name span{display:block;margin-top:2px;font-size:9px;font-weight:800;
  letter-spacing:.12em;color:var(--muted)}
.chip{display:inline-flex;align-items:center;gap:5px;background:var(--surface);
  border:1px solid var(--hairline);border-radius:999px;padding:5px 10px;
  font-size:10px;font-weight:700;color:var(--ink);white-space:nowrap}
.chip svg{width:12px;height:12px;stroke:var(--accent);flex:none}
.fullpot .axis{margin-top:16px}
.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}
.fp-rule{height:1px;background:var(--hairline);margin:14px 0 0}
.fp-note{margin:12px 0 0;font-size:11px;line-height:1.5;color:var(--muted)}

/* ------------------------------------------------------- testimonials */
/* The reference's testimonial: one tinted panel holding a photo with the stars
   and the quote over it, two cards, and the person on a row of their own. */
.quotepanel{background:var(--neutral-tint);border-radius:12px;padding:10px;
  margin-top:var(--gap-block)}
.qshot{position:relative;margin:0;border-radius:var(--radius-card);overflow:hidden;
  background:linear-gradient(150deg,#3B2F2A,#1B1512)}
.qshot img{display:block;width:100%;height:196px;object-fit:cover}
.qshot figcaption{position:absolute;inset:0;display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:10px;padding:20px;
  background:linear-gradient(180deg,rgba(0,0,0,.32),rgba(0,0,0,.52))}
.qstars{display:flex;gap:5px;color:#FFC531}
.qstars svg{width:17px;height:17px;display:block}
.qshot blockquote{margin:0;text-align:center;color:#fff;font-size:19px;
  font-weight:700;line-height:1.3;text-wrap:balance}

.qcards{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px}
.qcard{background:var(--surface);border-radius:var(--radius-card);
  box-shadow:var(--shadow);padding:14px 12px;text-align:center}
.qcard b{display:block;font-size:13px;font-weight:700;color:var(--ink)}
.qbubs{display:flex;justify-content:center;gap:8px;margin:12px 0}
.qcard .bubble{width:36px;height:36px;border-radius:50%;flex:none;display:grid;
  place-items:center;background:var(--bub);color:var(--gly)}
.qcard .bubble svg{width:19px;height:19px}
.qcard p{margin:0;font-size:12px;line-height:1.4;color:var(--ink)}

.qwho{display:flex;align-items:center;justify-content:center;gap:10px;
  margin-top:10px;background:var(--surface);border-radius:var(--radius-card);
  box-shadow:var(--shadow);padding:12px;font-size:12px;color:var(--ink)}
.qavatar{width:28px;height:28px;border-radius:50%;flex:none;display:grid;
  place-items:center;background:#DBEAFE;color:#3B82F6;
  object-fit:cover;object-position:50% 22%}
.qavatar svg{width:16px;height:16px}

/* ------------------------------------------------------ medical review */
/* The one screen that replaces the masthead and the bar with a header of its
   own, as the reference does: a brand bar, a green confirmation, the review
   panel, then the "how it helps" block. */
.rv{gap:0}
.rv-head{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;
  background:var(--accent);color:#fff;
  padding:16px;margin:calc(var(--gap-block) * -1) calc(var(--pad) * -1) 0}
.rv-head b{display:block;font-size:19px;font-weight:800;letter-spacing:.02em}
.rv-head span{display:block;font-size:14px;color:#FDE0D4}
.rv-head-r{text-align:right}
/* Carries .rv-head so it beats the 14px set on that block's spans. */
.rv-head .rv-ready{font-size:12px;font-weight:700;color:#FFD9C7}

.rv-ok{display:flex;gap:10px;align-items:flex-start;background:#F0FDF4;
  padding:14px 16px;margin:0 calc(var(--pad) * -1)}
.rv-ok svg{flex:none;width:20px;height:20px;stroke:#16A34A;margin-top:1px}
.rv-ok b{display:block;font-size:14px;font-weight:600;color:#166534}
.rv-ok p{margin:2px 0 0;font-size:12px;line-height:1.45;color:#16A34A}

.rv-panel{background:var(--neutral-tint);border-radius:var(--radius-card);
  padding:20px 16px;margin-top:var(--gap-block)}
.rv-title{margin:0 0 16px;font-size:26px;line-height:1.2;font-weight:600;
  color:var(--ink);text-align:center}
.rv-card{background:var(--surface);border-radius:var(--radius-card);
  box-shadow:var(--shadow);padding:16px}
.rv-card + .rv-card{margin-top:12px}
/* The reference puts the label and the figure on one line and runs the bar the
   full width underneath, rather than squeezing all three into a row. */
.rv-prob-top{display:flex;align-items:center;justify-content:space-between;gap:12px}
.rv-prob-top span{font-size:16px;color:var(--muted)}
.rv-prob-top b{font-size:26px;font-weight:800;color:#16A34A;line-height:1}
.rv-bar{height:10px;border-radius:999px;background:var(--wash);overflow:hidden;
  margin-top:14px}
.rv-bar i{display:block;height:100%;border-radius:999px;background:#22C55E}

.rvrow{display:flex;align-items:flex-start;gap:12px;padding:12px 0;
  border-top:1px solid var(--border)}
.rvrow:first-child{border-top:none;padding-top:0}
.rvrow:last-child{padding-bottom:0}
.rvrow .bubble{flex:none;width:36px;height:36px;border-radius:50%;display:grid;
  place-items:center;background:var(--bub);color:var(--gly)}
.rvrow .bubble svg{width:19px;height:19px}
.rvrow b{display:block;font-size:16px;font-weight:500;color:var(--ink)}
.rvrow > div > span{display:block;margin-top:2px;font-size:14px;color:var(--ink)}
.rv-verdict{margin:16px 0 0;text-align:center;font-size:17px;font-weight:500;
  line-height:1.4;color:var(--ink)}
.rv-verdict b{font-weight:700;color:var(--accent)}

.rv-help{display:flex;gap:14px;align-items:flex-start;background:#F0FDF4;
  border-radius:var(--radius-card);padding:16px;margin-top:12px}
.rv-help img{flex:none;width:64px;height:auto;object-fit:contain}
.rv-help b{display:block;font-size:17px;font-weight:700;color:var(--title-ink)}
.rv-help p{margin:8px 0 0;font-size:14px;line-height:1.5;color:var(--ink)}
.rv-help ul{margin:12px 0 0;padding:0;list-style:none;display:grid;gap:8px}
.rv-help li{display:flex;align-items:center;gap:8px;font-size:14px;color:var(--ink)}
.rv-help li svg{flex:none;width:16px;height:16px;stroke:#16A34A}

/* ---------------------------------------------------- disqualification */
/* The eligibility stop, laid out as the reference lays it out: on white, under
   the masthead, everything centred. A card carries the mark, the title and the
   two lines; the two ways out sit under it on the page, split by a rule. It is
   not an overlay - it takes the stage's place inside the shell, so the
   masthead stays where it was and nothing slides. */
.dq{display:none;flex:1;padding:0 var(--pad) 40px}
.dq.on{display:block}
/* The completion state reuses the stop's layout - same card, green mark. The
   selectors carry .dq as well so they beat the stop's own rules, which come
   later in this block. */
.dq.done .dq-mark{background:#DCFCE7}
.dq.done .dq-mark svg{stroke:#16A34A}
.dq.done h1{color:#16A34A}
.dq.done .dq-card p + p{margin-top:12px}
.dq-inner{max-width:var(--col);margin:0 auto;text-align:center}
.dq-card{background:var(--surface);border:1px solid var(--hairline);
  border-radius:var(--radius-card);box-shadow:var(--shadow);
  padding:28px 22px 30px;margin-top:var(--gap-block)}
.dq-mark{width:44px;height:44px;border-radius:50%;background:var(--accent-soft);
  display:grid;place-items:center;margin:0 auto 16px}
.dq-mark svg{width:22px;height:22px;stroke:var(--accent)}
.dq h1{margin:0;font-size:22px;line-height:1.25;font-weight:700;color:var(--accent)}
.dq-card p{margin:16px 0 0;font-size:14px;line-height:1.5;color:var(--ink)}
/* The two exits. Each is a lead-in line and a button, sized to its label the
   way the reference sizes them - not full-bleed, or they would read as the
   flow's Next and invite a click. */
.dq-lead{margin:28px 0 0;font-size:15px;font-weight:700;color:var(--ink)}
.dq-lead.soft{font-weight:500;color:var(--ink);line-height:1.5}
.dq-rule{height:1px;background:var(--hairline);margin:30px 0 0}
.dq-back,.dq-ghost{margin:14px auto 0;display:block;min-height:44px;
  padding:0 20px;border-radius:var(--radius);font-family:inherit;
  font-size:14px;font-weight:700;cursor:pointer}
.dq-back{border:none;background:var(--accent);color:#fff}
.dq-ghost{border:none;background:var(--wash);color:var(--muted)}

/* ---------------------------------------------- approval / checkout (48) */
/* ---- one step down the ramp, 2026-09-04 ----
   Every size in this block was the reference's own, measured off its live page:
   26px headings, 16px body, 14px sub-lines. Set in **Plus Jakarta Sans** they
   read markedly larger than the reference does in Inter - bigger x-height,
   wider set - so at identical numbers the page looks heavier than the thing it
   is copying. The client asked for it brought down to match.

   So the ramp is 26/20/18/17/16/15/14 -> 23/18/17/16/15/14/13. **Sizes at 12px
   and below are untouched** - captions, badges and tags are already at the
   floor and a step there costs legibility rather than buying likeness. The
   footer block below is untouched too: those sizes are braevon.com's own.

   This is the one place the checkout departs from the measured reference on
   purpose. Do not "restore" it to the reference's numbers. */

/* The reference's approval page, measured off the live DOM on 2026-09-04 and
   restated in Braevon's font, palette and button - see `checkout.py` for what
   was copied and what could not be.

   The page is one 480px column like every other screen, so nothing here changes
   the shell. What it does do is carry its own chrome: the reference drops the
   Trustpilot rating and the progress bar on this page and shows a centred
   wordmark over a countdown bar instead, which is why the screen is `data-bare`
   and prints a masthead of its own. Three blocks bleed to the column edge
   (`ck-mast`, `ck-clock`, `ft`) with the negative-margin trick `.rv-head`
   already uses; the stage's own padding is what they are cancelling. */
.ck{gap:0}
/* Blocks are 32px apart, as the reference's Content Stack is. Written as a
   margin rather than a flex `gap` so the three chrome blocks can opt out. */
.ck > * + *{margin-top:var(--gap-block)}

.ck-mast{margin:calc(var(--gap-block) * -1) calc(var(--pad) * -1) 0;
  display:flex;justify-content:center;padding:16px var(--pad) 14px}
.ck-mast .logo svg{height:22px}
/* Full-strength `--accent`, flat, at the client's word on 2026-09-04 - it was a
   gradient of `--accent-deep`. **White on #E6430D is 4.06:1**, which clears AA
   for large text and is just under the 4.5:1 this 14px label needs; the client
   asked for the primary orange and that is the call. Raising the label to 19px
   bold would make it "large text" and clear it at 3:1, if it ever comes up.

   And it runs the **full width of the window**, not the 480 column - also the
   client's, against the reference, whose own bar stops at its column. The
   `50% - 50vw` pair is the standard full-bleed: it works because every ancestor
   up to `body` is centred and none of them clips.

   `body.frames` keeps the column-width bar. Those frames are 480px boxes on a
   grey page for the Figma import, and a viewport-wide band there would run
   across the whole document once per frame. */
.ck-clock{margin:0 calc(var(--pad) * -1);
  background:var(--accent);
  color:#fff;display:flex;align-items:center;justify-content:center;gap:6px;
  padding:15px 16px;font-size:13px;font-weight:600;text-align:center}
body:not(.frames) .ck-clock{margin-inline:calc(50% - 50vw)}
/* `clip` rather than `hidden`: it does not make body a scroll container, so
   nothing else changes. It is only here to swallow the scrollbar's width, which
   `50vw` counts and the client area does not. */
body:not(.frames){overflow-x:clip}
/* Underlined, which is v1's settled treatment for the same clock - it is the
   one part of the sentence that changes, and weight alone did not carry it. */
.ck-clock b{font-weight:800;color:#fff;text-decoration:underline;
  text-underline-offset:3px;font-variant-numeric:tabular-nums}

/* The top margin is stated here rather than left to `.ck > * + *`. That rule
   and this selector have the same specificity, so this one wins on source
   order, and a bare `margin:0` was landing the headline flush against the
   countdown bar - a real zero-gap bug, not just a tight one. 40px rather than
   the block's 32 because the client asked for more air under the bar. */
.ck-h1{margin:40px 0 0;font-size:23px;line-height:1.2;font-weight:600;
  letter-spacing:-.01em;color:var(--title-ink)}
.ck-h2{margin:0;font-size:23px;line-height:1.2;font-weight:600;
  letter-spacing:-.01em;color:var(--title-ink)}
.ck-h2 em{font-style:normal;color:var(--accent)}
/* One heading takes this - "Choose your medication preference below:" - at the
   client's word on 2026-09-04. Centred and a step down from the section ramp,
   so it reads as the lead-in to the two cards under it rather than as another
   section title. Do not widen it to `.ck-h2`; the rest stay left at 23px. */
.ck-h2.mid{text-align:center;font-size:20px}
.ck-h2.accent{color:var(--accent)}
.ck-lead{margin:10px 0 0;font-size:15px;line-height:1.45;color:var(--muted)}
.ck-sect > * + *{margin-top:var(--gap-title)}
.ck-lead + *{margin-top:var(--gap-title)}

/* -- 1 goals ------------------------------------------------------------ */
/* The reference centres this card at 345px rather than running it full width,
   so it reads as a receipt of what was answered rather than as a section. */
.ck-goals{align-self:center;max-width:345px;width:100%;
  background:var(--surface);border-radius:var(--radius-media);
  box-shadow:var(--shadow);padding:24px;
  display:flex;align-items:center;gap:16px}
.ck-goals-mark{flex:none;width:56px;height:56px;border-radius:50%;
  background:linear-gradient(135deg,var(--accent-deep) 0%,var(--accent-deeper) 100%);
  display:grid;place-items:center;color:#fff}
.ck-goals-mark svg{width:28px;height:28px}
.ck-goals b{display:block;font-size:13px;font-weight:700;color:var(--accent)}
.ck-goals ul{margin:4px 0 0;padding:0;list-style:none;display:grid;gap:2px}
.ck-goals li{display:flex;align-items:center;gap:6px;font-size:13px;color:var(--ink)}
/* One glyph per goal rather than three identical ticks, as the reference sets
   them. The hues are `GOAL_STYLE`'s - the five the client picked for screen 1,
   and the documented exception to orange carrying emphasis. */
.ck-goals li svg{flex:none;width:13px;height:13px;stroke-width:2.2}
/* The first line echoes whichever goal was picked, so its glyph has to follow.
   All five ship in the markup and `fillSummary()` shows the one that matches;
   with no answer - the static frames - the first stays on, so a frame never
   renders an empty box where an icon should be. */
.ck-goal-ic{flex:none;display:flex;width:13px;height:13px}
.ck-goal-ic i{display:none}
.ck-goal-ic i.on{display:block}

/* -- 2 intro + the onset chart ------------------------------------------ */
.ck-intro p{margin:0;font-size:15px;line-height:1.45;color:var(--muted)}
.ck-intro p + p{margin-top:16px}
.ck-intro b{font-weight:700}
/* The reference gives the chart a 20px-padded box of its own under the copy.

   The chart holds a **floor width and scrolls sideways below it**, which is the
   fallback the artwork's own source suggests. Its chip lettering is outlined
   paths scaled off a 1168-unit viewBox, so it shrinks with the box: at the 432
   this column gives it the labels read, at the 284 a 320px phone gives it they
   are about 6px. 2x is the artwork's stated ceiling - past that the chips
   collide - so the width is what has to give, not the type. There is no scroll
   at all at 480px and up, which is every case but a phone. */
/* **The chart breaks out of the text column, up to 640px.** The reference draws
   its chart 392x280 in a 432 column - 1.4:1. This artwork is 1168x521, 2.24:1,
   so at the column's 432 it comes out 193px tall and reads as a strip beside
   the reference's block. Its proportions and its lettering are not ours to
   change, so the width is what gives: at 640 it is 285px tall, which is the
   reference's 280 within five pixels, with the artwork and every label
   untouched.

   `min()` is doing the capping, so this is 480 wide in a 480 window, 640 on any
   desktop, and never wider - a full-bleed chart on a 1400px monitor would be
   625px tall. Below 420 it holds its floor and scrolls, as before.

   `body.frames` keeps it inside the column: those frames are 480px boxes and a
   640px chart would hang out of each one. */
.ck-chart{margin-top:16px;padding:20px 0;overflow-x:auto;
  -webkit-overflow-scrolling:touch}
.ck-chart svg{display:block;width:100%;min-width:420px;height:auto;margin:0 auto}
body:not(.frames) .ck-chart{margin-inline:calc(50% - 50vw)}
body:not(.frames) .ck-chart svg{width:min(100vw,640px)}

/* -- 3 the programme card ----------------------------------------------- */
.ck-prog{background:var(--surface);border-radius:var(--radius-media);
  box-shadow:var(--shadow);padding:24px}
.ck-prog-head{display:flex;align-items:center;gap:16px}
.ck-prog-mark{flex:none;width:48px;height:48px;border-radius:50%;
  background:var(--accent-soft);display:grid;place-items:center;color:var(--accent)}
.ck-prog-mark svg{width:22px;height:22px}
.ck-prog-head h2{margin:0;font-size:23px;line-height:1.2;font-weight:600;
  color:var(--accent)}
/* Copy left, render right - the reference's own split, and it does not stack:
   the render is 109px wide and the column has 384px to give.
   40px above rather than the reference's 24: the client asked on 2026-09-04 for
   more air between the "BRAEVON 4-in-1" heading and the tablet under it. */
.ck-prog-body{display:flex;align-items:center;gap:10px;margin-top:40px}
.ck-prog-body p{margin:0;font-size:15px;line-height:1.45;color:var(--muted)}
.ck-prog-body b{font-weight:700}
.ck-prog-sub{margin-top:16px !important;font-size:13px !important;color:var(--ink) !important}
.ck-prog-body img{flex:none;width:112px;height:auto;align-self:center}
.ck-prob{display:flex;align-items:center;gap:16px;margin-top:32px;
  background:linear-gradient(180deg,#FFF3EE 0%,#FFEBE2 100%);
  border-radius:var(--radius-card);padding:24px}
.ck-prob p{margin:0;flex:1;font-size:13px;line-height:1.2;color:#9A2C06}
.ck-prob b{font-weight:700}
.ck-prob-fig{flex:none;text-align:center}
.ck-prob-fig b{display:block;font-size:23px;line-height:1.2;font-weight:800;
  color:var(--accent)}
.ck-prob-fig span{display:block;font-size:12px;color:var(--ink)}

/* -- 4 the benefit rows -------------------------------------------------- */
.ck-benefits{display:flex;flex-direction:column;gap:var(--gap-opt)}
.ck-benefit{display:flex;align-items:center;gap:16px;
  background:var(--surface);border-radius:var(--radius-media);
  box-shadow:var(--shadow);padding:12px 24px;min-height:64px}
.ck-benefit .bubble{flex:none;width:36px;height:36px;border-radius:50%;
  display:grid;place-items:center;background:var(--bub);color:var(--gly)}
.ck-benefit .bubble svg{width:18px;height:18px;stroke-width:2.4}
.ck-benefit b{display:block;font-size:15px;font-weight:500;color:var(--ink)}
.ck-benefit span{display:block;font-size:13px;color:var(--ink)}

/* -- 5 what's included --------------------------------------------------- */
.ck-incl{background:#FFF8F5;border-radius:var(--radius-media);padding:24px 24px 40px}
.ck-incl-card{display:flex;align-items:flex-start;gap:24px;margin-top:32px;
  background:var(--surface);border-radius:var(--radius-card);
  box-shadow:0 4px 16px rgba(0,0,0,.08);padding:24px}
/* 96px, up from the reference's 66 - the client asked for the tablet bigger on
   2026-09-04. The copy column takes the difference and still holds four
   molecule lines at 212px. */
.ck-incl-card img{flex:none;width:96px;height:auto}
/* Flex items floor at their own min-content width, so without this the stack
   list holds the card open and the whole thing runs past the column at 320px. */
.ck-incl-card > div,.ck-prog-body > div,.ck-prod-head > div,
.ck-benefit > div,.ck-goals > div{min-width:0}
.ck-incl-title{display:flex;align-items:center;gap:12px}
.ck-incl-title b{font-size:18px;line-height:1.3;font-weight:700;color:var(--ink)}
/* Primary `--accent`, at the client's word on 2026-09-04 - it was
   `--accent-deep`. Same trade as the countdown bar: white on #E6430D is 4.06:1
   and this cap is 10px, so it is under AA. Their brand call, taken knowingly.
   This one rule is every tag on the page - the 4-in-1 stack chip, the pack tag
   on the product card and the two in the "what's included" stack - so they
   cannot drift apart. */
.ck-tag{display:inline-block;background:var(--accent);color:#fff;border-radius:4px;
  padding:4px 8px;font-size:10px;font-weight:700;letter-spacing:.04em;
  text-transform:uppercase;line-height:1}
.ck-stack{margin:12px 0 0;padding:0;list-style:none;display:grid;gap:4px}
.ck-stack li{font-size:13px;line-height:1.35;color:var(--ink)}
.ck-stack b{font-weight:700}
.ck-incl-list{margin:32px 0 0;padding:0;list-style:none;display:grid;gap:16px}
.ck-incl-list li{display:flex;align-items:flex-start;gap:10px;
  font-size:12px;font-weight:500;line-height:1.3;color:var(--ink)}
.ck-incl-list li > span{min-width:0}
.ck-incl-list svg{flex:none;width:16px;height:16px;stroke:#16A34A;stroke-width:2.6}

/* -- 6 what happens next ------------------------------------------------- */
/* The connector is a border on the item, not a pseudo-element: the reference
   runs a 5px rule down the left of every step but the last, and a border stops
   at the item's own box for free. */
.ck-steps{margin:0;padding:24px;list-style:none;
  background:var(--surface);border-radius:var(--radius-media);box-shadow:var(--shadow)}
/* #FBD0BE rather than `--accent-soft` (#FDECE6). The reference's rail is a mid
   blue and clearly reads; the soft tint is 1.06:1 against white, so the rule
   vanished and the step dots floated unconnected. */
.ck-steps li{position:relative;padding:0 0 32px 24px;border-left:5px solid #FBD0BE}
.ck-steps li:last-child{border-left-color:transparent;padding-bottom:0}
.ck-steps li::before{content:"";position:absolute;left:-10px;top:2px;
  width:15px;height:15px;border-radius:50%;background:var(--accent)}
.ck-step-n{display:block;font-size:12px;font-weight:700;letter-spacing:.06em;
  color:var(--accent)}
.ck-steps b{display:block;margin-top:8px;font-size:15px;font-weight:600;color:var(--ink)}
.ck-steps p{margin:6px 0 0;font-size:13px;line-height:1.35;color:var(--muted)}

/* -- 7 the countdown pill ------------------------------------------------ */
/* **v1's mint**, at the client's word on 2026-09-04 - `#41D8A6` ground with
   `#00462F` type, which is exactly what v1's approval screen sets its countdown
   pill to (`Approval page.pdf`, 2026-08-14) and reads at 9.4:1. It was an
   orange gradient. The bar at the top of the page stays orange: v1 ran the same
   split - a mint pill on the approval, a different ground on the checkout bar -
   so the two are not meant to be one family. */
.ck-pill{align-self:center;display:flex;align-items:center;gap:8px;
  border-radius:4px;padding:9px 16px;color:#00462F;background:#41D8A6;
  font-size:15px;font-weight:600}
.ck-pill b{font-weight:800;font-variant-numeric:tabular-nums}

/* -- 8 the packs and the product card ------------------------------------ */
.ck-packs{display:flex;gap:16px}
/* Two cards, side by side, at every width - the reference never stacks them and
   208px each fits the 432px column with its 16px between. */
.ck-pack{flex:1;min-width:0;position:relative;background:var(--surface);
  border:1px solid var(--hairline);border-radius:var(--radius-card);
  box-shadow:var(--shadow);padding:24px 12px 20px;cursor:pointer;
  font-family:inherit;text-align:center;transition:box-shadow .14s ease,border-color .14s ease}
.ck-pack.selected{border-color:var(--accent-line);box-shadow:0 4px 20px var(--glow)}
.ck-pack .ring{position:absolute;top:10px;left:10px;width:16px;height:16px;
  border-radius:50%;border:1.5px solid var(--border);background:#fff}
.ck-pack.selected .ring{border-color:var(--accent);
  box-shadow:inset 0 0 0 3.5px #fff,inset 0 0 0 9px var(--accent)}
/* Only the "most popular" card carries a badge - that is where the client's
   Figma puts it. The pair are flex siblings, so the card without one is still
   the same height; the margin below the title is what keeps the two titles on
   the same line rather than a placeholder chip. */
.ck-pack em{display:inline-block;font-style:normal;border-radius:4px;
  padding:4px 8px;font-size:10px;font-weight:700;color:#fff;letter-spacing:.03em;
  line-height:1}
.ck-pack b{display:block;margin-top:12px;font-size:18px;font-weight:700;
  color:var(--accent);line-height:1.3}
.ck-pack:not(:has(em)) b{margin-top:33px}
.ck-pack small{display:block;font-size:13px;line-height:1.35;color:var(--ink)}

.ck-prod{margin-top:16px;background:var(--surface);border-radius:var(--radius-media);
  box-shadow:var(--shadow);padding:24px}
.ck-prod-head{display:flex;align-items:flex-start;justify-content:space-between;gap:10px}
.ck-prod-head b{display:block;margin-top:6px;font-size:18px;font-weight:600;
  color:var(--ink);line-height:1.3}
.ck-prod-head small{display:block;font-size:16px;font-weight:500;color:var(--title-ink)}
.ck-prod-rate{flex:none;text-align:right}
.ck-prod-rate .stars{justify-content:flex-end}
/* `:not(.stars)` is load-bearing. The rating mark is itself a `<span class=
   "stars">`, and a bare `.ck-prod-rate span` outranks `.stars`'s own
   `display:flex` on specificity - which turned the five tiles into a vertical
   column. Anything added here that styles `span` needs the same guard. */
.ck-prod-rate > span:not(.stars){display:block;margin-top:4px;font-size:12px;
  color:var(--ink)}
/* The render sits on the reference's own wash panel; ours is warmed to the
   brand rather than kept blue. */
.ck-prod-shot{margin-top:24px;border-radius:var(--radius-card);
  background:linear-gradient(180deg,#FAFAFA 0%,#FFEFE8 100%);
  display:grid;place-items:center;padding:20px}
.ck-prod-shot img{width:150px;height:auto}
.ck-prod-price{margin:24px 0 0;text-align:center;font-size:17px;font-weight:500;
  color:var(--title-ink)}
.ck-prod-price b{font-weight:700;color:var(--green-ink)}
.ck-prod-list{margin:20px 0 0;padding:0;list-style:none;display:grid;gap:16px}
.ck-prod-list li{display:flex;align-items:flex-start;gap:10px;
  font-size:12px;font-weight:500;line-height:1.3;color:var(--ink)}
.ck-prod-list svg{flex:none;width:16px;height:16px;stroke:#16A34A;stroke-width:2.6}
/* The text is one flex item, so a bold lead-in and the sentence after it set as
   a single wrapping paragraph. Without the span the bare text node became a
   second anonymous flex item and "Price includes:" got a column of its own. */
.ck-prod-list li > span{min-width:0}
.ck-prod-list b{font-weight:700}

/* -- 9 HSA and HIPAA ----------------------------------------------------- */
/* The reference sets this as a mark, not a chip: a circled tick beside
   "HSA/FSA Eligible" in the page's own ink, centred on the ground with no pill
   and no border. It was an outlined green capsule until the client asked for it
   matched on 2026-09-04. The ring is v1's own `hsa` glyph. */
.ck-hsa{display:flex;align-items:center;justify-content:center;gap:10px}
.ck-hsa svg{flex:none;width:30px;height:30px;color:var(--green-ink)}
.ck-hsa p{margin:0;font-size:17px;font-weight:500;color:var(--ink);letter-spacing:-.01em}
.ck-hsa b{font-weight:800}
.ck-hipaa{margin-top:16px !important;background:var(--surface);
  border-radius:var(--radius-media);box-shadow:var(--shadow);
  padding:24px 24px 32px;text-align:center}
.ck-hipaa p{margin:0;display:flex;align-items:center;justify-content:center;gap:5px;
  font-size:12px;color:var(--ink)}
.ck-hipaa svg{width:16px;height:16px;stroke:#16A34A}
.ck-hipaa span{display:block;margin-top:3px;font-size:12px;color:var(--ink)}

/* -- 10 / 14 the guarantee ---------------------------------------------- */
.ck-guar{display:flex;align-items:flex-start;gap:16px}
.ck-guar-mark{flex:none;width:33px;height:33px;color:var(--accent)}
.ck-guar-mark svg{width:33px;height:33px}
.ck-guar b{display:block;font-size:15px;font-weight:500;color:var(--ink)}
.ck-guar p{margin:2px 0 0;font-size:13px;line-height:1.35;color:var(--ink)}

/* -- 11 -----------------------------------------------------------------
   Nothing here. The reference's "BACKED BY RESEARCH FROM" logo row is not
   built - see the note in checkout.py - and the "as featured on" row that stood
   in for it came out on 2026-09-04 at the client's word, styles and all. */

/* -- 12 the quotes ------------------------------------------------------- */
.ck-quotes{display:flex;flex-direction:column;gap:24px}
.ck-quote{background:linear-gradient(135deg,#FFF7F4 0%,#FFF4F0 100%);
  border-radius:var(--radius-media);padding:24px}
.ck-quote-top{display:flex;align-items:flex-start;gap:16px}
.ck-quote-top h3{margin:0;flex:1;font-size:16px;font-weight:500;line-height:1.35;
  color:var(--title-ink)}
.ck-quote-top .stars{flex:none}
.ck-quote > p{margin:16px 0 0;font-size:13px;line-height:1.35;color:var(--ink)}
.ck-who{display:flex;align-items:center;justify-content:space-between;gap:8px;
  margin-top:16px}
.ck-who b{font-size:15px;font-weight:500;color:var(--ink)}
.ck-who span{display:flex;align-items:center;gap:4px;font-size:12px;color:var(--ink)}
.ck-who svg{width:15px;height:15px;stroke:#16A34A;stroke-width:2.6}

/* -- 13 are you ready ---------------------------------------------------- */
.ck-ready > * + *{margin-top:16px}
.ck-ready-tag{display:inline-block;border-radius:33px;padding:16px 24px;
  background:linear-gradient(90deg,#FFD9C7 0%,rgba(255,217,199,0) 100%);
  font-size:15px;font-weight:500;color:var(--ink)}
.ck-ready-clock{display:inline-flex;align-items:center;gap:5px;
  background:var(--surface);padding:6px 8px;font-size:12px;color:var(--muted)}
.ck-ready-clock b{font-weight:700;color:var(--accent);font-variant-numeric:tabular-nums}
.ck-ready-strip{display:flex;align-items:center;border-radius:4px;padding:10px 16px;
  background:linear-gradient(90deg,var(--accent-deep) 0%,var(--accent-deeper) 100%);
  color:#fff;font-size:12px}
.ck-ready-strip b{font-weight:900}
/* The reference runs a 4px rule down the left of the clock / strip / line
   group with an arrow head at its foot, pointing at the card below. It is one
   border on the group rather than three, and the head is a rotated caret. */
.ck-ready-rail{position:relative;padding-left:32px;
  border-left:4px solid var(--accent-soft);margin-top:24px !important}
.ck-ready-rail > * + *{margin-top:16px}
.ck-ready-rail::after{content:"";position:absolute;left:-9px;bottom:-6px;
  width:14px;height:14px;border-right:4px solid var(--accent-soft);
  border-bottom:4px solid var(--accent-soft);transform:rotate(45deg);
  border-bottom-right-radius:3px}
.ck-ready-line{margin:0;font-size:18px;font-weight:600;
  line-height:1.3;color:var(--ink)}
.ck-ready-card{background:var(--surface);border-radius:var(--radius-media);
  box-shadow:var(--shadow);padding:24px;margin-top:32px !important}
.ck-ready-card h3{margin:0;font-size:18px;font-weight:600;color:var(--ink)}
.ck-ready-list{margin:32px 0 0;padding:0;list-style:none;display:grid;gap:24px}
.ck-ready-list li{display:flex;align-items:flex-start;gap:16px}
.ck-ready-list svg{flex:none;width:20px;height:20px;stroke:var(--accent);stroke-width:2.4}
.ck-ready-list b{display:block;font-size:15px;font-weight:500;color:var(--ink)}
.ck-ready-list span{display:block;margin-top:2px;font-size:12px;color:var(--muted)}
.ck-ready-packs{display:flex;gap:24px;margin-top:32px;
  background:linear-gradient(180deg,#FAFAFA 0%,#FFEFE8 100%);
  border-radius:var(--radius-card);padding:24px}
.ck-ready-pack{flex:1;min-width:0}
.ck-ready-pack b{display:block;margin-top:8px;font-size:18px;font-weight:600;
  line-height:1.3;color:var(--ink)}
.ck-ready-pack em{display:block;margin-top:8px;font-style:normal;font-size:18px;
  font-weight:700;color:#16A34A}
.ck-ready-note{margin:24px auto 0;max-width:270px;text-align:center;
  font-size:12px;line-height:1.3;color:var(--muted)}
.ck-ready-note b{font-weight:700}
.ck-ready-card .cta{margin-top:24px}

/* -- 15 the FAQ ---------------------------------------------------------- */
.ck-faq{background:linear-gradient(180deg,#FFF3EE 0%,#FFF9F7 100%);
  border-radius:12px;padding:32px}
.ck-faq h2{margin:0 0 24px;text-align:center;font-size:18px;font-weight:600;
  color:var(--accent)}
.ck-faq-item{border-top:1px solid #FFE0D3}
.ck-faq-item:first-of-type{border-top:none}
.ck-faq-item summary{display:flex;align-items:flex-start;gap:10px;
  list-style:none;cursor:pointer;padding:14px 0;
  font-size:13px;line-height:1.35;color:var(--title-ink)}
.ck-faq-item summary::-webkit-details-marker{display:none}
.ck-faq-item summary svg{order:2;flex:none;width:16px;height:16px;margin-left:auto;
  stroke:var(--accent);transition:transform .16s ease}
.ck-faq-item[open] summary svg{transform:rotate(180deg)}
.ck-faq-item p{margin:0 0 16px;font-size:13px;line-height:1.5;color:var(--muted)}

/* ------------------------------------------------------------- footer */
/* braevon.com's own footer, its phone variant, in white rather than the site's
   #141414 - and without the full-width wordmark it prints at the very bottom.
   Bleeds to the column edge and eats the stage's bottom padding, so it sits
   flush at the foot of the page the way the site's does. */
.ft{margin:var(--gap-block) calc(var(--pad) * -1) -32px;
  border-top:1px solid var(--border);background:var(--page)}
.ft-in{padding:40px var(--pad) 32px;display:flex;flex-direction:column;gap:30px}
/* The site sets its footer mark at 179px in a 338px column. Held to that
   proportion here it would be 229px wide, which is a different design; 34px
   tall (~132px) keeps it clearly larger than the masthead's 22px without
   turning the footer into a second brand statement. */
.ft-mark svg{height:34px;width:auto}
.ft-tag{margin:17px 0 0;font-size:14px;line-height:1.6;letter-spacing:-.02em;
  color:var(--muted)}
.ft-contact{margin-top:20px;display:grid;gap:5px}
.ft-contact span{display:flex;align-items:center;gap:10px;font-size:12px;
  letter-spacing:-.02em;color:var(--muted)}
.ft-contact svg{flex:none;width:20px;height:20px;color:var(--faint)}
.ft-contact a{color:var(--muted);text-decoration:none}
.ft-contact a:hover{color:var(--accent)}
.ft-rule{height:1px;background:var(--border)}
.ft-legal p{margin:0;font-size:13px;line-height:1.4;letter-spacing:-.03em;
  color:var(--muted)}
.ft-legal p + p{margin-top:10px}
.ft-bottom{display:flex;flex-direction:column;gap:21px}
.ft-bot-top{display:flex;align-items:flex-end;justify-content:space-between;gap:16px}
.ft-seal{flex:none;width:63px;height:auto}
.ft-links{display:flex;flex-direction:column;gap:5px;align-items:flex-start}
.ft-links a{font-size:12px;letter-spacing:-.02em;color:var(--muted);text-decoration:none}
.ft-links a:hover{color:var(--accent)}
.ft-bot-row{display:flex;align-items:center;justify-content:space-between;gap:12px;
  font-size:12px;letter-spacing:-.03em;color:var(--muted)}
.ft-social{display:flex;align-items:center;gap:11px}
.ft-social a{color:var(--muted);display:block}
.ft-social a:hover{color:var(--accent)}
.ft-social svg{width:22px;height:22px;display:block}

/* ------------------------------------------------------------- narrow */
@media (max-width:420px){ .hero-h1{font-size:31px} .strip{font-size:11px} }
@media (max-width:379px){
  :root{--pad:18px;--gap-block:26px}
  .qhead{font-size:20px}
  .hero-h1{font-size:27px}
  .strip{white-space:normal}
  /* The checkout at 320px. Only the three two-column cards need anything: each
     pairs a fixed-width render with a text column, and the text is what runs
     out of room first. The pack pair is left alone - it is two 130px cards at
     this width and still reads. */
  .ck-h1,.ck-h2,.ck-prog-head h2{font-size:22px}
  .ck-incl,.ck-faq{padding:20px}
  .ck-incl-card{gap:16px;padding:18px}
  .ck-incl-card img{width:52px}
  .ck-prog-body img{width:88px}
  .ck-ready-packs{gap:16px;padding:18px}
  .ck-ready-line{font-size:18px}
}

/* ------------------------------------------------- all-screens document */
/* Only the static export uses these: each screen becomes its own frame so the
   file imports into Figma one frame per screen. */
body.frames{background:#DDE1E7;padding:40px 0}
body.frames .frame{background:var(--page);width:var(--col);margin:0 auto 40px;
  box-shadow:0 10px 40px rgba(16,20,34,.16)}
body.frames .frame .step{display:block}
body.frames .frame-label{max-width:var(--col);margin:0 auto 8px;font-size:10px;
  font-weight:700;color:#5A6377;letter-spacing:.04em}
body.frames .dq{position:static;display:block}
"""
