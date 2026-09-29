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
4. **Merge it, then delete the branch.** Keep branches small and short-lived (days, not weeks) so they don't drift from `main`.
5. **If `main` changed while you worked,** update your branch before merging:
   ```sh
   git fetch origin
   git merge origin/main
   ```

Rules:
- Never push directly to `main`; everything goes through a PR.
- Stable versions are marked with tags (`v0.1`, `v0.2`, ...), not with separate branches. To try an old version, run `git checkout v0.1`.
