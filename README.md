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

## Type-checking the game
```sh
python -m mypy .
```
This scans the full workspace to ensure everything is typed properly, avoiding many otherwise-hard-to-catch bugs.
It's expected to do this and fix errors arising from it before committing.

## Running the game
```sh
python main.py
```

Controls: arrow keys to move, **P** or **ESC** to pause, **Enter** to select in menus, **S** on the title screen for Settings.

## How scenes work

Every screen (title, game, settings) is a file in `scenes/`. Each scene must be registered in main.py and impliment the following functions:

`init() -> None`
* Called whenever the scene is switched to

`deinit() -> None`
* Called immediately before the scene is switched away from

`event(pygame.Event) -> list[Message]`
* Called whenever there is a a pygame event
* Returns a list of Messages (can be empty), commands to be executed by the game manager. The commands are detailed below.

`update() -> list[Message]`
* Core game update logic goes in here
* Called only when the game is **unpaused**
* Returns a list of Messages (can be empty), commands to be executed by the game manager. The commands are detailed below.

`draw(screen: Surface) -> None`
* Modifies the screen by drawing the current scene to it
* Is NOT permitted to modify any scene variables. Any scene variable modification should be done in another function such as `input` or `update`

### Boilerplate
Copy-pastable code for creating new scenes
```python
from core.message import Message
import pygame

def init() -> None:
	pass

def deinit() -> None:
	pass

def event(e: pygame.Event) -> list[Message]:
	return []

def update() -> list[Message]:
	return []

def draw(screen: pygame.Surface) -> None:
	pass
```

### Commands
* `ChangeScene(new_scene: Scene)`. Accepts a scene name, switches to that scene on the next frame
* `Pause`. Pauses the game and opens the pause menu
* `Quit(message: str, failure: bool)`. Accepts a message, tagged with if it's a successful or not exit, quits on the next frame

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
