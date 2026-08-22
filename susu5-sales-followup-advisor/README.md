# susu5-sales-followup-advisor

> R6 销售追单方案与话术生成 Skill

## 功能简介

针对 R6 追完课及完课后单个客户，结合实际拉取的聊天记录和用户基础信息，生成**证据准确、动作可执行、可由销售直接发送**的当前追单建议。

输出三个固定区块：
1. **事实分析**（D｜客户事实 + A｜已发生动作 + 问题｜当前卡点）
2. **建议方案**（正确 A 链路，带阶段化编号）
3. **建议话术**（销售可直接发送的自然微信话术）

## 触发场景

- 针对单个 R6 客户询问追单方案、下一步怎么跟
- 处理价格、课包、效果、老师、时间、家人、竞品、合同、退款、付款或明确拒绝
- 追完课、试听后跟进或完课后转化

## 使用前提

- 必须同时提供**实际拉取的聊天记录**和**用户基础信息**
- 任一资料缺失时，Skill 只提醒补齐，不继续分析或编写话术
- 仅适用于 R6 单客户追单，不用于销售日报、批量排序或 R7 教学服务

## 包内内容

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 主规则与触发设计 |
| `agents/openai.yaml` | Skill 展示信息与默认调用语 |
| `references/output-quality-rubric.md` | 输出质量量表 |
| `references/r6-daf-core.md` | R6 D/A/F 核心规则 |
| `references/r6-breakpoint-cards.md` | 15 类跨环节断点追单卡 |
| `references/r6-sales-talk-ai-guidance.txt` | 旧版销售话术 AI 指令（参考） |

## 安装

1. 将整个 `susu5-sales-followup-advisor` 文件夹复制到 skills 目录：
   - Windows: `C:/Users/<用户名>/.workbuddy/skills/`
   - macOS / Linux: `~/.workbuddy/skills/`
2. 确认路径为 `.../skills/susu5-sales-followup-advisor/SKILL.md`（不要多嵌套同名文件夹）
3. 重新加载或新建对话后使用

## 通用调用话术

> 请调用 `$susu5-sales-followup-advisor`，先检查并读取【聊天记录】和【用户基础信息】，结合固定资料生成当前客户的事实分析、正确A链路和一条可直接发送的销售话术；如资料不全，仅提醒先补齐资料，不继续分析。

## 版本

- v01 | 2026-08-22

## 许可证

CC-BY 4.0
