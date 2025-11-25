# GH CLI commands — ADR-1.0.4 Search strategy and URL design

> Always check available labels before creating issues, and reuse existing ones.

```bash
# 1) Check labels
gh label list

# 2) Create Issues for each brief and capture numbers (Git Bash friendly)

ISSUE_URL_01=$(gh issue create \
  -t "BRIEF: ADR-1.0.4-01 search view and query parsing" \
  -b "Trace: ADR-1.0.4; PRD §4 F-008, F-007. Acceptance: non-empty q, safe parse, 200 response." \
  -l feature,FR,travelmathlite)
ISSUE_01=$(echo "$ISSUE_URL_01" | sed -E 's#.*/([0-9]+)$#\1#')

ISSUE_URL_02=$(gh issue create \
  -t "BRIEF: ADR-1.0.4-02 pagination and querystring" \
  -b "Trace: ADR-1.0.4; INV-1 preserve q. Acceptance: page links keep q, page 2 renders." \
  -l feature,FR,travelmathlite)
ISSUE_02=$(echo "$ISSUE_URL_02" | sed -E 's#.*/([0-9]+)$#\1#')

ISSUE_URL_03=$(gh issue create \
  -t "BRIEF: ADR-1.0.4-03 highlight helper and safety" \
  -b "Trace: ADR-1.0.4; NF-003. Acceptance: <mark> around matches, no XSS, escaping intact." \
  -l feature,NF,travelmathlite)
ISSUE_03=$(echo "$ISSUE_URL_03" | sed -E 's#.*/([0-9]+)$#\1#')

ISSUE_URL_04=$(gh issue create \
  -t "BRIEF: ADR-1.0.4-04 URL design, canonical, sitemap" \
  -b "Trace: ADR-1.0.4; FR-F-007-1. Acceptance: namespaced URLs, canonical link, sitemap entries." \
  -l feature,FR,travelmathlite)
ISSUE_04=$(echo "$ISSUE_URL_04" | sed -E 's#.*/([0-9]+)$#\1#')

ISSUE_URL_05=$(gh issue create \
  -t "BRIEF: ADR-1.0.4-05 templates and navbar search" \
  -b "Trace: ADR-1.0.4; FR-F-007-1. Acceptance: navbar search submits to /search/ and preserves value." \
  -l feature,FR,travelmathlite)
ISSUE_05=$(echo "$ISSUE_URL_05" | sed -E 's#.*/([0-9]+)$#\1#')

ISSUE_URL_06=$(gh issue create \
  -t "BRIEF: ADR-1.0.4-06 tests and visual checks" \
  -b "Trace: ADR-1.0.4; §10 Acceptance. Acceptance: tests for pagination/highlight/canonical and one screenshot." \
  -l testing,AC,travelmathlite)
ISSUE_06=$(echo "$ISSUE_URL_06" | sed -E 's#.*/([0-9]+)$#\1#')

echo Created: #$ISSUE_01 #$ISSUE_02 #$ISSUE_03 #$ISSUE_04 #$ISSUE_05 #$ISSUE_06

# 3) Example commit+comment sync (issues-only workflow)
COMMIT_MSG="docs(brief): ADR-1.0.4 briefs set — Refs #$ISSUE_01 #$ISSUE_02 #$ISSUE_03 #$ISSUE_04 #$ISSUE_05 #$ISSUE_06"
git add -A && git commit -m "$COMMIT_MSG" && gh issue comment "$ISSUE_01" -b "$COMMIT_MSG" && gh issue comment "$ISSUE_02" -b "$COMMIT_MSG" && gh issue comment "$ISSUE_03" -b "$COMMIT_MSG" && gh issue comment "$ISSUE_04" -b "$COMMIT_MSG" && gh issue comment "$ISSUE_05" -b "$COMMIT_MSG" && gh issue comment "$ISSUE_06" -b "$COMMIT_MSG"
```

Notes

- Use issues-only on the base branch unless you prefer per-issue branches (`gh issue develop ISSUE_NUM`).
- Keep commits small and reference the Issue using `Refs #ISSUE_NUM` until the final merge commit uses `Closes #ISSUE_NUM`.
