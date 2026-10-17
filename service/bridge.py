# -*- coding: utf-8 -*-
"""三元九维 19683 · 认知坐标服务 + 语义桥（MVP）。

设计原则（沿「形式统一 + 语义自适配」）：
- sanjiu-core 只提供与领域无关的数学底座（索引/算子/距离），本模块不修改它。
- 语义桥 = 同一编号卦，在各已适配领域（D/R/T · 体用变 · 洛书九宫）各自"从卦象义长出来"的确定性解读。
  各域先用自身 manifest 的 bit_weight_map 把 core 规范向量映射到域内维序，再用域规则生成解读。
- 结构倾向（进/守/待/变/衡/张力）从 core 向量直接算出，跨域共享 —— 这是"同一坐标、多语言说同一件事"的可量化锚点。

公理锁定；本模块只做映射层创作与检索，不改数理。
"""
from __future__ import annotations

import os
import sys
import math
import json

_HERE = os.path.dirname(os.path.abspath(__file__))
_CORE = os.path.normpath(os.path.join(_HERE, "..", "..", "sanjiu-core"))
_TRIG = os.path.normpath(os.path.join(_HERE, "..", "..", "trigram"))
for p in (_CORE, _TRIG):
    if p not in sys.path:
        sys.path.insert(0, p)

from sanjiu_core import (  # noqa: E402
    idx_to_g, g_to_idx, F_C, F_Z, F_CZ, F_H, F_B_multi, N,
)

# ======================================================================
# 台阶一 · 认知坐标服务原语
# ======================================================================

# 自然语言→9维向量词表（对应 core 规范 g1..g9，上→下）
# 每维 ((正词,权重)...), ((负词,权重)...)：加权语义打分，多命中累加。
# 语义分辨率受限（纯符号词表），是 encode 环节已知限制；enhance 接口可注入 LLM。
LEXICON = [
    ((("显", 1.5), ("达成", 1.5), ("上位", 1.2), ("向外", 1.2), ("盛", 1.5), ("成熟", 1.3), ("明达", 1.3)),
     (("隐", 1.5), ("潜藏", 1.3), ("退", 1.2), ("收敛", 1.2), ("衰", 1.5), ("暗晦", 1.3))),
    ((("生发", 1.5), ("增益", 1.5), ("主导", 1.2), ("动", 0.8), ("扩张", 1.5), ("增长", 1.3), ("推进", 1.2)),
     (("减损", 1.5), ("被动", 1.3), ("静", 0.9), ("亏损", 1.5), ("消耗", 1.2))),
    ((("居间", 1.3), ("耦合", 1.3), ("过渡", 1.2), ("中", 0.5), ("协调", 1.3), ("均衡", 1.3)),
     (("偏", 1.2), ("极端", 1.3), ("失衡", 1.5), ("震荡", 1.4), ("争夺", 1.4))),
    ((("主动", 1.4), ("进", 0.8), ("张", 1.2), ("攻", 1.3), ("投放", 1.4), ("出击", 1.4)),
     (("缩", 1.3), ("雌", 1.2), ("守", 1.0), ("退", 1.2), ("观望", 1.3), ("避险", 1.4))),
    ((("势能", 1.4), ("平衡", 1.2), ("稳", 1.0), ("蓄", 1.3), ("稳固", 1.4), ("积淀", 1.3), ("耐心", 1.2)),
     (("不稳", 1.4), ("倾", 1.3), ("泄", 1.3), ("剧烈", 1.5), ("单薄", 1.4), ("冒进", 1.4))),
    ((("生", 1.2), ("长", 1.2), ("升", 1.3), ("阳", 1.2), ("向好", 1.5), ("上升", 1.4)),
     (("衰", 1.5), ("降", 1.3), ("阴", 1.2), ("疲劳", 1.4), ("亏", 1.3))),
    ((("通", 1.3), ("交", 1.2), ("联", 1.3), ("化", 0.8), ("协调", 1.3), ("人心", 1.4), ("和解", 1.4)),
     (("隔", 1.4), ("滞", 1.4), ("塞", 1.4), ("争执", 1.5), ("不齐", 1.4), ("决裂", 1.5))),
    ((("明", 1.4), ("显于外", 1.3), ("成", 1.0), ("盈利", 1.4), ("达成", 1.3)),
     (("晦", 1.4), ("藏于内", 1.3), ("败", 1.4), ("未成", 1.2))),
    ((("下位", 1.3), ("根基", 1.4), ("本", 1.0), ("内", 0.6), ("实", 1.2), ("积累", 1.3), ("沉淀", 1.3)),
     (("末", 1.2), ("枝", 1.2), ("外", 0.8), ("虚", 1.2), ("单薄", 1.4))),
]


