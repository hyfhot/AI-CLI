🌐 [English](TOOLS.md) | [中文](TOOLS.zh.md) | [日本語](TOOLS.ja.md)

# AI CLI ツールリファレンス

このドキュメントでは、AI-CLI がサポートする主要な AI プログラミングツールと、そのインストールおよび設定情報をリストしています。

---

## 🤖 サポートされるツール一覧

### 1. Kiro CLI (AWS)
- **公式ウェブサイト**: https://kiro.dev/cli/
- **開発元**: Amazon Web Services
- **特徴**:
  - 仕様駆動型開発プラットフォーム
  - エージェントワークフローをサポート
  - AWS サービスと統合
  - Model Context Protocol (MCP) をサポート
- **インストールコマンド**:
  - WSL/Linux: `curl -fsSL https://cli.kiro.dev/install | bash`
  - Windows: ネイティブインストールはサポートされていません
- **確認方法**: `kiro-cli --version`

---

### 2. Claude Code (Anthropic)
- **公式ウェブサイト**: https://www.npmjs.com/package/@anthropic-ai/claude-code
- **開発元**: Anthropic
- **特徴**:
  - エージェント型コーディングアシスタント
  - 100K+ コンテキストウィンドウ
  - 複数ファイル操作をサポート
  - Git ワークフローと統合
  - MCP プロトコルをサポート
- **インストールコマンド**:
  - Windows: `npm install -g @anthropic-ai/claude-code`
  - WSL/Linux: `npm install -g @anthropic-ai/claude-code`
- **確認方法**: `claude --version`
- **要件**: Node.js 18+

---

### 3. OpenAI Codex CLI
- **公式ウェブサイト**: https://www.npmjs.com/package/@openai/codex
- **開発元**: OpenAI
- **特徴**:
  - 軽量コーディングエージェント
  - ローカル実行、コードはアップロードされない
  - 自然言語コマンドをサポート
  - オープンソースプロジェクト
- **インストールコマンド**:
  - Windows: `npm install -g @openai/codex`
  - WSL/Linux: `npm install -g @openai/codex`
- **確認方法**: `codex --version`
- **要件**: Node.js 18+

---

### 4. Kimi CLI (Moonshot AI)
- **公式ウェブサイト**: https://pypi.org/project/kimi-cli/
- **開発元**: Moonshot AI
- **特徴**:
  - ターミナル AI エージェント
  - コードの読み書きとコマンド実行をサポート
  - ウェブ検索とスクレイピングをサポート
  - 自律的な計画とアクションの調整
- **インストールコマンド**:
  - Windows: `pip install kimi-cli`
  - WSL/Linux: `uv tool install --python 3.13 kimi-cli`
- **確認方法**: `kimi --version`
- **要件**: Python 3.13+, uv (推奨)

---

### 5. Gemini CLI (Google)
- **公式ウェブサイト**: https://www.npmjs.com/package/@google/gemini-cli
- **開発元**: Google
- **特徴**:
  - オープンソース AI エージェント
  - 1M トークンコンテキストウィンドウ
  - マルチモーダル AI 機能
  - 無料で使用可能
- **インストールコマンド**:
  - Windows: `npm install -g @google/gemini-cli`
  - WSL/Linux: `npm install -g @google/gemini-cli`
- **確認方法**: `gemini --version`
- **要件**: Node.js

---

### 6. Cursor Agent CLI
- **公式ウェブサイト**: https://docs.cursor.com/en/cli/installation
- **開発元**: Cursor
- **特徴**:
  - ターミナル AI アシスタント
  - リモートサーバーとコンテナをサポート
  - GitHub Actions と統合
  - 自動更新
- **インストールコマンド**:
  - WSL/Linux: `curl https://cursor.com/install -fsS | bash`
  - Windows: ネイティブインストールはサポートされていません
- **確認方法**: `cursor-agent --version`
- **使用方法**: `cursor-agent` または `agent chat "prompt"`

---

### 7. OpenCode
- **公式ウェブサイト**: https://opencode.ai/docs
- **開発元**: オープンソースコミュニティ
- **特徴**:
  - オープンソース AI コーディングエージェント
  - プライバシー優先、コードを保存しない
  - 無料ビルトインモデルをサポート
  - 外部 AI プロバイダーに接続可能
  - ネイティブターミナル UI
