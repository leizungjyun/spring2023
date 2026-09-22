// Standalone reveal.js plugin. Each Reveal instance owns its ink.
export default () => ({
  id: 'annotations',
  init(Reveal) {
    if (Reveal.isPrintingPDF()) return;
    const root = Reveal.getRevealElement();
    const layers = new Map();
    const ns = 'http://www.w3.org/2000/svg';
    let mode = null, activeLayer = null, stroke = null, pointer = null;

    if (!document.getElementById('reveal-ink-style')) {
      const style = document.createElement('style');
      style.id = 'reveal-ink-style';
      style.textContent = '.reveal > .slide-ink {position:absolute;right:0;bottom:0;max-width:none;max-height:none;margin:auto;z-index:30;pointer-events:none;touch-action:none;cursor:crosshair;} @media print {.reveal .slide-ink {display:none!important;}}';
      document.head.appendChild(style);
    }
    function finishStroke() {
      const captured = pointer;
      pointer = null;
      stroke = null;
      if (captured !== null && activeLayer && activeLayer.hasPointerCapture(captured)) activeLayer.releasePointerCapture(captured);
    }
    function point(event, layer) {
      const p = layer.createSVGPoint();
      p.x = event.clientX;
      p.y = event.clientY;
      const local = p.matrixTransform(layer.getScreenCTM().inverse());
      return `${local.x.toFixed(1)},${local.y.toFixed(1)}`;
    }
    function resize() {
      const size = Reveal.getComputedSlideSize();
      const slidesStyle = getComputedStyle(Reveal.getSlidesElement());
      layers.forEach(layer => {
        // Keep each layer's original coordinate system on resize.
        layer.style.width = `${size.width}px`;
        layer.style.height = `${size.height}px`;
        ['left', 'top', 'right', 'bottom', 'transform', 'transformOrigin', 'zoom'].forEach(property => { layer.style[property] = slidesStyle[property]; });
      });
    }
    function getLayer() {
      const slide = Reveal.getCurrentSlide();
      if (!slide) return null;
      if (!layers.has(slide)) {
        const layer = document.createElementNS(ns, 'svg');
        const size = Reveal.getComputedSlideSize();
        layer.classList.add('slide-ink');
        layer.setAttribute('viewBox', `0 0 ${size.width} ${size.height}`);
        layer.setAttribute('preserveAspectRatio', 'none');
        layer.setAttribute('aria-hidden', 'true');
        layer.setAttribute('data-prevent-swipe', '');
        root.appendChild(layer);
        layers.set(slide, layer);
        resize();
        layer.addEventListener('pointerdown', event => {
          if (!mode || event.button !== 0 || pointer !== null) return;
          event.preventDefault();
          pointer = event.pointerId;
          layer.setPointerCapture(pointer);
          stroke = document.createElementNS(ns, 'polyline');
          stroke.setAttribute('fill', 'none');
          stroke.setAttribute('stroke', mode === 'highlight' ? '#ffd43b' : '#ed3650');
          stroke.setAttribute('stroke-width', mode === 'highlight' ? '20' : '3.5');
          stroke.setAttribute('opacity', mode === 'highlight' ? '.4' : '1');
          stroke.setAttribute('stroke-linecap', 'round');
          stroke.setAttribute('stroke-linejoin', 'round');
          const start = point(event, layer);
          stroke.setAttribute('points', `${start} ${start}`);
          layer.appendChild(stroke);
        });
        layer.addEventListener('pointermove', event => {
          if (!stroke || event.pointerId !== pointer) return;
          event.preventDefault();
          const samples = event.getCoalescedEvents ? event.getCoalescedEvents() : [];
          const points = (samples.length ? samples : [event]).map(e => point(e, layer));
          stroke.setAttribute('points', `${stroke.getAttribute('points')} ${points.join(' ')}`);
        });
        ['pointerup', 'pointercancel', 'lostpointercapture'].forEach(name => layer.addEventListener(name, event => {
          if (event.pointerId === pointer) finishStroke();
        }));
        layer.addEventListener('click', event => event.stopPropagation());
      }
      return layers.get(slide);
    }
    function setMode(next) {
      finishStroke();
      layers.forEach(layer => { layer.style.display = 'none'; layer.style.pointerEvents = 'none'; });
      mode = next;
      activeLayer = getLayer();
      if (activeLayer) {
        activeLayer.style.display = Reveal.isOverview() || Reveal.isPaused() ? 'none' : 'block';
        activeLayer.style.pointerEvents = mode ? 'auto' : 'none';
      }
    }
    function clear() {
      setMode(null);
      if (activeLayer) while (activeLayer.firstChild) activeLayer.removeChild(activeLayer.firstChild);
    }
    function onKey(event) {
      const config = Reveal.getConfig();
      const target = event.target;
      if (!Reveal.isReady() || !root.isConnected || config.keyboard === false) return;
      if ((config.embedded || config.keyboardCondition === 'focused' || document.querySelectorAll('.reveal').length > 1) && !Reveal.isFocused()) return;
      if (typeof config.keyboardCondition === 'function' && config.keyboardCondition(event) === false) return;
      if (document.querySelector('dialog[open],.reveal .overlay') || target.isContentEditable || (target.closest && target.closest('input,textarea,select,[role="textbox"]'))) return;
      if (event.ctrlKey || event.metaKey || event.altKey || event.isComposing || event.repeat) return;
      const key = (event.key || '').toLowerCase();
      if (key === 'escape' && (mode || (activeLayer && activeLayer.childElementCount))) {
        event.preventDefault();
        event.stopImmediatePropagation();
        clear();
      } else if ((key === 'd' || key === 'h') && !Reveal.isOverview() && !Reveal.isPaused()) {
        event.preventDefault();
        event.stopImmediatePropagation();
        const next = key === 'h' ? 'highlight' : 'pen';
        setMode(mode === next ? null : next);
      }
    }
    window.addEventListener('keydown', onKey, true);
    window.addEventListener('blur', finishStroke);
    Reveal.on('slidechanged', () => setMode(mode));
    Reveal.on('resize', resize);
    Reveal.on('overviewshown', () => setMode(null));
    Reveal.on('overviewhidden', () => setMode(null));
    Reveal.on('paused', () => setMode(null));
    Reveal.on('resumed', () => setMode(null));
    Reveal.registerKeyboardShortcut('D', 'Toggle drawing');
    Reveal.registerKeyboardShortcut('H', 'Toggle highlighting');
    Reveal.registerKeyboardShortcut('Esc (with ink)', 'Clear current slide annotations and exit drawing');
  }
});
