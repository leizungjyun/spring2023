"""Embed TeX math as SVG paths; needs local latex and dvisvgm only when rebuilding."""
from functools import lru_cache
from pathlib import Path
import hashlib
import re
import subprocess
import tempfile

@lru_cache(maxsize=None)
def _render(expression):
    with tempfile.TemporaryDirectory(prefix='deck-math-') as directory:
        root = Path(directory)
        source = (r'\documentclass{article}\usepackage{amsmath,amssymb}'
                  r'\pagestyle{empty}\begin{document}\fontsize{20}{24}\selectfont'
                  r'\(\displaystyle ' + expression + r'\)\end{document}')
        (root / 'math.tex').write_text(source)
        for command in [
            ['latex', '-interaction=nonstopmode', '-halt-on-error', 'math.tex'],
            ['dvisvgm', '--no-fonts', '--exact-bbox', '--bbox=min', '--output=math.svg', 'math.dvi'],
        ]:
            result = subprocess.run(command, cwd=root, capture_output=True, text=True)
            if result.returncode:
                raise RuntimeError(result.stdout + result.stderr)
        svg = (root / 'math.svg').read_text()
    box = re.search(r"viewBox=['\"]([^'\"]+)", svg)[1]
    x, y, w, h = map(float, box.split())
    body = svg[svg.index('>', svg.index('<svg')) + 1:svg.rindex('</svg>')]
    return x, y, w, h, body

def math_svg(expression, cx, cy, size=24, color='#203441'):
    """Center math at (cx, cy), sized like a text font; paths work offline."""
    x, y, w, h, body = _render(expression)
    prefix = 'm' + hashlib.sha1(f'{expression}:{cx}:{cy}'.encode()).hexdigest()[:12]
    body = re.sub(r"(id=|xlink:href=)(['\"])(#?)([^'\"]+)",
                  lambda m: m[1] + m[2] + m[3] + prefix + '-' + m[4], body)
    scale = size / 20
    return (f'<g fill="{color}" transform="translate({cx-w*scale/2:.4f} {cy-h*scale/2:.4f}) '
            f'scale({scale:.4f}) translate({-x:.4f} {-y:.4f})">{body}</g>')

def typeset_physics_svg(svg):
    """Replace math labels in the two translated physics illustrations."""
    labels = {
        'E &lt; U': ('E<U', 58, 112, 17, '#b76b29'),
        'dI/dV &lt; 0': (r'\frac{\mathrm{d}I}{\mathrm{d}V}<0', 143, 120, 16, '#b76b29'),
        'I': ('I', 20, 42, 17, '#203441'),
        'V': ('V', 276, 206, 17, '#203441'),
    }
    def substitute(match):
        key = match[1]
        return math_svg(*labels[key]) if key in labels else match[0]
    svg = re.sub(r'<text\b[^>]*>([^<]*)</text>', substitute, svg)
    if 'xmlns:xlink=' not in svg:
        svg = svg.replace('<svg ', '<svg xmlns:xlink="http://www.w3.org/1999/xlink" ', 1)
    return svg
