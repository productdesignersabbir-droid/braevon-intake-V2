# -*- coding: utf-8 -*-
"""Build the Braevon intake, v2.

    cd v2/src && python3 build.py

Writes `v2/index.html` (the click-through prototype) and `v2/all-screens.html`
(every screen as its own frame, for importing into Figma).

**The flow is the MEDVi QUAD reference's, screen for screen.** Questions,
options, the notes under them, the branching and the safety rules are parsed
out of the reference by `extract_medvi.py` into `medvi-flow.json` rather than
retyped, so they cannot drift and a change over there shows up as a diff. The
client asked for the reference's questions wholesale on 2026-09-02 and will say
screen by screen which become Braevon's own.

Two things are deliberately not carried across:

- **Brand names.** QUAD becomes BRAEVON, and the product is Braevon's 4-in-1.
- **The two customer quotes.** Those are MEDVi's named customers; presenting
  another company's reviews as Braevon's would be fabricating testimonials. The
  cards keep the reference's shape with copy written for this concept - the
  same call v1 made about DirectMeds' reviews. See `QUOTES`.

v1's question set is no longer rendered. `extract_v1.py` and `questions.json`
stay in the repo so it can be pulled back a screen at a time.
"""
import json
import os
import re

from logo import LOGO
from theme import CSS

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
FLOW = json.load(open(os.path.join(HERE, 'medvi-flow.json'), encoding='utf-8'))

BRAND = 'BRAEVON'
STOP_SCREEN = 46          # the reference's "NO RX" page; here it is the overlay
INTERSTITIALS = {2, 5, 8, 32, 33, 44}
# Screens the reference lays out as two cards side by side rather than a
# stacked list — measured off the live page, where the option wrapper is
# flex-direction:row and each card is 208x190 instead of 432x51.
TILE_SCREENS = {3, 7, 24, 39, 40, 41, 42}

SEGMENTS = 5


def _ic(paths):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round">%s</svg>' % paths)


ICON = {
    'arrow': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    'back': _ic('<path d="M19 12H5M11 18l-6-6 6-6"/>'),
    'warn': _ic('<path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/>'
                '<path d="M12 9v4M12 17h.01"/>'),
    'shield': _ic('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'),
}

# Screen 1's goal icons, keyed by the reference's own option labels. The bubble
# and glyph colours are its design tokens - "Light Green 1"/"Green", "light
# blue"/"blue 2", "Light red", "light purple"/"purple", "Light Orange"/"Orange".
# A deliberate exception to the rule that orange carries emphasis: the client
# asked for these five hues and nothing else in the flow takes them.
GOAL_STYLE = {
    'Improve stamina & endurance': ('#DFF7E6', '#22C55E',
                                    _ic('<circle cx="12" cy="13" r="8"/><path d="M12 9v4l2.5 2.5M9 2h6"/>')),
    'Increase erection strength':  ('#DBEAFE', '#31ABE8',
                                    _ic('<path d="M4 17l5-5 4 4 7-7"/><path d="M14 9h6v6"/>')),
    'Boost sex drive & desire':    ('#FEE2E2', '#EC4899',
                                    _ic('<path d="M12 21s-7-4.5-7-9.5A4.5 4.5 0 0 1 12 8a4.5 4.5 0 0 1 7 3.5c0 5-7 9.5-7 9.5z"/>')),
    'Quicker recovery':            ('#F3EBFF', '#A855F7',
                                    _ic('<path d="M20 12a8 8 0 1 1-2.3-5.6"/><path d="M20 3v5h-5"/>')),
    'Boost confidence':            ('#FFEDD5', '#F97316',
                                    _ic('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>')),
}

