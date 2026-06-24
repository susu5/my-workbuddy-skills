# My WorkBuddy Skill List

> 个人 WorkBuddy Skill 使用清单与描述。
> License: CC-BY 4.0 | 使用时请注明来源

---

## Skill 清单

| # | Skill 名称 | 安装地址 | 描述 | 作者 | 备注 |
|---|-----------|---------|------|------|------|
| 1 | elite-longterm-memory | [GitHub](https://github.com/susu5/elite-longterm-memory) | 终极 AI 长期记忆系统，WAL 协议 + 向量检索 + git-notes + 云备份。防止跨对话失忆，支持 Cursor/Claude/ChatGPT/Copilot | NextFrontierBuilds | 需要 OPENAI_API_KEY 和 memory-lancedb 插件 |
| 2 | github-onboarding | [GitHub](https://github.com/susu5/github-onboarding) | 引导用户完成 GitHub 注册 → 创建仓库 → 上传本地代码全流程，含 .gitignore 自动生成脚本 | zorro | 自建 Skill，首次安装于 2026-06-24 |
| 3 | guizang-ppt-skill | [GitHub](https://github.com/susu5/guizang-ppt-skill) | 生成横向翻页网页 PPT（单 HTML 文件），支持"电子杂志 × 电子墨水"和"瑞士国际主义"两种风格 | 歸藏 (op7418) | 原仓库: github.com/op7418/guizang-ppt-skill |
| 4 | html-report-generator | [GitHub](https://github.com/susu5/html-report-generator) | 内置 47 套 PPT 模板，自动将任意内容生成 5-15 页精美 HTML 报告（1017×720px），覆盖商务/科技/学术等场景 | susu5 | 触发词：生成报告、做成HTML、内容可视化 |
| 5 | tencent-sheet-images | [GitHub](https://github.com/susu5/tencent-sheet-images) | 从腾讯在线表格提取单元格图片，并结合行列文字进行图文对照阅读 | susu5 | 适用场景：产品流程图阅读、界面截图分析 |

---

## 分类概览

### 按功能分类

| 分类 | Skill |
|------|-------|
| 记忆增强 | elite-longterm-memory |
| 开发工具 | github-onboarding |
| 内容创作 | guizang-ppt-skill、html-report-generator |
| 数据读取 | tencent-sheet-images |

### 按来源分类

| 来源 | Skill |
|------|-------|
| 自建 | github-onboarding、html-report-generator、tencent-sheet-images |
| 社区 | elite-longterm-memory（NextFrontierBuilds）、guizang-ppt-skill（歸藏） |

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
