# harness-engineering
## 一、全局说明
* `docs/`：架构原则与最佳实践
* `.skills/`：稳定能力
* `.agents/`：角色约束
* `.commands/`：启动与编排
* `.harness/`：运行时状态与项目记忆

### 1. Web 和 Backend 共用同一套流程骨架

流程是：

* orchestrator 启动
* planner 规划
* generator 实现
* evaluator 验证
* 不通过则回流修复
* 全部 feature `passes=true` 后完成
 

---

## 二、可直接落地的标准目录

### 2.1 仓库级标准目录

```text
repo-root/
├── .harness/
│   ├── project.json
│   ├── feature_list.json
│   ├── spec.md
│   ├── design_tokens.json
│   ├── api_contracts/
│   ├── domain_model.md
│   ├── sprint_plan.json
│   ├── run_state.json
│   ├── progress.md
│   ├── decisions.md
│   ├── risks.md
│   ├── evaluator_reports/
│   ├── artifacts/
│   └── sprints/
│       ├── sprint_01_contract.md
│       ├── sprint_01_handoff.md
│       ├── sprint_01_eval.md
│       └── ...
│
├── .agents/
│   ├── planner.md
│   ├── generator.md
│   ├── evaluator.md
│   └── reviewer.md
│
├── .skills/
│   ├── harness-core/
│   │   ├── SKILL.md
│   │   └── templates/
│   ├── harness-planning/
│   │   ├── SKILL.md
│   │   └── templates/
│   ├── harness-generation/
│   │   ├── SKILL.md
│   │   └── templates/
│   ├── harness-evaluation/
│   │   ├── SKILL.md
│   │   └── templates/
│   ├── web-delivery/
│   │   ├── SKILL.md
│   │   └── templates/
│   └── backend-delivery/
│       ├── SKILL.md
│       └── templates/
│
├── .commands/
│   ├── start-harness.md
│   ├── plan-project.md
│   ├── run-sprint.md
│   ├── evaluate-sprint.md
│   └── close-project.md
│
├── scripts/
│   ├── validate_harness_state.py
│   ├── validate_feature_schema.py
│   ├── enforce_state_transition.py
│   ├── summarize_eval_report.py
│   └── bootstrap_harness.py
│
├── docs/
│   ├── harness-architecture.md
│   ├── harness-best-practices.md
│   ├── engineering-standards.md
│   ├── coding-standards.md
│   └── testing-standards.md
│
├── apps/
│   ├── web/
│   └── backend/
│
├── tests/
│   ├── e2e/
│   ├── integration/
│   ├── contract/
│   └── unit/
│
└── ci/
    ├── pipeline.yml
    └── quality-gates.yml
```

---

### 2.2 Web 项目目录建议

```text
apps/web/
├── src/
│   ├── app/
│   ├── pages/
│   ├── modules/
│   ├── components/
│   ├── services/
│   ├── hooks/
│   ├── store/
│   ├── styles/
│   ├── utils/
│   └── types/
├── public/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── visual/
├── playwright/
│   ├── specs/
│   ├── fixtures/
│   └── reports/
└── package.json
```
 
---

### 2.3 Backend 项目目录建议

```text
apps/backend/
├── src/
│   ├── api/
│   │   ├── controllers/
│   │   ├── dto/
│   │   └── routes/
│   ├── application/
│   │   ├── services/
│   │   ├── commands/
│   │   └── queries/
│   ├── domain/
│   │   ├── entities/
│   │   ├── value_objects/
│   │   ├── repositories/
│   │   └── policies/
│   ├── infrastructure/
│   │   ├── persistence/
│   │   ├── mq/
│   │   ├── cache/
│   │   └── external_clients/
│   ├── jobs/
│   ├── config/
│   └── utils/
├── migrations/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── contract/
│   └── e2e/
└── pyproject.toml / package.json / pom.xml
```
 
* Backend 不需要 `design_tokens` 作为核心输入，但仍需要 `api_contracts/`、`domain_model.md`、`contract tests`，这样 planner 和 evaluator 才有可验证依据。

---

## 三、`.harness/` 标准模板清单

