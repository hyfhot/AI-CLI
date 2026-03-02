# 工具检测逻辑差异 - 快速总结

> **性能**: 迁移版慢 5.8 倍 (首次) / 64 倍 (后续)  
> **功能**: 迁移版增强 (获取版本信息)

---

## 🔴 关键差异

### 1. WSL 检测方式

**原版** (快):
```powershell
# 单次 WSL 启动，批量检测所有工具
wsl.exe -e bash -ic "for t in tool1 tool2 tool3; do ...; done"
# 时间: 500ms (5 个工具)
```

**迁移版** (慢):
```python
# 每个工具 2 次 WSL 启动 (检测 + 版本)
for tool in tools:
    wsl.exe -e bash -ic "command -v tool"    # 300ms
    wsl.exe -e bash -ic "tool --version"     # 300ms
# 时间: 3000ms (5 个工具)
```

**差异**: 慢 6 倍

---

### 2. 缓存机制

**原版** (有缓存):
```powershell
# 检测后写入配置文件
$config.tools[$i].winAvailable = $true
$config | ConvertTo-Json | Set-Content config.json

# 下次启动直接读取
# 时间: 50ms
```

**迁移版** (无缓存):
```python
# 每次都重新检测
tools = await detector.detect_all_tools(self.config.tools)
# 时间: 3200ms
```

**差异**: 慢 64 倍 (后续启动)

---

### 3. 版本信息

**原版**: ❌ 不获取  
**迁移版**: ✅ 获取

**权衡**: 性能换功能

---

## 📊 性能对比

| 场景 | 原版 | 迁移版 | 差异 |
|------|------|--------|------|
| 首次启动 (5+5 工具) | 550ms | 3200ms | 慢 5.8x |
| 后续启动 (有缓存) | 50ms | 3200ms | 慢 64x |

---

## 💡 优化方案

### 1. 批量 WSL 检测 (高优先级)

```python
# 单次 WSL 调用检测所有工具
check_script = "for t in tool1 tool2 tool3; do ...; done"
result = await asyncio.create_subprocess_exec(
    'wsl.exe', '-e', 'bash', '-ic', check_script
)
```

**预期**: 3000ms → 800ms (提升 3.75x)

### 2. 内存缓存 (高优先级)

```python
class ToolDetector:
    def __init__(self):
        self._cache = None
        self._cache_ttl = 30  # 30 秒
```

**预期**: 3200ms → 0ms (30 秒内)

---

## 🎯 结论

**当前问题**:
- ⚠️ WSL 检测慢 6 倍 (多次启动)
- ⚠️ 无缓存，每次都检测 (慢 64 倍)

**优化后**:
- ✅ 批量检测: 800ms (接近原版)
- ✅ 内存缓存: 0ms (30 秒内)
- ✅ 功能增强: 版本信息

**建议**: 立即实现批量检测和缓存机制

---

详细分析: [TOOL-DETECTION-COMPARISON.md](TOOL-DETECTION-COMPARISON.md)
