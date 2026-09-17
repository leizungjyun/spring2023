"""Validate catalog targets, migrated references, exact file preservation and redirects."""
from pathlib import Path
import hashlib, json, re, sys, subprocess
from urllib.parse import unquote
from library_paths import refs,resolve

def main():
    root=Path(__file__).resolve().parents[1]
    import os
    os.chdir(root)
    catalog=json.loads(Path('portal/catalog.json').read_text())['presentations']
    manifest=json.loads(Path('portal/migration-map.json').read_text());audit=json.loads(Path('portal/migration-audit.json').read_text())
    files={p.as_posix() for b in ['collections','assets','lectures','music15b','piano-group','dist','plugin','css','js','portal','templates'] for p in Path(b).rglob('*') if p.is_file()}
    files|={'index.html','README.md','package.json'}
    errors=[];known=[];count=0
    preexisting={(manifest['paths'].get(b['source'],b['source']),manifest['paths'].get(b['target'],b['target'])) for b in manifest['existingMissingReferences']}
    retired=set(json.loads(Path('portal/retired-redirects.json').read_text())['paths']) if Path('portal/retired-redirects.json').exists() else set()
    ids=set()
    for e in catalog:
        if e['id'] in ids:errors.append('Duplicate id: '+e['id'])
        ids.add(e['id'])
        p=Path(e['path'])
        if not p.is_file():errors.append('Missing catalog target: '+str(p));continue
        text=p.read_text()
        if e.get('submodule'):
            if 'lectures/neuralmorphic_kickoff/main.html' not in text:errors.append('Missing submodule forwarding target')
        elif 'Reveal.initialize' not in text and 'presentation.js' not in text:errors.append('Not a Reveal presentation: '+str(p))
        if e.get('date') and not re.fullmatch(r'\d{4}-\d{2}-\d{2}',e['date']):errors.append('Invalid date: '+e['id'])
    for r in audit:
        p=Path(r['new'])
        if not p.is_file():errors.append('Missing migrated file: '+str(p));continue
        if '--audit' in sys.argv and hashlib.sha256(p.read_bytes()).hexdigest()!=r['after']:errors.append('Changed since migration: '+str(p))
        if r['old']!=r['new'] and r['old'].endswith('.html') and r['old'] not in retired:
            old=Path(r['old']).read_text()
            if 'destination.search = location.search' not in old or 'destination.hash = location.hash' not in old:errors.append('Redirect loses suffix: '+r['old'])
        if p.suffix not in {'.html','.md','.css','.js','.svg'} or p.name=='plotly.min.js':continue
        # Includes supplementary Markdown and source references, not just catalog entrypoints.
        for _,_,raw in refs(p.read_text(errors='replace'),p.suffix):
            target=resolve(p.as_posix(),raw)
            if not target:continue
            count+=1
            if target not in files and not Path(target).is_dir():
                item=dict(source=p.as_posix(),url=raw,target=target)
                if (p.as_posix(),target) in preexisting:known.append(item)
                else:errors.append(item)
    audited={r['new'] for r in audit}
    for source in sorted(files-audited):
        p=Path(source)
        if not source.startswith(('collections/','portal/')) or p.suffix not in {'.html','.md','.css','.js','.svg'} or p.name=='plotly.min.js':continue
        for _,_,raw in refs(p.read_text(errors='replace'),p.suffix):
            target=resolve(source,raw)
            # Portal URLs are resolved by the root HTML document, not portal.js itself.
            if source=='portal/portal.js':target=resolve('index.html',raw)
            if target and target not in files and not Path(target).is_dir():errors.append(dict(source=source,url=raw,target=target))
    report=dict(presentations=len(catalog),referencesChecked=count,filesPreserved=len(audit),knownMissingReferences=known,errors=errors)
    Path('portal/validation-static.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 1 if errors else 0
if __name__=='__main__':sys.exit(main())