下面这些文件是**必须有**的。没有它们，agent 只能“理解概念”，不能稳定执行。

---

### 3.1 `project.json`

定义项目元信息和类型。

```json id="6tw0m"
{
  "project_name": "order-center",
  "project_type": "backend",
  "delivery_mode": "incremental",
  "stack": ["python", "fastapi", "postgres", "redis"],
  "modules": ["order", "payment", "refund"],
  "quality_gate": {
    "min_eval_score": 80,
    "blocker_allowed": 0,
    "max_rework_rounds_per_sprint": 3
  },
  "entrypoints": {
    "planner": ".agents/planner.md",
    "generator": ".agents/generator.md",
    "evaluator": ".agents/evaluator.md"
  }
}
```

---

### 3.2 `feature_list.json`

“唯一可信来源”

```json id="03bxj"
[
  {
    "id": "FEAT-001",
    "name": "创建订单",
    "module": "order",
    "type": "backend_api",
    "priority": "P0",
    "status": "planned",
    "passes": false,
    "dependencies": [],
    "inputs": ["user_id", "items", "address_id"],
    "outputs": ["order_id", "status", "amount"],
    "acceptance_criteria": [
      "请求参数校验完整",
      "订单创建成功并持久化",
      "返回统一响应结构",
      "异常场景有明确错误码"
    ],
    "test_scope": ["unit", "integration", "contract"],
    "owner": "generator",
    "last_eval_score": 0,
    "notes": ""
  }
]
```

Web 版可把 `type` 换成 `page`, `component`, `flow`, `api_integration`。

---

### 3.3 `spec.md`

项目规格总文档，面向 planner 输出。

```md 
id="327tz"
# Project Specification

## 1. Business Goal
## 2. User / Caller Scenarios
## 3. Functional Scope
## 4. Non-functional Requirements
## 5. Constraints
## 6. Module Boundaries
## 7. Acceptance Principles
## 8. Out of Scope
## 9. Assumptions
## 10. Risks
```

要求：

* Backend 必须写接口边界、数据一致性、错误码策略
* Web 必须写用户路径、页面状态、交互反馈规则

---

### 3.4 `domain_model.md`

后端尤其需要，Web 复杂业务也建议有。

```md id="h1rhk"
# Domain Model

## Entities
- Order
- Payment
- Refund

## Value Objects
- Money
- Address
- OrderItem

## State Transitions
- CREATED -> PAID -> FULFILLED
- CREATED -> CANCELLED

## Invariants
- Paid order cannot be deleted
- Refund amount cannot exceed paid amount
```

---

### 3.5 `design_tokens.json`

视觉标识文件；Backend 可为空对象或不作为必填。

```json id="l0suh"
{
  "theme": "default",
  "colors": {
    "primary": "#2563eb",
    "danger": "#dc2626"
  },
  "typography": {
    "font_family": "Inter",
    "base_size": "14px"
  },
  "spacing": {
    "sm": 8,
    "md": 12,
    "lg": 16
  },
  "anti_patterns": [
    "Do not mix more than 3 primary actions in one screen",
    "Do not use hard-coded inline colors"
  ]
}
```

---

### 3.6 `api_contracts/`

前后端都建议有，尤其适合 evaluator 做 contract 校验。

目录示例：

```text
.harness/api_contracts/
├── order-create.yaml
├── order-detail.yaml
└── common-error-codes.yaml
```

单文件模板：

```yaml id="m4isk"
name: CreateOrder
method: POST
path: /api/orders
request:
  body:
    user_id: string
    items:
      - sku_id: string
        quantity: integer
response:
  200:
    order_id: string
    status: string
    amount: number
  400:
    code: INVALID_ARGUMENT
    message: string
```

---

### 3.7 `sprint_plan.json`
  sprint_plan 很重要，但还需要固定字段。

```json id="myehy"
{
  "total_sprints": 3,
  "current_sprint": 1,
  "sprints": [
    {
      "sprint_no": 1,
      "goal": "完成订单创建主链路",
      "feature_ids": ["FEAT-001", "FEAT-002"],
      "depends_on": [],
      "exit_criteria": [
        "相关 feature evaluator score >= 80",
        "无 blocker",
        "所有 contract tests 通过"
      ]
    }
  ]
}
```

