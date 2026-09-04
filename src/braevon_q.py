"""Braevon's own questions, laid over the reference's screens.

The reference's design, layout and spacing are untouched. This module only
replaces what a screen ASKS - its headline, its sub-head, its answers and its
follow-ups. Screen numbers (`n`) are deliberately left alone so that every
per-screen table in build.py (TILE_SCREENS, BAND_SCREENS, GROUPS, DEFAULTS,
SCREEN_IMAGE, the conditionals) keeps pointing at the screen it was written
for. `medvi-flow.json` stays as extracted; this is applied on top of it.

Source: "Braevon Intake v2 - All Prototype Questions (for Design)", 10 August
2026. `doc=` on each screen is that document's own screen number, so any entry
here can be checked against it line by line.

Asked for on 2026-09-04. The client's mapping, in their own numbering of the
29-screen floor (the unconditional path plus the checkout):

    keep    1 2 3 5 8 11 16 17 25 26 27 28 29
    change  4 6 7 9 10 12 13 14 15 18 19 20 21 22 23 24

Three decisions they made when asked:
  - floor 12 (this file's screen 27) changes rather than stays;
  - the document's screen 26, "other health concerns", is DROPPED - it is the
    only question in the document that is not clinical screening, and the floor
    was to stay at 29 screens;
  - floor 24 (screen 42) takes the document's wording.

ONE PIECE OF COPY HERE IS NOT THE CLIENT'S. Screen 28 merges the document's
screens 20 and 21 (penile curve, tight foreskin) into the one slot the floor
allows, and a merged screen needs a headline neither of them has. Rather than
write one, it keeps the headline already on that screen. Flagged in the README.

NOT REVIEWED BY A PRESCRIBER. The `dq` lists below are transcribed from the
document's own NOTE lines and nothing more - see the README's standing warning
about the disqualification rules.
"""

# --------------------------------------------------------------- helpers

def _opt(value, label=None, note=None, kind='checkbox'):
    o = {'value': value, 'label': label if label is not None else value,
         'type': kind, 'name': None}
    if note:
        o['note'] = note
    return o


def _radio(value, label=None, note=None):
    return _opt(value, label, note, kind='radio')


def _text(on, label, name, placeholder='Write here...', sub=None):
    """A free-text follow-up that opens on `on`.

    `on` is an answer's value, or '*' for "anything but the none-answer".
    Optional, exactly as the reference's own follow-ups are: it opens, it can
    be typed into, and it does not gate Next."""
    r = {'kind': 'text', 'on': on, 'label': label, 'name': name,
         'placeholder': placeholder, 'optional': True}
    if sub:
        r['sub'] = sub
    return r


def _yesno(on, label, name, dq=False):
    """A yes/no follow-up that opens on `on`.

    Required once open - it is asked precisely because the answer decides
    eligibility. When `dq` is set, Yes stops the flow, and the value is added
    to the screen's stopping answers so the engine's existing check catches it
    with no new machinery."""
    return {'kind': 'yesno', 'on': on, 'label': label, 'name': name, 'dq': dq}


# --------------------------------------------------------------- overrides
#
# Every entry replaces title / subs / options / mode / reveals / dq on one
# screen. `group` is deliberately NOT changed: the medical review echoes three
# groups back to the patient and the conditional screens gate on two more, so
# renaming them would break both for no gain.

