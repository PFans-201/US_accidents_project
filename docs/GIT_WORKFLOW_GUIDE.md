# Git Workflow Guide for US Accidents Project

## Current Repository Status

✅ **Repository**: https://github.com/PFans-201/US_accidents_project
✅ **README.md**: Updated and pushed to `develop` branch
✅ **Feature Branches**: All created and pushed to GitHub

### Branches Overview

| Branch | Status | Purpose |
|--------|--------|---------|
| `main` | Stable | Production-ready code |
| `develop` | Active | Integration branch |
| `feature/01-data-loading` | ✅ Pushed | Notebook 01 |
| `feature/02-osm-network` | ✅ Pushed | Notebook 02 |
| `feature/03-spatial-join` | ✅ Pushed | Notebook 03 |
| `feature/04-data-cleaning` | ✅ Pushed | Notebook 04 |
| `feature/05-eda` | Created | Notebook 05 (future) |
| `feature/06-feature-engineering` | Created | Notebook 06 (future) |
| `feature/07-modeling` | Created | Notebook 07 (future) |

---

## Daily Workflow

### 1. Start Working on a Notebook

```bash
# Switch to the appropriate feature branch
git checkout feature/05-eda

# Make sure you have latest changes
git pull origin feature/05-eda

# Start working in your notebook...
```

### 2. Save Your Progress (Commit Changes)

```bash
# Check what has changed
git status

# Add your notebook
git add notebooks/05_eda.ipynb

# Commit with descriptive message
git commit -m "notebook: Add initial EDA visualizations

- Create distribution plots for accident severity
- Analyze temporal patterns
- Generate correlation matrices"

# Push to GitHub
git push origin feature/05-eda
```

### 3. When Notebook is Complete

```bash
# Switch to develop branch
git checkout develop

# Merge your feature branch
git merge feature/05-eda

# Push merged changes
git push origin develop

# Switch to next feature branch
git checkout feature/06-feature-engineering
```

---

## Quick Commands Reference

### Check Status
```bash
git status                    # See changed files
git branch                    # See local branches
git branch -a                 # See all branches (local + remote)
git log --oneline --graph    # See commit history
```

### Work with Branches
```bash
git checkout <branch-name>           # Switch to branch
git checkout -b <new-branch>         # Create and switch to new branch
git merge <branch-name>              # Merge branch into current
git branch -d <branch-name>          # Delete local branch
```

### Sync with GitHub
```bash
git pull origin <branch-name>        # Get latest changes
git push origin <branch-name>        # Push your changes
git push --all origin                # Push all branches
```

### Common Tasks
```bash
# Undo uncommitted changes
git restore <file>

# Undo last commit (keep changes)
git reset --soft HEAD~1

# See what changed
git diff                      # Unstaged changes
git diff --staged            # Staged changes
git diff main develop        # Compare branches
```

---

## Commit Message Guidelines

Use this format for clear, searchable commit history:

### Format
```
<type>: <short description>

<optional detailed explanation>
<optional bullet points>
```

### Types
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `perf:` - Performance improvements
- `test:` - Adding tests
- `notebook:` - Notebook updates
- `data:` - Data-related changes

### Examples
```bash
# Good commits
git commit -m "feat: Add spatial indexing for faster joins"
git commit -m "fix: Resolve memory leak in data loading"
git commit -m "notebook: Complete EDA in notebook 05"
git commit -m "docs: Update installation instructions"

# Avoid
git commit -m "updates"           # Too vague
git commit -m "fixed stuff"       # Not descriptive
git commit -m "asdfasdf"          # Meaningless
```

---

## Working with Multiple Notebooks

### Scenario: Work on Multiple Notebooks Simultaneously

