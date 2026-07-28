# Track 7 — Tech Stack Verification

**Verified:** 2026-07-28. Every version below was read from the npm registry, the vendor's own
docs, or measured locally on this machine. Nothing here is from memory.

> **Read this first.** Astro is on **v7**, not v5. Three major versions landed since the
> commonly-cited tutorials were written (v5 → v6 → v7). The content-collections API you will find
> in most blog posts (`src/content/config.ts`, no `loader`) **was deleted in v6** and will not
> boot. `<ViewTransitions />` was **deleted in v6**. `outputEncoding` in three.js **no longer
> exists**. Treat every StackOverflow answer older than 2026 as wrong.

---

## 0. Decisions (the short version)

| Question | Decision |
|---|---|
| Framework | **Astro 7.1.5** |
| Vercel adapter | **None.** Pure static needs no adapter — quoted below |
| i18n | Astro native `i18n` config, `prefixDefaultLocale: false`, **plus a hand-rolled slug map** (Astro does not translate URL segments) |
| Content | Content Layer `glob()` loader over **YAML, one file per product, locale map inside** |
| 3D viewer | **`<model-viewer>` 4.3.1**, lazy-mounted on interaction |
| Carousel | **CSS scroll-snap + ~50 lines JS.** Embla 8.6.0 only if you need loop/free-drag |
| Contact form | **Web3Forms** (250 submissions/mo free) + `mailto:` fallback |
| glTF pipeline | Blender GLB → `gltf-transform optimize` (meshopt + KTX2) → target **≤ 2.5 MB** |

---

## 1. Astro

### 1.1 Verified versions

| Package | Version | Notes |
|---|---|---|
| `astro` | **7.1.5** | 7.0.0 released **2026-06-22** |
| `@astrojs/vercel` | 11.0.4 | **not needed for this project** |
| `@astrojs/sitemap` | 3.7.3 | needed |
| `@astrojs/mdx` | 7.0.5 | only if you want MDX |
| `sharp` | 0.35.3 | image service backend |
| Node | **≥ 22.12.0** | hard engine requirement |
| Vite | 8.x (bundled) | Astro 7 ships Vite 8 / Rolldown |
| Zod | 4.x (bundled as `astro/zod`) | Zod 4, not 3 |

Source: `registry.npmjs.org/astro` (`engines`, `dependencies`), <https://astro.build/blog/astro-7/>

### 1.2 What changed in v6 and v7 — the things that will actually break you

**Astro 6 (the one that matters most for copied code):**

- **Legacy content collections removed entirely.** The `legacy.collections` escape hatch is gone.
  `src/content/config.ts` must become **`src/content.config.ts`**, and *every* collection must
  declare a `loader`. There is no implicit "folders in `src/content/` are collections" behaviour
  any more.
- **`<ViewTransitions />` removed** → use `<ClientRouter />`. The `handleForms` prop no longer exists.
- `i18n.routing.redirectToDefaultLocale` default flipped **`true` → `false`**.
- Images now **crop by default** and the default service **never upscales**.
- `getImage()` throws if called client-side.
- Node 18/20 dropped; CommonJS config files (`.cjs`, `.cts`) no longer supported.

Source: <https://docs.astro.build/en/guides/upgrade-to/v6/>

**Astro 7:**

- **Rust compiler is the only compiler.** It is *stricter about invalid HTML*: every non-void
  element needs a closing tag, and it no longer auto-corrects invalid nesting (e.g. a `<div>`
  inside a `<p>`). Sloppy markup that silently worked in v5 is now a build error. It can also
  change CSS output (colour serialisation, `url()` formatting).
- **`compressHTML` default changed `true` → `'jsx'`.** Whitespace between inline elements is now
  stripped using JSX rules. **This will visually bite you**: `<a>x</a> <a>y</a>` loses the space.
  Use an explicit `{" "}`, or set `compressHTML: true` to restore v6 behaviour. For a typography-led
  editorial design, decide this on day one — retrofitting `{" "}` across 40 pages is miserable.
- **Sätteri replaces remark/rehype as the default Markdown pipeline.** Rust-based, built on
  pulldown-cmark + oxc. `@astrojs/markdown-remark` is **no longer installed by default**. Ships
  built-in GFM, smartypants, heading IDs, directives, math, frontmatter, wikilinks. If you need a
  remark/rehype plugin, install `@astrojs/markdown-remark` and set `markdown.processor: unified()`.
  *For this site: stay on Sätteri.* We have no exotic Markdown needs.
- `cache` and `routeRules` graduated from `experimental` to **top-level config**.
- **`src/fetch.ts` is now a reserved filename** (advanced routing entrypoint). Don't create one.
- `@astrojs/db` removed from the project entirely.
- Removed from `astro:transitions`: `TRANSITION_BEFORE_PREPARATION`, `TRANSITION_AFTER_PREPARATION`,
  `TRANSITION_BEFORE_SWAP`, `TRANSITION_AFTER_SWAP`, `TRANSITION_PAGE_LOAD`,
  `isTransitionBeforePreparationEvent()`, `isTransitionBeforeSwapEvent()`, `createAnimationScope()`.
  Use the lifecycle event name strings directly.

Sources: <https://docs.astro.build/en/guides/upgrade-to/v7/>, <https://astro.build/blog/astro-7/>

Reported build-time improvement for v7: **"overall build times improved by 15–61%"**.

### 1.3 i18n routing — Turkish default (unprefixed), English at `/en/`

#### Config

```js
// astro.config.mjs
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://maven.com.tr',
  output: 'static',            // default; stated explicitly for clarity
  trailingSlash: 'always',     // pick one and never change it — see note below
  build: { format: 'directory' },
  compressHTML: true,          // opt OUT of the new v7 'jsx' whitespace stripping

  i18n: {
    defaultLocale: 'tr',
    locales: ['tr', 'en'],
    routing: {
      prefixDefaultLocale: false,   // → TR at "/", EN at "/en/"
      redirectToDefaultLocale: false,
      fallbackType: 'redirect',
    },
  },

  integrations: [sitemap({ i18n: { defaultLocale: 'tr', locales: { tr: 'tr-TR', en: 'en-US' } } })],
});
```

`i18n.routing` accepts `object | "manual"`. The object keys are exactly
`prefixDefaultLocale`, `redirectToDefaultLocale`, `fallbackType` (`"redirect" | "rewrite"`).
Top-level keys are `locales`, `defaultLocale`, `fallback`, `routing`, `domains`.

Source: <https://docs.astro.build/en/reference/configuration-reference/>,
<https://docs.astro.build/en/guides/internationalization/>

> **Set `trailingSlash` explicitly.** Default is `'ignore'`, which lets `/urunler` and `/urunler/`
> both resolve in dev but produces one canonical URL in the static build. Mismatched internal links
> then cause a 308 on Vercel and a wasted round-trip. Pick `'always'` (matches
> `build.format: 'directory'`) and make the link helper emit it.

#### The thing Astro does *not* do

**Astro's i18n gives you helpers, not routes.** It does not generate a single page for you. From the
docs: *"Astro's built-in file-based routing automatically creates URL routes based on your file
structure within `src/pages/`. When i18n routing is configured, helper functions use this file
structure information to generate, use, and verify routes."*

