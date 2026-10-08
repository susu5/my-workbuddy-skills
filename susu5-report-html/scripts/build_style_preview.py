#!/usr/bin/env python3
"""Build the offline gallery through the same renderer used for real reports."""
from pathlib import Path
import argparse
import html
import json
from render_report import ROOT, STYLES as CATALOG, render_html

STYLES = {key: (item['name'], item['description']) for key, item in CATALOG.items()}
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



def demo_values(theme="clean-table"):
    summary = '<div class="conclusion-grid">'
    for label, total, buyers, rate, _ in GROUPS[0][2]:
        summary += f'<article class="conclusion-card"><h3>{label}：总体买单比例</h3><span class="metric-status">虚构示例数据 · 2026年9月</span><p class="strong-number metric-primary">{rate}</p><p class="note">{buyers}名买单客户 / {total}名客户。仅展示数值，不能判断真实业务效果。</p></article>'
    summary += '<article class="conclusion-card"><h3>比较结果的成立条件</h3><p>先核对样本与观察时间。</p><p class="note is-uncertain">真实报告须确认两组客户是否可比；本页所有数据均为虚构。</p></article></div>'
    evidence = '<p>买单比例＝买单人数÷客户人数。类别颜色区分方案，不表示好坏。三张图使用同一刻度。</p>'
    for index, group in enumerate(GROUPS):
        evidence += f'<h3>{group[0]}</h3><div class="evidence-pair"><div>{table(group, f"comparison-{index}")}</div>{chart(group, f"chart-{index}")}</div>'
    details = '<p>所有方案、人数和比例均为虚构示例；不对应任何真实客户或项目。</p><details><summary>展开：缺失数据与零值的写法</summary><table id="missing-example"><thead><tr><th scope="col">数据状态</th><th scope="col">显示内容</th></tr></thead><tbody><tr><td>尚未提供结果</td><td class="is-insufficient">未提供</td></tr><tr><td>已确认无人买单</td><td class="number">0</td></tr></tbody></table><p class="note">“未提供”表示缺少记录，“0”表示已有记录且数值为零，二者不能互换。</p></details>'
    visual = '<dl class="hero-metric"><dt>方案甲 · 总体买单比例</dt><dd>8.0%</dd></dl><p class="note">80名买单客户 / 1,000名客户<br>2026年9月 · 虚构示例；样本可比性待确认</p>'
    if theme == "engineering-blueprint":
        visual = '<ol class="blueprint-flow" aria-label="方案甲数据关系图"><li>客户样本<strong>1,000名</strong></li><li>其中买单客户<strong>80名</strong></li><li>总体买单比例<strong>8.0%</strong></li></ol><p class="note">2026年9月 · 虚构示例；样本可比性待确认</p>'
    return {
        "REPORT_TITLE": "服务方案与买单情况", "REPORT_TYPE": "证据分析 · 虚构示例",
        "REPORT_META": "<span>数据日期：2026年9月</span><span>统计截至：2026年9月30日</span><span>数据范围：2,000名虚构客户</span>",
        "ONE_SENTENCE_CONCLUSION": CONCLUSION, "HERO_VISUAL": visual,
        "SUMMARY_TITLE": "先看总体差别与判断条件", "SUMMARY_SCOPE": "精确人数与分组证据随后展开；本页用于比较模板构图。",
        "SUMMARY_CONTENT": summary, "EVIDENCE_TITLE": "总体与不同咨询阶段的差别是否一致？",
        "EVIDENCE_CONTENT": evidence, "INTERPRETATION_TITLE": "看到差异，还要检查比较条件",
        "INTERPRETATION_CONTENT": '<p>两组客户可能来自不同渠道，也可能在咨询阶段、观察时间或参与方式上存在差异。真实报告应说明这些条件，再判断结果能支持多强的结论。</p><p class="callout is-uncertain"><strong>需要确认：</strong>样本是否可比、观察时间是否一致。不能把“比例较高”直接写成“方案带来了提升”。</p>',
        "NOTES_TITLE": "数据说明", "DETAIL_SECTIONS": details,
        "DATA_SOURCES": "虚构数据，仅供风格预览", "GENERATED_DATE": "2026年10月8日", "REPORT_VERSION": "风格实样 v3.0.0",
    }


def render_demo(theme="clean-table", controls=False):
    if controls:
        return render_gallery(theme)
    return render_html(theme, "evidence-report", demo_values(theme))


