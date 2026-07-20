"""Deterministic, data-driven classification for literature-note metadata."""

from __future__ import annotations

from collections.abc import Sequence


Rule = tuple[tuple[str, ...], str]


THEME_RULES: tuple[Rule, ...] = (
    (("hank",), "异质主体宏观模型与政策传导"),
    (("migration", "commuting"), "人口迁移与空间劳动力配置"),
    (("housing",), "住房约束与空间资源错配"),
    (("spatial", "geography"), "空间结构与宏观经济政策"),
    (("monetary",), "货币政策传导与区域异质性"),
    (("climate",), "气候冲击与宏观经济"),
)

METHODOLOGY_RULES: tuple[Rule, ...] = (
    (("gravity",), "引力模型与迁移流估计"),
    (("hank",), "HANK模型与政策冲击分析"),
    (("dynamic spatial", "spatial general equilibrium"), "动态空间一般均衡模型"),
    (("deep learning", "neural"), "深度学习近似动态规划"),
    (("difference-in-differences", "instrument"), "准实验识别与计量估计"),
    (("model",), "结构模型与数值模拟"),
)

VARIABLE_RULES: tuple[Rule, ...] = (
    (("migration",), "迁移流、城市便利性和就业机会"),
    (("commuting",), "通勤联系、本地就业弹性和福利"),
    (("housing",), "住房供给、价格约束和就业增长"),
    (("monetary",), "货币政策冲击、收入分布和消费响应"),
    (("hank",), "家庭异质性、资产分布和政策传导"),
)


def _joined_text(values: Sequence[str]) -> str:
    if any(not isinstance(value, str) for value in values):
        raise TypeError("classification inputs must be strings")
    return " ".join(values).casefold()


def _classify(values: Sequence[str], rules: tuple[Rule, ...], fallback: str) -> str:
    text = _joined_text(values)
    for keywords, label in rules:
        if any(keyword in text for keyword in keywords):
            return label
    return fallback


def classify_theme(title: str) -> str:
    return _classify((title,), THEME_RULES, "空间宏观经济与异质性分析")


def classify_methodology(title: str, abstract: str, fulltext: str) -> str:
    if not all(isinstance(value, str) for value in (title, abstract, fulltext)):
        raise TypeError("classification inputs must be strings")
    return _classify(
        (title, abstract, fulltext[:8000]),
        METHODOLOGY_RULES,
        "文献综述或理论分析",
    )


def classify_core_variable(title: str, abstract: str) -> str:
    return _classify(
        (title, abstract),
        VARIABLE_RULES,
        "空间分布、异质性和政策响应",
    )
