# -*- coding: utf-8 -*-
"""
诡秘之主深度分析 - 提取角色详细信息和文本片段
"""
import os
import re
import json
from collections import Counter

# 设置输出编码
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 读取所有文件内容
print("正在读取文件...")
all_content = ''
for i in range(1, 12):
    with open(f'{i}.txt', 'r', encoding='utf-8') as f:
        all_content += f.read()

print(f"总字符数：{len(all_content):,}")

# ============ 提取角色相关段落 ============
print("\n=== 提取角色相关段落 ===")

# 角色详细信息提取
characters_detail = {
    '克莱恩·莫雷蒂': {
        'keywords': ['克莱恩', '莫雷蒂', '周明瑞'],
        'description': '',
        'traits': [],
        'abilities': [],
        'quotes': []
    },
    '奥黛丽·霍尔': {
        'keywords': ['奥黛丽', '正义', '霍尔小姐', '观众'],
        'description': '',
        'traits': [],
        'abilities': []
    },
    '阿尔杰·威尔逊': {
        'keywords': ['阿尔杰', '倒吊人', '威尔逊'],
        'description': '',
        'traits': [],
        'abilities': []
    },
    '佛尔思·沃尔': {
        'keywords': ['佛尔思', '魔术师', '沃尔'],
        'description': '',
        'traits': [],
        'abilities': []
    },
    '休·迪尔查': {
        'keywords': ['休', '审判', '迪尔查'],
        'description': '',
        'traits': [],
        'abilities': []
    },
    '戴里克·伯格': {
        'keywords': ['戴里克', '太阳', '伯格'],
        'description': '',
        'traits': [],
        'abilities': []
    },
    '埃姆林·怀特': {
        'keywords': ['埃姆林', '月亮', '怀特'],
        'description': '',
        'traits': [],
        'abilities': []
    },
    '阿蒙': {
        'keywords': ['阿蒙', '时天使', '错误'],
        'description': '',
        'traits': [],
        'abilities': []
    },
    '阿兹克·铜哨': {
        'keywords': ['阿兹克', '铜哨', '死灵'],
        'description': '',
        'traits': [],
        'abilities': []
    },
}

# 提取包含角色名的上下文段落
def extract_context(text, keyword, window=100):
    """提取关键词周围的上下文"""
    contexts = []
    idx = 0
    while idx < len(text):
        pos = text.find(keyword, idx)
        if pos == -1:
            break
        start = max(0, pos - window)
        end = min(len(text), pos + len(keyword) + window)
        context = text[start:end].replace('\n', ' ')
        contexts.append(context)
        idx = pos + 1
    return contexts

# 为每个角色提取样本段落
print("\n提取角色相关段落样本...")
for char_name, char_info in characters_detail.items():
    all_contexts = []
    for kw in char_info['keywords'][:2]:  # 用前两个关键词
        contexts = extract_context(all_content, kw, window=50)
        all_contexts.extend(contexts[:5])  # 每个关键词取 5 个样本

    # 去重
    unique_contexts = list(set(all_contexts))[:10]
    char_info['samples'] = unique_contexts
    print(f"  {char_name}: 提取 {len(unique_contexts)} 个段落样本")

# ============ 提取力量体系详细信息 ============
print("\n=== 提取力量体系信息 ===")

power_system_detail = {
    '序列等级': [],
    '魔药配方': [],
    '晋升仪式': [],
    '扮演法则': [],
}

# 提取包含"序列"的段落
seq_contexts = extract_context(all_content, '序列', window=80)
# 去重并采样
unique_seq = list(set(seq_contexts))[:30]
power_system_detail['序列等级'] = unique_seq

# 提取包含"魔药"的段落
potion_contexts = extract_context(all_content, '魔药', window=80)
unique_potion = list(set(potion_contexts))[:20]
power_system_detail['魔药配方'] = unique_potion

# 提取包含"仪式"的段落
ritual_contexts = extract_context(all_content, '仪式', window=80)
unique_ritual = list(set(ritual_contexts))[:20]
power_system_detail['晋升仪式'] = unique_ritual

print(f"  提取序列相关段落：{len(unique_seq)} 个")
print(f"  提取魔药相关段落：{len(unique_potion)} 个")
print(f"  提取仪式相关段落：{len(unique_ritual)} 个")

# ============ 提取世界观描述 ============
print("\n=== 提取世界观描述 ===")

