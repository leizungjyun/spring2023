<!-- .slide: class="cover" -->
<div class="eyebrow">NEURO GROUP · 23 SEPTEMBER 2026</div>

# Neuro Group<br>Opening Keynote

<p class="cover-subtitle">Toward low-latency, low-power intelligence</p>
<p class="cover-speaker">LI Shaun</p>
<div class="cover-rule"></div>

Note:
The brief leaves the title TBD; retain its working title and use a descriptive subtitle for this opening section. Speaker, date, language, and white theme follow docs/brief.md. This deck implements the seven specified content slides; the trailing empty separator in the brief does not create a blank slide. The reference deck is collections/external-presentations/2026-09-15-neuro (the user called it 2016-09-15-neuro).

===

<div class="eyebrow">01 · THE COMPUTE QUESTION</div>

## AI is a strategic arena. Compute is uneven.

<div class="two-columns">
<div><h3>Three pillars of AI</h3><img class="pillars" src="media/diagrams/ai-pillars.svg" alt="Algorithms, data, and compute: model performance is converging, data access varies by domain, hardware capacity remains uneven."><p class="micro">U.S. and Chinese models have traded the lead.<br>Benchmark convergence does not prove data parity.</p></div>
<div><h3>Share of tracked AI-supercomputer performance</h3><div id="compute-gap-chart" class="chart gap-chart" role="img" aria-label="Estimated share of performance in a 2025 dataset: United States 75 percent, China 15 percent, other countries 10 percent."></div><p class="micro">2025 research snapshot · 500 systems in the dataset<br>Estimated capacity, not a census of all national compute.</p></div>
</div>
<p class="takeaway">Efficient computing is a strategic research opportunity.</p>
<p class="source">Sources: <a href="https://arxiv.org/abs/2504.16026" target="_blank" rel="noopener">Pilz et al., Trends in AI Supercomputers (2025)</a> · <a href="https://hai.stanford.edu/ai-index/2026-ai-index-report" target="_blank" rel="noopener">Stanford AI Index 2026</a></p>

Note:
The brief frames AI as the main arena of U.S.–China competition. The heading expresses the strategic framing without asserting a measurable ranking of all geopolitical arenas. The three pillars are a conceptual diagram, not quantitative scores. Stanford's 2026 report describes converging model performance; this is not evidence that algorithms or training data are identical or equally accessible. Public information does not establish aggregate data parity.
The right chart redraws the approximate geographic shares reported by Pilz, Sanders, Rahman and Heim, Trends in AI Supercomputers, arXiv:2504.16026v2 (23 April 2025): United States ~75%, China ~15%; other ~10% is the remainder. These are shares of the study's tracked performance, not shares of all chips or all national compute in September 2026. The dataset covers 500 systems over 2019–2025; the paper discusses incomplete coverage and uncertainties in Chinese-system data. The comparison is roughly five to one within that dataset. Do not substitute TOP500 system counts or private investment for AI compute capacity.

==

<!-- .slide: class="compute-slide" -->
<div class="eyebrow">02 · SCALING</div>

## Model demand outruns a simple Moore’s-law story

<div class="two-columns compute-columns">
<div><div class="moore-profile"><img src="media/profiles/gordon-moore.jpg" alt="Gordon Moore"><div><h3>Gordon Moore</h3><p>Fairchild R&amp;D · 1965<br>Later, Intel co-founder</p></div></div><div class="law-number">2× <span>per year</span></div><p class="law-text">Components per integrated circuit<br>at minimum cost per component.</p><p class="micro">The original 1965 observation and forecast.<br>The two-year revision came in 1975.</p><p class="micro separation">Component density ≠ training compute<br>≠ useful performance per watt.</p></div>
<div><h3>Training compute across model generations</h3><div id="training-chart" class="chart training-chart" aria-label="Interactive log-scale chart of historical model training compute. Hover or choose a model to inspect its estimate and paper."></div><div class="chart-inspector"><label for="model-select">Inspect model</label><select id="model-select" aria-label="Select a model"></select><div id="model-detail" aria-live="polite"></div></div></div>
</div>
<p class="source">Sources: <a href="https://download.intel.com/newsroom/2023/manufacturing/moores-law-electronics.pdf" target="_blank" rel="noopener">Moore, Electronics (1965)</a> · <a href="https://epoch.ai/data/ai-models" target="_blank" rel="noopener">Epoch AI model estimates</a> · <a href="media/imgs/computing-demands.pdf" target="_blank" rel="noopener">supplied visual reference</a></p>

