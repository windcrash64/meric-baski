# Track 3 — Ink & Consumables Product Presentation

Research for the Maven corporate site (Turkish dealer/distributor of digital printing machines +
inks/consumables + technical service). Static site, TR default + EN, Vercel.

Verified July 2026 against live vendor sites and current TDS/PDF documents. Every non-obvious claim
is cited inline. Sources fetched: 21 (list at the end).

---

## 0. The single most important structural finding

**Serious ink pages are not e-commerce pages.** Every manufacturer and technical distributor studied
uses a *specify-then-enquire* pattern, never a cart:

| Vendor | Primary CTA on an ink product page |
|---|---|
| Nazdar | "Request More Information" → contact form ([nazdar.com](https://www.nazdar.com/en-us/P/4399/203-Series-Digital-Ink)) |
| Bordeaux | "Get a Quote" + *"Authorized resellers, please login for complete product information"* ([c-m-y-k.com](https://c-m-y-k.com/product/fuze-eco-trv2/)) |
| Nazdar (global) | "Where to Buy" / "Find a Distributor" in top nav |
| Gür Dijital (TR) | "Ürünü incele" / "Bize Ulaşın" ([gurdijital.com](https://www.gurdijital.com/urun-kategori/eco-solvent-baski-murekkebi)) |

The only site studied that shows prices on ink is a small Turkish reseller (Printec, `719,00 ₺ –
1.437,99 ₺ + KDV`) — and that same page also contains a factual error ("UV mürekkebi su bazlı sıvı
bir mürekkeptir" — UV ink is *not* water-based). That contrast is our positioning opportunity:
**correct technical content + quote CTA reads as a real distributor; price + wrong chemistry reads as
a dropshipper.**

→ **Decision: no prices, no cart. Every ink page ends in "Teklif İsteyin" / "Request a Quote" plus a
"Uyumluluk kontrolü" (compatibility check) contact hook.**

---

## 1. Anatomy of an ink product page — section by section

Synthesised from Nazdar, Bordeaux, InkTec Europe, Marabu, Kiian and INXJet. The **bold** sections are
present in ≥4 of the 6; the rest are strong differentiators.

| # | Section | TR label | Evidence |
|---|---|---|---|
| 1 | **Breadcrumb** (3 levels: catalogue → family → product) | Anasayfa › Mürekkepler › UV & UV-LED › … | Nazdar: `Home > Digital Inkjet Inks > Inks By Chemistry > Eco-Solvent Inkjet Inks` |
| 2 | **Product name + one-line role** ("For Mimaki UV LED printers") | Ürün adı + alt başlık | Bordeaux `PLASMA LED MK120 / For Mimaki Printers` |
| 3 | **Image gallery** (bottle/pouch shot + print-sample shot) | Görseller | All |
| 4 | **Positioning paragraph** — usually "alternative to OEM ink X" | Açıklama | Nazdar 203: *"designed as a high quality alternative to Roland™ Eco Max 3 original inks"* |
| 5 | **Key features / benefits** — 4–7 bullets | Öne çıkan özellikler | Bordeaux "Benefits and Primary Features"; Marabu "Key features" |
| 6 | Qualitative property ratings | Performans profili | Marabu "Ink properties" table: `Colour Gamut +++ / Flexibility +++ / Pigmentation +++` |
| 7 | **Colour range / channel set** (with per-colour item codes) | Renk seti / kanal yapılandırması | Kiian per-colour codes `501215 Yellow` … ; Marabu shade numbers `428 Yellow, 459 Cyan, 489 Black, 170 White` |
| 8 | **Packaging** | Ambalaj | Bordeaux `1L bottle / 600ml bag`; Nazdar `1, 5, and 8 liter containers` |
| 9 | **Compatible printers** (model list) | Uyumlu makineler | Bordeaux: `Mimaki JFX Plus series, UJF-3042 FX/HG, UJF-6042, UJV-160` |
| 10 | **Compatible printheads** | Uyumlu baskı kafaları | InkTec SE Series: `Epson DX4, DX5, DX7, XP600, i3200` |
| 11 | **Substrates / media** + "always test adhesion" caveat | Uygulanabilir yüzeyler | Nazdar 730 substrate list + *"Adhesion should always be tested…"* |
| 12 | Cure / fixation parameters | Kürleme / fiksaj | Nazdar 730: `225–300 mJ/cm² and 600 mW/cm²` (EIT UviCure Plus, UVA); Marabu: `395 nm`, post-cure 24 h; Kiian: transfer `180–220 °C` |
| 13 | Durability claim, scoped | Dış mekân dayanımı | Nazdar 730: `24 months' vertical outdoor exposure` (central U.S. test); Marabu: `at least 2-year vertical outdoor exposure, middle European climate` |
| 14 | **Shelf life + storage** | Raf ömrü ve depolama | Nazdar `12 months from date of manufacture`, `18–27 °C`; Marabu `1 year`, `15–25 °C` dark; Kiian `15 months`, `< 25 °C`; Triangle `12 months`, `15–30 °C` |
| 15 | Environmental operating window | Çalışma ortamı | Nazdar: temp `18–27 °C`, humidity optimum `40–60 %` non-condensing, operational `30–70 %` |
| 16 | Ink changeover / conversion procedure | Mürekkep geçişi | Marabu's three-tier model (see §4); Nazdar "Ink Changeover" + flush code `LWU7001FF`; Kiian "SPECIAL INSTRUCTIONS – INK CONVERSION" |
| 17 | Ancillaries / auxiliaries (cross-sell) | Yardımcı ürünler | Nazdar: adhesion promoters 7020/7025/7030, overprint clears, flush; Marabu: `DI-UR`, `DI-UR 3`, `P 2 Primer`; Kiian: capping fluid, cleaner, cleaner NFS |
| 18 | **Downloads: TDS + SDS** | Belgeler: TDS / GBF | Nazdar has a dedicated SDS route `/SDS?inkseries=203`; Bordeaux tab "Product Files"; InkTec: `SE-Series-UV-ink-TDS.pdf` + `ECO PASSPORT Certificate` |
| 19 | Certifications | Sertifikalar | GREENGUARD Gold, ECO PASSPORT, ISO 9001/14001 |
| 20 | **Legal disclaimer** | Yasal uyarı | Nazdar "Product Disclaimer"; Marabu "Note"; Kiian "IMPORTANT NOTE" — all say *the user must test* |
| 21 | **CTA: quote / where to buy** | Teklif isteyin | §0 |
| 22 | Related: the machine this ink runs in | İlgili makine | our own addition — we sell both, nobody else studied does |

**Nazdar's tab split is the cleanest and is what I recommend copying:**
`Product Description` | `Benefits & Specifications` | `Links & Downloads`
(TR: `Ürün Açıklaması` | `Özellikler ve Teknik Veriler` | `Belgeler ve İndirmeler`).

Bordeaux uses only two: `Additional information` | `Product Files`.
Turkish resellers use WooCommerce defaults: `Açıklama` | `Ek bilgi` | `Yorumlar` — **drop "Yorumlar",
it is a dropshipper tell.**

---

## 2. The attribute dictionary (exact field names observed → our data model)

These are the labels actually used in the wild. Left column = our JSON key.

### Identity
| Key | Observed label(s) | Example value |
|---|---|---|
| `sku` | "Item Number" (Nazdar), "Code N°" (Kiian), "Model Name" (InkTec) | `LWU730CY`, `501215`, `SE-B01KC` |
| `series` | "Series" | `730 Series`, `PLASMA LED MK120`, `SE Series` |
| `family` | "Ink Chemistries" (Nazdar), "Ink Type" (INXJet) | `uv-led` |
| `oemEquivalent` | "alternative to …", "Mix & Match with …" | `Mimaki LUS-120`, `Roland Eco Max 3`, `HP 831` |

`oemEquivalent` is load-bearing in this market. Bordeaux literally names latex products after the HP
cartridge they replace — **EDEN LX792** ↔ HP 792, **EDEN LX831** ↔ HP 831
([c-m-y-k.com](https://c-m-y-k.com/products/latex-based-ink/)). Bordeaux's eco-solvent series encodes
the target machine in the suffix: `FUZE ECO TRV2` (Roland TrueVIS TR2), `MT` (Mutoh), `PR4` (Roland
Pro4), `ME` (Mimaki), `SC` (Epson SureColor), `GS` (Epson GS6000).

### Chemistry & process
| Key | Observed label(s) | Example |
|---|---|---|
| `chemistry` | "Ink Chemistries" | UV curable / UV-LED / eco-solvent / mild solvent / true solvent / aqueous / latex / sublimation / DTF pigment / textile pigment / reactive / acid / disperse |
| `cureMethod` | "Curing", "Curing Parameters" | UV mercury-vapour / UV-LED 395 nm / heat 160 °C / calender transfer 180–220 °C |
| `cureDose` | "225 – 300 mJ/cm² and 600 mW/cm²" | Nazdar 730, EIT UviCure Plus, UVA band |
| `postCure` | "post-curing … final adhesion after 24 hours" | Marabu DLE-JX |
| `viscosity` | "Viscosity" | `4.0 cps ± 0.5 @ 25 °C` (DTF) |
| `surfaceTension` | "Surface Tension" | `30 ± 3 dynes/cm @ 25 °C` (DTF) |
| `ph` | "pH" | `9.0 ± 0.5` (DTF, aqueous only) |
| `particleSize` | "Pigment Particle Size" | white D50 `200–250 nm` |

Viscosity/surface tension/pH appear **only on aqueous/textile/DTF TDS**. UV and solvent TDS from
Nazdar and Marabu publish *no* viscosity at all — they publish cure dose and substrate lists instead.
Do not invent viscosity numbers for UV inks; it signals fake data.

### Compatibility
| Key | Observed label(s) | Example |
|---|---|---|
| `printheads` | "Compatible Printheads", "COMPATIBLE WITH DX7 PRINTHEADS (and preceding)" | Epson DX4/DX5/DX7/XP600/i3200/T3200; Ricoh Gen5; Konica Minolta; Kyocera KJ4A; Spectra StarFire; Toshiba |
| `dropSizeRange` | INXJet facet | `5-50 Picoliter` … `40-105 Picoliter` |
| `printers[]` | "Validated Equipment" (Nazdar), "Field of use" (Marabu), "Printer Compatibility" (Bordeaux) | `Inca Onset S40i`, `Durst P10`, `Mimaki JFX200/500` |
| `chipIncluded` | "including chips", "Including LUS120 chips" | InkTec SE, Marabu DLE-JX |
| `changeover` | "Change-Over" | see §4 |

### Colour & packaging
| Key | Observed label(s) | Example |
|---|---|---|
| `channels[]` | "Colour Range / Basic Shades", "Available Colors", "PRODUCTS OF THE SERIES" | `["C","M","Y","K","Lc","Lm","W"]` |
| `packaging[]` | "Packaging", "PACKING", "Manufacturer Product Offering" | `1 L bottle`, `600 ml bag`, `2 L MBS bag` |
| `shelfLifeMonths` | "Shelf Life", "SHELF LIFE", "Storage/Shelf Life" | 12 / 15 |
| `storageTempC` | "Storage" | `18–27` |

### Application & durability
| Key | Observed label(s) |
|---|---|
| `substrates[]` | "Substrates", "Supported Substrates", "Field of application" |
| `applications[]` | "Inks By Application", "Approved Applications", "Primary uses" |
| `outdoorDurabilityMonths` | "Outdoor Durability", "Fade resistance" — **always scoped**: vertical exposure, named climate |
| `fastness` | Kiian: `EN ISO 105-B02` light, `105-C10` washing, `105-E04` perspiration + sublimation class A–D |
| `washFastness` | DTG: `ISO 105-C06` level 4+ |

### Documents & compliance
| Key | Observed label(s) |
|---|---|
| `tds` | "Technical Data Sheet", "Product Files", "Links & Downloads" |
| `sds` | "SDS (Safety Data Sheet)" — TR: **Güvenlik Bilgi Formu (GBF)** |
| `certifications[]` | GREENGUARD Gold, ECO PASSPORT by OEKO-TEX, ZDHC, EN 71-3, ISO 9001, ISO 14001 |
| `disclaimer` | "Product Disclaimer" / "IMPORTANT NOTE" / "Note" |

---

## 3. Ink families × attributes — the data-model table

This is the table to turn straight into `content/inks/*.json` and the family landing pages. All
numbers are the *realistic ranges* observed in the sources above; use them to author sample data.

| Family (`family`) | TR name | What it's for | Cure / fixation | Typical channel set | Packaging seen | Shelf life | Key spec fields to show | Certs typically claimed |
|---|---|---|---|---|---|---|---|---|
| `uv` (mercury-vapour) | UV kürlemeli mürekkep | Rigid + roll-to-roll flatbed/hybrid, POP, signage | Medium-pressure Hg lamp, `225–300 mJ/cm²`, `600 mW/cm²` | C M Y K Lc Lm + **Lk, Or, W, Clear**; Green/Violet on request | 1 L / 5 L / 8 L bottle; 2 L MBS bag; 3 L & 5 L bag-in-box | 12 mo @ 18–27 °C | cure dose, substrates, adhesion-promoter matrix, outdoor 24 mo | GREENGUARD Gold, EN 71-3 (toy/POP) |
| `uv-led` | UV LED mürekkep | Same, LED lamps: less heat, thin/heat-sensitive media | `395 nm`; post-cure 24 h to final adhesion | C M Y K Lc Lm **W, Varnish/Lak** | 1 L bottle (+chip), 600 ml bag, 250 ml cartridge | 12 mo @ 15–25 °C, dark | 395 nm, flexibility rating, W opacity, chip included | GREENGUARD Gold (JETRIX ULE/ULS) |
| `uv-dtf` | UV DTF mürekkep | UV transfer stickers onto 3D objects (A/B film) | UV-LED + adhesive B-film | C M Y K **W, Varnish** | 1 L bottle | 12 mo | film pairing, laminating pressure | — |
| `eco-solvent` | Eco solvent mürekkep | Indoor/outdoor signage, vinyl, banner — low odour | Air dry + heater | C M Y K (+ Lc Lm, **Or, Gr**) | 220 / 440 / 500 / 600 ml cartridge; 1 L, 2 L pouch | 12 mo @ 15–30 °C | odour class, OEM cartridge equivalence, chip/cartridge type | GREENGUARD Gold (Streamline) |
| `mild-solvent` | Mild solvent | Mid-durability outdoor, faster dry than eco | Heater | C M Y K Lc Lm | 1 L bottle, 2 L bag | 12 mo | drop-size range (pL) | — |
| `solvent` | Solvent (true solvent) | Super-wide 3.2 m, billboards, max durability/cheapest per m² | Heater + ventilation | C M Y K (+Lc Lm) | 5 L / 10 L / 20 L bottle, 5 L BiB | 12 mo | outdoor years, VOC handling, extraction required | — |
| `latex` | Lateks mürekkep | Water-based, odourless prints, wall/indoor, HP-type machines | Heat-cure ~110–120 °C in printer | C M Y K Lc Lm + **Optimizer + Overcoat** | 775 ml cartridge; 3 L bag-in-box | 12 mo | optimizer requirement, no-lamination claim | GREENGUARD Gold |
| `sublimation` | Süblimasyon mürekkebi | Transfer onto polyester ≥80 % PES, sportswear, flag, soft signage | Calender/flat press `180–220 °C`, 30–180 s | C M Y K + **Lc Lm, Blue, Orange, Black Plus/Deep Black, Fluo Pink/Blue/Yellow/Green** | 1 L bottle, 2 L bag, 5 L | **15 mo** @ < 25 °C | sublimation class A–D (180/190/200/210 °C), EN ISO 105-B02/C10/E04 fastness | ECO PASSPORT by OEKO-TEX, ZDHC |
| `dtf` | DTF pigment mürekkep | Film transfer to cotton/blend garments | Powder + oven/press `150–160 °C` | C M Y K + **W (separate, higher volume)** | CMYK **1 L**, White **900 ml** pouch/bottle | CMYK 12 mo, **White 6 mo** | viscosity 4.0 cps, ST 30 dyn/cm, pH 9.0, white D50 200–250 nm, anti-sedimentation | ECO PASSPORT, ZDHC |
| `dtf-powder` | DTF hot-melt tozu | Adhesive for DTF transfers | Melts ~110 °C, cures ~150–160 °C | n/a (white/black powder) | 1 kg / 5 kg / 20 kg bag or drum | 12 mo | **grade by particle size**: fine 0–80 µm, soft 80–170 µm, coarse 120–250 µm | — |
| `textile-pigment` | Tekstil pigment mürekkebi | DTG + direct-to-textile pigment, needs pretreatment | Fixation `160 °C` / 60–90 s (or 2–3 min) | C M Y K + **W** | 1 L, 2 L bag-in-box | 6–12 mo | pretreatment fluid required, ISO 105-C06 ≥4 | ECO PASSPORT, ZDHC, GOTS-compatible |
| `reactive` / `acid` / `disperse` | Reaktif / asit / dispers | Industrial textile: cotton (reactive), silk-wool-nylon (acid), direct-disperse polyester | Steam + wash-off / heat | C M Y K + Or, Bl, Red, Grey | 2 L / 5 L bag-in-box (BIB) | 12 mo | steaming time, wash-off, fastness | ECO PASSPORT, ZDHC |
| `aqueous` | Su bazlı mürekkep | Fine art, photo, indoor POP, low-emission | Air dry | C M Y K Lc Lm Lk + Photo Black / Matte Black | 1 L bottle, 3 L BiB | 12 mo | media coating requirement, lightfastness | GREENGUARD Gold |
| `cleaning` | Temizleme sıvısı / flush | System conditioning, head soak, capping | n/a | n/a | 250 ml pipette bottle, 1 L bottle, cartridge-format | 24 mo | which ink chemistry it matches | — |
| `primer` | Yapışma artırıcı / astar | Adhesion on glass, metal, PP, powder coating | Wipe/spray, flash-off | n/a | 1 L bottle | 12 mo | **substrate × primer matrix** | — |

Colour-set notation to standardise on: `C, M, Y, K, Lc, Lm, Lk, W, Or, Gr, Vt, Cl (varnish/lak), Opt
(optimizer), Ov (overcoat), Fl-P/Fl-B/Fl-Y/Fl-G (fluor)`.

Real-world evidence for the wide sets:
- Nazdar 730 stocks **Cyan, Magenta, Yellow, Black, Light Cyan, Light Magenta, Light Black, Orange,
  White, Clear**, with **Green and Violet "Available Upon Request"** — a nice UI state to model
  (`availability: "on-request"`).
- Kiian Digistar Hi-Pro carries **four fluor shades** (Green/Blue/Yellow/Pink Fluo) plus three blacks
  (Black, Black Plus, Deep Black, Eco Black).
- Bordeaux PLASMA LED MK: `BLACK, CYAN, LT-CYAN, LT-MAGENTA, MAGENTA, WHITE, YELLOW`.

---

## 4. How compatibility is communicated — four patterns, all in use

**Pattern A — printer-model list on the product page.** The default.
`Mimaki JFX Plus series, UFJ-3042 FX/HG, UJF-6042, UJV-160` (Bordeaux); `Inca Onset S40i, Durst P10`
under the heading **"Validated Equipment"** (Nazdar 730). Nazdar's word choice — *validated*, not
*compatible* — is worth stealing; it implies testing.

**Pattern B — a second navigation axis by printer brand.** Bordeaux has a full parallel menu:
`Agfa/Gandi™, DGI™, EFI VUTEK™, Epson™, Fujifilm™, HP Scitex™, Infiniti™, Mimaki™, Mutoh™, OCE™,
Roland™, SEIKO™, Teckwin™`, and every product is filed under both axes (`Inks for Mimaki | Mimaki JFX
Series | Mimaki UJF-Series | UV Curable inks`).

**Pattern C — faceted filters with live counts.** Nazdar's category pages show
`Filter By: → Digital Inks Compatibility by Printer: Epson (1), Mimaki (6), Roland (3)` and
`Ink Chemistries: Eco-Solvent (9), Solvent (10)`, plus Grid/List toggle, a **Compare Products**
checkbox per card, and `Products per page: 12 / 48 / 96 / All`.
INXJet goes further with an **"Advanced Product Selector"** on four axes:
**By Ink Type · By Printer Brand · By Application · By Packaging**, plus a printhead **drop-size**
facet (`5-50 Picoliter` → `40-105 Picoliter`).

**Pattern D — printhead-level compatibility.** InkTec's page title is literally
*"LED UV Inks for Epson Printheads"* and the spec is `Epson DX4, DX5, DX7, XP600, i3200`. This is how
the Turkish market actually shops (people ask "XP600 için mi?"), so it must be a first-class facet,
not buried text.

**Bonus — Marabu's changeover taxonomy is the best UX idea found.** Three named states describing how
hard it is to switch to their ink:

- **Switch & Print** = full chemical and colour compatibility (just print)
- **Switch & Swap** = flushing required
- **Switch & Match** = colour profiling required for best colour match

→ **Decision: implement this as a three-state badge on every alternative-ink product** (TR:
*Doğrudan geçiş* / *Yıkama gerekir* / *Profil gerekir*). It converts an invisible technical risk into
a scannable trust signal, and it is exactly the question a Turkish print shop asks a dealer.

**Also steal: Nazdar's "Printer Reference Charts"** — a standalone printer→ink cross-reference page
(`/DIGITAL-INKS/Printer-Compatibility/Printer-Reference-Charts`). For us this is one static
`/uyumluluk` page: a table of machine model × available ink families, filterable, deep-linking into
both product types. It is the single highest-value page a dealer site can have and almost no Turkish
competitor has one.

---

## 5. Packaging conventions

INXJet (Triangle/INX) exposes packaging as a **navigation facet**, and its label set is the most
complete real-world vocabulary found — copy it verbatim as our enum:

`1 KG Bottle` · `1 LT Bottle` · `1 LT Nite Bags` · `1.5 LT Bag` · `2 LT MBS Bags` ·
`3 LT Bag-in-Box` · `5 KG Bottle` · `5 LT Bottle` · `5 LT Bag-in-Box` · `10 LT Bottle` · `20 LT Bottle`

Cross-referenced with the other sources:

| Format | Where it's used | Real examples |
|---|---|---|
| 220 / 440 / 500 ml cartridge | Eco-solvent & mild-solvent desktop/roll printers | Roland Eco-Sol MAX, Mimaki SS21 (cleaning cartridge also 220 ml) |
| 600 ml bag / 250 ml cartridge | Mimaki UV LED | Bordeaux PLASMA LED MK `600ml bag` |
| **775 ml cartridge** | HP Latex 300/500 | HP 831A/831C |
| **900 ml** | DTF **white only** (asymmetric with CMYK) | STS DTF |
| **1 L bottle** | The default unit for aftermarket UV / DTF / sublimation | InkTec SE (`1 litre bottles including chips`), Kiian (`1 litre`), Bordeaux, virtually all Turkish resellers |
| 1.5 L / 2 L pouch or bag | Bulk feed systems | INXJet `2 LT MBS Bags`, Kiian ink feeder `M4087` |
| 3 L / 5 L bag-in-box | Latex + industrial textile | HP Latex 3 L "bag within a recyclable cardboard box"; textile BIB |
| 5 L / 8 L / 10 L / 20 L bottle | Grand-format UV and true solvent | Nazdar 730: `1, 5, and 8 liter containers` |
| 1 kg / 5 kg / 20 kg | Powders (DTF hot-melt) and kg-denominated inks | INXJet `1 KG Bottle`, `5 KG Bottle` |
| 250 ml with dosing pipette | Capping-station fluid | Kiian `DIGISTAR CAPPING FLUID (CODE 408703)` |

**How it's shown:** as a plain labelled row in a spec table ("Packaging: 1L bottle, 600ml bag"), or as
a *selectable variant* on reseller sites — Printec exposes `Şişe Boyutu: 500 ml / 1 Litre` as a
product option alongside `Mürekkep Rengi: Lak, C, M, Y, K, LC, LM, W`.

→ **Decision: model packaging as an array of `{format, volume, unit, note}` and render it as chips
under the colour row.** Do NOT make it a price-bearing variant selector; make it informational, since
we don't sell online. Show a per-colour availability grid when volumes differ by colour (the DTF
`1 L CMYK / 900 ml White` case is real and common).

---

## 6. Safety & regulatory content — manufacturer vs dealer

### What a manufacturer carries
- **SDS/MSDS per product**, referenced from every page. Nazdar has a site-wide `/SDS` route plus a
  per-series deep link `/SDS?inkseries=203`.
- **TDS** as a separate downloadable PDF, versioned (`v 1.0EN`, `Ref: v1.0 EN`, `FEBRUARY 2025`).
- **Regulatory basis statement.** Marabu: SDS *"according to EC regulation 1907/2006"* (REACH) and
  labelling *"according to EC regulation 1272/2008 (CLP regulation)"*.
- **Chemistry-specific safety rules.** Marabu has a standing block "Safety rules for UV printing
  inks" (UV inks contain skin irritants; wash with soap and water).
- **Handling / PPE.** Nazdar: *"All personnel mixing and handling this product must wear gloves and
  eye protection."*
- **Heavy-metal statement.** Nazdar: formulated to contain *"less than 0.06 % lead"*, with the honest
  caveat *"If exact heavy metal content is required, independent lab analysis is recommended."*
- **Liability limitation.** All three of Nazdar ("Nazdar Quality Statement"), Marabu ("Note") and
  Kiian ("IMPORTANT NOTE") limit liability to the value of goods and put testing responsibility on
  the user.

### The certifications that actually appear, and what they mean
| Mark | Standard | What it certifies | Who claims it |
|---|---|---|---|
| **GREENGUARD Gold** | UL 2818 | Chemical emissions / indoor air quality. Health-based criteria for **>360 VOCs**; allowable predicted TVOC **0.22 mg/m³**; also requires CDPH Standard Method (California Section 01350) compliance. | Sun Chemical Streamline (whole range); InkTec **JETRIX ULE and ULS**; Roland; Agfa UV-LED; Mutoh MS41 |
| **ECO PASSPORT by OEKO-TEX** | OEKO-TEX | Chemical/colorant-level certification for textile & leather manufacturing inputs. | InkTec (certificate offered as a download next to the TDS); Polyprint; Hongsam |
| **ZDHC MRSL** | ZDHC | Restricted-substance conformance for textile chemicals, quoted by level (e.g. "Level 3"). | Textile pigment/DTG ink makers |
| **EN 71-3** | EN 71-3:2013+A1 | Toy safety — *migration of certain elements* (heavy metals). Requires a current test report from an accredited lab (SGS, Intertek) naming the **material categories and specific colour channels** tested. | Relevant to UV inks printed on toys/children's POP |
| **REACH / CLP** | EC 1907/2006 / EC 1272/2008 | SDS content and hazard labelling in the EU. | Marabu, all EU makers |
| **ISO 9001 / 14001** | ISO | QMS/EMS of the *maker*, not the product. Nazdar links its ISO certificate PDF from the footer. | Nazdar, Marabu, InkTec |

### What a **dealer** shows instead (this is us)
A distributor does not own the certification and must not imply it does. The honest, standard pattern:

1. **Re-host or link the manufacturer's TDS and SDS**, labelled with the manufacturer's name and the
   document version/date. Never re-typeset a TDS into HTML and present it as our own spec.
2. **Show certification badges as attributes of the product line, attributed to the maker** —
   "GREENGUARD Gold sertifikalı (üretici: Sun Chemical)". Never as a Maven badge.
3. **Carry a Turkish-language GBF, not a translated English SDS.** This is a hard legal point in
   Turkey (see below) and is a genuine differentiator.
4. **A "Belgeler / Documents" hub page** listing, per product: TDS (EN/TR), GBF (TR), certificate
   scans, and warranty terms.
5. **Warranty language.** Nazdar's whole aftermarket proposition rests on
   *"Fully backed by Nazdar's comprehensive equipment warranty"* + a standalone "Inkjet Ink Warranty"
   page. For a dealer selling third-party ink into OEM machines, an explicit warranty statement is
   the #1 objection-handler. Give it its own page.
6. **The testing disclaimer, in Turkish, on every ink page.** Model it on Bordeaux's:
   *"Ink properties such as weather resistance and adhesion may vary according to the substrate use;
   users must test materials prior to commercial use."*

### Turkey-specific compliance — the highest-value non-obvious finding
- In Turkey the SDS is the **Güvenlik Bilgi Formu (GBF)** and **must be supplied in Turkish**.
- It is governed by **KKDİK** (*Kimyasalların Kaydı, Değerlendirilmesi, İzni ve Kısıtlanması Hakkında
  Yönetmelik* — Turkey's REACH) and **SEA** (*Maddelerin ve Karışımların Sınıflandırılması,
  Etiketlenmesi ve Ambalajlanması* — Turkey's CLP).
- **Since 31 December 2023, a GBF may only be prepared or updated by a certified Kimyasal
  Değerlendirme Uzmanı (KDU)** under KKDİK Annex-18.
- The GBF has 16 mandatory sections, whose Turkish headings are fixed:
  1 Maddenin/karışımın ve şirketin/dağıtıcının kimliği · 2 Zararlılık tanımlanması ·
  3 Bileşim/içindekiler hakkında bilgi · 4 İlk yardım önlemleri · 5 Yangınla mücadele önlemleri ·
  6 Kaza sonucu yayılmaya karşı önlemler · 7 Elleçleme ve depolama ·
  8 Maruz kalma kontrolleri/kişisel korunma · 9 Fiziksel ve kimyasal özellikler ·
  10 Kararlılık ve tepkime · 11 Toksikolojik bilgiler · 12 Ekolojik bilgiler ·
  13 Bertaraf etme bilgileri · 14 Taşımacılık bilgileri · 15 Mevzuat bilgileri · 16 Diğer bilgiler.

→ **Decision: a `/tr/belgeler` (EN `/en/documents`) page that states plainly "Sattığımız tüm
kimyasal ürünler için Türkçe Güvenlik Bilgi Formu (GBF) sağlıyoruz — KKDİK ve SEA yönetmeliklerine
uygun, sertifikalı KDU tarafından hazırlanmış."** No Turkish competitor site found makes this claim,
and every serious industrial buyer needs it for their own ISG file.

---

## 7. Turkish-market vocabulary & IA conventions

Observed on Turkish supplier sites (Troy Makine, Gür Dijital, Center Design, Printec, Meka Dijital):

| Concept | Turkish term(s) actually used | Note |
|---|---|---|
| Ink | **Mürekkep** (correct) / **Boya** (trade colloquial) | Troy Makine's nav literally says **"Boyalar"**; Gür Dijital says **"Dijital Baskı Boyaları"**; Center Design says **"Dijital Baskı Yazıcı Mürekkepleri"** |
| Top-level nav pattern | **Makineler · Boyalar · Yedek Parçalar · 2. El Makineler** | Troy Makine — the canonical Turkish dealer IA |
| Consumables | Sarf malzeme | |
| Spare parts | Yedek parça — sub-terms: **baskı kafası, damper, kapak (cap), kablo, encoder film, filtre, hortum, kayış, motor, plotter bıçağı** | Troy Makine's spare-parts taxonomy; head brands listed: Epson, Konica, Kyocera, Ricoh, Starfire, Toshiba |
| Colour selector | **Mürekkep Rengi** — options `Lak, C, M, Y, K, LC, LM, W` | Printec; note **"Lak"** is the Turkish trade word for varnish/clear |
| Volume selector | **Şişe Boyutu** — `500 ml`, `1 Litre` | Printec |
| Price | always `+ KDV` | |
| Product tabs | `Açıklama` / `Ek bilgi` / `Yorumlar` | WooCommerce default — avoid the third |

→ **Decision: use "Mürekkepler" as the canonical nav label (professional), but make "boya" a search
synonym** so `/tr/urunler?q=uv+boya` resolves. Same for `kafa` → printhead, `sarf` → consumables.

---

## 8. Concrete recommendations for our build

### 8.1 Content model (`content/products/inks/*.json`)
```jsonc
{
  "slug": "maven-uv-led-mk",
  "type": "ink",
  "family": "uv-led",                    // enum, drives family landing page + colour token
  "series": "MAVEN UV-LED MK",
  "tagline": { "tr": "Mimaki UV LED yazıcılar için", "en": "For Mimaki UV LED printers" },
  "oemEquivalent": ["Mimaki LUS-120"],
  "changeover": "switch-and-print",      // switch-and-print | switch-and-swap | switch-and-match
  "channels": [
    { "code": "C",  "name": {"tr":"Camgöbeği","en":"Cyan"},  "sku": "MV-UVMK-C", "availability": "stock" },
    { "code": "W",  "name": {"tr":"Beyaz","en":"White"},     "sku": "MV-UVMK-W", "availability": "stock" },
    { "code": "Cl", "name": {"tr":"Lak","en":"Varnish"},     "sku": "MV-UVMK-CL","availability": "on-request" }
  ],
  "packaging": [
    { "format": "bottle", "volume": 1,   "unit": "L"  },
    { "format": "bag",    "volume": 600, "unit": "ml" }
  ],
  "compat": {
    "printheads": ["Ricoh Gen5"],
    "dropSizePl": [5, 50],
    "printers": ["Mimaki JFX200", "Mimaki JFX500", "Mimaki UJF-7151"],
    "chipIncluded": true
  },
  "specs": {
    "cure":        { "method": "uv-led", "wavelengthNm": 395, "postCureHours": 24 },
    "shelfLifeMonths": 12,
    "storageTempC": [15, 25],
    "operatingTempC": [18, 27],
    "operatingHumidityPct": [40, 60],
    "outdoorDurabilityMonths": 24,
    "outdoorDurabilityNote": { "tr": "dikey maruziyet, Orta Avrupa iklimi", "en": "vertical exposure, central European climate" }
  },
  "substrates": ["akrilik (PMMA)", "sert PVC", "alüminyum kompozit", "polikarbonat", "PVC branda", "folyo"],
  "applications": ["indoor-signage", "outdoor-signage", "pop-display"],
  "certifications": ["greenguard-gold"],
  "documents": [
    { "kind": "tds", "lang": "en", "file": "/docs/tds/maven-uv-led-mk-v1.0-en.pdf", "version": "v1.0", "date": "2026-03" },
    { "kind": "gbf", "lang": "tr", "file": "/docs/gbf/maven-uv-led-mk-gbf-tr.pdf",  "version": "2026-01" }
  ],
  "relatedMachines": ["maven-uv-flatbed-2513"],
  "ancillaries": ["maven-uv-flush", "maven-primer-p2"]
}
```
Note every human-facing string is `{tr, en}` and every enum is a stable slug resolved through a
locale dictionary — that is what makes adding a third locale a data job, not a rebuild.

### 8.2 Catalogue IA
```
/tr/urunler                     → both machines and inks, two big entry cards
/tr/urunler/makineler/[slug]
/tr/urunler/murekkepler                       → family grid (7 families)
/tr/urunler/murekkepler/[family]              → uv-led, eco-solvent, sublimasyon, dtf, lateks, tekstil, su-bazli
/tr/urunler/murekkepler/[family]/[slug]       → product detail
/tr/urunler/sarf-malzemeler                   → film, powder, cleaning fluid, primer, capping fluid
/tr/urunler/yedek-parca                       → printheads, dampers, caps, filters, belts
/tr/uyumluluk                                 → the machine × ink cross-reference table
/tr/belgeler                                  → TDS / GBF hub
```
Filters on the family pages, mirroring Nazdar + INXJet: **Kimya (family) · Marka/Makine · Baskı kafası
· Ambalaj · Uygulama**, each with a live count, plus a compare checkbox. All client-side over a
prebuilt JSON index — no backend needed.

### 8.3 Page composition for an ink detail page
Hero (name + tagline + family colour accent + changeover badge) → gallery → positioning paragraph →
feature bullets → **channel strip** (actual colour swatches per channel, W and Lak rendered as
outlined/hatched chips, `on-request` greyed) → packaging chips → compatibility block (three columns:
Baskı kafaları / Makineler / OEM eşdeğeri) → spec table → substrates → cure & durability →
ancillaries carousel → documents list → disclaimer → quote CTA → related machine card.

The **channel strip is the visual signature move** for this site: nothing in the competitor set
renders the colour set graphically, and it ties straight back to the CMYK pixel cluster in the Maven
logo. Reuse the exact cyan/magenta/yellow tokens from the mark.

### 8.4 Authoring sample data credibly
Use these anchors so the fake SKUs read as real:
- Shelf life: **12 months** for everything except sublimation (**15**) and DTF white (**6**).
- Storage: **18–27 °C** (UV/solvent), **15–25 °C dark** (UV-LED), **< 25 °C** (sublimation).
- Operating environment: **18–27 °C**, humidity optimum **40–60 %** non-condensing.
- UV cure: **225–300 mJ/cm²** at **600 mW/cm²** for mercury; **395 nm** for LED.
- Outdoor durability: **24 months vertical exposure** — always with the scoping clause.
- Sublimation transfer: **180–220 °C**, 30–180 s; classes A/B/C/D = 180/190/200/210 °C.
- DTF: viscosity **4.0 cps ± 0.5 @ 25 °C**, surface tension **30 ± 3 dyn/cm**, pH **9.0 ± 0.5**.
- DTF powder grades: **0–80 µm / 80–170 µm / 120–250 µm**, melt ~110 °C, cure 150–160 °C.
- Textile pigment fixation: **160 °C for 60–90 s**, wash fastness ISO 105-C06 ≥ 4.

### 8.5 Anti-patterns (all observed in the wild — do not copy)
- Publishing viscosity/pH for UV or solvent inks (real UV TDS don't; it reads as copy-paste).
- An unscoped "5 years outdoor" claim. Every credible source scopes it: *vertical exposure, named
  climate, statically mounted, proper colour management*.
- A "GREENGUARD" badge on a dealer's own logo lockup.
- Reviews/star ratings on an industrial ink page.
- Prices with `+ KDV` next to a wrong chemistry description.
- Hiding the TDS behind a reseller login (Bordeaux does this and it's a dead end for SEO and trust);
  gate nothing that a print shop needs to decide.

---

## Sources

1. https://c-m-y-k.com/products/ — Bordeaux family + printer-brand taxonomy
2. https://c-m-y-k.com/products/uv-uv-led-curable-inks/ — PLASMA line-up
3. https://c-m-y-k.com/product/plasma-led-mk/ — colours, packaging, printers, substrates, tabs
4. https://c-m-y-k.com/product/plasma-led-mk120/ — Mix & Match™, Printer specific™, "Get a Quote"
5. https://c-m-y-k.com/products/eco-solvent-inks/ — FUZE ECO per-printer naming
6. https://c-m-y-k.com/product/fuze-eco-trv2/ — reseller-login gating
7. https://c-m-y-k.com/products/latex-based-ink/ — EDEN LX792 / LX831 OEM-number naming
8. https://www.nazdar.com/en-us/digital-inks — Chemistry / Application / Printer-Compatibility IA
9. https://www.nazdar.com/en-us/DIGITAL-INKS-Inks-By-Chemistry-Eco-Solvent-Inks — facets with counts, compare, grid/list
10. https://www.nazdar.com/en-us/P/4399/203-Series-Digital-Ink — 3-tab product page, SDS route, disclaimer
11. https://www.martin-supply.com/images/pdf/VENDOR%20TECH%20DATA%20SHEETS/621635-621642%20NAZDAR_730_Series_UV_Inkjet.pdf — full Nazdar 730 TDS (cure dose, 1/5/8 L, item numbers, primer matrix)
12. https://www.kiiandigital.com/gallery/99/DIGISTAR_HI-PRO__E_.pdf — Kiian TDS Feb 2025 (codes, 15 mo, fastness, sublimation classes)
13. https://www.kiiandigital.com/en/ink/products/ — sublimation / pigments / reactive / dispersed facets
14. https://www.marabu-northamerica.com/fileadmin/marabu-druckfarben/PDFs/Technical_Data_Sheets/TDS_EN_DLE-JX_0123.pdf — Marabu Ultra Jet DLE-JX TDS, Switch & Print/Swap/Match
15. https://www.sunchemical.com/product/streamline/ — Streamline sub-products, GREENGUARD Gold, printheads
16. https://www.inktec-europe.com/inks/ — Solvent/Aqueous/Sublimation/DTF/UV/Latex + DTF powder + bulk system
17. https://www.inktec-europe.com/inks/uv-inks/uv-inks-for-led-uv-printers-with-epson-printheads/ — SE Series codes, 1 L + chips, TDS + ECO PASSPORT downloads
18. https://www.inktec-europe.com/news/jetrix-inks-achieve-greenguard-gold-certification/ — JETRIX ULE/ULS GREENGUARD Gold
19. https://www.inxjetdigital.com/ + https://www.inxjetdigital.com/packaging/1-lt-bottle — Advanced Product Selector, full packaging enum, pL facet
20. https://www.triangleinx.com/arguments/uv-ink-storage-and-shelf-life — 12 months, 15–30 °C
21. https://www.ul.com/resources/ul-greenguard-certification-program + https://kmbs.konicaminolta.us/blog/greenguard-gold-certification/ — UL 2818, >360 VOCs, TVOC 0.22 mg/m³, CDPH 01350
22. https://law.resource.org/pub/eu/toys/en.71.3.2015.html — EN 71-3 migration of certain elements
23. https://www.chemleg.com/makaleler/guvenlik-bilgi-formunda-bulunmasi-gereken-bilgiler — 16 GBF sections in Turkish, KDU requirement
24. https://msds.com.tr/kkdik-ve-gbf-yonetmeligi/ — KKDİK + SEA, Turkish-language obligation, 31 Dec 2023 KDU rule
25. https://troymakine.com/ — Turkish dealer IA (Makineler / Boyalar / Yedek Parçalar / 2. El), spare-part taxonomy
26. https://www.gurdijital.com/urun-kategori/eco-solvent-baski-murekkebi — "Dijital Baskı Boyaları", "Ürünü incele / Bize Ulaşın"
27. https://www.printec-online.com/urun/printec-uv-murekkebi/ — "Mürekkep Rengi" / "Şişe Boyutu" option labels, + KDV
28. https://www.stsinks.com/product/direct-to-film-ink-1-liter-pouch-of-cmyk — DTF 1 L CMYK / 900 ml White
29. https://www.hp.com/emea_africa-en/products/ink-toner/product-details/product-specifications/5708878 — HP Latex 775 ml / 3 L, Optimizer
