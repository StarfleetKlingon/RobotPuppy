import pyfirmata
import sched
import time

samples_per_second = 60

from Tkinter import *

class movement:
    def __init__(self): # def setup_arduino(): 
        self.board = pyfirmata.Arduino('/dev/ttyACM0')
        self.iter8 = pyfirmata.util.Iterator(self.board)
        self.iter8.start()
        
        self.pins = {}
        
        # motor shield enable pins; PWM allowed on these channels,
        # but not the individual outputs
        self.pins["enable_channel_left"]  = self.board.get_pin('d:9:p')  # enable outputs 0-1
        self.pins["enable_channel_right"] = self.board.get_pin('d:10:p') # enable outputs 2-3
        
        # power enabled to pins
        self.pins["left"]        = self.board.get_pin('d:8:o')  # motor out 1
        self.pins["claw_open"]   = self.board.get_pin('d:11:o') # motor out 2
        self.pins["right"]       = self.board.get_pin('d:12:o') # motor out 3
        self.pins["claw_closed"] = self.board.get_pin('d:13:o') # motor out 4
        
        # enable output pins initially
        self.pins["enable_channel_left"].write(1)
        self.pins["enable_channel_right"].write(1)
        
        # pretend these are constants
        self.claw_speed = 0.5
        self.mouth_time = 30
        
        # 0.0 is fully closed
        self.mouth_state = 0.0
        
        # intial position
        self.position = [ 0.0, 0.0 ] # [x,y] rotation 0 is y+
        self.rotation = 0.0 # in degrees; positive is clockwise
        
        # Rotation speed; adjusted by AI using the camera
        self.rotation_speed = 3.0 # degrees/power/delta direction/time tick
        
        self.all_stop()
    
    def drive_forward(self,speed):
        self.pins["enable_channel_left"].write(speed)
        self.pins["enable_channel_right"].write(speed)
        self.pins["left"].write(1)
        self.pins["right"].write(1)
    
    def open_claw(self):
        self.pins["enable_channel_left"].write(self.claw_speed)
        self.pins["enable_channel_right"].write(self.claw_speed)
        self.pins["claw_open"].write(1)
        self.pins["claw_closed"].write(0)
    
    def close_claw(self):
        self.pins["enable_channel_left"].write(self.claw_speed)
        self.pins["enable_channel_right"].write(self.claw_speed)
        self.pins["claw_open"].write(0)
        self.pins["claw_closed"].write(1)
    
    def all_stop(self):
        for pin in self.pins.values():
            pin.write(0)
    
    def test_driver():
        pins = setup_arduino()
        drive_forward(pins, 0.5)
        all_stop(pins)

########
# Temp

timer = sched.scheduler(time.time, time.sleep)
seconds_running = 0.0
delta_time = 1.0 / samples_per_second

def do_nothing():
    return
  
navigator = movement()

navigator.close_claw()
timer.enter(30 * delta_time, 1, do_nothing, ())
timer.run()
navigator.all_stop()

for i in range(5):
    print "*Aaaaaa*"
    navigator.open_claw()

    timer.enter(30 * delta_time, 1, do_nothing, ())
    timer.run()
      
    navigator.all_stop()
    print "Noms?"

    timer.enter(5, 1, do_nothing, ())
    timer.run()

    navigator.close_claw()
    print "Noms!"

    timer.enter(30 * delta_time, 1, do_nothing, ())
    timer.run()

    navigator.all_stop()
    print "Nom :)"
    
    timer.enter(5, 1, do_nothing, ())
    timer.run()

