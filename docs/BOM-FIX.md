# BOM 问题修复指南

## 问题描述

错误信息：
```
Error: Failed to load config: Unexpected UTF-8 BOM (decode using utf-8-sig): line 1 column 1 (char 0)
```

这是因为配置文件包含 UTF-8 BOM (Byte Order Mark)。

## 解决方案

### 方法 1: 已修复（推荐）

代码已更新，使用 `utf-8-sig` 编码自动处理 BOM：

```python
# ai_cli/config.py
with open(self.config_file, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
```

**重新安装即可**：
```bash
cd /mnt/c/Projects/AIStudio/ai-cli-multi-platform
pip install -e ".[dev]" --force-reinstall
```

### 方法 2: 手动移除 BOM

如果需要手动修复配置文件：

**Windows**:
```powershell
# 找到配置文件
$configPath = "$env:APPDATA\AI-CLI\config.json"

# 读取并重新保存（移除 BOM）
$content = Get-Content $configPath -Raw
[System.IO.File]::WriteAllText($configPath, $content, [System.Text.UTF8Encoding]::new($false))
```

**Linux/macOS**:
```bash
# 找到配置文件
config_path="$HOME/.config/ai-cli/config.json"

# 移除 BOM
sed -i '1s/^\xEF\xBB\xBF//' "$config_path"
```

### 方法 3: 重新初始化配置

```bash
# 备份旧配置
mv ~/.config/ai-cli/config.json ~/.config/ai-cli/config.json.bak

# 重新初始化
ai-cli --init

# 手动迁移配置内容
```

## 验证修复

```bash
# 运行程序
ai-cli

# 应该正常启动，不再报错
```

## 预防措施

1. **使用正确的编辑器**：
   - VS Code: 设置 `"files.encoding": "utf8"` (不带 BOM)
   - Notepad++: 选择 "UTF-8" 而不是 "UTF-8 BOM"
   - Vim: `:set nobomb`

2. **使用示例配置**：
   ```bash
   cp config.example.json ~/.config/ai-cli/config.json
   ```

3. **程序自动处理**：
   - 新版本已自动处理 BOM
   - 保存时不会写入 BOM

## 技术细节

### 什么是 BOM？

BOM (Byte Order Mark) 是 UTF-8 文件开头的特殊字节序列 (`EF BB BF`)，某些 Windows 编辑器会自动添加。

### 为什么会出现问题？

Python 的 `json.load()` 默认使用 `utf-8` 编码，不会自动处理 BOM，导致解析失败。

### 修复方案

使用 `utf-8-sig` 编码，Python 会自动检测并移除 BOM：

```python
# 修复前
with open(file, 'r', encoding='utf-8') as f:  # ❌ 不处理 BOM

# 修复后  
with open(file, 'r', encoding='utf-8-sig') as f:  # ✅ 自动处理 BOM
```

## 相关链接

- [Python 编码文档](https://docs.python.org/3/library/codecs.html#encodings-and-unicode)
- [UTF-8 BOM 说明](https://en.wikipedia.org/wiki/Byte_order_mark)
