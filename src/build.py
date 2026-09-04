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

import checkout
import flow_v1
from logo import LOGO
from theme import CSS

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)

# **The flow is Braevon's own 24 questions**, from 2026-09-04. It was the MEDVi
# QUAD reference's 40 until then; the client asked for the reference's questions
# to be replaced with v1's, keeping v2's design and every component - and for no
# screen that does not ask something to be carried over. `flow_v1.py` does the
# reshaping and refuses to build a screen with no question on it; the reference's
# own flow stays in `medvi-flow.json` beside it, unread, so a screen can be
# pulled back one at a time if the client wants one.
FLOW = flow_v1.FLOW
# Where the exclusive answer sits on each multi-answer screen, the line under it
# when it has one, and the captions that break a long list into groups. Read off
# the live reference on 2026-09-03, because the DOM extraction flattens all
# three away. Keyed by screen; the caption is keyed by the label of the option
# it sits above.
# Where the "none of these" answer sits, per screen. v1 hoists it to the top of
# every list that has one, so this is derived from the flow rather than read off
# a page - `groups.json` was the reference's and is no longer loaded.
GROUPS = {str(n): {'exclusive_first': True, 'exclusive_note': None, 'captions': {}}
          for n in flow_v1.EXCLUSIVE_FIRST}

BRAND = 'BRAEVON'
# The eligibility stop is an overlay, not a screen, in both flows.
STOP_SCREEN = None
# **Nothing here is an interstitial any more.** Every screen in this flow asks
# something - that is the rule the client set - so the reference's marketing,
# processing and read-back screens have no counterpart. The renderers for them
# are still below and are simply never reached; they are the reference
# implementation and are kept so a screen can be brought back deliberately.
INTERSTITIALS = set()
# v1's two-up control, its sex question's Male / Female cards. Read off the
# extraction (`style: tiles`) rather than listed by number.
TILE_SCREENS = flow_v1.TILE_SCREENS

SEGMENTS = 5
# No screen carries its own chrome in this flow.
BARE_SCREEN = None

# The approval / checkout page, added on 2026-09-04. It is not in
# `medvi-flow.json` because it is not part of the questionnaire: the reference
# serves it from `/approval`, a separate page the intake hands off to, and the
# extractor only walks `/intake-s`. It is built by `checkout.py` and appended to
# the flow as one more step, so Submit walks onto it the way Continue walks onto
# any other screen. Like the medical review it carries its own chrome, so it is
# `data-bare` too.
CHECKOUT_SCREEN = 48

# The reference numbers its own steps - every screen name ends in one ("A2 - 03",
# "Blood Pressure 2 - 07.a", "Birth Date - 20"), running 1 to 21. Its bar is
# divided over those steps, not over our question count, which is why an even
# five-way split of 40 questions ran a segment ahead of it.
#
# Boundaries below are the step each segment starts at. Confirmed against the
# live page: step 5 and step 6 sit in segment 1, step 7 through 11 in segment 2,
# step 12 in segment 3. The last two (16, 19) are the remaining steps split
# evenly and are NOT confirmed - see the README.
SEGMENT_STARTS = flow_v1.SEGMENT_STARTS

_STEP_RE = re.compile(r'-\s*(\d+)')


def step_of(p):
    """The reference's own step number for a screen, from its name.

    The LAST number in the name is the step: "FACT-2 - 12" is step 12, not 2.
    An interstitial is not a step even when its name carries one - the
    reference holds the bar at the step before it, which is why its "137%"
    screen and the question after it both say "12" but sit in different
    segments. The stop and the submission have no step at all."""
    if p['n'] in INTERSTITIALS:
        return None
    found = _STEP_RE.findall(p.get('name') or '')
    return int(found[-1]) if found else None


def segment_of(step):
    """Which of the five segments a step falls in, zero-based."""
    at = 0
    for i, start in enumerate(SEGMENT_STARTS):
        if step >= start:
            at = i
    return at


# Every screen's step, with the interstitials holding the step before them -
# which is what the reference's own bar does as you pass through one.
STEP_AT = {}
_last = 1
for _p in FLOW:
    _s = step_of(_p)
    if _s:
        _last = _s
    STEP_AT[_p['n']] = _last


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
    'info': _ic('<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>'),
    'star': ('<svg viewBox="0 0 20 20" fill="currentColor"><path d="M10 1l2.7 6.1 6.6.6'
             '-5 4.4 1.5 6.5L10 15.2 4.2 18.6l1.5-6.5-5-4.4 6.6-.6z"/></svg>'),
    'person': _ic('<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>'),
    'tick': _ic('<path d="M5 12.5l4.5 4.5L19 7.5"/>'),
    'clock': _ic('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>'),
    'check': _ic('<path d="M4 12.5l5 5L20 6.5"/>'),
}

# Screen 1's goal icons, keyed by the reference's own option labels. The bubble
# and glyph colours are its design tokens - "Light Green 1"/"Green", "light
# blue"/"blue 2", "Light red", "light purple"/"purple", "Light Orange"/"Orange".
# A deliberate exception to the rule that orange carries emphasis: the client
# asked for these five hues and nothing else in the flow takes them.
# Screen 1's goal icons, keyed by **v1's** option labels from 2026-09-04 (they
# were the reference's until then). The five hues are the client's own, set on
# 2026-09-03, and are a deliberate exception to orange carrying emphasis -
# nothing else in the flow uses them. Paired to the nearest sense: a stopwatch
# for lasting, a rising line for erections, a heart for arousal, a refresh arrow
# for rebound, a shield-tick for confidence.
GOAL_STYLE = {
    'Last longer':         ('#DFF7E6', '#22C55E',
                            _ic('<circle cx="12" cy="13" r="8"/><path d="M12 9v4l2.5 2.5M9 2h6"/>')),
    'Better erections':    ('#DBEAFE', '#31ABE8',
                            _ic('<path d="M4 17l5-5 4 4 7-7"/><path d="M14 9h6v6"/>')),
    'More arousal':        ('#FEE2E2', '#EC4899',
                            _ic('<path d="M12 21s-7-4.5-7-9.5A4.5 4.5 0 0 1 12 8a4.5 4.5 0 0 1 7 3.5c0 5-7 9.5-7 9.5z"/>')),
    'Faster rebound time': ('#F3EBFF', '#A855F7',
                            _ic('<path d="M20 12a8 8 0 1 1-2.3-5.6"/><path d="M20 3v5h-5"/>')),
    'More confidence':     ('#FFEDD5', '#F97316',
                            _ic('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>')),
}