def encode(text: str, lexicon=None, threshold: float = 0.2) -> tuple:
    """自然语言状态 → 9 维向量（加权语义打分，core 规范）。

    每维 score = Σ正词权重 − Σ负词权重；score > threshold → +1，
    score < -threshold → -1，否则 → 0（默认对称阈值 0.2）。
    """
    lex = lexicon or LEXICON
    vec = []
    for pos, neg in lex[:9]:
        s = sum(w for kw, w in pos if kw in text) - sum(w for kw, w in neg if kw in text)
        if s > threshold:
            vec.append(1)
        elif s < -threshold:
            vec.append(-1)
        else:
            vec.append(0)
    return tuple(vec)


def search(vec, top_n: int = 5):
    """给定 9 维向量 → 欧氏距离 Top-N 邻近卦（全套变换推演）。"""
    full = [idx_to_g(i) for i in range(N)]
    dists = []
    for i, g in enumerate(full):
        d = math.sqrt(sum((a - b) ** 2 for a, b in zip(g, vec)))
        dists.append((d, i, g))
    dists.sort(key=lambda x: (x[0], x[1]))
    out = []
    for d, i, g in dists[:top_n]:
        out.append({
            "idx": i, "dist": round(d, 4), "gua": g,
            "F_C": F_C(g), "F_Z": F_Z(g), "F_CZ": F_CZ(g), "F_H": F_H(g),
        })
    return out


def transform(g):
    """全套结构变换：错/综/错综/互（5维内核）+ 逐爻动变。"""
    return {
        "错卦 F_C": F_C(g), "综卦 F_Z": F_Z(g), "错综 F_CZ": F_CZ(g),
        "互卦 F_H(5维)": F_H(g),
        "变卦": {p + 1: F_B_multi(g, [p]) for p in range(9)},
    }


# ======================================================================
# 台阶二 · 结构倾向（跨域共享锚点）
# ======================================================================

def fingerprint(g):
    """跨域结构指纹：阳性/阴性/中性计数 + 倾向标签 + 张力。"""
    pos = sum(1 for x in g if x > 0)
    neg = sum(1 for x in g if x < 0)
    zero = 9 - pos - neg
    bal = pos - neg
    en = pos + neg
    if zero >= 5:
        tend = "枢·待（中性维多，处于枢纽/过渡，宜静观）"
    elif bal >= 3 and en >= 6:
        tend = "显·进（阳气盛而贯通，宜主动推进）"
    elif bal <= -3 and en >= 6:
        tend = "隐·守（阴气盛而收敛，宜守正待时）"
    elif bal >= 1:
        tend = "偏显·渐（阳气略胜，可缓进勿躁）"
    elif bal <= -1:
        tend = "偏隐·渐守（阴气略胜，宜蓄力勿进）"
    else:
        tend = "衡·中（阴阳相持，宜居中权衡）"
    tension = "张力高（阴阳并争）" if (pos >= 3 and neg >= 3) else "张力低（势单一致）"
    return {
        "pos": pos, "neg": neg, "zero": zero,
        "balance": bal, "energy": en, "tendency": tend, "tension": tension,
    }


# ======================================================================
# 深度象义（主仓人类卦典，按 idx 查，19683 全）——核心假设的深度层
# ======================================================================
_HUMAN_JSON = os.path.normpath(os.path.join(_HERE, "..", "..", "trigram",
                                            "sanjiu_quanji_human.json"))
_human = None


def _load_human():
    global _human
    if _human is None:
        _human = json.load(open(_HUMAN_JSON, encoding="utf-8"))
    return _human


def deep_oracle(idx: int):
    """按编号查主仓人类卦典深度象义：卦名/卦辞/白话/启示。"""
    try:
        d = _load_human().get(str(idx))
        if not d:
            return None
        return {k: d.get(k) for k in ("ming", "guan", "su", "qi", "yinyang", "drt")}
    except Exception:
        return None


# ======================================================================
# 台阶二 · 语义桥：三域规则（manifest 位权映射 + 各域语义）
# ======================================================================

# 各域：dims=域内 9 维名（序=manifest bit_weight_map 映射后的域内序）；bit_weight_map；trit 语义
DOMAINS = {}

# --- 域 A · D/R/T（主仓 sanjiu-nine，位权恒等：core g1..g9 即 D/R/T 上→下）---
DOMAINS["D/R/T"] = {
    "bit_weight": [0, 1, 2, 3, 4, 5, 6, 7, 8],
    "dims": ["承载", "审定", "增益", "承载", "审定", "增益", "承载", "审定", "增益"],
    "trit": {"-1": "亏/隐", "0": "衡/待", "+1": "盈/显"},
    "render": lambda v: _render_drt(v),
}

