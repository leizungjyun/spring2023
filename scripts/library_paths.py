"""Local URL discovery and rebasing shared by migration and validation."""
import html, posixpath, re
from urllib.parse import urlsplit, unquote, quote

ATTR = re.compile(r'''\b(?:src|href|xlink:href|poster|data-src|data-background-image|data-background-video|data-background-iframe|data-markdown)\s*=\s*(["'])(.*?)\1''',re.I)
MD = re.compile(r'''!?\[[^\]\n]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+["'][^\n]*?["'])?\s*\)''')
CSS = re.compile(r'''url\(\s*(["']?)([^)'"\n]+)\1\s*\)''')
JS = re.compile(r'''(["'])([^"'\n]+\.(?:html|md|css|js|png|jpe?g|gif|svg|mp4|mov|pdf)(?:[?#][^"'\n]*)?)\1''',re.I)
TEXT_EXT={'.html','.md','.css','.js','.svg','.bak'}

def refs(text, suffix):
    found=[]
    for m in ATTR.finditer(text): found.append((m.start(2),m.end(2),m.group(2)))
    if suffix in {'.md'}:
        for m in MD.finditer(text):
            a,b=m.span(1);raw=m.group(1)
            if raw.startswith('<'):a+=1;b-=1;raw=raw[1:-1]
            found.append((a,b,raw))
    if suffix in {'.css','.html','.svg'}:
        for m in CSS.finditer(text):found.append((m.start(2),m.end(2),m.group(2).strip()))
    if suffix=='.js':
        for m in JS.finditer(text):found.append((m.start(2),m.end(2),m.group(2)))
    unique={}
    for a,b,v in found:
        if not any(a>=x and b<=y for x,y in unique):unique[(a,b)]=v
    return [(a,b,v) for (a,b),v in sorted(unique.items())]

def resolve(source, raw):
    raw=html.unescape(raw).strip()
    if not raw or raw.startswith(('#','//','data:','mailto:','javascript:','tel:','app:','codex:')):return None
    try:u=urlsplit(raw)
    except ValueError:return None
    if u.scheme or u.netloc:return None
    if not u.path:return None
    return posixpath.normpath(posixpath.join(posixpath.dirname(source),unquote(u.path))) if not u.path.startswith('/') else unquote(u.path).lstrip('/')

def rewrite(text, source, destination, mapping, fixups=None):
    fixups=fixups or {};changes=[]
    for a,b,raw in refs(text,posixpath.splitext(source)[1]):
        old=resolve(source,raw)
        if old is None:continue
        old=fixups.get(old,old)
        new=mapping.get(old,old)
        u=urlsplit(html.unescape(raw));rel=posixpath.relpath(new,posixpath.dirname(destination) or '.')
        # Preserve an unchanged spelling (including Chinese names and '%' in legacy sources).
        if source==destination and new==old:continue
        original_target=resolve(destination,raw)
        if original_target==new:continue
        value=quote(rel,safe='/@-._~')
        if u.query:value+='?'+u.query
        if u.fragment:value+='#'+u.fragment
        if '&amp;' in raw:value=value.replace('&','&amp;')
        changes.append((a,b,value))
    for a,b,v in reversed(changes):text=text[:a]+v+text[b:]
    return text
