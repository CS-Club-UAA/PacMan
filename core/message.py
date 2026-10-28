from core.scene import Scene
from dataclasses import dataclass

@dataclass
class ChangeScene:
    new_scene: Scene

@dataclass
class Pause:
    pass

@dataclass
class Quit:
    message: None | str # Message to print on exit, or none if not applicable
    failure: bool # If true, returns a nonzero error code

Message = ChangeScene | Pause | Quit
