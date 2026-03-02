# AI-CLI 功能对比清单

对比 PowerShell 版本 (v2.2) 和 Python 版本 (v3.1.0) 的功能实现情况。

## ✅ 已完全移植的功能

### 核心功能
- ✅ **配置管理**
  - 用户配置目录 (`%APPDATA%\AI-CLI\config.json`)
  - 配置加载/保存
  - 配置初始化 (`--init`)
  - 配置编辑 (`--config`)
  - 配置迁移（旧格式自动升级）
  - 增量工具更新（保留用户项目和自定义工具）

- ✅ **项目管理**
  - 树状结构（文件夹 + 项目）
  - 添加项目/文件夹 (N 键)
  - 删除项目/文件夹 (D 键)
  - 面包屑导航
  - 环境变量注入
  - 路径验证和创建

- ✅ **工具检测**
  - Windows 工具检测
  - WSL 工具检测
  - Linux 工具检测
  - macOS 工具检测
  - 批量检测优化
  - 缓存机制（30秒 TTL）
  - 手动刷新 (R 键)

- ✅ **工具安装**
  - 安装菜单 (I 键)
  - Windows 工具安装
  - WSL 工具安装
  - Linux 工具安装
  - macOS 工具安装
  - PATH 自动更新（Windows）
  - 安装后状态刷新

- ✅ **终端启动**
  - Windows 环境启动
  - WSL 环境启动
  - Linux 环境启动
  - macOS 环境启动
  - 新窗口启动 (Enter)
  - 新标签页启动 (Ctrl+Enter / T)
  - Windows Terminal 支持
  - 环境变量传递
  - 路径自动转换（Windows ↔ WSL）

- ✅ **Git 集成**
  - Git worktree 检测
  - 分支信息显示
  - 当前分支检测

- ✅ **国际化 (i18n)**
  - 多语言支持（英文、中文、日文、德文）
  - 自动语言检测
  - 语言切换

- ✅ **用户界面**
  - 交互式菜单
  - 键盘导航（↑↓）
  - 快捷键支持
  - 面包屑导航
  - 项目信息显示（名称、路径、分支、环境变量）
  - 工具列表显示
  - 图标显示（📁 文件夹、📄 项目）

- ✅ **命令行接口**
  - `ai-cli` - 启动交互界面
  - `ai-cli --init` - 初始化配置
  - `ai-cli --config` - 编辑配置
  - `ai-cli --version` - 显示版本
  - `ai-cli --help` - 显示帮助
  - `ai-cli --uninstall` - 卸载程序

- ✅ **安装/卸载**
  - Windows 安装脚本 (`install.ps1`)
  - Linux/macOS 安装脚本 (`install.sh`)
  - 桌面快捷方式创建
  - 卸载功能（保留用户配置）
  - PATH 环境变量管理

## ⚠️ 部分移植的功能

### Git Worktree 管理
- ✅ 检测 worktree
- ✅ 显示分支信息
- ❌ **Worktree 选择菜单**（PowerShell 版本有 `Select-GitWorktree` 函数）
  - 多个 worktree 时弹出选择界面
  - 显示分支状态（ahead/behind）
  - 显示当前 worktree 标记
  - 支持 detached HEAD 显示

### 后台工具检测
- ✅ 前台检测（带缓存）
- ✅ 手动刷新 (R 键)
- ❌ **后台异步检测**（PowerShell 版本有 `Start-BackgroundDetection` 函数）
  - 启动时后台 Job 检测工具
  - 检测完成后自动更新配置
  - 不阻塞主界面

## ❌ 未移植的功能

### 1. Git Worktree 选择界面
**PowerShell 版本实现：**
```powershell
function Select-GitWorktree {
    param([array]$worktrees, [string]$currentPath, [string]$projectName)
    # 显示多个 worktree 选择菜单
    # 显示分支名、状态（↑ahead ↓behind）、路径
    # 支持键盘导航选择
}
```

**影响：**
- 当项目有多个 worktree 时，Python 版本无法让用户选择
- 只能使用配置中的默认路径

**建议实现位置：**
- `ai_cli/core/git.py` - 添加 `select_worktree()` 方法
- `ai_cli/app.py` - 在 `_select_project()` 中调用

### 2. 后台异步工具检测
**PowerShell 版本实现：**
```powershell
function Start-BackgroundDetection {
    param($configPath)
    # 启动后台 Job 检测所有工具
    # 检测完成后更新配置文件
    # 主界面不阻塞
}
```

