# -*- coding: utf-8 -*-
"""Screen 50 — informed consent.

Added on 2026-09-08 at the client's word, and it closes the compliance gap the
README has carried since the flow was built: the client's own document has an
informed-consent step (its screen 30), v1 shipped one, and v2 had none because
**the reference has no consent screen to lay it over**. It is not in
`medvi-flow.json` for the same reason the checkout is not - the extractor walks
`/intake-s`, and nothing on that page corresponds to this. So it is numbered
outside the extracted range, after the checkout (48) and the received page (49),
and inserted into the flow by position rather than by number.

**The copy is v1's, verbatim, and v1's is `Consent box.pdf` (2026-08-17)
verbatim** - including the file's own instruction about what shows before the
document is opened. It marks "What this medication does" as the default-visible
block and puts everything else behind "Read full Consent". That split is
`CS_LEAD` against `CS_MORE` + `CS_DOC` here, exactly as it was in v1.

Carried across with it, because they are still true here:

**The contraindications sit behind a tap, and that is worth a second opinion.**
"Do not use if you take nitrates" is the line on this screen that stops someone
being harmed, and the client's own earlier mock had it visible. Built as the
document asks; raised with them rather than quietly overridden. Moving an entry
from `CS_MORE` to `CS_LEAD` is the whole change if they want it out in the open.

**`Possible side effects` and `Most common side effects` cover the same ground
twice**, one as the PDF's full list and one as a summary, and they read as a
repeat this close together. Worth merging if the client agrees.

What is NOT v1's is the dress. v1 built this from its own components on a grey
page with a sticky footer; here it is v2's: the eyebrow, `.reviewcard`, the
checkbox `.opts` box every other screen uses, `cta()`, and the CTA in normal
flow like every other screen in this build.

**The headline is v1's, and it is the reason screen 43 lost its pill.** v1 heads
this screen "One last step — your consent"; screen 43 carried the reference's
LAST STEP pill. With consent after the date of birth the pill was the false one
of the two, so on 2026-09-08 it came off 43 and the headline stayed here.
"""

# `CS_LEAD` shows before the document is opened, `CS_MORE` + `CS_DOC` after.
# The PDF put only the first block in `CS_LEAD`; the client asked on 2026-08-17
# for one more, so the benefits moved up. Moving another entry between these two
# lists is the whole change - nothing else reads them.
CS_LEAD = [
    ('What this medication does',
     'PDE5 inhibitors (the medication class in BRAEVON) increase blood flow to '
     'help you get and keep an erection.'),
    ('Potential benefits',
     'May improve your ability to achieve and maintain an erection, enhance '
     'sexual performance and satisfaction, and improve your quality of life and '
     'personal relationships.'),
]

CS_MORE = [
    ('Do not use if you',
     'Take nitrates for chest pain &middot; use &ldquo;poppers&rdquo; &middot; have '
     'severe heart or liver problems &middot; recently had a stroke or heart attack '
     '&middot; have low blood pressure.'),
    ('Good to know',
     'Alternatives exist (lifestyle changes, counseling, devices, other '
     'therapies). Treatment is voluntary &mdash; you can stop at any time.'),
]

# The document proper. The opening paragraph carries no heading in the PDF
# either - it is the diagnosis statement the rest hangs off.
CS_DOC_INTRO = (
    'You have been diagnosed with or have reported that you have a known '
    'diagnosis of organic or psychogenic (situational) erectile dysfunction, a '
    'condition characterized by the inability to achieve or maintain an erection '
    'sufficient for satisfactory sexual performance. Phosphodiesterase Type 5 '
    'Inhibitors (PDE5i) are medications prescribed to treat this condition by '
    'enhancing erectile function.')