And critically: **`getRelativeLocaleUrl()` only prefixes the locale — it does not translate the
path.** `getRelativeLocaleUrl('en', 'urunler')` returns `/en/urunler`, not `/en/products`.

For a corporate identity site in Turkish, `/en/urunler/` is bad craft and bad SEO. So we need a
**slug map**. This is the single most important architectural decision in this section.

#### `src/i18n/routes.ts` — the slug map (the actual deliverable)

```ts
// src/i18n/routes.ts
export const LOCALES = ['tr', 'en'] as const;
export type Locale = (typeof LOCALES)[number];
export const DEFAULT_LOCALE: Locale = 'tr';

/** Route key → per-locale URL segment. Add a locale = add a column, and TS forces you to fill it. */
export const ROUTES = {
  home:       { tr: '',                en: '' },
  products:   { tr: 'urunler',         en: 'products' },
  inks:       { tr: 'sarf-malzemeler', en: 'consumables' },
  service:    { tr: 'teknik-servis',   en: 'technical-service' },
  about:      { tr: 'kurumsal',        en: 'about' },
  contact:    { tr: 'iletisim',        en: 'contact' },
} as const satisfies Record<string, Record<Locale, string>>;

export type RouteKey = keyof typeof ROUTES;

/**
 * Build a locale-aware, trailing-slashed absolute path.
 *   localizePath('products', 'tr')            -> '/urunler/'
 *   localizePath('products', 'en')            -> '/en/products/'
 *   localizePath('products', 'en', 'dtf-600') -> '/en/products/dtf-600/'
 *   localizePath('home', 'tr')                -> '/'
 */
export function localizePath(key: RouteKey, locale: Locale, ...rest: string[]): string {
  const segments = [
    locale === DEFAULT_LOCALE ? null : locale,   // TR is unprefixed
    ROUTES[key][locale] || null,
    ...rest,
  ].filter(Boolean);
  return segments.length ? `/${segments.join('/')}/` : '/';
}

/** Same page, other locale — for the language switcher. */
export function alternatesFor(key: RouteKey, ...rest: string[]) {
  return LOCALES.map((l) => ({ locale: l, href: localizePath(key, l, ...rest) }));
}
```

The `satisfies Record<string, Record<Locale, string>>` is doing real work: **add `'de'` to
`LOCALES` and TypeScript immediately errors on every route missing a German segment.** That is the
"scales to more locales" guarantee, enforced by the compiler rather than by discipline.

#### `<LocaleLink />` and the language switcher

```astro
---
// src/components/LocaleLink.astro
import { localizePath, type RouteKey, type Locale } from '../i18n/routes';

interface Props { to: RouteKey; rest?: string[]; class?: string; }
const { to, rest = [], class: className } = Astro.props;

const locale = (Astro.currentLocale ?? 'tr') as Locale;
const href = localizePath(to, locale, ...rest);
const current = Astro.url.pathname === href;
---
<a href={href} class={className} aria-current={current ? 'page' : undefined}>
  <slot />
</a>
```

```astro
---
// src/components/LangSwitch.astro
import { alternatesFor, type RouteKey, type Locale } from '../i18n/routes';
interface Props { routeKey: RouteKey; rest?: string[]; }
const { routeKey, rest = [] } = Astro.props;
const current = (Astro.currentLocale ?? 'tr') as Locale;
const LABEL: Record<Locale, string> = { tr: 'TR', en: 'EN' };
---
<nav aria-label="Dil / Language">
  {alternatesFor(routeKey, ...rest).map(({ locale, href }) => (
    <a href={href} hreflang={locale} lang={locale}
       aria-current={locale === current ? 'true' : undefined}>{LABEL[locale]}</a>
  ))}
</nav>
```

`Astro.currentLocale` is populated from the URL by Astro's i18n middleware. Also available:
`Astro.preferredLocale` and `Astro.preferredLocaleList` (from `Accept-Language`) — **both are
useless in a static build**, since there is no request at build time. Do not build a
"redirect to the user's language" feature on them without an adapter.

#### `hreflang` in `<head>`

```astro
---
// inside BaseLayout.astro
import { alternatesFor, DEFAULT_LOCALE, type RouteKey } from '../i18n/routes';
interface Props { routeKey: RouteKey; rest?: string[]; }
const { routeKey, rest = [] } = Astro.props;
const alts = alternatesFor(routeKey, ...rest);
---
{alts.map(({ locale, href }) => (
  <link rel="alternate" hreflang={locale} href={new URL(href, Astro.site)} />
))}
<link rel="alternate" hreflang="x-default"
      href={new URL(alts.find(a => a.locale === DEFAULT_LOCALE)!.href, Astro.site)} />
<link rel="canonical" href={new URL(Astro.url.pathname, Astro.site)} />
```

#### Page file layout

Two viable shapes. **Use B.**

