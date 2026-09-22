# Neuro Group — Opening Keynote

Eight-slide English reveal.js keynote for **LI Shaun · 23 September 2026**, using the white theme. The cover and seven content slides implement [docs/brief.md](docs/brief.md). The title is still a working title.

## Preview and navigation

Run `npm start` from the repository root, then open:

<http://localhost:8000/collections/research-talks/neuro-group-opening-keynote/>

Use Right from the cover, then Down for the vertical sequence; Space advances through the whole deck. Escape opens overview, and S opens speaker notes. The annotation plugin remains enabled.

On the computing-demand slide, hover a point to inspect its estimate and source URL; click the point or **Open model paper** to open its reference. The model selector provides keyboard access. Charts, data, portraits and figures load locally; opening external source links requires a network.

## File organization

```text
neuro-group-opening-keynote/
├── index.html                 # launcher and shared framework references
├── slides.md                  # slides, sources, and speaker notes
├── presentation.css           # deck layout and typography
├── presentation.js            # local charts, interactions, Reveal setup
├── media/
│   ├── data/                  # selected model estimates and references
│   ├── diagrams/              # editable explanatory SVGs
│   ├── figures/               # reused GPU and analog-error figures
│   ├── imgs/                  # user-supplied computing-demands.pdf
│   ├── photos/                # supercomputer and edge-demo photographs
│   └── profiles/              # Gordon Moore and Xiangwei Zhu
├── vendor/                    # local Plotly bundle
├── docs/
│   ├── brief.md               # user brief; preserved as supplied
│   └── evidence/              # source register and selected raw data
├── scripts/
│   ├── build-diagrams.py      # regenerate explanatory SVGs
│   └── qa/check.cjs           # browser checks
└── qa/
    ├── screenshots/           # reviewed slide captures
    └── reports/               # browser/static verification
```

Keep `===` for horizontal slides, `==` for vertical detail, and `Note:` for speaker notes. Update plotted model estimates in `media/data/training-compute.json`, preserving source notes and units. The national-compute and electricity chart values are in `presentation.js`.

[Source register and qualifications](docs/evidence/sources.md) records dataset dates, image credits, and unresolved experimental context. Original PDF figures remain available. The unused math plugin was removed from this deck's launcher so the presentation does not request a remote math CDN.

## Verification

With a preview server running:

```sh
CHROME_PATH='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' \
  node collections/research-talks/neuro-group-opening-keynote/scripts/qa/check.cjs http://127.0.0.1:8000
```

`CHROME_PATH`, `BASE_URL`, and `QA_OUTPUT` are configurable. The check covers slide count, local asset loading, runtime errors, vertical bounds, real hover targeting at two viewport sizes, source selection, overview, and plugin registration. Visually inspect screenshots as well.
