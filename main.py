#!/usr/bin/python
samples_per_second = 60
import math
import sched # https://docs.python.org/2/library/sched.html
import time

class find_ball_class:
    def update(self):
        return "find_ball", {["left"]=0.0,["right"]=0.0,["mouth"]="open"}

class return_ball_class:
    def update(self):
        return "return_ball", {["left"]=0.0,["right"]=0.0,["mouth"]="closed"}

class main_loop_class():
    def __init__(self):
        self.timer = sched.scheduler(time.time, time.sleep)
        self.seconds_running = 0.0
        
        self.active_mode = "find_ball"
        
        self.navigate = {}
        self.navigate["left"]  = 0.0
        self.navigate["right"] = 0.0
        self.navigate["mouth"] = "closed"

    def loop_code(self):
        print self.seconds_running
        # update ball state
        # update camera state
        # run find_ball AI if active
        if self.active_mode == "find_ball":
            self.active_mode, self.navigate = find_ball.update()
        # run return ball AI if active
        if self.active_mode == "return_ball":
            self.active_mode, self.navigate = return_ball.update()
        # update motors
        
    
    def do_nothing(self):
        return
    
    def loop(self):
        delta_time = 1.0 / samples_per_second
        while True:
            self.timer.enter(delta_time, 1, self.do_nothing, ())
            self.loop_code()
            # a check for a key press here would be nice for exiting safely
            self.seconds_running = self.seconds_running + delta_time
            self.timer.run()

puppy = main_loop_class()
puppy.loop()

