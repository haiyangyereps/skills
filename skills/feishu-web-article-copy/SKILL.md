---
name: feishu-web-article-copy
description: Create local Markdown and browser-copyable HTML from web articles or rendered documents for pasting into Feishu or Lark Docs while preserving original remote image URLs. Use when the user wants to copy an article into Feishu, remote Markdown images or pasted HTML image tags do not render, images must remain original links rather than downloaded files, or a page needs to be copied as rendered rich text with image src URLs intact.
---

# Feishu Web Article Copy

## Core Rule

Preserve original image URLs by default. Do not download images unless the user explicitly asks.

The reliable Feishu path is not pasting Markdown source or literal image tags. Generate an HTML page, open it in a browser, let images render, then copy the rendered page into Feishu.

## Workflow

1. Extract the article.
   - Prefer structured API data when available.
   - If the page is rendered or virtualized, use a browser session, scroll through the whole document, collect blocks by stable index or id, and verify there are no gaps.
   - Preserve each rendered image `src` exactly.

2. Write a source Markdown file.
   - Use headings, paragraphs, lists, tables, and `![](original-url)` image syntax.
   - Keep the original source URL near the top when useful.
   - Verify image count and any virtualized block range.

3. Generate Feishu-copyable HTML.
   - Use `scripts/md_to_feishu_html.py` for Markdown inputs.
   - The output should contain real rendered image elements with original `src` URLs.
   - Tell the user to open the HTML in a browser, wait for images to load, then use `Cmd+A`, `Cmd+C`, and paste into Feishu.
   - Do not tell the user to copy the HTML source text.

4. Validate.
   - Count Markdown image links and HTML image tags; counts should match.
   - Inspect the first few output lines to confirm image URLs are present.
   - If the browser HTML shows images but Feishu still drops them, Feishu is refusing those remote sources. The remaining options are uploading images or using Feishu APIs.

## Script

Convert Markdown with remote images to a browser-copyable HTML page:

```bash
python3 scripts/md_to_feishu_html.py article.md -o article-复制到飞书.html --title "文章标题"
```

Options:

- `--title`: set the browser page title.
- `--keep-link-captions`: add visible original-link captions under images. Use only when the user wants links visible in the pasted doc.

## Delivery Text

When finished, provide both paths if both exist:

- Markdown source file for archive/import.
- HTML copy page for Feishu paste.

Use this instruction wording:

Open the HTML in a browser, wait for all images to display, then copy the rendered page into Feishu. Do not copy the HTML source.
