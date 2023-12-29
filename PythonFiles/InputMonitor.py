class InputMonitor:
    def __init__(self):
        self.start_button = False
        self.angle = 90
        self.solenoid = False
        self.flywheels = False
        self.AI_sens = 0
        self.Manual_sens = 2

    def getAngle(self):
        return self.angle

    def getPressed(self):
        return self.start_button

    def __str__(self):
        return f'start_button: {self.start_button}, angle:{self.angle}, solenoid:{self.solenoid}, flywheels:{self.flywheels}, Manual_Sens:{self.Manual_sens}'
