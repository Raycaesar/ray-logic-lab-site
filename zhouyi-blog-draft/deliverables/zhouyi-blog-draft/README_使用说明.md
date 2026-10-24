# 周易卦序中文博客底稿包

本包按 `Raycaesar/ray-logic-lab-site` 当前的 Astro 内容结构整理，未对 GitHub 仓库做任何提交或修改。

仓库已经安装 `@astrojs/mdx`，但当前 `astro.config.mjs` 尚未把 `mdx()` 加入 `integrations`。由于底稿嵌入了 Astro 交互组件，使用前需按 `astro.config.mjs_启用MDX.diff` 增加两行配置。若不需要交互演示，也可删除文章中的组件导入和 `<IChingSequenceExplorer />`，再把扩展名改成 `.md`，其余正文、公式、代码和四张 SVG 图不受影响。

## 文件对应位置

- `src/content/blog/zh/zhouyi-hexagram-sequence-radisic-shen-zhang.mdx`：中文长篇底稿，含网站所需前置信息，不在正文重复一级标题。
- `src/components/IChingSequenceExplorer.astro`：错、综、轨道、权重和匹配能量的交互演示。
- `public/images/zhouyi/king-wen-math-pipeline.svg`：从六维状态空间到完整卦序的分层机制。
- `public/images/zhouyi/k4-orbit-example.svg`：屯、蒙、革、鼎四元轨道及三种完美匹配。
- `public/images/zhouyi/shen-sequence-skeleton.svg`：沈有鼎主卦骨架与三十、三十四分篇。
- `public/images/zhouyi/trigram-coordinate-system.svg`：八卦阴阳族与父母长中少坐标。
- `scripts/verify_iching_sequence.py`：独立有限核验程序。
- `astro.config.mjs_启用MDX.diff`：启用仓库已安装的 MDX 集成所需的最小配置差异。

## 放入博客仓库

把本包中的 `src`、`public` 目录内容合并到博客仓库同名目录即可。文章已经用以下相对路径导入组件：

```mdx
import IChingSequenceExplorer from '../../../components/IChingSequenceExplorer.astro';
```

再把 MDX 集成加入 `astro.config.mjs`：

```js
import mdx from '@astrojs/mdx';

export default defineConfig({
  integrations: [
    mdx(),
    sitemap(),
  ],
});
```

图片均使用 Astro `public` 目录下的绝对网址，例如：

```md
![分层数学机制](/images/zhouyi/king-wen-math-pipeline.svg)
```

## 发布前建议核对

1. 核实 Alejandro Radisic 是否适合表述为“墨西哥学者”；公开论文和代码页面只足以确认其独立研究者身份。
2. 重新检查 arXiv 是否已有第四版，以及公开 Lean 4 仓库是否已同步第三版的权重优化模块。
3. 如能取得张清宇 2011 年《周易卦序结构分析》全文，补核其是否写明 2000 年略去的两条组内排序原则。
4. 依个人行文风格删减摘要、表格、程序或附录；当前文本有意保留较多论证和限定语。
5. 若网站后来修改内容集合的前置信息结构，按 `src/content.config.ts` 同步更新文章头部字段。

## 运行独立核验

项目外也可直接运行：

```bash
python3 scripts/verify_iching_sequence.py
```

预期核心输出：

```text
轨道：20 = 8 个二元 + 12 个四元
主卦组 / 散卦组：6 / 14
通行本匹配汉明成本：120
完整 K4 候选类纯距离最优：96
秩优先词典序最优：(4, 120)
逐轨道唯一：是
```
