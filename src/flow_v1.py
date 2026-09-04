# -*- coding: utf-8 -*-
"""Braevon's own question set, shaped for v2's renderer.

**This is the flow from 2026-09-04.** v2 was built against the MEDVi QUAD
reference's 40 questions; the client asked for those to be replaced with
Braevon's own - v1's 24 - keeping v2's design, layout and every component. So
the questions and their options change and nothing else does.

Two rules the client stated twice, and both are enforced here rather than left
to a reviewer's eye:

1. **Only screens that ask something.** v1 has 34 screens; ten are marketing,
   consent, processing, approval or checkout pages with no question on them, and
   `marketing` is true on every one of those. They are dropped, so the flow is
   24 screens, all of them questions. `_check()` at the foot of this file fails
   the build if a screen without a question ever gets through.
2. **The reference's own extra screens go too.** v2's hero interstitials, its
   "LAST STEP" birth-date screen, its medical review and its submission screen
   were MEDVi's, not Braevon's. None of them is in this flow. v1's screen 4 asks
   for the date of birth as part of eligibility, and its screen 28 collects name,
   email and phone; those are the Braevon equivalents and they are questions, so
   they stay.

The questions are **parsed, never retyped**: `extract_v1.py` reads them out of a
v1 build into `questions.json` and this module reshapes that into the record
`build.py` renders. Verified on 2026-09-04 against the live v1 at
`braevon-intake-form-updates.vercel.app` - all 24 question screens came back
byte-identical to the copy already in the repo.

What this module does NOT do is invent anything. Where v2 had a table of
per-screen decoration keyed to MEDVi screen numbers - photographs, molecule
lists, accented phrases, footnotes - those keys do not exist in this flow and
the tables are empty rather than re-guessed onto Braevon's screens.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = json.load(open(os.path.join(HERE, 'questions.json'), encoding='utf-8'))


def _blocks(p, kind):
    return [b for b in p['blocks'] if b['t'] == kind]


def _first(p, kind, key='text'):
    b = _blocks(p, kind)
    return b[0].get(key) if b else None


def _exclusive(block):
    """v1 marks its "none of these" answer with `data-exclusive`."""
    for o in block['options']:
        if o.get('exclusive'):
            return o['value']
    return None


def _option(o, mode, group):
    """v2's `option()` reads `type` to decide between a radio ring and a
    checkbox, and the reference's extractor writes it on every option."""
    out = {'value': o['value'], 'label': o['label'],
           'type': 'checkbox' if mode == 'multi' else 'radio',
           'name': group}
    for k in ('note', 'sub'):
        if o.get(k):
            out[k] = o[k]
    if o.get('preselected'):
        out['preselected'] = True
    return out


def _field(f):
    """v1's field record into v2's. `id` becomes `name` because that is what
    `field_block()` writes into the control's id, and the engine looks controls
    up by it - `#first_name`, `#state` and the checkout's echoes all depend on
    the ids staying exactly as v1 wrote them."""
    out = {'tag': f['tag'], 'name': f['id'],
           'input_type': f.get('input_type'),
           'placeholder': f.get('placeholder'),
           'half': bool(f.get('half')),
           'dob': bool(f.get('dob')),
           'label': f.get('label')}
    if f.get('options'):
        out['options'] = f['options']
    # The phone box takes v2's US formatter - the same rule v1 validated with.
    if f['id'] == 'phone':
        out['us_phone'] = True
    return out


