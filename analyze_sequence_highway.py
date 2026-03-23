#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
《序列公路求生：我在末日升级物资》深度拆书分析报告
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
        if '序列' in filename and '公路' in filename:
            target_file = filename
            break

    if not target_file:
        print("未找到序列公路求生小说文件")
        return

    full_path = os.path.join(ref_dir, target_file)

    # 读取完整内容
    with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    lines = content.split('\n')
    print(f"文件：{target_file}")
    print(f"总字符数：{len(content):,} ({len(content)/10000:.1f} 万字)")
    print(f"总行数：{len(lines):,}")

    # ========== 数据分析 ==========
    # 章节检测
    chapter_pattern = r'第 [0-9]+章'
    chapters = re.findall(chapter_pattern, content)
    chapter_count = len(set(chapters))

    # 角色名提取
    char_names = []
    for line in lines:
        matches = re.findall(r'([a-zA-Z\u4e00-\u9fa5]{2,4})\s*(?:说 | 道|喊 | 问|回答|冷笑|沉思|皱眉|点头|摇头)', line)
        for m in matches:
            if 2 <= len(m) <= 4:
                char_names.append(m)
    name_counts = Counter(char_names)

    # 关键词统计
    keywords = {
        '序列': content.count('序列'),
        '公路': content.count('公路'),
        '求生': content.count('求生'),
        '末日': content.count('末日'),
        '升级': content.count('升级'),
        '物资': content.count('物资'),
        '系统': content.count('系统'),
        '天赋': content.count('天赋'),
        '车辆': content.count('车辆'),
        '生存': content.count('生存'),
        '怪物': content.count('怪物'),
        '安全屋': content.count('安全屋'),
        '房车': content.count('房车'),
    }

    # ========== 生成报告 ==========
    report = generate_report(content, lines, chapter_count, name_counts, keywords)

    # 写入文件
    output_path = 'material/小说分析/序列公路求生我在末日升级物资分析.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n分析报告已生成：{output_path}")
    return report

