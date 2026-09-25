# Slide annotations

A standalone reveal.js plugin using public APIs. No changes to reveal.js core are required.

- **D** toggles the pen; **H** toggles the highlighter; **L** toggles the laser pointer; **R** toggles a reading spotlight.
- While the spotlight is active, **<** decreases its radius and **>** increases it.
- **T** shows or hides the annotation tool panel. The panel contains the modes, undo, redo, and clear controls.
- Drag to draw. **Backspace** undoes the last stroke; **Shift+Backspace** restores it. **Esc** clears the current slide and exits drawing.
- The laser and spotlight follow the pointer while active and leave no mark.
- Annotation tools and the panel remain usable on Reveal's black pause screen (`.`). New pen strokes are white there; the spotlight reveals the slide inside its circle.
- Marks are per-slide and session-only. The tool panel is hidden by default.
- Text inputs, dialogs, print/PDF export, and embedded deck focus are respected.

## Usage

Load the script and register `RevealAnnotations` in the `plugins` array, just like other reveal.js plugins. No shared helper is required.

UMD:

```html
<script src="dist/reveal.js"></script>
<script src="plugin/annotations/annotations.js"></script>
<script>
  Reveal.initialize({ plugins: [RevealAnnotations] });
</script>
```

ES modules:

```js
import Reveal from './dist/reveal.esm.js';
import RevealAnnotations from './plugin/annotations/annotations.esm.js';
new Reveal(document.querySelector('.reveal'), {
  plugins: [RevealAnnotations]
}).initialize();
```

Run `npx gulp plugins` after editing `plugin.js`. Both distribution files are generated; do not hand-edit them. Run `node scripts/check-annotations.cjs http://127.0.0.1:PORT` against a local preview server to check repository integration and the unmodified core.
