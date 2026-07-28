# Track 2 — Global OEM / Manufacturer Site Patterns

**Purpose:** establish the quality bar for the Maven corporate site by dissecting the actual live
websites of the leading wide-format / industrial digital printing manufacturers.
**Date of research:** 2026-07-28. All URLs verified live on that date unless marked otherwise.

---

## 0. Method, coverage and gaps

| Vendor | What was inspected | Result |
|---|---|---|
| swissQprint | homepage, printer index, Nyala 5 PDP, spec page, applications hub, showcases, compare tool, book-a-demo form | full |
| Durst | homepage, P5 350/HS PDP, applications page, **Virtual Showroom (3D)** — incl. JS/network internals via headless Chrome | full + deep |
| Canon | Arizona 2300 FLXflow PDP + dedicated `/specifications/` page, JSON-LD | full |
| Roland DG | printer index (EU), TrueVIS XG-640 PDP, VersaOBJECT MO PDP, DGA 3D showroom / AR | full |
| Mimaki | global nav + region switcher, mimakiusa catalog, UJ330H-160 PDP, Mimaki Europe Digital Showroom | full |
| HP | Latex R series hub incl. interactive hotspot explorer, model cards, datasheets | full |
| Epson | SureColor SC-S80600 PDP spec-group structure | partial (product discontinued) |
| Kornit | Atlas MAX PLUS PDP | full |
| Mutoh | product catalog segmentation | partial |
| Agfa | — | **BLOCKED** (bot CAPTCHA on `agfa.com/printing/...`) |
| EFI / VUTEk | — | **404** — EFI's inkjet business was carved out; legacy `efi.com/products/...` URLs are dead |
| Brother GTX | — | **DNS failure** on `base.brother.com` |

Where a claim below is non-obvious, the source URL is inline. Where something could not be verified,
it says so — nothing here is inferred from memory.

---

## 1. The one-paragraph summary of the bar

None of these sites are "pretty". They are **catalog machines**. What makes them read as premium is
not decoration — it is (a) a ruthlessly consistent product-object model (every machine has the same
spec fields, so a comparison table is possible), (b) three orthogonal entry paths into the same
catalog (by machine, by application, by ink/consumable), (c) a single dominant CTA repeated at
predictable intervals ("Book a demo" / "Contact us"), and (d) **ungated PDFs**. The visual craft is
mostly restraint: big product photography on white/near-white, one accent colour, generous type
scale, and numbers presented as hero metrics. The only genuinely "expensive-feeling" interactive
thing in the whole category is Durst's WebGL showroom (§6) — and it is a separate subdomain, not the
product page.

---

## 2. Global navigation structure

### 2.1 The three real segmentation axes

Across all vendors, products are segmented by exactly one of three axes at the top level, with the
other two available as *finders*:

1. **By technology / form factor** — swissQprint (`Flatbed printers` vs `Roll to roll printers`),
   Mutoh (`Waterbased UV`, `UV & MP`, `Sign & Display`, `Waterbased Textile`),
   Mimaki USA (`UV-DTF`, `UV-LED Hybrid Roll and Flatbed`, `UV-LED & Eco-Solvent Roll to Roll`,
   `UV-LED Flatbeds`, `Textile & Dye Sub`, `Large Format Cutters & Laminators`, `3D`,
   `Software, Inks, Media`).
2. **By market segment** — Durst (`Large Format`, `Soft Signage & Fabrics`, `Textile`, `Labels`,
   `Ceramics`, `Corrugated`).
3. **By brand family** — Roland DG runs *both* simultaneously: "By Type" (Printers, Cutters,
   Engravers/Decorators, Milling/3D, Dental, Software, Inks) **and** "By Brand" (TrueVis,
   VersaStudio, VersaObject).

### 2.2 Verbatim top-level menus

- **swissQprint** (`swissqprint.com`): `Printers` · `Applications` · `Inks` · `Showcases` · `Company`
  — five items, no mega-menu. The cleanest IA in the category and the closest model for Maven.
- **Durst** (`durst-group.com`): `Printing systems` · `Applications` · `Inks` · `Software` ·
  `Support` · `Academy` · `Career` · `Corporate`.
- **Mimaki** (`mimaki.com`): `Product` · `Case Study` · `Application` · `Supply` · `Support` ·
  `Download` · `Contact Us` · `News` · `Company Profile` · `Company / IR Information`.
- **Roland DG EU**: `Products` · `Applications` · `Case Studies` · `Training` (Roland DG Academy) ·
  `Support`.
- **Mimaki USA**: `Products` · `Create` · `Support` · `Resources` · `About` · `News` · `Contact` ·
  `Promos`.

**Pattern:** `Products` → `Applications` → `Inks/Supplies` → `Support/Service` → `Company` is the
canonical spine. Four of five put **Inks / Supply as a sibling of Products, not a child.** For a
dealer that sells machines *and* inks, this is the single most important structural takeaway.

### 2.3 The "finder" pattern (Durst — best in class)

