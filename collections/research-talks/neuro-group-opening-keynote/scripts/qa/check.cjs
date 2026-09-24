// Run from any directory. BASE_URL, CHROME_PATH and QA_OUTPUT are configurable.
const path = require('path');
const fs = require('fs');
const deck = path.resolve(__dirname, '../..');
const puppeteer = require(path.resolve(deck, '../../../node_modules/puppeteer'));
const baseUrl = process.argv[2] || process.env.BASE_URL || 'http://127.0.0.1:8000';
const url = new URL('/collections/research-talks/neuro-group-opening-keynote/', baseUrl).href;
const output = process.env.QA_OUTPUT || path.join(deck, 'qa');
const screenshots = path.join(output, 'screenshots');
fs.mkdirSync(screenshots, {recursive:true});
fs.mkdirSync(path.join(output, 'reports'), {recursive:true});
(async () => {
  const browser = await puppeteer.launch({headless:true, pipe:true,
    executablePath:process.env.CHROME_PATH || undefined, args:['--no-sandbox']});
  try {
    const page = await browser.newPage();
    const errors = [], requests = [];
    page.on('pageerror', e=>errors.push(e.message));
    page.on('requestfailed', r=>errors.push(r.url()+' '+r.failure().errorText));
    page.on('response', r=>{if (r.status()>=400) errors.push(r.status()+' '+r.url());});
    page.on('request', r=>requests.push(r.url()));
    await page.setViewport({width:1440,height:900});
    await page.goto(url, {waitUntil:'networkidle0'});
    await page.waitForFunction('window.Reveal && Reveal.isReady() && document.documentElement.dataset.chartsReady === "true"');
    await page.evaluate(()=>Reveal.configure({transition:'none'}));
    const count = await page.evaluate(()=>Reveal.getTotalSlides());
    const slides = [];
    for (let i=0;i<count;i++) {
      await page.evaluate(i=>{const index=Reveal.getIndices(Reveal.getSlides()[i]);Reveal.slide(index.h,index.v);},i);
      await page.waitFor(250);
      slides.push(await page.evaluate(()=>{
        const s=Reveal.getCurrentSlide(),r=s.getBoundingClientRect();
        // The closing slide is a full-bleed image with no heading, so fall back to the
        // section's own class rather than failing the whole run on it. It is also the one
        // slide where content is meant to reach the slide edge, so the flow-fence check
        // does not apply to it.
        const heading=s.querySelector('h1,h2'),fullBleed=s.classList.contains('ending-slide');
        // .takeaway is absolutely positioned, so flow content can run underneath it
        // without leaving the slide. Treat its top edge as the fence, and fall back to
        // the section's own bottom padding when a slide has no such element.
        const fence=Math.min(...[...s.querySelectorAll('.takeaway')].map(f=>f.getBoundingClientRect().top), r.bottom-30);
        return {title:heading?heading.innerText:'['+s.className+']',indices:Reveal.getIndices(),
          brokenImages:[...s.querySelectorAll('img')].filter(x=>!x.complete||!x.naturalWidth).map(x=>x.getAttribute('src')),
          overflow:[...s.querySelectorAll('h1,h2,h3,p,img,.chart-inspector')].filter(x=>!x.closest('aside')&&x.getBoundingClientRect().bottom>r.bottom+2).map(x=>x.className||x.tagName),
          collisions:fullBleed?[]:[...s.querySelectorAll('h1,h2,h3,p,img,.chart-inspector')].filter(x=>!x.closest('aside')&&!x.closest('.source,.takeaway')&&x.getBoundingClientRect().bottom>fence-2).map(x=>x.className||x.tagName)};
      }));
      await page.screenshot({path:path.join(screenshots,`slide-${String(i+1).padStart(2,'0')}.png`)});
    }
    // Target whichever slide holds the chart, so reordering the deck cannot silently
    // point the hover checks at a slide with no chart on it.
    await page.evaluate(()=>{const i=Reveal.getIndices(document.getElementById('training-chart').closest('section'));Reveal.slide(i.h,i.v);});
    await page.waitFor(250);
    const hoverChecks = [];
    for (const viewport of [{width:1440,height:900},{width:1000,height:700}]) {
      await page.setViewport(viewport);await page.waitFor(350);
      // Use the actual rendered marker centre, not Plotly's unscaled data coordinates.
      const point = await page.evaluate(()=>{
        const el=document.querySelector('#training-chart .scatterlayer .trace .point');
        const r=el.getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2};
      });
      await page.mouse.move(5,5);await page.mouse.move(point.x,point.y);await page.waitFor(250);
      hoverChecks.push(await page.evaluate(viewport=>({viewport,tooltip:document.querySelector('#training-chart .hoverlayer').textContent,selected:document.getElementById('model-detail').dataset.model}),viewport));
    }
    await page.select('#model-select','0');
    const selection = await page.$eval('#model-detail',el=>({model:el.dataset.model,link:el.querySelector('a').href}));
    await page.keyboard.press('Escape');
    const overviewOpened = await page.evaluate(()=>Reveal.isOverview());
    await page.keyboard.press('Escape');
    const overviewClosed = await page.evaluate(()=>!Reveal.isOverview());
    const plugins = await page.evaluate(()=>({annotations:Reveal.hasPlugin('annotations'),notes:Reveal.hasPlugin('notes')}));
    const externalRequests = requests.filter(u=>/^https?:/.test(u)&&!u.startsWith(new URL(url).origin));
    const report={count,slides,hoverChecks,selection,overviewOpened,overviewClosed,plugins,errors,externalRequests};
    fs.writeFileSync(path.join(output,'reports/browser.json'),JSON.stringify(report,null,2)+'\n');
    console.log(JSON.stringify(report,null,2));
    if(count!==20||slides.some(s=>s.brokenImages.length||s.overflow.length||s.collisions.length)||errors.length||externalRequests.length||hoverChecks.some(x=>!x.tooltip||x.selected!=='BERT-Large')||!overviewOpened||!overviewClosed||!plugins.annotations)process.exitCode=1;
  } finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exitCode=1;});
