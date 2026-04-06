---
name: COMPREHENSIVE_WORKFLOW_DIAGRAM
purpose: 完整工作流总图，包含所有 Agent、Skill、数据的调用点和决策分支
version: "1.0"
---

# 完整工作流总图 v1.0

**本图展示**: webnovel-init → webnovel-plan → webnovel-write → webnovel-review 的完整流程，以及所有 Agent 和 Skill 的精确调用点

---

## 总体流程 (Swimlane 图)

```
【项目初始化】
┌─────────────────────────────────────────────────────────────┐
│ webnovel-init                                               │
├─────────────────────────────────────────────────────────────┤
│ Phase 1-6: 项目初始化（现有）                                │
│                                                              │
│ Phase 6.5: 生成创意包                                        │
│   → skill: webnovel-init/phase-6.5-creativity               │
│   → 输出: idea_bank.json (v2.0 格式，含爽点白名单)          │
│                                                              │
│ Phase 7: 完成                                               │
│ ✅ 检查清单:                                                 │
│   - [ ] idea_bank.json 已生成                                │
│   - [ ] 三轴混搭已选定                                       │
│   - [ ] 反套路库已选择（≥3条）                               │
│   - [ ] 爽点白/黑名单已定义                                   │
└──────────────────────────────┬────────────────────────────────┘
                               ↓

【大纲规划】
┌──────────────────────────────────────────────────────────────┐
│ webnovel-plan                                                │
├──────────────────────────────────────────────────────────────┤
│ Phase 1: 大纲框架规划（现有）                                 │
│                                                               │
│ Phase 2-6: 详细大纲规划（现有）                               │
│   - 总纲 → 分卷纲 → 细纲框架                                  │
│                                                               │
│ Phase 2.5(新): 约束加载检查 ⭐ NEW                           │
│   → 读取 idea_bank.json 中的约束配置                         │
│   → 检查三轴混搭和反套路是否合理                             │
│                                                               │
│ Phase 7: 约束激活日历生成 ⭐ NEW                             │
│   → Agent: constraint-inheritance-manager                    │
│   → 输入: idea_bank.json + 总纲/分卷纲                        │
│   → 输出: .webnovel/constraint_activation_calendar.md        │
│   → 内容: 反套路触发表、三轴深化计划、触发章节表              │
│                                                               │
│ Phase 7.5(新): 细纲自动标注 ⭐ NEW                          │
│   → Agent: constraint-inheritance-manager                    │
│   → 遍历所有细纲文件                                          │
│   → 自动添加 Frontmatter YAML:                               │
│     constraints:                                             │
│       dominant_constraint: [从日历读取]                      │
│       constraint_strength: [强/中/弱]                        │
│       constraint_activation_method: [具体方式]                │
│       triad_validation: [三轴检查点]                         │
│       anti_trope_checklist: [反套路清单]                    │
│                                                               │
│ ✅ 检查清单:                                                  │
│   - [ ] constraint_activation_calendar.md 已生成              │
│   - [ ] 所有细纲已标注约束 Frontmatter                       │
│   - [ ] 约束激活日历已评审                                    │
└──────────────────────────────┬────────────────────────────────┘
                               ↓

【章节写作】
┌──────────────────────────────────────────────────────────────┐
│ webnovel-write {chapter}                                      │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│ 【Step 0: 上下文快照】                                        │
│   → Skill: context-manager (v5.x)                            │
│   → 输入: state.json, index.db                               │
│   → 输出: 上下文快照                                          │
│                                                               │
│ 【Step 0.5: 执行包生成】⭐ UPDATED                           │
│   → Agent: context-agent v5.5.1                              │
│   → 输入:                                                    │
│     - 细纲文件 (含约束 Frontmatter)                          │
│     - constraint_activation_calendar.md                      │
│     - state.json, index.db                                   │
│     - 上一章摘要                                              │
│   → 新增读取: 约束激活日历，融合到执行包                      │
│   → 输出: 执行包 (含新增"创意约束执行"板块)                  │
│   → 关键字段:                                                │
│     - constraints_section.dominant                           │
│     - constraints_section.triad_check                        │
│     - constraints_section.activation_method                  │
│                                                               │
│ 【Step 1: 初稿写作前】                                       │
│   → Skill: webnovel-write/step-1-preparation                 │
│   → 读取生成的执行包                                          │
│   → 输出: 开写提示                                            │
│                                                               │
│ 【Step 1A-2C: 初稿写作】                                     │
│   → Skill: webnovel-write/step-2-composition                 │
│   → 参考执行包进行初稿创作                                    │
│   → 产出: 初稿文本 (~50%)                                    │
│                                                               │
│ ⏹️ 【中点检查: 50% 进度】⭐ NEW                              │
│   ┌─────────────────────────────────────┐                    │
│   │ 执行包符合度检查                      │                    │
│   ├─────────────────────────────────────┤                    │
│   │ Agent: execution-package-checker     │                    │
│   │ 输入: 执行包 + 50% 草稿              │                    │
│   │ 输出: 偏差报告 + 修改清单             │                    │
│   │ 得分: 0-100%                        │                    │
│   │                                      │                    │
│   │ 决策分支:                            │                    │
│   │ - ✅ ≥70%: 继续写作                  │                    │
│   │ - ⚠️  50-70%: 继续但标记风险         │                    │
│   │ - ❌ <50%: 立即回修 Phase 2         │                    │
│   │                                      │                    │
│   │ 若回修:                              │                    │
│   │ → 回到 Step 2A 修改初稿              │                    │
│   │ → 修改后可重新运行本检查              │                    │
│   └─────────────────────────────────────┘                    │
│          ↓ (通过, 继续)                                      │
│                                                               │
│ 【Step 2D-4: 后续写作 & 风格优化】                            │
│   → Skill: webnovel-write/step-2B-style-adapter (v5.x)      │
│   → Skill: webnovel-write/step-2C-dialogue-optimizer         │
│   → Skill: webnovel-write/step-4-combat (if needed)          │
│   → 产出: 完整初稿 (~100%)               　                   │
│                                                               │
│ ✅ 检查清单:                                                  │
│   - [ ] 执行包符合度 ≥ 70% (或已标记风险)                    │
│   - [ ] 约束激活是否可识别                                    │
│   - [ ] 钩子强度是否足够                                      │
└──────────────────────────────┬────────────────────────────────┘
                               ↓

【审查与定稿】
┌──────────────────────────────────────────────────────────────┐
│ webnovel-review                                               │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│ 【Phase 1: 自动审计】⭐ NEW                                  │
│   ┌─────────────────────────────────────┐                    │
│   │ 四维审计清单生成                     │                    │
│   ├─────────────────────────────────────┤                    │
│   │ Agent: chapter-audit-checklist       │                    │
│   │ 输入:                               │                    │
│   │  - 执行包                           │                    │
│   │  - 完整正文                         │                    │
│   │  - 细纲 (含约束)                    │                    │
│   │  - 约束激活日历                     │                    │
│   │                                      │                    │
│   │ 输出: 四维审计清单                  │                    │
│   │  1. 故事完整性 (开头/推进/结尾)     │                    │
│   │  2. 约束激活度 (反套路/三轴/镜像)   │                    │
│   │  3. 写作风格 (AI味/节奏/感官)       │                    │
│   │  4. 追读力 (钩子/微兑现)            │                    │
│   │                                      │                    │
│   │ 关键项预警:                         │                    │
│   │  - 开头承接 (必须)                  │                    │
│   │  - 推进点 (必须)                    │                    │
│   │  - 约束激活 (必须)                  │                    │
│   │  - 钩子强度 (必须)                  │                    │
│   │                                      │                    │
│   │ 决策:                               │                    │
│   │ - ✅ PASS: 关键项全部 ✅             │                    │
│   │ - ⚠️  WARNING: 建议项有缺            │                    │
│   │ - ❌ FAIL: 关键项有 ❌               │                    │
│   └─────────────────────────────────────┘                    │
│          ↓                                                    │
│   ┌─────────────────────────────────────┐                    │
│   │ FAIL ❌                             │                    │
│   │ 回修 Phase 2-N                      │                    │
│   │ (修改后重新运行 chapter-audit-checklist)                  │
│   └─────────────────────────────────────┘                    │
│          ↓ (修改后再检查)                                    │
│   ┌─────────────────────────────────────┐                    │
│   │ PASS ✅                             │                    │
│   │ 进入下一步                          │                    │
│   └─────────────────────────────────────┘                    │
│          ↓                                                    │
│                                                               │
│ 【Phase 2-N: 人工审查与修改】                                 │
│   → Skill: webnovel-review/step-2-consistency-check          │
│   → Skill: webnovel-review/step-3-plot-architect             │
│   → Skill: webnovel-review/step-4-ai-trace-removal           │
│   → Skill: webnovel-review/step-5-final-polish               │
│                                                               │
│ 【定稿与数据处理】                                            │
│   → 若 PASS: 进入 Phase Final                                │
│   → 若修改完毕再次 PASS:                                     │
│     - Agent: data-agent (提取实体、更新 state.json)          │
│     - 输出: 章节摘要 + 实体索引 + 状态变化                   │
│                                                               │
│ ✅ 检查清单:                                                  │
│   - [ ] 四维审计清单已生成                                    │
│   - [ ] 关键项是否全部 ✅                                     │
│   - [ ] 约束激活度是否 ≥ 70%                                 │
│   - [ ] 是否需要回修                                          │
└──────────────────────────────┬────────────────────────────────┘
                               ↓

【周期性审计】 (每 5-10 章执行一次)
┌──────────────────────────────────────────────────────────────┐
│ webnovel-review 末期 / 或独立触发                             │
├──────────────────────────────────────────────────────────────┤
│ 【周期审计: 约束执行情况总结】⭐ NEW                         │
│   → Agent: constraint-inheritance-manager                    │
│   → 输入: 前 5-10 章的章节数据 + 约束日历                     │
│   → 输出: 约束执行总结报告                                    │
│                                                               │
│ 报告内容:                                                    │
│   - 约束激活进度 (是否按计划)                                 │
│   - 三轴混搭保持度                                            │
│   - 反套路执行情况                                            │
│   - 镜像对抗深化度                                            │
│   - 风险预警 (是否偏离)                                       │
│   - 后续调整建议                                              │
│                                                               │
│ 决策:                                                        │
│   - ✅ 正常: 继续按计划执行                                   │
│   - ⚠️  偏离: 调整约束激活计划 (后续章节)                     │
│   - ❌ 严重偏离: 考虑修改约束或大纲                           │
│                                                               │
│ ✅ 检查清单:                                                  │
│   - [ ] 约束激活日历执行情况                                  │
│   - [ ] 是否需要调整后续计划                                  │
│   - [ ] 新发现的问题是否需要回溯修复                          │
└──────────────────────────────┬────────────────────────────────┘
                               ↓
                          下一章循环
                          (回到 webnovel-write)
```

