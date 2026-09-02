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
  font-size:16px; line-height:1.45;
  -webkit-font-smoothing:antialiased;
}
button{font-family:inherit}
img{max-width:100%;display:block}
:focus-visible{outline:2px solid var(--accent-hover);outline-offset:2px}

/* ---------------------------------------------------------------- shell */
.shell{max-width:var(--col);margin:0 auto;min-height:100dvh;display:flex;flex-direction:column}

/* Wordmark left, rating right — v1's masthead, kept. */
.masthead{
  display:flex;align-items:center;justify-content:space-between;
  padding:16px var(--pad); gap:16px; min-height:46px;
}
.logo{display:flex;align-items:center;flex:none}
.logo svg{height:22px;width:auto;display:block}

.rating{display:flex;align-items:center;gap:8px;white-space:nowrap}
.rating .txt{font-size:13px;font-weight:700;color:var(--ink)}
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
.navrow{display:flex;align-items:center;gap:12px;padding:16px var(--pad) 0;height:28px}
.back-btn{
  width:32px;height:32px;flex:none;display:grid;place-items:center;
  background:none;border:none;padding:0;cursor:pointer;color:var(--muted);
  border-radius:var(--radius);
}
.back-btn svg{width:19px;height:19px}
.back-btn:hover{background:var(--neutral-tint);color:var(--ink)}
/* Hidden, not removed: the bar must not shift sideways between a screen with a
   back button and one without. */
.back-btn[hidden]{display:grid;visibility:hidden}

/* ------------------------------------------------------------- progress */
/* Five segments, as the reference runs it: the 24 questions are grouped into
   five sections and each segment fills across its own section, so the bar
   reads as chapters rather than as one long crawl. */
