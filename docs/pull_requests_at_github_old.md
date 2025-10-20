# CIDM 6325 — Pull Requests Two Ways (GitHub Website & GitHub CLI)

*A focused, copy‑paste‑ready tutorial that shows how to open, iterate on, and merge a Pull Request (PR) first via the GitHub website, then via the GitHub CLI (`gh`).*

---

## 0) Prerequisites (both methods)

* A local branch with your changes pushed to a **remote** (same repo or your fork).
  Minimal flow:

  * `git checkout -b feature/{{topic}}`
  * edit, `git add -p`, `git commit -m "feat: {{summary}}"`
  * `git push -u origin feature/{{topic}}`
* Know your target: **Base** = `main` (usually). **Compare/Head** = your branch.
* Have your project’s **PR template** handy (if provided) and links to PRD / ADR / Issues.

---

## 1) Open a PR — **GitHub Website**

### 1.1 Navigate to the compare view

1. Go to GitHub → repository → you’ll often see a banner: *“Compare & pull request”*. Click it.
  If you don’t see it: **Pull requests** tab → **New pull request** → set **base:** `main` and **compare:** `feature/{{topic}}`.

### 1.2 Fill out the PR form

* **Title**: Short, imperative (e.g., `feat: add item search form`).

* **Description**: Paste your PR template and complete it. Example:

  ## Summary

  Implements item search form and results list (PRD §2.1).

  ## Changes

  * Adds CBV + ModelForm for search
  * Wires template and partials
  * Basic tests (Django TestCase)

  ## How to Test

  1. Run migrations
  2. Visit /items

  ## Risks/Rollback

  * Low; revert with `git revert {{merge-commit}}`

  ## Links

  PRD §2.1, ADR-0101, Closes #123

* **Link issues**: Use `Closes #{{id}}` or the sidebar “Development → Link issues”.

* **Reviewers**: Add your instructor/teammates.

* **Draft**: If not ready for merge, mark as **Draft** (button near the Create PR button or drop‑down).

* Click **Create pull request**.

### 1.3 Keep the PR moving

* **Commits**: Push more commits to the same branch; the PR updates automatically.
* **Checks**: Wait for CI; click **Details** to see failures; push fixes.
* **Conversations**: Reply to comments; use “**Resolve conversation**” when addressed.
* **Files changed**: Use the *Viewed* checkbox to track your own review sweep.

### 1.4 Merge (recommended policy for class)

* If approved and green: click **Squash and merge** → confirm message → **Delete branch**.
* If you need to update from `main`: use **Update branch** or rebase locally and force‑with‑lease.

### 1.5 Optional website features

* **Convert to draft / Ready for review** buttons manage review state.
* **Auto‑merge**: enable (squash) once checks pass.
* **PR checks summary**: ask Copilot (if enabled) for a PR summary to help reviewers.

---

## 2) Open a PR — **GitHub CLI (`gh`)**

> Install: [https://cli.github.com](https://cli.github.com)
> Authenticate once: `gh auth login`

### 2.1 Create a PR from your current branch

``` bash
# From the repo root, on your feature branch with upstream set
gh pr create \
  --base main \
  --head feature/{{topic}} \
  --title "feat: add item search form" \
  --body-file .github/pull_request_template.md
```

* Omit `--head` if you’re already on that branch.
* Use `--web` to open the browser pre‑filled instead of finishing in the terminal.
* Use `--draft` to open as a draft.

**Common variations**
gh pr create --fill                 # Use commit messages to fill body
gh pr create --assignee @me         # Assign yourself
gh pr create --reviewer user1,user2 # Request reviews

### 2.2 View, check, and iterate

``` bash
gh pr view --web          # open PR in browser
gh pr status              # see current branch PR, CI status
gh pr checks              # view status checks (if enabled)
gh pr comment {{num}} -b "Please review the HTMX fragment pattern."
```

* Push new commits; the PR updates.
* To fetch & switch to a teammate’s PR branch: `gh pr checkout {{num}}`.

``` bash
# Mark ready (if draft)
gh pr ready {{num}}

# Merge with squash and delete branch
gh pr merge {{num}} --squash --delete-branch
```

Other merge modes: `--merge` (merge commit), `--rebase` (rebase + merge). For class, prefer **squash**.

### 2.4 Update from main (if needed)

``` bash
git fetch origin
git rebase origin/main
git push --force-with-lease
```

---

## 3) Same‑repo vs Fork‑and‑PR (quick note)

* **Same‑repo**: You have write access. Branch lives in the main repo. Simpler.
* **Fork‑and‑PR**: No write access. Branch lives in *your* fork; open PR back to upstream.

CLI helpers for fork flow:
gh repo fork --clone
git remote add upstream [git@github.com](mailto:git@github.com):{{org}}/{{repo}}.git
git fetch upstream && git checkout main && git merge upstream/main
git push origin main

Open PR from your forked branch: `gh pr create --base main --head {{your-username}}:feature/{{topic}}`

---

## 4) Quality Bar (what good looks like)

* **Scope**: One topic per PR; <= ~300 lines changed.
* **Commits**: Small, atomic; conventional messages (`feat:`, `fix:`, `docs:`…).
* **Description**: Template filled; testing steps included.
* **Links**: PRD section, ADR id, Issue (e.g., `Closes #123`).
* **CI**: All checks pass; you’ve re‑run flaky ones.
* **Review**: Comments addressed; conversations resolved.

---

## 5) Troubleshooting

* **PR includes unrelated commits** → You branched from an old base. Rebase onto `origin/main` and force‑with‑lease.
* **Can’t push** → Set upstream: `git push -u origin feature/{{topic}}`.
* **Branch out of date** → Click **Update branch** on the PR or rebase locally.
* **Accidentally pushed to `main`** → Create branch at that commit, revert on `main`, open PR from the branch.

---

## 6) Quick Reference

**Website**: Pull requests → New pull request → base vs compare → fill template → Create PR → Squash & merge.
**CLI**: `gh pr create --base main --title … --body-file …` → `gh pr view --web` → `gh pr merge --squash --delete-branch`.

*End of tutorial.*
