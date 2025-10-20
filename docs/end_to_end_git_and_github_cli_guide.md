# CIDM 6325 — End‑to‑End Git & GitHub Workflow (Rich Guide: `git` + `gh`)

A comprehensive, example‑heavy tutorial covering the **common pathways** students use in this course. It emphasizes both **Git** and the **GitHub CLI (`gh`)**, shows how they interoperate, and provides practical recipes for day‑to‑day work.

> House rules for this course: **No pytest**. Use `python -m unittest` for pure Python and `python manage.py test` for Django.

---

## 0) Mental model in 90 seconds

- **Local repo** (your working directory) ←→ **Remotes** (`origin` = your fork, `upstream` = course repo)
- **Commits**: snapshots you make locally. **Push** sends them to a remote. **Pull** fetches remote commits to you.
- **Branches**: pointers to commit histories. In this course we emphasize **trunk‑only** PRs (fork’s `main` → upstream `main`), but we also show feature‑branch patterns so you recognize them.
- **PRs**: a request to merge one line of history into another, with review + checks.

---

## 1) One‑time setup (fork, clone, remotes)

``` bash
gh auth login

# Fork the course repo and clone your fork locally
gh repo fork <course-org>/<repo> --clone
cd <repo>

# Add upstream (the course repo); origin is your fork by default
git remote add upstream https://github.com/<course-org>/<repo>.git
git remote -v

# Optional: identity
git config user.name "<Your Name>"
git config user.email "<you@example.com>"
```

---

## 2) Sync before you start (keep your fork current)

**Using `gh`**
gh repo sync --source upstream --force
git push origin main

**Using `git`**
git fetch upstream
git checkout main
git merge --ff-only upstream/main
git push origin main

Why: prevents drifting far behind upstream and avoids painful conflicts later.

---

## 3) Make changes the right way (atomic commits)

- Work in **small, coherent steps**. Each commit should do one thing.
- Use **conventional** commit messages: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`

### Example

``` bash
# edit files
git add -p
git commit -m "feat: add search form to items page"

Run tests locally **before** pushing:
# pure Python
python -m unittest -v


# Django
python manage.py test -v 2

#Push to your fork:
git push origin main
```

---

## 4) Open Pull Requests (two common pathways)

### 4A) Trunk‑only PR (recommended for this course)

Head = `<your-username>:main` → Base = `<course-org>:main`

#### Web

1. Go to **your fork** → **Contribute** → **Open pull request**
2. Confirm compare/base: base `<course-org>:main`, compare `<your-username>:main`
3. Title + description (use PR template). Link PRD/ADR. Create PR.

#### CLI

```bash
gh pr create
--base main
--head <your-username>:main
--title "feat: add search form"
--body-file .github/pull_request_template.md
```

Iterate by pushing more commits to your fork’s `main`.

### 4B) Feature‑branch PR (for awareness; not required here)

Head = `<your-username>:feature/x` → Base = `<course-org>:main`

Create a branch, commit, push, PR. (Omitted here—use trunk in class.)

---

## 5) Review loop: comments, checks, revisions

### Website

- Reply to comments, push fixes, click **Resolve conversation** when done.
- Use **Viewed** checkboxes on Files changed to track your sweep.

### CLI (review loop)

``` bash
gh pr comment <number> -b "Explained validation path; new test covers edge case."
gh pr status
gh pr checks <number>
```

> Keep commits small; reviewers approve faster.

---

## 6) Updating when upstream moves (rebasing vs fast‑forward merge)

Trunk‑only uses **fast‑forward merges** to move your fork’s `main` ahead.

**Using `gh`**

``` bash
gh repo sync --source upstream --force
git push origin main
```

**Using `git`**

``` bash
git fetch upstream
git checkout main
git merge --ff-only upstream/main
git push origin main
```

Your open PR updates automatically.

---

## 7) Resolve merge conflicts (step‑by‑step)

```bash
# ensure you have the latest upstream
git fetch upstream
git checkout main

# merge upstream/main into your main and resolve conflicts
git merge upstream/main`

# open conflict files, choose correct hunks
git add <resolved-file1> <resolved-file2>
git commit   # commit the merge resolution
git push origin main
```

PR will re‑evaluate and conflicts should clear.

---

