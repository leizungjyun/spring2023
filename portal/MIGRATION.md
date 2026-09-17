# Library migration record

The complete per-file old-to-new map is `migration-map.json`, written before moving any presentation files. `migration-audit.json` records SHA-256 hashes before and after reference-only rewrites. All source files, including unreferenced media, source PDFs/PPTX files, drawings and hidden metadata, were retained. Shared lecture images live in `assets/presentations/lectures-images/`; the shared piano illustration lives in `collections/music/_shared/`.

## Classification decisions

- Coding with Copilot: **Teaching**, because it is a programming tutorial with setup and a demonstration.
- Meta-Seminar: **Teaching / scientific communication**, because it teaches seminar preparation and delivery.
- July “paper”: **Teaching / deep learning**, because its content is explicitly a test review of applied math and machine learning.
- Semester opening / KAN2: **Group meetings**. Orientation, onboarding and semester strategy introduce a substantial KAN 2.0 segment. This mixed-purpose classification is worth reviewing.
- Ornithopter / SDEM July report: **Projects**. Design and implementation, engineering targets and the training roadmap are central, although it also surveys research. This classification is worth reviewing.
- June discussion: **Group meetings**, because it organizes internal research tasks and releases, rather than presenting a single project report.
- Neuromorphic kickoff: **Projects**, based on its kickoff, scientific questions and roadmap.
- Music 15B remains a numbered teaching course. Piano-group and concert content belongs in **Music**.

The portal uses subject tags independently of collections, so AI, robotics, brain-inspired computing and hardware do not force a deck into one purpose category.

## Date evidence

Dates shown in the catalog follow title-slide evidence where available. Historic path dates were retained when they disagree:

- KAN: filename **2024-05-15**, title slide **2024-05-17**.
- Applied math review: folder **2024-07-24**, title slide **2024-07-22**.
- AI Group Gathering: folder **2026-09-10**, title slide **2026-09-11**.
- December brain-inspired talk includes **2024-12-09** and **2024-12-16** sessions. One deck is retained with the first date.
- Concert program has no documented date and remains **undated**.

## Preserved exceptions and existing issues

- `lectures/neuralmorphic_kickoff` remains the Git submodule at its registered path. The Projects collection launcher redirects into it. Its gitlink commit, `.git` pointer, `.gitmodules`, local Git configuration and contents were not rewritten or relocated. This avoids introducing changes into the nested repository or staging its relocation in the parent.
- The January recap already imported missing `neuro.md` and `semiconductor.md`. These remain documented missing references; no unrelated material was substituted. The main recap content is preserved.
- `2024-09-sci-verbal03.md` is retained in the Verbal for Science series folder. It has no original HTML launcher and repeats an earlier session's title/date. It is excluded as an unpublished draft, not silently promoted to a dated lesson.
- Music 15B weeks 05–07 and 10–12 retain a pre-existing ABCJS editor initialization error (missing textarea); week 04 can also race Markdown loading. These errors were reproduced from the original Git HEAD files. The slides still render; notation-widget repair is outside this organizational migration.
- The Ornithopter launcher used the wrong case for its Markdown filename. The migrated launcher points to `slides.md`, resolving that case-sensitive hosting issue.
- Old root `index.html.bak` was a framework starter with a missing placeholder Markdown path; it is archived under `templates/`, outside the catalog.
- External images, fonts, math libraries, scripts and embedded videos in historical decks still require their original providers. This migration does not replace or upgrade them.

## Reversibility and validation

No commits, pushes, deployments, dependency upgrades, framework source edits or Git index writes are part of the migration. Existing HTML endpoints are lightweight redirects; they append the incoming query string and slide hash to the new URL. The submodule's old URL continues serving its actual presentation.

Run `npm run check:library` for local references and catalog checks. For the initial migration audit, run `python3 scripts/validate_library.py --audit`; it checks every output against the recorded post-rewrite hash. Future intentional edits naturally invalidate that historical byte audit, but not the normal library check. Browser validation results are in `validation-browser.json`; static results are in `validation-static.json`. These are reports, not catalog entries.

The one-time planner and migration scripts must not be rerun over an already migrated repository. To review a moved file, find its original path in the manifest and compare against Git HEAD. The migration audit's pre-rewrite hashes include uncommitted edits, not just HEAD. Original binary documents/media remain byte-identical.

Initial verification: all 30 catalog presentations initialized in Chrome; 30 legacy HTML redirects and the Projects submodule launcher preserved query strings and slide hashes. Representative decks from all five collections were visually inspected. The latest gathering passed Escape overview, Plotly hover at three window sizes, and autoplay/loop checks for all three videos. Local live reload was exercised for nested Markdown and portal CSS; the portal and a deck also opened under a hosting subdirectory. The static audit checked 631 local references and all 394 original files, with only the two pre-existing recap imports unresolved. Browser checks intentionally block external resources.

## Subsequent root cleanup

At the owner’s request, root `music15b/` and `piano-group/` were removed after confirming they contained only 12 redirect pages and empty directories. Their presentations and assets remain in `collections/`; no deck content was deleted. Those 12 legacy URLs are intentionally retired, listed in `retired-redirects.json`, and removed from active catalog metadata. The initial validation figures above are historical. Current redirect checks exclude retired endpoints. `lectures/` is still required by the neuromorphic submodule launcher and has not been removed. The two pre-existing missing recap imports also still point into that root.
