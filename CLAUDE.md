# AssortaWeb - Project Guidelines

Marketing landing page for Assorta. Hand-written static site: `index.html`, `privacy.html`,
`terms.html`, `delete-account.html` - no build step, no framework, inline CSS/JS.

## Where the rules live

| Layer | Where | How it loads |
| --- | --- | --- |
| Global, always-on | [`~/.claude/rules/`](.ai/global-rules) | automatically in every project - communication, git, planning, comments, naming, i18n |
| Global, this stack | [`~/.claude/stacks/web.md`](.ai/global-stacks/web.md) | **empty placeholder** - no reusable web rules written yet, so nothing is imported here |
| This project only | `.ai/rules/` | does not exist yet - create it when a rule is worth writing down |

The always-on rules are **not** copied into this repository on purpose: one shared copy in
[`~/.claude/rules/`](.ai/global-rules) is the whole point, and a second copy would drift out of sync within weeks.

Project conventions that already exist are documented in [README.md](README.md) - the theming setup,
and the rule that `index.html` and `privacy.html` each carry their own copy of the theme tokens,
toggle and script, so both must be updated together. Read it before editing markup or styles.

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
