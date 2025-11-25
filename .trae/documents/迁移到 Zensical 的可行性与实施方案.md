## 结论

* 可行：Zensical承诺兼容现有的 `mkdocs.yml`、Markdown 扩展、项目结构与模板覆盖，初期即可构建大多数 Material for MkDocs 项目 \[1]\[3]\[4]。

* 条件：当前站点依赖多款第三方插件与 Python 钩子，部分功能需要临时替代或调整后再迁移；建议先在独立分支进行验证。

## 为什么考虑 Zensical

* 更快的增量构建与更现代的运行时（Rust + ZRX），对大型文档站点友好 \[4]\[5]。

* 原生或规划中的功能涵盖搜索、版本管理、API 文档、国际化、压缩优化、博客/标签等，目标是与 Material for MkDocs 达到特性对等 \[2]\[5]。

## 当前站点清单

* 主题与模板：Material 主题，`overrides/` 自定义模板与 `extra_css`/`extra_javascript`（`mkdocs.yml:33-95,160-179`）。

* Markdown 扩展：`pymdownx.*`、`admonition`、`tabbed`、`details` 等（`mkdocs.yml:100-154`）。

* 插件：`search`、`rss`、`glightbox`、`git-revision-date-localized`、`minify`、`mkdocs-video`、`statistics`（改装版）、`heti`、`blogging`（`mkdocs.yml:210-285`；版本与列表见 `requirements.txt:2-20`）。

* 钩子：`hooks/theme_override.py`、`hooks/linkbackward.py`、`hooks/toc.py`、`hooks/tikzautomata.py` 使用 MkDocs 钩子API（例如 `theme_override.py:20-39`、`linkbackward.py:73-120`、`toc.py:45-62`、`tikzautomata.py:26-76`）。

* CI：GitHub Pages，严格构建并上传产物（`.github/workflows/ci.yml:1-58`）。

## 兼容性评估

* 配置与内容：`mkdocs.yml` 可被 Zensical 直接读取；Python Markdown 扩展保持兼容，项目结构、URL 与锚点保持不变 \[1]\[3]\[4]。

* 主题与模板覆盖：MiniJinja 兼容下的小幅调整；整体 HTML 结构与 CSS 变量保持一致，可复用 `overrides/` 与自定义样式 \[3]。

* 插件映射与现状：

  * `search` → 原生搜索：兼容。

  * `minify` → 原生构建优化：兼容/内置 \[2]。

  * `git-revision-date-localized` → 原生 Git 元数据：规划内置 \[2]。

  * `macros` → 组件系统替代：规划兼容 \[2]。

  * `mike`（版本管理）→ Zensical 提供改进工作流：规划兼容 \[2]。

  * `blogging`/`tags` → 路线图明确支持 \[5]。

  * `static-i18n`（若后续需要）→ 原生国际化：规划兼容 \[2]。

  * `glightbox`、`mkdocs-video`、`rss`、`statistics`、`heti`：官方未列为首批重点，短期可能需替代方案（如自定义模板/CSS、构建后脚本或临时禁用）。`heti` 多依赖 CSS，可沿用现有 `css/heti.css`。

* 钩子（Python Hooks）：Zensical 的运行时与模块体系不再使用 MkDocs 的 Python 钩子机制。当前自定义钩子需：

  * `theme_override`：可通过模板/JS 实现同等 DOM 标记；或等待组件系统。

  * `linkbackward`（批量重定向）：改为静态重定向文件清单或构建后脚本生成；也可用 Nginx/GitHub Pages 级别重定向策略。

  * `toc`（自定义目录块渲染与统计）：迁移为模板/组件；统计逻辑可在构建阶段以脚本计算并注入。

  * `tikzautomata`（LaTeX/TikZ 到 SVG）：保留当前 Python 渲染链作为预处理；或改为本地/CI 预编译生成 SVG 并在 Markdown 引用。

## 迁移方案（分支试运行）

* 建立验证分支：`feature/zensical-migration`。

* 安装与试构建：

  * 本地/CI 安装：`pip install zensical`（或 `uv add zensical`）\[4]。

  * 在项目根执行：`zensical build`（沿用现有 `mkdocs.yml`）。

* 逐项对齐：

  * 先移除/禁用不兼容插件与钩子，保证可生成站点。

  * 检查页面功能：搜索、代码高亮、KaTeX、Mermaid、任务列表、标签页、中文排版、博客列表与分页。

  * 针对 `glightbox`/`video`/`rss`/`statistics`/`heti`：用模板覆盖与 CSS 复现必要UI；统计可暂时下线或以外部脚本填充；RSS 可临时用轻量脚本生成。

  * 比较 HTML 结构与样式差异，确保 `overrides/` 与 `extra_css`/`extra_javascript` 行为一致。

* CI 改造（验证阶段）：

  * 在现有工作流中新增一个并行 Job，仅执行 `zensical build`，并上传独立 Preview Artifact，不影响正式发布（保留 MkDocs 主流程）。

  * 当验证通过后，将发布步骤切换到 Zensical 产物。

## 验证标准

* 构建稳定：无报错，产物完整；增量构建时间显著下降。

* 兼容性：现有 URL、锚点、导航不变；搜索可用；代码块/提示框/标签页/脚注正常。

* 数学与图形：KaTeX、Mermaid 与 TikZ（若改为预编译）渲染正确。

* 博客与标签：分页与 RSS（如保留）工作正常或提供替代方案。

* 中文排版：`heti` 效果可通过现有 CSS 保持一致。

## 回滚与并行策略

* 在验证完成前，保留 MkDocs 生产构建；Zensical 构建仅用于预览与对比。

* 若关键功能在路线图内但暂未到位，则延后切换并跟踪官方进度 \[5]。

## 预估投入

* 初次试构建与对齐：0.5–1 天。

* 钩子替代与插件兼容：按功能复杂度 1–3 天（并行可缩短）。

* CI 并行验证与切换：0.5 天。

## 交付物

* 兼容性清单（逐项功能与差异）。

* 可构建的 Zensical 产物与预览链接。

* 更新后的 CI 工作流（并行/切换两套）。

* 替代实现（模板/CSS/脚本）与移植说明。

## 参考资料

* \[1] Zensical 兼容性与迁移文章（Material 官方博客）：<https://squidfunk.github.io/mkdocs-material/blog/2025/11/05/zensical/>

* \[2] Zensical 对第三方插件的支持与规划：<https://zensical.org/compatibility/plugins/>

* \[3] Zensical 兼容性总览与阶段策略：<https://zensical.org/compatibility/>

* \[4] Zensical 安装与快速上手指南：<https://zensical.org/docs/get-started/>

* \[5] Zensical 路线图（特性对等与博客/标签等）：<https://zensical.org/about/roadmap/>

