// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

import { SITE } from './src/config/site.js';

export default defineConfig({
  site: SITE.url,
  output: 'static',

  // One canonical URL shape. Must agree with vercel.json's trailingSlash.
  trailingSlash: 'always',
  build: { format: 'directory' },

  // Astro 7 changed the default to 'jsx', which strips the whitespace between
  // inline elements (`<a>x</a> <a>y</a>` loses its space). This design is
  // typography-led, so opt back out.
  compressHTML: true,

  image: {
    layout: 'constrained',
    // Defaults to false: without it `layout` emits a srcset but no responsive
    // sizing, which silently costs the whole point of the image service.
    responsiveStyles: true,
    objectFit: 'cover',
  },

  i18n: {
    defaultLocale: 'tr',
    locales: ['tr', 'en'],
    routing: {
      prefixDefaultLocale: false,
      redirectToDefaultLocale: false,
      fallbackType: 'redirect',
    },
  },

  integrations: [
    sitemap({
      i18n: { defaultLocale: 'tr', locales: { tr: 'tr-TR', en: 'en-US' } },
      filter: (page) => !page.includes('/tesekkurler/') && !page.includes('/thank-you/'),
    }),
  ],
});
