---
name: AGENT_COLLABORATION_MATRIX
purpose: 定义新增三个 Agent 与现有系统的协作规范、调用顺序、数据流
version: "1.0"
---

# Agent 协作矩阵 v1.0

**目的**: 明确 constraint-inheritance-manager、execution-package-checker、chapter-audit-checklist 与现有系统的集成点  
**适用**: webnovel-init / webnovel-plan / webnovel-write / webnovel-review 的完整流程

---

## 一、标准工作流总图

```
┌──────────────────────────────────────────────────────────────┐
│                   webnovel-init                               │
│  (Phase 6.5: 生成 idea_bank.json)                             │
└──────────────────────────┬───────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────────┐
│              webnovel-plan                                    │
│  (Phase 2: 加载创意约束)                                      │
│  (Phase 7: 大纲规划完成)                                      │
│                                                               │
│  → constraint-inheritance-manager ⭐ NEW                      │
│     (生成: constraint_activation_calendar.md)                 │
│                                                               │
│  → 细纲自动标注约束字段 (Frontmatter YAML)                    │
└──────────────────────────┬───────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────────┐
│              webnovel-write                                   │
│  (Step 0: 快照 & 执行包生成)                                 │
│                                                               │
│  → context-agent v5.5.1 ⭐ UPDATED                            │
│     (新增: 读取 constraint_activation_calendar)              │
│     (新增: 约束激活项到执行包)                                │
│     (输出: 执行包 + 约束激活建议)                             │
│                                                               │
│  (Step 1-3: 初稿写作)                                         │
│                                                               │
│  50% 进度检查点 ⭐ NEW                                        │
│  → execution-package-checker ⭐ NEW                           │
│     (对比执行包 vs 正文 50%)                                  │
│     (输出: 偏差报告 + 修改清单)                               │
│     (决策: 继续 or 回修)                                      │
│                                                               │
│  (Step 3-4: 继续写作)                                         │
└──────────────────────────┬───────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────────┐
│              webnovel-review                                  │
│  (Phase 1: 定稿前审查)                                        │
│                                                               │
│  → chapter-audit-checklist ⭐ NEW                             │
│     (自动生成四维清单)                                        │
│     (决策: PASS or FAIL)                                      │
│     (如果FAIL → 回修)                                         │
│                                                               │
│  (Phase N: 章节审核完成)                                      │
│                                                               │
│  周期性审计 (每 5 章) ⭐ NEW                                  │
│  → constraint-inheritance-manager                            │
│     (周期审计: 约束执行总结)                                  │
│     (输出: 约束执行审计报告)                                  │
└──────────────────────────┬───────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────────┐
│              定稿 & 发布                                      │
└──────────────────────────────────────────────────────────────┘
```

---

## 二、Agent 调用规范详解

### 📋 constraint-inheritance-manager

**调用时机**:
| 阶段 | 时机 | 用途 |
|-----|------|------|
| 初始化 | webnovel-plan Phase 7 后 | 生成约束激活日历 |
| 规划 | 每章细纲前 | 获取本章应激活的约束 |
| 审计 | 每 5-10 章 | 周期审计执行情况 |

**输入依赖**:
```
idea_bank.json (约束配置)
  ↓
大纲/ (总纲、分卷纲、细纲)
  ↓
constraint_activation_calendar.md (已生成或待生成)
```

**输出内容**:
```
1. constraint_activation_calendar.md (首次生成后可更新)
2. 细纲 Frontmatter YAML (约束标注)
3. 周期审计报告 (每 5 章)
```

**与其他工具的关系**:
```
constraint-inheritance-manager
  ↓ (输出: constraint_activation_calendar.md)
context-agent v5.5.1
  ↓ (读取和融合)
execution-package-checker
  ↓ (检查约束是否被激活)
chapter-audit-checklist
  ↓ (在四维清单中检查约束项)
最终定稿
```

---

### 📋 context-agent v5.5.1 (更新版)

**更新内容** (相比 v5.5):

```markdown
## 新增：约束激活输入 (Phase 0.5)

在读取大纲前，先读取并加载：
- constraint_activation_calendar.md
- 细纲的 Frontmatter YAML (约束字段)

## 新增：执行包字段

在输出的"任务书"中新增第 8 板块：

### 8. 创意约束执行（新增）
**主导约束**: [从细纲的 constraint_dominant 字段读取]
**约束强度**: 强 / 中 / 弱
**激活方式**: [从细纲的 constraint_activation_method 读取]

**三轴混搭检查**:
- 题材轴: [具体要求]
- 规则轴: [具体要求]
- 角色轴: [具体要求]

**反套路清单**: [本章涉及的反套路]

**镜像对抗深化**: [如果涉及]
```

