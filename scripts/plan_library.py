"""Content-reviewed migration manifest. Run before moving any source files."""
from pathlib import Path
import json, re, hashlib
from library_paths import refs,resolve
if Path('portal/migration-audit.json').exists():
    raise SystemExit('Migration already applied; edit catalog.json directly. Do not rerun the planner.')
mapping={};entries=[]

def add(old,dest):
    assert old not in mapping or mapping[old]==dest,(old,dest)
    mapping[old]=dest

def deck(oldhtml,newdir,title,collection,tags,date=None,reason='',assetroot=None,review=None,datesource='content',oldmd=None):
    newhtml=newdir+'/index.html';oldmd=oldmd or oldhtml[:-5]+'.md'
    add(oldhtml,newhtml);add(oldmd,newdir+'/slides.md')
    if assetroot:
        for f in Path(assetroot).rglob('*'):
            if not f.is_file() or f.as_posix() in mapping:continue
            rel=f.relative_to(assetroot).as_posix()
            if '/' not in rel:
                if f.suffix.lower() in {'.png','.jpg','.jpeg','.gif','.svg','.webp'}:rel='images/'+rel
                elif f.suffix.lower() in {'.pdf','.pptx','.drawio'}:rel='docs/'+rel
                elif f.suffix.lower() in {'.mp4','.mov'}:rel='videos/'+rel
            if rel=='promts.md':rel='docs/promts.md'
            add(f.as_posix(),newdir+'/'+rel)
    entry=dict(id=Path(newdir).name,title=title,collection=collection,tags=tags,date=date,dateSource=datesource if date else None,path=newhtml,legacyPaths=[oldhtml],classificationReason=reason)
    if review:entry['reviewNote']=review
    entries.append(entry)

