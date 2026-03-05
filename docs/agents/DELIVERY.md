# ✅ AI Worker System - 角色 Agent 交付文档

> **交付日期**: 2026-03-05  
> **版本**: 3.0 (Role-Based)  
> **格式**: JSON (role + description + prompt)

---

## 🎯 核心变更

### ✨ 角色 vs 团队成员

**之前的问题**: Agent 与团队成员 1:1 对应（11 个 Agent）

**现在的方案**: Agent 按**角色**划分，一个角色可被多个团队成员使用

**优势**:
- ✅ 更灵活：多个开发人员共用同一个角色 Agent
- ✅ 更清晰：角色职责明确，不与具体人员绑定
- ✅ 更易维护：修改角色定义即可影响所有使用者
- ✅ 更符合实际：团队成员可能承担多个角色

---

## 📦 交付内容

### 🤖 9 个角色 Agent（JSON 格式）

| 文件 | 角色 | 描述 | 适用人员 |
|------|------|------|---------|
| `architect.json` | Architect | 架构设计和技术决策 | Tech Lead, Backend Architect |
| `backend-developer.json` | Backend Developer | 后端服务实现 | 4 个后端开发人员 |
| `ai-engineer.json` | AI Engineer | AI 模型集成和 Prompt 工程 | AI Engineer |
| `data-engineer.json` | Data Engineer | 数据存储和向量数据库 | Data Engineer |
| `devops-engineer.json` | DevOps Engineer | 基础设施和部署 | DevOps Engineer |
| `qa-engineer.json` | QA Engineer | 质量保证和测试 | QA Engineer |
| `security-engineer.json` | Security Engineer | 安全监控和成本控制 | Tech Lead, DevOps |
| `product-manager.json` | Product Manager | 产品需求和功能规划 | Product Manager |
| `technical-writer.json` | Technical Writer | 技术文档编写 | Technical Writer |

### 🛠️ 使用方式

JSON 文件仅作为**参考模板**，需要手动创建 Agent：

```bash
kiro-cli agent create
# 按提示输入 Name, Description, Prompt（从 JSON 复制）
```

### 📚 使用文档（3 个）

- **`README.md`** - 完整使用指南
- **`QUICK_REFERENCE.md`** - 快速参考卡片
- **`DELIVERY.md`** - 交付文档

---

## 📖 Prompt 结构

每个 Agent 的 `prompt` 字段采用统一结构：

```
## Task:
角色的核心任务描述

## Requirements:
1. 具体要求 1
2. 具体要求 2
3. ...

## Output:
期望的交付物和输出格式
```

**示例**（Security Engineer）:
```
## Task:
为编排系统建立全方位的监控和安全屏障。

## Requirements:
1. 设计实时 Token 消耗阈值和成本熔断机制（Kill Switch）
2. 建立所有 Agent 行为的 Trace 审计链路（基于 OpenTelemetry）
3. 针对 AI 生成的代码执行严格的敏感字符过滤和指令注入检测

## Output:
安全评估报告模板及紧急熔断逻辑的实现逻辑
```

---

## 🚀 快速开始

### 步骤 1: 手动创建角色 Agent

由于 kiro-cli 是交互式设计，需要手动创建每个角色：

```bash
kiro-cli agent create
```

在交互界面中输入：
- **Name**: 角色名称（如 `architect`）
- **Description**: 从 JSON 文件复制 `description` 字段
- **Prompt**: 从 JSON 文件复制 `prompt` 字段

重复以上步骤创建所有 9 个角色。

### 步骤 2: 验证

```bash
kiro-cli agent list
```

### 步骤 3: 使用

```bash
kiro-cli agent use backend-developer
kiro-cli chat
# 在 chat 中询问具体问题
```

---

## 💡 角色使用场景

### 架构设计阶段
```bash
kiro-cli agent use architect
"Design the Worker Manager module architecture"
```

### 开发阶段
```bash
# 所有后端开发人员使用同一个角色
kiro-cli agent use backend-developer
"Implement RESTful API for worker management"
```

### AI 集成阶段
```bash
kiro-cli agent use ai-engineer
"Design prompt template for code review tasks"
```

### 部署阶段
```bash
kiro-cli agent use devops-engineer
"Create Kubernetes deployment manifests"
```

### 测试阶段
```bash
kiro-cli agent use qa-engineer
"Write integration tests for API Gateway"
```

### 安全审计
```bash
kiro-cli agent use security-engineer
"Implement token consumption monitoring with circuit breaker"
```

---

## 📊 统计

- **角色数量**: 9 个
- **JSON 文件**: 9 个 (~9 KB)
- **文档**: 3 个 (~8 KB)
- **总大小**: ~17 KB

---

## ✅ 交付状态

**状态**: ✅ 完成  
**格式**: JSON (role + description + prompt)  
**结构**: Task + Requirements + Output  
**准备就绪**: 可立即使用 🚀

---

**交付日期**: 2026-03-05  
**版本**: 3.0 (Role-Based)  
**位置**: `/mnt/c/Projects/AIStudio/AI-CLI/docs/agents/`
