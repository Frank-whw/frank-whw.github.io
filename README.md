# Frank's Blog

这是我的个人博客，基于 MkDocs 构建，使用 Material for MkDocs 主题。

## 特性

- 📝 支持 Markdown 写作
- 🎨 Material Design 风格
- 🌙 自动深色模式
- 📊 数学公式支持
- 🔍 全站搜索
- 📱 移动端适配
- 💻 代码高亮
- 📈 阅读时间统计

## 本地开发

### 环境要求

- Python 3.8+
- pip

### 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/Frank-whw/Frank-whw.github.io.git
cd Frank-whw.github.io
```

2. 创建并激活虚拟环境
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/MacOS
source .venv/bin/activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 本地运行
```bash
mkdocs serve
```

5. 在浏览器中访问 `http://127.0.0.1:8000`

### 部署

项目使用 GitHub Actions 自动部署到 GitHub Pages。只需要推送到 main 分支，GitHub Actions 会自动构建并部署网站。

## 目录结构

```
.
├── docs/               # 文档目录
├── overrides/          # 主题覆盖文件
├── .github/            # GitHub Actions 配置
├── .gitignore         # Git 忽略文件
├── mkdocs.yml         # MkDocs 配置文件
└── requirements.txt    # Python 依赖
```