
from classes.sense import Sense
sense = Sense()

class Think():
    # def read_status(self, datas: list = None) -> list:
    #     self._reference = grayscale.reference()
    #     if self._reference == None:
    #         raise ValueError("Reference value is not set")
    #     if datas == None:
    #         datas = sense.grayscale_data()
    #     return [0 if data > self._reference[i] else 1 for i, data in enumerate(datas)]
    def read_status(self, datas: list = None) -> list:
        if datas == None:
            datas = sense.grayscale_data()
        # higher grayscale value means darker color
        if abs(datas[0]) - abs(datas[1]) > 100:
            return [1, 0, 0]
        elif abs(datas[1]) - abs(datas[0]) > 100 or abs(datas[1]) - abs(datas[2]) > 100:
            return [0, 1, 0]
        elif abs(datas[2]) - abs(datas[1]) > 100:
            return [0, 0, 1]
        
    def speed_scaling(self, speed = 30):
        speed_scale = 1.0
        if self.read_status() == [1, 0, 0]:
            speed_scale = speed * abs(self.read_status()[0]) - abs(self.read_status()[1]) / 100
            speed = speed * speed_scale 
        elif self.read_status() == [0, 1, 0]:
            speed_scale = speed * abs(self.read_status()[1]) - abs(self.read_status()[0]) / 100
            speed = speed * speed_scale
        elif self.read_status() == [0, 0, 1]:
            speed_scale = speed * abs(self.read_status()[2]) - abs(self.read_status()[1]) / 100
            speed = speed * speed_scale
        return speed
    
    def get_state(self, gs_data):
        _state = self.read_status(gs_data)
        if _state == [0, 0, 0]:
            return 'stop'
        elif _state[1] == 1:
            return 'forward'
        elif _state[0] == 1:
            return 'right'
        elif _state[2] == 1:
            return 'left'