_DROP = _ic('<path d="M12 3s6 6.5 6 10.5a6 6 0 0 1-12 0C6 9.5 12 3 12 3z"/>')

# The sex screen's two cards carry a 64px icon bubble in the reference, in the
# same two hues its goal icons use. The other tile screens carry a small mark
# that reads as decoration, and are left plain.
# v1's sex question is screen 4, and it is the only tile screen in this flow.
TILE_ICONS = {
    (4, 'male'):   ('#DBEAFE', '#3B82F6',
                    _ic('<circle cx="10" cy="14" r="6"/><path d="M15 9l6-6M15 3h6v6"/>')),
    (4, 'female'): ('#FCE7F3', '#EC4899',
                    _ic('<circle cx="12" cy="9" r="6"/><path d="M12 15v7M9 19h6"/>')),
}

# The blood-pressure screens read as a scale, and the reference colours them as
# one: a droplet per band, running blue (low) through green (normal) to red,
# with the band's own caption in the same hue. "I don't know" steps out of the
# scale and takes a grey cross.
BAND_SCREENS = flow_v1.BAND_SCREENS

# v1's five blood-pressure bands, in its own values. The ramp is the reference's
# - blue for low, green for normal, red for high - so the list reads as a scale
# rather than five equal choices.
BAND_STYLE = {
    (25, 'very-high'): ('#FEE2E2', '#EF4444'),
    (25, 'high'):      ('#FFEDD5', '#F97316'),
    (25, 'normal'):    ('#DFF7E6', '#22C55E'),
    (25, 'low'):       ('#DBEAFE', '#3B82F6'),
    (25, 'very-low'):  ('#E0E7FF', '#6366F1'),
}

_NOBAND = ('#E9ECF1', '#94A3B8')
_CROSS = _ic('<circle cx="12" cy="12" r="9"/><path d="M9 9l6 6M15 9l-6 6"/>')

# The reference marks a yes/no screen with a green tick and a red cross - but
# on the answer, not on the word. "Do you still wake up with an erection?" puts
# the tick on Yes; "Are you allergic to any of these?" puts it on No, because
# there No is the good news. So the tick follows the favourable answer, which
# is per screen.
_TICK_ART  = ('#DFF7E6', '#22C55E', _ic('<path d="M5 12.5l4.5 4.5L19 7.5"/>'))
_CROSS_ART = ('#FEE2E2', '#EF4444', _ic('<path d="M6.5 6.5l11 11M17.5 6.5l-11 11"/>'))
# Keyed to the reference's screens, which are gone. v1 draws no yes/no screen as
# a pair of tiles - its only tile screen is the sex question - so nothing reads
# this today. Left in place because the treatment is right and one line brings
# it back if a Braevon screen is ever drawn that way.
GOOD_ANSWER = {}

# **Every table in this block was keyed to the reference's screen numbers**, and
# those screens are not in this flow. They are emptied rather than re-guessed
# onto Braevon's questions: which headline word takes the accent, which sub-head
# is a heading rather than a caption, which screen carries a photograph and
# which carries a footnote are per-screen judgements about the reference's copy,
# and inventing new ones for v1's copy is design work nobody has asked for.
#
# Adding an entry is one line each and the renderers all still read them, so any
# of it can come back for a named Braevon screen when someone decides it should.
LEADS = set()          # sub-heads set as a second heading rather than a caption
LEGENDS = set()        # v1 carries its own legends inline, in document order
SCREEN_IMAGE = {}      # the reference's one photographed question screen
REVEALS = {}           # v1's reveals are in its own blocks, rendered in order
MEDLISTS = {}
BREAKS = {}
FOOTNOTES = {}
HIGHLIGHTS = {}

# **This flow preselects only what v1 preselects**, and that is two screens:
# "Male" on the eligibility question and "Normal" on the blood-pressure bands.
# Both are v1's own decisions, and the extraction carries them as `preselected`.
#
# The reference's rule was different and is deliberately not carried over: it
# opened *every* single-answer screen on its first option, which on its safety
# screens meant a patient clicking through submitted "no allergies, no
# medications, no conditions" without reading one of them. v2's own README
# flagged that as the thing on the build most in need of a prescriber's
# sign-off. With Braevon's questions there is no reason to reintroduce it, so an
# unanswered safety screen stays unanswered and the CTA says what is missing.
DEFAULTS = {p['n']: o['value']
            for p in FLOW for o in p['options'] if o.get('preselected')}


def _none_of(p):
    """The "none of these" answer on a multi-answer screen. v1 marks its own
    with `data-exclusive`, so unlike the reference there is nothing to infer."""
    return p['exclusive']


def highlight(n, title):
    """Wrap this screen's accented phrase and put in its line break."""
    at = BREAKS.get(n)
    if at and at in title:
        title = title.replace(at, at + '<br/>', 1)
    phrase = HIGHLIGHTS.get(n)
    if not phrase or phrase not in title:
        return title
    return title.replace(phrase, '<span class="hl">%s</span>' % phrase, 1)


# Braevon's four, in the order braevon.com lists them. The dose column is not
# rendered anywhere and the figures in it were never verified - see the README.
_BRAIN = _ic('<path d="M12 6a3.2 3.2 0 0 0-6-1.1A2.7 2.7 0 0 0 4.2 9.4 2.8 2.8 0 0 0 6 14.4'
             'a3 3 0 0 0 3 2.6"/><path d="M12 6a3.2 3.2 0 0 1 6-1.1 2.7 2.7 0 0 1 1.8 4.5'
             'A2.8 2.8 0 0 1 18 14.4a3 3 0 0 1-3 2.6"/><path d="M12 6v15"/>')
_HEART = _ic('<path d="M12 21s-7-4.5-7-9.5A4.5 4.5 0 0 1 12 8a4.5 4.5 0 0 1 7 3.5'
             'c0 5-7 9.5-7 9.5z"/>')

MOLECULES = [
    ('Sildenafil', 'For getting hard fast', '&mdash;'),
    ('Tadalafil', 'For staying ready up to 36 hours', '&mdash;'),
    ('Vardenafil', 'For a firmer, more reliable response', '&mdash;'),
    ('Apomorphine', 'Ignites desire in the brain', '&mdash;'),
]