.progress{flex:1;display:flex;gap:8px;min-width:0}
.seg{flex:1;height:12px;border-radius:6px;background:var(--track);overflow:hidden}
.seg span{display:block;height:100%;width:0;border-radius:6px;background:var(--accent);
  transition:width .32s cubic-bezier(.4,0,.2,1)}
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
  margin:0 0 8px; font-size:12px; font-weight:700; letter-spacing:.09em;
  text-transform:uppercase; color:var(--accent);
}
.qhead{
  margin:0; font-size:26px; line-height:1.2; font-weight:600;
  letter-spacing:-.01em; color:var(--title-ink);
}
.qhead.big{font-size:30px}
.sub{margin:10px 0 0;font-size:15px;line-height:1.5;color:var(--muted)}
.legend{margin:var(--gap-title) 0 10px;font-size:14px;font-weight:700;color:var(--ink)}
.foot{margin:12px 0 0;font-size:12px;line-height:1.5;color:var(--faint)}
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
  background:var(--surface); border:1.5px solid transparent;
  border-radius:var(--radius-card); box-shadow:var(--shadow);
  padding:16px; cursor:pointer; color:var(--ink);
  transition:border-color .12s ease,background-color .12s ease;
}
.opt:hover{border-color:#C9CFDA}
.opt .lbl{flex:1;font-size:16px;font-weight:500;line-height:1.2}
.opt .lbl small{display:block;margin-top:5px;font-size:12px;line-height:1.35;
  font-weight:400;color:var(--muted)}
.inline-note{font-weight:400;color:var(--muted)}

/* The ring is the single-select mark and stays a circle; the checkbox takes
   3px. That contrast is what tells one-answer from many-answers apart, and it
   is the one place the single-radius rule is deliberately broken. */
.opt .ring{
  order:-1; flex:none; width:20px;height:20px;border-radius:50%;
  border:1.5px solid #C9CFDA; background:#fff; position:relative;
}
.opt.checkbox .ring{border-radius:3px}
.opt.selected{border-color:var(--accent);background:var(--accent-soft)}
.opt.selected .ring{border-color:var(--accent);background:var(--accent)}
.opt.selected .ring::after{
  content:"";position:absolute;inset:0;margin:auto;
  width:5px;height:9px;border:solid #fff;border-width:0 2px 2px 0;
  transform:translateY(-1px) rotate(45deg);
}
.opt:not(.checkbox).selected .ring::after{
  width:7px;height:7px;border:none;border-radius:50%;background:#fff;transform:none;
}
.opt-note{margin:-4px 0 0;font-size:13px;color:var(--muted);font-weight:600}

/* Two-up cards — the sex question. No ring: with only two choices side by side
   the fill and border carry the state on their own, and the reference draws its
   own male/female question the same way. */
.opts.tilegrid{display:grid;grid-template-columns:1fr 1fr;gap:var(--gap-opt)}
.opt.tile{justify-content:center;text-align:center;padding:22px 16px}
.opt.tile .lbl{flex:none;font-weight:600}

/* --------------------------------------------------------------- fields */
.fields{display:flex;flex-wrap:wrap;gap:12px}
.field{flex:1 1 100%;min-width:0}
.field.half{flex:1 1 calc(50% - 6px)}
.field label,.dob-label{display:block;margin:0 0 6px;font-size:13px;font-weight:600;color:var(--muted)}
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
.reveal label{display:block;margin:0 0 8px;font-size:14px;font-weight:600;color:var(--ink)}
.reveal-sub{margin:0 0 8px;font-size:13px;color:var(--muted)}
.err{margin:8px 0 0;font-size:13px;color:var(--error);font-weight:600}
.err[hidden]{display:none}

/* ----------------------------------------------------------------- note */
.note{
  display:flex;gap:10px;align-items:flex-start;
  background:var(--neutral-tint);border-radius:var(--radius-card);
  padding:14px;font-size:13.5px;line-height:1.5;color:var(--muted);
}
.note svg{flex:none;width:18px;height:18px;stroke:var(--muted);margin-top:1px}
.note.warn{background:#FEF3F2;color:#912018}
.note.warn svg{stroke:var(--error)}
.note b{color:var(--ink)}
.darknote{background:var(--dark);color:#D7DBE4;border-radius:var(--radius-card);padding:18px}
.darknote h4{margin:0 0 6px;font-size:15px;color:#fff;font-weight:700}
.darknote p{margin:0;font-size:13.5px;line-height:1.5}
.darknote b{color:#fff}

/* ------------------------------------------------------------------ cta */
/* Braevon's button, unchanged from v1 — orange, 10px radius, weight 800,
   arrow glyph — at the reference's full-width placement. */
.cta{
  width:100%;border:none;border-radius:var(--radius);
  background:var(--accent);color:#fff;
  font-weight:800;font-size:15.5px;letter-spacing:.01em;
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

.privacy{
  display:flex;align-items:center;justify-content:center;gap:7px;
  margin:14px 0 0;font-size:12px;color:var(--faint);text-align:center;
}
.privacy svg{width:13px;height:13px;stroke:var(--faint);fill:none;flex:none}

/* ------------------------------------------------------- blood pressure */
.bp{display:flex;align-items:flex-start;justify-content:center;gap:14px;margin-top:var(--gap-opt)}
.cellwrap{text-align:center}
.cell{
  width:96px;text-align:center;font-size:30px;font-weight:800;color:var(--ink);
  border:1px solid var(--border);border-radius:var(--radius);padding:10px 6px;
  background:var(--surface);font-family:inherit;
}
.cell:focus{border-color:var(--accent);outline:none;box-shadow:0 0 0 3px var(--accent-soft)}
.cap{margin-top:6px;font-size:11px;color:var(--faint)}
.slash{font-size:28px;color:var(--faint);line-height:1.6}
.bp-lead{margin:var(--gap-title) 0 0;font-size:13px;color:var(--muted);text-align:center}

/* ----------------------------------------------------- the opening screen */
/* Video, with the product render breaking out of its bottom-right corner —
   the reference's opening layout. The render is a transparent PNG, so its lift
   is a drop-shadow filter and never a box-shadow: a box-shadow follows the
   element box and would paint a rectangle behind the cut-out. */
.hero{position:relative;margin-bottom:21px}
.hero-media{
  width:100%;aspect-ratio:432/241;object-fit:cover;display:block;
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
  margin:0;font-size:44px;line-height:1.1;font-weight:700;
  letter-spacing:-.02em;color:var(--title-ink);
}
.hero-h1 .hi{font-weight:700}

/* The claim strip. The reference fades a blue through a violet; this is the one
   accent, faded out to the right, so it stays inside house rule 2. */
.strip{
  margin:15px 0 0;padding:9px 14px;border-radius:var(--radius-card);
  font-size:13px;line-height:1.35;color:var(--ink);white-space:nowrap;
  background:linear-gradient(90deg,rgba(230,67,13,.16) 0%,rgba(230,67,13,.06) 55%,rgba(230,67,13,0) 100%);
}
.strip strong{font-weight:800;font-style:italic}

.ask{margin:24px 0 0;font-size:20px;line-height:1.3;font-weight:400;color:var(--ink)}
.ask strong{font-weight:800}
.ask-sub{margin:5px 0 0;font-size:16px;color:var(--muted)}
.ask-sub + .opts{margin-top:24px}

/* Goal rows are taller than an ordinary option and carry a bubble instead of a
   ring — there is nothing to compare them against yet, so the icon does the
   work the radio would. */
.opt.goal{padding:14px 16px;gap:14px;min-height:67px}
.opt.goal .bubble{
  flex:none;width:36px;height:36px;border-radius:50%;
  background:var(--bub,var(--accent-soft));color:var(--gly,var(--accent));
  display:grid;place-items:center;
}
.opt.goal .bubble svg{width:19px;height:19px}
/* The row's own selected tint would muddy the bubble, so it goes white and
   the glyph keeps its hue. */
.opt.goal.selected .bubble{background:#fff}

/* ------------------------------------------------------------- markety */
.media{border-radius:var(--radius-card);overflow:hidden;box-shadow:var(--shadow-img)}
.media img{width:100%;height:auto}
.statnum{color:var(--accent);font-weight:800}

.rail{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;
  margin:var(--gap-title) calc(var(--pad) * -1) 0;padding:4px var(--pad) 12px}
.tcard{flex:0 0 268px;scroll-snap-align:start;background:var(--surface);
  border-radius:var(--radius-card);box-shadow:var(--shadow);padding:16px}
.tcard h3{margin:8px 0 6px;font-size:15px;font-weight:700}
.tcard p{margin:0;font-size:13.5px;line-height:1.5;color:var(--muted)}
.tcard .who{margin-top:10px;font-size:12px;font-weight:700;color:var(--faint)}
.railnote{margin:0;font-size:12px;color:var(--faint);text-align:right}

.tiles{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:var(--gap-title)}
.tile{background:var(--surface);border-radius:var(--radius-card);box-shadow:var(--shadow);padding:14px}
.tile b{display:block;font-size:14px;color:var(--ink)}
.tile span{display:block;margin-top:3px;font-size:12px;color:var(--muted)}

.factcard{background:var(--dark);color:#fff;border-radius:var(--radius-card);
  padding:26px 22px;text-align:center}
.factcard .k{font-size:46px;font-weight:800;line-height:1;color:var(--accent-tint)}
.factcard .u{margin-top:6px;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#98A0B4}
.factcard p{margin:10px 0 0;font-size:14px;color:#D7DBE4;line-height:1.5}

.quote{background:var(--surface);border-radius:var(--radius-card);
  box-shadow:var(--shadow);padding:22px}
.quote blockquote{margin:10px 0 0;font-size:19px;line-height:1.35;font-weight:600;color:var(--title-ink)}
.quote .meta{display:flex;gap:10px;margin-top:16px;flex-wrap:wrap}
.qmeta{flex:1 1 calc(50% - 5px);background:var(--neutral-tint);border-radius:6px;padding:10px}
.qmeta b{display:block;font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--faint)}
.qmeta span{font-size:13px;font-weight:600;color:var(--ink)}
.quote .who{margin-top:14px;font-size:13px;font-weight:700;color:var(--muted)}

/* the processing screens */
.loader{text-align:center;padding:24px 0}
.dial{width:132px;height:132px;margin:0 auto;position:relative}
.dial svg{transform:rotate(-90deg)}
.dial .pct{position:absolute;inset:0;display:grid;place-items:center;
  font-size:26px;font-weight:800;color:var(--ink)}
.loader h2{margin:20px 0 0;font-size:19px;font-weight:700;color:var(--title-ink)}
.checklist{margin:var(--gap-title) 0 0;display:flex;flex-direction:column;gap:10px}
.checklist div{display:flex;align-items:center;gap:10px;font-size:14px;color:var(--muted)}
.checklist i{width:18px;height:18px;border-radius:50%;border:1.5px solid var(--border);flex:none}
.checklist div.done i{background:var(--accent);border-color:var(--accent);position:relative}
.checklist div.done i::after{content:"";position:absolute;inset:0;margin:auto;
  width:4px;height:8px;border:solid #fff;border-width:0 2px 2px 0;
  transform:translateY(-1px) rotate(45deg)}
.checklist div.done{color:var(--ink);font-weight:600}

/* the result screen */
.result-badge{align-self:flex-start;display:inline-flex;align-items:center;gap:7px;background:var(--accent-soft);
  color:var(--accent-hover);border-radius:999px;padding:7px 13px;
  font-size:12px;font-weight:800;letter-spacing:.06em;text-transform:uppercase}
.reviewcard{background:var(--surface);border-radius:var(--radius-card);
  box-shadow:var(--shadow);padding:18px;margin-top:var(--gap-title)}
.reviewcard h3{margin:0 0 14px;font-size:15px;font-weight:700}
.rrow{display:flex;justify-content:space-between;gap:14px;padding:10px 0;
  border-top:1px solid var(--border);font-size:14px}
.rrow:first-of-type{border-top:none}
.rrow span{color:var(--muted)}
.rrow b{text-align:right;font-weight:700}
.mol{display:flex;justify-content:space-between;gap:10px;padding:11px 0;border-top:1px solid var(--border)}
.mol:first-child{border-top:none}
.mol b{font-size:14px}
.mol span{font-size:12px;color:var(--muted);display:block;font-weight:400}
.mol .dose{font-size:14px;font-weight:700;color:var(--accent);white-space:nowrap}

/* ---------------------------------------------------- disqualification */
/* The one full-bleed dark surface in the flow, because it is a stop and not a
   step. Same call as v1, and the reference's own "NO RX" screen agrees. */
.dq{position:fixed;inset:0;background:var(--dark);color:#fff;z-index:40;
  display:none;overflow-y:auto}
.dq.on{display:block}
.dq-inner{max-width:var(--col);margin:0 auto;padding:56px var(--pad) 40px}
.dq-mark{width:52px;height:52px;border-radius:50%;background:rgba(230,67,13,.16);
  display:grid;place-items:center;margin-bottom:22px}
.dq-mark svg{width:26px;height:26px;stroke:var(--accent-tint)}
.dq h1{margin:0;font-size:28px;line-height:1.2;font-weight:700}
.dq-sub{margin:12px 0 0;font-size:15px;line-height:1.55;color:#AEB5C4}
.dq-reason{margin:22px 0 0;background:rgba(255,255,255,.06);border-radius:var(--radius-card);
  padding:16px;font-size:14.5px;line-height:1.55;color:#E4E7EE}
.dq-note{margin:22px 0 0;font-size:13px;color:#8C94A6;line-height:1.55}
.dq-back{margin-top:26px;width:100%;min-height:56px;border-radius:var(--radius);
  border:none;background:var(--accent);color:#fff;font-weight:800;font-size:15.5px;
  cursor:pointer;font-family:inherit}
.dq-back:hover{background:var(--accent-hover)}
.dq-ghost{margin-top:12px;width:100%;min-height:52px;border-radius:var(--radius);
  background:none;border:1px solid rgba(255,255,255,.22);color:#fff;
  font-weight:700;font-size:14.5px;cursor:pointer;font-family:inherit}

/* ------------------------------------------------------------- narrow */
@media (max-width:420px){ .hero-h1{font-size:38px} .strip{font-size:12.5px} }
@media (max-width:379px){
  :root{--pad:18px;--gap-block:26px}
  .qhead{font-size:23px}
  .hero-h1{font-size:34px}
  .hero{margin-bottom:36px}
  /* Below this the claim will not hold one line at any readable size. Wrapping
     is the right failure — an ellipsis would quietly eat "In minutes". */
  .strip{white-space:normal}
}

/* ------------------------------------------------- all-screens document */
/* Only the static export uses these: each screen becomes its own frame so the
   file imports into Figma one frame per screen. */
body.frames{background:#DDE1E7;padding:40px 0}
body.frames .frame{background:var(--page);width:var(--col);margin:0 auto 40px;
  box-shadow:0 10px 40px rgba(16,20,34,.16)}
body.frames .frame .step{display:block}
body.frames .frame-label{max-width:var(--col);margin:0 auto 8px;font-size:12px;
  font-weight:700;color:#5A6377;letter-spacing:.04em}
body.frames .dq{position:static;display:block}
"""
