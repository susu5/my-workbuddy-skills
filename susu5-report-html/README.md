# susu5-report-html

> SUSU5 报告 HTML — 离线单文件 HTML 报告制作与美化 Skill（v2.0.0）

## 功能

把已确认的内容做成逻辑清楚、对比方便的**离线单文件 HTML 报告**。核心要求：准确表达、少用缩词、完整逻辑、多图多表、重点有颜色和字体区分（不是默认放大字号）。

### 何时调用

- 用户提出或确认使用 HTML 交付报告、分析、总结、方案或文档时立即进入
- 对已有 HTML 报告重新设计、改风格或完善展示时调用
- 不接管：HTML 代码教学、网站应用开发、邮件模板等普通网页开发

### 四种风格，先推荐后确认

每次新报告先**推荐且只推荐一种风格**并说明理由，同时展示全部四种供用户选择：

| 风格 | 视觉特征 | 适用场景 |
|------|---------|---------|
| 清晰商务（clean-table） | 白底深蓝 · 表格清楚 | 正式汇报与逐项核对 |
| 现代数据（light-glass） | 浅灰蓝紫 · 图表成组 | 转化率与多维数据分析 |
| 温暖编辑（editorial-brief） | 暖白单栏 · 中文衬线标题 | 长报告与策略说明 |
| 深色研判（dark-analytics） | 深蓝灰底 · 高对比文字 | 专题研判与会议展示 |

### 内容纪律

- 保留原有数值、结论、证据强度、比较条件、时间范围、样本数量、限制与负责人
- 缺失数据不填零；相关性不写成因果；猜测不写成事实
- 对比优先用表格给精确值，用图表解释差异、趋势或分布；每张图表回答一个问题
- 单文件、UTF-8、`lang="zh-CN"`、内嵌 CSS/JS/SVG，无外部资源依赖

## 目录结构

```
susu5-report-html/
├── SKILL.md                                # Skill 主指令
├── agents/openai.yaml                      # Codex/其他 agent 配置
├── assets/
│   ├── report-template.html                # 报告起点模板
│   └── style-preview.html                  # 四风格实样预览
├── references/
│   ├── html-design-and-acceptance.md       # 设计规范与验收标准
│   └── style-themes.md                     # 风格定义与选择记录格式
└── scripts/
    ├── build_style_preview.py              # 从模板重建四风格画廊（合成数据）
    ├── validate_report.py                  # 报告静态校验（结构/风格记录/内容一致性）
    └── test_validate_report.py             # 行为回归测试
```

## 使用

将本目录复制到 WorkBuddy 的 skills 目录：

```bash
cp -r susu5-report-html ~/.workbuddy/skills/
```

交付前运行校验脚本：

```powershell
python scripts/validate_report.py <报告.html> --theme <风格参数> --style-selection <风格记录.json> --require-style-selection --content-package <内容包.json>
```

## 版本

- **v2.0.0**（2026-09-22）：当前版本，新增强制风格选择流程与内容包校验
- 更新日期：2026-09-22

## 许可证

[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/) · 使用时请注明来源
