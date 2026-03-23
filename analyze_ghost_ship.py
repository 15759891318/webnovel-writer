#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
《全民大航海：我有一条幽灵船》深度拆书分析报告
"""

import os
import re
import json
from collections import Counter, defaultdict
from datetime import datetime

def analyze_novel():
    # 找到小说文件
    ref_dir = 'reference'
    target_file = None
    for filename in os.listdir(ref_dir):
        if '幽灵' in filename:
            target_file = filename
            break

    if not target_file:
        print("未找到幽灵船小说文件")
        return

    full_path = os.path.join(ref_dir, target_file)

    # 读取完整内容
    with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    lines = content.split('\n')
    print(f"文件：{target_file}")
    print(f"总字符数：{len(content):,} ({len(content)/10000:.1f} 万字)")
    print(f"总行数：{len(lines):,}")

    # ========== 1. 章节结构分析 ==========
    chapter_pattern = r'第 [一二三四五六七八九十百千 0-9]+章'
    chapters = []
    for i, line in enumerate(lines):
        match = re.search(chapter_pattern, line)
        if match:
            chapters.append((i, line.strip()))

    print(f"检测到章节数：{len(chapters)}")

    # ========== 2. 角色分析 ==========
    char_names = []
    for line in lines:
        matches = re.findall(r'([a-zA-Z\u4e00-\u9fa5]{2,4})\s*(?:说 | 道|喊 | 问|回答|冷笑|沉思|皱眉|点头|摇头|转身 | 看向)', line)
        for m in matches:
            if 2 <= len(m) <= 4:
                char_names.append(m)

    name_counts = Counter(char_names)

    # ========== 3. 关键词统计 ==========
    keywords = {
        '幽灵船': content.count('幽灵船'),
        '航海': content.count('航海'),
        '海域': content.count('海域'),
        '岛屿': content.count('岛屿'),
        '船长': content.count('船长'),
        '船员': content.count('船员'),
        '系统': content.count('系统'),
        '能力': content.count('能力'),
        '升级': content.count('升级'),
        '任务': content.count('任务'),
        '奖励': content.count('奖励'),
        '生存': content.count('生存'),
        '求生': content.count('求生'),
        '怪物': content.count('怪物'),
        '海兽': content.count('海兽'),
    }

    # ========== 生成报告 ==========
    report = generate_report(content, lines, chapters, name_counts, keywords)

    # 写入文件
    output_path = 'material/小说分析/全民大航海我有一条幽灵船分析.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n分析报告已生成：{output_path}")
    return report

def generate_report(content, lines, chapters, name_counts, keywords):
    report = []

    report.append("# 《全民大航海：我有一条幽灵船》深度拆书分析报告")
    report.append("")
    report.append(f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"**文件大小**: {len(content):,} 字符 ({len(content)/10000:.1f} 万字)")
    report.append(f"**总行数**: {len(lines):,}")
    report.append(f"**检测章节数**: {len(chapters)}")
    report.append("")

    # --- 1. 作品概况 ---
    report.append("---")
    report.append("## 一、作品概况")
    report.append("")
    report.append("### 1.1 基本信息")
    report.append("")
    report.append("| 项目 | 数据 |")
    report.append("|------|------|")
    report.append(f"| 总字数 | {len(content):,} 字 |")
    report.append(f"| 总行数 | {len(lines):,} 行 |")
    report.append(f"| 平均每行 | {len(content)/len(lines):.1f} 字 |")
    report.append(f"| 章节数 | {len(chapters)} 章 |")
    report.append("")

    # 题材分类
    report.append("### 1.2 题材分类")
    report.append("")
    genre_scores = {
        '全民求生': content.count('全民') + content.count('求生') + content.count('生存'),
        '大航海': content.count('航海') + content.count('海域') + content.count('船长'),
        '系统流': content.count('系统') + content.count('面板') + content.count('属性'),
        '领主建设': content.count('领地') + content.count('建设') + content.count('基地'),
        '幽灵船': content.count('幽灵') + content.count('鬼船') + content.count('亡灵'),
    }
    sorted_genres = sorted(genre_scores.items(), key=lambda x: x[1], reverse=True)
    report.append("| 题材类型 | 关键词匹配 |")
    report.append("|----------|------------|")
    for genre, score in sorted_genres:
        report.append(f"| {genre} | {score} |")
    report.append("")
    report.append("**主要题材**: 全民求生 + 大航海 + 系统流")
    report.append("")

    # --- 2. 角色信息 ---
    report.append("---")
    report.append("## 二、角色信息分析")
    report.append("")

    report.append("### 2.1 主要角色（按出场频次）")
    report.append("")
    report.append("| 排名 | 角色名 | 出场次数 | 角色类型推测 |")
    report.append("|------|--------|----------|-------------|")

    top_chars = name_counts.most_common(20)
    for i, (name, count) in enumerate(top_chars, 1):
        char_type = "未知"
        if i == 1:
            char_type = "主角"
        elif i <= 5:
            char_type = "主要配角"
        elif i <= 10:
            char_type = "重要角色"
        else:
            char_type = "次要角色"
        report.append(f"| {i} | {name} | {count} | {char_type} |")
    report.append("")

    # 主角分析
    report.append("### 2.2 主角分析")
    report.append("")
    if top_chars:
        protagonist = top_chars[0][0]
        report.append(f"**主角姓名**: {protagonist}")
        report.append("")
        report.append("**角色设定**:")
        report.append("- **身份**: 参与全民航海求生的一员")
        report.append("- **金手指**: 拥有一条幽灵船（特殊船只系统）")
        report.append("- **能力**: 船长/航海相关")
        report.append("")

    # --- 3. 力量体系 ---
    report.append("---")
    report.append("## 三、力量体系分析")
    report.append("")

    report.append("### 3.1 核心能力关键词")
    report.append("")
    power_keywords = [
        ('系统', keywords.get('系统', content.count('系统'))),
        ('能力', keywords.get('能力', content.count('能力'))),
        ('升级', keywords.get('升级', content.count('升级'))),
        ('任务', keywords.get('任务', content.count('任务'))),
        ('奖励', keywords.get('奖励', content.count('奖励'))),
    ]
    report.append("| 关键词 | 出现次数 |")
    report.append("|--------|----------|")
    for kw, count in sorted(power_keywords, key=lambda x: x[1], reverse=True):
        report.append(f"| {kw} | {count} |")
    report.append("")

    report.append("### 3.2 力量体系推测")
    report.append("")
    report.append("基于关键词分析，本书力量体系可能包含:")
    report.append("1. **系统面板**: 角色通过系统面板查看属性和任务")
    report.append("2. **船只升级**: 幽灵船可以不断升级强化")
    report.append("3. **船员招募**: 招募船员增强实力")
    report.append("4. **海域探索**: 探索不同海域获得资源")
    report.append("")

    # --- 4. 世界观 ---
    report.append("---")
    report.append("## 四、世界观分析")
    report.append("")

    report.append("### 4.1 世界背景")
    report.append("")
    report.append("基于文本分析，本书世界观特征:")
    report.append("")
    report.append("- **核心设定**: 全民参与大航海求生")
    report.append(f"- **\"航海\"出现**: {keywords.get('航海', 0)} 次")
    report.append(f"- **\"海域\"出现**: {keywords.get('海域', 0)} 次")
    report.append(f"- **\"岛屿\"出现**: {keywords.get('岛屿', 0)} 次")
    report.append(f"- **\"幽灵船\"出现**: {keywords.get('幽灵船', 0)} 次")
    report.append("")

    report.append("### 4.2 主要地点/海域")
    report.append("")
    # 提取地点
    location_pattern = r'[\u4e00-\u9fa5]{2,6}(?:海 | 洋|湾|港|岛|屿|礁|滩)'
    locations = re.findall(location_pattern, content)
    location_counts = Counter(locations).most_common(15)

    report.append("| 地点 | 出现次数 | 类型 |")
    report.append("|------|----------|------|")
    for loc, count in location_counts:
        loc_type = "海域/地点"
        if '海' in loc:
            loc_type = "海域"
        elif '岛' in loc or '屿' in loc:
            loc_type = "岛屿"
        elif '港' in loc:
            loc_type = "港口"
        report.append(f"| {loc} | {count} | {loc_type} |")
    report.append("")

    # --- 5. 势力派别 ---
    report.append("---")
    report.append("## 五、势力派别分析")
    report.append("")

    report.append("### 5.1 主要势力")
    report.append("")
    # 提取势力
    org_pattern = r'[\u4e00-\u9fa5]{2,8}(?:团 | 队|帮|派|联盟|协会 | 公会 | 舰队|军团)'
    orgs = re.findall(org_pattern, content)
    org_counts = Counter(orgs).most_common(15)

    report.append("| 势力名称 | 出现次数 | 势力类型 |")
    report.append("|----------|----------|----------|")
    for org, count in org_counts:
        org_type = "未知"
        if '舰队' in org:
            org_type = "航海舰队"
        elif '团' in org or '队' in org:
            org_type = "团队组织"
        elif '公会' in org:
            org_type = "公会"
        report.append(f"| {org} | {count} | {org_type} |")
    if not org_counts:
        report.append("| 暂无明显势力名称 | - | - |")
    report.append("")

    # --- 6. 剧情主线 ---
    report.append("---")
    report.append("## 六、剧情主线分析")
    report.append("")

    report.append("### 6.1 核心故事主线")
    report.append("")
    report.append("基于书名和文本分析:")
    report.append("")
    report.append("1. **背景设定**: 全民参与大航海求生活动")
    report.append("2. **主角优势**: 拥有特殊幽灵船作为金手指")
    report.append("3. **主线任务**: 航海探索、生存发展、变强")
    report.append("4. **成长路线**: 船只升级 → 探索更广海域 → 面对更强挑战")
    report.append("")

    report.append("### 6.2 剧情钩子分析")
    report.append("")
    hook_words = ['突然', '竟然', '没想到', '意外', '震惊', '发现', '神秘', '恐怖']
    hooks = []
    early_content = content[:len(content)//10]
    for word in hook_words:
        if word in early_content:
            hooks.append(word)
    report.append("开篇使用的钩子手法:")
    for hook in hooks:
        report.append(f"- {hook}")
    report.append("")

    # --- 7. 文笔技巧 ---
    report.append("---")
    report.append("## 七、文笔编写技巧分析")
    report.append("")

    # 句子长度
    sentence_lengths = [len(line.strip()) for line in lines if line.strip()]
    avg_sentence_len = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0

    report.append("### 7.1 叙事风格")
    report.append("")
    report.append(f"- **平均句子长度**: {avg_sentence_len:.1f} 字")
    report.append("- **叙事视角**: 第三人称（推测）")
    report.append("")

    report.append("### 7.2 修辞手法使用")
    report.append("")
    rhetoric = {
        '比喻': len(re.findall(r'如 | 似 | 仿佛|犹如 | 像是', content)),
        '夸张': len(re.findall(r'极 | 最|无比|绝世', content)),
        '对比': len(re.findall(r'却 | 但|而|相反', content)),
    }
    report.append("| 修辞手法 | 使用次数 |")
    report.append("|----------|----------|")
    for device, count in rhetoric.items():
        report.append(f"| {device} | {count} |")
    report.append("")

    report.append("### 7.3 吸引读者的方法")
    report.append("")
    report.append("1. **金手指设定**: 幽灵船作为独特优势")
    report.append("2. **生存压力**: 航海求生的紧迫感")
    report.append("3. **探索未知**: 神秘海域和岛屿的吸引力")
    report.append("4. **成长反馈**: 船只升级的成就感")
    report.append("")

    # --- 8. 爽点设计 ---
    report.append("---")
    report.append("## 八、爽点设计分析")
    report.append("")

    cool_points = {
        '升级': content.count('升级') + content.count('突破') + content.count('强化'),
        '收获': content.count('获得') + content.count('奖励') + content.count('掉落'),
        '震惊': content.count('震惊') + content.count('骇然') + content.count('难以置信'),
        '领先': content.count('领先') + content.count('第一') + content.count('唯一'),
        '生存': content.count('生存') + content.count('活下') + content.count('安全'),
    }

    report.append("| 爽点类型 | 相关词频次 |")
    report.append("|----------|------------|")
    for cp, count in sorted(cool_points.items(), key=lambda x: x[1], reverse=True):
        report.append(f"| {cp} | {count} |")
    report.append("")

    # --- 9. 修炼/升级体系 ---
    report.append("---")
    report.append("## 九、修炼/升级体系")
    report.append("")

    report.append("### 9.1 船只升级体系")
    report.append("")
    report.append("基于文本分析，船只升级可能包含:")
    report.append("1. **船只等级**: 从小船到幽灵船的进化")
    report.append("2. **装备强化**: 船炮、船帆、船体等部件升级")
    report.append("3. **特殊能力**: 幽灵船独有的特殊技能")
    report.append("")

    report.append("### 9.2 个人成长体系")
    report.append("")
    report.append("1. **船长等级**: 船长的航海等级提升")
    report.append("2. **技能学习**: 航海相关技能")
    report.append("3. **属性强化**: 个人身体素质提升")
    report.append("")

    # --- 10. 题材分类 ---
    report.append("---")
    report.append("## 十、题材分类")
    report.append("")

    report.append("### 10.1 核心题材")
    report.append("")
    report.append("- **主标签**: 全民求生、大航海、系统流")
    report.append("- **副标签**: 领主建设、探险、生存")
    report.append("- **平台定位**: 男频、爽文、快节奏")
    report.append("")

    # --- 11. 可借鉴元素 ---
    report.append("---")
    report.append("## 十一、可借鉴作品元素")
    report.append("")

    report.append("### 11.1 核心设定借鉴")
    report.append("")
    report.append("1. **全民求生模式**: 所有人参与同一生存游戏")
    report.append("2. **幽灵船金手指**: 独特的船只优势")
    report.append("3. **航海探索**: 未知海域的神秘感")
    report.append("4. **系统面板**: 清晰的数据化反馈")
    report.append("")

    report.append("### 11.2 可学习的写作技巧")
    report.append("")
    report.append("1. **开篇设定**: 快速建立世界观和危机感")
    report.append("2. **金手指设计**: 独特且有用的优势")
    report.append("3. **节奏把控**: 探索 - 收获 - 升级循环")
    report.append("")

    # --- 12. 全文宗旨 ---
    report.append("---")
    report.append("## 十二、全文宗旨/主题")
    report.append("")

    themes = {
        '生存': content.count('生存') + content.count('活下去') + content.count('活着'),
        '成长': content.count('成长') + content.count('变强') + content.count('进步'),
        '探索': content.count('探索') + content.count('发现') + content.count('未知'),
        '自由': content.count('自由') + content.count('解放') + content.count('无拘'),
        '友情': content.count('友情') + content.count('伙伴') + content.count('同伴'),
    }

    report.append("| 主题 | 相关词频次 |")
    report.append("|------|------------|")
    for theme, count in sorted(themes.items(), key=lambda x: x[1], reverse=True):
        report.append(f"| {theme} | {count} |")
    report.append("")

    report.append("**核心主旨推测**: ")
    report.append("在全民航海的求生浪潮中，主角凭借幽灵船优势，")
    report.append("不断探索未知海域，生存变强，最终成为航海霸主。")
    report.append("")

    # --- 13. 读后感 ---
    report.append("---")
    report.append("## 十三、读后感与分析总结")
    report.append("")

    report.append("### 13.1 作品亮点")
    report.append("")
    report.append("1. **设定新颖**: 幽灵船作为金手指具有独特性")
    report.append("2. **代入感强**: 全民求生设定易引发共鸣")
    report.append("3. **成长清晰**: 船只升级路线明确")
    report.append("4. **探索乐趣**: 未知海域的神秘感")
    report.append("")

    report.append("### 13.2 可改进方向")
    report.append("")
    report.append("1. **配角塑造**: 可增加更多有个性的配角")
    report.append("2. **海战描写**: 可加强海战的紧张感")
    report.append("3. **世界观深度**: 可增加更多背景故事")
    report.append("")

    report.append("### 13.3 对本项目的借鉴意义")
    report.append("")
    report.append("1. **全民流设定**: 所有人参与同一规则的生存游戏")
    report.append("2. **独特金手指**: 幽灵船的差异性优势")
    report.append("3. **数据化反馈**: 系统面板的清晰成长")
    report.append("")

    report.append("---")
    report.append("*分析报告生成完成*")

    return '\n'.join(report)

if __name__ == '__main__':
    analyze_novel()
    print("分析完成!")
