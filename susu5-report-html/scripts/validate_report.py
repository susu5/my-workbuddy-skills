#!/usr/bin/env python3
"""Static checks only: structure, recorded style choice and selected content."""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from render_report import STYLES, KINDS

ALLOWED_THEMES = set(STYLES)
ALLOWED_REPORT_KINDS = set(KINDS)
REQUIRED_SEMANTIC_CLASSES = {
    "metric-primary", "metric-forecast", "is-problem", "is-opportunity",
    "is-uncertain", "delta-negative", "delta-positive", "is-neutral", "is-insufficient",
}
BANNED_WORDS = ["空转", "承压", "走弱", "抓手", "卡点", "雷达", "赋能", "拉通", "闭环", "失速", "击穿"]
ABBREVIATION_PATTERN = re.compile(r"(?:T\+\d+)|\b(?:AOV|GMV|CVR|CTR|ROI|SOP|P0|P1|O1)\b", re.I)
MOJIBAKE_MARKERS = ("�", "ï¼", "ã€", "æœ", "çš", "å…", "Â")
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


def read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def load_package(path: Path) -> dict[str, Any]:
    data = json.loads(read_utf8(path))
    if not isinstance(data, dict):
        raise ValueError("JSON 顶层必须是对象。")
    return data


def normalized_text(text: str) -> str:
    return re.sub(r"\s+", "", text)


def contains_mojibake(text: str) -> bool:
    return any(marker in text for marker in MOJIBAKE_MARKERS)


class ReportParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[tuple[str, str | None]] = []
        self.ids: set[str] = set()
        self.duplicate_ids: set[str] = set()
        self.id_text: dict[str, list[str]] = {}
        self.visible_text: list[str] = []
        self.anchors: list[str] = []
        self.resource_refs: list[str] = []
        self.tables: list[dict[str, int]] = []
        self.table: dict[str, int] | None = None
        self.row_cells = 0
        self.in_thead = False
        self.tag_counts: dict[str, int] = {}
        self.inputs: list[dict[str, str | None]] = []
        self.label_text: dict[str, list[str]] = {}
        self.active_labels: list[str] = []

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        self.tag_counts[tag] = self.tag_counts.get(tag, 0) + 1
        if tag == "input" and (attr.get("type") or "text").lower() in {"range", "number"}:
            self.inputs.append(attr)
        if tag == "label":
            target = attr.get("for") or ""
            self.active_labels.append(target)
            self.label_text.setdefault(target, [])
        element_id = attr.get("id")
        if element_id:
            if element_id in self.ids:
                self.duplicate_ids.add(element_id)
            self.ids.add(element_id)
            self.id_text.setdefault(element_id, [])
        if tag not in VOID_TAGS:
            self.stack.append((tag, element_id))
        href = attr.get("href") or ""
        if tag == "a" and href.startswith("#") and len(href) > 1:
            self.anchors.append(href[1:])
        resource_keys = {"src", "poster", "srcset"}
        if tag in {"link", "image", "use"}:
            resource_keys.update({"href", "xlink:href"})
        if tag == "object":
            resource_keys.add("data")
        for key in resource_keys:
            value = attr.get(key)
            if value and not value.startswith(("data:", "#")):
                self.resource_refs.append(value)
        if tag == "table":
            self.table = {"data_rows": 0, "max_columns": 0}
            self.tables.append(self.table)
        elif tag == "thead":
            self.in_thead = True
        elif tag == "tr" and self.table is not None:
            if not self.in_thead:
                self.table["data_rows"] += 1
            self.row_cells = 0
        elif tag in {"td", "th"} and self.table is not None:
            try:
                self.row_cells += max(1, int(attr.get("colspan") or "1"))
            except ValueError:
                self.row_cells += 1
            self.table["max_columns"] = max(self.table["max_columns"], self.row_cells)

    def handle_endtag(self, tag):
        if tag == "label" and self.active_labels:
            self.active_labels.pop()
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break
        if tag == "table":
            self.table = None
        elif tag == "thead":
            self.in_thead = False

    def handle_data(self, data):
        if any(tag in {"script", "style", "head"} for tag, _ in self.stack):
            return
        text = re.sub(r"\s+", " ", data).strip()
        if text:
            for target in self.active_labels:
                self.label_text[target].append(text)
            self.visible_text.append(text)
            for _, element_id in self.stack:
                if element_id:
                    self.id_text[element_id].append(text)


