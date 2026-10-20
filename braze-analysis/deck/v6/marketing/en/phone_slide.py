"""English slide for the offsite deck: three real cases seen from the person's phone.
Phone screens are illustrative (message types, not real copy); every number comes from the Braze audit (deck v6)."""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'scripts'))
from deck_v6_render import page

INK, TXT, SEC, BLUE, BSOFT = '#0B1220', '#3B4556', '#6B7484', '#1F4FD8', '#E8EEFC'
FF = 'Inter, system-ui, sans-serif'
APP = {'Email': '#6B7484', 'Push': '#1F4FD8', 'WhatsApp': '#127A5B'}


def phone(notifs, badge):
    """notifs = [(channel, title, when)] drawn as a lock screen; badge = red counter text."""
    W, H = 200, 380
    o = [f'<svg viewBox="0 0 {W} {H}" width="100%" style="display:block;height:auto" role="img" aria-label="Phone lock screen with {len(notifs)} notifications" font-family="{FF}">',
         f'<rect x="4" y="4" width="{W - 8}" height="{H - 8}" rx="30" fill="#0B1220"/>',
         f'<rect x="12" y="12" width="{W - 24}" height="{H - 24}" rx="23" fill="#EEF1F6"/>',
         f'<rect x="{W / 2 - 30}" y="20" width="60" height="14" rx="7" fill="#0B1220"/>',
         f'<text x="{W / 2}" y="66" font-size="26" font-weight="300" fill="{INK}" text-anchor="middle">9:41</text>']
    y = 84
    for ch, title, when in notifs:
        o.append(f'<rect x="20" y="{y}" width="{W - 40}" height="38" rx="9" fill="#FFFFFF"/>')
        o.append(f'<rect x="27" y="{y + 9}" width="20" height="20" rx="5" fill="{APP[ch]}"/>')
        o.append(f'<text x="37" y="{y + 23}" font-size="9" font-weight="700" fill="#FFFFFF" text-anchor="middle">{ch[0]}</text>')
        o.append(f'<text x="53" y="{y + 16}" font-size="8.5" fill="{SEC}">Kueski · {ch}</text>')
        o.append(f'<text x="{W - 26}" y="{y + 16}" font-size="8" fill="{SEC}" text-anchor="end">{when}</text>')
        o.append(f'<text x="53" y="{y + 29}" font-size="9.5" font-weight="600" fill="{INK}">{title}</text>')
        y += 43
    o.append(f'<rect x="{W - 78}" y="{H - 52}" width="58" height="24" rx="12" fill="#D92D20"/>')
    o.append(f'<text x="{W - 49}" y="{H - 36}" font-size="11" font-weight="700" fill="#FFFFFF" text-anchor="middle">{badge}</text>')
    return ''.join(o) + '</svg>'


def case(eyebrow, ph, big, sub, body):
    return ('<div style="display:grid;grid-template-columns:52fr 48fr;gap:1.2cqi;align-items:start">'
            f'<div>{ph}</div>'
            '<div style="display:flex;flex-direction:column;gap:.5cqi">'
            f'<div style="font-size:.85cqi;letter-spacing:.1em;text-transform:uppercase;color:{BLUE};font-weight:700">{eyebrow}</div>'
            f'<div class="big" style="font-size:3.6cqi;color:{INK}">{big}</div>'
            f'<div style="font-size:1.1cqi;font-weight:700;color:{INK};line-height:1.3">{sub}</div>'
            f'<div style="font-size:1.02cqi;line-height:1.4;color:{TXT}">{body}</div></div></div>')


p1 = phone([('Email', 'Finish verifying your identity', 'day 1'), ('Email', 'Your loan is one step away', 'day 2'),
            ('Email', 'Finish verifying your identity', 'day 3'), ('Email', 'Tasa 0 on your first loan', 'day 4'),
            ('Email', 'Finish verifying your identity', 'day 5'), ('Email', 'Unsubscribe confirmed', 'day 5')], '10 emails')
p2 = phone([('WhatsApp', 'Your Tasa 0 offer ends today', '9:02'), ('Push', 'Invite a friend, both win', '11:30'),
            ('Email', 'New deals with Kueski Pay', '13:15'), ('Push', 'Your credit is waiting', '18:40'),
            ('Email', 'Tasa 0: last hours', '20:05'), ('WhatsApp', 'Don’t miss your offer', '21:10')], '2 a day')
p3 = phone([('Email', 'You have been unsubscribed', 'Jan'), ('Email', 'Tasa 0 is back for you', 'Feb'),
            ('Email', 'Finish verifying your identity', 'Mar'), ('Email', 'Invite a friend, both win', 'May'),
            ('Email', 'Finish verifying your identity', 'Jul'), ('Email', 'Finish verifying your identity', 'Sep')], 'still here')

html = ('<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2cqi;margin-top:.6cqi">'
        + case('The person who just signed up', p1, '10 emails', 'before she unsubscribed, around day 5',
               '70K new users unsubscribed from our emails, typically 5 days and 10 emails in. Half did it on the sign-up reminder, '
               'which arrives almost 6 times a month.')
        + case('Our most active customer', p2, '2 a day', 'on 210 of the 273 days',
               '339K people (1.7% of the base) got 482 messages each in nine months. When three campaigns hit someone on the same '
               'day, we are in 63% of those clashes.')
        + case('The person who already said no', p3, '58K', 'promotional emails from us after they unsubscribed',
               '45K people who had unsubscribed still got 79K promotions; 58K were ours. The verification reminder kept arriving '
               'for nine months.')
        + '</div>'
        + f'<div style="margin-top:2cqi;background:{BSOFT};padding:.9cqi 1.3cqi;display:flex;gap:1.3cqi;align-items:baseline">'
          f'<b style="font-size:.85cqi;letter-spacing:.12em;color:{BLUE}">AND</b>'
          f'<span style="font-size:1.15cqi;color:{INK};line-height:1.35">59% of all messages go through a channel that person has never '
          'responded to: emails to people who only read WhatsApp, push to people who never open push.</span></div>')

d = dict(n=5, kind='html', ancho_completo=True,
         titulo='Seen from the person’s phone, this is what our messages feel like: three real cases',
         html=html,
         fuente=('Source: Braze audit, Jan to Sep 2026 (deck v6, pages 8, 18, 24, 35, 52, 63). Screens are illustrative; numbers are real. '
                 '58K = Marketing promotional emails to people already unsubscribed.'))
OUT = pathlib.Path(__file__).resolve().parent
(OUT / 'phone_slide.json').write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
(OUT / 'phone_slide.html').write_text(page([d], 'Seen from the phone'), encoding='utf-8')
print(OUT / 'phone_slide.html')
