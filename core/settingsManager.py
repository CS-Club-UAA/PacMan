import json
from pathlib import Path


class SettingsManager:
    """Helper to wrap JSON settings with attribute-style access."""

    def __init__(self, json_path):
        self.json_path = Path(json_path)
        self._load()

    def _load(self):
        with self.json_path.open("r") as f:
            data = json.load(f)
        self._data = data
        # Recursively convert dicts to objects
        self._wrap_dicts(self._data)

    def _wrap_dicts(self, obj):
        for k, v in obj.items():
            if isinstance(v, dict):
                obj[k] = SettingsNode(v)

    def __getattr__(self, item):
        if item in self._data:
            return self._data[item]
        raise AttributeError(f"Settings has no attribute '{item}'")


class SettingsNode:
    """Wrap a dict for attribute-style access."""

    def __init__(self, data):
        self._data = data
        for k, v in data.items():
            if isinstance(v, dict):
                v = SettingsNode(v)
            setattr(self, k, v)

    def __getitem__(self, key):
        return getattr(self, key)
