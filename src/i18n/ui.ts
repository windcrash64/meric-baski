/**
 * UI strings.
 *
 * Anything a human reads that is not product content lives here. Turkish is
 * written first because it is the primary market and because TR copy runs
 * 15-20% longer than EN — designing against the Turkish string is the only way
 * a card or button survives translation.
 */

import type { Locale } from '../config/site';

type Dict = Record<Locale, string>;

export const UI = {
  /* --- chrome ---------------------------------------------------------- */
  skipToContent: { tr: 'İçeriğe geç', en: 'Skip to content' },
  menu: { tr: 'Menü', en: 'Menu' },
  close: { tr: 'Kapat', en: 'Close' },
  openMenu: { tr: 'Menüyü aç', en: 'Open menu' },
  closeMenu: { tr: 'Menüyü kapat', en: 'Close menu' },
  languageLabel: { tr: 'Dil', en: 'Language' },
  switchToEnglish: { tr: "English'e geç", en: 'Switch to English' },
  switchToTurkish: { tr: "Türkçe'ye geç", en: 'Switch to Turkish' },
  home: { tr: 'Ana Sayfa', en: 'Home' },
  breadcrumb: { tr: 'Sayfa yolu', en: 'Breadcrumb' },
  backToTop: { tr: 'Yukarı dön', en: 'Back to top' },

  /* --- navigation ------------------------------------------------------ */
  navMachines: { tr: 'Makineler', en: 'Machines' },
  navInks: { tr: 'Mürekkep & Sarf', en: 'Inks & Supplies' },
  navApplications: { tr: 'Uygulamalar', en: 'Applications' },
  navService: { tr: 'Teknik Servis', en: 'Service' },
  navAbout: { tr: 'Kurumsal', en: 'Company' },
  navContact: { tr: 'İletişim', en: 'Contact' },
  navDocuments: { tr: 'Belgeler ve GBF', en: 'Documents & SDS' },

  /* --- actions --------------------------------------------------------- */
  getQuote: { tr: 'Teklif Al', en: 'Request a Quote' },
  requestQuote: { tr: 'Teklif İsteyin', en: 'Request a Quote' },
  askWhatsApp: { tr: 'WhatsApp ile sor', en: 'Ask on WhatsApp' },
  callUs: { tr: 'Bizi arayın', en: 'Call us' },
  explore: { tr: 'İncele', en: 'Explore' },
  exploreMachines: { tr: 'Makineleri İncele', en: 'Explore Machines' },
  viewAll: { tr: 'Tümünü gör', en: 'View all' },
  readMore: { tr: 'Devamını oku', en: 'Read more' },
  downloadCatalog: { tr: 'Katalog İndir', en: 'Download Catalogue' },
  requestSample: { tr: 'Numune İste', en: 'Request a Sample' },
  requestDemo: { tr: 'Demo Talep Et', en: 'Request a Demo' },
  serviceRequest: { tr: 'Servis Talebi Oluştur', en: 'Create a Service Request' },
  compare: { tr: 'Karşılaştır', en: 'Compare' },
  showFullList: { tr: 'Tam listeyi aç', en: 'Show the full list' },
  openTable: { tr: 'Tüm tabloyu aç', en: 'Open the full table' },
  getDirections: { tr: 'Yol tarifi al', en: 'Get directions' },
  send: { tr: 'Gönder', en: 'Send' },

  /* --- product --------------------------------------------------------- */
  models: { tr: 'model', en: 'models' },
  specifications: { tr: 'Teknik Özellikler', en: 'Specifications' },
  description: { tr: 'Açıklama', en: 'Description' },
  technicalData: { tr: 'Teknik Veriler', en: 'Technical Data' },
  features: { tr: 'Özellikler', en: 'Features' },
  applications: { tr: 'Uygulamalar', en: 'Applications' },
  gallery: { tr: 'Görseller', en: 'Gallery' },
  view3d: { tr: '3D Görünüm', en: '3D View' },
  explore3d: { tr: '360° İNCELE', en: '360° EXPLORE' },
  resetView: { tr: 'Sıfırla', en: 'Reset' },
  loading3d: { tr: '3D model yükleniyor', en: 'Loading 3D model' },
  load3dManually: { tr: '3D modeli yükle', en: 'Load the 3D model' },
  priceOnRequest: { tr: 'Fiyat için teklif alın', en: 'Price on request' },
  vatExcluded: { tr: 'KDV hariç', en: 'excl. VAT' },
  compatibleInks: { tr: 'Uyumlu Mürekkepler', en: 'Compatible Inks' },
  compatibleMachines: { tr: 'Bu mürekkebi kullanan makineler', en: 'Machines using this ink' },
  validatedMachines: { tr: 'Doğrulanmış Makineler', en: 'Validated Equipment' },
  compatiblePrintheads: { tr: 'Uyumlu Baskı Kafaları', en: 'Compatible Printheads' },
  similarMachines: { tr: 'Benzer Makineler', en: 'Similar Machines' },
  installRequirements: { tr: 'Kurulum Gereksinimleri', en: 'Installation Requirements' },
  notIncluded: { tr: 'Fiyata dahil değildir', en: 'Not included in the price' },
  substrates: { tr: 'Uygulanabilir Malzemeler', en: 'Compatible Substrates' },
  surfaces: { tr: 'Uygulanabilir Yüzeyler', en: 'Suitable Surfaces' },
  documents: { tr: 'İndirilebilir Dosyalar', en: 'Downloads' },
  videos: { tr: 'Videolar', en: 'Videos' },
  financing: { tr: 'Ödeme ve Finansman', en: 'Payment & Financing' },
  warrantyService: { tr: 'Servis ve Garanti', en: 'Service & Warranty' },
  faq: { tr: 'Sıkça Sorulan Sorular', en: 'Frequently Asked Questions' },
  systemComponents: { tr: 'Sistem Bileşenleri', en: 'System Components' },
  channels: { tr: 'Renk Kanalları', en: 'Colour Channels' },
  packaging: { tr: 'Ambalaj', en: 'Packaging' },
  onRequest: { tr: 'talep üzerine', en: 'on request' },
  inStock: { tr: 'stokta', en: 'in stock' },
  metric: { tr: 'Metrik', en: 'Metric' },
  imperial: { tr: 'İnç', en: 'Imperial' },
  passMode: { tr: 'geçiş', en: 'pass' },

  /* --- changeover badges ------------------------------------------------ */
  switchAndPrint: { tr: 'Doğrudan geçiş', en: 'Switch & Print' },
  switchAndSwap: { tr: 'Yıkama gerekir', en: 'Switch & Swap' },
  switchAndMatch: { tr: 'Profil gerekir', en: 'Switch & Match' },

  /* --- applications ------------------------------------------------------ */
  machinesForThis: { tr: 'Bu işi yapan makineler', en: 'Machines that do this work' },
  inksUsed: { tr: 'Kullanılan mürekkepler', en: 'Inks used' },
  substratesApplied: { tr: 'Uygulanan malzemeler', en: 'Materials printed' },
  machineMatrix: {
    tr: 'Sektör – makine ailesi eşleşme tablosu',
    en: 'Sector – machine family matrix',
  },
  suitable: { tr: 'uygun', en: 'suitable' },
  notSuitable: { tr: 'uygun değil', en: 'not suitable' },

  /* --- forms ------------------------------------------------------------ */
  formName: { tr: 'Ad Soyad', en: 'Full name' },
  formCompany: { tr: 'Firma', en: 'Company' },
  formPhone: { tr: 'Telefon', en: 'Phone' },
  formEmail: { tr: 'E-posta', en: 'E-mail' },
  formCity: { tr: 'Şehir', en: 'City' },
  formProduct: { tr: 'İlgilendiğiniz ürün', en: 'Product of interest' },
  formMessage: { tr: 'Mesaj', en: 'Message' },
  formMachineModel: { tr: 'Makine Modeli', en: 'Machine model' },
  formSerial: { tr: 'Seri No', en: 'Serial number' },
  formFault: { tr: 'Arıza Açıklaması', en: 'Fault description' },
  formAddress: { tr: 'Adres', en: 'Address' },
  formContactPerson: { tr: 'Yetkili Kişi', en: 'Contact person' },
  formSubjectArea: { tr: 'Konu', en: 'Subject' },
  formInterest: { tr: 'Hangi makine veya mürekkep', en: 'Which machine or ink' },
  formSubstrate: { tr: 'Basılacak malzeme', en: 'Material to be printed' },
  formSelect: { tr: 'Seçiniz', en: 'Select' },
  formOther: { tr: 'Diğer', en: 'Other' },
  formRequired: { tr: 'zorunlu alan', en: 'required' },
  /** The phrase inside `formKvkkConsent` that becomes the link to the notice. */
  formKvkkLink: { tr: 'KVKK Aydınlatma Metni', en: 'privacy notice' },
  formKvkkConsent: {
    tr: 'KVKK Aydınlatma Metni’ni okudum ve kişisel verilerimin işlenmesini onaylıyorum.',
    en: 'I have read the privacy notice and consent to the processing of my personal data.',
  },
  formAfterSubmit: {
    tr: 'Formu gönderdiğinizde 1 iş günü içinde bir satış mühendisimiz sizi arar. Acil ihtiyaçlar için WhatsApp daha hızlıdır.',
    en: 'A sales engineer will call you within one business day. For urgent needs WhatsApp is faster.',
  },
  formError: {
    tr: 'Form gönderilemedi. Lütfen telefon veya WhatsApp ile ulaşın.',
    en: 'The form could not be sent. Please reach us by phone or WhatsApp.',
  },
  formSending: { tr: 'Gönderiliyor…', en: 'Sending…' },

  /* --- gallery / carousel a11y ------------------------------------------ */
  carousel: { tr: 'görsel galerisi', en: 'image gallery' },
  slide: { tr: 'görsel', en: 'slide' },
  previous: { tr: 'Önceki', en: 'Previous' },
  next: { tr: 'Sonraki', en: 'Next' },
  pause: { tr: 'Duraklat', en: 'Pause' },
  play: { tr: 'Oynat', en: 'Play' },

  /* --- service & company ------------------------------------------------- */
  serviceCoverage: { tr: 'Yerinde Servis Kapsamı', en: 'On-Site Service Coverage' },
  installTraining: { tr: 'Kurulum ve Eğitim', en: 'Installation & Training' },
  warrantyTerms: { tr: 'Garanti Koşulları', en: 'Warranty Terms' },
  brandsSupply: { tr: 'Markalar ve Tedarik', en: 'Brands & Supply' },

  /* --- legal ------------------------------------------------------------ */
  lastUpdated: { tr: 'Son güncelleme', en: 'Last updated' },
  privacyNotice: { tr: 'KVKK Aydınlatma Metni', en: 'Privacy Notice' },
  cookiePolicy: { tr: 'Çerez Politikası', en: 'Cookie Policy' },
  termsOfUse: { tr: 'Kullanım Koşulları', en: 'Terms of Use' },

  /* --- misc ------------------------------------------------------------- */
  notFoundTitle: { tr: 'Sayfa bulunamadı', en: 'Page not found' },
  notFoundBody: {
    tr: 'Aradığınız sayfa taşınmış veya hiç var olmamış olabilir. Aşağıdan devam edebilirsiniz.',
    en: 'The page you were looking for has moved or never existed. You can continue from here.',
  },
  workingHours: { tr: 'Çalışma Saatleri', en: 'Working hours' },
  closed: { tr: 'Kapalı', en: 'Closed' },
  address: { tr: 'Adres', en: 'Address' },
  phone: { tr: 'Telefon', en: 'Phone' },
  email: { tr: 'E-posta', en: 'E-mail' },
  allRightsReserved: { tr: 'Tüm hakları saklıdır.', en: 'All rights reserved.' },
  imageCredits: {
    tr: 'Görseller: Pexels ve Unsplash katkıda bulunanları. Makine görselleri Maven tarafından üretilmiştir.',
    en: 'Photography: Pexels and Unsplash contributors. Machine imagery produced by Maven.',
  },
  quickLinks: { tr: 'Hızlı Erişim', en: 'Quick links' },
  support: { tr: 'Destek', en: 'Support' },
} as const satisfies Record<string, Dict>;

