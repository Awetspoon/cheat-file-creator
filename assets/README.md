# Brand Assets

This folder contains runtime images and retained brand-source files for Cheat Editor Manager Tool.

## Runtime Assets Used By The App

- `app-icon.ico` - executable and Windows title-bar icon.
- `icon-256.png` - Tk window icon image.
- `app-icon.png` - fallback Tk window icon image.
- `mark-48.png` - compact header mark.

The runtime header intentionally uses `mark-48.png` plus code-native text.
Do not reintroduce `wordmark-360.png`, `logo-header.png`, or watermark
images into the top-left header.
Only the four runtime assets above are bundled into the Windows executable.

## README Screenshot

- `app-fullscreen.png` - current full-app screenshot used by the project README.

## Retained Brand Source Files

- `icon-master.png`
- `icon-16.png`, `icon-32.png`, `icon-48.png`, `icon-64.png`, `icon-96.png`,
  `icon-128.png`, `icon-256.png`, `icon-512.png`
- `mark-96.png`
- `wordmark.png`, `wordmark-360.png`
- `primary-logo.png`, `logo-wide.png`
- `secondary-logo.png`, `logo-header.png`
- `logomark.png`
- `watermark-brand.png`, `watermark.png`, `watermark-ui.png`
- `logo-square.png`
- `splash-1366x768.png`, `splash-1920x1080.png`, `social-card.png`

Some files are intentional aliases with identical image content. The friendly
names (`primary-logo.png`, `secondary-logo.png`, `watermark-brand.png`,
`wordmark.png`, `logomark.png`) are kept because they are easier to understand
in documentation and future packaging work.

## Generated QA Images

Temporary screenshots and preview images belong in `build/`, not in this folder.

## Regenerate Assets

Run:

```bash
python assets/generate_brand_assets.py
```
