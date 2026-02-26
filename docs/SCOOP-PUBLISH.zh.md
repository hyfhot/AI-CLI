🌐 [English](SCOOP-PUBLISH.md) | [中文](SCOOP-PUBLISH.zh.md) | [日本語](SCOOP-PUBLISH.ja.md)

# 发布到 Scoop 教程

## 方案一：发布到官方 Scoop Bucket（推荐但审核严格）

### 1. 准备工作

**创建 GitHub Release：**
```bash
# 1. 确保代码已提交
git add .
git commit -m "Release v2.2.0"
git push

# 2. 创建并推送 tag
git tag -a v2.2.0 -m "Release version 2.2.0"
git push origin v2.2.0

# 3. 在 GitHub 网页创建 Release
# 访问：https://github.com/hyfhot/AI-CLI/releases/new
# - Tag: v2.2.0
# - Title: AI-CLI v2.2.0
# - Description: 添加版本更新说明
# - 点击 "Publish release"
```

**计算文件哈希：**
```powershell
# 下载 release 压缩包
$url = "https://github.com/hyfhot/AI-CLI/archive/refs/tags/v2.2.0.zip"
Invoke-WebRequest -Uri $url -OutFile "ai-cli-v2.2.0.zip"

# 计算 SHA256
Get-FileHash "ai-cli-v2.2.0.zip" -Algorithm SHA256 | Select-Object -ExpandProperty Hash
```

**更新 manifest 的 hash 字段：**
```json
{
    "hash": "计算出的 SHA256 值"
}
```

### 2. 提交到官方 Bucket

```bash
# Fork Scoop 官方 bucket
# 访问：https://github.com/ScoopInstaller/Main
# 点击右上角 "Fork"

# Clone 你的 fork
git clone https://github.com/你的用户名/Main.git scoop-main
cd scoop-main

# 创建新分支
git checkout -b add-ai-cli

# 复制 manifest
cp /path/to/ai-cli.json bucket/ai-cli.json

# 提交
git add bucket/ai-cli.json
git commit -m "Add ai-cli: AI CLI Launcher for coding tools"
git push origin add-ai-cli

# 在 GitHub 创建 Pull Request
# 访问你的 fork 页面，点击 "Compare & pull request"
```

**注意：** 官方 bucket 审核严格，可能需要：
- 工具有一定知名度
- 代码质量高
- 文档完善
- 可能需要等待数天到数周

---

## 方案二：创建自己的 Bucket（推荐，快速上线）

### 1. 创建 Bucket 仓库

```bash
# 在 GitHub 创建新仓库
# 仓库名：scoop-bucket（或任意名称）
# 描述：Scoop bucket for AI-CLI
# Public 仓库

# Clone 到本地
git clone https://github.com/hyfhot/scoop-bucket.git
cd scoop-bucket

# 复制 manifest
cp /path/to/ai-cli.json ./ai-cli.json

# 创建 README
cat > README.md << 'EOF'
# Scoop Bucket for AI-CLI

AI CLI Launcher - Unified terminal launcher for AI coding tools.

## Installation

```powershell
# Add this bucket
scoop bucket add ai-cli https://github.com/hyfhot/scoop-bucket

# Install AI-CLI
scoop install ai-cli
```

## Usage

```powershell
ai-cli          # Start interactive launcher
ai-cli --help   # Show help
ai-cli --init   # Initialize configuration
```

## Links

- [GitHub Repository](https://github.com/hyfhot/AI-CLI)
- [Documentation](https://github.com/hyfhot/AI-CLI/blob/master/README.md)
EOF

# 提交并推送
git add .
git commit -m "Initial commit: Add ai-cli manifest"
git push origin main
```

### 2. 用户安装方式

用户只需运行：
```powershell
# 添加你的 bucket
scoop bucket add ai-cli https://github.com/hyfhot/scoop-bucket

# 安装
scoop install ai-cli

# 使用
ai-cli
```

### 3. 更新版本

```bash
# 1. 更新主项目并创建新 tag
cd AI-CLI
git tag v2.3.0
git push origin v2.3.0

# 2. 更新 bucket 中的 manifest
cd scoop-bucket
# 编辑 ai-cli.json，更新 version 和 hash
git add ai-cli.json
git commit -m "Update ai-cli to v2.3.0"
git push

# 用户更新
scoop update ai-cli
```

---

## 方案三：提交到社区 Bucket（折中方案）

Scoop 有一些社区维护的 bucket，审核相对宽松：

### Extras Bucket（推荐）
适合 GUI 工具和非主流 CLI 工具：

```bash
# Fork https://github.com/ScoopInstaller/Extras
git clone https://github.com/你的用户名/Extras.git
cd Extras

git checkout -b add-ai-cli
cp /path/to/ai-cli.json bucket/ai-cli.json

git add bucket/ai-cli.json
git commit -m "ai-cli: Add AI CLI Launcher"
git push origin add-ai-cli

# 创建 PR 到 ScoopInstaller/Extras
```

---

## 测试 Manifest

在发布前本地测试：

```powershell
# 方法 1：直接从本地安装
scoop install /path/to/ai-cli.json

# 方法 2：从 URL 安装
scoop install https://raw.githubusercontent.com/hyfhot/scoop-bucket/main/ai-cli.json

# 测试卸载
scoop uninstall ai-cli

# 测试更新
scoop update ai-cli
```

---

## 推荐流程

**第一阶段（立即可做）：**
1. 创建自己的 bucket（方案二）
2. 在 README.md 中添加 Scoop 安装说明
3. 用户可以立即使用

**第二阶段（项目成熟后）：**
1. 提交到 Extras bucket（方案三）
2. 获得更多曝光

**第三阶段（可选）：**
1. 如果工具足够流行，提交到 Main bucket（方案一）

---

## 在 README 中添加安装说明

在你的 `README.md` 中添加：

```markdown
### 通过 Scoop 安装（推荐）

```powershell
# 添加 bucket
scoop bucket add ai-cli https://github.com/hyfhot/scoop-bucket

# 安装
scoop install ai-cli

# 使用
ai-cli
```

### 通过安装脚本

```powershell
irm https://raw.githubusercontent.com/hyfhot/AI-CLI/master/install.ps1 | iex
```
```

---

## 自动化更新（可选）

创建 GitHub Action 自动更新 hash：

```yaml
# .github/workflows/update-scoop.yml
name: Update Scoop Manifest

on:
  release:
    types: [published]

jobs:
  update:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
        with:
          repository: hyfhot/scoop-bucket
          token: ${{ secrets.SCOOP_TOKEN }}

      - name: Update manifest
        run: |
          $version = "${{ github.event.release.tag_name }}".TrimStart('v')
          $url = "https://github.com/hyfhot/AI-CLI/archive/refs/tags/v$version.zip"
          $hash = (Invoke-WebRequest $url | Get-FileHash).Hash

          $manifest = Get-Content ai-cli.json | ConvertFrom-Json
          $manifest.version = $version
          $manifest.hash = $hash
          $manifest | ConvertTo-Json -Depth 10 | Set-Content ai-cli.json

          git config user.name "github-actions"
          git config user.email "actions@github.com"
          git add ai-cli.json
          git commit -m "Update ai-cli to v$version"
          git push
```

---

需要我帮你执行哪一步？
