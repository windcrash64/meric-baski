# Track 4 — Turkish Market Expectations, Terminology & SEO

Research date: 2026-07-28. Target: a **static, bilingual (TR default / EN), non-e-commerce corporate
site** for a dealer/distributor of digital printing machines + inks/consumables + technical service.

Everything below is observed on live Turkish vendor sites, Turkish marketplaces, or primary legal
sources. Where I could not verify something, it says so explicitly.

**Honest caveat on the keyword table:** I have no access to Ahrefs/Semrush/Google Keyword Planner
volume data for TR. The keyword list is derived from *observed targeting* — real `<title>`/H1/URL
patterns on Turkish dealer and marketplace pages — not from measured search volume. Treat the
ordering as "what the market is optimising for", not "verified monthly volume". Validate with
Google Search Console after 60 days live.

---

## 0. The single most important finding

**Turkish trade vocabulary is not standardised, and the site must carry the synonyms, not pick one.**
Four independent axes of variation appear across every site I looked at:

| Axis | Variants observed in the wild | Where |
|---|---|---|
| makine / makina | "Baskı Makineleri" vs "Baskı Makinaları" / "Makinası" | mekadijital.com uses *makineleri*; makinaturkiye.com and makinecim.com use *makinası*; passreklam uses *makinaları* |
| ink word | **boya** ≈ **mürekkep** ≈ **ink** (used interchangeably, often stacked) | prodigital.com.tr menu says "Boyalar ve Sarf Malzemeler"; mekadijital says "Dijital Baskı Boyaları"; inkmarketi.com literally titles categories "Dijital Baskı **İnk Boya Mürekkep**" |
| eco-solvent | eko solvent / ekosolvent / eco solvent / ecosolvent | mekadijital "Ekosolvent"; mrtdijital "Solvent & Ecosolvent"; makinaturkiye "Eko Solvent" |
| sublimation | süblimasyon / sublimasyon | mekadijital "Süblimasyon"; serfoto/passreklam "Sublimasyon" |

**Actionable:** the i18n dictionary must be able to express a *primary* label plus an *alias* array.
Primary label = editorial (what shows in UI); aliases = injected into `<meta name="keywords">`-free
places that actually matter: body copy, `alt` text, FAQ answers, and JSON-LD `alternateName`.
Never render both variants in the same visible sentence — it reads as keyword stuffing.

Recommended house style for Maven (pick and enforce):
- **makine** (not *makina*) — modern/editorial, matches the "minimal, high-craft" brand.
- **mürekkep** in headings and product titles; **boya** allowed in body copy and FAQ (because that
  is what customers say on the phone).
- **eko solvent** (two words) as primary; alias list covers the other three.
- **süblimasyon** (with ü) as primary.

Sources: <https://www.mekadijital.com/>, <https://www.prodigital.com.tr/mutoh-uv-baski-makineleri/>,
<https://www.inkmarketi.com/product/category&path=135>, <https://www.makinaturkiye.com/passreklam>,
<https://mrtdijital.com/>

---

## 1. Glossary — Turkish industry vocabulary

Column 3 says **where in our site the term belongs**, so this doubles as an IA checklist.

### 1.1 Machine classes & configurations

| Turkish | English | Use in our site |
|---|---|---|
| dijital baskı makinesi / makinası | digital printing machine | Top-level product category name |
| rulodan ruloya (kısaltma: RTR) | roll-to-roll | Product **filter** value + spec field `Besleme Tipi` |
| tabaka / levha baskı | sheet / rigid-board printing | Filter value |
| flatbed (düz yatak) | flatbed | Filter value. "Düz yatak" is used but "flatbed" is the dominant trade word — see crystek TR listing "UV Düz Yatak Yazıcı" |
| hibrit (hybrid) | hybrid (roll + rigid on one machine) | Filter value — Prodigital markets Dilli 160/250/320 cm as "hibrit UV sistemler" |
| eko solvent baskı makinesi | eco-solvent printer | Category |
| solvent baskı makinesi | (hard/true) solvent printer | Category |
| UV baskı makinesi / UV LED | UV / UV-LED printer | Category |
| UV flatbed | UV flatbed | Sub-category |
| UV DTF (soğuk transfer) | UV DTF / cold transfer | Sub-category — lazerpol sells "UV-DTF Soğuk Transfer Baskı Makinesi 30cm" |
| süblimasyon baskı makinesi | dye-sublimation printer | Category |
| transfer / direkt süblimasyon | transfer vs direct sublimation | Spec field value (Mimaki TS330 marketed as "direkt ve transfer süblimasyon hibrit") |
| DTF baskı makinesi / DTF yazıcı | direct-to-film printer | Category |
| tekstil baskı makinesi | textile printer | Category |
| bayrak baskı makinesi | flag printer (with inline fixation) | Sub-category (Meka: "Dijital Bayrak Baskı Makineleri") |
| halı baskı sistemi | carpet printing system | Optional category (Mutoh/Prodigital carry it) |
| kesici plotter / folyo kesici | cutting plotter / vinyl cutter | Category |
| bas-kes (print & cut) | print-and-cut | Sub-category (Roland/Promakim uses "Bas Kes Modelleri") |
| flatbed kesici / dijital kesim sistemi | flatbed cutter / digital cutting system | Category |
| laminasyon makinesi | laminator | Category |
| CNC router / fiber lazer | CNC router / fiber laser | Adjacent category — most TR dealers carry these too |
| transfer baskı presi / ısı presi | heat press | Accessory category |
| masaüstü (tabletop) | desktop | Filter for small UV units |

### 1.2 Print engine / spec-sheet fields

These are the **exact spec-table row labels** harvested from live TR product pages
(mrtdijital.com, lazerpol.com). Use these verbatim as our `specs` schema keys — do not invent.

