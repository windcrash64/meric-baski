/**
 * Content collections.
 *
 * Astro 6 deleted the legacy `src/content/config.ts` behaviour entirely: this
 * file must be `src/content.config.ts` and every collection must declare a
 * `loader`. There is no implicit "folders are collections" any more.
 *
 * The i18n guarantee lives here. `z.object({tr, en})` on every human-facing
 * block means a missing translation is a BUILD ERROR, not a page that silently
 * ships Turkish under /en/. That turns "keep the locales in sync" from a
 * discipline problem into a compile error.
 */

import { defineCollection, reference, z } from 'astro:content';
import { glob } from 'astro/loaders';

/* --- primitives ------------------------------------------------------------ */

/** Every human-facing string. Add a locale here and the build tells you what to translate. */
const i18nString = z.object({ tr: z.string(), en: z.string() });
const i18nStrings = z.object({ tr: z.array(z.string()), en: z.array(z.string()) });

const scalarOrRange = z.union([z.number(), z.tuple([z.number(), z.number()])]);

const measure = z.object({
  value: scalarOrRange,
  unit: z.string().optional(),
  note: i18nString.optional(),
});

/** A spec cell is either a measured value or a plain literal (a head name, a list). */
const specValue = z.union([measure, z.string(), z.number(), z.boolean()]);

const dimensions = z.object({
  w: z.number(),
  d: z.number(),
  h: z.number(),
  unit: z.enum(['mm', 'cm', 'm']).default('mm'),
});

const docRef = z.object({
  kind: z.enum(['catalog', 'datasheet', 'tds', 'gbf', 'certificate', 'install-checklist']),
  lang: z.enum(['tr', 'en']),
  file: z.string(),
  bytes: z.number(),
  version: z.string().optional(),
  date: z.string().optional(),
});

const mediaRef = z.object({
  src: z.string(),
  alt: i18nString,
  caption: i18nString.optional(),
  kind: z.enum(['machine', 'application', 'detail', 'diagram']).default('machine'),
});

const faq = z.array(z.object({ q: z.string(), a: z.string() }));

/* --- machines --------------------------------------------------------------- */

const MACHINE_FAMILIES = [
  'uv-flatbed', 'uv-hybrid', 'eco-solvent', 'dtf', 'sublimation', 'uv-dtf', 'cutting',
] as const;

const printhead = z.object({
  brand: z.enum(['ricoh', 'konica', 'epson', 'kyocera', 'toshiba', 'starfire']),
  model: z.string(),
  count: scalarOrRange,
  dropSizePl: scalarOrRange.optional(),
});

const machines = defineCollection({
  loader: glob({ pattern: '**/*.yaml', base: './src/content/machines' }),
  schema: z.object({
    sku: z.string(),
    model: z.string(),
    family: z.enum(MACHINE_FAMILIES),
    /** Drives the register of the copy, never rendered as a badge. */
    tier: z.enum(['entry', 'mid', 'upper-mid', 'industrial', 'flagship']),
    order: z.number(),
    featured: z.boolean().default(false),
    status: z.enum(['active', 'on-request', 'discontinued']).default('active'),

    /** Machines are always quote-only. A fabricated price is worse than none. */
    price: z.null().default(null),
    leadTimeWeeks: z.tuple([z.number(), z.number()]).optional(),

    /** Exactly four, resolved out of `specs` for the PDP hero. */
    headline: z.array(z.string()).length(4),

    printhead,
    headOptions: z.array(printhead).optional(),

    specs: z.record(z.string(), specValue),

    /**
     * Always an array. A single "speed" number is the clearest tell of a
     * fabricated catalogue — real machines publish a per-pass table.
     */
    speedModes: z.array(z.object({
      pass: z.number(),
      value: scalarOrRange,
      unit: z.literal('m2/h').default('m2/h'),
      mode: i18nString.optional(),
    })).min(1),

    /** DTF shaker, calender — parts of a system, not separate SKUs. */
    components: z.array(z.object({
      sku: z.string(),
      name: i18nString,
      role: i18nString,
      specs: z.record(z.string(), specValue).optional(),
    })).optional(),

    compatibleInks: z.array(z.string()).default([]),
    applications: z.array(z.string()).default([]),
    substrates: z.array(z.string()).default([]),
    siblings: z.array(z.string()).default([]),
    rip: z.array(z.string()).default([]),

    /** The honest block nobody else publishes. */
    installation: z.object({
      powerPhase: z.enum(['1F', '3F']),
      floorAreaM2: z.number(),
      ceilingHeightM: z.number(),
      cratedDimensions: dimensions,
      ventilationRequired: z.boolean(),
      compressedAir: z.string().optional(),
      notIncluded: i18nStrings,
    }),

    gallery: z.array(mediaRef).default([]),
    model3d: z.object({
      glb: z.string(),
      poster: z.string(),
      triangles: z.number(),
      bytes: z.number(),
      hotspots: z.array(z.object({
        key: z.string(),
        position: z.string(),
        normal: z.string(),
        label: i18nString,
        body: i18nString.optional(),
      })).default([]),
    }).optional(),
    videos: z.array(z.object({
      url: z.string().url(),
      title: i18nString,
      thumb: z.string(),
    })).optional(),
    documents: z.array(docRef).default([]),

    i18n: z.object({
      tr: machineProse(),
      en: machineProse(),
    }),
  }),
});

