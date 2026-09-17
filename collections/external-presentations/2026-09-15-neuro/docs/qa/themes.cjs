const path=require('path'),fs=require('fs'),assert=require('assert');
const puppeteer=require(path.resolve(__dirname,'../../../../../node_modules/puppeteer'));
const wait=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
 const browser=await puppeteer.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,pipe:true,args:['--no-sandbox']});
 const report={themes:[],errors:[]};
 try {
  const page=await browser.newPage();await page.setViewport({width:1440,height:900});
  page.on('pageerror',e=>{if(!e.message.startsWith('AbortError'))report.errors.push(e.message)});
  await page.goto('http://localhost:8017/collections/external-presentations/2026-09-15-neuro/index.html?theme=white',{waitUntil:'domcontentloaded'});
  await page.waitForFunction('window.Reveal && Reveal.isReady() && document.documentElement.dataset.diagramTone === "light"');
  assert((await page.$eval('#theme',e=>e.href)).endsWith('/white.css'));
  const indices=await page.evaluate(()=>Reveal.getSlides().map(s=>Reveal.getIndices(s)));
  for(const theme of ['white','serif','simple','beige','sky','solarized','black','league','night','blood','moon']){
   await page.evaluate(theme=>new Promise(resolve=>{const link=document.querySelector('#theme');if(link.href.endsWith(`/${theme}.css`)){resolve();return}link.addEventListener('load',resolve,{once:true});link.href=`../../../dist/theme/${theme}.css`}),theme);
   const tone=['white','serif','simple','beige','sky','solarized'].includes(theme)?'light':'dark';
   await page.waitForFunction(tone=>document.documentElement.dataset.diagramTone===tone,{},tone);
   await page.evaluate(()=>Promise.all([...document.querySelectorAll('.reveal img')].map(i=>i.decode().catch(()=>{}))));
   const result={theme,tone,issues:[],minContrast:100};
   for(let n=0;n<indices.length;n++){
    await page.evaluate(i=>Reveal.slide(i.h,i.v),indices[n]);await wait(100);
    const data=await page.evaluate(()=>{
     const slide=Reveal.getCurrentSlide(),bounds=slide.getBoundingClientRect();
     function rgb(s){return s.match(/[\d.]+/g).slice(0,3).map(Number)}
     function lum(c){const v=c.map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4});return .2126*v[0]+.7152*v[1]+.0722*v[2]}
     const probe=document.createElement('span');probe.style.color='var(--r-background-color)';document.body.append(probe);const bg=rgb(getComputedStyle(probe).color);probe.remove();
     const issues=[];let min=100;
     for(const e of slide.querySelectorAll('h1,h2,h3,p,li,td,th,small,strong,span,a')){
      if(e.closest('aside')||![...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))continue;
      const q=e.getBoundingClientRect();if(!q.width||!q.height)continue;
      let back=bg;
      for(let a=e;a;a=a.parentElement){const c=getComputedStyle(a).backgroundColor;if(c!=='rgba(0, 0, 0, 0)'&&c!=='transparent'){back=rgb(c);break}}
      const a=lum(rgb(getComputedStyle(e).color)),b=lum(back),ratio=(Math.max(a,b)+.05)/(Math.min(a,b)+.05);min=Math.min(min,ratio);
      if(ratio<4.5)issues.push({text:e.textContent.slice(0,30),contrast:ratio});
      if(q.bottom>bounds.bottom+2||q.left<bounds.left-2||q.right>bounds.right+2)issues.push({text:e.textContent.slice(0,30),overflow:true});
     }
     for(const i of slide.querySelectorAll('img'))if(!i.complete||!i.naturalWidth)issues.push({missing:i.getAttribute('src')});
     return {issues,min};
    });
    result.issues.push(...data.issues.map(i=>({slide:n+1,...i})));result.minContrast=Math.min(result.minContrast,data.min);
    if((theme==='white'&&(n===2||n===8))||(theme==='serif'&&n===6)||(theme==='black'&&n===8)){
     await wait(400);await page.screenshot({path:path.join(__dirname,`theme-${theme}-${n+1}.png`)});
    }
   }
   report.themes.push(result);
  }
  await page.keyboard.press('Escape');await wait(250);assert(await page.evaluate(()=>Reveal.isOverview()));await page.keyboard.press('Escape');
  report.escapeOverview=true;
  const mediaIndex=await page.evaluate(()=>Reveal.getIndices(document.querySelector('video').closest('section')));
  await page.evaluate(i=>Reveal.slide(i.h,i.v),mediaIndex);await wait(800);
  report.video=await page.$eval('video',v=>({muted:v.muted,loop:v.loop,playing:!v.paused&&v.currentTime>0}));
  assert(Object.values(report.video).every(Boolean));
  assert(report.themes.every(t=>!t.issues.length),'Theme contrast or layout issues');assert(!report.errors.length);
  report.passed=true;
 }finally{fs.writeFileSync(path.join(__dirname,'themes.json'),JSON.stringify(report,null,2));await browser.close()}
 console.log(JSON.stringify(report,null,2));
})().catch(e=>{console.error(e);process.exitCode=1});
