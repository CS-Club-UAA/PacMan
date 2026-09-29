# Pac-Man Clone: Code Review & TODO

Review of the `test-stable` branch, done 2026-09-28 and updated after `main` was merged in. Bugs marked ✅ were reproduced by running the code headless. The others come from reading the code.

---

## What's working well

- **Scene architecture.** `sceneHandler` gives every scene the same `handleEvent`, `gameUpdate`, `sceneRender` interface. `game.py` runs a clean *input → update → render → transition* loop, which is the standard game-loop shape.
- **Auto-registered scenes.** `sceneManager.load_all_scenes()` imports everything in `scenes/`, so a new scene is one new file plus `register_scene(...)` at the bottom. That makes it easy for several people to work in parallel.
- **Wall auto-tiling.** `_build_image_grid` computes a 4-bit neighbor mask (top/right/bottom/left) and uses it to pick the tile sprite. Real games do it the same way.
- **Buffered turning.** Keeping `desired_dir` separate from `curr_dir` means you can press a direction early and Pac-Man turns at the next opening. That's how the arcade game feels.
- **Tunnel wrap.** The `% GRID_WIDTH` in movement makes the side tunnel work with no special-case code.
- **Settings live in JSON** (`data/usrSettings.json`) and are read as `settings.video.resolution` instead of being hardcoded.
- **Portable paths.** `main.py` and `gameScene.py` build paths from `Path(__file__)`, so the game runs from any working directory.
- **Asset fallback.** If images fail to load, colored placeholder squares keep the game running.

## What you're doing well as a team

- The `FIX 1`–`FIX 7` comments in `gameScene.py` explain *why* each change was made. That's very useful for a learning club, so keep doing it.
- You use PRs, a lint workflow, and a venv with `requirements.txt`.
- You work in small steps: the maze and movement work before ghosts and pellets get added.

## What's going badly (fix these first)

1. **The settings menu doesn't work.** `SubMenu.handleEvent` *returns* the selected option, but `game.py` throws the return value away, so choosing an option does nothing. On top of that:
   - ✅ Moving the mouse on the first frame of the settings scene crashes with `AttributeError: 'SubMenu' object has no attribute 'font'`. The font is only created inside `sceneRender`, and `handleEvent` runs first.
   - ✅ Up/Down cycles through all 23 options while only 6 are visible, so the highlight disappears.
   - The ESC handler sets `menu_section = self.options.index(...)`, which gives a list position (e.g. 7), not a section number.
   - Section 3 uses `options[14:15]`, which leaves out its "Back" entry.
   - `sceneRender` calls `pygame.display.flip()` even though `game.py` already flips each frame.
   - ESC is read from `pressed_keys` (held), so one press fires on every frame.
2. **There are two copies of the settings menu.** `core/settingsManager.py::SettingsMenu` is an older, unused copy of `scenes/settingsMenu.py::SubMenu`. The old copy also has bugs:
   - ✅ `pygame.mixer.Sound.set_volume(level)` raises `TypeError` because it's called on the class, not on a sound object.
   - `change_resolution` swaps width and height (`[1]`, `[0]`) and uses `global res/screen`.
   - `1280,780` should be `1280,720`.
3. ~~**The pygame library isn't consistent.**~~ Fixed: the project now uses **pygame-ce** (`pygame-ce>=2.5.8` in `requirements.txt`). Plain pygame 2.6.1 has no installer for Python 3.14. The branch drift between `main` and `test-stable` has also been fixed by merging `main` in.
4. ~~**The CI lint job can't pass.**~~ Fixed: see P0. What it used to do wrong:
   - It tests Python 3.8 and 3.9, but the code uses `match` (Python 3.10+), so those runs fail with syntax errors.
   - It doesn't install pygame, so every import is flagged.
   - It uses the outdated `actions/setup-python@v3`.
