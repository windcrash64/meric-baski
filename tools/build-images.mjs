/**
 * Responsive image ladder.
 *
 * Every source in assets/renders and assets/photos becomes an AVIF + WebP +
 * JPEG ladder in public/img. The reference site ships 3.3 MB of unoptimised
 * JPEG on its homepage with no srcset and no lazy loading; beating that by an
 * order of magnitude is a stated goal, and this script is how.
 *
 *   node tools/build-images.mjs [--force]
 */

import { mkdir, readdir, stat, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import sharp from 'sharp';

const ROOT = path.resolve(import.meta.dirname, '..');
const OUT = path.join(ROOT, 'public', 'img');
const FORCE = process.argv.includes('--force');

/** Widths per role. Six for a full-bleed hero, fewer for anything smaller. */
const LADDERS = {
  hero: [640, 960, 1280, 1600, 1920, 2560],
  machine: [480, 768, 1200, 1800],
  stage: [480, 768, 1200, 1800],
  card: [400, 640, 960],
  thumb: [200, 400],
};

const QUALITY = { avif: 55, webp: 74, jpeg: 78 };

async function walk(dir) {
  if (!existsSync(dir)) return [];
  const out = [];
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...(await walk(full)));
    else if (/\.(png|jpe?g|webp)$/i.test(entry.name)) out.push(full);
  }
  return out;
}

/**
 * A render on a light sweep is mostly background; trim it so the machine fills
 * the frame.
 *
 * NOT per-image for the cutouts. Blender composes every machine on one
 * 2000×1250 canvas with a common camera and floor, and trimming each to its own
 * content box throws that away: the four hero slides came back at aspect ratios
 * from 1.61 to 2.02, so the row sized itself to the tallest, the shorter ones
 * hung from its top edge, and the machine changed size on every rotation.
 *
 * But the composed canvas also carries a lot of nothing — 13% of the width to
 * the left of the widest machine, up to 28% above the tallest — and that dead
 * band is what makes the hero image read as small and low. So the cutouts get
 * ONE crop, computed from the union of all of them (see stageCrop), applied
 * identically. The shared stage survives; the emptiness does not.
 */
async function normalise(file, role, crop) {
  let img = sharp(file);
  if (role === 'machine') {
    img = sharp(await img.trim({ threshold: 12 }).toBuffer());
  } else if (role === 'stage' && crop) {
    img = sharp(await fadeFloor(await img.extract(crop).toBuffer()));
  }
  return img;
}

/**
 * Fade the studio floor out at the bottom edge — and only the floor.
 *
 * Cropping to the machine leaves the shadow-catcher's floor cut off square,
 * which paints a faint but perfectly straight line across the hero where the
 * image ends. A plain gradient mask would fix it and take the machine with it:
 * DTF's chassis reaches the last row of pixels.
 *
 * The two are separable by opacity. The machine is opaque; the floor and its
 * shadow are not. So the ramp is applied to alpha only where alpha is already
 * partial, and the machine passes through untouched.
 */
async function fadeFloor(buffer, band = 0.14, solid = 200) {
  const img = sharp(buffer).ensureAlpha();
  const { data, info } = await img.raw().toBuffer({ resolveWithObject: true });
  const { width, height, channels } = info;
  const from = Math.round(height * (1 - band));
  for (let y = from; y < height; y++) {
    const k = 1 - (y - from) / (height - from);
    for (let x = 0; x < width; x++) {
      const a = (y * width + x) * channels + 3;
      if (data[a] < solid) data[a] = Math.round(data[a] * k);
    }
  }
  return sharp(data, { raw: { width, height, channels } }).png().toBuffer();
}

/** Opaque bounding box of one RGBA image, in pixels. */
async function opaqueBox(file) {
  const { data, info } = await sharp(file).ensureAlpha().raw()
    .toBuffer({ resolveWithObject: true });
  const { width: w, height: h, channels: c } = info;
  let left = w, right = -1, top = h, bottom = -1;
  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      if (data[(y * w + x) * c + 3] <= 200) continue;
      if (x < left) left = x;
      if (x > right) right = x;
      if (y < top) top = y;
      if (y > bottom) bottom = y;
    }
  }
  return { left, right, top, bottom, w, h };
}

/**
 * The single crop shared by every cutout.
 *
 * Computed rather than hard-coded so it stays correct when a machine is
 * re-rendered or a new one lands. Padded, because the shadow and the floor
 * fade past the opaque silhouette; and the bottom edge is never cropped — on
 * DTF the machine itself reaches the last row of pixels, and that edge is what
 * the hero stands the machine on.
 */
