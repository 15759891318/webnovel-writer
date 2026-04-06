---
name: PYTHON_SCRIPT_FRAMEWORKS
purpose: 三个新 Agent 的可执行 Python 脚本框架与实现指南
version: "1.0"
---

# Python 脚本框架 v1.0

**目的**: 为 constraint-inheritance-manager, execution-package-checker, chapter-audit-checklist 提供可执行的 Python 框架  
**状态**: 80% 框架 + 注释，等待实现细节补充

---

## 项目结构

```
.claude/
├── scripts/  (新目录)
│   ├── constraint_inheritance_manager.py    ⭐ 本文件覆盖
│   ├── execution_package_checker.py         ⭐ 本文件覆盖
│   ├── chapter_audit_checklist.py           ⭐ 本文件覆盖
│   ├── utils/
│   │   ├── config.py          (读取 idea_bank.json, state.json)
│   │   ├── file_handler.py    (读写 Markdown 文件)
│   │   └── validators.py      (检查数据格式)
│   └── __init__.py
```

---

## 脚本 1: constraint_inheritance_manager.py

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
约束继承管理器 (Constraint Inheritance Manager v1.0)

目的: 生成约束激活日历，为细纲标注约束字段，执行周期审计

用法:
    python constraint_inheritance_manager.py --action init
    python constraint_inheritance_manager.py --action annotate --chapter 0100
    python constraint_inheritance_manager.py --action audit --start 1 --end 10
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# ============================================================================
# 数据结构定义
# ============================================================================

@dataclass
class AntiTrope:
    """反套路定义"""
    id: int
    name: str
    setup_start: int
    setup_end: int
    activation_main: int
    deepening_start: int
    deepening_end: int
    
    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class TriadTimeline:
    """三轴时间线"""
    axis_name: str
    early_freq: str
    early_depth: str
    middle_freq: str
    middle_depth: str
    late_freq: str
    late_depth: str

@dataclass
class ActivationCalendar:
    """激活日历容器"""
    total_chapters: int
    anti_tropes: List[AntiTrope]
    triads: Dict[str, TriadTimeline]
    validation_issues: List[str]
    generated_at: str
    
    def to_dict(self) -> dict:
        return {
            'total_chapters': self.total_chapters,
            'anti_tropes': [at.to_dict() for at in self.anti_tropes],
            'triads': {k: asdict(v) for k, v in self.triads.items()},
            'validation_issues': self.validation_issues,
            'generated_at': self.generated_at
        }

# ============================================================================
# 核心算法
# ============================================================================

