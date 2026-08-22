# My Agent Skill List

> 个人 WorkBuddy Skill 使用清单与描述。
> License: CC-BY 4.0 | 使用时请注明来源

---

## Skill 清单

| # | Skill 名称 | 安装地址 | 描述 | 作者 | 备注 |
|---|-----------|---------|------|------|------|
| 1 | elite-longterm-memory | [GitHub](https://github.com/susu5/elite-longterm-memory) | 终极 AI 长期记忆系统，WAL 协议 + 向量检索 + git-notes + 云备份。防止跨对话失忆，支持 Cursor/Claude/ChatGPT/Copilot | NextFrontierBuilds | 需要 OPENAI_API_KEY 和 memory-lancedb 插件 |
| 2 | github-onboarding | [GitHub](https://github.com/susu5/github-onboarding) | 引导用户完成 GitHub 注册 → 创建仓库 → 上传本地代码全流程，含 .gitignore 自动生成脚本 | zorro | 自建 Skill，首次安装于 2026-06-24 |
| 3 | guizang-ppt-skill | [GitHub](https://github.com/susu5/guizang-ppt-skill) | 生成横向翻页网页 PPT（单 HTML 文件），支持"电子杂志 × 电子墨水"和"瑞士国际主义"两种风格 | 歸藏 (op7418) | 原仓库: github.com/op7418/guizang-ppt-skill |
| 4 | html-report-generator | [GitHub](https://github.com/susu5/html-report-generator) | 内置 47 套 PPT 模板，自动将任意内容生成 5-15 页精美 HTML 报告（1017×720px），覆盖商务/科技/学术等场景 | 未知 | 触发词：生成报告、做成HTML、内容可视化 |
| 5 | tencent-sheet-images | [GitHub](https://github.com/susu5/tencent-sheet-images) | 从腾讯在线表格提取单元格图片，并结合行列文字进行图文对照阅读 | susu5 | 适用场景：产品流程图阅读、界面截图分析 |
| 6 | SUSU5-chain-evidence-data-analysis | [GitHub](https://github.com/susu5/chain-evidence-data-analysis) | SUSU5 链路证据数据分析法 — 先出分析方案、确认后再执行，含数据体检、统计验证、归因分析、报告产出全流程 | susu5 | 2026-07-08 升级为 SUSU5 品牌 + 强制确认流程 |
| 7 | susu5-social-carousel-maker | [GitHub](https://github.com/susu5/my-workbuddy-skills/tree/main/susu5-social-carousel-maker) | 社媒多图轮播内容生成 — 根据文章/主题/产品生成小红书/微信/视频号多图，含逐页策划、尺寸/风格选择、提示词组装、3 张小样确认流程 | susu5 | 2026-07-08 新增，含 README + CC-BY 4.0 LICENSE |
| 8 | susu5-sales-followup-advisor | [GitHub](https://github.com/susu5/my-workbuddy-skills/tree/main/susu5-sales-followup-advisor) | R6 销售追单方案与话术生成 — 结合聊天记录和用户基础信息，生成事实分析、正确 A 链路和可直接发送的销售微信话术 | susu5 | 2026-08-22 新增，含 SKILL.md + references + agents/openai.yaml |

---

## 分类概览

### 按功能分类

| 分类 | Skill |
|------|-------|
| 记忆增强 | elite-longterm-memory |
| 开发工具 | github-onboarding |
| 内容创作 | guizang-ppt-skill、html-report-generator、susu5-social-carousel-maker |
| 数据读取 | tencent-sheet-images |
| 数据分析 | SUSU5-chain-evidence-data-analysis |
| 销售转化 | susu5-sales-followup-advisor |

### 按来源分类

| 来源 | Skill |
|------|-------|
| 自建 | github-onboarding、html-report-generator、tencent-sheet-images、susu5-sales-followup-advisor |
| 社区 | elite-longterm-memory（NextFrontierBuilds）、guizang-ppt-skill（歸藏） |
| 从 Codex 迁移 | chain-evidence-data-analysis |

---

## 安装方式

将 Skill 目录复制到 WorkBuddy 的 skills 目录：

```bash
# 用户级（所有项目可用）
cp -r <skill-name> ~/.workbuddy/skills/

# 项目级（仅当前项目）
cp -r <skill-name> .workbuddy/skills/
```

或从 GitHub 克隆：

```bash
git clone https://github.com/susu5/<skill-name>.git ~/.workbuddy/skills/<skill-name>
```

---

## 许可证

所有 Skill 均采用 [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/) 许可证，使用时必须注明来源。
