# 01 — Reference Site Teardown

**Scope:** primary teardown of `cmykreklam.com` (the site the client pointed at), plus three Turkish
comparables in the same niche. Everything below was fetched live on **2026-07-28** — raw HTML was
downloaded and parsed, not summarised from memory.

**Sources fetched**

| # | Site | What it is | Why included |
|---|---|---|---|
| 1 | [cmykreklam.com](https://www.cmykreklam.com/) | Ankara-based Liyu/Platinum machine dealer, 25 yrs | The client's stated reference |
| 2 | [gurdijital.com](https://www.gurdijital.com/) | İstanbul dealer: machines **+ inks + consumables + service** | Closest match to *our* business model |
| 3 | [lazerpol.com](https://lazerpol.com/) | UV/DTF/laser machine seller, WooCommerce | Shows a spec-table + tab pattern |
| 4 | [csdijital.com](https://www.csdijital.com/) | Ink / printhead / spare-part specialist | Ink taxonomy by printhead |
| 5 | [mimaki.com.tr](https://www.mimaki.com.tr/urunler/) | Mimaki Eurasia (manufacturer, TR) | The "grown-up" taxonomy in this sector |

---

## 1. cmykreklam.com — information architecture

### 1.1 Sitemap (verified against `https://www.cmykreklam.com/sitemap.xml`)

```
/                                                Ana Sayfa            (no <h1> at all)
├── /kurumsal                                    Hakkımızda
├── Medya  (dropdown, parent links to /haberler)
│   ├── /haberler                                Haberler
│   │   └── /haber-detay/<slug>                  news detail  (5 items)
│   └── /showroom                                Fuar ve Showroom
│       └── /showroom/<slug>                     showroom detail (5 items, 2 are test junk:
│                                                 "test6", "baslik-uzun")
├── Ürünler  (dropdown, parent href = /platinum-hybrid  ← broken parent, see §5)
│   ├── /hybrid-baski-makineleri                 Hybrid Baskı Makineleri
│   ├── /flatbed-baski-makineleri                Flatbed Baskı Makineleri
│   ├── /platinum-kesim-makineleri               Platinum Kesim Makineleri
│   ├── /roll-to-roll-baski-makineleri           Roll to Roll Baskı Makineleri
│   ├── /platinum-pack                           Platinum Pack
│   └── /xline-kesim-makineleri                  Xline Kesim Makineleri
│         └── product detail pages live at ROOT level, not nested:
│            /xline-kc-xline-kc
│            /kcxl-yeni-hiz-makinesi-kcxl-uv-flatbed
│            /flatbed-uv-kcb-xline-kcb
│            /platinum-hybrid-q3-2
│            /platinum-qr-5mt
│            /platinum-qcut3521
│            /platinum-qcut-2516
│            /platinum-pack-platinum-pack
│            /platinum-df-plotter
│            /platinum-tekstil-baski-makinesi
│            /platinum-pct-inkjet-printer
│            /pct-led
│            /textil-baski-da-yeni-vizyon-platinum-fh-tekstil
│            /kalite-hiz-ve-ekonomik-xline-solvent-baski-makinesi
│            /sinifinda-en-verimli-xline-solvent-baski-makinesi
│            /xline-hybrid-xline-hybrid-uv-baski-makinesi
│            /xline-kesici-xline-dijital-kesim-makinesi
│            /hepsi-bir-arada-ekonomik-platinum-hybrid-eq3
│            /yuksek-performansli-endustriyel-baski-cozumu-platinum-pct-solvent
│            /guclu-baski-signature-ile-imzalayin-signature-serisi
├── Uygulamalar  (dropdown, parent href = /uygulama/platinum-hybrid ← 404-ish)
│   ├── /uygulama/hybrid-baski-makineleri
│   ├── /uygulama/flatbed-baski-makineleri
│   ├── /uygulama/roll-to-roll-baski-makineleri
│   ├── /uygulama/platinum-kesim-makineleri
│   ├── /uygulama/platinum-pack          ← in sitemap, MISSING from menu
│   └── /uygulama/xline-kesim-makineleri ← in sitemap, MISSING from menu
├── /sektor/<slug>   reklam | ambalaj | mobilya | tekstil | cam
│                    ← reachable only from the homepage tiles, NOT in the top nav
├── /destek                                      Destek  (H1 is wrongly "İletişim")
├── /blog                                        Blog
│   └── /<slug>                                  blog detail (6 posts, root-level slugs)
└── /iletisim                                    İletişim
```

**Exact top-nav labels (from `nav.main-menu` markup):**
`Ana Sayfa` · `Hakkımızda` · `Medya` ▸ (`Haberler`, `Fuar ve Showroom`) · `Ürünler` ▸ (6 categories) ·
`Uygulamalar` ▸ (4 categories) · `Blog` · `Destek` · `İletişim`

**Language:** `<html lang="tr">`. No `hreflang`, no `/en/`, no language switcher. `/en` 301s to `/`.
Interestingly the WhatsApp deep-link text on product pages hard-codes a `/tr/` prefixed URL
(`https://www.cmykreklam.com/tr/kcxl-...`) which **404s** — the CMS once had locale prefixes and the
templates were never cleaned up. Relevant to us: this is exactly the multilingual debt we must avoid.

### 1.2 Product category taxonomy — exact Turkish names

Six families, split by **machine form-factor / technology**, not by application:

| Turkish label (verbatim) | Slug | Members observed |
|---|---|---|
| Hybrid Baskı Makineleri | `/hybrid-baski-makineleri` | PLATINUM HYBRID Q3XL+, PLATINUM HYBRID EQ3, Xline Hybrid |
| Flatbed Baskı Makineleri | `/flatbed-baski-makineleri` | Xline KC, KCXL+ UV FLATBED, Xline KCB |
| Platinum Kesim Makineleri | `/platinum-kesim-makineleri` | PLATINUM Q CUT 3521, PLATINUM Q-CUT 2516, PLATINUM DF PLOTTER |
| Roll to Roll Baskı Makineleri | `/roll-to-roll-baski-makineleri` | Xline Solvent, PLATINUM PCT LED, PLATINUM QR 5mt., Platinum FH Tekstil, Platinum PCT Solvent |
| Platinum Pack | `/platinum-pack` | Platinum Pack (corrugated/packaging single-pass) |
| Xline Kesim Makineleri | `/xline-kesim-makineleri` | Xline Kesici |

Secondary axis — **Sektörler** (5, homepage tiles only, `/sektor/<slug>`):
`Reklam` · `Ambalaj` · `Mobilya` · `Tekstil` · `Cam`.

**Critical gap for us:** cmykreklam sells *only machines*. There is **no ink / consumable / spare-part
category anywhere on the site** — inks appear once, as a news post
(`/haber-detay/platinum-uv-baski-murekkepleri-greenguard-altin-sertifikalidir`). Since Maven sells inks
and consumables as a real revenue line, the reference site gives us **zero** IA guidance there; we take
that from `gurdijital.com` and `csdijital.com` (§4).

---

## 2. Anatomy of pages, top to bottom

### 2.1 Product detail page — `/kcxl-yeni-hiz-makinesi-kcxl-uv-flatbed`
Markup is Bootstrap 5 grid, `col-lg-8` main + `col-lg-4` sidebar. Order:

1. **`section.breadcrumb`** — a title block, not a strip:
   `<h1>KCXL+ UV FLATBED</h1>` + `<span>Flatbed Baskı Makineleri</span>` (the parent category as a kicker),
   then the crumb list `Ana Sayfa › Flatbed Baskı Makineleri › KCXL+ UV FLATBED`.
   Note the H1 is duplicated further down the page — two `<h1>` on one document.
2. **Gallery** (`col-lg-8`) — Swiper 2-up: `.swiper.mySwiper2` main slider with
   `.swiper-button-next/prev` arrows, plus `.swiper.mySwiper` thumbnail strip beneath. 6 images.
   Each slide is wrapped in `a.swiper-box.fancybox` → Fancybox lightbox at full res.
3. **`div.paragraph`** — one long marketing paragraph (~110 words), no sub-headings, no bullets.
4. **`div.section > h2 "Teknik Özellikler"`** — spec block. *Not a `<table>`*: it is
   `<ul class="table">` with alternating `<li>label</li><li>: value</li>` pairs, styled into two columns.
   14 rows here.
5. **Sidebar (`col-lg-4 > .services__sidebar.sidebar > .widget`)**, in order:
   - `.brouchers` — PDF card: pdf.svg icon + `.h6.heading` "KCXL+ Katalog" + `a.link` **"İndir"**
     → `/uploads/files/kcxl-katalog_250718100217.pdf`
   - `.contact-address` — background-image card: info icon, `<span class="h3">`
     **"Nasıl Yardımcı Olabiliriz?"**, phone **+90 312 386 14 15**,
     "E-Posta: alpaslanyesil@cmykreklam.com". No form.
   - `.brouchers > h3 "Videolar"` — 2 YouTube thumbnails, `a.fancybox.playb` iframe lightbox.
6. **`h2 "Uygulama Görselleri"`** — 20–23 thumbnails in `a.product_group.fancybox2`, each captioned
   ("UV Cam Kapı Baskı", "UV Braille Alfabesi (Kabartma) Baskı", …).
7. **Floating WhatsApp button** (bottom-right, all pages).
8. **Footer** (see §2.5).

**There is no quote form, no "Teklif Al" button, no price, no "compare", no related-products block,
no stock/lead-time, no financing** on the product page. `Teklif` appears **0 times** in the HTML;
`Fiyat` appears **0 times**; `<form>` appears **0 times**.

### 2.2 Category page — `/flatbed-baski-makineleri`
1. `section.breadcrumb` — `<h1>Ürünler</h1>` (generic on **every** category page — the actual category
   name is only a `<span>` under it) + crumbs `Ana Sayfa › Flatbed Baskı Makineleri`.
2. `section.product.pt-50` — Bootstrap `row` of `col-md-4` cards. Card markup:
   ```html
   <div class="product-card">
     <div class="image"><a href="…"><img src="…/uploads/product/thumbs/xline-kc-…png" alt="Xline KC"></a></div>
     <div class="text">
       <a href="…" class="title"><span class="head">Xline KC</span><span class="line"></span></a>
       <p class="desc">Her Yüzeye Yüksek Kalite … imkânı&#8230;</p>
     </div>
   </div>
   ```
   The `<span class="line">` is a hover-underline element — this is the sliding-underline micro-interaction
   the client likes, and it is the *only* one on the site.
3. No filters, no sort, no sidebar, no per-card specs, no CTA button (the title *is* the link),
   no intro copy on the flatbed page (roll-to-roll has one sentence).
4. Footer. Total page weight 23 KB HTML — the page is genuinely thin (3 cards).

### 2.3 Homepage
No `<h1>` anywhere. Order of sections:
1. Hero slider — "Signature Serisi", copy *"Performansın mükemmel birleşimi olan Signature Serisi
   UV Hibrit Yazıcı ile tanışın"*, CTA **"Ürünü İncele"**; further slides: PLATINUM QR 5, PLATINUM
   HYBRID Q3, PLATINUM KC, PLATINUM TEX, PLATINUM PCT.
2. `h2` **"Her Yüzeye Uygun Dijital Baskı ve Kesim Makineleri"** — 5 sector tiles as `h3`:
   `Reklam` `Ambalaj` `Mobilya` `Tekstil` `Cam` → `/sektor/<slug>`.
3. `h2` **"Endüstriyel ve Profesyonel Makineler"** — product grid, CTA **"Ürüne Git"**.
4. `h2` **"Uygulama Görselleri"** — application photo wall.
5. `h2` **"Bilgilendirme"** → news cards (h3 titles truncated with `…`).
6. `h2` **"Showroom ve Fuarlar"**.
7. `h2` **"@cmyk_reklam Bizi Takip Edin!"** — Instagram wall.
8. Footer.

### 2.4 Kurumsal / Destek / İletişim
- **`/kurumsal`** (`<h1>Hakkımızda`): kicker *"güvenilirlik, kalite ve hız"*, headline
  **"25 Yıllık Tecrübe"**, then **"Farklı ihtiyaçlara yönelik İdeal Çözümler"**. Body:
  *"Dijital baskı sektörlerinde hizmet veren firmaların farklı ihtiyaçlarına ideal çözümler üretmek
  amacındayız."* and *"Kaliteli hizmet vererek başarıya ulaşmayı hedefleyen firmalardan farklı olmasa
  da, farkımız; bu prensiplere gösterdiğimiz sadakattir."* Then it reuses the homepage
  "Bizden Haberler" + "Showroom ve Fuarlar" blocks. **No timeline, no team, no counters, no references
  logo wall, no certificates.**
- **`/destek`** — H1 is wrongly **"İletişim"**; sections `Bizimle İletişime Geçin`,
  **`Teknik Servis Detayları`**, `Adres`, `Telefon / Fax`, `E-Posta`. Content is a fee schedule in
  plain prose: warranty parts covered by the firm; out-of-warranty parts + labour billed;
  **İstanbul/Ankara 120 USD**, **diğer iller 350 USD**, **genel bakım 500 USD**,
  **operatör eğitimi 350 USD**, **yazılım kurulumu 100 USD**, **bilgisayar müdahale 150 USD**.
  Service requests are taken by e-mail to info@ or **fax to 0312-386 02 25**.
- **`/iletisim`** — H1 `İletişim`, sub `Bizimle İletişime Geçin`; address
  *Susuz Mahallesi Dempa Sanayi Sitesi 3793. Cadde No: 34, 06105 Yenimahalle/Ankara*;
  `T: +90 312 386 14 15`, `F: +90 312 386 02 25`; a contact form with a **CAPTCHA image** and submit
  button **"Mesaj Gönder"**. **No map embed, no working hours, no department routing** — instead five
  raw personal mailboxes are dumped on the page (muratyorulmaz@, grafik@, burhan@, kemal@, alpaslanyesil@).

### 2.5 Footer (site-wide)
White-on-dark logo · tagline **"Dijital baskı sektörlerine ideal çözümler sunar"** · Facebook + Instagram ·
address · two phones · `info@cmykreklam.com` + `Destek : alpaslanyesil@cmykreklam.com` ·
column **"Kategoriler"** (the 6 machine families) · column **"Blog Yazıları"** (6 posts) ·
`© Copyright 2026 CMYK Reklam. Tüm Hakları Saklıdır.` · agency credit "Kodes" (`kodes.com.tr`).

---

## 3. Technical spec field names — the actual vocabulary

Harvested verbatim from seven product pages across all six families. **This is the field dictionary
our product schema should speak.** ✓ = present on that family's pages.

| # | Field (TR, verbatim) | Flatbed | Hybrid | Roll-to-roll | Tekstil | Kesim | Pack | Typical values seen |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|
| 1 | `Baskı Çözünürlüğü` | ✓ | ✓ | ✓ | ✓ | — | ✓ | `2400 dpi` · `2880 dpi` · `1200 dpi` · `Konica - 2880 Dpi / Epson - 2400 Dpi` |
| 2 | `Baskı Genişliği` | ✓ | ✓ | ✓ | ✓ | — | ✓ | `3200mm` · `5300 mm` · `2500mmx1250mm` · `2,5m x 1,5m` |
| 3 | `Baskı Hızı (Maksimum)` | ✓ | ✓ | ✓ | ✓ | — | ✓ | `400 m2/s` · `250 m2/s` · `68 m2/s` · `Yaklaşık 350 plaka / Saat (1 metrelik plaka)` |
| 4 | `Baskı Kafaları` | ✓ | ✓ | ✓ | ✓ | — | ✓ | `Ricoh GEN6` · `RICOH GEN5-6` · `Konica Minolta 1024i` · `KM 1024i - Kyocera` · `EPSON S3200 - EPSON i3200` |
| 5 | `Baskı Kafaları Sayısı` | ✓ | ✓ | ✓ | ✓ | — | ✓ | `16 (Maks.)` · `32 (Maks.)` · `9 (Maks.)` · `12 Maksimum - 16 Maksimum` |
| 6 | `Baskı Yüksekliği` | ✓ | ✓ | — | — | — | — | `100 mm` · `50mm` |
| 7 | `Damla Hacmi` | ✓ | — | ✓ | ✓ | — | ✓ | `5 Pl.` · `6 Pl. - 13 Pl.` · `13 Pl. - 3,5 Pl.` |
| 8 | `Güç Gereksinimi` | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | `230v (+/-) 10% / 40A / 50HZ / 60HZ` · `380v +/- 10% 50HZ` |
| 9 | `Güç (KW)` | — | — | — | — | ✓ | — | `30 KW` (also mis-used on Xline Solvent to hold a voltage string) |
| 10 | `Kurutma Sistemi` | ✓ | ✓ | ✓ | ✓ | — | — | `Su soğutma LED UV` · `UV - LED` · `UV Curing - LED Curing` · `Halojen – Fan` · `İnfrared / Fan` |
| 11 | `Makine Ağırlığı` | ✓ | ✓ | ✓ | — | — | ✓ | `1370 - 2500 kg.` · `3500 kg.` · `5500 kg.` |
| 12 | `Makine Ölçüsü` | — | ✓ | ✓ | — | — | ✓ | `6020 mm x 3732 mm x 1775 mm` (W×D×H) |
| 12a | `Makine Ölçüsü 2512` / `Makine Ölçüsü 3020` | ✓ | — | — | — | — | — | per-variant duplicate rows: `2200 mm x 5220 mm x 1530 mm` / `3000 mm x 5800 mm x 1530 mm` |
| 12b | `Makine Ölçüsü (Fikse Dahil)` | — | — | — | ✓ | — | — | `3000 mm x 5800 mm x 1530 mm` |
| 13 | `Mürekkep Tipleri` | ✓ | ✓ | ✓ | — | — | — | `UV -LED` · `LED` |
| 14 | `Renk Skalası` | ✓ | ✓ | ✓ | ✓ | — | ✓ | `CMYK + White + Lc + Lm + Varnish` · `CMYK + Lc + Lm + W + V` · `CMYK` |
| 15 | `RIP Yazılımı` | ✓ | ✓ | ✓ | — | — | ✓ | `PhotoPrint / Caldera (Opsiyonel)` · `Photo Print - Caldera (Opt.)` |
| 16 | `Tabla Ölçüsü` | ✓ | — | — | — | ✓ | — | `3050 mm x 2050 mm` · `3500mm x 3200mm` |
| 17 | `Standart` | — | ✓ | — | — | — | — | `LCD Monitor` |
| 18 | `Kesim Alanı` | — | — | — | — | ✓ | — | `3500mm x 3200mm` |
| 19 | `Kesim Formatları` | — | — | — | — | ✓ | — | `PLT, DXF, HPGL, PDF, EPS` |
| 20 | `Kesim Hassasiyeti` | — | — | — | — | ✓ | — | `± 0.1mm` |
| 21 | `Kesim Malzemeleri` | — | — | — | — | ✓ | — | `Araç Etiketleri, Etiket, Kart Etiketleri, PP Kağıt, Reflektif malzemeler, Kuşe-Bristol-1.Hamur Kağıt, MDF, Pleksiglass, PVC Dekota, Ahşap vs.` |
| 22 | `Kesim Takımı` | — | — | — | — | ✓ | — | `EOT, UCT, KissCUT, PEN, V-CUT, CNC` |
| 23 | `Maks. Kesim Hızı` | — | — | — | — | ✓ | — | `1500mm/s` |
| 24 | `Malzeme Kalınlığı` | — | — | — | — | ✓ | — | `45mm` |
| 25 | `Makine Tipi` | — | — | — | — | ✓ | — | `Q-Cut 3532` (and it contradicts the H1 "3521" — copy-paste error) |

Extra field names worth stealing from comparables (not on cmykreklam):
`Çalışma Ortamı` (`20-28°C-40-60RH`), `Güç Tüketimi` (`3800W`), `Güç Kaynağı` (`220V, 50/60Hz`),
`Uygulanabilir Formatlar` (`BMP/TIFF/JPG/EPS/PDF/CAD/PSD`), `Boya Kapasitesi` (`Her Renk için 3000ml`),
`Boya Tüketimi` (`Metrekarede 10-30ml`), `Dil`, `Baskı Alanı`, `Tabla`, `Kurutma`, `Renkler`
— all from [lazerpol.com/urun/uv-130x130-flatbed-printer](https://lazerpol.com/urun/uv-130x130-flatbed-printer/).

**Also listed on cmykreklam product pages as free-text (not a spec row): the media list.**
Xline KC: `Cam, Ahşap, MDF, Dekota, PVC, Policarbon, Suntalam, OWV, Plexiglass, Alüminyum, Fotoblok,
Canvas, Şeffaf Plexi, Alikobant, Blueback, Duvar Kağıdı`. This deserves to be a first-class,
filterable field (`Uygulanabilir Malzemeler`).

### 3.1 Unit bugs to *not* copy
- **`m2/s`** is used for throughput on every page. The real unit is m²/**hour**. Written as printed it
  claims 400 m² per second. Use `m²/sa` (TR) and `m²/h` (EN).
- `Baskı Genişliği` sometimes holds a *bed* dimension (`2500mmx1250mm`) and sometimes a true width
  (`3200mm`) — two different quantities in one field. Split into `Baskı Genişliği` and `Tabla Ölçüsü`.
- `Güç (KW)` on the Xline Solvent page holds `230v (+/-) 10% 10A / 50HZ`, i.e. a voltage string in a
  power field.
- Variant-specific dimensions are faked by inventing new field names (`Makine Ölçüsü 2512`,
  `Makine Ölçüsü 3020`) instead of modelling variants.

---

## 4. Consumables / ink taxonomy (from the comparables — cmykreklam has none)

**gurdijital.com** nav: `Kurumsal` · `Makineler` · `Ürünler` · `Sektörler` · `Teknik Servis` ·
`Galeri` · `Katalog` · `İletişim` — note **Makineler and Ürünler are separate top-level items**, which
is the right shape for a dealer that also sells consumables.

- **Makineler ▸** `UV Baskı Makineler` · `Solvent Makineler` · `Eco Solvent Makineler` ·
  `Kesici Makineler` · `Single Pass`
- **Ürünler ▸**
  - `Dijital Baskı Boyaları` ▸ `UV Baskı Mürekkebi` · `Eco Solvent Baskı Mürekkebi` ·
    `Solvent Baskı Mürekkebi` · `Bayrak Baskı Mürekkebi` · `Single Pass Baskı Mürekkebi` ·
    `Solvent` · `Primer`
  - `Baskılık Kağıt ve Kumaşlar` · `Yardımcı Malzemeler` · `Levhalar` · `Led ve Ekipmanları` ·
    `Reklam Folyoları` · `Viniller`
- **Sektörler ▸** `İnşaat ve Mimarlık` · `Reklam` · `Endüstriyel` · `Aydınlatma` · `Mobilya` · `Tuning`
- Card CTAs: **"Ürünü incele"** + **"Bize Ulaşın"**. Sort options exist:
  `En Son Eklenen, En Başta` / `En Son Eklenen, En Sonda` / `Fiyata Göre Azalan` / `Fiyata Göre Artan`.
- Product-page tabs: `Açıklama` · `İndirilebir Dosyalar` *(sic — typo for "İndirilebilir")* ·
  `Sipariş Formu`; ink pages add `Sıkça Sorulan Sorular`. CTA **"Sipariş Talebi Oluştur"**, submit
  **"GÖNDER"**, download **"İndir"**.
- Ink attribute vocabulary (from `/urun/universal-c5i`):
  **`Uyumlu Baskı Kafaları`** (`Ricoh Gen5i`), **`Kürlenme Yöntemi`** (`UV ışık`),
  **`Uygulama Yüzeyleri`** (`PVC, akrilik, karton, metal, ahşap, cam`), **`Renk Gamutu`**, **`Dayanım`**
  (`Dış mekân dayanımı, çizilmelere karşı direnç`). Trust: "2009'dan beri", brands
  `Galaxy` (distributor), `Phaeton`, `AluTechBond`, `Oracal`, `Frimpeks`, `Softmark`.

**csdijital.com** organises its whole nav around consumables:
`Dijital Baskı Makineleri` · `Mürekkepler` · `Baskı Kafaları` · `Yedek Parça` · `Tanıtım Videoları` ·
`Fuar` · `Bize Ulaşın`, and indexes inks **by machine + printhead + drop size**:
`Allwin 512i 30PL`, `Allwin Konica 1024 14PL-42PL`, `Galaxy Epson Dx5`, `Infiniti Polaris 15PL-35PL`,
`Crystaljet Seiko 35PL-50PL`… CTAs: **"Teknik Destek Talep Formu"**, claims **"7/24 Teknik Servis"**
and **"Uygun fiyat garantisi"**.

**mimaki.com.tr** is the cleanest reference for a dual-axis taxonomy — by segment
(`Tabela ve Reklam` · `Tekstil ve Giyim` · `Endüstriyel` · `3D Endüstri`) **and** by technology
(`Solvent Baskı Makineleri` · `Tekstil Baskı Makineleri` · `UV Baskı Makineleri` · `3D` ·
`Kesim Plotterları` · `Geçmiş Modeller`), plus `Yazılım` and `Opsiyonel Ürünler`, with a "Product Wizard"
selector. Its nav: `Ürünler` · `Haberler ve Etkinlikler` · `Yüklemeler ve Destek` · `Mimaki Hakkında` · `İletişim`.

---

## 5. Copy tone, heading patterns, CTA wording

**Tone.** Third-person corporate, present tense, adjective-heavy, no numbers in the prose beyond the
spec sheet. Sentences run long (40+ words). Zero second-person questions, zero pain-point framing,
zero pricing or ROI language. Sample, verbatim:

> "Platinum KCXL+ Flatbed UV Baskı Makinesi, endüstrideki en son teknolojiyi kullanarak benzersiz baskı
> deneyimleri sunuyor. Çift vakum motoru ve malzeme dayama pinleri gibi özelliklerle donatılmış olan bu
> makine, yüksek hassasiyetle çalışırken güvenilirliği de garanti ediyor. … 2400 dpi maksimum çözünürlük
> ve 100 mm'ye kadar baskı yapabilme özelliği sayesinde detaylı ve çeşitli malzemeler üzerine baskılar
> yapabilirsiniz."

**Heading patterns.**
- Product taglines are benefit-pairs joined by a comma:
  *"Her Yüzeye Yüksek Kalite, Her Sektöre Yaratıcı Çözümler"* (Xline KC).
- Section headings are noun phrases, Title Case: *"Endüstriyel ve Profesyonel Makineler"*,
  *"Her Yüzeye Uygun Dijital Baskı ve Kesim Makineleri"*, *"Uygulama Görselleri"*, *"Teknik Özellikler"*,
  *"Bizden Haberler"*, *"Showroom ve Fuarlar"*, *"Bilgilendirme"*.
- The one imperative sentence on the whole site:
  *"Camdan ahşaba, tekstilden metale kadar her yüzeye göz alıcı baskılar yapın"*.
- Application labels follow `UV + <malzeme/nesne> + Baskı`: `UV Cam Kapı Baskı`, `UV Deri Baskı`,
  `UV Braille Alfabesi (Kabartma) Baskı`, `Metal Etiket UV Baskı`, `UV Stor Perde Baskı`.

**CTA inventory — the complete list on cmykreklam.com:**

| CTA (verbatim) | Where |
|---|---|
| `Ürünü İncele` | homepage hero slides |
| `Ürüne Git` | homepage product grid |
| `İndir` | catalog PDF, product sidebar |
| `Mesaj Gönder` | contact form submit |
| `Nasıl Yardımcı Olabiliriz?` + phone | sidebar contact card (heading, not a button) |
| WhatsApp float | every page, `https://wa.me/+905548991530` |

**No `Teklif Al`, no `Hemen Ara`, no `Fiyat Teklifi`, no `Demo Talep Et`, no `Katalog İndir` button on
the category level, no callback request.** For a capital-goods site whose entire job is lead capture,
that is the single biggest commercial failure on the page.

CTA wording seen at the comparables and worth adopting:
`Teklif Al` / `Bilgi Al` (lazerpol) · `Bize Ulaşın` + `Ürünü incele` (gurdijital) ·
`Sipariş Talebi Oluştur` (gurdijital ink pages) · `Teknik Destek Talep Formu` (csdijital) ·
`Demo Talep Et` (teknoprint) · `GÖNDER` (form submits) · `Devamını Oku`.

**WhatsApp deep-link pattern (per product, verbatim from the markup):**
```
https://wa.me/+905548991530&text=Merhaba ürün hakkında bilgi istiyorum! KCXL+ UV FLATBED (KCXL Yeni Hız Makinesi...) https://www.cmykreklam.com/tr/kcxl-yeni-hiz-makinesi-kcxl-uv-flatbed
```
Two bugs in one link: `&text=` instead of `?text=` (so the prefilled message is **silently dropped** —
`wa.me` needs `?` for the first query param), and the `/tr/` URL 404s. The *idea* is right and worth
copying properly:
`https://wa.me/905XXXXXXXXX?text=` + `encodeURIComponent("Merhaba, {ÜRÜN} hakkında teklif almak istiyorum. {URL}")`.

---

## 6. Trust signals inventory

| Signal | cmykreklam | Notes |
|---|---|---|
| Years in business | ✅ **"25 Yıllık Tecrübe"** on `/kurumsal` | Just a heading, not a stat block; not on the homepage |
| Brands carried | ⚠️ `Liyu` / `Liyu Printer`, own line `Platinum`, `Xline` | Never a logo wall, only mentioned inside news copy |
| OEM component brands | ✅ `Ricoh GEN5/GEN6`, `Konica Minolta 1024i`, `Kyocera`, `EPSON S3200/i3200` | Only inside spec tables — never merchandised |
| Certification | ✅ `GreenGuard Gold` on Platinum UV inks | Buried in a 2022 news post |
| Showrooms | ✅ `Liyu İtalya Showroom` (Milano), `Liyu İngiltere Showroom` (Burscough) | `/showroom` also contains 2 unpublished test entries |
| Trade fairs | ✅ `Sign İstanbul`, `Viscom Milano`, `FESPA`, `drupa 2024` | Newest fair content is 2024 — site looks stale in 2026 |
| Service promise | ✅ published **price list** for service call-outs, training, installs | Unusually transparent; the *presentation* is a wall of text |
| Warranty | ✅ "İşletmemiz garantisi altındaki makinalarda oluşabilecek yedek parça değişimleri firmamız tarafından karşılanmaktadır" | |
| Customer references | ❌ none | No logos, no case studies, no testimonials, no install count |
| Physical proof | ⚠️ address only | No map, no photos of the premises/service workshop, no team |
| Spare-parts stock claim | ❌ none | csdijital by contrast leads with "7/24 Teknik Servis" |

---

## 7. What they do well — worth keeping

1. **Family-first taxonomy.** Six machine families named by form-factor is exactly how a Turkish buyer
   searches (`flatbed baskı makinesi`, `roll to roll baskı makinesi`). Slugs are clean, Turkish, and
   keyword-bearing. Keep.
2. **A real, consistent spec vocabulary.** ~25 field names reused across 20 products. It is the single
   most valuable artefact on the site — see §3. Keep and normalise.
3. **Application imagery as the primary sales argument.** 20+ captioned real-world shots per machine
   (`UV Asansör İçi Cam Baskı`, `UV Braille Alfabesi (Kabartma) Baskı`) does more selling than any of
   their prose. Keep — but make it a proper gallery with alt text and lazy loading.
4. **Per-product catalog PDF** in the sidebar with a plain `İndir`. Keep; add gating-free download +
   file size + language badge.
5. **Product-scoped WhatsApp deep link** with the product name pre-filled. Right instinct, broken
   implementation. Keep the idea, fix the URL.
6. **Sector cross-axis** (`Reklam / Ambalaj / Mobilya / Tekstil / Cam`). Good SEO surface. Keep, and
   actually put it in the nav.
7. **Published service pricing.** Genuinely differentiating in this market. Keep, present as a table.

## 8. What is dated or broken — measured, not guessed

1. **Not multilingual at all.** `<html lang="tr">`, no hreflang, no switcher, dead `/tr/` links in
   templates. A machine importer with no EN site cannot talk to a supplier or a non-Turkish buyer.
2. **H1 discipline is broken.** Homepage has **no `<h1>`**. Every category page's H1 is the literal word
   **"Ürünler"**. Product pages emit **two `<h1>`** elements. Category pages are therefore competing
   against each other for nothing.
3. **No `og:`/Twitter meta, no JSON-LD.** Raw HTML contains zero Open Graph tags and zero structured
   data. Sharing a machine on WhatsApp/LinkedIn yields a blank card. No `Product`/`Organization`/
   `BreadcrumbList` schema.
4. **Images are unoptimised.** Homepage pulls 63 images; the 40 measured total **~3.3 MB**, with five
   hero JPEGs at 258–322 KB each. Product hero is a **220 KB PNG**. Zero `loading="lazy"`, zero
   `srcset`, zero `<picture>`/WebP/AVIF, and only 11 of the images carry a `width` attribute → guaranteed
   CLS. HTML alone is 91 KB.
5. **jQuery + Bootstrap bundle + Modernizr 3.5.0 + Swiper + Fancybox**, all render-blocking, plus a
   full-screen CSS loader overlay that gates first paint. Modernizr 3.5.0 shipped in 2017.
6. **Zero lead capture on the money pages.** No quote form, no "Teklif Al", no price-on-request, no
   callback, no comparison, no financing/leasing note. The only conversion path is a WhatsApp button
   with a broken prefill, or scrolling to a phone number.
7. **Contact page is a mailbox dump.** Five personal e-mail addresses in plain text (spam-harvestable,
   and it leaks staff turnover), a **CAPTCHA image** in 2026, **fax** as a documented support channel,
   no map, no hours.
8. **`/destek` has the wrong H1 ("İletişim")** and reads as a fee schedule in prose. No FAQ, no
   troubleshooting, no parts catalogue, no service-request form, no SLA, no coverage map.
9. **Broken/placeholder IA.** `Ürünler` parent links to `/platinum-hybrid`; `Uygulamalar` parent links
   to `/uygulama/platinum-hybrid`; the Uygulamalar dropdown contains two empty `<li><a href="/uygulama/"></a></li>`
   items; `/showroom` publishes test records named `test6` and `baslik-uzun`; `Makine Tipi: Q-Cut 3532`
   on a page titled `PLATINUM Q CUT 3521`.
10. **Stale.** Latest news is 2024 (drupa 2024, FESPA 2024) while the footer says 2026. Blog is 6 posts
    of generic "UV baskı nedir" content.
11. **No consumables business online at all** — no inks, no printheads, no spare parts, no media. For
    Maven this is the largest single opportunity: the recurring-revenue half of the business is
    invisible on the reference site.
12. **Micro-interaction poverty.** One hover underline (`span.line`) and a Swiper. No scroll reveals
    worth the name, no 3D, no interactive spec comparison. The bar for "better" is low and we should
    clear it by a mile.

---

## 9. Direct implications for the Maven build

**IA — proposed top nav (TR / EN), 6 items, dual-axis taxonomy:**

```
Ürünler / Products
  ├── Makineler / Machines
  │     ├── Flatbed Baskı Makineleri        (UV flatbed)
  │     ├── Hibrit Baskı Makineleri
  │     ├── Roll to Roll Baskı Makineleri
  │     ├── Tekstil Baskı Makineleri
  │     ├── Kesim Makineleri / Plotterlar
  │     └── Endüstriyel / Single Pass
  └── Sarf Malzemeleri / Consumables        ← the half cmykreklam is missing
        ├── UV Mürekkep
        ├── Solvent & Eco Solvent Mürekkep
        ├── Tekstil / Süblimasyon Mürekkebi
        ├── Baskı Kafaları
        ├── Yedek Parça
        └── Yardımcı Malzemeler (primer, temizleyici, filtre)
Sektörler / Industries      Reklam · Ambalaj · Mobilya · Cam · Tekstil · Endüstriyel
Teknik Servis / Service     kurulum · eğitim · bakım · yedek parça · servis talebi
Kurumsal / About            hikaye · ekip · showroom · fuarlar · sertifikalar
Bilgi / Insights            blog + haberler merged
İletişim / Contact          + persistent "Teklif Al" button in the header
```

Routing: `/{locale}/urunler/makineler/{kategori}/{model}` with a locale-keyed slug map, so EN gets
`/en/products/machines/{category}/{model}` — never a `/tr/` prefix bolted on after launch.

**Product page section order (improving on §2.1):**
breadcrumb → H1 + kicker (category) + one-line benefit tagline → **hero split: gallery / 3D viewer toggle**
+ 4 headline specs + `Teklif Al` & WhatsApp → intro (short, 3 bullets not 110 words) →
`Teknik Özellikler` (real `<table>`, grouped: Baskı / Mekanik / Elektrik / Yazılım) →
`Uygulanabilir Malzemeler` (chips) → `Uygulama Görselleri` → `Videolar` → `İndirilebilir Dosyalar`
(katalog PDF + size) → `Sarf Malzemeleri` (cross-sell — the ink that fits this machine) →
`Benzer Makineler` → sticky quote bar on mobile.

**Data model:** one JSON per product, keyed on the §3 field dictionary, with `unit` separated from
`value` so EN can render `m²/h` while TR renders `m²/sa`; variants as an array (kills the
`Makine Ölçüsü 2512` hack); `compatible_inks: []` and `printhead: {brand, model, count, drop_pl}` as
first-class relations so machine↔consumable cross-linking is automatic in both locales.
