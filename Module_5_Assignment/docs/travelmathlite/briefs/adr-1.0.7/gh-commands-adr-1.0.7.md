# GitHub CLI Commands for ADR-1.0.7 Implementation

Use these commands to create Issues tied to ADR-1.0.7 (Static, media, and asset pipeline) before picking up each brief. Always capture the Issue numbers for commit/issue-comment sync.

---

## Prerequisites

```bash
# Check available labels FIRST
gh label list

# Stay current on FALL2025
git checkout FALL2025
git pull origin FALL2025
```

---

## Create Issues per Brief

### Brief 01: Static/media folders + base template

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.7-01: Static/media folders and base asset wiring" \
  -b "**Goal:** Configure STATIC/MEDIA directories plus base template asset references so Bootstrap and branding load from local files.\n\n**Scope:** PRD §4 F-007/F-010; §7 NF-004. Files: `travelmathlite/core/settings.py`, `travelmathlite/templates/base.html`, `travelmathlite/static/`.\n\n**Acceptance:** Local assets replace CDN links, collectstatic writes to STATIC_ROOT, docs updated.\n\n**Brief:** docs/travelmathlite/briefs/adr-1.0.7/brief-ADR-1.0.7-01-static-folders-and-base-template.md" \
  -l feature,FR,travelmathlite)
ISSUE_STATIC=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_STATIC}"
```

### Brief 02: WhiteNoise + manifest config

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.7-02: WhiteNoise and manifest storage" \
  -b "**Goal:** Add WhiteNoise middleware and ManifestStaticFilesStorage for hashed assets in production.\n\n**Scope:** PRD §4 F-010; §7 NF-004. Files: `core/settings.py`, `core/wsgi.py`, `pyproject.toml`.\n\n**Acceptance:** collectstatic builds hashed files; DEBUG=False uses WhiteNoise.\n\n**Brief:** docs/travelmathlite/briefs/adr-1.0.7/brief-ADR-1.0.7-02-whitenoise-manifest-prod-config.md" \
  -l feature,FR,NF,travelmathlite)
ISSUE_WHITENOISE=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_WHITENOISE}"
```

### Brief 03: Media + avatar upload flow

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.7-03: Media handling and avatar upload" \
  -b "**Goal:** Implement optional avatar uploads stored under MEDIA_ROOT with env gating.\n\n**Scope:** PRD §4 F-007; §7 NF-004. Files: `apps/accounts/`, `core/settings.py`, docs.\n\n**Acceptance:** Profile form saves avatars when allowed; files stored under media/avatars.\n\n**Brief:** docs/travelmathlite/briefs/adr-1.0.7/brief-ADR-1.0.7-03-media-and-avatar-upload-flow.md" \
  -l feature,FR,NF,travelmathlite,accounts)
ISSUE_MEDIA=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_MEDIA}"
```

### Brief 04: Collectstatic automation + docs

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.7-04: Collectstatic automation and docs" \
  -b "**Goal:** Script collectstatic via uv and document the operator workflow.\n\n**Scope:** PRD §7 NF-004. Files: `scripts/collectstatic.sh`, docs/ops, README.\n\n**Acceptance:** Single command runs collectstatic; docs updated with troubleshooting guidance.\n\n**Brief:** docs/travelmathlite/briefs/adr-1.0.7/brief-ADR-1.0.7-04-collectstatic-automation-and-docs.md" \
  -l chore,docs,NF,travelmathlite)
ISSUE_DOCS=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_DOCS}"
```

### Brief 05: Tests + visual attestation

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.7-05: Static/media tests and visual checks" \
  -b "**Goal:** Add Django tests plus Playwright evidence proving hashed assets + avatars work.\n\n**Scope:** PRD §4 F-007/F-010; §7 NF-004. Files: app tests, scripts/visual_checks, screenshots.\n\n**Acceptance:** Tests cover INV-1/INV-2; Playwright artifacts stored under screenshots/static-pipeline.\n\n**Brief:** docs/travelmathlite/briefs/adr-1.0.7/brief-ADR-1.0.7-05-static-media-tests-and-visual-checks.md" \
  -l test,FR,NF,travelmathlite)
ISSUE_TESTS=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_TESTS}"
```

---

## Workflow Tips

```bash
# Issues-only workflow example
ISSUE_NUM=<paste-number>
COMMIT_MSG="feat: configure static folders — Refs #${ISSUE_NUM}"
git add -A
git commit -m "$COMMIT_MSG"
gh issue comment "$ISSUE_NUM" -b "$COMMIT_MSG"

# Branch-per-issue workflow
gh issue develop ${ISSUE_NUM} --base FALL2025
git switch $(git branch --show-current)
```

- Mirror commit messages as Issue comments; final commit that closes the Issue should use `Closes #N` when merging to FALL2025.
- Attach collectstatic transcripts and screenshots to the ADR evidence folder referenced in `docs/travelmathlite/ops/static-and-media.md`.
