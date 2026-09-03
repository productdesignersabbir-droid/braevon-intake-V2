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
  --accent-hover:#7C0E0C;  /* button hover + focus ring                  */
  --accent-soft:#FDECE6;   /* selected-option fill                       */
  --accent-tint:#FF8B5E;   /* the accent on a dark surface               */
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
:focus-visible{outline:2px solid var(--accent-hover);outline-offset:2px}

/* ---------------------------------------------------------------- shell */
.shell{max-width:var(--col);margin:0 auto;min-height:100dvh;display:flex;flex-direction:column}

/* Wordmark left, rating right — v1's masthead, kept. */
/* Two columns. The back control is absolutely positioned in the gutter rather
   than taking a slot here, so the wordmark, the progress bar and every screen's
   content share one left edge at --pad. Giving it a column indented all three. */
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
.back-btn:hover{background:var(--neutral-tint);color:var(--ink)}
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
/* The exclusive answer is the list's last row and is split off from it, the
   way the reference splits it - a rule in the gap above, not a heavier row. */
.opt.last{margin-top:14px;position:relative}
.opt.last::before{content:"";position:absolute;left:0;right:0;top:-8px;
  height:1px;background:var(--hairline)}
.opt-note{margin:-4px 0 0;font-size:11px;color:var(--muted);font-weight:600}

/* ------------------------------------------------ the fact interstitial */
/* Screen 2, centred on white the way the reference sets it. */
.col.fact{text-align:center}
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

/* --------------------------------------------------------------- fields */
.fields{display:flex;flex-wrap:wrap;gap:12px}
.field{flex:1 1 100%;min-width:0}
.field.half{flex:1 1 calc(50% - 6px)}
.field label,.dob-label{display:block;margin:0 0 6px;font-size:11px;font-weight:600;color:var(--muted)}
.field input,.field select,.field textarea,.reveal textarea,.reveal input{
  width:100%;font-family:inherit;font-size:16px;color:var(--ink);
  background:var(--surface);border:1px solid var(--border);
  border-radius:var(--radius);padding:13px;min-height:50px;
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
.dob{display:grid;grid-template-columns:1.3fr .8fr 1fr;gap:8px}

/* -------------------------------------------------------------- reveals */
.reveal{display:none;margin-top:var(--gap-opt)}
.reveal.on{display:block}
.reveal label{display:block;margin:0 0 8px;font-size:12px;font-weight:600;color:var(--ink)}
.reveal-sub{margin:0 0 8px;font-size:11px;color:var(--muted)}
.err{margin:8px 0 0;font-size:11px;color:var(--error);font-weight:600}
.err[hidden]{display:none}

/* ----------------------------------------------------------------- note */
.note{
  display:flex;gap:10px;align-items:flex-start;
  background:var(--neutral-tint);border-radius:var(--radius-card);
  padding:14px;font-size:11px;line-height:1.5;color:var(--muted);
}
.note svg{flex:none;width:18px;height:18px;stroke:var(--muted);margin-top:1px}
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
.cta:hover{background:var(--accent-hover)}
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

.quote{background:var(--surface);border-radius:var(--radius-card);
  box-shadow:var(--shadow);padding:22px}
.quote blockquote{margin:10px 0 0;font-size:16px;line-height:1.35;font-weight:600;color:var(--title-ink)}
.quote .meta{display:flex;gap:10px;margin-top:16px;flex-wrap:wrap}
.qmeta{flex:1 1 calc(50% - 5px);background:var(--neutral-tint);border-radius:6px;padding:10px}
.qmeta b{display:block;font-size:9px;letter-spacing:.08em;text-transform:uppercase;color:var(--faint)}
.qmeta span{font-size:11px;font-weight:600;color:var(--ink)}
.quote .who{margin-top:14px;font-size:11px;font-weight:700;color:var(--muted)}

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
  color:var(--accent-hover);border-radius:999px;padding:7px 13px;
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

/* ---------------------------------------------------- disqualification */
/* The eligibility stop, laid out as the reference lays it out: on white, under
   the masthead, everything centred. A card carries the mark, the title and the
   two lines; the two ways out sit under it on the page, split by a rule. It is
   not an overlay - it takes the stage's place inside the shell, so the
   masthead stays where it was and nothing slides. */
.dq{display:none;flex:1;padding:0 var(--pad) 40px}
.dq.on{display:block}
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
.dq-back:hover{background:var(--accent-hover)}
.dq-ghost{border:none;background:var(--wash);color:var(--muted)}
.dq-ghost:hover{background:#E7EAF0}

/* ------------------------------------------------------------- narrow */
@media (max-width:420px){ .hero-h1{font-size:31px} .strip{font-size:11px} }
@media (max-width:379px){
  :root{--pad:18px;--gap-block:26px}
  .qhead{font-size:20px}
  .hero-h1{font-size:27px}
  .strip{white-space:normal}
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
