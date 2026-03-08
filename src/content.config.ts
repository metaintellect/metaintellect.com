import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const timeline = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/timeline" }),
  schema: z.object({
    period: z.string(),
    role: z.string(),
    company: z.string(),
    order: z.number(),
    highlight: z.boolean().default(false),
  }),
});

const sections = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/sections" }),
  schema: z.object({
    title: z.string(),
    icon: z.string().optional(),
  }),
});

const projects = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/projects" }),
  schema: z.object({
    title: z.string(),
    subtitle: z.string(),
    description: z.string(),
    order: z.number(),
    status: z.string().optional(),
    demo: z.string().url().optional(),
    statsTitle: z.string().optional(),
    stats: z
      .array(
        z.object({
          value: z.string(),
          label: z.string(),
        }),
      )
      .optional(),
    technologies: z.array(z.string()),
  }),
});

export const collections = { timeline, sections, projects };
