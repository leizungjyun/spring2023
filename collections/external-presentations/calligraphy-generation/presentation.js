Reveal.initialize({
  width: 1200, height: 700, margin: 0.06, hash: true, center: false,
  slideNumber: 'c/t',
  plugins: [RevealAnnotations, RevealMarkdown, RevealNotes]
});

// Patent viewer lives outside Reveal's scaled canvas, so the full page fits the viewport.
const patentViewer = document.createElement('dialog');
patentViewer.className = 'patent-viewer';
patentViewer.setAttribute('aria-label', '图片放大预览');
patentViewer.innerHTML = '<button type="button" class="patent-viewer-close" aria-label="关闭图片">×</button><img alt="">';
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
  const link = event.target.closest('.patent-preview, .figure-preview');
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
  } else if (event.key === ' ' && event.target.matches('.patent-preview, .figure-preview')) {
    event.preventDefault();
    event.stopImmediatePropagation();
    openPatentViewer(event.target);
  }
}, true);
Reveal.on('slidechanged', closePatentViewer);