OVERRIDES = {

    # ---------------------------------------------------------- floor 4
    4: dict(doc=7, name='Erection confidence - 03', mode='single',
            title='How confident are you in getting or keeping an erection?',
            subs=[],
            options=[_radio('Not confident'),
                     _radio('Low confident'),
                     _radio('Somehow confident'),
                     _radio('Mostly confident'),
                     _radio('Very confident',
                            note='This answer will disqualify you from medication')],
            # doc: "The last option routes the patient to the Disqualify screen."
            dq=['Very confident'],
            exclusive=None),

    # ---------------------------------------------------------- floor 6
    # The document has no duration question, so the screen that asked one now
    # carries the performance-factors question. The medical review's third
    # read-back row follows it - see build.py's screen_review.
    6: dict(doc=9, name='Performance factors - 03', mode='multi',
            title='Is your sexual performance affected by any of the following?',
            subs=[],
            options=[_opt('A feeling of nervousness or anxiety before and/or during sex'),
                     _opt('Concern about your sexual performance'),
                     _opt('Concern about your body image'),
                     _opt('Concern about sexual dysfunction conditions you may have'),
                     _opt('Relationship problems'),
                     _opt('None of these')],
            dq=[], exclusive='None of these'),

    # ---------------------------------------------------------- floor 7
    7: dict(doc=8, name='Erections - 04', mode='multi',
            title='Do you get erections?',
            subs=[],
            options=[_opt('When you wake up'),
                     _opt('Other times'),
                     _opt('Neither')],
            # doc: "'Neither' is exclusive - selecting it clears the other two."
            dq=[], exclusive='Neither'),

    # ---------------------------------------------------------- floor 9
    # Was the reference's six-drug picker, which fanned out into thirteen
    # follow-up screens. The document asks one Yes/No instead and hangs two
    # screens off it, so eleven of those thirteen are dropped (see DROP) and
    # the remaining two are rewritten below.
    9: dict(doc=10, name='ED medication history - 5', mode='single',
            title='Have you ever taken ED medications?',
            subs=['Your History'],
            options=[_radio('no', 'No'), _radio('yes', 'Yes')],
            dq=[], exclusive=None,
            reveals=[_text('yes',
                           'Please provide any details related to the treatment, '
                           'dosage and effectiveness',
                           'Q_ed_history_detail',
                           'e.g., Viagra 50mg for 3 months - worked, but inconsistent')]),

    # ------------------------------------------- conditional, behind floor 9
    10: dict(doc=11, mode='single',
             name='ED side effects - 5.a',
             title='Did you experience any side effects from your treatments for ED?',
             subs=[],
             options=[_radio('no', 'No, never had any side effects'),
                      _radio('yes', 'Yes')],
             # doc: "No answer here disqualifies the patient."
             dq=[], exclusive=None,
             cond={'group': 'Q6_ed_treatments_tried', 'any': ['yes']},
             reveals=[_text('yes', 'Please explain any side effects you experienced.',
                            'Q_ed_side_effects_detail')]),

    # ------------------------------------------- conditional, behind floor 9
    # Free text and nothing else, which is the shape this screen already had.
    22: dict(doc=12, mode=None,
             name='ED last use - 5.b',
             title='How long ago was your last use of this medication?',
             subs=[], options=[], dq=[], exclusive=None,
             cond={'group': 'Q6_ed_treatments_tried', 'any': ['yes']},
             fields=[{'tag': 'textarea', 'name': 'Q_ed_last_use',
                      'input_type': None,
                      'placeholder': 'e.g., about 6 months ago'}]),

    # ---------------------------------------------------------- floor 10
    23: dict(doc=13, name='Physical exam - 06', mode='single',
             title='Have you had a physical exam with a healthcare provider '
                   'in the past 5 years?',
             subs=['Your History'],
             options=[_radio('yes_normal', 'Yes, it was normal'),
                      _radio('yes_issues', 'Yes, but there were issues'),
                      _radio('no', 'No')],
             # doc: "No answer here disqualifies the patient." The reference
             # stopped the flow here; the document does not.
             dq=[], exclusive=None,
             reveals=[_text('yes_issues',
                            'Please explain any issues during your last physical exam',
                            'Q_physical_exam_detail')]),

    # ---------------------------------------------------------- floor 12
    27: dict(doc=22, name='Conditions - 08', mode='multi',
             title='Do you have now, or have you ever had any of the '
                   'following conditions?',
             subs=['Select all that apply.'],
             options=[_opt('Priapism (erection lasting longer than 4 hours)'),
                      _opt('Retinitis Pigmentosa'),
                      _opt('Sudden vision loss'),
                      _opt('Neurologic disease or stroke'),
                      _opt('Blood clotting disorder, abnormal bleeding or bruising'),
                      _opt('Stomach or intestinal ulcer'),
                      _opt('A prior heart attack or heart failure'),
                      _opt('Peripheral artery disease'),
                      _opt('Any history of QT prolongation'),
                      _opt('Sickle cell anemia, Myeloma, Leukemia'),
                      _opt('Idiopathic Hypertrophic Subaortic Stenosis'),
                      _opt('Use of blood thinners'),
                      _opt('None of these')],
             # doc: nothing in the list itself disqualifies - the two dated
             # follow-ups do.
             dq=[], exclusive='None of these',
             reveals=[
                 _yesno('A prior heart attack or heart failure',
                        'Have you had a heart attack within the last three months?',
                        'Q_heart_attack_recent', dq=True),
                 _yesno('Neurologic disease or stroke',
                        'Have you had a stroke within the last six months?',
                        'Q_stroke_recent', dq=True),
                 _text('*', 'Please tell us more about your conditions you selected.',
                       'Q_conditions_detail'),
             ]),

    # ---------------------------------------------------------- floor 13
    # The document's screens 20 and 21 in the one slot the floor allows. The
    # headline is this screen's existing one - see the note at the top of this
    # file - because a merged screen has no headline of its own in the source.
    28: dict(doc='20+21', name='Curve & foreskin - 09', mode='multi',
             title='Thank you. Now, please check any of the following that apply.',
             subs=['Select all that apply.'],
             options=[_opt('A curve or bend in the penis that interferes with sex, '
                           "or Peyronie's disease"),
                      _opt('A tight foreskin',
                           note='This answer will disqualify you from medication'),
                      _opt('None of these')],
             # doc screen 21: "'Yes' routes the patient to the Disqualify
             # screen." doc screen 20: the main answer alone does NOT.
             dq=['A tight foreskin'], exclusive='None of these',
             reveals=[
                 _yesno('A curve or bend in the penis that interferes with sex, '
                        "or Peyronie's disease",
                        'Have you had active bending of your penis within '
                        'the last 12 months?',
                        'Q_curve_active', dq=True),
                 _yesno('A curve or bend in the penis that interferes with sex, '
                        "or Peyronie's disease",
                        'Do you experience pain with erections or with ejaculation?',
                        'Q_curve_pain', dq=True),
             ]),

    # ---------------------------------------------------------- floor 14
    29: dict(doc=19, name='Diagnoses - 10', mode='multi',
             title='Have you ever been diagnosed with any of the following?',
             subs=['Select all that apply.'],
             options=[_opt('Prostate cancer'),
                      _opt('Enlarged prostate (BPH)'),
                      _opt('Kidney transplant or any condition affecting the kidney'),
                      _opt('Pulmonary artery hypertension (PAH)'),
                      _opt('Liver disease'),
                      _opt('Multiple Sclerosis (MS) or a similar disease'),
                      _opt('Spinal injuries and/or paralysis'),
                      _opt('Neurological diseases'),
                      _opt('Stomach, intestinal, or bowel ulcers'),
                      _opt('Heart arrhythmias',
                           note='abnormal beating of the heart'),
                      _opt('Heart abnormalities including heart murmurs',
                           note='acquired, congenital, or developmental'),
                      _opt('None of these apply to me')],
             # doc: "Nothing here disqualifies the patient."
             dq=[], exclusive='None of these apply to me',
             reveals=[_text('*', 'Please tell us more about the diagnoses you '
                                 'selected (diagnosis and treatment).',
                            'Q_diagnoses_detail')]),

    # ---------------------------------------------------------- floor 15
    # The reference sent diabetes off to a screen of its own; the document asks
    # it inline, so that screen is dropped and this one gains three follow-ups.
    30: dict(doc=24, name='Cardiovascular risk - 11', mode='multi',
             title='Do you have any of the following cardiovascular risk factors?',
             subs=['Please check all that apply.'],
             options=[_opt('High cholesterol'),
                      _opt('High blood pressure'),
                      _opt('Diabetes, pre-diabetes, or glucose intolerance'),
                      _opt('Father had heart attack/disease (before age 55)'),
                      _opt('Mother had heart attack/disease (before age 65)'),
                      _opt('None of these apply to me')],
             # doc: "No answer here disqualifies the patient, including an
             # unknown A1c."
             dq=[], exclusive='None of these apply to me',
             reveals=[
                 _text('Diabetes, pre-diabetes, or glucose intolerance',
                       'Tell us more about your diabetes.', 'Q_diabetes_detail',
                       sub='When was your last Hemoglobin A1c checked and '
                           'what was the value?'),
                 _text('High cholesterol', 'Tell us more about your high cholesterol',
                       'Q_cholesterol_detail'),
                 _text('High blood pressure',
                       'Tell us more about your high blood pressure',
                       'Q_bp_detail'),
             ]),

    # ---------------------------------------------------------- floor 18
    34: dict(doc=23, name='Cardiovascular symptoms - 12', mode='multi',
             title='Do you experience any of the following cardiovascular symptoms?',
             subs=[],
             options=[_opt('Chest pain or shortness of breath when climbing 2 '
                           'flights of stairs or walking 4 blocks'),
                      _opt('Chest pain or shortness of breath with sexual activity'),
                      _opt('Unexplained fainting or dizziness'),
                      _opt('Prolonged cramping of the legs with exercise'),
                      _opt('Abnormal heart beats or rhythms'),
                      _opt('None of these apply to me')],
             # doc: "No answer here disqualifies the patient."
             dq=[], exclusive='None of these apply to me',
             reveals=[_text('Prolonged cramping of the legs with exercise',
                            'Please tell us more about your prolonged leg cramps.',
                            'Q_leg_cramps_detail')]),

    # ---------------------------------------------------------- floor 19
    # The reference hung two follow-up screens off nitroglycerin and alpha
    # blockers. The document stops the flow on any of the five instead, so
    # both are dropped (see DROP).
    35: dict(doc=17, name='Medicines - 13', mode='multi',
             title='Do you take any of the following medicines?',
             subs=['Select all that apply.'],
             options=[_opt('Nitroglycerin spray, ointment, patches or tablets'),
                      _opt('Isosorbide mononitrate, or isosorbide dinitrate',
                           note='Isordil, Dilatrate, Sorbitrate, Imdur, Ismo, Monoket'),
                      _opt('Other medicines containing nitrates'),
                      _opt('Alpha blocker medications',
                           note='doxazosin (Cardura), prazosin (Minipress), '
                                'terazosin (Hytrin)'),
                      _opt('Riociguat (Adempas)'),
                      _opt('None of these')],
             # doc: "Selecting ANY of the five medicines routes the patient to
             # the Disqualify screen."
             dq=['Nitroglycerin spray, ointment, patches or tablets',
                 'Isosorbide mononitrate, or isosorbide dinitrate',
                 'Other medicines containing nitrates',
                 'Alpha blocker medications',
                 'Riociguat (Adempas)'],
             exclusive='None of these'),

    # ---------------------------------------------------------- floor 20
    38: dict(doc=18, name='Recreational drugs - 14', mode='multi',
             title='Do you use any of the following recreational drugs?',
             subs=['Medical Info'],
             options=[_opt('Cocaine'),
                      _opt('Poppers/Rush (amyl/butyl nitrate)'),
                      _opt('Methamphetamines'),
                      _opt('Cigarettes'),
                      _opt('Other'),
                      _opt('None of these')],
             # doc: "Nothing here disqualifies the patient - any selection gets
             # the follow-up and the doctor reviews it." The reference stopped
             # the flow here; the document does not.
             dq=[], exclusive='None of these',
             reveals=[_text('*', 'Please explain your use of the drugs you selected.',
                            'Q_recreational_detail',
                            sub='How frequently do you use them? When was the '
                                'last time you used them?')]),

    # ---------------------------------------------------------- floor 21
    39: dict(doc=14, name='Conditions & surgeries - 15', mode='single',
             title='Do you have any medical conditions or a history of '
                   'prior surgeries?',
             subs=['Medical Info'],
             options=[_radio('no', 'No'), _radio('yes', 'Yes')],
             dq=[], exclusive=None,
             reveals=[_text('yes',
                            'Please briefly describe your condition(s) or '
                            'surgery history:',
                            'Q_conditions_surgeries_detail',
                            'e.g. High blood pressure, knee surgery in 2019...')]),

    # ---------------------------------------------------------- floor 22
    40: dict(doc=16, name='Allergies - 16', mode='single',
             title='Do you have any allergies?',
             subs=['Medical Info'],
             options=[_radio('no', 'No'), _radio('yes', 'Yes')],
             dq=[], exclusive=None,
             reveals=[_text('yes',
                            'Please list any known allergies (medications, '
                            'foods, or other):',
                            'Q_allergies_detail',
                            'e.g. Penicillin, sulfa drugs, shellfish...')]),

    # ---------------------------------------------------------- floor 23
    # The screen that carries the photograph.
    41: dict(doc=15, name='Current medications - 17', mode='single',
             title='Are you currently taking any medications, vitamins or '
                   'dietary supplements?',
             subs=['Medical Info'],
             options=[_radio('no', "No, I don't take anything"),
                      _radio('yes', 'Yes')],
             dq=[], exclusive=None,
             reveals=[_text('yes',
                            'Please list your current medications, vitamins, '
                            'or supplements:',
                            'Q_medication_detail',
                            'e.g. Lisinopril 10mg, Fish oil, Vitamin D...')]),

    # ---------------------------------------------------------- floor 24
    42: dict(doc=27, name='Doctor notes - 18', mode='single',
             title='Is there anything else you want your doctor to know about '
                   'your condition or health?',
             subs=['Additional Info'],
             options=[_radio('no', 'No'), _radio('yes', 'Yes')],
             dq=[], exclusive=None,
             reveals=[_text('yes',
                            "Please share anything you'd like your doctor to know:",
                            'Q_doctor_note_detail')]),
}


