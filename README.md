# Meriç Baskı — Kurumsal Web Sitesi

Dijital baskı makineleri, kesim sistemleri, sarf malzemeleri ve teknik servis
hizmetleri sunan bir firma için hazırlanmış klasik, keskin hatlı kurumsal web
sitesi. Saf HTML/CSS/JS ile geliştirilmiştir; herhangi bir derleme (build)
adımı gerektirmez.

## Sayfalar

| Dosya | Açıklama |
|---|---|
| `index.html` | Anasayfa — hero, ürün grupları, istatistikler, markalar |
| `urunler.html` | Ürün kataloğu — UV flatbed, rulodan ruloya, eko solvent, süblimasyon, kesim sistemleri, sarf malzemeleri |
| `teknik-servis.html` | Teknik servis hizmetleri, servis süreci ve bakım paketleri |
| `kurumsal.html` | Hakkımızda, misyon/vizyon, tarihçe |
| `iletisim.html` | İletişim bilgileri, teklif/servis formu ve harita |

## Yapı

```
├── index.html
├── urunler.html
├── teknik-servis.html
├── kurumsal.html
├── iletisim.html
├── favicon.svg
├── css/
│   └── style.css      # Tüm site stilleri (tek dosya)
└── js/
    └── main.js        # Mobil menü davranışı
```

## Yerelde Çalıştırma

Statik dosyalar olduğu için doğrudan tarayıcıda açılabilir veya basit bir
sunucu ile servis edilebilir:

```bash
npx serve .
# veya
python3 -m http.server 8000
```

## Vercel ile Yayınlama

1. [vercel.com](https://vercel.com) hesabınızla giriş yapın.
2. **Add New → Project** ile bu GitHub reposunu içe aktarın.
3. Framework Preset olarak **Other** seçin; build komutu ve output dizini
   ayarlarını boş bırakın (statik site olarak otomatik yayınlanır).
4. **Deploy** butonuna basın. Sonraki her `git push` otomatik olarak yeniden
   yayınlanır.

## Özelleştirme Notları

- Telefon, e-posta ve adres bilgileri örnek (placeholder) değerlerdir; tüm
  sayfalarda ve `iletisim.html` içinde gerçek bilgilerle güncelleyin.
- Ürün modelleri ve teknik özellik tabloları örnek içeriktir; gerçek makine
  bilgileriyle değiştirin.
- Renk paleti `css/style.css` dosyasının başındaki `:root` değişkenlerinden
  tek noktadan değiştirilebilir.
- İletişim formu şu an `mailto:` ile çalışır; gerçek form gönderimi için
  [Formspree](https://formspree.io) veya benzeri bir servis `action`
  adresine bağlanabilir.
- Harita, örnek koordinatlarla OpenStreetMap embed'i kullanır; gerçek konumla
  güncelleyin.
