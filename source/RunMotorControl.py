import time
import Robot

import termios, fcntl, sys, os

# Set the trim offset for each motor (left and right).  This is a value that
# will offset the speed of movement of each motor in order to make them both
# move at the same desired speed.  Because there's no feedback the robot doesn't
# know how fast each motor is spinning and the robot can pull to a side if one
# motor spins faster than the other motor.  To determine the trim values move the
# robot forward slowly (around 100 speed) and watch if it veers to the left or
# right.  If it veers left then the _right_ motor is spinning faster so try
# setting RIGHT_TRIM to a small negative value, like -0.05, to slow down the right
# motor.  Likewise if it veers right then adjust the _left_ motor trim to a small
# negative value.  Increase or decrease the trim value until the bot moves
# straight forward/backward.
LEFT_TRIM = 0
RIGHT_TRIM = 0

fd = sys.stdin.fileno()

oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)

oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

# Create an instance of the robot with the specified trim values.
robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)

try:
    while 1:
        try:
            c = sys.stdin.read(1)
            if c=="w":
                print("forward")
                robot.forward(1)
            elif c=="s":
                print("backward")
                robot.backward(1)
            elif c=="a":
                print("left")
                robot.left(1)
            elif c=="d":
                print("right")
                robot.right(1)
            elif c=="z":
                print("stop")
                robot.stop()
            elif c=="x":
                print("exit")
                break
        except IOError: pass
finally:
    robot.stop()
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)