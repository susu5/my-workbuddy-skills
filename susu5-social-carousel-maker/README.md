# Susu5 Social Carousel Maker

> 社媒多图轮播内容生成 Skill —— 根据文章、主题、产品信息或粗略想法，生成小红书/Rednote、微信图文、视频号封面、海报等多图内容的完整工作流。

## 功能概览

一套**受控的**多图社媒内容生产流程。它扮演「内容导演 + image2 提示词组装器」的角色，而不是一次性图像生成器。

核心特点：

- **逐页内容策划**：从输入中提取主题、受众、平台、目标、核心信息，按内容类型选择结构（知识/种草/文章拆解/故事/报告），产出逐页计划。
- **强制确认闸门**（Hard Gates）：内容计划 → 尺寸 → 视觉风格 → 3 张小样 → 完整多图，每步都需用户确认，避免失控生成。
- **尺寸预设**：内置小红书 3:4、竖版 9:16、方形 1:1、横版 16:9 等 10 种常见规格。
- **视觉风格模板**：20+ 种风格（知识卡片、瑞士强字海报、编辑杂志、极简高级、数据报告、手写笔记、漫画解说等）。
- **图片布局模板**：封面钩子、内容卡片、清单、步骤、对比、数据英雄、案例故事、引用、总结 CTA、思维导图等。
- **提示词组装**：将确认后的页面文案 + 尺寸 + 风格 + 布局 + 一致性规则，组装成完整的最终 image2 提示词。
- **计划校验脚本**：`scripts/validate-carousel-plan.mjs` 校验分页计划 JSON 的完整性。

## 工作流

```
Step 1  理解输入（文章/主题/产品/想法）
Step 2  构建逐页计划 → 用户确认
Step 3  选择尺寸 → 用户确认
Step 4  选择视觉风格 → 用户确认
Step 5  组装最终提示词（封面 + 前两页）
Step 6  生成 3 张小样 → 用户确认
Step 7  生成完整多图
Step 8  交付发布包（标题/正文/标签/清单）
```

## 目录结构

```
susu5-social-carousel-maker/
├── SKILL.md                        # 主技能文件（触发词与流程定义）
├── agents/
│   └── openai.yaml                 # Agent 接口定义
├── references/
│   ├── carousel-structures.md      # 轮播结构模板
│   ├── dimensions.md               # 尺寸预设
│   ├── image-templates.md          # 图片布局模板
│   ├── image2-generation.md        # 图像生成规则
│   ├── page-roles.md               # 页面角色定义
│   ├── prompt-assembly.md          # 提示词组装公式
│   ├── quality-checklist.md        # 质量检查清单
│   └── style-templates.md          # 视觉风格模板
└── scripts/
    └── validate-carousel-plan.mjs  # 分页计划校验脚本
```

## 安装

将 Skill 目录复制到 WorkBuddy 的 skills 目录：

```bash
# 用户级（所有项目可用）
cp -r susu5-social-carousel-maker ~/.workbuddy/skills/

# 项目级（仅当前项目）
cp -r susu5-social-carousel-maker .workbuddy/skills/
```

## 校验脚本用法

```bash
node scripts/validate-carousel-plan.mjs <plan.json>
```

校验分页计划是否包含必需的 `pages[].page_role/title/page_objective/image_template_id`，以及确认后的 `dimension_id` 与 `style_id`，并阻止在小样确认前生成完整多图。

## 许可证

[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/) —— 使用时请注明来源。