Durst's mega-nav contains three faceted finders, all client-side:

- **Printer finder** — facets: `Series` · `Segment` · `Print Width` · `Inks` → `Search results`
- **Application finder** — facets: `Large Format` · `Textile` · `Labels` · `Ceramics` · `Corrugated`
- **Ink finder** — facets: `Segment` · `Printers` · `Inks`

Source: rendered DOM of <https://www.durst-group.com/en/products/p5-350-hs/>. This is what makes a
30-SKU catalog feel navigable. It is trivially implementable as static JSON + client-side filter.

### 2.4 Localisation / URL architecture (critical for Maven)

- **swissQprint** uses `**/{market}/{language}/**` — real live examples: `/ch/en/`, `/uk/en/`,
  `/us/en/`, `/jp/en/`, `/es/fr/`. Note `/es/fr/` — Spain market, French language: **market and
  language are independent axes**. Contact pages are market-specific and *named* per market:
  `/uk/en/contact/contact-uk/` and `/uk/en/contact/book-a-demo-uk/`.
- **Durst** uses `/{lang}/` only — `en`, `de`, `it`, `es`, `fr`.
- **Mimaki** does not localise in-place; it **hard-splits into separate domains per region**
  (`japan.mimaki.com`, `mimakieurope.com`, `mimakiusa.com`, and country sites incl. a Turkey site).
  Region switcher groups: `Japan` · `Europe` · `Asia Oceania` · `North America` · `South America`.
- **Canon Europe** on the Arizona 2300 pages emits **zero `hreflang` tags** (verified in DOM) — a
  real SEO defect at a company with dozens of locale sites. Do not copy this.

**Decision input:** Durst's `/{lang}/` is the right shape for Maven (single market, many languages).
swissQprint's two-segment scheme only pays off with per-country sales entities.

---

## 3. Product detail page anatomy — three real PDPs, section by section

### 3.1 swissQprint Nyala 5 — <https://www.swissqprint.com/uk/en/flatbed-printer/nyala-5/>

The most minimal and the closest to the Maven design brief.

1. **Above the fold:** product name `Nyala 5` as H1 + tagline `First choice, worldwide` + one short
   paragraph. Large product photograph. No slider, no video, no autoplay.
2. **Hero metric strip** — five oversized numbers, no table chrome:
   `Flatbed size 3.2×2 m` · `Productivity 253 m²/h` · `Operation 24/7` ·
   `Print head rows 1–2` · `Colour channels 10`.
3. **Five icon proof-points**, each linking to its own page: `No. 1 printer` · `2.2 kWh power
   consumption` · `36 months warranty` · `Neon printing` · `Swiss made`.
4. **`Options`** — 8 expandable optional configurations (roll-to-roll, dual roll, oversize board,
   collector paper, edge holders, automation interface…).
5. **CTA block** — `Book a demo`, plus links to `Specifications` (separate page) and an **ungated**
   brochure PDF.
6. **Customer testimonials** — four quotes with photos + `More` → showcase detail pages.
7. **`Application areas`** — 8 tiles (Sign & Display, Interior Décor, Packaging, Fine Art, Wood,
   Glass, Industrial) linking to application pages.
8. **Model comparison table** — this model vs the other four flatbeds, each with `Explore`.
9. **Closing contact block** — `Contact us` + `Book a demo`.
10. Footer.

Note the ordering logic: **numbers → proof → configurability → demo → social proof → applications →
comparison → contact.** Specs are *not* on this page; they live at
`/uk/en/flatbed-printer/nyala-5/specifications-nyala-5/`.

### 3.2 Roland DG TrueVIS XG-640 — <https://www.rolanddg.eu/en/products/printers/truevis-xg-640>

The most content-heavy, and a good example of "long PDP done well".

Tab bar directly under the hero: `Overview` · `Specifications` · `Request a Consultation` ·
`Interested?` (in-page anchors, not route changes).

Section order (verbatim headings):
1. Hero + tagline `Versatility at Full Velocity`
2. Product intro + bullet feature summary
3. `One Machine. Every Job. Full Speed.`
4. `Pushing the Limits of Performance` — six icon blocks
5. `Industry-Leading Productivity`
6. `Endless Applications Infinite Possibilities` — **8-slide application carousel** with Previous/Next
7. `Everything You Need to Succeed`
8. `Expect Big Things`
9. `Introducing Our Most Vibrant and Eco-Friendly TrueVIS Inks` — **inks sold on the machine page**
10. `TrueVIS XG-640 Highlighted Features` — three image+text blocks
11. `Compare Our High Productivity Large-format Printers` — XG-640 vs XP-640
12. `Powerful Software Included` — two software cards
13. `For the Future`
14. **Specifications** — collapsible table
15. Certification badges (GREENGUARD Gold, Roland DG Care)
16. `Protect Your Investment` — warranty / service
17. `Why Choose Roland DG?`

The VersaOBJECT MO PDP repeats the same skeleton and adds `Frequently Asked Questions`,
`Optional Rotary Printing Unit`, and `Certifications`.