```bash
# Work on notebook 05
git checkout feature/05-eda
# ... make changes ...
git add notebooks/05_eda.ipynb
git commit -m "notebook: Add distribution analysis"
git push origin feature/05-eda

# Switch to notebook 06 without merging
git checkout feature/06-feature-engineering
# ... make changes ...
git add notebooks/06_feature_engineering.ipynb
git commit -m "notebook: Create temporal features"
git push origin feature/06-feature-engineering
```

Each feature branch is independent until you merge them!

---

## Merging Strategy

### Option 1: Merge to Develop (Recommended)
```bash
# Complete notebook in feature branch
git checkout feature/05-eda
git add notebooks/05_eda.ipynb
git commit -m "notebook: Complete EDA analysis"
git push origin feature/05-eda

# Merge to develop
git checkout develop
git merge feature/05-eda
git push origin develop
```

### Option 2: Create Pull Request on GitHub
1. Push your feature branch
2. Go to: https://github.com/PFans-201/US_accidents_project/pulls
3. Click "New pull request"
4. Select: `base: develop` ← `compare: feature/05-eda`
5. Add description and create PR
6. Review and merge on GitHub

---

## Helpful Scripts

### View All Branch Status
```bash
# Show all branches with last commit
git branch -v

# Show branches with remote tracking
git branch -vv
```

### Sync All Branches
```bash
# Get all updates from GitHub
git fetch --all

# Pull latest for current branch
git pull
```

### Clean Up Old Branches
```bash
# Delete local branch (after merging)
git branch -d feature/05-eda

# Delete remote branch
git push origin --delete feature/05-eda
```

---

## Troubleshooting

### Problem: "Your branch is behind 'origin/develop'"
```bash
git pull origin develop
```

### Problem: Merge conflict
```bash
# After git merge shows conflict
# 1. Open conflicted files
# 2. Resolve conflicts (remove <<<<<<, ======, >>>>>> markers)
# 3. Stage resolved files
git add <resolved-file>
# 4. Complete merge
git commit -m "merge: Resolve conflicts from feature/XX"
```

### Problem: Committed to wrong branch
```bash
# Undo last commit but keep changes
git reset --soft HEAD~1

# Switch to correct branch
git checkout <correct-branch>

# Commit again
git add .
git commit -m "Your message"
```

### Problem: Want to see changes between branches
```bash
# Compare two branches
git diff develop..feature/05-eda

# See file changes only
git diff --name-only develop..feature/05-eda
```

---

## Best Practices

1. **Commit Often**: Small, frequent commits are better than large ones
2. **Descriptive Messages**: Future you will thank present you
3. **One Feature Per Branch**: Don't mix unrelated work
4. **Push Regularly**: Backup your work to GitHub
5. **Pull Before Push**: Avoid conflicts
6. **Review Before Commit**: Check `git status` and `git diff`
7. **Branch Naming**: Use clear, descriptive names

---

## Next Steps

### For Your Current Work:
1. ✅ README.md updated and pushed to `develop`
2. ✅ Notebooks 01-04 in respective feature branches
3. 📝 Continue with Notebook 05 (EDA)

### Workflow for Notebook 05:
```bash
# Start work
git checkout feature/05-eda

# Create the notebook
# ... work in notebooks/05_eda.ipynb ...

# Commit and push
git add notebooks/05_eda.ipynb
git commit -m "notebook: Complete exploratory data analysis

- Statistical analysis of accident patterns
- Correlation analysis with road attributes
- Geographic and temporal visualizations
- Key insights documentation"
git push origin feature/05-eda

# When done, merge to develop
git checkout develop
git merge feature/05-eda
git push origin develop
```

---

## Resources

- **GitHub Repository**: https://github.com/PFans-201/US_accidents_project
- **Git Cheat Sheet**: https://education.github.com/git-cheat-sheet-education.pdf
- **Conventional Commits**: https://www.conventionalcommits.org/

---

**Questions?** Run these commands to check your status:
```bash
git status              # What's changed?
git branch -vv          # Where am I?
git log --oneline -5    # What have I done recently?
```