class ConstraintActivationCalculator:
    """约束激活计算引擎"""
    
    def __init__(self, total_chapters: int):
        self.total_chapters = total_chapters
    
    def calculate_activation_windows(
        self, 
        anti_tropes_count: int
    ) -> List[AntiTrope]:
        """
        计算反套路的激活窗口
        
        原则:
        1. 均匀分布: 总章数 / 反套路数
        2. 间隔分散: 相邻反套路间隔 ≥ 8 章
        3. 区域划分: 设置/激活/深化三个阶段
        
        Args:
            anti_tropes_count: 反套路总数
            
        Returns:
            List[AntiTrope]: 计算结果
        """
        interval = self.total_chapters // anti_tropes_count
        anti_tropes = []
        
        for i in range(anti_tropes_count):
            region_start = i * interval
            region_end = (i + 1) * interval
            
            # 主激活章 = 区间 1/3 处 + 轻微随机化
            offset = interval // 3 + (i % 2) * 5
            main_activation_chapter = region_start + offset
            
            trope = AntiTrope(
                id=i + 1,
                name=f"反套路 #{i + 1}",  # TODO: 从 idea_bank 读取实际名称
                setup_start=region_start,
                setup_end=main_activation_chapter - 5,
                activation_main=main_activation_chapter,
                deepening_start=main_activation_chapter + 3,
                deepening_end=region_end
            )
            anti_tropes.append(trope)
        
        return anti_tropes
    
    def calculate_triad_timeline(self, triad_axes: List[str]) -> Dict[str, TriadTimeline]:
        """
        计算三轴深化时间线
        
        Args:
            triad_axes: 三轴名称列表 (e.g., ["赛博修真", "寿命修炼", "反派未来身"])
            
        Returns:
            Dict[str, TriadTimeline]: 每个轴的深化计划
        """
        timeline = {}
        
        for axis in triad_axes:
            timeline[axis] = TriadTimeline(
                axis_name=axis,
                early_freq="每 5-10 章点触 1 次",
                early_depth="浅度 (基本概念)",
                middle_freq="每 3-5 章点触 1 次",
                middle_depth="中度 (冲突体现)",
                late_freq="每 2-3 章必有",
                late_depth="深度 (世界观挑战)"
            )
        
        return timeline
    
    def validate_calendar(
        self, 
        anti_tropes: List[AntiTrope]
    ) -> List[str]:
        """
        验证生成的日历是否合理
        
        检查项:
        1. 相邻反套路激活时间是否过近
        2. 每条反套路的激活跨度是否足够长
        3. 是否有间隔过大的空档
        
        Args:
            anti_tropes: 反套路列表
            
        Returns:
            List[str]: 问题列表 (空列表 = 无问题)
        """
        issues = []
        
        # 检查 1: 相邻反套路是否过近
        for i in range(len(anti_tropes) - 1):
            current_end = anti_tropes[i].deepening_end
            next_start = anti_tropes[i + 1].setup_start
            
            if next_start - current_end < 5:
                issues.append(
                    f"反套路 #{anti_tropes[i].id} 与 #{anti_tropes[i+1].id} "
                    f"激活间隔过近 ({next_start - current_end} 章)"
                )
        
        # 检查 2: 激活跨度
        for trope in anti_tropes:
            activation_span = trope.activation_main - trope.setup_start
            if activation_span < 3:
                issues.append(
                    f"反套路 #{trope.id} 的激活跨度过短 ({activation_span} 章)"
                )
        
        return issues

# ============================================================================
# Phase 1: 初始化
# ============================================================================

class Phase1Initializer:
    """初始化阶段: 生成约束激活日历"""
    
    def __init__(self, project_root: str, idea_bank_path: str):
        self.project_root = Path(project_root)
        self.idea_bank_path = Path(idea_bank_path)
    
    def load_idea_bank(self) -> Dict:
        """
        读取 idea_bank.json
        
        Returns:
            Dict: 包含 selected_triad, selected_anti_tropes 等
        """
        # TODO: 实现文件读取和 JSON 解析
        with open(self.idea_bank_path, 'r', encoding='utf-8') as f:
            idea_bank = json.load(f)
        return idea_bank
    
    def load_outline_metadata(self) -> Tuple[int, List[str]]:
        """
        读取大纲元数据
        
        Returns:
            Tuple[int, List[str]]: (总章数, 三轴列表)
        """
        # TODO: 实现大纲解析
        # 需要读取 大纲/总纲.md，提取总章数和三轴信息
        raise NotImplementedError("需要解析大纲文件获取总章数")
    
    def generate_calendar(self, total_chapters: int, triad_axes: List[str]) -> ActivationCalendar:
        """
        生成约束激活日历
        """
        calculator = ConstraintActivationCalculator(total_chapters)
        
        # 假设有 5 条反套路
        anti_tropes = calculator.calculate_activation_windows(anti_tropes_count=5)
        triads = calculator.calculate_triad_timeline(triad_axes)
        issues = calculator.validate_calendar(anti_tropes)
        
        calendar = ActivationCalendar(
            total_chapters=total_chapters,
            anti_tropes=anti_tropes,
            triads=triads,
            validation_issues=issues,
            generated_at=datetime.now().isoformat()
        )
        
        return calendar
    
    def save_calendar_to_markdown(self, calendar: ActivationCalendar) -> str:
        """
        将日历转换为 Markdown 格式并保存
        
        Returns:
            str: 保存文件路径
        """
        # TODO: 实现 Markdown 生成
        output_path = self.project_root / '.webnovel' / 'constraint_activation_calendar.md'
        
        markdown_content = f"""# 本书约束激活日历 (自动生成)

生成时间: {calendar.generated_at}
总章数: {calendar.total_chapters}

## 反套路激活时间表

| 反套路编号 | 名称 | 伏笔阶段 | 主激活章 | 深化阶段 |
|--------|------|--------|---------|--------|
"""
        
        for trope in calendar.anti_tropes:
            markdown_content += f"| #{trope.id} | {trope.name} | {trope.setup_start}-{trope.setup_end} | **{trope.activation_main}** | {trope.deepening_start}-{trope.deepening_end} |\n"
        
        markdown_content += f"""

## 三轴深化时间线

[见下表]

## 验证结果

"""
        if calendar.validation_issues:
            for issue in calendar.validation_issues:
                markdown_content += f"- ⚠️ {issue}\n"
        else:
            markdown_content += "- ✅ 无问题\n"
        
        # TODO: 实现文件写入
        print(f"[DEBUG] 日历将保存到: {output_path}")
        
        return str(output_path)


