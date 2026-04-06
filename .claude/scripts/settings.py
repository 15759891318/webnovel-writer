#!/usr/bin/env python3
"""
Webnovel Writer 全局配置文件
"""

# 默认模型配置
DEFAULT_MODEL = "claude-opus-4-6"

# 模型选项
MODEL_OPTIONS = {
    "opus": "claude-opus-4-6",
    "sonnet": "claude-sonnet-4-6",
    "haiku": "claude-haiku-4-5-20251001"
}

# 其他配置项
MAX_CHAPTER_WORDS = 3000
MIN_CHAPTER_WORDS = 2000
DEFAULT_REVIEW_AGENTS = 4
