#!/usr/bin/env python3
"""Behavioral regression checks for style choice and loss of displayed evidence."""
import json
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
