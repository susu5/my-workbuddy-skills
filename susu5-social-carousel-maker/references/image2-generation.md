# Image2 Generation Rules

Use image generation only after page content, size, and style are confirmed.

## Execution Policy

- Default to Codex built-in image generation for normal image creation.
- If the user explicitly asks for image2, gpt-image-2, API, or CLI, use the imagegen skill fallback path for gpt-image-2.
- Do not create custom one-off OpenAI image API scripts.
- Use one prompt per image.
- Generate 3 samples first: cover plus 2 content pages.
- Generate the full set only after sample approval.

## Image2 Size Notes

For gpt-image-2 fallback:

- Use `quality low` or equivalent draft settings for quick samples when the user wants speed.
- Use medium/high/auto for final assets, dense text, diagrams, or polished deliverables.
- Prefer Image2 canvas sizes from `dimensions.md`.
- Keep max edge <= 3840, dimensions as multiples of 16, and long-to-short ratio <= 3:1 when using explicit gpt-image-2 sizes.

## Batch Strategy

Do not batch distinct pages into one prompt. For a 9-page carousel, create 9 prompt records and generate 9 images.

For the sample gate, only generate:

1. Page 1 cover.
2. First content page.
3. Second content page.

After sample approval, reuse the approved style and prompt pattern for remaining pages.

## Validation After Generation

Check:

- Does the image match the selected size/ratio?
- Is the text readable on mobile?
- Is the title close to the exact requested text?
- Does the page role match the image layout?
- Does the style match the approved sample?
- Are there watermarks, fake logos, QR codes, or random text?
- Does the image feel like part of the same carousel?

If text is distorted:

1. Shorten in-image text.
2. Increase title size and reduce body copy.
3. Regenerate only that page.

