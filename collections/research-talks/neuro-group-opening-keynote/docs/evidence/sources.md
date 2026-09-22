# Sources and interpretation

Checked 21 September 2026. The user brief remains unchanged in `../brief.md`. Slide notes contain the argument, qualifications, and full attribution; this file records the data and asset provenance needed for maintenance.

## Quantitative charts

| Chart | Data | Scope |
| --- | --- | --- |
| U.S.–China compute gap | [Pilz et al., Trends in AI Supercomputers, arXiv:2504.16026v2](https://arxiv.org/abs/2504.16026v2): approximately 75% U.S., 15% China; 10% other is the remainder | Share of tracked performance in the study's 500-system dataset, published April 2025. Not a 2026 national census. |
| Historical model training compute | [Epoch AI, Data on AI Models](https://epoch.ai/data/ai-models), [CSV](https://epoch.ai/data/all_ai_models.csv), retrieved 2026-09-21 | 15-model historical selection corresponding to the supplied reference; missing-compute rows omitted. Raw selected rows: `epoch-selected-models.csv`; runtime data: `../../media/data/training-compute.json`. Epoch estimates, not direct measurements for every model. CC BY, attribution to Epoch AI. |
| Electricity demand | [IEA, Key Questions on Energy and AI, executive summary (2026)](https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary): 485 TWh in 2025; 950 TWh in 2030 | All data centres. 2025 historical estimate; 2030 central projection. CC BY 4.0. |

The historical compute chart uses the supplied `media/imgs/computing-demands.pdf` as a design reference. It uses independently tabulated data instead of reproducing approximate pixel coordinates or unsupported trend fits. Dates and model versions follow Epoch; each point links to its model paper or source. PFLOP-days = total FLOP / 8.64e19. Original source notes and estimation methods remain in the JSON and selected CSV; some estimates are inferred rather than disclosed in the model paper. NETtalk's obsolete Citeseer link is replaced by the paper DOI.

The source's two-month doubling annotation is omitted because its underlying fit and sample were not supplied. The chart is a historical selection, not a new fitted scaling law or a direct measurement of hardware supply.

## Other claims

- [Stanford AI Index 2026](https://hai.stanford.edu/ai-index/2026-ai-index-report): converging U.S.–China model performance supports the algorithms discussion, but does not establish training-data parity.
- [Moore's 1965 paper](https://download.intel.com/newsroom/2023/manufacturing/moores-law-electronics.pdf): approximately annual doubling of components at minimum component cost. The two-year revision is later; neither statement is an annual performance-per-watt guarantee.
- [LLNL, June 2025 HPL result](https://www.llnl.gov/article/53006/el-capitan-reigns-supreme-): 1.742 EFLOP/s, used as a historical throughput example, not today's rank.
- [NVIDIA RTX 5090 specifications](https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5090/): correct product name and 32 GB GDDR7. The brief's “GTX” naming is corrected.
- [Spike-based dynamic computing, Nature Communications (2024)](https://www.nature.com/articles/s41467-024-47811-6): context for the approximate 20 W brain-power figure. Not a matched-workload comparison with a GPU.
- [Le Gallo et al., 64-core mixed-signal AIMC (2023)](https://research.ibm.com/publications/a-64-core-mixed-signal-in-memory-compute-chip-based-on-phase-change-memory-for-deep-neural-network-inference): published evidence for in-memory inference potential on specified tasks.
- [Rasch et al., hardware-aware training (2023)](https://www.nature.com/articles/s41467-023-40770-4): mitigation of hardware nonidealities, not blanket immunity to analog errors.

## Asset provenance

| Local asset | Origin / treatment |
| --- | --- |
| `media/profiles/gordon-moore.jpg` | [Computer History Museum profile](https://computerhistory.org/profile/gordon-moore/); [image](https://computerhistory.org/wp-content/uploads/2020/01/1998_gordon_moore-e1580707779947.jpg). Original downloaded; CSS presents it in grayscale. |
| `media/photos/el-capitan.jpg` | LLNL article above; [LLNL image](https://contenthub.llnl.gov/sites/contenthub/files/styles/scaled_877w/public/2025-10/el-capitan-cabinet.jpg?itok=WVEGj0Mi). Credit: Lawrence Livermore National Laboratory. |
| `media/photos/neuro-car.jpg` | Reference deck `video/neuro-car-browser.jpg`; still from the existing team demonstration. No performance inferred from the photo. |
| `media/profiles/xiangwei-zhu.png` | Reference deck `images/profiles/朱祥维-transparent.png`; existing portrait and watermark preserved. Quote translated from the user brief. |
| `media/figures/gb202-memory.svg` | Reference deck `images/gb202-gddr7-slide.svg`, translated metadata and white palette. Embedded die photo unchanged. Credits: Chip by ASUS Tony 俞元麟; Dieshot by 万扯淡; Layout by Kurnal. Original post: https://x.com/Kurnalsalts/status/1883153126011892140 . Layout is schematic. |
| `media/figures/accuracy-against-errors.{png,pdf}` | Copied unchanged from reference deck. English caption translates axes and legend. Experimental conditions are unspecified. |
| `media/diagrams/*.svg` | Editable explanatory schematics generated by `scripts/build-diagrams.py`; not measured data or anatomical drawings. |
| `vendor/plotly.min.js` | Reused local Plotly bundle from the 2026-09-10 group-gathering deck; upstream copyright/license header retained. |

The reference deck is `collections/external-presentations/2026-09-15-neuro/`, interpreted from the user's “2016-09-15-neuro” reference.

## Open content decisions

- The title remains the supplied working title; a descriptive subtitle is added.
- The analog-error example lacks dataset, architecture details, error injection conditions, repeated trials, and measured-versus-simulated status. It is marked as an illustrative supplied example.
- No additional topic was inferred from the trailing blank separator in the brief.