**A — folder per locale (Astro's documented default).** `src/pages/index.astro` (TR) +
`src/pages/en/index.astro`. Simple, but every page is duplicated per locale: 6 pages × 4 locales =
24 `.astro` files that must be kept structurally in sync. Rejected — it does not scale, and it is
exactly the "graveyard of near-identical files" failure mode.

**B — one dynamic route per page, locale as a param.**

```
src/pages/
  index.astro                     → /                  (TR home)
  [locale]/index.astro            → /en/               (EN home)
  urunler/index.astro             → /urunler/
  urunler/[sku].astro             → /urunler/dtf-600/
  [locale]/products/index.astro   → /en/products/
  [locale]/products/[sku].astro   → /en/products/dtf-600/
```

`[locale]` is safe next to literal segments because in a static build **only the paths returned by
`getStaticPaths()` are emitted** — `getStaticPaths` returns `locale: 'en'` only, so `/urunler/`
can never be captured by `[locale]/`.

```astro
---
// src/pages/[locale]/products/[sku].astro
import { getCollection } from 'astro:content';
import { LOCALES, DEFAULT_LOCALE, type Locale } from '../../../i18n/routes';
import ProductPage from '../../../layouts/ProductPage.astro';

export async function getStaticPaths() {
  const products = await getCollection('products');
  return LOCALES
    .filter((l) => l !== DEFAULT_LOCALE)          // TR is served by the unprefixed route
    .flatMap((locale) =>
      products.map((product) => ({
        params: { locale, sku: product.data.sku },
        props: { product, locale },
      })),
    );
}

const { product, locale } = Astro.props;
---
<ProductPage product={product} locale={locale as Locale} />
```

The TR twin (`src/pages/urunler/[sku].astro`) is a three-line file that hardcodes
`locale = 'tr'` and renders the same `<ProductPage />`. All real markup lives in the layout, so
there is exactly one copy of the page structure.

### 1.4 Content collections — the current API

`src/content/config.ts` is dead. The file is **`src/content.config.ts`** (project root `src/`), and
every collection needs a `loader`.

```ts
// src/content.config.ts
import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const LOCALE = z.enum(['tr', 'en']);

/** Prose that differs per locale. */
const localized = z.object({
  name: z.string(),
  tagline: z.string(),
  summary: z.string(),
  features: z.array(z.string()).min(3),
  applications: z.array(z.string()),
});

const products = defineCollection({
  loader: glob({ base: './src/content/products', pattern: '**/*.yaml' }),
  schema: ({ image }) =>
    z.object({
      sku: z.string(),
      family: z.enum(['dtf', 'uv', 'eco-solvent', 'sublimation', 'textile']),
      order: z.number().default(100),
      featured: z.boolean().default(false),

      // Locale-neutral, never translated:
      specs: z.object({
        printWidth: z.number(),            // mm
        printHeads: z.string(),            // "2 × Epson i3200-A1"
        resolution: z.string(),            // "1200 × 1200 dpi"
        maxSpeed: z.number(),              // m²/h
        inkType: z.enum(['dtf-pigment', 'uv', 'eco-solvent', 'sublimation']),
        inkChannels: z.string(),           // "CMYK + W"
        power: z.string(),                 // "220 V / 50 Hz / 3.5 kW"
        dimensions: z.object({ w: z.number(), d: z.number(), h: z.number() }), // mm
        weight: z.number(),                // kg
      }),

      gallery: z.array(z.object({ src: image(), alt: z.record(LOCALE, z.string()) })).min(1),
      model3d: z.string().optional(),      // "/models/dtf-600.glb"

      // One block per locale. Missing a locale = build error (see below).
      i18n: z.record(LOCALE, localized),
    }),
});

export const collections = { products };
```

**Verified locally against `zod@4.4.3`** (the version Astro 7 resolves): `z.record(z.enum([...]), v)`
**requires every enum key to be present**. Parsing `{ tr: … }` against
`z.record(z.enum(['tr','en']), …)` fails with `invalid_type` at path `["en"]`.

> This is the whole multilingual safety net in one line. **Add `'de'` to the `LOCALE` enum and
> `astro build` fails until every product has German copy.** No missing-translation can ever reach
> production. Verified by direct execution, not from docs.

Loaders: `glob({ base, pattern, generateId?, retainBody? })` and `file(path)` (many entries in one
JSON/YAML file). Both from `astro/loaders`.

Reading it:

```ts
import { getCollection, getEntry, render } from 'astro:content';

const all = await getCollection('products');
const dtf = await getCollection('products', ({ data }) => data.family === 'dtf');
const one = await getEntry('products', 'dtf-600');
const { Content } = await render(mdEntry);   // Markdown/MDX entries only
```

Note `entry.id` (not `entry.slug` — that was the legacy API). With the `glob` loader, `id` is the
file path relative to `base`, minus extension.

`image()` in the schema is injected via `schema: ({ image }) => …` and yields a real
`ImageMetadata` that `<Image />` accepts — so gallery images get optimised and dimension-checked
at build. Use it; do not put raw `/public/` strings in the YAML.

Sources: <https://docs.astro.build/en/guides/content-collections/>,
<https://docs.astro.build/en/reference/content-loader-reference/>

**Why YAML and not one Markdown file per locale:** a machine catalogue is 80 % structured data
(spec tables) and 20 % short prose. Markdown-per-locale (`products/tr/dtf-600.md` +
`products/en/dtf-600.md`) means the *numbers* are duplicated across locales and will silently
drift the first time someone corrects a print width in one file only. The YAML shape keeps one
source of truth for specs and forces prose completeness via the enum-keyed record.

### 1.5 Static output + Vercel — no adapter

Straight from the adapter's own docs:

> *"If you're using Astro as a static site builder, you only need this adapter if you are using
> additional Vercel services (e.g. Vercel Web Analytics, Vercel Image Optimization). Otherwise, you
> do not need an adapter to deploy your static site."*

And from the deploy guide:

> *"Your Astro project is a static site by default. You don't need any extra configuration to
> deploy a static Astro site to Vercel."*

Sources: <https://docs.astro.build/en/guides/integrations-guide/vercel/>,
<https://docs.astro.build/en/guides/deploy/vercel/>

**Decision: ship no adapter.** `output: 'static'` (the default), Vercel auto-detects Astro, build
command `astro build`, output directory `dist/`. Zero serverless functions, zero cold starts, zero
runtime cost, and the whole thing is a folder of HTML that can be handed to anyone.

Do **not** add `@astrojs/vercel` for Vercel Image Optimization. Astro's build-time Sharp pipeline
already emits hashed, immutable, pre-optimised AVIF/WebP into `dist/_astro/`. Adding Vercel's image
service converts a free static asset into a metered per-image transformation and makes local builds
diverge from production.

Optional `vercel.json` — only worth adding for the static-asset cache header:

```json
{
  "headers": [
    {
      "source": "/_astro/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    }
  ],
  "cleanUrls": false,
  "trailingSlash": true
}
```

`trailingSlash: true` here must agree with `trailingSlash: 'always'` in `astro.config.mjs`.

### 1.6 Images

```astro
---
import { Image, Picture } from 'astro:assets';
import hero from '../assets/hero-dtf.jpg';   // 2400×1350
---

<!-- LCP hero: `priority` sets loading=eager + fetchpriority=high + decoding=sync -->
<Image src={hero} alt="Maven DTF-600" priority layout="full-width" />

<!-- Product card -->
<Image src={product.data.gallery[0].src} alt={alt} width={640} height={480}
       layout="constrained" quality={72} />

<!-- Art-directed / format-controlled -->
<Picture src={hero} formats={['avif', 'webp']} alt="…"
         widths={[480, 768, 1200, hero.width]}
         sizes="(max-width: 768px) 100vw, 1200px" />
```

Config:

```js
image: {
  layout: 'constrained',    // project-wide default: 'constrained' | 'fixed' | 'full-width'
  responsiveStyles: true,   // REQUIRED for layout to actually work — default is false
  objectFit: 'cover',       // default
  objectPosition: 'center', // default
}
```

**`responsiveStyles` defaults to `false`.** Set `layout` without it and the `srcset` is emitted but
the images do not lay out responsively. This is the #1 gotcha in the current image API.

With `layout: 'constrained'` Astro auto-generates `srcset` at 640/750/800/828/1080/1280/1600w plus
`sizes="(min-width: 800px) 800px, 100vw"` and `style="--fit: cover; --pos: center;"` with a
`data-astro-image="constrained"` hook. If you pass `widths` manually you **must** also pass `sizes`.

Behavioural notes (changed in v6): images **crop by default**, the default service **never
upscales**, and `getImage()` is **server-only** (throws client-side).

Source: <https://docs.astro.build/en/guides/images/>,
<https://docs.astro.build/en/reference/modules/astro-assets/>

### 1.7 View Transitions / ClientRouter

**Current name: `<ClientRouter />`. Stable.** `<ViewTransitions />` was removed in v6.

```astro
---
import { ClientRouter } from 'astro:transitions';
---
<head>
  <ClientRouter />
</head>
```

Directives: `transition:name="…"`, `transition:animate="fade | slide | none | initial"`,
`transition:persist`, `transition:persist-props`.

Lifecycle events on `document`, in order:
`astro:before-preparation` → `astro:after-preparation` → `astro:before-swap` →
`astro:after-swap` → `astro:page-load`.

Programmatic nav: `import { navigate } from 'astro:transitions/client'`.
Per-link opt-out: `data-astro-reload`; history control: `data-astro-history="replace"`.

**Critical for this project:** any DOM-touching script (carousel init, 3D viewer mount, sliding
underline) must re-run after each client-side navigation. Bind to `astro:page-load`, **not**
`DOMContentLoaded` — the latter fires exactly once and your carousels die on the second page.

```js
document.addEventListener('astro:page-load', () => {
  document.querySelectorAll('[data-gallery]:not([data-ready])').forEach(initGallery);
});
```

Removed in v7 (do not use): `TRANSITION_BEFORE_PREPARATION`, `TRANSITION_AFTER_PREPARATION`,
`TRANSITION_BEFORE_SWAP`, `TRANSITION_AFTER_SWAP`, `TRANSITION_PAGE_LOAD`,
`isTransitionBeforePreparationEvent()`, `isTransitionBeforeSwapEvent()`, `createAnimationScope()`.

**Recommendation:** ship `<ClientRouter />`. It is the cheapest way to get the "editorial, considered"
feel (persistent header, cross-page image morphs on product cards) and it is now boring, stable
technology. Wrap the whole thing in `@media (prefers-reduced-motion: reduce) { … }` guards.

Source: <https://docs.astro.build/en/guides/view-transitions/>

---

## 2. Astro vs hand-written HTML vs Vite+vanilla vs Next static export

Scored against *this* brief: static, TR+EN scaling to more, ~25–40 pages, product catalogue,
eventual handover to a non-technical client.

| | Hand-written HTML/CSS/JS | Vite + vanilla | **Astro 7** | Next 16 static export |
|---|---|---|---|---|
| Pages × locales | 40 files → **80+**, hand-synced | same problem; Vite doesn't route | generated from data | generated from data |
| Templating / partials | none (copy-paste header ×80) | none without a plugin | native components + layouts | React components |
| i18n | manual everything | manual everything | built-in config + helpers | `next-intl` etc., extra dep |
| Product catalogue | hand-write 20 detail pages | same | `getStaticPaths` from typed YAML | `generateStaticParams` |
| Content validation | none | none | **Zod schema, build fails on bad data** | manual |
| Image optimisation | manual (Squoosh by hand) | plugin, manual wiring | built-in Sharp + `srcset` | built-in, but **`next/image` is crippled in `output: 'export'`** — needs `unoptimized: true` or a loader |
| JS shipped by default | 0 KB | 0 KB | **0 KB** | React runtime (~90 KB+ br) even for static pages |
| Vercel static | trivial | trivial | trivial, no adapter | works, with export caveats |
| Handover to client | edit raw HTML — high risk | same | **edit YAML/Markdown** — low risk | edit MDX, but repo is heavier |
| Current repo fit | this is what exists today | — | clean migration | over-engineered |

**Recommendation: Astro 7.**

The decisive factor is not developer comfort, it is the **content model**. This site is a product
catalogue: ~10–20 machines × 2 locales × (spec table + gallery + 3D + prose). Hand-written HTML
means the spec table markup exists 40 times, and the first time a print-width number changes you
have to find every copy. Astro turns that into one YAML file per machine and one template, with a
Zod schema that refuses to build if a translation or a spec is missing.

**Against plain HTML specifically:** the current repo (5 hand-written `.html` files) already shows
the failure mode — `urunler.html` is 20 KB of markup that will need a Turkish and an English twin
per product. That is the thing to escape from.

**Against Next static export:** Next ships a React runtime to render pages that contain no
interactivity, `next/image` degrades under `output: 'export'`, and the resulting repo is
substantially more machinery for a brochure site. The only reason to pick Next would be a future
need for server rendering, which a static corporate site does not have. Astro can add an adapter
later if that ever changes.

**Against Vite + vanilla:** Vite is a bundler, not a site generator. You would end up hand-rolling
routing, layouts, i18n and a content pipeline — i.e. rebuilding a worse Astro.

**Handover caveat, stated honestly:** Astro is not a CMS. A non-technical client editing YAML in a
Git repo will make mistakes. Two mitigations, in order of cost: (1) the Zod schema catches most of
them at build time and Vercel refuses to deploy a broken build — this is genuinely strong; (2) if
the client needs real self-service later, point a Git-based CMS (Decap/Sveltia, both free, both
static) at `src/content/products/` — it reads the same YAML with no architectural change. Do not
build that now; do keep the content directory shaped so it stays possible.

---

## 3. 3D viewer — `<model-viewer>` vs raw three.js

### 3.1 Verified versions

| | Version | Released |
|---|---|---|
| `three` | **0.185.1** | 2026-07-01 |
| `@google/model-viewer` | **4.3.1** | ~2026-05 |

> **Version-pinning trap.** `@google/model-viewer@4.3.1` declares `peerDependencies: { three: "^0.183.0" }`,
> and the project explicitly *"strongly recommend[s] you keep your three.js version locked to
> model-viewer's"* because of frequent upstream breaking changes. So `three@0.185.1` and
> model-viewer **cannot share a copy**. Pick one; do not install both and expect deduplication.

### 3.2 Bundle sizes — measured, not estimated

Transfer sizes measured against jsDelivr with `Accept-Encoding: br`:

| Artifact | minified | brotli |
|---|---|---|
| `model-viewer.min.js` (standalone, three bundled in) | 1044 KB | **282 KB** |
| `model-viewer-module.min.js` (three external) | 463 KB | 138 KB |
| `three.module.min.js` (core only, needs `three.core.min.js` too) | 357 KB | 85 KB |

Tree-shaken app bundles, **built locally with esbuild 0.28 (`--bundle --minify --format=esm`) against
`three@0.185.1`**, brotli via `zlib.brotliCompressSync`:

| Entry | minified | gzip | brotli |
|---|---|---|---|
| `import * as THREE from 'three'` (everything) | 713 KB | 184 KB | 150 KB |
| GLTFLoader + OrbitControls + RoomEnvironment | 612 KB | 155 KB | **128 KB** |
| … + DRACOLoader | 619 KB | 158 KB | 130 KB |
| … + KTX2Loader + MeshoptDecoder | 697 KB | 186 KB | 154 KB |

**Finding: tree-shaking three.js barely helps.** A realistic glTF viewer is 128 KB brotli versus
150 KB for the entire library — a 15 % saving, not the 70 % that "just tree-shake it" advice
implies. `GLTFLoader` transitively touches most of the material, texture, animation and geometry
code. Anyone budgeting "~40 KB for three.js" is wrong by 3×.

So the honest comparison is **~128 KB br (three.js, hand-rolled) vs ~282 KB br (model-viewer)** —
model-viewer costs about **+154 KB brotli**, and roughly 400 lines of code you don't write.

### 3.3 What each gives you

**`<model-viewer>` 4.3.1** — orbit/pan/zoom, inertia, auto-rotate, poster image + `loading="lazy"`
+ `reveal="interaction"`, IBL/skybox with `environment-image` & `exposure`, contact shadows,
**AR out of the box** (WebXR on Android, USDZ/Quick Look on iOS), keyboard-accessible orbit,
ARIA labelling, automatic Draco/meshopt/KTX2 decoding, hotspot annotations. `<script type="module">`
tag, no build step required.

```html
<model-viewer
  src="/models/dtf-600.glb"
  poster="/models/dtf-600-poster.webp"
  alt="Maven DTF-600 dijital baskı makinesi"
  camera-controls
  touch-action="pan-y"
  loading="lazy"
  reveal="interaction"
  environment-image="neutral"
  exposure="1.0"
  shadow-intensity="1"
  camera-orbit="35deg 75deg auto"
  min-camera-orbit="auto 0deg auto"
  max-camera-orbit="auto 100deg auto"
  ar ar-modes="webxr scene-viewer quick-look"
  style="width:100%;aspect-ratio:4/3;--poster-color:transparent">
</model-viewer>
<script type="module"
  src="https://unpkg.com/@google/model-viewer@4.3.1/dist/model-viewer.min.js"></script>
```

`touch-action="pan-y"` matters on mobile: without it the model captures vertical swipes and the
user cannot scroll past it.

**Raw three.js 0.185.1** — smaller, total control, but you write and then maintain: camera framing
from the model's bounding box, damping, resize observer, `prefers-reduced-motion`, render-on-demand
(never `setAnimationLoop` unconditionally on a marketing page — it pins a GPU at 60 fps forever),
context-loss handling, poster/loading states, focus management, and AR (which is simply not
happening by hand).

### 3.4 Current three.js API — the renamed properties, confirmed

`outputEncoding` is **gone**. I grepped the shipped `three@0.185.1` `build/three.module.js`:

```
outputEncoding      : 0 occurrences
sRGBEncoding        : 0
LinearEncoding      : 0
useLegacyLights     : 0
physicallyCorrectLights : 0
--
outputColorSpace    : 18
SRGBColorSpace      : 7
LinearSRGBColorSpace: 5
ColorManagement     : 22
ACESFilmicToneMapping / AgXToneMapping / NeutralToneMapping : present
```

Current, correct PBR setup (mirrors `examples/webgl_loader_gltf_compressed.html` on `dev`):

```js
import * as THREE from 'three';
import { OrbitControls }  from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader }     from 'three/addons/loaders/GLTFLoader.js';
import { KTX2Loader }     from 'three/addons/loaders/KTX2Loader.js';
import { MeshoptDecoder } from 'three/addons/libs/meshopt_decoder.module.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));   // cap: 3× DPR phones melt
renderer.toneMapping = THREE.ACESFilmicToneMapping;      // or THREE.NeutralToneMapping
renderer.toneMappingExposure = 1;
renderer.outputColorSpace = THREE.SRGBColorSpace;        // NOT outputEncoding

const scene = new THREE.Scene();

// Studio IBL with no HDRI download — ~5 KB of code, generated on the GPU.
const pmrem = new THREE.PMREMGenerator(renderer);
const room  = new RoomEnvironment();                     // constructor takes NO renderer arg
scene.environment = pmrem.fromScene(room, 0.04).texture;
room.dispose();

const ktx2 = new KTX2Loader()
  .setTranscoderPath('/basis/')                          // copy from three/examples/jsm/libs/basis/
  .detectSupport(renderer);

const loader = new GLTFLoader();
loader.setKTX2Loader(ktx2);
loader.setMeshoptDecoder(MeshoptDecoder);
// If you chose Draco instead of meshopt:
// import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
// loader.setDRACOLoader(new DRACOLoader().setDecoderPath('/draco/'));

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.enablePan = false;
controls.minDistance = 2; controls.maxDistance = 10;
```

Import-path story: `three@0.185.1` publishes an `exports` map with `.`, `./addons`, `./addons/*`,
`./examples/jsm/*`, `./webgpu`, `./tsl`, `./src/*`. **Use `three/addons/…`** — it is the supported
alias and what the official examples use. In a plain `<script type="module">` without a bundler you
need an import map (`"three": "…/three.module.js", "three/addons/": "…/jsm/"`); inside Astro/Vite
the bare specifier just resolves.

`RoomEnvironment` vs an HDRI: `RoomEnvironment` is a procedural studio box — no network request, no
licensing question, and it flatters brushed metal and painted steel, which is exactly what a
printing machine is. **Use it.** Reach for an `.hdr`/UltraHDR only if the client supplies a branded
environment; that adds a 1–3 MB download and an extra loader.

Tone mapping: `ACESFilmicToneMapping` is the long-standing default recommendation and is what
model-viewer's `neutral` environment approximates. `NeutralToneMapping` (Khronos PBR neutral) is
newer and preserves product colours more faithfully — **worth A/B-ing for a catalogue**, since
ACES noticeably desaturates saturated brand colours, and this brand is CMYK-pixel-based.

### 3.5 Recommendation

**Use `<model-viewer>` 4.3.1, mounted lazily.**

Reasoning, given 3D is a *secondary* feature on a *marketing* site:

1. **The payload is deferred either way**, so the 282 KB vs 128 KB gap costs nothing on first paint
   or on any page the user doesn't interact with. Load the script only when the viewer scrolls into
   view. The gap only ever affects users who deliberately opened the 3D — who have already opted in.
2. **AR is a genuine sales feature here.** A distributor's customer standing in their own workshop
   can place a full-size DTF machine on the floor and check it fits. Building that by hand is
   weeks; `ar ar-modes="webxr scene-viewer quick-look"` is one attribute.
3. **Nobody has to maintain render code.** This site gets handed over. A hand-rolled three.js
   viewer is the single most likely thing to rot.
4. `poster` + `reveal="interaction"` gives a correct, designed loading state for free — which
   matters more for the "editorial, high-craft" bar than any of the rendering differences.
5. Keyboard-orbitable and ARIA-labelled out of the box; a hand-rolled OrbitControls canvas is a
   keyboard dead end unless you do the work.

Lazy mount (works with `ClientRouter` because it re-binds on `astro:page-load`):

```js
document.addEventListener('astro:page-load', () => {
  const host = document.querySelector('model-viewer[data-lazy]:not([data-armed])');
  if (!host) return;
  host.dataset.armed = '';
  new IntersectionObserver((entries, obs) => {
    if (!entries.some((e) => e.isIntersecting)) return;
    obs.disconnect();
    if (document.getElementById('mv-script')) return;
    const s = document.createElement('script');
    s.type = 'module'; s.id = 'mv-script';
    s.src = '/vendor/model-viewer-4.3.1.min.js';   // self-host; do not hotlink a CDN
    document.head.appendChild(s);
  }, { rootMargin: '200px' }).observe(host);
});
```

Self-host the file in `public/vendor/`. Hotlinking unpkg on a corporate site adds a third-party
DNS + TLS round trip, a privacy question under KVKK/GDPR, and a dependency on someone else's uptime.

**Switch to raw three.js only if** the design later demands bespoke rendering — exploded views,
animated ink-flow, custom shaders, scroll-linked camera. Then the 128 KB path and the code above
are ready.

---

## 4. glTF pipeline: Blender → web

### 4.1 Blender

**Blender 5.2 LTS is current** (released 2026-07-14, supported to July 2028). The brief said 5.1 —
5.1 shipped 2026-03-17 and is superseded. Use 5.2 LTS.

The bundled glTF 2.0 add-on (`io_scene_gltf2`) from `KhronosGroup/glTF-Blender-IO` `main` is
**version 5.3.18**, minimum Blender **5.2.1**.

Verified Draco export properties (name / default / range):

| Property | Default | Range |
|---|---|---|
| `export_draco_mesh_compression_enable` | `False` | — |
| `export_draco_mesh_compression_level` | `6` | 0–10 |
| `export_draco_position_quantization` | `14` | 0–30 |
| `export_draco_normal_quantization` | `10` | 0–30 |
| `export_draco_texcoord_quantization` | `12` | 0–30 |
| `export_draco_color_quantization` | `10` | 0–30 |
| `export_draco_generic_quantization` | `12` | 0–30 |

`export_format`: `GLB` (default, single binary file) | `GLTF_SEPARATE` | `GLTF_EMBEDDED`.
`export_image_format`: `AUTO` (default) | `JPEG` | `WEBP` | `NONE`.
`export_jpeg_quality` / `export_image_quality`: default `75`, range 0–100.

**Export from Blender with compression OFF.** Do the compression in gltf-transform, which is
strictly better at it and reproducible from a script. Blender's job is to emit a clean, correct GLB.

Blender export settings for this project:

- Format: **glTF Binary (.glb)**
- Include: **Selected Objects** (never dump the whole scene — you'll ship the lights and camera)
- Transform: **+Y Up** (on; glTF convention)
- Data ▸ Mesh: **Apply Modifiers** on, **UVs** on, **Normals** on, **Tangents** only if you have a
  normal map, **Vertex Colors** off unless used
- Material ▸ Images: **Automatic**, Quality 75
- Compression: **off**
- Animation: **off** (a static machine needs none; it doubles file size)
- Lighting/Cameras/Punctual Lights: **off** — the web viewer supplies its own IBL

Scriptable equivalent:

```python
import bpy
bpy.ops.export_scene.gltf(
    filepath="//export/dtf-600.glb",
    export_format='GLB',
    use_selection=True,
    export_apply=True,          # apply modifiers
    export_yup=True,
    export_materials='EXPORT',
    export_image_format='AUTO',
    export_image_quality=75,
    export_cameras=False,
    export_lights=False,
    export_animations=False,
    export_draco_mesh_compression_enable=False,   # gltf-transform does this
)
```

### 4.2 gltf-transform

`@gltf-transform/cli` **4.4.2**. Install: `npm install --global @gltf-transform/cli`

Verified `optimize` flags and defaults (read from `packages/cli/src/cli.ts` on `main`):

| Flag | Values | Default |
|---|---|---|
| `--compress` | `draco` \| `meshopt` \| `quantize` \| `false` | **`meshopt`** |
| `--texture-compress` | `ktx2` \| `webp` \| `avif` \| `auto` \| `false` | `auto` |
| `--texture-size` | number | `2048` |
| `--simplify` / `--simplify-error` / `--simplify-ratio` | bool / num / num | `true` / defaults |
| `--instance`, `--palette`, `--prune`, `--flatten`, `--join`, `--weld`, `--sparse`, `--resample` | bool | `true` |
| `--meshopt-level` | `medium` \| `high` | `high` |

Recommended pipeline for a marketing-site machine model:

```bash
# 1. Inspect first — always. Tells you triangle count, texture sizes, what's actually heavy.
gltf-transform inspect dtf-600.glb

# 2. One-shot optimise: meshopt geometry + KTX2 textures, textures capped at 1024.
gltf-transform optimize dtf-600.glb dtf-600.opt.glb \
  --compress meshopt \
  --texture-compress ktx2 \
  --texture-size 1024 \
  --simplify false

# 3. Verify.
gltf-transform inspect dtf-600.opt.glb
```

`--simplify false` is deliberate: automatic decimation on a machined product with crisp panel edges
and readable branding produces visible artefacts. Decimate deliberately in Blender where you can see
it, not in a build script.

Step-by-step alternative when `optimize` is too blunt:

```bash
gltf-transform prune  in.glb  s1.glb          # drop unused nodes/materials/textures
gltf-transform dedup  s1.glb  s2.glb          # merge duplicate accessors/textures
gltf-transform resize s2.glb  s3.glb --width 1024 --height 1024
gltf-transform etc1s  s3.glb  s4.glb --quality 200   # KTX2 ETC1S: small, good for colour maps
gltf-transform meshopt s4.glb out.glb --level high
```

Texture codec choice: **ETC1S** (`etc1s`, quality 1–255) for base-colour/ORM maps — smallest, and
the quality hit is invisible at marketing-site scale. **UASTC** (`uastc`, `--level 0–4`, `--zstd 0–22`)
only for normal maps, where ETC1S blocking is visible.

### 4.3 Draco vs meshopt — pick meshopt

| | Draco | meshopt (`EXT_meshopt_compression`) |
|---|---|---|
| Geometry ratio | slightly better | very close |
| Decoder | ~190 KB WASM, separate fetch | ~29 KB, inlineable |
| Decode speed | slower | **much faster** |
| GPU memory | decompresses to full-size buffers | **stays quantized on the GPU** |
| Combines with KTX2 | yes | yes |
| gltf-transform default | — | **yes** |

**Use meshopt.** For a marketing site the decoder payload and time-to-first-pixel dominate, not the
last 5 % of geometry ratio; and meshopt is what `gltf-transform optimize` defaults to. Draco's edge
only matters for very heavy meshes over slow links. model-viewer decodes both natively.

### 4.4 Target file sizes

For a single machine on a product page where 3D is secondary:

| Budget | Target | Hard ceiling |
|---|---|---|
| **GLB total** | **1.5–2.5 MB** | 4 MB |
| Triangles | 150 k–300 k | 500 k |
| Texture set | 1024², ETC1S | 2048² only for a hero model |
| Draw calls / materials | ≤ 10 | 20 |
| Poster image (WebP) | 40–80 KB | — |

Sanity check: a machine is a box with panels, a screen and rollers. If the optimised GLB exceeds
4 MB, the CAD import wasn't retopologised — fix the model, not the compression. Also `Ctrl+A`
apply transforms and delete interior geometry nobody can see before exporting.

Serving: `.glb` is already compressed — do **not** let Vercel re-gzip it (no gain, wasted CPU).
Serve from `public/models/` with a long immutable cache and a version in the filename
(`dtf-600.v2.glb`).

---

## 5. Carousel / sliding galleries

### 5.1 Options, measured

Brotli sizes measured from jsDelivr:

| Library | Version | Last publish | min | brotli | Weekly dl |
|---|---|---|---|---|---|
| **CSS scroll-snap + JS** | — | — | ~1.5 KB | **~0.7 KB** | — |
| Embla Carousel | **8.6.0** | 2025-04-04 | 17.9 KB | **7.3 KB** | 36.4 M |
| ⤷ `embla-carousel-accessibility` | 9.0.0-rc01 ⚠️ | — | 5.5 KB | 2.1 KB | — |
| Keen-slider | 6.8.6 | **2023-07-05** ⚠️ | 14.9 KB | 6.3 KB | 282 k |
| Swiper | 14.0.7 | 2026-07-28 | 151.6 KB | 44.4 KB | 4.3 M |

Notes that matter:

- **Keen-slider is effectively unmaintained** — last release three years ago. Disqualified for a
  site that must live for years.
- **Swiper is 6× Embla's weight** and its `swiper-bundle` pulls in every module. It is a fine
  library, but it is a framework for a job that is one flexbox row.
- **Embla's a11y plugin `latest` tag is `9.0.0-rc01` — a release candidate.** Embla core stable is
  8.6.0 and v9 is at `9.0.0-rc02`. If you install `embla-carousel-accessibility` you get an RC
  against a stable core. Flagged as a real risk; pin explicitly if you go this route.
- Embla supports RTL via `direction: 'rtl'` (default `'ltr'`) — verified in the shipped ESM source.

### 5.2 Recommendation: CSS scroll-snap, with Embla as the escape hatch

For a product gallery of 4–8 photos, `scroll-snap` wins on every axis that matters here:

- **Touch**: native momentum, native rubber-banding, native everything. No JS touch handling to get
  subtly wrong on iOS.
- **RTL**: `direction: rtl` on the container reverses it correctly with zero JS. Every library needs
  an explicit option, and the arrow-button logic has to invert too. Since the brief requires scaling
  to more locales, RTL-for-free is worth real money.
- **A11y**: it is a scrollable region. Keyboard scrolling works by default; `tabindex="0"` +
  `role="group"` + `aria-label` makes it announceable. No focus trap, no `aria-hidden` on offscreen
  slides to get wrong.
- **Degradation**: JS fails → it is still a horizontally scrollable strip of images. A JS carousel
  fails → a vertical stack of unstyled images.
- **Reduced motion**: honour it by switching `scroll-behavior` to `auto`.
- **Craft**: `scroll-snap` gives the precise, weighty snap that reads as "considered". Emulated
  drag physics usually don't.

```css
.gallery {
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: 100%;
  gap: var(--space-2);
  overflow-x: auto;
  overscroll-behavior-x: contain;   /* don't trigger browser back-swipe */
  scroll-snap-type: x mandatory;
  scrollbar-width: none;
}
.gallery::-webkit-scrollbar { display: none; }
.gallery > figure { scroll-snap-align: center; }

/* Arrows/dots are progressive enhancement — hidden until JS marks the gallery ready */
.gallery-nav { display: none; }
[data-ready] .gallery-nav { display: flex; }

@media (prefers-reduced-motion: reduce) {
  .gallery { scroll-behavior: auto; }
}
```

```html
<div class="gallery-shell" data-gallery>
  <div class="gallery" tabindex="0" role="group"
       aria-roledescription="carousel" aria-label="DTF-600 ürün görselleri">
    <figure role="group" aria-roledescription="slide" aria-label="1 / 5">…</figure>
    …
  </div>
  <div class="gallery-nav">
    <button type="button" data-prev aria-label="Önceki görsel">…</button>
    <button type="button" data-next aria-label="Sonraki görsel">…</button>
  </div>
  <div class="gallery-dots" role="tablist" aria-label="Görsel seç">…</div>
</div>
```

```js
// ~50 lines. Runs on astro:page-load so it survives ClientRouter navigation.
function initGallery(shell) {
  shell.dataset.ready = '';
  const track = shell.querySelector('.gallery');
  const slides = [...track.children];
  const dots = [...shell.querySelectorAll('[role="tab"]')];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const go = (i) => {
    const n = Math.max(0, Math.min(i, slides.length - 1));
    track.scrollTo({ left: slides[n].offsetLeft - track.offsetLeft,
                     behavior: reduce ? 'auto' : 'smooth' });
  };
  // Track the active slide without scroll listeners.
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (e.intersectionRatio < 0.6) continue;
      const i = slides.indexOf(e.target);
      dots.forEach((d, j) => {
        d.setAttribute('aria-selected', String(j === i));
        d.tabIndex = j === i ? 0 : -1;
      });
      shell.querySelector('[data-prev]').disabled = i === 0;
      shell.querySelector('[data-next]').disabled = i === slides.length - 1;
    }
  }, { root: track, threshold: 0.6 });
  slides.forEach((s) => io.observe(s));

  const active = () => dots.findIndex((d) => d.getAttribute('aria-selected') === 'true');
  shell.querySelector('[data-prev]').onclick = () => go(active() - 1);
  shell.querySelector('[data-next]').onclick = () => go(active() + 1);
  dots.forEach((d, i) => (d.onclick = () => go(i)));
  track.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') { e.preventDefault(); go(active() + 1); }
    if (e.key === 'ArrowLeft')  { e.preventDefault(); go(active() - 1); }
  });
}
document.addEventListener('astro:page-load', () =>
  document.querySelectorAll('[data-gallery]:not([data-ready])').forEach(initGallery));
```

**Use Embla 8.6.0 instead if** the design calls for infinite loop, free-drag momentum with custom
friction, or a synced thumbnail strip driving a main image. Those are genuinely hard with
scroll-snap. 7.3 KB brotli is a fair price. Pin it: `npm i embla-carousel@8.6.0`.

### 5.3 A11y requirements (W3C APG carousel pattern)

Mandatory:

- Container: `aria-roledescription="carousel"` **and** `role="region"` (or `role="group"`) **and**
  an accessible name via `aria-label` / `aria-labelledby`.
- Each slide: `role="group"` + `aria-roledescription="slide"` + `aria-label` (use `"3 / 10"` when
  slides have no unique name).
- Controls must be real `<button>` elements.
- If auto-rotating: a rotation control whose label toggles between "Stop/Start slide rotation", it
  must be the **first** tab stop, and **rotation must stop when any element in the carousel receives
  keyboard focus**.

Optional but recommended: `aria-live` + `aria-atomic` on the slide wrapper.

**For this site: do not auto-rotate.** It removes the entire rotation-control requirement, respects
`prefers-reduced-motion` by construction, and auto-rotating product photography on a B2B machinery
site is user-hostile — people are reading spec numbers.

Source: <https://www.w3.org/WAI/ARIA/apg/patterns/carousel/>

---

## 6. Contact form with no backend

### 6.1 Verified free tiers

| Service | Free tier | Notes |
|---|---|---|
| **Web3Forms** | **250 submissions/month**, unlimited forms/access keys, 30-day history | No account needed to create a key; key is public-safe |
| Formspree | **50 submissions/month**, unlimited forms, 2 notification emails, 30-day history | 5× less headroom |
| **Vercel** | **no native form product** | Only a Formspree marketplace integration |

Web3Forms Pro is $12/mo billed yearly (10 000 submissions, file uploads, webhooks, autoresponder,
domain restriction, reCAPTCHA v3 / Cloudflare Turnstile).

Sources: <https://web3forms.com/pricing>, <https://formspree.io/plans>,
<https://vercel.com/docs/integrations/cms/formspree>

**Recommendation: Web3Forms.** 250/mo is comfortably above what a B2B machinery dealer's contact
form receives, the free tier is 5× Formspree's, and the access key is explicitly designed to be
public — *"The Access Key is not a secret API Key. It can be Public and it's safe to use it in the
client-side code."* That is exactly right for a static site with no build-time secrets.

### 6.2 Markup

Endpoint: `https://api.web3forms.com/submit`, `method="POST"`.

```html
<form id="contact-form" action="https://api.web3forms.com/submit" method="POST" novalidate>
  <input type="hidden" name="access_key" value="YOUR-ACCESS-KEY-UUID">
  <input type="hidden" name="subject" value="Maven — Yeni İletişim Formu">
  <input type="hidden" name="from_name" value="maven.com.tr">
  <input type="hidden" name="redirect" value="https://maven.com.tr/tesekkurler/">

  <!-- Honeypot. Web3Forms rejects the submission if this is filled. -->
  <input type="checkbox" name="botcheck" class="hidden" style="display:none" tabindex="-1" autocomplete="off">

  <label for="cf-name">Ad Soyad</label>
  <input id="cf-name" type="text" name="name" required autocomplete="name">

  <label for="cf-company">Firma</label>
  <input id="cf-company" type="text" name="company" autocomplete="organization">

  <label for="cf-email">E-posta</label>
  <input id="cf-email" type="email" name="email" required autocomplete="email">

  <label for="cf-phone">Telefon</label>
  <input id="cf-phone" type="tel" name="phone" autocomplete="tel" inputmode="tel">

  <label for="cf-subject">İlgilendiğiniz ürün</label>
  <select id="cf-subject" name="interest">
    <option value="dtf">DTF Baskı Makineleri</option>
    <option value="uv">UV Baskı Makineleri</option>
    <option value="ink">Mürekkep &amp; Sarf Malzeme</option>
    <option value="service">Teknik Servis</option>
  </select>

  <label for="cf-message">Mesajınız</label>
  <textarea id="cf-message" name="message" rows="5" required></textarea>

  <label class="consent">
    <input type="checkbox" name="kvkk" required>
    <span>KVKK Aydınlatma Metni’ni okudum ve onaylıyorum.</span>
  </label>

  <button type="submit">Gönder</button>
  <p role="status" aria-live="polite" data-form-status></p>
</form>
```

The `redirect` hidden field makes this work **with JavaScript disabled** — a plain POST that lands
on a thank-you page. Progressive enhancement then upgrades it to AJAX:

```js
document.addEventListener('astro:page-load', () => {
  const form = document.getElementById('contact-form');
  if (!form || form.dataset.ready) return;
  form.dataset.ready = '1';
  const status = form.querySelector('[data-form-status]');
  const btn = form.querySelector('button[type=submit]');

  form.addEventListener('submit', async (e) => {
    if (!form.reportValidity()) { e.preventDefault(); return; }
    e.preventDefault();
    btn.disabled = true;
    status.textContent = 'Gönderiliyor…';
    try {
      const res = await fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify(Object.fromEntries(new FormData(form))),
      });
      const data = await res.json();
      if (data.success) { form.reset(); status.textContent = 'Teşekkürler. Mesajınız iletildi.'; }
      else { throw new Error(data.message); }
    } catch {
      status.textContent = 'Gönderilemedi. Lütfen tekrar deneyin veya bize e-posta gönderin.';
    } finally {
      btn.disabled = false;
    }
  });
});
```

Notes:
- Strip the `redirect` field before the JSON POST if you don't want the API to 302 the fetch — or
  simply leave it; the JSON endpoint returns `{ success: true }` regardless.
- **KVKK**: Turkish data-protection law. A consent checkbox plus a linked
  "Aydınlatma Metni" page is expected on a Turkish corporate site. Treat it as required content,
  not a nicety.

### 6.3 `mailto:` fallback

Never the primary path — it fails on shared/office desktops with no mail client configured, and it
leaks the address to scrapers. Use it as a visible secondary channel next to the form:

```astro
---
const to = 'info@maven.com.tr';
const subject = encodeURIComponent('Maven — Bilgi Talebi');
const body = encodeURIComponent('Firma:\nİlgilendiğim ürün:\nMesaj:\n');
---
<a href={`mailto:${to}?subject=${subject}&body=${body}`}>{to}</a>
```

Also expose a `tel:` link and a WhatsApp link (`https://wa.me/90XXXXXXXXXX`) — for Turkish B2B
industrial sales, WhatsApp is frequently the primary inbound channel and outperforms the form.

---

## 7. Local environment note

Every `bash` call in this repo emits:

```
error: We can't find the necessary environment variables to replace the Node version.
You should setup your shell profile to evaluate `fnm env` …
```

This is **cosmetic stderr noise from the shell profile**, not a failure — `node`, `npm` and `npx`
all ran correctly (Node v24.18.0, npm 11.16.0) and produced correct output throughout this research.
Worth fixing before the build work starts so real errors aren't lost in it: add
`eval "$(fnm env --use-on-cd)"` to `~/.bashrc`.

Node v24.18.0 satisfies Astro 7's `>=22.12.0` requirement.

---

## 8. Version lockfile summary

```jsonc
{
  "dependencies": {
    "astro": "7.1.5",
    "@astrojs/sitemap": "3.7.3",
    "sharp": "0.35.3"
    // "embla-carousel": "8.6.0"   // only if scroll-snap proves insufficient
  },
  "devDependencies": {
    "@gltf-transform/cli": "4.4.2"  // or install globally
  }
}
```

Vendored into `public/vendor/` (self-hosted, not CDN):
`model-viewer@4.3.1` → `dist/model-viewer.min.js` (1044 KB raw / 282 KB brotli)

Deliberately **not** installed: `@astrojs/vercel` (not needed for static),
`three` (model-viewer bundles its own, pinned to `^0.183.0`),
`@astrojs/markdown-remark` (Sätteri is sufficient), `swiper`, `keen-slider`.

Toolchain: Node ≥ 22.12, Blender 5.2 LTS + glTF add-on 5.3.18.

---

## 9. Sources

- <https://astro.build/blog/astro-7/> — Astro 7.0, released 2026-06-22
- <https://docs.astro.build/en/guides/upgrade-to/v7/>
- <https://docs.astro.build/en/guides/upgrade-to/v6/>
- <https://docs.astro.build/en/reference/configuration-reference/>
- <https://docs.astro.build/en/guides/internationalization/>
- <https://docs.astro.build/en/reference/modules/astro-i18n/>
- <https://docs.astro.build/en/guides/content-collections/>
- <https://docs.astro.build/en/reference/content-loader-reference/>
- <https://docs.astro.build/en/guides/images/> · <https://docs.astro.build/en/reference/modules/astro-assets/>
- <https://docs.astro.build/en/guides/view-transitions/>
- <https://docs.astro.build/en/guides/deploy/vercel/> · <https://docs.astro.build/en/guides/integrations-guide/vercel/>
- <https://registry.npmjs.org/astro> · `/three` · `/@google/model-viewer` · `/embla-carousel` · `/swiper` · `/keen-slider` · `/@gltf-transform/cli` (versions, engines, publish dates)
- <https://api.npmjs.org/downloads/point/last-week/> (adoption figures)
- <https://data.jsdelivr.com/v1/packages/npm/…> + `curl -H 'Accept-Encoding: br'` (transfer sizes)
- <https://threejs.org/docs/#manual/en/introduction/Color-management>
- `three@0.185.1/build/three.module.js` — grepped locally to confirm removed/current API names
- `mrdoob/three.js@dev` `examples/webgl_loader_gltf_compressed.html` — canonical KTX2 + meshopt + RoomEnvironment setup
- <https://gltf-transform.dev/cli> and `donmccurdy/glTF-Transform@main` `packages/cli/src/cli.ts`
- <https://github.com/KhronosGroup/glTF-Blender-IO> `addons/io_scene_gltf2/__init__.py`
- <https://www.blender.org/download/releases/> — Blender 5.2 LTS, 2026-07-14
- <https://www.w3.org/WAI/ARIA/apg/patterns/carousel/>
- <https://web3forms.com/pricing> · <https://docs.web3forms.com/> · <https://formspree.io/plans>
- <https://www.embla-carousel.com/docs/plugins/accessibility>
- Local measurement: esbuild 0.28 bundles of `three@0.185.1`; `zod@4.4.3` record-key semantics
