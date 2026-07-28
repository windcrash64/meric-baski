/**
 * Product URL and label resolution.
 *
 * Both the TR and EN routes derive a machine's URL from the same two facts —
 * its family and its file id — so a category slug can only ever be written down
 * once, in i18n/routes.ts.
 */

import type { CollectionEntry } from 'astro:content';

import type { Locale } from '../config/site';
import { FAMILY_ROUTE, INK_FAMILY_ROUTE, path, ROUTES, type RouteKey } from '../i18n/routes';

type MachineEntry = CollectionEntry<'machines'>;
type InkEntry = CollectionEntry<'inks'>;

export const MACHINE_FAMILY_NAMES: Record<string, Record<Locale, string>> = {
  'uv-flatbed': { tr: 'UV Flatbed Baskı Makineleri', en: 'UV Flatbed Printers' },
  'uv-hybrid': { tr: 'UV Hibrit Baskı Makineleri', en: 'UV Hybrid Printers' },
  'eco-solvent': { tr: 'Eko Solvent Baskı Makineleri', en: 'Eco-Solvent Printers' },
  dtf: { tr: 'DTF Baskı Sistemleri', en: 'DTF Printing Systems' },
  sublimation: { tr: 'Süblimasyon Baskı Sistemleri', en: 'Dye-Sublimation Systems' },
  'uv-dtf': { tr: 'UV DTF / Kristal Etiket Makineleri', en: 'UV DTF / Crystal Label Printers' },
  cutting: { tr: 'Kesim Makineleri ve Plotterlar', en: 'Cutting Systems & Plotters' },
};

export const INK_FAMILY_NAMES: Record<string, Record<Locale, string>> = {
  uv: { tr: 'UV Mürekkep', en: 'UV Curable Inks' },
  'uv-led': { tr: 'UV LED Mürekkep', en: 'UV-LED Inks' },
  'uv-dtf': { tr: 'UV DTF Mürekkep', en: 'UV DTF Inks' },
  'eco-solvent': { tr: 'Eko Solvent Mürekkep', en: 'Eco-Solvent Inks' },
  solvent: { tr: 'Solvent Mürekkep', en: 'Solvent Inks' },
  sublimation: { tr: 'Süblimasyon Mürekkebi', en: 'Dye-Sublimation Inks' },
  dtf: { tr: 'DTF Pigment Mürekkep', en: 'DTF Pigment Inks' },
  'textile-pigment': { tr: 'Tekstil Pigment Mürekkebi', en: 'Textile Pigment Inks' },
  auxiliary: { tr: 'Yardımcı Malzemeler', en: 'Auxiliaries' },
};

function segment(key: RouteKey, locale: Locale): string {
  return ROUTES[key][locale];
}

export function machineFamilyRoute(family: string): RouteKey {
  return FAMILY_ROUTE[family as keyof typeof FAMILY_ROUTE];
}

export function inkFamilyRoute(family: string): RouteKey {
  return INK_FAMILY_ROUTE[family as keyof typeof INK_FAMILY_ROUTE];
}

export function machineHref(machine: MachineEntry, locale: Locale): string {
  return path('machines', locale, [
    segment(machineFamilyRoute(machine.data.family), locale),
    machine.id,
  ]);
}

export function inkHref(ink: InkEntry, locale: Locale): string {
  return path('inks', locale, [segment(inkFamilyRoute(ink.data.family), locale), ink.id]);
}

/** The per-locale extra segments a dynamic page hands to Base for hreflang. */
export function machineRouteExtra(machine: MachineEntry): Record<Locale, string[]> {
  const family = machineFamilyRoute(machine.data.family);
  return {
    tr: [segment(family, 'tr'), machine.id],
    en: [segment(family, 'en'), machine.id],
  };
}

export function inkRouteExtra(ink: InkEntry): Record<Locale, string[]> {
  const family = inkFamilyRoute(ink.data.family);
  return {
    tr: [segment(family, 'tr'), ink.id],
    en: [segment(family, 'en'), ink.id],
  };
}

export function machineFamilyName(family: string, locale: Locale): string {
  return MACHINE_FAMILY_NAMES[family]?.[locale] ?? family;
}

export function inkFamilyName(family: string, locale: Locale): string {
  return INK_FAMILY_NAMES[family]?.[locale] ?? family;
}
