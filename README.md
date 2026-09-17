# Presentation library

A static library of research talks, group meetings, project presentations, courses and music. Open the root `index.html` through the local server to browse, search and filter the catalog.

## Local preview

```sh
npm install       # only when dependencies are not already installed
npm start
```

Open **http://localhost:8000/**. To choose another port: `npm start -- --port 8017`. When running multiple previews, also choose a separate live-reload port, for example `npm start -- --port 8017 --livereload-port 35731`. The server watches nested presentation content, local assets, templates and portal files for live reload. No backend is required. Opening HTML directly via `file://` is not supported because Markdown and catalog data are fetched.

Static hosting uses the same directory tree: publish the repository's static files, including `dist/`, `plugin/`, `collections/`, `assets/`, `portal/`, and legacy redirect pages. Relative links also work under a project subdirectory. Do not publish `.git/` or `node_modules/`. Publishing is a separate action; this reorganization does not deploy anything.

## Drawing and highlighting

Every deck using the shared reveal.js runtime supports **D** to toggle drawing, **H** to toggle highlighting, and **Esc** to clear the current slide's marks and exit drawing mode. Drag with the mouse while a tool is active. Press the same tool key again to return to normal links and video controls without clearing marks. There is no on-slide toolbar. Use the left arrow to navigate left; H is reserved for highlighting.

Marks stay with their slide for the current session, follow resizing and fullscreen, and disappear on reload. They are omitted from print/PDF export. With no marks or active tool, Esc retains its usual overview behavior; open dialogs and text inputs retain their own keyboard handling. For embedded presentations, click a deck to focus it first.

The built-in plugin lives in `plugin/annotations/plugin.js` and is registered by `js/reveal.js`. After editing it, run `npx gulp js` to regenerate both shared bundles in `dist/`; no per-deck script or stylesheet is required.

## Organization

```text
index.html                    Presentation-library portal
portal/                       Catalog, portal styles/script, migration records
collections/
  group-meetings/              Internal gatherings, recaps and discussions
  research-talks/              Research-topic presentations
  projects/                   Kickoffs, progress reports and project entrypoints
  external-presentations/     Presentations for external audiences
  teaching/
    music15b/                 Weekly lessons in their original sequence
    deep-learning/            Deep-learning course and applied-math review
    scientific-communication/ Academic English and seminar skills
  music/                      Piano-group presentations and concert programs
assets/presentations/         Shared and historically unassigned assets
templates/                   Reusable starters (not catalog presentations)
lectures/neuralmorphic_kickoff/ Registered Git submodule, retained in place
```

Standalone decks normally contain `index.html`, `slides.md`, optional `presentation.css` / `presentation.js`, and `images/`, `videos/`, `docs/` as needed. Courses retain sensible lesson filenames and shared assets. Framework directories (`js`, `css`, `dist`, `plugin`, `examples`, `test`) are shared across decks.

The Projects launcher for the neuromorphic kickoff opens the original submodule presentation. To populate it in a fresh clone, run `git submodule update --init lectures/neuralmorphic_kickoff` when you have access to its configured private remote. Keep the submodule's working changes intact; do not copy its files into the parent repository. Static publishing requires the initialized working tree, not just the gitlink.

Root `music15b/` and `piano-group/` were removed after migration at the owner’s request. Their old URLs are retired; use the collection URLs. `lectures/` remains necessary for the registered submodule and retains its other legacy redirects. The original path map remains available for historical lookup.

## Add a presentation

1. Choose a collection by purpose; use subject tags for overlapping topics. Internal discussion belongs in Group meetings, a topic explanation in Research talks, a project kickoff/report in Projects, and a course/tutorial in Teaching.
2. Create `collections/<collection>/YYYY-MM-DD-topic/` when a date is known. Use an undated descriptive directory when it is not; never invent a date. Keep course lessons together.
3. Copy a suitable launcher and local styling, then preserve Markdown separators: `===` horizontal, `==` vertical, `Note:` for speaker notes. Adjust relative framework links for the directory depth. Keep image, iframe, video and PDF links relative and case-correct.
4. Add a catalog entry and preview its **Open slides** link. Do not add embedded charts, framework examples/tests, skill assets or unpublished Markdown drafts to the catalog.
5. Run the library checks and inspect the affected slides. If moving an existing deck later, retain its old HTML endpoint as a redirect carrying both `location.search` and `location.hash`.

## Maintain the catalog

Edit `portal/catalog.json`. Each presentation has:

