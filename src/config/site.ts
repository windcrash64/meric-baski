/**
 * The single source of truth for every fact about the company.
 *
 * No phone number, address, e-mail or legal identifier may appear anywhere else
 * in the codebase. When the client supplies real details, this file is the only
 * one that changes.
 *
 * Placeholders are marked with `TODO` so `tools/check-content.mjs` can list
 * everything still outstanding, and so nothing fake ships silently.
 */

export const LOCALES = ['tr', 'en'] as const;
export type Locale = (typeof LOCALES)[number];
export const DEFAULT_LOCALE: Locale = 'tr';

/** Wraps a value that is still waiting on the client. */
const TODO = (value: string) => `${value}` as const;

export interface Localized<T = string> {
  tr: T;
  en: T;
}

export const SITE = {
  brand: {
    name: 'Maven',
    /** Full legal trade name — required in the footer by TTK m.39/2. */
    legalName: TODO('Maven Dijital Baskı Teknolojileri San. ve Tic. Ltd. Şti.'),
    foundedYear: 2005,
    tagline: {
      tr: 'Dijital baskı makineleri, mürekkep ve teknik servis',
      en: 'Digital printing machines, inks and technical service',
    } satisfies Localized,
  },

  /** Update in one place when the real domain is bought. */
  url: 'https://meric-baski.vercel.app',

  defaultLocale: DEFAULT_LOCALE,
  locales: LOCALES,

  contact: {
    phone: {
      display: { tr: '0212 000 00 00', en: '+90 212 000 00 00' } satisfies Localized,
      e164: '+902120000000',
    },
    mobile: {
      display: { tr: '0532 000 00 00', en: '+90 532 000 00 00' } satisfies Localized,
      e164: '+905320000000',
    },
    whatsapp: {
      e164: '905320000000',
      prefill: {
        tr: 'Merhaba, bilgi almak istiyorum.',
        en: 'Hello, I would like some information.',
      } satisfies Localized,
    },
    email: {
      general: 'info@maven.com.tr',
      sales: 'satis@maven.com.tr',
      service: 'servis@maven.com.tr',
      supplies: 'sarf@maven.com.tr',
      accounting: 'muhasebe@maven.com.tr',
    },
    address: {
      street: TODO('Adres satırı'),
      district: TODO('İlçe'),
      city: 'İstanbul',
      postalCode: TODO('34000'),
      country: 'TR' as const,
      geo: { lat: 41.0082, lng: 28.9784 },
      mapsUrl: TODO('https://maps.google.com/'),
    },
    hours: [
      { days: { tr: 'Pazartesi – Cuma', en: 'Monday – Friday' }, open: '08:30', close: '18:00' },
      { days: { tr: 'Cumartesi', en: 'Saturday' }, open: '09:00', close: '14:00' },
      { days: { tr: 'Pazar', en: 'Sunday' }, open: '', close: '' },
    ],
  },

  /** TTK m.39/2 identity block. Doubles as the cheapest trust signal there is. */
  legal: {
    tradeName: TODO('Maven Dijital Baskı Teknolojileri San. ve Tic. Ltd. Şti.'),
    mersis: TODO('0000000000000000'),
    taxOffice: TODO('Vergi Dairesi'),
    taxNumber: TODO('0000000000'),
    tradeRegistryNo: TODO('000000-0'),
  },

  /** Only ship what exists — an empty social row is worse than none. */
  social: {
    instagram: null as string | null,
    linkedin: null as string | null,
    youtube: null as string | null,
  },

  forms: {
    provider: 'web3forms' as const,
    /** Public by design — Web3Forms access keys are safe in client HTML. */
    accessKey: TODO('00000000-0000-0000-0000-000000000000'),
  },

  /** Rendered on /teknik-servis/ and the homepage proof strip. */
  commitments: {
    responseHours: 24,
    warrantyElectronicMonths: 12,
    warrantyMechanicalMonths: 24,
    onSiteCities: [
      'İstanbul', 'Ankara', 'İzmir', 'Bursa', 'Konya', 'Antalya',
      'Adana', 'Gaziantep', 'Kayseri', 'Denizli', 'Kocaeli', 'Mersin',
    ],
    installationsCount: 600,
    yearsInBusiness: new Date().getFullYear() - 2005,
  },

  /** Null on purpose: zero non-essential cookies means no consent banner. */
  analytics: null,
} as const;

export type SiteConfig = typeof SITE;

/** Everything still carrying a placeholder, for the pre-launch checklist. */
export const OUTSTANDING = [
  'legal.tradeName', 'legal.mersis', 'legal.taxOffice', 'legal.taxNumber',
  'legal.tradeRegistryNo', 'contact.phone', 'contact.mobile', 'contact.whatsapp',
  'contact.email.*', 'contact.address.*', 'forms.accessKey', 'url',
] as const;