def render_gallery(initial="swiss-impact"):
    if initial not in STYLES:
        raise ValueError("Unknown theme")
    def buttons(family):
        return ''.join(
            f'<button type="button" data-style="{key}" aria-pressed="{str(key == initial).lower()}" aria-controls="report-frame"><strong>{html.escape(item["name"])}</strong><span>{html.escape(item["description"])}</span></button>'
            for key, item in CATALOG.items() if item["family"] == family
        )
    docs = json.dumps({key: render_demo(key) for key in STYLES}, ensure_ascii=False).replace("<", "\\u003c")
    names = json.dumps({key: value[0] for key, value in STYLES.items()}, ensure_ascii=False)
    page = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>报告风格实样 · v3.0.0</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#eeece5;color:#222720;font:18px/1.6 "Microsoft YaHei","PingFang SC",system-ui,sans-serif}
.gallery-tools{max-width:1280px;margin:auto;padding:28px 32px}.gallery-tools h1{font-size:30px;margin:0 0 12px}.gallery-tools p{margin:8px 0 16px}
.options{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:18px 0}
button{min-width:0;text-align:left;font:inherit;line-height:1.5;background:#fffdf5;color:#222720;border:1px solid #8a9181;padding:16px;cursor:pointer}
button strong{display:block;font-size:19px}button span{display:block;font-size:15px;color:#4d5749;margin-top:6px}
button[aria-pressed="true"]{border:2px solid #203db6;padding:15px;background:#e5eaff}
button:focus-visible,summary:focus-visible{outline:3px solid #203db6;outline-offset:3px}
details{margin-top:16px}summary{cursor:pointer;font-weight:600}.gallery-note{font-size:15px;color:#4d5749}
.current{padding:12px 0;border-top:1px solid #8a9181;margin-top:24px}
iframe{display:block;width:100%;border:0;height:900px;background:#fff}
@media(max-width:800px){.options{grid-template-columns:repeat(2,minmax(0,1fr))}.gallery-tools{padding:24px 20px}}
@media(max-width:430px){.options{grid-template-columns:1fr}.gallery-tools{padding:20px 16px}.gallery-tools h1{font-size:26px}}
</style></head><body>
<div class="gallery-tools"><h1>同一份内容，十种报告设计</h1><p>六种大胆方向改变封面构图、字体层级与正文节奏；原四种基础风格继续保留。</p><p class="gallery-note">全部业务数据均为虚构。切换只用于预览，不记录正式报告的风格选择。</p>
<div class="options" aria-label="大胆风格">__BOLD__</div>
<details><summary>展开四种基础风格</summary><div class="options" aria-label="基础风格">__CLASSIC__</div></details>
<p id="current-style" class="current" role="status"></p><noscript><p>此预览切换需要 JavaScript；生成的静态业务报告不依赖它。</p></noscript></div>
<iframe id="report-frame" title="报告风格实样"></iframe>
<script id="demo-documents" type="application/json">__DOCS__</script>
<script>
const docs=JSON.parse(document.getElementById("demo-documents").textContent),names=__NAMES__;
const frame=document.getElementById("report-frame"),status=document.getElementById("current-style");
let observer;
frame.addEventListener("load",()=>{if(observer)observer.disconnect();const resize=()=>{frame.style.height=Math.ceil(frame.contentDocument.body.getBoundingClientRect().height+8)+"px"};resize();observer=new ResizeObserver(resize);observer.observe(frame.contentDocument.body)});
function show(key){frame.srcdoc=docs[key];frame.title=names[key]+" · 虚构报告实样";status.textContent="当前："+names[key]+" · 下方为完整首屏与正文";document.querySelectorAll("[data-style]").forEach(b=>b.setAttribute("aria-pressed",String(b.dataset.style===key)))}
document.querySelectorAll("[data-style]").forEach(b=>b.addEventListener("click",()=>show(b.dataset.style)));
show("__INITIAL__");
</script></body></html>"""
    return page.replace("__BOLD__", buttons("bold")).replace("__CLASSIC__", buttons("classic")).replace("__DOCS__", docs).replace("__NAMES__", names).replace("__INITIAL__", initial)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export-dir", type=Path, help="可选：导出十份实样用于逐份浏览器验证")
    args = parser.parse_args()
    path = ROOT / "assets/style-preview.html"
    path.write_text(render_gallery(), encoding="utf-8")
    if args.export_dir:
        args.export_dir.mkdir(parents=True, exist_ok=True)
        for theme in STYLES:
            (args.export_dir / (theme + ".html")).write_text(render_demo(theme), encoding="utf-8")
    print(f"已重建十种风格实样（虚构数据）：{path}")
