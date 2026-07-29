# Maven sitesi — bu depoda çalışırken

Kurulum ve komutlar için `README.md`. Burası, yalnızca burada geçerli olan kararlar
ve pahalıya öğrenilmiş tuzaklar.

## Dil ve ton

**Reklam dili yok.** Site var olanı anlatır. "Siz isterseniz biz üretiriz",
"sektörün lideri", "en iyi çözüm" gibi cümleler bu projede yanlıştır — müşteri
bunu açıkça iki kez istedi. Başlıklar düz isim öbeği olur: "Teknik Servis",
"Makine – Mürekkep Uyumluluğu". Sayı verilecekse doğrulanabilir olmalı.

Bu kural bir ajan turundan sonra sessizce geri geliyor. Metin üreten bir iş
yaptıysanız sonrasında tarayın.

## Doğrulama

**Ölç, bakma.** Bu projede "düzeldi gibi görünüyor" diye kapatılan her şey geri
geldi. `tools/audit-responsive.mjs` on gerçek viewport'ta ölçer; yeni bir kusur
sınıfı bulursanız oraya ekleyin.

Devtools iki konuda yanıltır:
- Telefon profilinde `vh`'nin tamamını bildirir. Gerçek cihazda o yüksekliğin
  ~150px'i tarayıcı çubuğuna gider — bu yüzden hero `svh` kullanır.
- Bayat CSS'i seve seve gösterir. Ölçmeden önce yeniden build edin ve sorgu
  dizesiyle cache'i atlayın.

**Deploy'u değişen artefaktla doğrulayın, CSS hash'iyle değil.** Yalnızca bir
GLB'ye veya bir script'e dokunan commit CSS'i değiştirmez; hash eşleşir ve
"yayınlandı" dersiniz, oysa değişiklik canlıda değildir. Bu tam olarak yaşandı.

## Değişmez kararlar

- **Aile arkadaşının render'ı gösterilmez.** 600×900 mm masaüstü bir cihazı 2.5 m'lik
  endüstriyel flatbed görseliyle göstermek ürün hakkında yanlış beyandır. Modeli
  olmayan makine etiketli yer tutucu gösterir. Gerekçe `src/lib/media.ts` içinde.
- **Bildirilmiş ≠ üretilmiş.** İçerik dosyası bir GLB veya PDF adı yazabilir; şablon
  dosyanın diskte olup olmadığını build sırasında kontrol eder (`model3dFile`,
  `docExists`). 404'e giden bir "360° model" sekmesi ya da güvenlik bilgi formu
  bağlantısı, hiç sunmamaktan kötüdür.
- **GBF (güvenlik bilgi formu) uydurulamaz.** KKDİK kapsamında yasal belgedir.
- **Cutout görselleri asla kırpılmaz** (`fit="contain"`). Makine içeriğin kendisidir;
  `cover` her ucundan beşte bir kesiyordu. Fotoğraflar `cover` kalır.
- **Sarı dolgu üstünde beyaz metin olmaz.** Sarı kağıtta 1.29:1, mürekkepte 15.22:1.
  Dolu bir accent üstüne yazarken `--on-accent` kullanın, `--accent-text` değil
  (o, zemin üstünde accent renkli METİN içindir).

## Tuzaklar

- **Astro scoped CSS global medya sorgusunu yener.** Kapsam attribute'u özgüllüğü
  0-2-0'a çıkarır. `.tiles`/`.cards` gibi global sözleşmelere sahip bir sınıfı
  bileşende ezmeye çalışmayın; ya `layout.css`'te tanımlayın ya da kendi adını verin.
- **Aynı özgüllükte kaynak sırası karar verir.** `.fit-contain > img` kuralı
  `.ratio-card > img`'den ÖNCE yazıldığında `cover` kazanıyordu.
- **`:where()` sıfır özgüllük demektir.** `ul[role='list'] { padding: 0 }` sıfırlaması
  rayların kendi kenar boşluğunu yiyordu.
- **Bir bileşeni geri alırken ona bağlı script'i de doğrulayın.** Eski hero geri
  getirildiğinde `enhance.ts` yeni işaretlemeye göre yazılıydı: `querySelector`
  bulamayınca `null` döner, `?.addEventListener` sessizce hiçbir şey yapmaz. Build
  geçer, konsol temizdir, düğme ölüdür.
- **Blender Z-up, glTF Y-up.** `(x, y, z)` → `(x, z, -y)`. Eksi düşerse her hotspot
  makinenin ters yüzüne aynalanır. Elle yazmayın: `tools/glb-anchors.mjs` sevk edilen
  GLB'den ölçer.
- **Prosedürel pürüzlülük glTF'e aktarılamaz.** BAĞLI bir soket faktör varsayılanıyla
  yazılır, yani roughness 1.0 — tamamen mat metal parlama yakalamaz ve model siyah
  siluet olur. `export_glb` dışa aktarım süresince bağları söküp geri takar.
- **Cutout'lar saydam; JPEG'in alfası yok.** sharp'ın varsayılan zemini siyahtır.
  Düzleştirmeyi format klonunda yapın, paylaşılan boru hattında değil — yoksa AVIF
  ve WebP de alfasını kaybeder.
- **`--factory-startup` altında Cycles "yok" görünür.** Statik RNA enum'u yalnızca
  yerleşikleri listeler. Eklentiyi etkinleştirip atamayı deneyin; ön kontrol yapmayın.

## Yayınlama

Production dalı `claude/dijital-baski-website-9563dx`, `main` değil. İkisi de aynı
commit'te tutulur:

```bash
git push origin main && git push origin main:claude/dijital-baski-website-9563dx
```

Vercel `npm run build` çalıştırır, yani görsel merdiveni orada üretilir.
