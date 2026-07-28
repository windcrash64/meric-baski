/**
 * Image resolution against the generated ladder.
 *
 * Content files name images that may not have been produced yet (photography is
 * sourced separately from the data layer). Rather than render a broken frame,
 * templates ask here what actually exists and fall back to the machine's own
 * Blender render — which is always available, because we make it ourselves.
 */

import manifest from '../../public/img/manifest.json';

const KNOWN = new Set(Object.keys(manifest as Record<string, unknown>));

/**
 * Blender renders, mapped ONLY to the machine each one actually is.
 *
 * It is tempting to fall back to a family-mate's render so every card has a
 * picture. Do not: a 600 x 900 mm desktop unit illustrated by a 2.5 m
 * industrial flatbed is a false claim about the product, and this is a
 * catalogue whose whole positioning is that its numbers can be trusted. A
 * machine without its own model shows a labelled placeholder until one exists.
 */
const RENDER_KEYS: Record<string, string> = {
  'MF-2513-R8': 'flatbed-uv',
  'MH-3200-R12': 'roll-uv',
  'MS-1802-E4': 'eco-solvent',
  'MD-600-A4': 'dtf',
};

export function exists(src: string): boolean {
  return KNOWN.has(src.replace(/^\/img\//, '').replace(/\.[a-z]+$/i, ''));
}

/** Normalise a content-file path ("/img/x/y.jpg") to a manifest key ("x/y"). */
export function toKey(src: string): string {
  return src.replace(/^\/img\//, '').replace(/\.[a-z]+$/i, '');
}

/**
 * The render for a machine, on a transparent ground (`cutout`) or on the studio
 * sweep. Returns null when that machine has no model yet.
 */
export function renderFor(sku: string, cutout = true): string | null {
  const family = RENDER_KEYS[sku];
  if (!family) return null;
  const key = cutout
    ? `machines/${family}/cutout/${family}-hero`
    : `machines/${family}/${family}-hero`;
  return KNOWN.has(key) ? key : null;
}

/** Every image key that resolves, in order, with the render as a guaranteed first. */
export function galleryFor(
  sku: string,
  gallery: Array<{ src: string; alt: string; caption?: string }>,
): Array<{ src: string; alt: string; caption?: string }> {
  const out: Array<{ src: string; alt: string; caption?: string }> = [];
  // Prefer the transparent render: a product card sits on the page's own ground,
  // and a baked-in grey studio sweep reads as a photo pasted into a box.
  const hero = renderFor(sku, true) ?? renderFor(sku, false);
  if (hero) {
    const first = gallery[0];
    out.push({ src: hero, alt: first?.alt ?? sku, caption: first?.caption });
  }
  for (const item of gallery.slice(hero ? 1 : 0)) {
    const key = toKey(item.src);
    if (KNOWN.has(key)) out.push({ ...item, src: key });
  }
  return out;
}