### 3.3 Canon Arizona 2300 FLXflow — <https://www.canon-europe.com/business/products/large-format-printers/arizona-2300-series/>

Section order (verbatim H2s, from rendered DOM):
`Lift your business` → `FLXflow in a nutshell` → `Optimised useability` →
`High quality and versatile` → `Reliability and serviceability by design` →
`Elevated and textured printing` → `Maximise uptime` → `In-field upgradability` →
**`Download Datasheet`** → **`Relevant Case Studies`** (8 case studies listed) →
**`Want to learn more about the Arizona 2300 FLXflow?`** (lead capture) →
**`Frequently Asked Questions`** (3 Q&As) → `Get in touch`.

Measured facts:
- `0` `<video>` / YouTube / Vimeo embeds; `0` `<canvas>` / `<model-viewer>`; 118 elements with
  carousel/slider classes.
- **JSON-LD present: `BreadcrumbList`, `Product`, `FAQPage`.** The FAQ block is there for the
  rich-result. Copy this.
- **`hreflang` count: 0.**
- Specs are on a **separate URL** — `/arizona-2300-series/specifications/`.

### 3.4 Mimaki UJ330H-160 — <https://www.mimakiusa.com/uj330h-160/>

Notable because it is the only one that **publishes a price**:
`List Price (USD): UJ330H-160: $39,995`, immediately under the hero. Section order:
Hero (with carousel arrows) → Price → `The Next Evolution in Mimaki Wide Format Innovation` →
seven key-benefit blocks → **nine "Core Technologies" icon tiles** (Waveform Control, Advanced Pass
System, Nozzle Check Unit …) → 8-image applications gallery → specifications table → **inks table
with SKUs** (ELS-170, ELS-175, LUS-210) → `Resources` (ungated Specifications PDF + Brochure PDF) →
`Want to learn more? Submit your request here` → footer. Also a `Let Us Call You` modal (name,
email, phone, state/province, description).

### 3.5 Kornit Atlas MAX PLUS — <https://www.kornit.com/printer/atlas-max/>

Interesting for its *specs-as-copy* approach: instead of a table above the fold it places three
callouts beside the product photo — `Ink channel: CMYKRG + White + Q.fix + Intensifier`,
`Print area: Up to 90×60 cm`, `Speed: Up to 150 impressions per hour`. Then MAX Technology →
Neopigment™ Olympia Ink → XDi Technology → QualiSet → Kornit Konnect → Service & Support →
5-testimonial carousel → 7 related-product cards. CTAs: `Book a Demo`, `Download Brochure` (PDF).

### 3.6 Synthesised canonical PDP skeleton

```
1  Hero            product name · one-line positioning · one large still · primary CTA
2  Hero metrics    3–5 oversized numbers (size / speed / channels / duty cycle)
3  Why it matters  4–8 icon or image feature blocks
4  Configurator    "Options" — what can be added, as an expandable list
5  Media           application carousel (6–8 images, real jobs, captioned)
6  Consumables     which inks run in this machine  ← the dealer's margin lives here
7  Specifications  grouped table (own page or collapsible), unit toggle
8  Comparison      this model vs siblings
9  Social proof    case studies / testimonials, linked out
10 Downloads       datasheet + brochure PDFs, UNGATED
11 Service         warranty / support / training
12 Lead capture    demo request form
13 FAQ             3–6 Q&As, marked up as FAQPage JSON-LD
```

---

## 4. How specifications are presented

**Four distinct patterns observed — all four are legitimate:**

| Pattern | Who | Notes |
|---|---|---|
| **Separate `/specifications/` URL** | swissQprint, Canon | Keeps the PDP a sales page; the spec page is a reference page. Best for SEO on long-tail spec queries. |
| **Collapsible section at the bottom of the PDP** | Roland DG, Mimaki | One page, one URL. Roland labels it in the anchor tab bar. |
| **Grouped table with category headings** | Epson | Groups: `Technology` · `Print` · `Paper / Media Handling` · `General` · `Other Features` · `Other` · `LCD and Memory Cards`. |
| **Specs as hero copy, full data in the PDF** | Kornit | Only viable when the buyer is already deep in the funnel. |

**Universal:** every vendor also ships a **PDF datasheet**, and in every case checked
(swissQprint, Roland DG, Mimaki, HP, Kornit, Canon) **the PDF is ungated** — a direct link, no form.
Canon even gives it its own H2 (`Download Datasheet`). Gating the datasheet is a dealer-site tell.

**Premium detail:** swissQprint's spec page and comparison table both have a **metric ⇄ imperial unit
toggle**. Cheap to build, immediately signals "we sell internationally".

### 4.1 Canonical English spec field names

**swissQprint — full flatbed/UV field list** (verbatim row labels from the live comparison tool,
<https://www.swissqprint.com/uk/en/cta/compare-printers/> — this is the single best reference for a
UV flatbed data model):

