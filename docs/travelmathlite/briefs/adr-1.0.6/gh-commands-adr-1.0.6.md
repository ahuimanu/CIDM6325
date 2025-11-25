# GitHub CLI Commands for ADR-1.0.6 Implementation

This file provides ready-to-use GitHub CLI commands for creating Issues and managing workflow for ADR-1.0.6 (Authentication and Saved Calculations).

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

### Brief 01: Auth Views and Templates

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.6-01: Auth views and templates" \
  -b "**Goal:** Enable login/logout/register using Django built-ins with themed templates.\n\n**Scope:** PRD §4 F-006; §7 NF-003\n\n**Files:** \`apps/accounts/urls.py\`, \`apps/accounts/templates/registration/*.html\`, \`templates/base.html\`\n\n**Acceptance:**\n- Login, logout, signup render and work\n- Redirects configured\n- Nav shows login/signup or username/logout\n\n**Trace:** FR-F-006-1, NF-003\n\n**Brief:** docs/travelmathlite/briefs/adr-1.0.6/brief-ADR-1.0.6-01-auth-views-and-templates.md" \
  -l feature,FR,travelmathlite,auth)
ISSUE_01=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_01}"
```

### Brief 02: SavedCalculation Model and Admin

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.6-02: SavedCalculation model and admin" \
  -b "**Goal:** Implement model to store last 10 calculations per user with pruning.\n\n**Scope:** PRD §4 F-006\n\n**Files:** \`apps/trips/models.py\`, \`apps/trips/admin.py\`, migrations\n\n**Acceptance:**\n- Model fields per ADR\n- Pruning keeps max 10 per user\n- Admin list/search enabled\n\n**Trace:** FR-F-006-1; Invariant: INV-2\n\n**Brief:** docs/travelmathlite/briefs/adr-1.0.6/brief-ADR-1.0.6-02-savedcalculation-model-and-admin.md" \
  -l feature,FR,travelmathlite)
ISSUE_02=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_02}"
```

### Brief 03: Session Migration Post-Login

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.6-03: Session migration after login" \
  -b "**Goal:** Migrate anonymous calculator inputs after login via signal.\n\n**Scope:** PRD §4 F-006; §7 NF-003\n\n**Files:** \`apps/accounts/signals.py\`, \`apps/core/session.py\` (or calculators)\n\n**Acceptance:**\n- Next calculation post-login sees previous inputs\n- No DB writes during login\n- Safe when no session data\n\n**Trace:** FR-F-006-1, NF-003; Invariant: INV-1\n\n**Brief:** docs/travelmathlite/briefs/adr-1.0.6/brief-ADR-1.0.6-03-session-migration-post-login.md" \
  -l feature,FR,travelmathlite,auth)
ISSUE_03=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_03}"
```

### Brief 04: Saved List and Delete Views

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.6-04: Saved list and delete views" \
  -b "**Goal:** Per-user list and delete for saved calculations (max 10).\n\n**Scope:** PRD §4 F-006; §7 NF-003\n\n**Files:** \`apps/trips/views.py\`, \`apps/trips/urls.py\`, templates\n\n**Acceptance:**\n- Only owner sees their items\n- Delete works; others' items inaccessible\n- Newest first; up to 10 listed\n\n**Trace:** FR-F-006-1, NF-003; Invariants: INV-1, INV-2\n\n**Brief:** docs/travelmathlite/briefs/adr-1.0.6/brief-ADR-1.0.6-04-saved-list-and-delete-views.md" \
  -l feature,FR,travelmathlite)
ISSUE_04=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_04}"
```

### Brief 05: Tests and Invariants

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.6-05: Tests for pruning, migration, access" \
  -b "**Goal:** Add TestCase coverage for pruning, session migration, and per-user access.\n\n**Scope:** PRD §10 Acceptance; §7 NF-003\n\n**Files:** tests in apps/trips and apps/accounts\n\n**Acceptance:**\n- INV-1 and INV-2 enforced by tests\n- Session migration safe when no data\n- Owner vs non-owner access verified\n\n**Trace:** FR-F-006-1, NF-003; Invariants: INV-1, INV-2\n\n**Brief:** docs/travelmathlite/briefs/adr-1.0.6/brief-ADR-1.0.6-05-tests-and-invariants.md" \
  -l test,travelmathlite)
ISSUE_05=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_05}"
```

---

## ADR Issue (Optional)

```bash
ISSUE_URL=$(gh issue create \
  -t "docs(adr): ADR-1.0.6 Authentication and Saved Calculations" \
  -b "**ADR:** adr-1.0.6-auth-and-saved-calculations-model.md\n\n**Scope:** Built-in auth; SavedCalculation model; session migration; list/delete.\n\n**Traceability:**\n- PRD §4 F-006\n- PRD §7 NF-003\n- FR-F-006-1\n\n**Decision:** Use Django auth + lightweight SavedCalculation with pruning.\n\n**Implementation:** 5 briefs covering auth, model, session migration, views, and tests." \
  -l docs,adr,travelmathlite,auth)
ADR_ISSUE=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created ADR Issue #${ADR_ISSUE}"
```

---

## Workflow Examples

### Issues-Only Workflow (no branches)

```bash
# Stay on base branch
git checkout FALL2025

# Create Issue (e.g., Brief 01)
ISSUE_URL=$(gh issue create -t "..." -b "..." -l feature,FR,travelmathlite,auth)
ISSUE_NUM=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')

# Work and commit
COMMIT_MSG="feat: wire auth views and templates — Refs #${ISSUE_NUM}"
git add -A
git commit -m "$COMMIT_MSG"
gh issue comment "$ISSUE_NUM" -b "$COMMIT_MSG"
git push

# Final commit closes issue
COMMIT_MSG="feat: complete auth views and templates — Closes #${ISSUE_NUM}"
git commit -m "$COMMIT_MSG"
gh issue comment "$ISSUE_NUM" -b "$COMMIT_MSG"
git push
```

### Branch-Per-Issue Workflow

```bash
# Create and link branch
gh issue develop ${ISSUE_NUM} --base FALL2025
git switch <auto-created-branch>

# Work and commit
COMMIT_MSG="feat: wire auth views and templates — Refs #${ISSUE_NUM}"
git add -A
git commit -m "$COMMIT_MSG"
gh issue comment "$ISSUE_NUM" -b "$COMMIT_MSG"
git push

# Open PR
gh pr create --fill --title "feat: auth views and templates" \
  --body-file .github/pull_request_template.md

# Merge PR
gh pr merge --squash --delete-branch
```

---

## Notes

- Always check labels first: `gh label list`
- Use existing labels only when creating issues
- Keep commit messages and Issue comments in sync (same text)
- Use "Refs #N" for ongoing work; "Closes #N" for final commit on merge to default
- Small PRs: <300 lines changed per class guidance
