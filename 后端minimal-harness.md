# 一、后端 minimal 版目录

```text id="0kl9x"
repo-root/
├── .harness/
│   ├── spec.md
│   ├── feature_list.json
│   ├── sprint.md
│   └── state.md
│
├── .agents/
│   ├── planner.md
│   ├── generator.md
│   └── evaluator.md
│
├── apps/backend/
│   ├── src/
│   └── tests/
│
└── README.md
```

---

# 二、每个文件夹是干什么的

## `.harness/`

这是最核心的目录。
只保留 4 个文件，够用就行。

### `spec.md`

写需求说明。
回答“这个后端要做什么”。

### `feature_list.json`

写功能清单。
回答“具体有哪些功能点要做”。

### `sprint.md`

写当前迭代任务。
回答“这一轮只做哪些东西”。

### `state.md`

写当前状态。
回答“现在跑到哪一步了，是规划中、开发中还是待修复”。

---

## `.agents/`

放 3 个角色的最小约束。

### `planner.md`

负责拆需求，不写代码。

### `generator.md`

负责实现，不扩需求。

### `evaluator.md`

负责检查，不改代码。

---

## `apps/backend/`

真实后端代码目录。

### `src/`

放业务代码。

### `tests/`

放测试代码。

---

# 三、4 个核心文件怎么写

---

## 1. `.harness/spec.md`

这是总需求说明，尽量短，但要清楚。

模板：

```md id="1py6x"
# 项目说明

## 目标
实现一个订单服务，支持创建订单、查询订单详情。

## 范围
本期只做：
- 创建订单
- 查询订单详情

本期不做：
- 支付
- 退款
- 库存扣减

## 接口要求
- POST /orders 创建订单
- GET /orders/{id} 查询订单

## 数据要求
- 订单必须保存到数据库
- 订单金额必须大于 0

## 错误处理
- 参数错误返回 400
- 订单不存在返回 404
```

怎么写：

* 用最少的话写清目标
* 明确“做什么”和“不做什么”
* 把接口和异常先定下来

---

## 2. `.harness/feature_list.json`

这是唯一功能清单。
minimal 版只保留最必要字段。

模板：

```json id="0x9np"
[
  {
    "id": "F1",
    "name": "创建订单",
    "status": "todo",
    "passes": false,
    "acceptance": [
      "接口可调用",
      "参数校验生效",
      "数据成功入库",
      "返回订单ID"
    ]
  },
  {
    "id": "F2",
    "name": "查询订单详情",
    "status": "todo",
    "passes": false,
    "acceptance": [
      "可按订单ID查询",
      "订单不存在返回404"
    ]
  }
]
```

怎么写：

* `id`：简短就行，比如 F1、F2
* `name`：功能名
* `status`：`todo` / `doing` / `done`
* `passes`：是否通过验收
* `acceptance`：验收标准，尽量写成能检查的话

不要一上来加很多字段。
先保证 agent 看得懂、你也维护得动。

---

## 3. `.harness/sprint.md`

这个文件只描述“当前这一轮做什么”。

模板：

```md id="8meqg"
# 当前迭代

## 目标
完成创建订单主链路

## 本轮功能
- F1 创建订单

## 允许修改
- apps/backend/src/**
- apps/backend/tests/**

## 暂不处理
- F2 查询订单详情
- 支付相关能力

## 完成标准
- F1 对应接口可运行
- 至少有基础测试
- feature_list.json 中 F1 可更新为 done / passes=true
```

怎么写：

* 一轮只放 1~2 个功能
* 不要贪多
* 写清这轮允许动哪里
* 写清“本轮不做什么”

---

## 4. `.harness/state.md`

这个文件就是纯文本状态，不需要 JSON。

模板：

```md id="gl7tc"
# 当前状态

state: planning
current_feature: F1
result: pending
notes:
- 正在拆解需求
```

常用状态建议只保留 5 个：

```text id="mvmup"
planning
generating
evaluating
rework
done
```

例如：

### 开发中

```md id="4j9e3"
# 当前状态

state: generating
current_feature: F1
result: pending
notes:
- 正在实现 POST /orders
```

### 待修复

```md id="zb2ew"
# 当前状态

state: rework
current_feature: F1
result: failed
notes:
- 参数校验缺失
- 测试未覆盖异常分支
```

