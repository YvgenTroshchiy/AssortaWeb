# AssortaWeb

Marketing landing page for [Assorta](../AssortaKMP) — a fast, AI-sorted
inbox for notes and links (Android, iOS).

Four self-contained pages — `index.html`, `privacy.html`, `terms.html`,
`delete-account.html`: no build step, no external assets, inline CSS/JS, brand
colors and logo taken from `AssortaKMP/brand/`.

The only files the pages load from the server are the favicons at the root —
`favicon.svg` (what Chrome shows in the tab), `favicon-32.png` (fallback for
browsers without SVG icon support) and `favicon-180.png` (iOS home screen).
They are copies of the same files in `AssortaKMP/webApp/src/webMain/resources/`,
generated from `AssortaKMP/brand/logo-icon-favicon.svg`; a new page must carry
the same three `<link>` tags. The paths are **relative** (`favicon.svg`, not
`/favicon.svg`) so that the icon also shows when a page is opened straight from
disk over `file://` — every page lives in the root, so nothing nests.

## Theming

All four pages support light and dark, matching the app. The palette mirrors
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

Every page carries its own copy of the theme tokens, the toggle and the script
(`index.html` has the full palette, the three text pages a 19-variable subset) —
when editing the theming on one page, sweep all four.

## llms.txt

`llms.txt` is the Markdown summary AI agents read at `https://assorta.app/llms.txt`
([spec](https://llmstxt.org)). It has to open with an H1 and carry Markdown links,
or Lighthouse's Agentic Browsing audit fails it. Without the file that URL served
`index.html` — Cloudflare answers unknown paths with the landing page — so the audit
saw HTML with no H1 and no links. Keep its links and the pre-release wording in step
with `index.html`.

## security.txt

`security.txt` is the RFC 9116 contact file telling security researchers where to
report a vulnerability ([spec](https://www.rfc-editor.org/rfc/rfc9116)). It points
at `contact@assorta.app`.

It sits at the repo root rather than in `.well-known/`, where the spec puts it,
because Cloudflare Pages does not deploy directories whose names begin with a dot.
Left there it would have hit the same trap as the missing `llms.txt`: the URL
answers with `index.html` at status 200, so the file looks present until you check
the content type. `_redirects` maps `/.well-known/security.txt` onto the root copy,
since scanners look under the canonical path first.

`Expires` is a required field and is set to **2027-07-01**. Past that date the file
reads as stale and should be reissued.

Note that the address is in plain text here, unlike `privacy.html`, which assembles
it in JS to keep it out of the page source. A security contact that a scraper cannot
read is useless, so the anti-scraping trick is deliberately not applied.

## The operator address and Cloudflare email obfuscation

`index.html`, `privacy.html` and `terms.html` name the operator (`Individual Entrepreneur
Yevhen Troshchii, Odesa, Ukraine`) with `contact@assorta.app` in plain text. That address has
to be readable without JavaScript: a Google Ads policy reviewer looks for contact information
in the page source, and the account was suspended once under Unacceptable business practices
with the site carrying no contact details a crawler could see.

Cloudflare's Scrape Shield rewrites any plain address it finds into `[email protected]` plus a
JS decoder, which reintroduces exactly that problem. The three operator blocks are therefore
wrapped in `<!--email_off--> … <!--email_on-->`, the documented opt-out. Keep the markers on any
new plain-text address, and do not "clean them up" as stray comments.

The JS-assembled `email-link` used elsewhere on those pages stays as it is - it is an
anti-scraping measure for the general contact link, and each occurrence has a `<noscript>`
fallback spelling the address out.

## robots.txt and sitemap.xml

`robots.txt` opens the whole site to crawlers and names the sitemap; `sitemap.xml`
lists the two real pages. Nothing here is restrictive — they exist because their
absence was, again, the catch-all trap: `/robots.txt` answered with `index.html`
at status 200, so Lighthouse read 958 lines of HTML as crawl directives and failed
the audit with "robots.txt is not valid".

Add a `<url>` entry whenever a page is added, and keep the `Sitemap:` line and the
`<loc>` values on the apex domain — they must be absolute and must match the host
the file is served from.

## Preview

Open `index.html` in a browser, or serve the folder:

```sh
python3 -m http.server 8080
```

## Before going live

- [ ] Replace the placeholder store badges (`.store-badge`) with the official
      App Store / Google Play badge artwork. Both store URLs are real.
- [ ] Add analytics (if wanted) and a favicon/OG image.
- [ ] Hook up hosting (Firebase Hosting fits the existing project setup).

Store listing texts, slogans, and ASO notes live in the main repo:
`AssortaKMP/docs/marketing/aso.md`.
