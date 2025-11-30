# CIDM 6325 — Pull Requests Two Ways (Trunk‑Only, Full Lifecycle)

A complete, copy‑paste‑ready tutorial for a **trunk‑only** workflow. You do all work on your **fork’s `main`** branch (no feature branches) and open Pull Requests (PRs) back to the course repository’s `main`. This guide presents two parallel, end‑to‑end paths:

1. **Web full lifecycle** — all local Git commands plus all Web UI interactions
2. **CLI full lifecycle** — all `gh` and `git` commands (no Web UI required)

---

## Crib Sheet — Branch‑based → Trunk‑only translation

| Old command or idea                                       | Trunk‑only equivalent                                         |
| --------------------------------------------------------- | ------------------------------------------------------------- |
| `git checkout -b feature/<topic>`                         | Do nothing. Stay on your fork’s `main`.                       |
| `git push -u origin feature/<topic>`                      | `git push origin main`                                        |
| Website compare: `base: main`, `compare: feature/<topic>` | `base: <course-org>:main`, `compare: <your-username>:main`    |
| `gh pr create --head feature/<topic>`                     | `gh pr create --head <your-username>:main`                    |
| Rebase feature branch onto `origin/main`                  | Sync your fork’s `main` with upstream `main` (see Sync steps) |
| Delete feature branch after merge                         | No branch to delete. Keep working on your fork’s `main`       |

---

## Common One‑Time Setup (used by both paths)

``` bash
gh auth login

# Fork the course repo into your account and clone your fork locally
gh repo fork {course-org}/{repo} --clone
cd {repo}

# Add the upstream remote (the course repository)
git remote add upstream https://github.com/{course-org}/{repo}.git
git remote -v

# Optional: set your Git identity
git config user.name "<Your Name>"
git config user.email "<you@example.com>"
```

---

## Path A — Web Full Lifecycle (local Git + Web UI)

Follow these steps start‑to‑finish using local Git plus GitHub’s website.

### A1) Sync your fork’s `main` before starting

``` bash
# Option A: GitHub CLI - note: the curly braces are for the placeholder, don't leave them in
gh repo sync --source {org}/{repo} --force

# be careful with --force, it you are ahead of upstream (org), it will pull you back
gh repo sync --source {org}/{repo} --force

# remedy
git pull origin main
git push -u origin main

# if all is well, push (copy to) origin/main
git push origin main

# Option B: Git
git fetch upstream
git checkout main
git merge --ff-only upstream/main
git push origin main
```

### A2) Make changes on trunk (your fork’s `main`)

``` bash
git checkout main
# edit files
git add -A
git commit -m "feat: <concise summary>"
git push origin main
```

### A3) Open the PR on the website (fork main → upstream main)

1. Navigate to **your fork** on GitHub.
2. Click **Contribute** → **Open pull request** (or **Compare**).
3. Verify compare/base:

   * base repository: `<course-org>/<repo>`
   * base: `main`
   * head repository: `<your-username>/<repo>`
   * compare: `main`
4. Fill the PR form:

   * Title: `feat: <concise summary>`
   * Description: paste the course PR template; include testing steps and rollback plan
   * Links: PRD section, ADR id, Issues (`Closes #<id>`)
5. Click **Create pull request**.

### A4) Iterate on the PR

``` bash
# keep committing on your fork’s main
git add -A
git commit -m "fix: address reviewer feedback"
git push origin main
```

On the PR page: reply to comments, mark conversations **Resolved**, watch status checks.

### A5) If upstream `main` advanced, update your PR

``` bash
# Option A: CLI
gh repo sync --source upstream --force
git push origin main

# Option B: Git
git fetch upstream
git checkout main
git merge --ff-only upstream/main
git push origin main
```

### A6) Resolve merge conflicts (if any)

``` bash
git fetch upstream
git checkout main
git merge upstream/main     # resolve conflicts
git add {resolved-files}
git commit                  # commit the merge
git push origin main
```

### A7) Merge (performed by maintainers)

Maintainers **Squash and merge** the PR into upstream `main` when green and approved.

### A8) Post‑merge hygiene

``` bash
gh repo sync --source upstream --force
git push origin main
```

Close any linked issues (if not auto‑closed) and record decisions in ADRs as needed.

---

## Path B — CLI Full Lifecycle (`gh` + `git` only)

Do the entire process from the terminal, including opening and reviewing PRs.

### B1) Sync your fork’s `main` before starting

``` bash
gh repo sync --source upstream --force
git push origin main
```

### B2) Make changes on trunk (your fork’s `main`)

``` bash
git checkout main
# edit files
git add -A
git commit -m "feat: <concise summary>"
git push origin main
```

### B3) Create the PR to upstream `main` (CLI)

``` bash
gh pr create \
  --base main \
  --head <your-username>:main \
  --title "feat: <concise summary>" \
  --body-file .github/pull_request_template.md
```

Optional variations:
gh pr create --fill      # derive body from recent commits
gh pr create --web       # open the prefilled PR in the browser

### B4) Iterate entirely from the CLI

``` bash
# push new commits; PR updates automatically
git add -A
git commit -m "fix: tighten validation and tests"
git push origin main

# discuss and check status from terminal
gh pr comment {number} -b "Please review the validation changes."
gh pr status
gh pr checks {number}
```

### B5) Update your PR if upstream `main` moved

``` bash
gh repo sync --source upstream --force
git push origin main
```

### B6) Resolve conflicts locally, then push

``` bash
git fetch upstream
git checkout main
git merge upstream/main     # resolve conflicts
git add {resolved-files}
git commit
git push origin main
```

### B7) Merge (maintainer action, for reference)

``` bash
gh pr ready {number}        # if it was a draft
gh pr merge {number} --squash
```

### B8) Post‑merge hygiene

``` bash
gh repo sync --source upstream --force
git push origin main
```

---

## Appendix — Power Tips

Website

* Files changed view: use **Viewed** checkboxes to track your pass on long diffs.
* Draft ↔ Ready for review to control signal/noise. Enable Auto‑merge (squash) if allowed.

CLI

* Request reviews and assign: `gh pr create --assignee @me`, `--reviewer user1,user2`
* Inspect CI quickly: `gh pr checks {number}`, `gh pr status`
* Review a teammate’s PR locally: `gh pr checkout {number}`

## Troubleshooting (trunk‑only)

* PR shows no changes: make sure you pushed commits to your fork’s `main` and that compare is `<your-username>:main` → `<course-org>:main`.
* Fork behind upstream: sync first (Path A1 or B1), push, and the PR updates automatically.