# The sex screen's two cards carry a 64px icon bubble in the reference, in the
# same two hues its goal icons use. The other tile screens carry a small mark
# that reads as decoration, and are left plain.
TILE_ICONS = {
    (3, 'male'):   ('#DBEAFE', '#3B82F6',
                    _ic('<circle cx="10" cy="14" r="6"/><path d="M15 9l6-6M15 3h6v6"/>')),
    (3, 'female'): ('#FCE7F3', '#EC4899',
                    _ic('<circle cx="12" cy="9" r="6"/><path d="M12 15v7M9 19h6"/>')),
}

MOLECULES = [
    ('Apomorphine', 'Primes the brain&rsquo;s arousal pathways', '2 mg'),
    ('L-Citrulline', 'Amplifies blood flow for speed', '&mdash;'),
    ('Sildenafil', 'Supports a strong blood-flow response', '40 mg'),
    ('Tadalafil', 'Extends the window', '4 mg'),
]

# Screen 5 reads as a benefit list, not an ingredient table: the reference leads
# each row with what the molecule does for you and names the molecule second.
# Bubble hues follow the goal-icon tokens - purple, green, red, blue.
MECHANISM = [
    ('Spark Desire', 'Apomorphine primes the brain&rsquo;s arousal pathways.',
     '#F3EBFF', '#A855F7',
     _ic('<path d="M12 6a3.2 3.2 0 0 0-6-1.1A2.7 2.7 0 0 0 4.2 9.4 2.8 2.8 0 0 0 6 14.4'
         'a3 3 0 0 0 3 2.6"/><path d="M12 6a3.2 3.2 0 0 1 6-1.1 2.7 2.7 0 0 1 1.8 4.5'
         'A2.8 2.8 0 0 1 18 14.4a3 3 0 0 1-3 2.6"/><path d="M12 6v15"/>')),
    ('Start Fast', 'L-Citrulline amplifies blood flow for speed.',
     '#DFF7E6', '#22C55E',
     _ic('<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>')),
    ('Boost Performance', 'Sildenafil supports a strong blood-flow response.',
     '#FEE2E2', '#EF4444',
     _ic('<path d="M12 21s-7-4.5-7-9.5A4.5 4.5 0 0 1 12 8a4.5 4.5 0 0 1 7 3.5c0 5-7 9.5-7 9.5z"/>')),
    ('Last Longer', 'Tadalafil extends the effect window (up to 36h reported).',
     '#DBEAFE', '#3B82F6',
     _ic('<rect x="2.5" y="7.5" width="15" height="9" rx="2.6"/>'
         '<path d="M20.5 10.5v3"/><path d="M6 10.5v3"/>')),
]

# Placeholder copy written for this concept, not real reviews - see the module
# docstring. Structure and slot are the reference's.
QUOTES = {
    32: ('&ldquo;It probably saved my marriage.&rdquo;',
         [('Personal goal', 'Boost sex drive and desire'),
          ('Benefits', 'Mood, and effects that last')],
         'David B. &mdash; Kansas City, MO'),
    44: ('&ldquo;The results were almost immediate &mdash; more energy, more desire, '
         'and a stronger performance every time.&rdquo;',
         [('Personal goal', 'Improve stamina and endurance'),
          ('Benefits', 'Quick effect, lasting performance')],
         'Bryan G. &mdash; New York, NY'),
}

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']


