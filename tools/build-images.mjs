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

/** A render on a light sweep is mostly background; trim it so the machine fills the frame. */
async function normalise(file, role) {
  let img = sharp(file);
  if (role === 'machine') {
    img = sharp(await img.trim({ threshold: 12 }).toBuffer());
  }
  return img;
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
      role: 'machine',
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
