from pathlib import Path
p=Path(__file__).resolve().parents[1] / 'media/diagrams'
p.mkdir(parents=True, exist_ok=True)
B='#00649e'; T='#203441'; M='#607582'; A='#b76b29'; L='#d5e2e9'; P='#eff5f8'
def svg(name,w,h,body):
 (p/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img"><style>text{{font-family:Arial,sans-serif;fill:{T}}}.small{{font-size:17px;fill:{M}}}.label{{font-size:22px;font-weight:600}}.blue{{fill:{B}}}</style><defs><marker id="a" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto-start-reverse"><path d="M0 0L9 4.5L0 9" fill="none" stroke="{B}" stroke-width="1.5"/></marker></defs>'+body+'</svg>')
svg('ai-pillars.svg',520,350,f'''<path d="M70 44V282" stroke="{L}" stroke-width="4"/>
<circle cx="70" cy="55" r="19" fill="{B}"/><circle cx="70" cy="165" r="19" fill="{B}"/><circle cx="70" cy="275" r="19" fill="{A}"/>
<text x="110" y="56" class="label">Algorithms</text><text x="110" y="84" class="small">Frontier model performance is converging</text>
<text x="110" y="166" class="label">Data</text><text x="110" y="194" class="small">Access and quality depend on the domain</text>
<rect x="99" y="234" width="409" height="86" rx="5" fill="{P}"/>
<text x="110" y="266" class="label blue">Compute</text><text x="110" y="296" class="small">Hardware capacity remains uneven</text>''')
svg('memory-traffic.svg',520,350,f'''<rect x="58" y="28" width="404" height="83" rx="8" fill="{P}" stroke="{B}" stroke-width="2"/><text x="260" y="64" text-anchor="middle" class="label">Memory</text><text x="260" y="91" text-anchor="middle" class="small">weights · activations · instructions</text>
<path d="M190 125V218" stroke="{B}" stroke-width="3" marker-end="url(#a)"/><path d="M330 218V125" stroke="{B}" stroke-width="3" marker-end="url(#a)"/><text x="260" y="165" text-anchor="middle" class="small">Move</text><text x="260" y="189" text-anchor="middle" class="small">data</text>
<rect x="58" y="232" width="404" height="83" rx="8" fill="{P}" stroke="{B}" stroke-width="2"/><text x="260" y="268" text-anchor="middle" class="label">Processor</text><text x="260" y="295" text-anchor="middle" class="small">arithmetic · control</text>''')
svg('edge-loop.svg',520,185,f'''<path d="M97 83H211M314 83H426" stroke="{B}" stroke-width="3" marker-end="url(#a)"/>
<circle cx="60" cy="83" r="35" fill="{P}" stroke="{B}" stroke-width="2"/><rect x="32" y="66" width="54" height="33" rx="6" fill="none" stroke="{B}" stroke-width="2"/><circle cx="59" cy="82" r="11" fill="none" stroke="{B}" stroke-width="2"/>
<rect x="218" y="43" width="89" height="80" rx="9" fill="{P}" stroke="{B}" stroke-width="2"/><text x="262" y="91" text-anchor="middle" class="label blue">AI</text>
<circle cx="465" cy="83" r="35" fill="{P}" stroke="{B}" stroke-width="2"/><path d="M443 90l17-31 21 18-17 22" fill="none" stroke="{B}" stroke-width="3"/>
<text x="60" y="153" text-anchor="middle" class="small">Sense</text><text x="262" y="153" text-anchor="middle" class="small">Infer</text><text x="465" y="153" text-anchor="middle" class="small">Act</text>''')
# Conceptual neural morphology and local weighted currents, not anatomical or measured.
brain=f'''<path d="M137 206C91 219 63 178 76 144C47 113 65 73 102 69C101 34 151 13 177 39C211 9 257 26 265 59C306 49 340 83 326 117C360 151 336 192 303 194C288 226 244 229 222 209C197 239 150 239 137 206Z" fill="{P}" stroke="{B}" stroke-width="3"/>
<path d="M178 40Q164 102 194 141Q171 167 184 226M104 70Q151 73 145 121Q102 117 78 145M266 60Q219 63 229 111Q279 113 301 84M326 119Q278 130 285 163Q253 181 224 160M137 207Q114 169 146 150" fill="none" stroke="{B}" stroke-width="2"/>
<text x="205" y="295" text-anchor="middle" style="font-size:54px;font-weight:600;fill:{B}">~20 W</text><text x="205" y="325" text-anchor="middle" class="small">whole-brain metabolic power</text>'''
svg('brain-power.svg',410,350,brain)
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
print('Generated five editable diagrams plus the AI pillars.')
