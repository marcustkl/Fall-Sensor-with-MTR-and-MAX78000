# usage: sudo python stream_acc_gyro_bmi1.py
from __future__ import print_function
from multiprocessing.dummy import Value
from mbientlab.metawear import MetaWear, libmetawear, parse_value
from mbientlab.metawear.cbindings import *
from time import sleep
from threading import Event
from queue import Queue
from copy import deepcopy

import os
import argparse
import serial
import struct
import platform
import sys

# Start - Match these with MAX78000 application
SERIAL_BAUD = 115200
DATA_LEN = 4*6
# End

SERIAL_TOUT = 5 # Seconds

# Sensor Classes and Functions
class State:
    # init state
    def __init__(self, device, sport):
        self.device = device
        self.samples = 0
        self.accCallback = FnVoid_VoidP_DataP(self.acc_data_handler)
        self.gyroCallback = FnVoid_VoidP_DataP(self.gyro_data_handler)
        self.gyro_reading = []
        self.sport = sport

    # gyro callback function
    def gyro_data_handler(self, ctx, data):
        value = deepcopy(parse_value(data))
        self.gyro_reading = [value.x, value.y, value.z]

    # acc callback function
    def acc_data_handler(self, ctx, data):
        value = deepcopy(parse_value(data))
        gyro = self.gyro_reading
        acc = [value.x, value.y, value.z]
        # [acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z]
        value_acc_gyro = acc + gyro
        # round to 6 dp
        value_acc_gyro = [round(num, 6) for num in value_acc_gyro]

        # to verify value list
        # print("ACC: %s GYRO: %s" % (value_acc_gyro[0:3], value_acc_gyro[3:]))

        # send readings to MAX78000
        # value_acc_gyro = [acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z]
        self.send_readings(self.sport, value_acc_gyro)
        self.samples+= 1

    def send_readings(self, sport, readings):
        sport.reset_input_buffer()
        sport.write(struct.pack('ffffff', *readings))
        print("Sent Data: %s" % (readings))
        chars = sport.read_until()
        print(chars.decode("utf-8"))

# init uart serial interface

#  parse arguments
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

# init sensor

# connect to C5:DE:74:B6:AC:5F
address = 'C5:DE:74:B6:AC:5F'
d = MetaWear(address)
d.connect()
print("Connected to " + d.address)
state = State(d, sport)

# configure all metawear
libmetawear.mbl_mw_settings_set_connection_parameters(state.device.board, 7.5, 7.5, 0, 6000)
sleep(1.5)

# config gyro
libmetawear.mbl_mw_gyro_bmi160_set_range(state.device.board, GyroBoschRange._1000dps)
libmetawear.mbl_mw_gyro_bmi160_set_odr(state.device.board, GyroBoschOdr._25Hz)
libmetawear.mbl_mw_gyro_bmi160_write_config(state.device.board)

# config acc to 1hz, as 1 sec delay is needed on MAX78000 for uart receive
libmetawear.mbl_mw_acc_set_odr(state.device.board, 1)
libmetawear.mbl_mw_acc_set_range(state.device.board, 16.0)
libmetawear.mbl_mw_acc_write_acceleration_config(state.device.board)

# get gyro signal and subscribe
gyro = libmetawear.mbl_mw_gyro_bmi160_get_rotation_data_signal(state.device.board)
libmetawear.mbl_mw_datasignal_subscribe(gyro, None, state.gyroCallback)

# get acc signal and subscribe
acc = libmetawear.mbl_mw_acc_get_acceleration_data_signal(state.device.board)
libmetawear.mbl_mw_datasignal_subscribe(acc, None, state.accCallback)

# start gyro
libmetawear.mbl_mw_gyro_bmi160_enable_rotation_sampling(state.device.board)
libmetawear.mbl_mw_gyro_bmi160_start(state.device.board)

# start acc
libmetawear.mbl_mw_acc_enable_acceleration_sampling(state.device.board)
libmetawear.mbl_mw_acc_start(state.device.board)

# sleep until interrupted
# sleep(10.0)
loop = True
while loop:
    try:
        sleep(10)
    except KeyboardInterrupt:
        loop = False
        print("Keyboard Interrupted")

# breakdown metawear
# stop acc
libmetawear.mbl_mw_acc_stop(state.device.board)
libmetawear.mbl_mw_acc_disable_acceleration_sampling(state.device.board)

# stop gyro
libmetawear.mbl_mw_gyro_bmi160_stop(state.device.board)
libmetawear.mbl_mw_gyro_bmi160_disable_rotation_sampling(state.device.board)

# unsubscribe acc
acc = libmetawear.mbl_mw_acc_get_acceleration_data_signal(state.device.board)
libmetawear.mbl_mw_datasignal_unsubscribe(acc)

# unsubscribe gyro
gyro = libmetawear.mbl_mw_gyro_bmi160_get_rotation_data_signal(state.device.board)
libmetawear.mbl_mw_datasignal_unsubscribe(gyro)

# disconnect
libmetawear.mbl_mw_debug_disconnect(state.device.board)

# download recap
print("Total Samples Received")
print("%s -> %d" % (state.device.address, state.samples))