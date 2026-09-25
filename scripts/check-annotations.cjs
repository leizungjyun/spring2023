/* Local browser regression: node scripts/check-annotations.cjs [http://127.0.0.1:8023] */
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');
const base = process.argv[2] || 'http://127.0.0.1:8023';
function deckFiles(dir = '.') {
  return fs.readdirSync(dir, {withFileTypes:true}).flatMap(entry => {
    if (['node_modules','.git','docs','test','plugin'].includes(entry.name)) return [];
    const file = path.join(dir, entry.name);
    if (entry.isDirectory()) return deckFiles(file);
    return file.endsWith('.html') && /<script[^>]+src=["'][^"']*dist\/reveal\.js/.test(fs.readFileSync(file,'utf8')) ? [file] : [];
  });
}
(async () => {
  const browser = await puppeteer.launch({executablePath: process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless:true, args:['--no-sandbox']});
  try {
    const page = await browser.newPage();
    await page.setViewport({width:1440,height:900});
    await page.setRequestInterception(true);
    page.on('request', r => {
      if (r.url() === base + '/__ink-core') return r.respond({status:200,contentType:'text/html',body:'<link rel="stylesheet" href="/dist/reveal.css"><div class="reveal"><div class="slides"><section>First</section><section>Second</section></div></div><script src="/dist/reveal.js"></script><script>Reveal.initialize();</script>'});
      if (r.url() === base + '/__ink-esm') return r.respond({status:200,contentType:'text/html',body:'<link rel="stylesheet" href="/dist/reveal.css"><div class="reveal"><div class="slides"><section>ES module test</section></div></div><script type="module">import Reveal from "/dist/reveal.esm.js"; import RevealAnnotations from "/plugin/annotations/annotations.esm.js"; window.Reveal=new Reveal(document.querySelector(".reveal"),{plugins:[RevealAnnotations]});window.Reveal.initialize();</script>'});
      if (/^https?:/.test(r.url()) && !r.url().startsWith(base + '/')) r.abort(); else r.continue();
    });
    const errors = [];
    page.on('pageerror', e => { errors.push({url:page.url(),message:e.message});  });
    async function draw(root = '.reveal', tool = 'h') {
      await page.keyboard.press(tool);
      const box = await page.$eval(root+' .slide-ink[style*="display: block"]',e=>{const r=e.getBoundingClientRect(),s=e.closest('.reveal').querySelector('.slides').getBoundingClientRect();return {x:r.left+r.width*.35,y:r.top+r.height*.4,aligned:Math.abs(r.left-s.left)<1 && Math.abs(r.top-s.top)<1 && Math.abs(r.width-s.width)<1 && Math.abs(r.height-s.height)<1};});
      assert(box.aligned,root+' annotation overlay must align with slides');
      await page.mouse.move(box.x,box.y);await page.mouse.down();await page.mouse.move(box.x+80,box.y+30,{steps:5});await page.mouse.up();
      return page.$eval(root+' .slide-ink[style*="display: block"] polyline',e=>({color:e.getAttribute('stroke'),points:e.getAttribute('points').split(' ').length}));
    }
    await page.goto(base+'/__ink-core');
    await page.waitForFunction('Reveal.isReady()');
    assert.equal(await page.evaluate(()=>Reveal.hasPlugin('annotations')),false);
    await page.evaluate(()=>Reveal.slide(1));
    await page.keyboard.press('h');
    assert.equal(await page.evaluate(()=>Reveal.getIndices().h),0,'Unmodified core retains H navigation');
    assert.equal(await page.$('.slide-ink'),null);
    const files = deckFiles().filter(f=>!f.endsWith('multiple-presentations.html'));
    for (const file of [...files,'__ink-esm']) {
      await page.goto(base+'/'+file,{waitUntil:'domcontentloaded'});
      await page.waitForFunction('window.Reveal && Reveal.isReady()', {timeout:15000});
      assert(await page.evaluate(()=>Reveal.hasPlugin('annotations')),file);
      const before = await page.evaluate(()=>JSON.stringify(Reveal.getIndices()));
      const mark = await draw();assert.equal(mark.color,'#ffd43b',file);assert(mark.points>2,file);
      assert.equal(await page.evaluate(()=>JSON.stringify(Reveal.getIndices())),before,file+' H must not navigate');
      await page.keyboard.press('Backspace');assert.equal(await page.$$eval('.slide-ink polyline',e=>e.length),0,file+' undo');
      await page.keyboard.down('Shift');await page.keyboard.press('Backspace');await page.keyboard.up('Shift');
      assert.equal(await page.$$eval('.slide-ink polyline',e=>e.length),1,file+' redo');
      await page.keyboard.press('l');
      const laser = await page.$eval('.slide-ink[style*="display: block"]',e=>{const r=e.getBoundingClientRect();return{x:r.left+r.width/2,y:r.top+r.height/2};});
      await page.mouse.move(laser.x,laser.y);
      assert.equal(await page.$eval('.slide-ink .laser-dot',e=>e.style.display),'block',file+' laser');
      assert.equal(await page.$$eval('.slide-ink polyline',e=>e.length),1,file+' laser leaves ink unchanged');
      await page.keyboard.press('r');await page.mouse.move(laser.x+20,laser.y+20);
      assert.equal(await page.$eval('.slide-ink .spotlight-shade',e=>e.style.display),'block',file+' spotlight');
      assert.equal(await page.$$eval('.slide-ink polyline',e=>e.length),1,file+' spotlight leaves ink unchanged');
      const radius = Number(await page.$eval('.slide-ink .spotlight-hole',e=>e.getAttribute('r')));
      await page.keyboard.down('Shift');await page.keyboard.press('Period');await page.keyboard.up('Shift');
      assert.equal(Number(await page.$eval('.slide-ink .spotlight-hole',e=>e.getAttribute('r'))),radius+20,file+' larger spotlight');
      await page.keyboard.down('Shift');await page.keyboard.press('Comma');await page.keyboard.up('Shift');
      assert.equal(Number(await page.$eval('.slide-ink .spotlight-hole',e=>e.getAttribute('r'))),radius,file+' smaller spotlight');
      await page.keyboard.press('t');
      assert.equal(await page.$eval('.slide-ink-tools',e=>e.hidden),false,file+' tool panel opens');
      await page.click('.slide-ink-tools button[data-action="pen"]');
      assert.equal(await page.$eval('.slide-ink-tools button[data-action="pen"]',e=>e.getAttribute('aria-pressed')),'true',file+' panel changes tool');
      await page.keyboard.press('t');
      assert.equal(await page.$eval('.slide-ink-tools',e=>e.hidden),true,file+' tool panel closes');
      await page.keyboard.press('Escape');
      assert.equal(await page.$$eval('.slide-ink polyline',e=>e.length),0,file);
      assert.equal(await page.evaluate(()=>Reveal.isOverview()),false,file);
      assert.equal(await page.$eval('.slide-ink-tools',e=>e.hidden),true,file);
      console.log('PASS '+file);
    }
    await page.goto(base+'/collections/research-talks/neuro-group-opening-keynote/');
    await page.waitForFunction('Reveal.isReady()');
    await page.keyboard.press('Period');
    assert(await page.evaluate(()=>Reveal.isPaused()),'period pauses the presentation');
    await page.keyboard.press('t');
    assert.equal(await page.$eval('.slide-ink-tools',e=>e.hidden),false,'tool panel works while paused');
    assert.equal((await draw('.reveal','d')).color,'#ffffff','pen draws in white while paused');
    assert.equal(await page.$eval('.slide-ink polyline',e=>e.getAttribute('stroke')),'#ffffff','drawing works while paused');
    await page.keyboard.press('Backspace');assert.equal(await page.$$eval('.slide-ink polyline',e=>e.length),0,'undo works while paused');
    await page.keyboard.press('r');
    await page.mouse.move(720,450);
    assert(await page.evaluate(()=>document.querySelector('.reveal').classList.contains('ink-spotlight-reveal')),'spotlight reveals slide through pause screen');
    await page.keyboard.press('Period');assert.equal(await page.evaluate(()=>Reveal.isPaused()),false,'period resumes the presentation');
    assert.equal(await page.$eval('.slide-ink-tools',e=>e.hidden),false,'tool panel survives pause');
    await page.goto(base+'/collections/external-presentations/2026-09-17-single-track/');
    await page.waitForFunction('Reveal.isReady()');
    assert.equal((await draw('.reveal','d')).color,'#ed3650');
    await page.keyboard.press('ArrowRight');assert.equal(await page.$eval('.slide-ink[style*="display: block"]',e=>e.childElementCount),0);
    await page.waitForFunction(()=>[...Reveal.getCurrentSlide().querySelectorAll('video')].every(v=>v.readyState>=2 && v.currentTime>0));
    await page.keyboard.press('ArrowLeft');assert.equal(await page.$eval('.slide-ink[style*="display: block"]',e=>e.childElementCount),1);
    await page.setViewport({width:1100,height:750});assert.equal(await page.$eval('.slide-ink[style*="display: block"]',e=>e.childElementCount),1);
    await page.keyboard.press('Escape');await page.keyboard.press('Escape');assert(await page.evaluate(()=>Reveal.isOverview()));await page.keyboard.press('Escape');
    await page.evaluate(()=>{const input=document.createElement('input');document.body.appendChild(input);input.focus();});await page.keyboard.type('hd');assert.equal(await page.$eval('body > input',e=>e.value),'hd');await page.evaluate(()=>document.querySelector('body > input').remove());
    await page.evaluate(()=>{const s=Reveal.getSlides().find(s=>s.querySelector('.patent-stack')),i=Reveal.getIndices(s);Reveal.slide(i.h,i.v);});await new Promise(r=>setTimeout(r,400));await page.click('.present .patent-stack a');await page.keyboard.press('Escape');assert.equal(await page.$eval('.patent-viewer',e=>e.open),false);
    await page.goto(base+'/examples/multiple-presentations.html');await page.waitForFunction('deck1.isReady() && deck2.isReady()');await page.click('.deck2');assert.equal((await draw('.deck2')).color,'#ffd43b');assert.equal(await page.$$('.deck1 .slide-ink').then(e=>e.length),0);await page.keyboard.press('Escape');
    await page.goto(base+'/examples/barebones.html?print-pdf');await page.waitForFunction('Reveal.isReady()');await page.keyboard.press('d');assert.equal(await page.$('.slide-ink'),null);
    // Existing ABC editor failures and blocked remote math scripts were reproduced
    // against the original runtime; all other browser errors remain failures.
    const unexpected = errors.filter(e => e.message !== 'Event' && !(e.url.includes('/music15b/') && e.message.includes('abcjs-basic-min.js') && e.message.includes('initEditor')));
    assert.deepEqual(unexpected,[],JSON.stringify(unexpected,null,2));
    console.log(`Known legacy/blocked-resource errors: ${errors.length}`);
    console.log(`PASS ${files.length} deck entrypoints + ESM; navigation, resize, input, dialogs, embedded decks, print exclusion`);
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exit(1);});
