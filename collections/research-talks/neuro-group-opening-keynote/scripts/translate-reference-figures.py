"""Translate the reference deck's dark-theme figures for this white-theme deck.

The reference deck (collections/external-presentations/2026-09-15-neuro) draws its
figures for a dark theme: dark shape fills, near-white labels, bright accents. This
script copies six of them into media/diagrams/, re-maps the palette onto this deck's
tokens, and replaces the Chinese labels with English ones. Illustration geometry is
preserved; mathematical labels in the physics figures are rendered as TeX SVG paths.

Run from anywhere:  python3 scripts/translate-reference-figures.py
Re-running is safe; it overwrites its own output and never writes the originals.
"""
import re
from math_typeset import typeset_physics_svg
from pathlib import Path

deck = Path(__file__).resolve().parents[1]
source = deck.parents[1] / 'external-presentations' / '2026-09-15-neuro' / 'images'
target = deck / 'media' / 'diagrams'

# Dark-theme hex -> this deck's white-theme equivalent. Shape fills become light
# panels, light labels become dark text, and the two accents become the deck's blue
# and amber.
PALETTE = {
    '#20272d': '#eff5f8',   # filled box / panel
    '#263946': '#e2ecf2',   # filled shape (camera body, barrier, hand)
    '#151e25': '#203441',   # near-black fill that should stay dark
    '#3c3328': '#fbf1e4',   # shaded amber region
    '#3b4750': '#b9cbd6',   # heavy dark stroke, e.g. a ground line
    '#f5f7fa': '#203441',   # label text
    '#aab7c3': '#607582',   # secondary text and axes
    '#42affa': '#00649e',   # accent blue
    '#ffbf69': '#b76b29',   # accent amber
}
FONT = ('PingFang SC,Microsoft YaHei,sans-serif', 'Arial,Helvetica,sans-serif')
FONT_SPACED = ('PingFang SC, Microsoft YaHei, sans-serif', 'Arial, Helvetica, sans-serif')

# Old label -> English label, per file. Each replacement is checked, so a change in
# the reference deck fails loudly here instead of shipping a half-translated figure.
FIGURES = {
    'nonlinearity.svg': ('device-nonlinearity-chain.svg', [
        ('线性变换', 'Linear transform'),
        ('非线性变换', 'Nonlinear transform'),
        ('下一层', 'Next layer'),
        ('技术核心：器件非线性', 'Technology acts here: device nonlinearity'),
        ('<title>nonlinearity</title>', '<title>Device nonlinearity chain</title>'),
    ]),
    'quantum-tunneling.svg': ('quantum-tunnelling.svg', [
        ('量子隧穿原理示意，不按比例', 'Schematic of quantum tunnelling, not to scale'),
        ('>量子隧穿<', '>Quantum tunnelling<'),
        ('>势垒<', '>Barrier<'),
        ('>入射<', '>Incident<'),
        ('>透射<', '>Transmitted<'),
    ]),
    'tunnel-diode-iv.svg': ('tunnel-diode-iv.svg', [
        ('隧道二极管正向 I–V 定性曲线：峰值、负微分电阻区与谷值；非实测数据',
         'Qualitative forward I-V curve of a tunnel diode: peak, negative differential resistance region, valley. Not measured data.'),
        ('>隧道二极管 I–V<', '>Tunnel diode I-V<'),
        ('>峰值<', '>Peak<'),
        ('>谷值<', '>Valley<'),
        ('>负微分电阻<', '>Negative differential resistance<'),
        ('定性示意 · 非实测', 'Schematic, not measured'),
    ]),
    'application-autofocus.svg': ('application-autofocus.svg', [
        ('消费级相机与高速公路监控摄像头', 'A consumer camera and a highway enforcement camera'),
        ('>消费级相机<', '>Consumer camera<'),
        ('>高速公路监控<', '>Highway capture<'),
    ]),
    'application-hypersonic.svg': ('application-guidance.svg', [
        ('制导应用：迫击炮与高超音速导弹', 'Guidance applications: mortar and hypersonic missile, as application categories'),
        ('应用类别示意。量大与高端为拟议定位，不表示已核实的市场数量或性能。',
         'Application categories only. Volume and high end are proposed positions, not verified market sizes or performance.'),
        ('>迫击炮<', '>Mortar<'),
        ('>量大<', '>Volume<'),
        ('>高超音速<', '>Hypersonic<'),
        ('>导弹<', '>missile<'),
        ('>高端<', '>High end<'),
    ]),
    'application-touch.svg': ('application-touch.svg', [
        ('触觉感知与柔性机械臂控制两个子图', 'Two panels: touch sensing and soft robotic-arm control'),
        ('>触觉<', '>Touch<'),
        ('>柔性机械臂控制<', '>Soft robotic-arm control<'),
    ]),
}

target.mkdir(parents=True, exist_ok=True)
written = []
for name, (out_name, labels) in FIGURES.items():
    text = (source / name).read_text()
    for old, new in PALETTE.items():          # colours first, then labels
        text = text.replace(old, new)
    text = text.replace(*FONT_SPACED).replace(*FONT)
    # One pass over all labels, longest first, so that replacing 线性变换 cannot also
    # consume the tail of 非线性变换. Each source label must be present exactly once.
    mapping = dict(labels)
    pattern = re.compile('|'.join(re.escape(k) for k in sorted(mapping, key=len, reverse=True)))
    for old in mapping:
        assert old in text, f'{name}: {old} not found'
    text = pattern.sub(lambda m: mapping[m.group(0)], text)
    for old in mapping:
        assert old not in text, f'{name}: {old} survived the pass'
    assert not any('一' <= c <= '鿿' for c in text), f'{name}: Chinese text left'
    if out_name in {'quantum-tunnelling.svg', 'tunnel-diode-iv.svg'}:
        text = typeset_physics_svg(text)
    (target / out_name).write_text(text)
    written.append(out_name)

print('Translated to the white theme:', ', '.join(written))