| Turkish spec label | English | Notes / observed values |
|---|---|---|
| Baskı Kafası / Miktarı | printhead / count | "Epson Dx5 / 2-3-4 Kafa", "İki Adet Epson Xp600" |
| Kafa Sayısı | number of heads | Used as a product-title modifier: "180cm **2 Kafa**", "60cm **4 Kafa**" |
| Mürekkep Türü / Renk | ink type / colours | "Ecosolvent boya / 4-8 renk"; "CMYK+Lc+Lm+W" |
| Maximum Malzeme / Baskı Genişliği | max media / print width | "1.9m / 1.8m" — TR sites give **two** widths, media and printable |
| Baskı Modları | print modes | "2 / 3 / 4 / 6 / 8 Pass" |
| Geçiş / Pass | pass | "5PASS", "8 Pass" — *pass* is used untranslated; "geçiş" is rarer |
| Baskı Hızları | print speeds | "16 sqm/h – 128 sqm/s"; also "m²/saat" |
| Baskı Çözünürlüğü | print resolution | "1440 dpi", "2880×2400 DPI" |
| Damla Boyutu (pikolitre / pL) | drop size | "min 2.5 pikolitre", "3.8 – 9.4 pL" |
| Nozül Adedi / Nozzle | nozzle count | "toplam 3.200 nozül (her satırda 400 nozül, 8 satır)" |
| Kurutma Sistemi | drying system | "Kurutma fanı ve infrared" |
| UV LED lamba / kürleme | UV LED lamp / curing | "UV LED ile anında kuruma" |
| Vakum tabla / vakumlu tabla | vacuum table/bed | Standard on flatbeds |
| Malzeme Besleme Sistemi | media feed | "Otomatik sarma ve Germe sistemi" |
| Sarma / take-up | take-up reel | part of feed spec |
| Negatif basınç sistemi | negative-pressure ink system | Common bullet on Chinese-built machines sold in TR |
| Kafa Temizleme | head cleaning | "Otomatik Temizleme sistemi" |
| Kafa Koruması / Cap istasyonu | capping station | "Otomatik Korumalı Cap Sistemi" |
| Baskı Dosya Formatı / Desteklenen Formatlar | supported file formats | "PSD/DWG/HPG/PLT/PS/EPS", "Bmp, Tiff, Jpg, Eps, Pdf, CAD" |
| Kontrol Sistemi | control system | "Driver ve RIP Yazılımı" |
| Yazılım | software | "Photoprint 12.0 / ONYX / Maintop" |
| Baskı Bağlantısı | interface | "USB", ethernet |
| Güç | power | "AC 220V - 50HZ" |
| Makine Ebatı ve Ağırlığı | dimensions & weight | "E: 3.35 m B: 0.75 m Y: 0.96 m / 380 Kg" (E=en, B=boy, Y=yükseklik) |
| Paket Boyutları | crated dimensions | "312cm X 74cm X 73cm" — matters because buyers must plan door/lift access |
| Lineer motor / manyetik kayışsız sistem | linear motor / beltless drive | Marketed as a premium differentiator (istanbulreklam.com) |
| Encoder film / encoder şerit | encoder strip | Spare part |

### 1.3 Consumables & spare parts (`Sarf Malzeme` / `Yedek Parça`)

Meka Dijital's spare-parts taxonomy is the cleanest live example; copy its structure.

| Turkish | English |
|---|---|
| sarf malzeme | consumables |
| yedek parça | spare parts |
| mürekkep / boya / ink | ink |
| eko solvent mürekkep, solvent mürekkep, UV mürekkep, süblimasyon mürekkebi, DTF pigment mürekkep | ink families |
| beyaz mürekkep (W), vernik (varnish) | white / varnish |
| Lc / Lm (açık camgöbeği / açık macenta) | light cyan / light magenta |
| temizleme solüsyonu | cleaning solution |
| baskı kafası (printhead) | printhead |
| damper | damper |
| filtre | filter |
| cap (kapak) / capping | cap |
| wiper | wiper |
| boya motoru / pompa / valf | ink pump / valve |
| boya tankı ve hortumlar | ink tank & tubing |
| elektronik kart | PCB / board |
| hareket motoru, kablo, sensör, limit sensör | motor, cable, sensor |
| kafa kablosu | head cable |
| adaptör (kafa adaptörü) | printhead adapter |
| DTF transfer tozu / baskı tozu | DTF adhesive powder |
| DTF PET film / transfer film | DTF film |
| toz serpme ünitesi / shaker / fırın | powder shaker / curing oven |
| sıvı laminasyon | liquid lamination |

Source: <https://www.mekadijital.com/> (Yedek Parça sub-menu),
<https://www.inkmarketi.com/product/category&path=135>, <https://lazerpol.com/urunler/dtf-urunleri/>

### 1.4 Media / substrates (what the customer prints ON)

This vocabulary belongs on the site even though we don't sell media — it is how customers describe
their job ("branda basacağım"), and it is the bridge between "machine" and "application".

| Turkish | English |
|---|---|
| medya / malzeme | media |
| vinil | vinyl (self-adhesive or banner) |
| branda | PVC banner / tarpaulin |
| germe branda | tensioned/frame banner |
| mesh (delikli branda) | mesh banner |
| ışıklı vinil / frontlit / backlit | frontlit / backlit |
| folyo | film / vinyl foil |
| one way vision (delikli folyo) | one-way vision |
| kanvas | canvas |
| forex / dekota (PVC foam levha) | PVC foam board (Forex/Dekota are brand names used generically) |
| alüminyum kompozit (ACP) | aluminium composite panel |
| pleksi (akrilik) | acrylic |
| sunta / MDF / ahşap, cam, seramik, metal | rigid substrates for UV |
| PET film | PET film (DTF) |
| kağıt: transfer kağıdı, fotoblok | transfer paper, foamboard |
| rulo / bobin | roll |

Sources: <https://www.jetmalzeme.com/kategori/mesh-vinil-branda>,
<https://www.jetmalzeme.com/kategori/dekota-foreks>,
<https://print.bestreklam.com.tr/branda-ve-vinil-baski-m2-fiyatlari-isikli-delikli-ve-branda-afis/>

### 1.5 Workflow / software / colour

| Turkish | English |
|---|---|
| RIP yazılımı | RIP software |
| ripleme / riplemek | to RIP a file |
| raster / raster görüntü işlemcisi | raster image processor |
| ICC profil / renk profili | ICC profile |
| renk yönetimi | colour management |
| ONYX, Caldera, PhotoPRINT, Maintop, Flexi | the RIPs actually named on TR sites |
| profil çıkarma / kalibrasyon | profiling / calibration |
| baskı-kesim (contour cut) | print & cut / contour cut |
| dosya hazırlama | prepress / file prep |

Sources: <https://www.matkagit.com.tr/rip-yazilimi-nedir-baski-atolyelerinde-hiz-ve-kaliteyi-nasil-artirir/>,
<https://www.matkagit.com.tr/urunler/yazilim-cozumleri/caldera/>, mrtdijital spec table.

### 1.6 Applications / customer verticals (drives our "Uygulamalar" section)

