# 00 — MAVEN MASTER BUILD SPEC

**Status:** authoritative. This document supersedes the eight research tracks for all build
decisions. Tracks 01–08 remain the evidence base; where they disagreed, this file picks one and
says why in one line. If the build contradicts this file, the build is wrong.

**Repo:** `C:/claude/projects/meric-baski` (folder name is legacy; the brand is **Maven**)
**Compiled:** 2026-07-28 from tracks 01–08 (212 cited sources)
**Deployment target:** Vercel, static output, no serverless functions.

---

## 1. POSITIONING

Maven is a Turkish **dealer, importer and technical-service house** for industrial digital printing
— it sells the machines (UV flatbed, hybrid, eco-solvent, DTF, dye-sublimation, UV-DTF, cutting)
*and* the recurring half nobody else in the Turkish market publishes properly: inks, printheads,
spare parts and the service contract that keeps the machine earning. The site's job is not to
impress; it is to make a print-shop owner who is about to spend $80,000 feel that **the people
behind this page know his machine better than he does.** Every decision follows from that: numbers
before adjectives, a real spec table instead of a PDF, published service commitments instead of
"kaliteli hizmet", Turkish Güvenlik Bilgi Formu on every chemical, a compatibility matrix that
answers "does this ink run in my Konica 1024i?" in one click, and one WhatsApp tap to a human. The
visual register is **instrument documentation, not brochure**: black ink on paper, hairline rules,
tabular figures, mono micro-labels, enormous whitespace, and exactly one CMYK accent per section —
the colour comes from the product, never from the chrome. The buyer should close the tab thinking
*"these are engineers who happen to sell,"* not *"this is a nice website."*

**The three things that must be true after launch, in priority order:**
1. A buyer can specify a machine completely without contacting us — then contacts us anyway,
   because the quote path is one tap from wherever he stopped reading.
2. A returning customer can find the exact ink and part for his existing machine in under 30 seconds.
3. Nothing on the page reads as fabricated to somebody who runs these machines for a living.

---

## 2. INFORMATION ARCHITECTURE

### 2.1 Routing decisions (locked)

| Decision | Value | One-line justification |
|---|---|---|
| Default locale | `tr` at **site root**, no `/tr/` prefix | TR is the primary market; shorter canonicals and better TR-geo signals, and track 01 proved a dead `/tr/` prefix is what happens when you bolt locales on later. |
| Second locale | `en` at `/en/` | Locale-prefixed non-default is the Durst model and the only shape that scales. |
| URL segments | **Translated per locale via a slug map** | `/en/urunler/` is bad craft and bad SEO; Astro's `getRelativeLocaleUrl()` does not translate segments, so `src/i18n/routes.ts` is mandatory (track 07). |
| Trailing slash | **always** (`trailingSlash: 'always'` + `build.format: 'directory'` + `vercel.json trailingSlash: true`) | One canonical form, no 308 round-trips. |
| Case | lowercase, ASCII-folded Turkish slugs (`urunler`, not `ürünler`) | Turkish characters in URLs percent-encode into noise in shares and analytics. |
| Nav depth | Max 2 levels | A 26-SKU catalogue does not need a mega-menu tree; it needs facets. |

### 2.2 Primary navigation (6 items + action cluster)

Inks sit at **top level as a sibling of machines** — 4 of 5 global OEMs do this (track 02), it is
swissQprint's precedent (track 06), and it is literally half of Maven's revenue.

| # | TR nav label | EN nav label | Target |
|---|---|---|---|
| 1 | `Makineler` | `Machines` | `/makineler/` ↔ `/en/machines/` |
| 2 | `Mürekkep & Sarf` | `Inks & Supplies` | `/murekkep-sarf/` ↔ `/en/inks-supplies/` |
| 3 | `Uygulamalar` | `Applications` | `/uygulamalar/` ↔ `/en/applications/` |
| 4 | `Teknik Servis` | `Service` | `/teknik-servis/` ↔ `/en/service/` |
| 5 | `Kurumsal` | `Company` | `/kurumsal/` ↔ `/en/company/` |
| 6 | `İletişim` | `Contact` | `/iletisim/` ↔ `/en/contact/` |

**Action cluster, pinned right at every breakpoint:** `[ Teklif Al ]` (filled button, the only
filled button in the header) · phone `0212 XXX XX XX` (`tel:` link) · WhatsApp glyph · `TR / EN`.
On mobile the phone and WhatsApp collapse into the sticky bottom bar; `Teklif Al` stays in the header.

**Deliberately not in the nav** (footer + contextual entry points only): `Referanslar`, `Belgeler`,
`Uyumluluk`, `Finansman`, `İkinci El`, `Bilgi`. They earn traffic from search and internal links,
not from nav real estate.

### 2.3 Full sitemap — TR

`H1` is the on-page heading. `<title>` pattern is defined in §10.1.

| URL (TR) | H1 | Nav label / where it's linked from |
|---|---|---|
| `/` | *(hero statement, see §4.1)* | `Ana Sayfa` — logo |
| `/makineler/` | Makineler | nav 1 |
| `/makineler/uv-flatbed-baski-makineleri/` | UV Flatbed Baskı Makineleri | dropdown |
| `/makineler/uv-hibrit-baski-makineleri/` | UV Hibrit Baskı Makineleri | dropdown |
| `/makineler/eko-solvent-baski-makineleri/` | Eko Solvent Baskı Makineleri | dropdown |
| `/makineler/dtf-baski-sistemleri/` | DTF Baskı Sistemleri | dropdown |
| `/makineler/sublimasyon-baski-sistemleri/` | Süblimasyon Baskı Sistemleri | dropdown |
| `/makineler/uv-dtf-kristal-etiket-makineleri/` | UV DTF / Kristal Etiket Makineleri | dropdown |
| `/makineler/kesim-makineleri/` | Kesim Makineleri ve Plotterlar | dropdown |
| `/makineler/{kategori}/{model}/` | {Model adı} | product cards |
| `/makineler/{kategori}/{model}/teknik-ozellikler/` | {Model adı} — Teknik Özellikler | PDP spec block "tam listeyi aç" |
| `/makineler/karsilastir/` | Makine Karşılaştırma | PDP + category |
| `/murekkep-sarf/` | Mürekkep ve Sarf Malzemeleri | nav 2 |
| `/murekkep-sarf/uv-murekkep/` | UV Mürekkep | dropdown |
| `/murekkep-sarf/uv-led-murekkep/` | UV LED Mürekkep | dropdown |
| `/murekkep-sarf/uv-dtf-murekkep/` | UV DTF Mürekkep | dropdown |
| `/murekkep-sarf/eko-solvent-murekkep/` | Eko Solvent Mürekkep | dropdown |
| `/murekkep-sarf/solvent-murekkep/` | Solvent Mürekkep | dropdown |
| `/murekkep-sarf/sublimasyon-murekkebi/` | Süblimasyon Mürekkebi | dropdown |
| `/murekkep-sarf/dtf-pigment-murekkep/` | DTF Pigment Mürekkep | dropdown |
| `/murekkep-sarf/tekstil-pigment-murekkebi/` | Tekstil Pigment Mürekkebi | dropdown |
| `/murekkep-sarf/{aile}/{urun}/` | {Ürün adı} | product cards |
| `/murekkep-sarf/baski-kafalari/` | Baskı Kafaları | dropdown |
| `/murekkep-sarf/yedek-parca/` | Yedek Parça | dropdown |
| `/murekkep-sarf/yardimci-malzemeler/` | Yardımcı Malzemeler | dropdown |
| `/uyumluluk/` | Makine – Mürekkep Uyumluluk Tablosu | ink + machine PDPs, footer |
| `/uygulamalar/` | Uygulamalar | nav 3 |
| `/uygulamalar/reklam-tabela/` | Reklam ve Tabela | tile |
| `/uygulamalar/ambalaj-etiket/` | Ambalaj ve Etiket | tile |
| `/uygulamalar/mobilya-dekorasyon/` | Mobilya ve Dekorasyon | tile |
| `/uygulamalar/cam-metal-endustriyel/` | Cam, Metal ve Endüstriyel | tile |
| `/uygulamalar/tekstil-promosyon/` | Tekstil ve Promosyon | tile |
| `/uygulamalar/arac-giydirme/` | Araç Giydirme | tile |
| `/teknik-servis/` | Teknik Servis | nav 4 |
| `/teknik-servis/servis-talebi/` | Servis Talep Formu | service page CTA |
| `/teknik-servis/kurulum-ve-egitim/` | Kurulum ve Operatör Eğitimi | service page |
| `/teknik-servis/garanti-kosullari/` | Garanti Koşulları | service page, PDP |
| `/belgeler/` | Belgeler ve Güvenlik Bilgi Formları | ink PDPs, footer |
| `/kurumsal/` | Kurumsal | nav 5 |
| `/kurumsal/referanslar/` | Referanslar | kurumsal, footer |
| `/kurumsal/fuarlar-ve-showroom/` | Fuarlar ve Showroom | kurumsal, footer |
| `/finansman/` | Ödeme ve Finansman | PDP finance block, footer |
| `/ikinci-el/` | İkinci El ve Takas Makineler | footer, machines index |
| `/bilgi/` | Bilgi Merkezi | footer |
| `/bilgi/{slug}/` | {Yazı başlığı} | index |
| `/iletisim/` | İletişim | nav 6 |
| `/teklif-al/` | Teklif Al | header button |
| `/numune-talebi/` | Baskı Numunesi Talebi | PDP secondary CTA |
| `/tesekkurler/` | Teşekkürler | form redirect target (no-JS path) |
| `/kvkk-aydinlatma-metni/` | KVKK Aydınlatma Metni | footer + every form |
| `/cerez-politikasi/` | Çerez Politikası | footer |
| `/kullanim-kosullari/` | Kullanım Koşulları | footer |
| `/404` | Sayfa bulunamadı | — |

### 2.4 Full sitemap — EN (slug map)

Same page set, English segments. This table **is** `src/i18n/routes.ts` (§9.3).

| Route key | TR segment | EN segment |
|---|---|---|
| `home` | `` | `` |
| `machines` | `makineler` | `machines` |
| `machines.uvFlatbed` | `uv-flatbed-baski-makineleri` | `uv-flatbed-printers` |
| `machines.uvHybrid` | `uv-hibrit-baski-makineleri` | `uv-hybrid-printers` |
| `machines.ecoSolvent` | `eko-solvent-baski-makineleri` | `eco-solvent-printers` |
| `machines.dtf` | `dtf-baski-sistemleri` | `dtf-printing-systems` |
| `machines.sublimation` | `sublimasyon-baski-sistemleri` | `dye-sublimation-systems` |
| `machines.uvdtf` | `uv-dtf-kristal-etiket-makineleri` | `uv-dtf-crystal-label-printers` |
| `machines.cutting` | `kesim-makineleri` | `cutting-systems` |
| `machines.specs` | `teknik-ozellikler` | `specifications` |
| `machines.compare` | `karsilastir` | `compare` |
| `inks` | `murekkep-sarf` | `inks-supplies` |
| `inks.uv` | `uv-murekkep` | `uv-inks` |
| `inks.uvled` | `uv-led-murekkep` | `uv-led-inks` |
| `inks.uvdtf` | `uv-dtf-murekkep` | `uv-dtf-inks` |
| `inks.ecoSolvent` | `eko-solvent-murekkep` | `eco-solvent-inks` |
| `inks.solvent` | `solvent-murekkep` | `solvent-inks` |
| `inks.sublimation` | `sublimasyon-murekkebi` | `dye-sublimation-inks` |
| `inks.dtf` | `dtf-pigment-murekkep` | `dtf-pigment-inks` |
| `inks.textile` | `tekstil-pigment-murekkebi` | `textile-pigment-inks` |
| `inks.printheads` | `baski-kafalari` | `printheads` |
| `inks.spares` | `yedek-parca` | `spare-parts` |
| `inks.auxiliaries` | `yardimci-malzemeler` | `auxiliaries` |
| `compatibility` | `uyumluluk` | `compatibility` |
| `applications` | `uygulamalar` | `applications` |
| `applications.signage` | `reklam-tabela` | `signage-advertising` |
| `applications.packaging` | `ambalaj-etiket` | `packaging-labels` |
| `applications.interior` | `mobilya-dekorasyon` | `furniture-interior` |
| `applications.industrial` | `cam-metal-endustriyel` | `glass-metal-industrial` |
| `applications.textile` | `tekstil-promosyon` | `textile-promotional` |
| `applications.vehicle` | `arac-giydirme` | `vehicle-wrapping` |
| `service` | `teknik-servis` | `service` |
| `service.request` | `servis-talebi` | `service-request` |
| `service.training` | `kurulum-ve-egitim` | `installation-training` |
| `service.warranty` | `garanti-kosullari` | `warranty` |
| `documents` | `belgeler` | `documents` |
| `about` | `kurumsal` | `company` |
| `about.references` | `referanslar` | `references` |
| `about.events` | `fuarlar-ve-showroom` | `trade-fairs-showroom` |
| `finance` | `finansman` | `financing` |
| `used` | `ikinci-el` | `used-machines` |
| `insights` | `bilgi` | `insights` |
| `contact` | `iletisim` | `contact` |
| `quote` | `teklif-al` | `request-a-quote` |
| `samples` | `numune-talebi` | `request-samples` |
| `thanks` | `tesekkurler` | `thank-you` |
| `privacy` | `kvkk-aydinlatma-metni` | `privacy-notice` |
| `cookies` | `cerez-politikasi` | `cookie-policy` |
| `terms` | `kullanim-kosullari` | `terms-of-use` |

**Page count:** 48 TR + 48 EN = **96 routes**, generated from ~26 product YAML files and 12 page
templates. This is exactly why the stack is Astro and not hand-written HTML.

### 2.5 Footer (site-wide, 5 columns + legal band)

```
COL 1  Logo · one-line positioning · WhatsApp + phone + e-mail
COL 2  Makineler        (7 family links)
COL 3  Mürekkep & Sarf  (8 ink families + Baskı Kafaları + Yedek Parça + Yardımcı Malzemeler)
COL 4  Kurumsal         (Kurumsal · Referanslar · Fuarlar ve Showroom · Bilgi Merkezi · İkinci El)
COL 5  Destek           (Teknik Servis · Servis Talebi · Garanti · Belgeler · Uyumluluk · Finansman)

LEGAL BAND (mono, --step--2, --muted-dark on --ink):
{Ticaret Unvanı} · {Adres} · Vergi Dairesi: {…} VKN: {…} · MERSİS: {…} · Ticaret Sicil No: {…}
KVKK Aydınlatma Metni · Çerez Politikası · Kullanım Koşulları · © 2026 Maven
Görseller: Pexels / Unsplash / Pixabay katkıda bulunanları. Makine görselleri Maven tarafından üretilmiştir.
```

The identity block is required by **TTK m.39/2** (ticaret unvanı, MERSİS no, işletme merkezi) and
doubles as the strongest cheap trust signal in the Turkish market (track 04).

---

## 3. PRODUCT TAXONOMY

### 3.1 Naming system (invented, coherent, trade-legible)

```
MAVEN  <SERIES><FORMAT>  <HEAD><COUNT>
        │       │          │      └── max head count in the configuration ladder
        │       │          └───────── head brand letter
        │       └──────────────────── format code: width in cm, or bed W×H in dm
        └──────────────────────────── two-letter family series
```

| Series | Family | Format code reads as |
|---|---|---|
| `MF` | **M**aven **F**latbed (UV flatbed) | bed size in dm: `2513` = 2500 × 1300 mm |
| `MH` | **M**aven **H**ybrid (UV hybrid / roll) | print width in cm: `3200` = 3.2 m |
| `MS` | **M**aven **S**olvent (eco-solvent roll & print-cut) | print width in cm |
| `MD` | **M**aven **D**TF (film transfer system) | film width in mm: `600` = 60 cm |
| `MT` | **M**aven **T**extile (dye-sublimation) | print width in cm |
| `MC` | **M**aven **C**rystal (UV DTF / crystal label) | web width in mm |
| `MK` | **M**aven **K**esim (cutting) | working area in dm |
| `MR` | **M**aven **R**otary (calender — system companion) | transfer width in cm |
| `MI` | **M**aven **I**nk (consumables) | 3-digit chemistry series (§3.4) |

