# AssortaWeb Agent Guidelines

Marketing landing page for Assorta. Hand-written static site: `index.html`, `privacy.html`,
`terms.html`, `delete-account.html` - no build step, no framework, inline CSS/JS.

## Related projects

- Landing page root: this repository (`AssortaWeb`)
- Mobile app root: the sibling `../AssortaKMP` repository - brand assets and the semantic color
  palette the page mirrors come from there
- Treat them as separate Git repositories.

## Where the rules live

Claude Code loads the global rules through `CLAUDE.md`; **every other agent must read them
directly** - they live outside this repository, in the user's home directory.

**Global, applies to every project - every `.md` in [`~/.claude/rules/`](.ai/global-rules)**

List that directory and read everything in it, rather than trusting a list of filenames written
here: such a list goes stale the moment a rule is added, and the rule nobody copied into it is the
rule nobody reads. The global entry point for agents outside a repository is `~/.claude/AGENTS.md`.

**Global, this stack - [`~/.claude/stacks/web.md`](.ai/global-stacks/web.md)**

Empty placeholder: no reusable web rules have been written yet.

**This project only**

There is no `.ai/rules/` folder yet. Existing project conventions are in [README.md](README.md) -
the theming setup, and the rule that every page (`index.html`, `privacy.html`, `terms.html`,
`delete-account.html`) carries its own copy of the theme tokens, toggle and script, so a theming
edit must sweep all four. Read it before editing markup or styles.

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