def esc(s):
    return (s or '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def attr(s):
    return esc(s).replace('"', '&quot;')


def brandify(s):
    """The reference's product name out, Braevon's in."""
    if not s:
        return s
    s = re.sub(r'MEDVi QUAD\xae|MEDVi QUAD|QUAD\xae|MEDVi', BRAND, s)
    return s.replace("QUAD's", BRAND + "&rsquo;s").replace('QUAD', BRAND)


# --------------------------------------------------------------- primitives
def cta(label='Next', blocked=True):
    """`blocked` means "this screen is not answered yet". A data attribute
    rather than the native `disabled`, because the client asked that the button
    stay orange - so it has to receive the click in order to say what is
    missing."""
    return ('<button class="cta cta-next"%s>%s%s</button>'
            % (' data-blocked="1"' if blocked else '', esc(label), ICON['arrow']))


def head(title=None, sub=None, eyebrow=None):
    out = ''
    if eyebrow:
        out += '<p class="eyebrow">%s</p>' % eyebrow
    if title:
        out += '<h1 class="qhead">%s</h1>' % title
    if sub:
        out += '<p class="sub">%s</p>' % sub
    return out


def option(o, exclusive, goal=False, tile=False, screen=None):
    label = esc(brandify(o['label']))
    if tile:
        note = ('<small>%s</small>' % esc(brandify(o['note']))) if o.get('note') else ''
        art = TILE_ICONS.get((screen, (o['value'] or '').lower()))
        bub = ('<span class="bubble big" style="--bub:%s;--gly:%s">%s</span>' % art
               ) if art else ''
        return ('<button class="opt tile" data-value="%s">%s'
                '<span class="lbl">%s%s</span></button>'
                % (attr(o['value']), bub, label, note))
    if goal:
        bub, gly, glyph = GOAL_STYLE.get(o['label'], ('#FDECE6', '#E6430D', ICON['shield']))
        return ('<button class="opt goal" data-value="%s"><span class="bubble" '
                'style="--bub:%s;--gly:%s">%s</span><span class="lbl">%s</span></button>'
                % (attr(o['value']), bub, gly, glyph, label))
    inner = label
    if o.get('note'):
        inner += '<small>%s</small>' % esc(brandify(o['note']))
    return ('<button class="opt%s" data-value="%s"%s>'
            '<span class="lbl">%s</span><span class="ring"></span></button>'
            % (' checkbox' if o['type'] == 'checkbox' else '', attr(o['value']),
               ' data-exclusive="1"' if o['value'] == exclusive else '', inner))


def options_block(p):
    """The exclusive "None of these" is hoisted to the top of every list.

    On a fifteen-item safety screen it otherwise sits below the fold, so a
    patient who has none of them has to read all fifteen to find that out - and
    every option scrolled past is one they might tick by mistake. The reference
    puts it first for the same reason."""
    goal = p['n'] == 1
    tile = p['n'] in TILE_SCREENS
    opts = (p['options'] if tile
            else sorted(p['options'], key=lambda o: o['value'] != p['exclusive']))
    return ('<div class="opts%s" data-group="%s" data-mode="%s">%s</div>'
            % (' tilegrid' if tile else '', attr(p['group']), p['mode'],
               ''.join(option(o, p['exclusive'], goal, tile, p['n']) for o in opts)))


def field_block(f, label=None):
    fid = attr(f['name'])
    lab = '<label for="%s">%s</label>' % (fid, esc(label)) if label else ''
    if f['tag'] == 'select':
        rows = ''.join('<option%s>%s</option>' % (' value=""' if i == 0 else '', esc(o))
                       for i, o in enumerate(f.get('options') or []))
        ctrl = '<select id="%s">%s</select>' % (fid, rows)
    elif f['tag'] == 'textarea':
        ctrl = ('<textarea id="%s" rows="3" placeholder="%s"></textarea>'
                % (fid, attr(f.get('placeholder') or '')))
    else:
        ctrl = ('<input id="%s" type="%s" placeholder="%s" autocomplete="off"/>'
                % (fid, attr(f.get('input_type') or 'text'), attr(f.get('placeholder') or '')))
    return ('<div class="field%s">%s%s</div>'
            % (' half' if f.get('half') else '', lab, ctrl))


# ------------------------------------------------------------------ screens
def screen_hero(p):
    """Screen 1 - the reference's opening layout with Braevon's photograph.

    The poster is braevon.com's own hero; drop a clip at assets/video/hero.mp4
    and the same element plays it instead."""
    return ('<div class="col">'
            '<div class="hero">'
            '<video class="hero-media" autoplay muted loop playsinline preload="metadata" '
            'poster="assets/images/braevon-hero.jpg">'
            '<source src="assets/video/hero.mp4" type="video/mp4"/></video>'
            '<img class="hero-product" src="assets/images/product-tablet.png" '
            'alt="The BRAEVON 4-in-1 tablet"/></div>'
            '<h1 class="hero-h1">You Deserve a<br/><span class="hi">Better Sex Life.</span></h1>'
            '<p class="strip">BRAEVON 4-in-1. Arousal &amp; performance. '
            '<strong>In minutes</strong></p>'
            '<p class="ask">See if <strong>BRAEVON</strong> is right for you.</p>'
            '<p class="ask-sub">Select your primary goal:</p>'
            + options_block(p) + cta() + '</div>')


def screen_question(p):
    """A plain question screen: the reference's h1, its first sub-head as the
    lead-in, its options, and any free-text box that follows them.

    The reference's remaining sub-heads are captions inside a long safety list
    ("Serious Reactions", "Common Side Effects"). They are dropped rather than
    faked into place: the exclusive answer is hoisted to the top here, so a
    caption would end up sitting against the wrong block. Flagged in the
    README."""
    title = brandify(p['title'])
    sub = brandify(p['subs'][0]) if p['subs'] else None
    out = ['<div class="col">', head(esc(title) if title else None,
                                     esc(sub) if sub else None)]
    if p['options']:
        out.append(options_block(p))
    for f in p['fields']:
        # the free-text box under a safety list is the reference's catch-all;
        # it never gates the screen
        out.append('<div class="reveal on" data-optional="1">%s</div>'
                   % field_block(f, 'Anything you would like to add'))
    out.append(cta())
    out.append('</div>')
    return ''.join(out)


def screen_birthdate(p):
    m = {f['name']: f for f in p['fields']}
    month = dict(m['birth_month'], options=['Month'] + MONTHS)
    day = dict(m['birth_day'], options=['Day'] + [str(i) for i in range(1, 32)])
    year = dict(m['birth_year'], placeholder='Year')
    return ('<div class="col">'
            + head('What is your date of birth?',
                   'We need to verify your age for medical review purposes.',
                   eyebrow='Last step')
            + '<div class="dob">%s%s%s</div>'
              % (field_block(month), field_block(day), field_block(year))
            + '<div class="note" style="margin-top:20px">%s<p><b>Your privacy is '
              'protected.</b> This is required for your medical review and is not '
              'shared.</p></div>' % ICON['shield']
            + cta() + '</div>')


def screen_review(p):
    m = {f['name']: f for f in p['fields']}
    mols = ''.join('<div class="mol"><div><b>%s</b><span>%s</span></div>'
                   '<div class="dose">%s</div></div>' % t for t in MOLECULES)
    return ('<div class="col">'
            '<span class="result-badge">Assessment complete</span>'
            '<h1 class="qhead" style="margin-top:16px">You are a strong candidate for '
            'prescription ED treatment.</h1>'
            '<p class="sub">A licensed clinician reviews your answers and confirms your '
            'plan. Nothing ships until they do.</p>'
            '<div class="reviewcard"><h3>Your medical review</h3>'
            '<div class="rrow"><span>Primary goal</span>'
            '<b data-echo="Q1_primary_goal">&mdash;</b></div>'
            '<div class="rrow"><span>Difficulty</span>'
            '<b data-echo="Q3_problem_getting_or_maintaining_erection">&mdash;</b></div>'
            '<div class="rrow"><span>Reviewed by</span><b>Braevon clinical team</b></div>'
            '</div>'
            '<div class="reviewcard"><h3>How BRAEVON 4-in-1 can help</h3>%s</div>' % mols
            + '<p class="legend">Let&rsquo;s check your eligibility.</p>'
            + '<div class="fields">%s%s</div>'
              % (field_block(dict(m['first_name'], half=True), 'First name'),
                 field_block(dict(m['last_name'], half=True), 'Last name'))
            + field_block(m['state'], 'What state will your medication be shipped to?')
            + cta() + '</div>')


def screen_submission(p):
    m = {f['name']: f for f in p['fields']}
    return ('<div class="col">'
            + head('<span data-name-echo>How</span> can you be reached if necessary?',
                   'Our medical team and pharmacy use email and text for patient '
                   'communication.')
            + '<div class="fields">%s%s</div>'
              % (field_block(m['email'], 'Email'),
                 field_block(m['phone_number'], 'Phone number'))
            + '<div class="opts" data-group="final_submission_terms_agreement" '
              'data-mode="multi" style="margin-top:16px">'
              '<button class="opt checkbox" data-value="yes"><span class="lbl">'
              'By clicking Submit, I agree to receive emails, customer support text '
              'messages and phone calls from Braevon, and I agree to the Terms of '
              'Service and Privacy Policy.</span><span class="ring"></span></button></div>'
            + cta('Submit') + '</div>')


def screen_interstitial(p):
    n = p['n']
    if n == 2:
        # Centred, on white, exactly as the reference sets it: the product name,
        # a gradient pill, then two figures at 58px with a rule between them.
        return ('<div class="col fact">'
                '<p class="fact-name">BRAEVON 4-in-1</p>'
                '<p class="fact-pill">Fast Acting / Long Lasting</p>'
                '<p class="fact-k accent">10&ndash;15</p>'
                '<p class="fact-u">MINUTES</p>'
                '<p class="fact-cap">Fast onset for the <b>&ldquo;Get it.&rdquo;</b></p>'
                '<div class="fact-rule"></div>'
                '<p class="fact-k"><span>36</span> HRS</p>'
                '<p class="fact-cap">The <b>&ldquo;Keep it&rdquo;</b> window<br/>'
                'for spontaneity.</p>'
                + cta(blocked=False) + '</div>')
    if n == 5:
        rows = ''.join(
            '<div class="mech"><span class="bubble" style="--bub:%s;--gly:%s">%s</span>'
            '<div><b>%s</b><span>%s</span></div></div>' % (bub, gly, svg, a, b)
            for a, b, bub, gly, svg in MECHANISM)
        return ('<div class="col">'
                + head('How BRAEVON&rsquo;s 4-in-1 Works for you',
                       'BRAEVON&rsquo;s 4-in-1 is engineered to hit both Desire (the brain) '
                       'and Performance (the body) in one dose.')
                + '<div class="reviewcard">%s</div>' % rows
                + cta(blocked=False) + '</div>')
    if n == 8:
        bars = [('L-Citrulline', 'Rapid onset', '10m', 12),
                ('Sildenafil', 'Peak strength', '4 hr', 34),
                ('Tadalafil', 'Extended window', '36 hr', 100),
                ('BRAEVON 4-in-1', 'All of it, one dose', '36 hr', 100)]
        rail = ''.join(
            '<div class="cmp%s"><div class="cmp-l"><b>%s</b><span>%s</span></div>'
            '<div class="cmp-bar"><i style="width:%d%%"></i></div>'
            '<div class="cmp-v">%s</div></div>'
            % (' on' if a.startswith(BRAND) else '', a, b, w, v)
            for a, b, v, w in bars)
        return ('<div class="col">'
                + head('A solution that starts in minutes and lasts as long as you need '
                       'it to', eyebrow='The 4-in-1 advantage')
                + '<div class="reviewcard">%s</div>' % rail
                + cta(blocked=False) + '</div>')
    if n == 33:
        return ('<div class="col">'
                + head('Her experience improves too.', eyebrow='Do it for her')
                + '<div class="factcard" style="margin-top:20px">'
                  '<div class="k">137%</div><div class="u">improvement</div>'
                  '<p>Reported improvement in sex, for partners.*</p></div>'
                + '<p class="foot">*Figure carried from the reference flow. Replace with '
                  'a Braevon source before this is shown to patients.</p>'
                + cta(blocked=False) + '</div>')
    quote, meta, who = QUOTES[n]
    chips = ''.join('<div class="qmeta"><b>%s</b><span>%s</span></div>' % kv for kv in meta)
    return ('<div class="col"><div class="quote"><blockquote>%s</blockquote>'
            '<div class="meta">%s</div><div class="who">%s</div></div>'
            % (quote, chips, who) + cta(blocked=False) + '</div>')


def render(p):
    n = p['n']
    if n == 1:
        return screen_hero(p)
    if n in INTERSTITIALS:
        return screen_interstitial(p)
    if n == 43:
        return screen_birthdate(p)
    if n == 45:
        return screen_review(p)
    if n == 47:
        return screen_submission(p)
    return screen_question(p)


def dq_reason(p):
    """Per-screen copy: "you selected a nitrate" and "your last physical was
    over three years ago" are not the same message."""
    n = p['n']
    if n == 4:
        return ('This treatment is prescribed for erectile difficulty. Based on your '
                'answer, this assessment is not the right route for you.')
    if n == 9:
        return ('Penile surgery, injections, a vacuum pump or a prosthesis needs a '
                'clinician who knows your history, so our prescribers cannot assess you '
                'from this questionnaire.')
    if n == 23:
        return ('A physical exam within the last three years is required before an ED '
                'medication can be prescribed here.')
    if 16 <= n <= 21:
        return ('The side effect you selected can be serious, and it means an ED '
                'medication cannot be safely prescribed to you through this service.')
    if n == 27:
        return ('One of the conditions you selected means an ED medication cannot be '
                'safely prescribed without an in-person assessment.')
    if n == 29:
        return ('One of the diagnoses you selected means our prescribers cannot safely '
                'determine your eligibility from this questionnaire.')
    if n == 38:
        return ('Recreational drug use in the last six months can interact dangerously '
                'with ED medication, so we cannot complete your assessment.')
    return ('Your safety is our priority. Based on your answer, our clinicians cannot '
            'safely determine your eligibility.')


# ------------------------------------------------------------------ assemble
STEPS = [p for p in FLOW if p['n'] != STOP_SCREEN]
QUESTIONS = [p for p in STEPS if p['options'] or p['fields']]
TOTAL_Q = len(QUESTIONS)


def sections():
    out, q = [], 0
    for p in STEPS:
        a = ' data-step="%d"' % p['n']
        if p in QUESTIONS:
            q += 1
            a += ' data-q="%d"' % q
        if p['n'] == 1:
            a += ' data-no-back'
        if p['cond']:
            a += (' data-if="%s" data-if-any="%s"'
                  % (attr(p['cond']['group']), attr('|'.join(p['cond']['any']))))
        if p['dq_on']:
            a += (' data-dq-on="%s" data-dq="%s"'
                  % (attr('|'.join(p['dq_on'])), attr(dq_reason(p))))
        out.append('<section class="step"%s>%s</section>' % (a, render(p)))
    return out


STARS = ('<span class="stars">%s</span>'
         % ('<i><svg viewBox="0 0 20 20" fill="currentColor"><path d="M10 1l2.7 6.1 6.6.6'
            '-5 4.4 1.5 6.5L10 15.3 4.2 18.6l1.5-6.5-5-4.4 6.6-.6L10 1z"/></svg></i>' * 5))

MASTHEAD = (
    '<header class="masthead">'
    '<div class="logo">%s</div>'
    '<div class="rating"><span class="txt">Excellent 4.6</span>%s</div>'
    '</header><div class="rule"></div>' % (LOGO, STARS))


# The back arrow sits at the left of the progress row, where the reference puts
# it - aligned with the wordmark above, with the bar starting after it. It keeps
# its slot when hidden, so the bar does not shift between a screen with an arrow
# and one without.
def nav(progress):
    return ('<div class="navrow">'
            '<button class="back-btn" id="backBtn" aria-label="Go back">%s</button>'
            '%s</div>' % (ICON['back'], progress))


PROGRESS = nav('<div class="progress" id="prog" role="progressbar" '
               'aria-label="Assessment progress" aria-valuemin="1" aria-valuemax="%d" '
               'aria-valuenow="1" aria-valuetext="Question 1 of %d">%s</div>'
               % (TOTAL_Q, TOTAL_Q,
                  ''.join('<div class="seg"><span></span></div>' for _ in range(SEGMENTS))))

DQ = ('<div class="dq" id="dq" role="dialog" aria-modal="true" aria-labelledby="dqTitle">'
      '<div class="dq-inner"><div class="dq-mark">%s</div>'
      '<h1 id="dqTitle">Eligibility status</h1>'
      '<p class="dq-sub">Based on your last answer, we cannot complete your assessment. '
      'Your safety is our priority: this treatment has specific medical criteria, and '
      'your response prevents our clinicians from safely determining your eligibility.</p>'
      '<div class="dq-reason" id="dqReason"></div>'
      '<p class="dq-note">Made a mistake? Review your answer. If it was correct, please '
      'speak with your own doctor about other options.</p>'
      '<button class="dq-back" id="dqBack">Review my answer</button>'
      '<button class="dq-ghost" id="dqExit">Exit the assessment</button>'
      '</div></div>' % ICON['warn'])

SCRIPT = open(os.path.join(HERE, 'engine.js'), encoding='utf-8').read()


def page(title, body, body_class=''):
    cls = ' class="%s"' % body_class if body_class else ''
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8"/>\n'
            '<title>%s</title>\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1"/>\n'
            # an unreleased prototype carrying placeholder marketing claims
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


def static_progress(q):
    """A frame carries no script, so its bar is drawn at the width that
    question would have reached - otherwise every frame imports empty."""
    per = TOTAL_Q / float(SEGMENTS)
    at = int((q - 1) // per)
    segs = ['<div class="seg"><span style="width:%d%%"></span></div>' % (100 if k <= at else 0)
            for k in range(SEGMENTS)]
    return nav('<div class="progress" role="progressbar" aria-valuenow="%d">%s</div>'
               % (q, ''.join(segs)))


def emit_frames():
    frames, q = [], 0
    for p, html in zip(STEPS, sections()):
        counted = p in QUESTIONS
        if counted:
            q += 1
        lbl = 'Screen %02d &mdash; %s' % (p['n'], esc(p['name']))
        inner = html.replace('<section class="step"', '<section class="step on"', 1)
        # ids are unique per document; 46 frames cannot each carry the
        # interactive build's element ids
        chrome = (MASTHEAD + (static_progress(q) if counted else nav(''))
                  ).replace(' id="backBtn"', '')
        if p['n'] == 1:
            chrome = chrome.replace('<button class="back-btn"', '<button class="back-btn" hidden')
        frames.append('<div class="frame-label">%s</div><div class="frame"><div class="shell">'
                      '%s<main class="stage">%s</main></div></div>' % (lbl, chrome, inner))
    frames.append('<div class="frame-label">Screen %02d &mdash; NO RX (eligibility stop)</div>'
                  '<div class="frame">%s</div>'
                  % (STOP_SCREEN, DQ.replace('class="dq"', 'class="dq on"')))
    open(os.path.join(OUT, 'all-screens.html'), 'w', encoding='utf-8').write(
        page('Braevon &mdash; Intake v2, all screens', '\n'.join(frames), 'frames'))
    return len(frames)


if __name__ == '__main__':
    emit_interactive()
    n = emit_frames()
    print('index.html + interactive.html   %d screens, %d counted questions'
          % (len(STEPS), TOTAL_Q))
    print('all-screens.html                %d frames' % n)