```
Productivity        Top speed · Production · Quality · Fine Art
Dimensions          Flatbed, full bleed · Clearance · Substrate weight · Roll width ·
                    Roll weight · Roll diameter · Roll material thickness
Equipment           Curing · Roll to roll option · Dual roll option · Tandem function ·
                    Print area, Tandem each zone · Tip Switch Vacuum
Colours             Colour channels · Print heads · Print heads per channel ·
                    Light cyan, light magenta, light black · Primer · White · Varnish ·
                    Orange · Neon yellow, neon pink
Inks                Integrated ink supply · UV-curable inks · White feed and maintenance system ·
                    Indoor and outdoor applications
Resolution          Addressable resolution · Visual resolution
Physical            Dimensions (L×W×H) · Weight
Compliance          Safety standards · Power supply · Temperature range · Relative humidity ·
                    Installation environment
```

**Canon Arizona 2300 — spec group headings** (verbatim `<h4>`s on the specifications page):
`Printing Technology` · `Ink Configurations` · `Resolution` · `Print speed` · `Ink System` ·
`System Architecture` · `Geometric Accuracy` · `Rigid Media` · `Rigid Media Print Area` ·
`Media Roll Specification` · `Roll Media Print Width` · `Image Processing` · `Connectivity` ·
`Arizona Xpert` · `Electrical Power / Compressed Air` · `Environment` · `Size/Weight`.

Canon's `Print speed` is a full matrix — rows are named print modes
(`High-Key`, `Express`, `Production-Fast`, `Production`, `Production Plus`, `Quality`,
`Quality-Plus`, `Quality-Matte`, `Quality-Density`, `Quality-Layered (2)`, `Quality-Layered (3)`,
`Fine Art`, `High Definition`, `Varnish (High Gloss)`), columns are model variant × `Flatbed`/`RMO`
× `m²/h`/`ft²/h`. `Geometric Accuracy` sub-fields: `Line length (system width)`,
`Line length (system height)`, `Line straightness (system width)`,
`Line straightness (system height)`, `Diagonal Error ("square-ness")` — each with
`Measured Over` and `Maximum Error`.

**Roland DG — roll/print-cut field list** (verbatim, from the XG-640 spec table):
`Printing method` · `Media` (`Width`, `Thickness`, `Roll outer diameter`, `Roll weight`,
`Core diameter`, `Printing/cutting width`) · `Ink` (`Type`, `Colours`, `Printing resolution`) ·
`Cutting speed` · `Blade force` · `Blade` (`Type`, `Offset`, `Software resolution`) ·
`Media heating system` · `Connectivity` · `Power-saving function` · `Rated input` ·
`Power consumption` · `Acoustic noise level` · `Dimensions` · `Weight` · `Environment` ·
`Included items`.

**Durst — the short-form set** used in the Virtual Showroom (verbatim, and a good "minimum viable"
spec set for sample data):
- `PRINTING SPECIFICATIONS`: `Productivity` · `Resolution` · `Drop size modulation` · `Printheads` ·
  `Standard colors` · `Additional color options`
- `MEDIA SPECIFICATIONS`: `Maximum printing width on boards` · `Max. board thickness` ·
  `Minimum board size` · `Maximum printing width on 1 roll` ·
  `Maximum printing width on 2 rolls (side by side)` ·
  `Maximum roll weight (SingleRoll & DualRoll)` · `Maximum roll diameter` · `Roller tables length`

**Mimaki:** `Print head` · `Print Resolutions` · `Print Speed` · `Maximum Print Width` ·
`Maximum Media Width` · `Maximum Media Thickness` · `Maximum Media Weight` · `Ink Type` ·
`Ink Package Size` · `Interface` · `Power Supply` · `Power Consumption` ·
`Operational Environment` · `Dimensions` · `Weight` · `Certifications`.

---

## 5. Media / gallery patterns on product pages

- **Application carousel is the dominant gallery**, not a product-photo gallery. Roland's
  `Endless Applications Infinite Possibilities` (8 slides, Previous/Next), HP's
  `Ultimate versatility to expand into new applications` (6 slides: Retail, Indoor signage, Outdoor
  signage, Window graphics, Décor, Vehicle wraps), Mimaki's 8-image applications gallery. The images
  are **printed output in situ**, not the machine.
- **Machine photography is usually a single hero still.** swissQprint and Canon show one large
  product image, no gallery, no lightbox.
- **Video is linked, not embedded.** Canon's Arizona PDP has zero video elements. HP uses three
  *thumbnail cards* that link out. Durst's showroom pulls ~15 YouTube thumbnails but plays them in
  the YouTube iframe API.
- **Lightboxes are basically absent** in this category.
- **Charts:** Durst's PDP loads Chart.js and renders productivity charts inline — a nice premium
  touch for making a speed number feel evidenced.

---

## 6. 3D / 360 / configurator / AR — exactly what exists and how it is built

This is the section that matters most for the Maven 3D requirement. **Only one vendor ships a real
in-browser 3D model of the machine: Durst.** Everything else is either a 2D hotspot diagram, a
themed video hub, or a post-sale service tool.

