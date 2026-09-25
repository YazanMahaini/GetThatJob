"""Render the readable, horizontal GetThatJob workflow PNG.

Requires cairosvg only when regenerating the public image. The plugin itself
does not need it.
"""

from pathlib import Path
from xml.sax.saxutils import escape

import cairosvg


HERE = Path(__file__).resolve().parent
WIDTH, HEIGHT = 3200, 1600
CARD_W, CARD_H = 655, 560
TOP_Y, BOTTOM_Y = 130, 910
XS = (80, 875, 1670, 2465)


def card(x: int, y: int, title: str, lines: tuple[str, ...]) -> str:
    heading = (
        f'<text x="{x + 45}" y="{y + 100}" font-family="Arial,Helvetica,sans-serif" '
        f'font-size="55" font-weight="800" fill="#70b5f3">{escape(title)}</text>'
    )
    rule = f'<path d="M{x + 45} {y + 135} H{x + CARD_W - 45}" stroke="#355675" stroke-width="3"/>'
    body = ''.join(
        f'<text x="{x + 45}" y="{y + 230 + index * 66}" '
        f'font-family="Arial,Helvetica,sans-serif" font-size="46" '
        f'fill="#d9e8f6">{escape(line)}</text>'
        for index, line in enumerate(lines)
    )
    frame = (
        f'<rect x="{x}" y="{y}" width="{CARD_W}" height="{CARD_H}" rx="45" '
        f'fill="#00182f" stroke="#355675" stroke-width="4"/>'
    )
    return frame + heading + rule + body


def arrow(d: str, *, dashed: bool = False) -> str:
    dash = ' stroke-dasharray="13 13"' if dashed else ""
    return (
        f'<path d="{d}" fill="none" stroke="#6f95b5" stroke-width="8" '
        f'stroke-linecap="round" stroke-linejoin="round"{dash} marker-end="url(#arrow)"/>'
    )


steps = [
    ('01  SET UP', (
        'Ask GetThatJob for help.',
        'SetupSkill creates your',
        'workspace on first use.',
        'SetupChecker finds gaps.',
    )),
    ('02  ADD SOURCES', (
        'Add CVs, credentials and',
        'search priorities.',
        'ProfileIntake verifies facts',
        'and follows your CV style.',
    )),
    ('03  FIND JOBS', (
        'JobFinder searches LinkedIn',
        'Jobs and employer sites.',
        'It checks fit and eligibility;',
        'you sign in if needed.',
    )),
    ('04  PREPARE', (
        'Tailor CV and cover letter.',
        'Fill and check a portal draft.',
        'ProfileBuilder saves verified',
        'answers for future forms.',
    )),
    ('05  REVIEW', (
        'You review the draft and',
        'request any changes.',
        'ApplicationFinalize submits',
        'only with your direction.',
    )),
    ('06  CONFIRM', (
        'EmailConfirmationChecker',
        'looks for a matching receipt',
        'and checks portal evidence.',
    )),
    ('07  TRACK', (
        'The tracker and packet',
        'record the outcome.',
        'ApplicationFollowUp checks',
        'later status when requested.',
    )),
    ('08  REUSE', (
        'The next application reads',
        'the private, growing profile.',
        'Scoped or stale facts are',
        'rechecked before reuse.',
    )),
]

wide_positions = [
    (XS[0], TOP_Y), (XS[1], TOP_Y), (XS[2], TOP_Y), (XS[3], TOP_Y),
    (XS[3], BOTTOM_Y), (XS[2], BOTTOM_Y), (XS[1], BOTTOM_Y), (XS[0], BOTTOM_Y),
]
wide_arrows = [
    arrow('M735 410 H875'),
    arrow('M1530 410 H1670'),
    arrow('M2325 410 H2465'),
    arrow('M2792 690 V910'),
    arrow('M2465 1190 H2325'),
    arrow('M1670 1190 H1530'),
    arrow('M875 1190 H735'),
    arrow('M80 1190 H35 V410 H80', dashed=True),
]

compact_positions = [(80, 80 + index * 680) for index in range(len(steps))]
compact_arrows = [
    arrow(f'M407 {640 + index * 680} V{760 + index * 680}')
    for index in range(len(steps) - 1)
]


def render(name: str, width: int, height: int, positions: list[tuple[int, int]], arrows: list[str]) -> None:
    cards = [card(x, y, title, lines) for (title, lines), (x, y) in zip(steps, positions)]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">GetThatJob workflow</title>
<desc id="desc">Eight steps from first-use setup to reusing verified answers in the next application.</desc>
<defs><marker id="arrow" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="16" markerHeight="16" orient="auto-start-reverse"><path d="M1 1 L11 6 L1 11" fill="none" stroke="#6f95b5" stroke-width="2"/></marker></defs>
<rect width="{width}" height="{height}" fill="#111111"/>
{''.join(arrows)}
{''.join(cards)}
</svg>
'''

    (HERE / f'{name}.svg').write_text(svg, encoding='utf-8')
    cairosvg.svg2png(
        bytestring=svg.encode('utf-8'),
        write_to=str(HERE / f'{name}.png'),
        output_width=width,
        output_height=height,
    )
    print(HERE / f'{name}.png')


render('workflow-diagram', WIDTH, HEIGHT, wide_positions, wide_arrows)
render('workflow-diagram-compact', 815, 5480, compact_positions, compact_arrows)