---

### 3.8 `run_state.json`

把“状态设计”正式机读化。

```json id="kaj0i"
{
  "run_id": "2026-04-16-001",
  "current_state": "PLANNING",
  "current_sprint": 1,
  "current_feature_ids": [],
  "retry_count": 0,
  "last_score": 0,
  "blockers": 0,
  "updated_at": "2026-04-16T10:00:00Z",
  "handoff_from": "",
  "handoff_to": "planner"
}
```

状态枚举建议固定为：

```text
INIT
PLANNING
PLAN_READY
GENERATING
GENERATED
EVALUATING
REWORK_REQUIRED
PASSED
DONE
FAILED
```

---

### 3.9 `progress.md`

 持续构建 

```md id="95ltb"
# Progress Log

- 2026-04-16 10:00 INIT completed
- 2026-04-16 10:10 PLANNING started
- 2026-04-16 10:40 PLAN_READY
- 2026-04-16 11:00 GENERATING sprint 1
- 2026-04-16 11:40 EVALUATING sprint 1
- 2026-04-16 11:55 REWORK_REQUIRED score=72 blocker=1
```

---

### 3.10 `decisions.md`

沉淀关键工程决策，防止 agent 每轮重复推翻。

```md id="glmfy"
# Architecture Decisions

## ADR-001
Decision: Use optimistic locking for order updates
Reason: Prevent concurrent overwrite

## ADR-002
Decision: Web list page uses cursor pagination
Reason: Better consistency for dynamic datasets
```

---

### 3.11 `risks.md`

 合理性评估、风险意识显式化。

```md id="x60id"
# Risks

- RISK-001: External payment API unstable
- RISK-002: Legacy schema lacks unique constraints
- RISK-003: UI mock not finalized
```

---

### 3.12 `sprints/sprint_XX_contract.md`

这是 sprint 的执行合同，最关键。

```md id="gs49z"
# Sprint 01 Contract

## Goal
完成订单创建主链路

## Included Features
- FEAT-001 创建订单
- FEAT-002 查询订单详情

## Allowed Changes
- apps/backend/src/api/**
- apps/backend/src/application/**
- apps/backend/src/domain/**
- tests/contract/**
- tests/integration/**

## Forbidden Changes
- payment module
- shared auth middleware
- CI pipeline

## Acceptance Criteria
- 所有 included features 的 acceptance criteria 达成
- contract test 全通过
- 无 blocker

## Handoff Requirements
- 更新 feature_list.json
- 更新 run_state.json
- 更新 progress.md
- 输出变更摘要
```

---

### 3.13 `sprints/sprint_XX_handoff.md`

generator 交接 evaluator 时必须填写。

```md id="n7c4m"
# Sprint 01 Handoff

## Changed Files
## Implemented Features
## Known Limitations
## Tests Added
## Areas Requiring Special Attention
```

---

## 3.14 `evaluator_reports/sprint_XX_eval.json`

让评分结构化。

```json id="lkvqn"
{
  "sprint_no": 1,
  "score": 82,
  "passed": true,
  "blockers": [],
  "major_issues": [],
  "minor_issues": [
    "Error message is not standardized"
  ],
  "test_summary": {
    "unit_passed": 18,
    "integration_passed": 7,
    "contract_passed": 5,
    "e2e_passed": 0
  },
  "verdict": "PASS"
}
```

---

## 四、`.agents/` 模板

### 4.1 `planner.md`

```md id="bi1pd"
# Planner Agent

## Role
你负责把需求转化为项目可执行资产，不编写业务代码。

## Must Read
- .skills/harness-core/SKILL.md
- .skills/harness-planning/SKILL.md
- .harness/project.json
- existing .harness/* files

## Responsibilities
- 生成或更新 spec.md
- 生成或更新 feature_list.json
- 生成或更新 sprint_plan.json
- 补充 domain_model.md / api_contracts 如需要
- 标记 assumptions / risks / out-of-scope

## Must Not
- 不得实现业务代码
- 不得跳过 acceptance criteria
- 不得生成未授权功能

## Completion Signal
输出：PLAN_READY
并确保所有规划文件通过 schema 校验
```

