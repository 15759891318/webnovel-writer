# -*- coding: utf-8 -*-
"""
诡秘之主详细分析脚本
分析角色、力量体系、势力、写作技巧等
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

# ============ 角色详细分析 ============
print("\n" + "="*60)
print("一、角色信息详细分析")
print("="*60)

# 主要角色列表（基于诡秘之主原著）
main_characters = {
    '克莱恩': '主角，穿越者，原名周明瑞',
    '周明瑞': '主角前世名字',
    '莫雷蒂': '克莱恩穿越后的姓氏',
    '愚者': '克莱恩在塔罗会的身份',
    '格尔曼': '克莱恩的马甲之一，冒险家形象',
    '夏洛克': '克莱恩的马甲之一，侦探形象',
    '梅林': '克莱恩的马甲之一，流浪法师形象',
    '奥黛丽': '正义小姐，观众途径，贵族少女',
    '阿尔杰': '倒吊人，水手途径，教会人员',
    '佛尔思': '魔术师，作家，门途径',
    '休': '审判，律师，仲裁人途径',
    '戴里克': '太阳，阅读者途径，来自神弃之地',
    '埃姆林': '月亮，药师途径，血族',
    '嘉德丽雅': '隐者，隐者途径',
    '阿兹克': '死灵导师，克莱恩的老师',
    '阿蒙': '反派，时天使，错误途径',
    '亚当': '心理炼金会会长，观众途径',
}

# 统计角色出现频率
print("\n【主要角色出现频率】")
char_freq = {}
for name in main_characters.keys():
    count = all_content.count(name)
    char_freq[name] = count
    print(f"  {name}: {count} 次")

# 排序
sorted_chars = sorted(char_freq.items(), key=lambda x: x[1], reverse=True)
print("\n【角色热度排名】")
for i, (name, count) in enumerate(sorted_chars[:15], 1):
    desc = main_characters.get(name, '')
    print(f"  {i}. {name}: {count} 次 - {desc}")

# ============ 序列途径分析 ============
print("\n" + "="*60)
print("二、力量体系 - 序列途径")
print("="*60)

# 22 条神之途径（基于原著）
sequences_keywords = {
    # 黑皇帝途径
    '黑皇帝': ['黑皇帝', '审判官', '仲裁人', '掌刑人', '律师'],
    # 白皇帝途径
    '白皇帝': ['白皇帝', '暴君', '灾难主祭', '海王', '天灾'],
    # 红祭司途径
    '红祭司': ['红祭司', '征服者', '巫师', '冰霜'],
    # 夜之途径（黑夜女神）
    '黑夜': ['黑夜', '安眠', '收尸人', '掘墓人', '看门人', '无光'],
    # 黑暗途径
    '黑暗': ['黑暗', '午夜', '厄运'],
    # 战士途径
    '战士': ['战神', '黎明', '战士', '格斗家', '黎明骑士'],
    # 蒸汽途径
    '蒸汽': ['蒸汽', '机械', '工匠'],
    # 太阳途径
    '太阳': ['太阳', '光明', '赞美诗', '牧首'],
    # 白塔途径
    '白塔': ['白塔', '知识', '智者'],
    # 愚者途径
    '愚者': ['愚者', '占卜家', '小丑', '无面人', '秘偶大师', '诡法师'],
    # 门途径
    '门': ['门', '学徒', '戏法大师', '占星人', '记录官', '旅行家', '秘法师'],
    # 错误途径
    '错误': ['错误', '偷盗者', '诈骗师', '解密学者', '时天使'],
    # 观众途径
    '观众': ['观众', '读心者', '心理医生', '操纵师'],
    # 水手途径
    '水手': ['水手', '暴怒', '灾祸'],
    # 阅读者途径
    '阅读者': ['阅读者', '理解', '诠释'],
    # 药师途径
    '药师': ['药师', '驯兽师', '医生'],
    # 猎人途径
    '猎人': ['猎人', '陷阱师', '挑衅者'],
    # 刺客途径
    '刺客': ['刺客', '教唆者', '女巫'],
    # 耕种者途径
    '耕种者': ['耕种者', '医师', '丰收'],
    # 仲裁人途径
    '仲裁人': ['仲裁人', '治安官', '审判'],
    # 隐者途径
    '隐者': ['隐者', '星象师', '占卜'],
    # 律师途径
    '律师': ['律师', '法则', '秩序'],
}

print("\n【序列途径关键词统计】")
seq_counts = {}
for seq, keywords in sequences_keywords.items():
    total = sum(all_content.count(kw) for kw in keywords)
    seq_counts[seq] = total
    print(f"  {seq}途径: {total} 次 (关键词：{', '.join(keywords[:3])}...)")

# 排序
sorted_seqs = sorted(seq_counts.items(), key=lambda x: x[1], reverse=True)
print("\n【途径热度排名】")
for i, (seq, count) in enumerate(sorted_seqs[:10], 1):
    print(f"  {i}. {seq}途径：{count} 次")

# ============ 魔药与晋升体系 ============
print("\n" + "="*60)
print("三、魔药与晋升体系")
print("="*60)

# 核心概念
core_concepts = {
    '魔药': '服用魔药获得非凡能力',
    '消化': '通过扮演消化魔药',
    '扮演': '按照魔药名称扮演来消化',
    '仪式': '晋升需要的仪式',
    '失控': '无法控制非凡特性',
    '疯批': '精神失控的状态',
    '特性': '非凡特性不灭定律',
    '聚合': '非凡特性聚合定律',
}

print("\n【核心概念出现频率】")
concept_counts = {}
for concept, desc in core_concepts.items():
    count = all_content.count(concept)
    concept_counts[concept] = count
    print(f"  {concept}: {count} 次 - {desc}")

# ============ 势力组织分析 ============
print("\n" + "="*60)
print("四、势力组织")
print("="*60)

organizations = {
    '塔罗会': '主角创建的神秘组织',
    '黑夜教会': '黑夜女神的教会',
    '风暴教会': '风暴之主的教会',
    '蒸汽教会': '蒸汽与机械之神的教会',
    '太阳教会': '永恒烈阳的教会',
    '战神教会': '战神的教会',
    '知识教会': '知识与智慧之神的教会',
    '大地教会': '大地母神的教会',
    '玫瑰学派': '堕落邪教组织',
    '心理炼金会': '亚当创建的组织',
    '极光会': '崇拜真实造物主的组织',
    '灵知会': '神秘组织',
    '命运隐士会': '隐者途径组织',
    '值夜者': '黑夜教会的非凡者部队',
    '代罚者': '风暴教会的非凡者部队',
    '机械之心': '蒸汽教会的非凡者部队',
}

print("\n【组织势力统计】")
org_counts = {}
for org, desc in organizations.items():
    count = all_content.count(org)
    org_counts[org] = count
    print(f"  {org}: {count} 次 - {desc}")

# ============ 世界观要素 ============
print("\n" + "="*60)
print("五、世界观要素")
print("="*60)

world_elements = {
    '鲁恩': '鲁恩王国，主要舞台',
    '廷根': '故事开始的城市',
    '贝克兰德': '鲁恩王国首都',
    '费内波特': '费内波特帝国',
    '弗萨克': '弗萨克帝国',
    '因蒂斯': '因蒂斯共和国',
    '伟大之红': '环绕大陆的血海',
    '神弃之地': '被神灵遗弃的地方',
    '源堡': '源质之一，诡秘之主的核心',
    '旧日': '外神，旧日支配者',
    '真神': '真正的神明',
    '天使': '神话生物',
    '圣者': '半神级别的强者',
}

print("\n【世界观要素统计】")
world_counts = {}
for element, desc in world_elements.items():
    count = all_content.count(element)
    world_counts[element] = count
    print(f"  {element}: {count} 次 - {desc}")

# ============ 写作技巧分析 ============
print("\n" + "="*60)
print("六、写作技巧分析")
print("="*60)

# 1. 悬念设置
suspense_patterns = [
    r'然而',
    r'就在这时',
    r'就在这个时候',
    r'突然',
    r'忽然',
    r'出乎意料',
    r'谁也没有想到',
    r'意想不到',
]

print("\n【悬念设置】")
suspense_count = {}
for pattern in suspense_patterns:
    count = all_content.count(pattern)
    suspense_count[pattern] = count
    print(f"  '{pattern}': {count} 次")

# 2. 情感描写
emotion_patterns = [
    '心中', '心想', '暗道', '忍不住', '深吸一口气',
    '吐了口气', '沉默', '凝视', '注视', '目光',
]

print("\n【情感/心理描写】")
emotion_count = {}
for pattern in emotion_patterns:
    count = all_content.count(pattern)
    emotion_count[pattern] = count
    print(f"  '{pattern}': {count} 次")

# 3. 场景描写
scene_patterns = [
    '阳光', '月光', '星光', '灯火', '阴影',
    '雾气', '雨水', '雪花', '微风', '空气中',
]

print("\n【场景/环境描写】")
scene_count = {}
for pattern in scene_patterns:
    count = all_content.count(pattern)
    scene_count[pattern] = count
    print(f"  '{pattern}': {count} 次")

# 4. 对话风格
dialogue_tags = ['说道', '问道', '回答道', '笑道', '沉声道', '轻声道']
print("\n【对话标识词】")
for tag in dialogue_tags:
    count = all_content.count(tag)
    print(f"  '{tag}': {count} 次")

# ============ 爽点/高潮分析 ============
print("\n" + "="*60)
print("七、爽点/高潮场景分析")
print("="*60)

climax_keywords = {
    '爆发': '力量爆发',
    '碾压': '实力碾压',
    '秒杀': '瞬间击败',
    '反转': '局势反转',
    '底牌': '亮出底牌',
    '震惊': '他人震惊',
    '恐惧': '敌人恐惧',
    '无敌': '无敌姿态',
    '掌控': '掌控全局',
    '算计': '智谋算计',
}

print("\n【爽点关键词】")
climax_counts = {}
for kw, desc in climax_keywords.items():
    count = all_content.count(kw)
    climax_counts[kw] = count
    print(f"  {kw}: {count} 次 - {desc}")

# ============ 金句/名场面分析 ============
print("\n" + "="*60)
print("八、金句/名场面分析")
print("="*60)

# 搜索可能的名言模式
famous_patterns = [
    r'"[^"]*"[。!！]',  # 引号内的话
    r'——[^"\n]+',  # 破折号后的话
]

# 采样一些引号内容
quotes = re.findall(r'"([^"]{10,50})"', all_content)
if quotes:
    print("\n【经典台词采样】")
    # 按出现频率统计
    quote_freq = Counter(quotes)
    for quote, count in quote_freq.most_common(20):
        # 过滤太短的
        if len(quote) > 15:
            print(f"  \"{quote}\" - {count} 次")

# ============ 综合分析输出 ============
print("\n" + "="*60)
print("九、综合分析")
print("="*60)

# 题材分析
print("\n【题材类型】")
print("  主题材：西方奇幻 + 克苏鲁神话 + 蒸汽朋克")
print("  副题材：悬疑推理 + 群像剧 + 升级流")
print("  风格标签：黑暗向、智斗、世界观宏大、设定严谨")

# 可借鉴元素
print("\n【可借鉴元素】")
print("  1. 塔罗会 - 神秘组织开会形式")
print("  2. 序列体系 - 清晰的力量等级")
print("  3. 扮演法 - 消化魔药的核心方法")
print("  4. 多马甲流 - 主角多个身份")
print("  5. 群像描写 - 多个配角有独立故事线")
print("  6. 世界观层层揭开 - 不一次性倒出设定")
print("  7. 反派智商在线 - 不是无脑反派")
print("  8. 伏笔回收 - 前面埋的后面会收")

# 文笔特色
print("\n【文笔特色】")
print("  1. 细节描写丰富 - 场景、动作、心理")
print("  2. 对话符合身份 - 不同角色说话风格不同")
print("  3. 节奏把控好 - 张弛有度")
print("  4. 悬念设置巧妙 - 章末留钩子")
print("  5. 情感真挚 - 不尬不煽情")

# 保存完整分析结果
analysis_result = {
    'total_chars': len(all_content),
    'characters': {
        'main': main_characters,
        'frequency': char_freq,
    },
    'power_system': {
        'sequences': sequences_keywords,
        'concepts': core_concepts,
    },
    'organizations': organizations,
    'world_view': world_elements,
    'writing_techniques': {
        'suspense': suspense_count,
        'emotion': emotion_count,
        'scene': scene_count,
        'dialogue': {tag: all_content.count(tag) for tag in dialogue_tags},
    },
    'climax': climax_keywords,
}

with open('detailed_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(analysis_result, f, ensure_ascii=False, indent=2)

print("\n详细分析结果已保存到 detailed_analysis.json")
print("\n分析完成！")
