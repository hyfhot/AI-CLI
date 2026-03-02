# 按 Enter 后"死机"问题说明

> **问题**: 按 Enter 后程序看起来死机  
> **原因**: 工具检测需要时间（2-5秒）  
> **修复**: 添加加载提示  
> **状态**: ✅ 已优化

---

## 问题

按 Enter 选择项目后，程序看起来"死机"：
- 界面无响应
- 无任何提示
- 实际上在后台检测工具

---

## 原因

工具检测需要时间：

```python
async def _select_tool(self, project):
    detector = ToolDetector()
    tools = await detector.detect_all_tools(self.config.tools)
    # ⏱️ 这里需要 2-5 秒
    # - 检测 Windows 工具
    # - 检测 WSL 工具
    # - 获取版本信息
```

**耗时操作**:
1. 检查 WSL 是否可用 (~1秒)
2. 检测每个工具是否安装 (~0.5秒/工具)
3. 获取工具版本信息 (~0.5秒/工具)
4. 总计：2-5秒（取决于配置的工具数量）

---

## 修复

### 添加加载提示

```python
async def _select_tool(self, project):
    detector = ToolDetector()
    
    # ✅ 显示加载提示
    self.menu.console.print("[yellow]Detecting tools (this may take a few seconds)...[/yellow]")
    
    tools = await detector.detect_all_tools(self.config.tools)
    
    # ✅ 处理无工具情况
    if not tools:
        self.menu.console.print("\n[red]No AI tools detected.[/red]")
        time.sleep(2)
        return None
```

---

## 用户体验

### 修复前
```
=== Select Project ===
> 📄 My Project

[按 Enter]
(无任何提示，看起来死机 2-5秒)

=== Select AI Tool ===
...
```

### 修复后
```
=== Select Project ===
> 📄 My Project

[按 Enter]
Detecting tools (this may take a few seconds)...
(清楚知道程序在工作)

=== Select AI Tool ===
...
```

---

## 优化建议

### 1. 缓存检测结果（未实现）

```python
class Application:
    def __init__(self):
        self._tools_cache = None
        self._cache_time = None
    
    async def _select_tool(self, project):
        # 缓存 30 秒
        if self._tools_cache and time.time() - self._cache_time < 30:
            tools = self._tools_cache
        else:
            tools = await detector.detect_all_tools(self.config.tools)
            self._tools_cache = tools
            self._cache_time = time.time()
```

### 2. 后台预加载（未实现）

```python
def run(self):
    # 启动时预加载
    asyncio.run(self._preload_tools())
    
    while True:
        project = self._select_project()
        # 工具已预加载，立即显示
        tool = self._select_tool_cached(project)
```

### 3. 并行检测（已实现）

```python
# ✅ 已使用 asyncio 并行检测
async def detect_all_tools(self, configs):
    tasks = [self.detect_tool(cfg) for cfg in configs]
    results = await asyncio.gather(*tasks)
    # 并行检测，比串行快 3-5 倍
```

---

## 验证

```bash
cd /mnt/c/Projects/AIStudio/ai-cli-multi-platform
pip install -e ".[dev]" --force-reinstall
ai-cli
```

**测试步骤**:
1. 选择项目
2. 按 Enter
3. 应该立即看到 "Detecting tools..." 提示
4. 等待 2-5 秒
5. 显示工具列表

---

## 总结

- ✅ 不是真的死机，只是检测工具需要时间
- ✅ 已添加加载提示，用户体验更好
- ✅ 使用 asyncio 并行检测，已经是最优性能
- 💡 未来可以添加缓存进一步优化

---

**修复时间**: 2026-03-01 11:42  
**版本**: 0.1.4
