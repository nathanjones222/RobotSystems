# This is the line following program for part 3 of the intro to robotics 2 manual
import os
import sys
sys.path.append(os.path.abspath(os.path.join(
os.path.dirname(__file__), "..")))

from picarx.picarx_improved import Picarx
from time import sleep

px = Picarx()

from classes.sense import Sense
from classes.think import Think
sense = Sense()
think = Think()

if __name__=='__main__':
    try:
        while True:
            gm_val_list = sense.grayscale_data()
            gm_state = think.get_state(gm_val_list)
            print("gm_val_list: %s, %s"%(gm_val_list, gm_state))

            if gm_state != "stop":
                last_state = gm_state

            if gm_state == 'forward':
                px.set_dir_servo_angle(0)
                sleep(0.5)
                px.forward(think.speed_scaling()) 
            elif gm_state == 'left':
                px.set_dir_servo_angle(30)
                sleep(0.5)
                px.forward(think.speed_scaling()) 
            elif gm_state == 'right':
                px.set_dir_servo_angle(-30)
                sleep(0.5)
                px.forward(think.speed_scaling()) 
            else:
                px.stop()
    finally:
        px.stop()
        print("stop and exit")
        sleep(0.1)