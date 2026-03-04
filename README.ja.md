# AI-CLI (Python エディション)

> 🌐 [English](README.md) | [中文](README.zh.md) | **日本語** | [Deutsch](README.de.md)

[![Python バージョン](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![ライセンス](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![ステータス](https://img.shields.io/badge/status-beta-yellow.svg)](https://github.com/hyfhot/AI-CLI)

**AI-CLI** は、複数の AI コーディングアシスタントを管理するためのクロスプラットフォームターミナルランチャーです。Kiro CLI、Claude Code、Cursor Agent などのツールをシームレスに切り替えます。

## ✨ コア機能

### 🌍 クロスプラットフォームサポート
- **Windows**: ネイティブサポート + WSL 統合 ✅ 完全にテスト済み
- **Linux**: すべての主要ディストリビューションを完全サポート ⚠️ **テスト未完了 - 問題が発生する可能性があります**
- **macOS**: Terminal.app と iTerm2 をサポート ⚠️ **テスト未完了 - 問題が発生する可能性があります**

### 🔄 深い WSL 統合
- WSL 環境の自動検出
- Windows ↔ WSL パスの自動変換
- Windows から WSL ツールを起動
- WSL から Windows ツールを起動

### 📁 プロジェクト管理
- **ツリー構造**: フォルダでプロジェクトを整理
- **Git Worktree**: Git worktree の自動検出と選択
- **環境変数**: プロジェクトごとの環境変数設定
- **パス正規化**: 異なるプラットフォームのパス形式を自動処理

### ⚡ ツール検出と管理
- **非同期検出**: async/await を使用した並列ツール検出
- **スマートキャッシング**: バックグラウンド検出と結果のキャッシング
- **ワンクリックインストール**: `I` キーを押して不足しているツールをインストール
- **手動更新**: `R` キーを押してツールリストを更新
- **環境認識**: Windows、WSL、Linux、macOS 環境を自動検出

### 🎨 ユーザーインターフェース
- **Rich UI**: Rich ライブラリによる美しいターミナルインターフェース
- **キーボードナビゲーション**: 完全なキーボードショートカットサポート
- **リアルタイムフィードバック**: ツール検出とインストールの進行状況を表示
- **テーマサポート**: カスタマイズ可能なカラーテーマ

### 🌐 国際化
- **多言語対応**: 英語、中国語、日本語、ドイツ語
- **自動検出**: システム言語に基づいて自動選択
- **設定可能**: 設定ファイルで言語を手動指定

## 🚀 クイックスタート

### インストール

#### 方法 1: PyPI からインストール（推奨）

```bash
# pip を使用
pip install ai-cli-launcher

# または pipx を使用（分離環境）
pipx install ai-cli-launcher
```

#### 方法 2: ワンラインインストールスクリプト

**Windows**:
```powershell
irm https://raw.githubusercontent.com/hyfhot/AI-CLI/master/install.ps1 | iex
```

**Linux/macOS**:
```bash
curl -fsSL https://raw.githubusercontent.com/hyfhot/AI-CLI/master/install.sh | bash
```

スクリプトは自動的に以下を実行します：
- Python のインストール確認（Python 3.8+ が必要）
- PyPI から AI-CLI をインストール
- 設定ファイルの初期化
- デスクトップショートカットの作成（Windows）

#### 方法 3: ソースからインストール（開発者向け）

```bash
# リポジトリをクローン
git clone https://github.com/hyfhot/AI-CLI.git
cd AI-CLI

# 開発モードでインストール
pip install -e ".[dev]"
```

### 設定の初期化

```bash
ai-cli --init
```

これにより、一般的な AI ツールの設定を含むデフォルトの設定ファイルが作成されます。

### 実行

```bash
ai-cli
```

### アンインストール

**完全アンインストール（推奨）**：

Windows (PowerShell)：
```powershell
ai-cli --uninstall; pip uninstall ai-cli-launcher
```

Linux/macOS：
```bash
ai-cli --uninstall && pip uninstall ai-cli-launcher
```

**段階的アンインストール**：
```bash
# ステップ 1: ショートカットをクリーンアップし、設定ファイルの場所を表示
ai-cli --uninstall

# ステップ 2: パッケージをアンインストール
pip uninstall ai-cli-launcher
```

**クイックアンインストール**：
```bash
# パッケージのみをアンインストール（ショートカットは残ります）
pip uninstall ai-cli-launcher
```

**手動クリーンアップ**（必要な場合）：
- Windows: `%APPDATA%\AI-CLI\` とデスクトップショートカットを削除
- Linux: `~/.config/ai-cli/` を削除
- macOS: `~/Library/Application Support/ai-cli/` を削除

### 実行

```bash
ai-cli
```

## 📖 使用方法

### コマンドラインオプション

```bash
ai-cli                    # インタラクティブインターフェースを起動
ai-cli --init             # 設定ファイルを初期化
ai-cli --config           # 設定ファイルを編集
ai-cli --lang zh          # 中国語で起動
ai-cli --lang ja          # 日本語で起動
ai-cli --uninstall        # AI-CLI をアンインストール
ai-cli --version          # バージョン情報を表示
ai-cli --help             # ヘルプ情報を表示
```

**言語オプション** (`--lang` / `-l`):
- `auto` - システム言語を自動検出（デフォルト）
- `en` - 英語 (English)
- `zh` - 中国語 (中文)
- `ja` - 日本語
- `de` - ドイツ語 (Deutsch)

**注意**: CLI言語パラメータは設定ファイルの設定より優先されます。

### キーボードショートカット

#### プロジェクト選択画面

| キー | 機能 |
|------|------|
| `↑` / `↓` | 上下に移動 |
| `Enter` | プロジェクトを選択 / フォルダに入る |
| `Esc` | 親フォルダに戻る |
| `N` | 新しいプロジェクトまたはフォルダを作成 |
| `D` | 選択したプロジェクトまたはフォルダを削除 |
| `Q` | アプリケーションを終了 |

#### ツール選択画面

| キー | 機能 |
|------|------|
| `↑` / `↓` | 上下に移動 |
| `Enter` | ツールを起動（新しいウィンドウ） |
| `Ctrl+Enter` | ツールを起動（新しいタブ） |
| `I` | 不足しているツールをインストール |
| `R` | ツールリストを更新 |
| `Esc` | プロジェクト選択に戻る |
| `Q` | アプリケーションを終了 |

### ワークフロー

1. **起動**: `ai-cli` を実行
2. **プロジェクトを選択**: 矢印キーでプロジェクトを選択し、`Enter` で確定
3. **ツールを選択**: 使用する AI ツールを選択
4. **作業開始**: ツールが新しいウィンドウまたはタブで起動

## 🔧 設定ガイド

### 設定ファイルの場所

- **Windows**: `%APPDATA%\AI-CLI\config.json`
- **Linux**: `~/.config/ai-cli/config.json`
- **macOS**: `~/Library/Application Support/ai-cli/config.json`

### 設定ファイルの構造

```json
{
  "projects": [
    {
      "type": "folder",
      "name": "マイプロジェクト",
      "children": [
        {
          "type": "project",
          "name": "Web アプリ",
          "path": "/path/to/project",
          "env": {
            "API_KEY": "your-api-key",
            "DEBUG": "true"
          }
        }
      ]
    }
  ],
  "tools": [
    {
      "name": "kiro-cli",
      "displayName": "Kiro CLI",
      "windowsInstall": "winget install kiro-cli",
      "wslInstall": "curl -fsSL https://cli.kiro.dev/install | bash",
      "linuxInstall": "curl -fsSL https://cli.kiro.dev/install | bash",
      "macosInstall": "brew install kiro-cli",
      "checkCommand": "kiro-cli --version",
      "url": "https://kiro.dev/cli/"
    }
  ],
  "settings": {
    "language": "auto",
    "terminalEmulator": "default",
    "theme": "default"
  }
}
```

### プロジェクト設定

#### プロジェクトタイプ

**フォルダ**:
```json
{
  "type": "folder",
  "name": "プロジェクトグループ名",
  "children": [...]
}
```

**プロジェクト**:
```json
{
  "type": "project",
  "name": "プロジェクト名",
  "path": "/absolute/path/to/project",
  "env": {
    "KEY": "value"
  }
}
```

#### 環境変数

各プロジェクトに独立した環境変数を設定：

```json
{
  "type": "project",
  "name": "API プロジェクト",
  "path": "/path/to/api",
  "env": {
    "API_KEY": "sk-xxx",
    "API_BASE_URL": "https://api.example.com",
    "DEBUG": "true",
    "LOG_LEVEL": "info"
  }
}
```

### ツール設定

#### 必須フィールド

- `name`: ツールのコマンド名（検出に使用）
- `displayName`: 表示名
- `checkCommand`: ツールがインストールされているかチェックするコマンド

#### インストールコマンド（プラットフォーム別）

- `windowsInstall`: Windows ネイティブインストールコマンド
- `wslInstall`: WSL 環境インストールコマンド
- `linuxInstall`: Linux インストールコマンド
- `macosInstall`: macOS インストールコマンド

#### オプションフィールド

- `url`: ツールの公式ウェブサイト（ツールリストに表示）

#### 設定例

```json
{
  "name": "cursor",
  "displayName": "Cursor Agent",
  "windowsInstall": "winget install Cursor",
  "wslInstall": "curl -fsSL https://cursor.sh/install | bash",
  "linuxInstall": "curl -fsSL https://cursor.sh/install | bash",
  "macosInstall": "brew install --cask cursor",
  "checkCommand": "cursor --version",
  "url": "https://cursor.sh"
}
```

### 設定オプション

#### language（言語）

- `auto`: システム言語を自動検出（デフォルト）
- `en`: 英語
- `zh`: 中国語
- `ja`: 日本語
- `de`: ドイツ語

#### terminalEmulator（ターミナルエミュレータ）

- `default`: システムデフォルトターミナルを使用（デフォルト）
- `wt`: Windows Terminal（Windows のみ）
- `iterm`: iTerm2（macOS のみ）
- `gnome-terminal`: GNOME Terminal（Linux のみ）
- `konsole`: Konsole（Linux のみ）

#### theme（テーマ）

- `default`: デフォルトダークテーマ
- 将来のバージョンでより多くのテーマをサポート予定

## 🏗️ プロジェクトアーキテクチャ

### ディレクトリ構造

```
ai_cli/
├── __init__.py        # パッケージ初期化
├── cli.py             # CLI エントリーポイント
├── app.py             # メインアプリケーションロジック
├── models.py          # データモデル
├── config.py          # 設定管理
├── utils.py           # パス変換ユーティリティ
├── core/              # コア機能モジュール
│   ├── __init__.py
│   ├── tools.py       # ツール検出
│   ├── projects.py    # プロジェクト管理
│   ├── git.py         # Git 統合
│   └── installer.py   # ツールインストール
├── ui/                # ユーザーインターフェースモジュール
│   ├── __init__.py
│   ├── theme.py       # テーマ設定
│   ├── menu.py        # メニューレンダリング
│   └── input.py       # キーボード入力処理
├── platform/          # プラットフォームアダプターモジュール
│   ├── __init__.py
│   ├── base.py        # 抽象基底クラス
│   ├── windows.py     # Windows アダプター
│   ├── linux.py       # Linux アダプター
│   ├── macos.py       # macOS アダプター
│   └── factory.py     # プラットフォームファクトリー
└── i18n/              # 国際化モジュール
    ├── __init__.py
    └── manager.py     # 言語マネージャー
```

### コアモジュールの説明

#### models.py - データモデル

すべてのデータ構造を定義：
- `Config`: メイン設定オブジェクト
- `Settings`: 設定オプション
- `ProjectNode`: プロジェクトノード（ツリー構造をサポート）
- `Tool`: ツールオブジェクト
- `ToolConfig`: ツール設定
- `ToolEnvironment`: ツール実行環境列挙型

#### config.py - 設定管理

- クロスプラットフォーム設定ファイルパス処理
- 設定ファイルの読み込みと保存
- レガシー設定バージョンからの移行
- デフォルト設定の作成

#### app.py - メインアプリケーション

- アプリケーションメインループ
- プロジェクト選択ロジック
- ツール選択ロジック
- ツール起動ロジック
- プロジェクトとフォルダの CRUD 操作

#### core/tools.py - ツール検出

- 非同期並列ツール検出
- プラットフォーム固有の検出ロジック
- Windows ネイティブツール検出
- WSL ツール検出
- ツールキャッシュ管理

#### core/git.py - Git 統合

- Git worktree の検出
- ブランチステータスの表示
- インタラクティブな worktree 選択

#### core/installer.py - ツールインストール

- プラットフォームごとのインストールコマンド選択
- インストールプロセスの実行
- インストール後のパス更新
- インストール済みツールの検索

#### ui/menu.py - メニューレンダリング

- プロジェクトツリーのレンダリング
- ツールリストのレンダリング
- パンくずナビゲーションの表示
- 画面クリアと更新

#### ui/input.py - キーボード入力

- クロスプラットフォームキーボード入力処理
- Windows と Unix システムの異なる実装
- テキスト入力サポート
- 特殊キー処理

#### platform/ - プラットフォームアダプター

- 抽象プラットフォームインターフェース
- Windows 固有の実装（Windows Terminal サポート）
- Linux 固有の実装（複数のターミナルサポート）
- macOS 固有の実装（iTerm2 サポート）
- プラットフォームファクトリーパターン

#### i18n/manager.py - 国際化

- 言語検出
- 翻訳辞書管理
- テキスト取得インターフェース

## 🔍 高度な機能

### Git Worktree サポート

プロジェクトパスが Git worktree の場合、AI-CLI は：

1. すべての worktree を自動検出
2. 各 worktree のブランチとステータスを表示
3. 使用する worktree の選択を許可
4. ブランチの先行/遅延コミット数を表示

### WSL パス変換

AI-CLI は Windows と WSL 間のパス変換を自動処理：

- Windows パス: `C:\Users\username\project`
- WSL パス: `/mnt/c/Users/username/project`

変換は双方向で、以下をサポート：
- Windows から WSL ツールを起動
- WSL から Windows ツールを起動

### 非同期ツール検出

ツール検出は非同期並列処理を使用：

1. **起動時**: インターフェースを素早く表示し、バックグラウンドでツールを検出
2. **キャッシング**: 検出結果をキャッシュして繰り返しチェックを回避
3. **更新**: `R` キーを押してキャッシュをクリアして再検出

### 環境変数インジェクション

各プロジェクトに設定された環境変数は、ツール起動時に注入されます：

```json
{
  "type": "project",
  "name": "API プロジェクト",
  "path": "/path/to/api",
  "env": {
    "API_KEY": "sk-xxx",
    "DEBUG": "true"
  }
}
```

ツールを起動すると、これらの環境変数がツールの実行環境に追加されます。

## 🧪 テスト

### テストの実行

```bash
# すべてのテストを実行
pytest

# 特定のテストファイルを実行
pytest tests/test_models.py

# 特定のテストを実行
pytest tests/test_models.py::TestConfig::test_from_dict

# 詳細出力を表示
pytest -v

# 印刷出力を表示
pytest -s
```

### テストカバレッジ

```bash
# カバレッジレポート付きでテストを実行
pytest --cov=ai_cli

# HTML カバレッジレポートを生成
pytest --cov=ai_cli --cov-report=html

# レポートを表示
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### テストファイルの説明

- `test_models.py`: データモデルテスト
- `test_config.py`: 設定管理テスト
- `test_utils.py`: パス変換テスト
- `test_platform.py`: プラットフォームアダプターテスト
- `test_git.py`: Git 統合テスト
- `test_tools.py`: ツール検出テスト
- `test_projects.py`: プロジェクト管理テスト
- `test_ui.py`: UI コンポーネントテスト
- `test_app.py`: アプリケーション統合テスト
- `test_cli.py`: CLI エントリーポイントテスト

## 📝 開発ガイド

### 要件

- **Python**: 3.8 以上
- **依存関係**:
  - `rich`: ターミナル UI レンダリング
  - `prompt-toolkit`: キーボード入力処理
  - `click`: CLI フレームワーク
  - `platformdirs`: クロスプラットフォームパス

### 開発環境のセットアップ

```bash
# 1. リポジトリをクローン
git clone https://github.com/hyfhot/AI-CLI.git
cd AI-CLI

# 2. Python バージョンの worktree を作成（必要な場合）
git worktree add ../ai-cli-multi-platform python-migration
cd ../ai-cli-multi-platform

# 3. 仮想環境を作成（推奨）
python -m venv venv

# 仮想環境をアクティブ化
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 4. 開発依存関係をインストール
pip install -e ".[dev]"

# 5. テストを実行して環境を確認
pytest
```

### コードスタイル

プロジェクトは PEP 8 スタイルガイドに従います：

```bash
# コードチェックツールをインストール
pip install flake8 black mypy

# コードチェックを実行
flake8 ai_cli tests

# コードを自動フォーマット
black ai_cli tests

# 型チェック
mypy ai_cli
```

### 新しいツールの追加

`config.json` に新しいツール設定を追加：

```json
{
  "name": "new-tool",
  "displayName": "New Tool",
  "windowsInstall": "winget install new-tool",
  "wslInstall": "curl -fsSL https://example.com/install | bash",
  "linuxInstall": "curl -fsSL https://example.com/install | bash",
  "macosInstall": "brew install new-tool",
  "checkCommand": "new-tool --version",
  "url": "https://example.com"
}
```

### 新しい言語の追加

`ai_cli/i18n/manager.py` に翻訳を追加：

```python
translations = {
    'new_lang': {
        'app_title': 'AI-CLI',
        'select_project': 'Select Project',
        # ... その他の翻訳
    }
}
```

### デバッグのヒント

```bash
# デバッグモードを有効化
ai-cli --debug

# Python デバッガーを使用
python -m pdb -m ai_cli.cli

# 詳細ログを表示
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🐛 トラブルシューティング

### Windows の問題

**問題**: Windows Terminal を検出できない
```bash
# 解決策: Windows Terminal がインストールされていることを確認
winget install Microsoft.WindowsTerminal
```

**問題**: WSL ツール検出が失敗
```bash
# 解決策: WSL が有効になっていることを確認
wsl --install
```

### Linux の問題

**問題**: ターミナルエミュレータ検出が失敗
```bash
# 解決策: サポートされているターミナルをインストール
sudo apt install gnome-terminal  # Ubuntu/Debian
sudo dnf install gnome-terminal  # Fedora
```

### macOS の問題

**問題**: iTerm2 が検出されない
```bash
# 解決策: iTerm2 がインストールされていることを確認
brew install --cask iterm2
```

### 一般的な問題

**問題**: 設定ファイルが破損
```bash
# 解決策: 設定を再初期化
ai-cli --init
```

**問題**: ツール検出キャッシュが古い
```bash
# 解決策: ツール選択画面で R キーを押して更新
```

## 🤝 貢献

あらゆる形式の貢献を歓迎します！

### 貢献方法

1. **バグ報告**: [GitHub Issues](https://github.com/hyfhot/AI-CLI/issues) で問題を報告
2. **機能リクエスト**: 新機能のアイデアを提案
3. **コード貢献**: Pull Request を送信
4. **ドキュメント**: ドキュメントと例を改善
5. **翻訳**: 新しい言語サポートを追加

### Pull Request プロセス

1. プロジェクトをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/AmazingFeature`)
3. 変更をコミット (`git commit -m 'Add some AmazingFeature'`)
4. ブランチにプッシュ (`git push origin feature/AmazingFeature`)
5. Pull Request を開く

### コミット規約

[Conventional Commits](https://www.conventionalcommits.org/) に従う：

```
feat: 新機能を追加
fix: バグを修正
docs: ドキュメント更新
style: コードフォーマット
refactor: コードリファクタリング
test: テスト関連
chore: ビルド/ツールチェーン更新
```

## 📄 ライセンス

このプロジェクトは MIT ライセンスの下でライセンスされています - 詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 🔗 関連リンク

- **オリジナルプロジェクト**: [AI-CLI (PowerShell エディション)](https://github.com/hyfhot/AI-CLI)
- **ドキュメント**: [docs/](docs/)
- **問題トラッカー**: [GitHub Issues](https://github.com/hyfhot/AI-CLI/issues)
- **変更履歴**: [CHANGELOG.md](CHANGELOG.md)

## 🙏 謝辞

これらのオープンソースプロジェクトに感謝：

- [Rich](https://github.com/Textualize/rich) - 強力なターミナル UI ライブラリ
- [Prompt Toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit) - インタラクティブコマンドラインツール
- [Click](https://github.com/pallets/click) - Python CLI フレームワーク
- [platformdirs](https://github.com/platformdirs/platformdirs) - クロスプラットフォームディレクトリパス

## 📊 プロジェクトステータス

- **バージョン**: Beta
- **Python バージョン**: 3.8+
- **プラットフォーム**: Windows, Linux, macOS
- **メンテナンス**: 活発に開発中

## 🗺️ ロードマップ

- [ ] より多くの AI ツールをサポート
- [ ] プラグインシステム
- [ ] 設定ファイル検証
- [ ] より多くのテーマオプション
- [ ] ツール使用統計
- [ ] クラウド設定同期
- [ ] プロジェクトテンプレートサポート

---

**AI-CLI チームが ❤️ を込めて作成**