async function stageCrop(files, pad = 0.04) {
  if (!files.length) return null;
  const boxes = await Promise.all(files.map(opaqueBox));
  const { w, h } = boxes[0];
  if (boxes.some((b) => b.w !== w || b.h !== h)) {
    console.log('[stage] cutouts differ in size; skipping the shared crop');
    return null;
  }
  const px = Math.round(w * pad);
  const py = Math.round(h * pad);
  const left = Math.max(0, Math.min(...boxes.map((b) => b.left)) - px);
  const right = Math.min(w - 1, Math.max(...boxes.map((b) => b.right)) + px);
  const top = Math.max(0, Math.min(...boxes.map((b) => b.top)) - py);
  const crop = { left, top, width: right - left + 1, height: h - top };
  console.log(
    `[stage] shared crop ${crop.width}×${crop.height} from ${w}×${h} ` +
    `(${(100 - (100 * crop.width * crop.height) / (w * h)).toFixed(0)}% of the canvas was empty)`,
  );
  return crop;
}

async function build(file, { role = 'machine', dest, crop }) {
  const widths = LADDERS[role] ?? LADDERS.machine;
  const base = dest ?? path.basename(file).replace(/\.[^.]+$/, '');
  const dir = path.join(OUT, path.dirname(dest ?? ''));
  await mkdir(dir, { recursive: true });

  const src = await normalise(file, role, crop);
  const meta = await src.metadata();
  const results = [];
  const emitted = [];

  for (const w of widths) {
    if (meta.width && w > meta.width * 1.05) continue; // never upscale
    emitted.push(w);
    const resized = src.clone().resize({ width: w, withoutEnlargement: true });
    for (const [fmt, opts] of [
      ['avif', { quality: QUALITY.avif, effort: 6 }],
      ['webp', { quality: QUALITY.webp, effort: 5 }],
      ['jpeg', { quality: QUALITY.jpeg, mozjpeg: true }],
    ]) {
      const out = path.join(OUT, `${base}-${w}.${fmt === 'jpeg' ? 'jpg' : fmt}`);
      if (!FORCE && existsSync(out)) continue;
      const info = await resized.clone()[fmt](opts).toFile(out);
      results.push({ file: path.relative(OUT, out), bytes: info.size, width: w, fmt });
    }
  }

  const dims = await sharp(await src.clone().toBuffer()).metadata();
  // Record the widths actually written, never the requested ladder: a 1100 px
  // render skips the 1200 and 1800 rungs, and a srcset advertising files that
  // do not exist is a 404 the browser only reveals at the largest breakpoint.
  return { base, intrinsic: { w: dims.width, h: dims.height }, emitted, results };
}

async function main() {
  const jobs = [];

  // Mirror the whole path under assets/renders so machines/<family>/cutout/…
  // stays distinct from machines/<family>/… — collapsing to the parent folder
  // name puts every machine's cutout in one bucket called "cutout".
  for (const file of await walk(path.join(ROOT, 'assets', 'renders'))) {
    const rel = path.relative(path.join(ROOT, 'assets', 'renders'), file).replace(/\\/g, '/');
    jobs.push({
      file,
      role: rel.includes('/cutout/') ? 'stage' : 'machine',
      dest: path.posix.join('machines', rel.replace(/\.[^.]+$/, '')),
    });
  }

  for (const file of await walk(path.join(ROOT, 'assets', 'photos'))) {
    const rel = path.relative(path.join(ROOT, 'assets', 'photos'), file).replace(/\\/g, '/');
    const stem = rel.replace(/\.[^.]+$/, '');
    jobs.push({ file, role: rel.includes('hero') ? 'hero' : 'card', dest: path.posix.join('photo', stem) });
  }

  if (!jobs.length) {
    console.log('no source images found under assets/renders or assets/photos');
    return;
  }

  // One crop for every cutout, from the union of all of them. Grouped by look:
  // the light and dark rigs frame the machine identically, but they are separate
  // sets and a union across both would only ever be looser than either.
  const looks = new Map();
  for (const job of jobs.filter((j) => j.role === 'stage')) {
    const look = job.dest.split('/cutout/')[1]?.split('/')[0] ?? 'default';
    if (!looks.has(look)) looks.set(look, []);
    looks.get(look).push(job);
  }
  for (const [look, group] of looks) {
    const crop = await stageCrop(group.map((j) => j.file));
    for (const job of group) job.crop = crop;
    if (crop) console.log(`[stage]   applied to ${group.length} ${look} cutouts`);
  }

  const manifest = {};
  let total = 0;
  for (const job of jobs) {
    const res = await build(job.file, job);
    manifest[job.dest] = { intrinsic: res.intrinsic, widths: res.emitted };
    const bytes = res.results.reduce((a, r) => a + r.bytes, 0);
    total += bytes;
    const src = (await stat(job.file)).size;
    console.log(
      `${job.dest.padEnd(42)} ${(src / 1024).toFixed(0).padStart(5)} KB source → ` +
      `${res.results.length} files, ${(bytes / 1024).toFixed(0)} KB total`,
    );
  }

  await writeFile(
    path.join(OUT, 'manifest.json'),
    JSON.stringify(manifest, null, 2) + '\n',
    'utf8',
  );
  console.log(`\n${jobs.length} sources → ${(total / 1024 / 1024).toFixed(2)} MB of derivatives`);
}

await main();
