# Track 5 — Realistic Machine Specifications

Research basis for the Maven sample catalogue. Every number below was pulled from a live vendor or
distributor page in **July 2026**. Where a figure could not be confirmed against a primary source it
is marked **⚠ UNVERIFIED** — do not publish those as hard specs without re-checking.

**How to read this:** each family section ends with a *"Plausible sample machine"* block. Those are
the numbers to transcribe into `content/products/*.json`. They sit inside the real ranges documented
above them, so a trade professional reading the site will not flinch.

---

## 0. Canonical spec schema (use these keys in product JSON)

Turkish labels below are taken verbatim from live Turkish dealer sites (Lazerpol, Meka Dijital, Pass
Dijital) so the site's vocabulary matches what a Turkish buyer already reads elsewhere.
Sources: [lazerpol.com](https://lazerpol.com/urun/uv-130x130-flatbed-printer/),
[mekadijital.com](https://www.mekadijital.com/urun-kategori/dijital-baski-makineleri/uv-dijital-baski-makineleri/),
[passdijital.com](https://www.passdijital.com/ekosolvent-baski-makineleri)

| JSON key | TR label | EN label | Example value | Notes |
|---|---|---|---|---|
| `printArea` | Baskı Alanı | Print Area | `2500 × 1300 mm` | flatbeds |
| `printWidth` | Baskı Genişliği | Print Width | `1610 mm` | roll machines |
| `mediaHeight` | Baskı Yüksekliği | Max Media Height | `100 mm` | flatbeds — vendors say "print height" |
| `mediaWeight` | Medya Ağırlığı | Max Media Weight | `< 50 kg/m²` | Mimaki phrasing |
| `printHead` | Baskı Kafası | Print Head | `3 × Epson i3200-U1` | count first, then model |
| `headCount` | Kafa Sayısı | Head Count | `3` | separate numeric key for filtering |
| `colors` | Renkler | Ink Channels | `CMYK + W + V` | V = varnish/vernik |
| `speedModes[]` | Baskı Hızı | Print Speed | `[{pass:4, value:60, unit:"m²/h"}]` | array; never a single number |
| `resolution` | Çözünürlük | Resolution | `726 × 2400 dpi` | |
| `curing` | Kurutma | Curing / Drying | `4 × LED UV` | UV families |
| `table` | Tabla | Table | `Bölgesel vakumlu alüminyum tabla` | flatbeds |
| `inkType` | Boya / Mürekkep | Ink Type | `UV Mürekkep` | |
| `inkCapacity` | Boya Kapasitesi | Ink Capacity | `Her renk için 3000 ml` | |
| `inkConsumption` | Boya Tüketimi | Ink Consumption | `Metrekarede 10–30 ml` | |
| `power` | Güç Tüketimi | Power Consumption | `3800 W` | |
| `powerSupply` | Güç Kaynağı | Power Supply | `220 V, 50/60 Hz` | |
| `environment` | Çalışma Ortamı | Operating Environment | `20–28 °C / 40–60 % RH` | |
| `rip` | RIP Yazılımı | RIP Software | `Photoprint` | |
| `dimensions` | Makine Ölçüleri | Dimensions | `4700 × 2100 × 1400 mm` | |
| `weight` | Ağırlık | Weight | `1510 kg` | |
| `fileFormats` | Uygulanabilir Formatlar | Supported Formats | `TIFF/JPG/EPS/PDF/PSD/AI` | |

**Design consequence:** `speedModes` must be an array. Every serious vendor publishes speed as a
3-row table (4-pass / 6-pass / 8-pass), never as one number. A single "speed" field on the product
page is the #1 tell of a fake catalogue.

---

## 1. Print head reference (the spec that drives everything else)

| Head | Nozzles | Native / effective | Swathe per head | Drop volume | Max freq | Ink types | Source |
|---|---|---|---|---|---|---|---|
| **Ricoh Gen5** (MH5420 / MH5421 / MH5421F) | 1,280 (4 × 320) | 4 × 150 npi → 600 npi, pitch 0.1693 mm | 54.1 mm (2.1") | 7–35 pl greyscale | up to 60 kHz | UV, solvent, aqueous | [allprintheads](https://www.allprintheads.com/products/ricoh-gen5-printhead-mh5421f), [digiprint-supplies](https://us.digiprint-supplies.com/en/ricoh-gen5-printhead-mh5421f) |
| **Ricoh Gen6** (MH5320 / MH5340) | 1,280 (4 × 320) | 600 npi, pitch 0.1693 mm | 54.1 mm (2.1") | 5 pl binary / 5–15 pl greyscale | 50 kHz greyscale | UV, solvent, aqueous | [allprintheads](https://www.allprintheads.com/products/ricoh-mh5320-gen6-printhead-cable-248mm-j352-04), [icolorpro](https://www.icolorpro.com/products/ricoh-gen6-mh5320-mh5340-printhead) |
| **Konica KM1024i** | 1,024 (4 × 256) | 360 npi (4 × 90 npi) | 72 mm | 6 / 13 / 30 pl by variant, 8 grey levels | SHE 56 kHz · MHE-D 45 kHz · SAE-C 43 kHz · LHE-30 27 kHz | UV, solvent, oil; water only on SAE-C/MAE-C | [konicaminolta.com spec](https://www.konicaminolta.com/global-en/inkjethead/products/inkjethead/km1024i/spec.html) |
| **Kyocera KJ4B-QA** | 2,656 | 600 dpi, pitch 0.042 mm | 108.25 mm | 5 / 7 / 12 / 18 pl | 30 kHz | water-based | [allprintheads](https://www.allprintheads.com/products/kyocera-water-printhead-kj4b-qa), [thermalprintheadstore](https://thermalprintheadstore.com/en/home/205-new-kyocera-kj4b-qa-printhead-water-based-600-dpi-frequency-30khz-for-xerox-printer.html) |
| **Epson i3200** (-U1 UV / -E1 eco-solvent / -A1 aqueous) | 3,200 (8 × 400) | 600 dpi native | 33.8 mm (1.33") | min 2.5 pl (VSDT) | up to 43 kHz | one variant per ink chemistry | [johopetech](https://johopetech.com/print-basics/analysis-of-epson-i3200-printheads-a1-e1-u1/), [subli-star](https://www.subli-star.com/uv-printer/uv-flatbed-printer-star-v-6090/) |
| **Toshiba CE4 / CE4M** | 636 | 84.5 µm pitch (≈300 npi) | 53.7 mm | 5–35 pl, 16 grey levels | ⚠ not published | UV curable, oil | [icolorpro](https://www.icolorpro.shop/products/toshiba-ce4m-printhead), [digiprint-usa](https://digiprint-usa.com/products/toshiba-ce4m-printhead) |

### How head COUNT maps to speed — the real relationship

This is the single most useful thing in this document. DOCAN publishes the same machine with three
different head brands and head counts, which lets us derive the actual scaling law
([docanuv.com](https://www.docanuv.com/printers/printers)):

| Machine | Head | Head count range | 4-pass m²/h | 6-pass m²/h | 8-pass m²/h |
|---|---|---|---|---|---|
| DOCAN H1216 (1.2 × 1.54 m flatbed) | Ricoh G6 5pl | 2–4 | 22–28 | 16–22 | 14–16 |
| DOCAN H1216 | Epson i3200 | 3 rows | 15 | 12 | 9 |
| DOCAN H1000 (2.5 × 1.25 m flatbed) | Ricoh G6 5pl | 2–12 | 50–60 | 36–42 | 27–30 |
| DOCAN H1000 | Konica 1024A 6pl | 4–12 | 33–40 | 30–36 | 24–28 |
| DOCAN H1000 | Epson T3200 | 2–4 | 48 | 38 | 28 |
| DOCAN H3000 (3.2 × 2.0 m flatbed) | Konica 1024A 6pl | 4–18 | 75–84 | 47–54 (8-pass) | — |
| DOCAN H3000 | Ricoh G6 5pl | 2–16 | 60–72 | — | 36–42 |
| DOCAN H3000 | Kyocera 3.5pl | 2–10 | 60 | — | 34 |
| DOCAN FR3210 (3.2 m hybrid) | Ricoh G6 | 2–20 | 92–111 | 61–74 | 41–49 |
| DOCAN FR3210 | Konica 1024A | 4–28 | 116–141 | 79–94 | 41–49 |
| DOCAN FR3210 | Kyocera | 2–10 | 94 | 63 | 47 |
| DOCAN R5200 (5.1 m roll) | Konica 1024A | 4–28 | 100–124 | 72–84 | 52–64 |
| DOCAN R5200 | Kyocera | 2–14 | 88–100 | 72–85 | 50–65 |

**Rules that fall out of this data — apply them when inventing numbers:**

1. **Doubling passes roughly halves speed, but not exactly.** 4→6 pass ≈ ×0.68; 6→8 pass ≈ ×0.72.
   4→8 pass ≈ ×0.49. Never make 8-pass exactly half of 4-pass; it looks synthetic.
2. **Konica 1024A is the speed head, Ricoh G6 the quality head, Kyocera the precision head.**
   On the same chassis Konica ≈ +25 % over Ricoh at 4-pass, but the gap collapses at 8-pass
   (FR3210: 116–141 vs 92–111 at 4-pass; both 41–49 at 8-pass).
3. **Speed range within one model = min-to-max head count.** H3000 Ricoh 60–72 m²/h at 4-pass spans
   the 2→16 head range. So publish a *range* for configurable machines and a *single value* for
   fixed-configuration machines (Mimaki, Roland, Epson).
4. **Adding white kills ~35–40 % of throughput.** Mimaki UCJV330-160: 28 m²/h 4-colour → 18 m²/h with
   white and/or clear ([mimakieurope](https://www.mimakieurope.com/products/uv/ucjv330-160/)).
   DOCAN FR1800: 45 m²/h full colour → 13 m²/h in Colour-White-Colour (CWC is 3 layers, so worse).
5. **Epson i3200 chassis are always slower than Ricoh/Konica industrial chassis at equal head count.**
   H1216: i3200 15 m²/h vs Ricoh G6 22–28 m²/h at 4-pass.

---

## 2. Family — UV Flatbed

### 2.1 Small format (~A3 to 60 × 90 cm) — promo / hobby / personalisation tier

| Spec | Sublistar UV-6090F "Star-V" | Mimaki UJF-3042MkII e | Mimaki UJF-6042MkII e | Roland VersaUV LEF2-200 | Roland VersaUV LEF2-300D |
|---|---|---|---|---|---|
| Print area | 600 × 900 mm | 297 × 420 mm (A3) | 610 × 420 mm (A2) | 508 × 330 mm | 770 × 330 mm |
| Max media size | — | — | — | 538 mm wide | 800 mm wide |
| Max media height | **180 mm** | 153 mm | 153 mm | 100 mm | **200 mm** (spacer table 0–100 mm) |
| Max media weight | — | — | 8 kg | 5 kg | 8 kg (2 kg with spacer) |
| Heads | 3 × i1600-U1 **or** 3 × i3200-U1 | on-demand piezo, staggered | 4 × on-demand piezo, staggered | piezo | piezo |
| Speed | 2–5 m²/h (i1600) · 2.5–8 m²/h (i3200) | ≈ 2.48 m²/h max · ≈38 A4/h | ≈ 52 A4/h | +60 % vs LEF-200 (bidirectional) | +60 % vs LEF-300 |
| Resolution | up to 720 × 2400 dpi | up to 1200 × 1200 dpi | up to 1200 × 1200 dpi | up to 1440 dpi | up to 1440 dpi |
| Ink channels | CMYK+W / CMYK+W+V | LH-100 / LUS-120 (CMYK+Lc+Lm+W+Cl), LUS-150, PR-200 primer | same | CMYK+W+Gloss, or CMYK+W+W | CMYK+W+Gloss, or CMYK+W+W |
| Ink supply | bulk tank | 250 ml / 1 L bottles | 250 ml / 1 L bottles | 220 cc cartridge (500 cc except white) | 220 cc / 500 cc |
| Power | AC 220/110 V ±10 %, 50/60 Hz | — | AC 100–240 V, ≤ 1000 W | 149 W | 178 W |
| Dimensions | 1696 × 1595 × 719 mm | — | 1665 × 1290 × 856 mm | 1202 × 962 × 549 mm | 1560 × 955 × 676 mm |
| Weight | 194 kg | — | 150 kg | 110 kg | 166 kg |
| Environment | 16–38 °C, 35–65 % RH | — | 20–30 °C (rec. 20–25), 35–65 % RH | 20–32 °C, 35–80 % RH | 20–32 °C, 35–80 % RH |
| RIP | MainTop, FlexiPRINT, CADlink | RasterLink7 (bundled) | RasterLink7 (bundled) | VersaWorks 6 (bundled) | VersaWorks 6 (bundled) |

Sources: [subli-star](https://www.subli-star.com/uv-printer/uv-flatbed-printer-star-v-6090/),
[mimaki UJF-6042MkII spec](https://mimaki.com/product/inkjet/i-flat/ujf-6042mkII/specification.html),
[mimaki UJF-3042MkII e spec](https://mimaki.com/product/inkjet/i-flat/ujf-3042mkII-e/specification.html),
[rolanddg.eu LEF2 specs](https://www.rolanddg.eu/en/products/printers/versaobject-lef2-series-benchtop-uv-flatbed-printer/specifications-accessories)

**Turkish-market reference machine** (Lazerpol, İstanbul) — useful because it shows the exact spec
fields Turkish buyers see: 3 × EPSON i3200-U1 · CMYK+W+V · *Bölgesel vakumlu alüminyum tabla* ·
*4 adet LED UV ışık* · Güç 3800 W · 220 V 50/60 Hz · 20–28 °C / 40–60 RH · boya kapasitesi
**3000 ml per colour** · boya tüketimi **10–30 ml/m²** · RIP Photoprint.
([lazerpol.com](https://lazerpol.com/urun/uv-130x130-flatbed-printer/) — note their listed
"Baskı Alanı 130×130 mm" is a typo for 1300 × 1300 mm; **⚠** don't copy that field.)

### 2.2 Mid format (~1.2 × 1.6 m)

| Spec | DOCAN H1216 |
|---|---|
| Print area | 1200 × 1540 mm |
| Max media height | 100 mm |
| Heads | Ricoh G6 (5 pl) / Ricoh G5s (3.5 pl) / Epson i3200 / Kyocera — **2–4 pcs** |
| Speed | Ricoh G6: 22–28 (4p) · 16–22 (6p) · 14–16 (8p) m²/h — Epson i3200: 15 / 12 / 9 m²/h |
| Resolution | up to 726 × 1200 dpi |
| Ink channels | CMYK / Lc / Lm + W |
| Ink tank | 2 L |
| Curing | UV LED |
| Power | AC 220 V 50/60 Hz, 10 kW, 45 A |
| Dimensions / weight | 3000 × 2300 × 1350 mm · 720 kg |
| Environment | 20–28 °C, 40–60 % RH |
| RIP | SAi / ONYX / Caldera |

Source: [docanuv.com/printers/flatbed/H1216](https://www.docanuv.com/printers/flatbed/H1216)

### 2.3 Large / industrial (2.5 × 1.3 m and up)

| Spec | Mimaki JFX200-2513 EX | Mimaki JFX600-2513 | DOCAN H1000 | DOCAN H3000 | Epson SC-V7000 | HandTop HT2500UV |
|---|---|---|---|---|---|---|
| Print area | 2500 × 1300 mm | 2500 × 1300 mm | 2500 × 1250 mm | 3200 × 2000 mm | 2500 × 1250 mm | 2500 × 3000 mm+ |
| Heads | 3 × piezo, staggered | **16 × piezo**, 320 nozzles × 4 rows, staggered 4-in-line | Ricoh G6 2–12 · G5s 2–12 · Konica 1024A 4–12 · Epson T3200 2–4 | Konica 1024A 4–18 · Ricoh G6 2–16 · Kyocera 2–10 | 180 nozzles × 8 lines × 8 heads | Ricoh Gen5 / Kyocera KJ4A |
| Speed | ⚠ per-mode table not published; "ink will not cure faster than draft mode" | **up to 200 m²/h** (4-colour) | G6 50–60 / 36–42 / 27–30 · Konica 33–40 / 30–36 / 24–28 · T3200 48 / 38 / 28 | Konica 75–84 → 47–54 · G6 60–72 → 36–42 · Kyocera 60 → 34 | up to 43.1 m²/h | up to 52 m²/h @ 1200 × 1200 dpi |
| Resolution | 300 / 450 / 600 / 900 / 1200 dpi | 600 / 1200 dpi | up to 726 × 1440 dpi | up to 604 × 2400 dpi | up to 720 × 1440 dpi | up to 1200 × 1200 dpi |
| Max thickness | **50 mm** | **60 mm** | 100 mm (300 mm upgrade) | 100 mm | ~80 mm, auto-detected | 50 mm |
| Max media weight | < 50 kg/m² | < 50 kg/m² | — | — | — | — |
| Vacuum | **2 partitions (X-axis)**, blower adsorption | 2 zones (2513) / **9 zones** (2531) | — | — | multi-zone | **3 zoned sections** |
| Ink | LUS-120/150/211/350, LH-100, PR-200 primer; 1 L + 250 ml bottles | LH-100, LUS-120/150/211; 1 L bottles; white circulation | CMYK/Lc/Lm + W + V; 2 L tank | CMYK/Lc/Lm + W + V | 10-colour UltraChrome UV incl. Red + White + Varnish | white ink recirculation pump |
| Ink configs | — | CMYK · CMYK+W+Cl+Pr · CMYKLcLm+W | — | — | 10-colour | 4–8 colour |
| Power | 1φ AC 200–240 V < 12 A, < 2.88 kVA | **3 × 1φ AC 200–240 V, 24 A, each < 4.8 kVA** | AC 220 V, 10 kW, 45 A | AC 220 V, 10 kW, 45 A | — | — |
| Dimensions | 4400 × 2450 × 1250 mm | 5300 × 2850 × 1700 mm | 4700 × 2100 × 1400 mm | 5600 × 3100 × 1540 mm | — | — |
| Weight | 650 kg | ≈ 1200 kg | 1510 kg | 2580 kg | — | — |
| Environment | 15–30 °C, 35–65 % RH | 20–30 °C (accuracy 20–25 °C), 35–65 % RH, gradient < ±10 °C/h | 20–28 °C, 40–60 % RH | 20–28 °C, 40–60 % RH | — | — |
| Interface | USB 2.0 / Ethernet | **Ethernet 10GBASE-T** | — | — | — | — |
| RIP | RasterLink | — | SAi / ONYX / Caldera | SAi / ONYX / Caldera | — | Caldera profile available |
| Notable | — | MAPS, NRS, bulk ink, Mimaki Circulation Technology, PICT IoT | — | — | auto thickness detection | water-cooled LED curing, media height measurement |

Sources: [JFX200-2513 EX spec](https://mimaki.com/product/inkjet/i-flat/jfx200-2513-ex/specification.html),
[JFX600-2513 spec](https://mimaki.com/product/inkjet/i-flat/jfx600-2513/specification.html),
[mimakiusa JFX600](https://www.mimakiusa.com/products/uv-led-flatbeds/jfx600-2513/),
[DOCAN H1000](https://www.docanuv.com/printers/flatbed/H1000),
[DOCAN H3000](https://www.docanuv.com/printers/flatbed/H3000),
[Epson news SC-V7000](https://news.epson.com/news/surecolor-v7000-uv-flatbed-printer),
[SSE HT2500UV](https://www.sseworldwide.co.uk/product/handtop-ht2500uv-hk4-hybrid-uv-printer/),
[Caldera HandTop Ricoh series](https://helpdesk.caldera.com/hc/en-us/articles/12237256153105-HandTop-Ricoh-series-Overview)

### 2.4 Flatbed hardware features worth naming in copy

Real, verifiable feature names — use these exact terms, they're what dealers list
([mtutech](https://www.mtutech.com/FlatbedUVPrinter1314/Mid-sizeFlatbedUVPrinterMT-UV1314-1296.html),
[andresjet](https://www.andresjet.com/blogs/info/how-do-high-speed-wide-format-uv-flatbed-printers-improve-efficiency)):

- **Zoned vacuum table / bölgesel vakumlu tabla** — 2 zones (Mimaki JFX200/JFX600-2513), 3 zones
  (HandTop HT2500UV), up to 6 zones "A–F" (mid-format Chinese), 9 zones (JFX600-2531).
- **Automatic media height / thickness sensor** — auto-detects up to 100 mm on Chinese industrial;
  Epson V7000 auto-detects to ~80 mm.
- **Print head anti-collision sensor** — carriage halts automatically on contact.
- **Registration pins / kılavuz pimler** — mechanical origin stops on the bed corner for repeat jobs.
- **White ink circulation / recirculation pump** — mandatory on any machine offering white; Mimaki
  calls it *Mimaki Circulation Technology*, HandTop calls it *re-circulation pump*.
- **Water-cooled LED curing** (HandTop) vs air-cooled LED — a genuine differentiator on 24/7 machines.
- **Nozzle Recovery System (NRS)** and **MAPS (Mimaki Advanced Pass System)** — banding mitigation.

**Price bands (family 2)** — see §9.

---

## 3. Family — UV Hybrid / Roll-to-Roll

Hybrid = one chassis that takes both rigid sheets and roll media (with a roll kit). The spec that
distinguishes it from a pure flatbed is **max print height on the rigid side (usually only 10–50 mm,
not 100 mm)** plus roll weight capacity.

| Spec | DOCAN FR1800 (1.8 m) | DOCAN FR3210 (3.2 m) | DOCAN R5200 (5.1 m, roll-only) | Mimaki UCJV330-160 (1.6 m print&cut) |
|---|---|---|---|---|
| Print width | 1800 mm | 3200 mm | 5100 mm | 1610 mm (UCJV330-130 = 1360 mm) |
| Heads | Epson i3200-U1 **× 1–4** (FR1800G = extended carriage) | Ricoh G6 2–20 · Konica 1024A 4–28 · Kyocera 2–10 | Konica 1024A 4–28 · Kyocera 2–14 | 2 × piezo, staggered |
| Speed | 45 m²/h full colour · **13 m²/h Colour-White-Colour** | Ricoh 92–111 / 61–74 / 41–49 · Konica 116–141 / 79–94 / 41–49 · Kyocera 94 / 63 / 47 (4/6/8-pass) | Konica 100–124 / 72–84 / 52–64 · Kyocera 88–100 / 72–85 / 50–65 | **28 m²/h** 4-colour · **18 m²/h** with white and/or clear |
| Resolution | 726 × 900 dpi | 726 × 2400 dpi | 726 × 2400 dpi | Y 600/1200 dpi · X 600/1200/1800 dpi |
| Max print height (rigid) | 10 mm | — | 20 mm | media thickness ≤ 1 mm (roll only) |
| Roll capacity | — | heavy-duty option **1–2 t/roll** | — | 1 roll ≤ 45 kg, φ ≤ 250 mm, 2"/3" core |
| Ink channels | CMYK + W (+ fluorescent option) | CMYK + Lc + Lm + W | CMYK / Lc / Lm + W | LUS-170 / 175 / 190 / 200 / 210; CMYK + Lc/Lm/W/Cl |
| Ink supply | 1.5 L tank | 5 L tank | 5 L tank | 1 L bottle |
| Cutting | — | — | — | integrated: max **300 mm/s**, pressure **10–450 gf** |
| Curing | UV LED | UV LED | UV LED | UV LED |
| Power | AC 220 V 50/60 Hz, **4 kW, 20 A** | AC 220 V 50/60 Hz, **15 kW, 70 A** | AC 220 V 50/60 Hz, 10 kW, 45 A | 1φ 100–120 / 200–240 V, max 1440 W |
| Dimensions | 3450 × 1000 × 1500 mm | 5950 × 1700 × 1600 mm | 8150 × 2000 × 1950 mm | 2890 × 800 × 1480 mm |
| Weight | 500 kg | 2985 kg | 6435 kg | 227 kg (130 model: 217 kg) |
| Environment | 20–28 °C, 40–60 % RH | 20–28 °C, 40–60 % RH | 20–28 °C, 40–60 % RH | 20–30 °C (rec. 20–25), 35–65 % RH |
| RIP | SAi / ONYX / Caldera | SAi / ONYX / Caldera | SAi / ONYX / Caldera | RasterLink |
| Formats | TIFF, JPEG, EPS, PDF | — | — | — |

Sources: [DOCAN FR1800](https://www.docanuv.com/printers/hybrid/FR1800),
[DOCAN FR3210](https://www.docanuv.com/printers/hybrid/FR3210),
[DOCAN R5200](https://www.docanuv.com/printers/roll_to_roll/R5200),
[Mimaki UCJV330 spec](https://mimaki.com/product/inkjet/print-cut/ucjv330-series/specification.html),
[mimakieurope UCJV330-160](https://www.mimakieurope.com/products/uv/ucjv330-160/)

**DOCAN's full hybrid/roll line-up for width tiers** (useful for naming our own model ladder):
hybrid FR1800 (1.8 m) → FR2010 (2.1 m) → C3200 / FR3210 (3.2 m) → FR5000 (5.2 m);
roll-to-roll FR2006 (2.05 m, C-W-C) → U3300 / FR3200 / R3200 / RD3200 (3.2 m, RD3200 = dual-side
simultaneous) → R5200 / U5300 (5.1–5.2 m) → FR6606 (6.6 m).
([docanuv.com/printers/printers](https://www.docanuv.com/printers/printers))

---

## 4. Family — Eco-solvent roll printer & print-and-cut

| Spec | Mimaki JV330-160 | Mimaki CJV330-160 (print & cut) | Roland TrueVIS VG3-640 | Epson SC-S60600 | Epson SC-S80600 | Chinese 1.8 m 4 × i3200-E1 |
|---|---|---|---|---|---|---|
| Media width | ≤ 1610 mm (130: 1360) | ≤ 1610 mm | 1625 mm cut width | 1626 mm | 1626 mm | 1800–1820 mm |
| Heads | 2 × staggered piezo, **6400 nozzles**, min 3 pl | same | piezo | PrecisionCore | PrecisionCore | 4 × Epson i3200-E1 |
| Speed | **up to 100 m²/h** (4-colour) | ≈ 100 m²/h (1076.4 sq ft/h) | max 327 sq ft/h ≈ **30.4 m²/h** | draft 1020 sq ft/h (94.8 m²/h) banner; production 550 (51.1) banner / 310 (28.8) vinyl; quality 310 (28.8) / 190 (17.7) | draft 1020 (94.8); production 290 (26.9) banner / 310 (28.8) vinyl; quality 195 (18.1) / 142 (13.2) | production **79 m²/h**, standard **54 m²/h** |
| Resolution | 600 / 800 / 900 / 1200 dpi | 600 / 800 / 900 / 1200 dpi | — | 1440×1440 / 1440×720 / 720×720 / 720×360 dpi | same | up to 2400 dpi |
| Ink | SS21 & SS22 (C,M,Y,K,Lc,Lm,Lk,**Or**,W) · BS4 (CMYK) | same | TR2, GREENGUARD Gold, 8 configs incl. Orange | UltraChrome GS3, 4-colour bulk | UltraChrome GS3, 9-colour + White or Metallic Silver | eco-solvent CMYK |
| Ink pack | SS21 2 L (W 500 ml) · SS22 1 L (W 500 ml) · BS4 2 L | same | pouch | bulk pack | bulk pack | bulk tank |
| Roll handling | 1 roll ≤ 45 kg / 3 rolls ≤ 90 kg total, φ ≤ 250 mm, 2"/3" core, media ≤ 1 mm; **3-roll changer + XY slitter** | same | — | — | — | unwinder + take-up |
| Heating | **tri-zone heater** | tri-zone heater | media heating system | — | — | 3-stage heating (pre / platen / post) |
| Cutting | — | max 300 mm/s, 10–450 gf, repeatability ±0.2 mm | ⚠ blade force listed as "2500 gf max instantaneous" by one reseller — treat as unverified; Roland's normal range is 30–500 gf | — | — | — |
| Power | 1φ AC 100–120 / 200–240 V, max 1440 W × 2 | same | — | — | — | — |
| Dimensions | 3170 × 1215 × 1305 mm | 3170 × 1215 × 1305 mm | — | — | — | — |
| Weight | 368 kg (130: 358 kg) | 373 kg (130: 363 kg) | — | — | — | — |
| Environment | 20–30 °C, 35–65 % RH | 20–30 °C, 35–65 % RH | — | — | — | — |
| RIP | RasterLink | RasterLink | VersaWorks 6 | — | — | Maintop, PhotoPrint, ONYX |

Sources: [Mimaki JV330 spec](https://mimaki.com/product/inkjet/i-roll/jv330-series/specification.html),
[Mimaki CJV330 spec](https://mimaki.com/product/inkjet/print-cut/cjv330-series/specification.html),
[Mimaki JV330/CJV330 launch release](https://mimaki.com/news/product/entry-393116.html),
[mclogan JV330](https://mclogan.com/products/mimaki-jv330-series-eco-solvent-printer),
[Epson S80600](https://epson.com/For-Work/Printers/Large-Format/Epson-SureColor-S80600-Printer/p/SCS80600PE),
[Epson S60600](https://www.equipmentzone.com/epson/s60600/index.php),
[uscutter VG3-640](https://uscutter.com/truevis-vg3-640-large-format-inkjet-printer-cutter/),
[grando-dg 1.8 m 4-head](http://www.grando-dg.com/1-8m-Eco-Solvent-Printer-With-Four-I3200-E1-Print-Heads-pd49907305.html)

**Turkish eco-solvent width ladder** actually sold in Turkey (Pass Dijital / Wit-Color "Ultra i3200"):
1.6 m (1701/1702) → 1.8 m (1902/1904) → 2.2 m (2401/2402) → 3.2 m (3302/3304) → 5.2 m (5308/5512).
The model-number suffix encodes head count — mirror that convention in our SKUs.
([passdijital.com](https://www.passdijital.com/ekosolvent-baski-makineleri))

---

## 5. Family — DTF (Direct-to-Film) printer + shaker/powder unit

DTF is always sold as a **system**: printer + powder shaker + oven (+ fume filter). Sell it that way
on the site; a DTF printer page without a shaker spec block reads as amateur.

### 5.1 60 cm (24") class — the volume seller

| Spec | LINKO S60 Pro (all-in-one) | Audley 2-head | Audley 4-head | PO-TRY 5-head |
|---|---|---|---|---|
| Heads | 2 × Epson i1600-A1 (i3200-A1 variants exist) | 2 × i3200-A1 | 4 × i3200-A1 | 5 × i3200-A1 |
| Print width | 620 mm (24") | 60 cm | 60 cm | 60 cm |
| Speed | **4-pass 12 m²/h · 6-pass 8 m²/h · 8-pass 6 m²/h** | ≈ 6–8 m²/h ⚠ | ≈ 13–18 m²/h ⚠ | — |
| Resolution | 720 × 2400 dpi (8-pass) | — | — | — |
| Ink channels | CMYK + W (5-channel, separate white) | CMYK+W | CMYK+W | CMYK+W (+ fluorescent options exist) |
| Ink supply | **2 L bulk ink pot** | bulk | bulk | bulk |
| Media | PET film roll | PET film | PET film | PET film |
| Shaker | A1 vertical powder shaker | DF-800(A) | ADL07K12 | — |
| Shaker dims | 1652 × 1066 × 902 mm | — | — | — |
| Shaker power | **220 V, 20 A rated; 2000–5200 W** | — | — | — |
| Shaker weight | ≈ 70 kg | — | — | — |
| Printer dims | 1160 × 610 × 500 mm | — | — | — |
| Operating temp | 20–35 °C (printer and shaker) | — | — | — |
| Power in | AC 110 V ±10 % / AC 220 V ±10 %, 50/60 Hz | — | — | — |
| Interface | RJ45 | — | — | — |
| RIP | **Hemo Driver, Maintop 6.1, PhotoPrint, PrintFactory** | — | — | — |
| Street price | — | **$11,499** | **$17,499** (also $13,999 for a competing 4-head) | — |

### 5.2 30 cm (A3+) class — entry tier

- 2 × Epson XP600, 300 mm width → **≈ 5 m²/h**; typical average 2.5–4 m²/h depending on resolution
  and coverage.
- 2 × Epson i3200-A1, 300 mm → **≈ 4.5 m²/h**.
- Front and rear heaters on the printer; separate 30 cm shaker unit **380 × 200 × 220 mm, 35 kg,
  220 V 50/60 Hz**.
- Consumables that must appear on the product page: **DTF ink CMYK + W (+ Lc/Lm on 6-colour rigs),
  PU hot-melt transfer powder, PET film, two cleaning solutions.**

Sources: [dtflinko S60 Pro](https://www.dtflinko.com/printer-product/s60-pro-all-in-one-dtf-printer/),
[dtflinko B-602](https://www.dtflinko.com/printer-product/dtf-printer-b-602/),
[dtfonestop Audley 2-head](https://www.dtfonestop.com/products/audley-2-printheads-i3200-a1-60cm-dtf-printer),
[dtfonestop Audley 4-head + shaker](https://www.dtfonestop.com/products/audley-4-printheads-i3200-a1-24in-60cm-dtf-printer-with-adl07k12-shaker),
[potryus 5-head](https://potryus.com/products/60cm-24in-5-printheads-dtf-printer),
[printec-online (TR consumables)](https://www.printec-online.com/urun-kategori/transfer-baski-makineleri/dtf-baski-makinesi-ve-sarf-malzemesi/)

---

## 6. Family — Sublimation / dye-sub transfer printer + calender

### 6.1 Printers

| Spec | Mimaki TS55-1800 | Epson SC-F9470 / F9470H | Epson SC-F10070 / F10070H | Sublicool S-1904E (1.9 m Chinese) |
|---|---|---|---|---|
| Max print width | **1940 mm** (media 1950 mm) | 1626 mm (64") | 1930 mm (76") | 1900 mm |
| Heads | staggered head assembly | PrecisionCore | **6 × 4.7" PrecisionCore** | **4 × Epson i3200-A1** |
| Speed | **max 140 m²/h** (1506 sq ft/h) · practical 55 m²/h (592 sq ft/h) · quality 31 m²/h (333 sq ft/h) | — | up to 2635 sq ft/h ≈ **245 m²/h** | **2-pass 180 · 3-pass 120 · 4-pass 90 m²/h** |
| Resolution | 480 / 600 / 1200 dpi | — | — | — |
| Ink | **Sb610**: Bk, M, Y, C, Lbk, Lm, Lc, Fl.Yellow, Fl.Pink — 4 / 6 / 7 / 8-colour configs, 8 slots | UltraChrome DS | UltraChrome DS6 (6-colour on H) | dye-sub CMYK |
| Ink pack | 2 L | — | — | 4 × 3 L reservoir, two-level supply |
| Roll handling | roll ≤ 45 kg; **mini jumbo option: feed 300 kg / φ600 mm, wind 100 kg / φ280 mm** | — | — | take-up with tension sensor bar, **max 1000 m media** |
| Drying | — | — | — | two-stage air-heat integrated dryer, external dryer max **7200 W** |
| Power | 1φ AC 100–120 / 200–240 V; **1.44 kW @100 V / 1.92 kW @200 V** | — | — | 210–230 VAC 50/60 Hz 10 A; print system 1200 W |
| Dimensions | 3240 × 713 × 1857 mm | — | — | 3180 × 1100 × 1700 mm |
| Weight | 202 kg | — | — | — |
| Environment | 20–30 °C, 35–65 % RH | — | — | 18–30 °C, 35–65 % RH |
| Interface | Ethernet 1000BASE-T / USB 2.0 Hi-Speed | — | — | — |
| RIP | TxLink / RasterLink | — | — | **Maintop 6.0, PhotoPrint, ONYX, Wasatch, NeoStampa** |
| Certifications | VCCI, FCC, CE, CB, Energy Star, RCM, EAC | — | — | — |

Sources: [Mimaki TS55-1800 spec](https://mimaki.com/product/inkjet/textile/ts55-1800/specification.html),
[gpisupplies TS55-1800 speeds](https://www.gpisupplies.com/products/mimaki-ts55-1800),
[Epson F10070H news](https://news.epson.com/news/surecolor-f10070h-industrial-six-inks-sublimation),
[Sublicool S-1904E](https://sublicool.com/sublimation-printing-solution/1-9m-sublimation-printer-s-1904e/)

### 6.2 Calenders (rotary heat presses)

| Spec | Easty ERT-H | Sublicool XYG-01 |
|---|---|---|
| Transfer widths | 1.6 m / 1.9 m / 3.1 m | 600 / 800 / 1200 / 1700 / 2000 mm |
| Drum diameter | **420 / 600 / 800 mm** | 420 mm |
| Heating | oil-filled drum, external tank, dual-layer hard-chrome drum | electric, Teflon-coated hot roll |
| Max temperature | ⚠ not published | **0–400 °C** |
| Transfer speed | ⚠ not published | **120–600 cm/h** |
| Heating power | **27.2 – 117 kW** | **18 – 60 kW** |
| Voltage | 3-phase 220 V / 380 V | 110 / 220 / 380 V |
| Dimensions | 2.45–4.07 × 1.98–2.3 × 1.65–2.01 m | 380 × 140–320 × 140–160 cm |
| Net weight | **1300 – 4200 kg** | **900 – 3600 kg** |
| Felt belt | 1650–3350 mm to 3150–5050 mm | breathable conveyor belt |
| Feed / collect | 3 feedings + 3 collecting stations | roll-to-roll |

Sizing rules dealers actually use, worth putting in body copy:
- A 1.8 m printer with 1.7 m paper transfers **1.65 m** of fabric → the **1.8 m drum is the volume
  seller**.
- **Bigger drum = faster line.** A 12" (≈300 mm) drum transfers ≈ 3.9 ft/min at a 35 s dwell. Choose
  a 210 mm drum only for ~35 m runs; choose 800 mm for high-throughput.

Sources: [eastyltd ERT-H](https://eastyltd.com/p/easty-calender-heat-press-roll-to-roll/),
[sublicool XYG-01](https://sublicool.com/heat-press-machine-calender-heat-press-machine-xyg-01/),
[eastyltd sizing guide](https://eastyltd.com/choose-best-heat-transfer-sublimation-heat-press-calender/),
[hbheatpress drum-diameter guide](https://hbheatpress.com/How-to-choose-a-suitable-calander-sublimation-machine-n.html)

---

## 7. Family — UV DTF / crystal label printer

The defining feature is **AB film + integrated laminator**: print colour + white + varnish on A-film,
laminate B-film on top inline, then die-cut and transfer to hard goods.

| Spec | MTuTech MT-UV DTF 30 | MTuTech MT-UV DTF 60 | ORIC OR-A3 (30 cm) | Sublistar A3 30R "Star IV" |
|---|---|---|---|---|
| Print width | 300 mm (12") | 600 mm (24") | 300 mm | 300 mm |
| Heads | 1 × Epson **i3200-U1HD** | 3–4 × Epson i1600-U1 | dual **F1080** (i1600-U1 optional) | Epson i3200-U1HD |
| Speed | **7.2 m²/h** | **8 m²/h** | **4-pass 3.6 m²/h** | 1.6–1.7 m²/h |
| Resolution | up to 1440 dpi | up to 1440 dpi | up to 2400 dpi | — |
| Ink channels | **CMYK + W + Varnish** | GL + CMYK + W + V + GV (9-ch) | CMYK + W + Varnish | CMYK + W + V |
| Ink supply | — | — | colour siphon + **white ink auto-stirring** | — |
| Max media thickness | print height 0–1 mm | 0–2 mm | ≤ 1.5 mm | — |
| Curing | UV LED | UV LED | **dual UV LED** | UV LED |
| Laminator | **integrated automatic** | **integrated automatic** | — | — |
| Power | 220 V | 220 V | **3500 W** | — |
| Dimensions | — | — | 1160 × 730 × 1380 mm (with stand) | — |
| Weight | — | — | 100 kg (with stand) | — |
| Environment | — | — | 15–32 °C, 35–80 % RH | — |
| Running cost | ≈ $17–30/month electricity (26 d × 10 h) | ≈ $32–56/month | — | — |

Sources: [mtutech UV DTF](https://www.mtutech.com/UVDTFPrinter.html),
[ORIC OR-A3](https://www.oricsystems.com/OR-A3-DTF-UV-Crystal-Label-Printer-30cm-pd550043178.html),
[Sublistar A3 30R](https://shop.subli-star.com/products/sublistar-a3-30cm-mini-desktop-uv-dtf-printer-with-i3200-printer-heads-ab-film-crystal-label-printing-machine)

**⚠ Caution:** vendors in this category frequently print "7.2 m/h" (linear metres) and "7.2 m²/h"
interchangeably. Given a 300 mm web, 7.2 m²/h would be 24 linear m/h — plausible; 7.2 linear m/h
would be 2.16 m²/h — also plausible. Pick **3.5–7 m²/h for a 30 cm machine** and state the unit
explicitly. ORIC's 3.6 m²/h at 4-pass is the most internally consistent figure found.

---

## 8. Family — Cutting

### 8.1 Roll-fed vinyl plotters

| Spec | Roland CAMM-1 GS-24 / VersaSTUDIO GS2-24 | Graphtec CE7000-60 |
|---|---|---|
| Max cutting width | **584 mm (22.9")** | **609 mm (24")** |
| Max media loading width | — | **711 mm (28")** |
| Max cutting force | **350 gf** | **450 gf** |
| Max cutting speed | **500 mm/s** | **900 mm/s @ 45°** |
| Series widths | GS-24 only | CE7000-40 / -60 / -130 / -160 |
| Materials | vinyl, paint mask, reflective vinyl | vinyl, HTV, sandblast, reflective |

Sources: [rolanddg.eu GS-24](https://www.rolanddg.eu/products/vinyl-cutters/camm-1-gs-24-desktop-vinyl-cutter/features),
[stahls GS2-24](https://www.stahls.com/vinyl-cutter-roland-gs2-24),
[graphtecgb CE7000](https://graphtecgb.co.uk/graphtec-ce7000-series-cutting-plotter/),
[stahls CE7000-60](https://www.stahls.com/vinyl-plotter-ce7000)

### 8.2 Flatbed digital cutter

| Spec | Summa F1612 |
|---|---|
| Working area | **1600 × 1200 mm** (63" × 47") |
| Max material width | 1650 mm (65") |
| Panelled length | up to ≈ 50 m (164 ft) in multi-panel |
| Max cutting speed | **1000 mm/s** (39 in/s) |
| Acceleration | up to **1 G** |
| Repeatability | **±0.05 mm** |
| Vertical (down) force | up to **200 N** |
| Vacuum zones | **4 (1 row × 4 columns)** |
| Vacuum power | 1.3 kW @50 Hz / 1.75 kW @60 Hz |
| Power | 3 × 400 V + N 50 Hz max 20 A · or 3 × 208 V + N 60 Hz max 30 A · or 3 × 230 V 50 Hz max 20 A (single-phase variant exists) |
| Overall dimensions | 2470 × 2200 × 1100 mm |
| Tool head | multi-module, **up to 3 tools loaded**, single-point fastening |
| Tool modules | tangential knife, kiss-cut, pneumatic oscillating tool, routing, V-cut, creasing |
| Materials | adhesive vinyl, banner, reflective, magnetic, foamboard, cardboard, corrugated, MDF, ACM, textile |
| Options | media-advance clamps, conveyor |

Sources: [summa.com F1612](https://www.summa.com/en-int/cutters/flatbed-cutters/f-series/f1612),
[airmark F1612](https://www.airmark.com/products/summa-f-series-f1612-flatbed-cutter)

---

## 9. Price bands (internal only — never publish)

Use these to pitch the *tone* of the copy. Verified list prices in **bold**; everything else is a
band derived from dealer listings and should be treated as indicative.

| Tier | Machine class | Band (USD) | Evidence |
|---|---|---|---|
| Entry | Desktop A3 UV flatbed (XP600) | $2.8k – $6k | reseller listing at $2,800 |
| Entry | 60 × 90 UV flatbed, 3 × i3200-U1 | $8k – $20k | ⚠ estimated from reseller range |
| Entry | 30 cm UV DTF / crystal label | $6k – $12k | ⚠ vendors quote-only |
| Entry | 30 cm DTF + shaker | $4k – $8k | ⚠ estimated |
| Entry | Vinyl plotter (GS2-24 / CE7000-60) | $1.5k – $3.5k | ⚠ bundle pricing varies |
| Mid | 60 cm DTF + shaker, 2-head i3200 | **$11,499** | dtfonestop (Audley + DF-800A) |
| Mid | 60 cm DTF + shaker, 4-head i3200 | **$13,999 – $17,499** | PO-TRY / Audley + ADL07K12 |
| Mid | Roland LEF2-200 / LEF2-300D benchtop UV | $25k – $50k | ⚠ dealer-quote only |
| Mid | Mimaki UJF-6042MkII e | $45k – $70k | ⚠ dealer-quote only |
| Mid | Eco-solvent 1.6–1.8 m Chinese (i3200-E1) | $6k – $20k | ⚠ estimated |
| Mid | Eco-solvent print&cut (Roland VG3-640 / Mimaki CJV330-160) | $25k – $40k | ⚠ dealer-quote only |
| Mid | Epson SC-S60600 / S80600 | $20k – $30k | ⚠ dealer-quote only |
| Mid | Dye-sub 1.9 m Chinese, 4 × i3200-A1 | $12k – $25k | ⚠ estimated |
| Mid | Calender 1.9 m | $8k – $25k | ⚠ estimated |
| Mid | Epson SureColor F9470 (64" dye-sub) | **$26,995 MSRP** ($21,995 after rebate) | dealer listings |
| Mid | Epson SureColor F9470H | **$32,995 MSRP** | dealer listings |
| Upper-mid | Mid-format UV flatbed 1.2 × 1.6 m (Chinese) | $25k – $50k | ⚠ estimated |
| Upper-mid | Summa F1612 flatbed cutter | **$55,990 – $70,990** new (used ≈ $36k) | wideimageprinters / signs101 |
| Industrial | Epson SureColor V7000 UV flatbed | **$79,999 MSRP** (street $85k–$95k) | Epson / resellers |
| Industrial | 2.5 × 1.3 m Chinese UV flatbed, Ricoh G5/G6 | **$80k – $150k** by configuration | andresjet buyer's guide |
| Industrial | Mimaki JFX200-2513 EX | $120k – $150k | ⚠ estimated |
| Industrial | 3.2 m hybrid, Konica/Ricoh, 8–20 heads | $60k – $180k | ⚠ estimated from head-count scaling |
| Flagship | **Mimaki JFX600-2513** | **$207,900 list** | mimakiusa |
| Flagship | **Mimaki JFX600-2531** | **$269,495 list** | mimakiusa |
| Flagship | Industrial UV overall envelope | $30k – $400k+ | andresjet B2B pricing article |

Sources: [mimakiusa JFX600](https://www.mimakiusa.com/products/uv-led-flatbeds/jfx600-2513/),
[andresjet price range article](https://www.andresjet.com/blogs/knowledge/what-is-the-price-range-for-an-industrial-uv-printer-in-b2b-production),
[allsquare F9470](https://www.allsquare.com/epson-surecolor-f9470-dye-sublimation-inkjet-printer.html),
[wideimageprinters F1612](https://wideimageprinters.com/products/summa-f-series-f1612-flatbed-cutter)

---

## 10. Cross-cutting facts (use these in consumables / service copy)

### Ink consumption & running cost
- **UV ink: 3–15 ml/m² typical**; a Turkish dealer quotes **10–30 ml/m²** for a promo flatbed —
  the higher figure reflects white underbase.
  ([dtflinko](https://www.dtflinko.com/uv-printing-costs-analysis/), [lazerpol](https://lazerpol.com/urun/uv-130x130-flatbed-printer/))
- **UV ink price $28–35/L** at the low end, up to ~$69/L for OEM.
- **1 L covers ≈ 70–100 m²** → **ink cost ≈ $0.30–0.98/m²**; with maintenance consumables
  **$1.19–1.38/m²** total.
- **White ink always costs more per m²** than colour (heavier lay-down + circulation waste).

### Ink supply architecture — say which one, it matters to buyers
- **Cartridge**: Roland LEF2 (220 cc / 500 cc). Lowest entry cost, highest cost per litre.
- **Bottle**: Mimaki UJF/JFX (250 ml / 1 L). Mid.
- **Bulk tank**: Chinese industrial (1.5 L FR1800 · 2 L H1000/H1216/DTF · 3 L dye-sub · 5 L
  FR3210/R5200). Lowest cost per litre; requires degassing + circulation on white.
- **Ink pack**: Mimaki JV/CJV/TS (1 L / 2 L; white always 500 ml because of settling).

### RIP software actually bundled/supported (real names only)
| RIP | Seen on |
|---|---|
| **RasterLink7 / TxLink** | Mimaki (bundled) |
| **VersaWorks 6** | Roland (bundled) |
| **ONYX** | DOCAN all series, Chinese eco-solvent & dye-sub |
| **Caldera** | DOCAN all series, HandTop (official Caldera driver family) |
| **SAi Flexi / FlexiPRINT** | DOCAN all series, Chinese small UV |
| **PhotoPRINT** | DTF Linko, Chinese eco-solvent, dye-sub |
| **Maintop (6.0 / 6.1)** | Chinese UV, DTF, dye-sub — near-universal on Chinese hardware |
| **Wasatch** | dye-sub |
| **NeoStampa** | dye-sub / textile |
| **PrintFactory** | DTF Linko |
| **CADlink** | Sublistar small UV |

### Environment specs — the honest ranges
- UV flatbeds: **20–30 °C** (Mimaki), **20–28 °C** (Chinese industrial), **16–38 °C** (small
  desktop). Humidity **35–65 % RH** (Mimaki/Chinese) or **35–80 % RH** (Roland benchtop).
- Mimaki JFX600 additionally specifies **±10 °C/h max temperature gradient** and warns dimensional
  accuracy is only guaranteed 20–25 °C — a genuinely differentiating spec worth quoting.
- DTF: **20–35 °C**. Dye-sub: **18–30 °C**.

### Power — the number that decides site prep
- Desktop UV: 1 kW (Mimaki UJF-6042) to 3.8 kW (Chinese 3-head).
- Roland benchtop: 149–178 W (!) — genuinely low, worth calling out.
- 1.6 m roll: max 1440 W × 2 (Mimaki), 4 kW / 20 A (DOCAN FR1800).
- 2.5 m flatbed: < 2.88 kVA (Mimaki JFX200) vs **10 kW / 45 A** (DOCAN H1000). Huge gap — Chinese
  machines put the UV lamps and vacuum blowers on the same feed.
- 3.2 m hybrid: **15 kW / 70 A** (DOCAN FR3210).
- JFX600-2513: **three separate single-phase 200–240 V / 24 A inlets**, each < 4.8 kVA.
- Calender: **18–117 kW, 3-phase 380 V** — by far the biggest electrical load in any shop.
- Summa F1612: 3-phase.

### Turkish consumables vocabulary (for the sarf/yedek parça section)
`mürekkep` (ink) · `baskı kafası` (print head) · `damper` (damper — replace every ~6 months) ·
`kaptop / capping station` · `wiper` · `kafa temizleme solüsyonu` (head cleaning solution) ·
`encoder şerit / kodlayıcı sensörü` · `PU transfer tozu` (DTF powder) · `PET film` ·
`temizleme kiti`.
([t2dijital](https://www.t2dijital.com/dijital-baski-yedek-parcalari/),
[printec-online](https://www.printec-online.com/urun-kategori/transfer-baski-makineleri/dtf-baski-makinesi-ve-sarf-malzemesi/))

---

## 11. Proposed sample catalogue — 11 machines

Every number is inside a documented real range. Model naming follows the industry convention
(format code + head count), so `MV-2513 R8` reads as "2500×1300, 8 Ricoh heads" to anyone in the
trade.

| # | Model | Family | Key specs to publish |
|---|---|---|---|
| 1 | **Maven MV-6090 U3** | UV flatbed, small | 600 × 900 mm · 3 × Epson i3200-U1 · 2.5–8 m²/h · 720 × 2400 dpi · CMYK+W+V · max media height 180 mm · 4 × LED UV · zoned vacuum aluminium table · 3.8 kW / 220 V · 1696 × 1595 × 719 mm · 194 kg · 16–38 °C / 35–65 % RH · PhotoPRINT / Maintop |
| 2 | **Maven MV-1216 R4** | UV flatbed, mid | 1200 × 1540 mm · 2–4 × Ricoh Gen6 (5 pl) · 4p 22–28 / 6p 16–22 / 8p 14–16 m²/h · 726 × 1200 dpi · CMYK+Lc+Lm+W · max height 100 mm · 2 L bulk tanks · 10 kW / 45 A · 3000 × 2300 × 1350 mm · 720 kg · 20–28 °C / 40–60 % RH · ONYX / Caldera / SAi |
| 3 | **Maven MV-2513 R8** | UV flatbed, large | 2500 × 1250 mm · 2–12 × Ricoh Gen6 · 4p 50–60 / 6p 36–42 / 8p 27–30 m²/h · 726 × 1440 dpi · CMYK+Lc+Lm+W+V · max height 100 mm (300 mm option) · 3-zone vacuum · auto height sensor + anti-collision · white ink circulation · 2 L tanks · 10 kW / 45 A · 4700 × 2100 × 1400 mm · 1510 kg |
| 4 | **Maven MV-3220 K12** | UV flatbed, industrial | 3200 × 2000 mm · 4–18 × Konica KM1024i (6 pl) · 4p 75–84 / 8p 47–54 m²/h · 604 × 2400 dpi · CMYK+Lc+Lm+W+V · water-cooled LED curing · 10 kW / 45 A · 5600 × 3100 × 1540 mm · 2580 kg |
| 5 | **Maven MH-1800 U4** | UV hybrid, 1.8 m | 1800 mm · 1–4 × Epson i3200-U1 · 45 m²/h colour / 13 m²/h C-W-C · 726 × 900 dpi · CMYK+W (+Fl option) · rigid height ≤ 10 mm · 1.5 L tanks · 4 kW / 20 A · 3450 × 1000 × 1500 mm · 500 kg |
| 6 | **Maven MH-3200 R12** | UV hybrid, 3.2 m | 3200 mm · 2–20 × Ricoh Gen6 · 4p 92–111 / 6p 61–74 / 8p 41–49 m²/h · 726 × 2400 dpi · CMYK+Lc+Lm+W · 5 L tanks · heavy-duty roll option 1–2 t · 15 kW / 70 A · 5950 × 1700 × 1600 mm · 2985 kg |
| 7 | **Maven MS-1802 E4** | Eco-solvent, 1.8 m | 1800 mm · 4 × Epson i3200-E1 · production 79 m²/h / standard 54 m²/h · up to 2400 dpi · CMYK · 3-stage heater (pre / platen / post) · auto capping & cleaning · take-up · Maintop / PhotoPRINT / ONYX |
| 8 | **Maven MSC-1600 PC** | Eco-solvent print & cut, 1.6 m | media ≤ 1610 mm · 2 staggered piezo heads, min 3 pl · up to 100 m²/h · 600–1200 dpi · CMYK+Lc+Lm+Lk+Or+W · 2 L packs (W 500 ml) · cut 300 mm/s, 10–450 gf, ±0.2 mm · tri-zone heater · 3-roll changer + XY slitter · 3170 × 1215 × 1305 mm · 373 kg |
| 9 | **Maven MD-600 A4** | DTF system, 60 cm | 620 mm · 4 × Epson i3200-A1 · 4p 12 / 6p 8 / 8p 6 m²/h · 720 × 2400 dpi · CMYK+W · 2 L bulk pot · vertical shaker 1652 × 1066 × 902 mm, 220 V 20 A, 2000–5200 W, ≈70 kg · integrated oven + fume filter · 20–35 °C · Maintop 6.1 / PhotoPRINT / PrintFactory |
| 10 | **Maven MT-1900 A4 + MC-1900** | Dye-sub 1.9 m + calender | printer: 1900 mm · 4 × Epson i3200-A1 · 2p 180 / 3p 120 / 4p 90 m²/h · CMYK · 4 × 3 L tanks · take-up to 1000 m · two-stage dryer (max 7.2 kW) · 3180 × 1100 × 1700 mm · 18–30 °C · calender: 1.9 m · 600 mm oil drum · 3-phase 380 V · ~40 kW · 3 feed + 3 collect |
| 11 | **Maven MC-300 UV** | UV DTF / crystal label, 30 cm | 300 mm · 1 × Epson i3200-U1HD · 3.6 m²/h @4-pass · up to 2400 dpi · CMYK+W+Varnish · white ink auto-stirring · dual UV LED · integrated automatic AB-film laminator · media ≤ 1.5 mm · 3.5 kW · 1160 × 730 × 1380 mm · 100 kg · 15–32 °C / 35–80 % RH |

**Optional 12th (cutting), if we want the finishing category:**
**Maven MK-1612** flatbed cutter — 1600 × 1200 mm · 1000 mm/s · 1 G acceleration · ±0.05 mm ·
200 N down-force · 4 vacuum zones · 3-tool head (tangential / oscillating / creasing / routing /
V-cut) · 3-phase · 2470 × 2200 × 1100 mm. Plus **Maven MK-600** roll plotter — 609 mm cut width,
450 gf, 900 mm/s.

---

## 12. Explicitly unverified / flag list

Do **not** present these as facts without re-checking:

1. **Mimaki JFX200-2513 EX and JFX600 per-pass speed tables.** Mimaki publishes only "max 200 m²/h"
   for JFX600 and no m²/h table at all for JFX200-2513 EX. The 4/6/8-pass ladders in this document
   come from DOCAN, not Mimaki.
2. **Roland TrueVIS VG3 blade force.** One reseller states "2500 gf max instantaneous"; Roland's
   normal published range for this class is 30–500 gf. Do not publish either number.
3. **Roland LEF2 print speed in m²/h.** Roland publishes only a relative claim ("up to 60 % faster").
4. **Mimaki TS55-1800 dryer temperatures** and **Epson F9470 m²/h** — not on the spec pages found.
5. **Ricoh's own printhead spec pages are offline** (`industry.ricoh.com` now 301s to a "closed"
   notice). All Ricoh Gen5/Gen6 figures here come from distributor pages that agree with each other,
   not from Ricoh.
6. **Toshiba CE4 max drive frequency** — not published by any source found.
7. **Lazerpol's "Baskı Alanı 130×130 mm"** is a typo on their site (should be 1300 × 1300 mm).
8. **UV DTF "m/h" vs "m²/h"** — vendors conflate the two constantly (§7).
9. **Price bands marked ⚠** are inferred from dealer listings, not manufacturer list prices.
10. **Kyocera KJ4B-QA is a water-based head.** Chinese UV vendors list "Kyocera" heads on UV
    machines — those are the KJ4A/KJ4B-EX UV-capable variants, not the QA. Don't put KJ4B-QA on a
    UV machine spec sheet.
