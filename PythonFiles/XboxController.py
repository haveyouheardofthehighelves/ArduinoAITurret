import pygame
import serial

pygame.init()
joysticks = []
clock = pygame.time.Clock()
keepPlaying = True
ser = serial.Serial("COM7", 9600, timeout=0)
ser.xonxoff = 1

'''
Left Stick:
Left -> Right   - Axis 0
Up   -> Down    - Axis 1

Right Stick:
Left -> Right   - Axis 4
Up   -> Down    - Axis 3

RT  AXIS 4
LT AXIS 5
'''

# for al the connected joysticks
for i in range(0, pygame.joystick.get_count()):
    # create an Joystick object in our list
    joysticks.append(pygame.joystick.Joystick(i))
    # initialize the appended joystick (-1 means last array item)
    joysticks[-1].init()
    # print a statement telling what the name of the controller is
    print("Detected joystick "), joysticks[-1].get_name(), "'"
while keepPlaying:
    clock.tick(60)
    for event in pygame.event.get():
        # The 0 button is the 'a' button, 1 is the 'b' button, 2 is the 'x' button, 3 is the 'y' button
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                value = 'abcd'
                array = bytearray(value.encode('utf-8'))
                ser.write(array)
                print(event)
            if event.axis == 4 or event.axis == 5:
                print(event)
