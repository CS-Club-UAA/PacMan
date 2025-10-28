import pygame

pygame.init()
pygame.joystick.init()

# joysticks = []
# for i in range(pygame.joystick.get_count()):
#     joy = pygame.joystick.Joystick(i)
#     joy.init()
#     joysticks.append(joy)
#     print(f"Initialized joystick {i}: {joy.get_name()}")

joystick_controls = {
    "button_pressed": [],
    "axis": [0, 0]
}

running = True
while running:
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                running = False

            case pygame.JOYDEVICEADDED:
                print("Joystick added")
                joysticks = []
                for i in range(pygame.joystick.get_count()):
                    joy = pygame.joystick.Joystick(i)
                    joy.init()
                    joysticks.append(joy)
                    print(f"Initialized joystick {i}: {joy.get_name()}")
                pass
            case pygame.JOYDEVICEREMOVED:
                print("Joystick removed")
                pass

            case pygame.JOYBUTTONDOWN:
                for _ in range(event.button - len(joystick_controls["button_pressed"]) + 1):
                    joystick_controls["button_pressed"].append(False)
                
                joystick_controls["button_pressed"][event.button] = True
                print(joystick_controls)

                print(f"Button {event.button} pressed on joystick {event.instance_id}")
            case pygame.JOYBUTTONUP:
                for _ in range(event.button - len(joystick_controls["button_pressed"]) + 1):
                    joystick_controls["button_pressed"].append(False)
                print(joystick_controls)
                joystick_controls["button_pressed"][event.button] = False
                print(f"Button {event.button} released on joystick {event.instance_id}")

            case pygame.JOYAXISMOTION:
                joystick_controls["axis"][event.axis] = event.value
                print(f"Axis {event.axis} moved to {event.value} on joystick {event.instance_id}")


    # print(joystick_controls)
    
# [x, y] top left is -1 -1
