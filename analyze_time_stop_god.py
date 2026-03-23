#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
《时停起手，邪神也得给我跪下！》深度拆书分析报告
"""

import os
import re
from collections import Counter
from datetime import datetime

def analyze_novel():
    ref_dir = 'reference'
    target_file = '时停起手，邪神也得给我跪下！.txt'
    full_path = os.path.join(ref_dir, target_file)

    with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    lines = content.split('\n')
    print(f"文件：{target_file}")
    print(f"总字符：{len(content):,} ({len(content)/10000:.1f} 万字)")
    print(f"总行数：{len(lines):,}")

    # 章节检测
    chapters = re.findall(r'第\d+ 章', content)
    chapter_count = len(set(chapters))
    print(f"章节数：{chapter_count}")

    # 角色提取
    char_names = []
    for line in lines:
        matches = re.findall(r'([a-zA-Z\u4e00-\u9fa5]{2,4})\s*(?:说 | 道|喊 | 问|回答|冷笑|皱眉|点头|看向)', line)
        for m in matches:
            if 2 <= len(m) <= 4:
                char_names.append(m)
    name_counts = Counter(char_names)

    # 关键词
    keywords = {
        '时停': content.count('时停'),
        '邪神': content.count('邪神'),
        '神明': content.count('神明'),
        '序列': content.count('序列'),
        '联邦': content.count('联邦'),
        '收容': content.count('收容'),
        '秦明神': content.count('秦明神'),
        '命运': content.count('命运'),
        '灰烬黎明': content.count('灰烬黎明'),
        '绘命师': content.count('绘命师'),
        '先知': content.count('先知'),
        '杜静哲': content.count('杜静哲'),
        '008': content.count('008'),
        '孕神': content.count('孕神'),
        '弑神': content.count('弑神'),
    }

    report = generate_report(content, lines, chapter_count, name_counts, keywords)
    output_path = 'material/小说分析/时停起手邪神也得给我跪下分析.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n报告已生成：{output_path}")

def generate_report(content, lines, chapter_count, name_counts, keywords):
    report = []

    report.append("# 《时停起手，邪神也得给我跪下！》深度拆书分析报告")
    report.append("")
    report.append(f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"**文件大小**: {len(content):,} 字符 ({len(content)/10000:.1f} 万字)")
    report.append(f"**总行数**: {len(lines):,}")
    report.append(f"**检测章节数**: {chapter_count} 章")
    report.append("")

    # 作品概况
    report.append("---")
    report.append("## 一、作品概况")
    report.append("")
    report.append("| 项目 | 数据 |")
    report.append("|------|------|")
    report.append(f"| 总字数 | {len(content):,} 字 |")
    report.append(f"| 章节数 | {chapter_count} 章 |")
    report.append("| 题材 | 都市异能 + 神明序列 + 收容物 |")
    report.append("| 核心设定 | 时停能力 + 弑神之路 |")
    report.append("")

    # 题材分类
    genre_scores = {
        '神明序列': keywords['神明'] + keywords['序列'] + content.count('神选'),
        '都市异能': keywords['联邦'] + content.count('异能') + content.count('天赋'),
        '收容异常': keywords['收容'] + content.count('008'),
        '命运博弈': keywords['命运'] + keywords['绘命师'] + keywords['先知'],
    }
    report.append("### 题材分类")
    report.append("")
    for genre, score in sorted(genre_scores.items(), key=lambda x: x[1], reverse=True):
        report.append(f"- **{genre}**: {score} 关键词匹配")
    report.append("")

    # 角色分析
    report.append("---")
    report.append("## 二、角色信息分析")
    report.append("")
    report.append("### 2.1 主角档案")
    report.append("")
    report.append("| 属性 | 描述 |")
    report.append("|------|------|")
    report.append("| **姓名** | 秦明神 |")
    report.append("| **性别** | 男 |")
    report.append("| **身份** | 灰烬黎明首领 / 序列拥有者 / 弑神者 |")
    report.append("| **能力** | 时停相关异能 / 序列能力 |")
    report.append("| **性格** | 冷静、淡漠、自信到妖异 |")
    report.append("| **行事风格** | 掌控全局、利用一切、目标明确 |")
    report.append("| **口头禅** | \"我已于凡尘中无敌\" |")
    report.append("| **反差萌** | 妖异外貌下的绝对理性 |")
    report.append("")

    report.append("### 2.2 主要角色（按出场频次）")
    report.append("")
    report.append("| 排名 | 角色名 | 出场次数 | 角色定位 |")
    report.append("|------|--------|----------|----------|")
    top_chars = name_counts.most_common(25)
    for i, (name, count) in enumerate(top_chars, 1):
        role = "主角" if i == 1 else ("主要配角" if i <= 5 else "重要角色" if i <= 10 else "次要角色")
        report.append(f"| {i} | {name} | {count} | {role} |")
    report.append("")

    report.append("### 2.3 重要配角")
    report.append("")
    report.append("| 角色 | 身份 | 能力/特点 | 与主角关系 |")
    report.append("|------|------|----------|------------|")
    report.append("| 绘命师 | 【命运】神选 / 卧底 | 命运相关能力 | 被利用的棋子 |")
    report.append("| 先知 | 卧底 / 双面间谍 | 预知类能力 | 叛徒 |")
    report.append("| 杜静哲 | 联邦高层 / 竞争者 | 念瞳相关 | 宿敌/利用对象 |")
    report.append("| 先驱者 | 联邦阵营 | 未知 | 敌人 |")
    report.append("| 黑皇后 | 被拯救对象 | 未知 | 剧情关键 |")
    report.append("")

    # 力量体系
    report.append("---")
    report.append("## 三、力量体系分析")
    report.append("")
    report.append("### 3.1 核心关键词")
    report.append("")
    report.append("| 关键词 | 频次 | 说明 |")
    report.append("|--------|------|------|")
    for kw, count in sorted(keywords.items(), key=lambda x: x[1], reverse=True):
        report.append(f"| {kw} | {count} | - |")
    report.append("")

    report.append("### 3.2 序列/神明体系")
    report.append("")
    report.append("```")
    report.append("┌─────────────────────────────────────┐")
    report.append("│         神明序列体系                 │")
    report.append("│  ┌─────────────────────────────┐    │")
    report.append("│  │  凡尘 → 神境 → 神明         │    │")
    report.append("│  │  序列拥有者 → 神选 → 真神  │    │")
    report.append("│  └─────────────────────────────┘    │")
    report.append("├─────────────────────────────────────┤")
    report.append("│         核心概念                     │")
    report.append("│  - 孕神：培育成神的过程             │")
    report.append("│  - 弑神：斩杀神明                   │")
    report.append("│  - 神选：被神明选中的人             │")
    report.append("│  - 命运之力：扰乱命运获得的力量     │")
    report.append("└─────────────────────────────────────┘")
    report.append("```")
    report.append("")

    report.append("### 3.3 已知神明/序列")
    report.append("")
    report.append("| 神明/序列 | 说明 |")
    report.append("|-----------|------|")
    report.append("| 【命运】 | 试图降临人间的神明 |")
    report.append("| 008 | 活体收容物，与孕神相关 |")
    report.append("| 念瞳 | 杜静哲追求的能力 |")
    report.append("")

    # 世界观
    report.append("---")
    report.append("## 四、世界观分析")
    report.append("")
    report.append("### 4.1 世界背景")
    report.append("")
    report.append("- **时代背景**: 近未来都市，联邦政府统治")
    report.append("- **核心冲突**: 人类 vs 神明 / 序列拥有者之间的博弈")
    report.append("- **特殊设定**: 收容物存在 / 序列能力者 / 神明可降临")
    report.append("")
    report.append("### 4.2 主要势力")
    report.append("")
    report.append("| 势力 | 类型 | 说明 |")
    report.append("|------|------|------|")
    report.append("| 灰烬黎明 | 地下组织 | 秦明神领导的序列组织 |")
    report.append("| 联邦政府 | 官方政权 | 统治联邦的政府 |")
    report.append("| 联邦 3 区 | 政府辖区 | 联邦划分的行政区 |")
    report.append("| 【命运】阵营 | 神明势力 | 试图降临的神明及其追随者 |")
    report.append("")

    # 剧情主线
    report.append("---")
    report.append("## 五、剧情主线分析")
    report.append("")
    report.append("### 5.1 核心故事线")
    report.append("")
    report.append("```")
    report.append("┌────────────────────────────────────────────┐")
    report.append("│  秦明神建立灰烬黎明组织                    │")
    report.append("│           ↓                                │")
    report.append("│  利用绘命师等人谋划 008 孕神计划              │")
    report.append("│           ↓                                │")
    report.append("│  识破【命运】神选的阴谋                    │")
    report.append("│           ↓                                │")
    report.append("│  决定全面进攻联邦政府抢夺 008                │")
    report.append("│           ↓                                │")
    report.append("│  孕神 → 问鼎神境 → 弑神                   │")
    report.append("└────────────────────────────────────────────┘")
    report.append("```")
    report.append("")

    report.append("### 5.2 剧情钩子")
    report.append("")
    report.append("- **身份暴露**: 绘命师神选身份被揭穿")
    report.append("- **弑神宣言**: 主角妄图弑神的狂傲目标")
    report.append("- **多方博弈**: 秦明神、绘命师、先知、杜静哲的命运推演")
    report.append("- **008 争夺**: 活体收容物的归属决定双神之战")
    report.append("")

    # 文笔技巧
    report.append("---")
    report.append("## 六、文笔编写技巧分析")
    report.append("")
    report.append("### 6.1 叙事风格")
    report.append("")
    avg_len = len(content) / len(lines) if lines else 0
    report.append(f"- **平均句子长度**: {avg_len:.1f} 字")
    report.append("- **叙事视角**: 第三人称")
    report.append("- **语言风格**: 冷峻、简洁、有压迫感")
    report.append("")

    report.append("### 6.2 吸引读者的方法")
    report.append("")
    report.append("1. **强者人设**: 主角开局即无敌，淡漠掌控一切")
    report.append("2. **宏大布局**: 多方势力博弈，命运推演")
    report.append("3. **弑神目标**: 从凡尘到弑神的成长路线")
    report.append("4. **身份反转**: 卧底、神选、叛徒的身份揭露")
    report.append("")

    # 爽点设计
    report.append("---")
    report.append("## 七、爽点设计分析")
    report.append("")
    report.append("| 爽点类型 | 表现 |")
    report.append("|----------|------|")
    report.append("| **碾压爽** | 主角凡尘无敌，掌控全局 |")
    report.append("| **智商爽** | 识破一切阴谋，将计就计 |")
    report.append("| **逼格爽** | 弑神宣言，问鼎神境 |")
    report.append("| **反转爽** | 身份揭露，棋手与棋子 |")
    report.append("")

    # 修炼体系
    report.append("---")
    report.append("## 八、修炼/成神体系")
    report.append("")
    report.append("```")
    report.append("凡尘无敌 → 孕神 → 神境 → 弑神")
    report.append("   ↓          ↓        ↓       ↓")
    report.append("序列觉醒   008 为引  双神之争  斩落神明")
    report.append("```")
    report.append("")

    # 题材分类
    report.append("---")
    report.append("## 九、题材分类")
    report.append("")
    report.append("- **主标签**: 都市异能、神明序列、收容异常")
    report.append("- **副标签**: 幕后布局、智商博弈、弑神之路")
    report.append("- **平台定位**: 男频、爽文、无敌流")
    report.append("")

    # 可借鉴元素
    report.append("---")
    report.append("## 十、可借鉴作品元素")
    report.append("")
    report.append("1. **时停金手指**: 时停能力的独特性")
    report.append("2. **神明序列**: 序列 + 神明的融合设定")
    report.append("3. **收容物体系**: 类似 SCP 的收容物设定")
    report.append("4. **幕后布局**: 主角作为棋手操控全局")
    report.append("5. **弑神目标**: 从凡人到弑神的成长路线")
    report.append("")

    # 全文宗旨
    report.append("---")
    report.append("## 十一、全文宗旨/主题")
    report.append("")
    themes = {
        '无敌': content.count('无敌') + content.count('无敌'),
        '命运': keywords['命运'],
        '神明': keywords['神明'] + keywords['邪神'],
        '掌控': content.count('掌控') + content.count('谋划'),
    }
    report.append("| 主题 | 相关词频次 |")
    report.append("|------|------------|")
    for theme, count in sorted(themes.items(), key=lambda x: x[1], reverse=True):
        report.append(f"| {theme} | {count} |")
    report.append("")

    # 读后感
    report.append("---")
    report.append("## 十二、读后感与分析总结")
    report.append("")
    report.append("### 12.1 作品亮点")
    report.append("")
    report.append("1. **强者主角**: 秦明神开局即无敌，淡漠妖异的人设独特")
    report.append("2. **宏大布局**: 多方势力博弈，命运推演的格局宏大")
    report.append("3. **弑神宣言**: \"我已于凡尘中无敌，待孕神之后，便要问一问诸神\"")
    report.append("4. **身份反转**: 绘命师神选身份暴露的戏剧张力")
    report.append("")

    report.append("### 12.2 可借鉴之处")
    report.append("")
    report.append("1. **无敌流写法**: 主角不憋屈，全程掌控")
    report.append("2. **布局设计**: 多层阴谋，棋手与棋子的转换")
    report.append("3. **台词设计**: 主角台词有逼格，令人记忆深刻")
    report.append("")

    report.append("---")
    report.append("*分析报告生成完成*")

    return '\n'.join(report)

if __name__ == '__main__':
    analyze_novel()
    print("分析完成!")
