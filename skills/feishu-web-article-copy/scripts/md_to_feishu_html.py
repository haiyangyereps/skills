#!/usr/bin/env python3
"""Convert Markdown with remote images into browser-copyable Feishu HTML.

The script preserves original image URLs. It does not download images.
"""
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


def inline_md(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    return text


def md_table_to_html(lines: list[str]) -> str:
    rows = []
    for line in lines:
        cells = [inline_md(c.strip()) for c in line.strip().strip('|').split('|')]
        rows.append(cells)
    rows = [r for i, r in enumerate(rows) if not (i == 1 and all(re.fullmatch(r":?-+:?", re.sub(r"<[^>]+>", "", c)) for c in r))]
    if not rows:
        return ""
    head, body = rows[0], rows[1:]
    thead = "<thead><tr>" + "".join(f"<th>{c}</th>" for c in head) + "</tr></thead>"
    tbody = "<tbody>" + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in body) + "</tbody>"
    return f"<table>{thead}{tbody}</table>"


def markdown_to_body(md: str, keep_link_captions: bool = False) -> str:
    lines = md.splitlines()
    out: list[str] = []
    para: list[str] = []
    list_type: str | None = None
    list_items: list[str] = []
    table_lines: list[str] = []
    image_count = 0

    def flush_para() -> None:
        nonlocal para
        if para:
            out.append(f"<p>{inline_md(' '.join(para))}</p>")
            para = []

    def flush_list() -> None:
        nonlocal list_type, list_items
        if list_type:
            out.append(f"<{list_type}>" + "".join(f"<li>{inline_md(x)}</li>" for x in list_items) + f"</{list_type}>")
            list_type = None
            list_items = []

    def flush_table() -> None:
        nonlocal table_lines
        if table_lines:
            rendered = md_table_to_html(table_lines)
            if rendered:
                out.append(rendered)
            table_lines = []

    for raw in lines:
        line = raw.strip()
        if not line:
            flush_para(); flush_list(); flush_table()
            continue
        if re.match(r"^\|.*\|$", line):
            flush_para(); flush_list()
            table_lines.append(line)
            continue
        flush_table()

        img = re.match(r"^!\[([^\]]*)\]\((https?://[^)]+)\)$", line)
        if img:
            flush_para(); flush_list()
            image_count += 1
            alt = img.group(1).strip() or f"图片{image_count:03d}"
            url = img.group(2)
            figcaption = f"<figcaption>{html.escape(alt)}</figcaption>" if alt else ""
            link_caption = f"<div class=\"source-link\">原图链接：{html.escape(url)}</div>" if keep_link_captions else ""
            out.append(f'<figure><img src="{html.escape(url, quote=True)}" alt="{html.escape(alt, quote=True)}">{figcaption}{link_caption}</figure>')
            continue

        html_img = re.match(r'^<img\s+src="([^"]+)"(?:\s+alt="([^"]*)")?\s*/?>$', line)
        if html_img:
            flush_para(); flush_list()
            image_count += 1
            url = html_img.group(1)
            alt = html_img.group(2) or f"图片{image_count:03d}"
            figcaption = f"<figcaption>{html.escape(alt)}</figcaption>" if alt else ""
            link_caption = f"<div class=\"source-link\">原图链接：{html.escape(url)}</div>" if keep_link_captions else ""
            out.append(f'<figure><img src="{html.escape(url, quote=True)}" alt="{html.escape(alt, quote=True)}">{figcaption}{link_caption}</figure>')
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            flush_para(); flush_list()
            level = len(heading.group(1))
            out.append(f"<h{level}>{inline_md(heading.group(2))}</h{level}>")
            continue

        unordered = re.match(r"^[-*]\s+(.+)$", line)
        if unordered:
            flush_para()
            if list_type != "ul":
                flush_list(); list_type = "ul"
            list_items.append(unordered.group(1))
            continue

        ordered = re.match(r"^\d+\.\s+(.+)$", line)
        if ordered:
            flush_para()
            if list_type != "ol":
                flush_list(); list_type = "ol"
            list_items.append(ordered.group(1))
            continue

        para.append(line)

    flush_para(); flush_list(); flush_table()
    return "\n".join(out)


def build_html(body: str, title: str) -> str:
    return f"""<!doctype html>
<html lang=\"zh-CN\">
<head>
<meta charset=\"utf-8\">
<title>{html.escape(title)}</title>
<style>
  body{{font-family:-apple-system,BlinkMacSystemFont,\"Segoe UI\",\"PingFang SC\",\"Microsoft YaHei\",sans-serif;line-height:1.72;color:#1f2329;max-width:900px;margin:40px auto;padding:0 28px;background:#fff;font-size:16px;}}
  h1{{font-size:30px;margin:32px 0 20px;}} h2{{font-size:24px;margin:30px 0 14px;}} h3{{font-size:20px;margin:24px 0 12px;}}
  p{{margin:12px 0;}} figure{{margin:22px 0;text-align:center;}} img{{max-width:100%;height:auto;display:inline-block;}} figcaption,.source-link{{font-size:12px;color:#8f959e;margin-top:6px;word-break:break-all;}}
  ul,ol{{padding-left:1.5em;}} li{{margin:8px 0;}} table{{border-collapse:collapse;width:100%;margin:18px 0;}} th,td{{border:1px solid #dee0e3;padding:8px;vertical-align:top;}} th{{background:#f5f6f7;}}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert Markdown to Feishu-copyable HTML with remote img src URLs.")
    parser.add_argument("input", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    parser.add_argument("--title", default=None)
    parser.add_argument("--keep-link-captions", action="store_true")
    args = parser.parse_args()

    md = args.input.read_text(encoding="utf-8")
    title = args.title or args.input.stem
    body = markdown_to_body(md, keep_link_captions=args.keep_link_captions)
    doc = build_html(body, title)
    output = args.output or args.input.with_name(args.input.stem + "-复制到飞书.html")
    output.write_text(doc, encoding="utf-8")
    img_count = doc.count("<img ")
    print(f"wrote {output}")
    print(f"img_tags={img_count}")


if __name__ == "__main__":
    main()