D='collections/'
deck('lectures/2023-04-21-copilot.html',D+'teaching/2023-04-21-coding-with-copilot','Coding with Copilot','teaching',['AI','programming'], '2023-04-21','Programming-practice tutorial with setup and live demo.')
deck('lectures/2023-09-29-embodied.html',D+'research-talks/2023-09-29-embodied-intelligence','Embodied Intelligence with Foundation Models','research-talks',['AI','robotics'],'2023-09-29','Webinar explaining foundation models and embodied cognition.',datesource='filename')
deck('lectures/2024-05-15-KAN.html',D+'research-talks/2024-05-15-kolmogorov-arnold-networks','On Kolmogorov–Arnold Networks','research-talks',['AI','mathematics'],'2024-05-17','Research architecture explanation and discussion.',assetroot='lectures/2024-05-15-KAN',review='Title slide says 2024-05-17; historical filename and folder date 2024-05-15 retained.')
deck('lectures/2024.5.31-sdem-kickoff.html',D+'projects/2024-05-31-sdem-kickoff','SDEM: From Controlling to Riding','projects',['AI','robotics'],'2024-05-31','Explicit project introduction, technical map and roadmap.',assetroot='lectures/2024.5.31-sdem')
deck('lectures/2024.6.5-discuss.html',D+'group-meetings/2024-06-05-research-and-delivery-discussion','Research and Project Delivery Discussion','group-meetings',['brain-inspired computing','robotics'],'2024-06-05','Internal discussion of research tasks and project releases.',assetroot='lectures/2024.6.5-discuss')
deck('lectures/metaseminar/2024-06-14-meta-seminar.html',D+'teaching/scientific-communication/2024-06-14-meta-seminar','Meta-Seminar: How to Present and Discuss','teaching',['academic skills','communication'],'2024-06-14','Teaches seminar preparation, presentation and discussion.',assetroot='lectures/metaseminar')
deck('lectures/2024-07-11-SDEM/2024-07-11-sdem.html',D+'projects/2024-07-11-ornithopter','Ornithopter: Design and Implementation','projects',['robotics','AI'],'2024-07-11','Engineering targets, design procedure and training roadmap.',assetroot='lectures/2024-07-11-SDEM',review='Includes a topic survey; Projects chosen because design targets and implementation dominate.')
deck('lectures/2024-07-24-paper/2024-07-24-paper.html',D+'teaching/deep-learning/2024-07-24-applied-math-review','Applied Math and Machine Learning: Test Review','teaching',['AI','mathematics'],'2024-07-22','Explicit review for a July test; not a paper presentation.',assetroot='lectures/2024-07-24-paper',review='Content dates this 2024-07-22; original folder says 2024-07-24. Folder date retained, catalog uses the title-slide date.')
deck('lectures/2024-09-14-KAN2/2024-09-14-KAN2.html',D+'group-meetings/2024-09-14-semester-opening','Semester Opening and KAN 2.0','group-meetings',['AI','mathematics','group planning'],'2024-09-14','Orientation, onboarding and semester strategy precede a KAN 2.0 discussion.',assetroot='lectures/2024-09-14-KAN2',review='Mixed group meeting and research talk; filed by its opening purpose and strategy content.')
deck('lectures/2024-10-19-KJW/2024-10-19.html',D+'research-talks/2024-10-19-brain-inspired-embodied-intelligence','类脑的时空具身智能概述','research-talks',['AI','brain-inspired computing','robotics'],'2024-10-19','Topic overview linking neuroscience and embodied intelligence.',assetroot='lectures/2024-10-19-KJW')
deck('lectures/2024-11-07-brain-inspired/2024-11-07.html',D+'research-talks/2024-11-07-brain-inspired-navigation','Brain-Inspired Navigation: CNS Review','research-talks',['brain-inspired computing','robotics'],'2024-11-07','Topic review of brain-inspired navigation and spatial intelligence.',assetroot='lectures/2024-11-07-brain-inspired')
deck('lectures/2024-12-09.html',D+'research-talks/2024-12-09-brain-inspired-spatial-intelligence','Brain-Inspired Navigation and Spatial Intelligence','research-talks',['AI','brain-inspired computing','robotics'],'2024-12-09','Extended research topic talk, including a second session.',assetroot='lectures/2024-12-09-brain-inspired',review='Contains title slides dated 2024-12-09 and 2024-12-16. Kept as one deck with its first date.')
deck('lectures/2025-01-16-recap/main.html',D+'group-meetings/2025-01-16-recap','Group Recap: Time, Seminars and Reading Groups','group-meetings',['group planning'],'2025-01-16','Internal recap and discussion of academic gathering formats.',assetroot='lectures/2025-01-16-recap',datesource='folder')
deck('lectures/2026-09-10-AI-group-gathering/main.html',D+'group-meetings/2026-09-10-ai-group-gathering','AI Group Gathering: Progress · People · Possibilities','group-meetings',['AI','brain-inspired computing','robotics','hardware'],'2026-09-11','Explicit internal gathering with progress, membership and future plans.',assetroot='lectures/2026-09-10-AI-group-gathering',review='Title slide says 2026-09-11; historical directory date 2026-09-10 retained.')
# Preserve course/series folders and lesson sequence.
for n,title in [(1,'Music & Culture'),(2,'Melody, Rhythm, and Sound'),(3,'Instrumentation'),(4,'Behind the Scenes: Harmony, Texture, and Form'),(5,'Musical Style'),(6,'Musical Theater'),(7,'Modern Jazz'),(10,'The Rock Revolution'),(11,'San Francisco and the Diversity of Rock'),(12,'New Trends of the Late 1970s')]:
    stem=f'week{n:02}';s=Path(f'music15b/{stem}.md').read_text();date=re.search(r'LI Shaun, (\d{4}-\d{2}-\d{2})',s).group(1)
    entries.append(dict(id='music15b-'+stem,title=title,collection='teaching',tags=['music','culture'],date=date,dateSource='content',path=f'collections/teaching/music15b/{stem}.html',legacyPaths=[f'music15b/{stem}.html'],series='Music 15B',lessonOrder=n,classificationReason='Weekly Music & Culture course lesson.'))
for f in Path('music15b').rglob('*'):
    if f.is_file():add(f.as_posix(),'collections/teaching/'+f.as_posix())
for oldstem,newstem,title,date,num in [('2024-06-07-d2l-01','lesson01','Dive into Deep Learning: Python and PyTorch','2024-06-07',1)]:
    for ext in ['.html','.md']:add('lectures/d2l/'+oldstem+ext,D+'teaching/deep-learning/dive-into-deep-learning/'+newstem+ext)
    entries.append(dict(id='d2l-lesson01',title=title,collection='teaching',tags=['AI','programming'],date=date,dateSource='content',path=D+'teaching/deep-learning/dive-into-deep-learning/lesson01.html',legacyPaths=['lectures/d2l/'+oldstem+'.html'],series='Dive into Deep Learning',lessonOrder=1,classificationReason='Course introduction and development environment tutorial.'))
