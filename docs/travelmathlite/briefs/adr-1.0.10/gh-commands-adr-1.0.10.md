# GitHub CLI Commands for ADR-1.0.10 Implementation

This file provides ready-to-use GitHub CLI commands for creating Issues and managing workflow for ADR-1.0.10 (Caching Strategy).

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

### Brief 01: Cache Backend Configuration

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.10-01: Configure cache backend" \
  -b "**Goal:** Configure Django CACHES setting with locmem for local and optional Redis/file-based for production.

**Scope:** PRD §4 F-013; §7 NF-001

**Files:**
- \`core/settings/base.py\` — Add CACHES configuration
- \`core/settings/local.py\` — Ensure locmem default
- \`core/settings/prod.py\` — Support CACHE_URL environment variable
- \`.env.example\` — Document CACHE_URL
- \`core/tests/test_cache_config.py\` — Tests

**Acceptance:**
- locmem backend in local
- CACHE_URL support in prod (Redis/file-based)
- Default TTL: 300 seconds
- Environment variable documented
- Tests verify configuration

**Trace:** FR-F-013-1, NF-001

**Brief:** docs/travelmathlite/briefs/adr-1.0.10/brief-ADR-1.0.10-01-cache-backend-config.md" \
  -l feature,FR,travelmathlite)
ISSUE_01=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_01}"
```

### Brief 02: Per-View Caching

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.10-02: Implement per-view caching with decorators" \
  -b "**Goal:** Apply @cache_page decorator to search and calculator views with short TTLs.

**Scope:** PRD §4 F-013; §7 NF-001

**Files:**
- \`apps/search/views.py\` — Add @cache_page (5 min)
- \`apps/calculators/views.py\` — Add @cache_page to nearest airport (10 min)
- \`apps/search/tests/test_caching.py\` — Tests
- \`apps/calculators/tests/test_caching.py\` — Tests

**Acceptance:**
- Search results cached (5 minutes)
- Nearest airport cached (10 minutes)
- Cache keys vary by query params
- POST requests bypass cache
- Tests verify hits/misses

**Trace:** FR-F-013-1, NF-001, INV-1

**Brief:** docs/travelmathlite/briefs/adr-1.0.10/brief-ADR-1.0.10-02-per-view-caching.md" \
  -l feature,FR,travelmathlite)
ISSUE_02=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_02}"
```

### Brief 03: Low-Level Caching

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.10-03: Implement low-level caching for computed data" \
  -b "**Goal:** Use Django low-level cache API for expensive computations (airport lists, distances).

**Scope:** PRD §4 F-013; §7 NF-001

**Files:**
- \`apps/airports/utils.py\` — Cache airport queries
- \`apps/calculators/utils.py\` — Cache distance calculations
- \`apps/airports/tests/test_cache_utils.py\` — Tests
- \`apps/calculators/tests/test_cache_utils.py\` — Tests

**Acceptance:**
- Airport queries cached (15 min)
- Distance calculations cached (15 min)
- Deterministic cache keys
- Manual invalidation helper
- Tests verify cache behavior

**Trace:** FR-F-013-1, NF-001, INV-1

**Brief:** docs/travelmathlite/briefs/adr-1.0.10/brief-ADR-1.0.10-03-low-level-caching.md" \
  -l feature,FR,travelmathlite)
ISSUE_03=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_03}"
```

### Brief 04: Cache Control Headers

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.10-04: Add cache control headers" \
  -b "**Goal:** Configure HTTP cache headers (Cache-Control, ETag, Vary) for browser/CDN caching.

**Scope:** PRD §7 NF-001

**Files:**
- \`core/middleware.py\` — Cache header middleware
- \`core/settings/base.py\` — Add middleware
- \`apps/search/views.py\` — Conditional headers
- \`apps/calculators/views.py\` — Conditional headers
- \`core/tests/test_cache_headers.py\` — Tests

**Acceptance:**
- Static assets: max-age=31536000 (1 year)
- Dynamic content: max-age=300 (5 min)
- Vary headers for API/authenticated
- Tests verify headers

**Trace:** FR-F-013-1, NF-001

**Brief:** docs/travelmathlite/briefs/adr-1.0.10/brief-ADR-1.0.10-04-cache-headers.md" \
  -l feature,FR,travelmathlite)
ISSUE_04=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_04}"
```

### Brief 05: Documentation and Testing

```bash
ISSUE_URL=$(gh issue create \
  -t "ADR-1.0.10-05: Caching documentation and comprehensive tests" \
  -b "**Goal:** Create comprehensive caching docs and integration tests.

**Scope:** PRD §4 F-013; §7 NF-001

**Files:**
- \`docs/travelmathlite/ops/caching.md\` — Operations guide
- \`core/tests/test_caching_integration.py\` — Integration tests
- \`management/commands/clear_cache.py\` — Cache clearing command
- \`management/commands/cache_stats.py\` — Cache statistics command
- \`README.md\` — Update with caching config

**Acceptance:**
- Ops guide covers: config, usage, invalidation, monitoring
- Management commands for clearing and stats
- Integration tests verify end-to-end behavior
- Redis setup documentation

**Trace:** FR-F-013-1, NF-001, INV-1

**Brief:** docs/travelmathlite/briefs/adr-1.0.10/brief-ADR-1.0.10-05-docs-and-tests.md" \
  -l feature,FR,travelmathlite,docs)
ISSUE_05=$(echo "$ISSUE_URL" | sed -E 's#.*/([0-9]+)$#\1#')
echo "Created Issue #${ISSUE_05}"
```

