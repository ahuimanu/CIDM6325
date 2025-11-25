# GitHub CLI Commands for ADR-1.0.1 Briefs

## Create Issues for ADR-1.0.1 Briefs

```bash
# Brief 01: Dataset selection
ISSUE_01=$(gh issue create -t "Brief ADR-1.0.1-01: Dataset selection" \
  -b "Acceptance: Candidate datasets documented with pros/cons, licensing, and recommendation.
Trace: ADR-1.0.1, PRD §1.0.1" \
  -l feature,brief,travelmathlite,ADR-1.0.1 \
  --json number --jq '.number')
echo "Created Issue #${ISSUE_01}"

# Brief 02: Data ingestion pipeline
ISSUE_02=$(gh issue create -t "Brief ADR-1.0.1-02: Data ingestion pipeline" \
  -b "Acceptance: ETL pipeline implemented, management command created, sample data loaded.
Trace: ADR-1.0.1, PRD §1.0.1" \
  -l feature,brief,travelmathlite,ADR-1.0.1 \
  --json number --jq '.number')
echo "Created Issue #${ISSUE_02}"

# Brief 03: Data validation and quality checks
ISSUE_03=$(gh issue create -t "Brief ADR-1.0.1-03: Data validation and quality checks" \
  -b "Acceptance: Validation logic implemented, test cases created, quality report generated.
Trace: ADR-1.0.1, PRD §1.0.1" \
  -l feature,brief,travelmathlite,ADR-1.0.1 \
  --json number --jq '.number')
echo "Created Issue #${ISSUE_03}"

# Brief 04: Schema mapping and normalization
ISSUE_04=$(gh issue create -t "Brief ADR-1.0.1-04: Schema mapping and normalization" \
  -b "Acceptance: Mapping logic implemented, normalized data loaded, migration included if needed.
Trace: ADR-1.0.1, PRD §1.0.1" \
  -l feature,brief,travelmathlite,ADR-1.0.1 \
  --json number --jq '.number')
echo "Created Issue #${ISSUE_04}"

# Brief 05: Update automation and sync strategy
ISSUE_05=$(gh issue create -t "Brief ADR-1.0.1-05: Update automation and sync strategy" \
  -b "Acceptance: Automated update process implemented, logs and error handling in place.
Trace: ADR-1.0.1, PRD §1.0.1" \
  -l feature,brief,travelmathlite,ADR-1.0.1 \
  --json number --jq '.number')
echo "Created Issue #${ISSUE_05}"

# Brief 06: Licensing and compliance review
ISSUE_06=$(gh issue create -t "Brief ADR-1.0.1-06: Licensing and compliance review" \
  -b "Acceptance: Licensing and compliance documented, risks and obligations summarized.
Trace: ADR-1.0.1, PRD §1.0.1" \
  -l docs,brief,travelmathlite,ADR-1.0.1 \
  --json number --jq '.number')
echo "Created Issue #${ISSUE_06}"

# Brief 07: Integration with core models
ISSUE_07=$(gh issue create -t "Brief ADR-1.0.1-07: Integration with core models" \
  -b "Acceptance: Core models updated and integrated, integration logic documented and tested.
Trace: ADR-1.0.1, PRD §1.0.1" \
  -l feature,brief,travelmathlite,ADR-1.0.1 \
  --json number --jq '.number')
echo "Created Issue #${ISSUE_07}"

# Brief 08: Documentation and onboarding
ISSUE_08=$(gh issue create -t "Brief ADR-1.0.1-08: Documentation and onboarding" \
  -b "Acceptance: Contributor docs updated, onboarding guide created and linked in README.
Trace: ADR-1.0.1, PRD §1.0.1" \
  -l docs,brief,travelmathlite,ADR-1.0.1 \
  --json number --jq '.number')
echo "Created Issue #${ISSUE_08}"

# Brief 09: Test coverage for data integrity
ISSUE_09=$(gh issue create -t "Brief ADR-1.0.1-09: Test coverage for data integrity" \
  -b "Acceptance: Automated tests for data integrity implemented, CI updated.
Trace: ADR-1.0.1, PRD §1.0.1" \
  -l test,brief,travelmathlite,ADR-1.0.1 \
  --json number --jq '.number')
echo "Created Issue #${ISSUE_09}"

# Brief 10: Rollback and recovery procedures
ISSUE_10=$(gh issue create -t "Brief ADR-1.0.1-10: Rollback and recovery procedures" \
  -b "Acceptance: Rollback and recovery procedures documented, scripts or manual procedures included.
Trace: ADR-1.0.1, PRD §1.0.1" \
  -l docs,brief,travelmathlite,ADR-1.0.1 \
  --json number --jq '.number')
echo "Created Issue #${ISSUE_10}"

# Summary
echo ""
echo "All Issues created for ADR-1.0.1 briefs:"
echo "Issue #${ISSUE_01}: Brief ADR-1.0.1-01 Dataset selection"
echo "Issue #${ISSUE_02}: Brief ADR-1.0.1-02 Data ingestion pipeline"
echo "Issue #${ISSUE_03}: Brief ADR-1.0.1-03 Data validation and quality checks"
echo "Issue #${ISSUE_04}: Brief ADR-1.0.1-04 Schema mapping and normalization"
echo "Issue #${ISSUE_05}: Brief ADR-1.0.1-05 Update automation and sync strategy"
echo "Issue #${ISSUE_06}: Brief ADR-1.0.1-06 Licensing and compliance review"
echo "Issue #${ISSUE_07}: Brief ADR-1.0.1-07 Integration with core models"
echo "Issue #${ISSUE_08}: Brief ADR-1.0.1-08 Documentation and onboarding"
echo "Issue #${ISSUE_09}: Brief ADR-1.0.1-09 Test coverage for data integrity"
echo "Issue #${ISSUE_10}: Brief ADR-1.0.1-10 Rollback and recovery procedures"
```

## Example Commit Workflow (for any brief)

```bash
# Example: Working on Brief 01 (use the actual ISSUE_01 number from above)
# Prepare commit message
COMMIT_MSG="docs(brief): add ADR-1.0.1-01 dataset selection - Refs #${ISSUE_01}"

# Make changes, then commit
git add docs/travelmathlite/briefs/adr-1.0.1/brief-ADR-1.0.1-01-dataset-selection.md
git commit -m "$COMMIT_MSG"

# Mirror commit message as Issue comment
gh issue comment "${ISSUE_01}" -b "$COMMIT_MSG"

# Push
git push
```

## Final Commit (when closing an Issue)

```bash
# Example: Final commit for Brief 01
COMMIT_MSG="docs(brief): complete ADR-1.0.1-01 dataset selection - Closes #${ISSUE_01}"
git commit -m "$COMMIT_MSG"
gh issue comment "${ISSUE_01}" -b "$COMMIT_MSG"
git push
```
