#!/usr/bin/env python3
"""Rebuild the four-style gallery from the actual report template; synthetic data only."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
STYLES = {
    "clean-table": ("清晰商务", "白底深蓝 · 表格清楚 · 适合正式汇报与逐项核对"),
    "light-glass": ("现代数据", "浅灰蓝紫 · 图表成组 · 适合转化率与多维数据分析"),
    "editorial-brief": ("温暖编辑", "暖白单栏 · 中文衬线标题 · 适合长报告与策略说明"),
    "dark-analytics": ("深色研判", "深蓝灰底 · 高对比文字 · 适合专题研判与会议展示"),
}
GROUPS = [
    ("总体对比", "全部客户", [("方案甲", "1,000", "80", "8.0%", 80), ("方案乙", "1,000", "50", "5.0%", 50)]),
    ("首次咨询客户", "首次咨询客户", [("方案甲", "400", "32", "8.0%", 80), ("方案乙", "400", "16", "4.0%", 40)]),
    ("再次咨询客户", "再次咨询客户", [("方案甲", "600", "48", "8.0%", 80), ("方案乙", "600", "34", "5.7%", 57)]),
]
CONCLUSION = "示例中方案甲的买单比例较高；这些虚构数据仅用于展示排版，不用于判断真实业务效果。"


def table(group, ident):
    title, scope, rows = group
    body = "".join(
        f'<tr><th scope="row" class="group-{letter}">{label}</th><td class="number">{total}</td><td class="number">{buyers}</td><td class="number group-{letter}"><strong>{rate}</strong></td></tr>'
        for letter, (label, total, buyers, rate, _) in zip("ab", rows)
    )
    return f'<table id="{ident}"><caption>{scope} · 虚构示例，2026年9月</caption><thead><tr><th scope="col">服务方案</th><th scope="col" class="number">客户人数</th><th scope="col" class="number">买单人数</th><th scope="col" class="number">买单比例</th></tr></thead><tbody>{body}</tbody></table>'


def chart(group, ident):
    title, scope, rows = group
    bars = "".join(
        f'<div class="bar-row"><div class="bar-label"><span class="group-{letter}">{label}</span><strong class="group-{letter}">{rate}</strong></div><div class="bar-track" aria-hidden="true"><div class="bar-fill group-{letter}" style="width:{width}%"></div></div></div>'
        for letter, (label, _, _, rate, width) in zip("ab", rows)
    )
    return f'<figure class="chart-card" id="{ident}"><figcaption>{title}：买单比例</figcaption>{bars}<div class="chart-scale"><span>0%</span><span>5%</span><span>10%</span></div><p class="note">2026年9月 · 三张图使用同一刻度；具体人数见相邻表格。</p></figure>'


def sample_package():
    return {
        "meta": {"title": "服务方案与买单情况", "data_date": "2026年9月", "cutoff_time": "2026年9月30日"},
        "one_sentence_conclusion": CONCLUSION,
        "key_metrics": [{"label": "方案甲", "display_value": "8.0%"}, {"label": "方案乙", "display_value": "5.0%"}],
        "presentation_checks": [
            {"id": f"comparison-{index}", "text_sequence": [str(value) for row in group[2] for value in row[:4]]}
            for index, group in enumerate(GROUPS)
        ] + [{"id": "missing-example", "text_sequence": ["尚未提供结果", "未提供", "已确认无人买单", "0"]}],
    }


def render_demo(theme="clean-table", controls=False):
    if theme not in STYLES:
        raise ValueError("Unknown theme")
    template = (ROOT / "assets/report-template.html").read_text(encoding="utf-8")
    summary = '<div class="conclusion-grid">'
    for label, total, buyers, rate, _ in GROUPS[0][2]:
        summary += f'<article class="conclusion-card"><h3>{label}：总体买单比例</h3><span class="metric-status">虚构示例数据 · 2026年9月</span><p class="strong-number metric-primary">{rate}</p><p class="note">{buyers}名买单客户 / {total}名客户。仅展示数值，不能据此判断真实业务效果。</p></article>'
    summary += '<article class="conclusion-card"><h3>比较结果的成立条件</h3><p>先核对样本与观察时间。</p><p class="note is-uncertain">真实报告须确认两组客户是否可比；本页所有数据均为虚构。</p></article></div>'
    sections = '<section class="panel" id="key-metrics"><div class="section-head"><p class="section-kicker">02 · 核心对比</p><h2>总体人数与买单比例有什么差别？</h2><p class="section-summary">买单比例＝买单人数÷客户人数。蓝色与紫色区分方案，不表示好坏。</p></div>'
    sections += table(GROUPS[0], 'comparison-0') + chart(GROUPS[0], 'chart-0') + '</section>'
    sections += '<section class="panel"><div class="section-head"><p class="section-kicker">03 · 分项对比</p><h2>不同咨询阶段的差别是否一致？</h2><p class="section-summary">每组先给人数与精确比例，再用同一刻度观察差异。</p></div>'
    for index, group in enumerate(GROUPS[1:], 1):
        sections += '<h3>' + group[0] + '</h3>' + table(group, f'comparison-{index}') + chart(group, f'chart-{index}')
    sections += '</section>'
    sections += '<section class="panel"><p class="section-kicker">03 · 理解限制</p><h2>看到差异，还要检查比较条件</h2><p>两组客户可能来自不同渠道，也可能在咨询阶段、观察时间或参与方式上存在差异。真实报告应当说明这些条件，再判断结果能支持多强的结论。</p><p class="callout is-uncertain"><strong>需要确认：</strong>样本是否可比、观察时间是否一致。不要把“买单比例较高”直接写成“方案带来了提升”。</p></section>'
    details = '<p>所有方案、人数和比例均为虚构示例；不对应任何真实客户或项目。</p><details><summary>展开：缺失数据与零值的写法</summary><table id="missing-example"><thead><tr><th scope="col">数据状态</th><th scope="col">显示内容</th></tr></thead><tbody><tr><td>尚未提供结果</td><td class="is-insufficient">未提供</td></tr><tr><td>已确认无人买单</td><td class="number">0</td></tr></tbody></table><p class="note">“未提供”表示缺少记录，“0”表示已有记录且数值为零，二者不能互换。</p></details>'
    values = {
        "REPORT_THEME": theme, "REPORT_TITLE": "服务方案与买单情况", "REPORT_TYPE": "四种风格实样 · 虚构示例数据",
        "REPORT_KIND": "evidence-report",
        "REPORT_META": "<span>数据日期：2026年9月</span><span>统计截至：2026年9月30日</span><span>数据范围：2,000名虚构客户</span>",
        "ONE_SENTENCE_CONCLUSION": CONCLUSION,
        "SUMMARY_TITLE": "先看总体差别与判断条件",
        "SUMMARY_SCOPE": "核心值与适用条件放在一起，精确人数与分组证据随后展开。",
        "SUMMARY_CONTENT": summary,
        "REPORT_SECTIONS": sections, "NOTES_TITLE": "数据说明", "DETAIL_SECTIONS": details,
        "DATA_SOURCES": "虚构数据，仅供风格预览", "GENERATED_DATE": "2026年9月29日", "REPORT_VERSION": "风格实样 v2.1.0",
    }
    html = re.sub(r"\{\{([A-Z0-9_]+)\}\}", lambda m: values[m[1]], template)
    if controls:
        buttons = ''.join(f'<button type="button" data-style="{key}" aria-pressed="{str(key == theme).lower()}"><strong>{name}</strong><span>{description}</span></button>' for key, (name, description) in STYLES.items())
        toolbar = '<aside class="preview-tools" aria-label="四种风格预览"><p><strong>同一份内容，四种设计</strong> · 点击下方风格查看实际效果</p><div class="preview-options">' + buttons + '</div><p class="note">全部数据均为虚构。此处切换仅用于预览，不记录正式报告的风格选择。</p></aside>'
        css = '.preview-tools{margin:24px 0;padding:20px;border:1px solid var(--border);background:var(--panel)}.preview-options{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}.preview-options button{font:inherit;text-align:left;padding:12px 14px;border:1px solid var(--border);border-radius:4px;background:var(--page-bg);color:var(--text);cursor:pointer}.preview-options button span{display:block;font-size:15px;line-height:1.6;margin-top:6px;color:var(--muted)}.preview-options button[aria-pressed="true"]{outline:2px solid var(--blue);outline-offset:1px}.preview-options button strong{font-size:18px}@media(max-width:900px){.preview-options{grid-template-columns:repeat(2,minmax(0,1fr))}}'
        js = 'document.querySelectorAll("[data-style]").forEach(function(button){button.addEventListener("click",function(){document.body.dataset.theme=button.dataset.style;document.querySelectorAll("[data-style]").forEach(function(item){item.setAttribute("aria-pressed",String(item===button));});});});'
        html = html.replace('</style>', css + '\n</style>').replace('<div class="shell">', '<div class="shell">' + toolbar, 1).replace('</body>', '<script>' + js + '</script></body>')
    return html


if __name__ == "__main__":
    path = ROOT / "assets/style-preview.html"
    path.write_text(render_demo(controls=True), encoding="utf-8")
    print(f"已重建四种风格实样（虚构数据）：{path}")
