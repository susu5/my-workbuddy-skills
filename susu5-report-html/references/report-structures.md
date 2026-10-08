# 阅读骨架与组合方式

骨架决定读者先回答什么问题，风格决定视觉组织，交互决定是否需要主动操作。四种骨架均可使用十种风格，组合仍需适配内容。

| 骨架 | 推荐顺序 | 组件 | 避免 |
| --- | --- | --- | --- |
| `decision-brief` 决策简报 | 判断与条件 → 必要证据 → 已确认下一步 | 少量结论、紧凑对比、行动段 | 为求完整塞入全部方法，或删掉关键限制 |
| `evidence-report` 证据分析 | 总体判断 → 按问题组织证据 → 解释与限制 → 已确认动作 | 精确表、图表、比较条件、来源 | 先贴数据再让读者猜结论，重复等价图表 |
| `process-playbook` 流程方案 | 目标与边界 → 步骤与交接 → 输入和完成标准 → 异常 → 推进动作 | 有序步骤、角色/输入/动作/输出、异常规则 | 用几个 KPI 卡片代替操作说明；补造负责人、时限、奖励 |
| `scenario-model` 情景测算 | 基准与前提 → 参数和结果 → 公式口径 → 情景与边界 | 静态情景表或已确认模型交互 | 排版中创造公式，把测算标为已实现收益 |

## 模板与字段

`render_report.py` 使用 `assets/report-template.html` 的离线基础样式，组合 `assets/layouts/` 的封面与 `assets/structures/` 的正文。输出文件无需模板目录即可离线打开。

先生成骨架再填写；或提供字符串字段 JSON 渲染：

```powershell
python scripts/render_report.py --theme swiss-impact --kind decision-brief --scaffold --out work.html
python scripts/render_report.py --theme swiss-impact --kind decision-brief --values layout-fields.json --out candidate.html
```

输出路径不得已存在，使用新候选文件名。骨架有占位符，不能交付。渲染后仍须核对内容、选择记录、静态检查与浏览器；渲染器不验证授权。

公共字段：

- 纯文本：`REPORT_TITLE`、`REPORT_TYPE`、`ONE_SENTENCE_CONCLUSION`、`DATA_SOURCES`、`GENERATED_DATE`、`REPORT_VERSION`。自动转义，不接受任意 HTML。
- HTML：`REPORT_META`、`DETAIL_SECTIONS`，可选 `HERO_VISUAL`；由执行者按已确认内容编写，脚本不做 HTML 安全净化。
- `SUMMARY_CONTENT` 为 HTML；`SUMMARY_TITLE`、`SUMMARY_SCOPE` 可调整摘要标题与范围。
- 正文 HTML：简报为 `EVIDENCE_CONTENT`；证据分析另加 `INTERPRETATION_CONTENT`；流程为 `FLOW_CONTENT`、`RULES_CONTENT`、`EXCEPTION_CONTENT`；测算为 `SCENARIO_CONTENT`、`METHOD_CONTENT`、`COMPARISON_CONTENT`。
- 前三种的 `ACTION_CONTENT` 可省略，无已确认动作时整节移除。其他必填缺失则报错；需要向读者说明缺失时在片段中写“未提供”及限制。
- 各节标题可用 `EVIDENCE_TITLE`、`INTERPRETATION_TITLE`、`ACTION_TITLE`、`FLOW_TITLE`、`RULES_TITLE`、`EXCEPTION_TITLE`、`SCENARIO_TITLE`、`METHOD_TITLE`、`COMPARISON_TITLE` 自定义。默认标题仅为起点，应以具体问题命名。

字段是从已确认材料整理的排版视图，不替代业务内容包。保留原 `display_value`，不要把 JSON 数字交给模板再决定精度。结构不适用时直接修改生成文件，不为填满栏目制造内容。

## 封面主视觉与组件

`HERO_VISUAL` 可放大数字、对比、流程或关系图。大数字可用 `<dl class="hero-metric"><dt>指标名与状态</dt><dd>已确认展示值</dd></dl>`；相邻 `.note` 写单位、分母、时期与条件。可以为空，不能补假 KPI。

证据对照可用 `.evidence-pair`，步骤可用 `.flow-track`，模型可用 `.scenario-grid`。这些组件只提供布局，步骤数与图表形式由实际内容决定。

- 按任务重组已有材料，保留有意义的先后关系。长报告可扩展目录，短简报三个导航目标即可。
- 复杂表格与长中文标签用整行，简单相关证据可并置；390/320px 改为单列。
- 保留 `summary`、`report-body`、`notes` 锚点；不强制有表或图，完整性由内容包与人工核对保障。
- 黑金用宽幅结果章，咨询用封面与论证内页，工程用步骤轨道，东方用连续图文；不能都退化为同一面板列表。
