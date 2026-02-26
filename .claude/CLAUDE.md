# AI-CLI Project - Claude Code 配置

## 项目信息

- **项目名称**: AI-CLI Launcher
- **项目类型**: PowerShell 终端启动工具
- **主要功能**: 统一管理和快速启动 AI CLI 工具
- **支持环境**: Windows / WSL (Linux)

## 文档结构

```
AI-CLI/
├── README.md           # 英文版（默认）
├── README.zh.md        # 中文版
├── README.ja.md        # 日文版
├── ai-cli.ps1          # 主程序
├── .claude/            # Claude Code 配置
│   ├── CLAUDE.md       # 项目配置
│   └── skills/         # 技能目录
├── docs/               # 文档目录
│   ├── TOOLS.md        # 工具参考（英文）
│   ├── TOOLS.zh.md     # 工具参考（中文）
│   ├── TOOLS.ja.md     # 工具参考（日文）
│   └── ...
└── .github/            # GitHub Actions 配置
```

## 常用命令

### 查看提交历史
```bash
git log --oneline -10
```

### 提交变更
```bash
git add .
git commit -m "版本号：描述"
```
