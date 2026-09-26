from pathlib import Path
import math
from math_typeset import math_svg
p=Path(__file__).resolve().parents[1] / 'media/diagrams'
p.mkdir(parents=True, exist_ok=True)
B='#00649e'; T='#203441'; M='#607582'; A='#b76b29'; L='#d5e2e9'; P='#eff5f8'
def svg(name,w,h,body):
 (p/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" role="img"><style>text{{font-family:Arial,sans-serif;fill:{T}}}.small{{font-size:17px;fill:{M}}}.label{{font-size:22px;font-weight:600}}.blue{{fill:{B}}}</style><defs><marker id="a" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto-start-reverse"><path d="M0 0L9 4.5L0 9" fill="none" stroke="{B}" stroke-width="1.5"/></marker><marker id="amber" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto-start-reverse"><path d="M0 0L9 4.5L0 9" fill="none" stroke="{A}" stroke-width="1.5"/></marker></defs>'+body+'</svg>')
def diagonal_memristor(x,y,dx,dy):
 # The branch and device share one diagonal between a word-line tap and bit line.
 angle=math.degrees(math.atan2(dy,dx))
 return (f'<path d="M{x-dx} {y}L{x} {y+dy}" fill="none" stroke="{A}" stroke-width="2"/>'
         f'<circle cx="{x-dx}" cy="{y}" r="3.5" fill="{B}"/>'
         f'<circle cx="{x}" cy="{y+dy}" r="3.5" fill="{B}"/>'
         f'<g transform="translate({x-dx/2:g} {y+dy/2:g}) rotate({angle:.1f})">'
         f'<rect x="-20" y="-11" width="40" height="22" fill="#fff4e8" stroke="{A}" stroke-width="2"/>'
         f'<path d="M-20 0h8v-6h8v12h8V-6h8v6h8" fill="none" stroke="{A}" stroke-width="1.7"/>'
         '</g>')
svg('ai-pillars.svg',520,350,f'''<path d="M70 44V282" stroke="{L}" stroke-width="4"/>
<circle cx="70" cy="55" r="19" fill="{B}"/><circle cx="70" cy="165" r="19" fill="{B}"/><circle cx="70" cy="275" r="19" fill="{A}"/>
<text x="110" y="56" class="label">Algorithms</text><text x="110" y="84" class="small">Frontier model performance is converging</text>
<text x="110" y="166" class="label">Data</text><text x="110" y="194" class="small">Access and quality depend on the domain</text>
<rect x="99" y="234" width="409" height="86" rx="5" fill="{P}"/>
<text x="110" y="266" class="label blue">Compute</text><text x="110" y="296" class="small">Hardware capacity remains uneven</text>''')
# The von Neumann organization: memory above, processor below, and the narrow path
# every weight and activation has to travel between them. Input and output sit on the
# processor row, because that is where data enters and leaves the machine.
svg('memory-traffic.svg',560,300,f'''<rect x="132" y="8" width="296" height="80" rx="10" fill="{P}" stroke="{B}" stroke-width="2"/><text x="280" y="56" text-anchor="middle" class="label">Memory</text>
<rect x="186" y="118" width="188" height="64" rx="12" fill="#fff4e8" stroke="{A}" stroke-width="2" stroke-dasharray="7 5"/>
<path d="M216 92V204" fill="none" stroke="{A}" stroke-width="3" marker-end="url(#amber)"/><path d="M344 204V92" fill="none" stroke="{A}" stroke-width="3" marker-end="url(#amber)"/>
<text x="280" y="156" text-anchor="middle" font-size="17" font-weight="600" fill="{A}">Move data</text>
<rect x="132" y="212" width="296" height="80" rx="10" fill="{P}" stroke="{B}" stroke-width="2"/><text x="280" y="260" text-anchor="middle" class="label">Processor</text>
<rect x="2" y="212" width="96" height="80" rx="10" fill="#fff" stroke="{B}" stroke-width="2"/><text x="50" y="260" text-anchor="middle" class="label">Input</text>
<rect x="462" y="212" width="96" height="80" rx="10" fill="#fff" stroke="{B}" stroke-width="2"/><text x="510" y="260" text-anchor="middle" class="label">Output</text>
<path d="M100 252H128" fill="none" stroke="{A}" stroke-width="2.5" marker-end="url(#amber)"/><path d="M432 252H460" fill="none" stroke="{A}" stroke-width="2.5" marker-end="url(#amber)"/>''')
svg('edge-loop.svg',520,185,f'''<path d="M97 83H211M314 83H426" stroke="{B}" stroke-width="3" marker-end="url(#a)"/>
<circle cx="60" cy="83" r="35" fill="{P}" stroke="{B}" stroke-width="2"/><rect x="32" y="66" width="54" height="33" rx="6" fill="none" stroke="{B}" stroke-width="2"/><circle cx="59" cy="82" r="11" fill="none" stroke="{B}" stroke-width="2"/>
<rect x="218" y="43" width="89" height="80" rx="9" fill="{P}" stroke="{B}" stroke-width="2"/><text x="262" y="91" text-anchor="middle" class="label blue">AI</text>
<circle cx="465" cy="83" r="35" fill="{P}" stroke="{B}" stroke-width="2"/><path d="M443 90l17-31 21 18-17 22" fill="none" stroke="{B}" stroke-width="3"/>
<text x="60" y="153" text-anchor="middle" class="small">Sense</text><text x="262" y="153" text-anchor="middle" class="small">Infer</text><text x="465" y="153" text-anchor="middle" class="small">Act</text>''')
# Three edge settings around local inference. Conceptual: no product-specific
# latency, battery or energy claim is made by this figure.
# Three edge settings, each named for the constraint that binds it — standby power,
# loop latency, daily energy — rather than by product category. Conceptual targets,
# not measured results.
svg('edge-applications.svg',560,290,f'''<g fill="{P}"><rect x="6" y="6" width="172" height="266" rx="14"/><rect x="194" y="6" width="172" height="266" rx="14"/><rect x="382" y="6" width="172" height="266" rx="14"/></g>
<g fill="none" stroke="{B}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round">
<rect x="80" y="44" width="24" height="46" rx="12"/><path d="M70 76a22 22 0 0 0 44 0"/><path d="M92 98v10M82 108h20"/>
<rect x="252" y="60" width="56" height="46" rx="11"/><circle cx="280" cy="83" r="13"/><circle cx="280" cy="83" r="5"/><path d="M266 60l6-11h16l6 11"/>
<rect x="446" y="50" width="44" height="52" rx="14"/><path d="M458 50V34h20v16M458 102v16h20v-16"/><path d="M456 76h7l4-8 6 16 4-8h7"/>
</g>
<g text-anchor="middle"><text x="92" y="152" font-size="17" font-weight="600">Always-on audio</text><text x="280" y="152" font-size="17" font-weight="600">Perception loop</text><text x="468" y="152" font-size="17" font-weight="600">On-body sensing</text></g>
<path d="M40 180H144M228 180H332M416 180H520" stroke="{L}" stroke-width="1.5"/>
<g class="small" font-size="15" text-anchor="middle"><text x="92" y="208">Listening all day</text><text x="92" y="232">on microwatts</text>
<text x="280" y="208">Answers within</text><text x="280" y="232">one frame time</text>
<text x="468" y="208">Months of runtime</text><text x="468" y="232">on a coin cell</text></g>''')
# Conceptual neural morphology and local weighted currents, not anatomical or measured.
brain=f'''<path d="M137 206C91 219 63 178 76 144C47 113 65 73 102 69C101 34 151 13 177 39C211 9 257 26 265 59C306 49 340 83 326 117C360 151 336 192 303 194C288 226 244 229 222 209C197 239 150 239 137 206Z" fill="{P}" stroke="{B}" stroke-width="3"/>
<path d="M178 40Q164 102 194 141Q171 167 184 226M104 70Q151 73 145 121Q102 117 78 145M266 60Q219 63 229 111Q279 113 301 84M326 119Q278 130 285 163Q253 181 224 160M137 207Q114 169 146 150" fill="none" stroke="{B}" stroke-width="2"/>
<text x="205" y="295" text-anchor="middle" style="font-size:54px;font-weight:600;fill:{B}">~20 W</text><text x="205" y="325" text-anchor="middle" class="small">whole-brain metabolic power</text>'''
svg('brain-power.svg',410,350,brain)
# The in-memory array that used to sit beside the synaptic figure is kept in the
# generator but is no longer referenced by any slide.
body=f'<text x="260" y="28" text-anchor="middle" class="label">Stored weights participate in computation</text>'
for y in [85,145,205]:
 body+=f'<path d="M35 {y}H460" stroke="{B}" stroke-width="2" marker-end="url(#a)"/>'
 for x in [150,260,370]:body+=f'<rect x="{x-11}" y="{y-11}" width="22" height="22" rx="3" fill="{A}"/>'
for x in [150,260,370]:body+=f'<path d="M{x} 56V266" stroke="{B}" stroke-width="2" marker-end="url(#a)"/>'
body+=f'<text x="260" y="304" text-anchor="middle" class="small">Local state × input → parallel summation</text><text x="260" y="337" text-anchor="middle" class="small">Less shuttling · shorter signal paths</text>'
svg('in-memory.svg',520,355,body)
svg('power-budget.svg',520,250,f'''<rect x="105" y="40" width="310" height="128" rx="16" fill="{P}" stroke="{B}" stroke-width="3"/><rect x="415" y="77" width="18" height="53" rx="3" fill="{B}"/>
<rect x="121" y="56" width="83" height="96" rx="4" fill="{B}"/><rect x="210" y="56" width="83" height="96" rx="4" fill="{B}" opacity=".55"/><rect x="299" y="56" width="100" height="96" rx="4" fill="{B}" opacity=".16"/>
<path d="M259 63l-26 44h25l-10 37 36-49h-26Z" fill="white"/>
<text x="260" y="218" text-anchor="middle" class="label">A fixed energy and thermal budget</text>''')
# National flags for the U.S.-China compute framing. Geometry follows each flag's official proportions.
import math
def star(cx,cy,r,rot=-90):
 pts=[]
 for i in range(10):
  a=math.radians(rot+i*36); rr=r if i%2==0 else r*.382
  pts.append(f'{cx+rr*math.cos(a):.2f},{cy+rr*math.sin(a):.2f}')
 return ' '.join(pts)
us=['<rect width="76" height="40" fill="#fff"/>']
for i in range(0,13,2):us.append(f'<rect y="{i*40/13:.3f}" width="76" height="{40/13:.3f}" fill="#b22234"/>')
us.append(f'<rect width="30.4" height="{7*40/13:.3f}" fill="#3c3b6e"/>')
for row in range(9):
 y=(row+.5)*(7*40/13)/9
 for c in range(6 if row%2==0 else 5):
  x=(c+.5)*30.4/6 if row%2==0 else (c+1)*30.4/6
  us.append(f'<polygon points="{star(x,y,1.15)}" fill="#fff"/>')
svg('flag-us.svg',76,40,''.join(us))
cn=[f'<rect width="60" height="40" fill="#de2910"/>',f'<polygon points="{star(10,10,6)}" fill="#ffde00"/>']
for x,y in [(20,4),(24,8),(24,14),(20,18)]:
 cn.append(f'<polygon points="{star(x,y,2,math.degrees(math.atan2(10-y,10-x)))}" fill="#ffde00"/>')
svg('flag-china.svg',60,40,''.join(cn))
# English translation of the reference deck's synaptic-state-computing.svg. The drawing
# is the same geometry as the reference, un-distorted, with the key moved to the right
# so the figure reads as one band across the top of its slide.
svg('synaptic-state.svg',1000,245,f'''<g transform="translate(2,8) scale(.96)">
<g font-size="17" fill="{M}"><text x="28" y="26">Three presynaptic axons</text><text x="352" y="26">One shared dendrite</text></g>
<g fill="none" stroke-linecap="round">
<g stroke="{M}" stroke-width="4" opacity=".55"><path d="M30 65C101 65 174 58 260 75"/><path d="M30 126H257"/><path d="M30 189C112 189 179 197 257 180"/></g>
<g stroke="{B}" stroke-width="2.5" marker-end="url(#a)"><path d="M106 64C142 62 179 62 213 67"/><path d="M105 126H214"/><path d="M106 191C147 193 181 193 215 188"/></g>
</g>
<g fill="{A}"><circle cx="279" cy="78" r="15" opacity=".10"/><circle cx="279" cy="127" r="21" opacity=".12"/><circle cx="279" cy="179" r="27" opacity=".14"/></g>
<g fill="#fff" stroke="{A}" stroke-width="2"><circle cx="279" cy="78" r="8"/><circle cx="279" cy="127" r="12"/><circle cx="279" cy="179" r="16"/></g>
<g fill="{A}"><circle cx="279" cy="78" r="3"/><circle cx="279" cy="127" r="5"/><circle cx="279" cy="179" r="8"/></g>
<path d="M361 51C365 78 359 97 365 115C372 128 406 127 445 117L451 139C408 134 381 135 373 148C365 163 365 183 363 203L352 203C350 181 351 163 357 144C359 137 359 127 354 118C349 98 355 75 351 53Z" fill="{P}" stroke="{M}" stroke-width="1.6"/>
<g fill="none" stroke="{M}" stroke-width="5" stroke-linecap="round"><path d="M318 80C337 78 344 85 356 88"/><path d="M322 127C337 127 345 127 360 130"/><path d="M324 176C342 179 348 171 358 167"/></g>
<path d="M445 118C448 95 462 78 485 78C509 78 526 96 529 118C531 128 540 130 558 130L558 136C539 136 531 137 527 148C520 168 501 180 480 176C455 173 442 154 445 134Z" fill="{P}" stroke="{M}" stroke-width="2"/>
<ellipse cx="486" cy="127" rx="17" ry="19" fill="{L}"/>
<g fill="none" stroke="{B}" stroke-width="2.7" stroke-linecap="round" marker-end="url(#a)"><path d="M264 78H331"/><path d="M262 127H335"/><path d="M260 179Q293 180 336 176"/><path d="M358 98Q357 110 366 119"/><path d="M358 156Q360 145 369 139"/><path d="M387 130H435"/></g>
<g font-size="17" fill="{T}"><text x="446" y="211">Neuron soma</text><text x="300" y="232" fill="{B}">Synaptic integration</text></g>
</g>
<g transform="translate(596,34)">
<rect x="0" y="2" width="15" height="15" rx="3" fill="{A}"/><text x="26" y="15" font-size="19" font-weight="600" fill="{A}">Memory</text>
<text x="26" y="40" font-size="16" fill="{M}">synapse presence and strength</text>
<rect x="0" y="70" width="15" height="15" rx="3" fill="{B}"/><text x="26" y="83" font-size="19" font-weight="600" fill="{B}">Compute</text>
<text x="26" y="108" font-size="16" fill="{M}">synaptic integration</text>
<rect x="0" y="136" width="380" height="64" rx="9" fill="{P}"/>
<text x="18" y="162" font-size="17" font-weight="600">Stored state directly</text>
<text x="18" y="186" font-size="17" font-weight="600">participates in signaling</text>
</g>''')
# Comparison of a separated architecture with a compute-in-memory array. Conceptual:
# peripheral circuits are omitted and no measured performance is claimed.
svg('separated-vs-in-memory.svg',1140,300,f'''<text x="280" y="30" text-anchor="middle" font-size="26" font-weight="600">Separate memory and processing</text>
<text x="860" y="30" text-anchor="middle" font-size="26" font-weight="600" fill="{B}">In-memory computing</text>
<rect x="5" y="196" width="115" height="54" rx="10" fill="{P}" stroke="{M}" stroke-width="2"/><text x="62" y="230" text-anchor="middle" font-size="20">Input</text>
<rect x="440" y="196" width="115" height="54" rx="10" fill="{P}" stroke="{M}" stroke-width="2"/><text x="497" y="230" text-anchor="middle" font-size="20">Output</text>
<path d="M122 223H141" fill="none" stroke="{B}" stroke-width="3" marker-end="url(#a)"/><path d="M423 223H437" fill="none" stroke="{B}" stroke-width="3" marker-end="url(#a)"/>
<rect x="146" y="52" width="272" height="72" rx="10" fill="{P}" stroke="{B}" stroke-width="2"/><text x="282" y="96" text-anchor="middle" font-size="21">Memory</text>
<rect x="146" y="196" width="272" height="72" rx="10" fill="{P}" stroke="{B}" stroke-width="2"/><text x="282" y="240" text-anchor="middle" font-size="21">Processor</text>
<path d="M218 192V130" fill="none" stroke="{A}" stroke-width="3" marker-end="url(#amber)"/><path d="M346 130V192" fill="none" stroke="{A}" stroke-width="3" marker-end="url(#amber)"/>
<text x="282" y="166" text-anchor="middle" font-size="18" font-weight="600" fill="{A}">Move data</text>
<g transform="translate(580,0)">
<rect x="5" y="196" width="115" height="54" rx="10" fill="{P}" stroke="{M}" stroke-width="2"/><text x="62" y="230" text-anchor="middle" font-size="20">Input</text>
<rect x="440" y="196" width="115" height="54" rx="10" fill="{P}" stroke="{M}" stroke-width="2"/><text x="497" y="230" text-anchor="middle" font-size="20">Output</text>
<path d="M122 223H141" fill="none" stroke="{B}" stroke-width="3" marker-end="url(#a)"/><path d="M423 223H437" fill="none" stroke="{B}" stroke-width="3" marker-end="url(#a)"/>
<rect x="146" y="52" width="272" height="216" rx="12" fill="#fff4e8" stroke="{A}" stroke-width="3"/>
<text x="282" y="88" text-anchor="middle" font-size="21" font-weight="600">Compute-in-memory array</text>
<g fill="{P}" stroke="{B}" stroke-width="2"><rect x="190" y="110" width="58" height="44" rx="6"/><rect x="253" y="110" width="58" height="44" rx="6"/><rect x="316" y="110" width="58" height="44" rx="6"/><rect x="190" y="164" width="58" height="44" rx="6"/><rect x="253" y="164" width="58" height="44" rx="6"/><rect x="316" y="164" width="58" height="44" rx="6"/></g>
<g fill="{B}" font-size="19" font-weight="600" text-anchor="middle"><text x="219" y="139">w</text><text x="282" y="139">w</text><text x="345" y="139">w</text><text x="219" y="193">w</text><text x="282" y="193">w</text><text x="345" y="193">w</text></g>
<text x="282" y="244" text-anchor="middle" font-size="18" font-weight="600" fill="{A}">Weights stored in place</text>
</g>
<path d="M570 40V284" stroke="{L}" stroke-width="2" stroke-dasharray="5 7"/>''')
# Redrawn from media/figures/accuracy-against-errors.pdf, the supplied measured figure:
# every marker below was read off the rendered figure, x = weight error (%), y = accuracy (%).
# The supplied figure plots eight parameter counts; these three — the smallest, the second
# smallest and the largest — carry the trend without crowding at slide scale.
TOL=[('26 506',A,[(1,86.78),(5,86.52),(9,86.16),(13,85.67),(17,85.40),(21,84.73),(26,84.00),(31,82.28),(36,81.04),(41,78.72),(46,78.74)]),
     ('55 050','#7ca0b3',[(1,87.93),(5,87.80),(9,87.60),(13,87.46),(17,87.02),(21,86.85),(26,86.79),(31,86.45),(36,85.44),(41,85.15),(46,84.14)]),
     ('1 863 690',B,[(1,88.44),(5,88.36),(9,88.20),(13,88.21),(17,87.97),(21,87.89),(26,87.95),(31,87.63),(36,87.52),(41,87.20),(46,87.43)])]
def tox(v): return 72+v*8.48
def toy(v): return 40+(90-v)*22.5
tol_grid=''.join(f'<path d="M72 {toy(v):.1f}H496" stroke="#e9eff3" stroke-width="1"/>' for v in range(78,91,2))
tol_grid+=''.join(f'<path d="M{tox(v):.1f} 40V310" stroke="#e9eff3" stroke-width="1"/>' for v in range(0,51,10))
tol_ticks=''.join(f'<text x="62" y="{toy(v)+5:.1f}" font-size="15" fill="{M}" text-anchor="end">{v}</text>' for v in range(78,91,2))
tol_ticks+=''.join(f'<text x="{tox(v):.1f}" y="330" font-size="15" fill="{M}" text-anchor="middle">{v}</text>' for v in range(0,51,10))
tol_lines=''
for name,colour,pts in TOL:
    tol_lines+=f'<path d="M'+'L'.join(f'{tox(x):.1f} {toy(y):.1f}' for x,y in pts)+f'" fill="none" stroke="{colour}" stroke-width="3" stroke-linejoin="round"/>'
    tol_lines+=''.join(f'<circle cx="{tox(x):.1f}" cy="{toy(y):.1f}" r="4.6" fill="{colour}"/>' for x,y in pts)
    ey=toy(pts[-1][1])
    tol_lines+=f'<path d="M{tox(46)+9:.1f} {ey:.1f}H496" stroke="{colour}" stroke-width="1.6"/>'
    tol_lines+=f'<text x="504" y="{ey+5:.1f}" font-size="16">{name}</text>'
svg('accuracy-tolerance.svg',720,380,f'''<text x="72" y="24" font-size="16" fill="{M}">Accuracy (%)</text>
<text x="504" y="24" font-size="14" fill="{M}">parameters</text>
{tol_grid}
<path d="M72 40V310M72 310H496" fill="none" stroke="{L}" stroke-width="2"/>
{tol_ticks}
<text x="284" y="358" font-size="16" fill="{M}" text-anchor="middle">Weight error (%)</text>
{tol_lines}
<text x="392" y="72" font-size="15" fill="{B}" text-anchor="middle">&#8722;1 point over the full range</text>
<text x="318" y="272" font-size="15" fill="{A}" text-anchor="middle">&#8722;8 points</text>''')
# Speech cloud for the closing quotation: a flat white cloud outline with a trail of
# shrinking circles pointing left, at the speaker's portrait. Drawn at the exact size it
# is used, 944x150, so the CSS can place it 1:1 without distorting the scallops.
def cloud(cx,cy,rx,ry,tip,base=(168,198)):
    # One smooth oval, broken at two points on its left end, with a straight wedge to the
    # tip: the simple speech bubble, not a scalloped border. The tail points left and up,
    # at the speaker's head in the portrait beside it.
    def pt(a):
        t=math.radians(a); return (cx+rx*math.cos(t), cy+ry*math.sin(t))
    x1,y1=pt(base[0]); x2,y2=pt(base[1])
    return (f'M{x1:.1f} {y1:.1f}A{rx} {ry} 0 1 0 {x2:.1f} {y2:.1f}'
            f'L{tip[0]} {tip[1]}Z')
svg('speech-cloud.svg',944,150,f'''<path d="{cloud(524,75,420,73,(22,32))}" fill="#fff" stroke="{B}" stroke-width="2.5"/>''')
# In-SRAM and in-DRAM computing: both add computation to an array the design already
# has. The SRAM cell is coarse and the process is ordinary CMOS, so the computation is
# added to the lines the cells already share; the DRAM cell is dense, so a single row
# holds too little to compute with, and the logic comes from activating several rows at
# once. Conceptual schematics: no array size, process node or energy number is implied.
def grid(x0,y0,cols,rows,w,h,dx,dy,sw=1.2,hl=()):
    out=[]
    for r in range(rows):
        for c in range(cols):
            on = r in hl
            out.append(f'<rect x="{x0+c*(w+dx)}" y="{y0+r*(h+dy)}" width="{w}" height="{h}" rx="2"'
                       f' fill="{"#fff4e8" if on else "#fff"}" stroke="{A if on else B}"'
                       f' stroke-width="{1.6 if on else sw}"/>')
    return '<g>'+''.join(out)+'</g>'
svg('sram-computing.svg',460,200,f'''<rect x="4" y="6" width="452" height="132" rx="12" fill="{P}" stroke="{B}" stroke-width="2"/>
<text x="20" y="34" font-size="17" fill="{M}">SRAM array — 6T cells, ordinary CMOS</text>
{grid(30,46,8,2,36,26,14,14,1.5)}
<path d="M173 38V158M323 38V158" stroke="{A}" stroke-width="3"/>
<rect x="86" y="160" width="300" height="34" rx="8" fill="#fff4e8" stroke="{A}" stroke-width="2"/>
<text x="236" y="183" text-anchor="middle" font-size="17" font-weight="600" fill="{A}">compute on the array's own bitlines</text>''')
svg('dram-computing.svg',460,200,f'''<rect x="24" y="6" width="400" height="132" rx="12" fill="{P}" stroke="{B}" stroke-width="2"/>
<text x="40" y="34" font-size="17" fill="{M}">DRAM array — one transistor, one capacitor</text>
{grid(44,46,12,4,20,13,12,7,1.1,hl=(0,1))}
<path d="M40 52H12V177H80" fill="none" stroke="{A}" stroke-width="3" marker-end="url(#amber)"/>
<rect x="86" y="160" width="300" height="34" rx="8" fill="#fff4e8" stroke="{A}" stroke-width="2"/>
<text x="236" y="183" text-anchor="middle" font-size="17" font-weight="600" fill="{A}">activate several rows at once</text>''')
# ACIM versus DCIM: same local dot product, different accumulation mechanisms.
cim_cells=''
for x in [72,184,296,408]:
 cim_cells+=f'<rect x="{x}" y="111" width="82" height="57" rx="5" fill="white" stroke="{B}" stroke-width="2"/><text x="{x+41}" y="134" text-anchor="middle" font-size="16">product</text>' + math_svg('w_i x_i', x+41, 156, 21)
for x in [660,772,884,996]:
 cim_cells+=f'<rect x="{x}" y="111" width="82" height="57" rx="5" fill="white" stroke="{A}" stroke-width="2"/><text x="{x+41}" y="134" text-anchor="middle" font-size="16">product</text>' + math_svg('w_i x_i', x+41, 156, 21) + f'<path d="M{x+41} 171V216" stroke="{A}" stroke-width="2" marker-end="url(#amber)"/><circle cx="{x+41}" cy="224" r="4" fill="{A}"/>'
svg('acim-vs-dcim.svg',1120,470,f'''{math_svg('y=\\sum_i x_i w_i',560,25,25)}<text x="695" y="31" font-size="20">· weights stay local in both</text>
<rect x="8" y="48" width="534" height="341" rx="12" fill="{P}"/>
<rect x="578" y="48" width="534" height="341" rx="12" fill="#fff4e8"/>
<text x="275" y="84" text-anchor="middle" font-size="25" font-weight="600">DCIM · digital compute-in-memory</text>
<text x="845" y="84" text-anchor="middle" font-size="25" font-weight="600">ACIM · analog compute-in-memory</text>
{cim_cells}
<path d="M113 168V185L169 213 M225 168V185L169 213 M337 168V185L393 213 M449 168V185L393 213 M169 239L281 281 M393 239L281 281" fill="none" stroke="{B}" stroke-width="2"/>
<circle cx="169" cy="225" r="19" fill="white" stroke="{B}" stroke-width="2"/><circle cx="393" cy="225" r="19" fill="white" stroke="{B}" stroke-width="2"/><circle cx="281" cy="287" r="19" fill="white" stroke="{B}" stroke-width="2"/>
{math_svg('+',169,225,28)}{math_svg('+',393,225,28)}{math_svg('+',281,287,28)}
<text x="72" y="290" font-size="18">Adder tree</text>
<path d="M281 309V326" stroke="{B}" stroke-width="2" marker-end="url(#a)"/>
<text x="281" y="352" text-anchor="middle" font-size="23">Digital result</text>
<path d="M685 224H1053" stroke="{A}" stroke-width="4"/>

<text x="704" y="250" font-size="18">Current / charge sum</text>
<path d="M971 225V276" stroke="{A}" stroke-width="2" marker-end="url(#amber)"/>
<rect x="929" y="282" width="84" height="39" rx="5" fill="white" stroke="{A}" stroke-width="2"/>
<text x="971" y="308" text-anchor="middle" font-size="21">ADC</text>
<text x="729" y="303" text-anchor="middle" font-size="21" font-weight="600">No in-array</text>
<text x="729" y="330" text-anchor="middle" font-size="21" font-weight="600">adder tree</text>
<path d="M971 323V335" stroke="{A}" stroke-width="2" marker-end="url(#amber)"/>
<text x="971" y="363" text-anchor="middle" font-size="21">Digital result</text>
<text x="275" y="378" text-anchor="middle" font-size="17">Logic gates + multi-stage accumulation</text>
<rect x="12" y="411" width="526" height="48" rx="7" fill="{P}"/>
<text x="275" y="441" text-anchor="middle" font-size="20">Strength: exact arithmetic at the chosen bit width</text>
<rect x="582" y="411" width="526" height="48" rx="7" fill="#fff4e8"/>
<text x="845" y="441" text-anchor="middle" font-size="21" font-weight="600">ACIM opportunity: lower core energy + area</text>''')
# Memristor branches connect row voltages to column current collectors.
cross_body=''
for j,x in enumerate([180,310,440]):
 cross_body+=f'<path d="M{x} 70V323" stroke="{B}" stroke-width="2.5"/><path d="M{x} 323V346" stroke="{B}" stroke-width="2" marker-end="url(#a)"/>' + math_svg('I_'+str(j+1), x, 369, 25)
for i,y in enumerate([100,180,260]):
 cross_body+=f'<path d="M62 {y}H482" stroke="white" stroke-width="9"/><path d="M62 {y}H482" stroke="{A}" stroke-width="2.5"/>' + math_svg('v_'+str(i+1), 42, y, 25)
 for j,x in enumerate([180,310,440]):
  cross_body+=diagonal_memristor(x,y,65,37)
  # Put conductance labels below each branch, clear of wires and junctions.
  cross_body+=math_svg('G_{'+str(i+1)+str(j+1)+'}', x-48, y+51, 19)
# A branch-current arrow occupies the free space to the right of the last cell.
cross_body+=f'<path d="M458 122V154" stroke="{B}" stroke-width="1.6" marker-end="url(#a)"/>' + math_svg('i_{13}', 490, 140, 20)
svg('memristor-crossbar.svg',540,450,f'''<text x="76" y="33" font-size="23" font-weight="600">Ohm’s law</text>{math_svg('i_{ij}=v_iG_{ij}', 338, 26, 26)}
{cross_body}
<text x="76" y="424" font-size="23" font-weight="600">KCL</text>{math_svg(r'\textstyle I_j=\sum_i i_{ij}=\sum_i v_iG_{ij}', 316, 418, 24)}''')
# Explicit anchors attach + to addition and the dot to scalar multiplication.
# V and F name sets; bold symbols below denote vectors, not scalar entries.
svg('vector-space-physics.svg',540,450,f'''<text x="48" y="33" font-size="23" font-weight="600">Vector space</text>
{math_svg(r'(V,F,+,\cdot)', 360, 26, 32)}
{math_svg(r'V=\mathbb{{R}}^3,\quad F=\mathbb{{R}}', 155, 72, 21)}
<path d="M385 46V91H135V109" fill="none" stroke="{A}" stroke-width="1.7"/>
<path d="M416 46V73H405V109" fill="none" stroke="{B}" stroke-width="1.7"/>
<rect x="12" y="110" width="246" height="226" rx="8" fill="#fff4e8"/>
<rect x="282" y="110" width="246" height="226" rx="8" fill="{P}"/>
<text x="135" y="141" text-anchor="middle" font-size="21" font-weight="600">Vector addition</text>
<text x="405" y="141" text-anchor="middle" font-size="21" font-weight="600">Scalar multiplication</text>
<path d="M48 255H132" stroke="{A}" stroke-width="2" marker-end="url(#amber)"/>
<path d="M132 255L215 183" stroke="{A}" stroke-width="2" marker-end="url(#amber)"/>
<path d="M48 255L215 183" stroke="{B}" stroke-width="2.5" marker-end="url(#a)"/>
{math_svg(r'\mathbf{i}_1', 90, 274, 22, A)}{math_svg(r'\mathbf{i}_2', 207, 236, 22, A)}{math_svg(r'\mathbf{i}_1+\mathbf{i}_2', 114, 193, 22, B)}
<path d="M317 238L382 202" stroke="{A}" stroke-width="2" marker-end="url(#amber)"/>
<path d="M325 267L494 174" stroke="{B}" stroke-width="2.5" marker-end="url(#a)"/>
{math_svg(r'\mathbf{g}_i', 336, 193, 23, A)}{math_svg(r'v_i\mathbf{g}_i', 457, 245, 23, B)}
<text x="36" y="316" font-size="20" font-weight="600">KCL</text>{math_svg(r'\textstyle \mathbf{I}=\sum_i\mathbf{i}_i', 171, 311, 21)}
<text x="297" y="316" font-size="20" font-weight="600">Ohm’s law</text>{math_svg(r'\mathbf{i}_i=v_i\mathbf{g}_i', 459, 309, 21)}
{math_svg(r'\mathbf{I}=\sum_i v_i\mathbf{g}_i=\mathbf{G}^{\mathsf{T}}\mathbf{v}', 270, 381, 29)}
{math_svg(r'\mathbf{g}_i=(G_{i1},G_{i2},G_{i3})^{\mathsf{T}}', 270, 431, 23)}''')
# Regular conceptual fabrics: logic/routing configuration versus conductance programming.
fpga_fabric=f'<rect x="8" y="6" width="544" height="330" rx="10" fill="white" stroke="{L}" stroke-width="2"/>'
# Routing channels meet at switch boxes; connection boxes join CLBs to channels.
for y in [55,135,215,295]:
 fpga_fabric+=f'<path d="M70 {y}H490" stroke="{B}" stroke-width="2"/>'
for x in [70,210,350,490]:
 fpga_fabric+=f'<path d="M{x} 55V295" stroke="{B}" stroke-width="2"/>'
for x in [140,280,420]:
 fpga_fabric+=f'<rect x="{x-28}" y="14" width="56" height="24" rx="3" fill="{P}" stroke="{B}" stroke-width="1.5"/><text x="{x}" y="31" text-anchor="middle" font-size="15">I/O</text><path d="M{x} 38V55" stroke="{B}" stroke-width="2"/>'
for y in [55,135,215,295]:
 for x in [70,210,350,490]:
  fpga_fabric+=f'<rect x="{x-7}" y="{y-7}" width="14" height="14" rx="2" fill="#fff4e8" stroke="{A}" stroke-width="1.7"/><path d="M{x-4} {y+3}L{x+4} {y-3}" stroke="{A}" stroke-width="1.5"/>'
for y in [72,152,232]:
 for x in [96,236,376]:
  fpga_fabric+=f'<path d="M{x-26} {y+23}H{x} M{x+88} {y+23}H{x+114}" stroke="{B}" stroke-width="2"/><rect x="{x-29}" y="{y+20}" width="6" height="6" fill="{A}"/><rect x="{x+111}" y="{y+20}" width="6" height="6" fill="{A}"/><rect x="{x}" y="{y}" width="88" height="46" rx="5" fill="{P}" stroke="{B}" stroke-width="1.8"/><text x="{x+44}" y="{y+18}" text-anchor="middle" font-size="16" font-weight="600">CLB</text><text x="{x+44}" y="{y+37}" text-anchor="middle" font-size="14">LUT + FF</text>'
fpga_fabric+=f'<text x="280" y="322" text-anchor="middle" font-size="16">Logic blocks + programmable interconnect</text><rect x="69" y="351" width="14" height="14" rx="2" fill="#fff4e8" stroke="{A}" stroke-width="1.7"/><text x="94" y="363" font-size="16">Switch box</text><text x="258" y="363" font-size="16">CLB: lookup tables + flip-flops</text>'
svg('fpga-fabric.svg',560,375,fpga_fabric)
fpma=f'<rect x="8" y="6" width="544" height="330" rx="10" fill="white" stroke="{L}" stroke-width="2"/><text x="157" y="32" font-size="18">Program conductances</text>' + math_svg('G_{ij}', 374, 26, 21)
for j,x in enumerate([210,350,490]):
 fpma+=f'<path d="M{x} 53V291" stroke="{B}" stroke-width="2.5"/><path d="M{x} 291V307" stroke="{B}" stroke-width="1.6" marker-end="url(#a)"/>' + math_svg('I_'+str(j+1), x, 323, 22)
for i,y in enumerate([75,155,235]):
 fpma+=f'<path d="M72 {y}H515" stroke="white" stroke-width="9"/><path d="M72 {y}H515" stroke="{B}" stroke-width="2.5"/>' + math_svg('v_'+str(i+1), 48, y, 23)
 for j,x in enumerate([210,350,490]):
  fpma+=diagonal_memristor(x,y,82,40)
  fpma+=math_svg('G_{'+str(i+1)+str(j+1)+'}', x-65, y+50, 17)
fpma+=f'<rect x="137" y="348" width="36" height="20" fill="#fff4e8" stroke="{A}" stroke-width="1.6"/><path d="M137 358h7v-5h7v10h8v-10h7v5h7" stroke="{A}" stroke-width="1.4" fill="none"/><text x="187" y="363" font-size="16">Programmable conductance</text>'
svg('fpma-array.svg',560,375,fpma)
# Training and inference are separated in practice: one side changes the weights inside
# a loop, the other reads fixed weights along a straight path, and the weights cross the
# gap once. The feedback path is what the device side does not have.
svg('training-inference.svg',1140,272,f'''<path d="M570 12V262" stroke="{L}" stroke-width="2" stroke-dasharray="6 8"/>
<text x="30" y="34" font-size="22" font-weight="600" fill="{T}">Training · data centre</text>
<text x="600" y="34" font-size="22" font-weight="600" fill="{B}">Inference · device</text>
<path d="M500 62H596" stroke="{A}" stroke-width="3" marker-end="url(#amber)"/>
<text x="548" y="50" text-anchor="middle" font-size="16" font-weight="600" fill="{A}">weights</text>
<rect x="30" y="76" width="150" height="58" rx="9" fill="{P}" stroke="{B}" stroke-width="2"/><text x="105" y="111" text-anchor="middle" font-size="17">Data batches</text>
<rect x="216" y="76" width="170" height="58" rx="9" fill="{P}" stroke="{B}" stroke-width="2"/><text x="301" y="102" text-anchor="middle" font-size="17">Forward and</text><text x="301" y="122" text-anchor="middle" font-size="17">backward</text>
<rect x="418" y="76" width="126" height="58" rx="9" fill="{P}" stroke="{B}" stroke-width="2"/><text x="481" y="102" text-anchor="middle" font-size="17">Update</text><text x="481" y="122" text-anchor="middle" font-size="17">weights</text>
<path d="M184 105H212M390 105H414" stroke="{B}" stroke-width="3" marker-end="url(#a)"/>
<path d="M481 134V208Q481 216 473 216H113Q105 216 105 208V140" fill="none" stroke="{A}" stroke-width="3" stroke-dasharray="8 5" marker-end="url(#amber)"/>
<text x="287" y="248" text-anchor="middle" font-size="16" font-weight="600" fill="{A}">every step changes the weights — many passes, data-centre power</text>
<rect x="616" y="76" width="150" height="58" rx="9" fill="{P}" stroke="{B}" stroke-width="2"/><text x="691" y="111" text-anchor="middle" font-size="17">Sensor input</text>
<rect x="806" y="76" width="150" height="58" rx="9" fill="{P}" stroke="{B}" stroke-width="2"/><text x="881" y="111" text-anchor="middle" font-size="17">Fixed weights</text>
<rect x="996" y="76" width="110" height="58" rx="9" fill="{P}" stroke="{B}" stroke-width="2"/><text x="1051" y="111" text-anchor="middle" font-size="17">Answer</text>
<path d="M770 105H802M960 105H992" stroke="{B}" stroke-width="3" marker-end="url(#a)"/>
<text x="853" y="248" text-anchor="middle" font-size="16" font-weight="600" fill="{B}">the weights are read, never written — one pass, device power</text>''')
# Compare the memory-device framing with our computation-first design approach.
svg('memory-first-vs-compute-first.svg',1120,490,f'''<text x="318" y="26" text-anchor="middle" font-size="18" fill="{M}">STARTING POINT</text>
<text x="664" y="26" text-anchor="middle" font-size="18" fill="{M}">DESIGN QUESTION</text>
<text x="992" y="26" text-anchor="middle" font-size="18" fill="{M}">RESULTING FRAME</text>
<text x="10" y="129" font-size="24" font-weight="600">From</text><text x="10" y="160" font-size="24" font-weight="600">memory</text>
<rect x="174" y="53" width="288" height="185" rx="10" fill="{P}"/>
<text x="318" y="86" text-anchor="middle" font-size="22" font-weight="600">Memory-device research</text>
<g stroke="{B}" stroke-width="2" fill="white"><rect x="288" y="104" width="60" height="51" rx="3"/><path d="M298 114H338V145H298Z M298 129H338 M311 114V145 M325 114V145 M279 115H288 M279 130H288 M279 145H288 M348 115H357 M348 130H357 M348 145H357"/></g>
<text x="318" y="184" text-anchor="middle" font-size="19">RRAM · PCM · MRAM</text>
<text x="318" y="212" text-anchor="middle" font-size="19">FeRAM · SRAM · …</text>
<path d="M475 146H516" stroke="{B}" stroke-width="2.5" marker-end="url(#a)"/>
<rect x="532" y="53" width="264" height="185" rx="10" fill="{P}"/>
<text x="664" y="87" text-anchor="middle" font-size="21" font-weight="600">Make memory compute</text>
<rect x="557" y="108" width="214" height="109" rx="8" fill="white" stroke="{B}" stroke-width="2"/>
<text x="664" y="135" text-anchor="middle" font-size="19">One device</text>
<text x="664" y="167" text-anchor="middle" font-size="22">stores the weight</text>
<text x="664" y="197" text-anchor="middle" font-size="22">+ computes with it</text>
<path d="M809 146H850" stroke="{B}" stroke-width="2.5" marker-end="url(#a)"/>
<rect x="866" y="53" width="248" height="185" rx="10" fill="{P}"/>
<text x="990" y="103" text-anchor="middle" font-size="22" font-weight="600">“Analog in-memory</text>
<text x="990" y="133" text-anchor="middle" font-size="22" font-weight="600">computing”</text>
<path d="M890 151H1090" stroke="{L}" stroke-width="1.5"/>
<text x="990" y="180" text-anchor="middle" font-size="19">Reviews by device family</text>
<text x="990" y="211" text-anchor="middle" font-size="19">Terminology bias</text>
<path d="M10 260H1114" stroke="{L}" stroke-width="1.5"/>
<text x="10" y="338" font-size="24" font-weight="600">From</text><text x="10" y="369" font-size="24" font-weight="600">compute</text>
<text x="10" y="399" font-size="16" fill="{A}">Our approach</text>
<rect x="174" y="282" width="288" height="191" rx="10" fill="#fff4e8"/>
<text x="318" y="316" text-anchor="middle" font-size="22" font-weight="600">First principles: compute</text>
<rect x="196" y="344" width="106" height="67" rx="6" fill="white" stroke="{A}" stroke-width="2"/>
{math_svg('Wx', 249, 365, 27)}<text x="249" y="397" text-anchor="middle" font-size="17">linear</text>
<path d="M309 377H329" stroke="{A}" stroke-width="2" marker-end="url(#amber)"/>
<rect x="340" y="344" width="100" height="67" rx="6" fill="white" stroke="{A}" stroke-width="2"/>
{math_svg('\\varphi(\\cdot)', 390, 365, 27)}<text x="390" y="397" text-anchor="middle" font-size="17">nonlinear</text>
<text x="318" y="449" text-anchor="middle" font-size="19">What operation do we need?</text>
<path d="M475 378H516" stroke="{A}" stroke-width="2.5" marker-end="url(#amber)"/>
<rect x="532" y="282" width="264" height="191" rx="10" fill="#fff4e8"/>
<text x="664" y="316" text-anchor="middle" font-size="22" font-weight="600">Let physics compute</text>
<g fill="none" stroke="{M}" stroke-width="1.3"><path d="M563 384V338 M563 384H629 M685 384V338 M685 384H751"/></g>
<path d="M570 380L623 343" fill="none" stroke="{B}" stroke-width="3"/>
<path d="M692 378C729 378 704 345 745 345" fill="none" stroke="{A}" stroke-width="3"/>
<text x="596" y="410" text-anchor="middle" font-size="17">Ohm + KCL</text>
<text x="718" y="410" text-anchor="middle" font-size="17">Nonlinearity</text>
<text x="664" y="449" text-anchor="middle" font-size="19">Choose physical mechanisms</text>
<path d="M809 378H850" stroke="{A}" stroke-width="2.5" marker-end="url(#amber)"/>
<rect x="866" y="282" width="248" height="191" rx="10" fill="#fff4e8"/>
<text x="990" y="316" text-anchor="middle" font-size="22" font-weight="600">Hardware follows</text>
<g fill="white" stroke="{A}" stroke-width="2"><rect x="887" y="346" width="55" height="42" rx="4"/><rect x="966" y="346" width="49" height="42" rx="4"/><rect x="1039" y="346" width="55" height="42" rx="4"/><path d="M942 367H966 M1015 367H1039"/></g>
{math_svg('W', 914, 367, 25)}{math_svg('\\varphi', 990, 367, 25)}{math_svg('W', 1067, 367, 25)}
<text x="990" y="425" text-anchor="middle" font-size="19">Weight storage becomes</text>
<text x="990" y="451" text-anchor="middle" font-size="19">an implementation choice</text>''')
# A finite feedforward composition; the return arrow advances the layer index.
svg('finite-linear-nonlinear-composition.svg',1120,225,f'''<text x="560" y="25" text-anchor="middle" font-size="23" font-weight="600">Deep network = finite alternating composition</text>
<text x="24" y="93" font-size="22">Input</text>{math_svg('x', 97, 85, 24)}<path d="M112 85H216" stroke="{B}" stroke-width="2.5" marker-end="url(#a)"/>
{math_svg('k=1', 152, 61, 20)}
<rect x="230" y="51" width="260" height="69" rx="8" fill="{P}" stroke="{B}" stroke-width="2"/>
<text x="360" y="79" text-anchor="middle" font-size="22" font-weight="600">Linear transform</text>
{math_svg('L_k(x)=W_kx+b_k', 360, 104, 22)}
<path d="M500 85H567" stroke="{B}" stroke-width="2.5" marker-end="url(#a)"/>
<rect x="583" y="51" width="260" height="69" rx="8" fill="#fff4e8" stroke="{A}" stroke-width="2"/>
<text x="713" y="79" text-anchor="middle" font-size="22" font-weight="600">Nonlinear transform</text>
{math_svg('\\varphi_k(\\cdot)', 713, 103, 25)}
<path d="M853 85H1003" stroke="{B}" stroke-width="2.5" marker-end="url(#a)"/>
<text x="1018" y="93" font-size="22">Output</text>{math_svg('y', 1102, 85, 24)}
{math_svg('k=L', 951, 61, 20)}
<circle cx="886" cy="85" r="4" fill="{A}"/>
<path d="M886 85V156H270V124" fill="none" stroke="{A}" stroke-width="2.5" marker-end="url(#amber)"/>
<rect x="365" y="138" width="400" height="33" fill="white"/>
{math_svg('k<L:\\quad k\\leftarrow k+1\\quad\\text{(next layer)}', 565, 155, 23)}
{math_svg('f=\\varphi_L\\circ L_L\\circ\\cdots\\circ\\varphi_2\\circ L_2\\circ\\varphi_1\\circ L_1', 560, 207, 28)}''')
# A fully analogue function basis: the nonlinear terms are device transfer curves, and
# only the weighted sum is done on a wire. Generic illustration of the idea — it is not
# a drawing of any published architecture. See the KANalogue framework PDF for one
# concrete arrangement (linked from the slide, not reproduced here).
basis=''
for i,(y,curve) in enumerate(zip([44,134,224],
        ['M0 26C26 26 34 4 52 4','M0 24C16 24 32 8 52 2','M0 2C22 2 36 20 52 24'])):
    basis+=f'<rect x="112" y="{y}" width="96" height="46" rx="8" fill="#fff4e8" stroke="{A}" stroke-width="2"/>'
    basis+=f'<g transform="translate(140,{y+11})" fill="none" stroke="{A}" stroke-width="2.5"><path d="{curve}"/></g>'
    basis+=math_svg(r'\varphi_'+str(i+1)+'(x)', 244, y+24, 23)
    end=[(336,137),(328,155),(337,173)][i]
    basis+=f'<path d="M274 {y+23}L{end[0]} {end[1]}" stroke="{A}" stroke-width="2.5" marker-end="url(#amber)"/>'
    basis+=math_svg('w_'+str(i+1), 305, [77,137,196][i], 22)
svg('device-function-basis.svg',620,272,f'''{math_svg('x', 25, 155, 26)}
<path d="M42 155H88" stroke="{B}" stroke-width="3" marker-end="url(#a)"/>
<path d="M104 67V247M104 155H96" stroke="{B}" stroke-width="2.5" fill="none"/>
<path d="M104 67H112M104 157H112M104 247H112" stroke="{B}" stroke-width="2.5"/>
{basis}
<circle cx="352" cy="155" r="24" fill="{P}" stroke="{B}" stroke-width="2.5"/>{math_svg('\\sum', 352, 155, 24)}
<path d="M376 155H438" stroke="{B}" stroke-width="3" marker-end="url(#a)"/>
{math_svg('\\sum_i w_i\\varphi_i(x)', 530, 155, 26)}
''')
print('Generated the deck diagrams: pillars, flags, von Neumann, edge, synaptic, in-memory,'
      ' tolerance, speech cloud, and the SRAM/DRAM, crossbar, FPGA, FPMA, training-inference,'
      ' memory-first and device-function-basis figures.')