def validate_selection(selection, selected_theme):
    errors = []
    for key in ("recommended", "selected"):
        value = selection.get(key)
        if not isinstance(value, str) or value not in ALLOWED_THEMES:
            errors.append(f"风格记录缺少有效的 {key}。")
    offered = selection.get("offered")
    valid_offered = (isinstance(offered, list) and bool(offered)
                     and all(isinstance(item, str) and item in ALLOWED_THEMES for item in offered))
    if not valid_offered or len(set(offered)) != len(offered):
        errors.append("风格候选必须是有效、非空且不重复的选项。")
    elif any(selection.get(key) not in offered for key in ('recommended', 'selected')):
        errors.append("候选必须包含本次推荐和最终选择。")
    elif selection.get('selection_basis') == 'user_choice' and len(offered) < 3:
        errors.append("请至少展示三个不同候选后再记录用户选择。")
    if selection.get("selection_basis") not in ("user_choice", "explicit_style", "delegated"):
        errors.append("风格记录没有有效选择依据；默认值、超时或未回复不算选择。")
    for key in ("reason", "user_response"):
        if not isinstance(selection.get(key), str) or not selection[key].strip():
            errors.append(f"风格记录缺少 {key}。")
    if selection.get("selected") != selected_theme:
        errors.append("HTML 风格与用户选择记录不一致。")
    return errors


def validate_inputs(parsed, report_kind):
    """Validate declared names/defaults/bounds; never execute a business model."""
    errors = []
    for index, attrs in enumerate(parsed.inputs, 1):
        name = attrs.get("id") or f"第 {index} 个输入"
        labelled_ids = (attrs.get("aria-labelledby") or "").split()
        labelled_by_text = bool(labelled_ids) and all(
            item in parsed.ids and bool(parsed.id_text.get(item)) for item in labelled_ids
        )
        label_text = " ".join(parsed.label_text.get(attrs.get("id"), []))
        if not (label_text.strip() or (attrs.get("aria-label") or "").strip() or labelled_by_text):
            errors.append(f"输入 {name} 缺少关联 label 或可访问名称。")
        if report_kind == "scenario-model" and any(attrs.get(key) in (None, "") for key in ("min", "max", "value")):
            errors.append(f"情景输入 {name} 必须明确 min、max 和默认 value。")
        is_range = (attrs.get("type") or "").lower() == "range"
        values = {}
        defaults = {"min": "0", "max": "100"} if is_range else {}
        for key in ("min", "max", "value", "step"):
            raw = attrs.get(key, defaults.get(key))
            if raw is None or (key == "step" and raw == "any"):
                continue
            try:
                number = float(raw)
                if not math.isfinite(number):
                    raise ValueError("not finite")
                values[key] = number
            except (TypeError, ValueError):
                errors.append(f"输入 {name} 的 {key} 必须是有限数值。")
        lo, hi, value = (values.get(key) for key in ("min", "max", "value"))
        if lo is not None and hi is not None and lo >= hi:
            errors.append(f"输入 {name} 的 min 必须小于 max。")
        if value is not None and ((lo is not None and value < lo) or (hi is not None and value > hi)):
            errors.append(f"输入 {name} 的默认值超出声明范围。")
        step = values.get("step", 1.0)
        if step <= 0:
            errors.append(f"输入 {name} 的 step 必须大于零或为 any。")
        elif value is not None and attrs.get("step") != "any":
            # Native number inputs use the value attribute as the step base when min is absent.
            base = lo if lo is not None else value
            ticks = (value - base) / step
            if not math.isfinite(ticks) or not math.isclose(ticks, round(ticks), abs_tol=1e-7):
                errors.append(f"输入 {name} 的默认值与步长不匹配。")
        kind = attrs.get("data-value-kind")
        if kind == "probability":
            scale = attrs.get("data-value-scale")
            if scale not in {"percent", "fraction"}:
                errors.append(f"概率输入 {name} 必须声明 percent 或 fraction 比例尺度。")
            else:
                upper = 100 if scale == "percent" else 1
                if lo is None or hi is None or lo < 0 or hi > upper or (value is not None and not 0 <= value <= upper):
                    errors.append(f"概率输入 {name} 的范围必须在 0 到 {upper} 之间。")
        elif kind == "count":
            if lo is None or lo < 0 or any(not item.is_integer() for item in (lo, hi, value, step) if item is not None):
                errors.append(f"人数输入 {name} 必须使用非负整数边界、默认值及整数步长。")
            if attrs.get("step") == "any":
                errors.append(f"人数输入 {name} 不得使用任意小数步长。")
    return errors


