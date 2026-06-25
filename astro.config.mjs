import mdx from "@astrojs/mdx";
import { unified } from "@astrojs/markdown-remark";
import { defineConfig } from "astro/config";
import rehypeKatex from "rehype-katex";
import remarkMath from "remark-math";

export default defineConfig({
  output: "static",
  integrations: [mdx()],
  markdown: {
    processor: unified({
      remarkPlugins: [remarkMath],
      rehypePlugins: [rehypeKatex],
    }),
  },
});
