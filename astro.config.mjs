import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

export default defineConfig({
  site: 'https://ray-logic-lab-preview.pages.dev',

  trailingSlash: 'always',

  integrations: [
    sitemap(),
  ],

  markdown: {
    remarkPlugins: [
      remarkMath,
    ],
    rehypePlugins: [
      rehypeKatex,
    ],
  },
});