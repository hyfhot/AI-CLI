# AI-CLI インストールガイド

> 🌐 [English](INSTALL-GUIDE.md) | [中文](INSTALL-GUIDE.zh.md) | **日本語**

## クイックインストール

### インストールスクリプトを使用（推奨）

**Windows**:
```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

**Linux/macOS**:
```bash
bash install.sh
```

### 手動インストール

```bash
# リポジトリをクローン
git clone https://github.com/hyfhot/AI-CLI.git
cd AI-CLI

# Git worktree を使用する場合
git worktree add ../ai-cli-multi-platform python-migration
cd ../ai-cli-multi-platform

# 依存関係をインストール
pip install -e ".[dev]"
```

## ツールインストール機能

ツール選択画面で `I` キーを押すと、まだインストールされていない AI CLI ツールを素早くインストールできます。

### 使用手順

1. **AI-CLI を起動**
   ```bash
   ai-cli
   ```

2. **プロジェクトを選択**
   - ↑↓ キーでプロジェクトを選択
   - Enter で確定

3. **I キーを押してインストール画面に入る**
   - ツール選択画面で `I` キーを押す
   - インストールツールリストが開く

4. **インストールするツールを選択**
   - リストには、インストールされていないがインストールコマンドが設定されているすべてのツールが表示される
   - `[Windows]`、`[WSL]`、`[Linux]`、または `[macOS]` はインストール環境を示す
   - ↑↓ キーで選択
   - Enter でインストールを確定
   - Esc でツール選択画面に戻る

5. **インストール完了を待つ**
   - 画面にインストールコマンドと実行プロセスが表示される
   - インストール完了後、任意のキーを押して戻る

## 設定

### 設定の初期化

```bash
ai-cli --init
```

これにより、以下の場所にデフォルトの設定ファイルが作成されます：
- **Windows**: `%APPDATA%\AI-CLI\config.json`
- **Linux**: `~/.config/ai-cli/config.json`
- **macOS**: `~/Library/Application Support/ai-cli/config.json`

### 設定の編集

```bash
ai-cli --config
```

または、お好みのテキストエディタで設定ファイルを手動で編集します。

## トラブルシューティング

### Python バージョンの問題

**問題**: コマンドが見つからない、またはインポートエラー

**解決策**: Python 3.8+ がインストールされていることを確認
```bash
python --version  # 3.8 以上である必要がある
```

### 権限の問題

**問題**: インストール中に権限が拒否される

**解決策**: 
- Linux/macOS: 必要に応じて `sudo` を使用
- Windows: 管理者として実行

### パスの問題

**問題**: インストール後に `ai-cli` コマンドが見つからない

**解決策**: 
- pip インストールディレクトリが PATH に含まれていることを確認
- 代わりに `python -m ai_cli.cli` を使用してみる

### WSL の問題

**問題**: WSL ツールが検出されない

**解決策**: 
- WSL がインストールされていることを確認: `wsl --install`
- WSL がアクセス可能か確認: `wsl --list`

## アンインストール

```bash
ai-cli --uninstall
```

これにより：
- 設定ディレクトリを削除
- Python パッケージをアンインストール
- すべての一時ファイルをクリーンアップ

---

詳細については、[メイン README](../README.ja.md) を参照してください。
