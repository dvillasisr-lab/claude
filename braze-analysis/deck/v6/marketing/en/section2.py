"""Two English slides for the offsite deck, section 2: 'Braze today: what the audit found' and 'What we found, in three sentences'.
Numbers from the Braze audit (E1, E2, E4b, E13; deck v6). Output: section2.html and, with html2pptx.js, section2.pptx."""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'scripts'))
from deck_v6_render import page

INK, TXT, SEC, BLUE, BSOFT, GREEN, GSOFT, NAVY = '#0B1220', '#3B4556', '#6B7484', '#1F4FD8', '#E8EEFC', '#127A5B', '#E4F2EC', '#0B1A3A'


def card(big, txt):
    return (f'<div style="background:#F4F6F9;padding:1.1cqi 1.3cqi;display:flex;flex-direction:column;gap:.4cqi">'
            f'<div class="big" style="color:{BLUE};font-size:3.4cqi">{big}</div>'
            f'<div style="font-size:1.05cqi;line-height:1.3;color:{INK}">{txt}</div></div>')


TH = 'style="padding:.4cqi .7cqi .4cqi 0"'
THN = 'class="num" style="padding:.4cqi .7cqi .4cqi 0"'
TD = 'style="padding:.42cqi .7cqi .42cqi 0"'
TDN = 'class="num" style="padding:.42cqi .7cqi .42cqi 0"'


def fila(c, *v, bold=False):
    tds = ''.join(f'<td {TDN}>{"<b style=color:" + BLUE + ">" + x + "</b>" if bold and i == len(v) - 1 else x}</td>' for i, x in enumerate(v))
    return f'<tr><td {TD}><b>{c}</b></td>{tds}</tr>'


tabla = ('<table style="font-size:1.02cqi">'
         f'<tr><th {TH}>Channel</th><th {THN}>Share of messages</th><th {THN}>Open rate</th><th {THN}>Click to open</th>'
         f'<th {THN}>Loans in 7 days, per month</th><th {THN}>Loans per 1,000 messages</th></tr>'
         + fila('Email', '50%', '23.7%', '3.9%', '185K', '5.0')
         + fila('Push', '38%', '1.5%', 'n/a', '89K', '3.2')
         + fila('WhatsApp', '8%', '68.9% read', 'n/a', '39K', '6.4')
         + fila('In-app', '4%', 'n/a', '38.2% click', '63K', '20.7', bold=True)
         + '</table>')

ver = (f'<div style="background:{NAVY};padding:1.4cqi 1.6cqi;color:#FFFFFF;display:flex;flex-direction:column;gap:.8cqi;height:100%;box-sizing:border-box">'
       '<div style="font-size:.9cqi;letter-spacing:.12em;font-weight:700;color:#8FA8EE">WHAT WE SEE</div>'
       + ''.join(f'<div style="font-size:1.08cqi;line-height:1.38;color:#FFFFFF"><b>{n} ·</b> {t}</div>' for n, t in (
           (1, 'In-app wins 20.7 loans per 1,000 messages, four to six times email or push, yet carries only 4% of what we send.'),
           (2, 'Email gets opened (24%) but only 4 in 100 who open it click; push is 38% of our messages and 1.5% open it.'),
           (3, 'WhatsApp is 71% of the spend with 8% of the messages, and wins barely more loans per message than email.')))
       + '</div>')

turno = (f'<div style="margin-top:1.4cqi;background:{GSOFT};padding:.9cqi 1.3cqi;display:flex;gap:1.3cqi;align-items:center">'
         f'<div style="background:{GREEN};color:#FFFFFF;font-weight:700;font-size:.9cqi;letter-spacing:.1em;padding:.5cqi 1cqi;border-radius:2cqi">YOUR TURN · 5 MIN</div>'
         f'<div style="font-size:1.25cqi;font-weight:600;color:{INK}">Which of these numbers surprises you? Which one did you already expect?</div></div>')

