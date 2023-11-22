class InputMonitor:
    def __init__(self):
        self.pressed = False
        self.angle = 90

    def getAngle(self):
        return self.angle

    def getPressed(self):
        return self.pressed
