# AssortaWeb

Marketing landing page for [Assorta](../AssortaKMP) — a fast, AI-sorted
inbox for notes and links (Android, iOS, Web).

The page is a single self-contained `index.html`: no build step, no external
assets, inline CSS/JS, brand colors and logo taken from `AssortaKMP/brand/`.

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