---

## 决策树: 各阶段的关键决策点

```
webnovel-plan Phase 7
  ↓
【是否准备就绪？】
  ├─ NO → 回到 Phase 2-6 重新规划
  └─ YES ↓
      生成 constraint_activation_calendar.md
      细纲标注约束 Frontmatter

webnovel-write Step 0.5
  ↓
【执行包质量是否满足？】
  ├─ NO (缺少约束字段等) → 联系 context-agent 维护者
  └─ YES ↓ 开始写作

webnovel-write 50% (中点)
  ↓
【运行 execution-package-checker】
  ├─ 符合度 ≥ 70% ✅ → 继续写作 Step 2D-4
  ├─ 符合度 50-70% ⚠️  → 继续但标记风险 (可选修改)
  └─ 符合度 < 50% ❌ → 立即回修 Step 2A-2C

webnovel-review Phase 1
  ↓
【运行 chapter-audit-checklist】
  ├─ PASS ✅ → 进入 data-agent 处理 (定稿)
  ├─ WARNING ⚠️ → 建议修改，但可接受
  └─ FAIL ❌ → 回到 Phase 2-N 修改

修改后重新运行 chapter-audit-checklist
  ├─ PASS ✅ → 进入 data-agent
  └─ FAIL ❌ → 继续修改或提报问题

【每 5-10 章一次】
webnovel-review 末期
  ↓
【运行 constraint-inheritance-manager 周期审计】
  ├─ 执行情况正常 ✅ → 继续下一轮
  ├─ 有偏离 ⚠️ → 调整后续约束激活计划
  └─ 严重问题 ❌ → 考虑修改约束选择或大纲
```

