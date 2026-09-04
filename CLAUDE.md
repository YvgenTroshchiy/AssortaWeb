# AssortaWeb - Project Guidelines

Marketing landing page for Assorta. Hand-written static site - no framework, inline CSS/JS, and
nothing to install to work on it.

**The four pages at the repo root are generated. Edit `src/`.** `build.py` renders them plus one
directory per language, from `src/*.html` and `i18n/<locale>.json`; the output is committed, so
Cloudflare Pages still deploys plain static files with no build command. Run `python3 build.py`
after any edit and `python3 build.py --check` to prove the committed output is current.

## Where the rules live

| Layer | Where | How it loads |
| --- | --- | --- |
| Global, always-on | [`~/.claude/rules/`](.ai/global-rules) | automatically in every project - communication, git, planning, testing, comments, naming, i18n |
| Global, this stack | [`~/.claude/stacks/web.md`](.ai/global-stacks/web.md) | **empty placeholder** - no reusable web rules written yet, so nothing is imported here |
| This project only | `.ai/rules/` | does not exist yet - create it when a rule is worth writing down |

The always-on rules are **not** copied into this repository on purpose: one shared copy in
[`~/.claude/rules/`](.ai/global-rules) is the whole point, and a second copy would drift out of sync within weeks.

Project conventions that already exist are documented in [README.md](README.md) - the build and the
language layout, the theming setup, and the rule that every page (`src/index.html`,
`src/privacy.html`, `src/terms.html`, `src/delete-account.html`) carries its own copy of the theme
tokens, the toggle, the picker and their scripts, so an edit to any of those must sweep all four.
Read it before editing markup or styles.

Localization has its own plan and its decisions in [docs/i18n/plan.md](docs/i18n/plan.md), and its
translator config in `.ai/l10n/` (`glossary.md`, `detectors.json`) - the `/localize` skill reads
both.

When a rule shows up that a *second* web project would also want (markup and asset structure,
SEO/`sitemap.xml`/`llms.txt` upkeep, deploy and redirect handling, accessibility baseline), put it in
[`~/.claude/stacks/parts/`](.ai/global-stacks/parts) and import it from [`~/.claude/stacks/web.md`](.ai/global-stacks/web.md) instead of writing it here.

## Skills

The commit skill is **global**, at `~/.claude/skills/commit/SKILL.md`.

## Global rule symlinks

`.ai/global-rules` and `.ai/global-stacks` are **gitignored symlinks** to `~/.claude/rules` and
`~/.claude/stacks`. They exist only so the links to the global rules above open on click in the IDE -
nothing depends on them at build time, and Claude Code loads the same files through the `~`-paths
regardless. On a fresh clone they are absent; recreate them with:

```bash
ln -s ~/.claude/rules .ai/global-rules && ln -s ~/.claude/stacks .ai/global-stacks
```
