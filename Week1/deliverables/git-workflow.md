# Git Workflow Example

A standard feature-branch workflow ending in a pull request.

```bash
# 1. Start from an updated main branch
git checkout main
git pull origin main

# 2. Create a feature branch
git checkout -b feature/items-endpoint

# 3. Do the work, then stage and commit
git add .
git commit -m "Add GET and POST /items endpoints with validation"

# 4. Push the branch to the remote
git push origin feature/items-endpoint

# 5. Open a Pull Request (on GitHub/GitLab) from
#    feature/items-endpoint  ->  main
#    Add a short description of what changed and how to test it.

# 6. After review & approval, the PR is merged into main.
```

## Good commit message habits
- Write in the imperative: "Add validation", not "Added validation".
- Keep the first line short (~50 chars); add detail in the body if needed.
- One logical change per commit.
