import termios, fcntl, sys, os

from adafruit_motorkit import MotorKit

kit = MotorKit()

fd = sys.stdin.fileno()

oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)

oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

try:
    while 1:
        try:
            c = sys.stdin.read(1)
            if repr(c)=="w":
                print("forward")
            elif repr(c)=="s":
                print("backward")
            elif repr(c)=="a":
                print("left")
            elif repr(c)=="d":
                print("right")
            elif repr(c)=="z":
                print("stop")
        except IOError: pass
finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)