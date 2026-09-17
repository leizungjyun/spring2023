"""Apply the pre-recorded migration exactly once, without Git index mutations."""
from pathlib import Path
import json, shutil, hashlib, html
from library_paths import rewrite

def redirect(target,title='Presentation moved'):
    # Keep the destination relative so repository/project static hosting also works.
    encoded=json.dumps(target)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title></head>
<body><p><a id="destination" href="{html.escape(target,quote=True)}">Open slides</a></p>
<script>const destination = new URL({encoded}, location.href); destination.search = location.search; destination.hash = location.hash; document.getElementById('destination').href = destination.href; location.replace(destination.href);</script>
<noscript>This presentation has moved. Follow the link above; append your existing query and slide hash if needed.</noscript></body></html>
'''

def main():
    import posixpath
    manifest=json.loads(Path('portal/migration-map.json').read_text());mapping=manifest['paths'];fixups=manifest['referenceFixups'];records=[]
    assert not Path('portal/migration-audit.json').exists(),'Migration already applied'
    # Validate all sources/destinations before the first mutation.
    for old,new in mapping.items():
        assert Path(old).is_file(),old
        if old!=new:assert not Path(new).exists(),new
    for old,new in mapping.items():
        f=Path(old);raw=f.read_bytes();rewritten=raw
        if old!=new and f.suffix in {'.html','.md','.css','.js','.svg','.bak'} and f.name!='plotly.min.js':
            rewritten=rewrite(raw.decode('utf-8'),old,new,mapping,fixups).encode('utf-8')
        records.append(dict(old=old,new=new,before=hashlib.sha256(raw).hexdigest(),after=hashlib.sha256(rewritten).hexdigest(),referenceChanges=raw!=rewritten))
        if old==new:continue
        dest=Path(new);dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.move(str(f),str(dest))
        if raw!=rewritten:dest.write_bytes(rewritten)
    # All historical HTML endpoints, including the embedded chart, receive redirects.
    for old,new in mapping.items():
        if old!=new and old.endswith('.html'):
            dest=Path(old);dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_text(redirect(posixpath.relpath(new,posixpath.dirname(old))))
    sub=Path('collections/projects/2025-01-15-neuromorphic-kickoff/index.html');sub.parent.mkdir(parents=True,exist_ok=True)
    sub.write_text(redirect('../../../lectures/neuralmorphic_kickoff/main.html','Neuromorphic Computing: Research Kick-off'))
    Path('portal/migration-audit.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
    print('Migrated',sum(r['old']!=r['new'] for r in records),'files; preserved',sum(r['old']==r['new'] for r in records),'submodule files.')
if __name__=='__main__':main()
