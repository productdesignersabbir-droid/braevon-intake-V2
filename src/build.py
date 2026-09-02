# -*- coding: utf-8 -*-
"""Build the Braevon intake, v2.

    cd v2/src && python3 build.py

Writes `v2/index.html` (the click-through prototype) and `v2/all-screens.html`
(every screen as its own frame, for importing into Figma).

The questions come from `questions.json`, lifted verbatim out of the v1 build by
`extract_v1.py` — v2 is a redesign, not a re-scope, so the clinical content, the
conditional follow-ups and the disqualification rules are v1's. The layout is
the MEDVi QUAD reference's; see `theme.py` and the design notes.
"""
import json
import os
import re

from logo import LOGO
from theme import CSS

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
Q = json.load(open(os.path.join(HERE, 'questions.json'), encoding='utf-8'))

ICON = {
    'arrow': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    'back': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>',
    'lock': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="10" rx="2"/>'
            '<path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
    'warn': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round"><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 '
            '1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/></svg>',
    'shield': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
              'stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
}


def _ic(paths):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round">%s</svg>' % paths)


# One icon per goal on the opening screen, keyed by the v1 option value.
#
# The bubble and glyph colours are the reference's own, read out of its design
# tokens rather than sampled off a screenshot — "Light Green 1"/"Green",
# "light blue"/"blue 2", "Light red", "light purple"/"purple",
# "Light Orange"/"Orange". This is a deliberate exception to house rule 2
# (orange carries emphasis, not decoration): the client asked for these five
# hues specifically on 2026-09-02. Nothing else in the flow takes them.
#
# value -> (bubble fill, glyph colour)
GOAL_COLORS = {
    'last-longer':      ('#DFF7E6', '#22C55E'),   # Light Green 1 / Green
    'better-erections': ('#DBEAFE', '#31ABE8'),   # light blue / blue 2
    # the reference draws this glyph with a gradient rather than a flat token,
    # so the magenta is sampled from its render; the bubble is its own token
    'more-arousal':     ('#FEE2E2', '#EC4899'),   # Light red / magenta
    'rebound':          ('#F3EBFF', '#A855F7'),   # light purple / purple
    'confidence':       ('#FFEDD5', '#F97316'),   # Light Orange / Orange
}

GOAL_ICONS = {
    'last-longer':      _ic('<circle cx="12" cy="13" r="8"/><path d="M12 9v4l2.5 2.5M9 2h6"/>'),
    'better-erections': _ic('<path d="M4 17l5-5 4 4 7-7"/><path d="M14 9h6v6"/>'),
    'more-arousal':     _ic('<path d="M12 21s-7-4.5-7-9.5A4.5 4.5 0 0 1 12 8a4.5 4.5 0 0 1 7 3.5c0 5-7 9.5-7 9.5z"/>'),
    'rebound':          _ic('<path d="M20 12a8 8 0 1 1-2.3-5.6"/><path d="M20 3v5h-5"/>'),
    'confidence':       _ic('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>'),
}


