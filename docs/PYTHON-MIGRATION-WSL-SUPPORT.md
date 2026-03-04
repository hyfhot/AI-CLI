# Python 迁移方案 - WSL 支持补充文档

> **补充说明**: 针对 Windows 平台的 WSL 双环境支持设计

---

## 问题说明

原迁移方案中移除了 WSL 相关功能，但这对 Windows 开发者来说是核心需求：
- Windows 开发者经常同时使用 Windows 原生工具和 WSL 工具
- 需要在同一界面中检测和启动两种环境的工具
- 需要自动进行路径转换（Windows ↔ WSL）

---

## 解决方案

### 1. 架构调整

**平台适配器增强**：
```
原方案:
  WindowsAdapter  → 仅支持 Windows 原生
  LinuxAdapter    → 仅支持 Linux 原生
  MacOSAdapter    → 仅支持 macOS 原生

修正方案:
  WindowsAdapter  → 支持 Windows 原生 + WSL 双环境
  LinuxAdapter    → 仅支持 Linux 原生
  MacOSAdapter    → 仅支持 macOS 原生
```

### 2. 工具检测增强

#### 2.1 数据模型扩展

```python
from dataclasses import dataclass
from enum import Enum

class ToolEnvironment(Enum):
    """工具运行环境"""
    WINDOWS = "windows"
    WSL = "wsl"
    LINUX = "linux"
    MACOS = "macos"

@dataclass
class Tool:
    """检测到的工具"""
    name: str
    display_name: str
    environment: ToolEnvironment  # 新增：标识运行环境
    available: bool
    version: Optional[str] = None
    
    def get_display_label(self) -> str:
        """获取显示标签"""
        env_label = {
            ToolEnvironment.WINDOWS: "[Win]",
            ToolEnvironment.WSL: "[WSL]",
            ToolEnvironment.LINUX: "",
            ToolEnvironment.MACOS: ""
        }
        label = env_label.get(self.environment, "")
        return f"{label} {self.display_name}".strip()
```

#### 2.2 Windows 平台双环境检测

```python
import sys
import shutil
import subprocess
import asyncio
from typing import List

class WindowsToolDetector:
    """Windows 平台工具检测器（支持 Windows + WSL）"""
    
    @staticmethod
    def is_wsl_available() -> bool:
        """检测 WSL 是否可用"""
        if sys.platform != 'win32':
            return False
        
        try:
            result = subprocess.run(
                ['wsl.exe', '--status'],
                capture_output=True,
                timeout=2
            )
            return result.returncode == 0
        except:
            return False
    
    async def detect_windows_tool(self, tool_config: ToolConfig) -> Optional[Tool]:
        """检测 Windows 原生工具"""
        if not tool_config.win_install:
            return None
        
        available = shutil.which(tool_config.name) is not None
        version = None
        
        if available:
            try:
                result = await asyncio.create_subprocess_exec(
                    tool_config.name, '--version',
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, _ = await result.communicate()
                version = stdout.decode().strip().split('\n')[0]
            except:
                pass
        
        if available:
            return Tool(
                name=tool_config.name,
                display_name=tool_config.display_name,
                environment=ToolEnvironment.WINDOWS,
                available=True,
                version=version
            )
        return None
    
    async def detect_wsl_tool(self, tool_config: ToolConfig) -> Optional[Tool]:
        """检测 WSL 工具"""
        if not tool_config.wsl_install:
            return None
        
        if not self.is_wsl_available():
            return None
        
        try:
            # 使用 wsl.exe -e bash -ic 确保加载完整环境
            result = await asyncio.create_subprocess_exec(
                'wsl.exe', '-e', 'bash', '-ic', f'command -v {tool_config.name}',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await result.communicate()
            available = bool(stdout.strip())
            
            version = None
            if available:
                # 获取版本
                result = await asyncio.create_subprocess_exec(
                    'wsl.exe', '-e', 'bash', '-ic', f'{tool_config.name} --version',
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, _ = await result.communicate()
                version = stdout.decode().strip().split('\n')[0]
            
            if available:
                return Tool(
                    name=tool_config.name,
                    display_name=tool_config.display_name,
                    environment=ToolEnvironment.WSL,
                    available=True,
                    version=version
                )
        except:
            pass
        
        return None
    
    async def detect_all_tools(self, tools_config: List[ToolConfig]) -> List[Tool]:
        """并发检测所有工具（Windows + WSL）"""
        tasks = []
        
        for tc in tools_config:
            # Windows 环境检测
            if tc.win_install:
                tasks.append(self.detect_windows_tool(tc))
            
            # WSL 环境检测
            if tc.wsl_install:
                tasks.append(self.detect_wsl_tool(tc))
        
        results = await asyncio.gather(*tasks)
        
        # 过滤掉 None 结果
        return [tool for tool in results if tool is not None]
```

