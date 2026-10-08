#!/usr/bin/env python3
"""Compose an offline report from independent structure and visual layout assets.

This renderer does no business calculations. Text slots are escaped; *_CONTENT,
REPORT_META and HERO_VISUAL accept already-reviewed HTML. It is not a sanitizer.
"""
from __future__ import annotations
import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = json.loads((ROOT / 'references/style-registry.json').read_text(encoding='utf-8'))
STYLES = {item['id']: item for item in REGISTRY['styles']}
KINDS = REGISTRY['report_kinds']
TOKEN = re.compile(r'\{\{([A-Z0-9_]+)\}\}')
HTML_SLOTS = {'REPORT_META', 'HERO_VISUAL', 'DETAIL_SECTIONS'} | {
    slot for kind in KINDS.values() for slot in kind['slots']
}
DEFAULTS = {
    'HERO_VISUAL': '', 'SUMMARY_SCOPE': '', 'ACTION_CONTENT': '',
    'SUMMARY_TITLE': '核心判断与成立条件', 'EVIDENCE_TITLE': '证据与精确值',
    'INTERPRETATION_TITLE': '解释与适用限制', 'ACTION_TITLE': '已确认的下一步',
    'FLOW_TITLE': '执行步骤与交接', 'RULES_TITLE': '角色、输入与完成标准',
    'EXCEPTION_TITLE': '异常与处理规则', 'SCENARIO_TITLE': '参数与结果',
    'METHOD_TITLE': '公式、单位与口径', 'COMPARISON_TITLE': '情景对比与边界',
    'NOTES_TITLE': '来源与口径',
}
NAV_LABELS = {
    'decision-brief': '必要证据与动作', 'evidence-report': '依据与解释',
    'process-playbook': '步骤与规则', 'scenario-model': '参数与情景',
}


def render_html(theme: str, kind: str, values: dict | None = None, *, scaffold=False) -> str:
    if theme not in STYLES or kind not in KINDS:
        raise ValueError('未知风格或内容结构。')
    base = (ROOT / 'assets/report-template.html').read_text(encoding='utf-8')
    header = (ROOT / 'assets/layouts' / (STYLES[theme]['layout'] + '.html')).read_text(encoding='utf-8')
    body = (ROOT / 'assets/structures' / KINDS[kind]['template']).read_text(encoding='utf-8')
    given = dict(values or {})
    for key, value in given.items():
        if not isinstance(value, str):
            raise ValueError(f'{key} 必须是字符串；数值请使用已确认的 display_value。')
    # Empty optional actions disappear; never invent owners to fill a section.
    if not scaffold:
        body = re.sub(
            r'<section\b[^>]*data-optional-slot="([A-Z_]+)"[^>]*>.*?</section>',
            lambda m: m[0] if given.get(m[1], '').strip() else '', body, flags=re.S,
        )
    notes = '<section class="panel" id="notes"><div class="section-head"><h2>{{NOTES_TITLE}}</h2></div>{{DETAIL_SECTIONS}}</section>'
    base = re.sub(r'<header\b.*?</header>', lambda _: header, base, count=1, flags=re.S)
    base = re.sub(r'<main>.*?</main>', lambda _: '<main>\n' + body + notes + '\n</main>', base, count=1, flags=re.S)
    base = base.replace('依据与解释</a>', NAV_LABELS[kind] + '</a>')
    merged = DEFAULTS | given | {'REPORT_THEME': theme, 'REPORT_KIND': kind}
    if scaffold:
        # Keep empty content slots visible to the author as placeholders.
        merged.pop('ACTION_CONTENT', None)
    unknown = {key for key in given if key not in set(TOKEN.findall(base)) and given[key].strip()}
    if unknown:
        raise ValueError('当前结构不使用这些字段：' + ', '.join(sorted(unknown)))
    def fill(match):
        key = match[1]
        if key not in merged:
            if scaffold:
                return match[0]
            raise ValueError(f'缺少内容字段：{key}。缺失材料应说明，不得虚构。')
        value = merged[key]
        return value if key in HTML_SLOTS else html.escape(value, quote=True)
    result = TOKEN.sub(fill, base)
    if not scaffold and TOKEN.search(result):
        raise ValueError('内容中仍有未替换字段。')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--theme', required=True, choices=list(STYLES))
    parser.add_argument('--kind', required=True, choices=list(KINDS))
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--values', type=Path, help='已确认的排版字段 JSON；不是业务分析器')
    mode.add_argument('--scaffold', action='store_true', help='仅输出含占位符的工作骨架，不能作为报告交付')
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    try:
        values = json.loads(args.values.read_text(encoding='utf-8-sig')) if args.values else {}
        if not isinstance(values, dict):
            raise ValueError('字段 JSON 顶层必须为对象。')
        result = render_html(args.theme, args.kind, values, scaffold=args.scaffold)
        if args.out.exists():
            raise ValueError('输出路径已存在，请使用新的候选文件名。')
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(result, encoding='utf-8')
    except (OSError, ValueError) as exc:
        parser.exit(1, str(exc) + '\n')
    print(('已生成待填充骨架：' if args.scaffold else '已生成待验收报告：') + str(args.out))


if __name__ == '__main__':
    main()
