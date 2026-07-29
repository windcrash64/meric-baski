/**
 * Responsive audit.
 *
 * Devtools lies about two things that decided most of this build: it reports
 * the full `vh` on a phone profile when a real handset gives ~150 px of it to
 * browser chrome, and it happily shows a cached stylesheet. So this measures
 * the built output over a real headless Chromium, at real viewport sizes, and
 * prints the numbers rather than a screenshot to squint at.
 *
 *   node tools/audit-responsive.mjs [baseUrl] [path...]
 */
import { chromium } from 'playwright';

const VIEWPORTS = [
  ['iPhone SE', 375, 667],
  ['iPhone 13', 390, 844],
  ['Pixel 7', 412, 915],
  ['iPhone PM', 430, 932],
  ['phone land', 740, 360],
  ['tablet', 768, 1024],
  ['tablet land', 1024, 768],
  ['laptop', 1366, 768],
  ['desktop', 1440, 900],
  ['wide', 1920, 1080],
];

const base = (process.argv[2] ?? 'http://127.0.0.1:8157').replace(/\/$/, '');
const paths = process.argv.slice(3).length ? process.argv.slice(3) : ['/'];

const probe = () => {
  const px = (n) => Math.round(n);
  const rect = (sel) => {
    const el = document.querySelector(sel);
    return el ? el.getBoundingClientRect() : null;
  };
  const hero = rect('.hero');
  const media = rect('.hero__media');
  const meter = rect('.hero__meter');
  const navs = [...document.querySelectorAll('[data-rail-nav]')];
  return {
    heroH: hero ? px(hero.height) : null,
    heroBottom: hero ? px(hero.bottom) : null,
    contentBottom: meter ? px(meter.bottom) : null,
    stage: media ? `${px(media.width)}×${px(media.height)}` : '—',
    avail: px(innerHeight),
    overflow: document.documentElement.scrollWidth - innerWidth,
    pageH: px(document.documentElement.scrollHeight),
    railNav: navs.map((n) => (n.hidden ? '·' : '↔')).join('') || '—',
    // Anything wider than the viewport is a horizontal-scroll bug; name it.
    // Ignore anything living inside a scroller or a clip — a card sitting 1900 px
    // along a mobile rail is the rail working, not the page overflowing.
    widest: (() => {
      const contained = (el) => {
        for (let p = el.parentElement; p && p !== document.body; p = p.parentElement) {
          const o = getComputedStyle(p);
          if (/(auto|scroll|hidden|clip)/.test(o.overflowX)) return true;
        }
        return false;
      };
      let worst = null;
      for (const el of document.querySelectorAll('body *')) {
        const r = el.getBoundingClientRect();
        if (r.width === 0) continue;
        const over = Math.round(r.right - innerWidth);
        if (over > 1 && !contained(el) && (!worst || over > worst.over)) {
          const cls = typeof el.className === 'string' && el.className.trim()
            ? '.' + el.className.trim().split(/\s+/)[0] : '';
          worst = { over, sel: el.tagName.toLowerCase() + cls };
        }
      }
      return worst ? `${worst.sel} +${worst.over}` : '';
    })(),
  };
};

const browser = await chromium.launch();
let bad = 0;

for (const p of paths) {
  console.log(`\n${base}${p}`);
  console.log(
    'viewport'.padEnd(18), 'hero'.padStart(5), 'fits'.padStart(5),
    'stage'.padStart(9), 'ovf'.padStart(4), 'rails'.padStart(6), 'length'.padStart(11), ' widest overflow',
  );
  for (const [name, w, h] of VIEWPORTS) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    const page = await ctx.newPage();
    await page.goto(`${base}${p}?_=${Math.random().toString(36).slice(2)}`, { waitUntil: 'networkidle' });
    const m = await page.evaluate(probe);
    const fits = m.heroBottom == null || (m.contentBottom <= m.avail && m.heroBottom <= m.avail + 1);
    if (!fits || m.overflow > 0) bad++;
    console.log(
      `${name} ${w}×${h}`.padEnd(18),
      String(m.heroH ?? '—').padStart(5),
      (fits ? 'yes' : 'NO').padStart(5),
      m.stage.padStart(9),
      String(m.overflow).padStart(4),
      m.railNav.padStart(6),
      `${(m.pageH / m.avail).toFixed(1)} screens`.padStart(11),
      ' ' + m.widest,
    );
    await ctx.close();
  }
}

await browser.close();
console.log(bad ? `\n${bad} viewport(s) failed` : '\nall viewports clear');
process.exit(bad ? 1 : 0);