| Head letter | Head |
|---|---|
| `R` | Ricoh Gen5 / Gen6 |
| `K` | Konica Minolta KM1024i |
| `U` | Epson i3200-**U**1 (UV) |
| `E` | Epson i3200-**E**1 (eco-solvent) |
| `A` | Epson i3200-**A**1 (aqueous / DTF / dye-sub) |
| `Y` | K**y**ocera |
| `T` | Toshiba CE4 |

Fixed-configuration machines carry a **config code** instead of a head code (`PC` = print & cut).
Machines with no heads (cutters) carry no suffix. So `MF-2513 R8` parses instantly to
"2500×1300 bed, up to 8 Ricoh heads" for anyone in the trade — which is exactly how the Turkish
market names product (track 04 §5.1).

### 3.2 Machine families (7)

| # | TR name | EN name | Slug (TR / EN) | Accent |
|---|---|---|---|---|
| 1 | UV Flatbed Baskı Makineleri | UV Flatbed Printers | `uv-flatbed-baski-makineleri` / `uv-flatbed-printers` | cyan |
| 2 | UV Hibrit Baskı Makineleri | UV Hybrid Printers | `uv-hibrit-baski-makineleri` / `uv-hybrid-printers` | cyan |
| 3 | Eko Solvent Baskı Makineleri | Eco-Solvent Printers | `eko-solvent-baski-makineleri` / `eco-solvent-printers` | cyan |
| 4 | DTF Baskı Sistemleri | DTF Printing Systems | `dtf-baski-sistemleri` / `dtf-printing-systems` | cyan |
| 5 | Süblimasyon Baskı Sistemleri | Dye-Sublimation Systems | `sublimasyon-baski-sistemleri` / `dye-sublimation-systems` | cyan |
| 6 | UV DTF / Kristal Etiket Makineleri | UV DTF / Crystal Label Printers | `uv-dtf-kristal-etiket-makineleri` / `uv-dtf-crystal-label-printers` | cyan |
| 7 | Kesim Makineleri ve Plotterlar | Cutting Systems & Plotters | `kesim-makineleri` / `cutting-systems` | cyan |

### 3.3 Machine catalogue — 12 models (v1)

Every number below sits inside a documented real range (track 05). Tier drives copy register, not
a visible badge.

| # | Model | Family | Tier | What it is (one line) |
|---|---|---|---|---|
| 1 | **Maven MF-6090 U3** | UV Flatbed | Giriş | 600 × 900 mm masaüstü UV flatbed, 3 × Epson i3200-U1, 180 mm baskı yüksekliği — promosyon, hediyelik, kişiselleştirme. |
| 2 | **Maven MF-1216 R4** | UV Flatbed | Orta | 1200 × 1540 mm UV flatbed, 2–4 × Ricoh Gen6 (5 pl), 22–28 m²/sa @4-pass — küçük tabela ve levha üretimi. |
| 3 | **Maven MF-2513 R8** | UV Flatbed | Endüstriyel | 2500 × 1300 mm UV flatbed, 2–12 × Ricoh Gen6, 3 bölgeli vakum, beyaz sirkülasyon — sektörün hacim makinesi. **3D** |
| 4 | **Maven MF-3220 K12** | UV Flatbed | Amiral | 3200 × 2000 mm endüstriyel UV flatbed, 4–18 × Konica KM1024i, su soğutmalı LED kürleme, 75–84 m²/sa @4-pass. |
| 5 | **Maven MH-1800 U4** | UV Hibrit | Giriş | 1.8 m hibrit, 1–4 × Epson i3200-U1, rulo + 10 mm levha, 45 m²/sa renk / 13 m²/sa C-W-C. |
| 6 | **Maven MH-3200 R12** | UV Hibrit | Endüstriyel | 3.2 m hibrit, 2–20 × Ricoh Gen6, 5 L tank, ağır rulo opsiyonu 1–2 t, 92–111 m²/sa @4-pass. **3D** |
| 7 | **Maven MS-1802 E4** | Eko Solvent | Orta | 1.8 m eko solvent rulo, 4 × Epson i3200-E1, 3 kademeli ısıtıcı, üretim 79 m²/sa. |
| 8 | **Maven MS-1600 PC** | Eko Solvent | Orta-üst | 1.6 m baskı-kesim (print & cut), 2 kademeli piezo kafa, 100 m²/sa, kesim 300 mm/s @10–450 gf, 3 rulo değiştirici. |
| 9 | **Maven MD-600 A4** | DTF Sistem | Orta | 60 cm DTF sistemi: 4 × Epson i3200-A1 yazıcı + dikey toz serpme/fırın ünitesi + duman filtresi, 12 m²/sa @4-pass. **3D** |
| 10 | **Maven MT-1900 A4** | Süblimasyon | Orta-üst | 1.9 m transfer süblimasyon, 4 × Epson i3200-A1, 2-pass 180 m²/sa, 1000 m sarma — **MR-1900** kalender ile sistem. |
| 11 | **Maven MC-300 U1** | UV DTF | Giriş | 30 cm UV DTF / kristal etiket, 1 × Epson i3200-U1HD, CMYK+W+Lak, entegre otomatik A/B film laminasyon, 3.6 m²/sa. **3D** |
| 12 | **Maven MK-1612** | Kesim | Endüstriyel | 1600 × 1200 mm dijital flatbed kesim, 1000 mm/s, 1 G ivme, ±0,05 mm, 200 N, 4 vakum bölgesi, 3 takımlı kafa. |

**System companions** (modelled as `components[]` inside their parent product, not as separate SKUs):
`MR-1900` kalender (600 mm yağlı tambur, 3 faz 380 V, ~40 kW) under MT-1900 A4; `MD-600 SH` toz
serpme ünitesi (1652 × 1066 × 902 mm, 220 V 20 A, 2000–5200 W, ≈70 kg) under MD-600 A4.

**Planned v1.1 (do not build now, keep the slug free):** `MK-600` rulo folyo kesici,
`MF-1313 U3` orta masaüstü, `MS-3200 K4` 3.2 m solvent.

### 3.4 Ink & consumable families (8 ink + 3 consumable)

| # | TR name | EN name | Slug (TR) | Accent |
|---|---|---|---|---|
| 1 | UV Mürekkep | UV Curable Inks | `uv-murekkep` | magenta |
| 2 | UV LED Mürekkep | UV-LED Inks | `uv-led-murekkep` | magenta |
| 3 | UV DTF Mürekkep | UV DTF Inks | `uv-dtf-murekkep` | magenta |
| 4 | Eko Solvent Mürekkep | Eco-Solvent Inks | `eko-solvent-murekkep` | magenta |
| 5 | Solvent Mürekkep | Solvent Inks | `solvent-murekkep` | magenta |
| 6 | Süblimasyon Mürekkebi | Dye-Sublimation Inks | `sublimasyon-murekkebi` | magenta |
| 7 | DTF Pigment Mürekkep | DTF Pigment Inks | `dtf-pigment-murekkep` | magenta |
| 8 | Tekstil Pigment Mürekkebi | Textile Pigment Inks | `tekstil-pigment-murekkebi` | magenta |
| 9 | Baskı Kafaları | Printheads | `baski-kafalari` | magenta |
| 10 | Yedek Parça | Spare Parts | `yedek-parca` | magenta |
| 11 | Yardımcı Malzemeler | Auxiliaries | `yardimci-malzemeler` | magenta |

Series numbering: `1xx` UV-Hg · `2xx` UV-LED · `3xx` UV-DTF · `4xx` eko solvent · `5xx` solvent ·
`6xx` süblimasyon · `7xx` DTF · `8xx` tekstil · `9xx` yardımcı.

### 3.5 Ink catalogue — 10 products (v1)

| # | Product | Family | Tier | What it is (one line) |
|---|---|---|---|---|
| 1 | **Maven MI-110 UV** | UV (Hg) | Endüstriyel | Cıva buharlı endüstriyel flatbed mürekkebi; 225–300 mJ/cm² @600 mW/cm²; C M Y K Lc Lm Lk Or W Cl (Gr/Vt talebe bağlı); 1 L / 5 L şişe, 2 L MBS torba. |
| 2 | **Maven MI-210 UV-LED R** | UV-LED | Endüstriyel | Ricoh Gen5/Gen6 kafalar için 395 nm UV-LED; 24 saat son kürlenme; C M Y K Lc Lm W Lak; 1 L şişe (çip dahil), 600 ml torba. |
| 3 | **Maven MI-220 UV-LED E** | UV-LED | Orta | Epson i3200-U1 / XP600 kafalar için UV-LED; esnek film ve ince malzeme; C M Y K W Lak; 1 L şişe. |
| 4 | **Maven MI-310 UV-DTF** | UV DTF | Orta | A/B film kristal etiket mürekkebi; CMYK + W + Lak; laminasyon basıncı ve film eşleşmesi tablolu. |
| 5 | **Maven MI-410 ECO** | Eko solvent | Volüm | i3200-E1 / DX5 / DX7 / XP600 için eko solvent; düşük koku; C M Y K (+Lc Lm Or); 1 L şişe, 2 L torba, 440/500 ml kartuş. |
| 6 | **Maven MI-420 ECO-TR** | Eko solvent | Volüm | OEM eşdeğeri seri — TrueVIS TR2 / SureColor / Mutoh kartuş formatlarında; `Doğrudan geçiş` sınıfı. |
| 7 | **Maven MI-510 SOL** | Solvent | Endüstriyel | Konica KM1024i grand-format için gerçek solvent; en düşük m² maliyeti; 5 / 10 / 20 L şişe, 5 L bag-in-box; havalandırma zorunlu. |
| 8 | **Maven MI-610 SUB** | Süblimasyon | Orta | Transfer süblimasyon; 180–220 °C, 30–180 s, A–D sınıfları; C M Y K + Lc Lm Bl Or + 4 flüor; 1 L şişe, 2 L torba; **raf ömrü 15 ay**. |
| 9 | **Maven MI-710 DTF** | DTF pigment | Volüm | Film transfer pigment; 4,0 cps ±0,5 @25 °C, 30 ±3 din/cm, pH 9,0 ±0,5; CMYK 1 L / **Beyaz 900 ml (raf ömrü 6 ay)**; anti-sedimantasyon. |
| 10 | **Maven MI-810 TEX** | Tekstil pigment | Orta | DTG / direkt tekstil pigment; ön işlem sıvısı gerekli; fiksaj 160 °C 60–90 s; ISO 105-C06 ≥4; 1 L / 2 L bag-in-box. |

**Yardımcı ve sarf (listed under `yardimci-malzemeler`, schema = `ink` with `family: 'auxiliary'`):**
`MI-910 FLUSH` (kafa temizleme / yıkama sıvısı, 1 L + 250 ml pipetli şişe) ·
`MI-920 PRIMER` (cam/metal/PP yapışma artırıcı, 1 L) ·
`MD-PWD 80 / 170 / 250` (DTF sıcak eriyik toz: ince 0–80 µm, yumuşak 80–170 µm, kaba 120–250 µm; 1/5/20 kg) ·
`MD-FILM 600` (PET transfer film, 60 cm × 100 m).

**Changeover badge** — every alternative-ink product carries exactly one (Marabu's taxonomy,
translated; track 03 §4):

| Badge (TR) | Badge (EN) | Meaning |
|---|---|---|
| `Doğrudan geçiş` | `Switch & Print` | Full chemical + colour compatibility, print immediately |
| `Yıkama gerekir` | `Switch & Swap` | System flush required before changeover |
| `Profil gerekir` | `Switch & Match` | ICC re-profiling required for colour match |

---

## 4. PAGE ANATOMY

Notation: sections are ordered top→bottom. `[accent]` marks the one process colour allowed in that
section. Every page ends with the site-wide CTA band + footer, which is not repeated below.

### 4.1 Homepage `/`

| # | Section | Contents |
|---|---|---|
| 1 | **Hero** (`--paper`) | Single `<h1>` statement, `--step-5`, `wdth 82`, max 3 lines: *"Dijital baskı makineleri, mürekkep ve teknik servis — tek adresten."* Sub-line ≤22 words. Two CTAs: `[ Teklif Al ]` filled + `Makineleri İncele ›` line-sweep. Right/below: one full-bleed 21:9 duotoned production-floor photograph (LCP element, preloaded, ≤160 KB @1920w). **No slider.** A 3-square CMYK pixel row sits under the H1 — the only place all three colours touch on this page. |
| 2 | **Proof strip** (`--paper`, hairline top+bottom) | Four mono facts, no icons: `{N} yıl` · `{N}+ kurulum` · `{N} şehirde yerinde servis` · `24 saat içinde müdahale`. Numbers count up on entry (`Intl.NumberFormat('tr-TR')`). |
| 3 | **Makineler** (`--paper`) `[cyan]` | Mono eyebrow `01 — MAKİNELER` in grid cols 1–2, content 4–12. Seven family cards (container-query component): family name, one-line role, 3 headline specs as mono chips, count of models, `İncele ›`. Card hover = accent rule scaleX + thumbnail scale 1.03. |
| 4 | **Mürekkep & Sarf** (`--bone`) `[magenta]` | Eyebrow `02 — MÜREKKEP & SARF`. The **channel strip** component as the section's visual signature: real colour swatches for a full 10-channel set, W and Lak as outlined/hatched chips. Eight family links. One line of hard copy: *"Sattığımız her kimyasal ürün için Türkçe Güvenlik Bilgi Formu (GBF) sağlıyoruz."* → `/belgeler/`. |
| 5 | **Uyumluluk teaser** (`--bone`) `[magenta]` | Three-row excerpt of the machine × ink matrix with `Tüm tabloyu aç ›`. This is the page's differentiator and it goes above the fold-and-a-half on mobile. |
| 6 | **Uygulamalar** (`--paper`) | Six tiles, 3:2 duotone application photography, colour revealed on hover only. Labels follow the TR trade pattern (`UV Cam Baskı`, `Araç Giydirme`, `Etiket ve Ambalaj`). |
| 7 | **Teknik Servis** (`--ink`, dark punctuation) `[yellow]` | Numbered commitment list (5 items, mono index): müdahale süresi, garanti bölünmesi (elektronik 1 yıl / mekanik 2 yıl), yedek parça stoğu, eğitim kapsamı, ön keşif. `Servis talebi oluştur ›` in yellow on ink (15.22:1). |
| 8 | **Referanslar / marka şeridi** (`--paper`) | Logo marquee, 36 s linear loop, **visible pause control** (WCAG 2.2.2). If no client logos are cleared, this section is cut entirely — never fake it. |
| 9 | **Bilgi** (`--paper`) | Three latest articles, outcome-led headlines, mono dates. |
| 10 | **CTA band** (`--ink`) `[cyan]` | `Makinenizi birlikte seçelim.` + quote form shortcut + phone + WhatsApp. Seamless into footer, no rule between. |

### 4.2 Category page (machine family) `/makineler/{kategori}/`

