# AssortaWeb Agent Guidelines

Marketing landing page for Assorta. Hand-written static site: `index.html`, `privacy.html`,
`terms.html`, `delete-account.html` - no build step, no framework, inline CSS/JS.

## Related projects

- Landing page root: this repository (`AssortaWeb`)
- Mobile app root: the sibling `../AssortaKMP` repository - brand assets and the semantic color
  palette the page mirrors come from there
- Treat them as separate Git repositories.

## Where the rules live

Claude Code loads the global rules through `CLAUDE.md`; **every other agent must read these files
directly** - they live outside this repository, in the user's home directory.

**Global, applies to every project - [`~/.claude/rules/`](.ai/global-rules)**

- [`~/.claude/rules/instructions.md`](.ai/global-rules/instructions.md) - where a durable instruction gets written down
- [`~/.claude/rules/communication.md`](.ai/global-rules/communication.md)
- [`~/.claude/rules/git.md`](.ai/global-rules/git.md)
- [`~/.claude/rules/planning.md`](.ai/global-rules/planning.md)
- [`~/.claude/rules/comments.md`](.ai/global-rules/comments.md)
- [`~/.claude/rules/naming.md`](.ai/global-rules/naming.md)
- [`~/.claude/rules/i18n.md`](.ai/global-rules/i18n.md)

**Global, this stack - [`~/.claude/stacks/web.md`](.ai/global-stacks/web.md)**

Empty placeholder: no reusable web rules have been written yet.

**This project only**

There is no `.ai/rules/` folder yet. Existing project conventions are in [README.md](README.md) -
the theming setup, and the rule that `index.html` and `privacy.html` each carry their own copy of the
theme tokens, toggle and script, so both must be updated together. Read it before editing markup or
styles.

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