function machineProse() {
  return z.object({
    name: z.string().optional(),
    /** Benefit pair joined by a comma — the established TR pattern. */
    tagline: z.string(),
    /** 60–90 words. Not 110. */
    summary: z.string(),
    features: z.array(z.object({
      /** An ownable technology name, reused across the site. */
      term: z.string(),
      body: z.string(),
    })).min(3).max(6),
    faq: faq.min(3).max(8),
    /** JSON-LD only — never rendered. Carries "makinası", "ekosolvent" etc. */
    alternateName: z.array(z.string()).optional(),
  });
}

/* --- inks ------------------------------------------------------------------- */

const INK_FAMILIES = [
  'uv', 'uv-led', 'uv-dtf', 'eco-solvent', 'solvent',
  'sublimation', 'dtf', 'textile-pigment', 'auxiliary',
] as const;

const inks = defineCollection({
  loader: glob({ pattern: '**/*.yaml', base: './src/content/inks' }),
  schema: z.object({
    sku: z.string(),
    series: z.string(),
    family: z.enum(INK_FAMILIES),
    type: z.enum(['ink', 'auxiliary', 'powder', 'film', 'printhead', 'spare']).default('ink'),
    order: z.number(),
    featured: z.boolean().default(false),

    /** Load-bearing in this market — buyers search by what they are replacing. */
    oemEquivalent: z.array(z.string()).default([]),
    changeover: z.enum(['switch-and-print', 'switch-and-swap', 'switch-and-match']),

    channels: z.array(z.object({
      code: z.string(),
      sku: z.string(),
      availability: z.enum(['stock', 'on-request']).default('stock'),
    })).default([]),

    packaging: z.array(z.object({
      format: z.enum(['bottle', 'bag', 'bag-in-box', 'cartridge', 'pouch', 'drum', 'sack', 'roll']),
      volume: z.number(),
      unit: z.enum(['ml', 'L', 'kg', 'm']),
      note: i18nString.optional(),
    })).default([]),

    compat: z.object({
      printheads: z.array(z.string()).default([]),
      dropSizePl: z.tuple([z.number(), z.number()]).optional(),
      machines: z.array(z.string()).default([]),
      /** Text only, never a logo — we do not have the marks cleared. */
      thirdPartyPrinters: z.array(z.string()).default([]),
      chipIncluded: z.boolean().default(false),
    }),

    specs: z.object({
      cure: z.object({
        method: z.enum(['uv-hg', 'uv-led', 'heat', 'calender', 'air', 'none']),
        doseMjCm2: z.tuple([z.number(), z.number()]).optional(),
        intensityMwCm2: z.number().optional(),
        wavelengthNm: z.number().optional(),
        postCureHours: z.number().optional(),
        transferTempC: z.tuple([z.number(), z.number()]).optional(),
        transferSeconds: z.tuple([z.number(), z.number()]).optional(),
        fixationC: z.number().optional(),
      }),
      shelfLifeMonths: z.number(),
      shelfLifeNote: i18nString.optional(),
      storageTempC: z.tuple([z.number(), z.number()]),
      operatingTempC: z.tuple([z.number(), z.number()]).optional(),
      operatingHumidityPct: z.tuple([z.number(), z.number()]).optional(),
      outdoorDurabilityMonths: z.number().optional(),
      /** Required whenever a durability figure is published — an unscoped
          "5 years outdoors" reads as fake to anyone who has read a real TDS. */
      outdoorDurabilityNote: i18nString.optional(),

      /* Aqueous / DTF / textile only. Real UV and solvent TDS do not publish
         viscosity, and doing so exposes the data as invented. */
      viscosityCps: z.object({ value: z.number(), tolerance: z.number(), atC: z.number() }).optional(),
      surfaceTensionDyn: z.object({ value: z.number(), tolerance: z.number() }).optional(),
      ph: z.object({ value: z.number(), tolerance: z.number() }).optional(),
      particleSizeNm: z.tuple([z.number(), z.number()]).optional(),
      fastness: z.array(z.object({ standard: z.string(), result: z.string() })).optional(),
    }),

    substrates: z.array(z.string()).default([]),
    applications: z.array(z.string()).default([]),

    /** Always attributed to the manufacturer, never rendered as a Maven mark. */
    certifications: z.array(z.object({
      mark: z.enum(['greenguard-gold', 'eco-passport', 'zdhc', 'en-71-3', 'reach', 'iso-9001']),
      issuedTo: z.string(),
    })).default([]),

    documents: z.array(docRef).default([]),
    ancillaries: z.array(z.string()).default([]),
    gallery: z.array(mediaRef).default([]),

    /** Consumables MAY carry a USD price with a visible "KDV hariç" label. */
    price: z.union([
      z.null(),
      z.object({ amount: z.number(), currency: z.literal('USD'), vatIncluded: z.literal(false) }),
    ]).default(null),

    i18n: z.object({ tr: inkProse(), en: inkProse() }),
  })
    .superRefine((data, ctx) => {
      // A published durability figure without a scope is the classic fake tell.
      if (data.specs.outdoorDurabilityMonths && !data.specs.outdoorDurabilityNote) {
        ctx.addIssue({
          code: 'custom',
          path: ['specs', 'outdoorDurabilityNote'],
          message: 'outdoorDurabilityMonths requires outdoorDurabilityNote scoping the claim',
        });
      }
      // Real UV/solvent technical data sheets do not publish viscosity.
      if (data.specs.viscosityCps && ['uv', 'uv-led', 'uv-dtf', 'solvent'].includes(data.family)) {
        ctx.addIssue({
          code: 'custom',
          path: ['specs', 'viscosityCps'],
          message: `viscosity must not be published for ${data.family} inks — real TDS do not`,
        });
      }
      // Every chemical we sell ships with a Turkish safety data sheet.
      if (data.type === 'ink' && !data.documents.some((d) => d.kind === 'gbf' && d.lang === 'tr')) {
        ctx.addIssue({
          code: 'custom',
          path: ['documents'],
          message: 'every ink needs a Turkish Güvenlik Bilgi Formu (kind: gbf, lang: tr)',
        });
      }
    }),
});