---

## Workflow Commands

### Create Branch for Brief

```bash
# Example for Brief 01
git checkout -b adr-1.0.10-01-cache-backend-config
git push -u origin adr-1.0.10-01-cache-backend-config

# Link branch to Issue (optional)
gh issue develop ${ISSUE_01} --base FALL2025
```

### Commit with Issue Reference

```bash
# Example commit messages
COMMIT_MSG="feat: configure cache backend for local and prod

- Add CACHES setting with locmem default
- Support CACHE_URL environment variable in prod
- Add cache configuration tests
- Document CACHE_URL in .env.example

Refs #${ISSUE_01}"

git add -A
git commit -m "$COMMIT_MSG"

# Mirror commit message as Issue comment
gh issue comment "${ISSUE_01}" -b "$COMMIT_MSG"

git push
```

### Create Pull Request

```bash
# Example for Brief 01
gh pr create \
  --title "feat: configure cache backend (ADR-1.0.10-01)" \
  --body "**Summary**
Configures Django cache backend with locmem for local development and optional Redis/file-based backend for production.

**Changes**
- Added CACHES configuration in base.py
- Added CACHE_URL support in prod.py with django-environ
- Created cache configuration tests
- Documented CACHE_URL in .env.example

**Testing**
- Cache backend loads correctly in local (locmem)
- Cache backend configurable in prod via CACHE_URL
- Tests verify configuration: \`test_cache_config\`

**Trace**
- FR-F-013-1: Per-view/low-level caching
- NF-001: Performance targets
- Issue: #${ISSUE_01}

**Checklist**
- [x] Tests pass
- [x] Documentation updated
- [x] No secrets committed
- [x] Conventional commit style" \
  --base FALL2025 \
  --head adr-1.0.10-01-cache-backend-config
```

### Merge PR

```bash
# After approval, squash merge
gh pr merge --squash --delete-branch

# Final commit message should use "Closes" keyword
git commit --amend -m "feat: configure cache backend (ADR-1.0.10-01)

- Add CACHES setting with locmem default
- Support CACHE_URL environment variable in prod
- Add cache configuration tests
- Document CACHE_URL in .env.example

Closes #${ISSUE_01}"
```

---

## Consolidated Commands (Create All Issues)

```bash
# Run all issue creation commands in sequence
bash -c '
gh label list

ISSUE_URL=$(gh issue create -t "ADR-1.0.10-01: Configure cache backend" -b "..." -l feature,FR,travelmathlite)
ISSUE_01=$(echo "$ISSUE_URL" | sed -E "s#.*/([0-9]+)$#\1#")
echo "Issue #${ISSUE_01}: Cache backend config"

ISSUE_URL=$(gh issue create -t "ADR-1.0.10-02: Implement per-view caching" -b "..." -l feature,FR,travelmathlite)
ISSUE_02=$(echo "$ISSUE_URL" | sed -E "s#.*/([0-9]+)$#\1#")
echo "Issue #${ISSUE_02}: Per-view caching"

ISSUE_URL=$(gh issue create -t "ADR-1.0.10-03: Implement low-level caching" -b "..." -l feature,FR,travelmathlite)
ISSUE_03=$(echo "$ISSUE_URL" | sed -E "s#.*/([0-9]+)$#\1#")
echo "Issue #${ISSUE_03}: Low-level caching"

ISSUE_URL=$(gh issue create -t "ADR-1.0.10-04: Add cache control headers" -b "..." -l feature,FR,travelmathlite)
ISSUE_04=$(echo "$ISSUE_URL" | sed -E "s#.*/([0-9]+)$#\1#")
echo "Issue #${ISSUE_04}: Cache headers"

ISSUE_URL=$(gh issue create -t "ADR-1.0.10-05: Caching documentation" -b "..." -l feature,FR,travelmathlite,docs)
ISSUE_05=$(echo "$ISSUE_URL" | sed -E "s#.*/([0-9]+)$#\1#")
echo "Issue #${ISSUE_05}: Documentation and tests"

echo ""
echo "Created 5 issues for ADR-1.0.10"
echo "Issue numbers: ${ISSUE_01}, ${ISSUE_02}, ${ISSUE_03}, ${ISSUE_04}, ${ISSUE_05}"
'
```

---

## Summary

**ADR-1.0.10: Caching Strategy**

**Briefs:**

1. Cache backend configuration (locmem/Redis)
2. Per-view caching with @cache_page decorators
3. Low-level caching for computed data
4. Cache control headers (Cache-Control, Vary, ETag)
5. Documentation and comprehensive testing

**Key Commands:**

- `gh label list` — Check available labels first
- `gh issue create` — Create issues with full context
- `git checkout -b <branch>` — Create feature branch
- `gh pr create` — Open PR with summary
- `gh pr merge --squash` — Squash merge after approval

**Commit Style:**

- Use "Refs #N" for ongoing work
- Use "Closes #N" for final merge commit
- Mirror commit messages as issue comments for traceability