#### 2.3 跨平台统一接口

```python
class ToolDetector:
    """跨平台工具检测器"""
    
    def __init__(self):
        if sys.platform == 'win32':
            self.detector = WindowsToolDetector()
        elif sys.platform == 'darwin':
            self.detector = MacOSToolDetector()
        else:
            self.detector = LinuxToolDetector()
    
    async def detect_all_tools(self, tools_config: List[ToolConfig]) -> List[Tool]:
        """检测所有工具"""
        return await self.detector.detect_all_tools(tools_config)

class LinuxToolDetector:
    """Linux 平台工具检测器（仅原生）"""
    
    async def detect_all_tools(self, tools_config: List[ToolConfig]) -> List[Tool]:
        tools = []
        for tc in tools_config:
            if not tc.linux_install:
                continue
            
            available = shutil.which(tc.name) is not None
            if available:
                tools.append(Tool(
                    name=tc.name,
                    display_name=tc.display_name,
                    environment=ToolEnvironment.LINUX,
                    available=True
                ))
        return tools

class MacOSToolDetector:
    """macOS 平台工具检测器（仅原生）"""
    
    async def detect_all_tools(self, tools_config: List[ToolConfig]) -> List[Tool]:
        tools = []
        for tc in tools_config:
            if not tc.macos_install:
                continue
            
            available = shutil.which(tc.name) is not None
            if available:
                tools.append(Tool(
                    name=tc.name,
                    display_name=tc.display_name,
                    environment=ToolEnvironment.MACOS,
                    available=True
                ))
        return tools
```

### 3. 路径转换增强

```python
from pathlib import Path, PureWindowsPath
import sys

class PathConverter:
    """跨平台路径转换器"""
    
    @staticmethod
    def to_wsl_path(windows_path: str) -> str:
        """Windows 路径 → WSL 路径"""
        win_path = PureWindowsPath(windows_path)
        
        # 提取驱动器号
        if win_path.drive:
            drive = win_path.drive[0].lower()
            rest = str(win_path.relative_to(win_path.drive)).replace('\\', '/')
            return f"/mnt/{drive}/{rest}".rstrip('/')
        
        # 已经是 Unix 风格路径
        return windows_path.replace('\\', '/')
    
    @staticmethod
    def to_windows_path(wsl_path: str) -> str:
        """WSL 路径 → Windows 路径"""
        import re
        
        # 匹配 /mnt/x/... 格式
        match = re.match(r'^/mnt/([a-z])/(.*)$', wsl_path)
        if match:
            drive = match.group(1).upper()
            rest = match.group(2).replace('/', '\\')
            return f"{drive}:\\{rest}"
        
        return wsl_path
    
    @staticmethod
    def normalize_for_environment(path: str, environment: ToolEnvironment) -> str:
        """根据目标环境规范化路径"""
        if environment == ToolEnvironment.WSL:
            # 如果是 Windows 路径，转换为 WSL 路径
            if ':' in path and path[1] == ':':
                return PathConverter.to_wsl_path(path)
        elif environment == ToolEnvironment.WINDOWS:
            # 如果是 WSL 路径，转换为 Windows 路径
            if path.startswith('/mnt/'):
                return PathConverter.to_windows_path(path)
        
        return path
```

### 4. 终端启动增强

