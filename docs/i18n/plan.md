# Localizing the site

## Goal

Ship the landing page and the delete-account page in every language the app ships, each on its
own URL, with a language picker in the nav and `hreflang` wiring that lets search engines index
all of them. Privacy and Terms stay English.

## Current state

Four hand-written pages at the repo root - `index.html`, `privacy.html`, `terms.html`,
`delete-account.html` - no build step, inline CSS/JS, English only. Each carries its own copy of
the theme tokens, the toggle and the script, so a theming edit already has to sweep all four.

Visible text: index 1065 words, delete-account 978, privacy 1381, terms 1419.

## Decisions

### The locale set is the app's language set, not its resource set - 31 locales

`AssortaKMP/shared/src/commonMain/composeResources/` carries 33 resource folders, but two of them
(`values-es-rES`, `values-fr-rCA`) are 4-key region overlays over `es` and `fr`. Marketing copy has
nothing regional in it, so a `/es-es/` would be a byte-identical duplicate of `/es/` and read as
duplicate content. The site therefore ships **en + 30**:

`ar cs da de el es fi fr he hi hu id it ja ko nb nl pl pt-BR pt-PT ro ru sk sv th tr uk vi zh-CN zh-TW`

*Overturn:* the app gains a region overlay that changes product wording rather than a UI label.

### One directory per locale, English at the root

```
assorta.app/                    en - canonical, x-default
assorta.app/<locale>/           translated index
assorta.app/<locale>/delete-account.html
assorta.app/privacy.html        English only, linked from every locale
assorta.app/terms.html          English only
```

The path token is BCP-47 lowercased (`/pt-br/`, `/zh-cn/`) so two URLs can never differ only in
case; `hreflang` keeps the canonical casing (`hreflang="pt-BR"`).

The alternative - one URL with JS switching - was rejected: `hreflang` needs distinct URLs, so
Google would index English only, which is the entire point of the exercise.

**No automatic redirect by `Accept-Language`.** A crawler arriving at `/` must see English, and a
visitor who picked a language must not be bounced out of it.

### Privacy and Terms stay English

Machine-translated terms are 30 more versions of a contract that drift from the English original,
argued under Ukrainian law. Every locale links to the one English copy.
*Overturn:* a market whose law requires consumer terms in the local language.

### Templates plus a generator, output committed

Source of truth is `src/*.html` (the English page, readable and openable as-is) plus
`i18n/<locale>.json`. `build.py` writes the root pages and every locale folder. The output is
committed, so Cloudflare Pages keeps deploying plain static files with no build command and a
broken generator can never take the site down.

Translatable content is marked in the template and stripped from the output:

- `data-i18n="key"` - the element's inner HTML is the unit of translation, so inline markup
  (`<span class="find">`, `<b>`, `&nbsp;`) travels with the sentence.
- `data-i18n-attr="content:key,aria-label:key2"` - for `<meta>`, `aria-label`, `title`, `alt`.
- Strings the inline scripts need are emitted as a `window.__I18N__` object.

Relative asset paths are depth-adjusted for locale folders (`favicon.svg` -> `../favicon.svg`), so
a generated page still opens over `file://`, the reason the paths are relative in the first place.

### Group names come from the app, not from a translator

The chip cloud and the demo grid name the app's own groups, and those are already localized in all
33 app locales as `information_tag_*`. `tools/sync-groups.py` copies them into `i18n/<locale>.json`
under `group.*`, so the site can never call a group something the app does not.

Two site chips have no exact app key: the site says *Shopping* where the app says *Shopping list*,
and *Movies* where the app says *Movies & TV*. The site adopts the app's wording.

## Slices

- [x] **S1 - build system.** `src/` templates, `build.py`, `i18n/en.json`, output byte-equivalent
      to today's English site. No visible change.
- [x] **S2 - picker, hreflang, sitemap.** Language control in the nav on all four pages, `hreflang`
      and `canonical` on every page, sitemap listing every locale URL. Ukrainian as the pilot
      locale, proving the pipeline end to end.
- [x] **S3 - group names.** `tools/sync-groups.py` and the `group.*` keys wired into the chips and
      the demo script.
- [x] **S4 - index in the remaining 29 locales.**
- [x] **S5 - delete-account in all 30.**
- [x] **S6 - RTL.** `dir="rtl"` for `ar` and `he`. Every directional rule in the four templates
      is a logical property now, so the page mirrors whole - the phone mockups included, which is
      right, because the app mirrors in those languages too. The play triangle keeps its physical
      nudge: it points the way the video runs, not the way the text does.
- [ ] **S7 - FAQ section.** Answers to what the app does, with `FAQPage` structured data, plus
      `SoftwareApplication` and `Organization` - for search and for AI answer engines. Questions
      drafted in [faq-draft.md](faq-draft.md); they need a yes before the translation round,
      because they add about 25 keys to every locale.

## Found on the way, not fixed

Three things this pass surfaced and deliberately left alone, because each is a change to the
English copy or to the app rather than to the translation.

- `index.html` claims **thirteen languages** in the "Yours to look at" feature card; the app ships
  31. Every locale now faithfully repeats "thirteen", and the store listings say 29, so all three
  numbers disagree. One word in `src/index.html` plus a top-up of that key in 30 files.
- **The English copy breaks the dash and apostrophe rules.** `detect.py` reports 23 errors and 6
  warnings, all on `en`: em dashes throughout and ASCII `'`. Every translation is clean, so the
  base is now the only thing failing the gate.
- **The app ships two words for "sort" in three languages.** ja (仕分け vs 分類), id (`penyortiran`
  vs `pengelompokan`) and tr (`yapay zekâ sıralaması` vs `AI sınıflandırması`) each use one word in
  `enter_information_*` and another everywhere else. The site picked the dominant one; the fix
  belongs in `AssortaKMP`.