function inkProse() {
  return z.object({
    name: z.string().optional(),
    /** "Ricoh Gen5/Gen6 kafalar için UV-LED" */
    role: z.string(),
    summary: z.string(),
    features: z.array(z.string()).min(4).max(8),
    /** The testing caveat, on every ink page. */
    disclaimer: z.string(),
    faq: faq.optional(),
  });
}

/* --- applications ------------------------------------------------------------ */

const applications = defineCollection({
  loader: glob({ pattern: '**/*.yaml', base: './src/content/applications' }),
  schema: z.object({
    key: z.enum(['signage', 'packaging', 'interior', 'industrial', 'textile', 'vehicle']),
    order: z.number(),
    accent: z.enum(['cyan', 'magenta', 'yellow']).default('cyan'),
    hero: mediaRef,
    gallery: z.array(mediaRef).default([]),
    machines: z.array(z.string()).default([]),
    inks: z.array(z.string()).default([]),
    substrates: z.array(z.string()).default([]),
    i18n: z.object({
      tr: applicationProse(),
      en: applicationProse(),
    }),
  }),
});

function applicationProse() {
  return z.object({
    name: z.string(),
    /** An action phrase, not a noun: "Şehirde görün". */
    kicker: z.string(),
    intro: z.string(),
    jobs: z.array(z.string()).min(3),
    faq: faq.min(2),
  });
}

/* --- insights ---------------------------------------------------------------- */

const insights = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/insights' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    locale: z.enum(['tr', 'en']),
    /** Ties the TR and EN version of one article together for hreflang. */
    translationKey: z.string(),
    date: z.coerce.date(),
    updated: z.coerce.date().optional(),
    hero: mediaRef.optional(),
    tags: z.array(z.string()).default([]),
    related: z.array(reference('machines')).default([]),
    draft: z.boolean().default(false),
  }),
});

export const collections = { machines, inks, applications, insights };