- **インストールコマンド**:
  - Windows: `curl -fsSL https://opencode.ai/install.ps1 | powershell`
  - WSL/Linux: `curl -fsSL https://opencode.ai/install.sh | bash`
- **確認方法**: `opencode --version`

---

### 8. Aider
- **公式ウェブサイト**: https://aider.chat/docs/install
- **開発元**: オープンソースコミュニティ
- **特徴**:
  - ターミナル AI プログラミングアシスタント
  - Git と深く統合
  - 複数の LLM をサポート (GPT-4, Claude, DeepSeek)
  - 自動コードテスト
  - 予算に優しい ($0.007/ファイル)
- **インストールコマンド**:
  - Windows: `pip install aider-install && aider-install`
  - WSL/Linux: `pip install aider-install && aider-install`
- **確認方法**: `aider --version`
- **要件**: Python 3.9+, Git

---

## 📊 ツール比較

| ツール | 開発元 | 無料 | オープンソース | Windows | WSL/Linux | 特徴 |
|------|--------|------|------|---------|-----------|------|
| Kiro CLI | AWS | ✅ | ❌ | ❌ | ✅ | 仕様駆動、AWS 統合 |
| Claude Code | Anthropic | ❌ | ❌ | ✅ | ✅ | 100K コンテキスト、MCP |
| Codex CLI | OpenAI | ❌ | ✅ | ✅ | ✅ | ローカル実行、プライバシー |
| Kimi CLI | Moonshot | ❌ | ❌ | ✅ | ✅ | ウェブ検索、中国語最適化 |
| Gemini CLI | Google | ✅ | ✅ | ✅ | ✅ | 1M コンテキスト、無料 |
| Cursor Agent | Cursor | ❌ | ❌ | ❌ | ✅ | CI/CD 統合 |
| OpenCode | コミュニティ | ✅ | ✅ | ✅ | ✅ | プライバシー優先、マルチモデル |
| Aider | コミュニティ | ✅ | ✅ | ✅ | ✅ | Git 統合、マルチ LLM |

---

## 🔧 事前要件

### 一般要件
- **Git**: ほとんどのツールはバージョン管理に Git を必要とします
- **ターミナル**: Windows Terminal (推奨) またはその他のモダンなターミナル

### Node.js ツール (Claude, Codex, Gemini)
- Node.js 18+
- npm または pnpm

### Python ツール (Kimi, Aider)
- Python 3.9+ (Aider) または 3.13+ (Kimi)
- pip または uv

### シェルスクリプトツール (Kiro, Cursor, OpenCode)
- bash (WSL/Linux)
- curl

---

## 💡 使用上の推奨事項

### ツール選択の考慮事項

1. **予算**:
   - 無料：Gemini CLI, OpenCode, Aider
   - 有料：Claude Code, Codex CLI, Kimi CLI, Cursor Agent

2. **プライバシー**:
   - ローカル実行：Codex CLI, OpenCode
   - クラウドベース：その他のツール

3. **機能要件**:
   - AWS 統合：Kiro CLI
   - Git 深い統合：Aider
   - マルチモデルサポート：OpenCode
   - 大きなコンテキスト：Gemini CLI (1M), Claude Code (100K)

4. **言語設定**:
   - 中国語最適化：Kimi CLI
   - 英語：その他のツール

---

## 🔄 設定の更新

新しいツールを追加したり、既存のツールの設定を変更したりするには、`config.json` ファイルを編集します：

```json
{
  "name": "tool-command",
  "displayName": "Tool Display Name",
  "winInstall": "Windows install command or null",
  "wslInstall": "WSL/Linux install command or null",
  "checkCommand": "tool-command --version",
  "url": "https://official-website.com"
}
```

---

## 📚 参考リソース

- [Kiro CLI ドキュメント](https://kiro.dev/docs/cli/installation/)
- [Claude Code ガイド](https://www.npmjs.com/package/@anthropic-ai/claude-code)
- [Codex CLI GitHub](https://github.com/openai/codex-cli)
- [Kimi CLI ドキュメント](https://moonshotai.github.io/kimi-cli/en/)
- [Gemini CLI 公式サイト](https://gemini-cli.click/)
- [Cursor CLI ドキュメント](https://docs.cursor.com/en/cli/)
- [OpenCode ドキュメント](https://opencode.ai/docs)
- [Aider ドキュメント](https://aider.chat/docs/)

---

*最終更新日：2026-02-26*
