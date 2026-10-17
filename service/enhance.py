# -*- coding: utf-8 -*-
"""增强接口（enhance）：符号给骨架，LLM 填自然语言。

默认（无 llm_fn）走纯符号管线：encode → search → bridge(五域 + 深度象义)。
宿主可注入 `llm_fn(skeleton) -> str`，把符号骨架交给 LLM 生成自然语言泛化结论 ——
这是"回归正轨人类语言体系"与 LLM 混合的落点，符号层不依赖外部 API 也能跑。
"""
from __future__ import annotations

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bridge import encode, search, bridge_by_idx, deep_oracle  # noqa: E402


def _skeleton(text: str, top_n: int = 1) -> dict:
    """纯符号骨架：向量 + 最近邻卦 + 深度象义 + 五域摘要。"""
    vec = encode(text)
    hits = search(vec, top_n=top_n)
    items = []
    for h in hits:
        b = bridge_by_idx(h["idx"])
        items.append({
            "dist": h["dist"], "idx": h["idx"], "gua": h["gua"],
            "fingerprint": b["fingerprint"], "deep": b["deep"],
            "domains": {d: b["domains"][d]["text"] for d in b["domains"]},
        })
    return {"text": text, "vec": vec, "top_n": top_n, "items": items}


def _symbol_summary(sk: dict) -> str:
    """默认符号化泛化结论（确定性拼接，无 LLM）。"""
    top = sk["items"][0]
    fp = top["fingerprint"]
    deep = top["deep"]
    return (f"符号判读：' {sk['text']} ' 写进 19683 坐标 → 向量 {sk['vec']}，"
            f"最近邻卦 {top['idx']}（{deep['ming']}，{fp['tendency']}）。"
            f"启示：{deep['qi']}。")


def enhance(text: str, top_n: int = 1, llm_fn=None):
    """认知原语增强。返回 {skeleton, summary}。

    llm_fn 可选：注入 `llm_fn(skeleton) -> str` 生成自然语言结论；
    未注入时用默认符号化总结。
    """
    sk = _skeleton(text, top_n=top_n)
    if llm_fn is not None:
        summary = llm_fn(sk)
    else:
        summary = _symbol_summary(sk)
    return {"skeleton": sk, "summary": summary}


if __name__ == "__main__":
    for t in ("产品成熟，市场向好，宜大力投放", "行情震荡，多空争夺，宜观望避险"):
        r = enhance(t)
        print("■", t)
        print("  →", r["summary"])
        print("  最近邻:", [f"{i['idx']} {i['deep']['ming']}" for i in r["skeleton"]["items"]])