# ============================================================================
# Phase 2: 细纲标注
# ============================================================================

class Phase2Annotator:
    """细纲标注阶段: 为细纲添加约束字段"""
    
    def __init__(self, project_root: str, calendar_path: str):
        self.project_root = Path(project_root)
        self.calendar_path = Path(calendar_path)
    
    def load_calendar(self) -> ActivationCalendar:
        """读取已生成的日历"""
        # TODO: 从 Markdown 重构 ActivationCalendar 对象
        raise NotImplementedError()
    
    def annotate_fine_outline(self, chapter_number: int) -> str:
        """
        为指定章节的细纲添加约束标注
        
        Args:
            chapter_number: 章号 (e.g., 100)
            
        Returns:
            str: 标注内容 (Markdown frontmatter)
        """
        calendar = self.load_calendar()
        
        # TODO: 查询日历，获取本章应激活的反套路
        # TODO: 生成 YAML frontmatter 字段
        
        frontmatter = f"""---
constraints:
  dominant_constraint: "反套路 #N (名称)"
  constraint_strength: "strong|medium|weak"
  constraint_activation_method: "具体激活方式"
  triad_validation:
    theme_axis: "检查点"
    rule_axis: "检查点"
    character_axis: "检查点"
  anti_trope_checklist:
    - "反套路 1 的具体表现要求"
    - "反套路 2 的具体表现要求"
---
"""
        return frontmatter


# ============================================================================
# Phase 3: 周期审计
# ============================================================================