---

# 四、3 个最小 agent 文件怎么写

---

## 1. `.agents/planner.md`

```md id="zu6mt"
你是 planner。

职责：
- 读取 .harness/spec.md
- 更新 .harness/feature_list.json
- 更新 .harness/sprint.md
- 更新 .harness/state.md

规则：
- 只做需求拆解
- 不写业务代码
- 不增加 spec 之外的新功能

完成标志：
- state.md 更新为 planning 完成
```

---

## 2. `.agents/generator.md`

```md id="ja4e5"
你是 generator。

职责：
- 根据 .harness/sprint.md 实现当前功能
- 修改 apps/backend/src 和 apps/backend/tests
- 完成后更新 feature_list.json 和 state.md

规则：
- 只做当前 sprint 中的功能
- 不扩需求
- 不修改无关模块

完成标志：
- 当前功能 status 改为 done
- state.md 更新为 evaluating
```

---

## 3. `.agents/evaluator.md`

```md id="eb1xj"
你是 evaluator。

职责：
- 检查当前功能是否满足 acceptance
- 检查是否有基础测试
- 给出通过或退回结论
- 更新 feature_list.json 和 state.md

规则：
- 只检查，不改代码
- 有明显问题就退回
- 通过后把 passes 改为 true

完成标志：
- 通过：state.md = done
- 不通过：state.md = rework
```

---

# 全局流程
 全局说明应尽可能短

```md id="8zyiv"
# Backend Minimal Harness

## 目标
这是一个最小版后端 harness，用来让 code agent 按固定流程开发，不追求复杂治理。

## 目录说明

### .harness/
保存需求、功能、当前 sprint、当前状态。

### .agents/
保存 planner / generator / evaluator 三个角色的最小约束。

### apps/backend/src/
业务代码目录。

### apps/backend/tests/
测试代码目录。

## 运行流程

1. 先写 `.harness/spec.md`
2. planner 拆成 `feature_list.json`
3. planner 确定本轮 `sprint.md`
4. generator 实现代码
5. evaluator 检查是否通过
6. 不通过就回到 generator 修复

## 最小规则

- spec 是需求来源
- feature_list 是功能清单
- sprint 只定义本轮任务
- state 记录当前进度
- evaluator 不通过，不进入下一轮
```

---

# 六、最小使用步骤

你只需要按这个顺序来：

## 第 1 步

先写 `.harness/spec.md`

## 第 2 步

根据 spec 写 `.harness/feature_list.json`

## 第 3 步

写 `.harness/sprint.md`
先只放一个功能，比如 F1

## 第 4 步

把 `.harness/state.md` 改成：

```md id="fo725"
state: generating
current_feature: F1
result: pending
notes:
- start
```

## 第 5 步

让 generator 开始写 `apps/backend/src/` 和 `apps/backend/tests/`

## 第 6 步

让 evaluator 检查 acceptance 是否通过
通过就把：

* `feature_list.json` 里的 `passes` 改成 `true`
* `state.md` 改成 `done`

---

# 七、这个 minimal 版删掉了什么

为了简单，我故意删掉了这些：

* schema 校验
* decisions.md
* risks.md
* evaluator_report 复杂结构
* api_contracts 目录
* domain_model 强约束
* command 编排模板
* 多 sprint 复杂状态机
* hooks / scripts

这些以后都可以再加。
现在先确保：**你能真的用起来。**

---

# 八、什么时候该从 minimal 升级

当你出现下面情况，再升级就行：

### 1. 功能变多了

`feature_list.json` 管不住了
→ 加 `sprint_plan.json`

### 2. 接口变复杂了

前后端开始联调
→ 加 `api_contracts/`

### 3. 业务规则复杂了

状态、实体、约束很多
→ 加 `domain_model.md`

### 4. 团队协作变多了

大家对“做到哪了”理解不一致
→ 把 `state.md` 升级成 `run_state.json`

---

# 九、我给你的直接建议

如果你现在觉得约束太多，那就只保留这 4 个文件：

```text id="0r4aj"
.harness/spec.md
.harness/feature_list.json
.harness/sprint.md
.harness/state.md
```

再配 3 个 agent 文件：

```text id="9ktq1"
.agents/planner.md
.agents/generator.md
.agents/evaluator.md
```