Note:
Moore's original 1965 paper, Cramming More Components onto Integrated Circuits, concerns the complexity of an integrated circuit at minimum component cost, with a roughly annual doubling and a forecast to 1975. It is not a promise that clock speed or performance doubles annually. The two-year revision is later. The left text is a paraphrase rather than a quotation.
The supplied computing-demands.pdf establishes the chart's historical scope and visual idea. The interactive reconstruction uses independently tabulated Epoch AI training-compute estimates, not pixels digitized from the supplied figure. Dates, estimates, model references, and estimation notes are stored locally in media/data/training-compute.json. Estimates may differ from the reference figure. Training compute is total floating-point operations; 1 PFLOP-day = 8.64e19 FLOP. This is a workload, not a hardware throughput unit. The plot omits the reference's unsourced two-month doubling line and avoids treating a hardware-density curve as measured compute supply. Open a point's model paper or the dataset to inspect its provenance. The chart is a selected historical sample, not a fitted scaling law or complete model inventory.

==

<div class="eyebrow">03 · THE APPLICATION METRIC</div>

## Throughput is only half the story

<div class="two-columns">
<div><h3>High-performance computing</h3><img class="scene-photo" src="media/photos/el-capitan.jpg" alt="The El Capitan supercomputer at Lawrence Livermore National Laboratory"><div class="metric-line"><strong>1.742 EFLOP/s</strong><span>HPL · June 2025</span></div><p class="short">How much work can we finish?</p><p class="micro">TOP500 emphasizes sustained numerical throughput.</p></div>
<div><h3>Intelligence in a feedback loop</h3><img class="scene-photo edge-photo" src="media/photos/neuro-car.jpg" alt="Still from the team's existing neuro-car demonstration"><img class="edge-loop" src="media/diagrams/edge-loop.svg" alt="Sense, infer, act: a local feedback loop"><p class="short">How soon can we respond?</p><p class="micro">End-to-end latency · jitter · missed deadlines</p></div>
</div>
<p class="takeaway">A fast batch does not guarantee a timely action.</p>
<p class="source">Photo and historical HPL result: <a href="https://www.llnl.gov/article/53006/el-capitan-reigns-supreme-" target="_blank" rel="noopener">LLNL (2025)</a> · Edge demonstration: existing neuro deck</p>

Note:
El Capitan is used as an example of a TOP500-class machine, with its documented June 2025 HPL performance. This is not a claim about the current number-one system in September 2026. HPL is a dense numerical benchmark; it is not an AI inference or sensor-to-actuator latency measurement. Supercomputers also have latency-sensitive workloads; the slide compares optimization objectives rather than making the categories exclusive.
For edge control, the relevant path includes sensing, preprocessing, inference, communication and actuation. Batching may improve throughput while adding waiting time. Measure the full loop and latency distribution, not just a best-case accelerator kernel. The right photo is reused from the team's neuro-car-browser.jpg; it demonstrates the application setting, not a measured real-time guarantee.

==

<div class="eyebrow">04 · THE ENERGY CONSTRAINT</div>

## Intelligence must fit a power budget

<div class="two-columns">
<div><h3>Data-centre electricity demand is rising</h3><div id="electricity-chart" class="chart energy-chart" role="img" aria-label="Global data centre electricity consumption: 485 terawatt-hours in 2025, projected to reach 950 terawatt-hours in 2030."></div><p class="micro">All data centres, not AI alone · IEA 2026 outlook<br>2030 is a projection; electricity and grid constraints matter.</p></div>
<div><h3>At the edge, the budget is local</h3><img class="power-budget" src="media/diagrams/power-budget.svg" alt="A battery represents a finite energy and thermal budget"><div class="energy-equation">Energy per decision<br><span>= power × active time</span></div><p class="short">Battery life. Heat. Always-on sensing.</p><p class="micro">Include sensors, conversion, memory and communication.</p></div>
</div>
<p class="takeaway">Lower energy per useful decision matters at every scale.</p>
<p class="source">Source: <a href="https://www.iea.org/reports/key-questions-on-energy-and-ai/executive-summary" target="_blank" rel="noopener">IEA, Key Questions on Energy and AI (2026)</a></p>

