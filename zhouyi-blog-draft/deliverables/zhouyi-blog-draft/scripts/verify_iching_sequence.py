#!/usr/bin/env python3
"""独立核验沈有鼎—张清宇—Radisic 卦序分析中的有限结论。"""

from collections import Counter


NAMES = [
    "乾", "坤", "屯", "蒙", "需", "讼", "师", "比",
    "小畜", "履", "泰", "否", "同人", "大有", "谦", "豫",
    "随", "蛊", "临", "观", "噬嗑", "贲", "剥", "复",
    "无妄", "大畜", "颐", "大过", "坎", "离", "咸", "恒",
    "遁", "大壮", "晋", "明夷", "家人", "睽", "蹇", "解",
    "损", "益", "夬", "姤", "萃", "升", "困", "井",
    "革", "鼎", "震", "艮", "渐", "归妹", "丰", "旅",
    "巽", "兑", "涣", "节", "中孚", "小过", "既济", "未济",
]

# 最低位是初爻。列表按通行本次序排列。
KW = [
    63, 0, 17, 34, 23, 58, 2, 16, 55, 59, 7, 56, 61, 47, 4, 8,
    25, 38, 3, 48, 41, 37, 32, 1, 57, 39, 33, 30, 18, 45, 28, 14,
    60, 15, 40, 5, 53, 43, 20, 10, 35, 49, 31, 62, 24, 6, 26, 22,
    29, 46, 9, 36, 52, 11, 13, 44, 54, 27, 50, 19, 51, 12, 21, 42,
]

# 三位整数同样以最低位为初爻。坐标为（卦名、阴阳族、父子序级）。
TRIGRAM = {
    0: ("坤", "-", 3),
    1: ("震", "+", 2),
    2: ("坎", "+", 1),
    3: ("兑", "-", 0),
    4: ("艮", "+", 0),
    5: ("离", "-", 1),
    6: ("巽", "-", 2),
    7: ("乾", "+", 3),
}

MASK = 0b111111


def comp(x: int) -> int:
    """错：六爻逐位取反。"""
    return x ^ MASK


def rev(x: int) -> int:
    """综：从初爻到上爻反转六个位次。"""
    y = 0
    for i in range(6):
        y |= ((x >> i) & 1) << (5 - i)
    return y


def cr(x: int) -> int:
    return comp(rev(x))


def orbit(x: int) -> tuple[int, ...]:
    return tuple(sorted({x, comp(x), rev(x), cr(x)}))


def hamming(x: int, y: int) -> int:
    return (x ^ y).bit_count()


def edge(x: int, y: int) -> tuple[int, int]:
    return tuple(sorted((x, y)))


def orbit_matchings(vertices: tuple[int, ...]):
    """一个错综轨道上，由 c、r、cr 诱导的不同完美匹配。"""
    vertices = set(vertices)
    result = {}
    for transform in (comp, rev, cr):
        pairs = frozenset(edge(x, transform(x)) for x in vertices)
        if any(a == b for a, b in pairs):
            continue
        if len(pairs) * 2 != len(vertices):
            continue
        failures = sum(a.bit_count() != b.bit_count() for a, b in pairs)
        distance = sum(hamming(a, b) for a, b in pairs)
        result[pairs] = (pairs, failures, distance)
    return tuple(result.values())


def hex_data(x: int):
    lower = TRIGRAM[x & 0b111]
    upper = TRIGRAM[(x >> 3) & 0b111]
    relation = "类合" if lower[1] == upper[1] else "应合"
    return {
        "lower": lower[0],
        "upper": upper[0],
        "relation": relation,
        "main": lower[2] == upper[2],
        "weight": x.bit_count(),
    }


def verify():
    assert len(KW) == 64
    assert len(set(KW)) == 64
    assert set(KW) == set(range(64))

    name_of = dict(zip(KW, NAMES))
    index_of = {code: i + 1 for i, code in enumerate(KW)}

    # 群关系。
    assert all(comp(comp(x)) == x for x in range(64))
    assert all(rev(rev(x)) == x for x in range(64))
    assert all(comp(rev(x)) == rev(comp(x)) for x in range(64))

    fixed = {
        "恒等": 64,
        "错": sum(comp(x) == x for x in range(64)),
        "综": sum(rev(x) == x for x in range(64)),
        "错综": sum(cr(x) == x for x in range(64)),
    }
    assert fixed == {"恒等": 64, "错": 0, "综": 8, "错综": 8}
    assert sum(fixed.values()) // 4 == 20

    orbits = sorted(
        {orbit(x) for x in range(64)},
        key=lambda one_orbit: min(index_of[x] for x in one_orbit),
    )
    sizes = Counter(map(len, orbits))
    assert len(orbits) == 20
    assert sizes == {2: 8, 4: 12}

    main_orbits = [
        one_orbit for one_orbit in orbits
        if all(hex_data(x)["main"] for x in one_orbit)
    ]
    scatter_orbits = [
        one_orbit for one_orbit in orbits
        if not hex_data(one_orbit[0])["main"]
    ]
    assert (len(main_orbits), len(scatter_orbits)) == (6, 14)

    received = {
        frozenset((KW[i], KW[i + 1]))
        for i in range(0, 64, 2)
    }
    priority = {
        frozenset((x, comp(x) if rev(x) == x else rev(x)))
        for x in range(64)
    }
    assert received == priority

    received_cost = sum(
        hamming(KW[i], KW[i + 1])
        for i in range(0, 64, 2)
    )
    assert received_cost == 120

    pure_minimum = sum(
        min(matching[2] for matching in orbit_matchings(one_orbit))
        for one_orbit in orbits
    )
    assert pure_minimum == 96

    winners = []
    for one_orbit in orbits:
        candidates = orbit_matchings(one_orbit)
        optimum = min((candidate[1], candidate[2]) for candidate in candidates)
        orbit_winners = [
            candidate for candidate in candidates
            if (candidate[1], candidate[2]) == optimum
        ]
        assert len(orbit_winners) == 1
        winners.append(orbit_winners[0])

    failures = sum(winner[1] for winner in winners)
    distance = sum(winner[2] for winner in winners)
    winner_edges = set().union(*(set(winner[0]) for winner in winners))
    assert (failures, distance) == (4, 120)
    assert winner_edges == {edge(*pair) for pair in received}

    print("固定点：", fixed)
    print("轨道：20 = 8 个二元 + 12 个四元")
    print("主卦组 / 散卦组：6 / 14")
    print("通行本匹配汉明成本：", received_cost)
    print("完整 K4 候选类纯距离最优：", pure_minimum)
    print("秩优先词典序最优：", (failures, distance))
    print("逐轨道唯一：是")

    print("\n二十个错综不变组：")
    for number, one_orbit in enumerate(orbits, 1):
        members = sorted(one_orbit, key=index_of.get)
        kind = "主" if hex_data(members[0])["main"] else "散"
        positions = ",".join(str(index_of[x]) for x in members)
        names = "、".join(name_of[x] for x in members)
        print(f"{number:02d}. {kind}卦组　{names}　位置 {positions}")


if __name__ == "__main__":
    verify()
