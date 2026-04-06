---
name: idea-bank-complete-schema
purpose: 完整的 idea_bank.json 数据结构定义与示例
version: "1.0"
---

# idea_bank.json 完整 Schema (v1.0)

**文件位置**: `.webnovel/idea_bank.json`  
**用途**: 存储项目的创意配置、约束选项、爽点库等全局设定  
**由谁生成**: `/webnovel-init` 阶段 (Phase 6.5)

---

## 完整 JSON Schema

```json
{
  "project": {
    "name": "幻梦边界",
    "genre": "xuanhuan",
    "target_word_count": 3000000,
    "created_date": "2026-01-15",
    "last_updated": "2026-04-06"
  },

  // ===== 三轴混搭配置 =====
  "creativity_constraints": {
    "selected_triad": {
      "theme_axis": {
        "selected": "克苏鲁诡秘+双修体系",
        "description": "将传统修仙与克苏鲁神话融合",
        "examples": ["不可名状的存在", "接触即疯狂", "双修时灵魂交融"],
        "visual_representation": "漆黑的意识空间中浮现眼睛",
        "active": true
      },
      "rule_axis": {
        "selected": "记忆献祭修炼法",
        "description": "每次突破或使用大招需要献祭记忆",
        "mechanics": [
          "突破一个小阶层: -2年寿命or记忆一段经历",
          "使用禁忌功法: -5年寿命or遗忘一个人",
          "境界越高消耗越快: 金丹期突破需要-10年"
        ],
        "consequence": "最终成仙需献祭全部寿命和最重要的记忆",
        "active": true
      },
      "character_axis": {
        "selected": "反派是主角灵魂碎片",
        "description": "最终boss不是敌人，而是主角被迫分裂出的另一个意识",
        "relationship": {
          "phase1_early": "反派行为疯狂，主角看不懂",
          "phase2_mid": "反派言论暗示'保护'的目的",
          "phase3_late": "真相大白：反派是在阻止主角走向自我毁灭"
        },
        "mirror_conflict": {
          "shared_motivation": "都想保护身边的人",
          "opposite_method": "主角→遵守规则、寻求力量；反派→打破规则、控制变量",
          "core_question": "在绝望中，是坚守道德还是不择手段？"
        },
        "active": true
      }
    },
    
    "validation": {
      "non_default_count": 3,
      "meets_requirement": true,
      "comment": "三轴均为非默认选项，创新度高"
    }
  },

  // ===== 反套路库配置 =====
  "anti_trope_library": {
    "selected_anti_tropes": [
      {
        "id": 3,
        "name": "反派智商在线",
        "description": "反派不会降智，每步都有逻辑，多次险些成功",
        "activation_chapter_range": "10-15",
        "activation_method": "反派首次出现时，通过对话or计划細節展现其周密性",
        "narrative_role": "增加反派的可信度和威胁感",
        "status": "pending_activation",
        "evidence_checklist": [
          "反派的长期计划是否合理？",
          "反派是否考虑到所有变数？",
          "反派的失败是否源于外力干扰而非计划漏洞？"
        ]
      },
      {
        "id": 15,
        "name": "主角有严重道德缺陷",
        "description": "主角不是绝对正义，有自私、贪心、软弱等缺点",
        "activation_chapter_range": "1-20",
        "activation_method": "主角为了快速突破，利用善良配角的信任",
        "narrative_role": "为后期的'主角vs反派'增加灰色感",
        "status": "pending_activation",
        "evidence_checklist": [
          "主角是否因私欲做过错误决定？",
          "主角是否对此感到内疚或合理化？",
          "这个缺陷是否与后期反派的'保护欲'形成对比？"
        ]
      },
      {
        "id": 40,
        "name": "多重视角叙事",
        "description": "定期从反派/配角角度讲述同一事件，揭示不同真相",
        "activation_chapter_range": "每 20 章一次",
        "activation_method": "插入反派或配角的独立章节（第 25 章、第 45 章等）",
        "narrative_role": "提升信息密度，增加读者参与感",
        "status": "pending_activation",
        "evidence_checklist": [
          "是否定期有反派的视角出现？",
          "反派视角是否揭露主角不知道的信息？",
          "是否有配角视角或第三方视角？"
        ]
      }
    ],
    
    "available_anti_tropes": [
      {
        "id": 1,
        "name": "金手指反向操作",
        "available": true,
        "reason": "可供后续选择"
      },
      {
        "id": 2,
        "name": "开局即满级",
        "available": false,
        "reason": "与已选择的#15冲突（主角应该弱点，不是满级）"
      }
    ]
  },

  // ===== 爽点库 =====
  "cool_point_system": {
    "enabled_types": [
      {
        "type": "镜像对抗爽",
        "description": "反派与主角的价值观碰撞引发的思想爽感",
        "density_target": "0.5次/万字",
        "ideal_position": ["高潮", "伏笔回收", "对话"],
        "active": true
      },
      {
        "type": "伏笔回收爽",
        "description": "前期埋的线索在后期得到解释",
        "density_target": "1次/1-2万字",
        "ideal_position": ["第20章、第40章等里程碑"],
        "active": true
      },
      {
        "type": "反转爽",
        "description": "读者预期的事件发生反转",
        "density_target": "0.3次/万字",
        "ideal_position": ["章末钩子", "高潮"],
        "active": true
      }
    ],
    
    "disabled_types": [
      {
        "type": "传统越级挑战爽",
        "reason": "与记忆献祭的代价设定冲突（不能无代价升级）"
      },
      {
        "type": "金手指一键解决爽",
        "reason": "与反套路#27（系统任务坑爹）冲突"
      },
      {
        "type": "后宫倒贴爽",
        "reason": "与克苏鲁诡秘气质不符"
      }
    ],
    
    "density_rules": {
      "episode_limit": 3,
      "rotation_threshold": "同类型连续≤2章，第3章必须换类型",
      "total_target_per_10k_words": "1.0-1.5次"
    }
  },

  // ===== Strand Weave 三线配置 =====
  "strand_weave_pattern": {
    "ideal_ratio": {
      "quest": "55-65%",
      "fire": "20-30%",
      "constellation": "10-20%"
    },
    
    "warning_thresholds": {
      "quest_max_consecutive": 5,
      "fire_max_gap": 10,
      "constellation_max_gap": 15
    },
    
    "planned_distribution": [
      {
        "chapter_range": "1-10",
        "quest": 60,
        "fire": 25,
        "constellation": 15,
        "notes": "开局快速铺设主线, 女主初登场"
      },
      {
        "chapter_range": "11-20",
        "quest": 55,
        "fire": 30,
        "constellation": 15,
        "notes": "感情线深化"
      },
      {
        "chapter_range": "21-30",
        "quest": 65,
        "fire": 20,
        "constellation": 15,
        "notes": "秘境冒险阶段，主线推进加速"
      }
    ]
  },

  // ===== 约束激活日历 =====
  "constraint_activation_schedule": {
    "反派智商在线": {
      "phase": 1,
      "trigger_chapter": "10-15",
      "depth": "初露锋芒",
      "method": "首次正式出现和对话"
    },
    "主角道德缺陷": {
      "phase": 1,
      "trigger_chapter": "1-20",
      "depth": "埋设伏笔",
      "method": "主角做出第一个自私的决定"
    },
    "多重视角": {
      "phase": 2,
      "trigger_chapter": "25",
      "depth": "首次启用",
      "method": "第一个'反派视角'章节"
    },
    "赛博修真": {
      "phase": 1,
      "trigger_chapter": "1-5",
      "depth": "概念引入",
      "method": "功法描写体现'程序化'特征"
    },
    "寿命献祭": {
      "phase": 1,
      "trigger_chapter": "10",
      "depth": "首次触发",
      "method": "主角首次献祭记忆"
    },
    "反派是灵魂碎片": {
      "phase": 2,
      "trigger_chapter": "40-50",
      "depth": "伏笔激活，暗示真相",
      "method": "反派言论/行为暗示'关联性'"
    }
  },

  // ===== 禁止元素 (optional) =====
  "forbidden_elements": {
    "tropes": ["滥竽充数的配角", "无脑女主", "莫名其妙的感情线"],
    "words": ["火山", "心湖", "涟漪", "掀起", "某种"],
    "narrative_patterns": ["突兀的时间跳跃", "无因果关系的情节", "过度描写环境无推进"]
  },

  // ===== 参考与灵感 =====
  "references": {
    "benchmark_works": [
      {
        "title": "《我在精神病院学斩神》",
        "author": "三九音域",
        "aspect": "文笔风格、短句节奏、镜像对抗",
        "extraction": "深POV、感官优先、简洁有力"
      },
      {
        "title": "《我不是戏神》",
        "author": "三九音域",
        "aspect": "对话、人物心理、灰色伦理",
        "extraction": "潜台词、角色复杂性"
      }
    ],
    
    "thematic_inspirations": [
      "克苏鲁神话 (恐怖与精神污染)",
      "多重人格心理学 (自我与他者)",
      "双修功法理论 (灵魂与肉体的交融)"
    ]
  },

  // ===== 追踪与状态 =====
  "version": "1.0",
  "last_review": "2026-04-06",
  "enforcement_status": {
    "constraint_inheritance_started": true,
    "constraint_activation_calendar_generated": true,
    "cool_point_whitelist_applied": true,
    "anti_trope_checklist_active": true
  }
}
```

---

## 使用指南

### 初始化时 (webnovel-init Phase 6.5)

1. 创建 `.webnovel/idea_bank.json`
2. 填写：
   - `selected_triad` (三轴混搭)
   - `selected_anti_tropes` (至少 3 条)
   - `enabled_types` (爽点白名单)
   - `disabled_types` (爽点黑名单)

### 大纲规划时 (webnovel-plan)

1. 读取 `idea_bank.json`
2. 生成 `constraint_activation_schedule` (约束激活日历)
3. 将约束分配到各章细纲

### 写作时

1. context-agent 读取 idea_bank.json 生成执行包
2. constraint-inheritance-manager 检查约束继承
3. cool-point-designer 检查爽点白名单

### 周期审计 (每 5-10 章)

1. 对照 `constraint_activation_schedule`，检查实际激活情况
2. 对照 `enabled_types`，检查爽点使用情况
3. 更新 `enforcement_status.last_review`

---

## 范例：《幻梦边界》的 idea_bank.json 实际配置

见项目的 `.webnovel/idea_bank.json` 文件。

