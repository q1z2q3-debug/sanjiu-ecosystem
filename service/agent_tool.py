# -*- coding: utf-8 -*-
"""agent_tool.py · 认知原语接入 Agent 运行时。

把语义桥封装成 Agent 可挂载的"工具函数注册表"（name / callable / desc / params）。
宿主 Agent 运行时按名字调用即可 —— 这是"Agent 认知层"的工程落点：
  Agent 决策前，调 sanjiu.decide 把处境写进 19683 坐标，取结构化认知参考，
  再结合业务判断给出最终决策（桥是认知辅助，不替代人/业务）。

decide 全链路：encode(可注入 LLM 向量) → 定位最近邻卦 → 五域解读 → 深度卦典
→ 结构倾向 → 行动建议。纯符号可跑，LLM 可注入增强。
"""
from __future__ import annotations

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bridge import encode, search, bridge_by_idx, fingerprint, DOMAINS  # noqa: E402
from llm_mix import run as llm_run  # noqa: E402


def _action_advice(fp, deep):
    """从结构倾向 + 卦典启示给行动建议（确定性模板）。"""
    t = fp["tendency"]
    if "显·进" in t:
        act = "宜乘势主动推进，把握当机；同时控住节奏防过亢。"
    elif "隐·守" in t:
        act = "宜收敛守正、蓄力待时，止损聚气，勿逆势强攻。"
    elif "枢·待" in t:
        act = "宜静观权衡、谋定后动，机在枢纽未熟，勿躁进。"
    elif "偏显" in t:
        act = "宜缓进勿躁，边进边察，留有余地。"
    elif "偏隐" in t:
        act = "宜蓄力渐进，守中待变，勿轻启强争。"
    else:
        act = "宜居中权衡，持衡而进。"
    return f"{act}（卦鉴：{deep['ming']}·{deep['qi']}）"


def decide(text: str, top_n: int = 3, vector=None, reason=None):
    """全链路认知决策辅助（Agent 主入口）。

    返回结构化结果：处境/向量/编码通道/最近邻卦/结构倾向/五域/卦典/行动建议。
    """
    r = llm_run(text, vector=vector, reason=reason, top_n=top_n)
    top = r["items"][0]
    fp = top["fingerprint"]
    deep = top["deep"]
    advice = _action_advice(fp, deep)
    return {
        "text": text, "vec": r["vec"], "encode_channel": r["encode_channel"],
        "reason": r["reason"],
        "location": {"idx": top["idx"], "gua": top["gua"],
                     "ming": deep["ming"], "tendency": fp["tendency"],
                     "tension": fp["tension"]},
        "domains": top["domains"], "oracle": deep,
        "advice": advice,
        "neighbors": [f"{i['idx']} {i['deep']['ming']}" for i in r["items"]],
    }


# 工具注册表（Agent 运行时按名调用）
TOOLS = {
    "sanjiu.encode": {"desc": "自然语言状态→9维向量(19683坐标)", "fn": encode},
    "sanjiu.search": {"desc": "向量→Top-N最近邻卦", "fn": search},
    "sanjiu.bridge": {"desc": "编号→五域解读+深度卦典", "fn": bridge_by_idx},
    "sanjiu.fingerprint": {"desc": "卦→结构倾向", "fn": fingerprint},
    "sanjiu.decide": {"desc": "全链路认知决策辅助(定位+五域+卦典+行动建议)",
                      "fn": decide},
    "sanjiu.domains": {"desc": "五域清单", "fn": lambda: list(DOMAINS)},
}


def agent_call(tool: str, *args, **kwargs):
    """Agent 运行时统一调用入口：按工具名调用。"""
    if tool not in TOOLS:
        raise KeyError(f"未知认知原语 {tool}；可选 {list(TOOLS)}")
    return TOOLS[tool]["fn"](*args, **kwargs)


if __name__ == "__main__":
    print("认知原语工具注册表：")
    for name, t in TOOLS.items():
        print(f"  {name} — {t['desc']}")
    print("\nAgent 决策示范（用 sanjiu.decide）：")
    r = agent_call("sanjiu.decide",
                   "认知引擎与治理均已就绪，生态下一阶段应偏产品落地还是继续扩张接入")
    print(f"处境: {r['text']}")
    print(f"编码: {r['vec']} ({r['encode_channel']})")
    print(f"定位: 卦{r['location']['idx']} {r['location']['ming']} | {r['location']['tendency']} | {r['location']['tension']}")
    print(f"卦典: {r['oracle']['ming']} — {r['oracle']['qi']}")
    print(f"行动建议: {r['advice']}")
