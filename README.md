# Maven — dijital baskı makineleri ve mürekkep

Kurumsal tanıtım sitesi. Backend yok: Astro ile statik üretilir, Vercel'de yayınlanır.
Türkçe kök dizinde, İngilizce `/en/` altında.

**Canlı:** https://meric-baski.vercel.app
**Production dalı:** `claude/dijital-baski-website-9563dx` — `main` değil.
İkisi de aynı commit'te tutulur; push ederken ikisine birden gönderin.

---

## Hızlı başlangıç

```bash
npm install
npm run dev            # http://localhost:4321
```

`npm run build` üç adımı sırayla çalıştırır:

1. `tools/build-images.mjs` — `assets/renders/` altındaki PNG'lerden AVIF+WebP+JPEG
   merdivenini üretir ve `public/img/manifest.json`'ı yazar
2. `tools/build-og.mjs` — `brand/*.svg`'den paylaşım kartı, yayıncı logosu, iOS ikonu
3. `astro build` — 121 sayfa

Vercel de bu zinciri çalıştırır, yani görseller repoda tutulmaz.

## Gereksinimler

| | sürüm | ne için |
|---|---|---|
| Node | ≥ 22.12 | zorunlu (`engines` alanında) |
| Blender | 5.1 | yalnızca makine render'ı / GLB üretimi |
| Python + uv | 3.12 | yalnızca `npm run brand` (logo vektörlerini yeniden üretir) |

Blender ve Python **siteyi derlemek için gerekmez** — kaynak render'lar ve marka
vektörleri repoda. Yalnızca yeni bir makine modellerken lazım.

### Windows / Git Bash tuzağı

`fnm` kabuk profilinden çözülmediğinde `node` bulunamaz ve hata mesajı yanıltıcıdır
("We can't find the necessary environment variables"). Her Bash oturumunda:

```bash
eval "$(fnm env --shell bash)"
```

PowerShell'de bu gerekmez.

---

## Repoda ne var, ne yok

**Var** — kaynak Blender render'ları (`assets/renders/`), marka vektörleri (`brand/`),
alt kümelenmiş fontlar (`public/fonts/`), 3B modeller (`public/models/*.glb`),
`<model-viewer>` kopyası (`public/vendor/`), ve `docs/research/` altında 113 KB'lık
build spesifikasyonu.

**Yok** (yeniden üretilir) — `public/img/**` görsel merdiveni, `dist/`, `node_modules/`.
`public/img/manifest.json` bilinçli olarak takip edilir: şablonlar onu build sırasında
import eder.

---

## Dizinler

```
src/content/      makine ve mürekkep verisi (YAML, Zod ile doğrulanır)
src/layouts/      sayfa şablonları — bir şablon, bir sayfa türü
src/components/   Astro bileşenleri
src/i18n/         rota slug haritası, arayüz metinleri, teknik terimler
src/styles/       tokens / base / layout / motion
src/scripts/      progressive enhancement (astro:page-load'a bağlı)
blender/          parametrik makine modelleri (Python), stüdyo ve shading kütüphanesi
tools/            görsel işleme, marka, denetim betikleri
docs/research/    00-SPEC.md yetkili build spesifikasyonu
```

## Araçlar

```bash
node tools/build-images.mjs [--force]        # görsel merdiveni
node tools/build-og.mjs                      # paylaşım görselleri
node tools/audit-responsive.mjs <url> [yol…] # 10 gerçek viewport'ta ölçüm
node tools/glb-anchors.mjs <file.glb> [ad…]  # GLB'den hotspot koordinatı
```

`audit-responsive.mjs` derlenmiş çıktıya karşı çalışır (`dist/` sunun ya da canlı
URL verin) ve hero sığmasını, yatay taşmayı, ray navigasyonunu ve sayfa uzunluğunu
raporlar. Devtools iki konuda yanıltır: telefon profilinde `vh`'nin tamamını bildirir
(gerçek cihazda ~150px'i tarayıcı çubuğuna gider) ve bayat CSS'i seve seve gösterir.

### Blender

```bash
blender --background --factory-startup --python blender/build_machine.py -- \
  --machine flatbed_uv --render --cutout --look light \
  --engine CYCLES --device GPU --samples 96 --width 2000 --height 1250

blender --background --factory-startup --python blender/build_machine.py -- \
  --machine flatbed_uv --export --glb-name mf-2513-r8.v1
```

Modül adları aile arketipidir (`flatbed_uv`, `roll_uv`, `ecosolvent`, `dtf`);
`--glb-name` modeli yükleyen SKU'nun adını verir.

---

## Bilinen açıklar

- 12 makinenin 8'inde 3B model yok. Bu makineler etiketli bir yer tutucu gösterir —
  aile arkadaşının render'ı **bilerek** gösterilmez (`src/lib/media.ts` yorumuna bakın).
- Fotoğraf yok; uygulama kutuları ikonla çalışır.
- 43 belge (TDS ve GBF) içerik dosyalarında bildirilmiş ama PDF'ler üretilmemiş.
  Satırlar "talep üzerine" olarak görünür; dosya `public/docs/` altına konduğu anda
  kendiliğinden indirme bağlantısına dönüşür. **GBF'ler yasal belgedir, uydurulamaz.**
- Hukuki metinler (KVKK, çerez, kullanım koşulları) avukat incelemesi bekliyor.
- Açık karar: render ölçek politikası. Her makine kendi kadrajını doldurur, yani
  5.95 m'lik MH-3200 ile 1.16 m'lik MD-600 kartta aynı boyda görünür. Ortak dünya
  ölçeği daha dürüst olurdu ama masaüstü modelleri kartta çok küçültür.
