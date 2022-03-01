# usage: sudo python stream_acc_gyro_bmi1.py
from __future__ import print_function
from multiprocessing.dummy import Value
from mbientlab.metawear import MetaWear, libmetawear, parse_value
from mbientlab.metawear.cbindings import *
from time import sleep
from threading import Event
from queue import Queue
from copy import deepcopy

import platform
import sys

class State:
    # init state
    def __init__(self, device):
        self.device = device
        self.samples = 0
        self.accCallback = FnVoid_VoidP_DataP(self.acc_data_handler)
        self.gyroCallback = FnVoid_VoidP_DataP(self.gyro_data_handler)
        self.readings = Queue()

    # acc callback function
    def acc_data_handler(self, ctx, data):
        value = deepcopy(parse_value(data))
        self.readings.put_nowait([value.x, value.y, value.z])
        self.samples+= 1

    # gyro callback function
    def gyro_data_handler(self, ctx, data):
        value = deepcopy(parse_value(data))
        acc = self.readings.get_nowait()
        gyro = [value.x, value.y, value.z]
        # [acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z]
        value_acc_gyro = acc + gyro
        print("ACC: %s GYRO: %s" % (value_acc_gyro[0:3], value_acc_gyro[3:]))
        print("--------------------")
        self.samples+= 1

# init
# connect to C5:DE:74:B6:AC:5F
address = 'C5:DE:74:B6:AC:5F'
d = MetaWear(address)
d.connect()
print("Connected to " + d.address)
state = State(d)

# configure all metawear
libmetawear.mbl_mw_settings_set_connection_parameters(state.device.board, 7.5, 7.5, 0, 6000)
sleep(1.5)

# config acc
libmetawear.mbl_mw_acc_set_odr(state.device.board, 25)
libmetawear.mbl_mw_acc_set_range(state.device.board, 16.0)
libmetawear.mbl_mw_acc_write_acceleration_config(state.device.board)

# config gyro
libmetawear.mbl_mw_gyro_bmi160_set_range(state.device.board, GyroBoschRange._1000dps);
libmetawear.mbl_mw_gyro_bmi160_set_odr(state.device.board, GyroBoschOdr._25Hz);
libmetawear.mbl_mw_gyro_bmi160_write_config(state.device.board);

# get acc signal and subscribe
acc = libmetawear.mbl_mw_acc_get_acceleration_data_signal(state.device.board)
libmetawear.mbl_mw_datasignal_subscribe(acc, None, state.accCallback)

# get gyro signal and subscribe
gyro = libmetawear.mbl_mw_gyro_bmi160_get_rotation_data_signal(state.device.board)
libmetawear.mbl_mw_datasignal_subscribe(gyro, None, state.gyroCallback)

# start acc
libmetawear.mbl_mw_acc_enable_acceleration_sampling(state.device.board)
libmetawear.mbl_mw_acc_start(state.device.board)

# start gyro
libmetawear.mbl_mw_gyro_bmi160_enable_rotation_sampling(state.device.board)
libmetawear.mbl_mw_gyro_bmi160_start(state.device.board)

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