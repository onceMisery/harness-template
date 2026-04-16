---
name: harness-minimal-backend-init
description: 初始化最小后端 harness 约束文件，只创建 .harness 和 .agents 下的必要文件。
---

# Harness Minimal Backend Init

## 作用

这个 skill 用于为一个后端项目初始化最小版 harness 约束文件。

初始化目标：
- 创建 `.harness/spec.md`
- 创建 `.harness/feature_list.json`
- 创建 `.harness/sprint.md`
- 创建 `.harness/state.md`
- 创建 `.agents/planner.md`
- 创建 `.agents/generator.md`
- 创建 `.agents/evaluator.md`

这个 skill **只做初始化**，不负责实现业务代码，不创建复杂 schema，不创建额外脚本。

## 适用场景

适用于：
- 想先跑通最小 harness 的后端项目
- 希望先让 code agent 在固定流程下工作
- 暂时不想引入复杂治理和大量约束

不适用于：
- 需要完整多 sprint 编排
- 需要复杂 contract/schema 校验
- 需要前后端一体化流程

## 初始化规则

1. 如果 `.harness/` 不存在，则创建它。
2. 如果 `.agents/` 不存在，则创建它。
3. 如果目标文件不存在，则按模板创建。
4. 如果目标文件已存在，不要覆盖其业务内容；只在用户明确要求重置时才覆盖。
5. 初始化完成后，提醒使用者先填写：
   - `.harness/spec.md`
   - `.harness/feature_list.json`
   - `.harness/sprint.md`
6. `state.md` 初始状态必须是 `planning`。
7. 该 skill 不生成任何 Web 专属文件。

## 创建后的目录

```text
.harness/
  spec.md
  feature_list.json
  sprint.md
  state.md

.agents/
  planner.md
  generator.md
  evaluator.md
```

## 文件内容要求

### `.harness/spec.md`
写清：
- 项目目标
- 本期范围
- 本期不做什么
- 接口要求
- 数据要求
- 错误处理

### `.harness/feature_list.json`
每个功能至少包含：
- `id`
- `name`
- `status`
- `passes`
- `acceptance`

### `.harness/sprint.md`
写清：
- 本轮目标
- 本轮功能
- 允许修改目录
- 暂不处理内容
- 完成标准

### `.harness/state.md`
只保留：
- `state`
- `current_feature`
- `result`
- `notes`

### `.agents/planner.md`
职责：拆需求，不写代码。

### `.agents/generator.md`
职责：实现当前 sprint，不扩需求。

### `.agents/evaluator.md`
职责：检查当前功能是否通过，不改代码。

## 推荐初始化步骤

1. 读取本 skill。
2. 创建 `.harness/` 和 `.agents/`。
3. 根据模板初始化 7 个文件。
4. 输出初始化结果。
5. 提醒用户先填写 spec / feature_list / sprint。

## 初始化完成后建议

初始化完成后，按这个顺序使用：
1. 先写 `.harness/spec.md`
2. 再写 `.harness/feature_list.json`
3. 再写 `.harness/sprint.md`
4. 然后让 generator 开始实现
5. 最后由 evaluator 检查并更新 `passes`