def esc(s):
    return (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def attr(s):
    return esc(s).replace('"', '&quot;')


# --------------------------------------------------------------- primitives
def cta(label='Next', blocked=True):
    """`blocked` means "this step is not answered yet". It is a data attribute
    and not the native `disabled`, because the client asked that the button stay
    orange rather than grey out — so it has to receive the click in order to
    point at what is missing. See `advance()` in the script."""
    return ('<button class="cta cta-next"%s>%s%s</button>'
            % (' data-blocked="1"' if blocked else '', esc(label), ICON['arrow']))


def head(eyebrow=None, title=None, sub=None, big=False):
    out = ''
    if eyebrow:
        out += '<p class="eyebrow">%s</p>' % esc(eyebrow)
    if title:
        out += '<h1 class="qhead%s">%s</h1>' % (' big' if big else '', title)
    if sub:
        out += '<p class="sub">%s</p>' % sub
    return out


def option(o, checkbox):
    lbl = esc(o['label'])
    if o.get('note'):
        lbl += ' <span class="inline-note">%s</span>' % esc(o['note'])
    if o.get('sub'):
        lbl += '<small>%s</small>' % esc(o['sub'])
    extra = ''
    if o.get('exclusive'):
        extra += ' data-exclusive="1"'
    if o.get('sys'):
        extra += ' data-sys="%s" data-dia="%s"' % (o['sys'], o['dia'])
    return ('<button class="opt%s%s" data-value="%s"%s>'
            '<span class="lbl">%s</span><span class="ring"></span></button>'
            % (' checkbox' if checkbox else '',
               ' selected' if o.get('preselected') else '',
               attr(o['value']), extra, lbl))


def options_block(b):
    checkbox = b['mode'] == 'multi'
    if b.get('style') == 'tiles':
        # Two-up cards rather than a stacked list. Same .opt/.opts contract, so
        # selection, validation and the disqualification rules are unchanged —
        # only the grid and the missing ring differ.
        rows = ''.join('<button class="opt tile%s" data-value="%s">'
                       '<span class="lbl">%s</span></button>'
                       % (' selected' if o.get('preselected') else '',
                          attr(o['value']), esc(o['label']))
                       for o in b['options'])
        return ('<div class="opts tilegrid" data-group="%s" data-mode="%s">%s</div>'
                % (attr(b['group']), b['mode'], rows))
    rows = []
    for i, o in enumerate(b['options']):
        rows.append(option(o, checkbox))
        # v1 hoists the exclusive "None of these" to the top of every long list
        # and drops a hint under it — on a fourteen-item safety screen the
        # patient who has none of them should not have to read all fourteen to
        # find that out. The hint rides with it.
        if o.get('exclusive') and b.get('hint'):
            rows.append('<p class="opt-note">%s</p>' % esc(b['hint']))
    return ('<div class="opts" data-group="%s" data-mode="%s"%s>%s</div>'
            % (attr(b['group']), b['mode'],
               ' data-optional="1"' if b.get('optional') else '',
               ''.join(rows)))


def reveal_block(b):
    if b.get('kind') == 'bp-warning':
        return ('<div class="reveal" data-bp-warning><div class="note warn">%s<p>%s</p></div></div>'
                % (ICON['warn'], esc(b.get('text', ''))))
    inner = ''
    if b.get('label'):
        inner += '<label for="%s">%s</label>' % (attr(rid(b)), esc(b['label']))
    if b.get('sub'):
        inner += '<p class="reveal-sub">%s</p>' % esc(b['sub'])
    if b.get('options'):
        inner += options_block({'group': b.get('group') or rid(b), 'mode': 'single',
                                'options': b['options']})
    else:
        inner += ('<textarea id="%s" placeholder="%s" rows="3"></textarea>'
                  % (attr(rid(b)), attr(b.get('placeholder') or '')))
    if b.get('error'):
        inner += '<p class="err" hidden>%s</p>' % esc(b['error'])
    return ('<div class="reveal" data-reveal-for="%s" data-reveal-on="%s"%s>%s</div>'
            % (attr(b.get('for') or ''), attr(b.get('on') or '*'),
               ' data-err="%s"' % attr(b['error']) if b.get('error') else '', inner))


def rid(b):
    base = '%s-%s' % (b.get('for') or 'x', b.get('on') or 'detail')
    return re.sub(r'[^a-zA-Z0-9-]', '-', base)


def field_block(b):
    fid = attr(b['id'])
    lab = '<label for="%s">%s</label>' % (fid, esc(b['label'])) if b.get('label') else ''
    if b['tag'] == 'select':
        opts = ''.join('<option%s>%s</option>' % (' value=""' if i == 0 else '', esc(o))
                       for i, o in enumerate(b.get('options') or []))
        ctrl = '<select id="%s">%s</select>' % (fid, opts)
    elif b['tag'] == 'textarea':
        ctrl = '<textarea id="%s" placeholder="%s" rows="3"></textarea>' % (
            fid, attr(b.get('placeholder') or ''))
    else:
        ctrl = ('<input id="%s" type="%s" placeholder="%s"%s autocomplete="off"/>'
                % (fid, attr(b.get('input_type') or 'text'), attr(b.get('placeholder') or ''),
                   ' inputmode="%s"' % attr(b['inputmode']) if b.get('inputmode') else ''))
    return '<div class="field%s">%s%s</div>' % (' half' if b.get('half') else '', lab, ctrl)


BP_WIDGET = (
    '<p class="bp-lead">Estimated from your selection. Tap a number to enter your own reading.</p>'
    '<div class="bp">'
    '<div class="cellwrap"><input class="cell" data-bp-sys type="text" inputmode="numeric" '
    'maxlength="3" autocomplete="off" aria-label="Systolic, the high number"/>'
    '<div class="cap">Sys (high number)</div></div>'
    '<span class="slash">/</span>'
    '<div class="cellwrap"><input class="cell" data-bp-dia type="text" inputmode="numeric" '
    'maxlength="3" autocomplete="off" aria-label="Diastolic, the low number"/>'
    '<div class="cap">Dia (low number)</div></div>'
    '</div>')


# ------------------------------------------------------------ question steps
def note_block(b):
    if b.get('dark'):
        return ('<div class="darknote">%s<p>%s</p></div>'
                % ('<h4>%s</h4>' % esc(b['lead']) if b.get('lead') else '', b['text']))
    return '<div class="note">%s<p>%s</p></div>' % (ICON['shield'], b['text'])


def field_row(run):
    """Flush a run of consecutive fields, splitting it where the date-of-birth
    selects start and stop.

    The three date selects get their own grid — month needs more room than day,
    and stacking them turns one question into three. Everything else goes in a
    wrapping row where a `half` field takes half of it."""
    out, i = [], 0
    while i < len(run):
        dob = bool(run[i].get('dob'))
        j = i
        while j < len(run) and bool(run[j].get('dob')) == dob:
            j += 1
        cls = 'dob' if dob else 'fields'
        out.append('<div class="%s">%s</div>'
                   % (cls, ''.join(field_block(f) for f in run[i:j])))
        i = j
    return ''.join(out)


def render_question(s):
    """One numbered question, in document order as v1 laid it out."""
    out = ['<div class="col">']
    seen_bp = False
    run = []

    def flush():
        if run:
            out.append(field_row(run))
            del run[:]

    for b in s['blocks']:
        t = b['t']
        if t != 'field':
            flush()
        if t == 'eyebrow':
            out.append('<p class="eyebrow">%s</p>' % esc(b['text']))
        elif t == 'title':
            out.append('<h1 class="qhead">%s</h1>' % esc(b['text']))
        elif t == 'sub':
            out.append('<p class="sub">%s</p>' % esc(b['text']))
        elif t == 'legend':
            out.append('<p class="legend">%s</p>' % esc(b['text']))
        elif t == 'options':
            out.append(options_block(b))
            # the blood-pressure screen's estimate readout sits directly under
            # its option list, before the opt-out group that follows it
            if b.get('grouped') and not seen_bp:
                out.append(BP_WIDGET)
                seen_bp = True
        elif t == 'reveal':
            out.append(reveal_block(b))
        elif t == 'note':
            out.append(note_block(b))
        elif t == 'field':
            run.append(b)
    flush()
    return ''.join(out) + cta() + '</div>' 


# ----------------------------------------------------------- marketing steps
STAR = ('<svg viewBox="0 0 20 20" fill="currentColor">'
        '<path d="M10 1l2.7 6.1 6.6.6-5 4.4 1.5 6.5L10 15.3 4.2 18.6l1.5-6.5-5-4.4 6.6-.6L10 1z"/>'
        '</svg>')
STARS = '<span class="stars">%s</span>' % ('<i>%s</i>' % STAR * 5)

TESTIMONIALS = [
    ('Life-changing, honestly',
     "I didn't think I needed this and tried it mostly out of curiosity. My marriage went up "
     "about ten notches. I had no idea what I'd been missing.", 'B.H.'),
    ('Does exactly what it says',
     "I really like how this makes me feel. It's just like the ad says — bigger, longer, "
     "stronger. Five stars, no notes.", 'Jared T.'),
    ('Best thing I&rsquo;ve tried',
     "Shipped fast and arrived unmarked, which matters when you've got teenagers in the house. "
     "I've tried the big-name pills and this is easily the better one.", 'Mike R.'),
]

MOLECULES = [
    ('APOmorphine', 'Primes for arousal', '2 mg'),
    ('Vardenafil', 'Rapid onset', '7.5 mg'),
    ('Sildenafil', 'Maintains blood flow', '40 mg'),
    ('Tadalafil', 'Extends effectiveness', '4 mg'),
]


def dial(pct=0):
    return ('<div class="dial"><svg width="132" height="132" viewBox="0 0 132 132">'
            '<circle cx="66" cy="66" r="58" fill="none" stroke="#E7EAED" stroke-width="10"/>'
            '<circle class="dial-arc" cx="66" cy="66" r="58" fill="none" stroke="#E6430D" '
            'stroke-width="10" stroke-linecap="round" stroke-dasharray="364.4" '
            'stroke-dashoffset="364.4" transform="rotate(-90 66 66)"/></svg>'
            '<div class="pct">%d%%</div></div>' % pct)


def loader(title, items):
    rows = ''.join('<div><i></i>%s</div>' % esc(i) for i in items)
    return ('<div class="col"><div class="loader" data-loader>%s<h2>%s</h2></div>'
            '<div class="checklist">%s</div></div>' % (dial(), esc(title), rows))


def marketing(n):
    """The interstitials, rebuilt in the reference's card language.

    v1 ran these as two-column splits with a photograph bleeding off one side.
    The reference has no two-column screen anywhere — every interstitial is a
    card in the same 480px column — so they are rebuilt rather than restyled."""
    if n == 2:
        return ('<div class="col">'
                '<div class="media"><img src="assets/images/stat-hero.jpg" alt="Braevon patient"/></div>'
                '<h1 class="qhead big" style="margin-top:24px">'
                '<span class="statnum">92%</span> of men prefer BRAEVON over other ED treatments*</h1>'
                + cta(blocked=False)
                + '<p class="foot">*Based on a survey of active Braevon patients.</p></div>')

    if n == 3:
        cards = ''.join('<article class="tcard">%s<h3>%s</h3><p>%s</p>'
                        '<div class="who">&mdash; %s</div></article>' % (STARS, t, esc(b), w)
                        for t, b, w in TESTIMONIALS)
        return ('<div class="col">'
                '<h1 class="qhead">Trusted by over 250k+ men</h1>'
                '<div class="rail">%s</div><p class="railnote">Scroll for more &rarr;</p>'
                % cards + cta(blocked=False) + '</div>')

    if n == 5:
        return ('<div class="col">'
                + head('Eligibility', 'Good news. BRAEVON is available in '
                                      '<span class="hi" data-state-echo>your state</span>.')
                + '<div class="tiles" style="grid-template-columns:1fr">'
                  '<div class="tile"><b>Licensed clinicians</b>'
                  '<span>Our clinicians are licensed and able to ship to '
                  '<span data-state-echo>your state</span>.</span></div>'
                  '<div class="tile"><b>Ships in 48 hours</b>'
                  '<span>Medication ships to <span data-state-echo>your state</span> '
                  'addresses within 48 hours.</span></div></div>'
                + cta(blocked=False) + '</div>')

    if n == 6:
        return ('<div class="col">'
                + head(None, "Looking great! Let's get some info about your health.",
                       'Our board-certified physicians use the information in the following '
                       'questions to tailor your treatment.')
                + '<div class="media" style="margin-top:24px">'
                  '<img src="assets/images/doctor.jpg" alt="A Braevon clinician"/></div>'
                + '<div class="note" style="margin-top:24px">%s<p>All medications are prescribed '
                  'by certified physicians. Your answers are private and <b>HIPAA protected</b>.</p></div>'
                  % ICON['shield']
                + cta(blocked=False) + '</div>')

    if n == 29:
        rows = [
            ('What this medication does',
             'PDE5 inhibitors (the medication class in BRAEVON) increase blood flow to help you '
             'get and keep an erection.'),
            ('Potential benefits',
             'May improve your ability to achieve and maintain an erection, enhance sexual '
             'performance and satisfaction, and improve your quality of life and personal '
             'relationships.'),
            ('Do not use if you',
             'Take nitrates for chest pain &middot; use &ldquo;poppers&rdquo; &middot; have severe '
             'heart or liver problems &middot; recently had a stroke or heart attack &middot; '
             'have low blood pressure.'),
        ]
        cards = ''.join('<div class="tile" style="grid-column:1/-1"><b>%s</b><span>%s</span></div>'
                        % (t, b) for t, b in rows)
        return ('<div class="col">'
                + head('Consent', 'One last step &mdash; your consent',
                       'Quick summary below. The full document is one tap away.')
                + '<div class="tiles">%s</div>' % cards
                + '<div class="opts" data-group="consent" data-mode="multi" style="margin-top:16px">'
                + option({'value': 'agree',
                          'label': 'I have read and agree to the consent document and the '
                                   'telehealth informed consent.'}, True)
                + '</div>' + cta() + '</div>')

    if n == 30:
        return loader('Processing your information&hellip;',
                      ['Medical history', 'Health info', 'ED frequency'])

    if n == 31:
        # The product render already names and explains all four molecules, so
        # the card under it says what the picture cannot — speed and delivery —
        # rather than repeating the list.
        return ('<div class="col">'
                + head(None, 'Meet the highest rated ED treatment, loved by over 175K+ men')
                + '<div class="media" style="margin-top:24px">'
                  '<img src="assets/images/ingredients.png" alt="BRAEVON 4-in-1: apomorphine, '
                  'vardenafil, sildenafil and tadalafil"/></div>'
                + '<div class="tiles">'
                  '<div class="tile"><b>15 minutes</b><span>Effects in 15 minutes or less*</span></div>'
                  '<div class="tile"><b>1&ndash;2 days</b><span>Delivered discreetly to your door</span></div>'
                  '</div>'
                + '<p class="foot">*On average, after the medication dissolves. Based on a survey '
                  'of active Braevon patients.</p>'
                + cta(blocked=False) + '</div>')

    if n == 32:
        return ('<div class="col">'
                + head(None, 'Get hard in just <span class="hi">15 minutes</span>.')
                + '<div class="factcard" style="margin-top:24px">'
                  '<div class="k">89%</div><div class="u">of men prefer</div>'
                  '<p>APOmorphine + sildenafil over sildenafil alone*</p></div>'
                + '<div class="media" style="margin-top:16px">'
                  '<img src="assets/images/hero-benefits.jpg" alt="Braevon"/></div>'
                + '<p class="foot">*On average, after the medication dissolves. Based on a '
                  'customer survey of active Braevon patients.</p>'
                + cta(blocked=False) + '</div>')

    if n == 33:
        return loader('Reviewing your assessment&hellip;',
                      ['Answers received', 'Clinician review', 'Preparing your plan'])

    if n == 34:
        mols = ''.join('<div class="mol"><div><b>%s</b><span>%s</span></div>'
                       '<div class="dose">%s</div></div>' % (a, b, d) for a, b, d in MOLECULES)
        return ('<div class="col">'
                '<span class="result-badge">Assessment complete</span>'
                '<h1 class="qhead" style="margin-top:16px">'
                'Good news<span data-name-echo></span>. You&rsquo;re a strong candidate for a '
                'prescription ED treatment.</h1>'
                '<p class="sub">A licensed clinician will review your answers and confirm your '
                'plan. Nothing ships until they do.</p>'
                '<div class="reviewcard"><h3>Your medical review</h3>'
                '<div class="rrow"><span>Primary goal</span><b data-echo="goals">&mdash;</b></div>'
                '<div class="rrow"><span>Performance</span><b data-echo="confidence">&mdash;</b></div>'
                '<div class="rrow"><span>Blood pressure</span><b data-echo="bp">&mdash;</b></div>'
                '<div class="rrow"><span>Reviewed by</span><b>Braevon clinical team</b></div>'
                '</div>'
                '<div class="reviewcard"><h3>Recommended &mdash; Precision Strength</h3>%s</div>'
                '<div class="note" style="margin-top:16px">%s<p>Trusted by over <b>175,000</b> '
                'customers. Performance guaranteed.</p></div>' % (mols, ICON['shield'])
                + cta('Continue to your plan', blocked=False) + '</div>')

    return '<div class="col">%s%s</div>' % (head(None, 'Screen %d' % n), cta(blocked=False))


def hero_screen(s):
    """Screen 1, rebuilt to the reference's opening layout.

    Video hero with the product render breaking out of its bottom-right corner,
    a two-line headline whose second line carries the accent, the tinted claim
    strip, then the goal list with an icon per row.

    The five goals are **v1's wording**, not the reference's — the standing
    instruction is that the questions stay ours. They map one to one onto the
    reference's five (last longer / stamina, better erections / erection
    strength, more arousal / sex drive, faster rebound / quicker recovery,
    more confidence / confidence), so the layout takes them unchanged."""
    goals = next(b for b in s['blocks'] if b['t'] == 'options')

    # v1 asked this as "select all that apply". The reference asks for one
    # primary goal and pre-picks the second, and the client asked for both —
    # so it is single-select here, and the copy above it already reads
    # "Select your primary goal:". This is the one place v2 changes a v1
    # question's shape rather than its dress; flagged in the README.
    goals = dict(goals, mode='single')
    for i, o in enumerate(goals['options']):
        o['preselected'] = (i == 1)

    rows = ''.join(
        '<button class="opt goal%s" data-value="%s">'
        '<span class="bubble" style="--bub:%s;--gly:%s">%s</span>'
        '<span class="lbl">%s</span></button>'
        % ((' selected' if o.get('preselected') else '', attr(o['value']))
           + GOAL_COLORS.get(o['value'], ('#FDECE6', '#E6430D'))
           + (GOAL_ICONS.get(o['value'], ICON['shield']), esc(o['label'])))
        for o in goals['options'])

    return (
        '<div class="col">'
        # The <video> is the layout; the file is the client's to supply. Until
        # it lands, the poster carries the frame at the right size, so the
        # screen is never broken — it just does not move. Drop the clip at
        # assets/video/hero.mp4 and it plays with no other change.
        '<div class="hero">'
        # The poster is braevon.com's own hero photograph, so the frame shows
        # the site's image today; drop a clip in at assets/video/hero.mp4 and
        # the same element plays it instead. Neither ask cancels the other.
        '<video class="hero-media" autoplay muted loop playsinline preload="metadata" '
        'poster="assets/images/braevon-hero.jpg">'
        '<source src="assets/video/hero.mp4" type="video/mp4"/></video>'
        '<img class="hero-product" src="assets/images/product-tablet.png" '
        'alt="The BRAEVON 4-in-1 tablet"/>'
        '</div>'
        '<h1 class="hero-h1">You Deserve a<br/><span class="hi">Better Sex Life.</span></h1>'
        '<p class="strip">BRAEVON 4-in-1. Arousal &amp; performance. <strong>In minutes</strong></p>'
        '<p class="ask">See if <strong>BRAEVON</strong> is right for you.</p>'
        '<p class="ask-sub">Select your primary goal:</p>'
        '<div class="opts" data-group="%s" data-mode="%s">%s</div>'
        % (attr(goals['group']), goals['mode'], rows)
        + cta() + '</div>')


# ------------------------------------------------------------------ assemble
def sections():
    out = []
    for s in Q:
        n = s['step']
        a = ' data-step="%d"' % n
        if s['q']:
            a += ' data-q="%d"' % s['q']
        if s['dq']:
            a += ' data-dq="%s"' % attr(s['dq'])
        if s['dq_on']:
            a += ' data-dq-on="%s"' % attr(s['dq_on'])
        if s['cond']:
            a += ' data-if="%s"' % attr(s['cond'])
        if s['no_back']:
            a += ' data-no-back'
        html = (hero_screen(s) if n == 1
                else render_question(s) if s['q'] else marketing(n))
        # The opening screen carries the tallest stack in the flow — hero,
        # two-line h1, claim strip, question and sub — so it gets its own
        # class and a tighter rhythm; see `.step.s1` in theme.py.
        cls = 'step s1' if n == 1 else 'step'
        out.append('<section class="%s"%s>%s</section>' % (cls, a, html))
    return out


TOTAL_Q = max(s['q'] for s in Q if s['q'])
SEGMENTS = 5

# The wordmark sits on the left and the rating on the right, as v1 had it —
# so the back control cannot live in the masthead any more. It moves down to
# sit beside the progress bar, which is where v1 kept it too.
MASTHEAD = (
    '<header class="masthead">'
    '<div class="logo">%s</div>'
    '<div class="rating"><span class="txt">Excellent 4.6</span>%s</div>'
    '</header><div class="rule"></div>' % (LOGO, STARS))


def nav(progress):
    return ('<div class="navrow">'
            '<button class="back-btn" id="backBtn" aria-label="Go back">%s</button>'
            '%s</div>' % (ICON['back'], progress))


PROGRESS = nav('<div class="progress" id="prog" role="progressbar" '
               'aria-label="Assessment progress" aria-valuemin="%d" aria-valuemax="%d" '
               'aria-valuenow="1" aria-valuetext="Question 1 of %d">%s</div>'
               % (1, TOTAL_Q, TOTAL_Q,
                  ''.join('<div class="seg"><span></span></div>' for _ in range(SEGMENTS))))

DQ = ('<div class="dq" id="dq" role="dialog" aria-modal="true" aria-labelledby="dqTitle">'
      '<div class="dq-inner">'
      '<div class="dq-mark">%s</div>'
      '<h1 id="dqTitle">We can&rsquo;t continue your assessment</h1>'
      '<p class="dq-sub">Your safety is our priority. This treatment has specific medical '
      'criteria, and your answer means our clinicians cannot safely determine your eligibility.</p>'
      '<div class="dq-reason" id="dqReason"></div>'
      '<p class="dq-note">If you entered something by mistake, go back and change it. If your '
      'answer was correct, please speak with your own doctor about other options.</p>'
      '<button class="dq-back" id="dqBack">Review my answer</button>'
      '<button class="dq-ghost" id="dqExit">Exit the assessment</button>'
      '</div></div>' % ICON['warn'])

SCRIPT = r"""
(function(){
  var stage=document.getElementById('stage');
  var steps=[].slice.call(stage.querySelectorAll('.step'));
  var prog=document.getElementById('prog');
  var segs=[].slice.call(prog.querySelectorAll('.seg span'));
  var backBtn=document.getElementById('backBtn');
  var dq=document.getElementById('dq'), dqReason=document.getElementById('dqReason');
  var TOTAL_Q=__TOTAL_Q__, SEGMENTS=__SEGMENTS__;
  var answers={};      /* group -> array of selected values */
  var idx=0, history=[];

  /* ---------------------------------------------------------- selection */
  function sel(group){ return answers[group]||[]; }

  stage.addEventListener('click', function(e){
    var opt=e.target.closest('.opt'); if(!opt) return;
    var box=opt.closest('.opts'); if(!box) return;
    var group=box.dataset.group, multi=box.dataset.mode==='multi';
    var val=opt.dataset.value;

    if(!multi){
      [].forEach.call(box.querySelectorAll('.opt'), function(o){ o.classList.remove('selected'); });
      opt.classList.add('selected');
      answers[group]=[val];
      if(opt.dataset.sys) setBP(opt.dataset.sys, opt.dataset.dia, false);
    } else {
      var on=!opt.classList.contains('selected');
      opt.classList.toggle('selected', on);
      /* "None of these" is exclusive both ways: picking it clears the rest,
         and picking anything else clears it. */
      if(on && opt.dataset.exclusive){
        [].forEach.call(box.querySelectorAll('.opt'), function(o){
          if(o!==opt) o.classList.remove('selected'); });
      } else if(on){
        [].forEach.call(box.querySelectorAll('.opt[data-exclusive]'), function(o){
          o.classList.remove('selected'); });
      }
      answers[group]=[].map.call(box.querySelectorAll('.opt.selected'),
                                function(o){ return o.dataset.value; });
    }
    syncReveals(); clearError(opt.closest('.step'));
    maybeAutoAdvance(opt, multi);
  });

  /* Answering advances the screen; Continue stays and still works, so this is
     a shortcut past it rather than a replacement. Four things hold it back:

     - a multi-select waits, unless the answer is the exclusive "None of these"
       — on "select all that apply" the patient may well want two or three, and
       leaving on the first tick collects exactly one;
     - unticking never advances;
     - an open follow-up still has to be typed into;
     - the blood-pressure screen never jumps: picking a band fills both numbers
       and so satisfies the step, but that screen exists precisely so someone
       who knows their real reading can type it.

     Everything else is `stepValid`, which the Continue button already uses — so
     screens 4 and 28 hold on their own, their inputs being unfilled. It routes
     through `advance()`, the same function Continue calls, so a disqualifying
     answer still opens the stop screen rather than being walked past. */
  function maybeAutoAdvance(opt, multi){
    var el=steps[idx];
    if(el.querySelector('.bp')) return;
    if(multi && !opt.dataset.exclusive) return;
    if(!opt.classList.contains('selected')) return;
    if(el.querySelector('.reveal.on')) return;
    if(!stepValid(el)) return;
    setTimeout(function(){ if(steps[idx]===el) advance(); }, 140);
  }

  /* ------------------------------------------------------------ reveals */
  function syncReveals(){
    [].forEach.call(stage.querySelectorAll('.reveal[data-reveal-for]'), function(r){
      var g=r.dataset.revealFor, on=r.dataset.revealOn, picked=sel(g);
      var show = on==='*'
        ? picked.some(function(v){ return v!=='none'; })
        : picked.indexOf(on)>-1;
      r.classList.toggle('on', show);
    });
  }

  /* ------------------------------------------------------ blood pressure */
  var sysEl=stage.querySelector('[data-bp-sys]'), diaEl=stage.querySelector('[data-bp-dia]');
  var bpLead=stage.querySelector('.bp-lead'), bpWarn=stage.querySelector('[data-bp-warning]');
  function setBP(s,d,manual){
    if(!sysEl) return;
    sysEl.value=s; diaEl.value=d;
    if(bpLead) bpLead.textContent = manual
      ? 'Using the reading you entered. Pick an option above to go back to an estimate.'
      : 'Estimated from your selection. Tap a number to enter your own reading.';
    checkBP();
  }
  function checkBP(){
    if(!sysEl||!bpWarn) return;
    var s=+sysEl.value||0, d=+diaEl.value||0;
    bpWarn.classList.toggle('on', s>=160||d>=100||(s>0&&s<90)||(d>0&&d<50));
  }
  [sysEl,diaEl].forEach(function(el){
    if(!el) return;
    el.addEventListener('input', function(){
      el.value=el.value.replace(/\D/g,'');
      var box=stage.querySelector('.opts[data-group="bp"]');
      if(box){ [].forEach.call(box.querySelectorAll('.opt'),function(o){o.classList.remove('selected');});
               answers['bp']=['manual']; }
      if(bpLead) bpLead.textContent='Using the reading you entered. Pick an option above to go back to an estimate.';
      checkBP();
    });
  });

  /* --------------------------------------------------------- validation */
  function stepValid(el){
    var ok=true;
    [].forEach.call(el.querySelectorAll('.opts'), function(box){
      if(box.dataset.optional) return;
      if(box.closest('.reveal') && !box.closest('.reveal').classList.contains('on')) return;
      if(!box.querySelector('.opt.selected')) ok=false;
    });
    [].forEach.call(el.querySelectorAll('.field input, .field select'), function(f){
      if(!f.value.trim()) ok=false;
    });
    [].forEach.call(el.querySelectorAll('.reveal.on textarea'), function(t){
      if(!t.value.trim()) ok=false;
    });
    return ok;
  }
  function showError(el){
    var r=el.querySelector('.reveal.on .err');
    if(r) r.hidden=false;
    var first=el.querySelector('.opts:not([data-optional]) , .field input, .field select');
    if(first) first.scrollIntoView({block:'center', behavior:'smooth'});
    el.animate([{transform:'translateX(0)'},{transform:'translateX(-5px)'},
                {transform:'translateX(5px)'},{transform:'translateX(0)'}],
               {duration:220});
  }
  function clearError(el){ if(!el) return;
    [].forEach.call(el.querySelectorAll('.err'), function(e){ e.hidden=true; }); }

  stage.addEventListener('input', function(e){
    if(e.target.matches('input,select,textarea')) clearError(e.target.closest('.step'));
  });

  /* --------------------------------------------------- disqualification */
  function disqualifies(el){
    var reason=el.dataset.dq; if(!reason) return null;
    var rule=el.dataset.dqOn;
    if(rule){
      var hit=rule.split(',').some(function(pair){
        var p=pair.split(':'); return sel(p[0].trim()).indexOf(p[1].trim())>-1;
      });
      return hit?reason:null;
    }
    /* With no rule, anything but the exclusive "none" is a contraindication. */
    var any=false;
    [].forEach.call(el.querySelectorAll('.opts'), function(box){
      if(box.closest('.reveal')) return;
      [].forEach.call(box.querySelectorAll('.opt.selected'), function(o){
        if(!o.dataset.exclusive) any=true;
      });
    });
    return any?reason:null;
  }

  /* ------------------------------------------------------------- moving */
  function shown(el){
    var cond=el.dataset.if; if(!cond) return true;
    var p=cond.split(':'); return sel(p[0]).indexOf(p[1])>-1;
  }
  function show(i){
    loaderRun++;   /* cancel any dial still running on the screen we are leaving */
    steps.forEach(function(s,j){ s.classList.toggle('on', j===i); });
    idx=i;
    var el=steps[i];
    var q=el.dataset.q?+el.dataset.q:0;
    prog.hidden=!q;
    if(q){
      prog.setAttribute('aria-valuenow', q);
      prog.setAttribute('aria-valuetext','Question '+q+' of '+TOTAL_Q);
      var per=TOTAL_Q/SEGMENTS, at=Math.floor((q-1)/per);
      segs.forEach(function(sp,k){ sp.style.width = k<=at ? '100%' : '0%'; });
    }
    backBtn.hidden = el.hasAttribute('data-no-back') || history.length===0;
    window.scrollTo({top:0, behavior:'auto'});
    if(el.querySelector('[data-loader]')) runLoader(el);
    if(el.querySelector('[data-name-echo]')) fillSummary(el);
    echoState();
  }
  function advance(){
    var el=steps[idx];
    if(!stepValid(el)){ showError(el); return; }
    var why=disqualifies(el);
    if(why){ dqReason.textContent=why; dq.classList.add('on'); return; }
    for(var j=idx+1;j<steps.length;j++){
      if(shown(steps[j])){ history.push(idx); show(j); return; }
    }
  }
  stage.addEventListener('click', function(e){
    if(e.target.closest('.cta-next')) advance();
  });
  backBtn.addEventListener('click', function(){
    if(!history.length) return;
    show(history.pop());
  });
  document.getElementById('dqBack').addEventListener('click', function(){
    dq.classList.remove('on');
  });
  document.getElementById('dqExit').addEventListener('click', function(){
    dq.classList.remove('on'); history=[]; show(0);
  });

  /* --------------------------------------------------------------- echo */
  function echoState(){
    var s=document.getElementById('state');
    var v=s&&s.value?s.value:'your state';
    [].forEach.call(document.querySelectorAll('[data-state-echo]'), function(e){
      e.textContent=v;
    });
  }
  function label(group){
    var box=stage.querySelector('.opts[data-group="'+group+'"]');
    if(!box) return null;
    var picked=[].map.call(box.querySelectorAll('.opt.selected'), function(o){
      var l=o.querySelector('.lbl').cloneNode(true);
      var sm=l.querySelector('small'); if(sm) sm.remove();
      return l.textContent.trim();
    });
    return picked.length?picked.join(', '):null;
  }
  function fillSummary(el){
    var fn=document.getElementById('firstName');
    var n=el.querySelector('[data-name-echo]');
    /* ", Marcus" or nothing — the sentence has to read either way, so the name
       is an aside rather than the subject. */
    if(n) n.textContent = (fn&&fn.value.trim()) ? ', '+fn.value.trim() : '';
    [].forEach.call(el.querySelectorAll('[data-echo]'), function(e){
      var k=e.dataset.echo;
      if(k==='bp'){
        e.textContent = (sysEl&&sysEl.value) ? sysEl.value+' / '+diaEl.value : '—';
      } else {
        e.textContent = label(k) || '—';
      }
    });
  }

  /* ------------------------------------------------------- the loaders */
  var C=2*Math.PI*58;
  var loaderRun=0;
  function runLoader(el){
    /* The processing screens carry no button: they run their dial and hand off
       on their own, the way the reference does. `loaderRun` is the guard — if
       the patient goes back mid-run, the old frame loop must not advance the
       flow out from under the screen they are now on. */
    var arc=el.querySelector('.dial-arc'), pct=el.querySelector('.pct');
    var rows=[].slice.call(el.querySelectorAll('.checklist div'));
    if(!arc) return;
    var mine=++loaderRun, from=idx, DUR=2600;
    rows.forEach(function(r){ r.classList.remove('done'); });
    arc.setAttribute('stroke-dasharray', C);

    /* The hand-off is on a timer, not on the animation frame. A background tab
       stops serving requestAnimationFrame, and this screen has no button — so
       driving the advance from the frame loop leaves anyone who switches tabs
       mid-processing stranded on a dial that never finishes. The frames are
       decoration; the timer is the flow. */
    setTimeout(function(){
      if(mine!==loaderRun || idx!==from) return;
      arc.setAttribute('stroke-dashoffset', 0);
      pct.textContent='100%';
      rows.forEach(function(r){ r.classList.add('done'); });
      setTimeout(function(){ if(mine===loaderRun && idx===from) advance(); }, 340);
    }, DUR);

    var t0=null;
    function frame(t){
      if(mine!==loaderRun) return;
      if(!t0) t0=t;
      var p=Math.min(1,(t-t0)/DUR);
      arc.setAttribute('stroke-dashoffset', C*(1-p));
      pct.textContent=Math.round(p*100)+'%';
      rows.forEach(function(r,i){ r.classList.toggle('done', p > (i+1)/(rows.length+0.6)); });
      if(p<1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  /* Two controls ship with an answer already chosen — sex on the eligibility
     screen, and "Normal" on the blood-pressure screen. Nothing clicks them, so
     without this pass the answer map starts out disagreeing with the markup and
     the summary reads them as blank. */
  [].forEach.call(stage.querySelectorAll('.opts'), function(box){
    var picked=[].map.call(box.querySelectorAll('.opt.selected'),
                           function(o){ return o.dataset.value; });
    if(picked.length) answers[box.dataset.group]=picked;
  });
  var bpPre=stage.querySelector('.opts[data-group="bp"] .opt.selected');
  if(bpPre && bpPre.dataset.sys) setBP(bpPre.dataset.sys, bpPre.dataset.dia, false);

  syncReveals();
  show(0);
})();
"""


def page(title, body, body_class=''):
    cls = ' class="%s"' % body_class if body_class else ''
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8"/>\n'
            '<title>%s</title>\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1"/>\n'
            # unreleased prototype carrying placeholder testimonials and
            # marketing claims — it should not be indexed if it is hosted
            '<meta name="robots" content="noindex, nofollow"/>\n'
            '<style>%s</style>\n</head>\n<body%s>\n%s\n</body>\n</html>\n'
            % (title, CSS, cls, body))


