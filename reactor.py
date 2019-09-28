# this is the top wrapper combining the hardware, model and real-time visualization.

import sys
import select
import time

def command1(test):
    print("command1: {}".format(test))

def command2():
    print("command 2")


def event_loop():
    if not sys.stdin.isatty():  # check if input is available
        for line in sys.stdin:  # read lines

            command = line.split()  # split command into components

            if command[0] == "help":
                pass
            elif command[0] == "cmd2":
                command2()


if __name__ == "__main__":
    while True:
        event_loop()
        time.sleep(0.5)
# https://docs.python.org/2/library/threading.html#using-locks-conditions-and-semaphores-in-the-with-statement
# https://stackoverflow.com/questions/3762881/how-do-i-check-if-stdin-has-some-data