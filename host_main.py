import os
import sys
import argparse
import serial
import struct
from time import sleep

# Start - Match these with MAX78000 application
SERIAL_BAUD = 115200
DATA_LEN = 4
# End

SERIAL_TOUT = 5 # Seconds

def print_result(filename, result):
    """ Print formatted result """
    print("{0}\t{1}".format(filename, result), end = '')
    
def input_value(sport):
        val = int(input("Enter your value: "))
        sport.write(struct.pack('i', val))
        
def send_value(sport, val):
        sport.write(struct.pack('i', val))

def main():
    """ main function """
    parser = argparse.ArgumentParser(description = "Test sending and receiving data from MAX78000 UART",
                                     formatter_class = argparse.RawTextHelpFormatter)
    parser.add_argument("-d", "--device",
                        required = True,
                        help = "Serial device connected to MAX78000.\n"
                               "Linux: /dev/ttyUSB0\n"
                               "Windows: COM3")

    args = parser.parse_args()

    # Open device with default description
    sport = serial.Serial(args.device, SERIAL_BAUD, timeout = SERIAL_TOUT)
    
    # input_value(sport)
    
    result = []
    
    # send range of values
    for i in range(0,10):
        send_value(sport, i)
        while 1:
            char = sport.read(1)
            if char == b'':
                print("Empty char received")
                break
            result.append(char.decode('utf-8'))
            if char == b'\n':
                result = "".join(result)
                print(result)
                result = []
                sport.reset_input_buffer()
                break
            sleep(0.1)
            
    # send user input value
    input_value(sport)
    while 1:
        char = sport.read(1)
        if char == b'':
            print("Empty char received")
        result.append(char.decode('utf-8'))
        if char == b'\n':
            result = "".join(result)
            print(result)
            result = []
            sport.reset_input_buffer()
        sleep(0.1)
    
if __name__ == "__main__":
    main()
