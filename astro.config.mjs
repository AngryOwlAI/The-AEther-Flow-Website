import mdx from "@astrojs/mdx";
import { unified } from "@astrojs/markdown-remark";
import { defineConfig } from "astro/config";
import rehypeKatex from "rehype-katex";
import remarkMath from "remark-math";

export default defineConfig({
  output: "static",
  redirects: {
    // Local-preview mirrors; public/_redirects remains production authority.
    "/diagrams": {
      status: 301,
      destination: "/documents/diagrams/",
    },
    "/equations": {
      status: 301,
      destination: "/documents/research/",
    },
    "/research/equations/": {
      status: 301,
      destination: "/documents/research/",
    },
    "/research/math-sample/": {
      status: 301,
      destination: "/documents/research/",
    },
    "/downloads": {
      status: 301,
      destination: "/documents/",
    },
    "/project/overview/": {
      status: 301,
      destination: "/",
    },
  },
  integrations: [mdx()],
  markdown: {
    processor: unified({
      remarkPlugins: [remarkMath],
      rehypePlugins: [rehypeKatex],
    }),
  },
});