---

### 4.2 `generator.md`

```md id="9hmhk"
# Generator Agent

## Role
你负责实现当前 sprint 已批准范围内的功能。

## Must Read
- .skills/harness-core/SKILL.md
- .skills/harness-generation/SKILL.md
- .harness/feature_list.json
- .harness/sprint_plan.json
- .harness/run_state.json
- current sprint contract

## Responsibilities
- 仅实现当前 sprint feature
- 仅修改 allowed changes 范围内文件
- 为变更补充对应测试
- 更新 handoff / progress / feature 状态

## Must Not
- 不得跨 sprint 扩 scope
- 不得修改 forbidden changes
- 不得自评通过

## Completion Signal
输出：GENERATED
并生成 sprint handoff
```

---

### 4.3 `evaluator.md`

```md id="1as6q"
# Evaluator Agent

## Role
你负责验证成果是否达到放行标准。你的职责是发现问题，而不是赞美结果。

## Must Read
- .skills/harness-core/SKILL.md
- .skills/harness-evaluation/SKILL.md
- current sprint contract
- sprint handoff
- feature_list.json

## Responsibilities
- 执行测试
- 根据 acceptance criteria 验收
- 输出 blocker / major / minor issue
- 生成 evaluator report
- 更新 feature passes / score

## Must Not
- 不得实现修复
- 不得跳过失败项
- 不得在存在 blocker 时判定通过

## Completion Signal
输出：PASSED 或 REWORK_REQUIRED
```

---

## 五、`.skills/` 模板

### 5.1 `harness-core/SKILL.md`

```md id="13r7v"
# Harness Core Skill

## Purpose
定义通用 harness 运行规则。

## Rules
1. .harness/ 是唯一项目运行时记忆目录
2. feature_list.json 是唯一可信功能来源
3. 所有状态变更必须更新 run_state.json
4. 所有阶段变更必须追加 progress.md
5. 禁止 background 模式执行关键流程
6. 未经 evaluator 放行不得推进 sprint
7. 所有 feature passes=true 才允许 DONE
```

关键约束：唯一可信源、command 串行、禁止 background、全部 passes 才完成。

---

### 5.2 `harness-planning/SKILL.md`

```md id="2g8qv"
# Harness Planning Skill

## Purpose
将需求扩展为可执行规划。

## Checklist
- 需求边界
- 模块拆分
- feature 列表
- acceptance criteria
- sprint 划分
- 风险与假设
- out of scope
```

---

### 5.3 `harness-generation/SKILL.md`

```md id="j1f5d"
# Harness Generation Skill

## Purpose
按 sprint 合同实现功能。

## Rules
- 只实现当前 sprint
- 只修改允许范围
- 每个 feature 必须有对应测试
- 输出 handoff 摘要
- 更新 feature 状态
```

---

### 5.4 `harness-evaluation/SKILL.md`

```md id="q0mfs"
# Harness Evaluation Skill

## Purpose
评估 sprint 成果是否达标。

## Score Dimensions
- 功能符合度
- 测试通过率
- 边界遵守度
- 稳定性
- 错误处理
- Web 时额外检查 UI 一致性
- Backend 时额外检查 API 合约与数据一致性
```

---

### 5.5 `web-delivery/SKILL.md`

```md id="oqvaf"
# Web Delivery Skill

## Scope
用于页面、组件、交互流、前后端联调。

## Additional Rules
- 必须遵守 design_tokens.json
- 主流程必须有 Playwright 用例
- 表单需覆盖 loading / success / error 状态
- 列表页需覆盖 empty / loaded / error 状态
```

---

### 5.6 `backend-delivery/SKILL.md`

```md id="r4xmd"
# Backend Delivery Skill

## Scope
用于 API、服务、数据流、异步任务。

## Additional Rules
- API 必须符合 api_contracts
- 关键服务必须有 unit + integration tests
- DB 变更必须包含 migration
- 错误码必须统一
- 领域状态转换必须符合 domain_model.md
```

