import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const translationStatus = z.enum([
  'original',
  'human',
  'ai-draft',
  'reviewed',
]);

const blog = defineCollection({
  loader: glob({
    base: './src/content/blog',
    pattern: '**/*.{md,mdx}',
    generateId: ({ entry }) =>
      entry
        .replace(/\.(md|mdx)$/, '')
        .replaceAll('/', '--'),
  }),

  schema: z.object({
    title: z.string(),
    description: z.string(),

    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),

    lang: z.enum(['zh', 'en']),
    routeSlug: z.string(),

    tags: z.array(z.string()).default([]),
    series: z.string().optional(),

    draft: z.boolean().default(false),
    featured: z.boolean().default(false),

    translationKey: z.string().optional(),
    translationStatus: translationStatus.default('original'),

    support: z.boolean().default(false),
    revisionNote: z.string().optional(),

    author: z.string().default('Rui Zhu'),
  }),
});

export const collections = {
  blog,
};
