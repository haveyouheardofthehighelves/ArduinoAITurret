import pygame
import serial
import time
import math
import InputMonitor

pygame.init()
joysticks = []
clock = pygame.time.Clock()
keepPlaying = True
# ser = serial.Serial("COM3", 9600, timeout=0)

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


def mapper(x, leftmin, leftmax, rightmin, rightmax):
    lspan = leftmax - leftmin
    rspan = rightmax - rightmin
    scaled = float(x - leftmin) / float(lspan)
    return rightmin + (scaled * rspan)


def writetoarduino(writeall):
    arr = bytes(writeall, 'utf-8')
    # ser.write(arr)


servoAngle = 90
prevscale = 0
check = InputMonitor.InputMonitor()


def servo_shenanigans(joyinput, manual_sens):
    global servoAngle
    global prevscale
    scaled_up = round(joyinput * manual_sens)
    prevscale = scaled_up
    if servoAngle < 180 and scaled_up > 0:
        if servoAngle + scaled_up > 180:
            servoAngle = 180
            return True
        else:
            servoAngle += scaled_up
            return True
    elif servoAngle > 0 and scaled_up < 0:
        if servoAngle + scaled_up < 0:
            servoAngle = 0
            return True
        else:
            servoAngle += scaled_up
            return True
    else:
        prevscale = 0
    return False


def findController():
    # for al the connected joysticks
    for i in range(0, pygame.joystick.get_count()):
        # create an Joystick object in our list
        joysticks.append(pygame.joystick.Joystick(i))
        # initialize the appended joystick (-1 means last array item)
        joysticks[-1].init()
        # print a statement telling what the name of the controller is
        print("Detected joystick "), joysticks[-1].get_name(), "'"


def StartGame():
    global servoAngle
    findController()
    while keepPlaying:
        clock.tick(60)
        if prevscale != 0:
            if not ((servoAngle == 180 and prevscale > 0) or (servoAngle == 0 and prevscale < 0)):
                servoAngle += prevscale
                if servoAngle > 180:
                    servoAngle = 180
                elif servoAngle < 0:
                    servoAngle = 0
                writetoarduino(f'{180 - servoAngle}s')

        for event in pygame.event.get():
            # The 0 button is the 'a' button, 1 is the 'b' button, 2 is the 'x' button, 3 is the 'y' button
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    if servo_shenanigans(event.value):
                        writetoarduino(f'{180 - servoAngle}s')
                if event.axis == 4:
                    if round(event.value) == 1:
                        check.flywheels = True
                        writetoarduino(f'1m')
                    else:
                        check.flywheels = False
                        writetoarduino(f'0m')
                if event.axis == 5:
                    if round(event.value) == 1:
                        check.solenoid = True
                        writetoarduino(f'1p')
                    else:
                        check.solenoid = False
                        writetoarduino(f'0p')
            if event.type == pygame.JOYBUTTONUP:
                if event.button == 7:
                    check.start_button = True
        check.angle = 180 - servoAngle