| Turkish | English |
|---|---|
| tabela | signage |
| ışıklı tabela / kutu harf | lightbox sign / channel letters |
| totem | totem / pylon sign |
| cephe giydirme / bina giydirme | building wrap |
| araç kaplama / araç giydirme | vehicle wrap |
| afiş, poster, raket, billboard | poster formats |
| dekorasyon, duvar kağıdı | interior decor, wallpaper |
| promosyon / hediyelik eşya | promotional items |
| etiket / etiket baskı | label printing |
| ambalaj | packaging |
| tekstil / giyim baskı | apparel printing |
| endüstriyel baskı | industrial printing |
| fason baskı | contract / trade printing |

### 1.7 Commercial & service vocabulary

| Turkish | English | Note |
|---|---|---|
| teklif al / teklif iste / fiyat teklifi | request a quote | **"Teklif Al"** is the canonical CTA; makinecim.com uses "Teklif İste" |
| bilgi al | request info | lazerpol's product-card CTA |
| bize ulaşın / iletişim | contact us |
| bayi / bayilik / distribütör / yetkili satıcı | dealer / distributorship / authorised reseller | serfoto.com.tr has a "Bayilik Başvurusu" page; Mimaki has "Bayi bul" |
| ithalatçı firma | importer | serfoto uses it as its main trust claim |
| satış sonrası destek | after-sales support |
| teknik servis | technical service |
| yerinde servis | on-site service |
| uzaktan destek / uzaktan yardım | remote support | istanbulreklam.com menu item |
| kurulum / montaj | installation |
| ön keşif | site survey before install | MRT: "makinelerinizi yerleştireceğiniz mekanda yapılacak ön keşif" |
| eğitim / operatör eğitimi | operator training |
| periyodik bakım / genel bakım | periodic / general maintenance |
| garanti / garanti kapsamı | warranty / warranty scope |
| yedek parça stoğu | spare-parts stock |
| demo / demo talebi | demo request |
| showroom / sergi salonu | showroom |
| sıfır / 2. el (ikinci el) | new / second-hand | makinecim facet: "Sıfır (35), 2. El (21)" |
| takas | trade-in |
| kiralık | rental | makinecim listing category: "Satılık, Aranıyor, Kiralık" |
| taksit / vade | instalments / terms |
| leasing / finansal kiralama | leasing |
| KDV hariç / KDV dahil | excl./incl. VAT |
| kargo / nakliye | shipping |
| stokta / stok durumu | in stock |
| referanslar | references / client list |
| sarf ömrü / tüketim | consumption |

---

## 2. SEO — keyword phrases Turkish buyers actually use

**Method:** phrases below appear as real page titles, H1s, URL slugs or category names on live Turkish
dealer/marketplace pages (evidence column). Intent labels: **C** = commercial/transactional,
**I** = informational, **B** = brand/navigational, **L** = local.

### 2.1 Machine-buying head terms

| # | Phrase (TR) | Intent | Evidence / where it is already targeted |
|---|---|---|---|
| 1 | dijital baskı makinesi | C | mekadijital.com/urun-kategori/dijital-baski-makineleri/ ; istanbulreklam.com/dijital-baski-makineleri/ |
| 2 | dijital baskı makinası fiyatları | C | makinecim.com title: "Dijital Baskı Makinası Fiyatları \| 2. El Sıfır Satılık" |
| 3 | uv baskı makinesi | C | lazerpol.com/urunler/uv-printer/ title "Uv Baskı Makinesi, DTF Baskı Makinesi, Dijital Printer Satışı" |
| 4 | uv baskı makinesi fiyatları | C | printec-online.com/urun-kategori/.../uv-baski-makinesi/ |
| 5 | uv flatbed baskı makinesi | C | prodigital.com.tr "Flatbed Uv baskı makineleri" |
| 6 | eko solvent baskı makinesi | C | makinaturkiye "Eko Solvent Baskı Makinası Fiyatları Çeşitleri" |
| 7 | ekosolvent baskı makinesi *(alias)* | C | mekadijital sub-category "Ekosolvent Dijital Baskı Makineleri" |
| 8 | solvent baskı makinesi | C | cmykreklam.com/solvent-baski-makinesi |
| 9 | dtf baskı makinesi | C | teknofinal, serfoto, printec all run this exact slug |
| 10 | dtf yazıcı fiyatları | C | dtfyazici.com title "DTF Baskı Makineleri \| DTF Yazıcı Fiyatları" |
| 11 | süblimasyon baskı makinesi | C | mekadijital "Süblimasyon Dijital Baskı Makineleri"; hepsiburada category page exists |
| 12 | tekstil baskı makinesi | C | makinaturkiye "Dijital Tekstil Baskı Makinası Fiyatları Çeşitleri" |
| 13 | rulodan ruloya baskı makinesi | C | lazerpol.com/urun/rulodan-ruloya-uv-baski-makinesi/ |
| 14 | hibrit uv baskı makinesi | C | prodigital (Dilli hibrit UV) |
| 15 | uv dtf baskı makinesi | C | lazerpol "UV-DTF Soğuk Transfer Baskı Makinesi"; meka "30cm UV DTF" |
| 16 | bayrak baskı makinesi | C | mekadijital "Dijital Bayrak Baskı Makineleri" |
| 17 | kesici plotter / folyo kesme makinesi | C | istanbulreklam "Kesici Plotterlar"; prodigital "Mutoh Folyo Kesiciler" |
| 18 | ikinci el dijital baskı makinesi | C | cmykreklam.com/dijital-baski-makinesi-2el ; ilkeldenikinciel.com "2.EL MAKİNELER" ; lazerpol nav item "İKİNCİ EL" |
| 19 | 2. el uv baskı makinesi | C | ilkeldenikinciel.com/urun-kategori/2-el-makineler/ |
| 20 | satılık dijital baskı makinesi | C | turkprinting.com "Dijital Baskı Makinası, Sıfır, İkinci El" |

### 2.2 Consumables / spare-parts terms (higher frequency, lower value per visit — but they are the
**repeat-purchase** funnel and the reason a dealer site earns organic traffic at all)