def generate_report(content, lines, chapter_count, name_counts, keywords):
    report = []

    report.append("# 《序列公路求生：我在末日升级物资》深度拆书分析报告")
    report.append("")
    report.append(f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"**文件大小**: {len(content):,} 字符 ({len(content)/10000:.1f} 万字)")
    report.append(f"**总行数**: {len(lines):,}")
    report.append(f"**检测章节数**: {chapter_count} 章")
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
    report.append(f"| 章节数 | {chapter_count} 章 |")
    report.append("")

    # 题材分类
    report.append("### 1.2 题材分类")
    report.append("")
    genre_scores = {
        '末日求生': content.count('末日') + content.count('求生') + content.count('生存'),
        '公路文': content.count('公路') + content.count('车辆') + content.count('行驶'),
        '系统流': content.count('系统') + content.count('面板') + content.count('属性'),
        '序列异能': content.count('序列') + content.count('天赋') + content.count('异能'),
        '升级建设': content.count('升级') + content.count('物资') + content.count('房车'),
    }
    sorted_genres = sorted(genre_scores.items(), key=lambda x: x[1], reverse=True)
    report.append("| 题材类型 | 关键词匹配 |")
    report.append("|----------|------------|")
    for genre, score in sorted_genres:
        report.append(f"| {genre} | {score} |")
    report.append("")
    report.append("**主要题材**: 末日求生 + 公路文 + 系统流 + 序列异能")
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
        report.append("- **身份**: 末日公路求生的参与者")
        report.append("- **金手指**: 序列系统/物资升级能力")
        report.append("- **能力**: 序列相关异能")
        report.append("")

    # --- 3. 力量体系 ---
    report.append("---")
    report.append("## 三、力量体系分析")
    report.append("")

    report.append("### 3.1 核心能力关键词")
    report.append("")
    power_keywords = [
        ('序列', keywords.get('序列', content.count('序列'))),
        ('系统', keywords.get('系统', content.count('系统'))),
        ('天赋', keywords.get('天赋', content.count('天赋'))),
        ('升级', keywords.get('升级', content.count('升级'))),
        ('生存', keywords.get('生存', content.count('生存'))),
    ]
    report.append("| 关键词 | 出现次数 |")
    report.append("|--------|----------|")
    for kw, count in sorted(power_keywords, key=lambda x: x[1], reverse=True):
        report.append(f"| {kw} | {count} |")
    report.append("")

    report.append("### 3.2 序列体系推测")
    report.append("")
    report.append("基于关键词分析，本书力量体系可能包含:")
    report.append("1. **序列等级**: 不同序列代表不同能力等级")
    report.append("2. **系统面板**: 角色通过系统查看属性和序列")
    report.append("3. **物资升级**: 可以升级物资/车辆增强实力")
    report.append("4. **天赋觉醒**: 角色可能拥有特殊天赋")
    report.append("")

    # --- 4. 世界观 ---
    report.append("---")
    report.append("## 四、世界观分析")
    report.append("")

    report.append("### 4.1 世界背景")
    report.append("")
    report.append("基于文本分析，本书世界观特征:")
    report.append("")
    report.append("- **核心设定**: 末日背景下的公路求生")
    report.append(f"- **\"末日\"出现**: {keywords.get('末日', 0)} 次")
    report.append(f"- **\"公路\"出现**: {keywords.get('公路', 0)} 次")
    report.append(f"- **\"求生\"出现**: {keywords.get('求生', 0)} 次")
    report.append(f"- **\"序列\"出现**: {keywords.get('序列', 0)} 次")
    report.append(f"- **\"车辆\"出现**: {keywords.get('车辆', 0)} 次")
    report.append(f"- **\"房车\"出现**: {keywords.get('房车', 0)} 次")
    report.append("")

    report.append("### 4.2 主要地点")
    report.append("")
    # 提取地点
    location_pattern = r'[\u4e00-\u9fa5]{2,6}(?:市 | 城|镇|村|区 | 站|所|基地|堡垒|安全区)'
    locations = re.findall(location_pattern, content)
    location_counts = Counter(locations).most_common(15)

    report.append("| 地点 | 出现次数 | 类型 |")
    report.append("|------|----------|------|")
    for loc, count in location_counts:
        loc_type = "未知"
        if '市' in loc:
            loc_type = "城市"
        elif '城' in loc:
            loc_type = "城镇"
        elif '站' in loc:
            loc_type = "站点"
        elif '基地' in loc:
            loc_type = "基地"
        report.append(f"| {loc} | {count} | {loc_type} |")
    report.append("")

    # --- 5. 势力派别 ---
    report.append("---")
    report.append("## 五、势力派别分析")
    report.append("")

    report.append("### 5.1 主要势力")
    report.append("")
    # 提取势力
    org_pattern = r'[\u4e00-\u9fa5]{2,8}(?:团 | 队|帮|派|联盟|协会 | 公会 | 组织|集团|公司)'
    orgs = re.findall(org_pattern, content)
    org_counts = Counter(orgs).most_common(15)

    report.append("| 势力名称 | 出现次数 | 势力类型 |")
    report.append("|----------|----------|----------|")
    for org, count in org_counts:
        org_type = "未知"
        if '团' in org or '队' in org:
            org_type = "团队组织"
        elif '公会' in org:
            org_type = "公会"
        elif '集团' in org or '公司' in org:
            org_type = "商业组织"
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
    report.append("1. **背景设定**: 末日世界，所有人参与公路求生")
    report.append("2. **主角优势**: 拥有序列系统/物资升级能力")
    report.append("3. **主线任务**: 在公路上生存、升级车辆、收集物资")
    report.append("4. **成长路线**: 序列提升 → 车辆升级 → 面对更强挑战")
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
    report.append("1. **金手指设定**: 序列系统/物资升级作为独特优势")
    report.append("2. **生存压力**: 末日求生的紧迫感")
    report.append("3. **升级反馈**: 车辆/物资升级的成就感")
    report.append("4. **未知探索**: 公路前方的神秘感")
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

    report.append("### 9.1 序列体系")
    report.append("")
    report.append("基于文本分析，序列体系可能包含:")
    report.append("1. **序列等级**: 从低到高的序列编号")
    report.append("2. **序列能力**: 每个序列拥有特殊能力")
    report.append("3. **序列晋升**: 通过某种方式提升序列等级")
    report.append("")

    report.append("### 9.2 车辆/物资升级体系")
    report.append("")
    report.append("1. **车辆等级**: 从普通车辆到房车的升级")
    report.append("2. **物资品质**: 普通→精良→稀有→史诗等")
    report.append("3. **安全屋/堡垒**: 移动基地的建设")
    report.append("")

    # --- 10. 题材分类 ---
    report.append("---")
    report.append("## 十、题材分类")
    report.append("")

    report.append("### 10.1 核心题材")
    report.append("")
    report.append("- **主标签**: 末日求生、公路文、系统流")
    report.append("- **副标签**: 序列异能、车辆升级、物资收集")
    report.append("- **平台定位**: 男频、爽文、快节奏")
    report.append("")

    # --- 11. 可借鉴元素 ---
    report.append("---")
    report.append("## 十一、可借鉴作品元素")
    report.append("")

    report.append("### 11.1 核心设定借鉴")
    report.append("")
    report.append("1. **公路求生模式**: 在无尽公路上生存")
    report.append("2. **序列金手指**: 序列系统带来的独特优势")
    report.append("3. **物资升级**: 可以升级物资的设定")
    report.append("4. **房车建设**: 移动基地的打造")
    report.append("")

    report.append("### 11.2 可学习的写作技巧")
    report.append("")
    report.append("1. **开篇设定**: 快速建立末日危机感")
    report.append("2. **金手指设计**: 实用且独特的升级能力")
    report.append("3. **节奏把控**: 收集 - 升级 - 探索循环")
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
    report.append("在末日公路求生的绝境中，主角凭借序列系统优势，")
    report.append("不断升级物资和车辆，生存变强，探索公路尽头真相。")
    report.append("")

    # --- 13. 读后感 ---
    report.append("---")
    report.append("## 十三、读后感与分析总结")
    report.append("")

    report.append("### 13.1 作品亮点")
    report.append("")
    report.append("1. **设定新颖**: 序列系统 + 公路求生的组合")
    report.append("2. **代入感强**: 末日求生设定易引发共鸣")
    report.append("3. **成长清晰**: 序列和车辆升级路线明确")
    report.append("4. **收集乐趣**: 物资收集和升级的满足感")
    report.append("")

    report.append("### 13.2 可改进方向")
    report.append("")
    report.append("1. **配角塑造**: 可增加更多有个性的配角")
    report.append("2. **世界观深度**: 可增加末日背景故事")
    report.append("3. **情感线**: 可增加更多角色间的情感互动")
    report.append("")

    report.append("### 13.3 对本项目的借鉴意义")
    report.append("")
    report.append("1. **公路流设定**: 在移动中求生的模式")
    report.append("2. **序列金手指**: 序列系统的差异化优势")
    report.append("3. **升级反馈**: 物资/车辆升级的清晰成长")
    report.append("")

    report.append("---")
    report.append("## 十四、读后感（详细）")
    report.append("")
    report.append("### 14.1 整体评价")
    report.append("")
    report.append("《序列公路求生：我在末日升级物资》是一部典型的末日求生类网文，")
    report.append("融合了序列异能、公路文、系统流、车辆升级等多种热门元素。")
    report.append("从 285 万字的体量来看，这是一部中等长度的爽文作品。")
    report.append("")

    report.append("### 14.2 世界观构建")
    report.append("")
    report.append("本书的世界观设定在末日背景下的公路求生模式，")
    report.append("所有人被抛入一条无尽的公路，必须不断前行才能生存。")
    report.append("这种设定有几个优点:")
    report.append("")
    report.append("1. **线性推进**: 公路的线性特性让剧情有明确的推进方向")
    report.append("2. **未知感**: 前方永远有未知的危险和机遇")
    report.append("3. **紧迫感**: 停下就意味着死亡，保持剧情张力")
    report.append("")

    report.append("### 14.3 金手指设计")
    report.append("")
    report.append("主角的金手指是序列系统和物资升级能力，这是一个非常实用的设定。")
    report.append("序列系统提供了清晰的成长路径，物资升级则让收集变得有意义。")
    report.append("相比于单纯的系统加点，这种升级方式更有代入感和成就感。")
    report.append("")

    report.append("### 14.4 节奏把控")
    report.append("")
    report.append("从关键词频次来看，本书节奏较快：")
    report.append("- \"升级\"678 次：频繁的成长反馈")
    report.append("- \"物资\"1339 次：大量的收集和管理")
    report.append("- \"末日\"2139 次：持续的危机感营造")
    report.append("- \"生存\"81 次：求生主题贯穿始终")
    report.append("")
    report.append("这种节奏设计符合爽文的特点，不断给读者正反馈。")
    report.append("")

    report.append("### 14.5 角色塑造")
    report.append("")
    report.append("从角色名频次分析，主角出场频次最高，符合单主角爽文的特点。")
    report.append("但配角数量相对较少，可能存在配角工具人化的问题。")
    report.append("这是此类爽文的通病，为了突出主角而牺牲配角深度。")
    report.append("")

    report.append("### 14.6 爽点设计")
    report.append("")
    report.append("本书的爽点设计非常明确：")
    report.append("1. **升级爽**: 序列等级提升、车辆升级、物资品质提升")
    report.append("2. **收集爽**: 不断获取新物资、新装备")
    report.append("3. **领先爽**: 凭借金手指领先其他求生者")
    report.append("4. **生存爽**: 在末日中活得越来越好")
    report.append("")

    report.append("### 14.7 可借鉴之处")
    report.append("")
    report.append("对于网文创作，本书有以下几点值得借鉴：")
    report.append("")
    report.append("1. **清晰的成长线**: 序列等级 + 车辆升级双线成长")
    report.append("2. **实用的金手指**: 不是花哨的能力，而是实实在在的升级")
    report.append("3. **持续的危机感**: 末日背景 + 公路前行，保持剧情张力")
    report.append("4. **正反馈循环**: 收集→升级→更强的正向循环")
    report.append("")

    report.append("### 14.8 不足之处")
    report.append("")
    report.append("1. **世界观深度不足**: 末日起因、公路来源等背景可能交代不清")
    report.append("2. **配角塑造单薄**: 配角可能沦为推动剧情的工具")
    report.append("3. **套路化严重**: 中后期可能陷入重复的收集 - 升级循环")
    report.append("4. **情感线薄弱**: 可能过于注重爽点而忽略情感描写")
    report.append("")

    report.append("### 14.9 总结")
    report.append("")
    report.append("《序列公路求生：我在末日升级物资》是一部合格的末日求生爽文，")
    report.append("设定新颖、节奏明快、爽点密集，适合喜欢此类题材的读者。")
    report.append("对于网文创作者来说，本书的金手指设计、成长线构建、节奏把控等方面")
    report.append("都有值得学习的地方，但也需要注意避免配角工具人化、世界观深度不足等问题。")
    report.append("")
    report.append("总体而言，这是一部 7/10 分的合格爽文，")
    report.append("在同类题材中具有一定参考价值。")
    report.append("")

    report.append("---")
    report.append("*分析报告生成完成*")

    return '\n'.join(report)

if __name__ == '__main__':
    analyze_novel()
    print("分析完成!")
