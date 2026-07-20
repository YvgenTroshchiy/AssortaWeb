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
the app's own `theme_mode` key). The phone mockups in the Screens carousel are
product shots of the app's light UI and stay light in both themes.

`index.html` and `privacy.html` each carry their own copy of the tokens, the
toggle and the script — keep the two in sync when editing either.

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
