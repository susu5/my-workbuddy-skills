---
name: susu5-social-carousel-maker
description: "Create confirmed multi-image social carousel content from articles, topics, product notes, or raw ideas. 根据文章、主题、产品信息或粗略想法，生成小红书/Rednote、微信图文、视频号封面、海报等社媒多图内容；包含内容提炼、逐页文案拆解、用户确认、尺寸选择、视觉风格选择、图片模板匹配、最终 image2 提示词合成、3 张小样生成确认，以及确认后完整多图生成。"
---

# Susu5 Social Carousel Maker

Produce a controlled multi-image social carousel workflow. Treat the skill as a content director plus image2 prompt assembler, not as a one-shot image generator.

## Hard Gates

Never skip these gates:

1. Confirm the page-by-page content plan before size selection.
2. Confirm the target size before style selection.
3. Confirm the visual style before image generation.
4. Generate only 3 sample images first: 1 cover and 2 content pages.
5. Generate the full image set only after the user approves the 3 samples.

Do not call image2 with only page copy or only a style name. Always assemble each final prompt from confirmed page content, selected size, selected visual style template, selected image layout template, and global carousel consistency rules.

## Workflow

### Step 1 - Interpret the Input

Accept articles, notes, rough themes, product descriptions, campaign briefs, course content, or user stories. Extract:

- topic
- audience
- platform/use case
- content objective
- core message
- supporting proof or examples
- required claims and forbidden claims
- desired tone

If information is missing but work can continue, make explicit assumptions. If a gap affects structure, ask 1-3 focused questions.

### Step 2 - Build the Page Plan

Read `references/carousel-structures.md` and `references/page-roles.md`. Choose a structure based on the content type, then produce a page-by-page plan.

Each page must include:

- page number
- page role id
- page objective
- in-image title
- in-image subtitle or body bullets
- visual idea
- recommended image template id
- risk or note, if any

Stop and ask the user to confirm or revise the page plan. Do not show size choices yet unless the user asks.

### Step 3 - Select Size

After page plan approval, read `references/dimensions.md`. Present 4-8 relevant size options with common uses. Recommend one primary size and explain why.

If the user is unsure, default to:

- Xiaohongshu multi-image note: `SIZE-XHS-3-4`
- Video Account cover or vertical poster: `SIZE-VERTICAL-9-16`
- WeChat article image or general social card: `SIZE-SQUARE-1-1`
- Desktop/PPT/landscape cover: `SIZE-LANDSCAPE-16-9`

Stop and ask the user to confirm the size.

### Step 4 - Select Visual Style

After size approval, read `references/style-templates.md`. Recommend 3-5 styles based on topic, audience, and platform. Show each with: best for, visual feel, strength, and caution.

If the user wants a custom mix, combine at most two styles. Preserve one primary style as the global visual anchor.

Stop and ask the user to confirm the style.

### Step 5 - Assemble Final Prompts

After style approval, read:

- `references/image-templates.md`
- `references/prompt-assembly.md`
- `references/image2-generation.md`

For the cover and the first two content pages, assemble complete `final_image_prompt` entries. Each final prompt must include:

- image2 generation rule
- platform/use
- canvas and target size
- page role and page objective
- exact in-image text
- selected visual style template
- selected image layout template
- composition rules
- carousel consistency rules
- avoid list

Use one prompt per image. Never ask image2 to generate the whole carousel in a single image.

### Step 6 - Generate 3 Samples

Use Codex image generation. Default to the built-in image generation capability. If the user explicitly asks for image2, gpt-image-2, API, or CLI, follow the imagegen skill fallback path for gpt-image-2; do not create a custom API script.

Generate:

- page 1 cover
- first approved content page
- second approved content page

Inspect outputs for text accuracy, composition, readability, style consistency, and platform suitability. Ask the user to approve or request adjustments.

### Step 7 - Generate Full Carousel

Only after sample approval:

1. Assemble final prompts for every remaining page.
2. Generate one image per page.
3. Keep the same visual system across the set.
4. Save or present outputs according to the user's requested destination.

### Step 8 - Deliver Publishing Pack

Deliver:

- final image list
- final prompt list or prompt summary
- suggested title options
- caption/body copy
- hashtags/topics
- quality checklist notes
- any unsupported or risky claims

## Reference Loading Order

1. `carousel-structures.md` and `page-roles.md` for planning.
2. `dimensions.md` after content approval.
3. `style-templates.md` after size approval.
4. `image-templates.md`, `prompt-assembly.md`, and `image2-generation.md` before sample generation.
5. `quality-checklist.md` before delivery.

## Resource Map

```
susu5-social-carousel-maker/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── carousel-structures.md
│   ├── dimensions.md
│   ├── image-templates.md
│   ├── image2-generation.md
│   ├── page-roles.md
│   ├── prompt-assembly.md
│   ├── quality-checklist.md
│   └── style-templates.md
└── scripts/
    └── validate-carousel-plan.mjs
```
