# AI-CLI 版本更新日志

## v2.0.0 (2026-02-26)

### 🎉 重大更新

#### 新功能
- ✅ **纯终端交互界面**：替代 WinForms，提供快速键盘驱动的 CLI 界面
- ✅ **循环启动模式**：程序不退出，支持连续选择工具和项目
- ✅ **多页签支持**：Ctrl+Enter 在 Windows Terminal 新页签中启动工具
- ✅ **工具安装功能**：按 I 键快速安装未安装的 AI CLI 工具
- ✅ **统一配置管理**：config.json 管理所有设置（项目、工具、偏好）
- ✅ **8个主流工具预配置**：开箱即用的工具配置

#### 核心修复
- 🐛 **WSL 工具检测**：使用 `bash -ic` 替代 `bash -lc`，正确加载 .bashrc 环境变量
- 🐛 **WSL 启动闪退**：采用单字符串参数方式，解决 ArgumentList 数组问题
- 🐛 **Show-Menu 返回值**：移除多余 return 语句，避免数组返回

#### 性能改进
- ⚡ **启动速度提升**：无 GUI 加载延迟，即时响应
- 🎨 **更好的键盘导航**：↑↓ 选择，Enter 确认，Esc 返回，I 安装
- 📚 **完善的文档系统**：README、TOOLS、INSTALL-GUIDE、BUGFIX

### 支持的 AI CLI 工具

| 工具 | 开发商 | Windows | WSL/Linux |
|------|--------|---------|-----------|
| Kiro CLI | AWS | ❌ | ✅ |
| Claude Code | Anthropic | ✅ | ✅ |
| OpenAI Codex | OpenAI | ✅ | ✅ |
| Kimi CLI | Moonshot AI | ✅ | ✅ |
| Gemini CLI | Google | ✅ | ✅ |
| Cursor Agent | Cursor | ❌ | ✅ |
| OpenCode | 开源 | ✅ | ✅ |
| Aider | 开源 | ✅ | ✅ |

### 快捷键

#### 工具选择界面
- `↑↓` - 导航选择
- `Enter` - 在新窗口启动工具
- `Ctrl+Enter` - 在新页签启动工具（需要 Windows Terminal）
- `I` - 安装新工具
- `Esc` - 返回项目选择
- `Q` - 退出程序

#### 项目选择界面
- `↑↓` - 导航选择
- `Enter` - 选择项目
- `Q` - 退出程序

### 技术架构

```
主循环
├── 项目选择循环
│   └── 工具选择循环
│       ├── 检测 Windows Terminal
│       ├── 显示提示（条件）
│       ├── 启动会话（普通/多页签）
│       ├── 安装工具（按 I 键）
│       └── 返回上级（按 Esc）
```

### 安装方式

#### 快速安装
```powershell
irm https://raw.githubusercontent.com/hyfhot/AI-CLI/master/install.ps1 | iex
```

#### 手动安装
```powershell
# 下载项目
git clone https://github.com/hyfhot/AI-CLI.git
cd AI-CLI

# 初始化配置
.\ai-cli.ps1 -Init

# 运行
.\ai-cli.ps1
```

### 配置文件

#### config.json 结构
```json
{
  "projects": [
    {
      "name": "项目名称",
      "path": "项目路径",
      "description": "项目描述"
    }
  ],
  "tools": [
    {
      "name": "工具命令",
      "displayName": "显示名称",
      "winInstall": "Windows安装命令",
      "wslInstall": "WSL安装命令",
      "checkCommand": "检测命令",
      "url": "官方网站"
    }
  ],
  "settings": {
    "language": "auto",
    "defaultEnv": "wsl",
    "terminalEmulator": "default"
  }
}
```

### 文档

- **README.md** - 完整使用说明和功能介绍
- **TOOLS.md** - 8个 AI CLI 工具的详细参考手册
- **INSTALL-GUIDE.md** - 工具安装功能使用指南
- **BUGFIX.md** - Bug 修复记录和技术细节
- **CHANGELOG.md** - 本文档，版本更新日志

---

## v1.x (历史版本)

### 特性
- ✅ WinForms 图形界面
- ✅ 环境变量配置（AI_PROJECTS）
- ✅ 基础工具检测和启动
- ✅ Windows/WSL 双环境支持
- ✅ 动态页签命名

### 限制
- ❌ 启动速度慢（GUI 加载）
- ❌ 每次启动后程序退出
- ❌ 不支持多页签
- ❌ 无工具安装功能
- ❌ 配置分散（环境变量 + JSON）

### 迁移到 v2.0

v1.x 用户无需手动迁移，v2.0 会自动：
1. 读取 `AI_PROJECTS` 环境变量
2. 生成 `config.json`
3. 保留所有项目配置

---

## 未来计划

### v2.1 (计划中)
- [ ] 项目管理：添加/编辑/删除项目
- [ ] 工具管理：添加/编辑/删除工具
- [ ] 配置导入/导出
- [ ] 工具使用统计

### v2.2 (计划中)
- [ ] 远程项目支持（SSH）
- [ ] Docker 容器支持
- [ ] 自定义启动脚本
- [ ] 工作区模板

---

*最后更新: 2026-02-26*
