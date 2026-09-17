const path=require('path'),fs=require('fs'),assert=require('assert');
const root=path.resolve(__dirname,'../../../../..');
const puppeteer=require(path.join(root,'node_modules/puppeteer'));
const wait=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
 const b=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,pipe:true,args:['--no-sandbox']});
 const report={slides:[],errors:[],mediaInterruptions:[]};
 try{
 const p=await b.newPage();await p.setViewport({width:1440,height:900});
 p.on('pageerror',e=>{if(e.message.startsWith('AbortError: The play() request was interrupted by a call to pause()'))report.mediaInterruptions.push(e.message);else report.errors.push(e.message);});
 await p.setRequestInterception(true);p.on('request',r=>r.url().includes('livereload')?r.abort():r.continue());
 await p.goto('http://localhost:8017/collections/external-presentations/2026-09-15-neuro/index.html');
 await p.waitForFunction('window.Reveal && Reveal.isReady()');
 const indices=await p.evaluate(()=>Reveal.getSlides().map(s=>Reveal.getIndices(s)));
 assert.equal(indices.length,12);
 for(let i=0;i<indices.length;i++){
  const a=indices[i];await p.evaluate(a=>Reveal.slide(a.h,a.v),a);await wait(750);
  const data=await p.evaluate(()=>{const s=Reveal.getCurrentSlide(),r=s.getBoundingClientRect();return{title:s.querySelector('h1,h2').textContent,images:[...s.querySelectorAll('img')].map(e=>({src:e.getAttribute('src'),loaded:e.complete&&e.naturalWidth>0})),overflow:[...s.querySelectorAll('h1,h2,h3,p,table,img,video,figure,li')].filter(e=>!e.closest('aside')).filter(e=>{const q=e.getBoundingClientRect();return q.width&&q.height&&(q.bottom>r.bottom+2||q.right>r.right+2||q.left<r.left-2);}).map(e=>e.tagName+': '+e.textContent.slice(0,70))};});
  report.slides.push(data);await p.screenshot({path:path.join(__dirname,`slide-${String(i+1).padStart(2,'0')}.png`)});
 }
 await p.keyboard.press('Escape');await wait(700);assert(await p.evaluate(()=>Reveal.isOverview()));
 await p.keyboard.press('Escape');await wait(700);assert(!(await p.evaluate(()=>Reveal.isOverview())));report.escapeOverview=true;
 await p.evaluate(()=>Reveal.slide(2,1));await wait(1000);
 report.video=await p.evaluate(async()=>{const v=document.querySelector('video'),started=!v.paused&&v.currentTime>0;v.currentTime=v.duration-.2;await new Promise(r=>setTimeout(r,750));return{started,muted:v.muted,loop:v.loop,wrapped:v.currentTime<1.5&&!v.paused};});
 assert(Object.values(report.video).every(Boolean));
 await p.click('video');await p.keyboard.press('Escape');await wait(700);assert(await p.evaluate(()=>Reveal.isOverview()));
 // Clicking an overview thumbnail must return to a usable slide.
 await p.evaluate(()=>{const s=Reveal.getSlides()[0];s.dispatchEvent(new MouseEvent('click',{bubbles:true}));});await wait(700);
 report.overviewThumbnail=await p.evaluate(()=>!Reveal.isOverview()&&Reveal.getIndices().h===0);assert(report.overviewThumbnail);
 assert(report.slides.every(s=>s.images.every(i=>i.loaded)),'Missing images');
 assert(report.slides.every(s=>!s.overflow.length),'Overflow detected');assert(!report.errors.length);
 report.viewports=[];
 for(const [width,height] of [[1024,768],[1920,1080]]){
  await p.setViewport({width,height});await p.evaluate(()=>Reveal.slide(1,1));await wait(700);
  const fits=await p.evaluate(()=>{const r=Reveal.getCurrentSlide().getBoundingClientRect();return r.left>=-1&&r.top>=-1&&r.right<=innerWidth+1&&r.bottom<=innerHeight+1;});
  assert(fits);report.viewports.push({width,height,fits});
 }
 report.passed=true;
 }finally{fs.writeFileSync(path.join(__dirname,'validation.json'),JSON.stringify(report,null,2));await b.close();}
 console.log(JSON.stringify(report,null,2));
})().catch(e=>{console.error(e);process.exitCode=1});
