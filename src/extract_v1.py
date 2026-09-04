# -*- coding: utf-8 -*-
"""Pull the v1 question set out of v1/interactive.html into questions.json.

The v1 flow is the approved clinical content: 24 numbered questions, their
options, the conditional follow-ups and the disqualification rules. v2 changes
the design, not the questions, so they are lifted verbatim rather than retyped.
Run from v2/src: python3 extract_v1.py
"""
import re, json, os, sys, html as H

# The v1 build to read the questions out of. This repo ships the extracted
# `questions.json`, so the site builds without v1 present; you only need v1 when
# pulling a content change across. Point at it explicitly:
#     python3 extract_v1.py /path/to/v1/interactive.html
DEFAULT_SRC = os.path.join(os.path.dirname(__file__), '..', '..', 'v1', 'interactive.html')
SRC = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SRC
OUT = os.path.join(os.path.dirname(__file__), 'questions.json')

TAG = re.compile(r'<[^>]+>')

def txt(s):
    s = re.sub(r'<small>.*?</small>', '', s, flags=re.S)
    s = re.sub(r'<br\s*/?>', ' ', s)
    return re.sub(r'\s+', ' ', H.unescape(TAG.sub('', s))).strip()

def small_of(s):
    m = re.search(r'<small>(.*?)</small>', s, re.S)
    return txt(m.group(1)) if m else None

def parse_opts(block):
    out = []
    for m in re.finditer(r'<button class="opt([^"]*)"([^>]*)>(.*?)</button>', block, re.S):
        cls, attrs, inner = m.groups()
        a = dict(re.findall(r'data-([a-z-]+)="([^"]*)"', attrs))
        o = {"value": a.get('value', ''), "label": txt(inner)}
        note = re.search(r'<span class="inline-note">(.*?)</span>', inner, re.S)
        if note:
            o["label"] = txt(re.sub(r'<span class="inline-note">.*?</span>', '', inner, flags=re.S))
            o["note"] = txt(note.group(1))
        sub = small_of(inner)
        if sub: o["sub"] = sub
        if 'exclusive' in attrs: o["exclusive"] = True
        if 'sys' in a: o["sys"], o["dia"] = a['sys'], a['dia']
        if 'selected' in cls: o["preselected"] = True
        out.append(o)
    return out

DIV_TOK = re.compile(r'<div\b|</div>')

def div_inner(body, open_start):
    """Return (inner_html, index_after_close) for the <div> opening at
    `open_start`, counting nested divs. The option lists interleave notes and
    separators as nested divs, so a non-greedy `.*?</div>` stops in the wrong
    place and silently drops every option after the first."""
    gt = body.index('>', open_start) + 1
    depth, i = 1, gt
    for m in DIV_TOK.finditer(body, gt):
        depth += 1 if m.group(0) == '<div' else -1
        if depth == 0:
            return body[gt:m.start()], m.end()
    return body[gt:], len(body)


HEAD = re.compile(
    r'<p class="eyebrow">(?P<eyebrow>.*?)</p>'
    r'|<h1 class="qhead(?P<big>[^"]*)">(?P<title>.*?)</h1>'
    r'|<p class="sub(?P<subcls>[^"]*)">(?P<sub>.*?)</p>'
    r'|<p class="fieldset-label[^"]*">(?P<flabel>.*?)</p>'
    r'|<div class="(?P<dcls>[^"]*)"(?P<drest>[^>]*)>',
    re.S)


