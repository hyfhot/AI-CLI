🌐 [English](SCOOP-PUBLISH.md) | [中文](SCOOP-PUBLISH.zh.md) | [日本語](SCOOP-PUBLISH.ja.md)

# Scoop への公開チュートリアル

## オプション 1: 公式 Scoop Bucket への公開（推奨だが審査は厳しい）

### 1. 準備

**GitHub Release の作成:**
```bash
# 1. コードがコミットされていることを確認
git add .
git commit -m "Release v2.2.0"
git push

# 2. タグの作成とプッシュ
git tag -a v2.2.0 -m "Release version 2.2.0"
git push origin v2.2.0

# 3. GitHub Web ページで Release を作成
# URL: https://github.com/hyfhot/AI-CLI/releases/new
# - Tag: v2.2.0
# - Title: AI-CLI v2.2.0
# - Description: バージョンアップデートノートを追加
# - 「Publish release」をクリック
```

**ファイルハッシュの計算:**
```powershell
# リリースアーカイブのダウンロード
$url = "https://github.com/hyfhot/AI-CLI/archive/refs/tags/v2.2.0.zip"
Invoke-WebRequest -Uri $url -OutFile "ai-cli-v2.2.0.zip"

# SHA256 の計算
Get-FileHash "ai-cli-v2.2.0.zip" -Algorithm SHA256 | Select-Object -ExpandProperty Hash
```

**manifest の hash フィールドを更新:**
```json
{
    "hash": "計算された SHA256 値"
}
```

### 2. 公式 Bucket へのサブミット

```bash
# Scoop 公式 bucket をフォーク
# URL: https://github.com/ScoopInstaller/Main
# 右上の「Fork」をクリック

# 自分のフォークをクローン
git clone https://github.com/あなたのユーザー名/Main.git scoop-main
cd scoop-main

# 新しいブランチを作成
git checkout -b add-ai-cli

# manifest をコピー
cp /path/to/ai-cli.json bucket/ai-cli.json

# コミット
git add bucket/ai-cli.json
git commit -m "Add ai-cli: AI CLI Launcher for coding tools"
git push origin add-ai-cli

# GitHub で Pull Request を作成
# 自分のフォークページにアクセスし、「Compare & pull request」をクリック
```

**注意:** 公式 bucket は審査が厳しく、以下が必要となる場合があります:
- ツールにある程度の知名度がある
- コード品質が高い
- ドキュメントが整備されている
- 数日から数週間の待機が必要な場合がある

---

## オプション 2: 独自の Bucket 作成（推奨、迅速に公開）

### 1. Bucket リポジトリの作成

```bash
# GitHub で新しいリポジトリを作成
# リポジトリ名：scoop-bucket（または任意の名前）
# 説明：Scoop bucket for AI-CLI
# Public リポジトリ

# ローカルにクローン
git clone https://github.com/hyfhot/scoop-bucket.git
cd scoop-bucket

# manifest をコピー
cp /path/to/ai-cli.json ./ai-cli.json

# README を作成
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

# コミットしてプッシュ
git add .
git commit -m "Initial commit: Add ai-cli manifest"
git push origin main
```

### 2. ユーザーのインストール方法

ユーザーが実行する必要があるのは:
```powershell
# あなたの bucket を追加
scoop bucket add ai-cli https://github.com/hyfhot/scoop-bucket

# インストール
scoop install ai-cli

# 使用
ai-cli
```

### 3. バージョンの更新

```bash
# 1. メインプロジェクトを更新し、新しいタグを作成
cd AI-CLI
git tag v2.3.0
git push origin v2.3.0

# 2. bucket 内の manifest を更新
cd scoop-bucket
# ai-cli.json を編集し、version と hash を更新
git add ai-cli.json
git commit -m "Update ai-cli to v2.3.0"
git push

# ユーザーの更新
scoop update ai-cli
```

---

## オプション 3: コミュニティ Bucket へのサブミット（折衷案）

Scoop にはコミュニティによって管理されている bucket があり、審査は比較的緩やかです:

### Extras Bucket（推奨）
GUI ツールや非メインストリームの CLI ツールに適しています:

```bash
# https://github.com/ScoopInstaller/Extras をフォーク
git clone https://github.com/あなたのユーザー名/Extras.git
cd Extras

git checkout -b add-ai-cli
cp /path/to/ai-cli.json bucket/ai-cli.json

git add bucket/ai-cli.json
git commit -m "ai-cli: Add AI CLI Launcher"
git push origin add-ai-cli

# ScoopInstaller/Extras に PR を作成
```

---

## Manifest のテスト

公開前にローカルでテスト:

```powershell
# 方法 1: ローカルから直接インストール
scoop install /path/to/ai-cli.json

# 方法 2: URL からインストール
scoop install https://raw.githubusercontent.com/hyfhot/scoop-bucket/main/ai-cli.json

# アンインストールのテスト
scoop uninstall ai-cli

# アップデートのテスト
scoop update ai-cli
```

---

## 推奨プロセス

**フェーズ 1（すぐに実施可能）:**
1. 独自の bucket を作成（オプション 2）
2. README.md に Scoop インストール手順を追加
3. ユーザーがすぐに使用可能

**フェーズ 2（プロジェクトが成熟した後）:**
1. Extras bucket にサブミット（オプション 3）
2. より多くの露出を得る

**フェーズ 3（オプション）:**
1. ツールが十分に人気がある場合、Main bucket にサブミット（オプション 1）

---

## README にインストール手順を追加

あなたの `README.md` に以下を追加:

```markdown
### Scoop でインストール（推奨）

```powershell
# bucket を追加
scoop bucket add ai-cli https://github.com/hyfhot/scoop-bucket

# インストール
scoop install ai-cli

# 使用
ai-cli
```

### インストールスクリプトでインストール

```powershell
irm https://raw.githubusercontent.com/hyfhot/AI-CLI/master/install.ps1 | iex
```
```

---

## 自動更新（オプション）

GitHub Action を作成してハッシュを自動更新:

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

どのステップを実行する必要がありますか？