# --- 域 B · 体用变（cog-layer / heal-belief，位权反向：域内位0=体=最低位=core g9）---
DOMAINS["体用变"] = {
    "bit_weight": [8, 7, 6, 5, 4, 3, 2, 1, 0],
    "dims": ["体", "用", "变", "时", "空", "势", "因", "果", "缘"],
    "trit": {"-1": "不足", "0": "中和", "+1": "充盈"},
    "render": lambda v: _render_tiyong(v),
}

# --- 域 C · 洛书九宫（meihua，位权恒等：core g1=坎最高…g9=离最低）---
DOMAINS["洛书九宫"] = {
    "bit_weight": [0, 1, 2, 3, 4, 5, 6, 7, 8],
    "dims": ["坎水", "坤土", "震木", "巽木", "中土", "乾金", "兑金", "艮土", "离火"],
    "trit": {"-1": "气敛", "0": "气枢", "+1": "气旺"},
    "render": lambda v: _render_luoshu(v),
}

# --- 域 D · 小六壬（xiuqiankun，位权恒等：core 即认知 9 维）---
DOMAINS["小六壬"] = {
    "bit_weight": [0, 1, 2, 3, 4, 5, 6, 7, 8],
    "dims": ["本心", "敏感度", "动力", "走向", "势能", "行动力", "连接感", "明暗", "根基"],
    "trit": {"-1": "敛", "0": "衡", "+1": "发"},
    "render": lambda v: _render_liuren(v),
}

# --- 域 E · 疗愈（heal-belief，位权反向：域内位0=体=core g9）---
DOMAINS["疗愈"] = {
    "bit_weight": [8, 7, 6, 5, 4, 3, 2, 1, 0],
    "dims": ["体", "用", "变", "时", "空", "势", "因", "果", "缘"],
    "trit": {"-1": "隐收", "0": "衡中", "+1": "显发"},
    "render": lambda v: _render_heal(v),
}


def _map_to_domain(g, dom):
    """core 规范向量 → 域内向量（按 manifest 位权）。"""
    bw = DOMAINS[dom]["bit_weight"]
    out = [0] * 9
    for i, j in enumerate(bw):       # core g[j] → 域内维 i
        out[i] = g[j]
    return tuple(out)


def _to_core_from_domain(v, dom):
    bw = DOMAINS[dom]["bit_weight"]
    out = [0] * 9
    for i, j in enumerate(bw):
        out[j] = v[i]
    return tuple(out)


def _render_drt(v):
    """D/R/T：以承载/审定/增益三组×上中下判强弱明晦（五档）。"""
    def _level(grp):
        s = sum(grp)
        if s >= 2:
            return "盈·强", "明·彻", "丰·足"
        if s == 1:
            return "略盈·可任", "略明·可察", "略增·有余"
        if s == 0:
            return "中平·堪任", "持衡·可判", "平允·相称"
        if s == -1:
            return "略亏·吃力", "略晦·欠察", "略耗·见绌"
        return "亏·难任", "晦·难判", "耗·虚损"
    c_s, j_s, g_s = (_level(g)[i] for i, g in enumerate(
        [(v[0], v[3], v[6]), (v[1], v[4], v[7]), (v[2], v[5], v[8])]))
    return f"承载{c_s}；审定{j_s}；增益{g_s}。"


def _render_tiyong(v):
    """体用变时空势因果缘：体用为纲，变时势为机，因果缘为链。"""
    ti, yong, bian = v[0], v[1], v[2]
    shi, kong, shi2 = v[3], v[4], v[5]
    yin, guo, yuan = v[6], v[7], v[8]
    ti_s = {1: "体充盈，根基厚实", 0: "体中平，根基稳当", -1: "体不足，根基薄弱"}[ti]
    yong_s = {1: "用有盈，施为得力", 0: "用中和，施为平实", -1: "用虚耗，施为乏力"}[yong]
    bian_s = {1: "变机已现，转捩在即", 0: "变候待发，机尚在伏", -1: "变机闭塞，转折难成"}[bian]
    shi_s = {1: "时势顺遂", 0: "时势平缓", -1: "时势逆阻"}[shi]
    yuan_s = {1: "外缘聚拢，得助可期", 0: "外缘平正，援而不强", -1: "外缘散逸，多靠自立"}[yuan]
    return f"{ti_s}；{yong_s}；{bian_s}；{shi_s}；{yuan_s}。"


def _render_luoshu(v):
    """洛书九宫：坎坤震巽中乾兑艮离，宫气旺衰 + 中宫枢纽。"""
    wang = [d for d, x in zip(DOMAINS["洛书九宫"]["dims"], v) if x > 0]
    lian = [d for d, x in zip(DOMAINS["洛书九宫"]["dims"], v) if x < 0]
    hub = v[4]  # 中土
    hub_s = {1: "中宫气旺，枢纽当行", 0: "中宫气枢，主权衡待定", -1: "中宫气敛，枢纽沉寂"}[hub]
    wang_s = ("气旺之宫：" + "、".join(wang) + "；") if wang else "无气旺之宫；"
    lian_s = ("气敛之宫：" + "、".join(lian) + "。") if lian else "无气敛之宫。"
    return f"{hub_s}；{wang_s}{lian_s}"