# Screen 5 reads as a benefit list, not an ingredient table: the reference leads
# each row with what the molecule does for you and names the molecule second.
# Bubble hues follow the goal-icon tokens - purple, green, red, blue.
MECHANISM = [
    ('Spark Desire', 'Apomorphine ignites desire in the brain.',
     '#F3EBFF', '#A855F7',
     _ic('<path d="M12 6a3.2 3.2 0 0 0-6-1.1A2.7 2.7 0 0 0 4.2 9.4 2.8 2.8 0 0 0 6 14.4'
         'a3 3 0 0 0 3 2.6"/><path d="M12 6a3.2 3.2 0 0 1 6-1.1 2.7 2.7 0 0 1 1.8 4.5'
         'A2.8 2.8 0 0 1 18 14.4a3 3 0 0 1-3 2.6"/><path d="M12 6v15"/>')),
    ('Start Fast', 'Sildenafil gets you hard fast.',
     '#DFF7E6', '#22C55E',
     _ic('<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>')),
    ('Boost Performance', 'Vardenafil gives a firmer, more reliable response.',
     '#FEE2E2', '#EF4444',
     _ic('<path d="M12 21s-7-4.5-7-9.5A4.5 4.5 0 0 1 12 8a4.5 4.5 0 0 1 7 3.5c0 5-7 9.5-7 9.5z"/>')),
    ('Last Longer', 'Tadalafil keeps you ready for up to 36 hours.',
     '#DBEAFE', '#3B82F6',
     _ic('<rect x="2.5" y="7.5" width="15" height="9" rx="2.6"/>'
         '<path d="M20.5 10.5v3"/><path d="M6 10.5v3"/>')),
]

# Placeholder copy written for this concept, not real reviews - see the module
# docstring. Structure and slot are the reference's.
_PINK = ('#FCE7F3', '#EC4899')
_PURPLE = ('#F3EBFF', '#A855F7')
_HEART_RED = ('#FEE2E2', '#EF4444')
_GREEN2 = ('#DFF7E6', '#22C55E')

