# 项目熟悉指南 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 编写一份基于当前源码的中文综合指南，帮助新维护者先运行项目，再理解前端、API、多智能体、数据库、RAG、测试和已知风险。

**Architecture:** 在仓库根目录新增单一入口文档 `PROJECT_GUIDE.md`，按“快速上手 -> 业务数据流 -> 源码导读 -> 维护参考”的顺序组织。所有事实从当前代码、配置和测试中提取，敏感环境变量只记录名称和用途，不记录实际值。

**Tech Stack:** Markdown、Vue 3、TypeScript、Vite、FastAPI、SQLAlchemy、MySQL、PostgreSQL、LangChain、LangGraph、DashScope、Tavily

---

## File Structure

- Create: `PROJECT_GUIDE.md`
  - 面向新维护者的唯一综合入口，包含启动、架构、源码、接口、测试和风险。
- Create: `docs/superpowers/plans/2026-06-14-project-guide.md`
  - 记录本次文档工作的执行步骤和验证方法。
- Reference only: `frontend/src/**`, `frontend/package.json`, `frontend/.env`
  - 核对前端入口、路由、页面、接口调用和运行命令。
- Reference only: `servicebackend/main.py`, `servicebackend/app/**`, `servicebackend/tests/**`
  - 核对后端入口、路由、多智能体、数据库、RAG 和测试。

### Task 1: 建立源码事实清单

**Files:**
- Reference: `frontend/src/main.ts`
- Reference: `frontend/src/router/index.js`
- Reference: `frontend/src/views/HomeView.vue`
- Reference: `frontend/src/views/LoginView.vue`
- Reference: `frontend/src/views/RegisterView.vue`
- Reference: `servicebackend/main.py`
- Reference: `servicebackend/app/api/*.py`
- Reference: `servicebackend/app/agents/*.py`
- Reference: `servicebackend/app/database/*.py`
- Reference: `servicebackend/app/rag/document_extractor.py`
- Reference: `servicebackend/tests/*.py`

- [x] **Step 1: 列出前后端源码文件**

Run:

```powershell
Get-ChildItem .\frontend\src, .\servicebackend\app, .\servicebackend\tests -Recurse -File |
  Where-Object { $_.FullName -notmatch '\\__pycache__\\' } |
  Select-Object -ExpandProperty FullName
```

Expected: 输出 Vue 页面、FastAPI 路由、Agent、数据库、RAG 和测试文件。

- [x] **Step 2: 核对已注册的 FastAPI 路由**

Run:

```powershell
Get-Content .\servicebackend\main.py -Encoding UTF8
Get-ChildItem .\servicebackend\app\api\*.py |
  ForEach-Object {
    Select-String $_.FullName -Pattern '@router\.(get|post|put|delete|patch)\('
  }
```

Expected: 主应用注册 `/auth`、`/chat`、`/conversations`；源码另有文档上传路由，需要在风险章节说明其接线状态。

- [x] **Step 3: 核对前端真实接口调用**

Run:

```powershell
Get-ChildItem .\frontend\src\views\*.vue |
  ForEach-Object {
    Select-String $_.FullName -Pattern 'axios\.|fetch\('
  }
```

Expected: 能识别登录、注册、会话、聊天、偏好和文档上传调用。

- [x] **Step 4: 核对数据库与多智能体职责**

Run:

```powershell
Get-Content .\servicebackend\app\database\mysql.py -Encoding UTF8
Get-Content .\servicebackend\app\database\postgres.py -Encoding UTF8
Get-Content .\servicebackend\app\agents\multi_agent.py -Encoding UTF8
Get-Content .\servicebackend\app\agents\supervisor.py -Encoding UTF8
Get-Content .\servicebackend\app\agents\memory.py -Encoding UTF8
```

Expected: 能描述 MySQL 认证、PostgreSQL 会话与记忆，以及 Supervisor 和专业 Agent 的协作关系。

### Task 2: 编写综合项目指南

**Files:**
- Create: `PROJECT_GUIDE.md`

- [x] **Step 1: 写入项目概览和快速启动**

内容必须包括：

```markdown
# 智能医疗助手项目熟悉指南

## 1. 项目概览
## 2. 五分钟快速启动
## 3. 环境变量与外部依赖
```

启动命令必须使用当前目录：

```powershell
cd E:\AprojectDmeo\AI-Medical-Assistant\servicebackend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py

cd E:\AprojectDmeo\AI-Medical-Assistant\frontend
npm install
npm run dev
```

