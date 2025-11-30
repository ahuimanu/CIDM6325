# GitHub CLI Commands for ADR-1.0.11 Implementation

This file provides ready-to-use GitHub CLI commands for creating Issues and managing workflow for ADR-1.0.11 (Testing Strategy).

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

### Brief 01: Test Infrastructure and Base Classes

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.11-01: Test infrastructure and base classes" \
  -b "**Goal:** Set up test infrastructure with base TestCase classes, fixtures, and helpers.

**Scope:** PRD §4 F-011

**Files:** \`apps/base/tests/__init__.py\`, \`apps/base/tests/base.py\`, \`docs/travelmathlite/testing.md\`

**Acceptance:**
- Base TestCase classes available across all apps
- Fixtures for deterministic test data
- Helpers for mocking and time-freezing
- Documentation updated

**Trace:** FR-F-011-1, NF-004
**Invariants:** INV-1

**Brief:** docs/travelmathlite/briefs/adr-1.0.11/brief-ADR-1.0.11-01-test-infrastructure.md" \
  -l feature,test,travelmathlite)
ISSUE_01=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_01}"
```

### Brief 02: Calculator Unit Tests

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.11-02: Calculator unit tests" \
  -b "**Goal:** Implement unit tests for calculator functions (distance, cost, nearest airport).

**Scope:** PRD §4 F-011

**Files:** \`apps/calculators/tests/test_geo.py\`, \`apps/calculators/tests/test_costs.py\`

**Acceptance:**
- Unit tests for distance calculation with edge cases
- Unit tests for cost estimation with boundary values
- Unit tests for nearest airport search
- All tests deterministic; no external calls

**Trace:** FR-F-011-1
**Invariants:** INV-1

**Brief:** docs/travelmathlite/briefs/adr-1.0.11/brief-ADR-1.0.11-02-calculator-tests.md" \
  -l feature,test,travelmathlite)
ISSUE_02=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_02}"
```

### Brief 03: Calculator View and Form Tests

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.11-03: Calculator view and form tests" \
  -b "**Goal:** Implement tests for calculator views and forms using RequestFactory.

**Scope:** PRD §4 F-011

**Files:** \`apps/calculators/tests/test_views.py\`

**Acceptance:**
- Tests for GET/POST requests
- Form validation tests
- HTMX request detection tests
- RequestFactory used for request simulation

**Trace:** FR-F-011-1
**Invariants:** INV-1, INV-2

**Brief:** docs/travelmathlite/briefs/adr-1.0.11/brief-ADR-1.0.11-03-view-tests.md" \
  -l feature,test,travelmathlite)
ISSUE_03=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_03}"
```

### Brief 04: Search Functionality Tests

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.11-04: Search functionality tests" \
  -b "**Goal:** Implement tests for search views, forms, and query logic.

**Scope:** PRD §4 F-011

**Files:** \`apps/search/tests.py\`, \`apps/search/tests/test_views.py\`, \`apps/search/tests/test_search.py\`

**Acceptance:**
- Tests for search form validation
- Tests for query processing and results
- Tests for empty results handling
- External calls mocked

**Trace:** FR-F-011-1
**Invariants:** INV-1

**Brief:** docs/travelmathlite/briefs/adr-1.0.11/brief-ADR-1.0.11-04-search-tests.md" \
  -l feature,test,travelmathlite)
ISSUE_04=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_04}"
```

### Brief 05: Authentication and Authorization Tests

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.11-05: Authentication and authorization tests" \
  -b "**Goal:** Implement tests for authentication flows and permission checks.

**Scope:** PRD §4 F-011

**Files:** \`apps/core/tests/test_auth.py\`

**Acceptance:**
- Tests for login/logout flows
- Tests for authenticated vs. anonymous access
- Tests for permission-based view access
- Registration tests (if applicable)

**Trace:** FR-F-011-1
**Invariants:** INV-1

**Brief:** docs/travelmathlite/briefs/adr-1.0.11/brief-ADR-1.0.11-05-auth-tests.md" \
  -l feature,test,travelmathlite)
ISSUE_05=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_05}"
```

### Brief 06: Health Endpoint and Data Import Tests

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.11-06: Health endpoint and data import tests" \
  -b "**Goal:** Implement tests for health endpoint and data import/update operations.

**Scope:** PRD §4 F-011; §7 NF-004

**Files:** \`apps/core/tests/test_health.py\`, \`apps/airports/tests/test_import.py\`

**Acceptance:**
- Health endpoint returns correct status and JSON
- Import tests verify idempotent behavior
- Network downloads mocked
- Error handling tests included

**Trace:** FR-F-011-1, NF-004
**Invariants:** INV-1

**Brief:** docs/travelmathlite/briefs/adr-1.0.11/brief-ADR-1.0.11-06-health-and-import-tests.md" \
  -l feature,test,travelmathlite)
ISSUE_06=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_06}"
```

