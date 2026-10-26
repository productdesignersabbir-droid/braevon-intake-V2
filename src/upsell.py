# -*- coding: utf-8 -*-
"""Screen 52 - the post-checkout upsell, one offer per pack.

**From the client's Figma, `Braevon - Checkout page`, page "Upsell and Thank
you page" (node 170-2)**, read on 2026-10-19. That page draws two frames,
"when select 6 tablet plan" and "When select 12 tablet plan"; both are v1's
screen 35 (`v1`'s quarterly VIP upsell), imported through html.to.design, so
the type sizes and colours here are v1's `.up` block, measured off the live v1
page and set down to this build's 480px column.

The checkout's last button walks onto this screen, and the screen shows the
offer for **the pack that was selected on the checkout**:

    bought   offered                         source
    6        quarterly, 18 tablets, $169     Figma frame 172:617
    12       quarterly, 36 tablets, $237     Figma frame 172:358
    18       3-month supply, 54 tablets, $299   v3 screen 35 (V5), 2026-10-26


**The 18 is a 3-month supply for $299** (2026-10-26, from v3's screen 35 "V5"
offer). It replaced a "buy 1 more month, get 1 free, +$144" offer. $299 is the
whole price, not the difference, and the struck-through comparison is three
months at the 18 pack's own $172 ($516), so the saving is $217.

Worth knowing:

* "You're currently only saving $24.75 / $33" on the 6 and 12 offers is the
  Figma's own line, copied unchanged. In v1 it was the 25% code's monthly
  saving; this checkout has no code. The 18 has no such figure from the
  client, so its offer leaves that line out rather than invent one.

Accepting and declining both end the flow (the order was placed on the
checkout). The reviews are the checkout's own `TESTIMONIALS` - this screen sits
directly under that one, and new names would read as another product's page.
"""
import checkout

UPSELL_SCREEN = 52

# The three-tablet render from v1 (`product-quarterly.png`), which is what the
# Figma frames draw in this slot.
SHOT = ('assets/images/product-quarterly.png',
        'Three BRAEVON 4-in-1 tablets')

# One dict per pack bought. Keys are the copy and the figures that differ;
# everything else on the page is shared.
OFFERS = {
    '6': dict(
        save='128', save2='128.00', retail='$297', price='$169.00',
        was='$297.00', now_save='24.75', n='18',
        h1='Don&rsquo;t run out. Upgrade to a 3&#8209;month&nbsp;supply',
        sub=('Your 6-tablet plan is secure! But monthly refills kill the momentum. '
             'Upgrade now and we&rsquo;ll automatically ship a fresh 18-tablet, '
             '3&#8209;month supply so you don&rsquo;t run empty.'),
        tag='Save $128 every 3 months',
        name='Quarterly VIP Supply',
        blurb='Maximize your confidence with continuous, automated&nbsp;coverage.',
        hero='on the 18-tablet plan',
        retail_label='Quarterly plan (retail)',
        price_label='Quarterly VIP pricing',
        price_note='You&rsquo;re saving $128 total',
        includes='3 months of BRAEVON 4-in-1',
        close='Upgrade to a 3-month supply.',
        cta='Upgrade to 18-Tablet Supply Now',
        bar='Upgrade &amp; Save $128'),
    '12': dict(
        save='159', save2='159.00', retail='$396', price='$237.00',
        was='$396.00', now_save='33', n='36',
        h1='Don&rsquo;t run out. Upgrade to a 3&#8209;month&nbsp;supply',
        sub=('Your 12-tablet plan is secure! But monthly refills kill the momentum. '
             'Upgrade now and we&rsquo;ll automatically ship a fresh 36-tablet, '
             '3&#8209;month supply so you don&rsquo;t run empty.'),
        tag='Save $159 every 3 months',
        name='Quarterly VIP Supply',
        blurb='Maximize your confidence with continuous, automated&nbsp;coverage.',
        hero='on the 36-tablet plan',
        retail_label='Quarterly plan (retail)',
        price_label='Quarterly VIP pricing',
        price_note='You&rsquo;re saving $159 total',
        includes='3 months of BRAEVON 4-in-1',
        close='Upgrade to a 3-month supply.',
        cta='Upgrade to 36-Tablet Supply Now',
        bar='Upgrade &amp; Save $159'),
    '18': dict(
        save='217', save2='217.00', retail='$516.00', price='$299.00',
        was='$516.00', now_save=None, n='54',
        h1='Don&rsquo;t run out. Get a 3&#8209;month&nbsp;supply',
        sub=('Your 18-tablet plan is secure! But monthly refills kill the momentum. '
             'Upgrade to a full 3&#8209;month supply now &mdash; 36 more tablets, '
             '54 in all, for $299 in total.'),
        tag='3-month supply',
        name='3-Month Supply &middot; 54&nbsp;Tablets',
        blurb='Three months of coverage for $299 in&nbsp;total.',
        hero='on your 3-month supply',
        retail_label='3 months at the monthly price (3 &times; $172)',
        price_label='3-Month Supply',
        price_note='54 tablets &middot; $5.54 per tablet',
        includes='3 months of BRAEVON 4-in-1 (54 tablets in all)',
        close='Get your 3-month supply for $299.',
        cta='Get 3-Month Supply &ndash; $299',
        bar='Upgrade &amp; Save $217'),
}
assert set(OFFERS) == {p[0] for p in checkout.PACKS}, \
    'every pack the checkout sells needs an upsell offer'
