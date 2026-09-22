# Slide annotations

A standalone reveal.js plugin using public APIs. No changes to reveal.js core are required.

- **D** toggles the pen; **H** toggles the highlighter.
- Drag to draw. **Esc** clears the current slide and exits drawing.
- Marks are per-slide and session-only. No toolbar is displayed.
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