### Brief 07: Mocking and Time-Freezing Test Examples

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.11-07: Mocking and time-freezing test examples" \
  -b "**Goal:** Create example tests demonstrating mocking external calls and time-sensitive operations.

**Scope:** PRD §4 F-011

**Files:** \`apps/base/tests/test_mocking_examples.py\`, \`docs/travelmathlite/testing.md\`

**Acceptance:**
- Example tests for mocking HTTP requests
- Examples for mocking Django model methods
- Time-freezing examples (unittest.mock or freezegun)
- Documentation updated with patterns

**Trace:** FR-F-011-1
**Invariants:** INV-1

**Brief:** docs/travelmathlite/briefs/adr-1.0.11/brief-ADR-1.0.11-07-mocking-and-time-tests.md" \
  -l feature,test,docs,travelmathlite)
ISSUE_07=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_07}"
```

### Brief 08: Playwright Visual Check Integration

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.11-08: Playwright visual check integration with tests" \
  -b "**Goal:** Integrate Playwright visual checks alongside unit tests for optional behavioral validation.

**Scope:** PRD §4 F-011

**Files:** \`scripts/visual_check.py\`, \`docs/travelmathlite/testing.md\`, \`scripts/README.md\`

**Acceptance:**
- Visual checks run independently of unit tests
- Screenshots captured for major flows
- Script runs headless
- Documentation updated

**Trace:** FR-F-011-1
**Invariants:** INV-1

**Brief:** docs/travelmathlite/briefs/adr-1.0.11/brief-ADR-1.0.11-08-visual-checks-integration.md" \
  -l feature,test,docs,travelmathlite)
ISSUE_08=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_08}"
```

---

## ADR Issue (Optional)

If you want to track the ADR itself as an issue:

```bash
ISSUE_URL=$(gh issue create \
  -t "docs(adr): ADR-1.0.11 Testing strategy" \
  -b "**ADR:** adr-1.0.11-testing-strategy.md

**Scope:** Define testing approach using Django TestCase without pytest.

**Traceability:**
- PRD §4 F-011
- PRD §7 NF-004
- FR-F-011-1

**Decision:** Use Django TestCase with stdlib mocking and optional time-freezing for deterministic, isolated tests.

**Implementation:** 8 briefs covering infrastructure, calculator tests, view tests, search tests, auth tests, health/import tests, mocking examples, and Playwright integration." \
  -l docs,adr,travelmathlite,test)
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
ISSUE_URL=$(gh issue create -t "..." -b "..." -l feature,test,travelmathlite)
ISSUE_NUM=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')

# Work and commit
COMMIT_MSG="test: add base test infrastructure — Refs #${ISSUE_NUM}"
git add -A
git commit -m "$COMMIT_MSG"
gh issue comment "$ISSUE_NUM" -b "$COMMIT_MSG"
git push

# Final commit closes issue
COMMIT_MSG="test: complete test infrastructure — Closes #${ISSUE_NUM}"
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
COMMIT_MSG="test: add base test infrastructure — Refs #${ISSUE_NUM}"
git add -A
git commit -m "$COMMIT_MSG"
gh issue comment "$ISSUE_NUM" -b "$COMMIT_MSG"
git push

# Open PR
gh pr create --fill --title "test: Base test infrastructure" \
  --body-file .github/pull_request_template.md

# Merge PR
gh pr merge --squash --delete-branch
```

---

## Combined Workflow (Create all issues at once)

```bash
# Check labels first
gh label list

# Create all issues in sequence and capture numbers
ISSUE_URL=$(gh issue create -t "ADR-1.0.11-01: Test infrastructure and base classes" -b "..." -l feature,test,travelmathlite)
ISSUE_01=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_01}"

ISSUE_URL=$(gh issue create -t "ADR-1.0.11-02: Calculator unit tests" -b "..." -l feature,test,travelmathlite)
ISSUE_02=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_02}"

# ... repeat for all 8 briefs ...

echo "All issues created: #${ISSUE_01}, #${ISSUE_02}, #${ISSUE_03}, #${ISSUE_04}, #${ISSUE_05}, #${ISSUE_06}, #${ISSUE_07}, #${ISSUE_08}"
```

---

## Notes

- **Always check labels first:** `gh label list`
- **Use existing labels only** when creating issues
- **Keep commit messages and Issue comments in sync**
- **Use "Refs #N" for ongoing work; "Closes #N" for final commit on merge to default**
- **Small PRs:** <300 lines changed per ADR guidance
- **Test coverage:** Run `uv run python manage.py test` after each brief
- **Visual checks:** Run `uvx playwright` scripts independently for behavioral validation

---

## Test Execution Commands

```bash
# Run all tests
cd travelmathlite
uv run python manage.py test

# Run specific app tests
uv run python manage.py test calculators
uv run python manage.py test search
uv run python manage.py test core.tests.test_health
uv run python manage.py test core.tests.test_auth

# Run visual checks (optional)
uvx playwright install
uvx python scripts/visual_check.py
```
