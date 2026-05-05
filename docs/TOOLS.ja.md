# AI CLI ツールリファレンス

> 🌐 [English](TOOLS.md) | [中文](TOOLS.zh.md) | **日本語** | [Deutsch](TOOLS.de.md)

このドキュメントは、AI-CLI がサポートする主流の AI プログラミングツールとそのインストールおよび設定情報をリストしています。

---

## 🤖 サポートされているツールリスト

### 1. Kiro CLI (AWS)
- **公式ウェブサイト**: https://kiro.dev/cli/
- **開発者**: Amazon Web Services
- **機能**:
  - 仕様駆動開発プラットフォーム
  - エージェントワークフローをサポート
  - AWS サービス統合
  - モデルコンテキストプロトコル (MCP) をサポート
- **インストール**:
  - **Linux/macOS/WSL**: `curl -fsSL https://cli.kiro.dev/install | bash`
  - **Windows**: `irm 'https://cli.kiro.dev/install.ps1' | iex`
- **検証**: `kiro-cli --version`

---

### 2. Claude Code (Anthropic)
- **公式ウェブサイト**: https://www.npmjs.com/package/@anthropic-ai/claude-code
- **開発者**: Anthropic
- **機能**:
  - エージェントコーディングアシスタント
  - 自然言語コード生成
  - コンテキスト対応の提案
- **インストール**:
  - **すべてのプラットフォーム**: `npm install -g @anthropic-ai/claude-code`
- **検証**: `claude-code --version`

---

### 3. Cursor Agent
- **公式ウェブサイト**: https://cursor.sh
- **開発者**: Cursor チーム
- **機能**:
  - AI 駆動のコードエディタ
  - インラインコード提案
  - チャットベースのコーディング支援
- **インストール**:
  - **Windows**: `winget install Cursor`
  - **macOS**: `brew install --cask cursor`
  - **Linux**: 公式ウェブサイトからダウンロード
- **検証**: `cursor --version`

---

### 4. GitHub Copilot CLI
- **公式ウェブサイト**: https://githubnext.com/projects/copilot-cli
- **開発者**: GitHub
- **機能**:
  - コマンドライン AI アシスタント
  - シェルコマンド提案
  - Git ワークフロー支援
- **インストール**:
  - **すべてのプラットフォーム**: `npm install -g @githubnext/github-copilot-cli`
- **検証**: `github-copilot-cli --version`

---

### 5. Aider
- **公式ウェブサイト**: https://aider.chat
- **開発者**: Aider チーム
- **機能**:
  - ターミナルでの AI ペアプログラミング
  - Git 統合
  - 複数の LLM をサポート
- **インストール**:
  - **すべてのプラットフォーム**: `pip install aider-chat`
- **検証**: `aider --version`

---

### 6. DeepSeek TUI
- **公式ウェブサイト**: https://github.com/Hmbown/DeepSeek-TUI
- **開発者**: Hunter Bown
- **機能**:
  - DeepSeek V4 に最適化されたターミナルネイティブ AI コーディングエージェント
  - 100 万トークンのコンテキストウィンドウをサポート
  - リアルタイムの Chain-of-Thought ストリーミング
  - RLM 並列推論（1-16 の同時タスク）
  - 3 つの作業モード：Plan / Agent / YOLO
  - 内蔵 LSP 診断機能
  - MCP サーバーサポート
  - 拡張用 Skills システム
- **インストール**:
  - **すべてのプラットフォーム**: `npm install -g deepseek-tui`
- **検証**: `deepseek --version`

---

## 📝 設定例

`config.json` にツールを追加：

```json
{
  "tools": [
    {
      "name": "kiro-cli",
      "displayName": "Kiro CLI",
      "windowsInstall": "irm 'https://cli.kiro.dev/install.ps1' | iex",
      "wslInstall": "curl -fsSL https://cli.kiro.dev/install | bash",
      "linuxInstall": "curl -fsSL https://cli.kiro.dev/install | bash",
      "macosInstall": "brew install kiro-cli",
      "checkCommand": "kiro-cli --version",
      "url": "https://kiro.dev/cli/"
    },
    {
      "name": "cursor",
      "displayName": "Cursor Agent",
      "windowsInstall": "winget install Cursor",
      "wslInstall": "curl -fsSL https://cursor.sh/install | bash",
      "linuxInstall": "curl -fsSL https://cursor.sh/install | bash",
      "macosInstall": "brew install --cask cursor",
      "checkCommand": "cursor --version",
      "url": "https://cursor.sh"
    },
    {
      "name": "aider",
      "displayName": "Aider",
      "windowsInstall": "pip install aider-chat",
      "wslInstall": "pip install aider-chat",
      "linuxInstall": "pip install aider-chat",
      "macosInstall": "pip install aider-chat",
      "checkCommand": "aider --version",
      "url": "https://aider.chat"
    }
  ]
}
```

---

## 🔧 カスタムツールの追加

新しいツールを追加する手順：

1. **インストールコマンドを見つける** - 各プラットフォームのインストールコマンドを見つける
2. **チェックコマンドを決定** - インストールを検証するコマンド
3. **config.json に追加** - 上記の形式に従って追加

### 必須フィールド

- `name`: コマンド名（検出に使用）
- `displayName`: UI での表示名
- `checkCommand`: インストールを検証するコマンド

### プラットフォーム固有のインストールコマンド

- `windowsInstall`: Windows ネイティブインストール
- `wslInstall`: WSL 環境インストール
- `linuxInstall`: Linux インストール
- `macosInstall`: macOS インストール

### オプションフィールド

- `url`: 公式ウェブサイト（ツールリストに表示）

---

## 💡 ヒント

1. **可能な限りパッケージマネージャーを使用**（winget、brew、apt など）
2. **チェックコマンドをテスト** して正しく動作することを確認
3. **URL を最新に保つ** ユーザー参照用
4. **前提条件を文書化** ツールが特定の依存関係を必要とする場合

---

詳細については、[メイン README](../README.ja.md) を参照してください。
