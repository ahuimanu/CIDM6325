# GitHub CLI Commands for ADR-1.0.5 Implementation

This file provides ready-to-use GitHub CLI commands for creating Issues and managing workflow for ADR-1.0.5 (Forms and HTMX Progressive Enhancement).

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

### Brief 01: HTMX Base Setup

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.5-01: HTMX base template integration" \
  -b "**Goal:** Add HTMX library to base template and configure progressive enhancement.

**Scope:** PRD §4 F-001, F-003, F-007; §7 NF-002

**Files:** \`templates/base.html\`, \`docs/ux/htmx-patterns.md\`

**Acceptance:**
- HTMX library loaded globally
- Templates remain valid HTML5
- No-JS fallback works

**Trace:** FR-F-001-2, FR-F-003-1, NF-002

**Brief:** docs/travelmathlite/briefs/adr-1.0.5/brief-ADR-1.0.5-01-htmx-base-setup.md" \
  -l feature,FR,travelmathlite,htmx)
ISSUE_01=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_01}"
```

### Brief 02: HTMX Calculator Forms

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.5-02: HTMX-enhanced calculator forms" \
  -b "**Goal:** Add HTMX attributes to calculator forms for partial updates.

**Scope:** PRD §4 F-001, F-003

**Files:** Calculator form templates, views

**Acceptance:**
- Forms have \`hx-post\`, \`hx-target\`, \`hx-swap\` attributes
- CSRF tokens present
- Progressive enhancement (works without JS)

**Trace:** FR-F-001-2, FR-F-003-1

**Brief:** docs/travelmathlite/briefs/adr-1.0.5/brief-ADR-1.0.5-02-htmx-calculator-forms.md" \
  -l feature,FR,travelmathlite,htmx)
ISSUE_02=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_02}"
```

### Brief 03: Partial Templates

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.5-03: Partial templates for HTMX responses" \
  -b "**Goal:** Create partial templates for calculator results.

**Scope:** PRD §4 F-001, F-003; §7 NF-002

**Files:** \`apps/calculators/templates/calculators/partials/\`

**Acceptance:**
- Partial templates for each calculator
- Shared validation/error display logic
- Proper ARIA attributes

**Trace:** FR-F-001-2, FR-F-003-1, NF-002

**Brief:** docs/travelmathlite/briefs/adr-1.0.5/brief-ADR-1.0.5-03-partial-templates.md" \
  -l feature,FR,travelmathlite,htmx)
ISSUE_03=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_03}"
```

### Brief 04: View HTMX Detection

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.5-04: View HTMX detection and partial rendering" \
  -b "**Goal:** Update calculator views to detect HTMX requests and return partials.

**Scope:** PRD §4 F-001, F-003

**Files:** \`apps/calculators/views.py\`

**Acceptance:**
- Views detect HX-Request header
- Same view handles both HTMX and full-page flows
- Tests cover both request types

**Trace:** FR-F-001-2, FR-F-003-1
**Invariants:** INV-1, INV-2

**Brief:** docs/travelmathlite/briefs/adr-1.0.5/brief-ADR-1.0.5-04-view-htmx-detection.md" \
  -l feature,FR,travelmathlite,htmx)
ISSUE_04=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_04}"
```

### Brief 05: Focus and Accessibility

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.5-05: Focus management and accessibility" \
  -b "**Goal:** Add focus management and ARIA attributes for HTMX updates.

**Scope:** PRD §7 NF-002

**Files:** Partial templates, calculator templates, base template

**Acceptance:**
- Focus moves to result after HTMX swap
- ARIA live regions for announcements
- Keyboard navigation works

**Trace:** NF-002

**Brief:** docs/travelmathlite/briefs/adr-1.0.5/brief-ADR-1.0.5-05-focus-and-accessibility.md" \
  -l feature,NF,travelmathlite,htmx,accessibility)
ISSUE_05=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_05}"
```

### Brief 06: Tests and Visual Checks

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.5-06: Tests and visual checks for HTMX" \
  -b "**Goal:** Add unit and behavioral tests for HTMX forms.

**Scope:** PRD §10 Acceptance

**Files:** \`apps/calculators/tests/\`, \`travelmathlite/scripts/\`, screenshots

**Acceptance:**
- Tests for HTMX detection and template selection
- CSRF token verification
- Playwright visual check script
- Non-JS fallback verified

**Trace:** FR-F-001-2, FR-F-003-1
**Invariants:** INV-1, INV-2

**Brief:** docs/travelmathlite/briefs/adr-1.0.5/brief-ADR-1.0.5-06-tests-and-visual-checks.md" \
  -l test,travelmathlite,htmx)
ISSUE_06=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_06}"
```

---

## ADR Issue (Optional)

If you want to track the ADR itself as an issue:

```bash
ISSUE_URL=$(gh issue create \
  -t "docs(adr): ADR-1.0.5 Forms and HTMX progressive enhancement" \
  -b "**ADR:** adr-1.0.5-forms-and-htmx-progressive-enhancement.md

**Scope:** Adopt HTMX for calculator forms with progressive enhancement.

**Traceability:**
- PRD §4 F-001, F-003, F-007
- PRD §7 NF-002
- FR-F-001-2, FR-F-003-1, FR-F-007-1

**Decision:** Use HTMX with partials for snappy UX while preserving full-page fallback.

**Implementation:** 6 briefs covering base setup, forms, partials, view logic, accessibility, and tests." \
  -l docs,adr,travelmathlite,htmx)
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
ISSUE_URL=$(gh issue create -t "..." -b "..." -l feature,FR,travelmathlite,htmx)
ISSUE_NUM=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')

# Work and commit
COMMIT_MSG="feat: add HTMX to base template — Refs #${ISSUE_NUM}"
git add -A
git commit -m "$COMMIT_MSG"
gh issue comment "$ISSUE_NUM" -b "$COMMIT_MSG"
git push

# Final commit closes issue
COMMIT_MSG="feat: complete HTMX base setup — Closes #${ISSUE_NUM}"
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
COMMIT_MSG="feat: add HTMX to base template — Refs #${ISSUE_NUM}"
git add -A
git commit -m "$COMMIT_MSG"
gh issue comment "$ISSUE_NUM" -b "$COMMIT_MSG"
git push

# Open PR
gh pr create --fill --title "feat: HTMX base setup" \
  --body-file .github/pull_request_template.md

# Merge PR
gh pr merge --squash --delete-branch
```

---

## Notes

- **Always check labels first:** `gh label list`
- **Use existing labels only** when creating issues
- **Keep commit messages and Issue comments in sync**
- **Use "Refs #N" for ongoing work; "Closes #N" for final commit on merge to default**
- **Small PRs:** <300 lines changed per ADR guidance
