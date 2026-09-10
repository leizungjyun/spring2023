// Plotly lives in an iframe so reveal.js scaling cannot distort pointer coordinates.
Reveal.initialize({width:1200,height:700,margin:.06,hash:true,slideNumber:'c/t',
  transition:'fade',plugins:[RevealMarkdown,RevealNotes,RevealSearch,RevealZoom]
});

// reveal.js 4 uses CSS zoom when enlarging on low-DPI displays. CSS zoom
// changes iframe viewport coordinates; use transform scaling consistently.
function normalizeSlideScale() {
  const slides = document.querySelector('.reveal .slides');
  // Overview owns the full transform while the slide grid is visible.
  if (!slides || !slides.style.zoom || Reveal.isOverview()) return;
  slides.style.zoom = '';
  slides.style.left = '50%';
  slides.style.top = '50%';
  slides.style.bottom = 'auto';
  slides.style.right = 'auto';
  slides.style.transform = `translate(-50%, -50%) scale(${Reveal.getScale()})`;
}
Reveal.on('ready', normalizeSlideScale);
Reveal.on('resize', normalizeSlideScale);
// Layout may reapply zoom without emitting resize when the scale is unchanged.
new MutationObserver(normalizeSlideScale).observe(
  document.querySelector('.reveal .slides'), {attributes:true, attributeFilter:['style']}
);
