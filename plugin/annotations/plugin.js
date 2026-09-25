// Standalone reveal.js plugin. Each Reveal instance owns its ink.
export default () => ({
  id: 'annotations',
  init(Reveal) {
    if (Reveal.isPrintingPDF()) return;
    const root = Reveal.getRevealElement();
    const layers = new Map();
    const undone = new Map();
    const ns = 'http://www.w3.org/2000/svg';
    let mode = null, activeLayer = null, stroke = null, pointer = null;
    let panelVisible = false;
    let spotlightRadius = 110;

    if (!document.getElementById('reveal-ink-style')) {
      const style = document.createElement('style');
      style.id = 'reveal-ink-style';
      style.textContent = '.reveal > .slide-ink {position:absolute;right:0;bottom:0;max-width:none;max-height:none;margin:auto;z-index:30;pointer-events:none;touch-action:none;cursor:crosshair;} .reveal.paused > .slide-ink {z-index:110;} .reveal.paused.ink-spotlight-reveal .pause-overlay {-webkit-mask-image:radial-gradient(circle var(--ink-radius) at var(--ink-x) var(--ink-y),transparent calc(var(--ink-radius) - 1px),black var(--ink-radius));mask-image:radial-gradient(circle var(--ink-radius) at var(--ink-x) var(--ink-y),transparent calc(var(--ink-radius) - 1px),black var(--ink-radius));} .reveal > .slide-ink.laser-mode,.reveal > .slide-ink.spotlight-mode {cursor:none;} .reveal > .slide-ink .laser-dot {filter:drop-shadow(0 0 5px #ed3650);} .reveal > .slide-ink-tools {position:absolute;right:20px;bottom:90px;z-index:40;display:flex;flex-wrap:wrap;gap:5px;max-width:min(680px,calc(100% - 40px));padding:8px;background:rgba(255,255,255,.96);border:1px solid #aebdc7;border-radius:8px;box-shadow:0 4px 18px rgba(0,0,0,.2);font-family:Arial,sans-serif;} .reveal.paused > .slide-ink-tools {z-index:120;} .reveal > .slide-ink-tools[hidden] {display:none;} .reveal > .slide-ink-tools button {font:500 14px Arial,sans-serif;color:#203441;background:#f5f8fa;border:1px solid #bdcbd4;border-radius:5px;padding:7px 10px;cursor:pointer;} .reveal > .slide-ink-tools button[aria-pressed="true"] {color:white;background:#00649e;border-color:#00649e;} .reveal > .slide-ink-tools button:focus-visible {outline:2px solid #b76b29;outline-offset:2px;} @media print {.reveal .slide-ink,.reveal .slide-ink-tools {display:none!important;}}';
      document.head.appendChild(style);
    }
    const panel = document.createElement('div');
    panel.className = 'slide-ink-tools';
    panel.setAttribute('role', 'toolbar');
    panel.setAttribute('aria-label', 'Annotation tools');
    panel.hidden = true;
    [
      ['pen', 'Pen · D'], ['highlight', 'Highlight · H'],
      ['laser', 'Laser · L'], ['spotlight', 'Read · R'],
      ['undo', 'Undo'], ['redo', 'Redo'], ['clear', 'Clear']
    ].forEach(([action, label]) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.dataset.action = action;
      button.textContent = label;
      button.setAttribute('aria-label', label);
      panel.appendChild(button);
    });
    panel.addEventListener('pointerdown', event => event.stopPropagation());
    panel.addEventListener('click', event => {
      event.stopPropagation();
      const action = event.target.closest('button')?.dataset.action;
      if (action === 'undo') undo();
      else if (action === 'redo') redo();
      else if (action === 'clear') clear();
      else if (action) setMode(mode === action ? null : action);
    });
    root.appendChild(panel);
    function updatePanel() {
      panel.hidden = !panelVisible || Reveal.isOverview();
      panel.querySelectorAll('button').forEach(button => {
        if (['pen', 'highlight', 'laser', 'spotlight'].includes(button.dataset.action)) {
          button.setAttribute('aria-pressed', String(mode === button.dataset.action));
        }
      });
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
    function updateSpotlightReveal(event, layer) {
      if (!Reveal.isPaused()) return;
      const rootBounds = root.getBoundingClientRect();
      root.style.setProperty('--ink-x', `${event.clientX - rootBounds.left}px`);
      root.style.setProperty('--ink-y', `${event.clientY - rootBounds.top}px`);
      root.style.setProperty('--ink-radius', `${spotlightRadius * layer.getBoundingClientRect().width / Reveal.getComputedSlideSize().width}px`);
      root.classList.add('ink-spotlight-reveal');
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
          if (!mode || mode === 'laser' || mode === 'spotlight' || event.button !== 0 || pointer !== null) return;
          event.preventDefault();
          undone.delete(slide);
          pointer = event.pointerId;
          layer.setPointerCapture(pointer);
          stroke = document.createElementNS(ns, 'polyline');
          stroke.setAttribute('fill', 'none');
          stroke.setAttribute('stroke', mode === 'highlight' ? '#ffd43b' : Reveal.isPaused() ? '#ffffff' : '#ed3650');
          stroke.setAttribute('stroke-width', mode === 'highlight' ? '20' : '3.5');
          stroke.setAttribute('opacity', mode === 'highlight' ? '.4' : '1');
          stroke.setAttribute('stroke-linecap', 'round');
          stroke.setAttribute('stroke-linejoin', 'round');
          const start = point(event, layer);
          stroke.setAttribute('points', `${start} ${start}`);
          layer.appendChild(stroke);
        });
        layer.addEventListener('pointermove', event => {
          if (mode === 'laser') {
            const dot = layer.querySelector('.laser-dot');
            if (dot) {
              const [x, y] = point(event, layer).split(',');
              dot.setAttribute('cx', x);
              dot.setAttribute('cy', y);
              dot.style.display = 'block';
            }
          }
          if (mode === 'spotlight') {
            const hole = layer.querySelector('.spotlight-hole');
            const shade = layer.querySelector('.spotlight-shade');
            if (hole && shade) {
              const [x, y] = point(event, layer).split(',');
              hole.setAttribute('cx', x);
              hole.setAttribute('cy', y);
              shade.style.display = 'block';
              updateSpotlightReveal(event, layer);
            }
          }
          if (!stroke || event.pointerId !== pointer) return;
          event.preventDefault();
          const samples = event.getCoalescedEvents ? event.getCoalescedEvents() : [];
          const points = (samples.length ? samples : [event]).map(e => point(e, layer));
          stroke.setAttribute('points', `${stroke.getAttribute('points')} ${points.join(' ')}`);
        });
        ['pointerup', 'pointercancel', 'lostpointercapture'].forEach(name => layer.addEventListener(name, event => {
          if (event.pointerId === pointer) finishStroke();
        }));
        layer.addEventListener('pointerleave', () => {
          const dot = layer.querySelector('.laser-dot');
          if (dot) dot.style.display = 'none';
          const shade = layer.querySelector('.spotlight-shade');
          if (shade) shade.style.display = 'none';
          root.classList.remove('ink-spotlight-reveal');
        });
        layer.addEventListener('click', event => event.stopPropagation());
      }
      return layers.get(slide);
    }
    function setMode(next) {
      finishStroke();
      root.classList.remove('ink-spotlight-reveal');
      layers.forEach(layer => {
        layer.style.display = 'none';
        layer.style.pointerEvents = 'none';
        layer.classList.remove('laser-mode');
        layer.classList.remove('spotlight-mode');
        const dot = layer.querySelector('.laser-dot');
        if (dot) dot.remove();
        const spotlight = layer.querySelector('.spotlight');
        if (spotlight) spotlight.remove();
      });
      mode = next;
      activeLayer = getLayer();
      if (activeLayer) {
        activeLayer.style.display = Reveal.isOverview() ? 'none' : 'block';
        activeLayer.style.pointerEvents = mode ? 'auto' : 'none';
        if (mode === 'laser') {
          activeLayer.classList.add('laser-mode');
          const dot = document.createElementNS(ns, 'circle');
          dot.classList.add('laser-dot');
          dot.setAttribute('r', '7');
          dot.setAttribute('fill', '#ed3650');
          dot.style.display = 'none';
          activeLayer.appendChild(dot);
        } else if (mode === 'spotlight') {
          activeLayer.classList.add('spotlight-mode');
          const group = document.createElementNS(ns, 'g');
          group.classList.add('spotlight');
          const mask = document.createElementNS(ns, 'mask');
          const maskId = `reveal-spotlight-${Math.random().toString(36).slice(2)}`;
          mask.id = maskId;
          const maskBase = document.createElementNS(ns, 'rect');
          maskBase.setAttribute('width', '100%');
          maskBase.setAttribute('height', '100%');
          maskBase.setAttribute('fill', 'white');
          const hole = document.createElementNS(ns, 'circle');
          hole.classList.add('spotlight-hole');
          hole.setAttribute('r', String(spotlightRadius));
          hole.setAttribute('fill', 'black');
          mask.append(maskBase, hole);
          const defs = document.createElementNS(ns, 'defs');
          defs.appendChild(mask);
          const shade = document.createElementNS(ns, 'rect');
          shade.classList.add('spotlight-shade');
          shade.setAttribute('width', '100%');
          shade.setAttribute('height', '100%');
          shade.setAttribute('fill', 'rgba(0,0,0,.72)');
          shade.setAttribute('mask', `url(#${maskId})`);
          shade.style.display = 'none';
          group.append(defs, shade);
          activeLayer.appendChild(group);
        }
      }
      updatePanel();
    }
    function clear() {
      setMode(null);
      if (activeLayer) while (activeLayer.firstChild) activeLayer.removeChild(activeLayer.firstChild);
      undone.delete(Reveal.getCurrentSlide());
    }
    function undo() {
      if (!activeLayer) return;
      const marks = activeLayer.querySelectorAll('polyline');
      const last = marks[marks.length - 1];
      if (!last) return;
      const slide = Reveal.getCurrentSlide();
      if (!undone.has(slide)) undone.set(slide, []);
      undone.get(slide).push(last);
      last.remove();
    }
    function redo() {
      const history = undone.get(Reveal.getCurrentSlide());
      if (activeLayer && history && history.length) activeLayer.appendChild(history.pop());
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
      if (key === 'escape' && (mode || (activeLayer && activeLayer.querySelector('polyline')))) {
        event.preventDefault();
        event.stopImmediatePropagation();
        clear();
      } else if ((key === '<' || key === '>') && mode === 'spotlight' && !Reveal.isOverview()) {
        event.preventDefault();
        event.stopImmediatePropagation();
        spotlightRadius = Math.max(40, Math.min(300, spotlightRadius + (key === '>' ? 20 : -20)));
        const hole = activeLayer && activeLayer.querySelector('.spotlight-hole');
        if (hole) hole.setAttribute('r', String(spotlightRadius));
        if (Reveal.isPaused() && activeLayer) root.style.setProperty('--ink-radius', `${spotlightRadius * activeLayer.getBoundingClientRect().width / Reveal.getComputedSlideSize().width}px`);
      } else if (key === 'backspace' && !Reveal.isOverview()) {
        event.preventDefault();
        event.stopImmediatePropagation();
        finishStroke();
        if (event.shiftKey) redo(); else undo();
      } else if (key === 't' && !Reveal.isOverview()) {
        event.preventDefault();
        event.stopImmediatePropagation();
        panelVisible = !panelVisible;
        updatePanel();
      } else if ((key === 'd' || key === 'h' || key === 'l' || key === 'r') && !Reveal.isOverview()) {
        event.preventDefault();
        event.stopImmediatePropagation();
        const next = key === 'h' ? 'highlight' : key === 'l' ? 'laser' : key === 'r' ? 'spotlight' : 'pen';
        setMode(mode === next ? null : next);
      }
    }
    window.addEventListener('keydown', onKey, true);
    window.addEventListener('blur', finishStroke);
    Reveal.on('slidechanged', () => setMode(mode));
    Reveal.on('resize', resize);
    Reveal.on('overviewshown', () => setMode(null));
    Reveal.on('overviewhidden', () => setMode(null));
    Reveal.on('paused', () => setMode(mode));
    Reveal.on('resumed', () => setMode(mode));
    Reveal.registerKeyboardShortcut('D', 'Toggle drawing');
    Reveal.registerKeyboardShortcut('H', 'Toggle highlighting');
    Reveal.registerKeyboardShortcut('L', 'Toggle laser pointer');
    Reveal.registerKeyboardShortcut('R', 'Toggle reading spotlight');
    Reveal.registerKeyboardShortcut('< / >', 'Decrease / increase spotlight radius');
    Reveal.registerKeyboardShortcut('T', 'Toggle annotation tool panel');
    Reveal.registerKeyboardShortcut('Backspace', 'Undo last stroke');
    Reveal.registerKeyboardShortcut('Shift+Backspace', 'Redo last stroke');
    Reveal.registerKeyboardShortcut('Esc (with ink)', 'Clear current slide annotations and exit drawing');
  }
});
