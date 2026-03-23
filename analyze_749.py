#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
《大一实习，你跑去 749 收容怪物》深度分析脚本
"""

import os
import re
import json
from collections import Counter, defaultdict

def analyze_novel():
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

    # 读取完整内容
    with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    lines = content.split('\n')
    print(f"文件：{target_file}")
    print(f"总字符数：{len(content):,} ({len(content)/10000:.1f}万字)")
    print(f"总行数：{len(lines)}")

    # ========== 1. 章节结构分析 ==========
    print("\n" + "="*60)
    print("1. 章节结构分析")
    print("="*60)

    chapter_pattern = r'第 [一二三四五六七八九十百千 0-9]+章'
    chapters = []
    for i, line in enumerate(lines):
        match = re.search(chapter_pattern, line)
        if match:
            chapters.append((i, line.strip()))

    print(f"检测到章节数：{len(chapters)}")
    if chapters:
        print("\n章节列表（前 30 章）:")
        for idx, (line_num, title) in enumerate(chapters[:30]):
            print(f"  {idx+1:3d}. {title}")
        if len(chapters) > 30:
            print(f"  ... 还有 {len(chapters)-30} 章")

    # 提取所有章节标题用于后续分析
    chapter_titles = [title for _, title in chapters]

    # ========== 2. 角色分析 ==========
    print("\n" + "="*60)
    print("2. 角色信息分析")
    print("="*60)

    # 角色名提取 - 通过对话和行为动词
    char_names = []
    name_patterns = [
        r'([二三四五六七八九十百千]{1,3}[a-zA-Z\u4e00-\u9fa5]{1,3})\s*[ said 道喊问回答冷笑沉思皱眉点头摇头转身]',
        r'["\']([a-zA-Z\u4e00-\u9fa5]{2,4})["\'][ said 道喊问]',
        r'([a-zA-Z\u4e00-\u9fa5]{2,4})[说 道喊问回答]道?',
    ]

    # 从文中提取人名（更精确的方法）
    for i, line in enumerate(lines):
        # 查找"XXX 说道"、"XXX 问"等模式
        matches = re.findall(r'([a-zA-Z\u4e00-\u9fa5]{2,4})\s*(?:说 | 道|喊 | 问|回答|冷笑|沉思|皱眉|点头|摇头|转身 | 看向)', line)
        for m in matches:
            if len(m) >= 2 and len(m) <= 4:
                char_names.append(m)

    name_counts = Counter(char_names)
    print("\n高频角色名（可能是主角/配角）:")
    top_names = name_counts.most_common(30)
    for name, count in top_names:
        print(f"  {name}: {count}次")

    # ========== 3. 力量体系/能力关键词 ==========
    print("\n" + "="*60)
    print("3. 力量体系/能力关键词")
    print("="*60)

    power_keywords = [
        '序列', '异能', '天赋', '能力', '实力', '境界', '等级', '阶段',
        'S 级', 'A 级', 'B 级', 'C 级', 'D 级', 'E 级', 'F 级',
        '一阶', '二阶', '三阶', '四阶', '五阶', '六阶', '七阶', '八阶', '九阶',
        '一品', '二品', '三品', '四品', '五品', '六品', '七品', '八品', '九品',
        '觉醒', '进化', '突破', '晋升', '修炼', '强化',
        '精神', '肉体', '灵魂', '意志', '能量', '魔力', '灵力'
    ]

    print("\n力量体系关键词频次:")
    for kw in power_keywords:
        count = content.count(kw)
        if count > 5:
            print(f"  {kw}: {count}次")

    # ========== 4. 世界观/势力关键词 ==========
    print("\n" + "="*60)
    print("4. 世界观/势力分析")
    print("="*60)

    world_keywords = [
        '749', '收容', '异常', '灵异', '怪物', '诡异', '神秘',
        '组织', '协会', '联盟', '集团', '公司', '机构', '部门', '局', '所', '站',
        '世界', '全球', '国家', '城市', '基地', '总部', '分部',
        '任务', '行动', '调查', '探索', '狩猎', '清除', '消灭',
        '安全区', '禁区', '副本', '秘境', '领域', '空间', '维度'
    ]

    print("\n世界观关键词频次:")
    for kw in world_keywords:
        count = content.count(kw)
        if count > 5:
            print(f"  {kw}: {count}次")

    # ========== 5. 题材分类 ==========
    print("\n" + "="*60)
    print("5. 题材分类分析")
    print("="*60)

    genre_keywords = {
        '都市': ['都市', '城市', '公司', '学校', '公司', '上班', '下班', '地铁', '公交'],
        '玄幻': ['玄幻', '修炼', '灵力', '法术', '神通', '天道'],
        '科幻': ['科幻', '科技', '飞船', '机甲', 'AI', '智能', '基因'],
        '悬疑': ['悬疑', '谜团', '真相', '线索', '推理', '破案'],
        '恐怖': ['恐怖', '惊悚', ' horror', '鬼魂', ' zombie', '丧尸'],
        '系统': ['系统', '面板', '属性', '技能', '加点', '升级'],
        '末日': ['末日', ' apocalypse', '灾难', '废墟', '幸存者'],
        '无限': ['无限', '副本', '穿越', '轮回', '世界'],
    }

    print("\n题材分类关键词频次:")
    for genre, kws in genre_keywords.items():
        total = sum(content.count(kw) for kw in kws)
        if total > 10:
            print(f"  {genre}: {total}次")

    # ========== 6. 文笔技巧分析 ==========
    print("\n" + "="*60)
    print("6. 文笔技巧分析")
    print("="*60)

    # 对话比例
    dialogue_pattern = r'[""].*?[""]'
    dialogues = re.findall(dialogue_pattern, content)
    dialogue_ratio = len(dialogues) / len(lines) if lines else 0
    print(f"\n对话行数：{len(dialogues)}")
    print(f"对话占比：{dialogue_ratio*100:.1f}%")

    # 感叹号使用（情感强度）
    exclamation_count = content.count('!') + content.count('!')
    print(f"感叹号数量：{exclamation_count}")

    # 问句数量
    question_count = content.count('?') + content.count('?')
    print(f"问句数量：{question_count}")

    # 心理描写（他想、她暗想等）
    thought_pattern = r'(?:他 | 她 | 我 | 你|name)\s*(?:心想|暗想|想着|思索 | 思考|寻思)'
    thoughts = re.findall(thought_pattern, content)
    print(f"心理描写次数：{len(thoughts)}")

    # ========== 7. 爽点设计分析 ==========
    print("\n" + "="*60)
    print("7. 爽点设计分析")
    print("="*60)

    cool_point_keywords = {
        '打脸': ['打脸', '瞧不起', '轻视', '嘲讽', '不屑', '震惊', '骇然'],
        '装逼': ['装逼', '炫酷', '霸气', '威压', '震慑', '敬畏'],
        '升级': ['升级', '突破', '晋升', '变强', '提升', '进步'],
        '收获': ['收获', '奖励', '获得', '得到', '捡到', '掉落'],
        '复仇': ['复仇', '报仇', '雪恨', '清算', '讨回'],
        '守护': ['守护', '保护', '拯救', '救援', '捍卫'],
        '逆袭': ['逆袭', '翻盘', '反转', '绝地', '绝境']
    }

    print("\n爽点关键词频次:")
    for cool_type, kws in cool_point_keywords.items():
        total = sum(content.count(kw) for kw in kws)
        if total > 5:
            print(f"  {cool_type}: {total}次")

    # ========== 8. 核心主题 ==========
    print("\n" + "="*60)
    print("8. 核心主题/主旨分析")
    print("="*60)

    theme_keywords = {
        '成长': ['成长', '成熟', '改变', '蜕变', '历练'],
        '友情': ['友情', '兄弟', '伙伴', '同伴', '队友', '朋友'],
        '爱情': ['爱情', '喜欢', '爱', '恋情', '暗恋', '表白'],
        '亲情': ['亲情', '家人', '父母', '兄妹', '家庭'],
        '正义': ['正义', '公平', '良知', '道德', '信念'],
        '生存': ['生存', '活下去', '求生', '活着', '幸存'],
        '自由': ['自由', '解放', '挣脱', '束缚', '独立'],
        '真相': ['真相', '事实', '秘密', '揭秘', '揭露']
    }

    print("\n主题关键词频次:")
    for theme, kws in theme_keywords.items():
        total = sum(content.count(kw) for kw in kws)
        if total > 5:
            print(f"  {theme}: {total}次")

    # ========== 9. 保存分析数据 ==========
    print("\n" + "="*60)
    print("9. 保存分析数据")
    print("="*60)

    analysis_data = {
        'basic_info': {
            'filename': target_file,
            'total_chars': len(content),
            'total_lines': len(lines),
            'chapter_count': len(chapters)
        },
        'top_characters': dict(top_names),
        'chapter_titles': chapter_titles,
        'power_system_keywords': {},
        'world_keywords': {},
        'genre_analysis': {},
        'writing_style': {
            'dialogue_count': len(dialogues),
            'dialogue_ratio': dialogue_ratio,
            'exclamation_count': exclamation_count,
            'question_count': question_count,
            'thought_count': len(thoughts)
        },
        'cool_points': {}
    }

    # 保存数据
    output_file = 'material/小说分析/749_analysis_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_data, f, ensure_ascii=False, indent=2)
    print(f"分析数据已保存到：{output_file}")

    return content, chapters, analysis_data

if __name__ == '__main__':
    analyze_novel()
    print("\n分析完成!")