def _xialiuren_phase(v):
    """小六壬相位：从 9 维三态算（同 xiuqiankun cogPhase）。"""
    pos = sum(1 for x in v if x > 0)
    neg = sum(1 for x in v if x < 0)
    zero = 9 - pos - neg
    if zero > 6:
        return "悬置"
    if pos > 5 and neg < 2:
        return "太阳"
    if neg > 5 and pos < 2:
        return "太阴"
    if 3 <= pos <= 5 and neg < 3:
        return "少阳"
    if 3 <= neg <= 5 and pos < 3:
        return "少阴"
    if pos < 3 and neg < 3 and zero > 5:
        return "平衡"
    return "参差"


def _render_liuren(v):
    """小六壬：相位 → 六宫判读 + 关键维度。"""
    ph = _xialiuren_phase(v)
    gong = {
        "太阳": "速喜·吉快", "少阳": "小吉·和合", "太阴": "空亡·虚耗",
        "少阴": "留连·缓滞", "平衡": "大安·吉稳", "悬置": "大安·观照",
        "参差": "赤口·争阻",
    }[ph]
    dims = DOMAINS["小六壬"]["dims"]
    fa = [dims[i] for i, x in enumerate(v) if x > 0]
    lian = [dims[i] for i, x in enumerate(v) if x < 0]
    if fa and lian:
        tail = f"发：{'、'.join(fa)}；敛：{'、'.join(lian)}。"
    elif fa:
        tail = f"发：{'、'.join(fa)}。"
    elif lian:
        tail = f"敛：{'、'.join(lian)}。"
    else:
        tail = "。"
    return f"{ph}之相，主{gong}；{tail}"


def _render_heal(v):
    """疗愈：复用体用变判级 + 疗愈视角（亏缺宜补、充盈宜疏）。"""
    base = _render_tiyong(v)
    dims = DOMAINS["疗愈"]["dims"]
    xu = [dims[i] for i, x in enumerate(v) if x < 0]
    ying = [dims[i] for i, x in enumerate(v) if x > 0]
    xu_s = "需养补之维：" + ("、".join(xu) if xu else "无") + "；"
    ying_s = "可疏通之维：" + ("、".join(ying) if ying else "无") + "。"
    return base + xu_s + ying_s


# ======================================================================
# 语义桥 · 同编号卦 → 多域并行解读
# ======================================================================

def render(domain: str, g):
    """单域解读：core 向量 → 域内 → 域解读 + 共享结构倾向。"""
    if domain not in DOMAINS:
        raise KeyError(f"未知领域 {domain}；可选 {list(DOMAINS)}")
    v = _map_to_domain(g, domain)
    text = DOMAINS[domain]["render"](v)
    return {"domain": domain, "vec_domain": v, "text": text}


def bridge(g):
    """同一编号卦 → 各域并行解读 + 深度象义（核心产品）。"""
    fp = fingerprint(g)
    g0 = idx_to_g(g) if not isinstance(g, tuple) else g
    idx = g_to_idx(g0)
    return {
        "idx": idx,
        "gua_core": g0,
        "fingerprint": fp,
        "deep": deep_oracle(idx),
        "domains": {d: render(d, g0) for d in DOMAINS},
    }


# ---- 便捷入口 ----
def bridge_by_idx(idx: int):
    return bridge(idx_to_g(idx))


def bridge_by_text(text: str, top_n: int = 1):
    vec = encode(text)
    hits = search(vec, top_n=top_n)
    return vec, hits, [bridge(h["gua"]) for h in hits]


if __name__ == "__main__":
    print("=" * 66)
    print("认知坐标服务 + 语义桥（5 域全景）· 三元九维 19683")
    print("=" * 66)
    for idx in (9841, 19682, 0, 12900):
        b = bridge_by_idx(idx)
        print(f"\n【编号 {b['idx']}】卦 {b['gua_core']}  指纹 {b['fingerprint']['tendency']}")
        print(f"  深度象义 · {b['deep']['ming']} — {b['deep']['qi']}")
        for d, r in b["domains"].items():
            print(f"  [{d}] {r['text']}")
    print("\n-- 自然语言定位 + 五域解读 --")
    vec, hits, bridges = bridge_by_text("根基稳固，主动进取，增益丰盈，时势顺遂", top_n=1)
    print("  输入→向量:", vec, " Top1 卦:", hits[0]["idx"], hits[0]["gua"])
    b = bridges[0]
    print(f"  深度象义 · {b['deep']['ming']}")
    for d, r in b["domains"].items():
        print(f"  [{d}] {r['text']}")
