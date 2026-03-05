# AI Worker 编排系统 - 技术设计文档

**项目名称**: AI-CLI Worker Orchestration System  
**版本**: 1.0  
**日期**: 2026-03-05  
**基于分支**: Master (Python)

---

## 目录

1. [项目概述](#1-项目概述)
2. [功能需求](#2-功能需求)
3. [技术选型](#3-技术选型)
4. [系统架构](#4-系统架构)
5. [核心模块设计](#5-核心模块设计)
6. [数据模型](#6-数据模型)
7. [API 设计](#7-api-设计)
8. [实施方案](#8-实施方案)
9. [风险评估](#9-风险评估)
10. [附录](#10-附录)

---

## 1. 项目概述

### 1.1 背景

AI-CLI 当前是一个终端启动器，帮助用户快速启动各种 AI 编程工具。本项目旨在将其升级为**智能 AI 工作者编排系统**，支持：

- 通过 IM/Email 等渠道远程触发开发任务
- 自动分析任务并分配给合适的 AI 工具
- 管理多个并发运行的 AI Agent 实例
- 智能路由用户消息到正确的工作者
- 工作者之间协作完成复杂任务

### 1.2 目标用户

- **个人开发者**: 通过 Slack/Telegram 远程触发代码任务
- **开发团队**: 集中管理多个项目的 AI 辅助开发
- **企业**: 构建内部 AI DevOps 平台

### 1.3 核心价值

- **自动化**: 从消息到代码变更的全自动流程
- **智能化**: AI 理解上下文，智能路由和任务分解
- **可扩展**: 支持任意 AI CLI 工具和项目
- **可观测**: 完整的日志、监控和审计

---

## 2. 功能需求

### 2.1 核心功能

#### F1: 多渠道消息接口

**需求描述**: 接收来自多种渠道的消息，统一处理

**功能点**:
- 支持 Slack、Telegram、Discord、Email、HTTP API
- 消息格式标准化
- 用户身份认证和权限管理
- 消息队列缓冲（防止丢失）

**示例**:
```
用户 (Slack): "@ai-bot 请用 kiro 为 AI-CLI 项目增加自动升级功能"
系统: 收到消息 → 验证用户 → 入队 → 返回确认
```

#### F2: 智能任务分析

**需求描述**: 使用 AI 大模型分析用户指令，提取关键信息

**功能点**:
- 提取工具名称（kiro-cli, claude, aider 等）
- 提取项目名称（AI-CLI, MyProject 等）
- 提取任务描述（增加功能、修复 bug、重构代码）
- 判断是否需要多工具协作
- 结合历史会话上下文理解意图

**示例**:
```python
输入: "请用 kiro 为 AI-CLI 项目增加自动升级功能"
输出: {
    "tool": "kiro-cli",
    "project": "AI-CLI",
    "task": "增加自动升级功能",
    "type": "feature",
    "multi_worker": false
}
```

#### F3: 专业项目管理模块

**需求描述**: 扩展现有项目管理，支持企业级功能

**功能点**:
- 项目元数据管理（语言、框架、依赖）
- Git Worktree 智能管理
- 项目模板和脚手架
- 依赖分析和健康检查
- 项目分组和标签
- 访问权限控制

**数据结构**:
```python
class Project:
    id: str
    name: str
    path: str
    git_repo: str
    worktrees: List[Worktree]
    metadata: ProjectMetadata  # 语言、框架、依赖
    tags: List[str]
    permissions: Dict[str, List[str]]  # user_id -> [read, write, admin]
```

#### F4: 专业 AI 工具管理模块

**需求描述**: 扩展工具管理，支持版本控制和健康监控

**功能点**:
- 工具注册表（本地 + 远程）
- 版本管理和自动更新
- 健康检查和性能监控
- 工具能力描述（支持的任务类型）
- 安装/卸载自动化
- 工具使用统计

**数据结构**:
```python
class Tool:
    name: str
    version: str
    capabilities: List[str]  # ["code_review", "refactor", "test_gen"]
    health_status: HealthStatus
    last_check: datetime
    usage_stats: UsageStats
```

#### F5: AI 工作者管理模块 ⭐核心

**需求描述**: 管理所有运行中的 AI Agent 实例

**功能点**:
- 工作者生命周期管理（创建、运行、暂停、销毁）
- 进程管道化 I/O（stdin/stdout/stderr）
- 工作者状态监控（运行中、等待输入、已完成）
- 资源限制（CPU、内存、并发数）
- 工作者隔离（独立工作目录和环境变量）
- 自动重启和故障恢复

**工作者状态机**:
```
CREATED → STARTING → RUNNING → WAITING_INPUT → RUNNING → COMPLETED
                  ↓                                    ↓
                ERROR ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ERROR
```

#### F6: 智能消息路由

**需求描述**: 根据上下文将用户消息路由到正确的工作者

**功能点**:
- 会话上下文跟踪（用户 + 渠道 + 工作者）
- 智能匹配算法（基于历史对话）
- 工作者询问响应匹配（优先级最高）
- 新任务 vs 继续对话判断
- 多工作者场景的消歧

**路由逻辑**:
```python
if worker_waiting_for_input(user_id):
    route_to_existing_worker()
elif is_new_task(message, context):
    create_new_worker()
else:
    route_to_recent_worker()
```

#### F7: 工作者间通讯机制

**需求描述**: 支持多个工作者协作完成复杂任务

**功能点**:
- 消息总线（发布/订阅模式）
- 工作者间数据共享（共享内存/Redis）
- 任务依赖管理（DAG 有向无环图）
- 协作协议（请求/响应、通知）
- 死锁检测和预防

**通讯模式**:
```python
# 工作者 A 请求工作者 B 的输出
worker_a.request(worker_b, "获取数据库 schema")
worker_b.respond(worker_a, schema_data)

# 广播通知
worker_a.broadcast("任务完成", {"status": "success"})
```

#### F8: 会话日志和持久化记忆

**需求描述**: 完整记录所有交互，支持长期记忆检索

**功能点**:
- 结构化日志（JSON 格式）
- 会话历史存储（用户、工作者、消息、时间戳）
- 向量化记忆存储（语义搜索）
- 记忆检索和注入（RAG 模式）
- 日志归档和清理策略
- 审计和合规支持

**记忆层次**:
```
短期记忆: Redis (当前会话，TTL 24h)
中期记忆: PostgreSQL (30 天内会话)
长期记忆: 向量数据库 (语义检索，永久)
```

---

## 3. 技术选型

### 3.1 核心技术栈

| 组件 | 技术选型 | 理由 |
|------|---------|------|
| **编程语言** | Python 3.10+ | 异步支持、AI 生态成熟 |
| **Web 框架** | FastAPI | 高性能、异步、自动文档 |
| **异步运行时** | asyncio | 标准库、I/O 多路复用 |
| **进程管理** | subprocess + asyncio | 管道化 I/O、非阻塞 |
| **AI 模型接口** | LiteLLM | 统一多模型接口 |
| **消息队列** | Redis Streams | 轻量、持久化、消费组 |
| **关系数据库** | PostgreSQL | 事务、JSON 支持 |
| **缓存** | Redis | 高性能、会话状态 |
| **向量数据库** | Qdrant | 开源、高性能、易部署 |
| **实时通信** | WebSocket (FastAPI) | 双向、低延迟 |
| **任务调度** | APScheduler | 轻量、灵活 |
| **日志** | structlog | 结构化、性能好 |
| **监控** | Prometheus + Grafana | 业界标准 |

### 3.2 AI 模型选型

| 用途 | 模型 | 理由 |
|------|------|------|
| **任务分析** | GPT-4o-mini / Claude 3.5 Haiku | 快速、便宜、准确 |
| **消息路由** | GPT-4o-mini | 低延迟、成本低 |
| **记忆检索** | text-embedding-3-small | 高质量嵌入、便宜 |
| **复杂推理** | Claude 3.5 Sonnet | 需要时升级 |

### 3.3 第三方集成

| 集成 | SDK/库 | 用途 |
|------|--------|------|
| **Slack** | slack-sdk | Slack Bot 集成 |
| **Telegram** | python-telegram-bot | Telegram Bot |
| **Email** | aiosmtplib + aiohttp | IMAP/SMTP |
| **GitHub** | PyGithub | Webhook、PR 评论 |
| **Docker** | docker-py | 容器化部署 |

### 3.4 部署架构

```
┌─────────────────────────────────────────────────────┐
│                   Load Balancer                      │
│                    (Nginx/Caddy)                     │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼────────┐   ┌────────▼───────┐
│  FastAPI App   │   │  FastAPI App   │  (多实例)
│  (Worker Mgr)  │   │  (Worker Mgr)  │
└───────┬────────┘   └────────┬───────┘
        │                     │
        └──────────┬──────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
┌───▼───┐   ┌─────▼─────┐   ┌───▼────┐
│ Redis │   │PostgreSQL │   │ Qdrant │
│(Queue)│   │  (Logs)   │   │(Memory)│
└───────┘   └───────────┘   └────────┘
```

---

## 4. 系统架构

### 4.1 整体架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        用户层                                │
│  Slack │ Telegram │ Email │ Web UI │ HTTP API │ CLI         │
└────────┬────────────────────────────────────────────────────┘
         │
┌────────▼────────────────────────────────────────────────────┐
│                      网关层 (Gateway)                        │
│  • 消息标准化  • 认证鉴权  • 限流  • 消息队列               │
└────────┬────────────────────────────────────────────────────┘
         │
┌────────▼────────────────────────────────────────────────────┐
│                   智能路由层 (Router)                        │
│  • AI 任务分析  • 上下文管理  • 工作者匹配  • 任务分解      │
└────────┬────────────────────────────────────────────────────┘
         │
┌────────▼────────────────────────────────────────────────────┐
│                 工作者管理层 (Worker Manager)                │
│  • 工作者生命周期  • 进程管理  • I/O 复用  • 资源控制       │
└────────┬────────────────────────────────────────────────────┘
         │
┌────────▼────────────────────────────────────────────────────┐
│                   工作者层 (AI Workers)                      │
│  Worker 1 (kiro-cli)  │  Worker 2 (claude)  │  Worker N     │
│  ├─ Project A         │  ├─ Project B       │  ├─ ...       │
│  └─ Worktree main     │  └─ Worktree dev    │  └─ ...       │
└────────┬────────────────────────────────────────────────────┘
         │
┌────────▼────────────────────────────────────────────────────┐
│                   基础设施层 (Infrastructure)                │
│  • 项目管理  • 工具管理  • 平台适配  • Git 操作             │
└─────────────────────────────────────────────────────────────┘
         │
┌────────▼────────────────────────────────────────────────────┐
│                    数据层 (Data Layer)                       │
│  PostgreSQL (会话/日志)  │  Redis (状态/队列)  │  Qdrant (记忆) │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 数据流图

#### 场景 1: 新任务创建

```
用户消息 → Gateway → 消息队列 → Router (AI分析) → 检查工具/项目
                                      ↓
                              WorkerManager.create_worker()
                                      ↓
                              启动子进程 (kiro-cli --no-interactive)
                                      ↓
                              管道化 stdin/stdout → 实时流式返回
                                      ↓
                              输出 → Gateway → 用户渠道
```

#### 场景 2: 继续对话

```
用户回复 → Gateway → Router (AI匹配) → 找到等待输入的 Worker
                                      ↓
                              Worker.send_input(message)
                                      ↓
                              输出 → Gateway → 用户渠道
```

#### 场景 3: 多工作者协作

```
用户: "用 kiro 分析代码，用 claude 重构"
         ↓
Router (AI分析) → 拆分为 2 个任务
         ↓
    ┌────┴────┐
Worker A    Worker B
(kiro)      (claude)
    │          │
    └────┬─────┘
         ↓
  消息总线 (Redis Pub/Sub)
         ↓
Worker A 完成 → 通知 Worker B → Worker B 开始
```

---

## 5. 核心模块设计

### 5.1 模块结构

```
ai_cli/
├── server/                    # 服务端模块（新增）
│   ├── __init__.py
│   ├── api.py                # FastAPI 应用
│   ├── websocket.py          # WebSocket 处理
│   ├── gateway/              # 消息网关
│   │   ├── __init__.py
│   │   ├── base.py           # 抽象基类
│   │   ├── slack.py          # Slack 集成
│   │   ├── telegram.py       # Telegram 集成
│   │   ├── email.py          # Email 集成
│   │   └── http.py           # HTTP API
│   ├── router.py             # 智能路由器
│   └── auth.py               # 认证鉴权
│
├── core/                      # 核心模块（扩展）
│   ├── worker_manager.py     # 工作者管理器（新增）⭐
│   ├── ai_worker.py          # AI 工作者实例（新增）⭐
│   ├── io_multiplexer.py     # I/O 多路复用（新增）
│   ├── message_bus.py        # 消息总线（新增）
│   ├── projects.py           # 项目管理（扩展）
│   ├── tools.py              # 工具管理（扩展）
│   ├── git.py                # Git 操作（已有）
│   └── installer.py          # 安装器（已有）
│
├── ai/                        # AI 模块（新增）
│   ├── __init__.py
│   ├── task_analyzer.py      # 任务分析器
│   ├── context_manager.py    # 上下文管理
│   ├── memory.py             # 记忆管理
│   └── embeddings.py         # 向量化
│
├── models/                    # 数据模型（扩展）
│   ├── __init__.py
│   ├── worker.py             # 工作者模型
│   ├── session.py            # 会话模型
│   ├── message.py            # 消息模型
│   ├── project.py            # 项目模型（扩展）
│   └── tool.py               # 工具模型（扩展）
│
├── db/                        # 数据库（新增）
│   ├── __init__.py
│   ├── postgres.py           # PostgreSQL 操作
│   ├── redis.py              # Redis 操作
│   └── qdrant.py             # Qdrant 操作
│
├── monitoring/                # 监控（新增）
│   ├── __init__.py
│   ├── metrics.py            # 指标收集
│   ├── logging.py            # 日志配置
│   └── health.py             # 健康检查
│
├── platform/                  # 平台适配（已有）
│   ├── base.py
│   ├── windows.py
│   ├── linux.py
│   └── macos.py
│
├── ui/                        # UI（已有，保留 CLI）
│   ├── menu.py
│   ├── input.py
│   └── theme.py
│
├── config.py                  # 配置管理（扩展）
├── utils.py                   # 工具函数（已有）
└── cli.py                     # CLI 入口（已有）
```

### 5.2 核心类设计

#### 5.2.1 AIWorker (AI 工作者)

```python
# ai_cli/core/ai_worker.py
from enum import Enum
from typing import Optional, AsyncIterator
import asyncio

class WorkerStatus(Enum):
    CREATED = "created"
    STARTING = "starting"
    RUNNING = "running"
    WAITING_INPUT = "waiting_input"
    COMPLETED = "completed"
    ERROR = "error"

class AIWorker:
    """单个 AI Agent 实例"""
    
    def __init__(
        self,
        worker_id: str,
        tool: str,
        project_path: str,
        worktree: Optional[str],
        task: str,
        user_id: str,
        channel: str
    ):
        self.worker_id = worker_id
        self.tool = tool
        self.project_path = project_path
        self.worktree = worktree
        self.task = task
        self.user_id = user_id
        self.channel = channel
        
        self.status = WorkerStatus.CREATED
        self.process: Optional[asyncio.subprocess.Process] = None
        self.created_at = datetime.utcnow()
        self.last_activity = datetime.utcnow()
        
    async def start(self) -> bool:
        """启动工作者进程"""
        self.status = WorkerStatus.STARTING
        
        # 构建命令
        cmd = self._build_command()
        
        # 启动子进程
        self.process = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=self.project_path
        )
        
        # 发送初始任务
        await self.send_input(self.task)
        self.status = WorkerStatus.RUNNING
        return True
    
    async def send_input(self, message: str):
        """发送输入到工作者"""
        if self.process and self.process.stdin:
            self.process.stdin.write(f"{message}\n".encode())
            await self.process.stdin.drain()
            self.last_activity = datetime.utcnow()
    
    async def read_output(self) -> AsyncIterator[str]:
        """流式读取输出"""
        while self.process and self.process.stdout:
            line = await self.process.stdout.readline()
            if not line:
                break
            self.last_activity = datetime.utcnow()
            yield line.decode()
    
    async def terminate(self):
        """终止工作者"""
        if self.process:
            self.process.terminate()
            await self.process.wait()
        self.status = WorkerStatus.COMPLETED
    
    def _build_command(self) -> list:
        """构建启动命令"""
        # 基于工具类型构建命令
        if self.tool == "kiro-cli":
            return ["kiro-cli", "chat", "--no-interactive", "--trust-all-tools"]
        elif self.tool == "claude":
            return ["claude", "--print", "--auto-edit"]
        # ... 其他工具
```

#### 5.2.2 WorkerManager (工作者管理器)

```python
# ai_cli/core/worker_manager.py
from typing import Dict, List, Optional
import asyncio

class WorkerManager:
    """管理所有 AI 工作者实例"""
    
    def __init__(self, max_workers: int = 10):
        self.workers: Dict[str, AIWorker] = {}
        self.max_workers = max_workers
        self.lock = asyncio.Lock()
    
    async def create_worker(
        self,
        tool: str,
        project: str,
        task: str,
        user_id: str,
        channel: str
    ) -> str:
        """创建新工作者"""
        async with self.lock:
            if len(self.workers) >= self.max_workers:
                raise Exception("达到最大工作者数量")
            
            worker_id = self._generate_id()
            worker = AIWorker(
                worker_id, tool, project, None, task, user_id, channel
            )
            
            await worker.start()
            self.workers[worker_id] = worker
            
            # 启动输出监听
            asyncio.create_task(self._monitor_worker(worker_id))
            
            return worker_id
    
    async def send_to_worker(self, worker_id: str, message: str):
        """发送消息到工作者"""
        if worker_id not in self.workers:
            raise Exception(f"工作者 {worker_id} 不存在")
        
        await self.workers[worker_id].send_input(message)
    
    async def get_worker_by_user(self, user_id: str) -> Optional[AIWorker]:
        """获取用户的活跃工作者"""
        for worker in self.workers.values():
            if worker.user_id == user_id and worker.status == WorkerStatus.WAITING_INPUT:
                return worker
        return None
    
    async def cleanup_worker(self, worker_id: str):
        """清理工作者"""
        if worker_id in self.workers:
            await self.workers[worker_id].terminate()
            del self.workers[worker_id]
    
    async def _monitor_worker(self, worker_id: str):
        """监控工作者输出"""
        worker = self.workers[worker_id]
        
        async for output in worker.read_output():
            # 保存到日志
            await log_worker_output(worker_id, output)
            
            # 发送到用户渠道
            await send_to_channel(worker.channel, worker.user_id, output)
            
            # 检测是否等待输入
            if is_waiting_for_input(output):
                worker.status = WorkerStatus.WAITING_INPUT
    
    def _generate_id(self) -> str:
        """生成唯一 ID"""
        import uuid
        return str(uuid.uuid4())[:8]
```


#### 5.2.3 IntelligentRouter (智能路由器)

```python
# ai_cli/server/router.py
from ai_cli.ai.task_analyzer import TaskAnalyzer
from ai_cli.ai.context_manager import ContextManager

class IntelligentRouter:
    """智能消息路由器"""
    
    def __init__(self, worker_manager: WorkerManager):
        self.worker_manager = worker_manager
        self.task_analyzer = TaskAnalyzer()
        self.context_manager = ContextManager()
    
    async def route_message(
        self,
        user_id: str,
        channel: str,
        message: str
    ) -> dict:
        """路由用户消息"""
        
        # 1. 获取会话上下文
        context = await self.context_manager.get_context(user_id, channel)
        
        # 2. 检查是否有等待输入的工作者
        waiting_worker = await self.worker_manager.get_worker_by_user(user_id)
        
        if waiting_worker:
            # 优先路由到等待输入的工作者
            await self.worker_manager.send_to_worker(
                waiting_worker.worker_id, message
            )
            return {
                "action": "continue",
                "worker_id": waiting_worker.worker_id
            }
        
        # 3. AI 分析任务
        analysis = await self.task_analyzer.analyze(message, context)
        
        # 4. 判断是新任务还是继续对话
        if analysis["is_new_task"]:
            # 验证工具和项目
            if not await self._validate_tool(analysis["tool"]):
                return {"error": "工具不支持或未安装"}
            
            if not await self._validate_project(analysis["project"]):
                return {"error": "项目不存在"}
            
            # 创建新工作者
            worker_id = await self.worker_manager.create_worker(
                tool=analysis["tool"],
                project=analysis["project"],
                task=analysis["task"],
                user_id=user_id,
                channel=channel
            )
            
            # 更新上下文
            await self.context_manager.add_worker(user_id, worker_id)
            
            return {
                "action": "created",
                "worker_id": worker_id,
                "analysis": analysis
            }
        else:
            # 路由到最近的工作者
            recent_worker = await self.context_manager.get_recent_worker(user_id)
            if recent_worker:
                await self.worker_manager.send_to_worker(recent_worker, message)
                return {"action": "routed", "worker_id": recent_worker}
            else:
                return {"error": "无法确定目标工作者，请明确指定"}
    
    async def _validate_tool(self, tool_name: str) -> bool:
        """验证工具是否可用"""
        from ai_cli.core.tools import ToolDetector
        detector = ToolDetector()
        tools = detector.detect_tools()
        return any(t.name == tool_name for t in tools)
    
    async def _validate_project(self, project_name: str) -> bool:
        """验证项目是否存在"""
        from ai_cli.core.projects import ProjectManager
        manager = ProjectManager()
        return manager.project_exists(project_name)
```

#### 5.2.4 TaskAnalyzer (任务分析器)

```python
# ai_cli/ai/task_analyzer.py
from litellm import acompletion
import json

class TaskAnalyzer:
    """使用 AI 分析用户任务"""
    
    SYSTEM_PROMPT = """你是一个任务分析助手。分析用户消息，提取以下信息：
1. tool: AI 工具名称（kiro-cli, claude, aider, cursor-agent 等）
2. project: 项目名称
3. task: 具体任务描述
4. is_new_task: 是否是新任务（true/false）
5. multi_worker: 是否需要多个工作者协作（true/false）
6. workers: 如果需要多工作者，列出每个工作者的配置

输出 JSON 格式。

示例：
输入: "请用 kiro 为 AI-CLI 项目增加自动升级功能"
输出: {
    "tool": "kiro-cli",
    "project": "AI-CLI",
    "task": "增加自动升级功能",
    "is_new_task": true,
    "multi_worker": false
}

输入: "好的"（上下文：工作者询问是否继续）
输出: {
    "is_new_task": false,
    "response_to_worker": true
}
"""
    
    async def analyze(self, message: str, context: dict) -> dict:
        """分析任务"""
        
        # 构建提示
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": f"上下文: {json.dumps(context, ensure_ascii=False)}\n\n用户消息: {message}"}
        ]
        
        # 调用 AI
        response = await acompletion(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.1
        )
        
        # 解析结果
        result = json.loads(response.choices[0].message.content)
        return result
```

#### 5.2.5 MessageBus (消息总线)

```python
# ai_cli/core/message_bus.py
import asyncio
from typing import Callable, Dict, List
import redis.asyncio as redis

class MessageBus:
    """工作者间消息总线"""
    
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)
        self.subscribers: Dict[str, List[Callable]] = {}
    
    async def publish(self, channel: str, message: dict):
        """发布消息"""
        await self.redis.publish(
            channel,
            json.dumps(message)
        )
    
    async def subscribe(self, channel: str, callback: Callable):
        """订阅频道"""
        if channel not in self.subscribers:
            self.subscribers[channel] = []
        self.subscribers[channel].append(callback)
        
        # 启动监听
        asyncio.create_task(self._listen(channel))
    
    async def _listen(self, channel: str):
        """监听频道"""
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(channel)
        
        async for message in pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                for callback in self.subscribers[channel]:
                    await callback(data)
    
    async def worker_request(
        self,
        from_worker: str,
        to_worker: str,
        request: str
    ) -> str:
        """工作者间请求/响应"""
        request_id = str(uuid.uuid4())[:8]
        
        # 发布请求
        await self.publish(f"worker:{to_worker}:requests", {
            "request_id": request_id,
            "from": from_worker,
            "content": request
        })
        
        # 等待响应（超时 60s）
        response = await self._wait_for_response(request_id, timeout=60)
        return response
    
    async def _wait_for_response(self, request_id: str, timeout: int) -> str:
        """等待响应"""
        # 实现响应等待逻辑
        pass
```

#### 5.2.6 ContextManager (上下文管理器)

```python
# ai_cli/ai/context_manager.py
from ai_cli.db.redis import RedisClient
from ai_cli.db.postgres import PostgresClient

class ContextManager:
    """会话上下文管理"""
    
    def __init__(self):
        self.redis = RedisClient()
        self.postgres = PostgresClient()
    
    async def get_context(self, user_id: str, channel: str) -> dict:
        """获取用户会话上下文"""
        
        # 1. 从 Redis 获取短期上下文（当前会话）
        short_term = await self.redis.get(f"context:{user_id}:{channel}")
        
        # 2. 从 PostgreSQL 获取中期上下文（最近 10 条消息）
        recent_messages = await self.postgres.get_recent_messages(
            user_id, channel, limit=10
        )
        
        # 3. 从向量数据库检索长期记忆（相关历史）
        from ai_cli.ai.memory import MemoryManager
        memory = MemoryManager()
        relevant_memories = await memory.search(
            user_id, recent_messages[-1]["content"], top_k=3
        )
        
        return {
            "short_term": short_term or {},
            "recent_messages": recent_messages,
            "relevant_memories": relevant_memories,
            "active_workers": await self.get_active_workers(user_id)
        }
    
    async def add_worker(self, user_id: str, worker_id: str):
        """添加工作者到上下文"""
        key = f"context:{user_id}:workers"
        await self.redis.sadd(key, worker_id)
        await self.redis.expire(key, 86400)  # 24h TTL
    
    async def get_active_workers(self, user_id: str) -> List[str]:
        """获取用户的活跃工作者"""
        key = f"context:{user_id}:workers"
        return await self.redis.smembers(key)
    
    async def get_recent_worker(self, user_id: str) -> Optional[str]:
        """获取最近使用的工作者"""
        workers = await self.get_active_workers(user_id)
        if not workers:
            return None
        # 返回最近活跃的
        return workers[0]  # 简化实现
```

#### 5.2.7 MemoryManager (记忆管理器)

```python
# ai_cli/ai/memory.py
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from litellm import aembedding

class MemoryManager:
    """持久化记忆管理"""
    
    def __init__(self):
        self.qdrant = QdrantClient(url="http://localhost:6333")
        self.collection = "ai_cli_memories"
        self._ensure_collection()
    
    def _ensure_collection(self):
        """确保集合存在"""
        try:
            self.qdrant.get_collection(self.collection)
        except:
            self.qdrant.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
            )
    
    async def store(
        self,
        user_id: str,
        content: str,
        metadata: dict
    ):
        """存储记忆"""
        
        # 生成向量
        embedding = await self._embed(content)
        
        # 存储到 Qdrant
        point_id = str(uuid.uuid4())
        self.qdrant.upsert(
            collection_name=self.collection,
            points=[
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "user_id": user_id,
                        "content": content,
                        "timestamp": datetime.utcnow().isoformat(),
                        **metadata
                    }
                )
            ]
        )
    
    async def search(
        self,
        user_id: str,
        query: str,
        top_k: int = 5
    ) -> List[dict]:
        """检索相关记忆"""
        
        # 生成查询向量
        query_vector = await self._embed(query)
        
        # 搜索
        results = self.qdrant.search(
            collection_name=self.collection,
            query_vector=query_vector,
            query_filter={
                "must": [{"key": "user_id", "match": {"value": user_id}}]
            },
            limit=top_k
        )
        
        return [
            {
                "content": r.payload["content"],
                "score": r.score,
                "metadata": r.payload
            }
            for r in results
        ]
    
    async def _embed(self, text: str) -> List[float]:
        """生成文本向量"""
        response = await aembedding(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0]["embedding"]
```

---

## 6. 数据模型

### 6.1 数据库 Schema

#### PostgreSQL 表结构

```sql
-- 用户表
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    permissions JSONB DEFAULT '{}'::jsonb
);

-- 会话表
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    channel VARCHAR(50) NOT NULL,  -- slack, telegram, email, api
    channel_user_id VARCHAR(255),  -- 渠道内的用户 ID
    started_at TIMESTAMP DEFAULT NOW(),
    ended_at TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- 消息表
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES sessions(id),
    worker_id VARCHAR(50),
    direction VARCHAR(10) NOT NULL,  -- inbound, outbound
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

-- 工作者表
CREATE TABLE workers (
    id VARCHAR(50) PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    session_id UUID REFERENCES sessions(id),
    tool VARCHAR(50) NOT NULL,
    project VARCHAR(255) NOT NULL,
    worktree VARCHAR(255),
    task TEXT NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    exit_code INTEGER,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- 工作者日志表
CREATE TABLE worker_logs (
    id BIGSERIAL PRIMARY KEY,
    worker_id VARCHAR(50) REFERENCES workers(id),
    stream VARCHAR(10) NOT NULL,  -- stdout, stderr
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW()
);

-- 项目表（扩展）
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    path TEXT NOT NULL,
    git_repo TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,  -- 语言、框架、依赖
    tags TEXT[],
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 工具表（扩展）
CREATE TABLE tools (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) UNIQUE NOT NULL,
    version VARCHAR(50),
    capabilities TEXT[],
    health_status VARCHAR(20),
    last_check TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 工作者通讯表
CREATE TABLE worker_communications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    from_worker VARCHAR(50) REFERENCES workers(id),
    to_worker VARCHAR(50) REFERENCES workers(id),
    message_type VARCHAR(20) NOT NULL,  -- request, response, notify
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

-- 索引
CREATE INDEX idx_messages_session ON messages(session_id, timestamp);
CREATE INDEX idx_workers_user ON workers(user_id, created_at);
CREATE INDEX idx_worker_logs_worker ON worker_logs(worker_id, timestamp);
CREATE INDEX idx_sessions_user ON sessions(user_id, started_at);
```

#### Redis 数据结构

```python
# 会话上下文（短期）
context:{user_id}:{channel} → Hash
    {
        "last_message": "...",
        "last_worker": "worker_123",
        "conversation_state": "waiting_response"
    }
    TTL: 24h

# 用户活跃工作者
context:{user_id}:workers → Set
    ["worker_123", "worker_456"]
    TTL: 24h

# 工作者状态
worker:{worker_id}:status → String
    "running" | "waiting_input" | "completed"
    TTL: 24h

# 消息队列
queue:incoming_messages → Stream
    {
        "user_id": "...",
        "channel": "slack",
        "message": "...",
        "timestamp": "..."
    }

# 工作者输出缓冲
worker:{worker_id}:output → List
    ["输出行1", "输出行2", ...]
    TTL: 1h
```

### 6.2 Python 数据模型

```python
# ai_cli/models/worker.py
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class WorkerStatus(str, Enum):
    CREATED = "created"
    STARTING = "starting"
    RUNNING = "running"
    WAITING_INPUT = "waiting_input"
    COMPLETED = "completed"
    ERROR = "error"

class WorkerModel(BaseModel):
    id: str
    user_id: str
    session_id: str
    tool: str
    project: str
    worktree: Optional[str]
    task: str
    status: WorkerStatus
    created_at: datetime
    completed_at: Optional[datetime]
    exit_code: Optional[int]
    metadata: dict = {}

# ai_cli/models/message.py
class MessageDirection(str, Enum):
    INBOUND = "inbound"   # 用户 → 系统
    OUTBOUND = "outbound"  # 系统 → 用户

class MessageModel(BaseModel):
    id: str
    session_id: str
    worker_id: Optional[str]
    direction: MessageDirection
    content: str
    timestamp: datetime
    metadata: dict = {}

# ai_cli/models/session.py
class SessionModel(BaseModel):
    id: str
    user_id: str
    channel: str
    channel_user_id: str
    started_at: datetime
    ended_at: Optional[datetime]
    metadata: dict = {}
```

---

## 7. API 设计

### 7.1 REST API

#### 端点列表

```python
# ai_cli/server/api.py
from fastapi import FastAPI, WebSocket, HTTPException
from pydantic import BaseModel

app = FastAPI(title="AI-CLI Worker System", version="1.0")

# ============ 任务管理 ============

@app.post("/api/v1/tasks")
async def create_task(request: TaskRequest) -> TaskResponse:
    """创建新任务"""
    pass

@app.get("/api/v1/tasks/{task_id}")
async def get_task(task_id: str) -> TaskResponse:
    """获取任务状态"""
    pass

@app.post("/api/v1/tasks/{task_id}/input")
async def send_input(task_id: str, input: InputRequest):
    """发送输入到任务"""
    pass

@app.delete("/api/v1/tasks/{task_id}")
async def cancel_task(task_id: str):
    """取消任务"""
    pass

# ============ 工作者管理 ============

@app.get("/api/v1/workers")
async def list_workers(user_id: Optional[str] = None) -> List[WorkerModel]:
    """列出工作者"""
    pass

@app.get("/api/v1/workers/{worker_id}")
async def get_worker(worker_id: str) -> WorkerModel:
    """获取工作者详情"""
    pass

@app.get("/api/v1/workers/{worker_id}/logs")
async def get_worker_logs(worker_id: str, limit: int = 100) -> List[str]:
    """获取工作者日志"""
    pass

@app.post("/api/v1/workers/{worker_id}/terminate")
async def terminate_worker(worker_id: str):
    """终止工作者"""
    pass

# ============ 项目管理 ============

@app.get("/api/v1/projects")
async def list_projects() -> List[ProjectModel]:
    """列出项目"""
    pass

@app.post("/api/v1/projects")
async def create_project(project: ProjectCreate) -> ProjectModel:
    """创建项目"""
    pass

@app.get("/api/v1/projects/{project_id}")
async def get_project(project_id: str) -> ProjectModel:
    """获取项目详情"""
    pass

@app.put("/api/v1/projects/{project_id}")
async def update_project(project_id: str, project: ProjectUpdate):
    """更新项目"""
    pass

# ============ 工具管理 ============

@app.get("/api/v1/tools")
async def list_tools() -> List[ToolModel]:
    """列出工具"""
    pass

@app.post("/api/v1/tools/{tool_name}/install")
async def install_tool(tool_name: str):
    """安装工具"""
    pass

@app.get("/api/v1/tools/{tool_name}/health")
async def check_tool_health(tool_name: str) -> HealthStatus:
    """检查工具健康状态"""
    pass

# ============ 会话管理 ============

@app.get("/api/v1/sessions/{session_id}/history")
async def get_session_history(session_id: str) -> List[MessageModel]:
    """获取会话历史"""
    pass

@app.get("/api/v1/sessions/{session_id}/context")
async def get_session_context(session_id: str) -> dict:
    """获取会话上下文"""
    pass

# ============ 记忆管理 ============

@app.post("/api/v1/memory/search")
async def search_memory(query: MemorySearchRequest) -> List[MemoryResult]:
    """搜索记忆"""
    pass

@app.get("/api/v1/memory/{user_id}")
async def get_user_memories(user_id: str, limit: int = 50) -> List[MemoryResult]:
    """获取用户记忆"""
    pass

# ============ WebSocket ============

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket 实时通信"""
    await websocket.accept()
    
    try:
        while True:
            # 接收用户消息
            data = await websocket.receive_json()
            
            # 路由消息
            result = await router.route_message(
                user_id, "websocket", data["message"]
            )
            
            # 返回结果
            await websocket.send_json(result)
            
    except WebSocketDisconnect:
        pass
```

### 7.2 请求/响应模型

```python
# ai_cli/models/api.py

class TaskRequest(BaseModel):
    message: str
    channel: str = "api"
    user_id: str
    metadata: dict = {}

class TaskResponse(BaseModel):
    task_id: str
    worker_id: str
    status: str
    analysis: dict
    created_at: datetime

class InputRequest(BaseModel):
    content: str

class MemorySearchRequest(BaseModel):
    user_id: str
    query: str
    top_k: int = 5

class MemoryResult(BaseModel):
    content: str
    score: float
    timestamp: datetime
    metadata: dict
```


---

## 8. 实施方案

### 8.1 开发阶段

#### 阶段 0: 准备工作（1 周）

**任务**:
- [ ] 环境搭建（PostgreSQL, Redis, Qdrant）
- [ ] 依赖管理（更新 pyproject.toml）
- [ ] 数据库迁移工具（Alembic）
- [ ] 开发环境配置（Docker Compose）

**交付物**:
- `docker-compose.yml`
- `alembic/` 迁移脚本
- `pyproject.toml` 更新

#### 阶段 1: 核心工作者管理（3 周）

**任务**:
- [ ] 实现 `AIWorker` 类（进程管理、I/O 管道）
- [ ] 实现 `WorkerManager` 类（生命周期管理）
- [ ] 实现 `IOMultiplexer` 类（异步 I/O）
- [ ] 单元测试（覆盖率 > 80%）

**关键代码**:
```python
# ai_cli/core/ai_worker.py
# ai_cli/core/worker_manager.py
# ai_cli/core/io_multiplexer.py
# tests/test_worker.py
```

**验收标准**:
- 能启动 kiro-cli 子进程并捕获输出
- 能发送输入到子进程
- 能同时管理 10+ 工作者
- 工作者崩溃不影响管理器

#### 阶段 2: 智能路由和任务分析（2 周）

**任务**:
- [ ] 实现 `TaskAnalyzer` 类（AI 任务分析）
- [ ] 实现 `IntelligentRouter` 类（消息路由）
- [ ] 实现 `ContextManager` 类（上下文管理）
- [ ] 集成 LiteLLM（多模型支持）

**关键代码**:
```python
# ai_cli/ai/task_analyzer.py
# ai_cli/server/router.py
# ai_cli/ai/context_manager.py
```

**验收标准**:
- AI 能准确提取工具、项目、任务
- 能区分新任务 vs 继续对话
- 能正确路由到等待输入的工作者
- 上下文检索准确率 > 90%

#### 阶段 3: 消息网关（2 周）

**任务**:
- [ ] 实现 Slack 集成
- [ ] 实现 Telegram 集成
- [ ] 实现 Email 集成
- [ ] 实现 HTTP API
- [ ] 消息队列（Redis Streams）

**关键代码**:
```python
# ai_cli/server/gateway/slack.py
# ai_cli/server/gateway/telegram.py
# ai_cli/server/gateway/email.py
# ai_cli/server/api.py
```

**验收标准**:
- 能接收 Slack 消息并响应
- 能接收 Telegram 消息并响应
- 能接收 Email 并回复
- HTTP API 完整可用

#### 阶段 4: 工作者通讯机制（2 周）

**任务**:
- [ ] 实现 `MessageBus` 类（发布/订阅）
- [ ] 实现工作者间请求/响应协议
- [ ] 实现任务依赖管理（DAG）
- [ ] 实现死锁检测

**关键代码**:
```python
# ai_cli/core/message_bus.py
# ai_cli/core/task_dag.py
```

**验收标准**:
- 工作者 A 能请求工作者 B 的数据
- 支持广播通知
- 能检测循环依赖
- 超时自动失败

#### 阶段 5: 记忆和日志（2 周）

**任务**:
- [ ] 实现 `MemoryManager` 类（向量存储）
- [ ] 实现结构化日志（structlog）
- [ ] 实现日志归档策略
- [ ] 实现记忆检索（RAG）

**关键代码**:
```python
# ai_cli/ai/memory.py
# ai_cli/monitoring/logging.py
# ai_cli/db/qdrant.py
```

**验收标准**:
- 所有消息持久化到数据库
- 向量检索准确率 > 85%
- 日志可查询和导出
- 记忆自动注入到上下文

#### 阶段 6: 项目和工具模块增强（2 周）

**任务**:
- [ ] 扩展项目管理（元数据、模板、权限）
- [ ] 扩展工具管理（版本、健康检查、统计）
- [ ] 实现自动更新机制
- [ ] 实现依赖分析

**关键代码**:
```python
# ai_cli/core/projects.py (扩展)
# ai_cli/core/tools.py (扩展)
# ai_cli/core/updater.py
```

**验收标准**:
- 项目支持标签和分组
- 工具能自动检测更新
- 依赖冲突能被检测
- 权限控制生效

#### 阶段 7: 监控和运维（1 周）

**任务**:
- [ ] 实现 Prometheus 指标导出
- [ ] 实现健康检查端点
- [ ] 实现管理面板（可选）
- [ ] 实现告警机制

**关键代码**:
```python
# ai_cli/monitoring/metrics.py
# ai_cli/monitoring/health.py
```

**验收标准**:
- Grafana 能显示关键指标
- 健康检查端点正常
- 异常能触发告警

#### 阶段 8: 测试和文档（2 周）

**任务**:
- [ ] 集成测试
- [ ] 端到端测试
- [ ] 性能测试
- [ ] API 文档（OpenAPI）
- [ ] 用户手册
- [ ] 部署文档

**交付物**:
- 测试覆盖率报告（> 80%）
- API 文档（Swagger UI）
- 部署指南
- 用户手册

### 8.2 时间线

```
Week 1:  [准备工作]
Week 2-4: [工作者管理] ████████████
Week 5-6: [智能路由] ██████
Week 7-8: [消息网关] ██████
Week 9-10: [工作者通讯] ██████
Week 11-12: [记忆日志] ██████
Week 13-14: [模块增强] ██████
Week 15: [监控运维] ███
Week 16-17: [测试文档] ██████

总计: 17 周（约 4 个月）
```

### 8.3 人力需求

| 角色 | 人数 | 职责 |
|------|------|------|
| **后端工程师** | 2 | 核心模块开发 |
| **AI 工程师** | 1 | 任务分析、记忆检索 |
| **DevOps 工程师** | 1 | 部署、监控、CI/CD |
| **测试工程师** | 1 | 测试、质量保证 |
| **技术文档** | 0.5 | 文档编写 |

**总计**: 5.5 人月

---

## 9. 风险评估

### 9.1 技术风险

| 风险 | 等级 | 影响 | 缓解措施 |
|------|------|------|---------|
| **进程管道阻塞** | 🔴 高 | 工作者卡死 | 异步 I/O + 超时机制 |
| **AI 模型延迟** | 🟡 中 | 用户体验差 | 使用快速模型 + 缓存 |
| **并发资源耗尽** | 🔴 高 | 系统崩溃 | 资源限制 + 队列 |
| **工作者死锁** | 🟡 中 | 任务卡住 | 超时 + 死锁检测 |
| **数据库性能** | 🟡 中 | 查询慢 | 索引优化 + 分区 |
| **向量检索准确性** | 🟢 低 | 记忆不准 | 调优嵌入模型 |

### 9.2 业务风险

| 风险 | 等级 | 影响 | 缓解措施 |
|------|------|------|---------|
| **AI 误判任务** | 🟡 中 | 错误路由 | 人工确认 + 反馈学习 |
| **成本超支** | 🟡 中 | 预算超标 | 使用便宜模型 + 限额 |
| **安全漏洞** | 🔴 高 | 数据泄露 | 权限控制 + 审计 |
| **工具兼容性** | 🟡 中 | 功能受限 | 工具能力测试 |

### 9.3 运维风险

| 风险 | 等级 | 影响 | 缓解措施 |
|------|------|------|---------|
| **服务宕机** | 🔴 高 | 业务中断 | 多实例 + 自动重启 |
| **数据丢失** | 🔴 高 | 无法恢复 | 定期备份 + 主从复制 |
| **日志爆炸** | 🟡 中 | 磁盘满 | 日志轮转 + 归档 |
| **依赖更新** | 🟢 低 | 兼容性问题 | 版本锁定 + 测试 |

---

## 10. 附录

### 10.1 依赖清单

```toml
# pyproject.toml (新增依赖)

[project]
dependencies = [
    # 现有依赖
    "click>=8.1.0",
    "rich>=13.0.0",
    "prompt-toolkit>=3.0.0",
    
    # Web 框架
    "fastapi>=0.110.0",
    "uvicorn[standard]>=0.27.0",
    "websockets>=12.0",
    
    # 异步和并发
    "asyncio>=3.4.3",
    "aiofiles>=23.2.0",
    "aiohttp>=3.9.0",
    
    # AI 模型
    "litellm>=1.30.0",
    "openai>=1.12.0",
    "anthropic>=0.18.0",
    
    # 数据库
    "asyncpg>=0.29.0",
    "redis[hiredis]>=5.0.0",
    "qdrant-client>=1.7.0",
    "sqlalchemy[asyncio]>=2.0.0",
    "alembic>=1.13.0",
    
    # 消息集成
    "slack-sdk>=3.26.0",
    "python-telegram-bot>=20.7",
    "aiosmtplib>=3.0.0",
    
    # 日志和监控
    "structlog>=24.1.0",
    "prometheus-client>=0.19.0",
    
    # 任务调度
    "apscheduler>=3.10.0",
    
    # 工具
    "pydantic>=2.6.0",
    "python-dotenv>=1.0.0",
]
```

### 10.2 环境变量配置

```bash
# .env.example

# 数据库
DATABASE_URL=postgresql://user:pass@localhost:5432/ai_cli
REDIS_URL=redis://localhost:6379/0
QDRANT_URL=http://localhost:6333

# AI 模型
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
DEFAULT_MODEL=gpt-4o-mini

# 消息集成
SLACK_BOT_TOKEN=xoxb-xxx
SLACK_SIGNING_SECRET=xxx
TELEGRAM_BOT_TOKEN=xxx
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=xxx
EMAIL_PASSWORD=xxx

# 系统配置
MAX_WORKERS=20
WORKER_TIMEOUT=3600
LOG_LEVEL=INFO
ENVIRONMENT=production

# 安全
JWT_SECRET=xxx
API_KEY=xxx
```

### 10.3 Docker Compose 配置

```yaml
# docker-compose.yml
version: '3.8'

services:
  # 应用服务
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/ai_cli
      - REDIS_URL=redis://redis:6379/0
      - QDRANT_URL=http://qdrant:6333
    depends_on:
      - postgres
      - redis
      - qdrant
    volumes:
      - ./projects:/projects  # 挂载项目目录
    restart: unless-stopped
  
  # PostgreSQL
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ai_cli
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
  
  # Redis
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
  
  # Qdrant
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage
  
  # Prometheus
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
  
  # Grafana
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
    depends_on:
      - prometheus

volumes:
  postgres_data:
  redis_data:
  qdrant_data:
  prometheus_data:
  grafana_data:
```

### 10.4 启动命令

```bash
# 开发环境
docker-compose up -d
python -m ai_cli.server.api

# 生产环境
docker-compose -f docker-compose.prod.yml up -d
```


---

## 11. 完整示例：端到端流程

### 11.1 场景：Slack 触发开发任务

#### 用户操作
```
用户在 Slack: @ai-bot 请用 kiro 为 AI-CLI 项目增加自动升级功能
```

#### 系统处理流程

**步骤 1: 消息接收**
```python
# ai_cli/server/gateway/slack.py
@slack_app.event("app_mention")
async def handle_mention(event, say):
    user_id = event["user"]
    message = event["text"].replace("<@BOT_ID>", "").strip()
    
    # 入队
    await redis.xadd("queue:incoming_messages", {
        "user_id": user_id,
        "channel": "slack",
        "channel_user_id": user_id,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    })
    
    await say("收到任务，正在分析...")
```

**步骤 2: 任务分析**
```python
# 消费队列
async def process_messages():
    while True:
        messages = await redis.xread({"queue:incoming_messages": ">"})
        
        for stream, msg_list in messages:
            for msg_id, data in msg_list:
                # 路由消息
                result = await router.route_message(
                    data["user_id"],
                    data["channel"],
                    data["message"]
                )
                
                # AI 分析结果
                # {
                #     "tool": "kiro-cli",
                #     "project": "AI-CLI",
                #     "task": "增加自动升级功能",
                #     "is_new_task": true
                # }
```

**步骤 3: 工作者创建**
```python
# ai_cli/core/worker_manager.py
worker_id = await worker_manager.create_worker(
    tool="kiro-cli",
    project="AI-CLI",
    task="增加自动升级功能",
    user_id=user_id,
    channel="slack"
)

# 启动子进程
# $ cd /mnt/c/Projects/AIStudio/AI-CLI
# $ kiro-cli chat --no-interactive --trust-all-tools
# > 增加自动升级功能
```

**步骤 4: 实时输出**
```python
# 监控工作者输出
async for output in worker.read_output():
    # 保存日志
    await postgres.execute(
        "INSERT INTO worker_logs (worker_id, stream, content) VALUES ($1, $2, $3)",
        worker_id, "stdout", output
    )
    
    # 发送到 Slack
    await slack_client.chat_postMessage(
        channel=channel_id,
        text=output
    )
```

**步骤 5: 用户交互**
```
Kiro 输出: "我将创建一个自动升级模块。是否需要支持回滚功能？(y/n)"
用户回复: "是的，需要"
```

```python
# 路由器检测到等待输入的工作者
waiting_worker = await worker_manager.get_worker_by_user(user_id)
# waiting_worker.status == WorkerStatus.WAITING_INPUT

# 直接发送到该工作者
await worker.send_input("是的，需要")
```

**步骤 6: 任务完成**
```python
# 工作者进程退出
worker.process.returncode == 0
worker.status = WorkerStatus.COMPLETED

# 保存到数据库
await postgres.execute(
    "UPDATE workers SET status=$1, completed_at=$2, exit_code=$3 WHERE id=$4",
    "completed", datetime.utcnow(), 0, worker_id
)

# 通知用户
await slack_client.chat_postMessage(
    channel=channel_id,
    text="✅ 任务完成！自动升级功能已添加。"
)

# 清理工作者
await worker_manager.cleanup_worker(worker_id)
```

### 11.2 场景：多工作者协作

#### 用户操作
```
用户: "用 kiro 分析 AI-CLI 的代码结构，然后用 claude 重构 app.py"
```

#### 系统处理

**步骤 1: AI 分析识别多任务**
```python
analysis = {
    "multi_worker": true,
    "workers": [
        {
            "tool": "kiro-cli",
            "project": "AI-CLI",
            "task": "分析代码结构",
            "order": 1
        },
        {
            "tool": "claude",
            "project": "AI-CLI",
            "task": "重构 app.py",
            "order": 2,
            "depends_on": ["worker_1"]  # 依赖第一个工作者
        }
    ]
}
```

**步骤 2: 创建 DAG**
```python
# ai_cli/core/task_dag.py
dag = TaskDAG()
dag.add_task("worker_1", analysis["workers"][0])
dag.add_task("worker_2", analysis["workers"][1], depends_on=["worker_1"])

# 执行 DAG
await dag.execute()
```

**步骤 3: 顺序执行**
```python
# 启动 Worker 1
worker_1 = await worker_manager.create_worker(...)
await worker_1.wait_completion()

# Worker 1 完成后，通过消息总线通知
await message_bus.publish("task:completed", {
    "worker_id": "worker_1",
    "output": "代码结构分析完成，主要模块有..."
})

# 启动 Worker 2，注入 Worker 1 的输出
worker_2 = await worker_manager.create_worker(
    task=f"重构 app.py。参考分析结果：{worker_1_output}"
)
```

### 11.3 场景：记忆检索

#### 用户操作
```
用户: "上次我让你分析的那个项目，现在要重构"
```

#### 系统处理

**步骤 1: 检索相关记忆**
```python
# ai_cli/ai/context_manager.py
memories = await memory_manager.search(
    user_id=user_id,
    query="上次我让你分析的那个项目",
    top_k=3
)

# 结果:
# [
#     {
#         "content": "用户让我分析 AI-CLI 项目的代码结构",
#         "score": 0.92,
#         "timestamp": "2026-03-01T10:30:00Z",
#         "metadata": {"project": "AI-CLI", "tool": "kiro-cli"}
#     }
# ]
```

**步骤 2: 注入上下文**
```python
# 构建增强提示
enhanced_message = f"""
用户消息: {message}

相关历史:
- {memories[0]["content"]} (3天前)
- 项目: {memories[0]["metadata"]["project"]}

请分析用户意图。
"""

# AI 分析
analysis = await task_analyzer.analyze(enhanced_message, context)
# 输出: {"project": "AI-CLI", "task": "重构", ...}
```

---

## 12. 性能指标

### 12.1 目标指标

| 指标 | 目标值 | 测量方法 |
|------|--------|---------|
| **消息响应延迟** | < 2s | 从接收到首次响应 |
| **AI 分析延迟** | < 3s | TaskAnalyzer 执行时间 |
| **工作者启动时间** | < 5s | 从创建到 RUNNING 状态 |
| **并发工作者数** | 50+ | 压力测试 |
| **记忆检索延迟** | < 500ms | Qdrant 查询时间 |
| **系统可用性** | 99.5% | 月度统计 |

### 12.2 资源估算

**单工作者资源消耗**:
- CPU: 0.5-1 核
- 内存: 200-500 MB
- 磁盘 I/O: 中等

**系统资源需求**（20 并发工作者）:
- CPU: 16 核
- 内存: 16 GB
- 磁盘: 100 GB SSD
- 网络: 100 Mbps

---

## 13. 安全设计

### 13.1 认证和授权

```python
# ai_cli/server/auth.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """验证 JWT Token"""
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="无效的 Token")

# 使用
@app.post("/api/v1/tasks")
async def create_task(
    request: TaskRequest,
    user_id: str = Depends(verify_token)
):
    # user_id 已验证
    pass
```

### 13.2 权限控制

```python
# ai_cli/server/auth.py
class Permission(str, Enum):
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"

async def check_permission(
    user_id: str,
    project_id: str,
    required: Permission
) -> bool:
    """检查用户权限"""
    permissions = await postgres.fetchval(
        "SELECT permissions FROM projects WHERE id=$1",
        project_id
    )
    
    user_perms = permissions.get(user_id, [])
    return required in user_perms or "admin" in user_perms
```

### 13.3 输入验证

```python
# ai_cli/server/api.py
from pydantic import BaseModel, validator

class TaskRequest(BaseModel):
    message: str
    channel: str
    user_id: str
    
    @validator("message")
    def validate_message(cls, v):
        if len(v) > 10000:
            raise ValueError("消息过长")
        if not v.strip():
            raise ValueError("消息不能为空")
        return v
    
    @validator("channel")
    def validate_channel(cls, v):
        allowed = ["slack", "telegram", "email", "api", "websocket"]
        if v not in allowed:
            raise ValueError(f"不支持的渠道: {v}")
        return v
```

### 13.4 审计日志

```python
# ai_cli/monitoring/audit.py
async def log_audit(
    user_id: str,
    action: str,
    resource: str,
    result: str,
    metadata: dict = {}
):
    """记录审计日志"""
    await postgres.execute("""
        INSERT INTO audit_logs (user_id, action, resource, result, metadata)
        VALUES ($1, $2, $3, $4, $5)
    """, user_id, action, resource, result, json.dumps(metadata))

# 使用
await log_audit(
    user_id="user_123",
    action="create_worker",
    resource="worker_abc",
    result="success",
    metadata={"tool": "kiro-cli", "project": "AI-CLI"}
)
```

---

## 14. 监控和告警

### 14.1 Prometheus 指标

```python
# ai_cli/monitoring/metrics.py
from prometheus_client import Counter, Gauge, Histogram

# 工作者指标
worker_created_total = Counter(
    "worker_created_total",
    "工作者创建总数",
    ["tool", "project"]
)

worker_active = Gauge(
    "worker_active",
    "活跃工作者数量"
)

worker_duration = Histogram(
    "worker_duration_seconds",
    "工作者执行时长",
    ["tool", "status"]
)

# API 指标
api_requests_total = Counter(
    "api_requests_total",
    "API 请求总数",
    ["method", "endpoint", "status"]
)

api_latency = Histogram(
    "api_latency_seconds",
    "API 延迟",
    ["endpoint"]
)

# AI 模型指标
ai_analysis_duration = Histogram(
    "ai_analysis_duration_seconds",
    "AI 分析耗时"
)

ai_tokens_used = Counter(
    "ai_tokens_used_total",
    "AI Token 使用量",
    ["model"]
)
```

### 14.2 告警规则

```yaml
# monitoring/prometheus.yml
groups:
  - name: ai_cli_alerts
    interval: 30s
    rules:
      # 工作者数量告警
      - alert: TooManyWorkers
        expr: worker_active > 50
        for: 5m
        annotations:
          summary: "工作者数量过多"
          description: "当前活跃工作者: {{ $value }}"
      
      # API 错误率告警
      - alert: HighErrorRate
        expr: rate(api_requests_total{status="500"}[5m]) > 0.05
        for: 2m
        annotations:
          summary: "API 错误率过高"
      
      # 数据库连接告警
      - alert: DatabaseDown
        expr: up{job="postgres"} == 0
        for: 1m
        annotations:
          summary: "数据库不可用"
```

---

## 15. 测试策略

### 15.1 单元测试

```python
# tests/test_worker.py
import pytest
from ai_cli.core.ai_worker import AIWorker

@pytest.mark.asyncio
async def test_worker_lifecycle():
    """测试工作者生命周期"""
    worker = AIWorker(
        worker_id="test_1",
        tool="kiro-cli",
        project_path="/tmp/test",
        worktree=None,
        task="测试任务",
        user_id="user_1",
        channel="test"
    )
    
    # 启动
    assert await worker.start() == True
    assert worker.status == WorkerStatus.RUNNING
    
    # 发送输入
    await worker.send_input("测试输入")
    
    # 读取输出
    output = []
    async for line in worker.read_output():
        output.append(line)
        if len(output) >= 5:
            break
    
    assert len(output) > 0
    
    # 终止
    await worker.terminate()
    assert worker.status == WorkerStatus.COMPLETED
```

### 15.2 集成测试

```python
# tests/test_integration.py
@pytest.mark.asyncio
async def test_end_to_end_flow():
    """端到端测试"""
    
    # 1. 发送消息
    response = await client.post("/api/v1/tasks", json={
        "message": "用 kiro 分析代码",
        "channel": "api",
        "user_id": "test_user"
    })
    
    assert response.status_code == 200
    task_id = response.json()["task_id"]
    
    # 2. 等待工作者启动
    await asyncio.sleep(2)
    
    # 3. 检查工作者状态
    worker_response = await client.get(f"/api/v1/workers/{task_id}")
    assert worker_response.json()["status"] == "running"
    
    # 4. 发送输入
    await client.post(f"/api/v1/tasks/{task_id}/input", json={
        "content": "继续"
    })
    
    # 5. 等待完成
    await asyncio.sleep(10)
    
    # 6. 验证日志
    logs = await client.get(f"/api/v1/workers/{task_id}/logs")
    assert len(logs.json()) > 0
```

### 15.3 性能测试

```python
# tests/test_performance.py
import asyncio
from locust import HttpUser, task, between

class AICliUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def create_task(self):
        self.client.post("/api/v1/tasks", json={
            "message": "测试任务",
            "channel": "api",
            "user_id": f"user_{self.user_id}"
        })
    
    @task
    def list_workers(self):
        self.client.get("/api/v1/workers")

# 运行: locust -f tests/test_performance.py --host=http://localhost:8000
```

---

## 16. 部署指南

### 16.1 生产环境部署

```bash
# 1. 克隆代码
git clone https://github.com/hyfhot/AI-CLI.git
cd AI-CLI
git checkout master

# 2. 配置环境变量
cp .env.example .env
vim .env  # 编辑配置

# 3. 启动服务
docker-compose -f docker-compose.prod.yml up -d

# 4. 运行数据库迁移
docker-compose exec app alembic upgrade head

# 5. 验证服务
curl http://localhost:8000/health
```

### 16.2 Kubernetes 部署（可选）

```yaml
# k8s/deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-cli-worker-system
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-cli
  template:
    metadata:
      labels:
        app: ai-cli
    spec:
      containers:
      - name: app
        image: ai-cli:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: ai-cli-secrets
              key: database-url
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
```

---

## 17. 成本估算

### 17.1 基础设施成本（月）

| 资源 | 规格 | 成本（USD） |
|------|------|------------|
| **服务器** | 16核 32GB | $150 |
| **PostgreSQL** | 托管服务 | $50 |
| **Redis** | 托管服务 | $30 |
| **Qdrant** | 自托管 | $0 |
| **负载均衡** | Nginx | $0 |
| **监控** | Grafana Cloud | $0-50 |
| **总计** | - | **$230-280** |

### 17.2 AI 模型成本（月）

假设：100 用户，每人每天 10 次任务

| 模型 | 用途 | 调用次数/月 | 成本 |
|------|------|------------|------|
| **GPT-4o-mini** | 任务分析 | 30,000 | $15 |
| **GPT-4o-mini** | 消息路由 | 30,000 | $15 |
| **text-embedding-3-small** | 向量化 | 60,000 | $1 |
| **Claude 3.5 Haiku** | 复杂推理 | 3,000 | $3 |
| **总计** | - | - | **$34** |

**总成本**: $264-314/月（约 ¥1,900-2,300/月）

---

## 18. 后续优化方向

### 18.1 短期优化（3 个月内）

1. **智能任务分解**: AI 自动将复杂任务拆分为子任务
2. **工作者池**: 预热工作者，减少启动延迟
3. **流式响应**: 实时流式输出，提升体验
4. **错误自愈**: 工作者异常自动重试

### 18.2 中期优化（6 个月内）

1. **多租户支持**: 支持多组织隔离
2. **工作流引擎**: 可视化编排工作者
3. **插件系统**: 支持自定义工具和集成
4. **Web UI**: 管理面板和监控界面

### 18.3 长期愿景（1 年内）

1. **自主学习**: 从用户反馈学习，优化路由
2. **代码理解**: 深度理解项目代码，智能建议
3. **团队协作**: 多用户协作开发
4. **市场化**: SaaS 服务，支持订阅

---

## 19. 总结

### 19.1 关键决策

| 决策点 | 选择 | 理由 |
|--------|------|------|
| **基础分支** | Master (Python) | 架构适合、生态成熟 |
| **Web 框架** | FastAPI | 异步、高性能、自动文档 |
| **AI 接口** | LiteLLM | 统一多模型、易切换 |
| **消息队列** | Redis Streams | 轻量、持久化、简单 |
| **向量数据库** | Qdrant | 开源、高性能、易部署 |

### 19.2 核心优势

✅ **智能化**: AI 理解意图，自动路由  
✅ **自动化**: 从消息到代码的全自动流程  
✅ **可扩展**: 支持任意工具和项目  
✅ **可观测**: 完整日志和监控  
✅ **高性能**: 异步架构，支持高并发  

### 19.3 技术亮点

1. **异步 I/O 多路复用**: 单进程管理多个工作者
2. **智能上下文管理**: 短期+中期+长期三层记忆
3. **工作者间通讯**: 支持复杂任务协作
4. **向量化记忆**: 语义检索历史对话
5. **多渠道统一**: 一套系统支持所有渠道

### 19.4 实施建议

**优先级排序**:
1. **P0**: 工作者管理 + 基础 API（核心功能）
2. **P1**: 智能路由 + Slack 集成（MVP）
3. **P2**: 记忆管理 + 工作者通讯（增强）
4. **P3**: 其他渠道 + 监控（完善）

**MVP 范围**（8 周）:
- 工作者管理（创建、I/O、终止）
- 基础路由（新任务 vs 继续对话）
- Slack 集成
- PostgreSQL 日志
- 基础监控

**完整版本**（17 周）:
- 所有功能完整实现
- 多渠道支持
- 向量记忆
- 工作者协作
- 完整监控

---

## 20. 参考资料

### 20.1 相关项目

- **AutoGPT**: https://github.com/Significant-Gravitas/AutoGPT
- **LangChain**: https://github.com/langchain-ai/langchain
- **CrewAI**: https://github.com/joaomdmoura/crewAI
- **Openclaw**: https://github.com/openclaw/openclaw
- **Nanobot**: https://github.com/nanobot/nanobot

### 20.2 技术文档

- FastAPI: https://fastapi.tiangolo.com/
- LiteLLM: https://docs.litellm.ai/
- Qdrant: https://qdrant.tech/documentation/
- Redis Streams: https://redis.io/docs/data-types/streams/
- Alembic: https://alembic.sqlalchemy.org/

### 20.3 最佳实践

- **12-Factor App**: https://12factor.net/
- **Microservices Patterns**: https://microservices.io/
- **Async Python**: https://realpython.com/async-io-python/

---

**文档版本**: 1.0  
**最后更新**: 2026-03-05  
**作者**: AI-CLI Team  
**审核状态**: 待审核

---

## 附录 A: 快速启动指南

### 开发环境快速启动

```bash
# 1. 安装依赖
pip install -e ".[dev]"

# 2. 启动基础设施
docker-compose up -d postgres redis qdrant

# 3. 运行迁移
alembic upgrade head

# 4. 启动服务
python -m ai_cli.server.api

# 5. 测试
curl http://localhost:8000/health
```

### 测试 API

```bash
# 创建任务
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "message": "用 kiro 分析代码",
    "channel": "api",
    "user_id": "test_user"
  }'

# 查看工作者
curl http://localhost:8000/api/v1/workers

# WebSocket 测试
wscat -c ws://localhost:8000/ws/test_user
```

---

## 附录 B: 故障排查

### 常见问题

**Q1: 工作者无法启动**
```bash
# 检查工具是否安装
kiro-cli --version

# 检查项目路径
ls -la /path/to/project

# 查看工作者日志
curl http://localhost:8000/api/v1/workers/{worker_id}/logs
```

**Q2: AI 分析不准确**
```bash
# 检查模型配置
echo $DEFAULT_MODEL

# 查看分析日志
tail -f logs/task_analyzer.log

# 调整提示词
vim ai_cli/ai/task_analyzer.py
```

**Q3: 数据库连接失败**
```bash
# 检查连接
psql $DATABASE_URL

# 查看连接池
curl http://localhost:8000/api/v1/debug/db-pool
```

---

**文档结束**
