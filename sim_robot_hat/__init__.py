#!/usr/bin/env python3
"""
Robot Hat Library
"""

# addition of fileDB to the init code
from .filedb import fileDB
from .adc import ADC
from .i2c import I2C
from .modules import *
from .music import Music
from .motor import Motor, Motors
from .pin import Pin
from .pwm import PWM
from .servo import Servo
from .tts import TTS
from .utils import *
from .robot import Robot
from .version import __version__

# create mocks of hardware variables
import platform

# Platform-specific bypass for Windows
if platform.system() == 'Windows':
    print("Running in Windows environment. Mocking hardware initialization.")
    from gpiozero import Device
    from gpiozero.pins.mock import MockFactory

    # Set the pin factory to MockFactory
    Device.pin_factory = MockFactory()

    # Now you can use GPIO-based code without actual hardware
    # Mock classes or methods here
    class MockServo:
        def __init__(self, channel, *args, **kwargs):
            print(f"Mocking Servo on Windows. Channel: {channel}")
            self.channel = channel
            self._angle = 0  # Default angle for mocked servo
    
        def angle(self, angle=None):
            if angle is not None:
                print(f"Setting angle for servo on channel {self.channel} to {angle} degrees")
                self._angle = angle  # Set the angle in the mocked servo
            else:
                print(f"Getting angle for servo on channel {self.channel}: {self._angle} degrees")
                return self._angle  # Return the mocked angle
    class MockI2C:
        def scan(self):
            print("Mocking I2C scan. No devices found.")
            return []
    class MockPWM:
        def __init__(self, channel, *args, **kwargs):
            print(f"Mocking PWM on Windows. Channel: {channel}")
            self.channel = channel
            # Initialize PWM mock settings here if necessary
    
        def scan(self):
            """Mocked scan function for Windows"""
            print(f"Mocking scan for PWM on channel {self.channel}. No actual devices.")
            return []  # Return an empty list to simulate no devices found

        def set_pwm(self, value):
            """Mocked function to set PWM value"""
            print(f"Setting PWM value for channel {self.channel} to {value}")
            # Logic for setting PWM value on Windows (mocked)

        def period(self, period_value):
            """Mocked period function for Windows"""
            print(f"Setting period for PWM on channel {self.channel} to {period_value}")
            # Mock setting the period value (you can add further logic if needed)
            self.period_value = period_value  # Store the period value if needed
        def prescaler(self, prescaler_value):
            """Mocked prescaler function for Windows"""
            print(f"Setting prescaler for PWM on channel {self.channel} to {prescaler_value}")
            # Mock setting the prescaler value (you can store or use it for further logic)
            self.prescaler_value = prescaler_value  # Store the prescaler value if needed
    class MockADC(ADC):  # Inherit from the real ADC class
        def __init__(self, *args, **kwargs):
            # Set the default I2C address or allow it to be passed as a parameter
            self.ADDR = kwargs.get('address', 0x48)  # Default address: 0x48
            print(f"Mocking ADC on Windows. Address: {hex(self.ADDR)}")

        def scan(self):
            """Mocked scan function for ADC on Windows"""
            print(f"Mocking scan for ADC. No actual devices.")
            return []  # Return an empty list to simulate no devices found

        def read(self):
            """Mocked read function for ADC"""
            print(f"Mocking read on ADC. Returning a fixed value.")
            return 0  # Return a fixed value (you can adjust this for testing)


    # Use the mocked classes for Servo, I2C, PWM, etc.
    Servo = MockServo
    I2C = MockI2C
    PWM = MockPWM
    ADC = MockADC
    # Similarly mock any other hardware classes like PWM, GPIO if needed.

def __usage__():
    print('''
    Usage: robot_hat [option]

    reset_mcu               reset mcu on robot-hat
    enable_speaker          enable speaker (drive high gpio 20)
    disable_speaker         disable speaker (drive low gpio 20)
    version                 get firmware version
    ''')
    quit()

def get_firmware_version():
    ADDR = [0x14, 0x15]
    VERSSION_REG_ADDR = 0x05
    i2c = I2C(ADDR)
    version = i2c.mem_read(3, VERSSION_REG_ADDR)
    print(f"Robot HAT Firmare version: {version[0]}.{version[1]}.{version[2]}")

def __main__():
    import sys
    import os
    if len(sys.argv) == 2:
        if sys.argv[1] == "reset_mcu":
            reset_mcu()
            print("Onboard MCU reset.")
        elif sys.argv[1] == "enable_speaker":
            print("Enable Speaker.")
            os.popen("pinctrl set 20 op dh")
        elif sys.argv[1] == "disable_speaker":
            print("Enable Speaker.")
            os.popen("pinctrl set 20 op dl")
        elif sys.argv[1] == "version":
            get_firmware_version()
        else:
            __usage__()
    else:
        __usage__()
