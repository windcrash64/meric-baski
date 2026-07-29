/**
 * Social and touch-icon rasters, from the brand vectors.
 *
 * Three files were referenced by every page and none of them existed:
 * `og:image` (what a shared link renders as on WhatsApp, LinkedIn and Slack),
 * the JSON-LD publisher logo, and the iOS home-screen icon. A corporate site
 * whose link previews come up blank is a worse first impression than one with
 * no preview declared at all.
 *
 * Generated rather than drawn, from brand/*.svg, so the identity stays in one
 * place: change the vector, re-run, and the social card follows.
 *
 *   node tools/build-og.mjs
 */
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';

const ROOT = path.resolve(import.meta.dirname, '..');
const BRAND = path.join(ROOT, 'brand');
const OUT = path.join(ROOT, 'public', 'img', 'og');

const INK = '#0A0A0A';
const PAPER = '#ffffff';

/**
 * Inline a brand vector's guts, resolving `currentColor`.
 *
 * The vectors are authored to inherit the surrounding text colour, which is
 * right in the page and wrong in a standalone raster: rasterised on its own,
 * `currentColor` falls back to black, and the mark came out ink-on-ink.
 */
function place(svg, { x, y, width, colour }) {
  const vb = /viewBox="([\d.\-\s]+)"/.exec(svg)?.[1]?.trim().split(/\s+/).map(Number);
  if (!vb) throw new Error('vector has no viewBox');
  const [, , vw, vh] = vb;
  const inner = svg
    .replace(/^[\s\S]*?<svg[^>]*>/, '')
    .replace(/<\/svg>\s*$/, '')
    .replace(/<title>[\s\S]*?<\/title>/, '')
    .replaceAll('currentColor', colour);
  const scale = width / vw;
  return { markup: `<g transform="translate(${x} ${y}) scale(${scale})">${inner}</g>`, height: vh * scale };
}

/** The OG card: mark on ink, with the one line that says what the company sells. */
function card(logo) {
  const width = 440;
  const logoBlock = place(logo, { x: (1200 - width) / 2, y: 214, width, colour: PAPER });

  return Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <rect width="1200" height="630" fill="${INK}"/>
  ${logoBlock.markup}
  <text x="600" y="${214 + logoBlock.height + 78}" text-anchor="middle"
        font-family="Archivo, Helvetica, Arial, sans-serif" font-size="32" font-weight="400"
        letter-spacing="0.01em" fill="#9AA0A6">Dijital baskı makineleri, mürekkepleri ve teknik servis</text>
  <rect x="0" y="616" width="400" height="14" fill="#0081D2"/>
  <rect x="400" y="616" width="400" height="14" fill="#E30161"/>
  <rect x="800" y="616" width="400" height="14" fill="#FFE305"/>
</svg>`);
}

const png = (svg, size) =>
  sharp(svg, { density: 384 }).resize(size.w, size.h, { fit: 'contain', background: size.bg }).png();

await mkdir(OUT, { recursive: true });

const logo = await readFile(path.join(BRAND, 'maven-logo.svg'), 'utf8');
const badge = await readFile(path.join(BRAND, 'maven-badge.svg'));

// Publisher logo for JSON-LD: schema.org wants it legible on its own, so it is
// drawn on paper with the mark in ink rather than left to inherit.
const publisher = place(logo, { x: 40, y: 40, width: 520, colour: INK });
const publisherCard = Buffer.from(
  `<svg xmlns="http://www.w3.org/2000/svg" width="600" height="${Math.round(publisher.height + 80)}" ` +
  `viewBox="0 0 600 ${Math.round(publisher.height + 80)}">` +
  `<rect width="600" height="${Math.round(publisher.height + 80)}" fill="${PAPER}"/>${publisher.markup}</svg>`,
);

const jobs = [
  ['default.png', card(logo), { w: 1200, h: 630, bg: INK }],
  ['logo.png', publisherCard, { w: 600, h: Math.round(publisher.height + 80), bg: PAPER }],
  // The badge already carries the ink tile and the white mark.
  ['apple-touch-icon.png', badge, { w: 180, h: 180, bg: INK }],
];

for (const [name, svg, size] of jobs) {
  const buf = await png(svg, size).toBuffer();
  await writeFile(path.join(OUT, name), buf);
  console.log(`  ${name.padEnd(22)} ${size.w}×${size.h}  ${(buf.length / 1024).toFixed(0)} KB`);
}