```python
class WindowsAdapter(PlatformAdapter):
    """Windows 平台适配器（支持 Windows + WSL）"""
    
    def launch_terminal(
        self,
        tool: Tool,
        command: str,
        cwd: str,
        env: Dict[str, str],
        title: str,
        use_tab: bool = False
    ):
        """启动终端会话"""
        
        if tool.environment == ToolEnvironment.WSL:
            self._launch_wsl_session(tool, command, cwd, env, title, use_tab)
        else:
            self._launch_windows_session(tool, command, cwd, env, title, use_tab)
    
    def _launch_windows_session(
        self,
        tool: Tool,
        command: str,
        cwd: str,
        env: Dict[str, str],
        title: str,
        use_tab: bool
    ):
        """启动 Windows 原生会话"""
        # 构建环境变量设置
        env_setup = ' & '.join([f'set {k}={v}' for k, v in env.items()])
        full_cmd = f'title {title} & cd /d "{cwd}" & {env_setup} & {command}'
        
        if use_tab and shutil.which('wt'):
            subprocess.Popen([
                'wt', '-w', '0', 'new-tab',
                '--title', title,
                'cmd', '/k', full_cmd
            ])
        else:
            subprocess.Popen(['cmd', '/k', full_cmd])
    
    def _launch_wsl_session(
        self,
        tool: Tool,
        command: str,
        cwd: str,
        env: Dict[str, str],
        title: str,
        use_tab: bool
    ):
        """启动 WSL 会话"""
        # 转换路径
        wsl_path = PathConverter.to_wsl_path(cwd)
        
        # 转换环境变量中的路径
        wsl_env = {}
        for k, v in env.items():
            # 检测是否为 Windows 路径
            if ':' in v and v[1] == ':':
                wsl_env[k] = PathConverter.to_wsl_path(v)
            else:
                wsl_env[k] = v
        
        # 构建环境变量设置
        env_setup = ' && '.join([f'export {k}="{v}"' for k, v in wsl_env.items()])
        
        # 构建完整命令
        full_cmd = f"cd '{wsl_path}'"
        if env_setup:
            full_cmd += f" && {env_setup}"
        full_cmd += f" && {command}; exec bash"
        
        if use_tab and shutil.which('wt'):
            subprocess.Popen([
                'wt', '-w', '0', 'new-tab',
                '--title', title,
                'wsl', '-e', 'bash', '-ic', full_cmd
            ])
        else:
            subprocess.Popen([
                'wsl.exe', '-e', 'bash', '-ic', full_cmd
            ])
```

### 5. UI 显示增强

```python
from rich.console import Console
from rich.table import Table

class MenuRenderer:
    """菜单渲染器"""
    
    def render_tool_menu(self, tools: List[Tool], selected: int, project_name: str):
        """渲染工具选择菜单"""
        console = Console()
        console.clear()
        
        console.print(f"\n  === Select AI Tool (Project: {project_name}) ===", style="cyan bold")
        console.print("  " + "=" * 60, style="dim")
        console.print()
        
        table = Table(show_header=False, box=None, padding=(0, 2))
        
        for i, tool in enumerate(tools):
            prefix = ">" if i == selected else " "
            style = "green" if i == selected else "white"
            
            # 显示环境标签
            label = tool.get_display_label()  # 例如: "[WSL] kiro-cli" 或 "[Win] claude"
            
            if tool.version:
                label += f" [dim]({tool.version})[/dim]"
            
            table.add_row(f"{prefix} {label}", style=style)
        
        console.print(table)
        
        console.print("\n  [dim][↑↓] Select  [Enter] Launch  [Ctrl+Enter] New Tab  [Esc] Back  [Q] Quit[/dim]")
```

### 6. 配置文件格式保持兼容

```json
{
  "tools": [
    {
      "name": "kiro-cli",
      "displayName": "Kiro CLI",
      "winInstall": null,
      "wslInstall": "curl -fsSL https://cli.kiro.dev/install | bash",
      "linuxInstall": "curl -fsSL https://cli.kiro.dev/install | bash",
      "macosInstall": "brew install kiro-cli",
      "checkCommand": "kiro-cli --version",
      "url": "https://kiro.dev/cli/"
    },
    {
      "name": "claude",
      "displayName": "Claude Code",
      "winInstall": "npm install -g @anthropic-ai/claude-code",
      "wslInstall": "npm install -g @anthropic-ai/claude-code",
      "linuxInstall": "npm install -g @anthropic-ai/claude-code",
      "macosInstall": "npm install -g @anthropic-ai/claude-code",
      "checkCommand": "claude --version",
      "url": "https://www.npmjs.com/package/@anthropic-ai/claude-code"
    }
  ]
}
```