Note:
The IEA's 2026 update reports global data-centre electricity use of 485 TWh in 2025 and a central projection of 950 TWh in 2030, about 1.96 times the 2025 level. These cover all data centres, not AI workloads alone. The source discusses constraints in electricity supply, grid connections and chip manufacturing; growth in demand alone does not prove a global generation shortfall. The outlined projection bar distinguishes a forecast from a historical estimate. Source accessed 21 September 2026.
The energy equation assumes constant average active power over the decision interval. For continuously operating systems, idle and support power must also be included. No product-specific battery runtime or energy saving is claimed.

==

<div class="eyebrow">05 · WHERE THE COST COMES FROM</div>

## Moving data costs energy and time

<div class="two-columns">
<div><h3>Separate memory and processing</h3><img class="architecture" src="media/diagrams/memory-traffic.svg" alt="Weights, activations and instructions move between memory and processor"><p class="micro">Bandwidth and data movement can limit useful compute.</p></div>
<div><h3>A modern example: GeForce RTX 5090</h3><img class="architecture gpu" src="media/figures/gb202-memory.svg" alt="Conceptual layout of a GB202 GPU and external GDDR7 memory, incorporating the existing die photograph"><p class="micro">On-chip L2 cache · 32 GB external GDDR7<br>Memory placement is schematic, not a PCB layout.</p></div>
</div>
<p class="takeaway">Can stored state participate directly in computation?</p>
<p class="source">Specification: <a href="https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5090/" target="_blank" rel="noopener">NVIDIA</a> · GB202 figure adapted from the existing neuro deck; photograph credits in notes</p>

Note:
The brief's “GTX 5090” is corrected to the product name GeForce RTX 5090. NVIDIA lists 32 GB GDDR7. The left diagram is conceptual: modern processors have caches, local memories, parallelism, and architectural features that mitigate the von Neumann bottleneck. Data movement is a contributor, not a proof that every workload is memory-bound or that all latency and power arise from this bottleneck. No measured GPU-to-prototype power or speed comparison is implied.
The right SVG reuses the reference deck's GB202 die photograph, with English metadata and a white-theme palette. Original photograph credits: Chip by ASUS Tony 俞元麟; Dieshot by 万扯淡; Layout by Kurnal. The photograph and original watermark remain unchanged. The reference deck sourced it from https://www.tomshardware.com/pc-components/gpus/gb202-die-shot-beautifully-showcases-blackwell-in-all-its-glory-gb202-is-24-percent-larger-than-ad102 and the photographer's original post https://x.com/Kurnalsalts/status/1883153126011892140 . Third-party die labels are illustrative, not our measurement. This slide makes no claim about memory area fractions, cache capacity, or task-specific energy consumption.

==

<!-- .slide: class="brain-slide" -->
<div class="eyebrow">06 · THE NEUROMORPHIC OPPORTUNITY</div>

## Learn from the brain’s organization

<div class="brain-layout"><div><img class="brain-power" src="media/diagrams/brain-power.svg" alt="Conceptual brain diagram with approximately 20 watts of whole-brain metabolic power"><p class="micro">An architectural inspiration,<br>not an equal-workload benchmark.</p></div><div><img class="memory-array" src="media/diagrams/in-memory.svg" alt="A conceptual array performs weighted parallel computation where its weights are stored"><p class="short">Local memory. Parallel dynamics.<br>Less movement, shorter paths.</p></div></div>
<div class="quote-row"><img src="media/profiles/xiangwei-zhu.png" alt="Xiangwei Zhu"><div><blockquote>“Neuromorphic computing is the direction<br>I care most about right now.”</blockquote><p>Xiangwei Zhu <span>· translated from the supplied brief</span></p></div></div>
<p class="source">Brain-power context: <a href="https://www.nature.com/articles/s41467-024-47811-6" target="_blank" rel="noopener">Nature Communications (2024)</a> · AIMC: <a href="https://research.ibm.com/publications/a-64-core-mixed-signal-in-memory-compute-chip-based-on-phase-change-memory-for-deep-neural-network-inference" target="_blank" rel="noopener">Le Gallo et al. (2023)</a></p>