**关键改动**:
```python
# 伪代码示例

class ContextAgent:
    def generate_execution_package(self, chapter):
        # Phase 0.5: 读取约束日历
        calendar = load_constraint_activation_calendar()
        constraints_for_this_chapter = calendar.get(chapter)
        
        # Phase 1-6: 现有逻辑
        outline = load_outline(chapter)
        state = load_state()
        ...
        
        # 新增: 融合约束到执行包
        execution_package['constraints_section'] = {
            'dominant': constraints_for_this_chapter['dominant'],
            'activation_method': outline['constraint_activation_method'],
            ...
        }
        
        return execution_package
```

**与其他工具的关系**:
```
idea_bank.json + constraint_activation_calendar.md
  ↓ (context-agent 读取)
执行包 (含约束激活部分)
  ↓ (execution-package-checker 验证)
修改建议 (若偏差)
```

---

### 📋 execution-package-checker

**调用时机**:
| 时机 | 触发 | 决策 |
|-----|------|------|
| 写作 50% | 自动 or 手动 | 符合度 < 70% → 修改 |
| 关键章节 | 手动触发 | 可多次调用 |

**输入依赖**:
```
执行包 (来自 context-agent)
  ↓
正文草稿 (当前已写部分)
  ↓
细纲 (参考)
```

**输出内容**:
```
1. 执行包追踪表 (逐项 0-100%)
2. 偏差分类报告
3. 修改清单 (P0/P1/P2)
4. 符合度总分 (0-100%)
```

**关键决策**:
```
符合度评分 ≥ 70%  → ✅ PASS, 继续写作
符合度评分 50-70% → ⚠️ WARNING, 建议修改本地，或继续但标记风险
符合度评分 < 50%  → ❌ FAIL, 必须回修，修改后重新检查
```

**与其他工具的关系**:
```
execution-package-checker 
  ↓ (输出: 修改清单)
webnovel-write (回修 Phase 2-3)
  ↓/或\ 继续写作
execution-package-checker (可再次检查)
  ↓
chapter-audit-checklist (定稿前另一层检查)
```

---

### 📋 chapter-audit-checklist

**调用时机**:
| 时机 | 触发 | 输出 |
|-----|------|------|
| 写作完成 (100%) | 自动 or 手动 | 四维审计清单 |
| 定稿前 | 必须 | PASS/FAIL 判定 |
| 修改后 | 可重新调用 | 更新清单 |

**输入依赖**:
```
执行包
  ↓
完整正文
  ↓
细纲
  ↓
约束激活日历
```

**输出内容**:
```
1. 四维审计清单 (可视化勾选表)
2. 关键项预警 (若失败)
3. 优先级修改清单
4. 通过/失败判定
```

**关键决策**:
```
关键项全部 ✅  → PASS, 可定稿
关键项有 ❌   → FAIL, 必须修改
建议项有缺    → WARNING, 建议修改但可接受
```

**与其他工具的关系**:
```
chapter-audit-checklist
  ↓ PASS
data-agent (提取实体、更新 state.json)
  ↓
下章 context-agent 读取数据
  ↓
循环到下一章

  或

chapter-audit-checklist
  ↓ FAIL
webnovel-review Phase 2-N (修改)
  ↓
chapter-audit-checklist (重新检查)
```

---

## 三、数据流向图

```
【数据层】
idea_bank.json
  ├─ selected_triad
  ├─ selected_anti_tropes
  └─ enabled_types / disabled_types
         ↓
constraint-inheritance-manager ←────┐
  ├─ 生成 constraint_activation_calendar.md
  ├─ 标注细纲 Frontmatter
  └─ 周期审计
         ↓
细纲 (带约束标注的 YAML Frontmatter)
         ↓
context-agent v5.5.1
  ├─ 读取: constraint_activation_calendar.md, 细纲约束字段
  └─ 输出: 执行包 (含约束激活部分)
         ↓
【执行层】
执行包 + 正文草稿 (50%)
         ↓
execution-package-checker
  ├─ 对比与检查
  └─ 输出: 修改清单
         ↓
【修改决策】
修改 (if 符合度 < 70%)
  ↓
或
继续写作 (if 符合度 ≥ 70%)
  ↓
完整正文 (100%)
         ↓
执行包 + 完整正文 + 细纲 + 约束日历
         ↓
chapter-audit-checklist
  ├─ 四维审计
  └─ 输出: 清单 + PASS/FAIL
         ↓
【质检决策】
PASS → data-agent (提取、更新)
                ↓
        下章流程重复
        
FAIL → webnovel-review (修改)
                ↓
        重新 chapter-audit-checklist
                ↓
        PASS → data-agent
```

