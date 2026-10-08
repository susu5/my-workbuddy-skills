# 外部参考与本地适配

2026-10-08 参考以下作者仓库的设计方法。注册表、封面、骨架和脚本为本地适配实现，未安装外部技能，未引入运行依赖。

| 来源 | 采用的方法 | 本地适配 |
| --- | --- | --- |
| [HTML Report Builder](https://github.com/thatrebeccarae/claude-marketing/tree/main/skills/html-report-builder) | 封面与内页层次、报告章法、结论与建议组件 | 咨询绿皮书；中文系统字体；保持现有无打印/PDF范围 |
| [HTML Design](https://github.com/NimaChu/html-design) | 内容、视觉与交互分开选择，实际浏览器验证 | 四种阅读骨架＋风格注册表；1440、1280、390、320px 检查 |
| [Visual Explainer](https://github.com/nicobailon/visual-explainer) | 图解回答问题，结合指标和精确表格解释 | 首屏可采用图解＋结论；不强制图表数，不删关键文字与条件 |
| [HTML Reports](https://github.com/andrewkobzev/html-reports) | 按文档任务组织模板，单文件与本地字体 | 离线样式、四种正文骨架；交互按需，成品默认单一主题 |

六种大胆风格结合本用户报告需求形成，并非上游提供的同名模板。通用网页能力和在线字体要求不直接带入离线中文报告。
