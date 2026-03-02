# 🐛 BOM 问题修复报告

> **修复时间**: 2026-03-01 11:04  
> **问题**: UTF-8 BOM 导致配置文件加载失败  
> **状态**: ✅ 已修复

---

## 问题描述

### 错误信息
```
PS C:\Users\hyfho> ai-cli
Error: Failed to load config: Unexpected UTF-8 BOM (decode using utf-8-sig): line 1 column 1 (char 0)
```

### 原因分析
- Windows 某些编辑器（如记事本）会在 UTF-8 文件开头添加 BOM (Byte Order Mark)
- BOM 是 3 个字节: `EF BB BF`
- Python `json.load()` 使用 `utf-8` 编码时不会自动处理 BOM
- 导致 JSON 解析失败

---

## 修复方案

### 代码修改

**文件**: `ai_cli/config.py`

**修改前**:
```python
with open(self.config_file, 'r', encoding='utf-8') as f:
    data = json.load(f)
```

**修改后**:
```python
with open(self.config_file, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
```

### 关键改动
- 使用 `utf-8-sig` 编码
- Python 会自动检测并移除 BOM
- 兼容有 BOM 和无 BOM 的文件

---

## 测试验证

### 新增测试

**文件**: `tests/test_config.py`

```python
def test_load_config_with_bom(self, temp_dir, sample_config_dict):
    """Test loading configuration file with UTF-8 BOM."""
    config_file = temp_dir / "config.json"
    # Write with BOM
    config_file.write_bytes(b'\xef\xbb\xbf' + json.dumps(sample_config_dict).encode('utf-8'))
    
    with patch.object(ConfigManager, 'get_config_dir', return_value=temp_dir):
        manager = ConfigManager()
        config = manager.load()
        
        assert config is not None
        assert len(config.projects) > 0
```

### 验证结果
```bash
$ python3 -c "from ai_cli.config import ConfigManager; cm = ConfigManager(); print('✓ OK')"
✓ OK
```

---

## 用户解决方案

### 方法 1: 重新安装（推荐）

```bash
cd /mnt/c/Projects/AIStudio/ai-cli-multi-platform
pip install -e ".[dev]" --force-reinstall
```

### 方法 2: 手动移除 BOM

**Windows PowerShell**:
```powershell
$configPath = "$env:APPDATA\AI-CLI\config.json"
$content = Get-Content $configPath -Raw
[System.IO.File]::WriteAllText($configPath, $content, [System.Text.UTF8Encoding]::new($false))
```

**Linux/macOS**:
```bash
sed -i '1s/^\xEF\xBB\xBF//' ~/.config/ai-cli/config.json
```

### 方法 3: 重新初始化

```bash
mv ~/.config/ai-cli/config.json ~/.config/ai-cli/config.json.bak
ai-cli --init
```

---

## 预防措施

### 编辑器设置

1. **VS Code**:
   ```json
   {
     "files.encoding": "utf8"
   }
   ```

2. **Notepad++**:
   - 选择 "编码" → "UTF-8" (不是 "UTF-8 BOM")

3. **Vim**:
   ```vim
   :set nobomb
   ```

### 使用示例配置

```bash
# Windows
copy config.example.json %APPDATA%\AI-CLI\config.json

# Linux/macOS
cp config.example.json ~/.config/ai-cli/config.json
```

---

## 技术细节

### UTF-8 BOM

| 编码 | BOM 字节 | Python 编码名 |
|------|----------|---------------|
| UTF-8 (无 BOM) | 无 | `utf-8` |
| UTF-8 (有 BOM) | `EF BB BF` | `utf-8-sig` |

### Python 编码处理

```python
# utf-8: 不处理 BOM，遇到 BOM 会报错
with open(file, 'r', encoding='utf-8') as f:
    pass

# utf-8-sig: 自动检测并移除 BOM
with open(file, 'r', encoding='utf-8-sig') as f:
    pass
```

### 为什么保存时用 utf-8？

```python
# 保存时使用 utf-8（不带 BOM）
with open(file, 'w', encoding='utf-8') as f:
    json.dump(data, f)
```

- JSON 标准不需要 BOM
- 避免跨平台兼容性问题
- 减少文件大小（3 字节）

---

## 相关文件

- ✅ `ai_cli/config.py` - 修复代码
- ✅ `tests/test_config.py` - 新增测试
- ✅ `docs/BOM-FIX.md` - 用户指南
- ✅ `CHANGELOG.md` - 版本记录

---

## 版本更新

- **版本**: 0.1.0 → 0.1.1
- **修复**: UTF-8 BOM 处理
- **影响**: 所有使用 Windows 编辑器的用户

---

## 总结

✅ **问题已修复**  
✅ **测试已添加**  
✅ **文档已更新**  
✅ **用户可重新安装解决**

---

**修复人**: AI Assistant  
**修复时间**: 2026-03-01 11:04  
**版本**: 0.1.1