- `id`: stable unique identifier.
- `title`, `collection`, `tags`, `path`: display title, one of the six collection keys, subject tags, and a root-relative presentation path without a leading slash.
- `date`: `YYYY-MM-DD` or `null`; `dateSource` records content/filename/folder evidence.
- Optional `status: "draft"`: explicitly requested catalog listings for unfinished decks; add a `reviewNote` explaining their state.
- Optional `series` and `lessonOrder`: group a course and sort its lessons numerically.
- `legacyPaths`: previous presentation URLs.
- `classificationReason` and optional `reviewNote`: evidence for the chosen purpose and any ambiguity/date discrepancy.

Research and other standalone decks sort newest first; courses are grouped and sorted by lesson order. Unknown dates appear after dated standalone decks. The portal supports shareable query parameters `q`, `collection`, `year`, and `topic`.

## Validation and migration notes

```sh
npm run check:library
# With npm start running and Chrome available:
npm run check:library:browser -- http://localhost:8000
```

Browser checks use the existing Puppeteer package with a current Chrome installation. Set `CHROME_PATH` if Chrome is elsewhere. They check catalog decks, combined filtering, course order, mobile overflow, legacy query/hash redirects, and the latest gathering's overview, chart pointer alignment and video autoplay/loop. Remote resources are blocked for deterministic local validation, so their availability is not certified.

See [migration decisions and limitations](portal/MIGRATION.md), the [complete path map](portal/migration-map.json), and [static validation results](portal/validation-static.json). The preserved missing recap imports and the draft scientific-communication session are documented there. No dependency versions were changed.

---

<details>
<summary>Original upstream reveal.js README</summary>

<p align="center">
  <a href="https://revealjs.com">
  <img src="https://hakim-static.s3.amazonaws.com/reveal-js/logo/v1/reveal-black-text-sticker.png" alt="reveal.js" width="500">
  </a>
  <br><br>
  <a href="https://github.com/hakimel/reveal.js/actions"><img src="https://github.com/hakimel/reveal.js/workflows/tests/badge.svg"></a>
  <a href="https://slides.com/"><img src="https://s3.amazonaws.com/static.slid.es/images/slides-github-banner-320x40.png?1" alt="Slides" width="160" height="20"></a>
</p>

reveal.js is an open source HTML presentation framework. It enables anyone with a web browser to create beautiful presentations for free. Check out the live demo at [revealjs.com](https://revealjs.com/).

The framework comes with a powerful feature set including [nested slides](https://revealjs.com/vertical-slides/), [Markdown support](https://revealjs.com/markdown/), [Auto-Animate](https://revealjs.com/auto-animate/), [PDF export](https://revealjs.com/pdf-export/), [speaker notes](https://revealjs.com/speaker-view/), [LaTeX typesetting](https://revealjs.com/math/), [syntax highlighted code](https://revealjs.com/code/) and an [extensive API](https://revealjs.com/api/).

---

### Sponsors
Hakim's open source work is supported by <a href="https://github.com/sponsors/hakimel">GitHub sponsors</a>. Special thanks to:
<div align="center">
<a href="https://www.doppler.com/?utm_campaign=github_repo&utm_medium=referral&utm_content=revealjs&utm_source=github">
  <div>
    <img src="https://user-images.githubusercontent.com/629429/146530588-2980c34d-862f-4393-8ac3-65fbef6443ca.png" width="290" alt="Doppler">
  </div>
  <b>All your environment variables, in one place</b>
  <div>
    <sub>Stop struggling with scattered API keys, hacking together home-brewed tools,</sub>
    <br>
    <sup>and avoiding access controls. Keep your team and servers in sync with Doppler.</sup>
  </div>
</a>
</div>

---

### Getting started
- 🚀 [Install reveal.js](https://revealjs.com/installation)
- 👀 [View the demo presentation](https://revealjs.com/demo)
- 📖 [Read the documentation](https://revealjs.com/markup/)
- 🖌 [Try the visual editor for reveal.js at Slides.com](https://slides.com/)
- 🎬 [Watch the reveal.js video course (paid)](https://revealjs.com/course)

---

### Online Editor
Want to create your presentation using a visual editor? Try the official reveal.js presentation platform for free at [Slides.com](https://slides.com). It's made by the same people behind reveal.js.

<br>
<br>

--- 
<div align="center">
  MIT licensed | Copyright © 2011-2021 Hakim El Hattab, https://hakim.se
</div>

</details>
