# AI Worker System - Role-Based Agents

> **Updated**: 2026-03-05  
> **Format**: JSON (role + description + prompt)  
> **Total Roles**: 9

---

## 🎯 角色定义原则

**角色 ≠ 团队成员**

- **角色（Role）**: 按职能划分的工作类型，可被多个团队成员使用
- **团队成员（Team Member）**: 具体的人员配置，一个人可能承担多个角色

例如：
- 4 个后端开发人员都使用 `backend-developer` 角色
- 技术负责人可能同时使用 `architect` 和 `backend-developer` 角色

---

## 📋 角色清单

| 角色 | Agent 名称 | 描述 | 适用团队成员 |
|------|-----------|------|-------------|
| **Architect** | architect | 系统架构设计和技术决策 | Tech Lead, Backend Architect |
| **Backend Developer** | backend-developer | 后端服务实现 | 所有后端开发人员 (4人) |
| **AI Engineer** | ai-engineer | AI 模型集成和 Prompt 工程 | AI Engineer |
| **Data Engineer** | data-engineer | 数据存储和向量数据库 | Data Engineer |
| **DevOps Engineer** | devops-engineer | 基础设施和部署 | DevOps Engineer |
| **QA Engineer** | qa-engineer | 质量保证和测试 | QA Engineer |
| **Security Engineer** | security-engineer | 安全监控和成本控制 | Tech Lead, DevOps |
| **Product Manager** | product-manager | 产品需求和功能规划 | Product Manager |
| **Technical Writer** | technical-writer | 技术文档编写 | Technical Writer |

---

## 🚀 快速开始

### 步骤 1: 创建角色 Agent

由于 kiro-cli 是交互式设计，需要手动创建每个角色：

```bash
# 创建架构师角色
kiro-cli agent create

# 在交互界面中：
# Name: architect
# Description: System architecture design and technical decision-making
# Prompt: [复制 architect.json 中的 prompt 内容]
```

重复以上步骤创建所有 9 个角色。

### 步骤 2: 验证

```bash
kiro-cli agent list
```

应该看到 9 个角色 Agent。

### 步骤 3: 使用

```bash
# 切换到 DevOps 角色开始 Phase 0
kiro-cli agent use devops-engineer

# 开始对话
kiro-cli chat

# 询问
"Create docker-compose.yml for development environment"
```

---

## 💡 使用场景

### 场景 1: 架构设计

```bash
kiro-cli agent use architect
# 在 chat 中询问
"Design the overall system architecture for AI Worker Orchestration"
```

### 场景 2: 实现功能

```bash
# 后端开发人员都使用这个角色
kiro-cli agent use backend-developer
# 在 chat 中询问
"Implement AIWorker class with lifecycle management"
```

### 场景 3: AI 集成

```bash
kiro-cli agent use ai-engineer
# 在 chat 中询问
"Design prompt template for code generation tasks"
```

### 场景 4: 部署配置

```bash
kiro-cli agent use devops-engineer
# 在 chat 中询问
"Create production Kubernetes manifests"
```

### 场景 5: 编写测试

```bash
kiro-cli agent use qa-engineer
# 在 chat 中询问
"Write integration tests for Worker Manager API"
```

### 场景 6: 安全审计

```bash
kiro-cli agent use security-engineer
# 在 chat 中询问
"Implement token consumption monitoring and cost circuit breaker"
```

---

## 📖 Prompt 结构

每个 Agent 的 prompt 包含 3 个部分：

### 1. Task
角色的核心任务和职责

### 2. Requirements
具体的工作要求和标准（编号列表）

### 3. Output
期望的交付物和输出格式

**示例**:
```
## Task:
Design overall system architecture and make technical decisions.

## Requirements:
1. Create architecture diagrams using Mermaid
2. Document decisions in ADR format
3. Review critical code changes

## Output:
Architecture diagrams, ADR documents, code review comments.
```

---

## 🔧 自定义角色

### 添加新角色

创建新的 JSON 文件（如 `frontend-developer.json`）：

```json
{
  "role": "Frontend Developer",
  "description": "Web UI implementation and user experience",
  "prompt": "## Task:\nImplement web user interface...\n\n## Requirements:\n1. Use React and TypeScript\n2. Follow accessibility guidelines\n\n## Output:\nReact components, CSS modules, unit tests."
}
```

然后手动创建 Agent：
```bash
kiro-cli agent create
# Name: frontend-developer
# Description: [复制 description]
# Prompt: [复制 prompt]
```

### 修改现有角色

直接编辑对应的 JSON 文件，修改 `prompt` 字段，然后重新创建 Agent。

---

## 📚 相关文档

- **[TEAM_ORGANIZATION.md](../TEAM_ORGANIZATION.md)** - 完整团队方案（10人配置）
- **[AI_WORKER_SYSTEM_DESIGN.md](../AI_WORKER_SYSTEM_DESIGN.md)** - 技术设计文档

---

## ✅ 交付状态

**状态**: ✅ 完成  
**格式**: JSON (role + description + prompt)  
**角色数**: 9 个  
**文件大小**: ~14 KB  
**准备就绪**: 可立即使用 🚀

---

**更新日期**: 2026-03-05  
**版本**: 3.0 (Role-Based)
