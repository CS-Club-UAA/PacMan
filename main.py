from core.message import *
from core.scene import Scene
from pathlib import Path
from sys import exit
from typing import Any
import pygame

# Scene imports
import scenes.title
#import scenes.game_scene
#import scenes.settings_scene
# Pause is NOT a scene

# Scene -> module conversion done here to avoid cyclic dependencies
def scene_to_module(scene: Scene) -> Any:
    match scene:
        case Scene.Title:
            return scenes.title
        case Scene.Game:
            pass#return scenes.game
        case Scene.Settings:
            pass#return scenes.settings

BASE_DIR = Path(__file__).resolve().parent

def main() -> None:
    # == Shared runtime state ==
    # Either None to indicate the program should stay running, or Quit with the quit payload
    quit: None | Quit = None
    # Module of the current scene
    current_scene = scene_to_module(Scene.Title)

    # == Initialization code ==
    print("Starting Pac-Man...")

    # == Main game loop ==
    while quit == None:
        # Check if the current scene has the necessary functions. If not, quit with error
        try:
            current_scene.init
            current_scene.deinit
            current_scene.event
            current_scene.update
            current_scene.draw
        except:
            quit = Quit(
                message = current_scene.__file__ + " missing at least one required function (update, draw)",
                failure = True
            )
            break # Unable to continue, quit immediately, do not wait for any other processing to happen
        messages: list[Message] = []

        for e in pygame.event.get():
            messages.extend(current_scene.event(e))
            if e.type == pygame.QUIT:
                quit = Quit(
                    message = "Close initiated by user",
                    failure = False
                )

        messages.extend(current_scene.update())

        for message in messages:
            match message:
                case ChangeScene():
                    current_scene.deinit()
                    current_scene = scene_to_module(message.new_scene)
                    current_scene.init()
                case Quit():
                    quit = message

    # == Cleanup/Closing code ==
    if quit.failure:
        if quit.message == None:
            print("Unknown failure")
        else:
            print("FAILURE:")
            print("> " + quit.message)
        exit(1)
    else:
        if quit.message != None:
            print(quit.message)
        exit(0)
    # == End of program, nothing's run after this point ==


if __name__ == "__main__":
    main()
