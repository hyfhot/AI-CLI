# AI CLI 工具 CI/CD 集成完整指南

> 详细说明如何将 Kiro CLI、Claude Code、Codex CLI 等工具的非交互参数集成到脚本和 CI/CD 流程中
> 
> 更新时间：2026-03-05

## 目录

- [核心概念](#核心概念)
- [参数详解](#参数详解)
- [Shell 脚本集成](#shell-脚本集成)
- [CI/CD 平台集成](#cicd-平台集成)
- [实战场景](#实战场景)
- [最佳实践](#最佳实践)
- [故障排查](#故障排查)

---

## 核心概念

### 非交互模式的本质

**交互模式** vs **非交互模式**：

```bash
# 交互模式 - 需要用户输入
$ kiro-cli chat
> 用户输入问题
> 查看响应
> 继续对话...

# 非交互模式 - 一次性执行
$ kiro-cli chat --no-interactive "生成代码"
输出结果
退出（返回退出码）
```

### 关键要素

1. **标准输入/输出**：结果输出到 stdout，错误到 stderr
2. **退出码**：0 = 成功，非 0 = 失败
3. **无需人工干预**：所有决策由参数预先指定
4. **可重复执行**：相同输入产生一致结果

---

## 参数详解

### 1. Kiro CLI 参数

#### `--no-interactive`
```bash
kiro-cli chat --no-interactive "任务描述"
```
- **作用**：打印第一个响应到 STDOUT 后立即退出
- **返回**：退出码 0（成功）或非 0（失败）
- **输出**：纯文本或 JSON（取决于任务）

#### `--trust-all-tools`
```bash
kiro-cli chat --no-interactive --trust-all-tools "执行任务"
```
- **作用**：允许 AI 使用任何工具（文件读写、命令执行）无需确认
- **风险**：⚠️ 高权限，仅在受控环境使用
- **适用**：CI/CD 自动化流程

#### `--trust-tools <list>`
```bash
kiro-cli chat --no-interactive \
  --trust-tools "read_file,write_file,search_files" \
  "分析代码"
```
- **作用**：仅信任指定工具，其他需确认（但非交互模式会失败）
- **安全**：✅ 限制权限范围
- **推荐**：生产环境使用

#### `--agent <name>`
```bash
kiro-cli chat --no-interactive --agent code-reviewer "审查代码"
```
- **作用**：使用预配置的自定义 Agent
- **优势**：一致的行为、专门优化的提示

### 2. Claude Code 参数

#### `--print` / `-p`
```bash
claude --print "生成代码"
claude -p "任务描述"
```
- **作用**：打印模式，仅输出结果，不进入交互
- **输出**：干净的文本输出
- **适用**：脚本捕获输出

#### `--auto-edit`
```bash
claude --auto-edit "重构代码"
```
- **作用**：自动批准所有文件编辑操作
- **确认**：Shell 命令仍需确认（安全考虑）
- **组合**：通常与 `--print` 一起使用

#### `--model <name>`
```bash
claude --print --model claude-opus-4 "复杂任务"
```
- **作用**：指定使用的模型
- **选择**：opus-4（复杂）、sonnet-4（平衡）、haiku-4（快速）

### 3. Codex CLI 参数

#### `--quiet` / `-q`
```bash
codex -q "生成代码"
```
- **作用**：安静模式，仅输出结果，无额外信息
- **输出**：最干净的输出，适合管道

#### `--auto-edit`
```bash
codex --auto-edit -q "修复 bug"
```
- **作用**：自动批准文件编辑

#### `--json`
```bash
codex --json "提取数据"
```
- **作用**：JSON 格式输出
- **解析**：易于脚本解析

---

## Shell 脚本集成

### 基础脚本模板

#### 1. 简单执行脚本

```bash
#!/bin/bash
set -e  # 遇到错误立即退出
set -o pipefail  # 管道中任何命令失败都退出

# 配置
TASK="生成单元测试"
OUTPUT_FILE="tests/generated_tests.py"

# 执行 AI 任务
echo "开始执行: $TASK"
kiro-cli chat --no-interactive --trust-tools "write_file" "$TASK" > "$OUTPUT_FILE"

# 检查结果
if [ $? -eq 0 ]; then
    echo "✅ 任务完成: $OUTPUT_FILE"
else
    echo "❌ 任务失败"
    exit 1
fi
```

#### 2. 带错误处理的脚本

```bash
#!/bin/bash

# 错误处理函数
handle_error() {
    local exit_code=$1
    local line_number=$2
    echo "❌ 错误发生在第 $line_number 行，退出码: $exit_code" >&2
    
    # 发送通知（可选）
    # curl -X POST https://hooks.slack.com/... -d "{'text':'AI 任务失败'}"
    
    exit $exit_code
}

trap 'handle_error $? $LINENO' ERR
set -e

# 执行任务
echo "🤖 启动 AI 代码审查..."
RESULT=$(kiro-cli chat --no-interactive \
    --trust-tools "read_file,search_files" \
    "审查所有 Python 文件，输出问题列表" 2>&1)

# 保存结果
echo "$RESULT" > code_review_report.txt

# 检查是否发现问题
if echo "$RESULT" | grep -q "问题"; then
    echo "⚠️  发现代码问题，请查看报告"
    exit 1
else
    echo "✅ 代码审查通过"
    exit 0
fi
```

#### 3. 多任务串行执行

```bash
#!/bin/bash
set -e

TASKS=(
    "生成 API 文档"
    "更新 README.md"
    "生成变更日志"
)

for task in "${TASKS[@]}"; do
    echo "📝 执行: $task"
    
    if ! kiro-cli chat --no-interactive --trust-all-tools "$task"; then
        echo "❌ 失败: $task"
        exit 1
    fi
    
    echo "✅ 完成: $task"
    sleep 2  # 避免 API 限流
done

echo "🎉 所有任务完成"
```

#### 4. 并行执行脚本

```bash
#!/bin/bash

# 并行执行多个独立任务
run_task() {
    local task=$1
    local output_file=$2
    
    echo "开始: $task"
    kiro-cli chat --no-interactive "$task" > "$output_file" 2>&1
    
    if [ $? -eq 0 ]; then
        echo "✅ $task"
    else
        echo "❌ $task"
        return 1
    fi
}

# 导出函数供子进程使用
export -f run_task

# 并行执行
parallel -j 3 run_task ::: \
    "生成单元测试" \
    "生成集成测试" \
    "生成 E2E 测试" \
    ::: \
    "tests/unit.py" \
    "tests/integration.py" \
    "tests/e2e.py"

echo "所有测试生成完成"
```

### 高级脚本技巧

#### 1. 输出解析和验证

```bash
#!/bin/bash

# 执行任务并捕获输出
OUTPUT=$(kiro-cli chat --no-interactive "生成 JSON 配置" 2>&1)
EXIT_CODE=$?

# 检查退出码
if [ $EXIT_CODE -ne 0 ]; then
    echo "执行失败: $OUTPUT" >&2
    exit 1
fi

# 验证输出格式
if echo "$OUTPUT" | jq . >/dev/null 2>&1; then
    echo "✅ 有效的 JSON 输出"
    echo "$OUTPUT" > config.json
else
    echo "❌ 无效的 JSON 输出" >&2
    exit 1
fi
```

#### 2. 重试机制

```bash
#!/bin/bash

retry_task() {
    local max_attempts=3
    local attempt=1
    local delay=5
    
    while [ $attempt -le $max_attempts ]; do
        echo "尝试 $attempt/$max_attempts..."
        
        if kiro-cli chat --no-interactive "$1"; then
            echo "✅ 成功"
            return 0
        fi
        
        echo "⚠️  失败，等待 ${delay}s 后重试..."
        sleep $delay
        delay=$((delay * 2))  # 指数退避
        attempt=$((attempt + 1))
    done
    
    echo "❌ 所有尝试均失败"
    return 1
}

# 使用
retry_task "生成复杂代码"
```

#### 3. 超时控制

```bash
#!/bin/bash

# 使用 timeout 命令
TIMEOUT=300  # 5 分钟

if timeout $TIMEOUT kiro-cli chat --no-interactive --trust-all-tools "长时间任务"; then
    echo "✅ 任务完成"
else
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 124 ]; then
        echo "❌ 任务超时（${TIMEOUT}s）"
    else
        echo "❌ 任务失败（退出码: $EXIT_CODE）"
    fi
    exit 1
fi
```

#### 4. 日志记录

```bash
#!/bin/bash

# 日志配置
LOG_DIR="logs"
LOG_FILE="$LOG_DIR/ai_tasks_$(date +%Y%m%d_%H%M%S).log"
mkdir -p "$LOG_DIR"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

# 执行任务
log "开始执行 AI 任务"

if kiro-cli chat --no-interactive "$TASK" 2>&1 | tee -a "$LOG_FILE"; then
    log "✅ 任务成功"
else
    log "❌ 任务失败"
    exit 1
fi
```

---

## CI/CD 平台集成

### 1. GitHub Actions

#### 基础工作流

```yaml
# .github/workflows/ai-code-review.yml
name: AI Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Install Kiro CLI
        run: |
          curl -fsSL https://cli.kiro.dev/install | bash
          echo "$HOME/.kiro/bin" >> $GITHUB_PATH
      
      - name: Configure Kiro
        env:
          KIRO_API_KEY: ${{ secrets.KIRO_API_KEY }}
        run: |
          kiro-cli login --api-key "$KIRO_API_KEY"
      
      - name: Run AI Code Review
        id: review
        run: |
          kiro-cli chat --no-interactive \
            --trust-tools "read_file,search_files" \
            "审查此 PR 的所有更改，输出 Markdown 格式报告" \
            > review_report.md
      
      - name: Post Review Comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('review_report.md', 'utf8');
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## 🤖 AI Code Review\n\n${report}`
            });
      
      - name: Upload Report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: ai-review-report
          path: review_report.md
```

#### 自动修复工作流

```yaml
# .github/workflows/ai-auto-fix.yml
name: AI Auto Fix

on:
  push:
    branches: [main, develop]

jobs:
  auto-fix:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code
      
      - name: Configure Claude
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: echo "ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY" >> $GITHUB_ENV
      
      - name: Run Linter
        id: lint
        continue-on-error: true
        run: |
          npm run lint > lint_errors.txt 2>&1 || true
      
      - name: AI Auto Fix
        if: steps.lint.outcome == 'failure'
        run: |
          claude --print --auto-edit \
            "根据 lint_errors.txt 中的错误修复所有代码问题"
      
      - name: Commit Changes
        run: |
          git config user.name "AI Bot"
          git config user.email "ai-bot@example.com"
          git add .
          git diff --staged --quiet || git commit -m "🤖 AI 自动修复 lint 错误"
          git push
```

#### 文档自动更新

```yaml
# .github/workflows/update-docs.yml
name: Update Documentation

on:
  push:
    paths:
      - 'src/**'
      - 'lib/**'

jobs:
  update-docs:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Codex CLI
        run: npm install -g @openai/codex
      
      - name: Generate API Docs
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          codex -q --auto-edit \
            "分析 src/ 目录，更新 docs/API.md 文档" \
            > docs/API.md
      
      - name: Generate README
        run: |
          codex -q "根据代码生成详细的 README.md" > README.md
      
      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v5
        with:
          commit-message: "📝 自动更新文档"
          title: "🤖 AI 生成的文档更新"
          body: "此 PR 由 AI 自动生成，包含最新的 API 文档和 README"
          branch: docs/auto-update
```

### 2. GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - review
  - test
  - deploy

variables:
  KIRO_LOG_LEVEL: "info"

ai-code-review:
  stage: review
  image: ubuntu:latest
  before_script:
    - apt-get update && apt-get install -y curl
    - curl -fsSL https://cli.kiro.dev/install | bash
    - export PATH="$HOME/.kiro/bin:$PATH"
  script:
    - |
      kiro-cli chat --no-interactive \
        --trust-tools "read_file,search_files" \
        "审查代码质量和安全问题" > review.md
  artifacts:
    paths:
      - review.md
    expire_in: 1 week
  only:
    - merge_requests

ai-generate-tests:
  stage: test
  image: node:18
  before_script:
    - npm install -g @anthropic-ai/claude-code
  script:
    - |
      claude --print --auto-edit \
        "为所有未覆盖的函数生成单元测试" || exit 1
    - npm test
  artifacts:
    paths:
      - tests/
  only:
    - main

ai-update-changelog:
  stage: deploy
  image: ubuntu:latest
  before_script:
    - apt-get update && apt-get install -y curl git
    - curl -fsSL https://cli.kiro.dev/install | bash
  script:
    - |
      CHANGES=$(git log --oneline $(git describe --tags --abbrev=0)..HEAD)
      kiro-cli chat --no-interactive \
        "根据以下 git 提交生成 CHANGELOG.md:\n$CHANGES" \
        > CHANGELOG.md
    - git add CHANGELOG.md
    - git commit -m "📝 更新 CHANGELOG" || true
    - git push origin HEAD:main
  only:
    - tags
```

### 3. Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        KIRO_API_KEY = credentials('kiro-api-key')
        ANTHROPIC_API_KEY = credentials('anthropic-api-key')
    }
    
    stages {
        stage('Setup') {
            steps {
                sh '''
                    curl -fsSL https://cli.kiro.dev/install | bash
                    export PATH="$HOME/.kiro/bin:$PATH"
                    kiro-cli login --api-key "$KIRO_API_KEY"
                '''
            }
        }
        
        stage('AI Code Review') {
            steps {
                script {
                    def review = sh(
                        script: '''
                            kiro-cli chat --no-interactive \
                                --trust-tools "read_file,search_files" \
                                "审查代码并输出 JSON 格式报告"
                        ''',
                        returnStdout: true
                    ).trim()
                    
                    writeFile file: 'review.json', text: review
                    archiveArtifacts artifacts: 'review.json'
                }
            }
        }
        
        stage('AI Auto Fix') {
            when {
                expression {
                    return currentBuild.result == 'UNSTABLE'
                }
            }
            steps {
                sh '''
                    claude --print --auto-edit \
                        "修复所有测试失败和 lint 错误"
                    
                    git add .
                    git commit -m "🤖 AI 自动修复" || true
                    git push origin HEAD:${BRANCH_NAME}
                '''
            }
        }
        
        stage('Generate Docs') {
            steps {
                sh '''
                    codex -q --auto-edit \
                        "生成完整的 API 文档" > docs/API.md
                '''
                publishHTML([
                    reportDir: 'docs',
                    reportFiles: 'API.md',
                    reportName: 'API Documentation'
                ])
            }
        }
    }
    
    post {
        failure {
            sh '''
                kiro-cli chat --no-interactive \
                    "分析构建失败原因并提供修复建议" \
                    > failure_analysis.txt
            '''
            archiveArtifacts artifacts: 'failure_analysis.txt'
        }
    }
}
```

### 4. CircleCI

```yaml
# .circleci/config.yml
version: 2.1

executors:
  ai-executor:
    docker:
      - image: cimg/node:18.0
    environment:
      KIRO_LOG_LEVEL: info

commands:
  install-kiro:
    steps:
      - run:
          name: Install Kiro CLI
          command: |
            curl -fsSL https://cli.kiro.dev/install | bash
            echo 'export PATH="$HOME/.kiro/bin:$PATH"' >> $BASH_ENV

jobs:
  ai-code-review:
    executor: ai-executor
    steps:
      - checkout
      - install-kiro
      - run:
          name: AI Code Review
          command: |
            kiro-cli chat --no-interactive \
              --trust-tools "read_file,search_files" \
              "审查代码质量" > review.md
      - store_artifacts:
          path: review.md
  
  ai-generate-tests:
    executor: ai-executor
    steps:
      - checkout
      - run:
          name: Install Claude Code
          command: npm install -g @anthropic-ai/claude-code
      - run:
          name: Generate Tests
          command: |
            claude --print --auto-edit \
              "为所有函数生成测试" || exit 1
      - run:
          name: Run Tests
          command: npm test
      - store_test_results:
          path: test-results

workflows:
  ai-workflow:
    jobs:
      - ai-code-review:
          filters:
            branches:
              only: /.*/
      - ai-generate-tests:
          requires:
            - ai-code-review
          filters:
            branches:
              only: main
```


### 5. Azure DevOps

```yaml
# azure-pipelines.yml
trigger:
  - main
  - develop

pool:
  vmImage: 'ubuntu-latest'

variables:
  - group: ai-credentials  # 包含 KIRO_API_KEY, ANTHROPIC_API_KEY

stages:
  - stage: AIReview
    displayName: 'AI Code Review'
    jobs:
      - job: Review
        steps:
          - task: Bash@3
            displayName: 'Install Kiro CLI'
            inputs:
              targetType: 'inline'
              script: |
                curl -fsSL https://cli.kiro.dev/install | bash
                echo "##vso[task.prependpath]$HOME/.kiro/bin"
          
          - task: Bash@3
            displayName: 'Run AI Review'
            env:
              KIRO_API_KEY: $(KIRO_API_KEY)
            inputs:
              targetType: 'inline'
              script: |
                kiro-cli chat --no-interactive \
                  --trust-tools "read_file,search_files" \
                  "审查代码并输出 Markdown 报告" > $(Build.ArtifactStagingDirectory)/review.md
          
          - task: PublishBuildArtifacts@1
            inputs:
              pathToPublish: '$(Build.ArtifactStagingDirectory)/review.md'
              artifactName: 'ai-review'

  - stage: AIAutoFix
    displayName: 'AI Auto Fix'
    dependsOn: AIReview
    condition: failed()
    jobs:
      - job: Fix
        steps:
          - task: NodeTool@0
            inputs:
              versionSpec: '18.x'
          
          - task: Bash@3
            displayName: 'Install Claude Code'
            inputs:
              targetType: 'inline'
              script: npm install -g @anthropic-ai/claude-code
          
          - task: Bash@3
            displayName: 'AI Auto Fix'
            env:
              ANTHROPIC_API_KEY: $(ANTHROPIC_API_KEY)
            inputs:
              targetType: 'inline'
              script: |
                claude --print --auto-edit "修复所有问题"
                
                git config user.name "Azure AI Bot"
                git config user.email "ai-bot@azure.com"
                git add .
                git commit -m "🤖 AI 自动修复" || true
                git push origin HEAD:$(Build.SourceBranchName)
```

---

## 实战场景

### 场景 1: 自动代码审查

#### 完整脚本

```bash
#!/bin/bash
# scripts/ai-code-review.sh

set -e

# 配置
REVIEW_AGENT="code-reviewer"
OUTPUT_DIR="reports"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_FILE="$OUTPUT_DIR/review_$TIMESTAMP.md"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 获取变更文件
CHANGED_FILES=$(git diff --name-only HEAD~1 HEAD | grep -E '\.(py|js|ts|go)$' || true)

if [ -z "$CHANGED_FILES" ]; then
    echo "没有代码文件变更"
    exit 0
fi

echo "📝 审查以下文件:"
echo "$CHANGED_FILES"

# 构建审查提示
PROMPT="请审查以下文件的代码质量、安全性和最佳实践:\n\n"
PROMPT+="$CHANGED_FILES\n\n"
PROMPT+="输出 Markdown 格式报告，包括:\n"
PROMPT+="1. 发现的问题（按严重程度分类）\n"
PROMPT+="2. 改进建议\n"
PROMPT+="3. 安全风险评估"

# 执行审查
echo "🤖 启动 AI 审查..."
if kiro-cli chat --no-interactive \
    --agent "$REVIEW_AGENT" \
    --trust-tools "read_file,search_files" \
    "$PROMPT" > "$REPORT_FILE"; then
    
    echo "✅ 审查完成: $REPORT_FILE"
    
    # 检查是否有严重问题
    if grep -q "严重\|critical\|security" "$REPORT_FILE"; then
        echo "⚠️  发现严重问题，请查看报告"
        cat "$REPORT_FILE"
        exit 1
    fi
else
    echo "❌ 审查失败"
    exit 1
fi
```

#### GitHub Actions 集成

```yaml
# .github/workflows/code-review.yml
name: AI Code Review

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 2  # 获取前一次提交
      
      - name: Setup Kiro CLI
        run: |
          curl -fsSL https://cli.kiro.dev/install | bash
          echo "$HOME/.kiro/bin" >> $GITHUB_PATH
      
      - name: Run Review Script
        env:
          KIRO_API_KEY: ${{ secrets.KIRO_API_KEY }}
        run: |
          chmod +x scripts/ai-code-review.sh
          ./scripts/ai-code-review.sh
      
      - name: Comment on PR
        if: always()
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const reports = fs.readdirSync('reports')
              .filter(f => f.startsWith('review_'))
              .sort()
              .reverse();
            
            if (reports.length === 0) return;
            
            const report = fs.readFileSync(`reports/${reports[0]}`, 'utf8');
            
            await github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## 🤖 AI Code Review Report\n\n${report}`
            });
```

### 场景 2: 自动生成测试

#### 脚本实现

```bash
#!/bin/bash
# scripts/generate-tests.sh

set -e

# 配置
SOURCE_DIR="src"
TEST_DIR="tests"
COVERAGE_THRESHOLD=80

# 查找未覆盖的文件
echo "📊 分析测试覆盖率..."
npm run test:coverage > coverage_report.txt || true

# 提取未覆盖的文件
UNCOVERED_FILES=$(grep -E "^src/.*\.(js|ts)$" coverage_report.txt | \
    awk '{if ($4 < '$COVERAGE_THRESHOLD') print $1}' || true)

if [ -z "$UNCOVERED_FILES" ]; then
    echo "✅ 所有文件覆盖率达标"
    exit 0
fi

echo "📝 为以下文件生成测试:"
echo "$UNCOVERED_FILES"

# 为每个文件生成测试
for file in $UNCOVERED_FILES; do
    test_file="$TEST_DIR/$(basename $file .js).test.js"
    
    echo "生成: $test_file"
    
    PROMPT="为 $file 生成完整的单元测试，包括:\n"
    PROMPT+="1. 所有公共函数的测试\n"
    PROMPT+="2. 边界条件测试\n"
    PROMPT+="3. 错误处理测试\n"
    PROMPT+="使用 Jest 框架"
    
    if claude --print --auto-edit "$PROMPT" > "$test_file"; then
        echo "✅ 生成成功: $test_file"
    else
        echo "❌ 生成失败: $test_file"
    fi
    
    sleep 2  # 避免 API 限流
done

# 运行新生成的测试
echo "🧪 运行测试..."
npm test

echo "🎉 测试生成完成"
```

#### CI 集成

```yaml
# .github/workflows/generate-tests.yml
name: Generate Missing Tests

on:
  schedule:
    - cron: '0 2 * * 1'  # 每周一凌晨 2 点
  workflow_dispatch:  # 手动触发

jobs:
  generate-tests:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      
      - name: Install Dependencies
        run: |
          npm install
          npm install -g @anthropic-ai/claude-code
      
      - name: Generate Tests
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          chmod +x scripts/generate-tests.sh
          ./scripts/generate-tests.sh
      
      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v5
        with:
          commit-message: "🧪 自动生成缺失的测试"
          title: "🤖 AI 生成的测试用例"
          body: |
            此 PR 由 AI 自动生成，包含以下内容：
            - 为覆盖率低于 80% 的文件生成测试
            - 包括单元测试、边界测试和错误处理测试
            
            请仔细审查生成的测试代码。
          branch: tests/auto-generated
          labels: automated, tests
```

### 场景 3: 文档自动同步

#### 脚本实现

```bash
#!/bin/bash
# scripts/sync-docs.sh

set -e

# 配置
DOCS_DIR="docs"
API_DOC="$DOCS_DIR/API.md"
README="README.md"
CHANGELOG="CHANGELOG.md"

echo "📚 同步文档..."

# 1. 生成 API 文档
echo "生成 API 文档..."
PROMPT="分析 src/ 目录的所有导出函数和类，生成详细的 API 文档，包括:\n"
PROMPT+="- 函数签名\n"
PROMPT+="- 参数说明\n"
PROMPT+="- 返回值\n"
PROMPT+="- 使用示例\n"
PROMPT+="输出 Markdown 格式"

codex -q --auto-edit "$PROMPT" > "$API_DOC"

# 2. 更新 README
echo "更新 README..."
PROMPT="根据当前代码库生成 README.md，包括:\n"
PROMPT+="- 项目简介\n"
PROMPT+="- 安装说明\n"
PROMPT+="- 快速开始\n"
PROMPT+="- 主要功能\n"
PROMPT+="- 配置选项"

codex -q "$PROMPT" > "$README"

# 3. 生成 CHANGELOG
echo "生成 CHANGELOG..."
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

if [ -n "$LAST_TAG" ]; then
    COMMITS=$(git log --oneline $LAST_TAG..HEAD)
else
    COMMITS=$(git log --oneline)
fi

PROMPT="根据以下 git 提交记录生成 CHANGELOG.md:\n\n$COMMITS\n\n"
PROMPT+="按类型分组（Features, Bug Fixes, Breaking Changes）"

kiro-cli chat --no-interactive "$PROMPT" > "$CHANGELOG"

echo "✅ 文档同步完成"

# 检查是否有变更
if git diff --quiet; then
    echo "没有文档变更"
    exit 0
fi

# 显示变更
git diff --stat
```

#### GitLab CI 集成

```yaml
# .gitlab-ci.yml
sync-docs:
  stage: deploy
  image: node:18
  before_script:
    - apt-get update && apt-get install -y git curl
    - npm install -g @openai/codex
    - curl -fsSL https://cli.kiro.dev/install | bash
    - export PATH="$HOME/.kiro/bin:$PATH"
  script:
    - chmod +x scripts/sync-docs.sh
    - ./scripts/sync-docs.sh
    - |
      git config user.name "GitLab CI"
      git config user.email "ci@gitlab.com"
      git add docs/ README.md CHANGELOG.md
      git diff --staged --quiet || git commit -m "📝 自动同步文档 [skip ci]"
      git push https://oauth2:${CI_PUSH_TOKEN}@${CI_SERVER_HOST}/${CI_PROJECT_PATH}.git HEAD:${CI_COMMIT_REF_NAME}
  only:
    - main
  when: on_success
```

### 场景 4: 安全漏洞修复

#### 脚本实现

```bash
#!/bin/bash
# scripts/security-fix.sh

set -e

# 运行安全扫描
echo "🔍 运行安全扫描..."
npm audit --json > audit_report.json || true

# 检查是否有漏洞
VULNERABILITIES=$(jq '.metadata.vulnerabilities.total' audit_report.json)

if [ "$VULNERABILITIES" -eq 0 ]; then
    echo "✅ 未发现安全漏洞"
    exit 0
fi

echo "⚠️  发现 $VULNERABILITIES 个安全漏洞"

# 提取漏洞详情
VULN_DETAILS=$(jq -r '.vulnerabilities | to_entries[] | 
    "\(.key): \(.value.severity) - \(.value.via[0].title)"' audit_report.json)

# AI 分析和修复
PROMPT="发现以下安全漏洞:\n\n$VULN_DETAILS\n\n"
PROMPT+="请:\n"
PROMPT+="1. 分析每个漏洞的影响\n"
PROMPT+="2. 更新 package.json 中的依赖版本\n"
PROMPT+="3. 如果需要代码修改，请一并处理\n"
PROMPT+="4. 生成修复报告"

echo "🤖 AI 分析和修复..."
claude --print --auto-edit "$PROMPT" > security_fix_report.md

# 尝试自动修复
npm audit fix --force || true

# 验证修复
npm audit --json > audit_report_after.json || true
VULNERABILITIES_AFTER=$(jq '.metadata.vulnerabilities.total' audit_report_after.json)

echo "修复前: $VULNERABILITIES 个漏洞"
echo "修复后: $VULNERABILITIES_AFTER 个漏洞"

if [ "$VULNERABILITIES_AFTER" -lt "$VULNERABILITIES" ]; then
    echo "✅ 部分漏洞已修复"
else
    echo "⚠️  需要手动处理"
fi
```

#### Jenkins Pipeline

```groovy
pipeline {
    agent any
    
    triggers {
        cron('H 2 * * *')  // 每天凌晨 2 点
    }
    
    environment {
        ANTHROPIC_API_KEY = credentials('anthropic-api-key')
    }
    
    stages {
        stage('Security Scan') {
            steps {
                sh 'npm install'
                sh 'npm audit --json > audit_report.json || true'
            }
        }
        
        stage('AI Security Fix') {
            when {
                expression {
                    def report = readJSON file: 'audit_report.json'
                    return report.metadata.vulnerabilities.total > 0
                }
            }
            steps {
                sh '''
                    npm install -g @anthropic-ai/claude-code
                    chmod +x scripts/security-fix.sh
                    ./scripts/security-fix.sh
                '''
            }
        }
        
        stage('Create Fix PR') {
            when {
                expression {
                    return sh(
                        script: 'git diff --quiet',
                        returnStatus: true
                    ) != 0
                }
            }
            steps {
                sh '''
                    git checkout -b security/auto-fix-$(date +%Y%m%d)
                    git add .
                    git commit -m "🔒 AI 自动修复安全漏洞"
                    git push origin HEAD
                '''
                
                // 创建 PR（需要 GitHub/GitLab API）
                script {
                    // 实现 PR 创建逻辑
                }
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: '*_report.*', allowEmptyArchive: true
        }
        failure {
            emailext(
                subject: "安全修复失败: ${env.JOB_NAME}",
                body: "请查看 Jenkins 日志",
                to: "security-team@example.com"
            )
        }
    }
}
```

---

## 最佳实践

### 1. 安全性

#### API 密钥管理

```bash
# ❌ 错误：硬编码密钥
export KIRO_API_KEY="sk-xxx"

# ✅ 正确：使用环境变量
export KIRO_API_KEY="${KIRO_API_KEY}"

# ✅ 正确：使用密钥管理服务
KIRO_API_KEY=$(aws secretsmanager get-secret-value \
    --secret-id kiro-api-key \
    --query SecretString \
    --output text)
```

#### 权限最小化

```bash
# ❌ 危险：信任所有工具
kiro-cli chat --no-interactive --trust-all-tools "任务"

# ✅ 安全：仅信任必要工具
kiro-cli chat --no-interactive \
    --trust-tools "read_file,search_files" \
    "任务"

# ✅ 最安全：只读操作
kiro-cli chat --no-interactive \
    --trust-tools "read_file" \
    "分析代码"
```

#### 输入验证

```bash
#!/bin/bash

# 验证用户输入
validate_input() {
    local input=$1
    
    # 检查危险字符
    if echo "$input" | grep -qE '[;&|`$]'; then
        echo "❌ 输入包含危险字符" >&2
        return 1
    fi
    
    # 检查长度
    if [ ${#input} -gt 1000 ]; then
        echo "❌ 输入过长" >&2
        return 1
    fi
    
    return 0
}

# 使用
USER_INPUT="$1"
if validate_input "$USER_INPUT"; then
    kiro-cli chat --no-interactive "$USER_INPUT"
fi
```

### 2. 错误处理

#### 完整错误处理模板

```bash
#!/bin/bash

# 严格模式
set -euo pipefail

# 错误追踪
trap 'handle_error $? $LINENO' ERR

handle_error() {
    local exit_code=$1
    local line_number=$2
    
    echo "❌ 错误: 退出码 $exit_code，行号 $line_number" >&2
    
    # 记录日志
    echo "[$(date)] 错误: $exit_code @ $line_number" >> error.log
    
    # 清理临时文件
    cleanup
    
    # 发送通知
    send_notification "AI 任务失败"
    
    exit $exit_code
}

cleanup() {
    rm -f /tmp/ai_task_*
}

send_notification() {
    local message=$1
    # 实现通知逻辑（Slack、Email 等）
}

# 主逻辑
main() {
    echo "开始执行..."
    
    # 执行 AI 任务
    kiro-cli chat --no-interactive "$@" || {
        echo "AI 任务失败" >&2
        return 1
    }
    
    echo "完成"
}

main "$@"
```

### 3. 性能优化

#### 并行执行

```bash
#!/bin/bash

# 使用 GNU parallel
parallel -j 4 --halt soon,fail=1 \
    kiro-cli chat --no-interactive ::: \
    "任务1" \
    "任务2" \
    "任务3" \
    "任务4"

# 或使用后台任务
pids=()

for task in "任务1" "任务2" "任务3"; do
    kiro-cli chat --no-interactive "$task" &
    pids+=($!)
done

# 等待所有任务完成
for pid in "${pids[@]}"; do
    wait $pid || exit 1
done
```

#### 缓存结果

```bash
#!/bin/bash

CACHE_DIR=".ai_cache"
mkdir -p "$CACHE_DIR"

ai_task_cached() {
    local task=$1
    local cache_key=$(echo -n "$task" | md5sum | cut -d' ' -f1)
    local cache_file="$CACHE_DIR/$cache_key"
    
    # 检查缓存
    if [ -f "$cache_file" ]; then
        local age=$(($(date +%s) - $(stat -c %Y "$cache_file")))
        if [ $age -lt 3600 ]; then  # 1 小时内有效
            echo "使用缓存结果"
            cat "$cache_file"
            return 0
        fi
    fi
    
    # 执行任务并缓存
    kiro-cli chat --no-interactive "$task" | tee "$cache_file"
}

# 使用
ai_task_cached "分析代码质量"
```

### 4. 监控和日志

#### 结构化日志

```bash
#!/bin/bash

LOG_FILE="ai_tasks.log"

log() {
    local level=$1
    shift
    local message="$*"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    # JSON 格式日志
    echo "{\"timestamp\":\"$timestamp\",\"level\":\"$level\",\"message\":\"$message\"}" \
        | tee -a "$LOG_FILE"
}

log "INFO" "开始执行 AI 任务"

if kiro-cli chat --no-interactive "$TASK" 2>&1 | tee -a "$LOG_FILE"; then
    log "INFO" "任务成功完成"
else
    log "ERROR" "任务执行失败"
    exit 1
fi
```

#### 指标收集

```bash
#!/bin/bash

# 记录执行时间
START_TIME=$(date +%s)

kiro-cli chat --no-interactive "$TASK"

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# 发送指标到监控系统
curl -X POST https://metrics.example.com/api/metrics \
    -H "Content-Type: application/json" \
    -d "{
        \"metric\": \"ai_task_duration\",
        \"value\": $DURATION,
        \"tags\": {
            \"task\": \"$TASK\",
            \"status\": \"success\"
        }
    }"
```

### 5. 测试

#### 单元测试

```bash
#!/bin/bash
# tests/test_ai_integration.sh

test_ai_code_review() {
    local result
    result=$(kiro-cli chat --no-interactive \
        --trust-tools "read_file" \
        "审查 test_file.py" 2>&1)
    
    # 验证输出包含预期内容
    if echo "$result" | grep -q "代码质量"; then
        echo "✅ test_ai_code_review 通过"
        return 0
    else
        echo "❌ test_ai_code_review 失败"
        return 1
    fi
}

test_ai_error_handling() {
    # 测试错误处理
    if kiro-cli chat --no-interactive "无效任务" 2>/dev/null; then
        echo "❌ test_ai_error_handling 失败：应该返回错误"
        return 1
    else
        echo "✅ test_ai_error_handling 通过"
        return 0
    fi
}

# 运行测试
test_ai_code_review
test_ai_error_handling
```

---

## 故障排查

### 常见问题

#### 1. 认证失败

```bash
# 问题：API 密钥无效
Error: Authentication failed

# 解决方案
# 检查环境变量
echo $KIRO_API_KEY

# 重新登录
kiro-cli logout
kiro-cli login

# 验证
kiro-cli whoami
```

#### 2. 超时问题

```bash
# 问题：任务执行超时
Error: Request timeout

# 解决方案：增加超时时间
timeout 600 kiro-cli chat --no-interactive "$TASK"

# 或分解任务
kiro-cli chat --no-interactive "步骤1"
kiro-cli chat --no-interactive "步骤2"
```

#### 3. 权限错误

```bash
# 问题：工具权限不足
Error: Tool 'write_file' not trusted

# 解决方案：添加信任
kiro-cli chat --no-interactive \
    --trust-tools "write_file" \
    "$TASK"
```

#### 4. 输出解析失败

```bash
# 问题：输出格式不符合预期

# 解决方案：明确指定输出格式
PROMPT="$TASK\n\n输出格式：JSON\n示例：{\"result\": \"...\"}"
kiro-cli chat --no-interactive "$PROMPT"
```

### 调试技巧

```bash
# 启用详细日志
export KIRO_LOG_LEVEL=debug
kiro-cli chat --no-interactive "$TASK"

# 保存完整输出
kiro-cli chat --no-interactive "$TASK" \
    > output.txt 2> error.txt

# 逐步执行
set -x  # 显示每个命令
kiro-cli chat --no-interactive "$TASK"
set +x
```

---

## 总结

### 关键要点

1. **非交互参数**是 CI/CD 集成的核心
2. **错误处理**和**重试机制**必不可少
3. **安全性**优先：最小权限原则
4. **监控和日志**帮助快速定位问题
5. **测试**确保集成稳定性

### 推荐工具组合

| 场景 | 推荐工具 | 关键参数 |
|------|---------|---------|
| 代码审查 | Kiro CLI | `--no-interactive --trust-tools "read_file"` |
| 自动修复 | Claude Code | `--print --auto-edit` |
| 测试生成 | Codex CLI | `-q --auto-edit` |
| 文档生成 | Kiro CLI | `--no-interactive` |

### 下一步

1. 选择适合的工具
2. 编写测试脚本
3. 在开发环境验证
4. 逐步集成到 CI/CD
5. 监控和优化

---

**文档版本**: 1.0  
**最后更新**: 2026-03-05  
**维护者**: AI-CLI Team
