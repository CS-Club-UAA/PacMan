# UAA PacMan 

## Setting up venv (Virtual Environment)
```sh
python -m venv .venv # You can also create it in VSCode with Ctrl+Shift+P >Python: Create Environment
# Activate venv. On Windows: `.venv/Scripts/activate`
# VSCode should automatically activate it when making a new terminal
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> **Note:** This project uses [pygame-ce](https://pyga.me/) (Community Edition), not plain `pygame`.
> You still write `import pygame` in code. The two packages conflict, so if you have plain pygame
> installed, remove it first with `pip uninstall pygame`. A venv avoids this entirely.

## Running the game
```sh
python main.py
```

## Contributing (GitHub Flow)

`main` is the only long-lived branch, and it must always run. All work happens on short-lived branches:

1. **Start from the latest `main`:**
   ```sh
   git checkout main
   git pull
   git checkout -b feature/pellets   # or fix/settings-crash, etc.
   ```
   Use one branch per task. [TODO.md](TODO.md) items make good branches. Prefix with `feature/` for new things and `fix/` for bugs.
2. **Commit and push your branch:**
   ```sh
   git add <files>
   git commit -m "Add pellets and score"
   git push -u origin feature/pellets
   ```
3. **Open a Pull Request into `main`** on GitHub. Another member reviews it, and CI must pass.
4. **If `main` changed while you worked,** update your branch before merging:
   ```sh
   git fetch origin
   git merge origin/main
   ```
5. **Merge it, then delete the branch.** Keep branches small and short-lived (days, not weeks) so they don't drift from `main`.

Rules:
- Never push directly to `main`; everything goes through a PR.
- Stable versions are marked with tags (`v0.1`, `v0.2`, ...), not with separate branches. To try an old version, run `git checkout v0.1`.

### Cleaning up branches

You'll create many branches over time, but only a few should exist at once, because each one is deleted after it merges. Nothing is lost: the commits are already in `main`, and the PR page on GitHub keeps the discussion and has a **Restore branch** button.

- **On GitHub:** turn on *Settings → General → "Automatically delete head branches"* so merged branches are deleted automatically.
- **On your computer:** clean up your local copies after a merge:
  ```sh
  git checkout main
  git pull
  git branch -d feature/pellets   # delete your local copy of the merged branch
  git fetch --prune               # forget branches that were deleted on GitHub
  ```

If a branch is still open after a couple of weeks, the task is probably too big. Split it into smaller ones.

### Found a bug? Where to fix it

| Situation | Where to fix it |
|---|---|
| The feature is **not merged yet** (you or the reviewer found the bug during the PR) | **On the same feature branch.** It's part of finishing the feature. Push more commits and the PR updates automatically. |
| The feature is **already merged** into `main` | **On a new `fix/...` branch made from the latest `main`**, with its own PR. Don't reuse the old feature branch; it's deleted or out of date. |

Example: Pac-Man can eat pellets through walls. If the `feature/pellets` PR is still open, fix it there. If it merged last week, create `fix/pellets-through-walls` from `main`.

### Merging a PR: merge commit vs. squash

GitHub's merge button has a **▾** dropdown with these options (the repo admin controls which ones are allowed in *Settings → General → Pull Requests*):

| | **Create a merge commit** | **Squash and merge** |
|---|---|---|
| What lands on `main` | Every commit from the branch, plus a merge commit tying them together | One new commit containing all the PR's changes |
| History | Shows exactly how the work was done, including "fix typo" commits | Clean: one commit per PR, easy to read and easy to revert |
| Does git know the branch is merged? | **Yes**: the branch's commits are in `main` | **No**: the branch's original commits are *not* in `main` |

**Our default: merge commit.** Use squash only when a branch has lots of messy commits, and then **delete the branch right after merging**.

⚠️ **Never keep working on a branch after it was squash-merged.** Git doesn't know its commits are already in `main`, so the next PR from that branch will hit merge conflicts on every file you touched again. (This happened to us with `test-stable` and PR #7.) Start a fresh branch from the latest `main` instead:
```sh
git fetch origin
git checkout -b feature/next-thing origin/main
```
