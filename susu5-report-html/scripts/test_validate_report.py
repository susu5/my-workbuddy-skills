#!/usr/bin/env python3
"""Behavioral regression checks for style choice and loss of displayed evidence."""
import json
import re
import tempfile
import unittest
from pathlib import Path
from build_style_preview import render_demo, sample_package, STYLES, ROOT
from validate_report import validate_html


class ReportChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)
        self.html = self.path / "report.html"
        self.package = self.path / "content.json"
        self.selection = self.path / "selection.json"
        self.package.write_text(json.dumps(sample_package(), ensure_ascii=False), encoding="utf-8")
        self.record = {"recommended": "light-glass", "reason": "多个分组需要图表和人数表对应。", "offered": list(STYLES), "selected": "clean-table", "selection_basis": "user_choice", "user_response": "测试夹具：选清晰商务"}
        self.save()

    def save(self, html=None):
        self.html.write_text(html or render_demo(self.record["selected"]), encoding="utf-8")
        self.selection.write_text(json.dumps(self.record, ensure_ascii=False), encoding="utf-8")

    def check(self, selection=True, required=True):
        return validate_html(self.html, False, self.package, None, self.selection if selection else None, required)[0]

    def test_all_themes_with_three_charts_and_long_chinese(self):
        for theme in STYLES:
            with self.subTest(theme=theme):
                self.record["selected"] = theme
                self.save()
                self.assertEqual(self.check(), [])

    def test_missing_choice_blocks_delivery(self):
        self.assertTrue(self.check(selection=False))

    def test_legacy_static_check_remains_usable(self):
        self.assertEqual(self.check(selection=False, required=False), [])

    def test_mismatched_choice_blocks_delivery(self):
        self.record["selected"] = "dark-analytics"
        self.save(render_demo("clean-table"))
        self.assertTrue(self.check())

    def test_not_all_styles_offered_blocks_delivery(self):
        self.record["offered"] = ["clean-table"]
        self.save()
        self.assertTrue(self.check())

    def test_timeout_cannot_stand_in_for_choice(self):
        self.record["selection_basis"] = "timeout"
        self.save()
        self.assertTrue(self.check())

    def test_explicit_style_and_delegation_are_supported(self):
        for basis in ("explicit_style", "delegated"):
            self.record["selection_basis"] = basis
            self.save()
            self.assertEqual(self.check(), [])

    def test_altered_numeric_cell_detected(self):
        self.save(render_demo().replace('>32</td>', '>33</td>'))
        self.assertTrue(self.check())

    def test_zero_cannot_be_replaced_by_eighty(self):
        self.save(render_demo().replace('>0</td>', '>80</td>'))
        self.assertTrue(self.check())

    def test_missing_not_interchangeable_with_zero(self):
        self.save(render_demo().replace('>未提供</td>', '>0</td>'))
        self.assertTrue(self.check())

    def test_duplicate_and_broken_anchors_detected(self):
        for added in ('<div id="summary"></div>', '<a href="#absent">详情</a>'):
            self.save(render_demo().replace('</body>', added + '</body>'))
            self.assertTrue(self.check())

    def test_external_and_relative_assets_detected(self):
        for source in ('https://example.com/chart.png', '//example.com/chart.png', 'chart.png'):
            self.save(render_demo().replace('</body>', f'<img src="{source}" alt="图"></body>'))
            self.assertTrue(self.check())

    def test_source_hyperlink_is_not_render_dependency(self):
        self.save(render_demo().replace('</body>', '<a href="https://example.com/source">来源说明</a></body>'))
        self.assertEqual(self.check(), [])

    def test_template_is_valid(self):
        self.assertEqual(validate_html(ROOT / "assets/report-template.html", True, None, None)[0], [])

    def add_input(self, markup, label='<label for="parameter">参数含义</label>', scenario=False):
        html = render_demo()
        if scenario:
            html = html.replace('data-report-kind="evidence-report"', 'data-report-kind="scenario-model"')
        self.save(html.replace('</main>', '<section><h2>参数与结果</h2>' + label + markup + '</section></main>'))

    def test_complete_brief_without_tables_or_optional_sections(self):
        # A brief can preserve its conclusions without inventing table rows or owners.
        package = sample_package()
        package.pop("presentation_checks")
        self.package.write_text(json.dumps(package, ensure_ascii=False), encoding="utf-8")
        html = render_demo().replace('data-report-kind="evidence-report"', 'data-report-kind="decision-brief"')
        html = re.sub(r'<table\b.*?</table>', '', html, flags=re.S).replace(' id="key-metrics"', '')
        self.save(html)
        self.assertEqual(self.check(), [])

    def test_legacy_report_without_kind_is_supported(self):
        self.save(render_demo().replace(' data-report-kind="evidence-report"', ''))
        self.assertEqual(self.check(), [])

    def test_unknown_kind_rejected(self):
        self.save(render_demo().replace('data-report-kind="evidence-report"', 'data-report-kind="unknown"'))
        self.assertTrue(self.check())

    def test_required_navigation_region_cannot_disappear(self):
        self.save(render_demo().replace('id="report-body"', 'id="other-body"'))
        self.assertTrue(self.check())

    def test_semantic_main_and_section_titles_required(self):
        for old, new in (('<h1>', '<div>'), ('<h2', '<div'), ('<main>', '<div>')):
            with self.subTest(old=old):
                self.save(render_demo().replace(old, new))
                self.assertTrue(self.check())

    def test_percentage_default_and_valid_boundaries(self):
        for value in ('0', '20', '100'):
            with self.subTest(value=value):
                self.add_input(f'<input id="parameter" type="range" min="0" max="100" step="5" value="{value}" data-value-kind="probability" data-value-scale="percent">', scenario=True)
                self.assertEqual(self.check(), [])

    def test_negative_or_excess_probability_rejected(self):
        for lo, hi, value in (('-10', '100', '20'), ('0', '110', '20'), ('0', '100', '-10')):
            with self.subTest(lo=lo, hi=hi, value=value):
                self.add_input(f'<input id="parameter" type="range" min="{lo}" max="{hi}" value="{value}" data-value-kind="probability" data-value-scale="percent">')
                self.assertTrue(any('概率' in error or '默认值' in error for error in self.check()))

    def test_fraction_scale_is_distinguished_from_percent(self):
        self.add_input('<input id="parameter" type="range" min="0" max="1" step="0.05" value="0.2" data-value-kind="probability" data-value-scale="fraction">')
        self.assertEqual(self.check(), [])
        self.add_input('<input id="parameter" type="range" min="0" max="100" value="20" data-value-kind="probability" data-value-scale="fraction">')
        self.assertTrue(self.check())

    def test_probability_requires_scale(self):
        self.add_input('<input id="parameter" type="range" min="0" max="100" value="20" data-value-kind="probability">')
        self.assertTrue(self.check())

    def test_unlabelled_or_broken_label_rejected(self):
        for label in ('', '<label for="absent">参数</label>', '<label for="parameter"> </label>'):
            with self.subTest(label=label):
                self.add_input('<input id="parameter" type="range" min="0" max="100" value="20">', label)
                self.assertTrue(any('可访问名称' in error for error in self.check()))

    def test_accessible_name_alternatives(self):
        for label, name in (('', 'aria-label="转化率"'), ('<p id="rate-label">转化率</p>', 'aria-labelledby="rate-label"')):
            self.add_input(f'<input id="parameter" type="range" min="0" max="100" value="20" {name}>', label)
            self.assertEqual(self.check(), [])
        self.add_input('<input id="parameter" type="range" value="20" aria-labelledby="absent">', '')
        self.assertTrue(self.check())

    def test_invalid_range_or_step_rejected(self):
        for attrs in ('min="20" max="10" value="15"', 'min="0" max="100" value="110"', 'min="0" max="100" value="20" step="0"', 'min="0" max="100" value="21" step="5"'):
            with self.subTest(attrs=attrs):
                self.add_input(f'<input id="parameter" type="range" {attrs}>')
                self.assertTrue(self.check())

    def test_scenario_requires_declared_defaults_and_bounds(self):
        self.add_input('<input id="parameter" type="range" value="20">', scenario=True)
        self.assertTrue(any('明确 min' in error for error in self.check()))

    def test_invalid_numbers_report_errors_without_crashing(self):
        for attrs in ('min="0" max="100" value="NaN"', 'min="0" max="Infinity" value="20"', 'min="-1e308" max="1e308" value="1e308"'):
            with self.subTest(attrs=attrs):
                self.add_input(f'<input id="parameter" type="range" {attrs}>')
                self.assertTrue(self.check())

    def test_count_cannot_be_negative_or_fractional(self):
        for attrs in ('min="-1" max="100" value="20"', 'min="0" max="100" value="20" step="0.5"', 'min="0" max="100" value="20" step="any"'):
            self.add_input(f'<input id="parameter" type="range" {attrs} data-value-kind="count">')
            self.assertTrue(self.check())
        self.add_input('<input id="parameter" type="range" min="0" max="100" value="20" step="1" data-value-kind="count">')
        self.assertEqual(self.check(), [])

    def test_negative_financial_input_can_be_valid(self):
        self.add_input('<input id="parameter" type="number" min="-100" max="100" value="-20" step="1">')
        self.assertEqual(self.check(), [])

    def test_metric_condition_and_status_cannot_be_lost(self):
        package = sample_package()
        package['key_metrics'][0].update(status_label='基准情景测算', condition='仅适用于已确认的同口径样本')
        self.package.write_text(json.dumps(package, ensure_ascii=False), encoding='utf-8')
        html = render_demo().replace('</main>', '<p>基准情景测算；仅适用于已确认的同口径样本</p></main>')
        self.save(html)
        self.assertEqual(self.check(), [])
        for text in ('基准情景测算', '仅适用于已确认的同口径样本'):
            self.save(html.replace(text, ''))
            self.assertTrue(self.check())


if __name__ == "__main__":
    unittest.main(verbosity=2)
