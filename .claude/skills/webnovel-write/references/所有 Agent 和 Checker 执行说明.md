# 所有 Agent 和 Checker 执行说明

> 确保在 `/webnovel-write` 编写章节时所有 Agent 和 Checker 都被正确执行

---

## 完整工作流程（6 Steps + 10 Agents/Checkers）

### Step 1: Context Agent

**Agent**: `context-agent`
**文件位置**: `.claude/agents/context-agent.md`
**职责**: 上下文搜集、创作执行包生成

**输出**：
- 任务书（7 板块）
- Contract v2
- Step 2A 直写提示词

**成功标准**：
- ✅ 创作执行包可直接驱动 Step 2A（无需补问）
- ✅ 任务书包含 7 个板块
- ✅ 上章钩子与读者期待明确
- ✅ 角色动机/情绪为推断结果
- ✅ Contract v2 字段完整且与任务书一致

---

### Step 2A: 正文起草

**无 Agent，主流程执行**

**输出**：章节草稿

---

### Step 2B: 风格适配（可选）

**无 Agent，主流程执行**

**输出**：风格化正文

---

### Step 3: 审查（6 个 Checker 并行）

#### 核心审查器（始终执行）

| Checker | 文件位置 | 职责 | 检查内容 |
|---------|---------|------|---------|
| `consistency-checker` | `.claude/agents/consistency-checker.md` | 设定一致性 | 战力/地点/角色/时间线一致性 |
| `continuity-checker` | `.claude/agents/continuity-checker.md` | 连续性 | 伏笔/线索/逻辑洞 |
| `ooc-checker` | `.claude/agents/ooc-checker.md` | 角色 OOC | 性格/说话风格 |

#### 条件审查器（auto 路由触发）

| Checker | 文件位置 | 触发条件 | 检查内容 |
|---------|---------|---------|---------|
| `reader-pull-checker` | `.claude/agents/reader-pull-checker.md` | 非过渡章/有未闭合问题 | 钩子/微兑现/约束分层 |
| `high-point-checker` | `.claude/agents/high-point-checker.md` | 关键章/高潮章/有高光信号 | 爽点数量/类型/密度 |
| `pacing-checker` | `.claude/agents/pacing-checker.md` | 章号>=10/节奏失衡风险 | strand 节奏/疲劳风险 |

**输出**：
- 审查汇总 JSON
- `review_metrics` 落库

**成功标准**：
- ✅ 所有审查器返回遵循 `checker-output-schema.md`
- ✅ `overall_score` 已生成
- ✅ `review_metrics` 成功落库

---

### Step 4: 润色

**内部调用**: `ai-trace-checker`（Anti-AI 检测）

**文件位置**: `.claude/agents/ai-trace-checker.md`

**执行顺序**：
1. 修复 `critical`（必须）
2. 修复 `high`（不能修复则记录 deviation）
3. 处理 `medium/low`（按收益择优）
4. 执行 Anti-AI 与 No-Poison 全文终检

**输出**：
- 润色后正文
- `anti_ai_force_check: pass/fail`

**成功标准**：
- ✅ `critical` 已清零
- ✅ `high` 未修项有 deviation 记录
- ✅ `anti_ai_force_check=pass`

---

### Step 5: Data Agent

**Agent**: `data-agent`
**文件位置**: `.claude/agents/data-agent.md`
**职责**: 数据处理、实体提取、索引构建

**执行流程（10 Steps）**：
- Step A: 加载上下文
- Step B: AI 实体提取
- Step C: 实体消歧
- Step D: 写入存储（state/index）
- Step E: 写入章节摘要
- Step F: AI 场景切片
- Step G: RAG 向量索引
- Step H: 风格样本评估
- Step I: 债务利息（可选）
- Step J: 生成处理报告

**输出**：
- `.webnovel/state.json` 更新
- `.webnovel/index.db` 更新
- `.webnovel/summaries/ch{NNNN}.md`
- `.webnovel/observability/data_agent_timing.jsonl`

**成功标准**：
- ✅ 所有出场实体被正确识别（准确率 > 90%）
- ✅ 状态变化被正确捕获（准确率 > 85%）
- ✅ 消歧结果合理（高置信度 > 80%）
- ✅ 章节摘要文件生成成功
- ✅ `chapter_meta` 写入 state.json

---

### Step 6: Git 备份

**无 Agent，主流程执行**

**输出**：Git commit

---

## 完整 Agent/Checker 清单

### 必须执行的 Agent（2 个）

| 名称 | 步骤 | 文件位置 | 说明 |
|------|------|---------|------|
| `context-agent` | Step 1 | `.claude/agents/context-agent.md` | 上下文搜集、创作执行包生成 |
| `data-agent` | Step 5 | `.claude/agents/data-agent.md` | 数据处理、实体提取、索引构建 |