QUOTES = {
    32: ('&ldquo;It probably saved my marriage.&rdquo;',
         [('Personal Goal',
           [_PINK + (_ic('<path d="M4 17l5-5 4 4 7-7"/><path d="M14 9h6v6"/>'),)],
           'Boost Sex Drive and Desire'),
          ('Benefits',
           [_PURPLE + (_BRAIN,), _HEART_RED + (_HEART,)],
           'Mental Mood and<br/>Lasting Effects')],
         'Ethan Caldwell &mdash; Kansas City, MO', 'hero-benefits.jpg',
         ('hero-benefits.jpg', '66% 12%')),
    44: ('&ldquo;The results were almost immediate &mdash; more energy, more desire, '
         'and a stronger performance every time.&rdquo;',
         [('Personal Goal',
           [_GREEN2 + (_ic('<circle cx="12" cy="13" r="8"/>'
                           '<path d="M12 9v4l2.5 2.5M9 2h6"/>'),)],
           'Improve Stamina and Endurance'),
          ('Benefits',
           [_GREEN2 + (_ic('<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>'),), _HEART_RED + (_HEART,)],
           'Quick Effect and<br/>Lasting Performance')],
         # Not the white-coat shot: this is a customer, not a clinician. Shares
         # stat-hero.jpg with screen 41's banner - a 28px avatar and a 168px
         # banner on different screens do not read as the same picture, but a
         # portrait of its own would be better. See the README.
         'Ryan Mitchell &mdash; New York, NY', 'braevon-hero.jpg',
         ('stat-hero.jpg', '50% 20%')),
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


def head(title=None, sub=None, eyebrow=None, lead=False):
    """`lead` marks a sub-head that is carrying the claim rather than
    captioning a question - the reference sets those as a second heading."""
    out = ''
    if eyebrow:
        out += '<p class="eyebrow">%s</p>' % eyebrow
    if title:
        out += '<h1 class="qhead">%s</h1>' % title
    if sub:
        out += '<p class="sub%s">%s</p>' % (' lead' if lead else '', sub)
    return out


def option(o, exclusive, goal=False, tile=False, screen=None,
           excl_first=False, excl_note=None, band=False):
    """`band` is passed rather than inferred from the screen. v1's
    blood-pressure screen carries two lists - the five bands and, under the
    warning, a single opt-out checkbox - and keying the droplet treatment off
    the screen number painted the opt-out as a grey crossed band too."""
    label = esc(brandify(o['label']))
    on = ' selected' if DEFAULTS.get(screen) == o['value'] else ''
    if tile:
        note = ('<small>%s</small>' % esc(brandify(o['note']))) if o.get('note') else ''
        val = (o['value'] or '').lower()
        art = TILE_ICONS.get((screen, val))
        good = GOOD_ANSWER.get(screen)
        if not art and good and val in ('yes', 'no'):
            art = _TICK_ART if val == good else _CROSS_ART
        bub = ('<span class="bubble big" style="--bub:%s;--gly:%s">%s</span>' % art
               ) if art else ''
        return ('<button class="opt tile%s" data-value="%s">%s'
                '<span class="lbl">%s%s</span></button>'
                % (on, attr(o['value']), bub, label, note))
    if goal:
        bub, gly, glyph = GOAL_STYLE.get(o['label'], ('#FDECE6', '#E6430D', ICON['shield']))
        return ('<button class="opt goal%s" data-value="%s"><span class="bubble" '
                'style="--bub:%s;--gly:%s">%s</span><span class="lbl">%s</span></button>'
                % (on, attr(o['value']), bub, gly, glyph, label))
    if band:
        bub, gly = BAND_STYLE.get((screen, o['value']), _NOBAND)
        glyph = _DROP if (screen, o['value']) in BAND_STYLE else _CROSS
        note = ('<small style="color:%s">%s</small>' % (gly, esc(brandify(o['note'])))
                ) if o.get('note') else ''
        return ('<button class="opt band%s" data-value="%s"><span class="bubble" '
                'style="--bub:%s;--gly:%s">%s</span>'
                '<span class="lbl">%s%s</span></button>'
                % (on, attr(o['value']), bub, gly, glyph, label, note))
    inner = label
    if o.get('note'):
        inner += '<small>%s</small>' % esc(brandify(o['note']))
    excl = o['value'] == exclusive
    if excl and excl_note:
        inner = ('%s<small>%s</small>'
                 % (label, esc(brandify(excl_note))))
    # `last` draws the rule above a trailing exclusive; `safe` is the green
    # card the reference gives it when it leads the list instead.
    mark = (' safe' if excl and excl_first else (' last' if excl else ''))
    return ('<button class="opt%s%s%s" data-value="%s"%s>'
            '<span class="lbl">%s</span><span class="ring"></span></button>'
            % (' checkbox' if o['type'] == 'checkbox' else '',
               mark, on, attr(o['value']),
               ' data-exclusive="1"' if excl else '', inner))


def options_block(p):
    """Renders a screen's options in the reference's own order.

    Where the exclusive answer goes is per screen, not a rule: the reference
    puts "None of the above" last on the ED-treatments screen and first - green,
    under a line telling you it is the answer that lets you continue - on the
    safety screens where every other answer is disqualifying. GROUPS carries
    that, along with the captions that break the long lists into sections."""
    goal = p['n'] == 1
    tile = p['n'] in TILE_SCREENS
    g = GROUPS.get(str(p['n']), {})
    excl_first = g.get('exclusive_first', False)
    if tile:
        opts = p['options']
    else:
        opts = sorted(p['options'],
                      key=lambda o: (o['value'] == p['exclusive']) != excl_first)
    caps = g.get('captions') or {}
    out = []
    for o in opts:
        cap = caps.get(o['label'])
        if cap:
            out.append('<p class="optcap">%s</p>' % esc(cap))
        note = g.get('exclusive_note') if o['value'] == p['exclusive'] else None
        out.append(option(o, p['exclusive'], goal, tile, p['n'], excl_first, note,
                          band=p['n'] in BAND_SCREENS))
    return ('<div class="opts%s" data-group="%s" data-mode="%s">%s</div>'
            % (' tilegrid' if tile else '', attr(p['group']), p['mode'], ''.join(out)))


def options_of(p, block, tile=False):
    """`options_block()` renders a screen's primary list from the flat record.
    v1 screens can carry a second list - screen 25's opt-out - and their reveals
    carry Yes/No pairs of their own, so this renders any one block."""
    excl = _exclusive_of(block)
    excl_first = bool(excl)
    opts = [{'value': o['value'], 'label': o['label'],
             'type': 'checkbox' if block['mode'] == 'multi' else 'radio',
             **({'note': o['note']} if o.get('note') else {}),
             **({'sub': o['sub']} if o.get('sub') else {})}
            for o in block['options']]
    if not tile:
        opts = sorted(opts, key=lambda o: (o['value'] == excl) != excl_first)
    out = ''.join(option(o, excl, False, tile, p['n'], excl_first, None,
                         band=bool(block.get('grouped')))
                  for o in opts)
    return ('<div class="opts%s" data-group="%s" data-mode="%s"%s>%s</div>'
            % (' tilegrid' if tile else '', attr(block['group']), block['mode'],
               ' data-optional="1"' if block.get('optional') else '', out))


def _exclusive_of(block):
    for o in block['options']:
        if o.get('exclusive'):
            return o['value']
    return None


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
        # A US number and nothing else: ten digits, formatted as they are typed,
        # with the numeric keypad on a phone.
        extra = (' data-us-phone="1" inputmode="tel" maxlength="14"'
                 if f.get('us_phone') else '')
        ctrl = ('<input id="%s" type="%s" placeholder="%s" autocomplete="off"%s/>'
                % (fid, attr(f.get('input_type') or 'text'),
                   attr(f.get('placeholder') or ''), extra))
    # Every field carries its own (hidden) error line, so a failed submit can
    # say what is wrong under the field rather than only shaking the screen.
    return ('<div class="field%s">%s%s<p class="err" hidden></p></div>'
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
            # The screen's own instruction, not a fixed one: the reference asked
            # for a single primary goal and v1 asks for all that apply, so a
            # hardcoded "Select your primary goal:" contradicted its own control.
            + '<p class="ask-sub">%s</p>'
              % esc(brandify(p['subs'][0] if p['subs'] else 'Select your goal:'))
            + options_block(p) + cta(blocked=p['n'] not in DEFAULTS) + '</div>')


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
    out = ['<div class="col">']
    if p['n'] in SCREEN_IMAGE:
        src, alt = SCREEN_IMAGE[p['n']]
        out.append('<div class="qshot-top"><img src="assets/images/%s" alt="%s"/></div>'
                   % (src, attr(alt)))
    out += [head(highlight(p['n'], esc(title)) if title else None,
                 esc(sub) if sub else None,
                 lead=p['n'] in LEADS)]
    if p['n'] in MEDLISTS:
        out.append('<ul class="medlist">%s</ul>'
                   % ''.join('<li>%s</li>' % esc(t) for t in MEDLISTS[p['n']]))
    if p['n'] in LEGENDS and len(p['subs']) > 1:
        out.append('<p class="legend">%s</p>' % esc(brandify(p['subs'][1])))
    if p['options']:
        out.append(options_block(p))
    if p['n'] in REVEALS:
        legend, name = REVEALS[p['n']]
        out.append('<div class="reveal" data-optional="1" data-reveal-for="%s" '
                   'data-reveal-on="yes">%s</div>'
                   % (attr(p['group']),
                      field_block({'tag': 'textarea', 'name': name,
                                   'placeholder': 'Write here...'}, legend)))
    if p['n'] in FOOTNOTES:
        title, body = FOOTNOTES[p['n']]
        out.append('<div class="infonote">%s<div><b>%s</b><p>%s</p></div></div>'
                   % (ICON['info'], title, body))
    # The extractor picks up a hidden catch-all input on every multi-answer
    # screen, named `answer_<group>`. The reference never renders those, so
    # neither does this - the answers are the options. A field with any other
    # name is a real question, though: screen 22 is nothing but its textarea,
    # and dropping it left that screen asking for a list with nowhere to type.
    for f in p['fields']:
        if (f['name'] or '').startswith('answer_'):
            continue
        out.append(field_block(f, brandify(p['title']) and None))
    out.append(cta(blocked=p['n'] not in DEFAULTS))
    out.append('</div>')
    return ''.join(out)


def screen_v1(p):
    """A Braevon question screen, rendered in v2's components.

    v1 composes a screen freely - eyebrow, title, a note, a legend, its options,
    a legend again, a row of fields - and the order carries meaning ("Sex
    assigned at birth" belongs above the tiles, "Date of birth" above the three
    selects). So this walks the extracted blocks in document order rather than
    rebuilding a fixed shape from the flat record, and every piece it emits is
    v2's own component: `.eyebrow`, `.qhead`, `.sub`, `.note`, `.legend`,
    `.opts`, `.reveal`, `.field`, `.cta`.

    Nothing here is reference-specific. The screens the reference rendered
    specially - its hero, its interstitials, its birth-date step, its medical
    review, its submission page - have no counterpart in this flow; their
    renderers are below and unreachable.
    """
    out = ['<div class="col">']
    fields = []           # consecutive fields collect into one `.fields` row
    dob = []              # …and v1's three date selects into `.dob`

    def flush():
        """Fields are laid out as a row, so they cannot be emitted one at a
        time: `.field.half` only pairs up inside a `.fields` wrapper."""
        if dob:
            out.append('<div class="dob">%s</div>' % ''.join(dob))
            del dob[:]
        if fields:
            out.append('<div class="fields">%s</div>' % ''.join(fields))
            del fields[:]

    tile = p['n'] in TILE_SCREENS
    for b in p['blocks']:
        t = b['t']
        if t in ('eyebrow', 'title', 'sub', 'legend', 'note', 'options'):
            flush()
        if t == 'eyebrow':
            out.append('<p class="eyebrow">%s</p>' % esc(brandify(b['text'])))
        elif t == 'title':
            out.append('<h1 class="qhead">%s</h1>' % esc(brandify(b['text'])))
        elif t == 'sub':
            out.append('<p class="sub">%s</p>' % esc(brandify(b['text'])))
        elif t == 'legend':
            out.append('<p class="legend">%s</p>' % esc(brandify(b['text'])))
        elif t == 'note':
            # v1 keeps `<b>` inside this one - the eligibility panel leans on it
            # for "male" and "18 years of age", which is the point of the panel.
            lead = ('<b>%s</b> ' % esc(b['lead'])) if b.get('lead') else ''
            body = re.sub(r'&lt;(/?b)&gt;', r'<\1>', esc(brandify(b['text'])))
            out.append('<div class="note">%s<p>%s%s</p></div>'
                       % (ICON['info'], lead, body))
        elif t == 'options':
            out.append(options_of(p, b, tile=tile and b.get('style') == 'tiles'))
        elif t == 'reveal':
            out.append(reveal_block(b))
        elif t == 'field':
            (dob if b.get('dob') else fields).append(
                field_block(_field_of(b), b.get('label')))
    flush()
    out.append(cta(blocked=p['n'] not in DEFAULTS))
    out.append('</div>')
    return ''.join(out)


def _field_of(b):
    """v1's field block into the record `field_block()` reads. The id is kept
    exactly as v1 wrote it - the engine and the checkout's echoes look controls
    up by it (`#firstName`, `#state`)."""
    f = {'tag': b['tag'], 'name': b['id'],
         'input_type': b.get('input_type'),
         'placeholder': b.get('placeholder'),
         'half': bool(b.get('half'))}
    if b.get('options'):
        f['options'] = b['options']
    if b['id'] == 'phone':
        f['us_phone'] = True
    return f


def reveal_block(b):
    """A follow-up that opens on a given answer. v1 has three kinds and they all
    use v2's `.reveal`:

    * a free-text box - the common case;
    * a **Yes/No question of its own** (`curve-recent`, `curve-pain`,
      `heart-recent`, `stroke-recent`), which is where four of the six stopping
      rules actually live, so losing them would have quietly disarmed the
      safety screens;
    * the blood-pressure warning, which is a line of copy rather than a control.

    `data-optional` is set on the text boxes: like the reference's, v1's do not
    gate the step. The Yes/No ones are NOT optional - an open question that can
    stop the flow has to be answered."""
    if b.get('kind') == 'bp-warning':
        return ('<div class="reveal warn" data-bp-warning data-reveal-for="%s" '
                'data-reveal-on="%s"><p>%s</p></div>'
                % (attr(b.get('for') or ''), attr(b.get('on') or ''),
                   esc(brandify(b.get('text') or ''))))
    inner = ''
    if b.get('options'):
        inner = ('<p class="legend">%s</p>' % esc(brandify(b['label']))
                 if b.get('label') else '')
        inner += ('<div class="opts tilegrid" data-group="%s" data-mode="%s">%s</div>'
                  % (attr(b['group']), b.get('mode') or 'single',
                     ''.join(option({'value': o['value'], 'label': o['label'],
                                     'type': 'radio'}, None, False, True, None)
                             for o in b['options'])))
        optional = ''
    else:
        inner = field_block({'tag': b.get('control') or 'textarea',
                             'name': (b.get('for') or 'answer') + '-detail',
                             'placeholder': b.get('placeholder') or 'Write here…'},
                            b.get('label'))
        optional = ' data-optional="1"'
    err = ('<p class="err" data-err>%s</p>' % esc(b['error'])) if b.get('error') else ''
    return ('<div class="reveal"%s data-reveal-for="%s" data-reveal-on="%s">%s%s</div>'
            % (optional, attr(b.get('for') or ''), attr(b.get('on') or ''),
               inner, err))


def screen_birthdate(p):
    """The reference labels each box above it and lets the closed select read
    as its first real value - "January", "01", "1985" - rather than putting
    "Month"/"Day"/"Year" inside as placeholder text. Its own labels are the
    screen's remaining sub-heads, which the extraction already carries."""
    m = {f['name']: f for f in p['fields']}
    labels = (p['subs'][1:4] + ['Month', 'Day', 'Year'])[:3]
    month = dict(m['birth_month'], options=MONTHS)
    day = dict(m['birth_day'], options=['%02d' % i for i in range(1, 32)])
    year = dict(m['birth_year'], placeholder='1985')
    return ('<div class="col">'
            + '<p class="steppill">%s LAST STEP</p>' % ICON['clock']
            + head('What is your date of birth?',
                   'We need to verify your age for medical review purposes.')
            + '<div class="dob">%s%s%s</div>'
              % (field_block(month, labels[0]), field_block(day, labels[1]),
                 field_block(year, labels[2]))
            # The reference uses the same tinted panel here that it uses on the
            # blood-pressure screen, in its accent rather than a grey box, and
            # its own longer wording.
            + '<div class="infonote">%s<div><b>Your privacy is protected</b>'
              '<p>This information is required for medical review and is kept '
              'strictly confidential in accordance with HIPAA regulations.</p>'
              '</div></div>' % ICON['shield']
            + cta() + '</div>')


def screen_review(p):
    """The reference drops its own masthead and bar here and puts a result
    header in their place, so this screen carries its own chrome - see the
    `data-bare` handling in sections()/emit_frames().

    Every figure and read-back below is the reference's, with the echoes wired
    to the patient's real answers. The 94% is NOT ours - see the README."""
    m = {f['name']: f for f in p['fields']}
    rows = [('Your Primary Goal:', 'Q1_primary_goal',
             ('#DBEAFE', '#3B82F6',
              _ic('<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/>'
                  '<path d="M12 3v3M12 18v3M3 12h3M18 12h3"/>'))),
            ('Performance Issues:', 'Q3_problem_getting_or_maintaining_erection',
             ('#F3EBFF', '#A855F7',
              _ic('<path d="M4 17l5-5 4 4 7-7"/><path d="M14 9h6v6"/>'))),
            ('Duration Satisfaction:', 'Q4_erection_last_as_long_as_desired',
             ('#FFEDD5', '#F97316',
              _ic('<rect x="2.5" y="7.5" width="15" height="9" rx="2.6"/>'
                  '<path d="M20.5 10.5v3"/><path d="M6 10.5v3"/>'))),
            ]
    readback = ''.join(
        '<div class="rvrow"><span class="bubble" style="--bub:%s;--gly:%s">%s</span>'
        '<div><b>%s</b><span data-echo="%s">&mdash;</span></div></div>'
        % (art[0], art[1], art[2], label, group)
        for label, group, art in rows)
    helps = ''.join('<li>%s%s</li>' % (ICON['check'], t) for t in
                    ('Effects in 10&ndash;15 minutes', 'Boosted Desire',
                     'Long-Lasting Results'))
    return ('<div class="col rv">'
            '<div class="rv-head"><div><b>BRAEVON</b><span>ED Treatment</span></div>'
            '<div class="rv-head-r"><span>Assessment Complete</span>'
            '<span class="rv-ready">Ready for Review</span></div></div>'
            '<div class="rv-ok">%s<div><b>Assessment Complete</b>'
            '<p>Congratulations! You&rsquo;re a strong candidate for a prescription '
            'ED treatment.</p></div></div>'
            '<div class="rv-panel">'
            '<h1 class="rv-title">Your Medical Review</h1>'
            '<div class="rv-card rv-prob">'
            '<div class="rv-prob-top"><span>Success Probability</span><b>94%%</b></div>'
            '<div class="rv-bar"><i style="width:94%%"></i></div></div>'
            '<div class="rv-card">%s</div>'
            '<p class="rv-verdict"><b>You are a strong candidate</b><br/>'
            'for prescription ED treatment</p>'
            '</div>'
            '<div class="rv-help">'
            '<img src="assets/images/product-tablet.png" alt="The BRAEVON 4-in-1 tablet"/>'
            '<div><b>How BRAEVON 4-in-1 Can Help</b>'
            '<p>Our 4-in-1 formula helps you by targeting both desire (the brain) '
            'and performance (the body).</p><ul>%s</ul></div></div>'
            % (ICON['tick'], readback, helps)
            + '<p class="sub lead" style="margin-top:var(--gap-block)">'
              'Let&rsquo;s proceed to check your eligibility.</p>'
            + '<div class="fields">%s%s</div>'
              % (field_block(dict(m['first_name'], half=True), 'First Name'),
                 field_block(dict(m['last_name'], half=True), 'Last Name'))
            + field_block(m['state'], 'What state will your medication be shipped to?')
            + '<p class="foot">Your information is never shared and is protected '
              'by HIPAA.</p>'
            + cta() + '</div>')


def screen_submission(p):
    m = {f['name']: f for f in p['fields']}
    return ('<div class="col">'
            + head('<span data-name-echo>How</span> can you be reached if necessary?',
                   'Our medical team and pharmacy use email and text for patient '
                   'communication.')
            + '<div class="fields">%s%s</div>'
              % (field_block(dict(m['email'], input_type='email'), 'Email'),
                 field_block(dict(m['phone_number'], input_type='tel',
                                  placeholder='(555) 123-4567', us_phone=True),
                             'Phone Number'))
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
                + head('How <span class="hl">BRAEVON&rsquo;s 4-in-1</span> Works for you',
                       'BRAEVON&rsquo;s 4-in-1 is engineered to hit both Desire (the brain) '
                       'and Performance (the body) in one dose.', lead=True)
                + '<div class="reviewcard">%s</div>' % rows
                + cta(blocked=False) + '</div>')
    if n == 8:
        clock = _ic('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>')
        bolt = _ic('<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>')
        peak = _ic('<path d="M4 17l5-5 4 4 7-7"/><path d="M14 9h6v6"/>')
        brain = _ic('<path d="M12 6a3.2 3.2 0 0 0-6-1.1A2.7 2.7 0 0 0 4.2 9.4 2.8 2.8 0 0 0 6 14.4'
                    'a3 3 0 0 0 3 2.6"/><path d="M12 6a3.2 3.2 0 0 1 6-1.1 2.7 2.7 0 0 1 1.8 4.5'
                    'A2.8 2.8 0 0 1 18 14.4a3 3 0 0 1-3 2.6"/><path d="M12 6v15"/>')

        # The reference's own axis: four marks on one line, spaced the way it
        # spaces them - 10m and 15m crowded at the left, 36hr hard against the
        # right end. It is not a linear scale and is not drawn as one.
        def axis():
            marks = [('10M', 4), ('15M', 19), ('4HR', 48), ('36HR', 99)]
            return ('<div class="axis"><span class="axis-ic">%s</span>'
                    '<div class="axis-line">%s</div></div>'
                    % (clock, ''.join('<i style="left:%d%%"><b>%s</b></i>' % (x, t)
                                      for t, x in marks)))

        # Brand, what it is fast at, the molecule that does it, and where the
        # bar sits on that axis. The three single-ingredient hues are the
        # reference's, and carry the same meaning its mechanism icons do.
        rows = [('Levitra&reg;', 'Rapid Onset', 'Vardenafil', '#12B76A', 22, 27),
                ('Viagra&reg;', 'Peak Strength', 'Sildenafil', '#3B82F6', 35, 15),
                ('Cialis&reg;', 'Extended Window', 'Tadalafil', '#8B5CF6', 34, 66),
                ('Other Stacks', 'Standard Combo',
                 'Sildenafil, Tadalafil, Apomorphine', '#D5D9E2', 27, 73)]
        rail = ''.join(
            '<div class="advrow"><div class="advrow-t">'
            '<b>%s <span>(%s)</span></b><span class="advrow-m">%s</span></div>'
            '<div class="track"><i style="left:%d%%;width:%d%%;background:%s"></i></div>'
            '</div>' % (a, b, mol, x, w, col)
            for a, b, mol, col, x, w in rows)

        chip = '<span class="chip">%s%s</span>'
        return ('<div class="col">'
                + head('You deserve a solution <span class="hl">that starts in '
                       'minutes</span> and lasts as long as you need it to')
                + '<div class="reviewcard adv">'
                  '<p class="adv-h">THE 4-IN-1 ADVANTAGE</p>'
                  '<p class="adv-sub">See how the BRAEVON 4-in-1 stack compares to '
                  'single-ingredient pills.</p>'
                + axis() + rail
                # The brand block the comparison builds to. It is the one part
                # of this screen drawn in Braevon orange rather than the
                # reference's three molecule hues - it is Braevon's own claim.
                + '<div class="fullpot">'
                  '<div class="fp-head"><div class="fp-name"><b>BRAEVON 4-in-1</b>'
                  '<span>FULL POTENTIAL</span></div>'
                + (chip % (brain, 'Arousal + Performance'))
                + '</div>' + axis()
                + '<div class="track"><i class="grad" style="left:10%;width:90%"></i></div>'
                  '<div class="chips">'
                + (chip % (bolt, 'Starts at 10m')) + (chip % (peak, 'Peak Power'))
                + (chip % (clock, '36h Window'))
                + '</div><div class="fp-rule"></div>'
                  '<p class="fp-note">Contains Sildenafil, Tadalafil, Vardenafil '
                  'and Apomorphine, which primes the brain for desire.</p>'
                  '</div></div>'
                + cta(blocked=False) + '</div>')
    if n == 33:
        # The reference sets this exactly as its other fact screen - centred on
        # white, the product name, a gradient pill, the figure, the read-out.
        # It is not a dark card; there is only one dark surface in the flow and
        # it is the stop.
        return ('<div class="col fact solo">'
                '<p class="fact-name">BRAEVON 4-in-1</p>'
                '<p class="fact-pill">Do It For Her</p>'
                '<p class="fact-k accent">137%</p>'
                '<p class="fact-u">improvement in sex<br/>for partner</p>'
                + cta(blocked=False) + '</div>')
    # The reference's testimonial: a photo carrying five stars and the quote in
    # white, two cards under it, then the person on a row of their own - all
    # inside one tinted panel.
    quote, meta, who, photo, face = QUOTES[n]
    stars = ''.join('<i>%s</i>' % ICON['star'] for _ in range(5))
    cards = ''.join(
        '<div class="qcard"><b>%s</b><div class="qbubs">%s</div><p>%s</p></div>'
        % (title, ''.join('<span class="bubble" style="--bub:%s;--gly:%s">%s</span>'
                          % art for art in arts), body)
        for title, arts, body in meta)
    return ('<div class="col"><div class="quotepanel">'
            '<figure class="qshot"><img src="assets/images/%s" alt=""/>'
            '<figcaption><span class="qstars">%s</span>'
            '<blockquote>%s</blockquote></figcaption></figure>'
            '<div class="qcards">%s</div>'
            '<div class="qwho">%s%s</div>'
            '</div>' % (photo, stars, quote, cards,
                        ('<img class="qavatar" src="assets/images/%s" alt="" '
                         'style="object-position:%s"/>' % face)
                        if face else
                        ('<span class="qavatar">%s</span>' % ICON['person']),
                        who)
            + cta(blocked=False) + '</div>')


def render(p):
    n = p['n']
    if n == 1:
        return screen_hero(p)
    return screen_v1(p)


def dq_reason(p):
    """v1 writes its own reason on every screen that can stop the flow and the
    extraction carries it - "you selected a nitrate" and "a tight foreskin needs
    to be looked at in person" are not the same message. The reference's
    per-screen copy, which this function used to hold, went with its questions.

    **These rules have never had a prescriber's sign-off.** They are v1's, and
    v1's own notes say the same of them: the nitrate interaction on screen 17 is
    a well-established contraindication, the rest are judgement calls. README.
    """
    return p['dq_reason'] or (
        'Your safety is our priority. Based on your answer, our clinicians '
        'cannot safely determine your eligibility.')


# ------------------------------------------------------------------ assemble
STEPS = list(FLOW)
QUESTIONS = [p for p in STEPS if p['options'] or p['fields']]
TOTAL_Q = len(QUESTIONS)


# The extractor reads each screen's stopping answers out of the DOM, and the
# reference keeps some of its rules in script the DOM does not expose. These
# are the ones observed on the live reference and added back by hand.
#
# Screen 3: the medication is male-only and the screen's own sub-head says so,
# so "Female" stops the flow rather than carrying on to questions that cannot
# apply. Confirmed against the reference's behaviour.
#
# NOT AUDITED: screens 31, 36 and 37 each carry an "I don't know" answer too,
# and the same reasoning would apply to them. They are left alone until
# someone confirms them against the reference - see the README.
# The reference kept some of its stopping rules in script the DOM did not
# expose, so two had to be added here by hand. v1 writes every one of its rules
# into `data-dq-on` and the extraction reads them all, so there is nothing left
# to add back.
DQ_EXTRA = {}


def dq_on(p):
    return list(p['dq_on']) + [v for v in DQ_EXTRA.get(p['n'], [])
                               if v not in p['dq_on']]


def sections():
    out, q = [], 0
    for p in STEPS:
        a = ' data-step="%d"' % p['n']
        if p in QUESTIONS:
            q += 1
            a += ' data-q="%d"' % q
        if p['n'] == 1:
            a += ' data-no-back'
        if p['n'] == BARE_SCREEN:
            a += ' data-bare'
        if p['cond']:
            a += (' data-if="%s" data-if-any="%s"'
                  % (attr(p['cond']['group']), attr('|'.join(p['cond']['any']))))
        # A screen can stop the flow two ways and v1 uses both. Named answers
        # go in `data-dq-on`; a screen with a reason and NO named answers stops
        # on **anything except its "none of these"**, which is how v1 writes the
        # nitrate screen - there every answer is a contraindication. Emitting
        # the reason only when there were named values silently disarmed that
        # screen, which is the one well-established interaction in the set.
        if p['dq_reason']:
            a += ' data-dq="%s"' % attr(dq_reason(p))
            stop = dq_on(p)
            if stop:
                a += ' data-dq-on="%s"' % attr('|'.join(stop))
            elif p['exclusive']:
                a += ' data-dq-safe="%s"' % attr(p['exclusive'])
        out.append('<section class="step"%s>%s</section>' % (a, render(p)))
    out.append(checkout_section())
    return out


def checkout_section():
    """The approval / checkout page as the flow's last step.

    It carries no `data-q`, so it takes no progress segment and no question
    number - the same as every screen after the last question. `data-bare` hides
    the shell's masthead and progress row; the page prints a centred wordmark
    and a countdown bar of its own instead, as the reference does."""
    return ('<section class="step" data-step="%d" data-bare data-checkout>%s</section>'
            % (CHECKOUT_SCREEN,
               checkout.screen(LOGO, ICON, _ic, STARS, MOLECULES,
                               GOAL_STYLE, attr)))


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
      '<div class="dq-inner">'
      '<div class="dq-card">'
      '<div class="dq-mark">%s</div>'
      '<h1 id="dqTitle">Eligibility Status</h1>'
      '<p>Based on your last answer, we cannot complete your assessment.</p>'
      # The screen's own reason, filled by `stop()` from its `data-dq`. It was
      # a fixed sentence until 2026-09-04 - the per-screen copy was being
      # computed and thrown away, so every stop read the same. v1 writes a real
      # reason on each of its six ("a tight foreskin needs to be looked at in
      # person", "you selected a nitrate") and they are worth showing. The
      # fallback below is what a screen with no reason of its own gets.
      '<p data-dq-reason>Your safety is our priority. This treatment has specific '
      'medical criteria, and your response prevents our clinicians from safely '
      'determining your eligibility.</p>'
      '</div>'
      '<p class="dq-lead">Made a mistake? Review your answer</p>'
      '<button class="dq-back" id="dqBack">Review Your Answer</button>'
      '<div class="dq-rule"></div>'
      '<p class="dq-lead soft">If your answer was correct, we cannot continue '
      'this assessment.</p>'
      '<button class="dq-ghost" id="dqExit">Exit Assessment</button>'
      '</div></div>' % ICON['shield'])

