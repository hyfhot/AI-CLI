🌐 [English](INSTALL-GUIDE.md) | [中文](INSTALL-GUIDE.zh.md) | [日本語](INSTALL-GUIDE.ja.md)

# AI-CLI インストールツールガイド

## 機能概要

ツール選択画面で `I` キーを押すと、未インストールの AI CLI ツールをすばやくインストールできます。

## 使用手順

### 1. AI-CLI の起動
```powershell
.\ai-cli.ps1
```

### 2. プロジェクトの選択
↑↓ キーを使用してプロジェクトを選択し、Enter キーを押して確定します。

### 3. I キーを押してインストール画面に入る
ツール選択画面で `I` キーを押すと、インストールツールリストが開きます。

### 4. インストールするツールの選択
- リストには、未インストールだがインストールコマンドが設定されているすべてのツールが表示されます
- ツール名の後の `[Win]` または `[WSL]` は、インストール環境を示します
- ↑↓ キーを使用して選択し、Enter キーでインストールを確定します
- Esc キーを押すとツール選択画面に戻ります

### 5. インストール完了を待つ
- 画面にインストールコマンドと実行プロセスが表示されます
- インストール完了後、任意のキーを押して戻ります

## キーボードショートカット

### ツール選択画面
- `↑↓` - ナビゲーション選択
- `Enter` - 新しいウィンドウでツールを起動
- `Ctrl+Enter` - 新しいタブでツールを起動（Windows Terminal が必要）
- `I` - 新しいツールをインストール
- `Esc` - プロジェクト選択に戻る
- `Q` - プログラムを終了

### インストールツール画面
- `↑↓` - ナビゲーション選択
- `Enter` - 選択したツールをインストール
- `Esc` - ツール選択に戻る
- `Q` - プログラムを終了

## インストールロジック

### Windows 環境ツール
PowerShell でインストールコマンドを直接実行します。例：
```powershell
npm install -g @anthropic-ai/claude-code
```

### WSL 環境ツール
WSL を通じて bash コマンドを実行します。例：
```bash
wsl.exe -e bash -ic "curl -fsSL https://cli.kiro.dev/install | bash"
```

## サポートされているツール

`config.json` の設定に基づき、現在以下のツールのインストールをサポートしています：

| ツール | Windows | WSL/Linux |
|------|---------|-----------|
| Kiro CLI | ❌ | ✅ |
| Claude Code | ✅ | ✅ |
| OpenAI Codex | ✅ | ✅ |
| Kimi CLI | ✅ | ✅ |
| Gemini CLI | ✅ | ✅ |
| Cursor Agent | ❌ | ✅ |
| OpenCode | ✅ | ✅ |
| Aider | ✅ | ✅ |

## 注意事項

1. **権限要件**：一部のインストールコマンドには管理者権限が必要な場合があります
2. **ネットワーク接続**：インストール中は安定したネットワーク接続が必要です
3. **依存関係の確認**：必要な依存関係（Node.js、Python、pip など）がインストールされていることを確認してください
4. **WSL 設定**：WSL ツールには事前に WSL 環境の設定が必要です
5. **インストール検証**：インストール完了後、次回の起動時にツールが自動的に検出されます

## カスタムインストールコマンド

`config.json` ファイルを編集して、ツールのインストールコマンドを変更または追加できます：

```json
{
  "name": "tool-name",
  "displayName": "Tool Display Name",
  "winInstall": "npm install -g tool-name",
  "wslInstall": "curl -fsSL https://example.com/install.sh | bash",
  "checkCommand": "tool-name --version",
  "url": "https://official-website.com"
}
```

- `winInstall`: Windows 環境のインストールコマンド（null はサポートされていないことを示します）
- `wslInstall`: WSL/Linux 環境のインストールコマンド（null はサポートされていないことを示します）
- `checkCommand`: ツールがインストールされているかどうかを検出するためのコマンド

## トラブルシューティング

### インストールの失敗
1. ネットワーク接続を確認する
2. 依存関係（Node.js、Python など）がインストールされていることを確認する
3. エラーメッセージを確認し、インストールコマンドを手動で実行する
4. ツールの公式ドキュメントを参照する

### インストール後に検出されない
1. AI-CLI を再起動する
2. PATH 環境変数を確認する
3. `tool-name --version` を手動で実行してインストールを検証する
4. `config.json` の `checkCommand` が正しいか確認する

### WSL ツールのインストール失敗
1. WSL が正しくインストールおよび設定されていることを確認する
2. WSL でインストールコマンドを手動で実行してテストする
3. WSL のネットワーク接続を確認する
4. WSL を更新する：`wsl --update`

---

*最終更新日：2026-02-26*