**影响：**
- Python 版本首次启动时需要等待工具检测完成
- 用户体验略有延迟（虽然有缓存机制）

**建议实现方式：**
- 使用 `asyncio.create_task()` 在后台运行检测
- 或使用 `threading.Thread` 启动后台线程
- 检测完成后更新缓存和配置

### 3. 配置文件原子写入的备份恢复
**PowerShell 版本实现：**
```powershell
function Save-Config {
    # 1. 写入临时文件 (.tmp)
    # 2. 备份现有配置 (.bak)
    # 3. 移动临时文件到目标位置
    # 4. 删除备份
    # 失败时从备份恢复
}
```

**Python 版本实现：**
- ✅ 使用 UTF-8-sig 编码（处理 BOM）
- ❌ 没有临时文件和备份机制
- ❌ 写入失败时无法恢复

**建议改进：**
- 在 `ConfigManager.save()` 中添加原子写入逻辑
- 使用 `tempfile` 模块创建临时文件
- 添加备份和恢复机制

### 4. PATH 长度检查
**PowerShell 版本实现：**
```powershell
function Add-ToUserPath {
    # 检查 PATH 长度是否超过 2047 字符
    # 超过时警告并跳过添加
}
```

**Python 版本实现：**
- ❌ 没有 PATH 长度检查
- 可能导致 Windows 系统问题

**建议改进：**
- 在 `ToolInstaller._add_to_user_path()` 中添加长度检查
- Windows PATH 限制：2047 字符

### 5. 工具可执行文件搜索路径
**PowerShell 版本搜索路径：**
```powershell
$searchPaths = @(
    "$env:LOCALAPPDATA\Programs\Python\Python*\Scripts",
    "$env:APPDATA\Python\Python*\Scripts",
    "$env:USERPROFILE\.local\bin",
    "$env:USERPROFILE\AppData\Roaming\npm",
    "$env:ProgramFiles\nodejs",
    "$env:LOCALAPPDATA\Microsoft\WindowsApps",
    "$env:ProgramFiles\Git\cmd",
    "$env:USERPROFILE\.cargo\bin",
    "$env:USERPROFILE\go\bin"
)
```

**Python 版本搜索路径：**
```python
search_paths = [
    os.path.expandvars(r"%LOCALAPPDATA%\Programs\Python\Python*\Scripts"),
    os.path.expandvars(r"%APPDATA%\Python\Python*\Scripts"),
    os.path.expandvars(r"%USERPROFILE%\.local\bin"),
    os.path.expandvars(r"%USERPROFILE%\AppData\Roaming\npm"),
]
```

**差异：**
- ❌ Python 版本缺少：
  - `%ProgramFiles%\nodejs`
  - `%LOCALAPPDATA%\Microsoft\WindowsApps`
  - `%ProgramFiles%\Git\cmd`
  - `%USERPROFILE%\.cargo\bin`
  - `%USERPROFILE%\go\bin`

**建议改进：**
- 在 `ToolInstaller._find_tool_executable()` 中补充搜索路径

### 6. 空项目列表提示
**PowerShell 版本实现：**
```powershell
if ($currentItems.Count -eq 0 -and $currentPath.Count -eq 0) {
    # 显示提示信息
    # 自动进入新增项目流程
}
```

**Python 版本实现：**
- ❌ 空列表时只显示空菜单
- 没有友好提示

**建议改进：**
- 在 `Application._select_project()` 中添加空列表检测
- 显示提示信息并引导用户添加项目

### 7. 输入取消支持
**PowerShell 版本实现：**
```powershell
function Read-InputWithPlaceholder {
    param([bool]$AllowCancel = $false)
    # 支持 ESC 键取消输入
    # 返回 "__CANCEL__" 标记
}
```

**Python 版本实现：**
- ❌ 输入框不支持 ESC 取消
- 用户必须输入或 Ctrl+C 退出

**建议改进：**
- 使用 `prompt_toolkit` 库实现高级输入
- 支持 ESC 取消、历史记录、自动补全

### 8. 滚动显示支持
**PowerShell 版本实现：**
```powershell
function Show-Menu {
    $maxDisplay = [Math]::Min($items.Count, 15)
    $offset = [Math]::Max(0, $selected - $maxDisplay + 1)
    # 只显示 15 项，支持滚动
}
```

**Python 版本实现：**
- ❌ 显示所有项目，不支持滚动
- 项目过多时界面混乱

**建议改进：**
- 在 `Menu.render_tree()` 和 `Menu.render_tools()` 中添加滚动逻辑
- 限制显示数量（如 15 项）
- 根据选中项动态调整显示范围