class Phase3Auditor:
    """周期审计阶段: 定期检查约束执行情况"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
    
    def audit_chapter_range(self, start_chapter: int, end_chapter: int) -> Dict:
        """
        审计指定章节范围内的约束执行情况
        
        Args:
            start_chapter: 起始章号
            end_chapter: 结束章号
            
        Returns:
            Dict: 审计报告
        """
        # TODO: 实现审计逻辑
        # 1. 读取范围内所有章节的 frontmatter
        # 2. 读取日历，查询本范围应激活的反套路
        # 3. 对比实际激活与计划激活
        # 4. 生成审计报告
        
        report = {
            'start_chapter': start_chapter,
            'end_chapter': end_chapter,
            'anti_tropes_status': {},
            'triad_balance': {},
            'issues': [],
            'recommendations': []
        }
        
        return report


# ============================================================================
# 命令行接口
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="约束继承管理器")
    parser.add_argument(
        '--action',
        choices=['init', 'annotate', 'audit'],
        required=True,
        help='执行操作: init(生成日历) / annotate(标注细纲) / audit(审计)'
    )
    parser.add_argument(
        '--project-root',
        default='.',
        help='项目根目录'
    )
    parser.add_argument(
        '--chapter',
        type=int,
        help='章号(用于 annotate)'
    )
    parser.add_argument(
        '--start',
        type=int,
        help='起始章号(用于 audit)'
    )
    parser.add_argument(
        '--end',
        type=int,
        help='结束章号(用于 audit)'
    )
    
    args = parser.parse_args()
    
    if args.action == 'init':
        # Phase 1: 生成日历
        initializer = Phase1Initializer(args.project_root, '.webnovel/idea_bank.json')
        total_chapters, triad_axes = initializer.load_outline_metadata()
        calendar = initializer.generate_calendar(total_chapters, triad_axes)
        output_path = initializer.save_calendar_to_markdown(calendar)
        print(f"✅ 约束激活日历已生成: {output_path}")
    
    elif args.action == 'annotate':
        # Phase 2: 标注细纲
        if not args.chapter:
            print("❌ 错误: 需要指定 --chapter")
            return
        annotator = Phase2Annotator(args.project_root, '.webnovel/constraint_activation_calendar.md')
        frontmatter = annotator.annotate_fine_outline(args.chapter)
        print(f"✅ 第 {args.chapter:04d} 章的约束标注:\n{frontmatter}")
    
    elif args.action == 'audit':
        # Phase 3: 周期审计
        if not (args.start and args.end):
            print("❌ 错误: 需要指定 --start 和 --end")
            return
        auditor = Phase3Auditor(args.project_root)
        report = auditor.audit_chapter_range(args.start, args.end)
        print(f"✅ 审计报告:\n{json.dumps(report, indent=2, ensure_ascii=False)}")


if __name__ == '__main__':
    main()
```

---

## 脚本 2: execution_package_checker.py

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
执行包符合度检查器 (Execution Package Checker v1.0)

目的: 检查章节写作对执行包的符合度，识别偏差，提出修改建议

用法:
    python execution_package_checker.py --chapter 0100 --checkpoint 50
    python execution_package_checker.py --chapter 0100 --checkpoint 100
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum

# ============================================================================
# 定义偏差类型
# ============================================================================

class DeviationType(Enum):
    """偏差类型枚举"""
    PLAN_MISSING = "计划缺失"          # 计划了但没执行
    EXECUTION_INSUFFICIENT = "执行不足"  # 执行了但表现太弱
    EXECUTION_DELAYED = "执行延迟"     # 执行了但时机晚
    EXECUTION_EXCESS = "执行超度"      # 比计划更强
    UNPLANNED_EXECUTION = "计划外执行"  # 计划外额外执行

class CriticalityLevel(Enum):
    """紧急度等级"""
    CRITICAL = "关键"  # 必须修改
    HIGH = "高"        # 强烈建议修改
    MEDIUM = "中"      # 建议修改
    LOW = "低"         # 可选修改

# ============================================================================
# 数据结构
# ============================================================================

@dataclass
class ComplianceItem:
    """单项符合度"""
    name: str
    expected: str
    actual: str
    compliance_score: float  # 0-100
    deviation_type: DeviationType
    criticality: CriticalityLevel
    modification_suggestion: str

@dataclass
class ComplianceReport:
    """符合度检查报告"""
    chapter: int
    checkpoint: int
    total_compliance_score: float
    critical_items: List[ComplianceItem]
    items: List[ComplianceItem]
    pass_fail_status: str  # "PASS" or "FAIL"
    recovery_strategy: str
    modification_list: List[Dict]

# ============================================================================
# 检查引擎
# ============================================================================

class ExecutionPackageChecker:
    """执行包符合度检查引擎"""
    
    def __init__(self, chapter: int, checkpoint_percent: int):
        self.chapter = chapter
        self.checkpoint_percent = checkpoint_percent
        self.critical_item_names = [
            "开头触发",
            "核心冲突",
            "主角动机",
            "追读力钩子",
            "主要约束"
        ]
    
    def load_execution_package(self, package_path: str) -> Dict:
        """加载执行包"""
        # TODO: 实现
        raise NotImplementedError()
    
    def load_draft(self, draft_path: str, checkpoint_percent: int) -> str:
        """加载草稿 (按进度百分比截取)"""
        # TODO: 实现
        # 需要根据 checkpoint_percent 计算字数，截取相应部分
        raise NotImplementedError()
    
    def check_opening_trigger(self, execution_package: Dict, draft: str) -> ComplianceItem:
        """
        检查: 开头触发 (钩子类型与执行包一致)
        """
        # TODO: 实现细节对比逻辑
        # 1. 从执行包读取"预期的开头"
        # 2. 从草稿读取前 500 字
        # 3. 对比相似度
        
        compliance_score = 85.0  # TODO: 动态计算
        
        return ComplianceItem(
            name="开头触发",
            expected="枪声响起作为开场，主角开始躲避",
            actual="钟声响起，主角睁开眼睛",
            compliance_score=compliance_score,
            deviation_type=DeviationType.EXECUTION_INSUFFICIENT,
            criticality=CriticalityLevel.HIGH,
            modification_suggestion="改为 '砰——枪声响了' 作为开场"
        )
    
    def check_core_conflict(self, execution_package: Dict, draft: str) -> ComplianceItem:
        """检查: 核心冲突 (大纲规定的冲突完整呈现)"""
        # TODO: 实现
        raise NotImplementedError()
    
    def check_protagonist_motivation(self, execution_package: Dict, draft: str) -> ComplianceItem:
        """检查: 主角动机 (主角"为什么这样做"清晰)"""
        # TODO: 实现
        raise NotImplementedError()
    
    def check_reading_power_hook(self, execution_package: Dict, draft: str) -> ComplianceItem:
        """检查: 追读力钩子 (章末钩子强度达标)"""
        # TODO: 实现
        raise NotImplementedError()
    
    def check_main_constraint(self, execution_package: Dict, draft: str) -> ComplianceItem:
        """检查: 主要约束 (本章约束是否激活)"""
        # TODO: 实现
        raise NotImplementedError()
    
    def generate_report(
        self, 
        execution_package: Dict,
        draft: str
    ) -> ComplianceReport:
        """
        生成符合度报告
        """
        # 检查所有关键项
        items = [
            self.check_opening_trigger(execution_package, draft),
            self.check_core_conflict(execution_package, draft),
            self.check_protagonist_motivation(execution_package, draft),
            self.check_reading_power_hook(execution_package, draft),
            self.check_main_constraint(execution_package, draft),
        ]
        
        # 分离关键项
        critical_items = [item for item in items if item.name in self.critical_item_names]
        
        # 计算总体符合度
        total_score = sum(item.compliance_score for item in items) / len(items)
        
        # 判定 PASS/FAIL
        # 规则: 总分 ≥ 70% 且 <= 1 个关键项失败 = PASS
        failed_critical_items = [item for item in critical_items if item.compliance_score < 70]
        
        if total_score >= 70 and len(failed_critical_items) <= 1:
            pass_fail_status = "PASS"
            recovery_strategy = "可以继续写作"
        else:
            pass_fail_status = "FAIL"
            recovery_strategy = "需要修改"  # TODO: 实现恢复策略选择逻辑
        
        # 生成修改清单
        modification_list = self._generate_modification_list(items)
        
        report = ComplianceReport(
            chapter=self.chapter,
            checkpoint=self.checkpoint_percent,
            total_compliance_score=total_score,
            critical_items=critical_items,
            items=items,
            pass_fail_status=pass_fail_status,
            recovery_strategy=recovery_strategy,
            modification_list=modification_list
        )
        
        return report
    
    def _generate_modification_list(self, items: List[ComplianceItem]) -> List[Dict]:
        """
        生成修改清单 (按优先级排序)
        """
        # TODO: 实现
        modifications = []
        
        for item in items:
            if item.compliance_score < 70:
                modifications.append({
                    'priority': 'P0' if item.criticality == CriticalityLevel.CRITICAL else 'P1',
                    'item': item.name,
                    'suggestion': item.modification_suggestion,
                    'estimated_edit_time_min': 30  # TODO: 动态估计
                })
        
        # 按优先级排序
        modifications.sort(key=lambda x: x['priority'])
        
        return modifications


# ============================================================================
# 命令行接口
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="执行包符合度检查器")
    parser.add_argument('--chapter', type=int, required=True, help='章号')
    parser.add_argument(
        '--checkpoint',
        type=int,
        default=50,
        choices=[30, 50, 70, 100],
        help='检查点(进度百分比)'
    )
    parser.add_argument(
        '--project-root',
        default='.',
        help='项目根目录'
    )
    
    args = parser.parse_args()
    
    # 初始化检查器
    checker = ExecutionPackageChecker(args.chapter, args.checkpoint)
    
    # 加载文件
    package_path = f'.webnovel/chapter_packages/ch{args.chapter:04d}_execution_package.md'
    draft_path = f'正文/第{args.chapter:04d}章.md'
    
    # TODO: 实现文件路径
    execution_package = checker.load_execution_package(package_path)
    draft = checker.load_draft(draft_path, args.checkpoint)
    
    # 生成报告
    report = checker.generate_report(execution_package, draft)
    
    # 输出
    print(f"""