同时说明后端默认由 `.env` 的 `HOST`、`PORT` 决定，前端使用 `VITE_BACKEND_URL`，API 文档位于 `/docs`。

- [x] **Step 2: 写入目录结构和推荐阅读顺序**

内容必须包括：

```markdown
## 4. 目录结构
## 5. 推荐阅读顺序
```

阅读顺序从 `frontend/src/main.ts`、路由和 `HomeView.vue` 开始，再进入 `servicebackend/main.py`、API、`multi_agent.py`、各专业 Agent、记忆和 RAG。

- [x] **Step 3: 写入四条核心业务流程**

内容必须包括：

```markdown
## 6. 核心业务流程
### 6.1 注册与登录
### 6.2 会话管理
### 6.3 发送医疗问题
### 6.4 上传医疗文档
```

每条流程使用编号步骤或 Mermaid 流程图，明确前端页面、HTTP 接口、后端模块和数据库/Agent 的关系。

- [x] **Step 4: 写入源码深入导读**

内容必须包括：

```markdown
## 7. 前端源码导读
## 8. 后端 API 与认证
## 9. 多智能体系统
## 10. 数据库与记忆
## 11. RAG 文档处理
```

所有模块说明必须引用仓库相对路径，并区分当前实际路由与未接入功能。

- [x] **Step 5: 写入维护参考**

内容必须包括：

```markdown
## 12. API 速查表
## 13. 测试与调试
## 14. 当前实现注意事项
## 15. 后续开发建议
## 16. 快速排障
```

注意事项至少覆盖：

- `medical_upload.py` 未在 `main.py` 注册。
- 前端调用了 `/preferences/*`，但当前主入口未注册偏好路由。
- 前端同时存在 `router/index.js` 和 `router/index.ts`，实际解析需要结合模块解析结果确认。
- `HomeView.vue` 体积较大且包含未使用代码。
- 启动后端时会尝试连接并建表，外部数据库不可用会影响功能。
- 测试主要覆盖路由存在性和聊天消息提取，覆盖面有限。
- 医疗建议属于辅助信息，产品化前需要完善安全提示和合规边界。

### Task 3: 验证文档准确性

**Files:**
- Verify: `PROJECT_GUIDE.md`

- [x] **Step 1: 检查章节和占位符**

Run:

```powershell
Select-String .\PROJECT_GUIDE.md -Pattern '^## '
$placeholderPattern = @('TB' + 'D', 'TO' + 'DO', '待' + '定', '稍后' + '补充') -join '|'
Select-String .\PROJECT_GUIDE.md -Pattern $placeholderPattern
```

Expected: 章节 1 至 16 均存在；占位符搜索无输出。

- [x] **Step 2: 检查文档引用的关键文件**

Run:

```powershell
$paths = @(
  'frontend/src/main.ts',
  'frontend/src/router/index.js',
  'frontend/src/views/HomeView.vue',
  'servicebackend/main.py',
  'servicebackend/app/api/chat.py',
  'servicebackend/app/agents/multi_agent.py',
  'servicebackend/app/agents/memory.py',
  'servicebackend/app/rag/document_extractor.py'
)
$paths | ForEach-Object { "$($_): $(Test-Path $_)" }
```

Expected: 每一项均为 `True`。

- [x] **Step 3: 检查路由表与源码一致**

Run:

```powershell
Select-String .\PROJECT_GUIDE.md -Pattern '/auth/register|/auth/token|/chat/send|/conversations/create|/conversations/list|/conversations/get|/conversations/delete'
```

Expected: 所有当前主应用路由均出现在 API 速查表中。

- [x] **Step 4: 运行已有构建和测试**

Run:

```powershell
cd .\frontend
npm run build

cd ..\servicebackend
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Expected: 前端构建成功；后端测试通过，或如外部数据库初始化导致失败则准确记录失败原因。

- [x] **Step 5: 检查 Markdown 和 Git 差异**

Run:

```powershell
cd E:\AprojectDmeo\AI-Medical-Assistant
git diff --check
git status --short
```

Expected: `git diff --check` 无错误；状态只包含本次计划和指南文档。

- [x] **Step 6: 提交正式指南**

```powershell
git add PROJECT_GUIDE.md docs/superpowers/plans/2026-06-14-project-guide.md
git commit -m "docs: add project onboarding guide"
```
