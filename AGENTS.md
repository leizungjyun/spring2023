# Repository Guidelines

## Project Structure & Module Organization

This repository combines reveal.js with a personal presentation library. Framework JavaScript lives in `js/`, styles in `css/`, generated bundles in `dist/`, and extensions in `plugin/`. Browser tests live in `test/`.

Presentations live in `collections/`, grouped by purpose: research talks, group meetings, projects, external presentations, teaching, and music. Each standalone deck normally contains `index.html`, `slides.md`, and optional `presentation.css`, `presentation.js`, `docs/`, and media. `portal/catalog.json` drives the root library page; `templates/` contains reusable starters. Preserve the `lectures/neuralmorphic_kickoff/` Git submodule and its local changes.

## Build, Test, and Development Commands

- `npm install`: install dependencies when needed.
- `npm start`: serve the library at `http://localhost:8000` with live reload. Use HTTP because Markdown loads through fetch.
- `npm run build`: build framework and plugin bundles.
- `npm test`: run ESLint and QUnit through Puppeteer.
- `npm run check:library`: validate catalog targets, local references, and migration records.
- `npm run check:library:browser -- http://localhost:8000`: check the served library with Chrome; set `CHROME_PATH` for a nonstandard installation.
- `npx gulp plugins`: rebuild plugin bundles after editing plugin source.

## Coding Style & Naming Conventions

Follow the surrounding file's style. Framework contributions use tabs and single-quoted JavaScript strings; ESLint configuration is in `package.json`. Avoid unrelated formatting changes and manual edits to generated bundles.

Name dated decks `collections/<category>/YYYY-MM-DD-topic/`; use an undated descriptive name when the event date is unknown. Preserve `===` horizontal separators, `==` vertical separators, and `Note:` speaker notes. Keep presentation changes local, retain annotation plugin registration, and add catalog entries for new decks. Follow the requested scope: a template-only request should contain no invented talk content.

## Testing Guidelines

Add focused QUnit regression cases in `test/test-<feature>.html` for framework behavior changes. No numeric coverage threshold is configured. For deck edits, inspect affected slides in a browser, including asset loading, readability, navigation, and relevant media or annotations. Report existing validation failures separately from new regressions.

## Commit & Pull Request Guidelines

History uses short descriptive subjects, without a consistent Conventional Commits scheme. Prefer an imperative summary naming the affected deck or component. Use a topic branch and keep changes focused. Describe the change, link relevant issues, report checks and limitations, and include screenshots for visible layout changes. Exclude unrelated working-tree edits.