Note:
The approximate 20 W figure refers to total human-brain metabolic power and varies with assumptions. It is not directly comparable to a GPU's board power at an unrelated workload. The brain is not a literal electronic crossbar. The diagram transfers principles—local stored state influencing computation and parallel signal integration—to an engineering design, without implying that biological and artificial mechanisms are identical.
Neuromorphic computing includes digital, analog and mixed-signal approaches. Analog in-memory computing is one relevant direction, not a synonym for the entire field. Reduced movement and parallel physical computation can lower latency and energy, but converters, interconnect, control, calibration, and peripheral circuits remain. Published silicon supports the potential on specified workloads; this diagram is not a claim of measured performance for our prototype.
Xiangwei Zhu's portrait is copied from the reference deck. The quotation is an English translation of the user-supplied wording: 神经形态计算是我目前最关心的方向. It is attributed to the brief, not to a separately verified public interview.

==

<!-- .slide: class="analog-slide" -->
<div class="eyebrow">07 · CHOOSING THE RIGHT DOMAIN</div>

## Analog imperfections can be a design constraint

<div class="two-columns analog-columns"><div><h3>Task accuracy can tolerate weight error</h3><a href="media/figures/accuracy-against-errors.pdf" target="_blank" rel="noopener"><img class="accuracy-plot" src="media/figures/accuracy-against-errors.png" alt="Supplied plot of classification accuracy against weight error for eight model sizes; the two smallest models lose more accuracy over the displayed range"></a><p class="micro">Axes: accuracy (%) vs weight error (%)<br>Legend: parameter count · supplied example, conditions pending</p></div><div><h3>Match the hardware to the task</h3><div class="tradeoff"><span>Limited generality</span><strong>Specialize a stable inference workload.</strong></div><div class="tradeoff"><span>Finite precision</span><strong>Optimize task accuracy, not exact arithmetic.</strong></div><div class="tradeoff"><span>Noise and device variation</span><strong>Train with hardware errors; calibrate and validate.</strong></div><p class="micro">Tolerance has limits: drift, out-of-distribution inputs,<br>and closed-loop stability still need testing.</p></div></div>
<p class="takeaway">Our opportunity: useful accuracy within tight time and energy budgets.</p>
<p class="source">Figure: supplied neuro-deck material · Supporting approach: <a href="https://www.nature.com/articles/s41467-023-40770-4" target="_blank" rel="noopener">Rasch et al., hardware-aware training (2023)</a></p>

Note:
The curve image and linked PDF are reused without changing their numerical content. The English caption translates the original Chinese axis and legend labels. The plot compares eight parameter counts from 26,506 to 1,863,690; the smallest two models degrade more strongly in this displayed example. It does not establish that more parameters always improve robustness, nor does it establish stability in closed-loop control.
As recorded in the reference deck, dataset, architectures, error distribution/injection procedure, number of repeats, and whether the results are simulated or hardware-measured are not supplied. Therefore this is illustrative supplied evidence, not a validated quantitative result to generalize. No error bars or significance claims are added. The source PDF is available by clicking the image.
Rasch et al., Hardware-aware training for large-scale and diverse deep learning inference workloads using in-memory computing-based accelerators, Nature Communications 14, 5282 (2023), studies robustness to modeled hardware nonidealities across network topologies. Hardware-aware training is a mitigation, not a universal guarantee. In our intended inference and control domains, exact arithmetic may be unnecessary, but accuracy, stability, drift, temperature, energy and end-to-end latency must be evaluated on the actual workload. End here as the brief's opening argument, without inventing a further research program or a generic thank-you slide.