export type UIKey = keyof typeof UI;

/** `t('getQuote', locale)` — the only way a UI string reaches a template. */
export function t(key: UIKey, locale: Locale): string {
  return UI[key][locale];
}

/** Number formatting. TR uses `.` for thousands and `,` for decimals. */
export function num(value: number, locale: Locale, opts: Intl.NumberFormatOptions = {}): string {
  return new Intl.NumberFormat(locale === 'tr' ? 'tr-TR' : 'en-GB', opts).format(value);
}

/**
 * Units that are written WITHOUT a thousands separator in this trade.
 *
 * Turkish groups thousands with a full stop, so a 3200 mm print width formats
 * as "3.200 mm" — grammatically correct, and wrong here twice over: every real
 * spec sheet in the industry writes "3200 mm" and "1440 dpi", and a reader used
 * to a decimal point can read "3.200 mm" as 3.2 mm. Dimensions and resolutions
 * are identifiers as much as quantities; masses and areas are not, and keep
 * their separator.
 */
const UNGROUPED_UNITS =
  /^(mm|cm|dpi|npi|nm|pl|µm|um|mikron|px|rpm|hz|khz)(\s*\/\s*(s|sn|dk|min|h|sa))?$/i;

/** Render a scalar or a [min, max] range with locale-correct separators. */
export function range(
  value: number | [number, number],
  locale: Locale,
  unit?: string,
): string {
  const opts: Intl.NumberFormatOptions =
    unit && UNGROUPED_UNITS.test(unit.trim()) ? { useGrouping: false } : {};
  return Array.isArray(value)
    ? `${num(value[0], locale, opts)}–${num(value[1], locale, opts)}`
    : num(value, locale, opts);
}

/** File size for a download link: "PDF · 2,4 MB". */
export function fileSize(bytes: number, locale: Locale): string {
  const mb = bytes / 1024 / 1024;
  return mb >= 1
    ? `${num(mb, locale, { maximumFractionDigits: 1 })} MB`
    : `${num(bytes / 1024, locale, { maximumFractionDigits: 0 })} KB`;
}
