/**
 * The URL segment map.
 *
 * Astro's i18n routing prefixes locales but does NOT translate path segments —
 * `/en/urunler/` is what you get for free, and it is both bad craft and bad SEO.
 * This table is the fix, and it is the only place a slug is written down.
 *
 * The `satisfies` constraint is the guarantee that makes adding a locale safe:
 * put `'ar'` in LOCALES and TypeScript errors on every route that lacks it,
 * rather than silently emitting Turkish URLs under an Arabic prefix.
 */

import { DEFAULT_LOCALE, LOCALES, type Locale } from '../config/site';

export type RouteKey =
  | 'home'
  | 'machines' | 'machines.uvFlatbed' | 'machines.uvHybrid' | 'machines.ecoSolvent'
  | 'machines.dtf' | 'machines.sublimation' | 'machines.uvdtf' | 'machines.cutting'
  | 'machines.specs' | 'machines.compare'
  | 'inks' | 'inks.uv' | 'inks.uvled' | 'inks.uvdtf' | 'inks.ecoSolvent' | 'inks.solvent'
  | 'inks.sublimation' | 'inks.dtf' | 'inks.textile'
  | 'inks.printheads' | 'inks.spares' | 'inks.auxiliaries'
  | 'compatibility'
  | 'applications' | 'applications.signage' | 'applications.packaging'
  | 'applications.interior' | 'applications.industrial' | 'applications.textile'
  | 'applications.vehicle'
  | 'service' | 'service.request' | 'service.training' | 'service.warranty'
  | 'documents'
  | 'about' | 'about.references' | 'about.events'
  | 'finance' | 'used' | 'insights'
  | 'contact' | 'quote' | 'samples' | 'thanks'
  | 'privacy' | 'cookies' | 'terms';

export const ROUTES = {
  home: { tr: '', en: '' },

  machines: { tr: 'makineler', en: 'machines' },
  'machines.uvFlatbed': { tr: 'uv-flatbed-baski-makineleri', en: 'uv-flatbed-printers' },
  'machines.uvHybrid': { tr: 'uv-hibrit-baski-makineleri', en: 'uv-hybrid-printers' },
  'machines.ecoSolvent': { tr: 'eko-solvent-baski-makineleri', en: 'eco-solvent-printers' },
  'machines.dtf': { tr: 'dtf-baski-sistemleri', en: 'dtf-printing-systems' },
  'machines.sublimation': { tr: 'sublimasyon-baski-sistemleri', en: 'dye-sublimation-systems' },
  'machines.uvdtf': { tr: 'uv-dtf-kristal-etiket-makineleri', en: 'uv-dtf-crystal-label-printers' },
  'machines.cutting': { tr: 'kesim-makineleri', en: 'cutting-systems' },
  'machines.specs': { tr: 'teknik-ozellikler', en: 'specifications' },
  'machines.compare': { tr: 'karsilastir', en: 'compare' },

  inks: { tr: 'murekkep-sarf', en: 'inks-supplies' },
  'inks.uv': { tr: 'uv-murekkep', en: 'uv-inks' },
  'inks.uvled': { tr: 'uv-led-murekkep', en: 'uv-led-inks' },
  'inks.uvdtf': { tr: 'uv-dtf-murekkep', en: 'uv-dtf-inks' },
  'inks.ecoSolvent': { tr: 'eko-solvent-murekkep', en: 'eco-solvent-inks' },
  'inks.solvent': { tr: 'solvent-murekkep', en: 'solvent-inks' },
  'inks.sublimation': { tr: 'sublimasyon-murekkebi', en: 'dye-sublimation-inks' },
  'inks.dtf': { tr: 'dtf-pigment-murekkep', en: 'dtf-pigment-inks' },
  'inks.textile': { tr: 'tekstil-pigment-murekkebi', en: 'textile-pigment-inks' },
  'inks.printheads': { tr: 'baski-kafalari', en: 'printheads' },
  'inks.spares': { tr: 'yedek-parca', en: 'spare-parts' },
  'inks.auxiliaries': { tr: 'yardimci-malzemeler', en: 'auxiliaries' },

  compatibility: { tr: 'uyumluluk', en: 'compatibility' },

  applications: { tr: 'uygulamalar', en: 'applications' },
  'applications.signage': { tr: 'reklam-tabela', en: 'signage-advertising' },
  'applications.packaging': { tr: 'ambalaj-etiket', en: 'packaging-labels' },
  'applications.interior': { tr: 'mobilya-dekorasyon', en: 'furniture-interior' },
  'applications.industrial': { tr: 'cam-metal-endustriyel', en: 'glass-metal-industrial' },
  'applications.textile': { tr: 'tekstil-promosyon', en: 'textile-promotional' },
  'applications.vehicle': { tr: 'arac-giydirme', en: 'vehicle-wrapping' },

  service: { tr: 'teknik-servis', en: 'service' },
  'service.request': { tr: 'servis-talebi', en: 'service-request' },
  'service.training': { tr: 'kurulum-ve-egitim', en: 'installation-training' },
  'service.warranty': { tr: 'garanti-kosullari', en: 'warranty' },

  documents: { tr: 'belgeler', en: 'documents' },

  about: { tr: 'kurumsal', en: 'company' },
  'about.references': { tr: 'referanslar', en: 'references' },
  'about.events': { tr: 'fuarlar-ve-showroom', en: 'trade-fairs-showroom' },

  finance: { tr: 'finansman', en: 'financing' },
  used: { tr: 'ikinci-el', en: 'used-machines' },
  insights: { tr: 'bilgi', en: 'insights' },

  contact: { tr: 'iletisim', en: 'contact' },
  quote: { tr: 'teklif-al', en: 'request-a-quote' },
  samples: { tr: 'numune-talebi', en: 'request-samples' },
  thanks: { tr: 'tesekkurler', en: 'thank-you' },

  privacy: { tr: 'kvkk-aydinlatma-metni', en: 'privacy-notice' },
  cookies: { tr: 'cerez-politikasi', en: 'cookie-policy' },
  terms: { tr: 'kullanim-kosullari', en: 'terms-of-use' },
} satisfies Record<RouteKey, Record<Locale, string>>;

