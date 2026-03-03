# AI-CLI 安装指南

> 🌐 [English](INSTALL-GUIDE.md) | **中文** | [日本語](INSTALL-GUIDE.ja.md) | [Deutsch](INSTALL-GUIDE.de.md)

## 快速安装

### 使用安装脚本（推荐）

**Windows**:
```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

**Linux/macOS**:
```bash
bash install.sh
```

### 手动安装

```bash
# 克隆仓库
git clone https://github.com/hyfhot/AI-CLI.git
cd AI-CLI

# 如果使用 Git worktree
git worktree add ../ai-cli-multi-platform python-migration
cd ../ai-cli-multi-platform

# 安装依赖
pip install -e ".[dev]"
```

## 工具安装功能

在工具选择界面按 `I` 键可以快速安装尚未安装的 AI CLI 工具。

### 使用步骤

1. **启动 AI-CLI**
   ```bash
   ai-cli
   ```

2. **选择项目**
   - 使用 ↑↓ 键选择项目
   - 按 Enter 确认

3. **按 I 键进入安装界面**
   - 在工具选择界面按 `I` 键
   - 打开安装工具列表

4. **选择要安装的工具**
   - 列表显示所有未安装但配置了安装命令的工具
   - `[Windows]`、`[WSL]`、`[Linux]` 或 `[macOS]` 表示安装环境
   - 使用 ↑↓ 键选择
   - 按 Enter 确认安装
   - 按 Esc 返回工具选择界面

5. **等待安装完成**
   - 屏幕显示安装命令和执行过程
   - 安装完成后按任意键返回

## 配置

### 初始化配置

```bash
ai-cli --init
```

这将在以下位置创建默认配置文件：
- **Windows**: `%APPDATA%\AI-CLI\config.json`
- **Linux**: `~/.config/ai-cli/config.json`
- **macOS**: `~/Library/Application Support/ai-cli/config.json`

### 编辑配置

```bash
ai-cli --config
```

或使用您喜欢的文本编辑器手动编辑配置文件。

## 故障排除

### Python 版本问题

**问题**: 命令未找到或导入错误

**解决方案**: 确保安装了 Python 3.8+
```bash
python --version  # 应该是 3.8 或更高版本
```

### 权限问题

**问题**: 安装时权限被拒绝

**解决方案**: 
- Linux/macOS: 必要时使用 `sudo`
- Windows: 以管理员身份运行

### 路径问题

**问题**: 安装后找不到 `ai-cli` 命令

**解决方案**: 
- 确保 pip 安装目录在 PATH 中
- 尝试使用 `python -m ai_cli.cli` 代替

### WSL 问题

**问题**: 未检测到 WSL 工具

**解决方案**: 
- 确保已安装 WSL: `wsl --install`
- 检查 WSL 是否可访问: `wsl --list`

## 卸载

```bash
ai-cli --uninstall
```

这将：
- 删除配置目录
- 卸载 Python 包
- 清理所有临时文件

---

更多信息请参阅[主 README](../README.zh.md)。
