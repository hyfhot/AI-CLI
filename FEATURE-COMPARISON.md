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

### 配置文件原子写入
- ✅ 使用 UTF-8-sig 编码（处理 BOM）
- ❌ **临时文件和备份机制**（PowerShell 版本有完整的原子写入）
  - 写入临时文件 (.tmp)
  - 备份现有配置 (.bak)
  - 失败时从备份恢复

## ❌ 未移植的功能

### 1. 配置文件原子写入的备份恢复
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

**影响：** 低优先级
- 配置文件损坏风险较低
- 可以手动恢复

**建议改进：**
- 在 `ConfigManager.save()` 中添加原子写入逻辑
- 使用 `tempfile` 模块创建临时文件
- 添加备份和恢复机制

### 2. WezTerm 终端模拟器支持
**PowerShell 版本支持：**
- `default` - 默认终端
- `wezterm` - WezTerm 终端

**Python 版本支持：**
- ✅ `default` - 默认终端
- ❌ 没有 WezTerm 支持

**影响：** 低优先级
- WezTerm 是小众终端模拟器
- 大多数用户使用默认终端或 Windows Terminal

**建议改进：**
- 在 `PlatformAdapter` 中添加 WezTerm 支持
- 检测 `wezterm` 命令是否可用
- 使用 `wezterm start --cwd` 启动

## 📊 功能完成度统计

| 类别 | 已完成 | 部分完成 | 未完成 | 完成度 |
|------|--------|----------|--------|--------|
| 核心功能 | 9 | 0 | 0 | 100% |
| 项目管理 | 7 | 0 | 0 | 100% |
| 工具管理 | 8 | 0 | 0 | 100% |
| Git 集成 | 3 | 0 | 0 | 100% |
| 用户界面 | 9 | 0 | 0 | 100% |
| 安装/卸载 | 5 | 0 | 0 | 100% |
| 配置管理 | 5 | 1 | 0 | 83% |
| 终端支持 | 1 | 0 | 1 | 50% |
| **总计** | **47** | **1** | **1** | **96%** |

## 🎯 优先级建议

### ~~高优先级（影响用户体验）~~ ✅ 已完成
1. ~~**滚动显示支持**~~ ✅ - 项目过多时界面混乱
2. ~~**空项目列表提示**~~ ✅ - 首次使用体验差
3. ~~**Git Worktree 选择界面**~~ ✅ - 多 worktree 项目无法使用

### ~~中优先级（功能完善）~~ ✅ 已完成
4. ~~**后台异步工具检测**~~ ✅ - 减少启动延迟
5. ~~**输入取消支持**~~ ✅ - 提升交互体验
6. ~~**工具搜索路径补充**~~ ✅ - 提高工具检测成功率

### 低优先级（稳定性增强）
7. **配置文件原子写入** - 防止数据丢失
8. **WezTerm 支持** - 小众需求

## 📝 实现建议

### ~~1. 滚动显示（最优先）~~ ✅ 已实现
```python
# ai_cli/ui/menu.py
def render_tree(self, items: List[Dict[str, Any]], selected: int = 0, max_display: int = 15) -> None:
    offset = max(0, min(selected - max_display // 2, total - max_display))
    visible_items = items[offset:offset + max_display]
    # 显示 visible_items
    # 显示滚动指示器（如 "↑ 3 more above" / "↓ 5 more below"）
```

### ~~2. Git Worktree 选择~~ ✅ 已实现
```python
# ai_cli/core/git.py
class GitManager:
    def select_worktree(self, worktrees: List[Dict], current_path: str) -> Optional[str]:
        # 显示 worktree 选择菜单
        # 返回选中的 worktree 路径
        pass

# ai_cli/app.py
def _select_project(self) -> Optional[ProjectNode]:
    # 检测 worktrees
    worktrees = git_manager.detect_worktrees(project.path)
    if len(worktrees) > 1:
        selected_path = git_manager.select_worktree(worktrees, project.path)
        if selected_path:
            project.path = selected_path
```

### ~~3. 后台异步检测~~ ✅ 已实现
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

### 1. 配置文件原子写入（低优先级）
```python
# ai_cli/config.py
import tempfile
import shutil

def save(self, config: Config) -> None:
    config_file = self.get_config_dir() / "config.json"
    
    # 1. 写入临时文件
    with tempfile.NamedTemporaryFile(mode='w', delete=False, 
                                     dir=config_file.parent) as tmp:
        json.dump(config.to_dict(), tmp, indent=2, ensure_ascii=False)
        tmp_path = tmp.name
    
    # 2. 备份现有配置
    if config_file.exists():
        backup_path = config_file.with_suffix('.bak')
        shutil.copy2(config_file, backup_path)
    
    # 3. 移动临时文件
    try:
        shutil.move(tmp_path, config_file)
        # 4. 删除备份
        if backup_path.exists():
            backup_path.unlink()
    except Exception as e:
        # 失败时从备份恢复
        if backup_path.exists():
            shutil.copy2(backup_path, config_file)
        raise
```

### 2. WezTerm 支持（低优先级）
```python
# ai_cli/platform/windows.py
def launch_terminal(self, tool: Tool, project: ProjectNode, new_tab: bool = False):
    terminal_emulator = self.config.settings.terminal_emulator
    
    if terminal_emulator == "wezterm":
        # 检测 wezterm
        if shutil.which("wezterm"):
            cmd = f'wezterm start --cwd "{project.path}" -- {tool.name}'
            subprocess.Popen(cmd, shell=True)
            return
    
    # 默认终端
    # ...
```

## 🔄 版本历史

- **v2.2** (PowerShell) - 原始版本，功能完整
- **v3.0** (Python) - 初始移植，核心功能实现
- **v3.1.0** (Python) - 功能补全，85% 功能完成
- **v3.2.0** (Python) - 高中优先级功能实现，96% 功能完成 ⭐

## 📌 总结

Python 版本 (v3.2.0) 已经实现了 PowerShell 版本 (v2.2) 的 **96%** 功能，核心功能完全可用。

**主要优势：**
- ✅ 跨平台支持（Windows、Linux、macOS）
- ✅ 更好的代码结构和可维护性
- ✅ 国际化支持
- ✅ 现代化的异步架构
- ✅ 滚动显示支持
- ✅ Git Worktree 选择界面
- ✅ 后台异步检测
- ✅ 输入取消支持（ESC）
- ✅ 扩展的工具搜索路径
- ✅ PATH 长度检查

**待改进：**
- ⚠️ 配置文件原子写入（低优先级）
- ⚠️ WezTerm 支持（低优先级）

**建议：**
Python 版本已达到 **96%** 功能完成度，完全满足日常使用需求。剩余 2 个低优先级功能可根据实际需求选择性实现。
