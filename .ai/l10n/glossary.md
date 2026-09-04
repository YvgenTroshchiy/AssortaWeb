# L10n glossary - the Assorta site

Pasted verbatim into every translation request run by `/localize`. The keys live in `i18n/*.json`
and render into `index.html` and `delete-account.html`; `build.py` substitutes them and strips the
markers. Privacy and Terms are English only and have no keys.

## Read the app's glossary first

`../AssortaKMP/.ai/l10n/glossary.md` is the source of truth for the product's vocabulary, and the
app has already shipped every one of these locales. **A word the app already renders is not
re-decided here** - the visitor reads the page and then opens the app, and two words for the same
thing is the defect users actually notice. The senses that bite hardest on this page:

- **sort / sorting / a sort** - deciding which group a saved item belongs to, and putting it there.
  Never ordering a list A-Z. Countable: "15 free AI sorts left" is a quota of filing operations.
- **group** - the container an item is filed into. Not a group of people.
- **note** - any saved item, pasted text or link alike.
- **file / files it / lands in** - placing an item into its group. Not a document file.
- **AI Summary** - the feature name. One rendering, used in every key that mentions it, and it must
  match the app's `note_summary_*` and the store listing.
- **share sheet** - the OS share menu. Use the word iOS and Android use in that locale.
- **Auto** - cars and vehicles, never "automatic".

The `group.*` keys are **not translated by hand**: `tools/sync-from-app.py` copies them out of the
app's `information_tag_*` strings. Leave whatever is already in the file. The exception is
`group.hobby`, which the app has no group for - translate that one.

## Brand literals - verbatim in every language

`Assorta`, `Assorta Pro`, `Pro`, `Google`, `Google Play`, `App Store`, `Apple`, `Android`, `iOS`,
`iPhone`, `iPad`, `YouTube`, `TikTok`, `Instagram`, `Firebase`, `Firebase Crashlytics`,
`Firebase Analytics`, `RevenueCat`.

`Delete my account` in `del.s2.p1` is an **email subject line we ask the visitor to type**, so it
stays English in every locale - we read that inbox in English.

## Values are HTML fragments - the part that breaks silently

Every value is the inner HTML of an element, not plain text. Copy the markup across unchanged and
translate only the words between the tags.

- **Keep every tag, in the same number**: `<span class="find">`, `<strong>`, `<em>`, `<b>`, `<li>`,
  `<ol>`, `<div class="add-bar">`, `<noscript>`.
- **Never touch an attribute**: `id="saved-group"`, `id="email-link"`, `id="email-link-2"`,
  `href="#kept"`, `href="#subscription"`, `href="privacy.html"`, `href="https://…"`,
  `class="find"`, `target`, `rel`, `aria-hidden`. The scripts look elements up by those ids, and a
  renamed one silently blanks a line on the page.
- **`&nbsp;` and `&amp;` stay as they are** - they are HTML entities, not characters.
- `python3 build.py --lint` compares tags and attributes against English and is the gate; run it
  before the detectors.

## Keys that are not prose

- `store.appstore.small` / `store.play.small` - the small line above the badge wordmark
  ("Download on the", "Get it on"). Use the exact wording of Apple's and Google's own localized
  badge artwork for that language, not a fresh translation. `App Store` and `Google Play` are set
  separately and never translated.
- `del.updated` - a date. Render it the way the locale writes dates, keeping 14 August 2026.
- `del.s1.list`, `del.s3.list`, `del.s5.list` - the app and OS paths inside them
  (`Settings → Delete account`, `Settings → Assorta Pro → Upgrade → Restore`,
  `Google Play app → profile picture → Payments & subscriptions → …`) must quote the **labels that
  locale's app and OS actually show**. Take the app's from its own `strings.xml` in that locale
  (`settings_title`, `settings_delete_account_action`, `enter_information_ai_upgrade`,
  `paywall_restore`); a translated-from-English path sends the visitor looking for a button that
  is not there.
- `del.s7.p` and `del.s2.p1` contain an empty `<a>` that JavaScript fills with the address. Do not
  put text inside it.
- `js.*` - read by the inline scripts, never rendered as HTML. Plain text only.
- `meta.title` - keep it under about 60 characters so the store of search results does not cut it;
  `meta.description` under about 155.

## Enum groups - members must stay distinct

- The `group.*` names, rendered side by side in the chip cloud. Already handled by the sync,
  except `group.hobby`, which must not collapse onto `group.inspiration` or `group.personal`.
- Share-sheet targets: Messages / Mail / Notes / Copy link / Browser / Cloud / More.
- Nav: Demo / How it works / Features / Screens / About - five links on one line, so keep each
  short. A nav item longer than roughly 16 characters starts pushing the row apart.
- Theme labels: `js.theme.toDark` / `js.theme.toLight`.

## Register and tone

This is marketing copy, not UI: it addresses the visitor directly and it is allowed to be shorter
and punchier than the app's strings. The **address form** still follows the app - de `du`,
fr `vous`, es `tú`, it `tu`, ja ですます, ko 존댓말 - so the page and the app do not switch
politeness on the same visitor. `delete-account.html` is instructional and stays plainer than the
landing page.

Where the store listing already says something (`../AssortaKMP/fastlane/metadata/<locale>/` and
`.../android/<locale>/`), reuse its wording: the visitor often arrives from that listing, and the
headline it promised should be the headline it delivers.

## Characters

`~/.claude/rules/i18n.md` owns these: `’` for every apostrophe, never `'`, `\'`, `ʼ` or `´`; the
locale's own quotation marks; and a spaced hyphen (` - `) between clauses, never an em dash.

The base copy was swept for both in the same pass, so English is clean now: if a `—` or an ASCII
`'` turns up in `i18n/en.json`, it came in with a later edit and belongs fixed there rather than
reproduced in thirty translations.