5. ✅ **A joystick can stop Pac-Man dead.** An axis value like `0.2` rounds to `0`, so `desired_dir` becomes `(0, 0)` and Pac-Man stops. There's no deadzone. The joystick code also never opens a `pygame.joystick.Joystick`, so on most setups joystick events never arrive at all.
6. ✅ **Pac-Man slides into walls.** When he's blocked, the render interpolation keeps drawing him 0.1–0.9 tiles *inside* the wall, then snaps him back. This repeats every 10 frames.

---

## TODO

### P0: Bugs / broken features
- [x] ~~Merge `main` into `test-stable`~~ (done).
- [x] ~~Agree on a branch workflow~~ (decided: **GitHub Flow**, see "Contributing" in the README).
- [ ] Switch over to GitHub Flow:
  - [ ] Open a PR from `test-stable` into `main` and merge it, so `main` has the latest work (pygame-ce, TODO, settings menu).
  - [ ] Check the old `dev` branch for work that never reached `main`. It has 14 commits from Nov 2025 that are in neither `main` nor `test-stable`. Rescue anything still needed, then delete `dev`.
  - [ ] Delete `test-stable` once it's merged.
  - [ ] Turn on branch protection for `main` on GitHub: require a PR, one approving review, and passing CI.
  - [ ] Tag the first working version: `git tag v0.1 && git push origin v0.1`.
- [x] ~~Choose **pygame** or **pygame-ce**~~ (done: pygame-ce).
- [ ] Every member: recreate your venv and reinstall from `requirements.txt` (see README). Uninstall plain `pygame` first if you have it.
- [ ] Settings menu:
  - [ ] Create `self.font` in `__init__`, not in `sceneRender`.
  - [ ] Act on the selection *inside* `handleEvent`; don't return it.
  - [ ] Clamp `selected_option` to the options currently shown.
  - [ ] Do mouse hit-testing only against the options shown.
  - [ ] Handle ESC as a `KEYDOWN` event, not a held key.
  - [ ] Remove `pygame.display.flip()` from `sceneRender`.
  - [ ] Fix the `[14:15]` slice.
- [ ] Replace the flat 23-item options list with a nested structure, e.g. `{"Graphics": ["Resolution", "Fullscreen", "Back"], ...}`. That removes all the magic slice numbers.
- [ ] Delete `SettingsMenu` from `core/settingsManager.py`, or move the working pieces (volume, fullscreen) into the scene and fix them. Volume should use `pygame.mixer.music.set_volume` plus `sound.set_volume` on each `Sound` object.
- [ ] Stop the wall-sliding render: only interpolate when the next tile is walkable. Better: move by a fraction of a tile each frame (see P1).
- [ ] Joystick:
  - [ ] Add a deadzone, e.g. ignore `abs(value) < 0.5`.
  - [ ] Never set the direction to `(0, 0)`.
  - [ ] Open joysticks on `JOYDEVICEADDED`.
- [x] ~~Use `pygame.key.key_code(name)` for key bindings~~ (done, came in from `main`).
- [ ] Wire up the unused `pause` key binding.
- [x] ~~Fix CI~~ (done): tests Python 3.10–3.14, installs `requirements.txt`, uses `checkout@v7` / `setup-python@v7`, and `.pylintrc` fixes the pygame false errors. Add new Python versions to the matrix as they come out.
- [ ] Clean up pylint warnings (score 7.64/10: naming, docstrings, unused variables/imports), then raise `fail-under` in `.pylintrc` so the score can't drop.
- [x] ~~`game.py`: remove the `settings=None` default~~ (done, came in from `main`).
- [ ] `game.py`: remove the unused imports (`Path`, `SettingsManager`).

### P1: Core gameplay (the actual Pac-Man)
- [ ] **Store more than wall / empty in the maze.** `0` currently means both "walkable path" and "empty space outside the maze". Use values such as `WALL, PELLET, POWER_PELLET, EMPTY, GHOST_DOOR`, or load the maze from a text file in `data/`:
  ```
  ############################
  #............##............#
  #.####.#####.##.#####.####.#
  #o####.#####.##.#####.####o#
  ```
