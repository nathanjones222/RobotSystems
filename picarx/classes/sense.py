from robot_hat.adc import ADC

class Sense():
    def __init__(self, pin0: ADC = None, pin1: ADC = None, pin2: ADC = None):
        self.pins = (pin0, pin1, pin2)
    def grayscale_data(self, channel: int = None) -> list:
        if channel == None:
            return [self.pins[i].read() for i in range(3) if self.pins[i] is not None]
        else:
            if self.pins[channel] is not None:
                return self.pins[channel].read()
            else:
                return None
# def get_grayscale_data(self):
    #     grayscale_data = list.copy(grayscale.read())
    #     return grayscale_data
    