### 9. 终端模拟器配置
**PowerShell 版本支持：**
- `default` - 默认终端
- `wezterm` - WezTerm 终端

**Python 版本支持：**
- ✅ `default` - 默认终端
- ❌ 没有 WezTerm 支持

**建议改进：**
- 在 `PlatformAdapter` 中添加 WezTerm 支持
- 检测 `wezterm` 命令是否可用
- 使用 `wezterm start --cwd` 启动

### 10. 工具显示优化
**PowerShell 版本：**
- 项目和文件夹显示图标（📁 📄）
- 工具不显示图标

**Python 版本：**
- ✅ 项目和文件夹显示图标
- ✅ 工具不显示图标
- ✅ 项目信息显示在顶部

**状态：** 已完全实现

## 📊 功能完成度统计

| 类别 | 已完成 | 部分完成 | 未完成 | 完成度 |
|------|--------|----------|--------|--------|
| 核心功能 | 9 | 0 | 0 | 100% |
| 项目管理 | 6 | 0 | 1 | 86% |
| 工具管理 | 6 | 1 | 1 | 75% |
| Git 集成 | 2 | 1 | 0 | 67% |
| 用户界面 | 7 | 0 | 2 | 78% |
| 安装/卸载 | 5 | 0 | 0 | 100% |
| 配置管理 | 5 | 0 | 1 | 83% |
| **总计** | **40** | **2** | **5** | **85%** |

## 🎯 优先级建议

### 高优先级（影响用户体验）
1. **滚动显示支持** - 项目过多时界面混乱
2. **空项目列表提示** - 首次使用体验差
3. **Git Worktree 选择界面** - 多 worktree 项目无法使用

### 中优先级（功能完善）
4. **后台异步工具检测** - 减少启动延迟
5. **输入取消支持** - 提升交互体验
6. **工具搜索路径补充** - 提高工具检测成功率

### 低优先级（稳定性增强）
7. **配置文件原子写入** - 防止数据丢失
8. **PATH 长度检查** - 避免系统问题
9. **WezTerm 支持** - 小众需求

## 📝 实现建议

### 1. 滚动显示（最优先）
```python
# ai_cli/ui/menu.py
def render_tree(self, items: List[Dict[str, Any]], selected: int = 0, max_display: int = 15) -> None:
    offset = max(0, selected - max_display + 1)
    visible_items = items[offset:offset + max_display]
    # 显示 visible_items
    # 显示滚动指示器（如 "↑ 3 more above" / "↓ 5 more below"）
```

### 2. Git Worktree 选择
```python
# ai_cli/core/git.py
class GitDetector:
    def select_worktree(self, worktrees: List[Dict], current_path: str) -> Optional[str]:
        # 显示 worktree 选择菜单
        # 返回选中的 worktree 路径
        pass

# ai_cli/app.py
def _select_project(self) -> Optional[ProjectNode]:
    # 检测 worktrees
    worktrees = git_detector.detect_worktrees(project.path)
    if len(worktrees) > 1:
        selected_path = git_detector.select_worktree(worktrees, project.path)
        if selected_path:
            project.path = selected_path
```

### 3. 后台异步检测
```python
# ai_cli/core/tools.py
class ToolDetector:
    def __init__(self):
        self._background_task = None
    
    def start_background_detection(self, tools_config: List[ToolConfig]):
        self._background_task = asyncio.create_task(
            self._background_detect(tools_config)
        )
    
    async def _background_detect(self, tools_config: List[ToolConfig]):
        tools = await self.detect_all_tools(tools_config)
        # 更新缓存和配置
```

## 🔄 版本历史

- **v2.2** (PowerShell) - 原始版本，功能完整
- **v3.0** (Python) - 初始移植，核心功能实现
- **v3.1.0** (Python) - 功能补全，85% 功能完成

## 📌 总结

Python 版本 (v3.1.0) 已经实现了 PowerShell 版本 (v2.2) 的 **85%** 功能，核心功能完全可用。

**主要优势：**
- ✅ 跨平台支持（Windows、Linux、macOS）
- ✅ 更好的代码结构和可维护性
- ✅ 国际化支持
- ✅ 现代化的异步架构

**待改进：**
- ⚠️ 滚动显示支持
- ⚠️ Git Worktree 选择界面
- ⚠️ 后台异步检测
- ⚠️ 部分细节优化

**建议：**
优先实现高优先级功能（滚动显示、空列表提示、Worktree 选择），即可达到 **95%** 功能完成度，满足日常使用需求。