- [ ] Pellets and power pellets: eating them, a score, and a win when the board is cleared.
- [ ] Use `dt` for movement. Speed is currently "1 tile per 10 frames", so it changes with the FPS setting. Move by `speed * dt` tiles and switch tiles when you cross a tile center.
- [ ] Ghosts: a base `Ghost` class plus Blinky, Pinky, Inky and Clyde targeting rules, with scatter, chase and frightened modes. The ghost house needs a door; it's currently fully walled in.
- [ ] Collisions between Pac-Man and ghosts, lives (`gameplay.lives` is already in the JSON), death, and game over.
- [ ] A HUD for score, high score, lives and level.
- [ ] A pause menu using the `P` binding. Opening Settings mid-game currently throws away the whole game, because scene changes create new instances.
- [ ] Pac-Man mouth animation, and sounds.

### P2: Code quality / structure
- [ ] Split `gameScene.py` into `entities/pacman.py`, `entities/ghost.py` and `world/maze.py`. Scenes should coordinate the pieces, not contain all the logic.
- [ ] Replace `XYPair` with `pygame.Vector2`. It already does `+ - *`, and it also supports `==`, which `XYPair` doesn't.
- [ ] Pick one naming style: PEP 8 means `snake_case` functions and `PascalCase` classes. Today `sceneHandler` is a lowercase class, methods mix camelCase and snake_case, and the game scene is registered as `"RGame"` instead of `"game"`.
- [ ] Make base-class methods `pass`, or raise `NotImplementedError`. The current `print` would spam the console every frame.
- [ ] `sceneHandler.endGame()` calls `pygame.quit()` in the middle of the loop, so the next frame would crash. Set a quit flag and let `game.py` exit instead.
- [ ] Remove unused code:
  - [ ] `current_scene` / `getCurrentScene` in `sceneHandler`
  - [ ] `SubMenu.selector`
  - [ ] the unused `text` variable in the mouse loop
  - [ ] the unused `width, height` in `SubMenu.__init__`
  - [ ] duplicate assets (`assets/tile_*.png` vs `assets/4x4/`, the unused `blue.png`, `tile_16.png`)
- [ ] Rename the misspelled `temperary_options` to `temporary_options`.
- [ ] `startScreen`:
  - [ ] Create fonts and text once in `__init__`, not every frame.
  - [ ] Remove the duplicate `start_rect` / `text_rect`.
  - [ ] Stop calling `set_caption` every frame.
  - [ ] Make Settings and Quit reachable by keyboard.
- [ ] Pre-scale tile images once when the resolution changes. Right now `transform.scale` runs about 870 times per frame (2.8 ms/frame measured; fine for now, but it adds up).
- [ ] Scenes read `settings.video.resolution`; use `screen.get_size()` instead so layout stays right in fullscreen.
- [ ] Use ESC instead of DELETE to leave the game scene.

### P3: Settings persistence
- [ ] Add `SettingsManager.save()`. `_data` currently holds `SettingsNode` objects, so it can't be `json.dump`ed; keep the raw dict separately.
- [ ] Apply the settings that already exist in the JSON but are never read: `vsync`, `scale`, `audio.*`, `gameplay.*`, `debug.*` (e.g. an FPS counter, collision boxes).
- [ ] Add `fps` to the JSON (the code already reads it, with a default of 60).
- [ ] Commit a `usrSettings.default.json` and gitignore the user's own copy, so personal settings don't create merge conflicts.

### P4: Project hygiene
- [ ] Expand the README. It has venv setup now; add how to run, controls, folder layout, and how to add a scene.
- [ ] Add a few `pytest` tests for code that doesn't need a window: `isValidMove`, auto-tile bitmasks, tunnel wrap, settings loading.
- [ ] Write GitHub issues for the P1 items so club members can claim them.