---

## 六、`.commands/` 模板

### 6.1 `start-harness.md`

```text id="3bbcn"
你正在启动 harness 工作框架，目标：$ARGUMENTS

执行顺序：
1. 初始化 .harness/ 必要文件
2. 触发 planner
3. planner 完成后检查 sprint_plan.json
4. 启动当前 sprint 的 generator
5. generator 完成后启动 evaluator
6. 若 evaluator 判定 REWORK_REQUIRED，则返回 generator
7. 若所有 feature passes=true，则标记 DONE

约束：
- 禁止 background
- 所有状态必须写入 run_state.json
- 所有阶段必须写入 progress.md
```

这个命令模板是  command 样例的通用化改写。

---

### 6.2 `plan-project.md`

```text id="yd1i8"
读取 .skills/harness-core 与 .skills/harness-planning。
基于输入需求，生成或更新：
- .harness/spec.md
- .harness/feature_list.json
- .harness/sprint_plan.json
- .harness/domain_model.md
- .harness/risks.md
完成后输出 PLAN_READY。
```

---

### 6.3 `run-sprint.md`

```text id="s1kg7"
读取当前 sprint 合同与所有相关 .harness 文件。
只实现当前 sprint 范围内功能。
更新 handoff、feature 状态、progress。
完成后输出 GENERATED。
```

---

### 6.4 `evaluate-sprint.md`

```text id="ibt3w"
读取当前 sprint 合同、handoff、feature_list.json。
执行对应测试并生成 evaluator report。
若存在 blocker 或 score < 阈值，则输出 REWORK_REQUIRED。
否则输出 PASSED。
```

---

## 七、脚本与校验清单

这些不是“可选项”，而是让 harness 真正工程化的关键。

## 必备脚本

* `bootstrap_harness.py`：初始化模板文件
* `validate_feature_schema.py`：校验 `feature_list.json`
* `enforce_state_transition.py`：校验状态转移是否合法
* `summarize_eval_report.py`：归总报告
* `validate_contract_consistency.py`：检查 sprint 合同与 feature 是否一致

### 必备校验

* schema 校验
* 状态流转校验
* forbidden changes 校验
* 测试覆盖校验
* report 结构校验

---

## 八、适配 Web 与 Backend 的差异规则

### Web 侧额外要求

* 必须维护 `design_tokens.json`
* evaluator 必须包含 Playwright
* feature 更偏页面/组件/流程
* handoff 要强调交互状态与视觉一致性

### Backend 侧额外要求

* 必须维护 `api_contracts/`
* 建议维护 `domain_model.md`
* evaluator 必须包含 contract + integration tests
* feature 更偏接口/服务/领域规则/任务流

### Fullstack 侧建议

同一套 `.harness/`，但 feature 需标记 `type`：

* `web_page`
* `web_flow`
* `backend_api`
* `backend_job`
* `integration`

这样一个 sprint 可同时包含 Web 和 Backend feature，但 evaluator 要按类型分别验收。

---

## 九、最小可执行版本

若你要先快速落地，不必一次全上。最小必需集如下：

```text
.harness/
  project.json
  feature_list.json
  spec.md
  sprint_plan.json
  run_state.json
  progress.md
  sprints/sprint_01_contract.md

.agents/
  planner.md
  generator.md
  evaluator.md

.skills/
  harness-core/
  harness-planning/
  harness-generation/
  harness-evaluation/

.commands/
  start-harness.md
```

Web 再补：

* `design_tokens.json`
* `playwright/`

Backend 再补：

* `api_contracts/`
* `domain_model.md`

---

## 十、最终建议

最适合直接开工的命名与结构是：

* **统一总目录**：`.harness/`
* **统一流程骨架**：planner → generator → evaluator
* **统一事实源**：`feature_list.json`
* **统一状态源**：`run_state.json`
* **统一调度入口**：`.commands/start-harness.md`
* **按项目类型扩展**：

    * Web：`design_tokens.json` + Playwright
    * Backend：`api_contracts/` + domain model + contract tests

 