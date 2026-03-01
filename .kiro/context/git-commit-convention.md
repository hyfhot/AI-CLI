# AI-CLI Project Git Commit Convention

## CRITICAL: This convention MUST be followed for ALL git commits in this project

## Commit Format

```
<type>[optional scope]: <subject>

[optional body with bullet points]
```

## Types & Examples

### 1. Version Release: `v<version>: <description>`
**When**: Major features, significant updates
**Body structure**:
```
## 🎯 核心变更
- Feature 1 description
- Feature 2 description

## 📝 变更说明
Detailed explanation

## 📊 变更统计
- Modified files list
```

### 2. Bug Fix: `fix: <description>`
**Body**: Bullet points with `-` prefix
```
fix: 优化卸载时的错误提示体验

- 捕获文件占用错误，提供友好的提示信息
- 引导用户关闭所有 AI-CLI 窗口后重试
- 提供手动删除路径作为备选方案
```

### 3. Documentation: `docs: <description>`
**Body**: Include sections with emoji headers
```
docs: 添加核心优势说明，提升用户吸引力

## 📝 变更内容
Description of changes

## 🎯 核心优势
1. Benefit 1
2. Benefit 2

## 📊 修改文件
- File list
```

### 4. Maintenance: `chore: <description>`
```
chore: 停止跟踪 .serena 目录

## 变更说明
- What changed

## 原因
Why it changed
```

## Rules

1. **Language**: Chinese (primary), English technical terms allowed
2. **Subject**: 
   - Concise (< 50 chars)
   - Use verbs: 修复, 优化, 新增, 添加, 移除, 实现
   - Focus on user impact
3. **Body**:
   - Use `-` bullet points for multiple items
   - Start with most important changes
   - Explain WHY, not just WHAT
   - Use emoji section headers for version releases (🎯 📝 💡 📊)
4. **Special attention**:
   - Always mention encoding changes (BOM, UTF-8, CRLF)
   - Highlight Windows compatibility fixes
   - Emphasize UX improvements

## AI Agent Instructions

When creating git commits:
1. Analyze the changes to determine the correct type
2. Write subject in Chinese, keep it concise
3. Structure body with bullet points
4. For version releases, use emoji section headers
5. Always explain user-facing impact
6. List modified files when relevant

**Example command pattern**:
```bash
git add <files> && git commit -m "<type>: <subject>

- Change 1 explanation
- Change 2 explanation
- Change 3 explanation" && git push
```
