from pathlib import Path
from xml.sax.saxutils import escape
B=Path(__file__).resolve().parents[1]/'images'
BLUE='#42affa'; AMBER='#ffbf69'; MUTED='#aab7c3'; WHITE='#f5f7fa';BG='#20272d'
def text(x,y,s,size=22,color=WHITE,anchor='middle'):
 return f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{color}" font-size="{size}">{escape(s)}</text>'
def box(x,y,w,h,label,color=BLUE):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{BG}" stroke="{color}" stroke-width="2"/>'+text(x+w/2,y+h/2+8,label)
def arrow(d,color=BLUE):return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="3" marker-end="url(#arrow-{color[1:]})"/>'
def save(name,w,h,s):
 defs=''.join(f'<marker id="arrow-{c[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="{c}"/></marker>' for c in [BLUE,AMBER,MUTED])
 (B/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img"><title>{name[:-4]}</title><defs>{defs}</defs><g font-family="PingFang SC, Microsoft YaHei, sans-serif">{s}</g></svg>')
def architecture(in_memory=False):
 # Identical input/output positions in both diagrams; no peripheral/control detail.
 s=box(5,203,115,54,'输入',MUTED)+box(440,203,115,54,'输出',MUTED)
 s+=arrow('M120 230H165')+arrow('M395 230H435')
 if not in_memory:
  s+=box(170,35,225,70,'存储器')+box(170,195,225,70,'处理器')
  s+=arrow('M225 110V190',AMBER)+arrow('M340 190V110',AMBER)
  s+=text(282,149,'数据',21,AMBER)
 else:
  s+=f'<rect x="170" y="35" width="225" height="230" rx="12" fill="{BG}" stroke="{AMBER}" stroke-width="3"/>'
  s+=text(282,73,'存内计算存储器',23)
  # Each cell combines storage and computation; no separate nearby processor.
  for y in [97,147]:
   for x in [190,255,320]:
    s+=f'<rect x="{x}" y="{y}" width="55" height="38" rx="5" fill="#263b43" stroke="{BLUE}"/>'+text(x+27.5,y+25,'存·算',17,BLUE)
  s+=text(282,225,'数据存储 + 计算',20,AMBER)
 return s
save('separated.svg',560,300,architecture())
s=text(280,28,'存储与计算分离',25)+text(860,28,'存内计算',25,BLUE)
s+='<g transform="translate(0,25)">'+architecture()+'</g><g transform="translate(580,25)">'+architecture(True)+'</g>'
s+=f'<path d="M570 40V310" stroke="#46515a" stroke-dasharray="4 6"/>'
save('coupling.svg',1140,330,s)
# Original schematic brain icon: engineering inspiration, not anatomical/experimental evidence.
s=f'<path d="M216 150 C207 178 211 193 223 211 L199 217 C184 194 180 177 181 155 Z" fill="#263b43" stroke="{BLUE}" stroke-width="3"/>'
s+=f'<path d="M225 137 C262 118 299 136 294 163 C290 190 256 194 233 177 Z" fill="#263b43" stroke="{BLUE}" stroke-width="3"/>'
s+=f'<path d="M63 164 C29 166 18 140 28 115 C10 90 27 62 50 57 C47 30 77 17 103 27 C124 6 156 12 172 22 C196 6 228 17 241 37 C276 31 299 52 297 77 C322 89 325 117 309 133 C305 157 278 167 253 158 C231 176 204 168 188 153 C163 167 136 157 122 166 C102 180 80 176 63 164 Z" fill="#233944" stroke="{BLUE}" stroke-width="4"/>'
for d in ['M53 58 C82 57 86 84 72 102 C58 120 66 145 88 154','M105 30 C90 53 110 62 121 75 C134 90 115 110 127 131','M170 25 C155 48 169 66 187 70 C207 78 214 104 194 119 C182 130 192 143 204 150','M242 40 C220 57 229 76 247 85 C268 95 268 117 249 129','M31 112 C51 103 57 80 73 85','M93 114 C102 101 117 111 128 114','M137 50 C146 74 135 88 151 103 C171 110 171 136 155 153','M276 68 C265 80 284 98 302 99','M232 151 C251 148 270 152 284 161','M241 166 C255 165 266 169 274 176']:
 s+=f'<path d="{d}" fill="none" stroke="{BLUE}" stroke-width="3" stroke-linecap="round"/>'
save('brain-inspired.svg',350,225,s)
s=''
for x,label,c in [(0,'线性变换',BLUE),(385,'非线性变换',AMBER),(770,'下一层',BLUE)]:s+=box(x+5,20,310,75,label,c)
s+=arrow('M320 58H380')+arrow('M705 58H765')+text(545,130,'技术核心：器件非线性',23,AMBER)
save('nonlinearity.svg',1100,145,s)
s=''
for i,(label,sub,c) in enumerate([('PCB 原型','已有平台',BLUE),('验证芯片','关键电路 / 工艺',MUTED),('SiP / 模块','互连 / 封装 / 测试',MUTED),('客户系统','同条件评价',MUTED)]):
 x=10+i*280;s+=box(x,25,230,80,label,c)+text(x+115,142,sub,20,c)
 if i<3:s+=arrow(f'M{x+235} 65H{x+270}',MUTED)
save('product-roadmap.svg',1100,165,s)
s=''
for i,(label,sub,c) in enumerate([('传感输入','读出与采样',MUTED),('焦点估计 / 控制','拟承担的计算环节',AMBER),('执行器','驱动与机械运动',MUTED),('光学响应','成像质量与稳定',MUTED)]):
 x=10+i*280;s+=box(x,22,230,80,label,c)+text(x+115,139,sub,19,c)
 if i<3:s+=arrow(f'M{x+235} 62H{x+270}',MUTED)
s+=arrow('M965 165V210H125V170',MUTED)+text(545,239,'整机对焦时延：传感、计算、执行与光学响应',23)
save('autofocus.svg',1100,260,s)