CS_DOC = [
    ('Common PDE5 inhibitors',
     '<p>Sildenafil (Viagra), Tadalafil (Cialis), Vardenafil (Levitra), and '
     'Avanafil (Stendra). These medications work by increasing blood flow to the '
     'penis during sexual stimulation.</p>'),
    ('Possible side effects',
     '<ul>'
     '<li>Headache, flushing, indigestion or upset stomach</li>'
     '<li>Nasal congestion, dizziness or lightheadedness</li>'
     '<li>Visual disturbances such as blurred vision or changes in colour '
     'perception</li>'
     '<li>Back pain or muscle aches (more common with Tadalafil)</li>'
     '<li>Hearing loss or ringing in the ears (rare)</li>'
     '<li>Priapism (a prolonged erection lasting more than four hours)</li>'
     '<li>Allergic reactions like rash, itching, or swelling</li>'
     '</ul>'),
    ('Do not use PDE5 inhibitors if you',
     '<ul>'
     '<li>Take nitrates for chest pain (angina)</li>'
     '<li>Use recreational drugs called &ldquo;poppers&rdquo; (amyl nitrate or '
     'nitrite)</li>'
     '<li>Have severe heart or liver problems</li>'
     '<li>Have recently had a stroke or heart attack</li>'
     '<li>Have low blood pressure</li>'
     '</ul>'),
    ('Alternative treatments',
     '<p>Lifestyle changes such as exercise, weight loss, quitting smoking, and '
     'reducing alcohol intake; psychotherapy or counseling; vacuum erection '
     'devices; penile injections or suppositories; hormone therapy if low '
     'testosterone is contributing; and surgical options like penile implants or '
     'vascular surgery.</p>'),
    ('Most common side effects',
     '<p>Headache, flushing, upset stomach, stuffy nose, dizziness. Rare but '
     'serious: vision or hearing changes, an erection lasting over 4 hours '
     '(seek care immediately).</p>'),
]

# The PDF's closing paragraph. It stays in the document, as its last section -
# the client shortened the CHECKBOX on 2026-08-17, not the consent, so this text
# is still what the patient is agreeing to and still has to be on the screen to
# read.
CS_ATTEST = (
    'I understand the potential benefits, risks, and side effects of using PDE5 '
    'inhibitors. I have been informed about alternative treatment options. I agree '
    'to inform my healthcare provider of any side effects or adverse reactions I '
    'may experience. I understand that this consent is voluntary and that I can '
    'withdraw from treatment at any time.')

# The tick itself. Client's wording, 2026-08-17.
CS_TICK = 'I have read and understand the information and I wish to proceed'

# The group the tick answers under. It is a real answer in the same shape every
# other screen's is, so `stepValid()` holds Continue until it is on and the back
# button restores it - no per-screen rule anywhere.
GROUP = 'informed_consent'


def _sec(title, body):
    return '<div class="cs-sec"><h3>%s</h3>%s</div>' % (title, body)


def screen(icon, ic, cta):
    """`icon` is build.py's ICON dict, `ic` its inline-SVG helper, `cta` its
    button. Nothing here is unique to this screen but the copy."""
    lead = ''.join(_sec(t, '<p>%s</p>' % b) for t, b in CS_LEAD)
    more = ''.join(_sec(t, '<p>%s</p>' % b) for t, b in CS_MORE)
    doc = ('<div class="cs-sec"><p>%s</p></div>' % CS_DOC_INTRO
           + ''.join(_sec(t, b) for t, b in CS_DOC)
           + _sec('Your acknowledgement', '<p>%s</p>' % CS_ATTEST))

    return ('<div class="col">'
            '<p class="eyebrow">Consent</p>'
            '<h1 class="qhead">One last step &mdash; your consent</h1>'
            '<p class="sub">Quick summary below. The full document is one tap '
            'away.</p>'
            # The summary, then one disclosure holding everything the PDF puts
            # behind "Read full Consent". It expands IN THE PAGE rather than
            # inside a scrolling box: a nested scroll region is the classic way
            # to trap a thumb on a phone, and page scroll costs nothing here
            # because the screen starts short and the patient can close it again.
            + '<div class="reviewcard cs-card">' + lead
            + '<details class="cs-doc"><summary>Read the full consent document%s'
              '</summary><div class="cs-doc-body">%s%s</div></details>'
              % (ic('<path d="M6 9l6 6 6-6"/>'), more, doc)
            + '</div>'
            # Unticked, and it gates Continue. A pre-ticked box is not consent to
            # a treatment, which is why this one is a normal `.opts` box: the
            # engine already refuses to advance a screen whose box has nothing
            # selected, and since 2026-09-08 nothing in the build opens ticked.
            + '<div class="opts cs-agree" data-group="%s" data-mode="multi">'
              '<button class="opt checkbox" data-value="yes"><span class="lbl">%s'
              '</span><span class="ring"></span></button></div>' % (GROUP, CS_TICK)
            + cta('Continue')
            + '<div class="rv-hipaa cs-hipaa">%s<p>We protect your privacy. Your '
              'answers are protected by HIPAA.</p></div>' % icon['shield']
            + '</div>')
