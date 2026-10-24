// @ts-check

import { defineConfig, fontProviders } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { unified } from '@astrojs/markdown-remark';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

// Consistent math support in both Markdown and MDX, so authors can write
// $...$ and $...$ directly without custom Astro math components.
const mathOptions = {
  remarkPlugins: [remarkMath],
  rehypePlugins: [[rehypeKatex, {
    throwOnError: false,
    strict: 'ignore',
    macros: {
      '\\strictif': '\\prec',
      '\\equive': '\\equiv_s',
    },
  }]],
};

export default defineConfig({
  // 部署到 Cloudflare 后，再替换为实际站点地址。
  site: 'https://ray-logic-lab-site.pages.dev',

  trailingSlash: 'always',

  integrations: [
    mdx({ processor: unified(mathOptions) }),
    sitemap(),
  ],

  fonts: [
    {
      provider: fontProviders.local(),
      name: 'Atkinson',
      cssVariable: '--font-atkinson',
      fallbacks: ['sans-serif'],
      options: {
        variants: [
          {
            src: ['./src/assets/fonts/atkinson-regular.woff'],
            weight: 400,
            style: 'normal',
            display: 'swap',
          },
          {
            src: ['./src/assets/fonts/atkinson-bold.woff'],
            weight: 700,
            style: 'normal',
            display: 'swap',
          },
        ],
      },
    },
  ],

  markdown: {
    processor: unified(mathOptions),
  },
});