seriesdir=D+'teaching/scientific-communication/verbal-for-science'
for oldstem,newstem,title,date,n in [('2024-09-sci-verbal','lesson01','Verbal for Science: English and Communication','2024-09-25',1),('2024-09-sci-verbal02','lesson02','Verbal for Science: Vocabulary','2024-10-30',2)]:
    for ext in ['.html','.md']:add('lectures/2024-09-sci-verbal/'+oldstem+ext,seriesdir+'/'+newstem+ext)
    entries.append(dict(id='verbal-for-science-'+newstem,title=title,collection='teaching',tags=['communication','academic skills'],date=date,dateSource='content',path=seriesdir+'/'+newstem+'.html',legacyPaths=['lectures/2024-09-sci-verbal/'+oldstem+'.html'],series='Verbal for Science',lessonOrder=n,classificationReason='Academic English and communication lesson.'))
for f in Path('lectures/2024-09-sci-verbal').rglob('*'):
    if f.is_file() and f.as_posix() not in mapping:add(f.as_posix(),seriesdir+'/'+f.relative_to('lectures/2024-09-sci-verbal').as_posix())
deck('piano-group/papillons.html',D+'music/2023-12-02-papillons','Schumann: Papillons','music',['music','piano'],'2023-12-02','Piano-group work presentation.')
deck('piano-group/concert-program.html',D+'music/concert-program','Schumann Piano Concerto: Concert Program','music',['music','piano'],None,'Concert program; no presentation date in the supplied material.')
for f in Path('piano-group').rglob('*'):
    if f.is_file() and f.as_posix() not in mapping:add(f.as_posix(),D+'music/_shared/'+f.relative_to('piano-group').as_posix())
for f in Path('lectures/images').rglob('*'):
    if f.is_file():add(f.as_posix(),'assets/presentations/lectures-images/'+f.relative_to('lectures/images').as_posix())
# Submodule is intentionally not relocated or rewritten; new collection launcher forwards to it.
for f in Path('lectures/neuralmorphic_kickoff').rglob('*'):
    if f.is_file():add(f.as_posix(),f.as_posix())
entries.append(dict(id='neuromorphic-kickoff',title='Neuromorphic Computing: Research Kick-off',collection='projects',tags=['AI','brain-inspired computing','hardware'],date='2025-01-15',dateSource='content',path=D+'projects/2025-01-15-neuromorphic-kickoff/index.html',legacyPaths=['lectures/neuralmorphic_kickoff/main.html'],submodule='lectures/neuralmorphic_kickoff',classificationReason='Explicit research kickoff, scientific questions and eNN roadmap.'))
add('index.html.bak','templates/reveal-starter/index.html.bak')
for base in ['lectures','music15b','piano-group']:
    for f in Path(base).rglob('*'):
        if f.is_file() and f.as_posix() not in mapping:
            assert f.name=='.DS_Store',str(f)
            add(f.as_posix(),'assets/presentations/legacy-metadata/'+f.as_posix())
assert len(set(mapping.values()))==len(mapping),'Destination collision'
fixups={'lectures/2024-07-11-SDEM/2024-07-11-SDEM.md':'lectures/2024-07-11-SDEM/2024-07-11-sdem.md'}
broken=[]
for old in mapping:
    f=Path(old)
    if f.suffix not in {'.html','.md','.css','.js','.svg'} or f.name=='plotly.min.js':continue
    for _,_,raw in refs(f.read_text(errors='replace'),f.suffix):
        target=resolve(old,raw)
        if target and not Path(target).exists():broken.append(dict(source=old,url=raw,target=target))
manifest=dict(version=1,submodulePolicy='Retained in place; collection launcher redirects to the registered submodule. No changes to gitlink, .gitmodules, core.worktree or its files.',paths=mapping,referenceFixups=fixups,existingMissingReferences=broken)
Path('portal/migration-map.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
Path('portal/catalog.json').write_text(json.dumps(dict(version=1,presentations=entries),ensure_ascii=False,indent=2)+'\n')
print('MAPPING WRITTEN BEFORE MOVES:',len(mapping),'files;',len(entries),'presentations;',len(broken),'pre-existing unresolved URL candidates')
for b in broken:print(b)
