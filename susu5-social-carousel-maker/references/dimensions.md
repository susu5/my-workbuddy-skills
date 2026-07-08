# Dimension Presets

Use these as controlled size presets. Show likely platform uses to the user before confirmation.

| ID | Target Size | Ratio | Image2 Canvas | Common Uses | Notes |
|---|---:|---:|---:|---|---|
| SIZE-XHS-3-4 | 1242x1660 or 1080x1440 | 3:4 | 1088x1456 | Xiaohongshu multi-image notes, knowledge cards, product seeding | Best default for Rednote/Xiaohongshu image posts. |
| SIZE-SOCIAL-4-5 | 1080x1350 | 4:5 | 1088x1360 | Xiaohongshu, Instagram, feed cards, friend circles | Balanced vertical feed format. |
| SIZE-SQUARE-1-1 | 1080x1080 | 1:1 | 1024x1024 or 2048x2048 | WeChat article images, social cards, product cards, profile grids | Safest universal format. |
| SIZE-VERTICAL-9-16 | 1080x1920 | 9:16 | 1088x1936 or 2160x3840 | Video Account cover, Douyin/Kuaishou cover, story image, phone poster | Leave top/bottom safe area. |
| SIZE-LANDSCAPE-16-9 | 1920x1080 | 16:9 | 2048x1152 or 3840x2160 | PPT cover, video thumbnail, desktop presentation, article hero | Best for horizontal viewing. |
| SIZE-DESKTOP-16-10 | 1920x1200 | 16:10 | 1920x1200 or 2560x1600 | Desktop wallpaper, software cover, wide visual card | Good for UI and productivity visuals. |
| SIZE-A4-POSTER | 2480x3508 | A4 | 1536x2176 | Printable poster, PDF page, course handout | Keep text large; avoid dense body copy. |
| SIZE-LONG-MOBILE | 1080x2340 | long vertical | 1088x2368 | Long mobile poster, process summary, timeline | Use section bands; avoid one long undivided layout. |
| SIZE-WECHAT-STICKER-ARTICLE | 900x500 | 1.8:1 | 1536x864 | WeChat article inline image, Video Account article sticker/cover insert | Good for horizontal graphic inserts. |
| SIZE-BANNER-WIDE | 1600x900 | 16:9 | 2048x1152 | Website banner, desktop article cover, event header | Use sparse text and strong visual anchor. |

Rules:

- Present the target size and Image2 canvas separately.
- If the exact target size is not supported, generate at the closest Image2 canvas and crop/resize locally if needed.
- Keep all images in one carousel on the same target ratio unless the user explicitly asks for platform adaptation.
- For text-heavy images, prefer `SIZE-XHS-3-4`, `SIZE-SOCIAL-4-5`, or `SIZE-SQUARE-1-1`.