### 6.1 Durst Virtual Showroom — the only true WebGL machine viewer ★

**URL:** <https://showroom.durst-group.com/en/P5-350-HS>
Index: <https://showroom.durst-group.com/>. Deep-linkable per machine
(`/en/LF-BB`, `/en/LF-GF`, `/en/LF-GT`, `/en/P5-500-TEX-iSUB`) **and per ink**
(`/en/Inks/aturion_led`, `/en/Inks/Roll_Led`, `/en/Inks/Pop_Flex_Led`, `/en/Inks/FLT_Led`,
`/en/Inks/Sublifix`, `/en/Inks/WT_Food`), with a `?machineID=` query param that cross-links an ink
back to the machine that runs it (e.g. `/en/Inks/Roll_Led?machineID=26`).

**How it is triggered and framed:** it is **not** embedded in the product page. The PDP at
`durst-group.com/en/products/p5-350-hs/` shows a large `VIRTUAL SHOWROOM` CTA next to `CONTACT US`,
which jumps to the separate subdomain. The showroom page carries its own breadcrumb —
`VIRTUAL SHOWROOM > LARGE FORMAT PRINTING > P5 350/HS` — and its own section order:
`Description` → `Technical Data (Printing Specifications)` → `Technical Data (Media Specifications)`
→ `Features` → `Applications` → `Downloads` → `Make Contact`.

**Verified stack** (from `performance.getEntriesByType('resource')` in headless Chrome):

| Asset | Transferred |
|---|---|
| `/Scripts/webgl/r129/build/three.module.js` | **1,152,916 B (1.1 MB, unminified)** |
| `/Scripts/webgl/r129/examples/jsm/loaders/GLTFLoader.js` | 96,043 B |
| `/Scripts/webgl/r129/examples/jsm/controls/OrbitControls.js` | 26,187 B |
| `postprocessing/EffectComposer.js` + `RenderPass` + `ShaderPass` + **`OutlinePass.js`** | ~31 KB |
| `shaders/FXAAShader.js` + `GammaCorrectionShader.js` + `CopyShader.js` | ~48 KB |
| `lines/Line2.js` + `LineGeometry.js` + `LineMaterial.js` + `LineSegments2.js` | ~25 KB |
| `tween-18.6.4.umd.js` | 32,503 B |
| custom `vsr/modules/20221109/`: `CSTLabelUtils.js`, `CSTControlsAndButtons.js`, `CSTLights.js`, `CSTSceneUtils.js`, `CSTUX.js`, `CSTGlobals.js`, `CSTLoggerConsole.js` | ~86 KB |
| `Machines/gltf/p5-350-hs/20210701/p5-350-ng/scene.gltf` | **513 KB (JSON, not `.glb`, no Draco)** |
| `…/scene.bin` | **1,384 KB** |
| 10 textures (`SCREEN_baseColor.png` 91 KB, `TONER_*_baseColor.jpeg` ~11 KB each) | ~215 KB |
| `r129/examples/fonts/Roboto_Regular.json` | (three.js TextGeometry font for 3D labels) |
| **Total page weight** | **~4.7 MB** |

So: **three.js r129, `OrbitControls`, `GLTFLoader`, `OutlinePass` for part highlighting, `Line2` for
leader lines from labels to parts, `TextGeometry` for in-scene labels, TWEEN.js for camera moves.**

**UX, precisely:**
- Markup is `<div id="canvasContainer">` containing a `.spinner-container` with
  `/media/img/spinner/spinner-radar-black.svg` overlaying `<canvas id="c">`. **The spinner is the
  loading state** — no progress %, no low-poly placeholder, no blurhash. On a 2 MB model this is a
  visible dead moment.
- Controls: orbit + zoom by drag/scroll (OrbitControls). No explicit on-canvas control chrome.
- **Hotspots are glTF node names.** The page defines
  `JSHighlightUtils_AddMachineHighlightsTESTP5350(gltf, HIGHLIGHT_ASSOC_ARR)` which traverses the
  scene and maps mesh names → semantic hotspot keys:

  | glTF node name (Blender object) | hotspot key |
  |---|---|
  | `TonerBoxes` | `SAFE_INK` |
  | `BLACK_2` | `ROLL_TABLE_BACK` |
  | `ROLLERS` | `ROLLERS` |
  | `RUBBER_PRINT_BED` | `RUBBER_PRINT_BED` |
  | `MULTIFRONT` | `MULTIFRONT` |
  | `PRINTHEAD` | `PRINTHEAD` |
  | `MULTIREAR` | (rear multi-roll) |
  | `350_DUAL_ROLL_Instance` | `DUAL_ROLL` / `MULTI_ROLL` |
  | `Black_Body` | `CORRUGATED_OPTION` |

- **In-scene configurator toggle:** `<a id="buttonShowDurstAutomat" data-checked="0"
  class="button-scene-action">AUTOMAT MT</a>` sits inside the canvas container and toggles the
  Automat MT automation module into/out of the 3D scene. That single button is the entire
  "configurator" — and it is very effective.
