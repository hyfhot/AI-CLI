# CLI 语言参数功能增强

**日期**: 2026-03-02  
**状态**: ✅ 已完成

## 📋 需求

用户询问：**可以通过 ai-cli 命令的参数指定语言吗？**

## ✅ 实现方案

### 1. 添加 CLI 参数

**文件**: `ai_cli/cli.py`

添加 `--lang` / `-l` 参数：

```python
@click.option('--lang', '-l', 
              type=click.Choice(['auto', 'en', 'zh', 'ja', 'de'], case_sensitive=False), 
              help='Set language (auto, en, zh, ja, de)')
def main(init, config, uninstall, version, lang):
    # ...
    app = Application(language=lang)
```

### 2. 修改 Application 构造函数

**文件**: `ai_cli/app.py`

接受可选的语言参数，并设置优先级：

```python
def __init__(self, language: Optional[str] = None):
    # ...
    # Priority: CLI argument > config file > auto
    if language:
        init_language(language)
    else:
        language = self.config.settings.language if hasattr(self.config.settings, 'language') else 'auto'
        init_language(language)
```

### 3. 更新文档

更新了三个语言版本的 README：
- `README.md` (English)
- `README.zh.md` (中文)
- `README.ja.md` (日本語)

添加了语言选项说明和优先级说明。

## 🎯 功能特性

### 支持的语言选项

| 参数值 | 语言 | 说明 |
|--------|------|------|
| `auto` | 自动检测 | 根据系统语言自动选择（默认） |
| `en` | English | 英语 |
| `zh` | 中文 | 简体中文 |
| `ja` | 日本語 | 日语 |
| `de` | Deutsch | 德语 |

### 使用方法

```bash
# 使用中文启动
ai-cli --lang zh

# 使用日语启动
ai-cli --lang ja

# 使用德语启动（短参数）
ai-cli -l de

# 自动检测系统语言
ai-cli --lang auto

# 不指定参数（使用配置文件设置）
ai-cli
```

### 优先级

**CLI 参数 > 配置文件 > 自动检测**

1. 如果指定了 `--lang` 参数，使用该参数
2. 否则，使用配置文件中的 `settings.language`
3. 如果配置文件未设置，使用 `auto`（自动检测）

## 🧪 测试结果

```bash
$ ai-cli --help
Usage: ai-cli [OPTIONS]

  AI-CLI: Terminal launcher for AI coding assistants.

Options:
  -i, --init                     Initialize configuration file
  -c, --config                   Open configuration file for editing
  -u, --uninstall                Uninstall AI-CLI
  -v, --version                  Show version information
  -l, --lang [auto|en|zh|ja|de]  Set language (auto, en, zh, ja, de)
  --help                         Show this message and exit.
```

### 功能测试

```
=== 测试 CLI 语言参数功能 ===

--lang en (English): Select Project
--lang zh (Chinese): 选择项目
--lang ja (Japanese): プロジェクトを選択
--lang de (German): Projekt auswählen
--lang auto (Default (auto)): Select Project

✅ 语言参数功能正常！
```

## 📝 修改的文件

1. `ai_cli/cli.py` - 添加 `--lang` 参数
2. `ai_cli/app.py` - 修改构造函数接受语言参数
3. `README.md` - 更新命令行选项文档（英文）
4. `README.zh.md` - 更新命令行选项文档（中文）
5. `README.ja.md` - 更新命令行选项文档（日文）
6. `I18N-REVIEW-REPORT.md` - 更新国际化审查报告

## 💡 使用场景

### 场景 1: 临时切换语言
用户通常使用中文，但想临时用英语查看界面：
```bash
ai-cli --lang en
```

### 场景 2: 演示或截图
需要用特定语言进行演示或截图：
```bash
ai-cli --lang ja  # 日语演示
```

### 场景 3: 测试多语言
开发者测试不同语言的翻译：
```bash
ai-cli --lang zh  # 测试中文
ai-cli --lang de  # 测试德语
```

### 场景 4: 脚本自动化
在脚本中指定固定语言，避免受系统语言影响：
```bash
#!/bin/bash
# 始终使用英语运行
ai-cli --lang en
```

## ✅ 优势

1. **灵活性**: 无需修改配置文件即可切换语言
2. **便捷性**: 一个参数即可指定语言
3. **优先级明确**: CLI 参数优先级最高
4. **向后兼容**: 不影响现有配置文件的使用
5. **用户友好**: 使用 Click 的 Choice 类型，自动验证和提示

## 🎉 总结

成功添加了 `--lang` / `-l` 命令行参数，用户现在可以通过以下三种方式指定语言：

1. ✅ **命令行参数**: `ai-cli --lang zh`（优先级最高）
2. ✅ **配置文件**: `settings.language: "zh"`
3. ✅ **自动检测**: 根据系统语言自动选择

功能已完整实现并更新文档！

---

**实现人**: AI Assistant  
**完成日期**: 2026-03-02  
**状态**: ✅ 已完成并测试
