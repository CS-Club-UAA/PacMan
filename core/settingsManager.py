import json
from pathlib import Path


def _merge(base, override):
    """Recursively copy values from override into base."""
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _merge(base[k], v)
        else:
            base[k] = v


class SettingsManager:
    """Helper to wrap JSON settings with attribute-style access.

    The defaults file is committed and never written to. When a player
    changes a setting, save() writes their copy to user_path (gitignored).
    On load, the user's copy is layered on top of the defaults, so new
    settings added to the defaults later still show up.
    """

    def __init__(self, defaults_path, user_path):
        self.defaults_path = Path(defaults_path)
        self.user_path = Path(user_path)
        self._load()

    def _load(self):
        with self.defaults_path.open("r") as f:
            data = json.load(f)
        if self.user_path.exists():
            with self.user_path.open("r") as f:
                _merge(data, json.load(f))
        self._root = SettingsNode(data)

    def save(self):
        """Write the current settings to the user's copy."""
        with self.user_path.open("w") as f:
            json.dump(self._root.to_dict(), f, indent=4)

    def __getattr__(self, item):
        return getattr(self._root, item)


class SettingsNode:
    """Wrap a dict for attribute-style access.

    Reads and writes go straight to the underlying dict, so
    `settings.video.fullscreen = True` followed by save() is all it takes.
    """

    def __init__(self, data):
        object.__setattr__(self, "_data", data)

    def __getattr__(self, key):
        if key not in self._data:
            raise AttributeError(f"Settings has no attribute '{key}'")
        value = self._data[key]
        return SettingsNode(value) if isinstance(value, dict) else value

    def __setattr__(self, key, value):
        self._data[key] = value

    def __getitem__(self, key):
        return getattr(self, key)

    def to_dict(self):
        return self._data