def emit_interactive():
    body = ('<div class="shell">' + MASTHEAD + PROGRESS
            + '<main class="stage" id="stage">%s</main>' % '\n'.join(sections())
            + '</div>' + DQ
            + '<script>%s</script>' % SCRIPT.replace('__TOTAL_Q__', str(TOTAL_Q))
                                            .replace('__SEGMENTS__', str(SEGMENTS)))
    html = page('Braevon &mdash; Intake Assessment v2', body)
    for name in ('index.html', 'interactive.html'):
        open(os.path.join(OUT, name), 'w', encoding='utf-8').write(html)
    return html


def static_progress(q):
    """The interactive build fills the segments from script. A frame has no
    script, so its bar is drawn at the width that question would have reached —
    otherwise all 24 frames import into Figma showing an empty bar."""
    per = TOTAL_Q / float(SEGMENTS)
    at = int((q - 1) // per)
    segs = ['<div class="seg"><span style="width:%d%%"></span></div>' % (100 if k <= at else 0)
            for k in range(SEGMENTS)]
    return nav('<div class="progress" role="progressbar" aria-label="Assessment progress" '
               'aria-valuemin="1" aria-valuemax="%d" aria-valuenow="%d" '
               'aria-valuetext="Question %d of %d">%s</div>'
               % (TOTAL_Q, q, q, TOTAL_Q, ''.join(segs)))


def emit_frames():
    """Every screen as its own frame, top to bottom, for the Figma import."""
    frames = []
    for s, html in zip(Q, sections()):
        n, q = s['step'], s['q']
        lbl = 'Screen %02d %s' % (n, ('— Question %d' % q) if q else '— interstitial')
        inner = html.replace('<section class="step', '<section class="step on', 1)
        # ids are unique per document; 35 frames in one file cannot each carry
        # the interactive build's element ids
        chrome = (MASTHEAD + (static_progress(q) if q else nav(''))).replace(' id="backBtn"', '')
        if s['no_back']:
            chrome = chrome.replace('<button class="back-btn"',
                                    '<button class="back-btn" hidden')
        frames.append('<div class="frame-label">%s</div><div class="frame"><div class="shell">'
                      '%s<main class="stage">%s</main></div></div>' % (lbl, chrome, inner))
    frames.append('<div class="frame-label">Screen %02d — disqualification</div>'
                  '<div class="frame">%s</div>'
                  % (len(Q) + 1, DQ.replace('class="dq"', 'class="dq on"')))
    html = page('Braevon &mdash; Intake v2, all screens', '\n'.join(frames), 'frames')
    open(os.path.join(OUT, 'all-screens.html'), 'w', encoding='utf-8').write(html)
    return len(frames)


if __name__ == '__main__':
    emit_interactive()
    n = emit_frames()
    print('index.html + interactive.html written (%d screens, %d questions)'
          % (len(Q), TOTAL_Q))
    print('all-screens.html written (%d frames)' % n)
