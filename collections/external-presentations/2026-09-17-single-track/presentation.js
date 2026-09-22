// Keep theme changes local to this deck; shared Reveal styles are untouched.
const deckThemeLink = document.querySelector('link[href*="dist/theme/"]');
const deckThemes = new Set(['black','white','league','beige','sky','night','serif','simple','solarized','blood','moon']);
const requestedTheme = new URLSearchParams(location.search).get('theme');
if (deckThemes.has(requestedTheme)) {
  deckThemeLink.href = `../../../dist/theme/${requestedTheme}.css`;
}

const diagramNames = new Set(['sim-to-real.svg', 'lane-control.svg']);
const diagramSources = new WeakMap();
const diagramDownloads = new Map();
const diagramVariants = new Map();
// Only original vector illustrations are recolored. Photographs, papers and video
// retain their original colors. The editable SVG files remain the source of truth.
const lightDiagramColors = {
  '#42affa':'#00649e', '#ffbf69':'#854700', '#aab7c3':'#526372',
  '#f5f7fa':'#20272d', '#20272d':'#eaf0f4', '#46515a':'#72808a',
  '#3b4750':'#72808a', '#263b43':'#d8e7ed', '#233944':'#d8e7ed',
  '#263946':'#d8e7ed', '#151e25':'#f7fbfc', '#3c3328':'#f4e5cc'
};
let diagramRevision = 0;
async function adaptDiagrams(tone) {
  const revision = ++diagramRevision;
  delete document.documentElement.dataset.diagramTone;
  await Promise.all([...document.querySelectorAll('.reveal img')].map(async img => {
    let source = diagramSources.get(img);
    if (!source) {
      if (!diagramNames.has(img.getAttribute('src')?.split('/').pop())) return;
      source = img.getAttribute('src');
      diagramSources.set(img, source);
    }
    if (tone === 'dark') {
      img.src = source;
      return;
    }
    try {
      if (!diagramDownloads.has(source)) {
        diagramDownloads.set(source, fetch(source).then(r => {
          if (!r.ok) throw new Error(`Unable to load ${source}`);
          return r.text();
        }));
      }
      const svg = await diagramDownloads.get(source);
      if (!diagramVariants.has(source)) {
        // Replace color values only; marker IDs, geometry and text stay intact.
        const adapted = svg.replace(/#[0-9a-f]{6}\b/gi, color => lightDiagramColors[color.toLowerCase()] || color);
        diagramVariants.set(source, URL.createObjectURL(new Blob([adapted], {type:'image/svg+xml'})));
      }
      if (revision === diagramRevision) img.src = diagramVariants.get(source);
    } catch (error) {
      // Keep original diagrams readable if an asset cannot be fetched.
      if (revision === diagramRevision) img.style.backgroundColor = '#20272d';
      console.warn(error);
    }
  }));
  if (revision === diagramRevision) document.documentElement.dataset.diagramTone = tone;
}
function adaptDeckTheme() {
  const probe = document.createElement('span');
  probe.style.cssText = 'position:absolute;visibility:hidden;color:var(--r-background-color,#191919)';
  document.body.appendChild(probe);
  const rgb = getComputedStyle(probe).color.match(/[\d.]+/g).slice(0,3).map(Number);
  probe.remove();
  const luminance = rgb.map(v => { v /= 255; return v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; });
  const tone = .2126*luminance[0] + .7152*luminance[1] + .0722*luminance[2] > .45 ? 'light' : 'dark';
  document.documentElement.dataset.deckTone = tone;
  adaptDiagrams(tone);
}
// Support both ?theme=white and changing/replacing the theme stylesheet live.
document.head.addEventListener('load', event => {
  if (event.target.matches?.('link[rel="stylesheet"]')) adaptDeckTheme();
}, true);
new MutationObserver(() => requestAnimationFrame(adaptDeckTheme)).observe(document.head, {
  childList:true, subtree:true, attributes:true, attributeFilter:['href']
});
adaptDeckTheme();

Reveal.initialize({
  width: 1200, height: 700, margin: 0.06, hash: true, center: false,
  slideNumber: 'c/t', transition: 'fade',
  plugins: [RevealAnnotations, RevealMarkdown, RevealNotes, RevealSearch, RevealZoom, RevealMath.KaTeX]
});
// Keep media flags explicit; Reveal owns starting and pausing off-slide media.
Reveal.on('ready', () => {
  adaptDeckTheme();
  document.querySelectorAll('video').forEach(video => {
    video.muted = true;
    video.loop = true;
  });
});

// Keep simultaneous galleries active only on the current slide.
function syncSlideVideos() {
  const current = Reveal.getCurrentSlide();
  document.querySelectorAll('video').forEach(video => {
    video.muted = true;
    video.loop = true;
    if (current?.contains(video)) video.play().catch(() => {});
    else video.pause();
  });
}
Reveal.on('ready', () => {
  document.querySelectorAll('video').forEach(video => video.addEventListener('loadeddata', () => {
    if (!Reveal.getCurrentSlide()?.contains(video)) video.pause();
  }));
  syncSlideVideos();
});
Reveal.on('slidechanged', syncSlideVideos);

// Patent viewer lives outside Reveal's scaled canvas, so the full page fits the viewport.
const patentViewer = document.createElement('dialog');
patentViewer.className = 'patent-viewer';
patentViewer.setAttribute('aria-label', '专利全文图片');
patentViewer.innerHTML = '<button type="button" class="patent-viewer-close" aria-label="关闭专利图片">×</button><img alt="">';
document.body.appendChild(patentViewer);
const patentImage = patentViewer.querySelector('img');
const patentClose = patentViewer.querySelector('button');
let patentOpener;
function closePatentViewer() {
  if (!patentViewer.open) return;
  patentViewer.close();
  patentOpener?.focus({preventScroll:true});
}
function openPatentViewer(link) {
  patentOpener = link;
  patentImage.src = link.href;
  patentImage.alt = link.querySelector('img').alt;
  patentViewer.showModal();
  patentClose.focus({preventScroll:true});
}
document.addEventListener('click', event => {
  const link = event.target.closest('.patent-stack a');
  if (!link) return;
  event.preventDefault();
  openPatentViewer(link);
});
patentClose.addEventListener('click', closePatentViewer);
patentViewer.addEventListener('click', event => {
  if (event.target === patentViewer) closePatentViewer();
});
patentViewer.addEventListener('cancel', event => {
  event.preventDefault();
  closePatentViewer();
});
window.addEventListener('keydown', event => {
  if (patentViewer.open) {
    // Escape closes the image only; the next Escape retains Reveal's overview behavior.
    event.stopImmediatePropagation();
    if (event.key === 'Escape') {
      event.preventDefault();
      closePatentViewer();
    } else if (event.key === 'Tab') {
      event.preventDefault();
      patentClose.focus();
    }
  } else if (event.key === ' ' && event.target.matches('.patent-stack a')) {
    event.preventDefault();
    event.stopImmediatePropagation();
    openPatentViewer(event.target);
  }
}, true);
Reveal.on('slidechanged', closePatentViewer);