# Screens the document has no question for, all of them conditional.
#
#   11-21  the reference's per-drug follow-ups ("How well did Viagra work for
#          you?" and its five siblings, twice over). The document asks one
#          Yes/No on screen 10 and hangs two screens off it instead, which is
#          what 10 and 22 now are.
#   31     the A1C screen behind diabetes - the document asks it inline on the
#          cardiovascular risk screen.
#   36,37  the nitroglycerin and alpha-blocker follow-ups - the document stops
#          the flow on those answers rather than asking more.
#
# Nothing unconditional is dropped, so the floor stays at 29 screens.
DROP = set(range(11, 22)) | {31, 36, 37}


def apply(flow):
    """Return `flow` with Braevon's questions in place of the reference's."""
    out = []
    for p in flow:
        if p['n'] in DROP:
            continue
        o = OVERRIDES.get(p['n'])
        if not o:
            out.append(p)
            continue
        p = dict(p)
        group = p['group']
        for opt in o['options']:
            opt = dict(opt)
        # Options carry the screen's group as their control name, the way the
        # extraction does.
        p['options'] = [dict(x, name=group) for x in o['options']]
        p['title'] = o['title']
        p['subs'] = list(o['subs'])
        p['mode'] = o['mode']
        p['exclusive'] = o['exclusive']
        p['dq_on'] = list(o['dq'])
        if 'name' in o:
            p['name'] = o['name']
        if 'cond' in o:
            p['cond'] = o['cond']
        if 'fields' in o:
            p['fields'] = list(o['fields'])
        # A yes/no follow-up that stops the flow puts its Yes on the screen's
        # own stopping list, so the engine's existing check catches it without
        # any new machinery.
        for r in o.get('reveals', []):
            if r['kind'] == 'yesno' and r.get('dq'):
                p['dq_on'] = p['dq_on'] + [r['name'] + '_yes']
        out.append(p)
    return out


def reveals():
    """{screen: [reveal, ...]} for every screen that has follow-ups."""
    return {n: o['reveals'] for n, o in OVERRIDES.items() if o.get('reveals')}


def groups(base):
    """GROUPS with our screens re-recorded.

    Everything in this file follows the document's own convention: the
    none-answer sits LAST, under a rule, with no note and no section captions.
    The reference's arrangement - green and first, under a line saying it is
    the only answer that lets you continue - was recorded per screen and no
    longer describes these lists."""
    out = dict(base)
    for n in OVERRIDES:
        out[str(n)] = {'exclusive_first': False, 'exclusive_note': None,
                       'captions': {}}
    return out