world_view_detail = {
    '地理': [],
    '历史': [],
    '神灵': [],
    '社会': [],
}

# 提取地名相关
locations = ['贝克兰德', '廷根', '鲁恩', '神弃之地']
for loc in locations:
    contexts = extract_context(all_content, loc, window=80)
    unique = list(set(contexts))[:10]
    world_view_detail['地理'].extend(unique)
    print(f"  {loc}: 提取 {len(unique)} 个段落")

# 提取神灵相关
gods = ['黑夜女神', '风暴之主', '永恒烈阳', '真实造物主', '愚者']
for god in gods:
    contexts = extract_context(all_content, god, window=80)
    unique = list(set(contexts))[:5]
    world_view_detail['神灵'].extend(unique)

# ============ 提取写作技巧样本 ============
print("\n=== 提取写作技巧样本 ===")

writing_samples = {
    '开头样本': [],
    '悬念样本': [],
    '战斗样本': [],
    '对话样本': [],
    '心理描写样本': [],
    '环境描写样本': [],
}

# 提取章节开头（假设以"第 X 章"开始）
chapter_starts = re.findall(r'第 [一二三四五六七八九十百千\d]+[章节][^\n]{0,200}', all_content)
writing_samples['开头样本'] = list(set(chapter_starts))[:20]

# 提取悬念结尾（"就在这时"等）
suspense_ends = extract_context(all_content, '就在这时', window=100)
writing_samples['悬念样本'] = list(set(suspense_ends))[:15]

# 提取战斗描写
battle_keywords = ['攻击', '防御', '命中', '躲避', '能力', '法术', '技能']
battle_contexts = []
for kw in battle_keywords:
    contexts = extract_context(all_content, kw, window=80)
    battle_contexts.extend(contexts)
writing_samples['战斗样本'] = list(set(battle_contexts))[:20]

# 提取对话
dialogues = re.findall(r'"([^"]{20,150})"', all_content)
writing_samples['对话样本'] = list(set(dialogues))[:30]

# 提取心理描写
psych_patterns = ['心想', '暗道', '想着', '思索', '回忆', '思考']
psych_contexts = []
for pattern in psych_patterns:
    contexts = extract_context(all_content, pattern, window=80)
    psych_contexts.extend(contexts)
writing_samples['心理描写样本'] = list(set(psych_contexts))[:20]

# 提取环境描写
env_patterns = ['阳光', '月光', '雾气', '街道', '房间', '建筑']
env_contexts = []
for pattern in env_patterns:
    contexts = extract_context(all_content, pattern, window=80)
    env_contexts.extend(contexts)
writing_samples['环境描写样本'] = list(set(env_contexts))[:20]

print(f"  提取开头样本：{len(writing_samples['开头样本'])} 个")
print(f"  提取悬念样本：{len(writing_samples['悬念样本'])} 个")
print(f"  提取战斗样本：{len(writing_samples['战斗样本'])} 个")
print(f"  提取对话样本：{len(writing_samples['对话样本'])} 个")
print(f"  提取心理描写样本：{len(writing_samples['心理描写样本'])} 个")
print(f"  提取环境描写样本：{len(writing_samples['环境描写样本'])} 个")

# ============ 保存结果 ============
print("\n=== 保存分析结果 ===")

output = {
    'total_chars': len(all_content),
    'characters': characters_detail,
    'power_system': power_system_detail,
    'world_view': world_view_detail,
    'writing_samples': writing_samples,
}

# 由于内容太多，分段保存
with open('characters_detail.json', 'w', encoding='utf-8') as f:
    json.dump({'characters': characters_detail}, f, ensure_ascii=False, indent=2)
print("  角色详情已保存到 characters_detail.json")

with open('power_system.json', 'w', encoding='utf-8') as f:
    json.dump({'power_system': power_system_detail}, f, ensure_ascii=False, indent=2)
print("  力量体系已保存到 power_system.json")

with open('world_view.json', 'w', encoding='utf-8') as f:
    json.dump({'world_view': world_view_detail}, f, ensure_ascii=False, indent=2)
print("  世界观已保存到 world_view.json")

with open('writing_samples.json', 'w', encoding='utf-8') as f:
    json.dump({'writing_samples': writing_samples}, f, ensure_ascii=False, indent=2)
print("  写作样本已保存到 writing_samples.json")

print("\n分析完成！")
