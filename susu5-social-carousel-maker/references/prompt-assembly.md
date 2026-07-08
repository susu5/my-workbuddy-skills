# Prompt Assembly

Every image2 call must use a complete final prompt.

## Formula

```text
final_image_prompt =
  engine_rule
+ dimension_preset
+ page_role
+ confirmed_page_copy
+ selected_visual_style
+ selected_image_template
+ composition_rule
+ carousel_consistency_rule
+ avoid_list
```

## Required Output Per Image

Before generation, prepare a prompt record:

```yaml
page: 1
page_role: PAGE-COVER
dimension_id: SIZE-XHS-3-4
style_id: STYLE-KNOWLEDGE-CARD
image_template_id: TEMPLATE-COVER-HOOK-01
target_size: 1080x1440
image2_canvas: 1088x1456
final_image_prompt: |
  ...
```

## Final Prompt Skeleton

```text
Use case: social media carousel image
Generation engine: image2 / gpt-image-2

Platform/use: {platform_use}
Canvas: {image2_canvas}
Target size: {target_size}
Target ratio: {target_ratio}

Page role: {page_role}
Page number: {page_number}
Topic: {topic}
Audience: {audience}
Page objective: {page_objective}

Exact text to include:
Title: "{title}"
Subtitle: "{subtitle}"
Body:
- "{body_1}"
- "{body_2}"
- "{body_3}"

Visual style template:
{style_prompt_clause}

Image layout template:
{image_template_prompt_clause}

Composition:
{composition_rule}

Typography:
Mobile-readable Chinese typography, clear hierarchy, large title, short body text, no dense paragraphs.

Consistency rules:
This image belongs to the same carousel set. Keep the same palette, typography feeling, margin density, background treatment, icon style, and visual rhythm across all pages.

Avoid:
watermark, QR code, fake logo, fake app UI, page number, signature, random English words, distorted Chinese text, tiny unreadable text, extra unrequested captions, excessive decoration.
```

## Text Handling Rules

- Quote exact in-image text.
- Keep Chinese text short; image models may distort dense text.
- If exact text fidelity is critical, reduce text and use stronger hierarchy.
- Do not add extra slogans.
- If a page has more than 5 bullets, split the page.

## Sample Prompt

```text
Use case: social media carousel image
Generation engine: image2 / gpt-image-2

Platform/use: Xiaohongshu multi-image note
Canvas: 1088x1456
Target size: 1080x1440
Target ratio: 3:4

Page role: PAGE-COVER
Page number: 01
Topic: AI tools improve sales follow-up efficiency
Audience: sales managers, sales operations, startup teams
Page objective: use a strong hook to earn the click

Exact text to include:
Title: "销售跟进慢，其实不是人的问题"
Subtitle: "3 个自动化动作，让客户不再被漏掉"
Body:
- "优先级提醒"
- "每日跟进清单"
- "状态变化追踪"

Visual style template:
Clean Xiaohongshu knowledge-card style, light background, modular content blocks, large Chinese headline, one bright accent color, strong hierarchy, high mobile readability.

Image layout template:
Large headline in the upper-middle safe area, short subtitle below, three keyword chips near the lower-middle area, simple visual anchor related to the topic, generous safe margins, cover-like click appeal.

Composition:
Strong vertical card composition. The headline is dominant. Use one simple workflow/calendar/customer-card visual metaphor, not a busy office scene.

Typography:
Mobile-readable Chinese typography, clear hierarchy, large title, short body text, no dense paragraphs.

Consistency rules:
This image belongs to the same carousel set. Keep the same palette, typography feeling, margin density, background treatment, icon style, and visual rhythm across all pages.

Avoid:
watermark, QR code, fake logo, fake app UI, page number, signature, random English words, distorted Chinese text, tiny unreadable text, extra unrequested captions, excessive decoration.
```