== 执行包符合度检查报告 ==
章节: {report.chapter:04d}
检查点: {report.checkpoint}%
总体符合度: {report.total_compliance_score:.1f}%
判定: {report.pass_fail_status}

修改清单:
""")
    for mod in report.modification_list:
        print(f"  [{mod['priority']}] {mod['item']}: {mod['suggestion']}")


if __name__ == '__main__':
    main()
```

---

## 脚本 3: chapter_audit_checklist.py

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
四维审计清单生成器 (Chapter Audit Checklist v1.0)

目的: 在章节写作完成时，自动生成 4 维度审计清单，判定是否可定稿

用法:
    python chapter_audit_checklist.py --chapter 0100
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass
from enum import Enum

# ============================================================================
# 定义审计维度
# ============================================================================

class AuditDimension(Enum):
    """审计维度"""
    STORY_INTEGRITY = "故事完整性"
    CONSTRAINT_ACTIVATION = "约束激活度"
    WRITING_STYLE = "写作风格"
    READING_POWER = "追读力"

class CheckStatus(Enum):
    """检查状态"""
    PASS = "✅"
    FAIL = "❌"
    WARNING = "⚠️"

# ============================================================================
# 数据结构
# ============================================================================

@dataclass
class ChecklistItem:
    """检查清单项"""
    dimension: AuditDimension
    item_name: str
    is_critical: bool
    expected: str
    actual: str
    status: CheckStatus
    feedback: str

@dataclass
class AuditReport:
    """四维审计报告"""
    chapter: int
    story_integrity_items: List[ChecklistItem]
    constraint_items: List[ChecklistItem]
    style_items: List[ChecklistItem]
    reading_power_items: List[ChecklistItem]
    overall_status: str  # "PASS" or "FAIL"
    critical_failures: List[str]
    recommendations: List[str]

# ============================================================================
# 审计生成器
# ============================================================================

class ChapterAuditGenerator:
    """四维审计清单生成器"""
    
    def __init__(self, chapter: int):
        self.chapter = chapter
    
    def generate_story_integrity_checklist(self, draft: str) -> List[ChecklistItem]:
        """维度 1: 故事完整性"""
        # TODO: 实现
        # 检查: 开头承接、推进点、结尾钩子
        return [
            ChecklistItem(
                dimension=AuditDimension.STORY_INTEGRITY,
                item_name="开头承接",
                is_critical=True,
                expected="承接上章钩子，读者知道发生了什么",
                actual="待检查",
                status=CheckStatus.PASS,
                feedback="开头清晰承接了上章的悬念"
            ),
            # ... 更多项目
        ]
    
    def generate_constraint_activation_checklist(self, draft: str) -> List[ChecklistItem]:
        """维度 2: 约束激活"""
        # TODO: 实现
        # 检查: 反套路激活度、三轴体现、镜像对抗
        return []
    
    def generate_style_checklist(self, draft: str) -> List[ChecklistItem]:
        """维度 3: 写作风格"""
        # TODO: 实现
        # 检查: AI 味、节奏、感官细节
        return []
    
    def generate_reading_power_checklist(self, draft: str) -> List[ChecklistItem]:
        """维度 4: 追读力"""
        # TODO: 实现
        # 检查: 钩子类型、钩子强度、微兑现
        return []
    
    def generate_report(self, draft: str) -> AuditReport:
        """
        生成完整的四维审计报告
        """
        story_items = self.generate_story_integrity_checklist(draft)
        constraint_items = self.generate_constraint_activation_checklist(draft)
        style_items = self.generate_style_checklist(draft)
        reading_power_items = self.generate_reading_power_checklist(draft)
        
        # 统计关键项失败
        all_items = story_items + constraint_items + style_items + reading_power_items
        critical_failures = [
            item.item_name 
            for item in all_items 
            if item.is_critical and item.status == CheckStatus.FAIL
        ]
        
        # 判定总体状态
        overall_status = "FAIL" if critical_failures else "PASS"
        
        # 生成建议
        recommendations = self._generate_recommendations(all_items)
        
        report = AuditReport(
            chapter=self.chapter,
            story_integrity_items=story_items,
            constraint_items=constraint_items,
            style_items=style_items,
            reading_power_items=reading_power_items,
            overall_status=overall_status,
            critical_failures=critical_failures,
            recommendations=recommendations
        )
        
        return report
    
    def _generate_recommendations(self, items: List[ChecklistItem]) -> List[str]:
        """根据检查结果生成建议"""
        # TODO: 实现
        recommendations = []
        
        for item in items:
            if item.status in (CheckStatus.FAIL, CheckStatus.WARNING):
                recommendations.append(f"{item.item_name}: {item.feedback}")
        
        return recommendations


# ============================================================================
# 命令行接口
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="四维审计清单生成器")
    parser.add_argument('--chapter', type=int, required=True, help='章号')
    parser.add_argument(
        '--project-root',
        default='.',
        help='项目根目录'
    )
    
    args = parser.parse_args()
    
    # 初始化生成器
    generator = ChapterAuditGenerator(args.chapter)
    
    # 加载草稿
    draft_path = f'正文/第{args.chapter:04d}章.md'
    # TODO: 实现文件读取
    draft = ""  # draft_content
    
    # 生成报告
    report = generator.generate_report(draft)
    
    # 输出
    print(f"""