## 8) Merge policies (what happens when approved)

- **Squash and merge** (class default): creates one clean commit in upstream `main` regardless of how many commits you made. Great for history.
- **Merge commit**: preserves your commits and adds a merge node. Not recommended here.
- **Rebase and merge**: linearizes commits. Advanced; not needed for trunk‑only in class.

Maintainers perform the merge. You then **sync your fork** again.

---

## 9) Full Web lifecycle (soup to nuts)

1. Sync your fork (Section 2)
2. Commit locally and push to `origin main`
3. Open PR on GitHub (Section 4A Web)
4. Discuss + fix (push more commits)
5. If upstream moves, sync fork → push
6. Conflicts? resolve locally → push
7. Maintainer **Squash and merge**
8. Post‑merge hygiene: sync fork → push

### All commands you’ll run locally

``` bash
gh repo sync --source upstream --force
git push origin main
git add -p
git commit -m "..."
git push origin main

# if needed
git fetch upstream
git checkout main
git merge --ff-only upstream/main
git push origin main
```

---

## 10) Full CLI lifecycle (no browser)

1. Sync fork
2. Commit and push
3. Create PR via CLI
4. Comment and check status
5. Update if upstream moves
6. Resolve conflicts locally
7. Maintainer merges
8. Post‑merge hygiene

### Commands

```bash
gh repo sync --source upstream --force
git push origin main
git add -p
git commit -m "..."
git push origin main
gh pr create --base main --head <you>:main --title "..." --body-file .github/pull_request_template.md
gh pr comment <number> -b "..."
gh pr status
gh pr checks <number>
gh repo sync --source upstream --force
git push origin main
git fetch upstream && git checkout main && git merge upstream/main && git push origin main
```

---

## 11) Undo and recovery (common rescues)

**Amend the last commit message**
```git commit --amend -m "fix: clearer message"```

**Unstage a file you accidentally added**
```git restore --staged path/to/file```

**Throw away local changes in a file**
```git restore --source=HEAD -- path/to/file```

### Revert a bad commit that has been pushed

```bash
git log --oneline
git revert <bad-commit-sha>
git push origin main
```

**Reset a local oops (before pushing)**
```git reset --hard HEAD~1```

**Stash WIP while you switch tasks**
```git stash push -m "wip: edit items form"```

### later

``` bash
git stash list
git stash pop
```

---

## 12) Tags and releases (optional, useful for milestones)

Create a tag locally and push:
```git tag -a v0.2.0 -m "Milestone: items search delivered"```
```git push origin v0.2.0```

Maintainers can turn tags into GitHub Releases.

---

## 13) Linking work (Issues, PRD, ADRs)

- In PR descriptions, reference issues using `Closes #123`.
- Link the relevant PRD section and ADR IDs so reviewers see context.
- Keep ADRs small and specific; one decision per record.

---

## 14) Collaboration recipes (fast reference)

**Assign yourself or request review (CLI)**
```gh pr create --assignee @me --reviewer user1,user2```

**Check out a teammate’s PR branch locally**
```gh pr checkout <number>```

**Open the PR in your browser (from CLI)**
```gh pr view --web```

---

## 15) Troubleshooting quick hits

- **PR shows no changes**: Did you push to your fork’s `main`? Compare must be `<your-username>:main` → `<course-org>:main`.
- **Auth errors**: run `gh auth status`; if needed, `gh auth login`.
- **Permission denied (publickey)**: confirm SSH keys or use HTTPS URL for remotes.
- **Merge conflict panic**: open the files shown by Git, choose correct sections, `git add` them, then `git commit`.

---

## 16) Appendix: Minimal file templates

### .github/pull_request_template.md

## Summary {what and why}

## Changes

- {bullets}

## How to Test

1) {steps}

## Risks / Rollback

- Risk: Low / Medium / High
- Rollback: git revert {merge-commit}

## Links

```PRD §<id>, ADR-<id>, Closes #<issue>```

### .github/copilot-instructions.md** (testing policy excerpt)

## Testing (MANDATORY)

- MUST use `python -m unittest` for pure Python modules.
- MUST use Django’s built‑in test runner: python manage.py test.
- MUST NOT add or suggest pytest or plugins; convert examples to unittest/Django TestCase.

---
