# -*- coding: utf-8 -*-
"""Screen 48 — the approval / checkout page.

**Layout, block order, geometry and type are the MEDVi QUAD reference's**, from
`https://quad.medvi.org/approval?flow=org` — the page its intake hands off to,
and the one screen the earlier v2 note said was out of scope. It is in scope
from 2026-09-04, at the client's word. Every number in `theme.py`'s `.ck` block
was read off that page with `getBoundingClientRect` / `getComputedStyle`, the
same way `reference/medvi/design-notes.md` measured the questionnaire — not
eyeballed from a screenshot. Its sixteen blocks, in order:

     0  headline                       8  pack radios + the product card
     1  goals card                     9  HSA mark + the HIPAA card
     2  intro copy + the onset chart  10  satisfaction / cancellation
     3  the programme card            11  "as featured on"
     4  the five benefit rows         12  three quotes
     5  what's included               13  "Are you ready?" + Checkout
     6  what happens next             14  satisfaction / cancellation (again)
     7  countdown pill                15  FAQ

**Everything inside those blocks is Braevon's**, and comes from v1's own
checkout (`v1/src/steps.py`, screen 34, itself built from the client's
`Checkout Page 2.pdf`): the product, the render, the price table, the FAQ, the
rating and the customer count. Four places where the reference could not simply
be copied, all deliberate and all the same call v1 already made:

- **"BACKED BY RESEARCH FROM" is v1's "As featured on" row.** The reference
  sets NIH, WebMD, ScienceDaily and Mayo Clinic logos under that heading. That
  is a third party's trademark carrying an endorsement claim Braevon has not
  evidenced. v1 answered the identical question for press logos with type-set
  marks and a drop-in path for real files; this reuses that component verbatim.
- **The quotes are v2's `QUOTES` copy**, written for this concept, not MEDVi's
  named customers. Same rule as screens 32 and 44.
- **The money-back guarantee became a cancellation promise.** The reference
  promises a refund. A refund is a commercial commitment only Braevon can make;
  what Braevon does say, in v1's own FAQ, is that a plan can be cancelled at any
  time from the patient portal. That is what this block says. **Ask the client
  whether they want the refund wording** — the slot and its ribbon are already
  the right shape for it.
- **The 4-in-1 stack is Braevon's four molecules**, from `MOLECULES` in
  `build.py`, not the reference's (which carries L-Citrulline where Braevon
  carries vardenafil).

The prices are v1's table, unchanged - see `PACKS` below.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- money
# **From the client's own Figma, `Braevon - Checkout page`, node 5-2**, read on
# 2026-09-04. That file supersedes v1's `QTY_PRICES`, which had three tiers of
# 6 / 10 / 20 uses at $119 / $159 / $189 and is what this screen shipped with
# until the client said the packs were wrong. The Figma's two rows are:
#
#     6 tablets/mon    $99.00    $16.50/tab
#     12 tablets/mon   $132.00   $11.00/tab   [Most popular]  Save 33% per tablet
#
# Its bill waives a $100 consultation and $25 shipping, which is where "$125
# SAVINGS" and the struck $224 / $257 totals come from. This screen has no bill
# - the reference does not - so only the two prices are used here.
#
# The badge is on the **12**, not the 6, because that is where the Figma puts
# it. That leaves the 6 without one, which is the Figma's own arrangement; the
# cards are flex siblings so they stay the same height regardless.
#
# `sub` is the per-tablet figure rather than the reference's "180 hour
# coverage". Those hours were a derivation of mine (pack x the 36-hour window);
# per-tablet price is the client's own number and is what their design leads on.
# `shown` is the Figma's own string, decimals and all: it prints $99.00 and
# $132.00 beside $16.50/tab and $11.00/tab, and dropping the cents on one of the
# pair reads as a typo. `price` stays a number because the CTA strip picks the
# cheapest from it.
PACKS = [
    # tablets, price, shown, sub-line, badge, badge hue
    ('6',  99,  '$99.00',  '$16.50 per tablet', '', ''),
    ('12', 132, '$132.00', '$11.00 per tablet &middot; save 33%',
     'MOST POPULAR', '#E6430D'),
]
# The Figma's "Most popular" opens selected, as the reference's does. The CTA
# strip says "start at just", so it reads the cheapest pack rather than this one.
LEAD_PACK = 1

# The group and the field ids the checkout echoes, all of them v1's own from
# 2026-09-04. They were the reference's (`Q1_primary_goal`, `first_name`) until
# the questions were swapped; naming them once here means the next swap is one
# edit rather than a hunt through the markup.
GOAL_GROUP = 'Q1_primary_goal'
FIRST_NAME_ID = 'first_name'

RATING = '4.6'
CUSTOMERS = '175,000+'


def _price(i):
    return PACKS[i][2]


def _from_price():
    """The lowest price on the page - what "prescriptions start at" means."""
    return min(PACKS, key=lambda p: p[1])[2]


# ---------------------------------------------------------------- the chart
def chart():
    """The BRAEVON onset chart, recoloured for a white ground.

    The artwork arrives as a dark-ground embed: white tick labels and dark
    translucent chips with near-white lettering. Rather than keep an edited
    second copy, `chart.svg` is the file as supplied and the five edits below
    are applied on the way out, so a new export drops in and the recolour still
    applies.

    Two of them are not colour:

    - The chip scale was behind `@media (max-width: 600px)`. Inside an inline
      SVG a media query still measures the **viewport**, not the drawing, and
      this chart is ~392px wide at every viewport width because the column is.
      Unconditional is therefore the correct reading of that rule, not a
      loosening of it: without it the lettering renders at about 4.7px on a
      desktop, which is the case the 2x scale exists for.
    - The `braevon-hold` wrapper, its `<style>` and its IntersectionObserver are
      dropped. They exist to stop the chart playing before it is scrolled to;
      here it lives inside a `display:none` step, and CSS animations do not run
      on a `display:none` subtree and start from frame zero when it is shown. So
      the step machinery already does the observer's job, and an observer on a
      hidden element would never fire — the chart would hold for ever.
    """
    svg = open(os.path.join(HERE, 'chart.svg'), encoding='utf-8').read()
    edits = [
        # The chips: kill the white underlay, then turn the dark translucent
        # pill into a white card with the flow's own hairline. Longest match
        # first — 'fill="white" fill-opacity="0.32"' contains 'fill="white"'.
        ('fill="white" fill-opacity="0.32"', 'fill="none"'),
        ('fill="#01000C" fill-opacity="0.56"',
         'fill="#FFFFFF" stroke="#DEE2EA" stroke-width="2.4"'),
        # What is left of fill="white" is the four tick labels.
        ('fill="white"', 'fill="#4B5568"'),
        # The chip lettering, near-white for a dark pill, now on a white one.
        ('fill="#FDFCFC"', 'fill="#171D2C"'),
    ]
    for a, b in edits:
        svg = svg.replace(a, b)
    return '<div class="ck-chart">%s</div>' % svg


# ---------------------------------------------------------------- content
# Block 4. The reference's five rows, restated against what this flow already
# claims elsewhere: 10-15 minutes and the 36-hour window are screen 2's own
# figures, and the four molecules are `MOLECULES` in build.py.
BENEFITS = [
    ('Be Ready in Minutes', 'Results seen within 10&ndash;15 min', '#FFEDD5', '#F97316'),
    ('Feel Desire Again', 'Primes the brain&rsquo;s arousal pathways', '#F3EBFF', '#A855F7'),
    ('Boost Performance', 'Supports a strong blood-flow response', '#FEE2E2', '#EF4444'),
    ('Last Longer', 'Up to 36 hour performance window', '#DFF7E6', '#22C55E'),
    ('Increased Confidence', 'A 4-in-1 formula for a reliable experience', '#DBEAFE', '#3B82F6'),
]

# Block 5. Service lines, each one a claim v1's checkout already makes: its bill
# waives the consultation and the shipping, and its FAQ says a plan can be
# cancelled from the patient portal at any time.
INCLUDED = [
    'Medication, supplies and instructions',
    'Cancel anytime, come back anytime',
    '24/7 medical support',
    'One-on-one access to our team of physicians',
    'Free express shipping, discreetly packaged',
    'Our promise to help you as much (or as little) as you want along the way',
]

# Block 6. The reference's five steps, with its timings kept and its brand
# swapped. NOT SIGNED OFF - "less than 24 hours" and "within 2 business days"
# are operational promises, and nobody at Braevon has confirmed them. See the
# README before this goes in front of a patient.
NEXT_STEPS = [
    ('Physician Review',
     'You&rsquo;re already pre-qualified. After checkout, a board-certified physician '
     'will review your information and begin the approval process.'),
    ('Fast Prescription Approval',
     'Most prescriptions are approved in less than 24 hours. If needed, same-day '
     'consultations with a licensed clinician are available &mdash; at no extra charge.'),
    ('Medication Shipping',
     'Once approved, your medication is prepared and shipped. You&rsquo;ll receive '
     'tracking information within 2 business days, and your prescription will be on '
     'its way.'),
    ('Monthly Refills',
     'At the end of each month, you&rsquo;ll fill out a quick refill form. We&rsquo;ll '
     'send email and text updates with tracking information as your next shipment '
     'heads your way.'),
    ('Unlimited Support',
     'Questions about your progress, side effects or dosage? You have unlimited, 24/7 '
     'access to our care team and licensed clinicians &mdash; whenever you need us.'),
]

# Block 13's "What's Included?" card - the reference's four lines.
READY_INCLUDED = [
    ('4-in-1 ED medication', 'Cost of medication is included'),
    ('No insurance necessary', ''),
    ('Board-certified doctor review', ''),
    ('1:1 physician guidance', ''),
]

# Block 15. v1's five checkout questions, verbatim from `ck_faq` in
# `v1/src/steps.py`; the reference asks four.
FAQ = [
    ("If Viagra&reg; or Cialis&reg; didn&rsquo;t work for me, could BRAEVON?",
     'Often, yes. BRAEVON is not a single-ingredient pill &mdash; it is a '
     'physician-designed formula combining apomorphine, vardenafil, sildenafil and '
     'tadalafil, so it works on arousal, onset, firmness and duration rather than one '
     'of them. Because it dissolves under the tongue it is absorbed directly into the '
     'bloodstream, which is usually faster than a swallowed tablet. Your dose is set '
     'by a licensed prescriber against your own medical profile. No treatment works '
     'for everyone, but a multi-mechanism formula gives more to work with than a '
     'single molecule does.'),
    ('How quickly does BRAEVON start working?',
     'It dissolves under the tongue instead of passing through the stomach, so it '
     'typically begins working within 15&ndash;30 minutes. For the best result, take '
     'it about 30 minutes beforehand.'),
    ('How long do the effects last?',
     'Most patients report effects lasting up to 36 hours &mdash; a window rather '
     'than a countdown. Duration varies with metabolism and general health, and can '
     'run longer if you have liver or kidney conditions or take certain other '
     'medicines. Your prescriber reviews your history before setting a dose for '
     'exactly this reason.'),
    ('What are the common side effects?',
     'The most commonly reported are headache, flushing, nasal congestion, mild '
     'indigestion, dizziness, back or muscle discomfort, nausea, temporary vision '
     'changes and mild irritation under the tongue. Most are mild and temporary when '
     'they occur. Because BRAEVON combines several active ingredients, your prescriber '
     'reviews your medical history and sets your dose to keep them to a minimum.'),
    ('Does the price cover the medication and the doctor?',
     'Yes. The price shown above includes the doctor consultation, unlimited 1:1 '
     'medical support, your written prescription, a month of medicine and free '
     'shipping. There is nothing else to pay and no insurance is needed. Plans can be '
     'cancelled at any time from your patient portal.'),
]

# **Block 11 is deliberately empty.** The reference runs a "BACKED BY RESEARCH
# FROM" row here, with NIH, WebMD, ScienceDaily and Mayo Clinic logos. This slot
# held v1's "As featured on" row instead - six mastheads set in type - until the
# client asked on 2026-09-04 for anything the reference does not have to come
# out, so it did.
#
# **Neither version is built now, and the reference's own needs two things
# first**: the logo files, and evidence that those bodies have researched or
# endorsed this product. Redrawing a real organisation's logotype reproduces its
# trademark, and "backed by research from the NIH" is a claim the client has to
# be able to stand behind. Ask before building it. The slot is between the
# guarantee and the quotes in `screen()`.

# Placeholder copy written for this concept, not real Braevon reviews - the same
# caveat `QUOTES` in build.py carries. Say so before showing this to anyone who
# might take them at face value.
TESTIMONIALS = [
    ('&ldquo;Feeling like my younger self again&rdquo;',
     'Honestly, I didn&rsquo;t think anything would really help me, but Braevon proved '
     'me wrong. I feel like my younger self again, and my wife has noticed too.',
     'Ethan C.'),
    ('&ldquo;The desire is back, not just the performance&rdquo;',
     'Incredible formula &mdash; not only does it work, but having the desire come '
     'back takes things to another level entirely.',
     'Ryan M.'),
    ('&ldquo;Nothing else compared to the combination&rdquo;',
     'I had tried other products, but nothing compares. The four medicines work '
     'together and the difference is hard to describe.',
     'Logan K.'),
]

# ---------------------------------------------------------------- the footer
# braevon.com's own footer, read off the live site's **phone** variant on
# 2026-09-04 - the right one to copy, because this page is a 480px column at
# every width. Two changes, both the client's:
#
#   * White theme. The site sets it #141414 with #EDEDED type; here the ground
#     is the page's own white and the type comes from the flow's ink ramp.
#   * The full-width BRAEVON wordmark at the very bottom is gone.
#
# Everything else - the tagline, the contact pair, the five legal paragraphs,
# the LegitScript seal, the four policy links, the copyright and the two social
# links - is the site's, wording and order unchanged.
FOOTER_LEGAL = [
    'This website is not a pharmacy or healthcare provider. Medical services and '
    'prescription fulfillment are provided by third-party licensed providers and '
    'pharmacies.',
    'Prescription medications are prescribed, when clinically appropriate, by licensed '
    'medical providers and filled and shipped by US-based, licensed pharmacies.',
    'Service availability and eligibility vary by state. You must be 18 years of age or '
    'older to use this service.',
    'The content on this website is for informational purposes only and should not be '
    'considered medical advice or a substitute for consultation with a licensed '
    'healthcare provider.',
    'All clinical services are provided by Beluga Health, a licensed Telehealth medical '
    'group. Website: belugahealth.com',
]

FOOTER_LINKS = [
    ('Our Medical Providers', 'https://www.braevon.com/providers'),
    ('Terms &amp; Conditions', 'https://www.braevon.com/terms'),
    ('Privacy &amp; Security Policy', 'https://www.braevon.com/privacy'),
    ('Shipping, Cancellation &amp; Refund Policy',
     'https://www.braevon.com/returns-and-shipping'),
]

_MAIL = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
         'stroke-linecap="round" stroke-linejoin="round">'
         '<rect x="2.5" y="4.5" width="19" height="15" rx="2.5"/>'
         '<path d="M3 7l9 6 9-6"/></svg>')
_PIN = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
        'stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M12 22s7-6.4 7-12a7 7 0 1 0-14 0c0 5.6 7 12 7 12z"/>'
        '<circle cx="12" cy="10" r="2.6"/></svg>')
_IG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">'
       '<rect x="3" y="3" width="18" height="18" rx="5"/>'
       '<circle cx="12" cy="12" r="4"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor"/></svg>')
_FB = ('<svg viewBox="0 0 24 24" fill="currentColor">'
       '<path d="M13.5 21v-8h2.7l.4-3.1h-3.1V7.9c0-.9.25-1.5 1.55-1.5H16.7V3.6A21 21 0 0 0 14.3 3.5'
       'c-2.4 0-4 1.45-4 4.12V9.9H7.6V13h2.7v8z"/></svg>')


def footer(logo):
    legal = ''.join('<p>%s</p>' % t for t in FOOTER_LEGAL)
    links = ''.join('<a href="%s" target="_blank" rel="noopener">%s</a>' % (h, t)
                    for t, h in FOOTER_LINKS)
    return (
        '<footer class="ft"><div class="ft-in">'
        '<div class="ft-brand">'
        '<div class="ft-mark">%s</div>'
        '<p class="ft-tag">Direct-to-consumer telehealth biological optimization with '
        'licensed board-certified medical guidance.</p>'
        '<div class="ft-contact">'
        '<span>%s<a href="mailto:support@braevon.com">support@braevon.com</a></span>'
        '<span>%s1317 Edgewater Dr, Suite 2177, Orlando, Florida 32804</span>'
        '</div></div>'
        '<div class="ft-rule"></div>'
        '<div class="ft-legal">%s</div>'
        '<div class="ft-rule"></div>'
        '<div class="ft-bottom">'
        '<div class="ft-bot-top">'
        '<img class="ft-seal" src="assets/images/footer-seal.png" '
        'alt="LegitScript Certified"/>'
        '<div class="ft-links">%s</div>'
        '</div>'
        '<div class="ft-bot-row">'
        '<span>&copy; 2026 BRAEVON LLC. All rights reserved.</span>'
        '<span class="ft-social">'
        '<a href="https://www.instagram.com/braevonhealth" target="_blank" '
        'rel="noopener" aria-label="Braevon on Instagram">%s</a>'
        '<a href="https://www.facebook.com/profile.php?id=61593288807004" '
        'target="_blank" rel="noopener" aria-label="Braevon on Facebook">%s</a>'
        '</span></div>'
        '</div></div></footer>'
        % (logo, _MAIL, _PIN, legal, links, _IG, _FB))


# ---------------------------------------------------------------- the screen
def screen(logo, icon, ic, stars, molecules, goal_style, attr):
    """The whole page. `icon` is build.py's ICON table, `ic` its `_ic` helper,
    `stars` its five-star mark, `molecules` its `MOLECULES` list, `goal_style`
    its `GOAL_STYLE` table and `attr` its attribute escaper - all passed in
    rather than imported so this module stays a leaf and build.py keeps the
    single definition of each."""
    tick = icon['check']
    guarantee = (
        '<div class="ck-guar">'
        '<span class="ck-guar-mark">%s</span>'
        '<div><b>Cancel Anytime</b>'
        '<p>Plans can be cancelled at any time from your patient portal. No contracts, '
        'no cancellation fees, and you can come back whenever you want to.</p></div>'
        '</div>'
        % ic('<path d="M12 2l2.4 4.9 5.4.8-3.9 3.8.9 5.4-4.8-2.5-4.8 2.5.9-5.4-3.9-3.8'
             ' 5.4-.8z"/><path d="M8.6 15.6L6.5 22l5.5-2.6 5.5 2.6-2.1-6.4"/>'))

    # -- 0 -----------------------------------------------------------------
    head = ('<h1 class="ck-h1"><span data-fname-echo>Your</span> BRAEVON 4-in-1 '
            'prescription plan approval!</h1>')

    # -- 1 -----------------------------------------------------------------
    # The reference hardcodes three goal lines and gives each its own glyph.
    # Line one is the patient's own answer from screen 1, echoed the way the
    # medical review echoes it; the two under it are Braevon's own goal wording
    # and are static, as the reference's three are.
    #
    # Because line one is dynamic its glyph has to be too, so all five of
    # screen 1's icons ship inside it and `fillSummary()` shows the one whose
    # `data-goal` matches the answer. The first carries `on` so the JS-less
    # frames render an icon rather than a gap.
    goal_icons = ''.join(
        '<i data-goal="%s" style="color:%s"%s>%s</i>'
        % (attr(k), v[1], ' class="on"' if i == 0 else '', v[2])
        for i, (k, v) in enumerate(goal_style.items()))
    # Line two is one of screen 1's own goals, so it takes that screen's glyph
    # and hue. Line three is not one of the five, so it takes the duration
    # glyph and the blue the "Last Longer" benefit row uses.
    _second = 'Increase erection strength'
    _clock = ic('<rect x="2.5" y="7.5" width="15" height="9" rx="2.6"/>'
                '<path d="M20.5 10.5v3"/><path d="M6 10.5v3"/>')
    goal_rows = (
        '<li><span class="ck-goal-ic" data-echo-icon="%s">%s</span>'
        '<span data-echo="%s">&mdash;</span></li>'
        '<li><span style="color:%s;display:flex">%s</span><span>%s</span></li>'
        '<li><span style="color:#3B82F6;display:flex">%s</span>'
        '<span>Longer duration &amp; satisfaction</span></li>'
        % (GOAL_GROUP, goal_icons, GOAL_GROUP,
           goal_style[_second][1], goal_style[_second][2], _second, _clock))
    goals = ('<div class="ck-goals">'
             '<span class="ck-goals-mark">%s</span>'
             '<div><b>YOUR GOALS</b><ul>%s</ul></div>'
             '</div>' % (icon['person'], goal_rows))

    # -- 2 -----------------------------------------------------------------
    intro = ('<div class="ck-intro">'
             '<p>You get <b>clinician-prescribed medication</b>, personalised dosing '
             'delivered discreetly to your door. Plus 1:1 physician guidance, and 24/7 '
             'Braevon support.</p>'
             '<p>Your medication price never goes up &mdash; even when your dose '
             'increases.</p>'
             '</div>' + chart())

    # -- 3 -----------------------------------------------------------------
    # The success figure is the medical review's 94%, not the reference's 96%,
    # so the two screens cannot disagree. It is still NOT ours - see the README.
    programme = (
        '<div class="ck-prog">'
        '<div class="ck-prog-head"><span class="ck-prog-mark">%s</span>'
        '<h2>BRAEVON 4-in-1</h2></div>'
        '<div class="ck-prog-body">'
        '<div><p>Based on your intake form, you are a good candidate for the '
        '<b>BRAEVON 4-in-1 programme</b>.</p>'
        '<p class="ck-prog-sub">This 4-in-1 stack is designed to prime desire (brain) '
        'and boost blood flow (body) in one sublingual dose.</p></div>'
        '<img src="assets/images/product-prime.png" alt="The BRAEVON 4-in-1 tablet"/>'
        '</div>'
        '<div class="ck-prob">'
        '<p>You have a <b>very high</b> chance of success with prescribed BRAEVON '
        'medication</p>'
        '<div class="ck-prob-fig"><b>94%%</b><span>VERY HIGH</span></div>'
        '</div></div>' % icon['shield'])

    # -- 4 -----------------------------------------------------------------
    rows = ''.join(
        '<div class="ck-benefit"><span class="bubble" style="--bub:%s;--gly:%s">%s</span>'
        '<div><b>%s</b><span>%s</span></div></div>'
        % (bub, gly, tick, name, note)
        for name, note, bub, gly in BENEFITS)
    benefits = ('<div class="ck-sect">'
                '<h2 class="ck-h2">The goals <em>you will accomplish</em> with your '
                'plan:</h2><div class="ck-benefits">%s</div></div>' % rows)

    # -- 5 -----------------------------------------------------------------
    stack = ''.join('<li><b>%s:</b> %s</li>' % (name, note.rstrip('.'))
                    for name, note, _ in molecules)
    incl_rows = ''.join('<li>%s<span>%s</span></li>' % (tick, t)
                        for t in INCLUDED)
    included = ('<div class="ck-incl">'
                '<h2 class="ck-h2 accent">What&rsquo;s included:</h2>'
                '<div class="ck-incl-card">'
                '<img src="assets/images/product-prime.png" alt="The BRAEVON 4-in-1 tablet"/>'
                '<div><div class="ck-incl-title"><b>BRAEVON</b>'
                '<span class="ck-tag">4-IN-1 STACK</span></div>'
                '<ul class="ck-stack">%s</ul></div></div>'
                '<ul class="ck-incl-list">%s</ul>'
                '</div>' % (stack, incl_rows))

    # -- 6 -----------------------------------------------------------------
    steps = ''.join(
        '<li><span class="ck-step-n">STEP %d</span><b>%s</b><p>%s</p></li>'
        % (i + 1, name, body) for i, (name, body) in enumerate(NEXT_STEPS))
    nexts = ('<div class="ck-sect">'
             '<h2 class="ck-h2">What happens <em>next?</em></h2>'
             '<ol class="ck-steps">%s</ol></div>' % steps)

    # -- 7 -----------------------------------------------------------------
    pill = ('<div class="ck-pill"><span>Your approval is reserved for</span>'
            '<b data-countdown>10:00</b></div>')

    # -- 8 -----------------------------------------------------------------
    packs = ''.join(
        '<button class="ck-pack%s" type="button" data-pack="%s" data-price="%s">'
        '<span class="ring"></span>%s'
        '<b>%s PACK</b><small>%s</small></button>'
        % (' selected' if i == LEAD_PACK else '', n, shown,
           ('<em style="background:%s">%s</em>' % (hue, badge)) if badge else '',
           n, sub)
        for i, (n, price, shown, sub, badge, hue) in enumerate(PACKS))
    card_lines = [
        ('Powerful 4-in-1 performance stack that targets desire (brain) and '
         'performance (body)'),
        '<b>Free shipping:</b> discreet delivery',
        ('<b>Price includes:</b> doctor consult, unlimited 1:1 medical support, written '
         'prescription, 4 weeks of medicine and free shipping'),
    ]
    card_rows = ''.join('<li>%s<span>%s</span></li>' % (tick, t)
                        for t in card_lines)
    product = (
        '<div class="ck-sect">'
        '<h2 class="ck-h2 mid"><em>Choose</em> your medication preference below:</h2>'
        '<div class="ck-packs" data-packs>%s</div>'
        '<div class="ck-prod">'
        '<div class="ck-prod-head">'
        '<div><span class="ck-tag" data-pack-tag>%s PACK</span>'
        '<b>BRAEVON 4-in-1</b><small>ED Medication</small></div>'
        '<div class="ck-prod-rate">%s<span>%s customers</span></div>'
        '</div>'
        '<div class="ck-prod-shot">'
        '<img src="assets/images/product-prime.png" alt="The BRAEVON 4-in-1 tablet"/>'
        '</div>'
        '<p class="ck-prod-price">Prescribed for only <b data-pack-price>%s</b></p>'
        '<ul class="ck-prod-list">%s</ul>'
        '</div></div>'
        % (packs, PACKS[LEAD_PACK][0], stars, CUSTOMERS,
           _price(LEAD_PACK), card_rows))

    # -- 9 -----------------------------------------------------------------
    hsa_mark = ('<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" '
                'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">'
                '<path d="M26.3 10.5A13 13 0 1 1 19.4 4.8"/>'
                '<path d="M8 17.6l6.5 6.4L27.6 3"/></svg>')
    hipaa = ('<div class="ck-hsa">%s<p><b>HSA/FSA</b> Eligible</p></div>'
             '<div class="ck-hipaa">'
             '<p>%sYour data is protected by HIPAA</p>'
             '<span>All transactions are secured and encrypted.</span>'
             '</div>' % (hsa_mark, icon['shield']))

    # -- 12 ----------------------------------------------------------------
    quotes = ''.join(
        '<article class="ck-quote"><div class="ck-quote-top"><h3>%s</h3>%s</div>'
        '<p>%s</p><div class="ck-who"><b>%s</b><span>%s Verified customer</span></div>'
        '</article>' % (title, stars, body, who, icon['tick'])
        for title, body, who in TESTIMONIALS)
    quotes = ('<div class="ck-sect">'
              '<h2 class="ck-h2">The <em>results</em> speak for themselves!</h2>'
              '<p class="ck-lead">Braevon success stories are coming in, and we cannot '
              'get enough.</p><div class="ck-quotes">%s</div></div>' % quotes)

    # -- 13 ----------------------------------------------------------------
    ready_rows = ''.join(
        '<li>%s<div><b>%s</b>%s</div></li>'
        % (tick, name, '<span>%s</span>' % note if note else '')
        for name, note in READY_INCLUDED)
    stack_rows = ''.join(
        '<div class="ck-ready-pack"><span class="ck-tag">%s Pack</span>'
        '<b>BRAEVON 4-in-1 prescribed for just</b><em>%s</em></div>'
        % (n, shown) for n, _p, shown, _s, _b, _h in PACKS)
    ready = (
        '<div class="ck-ready">'
        '<span class="ck-ready-tag">Are you ready?</span>'
        '<h2 class="ck-h2">It&rsquo;s time for the <em>life you deserve</em></h2>'
        '<div class="ck-ready-rail">'
        '<div class="ck-ready-clock"><span>You&rsquo;re approved for</span>'
        '<b data-countdown>10:00</b></div>'
        '<div class="ck-ready-strip">Prescriptions start at just <b>%s</b> '
        '&mdash; no insurance needed</div>'
        '<p class="ck-ready-line">The most effective ED programme is right here</p>'
        '</div>'
        '<div class="ck-ready-card">'
        '<h3>What&rsquo;s included?</h3>'
        '<ul class="ck-ready-list">%s</ul>'
        '<div class="ck-ready-packs">%s</div>'
        '<p class="ck-ready-note">Pay one month at a time. No contracts, cancel '
        'anytime. <b>Medication is included.</b></p>'
        '<button class="cta cta-next" type="button">Checkout%s</button>'
        '</div></div>' % (_from_price(), ready_rows, stack_rows, icon['arrow']))

    # -- 15 ----------------------------------------------------------------
    faq = ''.join(
        '<details class="ck-faq-item"><summary>%s%s</summary><p>%s</p></details>'
        % (q, ic('<path d="M6 9l6 6 6-6"/>'), a) for q, a in FAQ)
    faq = ('<div class="ck-faq"><h2>Frequently asked questions</h2>%s</div>' % faq)

    return ('<div class="col ck">'
            '<header class="ck-mast"><div class="logo">%s</div></header>'
            '<div class="ck-clock"><span><span data-fname-echo>Your</span> approval is '
            'valid for</span><b data-countdown>10:00</b></div>'
            % logo
            + head + goals + intro + programme + benefits + included + nexts
            + pill + product + hipaa + guarantee + quotes + ready
            + guarantee + faq
            + footer(logo)
            + '</div>')