== 四维审计清单 (第 {report.chapter:04d} 章) ==

【故事完整性】
{json.dumps([asdict(item) for item in report.story_integrity_items], indent=2, ensure_ascii=False)}

【约束激活度】
{json.dumps([asdict(item) for item in report.constraint_items], indent=2, ensure_ascii=False)}

【写作风格】
{json.dumps([asdict(item) for item in report.style_items], indent=2, ensure_ascii=False)}

【追读力】
{json.dumps([asdict(item) for item in report.reading_power_items], indent=2, ensure_ascii=False)}

== 总体判定 ==
状态: {report.overall_status}
关键项失败: {', '.join(report.critical_failures) if report.critical_failures else '无'}

== 建议 ==
{chr(10).join(report.recommendations)}
""")


if __name__ == '__main__':
    main()
```

---

## 实现指南

### Step 1: 环境准备

```bash
# 创建脚本目录结构
mkdir -p .claude/scripts/utils
mkdir -p .webnovel/chapter_packages

# 创建 utils 模块
touch .claude/scripts/utils/__init__.py
touch .claude/scripts/utils/config.py
touch .claude/scripts/utils/file_handler.py
touch .claude/scripts/utils/validators.py
```

### Step 2: 实现优先级

**优先实现 (P0)**:
1. `constraint_inheritance_manager.py::Phase1Initializer` (生成日历)
2. `execution_package_checker.py::ExecutionPackageChecker.generate_report` (符合度检查)
3. `chapter_audit_checklist.py::ChapterAuditGenerator.generate_report` (审计清单)

**然后实现 (P1)**:
4. Utils 模块 (文件读写、JSON 解析)
5. 各维度的具体检查逻辑

**最后完善 (P2)**:
6. 错误处理和日志
7. 单元测试

### Step 3: 测试

```bash
# 测试约束日历生成
python .claude/scripts/constraint_inheritance_manager.py --action init

# 测试执行包检查
python .claude/scripts/execution_package_checker.py --chapter 0100 --checkpoint 50

# 测试四维审计
python .claude/scripts/chapter_audit_checklist.py --chapter 0100
```

---

## 配置文件示例

```python
# .claude/scripts/utils/config.py

PROJECT_ROOT = "."
IDEA_BANK_PATH = ".webnovel/idea_bank.json"
STATE_PATH = ".webnovel/state.json"
OUTLINE_DIR = "大纲"
DRAFT_DIR = "正文"
PACKAGE_DIR = ".webnovel/chapter_packages"

# 检查器阈值
COMPLIANCE_PASS_THRESHOLD = 0.70  # 70%
CRITICAL_ITEM_FAILURE_LIMIT = 1   # 最多 1 个关键项可以失败

# 审计阈值
AUDIT_CRITICAL_ITEM_THRESHOLD = 0.70

# 运行配置
ENCODING = 'utf-8'
LOG_LEVEL = 'INFO'
```

---

## 总结

三个 Python 脚本框架已准备好，包含:
- ✅ 完整的数据结构定义
- ✅ 核心算法的骨架
- ✅ Phase 的逻辑划分
- ✅ 命令行接口
- ✅ TODO 注释标记需要实现的部分

**下一步**: 选择其中一个脚本，按 TODO 逐步实现功能。推荐从 `constraint_inheritance_manager.py::Phase1Initializer` 开始。

