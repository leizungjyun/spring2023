# Presentation starters

`reveal-starter/index.html.bak` is the repository's original root HTML starter, moved here with its framework paths rebased. Its `docs/slides-dir/main.md` reference was already a placeholder: it is an archive, not a catalog presentation.

For a new standalone deck, start with `reveal-starter/index.html` (a working two-slide example with annotations), or copy an appropriate existing `collections/.../index.html` launcher into a new deck directory, then point `data-markdown` to `slides.md` and adjust `dist/` and `plugin/` paths for the new depth. Copy deck-specific CSS/JavaScript only when needed. Use `===` for horizontal slides and `==` for vertical slides.

Reusable starter or skill packages belong here, outside actual decks, and are excluded from the portal. No repository copy of the previously packaged `ai-group-presentations.zip` was present at migration time. The installed personal Codex skill is external to this repository and was not modified.

Keep the annotation plugin script tag and `RevealAnnotations` entry in the `plugins` array when copying a starter. Initialize with `Reveal.initialize(options)` as usual. No changes to reveal.js core are needed.