def blocks_of(body):
    """Walk the step body in document order, emitting one entry per control."""
    out, pos = [], 0
    while True:
        m = HEAD.search(body, pos)
        if not m:
            break
        d = m.groupdict()
        pos = m.end()
        if d['eyebrow'] is not None:
            out.append({"t": "eyebrow", "text": txt(d['eyebrow'])})
        elif d['title'] is not None:
            out.append({"t": "title", "text": txt(d['title']),
                        "big": bool((d['big'] or '').strip())})
        elif d['sub'] is not None:
            out.append({"t": "sub", "text": txt(d['sub'])})
        elif d['flabel'] is not None:
            out.append({"t": "legend", "text": txt(d['flabel'])})
        else:
            cls = set((d['dcls'] or '').split())
            # `fields` is only a row wrapper; matching it as a field would
            # swallow every real field inside it and report one.
            kind = ('opts' if 'opts' in cls else
                    # `tiles` is v1's two-up control (Male / Female). It is a
                    # single-select like any other, drawn wider; the reference
                    # draws its own sex question the same way.
                    'tiles' if 'tiles' in cls and 'data-group' in (d['drest'] or '') else
                    'reveal' if 'reveal' in cls else
                    'note' if 'note' in cls else
                    'field' if 'field' in cls else None)
            if kind is None:
                continue
            inner, pos = div_inner(body, m.start())
            attrs = (d['dcls'] or '') + (d['drest'] or '')
            a = dict(re.findall(r'data-([a-z-]+)="([^"]*)"', attrs))
            if kind == 'note':
                # keep <b> — the eligibility note leans on it for "male" and
                # "18 years of age", which is the whole point of the panel
                keep_b = lambda h: re.sub(r'<(?!/?b\b)[^>]+>', ' ', h)
                out.append({"t": "note", "dark": 'dark' in cls,
                            "lead": (lambda m: txt(m.group(1)) if m else None)(
                                re.search(r'<p class="nt">(.*?)</p>', inner, re.S)),
                            "text": re.sub(r'\s+', ' ', H.unescape(keep_b(
                                re.sub(r'<p class="nt">.*?</p>', '', inner, flags=re.S)))).strip()})
            elif kind == 'tiles':
                tiles = [{"value": tm.group(2), "label": txt(tm.group(3)),
                          **({"preselected": True} if 'selected' in tm.group(1) else {})}
                         for tm in re.finditer(
                             r'<button class="tile([^"]*)" data-value="([^"]+)"[^>]*>(.*?)</button>',
                             inner, re.S)]
                if tiles:
                    out.append({"t": "options", "style": "tiles",
                                "group": a.get('group', ''), "mode": a.get('mode', 'single'),
                                "optional": False, "options": tiles})
            elif kind == 'opts':
                opts = parse_opts(inner)
                if not opts:
                    continue
                note = re.search(r'<div class="opt-note"><span>(.*?)</span>', inner, re.S)
                ent = {"t": "options", "group": a.get('group', ''),
                       "mode": a.get('mode', 'single'),
                       "optional": 'data-optional' in attrs,
                       "options": opts}
                if note:
                    ent["hint"] = txt(note.group(1))
                if 'grouped' in cls:
                    ent["grouped"] = True
                out.append(ent)
            elif kind == 'reveal':
                lab = re.search(r'<label[^>]*>(.*?)</label>', inner, re.S)
                ta = re.search(r'<(textarea|input)([^>]*)>', inner)
                ph = re.search(r'placeholder="([^"]*)"', ta.group(2)) if ta else None
                sub = re.search(r'<p class="reveal-sub">(.*?)</p>', inner, re.S)
                ent = {"t": "reveal", "for": a.get('reveal-for'), "on": a.get('reveal-on'),
                       "label": txt(lab.group(1)) if lab else None,
                       "control": ta.group(1) if ta else None,
                       "placeholder": H.unescape(ph.group(1)) if ph else None,
                       "error": a.get('err')}
                if sub:
                    ent["sub"] = txt(sub.group(1))
                if 'bp-warning' in attrs:
                    ent["kind"] = "bp-warning"
                    ent["text"] = txt(inner)
                # A follow-up question inside the reveal, not a text box: v1's
                # `reveal_yesno`, which draws its Yes/No as `.tile` buttons
                # under a `.fieldset-label`. `parse_opts` only matches `.opt`,
                # so these came out as empty reveals - which lost four
                # questions, all of them disqualifying ones (curve-recent,
                # curve-pain, heart-recent, stroke-recent).
                nested = parse_opts(inner)
                if not nested:
                    nested = [{"value": tm.group(2), "label": txt(tm.group(3))}
                              for tm in re.finditer(
                                  r'<button class="tile([^"]*)" data-value="([^"]+)"'
                                  r'[^>]*>(.*?)</button>', inner, re.S)]
                if nested:
                    g = re.search(r'data-group="([^"]+)"', inner)
                    ent["options"] = nested
                    ent["group"] = g.group(1) if g else None
                    ent["mode"] = (lambda m: m.group(1) if m else 'single')(
                        re.search(r'data-mode="([^"]+)"', inner))
                    q = re.search(r'<p class="fieldset-label[^"]*">(.*?)</p>', inner, re.S)
                    if q and not ent["label"]:
                        ent["label"] = txt(q.group(1))
                out.append(ent)
            else:  # field
                lab = re.search(r'<label[^>]*>(.*?)</label>', inner, re.S)
                el = re.search(r'<(input|select|textarea)([^>]*)>', inner)
                if not el:
                    continue
                fa = dict(re.findall(r'([a-z-]+)="([^"]*)"', el.group(2)))
                ent = {"t": "field", "tag": el.group(1), "id": fa.get('id', ''),
                       "label": txt(lab.group(1)) if lab else None,
                       "input_type": fa.get('type'), "placeholder": fa.get('placeholder'),
                       "inputmode": fa.get('inputmode'),
                       "half": 'half' in cls, "dob": 'dob' in cls}
                if el.group(1) == 'select':
                    ent["options"] = [txt(o) for o in
                                      re.findall(r'<option[^>]*>(.*?)</option>', inner, re.S)]
                out.append(ent)
    return out


