# AssortaWeb

Marketing landing page for [Assorta](../AssortaKMP) — a fast, AI-sorted
inbox for notes and links (Android, iOS, Web).

The page is a single self-contained `index.html`: no build step, no external
assets, inline CSS/JS, brand colors and logo taken from `AssortaKMP/brand/`.

## Theming

Both pages support light and dark, matching the app. The palette mirrors
`AssortaKMP/.../ui/theme/SemanticColor.kt` — dark is the CSS default (so it
survives JS being off), light overrides it under `:root[data-theme="light"]`.
An inline script in `<head>` stamps `data-theme` before first paint: it follows
`prefers-color-scheme` until the visitor uses the nav toggle, after which the
choice is remembered in `localStorage` under `assorta-theme` (deliberately not
the app's own `theme_mode` key).

The phone mockups in the Screens carousel follow the theme too, via the `--app-*`
tokens. Those mirror the app's semantic colors: where the app has a token
(`fgPrimary`, `bgCard`, `accentPrimary`, …) it is used in both themes; where it
has none (OS status bar, the iOS share sheet, image placeholders) the light value
reproduces what the mockups rendered before, so only the dark case is new. Tag
hues are user data and identical in the app's two palettes, so they are never
themed - including the low-luminance ones like Stone `#78716C` on the Auto group,
which stays dim on dark exactly as it does in the app.

`index.html` and `privacy.html` each carry their own copy of the tokens, the
toggle and the script — keep the two in sync when editing either.

## llms.txt

`llms.txt` is the Markdown summary AI agents read at `https://assorta.app/llms.txt`
([spec](https://llmstxt.org)). It has to open with an H1 and carry Markdown links,
or Lighthouse's Agentic Browsing audit fails it. Without the file that URL served
`index.html` — Cloudflare answers unknown paths with the landing page — so the audit
saw HTML with no H1 and no links. Keep its links and the pre-release wording in step
with `index.html`.

## Preview

Open `index.html` in a browser, or serve the folder:

```sh
python3 -m http.server 8080
```

## Before going live

- [ ] Replace the placeholder store badges (`.store-badge`) with the official
      App Store / Google Play badge artwork and real store URLs.
- [ ] Point "try the web app" at the deployed web app URL.
- [ ] Add analytics (if wanted) and a favicon/OG image.
- [ ] Hook up hosting (Firebase Hosting fits the existing project setup).

Store listing texts, slogans, and ASO notes live in the main repo:
`AssortaKMP/docs/marketing/aso.md`.
