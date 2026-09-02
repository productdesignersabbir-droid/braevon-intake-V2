# -*- coding: utf-8 -*-
"""Parse the MEDVi QUAD intake into medvi-flow.json.

    python3 extract_medvi.py ../../reference/medvi/medvi.html

The reference is a Framer site whose whole questionnaire ships in the server-
rendered HTML as sibling "pages", all but the first hidden. Each page carries a
`data-framer-name` ("Q3 - 03", "INT Quad 4in1"), its question in an <h1>, and
its options as <label><input name=... value=...><h4>label</h4><h6>note</h6>.

The input names are the reference's own field ids and are kept: they are the
closest thing to a data model the flow exposes, and they say which screens
belong to one question.
"""
import html as H
import json
import os
import re
import sys

SRC = sys.argv[1] if len(sys.argv) > 1 else '../../reference/medvi/medvi.html'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'medvi-flow.json')

TAG = re.compile(r'<[^>]+>')
DIV = re.compile(r'<div\b|</div>')


def txt(s):
    s = re.sub(r'<(script|style|svg)\b.*?</\1>', ' ', s, flags=re.S)
    s = re.sub(r'<br\s*/?>', ' ', s)
    return re.sub(r'\s+', ' ', H.unescape(TAG.sub('', s))).strip()


def div_inner(s, start):
    """(inner, index_after_close) for the <div> opening at `start`."""
    gt = s.index('>', start) + 1
    depth = 1
    for m in DIV.finditer(s, gt):
        depth += 1 if m.group(0) == '<div' else -1
        if depth == 0:
            return s[gt:m.start()], m.end()
    return s[gt:], len(s)


def pages(doc):
    m = re.search(r'<div[^>]*data-framer-name="Pages"[^>]*>', doc, re.I)
    if not m:
        sys.exit('could not find the Pages container')
    inner, _ = div_inner(doc, m.start())
    out, pos = [], 0
    while True:
        d = re.compile(r'<div\b').search(inner, pos)
        if not d:
            break
        body, pos = div_inner(inner, d.start())
        tag = inner[d.start():inner.index('>', d.start())]
        name = re.search(r'data-framer-name="([^"]*)"', tag)
        out.append((name.group(1) if name else '', body))
    return out


LABEL_OPEN = re.compile(r'<label\b', re.I)
LABEL_TOK = re.compile(r'<label\b|</label>', re.I)
INPUT = re.compile(r'<input\b([^>]*)>', re.I)


def enclosing_label(body, at):
    """The innermost <label> containing the input that starts at `at`.

    The reference nests one label per option inside an outer label that wraps
    the whole group, so scanning forward from every <label> yields the outer
    one first — with every option's text in it. Walking back from the input
    instead lands on the option's own label."""
    starts = [m.start() for m in LABEL_OPEN.finditer(body, 0, at)]
    for st in reversed(starts):
        depth, i = 1, body.index('>', st) + 1
        while depth:
            n = LABEL_TOK.search(body, i)
            if not n:
                return None
            depth += 1 if n.group(0).lower().startswith('<label') else -1
            i = n.end()
        if i > at:                     # this label still open at the input
            return body[body.index('>', st) + 1:n.start()]
    return None


def options_of(body):
    """Every radio/checkbox on the page, with its own label and note."""
    out = []
    for m in INPUT.finditer(body):
        a = dict(re.findall(r'([a-zA-Z-]+)="([^"]*)"', m.group(1)))
        if a.get('type') not in ('radio', 'checkbox'):
            continue
        inner = enclosing_label(body, m.start())
        if inner is None:
            continue
        h4 = re.search(r'<h[3-5][^>]*>(.*?)</h[3-5]>', inner, re.S)
        h6 = re.search(r'<h6[^>]*>(.*?)</h6>', inner, re.S)
        label = txt(h4.group(1)) if h4 else txt(inner)
        note = txt(h6.group(1)) if h6 else ''
        # a label built from the whole block swallows its own note
        if note and label.endswith(note):
            label = label[:-len(note)].strip()
        if not label:
            continue
        o = {'value': H.unescape(a.get('value', '')), 'label': label,
             'type': a['type'], 'name': H.unescape(a.get('name', ''))}
        if note and note != label:
            o['note'] = note
        if any(o['value'] == q['value'] and o['label'] == q['label'] for q in out):
            continue
        out.append(o)
    return out


def fields_of(body):
    out = []
    for m in re.finditer(r'<(input|textarea|select)\b([^>]*)>', body):
        a = dict(re.findall(r'([a-zA-Z-]+)="([^"]*)"', m.group(2)))
        if a.get('type') in ('radio', 'checkbox', 'hidden', 'submit'):
            continue
        if not a.get('name') and not a.get('id'):
            continue
        f = {'tag': m.group(1), 'name': H.unescape(a.get('name') or a.get('id')),
             'input_type': a.get('type'), 'placeholder': H.unescape(a.get('placeholder', ''))}
        if m.group(1) == 'select':
            blk, _ = (body[m.end():], 0)
            end = blk.find('</select>')
            f['options'] = [txt(o) for o in
                            re.findall(r'<option[^>]*>(.*?)</option>', blk[:end], re.S)]
        out.append(f)
    return out