def validate_against_package(html, visible_text, package, parsed=None):
    errors = []
    compact = normalized_text(visible_text)
    meta = package.get("meta", {})
    fields = [
        ("报告标题", meta.get("title")), ("数据日期", meta.get("data_date")),
        ("数据截止时间", meta.get("cutoff_time")), ("一句话结论", package.get("one_sentence_conclusion")),
    ]
    for metric in package.get("key_metrics", []):
        if isinstance(metric, dict):
            fields.extend((("关键指标名称", metric.get("label")), ("关键指标值", metric.get("display_value"))))
            fields.extend((("指标状态", metric.get("status_label")), ("指标成立条件", metric.get("condition"))))
    for finding in package.get("priority_findings", []):
        if not isinstance(finding, dict):
            continue
        fields.append(("主要发现", finding.get("title")))
        class_name = {"problem": "is-problem", "opportunity": "is-opportunity"}.get(finding.get("type"))
        if class_name and not re.search(r'class=["\'][^"\']*\b' + class_name + r'\b', html):
            errors.append(f"主要发现缺少语义类 {class_name}。")
    for label, value in fields:
        if value not in (None, "") and normalized_text(str(value)) not in compact:
            errors.append(f"HTML 没有完整呈现{label}：{value}")
    for check in package.get("presentation_checks", []):
        if not isinstance(check, dict) or not isinstance(check.get("id"), str) or not isinstance(check.get("text_sequence"), list) or not check["text_sequence"]:
            errors.append("presentation_checks 每项需要 id 与非空 text_sequence。")
            continue
        element_id = check["id"]
        if parsed is None or element_id not in parsed.id_text:
            errors.append(f"内容核对区域不存在：{element_id}")
            continue
        scope = normalized_text(" | ".join(parsed.id_text[element_id]))
        cursor = 0
        for value in check["text_sequence"]:
            expected = normalized_text(str(value))
            pattern = re.escape(expected)
            if re.fullmatch(r"[-+]?\d[\d,.]*%?", expected):
                pattern = r"(?<![\d.,])" + pattern + r"(?![\d.,%])"
            match = re.search(pattern, scope[cursor:])
            if not expected or match is None:
                errors.append(f"区域 {element_id} 缺少或错序：{value}")
                break
            cursor += match.end()
    return errors


