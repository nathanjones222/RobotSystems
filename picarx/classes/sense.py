from robot_hat.adc import ADC

class Sense():
    def __init__(self, pin0: ADC, pin1: ADC, pin2: ADC, reference: int = None):
        self.pins = (pin0, pin1, pin2)
    def grayscale_data(self, channel: int = None) -> list:
        if channel == None:
            return [self.pins[i].read() for i in range(3)]
        else:
            return self.pins[channel].read()
# def get_grayscale_data(self):
    #     grayscale_data = list.copy(grayscale.read())
    #     return grayscale_data
    