- Global config flags exposed on `window`: `INITIAL_GLTF_URL`, `GLTF_SET_INITIAL_SCALE`,
  `GLTF_PLAY_ALL_ANIMS_ON_LOAD` (so models can carry baked animations), `MACHINE_ID`,
  `LOG_CLICKED_GLTF_OBJECT` (a debug flag left in production).
- Lead form directly under the viewer: `Name`, `Surname`, `Company`, `Country` (select),
  `Phone`, `EMail`, `Message`, newsletter checkboxes segmented by product line
  (`LFP`, `Label`, `Textile`, `Ceramics`, `Software`), privacy-policy checkbox, Google reCAPTCHA v3.

**What to steal, what to fix:** steal the node-name→hotspot mapping, the OutlinePass highlight, the
leader-line labels, and the option-toggle button. Fix: ship `.glb` with Draco or Meshopt (their
2.1 MB of geometry should compress to ~200–400 KB), use a minified three.js build or import-map
+ ESM from a bundle, KTX2/WebP textures, and replace the bare spinner with a real progress readout.

### 6.2 HP — 2D interactive hotspot explorer (no WebGL)

**URL:** <https://www.hp.com/us-en/printers/large-format/latex-r-series.html>
A labelled diagram of the HP Latex R2000 Plus with **9 numbered hotspots** that reveal features
(easy white ink system, HP Latex Overcoat, automatic printhead maintenance, two touchscreens, …).
This is the pragmatic 80/20 alternative to 3D: one high-res still + absolutely-positioned hotspot
buttons + a panel. Zero load cost. **Maven should build this for every machine, and 3D for the
flagships only.**