/** Machine family key -> the route key of its category page. */
export const FAMILY_ROUTE = {
  'uv-flatbed': 'machines.uvFlatbed',
  'uv-hybrid': 'machines.uvHybrid',
  'eco-solvent': 'machines.ecoSolvent',
  dtf: 'machines.dtf',
  sublimation: 'machines.sublimation',
  'uv-dtf': 'machines.uvdtf',
  cutting: 'machines.cutting',
} as const satisfies Record<string, RouteKey>;

/** Ink family key -> the route key of its category page. */
export const INK_FAMILY_ROUTE = {
  uv: 'inks.uv',
  'uv-led': 'inks.uvled',
  'uv-dtf': 'inks.uvdtf',
  'eco-solvent': 'inks.ecoSolvent',
  solvent: 'inks.solvent',
  sublimation: 'inks.sublimation',
  dtf: 'inks.dtf',
  'textile-pigment': 'inks.textile',
  auxiliary: 'inks.auxiliaries',
} as const satisfies Record<string, RouteKey>;

/** The locale prefix for a path: '' for Turkish, '/en' for English. */
export function localePrefix(locale: Locale): string {
  return locale === DEFAULT_LOCALE ? '' : `/${locale}`;
}

/**
 * Build an absolute-from-root path for a route.
 *
 * `path('machines.uvFlatbed', 'tr')`            -> /makineler/uv-flatbed-baski-makineleri/
 * `path('machines.uvFlatbed', 'en')`            -> /en/machines/uv-flatbed-printers/
 * `path('machines', 'tr', ['uv-flatbed…','mf'])`-> /makineler/uv-flatbed…/mf/
 *
 * Parent segments are inferred from the dotted key, so a nested route can never
 * drift out of sync with its parent's slug.
 */
export function path(key: RouteKey, locale: Locale, extra: string[] = []): string {
  const parts = key.split('.');
  const segments: string[] = [];

  for (let i = 0; i < parts.length; i++) {
    const stepKey = parts.slice(0, i + 1).join('.') as RouteKey;
    const seg = ROUTES[stepKey]?.[locale];
    if (seg) segments.push(seg);
  }
  segments.push(...extra.filter(Boolean));

  const joined = segments.join('/');
  return `${localePrefix(locale)}/${joined}${joined ? '/' : ''}`.replace(/\/{2,}/g, '/');
}

/** Same as `path`, absolute against the site origin — for canonicals and JSON-LD. */
export function url(key: RouteKey, locale: Locale, extra: string[] = [], origin = ''): string {
  return `${origin}${path(key, locale, extra)}`;
}

/**
 * The hreflang set for one logical page. Every page renders this; nothing is
 * hard-coded, so adding a locale needs no template edits.
 */
export function alternates(
  key: RouteKey,
  extra: Partial<Record<Locale, string[]>> = {},
): Array<{ locale: Locale; href: string; xDefault: boolean }> {
  return LOCALES.map((locale) => ({
    locale,
    href: path(key, locale, extra[locale] ?? []),
    xDefault: locale === DEFAULT_LOCALE,
  }));
}

/** Translate the *current* path into the other locale, for the language switch. */
export function switchLocale(
  key: RouteKey,
  target: Locale,
  extra: Partial<Record<Locale, string[]>> = {},
): string {
  return path(key, target, extra[target] ?? []);
}

/** `getStaticPaths` helper: the non-default locales only. */
export const NON_DEFAULT_LOCALES = LOCALES.filter((l) => l !== DEFAULT_LOCALE);