s1 = dict(n=1, kind='html', ancho_completo=True, eyebrow='Section 2 · Diagnosis', titulo='Braze today: what the audit found',
          html=('<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1.2cqi">'
                + card('269', 'canvases sent something in September; 228 of them are marked "archived"')
                + card('12%', 'of sends fire because the person did something; the other 88% go to lists')
                + card('3', 'messages per customer per week, all teams (about 12 a month)')
                + card('96', 'canvases sending in 2026 with no owner or audience; 748 communications with no team or ticket')
                + '</div>'
                + '<div style="display:grid;grid-template-columns:62fr 38fr;gap:1.6cqi;margin-top:1.4cqi;align-items:stretch">'
                + f'<div>{tabla}</div><div>{ver}</div></div>' + turno),
          fuente=('Source: Braze audit, January to September 2026. Loans = granted within 7 days of a message, split across that day\'s '
                  'messages. WhatsApp read rate includes reads in the following month.'))


def caja(t):
    return f'<div style="border:1.5px dashed #B9C8F2;background:#FBFCFF;padding:1.2cqi 1.3cqi;font-size:1.18cqi;line-height:1.42;height:100%;box-sizing:border-box;color:{INK}">{t}</div>'


def num(n):
    return (f'<div style="width:2.6cqi;height:2.6cqi;border-radius:50%;background:{BLUE};color:#FFFFFF;font-weight:700;font-size:1.3cqi;'
            f'display:flex;align-items:center;justify-content:center">{n}</div>')


FILAS = [
    ('<b>73% of the people we wrote to (14.2M) did not respond to anything in nine months</b>, and 59% of our messages go through a channel that person has never responded to.',
     'We pay for messages nobody reads and wear out the permission: Marketing gets 5.9 unsubscribes per 1,000 emails, more than double the other teams (2.6).',
     '<b>Send each person through the channel they responded to in the last 90 days; WhatsApp only to people who read one, with 10% held out.</b> MarTech and Data build it; Marketing applies it. Week 3 to Month 2.'),
    ('<b>Messages with a reason win: 12% of our emails, 57% of the clicks</b> (26 vs 3.5 clicks per 1,000). In-app wins 20.7 loans per 1,000 messages with 4% of what we send.',
     'List promotions get ignored or unsubscribed, while the sign-up reminder wins a loan for MXN 21. The message is not the problem; who gets it, and why, is.',
     '<b>Rebuild the 10 biggest list promotions as journeys that fire on something the person did, starting with Tasa 0 to lapsed leads; move referrals into in-app.</b> Marketing with Product Growth, Weeks 1 to 4.'),
    ('<b>Braze has no owner and no shared rules: only 1 of 3,228 Canvases has a real control group</b>, 748 communications have no team or ticket, and there is no limit per person.',
     'Nobody can say what Braze actually sells. Up to 2.3M people a month get three or more campaigns in one day, and 43.3M promotions went to people with a frozen KPay line.',
     '<b>Global exclusions (Week 1), a 10% control group on every promotion (Week 2), and limits of 5 promotions a week and 1 push a day (Month 2).</b> MarTech configures; CRM runs a weekly review.'),
]
hdr = ''.join(f'<div style="font-size:.95cqi;letter-spacing:.1em;font-weight:700;color:{BLUE}">{h}</div>' for h in ('FINDING', 'WHAT IT MEANS', 'WHAT WE DO'))
grid = (f'<div style="display:grid;grid-template-columns:3.4cqi repeat(3,minmax(0,1fr));gap:1.2cqi 1.2cqi;align-items:stretch">'
        f'<div></div>{hdr}'
        + ''.join(f'<div style="display:flex;align-items:center">{num(i + 1)}</div>{caja(a)}{caja(b)}{caja(c)}' for i, (a, b, c) in enumerate(FILAS)) + '</div>')
s2 = dict(n=2, kind='html', ancho_completo=True, eyebrow='Section 2 · What we found', titulo='What we found, in three sentences',
          html=grid,
          fuente='Source: Braze audit, January to September 2026 (deck v6, pages 12, 14, 18, 28, 35, 51, 81, 86 and 88). Loans = granted within 7 days of a message.')

OUT = pathlib.Path(__file__).resolve().parent
(OUT / 'section2.html').write_text(page([s1, s2], 'Section 2 · What we found'), encoding='utf-8')
for i, d in enumerate((s1, s2), 1):
    (OUT / f'section2_{i}.json').write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
print(OUT / 'section2.html')