HP has *also* shipped a 3D virtual booth for the Latex 700/800 launch with 360° interactive
simulation — but that was an event microsite, reported by trade press
(<https://www.largeformatreview.com/hardware/wide-format-print/virtual-booth-showcases-new-hp-latex-700-and-800-printers>),
not a persistent product-page feature.

### 6.3 Roland DG — retired on the EU site; AR is a *service* tool

- `https://www.rolanddg.eu/en/virtual-showroom` **now 301s to the homepage** — the EMEA Virtual
  Showroom (360° renderings of TrueVIS, announced at
  <https://www.rolanddg.eu/en/company/pressroom/roland-dg-launches-emea-virtual-showroom>) has been
  retired. `https://www.rolanddga.com/sites/3d-showroom` also fails to load.
- Roland's AR is **post-sale**: an app that lets a Roland DGA Care engineer look inside a customer's
  machine to troubleshoot remotely (<https://www.rolanddga.com/blog/how-roland-dga-is-using-virtual-tool>).
- Verified: **neither** the TrueVIS XG-640 nor the VersaOBJECT MO PDP contains any 3D, 360 or AR.

**Lesson:** virtual showrooms built as standalone microsites rot. Build the viewer as a component of
the product page, in the same repo, or it will be dead in three years.

### 6.4 Mimaki — themed video hub, not 3D

<https://www.mimakieurope.com/digital-showroom/> is a **metro/transit-map metaphor**, not WebGL:
four lines — `SG Line` (Sign & Graphics roll-to-roll), `IP Line` (Industrial Products / UV flatbeds),
`TA Line` (Textile & Apparel), `3D Express` — with themed stops (`Sign City`, `Textile Town`,
`Industrial Valley`, `3D Dunes`) that open demo videos, tutorials, webinars and expert profiles.
Charming, cheap, and it organises video assets that would otherwise be a dumping ground.
Mimaki's AR work is *print-application* AR (printed graphics that come alive on a phone), not
product visualisation — e.g. the UJV100-160Plus / Doddz exhibition
(<https://www.texintel.com/press-room/mimaki-ujv100-160plus-shines-at-doddz-exhibition-with-augmented-reality-and-digital-print>).

### 6.5 Everyone else

swissQprint, Canon, Kornit, Epson, Mutoh: **no 3D, no 360, no AR, no configurator** anywhere on the
product pages (verified — Canon's Arizona PDP has `0` `<canvas>` and `0` `<model-viewer>` elements).

**Strategic conclusion: a well-executed, fast three.js viewer on a Turkish dealer's site would put
Maven ahead of every OEM in this category except Durst.**

---

## 7. Applications / industries ↔ products cross-linking

Three working models:

1. **swissQprint — flat, symmetrical.** Seven application pages:
   `/uk/en/applications/sign-display/`, `/interior-decor/`, `/packaging/`, `/fineart/`,
   `/glass-printing/`, `/industrial-printing/`, `/wood-printing/`. Every PDP carries an
   `Application areas` tile grid linking out; every application page links back to
   `All printers` / `Flatbed printers` / `Roll to roll printers`. Application pages use one big
   1200×1200 image + a short headline + an action phrase (`Create impact`, `Transform spaces`,
   `Make an impression`).
2. **Durst — three-hop, ink-terminated.** `Application segment → printing system → compatible ink`.
   The application page carries a `Find ink` module organised by printer family, so the journey ends
   on a consumable with a `Technical details` link. **This is exactly the journey a dealer that sells
   both machines and inks needs.** Durst's application taxonomy is granular and worth borrowing:
   traffic signs, soft signage, corrugated packaging, industrial decoration, indoor decoration,
   outdoor application, signage and advertising, variable data, specialty packaging, pharmaceuticals,
   food/beverages, beauty/care, wine/spirits, ceramic tiles.
3. **Case studies as the third leg.** Canon's Arizona PDP lists **8** `Relevant Case Studies`.
   swissQprint's `Showcases` are filterable by `Sign & Display`, `Packaging`,
   `Fine Art / Art reproduction`, `Interior Design`, `Industrial printing`, `Other`; each card is an
   image + an outcome headline (`When reliability drives growth`) + a subtitle stating the business
   result (`A second swissQprint in just six months`) — **not** a product name. Roland DG and Mimaki
   both promote `Case Studies` to the top-level nav.

---

## 8. Lead-capture patterns for high-ticket B2B machines

**The dominant CTA is `Book a demo`, not `Get a quote`.** Nobody in this category asks for a price
request on a €200k machine; they ask for a meeting.

| CTA | Who | Gated? |
|---|---|---|
| `Book a demo` / `Book a Demo` | swissQprint, HP, Kornit | form, ungated content |
| `Request a Consultation` | Roland DG | form |
| `Contact an HP Latex Expert` / `Have an Expert Contact Me` | HP | form |
| `Request Samples` | HP | form — **printed sample kit; strong for a dealer** |
| `Let Us Call You` (modal) | Mimaki USA | form: name, email, phone, state/province, description |
| `Download Brochure` / `Datasheet` | all | **ungated direct PDF** |
| `FIND YOUR LOCAL PARTNER` | Durst (footer) | dealer locator |
| `Want to learn more about the Arizona 2300 FLXflow?` | Canon | inline block on the PDP |

**Exact field sets observed:**

- **swissQprint `Book a demo`** (<https://www.swissqprint.com/uk/en/contact/book-a-demo-uk/>):
  `Select location *` (dropdown) · `Company *` · `First name *` · `Last name *` · `E-mail *` ·
  `Phone` · `Country *` · ☐ *I would like to sign up for the swissQprint newsletter.* ·
  ☐ *I have read the privacy policy and I accept it.* → **`Submit`**.
  Note: **`Company` is required and comes before the personal name** — a B2B tell. Note also that
  the page gives **no "what happens next"** copy, which is a miss worth fixing on Maven.
- **Durst showroom form:** `Name` · `Surname` · `Company` · `Country` (select) · `Phone` · `EMail` ·
  `Message` · newsletter checkboxes per product line (`LFP`, `Label`, `Textile`, `Ceramics`,
  `Software`) · privacy checkbox · reCAPTCHA.

**Pricing:** only Mimaki USA publishes list prices (`List Price (USD): UJ330H-160: $39,995`).
Everyone else omits price entirely.

---

## 9. What makes these feel premium (and what makes a dealer site feel cheap)

**Premium signals actually observed:**
- Numbers as hero typography. swissQprint's `253 m²/h` is set at display size with no table around it.
- One hero still, shot on seamless white, no slider. Restraint reads as confidence.
- A **model comparison table on every PDP** — implies a coherent portfolio, not a parts bin.
- **Metric ⇄ imperial toggle** (swissQprint).
- **Ungated PDFs.** Every single one.
- **Named, ownable technology terms** with their own pages: `Arizona FLOW` / `FLXflow`,
  `VariaDot imaging technology`, `Tip Switch Vacuum`, `Tandem function`, `QualiSet`, `XDi`,
  `Waveform Control`, `Advanced Pass System`. Even for sample data, invent and consistently reuse
  2–3 such terms per machine.
- **Certification badges** rendered as marks, not text: GREENGUARD Gold, UL ECOLOGO, iF DESIGN AWARD.
- **Sustainability / power consumption as a headline spec** (`2.2 kWh`, `Greentech`, `no VOCs`).
- **Warranty as a hero proof-point** (`36 months warranty`, `Roland DG Care`,
  `Protect Your Investment`).
- Structured data: Canon emits `Product` + `FAQPage` + `BreadcrumbList` JSON-LD.

**Cheap-dealer tells to avoid:**
- Gated brochure downloads.
- Stock photography of generic offices.
- A single flat "Products" list with no facets.
- Specs pasted as an image or an unstyled PDF-dump table.
- Multiple competing CTAs of equal weight in one block.
- No case studies / no named customers.
- A dead microsite link (see Roland's retired virtual showroom, §6.3).

---

## 10. Direct implications for the Maven build

1. **Nav:** `Ürünler` · `Uygulamalar` · `Mürekkep & Sarf` · `Teknik Servis` · `Kurumsal` ·
   `İletişim`. Put inks/consumables at top level as a sibling of products — four of five OEMs do.
2. **Routing / i18n:** locale-prefixed `/{lang}/…` (Durst model), `tr` default, `en` second, with a
   locale-keyed slug map so URLs are translated (`/tr/urunler/…` ↔ `/en/products/…`). Emit
   `hreflang` + `x-default` on every page — Canon's omission is a real defect, not a pattern.
3. **Product model:** one JSON schema per machine, fields taken from the swissQprint comparison list
   (§4.1) so a comparison table is generated, not hand-written. Include `applications[]` and
   `inks[]` as relation arrays — these drive the cross-link modules in both directions.
4. **PDP skeleton:** use §3.6 verbatim. Specs go in a collapsible section on the PDP *and* get a
   crawlable `/ozellikler/` sub-route.
5. **Metric/imperial toggle** on specs and comparison. Cheap; nobody in Turkey does it.
6. **Galleries:** the carousel should be *application photography*, not machine angles. Machine gets
   one hero still + the 3D viewer.
7. **3D:** three.js + `.glb` with Draco/Meshopt, `OrbitControls`, `OutlinePass`-style highlight,
   named Blender objects mapped to hotspot keys (copy Durst's `PRINTHEAD` / `ROLLERS` /
   `RUBBER_PRINT_BED` naming discipline), one option-toggle button in-canvas, and a **real progress
   indicator**. Budget: keep the whole model under 1 MB — Durst ships 2.1 MB of geometry and a
   1.1 MB unminified three.js, and it is the weakest part of their otherwise excellent viewer.
   Lazy-load the viewer on intersection/click so it never blocks LCP.
8. **Also build the cheap version:** a 2D hotspot explorer (HP model) for every machine that does not
   justify a Blender model.
9. **Lead capture:** single dominant CTA `Demo talep edin`. Fields: `Firma *`, `Ad *`, `Soyad *`,
   `E-posta *`, `Telefon`, `Ülke/İl`, `İlgilendiğiniz ürün` (prefilled from the PDP), message,
   KVKK consent checkbox. Add the "what happens next" line swissQprint is missing. Static-site
   constraint: post to Formspree/Web3Forms or a Vercel form endpoint.
10. **Add `Numune talebi` (request printed samples)** — HP's `Request Samples` is the highest-intent
    B2B CTA in the category and is perfect for a dealer with a demo room.
11. **Ungate every PDF.** Datasheet + brochure as direct links, given their own section.
12. **JSON-LD:** `Product`, `BreadcrumbList`, `FAQPage`, `Organization` on every PDP.
13. **Case studies (`Referanslar`)** filterable by application, with outcome-led headlines
    (swissQprint's copy pattern), cross-linked from both PDPs and application pages.
14. **Invent and reuse 2–3 named technology terms per machine** in the sample data — it is the
    cheapest single thing that separates OEM-grade copy from dealer-grade copy.

---

## 11. Source list

- <https://www.swissqprint.com/ch/en> · `/uk/en/printers/` · `/uk/en/flatbed-printer/nyala-5/` ·
  `/uk/en/flatbed-printer/nyala-5/specifications-nyala-5/` · `/uk/en/cta/compare-printers/` ·
  `/uk/en/applications/` · `/uk/en/showcases/` · `/uk/en/contact/book-a-demo-uk/`
- <https://www.durst-group.com/en/> · `/en/products/p5-350-hs/` · `/en/applications/signage-and-advertising/`
- <https://showroom.durst-group.com/en/P5-350-HS> (+ `/Machines/gltf/p5-350-hs/20210701/p5-350-ng/scene.gltf`,
  `/Scripts/webgl/r129/…`)
- <https://www.canon-europe.com/business/products/large-format-printers/arizona-2300-series/> ·
  `…/specifications/`
- <https://www.rolanddg.eu/en/products/printers> · `/truevis-xg-640` · `/versaobject-mo-series` ·
  `/en/virtual-showroom` (now 301) · <https://www.rolanddga.com/blog/how-roland-dga-is-using-virtual-tool>
- <https://mimaki.com/> · <https://www.mimakiusa.com/products/> · <https://www.mimakiusa.com/uj330h-160/> ·
  <https://www.mimakieurope.com/digital-showroom/>
- <https://www.hp.com/us-en/printers/large-format/latex-r-series.html> ·
  <https://www.largeformatreview.com/hardware/wide-format-print/virtual-booth-showcases-new-hp-latex-700-and-800-printers>
- <https://www.epson.co.uk/en_GB/products/printers/large-format/surecolor-s80600/p/20155>
- <https://www.kornit.com/printer/atlas-max/>
- <https://mutoh.eu/en/products>
- <https://www.texintel.com/press-room/mimaki-ujv100-160plus-shines-at-doddz-exhibition-with-augmented-reality-and-digital-print>

**Not reachable:** `agfa.com` (bot CAPTCHA), `efi.com` VUTEk product URLs (404 — business divested),
`base.brother.com` (DNS). If Agfa/Brother patterns are needed later, try a non-headless browser or
regional mirrors.
