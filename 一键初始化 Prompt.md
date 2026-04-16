你现在负责为当前仓库初始化一个 minimal 后端 harness。

目标：
在当前项目根目录创建最小可用的 harness 约束文件，只用于后端开发，不引入复杂治理，不创建多余文件，不实现业务代码。

请严格完成以下任务：

1. 创建目录：

- .harness/
- .agents/

2. 创建以下文件，并写入合理的初始化模板内容：

- .harness/spec.md
- .harness/feature_list.json
- .harness/sprint.md
- .harness/state.md
- .agents/planner.md
- .agents/generator.md
- .agents/evaluator.md

3. 文件要求如下：

A. .harness/spec.md

- 这是项目需求总说明模板
- 使用中文
- 包含以下章节：
    - 项目目标
    - 本期范围
    - 本期不做
    - 接口要求
    - 数据要求
    - 错误处理
- 内容写成可填写模板，不要编造业务细节
- 使用明显占位符，如“待补充”

B. .harness/feature_list.json

- 初始化为 JSON 数组
- 先放 2 个示例 feature，字段只保留：
    - id
    - name
    - status
    - passes
    - acceptance
- status 初始值为 "todo"
- passes 初始值为 false
- acceptance 为字符串数组
- 示例内容必须是后端场景，例如“创建实体”“查询详情”
- 保持格式正确、可直接编辑

C. .harness/sprint.md

- 这是“当前迭代”模板
- 使用中文
- 包含以下章节：
    - 目标
    - 本轮功能
    - 允许修改
    - 暂不处理
    - 完成标准
- 默认本轮功能只放 feature_list.json 里的第一个功能
- 不要写复杂规则

D. .harness/state.md

- 这是当前状态文件
- 使用最简结构：
    - state
    - current_feature
    - result
    - notes
- 初始值设置为：
    - state: planning
    - current_feature: F1
    - result: pending
    - notes: 初始化完成，待补充需求

E. .agents/planner.md

- 使用中文
- 只写最小约束
- 说明 planner 的职责：
    - 读取 .harness/spec.md
    - 更新 .harness/feature_list.json
    - 更新 .harness/sprint.md
    - 更新 .harness/state.md
- 说明 planner 不写业务代码
- 说明 planner 不增加 spec 之外的新功能

F. .agents/generator.md

- 使用中文
- 只写最小约束
- 说明 generator 的职责：
    - 根据 .harness/sprint.md 实现当前功能
    - 修改 apps/backend/src 和 apps/backend/tests
    - 完成后更新 feature_list.json 和 state.md
- 说明 generator 不扩需求
- 说明 generator 不修改无关模块

G. .agents/evaluator.md

- 使用中文
- 只写最小约束
- 说明 evaluator 的职责：
    - 检查当前功能是否满足 acceptance
    - 检查是否有基础测试
    - 给出通过或退回结论
    - 更新 feature_list.json 和 state.md
- 说明 evaluator 只检查，不改代码

4. 额外约束：

- 不要创建 README
- 不要创建 scripts
- 不要创建 commands
- 不要创建 skills
- 不要创建任何 web 相关文件
- 不要实现业务代码
- 不要添加 schema、ADR、risk、report 等复杂文件
- 所有文件内容必须尽量简洁，可直接手工修改

5. 输出要求：

- 完成后列出创建的文件路径
- 每个文件用一句话说明用途
- 不要输出多余分析