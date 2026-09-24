# Neuro Group — Opening Keynote

Nineteen-slide reveal.js keynote for **LI Shaun · 23 September 2026**, using the white theme. The policy slide preserves its source deck's Chinese text; the remaining slides are English. The title is still a working title.

The argument runs in two halves. The first ten slides are horizontal: strategic framing, then compute supply and demand (leading AI-supercomputer growth, then the historical model-training-compute trajectory, each against the same Moore benchmark), then latency, energy, the von Neumann bottleneck, the brain's organization, the analog trade-off, and the policy slide. The second half is one horizontal slide with seven vertical children: computing inside the SRAM and DRAM arrays, the memristor crossbar and the two circuit laws it computes with, the two papers behind the element, the FPGA comparison, training against inference, starting from the computation rather than the memory, nonlinearity taken from the device, and three application settings — then a full-bleed closing image. [docs/brief.md](docs/brief.md) is the outline, with the prompt behind every figure.

## Preview and navigation

Run `npm start` from the repository root, then open:

<http://localhost:8000/collections/research-talks/neuro-group-opening-keynote/>

Use Right from the cover through the first ten slides, Right again to reach the second section, then Down through its seven vertical slides and Right once more for the closing image; Space advances through the whole deck in that order. Escape opens overview, and S opens speaker notes. The annotation plugin remains enabled.

The closing slide is the one exception to the deck's layout: it is a single full-bleed image, so it carries no heading and hides the controls, progress bar and slide number while it is on screen. Its `data-state` lands on the viewport element, not on `.reveal`, which is why the rules in `presentation.css` are written as `.image-ending .reveal:not(.overview) …`.

Charts, tables and figures link from the visual wherever practical, and most carry a visible source line. The pricing table and both figures on the brain slide had their visible sources removed at the speaker's request: they still link out, and their provenance is in the speaker notes and [the source register](docs/evidence/sources.md). Photographs keep their credits off the slide surface; click a photo to open its source. Full provenance and qualifications remain in the speaker notes and [the source register](docs/evidence/sources.md). Slides 17 and 18 are imports from the reference deck and carry its qualifications with them: read the register's notes on the KANalogue framework and on the application categories before quoting anything from them.

On the computing-demand slide, every model is labelled, and hovering a point shows its name and estimate; the tooltip carries neither the source URL nor the estimation-status text, both of which were too long to read there. Click the point or **Open model paper** to open its reference; the estimation status stays in `media/data/training-compute.json` and in the speaker notes. The dashed era lines are annotations transcribed from the supplied figure — read the note in [the source register](docs/evidence/sources.md) before quoting them. The model selector provides keyboard access. Charts, data, portraits and figures load locally; opening linked sources requires a network.

## File organization

```text
neuro-group-opening-keynote/
├── index.html                 # launcher and shared framework references
├── slides.md                  # slides, sources, and speaker notes
├── presentation.css           # deck layout and typography
├── presentation.js            # local charts, interactions, Reveal setup
├── media/
│   ├── data/                  # selected model estimates and references
│   ├── diagrams/              # editable explanatory SVGs: generated figures plus the translated reference figures
│   ├── figures/               # reused GPU, supercomputer and circuit-element figures; the framework PDF; retained analog-error figure
│   ├── imgs/                  # user-supplied computing-demands.pdf
│   ├── photos/                # supplied supercomputer photo, two application photographs, closing image
│   ├── profiles/              # Gordon Moore, John von Neumann, Xiangwei Zhu and Leo Esaki
│   └── public-private-supercomputers.pdf   # supplied figure, linked from the slide
├── vendor/                    # local Plotly bundle
├── docs/
│   ├── brief.md               # deck outline: key point and figure prompt per slide
│   └── evidence/              # source register and selected raw data
├── scripts/
│   ├── build-diagrams.py      # regenerate this deck's SVGs: pillars, flags, edge, von Neumann, synaptic, in-memory comparison, accuracy chart, speech cloud, SRAM/DRAM arrays, crossbar, FPGA and FPMA fabrics, training/inference, memory-first framing, device function basis
│   ├── translate-reference-figures.py   # re-palette and translate the six reference-deck figures
│   └── qa/check.cjs           # browser checks
└── qa/
    ├── screenshots/           # reviewed slide captures
    └── reports/               # browser/static verification
```

Keep `===` for horizontal slides, `==` for vertical detail, and `Note:` for speaker notes. Update plotted model estimates in `media/data/training-compute.json`, preserving source notes and units. The national-compute bar widths and the V4.1 Flash pricing are inline in `slides.md`; the training chart is the only chart built by `presentation.js`. `media/public-private-supercomputers.pdf` is retained as supplied — if you need editable data from it, take the values from the Epoch AI study cited in [the source register](docs/evidence/sources.md) rather than tracing the figure.

Figures in `media/diagrams/` are generated, not hand-edited: `python3 scripts/build-diagrams.py` rewrites this deck's own schematics, and `python3 scripts/translate-reference-figures.py` rereads the reference deck and rewrites the six translated ones, failing loudly if a label it expects is no longer there. The diagrams carry no background, so they sit on the slide's white ground; give a figure a fixed height in `presentation.css` rather than a fixed width. Slides 11–18 are dense, and the takeaway line on each is absolutely positioned — if you add text to one of those slides, check the flow content still clears it. The browser check measures this for you.

[Source register and qualifications](docs/evidence/sources.md) records dataset dates, image credits, and unresolved experimental context. Original PDF figures remain available. The unused math plugin was removed from this deck's launcher so the presentation does not request a remote math CDN.

## Verification

With a preview server running:

```sh
CHROME_PATH='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' \
  node collections/research-talks/neuro-group-opening-keynote/scripts/qa/check.cjs http://127.0.0.1:8000
```

`CHROME_PATH`, `BASE_URL`, and `QA_OUTPUT` are configurable. The check expects nineteen slides; it covers slide count, local asset loading, runtime errors, vertical bounds, real hover targeting at two viewport sizes, source selection, overview, and plugin registration. The flow-fence check is skipped on the closing slide, which is a full-bleed image, and the report line for it falls back to its class name. Visually inspect screenshots as well.

Math in the slide 17–18 diagrams is rendered as SVG paths with `scripts/math_typeset.py`. Rebuilding these diagrams requires `latex` and `dvisvgm` on PATH; viewing the deck needs neither. The editable TeX expressions remain in the diagram scripts.