def heads(body):
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', body, re.S)
    subs = [txt(x) for x in re.findall(r'<h[23][^>]*>(.*?)</h[23]>', body, re.S)]
    return (txt(h1.group(1)) if h1 else None), [s for s in subs if s]


# ---------------------------------------------------------------- annotation
# The reference encodes its branching in the page names — "5.a.1" is the
# follow-up to option 1 of question 5, "13.a.2" to the alpha blocker on 13 —
# and its safety rules in the notes under the options. Both are read off here
# rather than hand-listed, so a change to the reference shows up as a diff.

TRIED = ['Viagra', 'Cialis', 'Levitra', 'Staxyn', 'Stendra',
         'A medication or supplement which is not listed here']

DISQUALIFY = re.compile(r'disqualif', re.I)
EXCLUSIVE_SAFE = re.compile(r'select this to continue', re.I)
NONE_OPTION = re.compile(r"(none of the|no, i don'?t)", re.I)


def annotate(flow):
    by_name = {p['name']: p for p in flow}

    def group_of(prefix):
        for p in flow:
            if p['name'].startswith(prefix) and p['group']:
                return p['group']
        return None

    tried_group = group_of('ED Tried 1')
    bp_group = group_of('Blood Pressure 1')
    risk_group = group_of('Cardiovascular risk -')
    meds_group = group_of('Medication - 13')

    for p in flow:
        n = p['name']
        cond = None
        m = re.search(r'5\.[ab]\.([1-6])$', n)
        if m:
            cond = {'group': tried_group, 'any': [TRIED[int(m.group(1)) - 1]]}
        elif n.endswith('5.c'):
            cond = {'group': tried_group, 'any': TRIED}
        elif n.endswith('07.a') or n.endswith('07.b'):
            cond = {'group': bp_group, 'any': ['yes']}
        elif 'if diabet' in n.lower():
            cond = {'group': risk_group,
                    'any': ['Diabetes, pre-diabetes, or glucose intolerance']}
        elif n.endswith('13.a.1'):
            cond = {'group': meds_group,
                    'any': ['Nitroglycerin under the tongue spray or tablet']}
        elif n.endswith('13.a.2'):
            cond = {'group': meds_group, 'any': ['Any alpha blocker']}
        p['cond'] = cond

        # safety rules. Two shapes: a note on one option saying it disqualifies,
        # or a note on the exclusive option saying everything else does.
        # "Select this to continue…" on most safety screens, but the drugs
        # screen words it as "…will make you ineligible" under its own None.
        safe = [o for o in p['options']
                if o.get('note') and (EXCLUSIVE_SAFE.search(o['note'])
                                      or (NONE_OPTION.match(o['label'])
                                          and re.search(r'ineligible', o['note'], re.I)))]
        if safe:
            p['exclusive'] = safe[0]['value']
            p['dq_on'] = [o['value'] for o in p['options'] if o['value'] != safe[0]['value']]
            p['dq_kind'] = 'all-but-exclusive'
        else:
            hits = [o['value'] for o in p['options']
                    if o.get('note') and DISQUALIFY.search(o['note'])]
            p['exclusive'] = None
            p['dq_on'] = hits
            p['dq_kind'] = 'named' if hits else None
        # a "none of these" option is exclusive even where nothing disqualifies
        if not p['exclusive']:
            for o in p['options']:
                if NONE_OPTION.match(o['label']):
                    p['exclusive'] = o['value']
                    break
    return flow



def main():
    doc = open(SRC, encoding='utf-8').read()
    flow = []
    for i, (name, body) in enumerate(pages(doc), 1):
        title, subs = heads(body)
        opts = options_of(body)
        flow.append({
            'n': i, 'name': name, 'title': title, 'subs': subs,
            'options': opts, 'fields': fields_of(body),
            'group': opts[0]['name'] if opts else None,
            'mode': 'multi' if opts and opts[0]['type'] == 'checkbox' else
                    ('single' if opts else None),
        })
    flow = annotate(flow)
    json.dump(flow, open(OUT, 'w'), indent=1, ensure_ascii=False)
    print('%d pages -> %s\n' % (len(flow), os.path.basename(OUT)))
    for p in flow:
        print('%2d  %-34s %-52s opts=%-3d fields=%s'
              % (p['n'], p['name'][:34], (p['title'] or '—')[:52],
                 len(p['options']), len(p['fields'])))


main()
