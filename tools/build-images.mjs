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

/**
 * What a transparent source is flattened onto for the JPEG rung.
 *
 * JPEG has no alpha and sharp's default matte is black, so the cutouts — which
 * ARE transparent — came out as black rectangles: mean luminance 194 → 39, with
 * 71% of the pixels below L 32. Only a browser with neither AVIF nor WebP ever
 * sees that file, but "renders as a black box" is not an acceptable fallback.
 *
 * One colour, not two. Cards sit on bone and the product page on white; bone
 * splits the difference at ΔL* ≈ 4.6 against white, which is far less visible
 * than doubling the JPEG count for a path almost nobody takes.
 */
const JPEG_MATTE = '#f2f1ed'; // --bone

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
 * A shared crop across all four was tried and reverted: it made the machine
 * noticeably bigger but cost the composition the air around it, and the calmer
 * framing reads better. The cutouts keep the canvas Blender composed them on.
 */
async function normalise(file, role) {
  let img = sharp(file);
  if (role === 'machine') {
    img = sharp(await img.trim({ threshold: 12 }).toBuffer());
  } else if (role === 'stage') {
    img = sharp(await fadeFloor(await img.toBuffer()));
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

async function build(file, { role = 'machine', dest }) {
  const widths = LADDERS[role] ?? LADDERS.machine;
  const base = dest ?? path.basename(file).replace(/\.[^.]+$/, '');
  const dir = path.join(OUT, path.dirname(dest ?? ''));
  await mkdir(dir, { recursive: true });

  const src = await normalise(file, role);
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
      // Flatten on the format clone, never on `resized` — the same pipeline
      // feeds AVIF and WebP, and flattening upstream would strip their alpha too.
      const encoder = fmt === 'jpeg' && meta.hasAlpha
        ? resized.clone().flatten({ background: JPEG_MATTE })
        : resized.clone();
      const info = await encoder[fmt](opts).toFile(out);
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
