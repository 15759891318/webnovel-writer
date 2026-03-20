# -*- coding: utf-8 -*-
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
files_content = {}
for i in range(1, 12):
    with open(f'{i}.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        files_content[i] = content
        all_content += content

print(f"总字符数：{len(all_content):,}")

# 结果存储
results = {
    'total_chars': len(all_content),
    'characters': {},
    'power_system': {},
    'organizations': {},
    'world_view': {},
    'writing_techniques': {},
    'story_lines': []
}

# ============ 1. 角色名提取 ============
print("\n=== 提取角色名 ===")

# 常见人称代词和对话模式
name_patterns = [
    (r'([克利摩塞贝兰唐戴恩伊莱文霍奇纳马蒂] [a-zA-Z 音译字]{1,10})', '音译名'),
    (r'([克莱恩][\u4e00-\u9fa5·]{1,6})', '克莱恩相关'),
    (r'([莫雷蒂][\u4e00-\u9fa5]{0,4})', '莫雷蒂相关'),
    (r'([·a-zA-Z]{2,20})', '外文名'),
]

# 统计高频词
words = re.findall(r'[\u4e00-\u9fa5·]{2,6}', all_content)
word_count = Counter(words)

# 过滤常见虚词
common_words = {'的是', '到了', '在了', '着的', '了着', '一个', '这个', '那个', '什么', '怎么',
                '起来', '进去', '出来', '了的', '是有', '没有', '还有', '就是', '不是', '到了',
                '看着', '想到', '心中', '自己', '已经', '可以', '能够', '一种', '这种', '那种',
                '有着', '有着', '的一', '的人', '的地方', '的声音', '的样子', '的感觉',
                '一下', '一下', '一眼', '一身', '一脸', '一手', '一脚', '一旁', '一边',
                '一样', '一般', '一阵', '一年', '一天', '一月', '一时', '一刻', '一会',
                '都是', '都有', '所有', '所有', '一切', '一些', '一些', '一些', '一些'}

filtered_names = {k: v for k, v in word_count.items()
                  if k not in common_words and v > 50 and len(k) >= 2}

print("高频词 Top 100:")
for word, count in list(filtered_names.items())[:100]:
    print(f"  {word}: {count}")

# ============ 2. 提取可能的力量体系关键词 ============
print("\n=== 力量体系相关 ===")

power_keywords = ['序列', '途径', '魔药', '非凡', '仪式', '晋升', '扮演', '失控',
                  '占卜', '神秘', '诅咒', '献祭', '召唤', '契约', '神灵', '天使',
                  '国王', '皇帝', '学徒', '观众', '门', '占卜家', '小丑', '无面人',
                  '秘偶', '旅行', '诡秘', '奇迹', '黑皇帝']

for kw in power_keywords:
    count = all_content.count(kw)
    if count > 0:
        print(f"  {kw}: {count}")
        results['power_system'][kw] = count

# ============ 3. 提取势力组织 ============
print("\n=== 势力组织相关 ===")

org_keywords = ['教会', '协会', '组织', '家族', '学派', '教会', '教廷', '教会',
                '塔罗', '秘密', '隐秘', '黄昏', '黎明', '光明', '黑夜', '风暴',
                '雷电', '战争', '知识', '价值', '教会', '正神', '邪神', '外神',
                '玫瑰', '蔷薇', '契约', '救赎', '救赎', '福音', '圣公会']

for kw in org_keywords:
    count = all_content.count(kw)
    if count > 10:
        print(f"  {kw}: {count}")
        results['organizations'][kw] = count

# ============ 4. 提取场景和环境描写 ============
print("\n=== 场景描写关键词 ===")

scene_keywords = ['蒸汽', '机械', '工业', '现代', '古典', '维多利亚', '哥特',
                  '城堡', '庄园', '教堂', '街道', '房屋', '马车', '煤油灯',
                  '枪械', '火车', '轮船', '工厂', '烟囱', '迷雾', '黑夜']

for kw in scene_keywords:
    count = all_content.count(kw)
    if count > 0:
        print(f"  {kw}: {count}")
        results['world_view'][kw] = count

# ============ 5. 提取写作技巧相关 ============
print("\n=== 写作技巧分析 ===")

# 对话描写
dialogue_count = len(re.findall(r'"[^"]*"', all_content))
print(f"  对话引号数：{dialogue_count}")

# 心理描写
psych_count = len(re.findall(r'心想 | 心中 | 暗道 | 思索 | 思考 | 回忆 | 想起', all_content))
print(f"  心理描写数：{psych_count}")

# 动作描写
action_count = len(re.findall(r'站起 | 坐下 | 站起 | 走过 | 跑 | 跳 | 转 | '
                              '拿 | 取 | 放 | 看 | 望 | 瞧 | 听 | 闻 | 摸 | 触', all_content))
print(f"  动作描写数：{action_count}")

# 环境描写
env_count = len(re.findall(r'天空 | 阳光 | 月光 | 星光 | 风 | 雨 | 雪 | 雾 | 云', all_content))
print(f"  环境描写数：{env_count}")

results['writing_techniques'] = {
    'dialogue_count': dialogue_count,
    'psych_count': psych_count,
    'action_count': action_count,
    'env_count': env_count
}

# ============ 6. 章节结构分析 ============
print("\n=== 章节结构 ===")

# 检测章节标题
chapter_patterns = [
    r'第 [一二三四五六七八九十百千 0-9]+章',
    r'第 [一二三四五六七八九十百千 0-9]+节',
    r'Chapter\s*\d+',
]

chapters = []
for pattern in chapter_patterns:
    matches = re.findall(pattern, all_content)
    if matches:
        chapters.extend(matches)
        print(f"  Pattern {pattern}: {len(matches)} chapters")

# 去重
unique_chapters = list(set(chapters))
print(f"  总章节数（估算）: {len(unique_chapters)}")

# 保存结果
with open('analysis_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n分析结果已保存到 analysis_results.json")

# ============ 7. 详细文本采样 ============
print("\n=== 文本采样 ===")

# 采样包含角色名的句子
sample_sentences = []
patterns_to_find = ['克莱恩', '莫雷蒂', '周明瑞', '梅林', '夏洛克', '格尔曼',
                    '愚者', '世界', '魔术师', '正义', '倒吊人', '太阳', '月亮',
                    '隐者', '星星', '审判', '正义', '佛尔思', '休', '阿尔杰',
                    '奥黛丽', '戴里克', '埃姆林', '嘉德丽雅', '阿兹克', '蕾妮特',
                    '阿蒙', '亚当', '真实造物主', '暗天使', '救赎天使']

for pattern in patterns_to_find:
    if pattern in all_content:
        count = all_content.count(pattern)
        print(f"  {pattern}: 出现 {count} 次")
        # 采样一个出现的上下文
        idx = all_content.find(pattern)
        if idx > 0:
            start = max(0, idx - 30)
            end = min(len(all_content), idx + len(pattern) + 30)
            sample = all_content[start:end].replace('\n', ' ')
            sample_sentences.append({'name': pattern, 'sample': sample})

# 保存采样
with open('text_samples.json', 'w', encoding='utf-8') as f:
    json.dump(sample_sentences, f, ensure_ascii=False, indent=2)

print("\n文本采样已保存到 text_samples.json")
print("\n分析完成！")
