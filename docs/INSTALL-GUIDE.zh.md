🌐 [English](INSTALL-GUIDE.md) | [中文](INSTALL-GUIDE.zh.md) | [日本語](INSTALL-GUIDE.ja.md)

# AI-CLI 安装工具功能说明

## 功能概述

在工具选择界面按 `I` 键可以快速安装未安装的 AI CLI 工具。

## 使用步骤

### 1. 启动 AI-CLI
```powershell
.\ai-cli.ps1
```

### 2. 选择项目
使用 ↑↓ 键选择项目，按 Enter 确认。

### 3. 按 I 键进入安装界面
在工具选择界面，按 `I` 键打开安装工具列表。

### 4. 选择要安装的工具
- 列表显示所有未安装但配置了安装命令的工具
- 工具名称后标注 `[Win]` 或 `[WSL]` 表示安装环境
- 使用 ↑↓ 键选择，Enter 确认安装
- 按 Esc 返回工具选择界面

### 5. 等待安装完成
- 屏幕会显示安装命令和执行过程
- 安装完成后按任意键返回

## 快捷键说明

### 工具选择界面
- `↑↓` - 导航选择
- `Enter` - 在新窗口启动工具
- `Ctrl+Enter` - 在新页签启动工具（需要 Windows Terminal）
- `I` - 安装新工具
- `Esc` - 返回项目选择
- `Q` - 退出程序

### 安装工具界面
- `↑↓` - 导航选择
- `Enter` - 安装选中的工具
- `Esc` - 返回工具选择
- `Q` - 退出程序

## 安装逻辑

### Windows 环境工具
直接在 PowerShell 中执行安装命令，例如：
```powershell
npm install -g @anthropic-ai/claude-code
```

### WSL 环境工具
通过 WSL 执行 bash 命令，例如：
```bash
wsl.exe -e bash -ic "curl -fsSL https://cli.kiro.dev/install | bash"
```

## 支持的工具

根据 `config.json` 配置，当前支持安装：

| 工具 | Windows | WSL/Linux |
|------|---------|-----------|
| Kiro CLI | ❌ | ✅ |
| Claude Code | ✅ | ✅ |
| OpenAI Codex | ✅ | ✅ |
| Kimi CLI | ✅ | ✅ |
| Gemini CLI | ✅ | ✅ |
| Cursor Agent | ❌ | ✅ |
| OpenCode | ✅ | ✅ |
| Aider | ✅ | ✅ |

## 注意事项

1. **权限要求**：某些安装命令可能需要管理员权限
2. **网络连接**：安装过程需要稳定的网络连接
3. **依赖检查**：确保已安装必要的依赖（Node.js, Python, pip 等）
4. **WSL 配置**：WSL 工具需要先配置好 WSL 环境
5. **安装验证**：安装完成后，工具会在下次启动时自动检测

## 自定义安装命令

编辑 `config.json` 文件可以修改或添加工具的安装命令：

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

- `winInstall`: Windows 环境安装命令（null 表示不支持）
- `wslInstall`: WSL/Linux 环境安装命令（null 表示不支持）
- `checkCommand`: 用于检测工具是否已安装的命令

## 故障排除

### 安装失败
1. 检查网络连接
2. 确认依赖已安装（Node.js, Python 等）
3. 查看错误信息，手动执行安装命令
4. 参考工具官方文档

### 安装后未检测到
1. 重启 AI-CLI
2. 检查 PATH 环境变量
3. 手动运行 `tool-name --version` 验证安装
4. 查看 `config.json` 中的 `checkCommand` 是否正确

### WSL 工具安装失败
1. 确认 WSL 已正确安装和配置
2. 在 WSL 中手动执行安装命令测试
3. 检查 WSL 网络连接
4. 更新 WSL：`wsl --update`

---

*最后更新：2026-02-26*
