---
name: update-timeline
description: |
  Use whenever you make a significant change to the blog
  (new component, migration, refactor, workflow, library, theme/CSS change).
  Updates src/content/posts/linea_temporal_blog.mdx with an entry for the
  current month explaining the change and why.
  Run `npm run build` before updating and only commit changes that build
  successfully.
---

# Update Timeline — src/content/posts/linea_temporal_blog.mdx

Always read the current `src/content/posts/linea_temporal_blog.mdx` first.
Append or insert under the corresponding month/year section.

## Rules

1. **Only blog changes** — never include changes from `test_githubActions`.
2. **All entries in Spanish** (castellano).
3. **New component?** Describe what it does and why.
4. **Refactor/migration?** Explain the before/after.
5. **Workflow/library?** Mention the tool and purpose.
6. **If the month doesn't exist**, create a new `### Month` section under the
   correct year.
7. **If the year doesn't exist**, create a new `## Year` section.
8. **Run `npm run build` before** writing the update.
9. **Only mark build-verified changes** in the timeline.
10. Keep entries concise — one or two lines per change.