### 必须执行的 Checker（3-6 个）

| 名称 | 类型 | 步骤 | 文件位置 | 说明 |
|------|------|------|---------|------|
| `consistency-checker` | 核心 | Step 3 | `.claude/agents/consistency-checker.md` | 设定一致性检查 |
| `continuity-checker` | 核心 | Step 3 | `.claude/agents/continuity-checker.md` | 连续性检查 |
| `ooc-checker` | 核心 | Step 3 | `.claude/agents/ooc-checker.md` | 角色 OOC 检查 |
| `reader-pull-checker` | 条件 | Step 3 | `.claude/agents/reader-pull-checker.md` | 追读力检查 |
| `high-point-checker` | 条件 | Step 3 | `.claude/agents/high-point-checker.md` | 爽点检查 |
| `pacing-checker` | 条件 | Step 3 | `.claude/agents/pacing-checker.md` | 节奏检查 |

### 内部调用的 Checker（1 个）

| 名称 | 步骤 | 文件位置 | 说明 |
|------|------|---------|------|
| `ai-trace-checker` | Step 4 | `.claude/agents/ai-trace-checker.md` | AI 味检测（内部调用） |

---

## 执行验证清单

在 `/webnovel-write` 执行完成后，验证以下项目：

### Step 1 验证
- [ ] Context Agent 已执行
- [ ] 创作执行包已生成
- [ ] 执行包包含 3 层（任务书/Contract v2/ 直写提示词）

### Step 3 验证
- [ ] 核心 3 个 Checker 已执行（consistency/continuity/ooc）
- [ ] 条件 Checker 已根据 auto 路由执行
- [ ] 审查汇总 JSON 已生成
- [ ] `review_metrics` 已落库

### Step 4 验证
- [ ] `critical` 问题已修复
- [ ] `high` 问题已修复或记录 deviation
- [ ] `anti_ai_force_check=pass`

### Step 5 验证
- [ ] Data Agent 已执行
- [ ] `state.json` 已更新
- [ ] `index.db` 已更新
- [ ] 章节摘要已生成
- [ ] `chapter_meta` 已写入 state.json
- [ ] 性能日志已写入

### Step 6 验证
- [ ] Git commit 已执行（或记录失败原因）

---

## 常见问题

### Q1: 如何确认所有 Checker 都执行了？

**A**: 查看 Step 3 审查汇总，`selected_checkers` 应包含：
- 核心 3 个：`consistency-checker`、`continuity-checker`、`ooc-checker`
- 条件 3 个（若触发）：`reader-pull-checker`、`high-point-checker`、`pacing-checker`

### Q2: 如何确认 Data Agent 执行了所有 Steps？

**A**: 查看 `.webnovel/observability/data_agent_timing.jsonl`，应包含 10 个步骤的耗时记录。

### Q3: 如何确认 AI 味检测已执行？

**A**: 查看 Step 4 润色报告，应包含 `anti_ai_force_check: pass/fail`。

### Q4: 如何确认 chapter_meta 已写入？

**A**: 查看 `.webnovel/state.json`，应包含：
```json
{
  "chapter_meta": {
    "0100": {
      "hook": { "type": "...", "content": "...", "strength": "..." },
      "pattern": { "opening": "...", "hook": "...", "emotion_rhythm": "..." },
      "ending": { "time": "...", "location": "...", "emotion": "..." }
    }
  }
}
```

---

## 文件结构总览

```
.claude/
├── agents/
│   ├── context-agent.md              # Step 1
│   ├── data-agent.md                 # Step 5
│   ├── consistency-checker.md        # Step 3 核心
│   ├── continuity-checker.md         # Step 3 核心
│   ├── ooc-checker.md                # Step 3 核心
│   ├── reader-pull-checker.md        # Step 3 条件
│   ├── high-point-checker.md         # Step 3 条件
│   ├── pacing-checker.md             # Step 3 条件
│   └── ai-trace-checker.md           # Step 4 内部
├── skills/webnovel-write/
│   ├── SKILL.md                      # 主流程
│   └── references/
│       ├── step-3-review-gate.md     # Step 3 路由规则
│       ├── polish-guide.md           # Step 4 润色规则
│       ├── 写作流程执行清单.md        # 完整执行清单
│       └── 所有 Agent 和 Checker 执行说明.md  # 本文件
└── references/
    └── checker-output-schema.md      # Checker 输出格式
```

---

*最后更新：2026-03-16*
*项目：《御兽：我能掌控诡异神明》*
