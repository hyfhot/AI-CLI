# Git Commit Convention for AI-CLI Project

## Commit Message Format

```
<type>[optional scope]: <subject>

[optional body]
```

## Types

### Version Release (Major Updates)
- **Format**: `v<version>: <description>`
- **Example**: `v2.3.0: 新增 Git Worktree 支持和用户体验优化`
- **When to use**: Major feature releases, significant updates
- **Body**: Include detailed changelog with sections:
  - `## 🎯 核心变更` - Core changes
  - `## 📝 变更说明` - Change description
  - `## 💡 实际效果` - Real-world impact
  - `## 📊 修改文件` / `## 📊 变更统计` - File changes

### Bug Fixes
- **Type**: `fix`
- **Format**: `fix: <description>`
- **Example**: `fix: 优化卸载时的错误提示体验`
- **Body**: Use bullet points with `-` prefix
  ```
  - 捕获文件占用错误，提供友好的提示信息
  - 引导用户关闭所有 AI-CLI 窗口后重试
  - 提供手动删除路径作为备选方案
  ```

### Documentation
- **Type**: `docs`
- **Format**: `docs: <description>`
- **Example**: `docs: 添加核心优势说明，提升用户吸引力`
- **Body**: Include sections when applicable:
  - `## 📝 变更内容` - What changed
  - `## 🎯 核心优势` - Key benefits
  - `## 📊 修改文件` - Modified files

### Maintenance
- **Type**: `chore`
- **Format**: `chore: <description>`
- **Example**: `chore: 停止跟踪 .serena 目录`
- **Body**: Include:
  - `## 变更说明` - Change description
  - `## 原因` - Reason

## Subject Guidelines

1. **Language**: Use Chinese (project's primary language)
2. **Length**: Keep concise, typically under 50 characters
3. **Style**: 
   - Use descriptive verbs: 修复, 优化, 新增, 添加, 移除, 实现
   - Be specific about what changed
   - Focus on user impact, not implementation details

## Body Guidelines

1. **Format**: Use bullet points with `-` prefix for multiple items
2. **Structure**: 
   - Start with most important changes
   - Group related changes together
   - Use emoji section headers for version releases (🎯 📝 💡 📊)
3. **Content**:
   - Explain WHY the change was made
   - Describe user-facing impact
   - Include technical details when relevant
4. **Language**: Consistent Chinese with occasional English technical terms

## Examples

### Simple Fix
```
fix: 移除 install.ps1 的 BOM 以支持管道执行

- install.ps1 不能有 BOM（通过 irm|iex 管道执行）
- ai-cli.ps1 保留 BOM（作为文件执行，Windows 中文版需要）
- 更新 .gitattributes 区分不同脚本的编码处理
```

### Version Release
```
v2.3.0: 新增 Git Worktree 支持和用户体验优化

## 🎯 核心变更

### 1. Git Worktree 自动检测与选择 ⭐ 新功能
- 选择项目后自动检测 Git 仓库和 worktree
- 多个 worktree 时弹出智能选择界面
- 单个 worktree 时透明处理，不影响现有流程

## 📝 变更说明
默认配置文件应保持空白，让用户通过以下方式添加项目：
1. 运行 `ai-cli` 后按 N 键交互式添加
2. 运行 `ai-cli -Config` 手动编辑配置

## 📊 变更统计
- 修改文件: config.json
- 新增功能: Git Worktree 支持
```

### Documentation Update
```
docs: 添加核心优势说明，提升用户吸引力

## 📝 变更内容
在三个语言版本的 README 中添加「为什么选择 AI-CLI？」章节

## 🎯 核心优势
1. **告别记忆命令** - 一个命令替代 8+ 个工具
2. **Windows ↔ WSL 无缝切换** - 自动路径转换
3. **环境变量自动注入** - 无需手动 export

## 📊 修改文件
- README.md (英文)
- README.zh.md (中文)
- README.ja.md (日文)
```

## Special Notes

1. **Encoding Issues**: Always mention encoding changes (BOM, UTF-8, CRLF)
2. **Windows Compatibility**: Highlight Windows-specific fixes
3. **User Experience**: Emphasize UX improvements and user-facing changes
4. **Breaking Changes**: Clearly mark in version releases
5. **Multi-file Changes**: List all affected files in body

## Commit Frequency

- Commit logical units of work
- One feature/fix per commit when possible
- Group related changes in version releases
