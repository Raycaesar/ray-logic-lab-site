import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const posts = (
    await getCollection('blog', ({ data }) => data.draft !== true)
  ).sort(
    (a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf(),
  );

  return rss({
    title: 'Ray Logic Lab',
    description:
      'Logic, history of logic, Chinese logic, and research notes.',
    site: context.site,

    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.pubDate,
      link: `/${post.data.lang}/blog/${post.data.routeSlug}/`,
    })),
  });
}