# The 18-pack figures, held to their own arithmetic: three months at $172 less
# $299 is the saving, and $299 over 54 tablets is the per-tablet line.
assert 3 * 172 - 299 == float(OFFERS['18']['save2'])
assert round(299 / 54, 2) == 5.54

TICK = ('<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<circle cx="12" cy="12" r="10" fill="currentColor"/>'
        '<path d="M7.4 12.2l3.1 3.1 6.1-6.4" stroke="#FFFFFF" stroke-width="2.2" '
        'stroke-linecap="round" stroke-linejoin="round"/></svg>')
WARN = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/>'
        '<path d="M12 9v4M12 17h.01"/></svg>')
ARROW = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')
# A back arrow to the checkout, for the team testing the flow (2026-10-19):
# the screen is `data-bare`, so the shell's own back button is hidden here.
BACK = ('<button class="up-back" type="button" data-up-back aria-label="Back to checkout">'
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M19 12H5M11 18l-6-6 6-6"/></svg></button>')
RING = ('<svg viewBox="0 0 96 96" fill="none" aria-hidden="true">'
        '<circle cx="48" cy="48" r="44" stroke="currentColor" stroke-width="5"/>'
        '<path d="M29 49l13 13 26-27" stroke="currentColor" stroke-width="6" '
        'stroke-linecap="round" stroke-linejoin="round"/></svg>')

WHY = [
    ('Set It &amp; Forget It:', 'Fresh supply delivered when you need it. Zero hassle.'),
    ('Never Run Out:', 'Eliminate timing anxiety. Always be ready.'),
    ('Lock-In Savings:', 'Secure your exclusive VIP rate for 90 days.'),
]


def offer(pack, stars):
    """One complete offer page for the pack bought."""
    o = OFFERS[pack]
    why = ''.join('<li>%s<span><b>%s</b> %s</span></li>' % (TICK, b, t) for b, t in WHY)
    warn = ('<p class="up-warn">%s<span>You&rsquo;re currently only saving $%s</span></p>'
            % (WARN, o['now_save'])) if o['now_save'] else ''
    rail = ''.join(
        '<article class="up-tcard">%s<h3>%s</h3><p>%s</p><div class="up-who">&mdash; %s</div>'
        '</article>' % (stars, title.replace('&ldquo;', '').replace('&rdquo;', ''), body, who)
        for title, body, who in checkout.TESTIMONIALS)
    return (
        '<div class="up" data-up-for="%(pack)s"%(hidden)s>%(back)s'
        '<p class="up-pending">%(warn_icon)s<span>Wait! Your order is pending '
        '<b data-countdown>10:00</b></span></p>'
        '<div class="up-head"><p class="up-eyebrow">One-time upgrade offer</p>'
        '<h1>%(h1)s &amp; <b>Save&nbsp;$%(save)s!</b></h1>'
        '<p class="up-sub">%(sub)s</p></div>'
        '<div class="up-offer">'
        '<div class="up-tagrow"><span class="up-tag">%(tag)s</span></div>'
        '<div class="up-prod"><div class="up-shot"><img src="%(img)s" alt="%(alt)s"/></div>'
        '<div class="up-prod-info"><p class="up-brand">BRAEVON <b>4-in-1</b></p>'
        '<h2>%(name)s</h2><p class="up-prod-sub">%(blurb)s</p></div></div>'
        '<div class="up-why"><p class="up-why-h">Why Men Upgrade:</p><ul>%(why)s</ul></div>'
        '<div class="up-bill">%(warn)s'
        '<p class="up-hero-save">Save <b>$%(save)s</b> %(hero)s</p>'
        '<div class="up-rows">'
        '<div class="up-row"><span>%(retail_label)s</span><span class="up-amt muted">%(retail)s</span></div>'
        '<div class="up-row"><span>Total savings</span><span class="up-amt green">$%(save2)s</span></div>'
        '<div class="up-row"><span>Shipping</span><span class="up-amt">FREE</span></div>'
        '</div>'
        '<div class="up-price"><span class="up-price-l"><b>%(price_label)s</b>'
        '<span>%(price_note)s</span></span>'
        '<span class="up-price-r"><b>%(price)s</b><s>%(was)s</s></span></div>'
        '<p class="up-includes"><b>Price includes:</b> %(includes)s &middot; Unlimited 24/7 '
        'medical support &middot; Written prescription &middot; Free rush shipping</p>'
        '</div>'
        '<div class="up-close"><h3>%(close)s</h3><p>Save money and always be ready!</p>'
        '<p class="up-lock">Bundle locked. Cancel anytime.</p></div>'
        '<p class="up-terms">By providing your card information, you allow Braevon to '
        'charge your card for future payments in accordance with the terms.</p>'
        '<p class="up-bypass">Bypass the forms! 1-Click Checkout</p>'
        '<button class="cta up-cta cta-next" type="button"><span>%(cta)s</span>%(arrow)s</button>'
        '<button class="up-decline cta-next" type="button"><u>No thanks.</u> '
        'I&rsquo;ll stick to my %(pack)s tablets.</button>'
        '</div>'
        '<div class="up-testhead"><p class="up-eyebrow">Those who chose Braevon</p>'
        '<h2>There&rsquo;s a reason people are <b>raving about us</b>.</h2>'
        '<p>Join the %(customers)s men who have trusted Braevon for verified results.</p></div>'
        '<div class="up-rail">%(rail)s</div>'
        '<p class="up-railnote">Scroll for more &rarr;</p>'
        '<div class="up-guar"><span class="up-guar-mark">%(ring)s</span>'
        '<p class="up-guar-eyebrow">Braevon Guarantee</p>'
        '<h2>The only thing you&rsquo;ll lose<br/>is performance anxiety.</h2>'
        '<p>This is a compound medication, formulated by US pharmacists and prescribed '
        'by licensed doctors, with the dose set specifically against your own medical '
        'history.</p></div>'
        '<div class="up-bar"><button class="cta up-cta cta-next" type="button">%(bar)s</button>'
        '<button class="up-bar-no cta-next" type="button">No thanks</button></div>'
        '</div>'
        % dict(o, pack=pack, hidden='' if pack == '12' else ' hidden',
               warn_icon=WARN, back=BACK, img=SHOT[0], alt=SHOT[1], why=why, warn=warn,
               arrow=ARROW, rail=rail, ring=RING, customers=checkout.CUSTOMERS))


def screen(stars):
    """All three offers in one step; the engine shows the one for the pack
    picked on the checkout. With no script (the frames) the 12 shows - the
    pack the checkout opens on."""
    return ''.join(offer(p, stars) for p in ('6', '12', '18'))


def frame(pack, stars):
    """One offer on its own, for all-screens.html."""
    return offer(pack, stars).replace(' hidden>', '>', 1)
