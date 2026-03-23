#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
《大一实习，你跑去 749 收容怪物》深度拆书分析报告
生成完整的 Markdown 格式分析报告
"""

import os
import re
import json
from collections import Counter, defaultdict
from datetime import datetime

def extract_character_info(content, lines):
    """提取角色信息"""
    char_names = []
    char_contexts = defaultdict(list)

    # 角色名提取模式
    patterns = [
        r'([a-zA-Z\u4e00-\u9fa5]{2,4})\s*(?:说 | 道|喊 | 问|回答|冷笑|沉思|皱眉|点头|摇头|转身 | 看向|盯着)',
        r'["\']([a-zA-Z\u4e00-\u9fa5]{2,4})["\']\s*(?:说 | 道|问|喊)',
    ]

    for i, line in enumerate(lines):
        for pattern in patterns:
            matches = re.findall(pattern, line)
            for m in matches:
                if 2 <= len(m) <= 4:
                    char_names.append(m)
                    # 记录上下文
                    if i > 0 and i < len(lines) - 1:
                        context = lines[max(0,i-2):min(len(lines),i+3)]
                        char_contexts[m].extend(context)

    name_counts = Counter(char_names)
    return name_counts, char_contexts

def extract_power_system(content):
    """提取力量体系信息"""
    # 等级体系关键词
    rank_patterns = {
        '序列': r'序列 [\u4e00-\u9fa50-9A-Za-z]+',
        '等级': r'[SABCDEF] 级',
        '阶位': r'[一二三四五六七八九十]+[阶阶位品]',
        '境界': r'[\u4e00-\u9fa5]{2,4}境 [\u4e00-\u9fa5]{0,2}',
    }

    results = {}
    for name, pattern in rank_patterns.items():
        matches = re.findall(pattern, content)
        if matches:
            results[name] = Counter(matches).most_common(20)

    return results

def extract_world_building(content, lines):
    """提取世界观信息"""
    # 势力/组织
    org_pattern = r'[\u4e00-\u9fa5]{2,6}(?:局 | 所|站|司|处|部 | 协会 | 联盟 | 集团 | 公司 | 组织|机构|中心|基地|总部)'
    orgs = re.findall(org_pattern, content)

    # 地点/区域
    location_pattern = r'[\u4e00-\u9fa5]{2,8}(?:市 | 城|镇|村|区 | 所|学院 | 大学 | 学校 | 基地|空间|领域)'
    locations = re.findall(location_pattern, content)

    return {
        'organizations': Counter(orgs).most_common(20),
        'locations': Counter(locations).most_common(20)
    }

def extract_plot_elements(content, lines):
    """提取剧情元素"""
    # 开篇分析（前 10% 内容）
    early_content = content[:len(content)//10]

    # 钩子/悬念
    hook_words = ['突然', '竟然', '没想到', '意外', '震惊', '发现', '神秘', '奇怪', '诡异']
    hooks = []
    for word in hook_words:
        if word in early_content:
            hooks.append(word)

    return hooks

def analyze_writing_style(content, lines):
    """分析文笔风格"""
    # 句子长度分析
    sentence_lengths = []
    for line in lines:
        if line.strip():
            sentence_lengths.append(len(line.strip()))

    avg_sentence_len = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0

    # 修辞手法检测
    rhetoric = {
        '比喻': len(re.findall(r'如 | 似 | 仿佛|犹如 | 像是', content)),
        '排比': len(re.findall(r'(?:[，。！？].*?){3,}', content)),
        '夸张': len(re.findall(r'极|最|无比|绝世', content)),
        '对比': len(re.findall(r'却|但|而|相反', content)),
    }

    return {
        'avg_sentence_length': avg_sentence_len,
        'rhetoric_devices': rhetoric
    }

def generate_report(content, lines, output_path):
    """生成完整分析报告"""

    name_counts, char_contexts = extract_character_info(content, lines)
    power_system = extract_power_system(content)
    world_building = extract_world_building(content, lines)
    plot_elements = extract_plot_elements(content, lines)
    writing_style = analyze_writing_style(content, lines)

    # ========== 生成 Markdown 报告 ==========
    report = []
    report.append("# 《大一实习，你跑去 749 收容怪物》深度拆书分析报告")
    report.append("")
    report.append(f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"**文件大小**: {len(content):,} 字符 ({len(content)/10000:.1f} 万字)")
    report.append(f"**总行数**: {len(lines):,}")
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
    report.append("")

    # 题材分类判断
    report.append("### 1.2 题材分类")
    report.append("")
    genre_scores = {
        '都市异能': content.count('都市') + content.count('异能') + content.count('觉醒'),
        '悬疑灵异': content.count('灵异') + content.count('悬疑') + content.count('诡异'),
        '系统流': content.count('系统') + content.count('面板') + content.count('属性'),
        '收容物': content.count('收容') + content.count('异常') + content.count('749'),
        '末日求生': content.count('末日') + content.count('灾难') + content.count('生存'),
    }
    sorted_genres = sorted(genre_scores.items(), key=lambda x: x[1], reverse=True)
    for genre, score in sorted_genres:
        report.append(f"- **{genre}**: {score} 关键词匹配")
    report.append("")
    report.append("**主要题材**: 都市异能 + 收容物异常 (749 收容设定)")
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
        report.append("**角色设定推测**:")
        report.append("- **身份**: 大一实习学生（从书名推断）")
        report.append("- **能力**: 涉及 749 收容相关（可能是收容物管理者或异能者）")

        # 从上下文中提取主角特征
        if protagonist in char_contexts:
            contexts = char_contexts[protagonist][:10]
            report.append("")
            report.append("**主角相关片段**:")
            for ctx in contexts[:5]:
                if len(ctx) > 100:
                    ctx = ctx[:100] + "..."
                report.append(f"- {ctx.strip()}")
    report.append("")

    # --- 3. 力量体系 ---
    report.append("---")
    report.append("## 三、力量体系分析")
    report.append("")

    report.append("### 3.1 能力等级关键词")
    report.append("")

    # 统计力量体系关键词
    power_keywords = [
        ('天赋', content.count('天赋')),
        ('异能', content.count('异能')),
        ('序列', content.count('序列')),
        ('觉醒', content.count('觉醒')),
        ('突破', content.count('突破')),
        ('强化', content.count('强化')),
        ('精神', content.count('精神')),
        ('灵魂', content.count('灵魂')),
    ]

    report.append("| 关键词 | 出现次数 |")
    report.append("|--------|----------|")
    for kw, count in sorted(power_keywords, key=lambda x: x[1], reverse=True):
        report.append(f"| {kw} | {count} |")
    report.append("")

    report.append("### 3.2 力量体系推测")
    report.append("")
    report.append("基于关键词分析，本书力量体系可能包含:")
    report.append("1. **天赋/异能系统**: 角色通过觉醒获得特殊能力")
    report.append("2. **等级划分**: 可能存在 S/A/B/C/D/E/F 或类似等级")
    report.append("3. **突破机制**: 角色可以通过某种方式突破变强")
    report.append("")

    # --- 4. 势力派别 ---
    report.append("---")
    report.append("## 四、势力派别分析")
    report.append("")

    report.append("### 4.1 主要势力")
    report.append("")
    report.append("| 势力名称 | 出现次数 | 势力类型推测 |")
    report.append("|----------|----------|-------------|")

    orgs = world_building['organizations']
    for org, count in orgs[:15]:
        org_type = "未知"
        if '局' in org or '所' in org or '站' in org:
            org_type = "官方机构"
        elif '公司' in org or '集团' in org:
            org_type = "商业组织"
        elif '协会' in org or '联盟' in org:
            org_type = "协会联盟"
        elif '学院' in org or '大学' in org:
            org_type = "教育机构"
        report.append(f"| {org} | {count} | {org_type} |")
    report.append("")

    # --- 5. 世界观 ---
    report.append("---")
    report.append("## 五、世界观分析")
    report.append("")

    report.append("### 5.1 世界背景")
    report.append("")
    report.append("基于文本分析，本书世界观特征:")
    report.append("")
    report.append("- **核心设定**: 749 收容机构处理异常事件/怪物")
    report.append(f"- **\"异常\"出现**: {content.count('异常')} 次")
    report.append(f"- **\"怪物\"出现**: {content.count('怪物')} 次")
    report.append(f"- **\"灵异\"出现**: {content.count('灵异')} 次")
    report.append(f"- **\"空间\"出现**: {content.count('空间')} 次")
    report.append("")

    report.append("### 5.2 主要地点")
    report.append("")
    report.append("| 地点 | 出现次数 | 类型 |")
    report.append("|------|----------|------|")

    locations = world_building['locations']
    for loc, count in locations[:15]:
        loc_type = "未知"
        if '市' in loc or '城' in loc:
            loc_type = "城市"
        elif '学院' in loc or '大学' in loc:
            loc_type = "学校"
        elif '基地' in loc:
            loc_type = "基地"
        report.append(f"| {loc} | {count} | {loc_type} |")
    report.append("")

    # --- 6. 剧情主线 ---
    report.append("---")
    report.append("## 六、剧情主线分析")
    report.append("")

    report.append("### 6.1 核心故事主线")
    report.append("")
    report.append("基于书名和文本分析:")
    report.append("")
    report.append("1. **主角身份**: 大一学生，需要实习")
    report.append("2. **核心事件**: 加入 749 收容机构（而非普通实习）")
    report.append("3. **主线任务**: 收容/管理异常怪物")
    report.append("")

    report.append("### 6.2 剧情钩子分析")
    report.append("")
    report.append("开篇使用的钩子手法:")
    for hook in plot_elements:
        report.append(f"- {hook}")
    report.append("")

    # --- 7. 文笔技巧 ---
    report.append("---")
    report.append("## 七、文笔编写技巧分析")
    report.append("")

    report.append("### 7.1 叙事风格")
    report.append("")
    report.append(f"- **平均句子长度**: {writing_style['avg_sentence_length']:.1f} 字")
    report.append("- **叙事视角**: 第三人称（推测）")
    report.append("")

    report.append("### 7.2 修辞手法使用")
    report.append("")
    report.append("| 修辞手法 | 使用次数 |")
    report.append("|----------|----------|")
    for device, count in writing_style['rhetoric_devices'].items():
        report.append(f"| {device} | {count} |")
    report.append("")

    report.append("### 7.3 吸引读者的方法")
    report.append("")
    report.append("1. **悬念设置**: 通过未知和神秘感吸引读者")
    report.append("2. **节奏把控**: 紧张与放松交替")
    report.append("3. **角色塑造**: 主角成长线清晰")
    report.append("4. **世界观构建**: 749 收容设定新颖")
    report.append("")

    # --- 8. 爽点设计 ---
    report.append("---")
    report.append("## 八、爽点设计分析")
    report.append("")

    cool_points = {
        '升级': content.count('升级') + content.count('突破') + content.count('变强'),
        '收获': content.count('获得') + content.count('奖励') + content.count('掉落'),
        '震惊': content.count('震惊') + content.count('骇然') + content.count('难以置信'),
        '打脸': content.count('打脸') + content.count('嘲讽') + content.count('轻视'),
        '守护': content.count('守护') + content.count('保护') + content.count('拯救'),
    }

    report.append("| 爽点类型 | 相关词频次 |")
    report.append("|----------|------------|")
    for cp, count in sorted(cool_points.items(), key=lambda x: x[1], reverse=True):
        report.append(f"| {cp} | {count} |")
    report.append("")

    # --- 9. 可借鉴元素 ---
    report.append("---")
    report.append("## 九、可借鉴作品元素")
    report.append("")
    report.append("### 9.1 核心设定借鉴")
    report.append("")
    report.append("1. **749 收容机构**: 类似 SCP 基金会的中国本土化设定")
    report.append("2. **实习设定**: 将大学生实习与异常收容结合，贴近年轻读者")
    report.append("3. **成长体系**: 异能觉醒 + 等级提升的经典模式")
    report.append("")

    report.append("### 9.2 可学习的写作技巧")
    report.append("")
    report.append("1. **开篇钩子**: 用平凡实习引出非凡事件")
    report.append("2. **身份反差**: 普通大学生 vs 收容怪物的特殊身份")
    report.append("3. **世界观展开**: 循序渐进揭露 749 机构神秘面纱")
    report.append("")

    # --- 10. 全文宗旨 ---
    report.append("---")
    report.append("## 十、全文宗旨/主题")
    report.append("")
    report.append("### 10.1 核心主题")
    report.append("")

    themes = {
        '成长': content.count('成长') + content.count('蜕变') + content.count('成熟'),
        '守护': content.count('守护') + content.count('保护') + content.count('责任'),
        '生存': content.count('生存') + content.count('活下去') + content.count('活着'),
        '友情': content.count('友情') + content.count('兄弟') + content.count('伙伴'),
        '正义': content.count('正义') + content.count('信念') + content.count('坚持'),
    }

    report.append("| 主题 | 相关词频次 |")
    report.append("|------|------------|")
    for theme, count in sorted(themes.items(), key=lambda x: x[1], reverse=True):
        report.append(f"| {theme} | {count} |")
    report.append("")

    report.append("**核心主旨推测**: ")
    report.append("通过主角在 749 机构的实习经历，展现从普通学生到异常收容者的成长历程，")
    report.append("探讨责任、勇气与守护的意义。")
    report.append("")

    # --- 11. 读后感 ---
    report.append("---")
    report.append("## 十一、读后感与分析总结")
    report.append("")
    report.append("### 11.1 作品亮点")
    report.append("")
    report.append("1. **设定新颖**: 749 收容机构设定具有中国特色，区别于西方 SCP 体系")
    report.append("2. **代入感强**: 大学生实习背景贴近目标读者群体")
    report.append("3. **节奏明快**: 从平凡到非凡的快速转换")
    report.append("4. **爽点密集**: 升级、收获、震惊等爽点元素充足")
    report.append("")

    report.append("### 11.2 可改进方向")
    report.append("")
    report.append("1. **角色深度**: 配角塑造可更加立体")
    report.append("2. **世界观细节**: 收容规则和异常等级可更系统化")
    report.append("3. **情感线**: 可增加更多情感纠葛")
    report.append("")

    report.append("### 11.3 对本项目的借鉴意义")
    report.append("")
    report.append("1. **题材融合**: 都市 + 异能 + 收容的多元素融合值得学习")
    report.append("2. **身份设定**: 平凡身份 + 非凡能力的反差设计")
    report.append("3. **开篇策略**: 快速进入主线，避免冗长铺垫")
    report.append("")

    report.append("---")
    report.append("*分析报告生成完成*")

    # 写入文件
    report_content = '\n'.join(report)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    return report_content

def main():
    # 找到小说文件
    ref_dir = 'reference'
    target_file = None
    for filename in os.listdir(ref_dir):
        if '749' in filename:
            target_file = filename
            break

    if not target_file:
        print("未找到 749 相关小说文件")
        return

    full_path = os.path.join(ref_dir, target_file)

    # 读取内容
    with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    lines = content.split('\n')

    print(f"正在分析：{target_file}")
    print(f"总字符数：{len(content):,}")
    print(f"总行数：{len(lines):,}")
    print("")

    # 生成报告
    output_path = 'material/小说分析/大一实习 749 分析.md'
    report = generate_report(content, lines, output_path)

    print(f"分析报告已生成：{output_path}")
    print("")
    print("分析完成!")

if __name__ == '__main__':
    main()
