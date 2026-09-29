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