| # | Phrase (TR) | Intent | Evidence |
|---|---|---|---|
| 21 | dijital baskı mürekkebi | C | makinaturkiye "Baskı Mürekkebi Fiyatları Çeşitleri" |
| 22 | eko solvent mürekkep fiyat | C | inkmarketi category names |
| 23 | uv mürekkep fiyatları | C | printec-online "Eko UV Mürekkebi"; inkateknik.net/dijital-baski-murekkepler/uv-murekkpeler |
| 24 | dtf mürekkep / dtf pigment mürekkep | C | lazerpol "DTF Pigment Mürekkep CMYK" |
| 25 | dijital baskı boyası *(boya synonym!)* | C | mekadijital "Dijital Baskı Boyaları"; prodigital "UV Baskı Boyaları" |
| 26 | baskı kafası fiyatları | C | mekadijital/urunler/.../baski-kafalari-ve-adaptorler/ |
| 27 | epson i3200 baskı kafası | C+B | exact-slug pages on mekadijital, lazerpol, iksirmedya |
| 28 | epson xp600 baskı kafası | C+B | lazerpol "Epson XP600 (DX11) Baskı Kafası" |
| 29 | dx5 baskı kafası | C+B | inkmarketi "Epson DX5/DX7 Dijital Baskı Kafası Printhead" |
| 30 | konica 1024i baskı kafası | C+B | centerdesign.com/40-yazici-kafalari |
| 31 | dtf transfer tozu | C | dtfturkiye.com/transfer-baski-tozu |
| 32 | dtf pet film | C | serfoto.com.tr/dtf-sarf-malzemeleri |
| 33 | dijital baskı yedek parça | C | inkmarketi "Eko Solvent Dijital Baskı Yedek Parçaları" |
| 34 | damper / wiper / cap (kafa yedek parça) | C | mekadijital sub-categories |

### 2.3 Service, local and informational

| # | Phrase (TR) | Intent | Evidence |
|---|---|---|---|
| 35 | dijital baskı makinesi teknik servis | C | mekadijital blog slug `dijital-baski-makinesi-teknik-servis`; ait.com.tr/teknik-servis-ve-yedek-parca |
| 36 | ankara dijital baskı teknik servis (şehir + servis) | L | ankagrupreklam.com.tr/ankara-dijital-baski-teknik-servis/ — proves the city-modifier pattern works |
| 37 | istanbul dijital baskı makinası | L | makinecim.com/dijital-baski-makinasi?CityId=İstanbul |
| 38 | baskı kafası tamiri | C | baskikafatamiri.com — a whole domain on this phrase |
| 39 | uv baskı nedir | I | widely used explainer slug |
| 40 | dtf baskı nedir / dtf nasıl yapılır | I | agoodprinter.com/tr, textek.cn/tr run TR explainers targeting this |
| 41 | rip yazılımı nedir | I | matkagit.com.tr/rip-yazilimi-nedir-... |
| 42 | eko solvent ile uv baskı farkı | I | comparison intent, weakly served in TR — **opportunity** |

### 2.4 SEO decisions that follow from the above

1. **URL scheme must be Turkish-slugged, English mirrored.**
   `/urunler/uv-baski-makineleri/<slug>` ↔ `/en/products/uv-printers/<slug>`.
   Do **not** use `/tr/` for the default locale — TR is the default and should sit at the root
   (better for `.com.tr` / TR-geo signals and shorter canonical URLs). Add `/en/` for English.
2. **hreflang**: emit `tr-TR`, `en`, and `x-default` → the Turkish root. Architecture must generate
   these from a locale registry, not hard-code them, so adding `ar`/`ru` (both real markets for
   Turkish machine exporters) is a config change.
3. **Category pages are the money pages, not the homepage.** Every one of the 20 machine head terms
   maps to a category or filtered listing. Build a category page per ink technology
   (UV / eko solvent / solvent / süblimasyon / DTF / tekstil), each with real editorial copy
   (300–600 words), not just a product grid.
4. **The "fiyat / fiyatları" modifier is unavoidable.** TR buyers append it to almost every query.
   Since we won't publish machine prices (see §3.4), serve the intent instead: an H2 named
   *"… fiyatları hakkında"* explaining what drives price (kafa sayısı, baskı genişliği, mürekkep
   sistemi, kurulum+eğitim dahil mi) and ending in a Teklif Al CTA. This is the highest-leverage
   page section on the whole site.