---

## 四、Agent 间的优先级和冲突解决

### 优先级顺序

**若发生冲突，按以下优先级解决**:

1. **constraint-inheritance-manager** (最高)
   - 约束是核心创意，不能妥协
   - 若约束与大纲冲突 → 参考 constraint-conflict-detection.md

2. **context-agent** (中高)
   - 执行包定义了本章的目标
   - 若执行包与正文冲突 → execution-package-checker 调解

3. **execution-package-checker** (中)
   - 检查符合度，提出修改建议
   - 不是绝对阻挦，但 50% 时发现问题应重视

4. **chapter-audit-checklist** (中低)
   - 最后一道关卡，但不改变内容
   - FAIL 时需修改，PASS 时不干涉

### 冲突处理示例

**场景**: 约束要求"反派智商在线"，但 context-agent 因大纲限制无法在执行包中体现

**处理流程**:
```
1. constraint-inheritance-manager 检测到冲突
2. 在约束激活日历中标记为 ⚠️ 风险
3. context-agent 在执行包中标注 "约束激活困难"
4. 人工审查: 修改大纲 or 调整约束表现方式
5. 若修改大纲 → 重新生成执行包
6. 若调整表现 → 在执行包中补充特殊说明
```

---

## 五、实施检查清单

### webnovel-plan 末期 (Phase 7)

- [ ] idea_bank.json 已确认
- [ ] constraint-inheritance-manager 已运行，生成 constraint_activation_calendar.md
- [ ] 所有细纲已自动标注约束 Frontmatter
- [ ] 约束激活日历已评审（是否合理）

### webnovel-write 开始 (Step 0)

- [ ] context-agent v5.5.1 已更新
- [ ] 执行包是否包含了"创意约束执行"部分？
- [ ] 执行包质量是否满足要求？

### webnovel-write 50% (中点检查)

- [ ] 触发 execution-package-checker
- [ ] 符合度是否 ≥ 70%？
- [ ] 若 < 50%，是否需要回修？

### webnovel-review 定稿前

- [ ] 触发 chapter-audit-checklist
- [ ] 四维清单是否全部通过？
- [ ] 关键项是否有 ❌？

### 每 5-10 章

- [ ] 触发 constraint-inheritance-manager 周期审计
- [ ] 约束执行情况总结是否符合预期？
- [ ] 是否需要调整后续的约束激活计划？

---

## 六、常见问题 (FAQ)

### Q: 三个新 Agent 是否必须全部使用？

**A**: 
- constraint-inheritance-manager: **必须** (对应问题"剧情普通")
- execution-package-checker: **强烈建议** (对应问题"执行不力")
- chapter-audit-checklist: **必须** (最后质检)

### Q: context-agent v5.5 需要大改吗？

**A**: 不需要大改。只需添加：
1. Phase 0.5: 读取约束日历
2. Phase 3-7 中融合约束信息到执行包
3. 输出新增"约束激活"板块

### Q: 若 execution-package-checker 在 50% 发现严重问题，应该怎么办？

**A**: 
- 符合度 < 50% → 建议**立即回修**，不要继续写
- 符合度 50-70% → **可继续但标记风险**，等定稿时一起修
- 符合度 ≥ 70% → 放心继续

### Q: 若 chapter-audit-checklist FAIL，是否意味着整章废了？

**A**: 不一定。FAIL 分两种：
- **关键项 FAIL**: 必须重改 (如开头未接住上章钩子)
- **建议项 FAIL**: 可修改也可接受 (如爽点密度稍低)

---

## 七、新增 Agent 版本号说明

- **constraint-inheritance-manager**: v1.0 (首次发布)
- **execution-package-checker**: v1.0 (首次发布)
- **chapter-audit-checklist**: v1.0 (首次发布)
- **context-agent**: v5.5 → **v5.5.1** (小幅更新: 新增约束激活输出)

---

## 总结

本矩阵定义了三个新 Agent 与现有系统的完整协作框架，确保：
- ✅ 调用顺序清晰
- ✅ 数据流向明确
- ✅ 冲突解决有规则
- ✅ 关键决策有标准

**使用本矩阵，可以确保整个系统的"约束执行链路"贯穿始终。**

