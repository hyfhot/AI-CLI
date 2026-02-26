🌐 [English](BUGFIX.md) | [中文](BUGFIX.zh.md) | [日本語](BUGFIX.ja.md)

# AI-CLI v2.0 バグ修正ドキュメント

## 🐛 問題の説明

**エラーメッセージ**:
```
The filename, directory name, or volume label syntax is incorrect.
'kiro-cli' is not recognized as an internal or external command,
operable program or batch file.
```

**根本原因**:
1. `Show-Menu` 関数に `return $selected` があり、ループのたびに値を返してしまったため、変数が配列になってしまった
2. WSL 起動コマンドが配列パラメータ渡し方式を使用しており、旧バージョンと互換性がなかった

---

## ✅ 修正ソリューション

### 修正 1: Show-Menu からの return 文の削除

**問題**: `Show-Menu` 関数がループ内で `$selected` を返しており、複数の戻り値を生成していた

**修正前**:
```powershell
function Show-Menu {
    # ...
    for ($i = 0; $i -lt $items.Count; $i++) {
        # メニュー項目の表示
    }
    return $selected  # ❌ エラー：呼び出しごとに返してしまう
}
```

**修正後**:
```powershell
function Show-Menu {
    # ...
    for ($i = 0; $i -lt $items.Count; $i++) {
        # メニュー項目の表示
    }
    # ✅ 値を返さない、表示のみを担当
}
```

### 修正 2: 旧バージョンの起動方法の使用

**問題**: 配列によるパラメータ渡しにより、WSL の起動に失敗していた

**修正前**:
```powershell
Start-Process "wsl.exe" -ArgumentList @("-e", "bash", "-ic", $bashCmd)
```

**修正後** (旧バージョン方式を採用):
```powershell
$wslExe = "C:\Windows\System32\wsl.exe"
$wslArgs = "-e bash -ic `"cd '$wslPath'; $tool; exec bash`""
Start-Process -FilePath $wslExe -ArgumentList $wslArgs
```

---

## 📝 最終コード

### WSL 起動
```powershell
if ($env -eq "wsl") {
    $wslPath = ConvertTo-WslPath $projectPath
    $wslExe = "C:\Windows\System32\wsl.exe"
    $wslArgs = "-e bash -ic `"cd '$wslPath'; $tool; exec bash`""
    Start-Process -FilePath $wslExe -ArgumentList $wslArgs
}
```

### Windows 起動
```powershell
else {
    $cmdArgs = "/k `"title $title & cd /d `"$projectPath`" & $tool`""
    Start-Process -FilePath "cmd.exe" -ArgumentList $cmdArgs
}
```

---

## ✅ 検証結果

- ✅ WSL ツールが正常に起動
- ✅ Windows ツールが正常に起動
- ✅ パス変換が正しい
- ✅ ターミナルが開いたままになる
- ✅ 変数渡しが正しい

---

**修正日**: 2026-02-26
**バージョン**: 2.0.1
**ステータス**: ✅ 修正済みおよびテスト合格