DONE = ('<div class="dq done" id="done" role="status">'
        '<div class="dq-inner">'
        '<div class="dq-card">'
        '<div class="dq-mark done-mark">%s</div>'
        '<h1>Assessment Received</h1>'
        '<p>Thank you. Your answers are with our clinical team.</p>'
        '<p>A licensed clinician reviews every assessment before anything is '
        'prescribed or shipped. We will email you as soon as they have.</p>'
        '</div></div></div>' % ICON['tick'])

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
            + DQ + DONE + '</div>'
            + '<script>%s</script>' % SCRIPT.replace('__TOTAL_Q__', str(TOTAL_Q))
                                            .replace('__SEGMENTS__', str(SEGMENTS))
                                            .replace('__SEGMENT_STARTS__',
                                                     json.dumps(SEGMENT_STARTS))
                                            .replace('__STEP_AT__',
                                                     json.dumps(STEP_AT)))
    html = page('Braevon &mdash; Intake Assessment v2', body)
    for name in ('index.html', 'interactive.html'):
        open(os.path.join(OUT, name), 'w', encoding='utf-8').write(html)


def static_progress(q, screen):
    """A frame carries no script, so its bar is drawn where that screen would
    have reached - otherwise every frame prints empty."""
    at = segment_of(STEP_AT.get(screen, 1))
    segs = ['<div class="seg%s"><span style="width:%d%%"></span></div>'
            % (' now' if k == at else '', 100 if k <= at else 0)
            for k in range(SEGMENTS)]
    return nav('<div class="progress" role="progressbar" aria-valuenow="%d">%s</div>'
               % (q, ''.join(segs)))


