````markdown
# GitHub CLI Commands for ADR-1.0.8 Implementation

This file provides ready-to-use GitHub CLI commands for creating Issues and managing workflow for ADR-1.0.8 (Settings configuration and secrets).

---

## Prerequisites

```bash
# Check available labels FIRST
gh label list

# Ensure you're on the correct base branch
git checkout FALL2025
git pull origin FALL2025
```

---

## Create Issues for Each Brief

### Brief 01: Settings split (base/local/prod)

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.8-01: Settings split (base/local/prod)" \
  -b "**Goal:** Split settings into `base`, `local`, and `prod`, using `django-environ` for config.

**Scope:** PRD §4 F-012; NF-003

**Files:** `project/settings/base.py`, `project/settings/local.py`, `project/settings/prod.py`

**Acceptance:**
- `base.py` contains shared settings and env parsing
- `local.py` enables `DEBUG=True`
- `prod.py` enforces `DEBUG=False` and required envs

**Brief:** docs/travelmathlite/briefs/adr-1.0.8/brief-ADR-1.0.8-01-settings-split.md" \
  -l feature,FR,travelmathlite)
ISSUE_01=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_01}"
```

### Brief 02: `.env.example` and docs

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.8-02: .env.example and settings docs" \
  -b "**Goal:** Add `.env.example` and `docs/ops/settings.md` documenting required env vars and validation steps.

**Files:** `.env.example`, `docs/ops/settings.md`

**Acceptance:** `.env.example` lists required variables and `docs/ops/settings.md` contains run/test instructions.

**Brief:** docs/travelmathlite/briefs/adr-1.0.8/brief-ADR-1.0.8-02-env-and-docs.md" \
  -l docs,travelmathlite)
ISSUE_02=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_02}"
```

### Brief 03: Prod security & WhiteNoise

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.8-03: Prod security hardening and WhiteNoise" \
  -b "**Goal:** Configure production security headers, secure cookies, and WhiteNoise static serving.

**Files:** `project/settings/prod.py`, `requirements.txt`, `docs/ops/settings.md`

**Acceptance:** `prod.py` enforces security flags and WhiteNoise is documented/added to requirements if needed.

**Brief:** docs/travelmathlite/briefs/adr-1.0.8/brief-ADR-1.0.8-03-prod-security-and-whitenoise.md" \
  -l feature,security,travelmathlite)
ISSUE_03=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_03}"
```

### Brief 04: Tests and invariants

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.8-04: Tests and invariants for settings" \
  -b "**Goal:** Add tests and reviewer checklist to verify INV-1 and INV-2 and provide quick-check commands.

**Files:** `apps/*/tests/`, `docs/ops/settings.md`

**Acceptance:** Tests assert `DEBUG=False` for prod and presence of security flags; docs include manual validation steps.

**Brief:** docs/travelmathlite/briefs/adr-1.0.8/brief-ADR-1.0.8-04-tests-and-invariants.md" \
  -l test,travelmathlite)
ISSUE_04=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_04}"
```

---

## ADR Issue (Optional)

If you want to track the ADR as an issue:

```bash
ISSUE_URL=$(gh issue create \
  -t "docs(adr): ADR-1.0.8 Settings configuration and secrets" \
  -b "**ADR:** adr-1.0.8-settings-configuration-and-secrets.md

**Scope:** Settings split, env-driven config, production hardening.

**Implementation:** Four briefs covering settings split, env/docs, prod security/WhiteNoise, and tests/invariants." \
  -l docs,adr,travelmathlite)
ADR_ISSUE=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created ADR Issue #${ADR_ISSUE}"
```

---

## Workflow Examples

Follow the repo guideline: prefer small PRs (<300 lines). Use `Refs #N` for ongoing work and `Closes #N` for final commit on merge.

````