5. **Publish an "İkinci El" page even with zero stock.** Term 18/19 has real demand and near-zero
   competition from *brand* dealers (it's dominated by classifieds). A page that says "elimizdeki
   ikinci el / takas makineler — güncel liste için arayın" captures it. Lazerpol puts İKİNCİ EL in
   its main nav; so should we.
6. **City-modifier landing pages work in this niche** (evidence: term 36). Build a small set:
   İstanbul, Ankara, İzmir, Bursa, Gaziantep, Konya, Antalya — but only if we can write genuinely
   different copy (service response time, nearest depot). Otherwise skip; thin doorway pages hurt.
7. **JSON-LD**: `Organization` + `LocalBusiness` on the contact page, `Product` **without**
   `offers.price` (use `offers.availability` + `priceCurrency` omitted) on product pages,
   `BreadcrumbList` everywhere, `FAQPage` on the explainer sections. Since it's a static build these
   are trivially generated from the same data file that feeds the page.
8. **Alias handling**: put "makinası", "ekosolvent", "sublimasyon", "boya" into `Product.alternateName`
   and into natural FAQ sentences — never into visible headings.

---

## 3. What Turkish B2B buyers expect that Western sites don't have

Every item below is observed behaviour on live TR sites, not speculation.

### 3.1 WhatsApp is a first-class channel, not a widget

- WhatsApp is the most-used app in Turkey — **88.6%** of individuals per TÜİK's 2025 ICT survey,
  ~58.5M monthly actives (2026 estimate). ([bloomberght.com](https://www.bloomberght.com/turkiyede-en-cok-kullanilan-uygulama-whatsapp-oldu-2359054), [avangardreklam.com](https://avangardreklam.com/blog/turkiye-dijital-pazarlama-istatistikleri-2026/))
- lazerpol.com labels its button **"WhatsApp Destek"**; istanbulreklam.com opens with a pre-filled
  greeting *"Merhaba Size nasıl yardımcı olabilirim?"*.

**Build decision:** a persistent floating WhatsApp FAB (bottom-right on mobile, bottom-right desktop),
plus an inline WhatsApp button *inside* every product page next to "Teklif Al". Static-friendly:
`https://wa.me/90XXXXXXXXXX?text=` with a **URL-encoded, product-specific prefill**, e.g.
`Merhaba, {ÜrünAdı} hakkında bilgi almak istiyorum.` — generate the link at build time per product.
No JS SDK, no third-party chat script (kills our Lighthouse score and creates a KVKK problem).

### 3.2 Phone-first, and the number is a design element

- lazerpol runs a 444 number ("444 3 103") in the header — a 444 line reads as "established company"
  in Turkey and is worth more than a mobile number visually.
- mrtdijital, mekadijital, serfoto, passteknik all put a full landline + district address in the
  header/footer. serfoto labels it **"Müşteri Destek Hattı"**.

**Build decision:** phone number in the header at all breakpoints (`tel:` link on mobile, plain text
+ click-to-call on desktop). Show it as `0212 XXX XX XX` for TR and `+90 212 XXX XX XX` for EN.

### 3.3 "Teklif Al" is the primary conversion, and the form is short

Real TR forms observed:

| Site | Fields |
|---|---|
| passteknik.com | Adı Soyadı · Email · Telefon · Konu · Mesaj · **KVKK aydınlatma onay kutusu** |
| mimaki.com.tr | firma adı · ad soyad · telefon · **ilgilenilen ürün** · şehir · ülke · posta kodu · **iletişim nedeni** · **mürekkep tercihi** · **daha önce bayi ile görüşüldü mü** · yetkili bayi adı · yorum |
| makinecim.com | CTA literally reads **"Teklif İste"** |

**Build decision (static, no backend):** the recommended field set for Maven's `Teklif Al` —
`Ad Soyad*`, `Firma`, `Telefon*`, `E-posta`, `Şehir`, `İlgilendiğiniz ürün` (pre-filled from the
product page, hidden on the generic form), `Mesaj`, plus a required KVKK consent checkbox linking to
`/kvkk-aydinlatma-metni`. Phone before email — TR B2B buyers give a phone number more readily than an
email. Since there is no backend, wire it to a static-friendly form endpoint (Formspree / Web3Forms /
Vercel Function-free provider) **or** — safer for KVKK — make the primary action WhatsApp/phone and
the form a secondary path. Decide before build; the DOM is the same either way.

### 3.4 Prices: machines hidden, consumables shown, always "+ KDV"

- Machine pages on TR dealer sites show **no price** — CTA is "Bilgi Al" / "Teklif Al" / "Sipariş Ver".
- Consumables **do** show prices, and typically **in USD with "+KDV"**: UV ink quoted at
  *"1000 ml CMYK 45 USD + KDV, beyaz (W) 55 USD + KDV"*; Inktec IURS UV 1000 ml *"$55,00 (2.326,80 TL) +KDV"*.
  ([inkateknik.net](https://inkateknik.net/dijital-baski-murekkepler/uv-murekkpeler), [printec-online.com](https://www.printec-online.com/urun/printec-uv-murekkebi/))
- MRT publishes a flat service price: *"Baskı makineleri için genel bakım ücreti 500 USD"*.

**Build decision:** product data model needs `price: null | {amount, currency, vatIncluded:false}` and
the UI must render `"KDV hariç"` next to any price. USD-denominated pricing is normal and *expected*
for imported machinery — don't "fix" it to TRY. For machines, render the price slot as a
**"Fiyat için teklif alın"** button, not an empty field.

### 3.5 The after-sales promise block is a required page, with specific claims

Verbatim from mrtdijital.com's *Satış Sonrası & Teknik Servis* page:

- *"Makinelerinizi yerleştireceğiniz mekanda yapılacak **ön keşif** ve sonrasında kurulum"*
- *"Eğitim müşterilerimizin isteği doğrultusunda **zaman sınırlaması olmadan**"*
- *"Garanti kapsamında olan makinelerden **servis ücreti talep edilmez**"*
- *"**Yedek parça stoklarımız** her zaman makinenizin ihtiyaç duyacağı parçaları sağlayabilecek…"*
- *"**24 saat içinde** teknik servis gerçekleştirilebilmektedir"*

Other observed patterns: split warranty (**elektronik parçalar 1 yıl, mekanik parçalar 2 yıl**),
*"yerinde teknik servis"*, *"uzaktan yardım"*, *"7/24 teknik destek"*.

**Build decision:** `/teknik-servis` (already exists as a file in the repo) must carry a
**numbered commitment list** — response SLA (saat), warranty split (elektronik/mekanik), what's
covered vs not, spare-parts stock claim, training scope, and a **Servis Talep Formu** with fields
`Firma`, `Yetkili`, `Telefon`, `Makine Modeli`, `Seri No`, `Arıza Açıklaması`. Vague "kaliteli hizmet"
copy is the default TR failure mode; numbers are the differentiator.

### 3.6 Taksit / leasing / finansal kiralama

- Leasing (finansal kiralama) with **12–60 month** terms is the standard way TR SMEs buy this class
  of equipment; İş Leasing runs a dedicated *"2. el pazarı → Matbaa Makineleri"* channel covering
  textile, label, offset and digital printing machines.
  ([isleasing.com.tr](https://m.isleasing.com.tr/hizmetlerimiz/2-el-pazari/matbaa-makineleri/))
- Credit-card instalment ("kredi kartına taksitle") is advertised by machine sellers.
- Leasing contracts carry tax/fee exemptions that are a genuine buying argument for KOBİ customers.

**Build decision:** a short **"Ödeme ve Finansman"** block on every product page and a dedicated
`/finansman` page: *Peşin · Kredi kartına taksit · Finansal kiralama (leasing) · Takas (trade-in)*.
Do **not** state specific KOSGEB grant amounts — I could not verify any current KOSGEB programme
covering digital printing machine purchase, and stale grant figures destroy credibility.

### 3.7 Trust signals TR buyers scan for

Ranked by how consistently they appear on the sites I reviewed:

1. **"İthalatçı firma" / "Türkiye distribütörü" / "yetkili bayi"** — serfoto leads with
   *"İthalatçı Firma & Satış Sonrası Destek"*; Prodigital leads with *"2012'den beri MUTOH'un
   Türkiye distribütörü"*.
2. **Years in business** — "20 yıllık tecrübe", "25 yıldır" appear in title tags.
3. **Physical address with district** (Ataşehir, Esenler, Beylikdüzü, Giyimkent) — proves showroom.
4. **Bayilik Başvurusu** page — signals the company is upstream in the chain, not a reseller.
5. **Referanslar / müşteri logoları.**
6. **Fuar presence** — SIGN İstanbul is *the* credential. The 27th edition runs
   **23–26 September 2026 at İstanbul Fuar Merkezi (İFM)**; FESPA Eurasia 2026 runs **9–12 July 2026**.
   ([ifm.com.tr](https://ifm.com.tr/tr/fuarlar/sign-istanbul-endustriyel-reklam-ve-dijital-baski-teknolojileri-fuari-2026), [signistanbul.com](https://www.signistanbul.com/))
7. **Support/download depth** — Mimaki Eurasia's *Yüklemeler ve Destek* menu is the gold standard:
   *İndirme Merkezi · MSDS · Teknik Yüklemeler · Renk Profilleri (MMCP) · SSS · Destek Videoları ·
   Bayi bul*. A **MSDS / Güvenlik Bilgi Formu** download per ink is a real B2B requirement, not decoration.

### 3.8 Nav patterns worth copying

| Site | Top nav |
|---|---|
| mekadijital.com | Ana Sayfa · Hakkımızda · Dijital Baskı Makineleri · DTF Malzemeleri · Dijital Baskı Boyaları · Yedek Parça · İletişim |
| mrtdijital.com | Anasayfa · Kurumsal · Ürünler · Hizmetler · Bizden Haberler · İletişim |
| prodigital.com.tr | Sign Reklam Dijital Baskı Makineleri · UV Dijital Baskı Makineleri · Tekstil Baskı · Halı Baskı Sistemleri · Dijital Kesim Sistemleri · **Boyalar ve Sarf Malzemeler** · İletişim |
| lazerpol.com | LAZER MAKİNELERİ · LAZER YEDEK PARÇALARI · OTOMASYON · BASKI MAKİNELERİ · ÖZEL ÇÖZÜMLER · **İKİNCİ EL** · **AKADEMİ** |
| mimaki.com.tr | Ürünler · Haberler ve Etkinlikler · Yüklemeler ve Destek · Mimaki Hakkında · İletişim |

**Recommended Maven nav (TR):**
`Kurumsal` · `Makineler` · `Mürekkep ve Sarf` · `Yedek Parça` · `Teknik Servis` · `Referanslar` · `İletişim`
— with `Teklif Al` as a visually distinct button, and a phone + WhatsApp pair pinned right.
(The repo already has `kurumsal.html`, `urunler.html`, `teknik-servis.html`, `iletisim.html` —
split `urunler` into machines vs consumables; that split is universal in this market.)

---

## 4. Legal / compliance for a **non-e-commerce** Turkish corporate site

### 4.1 Required — build these

| Item | Why | Applies to us? |
|---|---|---|
| **KVKK Aydınlatma Metni** (general, incl. website visitors) | KVKK m.10 disclosure duty triggers the moment we collect a name/phone via a form | **YES** |
| **Form-level KVKK notice + consent checkbox** | Real TR practice: passteknik.com's contact form has *"Kişisel verilerin işlenmesine ilişkin Aydınlatma Metnini okudum"* as a required checkbox | **YES** on every form |
| **Çerez Politikası / Çerezlere Dair Aydınlatma Metni** | Mandatory even for consent-exempt cookies — the disclosure duty survives. KVKK publishes a model text and a 61-page *Çerez Uygulamaları Hakkında Rehber* (final version 20 June 2022) | **YES** |
| **Opt-in cookie banner** (non-essential cookies OFF by default) | Kurul decision **2022/1358** (23/12/2022): explicit consent must be obtained via an *"opt-in"* mechanism where cookies do not run by default; a **300.000 TL** fine was imposed for processing via non-essential cookies without a legal basis | **YES — if we load analytics.** If we ship zero non-essential cookies, we still need the çerez aydınlatma metni but need no consent banner. **Strong recommendation: ship no analytics cookies** (use a cookieless analytics option or none) — it removes the banner, the CMP, and the risk in one move, and it fits the "minimal, high-craft" brief |
| **Footer corporate identity block** | TTK m.39/2 requires traders to show ticaret unvanı, MERSİS (or ticaret sicil) numarası, işletme merkezi on commercial documents/website; TR corporate sites conventionally add Vergi Dairesi + VKN | **YES** — cheap, and it is a trust signal (§3.7) |
| **İletişim page with full postal address, landline, KEP (if we have one)** | Convention + TTK identity | **YES** |

### 4.2 NOT required — do not add (adding them is a tell that the site was copy-pasted)

| Item | Verdict |
|---|---|
| **Mesafeli Satış Sözleşmesi** | **NO.** Only for distance contracts with *consumers* under 6502. We sell B2B capital equipment and take no online orders. |
| **Ön Bilgilendirme Formu** | **NO.** Same reason — it is a pre-payment consumer document. |
| **ETBİS kaydı / ETBİS logosu** | **NO.** ETBİS registration binds hizmet sağlayıcı/aracı hizmet sağlayıcı who actually *sell* online; a purely promotional corporate site with no sales flow has no obligation. ([parasut.com](https://www.parasut.com/blog/elektronik-ticaret-sitelerinin-etbise-kayit-zorunlulugu), [ataylaravukatlik.av.tr](https://ataylaravukatlik.av.tr/e-ticaret-sitem-icin-etbis-sistemine-kayit-zorunlulugum-var-midir/)) **This flips the moment we add a cart or an online-payment link.** |
| **İade / Teslimat / Gizlilik-Güvenlik (ödeme) politikaları** | **NO** while non-e-commerce. |
| **VERBİS kaydı** | **Probably not.** Data controllers with <50 employees **and** annual balance-sheet total under **100 million TL** (raised from 25M TL) whose core activity is not special-category data are exempt. A dealership almost certainly qualifies for the exemption — but this is the client's call with their mali müşavir, not ours. ([erdem-erdem.av.tr](https://www.erdem-erdem.av.tr/bilgi-bankasi/verbis-kayit-yukumlulugune-iliskin-yeni-istisnalarin-uygulama-esaslari-aciklandi)) |

### 4.3 Conditional

- **İYS (İleti Yönetim Sistemi)** — only if we send marketing SMS/e-mail/calls. A newsletter signup
  on the site pulls us into the ticari elektronik ileti regime. **Recommendation: no newsletter in v1.**
- **TTK m.1524 tescilli internet sitesi** — the *mandatory registered website* obligation applies to
  bağımsız denetime tabi sermaye şirketleri. A typical dealership is not; if the client is, the site
  must carry a dedicated "Bilgi Toplumu Hizmetleri" section, which is a different beast. **Ask the client.**

### 4.4 Concrete page list to ship

```
/kvkk-aydinlatma-metni      (EN: /en/privacy-notice)
/cerez-politikasi           (EN: /en/cookie-policy)
/kullanim-kosullari         (EN: /en/terms-of-use)   ← optional but cheap
footer block: Unvan · Adres · Tel · E-posta · Vergi Dairesi/VKN · MERSİS No · Ticaret Sicil No
```

Real-world footer legal-link sets for comparison: Mimaki Eurasia ships
*Gizlilik Politikası · Feragatname · Çerez Bilgilendirme · Telif Hakkı*; Prodigital ships
*Gizlilik Politikamız · Hakkımızda · Bize Ulaşın*.

Primary sources:
<https://www.kvkk.gov.tr/Icerik/7595/2022-1358> ·
<https://www.kvkk.gov.tr/SharedFolderServer/CMSFiles/fb193dbb-b159-4221-8a7b-3addc083d33f.pdf> ·
<https://www.kvkk.gov.tr/yayinlar/cerezlere_dair_aydinlatma_metni.pdf>

---

## 5. Print heads and machine brands — how they are sold in Turkey

### 5.1 The head is the headline

In this market the **printhead brand and count is part of the product name**, not a buried spec.
Real product titles observed:

- "Greenjet **Epson i3200** – 180cm **2 Kafa**" (istanbulreklam.com)
- "Partner Orion Plus **StarFire / 10 PL** ( **2-4 Kafa** )" — note the drop size in the *title*
- "Orion Plus **Konica 1024i** 3.20m" · "Partner Orion Pro **Konica 1024i** 5.30m"
- "SIHEDA SHD-1216 — 3× **Epson i3200 / Ricoh G5i**" (mekadijital.com)
- "CenturyStar CSP-3200 — 320 cm, **8× Epson I3200**"
- "2513 UV Düz Yatak Yazıcı **Toshiba CE4 / Ricoh Gen5 / Ricoh Gen6 / Konica 1024i**" — sold as a
  *selectable* head option on one chassis

**Build decision:** `printhead` must be a **first-class, filterable product attribute** with
`{brand, model, count, dropSizePl}` — and it must appear in the product card, not only the spec table.
Also model the case where **one chassis offers several head options** (`headOptions: []`), because
that is how the Chinese-built machines that dominate the TR mid-market are actually sold.

### 5.2 Head families and their TR marketing angle

| Head | TR marketing angle | Verified detail |
|---|---|---|
| **Epson i3200** (A1 / E1 / U1) | The volume default. Sold on *availability + price + versatility*. Meka markets the three variants explicitly: **A1** *"Su bazlı ve DTF sıvıları için ideal"*, **E1** *"Eco solventlere uygun"*, **U1** *"UV mürekkepler ve kür sistemleri"* | 3.200 nozül total (8 sıra × 400); etkin baskı genişliği **33,8 mm**; 600 dpi native (up to 1440 dpi modes); damla **2.5 pL min** / 3.8–9.4 pL range; viskozite 3–4 mPa·s; PrecisionCore MEMS → *"yüksek döngü ömrü"* |
| **Epson XP600 (DX11) / TX800 (DX10)** | Entry tier. Sold on **cheap to replace** — the honest pitch in TR is head *replacement cost*, not performance | Sold as bare heads on lazerpol/inkmarketi |
| **Epson DX5 / DX7** | Legacy but still traded; DX5 remains a spec line on eco-solvent machines and a big spare-parts SKU | mrtdijital's live spec: *"Epson Dx5 / 2-3-4 Kafa"* |
| **Ricoh Gen5 / Gen5i / Gen6** | Industrial tier. Sold on **durability + grayscale + UV suitability**, positioned above Epson | Offered as a head option on 2513-class UV flatbeds alongside Toshiba CE4 |
| **Konica Minolta 1024i** | The wide-format solvent workhorse (3.2 m / 5.3 m machines). Sold on **speed at width** | Orion Plus/Pro product lines; 2880×2400 DPI claimed on RTR machines |
| **Kyocera** | Top tier, single-pass / high-speed industrial. Sold on **throughput and head life** | Listed among heads carried by centerdesign.com |
| **Toshiba CE4** | UV flatbed premium option | Explicit head option on 2513 UV flatbed listings |
| **StarFire / Spectra Polaris / Seiko 510-35PL / Xaar** | Older industrial solvent heads; still a live spare-parts market | inkmarketi + centerdesign carry them |

### 5.3 Machine brands present in the Turkish market

- **Japanese/Western majors with TR presence:** Mimaki (Mimaki Eurasia, Beylikdüzü — own TR entity),
  Roland (via Promakim), Mutoh (via Prodigital, TR distributor since 2012), Epson, Konica Minolta
  (own TR entity for production print), Ricoh, Riso, HP, Agfa.
- **Chinese/other volume brands sold by TR dealers:** SIHEDA, CenturyStar, Galaxy, Flora, Gongzheng,
  Phaeton, Taimes, Signtstar, MyColor, DOCAN, Skytec, Dilli, Crystek, JWEI (cutting), PowerJet.
- **Ink brands:** Jetbest, Galaxy, InkTec, Sun Chemical, Mimaki, Triangle, Neom Ink, Printec.

**Build decision:** the product model needs `brand` **and** `oemSourced: boolean` — because a
credible Maven positioning is *"we import and support X and Y, and we stock heads/inks for everything
else"*. Also: a **`Markalar` logo strip** is expected; TR buyers read it as authorisation.

### 5.4 What to *avoid* claiming

Do not write "yetkili distribütör" / "Türkiye distribütörü" for any brand unless the client actually
holds the agreement — Prodigital and Mimaki Eurasia state theirs precisely and dated, and the market
notices. Use "**tedarik ediyoruz**" / "**stoklarımızda bulunur**" for non-exclusive lines.

---

## 6. Content the site needs that TR competitors do badly (our opening)

1. **Real comparison content.** "Eko solvent mi, UV mi?" / "DTF mi, süblimasyon mu?" — informational
   intent (#42) is barely served in Turkish by anyone with authority. A clean comparison table per
   pair, with our own machines linked, is cheap and ranks.
2. **Sarf tüketim hesaplayıcı** — a static JS calculator: m²/gün × mürekkep g/m² → aylık mürekkep
   maliyeti. No backend needed; it is exactly the kind of thing a dealer site never builds and a
   buyer screenshots.
3. **Spec comparison across our own catalogue** — a "Makine Karşılaştır" table (2–3 machines side by
   side) built from the same static JSON. Zero TR competitors do this well.
4. **The 3D model** (already in scope) is genuinely unique in this market — no Turkish dealer site
   has one. Pair it with a callout labelled *"Makineyi 360° inceleyin"*.
5. **Honest "what's not included"** on every machine: nakliye, forklift/vinç, elektrik altyapısı
   (trifaze?), havalandırma, kompresör, sarf başlangıç seti. TR buyers get burned by these and no one
   publishes them.

---

## 7. Sources

1. <https://www.mekadijital.com/> — nav, machine + spare-part taxonomy, product naming
2. <https://www.mekadijital.com/urun-kategori/dijital-baski-makineleri/> — product line & head options
3. <https://www.mekadijital.com/blog-yazilar/epson-i3200-baski-kafasi-ozellikleri/> — i3200 TR spec vocabulary
4. <https://mrtdijital.com/urun/solvent--ecosolvent-baski-makineleri/1/signtstar-epson-i3200--dx5--xp600-ecosolvent-yazici.html> — full TR spec-table field names
5. <https://mrtdijital.com/hizmet/2/satis-sonrasi--teknik-servis.html> — verbatim after-sales promises
6. <https://lazerpol.com/urun/rulodan-ruloya-uv-baski-makinesi/> — spec fields, "Bilgi Al", WhatsApp Destek, 444 line
7. <https://lazerpol.com/urunler/uv-printer/> — nav incl. İKİNCİ EL / AKADEMİ, printhead SKUs
8. <https://www.prodigital.com.tr/mutoh-uv-baski-makineleri/> — nav, "Boyalar ve Sarf Malzemeler", hibrit/RTR widths
9. <https://www.makinaturkiye.com/passreklam> — category vocabulary, consumables terms
10. <https://istanbulreklam.com/dijital-baski-makineleri/> — head-in-title naming, WhatsApp greeting, Uzaktan Yardım
11. <https://www.mimaki.com.tr/> — nav, support/download taxonomy, "Bayi bul"
12. <https://www.mimaki.com.tr/iletisim/> — quote-form field set, legal footer links
13. <https://makinecim.com/dijital-baski-makinasi> — marketplace facets (Sıfır / 2. El / Kiralık), "Teklif İste"
14. <https://www.turkprinting.com/tr/kategori/dijital-baski-makinasi-21> — sıfır/ikinci el listing convention
15. <https://www.passteknik.com/iletisim-formu> — contact-form fields + KVKK checkbox wording
16. <https://www.inkmarketi.com/product/category&path=135> — ink/head/spare taxonomy, "İnk Boya Mürekkep" stacking
17. <https://serfoto.com.tr/dtf-uv-baski-sistemleri> — "İthalatçı Firma & Satış Sonrası Destek", Bayilik Başvurusu
18. <https://www.jetmalzeme.com/kategori/mesh-vinil-branda> / <https://www.jetmalzeme.com/kategori/dekota-foreks> — substrate vocabulary
19. <https://print.bestreklam.com.tr/branda-ve-vinil-baski-m2-fiyatlari-isikli-delikli-ve-branda-afis/> — media naming + TR m² pricing conventions
20. <https://www.matkagit.com.tr/rip-yazilimi-nedir-baski-atolyelerinde-hiz-ve-kaliteyi-nasil-artirir/> — RIP/ripleme vocabulary
21. <https://www.centerdesign.com/40-yazici-kafalari> — head brand range carried in TR
22. <https://tr.made-in-china.com/co_crystek/product_2513-UV-Flatbed-Printer-Toshiba-CE4-Ricoh-Gen6-Printhead_uosiouyhog.html> — selectable head options, TR-language listing
23. <https://www.kvkk.gov.tr/Icerik/7595/2022-1358> — Kurul 2022/1358, opt-in requirement, 300.000 TL fine
24. <https://www.kvkk.gov.tr/SharedFolderServer/CMSFiles/fb193dbb-b159-4221-8a7b-3addc083d33f.pdf> — Çerez Uygulamaları Hakkında Rehber (20.06.2022)
25. <https://www.kvkk.gov.tr/yayinlar/cerezlere_dair_aydinlatma_metni.pdf> — model cookie disclosure text
26. <https://www.parasut.com/blog/elektronik-ticaret-sitelerinin-etbise-kayit-zorunlulugu> — ETBİS scope
27. <https://ataylaravukatlik.av.tr/e-ticaret-sitem-icin-etbis-sistemine-kayit-zorunlulugum-var-midir/> — ETBİS: no obligation without actual online sales
28. <https://www.erdem-erdem.av.tr/bilgi-bankasi/verbis-kayit-yukumlulugune-iliskin-yeni-istisnalarin-uygulama-esaslari-aciklandi> — VERBİS exemption thresholds (<50 employee, <100M TL)
29. <https://www.verginet.net/dtt/11/Vergi-Sirkuleri-2013-110.aspx> — TTK m.39 commercial-document/website identity requirements
30. <https://www.hukukegitim.com/makale-web-sitelerinde-bulunmasi-gereken-yasal-prosedurler-ve-metinler-100> — TR website legal-text layers
31. <https://www.bloomberght.com/turkiyede-en-cok-kullanilan-uygulama-whatsapp-oldu-2359054> — WhatsApp 88.6% (TÜİK)
32. <https://avangardreklam.com/blog/turkiye-dijital-pazarlama-istatistikleri-2026/> — TR digital stats 2026, 58.5M WhatsApp MAU
33. <https://ifm.com.tr/tr/fuarlar/sign-istanbul-endustriyel-reklam-ve-dijital-baski-teknolojileri-fuari-2026> — SIGN İstanbul 2026, 23–26 Eylül, İFM
34. <https://www.signistanbul.com/> — SIGN İstanbul positioning + exhibitor names
35. <https://www.fespaeurasia.com.tr/> — FESPA Eurasia
36. <https://m.isleasing.com.tr/hizmetlerimiz/2-el-pazari/matbaa-makineleri/> — leasing for printing machinery, 2. el channel
37. <https://inkateknik.net/dijital-baski-murekkepler/uv-murekkpeler> — UV ink USD+KDV pricing convention
38. <https://www.printec-online.com/urun/printec-uv-murekkebi/> — UV ink 1000 ml pricing
39. <https://www.dtfturkiye.com/transfer-baski-tozu> / <https://serfoto.com.tr/dtf-sarf-malzemeleri> — DTF consumable vocabulary
40. <https://www.baskikafatamiri.com/kategori/konica-minolta/> — "baskı kafası tamiri" as a standalone demand
