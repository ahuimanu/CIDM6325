
---

# TOC
[git-command-sequence--workflow-reference](#git-command-sequence--workflow-reference)



# Git Command Sequence & Workflow Reference**

## **1. Initial Setup**

### **Clone an existing repository**

```bash
git clone https://github.com/USERNAME/REPO.git
cd REPO
```

### **Set global identity**

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

---

## **2. Remote Management (origin & upstream)**

### **Check existing remotes**

```bash
git remote -v
```

### **Add upstream (for fork workflows)**

```bash
git remote add upstream https://github.com/ORIGINAL_OWNER/REPO.git
```

### **Verify**

```bash
git remote -v
```

---

## **3. Sync With Upstream**

### **Fetch latest metadata**

```bash
git fetch upstream
```

### **Merge upstream main into your local main**

```bash
git checkout main
git merge upstream/main
```

### **Push synced main back to origin**

```bash
git push origin main
```

---

## **4. Branching Strategy**

### **Create a feature branch**

```bash
git checkout -b feature/my-feature
```

### **Switch between branches**

```bash
git checkout main
git checkout feature/my-feature
```

### **List branches**

```bash
git branch
git branch -a
```

---

## **5. Stage, Commit, and Push**

### **Stage changes**

```bash
git add .
```

### **Commit with message**

```bash
git commit -m "Clear, formal commit message"
```

### **Push branch**

```bash
git push -u origin feature/my-feature
```

---

## **6. Keeping Feature Branch Updated**

### **Update local main**

```bash
git checkout main
git pull upstream main
```

### **Rebase your branch onto updated main**

```bash
git checkout feature/my-feature
git rebase main
```

### **Force-push after rebase**

```bash
git push --force-with-lease
```

---

## **7. Pull Requests (PR workflow)**

1. Push feature branch
2. Open PR from:
   **your-fork/feature/my-feature → upstream/main**
3. Ensure no merge conflicts
4. Request review
5. Merge via Squash or Rebase (recommended)

---

## **8.Backup Workflow**

### **Create backup branch**

```bash
git checkout -b backup/pre-major-change
git push origin backup/pre-major-change
```

### **Temporary archive tag**

```bash
git tag backup-2025-01-15
git push origin --tags
```

### **Local stash**

```bash
git stash
git stash list
```

### **Apply or drop stash**

```bash
git stash apply
git stash drop
```

---

## **9. Restore, Revert, Reset**

### **Restore a file**

```bash
git restore path/to/file
```

### **Restore entire working tree**

```bash
git restore .
```

### **Revert a commit (safe, keeps history)**

```bash
git revert <commit-hash>
```

### **Soft reset (keep changes staged)**

```bash
git reset --soft <commit-hash>
```

### **Mixed reset (default, unstage but keep files)**

```bash
git reset <commit-hash>
```

### **Hard reset (dangerous, wipes changes)**

```bash
git reset --hard <commit-hash>
```

---

## **10. Cleaning Workspace**

### **Remove untracked files**

```bash
git clean -fd
```

### **Check before deleting**

```bash
git clean -fd --dry-run
```

---

## **11. Standard Release Preparation**

### **Create release branch**

```bash
git checkout -b release/v1.0
```

### **Tag final release**

```bash
git tag -a v1.0 -m "Release 1.0"
git push origin --tags
```

---

## **12. Common Layout Summary**

### **Remote Layout**

```
origin     → your fork
upstream   → original repository
```

### **Branch Layout**

```
main                      → stable base
feature/xxxx              → new features
bugfix/xxxx               → issue-specific fix
backup/pre-major-change   → archived state
release/1.0               → release staging
```

### **Typical Daily Sequence**

```
1. git checkout main
2. git pull upstream main
3. git push origin main
4. git checkout -b feature/new-task
5. work...
6. git add .
7. git commit -m "Work summary"
8. git push origin feature/new-task
9. open PR
```

---

**Pull Requests (PR workflow)** and **Merge Conflict handling**.
You can append this directly to your Git cheat sheet.

---

# **PR & MERGE CONFLICT CHEAT SHEET (ONE PAGE)**

## **1. Creating a Pull Request**

### **Standard workflow**

```bash
git checkout main
git pull upstream main
git checkout feature/<name>
git rebase main
git push --force-with-lease
```

### **Open PR**

* Source: `your-fork / feature/<name>`
* Target: `upstream / main`
* Provide:

  * Clear title
  * Purpose summary
  * List of changes
  * Testing notes

---

## **2. Updating a PR**

When reviewer requests changes:

```bash
# make edits
git add .
git commit -m "Address reviewer feedback"
git push
```

If main has moved forward:

```bash
git fetch upstream
git rebase upstream/main
git push --force-with-lease
```

---

## **3. Detecting Merge Conflicts**

Conflicts occur during:

```bash
git merge main
git rebase main
```

or when GitHub reports: **“This branch has conflicts that must be resolved”**

Check conflict files:

```bash
git status
```

Conflict markers inside files:

```
<<<<<<< HEAD
your changes
=======
upstream changes
>>>>>>> branch
```

---

## **4. Resolving Merge Conflicts**

### **Step-by-step**

1. Open each conflicted file
2. Manually resolve code blocks
3. Stage resolved files:

```bash
git add <file>
```

### **For merge:**

```bash
git merge --continue
```

### **For rebase:**

```bash
git rebase --continue
```

### **If things go wrong**

```bash
git merge --abort
git rebase --abort
```

---

## **5. Using Rebase to Keep PR Clean**

### **Rebase your feature branch on top of main**

```bash
git checkout feature/<name>
git fetch upstream
git rebase upstream/main
git push --force-with-lease
```

This avoids noisy merge commits and ensures a linear history.

---

## **6. Squash Before Merging (Clean History)**

Interactive squash:

```bash
git rebase -i HEAD~5
```

Mark commits as:

```
pick
squash
```

Push updated branch:

```bash
git push --force-with-lease
```

---

## **7. Finishing the PR**

* Ensure **CI passes**
* Ensure **all comments resolved**
* Prefer **Squash & Merge** or **Rebase & Merge**
* Delete feature branch after merging

Delete locally:

```bash
git branch -d feature/<name>
```

Delete remote:

```bash
git push origin --delete feature/<name>
```

---

## **8. Practical Conflict Examples**

### **Conflict during merge**

```bash
git merge main
# resolve files
git add <file>
git merge --continue
```

### **Conflict during rebase**

```bash
git rebase upstream/main
# resolve files
git add <file>
git rebase --continue
```

### **Skip a commit during rebase** *(only if appropriate)*:

```bash
git rebase --skip
```

---

## **9. Hard Situations & Rescue**

### **View conflicting commits**

```bash
git log --merge --oneline
```

### **Show diff of conflict**

```bash
git diff
```

### **Stash unfinished work**

```bash
git stash push --include-untracked
```

### **Apply stash after resolving**

```bash
git stash apply
```

---

# **Additional Items to Include in Your Git Notes**

## **1. Safety Nets & Recovery Tools**

### **Check history before modifying**

```bash
git log --oneline --graph --decorate --all
```

### **View changes in a commit**

```bash
git show <commit-hash>
```

### **Create a patch file (offline backup)**

```bash
git format-patch -1 <commit-hash>
```

### **Apply a patch**

```bash
git apply file.patch
```

---

## **2. Conflict Resolution Essentials**

### **When merge or rebase conflicts occur**

```bash
git status
```

### **Resolve files manually, then**

```bash
git add <resolved-file>
git rebase --continue
# or
git merge --continue
```

### **Abort rebase**

```bash
git rebase --abort
```

---

## **3. Commit Hygiene Standards**

**Include rules for clean commit history:**

* Use short, imperative titles.
* Add detailed body if needed.
* Avoid “WIP” commits.
* Squash noisy commits before merging.

### **Squash commits**

```bash
git rebase -i HEAD~5
```

---

## **4. Tagging Standards**

### **Lightweight tags**

```bash
git tag v1.2
git push origin v1.2
```

### **Annotated tags (recommended)**

```bash
git tag -a v1.2 -m "Release v1.2"
```

### **Delete a tag**

```bash
git tag -d v1.2
git push origin :refs/tags/v1.2
```

---

## **5. Tracking and Cleaning Branches**

### **List remote branches**

```bash
git branch -r
```

### **Delete local branch**

```bash
git branch -d feature/my-feature
```

### **Force delete**

```bash
git branch -D feature/my-feature
```

### **Delete remote branch**

```bash
git push origin --delete feature/my-feature
```

---

## **6. Shallow Operations for Speed**

### **Shallow clone**

```bash
git clone --depth=1 https://github.com/...
```

### **Deepen shallow clone**

```bash
git fetch --depth=50
```

---

## **7. Submodules (if applicable)**

### **Add a submodule**

```bash
git submodule add https://github.com/... path/submodule
```

### **Update all submodules**

```bash
git submodule update --init --recursive
```

---

## **8. Git Ignoring Standards**

### **Edit .gitignore**

Provide patterns like:

```
*.pyc
.env
__pycache__/
node_modules/
```

---

## **9. Annotated Diagram (recommended)**

Include a small layout visual in your note:

```
            ┌──────────────┐
            │   upstream    │
            │ original repo │
            └───────┬──────┘
                    │ fetch/pull
                    ▼
     ┌──────────────┐     push PR branch
     │   origin      │◄──────────────┐
     │ your fork     │               │
     └───────┬──────┘               │
             │ clone                 │
             ▼                       │
     ┌─────────────────────┐         │
     │   local workspace   │─────────┘
     ├─────────────────────┤
     │ main                │
     │ feature/my-feature  │
     │ backup/...          │
     └─────────────────────┘
```

---

## **10. Security Practices**

### **Prevent committing secrets**

```bash
git update-index --assume-unchanged .env
```

### **Scan for accidental secret leaks**

Use tools like:

* trufflehog
* git-secrets
* Gitleaks

---

## **11. Grep & Search Tools (extremely useful)**

### **Search code history**

```bash
git grep "function_name"
```

### **Search committed patches**

```bash
git log -S "keyword"
```

---

## **12. Performance Optimization**

### **Garbage collection**

```bash
git gc --aggressive
```

### **Prune old unreachable objects**

```bash
git prune
```

---

## **13. Aliases (recommended)**

Add to `~/.gitconfig`:

```ini
[alias]
  co = checkout
  br = branch
  ci = commit
  st = status
  lg = log --oneline --graph --decorate --all
```

---

## **14. Worktree (Multiple Working Directories)**

### **Create a parallel working directory**

```bash
git worktree add ../temp-work main
```

### **List worktrees**

```bash
git worktree list
```

---

## **15. Notes on LFS (Large File Storage)**

### **Track large files**

```bash
git lfs track "*.zip"
git add .gitattributes
```

---

# **If you want, I can now prepare:**

* A **single-page cheat sheet**
* A **canvas notebook**
* A **PDF-style clean reference sheet**
* A **diagram-focused version**

Just tell me the style you want.

