# 🚀 角色 Agent 快速参考

## 📋 角色列表（9 个）

| Agent 名称 | 角色 | 使用场景 |
|-----------|------|---------|
| `architect` | 架构师 | 架构设计、技术决策、代码审查 |
| `backend-developer` | 后端开发 | 实现 API、Worker、消息总线 |
| `ai-engineer` | AI 工程师 | 模型集成、Prompt 设计、智能路由 |
| `data-engineer` | 数据工程师 | 向量数据库、记忆管理、数据管道 |
| `devops-engineer` | DevOps 工程师 | Docker、CI/CD、监控、部署 |
| `qa-engineer` | 测试工程师 | 单元测试、集成测试、性能测试 |
| `security-engineer` | 安全工程师 | 成本控制、安全审计、内容过滤 |
| `product-manager` | 产品经理 | 需求分析、用户故事、功能规划 |
| `technical-writer` | 技术文档工程师 | API 文档、用户指南、教程 |

---

## ⚡ 创建角色

由于 kiro-cli 是交互式设计，需要手动创建：

```bash
kiro-cli agent create
# 按提示输入 Name, Description, Prompt
```

对于每个角色，从对应的 JSON 文件复制内容。

---

## 🎯 按任务选择角色

| 任务 | 使用角色 |
|------|---------|
| 设计系统架构 | architect |
| 审查代码 | architect |
| 实现 Worker 引擎 | backend-developer |
| 实现 API 接口 | backend-developer |
| 实现消息总线 | backend-developer |
| 集成 Slack/Telegram | backend-developer |
| 设计 Prompt | ai-engineer |
| 模型选择和路由 | ai-engineer |
| 向量数据库配置 | data-engineer |
| 记忆检索实现 | data-engineer |
| Docker 配置 | devops-engineer |
| CI/CD 配置 | devops-engineer |
| 监控告警配置 | devops-engineer |
| 编写单元测试 | qa-engineer |
| 性能测试 | qa-engineer |
| 成本控制 | security-engineer |
| 安全审计 | security-engineer |
| 编写需求文档 | product-manager |
| 编写 API 文档 | technical-writer |

---

## 📅 按开发阶段选择角色

| 阶段 | 周 | 主要角色 | 辅助角色 |
|------|----|---------|---------| 
| **Phase 0** | 1 | devops-engineer | architect |
| **Phase 1** | 2-4 | backend-developer | architect, qa-engineer |
| **Phase 2** | 5-6 | ai-engineer | backend-developer |
| **Phase 3** | 7-8 | backend-developer | ai-engineer |
| **Phase 4** | 9-10 | backend-developer | - |
| **Phase 5** | 11-12 | data-engineer | ai-engineer |
| **Phase 6-8** | 13-17 | 所有角色 | - |

---

## 💡 使用示例

### 开始新功能

```bash
# 1. 产品经理定义需求
kiro-cli agent use product-manager
# 在 chat 中: "Write user story for Slack integration"

# 2. 架构师设计方案
kiro-cli agent use architect
# 在 chat 中: "Design architecture for Slack Bot integration"

# 3. 后端开发实现
kiro-cli agent use backend-developer
# 在 chat 中: "Implement Slack webhook handler"

# 4. 测试工程师编写测试
kiro-cli agent use qa-engineer
# 在 chat 中: "Write integration tests for Slack integration"
```

### 代码审查

```bash
kiro-cli agent use architect
# 在 chat 中: "Review PR #123: Implement AIWorker class"
```

### 部署配置

```bash
kiro-cli agent use devops-engineer
# 在 chat 中: "Create production docker-compose.yml with health checks"
```

---

## 🔄 角色 vs 团队成员映射

| 团队成员 | 主要角色 | 次要角色 |
|---------|---------|---------|
| Tech Lead | architect | backend-developer, security-engineer |
| Backend Architect | architect | backend-developer |
| Worker Engine Dev | backend-developer | - |
| API Gateway Dev | backend-developer | - |
| Message Bus Dev | backend-developer | - |
| AI Engineer | ai-engineer | - |
| Data Engineer | data-engineer | - |
| DevOps Engineer | devops-engineer | security-engineer |
| QA Engineer | qa-engineer | - |
| Product Manager | product-manager | - |
| Technical Writer | technical-writer | - |

---

**快速开始**: 运行 `.\create_agents.ps1` 创建所有角色！
