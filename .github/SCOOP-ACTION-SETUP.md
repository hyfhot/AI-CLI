# GitHub Action 配置说明

## 自动更新 Scoop Manifest

这个 GitHub Action 会在你创建新 Release 时自动更新 scoop-bucket 仓库中的 manifest。

## 设置步骤

### 1. 创建 Personal Access Token (PAT)

1. 访问 GitHub Settings: https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 设置：
   - Note: `Scoop Bucket Update`
   - Expiration: `No expiration` 或选择合适的时间
   - 勾选权限：
     - ✅ `repo` (Full control of private repositories)
     - ✅ `workflow` (Update GitHub Action workflows)
4. 点击 "Generate token"
5. **复制生成的 token**（只显示一次）

### 2. 添加 Secret 到 AI-CLI 仓库

1. 访问 AI-CLI 仓库设置: https://github.com/hyfhot/AI-CLI/settings/secrets/actions
2. 点击 "New repository secret"
3. 设置：
   - Name: `SCOOP_TOKEN`
   - Secret: 粘贴刚才复制的 PAT
4. 点击 "Add secret"

### 3. 创建 scoop-bucket 仓库

```bash
# 在 GitHub 创建新仓库
# 仓库名：scoop-bucket
# 类型：Public
# 不要初始化 README

# 本地初始化
mkdir scoop-bucket
cd scoop-bucket

# 复制 manifest
cp ../AI-CLI/ai-cli.json ./

# 创建 README
cat > README.md << 'EOF'
# Scoop Bucket for AI-CLI

AI CLI Launcher - Unified terminal launcher for AI coding tools.

## Installation

```powershell
scoop bucket add ai-cli https://github.com/hyfhot/scoop-bucket
scoop install ai-cli
```

## Usage

```powershell
ai-cli          # Start interactive launcher
ai-cli --help   # Show help
```

## Links

- [GitHub](https://github.com/hyfhot/AI-CLI)
- [Documentation](https://github.com/hyfhot/AI-CLI#readme)
EOF

# 提交并推送
git init
git add .
git commit -m "Initial commit: Add ai-cli manifest"
git branch -M main
git remote add origin https://github.com/hyfhot/scoop-bucket.git
git push -u origin main
```

### 4. 测试自动更新

```bash
# 在 AI-CLI 仓库创建新 Release
cd AI-CLI

# 更新版本号（如果需要）
# 编辑 ai-cli.ps1，修改 Version: 2.3

# 提交并创建 tag
git add .
git commit -m "Release v2.3.0"
git tag -a v2.3.0 -m "Release v2.3.0"
git push origin main
git push origin v2.3.0

# 在 GitHub 网页创建 Release
# 访问：https://github.com/hyfhot/AI-CLI/releases/new
# - Tag: v2.3.0
# - Title: v2.3.0
# - Description: 更新说明
# - 点击 "Publish release"

# GitHub Action 会自动：
# 1. 下载新版本压缩包
# 2. 计算 SHA256
# 3. 更新 scoop-bucket/ai-cli.json
# 4. 提交并推送
```

### 5. 查看 Action 运行状态

访问：https://github.com/hyfhot/AI-CLI/actions

如果失败，检查：
- SCOOP_TOKEN 是否正确设置
- Token 权限是否足够
- scoop-bucket 仓库是否存在

## 手动更新（备用方案）

如果 Action 失败，可以手动更新：

```bash
# 下载新版本
VERSION="2.3.0"
curl -L -o release.zip "https://github.com/hyfhot/AI-CLI/archive/refs/tags/v${VERSION}.zip"

# 计算 hash
sha256sum release.zip

# 更新 scoop-bucket
cd scoop-bucket
# 编辑 ai-cli.json，更新 version 和 hash
git add ai-cli.json
git commit -m "Update ai-cli to v${VERSION}"
git push
```

## 用户安装方式

```powershell
# 添加 bucket
scoop bucket add ai-cli https://github.com/hyfhot/scoop-bucket

# 安装
scoop install ai-cli

# 更新
scoop update ai-cli

# 卸载
scoop uninstall ai-cli
```