def main():
    if not os.path.exists(SRC):
        sys.exit("v1 build not found: %s\n"
                 "Pass the path to v1's interactive.html, e.g.\n"
                 "  python3 extract_v1.py ../../v1/interactive.html" % SRC)
    src = open(SRC, encoding='utf-8').read()
    parts = re.split(r'(<section class="step"[^>]*>)', src)
    steps = []
    for i in range(1, len(parts), 2):
        tag, body = parts[i], parts[i + 1]
        body = body.split('</section>')[0]
        a = dict(re.findall(r'data-([a-z-]+)="([^"]*)"', tag))
        if 'step' not in a: continue
        steps.append({
            "step": int(a['step']),
            "q": int(a['q']) if 'q' in a else None,
            "dq": H.unescape(a['dq']) if 'dq' in a else None,
            "dq_on": a.get('dq-on'),
            "cond": a.get('if'),
            "no_back": 'data-no-back' in tag,
            "blocks": blocks_of(body),
            # screens with no question number are the marketing / result screens;
            # v2 rebuilds those, so only their copy is carried across
            "marketing": 'data-q=' not in tag,
        })
    json.dump(steps, open(OUT, 'w'), indent=1, ensure_ascii=False)
    q = [s for s in steps if s['q']]
    print("steps: %d   numbered questions: %d" % (len(steps), len(q)))
    for s in steps:
        title = next((b['text'] for b in s['blocks'] if b['t'] == 'title'), '—')
        kinds = {}
        for b in s['blocks']:
            kinds[b['t']] = kinds.get(b['t'], 0) + 1
        n = sum(len(b['options']) for b in s['blocks'] if b['t'] == 'options')
        print("%2d %-4s %-58s opts=%-3d %s" % (
            s['step'], ("Q%d" % s['q']) if s['q'] else " ▸", title[:58], n,
            " ".join("%s:%d" % kv for kv in sorted(kinds.items()) if kv[0] not in ('title',))))

main()