**说明**：
- `winInstall`: Windows 原生安装命令
- `wslInstall`: WSL 环境安装命令（仅 Windows 使用）
- `linuxInstall`: Linux 原生安装命令
- `macosInstall`: macOS 原生安装命令

### 7. 工具安装功能增强

```python
class ToolInstaller:
    """工具安装器"""
    
    def __init__(self, platform_adapter: PlatformAdapter):
        self.adapter = platform_adapter
    
    async def install_tool(self, tool_config: ToolConfig, environment: ToolEnvironment) -> bool:
        """安装工具"""
        
        # 获取安装命令
        install_cmd = self._get_install_command(tool_config, environment)
        if not install_cmd:
            return False
        
        # 根据环境执行安装
        if environment == ToolEnvironment.WSL:
            return await self._install_in_wsl(install_cmd)
        elif environment == ToolEnvironment.WINDOWS:
            return await self._install_in_windows(install_cmd)
        else:
            return await self._install_native(install_cmd)
    
    def _get_install_command(self, tool_config: ToolConfig, environment: ToolEnvironment) -> Optional[str]:
        """获取安装命令"""
        if environment == ToolEnvironment.WINDOWS:
            return tool_config.win_install
        elif environment == ToolEnvironment.WSL:
            return tool_config.wsl_install
        elif environment == ToolEnvironment.LINUX:
            return tool_config.linux_install
        elif environment == ToolEnvironment.MACOS:
            return tool_config.macos_install
        return None
    
    async def _install_in_wsl(self, command: str) -> bool:
        """在 WSL 中安装"""
        try:
            process = await asyncio.create_subprocess_exec(
                'wsl.exe', '-e', 'bash', '-ic', command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            return process.returncode == 0
        except:
            return False
    
    async def _install_in_windows(self, command: str) -> bool:
        """在 Windows 中安装"""
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            return process.returncode == 0
        except:
            return False
    
    async def _install_native(self, command: str) -> bool:
        """在原生环境中安装"""
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            return process.returncode == 0
        except:
            return False
```

---

## 使用示例

### 完整流程

```python
import asyncio

async def main():
    # 1. 加载配置
    config = ConfigManager().load()
    
    # 2. 检测工具（Windows 会同时检测 Windows + WSL）
    detector = ToolDetector()
    tools = await detector.detect_all_tools(config.tools)
    
    # 输出示例:
    # [
    #   Tool(name="kiro-cli", environment=WSL, available=True),
    #   Tool(name="claude", environment=WINDOWS, available=True),
    #   Tool(name="aider", environment=WSL, available=True),
    # ]
    
    # 3. 显示工具菜单
    renderer = MenuRenderer()
    renderer.render_tool_menu(tools, selected=0, project_name="MyProject")
    
    # 4. 用户选择工具
    selected_tool = tools[0]  # 假设选择了 kiro-cli (WSL)
    
    # 5. 启动会话
    adapter = get_platform_adapter()
    adapter.launch_terminal(
        tool=selected_tool,
        command="kiro-cli chat",
        cwd="C:\\Projects\\MyProject",  # Windows 路径
        env={"API_KEY": "xxx"},
        title="KIRO-CLI - MyProject",
        use_tab=True
    )
    # 自动转换为: cd '/mnt/c/Projects/MyProject' && export API_KEY="xxx" && kiro-cli chat

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 关键改进点总结

| 功能 | 原方案 | 修正方案 |
|------|--------|----------|
| Windows 工具检测 | 仅原生 | 原生 + WSL 双环境 |
| 工具显示 | 无环境标签 | `[Win]` / `[WSL]` 标签 |
| 路径转换 | 移除 | 保留并增强 |
| 终端启动 | 仅 Windows | Windows + WSL 分别处理 |
| 环境变量注入 | 统一处理 | 根据环境自动转换路径 |
| 配置格式 | 简化 | 保留 `wslInstall` 字段 |

---

## 兼容性保证

1. **配置文件完全兼容** - 保留所有字段（winInstall, wslInstall, linuxInstall, macosInstall）
2. **用户体验一致** - Windows 用户仍能看到 `[Win]` 和 `[WSL]` 标签
3. **功能无损** - 所有 PowerShell 版本的 WSL 功能均保留
4. **跨平台扩展** - Linux/macOS 用户不受影响

---

**文档版本**: v1.1  
**更新日期**: 2026-03-01  
**状态**: 已修正
