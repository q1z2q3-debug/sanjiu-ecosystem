# -*- coding: utf-8 -*-
"""sanjiu-bridge 认知原语包 · 三元九维 19683 认知引擎。

对外统一导出：认知坐标服务（encode/search/transform）+ 语义桥（五域 + 深度象义）
+ 邻域泛化（generalize）+ 增强接口（enhance）。
任一 Agent / 脚本可通过本包调用"写进 19683 坐标 → 定位 → 多语言解读 → 泛化推理"。
"""
from .bridge import (  # noqa: F401
    encode, search, transform, render, bridge, bridge_by_idx, bridge_by_text,
    fingerprint, deep_oracle, LEXICON, DOMAINS,
)
from .generalize import generalize, synthesize  # noqa: F401
from .enhance import enhance  # noqa: F401

__version__ = "0.2.0"
__all__ = [
    "encode", "search", "transform", "render", "bridge", "bridge_by_idx",
    "bridge_by_text", "fingerprint", "deep_oracle", "LEXICON", "DOMAINS",
    "generalize", "synthesize", "enhance",
]
