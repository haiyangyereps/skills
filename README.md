# Codex Skills

这个仓库用于管理和分享可复用的 Codex Skills。

当前包含的 skill：

- `feishu-web-article-copy`：把网页文章整理成本地 Markdown，并生成适合复制到飞书或 Lark Docs 的 HTML 页面。图片默认保留原始远程链接，不下载到本地。

## 目录结构

```text
skills/
  feishu-web-article-copy/
    SKILL.md
    agents/
      openai.yaml
    scripts/
      md_to_feishu_html.py
```

## 安装方式

把需要使用的 skill 目录复制到本机 Codex skills 目录：

```bash
mkdir -p ~/.codex/skills
cp -R skills/feishu-web-article-copy ~/.codex/skills/
```

安装后，在 Codex 里可以通过 `$feishu-web-article-copy` 调用。

## feishu-web-article-copy

适用场景：

- 复制网页文章到飞书文档。
- Markdown 图片链接粘贴到飞书后不渲染。
- 希望保留图片原始链接，而不是下载图片。
- 需要生成一个浏览器可打开、可全选复制的 HTML 页面。

核心流程：

1. 提取网页正文内容和图片原始 URL。
2. 生成本地 Markdown 文件，图片使用 `![](原始图片链接)`。
3. 使用脚本把 Markdown 转成 HTML。
4. 在浏览器打开 HTML，等待图片显示后，全选复制渲染后的页面到飞书。

脚本示例：

```bash
cd skills/feishu-web-article-copy
python3 scripts/md_to_feishu_html.py article.md -o article-复制到飞书.html --title "文章标题"
```

可选参数：

- `--title`：设置 HTML 页面的标题。
- `--keep-link-captions`：在图片下方显示原图链接，仅在需要把链接明文保留到文档里时使用。

## 注意事项

- 默认不下载图片，只保留原始远程图片链接。
- 不建议把 HTML 源码直接复制到飞书；应该复制浏览器里渲染后的页面。
- 如果浏览器里能显示图片，但粘贴到飞书后仍不显示，通常是飞书拒绝了对应远程图片源。此时只能改为上传图片，或使用飞书 API 处理图片。

