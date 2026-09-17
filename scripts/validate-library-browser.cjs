/* Usage: node scripts/validate-library-browser.cjs [http://localhost:8017]
 * Requires the existing Puppeteer dependency and a current Chrome executable.
 * No remote media is fetched; this checks local migration behavior.
 */
const fs=require('fs'),path=require('path'),assert=require('assert');
const puppeteer=require('puppeteer');
const base=process.argv[2]||'http://localhost:8017';
const catalog=JSON.parse(fs.readFileSync('portal/catalog.json')).presentations;
const mapping=JSON.parse(fs.readFileSync('portal/migration-map.json')).paths;
const retired=new Set(fs.existsSync('portal/retired-redirects.json') ? JSON.parse(fs.readFileSync('portal/retired-redirects.json')).paths : []);
const chrome=process.env.CHROME_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const screenshots='/tmp/reveal-library-qa';fs.mkdirSync(screenshots,{recursive:true});
const delay=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
 const browser=await puppeteer.launch({executablePath:chrome,headless:true,args:['--no-sandbox']});
 const report={catalog:[],redirects:[],localFailures:[],consoleErrors:[],portal:{},latest:{},externalResources:'Blocked during validation; remote media availability was not checked.'};
 try{
  const page=await browser.newPage();await page.setViewport({width:1440,height:1000});
  await page.setRequestInterception(true);
  page.on('request',req=>{const u=req.url();if(u.startsWith('http')&&!u.startsWith(base)&&!u.startsWith('http://localhost:35729'))req.abort();else req.continue();});
  page.on('response',res=>{if(res.url().startsWith(base)&&res.status()>=400)report.localFailures.push({url:res.url(),status:res.status()});});
  page.on('pageerror',e=>report.consoleErrors.push(e.message));
  await page.goto(base+'/');await page.waitForSelector('#results .presentation-card');
  assert.strictEqual(await page.$$eval('#results .presentation-card',es=>es.length),catalog.length);
  await page.screenshot({path:screenshots+'/portal-desktop.png'});
  await page.click('[data-collection="research-talks"]');await page.select('#topic','AI');await page.select('#year','2024');
  const wanted=catalog.filter(e=>e.collection==='research-talks'&&e.tags.includes('AI')&&e.date.startsWith('2024'));
  assert.strictEqual(await page.$$eval('#results .presentation-card',es=>es.length),wanted.length);
  await page.type('#search','Kolmogorov');assert.strictEqual(await page.$$eval('#results .presentation-card',es=>es.length),1);
  await page.reload();await page.waitForSelector('#results .presentation-card');assert.strictEqual(await page.$eval('#search',e=>e.value),'Kolmogorov');
  await page.click('#clear');await page.click('[data-collection="teaching"]');
  const musicLinks=await page.$$eval('#results .open-slides',es=>es.map(e=>e.getAttribute('href')).filter(s=>s.includes('/music15b/')));
  assert.deepStrictEqual(musicLinks,catalog.filter(e=>e.series==='Music 15B').sort((a,b)=>a.lessonOrder-b.lessonOrder).map(e=>e.path));
  await page.click('#clear');await page.setViewport({width:390,height:844});
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));
  await page.screenshot({path:screenshots+'/portal-mobile.png'});
  report.portal={entries:catalog.length,combinedFilters:true,queryPersistence:true,courseOrder:true,mobileNoOverflow:true};
  await page.setViewport({width:1440,height:1000});
  const representatives=new Set(['2026-09-10-ai-group-gathering','2024-05-15-kolmogorov-arnold-networks','2024-05-31-sdem-kickoff','music15b-week03','2023-12-02-papillons','neuromorphic-kickoff','verbal-for-science-lesson01','d2l-lesson01']);
  for(const e of catalog){
   await page.goto(base+'/'+e.path,{waitUntil:'domcontentloaded'});
   try{await page.waitForFunction('window.Reveal && Reveal.isReady && Reveal.isReady()',{timeout:15000});}
   catch(err){report.catalog.push({id:e.id,error:err.message});continue;}
   const data=await page.evaluate(()=>({slides:Reveal.getSlides().length,hasContent:Reveal.getSlides().some(s=>s.textContent.trim().length||s.querySelector('img,video,iframe'))}));
   assert(data.slides>0&&(data.hasContent||e.status==='draft'),e.id);
   report.catalog.push({id:e.id,...data});
   if(representatives.has(e.id)){await delay(500);await page.screenshot({path:screenshots+'/'+e.id+'.png'});}
  }
  // Test the redirect itself before Reveal can normalize an out-of-range slide hash.
  const redirectPage=await browser.newPage();
  await redirectPage.setRequestInterception(true);
  let expectedPath='';
  redirectPage.on('request',req=>{
   if(req.resourceType()==='document' && decodeURI(new URL(req.url()).pathname)==='/'+expectedPath)
    req.respond({status:200,contentType:'text/html',body:'<!doctype html><title>Redirect destination reached</title>'});
   else req.continue();
  });
  const redirectPairs=Object.entries(mapping).filter(([a,b])=>a!==b&&a.endsWith('.html')&&!retired.has(a));
  const submodule=catalog.find(e=>e.submodule);
  redirectPairs.push([submodule.path,submodule.legacyPaths[0]]);
  for(const [old,newPath] of redirectPairs){
   expectedPath=newPath;
   await redirectPage.goto(base+'/'+old+'?transition=none&migration-check=1#/2/1',{waitUntil:'domcontentloaded'});
   await redirectPage.waitForFunction('document.title === "Redirect destination reached"',{timeout:10000});
   const u=new URL(await redirectPage.evaluate(()=>location.href));assert.strictEqual(decodeURI(u.pathname),'/'+newPath);assert.strictEqual(u.search,'?transition=none&migration-check=1');assert.strictEqual(u.hash,'#/2/1');
   report.redirects.push(old);
  }
  await redirectPage.close();
  const latest=catalog.find(e=>e.id==='2026-09-10-ai-group-gathering');
  await page.goto(base+'/'+latest.path);await page.waitForFunction('window.Reveal && Reveal.isReady()');
  await page.evaluate(()=>Reveal.slide(6));await delay(500);
  let chart=page.frames().find(f=>f.url().includes('acceptance-chart.html'));assert(chart,'Chart iframe missing');
  await chart.waitForFunction('document.getElementById("plot") && document.getElementById("plot").data');
  report.latest.hover=[];
  for(const [width,height] of [[1024,768],[1440,900],[1920,1080]]){
   await page.setViewport({width,height});await delay(350);
   await chart.evaluate(()=>{window.hovered=null;document.getElementById('plot').on('plotly_hover',e=>window.hovered={x:e.points[0].x,curve:e.points[0].curveNumber});});
   const p=await chart.evaluate(()=>{const r=document.querySelector('.scatterlayer .trace .points path:nth-child(5)').getBoundingClientRect();return{x:r.x+r.width/2,y:r.y+r.height/2};});
   const q=await page.evaluate(()=>{const e=document.querySelector('#acceptance-chart'),r=e.getBoundingClientRect();return{x:r.x,y:r.y,scale:r.width/e.offsetWidth};});
   await page.mouse.move(0,0);await page.mouse.move(q.x+p.x*q.scale,q.y+p.y*q.scale);await delay(120);
   const hovered=await chart.evaluate(()=>window.hovered);assert(hovered&&hovered.x===5&&hovered.curve===0,JSON.stringify({width,hovered}));report.latest.hover.push({width,height,correct:true});
  }
  // Escape from iframe focus then from parent, and return to the chart.
  await page.click('#acceptance-chart');await page.keyboard.press('Escape');await delay(300);assert(await page.evaluate(()=>Reveal.isOverview()));
  await page.keyboard.press('Escape');await delay(300);assert(!(await page.evaluate(()=>Reveal.isOverview())));
  report.latest.escapeOverview=true;
  await page.setViewport({width:1440,height:1000});await delay(1000);await page.screenshot({path:screenshots+'/latest-chart.png'});
  report.latest.videos=await page.evaluate(async()=>{
   const results=[];
   for(const v of document.querySelectorAll('video')){
    const i=Reveal.getIndices(v.closest('section'));Reveal.slide(i.h,i.v);await new Promise(r=>setTimeout(r,1100));
    const started=!v.paused&&v.currentTime>0;
    if(Number.isFinite(v.duration)){v.currentTime=v.duration-.15;await new Promise(r=>setTimeout(r,600));}
    results.push({src:v.currentSrc,autoplay:started,muted:v.muted,loop:v.loop,wrapped:v.currentTime<1.5&&!v.paused});
   }return results;
  });
  assert(report.latest.videos.every(v=>v.autoplay&&v.muted&&v.loop&&v.wrapped),'Video behavior failed');
  await page.evaluate(()=>Reveal.slide(0));
  report.latest.userEdits=await page.evaluate(()=>({newStudent:document.querySelector('.slides').textContent.includes('何梓彬'),progressText:Reveal.getSlides()[1].textContent.trim()}));
  assert(report.latest.userEdits.newStudent);assert(!report.latest.userEdits.progressText.includes('Milestones'));
  assert(!report.catalog.some(e=>e.error),'Some catalog pages failed');
  const knownMissing=new Set(['/favicon.ico','/lectures/2025-01-16-recap/neuro.md','/lectures/2025-01-16-recap/semiconductor.md']);
  report.unexpectedLocalFailures=report.localFailures.filter(e=>!knownMissing.has(new URL(e.url).pathname));
  // Historical ABCJS initialization errors were reproduced against original HEAD files.
  // Bare Event errors come from the intentionally blocked external math loaders.
  report.unexpectedConsoleErrors=report.consoleErrors.filter(e=>e!=='Event' && !(e.includes('abcjs-basic-min.js') && /music15b\/week(?:04|05|06|07|10|11|12)\.html/.test(e)));
  assert.equal(report.unexpectedLocalFailures.length,0,'Unexpected missing local resources');
  assert.equal(report.unexpectedConsoleErrors.length,0,'Unexpected browser errors');
  report.passed=true;
 }finally{fs.writeFileSync('portal/validation-browser.json',JSON.stringify(report,null,2)+'\n');await browser.close();}
 console.log(JSON.stringify(report,null,2));
})().catch(err=>{console.error(err);process.exitCode=1});