def emit_frames():
    frames, q = [], 0
    built = sections()
    checkout_html = built[-1]
    for p, html in zip(STEPS, built):
        counted = p in QUESTIONS
        if counted:
            q += 1
        lbl = 'Screen %02d &mdash; %s' % (p['n'], esc(p.get('label') or p['name']))
        inner = html.replace('<section class="step"', '<section class="step on"', 1)
        # ids are unique per document; 46 frames cannot each carry the
        # interactive build's element ids
        chrome = '' if p['n'] == BARE_SCREEN else (
            MASTHEAD + (static_progress(q, p['n']) if q else nav(''))
        ).replace(' id="backBtn"', '')
        if p['n'] == 1:
            chrome = chrome.replace('<button class="back-btn"', '<button class="back-btn" hidden')
        frames.append('<div class="frame-label">%s</div><div class="frame"><div class="shell">'
                      '%s<main class="stage">%s</main></div></div>' % (lbl, chrome, inner))
    # The checkout carries its own chrome, so it goes into a frame bare - the
    # same treatment BARE_SCREEN gets in the loop above.
    frames.append('<div class="frame-label">Screen %02d &mdash; Approval &amp; checkout</div>'
                  '<div class="frame"><div class="shell"><main class="stage">%s</main>'
                  '</div></div>'
                  % (CHECKOUT_SCREEN,
                     checkout_html.replace('<section class="step"',
                                           '<section class="step on"', 1)))
    frames.append('<div class="frame-label">Assessment received (after checkout)</div>'
                  '<div class="frame"><div class="shell">%s%s</div></div>'
                  % (MASTHEAD,
                     DONE.replace('class="dq done"', 'class="dq done on"')
                         .replace(' id="done"', '')))
    # Neither of these is a numbered screen - they are states the flow can enter
    # from several places - so they are labelled rather than numbered.
    frames.append('<div class="frame-label">Eligibility stop (any safety screen)</div>'
                  '<div class="frame"><div class="shell">%s%s</div></div>'
                  % (MASTHEAD,
                     DQ.replace('class="dq"', 'class="dq on"')
                       .replace(' id="dqBack"', '').replace(' id="dqExit"', '')
                       .replace(' id="dq"', '').replace(' id="dqTitle"', '')
                       .replace(' aria-labelledby="dqTitle"', '')))
    open(os.path.join(OUT, 'all-screens.html'), 'w', encoding='utf-8').write(
        page('Braevon &mdash; Intake v2, all screens', '\n'.join(frames), 'frames'))
    return len(frames)


def _check_defaults():
    for p in STEPS:
        v = DEFAULTS.get(p['n'])
        if v and v in dq_on(p):
            raise SystemExit('screen %d opens on a disqualifying answer: %r'
                             % (p['n'], v))


if __name__ == '__main__':
    _check_defaults()
    emit_interactive()
    n = emit_frames()
    print('index.html + interactive.html   %d screens, %d counted questions'
          % (len(STEPS), TOTAL_Q))
    print('all-screens.html                %d frames' % n)
