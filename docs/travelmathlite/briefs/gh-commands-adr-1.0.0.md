# GH CLI commands — ADR-1.0.0 briefs

This file is a running tally of GitHub CLI commands to open Issues for each ADR-1.0.0 brief (issues-only; no branches). Run from the repo root. Adjust the base branch if needed (default here: FALL2025).

## One-time label setup (optional)

```bash
# Optional: create labels (ignore errors if they already exist)
# gh label create brief --color BFD4F2 || true
# gh label create ADR --color F9D0C4 || true
# gh label create travelmathlite --color C2F0C2 || true
```

## Create Issues for each brief

> Important
>
> - Run these commands from the repo root (`CIDM6325`). If you're in `blog_site/`, either `cd ..` first or change each `-F docs/...` path to `-F ../docs/...`.
> - If the labels don't exist, run the optional label setup below or remove the `-l` flags.
> - Issues-only mode: per your preference, these snippets DO NOT create branches; continue working on `FALL2025`.

```bash
# 01 — App scaffolding under apps/*
gh issue create \
  -t "BRIEF: ADR-1.0.0 — App scaffolding under apps/*" \
  -F docs/travelmathlite/briefs/brief-ADR-1.0.0-01-app-scaffolding.md \
  -l brief -l ADR -l travelmathlite

# 02 — Settings wiring (INSTALLED_APPS, templates)
gh issue create \
  -t "BRIEF: ADR-1.0.0 — Settings wiring (INSTALLED_APPS, templates)" \
  -F docs/travelmathlite/briefs/brief-ADR-1.0.0-02-settings-installed-apps.md \
  -l brief -l ADR -l travelmathlite

# 03 — Project URLs and namespacing
gh issue create \
  -t "BRIEF: ADR-1.0.0 — Project URLs and namespacing" \
  -F docs/travelmathlite/briefs/brief-ADR-1.0.0-03-project-urls-and-namespaces.md \
  -l brief -l ADR -l travelmathlite

# 04 — Templates organization by app
gh issue create \
  -t "BRIEF: ADR-1.0.0 — Templates organization by app" \
  -F docs/travelmathlite/briefs/brief-ADR-1.0.0-04-templates-organization.md \
  -l brief -l ADR -l travelmathlite

# 05 — Tests for URL reverse and template rendering
gh issue create \
  -t "BRIEF: ADR-1.0.0 — Tests for URL reverse and template rendering" \
  -F docs/travelmathlite/briefs/brief-ADR-1.0.0-05-tests-url-reverse-and-templates.md \
  -l brief -l ADR -l travelmathlite

# 06 — Documentation: app layout guide
gh issue create \
  -t "BRIEF: ADR-1.0.0 — Documentation: app layout guide" \
  -F docs/travelmathlite/briefs/brief-ADR-1.0.0-06-docs-app-layout.md \
  -l brief -l ADR -l travelmathlite
```

### Optional: capture the Issue number for commit tagging

If you want to tag commits with the Issue number easily, capture it when creating the Issue:

```bash
# Replace the -t/-F args for the brief you are creating
ISSUE_URL=$(gh issue create -t "BRIEF: ..." -F docs/... -l brief -l ADR -l travelmathlite)
ISSUE_URL=$(echo "$ISSUE_URL" | tail -n1)
export ISSUE_NUM=${ISSUE_URL##*/}
echo "ISSUE_NUM=$ISSUE_NUM"
```

## After implementing each brief

```bash
# You are working directly on FALL2025.
# Commit and push as usual. Include the Issue number in commits.

# Tag ongoing work against the Issue (safe, non-closing):
git add -A
git commit -m "feat: brief 01 — app scaffolding (ADR-1.0.0) Refs #${ISSUE_NUM}"
git push

# When the brief is fully done, you can optionally close the Issue via commit:
# (This auto-closes when merged into the default branch; otherwise prefer Refs #)
# git commit -m "feat: complete brief 01 — closes #${ISSUE_NUM}" && git push
```

## Notes

- The `-F` flag reads the Issue body from the corresponding brief file.
- Replace `FALL2025` with your preferred base branch (e.g., `main`) if needed.
- Labels are optional; remove `-l` flags if you don’t want to create or use labels.
- Running from a subfolder (e.g., `blog_site/`): prepend `../` to the `-F docs/...` path or `cd ..` to the repo root before running the commands.
- Branches: intentionally not created here. If you later change your mind and want one branch per Issue, reintroduce `gh issue develop "$ISSUE_NUM" --base FALL2025` after each `gh issue create` and ensure your GH CLI supports it.

- Commit messages: include the Issue reference in all commits touching the brief. Use `Refs #<num>` for ongoing work; use `Closes #<num>` only when you intend to close the Issue (on merge to the default branch).

## Template for adding more items later

```bash
# Replace placeholders with your brief title and body file path
gh issue create \
  -t "BRIEF: <ADR/feature> — <short title>" \
  -F <path-to-brief-markdown> \
  -l brief -l ADR -l travelmathlite
```