def _convert(p):
    opts = _blocks(p, 'options')
    # The screen's primary group is its first option list. Screen 25 carries a
    # second, optional one ("No, I will get a new reading") which is not the
    # question - it is an opt-out under the answer - so it is rendered from
    # `blocks` and is not the screen's group.
    main = opts[0] if opts else None
    subs = [b['text'] for b in _blocks(p, 'sub')]
    cond = None
    if p['cond']:
        g, v = p['cond'].split(':', 1)
        cond = {'group': g, 'any': [v]}
    dq_on = []
    if p['dq_on']:
        # "sex:female" / "curve-recent:yes,curve-pain:yes" - v2 matches on the
        # value alone, and each of these values is unique within its screen.
        dq_on = [pair.split(':', 1)[1] for pair in p['dq_on'].split(',')]
    return {
        'n': p['step'],
        # `step_of()` in build.py reads the trailing number out of this, which
        # is what drives the progress bar's five segments.
        'name': 'Q%d - %02d' % (p['q'], p['step']),
        # What the Figma import calls the frame. `name` carries the trailing
        # step number `step_of()` parses, which reads badly beside the frame's
        # own "Screen 04 —", so the label is separate.
        'label': 'Question %d of %d' % (p['q'], len(RAW_Q)),
        'q': p['q'],
        'title': _first(p, 'title') or '',
        'subs': subs,
        'eyebrow': _first(p, 'eyebrow'),
        'options': [_option(o, main['mode'], main['group'])
                    for o in main['options']] if main else [],
        'fields': [_field(f) for f in _blocks(p, 'field')],
        'group': main['group'] if main else None,
        'mode': main['mode'] if main else None,
        'cond': cond,
        'exclusive': _exclusive(main) if main else None,
        'dq_on': dq_on,
        'dq_kind': None,
        'dq_reason': p['dq'],
        # The whole screen in document order, for the renderer to walk: v1
        # interleaves legends, notes, a second option list and its reveals
        # between the title and the fields, and the flat record above cannot
        # express that ordering.
        'blocks': p['blocks'],
    }


RAW_Q = [p for p in RAW if not p['marketing'] and p['q']]
FLOW = [_convert(p) for p in RAW_Q]

# ---------------------------------------------------------------- sections
# The five progress segments, as **step numbers**, following v1's own eyebrows:
# its goals screen, its eligibility screen, the history block, the medical block
# and the closing three. Uneven by design - the reference's five are uneven too,
# and these are where the questionnaire actually changes subject.
SEGMENT_STARTS = [1, 4, 7, 14, 26]

# ---------------------------------------------------- per-screen treatment
# v1's two-up control - the sex question's Male / Female cards. The extractor
# records it as `style: tiles`, so this is read off the data rather than listed.
TILE_SCREENS = {p['n'] for p in FLOW
                for b in p['blocks']
                if b['t'] == 'options' and b.get('style') == 'tiles'}

# The blood-pressure bands, which v2 draws as a coloured droplet per band. Same
# again - `grouped` is v1's own marker for that list.
BAND_SCREENS = {p['n'] for p in FLOW
                for b in p['blocks']
                if b['t'] == 'options' and b.get('grouped')}

# v1 hoists the "none of these" answer to the top of every list that has one and
# rules it off from the rest, so a patient with none of fourteen conditions does
# not have to read all fourteen to find that out. v2 draws that position as a
# green "safe" card, which is the same intent in v2's language.
EXCLUSIVE_FIRST = {p['n'] for p in FLOW if p['exclusive']}


def _check():
    seen = set()
    for p in FLOW:
        if not (p['options'] or p['fields']):
            raise SystemExit('screen %d asks nothing - it should not be in the '
                             'flow (see this module\'s docstring)' % p['n'])
        if p['n'] in seen:
            raise SystemExit('duplicate screen %d' % p['n'])
        seen.add(p['n'])
    qs = [p['q'] for p in FLOW]
    if qs != list(range(1, len(qs) + 1)):
        raise SystemExit('question numbers are not 1..N: %r' % qs)
    for start in SEGMENT_STARTS:
        if start not in seen:
            raise SystemExit('segment starts at screen %d, which is not in the '
                             'flow' % start)


_check()

if __name__ == '__main__':
    print('%d screens, all questions' % len(FLOW))
    for p in FLOW:
        print(' %2d  Q%-2d  %-46s opts %-3d fields %d'
              % (p['n'], p['q'], p['title'][:46], len(p['options']),
                 len(p['fields'])))