def validate_html(path, template_mode, content_package, expected_theme,
                  style_selection=None, require_style_selection=False):
    errors, warnings = [], []
    html = read_utf8(path)
    for pattern, message in [
        (r"^\s*<!doctype html>", "HTML 必须以 <!DOCTYPE html> 开始。"),
        (r'<html\b[^>]*\blang=["\']zh-cn["\']', 'HTML 必须设置 lang="zh-CN"。'),
        (r'<meta\b[^>]*charset=["\']?utf-8', "HTML 必须声明 UTF-8。"),
    ]:
        if not re.search(pattern, html, re.I):
            errors.append(message)
    if re.search(r"@import\b|\bfetch\s*\(|\bXMLHttpRequest\b|\bWebSocket\s*\(|\bimport\s*\(", html, re.I):
        errors.append("HTML 包含外部资源导入或网络请求代码。")
    for resource in re.findall(r"url\(\s*([^)]*)\)", html, re.I):
        if not resource.strip(" \t\r\n\"'").startswith(("data:", "#")):
            errors.append("HTML 包含未内嵌的 CSS 资源。")
            break
    if re.search(r"@media\s+print|window\.print\s*\(|保存为\s*pdf", html, re.I):
        errors.append("HTML 不得包含打印、保存为 PDF 或打印专用样式。")
    if re.search(r"overflow(?:-x|-y)?\s*:\s*(?:auto|scroll)", html, re.I):
        errors.append("HTML 包含内部滚动设置，请拆分表格并移除滑动块。")
    theme_match = re.search(r'<body\b[^>]*\bdata-theme=["\']([^"\']+)["\']', html, re.I)
    selected_theme = theme_match.group(1) if theme_match else None
    kind_match = re.search(r'<body\b[^>]*\bdata-report-kind=["\']([^"\']+)["\']', html, re.I)
    report_kind = kind_match.group(1) if kind_match else "evidence-report"
    if not (template_mode and report_kind == "{{REPORT_KIND}}") and report_kind not in ALLOWED_REPORT_KINDS:
        errors.append(f"不支持的内容结构：{report_kind}")
    if not (template_mode and selected_theme == "{{REPORT_THEME}}"):
        if selected_theme not in ALLOWED_THEMES:
            errors.append(f"不支持或缺少报告风格：{selected_theme}")
        if expected_theme and selected_theme != expected_theme:
            errors.append(f"HTML 风格与 --theme {expected_theme} 不一致。")
    # A delivered report needs only its selected style. Legacy four-theme reports
    # remain valid; unrelated palettes are not mandatory payload.
    if selected_theme in ALLOWED_THEMES and not re.search(
            r'body\[data-theme=["\']' + re.escape(selected_theme) + r'["\']\]', html):
        errors.append(f"HTML 缺少 {selected_theme} 风格定义。")
    parsed = ReportParser()
    parsed.feed(html)
    visible_text = " ".join(parsed.visible_text)
    if parsed.resource_refs:
        errors.append("HTML 包含未内嵌的资源依赖。")
    if parsed.duplicate_ids:
        errors.append("HTML 存在重复 ID：" + "、".join(sorted(parsed.duplicate_ids)))
    broken = set(parsed.anchors) - parsed.ids
    if broken:
        errors.append("内部链接没有目标：" + "、".join(sorted(broken)))
    if contains_mojibake(visible_text):
        errors.append("页面可能包含中文乱码。")
    for word in BANNED_WORDS:
        if word in visible_text:
            warnings.append(f"请人工核对含义是否准确，避免模糊表达：{word}")
    abbreviations = sorted(set(ABBREVIATION_PATTERN.findall(visible_text)))
    if abbreviations:
        warnings.append("请确认这些简称已有全称或解释：" + "、".join(abbreviations))
    missing_ids = {"summary", "report-body", "notes"} - parsed.ids
    if missing_ids:
        errors.append("缺少必要页面区域：" + "、".join(sorted(missing_ids)))
    if parsed.tag_counts.get("h1", 0) != 1:
        errors.append("报告必须有且仅有一个 h1 主标题。")
    for tag in ("header", "main", "footer"):
        if not parsed.tag_counts.get(tag):
            errors.append(f"报告缺少 {tag} 文档区域。")
    if not parsed.tag_counts.get("h2"):
        errors.append("报告章节应使用 h2 语义标题。")
    errors.extend(validate_inputs(parsed, report_kind))
    if parsed.inputs:
        warnings.append("包含参数输入；尚需独立核对模型、边界情景、动态同步、重置及键盘操作。")
    for index, table in enumerate(parsed.tables, 1):
        if table["max_columns"] > 7:
            errors.append(f"第 {index} 张表超过七列，请拆表。")
        if table["data_rows"] > 10:
            errors.append(f"第 {index} 张表超过十行数据，请拆表。")
    missing_classes = {name for name in REQUIRED_SEMANTIC_CLASSES if not re.search(r"\." + re.escape(name) + r"\b", html)}
    if missing_classes:
        errors.append("缺少通用颜色语义类：" + "、".join(sorted(missing_classes)))
    if not template_mode:
        unresolved = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", html)))
        if unresolved:
            errors.append("未替换的模板字段：" + "、".join(unresolved[:10]))
        if content_package:
            try:
                errors.extend(validate_against_package(html, visible_text, load_package(content_package), parsed))
            except (OSError, ValueError, TypeError, AttributeError) as exc:
                errors.append(f"内容包无法读取或结构不符合要求：{exc}")
        else:
            warnings.append("未提供内容包；需要人工核对全部数据和结论。")
        if style_selection:
            try:
                errors.extend(validate_selection(load_package(style_selection), selected_theme))
            except (OSError, ValueError, TypeError) as exc:
                errors.append(f"风格记录无法读取：{exc}")
        elif require_style_selection:
            errors.append("缺少本次风格选择记录，不能以默认风格生成报告。")
        else:
            warnings.append("未核对风格选择记录；新交付应使用 --require-style-selection。")
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description="单文件 HTML 报告静态检查，不代替视觉与业务验收。")
    parser.add_argument("html", type=Path)
    parser.add_argument("--content-package", type=Path)
    parser.add_argument("--theme", choices=sorted(ALLOWED_THEMES))
    parser.add_argument("--template", action="store_true")
    parser.add_argument("--style-selection", type=Path, help="独立的风格选择记录 JSON")
    parser.add_argument("--require-style-selection", action="store_true")
    args = parser.parse_args()
    if args.template and (args.require_style_selection or args.style_selection):
        parser.error("模板检查不接受业务报告的风格选择记录。")
    try:
        errors, warnings = validate_html(args.html, args.template, args.content_package,
                                        args.theme, args.style_selection, args.require_style_selection)
    except (OSError, UnicodeError, ValueError) as exc:
        errors, warnings = [str(exc)], []
    for warning in warnings:
        print(f"提醒：{warning}")
    for error in errors:
        print(f"错误：{error}")
    if errors:
        print(f"静态检查未通过：{len(errors)} 个错误。")
        return 1
    print("静态检查通过；仍需实际浏览器检查、人工内容核对，选择记录也须与真实对话一致。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