| # | Section | Contents |
|---|---|---|
| 1 | Breadcrumb | All-caps mono, `›` separators: `ANA SAYFA › MAKİNELER › UV FLATBED BASKI MAKİNELERİ`. `BreadcrumbList` JSON-LD. |
| 2 | Header | **Unique H1 = the category name** (never the word "Ürünler" — track 01's worst failure). One-line role + 2–3 paragraphs of real editorial copy (300–600 words total on the page). |
| 3 | Filter bar | Client-side over a prebuilt JSON index: `Baskı genişliği` · `Baskı kafası` (brand) · `Kafa sayısı` · `Mürekkep tipi` · `Uygulama`. Live counts per facet. Sort: `Baskı genişliği` / `Hız` / `Model`. State in the URL query so a filtered view is shareable. |
| 4 | Product grid | Cards with subgrid alignment: model name (mono), category kicker, 4 headline specs as a mono mini-table (`Baskı Alanı`, `Baskı Kafası`, `Hız @4-pass`, `Renk Skalası`), thumbnail, `İncele ›` + `Teklif Al`. Head brand + count **in the card title** — that is how the market names product. |
| 5 | Comparison strip | Checkbox on each card → `Karşılaştır (2)` sticky pill → `/makineler/karsilastir/?m=a,b,c`. |
| 6 | `{Kategori} fiyatları hakkında` | H2 explaining price drivers (kafa sayısı, baskı genişliği, mürekkep sistemi, kurulum + eğitim dahil mi, nakliye/forklift/trifaze) ending in `Teklif Al`. **The highest-leverage section on the site for TR search** — the "fiyat/fiyatları" modifier is attached to nearly every TR query. |
| 7 | `Sıkça Sorulan Sorular` | 4–6 Q&A, `FAQPage` JSON-LD. |
| 8 | Uyumlu mürekkepler | Cross-link block to the ink families that run in this machine family. |

Ink category pages use the same skeleton; facets become `Kimya · Marka/Makine · Baskı kafası ·
Ambalaj · Uygulama`, and section 6 becomes `{Aile} kullanım ve maliyet` (ml/m² consumption, cost
per m², shelf life).

### 4.3 Machine detail page (PDP) `/makineler/{kategori}/{model}/`

The most important template on the site. Durst's four-panel IA + swissQprint's hero metrics +
the dealer's quote path.

| # | Section | Contents |
|---|---|---|
| 1 | Breadcrumb | mono caps, `BreadcrumbList` JSON-LD |
| 2 | **Hero split** (`--paper`) `[cyan]` | **Left 55%:** viewer — tab pair `GÖRSELLER` / `3D GÖRÜNÜM` (3D tab only rendered if `model3d` exists). Gallery = CSS scroll-snap, 4–8 application + machine frames, arrows + dot tabs. 3D = lazy-mounted `<model-viewer>` (§8). **Right 45%:** category kicker (mono) → `<h1>` model name → benefit tagline (one line, comma-joined benefit pair per TR convention) → **4 oversized hero metrics** (`--step-3`, mono, tabular-nums) → `[ Teklif Al ]` + `WhatsApp ile sor` + `Katalog İndir (PDF, 2,4 MB)` |
| 3 | Feature blocks | 3–5 blocks, each = named technology term + 1 sentence + one image or diagram. **Invent and reuse 2–3 ownable technology names per machine** (e.g. `Bölgesel Vakum Kontrolü`, `MavenFlow beyaz sirkülasyon`, `AutoGap yükseklik sensörü`) — the cheapest single thing separating OEM-grade from dealer-grade copy. |
| 4 | Accordion `AÇIKLAMA / TEKNİK VERİLER / ÖZELLİKLER / UYGULAMALAR` | Durst's exact four-panel IA, translated. Only the first open by default. `<details>`/`<summary>` with `grid-template-rows: 0fr → 1fr`. |
| 5 | **Teknik Özellikler** | Real `<table>`, grouped by `Baskı · Kafa & Mürekkep · Mekanik · Elektrik & Ortam · Yazılım & Bağlantı · Fiziksel`. `speedModes` renders as its own 3-row mini-table (4/6/8-pass) — never a single number. **Metric ⇄ imperial toggle** (nobody in Turkey does this). Long lists collapse behind `Tam listeyi aç ›` → the crawlable `/teknik-ozellikler/` sub-route. |
| 6 | `Uygulanabilir Malzemeler` | Chips: `Cam · Ahşap · MDF · Dekota · PVC · Polikarbon · Pleksi · Alüminyum kompozit · Fotoblok · Kanvas · Duvar kağıdı` — filterable, links to application pages. |
| 7 | `Kurulum Gereksinimleri` | **The honest block nobody publishes:** elektrik (trifaze?), alan (m² + tavan yüksekliği), kapı/asansör ölçüsü + paket ölçüleri, havalandırma, kompresör, ortam sıcaklık/nem, ve açıkça **"Fiyata dahil değildir: nakliye, forklift/vinç, elektrik altyapısı, havalandırma, sarf başlangıç seti."** |
| 8 | `Uyumlu Mürekkepler` | Cards for every ink whose `compatibleMachines[]` contains this SKU, with changeover badge. The margin lives here. |
| 9 | `Uygulama Görselleri` | 12–20 captioned real-job frames, lazy, lightbox-free (a full-width scroll-snap strip). |
| 10 | `Videolar` | Thumbnail cards linking out — never an embedded autoplaying iframe. |
| 11 | `İndirilebilir Dosyalar` | **Ungated** direct PDFs with size + language badge: katalog, teknik özellik sayfası, kurulum kontrol listesi. Gating the datasheet is the dealer-site tell. |
| 12 | `Ödeme ve Finansman` | Peşin · Kredi kartına taksit · Finansal kiralama (12–60 ay) · Takas → `/finansman/`. |
| 13 | `Servis ve Garanti` | 3 bullets + link to `/teknik-servis/garanti-kosullari/`. |
| 14 | `Benzer Makineler` | Sibling comparison table (this model vs 2 siblings, same spec rows) + `Karşılaştır ›`. |
| 15 | `Sıkça Sorulan Sorular` | 3–6 Q&A, `FAQPage` JSON-LD. |
| 16 | Quote form (inline) | §4.9 field set, product pre-filled and read-only. |
| 17 | **Sticky action bar** | Desktop: bottom bar, 4 outlined actions `KATALOG · TEKLİF AL · NUMUNE İSTE · DEMO TALEP ET` (Durst's sticky 4-action bar). Mobile: 2 actions `Teklif Al` + `WhatsApp`, 64 px tall, safe-area padded. |

### 4.4 Ink detail page `/murekkep-sarf/{aile}/{urun}/`

| # | Section | Contents |
|---|---|---|
| 1 | Breadcrumb | 3 levels |
| 2 | Hero (`--paper`) `[magenta]` | Blender-rendered bottle/pouch on `--paper` + right column: family kicker → `<h1>` product name → one-line role (*"Ricoh Gen5/Gen6 kafalar için UV-LED"*) → **changeover badge** → `[ Teklif İsteyin ]` + `Uyumluluk kontrolü` |
| 3 | **Channel strip** | The site's signature component. Real swatches per channel using the exact logo hexes; `W` and `Lak` as outlined/hatched chips; `on-request` channels greyed with a mono note. Per-channel SKU on hover/tap. |
| 4 | Positioning paragraph | 60–90 words, includes `oemEquivalent` explicitly. |
| 5 | Öne çıkan özellikler | 4–7 bullets |
| 6 | Tabs `ÜRÜN AÇIKLAMASI / ÖZELLİKLER VE TEKNİK VERİLER / BELGELER VE İNDİRMELER` | Nazdar's 3-tab split, translated. **No `Yorumlar` tab** — reviews on an industrial ink page read as dropshipping. |
| 7 | Uyumluluk bloku | Three columns: `Uyumlu Baskı Kafaları` · `Doğrulanmış Makineler` (Nazdar's *validated*, not *compatible*) · `OEM Eşdeğeri`. Every machine name links to its PDP. |
| 8 | Spec table | Kürleme (yöntem, doz, dalga boyu, son kürlenme) · Raf ömrü & depolama · Çalışma ortamı · Dış mekân dayanımı **with the scoping clause** · Ambalaj chips. **Never publish viscosity for UV or solvent inks** — real TDS don't, and it exposes the data as fake. |
| 9 | `Uygulanabilir Yüzeyler` | Chips + the mandatory testing caveat sentence. |
| 10 | `Yardımcı Ürünler` | Flush / primer / temizleme kiti cross-sell. |
| 11 | `Belgeler` | TDS (üretici, sürüm, tarih) + **Türkçe GBF** + certificate scans. Certification badges attributed to the manufacturer, never as a Maven badge. |
| 12 | `Yasal Uyarı` | Turkish testing disclaimer, `--muted`, `--step--1`. |
| 13 | `Bu mürekkebi kullanan makineler` | Reverse cross-link cards. |
| 14 | Quote CTA + sticky mobile bar | `Teklif İsteyin` + WhatsApp |

### 4.5 Applications hub `/uygulamalar/` and sector page

**Hub:** H1 `Uygulamalar` → one paragraph → 6 tiles (3:2 duotone, colour on hover) → a
"hangi makine hangi işe" matrix (application × machine family, ✓ marks, links both ways) → CTA band.

**Sector page** (`/uygulamalar/reklam-tabela/`): breadcrumb → H1 → hero image (21:9) → 2 paragraphs
of what the segment actually prints → `Bu işi yapan makineler` (filtered machine cards) →
`Kullanılan mürekkepler` (ink cards) → `Uygulanan malzemeler` (chips) → application photo strip
(8–12 captioned) → `Referans işler` (or omitted if none real) → FAQ → CTA.

Cross-linking is the **three-hop, ink-terminated** Durst journey: sector → machine → compatible ink.

### 4.6 Service page `/teknik-servis/`

| # | Section | Contents |
|---|---|---|
| 1 | Header (`--ink`, dark) `[yellow]` | H1 `Teknik Servis` + one-line promise + `[ Servis Talebi Oluştur ]` + destek hattı + WhatsApp |
| 2 | **Numaralı taahhüt listesi** | 6 items, mono index, each a *number* not an adjective: müdahale süresi (saat), uzaktan destek kanalları, yerinde servis kapsamı, garanti bölünmesi (elektronik 1 yıl / mekanik 2 yıl), yedek parça stok taahhüdü, eğitim (süre sınırı yok). Vague "kaliteli hizmet" copy is the default TR failure mode; numbers are the differentiator. |
| 3 | Hizmetler | 4 blocks: `Ön Keşif ve Kurulum` · `Operatör Eğitimi` · `Periyodik Bakım` · `Yedek Parça`. |
| 4 | **Servis ücret tablosu** | A real `<table>`, not prose: kalem / kapsam / ücret (USD, `KDV hariç`). Publishing this is genuinely differentiating in this market — the reference site buries the same figures in a wall of text under the wrong H1. Gate behind client confirmation (§12). |
| 5 | Kapsama | City list + response commitment per zone. Map is a static SVG of Turkey with served provinces filled `--yellow` — **not** an embedded Google Maps iframe (third-party cookies, KVKK, and 300 KB). |
| 6 | Servis Talep Formu | `Firma*` · `Yetkili*` · `Telefon*` · `E-posta` · `Makine Modeli` (select, populated from the catalogue) · `Seri No` · `Arıza Açıklaması*` · dosya yok (static) · KVKK onayı. |
| 7 | SSS | 6–8 troubleshooting Q&A (`kafa tıkanması`, `banding`, `beyaz çökelmesi`, `encoder hatası`), `FAQPage` JSON-LD — these rank. |
| 8 | Belgeler | link to `/belgeler/` + `/teknik-servis/garanti-kosullari/` |

### 4.7 About page `/kurumsal/`

1. Header (`--paper`) — H1 `Kurumsal`, one-sentence positioning, no stock hero of people.
2. `Ne yapıyoruz` — 3 paragraphs, first person plural, concrete: what we import, what we stock, what we service. No "lider çözüm ortağı" boilerplate.
3. Sayılarla Maven (`--ink`, dark) `[cyan]` — 4 count-ups with real, defensible numbers.
4. `Neyi taahhüt ediyoruz` — 4 short commitments (stock, service, GBF, training).
5. Zaman çizelgesi — a hairline horizontal timeline, mono years. Only if there are ≥4 real milestones.
6. `Markalar ve tedarik` — brand logo strip **with honest wording**: `yetkili distribütör` only where the agreement exists, otherwise `tedarik ediyoruz / stoklarımızda bulunur`.
7. `Referanslar` teaser → `/kurumsal/referanslar/`.
8. `Fuarlar ve Showroom` teaser → `/kurumsal/fuarlar-ve-showroom/` (SIGN İstanbul 23–26 Eylül 2026, İFM; FESPA Eurasia 9–12 Temmuz 2026).
9. Ekip — **omitted until real photography exists.** Never stock people.
10. CTA band.

### 4.8 Contact page `/iletisim/`

1. H1 `İletişim` + one line: what happens after you write (`Mesajınıza aynı iş günü içinde dönüyoruz.`)
2. **Channel grid, 4 cards, phone first:** `Telefon` (tel: link, çalışma saatleri) · `WhatsApp` (deep link) · `E-posta` (single departmental address — never a dump of five personal mailboxes) · `Adres` (full postal + district).
3. Departman yönlendirme: `Satış` / `Teknik Servis` / `Sarf sipariş` / `Muhasebe` — one address each, obfuscated at build time.
4. Genel iletişim formu (§4.9). **No CAPTCHA image** — honeypot only.
5. Konum: static map SVG/PNG + `Yol tarifi al ›` deep link (opens Google/Apple Maps). No embedded iframe.
6. Çalışma saatleri table.
7. TTK identity block (repeat of footer legal band, expanded).
8. `LocalBusiness` + `Organization` JSON-LD.

### 4.9 Form field sets (locked)

**Teklif Al** — phone before e-mail; TR B2B buyers give a phone more readily than an e-mail.
```
Ad Soyad*          Firma          Telefon*        E-posta
Şehir (select)     İlgilendiğiniz ürün (pre-filled, editable)      Mesaj
☐ KVKK Aydınlatma Metni'ni okudum ve onaylıyorum.*    → [ Gönder ]
+ botcheck honeypot, + hidden redirect=/tesekkurler/
```
Under the button, the line swissQprint is missing: *"Formu gönderdiğinizde 1 iş günü içinde bir
satış mühendisimiz sizi arar. Acil ihtiyaçlar için WhatsApp daha hızlıdır."*

**Servis Talebi** — §4.6.6. **Numune Talebi** — `Ad Soyad*`, `Firma*`, `Telefon*`, `Adres*`,
`Hangi makine/mürekkep`, `Basılacak malzeme`, KVKK.

**WhatsApp deep link** (build-time generated per product — fix both of the reference site's bugs):
```
https://wa.me/905XXXXXXXXX?text= + encodeURIComponent(
  `Merhaba, ${product.name} hakkında teklif almak istiyorum. ${absoluteUrl}`)
```
`?text=` not `&text=`, and an absolute URL that actually resolves.

---

## 5. DATA MODEL

TypeScript shapes below are the source of truth. They are expressed in the Astro content collection
as Zod (`src/content.config.ts`); the runtime data lives as **one YAML file per product**.

### 5.1 Shared primitives

```ts
export const LOCALES = ['tr', 'en'] as const;
export type Locale = (typeof LOCALES)[number];

/** Every human-facing string. z.record(z.enum(LOCALES), …) makes a missing locale a BUILD ERROR. */
export type I18n<T = string> = Record<Locale, T>;

/** Value + unit stored separately so TR renders m²/sa and EN renders m²/h. */
export interface Measure {
  value: number | [number, number];   // scalar or min–max range
  unit: UnitKey;                      // resolved through the unit dictionary (§5.6)
  note?: I18n;                        // e.g. "beyaz ile" / "with white"
}

export interface Dimensions { w: number; d: number; h: number; unit: 'mm' | 'cm' | 'm'; }

export interface DocRef {
  kind: 'catalog' | 'datasheet' | 'tds' | 'gbf' | 'certificate' | 'install-checklist';
  lang: Locale | 'en';
  file: string;        // /docs/…  — ungated, direct
  bytes: number;       // rendered as "PDF · 2,4 MB"
  version?: string;
  date?: string;       // ISO yyyy-mm
}

export interface MediaRef { src: ImageMetadata; alt: I18n; caption?: I18n; kind: 'machine' | 'application' | 'detail'; }
```

### 5.2 `Machine`

```ts
export interface Machine {
  /* identity */
  sku: string;                    // "MF-2513-R8"     — URL-safe
  model: string;                  // "Maven MF-2513 R8"  (lang="en" in TR pages, §6.2)
  family: MachineFamily;          // enum, drives category page + accent
  tier: 'entry' | 'mid' | 'upper-mid' | 'industrial' | 'flagship';   // copy register only, never rendered
  order: number;
  featured: boolean;
  status: 'active' | 'on-request' | 'discontinued';

  /* commerce */
  price: null | { amount: number; currency: 'USD' | 'EUR' | 'TRY'; vatIncluded: false };
  // machines are ALWAYS null → the price slot renders "Fiyat için teklif alın"
  leadTimeWeeks?: [number, number];

  /* headline — the 4 oversized metrics on the PDP hero */
  headline: Array<{ key: SpecKey; }>;   // exactly 4, resolved from specs

  /* printheads — first-class, filterable, and in the card title */
  printhead: { brand: HeadBrand; model: string; count: number | [number, number]; dropSizePl?: number | [number, number] };
  headOptions?: Array<Machine['printhead']>;   // one chassis, selectable heads (how TR sells them)

  /* specs — locale-neutral numbers; labels come from the dictionary (§5.6) */
  specs: Partial<Record<SpecKey, Measure | string | number | boolean | Dimensions>>;
  speedModes: Array<{ pass: 4 | 6 | 8 | 2 | 3; value: number | [number, number]; unit: 'm2/h'; mode?: I18n }>;
  // ALWAYS an array. A single "speed" field is the #1 tell of a fabricated catalogue.

  /* system components — DTF shaker, calender. NOT separate SKUs. */
  components?: Array<{ sku: string; name: I18n; role: I18n; specs: Partial<Record<SpecKey, Measure | string>> }>;

  /* relations */
  compatibleInks: string[];       // ink slugs — drives the cross-sell module both ways
  applications: ApplicationKey[];
  substrates: SubstrateKey[];
  siblings: string[];             // for the comparison table
  rip: string[];                  // "ONYX" | "Caldera" | "SAi Flexi" | "Maintop 6.1" | …

  /* site-prep honesty block */
  installation: {
    powerPhase: '1F' | '3F';
    floorAreaM2: number;
    ceilingHeightM: number;
    cratedDimensions: Dimensions;
    ventilationRequired: boolean;
    compressedAir?: string;        // "6 bar, 200 L/dk"
    notIncluded: I18n<string[]>;   // nakliye, forklift, elektrik altyapısı, …
  };

  /* media */
  gallery: MediaRef[];            // ≥4
  model3d?: { glb: string; poster: string; hotspots: Hotspot[]; triangles: number; bytes: number };
  hotspot2d?: { image: MediaRef; points: Array<{ x: number; y: number; label: I18n; body: I18n }> };
  videos?: Array<{ url: string; title: I18n; thumb: MediaRef }>;
  documents: DocRef[];

  /* prose — one block per locale; missing a locale fails the build */
  i18n: I18n<{
    name: string;                 // display name if it differs per locale
    tagline: string;              // benefit pair, comma-joined (TR convention)
    summary: string;              // 60–90 words, NOT 110
    features: Array<{ term: string; body: string }>;   // 3–5, `term` = an ownable technology name
    faq: Array<{ q: string; a: string }>;              // 3–6
    alternateName?: string[];     // "makinası", "ekosolvent" aliases → JSON-LD only, never visible
  }>;
}

export type MachineFamily =
  | 'uv-flatbed' | 'uv-hybrid' | 'eco-solvent' | 'dtf' | 'sublimation' | 'uv-dtf' | 'cutting';
export type HeadBrand = 'ricoh' | 'konica' | 'epson' | 'kyocera' | 'toshiba' | 'starfire';
```

### 5.3 `Ink`

```ts
export interface Ink {
  slug: string;                   // "mi-210-uv-led-r"
  sku: string;                    // "MI-210"
  series: string;                 // "Maven MI-210 UV-LED R"
  family: InkFamily;
  type: 'ink' | 'auxiliary' | 'powder' | 'film' | 'printhead' | 'spare';
  order: number;

  oemEquivalent: string[];        // load-bearing in this market
  changeover: 'switch-and-print' | 'switch-and-swap' | 'switch-and-match';

  channels: Array<{
    code: 'C'|'M'|'Y'|'K'|'Lc'|'Lm'|'Lk'|'W'|'Or'|'Gr'|'Vt'|'Cl'|'Opt'|'Ov'|'FlP'|'FlB'|'FlY'|'FlG';
    name: I18n;                   // "Camgöbeği" / "Cyan";  Cl = "Lak" / "Varnish"
    sku: string;
    hex: string;                  // swatch for the channel strip
    availability: 'stock' | 'on-request';
  }>;

  packaging: Array<{ format: 'bottle'|'bag'|'bag-in-box'|'cartridge'|'pouch'|'drum'; volume: number; unit: 'ml'|'L'|'kg'; note?: I18n }>;

  compat: {
    printheads: string[];         // "Ricoh Gen5", "Epson i3200-U1", "Konica KM1024i"  → FIRST-CLASS FACET
    dropSizePl?: [number, number];
    machines: string[];           // Maven SKUs → generates /uyumluluk/
    thirdPartyPrinters?: string[];// "Mimaki JFX200", "Roland VG3-640" — text only, no logos
    chipIncluded: boolean;
  };

  specs: {
    cure: { method: 'uv-hg'|'uv-led'|'heat'|'calender'|'air'|'none'; doseMjCm2?: [number, number];
            intensityMwCm2?: number; wavelengthNm?: number; postCureHours?: number;
            transferTempC?: [number, number]; transferSeconds?: [number, number]; fixationC?: number };
    shelfLifeMonths: number;              // 12 default · sublimation 15 · DTF white 6
    shelfLifeNote?: I18n;
    storageTempC: [number, number];
    operatingTempC?: [number, number];
    operatingHumidityPct?: [number, number];
    outdoorDurabilityMonths?: number;
    outdoorDurabilityNote: I18n;          // MANDATORY when the above is set: "dikey maruziyet, Orta Avrupa iklimi"
    // aqueous / DTF / textile ONLY — never publish these for UV or solvent:
    viscosityCps?: { value: number; tolerance: number; atC: number };
    surfaceTensionDyn?: { value: number; tolerance: number };
    ph?: { value: number; tolerance: number };
    particleSizeNm?: [number, number];
    fastness?: Array<{ standard: string; result: string }>;   // "EN ISO 105-B02", "≥4"
  };

  substrates: SubstrateKey[];
  applications: ApplicationKey[];
  certifications: Array<{ mark: 'greenguard-gold'|'eco-passport'|'zdhc'|'en-71-3'|'reach'|'iso-9001';
                          issuedTo: string }>;   // ALWAYS the manufacturer, never "Maven"
  documents: DocRef[];                            // must include one { kind:'gbf', lang:'tr' }
  ancillaries: string[];                          // flush, primer, cleaning kit

  price: null | { amount: number; currency: 'USD'; vatIncluded: false };
  // consumables MAY carry a USD price with a visible "KDV hariç" label — that is TR market normal.

  i18n: I18n<{
    name: string;
    role: string;                 // "Ricoh Gen5/Gen6 kafalar için UV-LED"
    summary: string;
    features: string[];           // 4–7
    disclaimer: string;           // the testing caveat, in Turkish, on every ink page
    faq?: Array<{ q: string; a: string }>;
  }>;
}

export type InkFamily =
  | 'uv' | 'uv-led' | 'uv-dtf' | 'eco-solvent' | 'solvent'
  | 'sublimation' | 'dtf' | 'textile-pigment' | 'auxiliary';
```

### 5.4 `Application`

```ts
export interface Application {
  key: ApplicationKey;            // 'signage' | 'packaging' | 'interior' | 'industrial' | 'textile' | 'vehicle'
  slug: I18n;                     // { tr: 'reklam-tabela', en: 'signage-advertising' }
  order: number;
  hero: MediaRef;                 // 21:9 desktop / 4:5 mobile crop
  gallery: MediaRef[];            // 8–12, captioned "UV Cam Kapı Baskı" pattern
  machines: string[];             // machine SKUs
  inks: string[];                 // ink slugs
  substrates: SubstrateKey[];
  cases?: Array<{ slug: string; outcome: I18n; result: I18n; image: MediaRef }>;  // outcome-led headlines
  i18n: I18n<{
    name: string;                 // "Reklam ve Tabela"
    kicker: string;               // action phrase: "Şehirde görün"
    intro: string;                // 2 paragraphs
    jobs: string[];               // what this segment actually prints
    faq: Array<{ q: string; a: string }>;
  }>;
}
```

### 5.5 `SiteConfig` (`src/config/site.ts` — single source of truth, no hard-coded strings anywhere)

```ts
export interface SiteConfig {
  brand: { name: 'Maven'; legalName: string; foundedYear: number };
  url: 'https://maven.com.tr';           // update at domain purchase
  defaultLocale: 'tr';
  locales: ['tr', 'en'];

  contact: {
    phone:      { display: I18n; e164: string };   // TR "0212 XXX XX XX" / EN "+90 212 XXX XX XX"
    mobile?:    { display: I18n; e164: string };
    whatsapp:   { e164: string; prefill: I18n };   // "905XXXXXXXXX"
    email:      { general: string; sales: string; service: string; supplies: string; accounting: string };
    fax?: null;                                    // deliberately null — fax as a channel is a 2026 tell
    address: { street: string; district: string; city: string; postalCode: string; country: 'TR';
               geo: { lat: number; lng: number }; mapsUrl: string };
    hours: Array<{ days: I18n; open: string; close: string }>;
  };

  legal: {                                // TTK m.39/2 — required in the footer
    tradeName: string; mersis: string; taxOffice: string; taxNumber: string; tradeRegistryNo: string;
    kepAddress?: string;
  };

  social: { instagram?: string; linkedin?: string; youtube?: string; facebook?: string };
  // Only ship the ones that exist. An empty social icon row is worse than none.

  forms: { provider: 'web3forms'; accessKey: string; redirect: I18n };  // key is public-safe by design

  commitments: {                          // rendered on /teknik-servis/ and the homepage proof strip
    responseHours: number; warrantyElectronicMonths: number; warrantyMechanicalMonths: number;
    onSiteCities: string[]; installationsCount: number; yearsInBusiness: number;
  };

  analytics: null;                        // NULL. Zero non-essential cookies → no consent banner (§11.4)
}
```

### 5.6 Spec dictionary — the TR/EN label table

This is the i18n dictionary for `SpecKey`. Turkish labels are taken verbatim from live TR dealer
sites so the site's vocabulary matches what a buyer already reads elsewhere (tracks 01, 04, 05).

| `SpecKey` | TR label | EN label | Unit (TR / EN) | Group |
|---|---|---|---|---|
| `printArea` | Baskı Alanı | Print Area | mm × mm | Baskı |
| `printWidth` | Baskı Genişliği | Print Width | mm | Baskı |
| `mediaWidth` | Maks. Malzeme Genişliği | Max Media Width | mm | Baskı |
| `mediaHeight` | Baskı Yüksekliği | Max Media Height | mm | Baskı |
| `mediaThickness` | Malzeme Kalınlığı | Media Thickness | mm | Baskı |
| `mediaWeight` | Maks. Malzeme Ağırlığı | Max Media Weight | kg/m² | Baskı |
| `resolution` | Baskı Çözünürlüğü | Print Resolution | dpi | Baskı |
| `speedModes` | Baskı Hızı | Print Speed | m²/sa · m²/h | Baskı |
| `passModes` | Baskı Modları | Print Modes | pass | Baskı |
| `dropSize` | Damla Hacmi | Drop Volume | pL | Baskı |
| `printHead` | Baskı Kafası | Print Head | — | Kafa & Mürekkep |
| `headCount` | Kafa Sayısı | Head Count | adet · pcs | Kafa & Mürekkep |
| `headOptions` | Kafa Seçenekleri | Printhead Options | — | Kafa & Mürekkep |
| `colors` | Renk Skalası | Ink Channels | — | Kafa & Mürekkep |
| `inkType` | Mürekkep Tipi | Ink Type | — | Kafa & Mürekkep |
| `inkSupply` | Mürekkep Besleme | Ink Supply | — | Kafa & Mürekkep |
| `inkCapacity` | Boya Kapasitesi | Ink Capacity | ml · L | Kafa & Mürekkep |
| `inkConsumption` | Boya Tüketimi | Ink Consumption | ml/m² | Kafa & Mürekkep |
| `whiteCirculation` | Beyaz Mürekkep Sirkülasyonu | White Ink Circulation | var/yok · yes/no | Kafa & Mürekkep |
| `table` | Tabla | Table / Bed | — | Mekanik |
| `vacuumZones` | Vakum Bölgesi | Vacuum Zones | adet · zones | Mekanik |
| `feed` | Malzeme Besleme Sistemi | Media Feed System | — | Mekanik |
| `takeUp` | Sarma Sistemi | Take-up System | — | Mekanik |
| `curing` | Kurutma / Kürleme | Curing / Drying | — | Mekanik |
| `heaters` | Isıtıcı Sistemi | Heating System | — | Mekanik |
| `heightSensor` | Yükseklik Sensörü | Media Height Sensor | — | Mekanik |
| `antiCollision` | Kafa Çarpışma Sensörü | Head Anti-Collision | — | Mekanik |
| `capping` | Kafa Koruma / Cap Sistemi | Capping Station | — | Mekanik |
| `cleaning` | Kafa Temizleme | Head Cleaning | — | Mekanik |
| `cuttingArea` | Kesim Alanı | Cutting Area | mm × mm | Kesim |
| `cuttingSpeed` | Maks. Kesim Hızı | Max Cutting Speed | mm/s | Kesim |
| `cuttingForce` | Kesim Basıncı | Cutting Force | gf · N | Kesim |
| `cuttingAccuracy` | Kesim Hassasiyeti | Cutting Accuracy | mm | Kesim |
| `cuttingTools` | Kesim Takımı | Tool Modules | — | Kesim |
| `cutFormats` | Kesim Formatları | Cut File Formats | — | Kesim |
| `cutMaterials` | Kesim Malzemeleri | Cuttable Materials | — | Kesim |
| `powerSupply` | Güç Kaynağı | Power Supply | V / Hz / faz · phase | Elektrik & Ortam |
| `power` | Güç Tüketimi | Power Consumption | kW | Elektrik & Ortam |
| `current` | Akım | Current | A | Elektrik & Ortam |
| `compressedAir` | Basınçlı Hava | Compressed Air | bar · L/dk | Elektrik & Ortam |
| `environment` | Çalışma Ortamı | Operating Environment | °C / % BN · %RH | Elektrik & Ortam |
| `tempGradient` | Sıcaklık Değişim Limiti | Max Temperature Gradient | °C/sa · °C/h | Elektrik & Ortam |
| `noise` | Gürültü Seviyesi | Acoustic Noise | dB(A) | Elektrik & Ortam |
| `rip` | RIP Yazılımı | RIP Software | — | Yazılım & Bağlantı |
| `fileFormats` | Desteklenen Formatlar | Supported File Formats | — | Yazılım & Bağlantı |
| `interface` | Bağlantı | Interface | — | Yazılım & Bağlantı |
| `dimensions` | Makine Ölçüleri | Dimensions (W × D × H) | mm | Fiziksel |
| `cratedDimensions` | Paket Ölçüleri | Crated Dimensions | mm | Fiziksel |
| `weight` | Ağırlık | Weight | kg | Fiziksel |

**Ink spec labels:**

| Key | TR | EN | Unit |
|---|---|---|---|
| `chemistry` | Kimya | Chemistry | — |
| `cureMethod` | Kürleme Yöntemi | Curing Method | — |
| `cureDose` | Kürleme Dozu | Cure Dose | mJ/cm² |
| `cureIntensity` | Kürleme Şiddeti | Cure Intensity | mW/cm² |
| `wavelength` | Dalga Boyu | Wavelength | nm |
| `postCure` | Son Kürlenme Süresi | Post-Cure Time | saat · h |
| `transferTemp` | Transfer Sıcaklığı | Transfer Temperature | °C |
| `fixation` | Fiksaj | Fixation | °C / s |
| `channels` | Renk Kanalları | Colour Channels | — |
| `packaging` | Ambalaj | Packaging | — |
| `printheads` | Uyumlu Baskı Kafaları | Compatible Printheads | — |
| `machines` | Doğrulanmış Makineler | Validated Equipment | — |
| `oemEquivalent` | OEM Eşdeğeri | OEM Equivalent | — |
| `chipIncluded` | Çip Dahil | Chip Included | var/yok |
| `changeover` | Geçiş Sınıfı | Changeover Class | — |
| `shelfLife` | Raf Ömrü | Shelf Life | ay · months |
| `storageTemp` | Depolama Sıcaklığı | Storage Temperature | °C |
| `outdoorDurability` | Dış Mekân Dayanımı | Outdoor Durability | ay · months |
| `substrates` | Uygulanabilir Yüzeyler | Substrates | — |
| `viscosity` | Viskozite | Viscosity | cps @ °C |
| `surfaceTension` | Yüzey Gerilimi | Surface Tension | din/cm · dyn/cm |
| `ph` | pH | pH | — |
| `fastness` | Haslık | Fastness | — |
| `certifications` | Sertifikalar | Certifications | — |

**Number formatting:** Turkish uses `.` for thousands and `,` for decimals — `1.440 dpi`, `3,2 m`,
`0,25 s`. Format every number through `Intl.NumberFormat(locale)`, never a hand-rolled regex.

**Alias handling:** `makinası`, `ekosolvent`, `sublimasyon`, `boya` live **only** in
`i18n.tr.alternateName[]`, `alt` text and FAQ sentences → `Product.alternateName` in JSON-LD.
House style in visible copy: **makine** (not makina) · **mürekkep** in headings, **boya** allowed in
body/FAQ · **eko solvent** (two words) · **süblimasyon** (with ü). Never two variants in one sentence.

---

## 6. DESIGN SYSTEM

### 6.1 Typefaces — final

| Role | Family | Source | Weights / axes | Turkish |
|---|---|---|---|---|
| Display + body | **Archivo** (variable) | Google Fonts, SIL OFL | `wght 100–900`, `wdth 62–125` | ✅ complete (cmap-verified, all 18 TR codepoints) |
| Spec tables, eyebrows, model codes, counters | **IBM Plex Mono** (static) | Google Fonts, SIL OFL | **400 + 500 only** (no variable version exists) | ✅ complete |

**Two families total.** Archivo's `wdth` axis gives condensed-industrial headlines from a single
file, which is the cheapest route to a distinctive voice; Plex Mono carries engineering-documentation
pedigree without cosplay. **Rejected:** Inter (exhausted default), Poppins/Montserrat (template
tell), Geist (reads "AI startup"), Space Grotesk (quirky `g`/`ı` fights a technical register).

**Self-hosted, subsetted — never hotlink `fonts.googleapis.com`** (critical-path cost + KVKK exposure).

```bash
pyftsubset "Archivo[wdth,wght].ttf" \
  --output-file=archivo-var.woff2 --flavor=woff2 \
  --layout-features="kern,liga,calt,locl,case,tnum,frac" \
  --unicodes="U+0000-00FF,U+0100-024F,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20A0-20AB,U+20AC,U+2122,U+2212,U+2215" \
  --no-hinting --desubroutinize
```

`latin` **+ `latin-ext` is non-negotiable**: `İ` (U+0130), `ğ/Ğ` (U+011F/011E) and `ş/Ş`
(U+015F/015E) are **not** in the `latin` subset. Only `ı` (U+0131) is, which is why the bug survives
casual review. `locl` carries Turkish `i/ı` forms; `case` fixes punctuation in all-caps labels;
`tnum` gives tabular figures for spec tables.

Preload **exactly two files** (Archivo variable + Plex Mono 400). Do not preload Plex Mono 500.
Ship the metric-matched fallback `@font-face` (`size-adjust:97%; ascent-override:92%;
descent-override:24%`) so the swap does not reflow.

### 6.2 Turkish casing — the two rules that will otherwise break every label

1. `<html lang="tr">` on TR pages, `lang="en"` on EN pages, swapped by the locale switcher.
   With the wrong `lang`, `text-transform:uppercase` renders `ISTANBUL` instead of `İSTANBUL` —
   **every all-caps label on the site is misspelled**.
2. Inside a TR page, Latin brand names and model codes **must** carry `lang="en"`, or
   `DIGITAL`→`DİGİTAL`, `PRINT`→`PRİNT`, `MAVEN MF-2513`→ fine, but `EPSON i3200` → `EPSON İ3200`.

```html
<p class="eyebrow" lang="en">UV FLATBED</p>
<p class="eyebrow">makine ailesi</p>   <!-- → MAKİNE AİLESİ -->
```

Also: `hyphens: auto` with `lang="tr"` (agglutinative words overflow narrow columns), and design
every card/button/nav item against the **longest Turkish string** — TR copy runs 15–20% longer than EN.

### 6.3 Colour tokens — final, measured

The brand mark already ships with its own process colours (`brand/maven-logo.svg`). **Those are the
tokens** — the site must match the logo, not a generic SWOP swatch. All ratios below were computed
in this session from the WCAG 2.x relative-luminance formula.

```css
:root{
  /* ---- Structure: 92% of every viewport ---- */
  --ink:        #0B0B0C;   /* near-black. NOT #000 — pure black flares on OLED. 19.67 on paper */
  --paper:      #FFFFFF;
  --bone:       #F2F1ED;   /* warm off-white alternate light ground. 17.41 vs ink */
  --graphite:   #16171A;   /* raised panel on dark — only 1.10 vs ink, MUST be delimited by a rule */
  --rule:       #E3E1DC;   /* hairline on light */
  --rule-dark:  #26272B;   /* hairline on dark */
  --muted:      #5A5F66;   /* secondary text on light   — 6.43 ✅ AA */
  --muted-dark: #9BA1A9;   /* secondary text on dark    — 7.56 ✅ AAA */

  /* ---- Process accents: the logo's own values ---- */
  --cyan:       #0081D2;   /* 4.14 on paper (UI/large only) · 4.75 on ink ✅ AA text */
  --magenta:    #E30161;   /* 4.73 on paper ✅ AA text · 4.16 on ink (UI/large only) */
  --yellow:     #FFE305;   /* 1.29 on paper ❌ NEVER text on light · 15.22 on ink ✅ AAA */

  /* ---- Accent text variants for LIGHT grounds (links, inline emphasis) ---- */
  --cyan-ink:    #005A93;  /* 7.28 ✅ AAA on paper */
  --magenta-ink: #9E0043;  /* 8.28 ✅ AAA on paper */
  /* There is no usable yellow text colour. On light grounds yellow is a MARK only. */

  /* ---- Accent text variants for DARK grounds (when 4.75/4.16 is too tight) ---- */
  --cyan-lit:    #3FA0DD;  /* 6.82 ✅ AA on ink */
  --magenta-lit: #EA4088;  /* 5.23 ✅ AA on ink */

  /* ---- Semantic ---- */
  --accent:     var(--cyan);      /* per-section override, see §6.4 */
  --focus:      var(--cyan);
  --success:    #1B7F4B;
  --warning:    #B25A00;
  --danger:     #B3121B;
}
```

**The decisive insight: the CMYK trio is a dark-background palette.** Yellow scores 1.29 on white
and 15.22 on near-black. That is not a limitation — it is the reason dark sections exist.

### 6.4 Colour usage rules (enforce in review)

| Share of any viewport | Element |
|---|---|
| ~92% | `--ink` / `--paper` / `--bone` / `--muted` / rules |
| ~6% | Exactly **one** process accent, chosen per section |
| ~2% | The full CMYK trio together — logo pixel cluster only, plus at most one hero moment per page |

1. **One accent per section. Never two.** Section rotation is a wayfinding system:
   **cyan = Makineler · magenta = Mürekkep & Sarf · yellow = Teknik Servis.**
   `Uygulamalar` inherits the accent of the family it showcases; the hub is neutral.
2. **On light grounds accents are never text.** They are a 2 px underline sweep, a 4 px section rule,
   a 12 px logo square, a chart bar, a hover fill. Links use `--cyan-ink` / `--magenta-ink`.
3. **On dark grounds accents may be text** — this is where the brand shouts.
4. **Yellow always carries `--ink` on it, never white.**
5. **No gradients, no colour-tinted shadows, no glassmorphism.** Ink is flat.
6. `--graphite` on `--ink` is 1.10:1 — a dark panel is invisible by fill alone and must be delimited
   by a `--rule-dark` hairline.

### 6.5 Focus states

`--cyan` at 4.14 on white clears WCAG 2.2 SC 1.4.11 (3:1 for UI) but not by much on `--bone` (3.66).
Use the two-tone ring so correctness never depends on the ground:

```css
:where(a,button,input,select,textarea,summary,[tabindex]):focus-visible{
  outline: 2px solid var(--ink);
  outline-offset: 2px;
  box-shadow: 0 0 0 4px var(--cyan);
}
.on-dark :where(a,button,summary,[tabindex]):focus-visible{
  outline-color: var(--paper);
}
```
`:focus-visible`, never `:focus`. Never `outline:none` without a replacement.

### 6.6 Type scale (fluid, `clamp()`, no breakpoint jumps)

```css
:root{
  --step--2: clamp(0.69rem, 0.67rem + 0.11vw, 0.75rem);  /* 11→12  mono micro-labels */
  --step--1: clamp(0.83rem, 0.79rem + 0.20vw, 0.94rem);  /* 13→15  captions, spec cells */
  --step-0 : clamp(1.00rem, 0.94rem + 0.31vw, 1.19rem);  /* 16→19  BODY */
  --step-1 : clamp(1.20rem, 1.10rem + 0.50vw, 1.58rem);  /* 19→25  lead paragraph */
  --step-2 : clamp(1.44rem, 1.28rem + 0.80vw, 2.11rem);  /* 23→34  h3 */
  --step-3 : clamp(1.73rem, 1.47rem + 1.30vw, 2.81rem);  /* 28→45  h2, hero metrics */
  --step-4 : clamp(2.07rem, 1.66rem + 2.10vw, 3.75rem);  /* 33→60  h1 */
  --step-5 : clamp(2.49rem, 1.83rem + 3.30vw, 5.00rem);  /* 40→80  hero statement */
  --step-6 : clamp(2.99rem, 1.90rem + 5.40vw, 6.67rem);  /* 48→107 marquee / big number */
}
```

Body lands at **19 px desktop** — deliberately above the 16 px B2B default. Oversized body copy on a
white ground is a large part of why a page reads confident.

| Role | Size | Weight / width | Tracking | Leading |
|---|---|---|---|---|
| Hero statement | `--step-5/6` | `wght 600`, `wdth 82` | `-0.03em` | `0.95` |
| H1 | `--step-4` | `wght 600`, `wdth 88` | `-0.025em` | `1.02` |
| H2 | `--step-3` | `wght 600` | `-0.02em` | `1.08` |
| H3 | `--step-2` | `wght 500` | `-0.015em` | `1.15` |
| Lead | `--step-1` | `wght 400` | `-0.01em` | `1.45` |
| Body | `--step-0` | `wght 400` | `0` | `1.6` |
| Spec cell | `--step--1` | mono 400 | `0` | `1.5` |
| Eyebrow / micro-label | `--step--2` | **mono 500** | `+0.14em` | `1` |
| Button label | `--step--1` | `wght 500` | `+0.02em` | `1` |

**Mono is used in exactly four places** and nowhere else: eyebrows/section micro-labels, spec-table
values and units, model/SKU codes, numeric counters. `font-variant-numeric: tabular-nums` on every
spec table and count-up. `text-wrap: balance` on h1–h3, `text-wrap: pretty` on paragraphs.
Measure capped at `68ch`.

### 6.7 Spacing, radii, borders, shadows

```css
:root{
  --sp-1:4px;   --sp-2:8px;   --sp-3:12px;  --sp-4:16px;  --sp-5:24px;  --sp-6:32px;
  --sp-7:48px;  --sp-8:64px;  --sp-9:96px;  --sp-10:128px; --sp-11:160px; --sp-12:200px;

  --radius: 0;                        /* ZERO, site-wide. Machines are extruded aluminium. */
  --border: 1px;                      /* the only border width, except accent rules at 2px/4px */
  --gutter: clamp(16px, 2vw, 32px);
  --page-margin: clamp(20px, 5vw, 80px);
  --container: 1440px;
  --measure: 68ch;
}
```

Section padding: `padding-block: clamp(var(--sp-9), 12vh, var(--sp-12))` → 96 px mobile to 200 px
desktop. **Generous section padding is the cheapest luxury signal there is**; cheap B2B sites use 48 px.

**Shadow policy: there are no box-shadows on this site.** The single exception is the focus ring.
Elevation is expressed by a ground change (`--paper` → `--bone` → `--ink`) and 1 px rules. Hard edges
at every section boundary — never a gradient fade.

### 6.8 Grid & breakpoints

| Breakpoint | Columns | Notes |
|---|---|---|
| `< 640px` | 4 | single-column cards, sticky bottom action bar |
| `640–1023px` | 6 | 2-up cards |
| `≥ 1024px` | 12 | 3-up cards, hanging label column |
| `≥ 1440px` | 12, container capped | margins absorb the excess; full-bleed sections still bleed |

```css
--bp-sm: 640px; --bp-md: 1024px; --bp-lg: 1280px; --bp-xl: 1440px;
```

**Asymmetry is the whole game.** Mono section label in columns **1–2**, content in **4–12** — the
hanging left-margin label column does more for "engineered" than any animation. Use **subgrid** for
card internals (Baseline widely available 2026-03-15) so titles/specs/CTAs align across unequal
cards, and **container queries** (Baseline 2025-08-14) so one product card works in a 3-up grid, a
2-up rail and a full-width feature.

### 6.9 Light/dark section rhythm

Dark is **punctuation**, roughly 1 dark per 3–4 light — never a zebra.

| Section type | Ground |
|---|---|
| Hero, product categories, PDP hero | `--paper` |
| Applications, references, alternating bands | `--bone` |
| **Technical / stats / capability, service commitments** | **`--ink`** |
| **Closing CTA band + footer (seamless, no seam rule)** | **`--ink`** |

### 6.10 Imagery treatment

One pipeline for every photograph, or five photographers look like a ransom note:
`grayscale(1) contrast(1.12) brightness(0.97)` base grade + duotone (dark colour in `screen`, light
in `multiply`) + a single SVG `feTurbulence` grain at `opacity ≤ 0.06` with `stitchTiles='stitch'`.
**Three crop ratios only: 21:9 hero (4:5 on mobile), 3:2 card, 4:5 inset**, plus 32:9 for texture
bands. **Colour arrives only on hover** (`filter` transition 500 ms) — which makes the CMYK identity
read as a deliberate signal rather than decoration.

Sourcing: Pexels ~65% / Unsplash free tier ~25% / Pixabay ink context ~10%. Openverse and Wikimedia
Commons are **excluded** from the shipping set. Blocklist all 17 `@ai25studioai` Pexels IDs
(6620963–6621001, 4348164). **Zero third-party manufacturer marks anywhere, at any size, including
out-of-focus background machines and control-panel splash screens.** No stock people presented as
Maven staff; no faces on `/kurumsal/` or `/iletisim/`. Ink and consumable product shots are
**rendered in Blender with Maven-designed labels**, not sourced — wide-format ink does not exist in
free stock at all. Every asset gets a record in `assets/originals/MANIFEST.json` with the four-point
clearance check (licence tier, AI provenance, third-party marks, identifiable faces).

---

## 7. MOTION SPEC

### 7.1 Tokens

```css
:root{
  --d-instant: 90ms;  --d-fast: 160ms;  --d-base: 240ms;
  --d-slow:  380ms;   --d-slower: 560ms; --d-page: 480ms;

  --e-out:      cubic-bezier(0.16, 1, 0.30, 1);    /* HOUSE CURVE — sharp out, long settle */
  --e-out-soft: cubic-bezier(0.25, 1, 0.50, 1);
  --e-in-out:   cubic-bezier(0.76, 0, 0.24, 1);    /* symmetrical: page + overlay */
  --e-standard: cubic-bezier(0.20, 0, 0.00, 1);    /* Material 3 emphasized */
  --e-accel:    cubic-bezier(0.30, 0, 0.80, 0.15); /* exits */
  --e-linear:   linear;                             /* marquee only */
}
```

**No springs, no overshoot, no bounce anywhere on this site.** A machine that overshoots is a broken
machine. Nothing exceeds its endpoint.

### 7.2 The catalogue (18 interactions — build all of them, nothing else)

| # | Name | Trigger | Property | Duration | Easing | Reduced-motion fallback |
|---|---|---|---|---|---|---|
| 1 | **Sliding underline** ★ | `:hover` / `:focus-visible` on nav + inline links | `transform: scaleX()` + `transform-origin` swap | 320 ms | `--e-out` | Underline appears instantly at full width |
| 2 | Button line sweep | `:hover`/`:focus-visible` on `.btn` | `scaleX()` on `::before` + `color` | 420 / 160 ms | `--e-out` | Instant background + colour swap |
| 3 | Button arrow shift | `:hover` on CTA | `translateX(0 → 4px)` on `::after` | 240 ms | `--e-out` | Static arrow |
| 4 | Image clip reveal | Enters viewport, once | `clip-path: inset(0 0 100% 0 → 0)` + inner `scale(1.06 → 1)` | 900 / 1200 ms | `--e-out` | Visible at rest, 200 ms opacity only |
| 5 | Staggered line reveal | Heading enters viewport | per-line `translateY(105% → 0)` in an `overflow:hidden` mask | 640 ms, stagger 70 ms | `--e-out` | All lines visible, single 200 ms fade |
| 6 | Rule draw-in | Section enters viewport | `scaleX(0 → 1)`, `transform-origin:left` | 560 ms | `--e-out` | Full-width immediately |
| 7 | Number count-up | Stat block enters viewport | `rAF` + `Intl.NumberFormat('tr-TR')` | 1400 ms | JS `1-(1-t)³` | Final value written immediately |
| 8 | Marquee | Autoplay | `translateX(0 → -50%)` on a duplicated track | 36 s/loop | `--e-linear` | Animation stopped; becomes a scroll-snapped strip. **Visible pause control ships regardless** (WCAG 2.2.2). |
| 9 | Sticky condensing header | Sentinel `IntersectionObserver` at 120 px | `height 88→60px`, logo `scale(1→0.82)`, `border-bottom-color` | 280 ms | `--e-standard` | Condensed state applied instantly |
| 10 | Header hide-on-scroll-down | Scroll direction change | `translateY(0 → -100%)` | 320 ms | `--e-in-out` | Disabled; header pinned |
| 11 | Cursor-adaptive hover | `(hover:hover) and (pointer:fine)` only | lerped `translate3d`, label `opacity`/`scale` | lerp 0.15 / 200 ms | `--e-out` | Not mounted at all |
| 12 | Card hover | `:hover` on product card | `border-color`, thumb `scale(1→1.03)`, accent rule `scaleX(0→1)` | 300 ms | `--e-out` | `border-color` only |
| 13 | Page transition | Same-origin navigation | `@view-transition{navigation:auto}` cross-fade + `translateY(12px)`; shared-element morph on product thumb | 480 ms | `--e-in-out` | `navigation: none` |
| 14 | Gallery slide | Arrows, drag, arrow keys | native `scroll-snap` + `scrollTo({behavior:'smooth'})` | ~500 ms | native | `behavior:'auto'`, snap retained |
| 15 | Accordion | `<summary>` click | `grid-template-rows: 0fr → 1fr`, chevron `rotate(0→180deg)` | 340 ms | `--e-standard` | Instant, no rotation |
| 16 | Mega-menu open | Nav hover/click, desktop | `clip-path: inset(0 0 100% 0 → 0)` + item stagger 40 ms | 380 ms | `--e-out` | Instant, no stagger |
| 17 | 3D idle → engage | Model loaded / pointerdown | `auto-rotate` at 0.0015 rad/frame → damped orbit | continuous | linear / damping 0.08 | **Auto-rotation off**, static until dragged |
| 18 | Section index tick | Section enters viewport | mono index `01 → 02`, `opacity` + `translateY(6px)` | 240 ms | `--e-out` | Value swaps, no motion |

### 7.3 The signature interaction — exact implementation

The client asked for *"hover kayan buton çizgileri"*. The whole trick: **`transform-origin` is
swapped but never transitioned**, so the line enters from the left and exits to the right,
reading as one continuous line travelling through the word.

```css
.link{ position:relative; text-decoration:none; color:var(--ink); }
.link::after{
  content:""; position:absolute; left:0; right:0; bottom:-3px; height:1px;
  background:currentColor;
  transform:scaleX(0);
  transform-origin:right center;                 /* governs the EXIT */
  transition:transform var(--d-base) var(--e-out);
}
.link:hover::after,
.link:focus-visible::after{
  transform:scaleX(1);
  transform-origin:left center;                  /* governs the ENTER */
}
.link--accent::after{ height:2px; bottom:-4px; background:var(--accent); }
```

Never animate `width` (layout thrash). Never transition `transform-origin` (destroys the effect).
The button sweep is the same mechanic scaled to a box, with `overflow:hidden; isolation:isolate` and
`::before { inset:0; z-index:-1; background:var(--ink) }`.

### 7.4 Scroll reveals — progressive enhancement only

Scroll-driven animations are Chrome 115+ / Safari 26+, **no Firefox**. Ship them behind
`@supports (animation-timeline: view())` with an `IntersectionObserver` fallback that reveals
**once** and `unobserve`s. **Never** drive a reveal from a `scroll` event listener — that is the
single biggest cause of janky "premium" sites.

### 7.5 Reduced motion — selective, not a sledgehammer

`*{animation:none!important}` is wrong: it breaks loading states and any state conveyed only by
motion. Opacity fades are not vestibular triggers; travel, scale, parallax and rotation are.

```css
@media (prefers-reduced-motion: reduce){
  *,*::before,*::after{
    animation-duration:.01ms !important; animation-iteration-count:1 !important;
    transition-duration:.01ms !important; scroll-behavior:auto !important;
  }
  .reveal,.stagger-line{
    animation:none !important; transform:none !important; clip-path:none !important;
    opacity:1 !important; transition:opacity 200ms linear !important;
  }
  .marquee__track{ animation:none !important; }
  .marquee{ overflow-x:auto; scroll-snap-type:x mandatory; }
  @view-transition { navigation: none; }
}
```

Mirror in JS and **respond to live changes** (`matchMedia(...).addEventListener('change', …)`) —
users toggle it mid-session.

---

## 8. 3D SPEC

### 8.1 Decisions

| Question | Decision | One-line justification |
|---|---|---|
| Library | **`<model-viewer>` 4.3.1**, self-hosted in `public/vendor/` | The 282 KB br vs 128 KB br gap is deferred behind an intersection observer and only ever paid by a user who opted in; it buys AR, poster/lazy-reveal, keyboard orbit, ARIA labelling and native Draco/meshopt/KTX2 decoding — none of which we then maintain. |
| three.js | **Not installed** | model-viewer pins `three: ^0.183.0`; two copies cannot dedupe. Switch to raw three.js only if the design later demands exploded views or custom shaders. |
| Hosting | **Component inside the main repo**, never a separate subdomain | Roland's standalone virtual showroom is already dead at both its EU and US URLs. |
| Which machines | **4 get a real glTF.** Everything else gets the 2D hotspot explorer. | A Blender model is days of work per machine; the HP-style 2D hotspot diagram is 80% of the explanatory payoff at zero load cost. |

**glTF models (v1):** `MF-2513 R8` (the volume flagship) · `MH-3200 R12` (the widest, most
impressive) · `MD-600 A4` (a *system* — printer + shaker, best demonstrates why 3D helps) ·
`MC-300 U1` (small, desk-scale, the fastest to model and the best AR candidate).

**2D hotspot explorer** for the other 8, built from a Blender-rendered still on `--paper` with
absolutely-positioned numbered hotspots + a detail panel. Same `hotspots[]` data shape, same labels.

### 8.2 What the Blender model must contain to read as real

Built with the existing repo pipeline (`blender/lib/{build,shading,studio}.py`, Blender **5.2 LTS**,
glTF add-on 5.3.18). The `machine_kit()` material set already ships the right palette
(`INK #131518`, `GRAPHITE #4A4F55`, `SILVER #B9BCBF`, `WARN_YELLOW #FFE305`, `CYAN #0081D2`).

**Mandatory, or it reads as CG instantly:**
1. **Bevelled edges everywhere** — 3–5 mm chamfer, 2 segments. An unbevelled edge catches no
   highlight. `build.add_bevel()` exists precisely so this cannot be forgotten.
2. **Visible panel gaps** — 2–3 mm recessed seams between sheet-metal panels, not painted lines.
3. **Fastener rows** — `build.bolt_row()` along structural joins. Real machines are bolted.
4. **Extrusion profile beams** for the gantry (`build.profile_beam()`), not solid boxes.
5. **A real control station** — angled HMI screen with an emissive UI material, an e-stop mushroom in
   safety red, and a status LED strip.
6. **The functional bits a printer actually has:** carriage + printhead block, linear rail and drag
   chain, LED-UV lamp housings, zoned vacuum bed with a perforation texture, ink tanks/bottles with
   translucent level windows, waste bottle, take-up/feed rollers, castors or levelling feet.
7. **Safety yellow** on moving-part warnings and the bed edge — the machine's own accent, and it is
   the brand yellow, which is why the render sits with the site.
8. **Grounded**, with contact shadow. Floating machines look like clip art.
9. **Scale-true in metres.** The viewer's AR mode places a real-size object in the customer's
   workshop; a wrong-scale model is worse than no AR.
10. **Maven wordmark decal** on the front panel, from `brand/maven-logo-mono.svg` — no third-party
    marks anywhere.

**Hotspot naming discipline** (copy Durst's: glTF node names are the semantic hotspot keys):

| Blender object name | Hotspot key | TR label | EN label |
|---|---|---|---|
| `PRINTHEAD` | `printhead` | Baskı kafası bloğu | Printhead carriage |
| `UV_LAMP_L` / `UV_LAMP_R` | `curing` | LED UV kürleme | LED UV curing |
| `VACUUM_BED` | `bed` | Bölgesel vakumlu tabla | Zoned vacuum table |
| `INK_TANKS` | `ink_supply` | Mürekkep besleme | Ink supply system |
| `GANTRY` | `gantry` | Lineer köprü | Linear gantry |
| `HMI_SCREEN` | `control` | Kontrol paneli | Control station |
| `ROLLERS_FRONT` / `ROLLERS_REAR` | `media_feed` | Malzeme besleme | Media feed |
| `CAP_STATION` | `capping` | Kafa koruma istasyonu | Capping station |
| `SHAKER` (MD-600 only) | `shaker` | Toz serpme ünitesi | Powder shaker |
| `E_STOP` | `safety` | Acil stop | Emergency stop |

Rule: **the object name in Blender is the hotspot key in JS.** No mapping table in code.

### 8.3 Export pipeline (scripted, reproducible)

```bash
# 1. Blender: GLB, selected objects only, +Y up, modifiers applied, COMPRESSION OFF,
#    no lights, no cameras, no animations, images AUTO @ q75
blender --background --factory-startup --python blender/export_machine.py -- --machine mf-2513-r8

# 2. Always inspect before optimising
gltf-transform inspect out/mf-2513-r8.glb

# 3. Optimise — meshopt (29 KB decoder, stays quantized on the GPU) + KTX2 ETC1S
gltf-transform optimize out/mf-2513-r8.glb public/models/mf-2513-r8.v1.glb \
  --compress meshopt --texture-compress ktx2 --texture-size 1024 --simplify false

# 4. Verify
gltf-transform inspect public/models/mf-2513-r8.v1.glb
```

`--simplify false` is deliberate: auto-decimation artefacts crisp machined panel edges. Decimate in
Blender where you can see it. Draco is rejected in favour of meshopt (190 KB WASM vs 29 KB, slower
decode, decompresses to full-size GPU buffers).

**Budget, per machine — hard gate in CI:**

| Metric | Target | Hard ceiling |
|---|---|---|
| GLB total | **1.5–2.5 MB** | 4 MB |
| Triangles | 150k–300k | 500k |
| Textures | 1024², ETC1S (UASTC for normal maps only) | 2048² hero only |
| Materials / draw calls | ≤ 10 | 20 |
| Poster (WebP) | 40–80 KB | 100 KB |

If the optimised GLB exceeds 4 MB the CAD wasn't retopologised — fix the model, not the compression.
Version in the filename (`.v1.glb`), immutable cache, and **do not let Vercel re-gzip `.glb`** (already
compressed).

### 8.4 In-browser viewer UX

```html
<model-viewer
  src="/models/mf-2513-r8.v1.glb"
  poster="/models/mf-2513-r8-poster.webp"
  alt="Maven MF-2513 R8 UV flatbed baskı makinesi — 360° model"
  camera-controls
  touch-action="pan-y"
  loading="lazy" reveal="interaction"
  environment-image="neutral" exposure="1.0" shadow-intensity="1"
  camera-orbit="35deg 75deg auto" field-of-view="30deg"
  min-camera-orbit="auto 15deg auto" max-camera-orbit="auto 95deg auto"
  interaction-prompt="none"
  ar ar-modes="webxr scene-viewer quick-look" ar-scale="fixed"
  data-lazy
  style="width:100%;aspect-ratio:4/3;--poster-color:transparent">

  <button slot="hotspot-printhead" data-position="…" data-normal="…"
          class="hotspot" aria-label="Baskı kafası bloğu">
    <span class="hotspot__dot"></span>
    <span class="hotspot__label" lang="tr">Baskı kafası bloğu</span>
  </button>
  …
  <div slot="progress-bar" class="mv-progress"><span></span><em>%0</em></div>
</model-viewer>
```

**Controls:** left-drag orbit · scroll/pinch zoom · **pan disabled** (a marketing viewer that lets
you lose the object is broken) · double-tap or `Sıfırla` button resets the camera · full keyboard
orbit (native) · a single in-canvas option toggle where the machine has one (`RULO KİTİ` on the
hybrid, `TOZ SERPME ÜNİTESİ` on the DTF system) — Durst's one-button configurator is the whole idea
and it is very effective.

**Loading state:** a **real progress readout**, not a bare spinner — Durst's weakest point.
`<div slot="progress-bar">` renders a 2 px `--accent` rule filling left-to-right plus a mono `%`.
The poster is a Blender still of the same machine at the same camera angle, so the reveal is a
crossfade into an identical frame, not a jump.

**Mobile:** `touch-action="pan-y"` is mandatory — without it the model captures vertical swipes and
the page cannot be scrolled past. On `< 640px` the 3D tab is **not preselected**; the gallery is,
and a `360° İNCELE` chip switches to it. AR button shown only when
`model-viewer.canActivateAR === true`.

**Fallbacks, in order:**
1. No WebGL / context creation failure → `<model-viewer>` never mounts; the poster `<img>` plus the
   2D hotspot explorer is rendered in its place. Detect with a one-line
   `document.createElement('canvas').getContext('webgl2')` probe before appending the script.
2. JS disabled → the `<noscript>` path renders the poster image and the gallery. The 3D tab is
   generated by JS and simply never appears.
3. `prefers-reduced-motion: reduce` → `auto-rotate` never enabled; model static until dragged.
4. Save-Data / `connection.effectiveType` of `2g`/`slow-2g` → the 3D tab renders as a button
   labelled `3D modeli yükle (2,1 MB)` requiring an explicit tap.

**Never** let the glTF compete with the LCP image: the script and the model load only on
`IntersectionObserver` with `rootMargin: '200px'`, bound to `astro:page-load` so it survives
client-side navigation.

---

## 9. TECH STACK

### 9.1 Versions (verified 2026-07-28, not from memory)

```jsonc
{
  "engines": { "node": ">=22.12.0" },
  "dependencies": {
    "astro": "7.1.5",
    "@astrojs/sitemap": "3.7.3",
    "sharp": "0.35.3"
  },
  "devDependencies": {
    "@gltf-transform/cli": "4.4.2",
    "typescript": "^5.9",
    "prettier": "^3.6",
    "prettier-plugin-astro": "^0.14"
  }
}
```

Vendored, self-hosted (never a CDN): `public/vendor/model-viewer-4.3.1.min.js`.
Toolchain: Blender **5.2 LTS** + glTF add-on 5.3.18, Python venv already at `tools/.venv`.

**Deliberately not installed:** `@astrojs/vercel` (a static site needs no adapter — Astro's own docs
say so, and adding it converts free build-time Sharp output into metered Vercel image
transformations) · `three` (model-viewer bundles its own, pinned) · `@astrojs/markdown-remark`
(Sätteri is sufficient) · `swiper` / `keen-slider` (see §9.5) · any analytics SDK · any chat SDK.

**Escape hatch, pinned if needed:** `embla-carousel@8.6.0` (7.3 KB br) only if the design later
requires infinite loop or free-drag momentum. Do **not** install `embla-carousel-accessibility` —
its `latest` tag is a release candidate against a stable core.

### 9.2 `astro.config.mjs` (the four settings that are painful to retrofit)

```js
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://maven.com.tr',
  output: 'static',
  trailingSlash: 'always',            // must agree with vercel.json
  build: { format: 'directory' },
  compressHTML: true,                 // opt OUT of Astro 7's new 'jsx' whitespace stripping —
                                      // it eats the space in `<a>x</a> <a>y</a>` and this design is typography-led
  image: {
    layout: 'constrained',
    responsiveStyles: true,           // DEFAULT IS FALSE — without it `layout` emits srcset but no responsive layout
    objectFit: 'cover',
  },
  i18n: {
    defaultLocale: 'tr',
    locales: ['tr', 'en'],
    routing: { prefixDefaultLocale: false, redirectToDefaultLocale: false, fallbackType: 'redirect' },
  },
  integrations: [sitemap({ i18n: { defaultLocale: 'tr', locales: { tr: 'tr-TR', en: 'en-US' } } })],
});
```

**Astro 6/7 traps that will break copied code:** `src/content/config.ts` is dead (it is
`src/content.config.ts` and every collection needs a `loader`); `<ViewTransitions />` is dead (it is
`<ClientRouter />`); the Rust compiler rejects unclosed tags and invalid nesting; `src/fetch.ts` is a
reserved filename. Treat every StackOverflow answer older than 2026 as wrong.

### 9.3 Folder structure

```
meric-baski/
├─ astro.config.mjs
├─ vercel.json                      # cache headers for /_astro/, /img/, /models/, /docs/
├─ package.json
├─ tsconfig.json
├─ public/
│  ├─ fonts/                        # archivo-var.woff2, ibm-plex-mono-{400,500}.woff2  (subsetted)
│  ├─ img/                          # sharp-generated AVIF/WebP/JPEG ladders (§6.10)
│  ├─ models/                       # mf-2513-r8.v1.glb + posters
│  ├─ docs/                         # ungated PDFs: catalogs, TDS, GBF, certificates
│  ├─ vendor/model-viewer-4.3.1.min.js
│  ├─ robots.txt
│  └─ favicon.svg                   # brand/favicon.svg
├─ src/
│  ├─ config/site.ts                # SiteConfig (§5.5) — the only place a phone number exists
│  ├─ i18n/
│  │  ├─ routes.ts                  # ROUTES map + localizePath() + alternatesFor()  (§2.4)
│  │  ├─ ui.ts                      # UI strings: {tr,en} per key
│  │  └─ specs.ts                   # SpecKey → {tr,en,unit,group}  (§5.6)
│  ├─ content.config.ts             # Zod schemas, glob() loaders
│  ├─ content/
│  │  ├─ machines/*.yaml            # 12 files
│  │  ├─ inks/*.yaml                # 10 + auxiliaries
│  │  ├─ applications/*.yaml        # 6
│  │  └─ insights/*.md              # blog
│  ├─ layouts/
│  │  ├─ Base.astro                 # <head>, hreflang, JSON-LD, ClientRouter, skip link
│  │  ├─ MachinePage.astro
│  │  ├─ InkPage.astro
│  │  ├─ CategoryPage.astro
│  │  └─ ContentPage.astro
│  ├─ components/
│  │  ├─ nav/{Header,MegaMenu,LangSwitch,MobileNav,StickyActions}.astro
│  │  ├─ product/{SpecTable,SpeedTable,HeroMetrics,ChannelStrip,ChangeoverBadge,
│  │  │           CompareTable,CompatibilityMatrix,ProductCard,SubstrateChips}.astro
│  │  ├─ media/{Gallery,ModelViewer,Hotspot2D,Figure,Marquee}.astro
│  │  ├─ form/{QuoteForm,ServiceForm,SampleForm,WhatsAppButton,Field}.astro
│  │  └─ ui/{Button,Link,Eyebrow,Accordion,Breadcrumb,Rule,CountUp,Reveal}.astro
│  ├─ pages/
│  │  ├─ index.astro                        # TR home
│  │  ├─ [locale]/index.astro               # EN home
│  │  ├─ makineler/index.astro              # TR routes = literal segments
│  │  ├─ makineler/[kategori]/index.astro
│  │  ├─ makineler/[kategori]/[sku]/index.astro
│  │  ├─ makineler/[kategori]/[sku]/teknik-ozellikler.astro
│  │  ├─ murekkep-sarf/…  uygulamalar/…  teknik-servis/…  kurumsal/…
│  │  ├─ [locale]/machines/[category]/[sku]/index.astro   # EN routes = locale param
│  │  ├─ [locale]/inks-supplies/…  [locale]/applications/…
│  │  └─ 404.astro
│  ├─ scripts/                      # gallery.js, reveal.js, header.js, modelviewer.js, form.js, cursor.js
│  └─ styles/                       # tokens.css, base.css, type.css, layout.css, motion.css
├─ blender/                         # EXISTING — lib/{build,shading,studio}.py + per-machine builders
│  ├─ lib/…
│  └─ machines/{mf-2513-r8,mh-3200-r12,md-600-a4,mc-300-u1}.py
├─ tools/
│  ├─ build-images.mjs              # sharp ladder generator
│  └─ check-budgets.mjs             # CI gate: GLB size, image weight, JS/CSS budget
├─ assets/originals/                # source photography + MANIFEST.json (clearance record)
└─ docs/research/                   # tracks 01–08 + this file
```

**Page architecture: one dynamic route per page with locale as a param** —
`src/pages/makineler/[kategori]/[sku]/index.astro` (TR, hardcodes `locale = 'tr'`, three lines) and
`src/pages/[locale]/machines/[category]/[sku]/index.astro` (EN, `getStaticPaths` returns
`locale: 'en'` only), **both rendering the same `MachinePage.astro` layout** so the page structure
exists exactly once. `[locale]` is safe next to literal segments because a static build emits only
the paths `getStaticPaths()` returns, so `/makineler/` can never be captured by `/[locale]/`.
Rejected: folder-per-locale — 48 pages × N locales of hand-synced `.astro` files is exactly the
graveyard we are escaping.

### 9.4 The two guarantees that make multilingual safe

1. `ROUTES` typed `satisfies Record<string, Record<Locale, string>>` — **add `'ar'` to `LOCALES` and
   TypeScript errors on every untranslated route.**
2. `i18n: z.record(z.enum(LOCALES), localized)` in the content schema — verified against `zod@4.4.3`:
   a missing locale key fails with `invalid_type`. **`astro build` refuses to produce a page with a
   missing translation.** That turns "add a locale" from a discipline problem into a compile error.

### 9.5 Component-level decisions

| Concern | Decision | Justification |
|---|---|---|
| Carousel | **CSS `scroll-snap` + ~50 lines of progressive-enhancement JS** | Native touch momentum, free RTL via `direction:rtl` (required by "scale to more locales"), degrades to a scrollable image strip when JS fails, and no library to rot. |
| Auto-rotate galleries | **Never** | Removes the entire W3C APG rotation-control requirement and auto-rotating photos while someone reads spec numbers is user-hostile. |
| Page transitions | `<ClientRouter />` + `@view-transition { navigation: auto }` | SPA-grade transitions with zero framework; Firefox silently does a normal navigation. |
| DOM init | **Bind everything to `astro:page-load`, never `DOMContentLoaded`** | `DOMContentLoaded` fires once — carousels and the 3D viewer die on the second client-side navigation. |
| Forms | **Web3Forms**, `redirect` hidden field + `botcheck` honeypot, upgraded to `fetch` by PE | 250 submissions/mo free (5× Formspree), the access key is documented as public-safe, and the `redirect` field makes it work with JS disabled. |
| Map | Static SVG + deep link | An embedded Maps iframe costs ~300 KB, third-party cookies and a KVKK problem. |
| Chat | **WhatsApp deep link only, no SDK** | A chat SDK kills Lighthouse and creates a KVKK exposure for zero gain in this market. |
| Analytics | **None in v1** | Zero non-essential cookies → çerez aydınlatma metni required, consent banner *not* (§11.4). Revisit only with client sign-off. |

### 9.6 `vercel.json`

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "trailingSlash": true,
  "cleanUrls": false,
  "headers": [
    { "source": "/_astro/(.*)", "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }] },
    { "source": "/img/(.*)",    "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }] },
    { "source": "/models/(.*)", "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }] },
    { "source": "/fonts/(.*)",  "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }] },
    { "source": "/(.*)", "headers": [
      { "key": "X-Content-Type-Options", "value": "nosniff" },
      { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
      { "key": "Permissions-Policy", "value": "geolocation=(), microphone=(), camera=(), interest-cohort=()" }
    ]}
  ]
}
```
Immutable assets are versioned by filename — **replace an image or a model by renaming, never by
overwriting bytes.** That is the contract `immutable` implies.

---

## 10. CONTENT & SEO

### 10.1 Meta patterns

| Page type | `<title>` (≤60 chars) | `<meta description>` (≤155 chars) |
|---|---|---|
| Home TR | `Dijital Baskı Makineleri ve Mürekkep \| Maven` | `UV flatbed, hibrit, eko solvent, DTF ve süblimasyon baskı makineleri, mürekkep ve sarf malzemeleri, 24 saat içinde teknik servis. Teklif alın.` |
| Machine category | `{Kategori} — Modeller ve Fiyat Teklifi \| Maven` | `{N} model {kategori}. {Genişlik aralığı}, {kafa markaları} baskı kafası. Teknik özellikler, uyumlu mürekkepler ve fiyat teklifi.` |
| Machine PDP | `{Model} — {format} {kategori} \| Maven` | `{Model}: {spec1}, {spec2}, {spec3}. Teknik özellikler, uyumlu mürekkepler, kurulum gereksinimleri ve fiyat teklifi.` |
| Spec sub-route | `{Model} Teknik Özellikleri \| Maven` | `{Model} tam teknik özellik listesi: baskı, kafa, mekanik, elektrik ve fiziksel değerler.` |
| Ink category | `{Aile} — Uyumlu Makineler ve Fiyat \| Maven` | `{Aile} çeşitleri, uyumlu baskı kafaları ve makineler, ambalaj seçenekleri, Türkçe GBF. Teklif isteyin.` |
| Ink PDP | `{Ürün} — {kafa/makine} uyumlu \| Maven` | `{Ürün}: {kanal seti}, {ambalaj}, {kürleme}. Uyumlu kafalar: {…}. TDS ve Türkçe Güvenlik Bilgi Formu.` |
| Application | `{Sektör} için Dijital Baskı Çözümleri \| Maven` | `{Sektör} işlerinde kullanılan makineler, mürekkepler ve malzemeler. Uygulama örnekleri ve teklif.` |
| Service | `Teknik Servis ve Yedek Parça \| Maven` | `24 saat içinde müdahale, {N} şehirde yerinde servis, yedek parça stoğu, operatör eğitimi. Servis talebi oluşturun.` |
| Contact | `İletişim \| Maven` | `{İl} showroom ve teknik servis merkezi. Telefon, WhatsApp, adres ve çalışma saatleri.` |

Rules: the brand suffix is `| Maven`, once. Never `Maven` twice in one title. Never "Ana Sayfa" or
"Home" as a title. Every page gets a unique OG image — generated at build from a template
(model name + one hero metric + logo on `--ink`) at 1200×630, because the reference site's total
absence of `og:` tags means every WhatsApp share renders a blank card.

### 10.2 hreflang & canonicals

Generated from the locale registry on **every** page, never hard-coded:
```html
<link rel="alternate" hreflang="tr" href="https://maven.com.tr/makineler/uv-flatbed-baski-makineleri/">
<link rel="alternate" hreflang="en" href="https://maven.com.tr/en/machines/uv-flatbed-printers/">
<link rel="alternate" hreflang="x-default" href="https://maven.com.tr/makineler/uv-flatbed-baski-makineleri/">
<link rel="canonical" href="…self…">
```
`x-default` → the Turkish URL. Adding `ar`/`ru` is a config change, not a template edit.
(Canon Europe ships zero hreflang on its Arizona pages — that is a defect, not a pattern to copy.)

### 10.3 Structured data

| Schema type | Where |
|---|---|
| `Organization` | every page (in `Base.astro`), with `logo`, `sameAs[]`, `contactPoint` |
| `LocalBusiness` | `/iletisim/` — with `geo`, `openingHoursSpecification`, `areaServed` |
| `BreadcrumbList` | every page below root |
| `Product` | machine + ink PDPs — `brand`, `model`, `sku`, `image[]`, `description`, `additionalProperty[]` (one `PropertyValue` per spec, using the §5.6 dictionary), `alternateName[]` (the TR aliases), `isRelatedTo[]` (compatible inks/machines). **No `offers`** — we sell nothing online and a fabricated price is worse than none. |
| `ItemList` | category pages (ordered product list) |
| `FAQPage` | category, PDP, service, application pages — the on-page FAQ block exists for the rich result |
| `BlogPosting` | `/bilgi/{slug}/` |
| `WebSite` | root only |

### 10.4 sitemap & robots

`@astrojs/sitemap` with the i18n block emits `sitemap-index.xml` + per-locale entries with correct
`xhtml:link` alternates. `public/robots.txt`:
```
User-agent: *
Allow: /
Sitemap: https://maven.com.tr/sitemap-index.xml
```
No `Disallow` beyond `/tesekkurler/` (thin, duplicate across forms).

### 10.5 Turkish keyword targets → page map

Derived from *observed targeting* on live TR dealer pages (real titles/H1s/slugs), not from measured
volume — validate in Search Console after 60 days. Intent: **C** commercial · **I** informational ·
**L** local.

| Keyword (TR) | Intent | Target page |
|---|---|---|
| dijital baskı makinesi / makinası | C | `/makineler/` |
| dijital baskı makinası fiyatları | C | `/makineler/` §"fiyatları hakkında" |
| uv baskı makinesi (+ fiyatları) | C | `/makineler/uv-flatbed-baski-makineleri/` |
| uv flatbed baskı makinesi | C | same |
| hibrit uv baskı makinesi | C | `/makineler/uv-hibrit-baski-makineleri/` |
| rulodan ruloya baskı makinesi | C | same |
| eko solvent baskı makinesi / ekosolvent | C | `/makineler/eko-solvent-baski-makineleri/` |
| solvent baskı makinesi | C | same (section) |
| dtf baskı makinesi / dtf yazıcı fiyatları | C | `/makineler/dtf-baski-sistemleri/` |
| süblimasyon baskı makinesi | C | `/makineler/sublimasyon-baski-sistemleri/` |
| tekstil baskı makinesi | C | same + `/uygulamalar/tekstil-promosyon/` |
| bayrak baskı makinesi | C | `/makineler/sublimasyon-baski-sistemleri/` (section) |
| uv dtf baskı makinesi / kristal etiket | C | `/makineler/uv-dtf-kristal-etiket-makineleri/` |
| kesici plotter / folyo kesme makinesi | C | `/makineler/kesim-makineleri/` |
| ikinci el dijital baskı makinesi / 2. el uv | C | `/ikinci-el/` |
| dijital baskı mürekkebi / dijital baskı boyası | C | `/murekkep-sarf/` |
| uv mürekkep fiyatları | C | `/murekkep-sarf/uv-murekkep/` |
| eko solvent mürekkep fiyat | C | `/murekkep-sarf/eko-solvent-murekkep/` |
| dtf mürekkep / dtf pigment mürekkep | C | `/murekkep-sarf/dtf-pigment-murekkep/` |
| baskı kafası fiyatları | C | `/murekkep-sarf/baski-kafalari/` |
| epson i3200 / xp600 / dx5 baskı kafası | C+B | `/murekkep-sarf/baski-kafalari/` (per-head sections) |
| konica 1024i baskı kafası | C+B | same |
| dtf transfer tozu / dtf pet film | C | `/murekkep-sarf/yardimci-malzemeler/` |
| dijital baskı yedek parça | C | `/murekkep-sarf/yedek-parca/` |
| dijital baskı makinesi teknik servis | C | `/teknik-servis/` |
| baskı kafası tamiri | C | `/teknik-servis/` (section) |
| {şehir} dijital baskı teknik servis | L | `/teknik-servis/` coverage section — **city landing pages only if the copy genuinely differs** (response time, nearest depot); otherwise thin doorway pages hurt |
| uv baskı nedir | I | `/bilgi/uv-baski-nedir/` |
| dtf baskı nedir / nasıl yapılır | I | `/bilgi/dtf-baski-nedir/` |
| rip yazılımı nedir | I | `/bilgi/rip-yazilimi-nedir/` |
| eko solvent ile uv baskı farkı | I | `/bilgi/eko-solvent-mi-uv-mu/` — **the biggest under-served TR query in the niche** |
| dtf mi süblimasyon mu | I | `/bilgi/dtf-mi-sublimasyon-mu/` |
| mürekkep tüketimi hesaplama | I | `/bilgi/murekkep-maliyeti-hesaplayici/` — a static JS calculator (m²/gün × ml/m² → aylık maliyet). No dealer builds this; buyers screenshot it. |

**The "fiyat/fiyatları" modifier is unavoidable and we publish no machine prices.** Serve the intent
instead: every category page carries an H2 named `{Kategori} fiyatları hakkında` explaining what
drives price, ending in `Teklif Al`. That single section is the highest-leverage SEO surface on the site.

### 10.6 Editorial rules

- Category pages carry **300–600 words of real copy**, not a bare grid. They are the money pages, not
  the homepage.
- Product summary is **60–90 words**, three bullets — not the reference site's 110-word single paragraph.
- Taglines are benefit pairs joined by a comma (`Her yüzeye yüksek kalite, her sektöre çözüm`) — the
  established TR pattern.
- Application captions follow `UV + {malzeme/nesne} + Baskı` (`UV Cam Kapı Baskı`, `Metal Etiket UV Baskı`).
- **Never** write `yetkili distribütör` / `Türkiye distribütörü` for a brand unless the agreement
  exists; use `tedarik ediyoruz` / `stoklarımızda bulunur`. The market notices.
- Every durability/lifetime claim is **scoped** (`dikey maruziyet, Orta Avrupa iklimi`). An unscoped
  "5 yıl dış mekân" reads as fake to anyone who has read a real TDS.
- Certification badges are attributed to the manufacturer, never rendered as a Maven mark.

---

## 11. QUALITY BARS

### 11.1 Performance budget (CI-gated by `tools/check-budgets.mjs`)

| Metric | Budget | Hard fail |
|---|---|---|
| **LCP** (mobile, p75, 4G) | ≤ **2.0 s** | 2.5 s |
| **CLS** | ≤ 0.02 | 0.05 |
| **INP** | ≤ 150 ms | 200 ms |
| HTML per page (uncompressed) | ≤ 35 KB | 60 KB |
| CSS total (brotli) | ≤ 18 KB | 25 KB |
| JS on a non-3D page (brotli) | ≤ 12 KB | 20 KB |
| Fonts (2 files, subsetted) | ≤ 85 KB | 110 KB |
| Images above the fold | ≤ 250 KB | 350 KB |
| Hero @1920w AVIF | ≤ 160 KB | 200 KB |
| GLB per machine | ≤ 2.5 MB | 4 MB |
| Third-party requests | **0** | 0 |
| Lighthouse mobile | Perf ≥ 98 · A11y 100 · Best Practices 100 · SEO 100 | Perf 95 |

Reference point: cmykreklam's homepage ships **~3.3 MB of imagery with zero `lazy`, zero `srcset`,
zero WebP/AVIF**. We beat it by an order of magnitude, on purpose.

**Delivery rules:** AVIF → WebP → JPEG `<picture>`; six hero widths (640/960/1280/1600/1920/2560);
hero preloaded as an `<img>` with `fetchpriority="high"` (**never** a CSS `background-image` — it is
discovered late and cannot be preloaded); explicit `width`/`height` on every `<img>` matching the
delivered crop ratio; `loading="lazy"` below the fold and never on the LCP image.

### 11.2 Accessibility target

**WCAG 2.2 Level AA, no exceptions.** Specifically enforced:

- Contrast verified per token in §6.3; yellow is never text on a light ground.
- Two-tone `:focus-visible` ring on every interactive element; visible on both grounds.
- One `<h1>` per document, correct heading order, no skipped levels. (The reference site has zero
  `<h1>` on its homepage, the literal word "Ürünler" on every category page, and two `<h1>` on
  product pages — all three are disqualifying.)
- Skip link to `#main` as the first tab stop.
- Carousel: `aria-roledescription="carousel"` + `role="group"` + accessible name; each slide
  `role="group"` + `aria-roledescription="slide"` + `aria-label="3 / 10"`; real `<button>` controls.
  No auto-rotation, therefore no rotation-control requirement.
- Marquee: **visible pause control** — `prefers-reduced-motion` alone does not satisfy WCAG 2.2.2.
- Forms: every input has a `<label>` (never placeholder-as-label), `autocomplete` tokens,
  `inputmode` on tel, errors announced via `role="status" aria-live="polite"`, KVKK checkbox required.
- Touch targets ≥ 44 × 44 px; sticky mobile bar respects `env(safe-area-inset-bottom)`.
- `lang` correct per document **and** on inline foreign strings (§6.2).
- Tested with keyboard only, VoiceOver (iOS Safari) and NVDA (Windows Firefox) before launch.

### 11.3 Browser support

| Tier | Browsers | Guarantee |
|---|---|---|
| **Full** | Chrome/Edge ≥ 120, Firefox ≥ 121, Safari ≥ 17.5, iOS Safari ≥ 17, Samsung Internet ≥ 23 | Everything, including subgrid, container queries, `text-wrap:balance`, `@starting-style`, AVIF |
| **Graceful** | Safari 16.4–17.4, iOS 16.4–16.7, Firefox ESR | AVIF yes; no view transitions, no scroll-driven animations — both are progressive enhancements that degrade to a plain navigation and an IntersectionObserver reveal |
| **Baseline-functional** | Anything with ES2020 modules | Content, navigation, forms and galleries all work; 3D and custom cursor never mount |
| **Not supported** | IE, Opera Mini | — |

Every enhancement is gated: `@supports (animation-timeline: view())`, a WebGL2 probe before the 3D
script, `(hover:hover) and (pointer:fine)` before the custom cursor, and `<noscript>` paths for the
gallery and forms.

### 11.4 Legal & compliance bars (Turkey, non-e-commerce)

**Ship:** `/kvkk-aydinlatma-metni/` · `/cerez-politikasi/` · `/kullanim-kosullari/` · a required
KVKK consent checkbox on every form linking to the aydınlatma metni · the TTK m.39/2 footer identity
block (ticaret unvanı, MERSİS, işletme merkezi, + conventional Vergi Dairesi/VKN).

**Do not ship:** mesafeli satış sözleşmesi, ön bilgilendirme formu, iade/teslimat policies, an ETBİS
badge — none apply to a promotional B2B site with no online sales, and adding them is a tell that
the site was copy-pasted. **This flips the moment a cart or an online-payment link appears.**

**Cookie stance:** ship **zero non-essential cookies**. KVKK Kurul decision **2022/1358**
(23.12.2022) requires opt-in with non-essential cookies off by default and imposed a 300.000 TL fine;
by shipping no analytics we need the çerez aydınlatma metni but **no consent banner and no CMP** —
which also removes a Lighthouse tax and a CLS source. No newsletter in v1 (a newsletter pulls us into
the İYS / ticari elektronik ileti regime).

### 11.5 Anti-pattern list — the explicit ban

Any one of these makes the site look cheap. They are review-blocking.

**Imagery** — stock photos of people in hard hats / shaking hands / pointing at monitors · machines
composited onto gradient backgrounds with drop shadows · mixed treatments (some cut-out, some
photographed, some rendered) in one grid · upscaled low-res vendor JPEGs · **any third-party
manufacturer mark, at any size, including background machines and control-panel splash screens** ·
AI-generated "printing press" stock · stock people captioned as Maven staff.

**Typography** — Poppins/Montserrat/Raleway · centred body paragraphs · `text-transform:uppercase`
with zero tracking · three or more families · **Turkish rendered with fallback-font `ğ ş İ`** ·
**`ISTANBUL` instead of `İSTANBUL`** · `DİGİTAL` / `PRİNT` (English words given Turkish casing).

**Colour & surface** — blue-to-cyan gradient hero · coloured shadows, glow, glassmorphism,
neumorphism · more than one accent in a viewport · yellow text on white · cyan body text on white ·
border-radius anywhere.

**Layout** — everything centred in an 8-column well with 48 px section padding · **the 3-across
"feature card" row with a circular icon, a two-word title and a sentence of filler** (the single most
template-coded pattern in B2B) · auto-advancing hero sliders of near-identical images · cards with
unequal internal alignment · **no spec table.**

**Motion** — spring/bounce easing · `ease-in-out` on everything · 800 ms hover transitions ·
fade-up on every element, re-triggering on re-entry · parallax hero backgrounds · AOS/WOW.js ·
motion with no reduced-motion path · a 3D model that auto-rotates forever and fights the user.

**Content & trust** — "sektörün lider çözüm ortağı" above the fold · fake testimonials or a logo wall
of non-clients · a contact page that is only a form (industrial buyers want a phone number, a
WhatsApp link, an address and a named department) · gated PDF downloads · no lead times, no service
coverage, no pricing *direction* · English-first with a machine-translated Turkish page · a CAPTCHA
image · **fax as a documented support channel** · broken/absent favicon, no OG image, `title` reading
"Home" · publishing viscosity for a UV or solvent ink · an unscoped outdoor-durability claim ·
a GREENGUARD badge on Maven's own lockup · reviews/star ratings on an industrial ink page ·
`m2/s` where `m²/sa` is meant.

**Engineering** — `src/content/config.ts` (dead API) · `<ViewTransitions />` (dead) ·
`outputEncoding` (dead) · binding DOM init to `DOMContentLoaded` · hotlinking Google Fonts or unpkg ·
adding `@astrojs/vercel` to a static build · a `scroll` event listener driving reveals ·
`*{animation:none!important}` as the reduced-motion implementation.

---

## 12. OPEN QUESTIONS FOR THE CLIENT

Ordered by how much they block the build. Items 1–5 block launch; 6–12 block specific sections.

| # | Question | Blocks | Why it cannot be decided without them |
|---|---|---|---|
| 1 | **Legal identity block:** ticaret unvanı, MERSİS no, ticaret sicil no, vergi dairesi + VKN, full registered address, landline(s), WhatsApp Business number, departmental e-mail addresses, KEP (if any). | Footer, `/iletisim/`, JSON-LD, every form | Required by TTK m.39/2 and it is the single cheapest trust signal in the TR market. Placeholders cannot ship. |
| 2 | **Domain and brand name.** Is "Maven" final, and is `maven.com.tr` (or which domain) secured? | `site` config, canonicals, hreflang, OG images, e-mail | Every absolute URL, sitemap entry and share card depends on it. The repo folder is still `meric-baski`. |
| 3 | **Which brands do they actually represent, and at what level?** Per brand: `yetkili distribütör` / `yetkili bayi` / `tedarik ediyoruz`. Any written dealership agreements? | `/kurumsal/`, brand strip, all product copy | Claiming a distributorship that does not exist is a haksız rekabet exposure, and the market notices. It also decides whether the catalogue can name real machines at all. |
| 4 | **Is the 12-machine / 10-ink catalogue placeholder, or does the real line replace it before launch?** If real: we need the model list, spec sheets and photography. | Every product page, the 3D shortlist, the compatibility matrix | The sample data is plausible and internally consistent, but shipping invented SKUs to a live commercial site is a decision only the client makes. |
| 5 | **Service commitments — the real numbers.** Response SLA in hours, warranty split (electronic/mechanical months), which cities get on-site service, spare-parts stock claim, training scope. | `/teknik-servis/`, homepage proof strip, PDP service block | These are the site's main differentiator and they must be commitments the company will honour, not copy. |
| 6 | **Publish the service price table or not?** (e.g. İstanbul/Ankara call-out, other provinces, general maintenance, operator training, software install.) In USD + KDV hariç? | `/teknik-servis/` §4 | Publishing is genuinely differentiating in this market; it is also a commercial commitment. |
| 7 | **Do we hold Turkish GBF (Güvenlik Bilgi Formu) for every chemical we sell, prepared/updated by a certified KDU per KKDİK Annex-18?** | `/belgeler/`, every ink PDP, the strongest ink-side claim on the site | Since 31.12.2023 only a certified KDU may prepare a GBF. If we don't have them we must not claim them — and getting them is the highest-ROI thing the client can do. |
| 8 | **Analytics: accept zero-cookie (no analytics at all), or is GA4 required?** | Cookie banner, CMP, Lighthouse budget, `/cerez-politikasi/` | GA4 forces an opt-in CMP under Kurul 2022/1358, which costs the banner, the CLS and the risk. Cookieless alternatives exist if measurement is essential. |
| 9 | **Is the company subject to bağımsız denetim (TTK m.1524 tescilli internet sitesi)?** And VERBİS: employee count and annual balance-sheet total (exempt under 50 employees **and** under 100M TL). | Extra "Bilgi Toplumu Hizmetleri" section; VERBİS registration | Both are the client's call with their mali müşavir; if m.1524 applies the site needs a whole additional statutory section. |
| 10 | **İkinci el, takas and leasing: do they actually do these?** Which leasing partners, what terms? | `/ikinci-el/`, `/finansman/` | Both pages have real, underserved demand — but only if the offer is real. |
| 11 | **Showroom / demo room:** is there a machine a customer can come and see, and can we print and post samples? | `Demo talep et` and `Numune talebi` CTAs | These are the two highest-intent CTAs in the category; without capacity behind them they generate broken promises. |
| 12 | **Real photography access:** can we shoot the premises, workshop, service vehicle and team? Any existing client references we may name or logo? | `/kurumsal/`, `/iletisim/`, `/kurumsal/referanslar/`, marquee | No stock people may stand in for staff, and a fake logo wall is worse than no logo wall — those sections are cut until real assets exist. |

**Additional smaller decisions we will assume unless told otherwise:** TR is at the site root and EN
at `/en/` · no newsletter in v1 · no price on any machine, USD + `KDV hariç` on consumables where the
client supplies figures · SIGN İstanbul (23–26 Eylül 2026, İFM) is the primary fair credential ·
the third locale, when it comes, is Arabic or Russian (the architecture is ready for both; Arabic
additionally needs the RTL path, which the scroll-snap gallery already gives us for free).

---

*Compiled from tracks 01–08. Every non-obvious number in §6.3 was computed in this session; every
version in §9.1 was verified against the registry or the vendor's own docs on 2026-07-28. Where this
document and a research track disagree, this document wins.*