---

## 关键文件位置参考

```
.claude/
├── agents/
│   ├── context-agent.md (v5.5.1 ⭐ UPDATED)
│   ├── constraint-inheritance-manager.md ⭐ NEW
│   ├── execution-package-checker.md ⭐ NEW
│   └── chapter-audit-checklist.md ⭐ NEW
│
├── skills/
│   ├── webnovel-init/
│   ├── webnovel-plan/
│   ├── webnovel-write/
│   ├── webnovel-review/
│   └── ...
│
├── templates/
│   └── enhanced-fine-outline-template.md ⭐ NEW
│
├── references/
│   ├── creativity-constraints.md
│   ├── idea-bank-complete-schema.md ⭐ NEW
│   ├── constraint-conflict-detection.md ⭐ NEW
│   └── ...
│
├── AGENT_COLLABORATION_MATRIX.md ⭐ NEW
└── COMPREHENSIVE_WORKFLOW_DIAGRAM.md ⭐ NEW (本文件)

.webnovel/
├── idea_bank.json (v2.0 new format)
├── constraint_activation_calendar.md ⭐ AUTO-GENERATED
├── constraint_conflicts_log.md (可选)
├── chapter_packages/
│   ├── ch0001_execution_package.md
│   ├── ch0002_execution_package.md
│   └── ...
└── ...
```

---

## 总结

本总图定义了：
- ✅ 每个 Phase/Step 的确切作用
- ✅ 每个 Agent 的精确调用时机
- ✅ 所有决策分支的逻辑
- ✅ 关键检查点和质量门槛
- ✅ 数据的流向和转换

**使用本图，可以确保整个工作流的每一步都被精确控制，不遗漏任何关键环节。**

