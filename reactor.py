# this is the top wrapper combining the hardware, model and real-time visualization.

import sys
import time


def print_help():
    print("usage: reactor.py command arg0 arg1 ..")
    print("required: command")
    print()
    print("example commands:")
    # temperature control
    print("set temperature reactor0 39.0 // [°C]")
    print("disable temperature reactor0")
    # peristaltic pumps
    print("set speed pump0 100.0 // [%]")
    print("disable speed pump0")
    print("set volume pump0 50 // [ml]")
    # od sensor
    print("enable sensor od0")
    print("disable sensor od0")
    print()


def event_loop():
    if not sys.stdin.isatty():  # check if input is available
        for line in sys.stdin:  # read lines

            command = line.split()  # split command into components

            # go through all command queries
            try:
                if len(command) == 0 or command[0] == "help":
                    print_help()
                elif command[0] == "enable":
                    if command[1] == "sensor":
                        pass # TODO
                elif command[0] == "disable":
                    if command[1] == "temperature":
                        pass # TODO
                    elif command[1] == "speed":
                        pass # TODO
                    elif command[1] == "sensor":
                        pass # TODO
                elif command[0] == "set":
                    if command[1] == "temperature":
                        pass # TODO
                    elif command[1] == "speed":
                        pass # TODO
                    elif command[1] == "volume":
                        pass # TODO
                else:
                    print_help()
            except:
                print("Invalid syntax, try again.")

if __name__ == "__main__":
    while True:
        event_loop()
        time.sleep(0.5)
# https://docs.python.org/2/library/threading.html#using-locks-conditions-and-semaphores-in-the-with-statement
# https://stackoverflow.com/questions/3762881/how-do-i-check-if-stdin-has-some-data